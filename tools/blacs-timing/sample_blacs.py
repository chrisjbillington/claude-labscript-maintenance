"""Run BLACS with a thread that records the Python stack of every thread every 2 ms,
starting $SAMPLE_DELAY seconds (default 20) after start-up. On SIGTERM the counts of
each stack are written to $SAMPLE_OUT, one line per stack, as the thread name and the
frames separated by semicolons, followed by the count."""
import collections
import os
import runpy
import signal
import sys
import threading
import time

counts = collections.Counter()
main_id = threading.get_ident()
active = False


def sampler():
    me = threading.get_ident()
    while True:
        time.sleep(0.002)
        if not active:
            continue
        names = {t.ident: t.name for t in threading.enumerate()}
        for ident, f in sys._current_frames().items():
            if ident == me:
                continue
            stack = []
            while f is not None:
                c = f.f_code
                stack.append('%s (%s:%d)' % (c.co_name, os.path.basename(c.co_filename), f.f_lineno))
                f = f.f_back
            name = 'main' if ident == main_id else names.get(ident, str(ident))
            counts[name + ';' + ';'.join(reversed(stack))] += 1


def start_sampling():
    global active
    time.sleep(float(os.environ.get('SAMPLE_DELAY', '20')))
    active = True


def dump(*args):
    with open(os.environ['SAMPLE_OUT'], 'w') as f:
        for stack, n in counts.items():
            f.write('%s %d\n' % (stack, n))
    os._exit(0)


signal.signal(signal.SIGTERM, dump)
threading.Thread(target=sampler, daemon=True).start()
threading.Thread(target=start_sampling, daemon=True).start()
sys.argv = ['blacs']
runpy.run_module('blacs', run_name='__main__', alter_sys=True)
