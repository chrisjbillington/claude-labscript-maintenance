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

### Defects and behaviours found by the runs

All verified by running the code (the harness logs show each).

1. **BLACS logs an error with a traceback on its first launch.** `blacs/__main__.py:496`
   `restore_window` reads `tab_data['BLACS settings']["window_xpos"]`, which does not exist
   when there are no saved settings, and the `KeyError` is logged at ERROR level with a
   traceback ("Unable to load window and notebook defaults"). BLACS continues normally.
   Not in ISSUE-TRIAGE.md or REVIEW.md. The harness marks this as known in the `apps`
   step. Fix: check for the keys before restoring, or log at INFO without a traceback.
2. **`runmanager.make_single_run_file` fails for a bare filename.**
   `runmanager/compiler.py:178` calls `os.makedirs(os.path.dirname(filename), exist_ok=True)`,
   which raises `FileNotFoundError` for `''` when `filename` has no directory part. Not in
   REVIEW.md. Fix: skip `makedirs` when the directory part is empty.
3. **`runmanager.globals_diff_shots` raises `UnboundLocalError` for any two shots of one
   sequence**, not only identical shots as REVIEW.md runmanager B7 says: the shot files
   carry the same group definitions (expressions and expansions) and differ only in the
   evaluated values stored as attributes, so `globals_diff_groups` finds no difference.
   The harness marks this as known in the `runmanager-api` step.
4. **`labscript_utils.excepthook` imports `tkinter` at module level**
   (`excepthook/__init__.py:99`), so on a Python without tkinter, lyse, blacs,
   `labscript_utils.connections` and most labscript-devices modules cannot be imported and
   nothing compiles. Ubuntu's `python3.11` from the deadsnakes repository has no tkinter
   package; the uv-managed and python.org interpreters do. Related: ISSUE-TRIAGE.md item 96
   (labscript-utils #104). The harness README lists tkinter as a requirement.
5. **`import labscript_utils` creates a profile** in `~/labscript-suite` when none exists
   (`labscript_utils/__init__.py:22`). Any script that imports labscript_utils on a fresh
   machine writes a profile; the harness creates its profile first so that it owns it.
6. **zprocess tests `test_no_access` and `test_cant_create_files` fail when run as root**
   because root passes the permission checks that they test. They pass as a normal user.
   Environment, not a bug.
7. **`runmanager.get_shot_globals` emits a `FutureWarning`** telling callers to import it
   from `labscript_utils.shot_utils`. Expected deprecation path; the harness does not
   treat it as a failure.
8. **Qt on a bare Linux container** needs `libegl1`, `libopengl0`, `libxkbcommon0`,
   `libdbus-1-3`, `libfontconfig1` and `libglib2.0-0`, which GitHub's `ubuntu-latest`
   image has except `libegl1` and `libopengl0`. The workflow installs them.
9. **Compiler output streaming needs the labconfig security settings.** A plain `zmq`
   PULL socket receives nothing from the batch compiler; the socket must come from
   `labscript_utils.ls_zprocess.Context`, as the runmanager output box does. Documented
   behaviour, noted here because the first version of the harness got it wrong.

### What the harness does not cover yet

- Real devices, and any device class without a dummy implementation.
- The GUI itself beyond start-up: nothing clicks, and rendering is offscreen.
- Conda installs. The plan is to test them once, close to the release, on a machine where
  the pip install already passes.
- PyQt5 and PyQt6: `install --qt PyQt6` and `--qt PyQt5` exist but have not been run.
- Python 3.15, until h5py ships cp315 wheels.
