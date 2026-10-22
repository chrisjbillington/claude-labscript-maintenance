"""Start one suite application with a given Qt style and colour scheme, load example
data into it, and save an image of its main window.

    python shoot.py APP --style default|fusion --scheme system|light|dark
        --data DATA.json --out IMAGE.png

APP is blacs, runmanager, lyse or runviewer. DATA.json is written by run_all.py and
holds the paths of the files to load. After the image is saved, a JSON file with the
same name as the image records the Qt binding, versions, platform, style and the
resulting colour scheme, and the process keeps running until it is killed."""

import argparse
import json
import os
import platform
import runpy
import sys
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('app', choices=['blacs', 'runmanager', 'lyse', 'runviewer'])
parser.add_argument('--style', choices=['default', 'fusion'], required=True)
parser.add_argument('--scheme', choices=['system', 'light', 'dark'], required=True)
parser.add_argument('--data', required=True)
parser.add_argument('--out', required=True)
parser.add_argument('--size', default='1500x950', help='main window size in pixels')
args = parser.parse_args()
sys.argv = [args.app]
data = json.loads(Path(args.data).read_text())
out = Path(args.out)
width, height = (int(n) for n in args.size.split('x'))

QT_ENV = os.environ.get('QT_ENV', '')
if QT_ENV == 'PyQt5' and sys.platform == 'win32':
    # Qt 5 has no colour scheme API. On Windows its dark palette is enabled with this
    # platform option and is used only when Windows is in dark mode.
    if args.scheme == 'dark':
        os.environ['QT_QPA_PLATFORM'] = 'windows:darkmode=2'

from qtutils.qt import QtCore, QtGui, QtWidgets, QT_ENV  # noqa: E402

BaseQApplication = QtWidgets.QApplication
Checked = QtCore.Qt.CheckState.Checked


def app_object():
    """The application object that the entry module creates, or None before that."""
    return getattr(sys.modules['__main__'], 'app', None)


def main_window():
    windows = [
        w for w in QtWidgets.QApplication.topLevelWidgets()
        if isinstance(w, QtWidgets.QMainWindow) and w.isVisible()
    ]
    if not windows:
        return None
    return max(windows, key=lambda w: w.width() * w.height())


def wait(seconds, condition=lambda: True):
    """Process events for at least the given number of seconds and then until condition()
    is true, for at most 120 seconds."""
    qapp = QtWidgets.QApplication.instance()
    t0 = time.monotonic()
    while time.monotonic() - t0 < seconds or not condition():
        qapp.processEvents()
        time.sleep(0.02)
        if time.monotonic() - t0 > 120:
            print('condition not met after 120 s', flush=True)
            return


def setup_runmanager(app):
    from runmanager import get_grouplist

    app.ui.lineEdit_labscript_file.setText(data['labscript_file'])
    app.open_globals_file(data['globals_file'])
    groups = get_grouplist(data['globals_file'])
    for group in groups:
        if (data['globals_file'], group) not in app.currently_open_groups:
            app.open_group(data['globals_file'], group)
    wait(5)
    app.ui.tabWidget.setCurrentIndex(app.ui.tabWidget.count() - 1)


def setup_lyse(app):
    app.singleshot_routinebox.add_routines([(data['singleshot_routine'], Checked)])
    app.multishot_routinebox.add_routines([(data['multishot_routine'], Checked)])
    for shot in data['shots']:
        app.filebox.incoming_queue.put(shot)
    model = app.filebox.shots_model
    wait(5, lambda: model.dataframe.shape[0] == len(data['shots'])
         and model.get_first_incomplete() is None)


def setup_runviewer(app):
    rv = sys.modules['__main__']

    app.load_shot(data['example_shot'])
    wait(2)
    app.shot_model.item(0, rv.SHOT_MODEL__CHECKBOX_INDEX).setCheckState(Checked)
    wait(3)
    for row in range(min(6, app.channel_model.rowCount())):
        app.channel_model.item(row, rv.CHANNEL_MODEL__CHECKBOX_INDEX).setCheckState(Checked)
    wait(5)


SETUP = {
    'runmanager': setup_runmanager,
    'lyse': setup_lyse,
    'runviewer': setup_runviewer,
    'blacs': lambda app: wait(10),
}


def save(window):
    qapp = QtWidgets.QApplication.instance()
    window.grab().save(str(out))
    hints = qapp.styleHints()
    scheme = hints.colorScheme().name if hasattr(hints, 'colorScheme') else None
    window_colour = qapp.palette().color(QtGui.QPalette.ColorRole.Window)
    info = {
        'app': args.app,
        'style_requested': args.style,
        'scheme_requested': args.scheme,
        'binding': QT_ENV,
        'qt_version': QtCore.qVersion(),
        'python': platform.python_version(),
        'os': platform.platform(),
        'qpa_platform': qapp.platformName(),
        'style': style_name,
        'style_sheet': bool(qapp.styleSheet()),
        'color_scheme': scheme,
        'window_colour': window_colour.name(),
        'window_is_dark': window_colour.lightness() < 128,
        'device_pixel_ratio': window.devicePixelRatioF(),
    }
    out.with_suffix('.json').write_text(json.dumps(info, indent=1))
    print('saved', out, flush=True)


def take_screenshot():
    poll.stop()
    app = app_object()
    window = main_window()
    window.showNormal()
    window.resize(width, height)
    wait(1)
    SETUP[args.app](app)
    window.resize(width, height)
    wait(2)
    save(window)


def check_ready():
    if app_object() is not None and main_window() is not None:
        take_screenshot()


class QApplication(BaseQApplication):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        if args.style == 'fusion':
            self.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
        if args.scheme != 'system' and hasattr(self.styleHints(), 'setColorScheme'):
            scheme = {'light': QtCore.Qt.ColorScheme.Light, 'dark': QtCore.Qt.ColorScheme.Dark}
            self.styleHints().setColorScheme(scheme[args.scheme])
        global style_name
        style_name = self.style().objectName()
        global poll
        poll = QtCore.QTimer()
        poll.timeout.connect(check_ready)
        poll.start(500)


QtWidgets.QApplication = QApplication
runpy.run_module(args.app, run_name='__main__', alter_sys=True)
