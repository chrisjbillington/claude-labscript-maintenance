"""Run times of the shots in a sequence directory, from the 'run time' attribute,
relative to the engage time.

    python seqtimes.py SEQUENCE_DIR ENGAGED_TIME_FILE"""
import sys, os, glob, time, datetime, numpy as np
import labscript_utils.h5_lock, h5py
d, t_eng = sys.argv[1], float(open(sys.argv[2]).read())
files = sorted(glob.glob(os.path.join(d, '*.h5')))
rt = []
for f in files:
    with h5py.File(f, 'r') as h:
        v = h.attrs.get('run time')
        if v is not None:
            v = v.decode() if isinstance(v, bytes) else str(v)
            rt.append(datetime.datetime.strptime(v, '%Y%m%dT%H%M%S.%f').timestamp())
rt = np.sort(rt) - t_eng
print("%d files, %d run; first run at %.1f s, last at %.1f s after engage; per shot: mean %.0f ms, median %.0f ms, max %.0f ms" % (len(files), len(rt), rt[0], rt[-1], (rt[-1]-rt[0])/(len(rt)-1)*1e3, np.median(np.diff(rt))*1e3, np.max(np.diff(rt))*1e3))
