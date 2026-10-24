"""Separate the effects of compilation and of submission on BLACS's shot cycle.

    EXPERIMENT_SHOTS=<directory> python submit_exp.py RUN [RUN ...]

EXPERIMENT_SHOTS is the directory of the experiment's shots, which holds the
year/month/day/sequence directories. RUN is one of A (compile and submit, as normal), B
(precompiled shots submitted in a burst), C (burst, then a compile that is not
submitted), D (precompiled shots submitted at the rate of A) and E (the shots of the
previous run, which have been run, submitted again at the rate of A, so that BLACS
queues a copy of each)."""
import sys, os, glob, time, datetime, threading, subprocess, statistics as st
import labscript_utils.h5_lock, h5py
from labscript_utils.ls_zprocess import zmq_get, Lock
from labscript_utils import shared_drive
import runmanager.remote

SHOTS = os.path.expanduser(os.environ['EXPERIMENT_SHOTS'])
rm = runmanager.remote.Client()

def newest():
    return sorted(glob.glob(SHOTS + '/[0-9]*/[0-9]*/[0-9]*/[0-9][0-9][0-9][0-9]'))[-1]

def wait_compiled(prev):
    while newest() == prev:
        time.sleep(0.2)
    d = newest()
    while True:
        files = glob.glob(d + '/*.h5')
        n = 0
        if len(files) == 100:
            for f in files:
                try:
                    with h5py.File(f, 'r') as h:
                        n += 'connection table' in h
                except Exception:
                    pass
        if n == 100:
            return d, time.time()
        time.sleep(0.3)

def submit(path):
    r = zmq_get(42517, 'localhost', data=shared_drive.path_to_agnostic(path))
    assert 'added successfully' in r, r

def run_times(d, pattern='*.h5'):
    out = []
    for f in glob.glob(os.path.join(d, pattern)):
        with h5py.File(f, 'r') as h:
            v = h.attrs.get('run time')
        if v is None:
            return None
        v = v.decode() if isinstance(v, bytes) else str(v)
        out.append(datetime.datetime.strptime(v, '%Y%m%dT%H%M%S.%f').timestamp())
    return sorted(out)

def wait_run(d, pattern='*.h5'):
    while True:
        rt = run_times(d, pattern)
        if rt is not None:
            return rt
        time.sleep(2)

probe = []
def prober(stop):
    lock = Lock('submit-exp-probe')
    while not stop.is_set():
        t = time.time(); lock.acquire(); lock.release()
        probe.append((t, time.time() - t))
        time.sleep(0.02)

def cpu_total():
    with open('/proc/stat') as f:
        v = list(map(int, f.readline().split()[1:]))
    return sum(v), v[3] + v[4]

def proc_cpu(pids):
    tot = 0
    for p in pids:
        try:
            with open('/proc/%d/stat' % p) as f:
                s = f.read().rsplit(')', 1)[1].split()
            tot += int(s[11]) + int(s[12])
        except OSError:
            pass
    return tot / os.sysconf('SC_CLK_TCK')

def pids(pattern):
    r = subprocess.run(['pgrep', '-f', pattern], capture_output=True, text=True).stdout.split()
    return [int(x) for x in r]

def report(name, rt, t0, t1, cpu0, cpu1, pc0, pc1):
    iv_in = [b - a for a, b in zip(rt, rt[1:]) if t0 <= a < t1]
    iv_out = [b - a for a, b in zip(rt, rt[1:]) if a >= t1 + 0.5]
    pin = [l for t, l in probe if t0 <= t < t1]
    pout = [l for t, l in probe if t >= t1 + 0.5 and t < rt[-1]]
    busy = 1 - (cpu1[1] - cpu0[1]) / (cpu1[0] - cpu0[0])
    def q(x, p): return sorted(x)[int(p * (len(x) - 1))] * 1e3 if x else float('nan')
    print('%s: window %.1f s, %d shots in it: interval median %.0f ms (after: %.0f ms, %d shots); '
          'zlock round trip median/90%% %.2f/%.2f ms (after %.2f/%.2f); machine CPU busy %.0f%% of 4 CPUs in window; '
          'CPU s in window: %s' % (name, t1 - t0, len(iv_in), st.median(iv_in) * 1e3 if iv_in else float('nan'),
          st.median(iv_out) * 1e3, len(iv_out), q(pin, .5), q(pin, .9), q(pout, .5), q(pout, .9), busy * 100,
          ', '.join('%s %.1f' % (k, pc1[k] - pc0[k]) for k in pc0)), flush=True)

GROUPS = {'blacs': 'python -m blacs', 'runmanager+compiler': 'runmanager', 'zlock': 'zlock', 'lyse': 'lyse'}
def snap():
    return {k: proc_cpu(pids(v)) for k, v in GROUPS.items()}

def precompile():
    rm.set_run_shots(False)
    prev = newest(); rm.engage()
    d, _ = wait_compiled(prev)
    rm.set_run_shots(True)
    return d

rate = [0.08]
d = None
for run in sys.argv[1:]:
    stop = threading.Event(); probe.clear()
    if run in 'BCD':
        d = precompile(); time.sleep(2)
    th = threading.Thread(target=prober, args=(stop,), daemon=True); th.start()
    time.sleep(1)
    if run == 'A':
        rm.set_run_shots(True)
        prev = newest(); t0 = time.time(); c0 = cpu_total(); p0 = snap()
        rm.engage()
        d, t1 = wait_compiled(prev)
        rate[0] = (t1 - t0) / 100
    elif run == 'B':
        files = sorted(glob.glob(d + '/*.h5'))
        t0 = time.time(); c0 = cpu_total(); p0 = snap()
        for f in files: submit(f)
        t1 = time.time()
    elif run == 'C':
        files = sorted(glob.glob(d + '/*.h5'))
        for f in files: submit(f)
        rm.set_run_shots(False)
        prev = newest(); t0 = time.time(); c0 = cpu_total(); p0 = snap()
        rm.engage()
        _, t1 = wait_compiled(prev)
        rm.set_run_shots(True)
    elif run in 'DE':
        if run == 'E':
            files = sorted(f for f in glob.glob(d + '/*.h5') if '_rep' not in f)
        else:
            files = sorted(glob.glob(d + '/*.h5'))
        t0 = time.time(); c0 = cpu_total(); p0 = snap()
        for i, f in enumerate(files):
            submit(f)
            delay = t0 + (i + 1) * rate[0] - time.time()
            if delay > 0: time.sleep(delay)
        t1 = time.time()
    c1 = cpu_total(); p1 = snap()
    rt = wait_run(d, '*_rep*.h5' if run == 'E' else '*.h5')
    stop.set(); th.join()
    report(run + ' ' + os.path.basename(d), rt, t0, t1, c0, c1, p0, p1)
