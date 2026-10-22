"""Take screenshots of the four suite applications for each Qt binding, style and colour
scheme, by running shoot.py once per combination.

    python run_all.py --work HARNESS_WORK --out DIR --venv PySide6=PATH --venv PyQt6=PATH ...

HARNESS_WORK is a harness work directory in which the profile, compile and
runmanager-api steps have passed, for the profile that the applications will use. Each
venv is a harness venv with the named binding installed. Images are written to
DIR/<app>-<binding>-<style>-<scheme>.png, each with a JSON file beside it."""

import argparse
import itertools
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
APPS = ['blacs', 'runmanager', 'lyse', 'runviewer']
STYLES = ['default', 'fusion']
SCHEMES = ['light', 'dark']
TIMEOUT = 240

parser = argparse.ArgumentParser()
parser.add_argument('--work', required=True)
parser.add_argument('--out', required=True)
parser.add_argument('--venv', action='append', required=True, metavar='BINDING=PATH')
parser.add_argument('--app', action='append', choices=APPS)
parser.add_argument('--style', action='append', choices=STYLES)
parser.add_argument('--scheme', action='append', choices=SCHEMES)
args = parser.parse_args()

work = Path(args.work).resolve()
out = Path(args.out).resolve()
out.mkdir(parents=True, exist_ok=True)
state = json.loads((work / 'state.json').read_text())
profile = Path(state['profile'])

routines = out / 'routines'
routines.mkdir(exist_ok=True)
singleshot = routines / 'singleshot.py'
singleshot.write_text(
    'import lyse\n'
    'run = lyse.Run(lyse.path)\n'
    'g = run.get_globals()\n'
    "run.save_result('signal', float(g['amplitude']) * float(g['gain']))\n"
)
multishot = routines / 'multishot.py'
multishot.write_text('import lyse\ndf = lyse.data()\nprint(len(df), "shots")\n')

data = {
    'example_shot': state['example_shot'],
    'shots': sorted(str(p) for p in (work / 'runmanager_api' / 'sequence').glob('*.h5')),
    'globals_file': str(work / 'runmanager_api' / 'globals.h5'),
    'labscript_file': str(profile / 'userlib' / 'labscriptlib' / 'runmanager_test' / 'experiment.py'),
    'singleshot_routine': str(singleshot),
    'multishot_routine': str(multishot),
}
data_file = out / 'data.json'
data_file.write_text(json.dumps(data, indent=1))


def python(venv):
    if sys.platform == 'win32':
        return str(Path(venv) / 'Scripts' / 'python.exe')
    return str(Path(venv) / 'bin' / 'python')


def kill_tree(proc):
    if sys.platform == 'win32':
        subprocess.run(['taskkill', '/T', '/F', '/PID', str(proc.pid)], capture_output=True)
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    proc.wait()


venvs = dict(v.split('=', 1) for v in args.venv)
combinations = itertools.product(
    args.app or APPS, venvs.items(), args.style or STYLES, args.scheme or SCHEMES
)
for app, (binding, venv), style, scheme in combinations:
    if binding == 'PyQt5' and scheme == 'dark' and sys.platform != 'win32':
        # Qt 5 has no colour scheme API, and its dark palette option is Windows-only.
        continue
    name = f'{app}-{binding}-{style}-{scheme}'
    image = out / f'{name}.png'
    info = image.with_suffix('.json')
    info.unlink(missing_ok=True)
    log = open(out / f'{name}.log', 'w', encoding='utf8', errors='replace')
    cmd = [
        python(venv), '-X', 'utf8', str(HERE / 'shoot.py'), app, '--style', style,
        '--scheme', scheme, '--data', str(data_file), '--out', str(image),
    ]
    env = dict(os.environ, QT_ENV=binding)
    if sys.platform == 'win32':
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env,
                                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env,
                                start_new_session=True)
    t0 = time.monotonic()
    while not info.exists() and proc.poll() is None and time.monotonic() - t0 < TIMEOUT:
        time.sleep(0.5)
    if info.exists():
        print(f'{name}: {json.loads(info.read_text())}', flush=True)
    elif proc.poll() is not None:
        print(f'{name}: exited with code {proc.returncode}, see {name}.log', flush=True)
    else:
        print(f'{name}: no image after {TIMEOUT} s, see {name}.log', flush=True)
    kill_tree(proc)
    log.close()
    # Let the application's server port be released before the next start.
    time.sleep(2)
