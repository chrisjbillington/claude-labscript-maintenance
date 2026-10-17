"""Start each application under the offscreen Qt platform, wait for its ZMQ server port
to accept connections, exercise the runmanager remote API, and stop it."""

import os
import socket
import subprocess
import sys
import time

from _common import WORK, attempt, check, finish, load_state, port

state = load_state()
STARTUP_TIMEOUT = 120
HOLD = 5

# Each app with the labconfig port that it serves.
APPS = [
    ('runmanager', 'runmanager'),
    ('runviewer', 'runviewer'),
    ('lyse', 'lyse'),
    ('blacs', 'BLACS'),
]


def listening(p):
    try:
        with socket.create_connection(('127.0.0.1', p), timeout=1):
            return True
    except OSError:
        return False


def start(app):
    log = open(WORK / 'logs' / f'app-{app}.log', 'w', encoding='utf8', errors='replace')
    proc = subprocess.Popen([sys.executable, '-X', 'utf8', '-m', app], stdout=log, stderr=subprocess.STDOUT)
    return proc, log


def stop(proc):
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def wait_for(proc, p):
    t0 = time.time()
    while time.time() - t0 < STARTUP_TIMEOUT:
        if proc.poll() is not None:
            return False, time.time() - t0
        if listening(p):
            return True, time.time() - t0
        time.sleep(0.5)
    return False, time.time() - t0


def runmanager_remote():
    from runmanager.remote import Client
    client = Client(host='localhost', port=port('runmanager'), timeout=30)
    for _ in range(60):
        try:
            client.say_hello()
            break
        except Exception:
            time.sleep(1)
    check(client.say_hello() == 'hello', 'runmanager remote say_hello')
    version = client.get_version()
    check(isinstance(version, str) and version, f'runmanager remote get_version {version}')
    client.set_labscript_file(state['example_script'])
    check(client.get_labscript_file() == state['example_script'] or
          os.path.normcase(client.get_labscript_file()) == os.path.normcase(state['example_script']),
          f'set_labscript_file and get_labscript_file: {client.get_labscript_file()}')
    check(client.error_in_globals() is False, 'error_in_globals is False with no globals')
    n = client.n_shots()
    check(n is None or isinstance(n, int), f'n_shots returns {n!r} with no globals file loaded')
    check(client.get_shuffle() is False, 'get_shuffle')
    client.set_shuffle(True)
    check(client.get_shuffle() is True, 'set_shuffle')
    client.set_shuffle(False)
    check(client.is_output_folder_default() is True, 'is_output_folder_default')
    folder = client.get_shot_output_folder()
    check(isinstance(folder, str) and folder, f'get_shot_output_folder {folder}')
    custom = str(WORK / 'custom_out')
    client.set_shot_output_folder(custom)
    check(client.is_output_folder_default() is False, 'set_shot_output_folder')
    client.reset_shot_output_folder()
    check(client.is_output_folder_default() is True, 'reset_shot_output_folder')


for app, port_name in APPS:
    p = port(port_name)
    print(f'\n--- {app} on port {p}')
    if listening(p):
        check(False, f'port {p} is already in use before starting {app}')
        continue
    proc, log = start(app)
    try:
        up, seconds = wait_for(proc, p)
        check(up, f'{app} started and is listening on port {p} after {seconds:.0f} s')
        if up:
            if app == 'runmanager':
                attempt('runmanager remote API', runmanager_remote)
            time.sleep(HOLD)
            check(proc.poll() is None, f'{app} still running {HOLD} s after start')
    finally:
        stop(proc)
        log.close()
    output = (WORK / 'logs' / f'app-{app}.log').read_text(encoding='utf8', errors='replace')
    tracebacks = output.count('Traceback (most recent call last)')
    if app == 'blacs' and tracebacks == 1 and "KeyError: 'window_xpos'" in output:
        # BLACS logs an error with a traceback from restore_window on its first launch,
        # when there are no saved window settings.
        check(False, 'no traceback in the blacs output', known='blacs first launch restore_window KeyError')
    else:
        check(tracebacks == 0, f'no traceback in the {app} output ({tracebacks} found)')
    tail = output.strip().splitlines()[-15:]
    if tail:
        print(f'last lines of {app} output:')
        print('    ' + '\n    '.join(tail))
    # Give the port time to be released before the next app or a re-run.
    for _ in range(20):
        if not listening(p):
            break
        time.sleep(0.5)

finish()
