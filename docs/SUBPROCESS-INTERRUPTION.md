# Interrupting and ending subprocesses

Written 2026-10-22, from the investigation that followed lyse #151 (the analysis worker
no longer holds the kill lock for the whole of a routine) and lyse #153 (the Abort
button). Those two pull requests fix their own problems and showed that the suite has
no safe way to end a subprocess that is doing something: the kill lock has no effect on
Windows, SIGTERM only reaches a worker that is executing Python, and every Restart and
Remove button ends in `Popen.kill()`, which corrupts an HDF5 file that is open for
writing. This note records what was found, with how each fact was verified (run, read or
plausible, as in `REVIEW.md`), and the design that the suite is moving to. Status is in
section 4.

Scope: the lyse analysis workers, the runmanager batch compiler and the BLACS device
workers, and the zprocess machinery under them. The design applies to all three; lyse is
done first because its workers write to shot files most often.

## 1. Facts

### 1.1 The kill lock

`KillLock` (`zprocess/process_tree.py:42`) installs a Python SIGTERM handler and counts
acquisitions. While the count is nonzero, a SIGTERM is recorded and acted on when the
count reaches zero. `labscript_utils.h5_lock.File` acquires it for the lifetime of every
HDF5 file that it opens (`labscript_utils/h5_lock.py:47-48`, `:69-71`), and every suite
subprocess imports `h5_lock` before `h5py`, so an open shot file always holds the lock.

- **(read)** On Windows the lock has never had an effect. `Popen.terminate()` is
  `TerminateProcess`, and so is `os.kill(pid, SIGTERM)`; no handler runs. This covers
  `Process.terminate()` (`process_tree.py:1139-1151`), the SIGTERM stage of lyse's
  `check_child_exited` (`lyse/routines.py:583-604`) and runmanager's
  (`runmanager/__main__.py:1381-1399`), and, before the zprocess change of section
  3.1, the heartbeat failure path (`process_tree.py:230`).
- **(run, Linux)** On POSIX the handler runs only when the main thread next executes
  Python bytecode. A worker inside a C call that does not return (a BLAS routine, a
  driver call with no timeout, an HDF5 write of a large dataset) does not act on
  SIGTERM, lock or no lock. SIGTERM therefore only ends a worker that is executing
  Python, which is exactly the case in which a `KeyboardInterrupt` also works. The
  SIGTERM stage between "ask to quit" and "kill" in lyse and runmanager adds nothing to
  "interrupt, then kill".
- **(read)** `runmanager/batch_compiler.py:68` holds the lock for a whole compile, with
  the effect recorded for lyse in `DEFECTS.md` D15: SIGTERM is deferred until the compile
  finishes, so on Linux the SIGKILL that follows 2 s later is what ends a running
  compile. `labscript` imports `h5_lock` (`labscript/labscript.py:36`), so the file
  writes are covered without it.
- **(read)** The NI_DAQmx BLACS worker holds the lock in its wait monitor thread for the
  whole of a shot (`labscript_devices/NI_DAQmx/blacs_workers.py:772`). This is not about
  files. BLACS commit 2911942 (2013-02-19) added it to the GTK-era NI_PCIe_6363 tab so
  that "the process is not killed by lack of heartbeats when it needs to be timing out
  waits. This ensures a correctly wired experiment will still complete even if the rest
  of BLACS crashes." The wait monitor is the only device that resumes the master
  pseudoclock when a wait times out; if its worker is ended mid-shot, its DAQmx tasks
  are released with it, the resume trigger is never sent and the apparatus stays at the
  wait with its outputs frozen. The hold was carried into labscript-devices in 2014
  (682efdb) and into the unified `NI_DAQmx` worker in 2018 (3788039, 70851c7). The
  heartbeat failure path is the only path that the hold has ever affected, and only on
  Linux and macOS. With the zprocess change of section 3.1 it works on Windows too: an
  orphaned NI_DAQmx worker runs the shot's waits to the end before it exits. A shot
  that never completes
  (no resume pulse arrives after the trigger) leaves such an orphan waiting
  indefinitely, as it has on Linux since 2013. Keeping the hold is recommended; it is
  the reason section 3 says that the kill lock means "do not end this process now", not
  "an HDF5 file is open".

### 1.2 Main threads and listeners

- **(read)** lyse routines run in the worker's main thread: `do_analysis` is
  `@inmain_decorator()` (`lyse/analysis_subprocess.py:365`), and with lyse #153 a
  listener thread reads `from_parent` and sends each task to the main thread, so an
  abort message can arrive while a routine runs.
- **(read)** BLACS worker methods (`Worker.mainloop`, `blacs/tab_base_classes.py:910-953`)
  and runmanager compiles (`BatchProcessor.mainloop`, `batch_compiler.py:47-55`) also run
  in the main thread, because `Process._run` calls `run()` there. In both, the main
  thread is also the thread that reads `from_parent`, so nothing can receive a message
  while a task runs. They need the split that lyse #153 made.
- **(read)** BLACS `finalise_close_tab` (`tab_base_classes.py:631-659`) calls
  `terminate(wait_timeout=2)` and never kills. On POSIX a worker with a file open is
  left running until it closes the file; on Windows it is ended at once.
- **(read)** lyse #153 uses `_thread.interrupt_main()`, which calls
  `PyErr_SetInterruptEx` (CPython `Modules/signalmodule.c:1902-1915`). That sets the
  flag that the eval loop checks and sends no signal, so a main thread blocked in a
  system call is not woken; the exception is raised when the call returns. This is why
  the `lyse-gui` harness step's 600 s `time.sleep` routine needed the 5 s abort timeout
  and a worker restart on both platforms (`TESTING.md`, 2026-10-22).

### 1.3 How an interrupt reaches C code

Read from the CPython 3.14 source and measured on Linux (section 1.4).

- Python's C signal handler (`signalmodule.c:349-379`) only sets a flag and the eval
  loop's "breaker"; on Windows it also sets an event object (`sigint_event`).
  `KeyboardInterrupt` is raised by the main thread at its next bytecode boundary, or
  when C code calls `PyErr_CheckSignals()`.
- A blocking system call is interruptible on POSIX because a signal delivered to the
  blocked thread makes the call return `EINTR`, and the C wrapper calls
  `PyErr_CheckSignals()` before retrying (PEP 475). `time.sleep`, lock acquisition,
  sockets and pyzmq (`zmq/backend/cython/_zmq.py:179-183`) all work this way. On Windows
  there is no `EINTR`; in the main thread, `time.sleep` (`timemodule.c:2345-2380`) and,
  from Python 3.13, lock acquisition (`parking_lot.c:119-131`) wait on the SIGINT event
  as well as their own timer. Other blocking calls, a zmq poll among them, are not woken
  on Windows.
- A compute loop in an extension is interruptible only if the extension calls
  `PyErr_CheckSignals()` itself. NumPy 2.5.4 does not (the `NPY_SIGINT_ON`/`OFF` macros
  are gone; no call in its headers). NumPy code feels interruptible because it is
  usually many short calls in a Python loop, and the interrupt lands between calls.
- Releasing the GIL is unrelated to interruptibility. It only lets the listener thread
  run, so that the abort message can be received at all.

### 1.4 Measurements

Linux, Python 3.14.8, NumPy 2.5.4, h5py 3.16.0, pyzmq 27.2.0. A timer thread acts 0.5 s
after the main thread enters the blocking state; the table gives the time from the
start of the state to the `KeyboardInterrupt` in the main thread. The second column is
lyse #153's method; the third is a real SIGINT sent to the main thread with
`signal.pthread_kill`, which is what `zprocess.interrupt_main_thread()` does on POSIX
(`TESTING.md`, 2026-10-22, has the runs).

| Main thread in | `_thread.interrupt_main()` | SIGINT to the main thread |
|---|---|---|
| `time.sleep(6)` | 6.0 s (after the sleep ended) | 0.5 s |
| `Lock.acquire(timeout=6)` | 6.0 s | 0.5 s |
| zmq `poll(6000)` | 6.0 s | 0.5 s |
| Python loop | 0.5 s | 0.5 s |
| `np.linalg.inv` on 6000×6000 (4.6 s alone) | after the call returned | after the call returned |
| h5py write loop (0.1 s) | after the loop returned | after the loop returned |

A real signal fixes the first three rows. Nothing fixes the NumPy row, which is why the
timeout-then-kill path stays (section 3).

### 1.5 HDF5 integrity

**(run, Linux)** A `KeyboardInterrupt` raised during a write loop (`create_dataset` and
an attribute write per iteration, with a flush) lands in h5py's Python layer between C
calls. The file reopens with every dataset intact, both when the file is closed by
`with h5py.File` as the exception propagates and when the exception propagates out of
an open file and interpreter shutdown closes it. That is the whole case for the
interrupt stage: an exception between bytecodes never leaves HDF5 metadata half
written, whereas `SIGKILL` and `TerminateProcess` can (`TESTING.md`, 2026-10-22,
records "bad object header version number" from a worker killed mid-write; the result
is timing dependent, and a run with a flush per iteration happened to survive).

## 2. Why not keep the current sequence

The current parent sequence in lyse and runmanager is quit, then SIGTERM after 2 s, then
SIGKILL after 2 s more, with no message to the user, and the Restart and Remove buttons
run it unconditionally. Section 1 shows that the middle stage does nothing on Windows and
nothing useful on POSIX, and that the last stage is the only one that can corrupt a
file. Removing the kill lock altogether, as was considered, would discard the one
mechanism that can tell the parent whether killing is safe, and the NI_DAQmx hold
(section 1.1).

## 3. Design

Two stages for every subprocess in the suite:

1. **Interrupt.** Safe, no confirmation. Used by Abort, Restart, Remove and application
   quit. The worker raises `KeyboardInterrupt` in the task that is running, so the
   routine's or script's context managers close its files and release its locks, and
   the worker keeps its imports and windows.
2. **Kill.** Unsafe. Used only after the interrupt has failed and the user has
   confirmed, or when the worker reports that the kill lock is not held.

There is no SIGTERM stage.

### 3.1 zprocess

- `zprocess.interrupt_main_thread()`: on POSIX `signal.pthread_kill(main_thread, SIGINT)`,
  on Windows `signal.raise_signal(SIGINT)`, which runs Python's C handler in the calling
  thread and sets the SIGINT event. It requires a Python SIGINT handler
  (`signal.default_int_handler`) and raises `RuntimeError` otherwise. Python installs
  that handler at startup unless SIGINT was ignored when the process started, which is
  the case for a process started in the background by a shell; lyse #153 installs it
  explicitly in the worker, and the other workers will do the same.
- `KillLock.is_held()`, for the status reply below.
- `KillLock.exit_when_released(status)`: blocks until the lock is not held, then
  `os._exit(status)` without letting the lock be acquired in between. The heartbeat
  failure path calls it instead of sending itself SIGTERM, so an orphaned worker
  respects the lock on Windows and when its main thread is inside a C call.
- The POSIX SIGTERM handler stays. It is the only protection from an external SIGTERM
  (system shutdown, `kill`) and costs nothing.

### 3.2 Worker protocol

Applies to the lyse analysis worker now (lyse #153 has the structure), and to the BLACS
`Worker` and the runmanager `BatchProcessor` after.

- A listener thread reads `from_parent`; tasks run in the main thread.
- `abort`: `interrupt_main_thread()` while a task is running, guarded by a flag so that
  the interrupt is raised in the task and not in the code after it.
- `quit`: interrupt a running task first, then exit.
- `status`: reply with `kill_lock.is_held()`. The listener can reply only if the main
  thread's C call has released the GIL; no reply within about 1 s means "unknown".

### 3.3 Parent sequence

For Abort, Restart, Remove and application quit:

1. Send `abort` (or `quit`). Wait up to about 5 s.
2. If the task is still running, send `status`. If the reply is "not held", kill
   without asking. Otherwise show one dialog: the worker has not stopped after 5 s and is
   probably inside a call that Python cannot interrupt; it has an HDF5 file open for
   writing (or its state is unknown), and killing it may corrupt that file. Kill, or keep
   waiting.
3. On confirmation, `Popen.kill()`.

### 3.4 Per application

- **lyse.** On top of #151 and #153: `abort_analysis()` calls the zprocess helper;
  the `terminate()` stage leaves `check_child_exited`; the `status` query and the
  dialog are added; Restart and Remove go through abort, then the confirmation, instead
  of the current quit, SIGTERM and SIGKILL at 2 s intervals.
- **runmanager.** Remove the routine-wide `with kill_lock` in `batch_compiler.py:68`;
  restructure `BatchProcessor` like the lyse worker so that the Abort button can stop
  the compile that is running rather than only the next shot; make Restart subprocess
  confirm before killing. `DEFECTS.md` D14 (the `from_child.put` hang) applies here as
  well.
- **BLACS.** Lowest priority. Workers spend their time in driver calls that no interrupt
  reaches, and most file access is read-only; the risk is cameras writing images in
  `transition_to_manual`. The `_quit` message exists; the wait, status, confirmation and
  kill steps are added so that closing a tab behaves the same on both platforms (today
  POSIX never kills and Windows always does). The NI_DAQmx hold means that a tab closed
  or restarted mid-shot will report the lock as held; the dialog text must not assume a
  file.

### 3.5 Caveats

- A `KeyboardInterrupt` cannot stop a long single C call, so the timeout path stays.
- A routine or script with a bare `except:` swallows the interrupt. The same timeout
  covers it.
- On Windows with Python 3.11 and 3.12 a main thread in a lock wait is not woken; one in
  `time.sleep` is. A zmq poll is not woken on Windows on any version.

## 4. Status

| Item | Status |
|---|---|
| zprocess: `interrupt_main_thread()`, `KillLock.is_held()`, `exit_when_released()`, heartbeat path | branch `interrupt-main-thread` on chrisjbillington/zprocess, 2026-10-22; pull request to follow the test runs on Ubuntu, Windows and macOS (`TESTING.md`) |
| lyse: helper, no SIGTERM stage, status query, dialog, Restart and Remove through abort | not started; on top of lyse #151 and #153 |
| runmanager | not started |
| BLACS | not started |
