# Open pull requests across the labscript suite, reviewed 2026-10-17

Scope: every open PR on every repository under github.com/labscript-suite and on the
related repositories under github.com/chrisjbillington (zprocess, spinapi, desktop-app,
ci-helper, workflow-sandbox, qtutils, setuptools-conda, pynivision), except runmanager
#130 (the large refactor), which was reviewed separately and was merged upstream on
2026-10-17. 30 PRs in total. Repos with no
open PRs: labscript, runviewer, labscript-suite, labscript-c-extensions,
vendored-conda-builds, spinapi, ci-helper, workflow-sandbox, qtutils, pynivision, mise,
bias, opalkellyxem3001, pineblaster, and the two website repos.

Each PR's head is fetched in its local clone as `origin/pr/<N>`. "Merges" means
`git merge-tree` against the upstream default branch reports no conflict.

Importance: 5 = act now, 1 = close. Section 1 is the ranked list, section 2 has one
paragraph per PR, section 3 contains the detailed per-group reports.

## 1. Ranked list

| # | PR | Type | Imp. | Merges | Recommended action |
|---|---|---|---|---|---|
| 1 | blacs #123 plugin-loading bugfixes (ispielma, 2026) | bugfix | 4 | merged 2026-10-17 (d061535) | Merged as is after testing; the comment trim rides the next blacs pull request |
| 2 | labscript-devices #110 Windfreak SynthHD (dihm, 2024) | feature | 4 | yes | Merge after three one-line fixes |
| 3 | labscript-devices #126 AD9959 DDS Sweeper (carterturn, 2025) | feature | 4 | yes | Merge after deleting the dead runviewer parser and fixing `clock_limit` |
| 4 | zprocess #14 PAIR sockets (mjdoris, 2021) | bugfix, behaviour change | 3 | conflict | Maintainer rework: 14 real lines plus a version check for mixed zprocess versions |
| 5 | labscript-devices #148 TriggerableCamera + DummyCamera (ispielma, 2026) | refactor, feature | 3 | yes | Design feedback to author, hardware test, then merge; merge #144, #87, #63 first or re-apply onto it |
| 6 | labscript-devices #144 Andor fixes (TesseTiemens, 2026) | bugfix | 3 | yes | Ask author: SyntaxError on Python < 3.12, wrong model string, semaphore deadlock |
| 7 | lyse #132 data-group attributes in dataframe (chrisjbillington, 2026) | feature | 3 | yes | Merge after changing overwrite to merge-into-existing |
| 8 | labscript-utils #117 minimal example analysis script (Json-To-String, 2025) | docs-example | 3 | yes | Merge after fixing the `save_result` TypeError and axis label |
| 9 | PrawnBlaster #37 overclock voltage logic (Json-To-String, 2025) | firmware | 3 | yes | Merge after fixing response ordering and the stale release workflow |
| 10 | PrawnBlaster #35 variable instructions per pseudoclock (philipstarkey, 2025) | firmware, feature | 3 | yes | Maintainer rework: missing `ok` reply, unvalidated index, needs host-side PR |
| 11 | blacs #105 Virtual Devices plugin (carterturn, 2024) | feature | 3 | yes | Ask author: finish enum outputs, replace 10 Hz polling thread; the two output_classes fixes can merge alone |
| 12 | labscript-devices #129 Keysight oscilloscope (K-Takouti, 2025) | feature | 3 | yes | Ask author for a second round (compile-time VISA scan, `*RST`, unverified acquisition) |
| 13 | zprocess #21 fix remote example (restelli, 2024) | docs-example | 3 | yes | Redo as a small maintainer commit instead of merging |
| 14 | labscript-devices #87 autoscale + background subtraction (chrisjbillington, 2021) | feature | 2 | yes | Merge after guarding `set_bg_image`; re-apply onto #148 |
| 15 | labscript-devices #63 restore display ranges (zakv, 2020) | feature | 2 | yes | Merge after switching to `ui.histogram.getLevels()`; re-apply onto #148 |
| 16 | runmanager #104 + blacs #90 compilation queue (chrisjbillington, 2022) | feature, WIP | 2 (4 as design record) | conflict | Close as superseded by #130; convert the requirements to an issue |
| 17 | runmanager #128 config path in title (ispielma, 2026) | feature | 2 | conflict (since #130 merged) | Ask author: depends on a closed labscript-utils PR; drop the QShortcut hunk |
| 18 | labscript-devices #106 GeniCam cameras (TerryGeng, 2023) | feature | 2 | yes | Ask to rebase as a thin TriggerableCamera subclass, else close as stale |
| 19 | labscript-devices #130 Stahl BS 34-1A (OljaKhor, 2025) | feature | 2 | yes | Rework as a static device or close |
| 20 | labscript-devices #53 DummyIntermediateDevice widgets (rpanderson, 2020) | feature | 2 | conflict | Close as stale or maintainer rework |
| 21 | blacs #88 lock monitor plugin (zakv, 2021) | feature | 2 | yes | Close as out of scope; belongs in a separate package |
| 22 | prawn_digital_output #23 testing notebook (dihm, 2025) | tooling | 2 | yes | Merge after stripping outputs and fixing the save branch |
| 23 | setuptools-conda #5 extras support (philipstarkey, 2020) | feature | 2 | conflict | Close; untested and the parser it modifies was rewritten |
| 24 | lyse #118 + #85 rename Run to Shot (dihm 2024, philipstarkey 2020) | refactor | 1 | conflict | Close; participants agreed to abandon in 2025 |
| 25 | blacs #121 shared plugin refactor (ispielma, 2026) | refactor | 1 | yes | Close; depends on closed labscript-utils PRs, superseded by #123 |
| 26 | blacs #89 retry on timeout (mjdoris, 2021) | workaround | 1 | yes | Close; duplicates jobs if the worker did receive the message |
| 27 | desktop-app #6 Windows CI (rpanderson, 2020) | tooling-CI | 1 | conflict | Close as obsolete |
| 28 | pineblasterv2 #1 Wi-Fire pseudoclock (ARFritsch, 2020) | firmware | 1 | yes | Close; archive the repo |

## 2. One paragraph per PR

### Merge soon (importance 4)

**blacs #123.** Three real fixes: `ConfigParser` section inheritance of `[DEFAULT]`
keys makes `import blacs.plugins` raise `ValueError` when a plugin directory name
collides with a labconfig default, so BLACS does not start; `plugin_setup_complete` is
retried on any exception, so a plugin with an optional-argument signature runs its side
effects twice; and an undocumented third commit fixes `str.strip('.h5')` in
compile_and_restart.py. The `has_option()` change is a no-op, because `has_option` also
consults `[DEFAULT]`; the `try/except ValueError` is the real fix. Independent of #121.

**labscript-devices #110.** Static-only Windfreak driver, in lab use since 2022,
structured like TekScope, `windfreak` imported only in the worker. Defects: a
`LabscriptError(...)` constructed but not raised, `self.device.name` where `self.name`
is meant, and a wrong-case import path in the docs. Unreviewed for two years.

**labscript-devices #126.** Hardware-tested by two groups. The labscript device and
BLACS worker are sound. The runviewer parser is dead code (undefined `DDSs`, `np.float`,
mismatched keys). `clock_limit` is derived from the AD9959 reference clock where the
Pico system clock is the real limit. `sweep_mode != 0` is accepted but unsupported.
Waiting on dihm's final review since 2025-09.

### Worth doing with rework (importance 3)

**zprocess #14.** Your own "more aggressive option" from blacs #89: PUSH/PULL to PAIR
for the parent-child sockets plus explicit POLLIN/POLLOUT flags, which are required with
PAIR because `get()` would otherwise wake on POLLOUT and block in `recv`. One lab, one
week of evidence. The diff is mostly whitespace churn and now conflicts with the 2026
heartbeat changes. PAIR refuses the handshake with a PUSH/PULL peer, so mixed zprocess
versions on remote worker computers fail with no useful error; a version check in the
parent-info handshake is needed. Moot for shotscript.

**labscript-devices #148.** Separates the generic camera device/tab/worker from the
IMAQdx backend and adds a DummyCamera that evaluates an image function at compile time
and stores uint16 arrays in the shot file. Vendor behaviour is preserved and three latent
master bugs are fixed. Defects: removing `mock` makes existing connection tables that
pass `mock=False` fail to compile (labscript rejects unknown kwargs); the RuntimeError
guard against worker subclasses overriding `get_attributes_as_dict` breaks a documented
pattern; stray positional args reach the image function; long LLM-style comments.
Conflicts with #144, #87 and #63.

**labscript-devices #144.** Valid Andor fixes (cooldown before EM gain, EM gain mode,
`GetKeepCleanTime` guard, EM-gain range check). Broken as written: a nested same-quote
f-string is a SyntaxError on Python < 3.12 so AndorSolis would not import; the model
string compared is `'IXON ULTRA'` where the enum yields `'IXONULTRA'`, so iXon Ultra crop
mode regresses; the new range check excludes endpoints; the semaphore is released only
in single mode so kinetic modes deadlock. The andor_utils.py fixes do not overlap #148.

**lyse #132.** Four lines. `row[groupname] = get_attributes(datagroup)` overwrites a
results group of the same name, which is the documented FunctionRunner pattern.

**labscript-utils #117.** Device and dataset names match the default profile. The last
line passes a dict of arrays to `save_result`, which raises TypeError; the x label says
ms but the rows are clock ticks. #116 was closed unmerged and this does not depend on it.

**PrawnBlaster #37.** Based on `origin/overclock` (master plus #36 and a bounds fix);
merges into both. Voltage is set before `src` validation and before the clock change, so
a failed change leaves voltage mismatched; the >200 MHz warning is printed before `ok`,
which breaks the host worker's `send_command_ok`; `build.yaml` and the readme still
reference `_overclock.uf2` files that are no longer built; VERSION not bumped; host side
still caps at 133/150 MHz.

**PrawnBlaster #35.** Memory accounting is right. `setnuminstructions` never replies
`ok`; `set`/`get`/`setb` compute the per-pseudoclock offset from an unvalidated index
before the bounds checks; `setb` keeps an off-by-one that rejects a full program; no
`getnuminstructions`; labscript-devices has no way to send per-pseudoclock counts.

**blacs #105.** Self-contained, labscript-utils dependency merged in 2023. Enum-output
support is unfinished (the tree row is never appended; `vd['EO']` KeyError for older
save data); a 10 Hz polling thread does `inmain` round-trips for the life of BLACS;
channel tuples are parsed back from display text; qtutils star imports that master
removed; 37 commits with 18 duplicated. The two `output_classes.py` inverted-digital
fixes are correct and could merge alone. The requirement (cross-device channel groups
in one tab) is relevant to shotscript control.

**labscript-devices #129.** Config-slot design is reasonable. The labscript class probes
every VISA resource at compile time to find the scope by serial number; the tab imports
PyQt5 directly; the worker sends `*RST` at startup and writes default setups into empty
slots; acquisition is never verified so stale data is saved on a missed trigger;
`create_group('/data/traces')` collides on reuse; only the last channel's preamble is
saved. dihm promised a review and did not return.

**zprocess #21.** Correct diagnosis (the example defines its `Process` subclass in
`__main__`, which the remote check rejects). The fix leaves the old class as a dead
string literal, copies a license header naming the wrong file, has a typo, and puts the
package under `zprocess/examples/`, which is not a package. Five minutes to do properly.

### Low priority (importance 2)

**labscript-devices #87.** Your own PR. zakv's reported crash is real: "Set background"
before any frame does `None.swapaxes`; a shape-mismatched background raises in the
handler. The description overstates prior behaviour (master autoscaled only the first
frame).

**labscript-devices #63.** `self.image.getLevels()` does not exist on
`pyqtgraph.ImageView` (checked against 0.14.0; it is on `HistogramLUTItem`), so saving
tab state raises whenever an image is shown. Otherwise fine.

**runmanager #104 + blacs #90.** #104 conflicts with master, which since the merge of #130
on 2026-10-16 has the compile functions in compiler.py. blacs #90 merges but depends on
`runmanager.new_rep_name`, which exists only in #104. Defects: `new_rep_name` off by one;
compile error clears the whole queue; abort no longer discards remaining shots; dynamic
globals substitute whole evaluated lists for scan globals; at most one shot compiled per
BLACS report. The design question (BLACS REQ to a labconfig-named runmanager, blocking up
to 5 s in the queue thread) should become PUB/SUB plus one initial request. shotscript's
sequencer already implements just-in-time compilation with `lookahead` and `override`.

**runmanager #128.** Imports `LabscriptApplication` from `labscript_utils.labconfig`,
which exists only in closed labscript-utils PRs 125/127, so it fails at import. The
companion PRs on blacs, lyse and runviewer were closed; this is the orphaned fifth part.
It also reverts `QtGui.QShortcut` to `QtWidgets.QShortcut`, undoing master's Qt6
compatibility commit, and silently moves the default config directory.

**labscript-devices #106.** About 1500 of 2520 lines duplicate IMAQdxCamera; the new
parts are the harvesters backend and the feature-tree widget. Uses `np.string_` (NumPy
2 broken), raw zmq sockets bypassing zprocess security with a leaked receive thread on
restart, saves images ignoring orientation. Author silent since 2023 after agreeing to
the split that #148 now provides.

**labscript-devices #130.** The time.sleep-in-thread buffered mode is not acceptable:
timing starts at transition time rather than the trigger, `transition_to_buffered`
returns None, `abort_buffered` is missing, `program_manual` does not program the device,
a log file is created inside site-packages at import. The serial protocol knowledge is
useful; a static device with StaticAnalogOut children is the viable version.

**labscript-devices #53.** Master's DummyIntermediateDevice is unchanged since 2020, so
not superseded, but the PR conflicts with the docstring conversion, removes
`BLACS_connection`, and enforces fixed channel names; philipstarkey asked for
connection-table introspection and the author never responded.

**blacs #88.** High code quality but 3.8k lines of lab-specific policy, imports
matplotlib, and reimplements the Tab/Worker protocol because PluginTab has no state
machine. The real gap is that blacs has no entry-point plugin loading, which is why the
author proposed bundling it.

**prawn_digital_output #23.** Committed notebook outputs (192 KB of PNGs), hard-coded
`COM7`, `if SHOW_IMAGES/elif SAVE_IMAGES` so saving never happens, `conn.close()` on
None in the error path. Consistent with the PrawnBlaster repo's tests notebooks.

**setuptools-conda #5.** Untested by the author's own account. Master rewrote the
function it modifies and its parser would treat `[:marker]` sections as extras, undoing
commit b52873f. Irrelevant to shotscript, which drops conda.

### Close (importance 1)

**lyse #118 + #85.** Discussion ended 2025-04 with dihm recommending rejection (run
time/run number/n_runs cannot be renamed compatibly) and philipstarkey agreeing. 79
commits behind, conflicts in `__init__.py`, `__main__.py` and the docs. Nobody closed it.

**blacs #121.** Requires `labscript_utils.plugins` and a new `Splash` signature from
labscript-utils PRs 126/127, both closed unmerged. Deletes a test HDF5 file still
referenced by device_base_class.py and adds a `.DS_Store`. Its fixes were resubmitted as
#123.

**blacs #89.** The `put` timeouts never fire in practice; the retry triggers on the ack
`get(30)` timeout, and if the worker did receive the request the job runs twice and the
ack/result stream is permanently offset by two messages. The fix belongs in zprocess
(#14).

**desktop-app #6.** Draft from 2020 using actions that no longer run, Python 3.6 to 3.8,
an unconditional `win32com` import in the cross-platform example, debugging leftovers.
Master's release workflow builds on windows-2022 but does not test installation.

**pineblasterv2 #1.** Repo dormant since 2017 with no V2 host class in labscript-devices.
The change swaps in the v1 interrupt vector (wrong on PIC32MZ) and deletes
`detachInterrupt(0)` unguarded by board, so Max32/BitBlaster behaviour changes too. The
actual cause of the reported symptom is `readline()` stopping at `\r` with the trailing
`\n` triggering the just-attached abort interrupt.

## 3. Detailed per-group reports


## 3.x labscript-devices camera PRs

Repo: `labscript-devices`, base `origin/master`.
All five PRs merge cleanly with master on their own. Pairwise: #148 conflicts with
#144 (AndorSolis/blacs_workers.py, IMAQdxCamera/blacs_workers.py), with #87 and with
#63 (IMAQdxCamera/blacs_tabs.py, which #148 reduces to a 24-line stub). #87 and #63
merge cleanly with each other. #106 touches no shared files.

Base class on master (what #144, #87, #63 modify and #148 moves):
`IMAQdxCamera/labscript_devices.py` is the `TriggerableDevice` subclass with
`expose()` and an `EXPOSURES` table; `IMAQdxCamera/blacs_tabs.py` has `ImageReceiver`
(a `ZMQServer` that receives frames and drives a `pyqtgraph.ImageView`) and
`IMAQdxCameraTab` (buttons, attribute dialog, `get_save_data`/`restore_save_data`,
worker kwargs including `mock`); `IMAQdxCamera/blacs_workers.py` has `MockCamera`,
`IMAQdx_Camera` (the nivision wrapper, including the `grab_multiple` retry loop) and
`IMAQdxCameraWorker` (smart attribute cache, continuous acquisition thread,
`transition_to_buffered` starts a `grab_multiple` thread, `transition_to_manual` joins
it and writes `images/<orientation>/<name>/<frametype>` datasets). Pylon, Spinnaker,
FlyCapture2 and AndorSolis subclass all three and replace the interface class; Pylon
and FlyCapture2 also override the worker's `get_attributes_as_dict`, AndorSolis
overrides `get_camera` and `get_attributes_as_dict`.

---

### labscript-devices #148: Move generic camera patterns into a generic TriggerableCamera class and create a Dummy camera class (ispielma, opened 2026-09-18, last updated 2026-10-07)

- **What it does**: Copies the IMAQdx device class, tab and worker verbatim into a new
  `TriggerableCamera` package and adds `TriggerableCameraInterface`, a base class for
  the vendor interface classes that supplies `grab_multiple`, the abort flag, a composed
  `get_attributes_as_dict`, and two hooks (`is_transient_grab_error`,
  `is_skippable_grab_error`) that replace each vendor's own retry loop. The five vendor
  packages become subclasses holding only SDK code. `MockCamera` and the `mock`
  property are removed. A new `DummyCamera` evaluates a user function per exposure in
  `generate_code`, stores the resulting uint16 arrays in `devices/<name>/IMAGES`, and
  its worker reads them back in a `load_shot_data` hook and feeds them through the
  normal acquisition path.
- **Type**: refactor / feature
- **Size**: 34 files, +1858/-1063, 19 commits
- **No-brainer?**: No. Large, breaking in several ways, untested on hardware, and the
  author says most of it was written by Claude and Codex and asks for feedback rather
  than a merge.
- **Implementation**:
  Behaviour of the vendor cameras: I checked each against master and it is preserved.
  IMAQdx retries on `IMAQdxErrorTimeout` and skips other `ImaqDxError`s when
  `exception_on_failed_shot` is False (now via the two hooks); Pylon retries on
  `pylon.TimeoutException`; FlyCapture2 retries on every `Fc2error`; Spinnaker never
  retries; Andor keeps its own `grab_multiple`. Pylon's `grab(continuous=False)` becoming
  `grab()` is harmless (the parameter is unused). Andor's worker-level
  `get_attributes_as_dict` returned `self.camera.attributes`; the composed version
  over `get_attribute_names`/`get_attribute` returns the same dict.
  Three master bugs are fixed in passing: Spinnaker `close()` referenced
  `self.camList`, which was never assigned (master `SpinnakerCamera/blacs_workers.py:40`
  stores a local, `:251` reads an attribute), so shutdown raised AttributeError; Pylon
  `raise('Snap Error:', ...)` raised a tuple (TypeError) and is now a RuntimeError; the
  attributes-dialog copy button used `QtGui.QApplication`, which master's 2022
  QtGui→QtWidgets commits missed.
  Defects:
  1. Removing `mock` from the device signature is not only "the connection table reads
     as changed once". A connection table that passes `mock=False` explicitly (as the
     docs example did until this PR deletes it) now fails to compile:
     `labscript/base.py:84` raises on unknown kwargs. Needs to stay accepted and
     ignored (with a warning) for at least one release.
  2. `MockCamera` is no longer importable from `IMAQdxCamera.blacs_workers` and
     `self.mock` is no longer set on workers. Lab-local cameras written on the
     AndorSolis pattern (`if self.mock: return MockCamera()`) fail with ImportError.
  3. `TriggerableCameraWorker.init` (`TriggerableCamera/blacs_workers.py:213-220`)
     raises RuntimeError if any worker subclass defines `get_attributes_as_dict`. That
     was the documented pattern (Pylon and FlyCapture2 did it on master) and lab-local
     cameras copied it; they now refuse to start. `IMAQdxCameraWorker.init`
     (`IMAQdxCamera/blacs_workers.py:181-194`) then adds a `MethodType` monkeypatch for
     cameras that lack the method. Both are unnecessary: keep `get_attributes_as_dict`
     as a worker method that delegates to the camera (falling back to composing from
     `get_attribute_names`/`get_attribute`). Existing overrides then keep working and
     no guard or shim is needed.
  4. `DummyCamera.expose(t, name, frametype, trigger_duration, *args, function=None,
     **kwargs)`: positional arguments after `trigger_duration` are forwarded to the
     image function, so a stray fifth positional argument is silently passed on. Drop
     `*args`; keyword arguments are enough.
  5. The dummy images are stored twice per shot (`devices/<name>/IMAGES` and
     `images/<orientation>/...`). Acceptable for a test device, but worth noting.
  6. The comments are long and discursive, and many explain history or what the code
     does not do (e.g. `TriggerableCamera/blacs_workers.py:31-36, 57-60, 132-146`,
     `DummyCamera/labscript_devices.py:158-163`, all of `sensor.py`'s docstrings). The
     repo's existing style is terse. This is a lot of prose to review and maintain.
  7. `docs/source/devices/triggerablecamera.rst` has empty Installation and Usage
     sections.
  8. `exception_on_failed_shot` and `_abort_acquisition` are class attributes on the
     interface (`:66, :71`) that the worker overwrites per instance. Works, but
     instance attributes set in `__init__` would be clearer; the PR removed the
     `__init__` from the base deliberately so subclasses need not call super.
  How the image function reaches the shot file: it does not. It is called once per
  exposure during compilation with `(X, Y, *args, **kwargs)` on a metre-scaled
  meshgrid built from `Width`/`Height`/`pixel_size`/`magnification`; the result is
  checked for shape and finiteness, clipped to the `PixelFormat` bit depth, cast to
  uint16 and written as a gzip dataset. The function itself is never pickled or named
  in the file. Image order: `generate_code` sorts exposures as tuples and the worker
  sorts the structured array with `order='t'`; numpy breaks ties on the remaining
  fields in dtype order, so the two orders agree. `NOT_REAL_DATA=True` is written as an
  attribute of the image group regardless of `saved_attribute_visibility_level`.
  Design: the split (generic device + tab + worker, plus a small interface contract
  with "is this grab error a wait or a failure" hooks) is sound and is what dihm asked
  for on #106 in 2023. The dummy camera is a reasonable way to test compile → BLACS →
  lyse without hardware. The costs are the breaking changes above and the volume of
  LLM-written prose.
- **Up to date?**: Merges cleanly; 0 commits behind master. Conflicts with #144 (both
  worker files), #87 and #63 (tab file). `.ui` files move into `TriggerableCamera/`;
  packaging uses `include-package-data` with setuptools_scm, so they are still shipped.
- **Tested?**: Author: tested in Dummy mode only, "still needs lab testing". No vendor
  camera has been run. The vendor changes are mechanical enough that this is plausible
  but not sufficient for a merge.
- **Discussion state**: Author explicitly requests feedback, not a merge. No review
  comments yet. Ball with maintainers.
- **Breaking?**: Yes: `mock` kwarg removed (compile failure where passed explicitly;
  connection-table property set changes for every camera, so BLACS flags every camera's
  connection table as changed once); `MockCamera` import removed; worker subclasses
  overriding `get_attributes_as_dict` refuse to start; `grab_multiple` signature loses
  `waitForNextBuffer` (the worker never passed it, so third-party cameras are
  unaffected).
- **Rewrite relevance**: The interface contract (set/get attributes, snap, configure,
  grab, stop, close, plus the transient-vs-fatal grab error hook) is the right shape for
  shotscript's camera devices, and a dummy camera whose frames are computed at compile
  time from a function of the globals is a useful end-to-end test fixture.
- **Importance**: 3. Right direction, but needs design feedback, hardware testing and
  a compatibility pass before merging.
- **Recommended action**: Ask author for: (1) keep accepting `mock` (ignored, with a
  warning); (2) replace the override guard and the `MethodType` shim with a worker
  `get_attributes_as_dict` that delegates to the camera; (3) drop `*args` from
  `DummyCamera.expose`; (4) cut comments to the repo's style; (5) run at least IMAQdx
  and Pylon on hardware. Decide the ordering with #144/#87/#63 (see end).

---

### labscript-devices #144: Bugfixes for older andor cameras, using cooldown and emccd gain (TesseTiemens, opened 2026-03-20, last updated 2026-03-20)

- **What it does**: In `andor_utils.py`: adds `em_gain_mode` and calls `SetEMGainMode`
  before reading `GetEMGainRange`; moves cooldown before EM-gain setup; adds
  `wait_until_cool`/`wait_until_stable` attributes; rewrites the EM gain range check;
  wraps `GetKeepCleanTime` in try/except; uses `SetIsolatedCropMode` instead of
  `SetIsolatedCropModeEx` unless the model is an iXon Ultra; adds
  `setup_acquisition_fast` (trigger and shutter only) and a `semaphore` argument to
  `acquire()` that is released after `StartAcquisition()`. In the Andor worker:
  `configure_acquisition` takes the fast path when attributes are unchanged,
  `grab_multiple` accepts the semaphore, single mode appends `downloaded[0]`. In
  `IMAQdxCameraWorker.transition_to_buffered`: if the camera class has
  `supportSemaphore`, block until the acquisition thread releases it.
- **Type**: bugfix / feature
- **Size**: 3 files, +120/-33, 3 commits
- **No-brainer?**: No. Several of the fixes are correct and needed, but the PR as
  written does not import on Python < 3.12 and introduces two regressions.
- **Implementation**: Each claimed fix against master (`AndorSolis/andor_sdk/andor_utils.py`):
  1. Cooldown before EM gain: master sets EM gain at `:300` and cools at `:303`. The
     SDK's EM gain range depends on sensor temperature, so the swap is correct.
  2. EM gain check: master `:204` `if not emccd_gain in self.emccd_gain_range` tests
     membership in the `(low, high)` tuple returned by `GetEMGainRange`
     (`andor_solis.py:1449`), so only the two endpoints were accepted. Real bug. The
     replacement uses strict `>` and `<`, which rejects the endpoints. Should be
     `low <= emccd_gain <= high`.
  3. `GetKeepCleanTime` try/except: fine; the value is only printed.
  4. Crop mode fallback: `self.model` is the list returned by `camera_type.get_type`
     (`andor_capabilities.py:72-73`), whose member for the Ultra is `IXONULTRA`
     (`:61`). The PR compares `self.model[0]` with `'IXION ULTRA'` (typo) in the
     crop branch and `'IXON ULTRA'` in the uncrop branch. Neither matches, so
     `SetIsolatedCropModeEx` is never called: iXon Ultra users lose the
     `left_start`/`bottom_start` crop offsets that worked on master.
  5. `images.append(downloaded[0])`: `download_acquisition` returns shape
     `(N, Ny, Nx)` (`:603-612`), so master's single mode appended 3-D arrays, giving a
     3-D dataset per frame and a 4-D block for the GUI. Valid fix when
     `number_kinetics == 1`; `images.extend(list(downloaded))`, as the other two
     branches already do, would be consistent and not drop frames otherwise.
  6. `em_gain_mode`: `SetEMGainMode` exists (`andor_solis.py:1506`). Fine. Leaves two
     debug `print(GetEMGainRange())` calls.
  7. Wait flags default True, so default behaviour is unchanged. Fine.
  8. Semaphore: `aquisitionSemaphore.acquire()` in the worker has no timeout.
     `acquire()` releases it only inside the `DRV_IDLE` branch, and the Andor
     `grab_multiple` passes it only in the `'single'` branch. `supportSemaphore` is a
     class attribute, so in `kinetic_series` and `fast_kinetics` modes nothing ever
     releases it and `transition_to_buffered` blocks forever. Same if `acquire()`
     raises before `StartAcquisition()`. Needs a timeout and a release in a `finally`,
     in every mode.
  9. `setup_acquisition_fast`: leaves `print(f'full attrs: ...')`. The fast path is
     taken when `self.attributes == self.conf_attributes`; since
     `manual_mode_camera_attributes` normally differ from `camera_attributes`, the
     attributes change on every transition and the fast path is only hit when the
     manual attributes are empty.
  10. Python version: `print(f'setting em gain mode to
      {self.acquisition_attributes['em_gain_mode']}')` nests the string's own quote
      inside the f-string, which is a SyntaxError before Python 3.12 (PEP 701).
      `pyproject.toml` requires `>=3.8`. Importing `andor_utils` fails, so AndorSolis
      is unusable on 3.8–3.11.
  11. Status polling interval in `homemade_wait_for_acquisition` goes from 50 ms to
      1 ms (1 kHz `GetStatus` calls). Probably fine, undocumented.
- **Up to date?**: Merges cleanly; 3 commits behind, none touching Andor or IMAQdx.
  Conflicts with #148 on both worker files. `andor_utils.py` is untouched by #148, so
  the SDK-level fixes apply either way; the semaphore hook would have to move to
  `TriggerableCameraWorker`.
- **Tested?**: On an iXon 855 (not an Ultra), so the model-name bug would not have
  shown, and presumably on Python 3.12+, so neither would the f-string.
- **Discussion state**: Author asked whether the fast setup and semaphore should be a
  separate PR. No maintainer response in seven months. Ball with maintainers.
- **Breaking?**: Crop mode on iXon Ultra regresses (defect 4). Non-single acquisition
  modes deadlock (defect 8). Otherwise defaults are preserved.
- **Rewrite relevance**: `StartAcquisition()` takes 90–120 ms on this camera and
  shots started before it returned; the rewrite's camera worker should make "armed"
  the completion condition of transition-to-buffered rather than starting a thread and
  returning. Also: EM gain range depends on temperature, so cool first.
- **Importance**: 3. Real fixes for Andor users, but unmergeable as written.
- **Recommended action**: Ask author for: f-string quoting; compare with
  `'IXONULTRA' in self.model`; inclusive range check; `extend(list(downloaded))`;
  remove debug prints; either release the semaphore in all modes with a timeout or
  split the semaphore and `setup_acquisition_fast` into a second PR as offered. Then
  merge the `andor_utils.py` fixes before #148 (they do not conflict with it).

---

### labscript-devices #106: Adding support for GeniCam-compatible cameras (TerryGeng, opened 2023-06-06, last updated 2023-07-14)

- **What it does**: Adds a `GeniCam` package driving GenICam/GenTL cameras through
  `harvesters`: a device class copied from `IMAQdxCamera` (plus `cti_file`,
  `manual_acquisition_timeout`, GenICam visibility names `beginner/expert/guru`, minus
  `pixel_size`/`magnification`), a worker that is `IMAQdxCameraWorker` rewritten around
  a `GeniCam` backend object, a tab that receives frames on a raw zmq REP socket and
  shows them in a new `GeniCamWidget`, and a 511-line Qt tree widget for browsing and
  editing the camera's feature tree.
- **Type**: feature
- **Size**: 14 files, +2520/-0, 1 commit
- **No-brainer?**: No. Three years stale, draft by the author's own description,
  NumPy 2 incompatible, and structurally what #148 now provides generically.
- **Implementation**: Duplication: `labscript_devices.py` is IMAQdxCamera's with
  edits (same docstring, `expose`, `generate_code`); `blacs_workers.py`
  `transition_to_buffered`/`transition_to_manual`/`abort`/continuous loop are IMAQdx's
  line for line, with `print` replaced by a logger; the tab duplicates `exp_av`, frame
  reception and worker kwargs. Genuinely new code is `_genicam/` (~500 lines: Harvester
  wrapper, feature tree model) and the two widgets (~650 lines). Under #148 the whole
  package would be a `TriggerableCamera` subclass, a 10-line tab and worker, and
  `_genicam.py` as the interface class (it already has snap/fetch/start/stop/abort/
  close), plus the attribute-tree widget, which dihm asked to go to labscript_utils.
  Defects:
  1. `np.string_` three times (`blacs_workers.py:316-318`): removed in NumPy 2.0.
     Master fixed the same lines in IMAQdx (b40cf0d, 2025-11-15); the copy did not
     get the fix.
  2. Frame transport bypasses `labscript_utils.ls_zprocess`: the tab binds a plain
     `zmq.REP` on a random port 50000–59999 (`blacs_tabs.py:65-67`) and the worker
     uses a plain `zmq.Context()` (`blacs_workers.py:80`), so zprocess's shared-secret
     security is not applied. The receive thread is never stopped and `restart()` has
     the socket close commented out (`blacs_tabs.py:152-157`), leaking a thread and a
     bound port per tab restart.
  3. Images are saved under `images/<device_name>` (`blacs_workers.py:282`),
     ignoring `orientation`, unlike every other camera.
  4. `feature_tree["Acquisition"]["AcquisitionFrameCount"]` is hard-coded
     (`blacs_workers.py:235`); the SFNC category is `AcquisitionControl` and vendors
     differ, so other cameras raise KeyError. Setting `AcquisitionMode` is a TODO.
  5. `saved_attribute_visibility_level` default `'beginner'` while the docstring still
     documents `'intermediate'`. `serial_number` is used as a string (no hex
     conversion), which is right for harvesters but differs from the other cameras.
  6. A `RichStreamHandler` is added to a named logger on every worker `init`, so a
     worker restart duplicates every log line.
  7. `get_save_data`/`restore_save_data` have TODOs; attribute visibility is not
     restored.
  8. `genicam_test.py` (182 lines) is a standalone script inside the package.
  9. Spelling: the standard is GenICam, not GeniCam, throughout.
  Dependency: `harvesters` depends on the `genicam` binary wheels published from the
  EMVA reference implementation, which have historically lagged new Python releases by
  months to a year (not verified here; no network). A vendor GenTL producer (`.cti`)
  is still required, so this replaces NI's SDK, not vendor SDKs in general.
- **Up to date?**: Merges cleanly (no shared files); 81 commits behind. Master's
  NumPy 2 fix to the code it copied is missing. Would be far smaller on top of #148.
- **Tested?**: Author: extensively on an Allied Vision Mako G-131B. Plausible for
  that camera.
- **Discussion state**: dihm reviewed twice (2023-06-27, 2023-07-14) asking for a
  generic/backend split and widgets in labscript_utils; the author agreed to the split
  and has been silent since 2023-06-27. Ball with the author; effectively abandoned.
- **Breaking?**: No (new device).
- **Rewrite relevance**: GenICam via harvesters is the vendor-neutral way to drive
  most machine-vision cameras (Allied Vision, Basler, FLIR, IDS), so one GenICam backend
  could replace separate Pylon/Spinnaker/FlyCapture2/IMAQdx classes in shotscript; the
  category → feature → visibility tree is the right model for an attribute browser.
- **Importance**: 2. Good idea, stale and superseded in structure.
- **Recommended action**: Ask author whether they will rebase as a thin
  `TriggerableCamera` subclass once #148 lands (or as an `IMAQdxCamera` subclass if it
  does not); otherwise close as stale and keep the branch as reference for a future
  GenICam backend.

---

### labscript-devices #87: IMAQdxCamera: optional autoscaling, and background subtraction (chrisjbillington, opened 2021-08-20, last updated 2021-08-22)

- **What it does**: Adds three buttons to the tab UI: a checkable "Auto Levels" that
  makes every displayed frame autoscale levels and histogram range, and "Set
  background"/"Clear background" that store the current frame in `ImageReceiver` and
  subtract it (as float) from displayed frames. `ImageReceiver.handler` now delegates
  to a new `update_image()`. `autolevels` is added to the tab save data.
- **Type**: feature
- **Size**: 2 files, +100/-12, 1 commit
- **No-brainer?**: No, only because of one known crash; otherwise small and
  self-contained.
- **Implementation**:
  1. "Set background" before any frame has arrived: `set_bg_image` sets
     `bg_image = None` and calls `update_image()`, where `image = self.image` is None
     and `image.swapaxes` raises AttributeError (reported by zakv; confirmed in the
     diff). Guard on `self.image is None`.
  2. A background of a different shape from the incoming frame (ROI change, or a
     2-D background against the 3-D block sent after a shot, or vice versa) raises
     ValueError inside the main-thread handler after `ok` has already been sent to the
     worker. Should fall back to no subtraction when shapes differ.
  3. Subtraction affects the display only; saved images are untouched. Not stated in
     the UI (zakv suggested a tooltip).
  4. The PR text says autoscaling was previously always on; the code it modifies
     autoscaled only the first frame. The PR adds per-frame autoscale as an option,
     default off, so default behaviour is unchanged.
  5. Background is not saved across BLACS restarts (zakv suggestion; optional).
- **Up to date?**: Merges cleanly with master (154 commits behind, but only the two
  QtGui→QtWidgets commits touched the tab file since). Merges cleanly with #63.
  Conflicts with #148 (file becomes a stub); the diff would be re-applied to
  `TriggerableCamera/blacs_tabs.py` and `blacs_tab.ui`, mechanically.
- **Tested?**: zakv ran it on a PCO camera (IMAQdx subclass) and it worked apart from
  defect 1. Author presumably ran it on his own setup.
- **Discussion state**: zakv reviewed 2021-08-22 with the points above; the author
  (the maintainer) never responded. Ball with the author.
- **Breaking?**: No. Save data gains one key.
- **Rewrite relevance**: Display-side background subtraction and a per-frame
  autoscale toggle are small features worth having in shotscript's camera view.
- **Importance**: 2. Useful, small, one crash to fix, four years idle.
- **Recommended action**: Merge after small fixes: guard `set_bg_image` when no image
  and when shapes differ; add a tooltip saying subtraction is display-only. Re-apply
  on top of #148 if that merges first.

---

### labscript-devices #63: Make IMAQdx camera tab restore more of the display's settings (zakv, opened 2020-07-31, last updated 2021-08-22)

- **What it does**: `get_save_data` additionally stores the displayed image's shape
  and dtype, the view box's target x/y ranges and auto-range flags, and the colour
  levels. `restore_save_data` displays a zero image of the saved shape so the first
  real frame does not autoscale, then restores ranges, auto-range flags and levels.
- **Type**: feature
- **Size**: 1 file, +74/-1, 2 commits
- **No-brainer?**: No, because of one API call that does not exist in current
  pyqtgraph; otherwise yes.
- **Implementation**:
  1. `self.image.getLevels()`: `pyqtgraph.ImageView` has no `getLevels` in pyqtgraph
     0.14.0 (checked the installed package: `ImageView` has `setLevels` and
     `autoLevels`; `getLevels` is on `HistogramLUTItem`). With current pyqtgraph,
     `get_save_data` raises AttributeError whenever an image is displayed, i.e. BLACS
     fails to save this tab's settings on exit. Use
     `self.image.ui.histogram.getLevels()`. I could not check whether a 2020 version
     had it; zakv has run the code in production, so it may have.
  2. BLACS stores tab save data via `repr` and restores via `eval`
     (`blacs/front_panel_settings.py:374, :91`). `targetRange()` returns lists of
     floats and `autoRangeEnabled()` bools, so that is fine once (1) is fixed.
  3. The `dummy_image[0, 0] = 1` workaround is for pyqtgraph < 0.11 and can go.
  4. If the camera's ROI changed since the save, the restored ranges are for the old
     shape. Tolerable.
  5. Interaction with #87: #87's `update_image` autoscales when `image_view.image is
     None`; after #63's dummy image that never happens on restore, which is #63's
     intent.
- **Up to date?**: Merges cleanly with master and with #87. Conflicts with #148 (file
  moved); re-apply to `TriggerableCamera/blacs_tabs.py`.
- **Tested?**: Used in zakv's lab since 2020 on a PCO camera. Could have been run as
  written on the pyqtgraph of the time.
- **Discussion state**: No maintainer response in six years; author added a comment
  clarification in 2021. Ball with maintainers.
- **Breaking?**: No.
- **Rewrite relevance**: Persisting the image view's zoom and levels across restarts
  is a reasonable default for shotscript's camera display.
- **Importance**: 2. Small quality-of-life change.
- **Recommended action**: Merge after small fix (`getLevels` via the histogram; drop
  the pre-0.11 workaround), on whichever tab file is current after #148.

---

## Ordering and overlaps

- #148 is the structural change the others depend on. If it is accepted, #87 and #63
  become one-file re-applies onto `TriggerableCamera/blacs_tabs.py`, #144's semaphore
  belongs in `TriggerableCameraWorker` (as a synchronous "armed" step in
  `transition_to_buffered`, not a `hasattr` probe), and #106 shrinks to an interface
  class plus the tree widget.
- #144's `andor_utils.py` fixes do not overlap #148 and can go first, once corrected.
- #87 and #63 can be merged in either order; they merge cleanly together.
- #106 cannot be merged as is regardless of #148 (NumPy 2, transport, stale author).

## Ranked

| Rank | PR | Type | Importance | Action |
|---|---|---|---|---|
| 1 | #148 TriggerableCamera + DummyCamera | refactor / feature | 3 | Review feedback to author (keep `mock`, drop override guard, trim prose), hardware test, then merge |
| 2 | #144 Andor fixes | bugfix / feature | 3 | Ask author to fix f-string, model name, range check, semaphore deadlock; merge SDK fixes before #148 |
| 3 | #87 autoscale + background | feature | 2 | Merge after guarding `set_bg_image`; re-apply onto #148's tab |
| 4 | #63 restore display ranges | feature | 2 | Merge after fixing `getLevels`; re-apply onto #148's tab |
| 5 | #106 GeniCam | feature | 2 | Ask author to rebase as a TriggerableCamera subclass; otherwise close as stale |

## 3.x labscript-devices: device PRs #130, #129, #126, #110, #53

Base: `origin/master` at 424b9f4 (2026-04-07). All five PRs add or extend a device.

Conventions checked against master for every PR:

- Registration: `labscript_utils.device_registry.populate_registry()` walks
  `labscript_devices/` for files named `register_classes.py` and executes each one as a
  standalone module (not as a package submodule, so relative imports in that file fail).
  Registration is keyed by labscript class name. NI_DAQmx and PrawnBlaster are the
  reference layouts (`<Device>/labscript_devices.py`, `blacs_tabs.py`,
  `blacs_workers.py`, `register_classes.py`, optional `runviewer_parsers.py`).
- `set_passed_properties` (labscript/utils.py) saves, for each listed name, the instance
  attribute of that name if it exists after `__init__`, otherwise the call argument.
- BLACS `DeviceTab.create_worker` (blacs/tab_base_classes.py:486) adds every connection
  table property to the worker kwargs automatically, so tabs do not need to forward them.
- BLACS `DeviceTab.transition_to_buffered` (blacs/device_base_class.py:644-657) treats a
  `None` return from the worker's `transition_to_buffered` as failure and aborts the
  transition. The returned dict is applied to the front panel in `transition_to_manual`
  (device_base_class.py:714), but only to the built-in `_AO/_DO/_DDS/_image/_EO` stores.
- Runviewer parsers for clocked devices receive `clock=(times, values)` and must pass
  `(clock_ticks, data)` tuples to `add_trace` (see NovaTechDDS9M parser). Exceptions in
  a parser are caught and logged; the device then shows no traces.

---

### labscript-devices #130: Add BS 34-1A precision voltage source (OljaKhor, opened 2025-06-12, last updated 2025-06-26)

- **What it does**: Adds `labscript_devices/BS_Series/`, a driver for the Stahl
  Electronics BS 34-1A 8-channel serial voltage source. The labscript class `BS_` is an
  `IntermediateDevice` that writes a `(time, ao…)` table to the shot file. The BLACS
  worker replays that table in a background thread with `time.sleep`, since the
  instrument has no clock input or buffer. Two model subclasses (`BS_341A`,
  `BS_341A_spec`) are generated from a `capabilities.json` in the NI_DAQmx style. A pty
  based emulator is included for testing without hardware.
- **Type**: feature
- **Size**: 15 files, +1082/-0, 14 commits (10 by the author, 1 merge of master, 3
  upstream commits carried by the merge)
- **No-brainer?**: No. The timing model does not fit labscript's hardware-timed model,
  and the BLACS worker does not follow the worker contract (see below).
- **Implementation**: Not mergeable as written. Concrete defects:
  - `BLACS_workers.py:70-101` `transition_to_buffered` returns `None`. BLACS master
    treats this as a failed transition and calls `abort_transition_to_buffered`
    (device_base_class.py:656). Buffered mode cannot have worked through an unmodified
    BLACS.
  - `BLACS_workers.py:103-122` timing is measured from the moment the worker thread
    starts, which is during `transition_to_buffered`, not from the pseudoclock start.
    The offset is the time between this device's transition and the master pseudoclock
    being triggered (seconds, variable). Each `set_voltage` also blocks on a serial
    round trip at 9600 baud (~20 ms per command), so timing drifts within a shot.
  - `BLACS_workers.py:138-139` `abort_transition_to_buffered` calls
    `transition_to_manual`, which does `self.thread.join()` without setting
    `_stop_event` (which nothing ever sets). An abort blocks until the whole sequence has
    been replayed. `abort_buffered` is not defined at all, so aborting a running shot
    raises in the worker.
  - `BLACS_workers.py:38-65` `program_manual` does not program the device. Front panel
    edits do nothing until the user presses the custom "Send to device" button
    (`send_to_BS`). This contradicts the BLACS contract. The method is used only to push
    the previous shot's final values into the front panel, which is what returning the
    dict from `transition_to_buffered` already does.
  - `BLACS_workers.py:162-215` `send_to_BS` appends the front panel values to an
    `AO_manual` dataset in the *previous shot's* h5 file, and raises `RuntimeError` if no
    shot has run yet. Writing manual-mode state into an already completed shot file is
    wrong, and the button fails until the first shot.
  - `BLACS_workers.py:36` `shutdown` references `self.connection`, which does not exist
    (`self.voltage_source.connection`), so shutdown raises.
  - `logger_config.py:6-14` creates `device.log` inside the installed package directory
    at import time. `register_classes.py:4` imports it, so every process that populates
    the device registry (BLACS, runviewer, runmanager) writes into site-packages. Fails
    on read-only installs.
  - `labscript_devices.py:9-74` the device is an `IntermediateDevice` requiring a parent
    clockline but declares no `clock_limit` and never uses the clock. The pseudoclock
    generates ticks for it anyway, and `pseudoclock.times[clockline]` includes ticks for
    other devices on the same line, each of which becomes a serial command. There is no
    check that the row rate is achievable (a 1 kS/s ramp on the shared clockline yields
    ~20 ms per command).
  - `labscript_devices.py:113-114` returns `None` for a device with no AnalogOut children;
    `create_dataset("AO_buffered", data=None)` then fails.
  - `labscript_devices.py:6` imports `split_conn_DO, split_conn_AO` from
    `NI_DAQmx.utils` and does not use them; `add_device` (line 76) is a no-op override.
    `static_AO` is a property but `StaticAnalogOut` is not handled.
  - Channel name handling is inconsistent: widgets are `CH0%d` (`BLACS_tabs.py:33`,
    `BLACS_workers.py:55,151`) while `voltage_source.py:65` formats `CH{:02d}`;
    `utils.py` accepts four different connection spellings.
  - Module names `BLACS_tabs.py`/`BLACS_workers.py` differ from the repo convention;
    docs are a Markdown file inside the package instead of `docs/source/devices/*.rst`;
    the README's emulator invocation `python3 -m BS_Series.testing.emulateSerPort` does
    not match the installed package path.
  - `supports_remote_value_check(False)` although the protocol has readback (`U`, `I`,
    `Q` queries are implemented in `voltage_source.py:118-217` and unused).
  - Structure vs NI_DAQmx: `capabilities.json`/`models/` layout is copied correctly, but
    for two hand-written entries (one of which encodes a per-unit calibration quirk,
    channel 1 at ±24 V) a subclass with class attributes would be simpler. Registration
    via `register_classes.py` is correct in mechanism (base `BS_` plus each model name).
  - The serial protocol knowledge is sound and useful: `IDN\r` returns
    `<serial> <range> <channels> <type>`; `<serial> CHxx <0..1 normalised>\r` sets a
    channel and echoes `CHxx <value>`; `TEMP`, `Uxx`, `Ixx`, `Qxx` queries.
- **Up to date?**: Merges cleanly; master is 34 commits ahead, none touching these paths.
  No dependency drift (pyserial already a dependency). The emulator uses `pty`
  (POSIX only), acceptable for a test tool.
- **Tested?**: Author says tested on their unit in manual and buffered mode. Given the
  `None` return and the missing `abort_buffered`, the buffered path cannot have run
  through BLACS master as written; manual mode via the button is plausible.
- **Discussion state**: No reviewer has commented. Ball is with the maintainers. The
  author explicitly invited design proposals for the timing model.
- **Breaking?**: No (new device).
- **Rewrite relevance**: Software-timed, unbuffered instruments are a category labscript
  has no model for; the rewrite should decide whether to support them explicitly
  (static-only, or best-effort software timing with a declared tolerance) rather than
  leave contributors to emulate buffering with threads.
- **Importance**: 2. The hardware is niche and the design needs to be replaced, not
  patched.
- **Recommended action**: Rework by author under maintainer guidance, or close. The
  minimum viable version is a static device (`Device` with `StaticAnalogOut` children,
  no clockline), modelled on the Windfreak/TekScope layout, with `program_manual`
  programming the device and remote value check using the `Uxx` query. If software
  timing is kept, it must at least return final values, honour aborts, and start its
  clock on a trigger rather than at transition time.

---

### labscript-devices #129: Keysight Oscilloscope Implementation with pyVISA (K-Takouti, opened 2025-05-13, last updated 2025-05-27)

- **What it does**: Adds `labscript_devices/KeysightScope/` for Keysight 1000 X-series
  and EDUX1052 scopes over pyVISA. `KeysightScope` is a `TriggerableDevice`; the shot
  script calls `set_config(n)` to choose one of the scope's 10 internal setup slots and
  `trigger_at(t, duration)` once. The worker recalls the slot, arms `:SINGle`, and in
  `transition_to_manual` reads the displayed channels' waveforms and stores them in
  `/data/traces/<device_name>` with the preamble and slot configuration as attributes.
  The BLACS tab shows a 10-tab widget (Qt Designer `.ui` files) to activate a slot,
  save the scope's current front-panel setup into it, or reset it to defaults, with a
  table summarising each slot's settings.
- **Type**: feature
- **Size**: 10 files, +1508/-0 (incl. a PNG), 21 commits
- **No-brainer?**: No. Several design problems, and no full review yet.
- **Implementation**:
  - `labscript_devices.py:27,36-64` `get_adress_from_serial_number` runs in the
    labscript device constructor, i.e. at every compile in runmanager. It opens every
    VISA resource on the machine, sends `*IDN?` and `:SERial?` to each with a 500 ms
    timeout, and uses the result as `BLACS_connection`. Compile therefore requires
    pyvisa, a VISA backend and the hardware, and probes unrelated instruments. The
    address should be a constructor argument (as in TekScope: `addr`). Also:
    `is_right_model` is never reset in the loop (a supported model earlier in the list
    makes a later unsupported model with the right serial pass), and the `ValueError`
    for an unsupported model at line 59 is raised inside the `try` and swallowed by the
    bare `except: continue` at line 60.
  - `blacs_tabs.py:9-11` imports `PyQt5` directly instead of `qtutils.qt`, and uses
    `PyQt5.uic`. The rest of the repo is binding-agnostic.
  - `KeysightScope.py:26,153-155` `KeysightScopeDevice.__init__` sends `*RST` whenever
    the worker starts, erasing the scope's live setup. `blacs_tabs.py:60-67` `init_osci`
    then recalls all 10 slots (`get_saving_register`) and, for every empty slot, calls
    `default_config`, which does `*RST` and saves the reset state into that slot. BLACS
    startup therefore writes into the instrument's stored setups without user action.
    Empty-slot detection is `"250" in :SYSTem:ERRor?` (`KeysightScope.py:131`), fragile.
  - `blacs_tabs.py:59,69,73,78` all four tab actions are allowed in `MODE_BUFFERED` and
    the transition modes, so a user can recall or overwrite a setup mid-shot.
  - Acquisition is not verified. `blacs_workers.py:74` arms `:SINGle`; `transition_to_manual`
    (lines 87-93) reads `:WAVeform:DATA?` with no `:TER?`/`*OPC?`/`:DIGitize` check. If
    the trigger is missed, the scope returns the previous acquisition and the shot is
    saved with stale data and no error (`get_trigger_event` exists at
    `KeysightScope.py:375` and is marked "Not used yet"). The `timeout` device property
    only bounds the VISA read.
  - `blacs_workers.py:109` `create_group('/data/traces')` raises if the group exists
    (two scopes, or a TekScope, in one shot); TekScope uses `require_group`. Line 111
    saves only the last channel's preamble (`preamble[ch]` after the loop). Line 97
    `len(t)` is a `NameError` if no channel is displayed. Line 39 opens the shot file
    `'r+'` to read.
  - `blacs_workers.py:49` `int(self.activated_configuration)` is `int(None)` if the
    script did not call `set_config`; the README documents this as mandatory but the
    error is a `TypeError` rather than a message. Line 59 raises `KeyError` for a
    non-external trigger source.
  - `__init__.py` defines `ScopeChannel(AnalogIn)` which nothing uses;
    `allowed_children` is not set.
  - `blacs_tabs.py:20-24` forwards connection table properties to the worker manually
    (BLACS does this automatically); harmless.
  - Config-slot design: as a pragmatic compromise for scopes it is reasonable, and
    saving the recalled slot's settings dict into the dataset attributes gives
    per-shot provenance. The weakness is that the reproducible state lives in the
    instrument's memory: a slot can be changed from the scope's own front panel without
    labscript noticing (the BLACS table refreshes only on "load and save"), and the
    `labscript` script refers to a slot number with no content check. A hash or the
    settings dict could be compared at `transition_to_buffered` time.
  - Registration (`register_classes.py`) is correct. File layout matches convention.
- **Up to date?**: Merges cleanly; master 39 commits ahead, no overlap. `PyVISA` is
  already a declared dependency; a VISA backend is not (same as TekScope). PyQt5 direct
  import is the only binding assumption.
- **Tested?**: Author reports working with their scope. The code is plausible for the
  happy path (one scope, trigger always arrives, `set_config` always called). The
  failure paths above are untested.
- **Discussion state**: dihm gave first-pass comments (2025-05-15): drop the
  capabilities machinery, make serial number an instance argument, rename the low-level
  class/file, split utilities out. Author replied and pushed (2025-05-27) removing
  `connection_manager`, renaming to `KeysightScopeDevice`, keeping serial-number
  discovery. dihm promised a full review and has not returned. Ball is with the
  maintainer.
- **Breaking?**: No (new device).
- **Rewrite relevance**: The idea of selecting an instrument-held setup snapshot per shot
  and recording the snapshot's contents in the shot file is worth keeping as a pattern
  for scopes and other heavily-configured instruments.
- **Importance**: 3. Useful hardware, workable concept, but needs a second round
  addressing the compile-time discovery, PyQt5, `*RST` on startup, and acquisition
  verification.
- **Recommended action**: Ask author for: (1) VISA address as a constructor argument,
  no hardware access in the labscript class; (2) `qtutils.qt` imports; (3) no `*RST`
  or slot writes at startup; (4) verify trigger before reading (`:TER?` or
  `*OPC?` after `:DIGitize`) and raise if not triggered; (5) `require_group`, per-channel
  preambles, tab actions restricted to `MODE_MANUAL`. Then full review.

---

### labscript-devices #126: AD9959 DDS Sweeper (carterturn, opened 2025-03-31, last updated 2026-08-25)

- **What it does**: Adds `labscript_devices/AD9959DDSSweeper/`, a driver for the
  QTC-UMD "dds-sweeper" firmware on a Raspberry Pi Pico (1 or 2) driving an AD9959
  four-channel DDS eval board. The `IntermediateDevice` accepts `DDS` children on the
  first `dynamic_channels` channels and `StaticDDS` on the rest, quantises to DDS tuning
  words, and writes `dds_data`/`static_data` tables. The worker uploads the table in
  binary (`setb`, with a "ready for N bytes" handshake), or line-by-line (`seti`) when a
  smart cache shows fewer than 10 % of rows changed, sets a stop instruction, starts,
  and checks for `STOPPED` at the end. Includes docs and a runviewer parser.
- **Type**: feature
- **Size**: 8 files, +1120/-0, 66 commits (includes a merge of master and upstream
  commits carried by it)
- **No-brainer?**: No, but close for the labscript and BLACS parts; the runviewer
  parser is broken and a few review items remain.
- **Implementation**: The labscript device and BLACS worker are in good shape and follow
  the NovaTechDDS9M/PrawnDO patterns (quantise in `generate_code`, smart cache with
  `fresh`, final values returned, aborts restore `initial_values`). Defects:
  - `runviewer_parsers.py` cannot run: `DDSs` is undefined (lines 32-37, `NameError`),
    `np.float` was removed in numpy 1.24, the dtype names are `freq%d` but the
    assignments use `'%d_freq'` (lines 47-49), and the traces are passed to `add_trace`
    as bare arrays with no time axis. The `clock` argument is ignored. Compare the
    NovaTechDDS9M parser, which derives `clock_ticks` from the clockline and passes
    `(clock_ticks, data)`. Runviewer will log a failure and show nothing for this
    device.
  - `labscript_devices.py:111-128` `clock_limit` is `ref_clock_frequency /
    cycles_per_instruction`, but the cycle counts are Pico system-clock cycles. With
    `ref_clock_external=1` the Pico system clock is not set from `ref_clock_frequency`
    (per the docstring, line 76), so the limit is wrong whenever the external reference
    differs from the Pico clock; an external reference above the Pico clock
    overestimates the limit and will produce the partially-applied-instruction failure
    the author describes in the 2025-04-30 comment. The limit should use the Pico
    system clock.
  - `labscript_devices.py:56-58,210-214` `sweep_mode` is accepted and stored but only
    `0` is supported; `generate_code` always builds a steps-format table, so a non-zero
    value is detected only at run time by the byte-count mismatch in `set_batch`
    (`blacs_workers.py:244-247`). Reject `sweep_mode != 0` in the constructor.
  - `blacs_workers.py:76,93,103` runtime checks via `assert` (dihm asked for
    `LabscriptError`; the Dec-2025 commits converted some). Stripped under `-O`.
  - `blacs_workers.py:476-488` `transition_to_manual` polls `status` 1000 times with no
    sleep; the effective timeout is 1000 serial round trips. Make it time based.
  - `labscript_devices.py:218` indexes `max_instructions_map` by total child count
    (dynamic plus static) while the firmware table width is `len(dyn_chans)`
    (`blacs_workers.py:404`). Conservative, but inconsistent with the documented
    per-channel counts. Line 231 error text says "n from 0 to 4".
  - `labscript_devices.py:45` lists `name` as a connection table property; pointless,
    and it is forwarded to the worker as kwarg `name`.
  - `blacs_workers.py:64` converts tuning words with `sys_clk/(2**32-1)` while
    quantisation uses `2**32/dds_clock`; negligible but inconsistent.
  - Docs: `AD9959DDSSweeper.rst:44` says "PrawnDO"; the `.. note::` at line 121 has
    unindented body text so renders empty; "Up to 0 dBm" (line 16) is presumably
    intended.
  - Firmware/protocol assumptions: minimum firmware 0.4.0; commands `version`, `board`,
    `status` (integer 0-5), `reset`, `setclock <ext> <freq> <mult>`, `mode <m> 0`,
    `debug off`, `setchannels <n>`, `setb 0 <n>` then raw bytes, `seti <ch> <addr> <f>
    <a> <p>`, `set 4 <count>` (stop), `start`, `abort`, `setfreq/setamp/setphase`.
    Table row format per channel `<u4 freq, <u2 amp, <u2 phase`, channel 0 first. The
    `set_batch` response parse at line 243 assumes exactly `ready for N bytes\n`.
    A 0.4.0 firmware release must exist publicly for this to be usable.
  - Registration and file layout are correct and match PrawnBlaster.
- **Up to date?**: Merges cleanly; master is 11 commits ahead with no overlap. numpy
  2 compatibility is fine except the dead parser.
- **Tested?**: Extensively, on hardware, by two groups (carterturn; Json-To-String and
  dihm at QTC-UMD) over 2025, including a reproducible smart-cache bug (stale
  `np.empty` rows) fixed 2025-09-24, and an abort fix 2026-08-24. The runviewer parser
  has never been run.
- **Discussion state**: 16 comments, last 2025-09-29 (carterturn applied the cache
  patch). Commits continued to 2026-08-24 without further review comments. dihm's
  2025-04-28 review asked for testing of no outputs / static only / dynamic only /
  final values / aborts; the Apr-29 and later commits address these. Nothing explicit
  is blocking: it is waiting for dihm (a maintainer, and co-author of the hardware) to
  finish review and merge. The broken parser and the `clock_limit` question above are
  the concrete remaining items.
- **Breaking?**: No (new device).
- **Rewrite relevance**: Good reference for a Pico-based buffered device: binary table
  upload with a byte-count handshake, row-level smart cache, status polling on
  transition to manual.
- **Importance**: 4. Working, tested, documented hardware driver with an active user
  base; blocked only on review.
- **Recommended action**: Merge after small fixes: rewrite or drop
  `runviewer_parsers.py` (and its `register_classes` entry) so it either works or does
  not exist; fix `clock_limit` to use the Pico system clock or document that
  `ref_clock_external` requires `ref_clock_frequency` equal to the Pico clock; reject
  `sweep_mode != 0`; replace remaining `assert`s; time-based status timeout; doc fixes.

---

### labscript-devices #110: Add Windfreak SynthHD and SynthHDPro devices (dihm, opened 2024-01-16, last updated 2025-11-18)

- **What it does**: Adds `labscript_devices/Windfreak/` with `WindfreakSynthHD` and
  `WindfreakSynthHDPro` (a subclass with wider frequency limits). Static only: a
  parentless `Device` with `StaticDDS` children, writing a one-row `STATIC_DATA` table
  (freq/amp/phase/gate per channel). The worker uses the `windfreak` PyPI package, sets
  reference mode and trigger mode at init, supports remote value check and a per-field
  smart cache. Gating is via the synth's `rf enable` trigger mode plus a labscript
  `digital_gate`.
- **Type**: feature
- **Size**: 7 files, +659/-0, 17 commits
- **No-brainer?**: Nearly. It is the maintainer's own driver, follows the TekScope
  static-device pattern, and has been in lab use since 2022; three small code defects.
- **Implementation**: Defects:
  - `labscript_devices.py:124` `LabscriptError(...)` is constructed but not raised, so
    the channel-range check never fires; a bad channel surfaces later as a numpy
    `ValueError` (no field `freq2`) at line 149.
  - `labscript_devices.py:171` `self.device.name` should be `self.name`
    (`AttributeError` on the error path of `enable_output`).
  - `labscript_devices.py:109-110` `validate_data` message says "frequencies" and
    "Hz" for amplitude and phase too.
  - `docs/source/devices/windfreak.rst:65` imports `NI_DAQmx.Models.NI_USB_6343`
    (capital M); the package is `models`, so the example fails on case-sensitive
    filesystems.
  - `blacs_workers.py:211` `shutdown` calls `synth.save()` (EEPROM write) on every
    BLACS shutdown; worth a comment or an opt-out.
  - `blacs_tabs.py:19-22` uses the `device_worker_class` indirection and
    `initialise_workers` forwards properties by hand; both unnecessary but harmless.
  - Connection table properties are used correctly: class attributes
    (`allowed_chans`, `freq_limits`, `*_res`) are picked up by `set_passed_properties`
    via the instance-attribute rule, and the tab builds widget limits from them, so the
    Pro/non-Pro difference is a class attribute override. `com_port` is both the
    `connection` and `BLACS_connection`.
  - Dependency: `windfreak` is imported inside `Worker.init` only, not declared in
    `pyproject.toml`. This matches how other optional vendor libraries are handled
    (spinapi excepted). API used (`SynthHD`, `trigger_modes`, `reference_modes`,
    `reference_mode`, `reference_frequency`, channel `frequency`/`power`/`phase`/
    `rf_enable`/`pll_enable`, `save`, `close`) matches windfreak 0.3.x.
  - Registration correct (both class names to the same tab).
- **Up to date?**: Merges cleanly; master is 68 commits ahead with no overlap. No
  Python or numpy version issues; `np.bool_` handled explicitly.
- **Tested?**: In use in the author's lab since 2022 (commit history shows bugs found
  and fixed in use). The docs note an unresolved intermittent failure to update outputs
  attributed to the device or the `windfreak` package.
- **Discussion state**: No reviewer comments in two years. The author is a maintainer;
  the PR appears to be waiting for a second maintainer to approve.
- **Breaking?**: No (new device).
- **Rewrite relevance**: None beyond the `windfreak` API notes.
- **Importance**: 4. Low risk, long in use, cheap to merge.
- **Recommended action**: Merge after small fixes: add `raise` at
  `labscript_devices.py:124`, fix `self.device.name`, fix the docs import path, fix the
  `validate_data` message.
- **Status 2026-10-17**: the three code defects reproduce on the head and are fixed on a
  local branch (`pr110-work` in `repos/labscript-devices`, 0593f45) together with the
  docs import path; the fixed branch compiles a two-channel connection table and raises
  `LabscriptError` on each bad input (`TESTING.md`, "labscript-devices #110 Windfreak
  SynthHD"). The branch is pushed upstream as `windfreak-110-fixes`; pushing it to the
  author's fork, which allows maintainer edits, is a row in `LOCAL-TASKS.md`.

---

### labscript-devices #53: Widgets and runviewer parser for DummyIntermediateDevice (rpanderson, opened 2020-06-12, last updated 2020-06-25)

- **What it does**: Rewrites `DummyIntermediateDevice.py` so the BLACS tab shows
  analog and digital output widgets (`num_AO` analog outputs named `ao%d`, digital
  lines `port%d/line%d` from a `ports` dict), stores these capabilities and
  `clock_limit` as connection table properties via `set_passed_properties`, keys the
  `OUTPUTS` table by connection string instead of output name, returns final values from
  `transition_to_buffered`, and adds a runviewer parser modelled on NI_DAQmx.
- **Type**: feature
- **Size**: 1 file, +189/-20, 1 commit
- **No-brainer?**: No. It conflicts, changes the device's constructor and channel
  naming, and has an unresolved TODO.
- **Implementation**:
  - Removes the `BLACS_connection` constructor argument (hard-codes
    `'dummy_connection'`). Master's own docstring example passes
    `BLACS_connection='dummy2'`, which would now fall into `**kwargs` and reach
    `Device.__init__`.
  - Enforces `ao%d` and `port%d/line%d` connection names. Master accepts any name
    (table keyed by output name), and philipstarkey noted real experiments use it with
    arbitrary names. He asked for the tab to introspect the connection table's child
    outputs instead; not done.
  - `DummyIntermediateDevice.py` (PR) imports `split_conn_AO, split_conn_DO` from
    `NI_DAQmx.utils` for widget sort keys; cross-device import.
  - Final values: the mechanism (dict from `transition_to_buffered`, applied in
    `DeviceTab.transition_to_manual`) is the standard one and the keys match the widget
    names, so the TODO ("front panel values don't reflect final values") is not
    explained by naming when connections are `ao%d`/`port%d/line%d`; outputs with other
    names are silently skipped. I could not determine the cause statically. blacs
    issue 58 ("final values not handled for devices with custom UIs") is unrelated, as
    philipstarkey said; it also appears unfixed: `device_base_class.py:714-724` still
    applies final values only to the built-in output stores.
  - Still uses the single-file `@BLACS_tab`/`@runviewer_parser` decorator layout, as
    master does for this device; the registry marks these deprecated.
- **Up to date?**: Conflicts in `labscript_devices/DummyIntermediateDevice.py`: master
  converted the header comment block into a module docstring (for the docs build) and
  the PR edits the same lines. Otherwise master's version of the device is functionally
  unchanged since 2020 (216 commits behind overall, none to this device's logic). Not
  superseded.
- **Tested?**: Author gave a test script (used with labscript-utils #54) and
  reported it working except for the front panel update.
- **Discussion state**: philipstarkey reviewed 2020-06-23, requested backward-compatible
  channel handling via connection-table introspection, set milestone 3.1. No response
  from the author since. Ball was with the author; both have since stopped maintaining.
- **Breaking?**: Yes: constructor loses `BLACS_connection`; outputs must use `ao%d` /
  `port%d/line%d` connection names; `OUTPUTS` table columns change from output names to
  connection names.
- **Rewrite relevance**: A dummy intermediate device with real widgets is useful for
  exercising `shotscript control` without hardware; the rewrite should have one from
  the start.
- **Importance**: 2. Nice-to-have testing aid, stale, with the reviewer's request
  unaddressed.
- **Recommended action**: Close as stale, or rework by maintainer: keep arbitrary
  connection names by building widgets from the connection table's children (AnalogOut
  → AO widget, DigitalOut → DO widget), keep `BLACS_connection`, and move the device to
  a subpackage with `register_classes.py`.

---

## Ranking

| Rank | PR | Type | Importance | Action |
|---|---|---|---|---|
| 1 | #126 AD9959 DDS Sweeper | feature | 4 | Merge after small fixes (fix or drop runviewer parser, `clock_limit` with external ref, reject `sweep_mode != 0`, asserts, docs) |
| 2 | #110 Windfreak SynthHD/Pro | feature | 4 | Merge after small fixes (missing `raise`, `self.device.name`, docs import path) |
| 3 | #129 Keysight scope | feature | 3 | Ask author: VISA address as argument, qtutils imports, no `*RST`/slot writes at startup, verify trigger before reading, `require_group`; then review |
| 4 | #130 Stahl BS 34-1A | feature | 2 | Rework (static device, or proper software-timed design) or close |
| 5 | #53 DummyIntermediateDevice widgets | feature | 2 | Close as stale, or maintainer rework with connection-table introspection |

## 3.x blacs open PR review (#123, #121, #105, #89, #88)

Base: `origin/master` = e5757c7 (2026-06-04, merge of #119). #90 is reviewed elsewhere.

### blacs #123: Fix two plugin-loading bugs (ispielma, opened 2026-08-28, last updated 2026-10-08)

- **What it does**: Three commits. (1) `blacs/plugins/__init__.py`: wraps `exp_config.getboolean('BLACS/plugins', name)` in `try/except ValueError`; on failure it writes a boolean into the section (shadowing the inherited `[DEFAULT]` value) and logs a warning, so BLACS starts instead of raising at import time. (2) `blacs/__main__.py`: replaces the call-then-retry-with-old-signature logic for `plugin_setup_complete` by `inspect.signature(...).bind(blacs_data)`, so the hook is called exactly once with the arity it accepts. (3) `blacs/compile_and_restart.py`: replaces `self.output_path.strip('.h5')` with `os.path.splitext(self.output_path)[0]`. Commit 3 is not mentioned in the PR description.
- **Type**: bugfix
- **Size**: 3 files, +36/-11, 3 commits
- **No-brainer?**: Nearly. All three are real bugs with small, local fixes; one claim in the description is wrong but harmless (below).
- **Implementation**:
  - Bug 1 is real: `ConfigParser.items(section)` and `has_option(section, option)` both include `[DEFAULT]` keys (verified against CPython `RawConfigParser.has_option`, which returns `option in self._sections[section] or option in self._defaults`). So the `has_option` change at `blacs/plugins/__init__.py:90` is a no-op in behaviour; the description's claim that it "asks the question directly" is incorrect. The actual fix is the `try/except ValueError` block, which is correct. The collision only occurs with a non-standard labconfig (the shipped `example.ini` has no `[DEFAULT]` key named after a plugin directory; the author's labconfig has `connection_table` in `[DEFAULT]`). A `[DEFAULT]` key with a boolean-looking value would still be silently read as the enable flag, but that is an edge case not worth handling.
  - Bug 2 is real: on master `blacs/__main__.py:443-450` catches any `Exception` from `plugin_setup_complete(blacs_data)` and retries with no argument, so a plugin with signature `(self, data=None)` that raises part-way is executed twice. All in-tree plugins declare `(self, BLACS)` so they were never affected. The new code is correct; `ValueError` from `inspect.signature` is handled.
  - Bug 3 is real: `str.strip('.h5')` strips any trailing `.`, `h` or `5` characters, so a connection table path ending in e.g. `..._h.h5` gives a wrong temp filename. `os` is already imported in that file.
  - The comment blocks added in both files describe history/alternatives ("Detecting the old no-argument API by letting a call fail would re-run...") and should be trimmed to a statement of what the code does.
- **Up to date?**: Merges cleanly; 0 commits behind master. Independent of #121 (does not contain it). The same two plugin fixes also appear in the author's closed labscript-utils branch `origin/pr/127` (commits d630999, 35b76df, 4cf6f52) as part of their `labscript_utils.plugins` module, so if #121 were ever taken, these fixes would move there.
- **Tested?**: Author says both reproduced against master and fixed (an AI-assisted audit). The code is runnable as written; no tests added (blacs has none for this).
- **Discussion state**: No reviewer comments. Ball is with the maintainer.
- **Breaking?**: No. Behaviour change only in the failure cases.
- **Rewrite relevance**: Avoid `ConfigParser [DEFAULT]` inheritance surprises in any ini-based config; `shotscript` uses its own config so this is a reminder only.
- **Importance**: 4. Startup crash for a plausible labconfig, plus two small correctness fixes.
- **Recommended action**: Merge after small fixes: drop the `has_option` change or keep it without the misleading rationale; shorten the two comment blocks; mention commit 3 in the PR description.
- **Status 2026-10-17**: merged as is, d061535, after the `[DEFAULT]` collision was reproduced on master and shown fixed on the branch, the branch merged with master passed the harness on Python 3.14, and the pull request head passed the workflow on Ubuntu and Windows for Python 3.11 to 3.14 with all three Qt bindings (`TESTING.md`, "blacs #123 plugin-loading fixes"). A comment on the PR records the test and the `has_option` note. The comment trim (local branch `pr123-work` in `repos/blacs`, commit f1aea3f, five lines) goes into the next blacs pull request.

### blacs #121: Refactor BLACS for shared plugin support (ispielma, opened 2026-04-26, last updated 2026-05-12)

- **What it does**: Moves `Callback`, `callback`, `DEFAULT_PRIORITY`, module discovery and plugin instantiation/setup from `blacs/plugins/__init__.py` and `blacs/__main__.py` into a new `labscript_utils.plugins.PluginManager` / `MenuBuilder` / `BasePlugin`; blacs then calls `plugins.manager.discover_modules()`, `instantiate_plugins()`, `setup_plugins()`, `setup_complete()`, `close_plugins()`. Also adds `APPLICATION_NAME`/`DESKTOP_APP_MODULE` constants, passes `application_name=` to `Splash`, adds a macOS `short_display_name` to `desktop-app.json`, commits a `.DS_Store`, and deletes `tests/device_base_classes_connection_table.h5`.
- **Type**: refactor
- **Size**: 7 files, +60/-153 (plus two binary changes), 5 commits (2 are merges of a MacOS branch)
- **No-brainer?**: No. It cannot run against labscript-utils master and its counterpart there is closed.
- **Implementation**:
  - `labscript_utils.plugins` does not exist on labscript-utils master. The counterpart was labscript-utils PR 126 (`origin/pr/126`, +1832 lines: `labscript_utils/plugins.py` 1566 lines, `tests/test_plugins.py`), later folded into PR 127 (+4133 lines, also PyQt6 migration, TOML app config, shot queue widget). Neither is in the open-PR list, so both are closed without merge. With #121 applied, `import blacs.plugins` raises `ImportError` on every current install.
  - `Splash(..., application_name=APPLICATION_NAME)` at `blacs/__main__.py:27`: `labscript_utils.splash.Splash.__init__(self, imagepath)` on master takes no such argument (the new signature exists only in `origin/pr/127`). Second hard dependency on unmerged labscript-utils code.
  - Deletes `tests/device_base_classes_connection_table.h5`, which `blacs/device_base_class.py:953` still references. Unrelated to the refactor and breaks the manual test harness.
  - Adds `blacs/.DS_Store`.
  - Logs a deprecation warning for `get_tab_classes()`/`tabs_created()` ("new UI integration should use application-owned plugin contexts instead") although blacs registers no contexts, so there is no replacement for in-tree plugins (`connection_table`, `progress_bar`) to move to; the warning will fire on every start.
  - The labscript-utils side (pr/126) `discover_modules` copies the master `items()` membership test, so it carries the `[DEFAULT]` bug that #123 fixes; pr/127 fixes it there.
  - The design (a 1566-line generic plugin framework with `MenuContext`, `register_context`, setup activities with priorities) is far larger than what blacs or the known third-party plugins need.
- **Up to date?**: Merges cleanly into blacs master (3 commits behind) but is unusable without labscript-utils PR 126/127, which are closed. Not a prerequisite of #123; #123 does not contain it.
- **Tested?**: No statement. Cannot have been run against released labscript-utils; the author runs a fork ("Production" branch) with their own labscript-utils.
- **Discussion state**: No reviewer comments. Author's labscript-utils PRs were closed (presumably by the author); the author has since opened #123 against plain master instead, suggesting they are no longer pursuing this route upstream.
- **Breaking?**: Requires a new labscript-utils release; third-party plugins would keep working by duck typing per the pr/126 docstring, but `blacs.plugins.Callback`/`callback` would become re-exports.
- **Rewrite relevance**: None beyond the general observation that a plugin API should be defined once in a shared package; the rewrite has its own device/worker model.
- **Importance**: 1. Depends on closed PRs in another repo; the useful bug fixes have been resubmitted separately as #123.
- **Recommended action**: Close as obsolete (superseded by #123 for the fixes; the shared-plugin framework would need a labscript-utils PR first and a design discussion before that).

### blacs #105: Virtual Devices BLACS Plugin (carterturn, opened 2024-10-09, last updated 2026-07-01)

- **What it does**: Adds `blacs/plugins/virtual_device/` (plugin, `VirtualDeviceTab(PluginTab)`, editor `.ui`). A virtual device is a named set of `(tab_name, parent_port[, inverted])` tuples for AO, DO, EO and DDS channels of existing device tabs; each gets a `PluginTab` with widgets created by the real channels' `create_widget()`/`add_widget()`, so the widgets are live mirrors of the hardware tab's outputs. A modal "Virtual Device Builder" dialog edits the sets, which are stored in plugin save data; changes take effect after a BLACS restart. A background thread reconnects widgets after a device tab restarts. Also fixes two generic bugs in `blacs/output_classes.py`: `DO.remove_widget` could not disconnect an inverted widget (the connected slot was an anonymous lambda), and `AO.remove_widget` triggered the unit-combobox change handler when replacing the model on a widget with no AO.
- **Type**: feature (+ small bugfix)
- **Size**: 4 files, +790/-3, 37 commits (the history is duplicated: a71d6cc merges the pre-force-push copy of the branch back in, so 18 commits appear twice)
- **No-brainer?**: No. Self-contained and merges cleanly, but has an unfinished enum-output feature and a polling design that should be fixed first.
- **Implementation**:
  - `output_classes.py` changes are correct and independently useful: `set_value_inverted` as a named bound method makes `disconnect` possible; `widget.connection_inverted` is set in the only `add_widget` path. The `block_combobox_signals()`/`unblock_combobox_signals()` methods exist on master `AnalogOutput`.
  - Enum outputs are half done (commit b9aa40f "Start adding enum outputs"): `Menu.__init__` at `virtual_device/__init__.py:270-272` appends the Analog, Digital and DDS group items to the device tree but never appends `enum_outputs`, so EO channels cannot be added in the editor. `virtual_device_tab.py:84-86` calls `widget.get_EO()`/`set_EO()`, which exist on master `EnumOutput`.
  - Save data from earlier versions of this branch lacks the `'EO'` key; `plugin_setup_complete` (`__init__.py:126`) and `on_edit_virtual_devices` (`:474`) index `vd['EO']` unconditionally and will `KeyError`. Use `.get('EO', [])`.
  - `reconnect()` (`__init__.py:108-114`) runs `connect_widgets()` every 0.1 s for the life of BLACS; `connect_widgets` is `@inmain_decorator(True)`, so this is 10 blocking main-thread round-trips per second, each iterating every device tab and every virtual widget. Tabs already have `connect_restart_receiver()`; the plugin uses it for disconnect but not to trigger reconnect. Reconnection should be driven by the tab's restart/initialisation completing (or by a `tabs_created`/`restart` hook), not polling.
  - DDS handling is asymmetric: `disconnect_widgets` (`virtual_device_tab.py:110-113`) only records `last_DDS` and does not call `DDS.remove_widget`, while AO/DO are detached with `set_AO(None)`/`set_DO(None)`.
  - Output rows are parsed back from display text: `text().split(' - ')[0].split('.')` (`__init__.py:561,565,570,574`); a port string containing `.` or ` - ` breaks round-tripping. Store the tuple in an item data role instead.
  - `from qtutils.qt.QtCore import *` / `QtGui import *` / `QtWidgets import *` / `from qtutils import *` in both files; master removed all qtutils star imports in b4cde4e for PySide6 support. Duplicate `from blacs.tab_base_classes import PluginTab` at `virtual_device_tab.py:8-9`. Unused imports: `subprocess`, `sys`, `time`, `h5py`, `properties`, `TimeoutError`, `Event`, `callback`, `inmain`.
  - Plugin is not listed in `labscript-utils` `example.ini` `[BLACS/plugins]`; it is added as `False` automatically on first start, so no action needed.
- **Up to date?**: Merges cleanly; 0 commits behind master. Its labscript-utils dependency (PR 109, `InvertedDigitalOutput.set_DO` fix, 1 line) was merged into labscript-utils master in 2023 (`3ab11ce`), so released labscript-utils satisfies it. No conflict with master's EO work (#109 in blacs), which this branch already builds on.
- **Tested?**: Author: in use in their lab for months (June 2025), AO/DO/DDS reliable. The EO part (June 2026) is clearly untested from the editor side given the missing tree row.
- **Discussion state**: philipstarkey reacted but nobody reviewed. Marked ready for review 2025-06-03. Ball is with the maintainer; author is still active (last push 2026-07-01).
- **Breaking?**: No. Off by default; `output_classes.py` changes are behaviour-preserving for existing paths.
- **Rewrite relevance**: Yes, as a requirement: users want cross-device "MOT panel" groupings of channels in the control UI; the data model (named list of channel references, stored in app settings, widgets that mirror the hardware tab) is the right shape for `shotscript control`.
- **Importance**: 3. Wanted feature, mature core, but needs the EO completion and the polling thread replaced before merge.
- **Recommended action**: Ask author for: finish or remove EO support (append `enum_outputs` to the tree, tolerate missing `'EO'` key); replace the 10 Hz polling thread with event-driven reconnection; store channel tuples in item data rather than parsing display text; remove star imports and unused imports; squash the duplicated history. Consider merging the two `output_classes.py` fixes separately now.

### blacs #89: Retry attempts on communication between parent and child (mjdoris, opened 2021-06-17, last updated 2021-07-01)

- **What it does**: In `Tab.mainloop` the job request `to_worker.put(...)` and the acknowledgement `from_worker.get()` get a 30 s timeout; on `TimeoutError` the request is re-sent once and the acknowledgement awaited again, then `TimeoutError` is raised. In `Worker.mainloop` the two `to_parent.put(...)` calls (ack and result) get the same 30 s timeout and one retry.
- **Type**: bugfix (workaround)
- **Size**: 1 file, +34/-7, 1 commit
- **No-brainer?**: No. The retry is not safe at the protocol level.
- **Implementation**:
  - `WriteQueue.put(obj, timeout)` (zprocess `process_tree.py:429`) polls for `POLLOUT` and sends with `NOBLOCK`; a timeout means the message was never handed to zmq, so re-sending after a put timeout is safe. But a PUSH socket to a connected peer is almost always writable, so `put` effectively never times out; the retry only ever triggers from the `get(30)`.
  - A `from_worker.get(30)` timeout does not mean the worker did not receive the request. If the worker received it and is slow to ack (or the ack was lost), the parent re-sends the request; the worker then executes the job twice (duplicate `transition_to_buffered`, `program_manual`, etc.), and the parent reads the first job's ack as the second's ack, the first result as the second's result, and the second job's ack/result remain in the queue, so every later exchange in that tab is offset by two messages. The code has no sequence numbers to detect this.
  - A 30 s acknowledgement timeout is also too short for a worker blocked in a long preceding job: `mainloop` sends the next request only after the previous result, so the worker should be idle, but worker-side `init`/startup and heavy device calls that hold the GIL can exceed it.
  - Worker side: `to_parent.put(..., 30)` retry is harmless (put timeout means not sent) but equally never triggers; a raised `TimeoutError` in the worker loop kills the worker process.
  - Where retries belong (as the maintainer said in-thread) is in zprocess, with request IDs, or by removing the cause.
- **Up to date?**: Merges cleanly; 85 commits behind, but the surrounding lines in `tab_base_classes.py:813-825` and `921/948` are unchanged, so the patch applies. The root cause (PUSH/PULL sockets accepting stray connections) was diagnosed in the thread and fixed experimentally by switching to PAIR sockets; zprocess master (`process_tree.py:1299-1300,1428`) still uses PUSH/PULL, so that fix was never merged either. Nothing on master supersedes this PR.
- **Tested?**: Author ran it at NIST and reports one retry restores communication. It runs as written. The author then tested the PAIR-socket zprocess patch for a week without failures, which makes this PR the less-preferred fix by both parties.
- **Discussion state**: Last comment 2021-07-01 by the author confirming the PAIR patch works. Ball was with the maintainer (zprocess back-compat for PAIR sockets); nothing since. Author quiet for 5 years.
- **Breaking?**: Behaviour change: duplicate job execution in the retry path; otherwise none.
- **Rewrite relevance**: Design requirement for the rewrite's worker transport: request IDs and idempotent acks, and never bind a many-to-one socket for a one-to-one channel. The rewrite drops zmq, so the specific bug does not carry over.
- **Importance**: 1. Unsafe workaround for a problem whose fix lies in zprocess.
- **Recommended action**: Close as superseded by the diagnosis in the thread; if the NIST problem is still live, do the PAIR-socket change in zprocess (with a version check) rather than this.

### blacs #88: Add plugin lock monitor (zakv, opened 2021-02-06, last updated 2023-01-02)

- **What it does**: Adds `blacs/plugins/lock_monitor/` (3787 lines: 2073-line `__init__.py`, 702-line `lockers.py` base classes, 411-line `dummy_lockers.py`, 482-line README, `.ui`, screenshots). The plugin spawns one zprocess `Worker` per user-configured "locker" (import path to a user instance of a `Locker` subclass), and in the queue callbacks `pre_transition_to_buffered`, `science_starting`, `science_over`, `analysis_cancel_send`, `shot_ignore_repeat` asks each worker in parallel whether its laser is locked. On out-of-lock it optionally runs the locker's `lock()`; on failure it aborts the shot via `current_queue.put(['Queue Manager','abort'])`, re-cleans the h5 file with `QueueManager.clean_h5_file`, prepends it to the queue, pauses the queue and shows a notification. A `PluginTab` shows per-locker Monitor/Lock/Force-lock/Restart controls and an output box; a settings page edits the import-path list. `lockers.py` includes a `ScanZoomLocker` (scan-and-zoom relock algorithm using matplotlib plots to disk).
- **Type**: feature
- **Size**: 7 files, +3787/-0, 5 commits
- **No-brainer?**: No. Large, lab-specific functionality that the author themself says need not live in blacs.
- **Implementation**:
  - Code quality is high: docstrings throughout, threading locks around shared state, a per-worker timeout on `close()`, parallel callback dispatch with `ThreadPoolExecutor`, a clean separation of worker/parent code. It reuses `QueueManager.clean_h5_file`, `prepend`, `manager_paused`, `current_queue`, `tempfilename`, all of which exist on master.
  - It reimplements `Tab.mainloop`'s request/ack/result protocol in `Plugin.run_worker_method` (`__init__.py:409-474`) and drives blacs `Worker` processes directly from a `PluginTab`, because `PluginTab` has no state machine. The author notes the consequence: "Force Lock" and "Restart Worker" buttons act only at the next shot's `pre_transition_to_buffered`. This is a blacs API gap, not a plugin defect, but it means the plugin depends on `Worker.run(worker_name, device_name, extraargs)` and the private message protocol in `tab_base_classes.py`, both unchanged on master.
  - Imports `matplotlib` in `Plugin.__init__` (`__init__.py:95`) and calls `matplotlib.use('Agg')` globally; blacs does not depend on matplotlib, and the plugin would need to be an optional extra or the import moved into `lockers.py`/the workers.
  - Loggers: `lockers.py` imports `LOG_PATH` from `labscript_utils.setup_logging` to write per-locker log files; fine.
  - Qt usage (`Qt.Vertical`, `QSizePolicy.Minimum`) matches master conventions; no star imports. Unverified on PyQt6/PySide6 since the branch predates that work, but nothing in it looks binding-specific.
  - Aborts after `science_over` cannot un-run the shot; the plugin re-queues it and the README says so. The `callback_pre_transition_to_buffered` path blocks the queue thread while lockers run `lock()`, which is intended.
- **Up to date?**: Merges cleanly; 59 commits behind (rebased 2023-01-02). Contains the fix from #87 (`7f9552a`), which was merged on master (`dbeccbc`), so that dependency is satisfied. Issue #86 is the same bug. Not superseded.
- **Tested?**: Author used it in their lab; one external user (matth2peters, Dec 2022) ran it with `DummyLocker` and hit the #87 bug until rebasing. Runnable as written against master as far as the APIs it touches go.
- **Discussion state**: Author asked in Feb 2021 whether this belongs in the repo and raised f-strings/copyright/`inmain_decorator` questions; no maintainer response in 5 years. Ball is with the maintainer.
- **Breaking?**: No. Off by default.
- **Rewrite relevance**: Two requirements: (1) a pre-shot "go/no-go" hook that can abort, re-clean and re-queue a shot and pause the queue; (2) plugin tabs that can own worker processes with the same state machine as device tabs. The scan-and-zoom relock algorithm is hardware knowledge worth keeping as an example.
- **Importance**: 2. Good code, but 3.8k lines of lab-specific policy with a matplotlib dependency; better distributed as its own package, which blacs plugin loading currently makes hard.
- **Recommended action**: Close as out of scope for the blacs repo, with a note that blacs should gain a way to load plugins from installed packages (entry points) so this can ship as `blacs-lock-monitor`; if a plugin entry-point mechanism is not going to happen in legacy blacs, merging is defensible provided matplotlib becomes an optional extra and the author confirms PyQt6/PySide6.

## Ranking

| Rank | PR | Type | Importance | Action |
|---|---|---|---|---|
| 1 | #123 plugin-loading bugfixes | bugfix | 4 | Merge after small fixes (drop/justify `has_option` change, trim comments, document commit 3) |
| 2 | #105 Virtual Devices plugin | feature | 3 | Ask author: finish EO, remove polling thread, store tuples in item data, remove star imports, squash; merge `output_classes.py` fixes now |
| 3 | #88 lock monitor plugin | feature | 2 | Close as out of scope / separate package (or merge with matplotlib optional and Qt6 check) |
| 4 | #121 shared plugin refactor | refactor | 1 | Close as obsolete (labscript-utils counterpart closed; fixes resubmitted as #123) |
| 5 | #89 tab/worker retry | bugfix | 1 | Close; unsafe retry, superseded by PAIR-socket diagnosis in zprocess |

## 3.x PR review: lyse #132, lyse #118/#85, runmanager #104 + blacs #90, runmanager #128

All comparisons are to `origin/master`. Line numbers refer to the file as it is at the PR head unless stated otherwise.

### lyse #132: Read attributes of subgroups of the 'data' h5 group into the dataframe (chrisjbillington, opened 2026-02-16, last updated 2026-02-16)

- **What it does**: Adds four lines to `get_nested_dict_from_shot()` in `lyse/dataframe_utilities.py`. After the existing loop over `results/<group>`, it loops over `data/<name>` and stores `get_attributes(h5_file['data'][name])` as `row[name]`, so attributes written under `data/` appear in the dataframe as columns `(name, attr)`, in the same top-level namespace as results groups.
- **Type**: feature
- **Size**: 1 file, +4/-0, 1 commit
- **No-brainer?**: Nearly. The change is tiny and consistent with how `results/` is read, but it has one collision defect (below).
- **Implementation**:
  - `lyse/dataframe_utilities.py:69-72`: `row[groupname] = get_attributes(datagroup)` overwrites any results group of the same name read on lines 66-68. The FunctionRunner docstring (`labscript_devices/FunctionRunner/labscript_devices.py:49-67`) recommends saving raw data to `data/<device_name>` and saving results via `lyse.Run`, which puts them in `results/<device_name>`. That is exactly the case the PR is for, and in that case the results attributes are dropped from the dataframe. Fix: `row.setdefault(groupname, {}).update(get_attributes(datagroup))`, or write the data attributes into a separate namespace.
  - Datasets directly under `data/` (`data/waits` from NI_DAQmx, PrawnBlaster, Cicero; `data/traces/<device>` from TekScope is one level down and not reached) are also visited. `get_attributes` works on datasets, so this is harmless; it just means `waits` becomes a column prefix if that dataset ever has attributes.
  - No other code in the suite writes attributes to a direct subgroup of `data/` today (NI_DAQmx and AlazarTech write datasets under `data/traces`), so the only producers are FunctionRunner and user code. The blacs commit `ec3f6b1` "Don't error if 'data' group already exists" (merged in blacs #117, same author, same day) is the companion fix that lets a FunctionRunner create `data/` before BLACS does.
- **Up to date?**: Merges cleanly. 19 commits on master since the base; none touch `dataframe_utilities.py`. No dependency on other PRs.
- **Tested?**: No tests in the repo for this file. The code is trivially runnable; the collision case was probably not exercised.
- **Discussion state**: No comments. Maintainer's own PR, unreviewed by anyone else. It appears to be unmerged simply because nobody approved it, not because of an objection.
- **Breaking?**: Adds columns only. A user who has a results group and a `data/` group with the same name would see the results columns replaced (the defect above).
- **Rewrite relevance**: The rewrite's analysis dataframe builder should decide up front which HDF5 locations feed the dataframe and how namespaces are merged, rather than adding locations one at a time.
- **Importance**: 3. Small useful feature, but should not merge with the overwrite behaviour.
- **Recommended action**: Merge after one fix: merge the `data/` attributes into an existing `row[groupname]` dict instead of replacing it.

### lyse #118: Finally merging #85 (dihm, opened 2024-02-14, last updated 2025-04-14) and lyse #85: Renaming Run to Shot (philipstarkey, opened 2020-11-05, closed 2020-11-08)

- **What it does**: Renames `lyse.Run` to `lyse.Shot` and `Sequence.runs` to `Sequence.shots`, renames positional parameters (`run1, run2` to `shot1, shot2`; `run_paths` to `shot_paths`; `other_run` to `other_shot`), and rewrites "run" as "shot" in docstrings and docs. Compatibility shims: `class Run(Shot)` with `__init__` that emits a `FutureWarning`, and a `Sequence.runs` property that warns and returns a copy of the private `_Sequence__shots` dict. #118 is #85 merged with master as of 2024-02, plus five commits: `DeprecationWarning` changed to `FutureWarning`, docstrings, and softening of the "removed in v4.0" wording. #85 is the original and is already closed; it conflicts with master in the same files.
- **Type**: refactor
- **Size**: #118: 6 files, +104/-63, 9 commits (3 of them Phil's from #85). #85: 6 files, +70/-34, 3 commits.
- **No-brainer?**: No. It renames the class that every user's analysis script instantiates, and the discussion ended with the author recommending rejection.
- **Implementation**:
  - `lyse/__init__.py:1136-1137`: `Run.globals_diff` is an identical copy of the inherited `Shot.globals_diff`; it only exists to keep the parameter name `other_run`. Redundant.
  - `lyse/__init__.py:1175-1198`: `Sequence.runs` and `Sequence.shots` return `copy.copy()` of the dict. On master `Sequence.runs` is a plain attribute that users can mutate. Any user code that does `seq.runs[path] = ...` or `del seq.runs[...]` silently stops having an effect. Not mentioned in the PR.
  - `isinstance(x, lyse.Run)` is still true for `Shot` instances? No: `Run` is a subclass of `Shot`, so `isinstance(Shot(...), Run)` is False. User code that type-checks on `Run` (zakv said his lab subclasses `lyse.Run`) keeps working for subclasses but not for `Shot` objects produced by `Sequence`.
  - The `FutureWarning` fires once per worker process (Python's default filter), so most users will see it only when they restart lyse. dihm noted this and did not resolve it.
  - `lyse/__main__.py:2289-2295` changes an unrelated msgpack `DeprecationWarning` to `FutureWarning`, including a `raise FutureWarning(...)`. Unrelated to the rename and raising a warning class as an exception is odd either way.
  - The dataframe columns `run time`, `run number`, `run repeat`, `n_runs` and the HDF5 attributes they come from are untouched, so the rename is partial. dihm identified this as the main reason not to proceed.
- **Up to date?**: Conflicts with master in `lyse/__init__.py` (import block, the removed `_rangeindex_to_multiindex`, two docstring examples), `lyse/__main__.py` (module header), and `docs/source/introduction.rst`. 79 commits on master since the merge base, including the `lyse.utils` refactor (#119, #126), `__all__` (which lists `'Run'` and would need `'Shot'` added), the PySide6/PyQt6 work, and removal of star imports from docs. `docs/listing_1.py`, `docs/listing_3.py`, `docs/lyse.tex` and `README` still use `Run`. Outside lyse, `lyse.Run` is used in `labscript_utils/labscript_profile/.../example_IMAQdx_remote.py` and in the FunctionRunner docstring and test (`labscript_devices/FunctionRunner/labscript_devices.py:58-62`, `testing/test.py:14`). #85 is closed and fully superseded by #118.
- **Tested?**: dihm says he "confirmed that the merge hasn't broken anything and the FutureWarning shows" (2024-02-16). No automated tests. The code as it was at that time would have run; it no longer merges.
- **Discussion state**: Decided, in effect. dihm (2025-04-11) recommended rejecting it because the `run *` column and attribute names cannot be renamed compatibly; philipstarkey (2025-04-12) agreed to abandon it; ispielma (2025-04-13) asked for keeping both syntaxes with a deprecation, which is what the PR already does for the class name; dihm (2025-04-14) replied that duplicating the dataframe columns is the only compatible route and is not worth it now. Nobody closed the PR. The ball is with the maintainers to close it.
- **Breaking?**: `lyse.Run` keeps working with a warning. `Sequence.runs` becomes a read-only copy (behaviour change). Positional-only renames of `globals_diff(run1, run2)`, `Sequence(h5_path, run_paths)` break anyone passing these as keywords.
- **Rewrite relevance**: Pick "shot" consistently in the rewrite's API, dataframe columns and HDF5 attributes from the start; this PR shows the cost of renaming later.
- **Importance**: 1. Three of the four participants agreed to drop it, and it has rotted against master.
- **Recommended action**: Close both #118 and the already-closed #85 (nothing to do for #85) with a note that the rename is deferred to a major version where `run time`/`run number`/`run repeat`/`n_runs` can be renamed at the same time. If the maintainers do want the class alias alone, redo it on current master as a ~20 line change: `Shot = Run` plus a warning subclass, `__all__` update, docs; do not touch `Sequence.runs` semantics.

### runmanager #104: WIP: Compilation queue (chrisjbillington, opened 2022-01-07, last updated 2022-03-02) and blacs #90: WIP: compilation-queue BLACS implementation (chrisjbillington, opened 2022-01-07, last updated 2022-01-07)

- **What it does**: Replaces runmanager's `compile_queue` (a `queue.Queue` of `[labscript_file, run_files_iterator, ...]`) with a visible queue tab. `engage` now calls `queue_new_sequence()`, which computes filenames (`runmanager.make_run_filenames`, new) and stores per-shot details in `self.queued_shots` and a `QStandardItemModel`; the HDF5 shot file is only written (`make_single_run_file`, now with a `rep_no` argument that writes `run repeat`) immediately before compilation. The compile thread waits on a `threading.Event`, pops one shot at a time via `next_queued_shot()`, and supports pause, repeat-all / repeat-last (using a new `runmanager.new_rep_name()`), "delayed compilation" (only compile when BLACS has reported at most N shots remaining), and "dynamic globals" (a comma-separated `QLineEdit`; the named globals are re-evaluated from the current active groups at compile time and substituted into the shot). A new remote command `advise_BLACS_shots_remaining` is added to `remote.py` and `RemoteServer`. blacs #90 removes `QueueManager.new_rep_name` in favour of `runmanager.new_rep_name`, and at the top of every iteration of `QueueManager.manage()` calls `runmanager.remote.Client(timeout=5).advise_BLACS_shots_remaining(rowCount)`.
- **Type**: feature
- **Size**: runmanager: 4 files, +1090/-231 (of which `main.ui` is +874/-231 including a wholesale re-serialisation), 7 commits (4 from 2019, 3 from 2022). blacs: 1 file, +11/-17, 2 commits.
- **No-brainer?**: No. Explicitly WIP with an unfinished TODO list, conflicts with master, and rewritten by #130 underneath.
- **Implementation** (concrete defects):
  - `runmanager/__init__.py:1134-1157` `new_rep_name()`: off by one. It returns `(path_with_rep N+1, N)`, so the first repetition is named `_rep00001.h5` but gets `run repeat = 0`. Verified by running the function. BLACS's original `new_rep_name` returned `N+1`. Both consumers write this number to the file: `clean_h5_file(..., repeat_number=repeat_number)` in BLACS (`blacs/experiment_queue.py:460` writes `attrs['run repeat']`) and `make_single_run_file(..., rep_no=...)` in runmanager. BLACS's abort/restart paths re-read `run repeat` from the file and pass it to `clean_h5_file`, so the error propagates.
  - `new_rep_name()` docstring says it creates an empty placeholder file so that concurrent callers are race-free; the code does not create any file. With both BLACS repeat and runmanager repeat using the same `_repNNNNN` scheme on the same directory, two processes can choose the same name.
  - `runmanager/__main__.py:3341` `print(f"{n_seq=}")` and `:3953` `print("BLACS said how many shots it has:", value)` are debug prints.
  - `next_queued_shot()` (`__main__.py:3282-3320`) drains all queued BLACS reports and keeps only the last; if none arrived since the previous call it returns `None` when delayed compilation is on. After compiling one shot the loop calls it again, finds no new report, and stops. So at most one shot is compiled per BLACS report, even if BLACS reported 0 remaining and the threshold is 3. It relies on BLACS re-reporting (once per loop iteration, which is once per second when idle) for throughput.
  - Dynamic globals (`__main__.py:3346-3365`) take `evaled_globals[group][name]` directly. For a global that is a list or has an expansion, that is the whole evaluated list, not the per-shot element, so a dynamic global that is also a scan axis writes the whole list into the shot. A typo in the dynamic-globals field raises `KeyError`, caught by the broad `except`, which clears the entire queue. dihm asked for "all globals" and "whole group" options; neither is implemented.
  - On compile failure or exception, the whole queue is cleared (`inmain(self.queue_model.clear)`); the author marked this TODO. Abort only sets `compilation_aborted`, which makes `next_queued_shot` return `None` without pausing or clearing, so the next event (a BLACS report, a pause toggle) resumes compiling the remaining shots. Before this PR, abort discarded the remaining shots.
  - `self.ui.delay_compilation_options.setVisible(False)` with a TODO about settings restore; the queue state (pause, repeat mode, delayed-N, dynamic globals) is not saved to the runmanager config.
  - `main.ui`: the PR changes `<iconset>` to `<iconset resource="../../qtutils/icons/icons.qrc">` throughout and `<include location="../../qtutils/icons/icons.qrc"/>`. Harmless at runtime (icons are resolved from the `:/qtutils/...` resource path), but it re-serialises the whole file, which is why the diff is 874 lines and conflicts.
  - `remote.py:25` pops `timeout` from `**kwargs` of every request, so no remote command can ever take a `timeout` keyword of its own. None does today.
  - blacs `experiment_queue.py:509-517`: the client is created inside the thread and called on every loop iteration, including the idle `time.sleep(1)` loop, so BLACS makes one request per second forever and blocks the queue thread for up to 5 s per iteration when runmanager is not running (author acknowledges). `logger` is the thread-local logger defined at line 488, so the `except` is fine. Only the runmanager named in `[servers] runmanager` in labconfig is informed. The reported number is `rowCount` at the top of the loop, which includes the shot about to be dequeued but is not updated while a shot runs, so the description's "plus one if a shot is running" semantics are approximately but not exactly met.
  - The TODO list in the description (delete, reorder, repeat of individual queued shots) is still open; the model items are `setEditable(False)` and no context menu or drag handling exists.
- **Up to date?**: runmanager: conflicts in `runmanager/__main__.py` and `runmanager/main.ui`; `__init__.py` and `remote.py` auto-merge. 76 commits on master since the base (2022-01), 37 of them touching the files the PR changes (Qt6 compatibility, theming singleton, logging, `main.ui` edits). Against `origin/pr/130` it conflicts in `__init__.py`, `__main__.py` and `main.ui`; #130 moves `make_run_files`/`make_single_run_file`/`new_sequence_details` out of `__init__.py` into `runmanager/compiler.py` and cuts `__main__.py` by ~950 lines, so every runmanager-side change in #104 would have to be reimplemented in #130's structure. blacs #90 merges cleanly (66 commits since base, 6 to `experiment_queue.py`, none to the touched hunks) but is useless without #104 and depends on `runmanager.new_rep_name`, which only exists in #104. The two PRs must land together or not at all.
- **Tested?**: Author says the feature was in use ("this WIP PR can be used to get the feedback feature working"). Manual testing only; the leftover prints are consistent with that. No automated tests.
- **Discussion state**: philipstarkey objected to BLACS pushing state to runmanager (reverses the data-flow direction, both apps must know about each other) and asked why runmanager does not poll. Author answered: latency, and proposed long-polling (runmanager asks "reply when the count changes or after n s"), which needs BLACS's ZMQ server to hold multiple pending replies like zlock. dihm requested "all globals" and "whole group" dynamic-globals options. No further activity since 2022-03. The ball is with the author (who is the maintainer being reported to).
- **Breaking?**: Behaviour: shot files are no longer created at engage time but just before compilation; `make_run_files` is retained so library users are unaffected; `run repeat` attribute is now written by runmanager (value 0) on every shot, which lyse already tolerates. New remote command; new labconfig `[servers] runmanager` requirement for BLACS. Abort semantics change (see above).
- **Design question (push vs PUB/SUB vs poll)**: With BLACS pushing a REQ to one named runmanager, as implemented, the coupling that philipstarkey objected to is real and the blocking in BLACS's queue thread is a liability. PUB/SUB from BLACS ("queue length changed" events on a known port, any number of runmanagers subscribing) removes the labconfig dependency, the blocking, and the one-runmanager limit; the deadlock the author worried about does not exist with PUB/SUB because the publisher never waits. Its weakness is that a subscriber that starts late has no current value until the next event, so BLACS must re-publish periodically (it already does in this PR) or runmanager must additionally request the current value once at start-up over the existing REQ/REP port. That hybrid (REQ for the initial value, SUB for updates) is the standard fix and matches the "ask once, then get notified" long-poll proposal with less server complexity. Of the three options, PUB/SUB plus one initial request is the one worth doing for the legacy suite; pure polling is acceptable at 1 Hz if latency of under a second is tolerable, which for JIT compilation it probably is.
- **Rewrite relevance**: High for design, not code. The rewrite is dropping zprocess/zeromq, so the transport question is moot there, but the requirements this PR exposes carry over: a visible compile queue; just-in-time compilation gated on the controller's remaining-shot count; per-shot re-evaluation of marked globals at compile time for synchronous intra-sequence feedback (and the need to decide how an expanded/scan global interacts with "dynamic"); repeat numbering owned by one component; and the controller publishing its queue state rather than being asked.
- **Importance**: 2 for the legacy suite as a mergeable PR; 4 as a design record. It cannot be merged in this form and would need a rewrite on top of #130.
- **Recommended action**: Close #104 and #90 as superseded by #130's restructuring, or convert #104 to a draft/issue listing the requirements and the design decision (PUB/SUB plus initial request). If the feature is still wanted in the legacy suite, reimplement it against #130's `compiler.py`, fix the `new_rep_name` off-by-one and the overwrite-on-error behaviour, and implement BLACS reporting as PUB/SUB from a queue-manager hook rather than a REQ inside the queue loop.

### runmanager #128: Show active config path in window title (ispielma, opened 2026-04-07, last updated 2026-04-07)

- **What it does**: Makes `RunManager` inherit a new `labscript_utils.labconfig.LabscriptApplication` mixin, which provides `init_config_window_title()`, `get_default_config_file()` and `set_config_window_title(filename)`. The title becomes `runmanager - ~/labscript-suite/userlib/app_saved_configs/<apparatus>/runmanager/runmanager.ini` at start-up and after each save/load of a configuration. It also changes the default save/load dialog directory from `<experiment_shot_storage>/runmanager.ini` to `<app_saved_configs>/runmanager/runmanager.ini`, and changes `QtGui.QShortcut` back to `QtWidgets.QShortcut` in three places.
- **Type**: feature
- **Size**: 1 file, +22/-8, 1 commit
- **No-brainer?**: No. It does not run against labscript-utils master and contains an unrelated Qt6 regression.
- **Implementation**:
  - `runmanager/__main__.py:57-62` imports `LabscriptApplication` from `labscript_utils.labconfig`. That class does not exist on labscript-utils `origin/master`. It is in labscript-utils commit `f1d4a98` (`labscript_utils/labconfig.py`, +71 lines: `format_path_for_display`, `get_default_appconfig_file`, `LabscriptApplication`), which is only on `origin/pr/125` and `origin/pr/127`, neither of which is in the open-PR list for labscript-utils (only #117 is open). So the dependency PR appears to have been closed unmerged, and this PR raises `ImportError` at start-up as it stands.
  - `runmanager/__main__.py:1807-1812`: `QtGui.QShortcut` replaced by `QtWidgets.QShortcut`. Master deliberately changed these to `QtGui.QShortcut` in `07a0f08` ("Changes for Qt6, that are backward compatible with PyQt5"). In PyQt6 and PySide6, `QShortcut` lives in `QtGui` and `QtWidgets.QShortcut` does not exist, so this hunk breaks runmanager under Qt6, which master now supports. It is unrelated to the title feature and looks like a stale local change.
  - `:1617-1642`: when there is no `autoload_config_file`, the title shows the default config path even though nothing has been loaded from it, and the file may not exist. Showing nothing (or "unsaved") until a file is loaded or saved would match what the title claims to verify.
  - The change of the default save/load dialog directory is a behaviour change not mentioned in the description. It is arguably correct (it is where BLACS and lyse keep their configs) but is a separate decision.
  - `get_default_appconfig_file` in the dependency mutates `exp_config` (`set('DEFAULT', 'app_saved_configs', ...)`) as a side effect of a getter; copied from the BLACS/lyse start-up pattern.
- **Up to date?**: Based on the current master tip (0 commits behind); merges cleanly into master. Conflicts with `origin/pr/130` in `runmanager/__main__.py` (#130 rewrites the areas around `__init__`, save/load config). Depends on labscript-utils PR #125 (closed/unmerged). Companion PRs exist as refs with the same commit message dated 2026-04-07: blacs `origin/pr/120` (`efc03e2`), lyse `origin/pr/137` (`c4182ca`), runviewer `origin/pr/71` (`01b5931`), labscript-utils `origin/pr/125` (`f1d4a98`). None of blacs #120 or lyse #137 appears in the open-PR lists for those repos, and the commits are not on any master, so they were closed without merging; runviewer's open-PR list was not captured. The runmanager PR is the leftover of a five-repo change whose other four parts are closed. Master does not already do this: the only `setWindowTitle` calls on master are for message boxes, the runmanager output pop-out, lyse plot windows and the BLACS recompile dialog.
- **Tested?**: Nothing stated. It can only have been run with the author's labscript-utils branch installed.
- **Discussion state**: No comments. Ball is with the maintainers; the author has not been asked anything.
- **Breaking?**: Default config dialog directory moves. `QShortcut` change breaks Qt6 users. Otherwise cosmetic.
- **Rewrite relevance**: Showing the active config path in the title bar is a reasonable UX default for `shotscript control` and any GUI; one line.
- **Recommended action**: Ask the author whether labscript-utils #125 and the blacs/lyse/runviewer companions were withdrawn and why; if the feature is still wanted, either merge the mixin into labscript-utils first or inline the ~10 lines into runmanager and drop the mixin. Require removal of the `QShortcut` hunk. If the companions were abandoned deliberately, close this one as orphaned.

## Ranked summary

| Rank | PR | Type | Importance | Action |
|---|---|---|---|---|
| 1 | lyse #132 data-group attributes in dataframe | feature | 3 | Merge after fixing the overwrite of same-named results groups |
| 2 | runmanager #128 config path in title | feature | 2 | Ask author about the closed labscript-utils #125 dependency; drop the QShortcut hunk; otherwise close as orphaned |
| 3 | runmanager #104 + blacs #90 compilation queue | feature (WIP) | 2 (4 as design record) | Close as superseded by #130, or convert to an issue; reimplement on `compiler.py` with PUB/SUB if still wanted |
| 4 | lyse #118 / #85 Run to Shot | refactor | 1 | Close; participants already agreed to abandon |

## 3.x Review: PrawnBlaster #37, #35; prawn_digital_output #23; pineblasterv2 #1; labscript-utils #117

All comparisons are against the PR's base branch as fetched (`origin/pr/N` vs `origin/overclock`, `origin/master` or `origin/main`). Line numbers refer to the file as it is in the PR head.

### PrawnBlaster #37: Add logic tree for conditional voltage setting based on freq request (Json-To-String, opened 2025-08-25, last updated 2025-08-27)

- **What it does**: In `setclock`, picks the core voltage from the requested frequency: above 200 MHz sets 1.30 V and prints a WARNING line; between the board's normal limit (133 MHz RP2040, 150 MHz RP2350) and 200 MHz sets 1.20 V; otherwise 1.10 V. Removes the frequency upper-bound rejection entirely, and removes the separate `_overclock` firmware build (the `foreach(overclock ...)` loop in `prawnblaster/CMakeLists.txt` and the `PRAWNBLASTER_OVERCLOCK`/`1.2.0-overclock` version variant). Limits are passed from CMake as `PRAWNBLASTER_NORMAL_FREQ_LIMIT`/`PRAWNBLASTER_OVERCLOCK_FREQ_LIMIT`.
- **Base branch**: `origin/overclock` exists. It is master at 7e22575 (the #30 merge, 2025-04-25) plus 3 commits: #36 (Jason Pruitt, adds `hardware_vreg`, a `getvolts` command, a crude `freq >= 150 MHz -> 1.30 V else 1.10 V` rule, and `tests/rp2040`, `tests/rp2350` notebooks plus about 70 PNG screenshots) and dihm's 2cd59b3 "Fix board dependent frequency bounds" (RP2040 non-overclock limit raised from 133 to 200 MHz). `overclock` lacks 4 master commits (#40, readme only). PR 37 merges cleanly into both `overclock` and `master`.
- **Type**: firmware / feature
- **Size**: 2 files, +60/-74, 2 commits
- **No-brainer?**: No. It changes the voltage/frequency sequencing on hardware and removes a safety limit, and it leaves the build/release pipeline and docs inconsistent.
- **Implementation**:
  - `prawnblaster/prawnblaster.cpp:1041-1050`: the voltage is set before `src` is validated and before `set_sys_clock_khz()` runs. If `set_sys_clock_khz` fails ("Cannot exactly achieve that clock frequency") or `src > 2`, the voltage has already changed while the frequency has not. Worse (dihm's review point): when going from an overclocked state to a lower frequency, the voltage is lowered first and the core runs at the high frequency on the lower voltage until the PLL is reconfigured. The correct order is: raise voltage, then frequency, when increasing; lower frequency, then voltage, when decreasing. A short settle delay (the common RP2040 practice is `sleep_ms(10)` after `vreg_set_voltage`) before changing the PLL is also absent.
  - `prawnblaster.cpp:1043`: the WARNING line is printed before `ok\r\n` and is terminated with `\n`, not `\r\n`. The labscript-devices worker (`labscript_devices/PrawnBlaster/blacs_workers.py:374`, `send_command_ok`) requires the first response line to be exactly `ok\r\n`, so any request above 200 MHz raises `LabscriptError` on the host. Either print the warning after `ok` or drop it (the host already knows the frequency it asked for).
  - Host compatibility: `labscript_devices/PrawnBlaster/labscript_devices.py:150,239` still rejects `clock_frequency` above 133/150 MHz, so with the stock host nothing in the new 1.20/1.30 V tiers is reachable; `blacs_workers.py:142-151` detects overclock firmware by the `-overclock` version suffix, which this PR removes, so that code becomes dead. The firmware `VERSION` stays `1.2.0` although behaviour (no upper limit) changed, so the host cannot distinguish limited from unlimited firmware.
  - `.github/workflows/build.yaml:40-41` and `readme.md:161-162,192-197` still reference `prawnblaster_rp2040_overclock.uf2` / `prawnblaster_rp2350_overclock.uf2`, which are no longer built; the tag-triggered release step lists files that will not exist. `readme.md:37,107` still state 133/150 MHz maxima.
  - `prawnblaster/CMakeLists.txt:8-10`: commented-out `if(overclock)` leftovers. `prawnblaster.cpp:1046`: `&& freq <= overclock_freq_limit * MHZ` is redundant inside the `else if`.
  - Voltage values: 1.10 V is the default on both chips; 1.20 V for RP2040 at up to 200 MHz is the usual overclock setting; 1.30 V is the maximum the SDK allows on RP2350 without `vreg_disable_voltage_limit()`, so the tiers are plausible. Setting the voltage from the frequency of an external clock input (`src` 1 or 2) is reasonable.
- **Up to date?**: Merges cleanly into `overclock` and `master`. Conflicts with PR #35 in `prawnblaster.cpp` (both touch the `VERSION` block). Not superseded.
- **Tested?**: Author reports testing on RP2040 and RP2350 boards; the `tests/` notebooks on the `overclock` branch (merged in #36) exercise 100 and 200 MHz with a time tagger. PR CI builds the firmware, but the release step is only run on tags, so the missing `_overclock` files would only fail at release time. dihm's ordering concern has not been tested.
- **Discussion state**: dihm reviewed 2025-08-27 ("minor comments, otherwise looks pretty good; test thoroughly before merging") and raised the voltage-before-frequency ordering concern. Author pushed a cleanup commit the same day. No activity since; ball is with the author (ordering test) and maintainer (decision on dropping the frequency limit).
- **Breaking?**: Removes the `_overclock` firmware variant and the frequency upper bound (any frequency accepted at 1.30 V with a warning); release artefact names change. Protocol change only for frequencies above 200 MHz (extra line before `ok`).
- **Rewrite relevance**: The per-chip voltage tiers and the ordering rule (voltage up before frequency up, frequency down before voltage down) are device knowledge for a shotscript PrawnBlaster driver if it exposes clock frequency.
- **Importance**: 3. Useful consolidation of the overclock firmware, but it must not merge with the response-ordering break and the stale release workflow.
- **Recommended action**: Merge after fixes: (1) reorder voltage/frequency changes and only change voltage once `src` is validated and `set_sys_clock_khz` has succeeded; (2) print the warning after `ok\r\n` with `\r\n`, or remove it; (3) update `build.yaml`, `readme.md` and bump `VERSION` (1.3.0 or similar); (4) in labscript-devices, raise `max_frequency_map` behind an explicit opt-in (e.g. `allow_overclock`) and remove the `-overclock` suffix parsing. Then rebase `overclock` onto master and merge both.

### PrawnBlaster #35: Allow a variable number of instructions per pseudoclock (philipstarkey, opened 2025-04-25, last updated 2025-04-25)

- **What it does**: Adds `setnuminstructions <pseudoclock> <n>`, which reassigns instruction storage between pseudoclocks. Instruction storage becomes a list of per-pseudoclock word counts (`num_pseudoclock_instructions[4]`, 2n+2 words each) with start addresses computed by summing the preceding counts. `set`, `get`, `setb` and the DMA setup use the new offsets; `setnumpseudoclocks` resets to equal shares. Also fixes a stray `%u` in the `setnumpseudoclocks` sscanf format and bumps `VERSION` to 1.3.0. Readme documents the command. Fixes #31.
- **Type**: firmware / feature
- **Size**: 2 files, +145/-24, 4 commits
- **No-brainer?**: No. Author warns it is not well tested, there is a response-protocol bug, and the host has no way to use it.
- **Implementation**:
  - `prawnblaster/prawnblaster.cpp` `setnuminstructions` handler (new block after `setnumpseudoclocks`): the success branch calls `set_num_prawnblaster_instructions()` and `reset_instructions()` but never prints `ok\r\n`. Every other command replies; a host using `send_command_ok` would time out.
  - `set `, `get `, `setb ` handlers: `pseudoclock_instruction_start_addr(pseudoclock)` and `get_num_prawnblaster_instructions(pseudoclock)` are now evaluated before `parsed` and the `pseudoclock > 3` / `>= num_pseudoclocks_in_use` checks. On a malformed command `pseudoclock` is uninitialised, and on `set 7 ...` it is out of range, so `num_pseudoclock_instructions[]` is read out of bounds (and the start-address loop runs up to `pseudoclock` iterations). On master the offset was plain arithmetic, so this is a new fault path. Move the two calls after validation.
  - Memory accounting is correct: the array is `2*max_instructions + 8` words; each pseudoclock owns `2n+2` words (the +2 is the unwritable stop pair); default `n = max/k` gives `2*max + 2k <= 2*max + 8` for `k <= 4`; `num_free_prawnblaster_instructions()` is `(array - others - 2)/2`, so the sum never exceeds the array. A single pseudoclock can be given `max_instructions + 3` (the unused slack), which is harmless but differs from the documented total.
  - `setb` keeps the pre-existing off-by-one `start_addr + inst_count >= n` (should be `>`), which rejects a program that exactly fills its allocation. Previously the check was against the total `max_instructions` (so it was wrong in the other direction for multi-pseudoclock); now it is per pseudoclock and the off-by-one becomes reachable whenever a labscript program compiles to exactly `max_instructions` instructions (`labscript_devices.py:451` only pads a stop instruction when the program is shorter than the maximum).
  - No `getnuminstructions` query, so a host cannot verify or recover the allocation after a reconnect (the firmware state persists while BLACS restarts).
  - `configure_pseudoclock_pio_sm`: `max_words` and `maximum_pseudoclock_instructions` hold the same value; cosmetic.
  - Host side: `labscript_devices/PrawnBlaster/labscript_devices.py:232-235` fixes `max_instructions = total // num_pseudoclocks` for every pseudoclock, and the worker only sends `setnumpseudoclocks`. To use this feature the device class needs a per-pseudoclock instruction count argument, per-clockline limits in `generate_code`, and the worker must send `setnuminstructions` after `setnumpseudoclocks` when firmware version >= 1.3.0. None of that exists or is proposed.
- **Up to date?**: Merges cleanly into master (master has only the 4 readme commits from #40 since the PR's base). Conflicts with PR #37 and will conflict with the `overclock` branch in `prawnblaster.cpp` (`VERSION` block and nearby code). Not superseded.
- **Tested?**: Author: "This isn't well tested!" The missing `ok` response means it cannot have been exercised through `send_command_ok`; only manual terminal use (where the lack of `ok` is just silence) is consistent with the code.
- **Discussion state**: No review comments. Author is a core maintainer; stale since 2025-04-25.
- **Breaking?**: Firmware-only; default behaviour (equal split) unchanged. Version bump to 1.3.0 is fine for the host (`min_version` is 1.1.0).
- **Rewrite relevance**: The per-pseudoclock allocation (a Novatech-clocking pseudoclock needs few instructions) is a real use case; a shotscript PrawnBlaster worker could adopt the command once the firmware is fixed.
- **Importance**: 3. Addresses a genuine limitation (#31), but needs fixes and a host-side counterpart before it is useful.
- **Recommended action**: Rework by maintainer (or ask author): add the `ok` reply, move offset computation after validation, fix the `setb` bound to `>`, add `getnuminstructions`, rebase onto the merged overclock work; then a labscript-devices PR adding per-pseudoclock instruction counts.

### prawn_digital_output #23: Basic testing notebook (dihm, opened 2025-11-17, last updated 2025-12-12)

- **What it does**: Adds `testing/basic_tests.ipynb` and `testing/KeysightScope.py`. The notebook opens a serial port to a PrawnDO, configures a Keysight scope over pyvisa (4 channels, trigger), and runs three checks: manual toggling (`man`), a `set`-programmed sequence (`swr`), and a binary bulk write (`adm`), capturing a scope screenshot after each. `KeysightScope` is a small SCPI wrapper (screenshot, timebase, annotation, channel scale/offset). `.gitignore` gains `*.pyc`.
- **Type**: tooling-CI (manual hardware test)
- **Size**: 3 files, +631/-1, 2 commits
- **No-brainer?**: No, because the committed notebook contains outputs and a hard-coded port; as a concept it is fine.
- **Implementation**:
  - Outputs are not stripped: three embedded PNG screenshots, stream outputs and execution counts are committed; the notebook is 192 KB. Re-running will produce a diff on every run. Strip outputs (nbstripout) or save screenshots to an ignored directory.
  - Cell 0: `PORT = 'COM7'` hard-coded (Windows). Kernel metadata names a custom kernel `Pico`. Scope is selected as the first `USB?*::INSTR` resource (`KeysightScope.py:8-13`). Parameters should be gathered at the top with a comment; the port is the only one that must change per machine.
  - Cell 10/14/18: `if SHOW_IMAGES: ... elif SAVE_IMAGES:` means images are never saved while they are shown; should be two independent `if`s.
  - Cell 5 `send()`: if `serial.Serial()` raises, `conn` is `None` and `finally: conn.close()` raises `AttributeError`, masking the original error.
  - No requirements note (pyvisa plus a VISA backend, pyserial, numpy, IPython).
  - Does it belong in the repo? The sibling PrawnBlaster repo already carries `tests/` notebooks with about 70 screenshots (merged by dihm in #36), so a `testing/` directory with a hardware-in-the-loop notebook is consistent with current practice. It is maintainer-only tooling tied to one scope model; acceptable if kept output-free and small.
- **Up to date?**: Merges cleanly into `main`; `main` has 3 later commits (#22 fixes, #28 download-URL fix) that do not touch these files.
- **Tested?**: The committed outputs show it was run end to end on real hardware (device responses and screenshots present).
- **Discussion state**: No comments. Author is the repo maintainer; ball is with dihm.
- **Breaking?**: No.
- **Rewrite relevance**: A scope-driven acceptance test for a pseudoclock/digital-output device is the kind of hardware check shotscript's device tests could reuse; the SCPI helper is generic.
- **Importance**: 2. Low risk, low urgency; housekeeping before merge.
- **Recommended action**: Merge after small fixes: strip outputs, move `PORT` and the VISA address to a parameters cell, fix the `if/elif`, guard `conn.close()`, add a one-line requirements note.

### pineblasterv2 #1: Modifications to run Wi-Fire board as a pseudoclock (ARFritsch, opened 2020-11-22, last updated 2020-11-23)

- **What it does**: Three changes to `PineBlasterV2.ino`, none guarded by board: (1) removes the `Serial.println("ready")` at the end of `setup()`; (2) in `start_clock()` replaces `Serial.attachInterrupt(serialInterruptDuringRun)` with the PineBlaster v1 mechanism, a `reset_on_serial` flag plus a naked ISR placed with `at_vector(24)` that jumps to the `reset` label when the flag is set; (3) comments out `detachInterrupt(0)` in `run_clock()` after a wait completes.
- **Type**: firmware / bugfix
- **Size**: 1 file, +19/-3, 4 commits (one is an empty merge of master)
- **No-brainer?**: No. It removes behaviour for both supported boards to work around symptoms whose root cause is elsewhere, and the repository is dormant.
- **Implementation**:
  - Repository state: last code commit 2017-01-11, readme edits 2020-04-29, readme still says "Under Development"; labscript-devices has only the v1 `PineBlaster.py` (15000 instructions, `hello`/`ok`/`done` protocol) and no V2 class. The repo is effectively archived.
  - Root cause of the `'o'` instead of `'ok'` symptom: `readline()` (`PineBlasterV2.ino:470-487`) returns at the first `\r` and leaves the `\n` of the host's `start\r\n` unread. `start_clock()` prints `ok` and attaches the serial interrupt; the `\n` arrives about 87 us later at 115200 baud, fires the interrupt and resets the board mid-transmission. The fix is to consume the trailing `\n` (or terminate on `\n`) before attaching the interrupt, not to replace the abort mechanism.
  - The replacement ISR (`PineBlasterV2.ino:46-59`) is copied from v1, which targeted the PIC32MX (Max32), where vector 24 is UART1. On the PIC32MZ (WiFire) `Serial` is a different UART with a different vector number, so this handler is most likely never invoked there; abort-on-serial during a run becomes dead code on the WiFire, which is also why the reset symptom disappears. On the Max32 the handler now overrides the core's UART handler, and the `beq $k0, $zero, IntSer0Handler` branch targets the function's own entry; whether this resolves to the chipKIT core handler as in v1 depends on how the core names its handler and should be verified by someone with the v1 toolchain. The maintainer wrote the v1 trick and can judge this quickly.
  - Commenting out `detachInterrupt(0)` leaves the trigger-pin interrupt enabled during the run, which the surrounding comment says slows execution (timing after a wait). The author's symptom (no `done`) points at the chipKIT core 1.3.1 `detachInterrupt` behaving differently on MZ; this needs an MZ-specific replacement rather than deletion.
  - Removing `ready`: needed for the labscript `PineBlaster.py` handshake (opening the FTDI port resets the board, and the stray `ready\r\n` would be read as the reply to `hello`), but the BitBlaster host code (`bitblaster.py` in this repo) expects it. Should be mode-dependent or flushed on the host.
  - The author's "fixing a typo" commit and the merge commit add nothing.
- **Up to date?**: Merges cleanly; master has had no commits since the PR. Nothing supersedes it; nothing in labscript-devices consumes this firmware.
- **Tested?**: Author tested on a WiFire with Arduino IDE 1.6.7 and chipKIT core 1.3.1 and reports it works with BLACS. Not tested on Max32; the changes apply to both boards.
- **Discussion state**: No maintainer response in 5 years. Ball is with the maintainer.
- **Breaking?**: Yes for Max32 and BitBlaster-mode users (no `ready`, changed abort mechanism, trigger interrupt left attached).
- **Rewrite relevance**: None.
- **Importance**: 1. Dormant repository, no host support, board-specific workaround with likely regressions on the other board.
- **Recommended action**: Close as out of scope (archive the repo and say so in the readme). If pineblasterv2 is to be revived, ask for: the trailing-newline fix instead of removing the serial-abort path, `#if defined(__PIC32MZXX__)` guards, and an MZ-correct `detachInterrupt`.

### labscript-utils #117: Add minimal example analysis script (Json-To-String, opened 2025-08-05, last updated 2025-08-05)

- **What it does**: Adds `labscript_profile/default_profile/userlib/analysislib/example_apparatus/example_analysis_script.py`: a lyse script that takes the current shot (or the last in the DataFrame), opens it with h5py, reads `devices/intermediate_device/OUTPUTS` (`analog_out`, `digital_out` columns), plots both, and saves a result with `run.save_result`. It is modelled on the existing `example_IMAQdx_remote.py` but uses the dummy devices from the default profile's `connection_table.py`/`example_experiment.py`.
- **Type**: docs-example
- **Size**: 1 file, +54, 1 commit
- **No-brainer?**: Nearly, but the final line raises, so not as is.
- **Implementation**:
  - Names match master: `connection_table.py` and `example_experiment.py` (both in `labscript_profile/default_profile/userlib/labscriptlib/example_apparatus/`) define `pseudoclock` and `intermediate_device` with children `analog_out` and `digital_out`; `DummyIntermediateDevice.generate_code` (`labscript-devices/labscript_devices/DummyIntermediateDevice.py:91`) writes `OUTPUTS` with one column per child named after the device (float64 / int8); `DummyPseudoclock` writes `PULSE_PROGRAM` (`labscript_devices/DummyPseudoclock/labscript_devices.py:114`).
  - `example_analysis_script.py:50-54`: `run.save_result('foobar', result)` with `result` a dict of two numpy arrays. `lyse.Run.save_result` stores attributes via `labscript_utils.properties.set_attributes`; h5py rejects the dict (object dtype), the fallback `serialise()` calls `json.dumps` with a `_default` that only handles `np.integer`, so an ndarray raises `TypeError`. The script fails on its last line every run. Use `run.save_result_array()` for the arrays, or save scalars (e.g. `analog_data.max()`), which also fits the comment about the results group.
  - Line 34: x-axis labelled `time (ms)`, but `OUTPUTS` has one row per pseudoclock tick (change times), not uniform milliseconds. Label it `clock tick` or plot against `PULSE_PROGRAM`-derived times.
  - Unused: `pulse` (line 27, marked unused), `run_globals` (line 20), `np.array()` wrappers (lines 32-33). Line 39 has a doubled `# #`. Line 48 comment still says "image processing" (copied from the IMAQdx example). Cosmetic.
  - Dependency on #116: there is no `origin/pr/116` ref, #116 is not in the open-PR list, and no master commit references #116, so #116 was closed without merge. This script does not need it; the connection table and experiment it uses have been in master since 2020 (#54).
- **Up to date?**: Merges cleanly; master has 22 later commits, none touching the profile directory.
- **Tested?**: Not stated. The `save_result` failure means it was not run to completion in lyse as written (the plot would show, then the error).
- **Discussion state**: No comments; ball is with the maintainer. Author active elsewhere in the suite.
- **Breaking?**: No.
- **Rewrite relevance**: A minimal end-to-end example (dummy connection table, experiment, analysis) is the smoke test shotscript needs too; the script itself is legacy-specific.
- **Importance**: 3. Cheap, gives the default profile a runnable lyse example for integration testing, which is currently missing (the only analysis example needs a remote camera).
- **Recommended action**: Merge after small fixes: replace the dict `save_result` with `save_result_array` or scalar results, fix the x label, remove the unused variables and stale comments.

## Ranking

| Rank | PR | Type | Importance | Action |
|---|---|---|---|---|
| 1 | PrawnBlaster #37 overclock voltage logic | firmware/feature | 3 | Merge after fixes: voltage/frequency ordering, warning after `ok`, update build.yaml/readme/VERSION; host `max_frequency_map` opt-in |
| 2 | labscript-utils #117 example analysis script | docs-example | 3 | Merge after small fixes: `save_result` dict -> `save_result_array`/scalars, x label, unused variables |
| 3 | PrawnBlaster #35 variable instructions per pseudoclock | firmware/feature | 3 | Rework: add `ok` reply, validate before computing offsets, `setb` bound, `getnuminstructions`; then host-side support |
| 4 | prawn_digital_output #23 testing notebook | tooling | 2 | Merge after small fixes: strip outputs, parameterise port/VISA address, fix `if/elif` |
| 5 | pineblasterv2 #1 Wi-Fire modifications | firmware/bugfix | 1 | Close as out of scope; archive repo. Root cause is the unread `\n` after `\r` before attaching the serial interrupt |

## 4. Pull requests opened by the maintenance track

Seventeen pull requests were opened on 2026-10-17 from this repository for the release
blockers (labscript #123 in three repos, zprocess #27, labscript-utils #28, and the Python
3.11 metadata change in twelve repos). They are listed with links and status in
`PULL-REQUESTS.md`, not here; this document covers the pull requests that existed when the
review was made.
