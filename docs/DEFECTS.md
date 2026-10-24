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
| D11 | 2026-10-21 | qtutils `icons/` (every icon is a 32×32 file since 244c556), runmanager `main.ui` (`label_non_default_folder` pixmap), blacs `analysis_submission.ui` (initial status pixmap) | An icon loaded as a raw pixmap, such as the `pixmap` property of a `QLabel` in a `.ui` file or a combo box popup entry, shows at 32×32 on a normal DPI display, twice its intended size; `QIcon` uses scale down and are unaffected | 2 | run | reported by the maintainer; fixed in [qtutils #39](https://github.com/philipstarkey/qtutils/pull/39) and, for the runmanager label so that it is also crisp on high DPI, [runmanager #141](https://github.com/labscript-suite/runmanager/pull/141), both merged 2026-10-23 |
| D12 | 2026-10-22 | labscript-utils `labscript_utils/connections.py:17`, blacs `blacs/device_base_class.py:31` and `blacs/front_panel_settings.py:18` | These library modules import `labscript_utils.excepthook`, which installs the Tk error window handler as `sys.excepthook` on import, so `import lyse`, or an experiment script run in a terminal that uses a device module importing `DeviceTab`, opens an error window for every uncaught exception | 3 | run | reported by the maintainer; fixed in [labscript-utils #136](https://github.com/labscript-suite/labscript-utils/pull/136), [blacs #133](https://github.com/labscript-suite/blacs/pull/133), [lyse #148](https://github.com/labscript-suite/lyse/pull/148), [runmanager #142](https://github.com/labscript-suite/runmanager/pull/142), [runviewer #79](https://github.com/labscript-suite/runviewer/pull/79) and [labscript-devices #156](https://github.com/labscript-suite/labscript-devices/pull/156), all merged 2026-10-23 |
| D13 | 2026-10-22 | lyse `lyse/filebox.py:1004`, `:1028` (`do_singleshot_analysis`, `do_multishot_analysis`), `:462` (`update_row`) | After an analysis routine, the analysis thread calls `update_row` once for each shot that the routine saved results to; each call is a separate request to the main thread, reads the whole row, goes through every model column and emits `layoutChanged`. After a multishot routine that saves results to every shot, no other analysis runs for 15 s with 1000 shots, growing faster than linearly; a user with 10,000 shots reported a long hang | 3 | run | reported by the maintainer from lyse 3.3.0; fixed in [lyse #150](https://github.com/labscript-suite/lyse/pull/150) (merged 2026-10-23) |
| D14 | 2026-10-22 | zprocess `zprocess/utils.py:46`, `:67`, `:83` (`Interruptor`), with lyse `lyse/routines.py:606` and runmanager `runmanager/__main__.py:1375` | `Interruptor.subscribe()` waits on its XPUB socket for the subscription message, but an XPUB socket passes on only the first subscription to a topic, so a second thread that subscribes while another thread is subscribed blocks forever. `ReadQueue.get()` and `ReadQueue.put()` use the same default interruptor under different locks, so `put()` blocks while another thread is in `get()`. Restarting or removing a lyse analysis routine while it is running hangs the lyse GUI: `check_child_exited` calls `from_worker.put()` while the analysis thread is in `from_worker.get()`. runmanager's Restart subprocess during a compilation calls `from_child.put()` in the same way | 4 | run (lyse, minimal `ReadQueue` case); read (runmanager) | reported by the maintainer; fixed in [zprocess #34](https://github.com/chrisjbillington/zprocess/pull/34), open |
| D15 | 2026-10-22 | lyse `lyse/analysis_subprocess.py:341` (`AnalysisWorker.mainloop`) | The worker holds the kill lock for the whole of each task, so SIGTERM is deferred until the routine finishes. On Linux and macOS a routine that is restarted or removed while it runs ignores lyse's SIGTERM and, if it is still running 2 s later, is ended with SIGKILL, which is not deferred for an open HDF5 file. `labscript_utils.h5_lock` already holds the kill lock while each HDF5 file is open | 3 | run | found while investigating D14; fixed in [lyse #151](https://github.com/labscript-suite/lyse/pull/151), open |
| D16 | 2026-10-22 | lyse `lyse/filebox.py:338-353` (`DataFrameModel.remove_selection`), `:652-656` (`renumber_rows`), `lyse/widgets.py:20-26` (`UneditableModel.flags`) | Removing many selected shots takes minutes: 61 s for 3990 of 4000 shots with 200 data columns, increasing with the square of the number of shots. `UneditableModel` overrides `flags()` in Python, and `selectedRows()` calls it for every cell of every selected row; rows are removed from the Qt model one at a time from the top, so each removal moves every row below it; with integer indexing, `renumber_rows` looks up three dataframe columns for every row | 3 | run | reported by the maintainer; fixed in [lyse #152](https://github.com/labscript-suite/lyse/pull/152) (merged 2026-10-23) |
| D17 | 2026-10-22 | lyse `lyse/widgets.py:76` (`ItemDelegate.paint`) | Painting the status column of the shots table calls `QApplication.fontMetrics()`, which PyQt6 does not provide, so with PyQt6 every paint of a shot whose analysis is not complete raises `AttributeError: 'QApplication' object has no attribute 'fontMetrics'` through the excepthook and the progress bar is not drawn. PySide6 and PyQt5 provide the method | 4 | run | found by the `lyse-gui` harness step with PyQt6 6.11.0 on Ubuntu and locally; fixed in [lyse #154](https://github.com/labscript-suite/lyse/pull/154) (merged 2026-10-23) |
| D18 | 2026-10-22 | zprocess `zprocess/process_tree.py:230` (`HeartbeatClient.mainloop`), `:1139` (`Process.terminate`); lyse `lyse/routines.py:591`; runmanager `runmanager/__main__.py:1388` | The kill lock has no effect on Windows: `Popen.terminate()` and `os.kill(pid, SIGTERM)` are `TerminateProcess`, so no handler runs, and a worker that is writing to an HDF5 file is ended at once by a heartbeat failure, by lyse's and runmanager's SIGTERM stage and by BLACS's `finalise_close_tab`. On Linux and macOS the SIGTERM handler runs only when the main thread next executes Python code, so a worker inside a long C call is not ended either | 3 | read | the heartbeat path is fixed in [zprocess #35](https://github.com/chrisjbillington/zprocess/pull/35) (`exit_when_released()`, `SUBPROCESS-INTERRUPTION.md`), open; the `terminate()` stages are replaced by the design there |
| D19 | 2026-10-22 | zprocess `zprocess/utils.py:272` (`get_venv_executable_and_env`) | In a venv made from a python.org framework build on macOS, every zprocess subprocess (BLACS workers, the runmanager compiler, lyse analysis workers) starts with the base interpreter's packages and fails at its first import of a venv package. The function starts the child from `sys._base_executable` with `__PYVENV_LAUNCHER__` set, to skip the launcher process of a Windows venv; on macOS `sys._base_executable` is the framework's `bin/python3.x` stub, which overwrites the variable with its own path before it execs the interpreter | 3 | run (macOS GitHub Actions runner, Python 3.11 to 3.14) | fixed in [zprocess #36](https://github.com/chrisjbillington/zprocess/pull/36), open, which skips the launcher on Windows only. desktop-app `desktop_app/environment.py:250` has a copy of the function, which its entry point launcher uses, so an application started from its entry point script on macOS fails the same way; fixed in [desktop-app #35](https://github.com/chrisjbillington/desktop-app/pull/35), open |
| D20 | 2026-10-22 | zprocess `tests/test_zprocess.py:331` (`ScriptedHeartbeatServer.close`) | The test's scripted heartbeat server closes its ROUTER socket from the test thread while its mainloop thread may be polling the socket; a zmq socket is not thread-safe. On macOS the zprocess test process ended with a segmentation fault in `HeartbeatTests` in five of twelve runs (Python 3.11 to 3.13; never on 3.14, Linux or Windows) | 2 | run (macOS GitHub Actions); read | fixed in [zprocess #36](https://github.com/chrisjbillington/zprocess/pull/36): the thread is stopped and joined before the socket is closed |
| D21 | 2026-10-22 | zprocess `zprocess/utils.py:117` (`start_daemon`) with labscript-utils `labscript_utils/excepthook/__init__.py:101` on macOS | With the Tcl/Tk 8.6.16 and 8.6.18 that the python.org installers of Python 3.12 and 3.13 bundle, a process that imports tkinter and forks gets a child that is killed with SIGKILL if it calls `fork()` again. `start_daemon` forks and then starts the daemon with `subprocess.Popen`, which forks a second time, so the daemon is never started. The four applications import `labscript_utils.excepthook`, which imports tkinter, before `setup_logging` starts the zlog server, so on the macOS runner with Python 3.12 and 3.13 they all fail at start-up. The zlock server is started from processes that do not import tkinter and is not affected; Python 3.11 (Tcl/Tk 8.6.13) and 3.14 (Tcl/Tk 9.0.4) are not affected | 3 | run (macOS GitHub Actions, reproduced without the suite) | fixed for the applications in [labscript-utils #137](https://github.com/labscript-suite/labscript-utils/pull/137) (merged 2026-10-23), which starts the zlog and zlock servers without `start_daemon`; `start_daemon` itself is fixed in [zprocess #37](https://github.com/chrisjbillington/zprocess/pull/37), open |
| D22 | 2026-10-22 | zprocess `zprocess/process_tree.py:163` (`HeartbeatServer.__init__`) with appnope 1.0.0 `appnope/_nope.py:70` | On macOS every `HeartbeatServer` calls `appnope.nope()`, which sets `objc_msgSend.argtypes`, a global, before each call. BLACS starts the workers of its device tabs from several threads at once, so two threads can set different `argtypes` at the same time, and one call fails with `ctypes.ArgumentError: argument 3: TypeError: wrong type`. The device tab's worker is then not started | 3 | run (macOS GitHub Actions, 1 of 12 jobs of run 39772363140, 1 of 12 of run 39793127711, 1 of 4 of run 39793279995); cause read | fixed by [zprocess #38](https://github.com/chrisjbillington/zprocess/pull/38), merged 2026-10-23 (0fbd203) |
| D23 | 2026-10-22 | zprocess `tests/test_zprocess.py:411` (`_assert_intervals_are_immediate_retries`) | The heartbeat tests that send malformed replies require every interval between heartbeat requests to be at most 1.5 s, with a heartbeat interval of 1 s. On the macOS runner intervals of 1.50 s to 1.53 s occur, so `test_subproc_survives_malformed_heartbeats_below_budget` or `test_successful_heartbeat_resets_miss_counter` fails in some jobs | 2 | run (macOS GitHub Actions, 2 of 12 jobs of run 39772363140) | open |
| D24 | 2026-10-23 | labscript-devices `labscript_devices/NI_DAQmx/blacs_workers.py:856` (`transition_to_manual`) | When the wait monitor thread raises an exception, `transition_to_manual` raises `TypeError: _reraise() takes 1 positional argument but 3 were given` instead of the wait monitor's exception. The worker calls `_reraise(*self.wait_monitor_thread_exception)`, but zprocess `utils._reraise` (a private function, `zprocess/utils.py:107`) takes the `exc_info` tuple as one argument | 2 | run (the function body with the same call, Python 3.14.8); read (the worker) | fixed in [labscript-devices #160](https://github.com/labscript-suite/labscript-devices/pull/160), open |
| D25 | 2026-10-23 | lyse #150 at 5142bbb, `lyse/filebox.py:484` (`update_row`) | `update_row` raises `KeyError` with a result column name, such as `('gaussian_fit', 'atoms_amp', '', '')`, when shots are added after all shots have been removed. `concat_with_padding` drops the empty dataframe, so the columns of earlier results leave the dataframe, but the pull request had removed the code that removed the corresponding Qt model columns. Reported by the maintainer from the lyse 3.3.0 backport on the lab machine | 4 | run (pandas 2.3.3 and 3.0.6) | fixed in lyse #150 at 79f9db9 (`DataFrameModel._remove_defunct_columns`, called from `add_files`), merged 2026-10-23 |
| D26 | 2026-10-23 | lyse `lyse/routines.py:509` (`AnalysisRoutine.do_analysis`) | If an analysis worker exits during a routine without `check_child_exited` ending it (here the worker received SIGKILL while lyse was being closed, by a route not established), `do_analysis` waits on `from_worker.get()` forever. Nothing polls the worker, so it stays a zombie, the routine box never runs another routine and the filebox analysis loop waits for it. Only `check_child_exited` (restart or remove) puts the `error` reply that unblocks the loop | 3 | run (lab machine, lyse 3.3.0 backport: worker a zombie with exit status SIGKILL, analysis thread blocked at `routines.py:509` under py-spy); cause read | open |
| D27 | 2026-10-23 | runmanager `runmanager/__init__.py:548` (3.3.0), `runmanager/expander.py:45` (master) | Without an axis order (`expansion_config`), `expand_globals` puts the zip group axes in the order of a `set` of their names, which depends on the string hash seed, so the shot order changes from one Python process to the next. On a globals file with two zip groups, half of the hash seeds tried iterated one group fastest and half the other, on 3.3.0 and on master 7e692f4. The GUI passes the order from the Axes tab and is not affected; `make_run_file_from_globals_files` and other library calls are | 2 | run | open |
| D28 | 2026-10-23 | runmanager `runmanager/__init__.py:399` (`evaluate_globals`, 3.3.0), `runmanager/evaluator.py:56` (master) | A global in a zip group that depends on globals on other axes of the outer product evaluates without an error and has wrong values in some shots. Each global is evaluated once for the whole sequence with the full lists of the globals that it refers to, so `a and b` or `x if flag else y` on lists tests the truth of the lists, not of each shot's values. A lab's globals file with `pulse_time = duration / 2 if (pulse_1 and pulse_2) else duration`, `pulse_1` and `pulse_2` in one zip group and `pulse_time` zipped with `duration` (as the GUI zips it automatically) gave `duration / 2` in all 100 shots, including those with one pulse | 3 | run (3.3.0, master 7e692f4, #139 and #140) | reported by the maintainer from a colleague's globals file; fixed in [runmanager #143](https://github.com/labscript-suite/runmanager/pull/143) (merged 2026-10-23), which reports such a global as an error |
| D29 | 2026-10-23 | lyse `lyse/filebox.py:897` (`FileBox.incoming_buffer_loop`), `:677` (`add_files`) | A shot file added before BLACS has run it (from the file dialog while a sequence runs) is loaded with a run time of NaT. When BLACS submits the shot after running it, `add_files` ignores it as a duplicate, so the row keeps NaT and no results from the run. On the lab machine three shots of a running sequence were loaded this way, and a multishot drift fit in run time failed with `SVD did not converge` on every run | 3 | run (lab machine, lyse 3.3.0 backport: rows with NaT, files with `run time`, lyse log showing the folder added before BLACS submitted the shots) | fixed in [lyse #155](https://github.com/labscript-suite/lyse/pull/155) (merged 2026-10-23); applied on the lab machine |
| D30 | 2026-10-23 | labscript-devices `labscript_devices/IMAQdxCamera/blacs_tabs.py:398` (`on_snap_clicked`) | With PySide6, clicking Snap in any camera tab based on the IMAQdxCamera tab raises `TypeError: IMAQdxCameraTab.on_snap_clicked() missing 1 required positional argument: 'button'`. PySide6 calls the `define_state` wrapper, which takes `*args`, with no arguments for `clicked`; PyQt5 and PyQt6 pass `checked` | 4 | run (reported by the maintainer from diginuc; reproduced with PySide6 6.12) | fixed in [labscript-devices #158](https://github.com/labscript-suite/labscript-devices/pull/158) (merged 2026-10-23) |
| D31 | 2026-10-23 | labscript-devices `labscript_devices/PhaseMatrixQuickSyn.py:185`, `:191`, `:196` | With PyQt5 or PyQt6, the reference out, blanking and lock recovery buttons raise `TypeError: ... takes 1 positional argument but 2 were given`: PyQt passes `checked` through the `define_state` wrapper to handlers that take no argument. PySide6 works | 2 | run (PyQt5 5.15) | fixed in [labscript-devices #158](https://github.com/labscript-suite/labscript-devices/pull/158) (merged 2026-10-23) |
| D32 | 2026-10-23 | blacs `blacs/tab_base_classes.py:1125`, `:1146` (example `MyTab.bar`, `baz_unpickleable`) | With PySide6, the example tab's bar and threading.Lock buttons raise `TypeError: missing 1 required positional argument: 'button'`, as in D30 | 1 | run (PySide6 6.12) | fixed in [blacs #134](https://github.com/labscript-suite/blacs/pull/134) (merged 2026-10-23) |
| D33 | 2026-10-23 | blacs `blacs/plugins/memory/__init__.py:71` | The memory plugin's Garbage collect menu item is connected directly to `gc.collect`, so with PyQt5 or PyQt6 `triggered` passes `False` as the generation and only generation 0 is collected | 1 | run (PyQt5 5.15) | fixed in [blacs #134](https://github.com/labscript-suite/blacs/pull/134) (merged 2026-10-23) |
| D34 | 2026-10-23 | lyse `lyse/__init__.py:981` (`Run.get_globals`), `:206` and `:1120` (`globals_diff`) | `Run.get_globals(group)` returns the attributes of `globals/<group>`, which in a shot file are the unevaluated expression strings, not the values that the docstring describes; `globals_diff(..., group)` compares those strings. The commit message of 8af660f (lyse #147) says that `get_globals('g')` returns the same types and values as `get_shot_globals`, which holds only for a file with values in the group attributes | 2 | run (lab shot file) | fixed in [lyse #156](https://github.com/labscript-suite/lyse/pull/156) by removing the argument (merged 2026-10-23) |
| D35 | 2026-10-24 | lyse `lyse/filebox.py` `DataFrameModel._set_dataframe_values` (from lyse #150, 79f9db9) | After each single-shot routine, the results are written to the dataframe with one `.loc[rows, column] = Series` assignment per column. For one row this is about 25 times slower than the `.at` assignment that it replaced: 6.8 ms against 0.27 ms for the 28 results of the lab's `gaussian_fit` on a 100-row dataframe (pandas 3.0.6), and 11 ms of the 70 ms per shot in lyse. It runs in the main thread | 3 | run (timed in lyse with the lab's shots and routine) | fix in [lyse #157](https://github.com/labscript-suite/lyse/pull/157) (open) |
| D36 | 2026-10-24 | blacs `blacs/__main__.py:813` (`ExperimentServer`) | BLACS starts its experiment server before it creates the `BLACS` window object, and the server handles a request in the main thread through `inmain`. A shot submitted after the port accepts connections but before start-up has finished is handled while `app` is undefined, and the client gets `NameError: name 'app' is not defined` instead of the shot being queued; runmanager reports that it could not submit the shot | 2 | run (a shot submitted as soon as the BLACS port accepted connections, Python 3.14.8, PySide6) | fixed in [blacs #138](https://github.com/labscript-suite/blacs/pull/138), open |
| D37 | 2026-10-24 | runmanager `runmanager/group_manager.py:101`–`:311` (every function that opens a globals file with `h5py.File(filename, 'a')`) | Each open of a globals file that writes a string attribute makes the file 4096 bytes larger, and the space is never reclaimed: HDF5 allocates a new global heap collection, which is at least 4 kB, for the variable-length strings written in each open. 2000 edits of one global (`set_value` and `set_expansion`) grew a file from 128 kB to 16.5 MB; `h5repack` reduced it to 18.6 kB. Integer, boolean and fixed-length string attributes do not grow the file, nor do many writes in one open. `libver='latest'`, persistent free-space tracking (`fs_strategy` `'fsm'` or `'page'` with `fs_persist=True`) and a smaller `meta_block_size` make no difference | 3 | run (h5py 3.16.0, HDF5 2.0.0, Python 3.14.8) | fix in [runmanager #144](https://github.com/labscript-suite/runmanager/pull/144) (4c876e7, open): the file is repacked after a write once it has grown by 1 MB and to twice its repacked size |
| D38 | 2026-10-24 | labscript-devices `labscript_devices/IMAQdxCamera/blacs_tabs.py:63` (`ImageReceiver.handler`) | `handler` runs in the main thread through `inmain_decorator(wait_for_return=True)`, called from the server thread. If `ImageReceiver.shutdown()`, which the tab calls in `restart`, is called in the main thread while an image is being received, the server thread waits for the main thread and the main thread waits in `shutdown()` to join the server thread, so the main thread hangs | 2 | run (a test script that sends a last image and then shuts the receiver down hung in one of three runs on master 5a5892c); read (the cause) | fixed in [labscript-devices #161](https://github.com/labscript-suite/labscript-devices/pull/161), open |
| D39 | 2026-10-24 | labscript-utils `labscript_utils/qtwidgets/headerview_with_widgets.py:75` and `:120` (`HorizontalHeaderViewWithWidgets.setWidget`, `update_indents`); seen as a crash in lyse `lyse/filebox.py:111` (`EditColumns.populate_model`, `self.model.clear()`) | On PySide6 6.12.0, lyse crashes (segmentation fault in `Shiboken::BindingManager::unregisterWrapper`, or a glibc heap-corruption abort) when an analysis routine adds columns and the Edit columns dialog rebuilds its model. The header view retrieves the header items that `setHorizontalHeaderLabels` creates; `clear()` deletes them and their wrappers remain. Reproduced in a few dozen rebuilds; PySide6 6.8.3 to 6.11.2, PyQt5 and PyQt6 do not crash | 3 | run | fixed in labscript-utils branch `header-items-pyside612` (pull request to follow the test run) |
| D40 | 2026-10-24 | blacs `blacs/__main__.py:813`, lyse `lyse/__main__.py:164`, runmanager `runmanager/__main__.py:3254`, runviewer `runviewer/__main__.py:1695` (the ZMQ server of each) | A second copy of BLACS, lyse, runmanager or runviewer, started while one is running, fails when it binds its labconfig port, with a `zmq.error.ZMQError: Address already in use` traceback in the graphical exception hook rather than a message. lyse and runmanager bind the port at the end of start-up, after lyse has created its routine boxes and runmanager has loaded its globals files; with the fix for D36, BLACS would also create its device tabs and start their workers first | 2 | run (harness steps `blacs-shot` and `apps` on master and on the fix, Ubuntu and Windows) | fixed in [labscript-utils #140](https://github.com/labscript-suite/labscript-utils/pull/140), [blacs #138](https://github.com/labscript-suite/blacs/pull/138), [lyse #159](https://github.com/labscript-suite/lyse/pull/159), [runmanager #146](https://github.com/labscript-suite/runmanager/pull/146) and [runviewer #80](https://github.com/labscript-suite/runviewer/pull/80), open |
| D41 | 2026-10-24 | zprocess `zprocess/security.py:414` (`SecureContext.instance`), `zprocess/process_tree.py:58` (`KillLock.__new__`), `zprocess/process_tree.py:1355` (`RemoteOutputReceiver` in `ProcessTree.subprocess`) | Each checks for a shared object and creates it with no lock. Threads calling `SecureContext.instance()` at once for a new shared secret get different contexts, each with its own authenticator thread; `KillLock()` can create two instances and stored the new one before setting its attributes; concurrently started remote children can be given different output receivers | 2 | run (`SecureContext.instance` from eight threads returned different contexts in five runs of five); read (the other two) | fixed in [zprocess #40](https://github.com/chrisjbillington/zprocess/pull/40), open |
| D42 | 2026-10-24 | PySide6 6.12.0 (upstream), on Python 3.10 and 3.11 | Every call of a PySide6 method that returns `None` decrements the reference count of `None` once more than it increments it. On Python 3.12 and later `None` is immortal and nothing happens; on 3.11, once the count reaches zero the process aborts with `Fatal Python error: none_dealloc: deallocating None` or crashes. lyse's Edit columns dialog makes several such calls per column, and 200 updates abort lyse every time; any long-running suite application with PySide6 6.12.0 on Python 3.11 will crash eventually. PySide6 6.11.2 on Python 3.11 does not do it | 4 | run (`sys.getrefcount(None)` before and after 2000 calls of `QObject.setObjectName`, `QWidget.setEnabled`, `QStandardItemModel.clear` and others: -1 per call on 6.12.0, 0 on 6.11.2, Python 3.11.17) | open; not fixable in the suite. Workaround: PySide6 other than 6.12.0 on Python 3.11 |

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

### D15. The analysis worker holds the kill lock for the whole of a routine

lyse 45181e9 (2012) wrapped each task in `AnalysisWorker.mainloop` in `with kill_lock:`
so that the worker was not terminated while it wrote to HDF5 files. labscript-utils
5295028 and a727c79 (2019) made `h5_lock.File` acquire the kill lock when a file opens
and release it on close (`labscript_utils/h5_lock.py:47-48`, `:69-71`), and
`hack_locks_onto_h5py()` replaces `h5py.File` with that class. The worker imports
`labscript_utils.h5_lock` before `h5py` (`lyse/analysis_subprocess.py:17`), so every
HDF5 file that a routine opens holds the kill lock while it is open, and the
routine-wide lock does not add protection for the files.

`AnalysisRoutine.end_child` sends SIGTERM 2 s after `quit` and SIGKILL 2 s after that.
With the routine-wide lock, SIGTERM has no effect while the routine runs, so a routine
that runs for more than another 2 s is ended with SIGKILL, also while a file is open. A
worker killed while writing to an HDF5 file left a file that h5py could not open ("bad
object header version number"). Without the routine-wide lock, SIGTERM ends the worker
at once, or when its open HDF5 file is closed. On Windows `terminate()` ignores the kill
lock in both cases. Fix: lyse #151 removes the routine-wide lock and the unused
`kill_lock` global (`TESTING.md`, 2026-10-22).

### D16. Removing many shots from lyse takes minutes

`DataFrameModel.remove_selection` reads the selected rows with
`QItemSelectionModel.selectedRows()`. For each row, `selectedRows()` checks every
selection range and calls the model's `flags()` for every column. The model is a
`lyse.widgets.UneditableModel`, which overrides `flags()` in Python to clear
`ItemIsEditable`, so a selection of 2000 rows of a table with 205 columns makes about
400,000 calls into Python. `remove_selection` then removes the rows from the Qt model
one at a time, starting at the top, so each removal moves every row below it. With
`integer_indexing` enabled in the labconfig, `renumber_rows`, which runs after every
removal and renumbers every remaining row, looks up `sequence_index`, `run number` and
`run repeat` in the dataframe once for each row.

Measured with `DataFrameModel` and a `QTableView` in the harness venv (Python 3.14,
PySide6, offscreen platform) and 200 data columns: removing 990 of 1000 shots took
4.8 s, 3990 of 4000 took 61 s, and 2000 of 4000 with integer indexing took 39 s. With
lyse #152, which sets `NoEditTriggers` on the views instead of overriding `flags()`,
reads the rows from the selection ranges, removes each contiguous block with one
`removeRows()` call starting with the last block, and looks up the three columns once,
these took 0.14 s, 0.47 s and 0.28 s, and 15990 of 16000 took 1.9 s (`TESTING.md`,
2026-10-22). A selection of many separate rows, such as every other row, needs one
`removeRows()` call per block, and each call moves the rows below the block, so its
removal time is proportional to the number of blocks times the number of rows.

### D17. The shots table status column does not paint with PyQt6

`ItemDelegate.paint` in `lyse/widgets.py` draws a progress bar for a shot whose analysis
is not complete, and fills a `QStyleOptionProgressBar` with
`self.app.qapplication.fontMetrics()`. `QApplication.fontMetrics()` is deprecated in Qt 6
and PyQt6 does not wrap it, so the call raises `AttributeError`, the excepthook reports
it, and the cell is left unpainted; with the graphical excepthook enabled, each repaint
of such a cell opens the error window. PySide6 and PyQt5 provide the method. Seen in the
`lyse-gui` harness step (run 39716288975, Ubuntu, PyQt6 6.11.0, 24 tracebacks in one
run of the check) and locally with PyQt6 6.11.0. `QtGui.QFontMetrics(qapplication.font())`
gives the same metrics on every binding. Fix: lyse #154 uses it.

### D18. The kill lock does nothing on Windows

`KillLock` is a Python SIGTERM handler (`zprocess/process_tree.py:42-150`). Windows has no
way to send SIGTERM to another process: `Popen.terminate()` and `os.kill(pid, SIGTERM)`
both call `TerminateProcess`, which ends the process without running any handler. So on
Windows the lock protects nothing: not against `Process.terminate()`
(`process_tree.py:1139`), the SIGTERM stage of lyse's `check_child_exited`
(`lyse/routines.py:591`) and runmanager's (`runmanager/__main__.py:1388`), BLACS's
`finalise_close_tab` (`blacs/tab_base_classes.py:631`), or the heartbeat failure path
(`process_tree.py:230`), which sent the process its own SIGTERM. On Linux and macOS the
handler runs only when the main thread next executes Python bytecode, so a worker inside
a long C call does not act on SIGTERM either. `SUBPROCESS-INTERRUPTION.md` has the
facts and the design that replaces the SIGTERM stages. The heartbeat path is fixed on the
zprocess branch `interrupt-main-thread`: the heartbeat thread waits for the lock to be
released and then exits, on every platform (zprocess #35).

### D19. zprocess subprocesses do not see the venv on macOS

`get_venv_executable_and_env` (`zprocess/utils.py:272`, from 4d7a5d3 for zprocess #13)
starts a subprocess from `sys._base_executable` with `__PYVENV_LAUNCHER__` set to the
venv's Python whenever the two differ, so that on Windows the venv's `python.exe`
launcher, which runs the base interpreter as a child process, is skipped. On macOS with a
python.org framework build, `sys._base_executable` is the framework's `bin/python3.x`
stub (CPython `Mac/Tools/pythonw.c`), which sets `__PYVENV_LAUNCHER__` to its own path
and execs the interpreter, so the child configures itself for the base installation:
its `sys.prefix` is the framework and its `sys.path` has no venv `site-packages`. On
Linux the variable is honoured and the venv is found, and on conda there is no venv, so
only macOS venvs are affected. Seen first in the harness on `macos-latest` (run
39739717279, `TESTING.md`), where every step that starts a subprocess failed with
`ModuleNotFoundError: No module named 'labscript_utils'` and 28 zprocess tests failed;
confirmed with a diagnostic workflow that started a child both ways from a uv venv of
Python 3.14.8 and printed its prefix and path. Fix: zprocess #36 skips the launcher on Windows only, as `multiprocessing` does.

desktop-app has a copy of the function (`desktop_app/environment.py:250`), which
`desktop_app/launcher.py:74` uses to start the application from its entry point script,
so `blacs`, `runmanager`, `lyse` and `runviewer` run from a macOS venv's `bin` directory
fail at their first import of a venv package. Confirmed with a diagnostic workflow on
`macos-latest` (run 39753264955, `TESTING.md`). Fix: desktop-app #35 makes the same
change.

### D20. The scripted heartbeat server closes its socket under its own thread

`ScriptedHeartbeatServer` in `tests/test_zprocess.py` runs a mainloop thread that polls
its ROUTER socket in 100 ms steps. `close()` set `_running` to false, closed the socket
and then joined the thread, so the socket could be closed while the thread was inside
`poll()`. libzmq sockets are not thread-safe, and on the macOS runner the test process
ended with "Fatal Python error: Segmentation fault" at the start of
`test_subproc_survives_malformed_heartbeats_below_budget` or
`test_subproc_survives_missing_heartbeats_below_budget` in five of the twelve macOS
jobs of runs 39743170120, 39743290230 and 39744288024 (`TESTING.md`), with every thread
in the dump inside `zmq` `poll`. Fix: zprocess #36 joins the thread before closing the
socket.

### D21. No zlog server on the macOS runner with Python 3.12 and 3.13

`ensure_connected_to_zlog` (`labscript_utils/ls_zprocess.py:361`) pings the zlog server
with a 50 ms timeout and, when that fails, starts `labscript_utils.zlog --daemon` with
`zprocess.start_daemon` and pings again with a 15 s timeout. `start_daemon`
(`zprocess/utils.py:117`) forks, calls `setsid` in the child and starts the command
from the child with `subprocess.Popen(..., close_fds=True, cwd=...)`. On macOS with
those arguments `Popen` does not use `posix_spawn`, so it forks a second time from the
forked child. On `macos-latest` with Python 3.12.10 and 3.13.16 every application fails
at `setup_logging` because the second ping also fails (runs 39743170120, 39743290230,
39744288024 and 39747320066).

The cause, found with a diagnostic workflow on a throwaway branch (runs 39757012414 to
39763681340, branch since deleted):

- The zlog server works on those jobs. Started from a shell, in the foreground or as a
  daemon, it binds port 7340 and answers pings.
- With `start_daemon` patched to trace each stage, every zlog start from an application
  ends with the forked child killed by signal 9 inside `Popen`, before the server
  process exists. The zlock start in the same job completes.
- A script that imports tkinter and then forks reproduces it without the suite: the
  child runs, but is killed with SIGKILL when it calls `fork()` itself. In that child
  `execv`, `posix_spawn` and `Popen` with `close_fds=False` and no `cwd` (which uses
  `posix_spawn`) work, and `Popen` as `start_daemon` calls it does not. Creating a Tk
  root window has the same effect as the import. A QApplication, the splash screen and
  `import desktop_app` do not have this effect, and neither do the harness's way of
  running a check, a new session, a pipe, the environment or the working directory.
- It depends on the bundled Tcl/Tk: Python 3.11.9 (Tcl/Tk 8.6.13) and 3.14.8 (9.0.4)
  are not affected, 3.12.10 (8.6.16) and 3.13.16 (8.6.18) are. The macOS notifier
  source, which installs the `pthread_atfork` handlers, is the same in Tcl 8.6.13 and
  8.6.16, so the change that causes it is elsewhere in Tcl or Tk; it was not located.
  No crash report is written.
- On labscript-utils master `labscript_utils/excepthook/__init__.py:101` imports
  tkinter when the module is imported, and runviewer, runmanager, lyse and BLACS import
  that module before `setup_logging`. The zlock server is started by
  `connect_to_zlock_server` from processes that have not imported it.

Fix: zprocess #37 (6143e79 on top of zprocess #36 for the macOS runs, 366f8f3 on
master) makes `start_daemon` on Unix run a short-lived fresh Python process with
`subprocess.run`, and that process starts the command with `start_new_session=True`.
The calling process then forks only once, and the daemon is still not its child.
labscript-utils #137 makes `ensure_connected_to_zlog` and `connect_to_zlock_server` run
the `--daemon` scripts with `subprocess.run` instead of `start_daemon`, so the second
fork happens in a process that has not imported tkinter. On the macOS runner each change
alone removes the failure on Python 3.12 and 3.13 (runs 39793127711 and 39793279995,
`TESTING.md`). Importing tkinter only when an error window is shown, as the
labscript-utils branch `excepthook-gui-only` does, would avoid the failure for the
applications only.

### D22. Concurrent `appnope.nope()` calls in BLACS on macOS

`HeartbeatServer.__init__` (`zprocess/process_tree.py:163`) calls `appnope.nope()` on
macOS. appnope 1.0.0 calls `objc_msgSend` through ctypes and sets
`objc.objc_msgSend.argtypes` before each call (`appnope/_nope.py:70` to `74`), so the
function is not thread-safe. BLACS starts the worker of each device tab from that tab's
own thread, and each start creates a `HeartbeatServer`. In the job for macOS, Python
3.11 and PyQt5 of run 39772363140 the worker of `intermediate_device` failed with
`ctypes.ArgumentError: argument 3: TypeError: wrong type` while `pseudoclock` was
starting, and the harness `apps` step reported the traceback. The other eleven macOS
jobs did not hit it. It happened again in the jobs for Python 3.12 with PySide6 of run
39793127711 and Python 3.13 with PySide6 of run 39793279995, both with `TypeError: this
function takes at least 4 arguments` from `appnope/_nope.py:71`.

The concurrent calls come from `ProcessTree.subprocess()` (`zprocess/process_tree.py:1305`),
which creates the tree's heartbeat server, and through `check_broker()` its event broker,
the first time it is called, without a lock. With eight threads starting children at
once, one tree created 4 to 8 brokers and 4 to 7 heartbeat servers. Children started
concurrently could therefore be given different brokers, and an event posted by one of
them did not reach a process waiting on another broker. Fix: zprocess #38 holds a lock
while creating the broker and the heartbeat server, and calls `appnope.nope()` in
`ProcessTree.__init__` instead of `HeartbeatServer.__init__`.

### D23. The heartbeat retry tests have a 0.5 s margin

The heartbeat tests with malformed replies in `tests/test_zprocess.py` check, through
`_assert_intervals_are_immediate_retries(1.5)` (`tests/test_zprocess.py:411`), that the
child sends its next heartbeat within 1.5 s, when the heartbeat interval is 1 s. In run
39772363140 the macOS jobs for Python 3.11 with PySide6 and Python 3.13 with PyQt6
measured intervals of 1.505 s, 1.532 s and 1.538 s and failed. Fix: a larger bound, for
example the midpoint between the heartbeat interval and the reply timeout.

### D24. The NI DAQmx worker loses the wait monitor's exception

The wait monitor thread of the NI DAQmx worker stores `sys.exc_info()` in
`self.wait_monitor_thread_exception` (`labscript_devices/NI_DAQmx/blacs_workers.py:827`).
`transition_to_manual` re-raises it with `_reraise(*self.wait_monitor_thread_exception)`
(`:856`), which passes three arguments to zprocess `utils._reraise(exc_info)`, a function
of one argument. Running the function body with the same call raised `TypeError:
_reraise() takes 1 positional argument but 3 were given`, so BLACS shows that error for
the shot instead of the wait monitor's.
Fix: `raise exc.with_traceback(tb)` from the stored tuple in the worker, without the
zprocess import.

### D27. The order of zip group axes depends on the hash seed

`expand_globals` collects the zip keys with `zip_keys = set(expansions.values())`
(`runmanager/expander.py:45` on master, `runmanager/__init__.py:548` on 3.3.0) and builds
the axes in that order. Axes that `expansion_config` does not order get order -1, and
the sort by order is stable, so their order is the order of the set. With
`PYTHONHASHSEED` 1 and 3 a file with the zip groups `clock` and
`total_yellow_pulse_duration` iterated `clock` fastest, and with 2 and 4 the durations
fastest. Fix: build the zip keys in the order in which the globals are defined, for
example with `dict.fromkeys(expansions.values())`.

### D28. A zipped global that depends on another axis has wrong values

The globals file had `yellow_pulse_1 = [True, False]` and `yellow_pulse_2 = [False, True]`
in the zip group `clock`, `total_yellow_pulse_duration = np.linspace(1, 2500, 50) * us`,
and `yellow_pulse_time = total_yellow_pulse_duration / 4 if ramsey else
total_yellow_pulse_duration / 2 if (yellow_pulse_1 and yellow_pulse_2) else
total_yellow_pulse_duration`, zipped with `total_yellow_pulse_duration` by the GUI's
automatic zip groups (`guess_expansion_modes`, `runmanager/__main__.py:2837` on master).
`yellow_pulse_1 and yellow_pulse_2` evaluates to the non-empty list `[False, True]`, so
`yellow_pulse_time` is half the duration in all 100 shots; with one pulse on in each shot,
the intended value is the full duration. `yellow_valid = ValueError(...) if ramsey and
(yellow_pulse_1 or yellow_pulse_2) else 'ok'` has the same form. The values were the same
on 3.3.0, master 7e692f4 and the #139 and #140 branches; #140's `automatic_expansions`
zips `yellow_pulse_time` with the durations as well.

A global that depends on two axes cannot be one axis of the outer product, so evaluating
it correctly would need evaluation per shot, which changes the meaning of existing
expressions such as `len(x)` of an expanded global. runmanager #143 instead gives a
global in a zip group a `ValueError` if it refers, directly or through globals that are
not expanded, to an `outer` global or a global in another zip group. Globals without an
expansion are not checked, since `len(a) * len(b)` is correct and cannot be told apart
from `a or b`. A zipped global that uses only the length of a global on another axis is
reported although its values are correct.

On 3.3.0 the scan can be written with all four globals in one zip group:
`durations = tuple(np.linspace(1, 2500, 50) * us)` with no expansion,
`total_yellow_pulse_duration = np.tile(durations, 2)`,
`yellow_pulse_1 = np.repeat([True, False], len(durations))`,
`yellow_pulse_2 = np.repeat([False, True], len(durations))` and `yellow_pulse_time =
np.where(ramsey, total_yellow_pulse_duration / 4, np.where(yellow_pulse_1 &
yellow_pulse_2, total_yellow_pulse_duration / 2, total_yellow_pulse_duration))`. This
gives 100 shots with `yellow_pulse_time` equal to the duration in each (run, library
only), and the #143 check does not report it. The alternative is to compute the pulse
time in the experiment script.

### D30 to D33. The checked argument of `clicked` and `triggered`

`QAbstractButton.clicked` and `QAction.triggered` have an optional `checked` argument.
For a slot that accepts `*args`, PyQt5 and PyQt6 pass it and PySide6 does not: PySide6
passes as many arguments as the slot's code object has named positional parameters.
Setting `__signature__` or using `functools.wraps` on the wrapper does not change this.
`define_state` (`blacs/tab_base_classes.py:202`) wraps a handler in `f(self, *args,
**kwargs)`, so a decorated handler connected to `clicked` gets no argument under PySide6
and `checked` under PyQt. A handler must therefore take an optional argument, as the
PulseBlaster and CiceroOpalKellyXEM3001 handlers do. A scan of every `clicked` and
`triggered` connection in the component repositories found D30 to D33; lambdas with no
parameters, undecorated methods and handlers with an optional argument or `*args` work
with all three bindings.

Verified by connecting the real handlers to a `QPushButton` through `define_state`,
clicking it and calling the queued function as the state machine does, with PySide6
6.12 and PyQt5 5.15, before and after the fixes. A prototype `define_state` that
generates a wrapper with the handler's own parameter list made every labscript-devices
handler work under both bindings without the call-site fixes; it was not adopted.

### D36. A shot submitted while BLACS is starting is not queued

`blacs/__main__.py` creates the `ExperimentServer` at line 813, then loads the connection
table and creates the `BLACS` object, `app`, at line 829. The server's handler calls
`app.queue.process_request` in the main thread, and the main thread processes events
during start-up (each `splash.update_text` does), so a request that arrives in that
interval runs before `app` exists. The harness step `blacs-shot`, which submitted a shot
as soon as the BLACS port accepted connections, got `NameError: The server had an
unhandled exception whilst processing the request: NameError: name 'app' is not
defined`. This can happen when runmanager submits shots to a BLACS that is restarting,
for example after a connection table recompile.
Fix: start the experiment server after `app` is created, as lyse does; done in blacs
#138. A shot submitted before then waits for the server and is queued when it starts.

### D39. lyse crashes on PySide6 6.12 when the Edit columns dialog is rebuilt

`EditColumns.populate_model` (`lyse/filebox.py:110`) calls `self.model.clear()`, then
`setHorizontalHeaderLabels(['', 'Name'])`, then `self.header.setWidget(0, checkbox)`.
`HorizontalHeaderViewWithWidgets.setWidget` and `update_indents` call
`self.model.horizontalHeaderItem(0)`, which gives Python a wrapper of the header item
that Qt created. The wrapper is kept by the model and is not invalidated when the next
`clear()` deletes the item. On PySide6 6.12.0, a later `clear()` that deletes
Python-created row items then crashes in `QStandardItem::~QStandardItem` →
`Shiboken::Object::destroy` → `BindingManager::unregisterWrapper`. lyse rebuilds the model
each time `columns_changed` is emitted, which happens when a routine saves a result in a
new column.

The crash needs only PySide6: rebuilding a `QStandardItemModel` with `clear()`,
`setHorizontalHeaderLabels`, one `horizontalHeaderItem(0)` call and a few rows of
`QStandardItem`s crashes within 300 rebuilds on PySide6 6.12.0 (Python 3.12 and 3.14) and
not on 6.8.3, 6.9.3, 6.10.2, 6.11.0 or 6.11.2, or on PyQt5 or PyQt6. The 6.12.0 change
that is probably involved is pyside-setup 50ab3a831 (PYSIDE-3365), which stopped
`clear()` from taking the rows and releasing their wrappers itself before Qt deletes them.
With lyse's own `EditColumns` and updates that add one column at a time, lyse master
crashed after 15 to 31 updates in five runs.

Fix: `HorizontalHeaderViewWithWidgets` reads the header font with `headerData(...,
FontRole)` and gives a section with no header item an empty label with `setHeaderData`,
so it retrieves no header item. With the change, three 30 s runs did about 10,000 updates
each without a crash, and the header labels and widget positions in a test with widgets
on a section that has a header item and on one that has none are the same as on master
under PySide6, PyQt6 and PyQt5. The `lyse-gui` harness step runs 200 updates in a
subprocess and reports the check as known while the header view still calls
`horizontalHeaderItem`.

### D40. A second copy of an application fails with a traceback

BLACS, lyse, runmanager and runviewer each bind their labconfig port when they create
their ZMQ server. A second copy started while one is running gets `zmq.error.ZMQError:
Address already in use` there, which is shown by the graphical exception hook. runviewer
binds first; lyse and runmanager bind at the end of start-up. The fix for D36 moves the
BLACS server to after the device tabs are created, so a second BLACS would also start
device workers, which open the same hardware as the running copy.
Fix: `labscript_utils.ls_zprocess.port_in_use` attempts a TCP connection to the port on
127.0.0.1; on Windows it disables SYN retransmission on the socket so that a refused
connection fails at once, and uses no socket timeout. `exit_if_port_in_use` logs and
shows a message that another copy is probably running, and exits. Each application calls
it with its port early in start-up; done in labscript-utils #140, blacs #138, lyse #159,
runmanager #146 and runviewer #80. The harness step `apps` times `port_in_use` and starts
a second copy of each application.

### D42. PySide6 6.12.0 decrements the reference count of None on Python 3.11

Found while testing the D39 fix: on Ubuntu, Python 3.11, PySide6 6.12.0, the `lyse-gui`
check that updates the Edit columns dialog 200 times aborted with the fix in place.
Locally on Python 3.11.17 the same script aborts in every run with `Fatal Python error:
none_dealloc: deallocating None`. With only PySide6 imported, `sys.getrefcount(None)`
falls by one per call of `QObject.setObjectName`, `QWidget.setEnabled`,
`QStandardItemModel.clear`, `setHorizontalHeaderLabels` and `QStandardItem.setData`, and
the process aborts after a few thousand calls. On PySide6 6.11.2 the count does not fall.
On Python 3.12 and later `None` is immortal, its reference count is not changed, and the
calls are harmless. The PySide6 6.12.0 wheels are built for Python 3.10 and later
(`cp310-abi3`), so pip installs them on Python 3.11.

The suite cannot work around this; an application that uses PySide6 6.12.0 on Python 3.11
crashes after enough calls. lyse crashes fastest, because the Edit columns dialog makes
several such calls per column each time a column is added. The applications use PyQt5
unless PySide6 is chosen. Not reported to Qt yet.
