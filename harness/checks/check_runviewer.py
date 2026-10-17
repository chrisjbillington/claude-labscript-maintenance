"""Load the compiled example shot with runviewer's Shot class, which runs the runviewer
parser of every device that has one."""

import logging

import numpy as np

from _common import check, finish, load_state

from qtutils.qt import QtWidgets

app = QtWidgets.QApplication([])

import runviewer.__main__ as rv  # noqa: E402
from labscript_utils import device_registry  # noqa: E402
from labscript_utils.connections import ConnectionTable  # noqa: E402

shot_path = load_state()['example_shot']


class Capture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record.getMessage())


capture = Capture()
logging.getLogger('runviewer').addHandler(capture)
logging.getLogger('runviewer').setLevel(logging.INFO)

# Devices with a registered parser must load; devices without one are logged as failed
# by runviewer and that is its normal behaviour.
table = ConnectionTable(shot_path)
with_parser = []
without_parser = []
for name, device in table.table.items():
    try:
        device_registry.get_runviewer_parser(device.device_class)
        with_parser.append(name)
    except Exception:
        without_parser.append(name)
print('devices with a runviewer parser:', with_parser)
print('devices without:', without_parser)
check('pseudoclock' in with_parser, 'DummyPseudoclock has a runviewer parser')

shot = rv.Shot(shot_path)
check(shot.master_pseudoclock_name == 'pseudoclock', f'master pseudoclock {shot.master_pseudoclock_name}')
traces = shot.traces
failed = [m for m in capture.records if m.startswith('Failed to load device')]
for name in with_parser:
    check(not any(m.startswith(f'Failed to load device {name}') for m in failed),
          f'parser for {name} ran without error')
for m in failed:
    print('runviewer log:', m.splitlines()[0])

check(len(traces) >= 1, f'{len(traces)} traces: {sorted(traces)}')
for name, (times, values) in traces.items():
    check(len(times) > 0 and len(times) == len(values), f'trace {name} has {len(times)} points')
    check(np.all(np.diff(times) >= 0), f'trace {name} times are monotonic')
    check(times[0] >= 0 and times[-1] <= shot.stop_time + 1e-6,
          f'trace {name} spans {times[0]:.6g} to {times[-1]:.6g} s of {shot.stop_time} s')

markers = shot.markers
check(len(markers) == 4, f'{len(markers)} markers: {sorted(markers)}')
labels = {m['label'].decode() if isinstance(m['label'], bytes) else str(m['label'])
          for m in markers.values()}
check('Start' in labels and 'End' in labels, f'marker labels {sorted(labels)}')
check(len(shot.channels) == len(traces), f'{len(shot.channels)} channels')
finish()
