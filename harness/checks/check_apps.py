"""Start each application under the offscreen Qt platform, wait for its ZMQ server port
to accept connections, exercise the runmanager remote API, and stop it."""

import os
import time

from _common import (WORK, app_output, attempt, check, finish, listening, load_state, port,
                     start_app, stop_app, wait_for_port, wait_for_port_release)

state = load_state()
HOLD = 5

# Each app with the labconfig port that it serves.
APPS = [
    ('runmanager', 'runmanager'),
    ('runviewer', 'runviewer'),
    ('lyse', 'lyse'),
    ('blacs', 'BLACS'),
]


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
    proc, log = start_app(app)
    try:
        up, seconds = wait_for_port(proc, p)
        check(up, f'{app} started and is listening on port {p} after {seconds:.0f} s')
        if up:
            if app == 'runmanager':
                attempt('runmanager remote API', runmanager_remote)
            time.sleep(HOLD)
            check(proc.poll() is None, f'{app} still running {HOLD} s after start')
    finally:
        stop_app(proc)
        log.close()
    output = app_output(app)
    tracebacks = output.count('Traceback (most recent call last)')
    check(tracebacks == 0, f'no traceback in the {app} output ({tracebacks} found)')
    tail = output.strip().splitlines()[-15:]
    if tail:
        print(f'last lines of {app} output:')
        print('    ' + '\n    '.join(tail))
    wait_for_port_release(p)

finish()
