# labscript suite maintenance track

Started: 2026-10-17. Companion to `REVIEW.md` (findings) and `ARCHITECTURE.md` (design
problems).

## Purpose

The existing suite is maintained and released in parallel with a from-scratch rewrite,
which is a separate project and is out of scope for this repository. The rewrite breaks
backward compatibility, and labs will keep running the existing suite for some time after
it exists. The maintenance track therefore takes the `REVIEW.md`
findings that can be fixed without changing the suite's design: everything in Part 1, the
Part 2 bugs, and the cruft that can be removed without an API change. The eight problems in
`ARCHITECTURE.md` are out of scope for this track.

This document records which findings have been addressed in the existing suite, in which
release or pull request, and where the affected code now lives when a refactor has moved
it. `REVIEW.md` keeps its original numbering. A fixed item is marked in place there, as item
20 is, and the detail is kept here.

## Repository state relative to the review

`REVIEW.md` was written against the commits in its scope table. The pull requests in
`PULL-REQUESTS.md` (dtype aliases, packaging metadata, workflow sync, the fixes below) have
since moved `master` of every repo. The changes that touch review items are:

| Repo | Reviewed | Now | Change |
|---|---|---|---|
| `labscript-utils` | 22616a7 | PR #128, merged 2026-10-13 | bug fixes in zlock, excepthook, properties, ls_zprocess, splash and the header view widget |
| `runmanager` | 08ccc99 | PR #130, merged 2026-10-17 as bfe63ba | module split of `runmanager/__init__.py`, widgets moved out of `__main__.py`, style cleanup |
| `labscript-c-extensions` | (scope table) | PR #13, merged 2026-10-17 as b0f985d | item 19: `resample.pyx` NaN lead-in and loop bounds |

### labscript-utils PR #128 (ispielma)

Review items affected:

- **Part 1 item 20: fixed.** `zlock.py` now passes `str(config['zlock_port'])` to `Popen`.
- **B2, partly fixed.** `properties._default` now handles `np.floating` and `np.bool_`. The
  JSON fallback is still taken only for a `TypeError` containing "has no native HDF5
  equivalent" (`properties.py:90-94`), and the round-trip type inconsistency remains.
- **B6, partly fixed.** `on_columnsRemoved` no longer mutates `self.widgets` while iterating
  it. `headerview_with_widgets.py:155` still calls `max()` on an empty sequence when all
  sections are hidden.
- **B10, mostly fixed.** The `issubclass` test now names `SecureSocket`, and the "security
  not configured" check runs whether or not `allow_insecure` is present. The docstring at
  `ls_zprocess.py:180` still names the nonexistent `labscript_utils.zprocess.ZMQServer`.
- **C5, partly fixed.** `set_logger` no longer makes `warnings.showwarning` recurse. The
  `Thread.run` monkeypatch (now `excepthook/__init__.py:40-56`) and `logger.warn` (line 86)
  remain.

### runmanager PR #130 (carterturn, with fix commit 7c50b46)

The PR rearranges code and changes no behaviour, so it fixes no bug in the review. The PR
head had four regressions (a broken `expand_globals` reference, the public API reduced to
one function, the icon resource import removed, a missing f-string prefix), which the fix
commit repairs. Library and GUI behaviour was checked to be identical to `master` before
merging.

The only cruft it removes is part of **C2**: the unused imports `ast` and `pprint`, and the
commented-out axes context-menu code. `qtutils.icons` is listed in C2 as unused, which is
wrong: the import registers the Qt resources behind every `:/qtutils/...` icon. The rest
of C2 remains. **C8** gains a `[tool.ruff.lint]` section in `pyproject.toml`.

The old `runmanager/__init__.py` is now split as follows:

| New module | Contents |
|---|---|
| `group_manager.py` | globals file and group CRUD, `get_all_groups`, `get_globals`, `get_shot_globals`, `guess_expansion_type` |
| `evaluator.py` | `TraceDictionary`, `iterator_to_tuple`, `evaluate_globals` |
| `expander.py` | `expand_globals` |
| `compiler.py` | sequence index, run file creation, the three `compile_*_async` functions |
| `differ.py` | `flatten_globals`, `dict_diff`, `globals_diff_groups`, `globals_diff_shots` |
| `tokenizer.py` | `find_comments`, `remove_comments_and_tokenify` |
| `exceptions.py` | `ExpansionError` |
| `widgets.py` | the Qt view, delegate, tab bar and colour classes from `__main__.py` |

`runmanager/__init__.py` re-exports all of these names, so `import runmanager` code is
unaffected. The review's line references map to the new layout as follows.

| Finding | Reviewed location | Current location |
|---|---|---|
| Part 1 item 9 | `__main__.py:1957`, `__init__.py:603`, `__main__.py:2150` | `__main__.py:1339`, `expander.py:102`, `__main__.py:1527` |
| Part 1 item 14 | `__main__.py:2776-2786`, `2392`, `2692`, `3347` | `__main__.py:2151-2161`, `1767`, `2067`, `2720` |
| B1 | `__init__.py:468-472`, `572`; `__main__.py:3438-3448`, `2745` | `evaluator.py:125-130`, `expander.py:71`; `__main__.py:2811-2821`, `2120` |
| B2 | `__main__.py:1372-1374` | `__main__.py:756-758` |
| B3 | `__main__.py:3456-3475`, `3562-3568` | `__main__.py:2829-2848`, `2935-2941` |
| B4 | `__init__.py:572` | `expander.py:71` |
| B5 | `__main__.py:1819-1821` | `__main__.py:1202-1204` |
| B6 | `__main__.py:3696` | `__main__.py:3070` |
| B7 | `__init__.py:1107-1111`, `1122` | `differ.py:110-114`, `125` |
| B8 | `__init__.py:749`, `815` | `compiler.py:159`, `225` |
| B9 | `batch_compiler.py:61-62`, `74`; `__main__.py:3380` | `batch_compiler.py:63-64`, `76`; `__main__.py:2753` |
| B10 | `__init__.py:1002-1003` | `tokenizer.py:31-32` |
| B11 | `__init__.py:607-608` | `expander.py:106-107` |
| B12 | `__main__.py:3392` | `__main__.py:2765` |
| B13 | `__init__.py:857-858`, `892-898`, `903` | `compiler.py:267-268`, `302-308`, `313` |
| B14 `delete_global` | `__init__.py:326-329` | `group_manager.py:281-284` |
| B14 `copy_group` | `__init__.py:201-217` | `group_manager.py:156-172` |
| B14 run number | `__init__.py:815` | `compiler.py:225` |
| B14 copy/move menu | `__main__.py:2179-2188` | `__main__.py:1556-1565` |
| B14 remote cwd | `__main__.py:3794`, `3804` | `__main__.py:3166`, `3176` |
| B14 missing return | `__main__.py:1872-1873` | `__main__.py:1255-1256` |
| B14 no current index | `__main__.py:427` | `widgets.py:375` |
| B14 `send_to_runviewer` | `__main__.py:3642-3647` | `__main__.py:3015-3020` |
| B14 zlock in main thread | `__main__.py:2593`, `__init__.py:641` | `__main__.py:1968`, `compiler.py:51` |
| B14 `e.__class__(msg)` | `__main__.py:3841` | `__main__.py:3213` |
| B14 `engage()` | `remote.py:53-54` | unchanged |
| C1 | `__main__.py:1847, 1890, 2293, 2314, 2334, 3148, 3249` | `__main__.py:1230, 1272, 1668, 1689, 1709, 2521, 2622` |
| C2 `nested` | `__main__.py:129-136` | `__main__.py:122-126` |
| C2 `log_if_global` | `__main__.py:86-102` | `__main__.py:91-107` |
| C2 axes menu stubs | `__main__.py:1671-1674`, `1761-1763`, `2018-2030` | `__main__.py:1054-1057`, `1144-1146`, `1400-1407` |
| C2 `iconPosition` | `__main__.py:160-163` | `widgets.py:108-111` |
| C2 `is None` checks | `__main__.py:1907`, `2623` | `__main__.py:1289`, `1998` |
| C2 commented logger lines | `__main__.py:1362`, `1369-1370`, `1381-1407`, `3403-3414` | `__main__.py:746`, `753-754`, `765-791`, `2776-2787` |
| C3 | `__main__.py:3597`, `3267`, `1449` | `__main__.py:2970`, `2640`, `833` |
| C4 `get_grouplist` | `__init__.py:161-166` | `group_manager.py:116-121` |
| C4 `_ensure_str` | `__init__.py:289, 303, 317, 392-394` | `group_manager.py:244, 258, 272, 332-334` |
| C4 `get_shot_globals` | `__init__.py:947-959` | `group_manager.py:338-350` |
| C4 docstring | `__init__.py:915` | `compiler.py:325` |
| C5 | `remote.py` | unchanged |
| C6 | `globals_diff.py` | unchanged, now calls `runmanager.differ` |
| C7 | `__main__.py:76`, `560` | `__main__.py:81`, `widgets.py:508` |

## Part 1 status

| Item | Status |
|---|---|
| 1 `'a256'` dtypes | fixed, labscript PR #124, labscript-devices PR #149 and blacs PR #124, merged 2026-10-17 |
| 2 `bitfield` dtype | open |
| 3 NI analog input final read | open |
| 4 PrawnDO wait insertion | open |
| 5 PrawnBlaster and PrawnDO clock limit | open |
| 6 ramp tick count | fixed, labscript PR #128 (open) |
| 7 `get_change_times` collision check | fixed, labscript PR #128 (open) |
| 8 trigger proximity check | fixed, labscript PR #128 (open) |
| 9 Qt6 check states | open |
| 10 `aom.py` `max` | fixed, labscript-utils PR #133 (open) |
| 11 BLACS queue `get(2)` | open |
| 12 BLACS error handlers | fixed, blacs PR #128 (open); the unbound `message` log line remains |
| 13 `_rep` filename | open; the 2022 WIP PRs blacs #90 and runmanager #104 contain a fix |
| 14 preparse `task_done` | open |
| 15 lyse `blockSignals` | open |
| 16 lyse on pandas 3 | open |
| 17 PrawnBlaster wait without monitor | fixed, labscript-devices PR #153 (open) |
| 18 `h5_lock` | fixed, labscript-utils PR #133 (open) |
| 19 runviewer resampler bounds | fixed, labscript-c-extensions PR #13, merged 2026-10-17 as b0f985d |
| 20 zlock port | fixed, labscript-utils PR #128 |

Item 1 is fixed by the pull requests in the table below. Items 10 and 18 are fixed by
labscript-utils PR #133 (open), which also fixes labscript-utils B16 (blacs #100),
DEFECTS.md D3 and labscript-utils #60. Items 6, 7 and 8 are fixed by labscript PR #128
(open), which also fixes labscript B1, B2, B4, B6, B7, B8, B9, B10 and most of B5 and B11,
and labscript #16, #43 and #52. Item 12 is fixed by blacs PR #128 (open) and item 17 by
labscript-devices PR #153 (open), both opened 2026-10-18 with issue fixes. No open pull
request addresses the other items.

## Pull requests opened by the maintenance track

`PULL-REQUESTS.md` lists every pull request opened from this repository, with links and
state. On 2026-10-17: three for the NumPy 2.5 dtype alias (labscript #124,
labscript-devices #149, blacs #124), zprocess #28, labscript-utils #129, and the Python
3.11 metadata change on twelve repos; later the same day, workflow-sandbox #46 for
labscript-suite #56 and a workflow sync PR on each of the twelve repos. All were merged
on 2026-10-17 except runmanager #131 and labscript-suite #106, which raise component
pins and are held for the release sequence (`RELEASE-PLAN.md` section 5). Later on
2026-10-17: qtutils #36 and #37 and desktop-app #34 (release sequence steps 2 and 3),
workflow-sandbox #47 and the twelve sync PRs for defect D7 were merged, as were
labscript-c-extensions #13 (item 19, closes runviewer #13). labscript-utils #133 and
labscript #128 are open. On 2026-10-18: runmanager #134, blacs #128, lyse #145 and
labscript-devices #153, the issue fixes for release sequence steps 7 to 11; all four are
open.

The scheme rename needs setuptools_scm 10, which introduced the name
`semver-pep440-release-branch` (setuptools_scm 9.2.2 does not have it); the default
conda channel and conda-forge both have 10.3.4. Both names give the same version: `3.5.0.dev41` on labscript-utils master.
rpanderson/workflow-sandbox still uses `release-branch-semver`; that is part of the
workflow sync (release plan 4.1 item 5).

## Recording further work

When a fix is merged, add a row to the repository state table, mark the item in `REVIEW.md`
as item 20 is marked, and update the status table above. When a refactor moves code, add a
line-reference table like the runmanager one so that the `REVIEW.md` text stays usable.
