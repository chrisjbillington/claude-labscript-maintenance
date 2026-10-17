# PR review brief

This is the brief given to the agents that produced the PR review of 2026-10-17
(`docs/PR-REVIEW.md`), kept as the record of the
method, criteria and importance scale. The instructions about other agents' checkouts, the
exhausted API rate limit and the scratch directory of scraped text were specific to that
session.

You are reviewing open GitHub pull requests on labscript-suite repositories for the
maintainer (an original labscript author). The repos are cloned under
`repos/<repo>` (see README.md). Every PR's head commit is fetched as
the remote-tracking ref `origin/pr/<N>` in that repo.

## Hard rules

- READ ONLY. Never run `git checkout`, `git switch`, `git stash`, `git reset`, `git merge`,
  `git rebase`, `git pull`, or edit any file in any repo. Other agents are working in
  these checkouts (runmanager is currently on a branch named `refactor-fixes` that
  belongs to another agent; do not touch it).
- Compare against the upstream default branch ref: `origin/master` for every repo except
  prawn_digital_output, which uses `origin/main`.
- Useful commands:
  - `git -C <repo> log --format='%h %ad %an: %s' --date=short origin/master..origin/pr/N`
  - `git -C <repo> diff --stat origin/master...origin/pr/N`
  - `git -C <repo> diff origin/master...origin/pr/N -- <path>`
  - `git -C <repo> show origin/pr/N:<path>` to read a file as it is in the PR
  - `git -C <repo> merge-tree --write-tree origin/master origin/pr/N` (exit status non-zero
    means merge conflicts; add `--name-only` to list the files)
  - `git -C <repo> rev-list --count origin/pr/N..origin/master` (commits on master the PR lacks)
  - `git -C <repo> log --oneline origin/pr/N..origin/master -- <path>` (what changed on
    master since in the files the PR touches)
- Do NOT use the GitHub API (`api.github.com`); the rate limit is exhausted. The PR
  metadata and the full conversation (description, comments, review comments) for each PR
  are already saved as text:
  - <scratch directory>/prs/<repo>_<N>.txt
  - raw JSON list of open PRs per repo: .../scratchpad/prs/<repo>.json (title, body, dates, author, head sha)
  Read these first.
- Read the actual code of the PR, not only the description. Check whether the base
  branch has since changed in ways that obsolete, conflict with, or already implement the
  PR. Check whether the PR is internally consistent (callers updated, imports present,
  obvious bugs, platform assumptions, Python version assumptions).

## Context on the maintainer's current direction

The maintainer is building a from-scratch successor ("shotscript", at
not part of this repository) that drops
zprocess/zeromq, drops conda, replaces BLACS with `shotscript control`, and has its own
device/worker model. The legacy repos are still maintained for the user community, so
PRs are judged mainly on their merit for the legacy suite, but note separately whether a
PR contains an idea or hardware knowledge worth carrying into the rewrite.

## Output

Write a Markdown report to the path given in your prompt. For each PR include a section:

### <repo> #<N>: <title> (<author>, opened <date>, last updated <date>)
- **What it does**: 2-4 sentences, from reading the code.
- **Type**: bugfix / feature / refactor / docs-example / tooling-CI / firmware (pick one or two)
- **Size**: files changed, +/- lines, number of commits
- **No-brainer?**: yes / no, with one sentence why
- **Implementation**: is it done reasonably? Is there an obviously better way? List concrete defects you found (file:line where possible). Be specific; do not pad.
- **Up to date?**: merges cleanly or conflicts (list files); has master since changed the same code; is it superseded by something merged; depends on other open/closed PRs; dependency or Python version drift.
- **Tested?**: what the author says, and whether the code could have been run as written.
- **Discussion state**: who the ball is with (author / maintainer), what reviewers asked for, whether the author went quiet.
- **Breaking?**: API, connection-table, file-format or behaviour changes for existing users.
- **Rewrite relevance**: one sentence, or "none".
- **Importance**: 1 (ignore/close) to 5 (merge or act soon) with one-sentence reason.
- **Recommended action**: merge as is / merge after small fixes (list them) / ask author for X / rework by maintainer / close as obsolete / close as out of scope.

End the report with a short ranked table of your PRs (rank, PR, type, importance, action).

Writing style: plain technical language, no metaphors, no flourishes. State facts and
conclusions. Do not restate the PR description at length.

When you finish, reply with the report path and a 1-2 line summary per PR (importance and action).
