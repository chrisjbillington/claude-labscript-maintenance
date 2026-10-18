# claude-labscript-maintenance

Working notes, plans and tooling for AI-assisted maintenance of the
[labscript suite](https://github.com/labscript-suite) and the related repositories
under [chrisjbillington](https://github.com/chrisjbillington) (zprocess, desktop-app,
setuptools-conda, spinapi, pynivision, ci-helper) and
[philipstarkey/qtutils](https://github.com/philipstarkey/qtutils). It is meant to be
opened by Claude Code sessions, including cloud sessions, so that each session can
continue from the recorded state instead of re-deriving it.

Scope: maintenance and release of the existing suite, with its existing design and
backward compatibility.

## Contents

| Path | What it is |
|---|---|
| `CLAUDE.md` | Instructions for Claude Code sessions working in this repository |
| `STYLE.md` | The maintainer's guidelines for prose, code comments and working habits |
| `docs/REVIEW.md` | Code review of every suite repo (2026-09-30): bugs and cruft with file and line, verification labels |
| `docs/ARCHITECTURE.md` | Eight structural problems found by the review, with proposed directions (2026-10-01) |
| `docs/MAINTENANCE.md` | Status of each review finding in the existing suite, and a map from review line numbers to code that later refactors moved |
| `docs/ISSUE-TRIAGE.md` | All 223 open issues ranked 1 to 5, each checked against current code, with per-repo detail (2026-10-17) |
| `docs/PULL-REQUESTS.md` | Every pull request opened by this maintenance track, with links and state |
| `patches/` | Commits waiting to be applied by a local session or carried into a later pull request, as `git format-patch` files; each is deleted once applied |
| `docs/PR-REVIEW.md` | All 30 open pull requests ranked, with defects found and a recommended action for each (2026-10-17) |
| `docs/RELEASE-PLAN.md` | Plan for the next minor release of every component: Python 3.11 to 3.15, NumPy 2.5, workflow sync, work items, release order (2026-10-17) |
| `briefs/` | The briefs given to the agents that produced the issue triage and PR review; the criteria and importance scale to reuse |
| `harness/` | Test harness: installs the component repositories at given refs into a venv and runs end-to-end checks (import, profile, compile, lyse, runviewer parsers, runmanager API, application start-up); `harness/README.md` |
| `.github/workflows/test.yml` | Runs the harness on Ubuntu and Windows for Python 3.11 to 3.15 with PySide6, PyQt6 and PyQt5: on pushes that change the harness, weekly, and on demand with chosen component refs |
| `docs/TESTING.md` | Results of the harness runs, with dates and versions |
| `docs/DEFECTS.md` | Defects found by testing that no GitHub issue or review document records, with importance and status |
| `docs/LOCAL-TASKS.md` | Tasks that a cloud session could not do, for a local session to do under supervision |
| `tools/` | Scripts used to produce the documents: GitHub page scrapers |

Read `docs/RELEASE-PLAN.md` first for what needs doing. `docs/MAINTENANCE.md` says what has
been fixed already. The ranked tables at the top of `docs/ISSUE-TRIAGE.md` and
`docs/PR-REVIEW.md` give the per-item actions; the rest of those files is the reasoning
and the file:line evidence.

## State as of 2026-10-18

- runmanager PR #130 (the module split) was merged 2026-10-17 as bfe63ba with a fix
  commit. labscript-utils PR #128 was merged upstream on 2026-10-13 and fixes review item
  20 and parts of several others (`docs/MAINTENANCE.md`).
- Release blocker, fixed: NumPy 2.5 removed the `a256` dtype alias, so no shot compiled
  on the master branches (labscript #123). labscript #124, labscript-devices #149 and
  blacs #124 replace it with `S256` and were merged 2026-10-17.
- Thirty pull requests opened 2026-10-17 for the six release plan blockers; table in
  `docs/PULL-REQUESTS.md`. Twenty-eight were merged the same day, which closed
  labscript #123, labscript-utils #28, labscript-suite #56 and zprocess #27. The two
  that remain, runmanager #131 and labscript-suite #106, raise component pins to
  unreleased versions and are held until their step of the release sequence
  (`docs/RELEASE-PLAN.md` section 5).
- Twenty-three pull requests of fixes, opened 2026-10-17 and 2026-10-18 and merged
  2026-10-18 (`docs/PULL-REQUESTS.md`): labscript #128 and #129, labscript-utils #133,
  #134 and #135, labscript-devices #153, #154 and #155, blacs #128, #129 and #130,
  runmanager #134, #135 and #136, runviewer #76 and #77, lyse #144 to #147,
  labscript-c-extensions #14, labscript-suite #109 and zprocess #32. Each passed the
  harness on Python 3.11 to 3.14 with all three Qt bindings (`docs/TESTING.md`). Every
  Part 1 review item is now fixed on `master`; item 3 (the NI_DAQmx final read) is
  verified by reading only and needs a test on NI hardware. Every Part 2 bug is fixed
  except the few that need a design decision or hardware (`docs/MAINTENANCE.md`, "Part 2
  status"). The issues the pull requests fix are closed, except zprocess #16, which the
  maintainer left open.
- The release pull requests from contributors (labscript-devices #110, #126, #144, #87,
  #63, lyse #132, labscript-utils #117, prawn_digital_output #23) were merged 2026-10-17
  with maintainer fix commits (`docs/LOCAL-TASKS.md`). The step 2 and 3 pull requests
  (qtutils #36, #37, desktop-app #34) are merged. Defect D7 (the release workflow's tag
  step under PowerShell) is fixed in the sandbox and in every repository. The
  labscript-c-extensions resampler fix #13 (release sequence step 4) is merged.
- No tag is pushed until the release set is ready; zprocess 2.28.0rc2 is the only release
  candidate. Changes are tested from the `release.yml` runs on `master` (Test PyPI and the
  conda test label) and from harness dispatches with branch or `pr/N` refs
  (`docs/RELEASE-PLAN.md` section 5).
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
