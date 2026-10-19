"""Run shots through BLACS with dummy devices and report per-shot timings from BLACS.log.

Runs inside the mount namespace made by ns.sh; refuses to run if the profile does not
carry the bench marker file.
"""
import argparse
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import labscript_utils.h5_lock  # noqa: F401
import h5py
from labscript_profile import LABSCRIPT_SUITE_PROFILE
from labscript_utils.labconfig import LabConfig
import runmanager

from analyse import analyse, since

PROFILE = Path(LABSCRIPT_SUITE_PROFILE)
MARKER = PROFILE / '.bench-profile'
PORT = 42517

CT_HEAD = """from labscript import start, stop, AnalogOut, DigitalOut
from labscript_devices.DummyPseudoclock.labscript_devices import DummyPseudoclock
from labscript_devices.DummyIntermediateDevice import DummyIntermediateDevice

DummyPseudoclock(name='pseudoclock')
"""
CT_DEV = """DummyIntermediateDevice(name='dev{i}', parent_device=pseudoclock.clockline)
AnalogOut(name='ao{i}', parent_device=dev{i}, connection='ao0')
DigitalOut(name='do{i}', parent_device=dev{i}, connection='port0/line0')
"""
CT_TAIL = """
if __name__ == '__main__':
    start()
    stop(1.0)
"""
EXP_HEAD = """from labscript import start, stop
from labscriptlib.example_apparatus.connection_table import *

start()
"""
EXP_DEV = """do{i}.go_high(0.01)
ao{i}.constant(0.02, 0.5)
"""
EXP_TAIL = """stop({stop})
"""


def connection_table(tabs):
    return CT_HEAD + ''.join(CT_DEV.format(i=i) for i in range(tabs)) + CT_TAIL


def experiment(tabs, stop):
    return EXP_HEAD + ''.join(EXP_DEV.format(i=i) for i in range(tabs)) + EXP_TAIL.format(stop=stop)


def compile_script(script, run_file):
    results = []
    runmanager.compile_labscript_async(script, run_file, done_callback=results.append)
    if results != [True]:
        raise RuntimeError(f'compile of {script} failed')


def listening(port):
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=1):
            return True
    except OSError:
        return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--tabs', type=int, default=1, help='number of DummyIntermediateDevice tabs')
    p.add_argument('--shots', type=int, default=30)
    p.add_argument('--stop', type=float, default=0.1, help='shot length in seconds')
    p.add_argument('--label', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()

    if not MARKER.exists():
        sys.exit(f'{PROFILE} is not the bench profile; run inside ns.sh')
    if listening(PORT):
        sys.exit('something is already listening on the BLACS port')
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    config = LabConfig()
    ct_py = Path(os.path.expandvars(config.get('paths', 'connection_table_py')))
    ct_h5 = Path(os.path.expandvars(config.get('paths', 'connection_table_h5')))
    ct_py.write_text(connection_table(args.tabs))
    exp_py = ct_py.parent / 'bench_experiment.py'
    exp_py.write_text(experiment(args.tabs, args.stop))
    ct_h5.parent.mkdir(parents=True, exist_ok=True)
    if ct_h5.exists():
        ct_h5.unlink()
    runmanager.new_globals_file(str(ct_h5))
    compile_script(str(ct_py), str(ct_h5))

    shots = out / f'shots-{args.label}'
    if shots.exists():
        shutil.rmtree(shots)
    shots.mkdir()
    first = shots / 'shot_0000.h5'
    sequence_attrs, _, _ = runmanager.new_sequence_details(
        str(exp_py), config=config, increment_sequence_index=False)
    runmanager.make_single_run_file(str(first), {}, {}, sequence_attrs, 0, 1)
    compile_script(str(exp_py), str(first))
    paths = [first]
    for i in range(1, args.shots):
        path = shots / f'shot_{i:04d}.h5'
        shutil.copy(first, path)
        paths.append(path)

    blacs_log = PROFILE / 'logs' / 'BLACS.log'
    t_start = time.time()

    env = dict(os.environ, QT_QPA_PLATFORM='offscreen', PYTHONUNBUFFERED='1')
    stdout = open(out / f'blacs-stdout-{args.label}.log', 'w', buffering=1)
    proc = subprocess.Popen([sys.executable, '-m', 'blacs'], stdout=stdout,
                            stderr=subprocess.STDOUT, env=env)
    try:
        t0 = time.time()
        while not listening(PORT):
            if proc.poll() is not None:
                sys.exit('BLACS exited during start-up')
            if time.time() - t0 > 180:
                sys.exit('BLACS did not start listening')
            time.sleep(0.5)
        # Let the tabs finish initialising before shots are queued.
        time.sleep(5)
        from labscript_utils.ls_zprocess import zmq_get
        for path in paths:
            response = zmq_get(PORT, 'localhost', data=str(path), timeout=30)
            if 'added successfully' not in str(response):
                sys.exit(f'BLACS refused {path}: {response!r}')
        deadline = time.time() + args.shots * (args.stop + 5) + 60
        stdout_log = out / f'blacs-stdout-{args.label}.log'
        while True:
            text = stdout_log.read_text(errors='replace')
            if text.count('All devices are back in static mode') >= args.shots:
                break
            if time.time() > deadline:
                sys.exit('timed out waiting for the shots to run')
            if proc.poll() is not None:
                sys.exit('BLACS exited while running shots')
            time.sleep(1)
        time.sleep(1)
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
        stdout.close()
    time.sleep(2)
    saved = out / f'BLACS-{args.label}.log'
    with open(blacs_log, errors='replace') as f, open(saved, 'w') as g:
        for line in f:
            if since(line, t_start):
                g.write(line)
    print(f'log saved to {saved}')
    print(analyse(saved, args.shots))


if __name__ == '__main__':
    main()
