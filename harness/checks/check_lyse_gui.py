"""Run the lyse GUI in this process under the offscreen platform. Check that a shot file
that has not been run is not loaded; that the results of single-shot routines appear in
the dataframe and the shots table when the shot is analysed, analysed again, and analysed
with a routine that fails after saving a result; that lyse code issues no
DeprecationWarning when the results add columns to the dataframe; and exercise the Abort button: a routine
that loops in Python is interrupted and its worker survives, a routine that is blocked in
a long sleep has its worker restarted, analysis is paused in both cases, and the
interrupted worker then runs a routine to completion. In a subprocess, check that the
Edit columns dialog survives being updated as 200 columns are added one at a time. The Abort checks are reported as KNOWN when
lyse has no Abort button."""

import faulthandler
import importlib.metadata
import inspect
import logging
import shutil
import subprocess
import sys
import time
import warnings
from pathlib import Path

from _common import SHOTS, WORK, check, finish, load_state

# Print the Python stack of every thread if the process crashes:
faulthandler.enable(all_threads=True)

state = load_state()
shot = state['example_shot']

# Importing the lyse entry module creates the QApplication and shows the splash, as
# starting lyse does; the application itself is created below.
import lyse.__main__ as lyse_main
import h5py
import qtutils.qt
from qtutils.qt import QtCore, QtWidgets
from labscript_utils.qtwidgets.headerview_with_widgets import HorizontalHeaderViewWithWidgets

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
# The multishot routine box logs this after each pass, which the analysis thread starts
# once it has finished with the last shot that needed analysis.
multishot_log = LogCounter('completed analysis of None')
logging.getLogger('lyse.RoutineBox.multishot').addHandler(multishot_log)


def copy_shot(name, run):
    """Copy the example shot, without its run time if run is False"""
    path = SHOTS / name
    shutil.copy(shot, path)
    if not run:
        with h5py.File(path, 'r+') as f:
            del f.attrs['run time']
    return str(path)


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
    # Shots are loaded with analysis paused, and removed before the Abort checks:
    filebox.ui.pushButton_analysis_running.setChecked(True)
    unrun_shot = copy_shot('not_run.h5', run=False)
    run_shot = copy_shot('run.h5', run=True)
    filebox.incoming_queue.put(unrun_shot)
    filebox.incoming_queue.put(run_shot)
    def loaded(path):
        return path in filebox.shots_model.row_number_by_filepath

    check(wait_until(lambda: loaded(run_shot), 60), 'a shot file that has been run is loaded')
    check(not loaded(unrun_shot) and 'has not been run' in output_text(),
          'a shot file that has not been run is not loaded')

    shots_model = filebox.shots_model
    results_scripts = {}
    for name in ['results_a', 'results_b', 'results_c']:
        results_scripts[name] = routines_dir / f'{name}.py'

    def write_results_script(name, value, fail=False):
        results_scripts[name].write_text(
            'import lyse\n'
            f'lyse.Run(lyse.path).save_result("value", {value!r})\n'
            + ('raise RuntimeError("routine failed")\n' if fail else '')
        )

    def result(name):
        column = (name, 'value') + ('',) * (shots_model.nlevels - 2)
        row = shots_model.row_number_by_filepath[run_shot]
        if column not in shots_model.dataframe.columns:
            return None, None
        item = shots_model._model.item(row, shots_model.column_indices[column])
        return shots_model.dataframe.at[row, column], item.text() if item else None

    def analyse(mark_not_done, until_paused=False):
        n_multishot = multishot_log.count
        n_paused = paused_log.count
        if mark_not_done:
            shots_model._view.selectAll()
            filebox.on_mark_selection_not_done_clicked()
        resume()
        if until_paused:
            return wait_until(lambda: paused_log.count > n_paused, 60)
        return wait_until(lambda: multishot_log.count > n_multishot, 60)

    write_results_script('results_a', 1.5)
    write_results_script('results_b', 'x')
    write_results_script('results_c', 3.5)
    box.add_routines([(str(path), QtCore.Qt.Checked) for path in results_scripts.values()])
    results_routines = dict(zip(results_scripts, box.routines))
    set_enabled(box, results_routines['results_c'], False)
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter('always', DeprecationWarning)
        check(analyse(mark_not_done=False), 'the shot is analysed by two of three routines')
    lyse_deprecations = [
        f'{Path(w.filename).name}:{w.lineno}: {w.message}' for w in caught_warnings
        if issubclass(w.category, DeprecationWarning) and 'lyse' in Path(w.filename).parts
    ]
    check(not lyse_deprecations,
          f'adding the result columns issues no DeprecationWarning in lyse: {lyse_deprecations}')
    check(result('results_a') == (1.5, '1.5') and result('results_b') == ('x', 'x'),
          'the results of both enabled routines are in the dataframe and the shots table: '
          f'{result("results_a")}, {result("results_b")}')
    check(result('results_c') == (None, None), 'the disabled routine did not run')
    check(results_routines['results_a'].done and results_routines['results_b'].done
          and not results_routines['results_c'].done, 'the routine statuses are done, done, clear')

    write_results_script('results_a', 4.5)
    write_results_script('results_b', 'y')
    check(analyse(mark_not_done=True), 'the shot is analysed again')
    check(result('results_a') == (4.5, '4.5') and result('results_b') == ('y', 'y'),
          'the new results replace the old in the dataframe and the shots table: '
          f'{result("results_a")}, {result("results_b")}')

    write_results_script('results_a', 6.5)
    write_results_script('results_b', 'z', fail=True)
    check(analyse(mark_not_done=True, until_paused=True) and filebox.analysis_paused,
          'analysis is paused after a routine error')
    check(results_routines['results_b'].error, 'the failed routine has the error status')
    check(result('results_a') == (6.5, '6.5') and result('results_b') == ('z', 'z'),
          'the results saved before the error are in the dataframe and the shots table: '
          f'{result("results_a")}, {result("results_b")}')

    box.ui.treeView.selectAll()
    box.remove_selection(confirm=False)
    shots_model._view.selectAll()
    shots_model.remove_selection(confirm=False)

    # In a subprocess, since the failure is a crash:
    edit_columns_script = (
        'from qtutils.qt import QtWidgets\n'
        'app = QtWidgets.QApplication([])\n'
        'from lyse.filebox import EditColumns\n'
        'class Filebox:\n'
        '    def set_columns_visible(self, columns_visible): pass\n'
        'names = {0: "status", 1: "filepath"}\n'
        'visible = {0: True, 1: True}\n'
        'dialog = EditColumns(Filebox(), names, visible)\n'
        'for i in range(200):\n'
        '    names[i + 2] = ("routine", f"value_{i}", "")\n'
        '    visible[i + 2] = True\n'
        '    dialog.update_columns(names, visible)\n'
        '    app.processEvents()\n'
    )
    edit_columns = subprocess.run([sys.executable, '-c', edit_columns_script],
                                  capture_output=True, text=True, timeout=300)
    if edit_columns.returncode != 0:
        print(edit_columns.stderr[-2000:], end='')
    if (qtutils.qt.QT_ENV == 'PySide6' and sys.version_info < (3, 12)
            and importlib.metadata.version('PySide6-Essentials') == '6.12.0'):
        edit_columns_known = 'D42'
    elif (qtutils.qt.QT_ENV == 'PySide6'
          and 'horizontalHeaderItem' in inspect.getsource(HorizontalHeaderViewWithWidgets)):
        edit_columns_known = 'D39'
    else:
        edit_columns_known = None
    check(edit_columns.returncode == 0,
          'the Edit columns dialog is updated 200 times as columns are added '
          f'(exit code {edit_columns.returncode})', known=edit_columns_known)

    if not check(hasattr(filebox.ui, 'pushButton_abort'), 'the filebox has an Abort button',
                 known=ABORT_FEATURE):
        finish()
    resume()

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
