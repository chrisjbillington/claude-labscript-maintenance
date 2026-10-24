"""Run shots through BLACS with the profile's dummy devices. Start lyse and BLACS, submit
a copy of the example shot to BLACS as runmanager does, and check that BLACS runs it and
sends it to lyse. The first shot is submitted as soon as BLACS listens on its port. Submit
the same file again, which BLACS runs as a repeat in a new file.
Time the check that BLACS makes at start-up for a process listening on its port, then
start a second copy of BLACS and check that it reports the port in use before it creates
device tabs.
Check the output of both applications for tracebacks, and BLACS.log for errors."""

import shutil
import socket
import time

from _common import (APP_STARTUP_TIMEOUT, SHOTS, app_output, check, finish, listening, load_state,
                     port, profile_dir, start_app, stop_app, wait_for_port, wait_for_port_release)

import labscript_utils.h5_lock  # noqa: F401
import h5py
import lyse
from labscript_utils.ls_zprocess import zmq_get
from labscript_utils.shared_drive import path_to_agnostic

state = load_state()
SHOT_TIMEOUT = 120

# A copy of the example shot without the run time that the compile step stamps on it.
shot = SHOTS / 'blacs_shot.h5'
repeat = SHOTS / 'blacs_shot_rep00001.h5'
for path in SHOTS.glob('blacs_shot*.h5'):
    path.unlink()
shutil.copy(state['example_shot'], shot)
with h5py.File(shot, 'r+') as f:
    del f.attrs['run time']

# BLACS logs this line when it has started.
BLACS_LOG = profile_dir() / 'logs' / 'BLACS.log'
BLACS_STARTED = 'BLACS instantiated'


def submit(path):
    return zmq_get(port('BLACS'), 'localhost', data=path_to_agnostic(str(path)), timeout=30)


def lyse_filepaths():
    try:
        df = lyse.data(port=port('lyse'), timeout=5)
    except Exception:
        return set()
    if df.empty:
        return set()
    return {str(p) for p in df['filepath']}


def wait_for_lyse(path):
    t0 = time.time()
    while time.time() - t0 < SHOT_TIMEOUT:
        if str(path) in lyse_filepaths():
            return True, time.time() - t0
        time.sleep(1)
    return False, time.time() - t0


def blacs_log():
    if not BLACS_LOG.exists():
        return ''
    return BLACS_LOG.read_text(encoding='utf8', errors='replace')


def wait_for_blacs(count_before):
    t0 = time.time()
    while time.time() - t0 < APP_STARTUP_TIMEOUT:
        if blacs_log().count(BLACS_STARTED) > count_before:
            return True, time.time() - t0
        time.sleep(0.5)
    return False, time.time() - t0


def submit_first(path, started_before):
    """Submit the shot as soon as BLACS listens on its port."""
    global d36
    try:
        return submit(path)
    except NameError as e:
        # A BLACS without the fix for D36 listens before it has started, and raises this.
        d36 = True
        check(False, f'BLACS queues a shot submitted as soon as it listens: {str(e).strip().splitlines()[-1]}',
              known='D36')
    up, seconds = wait_for_blacs(started_before)
    check(up, f'BLACS logged {BLACS_STARTED!r} after a further {seconds:.0f} s')
    return submit(path)


# A second copy of BLACS logs this, and shows it in a message box.
SECOND_BLACS_MESSAGE = 'Another copy of BLACS is probably running'
PROBE_TIMEOUT = 0.1
PROBES = 20


def probe(p):
    """Make the check that BLACS makes at start-up. Return whether the port is in use and
    the time taken."""
    t0 = time.perf_counter()
    try:
        with socket.create_connection(('127.0.0.1', p), timeout=PROBE_TIMEOUT):
            in_use = True
    except OSError:
        in_use = False
    return in_use, time.perf_counter() - t0


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def time_probes(p, in_use, description):
    results = [probe(p) for _ in range(PROBES)]
    correct = sum(r == in_use for r, _ in results)
    times = sorted(1e3 * t for _, t in results)
    check(correct == PROBES,
          f'{correct} of {PROBES} checks of {description} found it {"in use" if in_use else "free"}; '
          f'median {times[PROBES // 2]:.2f} ms, maximum {times[-1]:.2f} ms')


def check_second_blacs():
    global d40
    log_start = len(blacs_log())
    proc, log = start_app('blacs', 'blacs-second')
    running.append(('blacs-second', proc, log, None))
    t0 = time.time()
    while time.time() - t0 < APP_STARTUP_TIMEOUT:
        if SECOND_BLACS_MESSAGE in blacs_log()[log_start:] or proc.poll() is not None:
            break
        time.sleep(0.5)
    seconds = time.time() - t0
    new_log = blacs_log()[log_start:]
    reported = SECOND_BLACS_MESSAGE in new_log
    # A BLACS without the fix for D40 raises an exception when it binds its port.
    d40 = not reported
    check(reported, f'a second BLACS reported that the port is in use after {seconds:.0f} s',
          known=None if reported else 'D40')
    check('Instantiating devices' not in new_log, 'the second BLACS did not create device tabs')


def check_run(path):
    with h5py.File(path, 'r') as f:
        check('run time' in f.attrs, f'{path.name} has a run time')
        check('data' in f, f'{path.name} has a data group')


def run_shots():
    for app, port_name in [('lyse', 'lyse'), ('blacs', 'BLACS')]:
        p = port(port_name)
        if listening(p):
            check(False, f'port {p} is already in use before starting {app}')
            return
        started_before = blacs_log().count(BLACS_STARTED)
        proc, log = start_app(app)
        running.append((app, proc, log, p))
        up, seconds = wait_for_port(proc, p)
        check(up, f'{app} started and is listening on port {p} after {seconds:.0f} s')
        if not up:
            return

    response = submit_first(shot, started_before)
    check('added successfully' in response, f'BLACS accepted the shot: {response.strip()!r}')
    received, seconds = wait_for_lyse(shot)
    check(received, f'BLACS ran the shot and lyse received it after {seconds:.0f} s')
    if received:
        check_run(shot)

    response = submit(shot)
    check('re-run' in response, f'BLACS accepted the shot again as a repeat: {response.strip()!r}')
    received, seconds = wait_for_lyse(repeat)
    check(received, f'BLACS ran the repeat {repeat.name} and lyse received it after {seconds:.0f} s')
    if received:
        check_run(repeat)
        with h5py.File(repeat, 'r') as f:
            check(f.attrs.get('run repeat') == 1, f'run repeat attribute is {f.attrs.get("run repeat")!r}')

    time_probes(port('BLACS'), True, 'the BLACS port')
    time_probes(free_port(), False, 'a free port')
    check_second_blacs()


blacs_log_start = len(blacs_log())
d36 = False
d40 = False
running = []
try:
    run_shots()
finally:
    for app, proc, log, p in reversed(running):
        stop_app(proc)
        log.close()
        if p is not None:
            wait_for_port_release(p)

for app, _, _, _ in running:
    output = app_output(app)
    tracebacks = output.count('Traceback (most recent call last)')
    known = 'D36' if d36 and app == 'blacs' else 'D40' if d40 and app == 'blacs-second' else None
    check(tracebacks == 0, f'no traceback in the {app} output ({tracebacks} found)', known=known)
    if tracebacks:
        print(f'last lines of {app} output:')
        print('    ' + '\n    '.join(output.strip().splitlines()[-40:]))

# Errors in the device tabs and workers are logged in BLACS.log and not printed.
errors = [line for line in blacs_log()[blacs_log_start:].splitlines()
          if (' ERROR ' in line or ' CRITICAL ' in line or 'Traceback' in line)
          and SECOND_BLACS_MESSAGE not in line]
check(not errors, f'no errors in BLACS.log during the step ({len(errors)} found)',
      known='D36' if d36 else 'D40' if d40 else None)
for line in errors[:20]:
    print('    ' + line)

finish()
