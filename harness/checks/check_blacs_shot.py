"""Run shots through BLACS with the profile's dummy devices. Start lyse and BLACS, submit
a copy of the example shot to BLACS as runmanager does, and check that BLACS runs it and
sends it to lyse. The first shot is submitted as soon as BLACS listens on its port. Submit the same file again, which BLACS runs as a repeat in
a new file.
Check the output of both applications for tracebacks, and BLACS.log for errors."""

import shutil
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


blacs_log_start = len(blacs_log())
d36 = False
running = []
try:
    run_shots()
finally:
    for app, proc, log, p in reversed(running):
        stop_app(proc)
        log.close()
        wait_for_port_release(p)

for app, _, _, _ in running:
    output = app_output(app)
    tracebacks = output.count('Traceback (most recent call last)')
    known = 'D36' if d36 and app == 'blacs' else None
    check(tracebacks == 0, f'no traceback in the {app} output ({tracebacks} found)', known=known)
    if tracebacks:
        print(f'last lines of {app} output:')
        print('    ' + '\n    '.join(output.strip().splitlines()[-40:]))

# Errors in the device tabs and workers are logged in BLACS.log and not printed.
errors = [line for line in blacs_log()[blacs_log_start:].splitlines()
          if ' ERROR ' in line or ' CRITICAL ' in line or 'Traceback' in line]
check(not errors, f'no errors in BLACS.log during the step ({len(errors)} found)',
      known='D36' if d36 else None)
for line in errors[:20]:
    print('    ' + line)

finish()
