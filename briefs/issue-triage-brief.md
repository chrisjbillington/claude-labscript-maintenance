# Issue triage brief

This is the brief given to the agents that produced the issue triage of 2026-10-17
(`docs/ISSUE-TRIAGE.md`), kept as the record of the
method, criteria and importance scale. The instructions about other agents' checkouts, the
exhausted API rate limit and the scratch directory of scraped text were specific to that
session.

You are triaging open GitHub issues (bug reports, feature requests, questions) on
labscript-suite repositories for the maintainer (an original labscript author). The
repos are cloned under `repos/<repo>` (see README.md).

## Hard rules

- READ ONLY. Never run `git checkout`, `git switch`, `git stash`, `git reset`, `git merge`,
  `git rebase`, `git pull`, or edit any file in any repo. Other agents use these checkouts.
  The runmanager checkout is on a branch named `refactor-fixes` that belongs to another
  agent: for runmanager, read code with `git -C runmanager show origin/master:<path>` and
  `git -C runmanager grep <pattern> origin/master -- <path>`, never from the working tree.
  For every other repo the working tree is the upstream default branch and you may read
  files directly.
- Do NOT call api.github.com (rate limit exhausted). Each issue's full conversation
  (title, body, every comment) is saved as text at
  <scratch directory>/issues/<repo>_<N>.txt
  and the raw metadata list at .../scratchpad/issues/<repo>.json (labels, dates, comment counts).
  Read these first. If a file is missing or empty, say so and judge from the JSON only.
- For every bug report, CHECK THE CURRENT CODE. Many issues are years old. Determine
  whether the bug still exists on the current default branch (cite file:line), was fixed
  (cite the commit if you can find it with `git log -S` or `git log --grep`), or cannot be
  determined without hardware. Do not take the issue text's word for the current state.
- Open PRs were reviewed separately; the ranked list is at
  docs/PR-REVIEW.md. Read its section 1 table so
  you can say when an open PR addresses an issue.

## Context

The maintainer is preparing a next release of the legacy labscript suite (support for
Python 3.11-3.15, dropping 3.8-3.10; PySide6/PyQt6 transition already partly done in
2026 commits; qtutils now lives at github.com/philipstarkey/qtutils v4.1.3). Separately,
a from-scratch successor ("shotscript") is being built; its design choices make some
legacy issues moot, and some issues are requirements it should meet. Flag both.

## Output

Write a Markdown report to the path given in your prompt. For each issue include:

### <repo> #<N>: <title> (<author>, opened <date>, last activity <date>, <n> comments)
- **Summary**: 1-3 sentences, what is actually being reported or asked.
- **Type**: bug / feature request / question-support / docs / tooling / meta
- **Still valid?**: yes (bug reproduced in current code at file:line) / fixed (commit) /
  obsolete (why) / cannot verify (why) / n.a. for non-bugs
- **Severity** (bugs): crash-data-loss / wrong-behaviour / annoyance / cosmetic
- **Scope**: which component, platform- or hardware-specific?
- **Related**: duplicates, related issues, open PRs (from PR-REVIEW.md) that address it
- **Effort**: trivial (<1 h) / small (hours) / medium (days) / large
- **Release relevance**: yes/no, with a sentence if yes (e.g. breaks on Python 3.13+,
  PySide6, NumPy 2, modern h5py, Windows 11); this feeds the release plan.
- **Rewrite relevance**: "moot (why)", "requirement (what)", or "none".
- **Importance**: 1 (close) to 5 (fix before next release) with one-sentence reason
- **Recommended action**: fix for next release / fix later / ask reporter for info /
  close as fixed / close as stale or won't fix / convert to docs / leave open

End the report with a ranked table (rank, issue, type, importance, action), and a short
list of "release-relevant" issues.

Writing style: plain technical language, no metaphors, no flourishes. State facts and
conclusions. Be specific and concise; do not pad.

When you finish, reply with the report path and one line per issue with importance 4-5,
plus a count of the rest by recommended action.
