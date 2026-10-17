# Pull requests opened by the maintenance track

Every pull request opened from this repository, with its state. A session that opens,
updates or sees one merged or closed updates the row. Links go to GitHub.

## Open

| Opened | Pull request | Change | Addresses |
|---|---|---|---|
| 2026-10-17 | [labscript #124](https://github.com/labscript-suite/labscript/pull/124) | `'a256'` to `'S256'` in `labscript.py` and `outputs.py` | labscript #123; review Part 1 item 1 |
| 2026-10-17 | [labscript-devices #149](https://github.com/labscript-suite/labscript-devices/pull/149) | `'a256'` to `'S256'` in six device files; `tostring()` to `tobytes()` in `LightCrafterDMD.py` | labscript #123; labscript-devices #131; review Part 1 item 1 |
| 2026-10-17 | [blacs #124](https://github.com/labscript-suite/blacs/pull/124) | `'a'` aliases to `'S'` in `front_panel_settings.py` | labscript #123; review Part 1 item 1 |
| 2026-10-17 | [zprocess #28](https://github.com/chrisjbillington/zprocess/pull/28) | guard `SetConsoleMode` in `disable_quick_edit`; head 256ac43 names the PowerShell console mode as the cause (tested on Windows 11, `TESTING.md`) | zprocess #27 |
| 2026-10-17 | [labscript-utils #129](https://github.com/labscript-suite/labscript-utils/pull/129) | ModuleWatcher unloads namespace packages under userlib; `__init__.py` in the default profile's `example_apparatus` directories | labscript-utils #28 |
| 2026-10-17 | [labscript #125](https://github.com/labscript-suite/labscript/pull/125) | `requires-python >= 3.11`, classifiers, `semver-pep440-release-branch`, `setuptools_scm>=10`, no `importlib_metadata` fallback | release plan 4.1 item 6 |
| 2026-10-17 | [labscript-utils #130](https://github.com/labscript-suite/labscript-utils/pull/130) | same, also in `versions.py` | release plan 4.1 item 6 |
| 2026-10-17 | [labscript-devices #150](https://github.com/labscript-suite/labscript-devices/pull/150) | same | release plan 4.1 item 6 |
| 2026-10-17 | [blacs #125](https://github.com/labscript-suite/blacs/pull/125) | same | release plan 4.1 item 6 |
| 2026-10-17 | [lyse #140](https://github.com/labscript-suite/lyse/pull/140) | same | release plan 4.1 item 6 |
| 2026-10-17 | [runmanager #131](https://github.com/labscript-suite/runmanager/pull/131) | same, plus `labscript>=3.5.0` and `labscript_utils>=3.5.0` | release plan 4.1 item 6 |
| 2026-10-17 | [runviewer #73](https://github.com/labscript-suite/runviewer/pull/73) | same | release plan 4.1 item 6 |
| 2026-10-17 | [labscript-suite #106](https://github.com/labscript-suite/labscript-suite/pull/106) | same, plus the component pins of the 3.4.0 release set; merge last | release plan 4.1 item 6 |
| 2026-10-17 | [labscript-c-extensions #10](https://github.com/labscript-suite/labscript-c-extensions/pull/10) | `requires-python`, classifiers, no `importlib_metadata` fallback (`guess-next-dev` kept) | release plan 4.1 item 6 |
| 2026-10-17 | [zprocess #29](https://github.com/chrisjbillington/zprocess/pull/29) | `requires-python`, classifiers, scheme name, `setuptools_scm>=10` | release plan 4.1 item 6 |
| 2026-10-17 | [desktop-app #31](https://github.com/chrisjbillington/desktop-app/pull/31) | `requires-python`, classifiers, no `importlib_metadata` fallback in `fix_entry_points.py` and `environment.py` | release plan 4.1 item 6 |
| 2026-10-17 | [qtutils #33](https://github.com/philipstarkey/qtutils/pull/33) | `requires-python`, classifiers, scheme name, `setuptools_scm>=10` | release plan 4.1 item 6 |
| 2026-10-17 | [workflow-sandbox #46](https://github.com/rpanderson/workflow-sandbox/pull/46) | release workflow: delete every local tag at HEAD except the pushed one before computing the version; `action-gh-release` v3 | labscript-suite #56; release plan 4.1 item 4 |
| 2026-10-17 | [labscript #126](https://github.com/labscript-suite/labscript/pull/126) | sync `release.yml` with workflow-sandbox 6f21e86 (the head of #46): `windows-2022`, `macos-15-intel`, `setup-miniconda` v4, `verbose`/`skip-existing`, tag step, `gh-release` v3 | release plan 4.1 item 5 |
| 2026-10-17 | [labscript-utils #131](https://github.com/labscript-suite/labscript-utils/pull/131) | same | release plan 4.1 item 5 |
| 2026-10-17 | [labscript-devices #151](https://github.com/labscript-suite/labscript-devices/pull/151) | same | release plan 4.1 item 5 |
| 2026-10-17 | [blacs #126](https://github.com/labscript-suite/blacs/pull/126) | same | release plan 4.1 item 5 |
| 2026-10-17 | [lyse #141](https://github.com/labscript-suite/lyse/pull/141) | same | release plan 4.1 item 5 |
| 2026-10-17 | [runmanager #132](https://github.com/labscript-suite/runmanager/pull/132) | same | release plan 4.1 item 5 |
| 2026-10-17 | [runviewer #74](https://github.com/labscript-suite/runviewer/pull/74) | same | release plan 4.1 item 5 |
| 2026-10-17 | [labscript-suite #107](https://github.com/labscript-suite/labscript-suite/pull/107) | same | labscript-suite #56; release plan 4.1 item 5 |
| 2026-10-17 | [labscript-c-extensions #11](https://github.com/labscript-suite/labscript-c-extensions/pull/11) | sync `release.yml`: tag step and `gh-release` v3 only (was already at sandbox 6f9346a) | release plan 4.1 item 5 |
| 2026-10-17 | [zprocess #30](https://github.com/chrisjbillington/zprocess/pull/30) | sync `release.yml`: `windows-2022`, `setup-miniconda` v4, tag step, `gh-release` v3 | release plan 4.1 item 5 |
| 2026-10-17 | [desktop-app #32](https://github.com/chrisjbillington/desktop-app/pull/32) | sync `release.yml`: tag step and `gh-release` v3 only | release plan 4.1 item 5 |
| 2026-10-17 | [qtutils #34](https://github.com/philipstarkey/qtutils/pull/34) | sync `release.yml`: all action pins (checkout v6, setup-python v6, upload-artifact v6, download-artifact v8, setup-miniconda v4, gh-release v3), runner labels, tag step | release plan 4.1 item 5 |

## Merged or closed

None yet.
