# Instructions for Claude Code sessions

This repository holds the notes, plans and tooling for maintaining the labscript suite.
`README.md` lists the contents and the state of the work. Read it, then
`docs/RELEASE-PLAN.md` and `docs/MAINTENANCE.md`, before starting a task.

@STYLE.md

## Scope

- Maintain and release the existing labscript suite and its related repositories. Keep
  backward compatibility: existing experiment scripts, connection tables, shot files,
  globals files and labconfig files must keep working.
- The eight problems in `docs/ARCHITECTURE.md` are a record of design limits. Fixes that
  stay within the current design are in scope; a redesign is not. A from-scratch
  successor exists as a separate project and is not discussed or worked on here.
- Support Python 3.11 to 3.15, PyQt5, PyQt6 and PySide6 through qtutils, pip and conda
  installs, and Windows, Linux and macOS. Windows is the platform most labs run.

## Repositories

- Component repositories are cloned under `repos/` (ignored by git); `README.md` has the
  clone commands. Do not vendor them into this repository.
- Work in the component repositories on branches and open pull requests against the
  upstream default branch. Do not push to `master` of a labscript-suite repository
  without being asked.
- Commits need a clear message that states the change and the issue or PR number it
  addresses. Follow the attribution instructions that the session provides.

## Recording work

- When a review finding or triaged issue is fixed, update the status tables in
  `docs/MAINTENANCE.md` and mark the item in `docs/REVIEW.md` in place, as item 20 is
  marked. Do not rewrite the finding text.
- When a refactor moves code, add a line-reference table to `docs/MAINTENANCE.md` so the
  file:line citations in the other documents stay usable.
- When an issue or PR is closed or merged, update its row in `docs/ISSUE-TRIAGE.md` or
  `docs/PR-REVIEW.md` rather than deleting it.
- Record facts about the suite that were found by running code (what works on which
  Python and dependency versions, what fails and how) in `docs/TESTING.md`, with the date
  and the versions used.
- A defect found by testing that no GitHub issue, `docs/REVIEW.md` entry or
  `docs/ISSUE-TRIAGE.md` entry records goes in `docs/DEFECTS.md` with file and line,
  importance, how it was verified and its status. Defects are not filed upstream unless a
  fix is made; then the row names the pull request.

## Tests

- Prefer few tests, mostly integration or end-to-end tests that go through public entry
  points: install the packages, compile a shot with dummy devices, read it back, run the
  runviewer parsers on it. Do not add unit tests that restate the implementation.
- Verify findings by running code where possible and label each finding with how it was
  verified, as `docs/REVIEW.md` does: run, read or plausible.

## Issues and pull requests on GitHub

- Importance scale: 5 means fix before the next release, 1 means close. Keep it when
  ranking new items.
- For every bug report, check the current code before accepting the report's description
  of the state of the suite, and cite file and line.
- Public comments on GitHub are written to contributors and users of the suite. Keep them
  factual and specific; name the defect, the file and the suggested change.
