# Plan for the next labscript suite release

Written 2026-10-17 from PR-REVIEW.md (30 open PRs), ISSUE-TRIAGE.md (223 open issues),
the release workflow in rpanderson/workflow-sandbox, the state of PyPI and conda-forge,
and a local install and compile test of the current default branches on Python 3.14 and
3.15. Sections: 1 decision summary, 2 workflow, 3 Python versions and dependencies,
4 work items, 5 release sequence, 6 explicitly deferred.

## 1. Summary

- Support Python 3.11 to 3.15; drop 3.8 to 3.10. The workflow already does this on its
  own because `ci-helper` reads python.org's release cycle; the code and metadata do not.
- The suite does not compile on NumPy 2.5 or newer (released 2026-10-10): every
  compile writes a connection table with the `a256` dtype alias that NumPy 2.5 removed
  (labscript issue #123). With that alias replaced, the current master branches compile a
  shot and read it back in lyse on Python 3.14 with NumPy 2.5.4, pandas 3.0.6, h5py 3.16
  and PySide6 6.12. This is the one release blocker.
- Python 3.15 works for the code, but installs are blocked by third parties: h5py has
  no 3.15 wheels on PyPI, and conda-forge has no 3.15 builds of pyzmq, pyqt or pyqt6.
  Release with 3.15 in the classifiers and the build matrix, say in the release notes
  what is missing, and recommend 3.14.
- Every repo except labscript-c-extensions and desktop-app is one sync behind the
  workflow sandbox (dead `macos-13` label, Node 20 `setup-miniconda@v3`). The sandbox
  itself should move `action-gh-release` to v3 (Node 24) and fix labscript-suite #56
  before the rc-to-final step.
- This is a minor release of every component: labscript 3.5.0, labscript-utils 3.5.0,
  labscript-devices 3.4.0, blacs 3.3.0, lyse 3.4.0, runmanager 3.4.0, runviewer 3.3.0,
  labscript-suite 3.4.0, plus zprocess 2.28.0, desktop-app 0.5.1,
  labscript-c-extensions 1.3.1 and qtutils 4.1.4. The master branches already carry
  these version numbers in their dev builds on the conda test label.

## 2. Build and release workflow (workflow-sandbox)

The canonical workflow is github.com/rpanderson/workflow-sandbox (last change 2026-05-19,
commit 6f9346a). github.com/chrisjbillington/workflow-sandbox is a 2020 fork and is not
used by any repo. Each repo carries a copy of `release.yml` plus a `release-vars.sh`;
the sandbox has a `deploy` script that pushes the workflow to the other repos.

### 2.1 Pinned actions

| Action | Sandbox pin | Runtime | Latest release (2026-10-17) | Notes |
|---|---|---|---|---|
| actions/checkout | v6 | node24 | v7.0.1 (2026-07) | v7 only adds ESM and fork-PR checks; bump is optional |
| actions/setup-python | v6 | node24 | v7.0.0 (2026-07) | v7 removes the `pip-install` input, which the workflow does not use; bump is optional |
| actions/upload-artifact | v6 | node24 | v7.0.2 (2026-10) | v7 adds direct single-file uploads; bump is optional |
| actions/download-artifact | v8 | node24 | v8.0.2 (2026-10) | current |
| conda-incubator/setup-miniconda | v4 | node24 | v4.1.0 (2026-09) | current |
| softprops/action-gh-release | v2 | **node20** | v3.0.3 (2026-08) | v3 is only the Node 24 move; bump to v3 |
| pypa/gh-action-pypi-publish | release/v1 | composite | floating branch | current |

GitHub removed Node 20 from hosted runners on 2026-09-23. Builds on 2026-10-13
(labscript-utils, zprocess) still passed with node20 actions in the workflow, so the
runner is forcing them onto Node 24 rather than failing. That is not something to rely
on: bump `softprops/action-gh-release` to v3 in the sandbox, and the main repos need the
sync below so that `conda-incubator/setup-miniconda` moves from v3 (node20) to v4.

### 2.2 Repos out of sync with the sandbox

| Repo | State vs sandbox |
|---|---|
| labscript-c-extensions, desktop-app | identical to sandbox 6f9346a |
| labscript, labscript-utils, labscript-devices, blacs, lyse, runmanager, runviewer, labscript-suite | synced 2026-03-16/17: still `setup-miniconda@v3` (node20), `windows-latest`, **`macos-13`** (runner retired 2025-12-04), and lack `verbose`/`skip-existing` on the PyPI upload steps |
| zprocess | synced 2026-03-18: `setup-miniconda@v3`, `windows-latest`, has `macos-15-intel` |
| setuptools-conda | own workflow (`build-and-release.yaml`), updated 2026-05-19 |
| qtutils (philipstarkey) | old pins: checkout@v4, setup-python@v5, upload-artifact@v4, download-artifact@v4, setup-miniconda@v3, gh-release@v2 |
| PrawnBlaster, prawn_digital_output | firmware `build.yaml`, separate; not examined for pins beyond noting they are C builds |

`macos-13` matters only when `BUILD_OS_LIST` is `OS_LIST_ALL`, which the configure job
selects when the package is impure or has environment markers. The eight main repos are
pure noarch, so their builds run on Ubuntu only and the dead label is harmless today;
it becomes a failure the moment a platform-specific dependency is added. zprocess and
desktop-app have env markers and build on all four OS labels.

`windows-latest` now resolves to Windows Server 2025 with Visual Studio 2026. The
sandbox pinned `windows-2022` on 2026-05-19 because conda-build still targets VS 2022.
zprocess builds on `windows-latest` and passed on 2026-10-13, so the pin is a precaution
rather than a fix for an observed failure, but the main repos should take it with the
sync.

`macos-15-intel` is the last Intel macOS runner; GitHub retires it in autumn 2027, after
which there are no Intel macOS builds. The suite's packages are noarch so only
labscript-c-extensions and zprocess are affected, and c-extensions wheels for Intel
macOS could then come from cibuildwheel cross-compilation or be dropped.

Recommended workflow actions for the release:

1. In the sandbox: `softprops/action-gh-release@v3`; optionally checkout@v7,
   setup-python@v7, upload-artifact@v7 (no behaviour change for this workflow).
2. Run the sandbox deploy script against the nine lagging repos and qtutils.
3. Fix labscript-suite issue #56 (PKGVER on a commit that carries both an rc and a final
   tag) in the sandbox before the rc-to-final step of this release.

### 2.3 Python versions chosen by the workflow

`ci-helper pythons` reads peps.python.org/api/release-cycle.json and returns every
version whose status is `bugfix` or `security`. As of 2026-10-17 that is 3.11, 3.12,
3.13, 3.14, 3.15 (3.10 is listed as end-of-life since 2026-10-01; 3.15.0 was released
2026-10-09). `ci-helper defaultpython` returns 3.14. `CIBW_BUILD` becomes
`cp311-* ... cp315-*`; cibuildwheel 4.3.1 knows cp315.

Nothing in the workflow pins Python; every repo's `release-vars.sh` leaves
`CONDA_PYTHONS` and `CIBW_BUILD` empty. So the next push already builds for 3.15 and
no longer builds conda packages for 3.10. The zprocess master build of 2026-10-13
produced conda packages for py311 to py315 on all four platforms, and
labscript-c-extensions 1.3.0 (2026-05-20) produced py310 to py314; its next build adds
py315.

## 3. Python versions and dependencies

### 3.1 Supported Python versions

Python status on 2026-10-17 (peps.python.org release-cycle data):

| Version | Status | End of life |
|---|---|---|
| 3.10 | end-of-life | 2026-10-01 |
| 3.11 | security | 2027-10 |
| 3.12 | security | 2028-10 |
| 3.13 | security | 2029-10 |
| 3.14 | bugfix | 2030-10 |
| 3.15 | bugfix (released 2026-10-09) | 2031-10 |

Decision for the release: support 3.11 to 3.15, drop 3.8 to 3.10. This is what the
workflow already builds. Every repo still declares `requires-python = ">=3.8"` and the
docs suggest a Python 3.11 conda environment; both should say 3.11 as the minimum.
Code that exists only for Python < 3.8 and can go: the `importlib_metadata` fallback in
every `__version__.py`, `labscript_utils/versions.py` and `desktop_app/fix_entry_points.py`.
No other version-conditional code remains in the suite. Dropping 3.8 to 3.10 also allows
`match`, `tomllib`, `ExceptionGroup` and PEP 604 unions in new code, but no existing
code needs changing for the bump.

### 3.2 What works on 3.14 and 3.15 today

A local smoke test installed the current default branches of zprocess, qtutils 4.1.3
(PyPI wheel), desktop-app, labscript-c-extensions, labscript-utils, labscript,
runmanager (upstream master including the #130 refactor), blacs, lyse, runviewer,
labscript-devices and labscript-suite into fresh virtual environments.

Python 3.14 with numpy 2.5.4, h5py 3.16.0, pandas 3.0.6, scipy 1.18.1, pyzmq 27.2.0,
PySide6 6.12.0: every package installs and every top-level module imports with
`-W error::DeprecationWarning`, including the Qt-dependent modules under an offscreen
platform plugin. labscript-c-extensions compiles against numpy 2.5 and Cython from
source. (Results of the zprocess test suite and an end-to-end compile of the default
profile's example experiment are in section 3.4.)

Python 3.15: zprocess, qtutils and desktop-app install and import. labscript-utils and
everything above it cannot be installed from PyPI, because **h5py 3.16.0 (2026-03) ships
no cp315 wheels** and building it from source needs Cython and HDF5 headers. numpy,
scipy, pandas, matplotlib, pillow, pyzmq (abi3), pywin32 and PySide6 (abi3) all have
3.15 wheels. So on pip, 3.15 support waits on the next h5py release; PyQt5 and PyQt6 are
abi3 and already work. psutil is not a suite dependency.

### 3.3 Conda

The suite's conda packages come from the labscript-suite channel on anaconda.org, built
with setuptools-conda on top of conda-forge (miniforge). All eight suite packages plus
qtutils are noarch and install on any Python for which their dependencies resolve.
zprocess and labscript-c-extensions are built per Python version.

conda-forge availability on 2026-10-17 for the dependencies that have compiled builds:

| Package | py311 | py312 | py313 | py314 | py315 |
|---|---|---|---|---|---|
| numpy 2.5.4 | yes | yes | yes | yes | yes |
| h5py 3.16.0 | yes | yes | yes | yes | yes |
| scipy 1.18.1 | yes | yes | yes | yes | yes |
| pandas 3.1.0rc0 / 3.0.x | yes | yes | yes | yes | yes |
| matplotlib 3.11.2 | yes | yes | yes | yes | yes |
| pyside6 6.11.2 | yes | yes | yes | yes | yes |
| pyqt 5.15.11 | yes | yes | yes | yes | **no** |
| pyqt6 6.11.0 | 6.8.1 | yes | yes | yes | **no** |
| **pyzmq 27.2.0** | yes | yes | yes | yes | **no** |
| pywin32 312 | yes | yes | yes | yes | yes |

pyqtgraph, qtpy, pyserial, tzlocal are noarch. The conda-forge Python 3.15 migration
started with 3.15.0rc1 in September 2026 and the full compiled-package rebuild had not
started as of the conda-forge announcement; pyzmq and the Qt bindings are the holdouts
that matter here.

Consequences:

- The labscript-suite channel already has a zprocess 2.28.0.dev4 build for py315 on all
  four platforms (2026-10-13); the build succeeded because conda-build only needs
  python, setuptools and setuptools_scm at build time. That package is not installable
  on conda until conda-forge has a py315 pyzmq. This is the "hold back" edge case: the
  package builds, the solver cannot install it. Nothing breaks in CI, so there is no
  need to set `CONDA_PYTHONS` to exclude 3.15; the py315 packages simply become usable
  when pyzmq lands.
- conda users on 3.15 also need pyside6 (available) rather than pyqt (not available).
- labscript-c-extensions 1.3.0 has py310 to py314 conda packages; the next tag adds
  py315 and drops py310 automatically.
- A dev build of the 3.3.0 blacs and 3.5.0 labscript noarch packages is uploaded to the
  channel's test label on every push to master, so the channel is exercised.

Recommendation: release for 3.11 to 3.15 on PyPI and conda, state in the release notes
that on conda 3.15 requires conda-forge's pyzmq and that PyQt5 is unavailable for 3.15
on conda, and on pip that 3.15 waits on an h5py release with cp315 wheels. Do not hold
the release for either; 3.14 is the version to recommend in the docs.

### 3.4 Qt bindings

The 2026 commits made blacs, lyse, runviewer and labscript-utils run on PyQt5, PyQt6 and
PySide6 through qtutils 4.1.x (philipstarkey/qtutils; the chrisjbillington fork is
unmaintained since 2021). The installation docs still say `pip install PyQt5` and the
`docs` extras still pull PyQt5. PyQt5 is abi3 and works on 3.15, but it is in
maintenance only, and conda-forge has no py315 build. The release should document
PySide6 as the recommended binding (it has wheels and conda packages for every supported
Python) and keep PyQt5 as supported.

### 3.5 Smoke-test results (Python 3.14, 2026-10-17)

| Check | Result |
|---|---|
| Install all packages from local clones, PySide6 6.12, numpy 2.5.4, h5py 3.16.0, pandas 3.0.6, scipy 1.18.1, pyzmq 27.2.0 | OK |
| Import every top-level module and the Qt-dependent modules with `-W error::DeprecationWarning` | OK |
| labscript-c-extensions build from source with Cython against numpy 2.5 | OK |
| zprocess test suite (`tests/`) | 73 passed in 110 s |
| Compile the default profile's `example_experiment.py` via `runmanager.compiler` and `labscript` in-process | **fails** with `TypeError: data type 'a256' not understood` in `save_time_markers` and `generate_connection_table` |
| Same compile with `a256` replaced by `S256` in the installed copy | OK; shot has 6 connection-table rows, two devices, time markers |
| `lyse.Run` and `get_dataframe_from_shot` on that shot (pandas 3.0) | OK, 9 columns |

The `a` alias was deprecated in NumPy 2.0 (warning) and removed in 2.5. NumPy 2.4 still
accepts it, so users who have not updated NumPy this month do not see the failure yet.
`S256` produces the same on-disk dtype, so shot files are unchanged. The setuptools_scm
10 warning that `release-branch-semver` was renamed `semver-pep440-release-branch` also
appeared; every repo's pyproject uses the old name.

## 4. Work items

Ordered by priority. "Issue" and "PR" numbers refer to ISSUE-TRIAGE.md and PR-REVIEW.md,
which give file:line and the reasoning.

### 4.1 Blockers (release cannot ship without these)

1. **NumPy 2.5 `a` dtype alias** (labscript #123). Replace `a256`, `a2` and `'a'+str(n)`
   with the `S` alias in: labscript `labscript.py:216,268,477`, `outputs.py:1604`;
   labscript-devices `Camera.py:107`, `AlazarTechBoard.py:157-158`,
   `CiceroOpalKellyXEM3001.py:652`, `NI_DAQmx/labscript_devices.py:514-520`,
   `NI_DAQmx/blacs_workers.py:956`, `PrawnBlaster/blacs_workers.py:497`; blacs
   `front_panel_settings.py:348,387` (BLACS cannot save front-panel settings on NumPy
   2.5 either). Also `LightCrafterDMD.py:348,359` `ndarray.tostring()` (removed in
   NumPy 2). The `np.string_` fixes for the cameras are already on master, unreleased.
   Status 2026-10-17: done. labscript #124, labscript-devices #149 and blacs #124
   merged; labscript #123 closed.
2. **zprocess #27**: `SetConsoleMode` crash on Windows 11 when any suite program is
   restarted from Windows Terminal or VS Code. Two lines in `zprocess/utils.py:190`.
   Needs zprocess 2.28.0, which also carries the heartbeat changes merged in 2026.
   Status 2026-10-17: done. zprocess #28 merged and the issue closed; the branch was
   tested on Windows 11 with BLACS restarted from PowerShell in Windows Terminal and
   from cmd.exe (`TESTING.md`). zprocess 2.28.0 is step 1 of the release sequence.
3. **labscript-utils #28**: compile crash `KeyError: 'labscriptlib'` after editing a
   file, because `labscript-profile-create` lays out `example_apparatus` as a namespace
   package and ModuleWatcher unloads its parent. Ship `__init__.py` in the default
   profile and stop whitelisting namespace packages under userlib.
   Status 2026-10-17: labscript-utils #129 merged (c023465); issue closed.
4. **labscript-suite #56**: the release workflow computes `PKGVER` from a commit that
   carries both an rc and a final tag. Fix in the sandbox and deploy before tagging.
   Status 2026-10-17: workflow-sandbox #46 merged (e3fb720); issue closed. The step was tested in this
   repository's `tag-test.yml` on branch `claude/release-tag-test`, locally with
   setuptools_scm, and with real tag pushes to the chrisjbillington fork of the sandbox:
   an rc tag, then the final tag on the same commit, then a branch push built
   0.6.0rc2, 0.6.0 and 0.7.0.dev70 (`TESTING.md`).
5. **Workflow sync** (section 2): deploy the sandbox to the nine lagging repos and
   qtutils; bump `action-gh-release` to v3 in the sandbox first.
   Status 2026-10-17: sync PRs merged on all twelve repos, from the head of sandbox #46
   (table in `PULL-REQUESTS.md`). Done.
6. **Metadata**: `requires-python = ">=3.11"` and matching classifiers in every repo;
   component pins in labscript-suite and runmanager pyproject raised to the new
   versions; `version_scheme = "semver-pep440-release-branch"`; delete the
   `importlib_metadata` fallbacks (every `__version__.py`, `labscript_utils/versions.py`,
   `desktop_app/fix_entry_points.py`).
   Status 2026-10-17: merged on ten repos (table in `PULL-REQUESTS.md`). The scheme
   rename needs `setuptools_scm>=10`, which conda-forge has.
   runmanager #131 and labscript-suite #106 are held until the release sequence
   (section 5) because they raise the component pins to versions that are not released
   yet: `labscript>=3.5.0rc1` and `labscript_utils>=3.5.0rc1` in runmanager, the seven
   component pins in labscript-suite. A master checkout builds as a development version
   such as 3.5.0.devN, which is lower than 3.5.0rc1, so after a merge a source install
   of runmanager or labscript-suite fails to resolve its dependencies until the pinned
   release candidates are on PyPI. Merge each of the two immediately before its own rc
   tag, after the pinned components have release candidates.

### 4.2 Bugs worth fixing in this release (importance 4, all small)

- blacs #46 and #29: shot-file cleanup in `experiment_queue.py:808-821, 926-947` runs
  outside any `try`, so an I/O error kills the queue thread until BLACS restarts. Fixed
  on the blacs branch `queue-robustness-and-window-geometry` (2026-10-18) with #52, #56,
  defect D1 and the #123 comment trim; blacs #128 merged 2026-10-18.
- blacs #52 and #56: window geometry restored by `move()/resize()` arithmetic with no
  screen check; reproduced again in 2026-01. Use `saveGeometry/restoreGeometry` and clamp.
- desktop-app #20: `desktop_app/windows.py` imports pywin32 in the launcher before the
  environment is activated; make the imports lazy (desktop-app 0.5.1). desktop-app #34 merged 2026-10-17.
- zprocess #19 and #16: call `zmq.has('curve')` before CURVE APIs and raise a readable
  error; document that conda users need conda-forge's pyzmq. Fixed in zprocess #32 (merged
  2026-10-18); the install-docs note is still to do. #19 is closed; #16 is left open.
- blacs #100: `setup_logging.py:60,73` crash when `sys.stdout` is `None` (pythonw). Fixed
  in labscript-utils #133 (merged 2026-10-18), which also carries REVIEW.md items 10 and 18,
  DEFECTS.md D3 and labscript-utils #60.
- labscript-devices #109: PrawnBlaster runviewer parser drops the instruction after a
  wait; one-line fix at `PrawnBlaster/runviewer_parsers.py:104`. Fixed on the
  labscript-devices branch `prawnblaster-and-esrpro500-fixes` (2026-10-18) with #79,
  labscript #95 and defect D9; labscript-devices #153 merged 2026-10-18.
- labscript-devices #79: ESRPro500 has no runviewer parser and exposes 21 of 24 flags;
  two users report no output without the extra flags.
- labscript #52: duplicate `connection` on one parent is silent (`base.py:345-359`).
- labscript #43: clock-collision errors name clocklines and times but not the outputs.
  Fixed for #52, #43 and #16 in labscript #128 (merged 2026-10-18), which also carries REVIEW.md
  items 6, 7 and 8 and most of the labscript Part 2 bugs.
- labscript #95: PrawnBlaster `half_period` overflow for idle clocklines longer than
  about 42 s now truncates silently under NumPy 2; add a range check in labscript-devices.
  Range check in labscript-devices #153 (merged 2026-10-18).
- labscript #104: `from pylab import *` in `labscript.py:46` and `functions.py:17`;
  the docs build already pins `numpy<2` because of it. Maintainer decision 2026-10-18:
  remove the star import with no re-exports, and list the change in section 4.6.
  Fixed in labscript #130 (opened 2026-10-18).
- runmanager #66: preparse materialises the full outer product to count shots; compute
  the count from axis lengths. Fixed in runmanager #134 (merged 2026-10-18).
- runmanager #123: `remote.set_globals(raw=True)` appends the previous comment; the
  reporter offered a PR. Fixed on the runmanager branch `compile-loop-and-remote-fixes`
  (2026-10-18) with #66, #33, #30, #26 and defect D2; runmanager #134 merged 2026-10-18.
- runmanager #33, #30, #26; blacs #49, #32, #7, #72; lyse #14, #90, #139; runviewer
  #13 (in labscript-c-extensions, which is rebuilt for 3.15 anyway); labscript #16;
  labscript-utils #60; labscript-suite #5, #59, #60: each under an hour, see the triage.
  Status 2026-10-18: all fixed and merged except labscript-suite #60, which is not
  started: lyse #14, #90 and #139 in lyse #145; runviewer #13 in labscript-c-extensions
  #13 (merged 2026-10-17); labscript #16 in labscript #128; labscript-utils #60 in
  labscript-utils #133; blacs #49, #32, #7 and #72 in blacs #129; labscript-suite #5 in
  labscript-utils #134 and labscript-suite #109; labscript-suite #59 in labscript-suite
  #109. The issues are closed.
- Ending a busy subprocess safely (lyse Restart and Remove, runmanager Restart
  subprocess, BLACS tab close): the kill lock has no effect on Windows and the
  SIGTERM stage is useless on every platform (`DEFECTS.md` D18). The design and status
  are in `SUBPROCESS-INTERRUPTION.md`; the zprocess part goes into 2.28.0, the lyse part
  follows lyse #151 and #153.
- labscript #41: there are no tests in labscript or labscript-utils. The harness in
  this repository (`harness/`, results in `TESTING.md`) runs install, import, compile,
  lyse, runviewer-parser, runmanager-API and application start-up checks on Ubuntu and
  Windows for Python 3.11 to 3.15 and reproduces #123; what remains is deploying a copy
  of it to the component repos' CI before tagging.

### 4.3 Pull requests to merge in this release

From PR-REVIEW.md, in order: blacs #123 (plugin crash; merged 2026-10-17 as d061535,
with a five-line comment trim to carry in the next blacs pull request), labscript-devices #110
(Windfreak), #126 (AD9959, after the dead parser is removed), lyse #132 (after the
overwrite fix), labscript-utils #117 (after the `save_result` fix), labscript-devices
#87 and #63 (one guard each), #144 (after the author fixes the SyntaxError, model string
and semaphore), prawn_digital_output #23 (notebook outputs stripped). PrawnBlaster #37
and #35 are firmware and need the matching host changes in labscript-devices
(`PrawnBlaster/labscript_devices.py:150,239`, `blacs_workers.py:137-151`) in the same
labscript-devices release if they go in.
Status 2026-10-17: labscript-devices #110 and lyse #132 merged. Maintainer fix commits
for labscript-utils #117, labscript-devices #126, #144, #87 and #63 and
prawn_digital_output #23 are in `patches/` with rows in `LOCAL-TASKS.md` to push each to
its pull request branch, dispatch the test workflow with the pull request refs and merge
(`TESTING.md`, "fixes for the remaining release pull requests").
Status 2026-10-18: all six are merged. The fix commits were pushed to the pull request
branches and labscript-utils #117, labscript-devices #126, #144, #87 and #63 and
prawn_digital_output #23 were merged on 2026-10-17 (`LOCAL-TASKS.md` has the merge
commits). The blacs #123 comment trim went into blacs #128, merged 2026-10-18, and
`patches/` is empty. PrawnBlaster #37 and #35
are not prepared: both need firmware changes tested on hardware and a host-side change,
and neither blocks the release.

The runmanager refactor (#130) was merged on 2026-10-17 as bfe63ba, including the fix
commit 7c50b46 for the regressions found in review (see MAINTENANCE.md). Merging #130
means runmanager 3.4.0 is a larger change than the other packages; test the GUI, remote
API and BLACS submission paths specifically.

### 4.4 Housekeeping

- Close the dead PRs (lyse #118 and #85, blacs #89, desktop-app #6, pineblasterv2 #1,
  setuptools-conda #5) and the roughly 95 issues marked close in ISSUE-TRIAGE.md, each
  with the one-line reason from the triage. The author closed blacs #121 on 2026-10-16.
- Docs: minimum Python 3.11, PySide6 as the recommended binding with PyQt5 and PyQt6
  supported, the `git` note (labscript-suite #59) and apparatus-name rules (#5), both in
  labscript-suite #109 (merged 2026-10-18),
  CITATION.cff in component repos (#60, left open and not for this release by
  maintainer decision 2026-10-18); delete `blacs/docs/UsingBLACS.*` and
  `docs/How to add a new device` (blacs #19).
- Release notes per package with contributors (labscript-suite #21 checklist); the
  Qt6/PySide6 work of 2025-12 to 2026-03 and the runmanager refactor are the headline
  items alongside Python 3.11 to 3.15 and NumPy 2.5.

### 4.5 Tests before tagging

- The smoke test of section 3.5 on 3.11, 3.12, 3.13, 3.14 (pip, PySide6) and on 3.15
  once h5py ships cp315 wheels.
- Conda install of the test-label packages into a fresh miniforge env on 3.14 with
  pyside6, on Windows and Linux.
- GUI launch of blacs, lyse, runmanager and runviewer under PySide6, PyQt6 and PyQt5
  (blacs #57 and #97 concern launch-time rendering).
- The Windows restart path (compile-and-restart in BLACS, zprocess #27) from Windows
  Terminal. Done 2026-10-17 on the zprocess #28 branch (`TESTING.md`); repeat on the
  released zprocess.
- A real shot on hardware in at least one lab from the rc packages before the final tag.

### 4.6 Breaking changes for the release notes

The release notes of each package list these first, above the other changes. Add to
this list any change that makes a script, connection table, globals file or labconfig
that worked with the previous release fail or behave differently.

- Python 3.11 is the minimum supported version.
- labscript: `from labscript import *` no longer provides the numpy and matplotlib names
  of `from pylab import *` (labscript #104, fixed in labscript #130). Scripts must import
  numpy themselves.
- labscript: a secondary pseudoclock that shares its trigger line with a device that has
  different triggers is a compile error (labscript #130).
- labscript: duplicate connections on one parent, outputs commanded too soon before a
  trigger and collisions inside ramps are now compile errors (labscript #128).
- labscript-utils: `labscript-profile-create` rejects an apparatus name that is not a
  Python identifier (labscript-utils #134).
- labscript-devices: a PrawnBlaster clockline that is idle for longer than the maximum
  half period, or a wait timeout above the maximum, is now a compile error instead of a
  wrapped value (labscript-devices #153, #155). The PulseBlasterESRPro500 exposes 24
  flags instead of 21 (#153).
- runmanager: `remote.set_globals(raw=True)` no longer appends the previous comment
  (runmanager #134). A zip group with globals of unequal lengths is an error instead of
  being truncated to the shortest (runmanager #137).
- blacs: with no saved settings, analysis submission is enabled with lyse host
  `localhost` (blacs #129). Closing BLACS during a shot aborts the shot and puts it back
  at the top of the queue (blacs #131).

### 4.7 Changes that need testing on hardware

These changes are merged and were tested only by reading the code, by compiling shots
with them, or with simulated devices. The release-candidate notes ask users with this
hardware to test them and report the result; a checklist for testers can be made from
this list.

- NI_DAQmx: the final analog input read in `stop_task()` (labscript-devices #154).
- PrawnBlaster: `clock_limit` with a clock frequency other than the default; the wait
  without the internal wait monitor and as a secondary pseudoclock; the range checks and
  `uint32` pulse program (labscript-devices #153, #154, #155).
- PrawnDO: wait insertion with several waits; `clock_limit`; the interval range check
  and the `set_initial_trigger_time` check (labscript-devices #154, #155).
- PulseBlasterESRPro500: output on flags 21 to 23 with short-pulse firmware
  (labscript-devices #153). PulseBlaster ESR-PRO direct outputs with edges closer than
  120 ns (`clock_limit`, #155).
- PhaseMatrixQuickSyn: the `OUTP:STAT 1` command now has its terminator, so the gate
  command in `transition_to_buffered` is executed (#155).
- PylonCamera grab errors; IMAQdxCamera attribute dialog Copy button (#155).
- RFBlaster retry on `requests` exceptions; PineBlaster runviewer trigger delay (#155).
- The contributor pull requests merged without a hardware test: AD9959 DDS sweeper
  worker (labscript-devices #126), Andor (#144), IMAQdx background subtraction (#87) and
  view range restore (#63), Windfreak (#110).
- BLACS queue error handling and window geometry (blacs #128, #129), which were run with
  simulated device tabs only, and a real shot in at least one lab (section 4.5).

### 4.8 zprocess 3

The maintainer plans a zprocess 3 release. These zprocess pull requests are intended for
it:

- zprocess #39: no default `ProcessTree` is created on import. `Event`, `Process` and
  `subprocess_with_queues()` without a tree raise `RuntimeError` until
  `set_default_process_tree()` is called. Code outside the suite that uses them in a
  top-level process without setting a default breaks, so this goes in the release notes.
- zprocess #37: `start_daemon` raises `CalledProcessError` if the command cannot be
  started, instead of returning silently.
- zprocess #38: on macOS, App Nap is disabled in every process that creates a
  `ProcessTree`.

The goal is that zprocess 3 breaks compatibility for code outside the suite, but not for
the suite: neither for the release set that requires zprocess 3 nor for an install of
earlier 3.x releases in which zprocess, or labscript-utils with zprocess, is upgraded on
its own. A name that a 3.x release of a component uses therefore stays in zprocess 3 as a
shim, and is removed in a later major version, some time after the suite has stopped
using it. The review of 2026-10-23 (zprocess master 1de4c26, the component default
branches, and every 3.x release tag of labscript-utils, blacs, lyse, runmanager,
runviewer, labscript-devices and labscript) gives the items below. Line numbers are for
zprocess master 1de4c26. The status of each item is "agreed" (the maintainer accepted
it), "proposed" (not yet decided) or "withdrawn".

| # | Change in zprocess 3 | Users found | Change needed in the suite | Status |
|---|---|---|---|---|
| Z1 | Remove the module-level zlock functions and the `Lock` wrapper that uses `_default_zlock_client` (`zlock/__init__.py:231-303`) | none. labscript-utils `ls_zprocess.py:158` (master and the 3.x releases) assigns `_default_zlock_client`; the assignment is harmless after the removal | delete the assignment in labscript-utils #138 | agreed |
| Z2 | Remove the module-level zlog functions and the `ZMQLoggingHandler` wrapper (`zlog/__init__.py:184-230`) | none | none | agreed |
| Z3 | Remove the `ZMQServer.setup_auth` hook (`clientserver.py:86-94`, `142`). A subclass that defines `setup_auth(context)` in its own class body gets a plain `zmq.Context` instead of a `SecureContext`; zprocess calls the hook with that context so that the subclass can configure its own authentication, and ignores `shared_secret` and `allow_insecure`. It dates from zprocess 2.4.1 (848cb04, 2018) | none in the suite or in its history | none | agreed |
| Z4 | Keep, as a shim, the `ZMQServer` subclass (`clientserver.py:440-460`) that accepts `type=` for `dtype=` and defaults to `allow_insecure=True`; remove it in a later major version | labscript-utils `camera_server.py:76` (`type='string'`) in every 3.x release. Its user is the legacy `labscript_devices/imaqdx_server.py`, the server for the "use zmq" option of `labscript_devices/Camera.py` (REVIEW.md C2). The device works with current code (`TESTING.md`, 2026-10-23) | `camera_server.py`: `dtype='string', allow_insecure=True`, which keeps the server's behaviour | proposed |
| Z5 | Create the insecure default `ZMQClient` of `zmq_get*` and `zmq_push*` on first use instead of on import (`clientserver.py:464`), and keep its behaviour; replace it with a client that must be set (`set_default_client()`) in a later major version | `labscript_devices/Camera.py` (`zmq_get_string`, 6 calls) in every 3.x release, against the insecure camera server of Z4. Outside the suite, the BEC2 experiment control of the University of Trento sends shot files to BLACS and runviewer with `zprocess.zmq_get` (github.com/jack00look/BEC2_exp_control_3_wayback_machine, `libraries/system.py:516`) | `Camera.py` uses its own `zprocess.ZMQClient(allow_insecure=True)`. labscript-utils does not set a default client: a released `Camera.py` would then use CURVE when the lab has a shared secret, and the camera server does not | proposed |
| Z6 | Remove `setup_connection_with_parent()` and `subprocess_with_queues()` (`process_tree.py:1552-1575`) | none in the suite; on GitHub only labscript-suite/mise (last push 2020) and an old lyse fork | none | agreed |
| Z7 | Remove `embed()` (`utils.py:201`), which raises `NotImplementedError` | none | none | agreed |
| Z8 | Keep `Event` and `Process` without a `ProcessTree` (they use the default tree) and the `type=` keyword of `Event` (`process_tree.py:1519-1550`) | blacs `Worker` subclasses `zprocess.Process`; NI_DAQmx, PrawnBlaster and CiceroOpalKellyXEM3001 call `Event(..., type='post')` without a tree; labscript-utils `qtwidgets/InputPlotWindow.py` subclasses `zprocess.Process` | change the three devices to `role=` | agreed |
| Z9 | Keep `zprocess.locking` (`locking/__init__.py:1` says it will be removed in zprocess 3) as a shim; remove it in a later major version | `blacs/__main__.py:60` imports it in master and every 3.x release and does not use it | delete the import in blacs | agreed |
| Z10 | Default `allow_insecure` to `False` in the zlock, zlog and remote server command lines (`zlock/__main__.py:129`, `zlog/__main__.py:173`, `remote/__main__.py:38`, planned since 6b11198), in `ZLockClient`, `ZLogClient` and the three server classes | none: labscript-utils `zlock.py`, `zlog.py` and `remote.py` pass the option explicitly in every tag since 3.0.0b1, and `ProcessTree` passes it to its clients | none | proposed |
| Z11 | `PICKLE_PROTOCOL` 4 to 5 (`__init__.py:3`). Protocol 5 is the highest protocol on Python 3.11 to 3.15 (run on 3.12, 3.13, 3.14 and 3.15) and is read by Python 3.8 and later, so a peer with an older zprocess on Python 3.8 or later still unpickles the messages | n.a. | none | agreed |
| Z12 | `ProcessTree.connect_to_parent()` sets the tree as the default. With #39 only `Process._run()` and `setup_connection_with_parent()` set it, so in a child that calls `connect_to_parent()` itself (the runmanager batch compiler, the lyse analysis subprocess) `Event` without a tree raises `RuntimeError`. A `Process` child runs `process_class_wrapper.py`, which calls `connect_to_parent()`, creates the `Process` instance with that tree and calls `_run()`; the override of `_run()` in the `Process` shim (`process_tree.py:1546`) only sets the default and is then removed | n.a. | none | proposed |
| Z13 | Remove `setuptools_scm` from the runtime dependencies. In a git checkout (an editable install) `__version__.py` uses it to give the version of the checked-out commit; the suite gets it through labscript-utils in any case | n.a. | none | withdrawn |

Besides the names above, the 3.x releases use these internals, which zprocess 3 keeps:
`zprocess.process_tree._default_process_tree`, which labscript-utils assigns (#39 keeps
the name, and `get_default_process_tree()` reads it), and `zprocess.utils._reraise`,
which labscript-devices `NI_DAQmx/blacs_workers.py:26` imports and calls wrongly
(`DEFECTS.md` D24; the fix stops the import). The changes in the suite go into the 3.5.0
release set, before zprocess 3 is released.

When zprocess 3 is released, the labscript suite's dependency on zprocess must be raised
to it:

- labscript-utils #138 calls `zprocess.set_default_process_tree()`, which only zprocess 3
  has. Amend it to raise `zprocess>=2.18.0` in `pyproject.toml` to zprocess 3, then
  merge it.
- The other components pin zprocess at `>=2.14.1` (blacs), `>=2.2.2` (lyse),
  `>=2.18.0` (labscript-devices), or not at all (runviewer). They work with zprocess 3
  through labscript-utils, so their pins do not need to change, but they can be raised
  with labscript-utils to keep the pins consistent.

## 5. Release sequence

Dependency order. Each is tagged on a `maintenance/x.y.x` branch per the release flow
(zprocess releases from `master`):

| Step | Package | Version | Carries |
|---|---|---|---|
| 1 | zprocess | 2.28.0 | #27, #19, heartbeat changes, PAIR sockets (#33, maintainer's decision 2026-10-19; merged 2026-10-23 as 1ec60ed, so a new release candidate is needed). Tagged from `master`: `v2.28.0rc1` at e74b638 on 2026-10-17 is on PyPI but has no win-64 conda packages (defect D7, `DEFECTS.md`); `v2.28.0rc2` at f5f4685, which carries the D7 fix (#31), is on PyPI and on the Anaconda main label for all four platforms (run 39029064804). The `maintenance/2.28.x` branch that was pushed for rc1 is deleted; zprocess does not use maintenance branches |
| 2 | qtutils (philipstarkey) | 4.1.4 | #22 RTD version, optional "Clear output" part of PR #32. qtutils #37 (#22) and #36 (clear output, closes #2) merged 2026-10-17; qtutils #39 (16 px icons, DEFECTS.md D11), #40 (PyQt6 `exec_()` alias only) and #41 (auto scroll to end across hiding and showing, runmanager #32) merged 2026-10-23; not tagged |
| 3 | desktop-app | 0.5.1 | #20 lazy pywin32. desktop-app #34 merged 2026-10-17; not tagged. desktop-app #35 (the entry point launcher loses the venv on macOS, DEFECTS.md D19), open |
| 4 | labscript-c-extensions | 1.3.1 | runviewer #13 resampler fix (PR #13, also fixes REVIEW.md item 19, merged 2026-10-17 as b0f985d); py311 to py315 wheels come from the metadata (#10) and workflow (#11) merges; the `master` run on b0f985d builds them (`TESTING.md`) |
| 5 | labscript-utils | 3.5.0 | #28, #100, #60, PR #117, Qt6 work; PRs #136 (D12), #137 (D21) and #139 (`get_shot_globals` with an open file), merged 2026-10-23 |
| 6 | labscript | 3.5.0 | #123, #52, #43, #104, #16 |
| 7 | runmanager | 3.4.0 | #130 refactor plus fixes, #66, #123, #33, #30, #26; PRs #137 and #138 (merged 2026-10-21), #139 (topological evaluator), #140 (custom and automatic expansion settings), #141 (D11), #142 (D12) and #143 (D28), merged 2026-10-23 |
| 8 | blacs | 3.3.0 | PR #123, #46, #52, #100, front-panel dtype, Qt6 work; PRs #131 (REVIEW.md B3), #132 (non-blocking state display), #133 (D12) and #134 (D32, D33), merged 2026-10-23 |
| 9 | lyse | 3.4.0 | PR #132, #14, #90, #139, Qt6 work; PRs #148 (D12), #149, #150 (D13, D25), #152 (D16), #154 (D17), #155 (D29) and #156 (D34), merged 2026-10-23; Abort button (PR #153) |
| 10 | runviewer | 3.3.0 | Qt6 work, c-extensions pin; PRs #78 and #79 (D12), merged 2026-10-23 |
| 11 | labscript-devices | 3.4.0 | dtype fixes, #109, #79, #95, PRs #110, #126, #87, #63, #144; PRs #156 (D12), #157 (DummyIntermediateDevice runviewer parser), #158 (D30, D31) and #159 (FunctionRunner opens the shot file once), merged 2026-10-23 |
| 12 | labscript-suite | 3.4.0 | pins, docs, `requires-python` |

The component pins in runmanager (step 7) and labscript-suite (step 12) are raised by
runmanager #131 and labscript-suite #106, which are merged at their step and not
before (section 4.1 item 6). The pins are of the form `>=3.5.0rc1`, so that the release
candidates of runmanager and labscript-suite install with the release candidates of
the packages they pin; a `>=3.5.0` pin would be satisfied by neither a development
version nor a release candidate. The rc1 form is kept in the final release: pip does
not select a release candidate once a final release exists, so the looser pin changes
nothing for users, and one commit can carry both the rc and the final tag.

blacs #133, lyse #148, runmanager #142 and runviewer #79 (DEFECTS.md D12) make blacs,
lyse, runmanager and runviewer call `labscript_utils.excepthook.install()`, which is new in labscript-utils
3.5.0. They were merged on 2026-10-23, so the `labscript_utils` pins of those four and of
labscript-devices are raised to `>=3.5.0rc1` at their steps, in the same way. lyse #156
and labscript-devices #159, also merged, call `get_shot_globals` with an open file, which
labscript-utils #139 adds for 3.5.0.

No tag is pushed until the whole release set is ready (maintainer's decision,
2026-10-18); the sequence above is the order of the tags on that day, and only zprocess
has release candidates on PyPI. Until then, testing uses two things that need no tag:
every push to `master` or a `maintenance/*` branch runs `release.yml`, which builds the
sdist, wheels and conda packages as a development version and uploads them to Test PyPI
and the Anaconda `test` label; and the harness workflow in this repository installs any
mix of branches, commits and `pr/N` refs (`harness/README.md`). A change is checked by
merging it and reading its `release.yml` run, or by a harness dispatch with its ref.

Conda packages for steps 1 and 4 are built per Python (3.11 to 3.15); the rest are
noarch. Nothing needs `CONDA_PYTHONS` set: the py315 packages build now and become
installable when conda-forge ships pyzmq for 3.15.

### 5.1 Maintenance branches and patch releases

Each minor release of an application repository is tagged on its `maintenance/x.y.x`
branch, which is created from `master` at the release candidate. The release workflow
builds development versions on these branches with a patch bump and on `master` with a
minor bump, so the branch is needed even when no patch release follows. zprocess,
qtutils and desktop-app tag from `master` and have no maintenance branches.

Only the newest minor release of each package is maintained. A bug fix is merged to
`master`, cherry-picked to the current maintenance branch and tagged there as a patch
release (x.y.1, x.y.2, ...). No change goes to a maintenance branch that is not on
`master`, and no feature, dependency change or workflow change is picked. The maintenance
branches of earlier minors (3.3.x and 3.4.x at the time of writing) are not updated.

This is the model that the labscript-suite contributing guide describes
(`docs/source/project/contributing_guide.md`, "Branching model"). The existing patch
releases are not a precedent to copy: each "Squashed commit of the following" on a
maintenance branch is a squash merge of the whole of `master`. After this release
`master` carries changes that must not ship as patches (labscript-devices #148,
section 6).

## 6. Deferred, with the reason

- zprocess #14 (PAIR sockets): correct idea, but it breaks mixed-version remote workers
  with no clear error; needs the version check (blacs #54) and a decision on how to
  break compatibility. Done 2026-10-19 as zprocess #33: the socket type is negotiated
  through the parent info and the remote process server's protocol version, so no
  compatibility is broken and blacs #54 is not needed for it. The maintainer decided on
  2026-10-19 that it goes into 2.28.0 (section 5, step 1). #33 was merged and #14 closed on
  2026-10-23.
- labscript-devices #148 (TriggerableCamera and DummyCamera): the right structure, but
  removes the `mock` kwarg from every connection table and needs hardware testing;
  schedule for labscript-devices 3.5.0 with #106 rebased on top.
- runmanager #104 and blacs #90 (compilation queue): superseded by the refactor;
  reopen as a requirements issue.
- lyse Run-to-Shot rename, blacs #88 (lock monitor), #105 (virtual devices, pending
  author fixes), the Stahl and Keysight devices: see PR-REVIEW.md.
- macOS application behaviour, from closed pull requests by ispielma: the Fusion Qt
  style instead of the native macOS style, dock icons, and the Qt application name
  from a string that the application passes to `Splash` instead of from `argv[0]`
  (labscript-utils #124, `labscript_utils/splash.py`); `short_display_name` in each
  application's `desktop-app.json` and the application name passed to the splash
  screen (blacs #122, runmanager #129, runviewer #72, lyse #138). The author closed
  all of them on 2026-10-13 and 2026-10-15 without comment. The desktop-app side
  (desktop-app #29, `.app` bundles, `short_display_name` read at
  `desktop_app/shell.py:65`) is merged. Fusion is more consistent across platforms,
  and we may adopt it if the problems that it causes can be fixed. Probably not in this
  release, but to be reconsidered.
- Free-threaded Python builds (setuptools-conda #26) and Intel macOS after the
  `macos-15-intel` runner retires in 2027.
- Lower the scheduling priority of the lyse analysis subprocess, so that analysis
  routines do not slow BLACS when both run on one machine. A nice-to-have, not
  scheduled. The maintainer's lab machine runs `os.nice(10)` at the top of
  `lyse/analysis_subprocess.py`; a mainline version needs a Windows equivalent (`os.nice`
  does not exist there) and probably a labconfig setting instead of a fixed value.
