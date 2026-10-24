"""Timing of cancel_read() and read timeouts of usbserial on COM3, an FTDI cable with TX
connected to RX. Uses usbserial.py from this directory."""

import importlib.util
import random
import statistics
import sys
import threading
import time
from pathlib import Path

PORT = 'COM3'
BAUDRATE = 115200
N = 300

spec = importlib.util.spec_from_file_location('usbserial', Path(__file__).with_name('usbserial.py'))
usbserial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usbserial)


def summary(name, times):
    t = sorted(x * 1e3 for x in times)
    q = statistics.quantiles(t, n=100)
    print(f'{name} (ms, {len(t)} samples): min {t[0]:.2f}, 10% {q[9]:.2f}, median {q[49]:.2f}, '
          f'90% {q[89]:.2f}, 99% {q[98]:.2f}, max {t[-1]:.2f}', flush=True)
    edges = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 1e9]
    counts = [sum(lo <= x < hi for x in t) for lo, hi in zip(edges, edges[1:])]
    print('   ' + ', '.join(f'[{lo:g}, {hi:g}): {c}' if hi < 1e9 else f'>= {lo:g}: {c}'
                            for lo, hi, c in zip(edges, edges[1:], counts) if c))


print(f'Python {sys.version.split()[0]} on {sys.platform}')
port = usbserial.Serial(PORT, BAUDRATE, timeout=None, write_timeout=1.0, exclusive=True)
print('opened as', type(port).__name__)
base = super(usbserial._SoftwareTimeoutMixin, port)

# One read of the underlying port, which has a 10 ms timeout, with no data arriving.
times = []
for i in range(N):
    t0 = time.perf_counter()
    base.read(1)
    times.append(time.perf_counter() - t0)
summary('underlying read with its 10 ms timeout, no data', times)

# cancel_read() at a random time while another thread is blocked in read(1).
times = []
for i in range(N):
    result = []
    thread = threading.Thread(target=lambda: result.append((port.read(1), time.perf_counter())))
    thread.start()
    time.sleep(0.02 + random.random() * 0.02)
    t0 = time.perf_counter()
    port.cancel_read()
    thread.join(1)
    if thread.is_alive() or result[0][0] != b'':
        print('FAIL: the read did not return empty after cancel_read()')
        break
    times.append(result[0][1] - t0)
summary('cancel_read() to the return of read()', times)

# read(1, timeout=0.05) with no data: time beyond the timeout.
times = []
for i in range(N):
    t0 = time.perf_counter()
    port.read(1, timeout=0.05)
    times.append(time.perf_counter() - t0 - 0.05)
summary('read(1, timeout=0.05) beyond the timeout', times)

# A byte written while a read is blocked: time from the write to the return of read().
times = []
for i in range(N):
    result = []
    thread = threading.Thread(target=lambda: result.append((port.read(1, timeout=1), time.perf_counter())))
    thread.start()
    time.sleep(0.02 + random.random() * 0.02)
    t0 = time.perf_counter()
    port.write(b'x')
    thread.join(2)
    if result[0][0] != b'x':
        print('FAIL: loopback byte not received')
        break
    times.append(result[0][1] - t0)
summary('write to the return of a blocked read (loopback)', times)

port.close()
