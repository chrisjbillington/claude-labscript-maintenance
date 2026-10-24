#####################################################################
#                                                                   #
# /labscript_devices/usbserial.py                                   #
#                                                                   #
# Copyright 2026, Christopher Billington                            #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################
"""A wrapper around pyserial for USB-serial adaptors that sets the latency timer of FTDI
adaptors to 1 ms and implements read timeouts in software.

An FTDI adaptor holds received data for up to its latency timer before sending it to the
computer, 16 ms by default, so every reply from a device takes at least that long. On
Linux the low-latency mode of the ``ftdi_sio`` driver sets the timer to 1 ms. On Windows
and macOS the timer can only be set through FTDI's D2XX library, so for FTDI adaptors
:func:`Serial` uses D2XX instead of the virtual COM port driver if the library is
installed. D2XX is installed with FTDI's driver on Windows; on macOS it is available from
https://ftdichip.com/drivers/d2xx-drivers/.
"""

import ctypes
import os
import sys
import threading
import time
import warnings
import weakref

import serial
from serial.tools.list_ports import comports

_LINUX = sys.platform.startswith('linux')
_WINDOWS = sys.platform == 'win32'
_MACOS = sys.platform == 'darwin'

_FTDI_VENDOR_ID = 0x0403

_FTD2XX_WARNING = """FTDI D2XX library not found. Serial communication with FTDI
adaptors will have up to 16 ms of added latency. The D2XX library for Windows and macOS
is available from https://ftdichip.com/drivers/d2xx-drivers/"""

if _WINDOWS:
    try:
        _ftd2xx = ctypes.WinDLL("ftd2xx.dll")
    except OSError:
        _ftd2xx = None
elif _MACOS:
    try:
        _ftd2xx = ctypes.CDLL("libftd2xx.dylib")
    except OSError:
        _ftd2xx = None
else:
    _ftd2xx = None


def _get_usb_info(port):
    """The USB vendor ID, product ID and serial number of a serial port, or None if
    the port is not a USB device that pyserial lists."""
    if not _WINDOWS:
        port = os.path.realpath(port)
    for p in comports():
        if p.device == port and p.vid is not None:
            return p.vid, p.pid, p.serial_number
    return None


def _set_low_latency_serial_linux(fd):
    """Enable low-latency mode on a Linux serial port, which sets the latency timer of an
    FTDI adaptor to 1 ms. Does nothing if the mode is already enabled, since enabling it
    again delays the next read by up to 255 ms."""
    import array
    import fcntl
    import termios

    ASYNC_LOW_LATENCY_WORD = 4
    ASYNC_LOW_LATENCY_MASK = 0x2000

    buf = array.array('i', [0] * 32)
    try:
        fcntl.ioctl(fd, termios.TIOCGSERIAL, buf)
        if buf[ASYNC_LOW_LATENCY_WORD] & ASYNC_LOW_LATENCY_MASK:
            return
        buf[ASYNC_LOW_LATENCY_WORD] |= ASYNC_LOW_LATENCY_MASK
        fcntl.ioctl(fd, termios.TIOCSSERIAL, buf)
    except OSError:
        # Not supported by the driver
        return
    # When the latency timer is reduced, it may not fire for up to 255 ms, the largest
    # value that it can have. We wait for this time so that the caller's read timeouts
    # do not have to allow for it.
    time.sleep(0.255)


class _FTD2xxSerialBase:
    """A serial port opened through FTDI's D2XX library instead of the virtual COM port
    driver, with the latency timer set to 1 ms. Implements the parts of the interface of
    ``serial.Serial`` that :class:`_SoftwareTimeoutMixin` needs, and `port`,
    `baudrate` and `break_condition`. The port is always opened exclusively."""

    _FT_OPEN_BY_SERIAL_NUMBER = 1
    _WORD_LENGTH = {7: 7, 8: 8}
    _STOP_BITS = {1: 0, 1.5: 1, 2: 2}
    _PARITY = {'N': 0, 'O': 1, 'E': 2, 'M': 3, 'S': 4}
    _FLOW_RTSCTS = 0x100
    _FLOW_DSRDTR = 0x200
    _FLOW_XONXOFF = 0x400
    _XON = 0x11
    _XOFF = 0x13

    _FT_STATUS = {
        0: "FT_OK",
        1: "FT_INVALID_HANDLE",
        2: "FT_DEVICE_NOT_FOUND",
        3: "FT_DEVICE_NOT_OPENED",
        4: "FT_IO_ERROR",
        5: "FT_INSUFFICIENT_RESOURCES",
        6: "FT_INVALID_PARAMETER",
        7: "FT_INVALID_BAUD_RATE",
        8: "FT_DEVICE_NOT_OPENED_FOR_ERASE",
        9: "FT_DEVICE_NOT_OPENED_FOR_WRITE",
        10: "FT_FAILED_TO_WRITE_DEVICE",
        11: "FT_EEPROM_READ_FAILED",
        12: "FT_EEPROM_WRITE_FAILED",
        13: "FT_EEPROM_ERASE_FAILED",
        14: "FT_EEPROM_NOT_PRESENT",
        15: "FT_EEPROM_NOT_PROGRAMMED",
        16: "FT_INVALID_ARGS",
        17: "FT_NOT_SUPPORTED",
        18: "FT_OTHER_ERROR",
    }

    def __init__(
        self,
        port,
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=None,
        xonxoff=False,
        rtscts=False,
        write_timeout=None,
        dsrdtr=False,
        exclusive=None,
    ):
        self.port = port
        self._baudrate = baudrate
        self._break_condition = False
        self._handle = None

        _, _, sn = _get_usb_info(port)
        handle = ctypes.c_void_p()
        rc = _ftd2xx.FT_OpenEx(
            sn.encode(), self._FT_OPEN_BY_SERIAL_NUMBER, ctypes.byref(handle)
        )
        # On Windows, pyserial reports the serial number in the device ID that FTDI's
        # driver assigns to each channel, which ends in the channel's letter. D2XX
        # includes the letter only for devices with more than one channel.
        if rc == 2:  # FT_DEVICE_NOT_FOUND
            sn = sn[:-1]
            self._checkrc(
                _ftd2xx.FT_OpenEx,
                sn.encode(),
                self._FT_OPEN_BY_SERIAL_NUMBER,
                ctypes.byref(handle),
            )
        elif rc != 0:
            self._raise_err(_ftd2xx.FT_OpenEx, rc)

        self._handle = handle
        self._finalizer = weakref.finalize(self, _ftd2xx.FT_Close, handle)
        try:
            self._set_baudrate(baudrate)
            self._checkrc(
                _ftd2xx.FT_SetDataCharacteristics,
                handle,
                self._WORD_LENGTH[bytesize],
                self._STOP_BITS[stopbits],
                self._PARITY[parity],
            )
            if sum([xonxoff, rtscts, dsrdtr]) > 1:
                raise ValueError("Only one of xonxoff, rtscts, dsrdtr can be True")
            if rtscts:
                flow = self._FLOW_RTSCTS
            elif dsrdtr:
                flow = self._FLOW_DSRDTR
            elif xonxoff:
                flow = self._FLOW_XONXOFF
            else:
                flow = 0
            self._checkrc(_ftd2xx.FT_SetFlowControl, handle, flow, self._XON, self._XOFF)
            self._checkrc(
                _ftd2xx.FT_SetTimeouts,
                handle,
                int(timeout * 1000) if timeout is not None else 0,
                int(write_timeout * 1000) if write_timeout is not None else 0,
            )
            self._checkrc(_ftd2xx.FT_SetLatencyTimer, handle, 1)
        except:
            self.close()
            raise

    def _raise_err(self, func, rc):
        msg = f"{func.__name__} error: {self._FT_STATUS.get(rc, f'unknown ({rc})')}"
        raise serial.SerialException(f"{self.port}: {msg}")

    def _checkrc(self, func, *args):
        rc = func(*args)
        if rc != 0:
            self._raise_err(func, rc)

    def write(self, data):
        written = ctypes.c_ulong()
        self._checkrc(
            _ftd2xx.FT_Write,
            self._handle,
            bytes(data),
            len(data),
            ctypes.byref(written),
        )
        return written.value

    def read(self, n):
        buf = ctypes.create_string_buffer(n)
        read_n = ctypes.c_ulong()
        self._checkrc(_ftd2xx.FT_Read, self._handle, buf, n, ctypes.byref(read_n))
        return buf.raw[: read_n.value]

    def _set_baudrate(self, baudrate):
        self._checkrc(_ftd2xx.FT_SetBaudRate, self._handle, baudrate)

    @property
    def is_open(self):
        return self._handle is not None

    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baudrate):
        self._set_baudrate(baudrate)
        self._baudrate = baudrate

    @property
    def break_condition(self):
        return self._break_condition

    @break_condition.setter
    def break_condition(self, value):
        if value:
            self._checkrc(_ftd2xx.FT_SetBreakOn, self._handle)
        else:
            self._checkrc(_ftd2xx.FT_SetBreakOff, self._handle)
        self._break_condition = bool(value)

    @property
    def in_waiting(self):
        n = ctypes.c_ulong()
        self._checkrc(_ftd2xx.FT_GetQueueStatus, self._handle, ctypes.byref(n))
        return n.value

    def close(self):
        if self._handle is not None:
            self._finalizer()
            self._handle = None


class _SoftwareTimeoutMixin:
    """Mixin for ``serial.Serial`` or :class:`_FTD2xxSerialBase` that implements read
    timeouts in software and adds `cancel_read`. The underlying port has a fixed read
    timeout of 10 ms.

    This works around two problems:

    a) on Windows, changing the timeouts of an FTDI adaptor after opening the port
       corrupts data, see https://github.com/pyserial/pyserial/issues/394

    b) pyserial's ``send_break()`` on Linux and macOS gets the duration wrong.

    A read timeout can be passed when the port is created. Do not set the `timeout`
    attribute afterwards; pass a `timeout` argument to `read` instead."""

    # Distinguishes timeout=None from no timeout argument to read():
    _UNSET = object()

    _MIN_NONZERO_TIMEOUT = 0.010

    def __init__(
        self,
        port,
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=None,
        xonxoff=False,
        rtscts=False,
        write_timeout=None,
        dsrdtr=False,
        exclusive=None,
    ):
        self.__timeout = timeout
        self.__cancelled = threading.Event()
        super().__init__(
            port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=self._MIN_NONZERO_TIMEOUT,
            xonxoff=xonxoff,
            rtscts=rtscts,
            write_timeout=write_timeout,
            dsrdtr=dsrdtr,
            exclusive=exclusive,
        )

    def read(self, n=1, timeout=_UNSET):
        """Read up to `n` bytes, as ``serial.Serial.read()`` does, with the timeout
        implemented in software. `timeout` replaces the timeout given when the port was
        created.

        * If `timeout` is None, block until `n` bytes are read.
        * If `timeout` is 0, return up to `n` bytes that are available immediately.
        * Otherwise return up to `n` bytes received within the timeout. The call may
          block for up to about 16 ms longer than the timeout.

        A call to `cancel_read` from another thread makes this method return the bytes
        read so far within about 16 ms. If `cancel_read` is called when no read is in
        progress, the next read returns immediately."""
        if timeout is self._UNSET:
            timeout = self.__timeout
        if timeout == 0:
            return super().read(min(n, self.in_waiting))
        if timeout is not None:
            deadline = time.monotonic() + timeout
        chunks = []
        nread = 0
        while nread < n:
            if self.__cancelled.is_set():
                self.__cancelled.clear()
                break
            chunk = super().read(n - nread)
            chunks.append(chunk)
            nread += len(chunk)
            if timeout is not None and time.monotonic() > deadline:
                break
        return b''.join(chunks)

    def cancel_read(self):
        """Make a `read` in another thread return within about 16 ms."""
        self.__cancelled.set()

    # pyserial's send_break() on Linux calls tcsendbreak() as if its argument were in
    # units of 0.25 s, but Linux takes milliseconds and rounds up to 100 ms; macOS ignores
    # the argument. Toggling the break condition with a sleep, as pyserial does on
    # Windows, works on every platform.
    def send_break(self, duration=0.25):
        if not self.is_open:
            raise serial.PortNotOpenError()
        try:
            self.break_condition = True
            time.sleep(duration)
        finally:
            self.break_condition = False


class _Serial(_SoftwareTimeoutMixin, serial.Serial):
    pass


class _FTD2xxSerial(_SoftwareTimeoutMixin, _FTD2xxSerialBase):
    pass


def Serial(
    port,
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=None,
    xonxoff=False,
    rtscts=False,
    write_timeout=None,
    dsrdtr=False,
    exclusive=None,
):
    """Open a serial port. Takes the same arguments as ``serial.Serial``.

    For an FTDI adaptor, the latency timer is set to 1 ms. On Linux this uses the
    low-latency mode of the ``ftdi_sio`` driver; enabling the mode the first time that
    a port is opened takes 255 ms. On Windows and macOS the port is opened through
    FTDI's D2XX library if it is installed, and a warning is issued if it is not. A
    port opened through D2XX is always exclusive, has the methods and attributes of
    ``serial.Serial`` that are listed below, and raises ``serial.SerialException``.

    The returned object has ``read(n=1, timeout)``, ``write(data)``, ``in_waiting``,
    ``cancel_read()``, ``send_break(duration=0.25)``, ``close()``, ``is_open``,
    ``port``, ``baudrate`` and ``break_condition``. Read timeouts are implemented in
    software:

    * If `timeout` is None, ``read()`` blocks until `n` bytes are read.
    * If `timeout` is 0, it returns up to `n` bytes that are available immediately.
    * Otherwise it returns up to `n` bytes received within the timeout, and may block
      for up to about 16 ms longer than the timeout.

    The timeout passed to ``read()`` replaces the one given here. Do not set the
    ``timeout`` attribute. ``cancel_read()`` makes a ``read()`` in another thread
    return the bytes read so far within about 16 ms; if no read is in progress, the next
    read returns immediately.
    """
    usb_info = _get_usb_info(port)
    ftdi = usb_info is not None and usb_info[0] == _FTDI_VENDOR_ID

    cls = _Serial
    if ftdi and (_WINDOWS or _MACOS):
        if _ftd2xx is not None:
            cls = _FTD2xxSerial
        else:
            warnings.warn(_FTD2XX_WARNING)

    dev = cls(
        port,
        baudrate=baudrate,
        bytesize=bytesize,
        parity=parity,
        stopbits=stopbits,
        timeout=timeout,
        xonxoff=xonxoff,
        rtscts=rtscts,
        write_timeout=write_timeout,
        dsrdtr=dsrdtr,
        exclusive=exclusive,
    )

    if ftdi and _LINUX:
        _set_low_latency_serial_linux(dev.fd)

    return dev
