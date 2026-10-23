"""Checks of the behaviour of the BLACS queue manager, with the BLACS main window, three
tabs that have real worker processes, and stand-ins for the rest of BLACS. Prints PASS
or FAIL for each check and exits with status 1 if any failed. Run it from this directory
with the Qt offscreen platform, inside ns.sh from tools/blacs-timing with a scratch
profile, so that the zlock and zlog servers are its own; the blacs under test is the
installed one, or the first on PYTHONPATH.

The tabs are pc (the master pseudoclock), a and b. Their start orders are 0, 0 and 1
and their stop orders are 0, 1 and 0. Each transition takes a worker job of 50 ms, and
the run lasts 100 ms. PLANS sets how each tab behaves in each step of a shot."""
import functools
import os
import shutil
import sys
import tempfile
import threading
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qtutils.qt.QtCore import QTimer
from qtutils.qt.QtWidgets import QApplication, QMainWindow
from qtutils import inmain, UiLoader
import labscript_utils.h5_lock  # noqa: F401
import h5py
import labscript_utils.properties
import blacs
import blacs.experiment_queue
from blacs.experiment_queue import QueueManager, QueueTreeview
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
DEVICES = {'pc': (0, 0), 'a': (0, 1), 'b': (1, 0)}

# Records of (time, *event), appended in the main thread and the queue manager thread:
REC = []


def rec(*event):
    REC.append((time.time(),) + event)


# Behaviour of each tab: 'ttb' and 'ttm' are 'ok', 'fail', 'error' (set an error
# message and do not report back) or 'hang' (do not report back); 'run' is 'ok' or
# 'hang':
PLANS = {name: {} for name in DEVICES}


class TestTab(Tab):
    def __init__(self, notebook, settings, restart=False):
        Tab.__init__(self, notebook, settings, restart)
        self.create_worker('w', 'queuetest_worker.TestWorker')

    @property
    def plan(self):
        return PLANS[self.device_name]

    @define_state(MODE_MANUAL, True)
    def transition_to_buffered(self, h5_file, notify_queue):
        rec(self.device_name, 'ttb')
        self.mode = MODE_TRANSITION_TO_BUFFERED
        plan = self.plan.get('ttb', 'ok')
        yield (self.queue_work('w', 'sleep', 0.05))
        if plan == 'ok':
            self.mode = MODE_BUFFERED
            rec(self.device_name, 'buffered')
            notify_queue.put([self.device_name, 'success'])
        elif plan == 'fail':
            self.mode = MODE_MANUAL
            notify_queue.put([self.device_name, 'fail'])
        elif plan == 'error':
            self.mode = MODE_MANUAL
            self.error_message = 'deliberate error'
        elif plan == 'hang':
            yield (self.queue_work('w', 'sleep', 1))
            self.mode = MODE_BUFFERED

    @define_state(MODE_BUFFERED, True)
    def start_run(self, notify_queue):
        rec(self.device_name, 'start_run')
        if self.plan.get('run', 'ok') == 'ok':
            QTimer.singleShot(100, functools.partial(self._run_done, notify_queue))

    def _run_done(self, notify_queue):
        rec(self.device_name, 'run done')
        notify_queue.put('done')

    @define_state(MODE_BUFFERED, False)
    def transition_to_manual(self, notify_queue):
        rec(self.device_name, 'ttm')
        self.mode = MODE_TRANSITION_TO_MANUAL
        plan = self.plan.get('ttm', 'ok')
        yield (self.queue_work('w', 'sleep', 0.05))
        self.mode = MODE_MANUAL
        if plan == 'ok':
            rec(self.device_name, 'manual')
            notify_queue.put([self.device_name, 'success'])
        elif plan == 'fail':
            notify_queue.put([self.device_name, 'fail'])

    @define_state(MODE_BUFFERED, False)
    def abort_buffered(self, notify_queue):
        rec(self.device_name, 'abort_buffered')
        self.mode = MODE_MANUAL
        notify_queue.put([self.device_name, 'success'])

    @define_state(ALL, True)
    def reset(self):
        self.mode = MODE_MANUAL
        self.error_message = ''


class FakeConnection(object):
    BLACS_connection = 'None'
    properties = {}


class FakeConnectionTable(object):
    master_pseudoclock = 'pc'

    def find_by_name(self, device_name):
        return FakeConnection()

    def compare_to(self, other):
        return True, None


class FakeConfig(object):
    def __init__(self, directory):
        self.directory = directory

    def get(self, section, option):
        return self.directory


class FakeFrontPanelSettings(object):
    fail = False

    def get_save_data(self):
        rec('front panel', 'get')
        return {}, {}, {}, {}

    def store_front_panel_in_h5(self, hdf5_file, *args, **kwargs):
        rec('front panel', 'store')
        if self.fail:
            raise RuntimeError('deliberate front panel save failure')
        hdf5_file.create_group('front_panel')


class FakeAnalysisSubmission(object):
    def get_queue(self):
        return self

    def put(self, item):
        rec('analysis', item[1])


class TestPlugin(object):
    """Records each callback. pre_transition_to_buffered waits for the event `block`
    if it is set."""

    def __init__(self):
        self.callbacks = set()
        self.block = None

    def get_callbacks(self):
        return {name: functools.partial(self.callback, name) for name in self.callbacks}

    def callback(self, name, path):
        rec('plugin', name)
        if name == 'pre_transition_to_buffered' and self.block is not None:
            self.block.wait(10)


ALL_CALLBACKS = {'pre_transition_to_buffered', 'science_starting', 'science_over', 'shot_complete'}


class FakeBLACS(object):
    def __init__(self, directory, tablist):
        self.exp_config = FakeConfig(directory)
        self.connection_table = FakeConnectionTable()
        self.tablist = tablist
        self.front_panel_settings = FakeFrontPanelSettings()
        self.analysis_submission = FakeAnalysisSubmission()
        self.plugins = {'test': TestPlugin()}


# blacs.plugins.get_callbacks() reads the plugins of __main__.app:
app = None

RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, ok))
    print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail if not ok else ''), flush=True)


def wait_for(condition, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if inmain(condition):
            return True
        time.sleep(0.01)
    return False


def make_shot(directory, name):
    path = os.path.join(directory, name + '.h5')
    with h5py.File(path, 'w') as f:
        for device, (start_order, stop_order) in DEVICES.items():
            f.create_group('devices/' + device)
            labscript_utils.properties.set_device_properties(
                f, device, {'start_order': start_order, 'stop_order': stop_order}
            )
    return path


def events(since, *names):
    """The events recorded since time `since` as tuples without the time, optionally
    only those of the given tabs or sources"""
    return [r[1:] for r in REC if r[0] >= since and (not names or r[1] in names)]


def first(since, event):
    for r in REC:
        if r[0] >= since and r[1:] == event:
            return r[0]
    return None


class Driver(object):
    def __init__(self, qm, blacs_app, tabs, directory):
        self.qm = qm
        self.app = blacs_app
        self.tabs = tabs
        self.directory = directory
        self.plugin = blacs_app.plugins['test']
        self.n = 0

    def new_shot(self):
        self.n += 1
        return make_shot(self.directory, 'shot_%03d' % self.n)

    def status(self):
        return self.qm.get_status()

    def queued(self):
        model = self.qm._model
        return inmain(lambda: [model.item(i).text() for i in range(model.rowCount())])

    def tabs_idle(self):
        return all(t.state == 'idle' and not t.event_queue.list_of_states for t in self.tabs.values())

    def reset(self):
        """Return the tabs, the queue and the plugins to their initial state"""
        del REC[:]
        for plan in PLANS.values():
            plan.clear()
        self.plugin.callbacks = set()
        self.plugin.block = None
        self.app.front_panel_settings.fail = False
        wait_for(lambda: self.qm._ui.queue_abort_button.isEnabled() is False, 10)
        inmain(self.qm._toggle_clear)
        wait_for(self.tabs_idle, 10)
        for tab in self.tabs.values():
            tab.reset()
        wait_for(self.tabs_idle, 10)
        self.qm.manager_paused = False
        wait_for(lambda: self.qm.get_status() == 'Idle', 5)
        del REC[:]

    def submit(self, path):
        message = self.qm.process_request(path)
        if 'added successfully' not in message:
            raise RuntimeError(message)

    def wait_status(self, text, timeout=15):
        """Wait for the queue manager to set the status to text, which it may have
        replaced since"""
        t0 = time.time()
        while time.time() - t0 < timeout:
            if any(r[1:] == ('status', text) for r in REC):
                return True
            time.sleep(0.01)
        return False

    def run(self):
        try:
            for test in [
                self.test_shot_with_callbacks,
                self.test_shot_without_callbacks,
                self.test_idle_queue_starts_promptly,
                self.test_pause,
                self.test_ttb_fail,
                self.test_ttb_error_state,
                self.test_restart_in_ttb,
                self.test_abort_in_ttb,
                self.test_abort_in_pre_transition_callback,
                self.test_abort_in_run,
                self.test_restart_in_run,
                self.test_ttm_fail,
                self.test_front_panel_save_fails,
                self.test_stop_in_run,
            ]:
                if test == self.test_stop_in_run and not hasattr(self.qm, 'stop'):
                    # QueueManager.stop() is blacs #131
                    continue
                self.reset()
                try:
                    test()
                except Exception:
                    traceback.print_exc()
                    check(test.__name__ + ' ran without an exception', False)
        except Exception:
            traceback.print_exc()
            RESULTS.append(('driver', False))
        finally:
            for tab in self.tabs.values():
                inmain(tab.close_tab)
            inmain(QApplication.instance().quit)

    def check_normal_shot(self, label, path, t0):
        ok = wait_for(lambda: first(t0, ('analysis', path)) is not None)
        check(label + ': shot completes and is sent for analysis', ok, events(t0))
        if not ok:
            return
        ttb_b = first(t0, ('b', 'ttb'))
        check(label + ': start group 1 transitions after group 0 is buffered',
              ttb_b > max(first(t0, ('pc', 'buffered')), first(t0, ('a', 'buffered'))),
              events(t0, 'pc', 'a', 'b'))
        check(label + ': the run starts after every tab is buffered',
              first(t0, ('pc', 'start_run')) > first(t0, ('b', 'buffered')), events(t0))
        ttm_a = first(t0, ('a', 'ttm'))
        check(label + ': stop group 1 transitions after group 0 is in manual mode',
              ttm_a > max(first(t0, ('pc', 'manual')), first(t0, ('b', 'manual'))), events(t0))
        check(label + ': the tabs transition to manual after the run',
              first(t0, ('pc', 'ttm')) > first(t0, ('pc', 'run done')), events(t0))
        with h5py.File(path, 'r') as f:
            saved = 'front_panel' in f and 'data' in f and 'run time' in f.attrs
        check(label + ': front panel, data group and run time saved to the shot file', saved)
        check(label + ': queue not paused', not self.qm.manager_paused)
        check(label + ': abort button disabled', not inmain(self.qm._ui.queue_abort_button.isEnabled))

    def test_shot_with_callbacks(self):
        self.plugin.callbacks = set(ALL_CALLBACKS)
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        self.check_normal_shot('with plugin callbacks', path, t0)
        e = events(t0, 'plugin', 'pc')
        expected = [
            ('plugin', 'pre_transition_to_buffered'),
            ('pc', 'ttb'),
            ('pc', 'buffered'),
            ('plugin', 'science_starting'),
            ('pc', 'start_run'),
            ('pc', 'run done'),
            ('plugin', 'science_over'),
            ('pc', 'ttm'),
            ('pc', 'manual'),
            ('plugin', 'shot_complete'),
        ]
        check('with plugin callbacks: callbacks are called in order', e == expected, e)

    def test_shot_without_callbacks(self):
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        self.check_normal_shot('without plugin callbacks', path, t0)

    def test_idle_queue_starts_promptly(self):
        time.sleep(1.5)
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        wait_for(lambda: first(t0, ('analysis', path)) is not None)
        dt = (first(t0, ('pc', 'ttb')) or float('inf')) - t0
        check('a shot added to an idle queue starts within 0.2 s', dt < 0.2, dt)

    def test_pause(self):
        self.qm.manager_paused = True
        self.wait_status('Queue paused', 5)
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        time.sleep(1.5)
        check('paused: the shot does not run', events(t0, 'pc') == [] and self.queued() == [path],
              (events(t0), self.queued()))
        t1 = time.time()
        self.qm.manager_paused = False
        wait_for(lambda: first(t1, ('analysis', path)) is not None)
        dt = (first(t1, ('pc', 'ttb')) or float('inf')) - t1
        check('unpaused: the shot starts within 0.2 s', dt < 0.2, dt)

    def check_paused_and_requeued(self, label, path):
        check(label + ': queue paused', wait_for(lambda: self.qm.manager_paused, 5))
        requeued = wait_for(lambda: self.queued()[:1] == [path], 5)
        check(label + ': shot put back at the top of the queue', requeued, self.queued())

    def test_ttb_fail(self):
        PLANS['a']['ttb'] = 'fail'
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        ok = self.wait_status('Device a in error state\nQueue paused')
        check('transition to buffered fails: status', ok, self.status())
        self.check_paused_and_requeued('transition to buffered fails', path)
        wait_for(self.tabs_idle)
        check('transition to buffered fails: start group 1 is not transitioned',
              ('b', 'ttb') not in events(t0), events(t0))
        check('transition to buffered fails: buffered tabs are aborted',
              ('pc', 'abort_buffered') in events(t0), events(t0))

    def test_ttb_error_state(self):
        PLANS['b']['ttb'] = 'error'
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        ok = self.wait_status('Device b in error state\nQueue paused')
        check('tab in an error state in transition to buffered: status', ok, self.status())
        self.check_paused_and_requeued('tab in an error state in transition to buffered', path)
        wait_for(self.tabs_idle)
        check('tab in an error state in transition to buffered: buffered tabs are aborted',
              ('pc', 'abort_buffered') in events(t0) and ('a', 'abort_buffered') in events(t0),
              events(t0))

    def test_restart_in_ttb(self):
        PLANS['b']['ttb'] = 'hang'
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        wait_for(lambda: first(t0, ('b', 'ttb')) is not None)
        inmain(self.tabs['b'].restart)
        ok = self.wait_status('Device b restarted in transition to buffered\nQueue paused')
        check('restart in transition to buffered: status', ok, self.status())
        self.check_paused_and_requeued('restart in transition to buffered', path)
        wait_for(self.tabs_idle)
        check('restart in transition to buffered: buffered tabs are aborted',
              ('pc', 'abort_buffered') in events(t0) and ('a', 'abort_buffered') in events(t0),
              events(t0))

    def test_abort_in_ttb(self):
        PLANS['b']['ttb'] = 'hang'
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        wait_for(lambda: first(t0, ('b', 'ttb')) is not None)
        inmain(self.qm._ui.queue_abort_button.click)
        ok = self.wait_status('Aborted')
        check('abort in transition to buffered: status', ok, self.status())
        check('abort in transition to buffered: queue not paused, shot not requeued',
              not self.qm.manager_paused and self.queued() == [], self.queued())
        wait_for(self.tabs_idle)
        e = events(t0)
        check('abort in transition to buffered: every tab is aborted, including the one '
              'that was transitioning', all((name, 'abort_buffered') in e for name in DEVICES), e)

    def test_abort_in_pre_transition_callback(self):
        self.plugin.callbacks = {'pre_transition_to_buffered'}
        self.plugin.block = threading.Event()
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        wait_for(lambda: first(t0, ('plugin', 'pre_transition_to_buffered')) is not None)
        inmain(self.qm._ui.queue_abort_button.click)
        self.plugin.block.set()
        ok = self.wait_status('Aborted')
        check('abort in a pre_transition_to_buffered callback: status', ok, self.status())
        wait_for(self.tabs_idle)
        time.sleep(0.5)
        modes = inmain(lambda: [t.mode for t in self.tabs.values()])
        check('abort in a pre_transition_to_buffered callback: tabs end in manual mode',
              modes == [MODE_MANUAL] * 3, (modes, events(t0)))

    def test_abort_in_run(self):
        PLANS['pc']['run'] = 'hang'
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        wait_for(lambda: first(t0, ('pc', 'start_run')) is not None)
        time.sleep(0.2)
        inmain(self.qm._ui.queue_abort_button.click)
        ok = self.wait_status('Aborted')
        check('abort in the run: status', ok, self.status())
        wait_for(self.tabs_idle)
        e = events(t0)
        check('abort in the run: every tab is aborted',
              all((name, 'abort_buffered') in e for name in DEVICES), e)
        check('abort in the run: queue not paused, shot not requeued',
              not self.qm.manager_paused and self.queued() == [], self.queued())

    def test_restart_in_run(self):
        PLANS['pc']['run'] = 'hang'
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        wait_for(lambda: first(t0, ('pc', 'start_run')) is not None)
        time.sleep(0.2)
        inmain(self.tabs['a'].restart)
        ok = self.wait_status('Device a restarted during run\nQueue paused')
        check('restart in the run: status', ok, self.status())
        self.check_paused_and_requeued('restart in the run', path)
        with h5py.File(path, 'r') as f:
            clean = 'front_panel' not in f and 'data' not in f
        check('restart in the run: requeued shot file has no front panel or data', clean)
        wait_for(self.tabs_idle)
        e = events(t0)
        check('restart in the run: the other tabs are aborted',
              ('pc', 'abort_buffered') in e and ('b', 'abort_buffered') in e, e)

    def test_ttm_fail(self):
        PLANS['b']['ttm'] = 'fail'
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        ok = self.wait_status('Device b failed to transition to manual\nQueue paused')
        check('transition to manual fails: status', ok, self.status())
        self.check_paused_and_requeued('transition to manual fails', path)
        check('transition to manual fails: stop group 1 still transitions',
              ('a', 'manual') in events(t0), events(t0))
        with h5py.File(path, 'r') as f:
            clean = 'front_panel' not in f and 'data' not in f
        check('transition to manual fails: requeued shot file has no front panel or data', clean)

    def test_front_panel_save_fails(self):
        self.app.front_panel_settings.fail = True
        path = self.new_shot()
        t0 = time.time()
        self.submit(path)
        ok = self.wait_status('Error in queue manager\nQueue paused')
        check('front panel save fails: status', ok, self.status())
        self.check_paused_and_requeued('front panel save fails', path)
        wait_for(self.tabs_idle)
        e = events(t0)
        check('front panel save fails: tabs are aborted, not transitioned to manual',
              all((name, 'abort_buffered') in e for name in DEVICES)
              and not any(name_event[1] == 'ttm' for name_event in e), e)

    def test_stop_in_run(self):
        PLANS['pc']['run'] = 'hang'
        path = self.new_shot()
        second = self.new_shot()
        t0 = time.time()
        self.submit(path)
        self.submit(second)
        wait_for(lambda: first(t0, ('pc', 'start_run')) is not None)
        time.sleep(0.2)
        inmain(self.qm.stop)
        ok = self.wait_status('Aborted, shot requeued')
        check('stop in the run: status', ok, self.status())
        check('stop in the run: queue manager thread ends',
              wait_for(lambda: not self.qm.manager.is_alive(), 5))
        check('stop in the run: shot requeued first', self.queued() == [path, second], self.queued())
        with h5py.File(path, 'r') as f:
            clean = 'front_panel' not in f and 'data' not in f
        check('stop in the run: requeued shot file has no front panel or data', clean)
        wait_for(self.tabs_idle)
        e = events(t0)
        check('stop in the run: every tab is aborted',
              all((name, 'abort_buffered') in e for name in DEVICES), e)


def main():
    global app
    qapp = QApplication(sys.argv)
    directory = tempfile.mkdtemp(prefix='queuetest-')
    # process_request() reads the connection table of a shot file; the stand-in
    # connection table accepts any shot:
    blacs.experiment_queue.ConnectionTable = lambda *args, **kwargs: None
    loader = UiLoader()
    loader.registerCustomWidget(QueueTreeview)
    ui = loader.load(os.path.join(os.path.dirname(blacs.__file__), 'main.ui'), QMainWindow())
    notebook = DragDropTabWidget()
    connection_table = FakeConnectionTable()
    tabs = {
        name: TestTab(notebook, settings={'device_name': name, 'connection_table': connection_table})
        for name in DEVICES
    }
    app = FakeBLACS(directory, tabs)
    qm = QueueManager(app, ui)
    set_status = qm.set_status

    def recording_set_status(queue_status, shot_filepath=None):
        rec('status', queue_status)
        set_status(queue_status, shot_filepath)

    qm.set_status = recording_set_status
    ui.show()
    print('blacs from', blacs.__file__, flush=True)
    driver = Driver(qm, app, tabs, directory)
    threading.Thread(target=driver.run, daemon=True).start()
    qapp.exec()
    shutil.rmtree(directory, ignore_errors=True)
    failed = [name for name, ok in RESULTS if not ok]
    print('%d checks, %d failed' % (len(RESULTS), len(failed)), flush=True)
    os._exit(1 if failed else 0)


if __name__ == '__main__':
    main()
