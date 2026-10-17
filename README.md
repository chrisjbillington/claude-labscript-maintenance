# claude-labscript-maintenance

Working notes, plans and tooling for AI-assisted maintenance of the
[labscript suite](https://github.com/labscript-suite) and the related repositories
under [chrisjbillington](https://github.com/chrisjbillington) (zprocess, desktop-app,
setuptools-conda, spinapi, pynivision, ci-helper) and
[philipstarkey/qtutils](https://github.com/philipstarkey/qtutils). It is meant to be
opened by Claude Code sessions, including cloud sessions, so that each session can
continue from the recorded state instead of re-deriving it.

Scope: maintenance and release of the existing suite, with its existing design and
backward compatibility. A from-scratch successor is being developed separately and is not
part of this repository.

## Contents

| Path | What it is |
|---|---|
| `CLAUDE.md` | Instructions for Claude Code sessions working in this repository |
| `STYLE.md` | The maintainer's guidelines for prose, code comments and working habits |
| `docs/REVIEW.md` | Code review of every suite repo (2026-09-30): bugs and cruft with file and line, verification labels |
| `docs/ARCHITECTURE.md` | Eight structural problems found by the review, with proposed directions (2026-10-01) |
| `docs/MAINTENANCE.md` | Status of each review finding in the existing suite, and a map from review line numbers to code that later refactors moved |
| `docs/ISSUE-TRIAGE.md` | All 223 open issues ranked 1 to 5, each checked against current code, with per-repo detail (2026-10-17) |
| `docs/PR-REVIEW.md` | All 30 open pull requests ranked, with defects found and a recommended action for each (2026-10-17) |
| `docs/RELEASE-PLAN.md` | Plan for the next minor release of every component: Python 3.11 to 3.15, NumPy 2.5, workflow sync, work items, release order (2026-10-17) |
| `briefs/` | The briefs given to the agents that produced the issue triage and PR review; the criteria and importance scale to reuse |
| `harness/` | Test harness: installs the component repositories at given refs into a venv and runs end-to-end checks (import, profile, compile, lyse, runviewer parsers, runmanager API, application start-up); `harness/README.md` |
| `.github/workflows/test.yml` | Runs the harness on Ubuntu and Windows for Python 3.11 to 3.15: on pushes that change the harness, weekly, and on demand with chosen component refs |
| `docs/TESTING.md` | Results of the harness runs, with dates and versions, and the defects they found |
| `docs/LOCAL-TASKS.md` | Tasks that a cloud session could not do, for a local session to do under supervision |
| `tools/` | Scripts used to produce the documents: GitHub page scrapers |

Read `docs/RELEASE-PLAN.md` first for what needs doing. `docs/MAINTENANCE.md` says what has
been fixed already. The ranked tables at the top of `docs/ISSUE-TRIAGE.md` and
`docs/PR-REVIEW.md` give the per-item actions; the rest of those files is the reasoning
and the file:line evidence.

## State as of 2026-10-17

- No issue has been fixed and no PR merged or closed as a result of these documents,
  except runmanager PR #130 (the module split), merged 2026-10-17 as bfe63ba with a fix
  commit. labscript-utils PR #128 was merged upstream on 2026-10-13 and fixes review item
  20 and parts of several others (`docs/MAINTENANCE.md`).
- Release blocker: NumPy 2.5 removed the `a256` dtype alias, so no shot compiles on the
  current master branches (labscript #123). With `S256` the suite compiles and lyse reads
  the shot on Python 3.14.
- Python 3.15 works for the code but installs are blocked by missing h5py wheels on PyPI
  and missing pyzmq and PyQt builds on conda-forge.
- No component repo has a test or lint workflow; only `release.yml`. The harness in this
  repository covers the suite end to end on Linux and Windows (`docs/TESTING.md`).

## Working with the component repositories

Clone the component repositories into `repos/` (ignored by git) when a session needs
them. The documents cite paths relative to each repo root. Branch names: `master`
everywhere except prawn_digital_output, which uses `main`.

```
mkdir -p repos && cd repos
for r in labscript labscript-utils labscript-devices blacs lyse runmanager runviewer \
         labscript-suite labscript-c-extensions PrawnBlaster prawn_digital_output; do
  git clone git@github.com:labscript-suite/$r.git
done
for r in zprocess desktop-app setuptools-conda spinapi pynivision ci-helper; do
  git clone git@github.com:chrisjbillington/$r.git
done
git clone git@github.com:philipstarkey/qtutils.git
git clone git@github.com:rpanderson/workflow-sandbox.git
```

The release workflow in every repo is a copy deployed from rpanderson/workflow-sandbox.
The chrisjbillington fork of workflow-sandbox and the chrisjbillington fork of qtutils
are unmaintained and not used.

`docs/PR-REVIEW.md` refers to PR heads as `origin/pr/<N>`. To get them:

```
git -C repos/<repo> fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'
```

The documents were written against the commits listed in `docs/REVIEW.md` and
`docs/MAINTENANCE.md`. Fetch before relying on a line number, and record moved code in
`docs/MAINTENANCE.md` as the runmanager table there does.

`python harness/suite.py clone` does the same clones, shallow, and accepts a branch, tag,
commit or `pr/<N>` per component.

## Planned additions

Issue lists synced from GitHub or found in testing.
