"""Per-shot and per-tab timings from a BLACS.log."""
import re
import statistics
import sys
from datetime import datetime

LINE = re.compile(r'^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3}) (\w+) (\S+): (.*)$')


def since(line, t):
    """True if the log line has a timestamp at or after t (seconds since the epoch)."""
    m = LINE.match(line.rstrip('\n'))
    if not m:
        return False
    return datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S,%f').timestamp() >= t


def parse(path):
    records = []
    for line in open(path, errors='replace'):
        m = LINE.match(line.rstrip('\n'))
        if m:
            t = datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S,%f').timestamp()
            records.append((t, m.group(3), m.group(4)))
    return records


def med(xs):
    return statistics.median(xs) if xs else float('nan')


def analyse(path, expected_shots):
    records = parse(path)
    # Queue manager phases.
    marks = [(t, msg) for t, name, msg in records if 'queue_manager' in name]
    shots = []
    current = None
    for t, msg in marks:
        if msg.startswith('Got a file'):
            current = {'got': t}
            shots.append(current)
        elif current is None:
            continue
        elif msg.startswith('About to start the master pseudoclock'):
            current['start'] = t
        elif msg.startswith('Run complete'):
            current['done'] = t
        elif msg.startswith('All devices are back in static mode'):
            current['static'] = t
    complete = [s for s in shots if {'got', 'start', 'done', 'static'} <= set(s)]
    # Exclude the first shot, as BLACS does extra work on it.
    stats = complete[1:]
    cycles = [b['got'] - a['got'] for a, b in zip(complete, complete[1:])][1:]
    out = []
    out.append(f'{len(complete)} of {expected_shots} shots complete; stats over {len(stats)} shots, medians')
    out.append(f"cycle {med(cycles):.3f} s: to buffered {med([s['start'] - s['got'] for s in stats]):.3f}, "
               f"run {med([s['done'] - s['start'] for s in stats]):.3f}, "
               f"to manual {med([s['static'] - s['done'] for s in stats]):.3f}, "
               f"gap {med([b['got'] - a['static'] for a, b in zip(complete, complete[1:])][1:]):.3f}")
    # Per-tab mainloop events: 'Processing event X' ... 'Waiting for next event'.
    tabs = {}
    for t, name, msg in records:
        m = re.match(r'BLACS\.(.+)\.mainloop$', name)
        if not m:
            continue
        tabs.setdefault(m.group(1), []).append((t, msg))
    rows = []
    for tab, lines in sorted(tabs.items()):
        events = {}
        ev = None
        for t, msg in lines:
            m = re.match(r'Processing event (\w+)', msg)
            if m:
                ev = {'name': m.group(1), 'start': t}
            elif ev is None:
                continue
            elif msg.startswith('Instructing worker'):
                ev['instruct'] = t
            elif msg.startswith('Waiting for worker to acknowledge'):
                ev['ack_wait'] = t
            elif msg.startswith('Worker reported job started'):
                ev['job_start'] = t
            elif msg.startswith('Job completed'):
                ev['job_done'] = t
            elif msg.startswith('Finalising function'):
                ev['finalise'] = t
            elif msg.startswith('Waiting for next event'):
                ev['end'] = t
                events.setdefault(ev['name'], []).append(ev)
                ev = None
        for name in ('_transition_to_buffered', '_transition_to_manual'):
            evs = [e for e in events.get(name, []) if 'job_start' in e and 'job_done' in e][1:]
            if not evs:
                continue
            total = [e['end'] - e['start'] for e in evs]
            job = [e['job_done'] - e['job_start'] for e in evs]
            overhead = [a - b for a, b in zip(total, job)]
            s1 = [e['ack_wait'] - e['instruct'] for e in evs if 'ack_wait' in e and 'instruct' in e]
            s2 = [e['end'] - e['finalise'] for e in evs if 'finalise' in e]
            rows.append((tab, name, len(evs), med(total), med(job), med(overhead), med(s1), med(s2)))
    out.append('tab, event, n, total ms, worker job ms, mainloop overhead ms, instruct->ack-wait ms, finalise->next ms')
    for r in rows:
        out.append(f'{r[0]}, {r[1]}, {r[2]}, ' + ', '.join(f'{1000 * x:.1f}' for x in r[3:]))
    if rows:
        out.append(f'mean over tabs of median mainloop overhead per event: '
                   f'{1000 * statistics.mean(r[5] for r in rows):.1f} ms')
    return '\n'.join(out)


if __name__ == '__main__':
    print(analyse(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0))
