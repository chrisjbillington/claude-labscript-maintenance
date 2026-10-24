"""Run BLACS with a profiler. SIGUSR1 starts recording (clearing previous data); SIGUSR2
stops it and writes $PROF_DIR/events<n>.txt, $PROF_DIR/timeline<n>.txt and
$PROF_DIR/prof<n>.txt. SIGHUP minimises the BLACS window, or restores it if it is
minimised. PROF_SWITCH_INTERVAL, if set, is passed to sys.setswitchinterval().

events: every Qt event delivered in the main thread through QApplication.notify, with its
wall and thread CPU time, inclusive for outermost events and exclusive of nested events.
The key is the event type, the receiver's class and either the function called (qtutils
CallEvents) or the receiver's object name. Paint events also have the summed area of
their bounding rectangles.
timeline: start, wall and CPU time of every outermost event, in ns from the start of
recording.
prof: every PROF_INTERVAL s, the stack of the main thread if it is inside an event (one
count per sample), and the stack of each other thread with the thread CPU time used since
the previous sample. A thread that is running C code without releasing the GIL is sampled
only when it next runs Python code, so the lines in these stacks are approximate."""
import collections, os, runpy, signal, sys, threading, time

INTERVAL = float(os.environ.get('PROF_INTERVAL', '0.005'))
OUT = os.environ.get('PROF_DIR', '/tmp/blacsprof')
main_id = threading.get_ident()
active = threading.Event()
counts = collections.Counter(); cpu = collections.Counter(); lastcpu = {}
ev_top = collections.defaultdict(lambda: [0, 0, 0])   # key -> [n, wall_ns, cpu_ns] inclusive, outermost only
ev_excl = collections.defaultdict(lambda: [0, 0, 0])  # key -> [n, wall_ns, cpu_ns] exclusive
depth = [0]
childacc = []   # stack of [wall, cpu] of nested events
nrun = [0]
area_acc = collections.Counter()
timeline = []
t_window = [0, 0]

import qtutils.qt.QtWidgets as QtWidgets
from qtutils.qt.QtCore import QEvent
from qtutils.qt import QtCore
_typenames = {}
for k in dir(QEvent):
    v = getattr(QEvent, k)
    if isinstance(v, QEvent.Type):
        _typenames.setdefault(int(v), k)
_Base = QtWidgets.QApplication
perf = time.perf_counter_ns; tcpu = time.thread_time_ns

def evkey(receiver, event):
    t = int(event.type())
    name = _typenames.get(t, str(t))
    fn = getattr(event, 'fn', None)
    rc = type(receiver).__name__
    if fn is not None:
        f = getattr(fn, '__func__', fn)
        extra = getattr(f, '__qualname__', repr(f))
        mod = getattr(f, '__module__', '')
        return (name, rc, '%s.%s' % (mod, extra))
    try:
        on = receiver.objectName()
        if t == 12:  # Paint
            par = receiver.parentWidget()
            if on == 'qt_scrollarea_viewport' and par is not None:
                on = '%s(%s).viewport' % (type(par).__name__, par.objectName())
            r = event.rect()
            area = r.width() * r.height()
            area_acc[(name, rc, on)] += area
    except Exception:
        on = ''
    return (name, rc, on)

class ProfApp(_Base):
    def notify(self, receiver, event):
        if not active.is_set() or threading.get_ident() != main_id:
            return _Base.notify(self, receiver, event)
        key = evkey(receiver, event)
        w0 = perf(); c0 = tcpu()
        depth[0] += 1
        childacc.append([0, 0])
        try:
            return _Base.notify(self, receiver, event)
        finally:
            dw = perf() - w0; dc = tcpu() - c0
            cw, cc = childacc.pop()
            depth[0] -= 1
            e = ev_excl[key]; e[0] += 1; e[1] += dw - cw; e[2] += dc - cc
            if childacc:
                childacc[-1][0] += dw; childacc[-1][1] += dc
            else:
                e = ev_top[key]; e[0] += 1; e[1] += dw; e[2] += dc
                timeline.append((w0, dw, dc, key))

QtWidgets.QApplication = ProfApp

def sampler():
    me = threading.get_ident(); clocks = {}
    while True:
        active.wait()
        time.sleep(INTERVAL)
        names = {t.ident: t.name for t in threading.enumerate()}
        indepth = depth[0] > 0
        for ident, f in sys._current_frames().items():
            if ident == me:
                continue
            if ident == main_id:
                if not indepth:
                    continue
                d = 0
            else:
                try:
                    cid = clocks.get(ident)
                    if cid is None:
                        cid = clocks[ident] = time.pthread_getcpuclockid(ident)
                    c = time.clock_gettime_ns(cid)
                except OSError:
                    continue
                prev = lastcpu.get(ident); lastcpu[ident] = c
                d = 0 if prev is None else c - prev
            stack = []
            while f is not None:
                stack.append((f.f_code, f.f_lineno)); f = f.f_back
            key = ('main' if ident == main_id else names.get(ident, str(ident)), tuple(stack))
            counts[key] += 1; cpu[key] += d

def fmt(code, line):
    return '%s (%s:%d)' % (code.co_name, os.path.basename(code.co_filename), line or 0)

def start(*a):
    counts.clear(); cpu.clear(); lastcpu.clear(); ev_top.clear(); ev_excl.clear(); area_acc.clear(); del timeline[:]
    t_window[0] = perf(); t_window[1] = tcpu()
    active.set()

def stop(*a):
    active.clear()
    wall = perf() - t_window[0]; mcpu = tcpu() - t_window[1]
    time.sleep(2 * INTERVAL)
    nrun[0] += 1
    with open(os.path.join(OUT, 'prof%d.txt' % nrun[0]), 'w') as fh:
        for (name, stack), n in list(counts.items()):
            fh.write('%s;%s %d %d\n' % (name, ';'.join(fmt(c, l) for c, l in reversed(stack)), n, cpu[(name, stack)]))
    with open(os.path.join(OUT, 'events%d.txt' % nrun[0]), 'w') as fh:
        fh.write('window\t%d\t%d\n' % (wall, mcpu))
        for kind, d in (('top', ev_top), ('excl', ev_excl)):
            for key, (n, w, c) in d.items():
                fh.write('%s\t%s\t%d\t%d\t%d\t%d\n' % (kind, '\t'.join(key), n, w, c, area_acc.get(key, 0)))
    with open(os.path.join(OUT, 'timeline%d.txt' % nrun[0]), 'w') as fh:
        for w0, dw, dc, key in timeline:
            fh.write('%d\t%d\t%d\t%s\n' % (w0 - t_window[0], dw, dc, '\t'.join(key)))

def toggle_minimized(*a):
    for w in QtWidgets.QApplication.topLevelWidgets():
        if type(w).__name__ == 'BLACSWindow':
            if w.isMinimized():
                w.hide()
                w.setWindowState(w.windowState() & ~QtCore.Qt.WindowMinimized)
                w.show()
                w.raise_()
                w.activateWindow()
            else:
                w.showMinimized()
            print('BLACS window minimized:', w.isMinimized(), flush=True)

if os.environ.get('PROF_SWITCH_INTERVAL'):
    sys.setswitchinterval(float(os.environ['PROF_SWITCH_INTERVAL']))

signal.signal(signal.SIGHUP, toggle_minimized)
signal.signal(signal.SIGUSR1, start)
signal.signal(signal.SIGUSR2, stop)
threading.Thread(target=sampler, daemon=True, name='profiler').start()
sys.argv = ['blacs']
runpy.run_module('blacs', run_name='__main__', alter_sys=True)
