# BLACS shot queue in the main thread

Written 2026-10-23. Measurement of the delay between BLACS taking a shot from the queue
and the tabs starting their transitions, and an experimental rewrite of the queue
manager (`blacs/experiment_queue.py`) that removes most of it. The rewrite is blacs
branch `queue-main-thread` (9cce66f), one commit on `statemachine-main-thread` (52b0383,
`BLACS-STATE-MACHINE.md`). It is experimental; no pull request is planned. Each fact is
labelled with how it was verified (run, read or plausible), as in `REVIEW.md`.

## 1. Summary

The queue manager thread transitions the tabs one at a time and makes a blocking call
into the main thread for each tab, each status change, each change to the abort button
and each error check. Under CPU load each such call costs several milliseconds, so with
8 tabs the transitions to buffered and to manual each took about 50 ms to start
(run). In the rewrite the main thread transitions all tabs of a group in one pass and
moves the shot from phase to phase itself; the queue manager thread is woken once per
phase, and only for work that can block. With 8 dummy tabs and 16 busy processes on 16
cores the shot cycle went from 316 ms to 251 ms (run). The rest of the cycle under load
is mostly the tabs' worker round trips and the main thread's logging, which the queue
manager does not control (plausible, from the sampled stacks in section 3).

## 2. The present design (statemachine-main-thread, 52b0383)

- **(read)** `QueueManager.manage()` runs in its own thread. Every loop iteration reads
  `manager_running` and `manager_paused` through `inmain`, and an empty or paused queue
  is polled with `time.sleep(1)`, so a shot added to an idle queue waits up to 1 s.
- **(read)** For each shot the thread makes, before the first tab is told to transition:
  `get_next_file`, two `set_status` calls, the abort button `connect` and `setEnabled`,
  all through `inmain`; then it opens the shot file to read the start and stop orders.
- **(read)** `transition_device_to_buffered` is one `inmain` call per tab, made one tab
  after another. Each tab's notification wakes the thread, which reads the tab's
  `error_message` through `inmain`. `transition_to_manual` is likewise one `inmain` call
  per tab (through `define_state` and the state queue's `put`).
- **(read)** Between the end of the run and the first transition to manual the thread
  saves the front panel to the shot file. `store_front_panel_in_h5` is decorated with
  `inmain_decorator`, so the HDF5 writes run in the main thread while the file is open
  in the queue manager thread.

## 3. Measurements of the present design

`tools/blacs-timing/bench.py`, 8 `DummyIntermediateDevice` tabs and a `DummyPseudoclock`,
50 shots of 0.1 s, Python 3.14.8, PySide6, offscreen, the maintainer's laptop (12th Gen
Core i7-1270P, 16 logical CPUs). Load is N processes that each run `while True: pass`.
Medians in ms over the shots of each run, from `tools/blacs-timing/phases.py`; two
interleaved runs of each.

| Phase | no load | load 8 | load 16 |
|---|---|---|---|
| end of previous shot to first transition to buffered | 9, 10 | 18, 17 | 35, 36 |
| first to last transition to buffered | 16, 17 | 29, 28 | 47, 51 |
| last transition to buffered to start of run | 8, 8 | 12, 16 | 28, 29 |
| run | 107, 107 | 106, 106 | 110, 109 |
| end of run to first transition to manual | 11, 11 | 8, 8 | 14, 14 |
| first to last transition to manual | 22, 23 | 28, 26 | 46, 49 |
| last transition to manual to end of shot | 9, 7 | 12, 16 | 28, 31 |
| cycle | 184, 184 | 211, 221 | 305, 327 |

**(run)** The delay that the queue manager adds grows with load: the "first to last"
rows are the time that the thread takes to tell 8 tabs, one `inmain` call each. With a
timing log added to the rewrite, the shot file read before the first transition took
13 to 21 ms under load 16, and one `inmain` call took 15 to 24 ms.

**(run)** `bench.py --sample` under load 16 on the rewrite: of the main thread's samples
in which it was running Python code, 87% were in `logging` calls, almost all in the zlog
handler's `send`, which encrypts and sends each record.

## 4. Design of the rewrite

- A `Shot` object holds the tabs of the shot being run, its phase and its start and stop
  groups. It is accessed only in the main thread. The phases are preparing, buffered,
  starting, running and manual.
- The tabs are given a `MainThreadNotifier` as their notify queue. Its `put` posts the
  item to a `Shot` method in the main thread, whichever thread calls it. Notifications
  from a phase that has ended are ignored.
- In the main thread, `Shot` transitions every tab of a start group in one pass, starts
  the next group when every tab of the group has reported back, takes the front panel
  data when all are buffered, and starts the run. When the run is done and the front
  panel has been saved, it transitions the stop groups to manual mode in the same way.
- When a phase ends, `Shot` puts one event on a `queue.Queue` that the queue manager
  thread reads: buffered (only when there are `science_starting` callbacks), running,
  done, manual, error, timeout, restart or abort. Where plugin callbacks are registered
  for a phase boundary, the main thread stops there, and the thread calls the callbacks
  and then tells the main thread to continue. The callbacks are called in the same
  order relative to the tab transitions as before.
- The thread does the work that can block: plugin callbacks, reading the shot file when
  its device orders are not known, saving the front panel, cleaning and requeueing a
  failed shot, the analysis submission and the repeat. It checks the tabs for an error
  state through one `inmain` call every 2 seconds without an event, as before.
- `process_request` reads the start and stop orders when it opens the file and stores
  them on the queue item (`DeviceOrders`, item data role `Qt.UserRole + 1`). If they are
  known and there are no `pre_transition_to_buffered` callbacks, the main-thread call
  that takes the shot from the queue also starts the transition to buffered.
- The thread waits on a `threading.Event` that is set when a row is inserted into the
  queue, the queue is paused or unpaused, or `manager_running` is set, instead of
  sleeping for 1 s.
- The front panel is saved by the thread while the run is in progress, outside the main
  thread. The transition to manual starts when the run is done and the save has
  finished.

## 5. Behaviour that changes

- **(run)** A shot added to an idle queue, or to a queue that is then unpaused, starts
  at once instead of up to 1 s later (under 0.2 s in `queuetest.py`; 0.50 s in both
  checks on `statemachine-main-thread`).
- **(run)** The front panel group, the `data` group and the `run time` attribute are
  written during the run instead of after it. A shot that is restarted during the run is
  therefore cleaned before it is requeued (before, it was requeued as it was).
- **(read)** A shot aborted during the run keeps these groups; resubmitting it makes a
  fresh copy, as for any file with a `data` group.
- **(read)** An abort during the `pre_transition_to_buffered` or `science_starting`
  callbacks ends the shot before the run starts. Before, the abort was seen only after
  the transition to buffered or after the run had been started. In both versions the
  tabs end in manual mode (run).
- **(read)** The "Running (program time: ...)" status is set by the main thread when the
  last tab is buffered, before the `science_starting` callbacks.
- **(read)** A tab in a later stop group that is restarted during the transition to
  manual is counted as failed. Before, the restart was ignored and the queue manager
  waited for it indefinitely.
- **(read)** `get_next_file`, `transition_device_to_buffered`, `get_device_error_state`,
  `_abort_buffered_devices` and the attribute `current_queue` are removed. blacs #131
  (abort the shot when BLACS closes, merged 2026-10-23) puts an abort to `current_queue`; its `stop()` is
  ported to the main-thread queue in `patches/blacs-queue-main-thread-stop.patch`, for
  when the two are combined (`LOCAL-TASKS.md`).

## 6. Results of the rewrite

**Behaviour (run).** `tools/blacs-queue/queuetest.py` checks the queue manager with the
BLACS main window, three tabs with real worker processes and stand-ins for the rest of
BLACS: group order, the order of plugin callbacks, what is saved to the shot file, and
the status, pause, requeue and abort of the tabs after a failed or hung transition, a
tab in an error state, a restart and an abort in each phase, and a failed front panel
save. The rewrite passes all 55 checks. On `statemachine-main-thread` the two checks of
start-up latency fail (0.50 s each, from the 1 s poll) and the others pass.

**Shot cycle (run).** Same set-up as section 3, interleaved with those runs.

| Phase | no load | load 8 | load 16 |
|---|---|---|---|
| end of previous shot to first transition to buffered | 2, 2 | 3, 3 | 6, 6 |
| first to last transition to buffered | 5, 6 | 8, 9 | 11, 11 |
| last transition to buffered to start of run | 16, 16 | 30, 30 | 59, 58 |
| run | 109, 110 | 114, 113 | 119, 120 |
| end of run to first transition to manual | 1, 1 | 1, 1 | 2, 2 |
| first to last transition to manual | 13, 13 | 9, 9 | 13, 14 |
| last transition to manual to end of shot | 13, 12 | 22, 22 | 42, 43 |
| cycle | 159, 160 | 184, 185 | 248, 254 |

The time before the first tab is told to transition fell from 35 to 6 ms under load 16,
and the time to tell all 8 tabs from 49 to 11 ms. Because the tabs now transition at the
same time, their worker round trips and the main thread's handling of the results
overlap, and the time from the last tab starting to the run starting is longer; the
total transition to buffered still fell from about 113 to 76 ms under load 16. The run
phase is 10 ms longer under load 16 (plausible: the front panel save in the queue
manager thread competes with the main thread for the GIL while the run is in progress,
or the "Run complete" message is now logged when the main thread processes the
notification).

## 7. What remains

1. The main thread's logging. Under load most of the main thread's time is in the zlog
   handler. A `logging.handlers.QueueHandler` in BLACS, with a `QueueListener` thread
   that sends the records, takes the send out of the main thread; in one run under load
   16 it shortened the spread of the transitions from 12 to 4 ms and the cycle from 265
   to 252 ms, within the run-to-run variation. Fewer debug messages from the state
   machine (`BLACS-STATE-MACHINE.md` section 7, item 2) reduce the formatting as well.
2. The worker round trips: per job the main thread hands the job to the tab's job
   thread, which sends it to the worker and waits for an acknowledgement before the
   result. Each is a thread or process wake-up, which costs most under load.
3. The repeat: `process_request` for a repeated shot copies the file in the queue
   manager thread before the next shot is taken. It could run in another thread when
   the queue is not empty.
4. Measure the branch on the lab machine with its real devices.
