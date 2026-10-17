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
