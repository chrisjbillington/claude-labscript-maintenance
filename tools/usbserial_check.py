"""Check labscript_devices.usbserial on an FTDI adaptor. Usage:

    python usbserial_check.py PORT [--loopback] [--baudrate N]

PORT is a COM port on Windows or a device path on Linux and macOS. With --loopback, the
adaptor's TX and RX pins must be connected to each other, and the script also checks
reads, writes and the reply latency. Uses labscript_devices.usbserial if it is installed,
otherwise usbserial.py from the directory of this script. Needs only pyserial."""

import argparse
import importlib.util
import sys
import threading
import time
from pathlib import Path

import serial
from serial.tools.list_ports import comports

try:
    from labscript_devices import usbserial
except ImportError:
    spec = importlib.util.spec_from_file_location('usbserial', Path(__file__).with_name('usbserial.py'))
    usbserial = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(usbserial)

parser = argparse.ArgumentParser()
parser.add_argument('port')
parser.add_argument('--loopback', action='store_true')
parser.add_argument('--baudrate', type=int, default=115200)
args = parser.parse_args()

failures = 0


def check(cond, msg):
    global failures
    failures += not cond
    print('PASS' if cond else 'FAIL', msg, flush=True)


def round_trips(port, read, n=50):
    times = []
    for i in range(n):
        t0 = time.perf_counter()
        port.write(b'x')
        reply = read()
        times.append(time.perf_counter() - t0)
        if reply != b'x':
            return None
    times.sort()
    return times[0], times[n // 2], times[-1]


print(f'Python {sys.version.split()[0]} on {sys.platform}, pyserial {serial.__version__}')
print('usbserial from', usbserial.__file__)
print('D2XX library loaded:', usbserial._ftd2xx is not None)
for p in comports():
    print(f'  {p.device}: vid={p.vid and hex(p.vid)} pid={p.pid and hex(p.pid)} serial={p.serial_number} '
          f'location={p.location} description={p.description}')

ftd2xx = usbserial._ftd2xx
if ftd2xx is not None:
    import ctypes
    n = ctypes.c_ulong()
    ftd2xx.FT_CreateDeviceInfoList(ctypes.byref(n))
    print(f'D2XX device list ({n.value} devices):')
    for i in range(n.value):
        flags, dtype, dev_id, loc_id = (ctypes.c_ulong() for _ in range(4))
        sn, desc, handle = ctypes.create_string_buffer(16), ctypes.create_string_buffer(64), ctypes.c_void_p()
        rc = ftd2xx.FT_GetDeviceInfoDetail(i, ctypes.byref(flags), ctypes.byref(dtype), ctypes.byref(dev_id),
                                           ctypes.byref(loc_id), sn, desc, ctypes.byref(handle))
        print(f'  {i}: rc={rc} serial={sn.value.decode()!r} description={desc.value.decode()!r} '
              f'type={dtype.value} id={dev_id.value:#010x} location={loc_id.value:#x} flags={flags.value:#x}')
    pyserial_sn = next(p.serial_number for p in comports() if p.device == args.port)
    for sn in [pyserial_sn, pyserial_sn[:-1]]:
        handle = ctypes.c_void_p()
        rc = ftd2xx.FT_OpenEx(sn.encode(), 1, ctypes.byref(handle))
        com = ctypes.c_long(-2)
        if rc == 0 and hasattr(ftd2xx, 'FT_GetComPortNumber'):
            ftd2xx.FT_GetComPortNumber(handle, ctypes.byref(com))
        if rc == 0:
            ftd2xx.FT_Close(handle)
        print(f'FT_OpenEx({sn!r}) returned {rc}' + (f', FT_GetComPortNumber gives {com.value}' if rc == 0 else ''))

port = usbserial.Serial(args.port, args.baudrate, timeout=None, write_timeout=1.0, exclusive=True)
print('opened as', type(port).__name__)
if sys.platform in ('win32', 'darwin') and usbserial._ftd2xx is not None:
    check(type(port).__name__ == '_FTD2xxSerial', 'the port is opened through D2XX')

for name, opener in [('usbserial.Serial', lambda: usbserial.Serial(args.port, args.baudrate, exclusive=True)),
                     ('serial.Serial', lambda: serial.Serial(args.port, args.baudrate, exclusive=True))]:
    try:
        opener().close()
        check(False, f'a second open with {name} raises')
    except serial.SerialException as e:
        check(True, f'a second open with {name} raises SerialException: {e}')
    except Exception as e:
        check(False, f'a second open with {name} raises {type(e).__name__}, not SerialException: {e}')

t0 = time.perf_counter()
data = port.read(5, timeout=0.1)
elapsed = time.perf_counter() - t0
if not args.loopback:
    check(data == b'' and 0.1 <= elapsed < 0.13, f'read with timeout 0.1 s returned {data!r} after {elapsed:.3f} s')
t0 = time.perf_counter()
data = port.read(5, timeout=0)
check(time.perf_counter() - t0 < 0.01, f'read with timeout 0 returned {data!r} immediately')

result = []
thread = threading.Thread(target=lambda: result.append((port.read(1), time.perf_counter())))
thread.start()
time.sleep(0.2)
t0 = time.perf_counter()
port.cancel_read()
thread.join(1)
check(not thread.is_alive() and result[0][0] == b'' and result[0][1] - t0 < 0.02,
      f'cancel_read ended a blocking read after {(result[0][1] - t0) * 1e3:.1f} ms' if result else 'cancel_read ended a blocking read')

if args.loopback:
    port.write(b'hello')
    check(port.read(5, timeout=1) == b'hello', 'loopback: write and read 5 bytes')
    stats = round_trips(port, lambda: port.read(1, timeout=1))
    check(stats is not None, 'loopback: 50 single-byte round trips')
    if stats:
        print(f'   usbserial round trip: min {stats[0]*1e3:.2f} ms, median {stats[1]*1e3:.2f} ms, max {stats[2]*1e3:.2f} ms')
    port.close()
    plain = serial.Serial(args.port, args.baudrate, timeout=1)
    stats = round_trips(plain, lambda: plain.read(1))
    plain.close()
    if stats:
        print(f'   serial.Serial round trip: min {stats[0]*1e3:.2f} ms, median {stats[1]*1e3:.2f} ms, max {stats[2]*1e3:.2f} ms')
else:
    port.close()

check(not port.is_open, 'close')
print(f'{failures} failure(s)')
