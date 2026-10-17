# labscript suite: architectural and design problems

Date: 2026-10-01

This document lists the design decisions and structural problems that limit the labscript
suite, as judged from the code review in `REVIEW.md` (same directory). `REVIEW.md` lists
individual bugs and cruft with file and line. This document covers the larger changes.

The assessment comes from reading the code. The suite was not run with hardware, and no GUI
was launched. The first three sections are the most important.

## 1. No tests, and an architecture that makes tests hard to write

No repo has a test or lint job. The only workflow in each repo is `release.yml`.
Consequences found in the review:

- `labscript/utils.py:210` (`dtype=np.dtype`) is a one-character regression from 2024-01
  that breaks compilation for common NI and PrawnDO configurations.
- The `'a256'` dtype strings fail on numpy 2.5 in three repos.
- Qt6 support changed the meaning of check-state truthiness, and nothing detected it.

Without tests, none of the refactors below can be done safely. The causes are structural:

- **BLACS has no headless core.** The shot queue is a `QStandardItemModel`
  (`blacs/experiment_queue.py`). The queue manager and the tab state machine
  (`blacs/tab_base_classes.py`) call into the Qt main thread throughout. BLACS cannot run
  without a display, so it cannot run in CI.
- **lyse and runmanager store primary state in Qt item models.** Examples are lyse's
  filebox and runmanager's groups and axes models. runmanager has a partly separate library
  (`runmanager/__init__.py`), which is the model to follow.
- **labscript compiles through global state.** The `compiler` singleton, device names
  injected into the Python namespace, and `from pylab import *` mean that a compile is not
  a function that can be called twice in one process. runmanager works around this with a
  batch compiler subprocess.

Proposed direction:

- Split each program into a Qt-free core and a GUI.
- Make `labscript` compile from an explicit context object, with the singleton kept as a
  thin compatibility layer for existing scripts.
- Add an end-to-end test with dummy devices: compile a shot, run it through a headless
  BLACS, and analyse it.

## 2. Float time in the compiler

Times are floats. They are rounded to 10 decimals at instruction entry and quantised per
pseudoclock late in compilation. Bugs from `REVIEW.md` that come from this:

- Part 1 item 6: the ramp tick count is one short when the sample rate equals the clock
  limit (`labscript/core.py:419-426`).
- labscript B1: clock-limit checks reject pulses of exactly the minimum period, depending
  on t (`labscript/core.py:229, 262, 289`).
- Part 1 item 7: ramp collision detection (`labscript/outputs.py:432-447`).

Proposed direction: convert times to integer multiples of the clock resolution at
instruction entry, and do all comparisons and tick counts in integers. This removes the
class of bug, not just the instances found.

Open question: devices on different pseudoclocks have different resolutions, so the
integer unit must be chosen per pseudoclock, or one common base unit must be chosen for
the whole shot.

## 3. Each device is four loosely coupled implementations

A device consists of a labscript class, a BLACS tab, a BLACS worker and a runviewer parser.
These are coupled only by an HDF5 group layout that each device defines for itself and
does not document.

- **Runviewer parsers reverse-engineer hardware instructions.** Each parser is a second
  implementation of its device, and nothing checks it. The review found broken parsers for
  PrawnDO, PrawnBlaster (two bugs), PulseBlaster (`LONG_DELAY`), NI_DAQmx (PFI-style
  connection names) and no parser at all for PulseBlasterESRPro500. The design is
  defensible, because it shows what the hardware will do. It is only useful if CI compares
  the parser output with the output that the compiler intended.
- **Pseudoclock instruction reduction is copied** between PineBlaster, PrawnBlaster,
  PrawnDO and DummyPseudoclock. The copies have diverged (missing `continue`, wrong
  `np.insert` indices, wrong `clock_limit` scaling).
- **The worker interface is implicit.** There is no abstract base class that states what
  `transition_to_buffered`, `program_manual`, `transition_to_manual` and the abort methods
  must accept and return. Devices drift: `DummyPseudoclock` has no
  `abort_transition_to_buffered`, and `device_base_class.py` treats a `{}` return as
  failure.
- **`labscript-devices` holds every device and every vendor dependency.** PyDAQmx,
  PyNIVision, spinapi and PyVISA are hard dependencies. Devices that cannot run on the
  current stack (`imaqdx_server.py`, `LightCrafterDMD.py`, `CiceroOpalKellyXEM3001.py`) are
  not marked as unmaintained. PulseBlaster variants duplicate about 400 lines.

Proposed direction:

- Shared base code for pseudoclock instruction reduction and its parser.
- A formal worker interface (abstract base class with documented return values).
- Round-trip tests: compile a shot, run the parser, and compare with the intended output.
- A support tier per device. Unmaintained devices move out of tree. `device_registry`
  already supports out-of-tree devices through `register_classes.py`.
- Vendor packages become optional extras.

## 4. HDF5 as storage, interchange format and lock target

- **`h5_lock` monkeypatches `h5py.File` process-wide.** It needs a lock server (`zlock`), a
  kill lock, and a workaround for h5py's own lock (`labscript_utils/h5_lock.py`). It
  changes behaviour for every library in the process, and it currently breaks
  `h5py.File(path)` with no mode argument.
- **There is no schema and no format version for shot files.** There is also no single
  access library. Every program uses h5py directly, which is why `'a256'` must be fixed
  separately in `labscript`, `blacs` and `labscript-devices`.
- **Globals files are HDF5.** They cannot be diffed, merged or reviewed in version
  control. A text format for globals would probably be the largest usability gain for the
  least work.
- **Three ad hoc serialisations coexist.**
  - `repr`/`eval`: BLACS front panel and plugin data, `labscript_utils/settings.py`.
  - JSON in attributes with a native-type fallback: `labscript_utils/properties.py`, with
    content-dependent round-trip types.
  - Fixed-width byte strings, which are ASCII-only and limited to 256 characters.

Proposed direction:

- One shot-file access library (growing from `labscript_utils.shot_utils`) with a
  documented and versioned schema. Programs stop using h5py directly for shot files.
- Explicit locking in that library instead of the global monkeypatch.
- One serialisation (JSON) for settings and properties.
- A text globals format, with import from existing HDF5 globals files.

## 5. BLACS state machine and process model

- The tab state machine is a hand-written coroutine scheduler built on generators,
  threads and `inmain` calls. It was written before `asyncio` existed. Several hangs in
  `REVIEW.md` come from error handling inside it (blacs B2, Part 1 items 11 and 12).
- The queue manager (`experiment_queue.py`, `manage()`) is one long function with one
  hard-coded 300 s timeout. There is no per-device failure policy, and closing BLACS
  during a shot has no guard.
- Workers are separate processes that exchange pickles over ZMQ.

Proposed direction: after section 1 provides a headless core and tests, rewrite the state
machine on `asyncio` or as a much smaller explicit state machine, and split `manage()` into
tested steps with defined failure handling.

## 6. Bespoke infrastructure with a small maintainer base

Custom components: `zprocess`, `zlock`, `zlog`, `qtutils`, the double import denier, the
custom excepthook and `Thread.run` monkeypatch, the `.pth` file that runs on every
interpreter start (`labscript_profile`), `labscript_utils/versions.py`, and the `setup.py`
editable-install hook.

Each component is reasonable in isolation. Together they form a large body of code that
few people understand. Several depend on private behaviour of setuptools or h5py.

Proposed direction: review each component and decide whether a standard-library or
widely used alternative now exists (for example `threading.excepthook`, entry points
instead of the `.pth` file, `importlib.metadata` for versions). Remove those that have no
callers.

## 7. Nine repos, one product

A change such as Qt6 support or the numpy dtype fix needs coordinated releases across
repos that have no integration test between them. The copies of `release.yml` and
`__version__.py` have drifted. Version floors (`requires-python`, numpy, h5py, qtutils)
are inconsistent and stale.

Proposed direction: a monorepo, or a shared reusable workflow plus one integration-test
repo that installs all components from their development branches.

## 8. lyse's data model

- The dataframe is held in the GUI process and pickled in full over ZMQ on every `data()`
  call.
- Analysis routines learn their context from module globals (`lyse.path`, and the
  `sys.argv` check in `lyse/__init__.py:58-62`).
- Live updates and reload-from-file take different code paths and give different results
  (lyse B8 in `REVIEW.md`).
- Object-dtype columns are the norm, which is the source of the pandas 3 breakage.

Proposed direction: one code path that builds a row from a shot file, used for both live
updates and reload. Incremental or filtered dataframe transfer. An explicit context
argument for routines, with the module globals kept for compatibility.

## A scope limit, not a defect

Shots are fully precompiled, and `wait()` is the only run-time behaviour. Conditional
branching within a shot is not possible. This is a deliberate boundary of the design, and
this document does not propose changing it.

## Proposed order of work

1. Headless compile test with dummy devices, and parser round-trip tests (sections 1
   and 3). This needs no architectural change and gives a safety net for everything else.
2. Integer time in the compiler (section 2).
3. Formal worker interface and shared pseudoclock code (section 3).
4. Qt-free cores, BLACS first (sections 1 and 5).
5. Shot-file schema and access library, then text globals (section 4).

Sections 6, 7 and 8 are independent of this order and can be done at any point.

The immediate bug fixes in `REVIEW.md` Part 1 (numpy 2.5, `bitfield`, NI analog input,
PrawnBlaster and PrawnDO compile paths) should be released before any of this work starts.
