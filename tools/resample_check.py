"""Checks of labscript_c_extensions.runviewer.resample through runviewer's calling
convention: x_out = linspace(xmin, xmax, 3*2000+2), y_out of length len(x_out)-1."""
import sys
import numpy as np
from labscript_c_extensions.runviewer.resample import resample

N_OUT = 3 * 2000 + 2
GUARD = 8

def run(x_in, y_in, xmin, xmax, stop_time):
    x_out = np.linspace(xmin, xmax, N_OUT)
    buf = np.full(N_OUT - 1 + GUARD, -999.0)
    y_out = buf[:N_OUT - 1]
    resample(np.float64(x_in), np.float64(y_in), x_out, y_out, float(stop_time))
    return x_out, y_out, buf[N_OUT - 1:]

results = {}

# runviewer #13: a 100 us pulse at t=0 on a 1 s shot, view padded 5% either side as
# pyqtgraph does on auto-range.
x, y, guard = run([0, 1e-4, 1.0], [1, 0, 0], -0.05, 1.05, 1.0)
results['pulse_at_t0_visible'] = np.nanmax(y) == 1
results['pulse_at_t0_guard_intact'] = bool(np.all(guard == -999.0))
results['pulse_at_t0_no_data_before_t0_is_nan'] = bool(np.all(np.isnan(y[x[:-1] < -0.01])))
results['pulse_at_t0_after_stop_is_nan'] = bool(np.all(np.isnan(y[x[:-1] > 1.001])))

# The same pulse with the view start swept over a range of paddings before t=0: which
# output interval t=0 falls in depends on the padding, and the pulse used to be dropped
# whenever the first interval boundary after t=0 was past the end of the pulse.
dropped = 0
for pad in np.linspace(0, 0.05, 101)[1:]:
    x, y, guard = run([0, 1e-4, 1.0], [1, 0, 0], -pad, 1.0, 1.0)
    dropped += np.nanmax(y) != 1
results['pulse_at_t0_paddings_dropping_pulse_of_100'] = int(dropped)

# Same pulse, view starting exactly at t=0 (no padding): worked before, must still.
x, y, guard = run([0, 1e-4, 1.0], [1, 0, 0], 0.0, 1.0, 1.0)
results['pulse_at_t0_unpadded_visible'] = np.nanmax(y) == 1

# REVIEW.md item 19: first data time inside the last output interval. The NaN lead-in
# used to run past the end of y_out.
x_out = np.linspace(0.0, 1.0, N_OUT)
t0 = x_out[N_OUT - 2] + 0.3 * (x_out[1] - x_out[0])
x, y, guard = run([t0, t0 + 1.0], [5, 6], 0.0, 1.0, 2.0)
results['late_first_point_guard_intact'] = bool(np.all(guard == -999.0))
results['late_first_point_values_sane'] = bool(np.all(np.isnan(y[:-1]))) and (np.isnan(y[-1]) or y[-1] in (5.0, 6.0))

# Two input points, both inside the first data interval: the skip-ahead loop used to
# read past the end of x_in.
x, y, guard = run([0, 1e-6], [1, 0], -0.1, 1.0, 1.0)
results['two_points_pulse_visible'] = np.nanmax(y) == 1
results['two_points_tail_is_last_value'] = bool(np.all(y[(x[:-1] > 0.01) & (x[:-1] < 0.99)] == 0))

# A long random trace viewed from t=0 (the common case): output must be unchanged
# between builds; print a checksum.
rng = np.random.default_rng(0)
x_in = np.sort(rng.uniform(0, 10, 50000)); x_in[0] = 0
y_in = rng.normal(size=50000)
x, y, guard = run(x_in, y_in, 0.0, 10.0, 10.0)
results['random_from_t0_checksum'] = float(np.nansum(np.abs(y)))
x, y, guard = run(x_in, y_in, 2.5, 7.5, 10.0)
results['random_zoomed_checksum'] = float(np.nansum(np.abs(y)))
x, y, guard = run(x_in, y_in, -0.5, 10.5, 10.0)
results['random_padded_checksum'] = float(np.nansum(np.abs(y)))

for k, v in results.items():
    print(f'{k:45s} {v}')
