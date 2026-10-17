# Test harness results

Results of running `harness/suite.py` (see `harness/README.md`) on the component default
branches, and the defects that the runs found. Newest first. Each run is identified by
the date, the platform, the Python version and the commits in the report's component
table.

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
