"""Summarise the stack counts written by sample_blacs.py for one thread: the number of
samples in which each function is on the stack, and in which it is at the top.

    python stacks.py COUNTS THREAD [N]

THREAD is 'main' or a thread name such as 'Thread-29 (manage)'. Without THREAD, the
thread names and their sample counts are listed."""
import collections
import re
import sys


def main():
    path = sys.argv[1]
    want = sys.argv[2] if len(sys.argv) > 2 else None
    n_rows = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    threads = collections.Counter()
    inclusive = collections.Counter()
    top = collections.Counter()
    for line in open(path):
        stack, _, n = line.rstrip().rpartition(' ')
        n = int(n)
        frames = stack.split(';')
        threads[frames[0]] += n
        if frames[0] != want:
            continue
        for name in {re.sub(r':\d+\)', ')', f) for f in frames[1:]}:
            inclusive[name] += n
        top[frames[-1]] += n
    if want is None:
        for name, n in threads.most_common():
            print(n, name)
        return
    print(f'{threads[want]} samples of {want}')
    print('--- on the stack')
    for name, n in inclusive.most_common(n_rows):
        print(n, name)
    print('--- at the top of the stack')
    for name, n in top.most_common(n_rows // 2):
        print(n, name)


if __name__ == '__main__':
    main()
