"""Medians of the phases of the shot cycle in one or more BLACS.log files, one row per
file, in milliseconds. The phases are measured from the queue manager's log messages
and the first and last "Processing event" message of the tabs for each transition. The
first two shots of each log are excluded.

    python phases.py BLACS.log [BLACS.log ...]
"""
import os
import statistics
import sys

from analyse import parse

COLUMNS = [
    'end of previous shot to first transition to buffered',
    'first to last transition to buffered',
    'last transition to buffered to start of run',
    'run',
    'end of run to first transition to manual',
    'first to last transition to manual',
    'last transition to manual to end of shot',
    'cycle',
]


def phases(path):
    shots = []
    current = None
    for t, name, msg in parse(path):
        if 'queue_manager' in name and msg.startswith('Got a file'):
            current = {'ttb': [], 'ttm': []}
            shots.append(current)
        elif current is None:
            continue
        elif 'queue_manager' in name:
            for key, prefix in [('start', 'About to start the master pseudoclock'),
                                ('done', 'Run complete'),
                                ('static', 'All devices are back in static mode')]:
                if msg.startswith(prefix):
                    current[key] = t
        elif name.endswith('.mainloop') and msg.startswith('Processing event _transition_to_buffered'):
            current['ttb'].append(t)
        elif name.endswith('.mainloop') and msg.startswith('Processing event _transition_to_manual'):
            current['ttm'].append(t)
    shots = [s for s in shots if {'start', 'done', 'static'} <= set(s) and s['ttb'] and s['ttm']]
    for a, b in zip(shots, shots[1:]):
        b['previous'] = a['static']
    shots = shots[2:]

    def med(f):
        return 1000 * statistics.median(f(s) for s in shots)

    return [
        med(lambda s: min(s['ttb']) - s['previous']),
        med(lambda s: max(s['ttb']) - min(s['ttb'])),
        med(lambda s: s['start'] - max(s['ttb'])),
        med(lambda s: s['done'] - s['start']),
        med(lambda s: min(s['ttm']) - s['done']),
        med(lambda s: max(s['ttm']) - min(s['ttm'])),
        med(lambda s: s['static'] - max(s['ttm'])),
        1000 * statistics.median(b['previous'] - a['previous'] for a, b in zip(shots, shots[1:])),
    ]


def main():
    print('file | ' + ' | '.join(COLUMNS))
    for path in sys.argv[1:]:
        print(os.path.basename(path) + ' | ' + ' | '.join('%.0f' % x for x in phases(path)))


if __name__ == '__main__':
    main()
