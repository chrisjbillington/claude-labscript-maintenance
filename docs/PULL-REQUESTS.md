# Pull requests opened by the maintenance track

Every pull request opened from this repository, with its state. A session that opens,
updates or sees one merged or closed updates the row. Links go to GitHub.

## Open

| Opened | Pull request | Change | Addresses |
|---|---|---|---|
| 2026-10-17 | [labscript-c-extensions #13](https://github.com/labscript-suite/labscript-c-extensions/pull/13) | `resample.pyx`: NaN lead-in stops at the group containing the first data point; bounds on the lead-in and skip-ahead loops (head d80a2a8) | runviewer #13; REVIEW.md item 19; release sequence step 4 |
| 2026-10-17 | [desktop-app #34](https://github.com/chrisjbillington/desktop-app/pull/34) | pywin32 and `wineventhook` imported inside the functions in `windows.py` (head ec3d9da) | desktop-app #20; release sequence step 3 |
| 2026-10-17 | [qtutils #36](https://github.com/philipstarkey/qtutils/pull/36) | "Clear output" context-menu action and `OutputBox.clear_output()`; CHANGELOG entry (head 3d0cad3). Context-menu part of PR #32, author co-credited; comment left on #32 | qtutils #2, PR #32; release sequence step 2 |
| 2026-10-17 | [qtutils #37](https://github.com/philipstarkey/qtutils/pull/37) | `readthedocs.yaml` unshallows and fetches tags before install; `recommonmark` dropped from the docs extra (head e507f36) | qtutils #22; release sequence step 2 |
| 2026-10-17 | [runmanager #131](https://github.com/labscript-suite/runmanager/pull/131) | same, plus `labscript>=3.5.0rc1` and `labscript_utils>=3.5.0rc1` (head e5283ab); held until the release sequence, merge immediately before the runmanager tag | release plan 4.1 item 6; release sequence step 7 |
| 2026-10-17 | [labscript-suite #106](https://github.com/labscript-suite/labscript-suite/pull/106) | same, plus the component pins of the 3.4.0 release set in the form `>=x.y.0rc1` (head 4e7de5e); held until the release sequence, merge immediately before the labscript-suite tag | release plan 4.1 item 6; release sequence step 12 |
| 2026-10-17 | [lyse #142](https://github.com/labscript-suite/lyse/pull/142) | `__getattr__` serves `spinning_top` as well as `path` from `lyse.utils.worker`; `spinning_top` back in `__all__` | DEFECTS.md D8 |
| 2026-10-17 | [workflow-sandbox #47](https://github.com/rpanderson/workflow-sandbox/pull/47) | release workflow: `shell: bash` on both "Ignore tags other than the pushed tag" steps (7df7261) | DEFECTS.md D7; labscript-suite #56 |
| 2026-10-17 | [labscript #127](https://github.com/labscript-suite/labscript/pull/127) | sync `release.yml` with workflow-sandbox 7df7261 (the head of #47) | DEFECTS.md D7 |
| 2026-10-17 | [labscript-devices #152](https://github.com/labscript-suite/labscript-devices/pull/152) | same | DEFECTS.md D7 |
| 2026-10-17 | [labscript-utils #132](https://github.com/labscript-suite/labscript-utils/pull/132) | same | DEFECTS.md D7 |
| 2026-10-17 | [blacs #127](https://github.com/labscript-suite/blacs/pull/127) | same | DEFECTS.md D7 |
| 2026-10-17 | [lyse #143](https://github.com/labscript-suite/lyse/pull/143) | same | DEFECTS.md D7 |
| 2026-10-17 | [runmanager #133](https://github.com/labscript-suite/runmanager/pull/133) | same | DEFECTS.md D7 |
| 2026-10-17 | [runviewer #75](https://github.com/labscript-suite/runviewer/pull/75) | same | DEFECTS.md D7 |
| 2026-10-17 | [labscript-suite #108](https://github.com/labscript-suite/labscript-suite/pull/108) | same | DEFECTS.md D7 |
| 2026-10-17 | [labscript-c-extensions #12](https://github.com/labscript-suite/labscript-c-extensions/pull/12) | same | DEFECTS.md D7 |
| 2026-10-17 | [desktop-app #33](https://github.com/chrisjbillington/desktop-app/pull/33) | same | DEFECTS.md D7 |
| 2026-10-17 | [qtutils #35](https://github.com/philipstarkey/qtutils/pull/35) | same | DEFECTS.md D7 |
| 2026-10-17 | [labscript-utils #133](https://github.com/labscript-suite/labscript-utils/pull/133) | `h5_lock.File` default mode `'r'`, kill lock released on zlock failure, locks released once; `setup_logging` with `sys.stdout` None; `excepthook` without tkinter; `aom.py` numpy imports; `labscript-profile-create` writes `runmanager.ini` (head 12f86ac) | REVIEW.md items 10 and 18, labscript-utils B16; blacs #100; labscript-utils #60; DEFECTS.md D3; release sequence step 5 |
| 2026-10-17 | [labscript #128](https://github.com/labscript-suite/labscript/pull/128) | ramp tick count rounding; clock-limit checks with tolerance; collision errors name the outputs; every ramp checked for collisions; the "too soon before a trigger" check; output limits with tolerance and values in the error; duplicate connections rejected; device name check; static outputs and shutters at `t0`; `StaticDDS` gate; `DDS.pulse`; parentless `TriggerableDevice`; script encoding; error paths (head 4549021) | REVIEW.md items 6, 7, 8 and labscript B1, B2, B4, B5 (part), B6, B7, B9, B10, B11 (part); labscript #16, #43, #52; release sequence step 6 |

## Merged or closed

| Opened | State | Pull request | Change | Addresses |
|---|---|---|---|---|
| 2026-10-17 | merged 2026-10-17 11:30 UTC, f5f4685 | [zprocess #31](https://github.com/chrisjbillington/zprocess/pull/31) | same; tagged `v2.28.0rc2`, which built 2.28.0rc2 on Windows | DEFECTS.md D7 |
| 2026-10-17 | merged 2026-10-17 08:27 UTC, ede3584 | [labscript #124](https://github.com/labscript-suite/labscript/pull/124) | `'a256'` to `'S256'` in `labscript.py`, `outputs.py` and the docs' intermediate device example (head c6055a0) | labscript #123; review Part 1 item 1 |
| 2026-10-17 | merged 2026-10-17 08:27 UTC, c023465 | [labscript-utils #129](https://github.com/labscript-suite/labscript-utils/pull/129) | ModuleWatcher unloads namespace packages under userlib; `__init__.py` in the default profile's `example_apparatus` directories | labscript-utils #28 |
| 2026-10-17 | merged 2026-10-17 08:28 UTC, 665a73d | [labscript #125](https://github.com/labscript-suite/labscript/pull/125) | `requires-python >= 3.11`, classifiers, `semver-pep440-release-branch`, `setuptools_scm>=10`, no `importlib_metadata` fallback | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:28 UTC, 89457f5 | [labscript-utils #130](https://github.com/labscript-suite/labscript-utils/pull/130) | same, also in `versions.py` | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:20 UTC, e3fb720 | [workflow-sandbox #46](https://github.com/rpanderson/workflow-sandbox/pull/46) | release workflow: delete every local tag at HEAD except the pushed one before computing the version; `action-gh-release` v3 | labscript-suite #56; release plan 4.1 item 4 |
| 2026-10-17 | merged 2026-10-17 08:20 UTC, 08483e9 | [labscript #126](https://github.com/labscript-suite/labscript/pull/126) | sync `release.yml` with workflow-sandbox 6f21e86 (the head of #46): `windows-2022`, `macos-15-intel`, `setup-miniconda` v4, `verbose`/`skip-existing`, tag step, `gh-release` v3 | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:20 UTC, 76fb778 | [labscript-utils #131](https://github.com/labscript-suite/labscript-utils/pull/131) | same | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:25 UTC, 9a80772 | [labscript-devices #151](https://github.com/labscript-suite/labscript-devices/pull/151) | same | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:21 UTC, 68a243d | [blacs #126](https://github.com/labscript-suite/blacs/pull/126) | same | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:25 UTC, dff7ba6 | [lyse #141](https://github.com/labscript-suite/lyse/pull/141) | same | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:21 UTC, 264434c | [runmanager #132](https://github.com/labscript-suite/runmanager/pull/132) | same | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:24 UTC, 666fd25 | [runviewer #74](https://github.com/labscript-suite/runviewer/pull/74) | same | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:24 UTC, 4fbc7fc | [labscript-suite #107](https://github.com/labscript-suite/labscript-suite/pull/107) | same | labscript-suite #56; release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:24 UTC, d72e599 | [labscript-c-extensions #11](https://github.com/labscript-suite/labscript-c-extensions/pull/11) | sync `release.yml`: tag step and `gh-release` v3 only (was already at sandbox 6f9346a) | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:24 UTC, 1b38a59 | [zprocess #30](https://github.com/chrisjbillington/zprocess/pull/30) | sync `release.yml`: `windows-2022`, `setup-miniconda` v4, tag step, `gh-release` v3 | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:24 UTC, 7933d77 | [desktop-app #32](https://github.com/chrisjbillington/desktop-app/pull/32) | sync `release.yml`: tag step and `gh-release` v3 only | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:24 UTC, 0f06616 | [qtutils #34](https://github.com/philipstarkey/qtutils/pull/34) | sync `release.yml`: all action pins (checkout v6, setup-python v6, upload-artifact v6, download-artifact v8, setup-miniconda v4, gh-release v3), runner labels, tag step | release plan 4.1 item 5 |
| 2026-10-17 | merged 2026-10-17 08:33 UTC, 41c0058 | [labscript-c-extensions #10](https://github.com/labscript-suite/labscript-c-extensions/pull/10) | `requires-python`, classifiers, no `importlib_metadata` fallback (`guess-next-dev` kept) | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:33 UTC, 526726f | [zprocess #29](https://github.com/chrisjbillington/zprocess/pull/29) | `requires-python`, classifiers, scheme name, `setuptools_scm>=10` | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:33 UTC, dc6be4e | [desktop-app #31](https://github.com/chrisjbillington/desktop-app/pull/31) | `requires-python`, classifiers, no `importlib_metadata` fallback in `fix_entry_points.py` and `environment.py` | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:32 UTC, 4c9cd95 | [qtutils #33](https://github.com/philipstarkey/qtutils/pull/33) | `requires-python`, classifiers, scheme name, `setuptools_scm>=10` | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:39 UTC, 25f75fb | [labscript-devices #149](https://github.com/labscript-suite/labscript-devices/pull/149) | `'a256'` to `'S256'` in six device files; `tostring()` to `tobytes()` in `LightCrafterDMD.py`; verified by import and the dummy-device compile only, as the description says | labscript #123; labscript-devices #131; review Part 1 item 1 |
| 2026-10-17 | merged 2026-10-17 08:40 UTC, 73ec9d2 | [blacs #124](https://github.com/labscript-suite/blacs/pull/124) | `'a'` aliases to `'S'` in `front_panel_settings.py` | labscript #123; review Part 1 item 1 |
| 2026-10-17 | merged 2026-10-17 08:36 UTC, e74b638 | [zprocess #28](https://github.com/chrisjbillington/zprocess/pull/28) | guard `SetConsoleMode` in `disable_quick_edit`; head 256ac43 names the PowerShell console mode as the cause (tested on Windows 11, `TESTING.md`) | zprocess #27 |
| 2026-10-17 | merged 2026-10-17 08:40 UTC, 2183314 | [labscript-devices #150](https://github.com/labscript-suite/labscript-devices/pull/150) | same | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:44 UTC, bc3fd1f | [blacs #125](https://github.com/labscript-suite/blacs/pull/125) | same | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:44 UTC, 01246cf | [lyse #140](https://github.com/labscript-suite/lyse/pull/140) | same | release plan 4.1 item 6 |
| 2026-10-17 | merged 2026-10-17 08:43 UTC, 7ea7dc9 | [runviewer #73](https://github.com/labscript-suite/runviewer/pull/73) | same | release plan 4.1 item 6 |
