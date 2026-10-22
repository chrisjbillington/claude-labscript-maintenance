# Defects found by testing

Defects found by running the suite that no GitHub issue, `REVIEW.md` entry or
`ISSUE-TRIAGE.md` entry records. They are kept here rather than filed upstream unless a
fix is made, in which case the row names the pull request. Importance uses the scale from
`CLAUDE.md`: 5 is fix before the next release, 1 is not worth fixing. Verification is
`run` (reproduced by running code), `read` (seen in the code) or `plausible`, as in
`REVIEW.md`.

## List

| # | Found | Component and location | Defect | Imp. | Verified | Status |
|---|---|---|---|---|---|---|
| D1 | 2026-10-17 | blacs `blacs/__main__.py:496` | First launch logs an ERROR with a traceback: `restore_window` reads `window_xpos` from settings that do not exist yet | 2 | run | fixed in blacs #128 (merged 2026-10-18) with #52 and #56 |
| D2 | 2026-10-17 | runmanager `runmanager/compiler.py:178` | `make_single_run_file` fails with `FileNotFoundError` when the filename has no directory part | 2 | run | fixed in runmanager #134 (merged 2026-10-18) |
| D9 | 2026-10-18 | labscript-devices `labscript_devices/PrawnBlaster/labscript_devices.py:408` | With `use_wait_monitor=False`, or a PrawnBlaster that is a secondary pseudoclock, `wait()` makes `generate_code` raise `TypeError: string indices must be integers`: the branch that appends the two indefinite-wait rows does not `continue`, so the `"WAIT"` string reaches the normal-instruction code | 3 | run | the same defect as REVIEW.md Part 1 item 17; fixed in labscript-devices #153 (merged 2026-10-18) |
| D3 | 2026-10-17 | labscript-utils `labscript_utils/excepthook/__init__.py:99` | `tkinter` is imported at module level, so a Python without tkinter cannot import lyse, blacs, `labscript_utils.connections` or most device classes | 3 | run | fixed in [labscript-utils #133](https://github.com/labscript-suite/labscript-utils/pull/133), merged 2026-10-18 |
| D4 | 2026-10-17 | labscript-utils `labscript_utils/ls_zprocess.py:332` with zprocess `zlock` | A running zlock server with a different shared secret makes `import labscript_utils.h5_lock` fail with `AuthenticationFailure`; nothing restarts the server or says what to do | 3 | run | open |
| D5 | 2026-10-17 | labscript-utils `labscript_profile/default_profile/userlib/analysislib/example_apparatus/example_IMAQdx_remote.py:6` | The example analysis script tests `lyse.spinning_top`, which lyse 3.3.0rc1 moved to `lyse.utils.worker`; lyse's lazy attribute loader resolves only `path`, so the script raises `AttributeError` as soon as lyse runs it | 3 | run | fixed by [lyse #144](https://github.com/labscript-suite/lyse/pull/144), merged 2026-10-18, which serves `lyse.spinning_top` again; the same line in the script of labscript-utils #117 was changed to `lyse.path` before that pull request was merged |
| D6 | 2026-10-17 | labscript-devices `labscript_devices/IMAQdxCamera/blacs_tabs.py:264` | `on_copy_clicked` calls `QtGui.QApplication.instance().clipboard()`; `QtGui` has no `QApplication` under PySide6 or PyQt6, so the Copy button of the attributes dialog raises `AttributeError` with a Qt6 binding | 3 | read | fixed in [labscript-devices #155](https://github.com/labscript-suite/labscript-devices/pull/155), merged 2026-10-18 (REVIEW.md labscript-devices B12) |
| D7 | 2026-10-17 | release workflow `release.yml:45` and `:235` (rpanderson/workflow-sandbox master, synced to ten repositories by the sync PRs listed in `PULL-REQUESTS.md`) | The "Ignore tags other than the pushed tag" step has no `shell: bash`, so on Windows runners it runs under PowerShell, where `${GITHUB_REF_NAME}` is empty, and deletes the pushed tag; a tag push builds a development version on Windows | 5 | run | fixed in zprocess by #31 (f5f4685), confirmed by the `v2.28.0rc2` run 39029064804, which built 2.28.0rc2 on windows-2022 (`TESTING.md`); fixed in the sandbox by [workflow-sandbox #47](https://github.com/rpanderson/workflow-sandbox/pull/47), merged 2026-10-17 (51023a1), and in the twelve other repositories by the sync PRs merged the same day (`PULL-REQUESTS.md`) |
| D8 | 2026-10-17 | lyse `lyse/__init__.py:76` | `lyse.spinning_top` raises `AttributeError` and `from lyse import *` does not provide it since 3.3.0: the lazy loader serves only `path` after the variable moved to `lyse.utils.worker` | 4 | run | fixed in [lyse #144](https://github.com/labscript-suite/lyse/pull/144), merged 2026-10-18, which replaced #142 after GitHub closed it |
| D10 | 2026-10-21 | runmanager `runmanager/evaluator.py:125-135`, `runmanager/__main__.py:2855-2865` | A global with the `outer` expansion that is edited to a non-iterable value keeps the `outer` expansion and shows `'int' object is not iterable` for as long as another global refers to it; the referring global shows `NameError`. Without the referring global the expansion is reset to blank, as intended | 3 | run | reported by the maintainer from runmanager 3.3.0, reproduced on master 73199cb; fixed in [runmanager #138](https://github.com/labscript-suite/runmanager/pull/138), merged 2026-10-21 (3e1de29) |
| D11 | 2026-10-21 | qtutils `icons/` (every icon is a 32×32 file since 244c556), runmanager `main.ui` (`label_non_default_folder` pixmap), blacs `analysis_submission.ui` (initial status pixmap) | An icon loaded as a raw pixmap, such as the `pixmap` property of a `QLabel` in a `.ui` file or a combo box popup entry, shows at 32×32 on a normal DPI display, twice its intended size; `QIcon` uses scale down and are unaffected | 2 | run | reported by the maintainer; fixed in [qtutils #39](https://github.com/philipstarkey/qtutils/pull/39) and, for the runmanager label so that it is also crisp on high DPI, [runmanager #141](https://github.com/labscript-suite/runmanager/pull/141), both open |
| D12 | 2026-10-22 | labscript-utils `labscript_utils/connections.py:17`, blacs `blacs/device_base_class.py:31` and `blacs/front_panel_settings.py:18` | These library modules import `labscript_utils.excepthook`, which installs the Tk error window handler as `sys.excepthook` on import, so `import lyse`, or an experiment script run in a terminal that uses a device module importing `DeviceTab`, opens an error window for every uncaught exception | 3 | run | reported by the maintainer; fixed in [labscript-utils #136](https://github.com/labscript-suite/labscript-utils/pull/136), [blacs #133](https://github.com/labscript-suite/blacs/pull/133), [lyse #148](https://github.com/labscript-suite/lyse/pull/148), [runmanager #142](https://github.com/labscript-suite/runmanager/pull/142), [runviewer #79](https://github.com/labscript-suite/runviewer/pull/79) and [labscript-devices #156](https://github.com/labscript-suite/labscript-devices/pull/156), all open |
| D13 | 2026-10-22 | lyse `lyse/filebox.py:1004`, `:1028` (`do_singleshot_analysis`, `do_multishot_analysis`), `:462` (`update_row`) | After an analysis routine, the analysis thread calls `update_row` once for each shot that the routine saved results to; each call is a separate request to the main thread, reads the whole row, goes through every model column and emits `layoutChanged`. After a multishot routine that saves results to every shot, no other analysis runs for 15 s with 1000 shots, growing faster than linearly; a user with 10,000 shots reported a long hang | 3 | run | reported by the maintainer from lyse 3.3.0; fix on branch `batch-dataframe-updates` (1f6da15 or later), awaiting a test on the lab computer |
| D14 | 2026-10-22 | zprocess `zprocess/utils.py:46`, `:67`, `:83` (`Interruptor`), with lyse `lyse/routines.py:606` and runmanager `runmanager/__main__.py:1375` | `Interruptor.subscribe()` waits on its XPUB socket for the subscription message, but an XPUB socket passes on only the first subscription to a topic, so a second thread that subscribes while another thread is subscribed blocks forever. `ReadQueue.get()` and `ReadQueue.put()` use the same default interruptor under different locks, so `put()` blocks while another thread is in `get()`. Restarting or removing a lyse analysis routine while it is running hangs the lyse GUI: `check_child_exited` calls `from_worker.put()` while the analysis thread is in `from_worker.get()`. runmanager's Restart subprocess during a compilation calls `from_child.put()` in the same way | 4 | run (lyse, minimal `ReadQueue` case); read (runmanager) | reported by the maintainer; fix not yet made |

## Detail

### D1. BLACS logs a traceback on its first launch

With no saved front-panel settings, `restore_window` in `blacs/__main__.py:496` does
`tab_data['BLACS settings']["window_xpos"]`, the `KeyError` is caught by the caller and
logged at ERROR level as "Unable to load window and notebook defaults" with the
traceback. BLACS continues normally. Fix: check that the keys exist before restoring the
geometry, and log the absence at INFO level without a traceback. Found by the harness
`apps` step, which marks the traceback as known. Related to blacs #52 and #56 (window
geometry restoration), which the release plan already lists; a fix for those should remove
this as well.

### D2. `make_single_run_file` fails for a bare filename

`runmanager/compiler.py:178` calls `os.makedirs(os.path.dirname(filename), exist_ok=True)`;
for a filename with no directory part, `dirname` is `''` and `makedirs` raises
`FileNotFoundError`. Reproduced with `make_single_run_file('shot.h5', {}, {}, attrs, 0, 1)`.
Fix: skip `makedirs` when the directory part is empty, or `makedirs` on the absolute path.

### D3. `labscript_utils.excepthook` needs tkinter at import time

`import tkinter` at `excepthook/__init__.py:99` runs whenever `labscript_utils.excepthook`
is imported, which lyse, blacs, `labscript_utils.connections` and the device classes do.
On an interpreter without tkinter (Ubuntu's `python3.11` from the deadsnakes repository in
the test container; conda and python.org interpreters have it) those imports fail with
`ModuleNotFoundError: No module named 'tkinter'` and nothing compiles. labscript-utils #104
(ISSUE-TRIAGE.md item 96) asks why Tk is used but does not record the hard import-time
dependency. Fix: import tkinter inside the function that shows the dialog and fall back
to stderr when it is missing, which is the "optional stderr fallback" that the triage
suggests.

### D4. A stale zlock server with another secret blocks the suite

`connect_to_zlock_server` in `labscript_utils/ls_zprocess.py:332` pings the configured
zlock server and starts one if the ping fails. A server started by an earlier profile
keeps that profile's shared secret; after the profile is recreated (new `zpsecret-*.key`),
the ping fails with `zprocess.security.AuthenticationFailure` and the exception propagates
out of `import labscript_utils.h5_lock`, so every application fails at import until the
old server process is killed by hand. Reproduced by deleting and recreating the profile
while the server from the first profile was running. Fix: on `AuthenticationFailure`,
report that a zlock server with a different shared secret is running on the port and how
to stop it, or shut it down and start a new one when it is a local child process. The
harness avoids it by carrying the shared secret over when it recreates its profile.

### D5. The camera example analysis script fails on current lyse

`example_IMAQdx_remote.py:6` reads `lyse.spinning_top` to decide whether it is running
inside lyse. lyse commit 06ce8dc (v3.3.0rc1) moved `spinning_top` to
`lyse.utils.worker`, and the module `__getattr__` in `lyse/__init__.py:74` resolves only
`path`, so the script raises `AttributeError: module 'lyse' has no attribute
'spinning_top'` on its first statement after the imports. Reproduced with the script of
labscript-utils #117, which copied the same line, run the way lyse's analysis subprocess
runs it. Fix: use `lyse.path`, which is the shot being analysed inside lyse and `None`
outside it, as the fixed #117 script does.

### D6. The camera tab's Copy button fails under Qt6 bindings

`on_copy_clicked` in `labscript_devices/IMAQdxCamera/blacs_tabs.py:264` reads the
clipboard through `QtGui.QApplication.instance()`. In PySide6 and PyQt6 `QApplication`
is only in `QtWidgets` (`QtGui` has `QGuiApplication`), so the attribute lookup raises.
The two `QtGui.QApplication` uses elsewhere in the file were changed to `QtWidgets` in
the Qt6 work; this one was missed. Fix: `QtWidgets.QApplication.instance().clipboard()`.
Found while testing the fixes for #87 and #63 (`TESTING.md`); the attribute lookup was
checked against the installed PySide6 6.12.0, the button was not clicked.
### D7. The tag-ignoring step deletes the pushed tag on Windows

The step added by rpanderson/workflow-sandbox #46 runs
`git tag -d $(git tag --points-at HEAD | grep -vx "${GITHUB_REF_NAME}" || true)` with no
`shell:` and the workflow has no `defaults.run.shell`, so on a Windows runner it runs under
PowerShell (`pwsh -command`). There `${GITHUB_REF_NAME}` is a PowerShell variable, which is
empty (the environment variable is `$env:GITHUB_REF_NAME`), so `grep -vx ""` passes every
tag at HEAD through and the step deletes the pushed tag as well. On the zprocess
`v2.28.0rc1` run (39025867956, `TESTING.md`) the Windows job logged
`Deleted tag 'v2.28.0rc1' (was e74b638)` and built 2.28.0.dev11 while the Ubuntu and
macOS jobs built 2.28.0rc1. A branch push is unaffected, since every tag at HEAD is
deleted on every platform. The sandbox test of the step ran only on Ubuntu, because the
sandbox package is noarch. Fix: add `shell: bash` to both copies of the step (or a
top-level `defaults: run: shell: bash`, which the sandbox had before #46), in the sandbox
and in every repository that carries the synced workflow: labscript, labscript-devices,
labscript-utils, blacs, lyse, runmanager, runviewer, labscript-suite,
labscript-c-extensions and chrisjbillington/zprocess. Until it is fixed, no tag push
produces Windows conda packages with the release version.

Fix: workflow-sandbox #47 adds `shell: bash` to both steps, and sync pull requests carry it
to the twelve repositories (`PULL-REQUESTS.md`). #47 and the twelve sync pull requests were
merged on 2026-10-17. Verified on a Windows runner
(`TESTING.md`, "release tag step on Ubuntu and Windows"): under the default shell the step
deletes every tag at HEAD, under bash it leaves the pushed tag.

### D9. PrawnBlaster `generate_code` fails on a wait without the internal wait monitor

Found while testing the #109 parser fix; REVIEW.md Part 1 item 17 records the same
defect. In `PrawnBlaster.generate_code`, the `else`
branch for a wait when `use_wait_monitor` is False appends two indefinite-wait rows
and then falls through to `reps = instruction["reps"]` with `instruction == "WAIT"`.
Reproduced by compiling a shot with `use_wait_monitor=False`, an external `WaitMonitor`
and one `wait()`. Fix: `continue` after the two rows; with it the shot compiles and the
runviewer parser shows clock ticks on both sides of the wait.

### D8. `lyse.spinning_top` is gone from the module namespace

Analysis routines test `lyse.spinning_top` to find out whether they run inside lyse, and
the default profile's `analysislib/example_apparatus/example_IMAQdx_remote.py:6` does so.
Commit 06ce8dc (2025-04-15, in 3.3.0rc1) moved the variable to `lyse.utils.worker` and
left only `path` in the module's `__getattr__` (`lyse/__init__.py:76`), so since lyse
3.3.0 `lyse.spinning_top` raises `AttributeError` and `from lyse import *` no longer
provides it. Reproduced in a venv with lyse master: `import lyse; lyse.spinning_top`
raises, and a star import has `path` but not `spinning_top`. Fix: read both names from
`lyse.utils.worker` in `__getattr__` and list `spinning_top` in `__all__`, which lyse #144
(formerly #142) does. The harness `lyse` step checks both names and marks them as known until the fix
is merged.

### D10. An `outer` global edited to a constant is not reset while another global refers to it

With `x = np.linspace(0, 10, 10)` (expansion `outer`) and `y = np.max(x)`, editing `x`
to `5` leaves `x` with the `outer` expansion, `x` shows `ExpansionError: 'int' object is
not iterable` and `y` shows `NameError: name 'x' is not defined`. Clearing the expansion
of `x` by hand makes both evaluate. The preparse is meant to clear the expansion itself:
`guess_expansion_modes` ignores an `ExpansionError` and resets the expansion of a global
that is no longer a list or array (`runmanager/__main__.py:2855-2865`). It does not reach
that step because `evaluate_globals` leaves a global that raised `ExpansionError` out of
the evaluation namespace (`runmanager/evaluator.py:125-135`), so `y` raises `NameError`,
and `guess_expansion_modes` returns without changes when any global holds an exception
other than `ExpansionError`. With no global referring to `x`, the expansion is reset on
the next parse.

Reproduced on master 73199cb with a globals file made through `group_manager`, the
library evaluation and the GUI's `guess_expansion_modes` called on a stub: after the edit
the evaluation is `{'x': ExpansionError, 'y': NameError}`, the expansion of `x` is still
`outer` and the shot count is 0. The same code is in 3.3.0 (`runmanager/__init__.py:468-472`
and `__main__.py:3438-3448` of that release). Fix: in `evaluate_globals`, put the value of
a global that raised `ExpansionError` into the namespace before recording the error, since
the expression itself evaluated. With that change the same steps give `x = 5` with a
blank expansion, `y = 5` and one shot. runmanager #138, merged 2026-10-21, makes this change,
and the harness `runmanager-api` step checks the case.

### D11. Icons loaded as raw pixmaps are twice their intended size

Since qtutils 244c556 every icon in the resource is the 32×32 upscale of the 16×16 Fugue
original. `QIcon` renders an icon at the size a widget asks for, so tool buttons, items
and menus are right, but a raw pixmap is shown at its native size: runmanager's
non-default output folder marker (the `pixmap` property of `label_non_default_folder` in
`main.ui`), the initial server status image in blacs' `analysis_submission.ui`, and the
entries of a combo box popup. Verified on 2026-10-21 in the Python 3.14 harness venv
with PySide6 6.12 at scale factor 1: the label's pixmap was 32×32 and the expansion
editor of runmanager #140 drew its icons at 32 px. Fix: qtutils #39 restores the 16×16
files as the base icons, renames the 32×32 files to `@2x` variants that Qt picks on
high DPI displays, and lists each file under an extension-less alias so that the
`:qtutils/fugue/name` references in the suite find the variant too. With it the label's
pixmap is 16×16 and the popup icons match the table's. A raw pixmap never gets the `@2x`
variant, so runmanager #141 renders that label from a `QIcon` at the small icon size,
which is 16 logical pixels on any display and the 2× image on high DPI. The explicit 16 px
pixmaps that blacs and labscript-devices render from a `QIcon` are the correct API and are
unchanged.

### D12. Importing a library module installs the graphical excepthook

`labscript_utils/excepthook/__init__.py` sets `sys.excepthook` and patches
`threading.Thread.run` when it is imported. `labscript_utils.connections`,
`blacs.device_base_class` and `blacs.front_panel_settings` import it at module level.
`lyse.dataframe_utilities` imports `labscript_utils.connections`, so `import lyse; 1/0`
in a terminal opens an error window. Eleven single-file labscript-devices modules, including
`PulseBlaster.py` and `NovaTechDDS9M.py`, import `DeviceTab` at module level, so an
experiment script that uses them gets the handler when it is run in a terminal or
compiled by runmanager. `NI_DAQmx/testing/test_NI_DAQmx_labscript.py:20` resets
`sys.excepthook` to work around this. Fix: the three imports are removed, the module gets
an `install()` function that the applications, the lyse analysis subprocess and the BLACS
workers call, and `LABSCRIPT_DISABLE_GRAPHICAL_EXCEPTHOOK` turns off the windows for
automated testing. Importing the module still calls `install()`, with a TODO to remove
the call in a future release.

### D13. Results of an analysis routine are applied to the dataframe one shot at a time

`FileBox.do_singleshot_analysis` and `FileBox.do_multishot_analysis` call
`DataFrameModel.update_row(file, updated_row_data=...)` for each shot in the results that
a routine returns. `update_row` is an `inmain` call, so the analysis thread waits for the
main thread once per shot. Each call reads the shot's full row with
`self.dataframe.iloc[row_number].to_dict()`, checks every model column against the
updated keys and emits `layoutChanged`. The GUI stays responsive between calls, but no
single-shot or multishot analysis runs until the calls are done.

Measured with the harness venv (Python 3.14, pandas 3.0.6, PySide6 6.12.0, offscreen
platform): 2.3 ms per shot through `inmain` from a worker thread with 200 columns, and
in a running lyse with a single-shot routine and a multishot routine that saves five
results to every shot, 6.7 s after the routine finished for 500 shots and 15.3 s for
1000 shots. Fix: `DataFrameModel.update_rows`, which applies all of a routine's results
in one main-thread call, setting each column for all of its rows at once; 0.3 s and
0.4 s in the same lyse runs (`TESTING.md`, 2026-10-22).

### D14. A second thread that subscribes to an `Interruptor` blocks forever

`Interruptor.subscribe()` subscribes the calling thread's SUB socket to the empty topic
and then calls `self._xpub.recv()` to wait until the XPUB socket has the subscription.
An XPUB socket passes on a subscription message only for the first subscriber to a
topic, and an unsubscription message only for the last, so `subscribe()` in a second
thread does not return while a first thread is subscribed. The second thread holds
`Interruptor._lock`, so `unsubscribe()` in the first thread then blocks too. The code is
the same in zprocess 2.26.0, 2.27.1 and master 1de4c26.

`ReadQueue.get()` holds `self.lock` and `ReadQueue.put()` holds `self.to_self_lock`, and
both subscribe to `self.interruptor` when no interruptor is given. A `put()` from one
thread while another thread is in `get()` therefore never returns, although the class
docstring gives this as the purpose of `put()`.

In lyse, `AnalysisRoutine.end_child` sends `quit`, waits 2 s, sends SIGTERM, waits 2 s
and sends SIGKILL, then `check_child_exited` calls `self.from_worker.put(('error', {}))`
to end the analysis thread's `from_worker.get()`. If the routine was running, the main
thread blocks in that `put()` and the lyse GUI stops responding. The worker is killed,
but no new worker is started. The message "SIGTERM ignored: will be handled when kill
lock released." is printed by the worker because the analysis holds the kill lock; it is
expected, and SIGKILL ends the worker 2 s later. On Windows `terminate()` ends the worker
at once, but the same `put()` follows, so the hang is expected there too (read).
runmanager's `on_restart_subprocess_clicked` calls `self.from_child.put(['done', False])`
while `compile_loop` can be in `self.from_child.get()` (`__main__.py:2781`), which is the
same case (read).

Fix: `self._xpub.setsockopt(zmq.XPUB_VERBOSER, 1)` after the XPUB socket is created, so
that every subscription and unsubscription message reaches the XPUB socket. With this
line, the minimal case returns and the lyse restart completes (`TESTING.md`,
2026-10-22).
