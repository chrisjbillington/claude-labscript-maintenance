"""Shared helpers for the check scripts. Each script runs in the harness venv with the
working directory set to the work directory."""

import json
import os
import sys
import traceback
from pathlib import Path

WORK = Path(os.environ['HARNESS_WORK'])
REPOS = Path(os.environ['HARNESS_REPOS'])
FIXTURES = Path(os.environ['HARNESS_FIXTURES'])
SHOTS = WORK / 'shots'
STATE = WORK / 'state.json'

# Written into a profile directory that the harness created, so that a later run may
# delete it. A profile without this file is never touched.
PROFILE_MARKER = '.created-by-labscript-test-harness'

_failures = 0


def check(cond, msg, known=None):
    """Record a check. `known` names an open bug that makes the check fail; the failure
    is then reported as KNOWN and not counted, and a pass is reported as FIXED so that the
    marker can be removed."""
    global _failures
    if known is not None:
        print(('FIXED ' if cond else 'KNOWN ') + msg + f' [{known}]', flush=True)
        return bool(cond)
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)
    if not cond:
        _failures += 1
    return bool(cond)


def fail(msg):
    return check(False, msg)


def attempt(msg, func, *args, **kwargs):
    """Run func and record PASS or FAIL with the exception text."""
    try:
        result = func(*args, **kwargs)
    except Exception:
        check(False, f'{msg}: {traceback.format_exc().strip().splitlines()[-1]}')
        traceback.print_exc()
        return None, False
    check(True, msg)
    return result, True


def finish():
    print(f'\n{_failures} failure(s)', flush=True)
    sys.exit(1 if _failures else 0)


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {}


def save_state(**kwargs):
    state = load_state()
    state.update(kwargs)
    STATE.write_text(json.dumps(state, indent=1))


def profile_dir():
    from labscript_profile import LABSCRIPT_SUITE_PROFILE
    return Path(LABSCRIPT_SUITE_PROFILE)


def labconfig():
    from labscript_utils.labconfig import LabConfig
    return LabConfig()


def port(name):
    return int(labconfig().get('ports', name))
