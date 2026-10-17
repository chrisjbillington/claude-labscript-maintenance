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

## Smoke tests behind the release plan

`smoke/install-and-import.sh <python version> <repos dir> <work dir>` makes a uv venv,
installs every component from the clones in dependency order with PySide6, imports every
top-level module with `-W error::DeprecationWarning` under the offscreen Qt platform,
byte-compiles the GUI entry modules and runs the zprocess test suite. Results for
Python 3.14 and 3.15 on 2026-10-17 are in `docs/RELEASE-PLAN.md` section 3.

`smoke/compile-example.sh <python version> <repos dir> <work dir>` uses that venv to
compile the default profile's example experiment through `runmanager` and reads the shot
back with `lyse.Run`. It needs a labscript profile, made with `labscript-profile-create`
in the venv. This is the test that fails on NumPy 2.5 with `data type 'a256' not
understood` (labscript #123).

`smoke/runmanager/` holds the scripts used to check runmanager PR #130 against master
before merging: `libtest.py <profile dir>` exercises the public library API (globals file
CRUD, evaluation, expansion, diff, run file creation, async compile) and `guitest.py
<profile dir>` drives a running runmanager through `runmanager.remote.Client`
(start runmanager with `QT_QPA_PLATFORM=offscreen python -m runmanager` first). Both
expect `experiment.py` and `connection_table.py` from that directory at
`<profile dir>/userlib/labscriptlib/refactor_test/`, and `guitest.py` expects runmanager
to have that experiment loaded with the globals file that `libtest.py` creates. They use
only dummy devices.
