"""Per-shot phases from timeline<n>.txt of profile_blacs.py. A cycle starts at
Shot.start_run; the run phase ends when Shot._on_run_notification returns, and the gap
lasts from then to the next Shot.start_run. Prints medians for the shots started while
shots were still being submitted and for those after, and the main thread's busy time in
the gap and the run phase of the shots after submissions, by event.

    python timeline.py TIMELINE"""
import sys, collections, numpy as np
ev = []
for line in open(sys.argv[1]):
    p = line.rstrip('\n').split('\t')
    ev.append((int(p[0]) / 1e6, int(p[1]) / 1e6, int(p[2]) / 1e6, tuple(p[3:])))
def short(k):
    if k[0] == '65534': return k[2].split('.')[-2] + '.' + k[2].split('.')[-1]
    return k[0] + ':' + k[1] + ('(%s)' % k[2] if k[2] else '')
starts = [e[0] for e in ev if e[3][2].endswith('Shot.start_run')]
runnote = [e[0] + e[1] for e in ev if e[3][2].endswith('Shot._on_run_notification')]
procs = [e[0] for e in ev if e[3][2].endswith('ExperimentServer.process')]
last_proc = max(procs)
print('shots %d; last submission at %.1f s; first start_run at %.1f s' % (len(starts), last_proc/1e3, starts[0]/1e3))
# phases per cycle: run = start_run -> end of run notification; gap = run notification end -> next start_run
rows = []
for i in range(len(starts) - 1):
    rn = [t for t in runnote if starts[i] < t < starts[i + 1]]
    if not rn: continue
    rows.append((starts[i], rn[0] - starts[i], starts[i + 1] - rn[0], starts[i + 1] - starts[i]))
rows = np.array(rows)
for lab, sel in (('during submissions', rows[:, 0] < last_proc), ('after submissions', rows[:, 0] > last_proc)):
    r = rows[sel]
    print('%-20s n=%3d  cycle %.0f ms, run phase %.0f ms, gap (run done -> next start_run) %.0f ms  [medians]' % (lab, len(r), np.median(r[:, 3]), np.median(r[:, 1]), np.median(r[:, 2])))
# busy breakdown within gap and run phases, after submissions
def breakdown(phase_idx, lab, after=True):
    acc = collections.Counter(); accc = collections.Counter(); n = 0; tot = 0
    for s, run, gap, cyc in rows:
        if after and s < last_proc: continue
        if phase_idx == 'gap': a, b = s + run, s + cyc
        else: a, b = s, s + run
        n += 1; tot += b - a
        for t0, dw, dc, k in ev:
            if t0 >= a and t0 < b:
                acc[short(k)] += dw; accc[short(k)] += dc
    print('--- main thread during %s (%d shots, mean phase %.1f ms): busy %.1f ms/shot wall, %.1f ms CPU' % (lab, n, tot/n, sum(acc.values())/n, sum(accc.values())/n))
    for k, w in acc.most_common(14): print('  %6.2f ms wall %6.2f ms cpu  %s' % (w/n, accc[k]/n, k))
breakdown('gap', 'gap run-done -> next start_run')
breakdown('run', 'run phase start_run -> run-done')
