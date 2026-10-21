# Open issues across the labscript suite, triaged 2026-10-17

Scope: all 223 open issues on the labscript-suite organisation repos (labscript 34,
labscript-utils 18, labscript-devices 28, blacs 33, lyse 25, runmanager 29, runviewer 13,
labscript-suite 20, PrawnBlaster 2, prawn_digital_output 5, mise 1, bias 1) and on the
related repos under chrisjbillington (zprocess 7, desktop-app 4, setuptools-conda 3) and
philipstarkey/qtutils (3 issues and PR #32). The remaining repos have no open issues.

Each issue was read with its full comment thread, and every bug was checked against the
current default branch (file:line in the detailed reports). Open PRs are covered in
PR-REVIEW.md. Importance: 5 = fix before the next release, 1 = close.

| Importance | Count |
|---|---|
| 5 | 2 |
| 4 | 14 |
| 3 | 36 |
| 2 | 80 |
| 1 | 92 |

Status 2026-10-18: 36 of these issues are closed, each fixed by a merged pull request of
the maintenance track (the rows say which); 190 remain open. No issue or pull request
has been opened on these repositories since 2026-10-16 except by the maintenance track.

About 95 issues can be closed outright (fixed, obsolete, answered, duplicate, or
abandoned by agreement); the per-repo tables in section 3 give the reason for each.

## 1. Ranked list

| # | Issue | Type | Imp. | Action |
|---|---|---|---|---|
| 1 | labscript #123 'a256' dtype fails on NumPy >= 2.5 | bug | 5 | Fixed 2026-10-17 by labscript #124, labscript-devices #149 and blacs #124; issue closed. Add NumPy 2.5 to CI |
| 2 | zprocess #27 `disable_quick_edit` crash on ConPTY | bug (crash, Windows 11) | 5 | fixed 2026-10-17 by zprocess #28; issue closed; needs zprocess 2.28.0 |
| 3 | blacs #46 queue thread dies when the shot file cannot be written | bug | 4 | fixed in blacs #128 (merged 2026-10-18), with #29; issue closed |
| 4 | blacs #29 crash on shared drive becoming unavailable | bug | 4 | fixed in blacs #128 (merged 2026-10-18), with #46; issue closed |
| 5 | blacs #52 lost window after compile and restart | bug | 4 | fixed in blacs #128 (merged 2026-10-18), with #56; issue closed |
| 6 | desktop-app #20 launcher imports pywin32 before activating the env | bug | 4 | fixed in desktop-app #34 (merged 2026-10-17); issue closed |
| 7 | labscript-devices #109 PrawnBlaster runviewer drops instruction after wait | bug | 4 | fixed in labscript-devices #153 (merged 2026-10-18); issue closed |
| 8 | labscript-devices #131 NumPy 2 `np.string_` | bug | 4 | close as fixed; the `LightCrafterDMD.py` `tostring()` fix merged 2026-10-17 in labscript-devices #149; issue closed |
| 9 | labscript #104 remove pylab star import | feature/compat | 4 | fixed in labscript #130 (opened 2026-10-18): star import removed with no re-exports; listed at the top of the release notes (maintainer decision 2026-10-18) |
| 10 | labscript #52 duplicate output connection is silent | bug | 4 | fixed in labscript #128 (merged 2026-10-18); issue closed |
| 11 | labscript #43 collision errors do not name outputs | feature | 4 | fixed in labscript #128 (merged 2026-10-18); issue closed |
| 12 | labscript #41 no test suite | tooling | 4 | Fix for next release at smoke-test level |
| 13 | zprocess #19 `curve_keypair` Not supported on conda Windows | bug (upstream) + diagnostics/docs | 4 | fixed in zprocess #32 (merged 2026-10-18): clear error naming the pyzmq source, README Security section; the installation docs note is still to do; issue closed |
| 14 | runmanager #66 preparse memory blow-up counting shots | bug | 4 | fixed in runmanager #134 (merged 2026-10-18); issue closed |
| 15 | runmanager #123 set_globals comment preservation with raw=True | bug | 4 | fixed in runmanager #134 (merged 2026-10-18); the offered PR was not used; issue closed |
| 16 | labscript-suite #56 release workflow with rc + final tag on one commit | tooling | 4 | fixed 2026-10-17: workflow-sandbox #46 and the sync PR on each of the twelve repos merged; issue closed |
| 17 | blacs #56 window geometry restoration | bug | 3 | fixed in blacs #128 (merged 2026-10-18), with #52; issue closed |
| 18 | blacs #100 setup_logging crashes when sys.stdout is None | bug | 3 | fixed in labscript-utils #133 (merged 2026-10-18); issue closed |
| 19 | blacs #49 StopIteration before first yield gives fatal error | bug | 3 | fixed in blacs #129 (merged 2026-10-18); issue closed |
| 20 | blacs #32 report which device paused the queue | feature | 3 | fixed in blacs #129 (merged 2026-10-18); issue closed |
| 21 | blacs #7 file dialogs default to "C:\\" | feature | 3 | fixed in blacs #129 (merged 2026-10-18); issue closed |
| 22 | blacs #72 default lyse host localhost, analysis on | feature | 3 | fixed in blacs #129 (merged 2026-10-18); issue closed |
| 23 | blacs #12 compile dialog unclosable when compiler child dies | bug | 3 | fix via runmanager #35 (refactor in progress), else later |
| 24 | blacs #54 remote worker version check | feature | 3 | fix later; no longer tied to zprocess #14, since zprocess #33 negotiates the socket type |
| 25 | labscript-devices #79 ESRPro500 missing runviewer parser, 21 vs 24 flags | bug | 3 | fixed in labscript-devices #153 (merged 2026-10-18): parser added and all 24 flags exposed; no short-pulse timing feature; issue closed |
| 26 | labscript-devices #49 declare missing dependencies | tooling | 3 | fix for next release (per-device extras) |
| 27 | labscript-devices #104 project structure / per-device deps | meta | 3 | leave open; extras in release |
| 28 | labscript-devices #117 PrawnBlaster triggered from a clockline | feature | 3 | fix later (PrawnDO pattern) |
| 29 | labscript-devices #68 manual-mode-only camera attributes | bug | 3 | fix later, on top of #148 |
| 30 | PrawnBlaster #34 200 MHz clock | feature | 3 | fix later via PR #37 + host change |
| 31 | PrawnBlaster #31 uneven instruction split | feature | 3 | fix later via PR #35 rework |
| 32 | labscript #16 ramp limit check has no tolerance | bug | 3 | fixed in labscript #128 (merged 2026-10-18); issue closed |
| 33 | labscript-utils #60 runmanager.ini in default profile | feature | 3 | fixed in labscript-utils #133 (merged 2026-10-18); issue closed |
| 34 | labscript-utils #116 minimal analysis example | docs | 3 | Merge PR #117, close |
| 35 | labscript #50 wait_delay not applied to resume trigger | bug | 3 | Fix later; ask labs with secondary PulseBlasters |
| 36 | labscript #44 limits not saved for BLACS | feature | 3 | Fix later (labscript half with #16) |
| 37 | lyse #14 multishot runs while paused | bug | 3 | fixed in lyse #145 (merged 2026-10-18); issue closed |
| 38 | lyse #90 dict results flattened inconsistently | bug | 3 | fixed in lyse #145 (merged 2026-10-18); issue closed |
| 39 | lyse #139 serial subprocess start-up | bug (performance) | 3 | fixed in lyse #145 (merged 2026-10-18); issue closed |
| 40 | runviewer #13 pulses at t=0 dropped by resampler | bug (in labscript-c-extensions) | 3 | fixed in labscript-c-extensions #13 (merged 2026-10-17); issue closed |
| 41 | runmanager #33 abort only stops current sequence | bug | 3 | fixed in runmanager #134 (merged 2026-10-18); issue closed |
| 42 | runmanager #30 no header between shot compilations | bug | 3 | fixed in runmanager #134 (merged 2026-10-18); issue closed |
| 43 | runmanager #26 .h5 not appended (Linux) | bug | 3 | fixed in runmanager #134 (merged 2026-10-18); issue closed |
| 44 | labscript-suite #5 apparatus name must be identifier | docs/tooling | 3 | fixed in labscript-utils #134 (validation in `labscript-profile-create`) and labscript-suite #109 (docs), both merged 2026-10-18; issue closed |
| 45 | labscript-suite #60 CITATION.cff in component repos | docs | 3 | leave open, not for this release (maintainer decision 2026-10-18) |
| 46 | runmanager #97 remote is_compiling | feature | 3 | fix for next release if cheap |
| 47 | runmanager #41 save window geometry | feature | 3 | fix later |
| 48 | runmanager #50 expansion types rewritten on restart | bug | 3 | fix later (mitigate with #66) |
| 49 | runmanager #35 async compile hangs if worker dies | bug | 3 | fix later |
| 50 | runmanager #45 compile progress / per-sequence abort | feature | 3 | fix later; merge abort part into #33 |
| 51 | labscript-suite #105 uv install docs | docs | 3 | convert to docs |
| 52 | labscript-suite #23 end-to-end test | tooling | 3 | leave open; ask Json-To-String/dihm for status |
| 53 | blacs #58 final values for custom-UI tabs | feature | 2 | fix later |
| 54 | blacs #40 state machine defaults and errors | feature | 2 | fix later |
| 55 | blacs #31 graceful worker shutdown on restart | feature | 2 | fix later |
| 56 | blacs #50 report loaded/failed plugins | feature | 2 | fix later (after PR #123) |
| 57 | blacs #41 plugin base classes | feature | 2 | fix later |
| 58 | blacs #97 widget sizing on startup | bug | 2 | fix later; re-test on Qt6 |
| 59 | blacs #19 documentation out of date | docs | 2 | convert to docs task (delete stale files) |
| 60 | blacs #33 output limits from connection table | feature | 2 | leave open, blocked on labscript #44 |
| 61 | blacs #92 slow transition to buffered | performance | 2 | leave open (rewrite reference) |
| 62 | blacs #53 pipelining / cycle time design | design | 2 | leave open (rewrite design record) |
| 63 | blacs #24 remote control API | feature | 2 | leave open (rewrite) |
| 64 | blacs #23 analog input display | feature | 2 | leave open (rewrite) |
| 65 | blacs #116 real-time input display | feature | 2 | leave open (rewrite) |
| 66 | blacs #13 secondary control system | feature | 2 | leave open (remote workers done; GUIs not) |
| 67 | desktop-app #17 customise .desktop file | feature | 2 | fix later |
| 68 | labscript-devices #23 PulseBlaster 2323 outputs drop during programming | bug | 2 | fix later (port 4cadcff to `PulseBlaster.py`) |
| 69 | labscript-devices #91 NI-6738 per-bank AO rate | bug/docs | 2 | convert to docs |
| 70 | labscript-devices #69 TekScope as TriggerableDevice | feature | 2 | fix later (with #129) |
| 71 | labscript-devices #38 AndorSolis docstring | docs | 2 | convert to docs (via #144) |
| 72 | labscript-devices #55 mock flag for more devices | proposal | 2 | leave open |
| 73 | labscript-devices #29 save class attributes as properties | proposal | 2 | leave open (merge with #24/#30) |
| 74 | labscript-devices #30 device code versions | proposal | 2 | leave open (merge) |
| 75 | labscript-devices #24 version-tolerant connection table compare | proposal | 2 | leave open (merge) |
| 76 | labscript-devices #107 PrawnBlaster waits run to timeout | question | 2 | ask reporter, else close stale |
| 77 | labscript-devices #15 unplugged PulseBlaster | bug | 2 | fix later (`pb_count_boards` check from the thread), else close |
| 78 | prawn_digital_output #26 instruction guardrails | feature | 2 | fix later |
| 79 | prawn_digital_output #24 remove `add` | refactor | 2 | fix later |
| 80 | prawn_digital_output #25 docs | docs | 2 | fix later; merge PR #23 |
| 81 | prawn_digital_output #20 higher system clock | feature | 2 | fix later after PR #37 |
| 82 | prawn_digital_output #17 overclock build | feature | 2 | close as duplicate of #20 |
| 83 | labscript #6 clocklines coupled during ramps | feature | 2 | Leave open as canonical limitation issue |
| 84 | labscript #2 shutter reordering | bug | 2 | Close as won't fix in legacy (deferred to v3 in 2017) |
| 85 | labscript #3 shutter timing model | feature | 2 | Close; rewrite input |
| 86 | labscript #4 reject instructions before last wait | feature | 2 | Fix later; delete dead check at outputs.py:364-375 |
| 87 | labscript #10 imported connection table not re-run | bug | 2 | Fix later per 2014 plan (unload device-defining modules), or docs |
| 88 | labscript #18 in-shot analysis scripts | proposal | 2 | Close; rewrite analysis design supersedes |
| 89 | labscript #32 BLACS error policy | proposal | 2 | Close here (wrong repo) |
| 90 | labscript #34 ramp splitting | feature | 2 | Close as duplicate of #6 |
| 91 | labscript #36 safe idle state with timeout | proposal | 2 | Close; rewrite input |
| 92 | labscript #54 constant with duration | feature | 2 | Fix later or close; rewrite input |
| 93 | labscript #109 Trigger ignores `inverted` | bug | 2 | Fix later (error when both given) |
| 94 | labscript-utils #20 shared "open external program" helper | feature | 2 | Fix later |
| 95 | labscript-utils #29 macOS autostart (fork in GUI process) | bug | 2 | Fix later in zprocess, needs macOS tester |
| 96 | labscript-utils #104 excepthook uses Tk | question | 2 | Close as answered; optional stderr fallback |
| 97 | labscript #112 timing limited by slow component | support | 2 | Convert to docs (gated clocks page), close |
| 98 | qtutils #22 RTD version string | tooling | 2 | fixed in qtutils #37 (merged 2026-10-17); issue closed |
| 99 | qtutils #31 PyQt6 aliases tracker | meta | 2 | closed 2026-10-21; the dead `exec()` alias branch is removed in qtutils #40 |
| 100 | qtutils #2 / PR #32 clear output box | feature | 2 | fixed in qtutils #36 (merged 2026-10-17) (context-menu part of #32, author credited); issue closed |
| 101 | lyse #35 persist hidden columns | feature | 2 | fix later |
| 102 | lyse #41 plot window size | bug | 2 | fix later |
| 103 | lyse #53 get_image argument names | API | 2 | fix later |
| 104 | lyse #4 multishot before all single-shots | feature | 2 | fix later |
| 105 | lyse #7 save scripts in shot file | feature | 2 | fix later |
| 106 | lyse #84 logging | feature | 2 | leave open |
| 107 | lyse #32 second instance | feature | 2 | leave open |
| 108 | lyse #123 datasets in dataframe | feature/question | 2 | reply, close as won't fix |
| 109 | lyse #26 image cache | feature | 2 | close as stale or leave open |
| 110 | lyse #6 analysis globals | feature | 2 | leave open (successor has it) |
| 111 | runviewer #47 slice before resample | performance | 2 | fix later (with #13) |
| 112 | runviewer #45 progress indicator | feature | 2 | fix later |
| 113 | runviewer #22 units | feature | 2 | leave open |
| 114 | runviewer #14 smaller digital plots | feature | 2 | leave open, reply |
| 115 | runviewer #17 line numbers per instruction | feature | 2 | close for legacy; rewrite requirement |
| 116 | setuptools-conda #26 free-threaded python deps | feature | 2 | leave open (wait for upstream) |
| 117 | runmanager #60 API lacks zip-group guessing | bug | 2 | leave open |
| 118 | runmanager #54 labscript file not cached per sequence | bug | 2 | fix later |
| 119 | runmanager #52 file checkbox after group deletion | bug | 2 | fix later |
| 120 | runmanager #34 tabs can be moved before fixed tabs | bug | 2 | fix later |
| 121 | runmanager #23 cursor at end on edit | bug | 2 | fix later |
| 122 | runmanager #13 missing units attr leaves orphan tab | bug | 2 | fix later |
| 123 | runmanager #28 unit conversions whitelisted by ModuleWatcher | bug | 2 | fix later (labscript star import) |
| 124 | runmanager #48 continuous engage / compile queue | feature | 2 | leave open (or fold into new compile-queue issue) |
| 125 | runmanager #46 engage log | feature | 2 | leave open |
| 126 | runmanager #37 favourite globals | feature | 2 | leave open |
| 127 | runmanager #27 explicit save of globals | feature | 2 | leave open |
| 128 | runmanager #44 arrow-key value stepping | feature | 2 | close as won't fix |
| 129 | labscript-suite #59 add git to conda install line | docs | 2 | fixed in labscript-suite #109 (merged 2026-10-18); issue closed |
| 130 | labscript-suite #26 copyright headers | meta | 2 | fix for next release if cheap ("Monash University and contributors"), else later |
| 131 | labscript-suite #103 headless/scriptable components | feature | 2 | close for legacy, pointer to rewrite |
| 132 | labscript-suite #6 editor/hdfview in docs | docs | 2 | convert to docs |
| 133 | blacs #57 stylesheet not applied on launch (PyQt 5.13) | bug | 1 | close as obsolete after a Qt6 launch check |
| 134 | blacs #45 startup with deleted queued shots | bug | 1 | close as stale (never reproduced; guard experiment_queue.py:390) |
| 135 | blacs #55 abort during cycle_time delay | bug | 1 | close as fixed (reporter-confirmed 2021) |
| 136 | blacs #15 per-device error-state check cost | performance | 1 | close as stale |
| 137 | blacs #115 better tab arrangement | feature | 1 | leave open as rewrite requirement or close as vague |
| 138 | blacs #4 check labscript version of connection table | feature | 1 | close as won't fix (rewrite requirement) |
| 139 | blacs #27 plugin tabs | feature | 1 | close as fixed (5ba525f) |
| 140 | blacs #5 AppID after compile and restart | bug | 1 | close as fixed (b296deb) |
| 141 | desktop-app #18 GUI entry point does nothing | support | 1 | close as stale |
| 142 | desktop-app #14 selective entry-point fixing | feature | 1 | close as fixed (af652ad) |
| 143 | labscript-devices #66 TekScope `/data/traces` collision | bug | 1 | close as fixed (259ea85) |
| 144 | labscript-devices #31 imaqdx server model assumptions | bug | 1 | close as fixed (IMAQdxCamera implements the agreed option) |
| 145 | labscript-devices #124 NovaTech TS/pin 10 | question | 1 | close (answered by philipstarkey; docs pointer) |
| 146 | labscript-devices #22 third-party devices | proposal | 1 | close as superseded |
| 147 | labscript-devices #6 one folder per device | proposal | 1 | close as done |
| 148 | labscript-devices #14 NI 6733 needs 2 samples | bug | 1 | close as obsolete |
| 149 | labscript-devices #39 Zaber not homed | enhancement | 1 | close as stale |
| 150 | labscript-devices #13 PulseBlaster DDS ramps | feature | 1 | close as won't fix |
| 151 | labscript-devices #100 PyCapture2 bus failure | question | 1 | close with diagnosis (string serial number) |
| 152 | labscript-devices #8 DDS shape error | question | 1 | close as resolved in thread (2014) |
| 153 | labscript-devices #2 RFBlaster minimum frequency | bug | 1 | close as won't fix |
| 154 | labscript #5 instruction time tolerance | feature | 1 | Close |
| 155 | labscript #7 nested loops | feature | 1 | Close |
| 156 | labscript #11 builtins injection | feature | 1 | Close as won't fix (decided 2014) |
| 157 | labscript #15 empty connection table | bug | 1 | Close as fixed after one compile check |
| 158 | labscript #21 live in-shot feedback | proposal | 1 | Close |
| 159 | labscript #39 short ticks during ramps | bug | 1 | Close as fixed (a9888d5) |
| 160 | labscript #42 loop recognition | feature | 1 | Close as answered (`repeat_pulse_sequence`) |
| 161 | labscript #45 restructure properties/BLACS_connection | proposal | 1 | Close |
| 162 | labscript #49 set_passed_properties on outputs | feature | 1 | Close as stale |
| 163 | labscript #53 pseudoclock/clockline collision | support | 1 | Close as fixed by a9888d5, link #6/#43 |
| 164 | labscript #96 NI 6535 PFI4 impedance | support | 1 | Close as resolved (reporter confirmed) |
| 165 | labscript #105 type hints | feature | 1 | Close or leave open low priority |
| 166 | labscript #108 integer times | design | 1 | Close; rewrite uses Fractions |
| 167 | labscript-utils #2 labconfig initialisation | feature | 1 | Close as fixed by labscript-profile-create |
| 168 | labscript-utils #3 unitconversions location | feature | 1 | Close |
| 169 | labscript-utils #6 exec in UnitConversion | feature | 1 | Close as fixed (a3ccc40) |
| 170 | labscript-utils #7 ModuleWatcher blacklist | feature | 1 | Close as superseded |
| 171 | labscript-utils #10 check_version minimum only | feature | 1 | Close as obsolete (no callers) |
| 172 | labscript-utils #12 units inside spinbox | feature | 1 | Close or leave open |
| 173 | labscript-utils #19 flag to disable denier | feature | 1 | Close as fixed (fb78e55) |
| 174 | labscript-utils #23 ModuleWatcher whitelist | feature | 1 | Close as fixed (c3141fb) |
| 175 | labscript-utils #26 enum widget | feature | 1 | Close as fixed (5810137); larger proposal to blacs if wanted |
| 176 | labscript-utils #68 FileWatcher public attributes | cleanup | 1 | Close or fix opportunistically |
| 177 | labscript-utils #87 double import on Python 3.6 | bug | 1 | Close as obsolete |
| 178 | labscript-utils #100 `imp` removed | bug | 1 | Close as fixed (189c3cf, v3.4.0) |
| 179 | lyse #83 `.py` in group name | bug | 1 | close as fixed (5138e40) |
| 180 | lyse #44 compression kwargs | feature | 1 | close as fixed (50be460) |
| 181 | lyse #29 shot loading speed | performance | 1 | close as fixed (22219f5) |
| 182 | lyse #2 shots during multishot | bug | 1 | close as fixed (4f69e8b) |
| 183 | lyse #5 plot window geometry | feature | 1 | close as fixed (fd624b0) |
| 184 | lyse #131 lab book copy | feature | 1 | close as fixed (clipboard action exists) |
| 185 | lyse #19 fewer column levels | bug | 1 | close (not a bug) |
| 186 | lyse #25 plots after error | bug | 1 | close as stale |
| 187 | lyse #94 protocol question | question | 1 | close (answered) / docs |
| 188 | lyse #81 rename Run to Shot | meta | 1 | close as won't fix with PR #118 |
| 189 | lyse #23 root attributes | refactor | 1 | leave open or close |
| 190 | lyse #8 taskbar grouping | feature | 1 | close as won't fix |
| 191 | runviewer #44 markers dropdown | bug | 1 | close as fixed (c15fc9f) |
| 192 | runviewer #26 PyQt 5.13 plots | bug | 1 | close as obsolete |
| 193 | runviewer #16 PulseBlaster shutter markers | bug | 1 | close as fixed |
| 194 | runviewer #46 redraw on focus | bug | 1 | close as stale |
| 195 | runviewer #21 enabled checkbox column | UI | 1 | fix later or close |
| 196 | runviewer #9 channel grouping | feature | 1 | leave open or remove buttons |
| 197 | runviewer #3 rfblaster | feature | 1 | close as won't fix |
| 198 | zprocess #16 libsodium | upstream | 1 | close as duplicate of #19; the clear error in zprocess #32 (merged 2026-10-18) covers it. Left open by the maintainer on 2026-10-18 |
| 199 | zprocess #13 venv shim | bug | 1 | close as fixed (4d7a5d3) |
| 200 | zprocess #9 sphinx docs | docs | 1 | close as won't fix |
| 201 | zprocess #8 zlock callback | feature | 1 | close as won't fix |
| 202 | zprocess #6 expose ports | feature | 1 | close as won't fix |
| 203 | setuptools-conda #9 per-dependency channels | feature | 1 | close as won't fix |
| 204 | setuptools-conda #2 save recipes | feature | 1 | close as won't fix |
| 205 | runmanager #47 lazy shot-file creation | proposal | 1 | close as fixed |
| 206 | runmanager #53 ModuleWatcher reloads runmanager | bug | 1 | close as obsolete |
| 207 | runmanager #32 output box scrolling | bug | 1 | close as stale |
| 208 | runmanager #2 FingerTabBar paintEvent | bug | 1 | close as won't fix |
| 209 | runmanager #62 nested group folders | feature | 1 | close as won't fix |
| 210 | runmanager #125 per-variable history (empty) | feature | 1 | close as stale |
| 211 | runmanager #126 default case for variables | feature | 1 | ask reporter, else close |
| 212 | labscript-suite #66 WindowsError/hg TypeError | bug | 1 | close as fixed (labscript v3.3.0) |
| 213 | labscript-suite #58 missing packaging | docs | 1 | close as stale |
| 214 | labscript-suite #45 don't recommend venvs | docs | 1 | close as won't fix |
| 215 | labscript-suite #54 third-party RPC | proposal | 1 | close for legacy; rewrite design note |
| 216 | labscript-suite #22 dead code | task | 1 | close as fixed |
| 217 | labscript-suite #21 per-repo checklist | task | 1 | convert to docs or close (release notes item goes to release plan) |
| 218 | labscript-suite #20 post-install cite message | feature | 1 | close as won't fix |
| 219 | labscript-suite #18 pip install wrapper | feature | 1 | close as fixed |
| 220 | labscript-suite #104 remerge JQI | task | 1 | close as obsolete |
| 221 | labscript-suite #7 notepad++ setup | docs | 1 | close as stale |
| 222 | labscript-suite #98 goggle mode | feature | 1 | leave open or close |
| 223 | mise #1 port mise to Qt | proposal | 1 | close as won't fix; archive repo |
| 224 | bias #1 CameraBase VI docs | docs | 1 | close as obsolete; archive repo |

## 2. Release-relevant issues by repo

### labscript, labscript-utils

- labscript #123: `'a256'` dtypes fail on NumPy >= 2.5; compilation is impossible. Four sites in labscript, six files in labscript-devices. Fixed 2026-10-17 by labscript #124, labscript-devices #149 and blacs #124; issue closed.
- labscript #104: `from pylab import *` in `labscript.py` and `functions.py`; the docs build already needed `numpy<2`. Decide the compatibility policy in the Python 3.11+ release.
- labscript #41: no automated tests; a compile smoke test across the supported Python/NumPy matrix is the cheapest guard against the two items above.
- labscript #95: NumPy 2 turns the PrawnBlaster `half_period` overflow (idle clockline longer than 42 s) from a crash into silent truncation; add dtype and range check in labscript-devices. Fixed in labscript-devices #153 (merged 2026-10-18).
- labscript-utils #28: compile crashes (`KeyError: 'labscriptlib'`) after editing a file when the apparatus directory is a namespace package, which is how `labscript-profile-create` lays it out; ship `__init__.py` and fix the ModuleWatcher whitelist. Fixed by labscript-utils #129, merged 2026-10-17; issue closed.
- labscript-utils #29: zprocess `start_daemon` forks the GUI process; relevant only if macOS is a release target.
- labscript-utils #104: Tk excepthook subprocess needs `tkinter`; confirm availability on the supported Pythons or add a stderr fallback.
- labscript-utils #100: already fixed (v3.4.0); mention Python 3.12+ support in release notes.
- labscript-utils #60 and #116 (PR #117): first-run experience of the release; both small.
### labscript-devices, PrawnBlaster, prawn_digital_output

- #131: NumPy 2 camera fix is in master but unreleased; the `LightCrafterDMD.py:348,359` `tostring()` calls were fixed by #149 on 2026-10-17. Close when 3.4.0 is released.
- #109: one-line runviewer parser fix, confirmed.
- #79: four-line ESRPro500 runviewer parser, and `n_flags`/`num_DO` 21 to 24 (two users report no output otherwise).
- #49 / #104: declare per-device optional extras; demote PyNIVision/PyDAQmx/spinapi from hard dependencies; add zaber/pypylon extras.
- #31: delete or deprecate the legacy `Camera.py`, `camera.ui`, `imaqdx_server.py`.
- PrawnBlaster #34 (host part): if PR #37 merges, `labscript_devices/PrawnBlaster/labscript_devices.py:150,239` and `blacs_workers.py:137-151` must change in the same labscript-devices release.

### blacs, desktop-app

- blacs #46 / #29: wrap the shot-file cleanup in `experiment_queue.py:808-821` and `:926-947` so the queue-manager thread cannot die on I/O errors. Fixed in blacs #128 (merged 2026-10-18).
- blacs #52 / #56: replace the `move()/resize()` geometry restore (`__main__.py:481-515`) with `saveGeometry()/restoreGeometry()` plus a `QScreen` bounds check; Qt6 and Windows 11 multi-monitor. Fixed in blacs #128 (merged 2026-10-18).
- desktop-app #20: make `desktop_app/windows.py` pywin32 imports lazy so the launcher runs in an unactivated conda env. fixed in desktop-app #34 (merged 2026-10-17).
- blacs #100: guard `sys.stdout is None` in `labscript_utils/setup_logging.py:60` (and `sys.stderr` at `:73`).
- blacs #49: handle `StopIteration` from the first `__next__` at `tab_base_classes.py:792`. Fixed in blacs #129 (merged 2026-10-18).
- blacs #32, #7, #72: three trivial usability fixes (device names in pause status; dialog start directories from labconfig; localhost default for lyse). Fixed in blacs #129 (merged 2026-10-18).
- blacs #57 and #97: not fixes, but launch-time rendering must be checked under PySide6 and PyQt6 before tagging.
- blacs #54: becomes required if zprocess #14 (PAIR sockets) is merged, since mixed zprocess versions on remote worker PCs would then fail without a clear error. Not required by zprocess #33 (2026-10-19), which negotiates the socket type.
- blacs #19: delete `docs/UsingBLACS.pdf`, `docs/UsingBLACS.docx` and `docs/How to add a new device/` before the release.
### lyse, runviewer, zprocess, setuptools-conda, qtutils

- zprocess #27: `SetConsoleMode` crash on Windows 11 / Windows Terminal when any labscript program is restarted. Two-line fix in `zprocess/utils.py:190`; needs a zprocess point release. Fixed by zprocess #28, merged 2026-10-17; issue closed. Tested on Windows 11 2026-10-17: the branch restarts BLACS from PowerShell in Windows Terminal, where 2.27.0 exits with the issue's traceback (`TESTING.md`).
- zprocess #19 (and #16): conda defaults' Windows zeromq lacks CURVE, so secured installs fail with `ZMQError: Not supported`. Add a `zmq.has('curve')` check with a readable message and state the required pyzmq source in the release installation docs. The error is in zprocess #32 (merged 2026-10-18); the docs note is still to do.
- lyse #139: serial analysis-subprocess start-up is slower under PySide6/PyQt6, which the release moves users to. Fixed in lyse #145 (merged 2026-10-18).
- lyse #14 and #90: small, long-standing behaviour bugs with contained fixes. Fixed in lyse #145 (merged 2026-10-18).
- runviewer #13: resampler drops short pulses at t=0; labscript-c-extensions must be rebuilt for Python 3.13 to 3.15 anyway, so include the fix. fixed in labscript-c-extensions #13 (merged 2026-10-17).
- qtutils #31 (closed 2026-10-21; aliases shipped in 4.1.3, which lyse pins; qtutils #40 removes the `exec()` alias branch, which no binding needs) and #22 (RTD shows version 0.1.0.dev1; fixed in qtutils #37 (merged 2026-10-17)).
- setuptools-conda #26 only if conda packages are built for free-threaded Pythons.
### runmanager, labscript-suite

- labscript-suite #56: release workflow must handle an rc tag and a final tag on the same commit; the upcoming rc → final flow hits it. Propagate the fix to every repo's `release.yml`.
- runmanager #66 (+ #50): preparse materialises the full parameter space to count shots; compute the count from axis lengths. Fixed in runmanager #134 (merged 2026-10-18).
- runmanager #123: `remote.set_globals(raw=True)` must not append comments; reporter offered a PR. Fixed in runmanager #134 (merged 2026-10-18).
- runmanager #33, #30, #26: trivial compile-loop/GUI fixes (drain queue on abort; header line per shot; append `.h5`). Fixed in runmanager #134 (merged 2026-10-18).
- labscript-suite #5: validate the apparatus name in `labscript-profile-create` and document it. Fixed in labscript-utils #134 and labscript-suite #109 (merged 2026-10-18).
- labscript-suite #60: add `CITATION.cff` to the component repos. Left open, not for this release (maintainer decision 2026-10-18).
- labscript-suite #59: add the agreed note that `git` must be available in the labscript env (`conda install git`), or drop that page. Fixed in labscript-suite #109 (merged 2026-10-18).
- labscript-suite #105 (indirect): bump `requires-python` (currently `>=3.8`) and the component version pins in the meta-package and runmanager `pyproject.toml` for the 3.11-3.15 release; optionally add a uv developer-install docs page.

## 3. Detailed per-repo reports


## 3.x Issue triage: labscript (34 open) and labscript-utils (18 open)

Reviewed 2026-10-17 against labscript master `a0787c4` (2026-03-20, last tag v3.4.2) and
labscript-utils master `22616a7` (last tag v3.4.3).

Source material: the per-issue text files under `scratchpad/issues/` (opening post,
all comments, timeline events). Revised 2026-10-17 after the files were regenerated
with full comment threads; the first pass had only the opening posts.

`labscript-utils #117` appears in the issue list but is a pull request (reviewed in
PR-REVIEW.md, rank 8); it is mentioned under #116 and not triaged separately.

Paths below are relative to the root of each repository clone.

Verification notes that apply to several issues:

- The 'a256' dtype is rejected by the installed NumPy 2.5.4 (`TypeError: data type
  'a256' not understood`, confirmed by running it). `from pylab import *` itself imports
  cleanly under NumPy 2.5.4 with DeprecationWarnings turned into errors.
- The ramp/clockline model in `labscript/labscript/core.py:149-540` is unchanged in
  structure since 2017: a change time on one clockline during a ramp on another
  clockline is inserted into the ramping clockline's change times
  (`core.py:201-221`), ramps are broken there, and the per-clockline `clock_limit` and
  `minimum_clock_high_time` checks are applied to the result (`core.py:280-320`). The
  `minimum_clock_high_time` check was added in `a9888d5` (2022-02-05, v3.3.0). Issues
  #6, #34, #39, #53 and #112 are all facets of this one design.
- No labscript compilation could be run here (labscript is not installed in any local
  interpreter and a profile directory would have to be created under $HOME), so
  "still valid" below rests on reading the code, not on reproduction.

---

### labscript

### labscript #2: Shutter commands can be reordered due to shutter delays (shjohnst via philipstarkey, opened 2014-06-11, last activity 2017-06-23, 2 comments)
- **Summary**: `shutter.open(t)` then `shutter.close(t+1e-3)` with open_delay 3 ms and close_delay 5 ms puts the close instruction before the open instruction, so the shutter opens and never closes.
- **Type**: bug
- **Still valid?**: partly. `Shutter.open`/`close` still subtract the delays with no reordering (`labscript/labscript/outputs.py:1564-1599`). Since `bcc77ec` (2017-08-06) `Shutter.get_change_times` (`outputs.py:1615-1644`) prints a WARNING when the next state change is requested earlier than the previous one after delays, so the case in the report is no longer silent, but the compiled output is still wrong.
- **Severity**: wrong-behaviour (with warning)
- **Scope**: `Shutter` class; all hardware
- **Related**: #3 (shutter model), #5 (time uncertainty)
- **Effort**: small to raise an error instead of a warning; medium to do anything smarter
- **Release relevance**: no
- **Rewrite relevance**: requirement (shutter model must reject or resolve physically impossible open/close sequences)
- **Importance**: 2. Warned since 2017; the only remaining change is escalating to an error, which may break scripts that rely on the warning.
- **Comments**: 2014: "aim to fix in labscript 2.0"; 2017 (philipstarkey): deferred to "labscript v3", i.e. an instruction class that keeps timing information; Bitbucket PR #9 implemented a fix but was backed out for performance.
- **Recommended action**: close as won't fix in legacy (maintainers deferred it to the next major version in 2017); the warning stands.

### labscript #3: Better control of shutters (shjohnst via philipstarkey, opened 2014-06-11, last activity 2014-06-12, 4 comments)
- **Summary**: Proposes `open_by/close_by/open_from/close_from` and six shutter timing parameters (open/close delay, open/close time, min opened/closed time) with errors when the physical shutter cannot follow the commands.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented; `Shutter.__init__` takes only `delay=(open, close)` (`outputs.py:1530-1533`).
- **Scope**: `Shutter` class
- **Related**: #2, #5
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: requirement (shutter timing model with rise/fall and minimum dwell times)
- **Importance**: 2. Useful design input; nobody has acted in 12 years.
- **Comments**: accepted as an enhancement for 2.0 in 2014 (chrisjbillington); the reporter corrected the example and suggested keyword arguments instead of a tuple of delays. Nothing was implemented.
- **Recommended action**: close as won't fix in legacy; keep as rewrite design input.

### labscript #4: labscript should reject commands after a wait if they have a time before the last wait (philipstarkey, opened 2014-06-18, last activity 2014-06-18, 0 comments)
- **Summary**: After `wait(t)`, instructions with time < t should be an error, because the real-time ordering is unknowable at compile time.
- **Type**: feature request (compile-time check)
- **Still valid?**: n.a. Not implemented: `Output.add_instruction` (`outputs.py:207-292`) checks only `time < self.t0` and collisions; `Output.do_checks` (`outputs.py:338-375`) checks ramps spanning a trigger and instructions inside `trigger_delay` after a trigger. The third check there, "too soon before the trigger" (`outputs.py:364-375`), compares `max(self.clock_limit, compiler.wait_delay)` (Hz) with a time difference (s) and so never fires; it is dead code.
- **Scope**: compiler, waits
- **Related**: #50 (waits), #5
- **Effort**: small (record the time of the last `wait()` call in `compiler` and compare in `add_instruction`); but it is a breaking change for scripts that deliberately schedule before a wait.
- **Release relevance**: no
- **Rewrite relevance**: requirement (reject instructions that precede the most recent wait)
- **Importance**: 2
- **Recommended action**: fix later (opt-in check), or close as won't fix; separately delete or fix the dead check at `outputs.py:364-375`.

### labscript #5: Instructions should be able to have an uncertainty to their time (philipstarkey, opened 2014-06-18, last activity 2014-06-18, 0 comments)
- **Summary**: Allow instructions a tolerance (float or (neg, pos) tuple) so the compiler can merge them into a nearby clock tick instead of raising clock_limit errors.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented.
- **Scope**: compiler core
- **Related**: #43, #53, #112 (the errors this would avoid)
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement candidate (instruction time tolerance), design decision needed
- **Importance**: 1
- **Recommended action**: close as won't fix in legacy.

### labscript #6: A clockline's clock_limit is effectively limited by another's while that other clockline is ramping (philipstarkey, opened 2014-06-18, last activity 2014-06-18, 0 comments)
- **Summary**: Constant updates on clockline B during a ramp on clockline A break A's loop and tick both clocklines; B is therefore limited to A's rate. Proposes interleaving separate pseudoclock instructions.
- **Type**: feature request (compiler limitation)
- **Still valid?**: n.a. Limitation still present (`core.py:201-221`, `core.py:327-540`).
- **Scope**: compiler core, all pseudoclocks
- **Related**: #34 (same proposal with code), #39, #53, #112
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement (clocklines on one pseudoclock should be scheduled independently where the pseudoclock instruction rate allows)
- **Importance**: 2
- **Recommended action**: leave open as the canonical issue for this limitation; close #34 and #112 as duplicates pointing here.

### labscript #7: Nested loops (philipstarkey, opened 2014-06-18, last activity 2014-06-18, 0 comments)
- **Summary**: Use nested pseudoclock loops when two clocklines ramp at commensurate rates.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented; `expand_change_times` emits a flat clock list.
- **Scope**: compiler core; only useful for pseudoclocks with nested loops (PulseBlaster)
- **Related**: #42
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: none (instruction-count optimisation specific to one device family)
- **Importance**: 1
- **Recommended action**: close as won't fix.

### labscript #10: Unexpected results when importing connection table (chrisjbillington via philipstarkey, opened 2014-10-04, last activity 2014-10-05, 2 comments)
- **Summary**: A connection table in a separately imported module runs only on first import; on the second compile in the same interpreter the devices are not defined. Proposes raising an error when `Device` instances are created at module level outside the main script.
- **Type**: bug (usability)
- **Still valid?**: yes. runmanager's batch compiler keeps one interpreter and only unloads user modules when a file changes (`runmanager/batch_compiler.py:90` on origin/master, `labscript_utils/modulewatcher.py:70-110`); labscript has no detection of device instantiation outside `__main__`. `import_or_reload` in `labscript-utils/labscript_utils/__init__.py:36` exists as a workaround but nothing in the suite uses it.
- **Severity**: wrong-behaviour (confusing compile failure, no data loss)
- **Scope**: compiler + runmanager batch compiler
- **Related**: #11; labscript-utils #28
- **Effort**: small. The 2014 follow-up comment (chrisjbillington) rejected the "raise an error" idea in favour of recording which modules instantiate `Device`s and deleting them (and their importers) from `sys.modules` after each compile, in ModuleWatcher. That is about twenty lines in `Device.__init__` plus a hook in `labscript_cleanup()`; it was never done.
- **Release relevance**: no
- **Rewrite relevance**: moot (shotscript imports connection tables through its own importing module and executes them per shot) or requirement; confirm in the rewrite's `importing.py`.
- **Importance**: 2
- **Related (addendum)**: labscript-utils #28 is the crash users hit when they work around this with `import_or_reload`.
- **Recommended action**: fix later per the 2014 plan (unload device-defining modules after compile), or convert to docs (wrap connection tables in a function).

### labscript #11: Globals and devices should be in modules, not builtins (chrisjbillington via philipstarkey, opened 2014-10-04, last activity 2014-10-04, 3 comments)
- **Summary**: Stop inserting shot globals and device objects into `builtins`; provide `shot_globals` and `shot_devices` modules instead, and refer to parents by string.
- **Type**: feature request (design)
- **Still valid?**: n.a. Not done: `base.py:144` puts every device into `builtins.__dict__`, `labscript.py:737` does the same for globals, and `compiler.reset()` restores them (`compiler.py:48-56`).
- **Scope**: compiler; breaks every user script if changed
- **Related**: #10, #104
- **Effort**: large (API break)
- **Release relevance**: no
- **Rewrite relevance**: moot (the rewrite has no builtins injection; globals namespace is explicit per the design notes)
- **Importance**: 1
- **Comments**: the proposal was argued down the same day (2014-10-04): philipstarkey objected that string parents cannot express `parent.direct_outputs` or `parent.get_clockline(7)`, and chrisjbillington agreed that "putting them in the namespace is looking like the best solution". The remaining open question (an explicit `labscript_init(h5_file)` call) was to be a separate issue. So the issue as titled was already decided against.
- **Recommended action**: close as won't fix (decided in 2014); the rewrite's explicit-namespace design is the successor.

### labscript #15: Basic connection tables (with no outputs) do not compile (philipstarkey, opened 2014-12-05, last activity 2017-07-19, 1 comment)
- **Summary**: A connection table with a pseudoclock and an NI board but no outputs fails in `NIBoard.generate_code` with `KeyError` on `pseudoclock.times[clockline]`.
- **Type**: bug
- **Still valid?**: probably fixed, not reproduced. A 2017 comment (Jan Werkmann) adds the case of an NI card with only `AnalogIn` children. `Pseudoclock.get_outputs_by_clockline` now seeds `outputs_by_clockline` with every `ClockLine` child (`core.py:551-553`), `collect_change_times` adds `0` when a clockline has no change times (`core.py:243-247`), and `generate_clock` fills `self.times` for every clockline (`core.py:585-588`). `NI_DAQmx._make_analog_out_table` returns `None` for no analogs (`labscript-devices/labscript_devices/NI_DAQmx/labscript_devices.py:440-443`). The 2014 code path no longer exists (NIBoard.py was replaced). The one comment (2017) is unknown.
- **Severity**: annoyance
- **Scope**: compiler + NI_DAQmx
- **Related**: none
- **Effort**: trivial to confirm with a DummyPseudoclock + DummyIntermediateDevice compile, and an NI_DAQmx device with only an `AnalogIn`
- **Release relevance**: no
- **Rewrite relevance**: requirement (empty connection tables and input-only devices must compile; worth a test)
- **Importance**: 1
- **Recommended action**: close as fixed after a one-line compile check.

### labscript #16: Round-off error in ramps tries to make devices go beyond their limits (shjohnst via philipstarkey, opened 2015-06-18, last activity 2015-06-18, 0 comments)
- **Summary**: Ramping to a limit value (e.g. 0 amplitude) fails the limits check because the evaluated ramp is slightly outside the limit; the error does not say the offending value.
- **Type**: bug
- **Still valid?**: yes. The ramp limits check in `Output.expand_timeseries` is exact with no tolerance and reports the function and start time but not the value (`outputs.py:521-529`). The constant check is also exact (`outputs.py:283-290`). The `exp_ramp` family evaluates `final` via floating arithmetic at the midpoint-shifted sample times, so overshoot below 0 is possible.
- **Severity**: annoyance (compile error with a documented workaround)
- **Scope**: `Output.expand_timeseries`; all analog outputs with `limits`
- **Related**: #44
- **Effort**: small (clip values within a relative tolerance of the limits, and include min/max of the offending array in the message)
- **Release relevance**: no
- **Rewrite relevance**: requirement (limit checks need a tolerance and informative errors)
- **Importance**: 3. Cheap fix, long-standing irritation.
- **Recommended action**: fix for next release.
- **Status 2026-10-18**: fixed in labscript #128 (merged 2026-10-18).

### labscript #18: Execution of small or time-critical analysis scripts as part of running shot (ispielma via philipstarkey, opened 2017-04-20, last activity 2018-08-08, 11 comments)
- **Summary**: Proposes a `ScriptManager` pseudo-device with BLACS tabs that runs Python callables locally or remotely at the end of each shot, with `start_order`/`stop_order`.
- **Type**: feature request (proposal)
- **Still valid?**: n.a. Partially implemented. The 2018-08-01 checklist (chrisjbillington) has `start_order`/`stop_order` done (`base.py:54-108`, `labscript.py:442-456`), zprocess remote-broker events done (zprocess 2.6), and `runmanager.remote` exists on runmanager master; not done: BLACS queue-size events and ordered transitions settings, runmanager compilation-queue tab and just-in-time compilation, and the `script_runner` labscript device. Design decisions recorded in the thread: scripts are plain functions taking an HDF5 path (not open handles), run after the shot by a BLACS-tab "device", feed back through the runmanager remote API, and persist state via a per-function dict rather than a labscript-provided mechanism; "persistent variables in the next shot file" was rejected.
- **Scope**: labscript + BLACS + lyse; cross-repo
- **Related**: #21, #32, #36 (all ispielma proposals about BLACS behaviour); runmanager #104 + blacs #90 compilation-queue PRs (PR-REVIEW rank 16) implement part of the same checklist
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement (per-shot analysis hooks with feedback; shotscript.analysis already covers between-shot analysis, see ANALYSIS-DESIGN.md)
- **Importance**: 2
- **Recommended action**: close as won't fix in legacy, noting the partial implementation and that the rewrite's analysis design is the follow-up.

### labscript #21: Far future: have in-shot analysis with live feedback rather than between shots (ispielma via philipstarkey, opened 2017-04-21, last activity 2017-04-21, 0 comments)
- **Summary**: Run analysis at a defined point inside a shot and feed results back within the same shot.
- **Type**: feature request (proposal)
- **Still valid?**: n.a.
- **Scope**: whole suite; requires hardware-level mid-shot communication
- **Related**: #18
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: none for now (out of scope of a compile-ahead model)
- **Importance**: 1
- **Recommended action**: close as won't fix.

### labscript #32: Smarter dealing with errors, so not every error causes a stop (ispielma via philipstarkey, opened 2017-04-21, last activity 2020-04-05, 3 comments)
- **Summary**: BLACS should not stop the queue on every device error; some errors (missed camera frame) should be ignored or the shot retried, and a "safe" script should run after too many errors.
- **Type**: feature request (labelled bug), BLACS behaviour
- **Still valid?**: n.a. Filed against the wrong repo; nothing in labscript implements queue policy. In the thread chrisjbillington sketched an escalation policy (restart tab, retry shot, restart all tabs, hardware reset, keep cycling on transition_to_manual errors) and philipstarkey asked for it to be re-posted on the BLACS repo and referenced labscript-suite#104; that re-post never happened.
- **Scope**: BLACS queue manager
- **Related**: #36; blacs #89 (retry on timeout, PR-REVIEW rank 26, recommended close)
- **Effort**: medium (in BLACS)
- **Release relevance**: no
- **Rewrite relevance**: requirement (configurable error policy in the shot runner)
- **Importance**: 2
- **Recommended action**: close here; re-file or link in blacs if the maintainer wants to keep it.

### labscript #34: Ramp splitting (ReneKolb via philipstarkey, opened 2017-05-30, last activity 2017-05-31, 2 comments)
- **Summary**: A digital change on clockline 2 during a ramp on clockline 1 inserts a tick on clockline 1 that its device cannot handle; the reporter attached a patch that splits ramps and ticks clockline 2 alone.
- **Type**: feature request with prototype
- **Still valid?**: n.a. Limitation still present (see header note). The author pushed a `split_ramps` branch to the Bitbucket archive (2017-05-31); nothing further happened.
- **Scope**: compiler core
- **Related**: duplicate of #6; #39, #53, #112
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement (same as #6)
- **Importance**: 2
- **Recommended action**: close as duplicate of #6.

### labscript #36: Desire output values between shots different from those present when stopping sequencing (ispielma via philipstarkey, opened 2017-05-31, last activity 2017-05-31, 0 comments)
- **Summary**: `DO_2.safe_state(0, timeout=5)` would tell BLACS to return an output to a safe value after N seconds idle between shots.
- **Type**: feature request (proposal)
- **Still valid?**: n.a. Not implemented in labscript or BLACS.
- **Scope**: labscript API + BLACS manual mode
- **Related**: #32
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: requirement candidate (idle-state timeouts for outputs)
- **Importance**: 2
- **Recommended action**: close as won't fix in legacy; record for the rewrite.

### labscript #39: Non-looping clock ticks may be too short if they happen during a ramp (philipstarkey, opened 2017-06-27, last activity 2017-06-28, 2 comments)
- **Summary**: The first tick of a ramp also ticks non-ramping clocklines, but the tick period is set by the fastest ramp, ignoring the non-ramping clocklines' limits.
- **Type**: bug
- **Still valid?**: fixed in the sense proposed as option 1: `a9888d5` (2022-02-05, v3.3.0) added `ClockLine.minimum_clock_high_time` and a check in `collect_change_times` (`core.py:298-320`) that raises when another clockline's event is closer than twice the minimum high time. Short ticks are now a compile error rather than silently generated. The 2017 comments proposed a per-pseudoclock `supports_slow_clock` flag and a six-instruction PulseBlaster scheme (looping and non-looping clocks with separate high/low instructions); that was not done, and the minimum-high-time approach was the alternative philipstarkey proposed in the #53 thread (2019-08-02). Option 2 (splitting ramps) was not done (see #6).
- **Severity**: was wrong-behaviour; now a compile error
- **Scope**: compiler core
- **Related**: #6, #34, #53, #112 (the error this introduced is the one #112 reports)
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: requirement (per-clockline minimum high time respected when scheduling)
- **Importance**: 1
- **Recommended action**: close as fixed (a9888d5), pointing to #6 for the remaining limitation.

### labscript #41: Test suite for labscript (philipstarkey, opened 2017-06-28, last activity 2024-01-28, 2 comments)
- **Summary**: Build a regression suite that compiles a reference shot and compares runviewer-style traces against stored expectations.
- **Type**: tooling
- **Still valid?**: yes. The labscript repo has no tests directory and no CI test step; labscript-utils likewise. dihm's 2024-01-28 comment asks to revisit this now that the #102 submodule refactor and the breaking changes in #104/#105 are on the table.
- **Scope**: labscript, labscript-utils
- **Related**: #105 (type hints wants tests first)
- **Effort**: medium for a compile-smoke suite using DummyPseudoclock/DummyIntermediateDevice; large for trace comparison
- **Release relevance**: yes. A compile smoke test on Python 3.11-3.15 with NumPy 2.x would have caught #123 and the pylab/NumPy 2 issue before users did.
- **Rewrite relevance**: moot for the rewrite itself (it has tests under rewrite/tests); the "judicious tests" policy applies.
- **Importance**: 4. The release supports five Python versions and NumPy 2 with zero automated coverage.
- **Recommended action**: fix for next release at the smoke-test level (compile `example.py` with dummy devices on each supported Python in CI).

### labscript #42: Loop recognition (PhyNerd via philipstarkey, opened 2017-07-19, last activity 2017-07-20, 6 comments)
- **Summary**: Repeated digital pulse patterns should be detected and emitted as pseudoclock loops to save PulseBlaster instructions.
- **Type**: feature request
- **Still valid?**: n.a. Answered in 2017: the reporter's outputs were on an NI card, and `DigitalQuantity.repeat_pulse_sequence` (`outputs.py:1375`) covers that case; the reporter tried it and it worked, though "not as user friendly as for loops". philipstarkey stated that pattern recognition on PulseBlaster instructions was considered and never needed, and that adding pseudoclocks is the preferred fix. The PrawnBlaster device merges consecutive identical periods (`labscript-devices/.../PrawnBlaster/labscript_devices.py:428-447`), which is the only loop compression in the suite.
- **Scope**: compiler core / PulseBlaster
- **Related**: #7
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: none (device-specific optimisation); the rewrite's `pattern.py` may already cover repeated patterns.
- **Importance**: 1
- **Recommended action**: close as answered (`repeat_pulse_sequence`) / won't fix.

### labscript #43: Better "too short delay" error message (PhyNerd via philipstarkey, opened 2017-07-21, last activity 2017-07-21, 0 comments)
- **Summary**: The "Commands have been issued to devices attached to X at t=... and ..." error should name the outputs that collided.
- **Type**: feature request (error message)
- **Still valid?**: yes. The three collision errors in `collect_change_times` (`core.py:230-236`, `core.py:290-297`, `core.py:309-320`) report only clockline/pseudoclock names and times. The output names are available in `outputs_by_clockline` and each output's `instructions` dict, so the lookup is straightforward.
- **Scope**: compiler core
- **Related**: #53, #112 (both reporters could not understand this message), #5
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: requirement (collision errors must name the instructions and their source lines)
- **Importance**: 4. Two later issues (#53, #112) are users failing to diagnose this message; a few lines fix it.
- **Recommended action**: fix for next release.
- **Status 2026-10-18**: fixed in labscript #128 (merged 2026-10-18).

### labscript #44: limits should be stored in the connection table (philipstarkey, opened 2018-01-23, last activity 2018-03-22, 5 comments)
- **Summary**: Output `limits` only apply at compile time; BLACS never sees them because they are not saved. Also undocumented.
- **Type**: feature request (labelled bug)
- **Still valid?**: yes. `Output.__init__` stores `self.limits` only on the object (`outputs.py:115`), with `set_passed_properties(property_names={})`, so nothing is written to the connection table. BLACS gets limits from per-device-tab code (`blacs/blacs/output_classes.py:54`). `limits` does not appear in `labscript/example.py` or `labscript/docs`.
- **Severity**: wrong-behaviour (manual mode can exceed compile-time limits)
- **Scope**: labscript `Output`, BLACS tabs, docs
- **Related**: #45, #49 (where to store per-channel properties)
- **Effort**: small in labscript (`connection_table_properties: ["limits"]`), plus a change in `labscript_utils.connections.Connection.compare_to` so that experiment limits that are a sub-interval of the connection-table limits pass comparison (agreed in the 2018 thread between Jan Werkmann and philipstarkey; Werkmann offered two PRs that never arrived; the alternative `limits__allow_interval_subset` key encoding was floated and not adopted); medium to have BLACS consume them
- **Release relevance**: no
- **Rewrite relevance**: requirement (limits are part of the channel definition and must reach manual control)
- **Importance**: 3
- **Recommended action**: fix later (labscript half is trivial and backwards compatible; do it alongside #16).

### labscript #45: Restructure properties and BLACS connections (chrisjbillington via philipstarkey, opened 2018-03-12, last activity 2018-03-12, 3 comments)
- **Summary**: Move device_properties into a connection-table column, separate user configuration from compilation results, and replace the `BLACS_connection` column with a boolean plus connection_table_properties.
- **Type**: feature request (proposal)
- **Still valid?**: n.a. Not done. `generate_connection_table` still writes a `BLACS_connection` column (`labscript.py:242-250`, `labscript.py:268-275`); the 2026 commit `2b8c2a2` ("Don't have all devices have a BLACS_connection") moved in the direction of this proposal but kept the column. In the thread philipstarkey agreed with moving device_properties into the connection table but not with the motivating example (labscript_devices PR 27 data belongs in connection_table_properties), and spun off labscript_devices#24 (backwards-compatible connection-table comparison); the BLACS_connection column was left undecided (proposal: a `control_system_host` column).
- **Scope**: labscript + labscript-utils `connections.py` + BLACS
- **Related**: #44, #49
- **Effort**: large (file-format change across three repos)
- **Release relevance**: no
- **Rewrite relevance**: moot (the rewrite defines its own shot-file schema; this is a statement of what it should get right)
- **Importance**: 1
- **Recommended action**: close as won't fix in legacy.

### labscript #49: Allow set_passed_properties on objects without a device group (philipstarkey, opened 2018-10-17, last activity 2018-10-17, 0 comments)
- **Summary**: Using `device_properties` on outputs forces a `/devices/<output>` group, which BLACS then treats as a real device.
- **Type**: feature request (latent bug)
- **Still valid?**: yes. `write_device_properties` creates a device group for any inventory member with non-trivial `device_properties` (`labscript.py:464-468`); outputs are in the inventory. Nothing in the base classes currently sets `device_properties` on outputs, so the hazard is latent.
- **Severity**: annoyance (latent)
- **Scope**: labscript + BLACS
- **Related**: #44, #45
- **Effort**: small (store child properties under the parent group, or have BLACS filter on `BLACS_connection`)
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as stale unless #44 is implemented via device_properties.

### labscript #50: pseudoclock wait_delay is probably not respected (philipstarkey, opened 2018-10-30, last activity 2018-10-30, 0 comments)
- **Summary**: The master pseudoclock may re-trigger secondary pseudoclocks after a wait before they are ready (`wait_delay`), desynchronising them; suspected cause of dropped shots.
- **Type**: bug
- **Still valid?**: yes, by code reading. `trigger_all_pseudoclocks` computes `wait_delay` but calls `pseudoclock.trigger(t, compiler.trigger_duration)` without passing it (`labscript.py:540-547`); `PseudoclockDevice.trigger` only shifts its recorded `trigger_times` by `wait_delay` and still asks the `Trigger` output to pulse at `t` (`core.py:805-825`). So the resume pulse is emitted at the moment the master resumes, not `wait_delay` later. The delay only lengthens the value returned to the user from `wait()`. Whether this causes missed triggers depends on hardware (how early the secondary can accept a trigger after entering its wait).
- **Severity**: wrong-behaviour (potential shot desync; hardware dependent)
- **Scope**: compiler, secondary pseudoclocks with non-zero `wait_delay` (PulseBlaster, PineBlaster)
- **Related**: #4
- **Effort**: small (pass `wait_delay` and pulse at `t + wait_delay` for non-initial triggers); needs a hardware test
- **Release relevance**: no
- **Rewrite relevance**: requirement (`trigger_holdoff` in `rewrite/src/shotscript/pattern.py` appears to model this; verify it is applied to resume triggers)
- **Importance**: 3. Real but hardware-dependent and nobody has confirmed symptoms since 2018.
- **Recommended action**: fix later; ask on the mailing list whether any lab with secondary PulseBlasters and waits sees dropped shots.

### labscript #52: Redefinition of digital outputs (at least) is silent (lincolnturner via philipstarkey, opened 2019-07-11, last activity 2019-07-11, 2 comments)
- **Summary**: Two `DigitalOut`s on the same `port0/line11` compile without error; which label BLACS shows is arbitrary.
- **Type**: bug
- **Still valid?**: yes. `Device.add_device` checks only `allowed_children` (`base.py:345-359`); no uniqueness check on `connection` exists in `base.py`, `core.py` or `outputs.py`. In 2019 chrisjbillington diagnosed it (NI_DAQmx builds a `digitals[device.connection]` dict so the last duplicate wins the instructions while BLACS labels by the first) and said he would patch NI_DAQmx, with a general `Device.add_device` check deferred because connection strings are free-form on other devices. The NI_DAQmx patch did not land: `NI_DAQmx.add_device` (`labscript-devices/.../NI_DAQmx/labscript_devices.py:321-386`) validates format and port/line ranges but still has no duplicate check.
- **Severity**: wrong-behaviour (silent, wrong hardware line driven)
- **Scope**: all intermediate devices
- **Related**: none
- **Effort**: trivial (in `Device.add_device`: raise if another child has the same `connection`, excluding `connection="internal"`/`None` cases and DDS sub-channels). An exact-string comparison catches the reported case; case-insensitive duplicates on devices with loose connection strings remain, which is what stopped the 2019 fix and should not stop this one.
- **Release relevance**: no
- **Rewrite relevance**: requirement (duplicate channel assignment is a compile error)
- **Importance**: 4. Silent wrong-wiring bug with a ten-line fix.
- **Recommended action**: fix for next release.
- **Status 2026-10-18**: fixed in labscript #128 (merged 2026-10-18).

### labscript #53: Pseudoclock/clockline collision (dihm via philipstarkey, opened 2019-07-27, last activity 2019-08-02, 4 comments)
- **Summary**: A slow clockline's limit produces a collision error on the master pseudoclock when an analog update (fast clockline) and DDS updates (slow clockline) are within ~2 ms; runviewer shows both clocklines ticking identically.
- **Type**: bug report / support
- **Still valid?**: addressed. The thread links it to #51 (closed), chrisjbillington reproduced it at NIST with a slow LightCrafter DMD clockline after the gated-clocks commit, and philipstarkey's 2019-08-02 edit proposed letting intermediate devices declare a minimum clock high time so that the check distinguishes "time between adjacent instructions" from "time between ticks on this clockline". That is what `a9888d5` (2022-02-05, v3.3.0) implemented (`core.py:58-66`, `core.py:298-320`). The remaining coupling of clocklines is #6.
- **Severity**: annoyance (compile error)
- **Scope**: compiler core
- **Related**: #6, #34, #39, #43, #112
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: requirement (same as #6)
- **Importance**: 1
- **Recommended action**: close as fixed by a9888d5 (minimum clock high time), pointing to #6 for the remaining limitation and #43 for the message.

### labscript #54: Ability to define duration of a constant instruction (chrisjbillington via philipstarkey, opened 2019-10-25, last activity 2019-10-25, 1 comment)
- **Summary**: `output.constant(t, value, duration=...)` should make any instruction to the same output within the duration a compile error; ramps should accept a hold duration beyond their end.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented: `AnalogQuantity.constant(self, t, value, units=None)` (`outputs.py:1191`). The one comment settles naming: a `block_until=<absolute time>` keyword (ispielma's suggestion), or `block_for` if a duration.
- **Scope**: `Output` API
- **Related**: #4
- **Effort**: small to medium (reuse `ramp_limits` as "reserved intervals")
- **Release relevance**: no
- **Rewrite relevance**: requirement (hold durations with overlap detection)
- **Importance**: 2
- **Recommended action**: fix later or close as won't fix in legacy; the original author intended it for "labscript 3", i.e. the rewrite.

### labscript #95: It seems that the time sequence cannot be too long (Moriaty-TT, opened 2022-08-11, last activity 2022-08-15, 4 comments)
- **Summary**: A 75 s PrawnBlaster shot fails in `PrawnBlaster.generate_code` with `OverflowError: Python int too large to convert to C long`. philipstarkey diagnosed it in the thread: one PrawnBlaster clockline (`Dev3`) had outputs that were never commanded inside the loop, so labscript emitted a single clock tick spanning most of the shot, longer than the PrawnBlaster's maximum half period (2^32-1 ticks, about 42 s). Workaround (confirmed by the reporter): command any output on every clockline at least once per 42 s. philipstarkey: "We'll keep this open until we have a proper fix in labscript that covers all pseudoclocks."
- **Type**: bug (labscript compiler gap plus a labscript-devices validation gap)
- **Still valid?**: yes, both halves. (1) labscript has no notion of a pseudoclock's maximum clock period: nothing in `core.py` inserts extra ticks on an idle clockline (`collect_change_times`, `core.py:149-325`), and `PseudoclockDevice` has no attribute for it. (2) `PrawnBlaster.generate_code` builds `pulse_program` with dtype `("half_period", int)` (`labscript-devices/.../PrawnBlaster/labscript_devices.py:463`) and never range-checks `half_period`; on Windows with NumPy < 2 (`int` = int32) that raises the reported `OverflowError`, and on NumPy 2 (`int` = int64 everywhere) the value is written without error and truncated by the firmware, i.e. a silently wrong shot.
- **Severity**: crash (NumPy < 2) / silent wrong-behaviour (NumPy 2)
- **Scope**: compiler core (general), PrawnBlaster device (validation); any pseudoclock with a bounded instruction length
- **Related**: #6 (clockline scheduling), labscript-devices
- **Effort**: trivial for the device-side check (`np.uint32` plus a `LabscriptError` that names the idle clockline and the workaround); medium for the general fix (a `max_clock_period` attribute on pseudoclocks and keep-alive ticks inserted in `collect_change_times`, before ramps are expanded)
- **Release relevance**: yes. The NumPy 2 transition turns this from a compile error into silently truncated hardware instructions; the device-side check must ship with the release.
- **Rewrite relevance**: requirement (each pseudoclock declares a maximum tick period; the compiler inserts keep-alive ticks on idle clocklines or raises a clear error)
- **Importance**: 4. Silent wrong output on current NumPy with a one-line guard available; the general fix can wait.
- **Recommended action**: fix for next release in labscript-devices (range check with the workaround in the message); leave this issue open in labscript for the maximum-period feature, or retitle it.

### labscript #96: Input impedance control of the clock terminal PFI4 on NI 6535 (zhang-wenjun, opened 2023-04-11, last activity 2023-04-11, 2 comments)
- **Summary**: PFI4 on a PCIe-6535 presents ~50 ohm when used as the sample clock from an RP2040, so the clock high level is 1.3 V; asks whether labscript can configure the input impedance.
- **Type**: question-support (hardware)
- **Still valid?**: n.a. Answered the same day by chrisjbillington: the PFI terminal is driven as an output while BLACS is in manual mode; the reporter re-measured in buffered mode, found the expected high impedance, and used the suggested custom `ports` configuration. Reporter: "This solved my issue".
- **Scope**: labscript-devices NI_DAQmx, NI 6535 hardware
- **Related**: none
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as resolved (reporter confirmed).

### labscript #104: Remove pylab star import in `labscript.labscript` (dihm, opened 2024-01-28, last activity 2025-08-19, 1 comment)
- **Summary**: Remove `from pylab import *` (and ideally all star imports) from labscript; users may rely on the leaked names, so either import the useful names explicitly or accept the break and discourage `from labscript import *`.
- **Type**: feature request / docs
- **Still valid?**: yes. `from pylab import *` remains at `labscript/labscript/labscript.py:46` and `labscript/labscript/functions.py:17`; `labscript/__init__.py:13` re-exports everything. dihm's 2025-08-19 comment: the #102 submodule refactor plus NumPy 2 produced a namespace clobber found in #115 (`numpy.core` shadows `labscript.core` when the star import follows the submodule import), "technically not breaking since no code actually imports from the refactored submodules directly"; the docs extra was pinned to `numpy<2` as a workaround (`labscript/pyproject.toml:55`, commit `6d225b4`). `labscript/docs/source/introduction.rst:7` still teaches `from labscript import *`.
- **Scope**: labscript namespace; affects every user script that uses numpy names without importing numpy
- **Related**: #11, #123, #41
- **Effort**: small for the code (explicit `import numpy as np` and the handful of names labscript itself uses: `zeros`, `array`, `linspace`, etc.); the compatibility question is the cost. A middle path: keep a curated `from numpy import ...` list of the commonly used names for one release with a deprecation note.
- **Release relevance**: yes. The star import makes labscript's behaviour depend on matplotlib's `pylab` surface, which changes between matplotlib/NumPy releases (the docs build already needed a NumPy pin), and it imports matplotlib for every compile.
- **Rewrite relevance**: moot (the rewrite has no star imports; globals namespace is explicit)
- **Importance**: 4. Decide the compatibility policy and do it in the same release that drops Python 3.8-3.10.
- **Recommended action**: fix for next release (explicit imports, curated re-export list with deprecation warning, docs updated).
- **Maintainer decision 2026-10-18**: remove the star import without a re-export list. Scripts that use numpy or matplotlib names from `from labscript import *` break; the release notes list this at the top with the other breaking changes.
- **Status 2026-10-18**: labscript #130 opened.

### labscript #105: Add type hints to the labscript API (dihm, opened 2024-01-28, last activity 2024-01-28, 0 comments)
- **Summary**: Add type hints gradually, choose a checker, and decide the minimum Python; notes that the `Device(name, ...)` naming convention is the main obstacle.
- **Type**: feature request
- **Still valid?**: n.a. No type hints in `labscript/labscript/*.py`.
- **Scope**: labscript
- **Related**: #41
- **Effort**: medium (with Python 3.11 minimum the syntax question is settled)
- **Release relevance**: no
- **Rewrite relevance**: moot (rewrite is typed, e.g. `device.py`, `pattern.py`)
- **Importance**: 1
- **Recommended action**: close as won't fix in legacy, or leave open as low-priority.

### labscript #108: Store times as integer multiples of the master pseudoclock `clock_resolution` (philipstarkey, opened 2024-02-17, last activity 2024-02-17, 0 comments)
- **Summary**: Floating-point time storage causes spurious compile errors (ref #99); store quantised integer times internally and keep floats only for messages.
- **Type**: feature request (design)
- **Still valid?**: n.a. Times are floats rounded to 0.1 ns in `add_instruction` (`outputs.py:223-227`) and quantised late in `quantise_to_pseudoclock` (`base.py:378`).
- **Scope**: compiler core; touches every device's `generate_code`
- **Related**: #99 (closed), #5
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: moot (the rewrite uses `fractions.Fraction` for exact times, `rewrite/src/shotscript/device.py:14-20`)
- **Importance**: 1
- **Recommended action**: close as won't fix in legacy.

### labscript #109: Update `Trigger` to support the `inverted` kwarg (philipstarkey, opened 2024-02-17, last activity 2024-02-17, 0 comments)
- **Summary**: `Trigger` ignores `DigitalOut`'s `inverted` kwarg, which is confusing (ref #93); fix without breaking PulseBlaster secondary triggering.
- **Type**: bug (API inconsistency)
- **Still valid?**: yes. `Trigger.__init__` passes `inverted` through to `DigitalOut` (so it is recorded in connection_table_properties) but then rebinds `self.enable`/`self.disable` directly to `go_high`/`go_low` according to `trigger_edge_type` (`outputs.py:1653-1677`), bypassing `DigitalQuantity.enable/disable`, which are the only methods that honour `inverted` (`outputs.py:1349-1373`). So `inverted=True` on a `Trigger` changes the stored property but not the generated pulses.
- **Severity**: wrong-behaviour (only if someone passes `inverted` to a Trigger; otherwise cosmetic)
- **Scope**: `Trigger`
- **Related**: #93 (closed)
- **Effort**: small (define polarity once from `trigger_edge_type` and `inverted`; or raise if both are given)
- **Release relevance**: no
- **Rewrite relevance**: requirement (single polarity model for triggers)
- **Importance**: 2
- **Recommended action**: fix later (raise a clear error when `inverted` is passed to `Trigger` is the safe minimum).

### labscript #112: Experiment timing limited by slow component (neutrinonerd3333, opened 2025-01-14, last activity 2025-02-03, 4 comments)
- **Summary**: An NI 6739 analog update followed 1 us later by a PulseBlaster digital output fails with the "digital high time shorter than 1.25e-06 ... more than half the available time" error; asks whether a secondary pseudoclock is still the recommended workaround.
- **Type**: question-support
- **Still valid?**: n.a. Answered by dihm (2025-01/02): gated clocks already decouple clocklines when one is idle, PulseBlaster direct outputs may not be gated the same way, and the recommended hardware fix is PrawnBlaster + PrawnDO. The reporter asked for documentation of the gated-clock scheme (none exists in the labscript docs) and whether PulseBlaster direct outputs could be gated; dihm did not know without an example script. The error quoted is `core.py:309-320` (added by a9888d5) and the limitation is #6.
- **Scope**: compiler core; PulseBlaster as master with NI cards
- **Related**: #6, #39, #43
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: requirement (same as #6)
- **Importance**: 2
- **Recommended action**: convert to docs (a page on gated clocks and clockline limits is the concrete request), then close linking #6 and #43.

### labscript #123: NumPy deprecating 'a256' dtype (rogding, opened 2026-09-17, last activity 2026-09-17, 0 comments)
- **Summary**: NumPy 2.5 removed the 'a' dtype alias; labscript uses `'a256'` in four places and labscript-devices in more. Proposes `'S256'`.
- **Type**: bug
- **Still valid?**: yes. Confirmed: `numpy.dtype('a256')` raises `TypeError` on the installed NumPy 2.5.4. Sites: `labscript/labscript/labscript.py:216` (time markers), `:268` (connection table `name` column), `:477` (wait table), `labscript/labscript/outputs.py:1604` (shutter calibration table). Every compile writes the connection table, so compilation fails outright on NumPy >= 2.5. Also in labscript-devices: `NI_DAQmx/labscript_devices.py:514-520`, `PrawnBlaster/blacs_workers.py:497`, `Camera.py:107`, `AlazarTechBoard.py`, `CiceroOpalKellyXEM3001.py`, `NI_DAQmx/blacs_workers.py`. No open PR.
- **Severity**: crash (compile fails)
- **Scope**: labscript, labscript-devices; any platform with NumPy >= 2.5
- **Related**: #104 (same NumPy-2 class of problem), #41
- **Effort**: trivial (`'a256'` -> `'S256'`; identical on-disk dtype so no file-format change; readers using `.decode()` are unaffected)
- **Release relevance**: yes. Blocks compilation on current NumPy; must be in the release.
- **Rewrite relevance**: moot (no 'a' aliases in rewrite/src)
- **Importance**: 5
- **Recommended action**: fix for next release, in both repos, and add NumPy >= 2.5 to the CI matrix.
- **Status (2026-10-17)**: fixed by labscript PR #124, labscript-devices PR #149 and blacs PR #124, merged 2026-10-17; verified by compiling the example experiment on NumPy 2.5.4 (`TESTING.md`).

---

### labscript-utils

### labscript-utils #2: labconfig should do some initialisation on config files (chrisjbillington via philipstarkey, opened 2014-10-03, last activity 2014-10-03, 0 comments)
- **Summary**: `LabConfig()` should validate the apparatus name, create analysislib/labscriptlib subfolders, check shared-drive paths, and hold all defaults in one place.
- **Type**: feature request
- **Still valid?**: n.a. `LabConfig.__init__` (`labscript-utils/labscript_utils/labconfig.py:38-93`) only reads, applies `labscript_suite` default, renames `experiment_name`, and checks required keys. Directory creation moved to `labscript-profile-create` (`labscript_profile/create.py:138-186`), which largely satisfies the original motivation at install time rather than at every instantiation.
- **Scope**: labscript-utils labconfig / profile
- **Related**: #60
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: requirement (config validation with clear errors; `rewrite/src/shotscript/config.py` exists)
- **Importance**: 1
- **Recommended action**: close as fixed by `labscript-profile-create`.

### labscript-utils #3: Unitconversions module does not belong in labscript_utils (chrisjbillington via philipstarkey, opened 2014-10-03, last activity 2014-10-04, 8 comments)
- **Summary**: Unit conversion classes are user-space code and should live in their own package (or labscript_devices), with a deprecation shim in labscript_utils.
- **Type**: feature request (packaging)
- **Still valid?**: n.a. Still at `labscript-utils/labscript_utils/unitconversions/` (11 classes). The 2014 thread converged on: keep `UnitConversionBase` in labscript_utils, let user conversions live anywhere on the import path via a registration decorator (labscript-utils #4), and move the bundled classes into `labscript_devices/unitconversions`. None of it was done; users add their own via `userlib/pythonlib`, which removed most of the pressure.
- **Scope**: packaging
- **Related**: #6
- **Effort**: medium (new package, shim, docs)
- **Release relevance**: no
- **Rewrite relevance**: requirement (unit conversions are user code; the rewrite should load them from the user's library, not ship them)
- **Importance**: 1
- **Recommended action**: close as won't fix in legacy.

### labscript-utils #6: Unitconversions base class should use different style of dynamic method creation (chrisjbillington via philipstarkey, opened 2014-10-04, last activity 2014-10-04, 0 comments)
- **Summary**: Replace `exec`'d `def` statements in `UnitConversion.__init__` with ordinary dynamic method creation.
- **Type**: feature request (code quality)
- **Still valid?**: fixed by `a3ccc40` (2018-03-02, "Replace use of exec and eval with other metaprogramming stuff"). `UnitConversionBase.py:20-37` now uses a `_MultiplicativeConversion` descriptor; no `exec`/`eval` remain in the module.
- **Scope**: labscript-utils unitconversions
- **Related**: #3
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as fixed (a3ccc40).

### labscript-utils #7: Modulewatcher: ability to blacklist modules (chrisjbillington via philipstarkey, opened 2014-10-05, last activity 2014-10-05, 1 comment)
- **Summary**: `ModuleWatcher.blacklist(name)` should mark a module (and its importers) for unconditional unloading on request, for modules with import side effects.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented. `ModuleWatcher` (`labscript_utils/modulewatcher.py:34-130`) has a whitelist only, and since `c3141fb` (2019-05-09) whitelists everything under site-packages/stdlib so only user code is ever unloaded. The whitelist is a public `set` attribute, so callers can already add to it.
- **Scope**: labscript-utils modulewatcher (used by runmanager batch compiler and lyse)
- **Related**: #23, #28; labscript #10
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: requirement (reload policy for user code; the rewrite's `importing.py` should define it explicitly)
- **Importance**: 1
- **Recommended action**: close as won't fix / superseded by the 2019 whitelist redesign.

### labscript-utils #10: Allow check_version to require only minimum version (rpanderson via philipstarkey, opened 2016-08-21, last activity 2019-05-13, 1 comment)
- **Summary**: `check_version(module, at_least, less_than)` should allow omitting the upper bound so routine dependency updates do not stop applications from starting.
- **Type**: feature request
- **Still valid?**: obsolete. chrisjbillington agreed in 2019 (upper bound should warn unless `strict=True`) and intended to do it before zprocess 3.0; it was not done, and the signature still requires `less_than` (`labscript_utils/versions.py:214`). But no suite package calls `check_version` any more (grep over labscript, labscript-utils, blacs, lyse, runviewer, labscript-devices and runmanager origin/master finds no callers; dependency bounds now live in `pyproject.toml`).
- **Scope**: labscript-utils versions
- **Related**: none
- **Effort**: trivial (`less_than=None`)
- **Release relevance**: no
- **Rewrite relevance**: moot (packaging metadata handles version constraints)
- **Importance**: 1
- **Recommended action**: close as obsolete; optionally deprecate `check_version`.

### labscript-utils #12: Units in spinbox for analog quantities (shjohnst via philipstarkey, opened 2017-06-22, last activity 2017-06-22, 2 comments)
- **Summary**: Render the unit inside the analog spinbox and change units from a right-click submenu, instead of the separate combobox, to tidy the DDS widget layout.
- **Type**: feature request (UI)
- **Still valid?**: n.a. `AnalogOutput` still uses a separate `QComboBox` for units (`labscript_utils/qtwidgets/analogoutput.py:170-205`). philipstarkey's 2017 preference: a small button next to the spinbox that opens a units menu (the right-click menu is already used for step size and lock).
- **Scope**: qtwidgets (BLACS front panels)
- **Related**: none
- **Effort**: small to medium
- **Release relevance**: no
- **Rewrite relevance**: requirement candidate for the rewrite's control UI
- **Importance**: 1
- **Recommended action**: close as won't fix, or leave open as a UI wish.

### labscript-utils #19: Command line argument to turn off double import denier (philipstarkey, opened 2018-04-30, last activity 2018-04-30, 1 comment)
- **Summary**: Add a command-line flag to disable the double import denier so users can keep working around false positives.
- **Type**: feature request
- **Still valid?**: fixed by `fb78e55` (2018-04-30, same day, flag name proposed in the only comment): `--allow-double-imports` in `sys.argv` makes `enable()`/`disable()` no-ops (`labscript_utils/double_import_denier.py:141-168`).
- **Scope**: labscript-utils
- **Related**: #87
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as fixed (fb78e55).

### labscript-utils #20: Encapsulate running external programs (chrisjbillington via philipstarkey, opened 2018-06-06, last activity 2018-06-06, 1 comment)
- **Summary**: Opening HDF5 files and text files in external programs should be one shared function (with a dialog to pick the program and write it to labconfig) instead of copies in each application.
- **Type**: feature request (refactor)
- **Still valid?**: yes. `hdf5_viewer`/`text_editor` handling is duplicated in `blacs/blacs/__main__.py`, `blacs/blacs/plugins/connection_table/__init__.py`, `lyse/lyse/__main__.py`, `lyse/lyse/filebox.py`, `lyse/lyse/routines.py` and `runmanager/__main__.py` (origin/master); nothing in labscript-utils provides it.
- **Scope**: labscript-utils + three applications
- **Related**: none
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: requirement (one helper for launching the configured editor/viewer)
- **Importance**: 2
- **Recommended action**: fix later (low-risk cleanup) or leave open.

### labscript-utils #23: ModuleWatcher: ability to append to whitelist (rpanderson via philipstarkey, opened 2019-05-09, last activity 2019-05-29, 2 comments)
- **Summary**: Reloading `tensorflow` after a user-module change crashes (protobuf cannot be re-imported); wants a way to exempt packages from reloading.
- **Type**: feature request / bug
- **Still valid?**: fixed by `c3141fb` (2019-05-09; the commit message in the thread says "This addresses issue #23, though it is different to the solution than proposed there"): modules under stdlib/site-packages are never unloaded (`modulewatcher.py:20-30`, `:84-87`), which covers tensorflow. Anything else can be added through the public `whitelist` set.
- **Scope**: labscript-utils modulewatcher; lyse
- **Related**: #7, #28
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: requirement (same as #7)
- **Importance**: 1
- **Recommended action**: close as fixed (c3141fb).

### labscript-utils #26: Add enum control widget (dihm via philipstarkey, opened 2019-09-24, last activity 2019-10-03, 4 comments)
- **Summary**: A combobox-based widget for enum-valued static device settings (SRS SG386 modulation controls), plus guidance on integrating with BLACS widget auto-creation.
- **Type**: feature request
- **Still valid?**: the widget is fixed by `5810137` (2019-10-08, "device_properties: Add EnumOutput widget type"): `labscript_utils/qtwidgets/enumoutput.py` exists. The thread grew into a larger proposal (philipstarkey 2019-09-25, endorsed by dihm): a per-device metadata class describing device/connection-table properties (name, default, type, allowed values), labscript type-checking from it, superseding `set_passed_properties`, and BLACS tabs that auto-render editable device properties with a new worker method. dihm concluded it was too large to take on. That proposal was never implemented; blacs #105 (Virtual Devices, PR-REVIEW rank 11) touches the enum output class only.
- **Scope**: qtwidgets + BLACS
- **Related**: blacs #105
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: requirement (enum-typed static channels)
- **Importance**: 1
- **Recommended action**: close as fixed for the widget (5810137); if the editable-device-properties proposal is wanted, open it as its own issue on blacs.
- **Rewrite relevance (addendum)**: requirement (device properties editable from the control UI, driven by typed property metadata; the thread is a good specification).

### labscript-utils #28: ModuleWatcher issue with import_or_reload (chrisjbillington via philipstarkey, opened 2019-12-06, last activity 2021-05-12, 2 comments)
- **Summary**: Compiling with `import_or_reload('labscriptlib.<apparatus>.connection_table')` crashes after a module has been modified. ispielma's 2020 comment supplies the traceback: `KeyError: 'labscriptlib'` raised from `_NamespacePath._recalculate` inside `double_import_denier.find_spec` at `tuple(path)`; the only recovery is restarting runmanager. zakv (2021) resolved the same crash by adding empty `__init__.py` files to the `userlib` directories.
- **Type**: bug
- **Still valid?**: yes. Mechanism: `userlib/labscriptlib/` ships an `__init__.py` but `labscriptlib/<apparatus>/` does not (`labscript_profile/default_profile/userlib/labscriptlib/example_apparatus/` has no `__init__.py`), so the apparatus package is a namespace package. `ModuleWatcher.check` whitelists any module with `__file__ is None` (`labscript_utils/modulewatcher.py:74-76`), which includes namespace packages, but unloads the regular parent package `labscriptlib`. After a user file changes, `labscriptlib.<apparatus>` survives in `sys.modules` with a `_NamespacePath` whose parent lookup `sys.modules['labscriptlib']` now fails, and the first thing to iterate that path is `tuple(path)` in `double_import_denier.find_spec` (`labscript_utils/double_import_denier.py:52`). The denier is incidental; the import system itself would raise the same `KeyError`. Plain `import labscriptlib.<apparatus>.connection_table` is affected as well, not only `import_or_reload`.
- **Severity**: crash (compile fails until runmanager is restarted; the default profile layout triggers it)
- **Scope**: labscript-utils modulewatcher + default profile; runmanager batch compiler and lyse
- **Related**: #7, #23; labscript #10
- **Effort**: trivial: (a) ship `__init__.py` in `default_profile/userlib/labscriptlib/example_apparatus/` and `analysislib/example_apparatus/` (the rename in `create_profile` keeps them); (b) in `ModuleWatcher.unload`, also delete namespace-package modules whose `__path__` is under a non-PKGDIRS location, or stop whitelisting `__file__ is None` modules that have a `__path__`; (c) guard `tuple(path)` in the denier.
- **Release relevance**: yes. A crash in the usual connection-table-import workflow on a fresh profile; independent of Python version but cheap and visible.
- **Rewrite relevance**: requirement (user-code reload policy must handle namespace packages, or the profile must create regular packages)
- **Importance**: 4
- **Recommended action**: fix for next release ((a) and (b)); keep `import_or_reload` (user scripts call it even though nothing in the suite does).
- **Status (2026-10-17)**: fixed by labscript-utils PR #129 ((a) and (b)), merged 2026-10-17; the `KeyError` was reproduced on master and does not occur with the branch.

### labscript-utils #29: Cannot autostart servers on macos Catalina (chrisjbillington via philipstarkey, opened 2019-12-06, last activity 2019-12-06, 0 comments)
- **Summary**: Applications cannot auto-start zlock/zlog on macOS Catalina; starting the servers manually works.
- **Type**: bug
- **Still valid?**: cannot verify (no macOS here). Mechanism unchanged: `connect_to_zlock_server`/`ensure_connected_to_zlog` (`labscript_utils/ls_zprocess.py:323-388`) call `zprocess.start_daemon`, which on POSIX does `os.fork()` in the running GUI process and `os.setsid()` in the child (`zprocess/zprocess/utils.py:117-146`). Forking a process that has initialised Cocoa/Qt is exactly what macOS >= 10.15 aborts (the `OBJC_DISABLE_INITIALIZE_FORK_SAFETY` crash), so the report is consistent with current code. A fix is to drop the fork and use `subprocess.Popen(start_new_session=True)`.
- **Severity**: annoyance (manual server start works)
- **Scope**: zprocess + labscript-utils; macOS only
- **Related**: none
- **Effort**: small (in zprocess)
- **Release relevance**: yes if macOS is a supported platform for the release; otherwise no.
- **Rewrite relevance**: requirement (service auto-start must not fork a GUI process; `rewrite/src/shotscript/server.py` should spawn, not fork)
- **Importance**: 2
- **Recommended action**: fix later in zprocess (`Popen(start_new_session=True)`), ask a macOS user to test.

### labscript-utils #60: Load example_experiment.py on first run of runmanager (rpanderson, opened 2020-06-25, last activity 2020-06-25, 0 comments)
- **Summary**: Ship `app_saved_configs/example_apparatus/runmanager/runmanager.ini` in the default profile so runmanager opens the example experiment on first run; path needs generating or interpolation.
- **Type**: feature request (out-of-the-box experience)
- **Still valid?**: yes. `labscript_profile/default_profile/app_saved_configs/` contains only a README; the example labconfig points `autoload_config_file` at `%(app_saved_configs)s\runmanager\runmanager.ini` (`default_profile/labconfig/example.ini:58-59`) and runmanager tries to load it and prints "Could not load config file" when absent (`runmanager/__main__.py:990-1006` on origin/master). `load_appconfig` uses `interpolation=None`, so the file must contain an absolute path, i.e. it must be written by `labscript-profile-create`.
- **Scope**: labscript-utils profile + runmanager
- **Related**: #116 / PR #117 (same goal, analysis side); #2
- **Effort**: small (write the ini in `create_profile` with the expanded path)
- **Release relevance**: no (but it affects first impressions of the release)
- **Rewrite relevance**: requirement (first-run experience: example apparatus loads without manual steps)
- **Importance**: 3
- **Recommended action**: fix for next release together with #116/#117 (cheap, visible).
- **Status 2026-10-18**: fixed in labscript-utils #133 (merged 2026-10-18); `labscript-profile-create` writes the file.

### labscript-utils #68: FileWatcher has thread unsafe attributes exposed (philipstarkey, opened 2020-10-14, last activity 2020-10-14, 0 comments)
- **Summary**: `FileWatcher.files`/`folders` are public but mutated under an internal lock; rename to private and clean up.
- **Type**: feature request (code quality)
- **Still valid?**: yes. `self.files`, `self.folders`, `self.lock` remain public (`labscript_utils/filewatcher.py:54-60`); only a 2021 docs commit touched the file since.
- **Scope**: labscript-utils; used by labscript (`labscript.py:37`) and BLACS connection-table plugin
- **Related**: none
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as won't fix, or fix opportunistically.

### labscript-utils #87: When I'm trying to use FlyCapture2Camera, double import error in blacs (Moriaty-TT, opened 2022-05-19, last activity 2022-05-27, 14 comments)
- **Summary**: The double import denier reports `user_devices` and `PyCapture2` as the same file, path `C:\Users\Administrator\namespace`, on Python 3.6.
- **Type**: bug report / support
- **Still valid?**: obsolete. philipstarkey and chrisjbillington diagnosed it in the thread: on Python 3.6/3.7 a namespace package spec has `origin == 'namespace'` (changed to `None` in CPython 3.8), and the denier does `os.path.realpath(spec.origin)` (`double_import_denier.py:64-65`), so the empty `user_devices` package and the not-yet-found `PyCapture2` both map to `<cwd>\namespace`. The reporter confirmed that patching line 64 with `and spec.origin != "namespace"` fixed it; the follow-up PyCapture2 bus error was split into another issue. The agreed one-line guard was never committed (last change to the file is `96c8c11`, 2020-04-28). With Python < 3.11 dropped it cannot recur.
- **Severity**: was crash on Python 3.6
- **Scope**: labscript-utils double_import_denier; Python 3.6 only
- **Related**: #19
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as obsolete (Python < 3.8); the agreed guard is harmless to add but unnecessary.

### labscript-utils #100: `imp` module removed from new python (ispielma, opened 2024-02-09, last activity 2024-03-18, 6 comments)
- **Summary**: `imp` is removed in Python 3.12; used in device_registry, double_import_denier and modulewatcher (for the global import lock).
- **Type**: bug
- **Still valid?**: fixed. The thread records the path: PR #101 (ispielma) hot-fixed with `import _imp as imp`, which broke BLACS device-registry discovery (`_imp.find_module` does not exist, dihm 2024-03-18); dihm then rewrote `populate_registry` with `importlib.machinery.PathFinder.find_spec` + `exec_module`, which is what master has (`labscript_utils/device_registry/_device_registry.py:262-264`), and `189c3cf` (2024-04-04) removed the import locks from modulewatcher. Shipped in v3.4.0rc1 and later; no `import imp` remains in labscript-utils or labscript (grep).
- **Severity**: was crash on Python >= 3.12
- **Scope**: labscript-utils
- **Related**: labscript #104/#123 (same class: modern-Python breakage)
- **Effort**: n.a.
- **Release relevance**: already done; note in release notes that 3.12+ works.
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as fixed (189c3cf, v3.4.0).

### labscript-utils #104: labscript_utils.excepthook uses tk (ispielma, opened 2024-02-27, last activity 2024-02-28, 3 comments)
- **Summary**: Why does the excepthook use Tk when the suite is Qt; two GUI toolkits waste resources.
- **Type**: question / feature request
- **Still valid?**: answered in the thread. philipstarkey: Tk was chosen because it ships with Python and still shows a window when the exception is a Qt problem; the dialog runs in a subprocess (`labscript_utils/excepthook/__init__.py:24`, `:72-73` spawn `tk_exception.py`) so a crashing parent does not hide it, so some GUI library must be imported from scratch either way. chrisjbillington: Debian/Ubuntu split tkinter into a separate package, so the dialog silently fails to appear there. ispielma's actual motivation was lyse popping up windows for errors already shown in its output box; chrisjbillington's answer is to catch and print those exceptions where they occur rather than change the hook.
- **Scope**: labscript-utils excepthook; all applications
- **Related**: none
- **Effort**: small (fall back to stderr when `tkinter` is missing; or port the dialog to a Qt subprocess)
- **Release relevance**: minor: check `tkinter` availability on the supported Pythons and document the dependency.
- **Rewrite relevance**: requirement (error reporting must not depend on the GUI toolkit's state; a subprocess dialog or terminal fallback)
- **Importance**: 2
- **Recommended action**: close as answered; optionally add a stderr fallback when tkinter is absent, and check lyse for the context that produced popups.

### labscript-utils #116: Example "out of the box" analysis script in userlib (Json-To-String, opened 2025-08-05, last activity 2025-08-05, 0 comments)
- **Summary**: The default profile's only lyse example (`example_IMAQdx_remote.py`) needs remote BLACS; wants a minimal analysis script using only the dummy pseudoclock/intermediate device so a fresh install runs end to end.
- **Type**: docs / tooling
- **Still valid?**: yes. `default_profile/userlib/analysislib/example_apparatus/` contains only `example_IMAQdx_remote.py`.
- **Scope**: labscript-utils default profile
- **Related**: PR labscript-utils #117 (PR-REVIEW rank 8, importance 3: "merge after fixing the `save_result` TypeError and axis label"); #60
- **Effort**: trivial (merge #117 with the two fixes)
- **Release relevance**: no, but it is the end-to-end smoke test for the release's fresh-install path.
- **Rewrite relevance**: requirement (example apparatus with an analysis routine that runs out of the box)
- **Importance**: 3
- **Recommended action**: fix for next release by merging PR #117; close this with it.

---

### Ranked table

| Rank | Issue | Type | Importance | Recommended action |
|---|---|---|---|---|
| 1 | labscript #123 'a256' dtype fails on NumPy >= 2.5 | bug | 5 | Fixed 2026-10-17 by labscript #124, labscript-devices #149 and blacs #124; issue closed. Add NumPy 2.5 to CI |
| 2 | labscript #104 remove pylab star import | feature/compat | 4 | fixed in labscript #130 (opened 2026-10-18): star import removed with no re-exports; listed at the top of the release notes (maintainer decision 2026-10-18) |
| 3 | labscript #52 duplicate output connection is silent | bug | 4 | fixed in labscript #128 (merged 2026-10-18); issue closed |
| 4 | labscript #43 collision errors do not name outputs | feature | 4 | fixed in labscript #128 (merged 2026-10-18); issue closed |
| 5 | labscript #41 no test suite | tooling | 4 | Fix for next release at smoke-test level |
| 5a | labscript #95 idle clockline exceeds PrawnBlaster max period; no range check | bug | 4 | fixed in labscript-devices #153 (merged 2026-10-18): range check with a `LabscriptError`; issue closed. A general max-period fix is not done |
| 5b | labscript-utils #28 namespace apparatus package crashes compile after a file change | bug | 4 | Fix for next release: ship `__init__.py` in profile, fix ModuleWatcher whitelist |
| 6 | labscript #16 ramp limit check has no tolerance | bug | 3 | fixed in labscript #128 (merged 2026-10-18); issue closed |
| 7 | labscript-utils #60 runmanager.ini in default profile | feature | 3 | fixed in labscript-utils #133 (merged 2026-10-18); issue closed |
| 8 | labscript-utils #116 minimal analysis example | docs | 3 | Merge PR #117, close |
| 10 | labscript #50 wait_delay not applied to resume trigger | bug | 3 | Fix later; ask labs with secondary PulseBlasters |
| 11 | labscript #44 limits not saved for BLACS | feature | 3 | Fix later (labscript half with #16) |
| 12 | labscript #6 clocklines coupled during ramps | feature | 2 | Leave open as canonical limitation issue |
| 13 | labscript #2 shutter reordering | bug | 2 | Close as won't fix in legacy (deferred to v3 in 2017) |
| 14 | labscript #3 shutter timing model | feature | 2 | Close; rewrite input |
| 15 | labscript #4 reject instructions before last wait | feature | 2 | Fix later; delete dead check at outputs.py:364-375 |
| 16 | labscript #10 imported connection table not re-run | bug | 2 | Fix later per 2014 plan (unload device-defining modules), or docs |
| 17 | labscript #18 in-shot analysis scripts | proposal | 2 | Close; rewrite analysis design supersedes |
| 18 | labscript #32 BLACS error policy | proposal | 2 | Close here (wrong repo) |
| 19 | labscript #34 ramp splitting | feature | 2 | Close as duplicate of #6 |
| 20 | labscript #36 safe idle state with timeout | proposal | 2 | Close; rewrite input |
| 21 | labscript #54 constant with duration | feature | 2 | Fix later or close; rewrite input |
| 22 | labscript #109 Trigger ignores `inverted` | bug | 2 | Fix later (error when both given) |
| 23 | labscript-utils #20 shared "open external program" helper | feature | 2 | Fix later |
| 24 | labscript-utils #29 macOS autostart (fork in GUI process) | bug | 2 | Fix later in zprocess, needs macOS tester |
| 25 | labscript-utils #104 excepthook uses Tk | question | 2 | Close as answered; optional stderr fallback |
| 26 | labscript #5 instruction time tolerance | feature | 1 | Close |
| 27 | labscript #7 nested loops | feature | 1 | Close |
| 28 | labscript #11 builtins injection | feature | 1 | Close as won't fix (decided 2014) |
| 29 | labscript #15 empty connection table | bug | 1 | Close as fixed after one compile check |
| 30 | labscript #21 live in-shot feedback | proposal | 1 | Close |
| 31 | labscript #39 short ticks during ramps | bug | 1 | Close as fixed (a9888d5) |
| 32 | labscript #42 loop recognition | feature | 1 | Close as answered (`repeat_pulse_sequence`) |
| 33 | labscript #45 restructure properties/BLACS_connection | proposal | 1 | Close |
| 34 | labscript #49 set_passed_properties on outputs | feature | 1 | Close as stale |
| 35 | labscript #53 pseudoclock/clockline collision | support | 1 | Close as fixed by a9888d5, link #6/#43 |
| 36 | labscript #96 NI 6535 PFI4 impedance | support | 1 | Close as resolved (reporter confirmed) |
| 37 | labscript #105 type hints | feature | 1 | Close or leave open low priority |
| 38 | labscript #108 integer times | design | 1 | Close; rewrite uses Fractions |
| 39 | labscript #112 timing limited by slow component | support | 2 | Convert to docs (gated clocks page), close |
| 40 | labscript-utils #2 labconfig initialisation | feature | 1 | Close as fixed by labscript-profile-create |
| 41 | labscript-utils #3 unitconversions location | feature | 1 | Close |
| 42 | labscript-utils #6 exec in UnitConversion | feature | 1 | Close as fixed (a3ccc40) |
| 43 | labscript-utils #7 ModuleWatcher blacklist | feature | 1 | Close as superseded |
| 44 | labscript-utils #10 check_version minimum only | feature | 1 | Close as obsolete (no callers) |
| 45 | labscript-utils #12 units inside spinbox | feature | 1 | Close or leave open |
| 46 | labscript-utils #19 flag to disable denier | feature | 1 | Close as fixed (fb78e55) |
| 47 | labscript-utils #23 ModuleWatcher whitelist | feature | 1 | Close as fixed (c3141fb) |
| 48 | labscript-utils #26 enum widget | feature | 1 | Close as fixed (5810137); larger proposal to blacs if wanted |
| 50 | labscript-utils #68 FileWatcher public attributes | cleanup | 1 | Close or fix opportunistically |
| 51 | labscript-utils #87 double import on Python 3.6 | bug | 1 | Close as obsolete |
| 52 | labscript-utils #100 `imp` removed | bug | 1 | Close as fixed (189c3cf, v3.4.0) |

### Release-relevant issues

- labscript #123: `'a256'` dtypes fail on NumPy >= 2.5; compilation is impossible. Four sites in labscript, six files in labscript-devices. Fixed 2026-10-17 by labscript #124, labscript-devices #149 and blacs #124; issue closed.
- labscript #104: `from pylab import *` in `labscript.py` and `functions.py`; the docs build already needed `numpy<2`. Decide the compatibility policy in the Python 3.11+ release.
- labscript #41: no automated tests; a compile smoke test across the supported Python/NumPy matrix is the cheapest guard against the two items above.
- labscript #95: NumPy 2 turns the PrawnBlaster `half_period` overflow (idle clockline longer than 42 s) from a crash into silent truncation; add dtype and range check in labscript-devices. Fixed in labscript-devices #153 (merged 2026-10-18).
- labscript-utils #28: compile crashes (`KeyError: 'labscriptlib'`) after editing a file when the apparatus directory is a namespace package, which is how `labscript-profile-create` lays it out; ship `__init__.py` and fix the ModuleWatcher whitelist. Fixed by labscript-utils #129, merged 2026-10-17; issue closed.
- labscript-utils #29: zprocess `start_daemon` forks the GUI process; relevant only if macOS is a release target.
- labscript-utils #104: Tk excepthook subprocess needs `tkinter`; confirm availability on the supported Pythons or add a stderr fallback.
- labscript-utils #100: already fixed (v3.4.0); mention Python 3.12+ support in release notes.
- labscript-utils #60 and #116 (PR #117): first-run experience of the release; both small.

## 3.x Issue triage: labscript-devices, PrawnBlaster, prawn_digital_output

Triaged 2026-10-17. 28 + 2 + 5 = 35 open issues.

Sources: the full conversation of every issue (opening post, comments, events) from
`scratchpad/issues/<repo>_<N>.txt`, plus the `.json` metadata. Revised 2026-10-17 after
the comment text became available; the revision notes at the end list what changed.

Code checked on the working trees: labscript-devices `master` at 424b9f4 (2026-04-07),
PrawnBlaster `master` at 1a8c07a (2025-12-11), prawn_digital_output `main` at 3fecbdd
(2025-12-31). Hardware-dependent behaviour could not be reproduced; for every bug the
code path was inspected instead.

Open PRs referenced from PR-REVIEW.md section 1: labscript-devices #148
(TriggerableCamera + DummyCamera), #144 (Andor fixes), #110 (Windfreak), #126 (AD9959),
#129 (Keysight scope), #106 (GeniCam), #87, #63, #53, #130; PrawnBlaster #37
(overclock voltage), #35 (variable instructions per pseudoclock); prawn_digital_output
#23 (testing notebook).

---

### labscript-devices

### labscript-devices #131: IMAQdx Camera worker fails if Numpy >= 2.0 (mjdoris, opened 2025-06-19, last activity 2025-11-19, 2 comments)
- **Summary**: `dset.attrs['CLASS'] = np.string_('IMAGE')` in `IMAQdxCamera/blacs_workers.py` raises `AttributeError` under NumPy 2, because `np.string_` was removed.
- **Type**: bug
- **Still valid?**: fixed. Commits b40cf0d (2025-11-15, `np.string_` to `np.bytes_` in `IMAQdxCamera/blacs_workers.py:483-485`) and 9fde1c0 (2025-11-18, same in `imaqdx_server.py:42,393-395` and `RFBlaster.py:186`), merged as PR #135; the second commenter (rogding, 2025-11-19) confirmed "resolved with PR #135". The issue was simply never closed. No `np.string_`, `np.float`, `np.int`, `np.bool`, `np.unicode_` or `np.NaN` remain in the package. One NumPy 2 defect remains elsewhere: `LightCrafterDMD.py:348` and `:359` call `ndarray.tostring()`, which NumPy 2 removed (verified with NumPy 2.5.4: the attribute is absent), so `LightCrafterDMD.transition_to_buffered` raises `AttributeError`. Replace with `tobytes()`.
- **Severity**: crash (fixed for cameras; still crash for LightCrafterDMD)
- **Scope**: IMAQdxCamera and every camera subclass; LightCrafterDMD
- **Related**: PR #106 (GeniCam) still uses `np.string_` per PR-REVIEW.md.
- **Effort**: trivial (the LightCrafter fix is two lines)
- **Release relevance**: yes. NumPy 2 is the default on Python 3.11-3.15; the camera fix must ship, and the LightCrafter `tostring()` calls should be fixed in the same release. `pyproject.toml:30-45` still says `numpy>=1.15.1` with no upper bound, which is right once these are fixed.
- **Rewrite relevance**: moot (shotscript targets NumPy 2 from the start).
- **Importance**: 4. The reported bug is fixed but unreleased; the remaining `tostring()` crash is the same class of defect.
- **Recommended action**: close as fixed; fix `LightCrafterDMD.py` `tostring()` for the next release.

### labscript-devices #124: To use TS/pin 10 to switch Channel 1 and 0 parameters in timing with the Novatech DDS9m (wxccl, opened 2025-03-03, last activity 2025-03-03, 1 comment)
- **Summary**: User asks how labscript drives the DDS9m table mode, given that pin 10 (TS) advances on a falling edge while the pseudoclock produces rising edges.
- **Type**: question-support
- **Still valid?**: n.a. philipstarkey answered the same day with the archived blog post (an inverter is not enough; pin 10 and pin 14 need different edges, hence the tri-state driver circuit). The same content is in the repository: `docs/source/devices/novatechDDS9m.rst:30-43` describes the circuit (falling edge on pin 10 loads the buffer, rising edge on pin 14 outputs it), and `NovaTechDDS9M.py:207-225` explains the `update_mode` ('synchronous'/'asynchronous') and `synchronous_first_line_repeat` options that duplicate the first table row to compensate for the half-cycle offset. No reply from the reporter.
- **Scope**: NovaTechDDS9M, hardware wiring
- **Related**: none
- **Effort**: trivial
- **Release relevance**: no
- **Rewrite relevance**: none (hardware wiring note; the shotscript NovaTech driver, if any, should carry the same documentation).
- **Importance**: 1
- **Recommended action**: close with a pointer to the docs page and the `update_mode` argument.

### labscript-devices #117: Allow Prawnblaster to be triggered directly by a Pseudoclock (dihm, opened 2024-06-21, last activity 2024-06-21, 0 comments)
- **Summary**: labscript forbids triggering a secondary pseudoclock from a device that is not clocked by the master, so a PrawnBlaster cannot hang off a PrawnDO. Request: let a PrawnBlaster take a `clock_line` parent the way PrawnDO does, so pseudoclocks and PrawnDOs can fan out from one parent PrawnBlaster.
- **Type**: feature request
- **Still valid?**: n.a. (feature). The restriction is `labscript/labscript/core.py:769-774`. PrawnDO already implements the requested pattern: `PrawnDO/labscript_devices.py:144-219` accepts `clock_line=` and builds an internal `_PrawnDOIntermediateDevice` (`:318-321`, allowed child `Trigger`) on that clockline. `PrawnBlaster/labscript_devices.py:174-252` has only `trigger_device`/`trigger_connection`.
- **Scope**: PrawnBlaster labscript class; needs hardware test (trigger pulse width from a clockline tick vs. `trigger_minimum_duration`)
- **Related**: PrawnBlaster #31 / PR #35 (instruction allocation for fan-out topologies)
- **Effort**: small (copy the PrawnDO pattern), plus a hardware test
- **Release relevance**: no
- **Rewrite relevance**: requirement. shotscript's device graph should allow pseudoclocks to be triggered from any clocked output, not only from devices on the master pseudoclock; the two-level rule is a legacy labscript limitation.
- **Importance**: 3. Real topology limitation with a known cheap solution.
- **Recommended action**: fix later.

### labscript-devices #109: PrawnBlaster runviewer parser drops first instruction after a wait with timeout (dihm, opened 2023-12-20, last activity 2023-12-21, 0 comments)
- **Summary**: In the runviewer parser's wait handling, the `elif last_instruction_was_wait:` branch skips the instruction after every wait, not only the second half of an indefinite wait.
- **Type**: bug
- **Still valid?**: yes. `PrawnBlaster/runviewer_parsers.py:97-110`, unchanged since 0af6f83 (2021-07-24). Line 104 is `elif last_instruction_was_wait:` and `continue`s, so any non-wait row following a wait is dropped. The fix in the issue (`elif row["reps"] == 0 and last_instruction_was_wait:`) is correct: an indefinite wait is encoded as two consecutive `reps == 0` rows.
- **Severity**: wrong-behaviour (runviewer display only; hardware output unaffected)
- **Scope**: PrawnBlaster runviewer parser, any shot with waits
- **Related**: none
- **Effort**: trivial
- **Release relevance**: yes, in the sense that it is a one-line fix to a confirmed bug that should go into the release.
- **Rewrite relevance**: requirement. Any shotscript trace decoder for PrawnBlaster programs must treat two consecutive `reps == 0` rows as one indefinite wait.
- **Importance**: 4. Confirmed by code reading, trivial fix, affects every runviewer view of a shot with waits.
- **Recommended action**: fix for next release.

### labscript-devices #107: PrawnBlaster Potential Bug with Waits (pmiller2022, opened 2023-08-04, last activity 2023-08-27, 2 comments)
- **Summary**: With waits in the program, the BLACS shot lasts the full wait timeout even though the external retrigger arrives earlier and the experiment finishes. Asks whether labscript can stop the PrawnBlaster early.
- **Type**: bug / question-support
- **Still valid?**: cannot verify (hardware). Code path: the firmware resumes a wait on an edge on the pseudoclock's `in_pin` (default GPIO 0 for all four pseudoclocks, `PrawnBlaster/labscript_devices.py` `in_pins` default) and the BLACS worker polls `status` until idle (`PrawnBlaster/blacs_workers.py:164-261`). The tab's `status_monitor` (`PrawnBlaster/blacs_tabs.py:121-151`) polls every 100 ms during a run and reports "done" as soon as the firmware is idle and all waits have been read out; the firmware writes the wait result by DMA when the wait ends (retrigger or timeout, `prawnblaster.cpp:383,826-850`). So a shot that always runs to the timeout means the retrigger was not detected by the firmware (wrong pin, wrong edge, or a pulse shorter than the minimum trigger duration, see the readme FAQ), not a host-side defect.
  Comments: philipstarkey asked for details (2023-08-27); dihm replied the same day that it was "fairly easy to reproduce" with the PrawnBlaster as the only pseudoclock, a minimal program and a 4 s wait timeout, and that BLACS always waits the full 4 s, adding that the BLACS shot-timing plugin reports the shot length as including the wait timeout and that it "probably indicates something more BLACS related"; he said he would check on a PulseBlaster. His description does not say that a retrigger was supplied; without one, running to the timeout is the correct behaviour. No follow-up since.
- **Severity**: wrong-behaviour if real
- **Scope**: PrawnBlaster hardware trigger input; possibly BLACS shot-timing plugin
- **Related**: #109
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: ask dihm whether his reproduction included a retrigger and whether the PulseBlaster comparison was done; if the retrigger was present, test on hardware; otherwise close.

### labscript-devices #104: Project structure for adding new devices (TerryGeng, opened 2023-03-27, last activity 2025-08-25, 8 comments)
- **Summary**: Every new device adds dependencies (sometimes vendor binaries) to one monolithic package. Proposes namespace packages (`labscript_devices.<device>` as separate pip packages) or git submodules.
- **Type**: meta / proposal
- **Still valid?**: n.a. Current state: out-of-tree devices are supported through the `user_devices` labconfig setting (`labscript_utils/device_registry/_device_registry.py:75-82`, any list of importable packages) and documented in `docs/source/user_devices.rst`. `pyproject.toml:30-45` lists PyDAQmx, PyNIVision, PyVISA, spinapi, pyserial as hard dependencies and has no per-device extras (`[project.optional-dependencies]` at `:59-65` contains only `docs`).
  Discussion (8 comments, 2023-03 to 2025-08): philipstarkey pointed to `user_devices` and suggested experimenting outside the main repo; ispielma and dihm split the problem into (1) packaging of non-core devices and (2) dependency checking inside workers (philipstarkey: keep checks in the worker process, friendlier `try/except ImportError` messages; DLL paths belong in labconfig, not the connection table); dihm argued `user_devices` must stay and listed open questions (conda, editable installs, the runmanager/blacs hard dependency on labscript_devices, device_registry). On 2025-08-25 Json-To-String reported that naqslab implemented the PEP 420 namespace-package approach as `naqs_devices` (template device, docs) "with the plan to eventually move `labscript_devices` to a namespace package", installed per device with pip plus the parent namespace in `user_devices`. No maintainer response to that yet.
- **Scope**: packaging, whole repo
- **Related**: #22 (same proposal, 2017), #49 (missing dependencies), #6 (done), PR #148 (reduces camera duplication, which is what GeniCam #106 and DMD work would build on)
- **Effort**: medium (per-device extras is small; a namespace-package split is large)
- **Release relevance**: yes, partially: declaring per-device optional extras and demoting PyNIVision/PyDAQmx/spinapi to extras is release-sized packaging work and makes installation on Linux/macOS and Python 3.13+ cleaner.
- **Rewrite relevance**: requirement. shotscript device drivers should be installable as separate distributions (entry points), each declaring only its own dependencies.
- **Importance**: 3
- **Recommended action**: leave open; do the extras part for the release, and reply to the 2025-08 `naqs_devices` proposal with a decision on whether `labscript_devices` itself will become a namespace package (a breaking packaging change that should not be bundled into this release).

### labscript-devices #100: PyCapture2 error (philipstarkey, opened 2022-05-27, last activity 2022-09-25, 3 comments)
- **Summary**: Moved from labscript-utils #87. FlyCapture2 worker fails at `bus.getCameraFromSerialNumber()` with `Fc2error: Bus Master Failure` and BLACS reports "Device failed to initialise".
- **Type**: question-support
- **Still valid?**: diagnosed in the thread. dihm suggested switching to Spinnaker/PySpin (FlyCapture2 is deprecated and pins Python 3.6); the original reporter gave up (2022-06-01). chrisjbillington (2022-09-25) hit the same error and found the cause: the serial number had been given as a string where an integer is expected, and nothing raises a `TypeError`. Current code: `IMAQdxCamera/labscript_devices.py:162-163` converts a `str` serial with `int(serial_number, 16)`, so a decimal string is silently reinterpreted as hex and the camera lookup fails with the SDK's opaque "Bus Master Failure" at `FlyCapture2Camera/blacs_workers.py:80`. Not a crash in labscript code, but the error is misleading.
- **Scope**: FlyCapture2Camera (and any IMAQdxCamera subclass given a decimal-string serial), Point Grey SDK
- **Related**: none
- **Effort**: trivial (catch `Fc2error` around `getCameraFromSerialNumber` and raise "camera with serial number 0x... not found; `serial_number` must be an int or a hex string", or document the hex interpretation in the `serial_number` docstring at `labscript_devices.py:74`)
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close with the diagnosis; optionally improve the error message or docstring.

### labscript-devices #91: NI-6738 AO sample clock too high (dihm, opened 2021-12-14, last activity 2021-12-14, 0 comments)
- **Summary**: The 6738's 1 MS/s AO rate applies only with one channel per bank of four; two channels in one bank limit the rate to 350 kS/s, and the driver errors at `transition_to_buffered`. Workaround: use one AO per bank or pass `max_AO_sample_rate=400e3`. Author calls it a cautionary note.
- **Type**: bug (capability model) / docs
- **Still valid?**: yes. `NI_DAQmx/models/capabilities.json` entries `PCIe-6738` and `PXIe-6738` give `max_AO_sample_rate: 1000000.0` with no bank information; `NI_DAQmx/labscript_devices.py` has no per-bank check; `docs/source/devices/ni_daqs.rst` does not mention it.
- **Severity**: annoyance (clear DAQmx error at transition time, documented workaround)
- **Scope**: NI_DAQmx, 6738 only (and possibly other 67xx 32-channel boards)
- **Related**: none
- **Effort**: small (a compile-time check in `NI_DAQmx.add_device`/`generate_code`: if two AO connections share a bank `ao4k..ao4k+3` and `clock_limit > 350e3`, raise with the workaround text; or document it in `ni_daqs.rst`)
- **Release relevance**: no
- **Rewrite relevance**: requirement. The shotscript device capability model should be able to express rate limits that depend on channel combinations, not only a single per-device number.
- **Importance**: 2
- **Recommended action**: convert to docs (add to `ni_daqs.rst`), optionally add the compile-time check later.

### labscript-devices #79: PulseblasterESRPRO500 no runviewer_parser and short pulse feature (AllenNCC, opened 2021-06-28, last activity 2021-06-30, 6 comments)
- **Summary**: `PulseBlasterESRPro500.py` registers no runviewer parser, so runviewer shows no channels; the reporter copied the parser from the ESRPro200 file. Also asks for the SpinCore "short pulse" feature.
- **Type**: bug (parser) + feature request (short pulse)
- **Still valid?**: yes, and the thread widens it. `PulseBlasterESRPro500.py` is 37 lines and ends after the worker class; `PulseBlasterESRPro200.py:38-41` has the `@runviewer_parser` subclass of `PulseBlaster_No_DDS_Parser` that the 500 file lacks. Second problem from the comments: `PulseBlasterESRPro500.py` sets `n_flags = 21` and `num_DO = 21`, but on the ESR-PRO boards of matth2peters and dihm no output appears at all unless flags 21-23 (the short-pulse control bits, manual p. 27) are exposed and set high; both run a local copy with `n_flags = 24`, `num_DO = 24` and a parser with `num_flags = 24` (dihm's snippet, 2021-06-29). philipstarkey confirmed the shipped class was tested on a loaned board that did not need those flags, so firmware differs between boards; dihm proposed making flag count and clock speed constructor arguments instead of adding subclasses. The reporter's own board is an old PulseBlaster re-flashed with ESR-PRO-500-like firmware without short pulses. matth2peters' separate runviewer problem (only the clockline appears) was not resolved in the thread.
- **Severity**: wrong-behaviour (runviewer parser missing); no output at all on boards that need flags 21-23 (hardware/firmware dependent)
- **Scope**: PulseBlaster ESR-PRO-500 (and ESR-PRO-200, same structure)
- **Related**: none
- **Effort**: trivial for the parser (4 lines); small to add an `n_flags`/`num_DO` option (24 with flags 21-23 user-controlled) or simply set 24 as `PulseBlaster_No_DDS.py:26,72` already does; medium for a proper short-pulse API
- **Release relevance**: yes (trivial confirmed fix; the 24-flag change is small and documented by two users).
- **Rewrite relevance**: none
- **Importance**: 3. Cheap confirmed fix plus a small, user-verified change.
- **Recommended action**: fix for next release: add the parser and expose 24 flags (document that flags 21-23 must be high on short-pulse-capable firmware); leave the short-pulse timing feature as won't fix.

### labscript-devices #69: Make tekscope a triggerable device (chrisjbillington, opened 2020-09-21, last activity 2020-09-21, 0 comments)
- **Summary**: TekScope should be a `TriggerableDevice` so scripts call `scope.trigger(t)` instead of toggling a separately tracked DO.
- **Type**: feature request
- **Still valid?**: n.a. `TekScope/labscript_devices.py:3` still subclasses `Device`.
- **Scope**: TekScope; the Keysight PR has the same shape
- **Related**: PR #129 (Keysight oscilloscope) would be the second instance of the pattern.
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: requirement. Acquisition instruments in shotscript should be triggerable devices with explicit trigger calls.
- **Importance**: 2
- **Recommended action**: fix later (or request it as part of the #129 review so both scopes share a base).

### labscript-devices #68: IMAQdxCamera manual_mode_camera_attributes should not be limited to those in Basler_camera_imaqdx_attributes (ispielma, opened 2020-09-15, last activity 2020-09-15, 0 comments)
- **Summary**: Every key of `manual_mode_camera_attributes` must also be in `camera_attributes`, but some attributes (e.g. `ExposeTimeRaw`) are only writable in a mode used in manual operation and not in the buffered configuration, so they cannot be listed in `camera_attributes` at all.
- **Type**: bug (design limitation)
- **Still valid?**: yes. `IMAQdxCamera/labscript_devices.py:170-176` raises `ValueError` for any manual-only key. The restriction exists so that `transition_to_buffered` (`blacs_workers.py`, `set_attributes_smart(camera_attributes)`) resets what manual mode changed; a manual-only attribute would otherwise persist into buffered mode.
- **Severity**: wrong-behaviour (prevents a valid configuration)
- **Scope**: IMAQdxCamera and all subclasses
- **Related**: PR #148 restructures the camera base class; PR-REVIEW.md does not record that it lifts this check, so the issue is not addressed by it.
- **Effort**: small to medium: drop the check and have the worker read the camera's current values of the manual-only keys before applying them in `transition_to_manual`, then restore those values in `transition_to_buffered` before applying `camera_attributes`. Needs a camera to test ordering constraints between attributes.
- **Release relevance**: no
- **Rewrite relevance**: requirement. Separate manual and buffered attribute sets with worker-side save/restore, and apply attributes in dictionary order so mode-dependent keys can be sequenced.
- **Importance**: 3
- **Recommended action**: fix later, ideally on top of #148.

### labscript-devices #66: Tekscope with multiple devices (ARFritsch, opened 2020-08-27, last activity 2020-08-27, 0 comments)
- **Summary**: With two scopes, the second `create_group('/data/traces')` fails because the group exists.
- **Type**: bug
- **Still valid?**: fixed. 259ea85 (2024-06-25, spielman) changed it to `require_group` at `TekScope/blacs_workers.py:65`.
- **Severity**: crash (fixed)
- **Scope**: TekScope
- **Related**: PR #129 (Keysight) reintroduces `create_group('/data/traces')` per PR-REVIEW.md; same fix needed there.
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot (shotscript data layout gives each device its own group).
- **Importance**: 1
- **Recommended action**: close as fixed.

### labscript-devices #55: Implement mock flag for more devices (rpanderson, opened 2020-06-15, last activity 2020-06-15, 1 comment)
- **Summary**: Proposes a `mock=True` option on more devices (as IMAQdxCamera has) so workflows can be exercised without hardware, as an alternative to dedicated dummy devices.
- **Type**: proposal
- **Still valid?**: n.a. Only IMAQdxCamera (and subclasses via `MockCamera`) and ZaberStageController (`ZaberStageController/labscript_devices.py:79`) have `mock`.
- **Scope**: all devices
- **Related**: PR #148 removes the `mock` kwarg from the camera class (PR-REVIEW.md item: keep it); PR #53 (DummyIntermediateDevice widgets); #104.
- **Effort**: large across the package
- **Release relevance**: no
- **Rewrite relevance**: requirement. shotscript should require a simulation backend for every device driver so sequences can be compiled and run end to end without hardware; this replaces per-device `mock` flags.
- **Importance**: 2
- **Recommended action**: leave open as a design record for the legacy suite; make sure #148 keeps `mock`.

### labscript-devices #49: Declare missing dependencies (rpanderson, opened 2020-05-22, last activity 2021-10-22, 1 comment)
- **Summary**: Dependencies such as the Zaber API, pyvisa and OpalKelly are used but not declared.
- **Type**: tooling / packaging
- **Still valid?**: yes, partially. dihm (2021-10-22) noted it was partially addressed in docs commit 45a54ed (per-device Installation sections in `docs/source/devices/*.rst` now name the SDKs) and added PySpin and pypylon to the non-pip list. `pyproject.toml:30-45` now declares PyVISA, PyNIVision, PyDAQmx, spinapi, pyserial, pillow, tqdm. Still undeclared: `zaber.serial` (`ZaberStageController/blacs_workers.py`), `ok` (OpalKelly, not on PyPI), `PyCapture2` and `PySpin` (vendor wheels, not on PyPI), `pypylon` (on PyPI). The inverse problem also exists: PyNIVision, PyDAQmx and spinapi are hard dependencies that only NI and SpinCore labs need.
- **Severity**: annoyance
- **Scope**: packaging
- **Related**: #104, #22; PR #110 (Windfreak) adds `windfreak` imported in the worker only.
- **Effort**: small: add `[project.optional-dependencies]` groups per device (`ni`, `pulseblaster`, `zaber`, `pylon`, `visa`, ...), keep the core list minimal, and list non-PyPI SDKs in each device's docs page.
- **Release relevance**: yes. Packaging metadata is release work, and dropping hard dependencies on vendor-specific packages reduces install failures on new Python versions and non-Windows platforms.
- **Rewrite relevance**: requirement (per-driver dependency declaration).
- **Importance**: 3
- **Recommended action**: fix for next release (extras).

### labscript-devices #39: in BLACS, Zaber stage does not obviously handle when device is not homed (philipstarkey for cbillington, opened 2020-01-28, last activity 2020-01-28, 0 comments)
- **Summary**: An unhomed stage reports its maximum position, so BLACS shows a remote-value mismatch rather than saying the stage is not homed.
- **Type**: enhancement
- **Still valid?**: cannot verify (hardware). `ZaberStageController/blacs_workers.py:44-70,79-90` has no homing query or state; the behaviour described is unchanged.
- **Scope**: ZaberStageController
- **Related**: none
- **Effort**: small (query `home` status in `check_remote_values` and raise a clear error or expose a Home button)
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as stale or leave open with "help wanted"; no maintainer has the hardware.

### labscript-devices #38: AndorCamera lacks a docstring (philipstarkey for cbillington, opened 2020-01-28, last activity 2020-01-28, 0 comments)
- **Summary**: AndorSolis should document the `camera_attributes` keys it accepts.
- **Type**: docs
- **Still valid?**: yes. `AndorSolis/labscript_devices.py` is 16 lines, class at line 15 with no docstring; `docs/source/devices/andorsolis.rst` has no attribute list.
- **Scope**: AndorSolis
- **Related**: PR #144 adds attributes (`cooldown`, EM gain mode) and is the natural place to document them.
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: convert to docs; ask the #144 author to include the attribute list.

### labscript-devices #31: imaqdx camera server makes model-specific assumptions (philipstarkey for cbillington, opened 2019-01-17, last activity 2019-04-16, 2 comments)
- **Summary**: The IMAQdx camera server hard-codes attribute names (exposure, width, height, pixel format) that differ between camera models.
- **Type**: bug
- **Still valid?**: fixed by design in `IMAQdxCamera`. In the thread chrisjbillington proposed option (b), "save all attributes as returned by IMAQdxEnumerateAttributes2" and stop referencing model-specific names, and rpanderson agreed (2019-04-16). That is what `IMAQdxCamera` (2019) implements: user-supplied `camera_attributes`, all attributes saved according to `saved_attribute_visibility_level`, and `exposure_time` used only as the trigger width. The hard-coded names remain only in the legacy `labscript_devices/imaqdx_server.py:309-331`, which belongs to the pre-2019 `Camera.py`/BIAS workflow and is not referenced from the docs.
- **Severity**: n.a.
- **Scope**: legacy camera server
- **Related**: #68, PR #148
- **Effort**: trivial
- **Release relevance**: yes, minor: consider deleting `Camera.py`, `camera.ui` and `imaqdx_server.py` in the release, or marking them deprecated in the docs.
- **Rewrite relevance**: moot.
- **Importance**: 1
- **Recommended action**: close as fixed (by IMAQdxCamera).

### labscript-devices #30: Device code should have a version associated with it (philipstarkey, opened 2018-10-30, last activity 2018-10-30, 1 comment)
- **Summary**: Each device class should carry a semver string that labscript saves in connection table properties, so BLACS/runviewer can check shot compatibility.
- **Type**: proposal
- **Still valid?**: n.a. Partially implemented for one device only, as chrisjbillington's comment (2018-10-30) proposed: `NI_DAQmx/labscript_devices.py:14,315` saves `__version__ = '1.2.0'` in `connection_table_properties`, and `NI_DAQmx/blacs_tabs.py:33` and `runviewer_parsers.py:33` read it back and refuse incompatible major versions. The generic `check_version` helper he suggested for `labscript_devices` was never written and no other device does this; labscript itself saves no device-code version.
- **Scope**: labscript, labscript-devices, blacs
- **Related**: #29, #24 (same design thread)
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: requirement. shotscript should record the driver package and version for every device in the shot file and define a compatibility rule between compile-time and run-time drivers.
- **Importance**: 2
- **Recommended action**: leave open as a design record, or merge #24/#29/#30 into one issue.

### labscript-devices #29: Device base classes should save class attributes in device/connection table properties (philipstarkey, opened 2018-10-30, last activity 2018-10-30, 0 comments)
- **Summary**: `clock_resolution`, `wait_delay`, `trigger_delay` and similar should be saved as device properties by the base classes so runviewer and BLACS read them from the shot instead of relying on matching device-class versions.
- **Type**: proposal
- **Still valid?**: n.a. Not implemented in the base classes (`labscript/labscript/core.py:723` `PseudoclockDevice` saves nothing itself). Some devices do it individually, e.g. `PrawnBlaster/labscript_devices.py:160-171` saves `clock_limit`, `clock_resolution`, `trigger_delay`, `wait_delay`, `max_instructions`.
- **Scope**: labscript base classes
- **Related**: #30, #24
- **Effort**: small in labscript (`set_property` calls in `PseudoclockDevice.__init__` / `generate_code`); runviewer parsers would then be updated over time.
- **Release relevance**: no
- **Rewrite relevance**: requirement. Timing parameters used to interpret a shot must be stored in the shot, not recomputed from code at view time.
- **Importance**: 2
- **Recommended action**: leave open (design record); cheap to do the labscript side if touching those classes anyway.

### labscript-devices #24: Backwards compatible connection table comparisons between different versions (philipstarkey, opened 2018-03-12, last activity 2018-03-12, 2 comments)
- **Summary**: Adding a new `connection_table_properties` key to a device should not invalidate existing connection tables; proposes per-device comparison classes and recording suite versions in the connection table.
- **Type**: proposal
- **Still valid?**: n.a. Comparison is still exact equality on the properties dictionary (`labscript_utils/connections.py:129,287-302`).
- **Scope**: labscript-utils connection table, all devices
- **Related**: #30, #29
- **Effort**: large as proposed; a simpler rule (treat missing keys with the class default as equal) is small.
- **Release relevance**: no
- **Rewrite relevance**: requirement. shotscript's connection-table/device-config comparison should be schema-aware with defaults, so adding an optional property does not force a recompile.
- **Importance**: 2
- **Recommended action**: leave open; merge with #29/#30.

### labscript-devices #23: Pulseblaster with 2323 firmware turns off all outputs during programming (philipstarkey for dihm, opened 2017-10-20, last activity 2017-10-20, 0 comments)
- **Summary**: Firmware 2323 drops all outputs on `pb_start_programming()` until `pb_start()`. The worker calls `pb_start_programming()` even when smart programming skips reprogramming; the issue includes a diff that calls it only when programming happens or when the `pb_stop_programming/STOP` scheme needs it.
- **Type**: bug
- **Still valid?**: partially fixed. `PulseBlaster_No_DDS.py` received exactly the proposed change in 4cadcff (2020-07-06): `pb_start_programming` is called inside the smart-cache branch (`:344`) and in the `pb_stop_programming/STOP` else-branch (`:399`). `PulseBlaster.py:1010-1014` (DDS boards) still calls `pb_start_programming(PULSE_PROGRAM)` unconditionally before the smart-cache check.
- **Severity**: annoyance (outputs drop between shots on affected firmware; hardware-specific)
- **Scope**: PulseBlaster DDS-board worker, firmware 2323
- **Related**: none
- **Effort**: small (port the 4cadcff structure to `PulseBlaster.py`); needs a DDS board to test
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: fix later (port to `PulseBlaster.py`), note the partial fix in the issue.

### labscript-devices #22: Third-Party Devices (philipstarkey for dihm, opened 2017-07-17, last activity 2018-10-29, 8 comments)
- **Summary**: Proposes a third-party subfolder or separate repository for contributed, unverified device classes (TekScope, VISA synthesizers).
- **Type**: proposal
- **Still valid?**: n.a. Superseded. The thread (2017-2018) converged on chrisjbillington's proposal: scan a labconfig-set extra directory for `register_classes.py` files, let device users maintain their own device code in-tree, and tag devices with `__version__`; dihm agreed. The first became the `user_devices` mechanism (`labscript_utils/device_registry/_device_registry.py:75-82`, `docs/source/user_devices.rst`), and the devices named (TekScope, VISA instruments) were merged. The remaining open thread is #104.
- **Scope**: repo organisation
- **Related**: #104 (same question, current), #49
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: requirement (see #104).
- **Importance**: 1
- **Recommended action**: close as superseded by `user_devices` and #104.

### labscript-devices #15: BLACS doesn't notice when a PulseBlaster has been unplugged (philipstarkey for shjohnst, opened 2016-01-13, last activity 2016-01-13, 1 comment)
- **Summary**: After unplugging a PulseBlaster, the tab keeps reporting OK; output changes time out after about 40 s with no error.
- **Type**: bug
- **Still valid?**: cannot verify (hardware/spinapi). `PulseBlaster.py:1092-1104` `check_status` returns `pb_read_status()` with no error check; nothing detects disconnection. chrisjbillington's comment (2016-01-13) gives a concrete fix: store `pb_count_boards()` in `init` and raise in `check_status` when the count changes. It was never implemented (`pb_count_boards` is not called anywhere in `labscript_devices`).
- **Severity**: annoyance
- **Scope**: PulseBlaster (all variants), spinapi
- **Related**: none
- **Effort**: trivial (the three-line `pb_count_boards` check in `PulseBlaster.py` and `PulseBlaster_No_DDS.py` workers), needs a board to confirm that spinapi re-enumerates on each call
- **Release relevance**: no
- **Rewrite relevance**: requirement. Device workers should run a periodic health check that distinguishes "idle" from "no device".
- **Importance**: 2
- **Recommended action**: fix later (apply the proposed `pb_count_boards` check when someone with a PulseBlaster can test it); otherwise close as stale.

### labscript-devices #14: NI PCI 6733 must have at least 2 instructions (philipstarkey, opened 2016-01-09, last activity 2016-01-09, 1 comment)
- **Summary**: With fewer than two samples DAQmx raises at programming time; the error should be raised at compile time with a useful message.
- **Type**: bug
- **Still valid?**: obsolete / cannot verify. The 2016 `NI_PCI_6733` class was replaced by the capabilities-driven `NI_DAQmx` package (`NI_PCI_6733.py` is now a shim). Buffered tables always contain the t=0 row and the stop row, so `len(table) >= 2` and the worker writes `len - 1 >= 1` samples (`NI_DAQmx/blacs_workers.py:290-310`). No explicit compile-time sample-count check exists, but the condition that produced the error is no longer reachable from labscript.
- **Severity**: n.a.
- **Scope**: NI_DAQmx
- **Related**: none
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot.
- **Importance**: 1
- **Recommended action**: close as obsolete.

### labscript-devices #13: Pulseblaster DDS cannot be ramped (philipstarkey for shjohnst, opened 2015-09-21, last activity 2015-09-21, 0 comments)
- **Summary**: The PulseBlaster's internal DDS outputs cannot be ramped; enabling ramping on the internal clockline produces wrong timing. Workaround: loop of constant updates.
- **Type**: feature request
- **Still valid?**: n.a. `PulseBlaster.py:229` still creates the direct-output clockline with `ramping_allowed=False`. The DDS frequency/amplitude/phase are register-indexed (`program_freq_regs` etc.) with a small register count, so a general ramp is not representable anyway; the loop-of-constants workaround is what a ramp would compile to.
- **Scope**: PulseBlaster DDS boards
- **Related**: none
- **Effort**: medium, with little payoff over the workaround
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as won't fix, with the workaround noted.

### labscript-devices #8: Pulseblaster Board DDS Problem (philipstarkey for jcevans, opened 2014-12-11, last activity 2014-12-12, 9 comments)
- **Summary**: Opening BLACS gives "DDS Shape capabilities not supported on this board".
- **Type**: question-support
- **Still valid?**: resolved in the thread (2014-12-11/12). The board is an SP17 with no DDS outputs; the `PulseBlaster` class is for the DDS-II board, so SpinCore's library raised the error. chrisjbillington and philipstarkey told the reporter to use or copy `PulseBlaster_SP2_24_100_32k.py` (subclass of `PulseBlaster_No_DDS`), and the reporter agreed the SP2 class fits. Nothing was left to do.
- **Scope**: PulseBlaster
- **Related**: none
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as resolved.

### labscript-devices #6: One folder per device, one file for each program's class (philipstarkey for cbillington, opened 2014-10-04, last activity 2014-10-04, 1 comment)
- **Summary**: Split each device into a package with separate labscript/BLACS/runviewer modules.
- **Type**: proposal
- **Still valid?**: n.a. Implemented: new devices are subpackages with `labscript_devices.py`, `blacs_tabs.py`, `blacs_workers.py`, `runviewer_parsers.py` and `register_classes.py` (e.g. `IMAQdxCamera/`, `PrawnBlaster/`, `NI_DAQmx/`). Older single-file devices remain but the mechanism exists.
- **Scope**: repo organisation
- **Related**: #104
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot.
- **Importance**: 1
- **Recommended action**: close as done.

### labscript-devices #2: RF Blaster minimum frequency is incorrect (philipstarkey, opened 2014-09-30, last activity 2014-09-30, 0 comments)
- **Summary**: The BLACS tab clamps frequencies below 0.5 MHz although the device accepts them via its web interface; the true minimum is unknown.
- **Type**: bug
- **Still valid?**: yes in code: `RFBlaster.py:228` `base_min['freq'] = 500000`. The correct minimum cannot be verified without the device (Monash-built hardware, no longer produced).
- **Severity**: annoyance
- **Scope**: RFBlaster BLACS tab
- **Related**: none
- **Effort**: trivial once the number is known
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as won't fix (hardware obsolete); anyone still using one can change the constant.

---

### PrawnBlaster (firmware)

### PrawnBlaster #31: Allow uneven splitting of instructions between pseudoclocks (philipstarkey, opened 2024-08-13, last activity 2024-08-13, 0 comments)
- **Summary**: Instruction memory is split equally between pseudoclocks; allow an uneven allocation so a slow device's pseudoclock takes few instructions.
- **Type**: feature request
- **Still valid?**: n.a. Master still computes equal shares: `prawnblaster.cpp:591` (`max_instructions / num_pseudoclocks_in_use`) and the address offsets at `:1146,1205,1247`. The host fixes `max_instructions // num_pseudoclocks` at `labscript_devices/PrawnBlaster/labscript_devices.py:232-235`.
- **Scope**: firmware plus host device class
- **Related**: PR #35 implements it (PR-REVIEW.md: missing `ok` reply, offset computed before validation, `setb` off-by-one, no `getnuminstructions`, no host support); #117.
- **Effort**: small firmware rework of #35 plus a small labscript-devices change (per-pseudoclock instruction counts)
- **Release relevance**: no (firmware), unless the host side lands in the labscript-devices release
- **Rewrite relevance**: requirement. shotscript's PrawnBlaster driver should expose per-pseudoclock instruction budgets once firmware 1.3 exists.
- **Importance**: 3
- **Recommended action**: fix later via #35 rework.

### PrawnBlaster #34: 200 MHz system clock (dihm, opened 2025-03-31, last activity 2025-09-08, 7 comments)
- **Summary**: Pico SDK 2.1.1 certifies the RP2040 at 200 MHz with a raised core voltage; proposes firmware support (and external 200 MHz clock input) to double timing resolution.
- **Type**: feature request
- **Still valid?**: n.a. Master firmware rejects above 133/150 MHz unless built with `PRAWNBLASTER_OVERCLOCK` (`prawnblaster.cpp:1038-1051`) and never touches `vreg`. Work exists on `origin/overclock` (PR #36 merged there: `hardware_vreg`, `getvolts`, test notebooks; 2cd59b3 raises the RP2040 bound to 200 MHz) and in PR #37 (voltage tiers by frequency). Host side still caps at 133/150 MHz (`labscript_devices/PrawnBlaster/labscript_devices.py:150,239`) and detects overclock firmware by a `-overclock` version suffix (`blacs_workers.py:137-151`) that #37 removes.
  Discussion (7 comments): philipstarkey suggested building on the RP2350 PR (#30, merged); ErichZimmer reported RP2350 boards running at 300 MHz at 1.2 V with PIO and USB working (400 MHz at 1.3 V did not), and later that above about 286 MHz the QSPI/PSRAM clock divider needs adjusting. On 2025-08-20 dihm set the design: one firmware, no separate overclock build, voltage tiers 1.1 V (<=133/150 MHz), 1.2 V (to 200 MHz), 1.3 V (>200 MHz) with a text warning, frequency boundaries passed as CMake compile definitions; PR #37 is the implementation of exactly that. He also proposed raising the RP2350 boundary to 300 MHz after in-house testing.
- **Scope**: firmware, both boards; host device class
- **Related**: PR #37 (importance 3 in PR-REVIEW.md with four required fixes), prawn_digital_output #20/#17, PrawnBlaster #35 (conflicts in `prawnblaster.cpp`)
- **Effort**: small to finish #37 per PR-REVIEW.md; small host change (`max_frequency_map` behind an explicit opt-in, drop suffix parsing)
- **Release relevance**: yes for the host part if the firmware merges first: `labscript_devices.py:150` and `blacs_workers.py:137-151` need to change together with a firmware version bump.
- **Rewrite relevance**: requirement (device knowledge): per-chip voltage tiers and the ordering rule (raise voltage before frequency, lower frequency before voltage) belong in the shotscript PrawnBlaster driver if it exposes clock frequency.
- **Importance**: 3
- **Recommended action**: fix later: land #37 with the PR-REVIEW.md fixes, then the host change; close this issue when both are in.

---

### prawn_digital_output (firmware, default branch `main`)

### prawn_digital_output #17: Add support for overclocking (philipstarkey, opened 2024-08-11, last activity 2024-08-11, 0 comments)
- **Summary**: Port the PrawnBlaster overclock build: set `overclocks` to `0;1` in CMake, add the firmware files to `build.yaml`, guard the frequency upper-bound check with the compile definition.
- **Type**: feature request
- **Still valid?**: n.a. `prawn_do/CMakeLists.txt:1` is `set(overclocks 0;)`; `PRAWNDO_OVERCLOCK` is defined at `CMakeLists.txt:39` but never referenced in `prawn_do.c`; the `clk` handler hard-rejects above 133/150 MHz (`prawn_do.c:648-656`) with no voltage control.
- **Scope**: firmware
- **Related**: duplicate in substance of #20; PrawnBlaster #34 / PR #37 define the approach (voltage tiers rather than a separate `_overclock` build), so the three-step plan in this issue is superseded.
- **Effort**: small once the PrawnBlaster approach is settled
- **Release relevance**: no
- **Rewrite relevance**: none beyond #34.
- **Importance**: 2
- **Recommended action**: close as duplicate of #20 (or merge the two), and follow the PrawnBlaster #37 design.

### prawn_digital_output #20: Higher system clock support (dihm, opened 2025-07-31, last activity 2025-07-31, 0 comments)
- **Summary**: Support 200 MHz (RP2040) and 300 MHz (RP2350) system clocks, in step with PrawnBlaster #34.
- **Type**: feature request
- **Still valid?**: n.a. See #17: no `vreg` handling, hard limits at `prawn_do.c:648-656`. Host `PrawnDO/labscript_devices.py:122,193` caps at 133/150 MHz.
- **Scope**: firmware and host
- **Related**: #17, PrawnBlaster #34, PR #37
- **Effort**: small (same code as #37, applied to `prawn_do.c`), plus host cap change
- **Release relevance**: no, unless done together with the PrawnBlaster host change
- **Rewrite relevance**: same as PrawnBlaster #34.
- **Importance**: 2
- **Recommended action**: fix later, after PrawnBlaster #37.

### prawn_digital_output #24: Remove `add` functionality (dihm, opened 2025-11-17, last activity 2025-11-17, 0 comments)
- **Summary**: Remove the interactive `add` command (line-by-line programming mode) in favour of `set` and the binary `adm`, to simplify the firmware.
- **Type**: refactor proposal
- **Still valid?**: n.a. `add` is at `prawn_do.c:450-525` (a blocking read loop with its own validation); `edt` (`:676`) is defined in terms of "the last command entered using `add`". The host never uses `add`: `PrawnDO/blacs_workers.py:170` uses `adm`, `:322,328` use `set`. The README documents `add` at lines 71 and 97 and the only programming example (line 119) uses it.
- **Scope**: firmware protocol, README
- **Related**: #25 (README example must change), #26, PR #23 (notebook exercises `set` and `adm`, not `add`)
- **Effort**: small; protocol change, so bump the firmware version (minor)
- **Release relevance**: no
- **Rewrite relevance**: none (shotscript would use `adm`/`set` only).
- **Importance**: 2
- **Recommended action**: fix later, together with #25 and #26 in one firmware release.

### prawn_digital_output #25: General documentation improvements (dihm, opened 2025-11-17, last activity 2025-11-17, 0 comments)
- **Summary**: Checklist: better README examples, testing/validation notebooks, link to the breakout board project, better external-clocking docs (or link to the PrawnBlaster's).
- **Type**: docs
- **Still valid?**: n.a. All four items are open: README example uses `add` (line 119); no "breakout" mention anywhere in the README; external clock section is two lines (`README.md:109-110`); notebooks are PR #23.
- **Scope**: README
- **Related**: PR #23 (addresses the notebook item; PR-REVIEW.md: merge after stripping outputs), #24
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: fix later; merge #23 as the notebook item.

### prawn_digital_output #26: Instruction guardrails (dihm, opened 2025-11-18, last activity 2025-11-18, 0 comments)
- **Summary**: Validate before `run`/`swr` that the program in memory ends with a stop instruction; ensure output words only set the low 16 bits.
- **Type**: feature request (firmware robustness)
- **Still valid?**: n.a., partially done. The 16-bit check already exists: `output_mask` (`prawn_do.c:25`, `(1 << 16) - 1`) is enforced in `set` (`:394`) and `add` (`:494`); `adm` validates reps (`:527-611`) and the mask check should be confirmed there. The stop check does not exist: `run` and `swr` (`:353-361`) push to the second core without inspecting `do_cmds`. Without a trailing stop (two consecutive `reps == 0` words) the PIO program runs past the written instructions into stale memory. The labscript host always writes a stop, so this only affects manual/serial users.
- **Scope**: firmware
- **Related**: #24, #25
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: none (host-side invariant already holds).
- **Importance**: 2
- **Recommended action**: fix later; update the issue to say the 16-bit half is done except possibly in `adm`.

---

### Ranked table

| Rank | Issue | Type | Importance | Action |
|---|---|---|---|---|
| 1 | labscript-devices #109 PrawnBlaster runviewer drops instruction after wait | bug | 4 | fixed in labscript-devices #153 (merged 2026-10-18); issue closed |
| 2 | labscript-devices #131 NumPy 2 `np.string_` | bug | 4 | close as fixed; the `LightCrafterDMD.py` `tostring()` fix merged 2026-10-17 in labscript-devices #149; issue closed |
| 3 | labscript-devices #79 ESRPro500 missing runviewer parser, 21 vs 24 flags | bug | 3 | fixed in labscript-devices #153 (merged 2026-10-18): parser added and all 24 flags exposed; no short-pulse timing feature; issue closed |
| 4 | labscript-devices #49 declare missing dependencies | tooling | 3 | fix for next release (per-device extras) |
| 5 | labscript-devices #104 project structure / per-device deps | meta | 3 | leave open; extras in release |
| 6 | labscript-devices #117 PrawnBlaster triggered from a clockline | feature | 3 | fix later (PrawnDO pattern) |
| 7 | labscript-devices #68 manual-mode-only camera attributes | bug | 3 | fix later, on top of #148 |
| 8 | PrawnBlaster #34 200 MHz clock | feature | 3 | fix later via PR #37 + host change |
| 9 | PrawnBlaster #31 uneven instruction split | feature | 3 | fix later via PR #35 rework |
| 10 | labscript-devices #23 PulseBlaster 2323 outputs drop during programming | bug | 2 | fix later (port 4cadcff to `PulseBlaster.py`) |
| 11 | labscript-devices #91 NI-6738 per-bank AO rate | bug/docs | 2 | convert to docs |
| 12 | labscript-devices #69 TekScope as TriggerableDevice | feature | 2 | fix later (with #129) |
| 13 | labscript-devices #38 AndorSolis docstring | docs | 2 | convert to docs (via #144) |
| 14 | labscript-devices #55 mock flag for more devices | proposal | 2 | leave open |
| 15 | labscript-devices #29 save class attributes as properties | proposal | 2 | leave open (merge with #24/#30) |
| 16 | labscript-devices #30 device code versions | proposal | 2 | leave open (merge) |
| 17 | labscript-devices #24 version-tolerant connection table compare | proposal | 2 | leave open (merge) |
| 18 | labscript-devices #107 PrawnBlaster waits run to timeout | question | 2 | ask reporter, else close stale |
| 19 | labscript-devices #15 unplugged PulseBlaster | bug | 2 | fix later (`pb_count_boards` check from the thread), else close |
| 20 | prawn_digital_output #26 instruction guardrails | feature | 2 | fix later |
| 21 | prawn_digital_output #24 remove `add` | refactor | 2 | fix later |
| 22 | prawn_digital_output #25 docs | docs | 2 | fix later; merge PR #23 |
| 23 | prawn_digital_output #20 higher system clock | feature | 2 | fix later after PR #37 |
| 24 | prawn_digital_output #17 overclock build | feature | 2 | close as duplicate of #20 |
| 25 | labscript-devices #66 TekScope `/data/traces` collision | bug | 1 | close as fixed (259ea85) |
| 26 | labscript-devices #31 imaqdx server model assumptions | bug | 1 | close as fixed (IMAQdxCamera implements the agreed option) |
| 27 | labscript-devices #124 NovaTech TS/pin 10 | question | 1 | close (answered by philipstarkey; docs pointer) |
| 28 | labscript-devices #22 third-party devices | proposal | 1 | close as superseded |
| 29 | labscript-devices #6 one folder per device | proposal | 1 | close as done |
| 30 | labscript-devices #14 NI 6733 needs 2 samples | bug | 1 | close as obsolete |
| 31 | labscript-devices #39 Zaber not homed | enhancement | 1 | close as stale |
| 32 | labscript-devices #13 PulseBlaster DDS ramps | feature | 1 | close as won't fix |
| 33 | labscript-devices #100 PyCapture2 bus failure | question | 1 | close with diagnosis (string serial number) |
| 34 | labscript-devices #8 DDS shape error | question | 1 | close as resolved in thread (2014) |
| 35 | labscript-devices #2 RFBlaster minimum frequency | bug | 1 | close as won't fix |

### Release-relevant issues

- #131: NumPy 2 camera fix is in master but unreleased; the `LightCrafterDMD.py:348,359` `tostring()` calls were fixed by #149 on 2026-10-17. Close when 3.4.0 is released.
- #109: one-line runviewer parser fix, confirmed.
- #79: four-line ESRPro500 runviewer parser, and `n_flags`/`num_DO` 21 to 24 (two users report no output otherwise).
- #49 / #104: declare per-device optional extras; demote PyNIVision/PyDAQmx/spinapi from hard dependencies; add zaber/pypylon extras.
- #31: delete or deprecate the legacy `Camera.py`, `camera.ui`, `imaqdx_server.py`.
- PrawnBlaster #34 (host part): if PR #37 merges, `labscript_devices/PrawnBlaster/labscript_devices.py:150,239` and `blacs_workers.py:137-151` must change in the same labscript-devices release.

### Rewrite requirements collected

- Pseudoclock fan-out: triggering a pseudoclock from any clocked output (#117).
- Device drivers as separate distributions with their own dependencies and a mandatory simulation backend (#104, #49, #55).
- Shot files record driver versions and all timing parameters; config comparison tolerant to added optional properties (#24, #29, #30).
- Capability model able to express channel-combination rate limits (#91).
- Camera attribute sets for manual and buffered modes independent, with save/restore (#68).
- Worker health check that detects a missing device (#15).
- Acquisition instruments as triggerable devices (#69).
- PrawnBlaster: per-pseudoclock instruction budgets (#31) and voltage/frequency ordering for clock changes (#34).

### Revision notes (after reading the full comment threads)

Verdict changes:

- #131: "fixed (commits b40cf0d, 9fde1c0)" -> same, now confirmed in-thread as PR #135; close.
- #79: "parser missing (trivial)" -> parser missing plus a user-verified second defect: `n_flags`/`num_DO` = 21 hides flags 21-23, without which two users' ESR-PRO boards output nothing; fix both for release.
- #100: "support question, close as stale" -> diagnosed by chrisjbillington (string serial number); close with diagnosis, optional error-message improvement.
- #31: "obsolete" -> "fixed by design": the thread agreed on saving all attributes and dropping model-specific names, which IMAQdxCamera implements; close as fixed.
- #15: "close as stale, importance 1" -> "fix later, importance 2": the thread contains a concrete three-line `pb_count_boards` check that was never applied.
- #8: "close as stale" -> "close as resolved": the 2014 thread answered the question (SP17 board has no DDS; use the SP2 class).
- #107: "ask reporter / close" -> "ask dihm": a maintainer reproduced "BLACS waits the full timeout" in 2023 but the description does not say a retrigger was supplied; host and firmware code paths end the shot within one 100 ms poll of the wait completing.

Context added without changing the verdict:

- #124: philipstarkey answered the same day with the archived blog post; docs already cover it.
- #104: 2025-08 update: naqslab implemented the namespace-package approach (`naqs_devices`) and intends to migrate `labscript_devices`; a maintainer decision is outstanding.
- #49: dihm's 2021 docs commit 45a54ed added per-device Installation sections; extras still missing.
- #30: NI_DAQmx already saves and checks `__version__`; the generic helper was never written.
- #22: thread converged on what became `user_devices`; superseded by #104.
- PrawnBlaster #34: dihm fixed the design on 2025-08-20 (single firmware, 1.1/1.2/1.3 V tiers, CMake-defined boundaries), which PR #37 implements; RP2350 reported working at 300 MHz at 1.2 V.
- #14, #24, #55, #6: comments add no new information.

## 3.x Issue triage: blacs (33 open issues) and desktop-app (4 open issues)

Reviewed 2026-10-17 against blacs master `e5757c7` and desktop-app master `f216ef0`.

Source material: the per-issue text files under scratchpad/issues/ (opening post,
all comments, timeline events), cross-checked with scratchpad/issues/blacs.json and
desktop-app.json. The JSON files also list the open PRs (blacs #123, #121, #105, #90,
#89, #88; desktop-app #6); those are covered by PR-REVIEW.md and are not repeated here.
Many blacs issues carry 2023-10-09 "referenced" events from commits in the Loki27182
fork; those are fork-internal references, not fixes, and are ignored below.

File references are relative to the package directory (blacs/blacs/, desktop-app/desktop_app/)
unless a full path is given.

---

### blacs

### blacs #100: BLACS Recompile Error: "None type object has no attribute file no" (Lufter, opened 2023-11-03, last activity 2023-11-03, 0 comments)
- **Summary**: After "compile and restart", the relaunched BLACS dies in `setup_logging` with `AttributeError: 'NoneType' object has no attribute 'fileno'` because `sys.stdout` is `None`. Starting BLACS from its shortcut works.
- **Type**: bug
- **Still valid?**: yes. labscript-utils `labscript_utils/setup_logging.py:57-60` calls `sys.stdout.fileno()` inside a `try` that catches only `io.UnsupportedOperation`; the `sys.stdout is not None` guard at line 68 comes after the call. Any launch where `sys.stdout is None` (pythonw.exe, or a process whose standard handles were closed) crashes at import. The relaunch itself is `subprocess.Popen([sys.executable] + sys.argv)` at `__main__.py:128`. I could not determine from the report which launcher produced a child without stdout (under the desktop-app launcher the child inherits the hidden console), but the crash site exists regardless.
- **Severity**: annoyance (BLACS exits after the restart; the user restarts it by hand; no data loss)
- **Scope**: labscript-utils `setup_logging`, triggered by blacs relaunch; Windows
- **Related**: blacs #5 (also about the relaunch path); zprocess #27 (2026-06-18: the same relaunch, from a ConPTY console, crashes in `zprocess.disable_quick_edit()` with `SetConsoleMode` error 87; also an unguarded call that only fails in the relaunched process). Both show that the `Popen([sys.executable] + sys.argv)` relaunch inherits a console state that differs from a fresh launch.
- **Effort**: trivial (check `sys.stdout is None` before calling `fileno()`, and the same for `sys.stderr` at line 73)
- **Release relevance**: yes, trivial robustness fix in labscript-utils; affects any pythonw launch.
- **Rewrite relevance**: moot (shotscript does not relaunch itself via `sys.argv`), but its logging setup must tolerate `sys.stdout is None`.
- **Importance**: 3. Cheap fix, real crash.
- **Recommended action**: fix for next release (in labscript-utils; move the issue there or fix and close).
- **Status 2026-10-18**: fixed in labscript-utils #133 (merged 2026-10-18) with the guard. The desktop-app launcher gives the programs a hidden console, so `sys.stdout` is a stream on the supported launch path; the crash needs a direct pythonw.exe launch.

### blacs #97: Widget sizing on startup (dihm, opened 2023-01-06, last activity 2023-01-06, 0 comments)
- **Summary**: On first start the output widgets in device tabs are laid out at the wrong size until the container is resized. Suspected cause: `ToolPalette._layout_widgets()` (labscript-utils) runs before the widget has its final width.
- **Type**: bug
- **Still valid?**: cannot verify (needs a running GUI). `labscript_utils/qtwidgets/toolpalette.py` has not changed functionally since 2023 (only enum-qualification commits `ca2a3a7`, `d631ab9`), so the behaviour is unchanged. `_layout_widgets` (toolpalette.py:292) relies on `resizeEvent`; nothing re-lays-out after the main window is first shown (`__main__.py:476`).
- **Severity**: cosmetic
- **Scope**: labscript-utils ToolPalette, used by blacs device tabs; all platforms
- **Related**: none
- **Effort**: small to medium (needs a Qt layout investigation; likely a deferred `_layout_widgets` call after show)
- **Release relevance**: yes as a test item: Qt6 layout timing differs from Qt5, so this must be re-checked under PySide6/PyQt6 before release.
- **Rewrite relevance**: none (the rewrite's GUI is a different design).
- **Importance**: 2. Cosmetic, but visible on every start.
- **Recommended action**: fix later; re-test on Qt6 during the release.

### blacs #92: Slow transition to manual [actually: to buffered] (MMittenbuehler, opened 2022-02-09, last activity 2022-02-09, 0 comments)
- **Summary**: Measurements at TU Darmstadt show transition_to_buffered takes about 150 ms with five devices, dominated by serialisation through the Qt main thread (StateQueue, tab mainloop) rather than by device programming. Asks for direction on a per-device thread architecture.
- **Type**: question-support / feature request (performance)
- **Still valid?**: yes. Every state-queue operation is an `inmain` call (`tab_base_classes.py:101`, `:121`, `:188-189`), each state function runs in the main thread (`:786`) and every generator step round-trips through the main thread (`:792`, `:840`). The queue manager also serialises on the main thread (`experiment_queue.py:492-499`). No change since the report.
- **Severity**: n.a. (performance)
- **Scope**: blacs core state machine; all platforms
- **Related**: #53, #15 (cycle-time), #49, #40 (state machine)
- **Effort**: large (architecture change)
- **Release relevance**: no
- **Rewrite relevance**: requirement: device transitions must run concurrently and not be serialised through a GUI thread; the GUI must be a view of device state, not the arbiter.
- **Importance**: 2 for legacy (not fixable without a redesign); the data in the report is useful.
- **Recommended action**: leave open as the performance reference for the rewrite; reply that the fix is architectural and out of scope for legacy blacs.

### blacs #72: Set lyse host to localhost and enable analysis by default (rpanderson, opened 2020-06-09, last activity 2020-06-09, 1 comment)
- **Summary**: Default the analysis submission server to `localhost` and enable "send to lyse" on a fresh install, as runmanager assumes localhost for BLACS.
- **Type**: feature request
- **Still valid?**: yes. `analysis_submission.py:52-53` initialises `send_to_server = False`, `server = ''`.
- **Scope**: blacs analysis submission
- **Related**: none
- **Effort**: trivial
- **Release relevance**: no (behaviour change, but harmless: a connectivity check against localhost fails quietly if lyse is not running)
- **Rewrite relevance**: requirement: works-out-of-the-box defaults, localhost everywhere.
- **Importance**: 3. Trivial and improves first-run experience.
- **Recommended action**: fix for next release. The maintainer agreed in 2020 ("super trivial", would do it the next day) and it was never done.

### blacs #58: Experiment final values not handled for devices with custom UIs (philipstarkey, opened 2020-04-06, last activity 2020-04-06, 0 comments)
- **Summary**: `DeviceTab.transition_to_manual` applies the shot's final values only to the built-in AO/DO/DDS/Image/EO output objects; a tab with a custom UI has no hook to receive `self._final_values`.
- **Type**: feature request (API gap)
- **Still valid?**: yes. `device_base_class.py:713-724` loops over the five output dicts only; no overridable method.
- **Scope**: blacs DeviceTab API
- **Related**: none
- **Effort**: small (add e.g. `update_final_values(final_values)` called at `device_base_class.py:725`; default no-op)
- **Release relevance**: no
- **Rewrite relevance**: requirement: the device/GUI contract must let any widget type receive end-of-shot values.
- **Importance**: 2. Real gap, affects only custom-UI devices.
- **Recommended action**: fix later.

### blacs #57: Qt stylesheet not applied on launch (philipstarkey, opened 2020-04-05, last activity 2020-04-05, 0 comments)
- **Summary**: Mailing-list report that with PyQt 5.13.0 the theme stylesheet is not applied at launch until a tab restart; worked on 5.14.
- **Type**: bug
- **Still valid?**: cannot verify (needs GUI). A workaround exists: `plugins/theme/__init__.py:133-139` calls `centralwidget.show()` before `setStyleSheet` (commit `f9e7471`, 2017-08-04, "PyQt5 stylesheet workaround"), so the 2020 report was with that workaround present. The report is specific to PyQt 5.13.0; current targets are PySide6/PyQt6 (commit `68bb2cf` reworked theme updates for Qt6 and `BLACSWindow.changeEvent` at `__main__.py:147-165` re-applies stylesheets on palette change).
- **Severity**: cosmetic
- **Scope**: blacs theme plugin; Qt-version specific
- **Related**: #97 (startup rendering), runviewer #26 (pyqtgraph/PyQt 5.14 incompatibility mentioned in the body)
- **Effort**: trivial to verify
- **Release relevance**: yes as a test item: confirm the default stylesheet applies at launch under PySide6 and PyQt6.
- **Rewrite relevance**: none
- **Importance**: 1. PyQt 5.13-specific; likely obsolete.
- **Recommended action**: close as obsolete after a launch check on Qt6.

### blacs #56: Improve restoration of windows geometry on launch (philipstarkey, opened 2020-04-05, last activity 2020-04-05, 0 comments)
- **Summary**: Restoring the saved window position can place the window off-screen; proposes `QWidget.saveGeometry()/restoreGeometry()`.
- **Type**: bug / feature request
- **Still valid?**: yes. `__main__.py:481-515` still restores with `move()`/`resize()` and frame-size arithmetic; `front_panel_settings.py:239-245` saves `normalGeometry` and frame deltas. No screen-bounds check, no `restoreGeometry`.
- **Severity**: wrong-behaviour (window unreachable; workaround is deleting the saved h5 or OS move commands)
- **Scope**: blacs main window; mostly Windows multi-monitor
- **Related**: #52 (same root cause)
- **Effort**: small (store `saveGeometry()` bytes in the settings h5, call `restoreGeometry()`, and clamp to `QScreen.availableGeometry()` if the result is off-screen)
- **Release relevance**: yes: Qt6 changed screen-geometry APIs (`QDesktopWidget` removed); whatever fix is made should use `QScreen`. Also affects Windows 11 multi-monitor users.
- **Rewrite relevance**: requirement: window placement must be validated against current screens on restore.
- **Importance**: 3
- **Recommended action**: fix for next release together with #52.

### blacs #55: Implement abort during delay when using cycle_time plugin (philipstarkey, opened 2020-01-28 [migrated], last activity 2021-01-13, 1 comment)
- **Summary**: Clicking abort while the cycle_time plugin waits for the target cycle time is not acted on until after transition_to_buffered.
- **Type**: bug
- **Still valid?**: fixed. The wait is interruptible: `plugins/cycle_time/__init__.py:197-214` connects the abort button to `self._abort` and breaks out of the wait (present since the plugin was `fixed_shot_interval`, commit `3fa878b` 2018-09-10; renamed in `5fe56f3` 2019-06-28). zakv confirmed on 2021-01-13 that aborting during the delay works. One ordering detail remains: the queue manager reads the abort only after it has started transition_to_buffered for the first start group (`experiment_queue.py:625-632` before `:643-650`) or, with `delay_after_programming`, after `start_run` (`:742-749` before `:761-765`), so the devices are programmed (or the shot started) and then aborted.
- **Severity**: cosmetic (the shot is aborted either way; some wasted programming)
- **Scope**: blacs queue manager / cycle_time plugin
- **Related**: #53
- **Effort**: trivial if the ordering is to be tightened (drain `self.current_queue` for an abort after the plugin callbacks at `experiment_queue.py:595-599` and `:742-746`)
- **Release relevance**: no
- **Rewrite relevance**: requirement: an abort must be honoured at every wait point in the shot cycle.
- **Importance**: 1
- **Recommended action**: close as fixed (reporter-confirmed 2021); optionally open a small follow-up for the ordering.

### blacs #54: Be able to check remote versions (of BLACS and other components) (philipstarkey, opened 2020-01-28 [migrated], last activity 2020-01-28, 0 comments)
- **Summary**: Remote workers (zprocess remote process server) may run a different BLACS/labscript-utils version; add a `check_version` worker method called at worker startup, with a clear "error occurred on the remote computer" message.
- **Type**: feature request (robustness)
- **Still valid?**: yes. No `check_version` anywhere in blacs (`grep -rn check_version blacs/` is empty). `Worker.run` (`tab_base_classes.py:872-894`) does no version handshake.
- **Scope**: blacs worker startup; remote-worker setups only
- **Related**: zprocess #14 (PAIR sockets; PR-REVIEW says it needs exactly this kind of version check for mixed zprocess versions), labscript #28, blacs #13
- **Effort**: small (send `labscript_utils.__version__`/`blacs.__version__` in the `init` call, compare in the worker, raise a wrapped error)
- **Release relevance**: yes if a wire-format change is merged without negotiation; otherwise no. zprocess #33 (2026-10-19) negotiates the PAIR socket change, so it does not need this.
- **Rewrite relevance**: requirement: protocol/version negotiation between controller and remote device workers.
- **Importance**: 3
- **Recommended action**: fix later; fix for next release only if zprocess #14 goes in. 2026-10-19: zprocess #33 does the PAIR change with negotiation, so this is not required by it.

### blacs #53: Ways of speeding up cycle time. Pipelining, readahead, removing redundant steps (philipstarkey, opened 2019-12-08 [migrated], last activity 2019-12-09, 6 comments)
- **Summary**: Design notes: split transition_to_buffered/manual into independent steps (read instructions, program, read data, save data, reconfigure), run independent steps concurrently, skip redundant ones, optionally read the shot file ahead of time. Profile first.
- **Type**: feature request (design)
- **Still valid?**: n.a. Nothing implemented; the queue manager still runs the phases strictly in sequence (`experiment_queue.py:578-947`).
- **Scope**: blacs core
- **Related**: #92 (measurements), #15
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement: this is the shot-cycle design brief for shotscript (pipelined phases, per-device concurrency, skip reprogramming for repeated shots). The 2019 comments add two points: multi-worker devices (NI cards) should have their workers programmed in parallel (yield a dict of jobs, wait with poll), and h5py releases the GIL during I/O since 3.0, so threads suffice for concurrent HDF5 writes.
- **Importance**: 2 for legacy; high value as a design record.
- **Recommended action**: leave open as a design record for the rewrite; mark won't-fix in legacy.

### blacs #52: Lost BLACS window after compile and restart (philipstarkey, opened 2019-06-04 [migrated], last activity 2026-01-22, 2 comments)
- **Summary**: On Windows 10 multi-monitor setups the window is off-screen/invisible after compile-and-restart; the taskbar entry exists but clicking does nothing.
- **Type**: bug
- **Still valid?**: yes, same cause as #56: `__main__.py:495-509` restores position with frame-size arithmetic from `front_panel_settings.py:239-245`, with no check that the result lies on a current screen. Confirmed recurring: Json-To-String hit it on 2026-01-22; the Win+arrow workaround (dihm, 2019) did not work and deleting `app_saved_configs/<apparatus>/blacs/` was needed.
- **Severity**: wrong-behaviour (window unusable until the settings file is deleted)
- **Scope**: Windows, multi-monitor
- **Related**: #56 (duplicate root cause), #5, #100 (other compile-and-restart issues)
- **Effort**: small (same fix as #56)
- **Release relevance**: yes (Windows 11 users, Qt6 screen APIs).
- **Rewrite relevance**: requirement (see #56).
- **Importance**: 4. Labelled major, recurring, cheap to fix.
- **Recommended action**: fix for next release (one fix closes #52 and #56).

### blacs #50: Add information on loaded plugins (philipstarkey, opened 2018-10-26 [migrated], last activity 2018-10-26, 2 comments)
- **Summary**: A misnamed plugin entry in labconfig was silently ignored; BLACS should report which plugins loaded and which failed.
- **Type**: feature request
- **Still valid?**: yes. `plugins/__init__.py:86-100` logs import failures with `logger.exception` only; a labconfig key that matches no plugin directory is never reported; `__main__.py:315-320` logs instantiation failures only. No GUI indication.
- **Scope**: blacs plugin loader
- **Related**: PR blacs #123 (fixes two other plugin-loading bugs in the same code; PR-REVIEW rank 1), #41, PR #121. Both maintainers agreed in 2018 to promote plugin load failures to a GUI notification (tracebacks already go to the log).
- **Effort**: small (log at INFO the list of loaded/disabled/unknown plugins; a notification for failures)
- **Release relevance**: no
- **Rewrite relevance**: requirement: plugin/extension loading must report failures visibly.
- **Importance**: 2
- **Recommended action**: fix later, after merging #123.

### blacs #49: The BLACS tab statemachine can crash if you return before yielding in a generator (philipstarkey, opened 2018-09-27 [migrated], last activity 2018-09-27, 0 comments)
- **Summary**: A `@define_state` method containing a `yield` is a generator even when it `return`s before reaching the `yield`; the first `__next__` then raises `StopIteration` outside the handler and the tab enters "fatal error".
- **Type**: bug
- **Still valid?**: yes. `tab_base_classes.py:792` calls `inmain(generator.__next__)` outside the `try/except StopIteration` that begins at `:795`; the `StopIteration` propagates to `except Exception` at `:853` and the tab is put in fatal error. (Also latent at `:840-843`: a generator that yields `None` re-sends the previous worker job.)
- **Severity**: wrong-behaviour (tab fatal error for valid device code)
- **Scope**: blacs state machine; affects device authors
- **Related**: #40
- **Effort**: trivial (move line 792 inside the try, or wrap in `try/except StopIteration`)
- **Release relevance**: no, but trivial and safe.
- **Rewrite relevance**: moot (no generator-based state machine).
- **Importance**: 3
- **Recommended action**: fix for next release.

### blacs #46: Blacs stuck in queue error (Anonymous via philipstarkey, opened 2018-07-12 [migrated], last activity 2018-07-12, 1 comment)
- **Summary**: When the file server is full and BLACS cannot save shot data, an error is shown and BLACS stays in an error state until restarted.
- **Type**: bug
- **Still valid?**: yes. The failure in `h5py.File(path,'r+')` at `experiment_queue.py:855` is caught at `:917`, but the cleanup that follows at `:926-947` is outside any `try`: `h5py.File(path,'r')` at `:930` and the second `shutil.move` at `:942` raise on the same unavailable path, the exception leaves `manage()` and the queue-manager thread exits. The same pattern is inside the first exception handler at `:808-821`. After that no shot can run until BLACS is restarted.
- **Severity**: crash-data-loss (queue thread dies; the shot's h5 may be left half-cleaned)
- **Scope**: blacs queue manager; any I/O failure on the shot path
- **Related**: #29 (same code, same cause). The maintainer's 2018 comment gives the same diagnosis: two places inside the exception-handling code move the file without checking `clean_h5_file()` and are outside any `try`.
- **Effort**: small (wrap the cleanup in `try/except`, log, set status "Shot file inaccessible, queue paused", keep the thread alive; put a top-level `try/except` around the loop body so the thread never dies)
- **Release relevance**: yes: robustness fix with no API impact; long-standing "major" bug.
- **Rewrite relevance**: requirement: the shot runner must survive storage errors and resume.
- **Importance**: 4
- **Recommended action**: fix for next release (together with #29).

### blacs #45: Can't start after a crash if previously queued shots have been deleted (shjohnst via philipstarkey, opened 2018-07-11 [migrated], last activity 2018-07-11, 2 comments)
- **Summary**: After a crash, BLACS restores a stale queue on startup; if those files were deleted, startup fails. Asks for a try/except around the restore.
- **Type**: bug
- **Still valid?**: cannot verify; never reproduced. `QueueManager.restore_save_data` (`experiment_queue.py:190-195`) calls `process_request`, which wraps `ConnectionTable(h5_filepath)` in `try/except` and returns a message (`:383-386`), so a missing file is skipped; that code dates from 2013 (`ade72e1`). The maintainer said the same in 2018 and asked for a traceback; the reporter had worked around it by moving a shot file into place (after which BLACS loaded, with dismissable popups for the other missing shots) and never followed up. The only unprotected call on that path is `h5py.File` at `:390` for a file that exists but is unreadable. The maintainer's proposed real fix was to save the queue state after every shot so a crash does not restore a stale queue.
- **Severity**: wrong-behaviour (startup failure, unconfirmed)
- **Scope**: blacs startup
- **Related**: #46, #29
- **Effort**: trivial (wrap `:390-394` in the same try); small for periodic queue-state saving
- **Release relevance**: no
- **Rewrite relevance**: requirement: restoring persisted state must tolerate missing files; persist queue state continuously.
- **Importance**: 1
- **Recommended action**: close as stale (no traceback in seven years; the code path handles missing files), after guarding `:390`.

### blacs #41: Plugin Base-Classes (PhyNerd via philipstarkey, opened 2018-04-25 [migrated], last activity 2018-04-25, 0 comments)
- **Summary**: Provide base classes for Plugin, Notification and Settings so the plugin API can grow without breaking plugins and so required methods are documented.
- **Type**: feature request
- **Still valid?**: yes. Plugins are duck-typed; `__main__.py:323-342`, `:403-429`, `:443-453` use `hasattr` checks and a fallback to an old `plugin_setup_complete()` signature.
- **Scope**: blacs plugin API
- **Related**: PR blacs #121 (shared plugin refactor; PR-REVIEW recommends closing), #50, #27
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: requirement: a typed plugin/extension interface with defaults.
- **Importance**: 2
- **Recommended action**: fix later.

### blacs #40: Better defaults and better error reporting for incorrect use of state machine (chrisjbillington via philipstarkey, opened 2018-04-25 [migrated], last activity 2018-04-26, 1 comment)
- **Summary**: `create_worker` should set `primary_worker` automatically for the first worker, `queue_work` should default to the primary worker, and `mainloop` should give informative errors instead of a KeyError traceback when `primary_worker` is `None`.
- **Type**: feature request (API ergonomics)
- **Still valid?**: yes. `device_base_class.py:57` initialises `_primary_worker = None` and nothing sets it in `create_worker` (`tab_base_classes.py:486-534`); `queue_work` (`:722-723`) requires the worker name; `mainloop` does `workers[worker_process]` at `:813` with no check, so a `None` worker surfaces as `KeyError: None` in a fatal-error tab.
- **Scope**: blacs device API
- **Related**: #49
- **Effort**: small. The 2018 comment settles the design: override `create_worker` in `DeviceTab` to set `primary_worker` for the first worker (keep the concept in `DeviceTab`, do not change `queue_work`), and type-check the yielded tuple in the mainloop.
- **Release relevance**: no
- **Rewrite relevance**: moot (different device API).
- **Importance**: 2
- **Recommended action**: fix later.

### blacs #33: BLACS should respect output limits as defined in the connection table (philipstarkey, opened 2018-01-23 [migrated], last activity 2018-01-23, 0 comments)
- **Summary**: Once labscript stores per-output `limits` in the connection table (labscript #44), BLACS should use them in `_create_AO_object` when they are inside the hardware limits.
- **Type**: feature request (blocked)
- **Still valid?**: yes, blocked. labscript `Output.__init__` accepts `limits` (`labscript/outputs.py:41`, `:119`) but they are not written to the connection table (`labscript_utils/connections.py` has no `limits` field); labscript #44 is still open. `device_base_class.py:208-223` uses only the device class's `min`/`max`.
- **Scope**: blacs AO widgets; depends on labscript and labscript-utils
- **Related**: labscript #44 (prerequisite)
- **Effort**: small once #44 is done
- **Release relevance**: no
- **Rewrite relevance**: requirement: output limits are a property of the connection table and enforced by the GUI.
- **Importance**: 2
- **Recommended action**: leave open, blocked on labscript #44.

### blacs #32: Report which device(s) have caused the queue to pause (rpanderson via philipstarkey, opened 2017-12-15 [migrated], last activity 2017-12-15, 1 comment)
- **Summary**: The status label says "Device(s) in error state, Queue Paused" but not which device; the name is only in the log.
- **Type**: feature request
- **Still valid?**: yes. `experiment_queue.py:701` sets the generic message; names are known at `:630`, `:665`, `:673-676` (the timeout path does not record the name at all), `:891-905`.
- **Scope**: blacs queue manager
- **Related**: none
- **Effort**: trivial (collect the names into a list and include them in `set_status`)
- **Release relevance**: no
- **Rewrite relevance**: requirement: error states name the device.
- **Importance**: 3. Trivial, large usability gain.
- **Recommended action**: fix for next release.

### blacs #31: Graceful Worker Process exit on restart (PhyNerd via philipstarkey, opened 2017-11-17 [migrated], last activity 2017-11-18, 2 comments)
- **Summary**: Restarting a tab terminates its worker immediately, leaving hardware/locks in a bad state; call the worker's `shutdown()` first.
- **Type**: feature request
- **Still valid?**: partially. On BLACS exit, `on_save_exit` calls `tab.shutdown_workers()` (`__main__.py:651-656`, `tab_base_classes.py:590-595`) with a 2 s grace period (`__main__.py:662`). On tab restart, `Tab.restart` (`tab_base_classes.py:672-683`) goes straight to `close_tab`/`finalise_close_tab`, which calls `worker.terminate()` (`:651`) without a `shutdown` request. Restart is usually used when the worker is unresponsive, so a blocking `shutdown` call there would need a timeout.
- **Scope**: blacs tab restart
- **Related**: the 2017 comments moved the signal-handling part to zprocess (PhyNerd said he would open a zprocess issue; zprocess #6 "Expose process communication ports" is his only zprocess issue from that time and is not about termination, so no zprocess issue tracks this)
- **Effort**: small (queue `shutdown` with a timeout before terminate; must not block the GUI)
- **Release relevance**: no
- **Rewrite relevance**: requirement: device teardown hook with a bounded timeout, both on exit and on restart.
- **Importance**: 2
- **Recommended action**: fix later.

### blacs #29: crash on shared drive becoming unavailable (PhyNerd via philipstarkey, opened 2017-09-22 [migrated], last activity 2017-09-22, 1 comment)
- **Summary**: If the shared drive disappears, uncaught exceptions in the queue manager's error-cleanup code stop BLACS from doing anything until restart.
- **Type**: bug
- **Still valid?**: yes. The two code regions the report cites (old queue.py 730-736 and 825-831) are now `experiment_queue.py:808-821` (inside an `except` block) and `:930-943` (outside any `try`). Both open or move the shot file without protection; an `OSError` there ends the `manage()` thread.
- **Severity**: crash-data-loss (queue thread dies)
- **Scope**: blacs queue manager; network storage setups
- **Related**: #46 (same cause), #45. The 2017 maintainer comment framed this as suite-wide (a retrying file/zlock access wrapper with a "retry now" dialog); that wrapper was never written. The blacs-local fix is still worth doing on its own.
- **Effort**: small (see #46)
- **Release relevance**: yes (see #46).
- **Rewrite relevance**: requirement (see #46).
- **Importance**: 4
- **Recommended action**: fix for next release; close as duplicate of #46 once fixed (or the reverse).

### blacs #27: Plugin Tabs (PhyNerd via philipstarkey, opened 2017-08-21 [migrated], last activity 2017-08-22, 5 comments)
- **Summary**: Let plugins create their own tabs; asks whether one tab per plugin suffices and whether a worker should be required.
- **Type**: feature request
- **Still valid?**: fixed. The design agreed in the comments (plugin returns a dict of tab classes, instantiated by BLACS with a notebook and settings, no worker required) is what was implemented: `PluginTab` (`tab_base_classes.py:951-1040`) and `__main__.py:321-342` instantiating `plugin.get_tab_classes()`. Commit `5ba525f` (2017-08-22, "Tabs-for-Plugins: Added ability for plugins to spawn tabs"); used by the `connection_table` plugin and PR #105.
- **Scope**: blacs plugin API
- **Related**: PR #105 (Virtual Devices plugin uses PluginTab)
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: requirement: extensions can contribute GUI panels.
- **Importance**: 1
- **Recommended action**: close as fixed.

### blacs #24: Remote control (PhyNerd via philipstarkey, opened 2017-08-05 [migrated], last activity 2017-08-08, 6 comments)
- **Summary**: Extend the BLACS zmq server so other programs can pause the queue (watchdogs), clear queued shots from runmanager's abort, etc. Asks whether a PR is wanted.
- **Type**: feature request
- **Still valid?**: yes. `ExperimentServer.handler` (`__main__.py:533-546`) accepts only an h5 filepath and calls `queue.process_request`; no pause/abort/clear/status commands.
- **Scope**: blacs network API
- **Related**: #13, runmanager compilation-queue work (PR runmanager #104 / blacs #90). The 2017 comments suggested doing it as a plugin (the Monash `labwatch` plugin pauses the queue from a notification class) and raised network security; zprocess preshared-key authentication was added afterwards and is in `labscript_utils.ls_zprocess`.
- **Effort**: small to medium (a dict-based request protocol with pause/resume/abort/clear/status; keep the bare-string path for compatibility)
- **Release relevance**: no
- **Rewrite relevance**: requirement: the shot runner exposes a programmatic control API (pause, abort, clear, status, submit).
- **Importance**: 2 for legacy.
- **Recommended action**: leave open; implement in the rewrite.

### blacs #23: Analoge Inputs (PhyNerd via philipstarkey, opened 2017-07-09 [migrated], last activity 2017-08-28, 7 comments)
- **Summary**: Display analog input values in device tabs (read-only, polled in manual mode) for troubleshooting.
- **Type**: feature request
- **Still valid?**: yes. `output_classes.py` has AO, DO, DDS, Image, EO only; no input display class; `DeviceTab` has no input hooks.
- **Scope**: blacs DeviceTab / output_classes, plus per-device worker support
- **Related**: #116 (real-time input display), labscript-devices NI acquisition workers. The 2017 comments agreed a design: workers publish on ZMQ PUB sockets, a forwarder/broker in its own BLACS process re-publishes on a port set in labconfig, tabs and external programs subscribe. PhyNerd said a PR was imminent (2017-08-28); none exists.
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: requirement: device panels can show acquired/monitored values in manual mode; a PUB/SUB data bus for live device data.
- **Importance**: 2.
- **Recommended action**: leave open; implement in the rewrite.

### blacs #19: Documentation is out of date (shjohnst via philipstarkey, opened 2017-06-16 [migrated], last activity 2017-06-16, 2 comments)
- **Summary**: The 2014 docs predate labscript_devices and show GTK screenshots; suggests moving device-adding docs to labscript_devices and refreshing "Using BLACS".
- **Type**: docs
- **Still valid?**: partially addressed. The 2017 comments asked for Sphinx on Read the Docs; that exists (`docs/source/*.rst`, 543 lines: usage, device-tabs, plugins, shot-management). The stale artefacts the report complains about are still in the repo: `docs/UsingBLACS.pdf`, `docs/UsingBLACS.docx`, `docs/How to add a new device/main.tex|main.pdf`.
- **Scope**: blacs docs
- **Related**: labscript-suite docs issues (not in my set)
- **Effort**: trivial to delete the stale files; small to review the rst text and screenshots for Qt6
- **Release relevance**: yes, minor: remove the stale PDFs/LaTeX from the repo and check screenshots before tagging.
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: convert to docs task (delete stale files; close when done).

### blacs #15: Improve shot cycle time in BLACS (philipstarkey, opened 2017-06-07 [migrated], last activity 2017-06-08, 3 comments)
- **Summary**: During the run loop the per-device error-state check does one `inmain` round trip per device; proposes a single `get_many_device_error_states`.
- **Type**: feature request (performance)
- **Still valid?**: mostly obsolete. The per-device loop still exists (`experiment_queue.py:769-771`) but, as in the 2017 code it cites, it executes only when a message arrives on `current_queue` (it is inside the `try` after `get_nowait()` at `:763`), not on every 0.5 s iteration, so it is not a per-iteration cost. The transition phases check error states only after a 2 s timeout (`:673-676`, `:890-894`). `get_many_device_error_states` was never added. Note that the placement at `:769-771` also means a device error during a run is only detected when some other message arrives; that is a separate latent bug.
- **Scope**: blacs queue manager
- **Related**: #92, #53. chrisjbillington's 2017 comment was already sceptical (50x the check made no measurable difference) and asked for profiling first; #92 later supplied measurements pointing at the state machine, not this loop.
- **Effort**: trivial
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as stale/won't fix; superseded by #92/#53.

### blacs #13: Launch BLACS as a secondary control system (philipstarkey, opened 2017-04-21 [migrated], last activity 2017-10-03, 8 comments)
- **Summary**: Run secondary BLACS instances on other PCs, declared in the connection table (`SecondaryControlSystem`), with the primary queue manager coordinating transitions.
- **Type**: feature request
- **Still valid?**: partially implemented. labscript has `RemoteBLACS` and `SecondaryControlSystem` (`labscript/remote.py:38-45`) and devices accept `worker=`/`gui=`. BLACS supports remote *workers* via `RemoteProcessClient` (`tab_base_classes.py:320-338`) but raises `NotImplementedError("Remote BLACS GUIs not yet supported by BLACS")` for the `gui` property (`:326-328`) and for multi-hop (`:332-334`).
- **Scope**: blacs architecture; multi-PC labs
- **Related**: #54 (version check for remote workers), #24, labscript #28. The 2017 comment thread converged on a `RemoteBLACSConnection` base with `RemoteWorkerBroker` (no tab) and `SecondaryControlSystem` (with a tab) subclasses, addresses in the connection table, and an eight-step TODO (2017-10-03) that also required moving the queue and analysis submission into plugins. The worker-broker half shipped as `RemoteBLACS`; none of the secondary-GUI steps were done.
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement: distributed device workers and, optionally, distributed GUI panels, declared in the connection table.
- **Importance**: 2.
- **Recommended action**: leave open; note that remote workers are done and secondary GUIs are not.

### blacs #116: Blacs real time display of input data (ispielma via philipstarkey, opened 2017-04-21 [moved from labscript 2026-01-26], last activity 2026-01-26, 0 comments)
- **Summary**: Stream camera/input data live to a BLACS tab (e.g. to watch a MOT) instead of using security cameras.
- **Type**: feature request
- **Still valid?**: yes; nothing in blacs core. (IMAQdxCamera's tab in labscript-devices has an acquisition preview, which partly covers the camera case.)
- **Scope**: blacs DeviceTab; camera devices
- **Related**: #23, labscript-devices PR #148 (TriggerableCamera)
- **Effort**: large in general; the camera case exists per device
- **Release relevance**: no
- **Rewrite relevance**: requirement (same as #23).
- **Importance**: 2
- **Recommended action**: leave open; point to IMAQdxCamera's live view for cameras.

### blacs #115: Better arrangement of tabs in blacs (ispielma via philipstarkey, opened 2017-04-21 [moved from labscript 2026-01-26], last activity 2026-01-26, 1 comment)
- **Summary**: Labs with many tabs find them hard to manage; asks for a better organising principle.
- **Type**: feature request (vague)
- **Still valid?**: n.a. BLACS has four drag-and-drop notebooks (`__main__.py:283-287`) with saved placement; no grouping, search or collapse.
- **Scope**: blacs main window
- **Related**: #27; PR blacs #105 (Virtual Devices plugin) implements the "virtual device tab" item from the maintainer's 2017 list of ideas (pop-out tabs, tighter padding, configurable notebook grid, tabs on secondary PCs, virtual devices).
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: requirement: device panel organisation (grouping by connection-table hierarchy, search) for large apparatuses.
- **Importance**: 1
- **Recommended action**: leave open as a rewrite requirement or close as too vague.

### blacs #12: Error not handled well during connection table recompile (shjohnst via philipstarkey, opened 2015-09-21 [migrated], last activity 2019-07-04, 5 comments)
- **Summary**: When the batch compiler child process died at import (zlock timeout), the compile-and-restart dialog stayed on "Recompiling connection table" with all buttons disabled and could not be closed.
- **Type**: bug
- **Still valid?**: yes. `compile_and_restart.py:65-68` disables compile/cancel/restart and `closeEvent` (`:53-57`) refuses to close while cancel is disabled; the buttons are re-enabled only in `finished_compiling`. runmanager's `compile_labscript_async` (origin/master `runmanager/compiler.py:255-266`) blocks on `from_child.get()` with no timeout and no check that the child is alive, so if the child dies before sending `done` the callback never fires. zprocess heartbeats only terminate children whose parent has gone, not the reverse.
- **Severity**: annoyance (the dialog is non-modal; the main window keeps working; the workaround noted in 2019 is to open a second compile-and-restart dialog)
- **Scope**: blacs compile_and_restart + runmanager compiler
- **Related**: runmanager #35 (open, 2015: "Asynchronous compilation functions should handle exceptions gracefully"), which the 2015 comments identify as the real bug and this issue's blocker; reconfirmed by shjohnst and chrisjbillington in 2019-07 (import-time failure of matplotlib in the compiler child).
- **Effort**: small (in runmanager: poll `child.poll()` with a timeout in the `from_child.get()` loop and call `done_callback(False)`; in blacs: always allow Cancel/close)
- **Release relevance**: no
- **Rewrite relevance**: requirement: compilation subprocess failures must propagate as failures, with timeouts.
- **Importance**: 3
- **Recommended action**: fix runmanager #35 (the runmanager refactor is in progress) and close this with it; in blacs, make the dialog closable regardless.

### blacs #7: Default file open paths (chrisjbillington via philipstarkey, opened 2014-10-03 [migrated], last activity 2014-10-03, 1 comment)
- **Summary**: File dialogs for globals files (connection-table import) and unit-conversion files should open in sensible directories.
- **Type**: feature request
- **Still valid?**: yes. `plugins/connection_table/__init__.py:392`, `:429`, `:452` hard-code `"C:\\"` as the starting directory (meaningless on Linux/macOS). The main-window dialogs already use `experiment_shot_storage` (`__main__.py:569`, `:713`) and the queue remembers `last_opened_shots_folder` (`experiment_queue.py:263-276`).
- **Scope**: blacs connection_table plugin
- **Related**: none
- **Effort**: trivial (use labconfig `paths` entries: `experiment_shot_storage`/`userlib`; remember the last directory)
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 3. Trivial and the current value is wrong on non-Windows.
- **Recommended action**: fix for next release.

### blacs #5: AppID stuff not set correctly after compile and restart (chrisjbillington via philipstarkey, opened 2014-10-02 [migrated], last activity 2017-06-14, 4 comments)
- **Summary**: After compile-and-restart BLACS is grouped with runmanager in the Windows 7 taskbar.
- **Type**: bug
- **Still valid?**: fixed, pending a Windows check. `__main__.py:20-21` calls `desktop_app.set_process_appid('blacs')` at import in every BLACS process, including the relaunched one (commit `b296deb`, 2020-05-10, "Use desktop-app package for desktop integration"). The 2017 comments (grouping with lyse on Windows 10; suggestion of `DETACHED_PROCESS` or a zprocess "restart current process" helper) predate desktop-app. The relaunch is still `Popen([sys.executable] + sys.argv)` (`__main__.py:128`); #100 and zprocess #27 show that this relaunch path still differs from a fresh launch in other ways.
- **Severity**: cosmetic
- **Scope**: Windows
- **Related**: #100, #52 (other relaunch issues)
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as fixed.

### blacs #4: BLACS should check the labscript version used to compile the connection table (philipstarkey, opened 2014-10-02 [migrated], last activity 2014-10-02, 0 comments)
- **Summary**: After a labscript upgrade that changes the device hierarchy, an old connection table h5 gives obscure errors and can silently reset front-panel values; BLACS should detect the version mismatch and prompt a recompile. Asks whether this is worth doing.
- **Type**: feature request
- **Still valid?**: yes; no version check exists (`labscript_utils/connections.py` reads no version metadata). The hierarchy has not changed since gated-clocks, so the trigger has not recurred.
- **Scope**: blacs startup / labscript-utils ConnectionTable
- **Related**: #54 (version checks generally)
- **Effort**: small (store labscript/labscript-utils versions as attributes when compiling; compare at startup; warn)
- **Release relevance**: no
- **Rewrite relevance**: requirement: the connection table records compiler versions and the controller warns on mismatch.
- **Importance**: 1
- **Recommended action**: close as won't fix for legacy (the body itself proposes this as an option); carry the requirement to the rewrite.

---

### desktop-app

### desktop-app #20: Environments not being set correctly (dihm, opened 2022-04-01, last activity 2022-04-02, 3 comments)
- **Summary**: On one of five Miniconda installs, start-menu shortcuts stopped launching BLACS. Running `blacs.exe` from an unactivated prompt fails with `ImportError: DLL load failed while importing win32api` raised from `desktop_app/windows.py` during `import desktop_app`.
- **Type**: bug
- **Still valid?**: yes. `desktop_app/__init__.py:3` imports `.shell`, which imports `.windows`, which at module level (`windows.py:7-12`) imports `win32com.shell`, `win32com.client`, `win32com.propsys`. The entry point `desktop_app:entry_point` therefore loads pywin32 in the *launcher* process, before `launcher.py:64-74` builds the activated environment for the child. dihm's debugging in the comments (2022-04-02) confirms this: print statements placed before the `win32com` import in `desktop_app.windows` ran with `Conda Name: base` (the launcher, not yet activated), the import resolved pywin32 DLLs from whichever Python was on `PATH` (the base env with a different Python version, or an unrelated system Python), and only the later calls ran in the activated `labscript` env. Upgrading base Python to match made `blacs.exe` work from base but not the shortcuts. The `-gui` launcher runs under pythonw so the failure is silent.
- **Severity**: wrong-behaviour (shortcuts silently do nothing)
- **Scope**: Windows + conda
- **Related**: desktop-app #18 (another "shortcut does nothing silently" report)
- **Effort**: small (move the win32 imports into the functions that need them, or import `shell` lazily in `__init__`; `launcher.py` needs none of it)
- **Release relevance**: yes: desktop-app is a dependency of every suite GUI; the fix is a safe import reorganisation and should ship before the release.
- **Rewrite relevance**: none (shotscript's launcher design is separate), but the lesson applies: the launcher must import nothing environment-dependent.
- **Importance**: 4
- **Recommended action**: fix for next release.

### desktop-app #18: GUI entry point doesn't work (demberto, opened 2022-03-06, last activity 2022-03-06, 4 comments)
- **Summary**: A third-party package's `dycall-gui` entry point does nothing (no output); `python -m dycall` works. Asks what is wrong.
- **Type**: question-support
- **Still valid?**: resolved by the reporter. The comments show the reporter first blamed their own config, then switched to their own entry point (which they said is fine for them); the maintainer noted the config was correct, pointed at a `deskto-app.json` typo in setup.cfg and the possibility of a broken desktop-app from test PyPI, and offered to reproduce. The reporter closed and reopened the issue several times by accident; it ended open with "up to you what to do". No reproduction was ever attempted. The one real gap it exposed is that launcher failures under pythonw are invisible, which also hides #20.
- **Scope**: Windows; third-party use of desktop-app
- **Related**: #20
- **Effort**: small to add diagnostics (write launcher exceptions to a log file or show a message box when `sys.stderr` is None)
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close (reporter no longer needs it); add launcher-failure logging as part of #20.

### desktop-app #17: Customization on the desktopfile (hmaarrfk, opened 2021-05-02, last activity 2021-05-02, 0 comments)
- **Summary**: Allow customising the generated Linux `.desktop` file (e.g. MIME types, `%F` arguments).
- **Type**: feature request
- **Still valid?**: yes. `linux.py:397-413` writes a fixed four-key template; the TODO at `:403-404` acknowledges this.
- **Scope**: Linux
- **Related**: none
- **Effort**: small (extra keys from `desktop-app.json`, e.g. `Categories`, `MimeType`, `Exec` arguments)
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: fix later.

### desktop-app #14: Selectively fixing entry points (hmaarrfk, opened 2021-03-03, last activity 2021-03-03, 2 comments)
- **Summary**: `desktop-app install` rewrites all entry points of the distribution on conda; asks for a disable switch and a subcommand to fix a single entry point.
- **Type**: feature request
- **Still valid?**: partially fixed. The reporter's motivation (comments): several conda "virtual" packages each own some GUI entry points and should not clobber the others' scripts. The disable switch was added 26 days later: `--no-fix-entry-points` (`__main__.py:31-38`, `shell.py:260`, `:311-312`; commit `af652ad`, 2021-03-29). No per-entry-point subcommand; `fix_entry_points.py:100-130` still rewrites every console and gui script of the distribution. This only matters on conda.
- **Scope**: Windows + conda
- **Related**: #20
- **Effort**: trivial for the subcommand
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as fixed (the requested switch exists); reopen if the subcommand is wanted.

---

### Ranked table

| Rank | Issue | Type | Importance | Action |
|---|---|---|---|---|
| 1 | blacs #46 queue thread dies when the shot file cannot be written | bug | 4 | fixed in blacs #128 (merged 2026-10-18), with #29; issue closed |
| 2 | blacs #29 crash on shared drive becoming unavailable | bug | 4 | fixed in blacs #128 (merged 2026-10-18), with #46; issue closed |
| 3 | blacs #52 lost window after compile and restart | bug | 4 | fixed in blacs #128 (merged 2026-10-18), with #56; issue closed |
| 4 | desktop-app #20 launcher imports pywin32 before activating the env | bug | 4 | fixed in desktop-app #34 (merged 2026-10-17); issue closed |
| 5 | blacs #56 window geometry restoration | bug | 3 | fixed in blacs #128 (merged 2026-10-18), with #52; issue closed |
| 6 | blacs #100 setup_logging crashes when sys.stdout is None | bug | 3 | fixed in labscript-utils #133 (merged 2026-10-18); issue closed |
| 7 | blacs #49 StopIteration before first yield gives fatal error | bug | 3 | fixed in blacs #129 (merged 2026-10-18); issue closed |
| 8 | blacs #32 report which device paused the queue | feature | 3 | fixed in blacs #129 (merged 2026-10-18); issue closed |
| 9 | blacs #7 file dialogs default to "C:\\" | feature | 3 | fixed in blacs #129 (merged 2026-10-18); issue closed |
| 10 | blacs #72 default lyse host localhost, analysis on | feature | 3 | fixed in blacs #129 (merged 2026-10-18); issue closed |
| 11 | blacs #12 compile dialog unclosable when compiler child dies | bug | 3 | fix via runmanager #35 (refactor in progress), else later |
| 12 | blacs #54 remote worker version check | feature | 3 | fix later (next release if zprocess #14 merges) |
| 13 | blacs #58 final values for custom-UI tabs | feature | 2 | fix later |
| 14 | blacs #40 state machine defaults and errors | feature | 2 | fix later |
| 15 | blacs #31 graceful worker shutdown on restart | feature | 2 | fix later |
| 16 | blacs #50 report loaded/failed plugins | feature | 2 | fix later (after PR #123) |
| 17 | blacs #41 plugin base classes | feature | 2 | fix later |
| 18 | blacs #97 widget sizing on startup | bug | 2 | fix later; re-test on Qt6 |
| 19 | blacs #19 documentation out of date | docs | 2 | convert to docs task (delete stale files) |
| 20 | blacs #33 output limits from connection table | feature | 2 | leave open, blocked on labscript #44 |
| 21 | blacs #92 slow transition to buffered | performance | 2 | leave open (rewrite reference) |
| 22 | blacs #53 pipelining / cycle time design | design | 2 | leave open (rewrite design record) |
| 23 | blacs #24 remote control API | feature | 2 | leave open (rewrite) |
| 24 | blacs #23 analog input display | feature | 2 | leave open (rewrite) |
| 25 | blacs #116 real-time input display | feature | 2 | leave open (rewrite) |
| 26 | blacs #13 secondary control system | feature | 2 | leave open (remote workers done; GUIs not) |
| 27 | desktop-app #17 customise .desktop file | feature | 2 | fix later |
| 28 | blacs #57 stylesheet not applied on launch (PyQt 5.13) | bug | 1 | close as obsolete after a Qt6 launch check |
| 29 | blacs #45 startup with deleted queued shots | bug | 1 | close as stale (never reproduced; guard experiment_queue.py:390) |
| 30 | blacs #55 abort during cycle_time delay | bug | 1 | close as fixed (reporter-confirmed 2021) |
| 31 | blacs #15 per-device error-state check cost | performance | 1 | close as stale |
| 32 | blacs #115 better tab arrangement | feature | 1 | leave open as rewrite requirement or close as vague |
| 33 | blacs #4 check labscript version of connection table | feature | 1 | close as won't fix (rewrite requirement) |
| 34 | blacs #27 plugin tabs | feature | 1 | close as fixed (5ba525f) |
| 35 | blacs #5 AppID after compile and restart | bug | 1 | close as fixed (b296deb) |
| 36 | desktop-app #18 GUI entry point does nothing | support | 1 | close as stale |
| 37 | desktop-app #14 selective entry-point fixing | feature | 1 | close as fixed (af652ad) |

### Release-relevant issues

- blacs #46 / #29: wrap the shot-file cleanup in `experiment_queue.py:808-821` and `:926-947` so the queue-manager thread cannot die on I/O errors. Fixed in blacs #128 (merged 2026-10-18).
- blacs #52 / #56: replace the `move()/resize()` geometry restore (`__main__.py:481-515`) with `saveGeometry()/restoreGeometry()` plus a `QScreen` bounds check; Qt6 and Windows 11 multi-monitor. Fixed in blacs #128 (merged 2026-10-18).
- desktop-app #20: make `desktop_app/windows.py` pywin32 imports lazy so the launcher runs in an unactivated conda env. fixed in desktop-app #34 (merged 2026-10-17).
- blacs #100: guard `sys.stdout is None` in `labscript_utils/setup_logging.py:60` (and `sys.stderr` at `:73`).
- blacs #49: handle `StopIteration` from the first `__next__` at `tab_base_classes.py:792`. Fixed in blacs #129 (merged 2026-10-18).
- blacs #32, #7, #72: three trivial usability fixes (device names in pause status; dialog start directories from labconfig; localhost default for lyse). Fixed in blacs #129 (merged 2026-10-18).
- blacs #57 and #97: not fixes, but launch-time rendering must be checked under PySide6 and PyQt6 before tagging.
- blacs #54: becomes required if zprocess #14 (PAIR sockets) is merged, since mixed zprocess versions on remote worker PCs would then fail without a clear error. Not required by zprocess #33 (2026-10-19), which negotiates the socket type.
- blacs #19: delete `docs/UsingBLACS.pdf`, `docs/UsingBLACS.docx` and `docs/How to add a new device/` before the release.

## 3.x Issue triage: lyse, runviewer, zprocess, setuptools-conda, qtutils (2026-10-17)

Scope: all open issues of labscript-suite/lyse (25), labscript-suite/runviewer (13),
chrisjbillington/zprocess (7), chrisjbillington/setuptools-conda (3), and
philipstarkey/qtutils (#2, #22, #31) plus a review of qtutils PR #32. 51 issues, 1 PR.

Sources: full conversations from `scratchpad/issues/<repo>_<N>.txt` (regenerated during this
triage; an independent scrape in `scratchpad/issues-full/` agrees comment for comment) and
metadata from `scratchpad/issues/<repo>.json`. qtutils issues and PR #32 were scraped from
the JSON that github.com embeds in each page (`scratchpad/myscripts/scrape_embedded.py`);
the PR description was not recoverable, only its title, commits and the author's one comment.
Code was checked on the working trees, which are at the
upstream default branches: lyse `ed0b6ca` (2026-03-23), runviewer `4989087` (2026-03-23),
zprocess `34443e5` (2026-10-14), setuptools-conda `9cdc9ec` (2026-05-19), qtutils
`5d2885f` (2026-03-23).

The JSON lists also contain open PRs (lyse #132, #118, #85; zprocess #21, #14;
setuptools-conda #5). These are covered in PR-REVIEW.md and are only referenced here.

---

### lyse

### lyse #139: Slow lyse window loading with large numbers of analyses open (dihm, opened 2026-09-09, last activity 2026-09-09, 0 comments)
- **Summary**: Start-up is slow with many routines because each analysis subprocess is started and waited for in series, and each imports matplotlib and (under PySide6) a slow QApplication.
- **Type**: bug (performance)
- **Still valid?**: yes. `AnalysisRoutine.__init__` calls `start_worker()` synchronously (`lyse/routines.py:437`), once per routine from `RoutineBox.add_routines` (`routines.py:176-178`); `start_worker` calls `process_tree.subprocess(..., startup_timeout=30)` (`routines.py:455-459`), which blocks until the child has connected. Start-up time is therefore the sum of the child start-up times.
- **Severity**: annoyance
- **Scope**: lyse GUI start-up and configuration load; all platforms; worse with PySide6.
- **Related**: lyse #129 (PySide6 port, merged). No open PR.
- **Effort**: small to medium. The model row must be created in the main thread, but the `subprocess()` calls can be issued from a thread pool and the handles attached afterwards; or zprocess could expose a two-phase start (spawn all, then wait for all).
- **Release relevance**: yes. The release moves users to PySide6/PyQt6, where the per-process cost is higher, so this regresses perceived start-up time.
- **Rewrite relevance**: moot if shotscript.analysis keeps routines as functions in one service process, as designed.
- **Importance**: 3. Visible regression for labs with many routines, but no data impact.
- **Recommended action**: fix for next release (parallel start-up).

### lyse #123: Feature Idea: Adding datasets into lyse dataframe instead of just attributes (Cardoran, opened 2025-07-17, last activity 2025-07-17, 0 comments)
- **Summary**: A lab patched lyse so that datasets in `results/<group>` (not just attributes) are loaded into the dataframe and pushed to it by `save_result_array`, and asks whether the exclusion was deliberate.
- **Type**: feature request / question
- **Still valid?**: n.a. The patch relies on `labscript_utils.properties.get_group_items`, which does not exist upstream (`labscript_utils/properties.py` has only `get_attributes`). The second part of their patch (catching `ValueError` when setting an array cell) is already in master at `lyse/filebox.py:482-493`.
- **Scope**: dataframe construction (`dataframe_utilities.get_nested_dict_from_shot`) and `Run.save_result_array`.
- **Related**: lyse PR #132 (adds `data/` group attributes to the dataframe; PR-REVIEW rank 7), #26 (array cache), #44.
- **Effort**: small to implement, but the design cost is high: the dataframe is pickled and sent to every routine on each `lyse.data()` call, which is why arrays were kept out of it (chrisjbillington's comment in #26, 2017-06-21).
- **Release relevance**: no.
- **Rewrite relevance**: requirement. Decide up front which HDF5 locations feed the shot table (scalars only) and provide a fast, cached path for per-shot arrays; #26 and this issue are the same need.
- **Importance**: 2.
- **Recommended action**: reply (the exclusion is deliberate: dataframe size and serialisation cost; arrays belong in datasets read by `get_result_array`), then close as won't fix.

### lyse #94: [Question] Http protocol for adding shots to lyse (ldes89150, opened 2021-07-21, last activity 2021-07-21, 1 comment)
- **Summary**: How to submit shots to lyse from another control system. Answered the same day: zeromq REQ/REP with a pickled `{"filepath": path}` dict.
- **Type**: question-support
- **Still valid?**: n.a. Protocol unchanged: `lyse/communication.py:53-65` accepts a dict with key `filepath` or a bare string. Note the answer's code sample uses the key `filename`, which the handler does not accept; the bare-string form would have worked.
- **Scope**: lyse server.
- **Related**: none.
- **Effort**: trivial (documentation).
- **Release relevance**: no.
- **Rewrite relevance**: requirement: the shotscript analysis service's submission API must be documented.
- **Importance**: 1.
- **Recommended action**: close (answered); optionally convert to docs (document the server protocol in the lyse docs).

### lyse #90: re-adding dictionaries (lenz-f, opened 2021-02-09, last activity 2021-02-09, 0 comments)
- **Summary**: `save_result('result', {'a': 1, 'b': 2})` appears as one column `('Example','result')` holding the dict, but after removing and re-adding the shot it appears as two columns `('Example','result','a')` and `('Example','result','b')`.
- **Type**: bug
- **Still valid?**: yes. Two code paths build rows differently. On load from disk, `flatten_dict` recurses into dict values (`lyse/dataframe_utilities.py:107-116`), so a JSON-serialised dict attribute (stored by `set_attributes`, `labscript_utils/properties.py:79-91`) becomes extra column levels. On live update, `DataFrameModel.update_row` stores the value object in the single cell `(group, name)` (`lyse/filebox.py:479-493`).
- **Severity**: wrong-behaviour (column layout depends on history; multishot code must handle both shapes).
- **Scope**: lyse dataframe; all platforms.
- **Related**: #19 (column levels), #123.
- **Effort**: small. Either apply `flatten_dict` to `updated_row_data` values in `update_row` (and call `update_column_levels`), or stop flattening on load. Flattening on update is the consistent choice.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: one code path builds a shot's row, used for both initial load and updates.
- **Importance**: 3.
- **Recommended action**: fix for next release (small, self-contained).

### lyse #84: Analysis script logging (philipstarkey, opened 2020-11-05, last activity 2020-11-05, 0 comments)
- **Summary**: Proposal for a logging facility in the lyse API (output box and/or per-script log files) available to lyse internals and user scripts.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented; subprocess output still goes to the output box through zprocess output redirection.
- **Scope**: lyse API and analysis subprocess.
- **Related**: #37, #80 (closed).
- **Effort**: medium.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: the analysis service should provide routines with a logger and keep per-routine logs.
- **Importance**: 2.
- **Recommended action**: leave open (fix later).

### lyse #83: Analysis results groupname does not reflect full filename if the filename contains ".py" somewhere in the middle (philipstarkey, opened 2020-11-05, last activity 2020-11-05, 0 comments)
- **Summary**: The results group name was derived by `split('.py')[0]`, which truncates names containing `.py` in the middle. Also raises the broader point that group names ignore directories, so routine file names must be unique across analysislib.
- **Type**: bug
- **Still valid?**: fixed by `5138e40` (2023-04-18, "Resolve issue with Run object choosing group name based on script name"): `Run.__init__` now uses `Path(main_module_path).stem` (`lyse/__init__.py:293-295`). The directory-collision point remains by design.
- **Severity**: cosmetic
- **Scope**: `lyse.Run`.
- **Related**: none.
- **Effort**: n.a.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: results are keyed by function name in shotscript.analysis; two modules defining the same function name need a defined policy (qualify by module or reject).
- **Importance**: 1.
- **Recommended action**: close as fixed; if the namespace discussion is wanted, open a separate issue.

### lyse #81: Rename Run to Shot (philipstarkey, opened 2020-11-03, last activity 2020-11-04, 2 comments)
- **Summary**: Rename `lyse.Run` to `lyse.Shot` with a deprecation shim.
- **Type**: meta / API change
- **Still valid?**: n.a. PRs #85 and #118 implement it; the 2025-04 discussion on #118 ended with dihm recommending rejection (the `run time`/`run number`/`run repeat`/`n_runs` columns and attributes cannot be renamed compatibly) and philipstarkey agreeing.
- **Scope**: lyse API.
- **Related**: lyse PR #118 and #85 (PR-REVIEW rank 24, recommend close).
- **Effort**: medium, with user-facing churn.
- **Release relevance**: no.
- **Rewrite relevance**: moot (shotscript uses "shot" throughout).
- **Importance**: 1.
- **Recommended action**: close as won't fix together with PR #118, noting deferral to a major version if ever.

### lyse #53: Run.get_image has arguments with names that differ from labscript args (philipstarkey, opened 2019-08-17, last activity 2019-08-17, 1 comment)
- **Summary**: `Run.get_image(orientation, label, image)` uses different names from `Camera.expose(t, name, frametype)`; proposes renaming with keyword compatibility.
- **Type**: bug (API inconsistency)
- **Still valid?**: yes. `lyse/__init__.py:862`: `def get_image(self, orientation, label, image)`; same naming in `get_images` (889), `get_images_dict` (909), `get_image_attributes` (940). `IMAQdxCamera.expose(self, t, name, frametype='frame', ...)` at `labscript_devices/IMAQdxCamera/labscript_devices.py:186`.
- **Severity**: cosmetic
- **Scope**: lyse API.
- **Related**: none.
- **Effort**: trivial (accept both keyword spellings; document the new ones).
- **Release relevance**: no.
- **Rewrite relevance**: requirement: acquisition and analysis APIs use the same names for image keys.
- **Importance**: 2.
- **Recommended action**: fix later (or fold into the next API-touching change).

### lyse #44: Allow save_result_array(s) methods to use h5 dataset compression filters (philipstarkey for dihm, opened 2018-11-13, last activity 2018-11-13, 0 comments)
- **Summary**: Pass kwargs through to `create_dataset` so results can be compressed.
- **Type**: feature request
- **Still valid?**: fixed by `50be460` and `c415451` (2019-02-05): `save_result_array(..., **kwargs)` passes kwargs to `create_dataset` (`lyse/__init__.py:679-747`), `save_result_arrays(*args, **kwargs)` forwards them (843-859).
- **Scope**: lyse API.
- **Related**: #123.
- **Effort**: n.a.
- **Release relevance**: no.
- **Rewrite relevance**: requirement already noted for the shot-file writer (compression options on large datasets).
- **Importance**: 1.
- **Recommended action**: close as fixed.

### lyse #41: Improve plot window size behaviour (philipstarkey, opened 2018-10-30, last activity 2018-10-30, 0 comments)
- **Summary**: Plot window sizes do not match `figure(figsize=...)`, and only the first run sets the size.
- **Type**: bug
- **Still valid?**: yes. `Plot.update_window_size` resizes the canvas to `figsize*dpi` and then calls `self.ui.adjustSize()` (`lyse/analysis_subprocess.py:195-199`); `adjustSize` is based on size hints and is capped by Qt at two thirds of the screen, so large figures and the toolbar height are not honoured. `update_window_size` is called only on creation (152) and when a hidden window is re-shown (452-454), so later `figsize` changes are ignored (second bullet). The exact mismatch cannot be reproduced without a display.
- **Severity**: annoyance
- **Scope**: analysis subprocess plot windows; all platforms.
- **Related**: #5.
- **Effort**: small to medium (compute the window size from canvas plus toolbar, and add a "resize on each run" toggle).
- **Release relevance**: no.
- **Rewrite relevance**: requirement: plot windows honour `figsize`, with an option to re-apply it on each run.
- **Importance**: 2.
- **Recommended action**: fix later.

### lyse #35: Save visible columns in configuration (philipstarkey for rpanderson, opened 2017-12-15, last activity 2017-12-15, 0 comments)
- **Summary**: Persist which dataframe columns are hidden in the lyse configuration file.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented: `get_save_data` (`lyse/__main__.py:306-328`) saves routines, folders, pause state and window geometry only. Column visibility is tracked by index in `DataFrameModel.columns_visible` (`lyse/filebox.py:318, 400-403`) and by name for deleted columns in `deleted_columns_visible` (321, 537-539); the by-name map is what should be saved and seeded on load.
- **Scope**: lyse GUI state.
- **Related**: none.
- **Effort**: small.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: GUI state (hidden columns) persists per apparatus.
- **Importance**: 2.
- **Recommended action**: fix later.

### lyse #32: Second lyse instance (philipstarkey for PhyNerd, opened 2017-09-04, last activity 2017-09-05, 3 comments)
- **Summary**: Allow two lyse instances on one computer (one for live data, one for old data). Agreed approach in 2017: a command-line option selecting an alternative labconfig with a different port, propagated to the analysis subprocesses.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented: the port comes from labconfig (`lyse/__main__.py:136`), the labconfig path is fixed by `labscript_profile.default_labconfig_path` (`labscript_utils/labconfig.py:21, 39-41`), and lyse has no argument parsing. Subprocesses and `lyse.data()` clients also read the port from labconfig, so they would need the override too.
- **Scope**: lyse start-up, labconfig.
- **Related**: none.
- **Effort**: medium.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: the analysis service should be runnable against an arbitrary sequence directory and config without colliding with the live instance.
- **Importance**: 2.
- **Recommended action**: leave open (fix later).

### lyse #29: speed up shot loading (philipstarkey for PhyNerd, opened 2017-07-12, last activity 2017-07-18, 15 comments)
- **Summary**: Loading thousands of shots was slow; the discussion identified quadratic filepath lookups, `dict(row)` versus `to_dict()`, duplicate checks and batch size as the costs.
- **Type**: bug (performance)
- **Still valid?**: fixed by `22219f5` (2018-02-26, "feature: Performance optimisation."): `row_number_by_filepath` dict lookup (`lyse/filebox.py:470`), `iloc[...].to_dict()` (551), dict-membership duplicate check in `add_files` (659-666), adaptive batch size `len(df)//3 + 1` (857), progress indicator. The remaining idea (a Qt model backed directly by the dataframe with lazy formatting) was not done.
- **Severity**: annoyance
- **Scope**: lyse file box.
- **Related**: #26.
- **Effort**: n.a. for the fixed part; large for a dataframe-backed model.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: loading a 10 000-shot sequence must be fast; shotscript's persisted analysis dataset directory avoids re-reading shot files.
- **Importance**: 1.
- **Recommended action**: close as fixed; open a new issue only if the dataframe-backed model is wanted.

### lyse #26: Loading images takes too long (philipstarkey for PhyNerd, opened 2017-06-21, last activity 2017-08-10, 9 comments)
- **Summary**: Multishot routines that read thousands of images re-open every file; proposes a cross-routine in-memory cache (PhyNerd prototyped a storage server in the lyse server; never submitted as a PR).
- **Type**: feature request
- **Still valid?**: n.a. Not implemented. `lyse.routine_storage` (`lyse/__init__.py:90`) gives per-routine in-process persistence only.
- **Scope**: lyse server and `Run.get_image`.
- **Related**: #123, #29.
- **Effort**: medium.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: multishot routines that need per-shot arrays must not re-read every shot file; shotscript's per-shot cache with "mark as not done" reruns covers part of this.
- **Importance**: 2.
- **Recommended action**: close as stale (the prototype branch is on the Bitbucket archive) or leave open as a design note.

### lyse #25: Plots don't update after error (philipstarkey for PhyNerd, opened 2017-06-20, last activity 2017-07-04, 9 comments)
- **Summary**: After an error in a script, its plots stopped updating until the routine was removed and re-added. Not reproducible by the maintainer; the reporter later narrowed it to a multishot script added while BLACS was submitting shots, where the script raised `KeyError` because a single-shot column did not exist yet.
- **Type**: bug
- **Still valid?**: cannot verify (needs a GUI and the reporter's scripts). In current code `do_analysis` always runs `post_analysis_plot_actions` in its `finally` block (`lyse/analysis_subprocess.py:385-394`), so plots are redrawn whether or not the script raised. The `KeyError` the reporter saw is a user-script error.
- **Severity**: wrong-behaviour if real.
- **Scope**: analysis subprocess.
- **Related**: #4 (multishot runs before single-shot results exist).
- **Effort**: unknown.
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close as stale / cannot reproduce; ask for a new report if it recurs.

### lyse #23: Better loading of root attributes of the HDF5 file into lyse (philipstarkey, opened 2017-06-19, last activity 2017-06-19, 0 comments)
- **Summary**: Load root attributes of the shot file generically instead of one hand-written `try/except` per attribute.
- **Type**: feature request (refactor)
- **Still valid?**: n.a. Still ad hoc: `lyse/dataframe_utilities.py:84-106` reads `sequence_id`, `sequence_index`, `run time`, `run number`, `run repeat`, `n_runs` individually.
- **Scope**: dataframe construction.
- **Related**: lyse PR #132 (adds another location the same way).
- **Effort**: small.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: the shot-file schema defines which root attributes exist, and the table builder reads them generically.
- **Importance**: 1.
- **Recommended action**: leave open (fix later) or close as won't fix for legacy.

### lyse #131: #23: Automatic data for insersion into labbook (philipstarkey for ispielma, opened 2017-04-21, last activity 2026-01-26, 3 comments)
- **Summary**: Copy figures and selected text from lyse to the clipboard for a lab book. The 2017 discussion listed three items: a copy-to-clipboard button, a function to trigger it, and a function to add text to what is copied.
- **Type**: feature request
- **Still valid?**: n.a. Items 1 and 2 exist: a "Copy to clipboard" toolbar action on every plot window (`lyse/analysis_subprocess.py:139-143`) and `lyse.utils.worker.figure_to_clipboard()` callable from scripts (`lyse/utils/worker.py:47`; not listed in `lyse.__all__`). Item 3 does not exist. The 2026-01-26 activity is a label change.
- **Scope**: plot windows.
- **Related**: none.
- **Effort**: small for item 3.
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close as fixed (items 1 and 2); retitle (the "#23" prefix is a Bitbucket import artefact) if kept for item 3.

### lyse #19: Need to check behaviour when dataframe number of levels decreases (philipstarkey for chrisjbillington, opened 2017-02-23, last activity 2017-02-23, 0 comments)
- **Summary**: Possible crash if shots with N > 2 column levels are added, removed, and shots with fewer levels are added.
- **Type**: bug (unconfirmed)
- **Still valid?**: obsolete. The number of levels never decreases: the dataframe starts as a MultiIndex frame (`lyse/filebox.py:299`), rows are removed with `drop`, which keeps columns (345), and `update_column_levels` relies on this (405-409, docstring).
- **Severity**: n.a.
- **Scope**: lyse dataframe.
- **Related**: #90.
- **Effort**: n.a.
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close (not a bug under the current implementation).

### lyse #14: Multi-shot analysis routines still run when analysis is paused (philipstarkey for shjohnst, opened 2015-06-09, last activity 2017-06-29, 1 comment)
- **Summary**: After a multishot error pauses analysis, new shots still trigger the multishot routines while single-shot routines are paused.
- **Type**: bug
- **Still valid?**: yes. `FileBox.analysis_loop` (`lyse/filebox.py:913-945`): when paused the inner loop breaks (941-942), then `if self.multishot_required: self.do_multishot_analysis()` (943-945) runs with no pause check. `multishot_required` is cleared only on `'done'` (1006), so after a multishot error every arriving shot (which sets `analysis_pending` at 903) re-runs the failing multishot routine. PhyNerd's 2017 suggestion (`return` instead of `break`, or `and not self.analysis_paused`) is the fix.
- **Severity**: wrong-behaviour
- **Scope**: lyse analysis loop; all platforms.
- **Related**: #2, #4.
- **Effort**: trivial.
- **Release relevance**: no platform dependence, but trivial and long-standing; include.
- **Rewrite relevance**: requirement: pausing the analysis queue pauses both per-shot and multishot work.
- **Importance**: 3.
- **Recommended action**: fix for next release.

### lyse #8: Analysis windows should be grouped by script on the task bar (philipstarkey, opened 2014-07-10, last activity 2014-07-10, 1 comment)
- **Summary**: On Windows all plot windows are grouped under one taskbar entry; wants one entry per routine.
- **Type**: feature request
- **Still valid?**: n.a. All lyse processes set the same app id `'lyse'` (`lyse/__main__.py:21`, `lyse/analysis_subprocess.py:45-46`), so grouping is per application, as described.
- **Scope**: Windows taskbar only.
- **Related**: none.
- **Effort**: small (per-routine app id suffix), with the side effect that per-routine groups lose the lyse icon/pin association unless registered.
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close as won't fix.

### lyse #7: Analysis scripts should be saved in the h5 file (philipstarkey, opened 2014-07-10, last activity 2014-07-10, 1 comment)
- **Summary**: Store a copy of each analysis script in the shot file, as is done for the labscript file.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented (no code in `lyse/__init__.py`, `analysis_subprocess.py` or `routines.py` writes script text to the file).
- **Scope**: `lyse.Run` / analysis subprocess.
- **Related**: #84.
- **Effort**: small (write under `results/<group>` on first save; beware file growth for routines run many times).
- **Release relevance**: no.
- **Rewrite relevance**: requirement: record routine provenance with results; shotscript.analysis's module version hash covers this.
- **Importance**: 2.
- **Recommended action**: fix later.

### lyse #6: Analysis Globals (philipstarkey, opened 2014-07-10, last activity 2018-11-13, 3 comments)
- **Summary**: A pane in lyse for analysis-only globals stored in a separate file and recorded in the shot when analysis runs; labs currently misuse runmanager globals for this. Bumped by PhyNerd (2017) and dihm (2018).
- **Type**: feature request
- **Still valid?**: n.a. Not implemented in lyse.
- **Scope**: lyse GUI and API.
- **Related**: none.
- **Effort**: large.
- **Release relevance**: no.
- **Rewrite relevance**: moot: shotscript.analysis has its own globals file (`[analysis] globals` in the config).
- **Importance**: 2.
- **Recommended action**: leave open (won't fix in legacy; point to the successor).

### lyse #5: Plot windows should remember their position/size/autoscale (philipstarkey, opened 2014-07-10, last activity 2014-07-10, 0 comments)
- **Summary**: Plot windows should persist geometry and autoscale/lock state across lyse restarts and routine re-adds.
- **Type**: feature request
- **Still valid?**: mostly fixed by `fd624b0` (2025-11-18): geometry is saved to a per-script QSettings file and restored on creation (`lyse/analysis_subprocess.py:69-104`). Axis lock state and limits are carried over only when the Plot class changes within a session (`get_window_state`, 219-236), not across restarts.
- **Scope**: plot windows.
- **Related**: #41.
- **Effort**: small for the lock state.
- **Release relevance**: no.
- **Rewrite relevance**: requirement (same persistence for the successor's plot windows).
- **Importance**: 1.
- **Recommended action**: close as fixed; open a narrow issue for persisting axis lock state if wanted.

### lyse #4: Add ability to run multi-shot analysis before all single-shot routines are complete (philipstarkey for shjohnst, opened 2014-07-07, last activity 2014-07-10, 1 comment)
- **Summary**: Option to run multishot routines after each shot's single-shot analysis instead of only when no incomplete shots remain, for fast experiments where analysis cannot keep up.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented: `multishot_required` is set only when `get_first_incomplete()` returns `None` (`lyse/filebox.py:933-934`) or by the button (812).
- **Scope**: lyse analysis loop.
- **Related**: #2, #14.
- **Effort**: small (a checkbox and one condition), but multishot then runs on a partially updated dataframe, which #25 shows users do not handle well.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: define the multishot scheduling policy (after every shot, after N shots, or when idle) in the analysis service.
- **Importance**: 2.
- **Recommended action**: fix later.

### lyse #2: Shots arriving during multi-shot analysis are not analysed (philipstarkey for shjohnst, opened 2014-07-07, last activity 2014-07-10, 1 comment)
- **Summary**: A shot added while a multishot routine was running was not analysed until another shot arrived.
- **Type**: bug
- **Still valid?**: fixed in the Qt port (`4f69e8b`, 2014-11-21, "Qt: Working on analysis loop"): the loop waits on a `threading.Event` (`lyse/filebox.py:737, 922-923`) that the incoming loop sets on every batch (903); a shot arriving during multishot leaves the event set, so the next iteration analyses it.
- **Severity**: n.a.
- **Scope**: lyse analysis loop.
- **Related**: #4, #14.
- **Effort**: n.a.
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close as fixed.

---

### runviewer

### runviewer #47: Resampling algorithm could be more efficient for large datasets (philipstarkey, opened 2020-06-22, last activity 2020-06-22, 1 comment)
- **Summary**: Slice traces to the visible range before passing them to the C resampler.
- **Type**: feature request (performance)
- **Still valid?**: yes. `__pool_resample` passes the full trace (`runviewer/__main__.py:1276-1290`) and `resample()` copies the whole trace to float64 on every call (1058-1059) before calling `_resample`. The extension (`labscript-c-extensions/src/runviewer/resample.pyx`) handles the out-of-range and `stop_time` cases itself, so slicing must keep one point either side of the view and pass `stop_time` unchanged.
- **Scope**: runviewer; large traces (10^6 points).
- **Related**: #13 (same function).
- **Effort**: small.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: the successor's trace viewer resamples only the visible range.
- **Importance**: 2.
- **Recommended action**: fix later (together with #13).

### runviewer #46: Unnecessary redraw when changing window focus (philipstarkey, opened 2020-06-22, last activity 2020-06-22, 0 comments)
- **Summary**: Regaining window focus redraws all plots, which hangs runviewer with large data; cause unknown (pyqtgraph or Windows).
- **Type**: bug
- **Still valid?**: cannot verify (needs a display, Windows, large shot; pyqtgraph has had several releases since).
- **Severity**: annoyance
- **Scope**: runviewer, probably Windows.
- **Related**: #47.
- **Effort**: unknown.
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close as stale; reopen with a reproduction on current pyqtgraph/Qt6.

### runviewer #45: Progress indicator when loading shots (philipstarkey, opened 2020-06-22, last activity 2020-06-22, 0 comments)
- **Summary**: Show progress while loading a large shot.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented; `load_shot` constructs `Shot(filepath)` synchronously in the GUI thread (`runviewer/__main__.py:782-784`) and traces are parsed on first access.
- **Scope**: runviewer GUI.
- **Related**: none.
- **Effort**: small to medium (move parsing off the GUI thread first).
- **Release relevance**: no.
- **Rewrite relevance**: requirement.
- **Importance**: 2.
- **Recommended action**: fix later.

### runviewer #44: Select markers dropdown doesn't behave as expected (philipstarkey, opened 2020-06-22, last activity 2020-06-22, 0 comments)
- **Summary**: Removing and re-adding a shot left duplicate entries in the markers dropdown with inconsistent enabled state.
- **Type**: bug
- **Still valid?**: fixed by `c15fc9f` (2023-12-29, "Remove shots from markers dropdown when they are deleted."): `on_remove_shots` removes the combobox item (`runviewer/__main__.py:714-716`). Residual defect: lookup is by `findText(basename)` (716, 743, 755, 814), so two loaded shots with the same file name in different directories address the wrong entry.
- **Severity**: cosmetic
- **Scope**: runviewer GUI.
- **Related**: none.
- **Effort**: trivial (look up by item data instead of text).
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close as fixed; fix the basename lookup opportunistically.

### runviewer #26: (Py)Qt version incompatibility (philipstarkey, opened 2020-04-05, last activity 2020-09-30, 1 comment)
- **Summary**: With PyQt 5.13.1+ plots did not display, attributed to pyqtgraph/pyqtgraph#1057; a user asked for a documentation note.
- **Type**: bug (upstream)
- **Still valid?**: obsolete. The pyqtgraph defect was fixed upstream in 0.11; runviewer requires `pyqtgraph>=0.11.1` since `968248d` (2023-09-26) and master now runs on PyQt5, PyQt6 and PySide6 (`4989087`, 2026-03-23).
- **Severity**: n.a.
- **Scope**: runviewer.
- **Related**: none.
- **Effort**: n.a.
- **Release relevance**: no (the pin already excludes the broken combination).
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close as fixed/obsolete.

### runviewer #22: Units (philipstarkey for shjohnst, opened 2018-05-03, last activity 2018-05-03, 1 comment)
- **Summary**: Plot traces in calibrated units using the BLACS unit-conversion classes, with a per-channel selector.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented: the axis label uses only the unit string stored with the trace (`runviewer/__main__.py:993-1014`); no conversion class is applied.
- **Scope**: runviewer; depends on connection-table unit conversion metadata.
- **Related**: none.
- **Effort**: medium.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: the viewer displays channels in the same calibrated units as control, using the same conversion definitions.
- **Importance**: 2.
- **Recommended action**: leave open (fix later).

### runviewer #21: Shot enabled checkbox should be relocated (philipstarkey, opened 2018-05-02, last activity 2018-05-02, 0 comments)
- **Summary**: Move the enable checkbox out of the path column into its own first column: `|enabled|colour|shutters|path|`.
- **Type**: feature request (UI)
- **Still valid?**: n.a. Unchanged: header `['colour', 'shutters', 'path']` (`runviewer/__main__.py:219`), checkbox on the path item (803-806).
- **Scope**: runviewer GUI.
- **Related**: none.
- **Effort**: trivial.
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: fix later or close as won't fix.

### runviewer #17: Tooltip should show line number from experiment logic file (philipstarkey, opened 2017-11-06, last activity 2017-11-06, 1 comment)
- **Summary**: Record the user-code call site for each instruction so runviewer can show which line produced a feature; proposed for the next major labscript.
- **Type**: feature request (labscript and runviewer)
- **Still valid?**: n.a. Not implemented in labscript or runviewer.
- **Scope**: labscript compiler, shot-file format, runviewer.
- **Related**: none.
- **Effort**: large for legacy.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: the shotscript compiler records the user call site per instruction (for error messages and the viewer); chrisjbillington's 2017 comment describes the `_inst_depth` scheme.
- **Importance**: 2 (as a rewrite requirement; 1 for legacy).
- **Recommended action**: close for legacy as won't fix; carry into the shotscript design.

### runviewer #16: Shutter markers for shutters attached to PulseBlasters do not show up (philipstarkey, opened 2017-10-02, last activity 2018-05-11, 1 comment)
- **Summary**: Shutter markers were computed in `_load_device`, which PulseBlaster direct outputs bypass; proposed moving the computation into `add_trace`. PhyNerd reported it fixed in 2018.
- **Type**: bug
- **Still valid?**: fixed. `Shot.add_trace` computes shutter times for any added trace whose connection-table entry is a `Shutter` with `open_state` (`runviewer/__main__.py:1531-1541`), which is the proposed fix; `_load_device` only reads precomputed times from `runviewer/shutter_times` (1579-1581). Not tested against a PulseBlaster shot file here.
- **Severity**: wrong-behaviour (historical)
- **Scope**: runviewer, PulseBlaster direct outputs.
- **Related**: none.
- **Effort**: n.a.
- **Release relevance**: no.
- **Rewrite relevance**: none.
- **Importance**: 1.
- **Recommended action**: close as fixed.

### runviewer #14: Smaller plots for digitals (philipstarkey for PhyNerd, opened 2017-06-27, last activity 2024-05-03, 5 comments)
- **Summary**: Shorter plots with Hi/Lo ticks for digital channels; later suggestions: per-type height preferences, a `QSplitter`, channel names as titles. A user asked for status in 2024.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented; every channel gets the same plot height.
- **Scope**: runviewer GUI.
- **Related**: #9.
- **Effort**: medium.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: compact display of digital channels (and user-adjustable heights) in the successor's viewer.
- **Importance**: 2.
- **Recommended action**: leave open; reply to the 2024 question that no implementation was merged.

### runviewer #13: Short pulses at t=0 not visible when zoomed out (philipstarkey for shjohnst, opened 2017-06-27, last activity 2017-06-27, 0 comments)
- **Summary**: A short digital pulse at t=0 is not drawn until the view is zoomed in to within about three orders of magnitude of the pulse length, although the resampler is meant to preserve short features.
- **Type**: bug
- **Still valid?**: yes, in the extension. In `labscript-c-extensions/src/runviewer/resample.pyx` the lead-in loop fills output bins before the first data point three at a time (`while x_out[i] < x_in[0]: y_out[i:i+3] = NAN; i += 3`), then skips input points earlier than `x_out[i]` (`while x_in[j] < x_out[i]: j += 1`). When the view starts before t=0 (pyqtgraph pads the auto-range), up to three output bins after `x_in[0]` are left NaN and any input points inside them are never examined by the jump search. With 6000 output bins, a pulse shorter than roughly view width / 2000 at t=0 is dropped, which matches the report (100 µs pulse hidden until the view is about 0.2 s). The `i < N_out - 2` loop later preserves short pulses elsewhere.
- **Severity**: wrong-behaviour (misleading display)
- **Scope**: labscript-c-extensions resampler; all platforms.
- **Related**: #47.
- **Effort**: small (fill one bin at a time, or stop the lead-in at the bin containing `x_in[0]` and let the jump search cover it). Needs a rebuild of labscript-c-extensions, which the release requires anyway for Python 3.13 to 3.15 wheels.
- **Release relevance**: yes, in the sense that labscript-c-extensions wheels must be rebuilt for the new Python versions and this fix should ride along.
- **Rewrite relevance**: requirement: the successor's resampler must never hide an instruction, including at the start of the trace.
- **Importance**: 3.
- **Recommended action**: fix for next release (in labscript-c-extensions; move the issue there).

### runviewer #9: Grouping of channels not implemented (philipstarkey for shjohnst, opened 2017-06-20, last activity 2017-06-20, 0 comments)
- **Summary**: The group/ungroup buttons do nothing; the intent was to plot several channels on one axis.
- **Type**: feature request
- **Still valid?**: n.a. Still not implemented; the buttons are disabled with a comment to that effect (`runviewer/__main__.py:306-308`).
- **Scope**: runviewer GUI.
- **Related**: #14.
- **Effort**: medium.
- **Release relevance**: no.
- **Rewrite relevance**: requirement: overlay several channels on one axis.
- **Importance**: 1.
- **Recommended action**: leave open, or remove the buttons and close.

### runviewer #3: rfblaster support (philipstarkey for shjohnst, opened 2015-06-12, last activity 2015-06-12, 0 comments)
- **Summary**: runviewer cannot display RFBlaster output.
- **Type**: feature request
- **Still valid?**: n.a. `labscript_devices/RFBlaster.py` imports `runviewer_parser` (line 16) but defines no parser class.
- **Scope**: RFBlaster hardware (legacy Monash device).
- **Related**: none.
- **Effort**: small to medium; needs hardware knowledge of the instruction table.
- **Release relevance**: no.
- **Rewrite relevance**: none (device not in scope).
- **Importance**: 1.
- **Recommended action**: close as won't fix unless an RFBlaster user volunteers; belongs in labscript-devices.

---

### zprocess

### zprocess #27: `disable_quick_edit()` crashes when restarting BLACS from a ConPTY console (damienBloch, opened 2026-06-18, last activity 2026-06-18, 0 comments)
- **Summary**: On Windows 11 under Windows Terminal or the VS Code terminal, restarting BLACS crashes at import of `labscript_utils` with `pywintypes.error 87` from `SetConsoleMode`; `GetConsoleMode` is guarded but `SetConsoleMode` is not. Reporter supplies a two-line fix.
- **Type**: bug
- **Still valid?**: yes. `zprocess/utils.py:180-191`: the `Get` call is in `try/except pywintypes.error`, `console.SetConsoleMode(new_mode)` at line 190 is not. `labscript_utils/__init__.py:101` calls this at import, so any labscript program relaunched from a ConPTY console is affected, not only BLACS.
- **Severity**: crash-data-loss (program fails to start; no data loss).
- **Scope**: Windows, ConPTY consoles (Windows Terminal is the default console on current Windows 11).
- **Related**: none.
- **Effort**: trivial (wrap the `Set` call and skip the `atexit` registration on failure).
- **Release relevance**: yes. Windows 11 with Windows Terminal is the normal environment for new installs; restart from BLACS is a daily operation.
- **Rewrite relevance**: moot (zprocess dropped; shotscript should not alter console modes).
- **Importance**: 5.
- **Recommended action**: fix for next release and publish a zprocess point release.
- **Status (2026-10-17)**: fixed by zprocess PR #28, merged 2026-10-17; tested on Windows 11 with BLACS: 2.27.0 exits with the issue's traceback when restarted from PowerShell in Windows Terminal, the branch restarts, and a start from cmd.exe still turns quick-edit off. The cause is the console input mode that PowerShell leaves at its prompt, which `SetConsoleMode` rejects once `ENABLE_QUICK_EDIT_MODE` is cleared; cmd.exe is unaffected (`TESTING.md`).

### zprocess #19: `make_shared_secret` fails with ZMQError: Not supported (dihm, opened 2024-01-29, last activity 2024-09-20, 3 comments)
- **Summary**: With the conda defaults channel's zeromq 4.3.5 on Windows, `zmq.curve_keypair()` raises `Not supported` (libzmq built without CURVE), so `python -m zprocess.makesecret` fails. Reported to anaconda-issues#13339; still broken as of 2024-09.
- **Type**: bug (upstream packaging) / tooling
- **Still valid?**: cannot verify here (depends on the conda build). zprocess has no handling: `generate_shared_secret` calls `zmq.curve_keypair()` directly (`zprocess/security.py:66-67`), and `SecureContext` sets CURVE socket options when a shared secret is configured, so every secured program fails on such a build, not only the key generator.
- **Severity**: crash-data-loss (secured installs cannot start).
- **Scope**: Windows conda installs using the defaults channel.
- **Related**: #16 (same root cause, milder symptom), labscript-suite/labscript-suite#83.
- **Effort**: small: check `zmq.has('curve')` at `SecureContext` creation and in `makesecret`, and raise a message naming the fix (install pyzmq from PyPI wheels or conda-forge); plus an installation-docs note.
- **Release relevance**: yes. The release installation instructions must specify a pyzmq source with CURVE support, and zprocess should fail with a readable message rather than `ZMQError: Not supported`.
- **Rewrite relevance**: moot (no zeromq).
- **Importance**: 4.
- **Recommended action**: fix for next release (diagnostic message and docs); the packaging defect itself stays upstream.

### zprocess #16: conda's pyzmq no longer built using libsodium on windows (dihm, opened 2021-12-24, last activity 2021-12-25, 1 comment)
- **Summary**: conda's Windows pyzmq lost libsodium when `zeromq` stopped being a pyzmq dependency (22.2.1), giving slow CURVE and warnings. Maintainer noted it is a recurring upstream regression.
- **Type**: bug (upstream packaging)
- **Still valid?**: cannot verify (packaging). zprocess itself emits no libsodium warning (no such text in `zprocess/`); the warnings came from pyzmq/libzmq. Superseded by #19, where the same build now lacks CURVE entirely.
- **Severity**: annoyance
- **Scope**: Windows conda.
- **Related**: #19.
- **Effort**: n.a.
- **Release relevance**: covered by #19.
- **Rewrite relevance**: moot.
- **Importance**: 1.
- **Recommended action**: close as duplicate of #19.

### zprocess #13: Non-ideal extra processes in venv (chrisjbillington, opened 2020-05-31, last activity 2020-05-31, 0 comments)
- **Summary**: In Windows venvs, subprocesses go through the `python.exe` launcher shim, adding an intermediate process; copy multiprocessing's use of `sys._base_executable` with `__PYVENV_LAUNCHER__`.
- **Type**: bug
- **Still valid?**: fixed by `4d7a5d3` (2022-01-29, "Address issue #13 - skip venv shim when possible"): `get_venv_executable_and_env` (`zprocess/utils.py:265-279`), used by `process_tree.py:1391`.
- **Severity**: n.a.
- **Scope**: Windows and macOS venvs.
- **Related**: none.
- **Effort**: n.a.
- **Release relevance**: no.
- **Rewrite relevance**: moot.
- **Importance**: 1.
- **Recommended action**: close as fixed.

### zprocess #9: sphinx docs (chrisjbillington, opened 2018-05-29, last activity 2018-05-29, 0 comments)
- **Summary**: Make a sphinx skeleton reading the docstrings and fold the examples into it.
- **Type**: docs
- **Still valid?**: n.a. A skeleton exists (`zprocess/doc/conf.py`, `index.rst`, `requirements.txt`) but is not published.
- **Scope**: zprocess docs.
- **Related**: zprocess PR #21 (example fix; PR-REVIEW rank 13).
- **Effort**: small to medium.
- **Release relevance**: no.
- **Rewrite relevance**: moot.
- **Importance**: 1.
- **Recommended action**: close as won't fix (zprocess is in maintenance only).

### zprocess #8: Callback for zlock failure (chrisjbillington, opened 2018-03-28, last activity 2018-03-28, 0 comments)
- **Summary**: Let programs register a callback (retry/ignore/fail) when the zlock server is unreachable instead of raising.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented.
- **Scope**: zlock client.
- **Related**: none.
- **Effort**: medium.
- **Release relevance**: no.
- **Rewrite relevance**: moot (no lock server; the analysis service is the single writer of results).
- **Importance**: 1.
- **Recommended action**: close as won't fix.

### zprocess #6: Expose proccess communication ports (chrisjbillington for PhyNerd, opened 2017-11-19, last activity 2017-11-19, 0 comments)
- **Summary**: Expose a Process's socket ports so the sockets can be re-created in another process.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented.
- **Scope**: zprocess process tree.
- **Related**: none.
- **Effort**: small, but it exposes internals that the heartbeat and security layers assume are private.
- **Release relevance**: no.
- **Rewrite relevance**: moot.
- **Importance**: 1.
- **Recommended action**: close as won't fix.

---

### setuptools-conda

### setuptools-conda #26: Better controls for enforcing GIL/free-threaded python (dihm, opened 2026-05-15, last activity 2026-05-21, 2 comments)
- **Summary**: For Python 3.14t builds the conda convention is to depend on `python-gil` or `python-freethreading`, but setuptools-conda hard-codes `python` in host/run requirements with no way to append. Both participants agreed to wait for upstream (mamba/conda ABI metadata) and use `ignore-run-exports` as a workaround meanwhile.
- **Type**: feature request
- **Still valid?**: n.a. `setuptools_conda/setuptools_conda.py:729-730` still hard-codes `'python'` in `host` and `run`; the workaround from the discussion (PR #27, merged as `6b86423`) is in master.
- **Scope**: conda packaging of compiled packages (labscript-c-extensions) for free-threaded Pythons.
- **Related**: setuptools-conda PR #5 (extras; PR-REVIEW rank 23).
- **Effort**: small (an `--append-requirements` option) or medium (ABI-aware `pythons` entries like `3.14t`).
- **Release relevance**: only if the release publishes conda packages for free-threaded Pythons; otherwise no.
- **Rewrite relevance**: moot (no conda).
- **Importance**: 2.
- **Recommended action**: leave open (decision recorded: wait for upstream).

### setuptools-conda #9: Set conda channels for each dependency (rpanderson, opened 2021-07-19, last activity 2021-07-20, 1 comment)
- **Summary**: Per-dependency channel or pip source, as poetry2conda does. Maintainer answered that conda packages cannot carry this information, so it is out of scope.
- **Type**: feature request
- **Still valid?**: n.a.
- **Scope**: setuptools-conda.
- **Related**: none.
- **Effort**: n.a. (out of scope).
- **Release relevance**: no.
- **Rewrite relevance**: moot.
- **Importance**: 1.
- **Recommended action**: close as won't fix (already explained in the thread).

### setuptools-conda #2: Save recipes instead of building (chrisjbillington, opened 2020-05-15, last activity 2020-05-18, 1 comment)
- **Summary**: Option to output a conda-forge-style recipe pointing at PyPI instead of building locally.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented; a recipe directory is generated internally (`setuptools_conda.py:669-671, 760`) but there is no save option and the source URL is the local sdist.
- **Scope**: setuptools-conda.
- **Related**: none.
- **Effort**: small to medium.
- **Release relevance**: no.
- **Rewrite relevance**: moot.
- **Importance**: 1.
- **Recommended action**: close as won't fix or leave open as a note.

---

### qtutils

### qtutils #2: Options to clear the output box (philipstarkey for chrisjbillington, opened 2014-10-04, last activity 2014-10-04, 0 comments)
- **Summary**: `OutputBox` should offer a context-menu "clear"; optionally Return adds a blank line and Ctrl+L scrolls so the next line is at the top.
- **Type**: feature request
- **Still valid?**: n.a. Not implemented in master (`qtutils/outputbox.py`); PR #32 attempts it (review below).
- **Scope**: qtutils OutputBox (used by runmanager, BLACS, lyse).
- **Related**: PR #32.
- **Effort**: trivial for the context-menu clear; the keyboard features need care (see PR review).
- **Release relevance**: no.
- **Rewrite relevance**: requirement if shotscript GUIs reuse an output box; otherwise none.
- **Importance**: 2.
- **Recommended action**: fix later via a reworked PR #32 (context-menu clear first).

### qtutils #22: Readthedocs builds failing (philipstarkey, opened 2023-04-08, last activity 2023-04-08, 0 comments)
- **Summary**: RTD builds were failing; probably a docs dependency.
- **Type**: tooling / docs
- **Still valid?**: partly. `readthedocs.yaml` was modernised in `c9a8bca` (2024-12-17: Ubuntu 22.04, Python 3.12, `pip install -e .[docs]`) and the docs extras list Sphinx>=7 and myst-parser (`pyproject.toml:50-58`; `recommonmark` is still listed but unused by `docs/conf.py`). https://qtutils.readthedocs.io/en/latest/ serves a page titled "qtutils 0.1.0.dev1 documentation" (checked 2026-10-17), so the build runs but setuptools_scm finds no tags in RTD's shallow checkout and reports a fallback version.
- **Severity**: cosmetic
- **Scope**: qtutils documentation.
- **Related**: none.
- **Effort**: trivial (`post_checkout: git fetch --unshallow` or `SETUPTOOLS_SCM_PRETEND_VERSION` in the RTD config; drop `recommonmark`).
- **Release relevance**: minor: qtutils 4.1.3 docs should report the right version when the release points users at them.
- **Rewrite relevance**: none.
- **Importance**: 2.
- **Recommended action**: fix for next release (one-line RTD config change), then close.

### qtutils #31: More PyQt6 aliases (chrisjbillington, opened 2026-03-20, last activity 2026-03-23, 2 comments)
- **Summary**: Tracking issue for binding-compatibility aliases: `exec`/`exec_` on QApplication and QDialog (done in `42fcc9e`), and any others found while porting labscript programs. dihm confirmed everything works with 4.1.3.
- **Type**: meta / tracking
- **Still valid?**: n.a. Implemented: `exec`/`exec_` aliases (`qtutils/qt.py:114-122`), QAction/QShortcut/QDesktopWidget location aliases (80-90), PyQt6 short enum names (92-111). No open items remain in the checklist.
- **Scope**: qtutils `qt` shim; PyQt5, PyQt6, PySide6.
- **Related**: lyse #129/#134, runviewer #70 (merged Qt6 ports).
- **Effort**: n.a.
- **Release relevance**: yes. The release's PySide6/PyQt6 support depends on qtutils>=4.1.3 (lyse already pins it); nothing further to do unless new aliases are found during release testing.
- **Rewrite relevance**: none.
- **Importance**: 2.
- **Recommended action**: close now that 4.1.3 is released; open specific issues for any alias found during release testing.
- **Status**: closed 2026-10-21 with a comment. The issue's premise that older PyQt5 lacks `exec()` is wrong: the sip declarations in the PyQt5 5.0 and 5.14 sources define `exec` under `%If (Py_v3)`, and the method tables of the PyPI wheels for 5.9 to 5.15 contain both names, so every Python 3 build of PyQt5 has both spellings. Only PyQt6 lacks `exec_()`. qtutils #40 keeps that alias alone and corrects the comment.

### qtutils PR #32: Add Outputbox clearing options (#2) (Json-To-String, opened 2026-05-16, last updated 2026-05-20)

Reviewed in the style of PR-REVIEW.md section 2. Head `453459d` (master merged in on 2026-05-20); `git merge-tree` reports no conflicts. 1 file, `qtutils/outputbox.py`, +53/-2, 4 commits.

**qtutils #32.** Adds a custom context menu with "Clear Output", a Return shortcut that appends a blank line, a Ctrl+L shortcut that deletes everything except the last line, and changes `flush()` to clear the box. Only the context-menu clear is mergeable as written. Defects: (1) `flush()` now calls `clear_output()`; `OutputBox` is file-like (`write`, `fileno`, `isatty`, `flush`) and is used as a stream target, and `logging.StreamHandler.emit()` calls `flush()` after every record (zprocess's `RichStreamHandler` and `rich_print`, shown in the file's own test block, do exactly this), so every log line would wipe the box; must revert to `pass`. (2) Both `QShortcut`s use the default `Qt.WindowShortcut` context, so Return and Ctrl+L fire whenever the host window (runmanager, BLACS, lyse main windows) is active, whatever has focus; a line edit does not claim Return through `ShortcutOverride`, so pressing Enter in other widgets would be consumed by the output box; needs `Qt.WidgetShortcut`. `self.shortcut` is also assigned twice. (3) `clear_output()` drains `_text_queue`, but the mainloop thread has already queued one `add_text()` call per item, and `add_text()` does a blocking `get()` (its `except queue.Empty` cannot fire); a drained item makes the next `add_text()` block the GUI thread until the next message arrives and leaves a permanent one-message lag; clear the widget only. (4) Ctrl+L discards history, which the author acknowledges contradicts the issue (scroll so the next line is at the top); either implement as a scroll or drop it. (5) `add_whitespace()` bypasses the zmq channel and pushes directly into `_text_queue` with charformat `'default'`, which is not a `FORMAT_ALIASES` key (it falls through `literal_eval` to plain white); use `'stdout'`. (6) Unscoped `Qt.CustomContextMenu` and `QTextCursor.End` work under PyQt6 only through qtutils' enum aliases (`qt.py:92-111`); the rest of the file uses the scoped forms. No CHANGELOG entry. Importance 2. Recommended action: ask the author for a rework (revert `flush`, `WidgetShortcut` context, do not drain the queue, decide Ctrl+L semantics), or have the maintainer merge the ~15-line context-menu part alone and close #2 with it.

---

### Ranked table

| Rank | Issue | Type | Importance | Action |
|---|---|---|---|---|
| 1 | zprocess #27 `disable_quick_edit` crash on ConPTY | bug (crash, Windows 11) | 5 | fixed 2026-10-17 by zprocess #28; issue closed; needs zprocess 2.28.0 |
| 2 | zprocess #19 `curve_keypair` Not supported on conda Windows | bug (upstream) + diagnostics/docs | 4 | fixed in zprocess #32 (merged 2026-10-18): clear error naming the pyzmq source, README Security section; the installation docs note is still to do; issue closed |
| 3 | lyse #14 multishot runs while paused | bug | 3 | fixed in lyse #145 (merged 2026-10-18); issue closed |
| 4 | lyse #90 dict results flattened inconsistently | bug | 3 | fixed in lyse #145 (merged 2026-10-18); issue closed |
| 5 | lyse #139 serial subprocess start-up | bug (performance) | 3 | fixed in lyse #145 (merged 2026-10-18); issue closed |
| 6 | runviewer #13 pulses at t=0 dropped by resampler | bug (in labscript-c-extensions) | 3 | fixed in labscript-c-extensions #13 (merged 2026-10-17); issue closed |
| 7 | qtutils #22 RTD version string | tooling | 2 | fixed in qtutils #37 (merged 2026-10-17); issue closed |
| 8 | qtutils #31 PyQt6 aliases tracker | meta | 2 | closed 2026-10-21; the dead `exec()` alias branch is removed in qtutils #40 |
| 9 | qtutils #2 / PR #32 clear output box | feature | 2 | fixed in qtutils #36 (merged 2026-10-17) (context-menu part of #32, author credited); issue closed |
| 10 | lyse #35 persist hidden columns | feature | 2 | fix later |
| 11 | lyse #41 plot window size | bug | 2 | fix later |
| 12 | lyse #53 get_image argument names | API | 2 | fix later |
| 13 | lyse #4 multishot before all single-shots | feature | 2 | fix later |
| 14 | lyse #7 save scripts in shot file | feature | 2 | fix later |
| 15 | lyse #84 logging | feature | 2 | leave open |
| 16 | lyse #32 second instance | feature | 2 | leave open |
| 17 | lyse #123 datasets in dataframe | feature/question | 2 | reply, close as won't fix |
| 18 | lyse #26 image cache | feature | 2 | close as stale or leave open |
| 19 | lyse #6 analysis globals | feature | 2 | leave open (successor has it) |
| 20 | runviewer #47 slice before resample | performance | 2 | fix later (with #13) |
| 21 | runviewer #45 progress indicator | feature | 2 | fix later |
| 22 | runviewer #22 units | feature | 2 | leave open |
| 23 | runviewer #14 smaller digital plots | feature | 2 | leave open, reply |
| 24 | runviewer #17 line numbers per instruction | feature | 2 (rewrite) | close for legacy; rewrite requirement |
| 25 | setuptools-conda #26 free-threaded python deps | feature | 2 | leave open (wait for upstream) |
| 26 | lyse #83 `.py` in group name | bug | 1 | close as fixed (5138e40) |
| 27 | lyse #44 compression kwargs | feature | 1 | close as fixed (50be460) |
| 28 | lyse #29 shot loading speed | performance | 1 | close as fixed (22219f5) |
| 29 | lyse #2 shots during multishot | bug | 1 | close as fixed (4f69e8b) |
| 30 | lyse #5 plot window geometry | feature | 1 | close as fixed (fd624b0) |
| 31 | lyse #131 lab book copy | feature | 1 | close as fixed (clipboard action exists) |
| 32 | lyse #19 fewer column levels | bug | 1 | close (not a bug) |
| 33 | lyse #25 plots after error | bug | 1 | close as stale |
| 34 | lyse #94 protocol question | question | 1 | close (answered) / docs |
| 35 | lyse #81 rename Run to Shot | meta | 1 | close as won't fix with PR #118 |
| 36 | lyse #23 root attributes | refactor | 1 | leave open or close |
| 37 | lyse #8 taskbar grouping | feature | 1 | close as won't fix |
| 38 | runviewer #44 markers dropdown | bug | 1 | close as fixed (c15fc9f) |
| 39 | runviewer #26 PyQt 5.13 plots | bug | 1 | close as obsolete |
| 40 | runviewer #16 PulseBlaster shutter markers | bug | 1 | close as fixed |
| 41 | runviewer #46 redraw on focus | bug | 1 | close as stale |
| 42 | runviewer #21 enabled checkbox column | UI | 1 | fix later or close |
| 43 | runviewer #9 channel grouping | feature | 1 | leave open or remove buttons |
| 44 | runviewer #3 rfblaster | feature | 1 | close as won't fix |
| 45 | zprocess #16 libsodium | upstream | 1 | close as duplicate of #19; the clear error in zprocess #32 (merged 2026-10-18) covers it. Left open by the maintainer on 2026-10-18 |
| 46 | zprocess #13 venv shim | bug | 1 | close as fixed (4d7a5d3) |
| 47 | zprocess #9 sphinx docs | docs | 1 | close as won't fix |
| 48 | zprocess #8 zlock callback | feature | 1 | close as won't fix |
| 49 | zprocess #6 expose ports | feature | 1 | close as won't fix |
| 50 | setuptools-conda #9 per-dependency channels | feature | 1 | close as won't fix |
| 51 | setuptools-conda #2 save recipes | feature | 1 | close as won't fix |

### Release-relevant issues

- zprocess #27: `SetConsoleMode` crash on Windows 11 / Windows Terminal when any labscript program is restarted. Two-line fix in `zprocess/utils.py:190`; needs a zprocess point release. Fixed by zprocess #28, merged 2026-10-17; issue closed. Tested on Windows 11 2026-10-17: the branch restarts BLACS from PowerShell in Windows Terminal, where 2.27.0 exits with the issue's traceback (`TESTING.md`).
- zprocess #19 (and #16): conda defaults' Windows zeromq lacks CURVE, so secured installs fail with `ZMQError: Not supported`. Add a `zmq.has('curve')` check with a readable message and state the required pyzmq source in the release installation docs. The error is in zprocess #32 (merged 2026-10-18); the docs note is still to do.
- lyse #139: serial analysis-subprocess start-up is slower under PySide6/PyQt6, which the release moves users to. Fixed in lyse #145 (merged 2026-10-18).
- lyse #14 and #90: small, long-standing behaviour bugs with contained fixes. Fixed in lyse #145 (merged 2026-10-18).
- runviewer #13: resampler drops short pulses at t=0; labscript-c-extensions must be rebuilt for Python 3.13 to 3.15 anyway, so include the fix. fixed in labscript-c-extensions #13 (merged 2026-10-17).
- qtutils #31 (closed 2026-10-21; aliases shipped in 4.1.3, which lyse pins; qtutils #40 removes the `exec()` alias branch, which no binding needs) and #22 (RTD shows version 0.1.0.dev1; fixed in qtutils #37 (merged 2026-10-17)).
- setuptools-conda #26 only if conda packages are built for free-threaded Pythons.

## 3.x Issue triage: runmanager, labscript-suite, mise, bias

Scope: 29 open runmanager issues (the JSON lists 31 entries; #128 and #104 are pull
requests, covered in PR-REVIEW.md), 20 labscript-suite issues, mise #1, bias #1.

Sources and limits:

- Issue bodies, every GitHub comment and the timeline events were read from the
  regenerated `scratchpad/issues/<repo>_<N>.txt` files. For issues migrated from
  Bitbucket the pre-2020 comments were also cross-checked with the archive at
  `https://bitbucket-archive.labscriptsuite.org/data/repositories/labscript_suite/<repo>/issues/<N>/comments_page=1.json`
  (saved in `scratchpad/bbarchive/`). The 2020-06-25 and 2023-10-09 "ReferencedEvent"
  entries on many issues are commits in personal forks whose messages mention the same
  issue numbers; they are migration artefacts, not fixes.
- runmanager code was read from `origin/master` (bfe63ba, merge of PR #130, 2026-10-17).
  Line numbers below refer to that commit. PR #130 split `runmanager/__main__.py` into
  `compiler.py`, `evaluator.py`, `expander.py`, `group_manager.py`, `differ.py`,
  `tokenizer.py`, `widgets.py`, `functions.py`, `exceptions.py`; the GUI (`RunManager`,
  `GroupTab`, `RemoteServer`, `compile_loop`, `guess_expansion_modes`) stayed in
  `__main__.py`. For every bug I state whether the refactor moved the relevant code.
  In no case did the refactor change the behaviour at issue.
- mise and bias are not cloned; those two are judged from the issue text only.

---

### runmanager

### runmanager #123: Comment-preservation behavior undesirable in runmanager.remote.set_globals (neutrinonerd3333, opened 2025-10-02, last activity 2025-10-02, 0 comments)
- **Summary**: `remote.set_globals()` appends the previous expression's final comment to the new value, even with `raw=True`. A `get_globals(raw=True)` / `set_globals(raw=True)` round trip therefore duplicates the comment on every cycle. Reporter proposes disabling it for `raw=True`, making it optional otherwise, and deprecating it; offers a PR.
- **Type**: bug
- **Still valid?**: yes. `RemoteServer.handle_set_globals`, `runmanager/__main__.py:3085-3095`: the comment is appended unconditionally, including when `raw=True`. The refactor kept this in `__main__.py` (was ~line 3571) and now calls `tokenizer.find_comments` instead of the local function.
- **Severity**: wrong-behaviour (silently corrupts stored globals on round trip)
- **Scope**: remote API; platform-independent
- **Related**: none
- **Effort**: trivial (skip the append when `raw`; optionally add a `preserve_comments` kwarg to `Client.set_globals`, `remote.py:44`)
- **Release relevance**: yes; a current user is blocked and offered a PR.
- **Rewrite relevance**: requirement: a remote set-globals API must be an exact inverse of get-globals; comment handling must be explicit, not implicit.
- **Importance**: 4
- **Recommended action**: fix for next release (accept the offered PR for points 1 and 2; skip the deprecation warning).

### runmanager #97: Remote API has no method for checking if compilation complete (philipstarkey, opened 2020-10-14, last activity 2020-10-14, 0 comments)
- **Summary**: Add a remote call that reports whether a compilation triggered by `engage()` has finished.
- **Type**: feature request
- **Still valid?**: n.a. (confirmed absent: `remote.py:29-114` and `RemoteServer` handlers `__main__.py:3044-3200` have no such method. The GUI state exists: `pushButton_abort.isEnabled()` and `compile_queue`.)
- **Scope**: remote API
- **Related**: #48 (continuous engage), #45; PR #104 compile queue
- **Effort**: small (`handle_is_compiling` returning `compile_queue.unfinished_tasks > 0` or the abort-button state, plus client method)
- **Release relevance**: no
- **Rewrite relevance**: requirement: remote API must expose compilation state (or `engage()` must block / return a handle).
- **Importance**: 3
- **Recommended action**: fix for next release if cheap, otherwise fix later.

### runmanager #66: Preparse thread memory leak/crash (philipstarkey for dihm, opened 2019-03-28, last activity 2019-04-16, 10 comments)
- **Summary**: With a complex globals group (six zip axes built with `np.concatenate`), the preparse thread consumed all memory and the engage button stayed greyed out. Archived comments establish the cause: preparse expands the full outer product only to count shots (57.6 million shots here), and on startup runmanager re-guesses expansion types rather than trusting those stored in the file. Reporter worked around it with `tuple()`; the thread ended with a word-wrap side discussion (merged in 2019).
- **Type**: bug
- **Still valid?**: yes. `preparse_globals`, `__main__.py:2101-2126`, calls `parse_globals(..., expand_globals=True)` and sets `self.n_shots = len(shots)`; `expander.expand_globals` (`expander.py:113-120`) materialises every shot with `itertools.product`, so memory scales with the shot count. `expand_globals` already computes `dimensions` (axis lengths) that would give the count without materialising. The refactor moved `expand_globals` from `__init__.py` to `expander.py`; logic unchanged.
- **Severity**: crash-data-loss (fills system memory, lab PC hard reset reported in #50)
- **Scope**: runmanager GUI preparse; also `RemoteServer.handle_n_shots`
- **Related**: #50 (startup re-guessing of expansions, the trigger), #60
- **Effort**: small (compute `n_shots` as the product of `dimensions.values()` in preparse; only materialise shots on engage)
- **Release relevance**: yes; a mis-set expansion can make runmanager unusable and take down the lab PC.
- **Rewrite relevance**: requirement: never materialise a parameter space to count it; shot count must be computed from axis lengths, and the GUI must survive a huge parameter space.
- **Importance**: 4
- **Recommended action**: fix for next release (the counting change); retitle to describe the cause.

### runmanager #62: Cascading sections for global variables (philipstarkey for Anonymous, opened 2019-02-20, last activity 2019-02-20, 0 comments)
- **Summary**: Nest globals groups in collapsible folders in the groups tab.
- **Type**: feature request
- **Still valid?**: n.a.
- **Scope**: GUI; would also change the HDF5 globals layout
- **Related**: #37 (favourites)
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: none (organisation of globals is a design choice for shotscript; note as a wish).
- **Importance**: 1
- **Recommended action**: close as won't fix.

### runmanager #60: Difference between API and GUI when handling zip groups (philipstarkey, opened 2018-06-19, last activity 2018-06-19, 0 comments)
- **Summary**: `guess_expansion_modes` (automatic zip-group detection) exists only in the GUI, so compiling via the library API from a globals file does not detect zip groups the way the GUI does.
- **Type**: bug
- **Still valid?**: yes. `guess_expansion_modes` is a `RunManager` method, `__main__.py:2793-2960`; the library path `compiler.make_run_file_from_globals_files` (`compiler.py:207-225`) reads expansions from the file as-is. The refactor did not move the guessing into the library, so the discrepancy is unchanged.
- **Severity**: wrong-behaviour
- **Scope**: library API vs GUI
- **Related**: #50, #66
- **Effort**: medium (requires separating guessing from GUI state in `self.previous_*`)
- **Release relevance**: no
- **Rewrite relevance**: requirement: expansion settings must be explicit data in the globals store; no guessing in either GUI or API, so the two cannot differ.
- **Importance**: 2
- **Recommended action**: leave open (document that the API uses stored expansions verbatim).

### runmanager #54: runmanager doesn't cache the labscript file when compiling shots (philipstarkey, opened 2018-03-13, last activity 2018-03-27, 3 comments)
- **Summary**: Each shot re-reads the labscript file from disk, so editing it mid-sequence produces a sequence compiled from two versions. Archived comments: cache the file in memory and hold the ModuleWatcher in a warning mode across the sequence; accepted as a minor limitation that conditionally imported modules cannot be covered.
- **Type**: bug
- **Still valid?**: yes. `batch_compiler.py:70-74` opens and compiles the file for every shot; `module_watcher.lock` is held per shot only (`batch_compiler.py:68`); `compile_loop` (`__main__.py:2733-2772`) sends `['compile', [labscript_file, run_file]]` per shot with no sequence start/end message. Not moved by the refactor.
- **Severity**: wrong-behaviour (silent mixed-version sequence; mitigated by labscript saving the actual script text into each shot file)
- **Scope**: batch compiler protocol
- **Related**: #53, #28 (ModuleWatcher); #47
- **Effort**: medium (protocol change: begin/end sequence messages; cache code object; ModuleWatcher warning mode)
- **Release relevance**: no
- **Rewrite relevance**: requirement: a sequence must compile from one snapshot of the script and its imports.
- **Importance**: 2
- **Recommended action**: fix later.

### runmanager #53: ModuleWatcher notices changes to runmanager module (philipstarkey, opened 2018-03-13, last activity 2018-03-14, 2 comments)
- **Summary**: Updating runmanager while it ran made the batch compiler's ModuleWatcher reload `runmanager/__init__.py`. Comments: author could not reproduce.
- **Type**: bug
- **Still valid?**: obsolete. `batch_compiler.py` no longer imports `runmanager` at all (imports: `labscript_utils.ls_zprocess`, `labscript`, `labscript_utils.modulewatcher`, lines 14-30), and `ModuleWatcher` whitelists everything imported before its instantiation (`batch_compiler.py:90`; `labscript_utils/modulewatcher.py:49`) plus everything under site-packages (`modulewatcher.py:23-31, 83-86`). The refactor did not touch `batch_compiler.py`.
- **Severity**: n.a.
- **Scope**: batch compiler
- **Related**: #28
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot (no in-process hot reloading planned in shotscript's compile worker, or it is a fresh design).
- **Importance**: 1
- **Recommended action**: close as fixed/obsolete.

### runmanager #52: Global checkbox for active groups doesn't update after group deletion (philipstarkey, opened 2018-01-17, last activity 2018-01-17, 0 comments)
- **Summary**: Deleting the only inactive group leaves the file-level "active" checkbox in the partial state.
- **Type**: bug
- **Still valid?**: yes. `delete_group`, `__main__.py:2478-2489`, removes the row and calls `globals_changed()` but never recomputes the parent check state; that only happens in `on_groups_model_active_changed` (`__main__.py:1877-1931`) on a child check-state change. Not moved by the refactor.
- **Severity**: cosmetic
- **Scope**: GUI groups tab
- **Related**: none
- **Effort**: trivial (after `removeRow`, re-run the parent-state block, or call the handler on any remaining child's active item)
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: fix later (or bundle with other trivial GUI fixes).

### runmanager #50: Bugs with restoring expansion type when runmanager is reopened (philipstarkey, opened 2017-09-11, last activity 2018-03-13, 6 comments)
- **Summary**: Two manual expansion settings are reverted on restart: an "outer" global cleared to "" reverts to "outer", and a zip group changed to "outer" reverts to the zip group. Comments add the memory-crash consequence (8 lists of 20 → 20^8 shots, see #66) and the `tuple()` workaround, and suggest not re-guessing on startup.
- **Type**: bug
- **Still valid?**: yes, by code reading of `guess_expansion_modes` (`__main__.py:2838-2866, 2928-2938`). Case 1: on first load with expansion "", `previous_value = 0` → `previous_guess ''`, `new_guess 'outer'` → written as `outer`. Case 2: with expansion "outer", `set_expansion_type_guess` (`__main__.py:2893-2912`) treats `'outer'` like "" and overwrites it with the zip key when the global has dependents. Not moved by the refactor.
- **Severity**: wrong-behaviour (and triggers #66)
- **Scope**: GUI preparse
- **Related**: #66, #60; docs already say tuples are not expanded (`docs/source/usage.rst:166`)
- **Effort**: medium for a full fix; small for the mitigation (on the first preparse after opening a group, read expansions from the file and do not guess)
- **Release relevance**: no on its own; the crash consequence is covered by #66.
- **Rewrite relevance**: requirement: expansion type is user data stored with the global and never silently rewritten; type-based guessing only as an explicit user action.
- **Importance**: 3
- **Recommended action**: fix later (mitigation together with #66 if time allows).

### runmanager #48: Continuous Engage (philipstarkey for Kevin Cox, opened 2017-08-17, last activity 2017-08-25, 5 comments)
- **Summary**: A mode that re-engages every X seconds, ideally paced by BLACS finishing. Comments: maintainer planned a BLACS-driven compile queue instead; JQI posted a QTimer patch.
- **Type**: feature request
- **Still valid?**: n.a. (not implemented; `remote.engage()` allows an external script to do it)
- **Scope**: runmanager/BLACS interaction
- **Related**: #45, #47, #97; PR #104 + blacs #90 (compile queue, recommended to close as superseded and convert requirements to an issue)
- **Effort**: large (queue redesign) / trivial (QTimer hack)
- **Release relevance**: no
- **Rewrite relevance**: requirement: just-in-time compilation driven by the executor's queue, with per-engage choice of locked vs live globals (see PR #104 discussion).
- **Importance**: 2
- **Recommended action**: leave open as the collection point for the compile-queue requirements, or close in favour of the new issue proposed in PR-REVIEW.md.

### runmanager #47: Move file creation to compile loop (philipstarkey for PhyNerd, opened 2017-08-09, last activity 2021-05-24, 8 comments)
- **Summary**: Create shot files lazily inside the compile loop so an abort leaves only compiled shots on disk. Comments turned into the compile-queue / JIT-globals design discussion.
- **Type**: proposal
- **Still valid?**: fixed, in effect since d65adb4 (2012): `compiler.make_run_files` is a generator (`compiler.py:131-167`) and `compile_loop` creates files one at a time with `next()` (`__main__.py:2740-2748`). After an abort only the already-compiled shots plus the one that failed exist. The reporter's lab probably ran a modified runmanager. Moved by the refactor from `__init__.py` to `compiler.py`, unchanged.
- **Severity**: n.a.
- **Scope**: compile loop
- **Related**: #48, #45, #33, PR #104. zakv (2021-05-24) already verified the lazy behaviour by aborting a compilation and checking the output folder, and proposed closing this and opening a separate issue for "just in time" vs "as submitted" globals.
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot (shotscript design already defers shot-file creation to compile time; the JIT-globals discussion is covered under #48).
- **Importance**: 1
- **Recommended action**: close as fixed; point to the compile-queue issue for the remaining discussion.

### runmanager #46: Engage Log (philipstarkey for PhyNerd, opened 2017-08-04, last activity 2017-08-04, 5 comments)
- **Summary**: A per-engage log (timestamp, script, output folder, shot count; optionally globals diff) to find old sequences.
- **Type**: feature request
- **Still valid?**: n.a. (`on_engage_clicked` only logs "Engage" to the application log, `__main__.py:1318`)
- **Scope**: runmanager
- **Related**: `globals_diff` tooling (`differ.py`) could supply the diff
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: requirement: a sequence index/log is part of the shot-storage design.
- **Importance**: 2
- **Recommended action**: leave open.

### runmanager #45: Compilation progress and abort (philipstarkey for PhyNerd, opened 2017-08-04, last activity 2017-08-04, 2 comments)
- **Summary**: Show compile progress and allow aborting any queued sequence, not just the current one. Comments establish that multiple engages are queued in mainline.
- **Type**: feature request
- **Still valid?**: n.a. (no progress display; abort behaviour is #33)
- **Scope**: GUI
- **Related**: #33 (duplicate for the abort part), PR #104
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: requirement: queue visible to the user, per-sequence cancel.
- **Importance**: 3
- **Recommended action**: fix later; merge abort part into #33.

### runmanager #44: changing values with arrow keys (philipstarkey for PhyNerd, opened 2017-08-04, last activity 2017-08-05, 1 comment)
- **Summary**: Up/down arrows change a numeric global by a step; left/right change the step.
- **Type**: proposal
- **Still valid?**: n.a. (`widgets.py` `Editor`/`ItemDelegate` have no such key handling)
- **Scope**: GUI editing
- **Related**: #48 (same lab's quick-iteration workflow)
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: close as won't fix unless someone contributes it.

### runmanager #41: Saving and restoration of window size & location (philipstarkey for shjohnst, opened 2017-06-19, last activity 2017-06-19, 1 comment)
- **Summary**: Remember window geometry and the popped-out state of the output box between runs.
- **Type**: feature request
- **Still valid?**: n.a. (confirmed absent: `get_save_data`, `__main__.py:2533-2593`, saves no geometry; no `saveGeometry`/`restoreGeometry` anywhere)
- **Scope**: GUI; BLACS and lyse do save geometry, so this is a runmanager gap
- **Related**: none
- **Effort**: small (store `saveGeometry()` bytes and `output_box_is_popped_out` in the config)
- **Release relevance**: no
- **Rewrite relevance**: requirement (GUI state persistence).
- **Importance**: 3
- **Recommended action**: fix for next release if time allows; otherwise fix later.

### runmanager #125: Add a history for each variable and a comment box about a variable in Runmanager (philipstarkey for ispielma, opened 2017-04-21, last activity 2026-01-26, 0 comments)
- **Summary**: Title only; body empty (migrated from labscript #24 in 2026).
- **Type**: feature request
- **Still valid?**: n.a.
- **Scope**: GUI
- **Related**: #46 (log), comments already live inside expressions
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: none (globals history is available from shot files).
- **Importance**: 1
- **Recommended action**: close as stale (no description).

### runmanager #126: #22: In run managed have "default" case for all the variables (philipstarkey for ispielma, opened 2017-04-21, last activity 2026-01-26, 1 comment)
- **Summary**: A default value per global used when "a ramp is not running". One sentence; the comment on the archive is empty.
- **Type**: feature request
- **Still valid?**: n.a.
- **Scope**: unclear
- **Related**: none
- **Effort**: unclear
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: ask reporter for a description, else close.

### runmanager #37: Ability to "star" or favourite globals (philipstarkey, opened 2016-09-07, last activity 2016-09-07, 0 comments)
- **Summary**: A tab showing starred globals from across groups.
- **Type**: feature request
- **Still valid?**: n.a.
- **Scope**: GUI
- **Related**: #62
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: none (GUI wish; record for a shotscript GUI backlog).
- **Importance**: 2
- **Recommended action**: leave open.

### runmanager #35: Asynchronous compilation functions should handle exceptions gracefully (philipstarkey, opened 2015-09-21, last activity 2015-09-21, 0 comments)
- **Summary**: `compile_labscript_async` and friends must call `done_callback(False)` if the worker process dies, so callers (BLACS connection-table compile) do not wait forever.
- **Type**: bug
- **Still valid?**: yes. `compiler.py:258` and `compiler.py:303` block on `from_child.get()` with no timeout and no check that `child` is alive; if the batch compiler process dies the callback is never called. `compile_multishot_async` only catches exceptions raised in the parent (`compiler.py:311-316`). Moved by the refactor from `__init__.py` to `compiler.py`, unchanged.
- **Severity**: wrong-behaviour (hang in BLACS connection-table recompile)
- **Scope**: library API; affects BLACS
- **Related**: blacs #12 (referenced)
- **Effort**: small (poll `child.poll()` with a timeout loop, or use zprocess's process-death detection; call `done_callback(False)`)
- **Release relevance**: no (rare)
- **Rewrite relevance**: requirement: compile worker failure must surface as an error result, never a hang.
- **Importance**: 3
- **Recommended action**: fix later.

### runmanager #34: Globals tabs can be relocated before the fixed tabs (philipstarkey, opened 2015-08-06, last activity 2015-08-06, 0 comments)
- **Summary**: The first three tabs are meant to be fixed, but a group tab can be dropped before them, after which the wrong tabs are fixed.
- **Type**: bug
- **Still valid?**: yes. `FingerTabBarWidget.setMovable(movable, index)` stores fixedness by index (`widgets.py:116-124`), checked only in `mousePressEvent` (`widgets.py:146-149`); nothing prevents dropping a movable tab at index < 3 and there is no `tabMoved` handler. Moved by the refactor from `__main__.py` to `widgets.py`, unchanged.
- **Severity**: annoyance
- **Scope**: GUI
- **Related**: #2
- **Effort**: small (connect `tabMoved` and move the tab back if `to < 3`, or override `mouseMoveEvent` to clamp)
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: fix later.

### runmanager #33: Abort button only stops current sequence of shots (philipstarkey for shjohnst, opened 2015-05-25, last activity 2021-05-23, 2 comments)
- **Summary**: Abort cancels the sequence being compiled; already-queued engages then compile with the abort button disabled.
- **Type**: bug
- **Still valid?**: yes. `compile_loop`, `__main__.py:2733-2772`: on abort the inner loop breaks, the abort button is disabled and `compilation_aborted` is cleared, then the outer loop takes the next queued item. Not moved by the refactor.
- **Severity**: wrong-behaviour
- **Scope**: compile loop
- **Related**: #45 (duplicate for the abort part), #47 discussion, PR #104
- **Effort**: trivial for the simple semantics (drain `compile_queue` on abort, and only disable the abort button when the queue is empty); medium for per-sequence cancel
- **Release relevance**: yes; cheap fix for behaviour users hit when queuing overnight sequences.
- **Rewrite relevance**: requirement: abort semantics must be defined (cancel all pending by default).
- **Importance**: 3
- **Recommended action**: fix for next release (simple semantics: abort cancels everything queued).

### runmanager #32: Output box scrolling issues (philipstarkey for shjohnst, opened 2015-01-23, last activity 2015-01-23, 0 comments)
- **Summary**: The output box sometimes shows blank space at the bottom after switching tabs.
- **Type**: bug
- **Still valid?**: cannot verify. `OutputBox` has since moved to qtutils (`qtutils/outputbox.py`, auto-scroll via `set_auto_scroll_to_end`), rewritten after this report. No reproduction steps.
- **Severity**: cosmetic
- **Scope**: qtutils OutputBox
- **Related**: none
- **Effort**: unknown
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as stale (reopen in qtutils if it recurs).

### runmanager #30: Output of multiple compilations not easily distinguishable (philipstarkey for chrisjbillington, opened 2014-10-04, last activity 2014-10-04, 0 comments)
- **Summary**: Print a visible header with the shot filename before each compilation.
- **Type**: bug (usability)
- **Still valid?**: yes. `compile_loop` writes nothing before `to_child.put(['compile', ...])` (`__main__.py:2749`); the only per-shot line is "Submitting run file" after success (`__main__.py:2987`). `batch_compiler.compile` prints nothing either. Not moved by the refactor.
- **Severity**: annoyance
- **Scope**: output box
- **Related**: #46
- **Effort**: trivial (one `output_box.output(...)` line)
- **Release relevance**: yes (trivial, improves error diagnosis).
- **Rewrite relevance**: requirement: per-shot compile output must be delimited.
- **Importance**: 3
- **Recommended action**: fix for next release.

### runmanager #28: Batch compiler does not notice changes to unit conversions (philipstarkey for chrisjbillington, opened 2014-10-03, last activity 2014-10-03, 0 comments)
- **Summary**: `labscript` does `from labscript_utils.unitconversions import *`, so all unit-conversion modules are imported before the ModuleWatcher starts and are whitelisted; edits and new unit conversion files are not picked up until restart.
- **Type**: bug
- **Still valid?**: yes, for editable installs. `labscript/labscript/labscript.py:53` still imports `*`; `unitconversions/__init__.py` `_All.__getitem__` imports every module in the package on `import *`; `batch_compiler.py:29` imports labscript before `ModuleWatcher()` at line 90, so all of them are whitelisted (`modulewatcher.py:49`). For non-editable installs everything under site-packages is whitelisted anyway (`modulewatcher.py:83-86`), so the issue is limited to developers editing `labscript_utils/unitconversions/`. The "Restart subprocess" button is a workaround. Not moved by the refactor.
- **Severity**: annoyance
- **Scope**: labscript + batch compiler; editable installs only
- **Related**: #53, #54
- **Effort**: small (drop the `import *` in labscript; devices needing a default conversion import it by name)
- **Release relevance**: no
- **Rewrite relevance**: moot (shotscript has no in-process hot reload of unit conversions; unit conversions are an explicit import).
- **Importance**: 2
- **Recommended action**: fix later (remove the star import in labscript).

### runmanager #27: More standard saving and loading of globals from h5 files, file changed on disk detection (philipstarkey for chrisjbillington, opened 2014-10-03, last activity 2014-10-08, 1 comment)
- **Summary**: Edit globals in a temporary copy, save explicitly, "save as", and detect external changes to the file.
- **Type**: feature request
- **Still valid?**: n.a. (runmanager still writes on every cell edit, `GroupTab.change_global_value` → `group_manager.set_value`; no `FileWatcher` in runmanager)
- **Scope**: globals storage model
- **Related**: #46
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement to decide: shotscript's globals store should have explicit save/revert semantics or document that edits are immediate; external-change detection is needed if files are shared.
- **Importance**: 2
- **Recommended action**: leave open as a design note; not for the legacy release.

### runmanager #26: New globals file creation does not automatically append .h5 to filename (philipstarkey for chrisjbillington, opened 2014-10-03, last activity 2017-09-09, 1 comment)
- **Summary**: Creating a globals file without typing `.h5` yields a file without extension. Comment (2017): on macOS the native dialog appends it.
- **Type**: bug
- **Still valid?**: yes, platform-specific. `on_new_globals_file_clicked`, `__main__.py:1684-1702`: static `QFileDialog.getSaveFileName` with a filter; no `setDefaultSuffix` (not available on the static call) and no manual append. Native dialogs on macOS/Windows usually append the filter extension; the Qt dialog on Linux does not. Not moved by the refactor.
- **Severity**: annoyance
- **Scope**: GUI; Linux (non-native dialog)
- **Related**: none
- **Effort**: trivial (`if not globals_file.endswith('.h5'): globals_file += '.h5'`)
- **Release relevance**: yes (trivial).
- **Rewrite relevance**: none
- **Importance**: 3
- **Recommended action**: fix for next release.

### runmanager #23: Cursor going to end of entry when clicked for editing vs highlighting the entry (philipstarkey for shjohnst, opened 2014-10-03, last activity 2014-10-03, 2 comments)
- **Summary**: When editing starts, the text is selected with the cursor at the end, so Left moves to the second-last character instead of the start. Users keep comments at the end and edit the start.
- **Type**: bug
- **Still valid?**: yes. `ItemDelegate.setEditorData`, `widgets.py:617-628`, calls `editor.selectAll()` on a `QTextEdit`, which puts the cursor at the end. Moved by the refactor from `__main__.py` to `widgets.py`, unchanged.
- **Severity**: cosmetic
- **Scope**: GUI editing
- **Related**: none
- **Effort**: trivial (build a `QTextCursor` with anchor at end and position at start, `editor.setTextCursor(cursor)`)
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: fix later (bundle with #52, #26).

### runmanager #13: Globals files without units or expansion entry in h5 file raise exceptions (philipstarkey, opened 2014-09-17, last activity 2014-09-17, 4 comments)
- **Summary**: A global missing its `units`/`expansion` attribute makes opening the group raise and leaves a tab that cannot be closed. Comments agreed the fix is GUI robustness (consistent state on any error), not per-case file repair.
- **Type**: bug
- **Still valid?**: yes. `group_manager.get_globals`, `group_manager.py:328-329`, raises `KeyError` on a missing units/expansion attribute (`add_expansion_groups` only handles a missing `expansion` subgroup, `group_manager.py:85-113`). `GroupTab.__init__` adds the tab (`__main__.py:171`) before `populate_model` (`__main__.py:206`), and `open_group` (`__main__.py:2432-2447`) only registers the tab after construction, so an exception leaves an orphan tab that `on_tabCloseRequested` cannot close. `get_globals` moved to `group_manager.py` by the refactor, unchanged.
- **Severity**: annoyance (requires restart; only with corrupt/hand-edited files)
- **Scope**: GUI + library
- **Related**: none
- **Effort**: small (use `units.get(name, '')`, and wrap `GroupTab` construction so the tab is removed on failure)
- **Release relevance**: no
- **Rewrite relevance**: requirement: globals store must validate/normalise on read; GUI must not be left inconsistent by a load error.
- **Importance**: 2
- **Recommended action**: fix later.

### runmanager #2: paintEvent method of FingerTabBar is not implemented fully (philipstarkey, opened 2014-09-16, last activity 2014-09-17, 1 comment)
- **Summary**: Tabs do not render correctly while being dragged because the custom vertical tab bar's `paintEvent` is rudimentary.
- **Type**: bug
- **Still valid?**: yes. `FingerTabBarWidget.paintEvent`, `widgets.py:166-192`, draws shape, icon and text per tab with no handling of the drag state. A copy also exists in `labscript_utils/qtwidgets/fingertab.py`. Moved by the refactor to `widgets.py`, unchanged.
- **Severity**: cosmetic
- **Scope**: GUI
- **Related**: #34
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as won't fix.

---

### labscript-suite

### labscript-suite #105: uv compatibility (Json-To-String, opened 2026-01-26, last activity 2026-03-10, 2 comments)
- **Summary**: `uv pip` works as a drop-in; the reporter shows a `uv` workspace `pyproject.toml` placed alongside clones of the seven repos and asks whether this could be integrated into the meta-package. Follow-up (2026-02-09): proposes a `labscript_suite/` source directory (with `.venv`, the seven clones and the uv workspace `pyproject.toml`) inside the profile directory, separate from `labconfig/`, `userlib/` etc., so reinstalls do not disturb user data; docs builds with this layout untested; later retested with uv 0.10.9.
- **Type**: tooling / docs
- **Still valid?**: n.a. (nothing in `labscript-suite/pyproject.toml` or `docs/source/installation/` mentions uv)
- **Scope**: installation docs, meta-package
- **Related**: #45 (environment recommendations), #59/#58 (developer install docs)
- **Effort**: small (a "developer install with uv" docs page with the reporter's `pyproject.toml`; the meta-package repo itself does not contain the component repos so a workspace cannot live in it)
- **Release relevance**: yes, partially: the release should bump `requires-python` (currently `>=3.8` in `labscript-suite/pyproject.toml:27` and `runmanager/pyproject.toml:27`) and the component pins (`blacs>=3.2.3` etc.) regardless; a uv page is a cheap docs addition.
- **Rewrite relevance**: requirement: shotscript's monorepo should install with uv out of the box.
- **Importance**: 3
- **Recommended action**: convert to docs (uv developer-install page); ask reporter to contribute the page.

### labscript-suite #98: Feature idea: Goggle Mode (Json-To-String, opened 2025-06-30, last activity 2025-06-30, 0 comments)
- **Summary**: Colour themes tuned for viewing through laser safety goggles.
- **Type**: feature request
- **Still valid?**: n.a. (runmanager follows the OS theme since PR #124/#127; no custom palettes)
- **Scope**: all GUIs (qtutils theming)
- **Related**: runmanager PR #124 (OS theming)
- **Effort**: medium
- **Release relevance**: no
- **Rewrite relevance**: none (note for a shotscript GUI theme system).
- **Importance**: 1
- **Recommended action**: leave open or close as won't fix; realistic path is an OS-level high-contrast theme.

### labscript-suite #66: Double error when compiling runmanager labscript file (manuelmorgado, opened 2022-01-28, last activity 2022-01-28, 4 comments)
- **Summary**: On Ubuntu without `hg`, `_run_vcs_commands` raised `FileNotFoundError`, then `save_labscripts` raised `TypeError` from `except WindowsError if os.name == 'nt' else None`.
- **Type**: bug
- **Still valid?**: fixed: labscript 427b2bf (2022-01-29, "Better catch when vcs programs not installed"), released in labscript v3.3.0. Current code: `_have_vcs()` guard at `labscript/labscript/labscript.py:303-312`, and no `WindowsError` remains.
- **Severity**: wrong-behaviour (was)
- **Scope**: labscript; Linux/macOS without hg
- **Related**: none
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as fixed.

### labscript-suite #60: Add `CITATION.cff` file to GitHub repos (philipstarkey, opened 2021-08-21, last activity 2021-08-21, 1 comment)
- **Summary**: Add GitHub citation metadata to all repositories.
- **Type**: docs / meta
- **Still valid?**: partially done: `labscript-suite/CITATION.cff` exists (dihm offered in 2021 to add it alongside configuration docs); none of labscript, runmanager, blacs, lyse, runviewer, labscript-devices, labscript-utils has one.
- **Scope**: all repos
- **Related**: #20
- **Effort**: trivial (copy with per-repo title)
- **Release relevance**: yes (cheap, release is when repos get touched).
- **Rewrite relevance**: requirement: shotscript repo should ship a CITATION.cff.
- **Importance**: 3
- **Recommended action**: fix for next release.

### labscript-suite #59: Anaconda Cloud Developer Installation requires git (dihm, opened 2021-04-16, last activity 2021-04-19, 4 comments)
- **Summary**: `setuptools-conda install-requirements` fails with "git was not found" because setuptools_scm needs git inside the labscript conda env. Reporter closed it (he had skipped the clone step), chrisjbillington reopened it asking for a docs note that `git` must be on the command line and can be installed with `conda install git`; dihm added that the docs clone in `base` but build in the `labscript` env, so git must be system-wide or installed into that env.
- **Type**: docs
- **Still valid?**: yes: `docs/source/installation/developer-anaconda.rst:40` is `conda install setuptools-conda "pyqt<6" pip desktop-app`, no `git`, and no note about git being required in the env.
- **Scope**: developer conda install docs; Windows mostly
- **Related**: #58, #105
- **Effort**: trivial
- **Release relevance**: yes if the conda developer path is kept in the docs for the release.
- **Rewrite relevance**: moot (no conda in shotscript).
- **Importance**: 2
- **Recommended action**: fix for next release (one-word docs change), or drop the conda developer page.

### labscript-suite #58: Anaconda Cloud Developer Install: missing module 'packaging' (dsbarker, opened 2020-12-22, last activity 2020-12-31, 2 comments)
- **Summary**: After the developer conda install, `lyse` failed with `No module named 'packaging'` because `pip install --no-deps` skips it. philipstarkey asked whether `setuptools-conda install-requirements ...` had been run (it should install `packaging`, then a new labscript-utils dependency); reporter confirmed it had. No further follow-up.
- **Type**: docs / tooling
- **Still valid?**: cannot verify. The docs instruct `setuptools-conda install-requirements <repos>` before the `--no-deps` pip step (`developer-anaconda.rst:41-42`) and `packaging>=20.4` is declared in `labscript-utils/pyproject.toml:36`, so the dependency should be picked up today; why it was not in Dec 2020 (possibly a setuptools-conda bug with a newly added dependency, or a stale clone) was never established and there have been no further reports in five years.
- **Scope**: developer conda install docs; setuptools-conda
- **Related**: #59
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as stale (not reproducible, no follow-up since 2020).

### labscript-suite #56: GitHub Actions: Our release script cannot handle multiple tags on the same commit (philipstarkey, opened 2020-11-04, last activity 2020-11-04, 0 comments)
- **Summary**: Tagging the same commit `vX.Y.ZrcN` and then `vX.Y.Z` rebuilds the rc version; workaround is deleting the rc tag first.
- **Type**: tooling
- **Still valid?**: yes. `.github/workflows/release.yml:41-43` deletes tags at HEAD only for non-tag pushes; for a tag push `PKGVER` comes from `ci-helper distinfo version .` (line 87), i.e. setuptools_scm's `git describe` on a commit carrying both tags, which does not depend on which tag triggered the run. The GitHub release step uses `github.event.ref` for the tag but `PKGVER` for the name (lines 312-313), so they can disagree.
- **Severity**: wrong-behaviour (release process)
- **Scope**: release workflow in every repo (same template)
- **Related**: none
- **Effort**: trivial (for tag pushes, delete every tag at HEAD except `$GITHUB_REF_NAME` before computing the version; propagate to all repos)
- **Release relevance**: yes; this is exactly the rc → final flow the upcoming release will use.
- **Rewrite relevance**: requirement: shotscript's release workflow must derive the version from the pushed tag.
- **Importance**: 4
- **Recommended action**: fix for next release.
- **Status (2026-10-17)**: fixed by rpanderson/workflow-sandbox PR #46, deployed as a sync PR in each of the twelve repos, all merged 2026-10-17 (`PULL-REQUESTS.md`).

### labscript-suite #54: Consider move to more mature 3rd party RPC protocol (philipstarkey, opened 2020-10-14, last activity 2020-10-14, 0 comments)
- **Summary**: Proposal to replace the home-grown ZMQ RPC between components with gRPC or similar, keeping ZMQ for high-throughput paths.
- **Type**: proposal
- **Still valid?**: n.a. (components still use `labscript_utils.ls_zprocess.ZMQServer`, e.g. `blacs/blacs/__main__.py:732`, `runmanager/__main__.py:3036`)
- **Scope**: inter-component RPC
- **Related**: runmanager #97, labscript-suite #103
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement to decide: shotscript's inter-process protocol should be versioned and documented; this issue is the record of the arguments.
- **Importance**: 1 (for legacy)
- **Recommended action**: close as won't fix for the legacy suite; note in the rewrite design.

### labscript-suite #45: Consider not recommending use of virtual environments for daily use (chrisjbillington, opened 2020-06-06, last activity 2020-06-09, 4 comments)
- **Summary**: Argument that the quick-start should recommend the base/system environment, with venvs only for development. philipstarkey and rpanderson both argued against (installing into base can break a user's other Python work; multi-host installs; VS Code handles envs well); no consensus for the change was reached.
- **Type**: docs / proposal
- **Still valid?**: n.a. The docs went the other way: `docs/source/installation/setting-up-an-environment.rst:4-24` recommend a venv/conda env and advise against `base`. Since then PEP 668 (Python 3.11+ distro builds) blocks `pip install` into system Python, so the proposal is no longer practical.
- **Scope**: installation docs
- **Related**: #105
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot (uv-managed environments).
- **Importance**: 1
- **Recommended action**: close as won't fix (superseded by current docs and PEP 668).

### labscript-suite #26: Correct copyright assignments (philipstarkey for chrisjbillington, opened 2018-05-29, last activity 2020-06-25, 1 comment)
- **Summary**: File headers assign copyright to Monash University; contributors retain copyright for non-trivial contributions, so headers should name contributors or defer to a per-repo list. Author's 2020 follow-up: use "Monash University and contributors" in headers and let `git blame` answer who owns what.
- **Type**: meta / task
- **Still valid?**: n.a. (headers still read "Copyright 2013, Monash University", e.g. `runmanager/batch_compiler.py:5`)
- **Scope**: all repos
- **Related**: #60
- **Effort**: trivial (search-and-replace of the header line per repo, per the 2020 decision)
- **Release relevance**: no
- **Rewrite relevance**: requirement: shotscript should start with correct attribution (SPDX header + contributors file).
- **Importance**: 2
- **Recommended action**: fix for next release if the repos are being touched anyway (header text change), otherwise fix later.

### labscript-suite #23: End-to-end test (philipstarkey for chrisjbillington, opened 2018-05-29, last activity 2025-07-31, 3 comments)
- **Summary**: An automated install-and-run test with dummy devices. 2025 update (Json-To-String with dihm): pytest judged ill-fitting while component logic lives in `__main__.py`; their plan is a VM, a scripted install, GUI automation (pyautogui/AutoHotkey or pytest-qt) and Python checks of the produced h5 files. They said they would proceed with this.
- **Type**: tooling
- **Still valid?**: n.a. (no test suite exists in any component except zprocess; `blacs/tests` holds a single h5 fixture)
- **Scope**: whole suite
- **Related**: #21; runmanager PR #130 (module split) removes part of the `__main__.py` obstacle they named
- **Effort**: large for legacy; community work in progress
- **Release relevance**: no (but a manual end-to-end check with DummyPseudoclock should be part of the release checklist, and the 2025 plan could be asked for as a release smoke test)
- **Rewrite relevance**: requirement: shotscript already follows "few, end-to-end tests"; this is the legacy statement of that requirement.
- **Importance**: 3
- **Recommended action**: leave open; ask Json-To-String/dihm for status and point them at the runmanager module split.

### labscript-suite #22: Remove dead code (philipstarkey for chrisjbillington, opened 2018-05-29, last activity 2018-05-29, 0 comments)
- **Summary**: Remove old GTK code and misplaced hardware drivers.
- **Type**: task
- **Still valid?**: mostly done: remaining "GTK" hits are comments and one legacy-restore branch (`labscript-utils/labscript_utils/settings.py:116`, `blacs/blacs/front_panel_settings.py:112`, `blacs/blacs/tab_base_classes.py:1087`, `blacs/blacs/plugins/general/__init__.py:70`). runmanager PR #130 removed its unreachable code.
- **Scope**: all repos
- **Related**: #21
- **Effort**: small
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as fixed.

### labscript-suite #21: Per-project repository rough edges (philipstarkey for chrisjbillington, opened 2018-05-29, last activity 2020-06-25, 2 comments)
- **Summary**: Maintain a checklist of what every component repo must have (version, README, docs skeleton, pip-installability, tests, CI, contributing guide, changelog).
- **Type**: task
- **Still valid?**: n.a. rpanderson's 2020-06-25 checklist marks done: versioning, README, pip/conda installability, Sphinx docs, CI release workflow, suite-level docs link, contributing guidelines. Still open: changelog/release notes with contributors, coverage, test suites. Nothing has changed since; no checklist document exists in `docs/source/project/`.
- **Scope**: all repos
- **Related**: #60, #23, #22
- **Effort**: small (write the checklist into `docs/source/project/contributing.rst`)
- **Release relevance**: partially: release notes per component are one of the open items and the next release needs them.
- **Rewrite relevance**: none (single repo)
- **Importance**: 1
- **Recommended action**: convert to docs (checklist in contributing guide) or close; track the remaining items under #23 and the release notes under the release plan.

### labscript-suite #20: Add post-install message requesting cites and contribution (philipstarkey for chrisjbillington, opened 2018-05-29, last activity 2018-05-29, 0 comments)
- **Summary**: Remind users to cite the paper and contribute, via a post-install message or about dialogs.
- **Type**: feature request
- **Still valid?**: n.a. (pip has no post-install hooks for wheels; the citation request lives in `docs/source/main.md:26` and `CITATION.cff`)
- **Scope**: packaging / docs
- **Related**: #60
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as won't fix (covered by docs and CITATION.cff).

### labscript-suite #18: Install wrapper for pip (philipstarkey for chrisjbillington, opened 2018-04-23, last activity 2018-04-23, 0 comments)
- **Summary**: Make components installable via pip by wrapping the old custom installer.
- **Type**: feature request
- **Still valid?**: obsolete: since the 3.0 release (2020) every component is a normal pip/conda package with a `labscript-profile-create` step.
- **Scope**: packaging
- **Related**: #103 (headless use, the other half of the mailing-list thread)
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as fixed.

### labscript-suite #103: #20: Ability to run directly from the console with ease (philipstarkey for ispielma, opened 2017-04-21, last activity 2026-01-26, 4 comments)
- **Summary**: GUIs should be clients of headless server processes so BLACS can run on a headless machine. Archived comments: start by making everything scriptable via remote APIs; multiple-client locking; Qt-free event loop for headless.
- **Type**: feature request / architecture
- **Still valid?**: n.a. Partially done: `runmanager.remote` (2019) and BLACS's `ExperimentServer`; lyse and runviewer have no remote API module; nothing runs headless.
- **Scope**: whole suite
- **Related**: #54 (RPC), runmanager #97
- **Effort**: large
- **Release relevance**: no
- **Rewrite relevance**: requirement: shotscript components should be scriptable without a GUI; GUI as a client is the stated design goal.
- **Importance**: 2
- **Recommended action**: close for the legacy suite with a pointer to the rewrite, or leave open as the architecture record.

### labscript-suite #104: #19: Remerge JQI with Monash. Then get ground rules down for proper behavior with rules (philipstarkey for ispielma, opened 2017-04-21, last activity 2026-01-26, 4 comments)
- **Summary**: Merge the JQI fork into mainline and document the feature-contribution process. Archived comments discuss BLACS plugin hooks for pre/post-shot actions.
- **Type**: task
- **Still valid?**: obsolete: the JQI/mainline convergence happened before the 2020 GitHub migration; the contribution process is in `docs/source/project/contributing.rst` and `contributing_guide.md`. The plugin-hook discussion is covered by BLACS's plugin system.
- **Scope**: project
- **Related**: blacs PR #123 (plugin loading)
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as fixed/obsolete.

### labscript-suite #7: Perhaps share our notepad++ python setup in the install instructions (philipstarkey for chrisjbillington, opened 2014-10-03, last activity 2014-10-03, 1 comment)
- **Summary**: Document an editor setup (run-on-keypress) for new Python users.
- **Type**: docs
- **Still valid?**: n.a. (no editor guidance anywhere in `docs/source`)
- **Scope**: docs
- **Related**: #6
- **Effort**: trivial
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 1
- **Recommended action**: close as stale (editor landscape has changed; a one-line "use any editor, e.g. VS Code" in #6 suffices).

### labscript-suite #6: Install docs should direct user to install a text editor and hdfview (philipstarkey for chrisjbillington, opened 2014-10-03, last activity 2014-10-03, 0 comments)
- **Summary**: Tell users to install an editor (tabs-to-spaces) and an HDF5 viewer, and how to set the editor/viewer in labconfig.
- **Type**: docs
- **Still valid?**: n.a. (`grep -ri hdfview` over `docs/source` finds nothing; `setup/configuration.rst` does not mention the `[programs]` labconfig keys for editor/hdf5 viewer)
- **Scope**: docs
- **Related**: #7, #5
- **Effort**: trivial
- **Release relevance**: no
- **Rewrite relevance**: none
- **Importance**: 2
- **Recommended action**: convert to docs (short paragraph in `setup/configuration.rst`).

### labscript-suite #5: Installation docs should say that the experiment name should be a valid python module name (philipstarkey for chrisjbillington, opened 2014-10-03, last activity 2014-10-03, 0 comments)
- **Summary**: The apparatus name becomes a `labscriptlib` subdirectory that must be importable.
- **Type**: docs (and a small tooling gap)
- **Still valid?**: yes. The docs do not say it, and `labscript-profile-create -n` accepts any string (`labscript-utils/labscript_profile/create.py:59-61, 110-112`) without an `isidentifier()` check.
- **Scope**: docs; `labscript_profile.create`
- **Related**: #6
- **Effort**: trivial (validate in `create.py` with a clear error, and one sentence in the docs)
- **Release relevance**: yes (trivial; first-run experience).
- **Rewrite relevance**: requirement: shotscript's profile/apparatus name must be validated as an identifier.
- **Importance**: 3
- **Recommended action**: fix for next release.

---

### mise

### mise #1: Port mise to Qt (philipstarkey for PhyNerd, opened 2017-07-03, last activity 2017-07-04, 1 comment)
- **Summary**: Asks why mise (closed-loop optimisation, GTK) is deprecated and offers to port it to Qt. Archived comment (Starkey): deprecated because it implemented one fixed optimisation protocol; the intended replacement is a lyse analysis script using lyse persistence and the runmanager remote API.
- **Type**: proposal
- **Still valid?**: n.a. (repo not cloned; judged from the issue text only). The replacement path exists since 2019 (`runmanager.remote`).
- **Scope**: mise (deprecated)
- **Related**: runmanager #97, #48
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: requirement: optimisation loops must be possible from analysis code via the shot-submission API; no separate optimiser application.
- **Importance**: 1
- **Recommended action**: close as won't fix; archive the repository if not already archived.

---

### bias

### bias #1: BIAS "CameraBase VI" documentation missing (philipstarkey, opened 2016-01-26, last activity 2016-01-26, 0 comments)
- **Summary**: The BIAS (LabVIEW camera server) PDF refers to CameraBase VI documentation that does not exist.
- **Type**: docs
- **Still valid?**: obsolete (repo not cloned; judged from the issue text only). BIAS has been superseded by the Python camera classes in labscript-devices (`IMAQdxCamera`, `PylonCamera`, etc.).
- **Scope**: bias (deprecated LabVIEW software)
- **Related**: labscript-devices PR #148 (TriggerableCamera)
- **Effort**: n.a.
- **Release relevance**: no
- **Rewrite relevance**: moot
- **Importance**: 1
- **Recommended action**: close as obsolete; archive the repository if not already archived.

---

### Ranked table

| Rank | Issue | Type | Importance | Action |
|---|---|---|---|---|
| 1 | runmanager #66 preparse memory blow-up counting shots | bug | 4 | fixed in runmanager #134 (merged 2026-10-18); issue closed |
| 2 | runmanager #123 set_globals comment preservation with raw=True | bug | 4 | fixed in runmanager #134 (merged 2026-10-18); the offered PR was not used; issue closed |
| 3 | labscript-suite #56 release workflow with rc + final tag on one commit | tooling | 4 | fixed 2026-10-17: workflow-sandbox #46 and the sync PR on each of the twelve repos merged; issue closed |
| 4 | runmanager #33 abort only stops current sequence | bug | 3 | fixed in runmanager #134 (merged 2026-10-18); issue closed |
| 5 | runmanager #30 no header between shot compilations | bug | 3 | fixed in runmanager #134 (merged 2026-10-18); issue closed |
| 6 | runmanager #26 .h5 not appended (Linux) | bug | 3 | fixed in runmanager #134 (merged 2026-10-18); issue closed |
| 7 | labscript-suite #5 apparatus name must be identifier | docs/tooling | 3 | fixed in labscript-utils #134 (validation in `labscript-profile-create`) and labscript-suite #109 (docs), both merged 2026-10-18; issue closed |
| 8 | labscript-suite #60 CITATION.cff in component repos | docs | 3 | leave open, not for this release (maintainer decision 2026-10-18) |
| 9 | runmanager #97 remote is_compiling | feature | 3 | fix for next release if cheap |
| 10 | runmanager #41 save window geometry | feature | 3 | fix later |
| 11 | runmanager #50 expansion types rewritten on restart | bug | 3 | fix later (mitigate with #66) |
| 12 | runmanager #35 async compile hangs if worker dies | bug | 3 | fix later |
| 13 | runmanager #45 compile progress / per-sequence abort | feature | 3 | fix later; merge abort part into #33 |
| 14 | labscript-suite #105 uv install docs | docs | 3 | convert to docs |
| 15 | labscript-suite #23 end-to-end test | tooling | 3 | leave open; ask Json-To-String/dihm for status |
| 16 | runmanager #60 API lacks zip-group guessing | bug | 2 | leave open |
| 17 | runmanager #54 labscript file not cached per sequence | bug | 2 | fix later |
| 18 | runmanager #52 file checkbox after group deletion | bug | 2 | fix later |
| 19 | runmanager #34 tabs can be moved before fixed tabs | bug | 2 | fix later |
| 20 | runmanager #23 cursor at end on edit | bug | 2 | fix later |
| 21 | runmanager #13 missing units attr leaves orphan tab | bug | 2 | fix later |
| 22 | runmanager #28 unit conversions whitelisted by ModuleWatcher | bug | 2 | fix later (labscript star import) |
| 23 | runmanager #48 continuous engage / compile queue | feature | 2 | leave open (or fold into new compile-queue issue) |
| 24 | runmanager #46 engage log | feature | 2 | leave open |
| 25 | runmanager #37 favourite globals | feature | 2 | leave open |
| 26 | runmanager #27 explicit save of globals | feature | 2 | leave open |
| 27 | runmanager #44 arrow-key value stepping | feature | 2 | close as won't fix |
| 28 | labscript-suite #59 add git to conda install line | docs | 2 | fixed in labscript-suite #109 (merged 2026-10-18); issue closed |
| 29 | labscript-suite #26 copyright headers | meta | 2 | fix for next release if cheap ("Monash University and contributors"), else later |
| 30 | labscript-suite #103 headless/scriptable components | feature | 2 | close for legacy, pointer to rewrite |
| 31 | labscript-suite #6 editor/hdfview in docs | docs | 2 | convert to docs |
| 32 | runmanager #47 lazy shot-file creation | proposal | 1 | close as fixed |
| 33 | runmanager #53 ModuleWatcher reloads runmanager | bug | 1 | close as obsolete |
| 34 | runmanager #32 output box scrolling | bug | 1 | close as stale |
| 35 | runmanager #2 FingerTabBar paintEvent | bug | 1 | close as won't fix |
| 36 | runmanager #62 nested group folders | feature | 1 | close as won't fix |
| 37 | runmanager #125 per-variable history (empty) | feature | 1 | close as stale |
| 38 | runmanager #126 default case for variables | feature | 1 | ask reporter, else close |
| 39 | labscript-suite #66 WindowsError/hg TypeError | bug | 1 | close as fixed (labscript v3.3.0) |
| 40 | labscript-suite #58 missing packaging | docs | 1 | close as stale |
| 41 | labscript-suite #45 don't recommend venvs | docs | 1 | close as won't fix |
| 42 | labscript-suite #54 third-party RPC | proposal | 1 | close for legacy; rewrite design note |
| 43 | labscript-suite #22 dead code | task | 1 | close as fixed |
| 44 | labscript-suite #21 per-repo checklist | task | 1 | convert to docs or close (release notes item goes to release plan) |
| 45 | labscript-suite #20 post-install cite message | feature | 1 | close as won't fix |
| 46 | labscript-suite #18 pip install wrapper | feature | 1 | close as fixed |
| 47 | labscript-suite #104 remerge JQI | task | 1 | close as obsolete |
| 48 | labscript-suite #7 notepad++ setup | docs | 1 | close as stale |
| 49 | labscript-suite #98 goggle mode | feature | 1 | leave open or close |
| 50 | mise #1 port mise to Qt | proposal | 1 | close as won't fix; archive repo |
| 51 | bias #1 CameraBase VI docs | docs | 1 | close as obsolete; archive repo |

### Release-relevant issues

- labscript-suite #56: release workflow must handle an rc tag and a final tag on the same commit; the upcoming rc → final flow hits it. Propagate the fix to every repo's `release.yml`.
- runmanager #66 (+ #50): preparse materialises the full parameter space to count shots; compute the count from axis lengths. Fixed in runmanager #134 (merged 2026-10-18).
- runmanager #123: `remote.set_globals(raw=True)` must not append comments; reporter offered a PR. Fixed in runmanager #134 (merged 2026-10-18).
- runmanager #33, #30, #26: trivial compile-loop/GUI fixes (drain queue on abort; header line per shot; append `.h5`). Fixed in runmanager #134 (merged 2026-10-18).
- labscript-suite #5: validate the apparatus name in `labscript-profile-create` and document it. Fixed in labscript-utils #134 and labscript-suite #109 (merged 2026-10-18).
- labscript-suite #60: add `CITATION.cff` to the component repos. Left open, not for this release (maintainer decision 2026-10-18).
- labscript-suite #59: add the agreed note that `git` must be available in the labscript env (`conda install git`), or drop that page. Fixed in labscript-suite #109 (merged 2026-10-18).
- labscript-suite #105 (indirect): bump `requires-python` (currently `>=3.8`) and the component version pins in the meta-package and runmanager `pyproject.toml` for the 3.11-3.15 release; optionally add a uv developer-install docs page.
