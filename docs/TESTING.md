# Test harness results

Results of running `harness/suite.py` (see `harness/README.md`) on the component default
branches, and the defects that the runs found. Newest first. Each run is identified by
the date, the platform, the Python version and the commits in the report's component
table.

## 2026-10-17: master branches on Ubuntu 24.04 and Windows Server 2025

Component commits: zprocess 34443e5, qtutils 5d2885f, desktop-app f216ef0,
labscript-c-extensions 4e440ac, labscript-utils cf0fb71, labscript a0787c4, runmanager
bfe63ba, blacs e5757c7, lyse ed0b6ca, runviewer 4989087, labscript-devices 424b9f4,
labscript-suite 0ab902d. Installed from PyPI with them: PySide6 6.12.0, h5py 3.16.0,
pandas 3.0.6, scipy 1.18.1, pyzmq 27.2.0, matplotlib 3.11.2, pyqtgraph 0.14.0. GitHub
Actions runs 39004344513 and 39004626263 in this repository; the local runs were in an
Ubuntu 24.04 container as root.

| Platform | Python | NumPy | Result |
|---|---|---|---|
| Ubuntu, Windows | 3.11 | 2.4.6 | all eight steps pass |
| Ubuntu, Windows | 3.12, 3.13, 3.14 | 2.5.4 | install and imports pass; `compile` fails with `TypeError: data type 'a256' not understood` (labscript #123), so lyse, runviewer and apps are skipped and the compile checks of runmanager-api fail |
| Ubuntu | 3.14 | 2.4.6 (`--pin "numpy<2.5"`) | all eight steps pass, and the zprocess test suite passes (`--all`) |
| Windows | 3.12, 3.14 | 2.4.6 (`--pin "numpy<2.5"`) | all eight steps pass, and the zprocess test suite passes (`--all`, 118 s) |
| Ubuntu, Windows | 3.15.0 | | install fails: h5py 3.16.0 has no cp315 wheel and its source build stops at `Unable to load dependency HDF5` |
| local container | 3.11.15, 3.14.6 | 2.4.6 | all eight steps pass; zprocess test suite 71 passed, 2 failed as root (see below) |

Python 3.11 passes on NumPy 2.5 because NumPy 2.5 requires Python 3.12 or newer, so pip
resolves NumPy 2.4.6 for 3.11 and the `a256` alias still exists. Users on Python 3.11 are
therefore not affected by labscript #123.

Job durations: a fully passing job takes 2 minutes on Ubuntu and 4 minutes on Windows,
of which the install step is about 40 s and the imports step 35 s to 60 s; the zprocess
test suite adds 2 minutes. The labscript-c-extensions Cython extension builds from source
on both platforms.

### Defects found by the runs

Defects that no GitHub issue or review document records are in `DEFECTS.md`: D1 (BLACS
first-launch traceback), D2 (`make_single_run_file` with a bare filename), D3 (tkinter
import in `labscript_utils.excepthook`) and D4 (stale zlock server with another shared
secret). The runs also showed that `runmanager.globals_diff_shots` raises
`UnboundLocalError` for any two shots of one sequence, not only identical shots as
REVIEW.md runmanager B7 says: the shot files carry the same group definitions and differ
only in the evaluated values stored as attributes, so `globals_diff_groups` finds no
difference. The harness marks B7 and D1 as known in the `runmanager-api` and `apps` steps.

### Behaviours worth knowing

All seen by running the code.

1. **`import labscript_utils` creates a profile** in `~/labscript-suite` when none exists
   (`labscript_utils/__init__.py:22`). Any script that imports labscript_utils on a fresh
   machine writes a profile; the harness creates its profile first so that it owns it.
2. **zprocess tests `test_no_access` and `test_cant_create_files` fail when run as root**
   because root passes the permission checks that they test. They pass as a normal user.
3. **`runmanager.get_shot_globals` emits a `FutureWarning`** telling callers to import it
   from `labscript_utils.shot_utils`. Expected deprecation path; the harness does not
   treat it as a failure.
4. **Qt on a bare Linux container** needs `libegl1`, `libopengl0`, `libxkbcommon0`,
   `libdbus-1-3`, `libfontconfig1` and `libglib2.0-0`, which GitHub's `ubuntu-latest`
   image has except `libegl1` and `libopengl0`. The workflow installs them.
5. **Compiler output streaming needs the labconfig security settings.** A plain `zmq`
   PULL socket receives nothing from the batch compiler; the socket must come from
   `labscript_utils.ls_zprocess.Context`, as the runmanager output box does.

### What the harness does not cover yet

- Real devices, and any device class without a dummy implementation.
- The GUI itself beyond start-up: nothing clicks, and rendering is offscreen.
- Conda installs. The plan is to test them once, close to the release, on a machine where
  the pip install already passes.
- PyQt5 and PyQt6: `install --qt PyQt6` and `--qt PyQt5` exist but have not been run.
- Python 3.15, until h5py ships cp315 wheels.
