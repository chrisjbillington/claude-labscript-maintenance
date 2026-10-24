# Tools

Scripts that produced the results in `docs/`. They are kept as they were used, with
machine-specific paths replaced by arguments, and are the starting material for a proper
test harness rather than one themselves.

## GitHub scrapers

`scrape_issue.py <org/repo> <number>` prints the title, state, opening post, every
comment and the timeline events of an issue, read from the JSON that github.com embeds
in the issue page. `scrape_pr.py <org/repo> <number> [pull|issues]` does the same for a
pull request page by parsing its HTML, and lists the file paths of inline review threads.
Neither uses the GitHub API, which is useful when the unauthenticated rate limit is
exhausted. The per-issue text files that `docs/ISSUE-TRIAGE.md` refers to as
`scratchpad/issues/<repo>_<N>.txt` were made with these scripts and are not kept here.
With `gh` authenticated, `gh issue view <N> --comments` is the simpler alternative.

## Integration testing branches

`integration-testing/build.sh WORKDIR [COMPONENT ...]` makes, for each component in
`integration-testing/branches`, a branch `integration-testing` that is the component's
master with the listed branches merged in the listed order, and force-pushes it to the
component's origin. It deletes the `integration-testing` branch of a component that has
no entries, and pushes nothing for a component in which master, the listed branches and
the result are unchanged. The branch is rebuilt from master each time; do not commit to
it. The script clones each component into `WORKDIR` from the origin of its clone under
`repos/` (`REPOS` overrides the location of `repos/`).

Merge conflicts are resolved with `git rerere`, and the recorded resolutions are kept in
`integration-testing/rr-cache/COMPONENT`. At a conflict with no recorded resolution, the
script stops with the merge in progress in `WORKDIR/COMPONENT`. Resolve it there, commit,
commit the new files under `rr-cache/` to this repository and run the script again.
After the merges, the patches in `integration-testing/patches/COMPONENT` are applied in
name order. A patch is a change to a merged branch that another merged branch requires
when there is no merge conflict:

| Patch | Change | Needed by |
|---|---|---|
| `runmanager/value-history-repack.patch` | `record_history` and `_modify_history_entry` open the globals file with `_open_for_writing` | runmanager #144 with #145; the second of the two to be merged needs the change |

`integration-testing/deploy.sh HOST DIR` checks out, in each git clone in `DIR` on
`HOST`, `integration-testing` at the version on origin, or `master` (fast-forwarded to
origin) if origin has no `integration-testing`. It does not update a clone that has
uncommitted changes. The lab machine's clones are in `~/labscript-suite/dev`, and the
components are installed from them in `~/labscript-suite/dev/.venv`.

## Smoke tests behind the release plan

The scripts that produced the results in `docs/RELEASE-PLAN.md` section 3 have been
replaced by the test harness in `harness/`, which runs the same install, import, compile
and read-back checks and more. See `harness/README.md`.

## Checks behind individual pull requests

`resample_check.py` exercises `labscript_c_extensions.runviewer.resample` the way
runviewer calls it (6002 output times, 6001 output values) with the cases from runviewer
#13 and `docs/REVIEW.md` item 19, and prints a checksum for a long random trace so that
builds can be compared. Run it with the Python of an environment that has the extension
installed. `outputbox_check.py <PySide6|PyQt6|PyQt5>` writes to a `qtutils.OutputBox`
under the offscreen platform, clears it through `clear_output()` and through the
context menu, and checks the displayed text after each step. Both were written for
labscript-c-extensions #13 and qtutils #36 (`docs/TESTING.md`, 2026-10-17).

## BLACS shot cycle timing

`blacs-timing/` measures the per-shot overhead of BLACS with dummy devices, for blacs
#132 and qtutils #38 (`docs/TESTING.md`, 2026-10-19). `bench.py --tabs N --shots M
--label L --out DIR` writes a connection table with a `DummyPseudoclock` and N
`DummyIntermediateDevice`s into the profile's labscriptlib, compiles one shot through
runmanager, starts BLACS under the offscreen Qt platform, submits M copies of the shot,
waits for them to run, and prints the medians of the queue manager phases and of each
tab's mainloop overhead per transition event from `BLACS.log`. `analyse.py
BLACS.log [M]` prints the same for an existing log. Both run with the Python of a
harness venv. `ns.sh`, run as `BENCH_SCRATCH=<dir> unshare -rmn ns.sh <command>`, runs
the command in a mount and network namespace in which `~/labscript-suite` is a scratch
profile (made beforehand with `labscript-profile-create` inside the namespace, with a
`.bench-profile` marker file) and only loopback is up, so that the zlock and zlog
servers BLACS starts are its own, write into the scratch profile, and are killed
afterwards. Without the network namespace a zlog server already running on the machine
writes the benchmark's `BLACS.log` into the real profile.

`bench.py --sample COUNTS` runs BLACS through `sample_blacs.py`, which records the Python
stack of every BLACS thread every 2 ms from 20 s after start-up and writes the count of
each stack to COUNTS when BLACS is terminated. `stacks.py COUNTS THREAD` lists, for one
thread (`main`, or a name such as `Thread-29 (manage)`), the number of samples in which
each function is on the stack and at its top. Use 150 shots or more so that the shots
are still running when sampling starts. py-spy does not work for this: in the namespace
it falls behind by minutes.

`bench.py --load N` runs N busy-loop processes while BLACS runs. `phases.py BLACS.log
...` prints, for each log, the medians of the phases of the shot cycle: from the end of
the previous shot to the first transition to buffered, the spread of the transitions,
the run, and so on, from the queue manager's messages and the tabs' "Processing event"
messages.

## BLACS queue manager behaviour

`blacs-queue/queuetest.py` checks the behaviour of the queue manager with the BLACS main
window, three tabs that have worker processes (`queuetest_worker.py`) and stand-ins for
the rest of BLACS: start and stop group order, the order of plugin callbacks, what is
saved to the shot file, start-up latency of an idle or unpaused queue, and the status,
pause and requeue after a failed or hung transition, a tab in an error state, a restart
or an abort in each phase, and a failed front panel save. It was written for the
experimental queue rewrite (`docs/BLACS-QUEUE.md`). Run it like `schedtest.py`, from its
directory: `QT_QPA_PLATFORM=offscreen PYTHONPATH=$PWD BENCH_SCRATCH=<dir> unshare -rmn
../blacs-timing/ns.sh <venv>/bin/python queuetest.py`, with the blacs under test first
on `PYTHONPATH` and a scratch profile in `<dir>` as for `bench.py`.

## BLACS state machine behaviour

`blacs-statemachine/schedtest.py` checks the behaviour of the tab state machine with two
tabs that have worker processes (`schedtest_worker.py`): state order, a state queued by
a state, mode selection, `delete_stale_states`, worker and state exceptions, an
unpicklable job, a bare `yield`, `event_queue.put` with a bound method, statemachine
timeouts, parallel jobs in two tabs, and restart and close during a worker job. It was
written for the main-thread state machine (`docs/BLACS-STATE-MACHINE.md`) and gives the
same results on blacs master. Run it from its directory as
`QT_QPA_PLATFORM=offscreen PYTHONPATH=$PWD BENCH_SCRATCH=<dir> unshare -rmn
../blacs-timing/ns.sh <venv>/bin/python schedtest.py`, with the blacs under test
installed in the venv or first on `PYTHONPATH`.

## Qt style screenshots

`style-screenshots/` takes images of the main windows of BLACS, runmanager, lyse and
runviewer for each Qt binding, with the platform's default Qt style and with Fusion, and
with the light and dark colour schemes. It was written to compare the look of the
applications across platforms before deciding whether to use Fusion everywhere
(`docs/RELEASE-PLAN.md` section 6). `run_all.py --work WORK --out DIR --venv
PySide6=PATH --venv PyQt6=PATH --venv PyQt5=PATH` runs `shoot.py` once per combination
and writes `DIR/<app>-<binding>-<style>-<scheme>.png`. WORK is a harness work directory
in which the `profile`, `compile` and `runmanager-api` steps have passed; the
applications load the shots, the globals file and the experiment script from it, and
two lyse routines that `run_all.py` writes. `shoot.py` replaces the binding's
`QApplication` with a subclass that sets the style and the colour scheme, runs the
application's entry module, loads the example data once the main window is shown,
resizes the window to 1500 by 950 pixels, saves the image and a JSON file of the
binding, the Qt version, the platform, the style and the resulting window colour, and
then waits to be killed. `--app`, `--style` and `--scheme` restrict the combinations.

The colour scheme is set with `QStyleHints.setColorScheme`, which Qt 5 does not have. On
Windows, a dark PyQt5 image uses the `windows:darkmode=2` platform option, which gives a
dark palette only when Windows itself is in dark mode. On Linux, `run_all.py` skips PyQt5
with the dark scheme.

On Linux the applications are run in namespaces, as the harness does on a machine with a
real profile, but the D-Bus session bus refuses a client whose user ID is 0, so the
command runs in a nested user namespace in which the user ID is that of the real user:

```
cat > ns.sh <<'END'
#!/bin/sh
ip link set lo up && mount --bind "$SCRATCH_HOME" /root || exit 1
export HOME=/root LOGNAME=root USER=root
exec unshare -U --map-user="$REAL_UID" --map-group="$REAL_GID" "$@"
END
SCRATCH_HOME=/tmp/fakeroot REAL_UID=$(id -u) REAL_GID=$(id -g) \
    unshare -Urmnp --fork sh ns.sh python tools/style-screenshots/run_all.py ...
```

The harness steps that make WORK run the same way, with `harness/suite.py test` in place
of `run_all.py`. The scratch home has no GNOME settings, so the GTK theme is the default
Adwaita and not the desktop's theme.

## runmanager value history

`value-history/drive.py --out DIR --labscript-file FILE [--scheme light|dark] [--size WxH]` starts
runmanager under the offscreen Qt platform, makes a globals file in DIR with older uses
recorded in its history, compiles FILE several times through Engage, and exercises the
value history: the order of the list, filtering, choosing a value with the keyboard,
pinning, removing, switching to the previous value, Alt+Down in the table and in the
editor, and renaming a global. It prints PASS or FAIL for each check and saves
screenshots in DIR. FILE is the runmanager test experiment of a harness profile
(`userlib/labscriptlib/runmanager_test/experiment.py`). It was run with the Python of a
harness venv that has the runmanager branch installed, in the namespace of
`blacs-timing/ns.sh`. With `--scheme dark` it sets a dark palette and tells runmanager
that the colour scheme is dark, since the offscreen platform has no colour scheme. The offscreen screen is 800 pixels
wide, which moves the popup to the left; the screenshots in runmanager #145 were taken
with `QT_QPA_PLATFORM=offscreen:configfile=value-history/offscreen.json`, a 1920 by 1080
screen, and `--size 1250x600`.

