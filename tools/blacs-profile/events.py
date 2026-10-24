"""Summarise events<n>.txt from profile_blacs.py: outermost and exclusive event time by
event type and by type, receiver and function.

    python events.py EVENTS [N]"""
import sys, collections
path = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
top = []; excl = []
for line in open(path):
    p = line.rstrip('\n').split('\t')
    if p[0] == 'window':
        wall, mcpu = int(p[1]), int(p[2]); continue
    rec = (p[1], p[2], p[3], int(p[4]), int(p[5]), int(p[6]))
    (top if p[0] == 'top' else excl).append(rec)
tw = sum(r[4] for r in top); tc = sum(r[5] for r in top)
print('window %.1f s; main-thread CPU %.2f s; outermost events: wall %.2f s, CPU %.2f s, n %d' % (wall/1e9, mcpu/1e9, tw/1e9, tc/1e9, sum(r[3] for r in top)))
def show(recs, title, group):
    agg = collections.defaultdict(lambda: [0, 0, 0])
    for t, rc, x, n, w, c in recs:
        k = group(t, rc, x); a = agg[k]; a[0] += n; a[1] += w; a[2] += c
    print('---', title)
    print('   wall s   cpu s      n  mean ms  key')
    for k, (n, w, c) in sorted(agg.items(), key=lambda kv: -kv[1][1])[:N]:
        print('%8.3f %7.3f %7d %7.2f  %s' % (w/1e9, c/1e9, n, w/n/1e6, ' | '.join(k)))
show(top, 'outermost, by type', lambda t, rc, x: (t,))
show(top, 'outermost, by type/receiver/fn', lambda t, rc, x: (t, rc, x))
show(excl, 'exclusive, by type', lambda t, rc, x: (t,))
show(excl, 'exclusive, by type/receiver', lambda t, rc, x: (t, rc, x))
