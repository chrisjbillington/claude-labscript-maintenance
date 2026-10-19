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
