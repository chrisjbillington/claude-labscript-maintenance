# BLACS tab state machine in the main thread

Written 2026-10-23. Assessment of whether the BLACS tab state machine
(`blacs/tab_base_classes.py`) can be rewritten to be simpler and faster without breaking
existing device code, the design that follows from it, and the status of the prototype.
Line numbers refer to blacs master at cac5198. Each fact is labelled with how it was
verified (run, read or plausible), as in `REVIEW.md`.

## 1. Summary

The internals can be rewritten; the interface that device code is written against
cannot. The interface is `define_state`, generator state functions that
`yield self.queue_work(...)`, the mode bitmasks, `notify_queue`,
`statemachine_timeout_add` and, in practice, `event_queue.put`. A rewrite that keeps that
interface removes the per-tab mainloop thread and almost every blocking `inmain` call
from the path of a state. A different interface for device authors is possible only in
the full rewrite of the suite.

## 2. The present design

- **(read)** Each tab starts a thread that runs `Tab.mainloop` (`tab_base_classes.py:762-868`).
  The thread does no work of its own. It takes a state from the `StateQueue`, runs the
  state function in the main thread through `inmain`, and for a generator calls
  `__next__` and `send` through `inmain`, one call per `yield`. Between those calls it
  sends the job to the worker and waits for the acknowledgement and the result.
- **(read)** `StateQueue` (`:59-196`) is not thread-safe, so `put`, `check_for_next_item` and
  the `last_requested_state` property are each wrapped in `inmain`. The mainloop thread
  waits for a new state on a second `queue.Queue` that `put` signals and
  `check_for_next_item` re-creates.
- **(read)** A state with one worker call costs about six blocking round trips to the main
  thread: setting `last_requested_state` twice, `check_for_next_item`, the state
  function, `__next__` and `send`. Each `state` assignment adds a label and tab icon
  update in the main thread (blocking on master; posted by blacs #132).
- **(read)** `_initialise_worker` is guaranteed to be the first state only because the
  mainloop thread cannot get a state until the Qt event loop runs (comment at `:60-74`).
- **(run)** On the lab machine the mainloop overhead per transition event per tab is 30 to
  42 ms with blacs #132 and qtutils #38 applied, for a 1.78 s cycle with three tabs
  (`TESTING.md`, 2026-10-19).

## 3. Design

- The scheduler runs in the main thread. `StateQueue` is a list that only the main thread
  accesses. `put` from another thread is still a blocking `inmain`, so a caller such as
  the queue manager knows that the state is queued when `put` returns. `put` schedules a
  call to the scheduler on the next iteration of the event loop and never runs a state
  directly, so a state that queues another state does not recurse.
- Each tab has one job thread. It starts the worker process for an `init` job, checks
  that the job can be pickled, sends it, waits for the acknowledgement and the result,
  and posts the result to the main thread, which sends it into the generator. A worker
  call then costs one posted event instead of several blocking round trips.
- The scheduler's state is held in an object that `Tab.__init__` creates. A restart calls
  `__init__` again on the same tab; events that the old job thread posts after the
  restart go to the old object, which ignores them.
- Restart and close mark the scheduler closed, interrupt the worker queues as before,
  and stop the job thread. There is no mainloop thread to join.
- Nothing runs until the event loop does, so `_initialise_worker`, which has priority
  -1, is the first state by construction.
- The worker side and the wire protocol (an acknowledgement, then the result) are not
  changed. A remote worker runs the BLACS that is installed on the remote machine, which
  may be a different version.
- The log messages and the `BLACS.<device>.mainloop` logger name are kept, so that
  `tools/blacs-timing/analyse.py` measures both designs in the same way.

## 4. Behaviour that is kept

Found from the code and from device code: labscript-devices master and 14 third-party
repositories of user devices from GitHub, 329 `@define_state` uses (read).

1. `event_queue.put(allowed_states, queue_state_indefinitely, delete_stale_states, data,
   priority=0)` is called directly by the INO-quantum `FPGA_device` and `MOGLabs_QRF`
   tabs, with keyword arguments. Some calls put a bound method in `data`; the scheduler
   calls `func(self, *args, **kwargs)`, and those devices give the method an extra
   parameter to receive the second `self`. Both are kept. `event_queue.logging_enabled`
   is kept.
2. Selection: by priority, then by order of insertion; the first state allowed in the
   current mode runs; a state that is not queued indefinitely and comes before it is
   dropped; with `delete_stale_states`, consecutive entries of the same function are
   merged into the last one. The algorithm of `check_for_next_item` is kept unchanged.
3. A state that is queued from inside a state runs after it (DummyPseudoclock
   `wait_until_done`, PulseBlaster `start_run`).
4. A statemachine timeout re-arms itself through the queued state `_timeout_add`, so the
   next period starts only after the states queued before it have run.
5. A worker exception appends to `error_message` and sends `None` into the generator,
   which continues. An exception in the state function, an unpicklable job, or a worker
   that cannot start puts the tab in `fatal error` and no further states run until a
   restart. A bare `yield` after the first resends the previous job (`:846`); a bare
   first `yield` is a fatal error.
6. Other threads call state functions and read `tab.mode`, `tab.state`,
   `shutdown_workers_complete` and `finalise_close_tab` (`experiment_queue.py`,
   `__main__.py:662-705`).
7. Device tabs that override `restart` and call `DeviceTab.restart` (the camera tabs,
   iPCdev) keep working.

No device found overrides `mainloop`, subclasses `StateQueue`, uses `_mainloop_thread`,
or uses the worker's `from_parent` and `to_parent` outside the worker. Private lab code
was not searched.

## 5. Risks

- Ordering and re-entrancy errors in the new scheduler. The harness and
  `tools/blacs-timing/` cover the shot cycle; restart during a worker job, fatal errors
  and statemachine timeouts need checks of their own.
- The size of the gain is not known until it is measured. Each generator step still
  waits its turn in the main thread behind other tabs and the GUI.
- The queue manager (`experiment_queue.py`, `manage()`) is not part of this work. It
  talks to the tabs only through state calls and `notify_queue`, so it can be changed
  separately.

## 6. Status

- Branch `statemachine-main-thread` of blacs: prototype in progress.
