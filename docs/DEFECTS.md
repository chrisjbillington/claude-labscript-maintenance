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
| D1 | 2026-10-17 | blacs `blacs/__main__.py:496` | First launch logs an ERROR with a traceback: `restore_window` reads `window_xpos` from settings that do not exist yet | 2 | run | fixed in blacs #128 (opened 2026-10-18, open) with #52 and #56 |
| D2 | 2026-10-17 | runmanager `runmanager/compiler.py:178` | `make_single_run_file` fails with `FileNotFoundError` when the filename has no directory part | 2 | run | fixed in runmanager #134 (opened 2026-10-18, open) |
| D9 | 2026-10-18 | labscript-devices `labscript_devices/PrawnBlaster/labscript_devices.py:408` | With `use_wait_monitor=False`, or a PrawnBlaster that is a secondary pseudoclock, `wait()` makes `generate_code` raise `TypeError: string indices must be integers`: the branch that appends the two indefinite-wait rows does not `continue`, so the `"WAIT"` string reaches the normal-instruction code | 3 | run | the same defect as REVIEW.md Part 1 item 17; fixed in labscript-devices #153 (opened 2026-10-18, open) |
| D3 | 2026-10-17 | labscript-utils `labscript_utils/excepthook/__init__.py:99` | `tkinter` is imported at module level, so a Python without tkinter cannot import lyse, blacs, `labscript_utils.connections` or most device classes | 3 | run | fix open: [labscript-utils #133](https://github.com/labscript-suite/labscript-utils/pull/133) |
| D4 | 2026-10-17 | labscript-utils `labscript_utils/ls_zprocess.py:332` with zprocess `zlock` | A running zlock server with a different shared secret makes `import labscript_utils.h5_lock` fail with `AuthenticationFailure`; nothing restarts the server or says what to do | 3 | run | open |
| D5 | 2026-10-17 | labscript-utils `labscript_profile/default_profile/userlib/analysislib/example_apparatus/example_IMAQdx_remote.py:6` | The example analysis script tests `lyse.spinning_top`, which lyse 3.3.0rc1 moved to `lyse.utils.worker`; lyse's lazy attribute loader resolves only `path`, so the script raises `AttributeError` as soon as lyse runs it | 3 | run | open; the same line in the script of labscript-utils #117 is fixed by `patches/labscript-utils-117-example-analysis-fixes.patch` |
| D6 | 2026-10-17 | labscript-devices `labscript_devices/IMAQdxCamera/blacs_tabs.py:264` | `on_copy_clicked` calls `QtGui.QApplication.instance().clipboard()`; `QtGui` has no `QApplication` under PySide6 or PyQt6, so the Copy button of the attributes dialog raises `AttributeError` with a Qt6 binding | 3 | read | open |
| D7 | 2026-10-17 | release workflow `release.yml:45` and `:235` (rpanderson/workflow-sandbox master, synced to ten repositories by the sync PRs listed in `PULL-REQUESTS.md`) | The "Ignore tags other than the pushed tag" step has no `shell: bash`, so on Windows runners it runs under PowerShell, where `${GITHUB_REF_NAME}` is empty, and deletes the pushed tag; a tag push builds a development version on Windows | 5 | run | fixed in zprocess by #31 (f5f4685), confirmed by the `v2.28.0rc2` run 39029064804, which built 2.28.0rc2 on windows-2022 (`TESTING.md`); fixed in the sandbox by [workflow-sandbox #47](https://github.com/rpanderson/workflow-sandbox/pull/47), merged 2026-10-17 (51023a1), and in the twelve other repositories by the sync PRs merged the same day (`PULL-REQUESTS.md`) |
| D8 | 2026-10-17 | lyse `lyse/__init__.py:76` | `lyse.spinning_top` raises `AttributeError` and `from lyse import *` does not provide it since 3.3.0: the lazy loader serves only `path` after the variable moved to `lyse.utils.worker` | 4 | run | fix open: [lyse #144](https://github.com/labscript-suite/lyse/pull/144), which replaced #142 after GitHub closed it |

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
