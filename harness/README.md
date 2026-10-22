# Test harness

End-to-end tests of the labscript suite through its public entry points. The harness
installs the component repositories into a virtual environment and checks that every
module imports, that a profile can be created, that the example experiment compiles,
that the shot can be read in lyse and by the runviewer parsers, that the runmanager
library API works and that the four applications start. It uses pip and uv only. Conda
is not used: conda installs on Windows runners are slow, and conda-specific checks are
left until a release is close.

The GitHub Actions workflow `.github/workflows/test.yml` runs the harness on Ubuntu and
Windows for Python 3.11 to 3.15 with PySide6, PyQt6 and PyQt5 on every push that changes
the harness, weekly, and on demand with chosen component refs, Qt bindings, Pythons and
runners.

## Usage

```
python harness/suite.py clone [name=[owner/repo@]ref ...]
python harness/suite.py install --python 3.14 [--qt PySide6|PyQt6|PyQt5] [--pin "numpy<2.5"]
python harness/suite.py test --python 3.14 [--step NAME] [--skip NAME] [--all]
```

`clone` puts the components in `repos/` (`--repos-dir` to change). A component with no
ref is fetched at its upstream default branch, unless a clone already exists there, in
which case the clone is used as it is. A ref is a branch, tag, commit or `pr/<N>`, for
example `labscript=pr/124` or `zprocess=chrisjbillington/zprocess@fix-conpty`. `pr/<N>`
is the head of pull request N merged by `clone` into the current tip of the component's
default branch, so the result is the code that merging would produce; if the merge
conflicts, `clone` stops with a message. The resolved commits, and for a `pr/<N>` ref
the pull request head and the default branch commit it was merged into, are written to
`repos/manifest.json` and appear in the report.

`install` makes `harness/venvs/py<version>` with uv (`--venv` to change) and installs
every component from its clone in one resolver run, with the Qt binding and any pins.
`--python` is a version for uv to find or download, or a path to an interpreter.
Components are built with `SETUPTOOLS_SCM_PRETEND_VERSION=99.0.0` because shallow clones
have no tags and the components pin each other by version.
The commit of each clone at install time is recorded in the venv's `harness.json`, and
the report's component table is taken from it, so a clone that is changed after `clone`
(a local branch, for example) is described as installed.

`test` runs the steps below in order and writes `report.md`, `state.json` and one log
per step to `harness/work-py<version>/` (`--work` to change). A step that another step
depends on is skipped when the dependency failed. The exit status is nonzero if any step
failed. Set `GITHUB_STEP_SUMMARY` and the report is appended to it.

Every step runs with `LABSCRIPT_DISABLE_GRAPHICAL_EXCEPTHOOK=1`, so that the
applications and their subprocesses print exceptions to stderr instead of opening an
error window. labscript-utils releases before 3.5.0 ignore the variable.

## Steps

| Step | What it checks |
|---|---|
| `versions` | Python, dependency and component versions; every component is installed |
| `profile` | `labscript-profile-create` makes a profile; the labconfig points `shared_drive` at the work directory; the runmanager test fixtures are copied into `userlib/labscriptlib/runmanager_test` |
| `imports` | Every top-level module and the Qt-dependent modules import in a fresh interpreter with `-W error::DeprecationWarning`; the application entry modules byte-compile |
| `compile` | The profile's connection table and `example_experiment.py` compile through `runmanager.compile_labscript_async`; the shot file has the expected groups, devices, connection table rows, time markers and stop time |
| `lyse` | `lyse.Run` reads globals, saves and reads back results and arrays; `get_dataframe_from_shot` and `get_dataframe_from_shots` return the results |
| `runviewer` | `runviewer.__main__.Shot` loads the shot, which runs the runviewer parser of every device that has one; the traces and markers are checked |
| `runmanager-api` | The library API on the `runmanager_test` fixture: globals file CRUD, evaluation, expansion, diff, run files, single-shot and multishot compilation with the compiler output streamed to a PULL socket |
| `apps` | runmanager, runviewer, lyse and BLACS start under `QT_QPA_PLATFORM=offscreen`, listen on their labconfig ports and run for five seconds; the runmanager remote API is exercised; the output of each is checked for tracebacks |
| `lyse-gui` | The lyse GUI in this process under `QT_QPA_PLATFORM=offscreen`: a routine that loops in Python is interrupted by the Abort button and its worker survives, a routine blocked in a long sleep has its worker restarted, analysis is paused in both cases, and the interrupted worker then runs a routine to completion |
| `zprocess-tests` | The zprocess test suite with pytest. Skipped unless `--all` or `--step zprocess-tests` is given; it takes two minutes |

A check for a known open bug is marked `KNOWN` in the log and does not fail the step.
When the bug is fixed the check prints `FIXED` so that the marker can be removed. At
present the `runmanager-api` checks "globals in a cycle hold an error naming the cycle"
and "hierarchy of a conditional" are marked as known for runmanager #139, and
"expansion settings API present" is marked as known for runmanager #140, with the
checks of that API run only when it is present. The `runviewer` check
"DummyIntermediateDevice has a runviewer parser" is marked as known for
labscript-devices #157, with the checks of the
`analog_out` and `digital_out` trace values run only when the parser is present.

## The profile

The suite reads its profile from `~/labscript-suite` and `import labscript_utils`
creates one when none exists, so the `profile` step runs before anything else imports
labscript_utils. The harness writes a marker file into the profile it creates and on the
next run deletes and recreates only a profile that has the marker. A profile without the
marker stops the run; move it away before testing on a machine that has one. The shared
secret is carried over from the previous harness profile so that a zlock or zlog server
left running by an earlier run still accepts connections.

The applications use the ports in the labconfig (42517 to 42523 and 7339 to 7341), so
the `apps` step fails if a suite application is already running on the machine.

On a Linux machine that has a real profile and running suite servers, the harness can run
in a user, mount and network namespace instead, with a scratch directory as the home of
the mapped root user, so that the profile goes to that directory and the ports are
separate. The profile path comes from the user name, so `LOGNAME` and `USER` are set to
`root`:

```
mkdir -p /tmp/fakeroot
unshare -Urmn sh -c 'ip link set lo up && mount --bind /tmp/fakeroot /root \
    && export HOME=/root LOGNAME=root USER=root \
    && python harness/suite.py test --python 3.14 --work /tmp/harness-work'
```

The X display is still reachable through its socket, so an application started this way
appears on the desktop.

## Requirements

uv on the PATH or installed in the Python that runs `suite.py`; git; a C compiler for
labscript-c-extensions; on Linux the shared libraries that Qt needs (`libegl1`,
`libopengl0`, `libgl1`, `libxkbcommon0`, `libxkbcommon-x11-0`, `libdbus-1-3`,
`libfontconfig1`, `libglib2.0-0`, `libxcb-cursor0` on Ubuntu 24.04).

## Fixtures

`fixtures/runmanager_test/` holds a connection table and an experiment with dummy
devices whose globals (`amplitude`, `gain`, `offset`, `duration`, `use_do`, `derived`)
are created by the `runmanager-api` step. The experiment prints a line so that the step
can check that compiler output is streamed.
