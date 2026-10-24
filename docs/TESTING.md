# Test harness results

Results of running `harness/suite.py` (see `harness/README.md`) on the component default
branches, and the defects that the runs found. Newest first. Each run is identified by
the date, the platform, the Python version and the commits in the report's component
table.

## 2026-10-24: lazy logging arguments (`lazy-logging` branches, no pull requests)

Branches `lazy-logging` in zprocess (111d879), labscript-utils (7462277),
labscript-devices (40e1c77), blacs (0f1c11d), lyse (5a3c252), runmanager (76c6d09) and
runviewer (f51c472) change every logging call that formatted its message with `%`,
`str.format`, an f-string or concatenation to pass a format string and arguments; about
180 calls, found by parsing the sources. labscript, qtutils, desktop-app and
labscript-c-extensions have none. Calls with arguments that do work beyond attribute
access are few: the zlock server's decoding of client IDs and keys on every acquire and
release (now done when the record is formatted), lyse's join of the added shot paths
(now behind `isEnabledFor(INFO)`), version lookups at application start, and traceback
formatting in error paths. blacs #136 adds two `', '.join(sorted(self.pending))`
arguments per transition, which are left as they are. A static check found no call in
which the number of placeholders differs from the number of arguments.

The branches are added to `integration-testing/branches`. `build.sh` needed new
resolutions for blacs (`experiment_queue.py` and `tab_base_classes.py` with #135 and
#136) and lyse (`routines.py` with #153 and #157), and the patch
`narwhal-lazy-logging.patch` changes the connection message of labscript-devices #162.
The rebuilt branches are blacs e47dca2, labscript-devices 5680d70, labscript-utils
bbe0d4f, lyse de7bf03 (later 706f72f with #160), runmanager 67564cc, runviewer 5012009
and zprocess a399e6f; a second build of blacs reproduced the hand resolution exactly.

Locally (Python 3.14.8, PySide6) the harness passed every step on these branches,
including `apps`, `lyse-gui` and `blacs-shot`, with no logging errors in the step logs.
The zprocess tests passed outside the namespace; inside it, `test_cant_create_files`
fails because the mapped root user can create the file. `deploy.sh` checked the branches
out in `diginuc:~/labscript-suite/dev`, and in the diginuc venv the changed modules of
every component import from the clones (the NI_DAQmx worker is not importable there: no
NI-DAQmx library). No shot was run on diginuc.

## 2026-10-24: pandas 3.1.0 and lyse #160 (D43)

pandas 3.1.0 (released 2026-10-22) issues a `Pandas4Warning` when `.at` sets a value with
a column key that is not in the dataframe; pandas 3.0.6 and 2.3.3 issue none. Setting an
existing cell with `.at` issues no warning. On pandas 3.1.0, with three-level column
labels, creating a column takes 0.34 to 0.41 ms with `.at` and 0.28 to 0.38 ms with `.loc`
for dataframes from 100 rows × 200 columns to 10000 × 1000; setting an existing cell
takes 13 to 14 µs with `.at` and 60 to 70 µs with `.loc`. For 18 value types (scalars,
strings, `None`, lists, tuples, 0-d, 1-d and 2-d arrays, bytes, complex, timestamps),
lyse's `_set_dataframe_value` with `.loc` for new columns gives the same column values and
dtypes as with `.at` on pandas 2.3.3, 3.0.6 and 3.1.0. The `catch_warnings(record=True)`
in lyse's shot-loading thread also records warnings that the main thread issues while a
shot is loading (checked with a two-thread script on Python 3.14.8).

The `lyse-gui` step now fails when lyse code issues a `DeprecationWarning` while results
add columns. Locally (Python 3.14.8, PySide6 6.12.0, pandas 3.1.0) every step passed with
lyse `pandas-new-columns` 061ce1f, and `lyse-gui` failed on master 3edf99c with the
warning from `filebox.py:570`. `test.yml` run
[40077643154](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40077643154)
(`lyse=labscript-suite/lyse@pandas-new-columns`): the 25 jobs for Python 3.11 to 3.14
passed every step; the six Python 3.15 jobs failed at install (h5py 3.16.0 does not
build). Run
[40077636478](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40077636478)
(push of the check, masters): `lyse-gui` failed with the warning in the 25 jobs for Python
3.11 to 3.14.

## 2026-10-24: D39, lyse's Edit columns dialog on PySide6 6.12.0, and D42

Locally (Linux), a script that updates lyse's `EditColumns` dialog with one more column
at a time crashed lyse master 3edf99c with labscript-utils master a9dbff7 after 15 to 31
updates in five runs (Python 3.14.8, PySide6 6.12.0), in `QStandardItemModel.clear()` →
`Shiboken::BindingManager::unregisterWrapper`. A PySide6-only script (300 rounds of
`clear()`, `setHorizontalHeaderLabels`, one `horizontalHeaderItem(0)` and up to 300
`appendRow` calls) crashed in three of three runs on PySide6 6.12.0 (Python 3.12 and
3.14) and in none on 6.8.3, 6.9.3, 6.10.2, 6.11.0 and 6.11.2 (Python 3.12), PyQt5 and PyQt6.
With labscript-utils `header-items-pyside612` 4964aa8 (DEFECTS.md D39), three 30 s runs
did 6,500 to 10,000 updates each without a crash, and 40 runs of the harness's 200-update
script on Python 3.14 passed. On Python 3.11.17 with PySide6 6.12.0 the 200-update script
aborts in every run with the fix (`none_dealloc: deallocating None`): every PySide6 call
that returns `None` lowers `sys.getrefcount(None)` by one (DEFECTS.md D42). On 6.11.2 it
does not.

The `lyse-gui` step now runs the 200 updates in a subprocess. Push run
[40063713700](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40063713700)
(masters): the check crashed in all five Ubuntu PySide6 jobs (KNOWN D39 on 3.12 to 3.14,
KNOWN D42 on 3.11) and passed on Windows and with PyQt5 and PyQt6; the Python 3.15 jobs
failed at install as before. Run
[40063716738](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40063716738)
(`labscript-utils=labscript-suite/labscript-utils@header-items-pyside612`): all 25 jobs
passed; the check passed in every job except Ubuntu, Python 3.11, PySide6 (KNOWN D42).
Run 40062621960, the same branch before the D42 marker, failed in that job only.

## 2026-10-24: runmanager run files built in memory (runmanager #147)

runmanager `copy-sequence-globals` changed from A (below) to build each run file in
memory from an in-memory file image holding the sequence globals, and to write it to disk
in one write without a zlock. Laptop, harness Python 3.14.8 venv, h5py 3.16.0 with HDF5
2.0.0, the `drop_mot` scan (8 groups, 174 sequence global attributes, 58 shot globals),
labscript master c8441c1 with B, run files made by `make_run_files` and compiled in a
batch compiler subprocess, 60 shots:

| runmanager | Make a run file (median) |
|---|---|
| master adc9777 | 8.6, 9.0 ms |
| A (a0ba68f) | 4.2, 4.3 ms |
| in memory (bc71818) | 2.1, 2.2 ms |

- The 100 run files of the scan and a `make_single_run_file` file have the same groups,
  attributes, attribute types and values as with master. Each file is 46.6 kB instead
  of 42.7 kB.
- Of the remaining 2.1 ms, about 1.6 ms is the 58 shot-global attribute writes; with
  low-level `h5a` calls instead of `attrs[name] = value` they take 1.3 ms.
- In labscript the per-shot file work is mostly shot-specific. With `generate_code`
  writing the shot file through an in-memory image (an experiment, not a branch), a
  compile took 15.4 ms instead of 16.0 to 16.6 ms. `load_globals` takes 3.3 ms,
  `save_labscripts` 1.8 ms (about 1 ms of it is the `sys.modules` scan) and
  `write_device_properties` 1.7 ms of the 15.4 ms.
- The test workflow passed on Ubuntu and Windows for Python 3.11 to 3.14 with every Qt
  binding (run 40069270747); the Python 3.15 jobs failed to install h5py, as before.
- labscript `set-passed-properties-bind` (labscript #132): the test workflow passed on
  Ubuntu and Windows for Python 3.11 to 3.14 with every Qt binding (run 40072696263);
  the Python 3.15 jobs failed to install h5py.

## 2026-10-24: drop_mot compile time on diginuc with the compile speed-ups

The 100-shot `drop_mot` scan as saved in diginuc's runmanager configuration, run on the
lab's hardware with BLACS, lyse and runmanager started on the lab's display and the scan
engaged through `runmanager.remote`. Python 3.14.8, h5py 3.16.0, NumPy 2.5.4, pyzmq
27.2.0, PyQt5 5.15.11; the integration-testing branches as deployed (blacs fa00b74,
runmanager 9e1807b, labscript-utils b8a5a49, zprocess ef150f8, lyse 5d13bdf,
labscript-devices bd41d67, labscript master c8441c1). Changed modules were put ahead of
the installed packages on `PYTHONPATH`, and the apps were restarted for each code
version; two sequences were run per start. Two of the lab's own GUI programs used about
1.4 of the machine's 4 logical CPUs throughout.

- A: runmanager `copy-sequence-globals` (sequence globals written once per sequence and
  copied into each run file; `patches/runmanager-copy-sequence-globals.patch`).
- B: labscript `set-passed-properties-bind` (`inspect.Signature.bind` instead of
  `getcallargs`; `patches/labscript-set-passed-properties-bind.patch`).
- E: blacs `ExperimentServer.process` run in the zmq request thread instead of the main
  thread, with `compare_to` called directly and the queue check and append done in one
  main-thread call. Not kept.

Time per shot is the time from the first to the last shot arriving at BLACS divided by
99. The handler time is from BLACS's `received filepath` log line to its `Request
handler` line.

| Code | lyse | Sequences | Time per shot | Handler (median) | runmanager CPU per shot |
|---|---|---|---|---|---|
| deployed | paused | 0009, 0010 | 109.3, 107.9 ms | 15, 14 ms | 67, 68 ms |
| A + B + E | paused | 0011, 0012 | 100.6, 95.7 ms | 22, 22 ms | 53, 53 ms |
| A + B | paused | 0013, 0014 | 95.7, 89.5 ms | 14, 14 ms | 54, 53 ms |
| deployed, with timers | analysing | 0015, 0016 | 146.5, 147.1 ms | 20, 20 ms | 71, 73 ms |
| A + B, with timers | analysing | 0017, 0018 | 121.4, 126.6 ms | 20, 21 ms | 55, 57 ms |

runmanager CPU is that of the runmanager process and its compile subprocess while the
sequence was being compiled. Phases from the timers (medians, the two sequences of each
row):

| Phase | deployed | A + B |
|---|---|---|
| runmanager: make the run file | 44.8, 44.9 ms | 24.5, 24.3 ms |
| compile subprocess: `labscript_init` | 13.9, 13.4 ms | 14.9, 14.9 ms |
| compile subprocess: run the script | 47.7, 42.8 ms | 44.3, 43.9 ms |
| compile round trip from runmanager | 67.6, 62.1 ms | 62.1, 63.4 ms |
| send to BLACS | 30.8, 29.1 ms | 29.5, 33.7 ms |

- lyse's state was not chosen. In sequences 0009 to 0014 the multishot routine
  `yellow_spectroscopy.py` failed on its first run (two shots) and lyse paused analysis
  for the rest of that start; in 0015 to 0018 it succeeded and lyse analysed every shot,
  using about 55 s of CPU per sequence instead of about 10 s. Rows are comparable only
  with the same lyse state.
- A shortens making a run file by about 20 ms on diginuc under load, and the time per
  shot by 13 to 25 ms. B's saving (1.3 ms on the laptop) is within the variation here.
- E made no shot faster: with E the handler time includes waiting for the main thread
  and was 22 ms instead of 14 ms, and the time per shot was 5 ms longer than with A + B
  alone. Moving the work to the request thread does not shorten the main thread's
  turnaround while the main thread is busy (plausible: the request thread also waits
  for the GIL).
- BLACS took 41 to 42 s (lyse paused) or 50 s (lyse analysing) from engage to sending
  the last shot to lyse, 0.41 to 0.50 s per shot, so compilation of every sequence
  finished 30 to 40 s before BLACS finished running it.
- The runs made sequences 2026/10/24/0009 to 0018 in the lab's shot storage.

## 2026-10-24: D9 rechecked on labscript-devices master

A shot with a `PrawnBlaster` with `use_wait_monitor=False`, a `DummyIntermediateDevice`
on its first clock line and one `wait()` between two digital output changes, compiled
in-process on Linux with Python 3.14.8, NumPy 2.5.4 and h5py 3.16.0. On labscript-devices
master 5a5892c the shot compiles and the pulse program has the two indefinite-wait rows
(`half_period` 4294967295, `reps` 0) between the instructions before and after the wait.
On 36ff62b, the parent of the fix a4a5f6b, `generate_code` raises `TypeError: string
indices must be integers` at `instruction["reps"]`. D9 stays fixed. The harness does not
compile a PrawnBlaster shot with a wait.

## 2026-10-24: per-shot compile time of drop_mot

The lab's `drop_mot` experiment and connection table, with copies of its `user_devices`
labscript classes and its 58 globals (taken from a shot of sequence 2026/10/24/0008),
compiled on the laptop (i7-1270P) with Python 3.14.8, h5py 3.16.0, NumPy 2.5.4, pyzmq
27.2.0 and PySide6 6.12.0: runmanager master adc9777, labscript c8441c1, labscript-utils
a9dbff7, labscript-devices `narwhal-pulsegen` 54e36ea. The labconfig had a shared secret
and no `allow_insecure`, as on diginuc, and `save_hg_info` and `save_git_info` off. The
runmanager GUI ran offscreen and compiled the saved 100-shot scan, sending each shot to a
stand-in for the BLACS request handler that parses the shot's connection table, compares
it to the lab's and checks for `/data`. Times are medians per shot over 100 shots; the
phases were timed by temporary timers in `compile_loop` and `batch_compiler.py`.

| Phase | master | both changes below |
|---|---|---|
| runmanager: make the run file | 15.9 ms | 8.2 ms |
| compile subprocess: `labscript_init` (reads the globals back) | 4.0 ms | 3.7 ms |
| compile subprocess: run the script | 14.6 ms | 13.5 ms |
| send to BLACS (stand-in handler 4 ms) | 5.2 ms | 4.5 ms |
| time between shots arriving at the stand-in BLACS | 41.4 ms | 31.8 ms |
| same, on 2 logical CPUs shared with 2 processes busy 70% of the time | 69.6 ms | 48.5 ms |

- Changes measured: runmanager's `_make_run_files` writes the sequence globals (174
  attributes in 24 groups) once per sequence to an in-memory HDF5 file and copies the
  groups into each run file, and labscript's `set_passed_properties` binds the call
  arguments with an `inspect.Signature` made once per decorated function instead of
  `inspect.getcallargs`. The run files' globals groups, attributes and attribute dtypes
  are identical to master's for all 100 shots, and 20 shots compiled with both labscript
  versions are identical in every dataset and attribute with a fixed hash seed. Without
  a fixed seed, the order of keys in the connection table `properties` JSON differs
  between processes on master too, because `set_passed_properties` collects the names in
  a set.
- With the CPUs shared, every phase takes longer in proportion to its CPU time; no phase
  is dominated by waiting for zlock or zmq. CPU time per shot on master: compile
  subprocess 17.7 ms, runmanager compile thread 15.5 ms, runmanager main thread 4.8 ms.
- On master, opening and closing an HDF5 file through `h5_lock` costs 0.5 to 1.2 ms more
  than without it (one zlock acquire and release); a shot is opened five times between
  runmanager and BLACS. Reading the 58 globals with `get_shot_globals` takes 1.5 ms of
  `load_globals`' 3.5 ms. `save_labscripts` takes 2 ms, of which 0.6 ms is
  `os.path.abspath` on each of the 948 modules in `sys.modules`. FunctionRunner's
  `serialise_function` takes 1 ms for two functions.
- On diginuc, sequence 0008 (100 shots, while BLACS and lyse were running) arrived at
  BLACS every 227 ms on average (124 to 349 ms), and BLACS's request handler took 28.5 ms
  (median). With diginuc idle, parsing the shot's connection table takes 1.9 ms,
  comparing it 0.1 ms and the check for `/data` 0.9 ms. The whole of
  `ExperimentServer.process` runs in the main thread (`@inmain_decorator` at
  `blacs/__main__.py:759`), and the logged handler time starts in the main thread, so the
  28.5 ms is main-thread time, not time spent waiting for the main thread (read; the
  section above has runs with the handler moved out of the main thread). runmanager waits
  for the reply before it compiles the next shot. zlock round trips on idle diginuc take
  0.47 ms, and attribute writes and reads take 92 and 24 µs, the same as on the laptop.

## 2026-10-24: integration-testing branches on diginuc

The `test-batch` branches on diginuc are replaced by `integration-testing` branches on
GitHub, made by `tools/integration-testing/build.sh` from master and these branches:
zprocess #35 and #39 (ef150f8), labscript-utils #138 (b8a5a49), labscript-devices
`narwhal-pulsegen`, #160 and #161 (bd41d67), blacs #135, #136 and #138 (fa00b74), lyse
#151, #153 and #157 (5d13bdf) and runmanager #144 and #145 (9e1807b). desktop-app,
labscript, qtutils and runviewer have nothing unmerged and stay on master.

- Conflicts: lyse `analysis_subprocess.py` (#157 with #153; #157's compile-on-change
  around #153's `routine_running` flag and `KeyboardInterrupt` handler), runmanager
  `group_manager.py` imports (#145 with #144) and zprocess `tests/test_zprocess.py` (#39
  with #35, the same resolution as `test-batch`, with an identical tree).
- runmanager #145's two history writes open the globals file with h5py directly, so
  without a change the history written at each compile makes the file grow by 4 kB, as
  before #144. The patch `value-history-repack.patch` makes them use
  `_open_for_writing`. With it, 400 calls of `record_history` on one global left the
  file at 18.5 kB, and it was repacked.
- Locally (Python 3.14.8), the zprocess test suite passes on the zprocess branch, 44
  tests, and blacs, lyse, runmanager, labscript-utils and labscript-devices import
  from the branches.
- `deploy.sh` checked out `integration-testing` or master in every clone in
  `diginuc:~/labscript-suite/dev`, and every component imports from its clone in the
  diginuc venv, including the Narwhal Devices and IMAQdx BLACS workers. The `test-batch`
  branches on diginuc are deleted.

## 2026-10-24: integration-testing branches on diginuc, second build

blacs #138 was rewritten after the first build and now imports `exit_if_port_in_use`
from labscript-utils #140, so #140 is added to `branches`, together with labscript #132,
labscript-devices #163 and runmanager #147. `build.sh` merged them without new conflicts
(the recorded lyse, runmanager and zprocess resolutions were reused, and
`value-history-repack.patch` still applies) and pushed blacs a4d09a6, labscript 613e712
(labscript's first integration-testing branch), labscript-devices a71fe95,
labscript-utils 7049a80 and runmanager fa47a6c; lyse 5d13bdf and zprocess ef150f8 are
unchanged. `deploy.sh` checked them out in `diginuc:~/labscript-suite/dev`, and in the
diginuc venv labscript, runmanager, blacs, `labscript_devices.usbserial` and
`labscript_utils.ls_zprocess` (with `exit_if_port_in_use`) import from the clones, as do
the Narwhal Devices and IMAQdx BLACS workers. No shot was compiled or run.

## 2026-10-24: `labscript_utils.ls_zprocess.port_in_use` (D40)

The 0.1 s connection timeout of the first version of the BLACS check (below) costs about
100 ms per start on Windows. A probe workflow on the workflow-sandbox fork (branch
`probe-ports`, run 40048838452) timed 200 calls each on a free port, a ZMQ REP port and
a plain listening socket, on windows-latest (Server 2025), windows-2022, macos-latest and
ubuntu-latest with Python 3.11 and 3.14. Every call gave the right result.

| Method | Windows free port | Windows ZMQ port | macOS and Ubuntu |
|---|---|---|---|
| connect with 0.1 s timeout | median 101–109 ms | median 15.5 ms | median under 0.1 ms |
| SYN retransmission off (`SIO_TCP_INITIAL_RTO`), 1 s timeout | median 15.4–15.6 ms | median 15.3–15.6 ms | median under 0.1 ms |
| SYN retransmission off, no timeout | median 0.04–0.11 ms, max 0.49 ms | median 0.08–0.18 ms, max 0.40 ms | median under 0.1 ms |

A socket timeout on Windows costs about 15.6 ms, the Windows timer interval, even when the
connection succeeds at once. A listener that does not accept connections and has a full
backlog: Windows refuses the connection at once (so `port_in_use` returns False);
Linux drops the SYN, and a connection attempt with a timeout times out (`port_in_use`
returns True after its 1 s timeout); macOS accepts it.
`port_in_use` in labscript-utils #140 uses no timeout on Windows and a 1 s timeout
elsewhere.

[Run 40049619223](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40049619223)
(labscript-utils `port-in-use` 0c71af0, blacs `submit-during-startup` 70091ce, lyse,
runmanager and runviewer `exit-if-port-in-use`; Ubuntu and Windows, Python 3.11–3.14,
three Qt bindings): all 25 jobs passed. In the `apps` step, `port_in_use` returned the
right result in every call: on Windows median 0.05–0.37 ms, maximum 0.65 ms; on Ubuntu
median 0.02–0.09 ms, maximum 0.27 ms. A second copy of each application reported its port
in use after 1–3 s with no traceback, and the second BLACS created no device tabs.

[Run 40052712233](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40052712233)
(the same changes with the functions moved to `labscript_utils.ls_zprocess`:
labscript-utils e62f2e5, blacs 21a7f56, lyse 1d6db44, runmanager bf33a4e, runviewer
5b04c61): all 25 jobs passed, with every `port_in_use` call right (maximum 1.02 ms on
Windows, 0.36 ms on Ubuntu) and every second copy reporting its port in use.

The masters push run 40049615503 for the same harness commit failed in one job, ubuntu
py3.14 PySide6: lyse aborted in the `lyse-gui` step with `malloc_consolidate(): unaligned
fastbin chunk detected` in `EditColumns.populate_model` (`lyse/filebox.py:111`), which is
D39. The Python 3.15 jobs failed as before.

## 2026-10-24: blacs #138 port check at start-up (D40)

blacs `submit-during-startup` 594723c checks for a process listening on the BLACS port
before it loads the connection table: a TCP connection attempt to `127.0.0.1` with a
0.1 s timeout. The harness step `blacs-shot` times 20 such attempts to the BLACS port of a
running BLACS and 20 to a free port, then starts a second BLACS.

- [Run 40047021693](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40047021693)
  (the branch; Ubuntu and Windows, Python 3.11–3.14, PySide6, PyQt6 and PyQt5): all 25
  jobs passed. Every attempt gave the correct result. The second BLACS logged the message
  after 1–2 s and created no device tabs.
- Time per attempt on Ubuntu: median 0.01–0.07 ms, maximum 0.16 ms, for both ports.
- Time per attempt on Windows: a free port takes the full timeout, median 101–104 ms,
  maximum 115 ms, because Windows retries a refused connection. The BLACS port of a running
  BLACS takes median 15–16 ms (0.2 ms in one job), maximum 25.5 ms. So the check adds
  about 0.1 s to every BLACS start on Windows.
- [Run 40047010897](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40047010897)
  (masters, push): the second BLACS failed with `zmq.error.ZMQError: Address already in
  use` (Windows: `Address in use`) and created no device tabs, as the experiment server
  is created first on master; reported as KNOWN D40.

## 2026-10-24: zprocess #40 (shared objects created under a lock)

Branch `instance-locks` on chrisjbillington/zprocess (head 61ab980, one commit on master
0fbd203).

- `SecureContext.instance()` for a new shared secret, called from eight threads released
  by a barrier at once, returned more than one context in five runs out of five on
  master and the same context in every run with the branch (Python 3.14.8, harness venv
  py3.14 with the branch first on the path). The zprocess test suite passed locally (78
  tests).
- `test.yml` run
  [40050076666](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40050076666)
  with `zprocess=chrisjbillington/zprocess@instance-locks` and every step: the 25 jobs
  for Python 3.11 to 3.14 passed every step, including `zprocess-tests`; the six Python
  3.15 jobs failed at "Install the components" because h5py 3.16.0 has no wheels for
  Python 3.15.

## 2026-10-24: lyse #158 (workers of both routine boxes started together)

Branch `concurrent-config-workers` on labscript-suite/lyse (head 0546d6f, one commit on
master 3edf99c), Python 3.14.8, PySide6, harness venv py3.14 with the branch, labscript-utils
master a9dbff7 and zprocess first on the path, offscreen, in the harness namespace.

- The lyse in diginuc's start of 11:07 (6a4f323) already had #139, but started its
  workers one after another: `load_configuration` called `add_routines` once per box, and
  each call started its first worker on its own. With one singleshot and two multishot
  routines no two workers started together.
- A configuration with two singleshot and two multishot routines (one disabled, one
  duplicate), loaded with `Lyse.load_configuration`:

  | lyse | zprocess | first load | second load |
  |---|---|---|---|
  | master 3edf99c | 8582358 (before #38) | 3.81 s, four workers in turn | 3.93 s |
  | branch, first worker alone on a new tree (earlier version of the commit) | 8582358 | 2.00 s | 1.23 s |
  | branch, first worker alone (earlier version) | master 0fbd203 | 2.04 s | 1.28 s |
  | branch 0546d6f, all workers together | master 0fbd203 (three runs) | 1.13 to 1.15 s | 1.24 to 1.28 s |
  | branch 0546d6f | 8582358 | 1.19 s | 1.49 s |

  In every run the rows and check states matched the configuration, the duplicate was
  reported, every worker was running 10 s after the load, a shot was analysed by the
  enabled singleshot routine and both multishot routines, a second load replaced the
  routines, and a worker that failed to start reached the excepthook while the others
  were added. With zprocess 8582358 the concurrent first starts can create more than one
  broker and heartbeat server; lyse does not use events, and the workers kept running.
- The harness `lyse-gui` step passed with the branch on both zprocess versions.
- `test.yml` run
  [40048985270](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40048985270)
  with `lyse=labscript-suite/lyse@concurrent-config-workers`: the 25 jobs for Python
  3.11 to 3.14 passed every step; the six Python 3.15 jobs failed at "Install the
  components" because h5py 3.16.0 has no wheels for Python 3.15, as on master.

## 2026-10-24: lyse start-up time on diginuc

lyse from `~/labscript-suite/dev` on diginuc (lyse 6a4f323, components installed from
git clones), Python 3.14.8, PyQt5, three analysis routines, load average 1.8 to 2.5.

- In `lyse.log` and `lyse.log.1` (16 starts on 23 and 24 October), lyse takes 4 to 11 s
  from its first log line until the last analysis worker is ready. Loading the UI, the
  routine boxes, the server and the configuration takes 0.03 to 0.25 s. The rest is the
  three workers, which are started one after another, each taking 1.2 to 4.6 s. Shots
  that arrive during this time are queued and not analysed until all workers are ready.
- Starting a worker through `ProcessTree.subprocess()` as lyse does took 1.17 to 1.49 s
  (four starts). The parent waits until the worker connects back, which the worker does
  after all of its module-level imports and `import pylab`, so the start time is
  almost all import time.
- Import time of `analysis_subprocess.py` (three runs, 1.29 to 1.62 s in total), by
  package: matplotlib 0.28 to 0.33 s, pandas 0.28 to 0.32 s (imported by `lyse/__init__.py`
  through `lyse.utils`), numpy 0.15 to 0.25 s, qtutils 0.05 to 0.08 s, and under 0.06 s
  for each other package.
- The `__version__` modules of labscript-utils, qtutils, desktop-app, lyse and zprocess
  call `setuptools_scm.get_version()` when the package is in a git clone. In the worker
  this imports setuptools_scm and runs 20 `git` commands: 0.29 s of a profiled start,
  0.16 s of it in labscript-utils. An install from a wheel reads the version from the
  package metadata instead and does not do this.

## 2026-10-24: `labscript_devices.usbserial` (labscript-devices #163)

Branch `usbserial` at 47aa493 on master 5a5892c.

- diginuc, the Narwhal pulse generator on `/dev/ttyUSB3` (FT2232H, second channel),
  `~/labscript-suite/dev/.venv` (Python 3.14.8, pyserial 3.5), with the module loaded
  from the branch: `latency_timer` was 16 before the first open and 1 after it. The first
  open took 260 ms including the echo request, the second 7 ms. A `get_state` request
  took 1.00 ms (median of 50; 0.36 to 1.51 ms) instead of 16 ms. A second exclusive open
  raised `SerialException`; closing the driver, which calls `cancel_read()` and joins
  its reader thread, took 5 to 7 ms. `tools/narwhal_hwtest.py` with `driver.open_port`
  using `usbserial.Serial`: 0 failures; waits with timeouts 0.3 s, 0.2 s and 0.1 s
  lasted 0.3021 s, 0.2015 s and 0.1020 s (17.5 ms over with `serial.Serial`), and the
  0.2 s plain shot finished 0.202 s after the trigger instead of 0.231 s.
  `tools/usbserial_check.py /dev/ttyUSB3` (no loopback): 0 failures; `cancel_read()`
  ended a blocking read after 2.0 ms. The port stays in low-latency mode until the
  device is unplugged or the driver is reloaded.
- Locally on a pseudo-terminal: reads with a timeout, with timeout 0, after a
  `cancel_read()` and `send_break()` behave as documented.
- Run [40054817217](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40054817217)
  with `labscript-devices=labscript-suite/labscript-devices@usbserial`: the 25 jobs for
  Python 3.11 to 3.14 passed; the six Python 3.15 jobs failed at "Install the
  components", as on the masters.
- Windows (the maintainer's VM, Python 3.12.7, pyserial 3.5, D2XX installed), FTDI
  TTL-232R-3V3 cable on COM3, `tools/usbserial_check.py COM3` without loopback: 0
  failures. pyserial reports the serial number `FTD421K0A`; D2XX lists the device as
  `FTD421K0` (type 5, id 0x04036001). `FT_OpenEx('FTD421K0A')` returns 2
  (FT_DEVICE_NOT_FOUND) and `FT_OpenEx('FTD421K0')` opens it, and
  `FT_GetComPortNumber` gives 3. The port opens through D2XX. A second open raises
  `SerialException` (D2XX: FT_DEVICE_NOT_OPENED; `serial.Serial`: access denied). A read
  with a 0.1 s timeout returns after 0.103 s; `cancel_read()` ends a blocking read after
  15.4 ms, against 2 ms on Linux. With TX connected to RX (`--loopback`), a second run:
  the same open results; `cancel_read()` took 9.7 ms; 5 bytes written are read back; 50
  single-byte round trips took 0.77 to 1.19 ms (median 1.00 ms) through D2XX and 8.13
  to 23.64 ms (median 15.99 ms) with `serial.Serial` on the virtual COM port.
- After this, c83cc6e removes the check that the D2XX handle has the requested COM port
  number: pyserial's serial number on Windows comes from the FTDI driver's device ID,
  which ends in the channel letter, and D2XX names the channels of a multi-channel
  device by the same letters, so the serial number cannot select another channel. The
  docstrings now give about 16 ms for `cancel_read()` and for the excess over a read
  timeout. The same changes were made to `pcp_serial.py` in portable-clocks-peripherals
  (uncommitted).
- Not run: the macOS D2XX path, a multi-channel FTDI device on Windows.
- Windows timing, same VM and cable, `tools/usbserial_timing.py` (300 samples each): one
  D2XX read with its 10 ms timeout and no data took 11.1 to 25.9 ms, median 15.98 ms
  (288 of 300 between 14 and 18 ms). `cancel_read()` to the return of the blocked read:
  0.05 to 60 ms, median 8.2 ms, 90% 15.2 ms, spread evenly up to 16 ms. A
  `read(1, timeout=0.05)` with no data ran 13.7 ms past its timeout (median), from 2.6 ms
  early to 63.5 ms late. `time.monotonic()`, which computes the deadline, has a
  resolution of 15.6 ms on Python 3.12 on Windows (`GetTickCount64`); `perf_counter()`
  has 0.1 us. A byte written while another thread was blocked in `read(1, timeout=1)`
  was not received within the timeout.
- `tools/usbserial_diag.py`: a write followed by a read in one thread: the write took 0.14
  to 0.27 ms and the read returned 0.5 to 0.8 ms later. With another thread blocked in
  `usbserial` `read(1, timeout=1)`, or calling the D2XX read with its 10 ms timeout in a
  loop, a write took 15 to 524 ms (roughly multiples of 16 ms) and the read returned 0.04
  to 1 ms after the write returned; 20 of 20 reads received the byte in both cases. The
  write is delayed while another thread reads, consistent with D2XX allowing one call on
  a handle at a time and the writer getting the handle only between two reads (not
  verified). The Narwhal driver writes from one thread while its reader thread reads.
- Run [40076336986](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40076336986)
  with `labscript-devices=pr/163` at c83cc6e: the 25 jobs for Python 3.11 to 3.14 passed;
  the six Python 3.15 jobs failed at "Install the components", as on the masters.

## 2026-10-24: Narwhal Devices Pulse Generator on hardware (labscript-devices #162)

diginuc, pulse generator serial number 12582921 (hardware version 5, firmware 1.002) on
`/dev/ttyUSB3`, `~/labscript-suite/dev/.venv` (Python 3.14.8) with labscript-devices
`integration-testing` bd41d67, which contains #162 at 54e36ea. BLACS was closed. The
maintainer has run the lab's `drop_mot` experiment with the device; no hardware trigger
source and no second unit are available. `tools/narwhal_hwtest.py`, with no channel in
use in any shot, so channels 2 and 7 stayed high and the others low throughout:

- `connect(12582921)` and `connect(None)` open the device. With the port held by
  another process, both raise after 5.1 s with messages that name `/dev/ttyUSB3` as
  "in use by another process".
- Manual mode: `program_manual` with the current values reads back the same values;
  each of the options run mode, accept hardware trigger, trigger-out length and delay,
  the two notify options, powerline trigger and powerline delay reads back as set;
  `disable_after_current_run` and `reset_run` on an idle device change nothing. The
  powerline is locked, mains period 19.99 ms.
- A 0.2 s shot finished 0.231 s after the software trigger.
- Waits that time out, timeout 0.3 s, recorded in `/data/waits` with `timed_out`:
  0.3176 s without `trigger_on_powerline`, 0.3299 s with it. In a shot with three waits
  the two timed-out waits (timeouts 0.2 s and 0.1 s) lasted 0.2173 s and 0.1176 s. The
  excess of 17.5 ms is the FTDI latency timer: `latency_timer` of the port is 16 ms, a
  `get_state` round trip takes 15.9 to 16.2 ms (20 requests), and the worker requests
  the state before the software trigger that resumes a timed-out wait. Every request
  to the device takes this long on this machine.
- `wait_for_powerline`: 13.3 ms with no delay and 18.6 ms with a 2 ms delay, both under
  one mains period plus the delay; in the three-wait shot 8.5 ms.
- An abort during a wait with a 5 s timeout: after 1 s the device is paused at the
  waiting instruction; `abort_buffered` leaves it stopped at address 0 with the outputs
  unchanged.
- A wait at t=0 with `use_wait_monitor=False`: after 1 s the device is paused at address
  0 with the outputs unchanged (there is no trigger to end the wait); `abort_buffered`
  stops it.
- The device's settings were restored afterwards; its instruction memory holds the last
  test shot (final address 2) instead of the lab's last shot.

Not tested: a wait ended by a hardware trigger, a wait of a few hundred nanoseconds
(`wait_delay = 0`), the trigger-out pulse on a scope, and a secondary pulse generator.

## 2026-10-24: Narwhal Devices Pulse Generator documentation (labscript-devices `narwhal-pulsegen` 54e36ea)

Branch `narwhal-pulsegen` at 54e36ea on master 5a5892c, Python 3.14.8, the py3.14 harness
venv with the branch first on the path.

- The five code blocks of `docs/source/devices/narwhalpulsegenerator.rst` were assembled
  into four scripts and compiled through `runmanager.compile_labscript_async`: the
  connection table and experiment, the same with a secondary pulse generator, a wait,
  and a powerline wait. Before the change to the page, the experiment failed to compile
  because the NI-USB-6363 had one analog output (`NI_DAQmx` requires an even number);
  the example now has two. The secondary, which has no direct outputs, then failed in
  `_compile_program` with `TypeError: 'int' object is not subscriptable`: the direct
  output states were the integer 0 when no output was connected. With the fix all four
  compile; the secondary's program is two instructions, lasting the stop time plus one
  cycle. The port listing block runs and prints nothing with no device connected.
- Harness step `narwhal` with the new fixture `no_direct_outputs.py`: 1 failure before
  the fix ("no_direct_outputs compile reported success"), 0 after. The step did not
  record a compile failure before this change, because `compile_fixture` did not check
  the result of the compile; it now does.
- Sphinx 8.2.3, dirhtml, from `docs/`: exits 0; the 12 warnings and errors are in other
  devices' pages and docstrings (NI_DAQmx, AlazarTechBoard, AD9959DDSSweeper,
  PrawnBlaster), none from the Narwhal page or modules.
- Run [40047034755](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/40047034755)
  with `labscript-devices=labscript-suite/labscript-devices@narwhal-pulsegen`: the 25 jobs
  for Python 3.11 to 3.14 passed every step; the six Python 3.15 jobs failed at "Install
  the components", as on the masters. labscript-devices #162 was opened after it.

## 2026-10-24: runmanager value history

runmanager branch `value-history` (2e41aa5) records the values of each global that are
used to compile shots and lists them in a drop-down on the value cell (`WISHLIST.md`).
`tools/value-history/drive.py` ran it under the offscreen platform with Fusion, on
Python 3.14.8 with PySide6 6.12.0, PyQt6 and PyQt5, with light and dark palettes, in a
namespace with a scratch profile. In each of the six runs the 26 checks passed: compiling
the runmanager test experiment through Engage records each value, comment included; a
value that fails to compile is not recorded; values that differ only in comments are one
entry; the list order, filtering, choosing with the keyboard, Ctrl+P, Delete, Escape,
Alt+Down in the table and in the editor, switching to the previous value and renaming a
global behave as intended. The first PyQt5 run showed no faded pin icons:
`QIcon.pixmap(16, QIcon.Disabled)` resolves to the `pixmap(width, height)` overload in
PyQt5 and gives a 16 by 1 pixmap; the branch passes a `QSize`. 2000 records of 50
globals in a test file did not change its size after the first few hundred, since the
history is written as fixed-length attributes (`DEFECTS.md` D37 is the growth that
variable-length strings cause).

The harness steps `versions` to `apps` passed locally with the branch installed (Python
3.14.8, PySide6). After the swap icon was changed to `arrow-circle-double` and screenshots were added to
the docs (head 48684a4), `test.yml` run
[39977851151](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39977851151)
passed the same 25 jobs; the Python 3.15 jobs failed at install as before. Earlier,
`test.yml` run
[39970622133](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39970622133)
with `runmanager=labscript-suite/runmanager@value-history`: the 25 jobs for Python 3.11
to 3.14 passed every step; the six Python 3.15 jobs failed at "Install the components",
as before.
## 2026-10-24: blacs #138 (D36, experiment server started last)

Locally (Python 3.14.8, PySide6, in a namespace with a scratch profile), with blacs
`submit-during-startup` (00587bb): the `blacs-shot` step submitted the first shot as soon
as the BLACS port accepted connections, and BLACS queued and ran it, in two runs out of
two; on master the same submission raised `NameError: name 'app' is not defined`. A shot
submitted 0.9 s after BLACS was launched, before the port accepted connections, waited
for the server and was queued when it started.

`test.yml` run
[39970164876](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39970164876)
with blacs `submit-during-startup`: the 25 jobs for Python 3.11 to 3.14 passed every step.
Run
[39970155698](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39970155698)
(push of the harness change, the masters): the 25 jobs for Python 3.11 to 3.14 passed,
with D36 reported as KNOWN by `blacs-shot`; the six Python 3.15 jobs failed at "Install
the components", as before.

## 2026-10-24: drop_mot on diginuc with the optimised pyzmq and h5py wheels

Sequences 2026/10/24/0004 to 0008 of drop_mot on diginuc, 100 shots each, Python 3.14.8,
with the wheels in `~/labscript-suite/dev/wheelhouse/`. lyse, runmanager and BLACS were
restarted between sequences; the zlock and zlog servers were restarted only before 0007.

- 0004: PyPI pyzmq 27.2.0 and h5py 3.16.0
- 0005: optimised h5py
- 0006: optimised h5py and pyzmq (zlock and zlog still on the PyPI wheels)
- 0007: as 0006 with zlock and zlog restarted; lyse paused after 3 shots on a fitting
  error, so it did no analysis for the rest of the sequence
- 0008: as 0007, with lyse analysing every shot

Mean BLACS cycle time (time between master pseudoclock starts) ± standard error, split at
the creation time of the last shot file, which is the time when runmanager finished
compiling:

| Sequence | while runmanager compiles | after compiling (63 to 71 cycles) |
|---|---|---|
| 0004 | 673 ± 10 ms | 567 ± 5 ms |
| 0005 | 678 ± 11 ms | 566 ± 5 ms |
| 0006 | 612 ± 10 ms | 537 ± 5 ms |
| 0007 (lyse idle) | 577 ± 9 ms | 445 ± 3 ms |
| 0008 | 647 ± 9 ms | 527 ± 5 ms |

The optimised h5py made no measurable difference to the cycle time. The optimised pyzmq
reduced it by 29 ± 7 ms, and restarting zlock and zlog on it by a further 10 ± 7 ms. The
largest change in the median BLACS worker job times from 0005 to 0006 is motcam
`transition_to_manual`, 81 → 64 ms. With lyse idle the cycle is 82 ms shorter than in
0008. runmanager's compile time per shot (from file creation times: 255, 221, 195, 172
and 226 ms) and lyse's per-shot times show no consistent trend.

## 2026-10-24: h5py Linux wheels build their extension modules without optimisation

h5py's `pyproject.toml` sets `CFLAGS = "-g1"` in `[tool.cibuildwheel.linux.environment]`
(added in h5py #2444, 2024). Since pypa/distutils #322 (December 2024), setuptools uses
`CFLAGS` from the environment in place of Python's `CFLAGS` instead of appending it, so
the Cython extension modules are compiled with no `-O` flag and without `-DNDEBUG`
(read). The compiler options recorded in the debug information of `h5d.*.so`:

- h5py 3.12.1 wheel: `-g -g1 -O3 -fno-strict-overflow -fPIC`
- h5py 3.13.0, 3.14.0, 3.15.1 and 3.16.0 wheels: `-g1 -fPIC`

The bundled libhdf5, libhdf5_hl, libaec and libsz come from h5py's Docker images and
are optimised: their code has no `-O0` frame-pointer pattern, which the extension
modules and the unoptimised pyzmq libsodium do have (run). The macOS build sets no
`CFLAGS` and builds HDF5 with CMake in Release mode; the Windows build uses MSVC (read).

Benchmark on the laptop (Python 3.14.8, median of 5): the PyPI 3.16.0 wheel (bundled
HDF5 2.0.0), and h5py 3.16.0 built from the sdist against Arch HDF5 2.2.0 with
`CFLAGS="-g1"` and with `CFLAGS="-g1 -DNDEBUG -fwrapv -O3"`. Times in µs.

| Operation | wheel | `-g1` | `-g1 -O3` | ratio |
|---|---|---|---|---|
| open and close a file | 48.6 | 50.6 | 29.8 | 1.70 |
| read 250 attributes into a dict | 5855 | 5988 | 3757 | 1.59 |
| read one attribute | 36.7 | 34.8 | 22.1 | 1.57 |
| read one row of a 1000×1000 dataset | 58.0 | 62.6 | 42.3 | 1.48 |
| read one element | 59.3 | 62.1 | 41.0 | 1.51 |
| read 100 small datasets in a group | 6135 | 6874 | 4449 | 1.55 |
| write 100 small datasets and 100 attributes | 9003 | 10525 | 7308 | 1.44 |
| read an 8 MB float dataset | 979 | 1003 | 937 | 1.07 |
| read 10000 rows of a compound with a vlen string | 1997 | 2939 | 2821 | 1.04 |
| read 10000 vlen strings | 1708 | 2670 | 2606 | 1.02 |

The `-g1` build matches the wheel apart from the vlen string reads, which depend on the
HDF5 version. Calls with little data take 1.4 to 1.7 times as long as with an optimised
build; bulk reads are not affected. No h5py issue reports this.

A fix, branch `optimise-linux-extensions` of chrisjbillington/h5py (one commit on h5py
master a372eab), sets `CFLAGS = "-g1 -O3 -DNDEBUG -fno-strict-overflow"`. The fork's
wheel workflow, run 40031561687, built every wheel except Windows ARM64, which fails in
HDF5's CMake configuration in the same way on master (fork run 40031544316 and the h5py
run at the same commit). The branch's Linux extension modules record `-O3` in their
compiler options. Mean size per wheel (7 wheels per platform) from the two fork runs,
and the uncompressed size of the extension modules:

| Platform | wheel, master | wheel, branch | change | extensions, master → branch |
|---|---|---|---|---|
| manylinux x86_64 | 5495 kB | 6114 kB | +9 to +18% | 10206 → 10893 kB |
| manylinux aarch64 | 5304 kB | 6006 kB | +11 to +21% | 15120 → 15975 kB |
| musllinux x86_64 | 5512 kB | 6068 kB | +8 to +17% | 10100 → 9649 kB |
| musllinux aarch64 | 5282 kB | 5938 kB | +10 to +20% | 11270 → 11021 kB |
| macOS arm64, macOS x86_64, Windows AMD64 | | | unchanged | |

On the laptop, h5py 3.16.0 built with `-O2` in place of `-O3` has the same benchmark
times (within 5%); its extension modules are 3.35 MB gzipped, compared with 3.62 MB for
`-O3` and 2.99 MB for `-g1` alone.

The branch was then changed to `-O2` (commit 55532179). Fork run 40037178550 built the
same wheels; the Linux extension modules record `-g1 -O2 -fno-strict-overflow`. Mean
size per wheel compared with master: manylinux x86_64 5495 → 5883 kB (+7%), manylinux
aarch64 5304 → 5780 kB (+9%), musllinux x86_64 5512 → 5843 kB (+6%), musllinux aarch64
5282 → 5717 kB (+8%); macOS and Windows unchanged. The first attempts of this run and of
the 3.16.0 run below failed in the wheel test step because pypi.anaconda.org returned
HTTP 503; the reruns passed.

Wheels for profiling on diginuc, in `~/labscript-suite/dev/wheelhouse/` (Python 3.14,
same tags as the PyPI wheels in `~/labscript-suite/dev/.venv`):

- `pyzmq-27.2.0-cp312-abi3-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl` from pyzmq
  fork run 39982600069. pyzmq main 1cbf63a has no changes under `zmq/` since v27.2.0.
- `h5py-3.16.0-cp314-cp314-manylinux_2_28_x86_64.whl` from h5py fork run 40037875841,
  built from the 3.16.0 tag with the `-O2` change (temporary branch, since deleted).

## 2026-10-24: pyzmq Linux wheels build libsodium without optimisation

The libsodium in the pyzmq Linux wheels is compiled without `-O`. pyzmq's cibuildwheel
configuration sets `CFLAGS="-Wl,-strip-all"` for Linux (`pyproject.toml`,
`[tool.cibuildwheel.linux.environment]`, since pyzmq 22.0.0, commit e29095d1 of
2021-01-28), and `tools/install_libzmq.sh` runs libsodium's `./configure` with it.
libsodium's `configure.ac` adds `-O3` only when `CFLAGS` is not set (read). The same
script builds libzmq with `CXXFLAGS="-Wl,-strip-all"`.

Throughput of `crypto_box_easy_afternm`, the cipher of CurveZMQ messages, on 6.2 MB,
called through ctypes, and the REQ/REP round trip of one 6.2 MB message on 127.0.0.1
(median):

| Machine | Library | Throughput | CURVE round trip | Plain round trip |
|---|---|---|---|---|
| laptop (i7-1270P, Arch) | pyzmq 27.2.0 wheel, bundled libsodium 1.0.22 | 161 MB/s | 76 ms | 2.6 ms |
| laptop | libsodium 1.0.22 built with `CFLAGS="-Wl,-strip-all"` | 164 MB/s | | |
| laptop | libsodium 1.0.22 built with default flags | 1896 MB/s | | |
| laptop | libsodium 1.0.22 built with `LDFLAGS="-Wl,-strip-all"` | 1955 MB/s | | |
| laptop | Arch libsodium 1.0.22, with pyzmq 27.2.0 built from source on Arch libzmq 4.3.5 | 1857 MB/s | 11.9 ms | 2.7 ms |
| diginuc (i3-1115G4, Ubuntu 22.04) | pyzmq 27.2.0 wheel (Python 3.14), bundled libsodium 1.0.22 | 72 MB/s | 174 ms | 2.7 ms |
| diginuc | pyzmq 25.1.0 wheel (Python 3.10), bundled libsodium 1.0.18 | 78 MB/s | 183 ms | 2.8 ms |
| diginuc | Ubuntu libsodium 1.0.18 | 1369 to 1673 MB/s | | |

- The build with `CFLAGS="-Wl,-strip-all"` reproduces the wheel's throughput and size
  (1.43 MB, wheel 1.35 MB; default flags 0.70 MB). With the strip flag in `LDFLAGS`
  instead, the library is fast and 0.63 MB.
- libzmq without optimisation changes plain zmq little: 21.8 µs per round trip of 100 B
  messages with the wheel and 19.0 µs with pyzmq built on the Arch libzmq.
- No pyzmq issue reports this; pyzmq #1491 (2021) about the wheel size led to the flag.
- Not measured: conda's pyzmq.

A fix, branch `libsodium-optimisation` of chrisjbillington/pyzmq (one commit on pyzmq
main 1cbf63a), passes `-O3` to libsodium's `configure` and `-O2` to libzmq's in
`tools/install_libzmq.sh`; the pull request is for the maintainer to post. The fork's
wheel workflow (run 39982600069) built every wheel except win_arm64, which fails in the
same way on pyzmq main at the same commit. Results for the PyPI 27.2.0 wheel and the
wheel built from the branch, with the same measurements as above:

| Machine | PyPI wheel | Branch wheel |
|---|---|---|
| laptop, Python 3.14 | 161 MB/s, CURVE 76 ms | 1908 MB/s, CURVE 11.9 ms |
| diginuc, Python 3.14 (temporary venv in `/tmp`, removed) | 72 MB/s, CURVE 174 ms | 2009 MB/s, CURVE 17.3 ms |
| GitHub `ubuntu-24.04`, Python 3.13 | 89 MB/s, CURVE 147 ms | 1503 MB/s, CURVE 13.9 ms |
| GitHub `macos-14` (arm64), Python 3.13, universal2 wheel | 58 MB/s, CURVE 288 ms | 351 MB/s, CURVE 46 ms |
| GitHub `windows-2022`, Python 3.13 | CURVE 24.5 ms (plain 5.4 ms); not affected | not changed by the branch |

Wheel and library sizes (2026-10-24), from the wheels of the fork run 39982600069 and of
upstream run 37984958991 on main 1cbf63a, which has the same set of wheels apart from
three macOS PyPy arm64 wheels that only the fork run built. Wheel sizes are the mean per
wheel; library sizes are uncompressed, from the cp310 wheel.

| Platform | wheels | wheel, main | wheel, branch | libsodium, main → branch | libzmq, main → branch |
|---|---|---|---|---|---|
| manylinux x86_64 | 9 | 887 kB | 785 kB (−11 to −13%) | 1482 → 650 kB | 940 → 675 kB |
| manylinux i686 | 9 | 983 kB | 878 kB (−10 to −12%) | 1792 → 850 kB | 909 → 769 kB |
| musllinux x86_64 | 6 | 1960 kB | 1856 kB (−5%) | 1482 → 650 kB | 963 → 695 kB |
| musllinux i686 | 6 | 2109 kB | 2027 kB (−4%) | 1682 → 789 kB | 905 → 731 kB |
| manylinux aarch64 | 9 | 681 kB | 707 kB (+4%) | 884 → 622 kB | 1124 → 859 kB |
| musllinux aarch64 | 6 | 1707 kB | 1732 kB (+1.5%) | 884 → 556 kB | 1123 → 793 kB |
| manylinux riscv64 | 1 | 742 kB | 768 kB (+3.6%) | 683 → 437 kB | 963 → 556 kB |
| macOS universal2 | 6 | 1469 kB | 1249 kB (−15%) | 1262 → 1038 kB | 3329 → 1314 kB |
| macOS x86_64 (PyPy) | 3 | 911 kB | 684 kB (−25%) | 1369 → 664 kB | 1621 → 639 kB |
| Android, Windows | 21 | | within 0.3% | not affected | not affected |

The libraries are smaller on every affected platform. The aarch64 and riscv64 wheels are
larger because the optimised libraries compress less well. Plain zmq round trips of 100 B messages on the laptop: 21.8
µs with the PyPI wheel, 18.7 µs with the branch wheel.

## 2026-10-24: labscript-devices `camera-image-ack` on diginuc

Sequences 0000 to 0003 of `drop_mot` on diginuc, 2026-10-24 01:29 to 01:38, 100 shots
each of the saved runmanager scan, with the `test-batch` branches of 2026-10-23 (blacs
`queue-main-thread`) on Python 3.14.8 and PyQt5. lyse ran its saved routines and
analysed every shot. labscript-devices was at `test-batch` without the branch (07f0045)
for 0000 and 0002 and with it (b2310d0) for 0001 and 0003; BLACS was restarted for each
sequence. Phase times from the BLACS log, shots 20 to 99; medians in ms, and the mean
cycle with its standard error.

| Seq | `ImageReceiver` | Cycle (mean) | Cycle | Run | To manual | To buffered | motcam `transition_to_manual` job | `_send_image_to_parent` (median, 10th to 90th percentile) |
|---|---|---|---|---|---|---|---|---|
| 0000 | master | 526 ± 6 | 513 | 306 | 92 | 107 | 68 | 22.3 (14.0 to 41.9) |
| 0001 | branch | 525 ± 5 | 518 | 304 | 93 | 102 | 60 | 19.4 (12.8 to 33.5) |
| 0002 | master | 523 ± 5 | 509 | 304 | 96 | 102 | 70 | 21.6 (12.8 to 40.4) |
| 0003 | branch | 528 ± 5 | 519 | 307 | 100 | 106 | 66 | 20.5 (12.9 to 31.1) |

- The branch shortens `_send_image_to_parent` by about 2 ms (median) and its 90th
  percentile by about 8 ms. The cycle and the transition to manual do not change
  measurably.
- The cycle was 0.07 s shorter than in sequence 0028 of 2026-10-23 with the same
  software, and `_send_image_to_parent` took 36 ms (median) then.
- A bare `labscript_utils.ls_zprocess.ZMQServer` that replies at once, on the
  maintainer's laptop, replies to a 0.23 MB image in 3.2 ms when images are sent
  back to back and in 11.4 ms when each is sent 0.5 s after the last. A plain zmq
  REQ/REP pair takes 0.1 and 1.5 ms, and the same pair with CurveZMQ 3.0 and 9.0 ms. So
  most of the remaining time on diginuc is the encryption of the image, which
  takes longer after an idle period, and not the wait for the main thread.

## 2026-10-24: camera image reply times and zprocess encryption on loopback

labscript-devices branch `camera-image-ack` (c3d8f5c, on master 5a5892c; reworded as 7a51c3a, labscript-devices #161) makes
`IMAQdxCamera.blacs_tabs.ImageReceiver` reply to the worker from the server thread
once the previous image has been displayed, instead of from the main thread. Locally,
Python 3.14.8, PySide6, offscreen, with the sender in a separate process and the
suite's encrypted sockets, 30 images of 2x224x260 uint16 (the size of the diginuc
`motcam` images), each 0.5 s after the last; medians, two runs of each:

| `ImageReceiver` | idle main thread | main thread blocked 50 ms of every 60 ms |
|---|---|---|
| master | 11.9, 11.3 ms | 57.4, 57.5 ms |
| `camera-image-ack` | 11.7, 11.4 ms | 11.2, 10.8 ms |

Continuous sending of 100x100 images reaches 1160 to 1280 frames/s with an idle main
thread and 19 frames/s with the blocked main thread, on both, so the display rate still
limits the sender. In sequence 0028 on diginuc, `_send_image_to_parent` in the
camera's `transition_to_manual` took 36 ms (median, 13 to 102 ms).

A REQ/REP round trip of one 6.2 MB message (2x1080x1440 uint16) on 127.0.0.1 takes
2.4 ms with plain zmq and 75 ms with a `labscript_utils.ls_zprocess.Context` socket,
which uses CurveZMQ when a shared secret is configured; for 0.23 MB it is 0.1 ms and
3.1 ms (libzmq 4.3.5, pyzmq 27.2.0).

## 2026-10-24: shots run through BLACS; labscript-devices #160 and blacs #137

The new harness step `blacs-shot` starts lyse and BLACS, submits a copy of the example
shot to BLACS as runmanager does, and checks that BLACS runs it with the dummy devices
and sends it to lyse, that the same file submitted again runs as a repeat in a new file,
and that neither application prints a traceback and BLACS.log has no errors. Before
this step, the harness only started BLACS for five seconds. Locally (Python 3.14.8,
PySide6, in a namespace with a scratch profile) the step passed in 11 s. Submitted as
soon as the BLACS port accepted connections, the first shot was refused with a
`NameError` (`DEFECTS.md` D36), so the step waits for BLACS to log that it has started.

`test.yml` run
[39964671583](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39964671583)
(push of the step, the masters): the 25 jobs for Python 3.11 to 3.14 passed every step,
including `blacs-shot`; the six Python 3.15 jobs failed at "Install the components", as
before.

`test.yml` run [39964678257](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39964678257) with labscript-devices `zprocess3-compat` (fa855e7, #160) and blacs
`remove-zprocess-locking-import` (251b8c6, #137): the 25 jobs for Python 3.11 to 3.14
passed every step, including `blacs-shot`. An earlier run,
[39962730807](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39962730807),
of the same branches without the step also passed. The NI DAQmx, PrawnBlaster and
CiceroOpalKellyXEM3001 workers are not run by the harness and have not been run with
hardware. For D24, the NI DAQmx module was imported locally with PyDAQmx replaced by
empty modules, and the wait monitor was run with a counter read that raises: on master
`stop_tasks` raised `TypeError: _reraise() takes 1 positional argument but 3 were
given`, and on #160 it raised the counter read's exception.

## 2026-10-24: growth of globals files (D37) and runmanager `repack-globals-files`

Locally, harness venv (Python 3.14.8, h5py 3.16.0, HDF5 2.0.0), runmanager master
adc9777:

- 2000 iterations of `set_value` and `set_expansion` on one global of a group of 20 grew
  the globals file from 128 kB to 16.5 MB, linearly, by 4096 bytes for each call.
  `h5repack` reduced the file to 18.6 kB.
- The growth is 4096 bytes for each open in which a variable-length string attribute is
  written, including a write of the value that the attribute already has. Opening and
  closing the file without writing adds nothing, and 1000 writes in one open grew a small
  file to 73 kB. Integer, boolean and fixed-length string attributes do not grow the file.
- Creating the file with `libver='latest'`, with `fs_strategy='fsm'` or `'page'` and
  `fs_persist=True`, or opening it with `meta_block_size=512`, makes no difference.

runmanager writes to globals files from two threads: the main thread when the user edits
a global and the preparse thread when `update_expansions` writes automatic expansion
settings (`runmanager/__main__.py:2938`). The remote server thread reads them. Every open
takes the zlock of the file through `labscript_utils.h5_lock`, which is a reentrant
readers-writer lock with one client per thread.

Branch `repack-globals-files`, same venv. The first version (500297b) held the write
zlock from each write until the repack check, so that every write acquired the zlock
twice: 2008 zlock acquisitions for 1000 writes, against 1000 on master, and 1.4 ms
instead of 1.0 ms per write. The second version (4c876e7) takes the zlock only to repack,
and checks the size again once it holds it; with it:

- 1000 writes made 1012 zlock acquisitions, the extra 12 for the four repacks.
- The same 2000 iterations: the file reached at most 1.06 MB and was repacked 15 times;
  the globals read back unchanged and no temporary files were left.
- Three threads writing 500 values each to one file: every final value was written.
- The 16.5 MB file from master was repacked to 15 kB on its first edit.
- A repack of a file with 500 globals takes 0.12 s, of which 0.10 s is reading the
  attributes of both files for the comparison (timed with 500297b; the repack itself
  is unchanged in 4c876e7).
- The `runmanager-api` step, in a scratch profile, passed with the new check printing
  `FIXED` (530 kB after 600 writes); on master the check is `KNOWN` at 2.6 MB.
- GitHub Actions run 39966730779 of 500297b was cancelled when 4c876e7 replaced it.
- GitHub Actions run [39967998841](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39967998841)
  of 4c876e7 (`runmanager=labscript-suite/runmanager@repack-globals-files`): the 24 jobs
  for Python 3.11 to 3.14 on Ubuntu and Windows with PySide6, PyQt6 and PyQt5 passed, with
  the new check printing `FIXED` at 530 kB on both platforms. The six Python 3.15 jobs
  failed to install, because h5py 3.16.0 has no wheels for Python 3.15. The pull request
  is [runmanager #144](https://github.com/labscript-suite/runmanager/pull/144).

## 2026-10-24: lyse #157 on diginuc

lyse at master 3edf99c and at the #157 branch head a00f06f, each run three times,
alternating, on diginuc (i3-1115G4, 4 cores, Python 3.14.8, PyQt5 5.15.11, Qt offscreen,
the `test-batch` versions of the other components). Each run started lyse with
`gaussian_fit` as the only routine, submitted the 100 shots of sequence 0029 (copies in
`/tmp`, removed afterwards) at once and waited for them to be analysed. BLACS was not
running; another program kept the load average at about 1.8. Medians over shots 5 to 99,
in ms, as the range over the three runs:

| | master, idle | #157, idle | master, 3 busy processes | #157, 3 busy processes |
|---|---|---|---|---|
| per shot | 126 to 129 | 102 to 104 | 229 to 233 | 187 to 203 |
| routine body | 67 to 69 | 72 to 73 | 131 to 134 | 131 to 143 |
| per shot minus routine body | 60 to 62 | 32 to 33 | 97 to 100 | 57 to 62 |
| routine sent to result received (`lyse.log`) | 78 to 79 | 79 to 81 | 149 to 158 | 147 to 162 |
| result received to next routine sent (`lyse.log`) | 50 to 52 | 23 to 25 | 76 to 82 | 38 to 43 |

100 shots took 14.1 to 14.7 s on master and 11.9 s on #157 when idle, and 25.6 to 25.9 s
and 21.4 to 22.2 s with three busy processes. The maintainer's measurement below, with
the lyse window on screen, had 117 ms and 87 ms for the last two rows.

## 2026-10-24: lyse #157 (per-shot time outside the routines)

lyse branch `shot-overhead`, four commits on master 3edf99c, measured as in the entry
below (100 shots of diginuc sequence 0029 submitted at once, the lab's `gaussian_fit`,
Python 3.14.8, PySide6, offscreen). Medians of three runs at each commit, in ms per shot;
"other" is the time per shot minus the routine body, which was 35 ms throughout:

| Commit | Change | Other, idle | Other, 16 busy processes on 16 cores |
|---|---|---|---|
| 3edf99c | master | 38.8 | 160, 192 |
| e839eb8 | `.at` for up to 20 rows (D35) | 27.7 | |
| 72f858f | `dataChanged`; no empty `update_rows` or repeated `set_status_percent` | 14.5 | 72, 79 |
| 79e7ed3 | two main-thread calls per routine instead of seven | 13.7 | 57, 58 |
| a00f06f | compile the routine only when its source changes | 12.4 | 58, 70 |

Compiling a routine takes 0.57 ms for `gaussian_fit` (127 lines) and 2.1 ms for
`yellow_spectroscopy` (532 lines) locally, 0.78 ms and 3.0 ms on diginuc; reading the
file takes 6 to 24 µs. On a 1000-row dataframe, setting 28 columns takes 0.29 ms with
`.at` and 7.7 ms with the per-column `.loc` for one row; for 100 rows, 29 ms and 9.3 ms.

The `lyse-gui` harness step now runs routines that save results (`harness/README.md`).
Locally it passed on master and on the branch, and with the branch merged with #153
(one conflict, in `analysis_subprocess.py`), where the Abort checks also passed. One
local run crashed in `EditColumns.populate_model` (`DEFECTS.md` D39). `test.yml` run
[39970007241](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39970007241)
(`lyse=labscript-suite/lyse@shot-overhead`): the 25 jobs for Python 3.11 to 3.14 passed
every step; the six Python 3.15 jobs failed at "Install the components", as on the
masters. In run
[39969987453](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39969987453)
(push of the new check, masters), the `lyse-gui` process on Ubuntu, Python 3.11, PySide6
ended with a segmentation fault while the second routine ran (D39); the job passed when
run again. Run
[39972898331](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39972898331)
(`lyse=pr/157`, with the harness waiting for the pause after the routine error): the 25
jobs for Python 3.11 to 3.14 passed every step; the six Python 3.15 jobs failed at
install.

## 2026-10-24: lyse per-shot time with the lab's single-shot routine

**On diginuc.** The maintainer loaded the 100 shots of sequence 0029 into lyse
(`test-batch` 6a4f323, PyQt5, pandas 3.1.0, NumPy 2.5.4, h5py 3.16.0, load average 3.6
on 4 cores, BLACS idle) with `gaussian_fit` as the only single-shot routine. Medians from
`lyse.log`, shots 5 to 99:

| Interval | Time |
|---|---|
| analysing one shot to analysing the next | 210 ms |
| routine sent to the worker to result received | 117 ms |
| routine finished to next shot started (`update_rows`, `set_status_percent`) | 87 ms |

The routine body, run in a plain process on the same files at the same time, takes
82 ms without `save_results_dict`: `analyse_image` for the two images 62 ms, `Run()` 6 ms
(two file opens), reading the images 6 ms; opening a shot file read-only takes 3 ms.
During sequence 0028 (BLACS running shots at 0.6 s), the routine took 256 ms, the time
after it 174 ms, and the multishot routine `yellow_spectroscopy`, about 1.0 s, ran 20
times in 100 shots.

**Locally** (Python 3.14.8, PySide6, offscreen, pandas 3.0.6), the same shots and routine
in lyse, labscript-utils, zprocess and qtutils copied from diginuc's `test-batch`, with
timing markers added to lyse and the routine, 100 shots submitted at once. Medians:

| Step | Time |
|---|---|
| per shot | 70 ms |
| routine body: `Run()` 3.1, read images 2.7, fits 22.5, `save_results_dict` 5.3 | 33.6 ms |
| worker: receive, start thread, call into Qt main thread, compile the routine; return result | 4.3 ms |
| routine box: status icons and `enabled()` checks, each a call into the main thread | 3.5 ms |
| `update_rows`: dataframe assignment (`DEFECTS.md` D35) | 10.9 ms |
| `update_rows`: Qt model items | 3.8 ms |
| waiting for the main thread after `layoutChanged` (`set_status_percent`, then `update_rows({})` and `set_status_percent` for `done`) | 12.6 ms |

The per-shot time is the same for rows 100 to 600 of a 600-shot run. With one shot
submitted every 0.15 s, a shot reaches the analysis thread 141 ms after submission:
100 ms is the wait in `incoming_buffer_loop` for more shots, 22 ms is
`get_dataframe_from_shot` in the incoming thread, 5 ms is `add_files` in the main thread
and 12 ms is the pass of the multishot routine box, which runs after every shot when the
queue is empty, even with no multishot routines. Assigning the same 28 results with
`.at` takes 0.27 ms, and with one `.loc[row, columns] = values` 2.7 ms, against 6.8 ms
for the current per-column `.loc` assignment.

## 2026-10-23: blacs #135 (`statemachine-main-thread`) and #136 (`queue-main-thread`)

`test.yml` runs
[39960991964](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39960991964)
(blacs at `statemachine-main-thread`, 4c0f058) and
[39961004193](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39961004193)
(blacs at `queue-main-thread`, 4fa3b05), the other components at their masters: in each,
the jobs for Python 3.11 to 3.14 passed every step, except the Ubuntu Python 3.14 PyQt5
job of the first run, which failed at "Clone the components" with a network error from
GitHub while fetching qtutils. The six Python 3.15 jobs failed at "Install the
components", as on the masters. The pull requests were opened after these runs.

## 2026-10-23: qtutils #41 and #38 rebased

#41 (`auto-scroll-after-show`, now f799f83) was rebased onto master 114a6ec, which
includes #39 and #40, and #38 (`qtlock-enforce-opt-in`, now 4d9b1b7) onto master
cf803f9, which includes #41. The only conflict in each was the 4.1.4 entries in
`CHANGELOG.txt`; all entries are kept, in merge order. Locally (Python 3.14.8), qtutils
imports from each rebased branch, and for #38 also with `QTUTILS_ENFORCE_QTLOCK=1`.

`test.yml` runs
[39954966629](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39954966629)
(`qtutils=pr/41`) and
[39956352577](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39956352577)
(`qtutils=pr/38`): in each, the 25 jobs for Python 3.11 to 3.14 passed every step; the
six Python 3.15 jobs failed at "Install the components", as on the masters. #41 was
merged after its run.

## 2026-10-23: test-batch branches on diginuc rebuilt on the current masters

After the merges of 2026-10-23, the `test-batch` branch of each clone in
`diginuc:~/labscript-suite/dev` was rebuilt on the component's master, with the pull
requests and branches of the previous batch that are not merged, at their current heads:
zprocess #35 and #39 (7af3a9d), desktop-app #35 (b6e255b), qtutils #38 and #41 (629f7d5),
labscript #130 (ac442c5), labscript-devices `narwhal-pulsegen` (07f0045), blacs
`statemachine-main-thread` and `queue-main-thread` (d834169) and lyse #151 and #153
(6a4f323). labscript-utils, runmanager and runviewer have nothing unmerged, so their
`test-batch` is master (a9dbff7, adc9777, b6bde5c). Conflicts: zprocess
`tests/test_zprocess.py` (#39 with #35; the imports of both are kept, with #39's default
tree set-up, and both new tests are kept) and qtutils `CHANGELOG.txt` (#38 and #41; both
entries are kept). The zprocess tests passed locally on the merged zprocess branch with
Python 3.14.8 (44 tests), and every component imports from its clone in the diginuc venv.

## 2026-10-23: blacs `statemachine-main-thread` and `queue-main-thread` rebased onto master c0c2322

`statemachine-main-thread` (now 98d55a1) was rebased onto master c0c2322, which includes
blacs #131 to #134. Its deferred state label and tab icon update is replaced by
master's, from #132. `queue-main-thread` (now 8794b42) was rebased onto it with its own
`blacs/experiment_queue.py`, and the port of #131's `QueueManager.stop()` was folded
into its commit. Locally (Python 3.14.8, PySide6, offscreen, labscript-utils master
9e05c17 or later), the queue checks in `tools/blacs-queue/` pass all 60 checks on
`queue-main-thread`, including those of `stop()`, and the state machine checks in
`tools/blacs-statemachine/` pass all 23 on `statemachine-main-thread`. With the
labscript-utils of the local harness venv, which is older than labscript-utils #136,
the worker processes fail on start-up, because blacs #133 calls
`labscript_utils.excepthook.install()` in them, and most queue checks fail.

## 2026-10-23: zprocess #38 rebased onto master 8582358

#38 (`appnope-once`, now c0ff0bf) was rebased onto master 8582358, which includes #34,
#36 and #37. The only conflict was the `zprocess.process_tree` import line in
`tests/test_zprocess.py`, which now imports both `ReadQueue` (from master) and
`ProcessTree` (from #38). Locally (Python 3.14.8), the zprocess test suite passes, 36
tests, including the new test of processes started concurrently.

`test.yml` run
[39952276822](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39952276822)
(`zprocess=pr/38`): the 25 jobs for Python 3.11 to 3.14 passed every step; the six
Python 3.15 jobs failed at "Install the components", as on the masters.

## 2026-10-23: labscript #131 (`load_globals` cleanup)

`test.yml` run
[39946972764](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39946972764)
with labscript at `load-globals-cleanup` (bb54fca) and the other components at their
masters: the 25 jobs for Python 3.11 to 3.14 passed every step, including the compile of
the example experiment through runmanager; the six Python 3.15 jobs failed at "Install
the components", as on the masters. Locally (Python 3.14.8), on a diginuc shot file with
None and bool globals added, `labscript_init` puts the same globals into builtins as
`get_shot_globals` returns, with the same types, `labscript_cleanup` removes them, and a
global named `stop` raises `LabscriptError`.

## 2026-10-23: time taken by `get_shot_globals`

Shot files of diginuc sequence 0029 (58 globals: 32 float, 9 int, 15 bool, 2 string),
with h5py 3.16.0, HDF5 2.0.0, NumPy 2.5.4 and Python 3.14.8, locally and on diginuc (load
average 1.7). Medians of repeated calls in a warm process.

| Step | Local | diginuc |
|---|---|---|
| `get_shot_globals(path)` | 1.5 ms | |
| `get_shot_globals(f)` with the file already open | 1.4 ms | 2.2 ms |
| opening and closing the file | 0.07 ms | 0.11 ms |
| `f['globals'].attrs[name]`, per attribute | 20 to 27 µs | 38 to 70 µs |
| the same attributes read through the HDF5 C library (`H5Aiterate2`, `H5Aopen`, `H5Aget_space`, `H5Aget_type`, `H5Aread`), per attribute | 1.1 µs | |

- Nearly all of the time is spent in h5py's `AttributeManager.__getitem__`. For each
  attribute it makes five calls into h5py's low-level API (`h5a.open`, `.shape`,
  `.dtype`, `h5t.py_create`, `read`), each of which takes 2 to 9 µs locally, mostly in
  creating and registering h5py object IDs. The conversions in `get_shot_globals` and
  the file open take under 5% of the total. The HDF5 library takes about 5%.
- Reading scalar numeric attributes through the low-level API with the memory type
  cached per dtype, and falling back to `attrs[name]` for other attributes, gives the
  same dict and takes 1.0 ms locally and 1.6 to 1.7 ms on diginuc, a saving of about
  0.5 ms per shot on diginuc.
- In sequence 0025 the FunctionRunner worker job took 76 ms (median), so reading the
  globals is about 3% of the job.

## 2026-10-23: runmanager #50 on master adc9777

With runmanager master adc9777 (#140 merged), Python 3.14.8: a globals file with
`a = [1, 2, 3]`, `b = array(a) * 2` and `c = [4, 5]`, all new and so automatic, gets `a`
and `b` in zip group `a` and `c` outer from the post-parse update that the GUI runs
(`RunManager.update_expansions`: `get_custom_expansions`, `automatic_expansions`, then
`set_expansion(..., custom=False)` for each global without a custom setting), reproduced
with the library functions. After `set_expansion` of `c` to `''` and of `b` to `outer`,
which record custom settings, two more runs of the update leave `c` unexpanded and `b`
outer, so the two cases of runmanager #50 persist across a reopen. Issue closed.

`test.yml` run
[39950460611](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39950460611),
on the push of the harness without the markers for runmanager #139, #140 and #143, lyse
#155 and labscript-devices #157, with every component at its master: the 25 jobs for
Python 3.11 to 3.14 passed every step; the six Python 3.15 jobs failed at "Install the
components", as before. The only `KNOWN` lines are for lyse #153 and the
`narwhal-pulsegen` branch.

## 2026-10-23: runmanager #139 and #140 rebased onto master 9770920

#139 (`topological-evaluator`, now 2d8129d) was rebased onto master 9770920, which
includes #141, #142 and #143; the only conflict was in `docs/source/usage.rst`, where
#143's paragraph on zip groups and other axes is kept before #139's paragraph on the
evaluation order. #140 (`expansion-settings`, now a658642) was rebased onto it without
conflicts. Locally (Python 3.14.8, PySide6), on the #140 branch: a two-global cycle holds
the cycle error, a conditional records both branches, a forward reference evaluates, and
#143's example (a global zipped with `duration` that refers to two globals in zip group
`clock`) holds the cross-axis error; `automatic_expansions` applied to the result and
evaluated again gives the same settings, with the error kept.

`test.yml` runs
[39947299743](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39947299743)
(`runmanager=pr/139`) and
[39947310296](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39947310296)
(`runmanager=pr/140`): in each, the 25 jobs for Python 3.11 to 3.14 passed every step; the
six Python 3.15 jobs failed at "Install the components", as on the masters. Both runs
report `FIXED` for the #139 checks and for the #143 check "zipped global referring to an
outer global holds an error"; the #140 run also reports `FIXED` for the #140 API presence
check and for the labscript-devices #157 check.

## 2026-10-23: labscript-devices #159 (FunctionRunner opens the shot file once)

`test.yml` run
[39944421762](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39944421762)
with labscript-devices at `function-runner-one-open` (db02f86) and the other components
at their masters, which include labscript-utils #139: the 25 jobs for Python 3.11 to
3.14 passed every step; the six Python 3.15 jobs failed at "Install the components", as
on the masters. The harness does not run the FunctionRunner worker. Locally (Python
3.14.8), `FunctionRunnerWorker.transition_to_buffered` on a diginuc shot file with a
start and a stop function opens the file once (twice before the change), and the
functions receive the same globals as `get_shot_globals` returns. An earlier run,
39943687032, failed at "Clone the components" on most jobs because labscript-utils #139
was merged and its branch deleted while the run was starting.

## 2026-10-23: labscript-utils #139 and lyse #156 (`get_shot_globals` with an open file)

`test.yml` run
[39939078038](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39939078038)
with labscript-utils at `shot-globals-open-file` (6ae6524), lyse at
`get-globals-open-file` (40370bd) and the other components at their masters: the 25 jobs
for Python 3.11 to 3.14 passed every step; the six Python 3.15 jobs failed at "Install
the components", as on the masters. Locally (Python 3.14.8), on a diginuc shot file with
None, bool, byte-string and array globals added, `get_shot_globals` returns the same
dict from the path and from an open file and leaves the file open, `Run.get_globals`
returns the same inside and outside `Run.open`, and the two `globals_diff` functions
return the changed globals.

## 2026-10-23: shot cycle time on the lab machine diginuc, by configuration

Sequences 0019 to 0029 of `drop_mot` on diginuc (4 cores, Linux), 100 shots each of
the same 50-point scan (shot duration 0.266 s, triggered on the mains line), run one
after another between 18:45 and 19:40 (0027 to 0029 between 21:00 and 21:18) with lyse running `gaussian_fit` and
`yellow_spectroscopy`. Phase times are from the BLACS debug log; mean of shots 20 to 99
(the first 20 shots of every sequence are 0.1 to 0.4 s slower). Standard error of each
cycle mean about 0.008 s. "New suite" is the test-batch branches on Python 3.14.8; "old
suite" is the labscript-suite 3.3.0 release on Python 3.10.12.

| Seq | Suite | BLACS state machine | Narwhal driver | Qt | Cycle (s) | To buffered | Start to run complete | To manual | Gap to next shot |
|---|---|---|---|---|---|---|---|---|---|
| 0023 | old | old | lab's `user_devices` | PyQt5 | 0.780 | 0.221 | 0.336 | 0.188 | 0.035 |
| 0022 | new | old | lab's `user_devices` | PyQt5 | 0.825 | 0.242 | 0.347 | 0.198 | 0.038 |
| 0020 | new | old | `labscript_devices.NarwhalPulseGenerator` | PyQt5 | 0.752 | 0.217 | 0.337 | 0.188 | 0.011 |
| 0019 | new | old | `labscript_devices.NarwhalPulseGenerator` | PySide6 | 0.865 | 0.256 | 0.350 | 0.242 | 0.018 |
| 0024 | new | `statemachine-main-thread` (52b0383) | lab's `user_devices` | PyQt5 | 0.702 | 0.189 | 0.327 | 0.172 | 0.014 |
| 0025 | new | `statemachine-main-thread` (52b0383) | `labscript_devices.NarwhalPulseGenerator` | PyQt5 | 0.686 | 0.199 | 0.323 | 0.151 | 0.013 |
| 0026 | new | `statemachine-main-thread` (52b0383) | `labscript_devices.NarwhalPulseGenerator` | PySide6 | 0.724 | 0.219 | 0.322 | 0.171 | 0.012 |
| 0027 | new | `queue-main-thread` (9cce66f) | `labscript_devices.NarwhalPulseGenerator` | PySide6 | 0.647 | 0.168 | 0.320 | 0.151 | 0.008 |
| 0028 | new | `queue-main-thread` (9cce66f) | `labscript_devices.NarwhalPulseGenerator` | PyQt5 | 0.600 | 0.155 | 0.312 | 0.128 | 0.005 |
| 0029 | new, logging disabled | `queue-main-thread` (9cce66f) | `labscript_devices.NarwhalPulseGenerator` | PyQt5 | 0.551 | | | | |

- PySide6 adds 0.113 s per shot with the old state machine, 0.038 s with
  `statemachine-main-thread` and 0.047 s with `queue-main-thread`, all of it in the two
  transitions.
- lyse ran `yellow_spectroscopy` after 0.16 (0027) and 0.22 (0028) of shots, against
  0.37 to 0.41 in 0024 to 0026, so lyse used less CPU time per shot in 0027 and 0028.
  The FunctionRunner still ends the transition to buffered and the camera the
  transition to manual in 0027 and 0028 (94% to 99% of shots).
- 0029 is 0028 with logging disabled in every component, so it has no phase times; its
  cycle time is from the `run time` attributes of the shot files, which give the same
  means as the BLACS log for 0025 to 0028. Disabling logging shortens the cycle by
  0.049 ± 0.009 s.
- FunctionRunner setup steps timed on diginuc in the Python 3.14 venv at a load average
  of about 1.5 (medians of repeated calls on shot 60 of 0029, in a warm process):
  `deserialise_function_table` for the two functions 0.64 ms (compile 0.35 and 0.21 ms,
  JSON arguments and `exec` under 0.01 ms; 1.5 ms on the first call); opening the shot
  file and reading `FUNCTION_TABLE` 2.1 ms; `get_shot_globals(path)` for 62 globals
  5.0 ms, of which reading the attributes from an open file is 2.6 ms; a zlock read
  lock acquire and release 0.85 ms.
- CPU load from other processes changes the cycle by more than any of these software
  changes: in sequence 0013 (old suite, 15:26 to 15:58) the cycle went from 0.98 s to
  0.67 s at shot 1600 with no change of software, and lyse's `gaussian_fit` from 0.41 s
  to 0.16 s at the same time. lyse ran `yellow_spectroscopy` after 0.57 to 0.70 of
  shots in 0020 and 0022 and after 0.37 to 0.43 in 0023 to 0026.
- In 0025 the transition to buffered ends when the FunctionRunner finishes (96% of
  shots): its worker job takes 76 ms (median), of which 38 ms is opening the shot file
  twice, reading the function table, deserialising the functions and reading the
  globals, and 18 ms is the lab's RPC call. The same file reads and deserialisation take
  about 10 ms in an idle process. The transition to manual ends when the camera
  (`motcam`) finishes (100% of shots), with a worker job of 84 ms.

## 2026-10-23: the BLACS shot queue in the main thread (blacs branch `queue-main-thread`)

`test.yml` run
[39935325016](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39935325016)
with blacs at `queue-main-thread` (9cce66f, on `statemachine-main-thread`) and the other
components at their masters: the 25 jobs for Python 3.11 to 3.14 (Ubuntu and Windows,
PySide6, PyQt6 and PyQt5) passed every step, including BLACS start-up in the `apps`
step. The harness does not run shots through BLACS. Locally (Python 3.14.8, PySide6,
offscreen), the queue checks in `tools/blacs-queue/` pass all 55 checks on the branch in
three runs; on `statemachine-main-thread` the two start-up latency checks fail (0.50 s,
from the 1 s poll) and the other 53 pass. The shot cycle measurements with and without
CPU load are in `BLACS-QUEUE.md` sections 3 and 6: with 8 dummy tabs the cycle goes
from 184 to 160 ms without load and from 316 to 251 ms with 16 busy processes.

## 2026-10-23: the BLACS state machine in the main thread (blacs branch `statemachine-main-thread`)

`test.yml` run
[39919928868](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39919928868)
with blacs at `statemachine-main-thread` (52b0383) and the other components at their
masters: the 25 jobs for Python 3.11 to 3.14 (Ubuntu and Windows, PySide6, PyQt6 and
PyQt5, plus the Ubuntu Python 3.14 PySide6 job with `numpy<2.5`) passed every step,
including BLACS start-up in the `apps` step. The six Python 3.15 jobs failed at "Install
the components", as on the masters. The behaviour checks in `tools/blacs-statemachine/`
(23 checks, Python 3.14.8, PySide6, offscreen, local) pass on the branch and on master,
and the shot cycle measurements with `tools/blacs-timing/` are in
`BLACS-STATE-MACHINE.md` section 6: with 8 dummy tabs the cycle goes from 0.24 s to
0.19 s.

## 2026-10-23: the Narwhal Devices Pulse Generator device (labscript-devices branch `narwhal-pulsegen`)

Branch `narwhal-pulsegen` on labscript-suite/labscript-devices, commit bf5cbc5 on master
33e20e7 (`NARWHAL-PULSEGEN.md`). The harness step `narwhal` was added for it
(`harness/README.md`): it compiles two fixture shots, checks the instruction tables, runs
the runviewer parser and runs the BLACS worker class on a simulated device that executes
the instructions in real time.

**Local** (harness venv, Python 3.14.8, PySide6 6.12, in a namespace with a scratch
profile, the branch on `PYTHONPATH`): the `narwhal` step passes its 51 checks in 7 s. The
master program of the fixture shot is 28 instructions and lasts the stop time plus the
final 1 us clock tick; the ramp with a 101-cycle period is 100 ticks of 50 + 51 cycles;
the wait after the second ramp is on a copy of the loop before it, so the device pauses
once; `powerline_sync` is set on the instruction after the `wait_for_powerline` wait. The
worker on the simulated device measured the wait ended by a trigger after 20 ms as
20.5 ms, resumed the wait with a 50 ms timeout after 50.7 ms and recorded it as timed
out, measured the powerline wait as 10.3 ms, wrote `/data/waits`, returned the final
values with the unused channels at their front panel values, aborted a run, and reported
"pulsegen2 is at instruction 0 of 6 and is not running. It may not have received its
trigger." for a secondary that was never triggered. The shot that begins with a wait
compiles to a one-cycle waiting instruction that holds the front panel state, and runs.
The `imports`, `compile`, `runviewer` and `apps` steps pass with the branch on the path,
so every module of the package imports without a deprecation warning and BLACS starts
with the device registered. The tab's control panel builds under PySide6 offscreen and
displays a device state.

**GitHub Actions:** dispatch of `test.yml` with
`labscript-devices=labscript-suite/labscript-devices@narwhal-pulsegen`, run
[39918371155](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39918371155):
24 of the 25 jobs for Python 3.11 to 3.14 passed every step. The Windows job for Python
3.12 with PyQt6 failed the `narwhal` step: the simulated device timed its run with
`time.monotonic()`, which has a resolution of 15.6 ms on Windows before Python 3.13, so
one measured wait was 15.5 ms instead of at least 20 ms and the powerline wait was
-1.0 ms. The simulator now uses `time.perf_counter()`, and the bound on the wait that
times out, which the worker times with `time.monotonic()`, allows 16 ms. Run
[39919806120](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39919806120)
with the same refs: the 25 jobs for Python 3.11 to 3.14 passed every step (on the
Windows Python 3.12 PyQt6 job the three waits measured 22.5 ms, 61.2 ms and 10.7 ms). In
both runs the six Python 3.15 jobs failed at "Install the components" on the h5py build,
as on the masters.

The device has not been run against hardware from this branch; that is a task in
`LOCAL-TASKS.md`. No pull request is opened until it has.

## 2026-10-23: labscript-devices #158 and blacs #134 (`clicked` argument, DEFECTS.md D30 to D33)

labscript-devices #158 at 422f2a3 and blacs #134 at 9fa23e7, both on master (b6ea556 and
cac5198).

- Locally with Python 3.14.8 and PySide6 6.12, and Python 3.13 and PyQt5: before the
  fixes, Snap and the example tab's `bar` and `baz_unpickleable` raised `TypeError` under
  PySide6, and the three QuickSyn handlers raised `TypeError` under PyQt5. After them none
  raised with either binding. The Garbage collect menu item collected generation 0 under
  PyQt5 before and generation 2 after.
- Run [39914034278](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39914034278) with both branches: every step passed in all 25 jobs on Ubuntu and Windows
  for Python 3.11 to 3.14 (the six Python 3.15 jobs fail at install as always).

## 2026-10-23: the 34 mergeable pull requests merged together

The 34 pull requests listed as mergeable now in `PULL-REQUESTS.md` were merged, in
pull request order, into a `test-batch` branch of each component on its master: zprocess
#33 to #39 (c02be91), desktop-app #35 (2842896), qtutils #38 to #41 (3649974),
labscript-utils #136 and #137 (a419aa3), labscript #130 (33c06f3), labscript-devices #156
and #157 (011b129), blacs #131 to #133 (071b76e), runmanager #139 to #143 (77714e6),
runviewer #78 and #79 (2cbe04a) and lyse #148 to #154 (b8f05c0). Conflicts: zprocess
`tests/test_zprocess.py` (#38 with #34 on an import line; #39 with the tests added by
the other pull requests, where #39's test changes were applied by hand), qtutils
`CHANGELOG.txt` (#38, #39 and #41 add entries at the same place; all kept) and
runmanager `docs/source/usage.rst` (#143 with #139; #143's paragraph is placed before
#139's description of the evaluator). runmanager `evaluator.py` merged without conflict,
and #143's check works on the #139 evaluator.

Locally on Arch Linux with Python 3.14.8 and PySide6, every harness step passed,
including the zprocess tests (85 tests). The checks for runmanager #139, #140 and #143,
lyse #153 and labscript-devices #157 reported FIXED. The branches are checked out in the
clones on the maintainer's lab machine, in a Python 3.14 venv with editable installs,
for testing with the lab's hardware and files.

## 2026-10-23: lyse #155 (skip shot files that have not been run, DEFECTS.md D29)

lyse #155 at af6977d, on master c74fa4e. The harness `compile` step now stamps the
example shot with a `run time` attribute, as BLACS does after running a shot, and the
`lyse-gui` step adds a copy of the example shot with a run time and a copy without one,
with analysis paused.

- Locally with Python 3.14.8 and PySide6: with #155 the first copy is loaded and the
  second is not, with the warning in the output box (FIXED); with lyse master both are
  loaded (KNOWN).
- Run [39906724789](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39906724789),
  before the shots were loaded with analysis paused: the check passed in all 25 jobs, but
  on Ubuntu with Python 3.11 and PyQt5 the `lyse-gui` process ended with a segmentation
  fault (exit code -11) after its checks, while the analysis threads were still running.
- Run [39907891995](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39907891995)
  with `lyse=labscript-suite/lyse@skip-unrun-shots`: every step passed in all 25 jobs,
  FIXED in each (the six Python 3.15 jobs fail at install as always).
- Run [39907895199](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39907895199)
  with `lyse=abort-analysis zprocess=pr/34`: every step passed in all 25 jobs; the check
  is KNOWN and the Abort checks pass after the shots are removed.
- On the lab machine (lyse 3.3.0 backport, Python 3.10, pandas 2.3.3), the same change
  was applied to the installed lyse. Of the shot files of the running sequence, the one
  that BLACS had not yet run has no run time and is skipped, and the others are not.

## 2026-10-23: globals files written by runmanager #140, read by runmanager 3.3.0

Locally (harness venv, Python 3.14.8). The library of the #140 branch (db18f83) wrote a
globals file with four globals: an array `a`, `b = 2*a` zipped with it automatically, a
list `c` with a custom `outer` setting and a scalar `d`. The group has the subgroups
`units`, `expansion` and `expansion_custom`, and the `expansion` attributes hold the same
values (`''`, `outer` or a zip group name) that 3.3.0 writes. runmanager 3.3.0 read the
file, evaluated and expanded it to 6 shots with `a` and `b` zipped and `c` outer, and
ignored `expansion_custom`. Edits made with 3.3.0 do not update `expansion_custom`: after
a rename of `b` to `bb`, the flag stayed under `b` and `bb` had none, and a changed
expansion setting kept the flag that it had before. The #140 GUI gives a global without a
flag a custom setting if its stored setting differs from the automatic one, and replaces
the stored setting of a global flagged as automatic with the automatic setting. runmanager
master (7e692f4) writes the same file structure as 3.3.0.

## 2026-10-23: evaluation of zipped globals that depend on other axes (DEFECTS.md D27, D28)

A colleague's globals file, with `yellow_pulse_time` derived from
`total_yellow_pulse_duration` and from `yellow_pulse_1` and `yellow_pulse_2` in another
zip group, evaluated and expanded with the library (harness venv, Python 3.14.8) on
runmanager 3.3.0, master 7e692f4 and the #139 (2101a63) and #140 (db18f83) branches: no
errors, 100 shots, and `yellow_pulse_time` half the duration in every shot on all four
(D28). On 3.3.0 and master, `PYTHONHASHSEED` 1 and 3 iterated the `clock` zip group
fastest and 2 and 4 the durations (D27). The same scan written as four globals in one zip
group with `np.tile`, `np.repeat` and `np.where` gave the intended pulse times on 3.3.0.

runmanager #143 (b283c3a, on master 7e692f4): the colleague's file gives the
`ValueError` on `yellow_pulse_time` only. A global derived from an `outer` global or
another zip group, and one that depends on another axis through a global with no
expansion, hold the error; a chain of derived globals in one zip group, an `outer` copy
of an `outer` global and a scalar computed from the lengths of two `outer` lists evaluate
as before; `raise_exceptions=True` raises the error. The evaluator change applied to the
#139 branch gives the same results.

**GitHub Actions:** run
[39904642902](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39904642902)
of `test.yml` with `runmanager=labscript-suite/runmanager@zip-cross-axis-check` passed
every step in all 25 jobs, with the new `runmanager-api` case reported as FIXED (the six
Python 3.15 jobs fail at install as always). The push run
[39904626431](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39904626431)
on the masters passed, with the case reported as KNOWN.

## 2026-10-23: lyse #150 with the removal of defunct model columns (DEFECTS.md D25)

lyse #150 at 79f9db9, on master c74fa4e. A script that drives `DataFrameModel` directly
adds shots, saves results that include a dict result, hides a column, removes all shots
and adds new shots. At 5142bbb, `update_row` raised `KeyError` with the name of a result
column, as on the lab machine; at 79f9db9 the Qt model no longer had the columns that are
not in the new dataframe, and a hidden column that a later result added again was
hidden. This was run with pandas 3.0.6 on Python 3.14 and, with the same change on the
lyse 3.3.0 backport, with pandas 2.3.3 on Python 3.10.

**GitHub Actions:** run
[39897307988](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39897307988)
of `test.yml` with `lyse=pr/150` passed every step in all 25 jobs (the six Python 3.15
jobs fail at install as always: no h5py wheel and no HDF5 to build one).

## 2026-10-23: the legacy `Camera` device and `camera_server`

Locally on Arch Linux with Python 3.14.8 in the harness venv (zprocess `pair-sockets`
71fe1dd, labscript-utils master c1aa2a3, labscript master 33cdb31, labscript-devices
master b6ea556). A connection table with a `DummyPseudoclock`, a `Trigger` and a
`labscript_devices.Camera.Camera` with two exposures compiled, and the shot file has the
`EXPOSURES` table. A `labscript_utils.camera_server.CameraServer` was started on
localhost, and the methods of `labscript_devices.Camera.CameraWorker` with "use zmq" set
were called directly, without BLACS: the connectivity check, `transition_to_buffered`
with the shot file, `transition_to_manual` and `abort` all returned success. The BLACS
tab and the `imaqdx_server.py` subclass, which needs NI-IMAQdx, were not run. The device
is therefore usable with current code (`RELEASE-PLAN.md` 4.8, Z4 and Z5).

## 2026-10-23: lyse fixes backported to lyse 3.3.0 on Python 3.10

The maintainer's lab machine runs lyse 3.3.0, which has the tree of master 92be8de, with
the local `os.nice(10)` edit and a local edit that reads the `data` group attributes. It
runs Python 3.10.12 with PyQt5 5.15.9, labscript-utils 3.4.1, zprocess 2.26.1, qtutils
4.0.0, pandas 2.3.3, NumPy 2.2.6 and h5py 3.15.1. lyse master requires Python 3.11, so
the fixes were cherry-picked onto v3.3.0 instead of installing master:

- 6066df4 and 001df5f (lyse #132), in place of the local `data` group edit;
- 8a6a5d5 (#144), 9cff0f3, 0b010a9 and 455f19b (#145), 3723c9b and 00a26a1 (#146), and
  the fourteen commits of #147;
- the open pull requests #149 (03e3c95), #150 (5142bbb), #151 (6c8312d) and #152 (ed71cc7,
  0bb3acd).

The Qt6 commits, the packaging commits and the open pull requests #148 (needs
labscript-utils #136), #153 (needs zprocess #34 and #35) and #154 (PyQt6 only) were left
out. Only 455f19b and 74f1968 conflicted, on start-up logging lines and a
`Qt.CheckState()` wrapper that 3.3.0 does not have; the resolution takes the incoming
code without those lines.

Locally on Arch Linux, in a Python 3.10.22 venv with the lab machine's versions of the
suite and its dependencies and the offscreen Qt platform:

- The harness `lyse` step passed, lyse and its submodules imported, and lyse started
  and listened on its port in the `apps` step with no traceback. The other failures were
  in the unchanged components (labscript 3.4.0 imports fail with `-W
  error::DeprecationWarning`, runmanager 3.3.0 has no `runmanager.widgets`, BLACS 3.2.3
  raises `KeyError: 'window_xpos'` in `restore_window` on a new profile).
- A script ran the lyse GUI in its process with three single-shot routines and a
  multishot routine that saves three results to every shot, on 500 copies of the example
  shot, then removed 490 shots. Two interleaved runs each:

  | | 3.3.0 with local edits | backport |
  |---|---|---|
  | start the four workers | 3.6 s | 2.7 s |
  | single-shot analysis of 500 shots | 34.6 s | 35.0 to 35.5 s |
  | end of single-shot analysis to multishot results in the dataframe | 5.1 to 5.2 s | 2.6 to 3.0 s |
  | remove 490 of 500 shots (about 20 columns) | 0.03 s | 0.01 s |

  The multishot time includes the routine opening the 500 shot files.
- Restarting a routine while it ran hung the GUI with both versions: the main thread
  blocked in `Interruptor.subscribe` under `check_child_exited` (DEFECTS.md D14). With
  the one-line change of zprocess #34 applied to zprocess 2.26.1 as well, the worker
  exited on SIGTERM (return code -15) and the routine restarted 2.9 s after `restart()`.

## 2026-10-23: zprocess #38, zprocess #39 and labscript-utils #138

zprocess #38 (4bece28, on master 1de4c26) creates a `ProcessTree`'s broker and heartbeat
server under a lock and calls `appnope.nope()` in `ProcessTree.__init__` (DEFECTS.md
D22). zprocess #39 (ea186ba, on master 1de4c26) creates no default `ProcessTree` on
import and adds `set_default_process_tree()`. labscript-utils #138 (f9afe16, on master
c1aa2a3) calls `set_default_process_tree()`.

Locally on Arch Linux with Python 3.14.8, with eight threads each starting a child from
one new `ProcessTree` at once, ten trials of master created 4 to 8 event brokers and 4 to
7 heartbeat servers per tree; with #38 every trial created one of each. The new test
`EventTests.test_events_from_processes_started_concurrently` failed with `TimeoutError`
in 3 of 3 runs on master and passed with #38. The zprocess suite passed on each branch
(74 tests).

- Run 39844040672 (zprocess #38, Ubuntu and Windows, Python 3.11 to 3.14 with PySide6,
  PyQt6 and PyQt5, and the `numpy<2.5` job, with the zprocess tests): all 25 jobs passed
  every step.
- Run 39844046729 (macOS, the throwaway branch `test/appnope-once-macos`: zprocess #36,
  #37 and #38, same matrix): all 12 macOS jobs passed every step, the first macOS run of
  the full matrix with no failure. No appnope traceback appeared.
- Run 39852927929 (zprocess #39 with labscript-utils master, which assigns
  `_default_process_tree` directly, Ubuntu and Windows): all 25 jobs passed every step.
- Run 39852934051 (zprocess #39 with labscript-utils #138, Ubuntu and Windows): all 25
  jobs passed every step.
- Run 39853002957 (macOS, the throwaway branch `test/v3-macos`: zprocess #36, #37, #38
  and #39, with labscript-utils #138): all 12 macOS jobs passed every step.

The Python 3.15 jobs failed at install as always. Both throwaway branches have been
deleted.

## 2026-10-23: zprocess #37 and labscript-utils #137 (DEFECTS.md D21)

zprocess #37 (366f8f3, on master 1de4c26) replaces the branch `start-daemon-single-fork`
of the section below: on Unix `start_daemon` runs a fresh Python process that starts
the command with `start_new_session=True`, with no thread. labscript-utils #137 (081c736,
on master c1aa2a3) starts the zlog and zlock `--daemon` scripts with `subprocess.run`.
Locally on Arch Linux with Python 3.14.8 the zprocess test file passed (34 tests), a
daemon that exits before its caller is not left as a zombie child of the caller, and a
command that does not exist raises `CalledProcessError`.

- Run 39793122431 (zprocess #37, Ubuntu and Windows, Python 3.11 to 3.14 with PySide6,
  PyQt6 and PyQt5, and the `numpy<2.5` job, with the zprocess tests): all 25 jobs passed
  every step. The Python 3.15 jobs failed at install as always.
- Run 39793127711 (macOS, the throwaway branch `test/start-daemon-macos`, 6143e79, which
  is zprocess #36 with the #37 commit on top, same matrix): `StartDaemonTests` passed in
  all twelve jobs and every application started on Python 3.11 to 3.14 with all three
  bindings. Python 3.12 with PySide6 failed the `apps` step on the appnope race (D22).
- Run 39793274699 (labscript-utils #137, Ubuntu and Windows, same matrix): all 25 jobs
  passed every step.
- Run 39793279995 (macOS, labscript-utils #137 with zprocess #36, which has the old
  `start_daemon`, PySide6, Python 3.11 to 3.14): every application started and connected
  to zlog on every version, including 3.12 and 3.13. Python 3.13 failed the `apps` step
  on the appnope race (D22).

The throwaway branches `test/start-daemon-macos` and `test/start-daemon-macos-control`
have been deleted.

## 2026-10-22: zprocess branch `start-daemon-single-fork` (DEFECTS.md D21)

The branch (f1ed197, on zprocess master 1de4c26) starts daemons with one `Popen` call
with `start_new_session=True` and adds `StartDaemonTests`, which starts a daemon from a
process that has imported tkinter. Locally on Arch Linux with Python 3.14.8 the zprocess
suite passed (74 tests).

- Run 39772349063 (the branch, Ubuntu and Windows, Python 3.11 to 3.14 with PySide6,
  PyQt6 and PyQt5, and the `numpy<2.5` job, with the zprocess tests): all 25 jobs passed
  every step. The Python 3.15 jobs failed at install as always.
- Run 39772363140 (macOS, the throwaway branch `test/start-daemon-macos`, which is the
  D19 fix of zprocess #36 with this commit on top, same matrix): every application step
  passed on Python 3.11 to 3.14 with all three bindings, including 3.12 and 3.13, which
  failed before for D21, and `StartDaemonTests` passed in all twelve jobs. Three jobs
  failed for other reasons: Python 3.11 with PyQt5 failed the `apps` step on a race in
  appnope (D22), and Python 3.11 with PySide6 and Python 3.13 with PyQt6 failed one
  heartbeat timing test each (D23).
- Run 39772376767 (macOS, control: the throwaway branch `test/start-daemon-macos-control`,
  which has the new test and the old `start_daemon`, PySide6): on Python 3.12 and 3.13
  the application steps failed for D21 as before and `StartDaemonTests` failed with
  "daemon did not run to completion"; on 3.11 and 3.14 every step passed. The test
  therefore detects D21.

## 2026-10-22: macOS, tkinter and a second fork (DEFECTS.md D21)

A diagnostic workflow on a throwaway branch (runs 39757012414, 39757563800,
39758623928, 39759157133, 39763180270 and 39763681340; branch since deleted) installed
the suite as the harness does, with zprocess at `macos-venv-launcher` (cd76607) and
PySide6 6.12.0, on `macos-latest` (macOS 26.6.2, arm64) with the python.org builds of
Python 3.11.9, 3.12.10, 3.13.16 and 3.14.8, and pyzmq 27.2.0 with libzmq 4.3.5.

- `labscript_utils.zlog --daemon` started from a shell gives a zlog server that answers
  pings on every version.
- In a harness run with `zprocess.start_daemon` traced, on Python 3.12 the forked child
  of every zlog start from runviewer, runmanager, lyse and BLACS was killed by signal 9
  inside `subprocess.Popen`. The zlock start in the same run completed. On 3.11 every
  start completed.
- A script that sets up a given state, forks, and in the child starts a process: after
  `import tkinter`, after creating a Tk root window, or after `import
  labscript_utils.excepthook`, the child was killed by signal 9 when it called `fork()`
  (directly or through `Popen` with `close_fds=True`) on Python 3.12 and 3.13, and
  completed on 3.11 and 3.14. `execv` and `posix_spawn` in the child completed on every
  version. With no tkinter import, or with only a QApplication, the splash screen or
  `import desktop_app`, every method completed.

| Python | Tcl/Tk | Second fork after `import tkinter` |
|---|---|---|
| 3.11.9 | 8.6.13 | completes |
| 3.12.10 | 8.6.16 | killed by signal 9 |
| 3.13.16 | 8.6.18 | killed by signal 9 |
| 3.14.8 | 9.0.4 | completes |

On Python 3.12 with labscript-utils master, `import runviewer.__main__` in a plain shell
failed in the same way; the error window process that the excepthook then started kept
the shell's pipe open, and the job was cancelled at its time limit.

## 2026-10-22: desktop-app #35 (the entry point launcher on macOS, DEFECTS.md D19)

desktop-app's `get_venv_executable_and_env` is a copy of the zprocess function of D19,
and `desktop_app/launcher.py` uses it to start the application from its entry point
script, so the `blacs`, `runmanager`, `lyse` and `runviewer` scripts of a macOS venv
start the application under the base interpreter. The harness does not show this: it
starts the applications with `python -m`.

A diagnostic workflow on a throwaway branch (run 39753264955, since deleted) ran on
`macos-latest` with Python 3.12.10 and 3.14.8 (framework builds from `setup-python`),
in a venv made with `python -m venv` and in one made with `uv venv`, each with pyzmq
installed. In each venv it installed desktop-app master and then the branch
`macos-venv-launcher`, and ran the launcher with `sys.argv[0]` set to the name of a
package in the working directory, so that the launcher started that package's
`__main__.py`, which prints the child's `sys.executable` and `sys.prefix` and imports
`zmq`. With master the launcher started the child from the framework's `python3.x`
(the venv's `python` is a symlink to it with both tools), the child reported the
framework prefix and `import zmq` failed. With the branch the child was started from
the venv's `python`, reported the venv prefix and imported `zmq` from the venv. The
same in all four venvs.

Locally on Linux (Arch, Python 3.14.8, the harness venv) the same check with master and
with the branch: both children report the venv prefix and import `zmq`; master starts
`/usr/bin/python3.14` with `__PYVENV_LAUNCHER__` set and the branch starts the venv's
`python`.

Run 39753073309 (`desktop-app=chrisjbillington/desktop-app@macos-venv-launcher`,
Ubuntu and Windows): the 25 jobs for Python 3.11 to 3.14 with PySide6, PyQt6 and PyQt5,
and Ubuntu Python 3.14 with `numpy<2.5`, passed every step. Run 39754354241
(`desktop-app=pr/35`, the pull request merged into master) gave the same result. In
both runs the six Python 3.15 jobs fail at install as always.

## 2026-10-22: interrupting the main thread of a subprocess (zprocess branch `interrupt-main-thread`)

Measurements behind `SUBPROCESS-INTERRUPTION.md`, on Arch Linux with Python 3.14.8,
NumPy 2.5.4, h5py 3.16.0, pyzmq 27.2.0 and libzmq 4.3.5.

**Interrupt latency.** A script puts the main thread into each blocking state below and a
timer thread acts 0.5 s later, either with `_thread.interrupt_main()` (lyse #153's
method) or with `zprocess.interrupt_main_thread()` from the branch, which on POSIX is
`signal.pthread_kill(main_thread, SIGINT)`. The table gives the time from the start of
the state to the `KeyboardInterrupt` in the main thread.

| Main thread in | `_thread.interrupt_main()` | `interrupt_main_thread()` |
|---|---|---|
| `time.sleep(6)` | 6.00 s, after the sleep ended | 0.50 s |
| `Lock.acquire(timeout=6)` | 6.00 s, after the timeout | 0.50 s |
| zmq `poll(6000)` | 6.01 s, after the poll ended | 0.50 s |
| Python `while` loop | 0.51 s | 0.51 s |
| `np.linalg.inv` on a 6000×6000 array (4.64 s alone) | 4.50 s, when the call returned | 3.82 s, when the call returned |
| h5py write loop that returns at 0.1 s | 0.61 s, after the loop returned | 0.50 s, after the loop returned |

**HDF5 files after an interrupt.** A subprocess writes to an HDF5 file in a loop
(`create_dataset`, an attribute write and `flush()` per iteration) and gets SIGINT from a
timer thread after 0.3 s:

| How the file was open | Result |
|---|---|
| `with h5py.File(...)`, closed as the exception propagates | reopens; 1392 datasets, attribute 1390 |
| `h5py.File(...)` left open, closed by interpreter shutdown | reopens; 1115 datasets, attribute 1114 |
| the same loop ended with SIGKILL after 0.5 s | reopens in this run; 1531 datasets (the 2026-10-22 lyse #151 test below records a file that did not reopen after SIGKILL) |

**zprocess test suite.** With the branch installed in a venv (editable, Python 3.14.8),
`pytest -o addopts= tests` passes: the new `InterruptMainThreadTests` (sleep, lock
acquisition, zmq poll and Python loop interrupted within 0.2 s of the call to
`interrupt_main_thread()`; `RuntimeError` with SIGINT ignored), the new `KillLockTests`
and the existing heartbeat tests, including `test_subproc_survives_until_kill_lock_released`,
which now exercises the `exit_when_released()` path.

**GitHub Actions.** Run 39739704191 (`zprocess=chrisjbillington/zprocess@interrupt-main-thread`
at 89b72d2, all steps including the zprocess test suite): the 21 Ubuntu and Windows jobs
for Python 3.11, 3.12 and 3.14 and the Ubuntu Python 3.13 PySide6 and PyQt5 jobs
passed every step. The three Windows Python 3.13.16 jobs failed the new
`test_lock_acquire`: the `KeyboardInterrupt` arrived 4.0 s after the call, when the
lock wait timed out, so a lock wait in the main thread is woken by the SIGINT event on
Windows from Python 3.14 (where the three Windows jobs passed) and not on 3.13 as the
test and the helper's docstring had assumed; the test now expects the late interrupt
before 3.14 (commit b05a273, which replaced 89b72d2). The Ubuntu Python 3.13 PyQt6 job
failed the pre-existing zlock test `OtherTests.test_bind_to_port` with "Address already
in use" for the random port it chose; unrelated to the change. Run 39741071991 with the
same refs at b05a273: the 25 jobs for Python 3.11 to 3.14 with PySide6, PyQt6 and PyQt5,
and Ubuntu Python 3.14 with `numpy<2.5`, passed every step, the zprocess test suite
included (80 tests, 2 skipped on Windows as always). The six Python 3.15 jobs fail at
install as always.

**macOS.** The harness had not been run on macOS before. Run 39739717279
(`macos-latest`, Python 3.11 to 3.15 with PySide6, the branch at 89b72d2, all steps):
the new `InterruptMainThreadTests` and `KillLockTests` passed on Python 3.11 to 3.14,
but on every job the `compile`, `runmanager-api`, `apps` and `lyse-gui` steps failed
with `ModuleNotFoundError: No module named 'labscript_utils'` in each subprocess that
zprocess started, and the 28 zprocess tests that start a subprocess failed the same
way. Run 39742429966 (zprocess master, Python 3.14) fails identically, so the cause
predates the branch: `DEFECTS.md` D19, zprocess starts a child on macOS from the
framework's `bin/python3.x` stub, which discards the venv. A diagnostic workflow on a
throwaway branch (run 39742696067, since deleted) started a child both ways from a uv
venv of Python 3.14.8 on the runner: from `sys._base_executable` with
`__PYVENV_LAUNCHER__` set the child reported the framework prefix and could not import
pyzmq; from `sys.executable` it reported the venv prefix and imported it.

With the D19 fix (zprocess branch `macos-venv-launcher`): run 39743170120 (the fix
alone, Python 3.11 to 3.14, PySide6) passed every harness step on Python 3.11 and 3.14,
and the zprocess suite on every job except `ZLogServerTests.test_no_access`, which
expects "Permission denied" for `/test.log` where macOS reports "Read-only file
system" (the second commit of the branch, fd5b647, accepts either). Run 39743290230
(the fix plus the interrupt branch, on the throwaway branch
`test/interrupt-main-thread-macos`, since deleted): the whole zprocess suite passed on
Python 3.14 apart from `test_no_access`, including the subprocess and heartbeat tests
and the new tests, and the same on 3.11 to 3.13. In both runs the Python 3.12 and 3.13
jobs failed the `runviewer`, `apps` and `lyse-gui` steps because no zlog server could
be reached: `ensure_connected_to_zlog` starts `labscript_utils.zlog --daemon` after
the first ping fails and the second ping, with a 15 s timeout, also fails, so every
application fails in `setup_logging`. The zlock server, started the same way, works on
those jobs, and the 3.11 and 3.14 jobs pass (`DEFECTS.md` D21; the cause is in the section "macOS, tkinter and a second fork").
Run 39744288024 (the branch at fd5b647, with the `test_no_access` change): the Python
3.11 and 3.14 jobs passed every step and all 73 zprocess tests, the first full pass of
the harness on macOS; the 3.12 and 3.13 jobs failed the same three steps for the zlog
reason, and their zprocess test process ended with "Fatal Python error: Segmentation
fault" during the heartbeat tests. The same crash had ended the 3.11, 3.12 and 3.13
jobs of run 39743290230; it is a race in the test's scripted heartbeat server, which
closed its socket under its polling thread (`DEFECTS.md` D20, fixed by the third
commit of the branch). The Python 3.15 job fails at install as always.

Runs 39747320066 (macOS) and 39747331413 (Ubuntu and Windows) at cd76607, the head of
zprocess #36: the zprocess test suite passes on every macOS job (73 tests on Python
3.11 to 3.14, no crash), the harness passes every step on macOS with Python 3.11 and
3.14, the 3.12 and 3.13 jobs fail only the three application steps for the zlog reason
(D21), and the 25 Ubuntu and Windows jobs for Python 3.11 to 3.14 pass every step. The
Python 3.15 jobs fail at install as always.

## 2026-10-22: Qt styles on Windows

The Windows set of the Qt style screenshots, for comparison with the Linux set in the
next section, taken with `tools/style-screenshots/` on Windows 11 Pro (build 26200) in a
VirtualBox virtual machine, with Python 3.14.3 and the components at the same
default-branch commits as the Linux set (labscript-utils c1aa2a3, blacs cac5198,
runmanager 7e692f4, lyse c74fa4e, runviewer 38e5c0b, qtutils d330ae1). Three venvs:
PySide6 6.12.0, PyQt6 6.11.0 (Qt 6.11.2) and PyQt5 5.15.11 (Qt 5.15.2). The light images
were taken with Windows in light app mode and the dark images with Windows in dark app
mode. Every one of the 48 combinations produced an image. The images, with their JSON
and log files, are in `Z:\screenshots` on the virtual machine, a folder shared with the
host, for the maintainer to copy to the Linux machine beside `screenshots/linux`.

- The default style is `windows11` with PySide6 and PyQt6, and `windowsvista` with
  PyQt5. The default-style and Fusion images differ throughout: window colour, frames,
  check boxes, tabs and headers.
- With Qt 6, `QStyleHints.setColorScheme` gives a light palette (window colour #f3f3f3
  with windows11, #f0f0f0 with Fusion) and a dark one (#1e1e1e with both styles).
- PyQt5 gives a dark palette through the `windows:darkmode=2` platform option when
  Windows is in dark app mode: the window and base colours are #000000 with white
  text, with both styles. With windowsvista, frames are drawn as white one-pixel lines
  and the four applications are readable. With Fusion, frames and the borders of line
  edits are not drawn, so the queue list and the hostname box of BLACS and the file
  boxes of runmanager are not distinguishable from the window, and the alternate rows
  of the lyse shots table keep the light Fusion colour (#e9e7e3) with black text on the
  black base. With both styles, the black colour swatch of the shot in runviewer is
  invisible on the black base. These are the combinations that look broken.
- With windows11 in the light scheme, the empty part of the vertical header of the lyse
  shots table is drawn mid-grey (#b3b3b3); Fusion and the PyQt5 images draw it in the
  window colour (#f0f0f0). With Fusion in the dark scheme, the alternate rows of the
  lyse shots table are dark blue (#001a68) on the #2d2d2d base; with windows11 they are
  #393939.
- In the dark scheme the runviewer plot area keeps a white background with every binding
  and style, and the blue "outer" expansion icon in runmanager has low contrast with the
  dark table, as on Linux.
- PyQt5 uses a different default font from the Qt 6 bindings, so the PyQt5 images have
  smaller text, as on Linux.
- The lyse runs with PyQt6 log the `fontMetrics` AttributeError of DEFECTS.md D17
  (lyse #154 is not merged), the lyse runs with PySide6 show the deprecation warning for
  the same call in the output pane, and every runviewer run logs the missing
  DummyIntermediateDevice parser of labscript-devices #157. None of these affects the
  images.
- The zlock and zlog servers that the suite starts with the harness profile's shared
  secret are still running after `run_all.py` finishes. They have to be stopped before
  a real profile is restored, since they refuse connections made with another secret.


## 2026-10-22: Qt styles on Linux

Screenshots of BLACS, runmanager, lyse and runviewer for comparison of the default Qt
style with Fusion (`docs/RELEASE-PLAN.md` section 6), taken with
`tools/style-screenshots/` on Arch Linux under GNOME on Wayland, with Python 3.14.8 and
the components at their default branches (labscript-utils c1aa2a3, blacs cac5198,
runmanager 7e692f4, lyse c74fa4e, runviewer 38e5c0b, qtutils d330ae1). Three venvs: PySide6
6.12.0, PyQt6 6.11.2 (Qt 6.11.2) and PyQt5 5.15.19. The images are in `screenshots/linux`,
which git ignores; the Windows set is in the section above.

- The default style is Fusion with every binding. Qt 6 runs on Wayland with the gtk3
  platform theme; PyQt5 runs on X11 through XWayland. The default-style and Fusion images
  of runviewer are identical pixel for pixel. Those of the other applications differ only
  in content that changes between runs: the BLACS status text, the lyse output and
  progress, and whether runmanager had finished parsing the globals.
- With Qt 6, `QStyleHints.setColorScheme` switches between a light palette (window colour
  #fcfcfc) and a dark one (#323232). PyQt5 has no colour scheme API and its palette is
  light (#efefef); there is no dark PyQt5 image.
- In the dark scheme, the runviewer plot area keeps a white background, and the blue
  "outer" expansion icon in runmanager has low contrast with the dark table background.
  The other widgets in the four applications follow the palette.
- PyQt5 uses a different default font from the Qt 6 bindings, so the PyQt5 images have
  smaller text.

## 2026-10-22: lyse #154 (status column with PyQt6, DEFECTS.md D17)

Branch `pyqt6-font-metrics` on labscript-suite/lyse (head feb7540, one commit on master
c74fa4e). A script loads `lyse/widgets.py`, sets an `ItemDelegate` on a `QTableView`
with one shot at 50 % in the status column, shows and grabs the view under the
offscreen platform and collects the exceptions that reach the excepthook. Python 3.14.8,
PyQt6 6.11.0, PySide6 6.12.0 and PyQt5 5.15.11:

| Code | PyQt6 | PySide6 | PyQt5 |
|---|---|---|---|
| master c74fa4e | `AttributeError: 'QApplication' object has no attribute 'fontMetrics'`, twice | no exception | no exception |
| feb7540 | no exception | no exception | no exception |

Run 39723562432 with `lyse=pyqt6-font-metrics`: the 25 jobs for Python 3.11 to 3.14
passed every step. The Ubuntu Python 3.14 PyQt6 job first failed in `apt-get update`
(403 from packages.microsoft.com) and passed when rerun. The PyQt6 job logs have no
`fontMetrics` traceback. The Python 3.15 jobs fail at install as always.

## 2026-10-22: labscript-devices #157 (DummyIntermediateDevice runviewer parser)

Branch `dummy-intermediate-runviewer-parser` on labscript-suite/labscript-devices (head
bcc6b40, one commit on master b6ea556). Before the change, the `runviewer` step passed
but runviewer logged "Failed to load device intermediate_device" with a `ValueError`
traceback for every job, because `DummyIntermediateDevice` has no runviewer parser; the
example shot showed only the clock line trace. The `runviewer` step now checks the
`digital_out` and `analog_out` values of the example shot at 0.5 s, 1.25 s, 1.625 s
and 2 s when the parser is present, and reports the parser as KNOWN for
labscript-devices #157 when it is not (harness commits 21aa43d and 04bace8).

**Local** (Python 3.14.8, PySide6, in the user namespace of `harness/README.md`, the
other components at master): with the branch, `intermediate_device` loads without
error and gives three traces; `digital_out` is 0, 1 and 0 at 0.5 s, 1.25 s and 2 s, and
`analog_out` is 0 V, 0.502 V and 1 V at 1.25 s, 1.625 s and 2 s. With labscript-devices
master, the step reports the parser as KNOWN and passes.

Run [39721228849](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39721228849)
with `labscript-devices=labscript-suite/labscript-devices@dummy-intermediate-runviewer-parser`
and run [39722600814](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39722600814)
with `labscript-devices=pr/157`: the 25 jobs for Ubuntu and Windows, Python 3.11 to 3.14
with PySide6, PyQt6 and PyQt5, and Ubuntu Python 3.14 with `numpy<2.5`, passed every
step, each with the parser check reported as FIXED and the value checks passing. The six
Python 3.15 jobs fail at install as always.

## 2026-10-22: lyse #153 (Abort button) and the `lyse-gui` harness step

Branch `abort-analysis` on labscript-suite/lyse (head 5e698ae, on the head of lyse #151,
6c8312d, on master c74fa4e), tested with zprocess #34 (`pr/34`), which the worker restart
path needs (DEFECTS.md D14). The new `lyse-gui` harness step runs the lyse GUI in the
check process under the offscreen platform, adds a routine that loops in Python
(`time.sleep(0.01)` in a loop) and one that sleeps for 600 s, submits the example shot
and clicks Abort.

**Local** (a venv with Python 3.14.8, PySide6 6.12.0 and PyQt6 6.11.0, in the user
namespace of `harness/README.md`): with both bindings, the looping routine stops 0.1 s
after Abort with "Interrupted" in the output box and its worker survives; the sleeping
routine's worker is replaced 7.8 s to 7.9 s after Abort (the 5 s abort timeout, 2 s for
the quit that the restart sends first, then SIGTERM); analysis is paused after each; the
interrupted worker then runs a routine to completion and the shot is marked as analysed.
Without the Abort button (lyse master), the step reports KNOWN for lyse #153 and
passes.

Run 39716288975 with `lyse=abort-analysis zprocess=pr/34`: the 21 Ubuntu and Windows
jobs for Python 3.11 to 3.14 with PySide6 and PyQt5, and Ubuntu with PyQt6, passed every
step; the four Windows PyQt6 jobs hung in `lyse-gui` before the check's first output
and were cancelled by the maintainer after 35 minutes. The check created the
QApplication before importing the lyse entry module, which calls
`desktop_app.set_process_appid()` and so installs the Windows event hook with a
QApplication already present; lyse itself does these the other way round. The check
now imports the lyse entry module first (harness commit cb88106). The run also showed
that `run_step` relayed the check's output in the calling thread and waited with the
timeout only after the pipe closed, so a check that hangs without exiting was never
timed out; the output is now relayed in a thread and on timeout the check's process
tree is ended (tested locally with a check that starts a child and sleeps: ended after
3 s with no child left).

Run 39719962771 with the same refs after that commit: the 25 jobs for Python 3.11 to
3.14 passed every step; the looping routine stopped 0.1 s after Abort on every job and
the sleeping routine's worker was replaced after 8 s to 9 s (Windows PyQt6: 9.1 s).
The Python 3.15 jobs fail at install as always.

The PyQt6 jobs' `lyse-gui` logs hold 20 to 24 tracebacks `AttributeError: 'QApplication'
object has no attribute 'fontMetrics'` from `lyse/widgets.py:76`, raised whenever the
status column of a shot that is not fully analysed is painted; the checks pass because
the excepthook reports the exception and painting continues. Recorded as DEFECTS.md
D17.

## 2026-10-22: lyse #152 (removing many shots, DEFECTS.md D16)

Branch `faster-shot-removal` on labscript-suite/lyse (head 0bb3acd, two commits on master
c74fa4e), compared with master c74fa4e. A script creates `lyse.filebox.DataFrameModel`
with a `QTableView` and a stub application, adds shots with 200 data columns through
`add_files` in batches of 1000, selects rows, calls `remove_selection(confirm=False)`
and checks that the dataframe, the Qt model rows, `row_number_by_filepath` and the row
headers list the remaining shots in order. The timings are for the harness venv (Python
3.14.8, PySide6 6.12.0, pandas 3.0.6, offscreen Qt platform):

| Shots removed | master | branch |
|---|---|---|
| 990 of 1000 | 4.8 s | 0.14 s |
| 3990 of 4000 | 61 s | 0.47 s |
| 2000 of 4000, integer indexing | 39 s | 0.28 s |
| 2667 of 4000 in blocks of 7, integer indexing | 36 s | 0.37 s |
| 8000 of 16000 | not run | 1.1 s |
| 15990 of 16000, integer indexing | not run | 1.9 s |

A profile of the branch before the selection ranges replaced `selectedRows()`, removing
1990 of 2000 shots, spent 4.0 s of 4.3 s in 408,000 calls to `UneditableModel.flags()`.
With `NoEditTriggers` and no `flags()` override, `selectedRows()` still took 1.3 s for
7990 rows that were selected one row per range, as each row is checked against every
range. The same consistency checks pass with PyQt6 6.11.0 and PyQt5 5.15.11 for 1990 of
2000 shots, contiguous and in blocks of 7. With all three bindings, double-clicking,
F2 and typing open no editor in the shots table, the edit columns dialog or a routine
list, and a routine checkbox toggles on click; with the default edit triggers, an
editor opens.

Run 39715065177 with `lyse=labscript-suite/lyse@faster-shot-removal`: the 25 jobs for
Python 3.11 to 3.14 passed every step (the six Python 3.15 jobs fail at install as
always).

## 2026-10-22: zprocess #34 and lyse #151 (DEFECTS.md D14 and D15)

Branches `interruptor-concurrent-subscribe` on chrisjbillington/zprocess (head c407999,
one commit on master 1de4c26) and `remove-routine-kill-lock` on labscript-suite/lyse
(head 6c8312d, one commit on master c74fa4e). zprocess #34 sets `XPUB_VERBOSER` on the
`Interruptor` XPUB socket and adds `ReadQueueTests.test_put_while_another_thread_gets`.
lyse #151 removes the routine-wide `with kill_lock:` in `AnalysisWorker.mainloop`.

**Local** (a venv with Python 3.14.8, PySide6, pyzmq 27.2.0, libzmq 4.3.5 and the other
components at their master branches, offscreen Qt platform): the new zprocess test fails
on master and passes on the branch, and the full zprocess test suite passes on the
branch (74 tests). With both branches installed, an `AnalysisRoutine` restarted 2 s into
a routine:

| Routine | Result |
|---|---|
| sleeps for 10 s | the worker exits on SIGTERM (return code -15); "worker restarted" 1 s later |
| writes to an open HDF5 file for 4 s, then sleeps | "SIGTERM ignored" printed; the worker exits with -15 when the file is closed, 1 s after SIGTERM; the file has all eight datasets |
| writes to an open HDF5 file for 5 s | the file is still open when SIGKILL is sent; the worker exits with -9 and h5py cannot open the file ("bad object header version number") |

With lyse master, SIGTERM has no effect in any of these cases while the routine runs.

**Run 39713730391** (`zprocess=interruptor-concurrent-subscribe
lyse=remove-routine-kill-lock`, all steps including the zprocess test suite): the 25 jobs
for Python 3.11 to 3.14 passed every step, and the new test passed on Ubuntu and Windows
(the six Python 3.15 jobs fail at install as always).

## 2026-10-22: lyse #149 (shots from the file dialog sorted by name)

Branch `sort-loaded-shots` on labscript-suite/lyse (head 03e3c95, one commit on master
c74fa4e). In the harness venv (Python 3.14.8, PySide6, offscreen Qt platform), with
`QFileDialog.getOpenFileNames` stubbed to return `s_10.h5, s_02.h5, s_01.h5, s_11.h5`,
`FileBox.on_add_shot_files_clicked` puts `s_01.h5, s_02.h5, s_10.h5, s_11.h5` on the
incoming queue. Run 39712368939 with `lyse=sort-loaded-shots`: the 25 jobs for Python
3.11 to 3.14 passed every step (the six Python 3.15 jobs fail at install as always).

## 2026-10-22: lyse routine restart during analysis hangs the GUI (DEFECTS.md D14)

A venv with Python 3.14.8, PySide6, pyzmq 27.2.0 and libzmq 4.3.5, with zprocess
1de4c26, qtutils d330ae1, labscript-utils c1aa2a3 and lyse c74fa4e (the master branches),
offscreen Qt platform.

**lyse.** A script that creates `lyse.routines.AnalysisRoutine` for a routine that sleeps
for 10 s, starts `do_analysis` in a thread as the routine box does, and calls
`restart()` 2 s later. The worker prints "SIGTERM ignored: will be handled when kill lock
released." when it gets SIGTERM, and lyse reports "worker killed" 2 s after that. The
main thread then blocks in `ReadQueue.put` at `Interruptor.subscribe`
(`zprocess/utils.py:67`), called from `lyse/routines.py:606`; the analysis thread is in
`ReadQueue.get`. No Qt timer fires after that point, and no new worker is started.

**zprocess.** A `ReadQueue` on an inproc PAIR socket, with one thread in `get()`: `put()`
from a second thread does not return within 3 s.

**Fix.** With `self._xpub.setsockopt(zmq.XPUB_VERBOSER, 1)` added to
`Interruptor.__init__` in the installed zprocess, the `put()` returns at once and
`get()` returns the object. In the lyse case the analysis thread receives
`(False, {})` when the worker is killed, lyse reports "worker restarted" 1 s later and
the main thread keeps running.

## 2026-10-22: lyse dataframe update after an analysis routine (DEFECTS.md D13)

Branch `batch-dataframe-updates` on labscript-suite/lyse (head 1f6da15, one commit on
master c74fa4e). `DataFrameModel.update_rows` applies all of a routine's results in one
main-thread call instead of one `update_row` call per shot.

**Equivalence** (harness venv, Python 3.14.8, pandas 3.0.6, PySide6 6.12.0; and a
Python 3.12 venv with pandas 2.3.3 and NumPy 1.26): 60 shots, three rounds of results of
mixed types (floats, ints, bools, strings, multi-line strings, arrays, lists, nested
dicts, None, all-None, int and str in one column, a float into an int column, a str into
a float column, a column that is float and then str), some shots without results and one
result for a shot that is not in lyse. The master `update_row` loop and `update_rows`
give the same dataframe values and dtypes and the same model item text and tooltips;
with pandas 2.3.3 both emit the same `FutureWarning` for the incompatible-dtype setting.

**Timing, model only** (offscreen, `update_row` called through `inmain` from a worker
thread as lyse does; 200 columns, five results per shot):

| Shots | Result columns | master | branch |
|---|---|---|---|
| 1000 | new | 2.34 s | 0.14 s |
| 1000 | existing | 2.18 s | 0.05 s |
| 2000 | new | 5.00 s | 0.29 s |
| 2000 | existing | 4.73 s | 0.08 s |

**Timing, running lyse** (offscreen, scratch profile; shots with 100 globals submitted
over the lyse port, a single-shot routine saving one result, a multishot routine that
saves five results to every shot once all shots are analysed; time from the end of the
multishot routine until `get dataframe` returns all of its results, polled every 0.5 s):

| Shots | master | branch |
|---|---|---|
| 500 | 6.72 s | 0.30 s |
| 1000 | 15.30 s | 0.36 s |

No tracebacks in the lyse output of any run.

**GitHub Actions:** run
[39712395251](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39712395251)
of `test.yml` with `lyse=labscript-suite/lyse@batch-dataframe-updates` passed every step
in all 25 jobs (the six Python 3.15 jobs fail at install as always).

## 2026-10-22: graphical excepthook only in the applications (DEFECTS.md D12)

Local branches `excepthook-gui-only`: labscript-utils 2f41c08 and e5cd210, blacs d2e7675
and 7719dee, lyse b956ecf, runmanager bf55903, runviewer c25afc2, labscript-devices
33e20e7, each on the master of 2026-10-22; the other components at master. Pull
requests labscript-utils #136, blacs #133, lyse #148, runmanager #142, runviewer #79 and
labscript-devices #156.

**Local** (Python 3.14.8, PySide6, a new harness venv installed from those commits, in a
user, mount and network namespace, with `LABSCRIPT_DISABLE_GRAPHICAL_EXCEPTHOOK=1`):
every harness step passed, with the three `runmanager-api` checks marked known as
before. With the branches, each in a fresh interpreter:

- after importing `lyse`, `labscript_utils.connections`, `blacs.device_base_class`,
  `blacs.front_panel_settings`, `labscript_devices.PulseBlaster` and `labscript`,
  `sys.excepthook` is the default hook and `Thread.run` is not patched; on master each
  of those imports installed the handler;
- `import lyse; 1/0` prints the traceback;
- `import labscript_utils.excepthook` installs the handler; a second `install()` does not
  patch `Thread.run` again; with the variable set, an exception in a thread and a direct
  call of the handler print the traceback and start no window process;
- with the variable unset or `0`, the handler would show windows.

**GitHub Actions:** run
[39707074062](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39707074062)
of `test.yml` with the six branches as `name=labscript-suite/name@excepthook-gui-only`
passed every step in the 25 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with
PySide6, PyQt6 and PyQt5 and the NumPy 2.4 job; the six Python 3.15 jobs failed at
"Install the components" as before.

## 2026-10-21: qtutils #41 (auto scroll to end after hiding, runmanager #32)

Branch `auto-scroll-after-show` on philipstarkey/qtutils (head 2ee0c86, one commit on
master d330ae1), qtutils #41.
`set_auto_scroll_to_end` records whether the scrollbar is at the end only while its
scroll area is visible, and scrolls to the end after a show event if it was at the end
before.

**Local** (harness venv, Python 3.14.8, PySide6 6.12.0; and Python 3.12 venvs with PyQt5
and PyQt6 from PyPI; offscreen Qt platform, also the Wayland and xcb platforms for
PySide6): an `OutputBox` or a bare `QPlainTextEdit` in the first tab of a `QTabWidget`.

| Scenario, with the Output tab hidden while 50 lines are written | master | branch |
|---|---|---|
| 3 or 60 lines before, scrollback cap reached, `\r` progress lines, wrapped lines, window resized | at end | at end |
| user clicked in the box first (text cursor above the end) | scrolled to the cursor; on PySide6 and PyQt6 does not follow further output, on PyQt5 follows it again | at end, follows further output |
| hidden at the 1000-line scrollback cap | at end, but the recorded state is "not at end" until the next value change | at end |
| `QTableView` (as in the lyse file box), switching tabs, hiding or minimising the window | at end | at end |
| user scrolled up first (`QTableView`) | stays where the user left it | stays where the user left it |

A `QPlainTextEdit` that the user scrolled up, with the text cursor at the end, scrolls to
the end on the first show after a hidden append on both master and the branch; Qt does
this, not qtutils. `unset_auto_scroll_to_end` stops the scrolling. The lyse file box
table did not show the defect in any scenario tried.

**GitHub Actions:** run
[39569702167](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39569702167)
of `test.yml` with `qtutils=philipstarkey/qtutils@auto-scroll-after-show` passed every
step in all 25 jobs (the six Python 3.15 jobs fail at install as always). Run
[39570652352](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39570652352)
with `qtutils=pr/41` passed every step in all 25 jobs as well.

## 2026-10-21: runviewer #78 (exec() on the warning box)

Branch `message-box-exec` on labscript-suite/runviewer (head 6feafc1, one commit on
master 38e5c0b): the warning box for files that are not valid HDF5 files calls `exec()`,
which was the last `exec_()` call on a program code path in the suite.

**Local** (a Python 3.14.8 venv with PyQt5 5.15.11, PyQt6 6.11.0 and PySide6 6.12.0):
`QMessageBox` has `exec` with each binding, and the module compiles.

**GitHub Actions:** run
[39568743406](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39568743406)
of `test.yml` with `runviewer=labscript-suite/runviewer@message-box-exec` passed every
step in all 25 jobs (the six Python 3.15 jobs fail at install as always). Run
[39569717948](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39569717948)
with `runviewer=pr/78` passed every step in all 25 jobs as well.

## 2026-10-21: qtutils #40 (exec_ alias only in PyQt6)

Branch `exec-alias-pyqt6` on philipstarkey/qtutils (head e8be350, one commit on master
d330ae1): the `exec`/`exec_` alias block keeps only the PyQt6 branch.

**Local** (a Python 3.14.8 venv with PyQt5 5.15.11, PyQt6 6.11.0 and PySide6 6.12.0,
offscreen Qt platform): with each binding selected through `QT_ENV`, `QCoreApplication`
and `QDialog` have both `exec` and `exec_` after importing `qtutils.qt`, and an
application event loop started with either spelling runs and returns 0. Without qtutils,
PyQt6 has neither `exec_`. The removed branch could never run: the sip declarations in
the PyQt5 5.0 and 5.14 sources define `exec` under `%If (Py_v3)` next to an unconditional
`exec_`, the method name tables in the QtCore binaries of the PyPI wheels for 5.9, 5.11.3,
5.12, 5.13.0 and 5.15.0 contain both names, and PyPI has never carried Python 2 wheels of
PyQt5.

**GitHub Actions:** run
[39566433436](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39566433436)
of `test.yml` with `qtutils=philipstarkey/qtutils@exec-alias-pyqt6` passed every step in
all 25 jobs (the six Python 3.15 jobs fail at install as always). Run
[39567292587](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39567292587)
with `qtutils=pr/40` passed every step in all 25 jobs as well.

## 2026-10-21: runmanager #141 (non-default output folder marker from an icon)

Branch `non-default-folder-icon` on labscript-suite/runmanager (head 9912fd0, one commit
on master 7e692f4): the marker is rendered from a `QIcon` at the small icon size instead
of the `pixmap` property in `main.ui` (DEFECTS.md D11).

**Local** (harness venv, Python 3.14.8, PySide6 6.12, the window built headless in a
namespace with a scratch profile): the label's pixmap is 16×16 at scale factor 1 and
32×32 at device pixel ratio 2 at scale factor 2, 16 logical pixels in both cases.

**GitHub Actions:** dispatch of `test.yml` with
`runmanager=labscript-suite/runmanager@non-default-folder-icon`, merged into master by
the harness, as run
[39565207484](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39565207484).
All 25 jobs passed every step, with the three known markers for #139 and #140 reported.

## 2026-10-21: qtutils #38 revised (enforce only on a non-empty value)

Branch `qtlock-enforce-opt-in` on philipstarkey/qtutils (head 066b805, one commit on
master d330ae1): `qtlock.enforce()` runs on import only when `QTUTILS_ENFORCE_QTLOCK` is
non-empty.

**Local** (harness venv, Python 3.14): importing qtutils from the branch installs the
`threading` profile hook with the variable set to `1`, and does not install it with the
variable unset or set to an empty string.

**GitHub Actions:** dispatch of `test.yml` with `qtutils=pr/38`, run
[39565884745](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39565884745):
the 25 jobs for Python 3.11 to 3.14 passed every step, and the 6 Python 3.15 jobs failed
at "Install the components" on the h5py build, as on the masters.

## 2026-10-23: qtutils #38 revised (a value of "0" does not enforce)

Branch `qtlock-enforce-opt-in` on philipstarkey/qtutils (head 44e2f3e, one commit on
master 114a6ec): `qtlock.enforce()` runs on import only when `QTUTILS_ENFORCE_QTLOCK` is
set to a value other than `""` or `"0"`.

**Local** (harness venv, Python 3.14): importing qtutils from the branch installs the
`threading` profile hook with the variable set to `1` or `yes`, and does not install it
with the variable unset, empty or `0`.

**GitHub Actions:** dispatch of `test.yml` with `qtutils=pr/38`, run
[39954916546](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39954916546):
the 25 jobs for Python 3.11 to 3.14 passed every step, and the 6 Python 3.15 jobs failed
at "Install the components", as on the masters.

## 2026-10-21: qtutils #39 (16×16 icons with @2x variants)

Branch `icons-16px-base` on philipstarkey/qtutils (head 1e853c6, one commit on master
d330ae1): the 16×16 icons from before 244c556 are the base files, the 32×32 files are the
`@2x` variants, and each file has an extension-less alias (DEFECTS.md D11).

**Local** (harness venv, Python 3.14.8, PySide6 6.12, the rebuilt resource): for
`:/qtutils/fugue/exclamation-white.png`, `:qtutils/fugue/exclamation-white` and
`:/qtutils/custom/outer`, `QIcon.availableSizes` is [16] at scale factor 1 and [16, 32]
at scale factor 2, `QIcon.pixmap(16)` is 16 px at ratio 1 and 32 px at ratio 2, and a raw
`QPixmap` is 16 px at either; a logo stays 32 px. Without the alias the extension-less
form loaded through the image reader's extension search and had no `@2x` variant. The
resource compiler stores a file listed twice only once (a two-entry test resource was
22 bytes larger than a one-entry one); the resource is 11.5 MB against 8.2 MB. In
runmanager, driven as for #140, the non-default output folder label's pixmap is 16×16
and the expansion editor's drop-down icons are 16 px without an explicit icon size.

**GitHub Actions:** dispatches of `test.yml` with
`qtutils=philipstarkey/qtutils@icons-16px-base`: run
[39560415769](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39560415769)
failed the `runmanager-api` check in all 25 jobs only on the cycle and conditional
cases that runmanager #139 adds, since runmanager was at master; those are now marked as
known for #139, and run
[39561230839](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39561230839)
passed every step in all 25 jobs with the three known markers reported. With
`runmanager=labscript-suite/runmanager@expansion-settings` as well, run
[39560501402](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39560501402)
passed every step in all 25 jobs.

## 2026-10-21: runmanager #140 (custom and automatic expansion settings)

Branch `expansion-settings` on labscript-suite/runmanager (head db18f83, one commit on
the #139 branch 2101a63; 469c8b3 before plain scalars were added to the screenshots,
223dff4 with an explicit icon size on the drop-down that qtutils #{n} made unnecessary): the globals file records whether each expansion setting is
custom, `automatic_expansions` computes the automatic settings, ranges are outer, and
the GUI edits the settings with a drop-down. The commit was revised on the maintainer's
request after the first screenshots (ce24437): no expansion shows as `None`, the entry
is `Auto` rather than `Automatic`, the drop-down puts `Auto` first and gives `outer` and
the zip groups their icons, and an empty entry means `Auto`.

**Local** (harness venv, Python 3.14.8, PySide6): the library functions round-trip the
flags, rename and delete carry them, files without the subgroup read as None and accept
writes; `automatic_expansions` keeps custom settings, makes lists and ranges outer, zips
a derived array with its source and leaves a global with a custom non-empty setting out
of the zip roots. The GUI, driven programmatically on a demo file with a scratch profile
(the namespace method in `harness/README.md`), migrates a file without the flags as
designed, makes a derived global custom when "outer" is chosen for it and returns its
source to plain outer, records a typed zip group name on Enter, discards the edit on
Escape, returns a global to `Auto` on an empty entry, records a custom none on a typed
`None`, and returns the globals to automatic settings from the reset action. The
screenshots in `docs/source/img` of the branch were taken from these runs. The
`runmanager-api` check, extended for the flags, `automatic_expansions` and a range,
passes through `harness/suite.py`.

**GitHub Actions:** dispatches of `test.yml` with
`runmanager=labscript-suite/runmanager@expansion-settings`, merged into master by the
harness: run
[39552719146](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39552719146)
on ce24437 passed every step in all 25 jobs; run
[39555021218](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39555021218)
on 469c8b3 passed every step in all 25 jobs as well, and run
[39556519853](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39556519853)
on 223dff4 passed every step in all 25 jobs, and run
[39560501402](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39560501402)
on db18f83 with the qtutils #{n} branch passed every step in all 25 jobs.

## 2026-10-21: runmanager #139 (topological evaluator)

Branch `topological-evaluator` on labscript-suite/runmanager (head 2101a63, one commit on
master 7e692f4; 803bb74 before `TraceDictionary` was removed on the maintainer's
request): `evaluate_globals` evaluates each expression once in dependency order
read from the syntax trees, instead of the retry loop over all unevaluated expressions.

**Local** (harness venv, Python 3.14.8, PySide6): a chain of three globals defined in
reverse order evaluates; a two-global cycle, a self-reference, a global that refers to the
cycle, an undefined name and a syntax error each hold the expected error and the rest
evaluate; a conditional records both branches in the hierarchy; comprehension variables
and lambda arguments are not dependencies; a global named `pi` is used by the globals that
refer to it; the expansion error, zip length and generator cases behave as before. A chain
of 1000 globals defined last-first evaluates in 0.05 s, against 11.7 s on master (the
same chain in definition order takes 0.02 s on master). The `runmanager-api` check was
extended with a cycle and a conditional case and passes, run through `harness/suite.py` in
a user, mount and network namespace with a scratch home directory so that the machine's
own profile and zlock server are not touched.

**GitHub Actions:** dispatches of `test.yml` with
`runmanager=labscript-suite/runmanager@topological-evaluator`, merged into master by the
harness, as runs
[39550004014](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39550004014)
(2243c87, the same code before a documentation change) and
[39550548845](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39550548845)
(803bb74). All 25 jobs of each passed every step. On 2101a63, run
[39556509567](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39556509567)
failed the `runmanager-api` check in all 25 jobs only because the check had been
extended for the API that #140 adds (`get_expansion_custom`, `get_custom_expansions`,
`automatic_expansions`, ranges as `outer`); every other check passed. Those checks are
now marked as known for #140 and run only when the API is present; with that harness,
run
[39557980780](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39557980780)
on 2101a63 passed every step in all 25 jobs, with the API presence check reported as
known and the expansion settings checks skipped.

## 2026-10-21: the harness tests a pull request merged into the current default branch

`harness/suite.py clone` fetched `refs/pull/N/head` for a `pr/N` ref, the branch as
pushed, so a run on a pull request did not include changes merged to the default branch
after the branch was made (the first #137 run below failed for that reason). It now
fetches the default branch and the pull request head in full and merges them itself
(commit 00ad31b; an intermediate version, 10c8a0f, used GitHub's `refs/pull/N/merge`,
which is recomputed only when something asks about the pull request).

**Local**: cloning into a scratch directory with `runmanager=pr/137` gives head 4e11a18
merged into master 3e1de29 with the pull request's change present, on a fresh clone and
on an existing shallow clone; `runmanager=pr/136`, which is merged, gives the master
tip; `labscript-devices=pr/148`, which conflicts with master, stops with a message and
leaves the clone clean.

**GitHub Actions:** on the final version, the dispatch with `runmanager=pr/137` as run
[39545120783](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39545120783)
passed every step in all 25 jobs for Python 3.11 to 3.14, with the clone log showing
the head merged into master 3e1de29, and the push run
[39545120201](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39545120201)
on the masters passed the same 25 jobs, with the 6 Python 3.15 jobs failing at install
on h5py as before. The same two runs on the intermediate version,
[39544208125](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39544208125)
and
[39544207365](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39544207365),
gave the same results.

## 2026-10-21: runmanager #137 (uneven zip groups) shortened and brought up to date

Branch `zip-length-check` on labscript-suite/runmanager: the zip group length check in
`evaluate_globals` rewritten in 16 lines in place of 24 (a9f99cb), then `master` merged
in for #138 (4e11a18). The branch was then replaced by the single commit 28fc9ae on
master 3e1de29 with the same tree; run
[39546648678](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39546648678),
dispatched with `runmanager=pr/137` on the harness that merges the pull request into
the current master itself, passed every step in all 25 jobs.

**Local** (harness venv, Python 3.14.8, PySide6): with a zip group of lengths 3 and 2,
an outer global and a constant, both zip globals hold the `ValueError` naming the
lengths, the other two globals are unaffected and `count_shots` gives 0; with
`raise_exceptions=True` the `ValueError` is raised with both names; with equal lengths
the group expands to 6 shots. A zip global that is an iterator without a length is
skipped by the check and caught by the strict `zip` in the expansion. The #138 case (a
non-iterable `outer` global holds `ExpansionError` and a global that refers to it
evaluates) passes after the merge.

**GitHub Actions:** two dispatches of `test.yml` with `runmanager=pr/137`, the other
components at their masters as of 04:03 UTC. Run
[39541941749](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39541941749),
on a9f99cb, failed the `runmanager-api` check in all 25 jobs at the case that #138
added, because the branch did not yet contain #138; every other check passed. Run
[39542471272](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39542471272),
on 4e11a18 after the merge, passed every step in all 25 jobs for Python 3.11 to 3.14
(Ubuntu and Windows, PySide6, PyQt6 and PyQt5, plus the `numpy<2.5` job).

## 2026-10-21: runmanager #138 (expansion error keeps the value in the namespace)

Branch `expansion-error-namespace` on labscript-suite/runmanager (head b5c4b25, one commit
on master 73199cb): `evaluate_globals` puts the value of a global that fails the
iterability check for its expansion into the namespace before recording the
`ExpansionError` (DEFECTS.md D10).

**Local** (harness venv, Python 3.14.8, PySide6): with `x = np.linspace(0, 10, 10)`
set to `outer` and `y = np.max(x)`, then `x` edited to `5`, the library evaluation and
the GUI's `guess_expansion_modes` on a stub gave on master `x` holding `ExpansionError`,
`y` holding `NameError`, the expansion still `outer` and 0 shots; on the branch `y = 5`,
the expansion blank and 1 shot. The `runmanager-api` check was extended with this case
(a non-iterable `outer` global holds `ExpansionError` and a global that refers to it
evaluates); it fails on master and passes on the branch.

**GitHub Actions:** dispatch of `test.yml` with
`runmanager=labscript-suite/runmanager@expansion-error-namespace`, the other components
at their masters as of 02:48 UTC, as run
[39535057217](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39535057217).
24 of the 25 jobs for Python 3.11 to 3.14 (Ubuntu and Windows, PySide6, PyQt6 and PyQt5,
plus the `numpy<2.5` job) passed every step. The Ubuntu 3.13 PyQt5 job passed every step
up to `runmanager-api` and failed at `apps`: runmanager raised "Address already in use"
on its labconfig port, so the remote API connection timed out; the runner already had a
process on that port, which is unrelated to the change. The six Python 3.15 jobs failed
at "Install the components" on the h5py build as before. The push of the extended check
to `main` also ran the masters as run
[39535056606](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39535056606),
where every job for 3.11 to 3.14 failed only at the new check, as expected without the
fix. runmanager #138 was merged on this result (3e1de29, 03:55 UTC).

## 2026-10-19: zprocess PAIR sockets (zprocess #33)

Branch `pair-sockets` on chrisjbillington/zprocess (head 71fe1dd, two commits on master
1de4c26): explicit poller event flags, then PAIR sockets for the parent/child channel
and the in-process `ReadQueue` sockets, negotiated through `parentinfo['pair_sockets']`
and the remote process server's protocol version (1.1.0 on the branch, 1.0.0 before).

**libzmq behaviour** (harness venv, Python 3.14.8, pyzmq 27.2.0, libzmq 4.3.5): a PAIR
socket connected to a PUSH or PULL socket, in either direction, reports CONNECTED then
DISCONNECTED on the connecting side; the sender's `send` succeeds and the message is
never delivered. A second PAIR peer connecting to an occupied PAIR socket completes the
handshake but receives nothing and has its own messages dropped. A PAIR socket over TCP
reconnects after the bound side is closed and rebound, and messages queued meanwhile are
delivered in both directions, so the zmq manual's statement that PAIR sockets do not
reconnect does not hold on this version. A reconnect test with a port in the ephemeral
range fails with "Address already in use" because the connecting side's retries
self-connect to its own port; this is a test artefact, not a PAIR property.

**Local:** the zprocess test suite on the branch passes in the harness venv: 74 tests in
110 s, one new (`test_legacy_server_process`, a remote process server whose protocol
query returns 1.0.0). The three mixed-version combinations were run end to end with the
installed master zprocess as the old side and the clone as the new side, each with a
real `RemoteProcessServer` in its own process and a `Process` subclass that echoes its
own zprocess path and socket type: old server with new parent used PUSH and PULL sockets
and printed the warning naming the server; new server with old parent used PUSH and
PULL; new server with new parent used PAIR. Each exchanged a message.

**GitHub Actions:** dispatch of `test.yml` with `zprocess=chrisjbillington/zprocess@pair-sockets`
and `all_steps` on, the other components at their masters as of 12:14 UTC, as run
[39250476711](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39250476711).
The 25 jobs for Python 3.11 to 3.14 (Ubuntu and Windows, PySide6, PyQt6 and PyQt5, plus
the `numpy<2.5` job) passed every step including `zprocess-tests` (111 s on Ubuntu, 115 s
on Windows); the six Python 3.15 jobs failed at "Install the components" on the h5py
build as before. zprocess #33 was opened on this result.

## 2026-10-19: BLACS shot cycle with the non-blocking state display and without qtlock enforcement

Measurements for blacs #132 (`state-display-nonblocking`, bfaaf25) and qtutils #38
(`qtlock-enforce-opt-in`, 6d0377b), made with `tools/blacs-timing/` in the local
harness venv (Python 3.14.8, PySide6 6.12.0, offscreen Qt platform) on the maintainer's
laptop (12th Gen Core i7-1270P, 12 cores). Each run compiles a 0.1 s shot with a
`DummyPseudoclock` and one or seven `DummyIntermediateDevice`s, submits 50 copies to
BLACS and takes medians over the last 49 from `BLACS.log`. Every configuration was run
twice. "Overhead per event" is the median over a tab's `transition_to_buffered` and
`transition_to_manual` events of the time outside the worker job; the range is over
tabs and runs.

| Tabs | blacs | qtutils | Cycle (s) | Overhead per event per tab (ms) | Instruct to ack wait (ms) | Finalise to next event (ms) |
|---|---|---|---|---|---|---|
| 2 | master | master | 0.160, 0.168 | 11 to 15 | 2 to 3 | 2 to 3 |
| 2 | branch | master | 0.161, 0.161 | 6 to 10 | 1 | 0 |
| 2 | master | branch | 0.161, 0.159 | 11 to 15 | 2 to 3 | 2 to 3 |
| 2 | branch | branch | 0.156, 0.156 | 5 to 9 | 0 to 1 | 0 |
| 8 | master | master | 0.231, 0.230 | 27 to 39 | 6 to 9 | 4 to 7 |
| 8 | branch | master | 0.215, 0.212 | 14 to 24 | 2 to 3 | 1 to 3 |
| 8 | master | branch | 0.201, 0.201 | 21 to 30 | 4 to 7 | 3 to 5 |
| 8 | branch | branch | 0.197, 0.201 | 17 to 22 | 2 to 5 | 1 to 2 |

The blacs change halves the per-tab overhead and removes the two steps that contain
only a `state` assignment; the cycle saving is about 0.017 s with 8 tabs and within
noise with 2, because the tabs transition in parallel. Disabling the qtlock profiling
hook saves 0.03 s per cycle with 8 tabs and nothing measurable with 2. The same two
changes were measured on the lab machine (an Intel NUC, 11th Gen Core i3-1115G4, three
real device tabs: a serial pseudoclock, a camera and a FunctionRunner; 1.405 s sequence;
BLACS 3.2.3 with the change applied to the installed file) on 2026-09-30, as medians of
ten shots excluding the first after each restart. Disabling `qtlock.enforce()` took the
cycle from 1.883 s to 1.845 s (transition to buffered 0.217 s to 0.194 s, transition to
manual 0.166 s to 0.155 s, mainloop overhead per transition event per tab 85 to 118 ms
down to 56 to 82 ms). The non-blocking `state` setter, measured with enforcement
already disabled, took the cycle from 1.845 s to 1.781 s (transition to buffered 0.194 s
to 0.166 s, transition to manual 0.155 s to 0.144 s, overhead per event per tab 56 to
82 ms down to 30 to 42 ms, "Instructing worker" to "Waiting for worker to acknowledge"
19.5 ms to 2.5 ms, "Finalising function" to "Waiting for next event" 16 ms to 1 ms).

Two `test.yml` dispatches, each with the other components at their masters as of 11:00
UTC: blacs `state-display-nonblocking` (bfaaf25) as run
[39241386260](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39241386260)
and qtutils `qtlock-enforce-opt-in` (6d0377b) as run
[39241439736](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39241439736).
The 25 jobs of each run (Ubuntu and Windows, Python 3.11 to 3.14, PySide6, PyQt6 and
PyQt5, plus the Ubuntu Python 3.14 PySide6 job with `numpy<2.5`) passed every step. The
pull requests blacs #132 and qtutils #38 were opened on these results.

## 2026-10-18: the harness without KNOWN markers, on the masters

Push run [39121553218](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39121553218)
after the three `KNOWN` markers were removed, with every component at its master as of
11:00 UTC: the 25 jobs for Python 3.11 to 3.14 passed every step, and the 6 Python 3.15
jobs failed at "Install the components" because h5py 3.16.0 has no cp315 wheel and does
not build from source on the runners, as in the earlier runs.

## 2026-10-18: the fourth fix round (maintainer decisions) on GitHub Actions

Three `test.yml` dispatches, one per branch, each with the other components at their
masters as of 10:20 UTC (after the 23 merges of 2026-10-18): labscript
`pylab-import-and-shared-triggers` (8f6ead7) as run [39119010476](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39119010476);
runmanager `zip-length-check` (2ae94b1) as run [39119016142](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39119016142);
blacs `close-during-shot` (d67dbe4) as run [39119021481](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39119021481).
The 25 jobs of each run passed every step. The pull requests labscript #130, runmanager
#137 and blacs #131 were opened on these results. The labscript branch removes the pylab
star import; the example experiment, the runviewer parsers and the four applications
work without it. The harness does not close BLACS through its window, so the blacs
change was checked separately with fake device tabs (the pull request describes it).

## 2026-10-18: the third fix round (review Part 2 bugs) on GitHub Actions

Seven `test.yml` dispatches, one per branch pushed on 2026-10-18 for the REVIEW.md Part 2
bugs, each with the other components at their masters as of 03:45 UTC: blacs `part2-bugs` (634f0cc) (on `queue-fixes-and-defaults`, the #129 branch) as run [39094671210](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39094671210); labscript-devices `part2-software-bugs` (9c03f2c) (on `prawnblaster-and-esrpro500-fixes`, the #153 branch) as run [39094702770](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39094702770); lyse `part2-bugs` (74f1968) (on `filebox-signals-and-pandas3`, the #146 branch) as run [39095000278](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39095000278); labscript-utils `part2-bugs` (9c10631) (on `apparatus-name-check`, the #134 branch) as run [39095065484](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39095065484); runviewer `part2-bugs` (13c39f6) (on `qt6-check-states`, the #76 branch) as run [39095202070](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39095202070); labscript-c-extensions `resample-nout` (c47656d) as run [39095204228](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39095204228); runmanager `part2-bugs` (da0fd6b) (on `check-states-and-preparse-recovery`, the #135 branch) as run [39095349356](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39095349356). The 25
jobs of each run (Ubuntu and Windows, Python 3.11 to 3.14, PySide6, PyQt6 and PyQt5,
plus the Ubuntu Python 3.14 PySide6 job with `numpy<2.5`) passed every step. The pull
requests blacs #130, labscript-devices #155, lyse #147, labscript-utils #135, runviewer
#77, labscript-c-extensions #14 and runmanager #136 were opened on these results.
With the runmanager branch installed, the runmanager-api check's `globals_diff_shots`
item (marked `KNOWN` for runmanager B7) passes; the marker is removed once runmanager
#136 merges.

## 2026-10-18: the second fix round on GitHub Actions

Nine `test.yml` dispatches, one per branch pushed on 2026-10-18 for the review Part 1
items and the small triaged issues, each with the other components at their masters as
of 03:00 UTC: labscript-utils `apparatus-name-check` (bc59222) (on `release-3.5.0-fixes`, the #133 branch) as run [39091163160](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39091163160); labscript-suite `docs-apparatus-name-and-git` (6a3992c) as run [39091165515](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39091165515); lyse `filebox-signals-and-pandas3` (00a26a1) (on `analysis-loop-and-dataframe-fixes`, the #145 branch) as run [39091201955](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39091201955); labscript `bitfield-dtype` (3516cb1) as run [39091236660](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39091236660); zprocess `curve-support-check` (5b3ad91) as run [39091238876](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39091238876); labscript-devices `nidaqmx-prawndo-prawnblaster-fixes` (b1b477f) as run [39092094838](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39092094838); runmanager `check-states-and-preparse-recovery` (03b54f9) as run [39092298549](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39092298549); runviewer `qt6-check-states` (eec9997) as run [39092300767](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39092300767); blacs `queue-fixes-and-defaults` (a10b3f8) (on `queue-robustness-and-window-geometry`, the #128 branch) as run [39092453984](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39092453984). The 25 jobs of each run (Ubuntu and Windows, Python 3.11 to 3.14,
PySide6, PyQt6 and PyQt5, plus the Ubuntu Python 3.14 PySide6 job with `numpy<2.5`)
passed every step. The pull requests labscript-utils #134, labscript-suite #109, lyse
#146, labscript #129, zprocess #32, labscript-devices #154, runmanager #135, runviewer
#76 and blacs #129 were opened on these results. The NI_DAQmx change in labscript-devices
#154 is not exercised by the harness and needs a test on NI hardware.

## 2026-10-18: the four fix branches on GitHub Actions

Four `test.yml` dispatches, one per branch pushed on 2026-10-18, each with the other
components at their masters as of 02:00 UTC: runmanager `compile-loop-and-remote-fixes`
(854c5da) as run [39088096916](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39088096916), blacs
`queue-robustness-and-window-geometry` (bbe883d) as run
[39088099212](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39088099212), lyse `analysis-loop-and-dataframe-fixes` (455f19b) as
run [39088101471](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39088101471) and labscript-devices
`prawnblaster-and-esrpro500-fixes` (a4a5f6b) as run
[39088103452](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39088103452). The 25 jobs of each run (Ubuntu and Windows, Python 3.11
to 3.14, PySide6, PyQt6 and PyQt5, plus the Ubuntu Python 3.14 PySide6 job with
`numpy<2.5`) passed every step. In the blacs run, the Ubuntu Python 3.14 PySide6 job
reports no traceback in the BLACS output (defect D1) and the `KNOWN` marker for
runmanager B7. The pull requests runmanager #134, blacs #128, lyse #145 and
labscript-devices #153 were opened on these results.

## 2026-10-18: the four fix branches on the local machine, Python 3.14, PySide6

The harness ran on this machine (Python 3.14.8, PySide6, NumPy 2.5.4, Linux) with the
branches made on 2026-10-18 installed from the clones: runmanager
`compile-loop-and-remote-fixes` (854c5da), blacs `queue-robustness-and-window-geometry`
(bbe883d), lyse `analysis-loop-and-dataframe-fixes` (455f19b) and labscript-devices
`prawnblaster-and-esrpro500-fixes` (a4a5f6b), with the other components at their masters
as of 2026-10-17. All eight steps passed (versions, profile, imports, compile, lyse,
runviewer, runmanager-api, apps). The BLACS output of the `apps` step has no traceback:
the first-launch `KeyError: 'window_xpos'` (defect D1) is gone with the blacs branch. The
remaining `KNOWN` markers are runmanager B7 (`globals_diff_shots`) and D8
(`lyse.spinning_top`, fixed by the unmerged lyse #144). The component table in the
report listed stale commits because `install` did not record what it installed (fixed
in the harness on 2026-10-18: the commits are now recorded at install time); the commits
above are the branch heads that were installed.

The GitHub Actions runs on the same branch heads are in the entry above.

## 2026-10-18: labscript-c-extensions master builds after #12 and #13

Both `release.yml` runs on labscript-c-extensions `master` passed on all four runners
(ubuntu-latest, windows-2022, macos-latest, macos-15-intel): run
[39080269759](https://github.com/labscript-suite/labscript-c-extensions/actions/runs/39080269759)
on a1e99dc (the #12 merge, the D7 workflow fix) built 1.3.1.dev4 and run
[39080289833](https://github.com/labscript-suite/labscript-c-extensions/actions/runs/39080289833)
on b0f985d (the #13 merge, the resampler fix) built 1.3.1.dev6. Each uploaded an sdist and
30 wheels to Test PyPI (cp311 to cp315 for manylinux x86_64, musllinux x86_64, macOS
x86_64 and arm64, win32 and win_amd64) and conda packages for every platform to the
Anaconda test label. This is the step 4 wheel set of the release plan, built without a
tag; the final tag will rebuild the same set.

## 2026-10-17: labscript-utils #133 and labscript compiler fixes

**labscript-utils [#133](https://github.com/labscript-suite/labscript-utils/pull/133)**
(head 12f86ac): the harness workflow was dispatched with
`labscript-utils=labscript-suite/labscript-utils@release-3.5.0-fixes` as run
[39033554974](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39033554974):
the 24 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with PySide6, PyQt6 and PyQt5
and the NumPy 2.4 job passed every step; the 6 Python 3.15 jobs failed at "Install the
components" on h5py as before. Locally (Python 3.14.6, h5py 3.16.0, numpy 2.5.4,
PySide6, the branch installed into the harness venv) all eight steps passed, and the
profile that the `profile` step created contains
`app_saved_configs/example_apparatus/runmanager/runmanager.ini` naming the example
experiment. Per-fix checks in the same venv: `h5py.File(path)` with no mode opens the
file read-only after `labscript_utils.h5_lock` is imported (master raises
`ValueError`); a second `close()` does not raise and the kill lock count returns to
zero; with `Lock.acquire` replaced by one that raises, `h5py.File` propagates the
error and the kill lock count is unchanged; `SineAom().fraction_to_base(0)` maps to a
power of 0 (master: -0.068); `setup_logging` with `sys.stdout` and `sys.stderr` set to
`None` returns a logger with the zlog handler and replaces both streams with devnull;
with `tkinter` blocked in `sys.modules`, `labscript_utils.excepthook` imports with a
`UserWarning` and the installed excepthook prints the traceback.

**labscript [#128](https://github.com/labscript-suite/labscript/pull/128)** (head
738bc7a; the run below tested 4549021): the harness workflow was dispatched with
`labscript=labscript-suite/labscript@compiler-fixes` as run
[39034242971](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39034242971):
the 24 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with PySide6, PyQt6 and
PyQt5 and the NumPy 2.4 job passed every step; the 6 Python 3.15 jobs failed at
"Install the components" on h5py as before. Locally (Python 3.14.6, numpy 2.5.4, PySide6, the branch installed into the
harness venv) all eight steps passed. The second commit, 738bc7a (2026-10-18), makes
the final clock tick one period of the slowest clock limit among the pseudoclock and its
clocklines, or twice the longest minimum clock high time if that is longer (REVIEW.md
labscript B8). The `runviewer` check allowed a trace to end at most 1 µs after the stop
time; it now allows one final tick, computed from the clock limits of the fixture's
device classes. With 738bc7a installed into a local harness venv (Python 3.14.8, numpy
2.5.4, PySide6) all eight steps passed on 2026-10-18, and the workflow was dispatched
with the branch as run
[39078500277](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39078500277):
the 24 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with PySide6, PyQt6 and PyQt5
and the NumPy 2.4 job passed every step; the 6 Python 3.15 jobs failed at "Install the
components" on h5py as before. Per-fix checks in the same venv, each in its own
interpreter, with `DummyPseudoclock` and a test `IntermediateDevice` with a 1 MHz clock
limit:

| Check | Result |
|---|---|
| 200 ramps of 1 to 200 µs at a 1 MHz sample rate | 20302 samples, the expected count; the previous formula gives a wrong tick count for 97 of the 200 |
| six pulses of exactly one clock period at t = 0.1 to 3.3 s | compile |
| `ao.ramp(0, 1, ...); ao.ramp(2, 1, ...); ao.constant(2.5, 7)` | `LabscriptError`: collides with a ramp |
| `do.go_high(1 - 0.5e-6); wait('w', 1)` | `LabscriptError`: too soon before a trigger |
| `do.go_high(1 - 2e-6); wait('w', 1)` | compiles |
| `AnalogOut('sin', ...)` | `LabscriptError`: already exists in the Python namespace |
| outputs named `worker`, `gui`, `connection`, `name`, `location`, `kwargs` | accepted |
| shutter with 10 ms delays opened at 5 ms, and a `StaticDigitalOut`, on a secondary PineBlaster (`t0` = 350 ns) | compile |
| `TriggerableDevice(..., parentless=True)` | compiles |
| `StaticDDS` without a gate, `enable()` | `LabscriptError`: does not have a digital gate |
| `StaticDDS` with a gate, `enable()` before `setamp` | gate instruction at t = 0; the caller's `digital_gate` dict unchanged |
| `DDS.pulse` without a gate, with and without a frequency, `print_summary=True` | amplitude 0 at the end of each pulse; summary printed |
| `quantise_to_pseudoclock` of a set | returns a set |
| two `DigitalOut` on `port0/line11` | `LabscriptError` naming both outputs |
| `TriggerableDevice` on a line that has a `DigitalOut` | `LabscriptError` |
| final tick (738bc7a), `DummyPseudoclock` at 10 MHz with a 1 MHz device; a 10 kHz device; a 1 MHz device with an 80 µs minimum clock high time; a device with no clock limit | 1 µs; 100 µs; 160 µs; 100 ns, read back from `PULSE_PROGRAM` |
| two `TriggerableDevice` children of one `Trigger` | accepted |
| two outputs 0.4 µs apart on a 1 MHz clockline | the error ends with "Outputs with an instruction at t=0.5: do1" and names do2 at the second time |
| `exp_ramp` from 1 to 0 with limits (0, 10), and a constant of 10 + 1e-12 | compile; the raw output is within 0 to 10 |
| constant 10.1 and a ramp to 11 with limits (0, 10) | `LabscriptError` with the value, and with the range of values the ramp generated |
| `wait()` with a parentless `TriggerableDevice` and no pseudoclock | `LabscriptError`: requires a pseudoclock |
| the default profile's example experiment | compiles, stop time 2.75 s |

## 2026-10-17: checks for the release sequence step 2 to 4 pull requests

Pull requests [labscript-c-extensions #13](https://github.com/labscript-suite/labscript-c-extensions/pull/13),
[desktop-app #34](https://github.com/chrisjbillington/desktop-app/pull/34),
[qtutils #36](https://github.com/philipstarkey/qtutils/pull/36) and
[qtutils #37](https://github.com/philipstarkey/qtutils/pull/37). The harness workflow
was dispatched with `labscript-c-extensions=pr/13 desktop-app=pr/34 qtutils=pr/36` as
run [39031528312](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39031528312):
the 24 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with PySide6, PyQt6 and PyQt5
and the NumPy 2.4 job passed every step; the 6 Python 3.15 jobs failed at "Install the
components" on h5py as before.

**Resampler** (`tools/resample_check.py`, Python 3.13.16, NumPy 2.5.4, the extension
built from the master and pull request heads with Cython into two venvs):

| Case | master (41c0058) | PR #13 (d80a2a8) |
|---|---|---|
| 100 µs pulse at t=0, 1 s shot, view padded 5 % before t=0 | visible | visible |
| same pulse, 100 paddings from 0.05 % to 5 % | dropped for 69 | dropped for 0 |
| same pulse, view starting at t=0 | visible | visible |
| first data time inside the last output interval (REVIEW.md item 19) | wrote past the end of `y_out` (guard values changed) | guard intact |
| two input times inside the first group of three | first value dropped | kept |
| 50000-point random trace, view from t=0 and zoomed | checksums 9543.146662, 8316.601051 | identical |
| same trace, view padded 5 % | 8800.748370 | 8802.633414 (the first group now carries data) |

Running every case in one process on the master build ended in a segmentation fault;
case by case it ran, with the results above.

**qtutils output box** (`tools/outputbox_check.py`, Python 3.13.16, PySide6 6.12.0,
PyQt6 6.11.0, PyQt5 5.15.11, offscreen platform): text written to the box is displayed,
`clear_output()` empties it and later text is displayed from the start of a line, and
triggering "Clear output" from the open context menu does the same, under all three
bindings. Connecting `clear_output` to `triggered` directly failed under PyQt6 and PyQt5
with `TypeError: OutputBox.clear_output() takes 1 positional argument but 2 were given`;
the pull request connects through a lambda.

**qtutils docs** (Python 3.13.16, Sphinx 9.1.0, no recommonmark installed): the dirhtml
build exits 0 with the three pre-existing warnings (`language = None`, missing
`_static`). In a clone made like Read the Docs makes it (depth 50, one branch), the
setuptools_scm version was 0.1.0.dev88 before `git fetch --unshallow` and
`git fetch --tags` and 4.2.0.dev6 after them.

**desktop-app** (harness venv py3.14, Python 3.14.6, Linux): importing `desktop_app`
from the pull request head loads no `win32*` module, and the five Windows-only
functions in `windows.py` raise `EnvironmentError`. The Windows launcher path is only
covered by the workflow run above.

## 2026-10-17: release tag step on Ubuntu and Windows

`.github/workflows/tag-step-test.yml` in this repository, run
[39028326108](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39028326108):
HEAD tagged `v9.9.9rc1` and `v9.9.9`, then the release workflow's "Ignore tags other than
the pushed tag" step run with the pushed tag given as `REF_NAME=v9.9.9` (`GITHUB_REF_NAME`
cannot be set in a workflow), once under the runner's default shell and once under bash.

| Runner | Shell | Tags deleted | Left at HEAD |
|---|---|---|---|
| windows-latest | default (`pwsh -command`) | `v9.9.9`, `v9.9.9rc1` | none |
| windows-latest | bash | `v9.9.9rc1` | `v9.9.9` |
| ubuntu-latest | default (bash) | `v9.9.9rc1` | `v9.9.9` |
| ubuntu-latest | bash | `v9.9.9rc1` | `v9.9.9` |

This reproduces DEFECTS.md D7 on a Windows runner and shows that `shell: bash` on the step
fixes it; workflow-sandbox #47 and the sync pull requests carry the change.

## 2026-10-17: lyse #142 (spinning_top) with the merged masters, every Qt binding

Run [39027308813](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39027308813),
dispatched with `lyse=pr/142` (a7de833; the same tree is 8a6a5d5 on lyse #144, which replaced #142 on 2026-10-18) and every other component at its master after
the blocker and metadata merges of the day: zprocess e74b638, qtutils 4c9cd95, desktop-app
dc6be4e, labscript-c-extensions 41c0058, labscript-utils 89457f5, labscript 665a73d,
runmanager 264434c, blacs d061535, runviewer 7ea7dc9, labscript-devices 2a2d785,
labscript-suite 4fbc7fc. Ubuntu and Windows, Python 3.11 to 3.15, PySide6, PyQt6 and
PyQt5, plus the `numpy<2.5` job: 31 jobs.

| Jobs | Result |
|---|---|
| 25 jobs: both OSes, Python 3.11 to 3.14, all three bindings, NumPy 2.5.4 (2.4.6 on 3.11), plus the pinned job | all eight steps pass, so the merged masters compile on NumPy 2.5.4 and the lyse branch reads shots and saves results on every binding |
| 6 jobs: Python 3.15 | install fails on h5py as before |

The run was dispatched before the commit that adds the `spinning_top` checks to the
harness `lyse` step reached `main`, so those checks did not run here; they were run by hand
in the local venvs, where lyse master reports KNOWN and the branch reports FIXED for both.

## 2026-10-17: zprocess v2.28.0rc2 release run, D7 fix confirmed

Tag `v2.28.0rc2` pushed at 11:32 UTC on f5f4685 of chrisjbillington/zprocess, the head of
`master` after #31, which differs from the rc1 commit only by `shell: bash` on the two
"Ignore tags other than the pushed tag" steps.
[Run 39029064804](https://github.com/chrisjbillington/zprocess/actions/runs/39029064804)
built 2.28.0rc2 on ubuntu-latest, windows-2022, macos-latest and macos-15-intel; the
Windows step ran under Git Bash and deleted no tag. Published: the sdist and pure wheel
to PyPI, the GitHub pre-release, and conda packages for linux-64, osx-64, osx-arm64 and
win-64 for Python 3.11 to 3.15 to the Anaconda main label. The win-64 packages missing
from rc1 are therefore present at 2.28.0rc2.

## 2026-10-17: zprocess v2.28.0rc1 release run

Tag `v2.28.0rc1` pushed at 10:41 UTC on e74b638 of chrisjbillington/zprocess, the head of
`master` and `maintenance/2.28.x`, with the release workflow synced from
rpanderson/workflow-sandbox #46 (zprocess PR #30).

| Push | Run | Version built | Published |
|---|---|---|---|
| branch `maintenance/2.28.x` at e74b638 | [39025269576](https://github.com/chrisjbillington/zprocess/actions/runs/39025269576) | 2.28.0.dev11 on all four runners | Test PyPI and the Anaconda test label (skipped as already existing from the master run) |
| tag `v2.28.0rc1` | [39025867956](https://github.com/chrisjbillington/zprocess/actions/runs/39025867956) | 2.28.0rc1 on ubuntu-latest, macos-latest and macos-15-intel; **2.28.0.dev11 on windows-2022** | PyPI (sdist and pure wheel, with attestations), GitHub pre-release with the sdist attached, Anaconda main label for linux-64, osx-64 and osx-arm64 (Python 3.11 to 3.15); the win-64 2.28.0.dev11 packages were skipped as already existing under the test label |

The Windows job's "Ignore tags other than the pushed tag" step logged
`Deleted tag 'v2.28.0rc1' (was e74b638)`: it ran under PowerShell, where
`${GITHUB_REF_NAME}` is empty. Recorded as defect D7 in `DEFECTS.md`. The Anaconda main
label therefore has no win-64 zprocess 2.28.0rc1 packages.
## 2026-10-17: zprocess maintenance/2.28.x branch build

Branch `maintenance/2.28.x` pushed at e74b638 (the head of master) for release sequence
step 1. [Run 39025269576](https://github.com/chrisjbillington/zprocess/actions/runs/39025269576)
of `release.yml`: the configure job and the four build jobs (ubuntu-latest, windows-2022,
macos-latest, macos-15-intel) pass, the sdist, pure wheel and conda packages are
published to TestPyPI and the Anaconda test label, and the three release jobs (GitHub
release, PyPI, Anaconda) are skipped, as they should be for an untagged push. The
`v2.28.0rc1` tag is a local task (`LOCAL-TASKS.md`).

## 2026-10-17: fixes for the remaining release pull requests

Maintainer fix commits for the pull requests of `RELEASE-PLAN.md` section 4.3 that were
still open after labscript-devices #110 and lyse #132 merged. Each is one commit on the
pull request head, stored in `patches/` with a `LOCAL-TASKS.md` row, because every
branch is on a contributor's fork. Each fix was checked in its own venv (Python 3.14.6,
NumPy 2.5.4, h5py 3.16.0, PySide6 6.12.0, every component installed from its clone at
the state of the fix branch) on the Ubuntu container.

**labscript-utils #117, example analysis script** (`example-117-fixes`, patch
`labscript-utils-117-example-analysis-fixes.patch`). The script as submitted fails on
its first statement after the imports with `AttributeError: module 'lyse' has no
attribute 'spinning_top'` when run the way lyse's analysis subprocess runs it (a
`__main__` module with `lyse.utils.worker.path` set to the shot). The review's claim
that `save_result` of a dict of arrays raises `TypeError` is wrong: it stores the dict
JSON-encoded as a 5.6 kB group attribute (`PR-REVIEW.md`, correction). After the fix:
the harness `profile`, `compile` and `lyse` steps pass with the branch installed; the
script run as lyse runs it finishes against the compiled example shot and saves the
`analog_out` (float64, 254 values, 0 to 1) and `digital_out` (int8, 254 values) datasets
and the `analog_out_max` attribute (1.0) under `results/example_analysis_script`;
`lyse.Run` reads them back and `get_dataframe_from_shot` has the
`('example_analysis_script', 'analog_out_max')` column; the deprecated standalone mode
with the shot path as an argument also runs. The branch merges cleanly into master.

Draft comment for #117: "Thanks for this; a runnable example with the dummy devices is
useful. Two defects before merging. `lyse.spinning_top` on line 8 no longer exists: lyse
moved it to `lyse.utils.worker` in 3.3.0rc1, so the script raises `AttributeError` as
soon as lyse runs it. `lyse.path` is the current shot inside lyse and `None` outside it.
`run.save_result('foobar', result)` with a dict of two arrays does run, but it JSON-encodes
the 254-element arrays into a group attribute and the lyse dataframe then gets nested
series in its cells; `save_result_array` for the arrays and `save_result` for a scalar is
the intended use. The x axis is labelled `time (ms)` but `OUTPUTS` has one row per clock
tick, and `run_globals`, `pulse`, the `np.array()` wrappers and the 'image processing'
comment are left over from the camera example. I have pushed a commit with these changes
to this branch."

**labscript-devices #126, AD9959 DDS Sweeper** (`ad9959-126-fixes`, patch
`labscript-devices-126-ad9959-fixes.patch`). Firmware behaviour checked in the
dds-sweeper repository (QTC-UMD/dds-sweeper d56ff74, firmware 0.4.0): `main()` sets the
Pico system clock to 125 MHz; `setclock` mode 0 sets it to the given frequency; mode 1
(external reference) only sets the AD9959 reference and does not change the Pico clock.
So `clock_limit`, which divided `ref_clock_frequency` by the Pico cycles per instruction,
was wrong for an external reference; it now divides the Pico system clock, 125 MHz when
the reference is external. Checks on the fixed branch: the harness `profile`, `imports`
and `compile` steps pass; an experiment with a `DummyPseudoclock`, an
`AD9959DDSSweeper(dynamic_channels=2)`, `DDS` children on channels 0 and 1 and `StaticDDS`
children on channels 2 and 3, with changes at 0, 1, 2 and 3 ms and stop at 4 ms, compiles
through runmanager; `runviewer.__main__.Shot` loads the shot with no device failure and
the rewritten parser gives twelve traces with one point per clock tick at 0 to 4 ms and
the programmed values (10 and 11 MHz, amplitudes 0.5 and 0.6, phase 0 then 90 degrees on
channel 0; constant 30 MHz, 0.25, 45 degrees on static channel 2) to within the DDS
quantisation (0.116 Hz, 1/1023, 360/16384); a static-only experiment does the same;
`sweep_mode=1` raises `LabscriptError` at construction; `clock_limit` is 250 kHz,
166.7 kHz and 100 kHz for one, two and four dynamic channels at the default clock and
stays at 166.7 kHz for two channels with an external 100 MHz reference (the old code
gave 133.3 kHz for an internal 100 MHz reference, which is correct, and would have given
333 kHz for an external 250 MHz reference, which is not); the worker, tab, parser and
`register_classes` modules import under offscreen Qt with deprecation warnings as
errors. The worker was not run: no hardware. Noticed and not fixed:
`AD9959DDSSweeperInterface.get_freqs` compares `readline().decode()` with `"ok"` without
stripping the newline, so it would never terminate; the worker does not call it. The
branch merges cleanly into master.

Draft comment for #126: "I have pushed a follow-up commit to this branch. The runviewer
parser could not run: `DDSs` was undefined, `np.float` no longer exists, the assignments
used `'%d_freq'` field names while the dtype declared `freq%d`, and the traces were
passed to `add_trace` without a time axis. It is rewritten after the NovaTechDDS9M
parser and shows the dynamic and static channels at the clockline ticks. `clock_limit`
divided `ref_clock_frequency` by the Pico cycles per instruction, but the firmware sets
the Pico system clock from that frequency only in `setclock` mode 0; with
`ref_clock_external=1` the Pico stays at 125 MHz, so the limit is now computed from the
Pico system clock and the docs say so. Also: `sweep_mode != 0` is rejected in the
constructor instead of at `setb` time, the remaining `assert`s in `blacs_workers.py`
raise `LabscriptError`, `transition_to_manual` waits a fixed 5 s for `STOPPED` rather
than 1000 status queries, and the `.. note::` in the docs is indented so it renders.
Verified by compiling a DummyPseudoclock experiment with two DDS and two StaticDDS
channels and loading it in runviewer. I have no hardware to run the worker, so please
check the worker changes on your setup."

**labscript-devices #144, Andor fixes** (`andor-144-fixes`, patch
`labscript-devices-144-andor-fixes.patch`). The Andor SDK is a Windows DLL, so the
checks are static. `andor_utils.py` from the PR head fails to byte-compile on Python
3.11.15 (`SyntaxError: f-string: unmatched '['`); after the fix the three changed files
byte-compile on 3.11.15 and 3.14.6. Importing `andor_utils` from the fixed branch stops
only at loading the missing `atmcd64d.dll`; `AndorSolis.blacs_workers` imports. After the
fix the pull request no longer touches `IMAQdxCamera/blacs_workers.py`, merges cleanly
into master and no longer conflicts with #148 (the PR head conflicts with #148 on both
worker files). Confirmed in `andor_capabilities.py` that `camera_type.get_type` returns
names such as `IXONULTRA`, so the PR's `'IXION ULTRA'` and `'IXON ULTRA'` comparisons
never matched.

Draft comment for #144: "Thanks for these fixes; the cooldown-before-EM-gain ordering,
the `GetKeepCleanTime` fallback and the `SetIsolatedCropMode` fallback are all needed. I
have pushed a commit on top of your branch that fixes four problems. The `print` in
`setup_acquisition` nested the string's own quote inside the f-string, which is a
SyntaxError before Python 3.12 and made `andor_utils` unimportable on 3.11. The model
comparisons used `'IXION ULTRA'` and `'IXON ULTRA'`, but `camera_type.get_type` returns
names like `'IXONULTRA'`, so an iXon Ultra never took the `SetIsolatedCropModeEx` branch;
it is now `'IXONULTRA' in self.model`. The EM gain range check used strict comparisons
and rejected the endpoints; it is now inclusive. The single-mode branch uses
`images.extend(list(downloaded))` like the other branches. As you offered, the fast
acquisition setup, the semaphore and the IMAQdx worker change are left for a separate
pull request: the semaphore is only released in single mode, so `transition_to_buffered`
blocks forever in kinetic-series and fast-kinetics modes, and both changes conflict with
the TriggerableCamera refactor in #148. The debug prints of the gain range and
attributes are also removed."

**prawn_digital_output #23, testing notebook** (`testing-notebook-23-fixes`, patch
`prawn_digital_output-23-testing-notebook-fixes.patch`). No hardware here; the notebook
parses as JSON and validates as nbformat 4.5, is 9 KB after the outputs are stripped
(192 KB before), every code cell compiles and `KeysightScope.py` byte-compiles. The
`send()` helper extracted from the notebook and called with a stand-in `serial` module
in which `Serial()` raises prints the original error and returns an empty string; the
PR head's version raises `AttributeError: 'NoneType' object has no attribute 'close'`
instead. The branch merges cleanly into main.

Draft comment for #23: "I pushed a small follow-up commit to this branch. It strips the
notebook outputs (the file drops from 192 KB to 9 KB, so re-running it no longer
produces a diff), moves `PORT`, the scope's VISA resource pattern and the two image
flags into a commented parameters cell and passes the pattern to `KeysightScope`, and
resets the kernelspec from the machine-specific `Pico` kernel to `python3`. It also
changes the `if SHOW_IMAGES: ... elif SAVE_IMAGES:` blocks to two independent `if`s so
a screenshot can be shown and saved in the same run, and makes the `finally` in `send()`
only call `conn.close()` when `serial.Serial()` succeeded, so a failed port open reports
the original error instead of an `AttributeError`. A first markdown cell lists the
packages needed. I could not run the hardware steps; the notebook validates and every
cell compiles."

**labscript-devices #87, background subtraction** (`imaqdx-87-fixes`, patch
`labscript-devices-87-imaqdx-background-fixes.patch`). Run offscreen with pyqtgraph 0.14.0
on PySide6, with the PR branch merged with master because the PR's base still had
`QtGui.QApplication` in `handler`. On the PR as submitted, "Set background" with no frame
raises `AttributeError: 'NoneType' object has no attribute 'swapaxes'` and a frame of a
different height and width raises `ValueError` in the main thread; a 2-D background and a
3-D post-shot stack broadcast and display correctly, contrary to the review. After the
fix, a real `ImageReceiver` with a real `pg.ImageView` and the tab's buttons from the `.ui`
file was driven through `handler()`: set-background with no frame returns False and leaves
the buttons; a 120 by 100 frame displays; set-background then shows zeros and swaps the
buttons; an 80 by 90 frame displays unsubtracted; a same-shape frame displays as the
difference; a stack of three has the background subtracted from each image; with the
stack as background a 2-D frame and a stack of two display unsubtracted and the same stack
shows zeros; the autolevels button makes the levels follow the frame; clear restores the
raw frame and the buttons. One frame sent over ZMQ from a REQ socket as the worker sends
it is answered `ok` and displayed. The same script passes on master with both the #87 and
#63 fixes merged.

Draft comment for #87: "I have pushed a small follow-up commit to this branch that fixes
the two cases zakv found. In `ImageReceiver`, `set_bg_image()` before any frame had
arrived stored `None` as the background and `update_image()` then failed on `swapaxes`;
it now returns False with no change, and the tab leaves the buttons as they are. A
background with a different shape from the incoming frame raised `ValueError` in the
main thread after the worker had been sent `ok`; the subtraction now happens only when
the background shape matches the frame's trailing dimensions, so a 2-D background is still
subtracted from each image of a post-shot stack and anything else is displayed
unsubtracted. The 'Set background' tooltip now says the subtraction affects the display
only. Tested offscreen with pyqtgraph 0.14.0 on PySide6; the branch merges cleanly with
master and with #63."

**labscript-devices #63, restore display settings** (`imaqdx-63-fixes`, patch
`labscript-devices-63-imaqdx-restore-fixes.patch`). `hasattr(pg.ImageView, 'getLevels')`
is False, but `ImageView.__init__` binds `getLevels` from the histogram onto each instance
in pyqtgraph 0.10.0, 0.11.0, 0.12.0, 0.13.0, 0.14.0 and master (sources read on GitHub),
so the author's `self.image.getLevels()` works and is kept; the review's claim that
`get_save_data` raises is wrong (`PR-REVIEW.md`, correction). Running the save and
restore round trip repeatedly on the PR as submitted shows the view range growing by
pyqtgraph's default padding each time (31 to 103, then 23.8 to 110.2, then 15.16 to
118.84); with `padding=0` the ranges round-trip exactly. After the fix, the tab's own
`get_save_data` and `restore_save_data` run on a stub holding a real `pg.ImageView`: with
no image only the original keys are saved; after a frame, zoom, pan, auto-range on y and
levels 250 and 2500 the saved dict survives `repr` and `eval` with Python float and bool
types, a fresh view restored from it has the same `targetRange`, `autoRangeEnabled`
`[False, 1.0]` and levels `(250.0, 2500.0)`, the first frame displayed afterwards keeps
them, a 3-D stack shape saves and restores, and save data without the new keys restores
without error. Zero images of 2-D and 3-D shape display without the nonzero-pixel
workaround on 0.14.0 (fixed in pyqtgraph 0.11.0, pull request 767). Passes on the branch
merged with master and on master with both the #63 and #87 fixes.

Draft comment for #63: "Thanks for this; it works as described with current pyqtgraph
(`ImageView.getLevels()` is a per-instance forward to the histogram, present in 0.10
through 0.14). Running the save and restore round trip repeatedly showed one problem:
`view_box.setRange(xRange=..., yRange=...)` in `restore_save_data` applies pyqtgraph's
default padding, so the saved range grows by about 20 % on every BLACS restart;
`padding=0` fixes it and the ranges then round-trip exactly. I have pushed a follow-up
commit with that change; it also converts the saved ranges and levels to Python floats
(BLACS restores save data with `eval`, which fails on numpy 2's `np.float64(...)` repr)
and drops the one-nonzero-pixel workaround, since pyqtgraph 0.11 fixed that. Merges
cleanly with master and with #87."

**Not done from the cloud.** The fix branches could not be pushed to the upstream
repositories (the proxy refused the pushes), so the test workflow has not run on them.
`LOCAL-TASKS.md` has the dispatches to run with the pull request refs once the fixes are
on the pull request branches. Also found: the camera tab's Copy button uses
`QtGui.QApplication` and fails under Qt6 bindings (`DEFECTS.md` D6).

## 2026-10-17: lyse #132 data-group attributes in the dataframe

lyse PR #132 (head 6066df4) merged into lyse master 01246cf, plus commit 724de8c, which
reads the `data/` groups before the `results/` groups and merges each group's attributes
into `row[name]` with `setdefault(...).update(...)` instead of assigning (local branch
`pr132-work` in `repos/lyse`; pushed upstream as `data-attributes-132-fix`). Python
3.14.6, pandas 3.0.6, h5py 3.16, with the clone on `PYTHONPATH`. A script writes a shot
file with `results/fr` (attributes `fitted=42.0`, `shared='from results'`), `data/fr`
(`raw=7`, `shared='from data'`), `data/other` (`temperature=300.0`) and a dataset
`data/waits`, then calls `get_nested_dict_from_shot` and `get_dataframe_from_shot`.

| Version | `row['fr']` | dataframe columns under `fr` and `other` |
|---|---|---|
| master 01246cf | `{'fitted': 42.0, 'shared': 'from results'}`; `data/` not read | `(fr, fitted)`, `(fr, shared)` |
| PR head 6066df4 | `{'raw': 7, 'shared': 'from data'}`: the results attributes are lost | `(fr, raw)`, `(fr, shared)`, `(other, temperature)` |
| with 724de8c | `{'raw': 7, 'shared': 'from results', 'fitted': 42.0}` | `(fr, fitted)`, `(fr, raw)`, `(fr, shared)`, `(other, temperature)` |

The dataset `data/waits` gives an empty `row['waits']` in both the PR head and the fix,
and no column.

**GitHub Actions:** dispatch with `lyse=data-attributes-132-fix` and every other
component at master,
[run 39022914882](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39022914882).
The 24 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with PySide6, PyQt6 and PyQt5
pass all eight steps, as does the `numpy<2.5` job; the six Python 3.15 jobs fail at the
h5py build as before. The fix commit is cherry-picked onto the PR head 6066df4 as
001df5f (local branch `pr132-head` in `repos/lyse`); that branch merged with master
01246cf has the same tree as 724de8c, so the run covers it.

## 2026-10-17: labscript-devices #110 Windfreak SynthHD

labscript-devices PR #110 (head 52f74fa) merged into master 2183314, plus one commit with
the four fixes from the review (local branch `pr110-work` in `repos/labscript-devices`,
0593f45; not pushed): `raise` on the channel-range `LabscriptError`, `self.name` in
`enable_output`, a `quantity` argument to `validate_data` so the message names the
quantity and unit, and `NI_DAQmx.models` in the docs example. Python 3.14.6, NumPy
2.5.4, labscript 665a73d, with the clone on `PYTHONPATH` in front of the installed
labscript-devices. A script compiles a connection table with a `WindfreakSynthHDPro`,
two `StaticDDS` children on `channel 0` and `channel 1`, and `enable_output(0)`; the
`windfreak` package is not needed for compilation.

| Case | PR head 52f74fa | With the fixes |
|---|---|---|
| two channels, 1 GHz at 0 dBm and 90 degrees, 2 GHz at -10 dBm | `STATIC_DATA` row `freq0=1e9, freq1=2e9, amp0=0.0, amp1=-10.0, phase0=90.0, phase1=0.0, gate0=True, gate1=False` | same |
| third child on `channel 2` | `ValueError: no field of name freq2` from numpy, after the unraised `LabscriptError` | `LabscriptError: Static RF:wf_b has invalid connection string. Only 'channel 0' or 'channel 1' is allowed.` |
| amplitude 25 dBm (limit 20) | `LabscriptError: ... can only have frequencies between -4.000000E+01Hz and 2.000000E+01Hz, 25.0 given` | `LabscriptError: Static RF wf_a can only have amplitudes in dBm between -40.0 and 20.0, 25.0 given` |
| `enable_output(5)` | `AttributeError: 'WindfreakSynthHD' object has no attribute 'device'` | `LabscriptError: Channel 5 is not a valid option for wf2.` |

The module imports with `-W error::DeprecationWarning`. The docs example's import path
`labscript_devices.NI_DAQmx.Models.NI_USB_6343` does not exist; the directory is
`models`.

**GitHub Actions, PR head alone:** the dispatch with `labscript-devices=pr/110`,
[run 39021953009](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39021953009),
fails the `imports` step in every job because the harness imports
`labscript_devices.PrawnDO.labscript_devices`, which master gained after this branch was
made; the branch is 68 commits behind master. The other steps pass in the `numpy<2.5`
job. A head that is behind master has to be tested merged with master, so the merged
branch with the fixes was pushed to labscript-suite/labscript-devices as
`windfreak-110-fixes` (0593f45) and dispatched:
[run 39022423569](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39022423569),
every other component at master. The 24 jobs on Ubuntu and Windows for Python 3.11 to
3.14 with PySide6, PyQt6 and PyQt5 pass all eight steps, as does the `numpy<2.5` job; the
six Python 3.15 jobs fail at the h5py build as before. The harness should derive its
module list from the installed package rather than a fixed list (`harness/suite.py`,
`imports` step).

## 2026-10-17: blacs #123 plugin-loading fixes

blacs PR #123 (head 4ec904f, three commits) merged into blacs master bc3fd1f, with one
commit on top that shortens the two added comment blocks (local branch `pr123-work`,
f1aea3f, in `repos/blacs`; not pushed). Every other component at its upstream master
of 09:00 UTC. Python 3.14.6, PySide6, NumPy 2.5.4, on the Ubuntu container.

**Harness:** all eight steps pass (versions, profile, imports, compile, lyse,
runviewer, runmanager-api, apps). BLACS starts, loads the `connection_table`,
`general` and `theme` plugins and runs for five seconds without a traceback.

**The `[DEFAULT]` collision, reproduced.** The active labconfig was given
`connection_table = %(labscript_suite)s/userlib/connection_table.py` under `[DEFAULT]`
and the `connection_table = True` line was removed from `[BLACS/plugins]`, which is the
state of a labconfig that has never had the flag written.

| `blacs/plugins/__init__.py` | `import blacs.plugins` |
|---|---|
| master bc3fd1f | raises `ValueError: Not a boolean: /root/labscript-suite/userlib/connection_table.py` from `configparser`, so BLACS cannot start |
| PR #123 | logs `WARNING BLACS.plugins: Plugin 'connection_table' shares its name with a labconfig [DEFAULT] key; using the default enabled state.` and imports; the plugin is enabled, as it is in `default_plugins` |

The `has_option` change in the same commit does not change behaviour: CPython's
`RawConfigParser.has_option` returns true for inherited `[DEFAULT]` keys, as `items()`
does. The `try/except ValueError` block is the fix.

**GitHub Actions:** dispatch of `.github/workflows/test.yml` with `blacs=pr/123` (head
4ec904f, without the comment commit) and every other component at its upstream master,
[run 39021000880](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39021000880),
started 09:24 UTC. The 24 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with
PySide6, PyQt6 and PyQt5 pass all eight steps, as does the `numpy<2.5` job; the six
Python 3.15 jobs fail at the h5py build as before.

**Draft comment for the PR**, to post once approved:

> Reviewed for the Python 3.11 to 3.15 release. All three changes are correct and
> reproduce as described:
>
> - With `connection_table = <path>` under `[DEFAULT]` and no `connection_table` flag in
>   `[BLACS/plugins]`, `import blacs.plugins` on master raises `ValueError: Not a
>   boolean` from `configparser`; on this branch it logs the warning and BLACS starts.
> - `str.strip('.h5')` in `compile_and_restart.py` removes any trailing `.`, `h` or `5`
>   characters, so the `os.path.splitext` change (third commit, not in the description)
>   is a real fix too.
>
> Two small things before merging:
>
> 1. `has_option()` also returns true for inherited `[DEFAULT]` keys (CPython
>    `RawConfigParser.has_option` checks `self._defaults` as well as the section), so
>    the change from the `items()` membership test is fine but is not part of the fix;
>    the `try/except ValueError` block is. The description's "asks the question
>    directly" sentence should go.
> 2. The two comment blocks describe the alternative that was not taken. Suggested
>    replacements: in `plugins/__init__.py`, "The section inherits the labconfig
>    `[DEFAULT]` keys, so a plugin with the same name as one of them reads that key's
>    value here. An option set in the section itself overrides the inherited value." In
>    `__main__.py`, "Call `plugin_setup_complete` once, with the arguments its signature
>    accepts."
>
> The branch merged with master passes the suite's end-to-end checks on Python 3.14 with
> PySide6 (install, import, compile, lyse, runviewer parsers, runmanager API, application
> start-up) and is being run on Ubuntu and Windows for Python 3.11 to 3.14 with PySide6,
> PyQt6 and PyQt5.

## 2026-10-17: master branches after the blocker merges, every Qt binding

Dispatch of `.github/workflows/test.yml` with no refs, so every component at its
upstream default branch, after the last of the blocker pull requests merged (blacs #125
at 08:44 UTC). [Run 39019282114](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39019282114),
started 08:57 UTC. Commits: labscript 665a73d, labscript-utils 89457f5, labscript-devices
2183314, blacs bc3fd1f, lyse 01246cf, runmanager 264434c, runviewer 7ea7dc9,
labscript-suite 4fbc7fc, labscript-c-extensions 41c0058, zprocess e74b638, desktop-app
dc6be4e, qtutils 4c9cd95. Ubuntu and Windows, Python 3.11 to 3.15, PySide6, PyQt6 and
PyQt5, plus the `numpy<2.5` job: 31 jobs.

| Jobs | Result |
|---|---|
| 24 jobs: both OSes, Python 3.11 to 3.14, all three Qt bindings | all eight steps pass |
| Ubuntu 3.14 PySide6 `numpy<2.5` | all eight steps pass |
| 6 jobs: Python 3.15 on both OSes, each binding | install fails building h5py 3.16.0 from source, as before; nothing else runs |

This is the first run of the master branches that compiles a shot on NumPy 2.5: the
previous master run (below) failed at the compile step on every job without the
`numpy<2.5` pin. Jobs took about two minutes on Ubuntu and three to five minutes on
Windows.

## 2026-10-17: version specifiers and development versions

Checked with `packaging` 26.3 on Python 3.14.6, the library that pip uses for version
matching: `3.5.0.dev12`, `3.4.1.dev3` and `3.5.0rc1` do not satisfy `>=3.5.0`, with
pre-releases excluded or allowed; `3.5.0` does. A master checkout of a component builds
as the next minor version with a `.devN` suffix, so the raised pins in runmanager #131
and labscript-suite #106 cannot be met by source installs or release candidates of the
pinned packages, only by their final releases. Released versions on PyPI on this date:
labscript 3.4.2, labscript-utils 3.4.3, labscript-devices 3.3.0, blacs 3.2.3, lyse
3.3.0, runmanager 3.3.0, runviewer 3.2.4, labscript-suite 3.3.0.

## 2026-10-17: zprocess #28 on Windows 11, BLACS restart from a console

zprocess PR #28 (head 81b1b10) on Windows 11 Pro build 26200 with Windows Terminal
1.24.12741.0, Windows PowerShell 5.1 (PSReadLine 2.0.0) and cmd.exe. The labscript
environment is the machine's Python 3.12.7 install: blacs 3.2.3, labscript-utils 3.4.1,
labscript 3.4.0, labscript-devices 3.3.0, runmanager 3.3.0, qtutils 4.0.0 on PyQt5
5.15.11, NumPy 2.4.2, h5py 3.15.1, pywin32 311, with zprocess 2.27.0 before and the PR
branch (version 2.28.0.dev5) after. One run used a Python 3.14.3 venv with blacs 3.2.3,
labscript-utils 3.4.3, PyQt6 6.11.0, NumPy 2.4.6 and zprocess 2.27.1. The connection
table is the default profile's `example_apparatus` with the dummy devices. In each run
BLACS was started with the `blacs` command, the connection table was recompiled from
the Connection Table menu (which runs the runmanager batch compiler) and "Restart BLACS"
was pressed in the recompile dialog. A `sitecustomize` hook on `PYTHONPATH` recorded
the start, the exit and any unhandled exception of every Python process to a file, and
a helper attached to the console of the running processes and read the console input
mode with `GetConsoleMode`.

| Console | Shell | zprocess | Result |
|---|---|---|---|
| Windows Terminal | cmd.exe | 2.27.0 | BLACS restarts |
| Windows Terminal | PowerShell | 2.27.0 | the relaunched process exits at `import labscript_utils` with `pywintypes.error: (87, 'SetConsoleMode', 'The parameter is incorrect.')`, the traceback of zprocess #27; the BLACS log ends with "relaunching BLACS after quit" |
| Windows Terminal | PowerShell | 2.27.1, Python 3.14 venv | BLACS restarts, twice (timing, see below) |
| Windows Terminal | PowerShell | PR #28 | BLACS restarts, twice; no exception recorded; input mode of the restarted BLACS 0x1a4, quick-edit off |
| classic console (`conhost.exe`) | cmd.exe | PR #28 | BLACS starts and the input mode changes from 0x1f7 to 0x1b7, quick-edit off; BLACS restarts with mode 0x1a7, quick-edit off; after BLACS exits the mode is 0x1e7, quick-edit on |

Cause, found with a script that calls `disable_quick_edit`, relaunches itself as BLACS
does (`Popen([sys.executable] + sys.argv)`, then exits) and calls `disable_quick_edit`
again in the child:

- While Windows PowerShell waits at its prompt, the console input mode is 0x1e4:
  `ENABLE_ECHO_INPUT` set and `ENABLE_LINE_INPUT` clear. cmd.exe leaves 0x1e7 at its
  prompt. `disable_quick_edit` adds `ENABLE_EXTENDED_FLAGS` and clears
  `ENABLE_QUICK_EDIT_MODE`, so after PowerShell it asks for 0x1a4.
- `SetConsoleMode` rejects every input mode that has `ENABLE_ECHO_INPUT` without
  `ENABLE_LINE_INPUT`, which its documentation requires: from a cmd.exe console it
  accepted 0x1f7, 0x1b7, 0x1e7, 0x1a7, 0x1a6 and 0x1a0 and returned error 87 for 0x1e4,
  0x1a4 and 0x1a5.
- With the child waiting 3 s before `disable_quick_edit`, so that the prompt has
  returned: from PowerShell, zprocess 2.27.1 raised error 87 in 3 of 3 runs and the PR
  branch returned in 3 of 3; from cmd.exe no run failed on any version. Without the
  wait, 2.27.0 and 2.27.1 failed in 4 of 7 runs from PowerShell. The failure also
  occurred in a classic `conhost.exe` window with PowerShell and never in Windows
  Terminal with cmd.exe, so the ConPTY console is not the cause. Python 3.12 and 3.14,
  and a venv or the system install, made no difference in the script.
- The two successful restarts of the 3.14 venv on 2.27.1 are consistent with timing:
  there the venv launcher process exited one second after the relaunched BLACS started,
  whereas in the system install the launcher exited in the same second, so the prompt
  with its 0x1e4 mode may not be back yet when the relaunched process runs
  `disable_quick_edit`. Plausible, not verified.
- After the failing call `GetConsoleMode` returns 0x1a4, so quick-edit is off in the
  relaunched process whether or not the call raised.

The comment that PR #28 adds attributes the failure to ConPTY consoles such as Windows
Terminal; it should name the console mode that PowerShell leaves at its prompt instead,
for example: "The console rejects the mode. This happens when the process was relaunched
from a PowerShell prompt: while PSReadLine waits for input it leaves ENABLE_ECHO_INPUT
set without ENABLE_LINE_INPUT, and SetConsoleMode rejects that combination."

Posted on the PR on 2026-10-17 as
[a comment](https://github.com/chrisjbillington/zprocess/pull/28#issuecomment-6231503544);
the PR description was updated to the same cause, and commit 256ac43 on the branch
rewords the comment in the `except` branch, with no change in behaviour.

## 2026-10-17: workflow-sandbox #46 tag step, local simulation

The "Ignore tags other than the pushed tag" step of workflow-sandbox #46 (head 6f21e86),
run outside GitHub Actions in a local clone with `GITHUB_REF_NAME` set by hand, followed
by `ci-helper distinfo version .` (ci-helper 0.4.0) and `python -m setuptools_scm`
(setuptools_scm 10.3.4, Python 3.14.8). The two tags `v0.6.0rc2` and `v0.6.0` were
created at 6f21e86, which has `v0.6.0rc1` as an ancestor 70 commits back. The two tools
agreed in every case.

| Tags at HEAD | Pushed ref | Step run | Version |
|---|---|---|---|
| both, annotated, final created after rc | `v0.6.0rc2`, `v0.6.0` or `master` | no | 0.6.0 |
| both, annotated, rc created after final | `v0.6.0` | no | 0.6.0rc2 |
| both, lightweight | `v0.6.0rc2`, `v0.6.0` or `master` | no | 0.6.0 |
| both, annotated or lightweight, either order | `v0.6.0rc2` | yes | 0.6.0rc2 |
| both, annotated or lightweight, either order | `v0.6.0` | yes | 0.6.0 |
| both, annotated or lightweight | `master` | yes | 0.7.0.dev70 |

Without the step the version is the tag that `git describe` picks, which for annotated
tags is the one with the newest tagger date, so a commit tagged final-then-rc, or re-tagged
rc after the final tag, builds the rc version on a final-tag push (labscript-suite #56).
With the step only the pushed tag remains at HEAD and the version is that tag's; a branch
push of a tagged commit builds a development version from the nearest ancestor tag.

The same was then done with real pushes to chrisjbillington/workflow-sandbox, where
uploads are disabled because `RELEASE_REPO` does not match, so only the configure, build
and GitHub release jobs run. Commit 6f21e86 was pushed as branch `fix-multiple-tags`,
then tagged `v0.6.0rc2` (annotated) and pushed, then tagged `v0.6.0` (annotated) and
pushed, then pushed as branch `maintenance/tag-test`. Every job of the three runs
succeeded.

| Push | Run | Tags deleted by the step | `PKGVER` | Built | GitHub release |
|---|---|---|---|---|---|
| tag `v0.6.0rc2` | [39011505494](https://github.com/chrisjbillington/workflow-sandbox/actions/runs/39011505494) | none | 0.6.0rc2 | `workflow_sandbox-0.6.0rc2` sdist, wheel and noarch conda package | draft, prerelease, sdist attached |
| tag `v0.6.0` on the same commit | [39011701607](https://github.com/chrisjbillington/workflow-sandbox/actions/runs/39011701607) | `v0.6.0rc2` | 0.6.0 | `workflow_sandbox-0.6.0` sdist, wheel and conda package | draft, not prerelease, sdist attached |
| branch `maintenance/tag-test` at the same commit | [39011875494](https://github.com/chrisjbillington/workflow-sandbox/actions/runs/39011875494) | `v0.6.0rc2`, `v0.6.0` | 0.7.0.dev70 | `workflow_sandbox-0.7.0.dev70` sdist, wheel and conda package | skipped (`RELEASE=false`) |

So `actions/checkout` with `fetch-depth: 0` fetches the other tags at HEAD,
`GITHUB_REF_NAME` is the bare tag name on a tag push, and the step deletes the right
tags in both the configure and the build job. The test tags, branches and draft releases
were left in the fork.

## 2026-10-17: blocker fix pull requests on GitHub Actions, every Qt binding

Two dispatches of `.github/workflows/test.yml`, as the CLAUDE.md rule asks before a merge.

**Run 39009659742, the fix pull requests, full matrix.** Refs: labscript pr/124
(3a328ae), labscript-devices pr/149 (e346f44), blacs pr/124 (1284b5d), zprocess pr/28
(81b1b10), labscript-utils pr/129 (490f49b); the other seven components at master. Ubuntu
and Windows, Python 3.11 to 3.15, PySide6, PyQt6 and PyQt5, plus the `numpy<2.5` job: 31
jobs.

| Jobs | Result |
|---|---|
| 24 jobs: both OSes, Python 3.11 to 3.14, all three Qt bindings, NumPy 2.5.4 (2.4.6 on 3.11) | all eight steps pass. The example experiment compiles on NumPy 2.5.4 and lyse, the runviewer parsers, the runmanager API and all four applications work on each binding |
| Ubuntu 3.14 PySide6 `numpy<2.5` | all eight steps pass |
| 6 jobs: Python 3.15 on both OSes, each binding | install fails on h5py as before; nothing else runs |

Fully passing jobs took 2.1 minutes on Ubuntu and 3.4 minutes on Windows. The results
were posted as a comment on each of the five pull requests on 2026-10-17.

**Run 39009717709, the metadata pull requests, `numpy<2.5`.** Refs: zprocess pr/29,
qtutils pr/33, desktop-app pr/31, labscript-c-extensions pr/10, labscript-utils pr/130,
labscript pr/125, runmanager pr/131, blacs pr/125, lyse pr/140, runviewer pr/73,
labscript-devices pr/150, labscript-suite pr/106 (all twelve components from their pull
request heads). Ubuntu and Windows, Python 3.11 and 3.14, PySide6: 4 jobs, all eight
steps pass on each. The components build and install with `requires-python >= 3.11`, the
new version scheme name and no `importlib_metadata` fallback, and the component pins in
labscript-suite pr/106 and runmanager pr/131 resolve to the local builds.

## 2026-10-17: fix branches on the local container, Python 3.14, NumPy 2.5.4

The pull request branches of the release blockers (`MAINTENANCE.md`, "Pull requests
opened by the maintenance track"), merged locally onto each master: labscript
`numpy-2.5-dtype-alias` and `python-3.11-metadata`, labscript-devices and blacs the
same, labscript-utils `fix-28-namespace-packages` and `python-3.11-metadata`, zprocess
`fix-27-setconsolemode` and `python-3.11-metadata`, and `python-3.11-metadata` on lyse,
runmanager, runviewer, labscript-suite, desktop-app and qtutils. Installed into the
Python 3.14.6 venv of the run below (NumPy 2.5.4, h5py 3.16.0, pandas 3.0.6, PySide6
6.12.0) with `uv pip install --no-deps`.

| Platform | Python | NumPy | Result |
|---|---|---|---|
| local container | 3.14.6 | 2.5.4 | all eight steps pass: compile, lyse, runviewer, runmanager-api and apps now pass on NumPy 2.5 (the known B7 and D1 items still show as known) |

Also run, outside the harness:

- labscript-utils #28: a script that imports a module from a namespace package under a
  temporary `userlib`, touches it, waits for `ModuleWatcher` to unload, and imports again.
  master: `KeyError: 'labscriptlib'`. Branch: the import succeeds. A profile created by
  the branch has `labscriptlib/example_apparatus/__init__.py`.
- zprocess #27: `disable_quick_edit` with `os.name` patched to `nt` and a stand-in
  `win32console` whose `SetConsoleMode` raises error 87 returns without registering an
  `atexit` handler. Not run on Windows.
- Version scheme: setuptools_scm 10.0.5 computes `3.5.0.dev41` on labscript-utils master
  with both `release-branch-semver` and `semver-pep440-release-branch`; setuptools_scm
  9.2.2 does not have the new name.
- Every package's `__version__` module imports with `-W error::DeprecationWarning`
  after the `importlib_metadata` fallback removal.

## 2026-10-17: master branches on Ubuntu 24.04 and Windows Server 2025

Component commits: zprocess 34443e5, qtutils 5d2885f, desktop-app f216ef0,
labscript-c-extensions 4e440ac, labscript-utils cf0fb71, labscript a0787c4, runmanager
bfe63ba, blacs e5757c7, lyse ed0b6ca, runviewer 4989087, labscript-devices 424b9f4,
labscript-suite 0ab902d. Installed from PyPI with them: PySide6 6.12.0, h5py 3.16.0,
pandas 3.0.6, scipy 1.18.1, pyzmq 27.2.0, matplotlib 3.11.2, pyqtgraph 0.14.0. GitHub
Actions runs 39004344513 and 39004626263 in this repository; the local runs were in an
Ubuntu 24.04 container as root.

| Platform | Python | NumPy | Result |
|---|---|---|---|
| Ubuntu, Windows | 3.11 | 2.4.6 | all eight steps pass |
| Ubuntu, Windows | 3.12, 3.13, 3.14 | 2.5.4 | install and imports pass; `compile` fails with `TypeError: data type 'a256' not understood` (labscript #123), so lyse, runviewer and apps are skipped and the compile checks of runmanager-api fail |
| Ubuntu | 3.14 | 2.4.6 (`--pin "numpy<2.5"`) | all eight steps pass, and the zprocess test suite passes (`--all`) |
| Windows | 3.12, 3.14 | 2.4.6 (`--pin "numpy<2.5"`) | all eight steps pass, and the zprocess test suite passes (`--all`, 118 s) |
| Ubuntu, Windows | 3.15.0 | | install fails: h5py 3.16.0 has no cp315 wheel and its source build stops at `Unable to load dependency HDF5` |
| local container | 3.11.15, 3.14.6 | 2.4.6 | all eight steps pass; zprocess test suite 71 passed, 2 failed as root (see below) |

Python 3.11 passes on NumPy 2.5 because NumPy 2.5 requires Python 3.12 or newer, so pip
resolves NumPy 2.4.6 for 3.11 and the `a256` alias still exists. Users on Python 3.11 are
therefore not affected by labscript #123.

Job durations: a fully passing job takes 2 minutes on Ubuntu and 4 minutes on Windows,
of which the install step is about 40 s and the imports step 35 s to 60 s; the zprocess
test suite adds 2 minutes. The labscript-c-extensions Cython extension builds from source
on both platforms.

### Defects found by the runs

Defects that no GitHub issue or review document records are in `DEFECTS.md`: D1 (BLACS
first-launch traceback), D2 (`make_single_run_file` with a bare filename), D3 (tkinter
import in `labscript_utils.excepthook`) and D4 (stale zlock server with another shared
secret). The runs also showed that `runmanager.globals_diff_shots` raises
`UnboundLocalError` for any two shots of one sequence, not only identical shots as
REVIEW.md runmanager B7 says: the shot files carry the same group definitions and differ
only in the evaluated values stored as attributes, so `globals_diff_groups` finds no
difference. The harness marks B7 and D1 as known in the `runmanager-api` and `apps` steps.

### Behaviours worth knowing

All seen by running the code.

1. **`import labscript_utils` creates a profile** in `~/labscript-suite` when none exists
   (`labscript_utils/__init__.py:22`). Any script that imports labscript_utils on a fresh
   machine writes a profile; the harness creates its profile first so that it owns it.
2. **zprocess tests `test_no_access` and `test_cant_create_files` fail when run as root**
   because root passes the permission checks that they test. They pass as a normal user.
3. **`runmanager.get_shot_globals` emits a `FutureWarning`** telling callers to import it
   from `labscript_utils.shot_utils`. Expected deprecation path; the harness does not
   treat it as a failure.
4. **Qt on a bare Linux container** needs `libegl1`, `libopengl0`, `libxkbcommon0`,
   `libdbus-1-3`, `libfontconfig1` and `libglib2.0-0`, which GitHub's `ubuntu-latest`
   image has except `libegl1` and `libopengl0`. The workflow installs them.
5. **Compiler output streaming needs the labconfig security settings.** A plain `zmq`
   PULL socket receives nothing from the batch compiler; the socket must come from
   `labscript_utils.ls_zprocess.Context`, as the runmanager output box does.

### What the harness does not cover yet

- Real devices, and any device class without a dummy implementation.
- The GUI itself beyond start-up: nothing clicks, and rendering is offscreen.
- Conda installs. The plan is to test them once, close to the release, on a machine where
  the pip install already passes.
- PyQt5 and PyQt6: `install --qt PyQt6` and `--qt PyQt5` exist but have not been run.
- Python 3.15, until h5py ships cp315 wheels.
