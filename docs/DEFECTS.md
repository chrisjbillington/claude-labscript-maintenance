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
| D1 | 2026-10-17 | blacs `blacs/__main__.py:496` | First launch logs an ERROR with a traceback: `restore_window` reads `window_xpos` from settings that do not exist yet | 2 | run | open |
| D2 | 2026-10-17 | runmanager `runmanager/compiler.py:178` | `make_single_run_file` fails with `FileNotFoundError` when the filename has no directory part | 2 | run | open |
| D3 | 2026-10-17 | labscript-utils `labscript_utils/excepthook/__init__.py:99` | `tkinter` is imported at module level, so a Python without tkinter cannot import lyse, blacs, `labscript_utils.connections` or most device classes | 3 | run | open |
| D4 | 2026-10-17 | labscript-utils `labscript_utils/ls_zprocess.py:332` with zprocess `zlock` | A running zlock server with a different shared secret makes `import labscript_utils.h5_lock` fail with `AuthenticationFailure`; nothing restarts the server or says what to do | 3 | run | open |
| D5 | 2026-10-17 | labscript-utils `labscript_profile/default_profile/userlib/analysislib/example_apparatus/example_IMAQdx_remote.py:6` | The example analysis script tests `lyse.spinning_top`, which lyse 3.3.0rc1 moved to `lyse.utils.worker`; lyse's lazy attribute loader resolves only `path`, so the script raises `AttributeError` as soon as lyse runs it | 3 | run | open; the same line in the script of labscript-utils #117 is fixed by `patches/labscript-utils-117-example-analysis-fixes.patch` |
| D6 | 2026-10-17 | labscript-devices `labscript_devices/IMAQdxCamera/blacs_tabs.py:264` | `on_copy_clicked` calls `QtGui.QApplication.instance().clipboard()`; `QtGui` has no `QApplication` under PySide6 or PyQt6, so the Copy button of the attributes dialog raises `AttributeError` with a Qt6 binding | 3 | read | open |

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
