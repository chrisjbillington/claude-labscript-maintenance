# Plan: a Narwhal Devices Pulse Generator device for labscript-devices

Written 2026-10-23. Sections: 1 what exists, 2 goals, 3 the device and its protocol,
4 package layout, 5 labscript device, 6 BLACS worker, 7 BLACS tab, 8 runviewer parser,
9 differences from the current device, 10 testing, 11 implementation sequence,
12 decisions.

The decisions of section 12 were taken by the maintainer on 2026-10-23, and the device
was implemented the same day on the labscript-devices branch `narwhal-pulsegen`
(section 13).

## 1. What exists

Three implementations were read for this plan.

| Implementation | Location | Notes |
|---|---|---|
| Original user_devices driver | `/home/bilbo/venvs/claude-blacs-timing/user_devices.bak/NarwhalDevicesPulseGenerator` and `diginuc:~/labscript-suite/userlib/user_devices.bak` | Written for the vendor library `ndpulsegen` 1.0.1. 2673 lines including a 442-line `.ui` file and a copied PulseBlaster runviewer parser that is not registered. |
| Modified user_devices driver | `diginuc:~/labscript-suite/userlib/user_devices/NarwhalDevicesPulseGenerator` | The original with the worker blocking on the device's notification queue in 0.5 s chunks during a run instead of the tab polling the device at 10 Hz. This is what the lab runs. |
| Rewrite (shotscript) | `/home/bilbo/venvs/claude-labscript-rewrite/rewrite/src/shotscript/drivers/narwhal_pulsegen.py`, `devices/narwhal_pulsegen.py`, `devices/narwhal_pulsegen_worker.py`, `tests/narwhal_sim.py`, `tests/test_narwhal.py` | A 574-line serial driver with no vendor dependency, a vectorised compiler, a worker, a simulated device and two end-to-end tests. Different architecture. |

The lab's connection table (`diginuc:~/labscript-suite/userlib/labscriptlib/asca_clock/connection_table.py`)
uses one pulse generator as the master pseudoclock with `trigger_on_powerline=True`,
eight `DigitalOut` children and one `Trigger` child on `pulsegen.direct_outputs`, and a
camera triggered from channel 0. No clocklines, no secondary pseudoclock and no waits
are used. A shot file from 2026-10-23 has twelve instructions.

The vendor library `ndpulsegen` imports a PyQt5 GUI at import time, uses a reader thread
with 100 ms read timeouts, decodes every message into a dictionary, and connects by
opening every FTDI port in turn, which made two BLACS workers block each other and led to
a `portalocker` lock file in the worker. None of this is needed.

## 2. Goals

- Correctness: every instruction table that labscript can produce is executed with the
  times labscript computed, waits pause exactly once, and errors are reported at compile
  time where possible.
- Simplicity: one package of about 1500 lines including the driver, no dependency beyond
  `pyserial` and NumPy, no `.ui` file, no smart programming.
- Performance: no polling of the device during a run; end-of-shot latency set by the
  serial notification; one serial write to program the device.
- Feature parity with the current device: the same things can be done from a labscript
  script and from the BLACS front panel (section 9 lists the differences).
- Supported platforms as for the rest of labscript-devices: Python 3.11 to 3.15, PyQt5,
  PyQt6 and PySide6 through qtutils, Windows, Linux and macOS.

## 3. The device and its protocol

Facts from the vendor's `transcode.py` docstrings and the rewrite's driver, which
implements the same formats for firmware 1.002 or later.

- 24 digital channels, one 10 ns clock cycle, 8192 instructions of RAM.
- An instruction has a 24-bit state, a duration of 1 to 2^48-1 cycles, a `goto_address`
  and a `goto_counter` of up to 2^32-1 (after the instruction ends, jump to `goto_address`
  and decrement a volatile copy of the counter; when the copy is zero continue to the
  next address and restore the copy), and four flags: `stop_and_wait` (pause after the
  last cycle until a trigger), `hardware_trig_out`, `notify_computer` (send a
  notification with the run time in cycles when the instruction starts) and
  `powerline_sync` (when paused and this is the next instruction, resume on the next
  positive zero crossing of the mains, ignoring hardware and software triggers).
- Device options: `final_address`, `run_mode` (`single` or `continuous`),
  `accept_hardware_trigger` (`never`, `always`, `single_run`, `once`),
  `trigger_out_length` (0 to 255 cycles) and `trigger_out_delay` (cycles) of the pulse
  on the trigger-out port at the start of a run, `notify_on_main_trig_out`,
  `notify_when_run_finished` and `software_run_enable`. A software trigger sets
  `software_run_enable`; hardware triggers are ignored while it is false.
- Powerline options: `trigger_on_powerline` (every trigger starts the run at the next
  zero crossing) and `powerline_trigger_delay` (0 to 2^22-1 cycles, 41.94 ms).
- Actions: software trigger, `reset_run` (pause and reset the run; the volatile
  `goto_counter` copies are not reset, so the instructions must be written again before
  the next run), `disable_after_current_run`, and requests for the state, the powerline
  state and the run time.
- Messages from the device: state, powerline state, run time, notification (run time in
  cycles, address, flags `instruction`, `trigger_out`, `finished`), echo with device
  type, hardware version, firmware version and serial number, and error.
- The USB bridge is an FTDI FT2232 (VID 0x0403, PID 0x6010) at 12 Mbaud. The first of
  its two channels is the JTAG port of the FPGA, which Linux also exposes as a serial
  port; the driver skips it.

Timing constants, as in the current device and the rewrite: trigger delay 40 ns (four
cycles), trigger minimum duration 10 ns, minimum recovery time 20 ns, wait delay 0.

## 4. Package layout

`labscript_devices/NarwhalPulseGenerator/`, with the standard labscript-devices license
header on every file:

| File | Contents | Size |
|---|---|---|
| `__init__.py` | Empty. There is no old import path to alias. | |
| `register_classes.py` | Registers the labscript device name, the BLACS tab and the runviewer parser, as `PrawnBlaster/register_classes.py` does. | 20 lines |
| `driver.py` | `shotscript/drivers/narwhal_pulsegen.py` copied verbatim except for the two changes below. | 575 lines |
| `labscript_devices.py` | `NarwhalPulseGenerator`, its direct outputs device and the internal wait monitor devices. | ~300 lines |
| `blacs_workers.py` | `NarwhalPulseGeneratorWorker`. | ~250 lines |
| `blacs_tabs.py` | `NarwhalPulseGeneratorTab`. | ~250 lines |
| `runviewer_parsers.py` | `NarwhalPulseGeneratorParser`. | ~120 lines |

Changes to the driver on copying:

- `except TimeoutError, DeviceError:` in `connect()` is Python 3.14 syntax (PEP 758).
  Write `except (TimeoutError, DeviceError):`.
- The module docstring refers to firmware 1.002 and the vendor repository; keep it, and
  add the license header.

Everything else in the driver works on Python 3.11: `int | np.integer` in `isinstance`,
the walrus in `_read`, dataclasses, `queue.SimpleQueue`. `serial.Serial(exclusive=True)`
is accepted on every platform and enforced on POSIX; on Windows a port that another
process has open cannot be opened anyway.

`pyserial` is already a dependency of labscript-devices. No dependency is added.

## 5. The labscript device

### 5.1 Class and children

`NarwhalPulseGenerator(PseudoclockDevice)`, with the same tree as the current device and
the PulseBlaster so that connection tables look the same:

- `pulsegen.pseudoclock`: the single internal `Pseudoclock` (connection `clock`), created
  by the constructor. Users create `ClockLine(name, pulsegen.pseudoclock, 'channel n')`
  for external devices.
- `pulsegen.direct_outputs`: an `IntermediateDevice` on an internal `ClockLine`
  (connection `internal`, `ramping_allowed=False`) that accepts `DigitalOut` children,
  including `Trigger`, with connection `'channel n'`.
- When `use_wait_monitor` is true and the device is the master pseudoclock, the dummy
  pseudoclock, clockline and intermediate device and the `WaitMonitor` named
  `{name}__wait_monitor`, exactly as `PrawnBlaster/labscript_devices.py` does. The worker
  recognises itself as the wait monitor from the `waits` dataset attributes.

Connection strings are checked when the child is added: a `_NarwhalPseudoclock`
subclass checks clockline connections and the direct outputs device checks output
connections, both for the format `channel n` with n in 0 to 23 and for a channel that
is already used by a clockline or a direct output. The current device does this in
`generate_code`.

Class attributes: `clock_limit = 100e6`, `clock_resolution = 10e-9`,
`trigger_delay = 40e-9`, `trigger_minimum_duration = 10e-9`,
`minimum_recovery_time = 20e-9`, `wait_delay = 0`, `trigger_edge_type = 'rising'`,
`max_instructions = 8192`. `clock_limit` is 100 MHz because the `Pseudoclock` applies it
to every change time (`labscript/core.py:248`) and direct outputs can change every
cycle. A clock tick needs two cycles, so `generate_code` raises a `LabscriptError` for a
clock instruction with external clocklines and a step of one cycle (section 5.3). The
direct outputs device has `clock_limit = 100e6` so that the internal clockline is not
limited to a lower value.

### 5.2 Constructor

```python
NarwhalPulseGenerator(
    name,
    serial_number=None,
    trigger_device=None,
    trigger_connection=None,
    trigger_out_length=10e-9,
    trigger_out_delay=0,
    trigger_on_powerline=False,
    powerline_trigger_delay=0,
    use_wait_monitor=True,
)
```

- `serial_number`: int, or a string of digits, or None to use the only pulse generator
  that is connected. Stored as an int or None in `connection_table_properties`, and as
  `BLACS_connection` for display.
- `trigger_out_length`, `trigger_out_delay`, `powerline_trigger_delay`: seconds, checked
  against the ranges in section 3 and stored in `device_properties` as cycles. An
  out-of-range value is a `LabscriptError` at compile time.
- `trigger_on_powerline`: bool, `device_properties`.
- `use_wait_monitor`: as for the PrawnBlaster.

`wait_for_powerline(label, t, timeout=1.0)` is a method of the device: it calls
`labscript.wait(label, t, timeout)` and records `t`, so that `generate_code` sets
`powerline_sync` on the instruction after that wait (section 5.3). The device then resumes
at the next positive zero crossing of the mains plus `powerline_trigger_delay`, and
ignores hardware and software triggers while it waits, so the timeout is never used and
the default of one second only has to be longer than one mains period. The method serves
two uses: a wait whose external trigger should take effect at a zero crossing, and a wait
whose only purpose is to realign the shot with the mains phase. The wait monitor measures
it like any other wait. Starting the shot at a zero crossing is `trigger_on_powerline`,
which applies to every trigger the device receives, including those that end waits.

`device_properties` also carry `clock_limit`, `clock_resolution`, `trigger_delay`,
`trigger_minimum_duration`, `minimum_recovery_time` and `wait_delay` for the runviewer
parser, and `generate_code` adds `is_master_pseudoclock`, `stop_time` and
`used_channels` (section 5.3).

### 5.3 Code generation

`generate_code` iterates `self.pseudoclock.clock`, the list that `Pseudoclock.generate_clock`
produces: dictionaries with `start`, `step`, `reps` and `enabled_clocks`, and the string
`'WAIT'`. labscript puts a clockline with `ramping_allowed=False` only into instructions
with `reps == 1` (`labscript/core.py`, `expand_change_times`), so the direct output index
advances by one for each instruction in which the internal clockline is enabled.

For each instruction:

1. If the internal clockline is enabled, advance the direct output index and set the
   direct output bits of the 24-bit state from each output's `raw_output`.
2. Set a bit for each enabled external clockline. If there is none, emit one device
   instruction: the state for `step` cycles.
3. Otherwise emit two device instructions: the state with the clock bits set for
   `step // 2` cycles, then the state with the clock bits clear for the remaining
   `step - step // 2` cycles, with `goto_address` the first of the pair and
   `goto_counter = reps - 1`. The split is exact in cycles; the current device rounds
   both halves and lengthens odd-cycle periods by one cycle.
4. If `step` is one cycle and external clocklines are enabled, raise a `LabscriptError`
   that names the clockline and the time: a clock tick needs two cycles.
5. For `'WAIT'`: set `stop_and_wait` on the last device instruction emitted. If that
   instruction has `goto_counter > 0`, first split the last repetition off into its own
   pair of instructions (reduce the loop's counter by one and append a copy of the pair
   without the loop), so that the device pauses once and not on every repetition. If the
   wait's time is one recorded by `wait_for_powerline`, set `powerline_sync` on the next
   device instruction emitted. If nothing has been emitted yet, see section 12,
   decision 4.
6. If `reps - 1 > 2^32 - 1`, raise a `LabscriptError`. No labscript ramp needs that
   many ticks.
7. After the loop, if there are more than 8192 device instructions, raise a
   `LabscriptError` with the count.

Durations are rounded to cycles once, from `step`, so that no instruction length
accumulates floating-point error: `round(step / clock_resolution)`. A duration of
2^48 cycles is 32 days, so no splitting of long instructions is needed.

The table is written to `devices/{name}/PULSE_PROGRAM` with dtype `state <u4`,
`duration <u8`, `goto_address <u2`, `goto_counter <u4`, `stop_and_wait ?`,
`powerline_sync ?`. The row index is the address. `used_channels`, a 24-bit mask of the
channels that have a clockline or a direct output, is a device property: the worker
holds the other channels at their front panel values (section 6.3). This replaces the
`-1` sentinels in the current device's `int8` channel arrays.

## 6. The BLACS worker

### 6.1 Initialisation

`init` calls `driver.connect(serial_number)`, logs the serial number, port, hardware and
firmware versions, and does not change any device setting, so that restarting BLACS does
not disturb a run that the device is executing. `driver.connect` retries ports that
another process holds open for up to five seconds, which replaces the lock file. The
connection goes through a small method `_connect(serial_number)` so that a test can
substitute the simulated port.

`shutdown` closes the port.

### 6.2 Manual mode

- `program_manual(values)`: build the 24-bit state from the 24 front panel values and
  send `set_static_state`. Return `{}`.
- `check_remote_values()`: `get_state().state` unpacked into the 24 channel values. The
  tab enables remote value checking.
- `get_status()`: the state, powerline state and run time for the tab's status display,
  plus the notifications and errors received since the last call (three request and
  reply round trips of about a millisecond each at 12 Mbaud, once a second).
- Methods for the tab's manual controls: software trigger, `software_run_enable`,
  `disable_after_current_run`, reset, run mode, `accept_hardware_trigger`, trigger-out
  length and delay, powerline options, notification options. Each is one
  `set_options`, `set_powerline_options` or action call.

### 6.3 Transition to buffered

1. Read `PULSE_PROGRAM`, the device properties and the `waits` dataset. The worker is the
   wait monitor when `wait_monitor_acquisition_device` and `wait_monitor_timeout_device`
   are `{name}_internal_wait_monitor_outputs` and there is at least one wait.
2. Replace the state of channels not in `used_channels` by the front panel values:
   `state = (table.state & mask) | (front_panel & ~mask)`.
3. Build the driver's `INSTRUCTION_DTYPE` array: `address = arange(n)`, the table
   columns, `notify` on each `stop_and_wait` instruction and on the instruction after it
   (the two notifications that measure a wait), `trigger_out` false.
4. `set_options(accept_hardware_trigger='never', software_run_enable=False)`,
   `reset_run()`, `write_instructions(...)` (one serial write of 19 bytes per
   instruction, at most 156 KB, 0.13 s at 12 Mbaud), `set_powerline_options(...)`.
5. If `trigger_on_powerline` and the powerline state is not locked, raise an error that
   says the device has no powerline signal, instead of letting the shot hang.
6. `set_options(final_address=n-1, run_mode='single', accept_hardware_trigger='single_run',
   notify_on_trigger_out=False, notify_when_finished=True, software_run_enable=not master)`.
   The master accepts hardware triggers so that an external trigger can end a wait, but
   is gated by `software_run_enable=False` until `start_run`; the software trigger sets
   it. A secondary device is armed and starts on its hardware trigger.
7. `raise_errors()`, drain stale notifications, reset the wait bookkeeping. Return the
   final values: the last row's state unpacked into 24 channel values.

`single_run` reverts to `never` after the run, so a device that finished cannot be
restarted by a stray trigger before the next shot.

### 6.4 The run

`start_run()` (master only): drain notifications, record `time.monotonic()`, send the
software trigger.

`wait_for_run_finished(timeout)`: block on the driver's notification queue until the
`finished` notification arrives or `timeout` seconds pass, processing each notification
as it arrives (section 6.5), and checking the wait timeout. Return
`(finished, notifications, errors)` so that the tab can show them. The tab calls this
repeatedly in buffered mode (section 7.3), so an abort is delayed by at most one chunk.
This is the design of the modified driver on diginuc, which replaced 10 Hz polling of
three state requests per poll.

The modified driver also extends a chunk's deadline when the expected end of the shot
(`trigger time + stop_time`) falls within one chunk of it, so that the finish lands
inside a blocking call and not in the gap between two calls. The gap is a few
milliseconds of tab state machine, so the gain is small; keep it, as it is five lines
and only applies to the master.

### 6.5 Waits

For the master as wait monitor, from the `instruction` notifications:

- The notification for a `stop_and_wait` instruction at address `a` gives the run time
  `r` at which it started; the wait begins at `r + duration(a)`. The deadline for the
  timeout is the notification's timestamp plus `duration(a)` in seconds plus the wait's
  timeout.
- The notification for address `a + 1` gives the run time at which the run resumed; the
  wait duration is the difference in cycles times 10 ns. Post `wait_completed` with the
  label, and `all_waits_finished` after the last wait, as the PrawnBlaster worker does.
- When the deadline passes, request the state; if the device is not running and its
  current address is `a`, send a software trigger and record `timed_out`. This is the
  wait monitor's timeout pulse, in software.

A wait can be followed immediately by another wait's instruction, so the end of one wait
and the start of the next can be the same notification; the rewrite's `_update` handles
this order and is the model.

`transition_to_manual` writes `/data/waits` (label, time, timeout, duration, timed_out)
and posts `wait_durations_analysed`, as the PrawnBlaster does, then checks the state:
the device must not be running and must be at the final address. A secondary device may
finish a little after the master, so poll the state for up to two seconds before raising
an error that names the current and final addresses and, for a secondary, says that it
may not have received its trigger. Finally `set_options(accept_hardware_trigger='never')`.

`abort_buffered` and `abort_transition_to_buffered`: `accept_hardware_trigger='never'`,
`reset_run()`, return True. BLACS then calls `program_manual` with the front panel values.

### 6.6 What is not done

- No smart programming: programming is one write of at most 0.13 s, and `reset_run`
  requires it anyway.
- No device information written into the shot file at the end of each shot (section 12,
  decision 3).

## 7. The BLACS tab

### 7.1 Widgets

Built in code with `qtutils.qt` widgets, no `.ui` file. The same controls as the
current tab:

- 24 digital outputs `channel 0` to `channel 23` through `create_digital_outputs` and
  `auto_place_widgets`, sorted numerically.
- Manual control: run mode (`single`, `continuous`), Start (software trigger), Pause
  (toggle of `software_run_enable`), Stop (`disable_after_current_run`), Reset
  (`reset_run` and `accept_hardware_trigger='never'`). The loaded program stays in RAM
  after a shot, so Start replays it and continuous mode repeats it.
- Status: running, software run enable, hardware run enable, current address, final
  address, total run time.
- Trigger out: length (µs) and delay (s).
- Trigger in: `accept_hardware_trigger`, trigger on powerline, powerline delay (ms).
- Synchronisation: reference clock source, powerline frequency or "no signal".
- Notifications: the two notify options and a `QPlainTextEdit` log with
  `setMaximumBlockCount(1000)`, which replaces the custom text widget.
- Device info: serial number, firmware version, hardware version, port, filled once from
  the worker after it connects.

Two widget behaviours from the current tab are kept, in a few lines: a spin box or combo
box ignores the mouse wheel unless it has focus, and the status monitor does not write
to a widget that has focus.

### 7.2 Status monitor

`status_monitor` runs on a one-second timer in manual mode only. It calls `get_status`,
updates the widgets with signals blocked, and appends notifications and errors to the
log. The timer is removed on entering buffered mode and restored on returning to manual
mode (including after an abort) by overriding the `mode` setter, as the modified driver
does.

### 7.3 The run

```python
@define_state(MODE_BUFFERED, True)
def start_run(self, notify_queue):
    self.notify_queue = notify_queue
    yield self.queue_work(self.primary_worker, 'start_run')
    self.wait_for_run_finished()

@define_state(MODE_BUFFERED, False)
def wait_for_run_finished(self):
    finished, notifications, errors = yield self.queue_work(
        self.primary_worker, 'wait_for_run_finished', self.RUN_FINISHED_WAIT_CHUNK)
    self.log(notifications, errors)
    if finished:
        self.notify_queue.put('done')
    else:
        self.wait_for_run_finished()
```

`RUN_FINISHED_WAIT_CHUNK` is 0.5 s. The second argument of `define_state` is False so
that a queued call is discarded when the tab leaves buffered mode after an abort
(`blacs/tab_base_classes.py:160`). The experiment queue blocks on `notify_queue` with a
0.5 s timeout (`blacs/experiment_queue.py:807`), so the end-of-shot latency is the
notification's arrival plus one worker return and one tab state.

## 8. The runviewer parser

`get_traces(add_trace, clock=None)`:

1. Read `PULSE_PROGRAM` and the device properties.
2. Decode the table into rows of (high state, high duration, low state, low duration,
   repetitions, wait before): an instruction with `goto_counter > 0` is the low half of
   the preceding instruction, as `decode_pattern` in the rewrite does, with NumPy and no
   loop over instructions. The compiler produces only one- and two-instruction loops.
3. Compute the start time of each row by cumulative sum of `duration × reps`. Segments
   between waits start at 0 (master) or at the rising edges of `clock` plus
   `trigger_delay` (secondary), as the PrawnBlaster parser does. Waits of the master are
   drawn with zero length, as in the PrawnBlaster parser.
4. For each direct output child, a trace of (row start times, channel bit of the high
   state); add it with `add_trace(name, trace, f'{name}.direct_outputs', connection)`.
   `Trigger` children also go into the returned dictionary so that runviewer descends
   into the devices they trigger.
5. For each clockline child, expand the ticks (`np.repeat` and `np.arange` over the
   repetitions) into a trace that alternates 1 and 0, add it and return it.

## 9. Differences from the current device

Fixed:

- Clock periods of an odd number of cycles are lengthened by one cycle
  (`labscript_devices.py:525-552` of the original rounds both halves).
- A wait after a looping instruction pauses on every repetition
  (`labscript_devices.py:472`).
- The device is polled three times per 100 ms during a run (original only; the
  modified driver fixed this).
- Two workers connecting at once block each other (lock file, `blacs_workers.py:34`).
- Unused channels are carried as `-1` sentinels in `int8` arrays through the shot file.
- The runviewer parser raises for a secondary device (`runviewer_parsers.py:132`) and
  prints debugging output.
- `transition_to_manual` returns False, with no message, when a secondary device has not
  finished.

Dropped:

- The vendor library and `portalocker`.
- A wait whose label starts with `ACsync` making the following instruction
  powerline-synchronised. Replaced by `wait_for_powerline` (section 5.2).
- The `.ui` file and the three custom widget classes.
- Writing the firmware version, hardware version, serial number and port into the shot
  file at the end of every shot.

Kept: every constructor argument, the `pseudoclock` and `direct_outputs` properties and
the `channel n` connection strings, the internal wait monitor, every front panel control,
the status display and the notification log.

## 10. Testing

No hardware is available to a cloud session, and the lab's device is in use. The rewrite
tests its worker with a simulated device behind an object that has the `read`, `write`,
`cancel_read` and `close` methods of `serial.Serial` (`tests/narwhal_sim.py`, 285
lines), which executes instructions in real time and schedules hardware triggers. The
same approach here:

- `harness/fixtures/narwhal/`: the simulator, ported to answer the run time request
  (identifier 106) and the device state fields that the tab displays; a connection table
  with a master pulse generator (direct outputs, a `Trigger`, a clockline with a
  `DummyIntermediateDevice`) and a secondary pulse generator triggered from a direct
  output; an experiment with two waits, one ended by a simulated hardware trigger and one
  that times out.
- `harness/checks/check_narwhal.py`: compile the experiment; check the `PULSE_PROGRAM`
  tables (instruction count, durations summing to `stop_time`, the loop structure of the
  clockline, `stop_and_wait` once per wait and never on a looping instruction); run the
  runviewer parser on the shot and check the traces; instantiate the worker class with
  the simulated port, run `transition_to_buffered`, `start_run`, the
  `wait_for_run_finished` loop and `transition_to_manual`, and check `/data/waits`
  (one wait not timed out with the simulated delay, one timed out) and the final values;
  run the secondary worker without a trigger and check the error message.
- The compile check also runs a shot with an odd-cycle clock period and a wait after a
  ramp, the two cases that the current device gets wrong.
- The harness's existing `imports`, `compile`, `runviewer` and `apps` steps cover the
  package import and BLACS start-up with the new device registered.

Hardware tests for the maintainer, on diginuc with the lab's device, recorded in
`docs/TESTING.md`:

- Connect by serial number and with `serial_number=None`; connect while another process
  holds the port and see the error after five seconds.
- Manual mode: outputs, remote value check, each manual control, the status display.
- The lab's `drop_mot` experiment with `trigger_on_powerline=True`, compared with the
  current device: same `PULSE_PROGRAM` states and durations, same shot duration.
- A shot with waits and the internal wait monitor, ended by an external trigger and by
  timeout; `/data/waits`.
- Trigger-out pulse length and delay on a scope.
- A secondary pulse generator, if a second unit is available; and a wait shorter than a
  few hundred nanoseconds, to check whether `wait_delay = 0` holds.

## 11. Implementation sequence

1. Branch `narwhal-pulsegen` in a worktree of `repos/labscript-devices`. Add the package
   (section 4) and `docs/source/devices/narwhalpulsegenerator.rst` with the specifications,
   an example connection table, the use of `pseudoclock` and `direct_outputs`, waits and
   the wait monitor, powerline triggering, and the automodule entries; add it to
   `docs/source/devices.rst`.
2. Add the harness fixtures and check (section 10); run the harness locally on Python
   3.14 with PySide6.
3. Push the branch to labscript-suite/labscript-devices, dispatch
   `.github/workflows/test.yml` with `labscript-devices=labscript-suite/labscript-devices@narwhal-pulsegen`,
   record the run in `docs/TESTING.md`.
4. Open the pull request with the "Written by Claude" note, the symptom-first
   description and the verification in plain terms; add a row to
   `docs/PULL-REQUESTS.md`; add the hardware tests to `docs/LOCAL-TASKS.md`.
5. After the hardware tests pass: change the lab's connection table import to
   `labscript_devices.NarwhalPulseGenerator.labscript_devices`, make `serial_number` an
   int, recompile the connection table, remove `user_devices/NarwhalDevicesPulseGenerator`
   and the `ndpulsegen` and `portalocker` packages from the lab's environment. The BLACS
   front panel settings are keyed by device and channel names, which do not change.
6. Merge, delete the branch, update `docs/PULL-REQUESTS.md`, and add the device to the
   release notes in `docs/RELEASE-PLAN.md`.

## 12. Decisions

Taken on 2026-10-23:

1. Name: `NarwhalPulseGenerator` for the package and the class.
2. Powerline-synchronised waits are kept, as the explicit method `wait_for_powerline`
   (section 5.2), not as a wait label prefix.
3. The firmware version, hardware version, serial number and port are not written into
   the shot file.
4. Tests live in this repository's harness, not in labscript-devices, which has no test
   suite. The simulator is a harness fixture, not a `mock` option of the device.

Open:

5. A wait at t=0. Its meaning is "pause before the first instruction until a trigger",
   which is how a master device starts a shot on an external trigger, or, with
   `wait_for_powerline`, at a zero crossing without `trigger_on_powerline` applying to
   the other waits. labscript already rejects it whenever a wait monitor exists: `start()`
   pulses the wait monitor at t=0 (`labscript/labscript.py:663`), the wait pulses it at
   t=0 again, and `Trigger.trigger` raises for overlapping triggerings
   (`labscript/outputs.py:1716`). The internal wait monitor is on by default, so the
   case only compiles with `use_wait_monitor=False` and no other wait monitor, and then
   nothing measures the wait. The current device supports it with a one-cycle instruction
   that has `stop_and_wait` set before the shot's first instruction. The plan can do the
   same at the cost of a device property `wait_at_start` and three lines in the worker,
   which fill that instruction's state from the front panel so that no output changes
   before the trigger; the device pauses one cycle after the software trigger and the
   first instruction starts at the hardware trigger plus the trigger delay, so no timing
   is shifted. Recommendation: support it that way, since the hardware allows it and
   the labscript limitation with wait monitors is separate.

## 13. Implementation (2026-10-23)

Branch `narwhal-pulsegen` of labscript-suite/labscript-devices, commit bf5cbc5 on master
33e20e7: `labscript_devices/NarwhalPulseGenerator/` (`driver.py` 586 lines,
`labscript_devices.py` 460, `blacs_workers.py` 350, `blacs_tabs.py` 423,
`runviewer_parsers.py` 110, `register_classes.py`, `__init__.py`), the docs page
`docs/source/devices/narwhalpulsegenerator.rst` and its toctree entry. Differences from
the plan:

- A wait at t=0 is supported (decision 5): the program begins with a one-cycle
  instruction that waits, and the device property `wait_at_start` tells the worker to
  fill its state from the front panel.
- The status monitor is a state function allowed only in manual mode, so the timer does
  not queue it during a shot; no `mode` setter override is needed (the timer checks the
  tab's mode before queueing, `blacs/tab_base_classes.py:555`).
- Errors that the device reports are raised in the worker, which puts the tab into its
  error state, instead of being appended to the notification log. The log shows the
  notifications only.
- Manual controls go through two generic worker methods, `set_options` and
  `set_powerline_options`, which pass keyword arguments to the driver.
- The direct outputs device is named `{name}_direct_outputs`.

The harness step `narwhal` (`harness/checks/check_narwhal.py`, fixtures in
`harness/fixtures/narwhal/`) is as planned in section 10; its results are in
`TESTING.md`. The hardware tests are a task in `LOCAL-TASKS.md`.
