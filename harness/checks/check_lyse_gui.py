"""Run the lyse GUI in this process under the offscreen platform and exercise the Abort
button: a routine that loops in Python is interrupted and its worker survives, a routine
that is blocked in a long sleep has its worker restarted, analysis is paused in both
cases, and the interrupted worker then runs a routine to completion. The checks are
reported as KNOWN when lyse has no Abort button."""

import logging
import sys
import time
from pathlib import Path

from _common import WORK, check, finish, load_state

state = load_state()
shot = state['example_shot']

# Importing the lyse entry module creates the QApplication and shows the splash, as
# starting lyse does; the application itself is created below.
import lyse.__main__ as lyse_main
from qtutils.qt import QtCore, QtWidgets

qapplication = QtWidgets.QApplication.instance()

ABORT_FEATURE = 'lyse #153'
routines_dir = WORK / 'routines'
routines_dir.mkdir(exist_ok=True)
loop_script = routines_dir / 'loop_routine.py'
loop_marker = routines_dir / 'loop_routine.running'
sleep_script = routines_dir / 'sleep_routine.py'
sleep_marker = routines_dir / 'sleep_routine.running'
loop_marker.unlink(missing_ok=True)
sleep_marker.unlink(missing_ok=True)
loop_script.write_text(
    'import time\n'
    'from pathlib import Path\n'
    f'Path({str(loop_marker)!r}).touch()\n'
    'while True:\n'
    '    time.sleep(0.01)\n'
)
sleep_script.write_text(
    'import time\n'
    'from pathlib import Path\n'
    f'Path({str(sleep_marker)!r}).touch()\n'
    'time.sleep(600)\n'
)


def wait_until(cond, timeout):
    """Process Qt events until cond() is true or timeout seconds have passed."""
    t0 = time.monotonic()
    while True:
        qapplication.processEvents()
        if cond():
            return True
        if time.monotonic() - t0 > timeout:
            return False
        time.sleep(0.05)


class LogCounter(logging.Handler):
    """Counts the records with a given message."""

    def __init__(self, message):
        super().__init__()
        self.message = message
        self.count = 0

    def emit(self, record):
        if record.getMessage() == self.message:
            self.count += 1


# The analysis thread logs this once it has paused after a routine error and has nothing
# more to do. Resuming before then is undone by the pause that the error causes.
paused_log = LogCounter('analysis is paused')
logging.getLogger('lyse.FileBox.analysis_loop').addHandler(paused_log)


def set_enabled(box, routine, enabled):
    item = box.model.item(routine.get_row_index(), box.COL_ACTIVE)
    item.setCheckState(QtCore.Qt.Checked if enabled else QtCore.Qt.Unchecked)


def resume():
    app.filebox.ui.pushButton_analysis_running.setChecked(False)


def output_text():
    return app.output_box.output_textedit.toPlainText()


app = lyse_main.Lyse(qapplication)
lyse_main.splash.hide()
filebox = app.filebox
box = app.singleshot_routinebox
try:
    if not check(hasattr(filebox.ui, 'pushButton_abort'), 'the filebox has an Abort button',
                 known=ABORT_FEATURE):
        finish()

    box.add_routines([(str(loop_script), QtCore.Qt.Checked)])
    loop_routine = box.routines[0]
    filebox.incoming_queue.put(shot)
    check(wait_until(loop_marker.exists, 120), 'the looping routine started on the shot')
    check(wait_until(lambda: loop_routine.working, 10), 'the routine is marked as working')
    worker = loop_routine.worker
    n_paused = paused_log.count
    t0 = time.monotonic()
    filebox.ui.pushButton_abort.click()
    stopped = wait_until(lambda: loop_routine.error, loop_routine.ABORT_TIMEOUT + 30)
    elapsed = time.monotonic() - t0
    check(stopped, f'the looping routine stopped {elapsed:.1f} s after Abort')
    check(elapsed < loop_routine.ABORT_TIMEOUT,
          'the routine stopped before the worker restart timeout')
    check(loop_routine.worker is worker and worker.poll() is None,
          'the worker survived the interrupt')
    check(filebox.analysis_paused, 'analysis is paused after Abort')
    check(wait_until(lambda: 'Interrupted' in output_text(), 10),
          'the output box reports the interrupt')
    check(wait_until(lambda: paused_log.count > n_paused, 10), 'the analysis thread is idle')

    box.add_routines([(str(sleep_script), QtCore.Qt.Checked)])
    sleep_routine = box.routines[1]
    set_enabled(box, loop_routine, False)
    resume()
    check(wait_until(sleep_marker.exists, 120), 'the sleeping routine started on the shot')
    check(wait_until(lambda: sleep_routine.working, 10), 'the sleeping routine is marked as working')
    worker = sleep_routine.worker
    n_paused = paused_log.count
    t0 = time.monotonic()
    filebox.ui.pushButton_abort.click()
    stopped = wait_until(lambda: sleep_routine.error, sleep_routine.ABORT_TIMEOUT + 60)
    elapsed = time.monotonic() - t0
    check(stopped, f'the sleeping routine stopped {elapsed:.1f} s after Abort')
    check(sleep_routine.worker is not worker and worker.poll() is not None,
          'the unresponsive worker was replaced')
    check(sleep_routine.worker.poll() is None, 'the new worker is running')
    check(filebox.analysis_paused, 'analysis is paused after the worker restart')
    check(wait_until(lambda: paused_log.count > n_paused, 10), 'the analysis thread is idle')

    loop_script.write_text('print("completed")\n')
    set_enabled(box, loop_routine, True)
    set_enabled(box, sleep_routine, False)
    resume()
    check(wait_until(lambda: loop_routine.done, 60), 'the interrupted worker ran the routine to completion')
    check(wait_until(lambda: filebox.shots_model.get_first_incomplete() is None, 10),
          'the shot is marked as analysed')
    check(not filebox.analysis_paused, 'analysis is still running')
finally:
    app.terminate_all_workers()
    wait_until(lambda: all(app.workers_terminated().values()), 15)
    app.server.shutdown()
finish()
