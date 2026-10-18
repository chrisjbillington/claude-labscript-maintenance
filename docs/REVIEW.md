# labscript suite review

Date: 2026-09-30

Fix status and current code locations after later refactors: see `MAINTENANCE.md`.

## Scope and method

Repos reviewed, with the commit that was read:

| Repo | Commit |
|---|---|
| `labscript` | a0787c4 |
| `blacs` | e5757c7 |
| `runmanager` | 08ccc99 |
| `runviewer` | 4989087 |
| `lyse` | ed0b6ca |
| `labscript-utils` | 22616a7 |
| `labscript-devices` | 424b9f4 |
| `labscript-c-extensions` | 4e440ac |
| `labscript-suite` | 0ab902d |
| `vendored-conda-builds` | 55f3cbf |

`PrawnBlaster` and `prawn_digital_output` (firmware) were cloned but not reviewed.

Each finding has one of these verification labels:

- **(run)**: reproduced by running code on Python 3.14, numpy 2.5, h5py 3.16, pandas 3.0 and
  PyQt6/PySide6 6.11.
- **(read)**: the code path and its callers were read, but nothing was executed.
- **(plausible)**: the code path was read, but the trigger or the consequence was not
  established.

No GUI was launched and no hardware was attached. PyQt5 behaviour was not run. The findings
in Part 1 were all checked a second time by reading the cited code. The findings in Part 2
were reported by the per-repo reviews and were not all checked a second time.

Paths are relative to each repo's root unless stated otherwise.

---

# Part 1: top findings and recommendations

## 1.1 The suite does not work on numpy 2.5

1. **Fixed upstream** by labscript PR #124, labscript-devices PR #149 and blacs PR #124, merged 2026-10-17.
   ~~**`'a256'` dtype strings (run).**~~ numpy 2.5 removed the `'a'` dtype alias, and no repo has
   an upper numpy bound. Replace with `'S256'` everywhere.
   - `labscript/labscript/labscript.py:216,268,477` and `labscript/outputs.py:1604`: every
     `stop()` raises `TypeError: data type 'a256' not understood`, so no shot compiles.
   - `blacs/blacs/front_panel_settings.py:348,387`: every shot fails at the front panel save
     and is re-queued, and the queue pauses. On exit, the saved front panel group is deleted
     before the error occurs, so all saved values are lost, and the window cannot then be
     closed.
   - `labscript-devices`: `NI_DAQmx/labscript_devices.py:514-520` (compile with any
     `AnalogIn`), `NI_DAQmx/blacs_workers.py:956` (wait monitor), `PrawnBlaster/blacs_workers.py:497`
     (wait results), `Camera.py:107`, `AlazarTechBoard.py:157-158`,
     `CiceroOpalKellyXEM3001.py:652`.
2. **Fixed** by labscript PR #129, opened 2026-10-18.
   ~~**`labscript/labscript/utils.py:210`: `bitfield()` passes `dtype=np.dtype` instead of
   `dtype=dtype` (run).**~~ Any NI digital port on which line 0 is unused, or a PrawnDO
   without `do0`, fails to compile with `TypeError: Cannot convert np.dtype into a dtype`.
   This is a regression from the 2024-01 refactor (6e43872). Lines 207 and 214 also index
   `n[dtype]` by the class `np.uint8` etc., so a `np.dtype` instance raises `KeyError`.

## 1.2 Wrong output with no error

3. **Fixed** by labscript-devices PR #154, opened 2026-10-18; verified by reading only and
   needs a test on NI hardware.
   ~~**`labscript-devices` `NI_DAQmx/blacs_workers.py:544` (read).**~~ `stop_task()` calls
   `self.read(self.task, None, -1)`, but the guard at line 454 compares the argument to
   `self.task.taskHandle.value`, so the final read returns early. Samples acquired after the
   last `EveryNSamples` callback are dropped on every shot. A shot shorter than one callback
   interval raises "No data was acquired". This is probably the cause of the workaround at
   lines 672-677.
4. **Fixed** by labscript-devices PR #154, opened 2026-10-18.
   ~~**`labscript-devices` `PrawnDO/labscript_devices.py:299-300` (run).**~~ `wait_idxs` are
   indices that already count earlier waits, but `np.insert` interprets a list of indices
   relative to the original array. With two or more waits, the k-th wait is inserted k
   instructions late and with the wrong held output word.
5. **Fixed** by labscript-devices PR #154, opened 2026-10-18.
   ~~**`labscript-devices` `PrawnBlaster/labscript_devices.py:244` and~~
   `PrawnDO/labscript_devices.py:202` (run).** `self.clock_limit *= factor` scales the clock
   limit in the wrong direction for a non-default `clock_frequency`. With
   `clock_frequency=50e6`, both devices report a 20 MHz limit instead of 5 MHz.
6. **Fixed** by labscript PR #128, opened 2026-10-17.
   ~~**`labscript` `labscript/core.py:419-426` (run).**~~ The ramp tick count comes from
   `divmod((t_next - t)*maxrate, 1)`. When the product is 10.999999 instead of 11, the count
   is one short, and the recovery test only passes if `maxrate` is below the clock limit.
   With ramps at a sample rate equal to the clock limit, 87 of 200 ramps with
   integer-microsecond durations got one tick too few, and the final tick is then two
   periods long.
7. **Fixed** by labscript PR #128, opened 2026-10-17.
   ~~**`labscript` `labscript/outputs.py:432-447` (run).**~~ `get_change_times` assigns
   `current_dict_time` once and never updates it, so it only detects collisions with the
   first ramp on each output. `ao.ramp(0,1,...); ao.ramp(2,1,0,1,1e3); ao.constant(2.5, 7)`
   compiles, and the second ramp is truncated at t=2.5.
8. **Fixed** by labscript PR #128, opened 2026-10-17. The check compares the time before the trigger with the clock period; `compiler.wait_delay` is not included.
   ~~**`labscript` `labscript/outputs.py:365-374` (run).**~~ The "instruction too soon before a
   trigger" check is `max(self.clock_limit, compiler.wait_delay) < trigger_time - t`. It
   compares a rate in Hz with a time, and the inequality is reversed, so it can never raise
   in practice. The error message has the same unit error.
9. **Fixed** by runmanager PR #135 and runviewer PR #76, opened 2026-10-18.
   ~~**Qt6 check states (run for enum semantics, read for code paths).**~~ On PyQt6 and PySide6,
   `Qt.CheckState.Unchecked` is truthy.
   - `runmanager/runmanager/__main__.py:1957` stores `checkState()` as the shuffle flag, and
     `runmanager/__init__.py:603` tests its truthiness, so every axis is always shuffled.
   - `runmanager/__main__.py:2150`: `stateChanged` delivers an int, and
     `2 in [Qt.Checked, Qt.Unchecked]` is false, so the master shuffle checkbox does nothing.
   - `runviewer/runviewer/__main__.py:725-730, 780, 830`: unticking a shot takes the
     "checked" branch, and shutter lines can never be hidden.
10. **Fixed** by labscript-utils PR #133, opened 2026-10-17.
    ~~**`labscript-utils` `labscript_utils/unitconversions/aom.py:15,59,73` (run).**~~
    `from numpy import *` exports `max` under numpy 2, so `max(c - A, 0)` becomes
    `np.max(x, axis=0)` and returns `c - A`. With the default parameters, Pmin is -0.068
    instead of 0.

## 1.3 Hangs, stuck states and crashes

11. **Fixed** by blacs PR #129, opened 2026-10-18; the mid-shot error poll is unchanged.
    ~~**`blacs` `blacs/experiment_queue.py:882` (run).**~~ `self.current_queue.get(2)` passes 2
    as `block`, not `timeout`, so the `except queue.Empty` branch that polls tabs for error
    state is unreachable. If a tab's state machine has exited with a fatal error during the
    shot, the queue manager blocks at "Saving data..." until the user restarts that tab. The
    mid-shot error poll at lines 761-773 is inside the `try` after `get_nowait()`, so it
    only runs when an abort or restart message was just dequeued.
12. **Fixed** by blacs PR #128 (the shot-file handlers) and blacs PR #129 (the unbound
    `message`), both opened 2026-10-18.
    ~~**`blacs` `blacs/experiment_queue.py:808-823, 930-945, 999` (read).**~~ The error handlers
    reopen the shot file and call `shutil.move` unguarded. If the shot file was deleted or
    is unreadable, or if `clean_h5_file` returned False, the handler raises and `manage()`
    exits. The status stays at "Transitioning to buffered...", and `process_request` keeps
    answering "Experiment added successfully". Line 999 logs `message`, which is unbound if
    `process_request` raised during a repeat.
13. **Fixed** by blacs PR #129, opened 2026-10-18.
    ~~**`blacs` `blacs/experiment_queue.py:437` (run).**~~
    `''.join(basename.split('_rep')[:-1])` deletes every earlier `_rep` in the full path.
    `/data/mot_repump_scan/2026/mot_repump_scan_0.h5` becomes
    `/data/motump_scan/2026/motump_scan_0_rep00002.h5` on the second repeat.
14. **Fixed** by runmanager PR #135, opened 2026-10-18.
    ~~**`runmanager` `runmanager/__main__.py:2776-2786` (read).**~~ `preparse_globals_loop`
    calls `task_done()` only after a successful `preparse_globals()`. After an exception,
    `preparse_globals_required.join()` never returns, every remote API call times out until
    restart, and the Engage button stays disabled until a later parse succeeds. Triggers:
    - Line 2392 is `if`, not `elif`, so clicking the Active column of the
      "<Click to add group>" row toggles the dummy row. `get_active_groups` then returns the
      dummy row as an active group, and `get_globals` raises `KeyError`.
    - Line 2692: `expansion_type, name = expansion_name.split()` raises `ValueError` for a
      zip group name containing whitespace. The same failure occurs in `load_configuration`
      (line 3347).
15. **Fixed** by lyse PR #146, opened 2026-10-18.
    ~~**`lyse` `lyse/filebox.py:463-473` (run for the Qt effect).**~~ `update_row` calls
    `self._model.blockSignals(True)` and then returns early when `filepath` is not a row.
    Any multishot routine that calls `Sequence(...).save_result(...)` triggers this, as does
    removing a shot while its analysis is running. The model stays blocked until the next
    successful `update_row`: removed rows remain visible and status changes do not repaint.
16. **Fixed** by lyse PR #146, opened 2026-10-18.
    ~~**`lyse` on pandas 3 (run).**~~
    - `lyse/filebox.py:482-494`: `update_row` catches only `ValueError`, but pandas 3 raises
      `TypeError` for an incompatible-dtype `.at` assignment (float into an int64 column,
      str into float64, etc.). The exception pauses analysis.
    - `lyse/__main__.py:461-464`: `pandas.to_numeric(..., errors='ignore')` raises
      `ValueError` on pandas 3, so "Save dataframe" fails for any dataframe with an
      object-dtype column.
17. **Fixed** by labscript-devices PR #153, opened 2026-10-18.
    ~~**`labscript-devices` `PrawnBlaster/labscript_devices.py:411-427` (run).**~~ The `else`
    branch for a WAIT without the internal wait monitor has no `continue`, so execution
    reaches `instruction["reps"]` with `instruction == "WAIT"`. Any PrawnBlaster used as a
    secondary pseudoclock, or with `use_wait_monitor=False`, fails to compile a shot
    containing `wait()`.
18. **Fixed** by labscript-utils PR #133, opened 2026-10-17.
    ~~**`labscript-utils` `labscript_utils/h5_lock.py:41-66` (run for the mode error).**~~
    - `File.__init__` has `mode=None` and passes it positionally to h5py 3, which rejects
      None. Once `h5_lock` is imported, `h5py.File(path)` with no mode raises `ValueError`.
      No suite code omits the mode, so this affects user analysis scripts and third-party
      libraries.
    - `kill_lock.acquire()`, `Lock(...)` and `zlock.acquire()` run before the `try`. If the
      zlock acquire times out, the KillLock count is never decremented, and the process can
      no longer be terminated by SIGTERM.
    - `close()` releases unconditionally, so a second `close()` releases the zlock twice and
      raises.
19. **Fixed** by labscript-c-extensions PR #13, merged 2026-10-17, with runviewer #13.
    ~~**`labscript-c-extensions` `src/runviewer/resample.pyx:61-67, 109-118` (run).**~~ The
    NaN-fill loop advances `i` by 3 with no bound. runviewer calls it with `N_out=6002` and
    `len(y_out)=6001`. If the first data time is inside the last sample interval of the
    view, `i` becomes 6003 and the code writes `y_out[6003]`, which is two elements past the
    buffer. Line 66 (`while x_in[j] < x_out[i]: j += 1`) has no `j < N_in` bound.
20. **Fixed upstream** by labscript-utils PR #128, merged 2026-10-13.
    ~~**`labscript-utils` `labscript_utils/zlock.py:43` (read).**~~ `config['zlock_port']` is
    put in the `Popen` command list without `str()`. When labconfig has no `[ports] zlock`,
    the default is an int and `Popen` raises `TypeError` in the detached launcher.
    `connect_to_zlock_server()` then waits 15 s and fails at `h5_lock` import.

## 1.4 Worst cruft

- **`from pylab import *`** in `labscript/labscript/labscript.py:46`,
  `labscript/labscript/functions.py:17` and `runmanager/runmanager/functions.py:14`.
  Consequences:
  - `labscript/__init__.py:13` re-exports pylab's `core`, so `labscript.core` is
    `numpy.core`, and `labscript.compiler` is the `Compiler` instance rather than the
    module. The docs extra pins `numpy<2` to work around this.
  - `labscript/labscript.py:600`: `all` is `numpy.all`, and `np.all(generator)` is always
    true, so the colour validation in `add_time_marker` never rejects anything.
- **`repr`/`eval` persistence in BLACS** (`front_panel_settings.py:91, 374, 401-404`;
  `__main__.py:313, 353, 365, 607, 615`). See Part 2, blacs bug B1.
- **Dead code**: `labscript_utils/versions.py`, runviewer `__resample3`/`__resample4` and
  `TempShot`, lyse `replace_with_padding` and the msgpack branch, the `__main__` demo blocks
  and GTK branches in blacs.
- **`blacs/measure_ball/`**: 6.7 MB of Windows binaries in every wheel.
- **`labscript-devices`**: devices that cannot run on the current stack, about 400
  duplicated lines between `PulseBlaster.py` and `PulseBlaster_No_DDS.py`, and vendor
  packages as hard dependencies.
- **Packaging**: `labscript-utils/pyproject.toml` lists only two packages (run: a wheel
  built without git metadata omits all subpackages); `requires-python >= 3.8` and
  `numpy >= 1.15` everywhere; `release.yml` tests `-z` on variables documented as "true or
  false".
- **PyQt4 and Python 2 leftovers** in every GUI repo.

## 1.5 Recommendations

1. Release `'S256'` and the `bitfield` fix in `labscript`, `blacs` and `labscript-devices`,
   or cap numpy below 2.5 until then.
2. Add one CI job per repo. No repo has a test or lint job. Running `ruff --select F,E9`,
   importing the package, and compiling one dummy-device shot and running its runviewer
   parser on the newest numpy would have caught items 1, 2, 4, 5 and 17.
3. Do clock arithmetic in integer multiples of `clock_resolution` in `labscript/core.py`.
   This fixes item 6 and the float `<` comparisons that reject pulses of exactly the
   minimum period (Part 2, labscript B1).
4. Replace every truthiness or int comparison of a check state with `== Qt.Checked`.
5. Make the long-running threads robust to exceptions in their own error handling: the
   BLACS queue manager, the runmanager preparse loop (`task_done` in a `finally` block) and
   lyse's `update_row` (`try`/`finally` around the blocked-signals section).
6. Fix the NI analog input read (item 3) and the PrawnBlaster/PrawnDO compile paths
   (items 4, 5, 17) before the legacy devices.
7. Delete the dead code, replace the pylab star imports with explicit imports or define
   `__all__`, and move vendor packages to optional extras.
8. Raise `requires-python` and the numpy/h5py floors consistently, and bound pandas below 3
   in `lyse` until item 16 is fixed.

---

# Part 2: further findings by repo

## labscript

### Bugs

- **B1. Fixed** by labscript PR #128. ~~**`labscript/core.py:229, 262, 289` (run).**~~ The clock-limit checks compare float
  differences with `<` and no tolerance. With a 1 MHz clockline,
  `do.go_high(0.3); do.go_low(0.3 + 1e-6)` raises "cannot support update delays shorter
  than 1e-06 seconds". A pulse of exactly the minimum period passes or fails depending on t.
- **B2. Fixed** by labscript PR #128. ~~**`labscript/base.py:128` (run).**~~ The device name check uses `locals()` and
  `globals()` of `base.py` since `Device` moved there (461344e). `AnalogOut('sin', ...)` is
  accepted, and the user script then fails with "'numpy.ufunc' object has no attribute
  'constant'". Devices named `worker`, `gui`, `connection`, `name`, `location` or `kwargs`
  are rejected. `load_globals` (`labscript.py:717`) has the same `locals()` problem for
  globals named `name`, `params` or `hdf5_file`.
- **B3. `labscript/labscript.py:540-559`, `labscript/core.py:805-825` (plausible).**
  `trigger_all_pseudoclocks` computes `wait_delay` but calls
  `pseudoclock.trigger(t, compiler.trigger_duration)` without it, and no caller passes the
  `wait_delay` argument of `PseudoclockDevice.trigger`. Secondary pseudoclocks are
  retriggered at t as soon as the master resumes. `Output.wait_delay`
  (`outputs.py:137-146`) is unused. The intent is inferred from the docstring and commit
  8afe91c.
- **B4. Fixed** by labscript PR #128. ~~**`labscript/outputs.py:1448, 1464, 1581, 1597` (run).**~~
  `StaticDigitalQuantity.go_high/go_low` call `add_instruction(0, ...)`, and
  `Shutter.open/close` clamp to 0. On a device clocked by a secondary pseudoclock with
  `trigger_delay > 0`, these raise "has an instruction at t=0s". They should use `self.t0`.
- **B5. Partly fixed** by labscript PR #128: `parentless=True` compiles. The `do_checks` signature clash remains. ~~**`labscript/core.py:634-656, 697-720` (run).**~~ `TriggerableDevice` with
  `parentless=True` cannot compile, because `self.trigger_device` is only set when a parent
  is given. `PseudoclockDevice.do_checks(outputs)` also overrides
  `TriggerableDevice.do_checks()` with a different signature, so the shared-trigger
  consistency check never runs for secondary pseudoclocks.
- **B6. Fixed** by labscript PR #128. ~~**`labscript/outputs.py:2077-2087, 2118-2150` (run).**~~ `StaticDDS` never sets
  `self.gate = None`. Without `digital_gate`, `enable()` raises `AttributeError` instead of
  the intended `LabscriptError`. With a gate, `enable(t=None)` fails in `round(None, 10)`.
- **B7. Fixed** by labscript PR #128. ~~**`labscript/outputs.py:1962-1965` (run for behaviour, plausible as a bug).**~~
  `setamp(t + duration, 0)` is inside `if amplitude != 0 and self.gate is not None`, so
  `DDS.pulse` on a DDS without a gate leaves the amplitude at its pulse value until the end
  of the shot. Line 1955 also fails with `frequency=None` and `print_summary=True`.
- **B8. Fixed** by labscript PR #128: the final tick is one period of the slowest clock limit among the pseudoclock and its clocklines, or twice the longest minimum clock high time if that is longer. ~~**`labscript/core.py:520-536` (read).**~~ `local_clock_limit` is computed over all
  clocklines and then unused. The final tick step is `10.0/self.clock_limit`, which uses
  the pseudoclock limit. With a clockline that is much slower than the pseudoclock, the
  last tick period is shorter than `1/clock_line.clock_limit`.
- **B9. Fixed** by labscript PR #128. ~~**`labscript/base.py:392-396` (run).**~~ The set branch of `quantise_to_pseudoclock`
  cannot work: `np.array(a_set)` is a 0-d object array, and the division raises. No current
  caller passes a set.
- **B10. Fixed** by labscript PR #128 with `tokenize.open`. ~~**`labscript/labscript.py:393, 420` (plausible).**~~ Script files are read with
  `open(path).read()` with no encoding, and the files are not closed. On Windows the locale
  encoding is used, so UTF-8 scripts with non-ASCII characters are saved incorrectly or
  raise `UnicodeDecodeError`.
- **B11. Fixed** by labscript PR #128 except the last item (`added_properties={}`), which is left because the decorator stores the call value and a `None` default would change the connection table. **Minor error-path problems (read).**
  - `labscript/utils.py:231-234, 248-251`: `suppress_*_warnings` have no `try`/`finally`,
    so an exception inside the `with` block leaves the flag changed.
  - `labscript/core.py:642`: the f-string is missing the opening quote before
    `{self.trigger_edge_type}`.
  - `labscript/labscript.py:639`: `min(clockline_limits)` raises on an empty sequence if
    the master pseudoclock has no clocklines. Line 557 raises `AttributeError` if `wait()`
    is used with no pseudoclocks.
  - `labscript/labscript.py:308`: `_have_vcs` only catches `FileNotFoundError`, so a
    non-zero exit of `git --version` or `hg --version` aborts the compile.
  - `labscript/outputs.py:1837-1838, 2079-2080`: `digital_gate.pop()` mutates the dict
    that the user passed.
  - `labscript/base.py:60`: the `added_properties={}` default is stored as a property, so
    one dict object is shared by all devices that do not pass it.

### Cruft

- **C1. `labscript/labscript.py:26-33, 710-766`.** The
  "TO_DELETE:runmanager-batchompiler-agnostic" notes are stale:
  `runmanager/batch_compiler.py:67` still calls `labscript_init(run_file, labscript_file=...)`,
  so `load_globals` is the live path. `load_globals` also opens the HDF5 file a second time
  and never uses the handle (line 715).
- **C2. `labscript/labscript.py:44`.** `import qtutils` exists only to make the pylab import
  select the right Qt binding.
- **C3. Packaging.** `scipy` is declared but never imported. `h5py`, `qtutils` and `PIL`
  are imported directly but not declared. `setuptools_scm` warns that the
  `release-branch-semver` version scheme has been renamed.
- **C4. `labscript/__version__.py`.** `importlib_metadata` fallback for Python < 3.8.
  `setuptools_scm` runs on every import from a git checkout. `local_scheme` differs from
  pyproject (`node-and-date` and `no-local-version`).
- **C5. CI.** `release.yml` builds and publishes only. `macos-13` is in `OS_LIST_ALL`.
- **C6. Python 2 leftovers.** `class Device(object)`; `type(t) in [str, bytes]`
  (`labscript.py:543`); `isinstance(color, (str, bytes))` (595); `.encode()` giving bytes
  for script name and path attributes when a file is set but str otherwise (397-398);
  `float(maxrate)  # avoiding integer division` (`core.py:422-466`);
  `startupinfo.dwFlags |= 1` with a comment that the constant is not defined
  (`labscript.py:102`).
- **C7. Dead code and unused names.** `core.py:146-147, 180-182` (commented-out code);
  `outputs.py:1200-1206` (`val = float(value)` unused with a bare `except`);
  `labscript.py:220` (unused `time_markers_dataset`); the `duration` argument of `sine()` in
  `functions.py`; `compiler.py:24-25` instantiates `LabConfig()` twice; repeated
  `if not hasattr(self, "_properties")` guards in `base.py:215, 303, 333`.
- **C8. Duplicated logic.** The six ramp methods in `outputs.py:558-953` repeat the same
  `add_instruction` dict. `StaticAnalogQuantity` and `StaticDigitalQuantity` duplicate four
  methods. `DDSQuantity` and `StaticDDS` duplicate the unit-conversion and `digital_gate`
  handling and have diverged (B6). `sine4_ramp` and `sine4_reverse_ramp` both have the
  description "sinusoidal ramp".
- **C9. Stale TODOs** at `core.py:77, 107, 144, 557` and `labscript.py:615`. None marks
  currently broken behaviour.
- **C10. Docs.** `docs/"Using the labscript API.docx"` and
  `docs/source/pyqt5-modified-objects.inv` are binary files in the repo.
  `docs/labscript-dev/clock_example.py` uses the old `slow_clock_tick` key.

## blacs

### Bugs

- **Fixed by blacs PR #130, opened 2026-10-18.** ~~**B1. `blacs/front_panel_settings.py:91` with `blacs/__main__.py:296, 302` (read; repr
  behaviour run).**~~ Tab save data is stored as `repr()` and restored with `eval()`. If
  `eval` fails, `tab_data[tab_name]` is left as `{}`. `__main__.py:296` then raises
  `KeyError: 'data'`, and the `except` handler at 302 raises `KeyError: 'saved_data'` out of
  `BLACS.__init__`. This repeats on every launch until the settings file is deleted.
  Triggers: a `get_save_data()` value that is a numpy scalar under numpy 2 (its repr is
  `np.float64(1.5)`), `inf`, `nan`, an array or an enum. In-tree tabs return builtins, so
  this affects third-party tabs. `plugin_data` (313) and `analysis_data` (353, 615) are
  unguarded `eval`s.
- **Fixed by blacs PR #129 (issue #49), opened 2026-10-18.** ~~**B2. `blacs/tab_base_classes.py:792` (run).**~~ The first `inmain(generator.__next__)` is
  outside the `try`/`except StopIteration`, so a state function that finishes without
  reaching a `yield` puts the tab into fatal error. In-tree, `shutdown_workers` (591) does
  this for a tab with no workers. Line 842: `if next_yield:` means that a falsy yield
  re-sends the previous job to the worker.
- **B3. `blacs/__main__.py:123-145, 635-657` (read).** Closing BLACS during a shot has no
  guard. `closeEvent` sets `manager_running = False`, queues `shutdown_workers` on every tab
  and terminates workers after 2 s. The running shot is abandoned with devices in buffered
  mode, and the shot is absent from the saved queue. The TODO at `experiment_queue.py:748`
  refers to this.
- **Fixed by blacs PR #130, opened 2026-10-18.** ~~**B4. `blacs/tab_base_classes.py:737-738` (run on PyQt6).**~~ `hide_error` sets
  `_tab_text_colour = 'black'` (a str), which is passed to `setTabTextColor`. PyQt6 raises
  `TypeError` on every click of the error-close button. PySide6 accepts it and forces black
  tab text, which overrides the dark-theme palette colour. Line 241 has the same value.
- **Fixed by blacs PR #130, opened 2026-10-18.** ~~**B5. `blacs/tab_base_classes.py:951-988` and `blacs/__main__.py:556-564` (read).**~~
  `PluginTab` never defines `_tab_icon` or `_tab_text_colour`, which
  `update_all_tab_icon_and_text` reads. On Qt6, any plugin that provides a tab makes each
  palette `changeEvent` raise `AttributeError` before the remaining device tabs are
  recoloured. No in-tree plugin defines tabs.
- **Fixed by blacs PR #130, opened 2026-10-18.** ~~**B6. `blacs/device_base_class.py:446-450, 471-475` (read).**~~ `if results:` treats a
  primary worker return of `{}` as failure, so the `program_manual` of secondary workers is
  never called. If a secondary returns None, `results.update(None)` raises `TypeError`.
  Line 483 checks `isinstance(self._last_programmed_values, dict)`, where
  `_last_remote_values` was probably intended.
- **Fixed by blacs PR #130, opened 2026-10-18.** ~~**B7. `blacs/plugins/progress_bar/__init__.py:336` with 187-190 (read).**~~ After a wait
  that precedes the first time marker, `update_bar_style(marker=True, previous=True)`
  computes `marker_index = -1` and fails `assert marker_index >= 0`.
- **Fixed by blacs PR #130, opened 2026-10-18.** ~~**B8. `blacs/__main__.py:644` with `blacs/front_panel_settings.py:387-390` (read).**~~
  "Save data from broken tabs?" → Yes keeps only front panel values. The `save_data` of
  failed devices is dropped.
- **Fixed by blacs PR #130, opened 2026-10-18.** ~~**B9. Small errors (read).**~~
  - `blacs/__main__.py:341`: `logger.exception` format string has `%s` and no argument.
  - `blacs/plugins/connection_table/__init__.py:113`: `Popen([editor_path, editor_args])`
    passes all editor arguments as one argv element.
  - `blacs/plugins/memory/__init__.py:71`: `memprof.start` is connected directly to
    `triggered` and probably receives `checked=False` as `filepath` (plausible).
  - `blacs/front_panel_settings.py:291`: the dialog says "connection table" where it means
    "front panel".
  - `blacs/front_panel_settings.py:358`: every Image output logs a warning once per shot.
  - `blacs/front_panel_settings.py:348,387`: the fixed-width bytes dtype is ASCII-only, so
    a non-ASCII `current_units` or tab save-data string raises `UnicodeEncodeError`.

### Cruft

- **C1. `eval` on user-selected files.** "Open front panel" evaluates strings from any h5
  file. The `except NameError` "quick fix for qt objects" (`__main__.py:364-367, 606-609`)
  exists because of this. `restore()` builds `question`/`error` dicts that no caller uses
  (TODOs at `__main__.py:275, 594`), so those channels are silently not restored.
- **C2. Demo and test code inside shipped modules**: `tab_base_classes.py:1042-1251`,
  `device_base_class.py:739-989`, `output_classes.py:947-1040`. The code is not runnable as
  written (e.g. `do_prop['port0/line%d']` without `% i` at line 888, and
  `sys.stdout = open(os.devnull)` opened read-only). `tests/` contains only an h5 fixture.
- **C3. GTK, PyQt4 and PySide1 leftovers.** `compile_and_restart.py:59-63`
  (`on_activate_default` uses `.get_sensitive()`); `front_panel_settings.py:112-124`
  ("Legacy restore from GTK save data") and 409-412; `plugins/connection_table/__init__.py:323-369`
  (`'PySide' in sys.modules` branches, and `order` computed then discarded);
  `plugins/progress_bar/__init__.py:94-96` (Plastique fallback); stale header path in
  `output_classes.py:3`.
- **C4. `__main__.py`.** Lines 749-774: a `tracelog` block listing modules that no longer
  exist. Line 734: `print(h5_filepath)`. Commented code at 230, 236, 239, 646-648. The
  comment block at 483-494 says that the window-position code does not work. Lines 724-725:
  `except Exception: raise`.
- **C5. `tab_base_classes.py` dead state.** `_tab_icon_and_colour_timer` (238-239) is
  created but never started. `hide_not_responding_error_for` (749) is written once and
  never read. `define_state` (210) reassigns `function.__name__` on every call.
  `StateQueue.logging_enabled` (75) is always False. At 643-644 and 661,
  `timer = inmain(QTimer)` followed by `timer.singleShot(...)` calls the static method, so
  `timer.stop()` cancels nothing. Lines 800-802 use `self.workers` while 813 uses the
  captured `workers`.
- **C6. Packaging, CI and docs.** `NEWS.md` stops at 2.8.0 (2019) with Bitbucket links.
  `docs/UsingBLACS.docx`/`.pdf` and `docs/How to add a new device/*.tex` predate the Sphinx
  docs. `pyproject.toml` uses the deprecated `license = {file=...}` table.
- **C7. Unused code.** `notifications.py:150-155` (`close_all` is never called and calls
  `.close()` on class keys); the `ct_editor` setting in `plugins/general`;
  `plugins/memory/__init__.py:41` (`get_callbacks` body is the bare expression `{}`) and 62
  (writes `memprof.txt` into the installed package directory); the `'close'` signal in
  `analysis_submission.py:213`; 22 unused imports.
- **C8. Hard-coded values.** `experiment_queue.py:532-533` (`timeout_limit = 300` with a
  TODO); `"C:\\"` as the file-dialog start directory in
  `plugins/connection_table/__init__.py:392, 429, 452`; `experiment_queue.py:546-554`
  detects an empty queue by catching `IndexError` under `except Exception`.
- **C9. Minor.** `compile_and_restart.py:34`: `output_path.strip('.h5')` strips a character
  set, not a suffix. `front_panel_settings.py:256`: mutable default `silent={}`.
  `__main__.py:739-745`: `ExperimentServer.process` runs `process_request` on the GUI
  thread.

## runmanager

### Bugs

- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B1. `runmanager/__init__.py:468-472, 572`; `__main__.py:3438-3448, 2745` (run for the
  library part).**~~ `evaluate_globals` checks iterability only for `outer`. The GUI relies on
  `guess_expansion_modes` to remove non-iterables from zip groups, but that function
  returns early if any global holds a non-`ExpansionError` exception. `expand_globals` then
  runs `zip(*[[1,2,3], 5])` and raises `TypeError` in the preparse thread.
- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B2. `runmanager/__main__.py:1372-1374` (plausible).**~~ `update_parse_indication` indexes
  `evaled_globals` by the names currently in the model. A global created or renamed while a
  parse is in progress raises `KeyError` in the preparse thread.
- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B3. `runmanager/__main__.py:3456-3475, 3562-3568` (run).**~~ A list-valued global with a
  deliberately blank expansion is reset to `outer` on every restart, and after deactivating
  and reactivating its group. With `x = [1,2,3]` and a cleared expansion, a fresh session
  produces 3 shots instead of 1.
- **B4. `runmanager/__init__.py:572` (run).** Zip groups with unequal lengths are silently
  truncated by `zip(*axis)`. If this is intended, the GUI should indicate it.
- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B5. `runmanager/__main__.py:1819-1821` (read).**~~ `close_current_tab` calls
  `close_group` inside iteration over `currently_open_groups` with no `break`, so Ctrl+W
  closes the tab and then raises "dictionary changed size during iteration".
- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B6. `runmanager/__main__.py:3696` (run on numpy 2.5).**~~ `remote.set_globals` stores
  `repr(new_value)`, which numpy summarises for arrays with more than 1000 elements. The
  stored expression is `array([0., ..., 1.], shape=(2000,))`, which fails to evaluate. With
  older numpy the repr would evaluate to a short object array containing `Ellipsis` (not
  tested).
- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B7. `runmanager/__init__.py:1107-1111, 1122` (run).**~~ `globals_diff_shots` raises
  `UnboundLocalError` when the two shots are identical, because `df` is only assigned when
  there are differences.
- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B8. `runmanager/__init__.py:749` (run).**~~ With zero shots (e.g. an `outer` global that
  evaluates to `[]`), `int(np.ceil(np.log10(0)))` raises `OverflowError` in the compile
  thread, after the sequence index has been consumed. `make_run_file_from_globals_files`
  (815) would raise `IndexError` on `shots[0]`.
- **Fixed by runmanager PR #136, opened 2026-10-18, except the `compile_loop` timeout.** ~~**B9. `runmanager/batch_compiler.py:61-62, 74`; `__main__.py:3380` (read; the indefinite
  wait is plausible).**~~ `os.chdir(os.path.dirname(labscript_file))` is outside the `try`,
  so a missing directory ends the batch compiler process. `except Exception` also does not
  catch `SystemExit`. In both cases `compile_loop` waits on `from_child.get()` with no
  timeout.
- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B10. `runmanager/__init__.py:1002-1003` (run).**~~ `find_comments` advances `line_start`
  only on `'\n'` tokens, which a triple-quoted string does not produce. Offsets after a
  multi-line string are wrong, and `remove_comments_and_tokenify` then deletes part of the
  string and keeps the comment.
- **Fixed by runmanager PR #134, opened 2026-10-18 (`_make_axes` iterates the axes).** ~~**B11. `runmanager/__init__.py:607-608` (run for the library).**~~ Keys in
  `expansion_config` that are not current axes give `axes.get(key) = None`, and
  `expand_globals` raises `TypeError`. In the GUI this can happen when Engage is clicked
  between a globals change and the end of the following preparse.
- **Fixed** by runmanager PR #134, opened 2026-10-18. ~~**B12. `runmanager/__main__.py:3392`
  (read).**~~ `compile_loop` disables the Abort button
  after each queue entry, and `on_engage_clicked` enabled it only at queue time. A second
  queued sequence cannot be aborted.
- **Fixed by runmanager PR #136, opened 2026-10-18.** ~~**B13. `runmanager/__init__.py:857-858, 892-898, 903` (read).**~~
  `compile_labscript_async` raises on an unexpected signal without quitting the child.
  `compile_multishot_async` ignores any signal other than `done` and loops forever, and its
  `except` path calls `zmq_push_multipart(stream_port, ...)` although `stream_port=None` is
  a documented default.
- **Fixed by runmanager PR #136, opened 2026-10-18, except the zlock in the main thread and `remote.engage()`.** ~~**B14. Smaller defects.**~~
  - `__init__.py:326-329`: `delete_global` leaves the `units` and `expansion` attributes in
    the file (run).
  - `__init__.py:201-217`: `copy_group` does not close `dest_f` on exception, and repeated
    copies are named `g_copy`, `g_copy(1)`, `g_copy(1)(2)` (run).
  - `__init__.py:815`: `make_run_file_from_globals_files` writes `run number = 1` with
    `n_runs = 1`, whereas `make_run_files` is 0-based.
  - `__main__.py:2179-2188`: the duplicate-filename expansion loop in the copy/move menu
    exits after one pass because `filenames = new_filename` aliases the two dicts.
  - `__main__.py:3794, 3804`: remote `get_labscript_file` and `get_shot_output_folder`
    return the cwd when the field is empty.
  - `__main__.py:1872-1873`: missing `return` after the "No editor specified" dialog.
  - `__main__.py:427`: Space or Enter with no current index gives `AttributeError`.
  - `__main__.py:3642-3647`: `send_to_runviewer` leaks the devnull handle and calls
    `os.fork()` from the compile thread of a multi-threaded process.
  - `__main__.py:2593` (via `__init__.py:641`): `get_default_output_folder` acquires a
    zlock in the Qt main thread on every change of either line edit and every 30 s
    (plausible).
  - `__main__.py:3841`: `e.__class__(msg)` fails for exception classes that need more than
    one constructor argument.
  - `remote.py:53-54`: `engage()` returns None whether or not `on_engage_clicked`
    succeeded.

### Cruft

- **C1. PyQt4 leftovers**: `if type(x) is tuple` after every `QFileDialog` call
  (`__main__.py:1847, 1890, 2293, 2314, 2334, 3148, 3249`).
- **C2. Dead code in `__main__.py`**: `nested` (129-136); `log_if_global` (86-102), which is
  called only with an empty list; axes context-menu stubs that raise `NotImplementedError`
  (1671-1674, 1761-1763, 2018-2030); `kwargs.pop('iconPosition')` after `kwargs` was already
  passed to `QTabBar` (160-163); `is None` checks on `get_default_output_folder`, which
  returns `''` (1907, 2623); commented-out logger lines (1362, 1369-1370, 1381-1407,
  3403-3414); unused imports `ast`, `pprint`, `qtutils.icons`.
- **C3. Stale comments**: "we only update it once a second" (3597; the loop sleeps 30 s);
  "Ensure folder exists..." (3267) above unrelated code; `changeEvent` says "only for
  PySide6" but tests `endswith('6')` (1449).
- **C4. `__init__.py:161-166`**: every `get_grouplist` call runs the deprecated
  `add_expansion_groups`. Other deprecated shims: `_ensure_str` (289, 303, 317, 392-394),
  `get_shot_globals` (947-959), `drop_times` in `functions.py:35`. The docstring of
  `compile_labscript_with_globals_files_async` starts mid-sentence (915).
- **C5. `remote.py`**: a `Client` is constructed at import time (117); commented-out
  `get_globals_full`/`set_globals_full` (122, 124); the `is_output_folder_default` docstring
  is inverted (109).
- **C6. `globals_diff.py` and `globals_diff.bat`**: the docstring gives an invalid command,
  the `.bat` only works from the package directory, and the function fails on identical
  shots (B7).
- **C7. `__main__.py:76`**: hard-coded "Ubuntu Mono" for every non-Windows platform.
  `__main__.py:560`: `index in self.view.selectedIndexes()` is evaluated per cell per paint.
- **C8. Packaging**: `importlib_metadata` fallback in `__version__.py`; `numpy`, `h5py` and
  `zprocess` are imported directly but not declared; BSD-2 and BSD-3 licence files next to
  `LICENSE.txt`; `docs/using_runmanager.docx` and `.pdf` in the repo.

## runviewer

### Bugs

- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B1. `runviewer/__main__.py:1283` (read).**~~ In non-linear time, the x data passed to
  `resample` is scaled but `shot.stop_time` is not. After a marker is dragged to the right,
  the trace is NaN between the unscaled stop time and the real end. `update_plots` (913)
  scales the stop time correctly.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B2. `runviewer/__main__.py:1024` (read).**~~ `scaled_t = t` applies no scaling to shutter
  line positions, and `_update_non_linear_time` (545-548) later treats the positions as
  scaled.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B3. `runviewer/__main__.py:522, 535, 579-582` (read).**~~ The loop
  `for shot in self.shutter_lines[channel]` rebinds the marker shot, so the axis ticks use
  the stop time of the last shot that has shutter lines.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B4. `runviewer/__main__.py:962-968` (read).**~~ Each `update_plots` call adds a full set
  of marker `InfiniteLine`s to every visible existing plot. The lines are only removed in
  `_update_markers` (368-376). Line 964 also builds `QColor(-1,-1,-1)` for the default
  colour.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B5. `runviewer/__main__.py:1287-1289, 1567-1574` (read).**~~ `__pool_resample` has
  `except Exception: pass`, so any resample error gives an empty plot. `_load_device` logs
  parser failures at INFO and continues.
- **Not a bug: runviewer resolves parsers through `labscript_utils.device_registry`, which tolerates a missing labscript-devices (checked 2026-10-18).** ~~**B6. `runviewer/pyproject.toml` (read).**~~ `labscript-devices` is not a dependency,
  although the parsers come from `labscript_devices`. Installed alone, runviewer shows no
  traces.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B7. `runviewer/__main__.py:450-453` (read).**~~ The tooltip value index is
  `argmin() - 1`, which is -1 when the cursor is nearest the first point. Only the first
  data item is read, and a plot with no data items raises `IndexError` on every mouse move.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B8. `runviewer/__main__.py:715, 743, 755, 813-815` (read).**~~ The markers combobox is
  keyed by basename, so two shots with the same filename in different folders enable,
  disable or remove the wrong entry.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B9. `runviewer/__main__.py:396-397, 424` (read).**~~ `delta_t` is not recomputed for the
  final marker, so its label repeats the preceding duration. With `stop_time == 0`,
  `delta_t` is unbound and `_space_markers_evenly` (474) divides by zero.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B10. `runviewer/__main__.py:614-629` (read).**~~ Loading a channel config moves rows in
  the model but does not call `update_plot_positions`.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B11. `runviewer/__main__.py:706-719, 937-949` (read).**~~ Plot items for unchecked
  channels are kept after a shot is removed, which keeps the `Shot` and its traces
  referenced.
- **Fixed by runviewer PR #77, opened 2026-10-18.** ~~**B12. `runviewer/__main__.py:1584-1590` (plausible).**~~ `Shot.scaled_times` is not
  thread-safe: pool threads for different channels can each reset `_scaled_x`. The
  resulting `KeyError` is swallowed by B5.

### Cruft

- **D1. `__main__.py:1089-1246`**: `__resample4` and `__resample3` (about 160 lines) are
  unused and use `numpy.float`. `resample` has an unused `num_pixels` parameter, a constant
  `resampling = True` branch and commented-out code (1056-1085).
- **D2. `__main__.py:1630-1649`**: `TempShot` is unused and assigns to the read-only
  `traces` property. `Shot.delete_cache`, `clear_cache` and `_scalehandler` are dead.
- **D3. `__main__.py:975-977`**: a hidden `PlotWidget` is created for every channel in the
  model on the first `update_plots`.
- **D4. `__main__.py:1428-1446`**: `update_plot_positions` calls `takeAt(i)` over a
  shrinking layout, which removes every other item. The result is only correct because
  `addWidget` moves widgets that are already in the layout.
- **D5. `__main__.py:76-81`**: `SHOT_MODEL__PATH_INDEX = 1` duplicates `SHUTTER_INDEX` and
  is unused. `int_to_enum` plus lambdas stored in `UserRole` (104-113, 190, 741) is an old
  PySide workaround.
- **D6. `__main__.py:1576-1581`**: the "backwards compat" `shutter_times` block reopens the
  h5 file once per device in the recursive `_load_device`.
- **D7. `__main__.py:1663`** uses `labscript_utils.shared_drive` without importing it.
  Lines 681-683: a flag that is set and never read. Line 690: `exec_()`. Line 633: PyQt4
  tuple check. Commented-out lines at 320, 369, 391, 398-400, 420, 753-763, 809-811,
  870-872, 902-905.
- **D8. pyproject**: `pyqtgraph>=0.11.1` and `labscript_utils>=3.1.0b1` predate the Qt6
  work.

## lyse

### Bugs

- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B1. `lyse/analysis_subprocess.py:61` (read).**~~ The module-level
  `LABCONFIG.get('lyse', 'autoload_config_file')` is unguarded, although `__main__.py:184-187`
  treats the option as optional. With a labconfig that lacks the option, every analysis
  worker raises at import, and `start_worker` blocks the GUI thread for the 30 s startup
  timeout. Plot geometry ini files are also always written next to the autoload config.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B2. `lyse/filebox.py:879-884, 908-911` (read).**~~ Only `IOError` is handled per file.
  `get_dataframe_from_shot` raises `KeyError` for any HDF5 file without a `globals` group,
  such as a file created by `lyse.Sequence`. The whole incoming batch is then discarded,
  and `n_shots_added` is not reset, so the progress bar stays visible.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B3. `lyse/__main__.py:498, 486` (run).**~~ `reset_index()` without `drop=True` when
  loading a saved dataframe inserts a column `('index', '')`, which appears in the filebox
  and in `lyse.data()`.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B4. `lyse/communication.py:82` (run).**~~ The result of `df.infer_objects()` is
  discarded, so object columns are sent as object. `__main__.py:461` has the same error.
  `DataFrameModel.infer_objects` (`filebox.py:450`) is correct but has no callers.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B5. `lyse/__main__.py:271, 467` (read).**~~ `self.app` does not exist on `Lyse`. "Revert
  configuration" with nothing to revert, and "Save dataframe" with an empty dataframe, raise
  `AttributeError`.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B6. `lyse/__init__.py:1036-1044, 1076-1080` (read).**~~ `get_globals_expansion` and
  `get_units` test `'expansion' in name` and `'units' in name` on the visited path, which
  is true for a globals group named e.g. `units_tests`. The test should be on
  `name.split('/')[-1]`.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B7. `lyse/__init__.py:58-62` (read).**~~ The `sys.argv` check runs in every process that
  imports lyse. In a Jupyter kernel or pytest it emits the `FutureWarning` and sets
  `lyse.path = sys.argv[1]`.
- **Fixed by lyse PR #145 (the dict cell) and lyse PR #147 (the rest), opened 2026-10-18.** ~~**B8. `lyse/__init__.py:671-676` and `dataframe_utilities.py:62-68` (read; dict-cell
  behaviour run).**~~ The live dataframe update differs from a reload from file.
  - ~~A dict result is one object cell live, and sub-columns after reload.~~ Fixed by lyse PR
    #145, opened 2026-10-18.
  - `group='results/a/b'` creates a live column that never appears on reload.
  - `group='/results/x'` gets no live update.
  - A tuple stays a tuple live and becomes a list on reload.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B9. `lyse/dataframe_utilities.py:66-106` (read).**~~ Row keys collide without warning. A
  results group with the same name as a global replaces that global's column. A script
  named `sequence.py`, `labscript.py` or `filepath.py` has its results overwritten.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B10. `lyse/__init__.py:958-974` (read).**~~ `Run.get_globals` returns raw `dict(attrs)`,
  unlike `shot_utils.get_shot_globals`. A None global is returned as a null
  `h5py.Reference`, and bools as `np.bool_`.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B11. `lyse/analysis_subprocess.py:385` (plausible).**~~ Only `Exception` is caught around
  the user script. A script that calls `sys.exit()` leaves the worker's mainloop thread
  blocked while holding `kill_lock`, and the GUI's analysis thread waits until the user
  restarts the worker.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B12. `lyse/filebox.py:637-646` (run for the format failure; trigger plausible).**~~
  `'{:04d}'.format(val)` fails when the `run number` column is float64, which happens if
  any loaded shot lacks the attribute. `renumber_rows` then raises part-way through
  `add_files`.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B13. `lyse/filebox.py:386-395`, `routines.py:193-202` (read).**~~ After the "No hdf5
  viewer / editor specified" dialog, the code does not return and runs `Popen([''] + args)`.
- **Fixed by lyse PR #147, opened 2026-10-18.** ~~**B14. `lyse/communication.py:60-64` with `__main__.py:137, 161` (plausible).**~~ The
  server starts before `self.filebox` exists. A shot submitted by BLACS during lyse startup
  gets an `AttributeError` reply and is lost.

### Cruft

- **C1. `dataframe_utilities.py:189-204`**: `replace_with_padding` uses
  `pandas.Int64Index` and `DataFrame.append`, which were removed in pandas 2.0. It is dead.
  Delete it together with the `new_row_data` branch at `filebox.py:466-467, 498-503`.
- **C2. `__main__.py:483-496`**: the `pandas.read_msgpack` branch (removed in pandas 1.0)
  and the `*.msg` file filter.
- **C3. `__init__.py:997-1018`**: commented-out `iterable_globals` block with Python 2
  print statements.
- **C4. `__init__.py:1175-1197`**: `Sequence.get_traces`, `get_result_arrays` and
  `get_image` stubs that raise `NotImplementedError`, while other inherited accessors act
  on the sequence file.
- **C5. PyQt4 and Python 2 leftovers**: tuple checks after `QFileDialog` calls
  (`__main__.py:290, 362, 449, 475`; `filebox.py:780`; `routines.py:148`); `u''` literals in
  `utils/gui.py:36-68`; `hasattr(multiprocessing, 'get_start_method')`
  (`analysis_subprocess.py:55`); `importlib_metadata` fallback; unused
  `import pickle as pickle`.
- **C6. `analysis_subprocess.py:37, 495`**: `backend_qt5agg` and `MPLBACKEND=qt5agg` are
  hard-coded although Qt6 is supported. Lines 501-502: `import pylab` under a comment that
  asks whether it should be there. Line 489: `reset_figs` is empty and has no callers.
- **C7. `routines.py:48`, `__main__.py:157-160`**: the `RoutineBox` `filebox` parameter
  receives the `Lyse` app, and `self.filebox` is never used. `routines.py:337-340` has a
  stale TODO with commented-out GTK code.
- **C8. `filebox.py:603-612`**: the tick icon is set inside `if done:` and then set again
  unconditionally, with two different resource path spellings.
- **C9. `communication.py:111`**: `np.intersect1d(x, x)` is used as "unique" under a
  comment that says ordering is maintained. It returns sorted values.
- **C10. `widgets.py:91-183`**: `TableView` and `TreeView` are full copies of each other.
- **C11. Wrong docstrings**: `get_globals_expansion` documents a nonexistent `h5_file`
  argument; `trace_names` says it raises `KeyError` but returns `[]`; `get_wait` says
  `KeyError` but raises `Exception`.
- **C12. Packaging**: `scipy` is declared and not imported; three licence files are
  shipped; `docs/` still holds the legacy LaTeX manual next to the Sphinx docs; the docs
  extra pins PyQt5.

## labscript-utils

### Bugs

- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B1. `labscript_utils/qtwidgets/digitaloutput.py:53-57`, `enumoutput.py:135-139` (run on
  PyQt6 and PySide6).**~~ The wheel-forwarding branch is guarded by `QT_ENV != PYQT5`, which
  used to select PyQt4 and now selects Qt6. It calls `event.pos()`, `globalPos()`, `delta()`
  and `orientation()`, none of which exist on a Qt6 `QWheelEvent`. Scrolling over a locked
  `DigitalOutput` raises `AttributeError` for every wheel event.
- **Fixed by labscript-utils PR #135, opened 2026-10-18, except the round-trip types, which are the stored format.** ~~**B2. `labscript_utils/properties.py:79-94, 60-64, 19` (run).**~~
  - `set_attributes` falls back to JSON only for a `TypeError` containing "has no native
    HDF5 equivalent". `{'k': ['a', 1]}` and `{'k': [[1,2],[3]]}` raise other errors and do
    not reach the JSON path.
  - `_default` handles only `np.integer`, so `np.bool_` and `np.float32` values raise a
    bare `TypeError`.
  - Round-trip types depend on content: `['a','b']` returns as an object ndarray,
    `['a', None]` as a list, and `[]` as an empty float64 array.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B3. `labscript_utils/double_import_denier.py:133-136, 90-107` (run).**~~
  `sys.tracebacklimit = 2` is restored only by a temporary `sys.excepthook`. If the
  double-import `RuntimeError` is caught, the limit is 2 for the rest of the process.
  Lines 64-65: all frozen stdlib modules map to the key `<cwd>/frozen`, so two frozen
  modules first imported after `enable()` raise a false double import. Line 57 passes
  `path` as the `package` argument of `find_spec`.
- **Fixed by labscript-utils PR #135, opened 2026-10-18, except the OptotuneLens default calibration.** ~~**B4. Other unit conversion bugs (run).**~~
  - `NovaTechDDS9m.py:22-25, 43-46` and `generic_frequency.py:26-27` mutate a class-level
    `derived_units` in place, so a subclass that defines `derived_units` gains duplicate
    units on each instantiation.
  - `optotunelens.py:44` raises `ZeroDivisionError` with its own default parameters.
  - `quad_driver.py:40` and `optotunelens.py:53` use builtin `max`/`min` and fail on
    arrays.
  - Every class except `BidirectionalCoilDriver` has `calibration_parameters=None` and then
    calls `.setdefault` on it.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B5. `labscript_utils/qtwidgets/imageoutput.py:180` (run).**~~ `QEvent` is undefined. The
  name is evaluated for every event delivered while the `ImageOutput` is disabled, so each
  one raises `NameError`. `ImageOutput` is used by `LightCrafterDMD`.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B6. `labscript_utils/qtwidgets/headerview_with_widgets.py:214-218` (run).**~~
  `on_columnsRemoved` iterates `self.widgets.items()` and calls `setWidget(idx, None)`,
  which deletes from that dict. Line 155 raises on `max()` of an empty sequence when all
  sections are hidden. lyse does not currently remove widget columns.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B7. `labscript_utils/qtwidgets/toolpalette.py:188, 204, 129/132, 174` (run).**~~ The
  loops in `create_linked_width_group` and `add_to_linked_width_group` rebind the
  `width_group_name` parameter. `reorder_palette_by_index` calls the undefined `count()`.
  BLACS does not call these methods.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B8. `labscript_utils/labconfig.py:82-90` (read).**~~ Only `NoOptionError` is caught, so a
  missing section or missing labconfig file gives a raw `NoSectionError`. `shared_drive.py:16`
  triggers this at import when `[paths]` is absent. Line 47 mutates the caller's `defaults`
  dict.
- **Fixed by labscript-utils PR #135, opened 2026-10-18, except the macOS `scutil` call.** ~~**B9. `labscript_profile/__init__.py:53-63` and `labscript-suite.pth` (read).**~~ The
  `.pth` code runs at every interpreter start and catches only `ModuleNotFoundError`. A
  labconfig with a parse error prints a traceback on every Python start in the
  environment. It uses `BasicInterpolation` without the env-var expansion of `LabConfig`,
  so `userlib = $HOME/...` is not added to `sys.path`. On macOS, `hostname()` runs `scutil`
  as a subprocess on every interpreter start.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B10. `labscript_utils/ls_zprocess.py:260, 105-110` (read).**~~
  `issubclass(socket_class, SecureContext)` should test `SecureSocket`. The "security not
  configured" check is inside the `except` for a missing `allow_insecure`, so an explicit
  `allow_insecure = False` with no shared secret skips the explanatory error. Line 179
  names the nonexistent `labscript_utils.zprocess.ZMQServer`.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B11. `labscript_utils/filewatcher.py:70-73, 212, 230, 49-53` (read).**~~ The docstring
  allows a single path string, but `set(files)` splits a string into characters.
  `getfullargspec` counts `self`, so a two-argument bound-method callback is treated as a
  three-argument callback.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B12. `labscript_utils/connections.py:112, 114, 241` (read).**~~ `assert_superset` builds
  the per-key diff lines without a newline. Line 241 is `name == _ensure_str(name)`, which
  is a comparison with no effect. Lines 358-365 are a commented-out test block with a
  personal path.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B13. `labscript_utils/__init__.py:62-74` (run).**~~ `dedent("a\n\n")` leaves
  `indentation = inf` and raises `TypeError`.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B14. Minor widget bugs.**~~
  - `qtwidgets/elide_label.py:36, 43`: `self.widget is None` tests the bound method and is
    always False (run).
  - `analogoutput.py:107`: the context menu position comes from the line edit but is mapped
    with `self.mapToGlobal` (read).
  - `analogoutput.py:227`, `digitaloutput.py:46`, `enumoutput.py:128`: each right-click
    creates a `QMenu` that is never deleted.
  - `digitaloutput.py:102`: the inverted setter computes `not state` before `int()`, so the
    string `'0'` sets the wrong state.
- **Fixed by labscript-utils PR #135, opened 2026-10-18.** ~~**B15. `labscript_utils/device_registry/_device_registry.py:212-213, 221-222` (read).**~~ A
  device registered with `runviewer_parser=None` raises
  `AttributeError: 'NoneType' object has no attribute 'split'` instead of a "no parser
  registered" message. Eight `register_classes.py` files pass `runviewer_parser=None`.
  After one failing `register_classes.py`, a retry of `populate_registry` raises "already
  registered".
- **B16. Fixed** by labscript-utils PR #133, opened 2026-10-17 (the `fileno()` call; the
  mkdir race remains). ~~**`labscript_utils/setup_logging.py:60, 68` (plausible).**~~
  `sys.stdout.fileno()` is
  called before the `sys.stdout is not None` check. Under plain `pythonw`, stdout is None.
  Lines 43-44 have an exists/mkdir race between processes.

### Cruft

- **C1. `labscript_utils/versions.py` (272 lines) and `__init__.py:50`.** Nothing in the
  suite calls `check_version` or `get_version`. The import makes `setuptools_scm` a runtime
  dependency and adds about 52 ms to every `import labscript_utils`.
- **C2. Dead modules** (confirmed by grepping the sibling repos):
  `qtwidgets/analoginput.py` and `qtwidgets/InputPlotWindow.py` (the only reason
  `pyqtgraph` is a dependency); `impprof.py`; `testing_utils.py`; `import_or_reload`;
  `unitconversions/test.py`; `camera_server.py` (used only by the legacy
  `imaqdx_server.py`). The lab-specific conversions `quad_driver`, `quad_monitor`,
  `optotunelens`, `aom` and `detuning` are shipped in the library.
- **C3. `labscript_utils/unitconversions/__init__.py:18-59`.** The lazy `_All` object
  exists to avoid importing every conversion module, but `labscript/labscript/labscript.py:53`
  does `from labscript_utils.unitconversions import *` on every import.
  `labscript_devices/NovaTechDDS9M.py:17` imports the class names from the package and
  works only because the labscript import on the previous line ran first (run).
- **C4. `setup.py`.** `develop_command` targets setuptools <= 63 while pyproject requires
  >= 64. `editable_wheel_command` overrides the private `_create_wheel_file`. It imports
  `wheel.wheelfile` without `wheel` in `build-system.requires`.
- **C5. Python 2 and PyQt4 leftovers.**
  - `excepthook/__init__.py:33-55`: `Thread.run` monkeypatch for a Python 2 bug. Line 85:
    `logger.warn`. Lines 89-92: calling `set_logger` twice makes `warnings._showwarning`
    recurse.
  - `headerview_with_widgets.py:87-91, 181-185`: `QVariant` branches.
  - `dragdroptab.py:39-46, 556-561`: PyQt4 debug prints and workaround.
  - `double_import_denier.py:83-87`: `imp` filters.
  - `fingertab.py:55`: `exec_()`.
  - `device_registry/__init__.py`: shim for labscript-devices < 3.1.
  - `labconfig.py:67-80`: `experiment_name` `FutureWarning` from 3.0.
  - `settings.py:59`: `eval()` of an HDF5 attribute, with GTK-era commented code at
    105-121.
- **C6. `qtwidgets/toolpalette.py:104-146, 212-214`**: TODO stubs that return without
  doing anything. Lines 302-312 and 343-376 are commented-out Python 2 prints.
- **C7. Packaging pins across the suite.** The docs extras pin Sphinx 8.2.3 (not checked
  against Sphinx metadata for its minimum Python), and `vendored-conda-builds` targets
  3.10-3.14. `h5py>=2.9`. The `qtutils` floor differs per repo (`>=4.0`, `>=4.1.3`,
  `>=2.2.3`). The docs extras and the `pyqt` extra of `labscript-suite` name PyQt5 only.
- **C8. CI.** The three copies of `release.yml` have drifted: `labscript-utils` and
  `labscript-suite` still list `macos-13` and `setup-miniconda@v3`.
- **C9. `labscript-utils/readthedocs.yaml:27`**: PDF builds are disabled because "h5_lock
  breaks build when sphinx is run twice".

## labscript-c-extensions

- **C1. `pyproject.toml`.** numpy is a build requirement although `resample.pyx` never
  cimports numpy (line 3). The URLs point to `labscript-c-extension`, with the final "s"
  missing (46-48). Runtime `numpy>=1.17.3` (35). `ext-modules` in pyproject is a setuptools
  experimental feature (13).
- **C2.** The `resample.pyx` header and README refer to `license.txt` and
  `raw/master/LICENSE`. The file is `LICENSE.txt`.
- **Fixed by labscript-c-extensions PR #14, opened 2026-10-18 (also for `N_out = 3k + 1`).** ~~**B1. `resample.pyx:117` (run).**~~ If a caller passes `N_out` divisible by 3, the code
  writes `y_out[N_out]` and beyond. runviewer does not do this today.

## labscript-suite (metapackage and docs)

- **C1.** The installation pages instruct `pip install PyQt5` and `conda install "pyqt<6"`
  only.
- **C2. `docs/source/conf.py:87-98`**: stale intersphinx entries and copyright 2020.
- **C3. `README.md:163`**: the link target is the literal `importlib.metadata`.

## vendored-conda-builds

- **C1. `pkgs.toml:14`** lists `osx-64`, but the workflow matrix has only ubuntu and
  windows-2022.
- **C2. `make_packages.py:3`** imports third-party `toml` without installing it explicitly.
- **C3.** The weekly schedule builds `version = "latest"` from PyPI and the unpinned
  default branch of `windows-curses`, and uploads to the main label with no review step.
- **C4. `pkgs.toml:18, 24`**: TODOs to release `spinapi` and `pynivision` normally.
  Workflow lines 95-105: commented-out test-label upload.

## labscript-devices

Paths are relative to `labscript_devices/`.

### Bugs

- **B1. `NI_DAQmx/blacs_workers.py:571` (read).**
  `self.AI_start_delay = self.AI_start_delay_ticks*self.buffered_rate` should divide by the
  rate. Only the PXIe-4499 uses this (64 ticks). At 1 kHz, t0 becomes 64000 s and every
  saved trace is empty.
- **B2. `PrawnBlaster/blacs_workers.py:544` (read; firmware response plausible).**
  `abort_buffered` sends `abort` only when the device is not the master pseudoclock.
  Aborting a running shot on a master PrawnBlaster sends nothing, so the device keeps
  clocking to the end of the program.
- **B3. `PrawnBlaster/blacs_workers.py:414, 420` (read).** After binary programming, the
  smart cache holds a numpy array, but the incremental path calls `.append(None)` on it. A
  shot with more instructions than the previous one and no more than 10% changed raises
  `AttributeError` in `transition_to_buffered`.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B4. `PrawnDO/runviewer_parsers.py:85` (run).**~~ `int(chan, 16)` is applied to
  connections of the form `do3`, which raises `ValueError`. No PrawnDO output is shown in
  runviewer.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B5. `PrawnBlaster/runviewer_parsers.py:97-108`.**~~
  - For a hardware-triggered PrawnBlaster, the final stop row is treated as a wait and
    indexes `clock_ticks[trigger_index]` past the end, so nothing clocked by a secondary
    PrawnBlaster is shown (run).
  - `elif last_instruction_was_wait:` does not test `reps == 0`, so in internal wait
    monitor mode the first real instruction after each wait is skipped (read).
- **B6. `NI_DAQmx/blacs_workers.py:747-763, 795-805` (read).** In the wait monitor thread,
  `read_edges` with a finite timeout makes one blocking `ReadCounterF64` call for the whole
  timeout. Aborting a shot blocks `stop_tasks(abort=True)` in `join()` for up to the time
  until the next wait plus its timeout. When the read times out, the thread calls
  `send_resume_trigger()` during the abort.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B7. `PulseBlaster.py:1216-1260` (read).**~~ `PulseBlasterParser` treats `LONG_DELAY` rows
  as a single delay of `length` and ignores `inst_data`. Any instruction longer than about
  57 s is shown too short.
- **Fixed by labscript-devices PR #153 (issue #79), opened 2026-10-18.** ~~**B8. `PulseBlasterESRPro500.py` (read).**~~ There is no `@runviewer_parser` class.
  runviewer raises "No class decorated as a runviewer_parser found", and since the device
  is normally the master pseudoclock, the whole shot is not displayed.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B9. `PulseBlaster.py:648` (read).**~~
  `PulseBlasterDirectOutputs.clock_limit = PulseBlaster.clock_limit` (8.3 MHz) is fixed for
  all subclasses. Direct outputs on ESR-PRO-200/500 are rejected by labscript when edges
  are closer than 120 ns.
- **B10. `IMAQdxCamera/blacs_workers.py:382-386, 422-424` (read).** If continuous
  acquisition is running and a shot has no exposures for this camera,
  `transition_to_buffered` pauses the continuous thread and `transition_to_manual` returns
  without restarting it. Clicking Stop then fails an assert at line 363. This affects all
  subclasses.
- **B11. `IMAQdxCamera/blacs_workers.py:226, 427` (read).** An exception in the acquisition
  thread only ends the thread. `transition_to_manual` tests only `is_alive()`, so the shot
  completes without an error and with fewer images, which are paired with the first
  exposures by `zip`. Spinnaker's `grab_multiple` has no retry loop, so a `GetNextImage`
  timeout takes this path.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B12. `IMAQdxCamera/blacs_tabs.py:264` (read).**~~ `QtGui.QApplication.instance()` does
  not exist under Qt5 with qtutils 4. The "Copy" button in the attributes dialog raises
  `AttributeError`.
- **B13. `NovaTechDDS9M.py` (read).**
  - Lines 481-492, 513-514, 538-543: responses to table and static programming commands
    are read and discarded with a 0.1 s serial timeout. A rejected line leaves a wrong
    table with no error.
  - Lines 199-205: a dynamic `DDS` on channel 2 or 3 compiles without error, and only
    `raw_output[0]` is used.
  - Line 167: `dds` is unbound when the first connection is out of range.
  - Line 382: `self.phase_mode.decode('utf8')` on a str.
  - Lines 404-410: `except socket.timeout` never triggers for pyserial.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B14. `PrawnBlaster/labscript_devices.py:403-405, 429`, `PrawnDO/labscript_devices.py:288`
  (plausible).**~~ There are no range checks before storing into uint32. A wait timeout or
  PrawnDO interval over 42.9 s (at 100 MHz) wraps when cast.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B15. `PrawnDO/labscript_devices.py:239, 244` (run).**~~
  `hasattr(self, "__intermediate")` is always False because the attribute is name-mangled.
  `set_initial_trigger_time()` on a clockline-triggered PrawnDO is accepted instead of
  raising.
- **B16. TekScope (read).**
  - `blacs_workers.py:68`: `dset.attrs.update(wfmp[ch])` uses the last channel of the loop.
  - `TekScope.py:65`: `datatype='i'` (32-bit) is used for 16-bit transfers.
  - `TekScope.py:143-148`: `reponse`/`response` `NameError` in `get_acquire_state`;
    `set_acquire_state(False)` sends the bare string `'STOP'`.
  - `blacs_workers.py:16-19`, `TekScope.py:156-157`: the assert message is a separate
    statement.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B17. `PhaseMatrixQuickSyn.py:344` (read).**~~ `self.connection.write(b'OUTP:STAT 1')` has
  no `'\r'` terminator, so the gate command in `transition_to_buffered` is not executed.
  `update_reference_out`, `update_blanking` and `update_lock_recovery` are `pass`.
- **B18. AndorSolis (read).** `andor_sdk/andor_utils.py:204`:
  `emccd_gain in self.emccd_gain_range` tests membership in the (low, high) tuple, so only
  the two end values are accepted. `andor_solis.py:160-165`: `EnableKeepCleans(mode)` has
  the body of `GetCurrentCamera`. `andor_solis.py:142-156, 566-571` are stubs that raise
  `NameError`.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B19. `PylonCamera/blacs_workers.py:129, 151` (read).**~~ `raise('Grab Error:', ...)`
  raises a tuple, which gives `TypeError` instead of the grab error.
- **Fixed by labscript-devices PR #155, opened 2026-10-18.** ~~**B20. Smaller items (read).**~~
  - `RFBlaster.py:39`: `wait_day = trigger_delay` is a typo for `wait_delay`.
  - `RFBlaster.py:~440`: the `except` clause does not catch `requests` exceptions, so the
    retry logic cannot run.
  - `PineBlaster.py:121` and `:41`: the parser uses trigger delay 1e-6 and the device uses
    350e-9.
  - `DummyPseudoclock/blacs_workers.py`: no `abort_transition_to_buffered`.
  - `NI_DAQmx/runviewer_parsers.py:76`: connections written as `port1/line0 (PFI0)` never
    match the trace keys.
  - `NI_DAQmx/labscript_devices.py:268`: `self.AI_timebease_rate` typo (harmless).
  - `LightCrafterDMD.py:281, 304`: undefined `time` and `body`.

### Cruft

- **C1. Devices that cannot run on the current stack.**
  - `imaqdx_server.py`: `Dataset.value` (284, 297), `is 'image_path'` (447). Nothing
    references it.
  - `LightCrafterDMD.py`: `ndarray.tostring()` (348, 359) on the normal
    `transition_to_buffered` path.
  - `CiceroOpalKellyXEM3001.py`: still uses `@labscript_device`/`@BLACS_worker` (122, 431).
- **C2. Import-time DLL loading.** `AlazarTechBoard.py:10-14` imports `tqdm` and
  `labscript_devices.atsapi` at module level, and `atsapi.py` (a 1191-line vendored copy)
  loads the ATSApi DLL at import. The labscript class therefore cannot be imported for
  compilation on a machine without the driver. `AndorSolis/andor_sdk/andor_solis.py:20-42`
  likewise loads `atmcd64d.dll` at import.
- **C3. PulseBlaster duplication.** `PulseBlaster_No_DDS.py:70-480` duplicates the tab and
  about 200 lines of worker from `PulseBlaster.py:680-1146`, with small divergences. The
  four variant files use inconsistent parser bases. `ESRPro200` declares
  `clock_limit=200e6`. `pb_core_clock(75)` is hard-coded at `PulseBlaster.py:878` although
  the class has `core_clock_freq`.
- **C4. `PulseBlaster.py:63-102`.** The `profile`/`start_profile`/`stop_profile` machinery
  is dead, yet `@profile` is still applied at 1304 and 1315. Commented-out prints at
  1242-1252, a commented block at 1323-1328, a `print('Wait at ...')` on every runviewer
  load (1256, 1269), and a dead redmine URL in a user-facing error (477).
- **C5. Near-identical pseudoclock code** in `PineBlaster.py`, `DummyPseudoclock/` and
  `PrawnBlaster/`. The `DummyPseudoclock` parser is the `PineBlaster` parser line for line.
- **C6. Deprecated-API leftovers.** `labscript_device`/`BLACS_worker` imports in
  `DummyIntermediateDevice.py:52`, `LightCrafterDMD.py:24` and
  `CiceroOpalKellyXEM3001.py:15`; the 2019 `deprecated_import_alias` shims
  `NI_PCI_6733.py`, `NI_PCIe_6363.py` and `NI_USB_6343.py`; backward-compat branches in
  `NovaTechDDS9M.py:282-292`, `NI_DAQmx/blacs_tabs.py:45-54` and `Camera.py:49-54, 113`.
- **C7. Stale TODOs that mark known-wrong behaviour.** `PrawnDO/labscript_devices.py:112`
  ("trigger_delay ... gets applied twice on waits"); `PulseBlaster.py:1263`;
  `RFBlaster.py:37, 401, 416`; `NovaTechDDS9M.py:559` (abort "untested");
  `NI_DAQmx/blacs_workers.py:472, 481` (manual-mode AI data is acquired continuously and
  discarded).
- **C8. `test_device.py`** registers placeholder classes in the real registry. The
  `*/testing/` directories are connection-table scripts with undefined names, not tests.
- **C9. Packaging.** PyDAQmx, PyNIVision (unmaintained), spinapi, PyVISA, pillow and tqdm
  are hard dependencies for every install. `NI_DAQmx/models/_subclass_template.py` is a
  `string.Template` file with a `.py` extension, which breaks linters and `compileall`.
- **C10. Small copy-paste errors.** `ZaberStageTLSR300B` has description `'T-LSR150D'`;
  bitbucket URLs in `NI_DAQmx/blacs_workers.py:120` and `get_capabilities.py:442`.

Checked and found consistent: the generated NI model files match `capabilities.json` (all
19 models compared programmatically), and the PulseBlaster smart-cache logic.
