"""Hardware tests of the NarwhalPulseGenerator BLACS worker and driver, run with BLACS
closed. No shot uses any channel, so every channel keeps its current level."""

import logging
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import labscript_utils.h5_lock  # noqa: F401
import h5py
import runmanager
from labscript_utils.labconfig import LabConfig

from labscript_devices.NarwhalPulseGenerator import driver
from labscript_devices.NarwhalPulseGenerator.blacs_workers import NarwhalPulseGeneratorWorker

SN = 12582921
logging.basicConfig(level=logging.WARNING)
failures = 0


def check(cond, msg):
    global failures
    failures += not cond
    print('PASS' if cond else 'FAIL', msg, flush=True)


tmp = Path(tempfile.mkdtemp(prefix='narwhal-test-'))
config = LabConfig()


def compile_shot(name, body, device_args=''):
    script = tmp / f'{name}.py'
    script.write_text(
        'from labscript import start, stop, wait\n'
        'from labscript_devices.NarwhalPulseGenerator.labscript_devices import NarwhalPulseGenerator\n'
        f"NarwhalPulseGenerator('pulsegen', serial_number={SN}, trigger_out_length=0{device_args})\n"
        'start()\n' + body)
    h5 = str(tmp / f'{name}.h5')
    attrs, _, _ = runmanager.new_sequence_details(str(script), config=config, increment_sequence_index=False)
    runmanager.make_single_run_file(h5, {}, {}, attrs, 0, 1)
    results = []
    runmanager.compile_labscript_async(str(script), h5, done_callback=results.append)
    check(results == [True], f'{name} compiles')
    return h5


def busy_connect(serial_number):
    code = ('import time\nfrom labscript_devices.NarwhalPulseGenerator import driver\n'
            't0 = time.monotonic()\n'
            f'try:\n    driver.connect({serial_number})\n    print("CONNECTED")\n'
            'except driver.DeviceError as e:\n    print(f"{time.monotonic() - t0:.1f} s: {e}")\n')
    return subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, timeout=60).stdout.strip()


try:
    # ---- Connecting
    for sn in [SN, None]:
        d = driver.connect(sn)
        check(d.info.serial_number == SN and d.info.firmware_version == (1, 2),
              f'connect({sn}): {d.port}, {d.info}')
        d.close()

    w = NarwhalPulseGeneratorWorker.__new__(NarwhalPulseGeneratorWorker)
    w.device_name = 'pulsegen'
    w.serial_number = SN
    w.logger = logging.getLogger('pulsegen')
    w.init()
    print('device info', w.get_device_info())
    original = w.device.get_state()
    original_powerline = w.device.get_powerline_state()
    front = w.check_remote_values()
    print('original state', original)
    print('original powerline state', original_powerline)
    high = [ch for ch, v in front.items() if v]
    print('channels high:', high)

    # ---- Port held by this process
    for sn in [SN, None]:
        out = busy_connect(sn)
        check('in use by another process' in out and w.device.port in out and not out.startswith('CONNECTED'),
              f'connect({sn}) while the port is held: {out}')

    # ---- Manual mode
    w.program_manual(front)
    check(w.check_remote_values() == front, 'program_manual with the current values reads back the same values')
    state, powerline, run_time, notifications = w.get_status()
    check(not state.running and powerline.locked, f'get_status: running={state.running}, powerline locked={powerline.locked}, '
          f'mains period {powerline.period * driver.CYCLE * 1e3:.3f} ms, run time {run_time}')
    for options, field, value in [
        ({'run_mode': 'continuous'}, 'run_mode', 'continuous'),
        ({'run_mode': 'single'}, 'run_mode', 'single'),
        ({'accept_hardware_trigger': 'once'}, 'accept_hardware_trigger', 'once'),
        ({'accept_hardware_trigger': 'never'}, 'accept_hardware_trigger', 'never'),
        ({'trigger_out_length': 5}, 'trigger_out_length', 5),
        ({'trigger_out_delay': 123}, 'trigger_out_delay', 123),
        ({'notify_on_trigger_out': True}, 'notify_on_trigger_out', True),
        ({'notify_on_trigger_out': False}, 'notify_on_trigger_out', False),
        ({'notify_when_finished': False}, 'notify_when_finished', False),
        ({'notify_when_finished': True}, 'notify_when_finished', True),
    ]:
        w.set_options(**options)
        got = getattr(w.device.get_state(), field)
        check(got == value, f'set_options({options}): {field} = {got}')
    for options, field, value in [
        ({'trigger_on_powerline': False}, 'trigger_on_powerline', False),
        ({'trigger_delay': 1000}, 'trigger_delay', 1000),
        ({'trigger_on_powerline': True, 'trigger_delay': 0}, 'trigger_on_powerline', True),
    ]:
        w.set_powerline_options(**options)
        got = getattr(w.device.get_powerline_state(), field)
        check(got == value, f'set_powerline_options({options}): {field} = {got}')
    w.disable_after_current_run()
    w.reset_run()
    state = w.device.get_state()
    check(not state.running and w.check_remote_values() == front,
          f'disable_after_current_run and reset_run when idle: running={state.running}, outputs unchanged')

    # ---- Shots
    def run_shot(h5, timeout=10.0, expect_finish=True):
        final = w.transition_to_buffered('pulsegen', h5, front, True)
        check(final == front, 'final values are the current values')
        t0 = time.monotonic()
        w.start_run()
        finished = False
        levels_ok = True
        while not finished and time.monotonic() - t0 < timeout:
            finished, _ = w.wait_for_run_finished(0.5)
            levels_ok &= w.device.get_state().state == original.state
        elapsed = time.monotonic() - t0
        check(levels_ok, 'the outputs kept their levels during the run')
        if expect_finish:
            check(finished, f'the run finished after {elapsed:.3f} s')
            check(w.transition_to_manual() is True, 'transition_to_manual')
            check(w.check_remote_values() == front, 'the outputs end at their original levels')
        return finished, elapsed

    def waits_of(h5):
        with h5py.File(h5, 'r') as f:
            return f['data/waits'][:] if 'data/waits' in f else None

    h5 = compile_shot('plain', 'stop(0.2)\n')
    run_shot(h5)

    for powerline in [False, True]:
        h5 = compile_shot(f'timeout_powerline_{powerline}',
                          "t = 10e-3\nt += wait('w', t, timeout=0.3)\nstop(t + 10e-3)\n",
                          f', trigger_on_powerline={powerline}')
        run_shot(h5)
        waits = waits_of(h5)
        print('   /data/waits', waits)
        upper = 0.3 + (0.021 if powerline else 0.005)
        check(waits is not None and bool(waits['timed_out'][0]) and 0.29 <= waits['duration'][0] <= upper,
              f'trigger_on_powerline={powerline}: the wait timed out after {waits["duration"][0]:.4f} s (timeout 0.3 s)')

    for delay in [0, 2e-3]:
        h5 = compile_shot(f'wait_for_powerline_{delay}',
                          "t = 10e-3\nt += pulsegen.wait_for_powerline('mains', t)\nstop(t + 10e-3)\n",
                          f', powerline_trigger_delay={delay}')
        run_shot(h5)
        waits = waits_of(h5)
        print('   /data/waits', waits)
        check(waits is not None and not waits['timed_out'][0] and 0 < waits['duration'][0] <= 0.0201 + delay,
              f'wait_for_powerline with delay {delay}: {waits["duration"][0] * 1e3:.3f} ms')

    h5 = compile_shot('three_waits',
                      "t = 10e-3\nt += wait('a', t, timeout=0.2)\nt += 1e-3\n"
                      "t += pulsegen.wait_for_powerline('b', t)\nt += 1e-3\n"
                      "t += wait('c', t, timeout=0.1)\nstop(t + 1e-3)\n")
    run_shot(h5)
    waits = waits_of(h5)
    print('   /data/waits', waits)
    check(waits is not None and [x.decode() for x in waits['label']] == ['a', 'b', 'c']
          and waits['timed_out'].tolist() == [True, False, True]
          and 0.19 <= waits['duration'][0] <= 0.205 and waits['duration'][1] <= 0.0201
          and 0.09 <= waits['duration'][2] <= 0.105,
          'three waits: durations ' + ', '.join(f'{x:.4f}' for x in waits['duration']))

    # Abort during a wait
    h5 = compile_shot('abort', "t = 10e-3\nt += wait('long', t, timeout=5)\nstop(t + 10e-3)\n")
    w.transition_to_buffered('pulsegen', h5, front, True)
    w.start_run()
    finished, _ = w.wait_for_run_finished(1.0)
    state = w.device.get_state()
    check(not finished and not state.running and state.current_address == w.wait_addresses[0],
          f'during the wait: running={state.running}, address {state.current_address}')
    check(w.abort_buffered() is True, 'abort_buffered')
    state = w.device.get_state()
    check(not state.running and state.current_address == 0 and w.check_remote_values() == front,
          f'after the abort: running={state.running}, address {state.current_address}, outputs unchanged')
    w.program_manual(front)

    # A wait at t=0 with no wait monitor waits for a hardware trigger; there is none, so abort it.
    h5 = compile_shot('wait_at_start', "t = wait('go', 0, timeout=1.0)\nstop(t + 10e-3)\n",
                      ', use_wait_monitor=False')
    final = w.transition_to_buffered('pulsegen', h5, front, True)
    w.start_run()
    finished, _ = w.wait_for_run_finished(1.0)
    state = w.device.get_state()
    check(not finished and not state.running and state.current_address == 0 and state.state == original.state,
          f'wait at t=0: not finished after 1 s, running={state.running}, address {state.current_address}, outputs unchanged')
    check(w.abort_buffered() is True and w.check_remote_values() == front, 'wait at t=0: abort_buffered, outputs unchanged')
    w.program_manual(front)

finally:
    # Restore the settings that the device had before the tests.
    try:
        w.device.set_options(
            run_mode=original.run_mode,
            accept_hardware_trigger=original.accept_hardware_trigger,
            trigger_out_length=original.trigger_out_length,
            trigger_out_delay=original.trigger_out_delay,
            notify_on_trigger_out=original.notify_on_trigger_out,
            notify_when_finished=original.notify_when_finished,
            software_run_enable=original.software_run_enable,
        )
        w.device.set_powerline_options(trigger_on_powerline=original_powerline.trigger_on_powerline,
                                       trigger_delay=original_powerline.trigger_delay)
        w.device.set_static_state(original.state)
        print('restored state', w.device.get_state())
        print('restored powerline state', w.device.get_powerline_state())
        w.shutdown()
    except NameError:
        pass
    shutil.rmtree(tmp)
    print(f'{failures} failure(s)')
