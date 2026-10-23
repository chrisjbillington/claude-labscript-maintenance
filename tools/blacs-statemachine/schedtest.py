"""Checks of the behaviour of the BLACS tab state machine, with two tabs that have real
worker processes. Prints PASS or FAIL for each check and exits with status 1 if any
failed. Run it from this directory with the Qt offscreen platform, inside ns.sh from
tools/blacs-timing so that the zlock and zlog servers are its own; the blacs under test
is the installed one, or the first on PYTHONPATH."""
import os
import sys
import threading
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qtutils.qt.QtCore import QTimer
from qtutils.qt.QtWidgets import QApplication, QWidget, QVBoxLayout
from qtutils import inmain
import blacs
from blacs.tab_base_classes import (
    Tab,
    define_state,
    MODE_MANUAL,
    MODE_BUFFERED,
    MODE_TRANSITION_TO_BUFFERED,
    MODE_TRANSITION_TO_MANUAL,
)
from labscript_utils.qtwidgets.dragdroptab import DragDropTabWidget

ALL = MODE_MANUAL | MODE_BUFFERED | MODE_TRANSITION_TO_BUFFERED | MODE_TRANSITION_TO_MANUAL

REC = []


class TestTab(Tab):
    def __init__(self, notebook, settings, restart=False):
        Tab.__init__(self, notebook, settings, restart)
        self.create_worker('w', 'schedtest_worker.TestWorker')

    def rec(self, *item):
        REC.append((self.device_name,) + item)

    @define_state(ALL, True)
    def s_echo(self, tag, value, delay=0):
        self.rec('start', tag)
        r = yield (self.queue_work('w', 'echo', value, delay))
        self.rec('result', tag, r)

    @define_state(ALL, True)
    def s_nested(self):
        self.rec('start', 'nested')
        self.s_echo('inner', 1)
        r = yield (self.queue_work('w', 'echo', 2))
        self.rec('result', 'nested', r)

    @define_state(MODE_MANUAL, True, True)
    def s_stale(self, n):
        self.rec('stale', n)

    @define_state(ALL, True)
    def s_set_mode(self, mode):
        self.mode = mode

    @define_state(MODE_MANUAL, True)
    def s_manual_indef(self, tag):
        self.rec('ran', tag)

    @define_state(MODE_MANUAL, False)
    def s_manual_once(self, tag):
        self.rec('ran', tag)

    @define_state(MODE_BUFFERED, True)
    def s_buffered(self, tag):
        self.rec('ran', tag)

    @define_state(ALL, True)
    def s_queue_mode_test(self):
        self.s_set_mode(MODE_BUFFERED)
        self.s_manual_indef('x')
        self.s_manual_once('y')
        self.s_buffered('z')
        self.s_set_mode(MODE_MANUAL)

    @define_state(ALL, True)
    def s_fail(self):
        r = yield (self.queue_work('w', 'fail'))
        self.rec('after fail', r)

    def bound_target(self, tab_again, value):
        self.rec('bound', tab_again is self, value)

    @define_state(ALL, True)
    def s_bare(self):
        r1 = yield (self.queue_work('w', 'echo', 'q'))
        r2 = yield
        self.rec('bare', r1, r2)

    @define_state(ALL, True)
    def s_tick(self):
        self.rec('tick')

    @define_state(ALL, True)
    def s_raise(self):
        self.rec('raising')
        raise RuntimeError('deliberate state failure')

    @define_state(ALL, True)
    def s_unpicklable(self):
        yield (self.queue_work('w', 'echo', threading.Lock()))


class FakeConnection(object):
    BLACS_connection = 'None'
    properties = {}


class FakeConnectionTable(object):
    def find_by_name(self, device_name):
        return FakeConnection()


def records(tab, since=0):
    return [r[1:] for r in REC[since:] if r[0] == tab.device_name]


def wait_for(condition, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if inmain(condition):
            return True
        time.sleep(0.02)
    return False


def idle(tab):
    return tab.state == 'idle' and not tab.event_queue.list_of_states


def wait_idle(tab, timeout=15):
    # idle twice in a row, 0.2 s apart:
    t0 = time.time()
    while time.time() - t0 < timeout:
        if wait_for(lambda: idle(tab), timeout):
            time.sleep(0.2)
            if inmain(idle, tab):
                return True
    return False


RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, ok))
    print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail if not ok else ''), flush=True)


def run_tests(tab1, tab2, app):
    try:
        _run_tests(tab1, tab2)
    except Exception:
        traceback.print_exc()
        RESULTS.append(('driver', False))
    finally:
        t0 = time.time()
        inmain(tab1.close_tab)
        inmain(tab2.close_tab)
        check('close_tab of two tabs takes under 5 s', time.time() - t0 < 5, time.time() - t0)
        inmain(app.quit)


def _run_tests(tab1, tab2):
    check('startup: tabs become idle', wait_idle(tab1) and wait_idle(tab2))

    n = len(REC)
    tab1.s_echo('a', 5)
    wait_idle(tab1)
    check('worker result is sent into the generator',
          records(tab1, n) == [('start', 'a'), ('result', 'a', 5)], records(tab1, n))

    n = len(REC)
    tab1.s_nested()
    wait_idle(tab1)
    expected = [('start', 'nested'), ('result', 'nested', 2), ('start', 'inner'), ('result', 'inner', 1)]
    check('a state queued by a state runs after it', records(tab1, n) == expected, records(tab1, n))

    n = len(REC)
    tab1.s_echo('slow', 0, 0.5)
    tab1.s_stale(1)
    tab1.s_stale(2)
    tab1.s_stale(3)
    wait_idle(tab1)
    expected = [('start', 'slow'), ('result', 'slow', 0), ('stale', 3)]
    check('delete_stale_states keeps the last of consecutive entries', records(tab1, n) == expected,
          records(tab1, n))

    n = len(REC)
    tab1.s_queue_mode_test()
    wait_idle(tab1)
    expected = [('ran', 'z'), ('ran', 'x')]
    check('mode selection: allowed state runs, non-indefinite state is dropped, indefinite waits',
          records(tab1, n) == expected, records(tab1, n))

    n = len(REC)
    tab1.s_fail()
    wait_idle(tab1)
    err = inmain(lambda: tab1.error_message).replace('&nbsp;', ' ')
    check('worker exception: None is sent and the state continues',
          records(tab1, n) == [('after fail', None)], records(tab1, n))
    check('worker exception: error message shown', 'deliberate worker failure' in err, err[:200])
    inmain(setattr, tab1, 'error_message', '')

    n = len(REC)
    tab1.event_queue.put(allowed_states=ALL, queue_state_indefinitely=True, delete_stale_states=False,
                         data=[tab1.bound_target, [[7], {}]])
    wait_idle(tab1)
    check('event_queue.put with a bound method passes the tab again',
          records(tab1, n) == [('bound', True, 7)], records(tab1, n))

    n = len(REC)
    tab1.s_bare()
    wait_idle(tab1)
    check('a bare yield repeats the previous job', records(tab1, n) == [('bare', 'q', 'q')], records(tab1, n))

    n = len(REC)
    inmain(tab1.statemachine_timeout_add, 100, tab1.s_tick)
    time.sleep(1.05)
    inmain(tab1.statemachine_timeout_remove, tab1.s_tick)
    ticks = len(records(tab1, n))
    time.sleep(0.5)
    wait_idle(tab1)
    after = len(records(tab1, n))
    check('statemachine timeout runs about every 100 ms', 6 <= ticks <= 12, ticks)
    check('statemachine timeout stops after removal', after <= ticks + 1, (ticks, after))

    n = len(REC)
    tab1.s_echo('t1', 1, 0.3)
    tab1.s_echo('t2', 2)
    wait_idle(tab1)
    expected = [('start', 't1'), ('result', 't1', 1), ('start', 't2'), ('result', 't2', 2)]
    check('states queued from another thread run in order', records(tab1, n) == expected, records(tab1, n))

    n = len(REC)
    t0 = time.time()
    tab1.s_echo('p1', 1, 1.0)
    tab2.s_echo('p2', 2, 1.0)
    wait_idle(tab1)
    wait_idle(tab2)
    dt = time.time() - t0
    check('worker jobs of two tabs run in parallel', dt < 1.8, dt)

    n = len(REC)
    tab1.s_echo('long', 0, 5)
    time.sleep(0.5)
    t0 = time.time()
    inmain(tab1.restart)
    time.sleep(0.5)
    wait_idle(tab1)
    tab1.s_echo('after restart', 9)
    wait_idle(tab1)
    recs = records(tab1, n)
    check('restart during a worker job: the new worker runs states',
          ('result', 'after restart', 9) in recs, recs)
    check('restart during a worker job: the old result is discarded',
          not any(r[:2] == ('result', 'long') for r in recs), recs)
    check('restart during a worker job takes under 5 s', time.time() - t0 < 5, time.time() - t0)
    check('restart: no error', inmain(lambda: tab1.error_message) == '', inmain(lambda: tab1.error_message)[:300])

    n = len(REC)
    tab1.s_raise()
    wait_for(lambda: tab1.state == 'fatal error')
    tab1.s_echo('dead', 0)
    time.sleep(1)
    check('exception in a state: fatal error', inmain(lambda: tab1.state) == 'fatal error')
    check('exception in a state: no further states run', records(tab1, n) == [('raising',)], records(tab1, n))
    check('exception in a state: message shown', 'deliberate state failure' in inmain(lambda: tab1.error_message).replace('&nbsp;', ' '))
    inmain(tab1.restart)
    time.sleep(0.5)
    wait_idle(tab1)
    n = len(REC)
    tab1.s_echo('recovered', 3)
    wait_idle(tab1)
    check('restart after a fatal error', records(tab1, n) == [('start', 'recovered'), ('result', 'recovered', 3)],
          records(tab1, n))

    tab2.s_unpicklable()
    wait_for(lambda: tab2.state == 'fatal error')
    err = inmain(lambda: tab2.error_message).replace('&nbsp;', ' ')
    check('unpicklable job: fatal error with message',
          inmain(lambda: tab2.state) == 'fatal error' and 'unserialisable' in err, err[:300])


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)
    notebook = DragDropTabWidget()
    layout.addWidget(notebook)
    ct = FakeConnectionTable()
    tab1 = TestTab(notebook, settings={'device_name': 'tab1', 'connection_table': ct})
    tab2 = TestTab(notebook, settings={'device_name': 'tab2', 'connection_table': ct})
    window.show()
    print('blacs from', blacs.__file__, flush=True)
    threading.Thread(target=run_tests, args=(tab1, tab2, app), daemon=True).start()
    app.exec()
    failed = [name for name, ok in RESULTS if not ok]
    print('%d checks, %d failed' % (len(RESULTS), len(failed)), flush=True)
    os._exit(1 if failed else 0)


if __name__ == '__main__':
    main()
