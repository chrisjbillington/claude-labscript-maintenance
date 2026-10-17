# Test harness results

Results of running `harness/suite.py` (see `harness/README.md`) on the component default
branches, and the defects that the runs found. Newest first. Each run is identified by
the date, the platform, the Python version and the commits in the report's component
table.

## 2026-10-17: lyse #142 (spinning_top) with the merged masters, every Qt binding

Run [39027308813](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39027308813),
dispatched with `lyse=pr/142` (a7de833) and every other component at its master after
the blocker and metadata merges of the day: zprocess e74b638, qtutils 4c9cd95, desktop-app
dc6be4e, labscript-c-extensions 41c0058, labscript-utils 89457f5, labscript 665a73d,
runmanager 264434c, blacs d061535, runviewer 7ea7dc9, labscript-devices 2a2d785,
labscript-suite 4fbc7fc. Ubuntu and Windows, Python 3.11 to 3.15, PySide6, PyQt6 and
PyQt5, plus the `numpy<2.5` job: 31 jobs.

| Jobs | Result |
|---|---|
| 25 jobs: both OSes, Python 3.11 to 3.14, all three bindings, NumPy 2.5.4 (2.4.6 on 3.11), plus the pinned job | all eight steps pass, so the merged masters compile on NumPy 2.5.4 and the lyse branch reads shots and saves results on every binding |
| 6 jobs: Python 3.15 | install fails on h5py as before |

The run was dispatched before the commit that adds the `spinning_top` checks to the
harness `lyse` step reached `main`, so those checks did not run here; they were run by hand
in the local venvs, where lyse master reports KNOWN and the branch reports FIXED for both.

## 2026-10-17: zprocess v2.28.0rc1 release run

Tag `v2.28.0rc1` pushed at 10:41 UTC on e74b638 of chrisjbillington/zprocess, the head of
`master` and `maintenance/2.28.x`, with the release workflow synced from
rpanderson/workflow-sandbox #46 (zprocess PR #30).

| Push | Run | Version built | Published |
|---|---|---|---|
| branch `maintenance/2.28.x` at e74b638 | [39025269576](https://github.com/chrisjbillington/zprocess/actions/runs/39025269576) | 2.28.0.dev11 on all four runners | Test PyPI and the Anaconda test label (skipped as already existing from the master run) |
| tag `v2.28.0rc1` | [39025867956](https://github.com/chrisjbillington/zprocess/actions/runs/39025867956) | 2.28.0rc1 on ubuntu-latest, macos-latest and macos-15-intel; **2.28.0.dev11 on windows-2022** | PyPI (sdist and pure wheel, with attestations), GitHub pre-release with the sdist attached, Anaconda main label for linux-64, osx-64 and osx-arm64 (Python 3.11 to 3.15); the win-64 2.28.0.dev11 packages were skipped as already existing under the test label |

The Windows job's "Ignore tags other than the pushed tag" step logged
`Deleted tag 'v2.28.0rc1' (was e74b638)`: it ran under PowerShell, where
`${GITHUB_REF_NAME}` is empty. Recorded as defect D7 in `DEFECTS.md`. The Anaconda main
label therefore has no win-64 zprocess 2.28.0rc1 packages.
## 2026-10-17: zprocess maintenance/2.28.x branch build

Branch `maintenance/2.28.x` pushed at e74b638 (the head of master) for release sequence
step 1. [Run 39025269576](https://github.com/chrisjbillington/zprocess/actions/runs/39025269576)
of `release.yml`: the configure job and the four build jobs (ubuntu-latest, windows-2022,
macos-latest, macos-15-intel) pass, the sdist, pure wheel and conda packages are
published to TestPyPI and the Anaconda test label, and the three release jobs (GitHub
release, PyPI, Anaconda) are skipped, as they should be for an untagged push. The
`v2.28.0rc1` tag is a local task (`LOCAL-TASKS.md`).

## 2026-10-17: fixes for the remaining release pull requests

Maintainer fix commits for the pull requests of `RELEASE-PLAN.md` section 4.3 that were
still open after labscript-devices #110 and lyse #132 merged. Each is one commit on the
pull request head, stored in `patches/` with a `LOCAL-TASKS.md` row, because every
branch is on a contributor's fork. Each fix was checked in its own venv (Python 3.14.6,
NumPy 2.5.4, h5py 3.16.0, PySide6 6.12.0, every component installed from its clone at
the state of the fix branch) on the Ubuntu container.

**labscript-utils #117, example analysis script** (`example-117-fixes`, patch
`labscript-utils-117-example-analysis-fixes.patch`). The script as submitted fails on
its first statement after the imports with `AttributeError: module 'lyse' has no
attribute 'spinning_top'` when run the way lyse's analysis subprocess runs it (a
`__main__` module with `lyse.utils.worker.path` set to the shot). The review's claim
that `save_result` of a dict of arrays raises `TypeError` is wrong: it stores the dict
JSON-encoded as a 5.6 kB group attribute (`PR-REVIEW.md`, correction). After the fix:
the harness `profile`, `compile` and `lyse` steps pass with the branch installed; the
script run as lyse runs it finishes against the compiled example shot and saves the
`analog_out` (float64, 254 values, 0 to 1) and `digital_out` (int8, 254 values) datasets
and the `analog_out_max` attribute (1.0) under `results/example_analysis_script`;
`lyse.Run` reads them back and `get_dataframe_from_shot` has the
`('example_analysis_script', 'analog_out_max')` column; the deprecated standalone mode
with the shot path as an argument also runs. The branch merges cleanly into master.

Draft comment for #117: "Thanks for this; a runnable example with the dummy devices is
useful. Two defects before merging. `lyse.spinning_top` on line 8 no longer exists: lyse
moved it to `lyse.utils.worker` in 3.3.0rc1, so the script raises `AttributeError` as
soon as lyse runs it. `lyse.path` is the current shot inside lyse and `None` outside it.
`run.save_result('foobar', result)` with a dict of two arrays does run, but it JSON-encodes
the 254-element arrays into a group attribute and the lyse dataframe then gets nested
series in its cells; `save_result_array` for the arrays and `save_result` for a scalar is
the intended use. The x axis is labelled `time (ms)` but `OUTPUTS` has one row per clock
tick, and `run_globals`, `pulse`, the `np.array()` wrappers and the 'image processing'
comment are left over from the camera example. I have pushed a commit with these changes
to this branch."

**labscript-devices #126, AD9959 DDS Sweeper** (`ad9959-126-fixes`, patch
`labscript-devices-126-ad9959-fixes.patch`). Firmware behaviour checked in the
dds-sweeper repository (QTC-UMD/dds-sweeper d56ff74, firmware 0.4.0): `main()` sets the
Pico system clock to 125 MHz; `setclock` mode 0 sets it to the given frequency; mode 1
(external reference) only sets the AD9959 reference and does not change the Pico clock.
So `clock_limit`, which divided `ref_clock_frequency` by the Pico cycles per instruction,
was wrong for an external reference; it now divides the Pico system clock, 125 MHz when
the reference is external. Checks on the fixed branch: the harness `profile`, `imports`
and `compile` steps pass; an experiment with a `DummyPseudoclock`, an
`AD9959DDSSweeper(dynamic_channels=2)`, `DDS` children on channels 0 and 1 and `StaticDDS`
children on channels 2 and 3, with changes at 0, 1, 2 and 3 ms and stop at 4 ms, compiles
through runmanager; `runviewer.__main__.Shot` loads the shot with no device failure and
the rewritten parser gives twelve traces with one point per clock tick at 0 to 4 ms and
the programmed values (10 and 11 MHz, amplitudes 0.5 and 0.6, phase 0 then 90 degrees on
channel 0; constant 30 MHz, 0.25, 45 degrees on static channel 2) to within the DDS
quantisation (0.116 Hz, 1/1023, 360/16384); a static-only experiment does the same;
`sweep_mode=1` raises `LabscriptError` at construction; `clock_limit` is 250 kHz,
166.7 kHz and 100 kHz for one, two and four dynamic channels at the default clock and
stays at 166.7 kHz for two channels with an external 100 MHz reference (the old code
gave 133.3 kHz for an internal 100 MHz reference, which is correct, and would have given
333 kHz for an external 250 MHz reference, which is not); the worker, tab, parser and
`register_classes` modules import under offscreen Qt with deprecation warnings as
errors. The worker was not run: no hardware. Noticed and not fixed:
`AD9959DDSSweeperInterface.get_freqs` compares `readline().decode()` with `"ok"` without
stripping the newline, so it would never terminate; the worker does not call it. The
branch merges cleanly into master.

Draft comment for #126: "I have pushed a follow-up commit to this branch. The runviewer
parser could not run: `DDSs` was undefined, `np.float` no longer exists, the assignments
used `'%d_freq'` field names while the dtype declared `freq%d`, and the traces were
passed to `add_trace` without a time axis. It is rewritten after the NovaTechDDS9M
parser and shows the dynamic and static channels at the clockline ticks. `clock_limit`
divided `ref_clock_frequency` by the Pico cycles per instruction, but the firmware sets
the Pico system clock from that frequency only in `setclock` mode 0; with
`ref_clock_external=1` the Pico stays at 125 MHz, so the limit is now computed from the
Pico system clock and the docs say so. Also: `sweep_mode != 0` is rejected in the
constructor instead of at `setb` time, the remaining `assert`s in `blacs_workers.py`
raise `LabscriptError`, `transition_to_manual` waits a fixed 5 s for `STOPPED` rather
than 1000 status queries, and the `.. note::` in the docs is indented so it renders.
Verified by compiling a DummyPseudoclock experiment with two DDS and two StaticDDS
channels and loading it in runviewer. I have no hardware to run the worker, so please
check the worker changes on your setup."

**labscript-devices #144, Andor fixes** (`andor-144-fixes`, patch
`labscript-devices-144-andor-fixes.patch`). The Andor SDK is a Windows DLL, so the
checks are static. `andor_utils.py` from the PR head fails to byte-compile on Python
3.11.15 (`SyntaxError: f-string: unmatched '['`); after the fix the three changed files
byte-compile on 3.11.15 and 3.14.6. Importing `andor_utils` from the fixed branch stops
only at loading the missing `atmcd64d.dll`; `AndorSolis.blacs_workers` imports. After the
fix the pull request no longer touches `IMAQdxCamera/blacs_workers.py`, merges cleanly
into master and no longer conflicts with #148 (the PR head conflicts with #148 on both
worker files). Confirmed in `andor_capabilities.py` that `camera_type.get_type` returns
names such as `IXONULTRA`, so the PR's `'IXION ULTRA'` and `'IXON ULTRA'` comparisons
never matched.

Draft comment for #144: "Thanks for these fixes; the cooldown-before-EM-gain ordering,
the `GetKeepCleanTime` fallback and the `SetIsolatedCropMode` fallback are all needed. I
have pushed a commit on top of your branch that fixes four problems. The `print` in
`setup_acquisition` nested the string's own quote inside the f-string, which is a
SyntaxError before Python 3.12 and made `andor_utils` unimportable on 3.11. The model
comparisons used `'IXION ULTRA'` and `'IXON ULTRA'`, but `camera_type.get_type` returns
names like `'IXONULTRA'`, so an iXon Ultra never took the `SetIsolatedCropModeEx` branch;
it is now `'IXONULTRA' in self.model`. The EM gain range check used strict comparisons
and rejected the endpoints; it is now inclusive. The single-mode branch uses
`images.extend(list(downloaded))` like the other branches. As you offered, the fast
acquisition setup, the semaphore and the IMAQdx worker change are left for a separate
pull request: the semaphore is only released in single mode, so `transition_to_buffered`
blocks forever in kinetic-series and fast-kinetics modes, and both changes conflict with
the TriggerableCamera refactor in #148. The debug prints of the gain range and
attributes are also removed."

**prawn_digital_output #23, testing notebook** (`testing-notebook-23-fixes`, patch
`prawn_digital_output-23-testing-notebook-fixes.patch`). No hardware here; the notebook
parses as JSON and validates as nbformat 4.5, is 9 KB after the outputs are stripped
(192 KB before), every code cell compiles and `KeysightScope.py` byte-compiles. The
`send()` helper extracted from the notebook and called with a stand-in `serial` module
in which `Serial()` raises prints the original error and returns an empty string; the
PR head's version raises `AttributeError: 'NoneType' object has no attribute 'close'`
instead. The branch merges cleanly into main.

Draft comment for #23: "I pushed a small follow-up commit to this branch. It strips the
notebook outputs (the file drops from 192 KB to 9 KB, so re-running it no longer
produces a diff), moves `PORT`, the scope's VISA resource pattern and the two image
flags into a commented parameters cell and passes the pattern to `KeysightScope`, and
resets the kernelspec from the machine-specific `Pico` kernel to `python3`. It also
changes the `if SHOW_IMAGES: ... elif SAVE_IMAGES:` blocks to two independent `if`s so
a screenshot can be shown and saved in the same run, and makes the `finally` in `send()`
only call `conn.close()` when `serial.Serial()` succeeded, so a failed port open reports
the original error instead of an `AttributeError`. A first markdown cell lists the
packages needed. I could not run the hardware steps; the notebook validates and every
cell compiles."

**labscript-devices #87, background subtraction** (`imaqdx-87-fixes`, patch
`labscript-devices-87-imaqdx-background-fixes.patch`). Run offscreen with pyqtgraph 0.14.0
on PySide6, with the PR branch merged with master because the PR's base still had
`QtGui.QApplication` in `handler`. On the PR as submitted, "Set background" with no frame
raises `AttributeError: 'NoneType' object has no attribute 'swapaxes'` and a frame of a
different height and width raises `ValueError` in the main thread; a 2-D background and a
3-D post-shot stack broadcast and display correctly, contrary to the review. After the
fix, a real `ImageReceiver` with a real `pg.ImageView` and the tab's buttons from the `.ui`
file was driven through `handler()`: set-background with no frame returns False and leaves
the buttons; a 120 by 100 frame displays; set-background then shows zeros and swaps the
buttons; an 80 by 90 frame displays unsubtracted; a same-shape frame displays as the
difference; a stack of three has the background subtracted from each image; with the
stack as background a 2-D frame and a stack of two display unsubtracted and the same stack
shows zeros; the autolevels button makes the levels follow the frame; clear restores the
raw frame and the buttons. One frame sent over ZMQ from a REQ socket as the worker sends
it is answered `ok` and displayed. The same script passes on master with both the #87 and
#63 fixes merged.

Draft comment for #87: "I have pushed a small follow-up commit to this branch that fixes
the two cases zakv found. In `ImageReceiver`, `set_bg_image()` before any frame had
arrived stored `None` as the background and `update_image()` then failed on `swapaxes`;
it now returns False with no change, and the tab leaves the buttons as they are. A
background with a different shape from the incoming frame raised `ValueError` in the
main thread after the worker had been sent `ok`; the subtraction now happens only when
the background shape matches the frame's trailing dimensions, so a 2-D background is still
subtracted from each image of a post-shot stack and anything else is displayed
unsubtracted. The 'Set background' tooltip now says the subtraction affects the display
only. Tested offscreen with pyqtgraph 0.14.0 on PySide6; the branch merges cleanly with
master and with #63."

**labscript-devices #63, restore display settings** (`imaqdx-63-fixes`, patch
`labscript-devices-63-imaqdx-restore-fixes.patch`). `hasattr(pg.ImageView, 'getLevels')`
is False, but `ImageView.__init__` binds `getLevels` from the histogram onto each instance
in pyqtgraph 0.10.0, 0.11.0, 0.12.0, 0.13.0, 0.14.0 and master (sources read on GitHub),
so the author's `self.image.getLevels()` works and is kept; the review's claim that
`get_save_data` raises is wrong (`PR-REVIEW.md`, correction). Running the save and
restore round trip repeatedly on the PR as submitted shows the view range growing by
pyqtgraph's default padding each time (31 to 103, then 23.8 to 110.2, then 15.16 to
118.84); with `padding=0` the ranges round-trip exactly. After the fix, the tab's own
`get_save_data` and `restore_save_data` run on a stub holding a real `pg.ImageView`: with
no image only the original keys are saved; after a frame, zoom, pan, auto-range on y and
levels 250 and 2500 the saved dict survives `repr` and `eval` with Python float and bool
types, a fresh view restored from it has the same `targetRange`, `autoRangeEnabled`
`[False, 1.0]` and levels `(250.0, 2500.0)`, the first frame displayed afterwards keeps
them, a 3-D stack shape saves and restores, and save data without the new keys restores
without error. Zero images of 2-D and 3-D shape display without the nonzero-pixel
workaround on 0.14.0 (fixed in pyqtgraph 0.11.0, pull request 767). Passes on the branch
merged with master and on master with both the #63 and #87 fixes.

Draft comment for #63: "Thanks for this; it works as described with current pyqtgraph
(`ImageView.getLevels()` is a per-instance forward to the histogram, present in 0.10
through 0.14). Running the save and restore round trip repeatedly showed one problem:
`view_box.setRange(xRange=..., yRange=...)` in `restore_save_data` applies pyqtgraph's
default padding, so the saved range grows by about 20 % on every BLACS restart;
`padding=0` fixes it and the ranges then round-trip exactly. I have pushed a follow-up
commit with that change; it also converts the saved ranges and levels to Python floats
(BLACS restores save data with `eval`, which fails on numpy 2's `np.float64(...)` repr)
and drops the one-nonzero-pixel workaround, since pyqtgraph 0.11 fixed that. Merges
cleanly with master and with #87."

**Not done from the cloud.** The fix branches could not be pushed to the upstream
repositories (the proxy refused the pushes), so the test workflow has not run on them.
`LOCAL-TASKS.md` has the dispatches to run with the pull request refs once the fixes are
on the pull request branches. Also found: the camera tab's Copy button uses
`QtGui.QApplication` and fails under Qt6 bindings (`DEFECTS.md` D6).

## 2026-10-17: lyse #132 data-group attributes in the dataframe

lyse PR #132 (head 6066df4) merged into lyse master 01246cf, plus commit 724de8c, which
reads the `data/` groups before the `results/` groups and merges each group's attributes
into `row[name]` with `setdefault(...).update(...)` instead of assigning (local branch
`pr132-work` in `repos/lyse`; pushed upstream as `data-attributes-132-fix`). Python
3.14.6, pandas 3.0.6, h5py 3.16, with the clone on `PYTHONPATH`. A script writes a shot
file with `results/fr` (attributes `fitted=42.0`, `shared='from results'`), `data/fr`
(`raw=7`, `shared='from data'`), `data/other` (`temperature=300.0`) and a dataset
`data/waits`, then calls `get_nested_dict_from_shot` and `get_dataframe_from_shot`.

| Version | `row['fr']` | dataframe columns under `fr` and `other` |
|---|---|---|
| master 01246cf | `{'fitted': 42.0, 'shared': 'from results'}`; `data/` not read | `(fr, fitted)`, `(fr, shared)` |
| PR head 6066df4 | `{'raw': 7, 'shared': 'from data'}`: the results attributes are lost | `(fr, raw)`, `(fr, shared)`, `(other, temperature)` |
| with 724de8c | `{'raw': 7, 'shared': 'from results', 'fitted': 42.0}` | `(fr, fitted)`, `(fr, raw)`, `(fr, shared)`, `(other, temperature)` |

The dataset `data/waits` gives an empty `row['waits']` in both the PR head and the fix,
and no column.

**GitHub Actions:** dispatch with `lyse=data-attributes-132-fix` and every other
component at master,
[run 39022914882](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39022914882).
The 24 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with PySide6, PyQt6 and PyQt5
pass all eight steps, as does the `numpy<2.5` job; the six Python 3.15 jobs fail at the
h5py build as before. The fix commit is cherry-picked onto the PR head 6066df4 as
001df5f (local branch `pr132-head` in `repos/lyse`); that branch merged with master
01246cf has the same tree as 724de8c, so the run covers it.

## 2026-10-17: labscript-devices #110 Windfreak SynthHD

labscript-devices PR #110 (head 52f74fa) merged into master 2183314, plus one commit with
the four fixes from the review (local branch `pr110-work` in `repos/labscript-devices`,
0593f45; not pushed): `raise` on the channel-range `LabscriptError`, `self.name` in
`enable_output`, a `quantity` argument to `validate_data` so the message names the
quantity and unit, and `NI_DAQmx.models` in the docs example. Python 3.14.6, NumPy
2.5.4, labscript 665a73d, with the clone on `PYTHONPATH` in front of the installed
labscript-devices. A script compiles a connection table with a `WindfreakSynthHDPro`,
two `StaticDDS` children on `channel 0` and `channel 1`, and `enable_output(0)`; the
`windfreak` package is not needed for compilation.

| Case | PR head 52f74fa | With the fixes |
|---|---|---|
| two channels, 1 GHz at 0 dBm and 90 degrees, 2 GHz at -10 dBm | `STATIC_DATA` row `freq0=1e9, freq1=2e9, amp0=0.0, amp1=-10.0, phase0=90.0, phase1=0.0, gate0=True, gate1=False` | same |
| third child on `channel 2` | `ValueError: no field of name freq2` from numpy, after the unraised `LabscriptError` | `LabscriptError: Static RF:wf_b has invalid connection string. Only 'channel 0' or 'channel 1' is allowed.` |
| amplitude 25 dBm (limit 20) | `LabscriptError: ... can only have frequencies between -4.000000E+01Hz and 2.000000E+01Hz, 25.0 given` | `LabscriptError: Static RF wf_a can only have amplitudes in dBm between -40.0 and 20.0, 25.0 given` |
| `enable_output(5)` | `AttributeError: 'WindfreakSynthHD' object has no attribute 'device'` | `LabscriptError: Channel 5 is not a valid option for wf2.` |

The module imports with `-W error::DeprecationWarning`. The docs example's import path
`labscript_devices.NI_DAQmx.Models.NI_USB_6343` does not exist; the directory is
`models`.

**GitHub Actions, PR head alone:** the dispatch with `labscript-devices=pr/110`,
[run 39021953009](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39021953009),
fails the `imports` step in every job because the harness imports
`labscript_devices.PrawnDO.labscript_devices`, which master gained after this branch was
made; the branch is 68 commits behind master. The other steps pass in the `numpy<2.5`
job. A head that is behind master has to be tested merged with master, so the merged
branch with the fixes was pushed to labscript-suite/labscript-devices as
`windfreak-110-fixes` (0593f45) and dispatched:
[run 39022423569](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39022423569),
every other component at master. The 24 jobs on Ubuntu and Windows for Python 3.11 to
3.14 with PySide6, PyQt6 and PyQt5 pass all eight steps, as does the `numpy<2.5` job; the
six Python 3.15 jobs fail at the h5py build as before. The harness should derive its
module list from the installed package rather than a fixed list (`harness/suite.py`,
`imports` step).

## 2026-10-17: blacs #123 plugin-loading fixes

blacs PR #123 (head 4ec904f, three commits) merged into blacs master bc3fd1f, with one
commit on top that shortens the two added comment blocks (local branch `pr123-work`,
f1aea3f, in `repos/blacs`; not pushed). Every other component at its upstream master
of 09:00 UTC. Python 3.14.6, PySide6, NumPy 2.5.4, on the Ubuntu container.

**Harness:** all eight steps pass (versions, profile, imports, compile, lyse,
runviewer, runmanager-api, apps). BLACS starts, loads the `connection_table`,
`general` and `theme` plugins and runs for five seconds without a traceback.

**The `[DEFAULT]` collision, reproduced.** The active labconfig was given
`connection_table = %(labscript_suite)s/userlib/connection_table.py` under `[DEFAULT]`
and the `connection_table = True` line was removed from `[BLACS/plugins]`, which is the
state of a labconfig that has never had the flag written.

| `blacs/plugins/__init__.py` | `import blacs.plugins` |
|---|---|
| master bc3fd1f | raises `ValueError: Not a boolean: /root/labscript-suite/userlib/connection_table.py` from `configparser`, so BLACS cannot start |
| PR #123 | logs `WARNING BLACS.plugins: Plugin 'connection_table' shares its name with a labconfig [DEFAULT] key; using the default enabled state.` and imports; the plugin is enabled, as it is in `default_plugins` |

The `has_option` change in the same commit does not change behaviour: CPython's
`RawConfigParser.has_option` returns true for inherited `[DEFAULT]` keys, as `items()`
does. The `try/except ValueError` block is the fix.

**GitHub Actions:** dispatch of `.github/workflows/test.yml` with `blacs=pr/123` (head
4ec904f, without the comment commit) and every other component at its upstream master,
[run 39021000880](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39021000880),
started 09:24 UTC. The 24 jobs on Ubuntu and Windows for Python 3.11 to 3.14 with
PySide6, PyQt6 and PyQt5 pass all eight steps, as does the `numpy<2.5` job; the six
Python 3.15 jobs fail at the h5py build as before.

**Draft comment for the PR**, to post once approved:

> Reviewed for the Python 3.11 to 3.15 release. All three changes are correct and
> reproduce as described:
>
> - With `connection_table = <path>` under `[DEFAULT]` and no `connection_table` flag in
>   `[BLACS/plugins]`, `import blacs.plugins` on master raises `ValueError: Not a
>   boolean` from `configparser`; on this branch it logs the warning and BLACS starts.
> - `str.strip('.h5')` in `compile_and_restart.py` removes any trailing `.`, `h` or `5`
>   characters, so the `os.path.splitext` change (third commit, not in the description)
>   is a real fix too.
>
> Two small things before merging:
>
> 1. `has_option()` also returns true for inherited `[DEFAULT]` keys (CPython
>    `RawConfigParser.has_option` checks `self._defaults` as well as the section), so
>    the change from the `items()` membership test is fine but is not part of the fix;
>    the `try/except ValueError` block is. The description's "asks the question
>    directly" sentence should go.
> 2. The two comment blocks describe the alternative that was not taken. Suggested
>    replacements: in `plugins/__init__.py`, "The section inherits the labconfig
>    `[DEFAULT]` keys, so a plugin with the same name as one of them reads that key's
>    value here. An option set in the section itself overrides the inherited value." In
>    `__main__.py`, "Call `plugin_setup_complete` once, with the arguments its signature
>    accepts."
>
> The branch merged with master passes the suite's end-to-end checks on Python 3.14 with
> PySide6 (install, import, compile, lyse, runviewer parsers, runmanager API, application
> start-up) and is being run on Ubuntu and Windows for Python 3.11 to 3.14 with PySide6,
> PyQt6 and PyQt5.

## 2026-10-17: master branches after the blocker merges, every Qt binding

Dispatch of `.github/workflows/test.yml` with no refs, so every component at its
upstream default branch, after the last of the blocker pull requests merged (blacs #125
at 08:44 UTC). [Run 39019282114](https://github.com/chrisjbillington/claude-labscript-maintenance/actions/runs/39019282114),
started 08:57 UTC. Commits: labscript 665a73d, labscript-utils 89457f5, labscript-devices
2183314, blacs bc3fd1f, lyse 01246cf, runmanager 264434c, runviewer 7ea7dc9,
labscript-suite 4fbc7fc, labscript-c-extensions 41c0058, zprocess e74b638, desktop-app
dc6be4e, qtutils 4c9cd95. Ubuntu and Windows, Python 3.11 to 3.15, PySide6, PyQt6 and
PyQt5, plus the `numpy<2.5` job: 31 jobs.

| Jobs | Result |
|---|---|
| 24 jobs: both OSes, Python 3.11 to 3.14, all three Qt bindings | all eight steps pass |
| Ubuntu 3.14 PySide6 `numpy<2.5` | all eight steps pass |
| 6 jobs: Python 3.15 on both OSes, each binding | install fails building h5py 3.16.0 from source, as before; nothing else runs |

This is the first run of the master branches that compiles a shot on NumPy 2.5: the
previous master run (below) failed at the compile step on every job without the
`numpy<2.5` pin. Jobs took about two minutes on Ubuntu and three to five minutes on
Windows.

## 2026-10-17: version specifiers and development versions

Checked with `packaging` 26.3 on Python 3.14.6, the library that pip uses for version
matching: `3.5.0.dev12`, `3.4.1.dev3` and `3.5.0rc1` do not satisfy `>=3.5.0`, with
pre-releases excluded or allowed; `3.5.0` does. A master checkout of a component builds
as the next minor version with a `.devN` suffix, so the raised pins in runmanager #131
and labscript-suite #106 cannot be met by source installs or release candidates of the
pinned packages, only by their final releases. Released versions on PyPI on this date:
labscript 3.4.2, labscript-utils 3.4.3, labscript-devices 3.3.0, blacs 3.2.3, lyse
3.3.0, runmanager 3.3.0, runviewer 3.2.4, labscript-suite 3.3.0.

## 2026-10-17: zprocess #28 on Windows 11, BLACS restart from a console

zprocess PR #28 (head 81b1b10) on Windows 11 Pro build 26200 with Windows Terminal
1.24.12741.0, Windows PowerShell 5.1 (PSReadLine 2.0.0) and cmd.exe. The labscript
environment is the machine's Python 3.12.7 install: blacs 3.2.3, labscript-utils 3.4.1,
labscript 3.4.0, labscript-devices 3.3.0, runmanager 3.3.0, qtutils 4.0.0 on PyQt5
5.15.11, NumPy 2.4.2, h5py 3.15.1, pywin32 311, with zprocess 2.27.0 before and the PR
branch (version 2.28.0.dev5) after. One run used a Python 3.14.3 venv with blacs 3.2.3,
labscript-utils 3.4.3, PyQt6 6.11.0, NumPy 2.4.6 and zprocess 2.27.1. The connection
table is the default profile's `example_apparatus` with the dummy devices. In each run
BLACS was started with the `blacs` command, the connection table was recompiled from
the Connection Table menu (which runs the runmanager batch compiler) and "Restart BLACS"
was pressed in the recompile dialog. A `sitecustomize` hook on `PYTHONPATH` recorded
the start, the exit and any unhandled exception of every Python process to a file, and
a helper attached to the console of the running processes and read the console input
mode with `GetConsoleMode`.

| Console | Shell | zprocess | Result |
|---|---|---|---|
| Windows Terminal | cmd.exe | 2.27.0 | BLACS restarts |
| Windows Terminal | PowerShell | 2.27.0 | the relaunched process exits at `import labscript_utils` with `pywintypes.error: (87, 'SetConsoleMode', 'The parameter is incorrect.')`, the traceback of zprocess #27; the BLACS log ends with "relaunching BLACS after quit" |
| Windows Terminal | PowerShell | 2.27.1, Python 3.14 venv | BLACS restarts, twice (timing, see below) |
| Windows Terminal | PowerShell | PR #28 | BLACS restarts, twice; no exception recorded; input mode of the restarted BLACS 0x1a4, quick-edit off |
| classic console (`conhost.exe`) | cmd.exe | PR #28 | BLACS starts and the input mode changes from 0x1f7 to 0x1b7, quick-edit off; BLACS restarts with mode 0x1a7, quick-edit off; after BLACS exits the mode is 0x1e7, quick-edit on |

Cause, found with a script that calls `disable_quick_edit`, relaunches itself as BLACS
does (`Popen([sys.executable] + sys.argv)`, then exits) and calls `disable_quick_edit`
again in the child:

- While Windows PowerShell waits at its prompt, the console input mode is 0x1e4:
  `ENABLE_ECHO_INPUT` set and `ENABLE_LINE_INPUT` clear. cmd.exe leaves 0x1e7 at its
  prompt. `disable_quick_edit` adds `ENABLE_EXTENDED_FLAGS` and clears
  `ENABLE_QUICK_EDIT_MODE`, so after PowerShell it asks for 0x1a4.
- `SetConsoleMode` rejects every input mode that has `ENABLE_ECHO_INPUT` without
  `ENABLE_LINE_INPUT`, which its documentation requires: from a cmd.exe console it
  accepted 0x1f7, 0x1b7, 0x1e7, 0x1a7, 0x1a6 and 0x1a0 and returned error 87 for 0x1e4,
  0x1a4 and 0x1a5.
- With the child waiting 3 s before `disable_quick_edit`, so that the prompt has
  returned: from PowerShell, zprocess 2.27.1 raised error 87 in 3 of 3 runs and the PR
  branch returned in 3 of 3; from cmd.exe no run failed on any version. Without the
  wait, 2.27.0 and 2.27.1 failed in 4 of 7 runs from PowerShell. The failure also
  occurred in a classic `conhost.exe` window with PowerShell and never in Windows
  Terminal with cmd.exe, so the ConPTY console is not the cause. Python 3.12 and 3.14,
  and a venv or the system install, made no difference in the script.
- The two successful restarts of the 3.14 venv on 2.27.1 are consistent with timing:
  there the venv launcher process exited one second after the relaunched BLACS started,
  whereas in the system install the launcher exited in the same second, so the prompt
  with its 0x1e4 mode may not be back yet when the relaunched process runs
  `disable_quick_edit`. Plausible, not verified.
- After the failing call `GetConsoleMode` returns 0x1a4, so quick-edit is off in the
  relaunched process whether or not the call raised.

The comment that PR #28 adds attributes the failure to ConPTY consoles such as Windows
Terminal; it should name the console mode that PowerShell leaves at its prompt instead,
for example: "The console rejects the mode. This happens when the process was relaunched
from a PowerShell prompt: while PSReadLine waits for input it leaves ENABLE_ECHO_INPUT
set without ENABLE_LINE_INPUT, and SetConsoleMode rejects that combination."

Posted on the PR on 2026-10-17 as
[a comment](https://github.com/chrisjbillington/zprocess/pull/28#issuecomment-6231503544);
the PR description was updated to the same cause, and commit 256ac43 on the branch
rewords the comment in the `except` branch, with no change in behaviour.

## 2026-10-17: workflow-sandbox #46 tag step, local simulation

The "Ignore tags other than the pushed tag" step of workflow-sandbox #46 (head 6f21e86),
run outside GitHub Actions in a local clone with `GITHUB_REF_NAME` set by hand, followed
by `ci-helper distinfo version .` (ci-helper 0.4.0) and `python -m setuptools_scm`
(setuptools_scm 10.3.4, Python 3.14.8). The two tags `v0.6.0rc2` and `v0.6.0` were
created at 6f21e86, which has `v0.6.0rc1` as an ancestor 70 commits back. The two tools
agreed in every case.

| Tags at HEAD | Pushed ref | Step run | Version |
|---|---|---|---|
| both, annotated, final created after rc | `v0.6.0rc2`, `v0.6.0` or `master` | no | 0.6.0 |
| both, annotated, rc created after final | `v0.6.0` | no | 0.6.0rc2 |
| both, lightweight | `v0.6.0rc2`, `v0.6.0` or `master` | no | 0.6.0 |
| both, annotated or lightweight, either order | `v0.6.0rc2` | yes | 0.6.0rc2 |
| both, annotated or lightweight, either order | `v0.6.0` | yes | 0.6.0 |
| both, annotated or lightweight | `master` | yes | 0.7.0.dev70 |

Without the step the version is the tag that `git describe` picks, which for annotated
tags is the one with the newest tagger date, so a commit tagged final-then-rc, or re-tagged
rc after the final tag, builds the rc version on a final-tag push (labscript-suite #56).
With the step only the pushed tag remains at HEAD and the version is that tag's; a branch
push of a tagged commit builds a development version from the nearest ancestor tag.

The same was then done with real pushes to chrisjbillington/workflow-sandbox, where
uploads are disabled because `RELEASE_REPO` does not match, so only the configure, build
and GitHub release jobs run. Commit 6f21e86 was pushed as branch `fix-multiple-tags`,
then tagged `v0.6.0rc2` (annotated) and pushed, then tagged `v0.6.0` (annotated) and
pushed, then pushed as branch `maintenance/tag-test`. Every job of the three runs
succeeded.

| Push | Run | Tags deleted by the step | `PKGVER` | Built | GitHub release |
|---|---|---|---|---|---|
| tag `v0.6.0rc2` | [39011505494](https://github.com/chrisjbillington/workflow-sandbox/actions/runs/39011505494) | none | 0.6.0rc2 | `workflow_sandbox-0.6.0rc2` sdist, wheel and noarch conda package | draft, prerelease, sdist attached |
| tag `v0.6.0` on the same commit | [39011701607](https://github.com/chrisjbillington/workflow-sandbox/actions/runs/39011701607) | `v0.6.0rc2` | 0.6.0 | `workflow_sandbox-0.6.0` sdist, wheel and conda package | draft, not prerelease, sdist attached |
| branch `maintenance/tag-test` at the same commit | [39011875494](https://github.com/chrisjbillington/workflow-sandbox/actions/runs/39011875494) | `v0.6.0rc2`, `v0.6.0` | 0.7.0.dev70 | `workflow_sandbox-0.7.0.dev70` sdist, wheel and conda package | skipped (`RELEASE=false`) |

So `actions/checkout` with `fetch-depth: 0` fetches the other tags at HEAD,
`GITHUB_REF_NAME` is the bare tag name on a tag push, and the step deletes the right
tags in both the configure and the build job. The test tags, branches and draft releases
were left in the fork.

## 2026-10-17: blocker fix pull requests on GitHub Actions, every Qt binding

Two dispatches of `.github/workflows/test.yml`, as the CLAUDE.md rule asks before a merge.

**Run 39009659742, the fix pull requests, full matrix.** Refs: labscript pr/124
(3a328ae), labscript-devices pr/149 (e346f44), blacs pr/124 (1284b5d), zprocess pr/28
(81b1b10), labscript-utils pr/129 (490f49b); the other seven components at master. Ubuntu
and Windows, Python 3.11 to 3.15, PySide6, PyQt6 and PyQt5, plus the `numpy<2.5` job: 31
jobs.

| Jobs | Result |
|---|---|
| 24 jobs: both OSes, Python 3.11 to 3.14, all three Qt bindings, NumPy 2.5.4 (2.4.6 on 3.11) | all eight steps pass. The example experiment compiles on NumPy 2.5.4 and lyse, the runviewer parsers, the runmanager API and all four applications work on each binding |
| Ubuntu 3.14 PySide6 `numpy<2.5` | all eight steps pass |
| 6 jobs: Python 3.15 on both OSes, each binding | install fails on h5py as before; nothing else runs |

Fully passing jobs took 2.1 minutes on Ubuntu and 3.4 minutes on Windows. The results
were posted as a comment on each of the five pull requests on 2026-10-17.

**Run 39009717709, the metadata pull requests, `numpy<2.5`.** Refs: zprocess pr/29,
qtutils pr/33, desktop-app pr/31, labscript-c-extensions pr/10, labscript-utils pr/130,
labscript pr/125, runmanager pr/131, blacs pr/125, lyse pr/140, runviewer pr/73,
labscript-devices pr/150, labscript-suite pr/106 (all twelve components from their pull
request heads). Ubuntu and Windows, Python 3.11 and 3.14, PySide6: 4 jobs, all eight
steps pass on each. The components build and install with `requires-python >= 3.11`, the
new version scheme name and no `importlib_metadata` fallback, and the component pins in
labscript-suite pr/106 and runmanager pr/131 resolve to the local builds.

## 2026-10-17: fix branches on the local container, Python 3.14, NumPy 2.5.4

The pull request branches of the release blockers (`MAINTENANCE.md`, "Pull requests
opened by the maintenance track"), merged locally onto each master: labscript
`numpy-2.5-dtype-alias` and `python-3.11-metadata`, labscript-devices and blacs the
same, labscript-utils `fix-28-namespace-packages` and `python-3.11-metadata`, zprocess
`fix-27-setconsolemode` and `python-3.11-metadata`, and `python-3.11-metadata` on lyse,
runmanager, runviewer, labscript-suite, desktop-app and qtutils. Installed into the
Python 3.14.6 venv of the run below (NumPy 2.5.4, h5py 3.16.0, pandas 3.0.6, PySide6
6.12.0) with `uv pip install --no-deps`.

| Platform | Python | NumPy | Result |
|---|---|---|---|
| local container | 3.14.6 | 2.5.4 | all eight steps pass: compile, lyse, runviewer, runmanager-api and apps now pass on NumPy 2.5 (the known B7 and D1 items still show as known) |

Also run, outside the harness:

- labscript-utils #28: a script that imports a module from a namespace package under a
  temporary `userlib`, touches it, waits for `ModuleWatcher` to unload, and imports again.
  master: `KeyError: 'labscriptlib'`. Branch: the import succeeds. A profile created by
  the branch has `labscriptlib/example_apparatus/__init__.py`.
- zprocess #27: `disable_quick_edit` with `os.name` patched to `nt` and a stand-in
  `win32console` whose `SetConsoleMode` raises error 87 returns without registering an
  `atexit` handler. Not run on Windows.
- Version scheme: setuptools_scm 10.0.5 computes `3.5.0.dev41` on labscript-utils master
  with both `release-branch-semver` and `semver-pep440-release-branch`; setuptools_scm
  9.2.2 does not have the new name.
- Every package's `__version__` module imports with `-W error::DeprecationWarning`
  after the `importlib_metadata` fallback removal.

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
