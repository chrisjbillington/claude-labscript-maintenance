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
- Prefer dependencies that the default conda channels carry. Before requiring a package
  or version that only conda-forge has, raise it with the maintainer.

## Repositories

- Commit work in this repository directly to `main` and push it there. Do not open
  branches or pull requests in this repository.
- Component repositories are cloned under `repos/` (ignored by git); `README.md` has the
  clone commands. Do not vendor them into this repository.
- Work in the component repositories on branches and open pull requests against the
  upstream default branch. Do not push to `master` of a labscript-suite repository
  without being asked.
- Commits need a clear message that states the change and the issue or PR number it
  addresses. Follow the attribution instructions that the session provides.
- A fix for a branch that the session cannot push to (a contributor's fork) is stored as
  a `git format-patch` file in `patches/`, with a row in `docs/LOCAL-TASKS.md` that says
  where to apply it with `git am`. Do not push it as a branch to the upstream
  repository. The local session deletes the patch file once it is applied. A commit
  kept only in a clone under `repos/` for a later pull request is stored the same way.
- Delete a branch in a component repository once its pull request is merged, and record
  in `docs/LOCAL-TASKS.md` any branch that the session cannot delete itself.
- Describe verification in commit messages and pull request descriptions in plain
  terms: what was run and what happened ("the module imports without a warning", "the
  example experiment compiles on NumPy 2.5.4"). Do not quote interpreter flags or the
  mechanics of the check; a reader who does not know the flag learns nothing from it.

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

- Check a change in one harness venv while making it. Before asking for a pull request
  to be merged, dispatch `.github/workflows/test.yml` with the pull request refs
  (`name=pr/N`, which tests the pull request merged into its base branch), so that the
  change has a result on Ubuntu and Windows for every supported Python and Qt binding,
  and record the run in `docs/TESTING.md`.
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
  factual and specific; name the defect, the file and the suggested change. Do not refer
  to this repository, its documents, its harness or how the work is organised; readers
  do not know what they are. State verification results directly.
- Open a pull request only after the test workflow has passed on the pushed branch
  (`name=owner/repo@branch` in the dispatch refs). Do not open one that says a test is
  still running.
- Every comment, review or pull request description that a session posts on GitHub, or
  drafts for the local session to post, goes out from the maintainer's account. Start
  it with this quoted note, so that readers know the maintainer did not write it:

  > **Written by Claude.** This comment and the commit it describes were produced by
  > Claude, the AI model, in a Claude Code session that @chrisjbillington is running
  > for labscript suite maintenance. It is posted from his account; the commit is
  > authored as Claude.

  Drop the clause about the commit when the comment describes no commit. Write the
  rest of the comment in the first person as Claude. Commits are authored as
  `Claude <noreply@anthropic.com>`.
