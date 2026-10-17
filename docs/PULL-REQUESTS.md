# Pull requests opened by the maintenance track

Every pull request opened from this repository, with its state. A session that opens,
updates or sees one merged or closed updates the row. Links go to GitHub.

## Open

| Opened | Pull request | Change | Addresses |
|---|---|---|---|
| 2026-10-17 | [runmanager #131](https://github.com/labscript-suite/runmanager/pull/131) | same, plus `labscript>=3.5.0rc1` and `labscript_utils>=3.5.0rc1` (head e5283ab); held until the release sequence, merge immediately before the runmanager tag | release plan 4.1 item 6; release sequence step 7 |
| 2026-10-17 | [labscript-suite #106](https://github.com/labscript-suite/labscript-suite/pull/106) | same, plus the component pins of the 3.4.0 release set in the form `>=x.y.0rc1` (head 4e7de5e); held until the release sequence, merge immediately before the labscript-suite tag | release plan 4.1 item 6; release sequence step 12 |
| 2026-10-17 | [lyse #142](https://github.com/labscript-suite/lyse/pull/142) | `__getattr__` serves `spinning_top` as well as `path` from `lyse.utils.worker`; `spinning_top` back in `__all__` | DEFECTS.md D8 |

## Merged or closed

| Opened | State | Pull request | Change | Addresses |
|---|---|---|---|---|
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
