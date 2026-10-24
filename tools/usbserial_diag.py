"""Diagnose loopback reads of usbserial on COM3, an FTDI cable with TX connected to RX,
when a read in one thread waits for a byte written from another. Uses usbserial.py from
this directory."""

import importlib.util
import sys
import threading
import time
from pathlib import Path

PORT = 'COM3'
BAUDRATE = 115200
N = 20

spec = importlib.util.spec_from_file_location('usbserial', Path(__file__).with_name('usbserial.py'))
usbserial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usbserial)

print(f'Python {sys.version.split()[0]} on {sys.platform}')
for clock in ['monotonic', 'perf_counter']:
    print(f'time.{clock}:', time.get_clock_info(clock))

port = usbserial.Serial(PORT, BAUDRATE, timeout=None, write_timeout=1.0, exclusive=True)
print('opened as', type(port).__name__, flush=True)
base = super(usbserial._SoftwareTimeoutMixin, port)


def ms(t):
    return f'{t * 1e3:.2f} ms'


print('\n1. Write, then read in the same thread')
for i in range(5):
    t0 = time.perf_counter()
    port.write(b'x')
    t1 = time.perf_counter()
    data = port.read(1, timeout=1)
    t2 = time.perf_counter()
    print(f'   write took {ms(t1 - t0)}, read returned {data!r} after {ms(t2 - t1)}, in_waiting {port.in_waiting}')

for name, read in [('2. usbserial read(1, timeout=1) in another thread', lambda: port.read(1, timeout=1)),
                   ('3. one D2XX read (10 ms timeout) at a time, in a loop in another thread for up to 1 s',
                    lambda: next((d for d in iter(lambda: base.read(1), None)
                                  if d or time.perf_counter() > deadline[0]), b''))]:
    print(f'\n{name}, byte written from this thread after 30 ms')
    n_ok = 0
    for i in range(N):
        result = []
        deadline = [time.perf_counter() + 1]
        thread = threading.Thread(target=lambda: result.append((read(), time.perf_counter())))
        thread.start()
        time.sleep(0.03)
        t0 = time.perf_counter()
        port.write(b'x')
        t1 = time.perf_counter()
        thread.join(2)
        data, t2 = result[0] if result else (None, None)
        n_ok += data == b'x'
        if i < 5 or data != b'x':
            after = ms(t2 - t1) if t2 else 'never'
            print(f'   {i}: write took {ms(t1 - t0)}, read returned {data!r} {after} after the write, '
                  f'in_waiting afterwards {port.in_waiting}')
        if port.in_waiting:
            print(f'      left in the buffer: {port.read(port.in_waiting, timeout=0)!r}')
    print(f'   {n_ok}/{N} reads returned the byte')

port.close()
