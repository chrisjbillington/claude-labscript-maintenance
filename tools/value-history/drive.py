"""Run runmanager under the offscreen platform, exercise the value history and save
screenshots.

    python drive.py --out DIR --labscript-file FILE [--scheme light|dark]
"""

import argparse
import os
import runpy
import sys
import time
import traceback
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
parser.add_argument('--labscript-file', required=True)
parser.add_argument('--scheme', default='light')
args = parser.parse_args()
sys.argv = ['runmanager']
out = Path(args.out)
out.mkdir(parents=True, exist_ok=True)

from qtutils.qt import QtCore, QtGui, QtWidgets  # noqa: E402

BaseQApplication = QtWidgets.QApplication
results = []


def check(condition, message):
    results.append((bool(condition), message))
    print('PASS' if condition else 'FAIL', message, flush=True)


def wait(seconds, condition=lambda: True, limit=120):
    qapp = QtWidgets.QApplication.instance()
    t0 = time.monotonic()
    while time.monotonic() - t0 < seconds or not condition():
        qapp.processEvents()
        time.sleep(0.02)
        if time.monotonic() - t0 > limit:
            print('condition not met', flush=True)
            return False
    return True


def main_window():
    for w in QtWidgets.QApplication.topLevelWidgets():
        if isinstance(w, QtWidgets.QMainWindow) and w.isVisible():
            return w
    return None


def popups():
    from runmanager.widgets import HistoryPopup
    return [w for w in QtWidgets.QApplication.topLevelWidgets()
            if isinstance(w, HistoryPopup) and w.isVisible()]


def save(name, extra=None):
    """Save the main window, with the visible popup or the given widget drawn over it"""
    window = main_window()
    pixmap = window.grab()
    painter = QtGui.QPainter(pixmap)
    for widget in popups() + ([extra] if extra is not None else []):
        painter.drawPixmap(window.mapFromGlobal(widget.mapToGlobal(QtCore.QPoint(0, 0))), widget.grab())
    painter.end()
    path = out / f'{name}-{args.scheme}.png'
    pixmap.save(str(path))
    print('saved', path, flush=True)


def crop(name, rect):
    path = out / f'{name}-{args.scheme}.png'
    QtGui.QPixmap(str(path)).copy(rect).save(str(path))


def run():
    poll.stop()
    rm = sys.modules['__main__']
    app = rm.app
    from runmanager import group_manager as gm
    window = main_window()
    window.showNormal()
    window.resize(1300, 700)
    wait(1)

    globals_file = str(out / 'globals.h5')
    if os.path.exists(globals_file):
        os.remove(globals_file)
    gm.new_globals_file(globals_file)
    gm.new_group(globals_file, 'MOT')
    values = {
        'amplitude': ('0.25  # optimised for loading', 'V'),
        'gain': ('2', ''),
        'duration': ('0.5', 's'),
        'use_do': ('True', ''),
        'mot_detuning': ('-12e6  # 2 linewidths', 'Hz'),
        'repump_power': ('0.8', 'mW'),
        'load_time': ('1.5  # was 2.0, shortened for faster cycle', 's'),
        'imaging_delay': ('linspace(0, 10e-3, 11)', 's'),
        'probe_frequency': ('# 80e6\n85e6  # shifted by the new AOM', 'Hz'),
    }
    for name, (value, units) in values.items():
        gm.new_global(globals_file, 'MOT', name)
        gm.set_value(globals_file, 'MOT', name, value)
        gm.set_units(globals_file, 'MOT', name, units)
    gm.set_expansion(globals_file, 'MOT', 'imaging_delay', 'outer', custom=False)
    groups = {'MOT': globals_file}
    # Older uses, so that the screenshot shows a realistic history:
    now = time.time()
    older = [
        (now - 21 * 86400, {'mot_detuning': '-10e6', 'repump_power': '1.0'}),
        (now - 14 * 86400, {'mot_detuning': '-15e6  # Dec 2025 setting', 'repump_power': '1.2'}),
        (now - 9 * 86400, {'mot_detuning': '-10e6', 'repump_power': '1.0'}),
        (now - 3 * 86400, {'mot_detuning': '-15e6  # Dec 2025 setting', 'repump_power': '0.6'}),
        (now - 2 * 86400, {'mot_detuning': '-15e6', 'repump_power': '0.6'}),
        (now - 26 * 3600, {'mot_detuning': '-24e6  # 4 linewidths, for imaging test', 'repump_power': '0.8'}),
        (now - 5 * 3600, {'mot_detuning': '-12e6', 'repump_power': '0.8'}),
    ]
    for t, overrides in older:
        sequence_globals = gm.get_globals(groups)
        for name, value in overrides.items():
            _, units, expansion = sequence_globals['MOT'][name]
            sequence_globals['MOT'][name] = (value, units, expansion)
        gm.record_history(groups, sequence_globals, gm.get_custom_expansions(groups), now=t)
    app.ui.lineEdit_labscript_file.setText(args.labscript_file)
    app.ui.checkBox_run_shots.setChecked(False)
    app.ui.checkBox_view_shots.setChecked(False)
    app.open_globals_file(globals_file)
    app.open_group(globals_file, 'MOT')
    app.get_group_item_by_name(globals_file, 'MOT', app.GROUPS_COL_ACTIVE).setCheckState(QtCore.Qt.Checked)
    wait(3)
    tab = app.currently_open_groups[globals_file, 'MOT']
    app.ui.tabWidget.setCurrentWidget(tab.ui)
    view = tab.ui.tableView_globals
    wait(2)

    def value_text(name):
        return tab.get_global_item_by_name(name, tab.GLOBALS_COL_VALUE).text()

    def set_value(name, value):
        tab.change_global_value(name, value_text(name), value, interactive=False)
        wait(1.5)

    def engage(expected_values):
        """Engage, and wait until the history records the expected values"""
        app.on_engage_clicked()

        def recorded():
            for name, value in expected_values.items():
                entries = gm.get_history(globals_file, 'MOT', name)
                if not any(e['text'] == value for e in entries):
                    return False
            return True
        ok = wait(0.5, recorded, limit=60)
        wait(0.5, lambda: app.compile_queue.empty() and not app.ui.pushButton_abort.isEnabled(), limit=60)
        if not ok:
            print('output box:', app.output_box.output_textedit.toPlainText()[-3000:], flush=True)
        return ok

    # Compile real shots with a few values of mot_detuning:
    check(engage({'mot_detuning': '-12e6  # 2 linewidths'}), 'first engage records the current values')
    entries = gm.get_history(globals_file, 'MOT', 'amplitude')
    check(len(entries) == 1 and entries[0]['text'] == '0.25  # optimised for loading',
          'history of amplitude has the compiled value, comment included')
    set_value('mot_detuning', '-18e6  # 3 linewidths')
    check(engage({'mot_detuning': '-18e6  # 3 linewidths'}), 'second engage records the new value')
    set_value('mot_detuning', '-12e6')
    check(engage({'mot_detuning': '-12e6'}), 'third engage updates the text of the existing entry')
    entries = gm.get_history(globals_file, 'MOT', 'mot_detuning')
    texts = sorted(e['text'] for e in entries)
    check('-12e6' in texts and '-12e6  # 2 linewidths' not in texts and len(set(e['key'] for e in entries)) == len(entries),
          f'values differing only in comments share one entry: {[e["text"] for e in entries]}')
    # A value that fails to compile is not recorded:
    set_value('duration', '-1')
    app.on_engage_clicked()
    wait(0.5, lambda: app.compile_queue.empty() and not app.ui.pushButton_abort.isEnabled(), limit=180)
    wait(2)
    entries = gm.get_history(globals_file, 'MOT', 'duration')
    check([e['text'] for e in entries] == ['0.5'], f'a value that fails to compile is not recorded: {entries}')
    set_value('duration', '0.5')

    gm.set_history_pinned(globals_file, 'MOT', 'mot_detuning', gm.history_key('-10e6'), True)
    set_value('mot_detuning', '-12e6  # 2 linewidths')

    # Screenshot: the table, with comments in grey and the button on the current cell
    index = tab.get_global_item_by_name('mot_detuning', tab.GLOBALS_COL_VALUE).index()
    view.setCurrentIndex(index)
    wait(1)
    save('table')

    # Screenshot: the popup
    tab.show_value_history('mot_detuning')
    wait(1)
    check(len(popups()) == 1, 'clicking the button shows the history popup')
    popup = popups()[0]
    texts = [popup.entry(row)['text'] for row in range(popup.model.rowCount())]
    print('popup order:', texts, flush=True)
    check(texts[0] == '-12e6', f'current value is first: {texts[0]}')
    check(texts[1] == '-18e6  # 3 linewidths', f'previous value is second: {texts[1]}')
    check(texts[2] == '-10e6', f'pinned value is third: {texts[2]}')
    save('popup')

    # Filter
    popup.filter_edit.setText('linewidth')
    wait(0.5)
    visible = [popup.entry(row)['text'] for row in popup.visible_rows()]
    check(visible == ['-18e6  # 3 linewidths', '-24e6  # 4 linewidths, for imaging test'],
          f'filter matches comments too: {visible}')
    save('popup-filtered')
    # Choose an entry with the keyboard:
    import importlib
    from qtutils.qt import QT_ENV
    QtTest = importlib.import_module(QT_ENV + '.QtTest')
    QtTest.QTest.keyClick(popup.filter_edit, QtCore.Qt.Key_Down)
    QtTest.QTest.keyClick(popup.filter_edit, QtCore.Qt.Key_Return)
    wait(1.5)
    check(not popups(), 'Enter closes the popup')
    check(value_text('mot_detuning') == '-24e6  # 4 linewidths, for imaging test',
          f'Enter sets the selected value: {value_text("mot_detuning")}')
    check(gm.get_value(globals_file, 'MOT', 'mot_detuning') == '-24e6  # 4 linewidths, for imaging test',
          'the value is written to the globals file')

    check(engage({'mot_detuning': '-24e6  # 4 linewidths, for imaging test'}), 'engage')
    # Switch to previous value, twice
    view.selectRow(index.row())
    tab.on_globals_previous_value_triggered()
    wait(1.5)
    check(value_text('mot_detuning') == '-12e6',
          f'switching to the previous value restores the value before the change: {value_text("mot_detuning")}')
    check(engage({}), 'engage')
    tab.on_globals_previous_value_triggered()
    wait(1.5)
    check(value_text('mot_detuning') == '-24e6  # 4 linewidths, for imaging test',
          f'switching again returns to the other value: {value_text("mot_detuning")}')

    # Keyboard shortcut on the table:
    window.activateWindow()
    view.setFocus()
    view.setCurrentIndex(tab.get_global_item_by_name('repump_power', tab.GLOBALS_COL_VALUE).index())
    wait(0.5)
    QtTest.QTest.keyClick(view, QtCore.Qt.Key_Down, QtCore.Qt.AltModifier)
    wait(1)
    check(len(popups()) == 1, 'Alt+Down on a value cell shows the popup')
    popup = popups()[0]
    texts = [popup.entry(row)['text'] for row in range(popup.model.rowCount())]
    print('repump order:', texts, flush=True)
    # Pin and remove with the keyboard:
    selected = popup.entry(popup.current_row())
    QtTest.QTest.keyClick(popup.filter_edit, QtCore.Qt.Key_P, QtCore.Qt.ControlModifier)
    wait(0.5)
    entries = {e['key']: e for e in gm.get_history(globals_file, 'MOT', 'repump_power')}
    check(entries[selected['key']]['pinned'], 'Ctrl+P pins the selected entry in the file')
    save('popup-pinned')
    QtTest.QTest.keyClick(popup.filter_edit, QtCore.Qt.Key_Delete)
    wait(0.5)
    entries = {e['key']: e for e in gm.get_history(globals_file, 'MOT', 'repump_power')}
    check(selected['key'] not in entries, 'Delete removes the selected entry from the file')
    QtTest.QTest.keyClick(popup.filter_edit, QtCore.Qt.Key_Escape)
    wait(0.5)
    check(not popups(), 'Escape closes the popup')

    # Alt+Down in the editor discards the edit and shows the popup
    load_index = tab.get_global_item_by_name('load_time', tab.GLOBALS_COL_VALUE).index()
    view.setCurrentIndex(load_index)
    view.edit(load_index)
    wait(0.5)
    editor = view.indexWidget(load_index)
    check(editor is not None, 'editor open')
    if editor is not None:
        editor.setPlainText('2.0  # trying a longer load\n# second line comment')
        wait(0.5)
        save('editor')
        QtTest.QTest.keyClick(editor, QtCore.Qt.Key_Down, QtCore.Qt.AltModifier)
        wait(1)
        check(len(popups()) == 1, 'Alt+Down in the editor shows the popup')
        check(value_text('load_time') == '1.5  # was 2.0, shortened for faster cycle',
              f'and discards the edit: {value_text("load_time")}')
        save('popup-from-editor')
        for p in popups():
            p.close()
        wait(0.5)

    # Rename and delete keep the history in step
    tab.get_global_item_by_name('repump_power', tab.GLOBALS_COL_NAME).setText('repump_power_mW')
    wait(1)
    check(gm.get_history(globals_file, 'MOT', 'repump_power_mW'), 'history follows a renamed global')

    # Context menu
    view.selectRow(tab.get_global_item_by_name('mot_detuning', tab.GLOBALS_COL_VALUE).row())
    menu = QtWidgets.QMenu(tab.ui)
    for action in [tab.action_globals_set_selected_true, tab.action_globals_set_selected_false,
                   tab.action_globals_reset_expansion, tab.action_globals_previous_value,
                   tab.action_globals_value_history, tab.action_globals_delete_selected]:
        menu.addAction(action)
    rect = view.visualRect(tab.get_global_item_by_name('mot_detuning', tab.GLOBALS_COL_NAME).index())
    menu.popup(view.viewport().mapToGlobal(rect.center()))
    wait(1)
    save('context-menu', extra=menu)
    menu.close()

    n_fail = sum(1 for ok, _ in results if not ok)
    print(f'{len(results) - n_fail} passed, {n_fail} failed', flush=True)
    (out / f'result-{args.scheme}.txt').write_text(
        '\n'.join(('PASS ' if ok else 'FAIL ') + m for ok, m in results) + '\n')
    QtWidgets.QApplication.instance().exit(0)


def check_ready():
    rm = sys.modules.get('__main__')
    if getattr(rm, 'app', None) is not None and main_window() is not None:
        try:
            run()
        except Exception:
            traceback.print_exc()
            QtWidgets.QApplication.instance().exit(1)


class QApplication(BaseQApplication):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
        if args.scheme == 'dark':
            palette = QtGui.QPalette()
            for role, color in [('Window', '#353535'), ('WindowText', '#e0e0e0'), ('Base', '#2a2a2a'),
                                ('AlternateBase', '#323232'), ('Text', '#e0e0e0'), ('Button', '#353535'),
                                ('ButtonText', '#e0e0e0'), ('Highlight', '#2a82da'), ('HighlightedText', '#ffffff'),
                                ('ToolTipBase', '#353535'), ('ToolTipText', '#e0e0e0')]:
                palette.setColor(getattr(QtGui.QPalette, role), QtGui.QColor(color))
            for role in ['Text', 'WindowText', 'ButtonText']:
                palette.setColor(QtGui.QPalette.Disabled, getattr(QtGui.QPalette, role), QtGui.QColor('#7f7f7f'))
            self.setPalette(palette)
        if hasattr(self.styleHints(), 'setColorScheme'):
            scheme = {'light': QtCore.Qt.ColorScheme.Light, 'dark': QtCore.Qt.ColorScheme.Dark}
            self.styleHints().setColorScheme(scheme[args.scheme])
        global poll
        poll = QtCore.QTimer()
        poll.timeout.connect(check_ready)
        poll.start(500)


QtWidgets.QApplication = QApplication
if args.scheme == 'dark':
    # The offscreen platform has no colour scheme, so runmanager is told it is dark:
    import runmanager.widgets
    runmanager.widgets.RunmanagerColors.check_if_light = lambda self: False
runpy.run_module('runmanager', run_name='__main__', alter_sys=True)
