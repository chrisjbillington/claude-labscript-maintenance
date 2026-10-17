"""Exercise OutputBox.clear_output and the context menu under one Qt binding, offscreen."""
import os, sys, time
binding = sys.argv[1]
os.environ['QT_ENV'] = binding
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from qtutils.qt import QT_ENV
from qtutils.qt.QtCore import QTimer, QPoint, Qt
from qtutils.qt.QtWidgets import QApplication, QWidget, QVBoxLayout
from qtutils.outputbox import OutputBox
assert QT_ENV == binding, QT_ENV

app = QApplication(sys.argv[:1])
window = QWidget()
layout = QVBoxLayout(window)
box = OutputBox(layout)
window.show()

def wait_for(pred, timeout=5):
    t0 = time.monotonic()
    while not pred():
        app.processEvents()
        time.sleep(0.01)
        assert time.monotonic() - t0 < timeout, 'timed out'

text = lambda: box.output_textedit.toPlainText().rstrip('\n')
box.print('first line')
box.print('second line')
wait_for(lambda: text() == 'first line\nsecond line')
policy = box.output_textedit.contextMenuPolicy()
assert policy == Qt.ContextMenuPolicy.CustomContextMenu, policy

# Clear through the API:
box.clear_output()
wait_for(lambda: text() == '')
box.print('third line')
wait_for(lambda: text() == 'third line')

# Clear through the context menu: open it, then trigger its 'Clear output' action from
# a timer while menu.exec() is running.
state = {}
def use_menu():
    menu = app.activePopupWidget()
    actions = [a.text() for a in menu.actions()]
    state['actions'] = actions
    [action] = [a for a in menu.actions() if a.text() == 'Clear output']
    action.trigger()
    menu.close()
QTimer.singleShot(200, use_menu)
box._show_context_menu(QPoint(5, 5))
wait_for(lambda: text() == '')
box.print('fourth line')
wait_for(lambda: text() == 'fourth line')
box.shutdown()
print(f'{binding}: ok; menu actions: {state["actions"]}')
