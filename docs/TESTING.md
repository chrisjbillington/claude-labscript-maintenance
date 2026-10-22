# Test harness results

Results of running `harness/suite.py` (see `harness/README.md`) on the component default
branches, and the defects that the runs found. Newest first. Each run is identified by
the date, the platform, the Python version and the commits in the report's component
table.

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
