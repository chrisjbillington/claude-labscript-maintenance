# Feature wishlist

Features that the maintainer may want to consider. None of them is planned or started.
Each entry states the feature and the use case that the maintainer gave for it.

## lyse: multishot routines that request another pass

A multishot routine can report that it has done some of its processing but has more to
do. lyse then runs more single-shot routines if there are shots waiting for them, and
otherwise runs the multishot routines again.

Use case: a multishot routine can do its processing in stages, so its plots update while
it runs, and an error in an early stage shows up sooner.

## lyse: lower overhead per shot

Look for performance gains in the overhead of handling each shot in lyse, such as adding
shot files and updating the dataframe.

## runmanager: recently used values for each global

Each global has a drop-down menu that lists the values recently used for that global,
with the date on which each was last used. The list is sorted by "frecency", a
combination of the frequency and the recency of use.

Status: written on runmanager branch `value-history` (2e41aa5), with comments drawn in
grey in the value cells and the editor. A value is recorded when the first shot of a
sequence compiles. The list shows the current value, then the most recently used other
value, then pinned values, then the rest by a score that counts at most one use per hour
and halves in a week; it keeps 20 values per global. Values that differ only in comments
or whitespace are one entry. The history is a `history` subgroup of each globals group,
with one fixed-length JSON attribute per global, which does not grow the file
(`DEFECTS.md` D37). No pull request is open.

## BLACS: close one worker process without closing BLACS

BLACS can end the worker process of a single device tab while the rest of BLACS keeps
running.

Use case: hardware that only one process at a time can access can be released for
another process to use.

## BLACS: further performance improvements

Look for more places where BLACS can be made faster.

## BLACS: faster queue handling

Look for performance gains in the way BLACS handles the shot queue.

Status: an experimental rewrite is on blacs branch `queue-main-thread`
(`BLACS-QUEUE.md`).

## BLACS: profile shot cycle time under load

Profile BLACS while the system is under load and find the sources of the extra delay in
the shot cycle time that the load causes. Some of the delay is unavoidable, but general
performance improvements may reduce the delay under load substantially.

## runmanager: group and output status shown on the tabs

The tab of each globals group shows the status of the group, for example an icon or bold
text if the group has globals with expansions, and red text if a global in the group has
an error. The output tab shows an icon or red text if there was an error.

A group tab already has an exclamation icon while one of its globals fails to evaluate
(`runmanager/__main__.py:798`, runmanager 7e692f4). The output tab has no status
indication.

## All applications: desktop-app functionality on macOS

`desktop-app install` and the applications themselves give BLACS, runmanager, lyse and
runviewer the same desktop integration on macOS as on Windows and Linux: an application
bundle with the correct name and icon, and a Dock icon and application name for the
running process.

desktop-app master (c8498cf) creates `.app` bundles in `~/Applications`
(`desktop_app/macos.py:29`, from desktop-app #29) and reads `short_display_name` from
`desktop-app.json` (`desktop_app/shell.py:65`). `set_process_appid`
(`desktop_app/shell.py:184`) does nothing on macOS. The four applications set no
`short_display_name` in their `desktop-app.json`, and the splash screen takes the Qt
application name from `sys.argv` (`labscript_utils/splash.py:55`, labscript-utils
e5cd210). The closed pull requests that would have changed the applications are listed
in section 6 of `RELEASE-PLAN.md` (labscript-utils #124, blacs #122, runmanager
#129, runviewer #72, lyse #138). An application started from its entry point script in
a macOS venv does not see the venv until desktop-app #35 is merged (`DEFECTS.md` D19).

## All repositories: consolidate duplicated functionality

Find functionality that is implemented more than once across the suite, within one
repository or in several, and replace the copies with one implementation, for example
in labscript-utils.

## All repositories: modern string handling in HDF5 files

Go through the suite and change every place that writes strings to HDF5 files, or reads
them, to the current h5py idioms: `h5py.string_dtype()` for variable-length UTF-8
strings, and `.asstr()` or `Dataset.asstr()[...]` for reading. Shot files, globals files
and connection tables written by older versions, which hold fixed-length or ASCII byte
strings, must stay readable.

The suite converts bytes to `str` after reading with a function `_ensure_str`, which is
defined four times: `labscript_utils/connections.py:24` (labscript-utils a9dbff7, also
imported by `lyse/dataframe_utilities.py:24`, lyse 3edf99c),
`runmanager/group_manager.py:29` (runmanager adc9777) and
`blacs/front_panel_settings.py:26` and `blacs/plugins/progress_bar/__init__.py:44`
(blacs c0c2322). labscript writes with `h5py.special_dtype(vlen=str)`
(`labscript/labscript.py:267`, labscript 33cdb31). labscript-devices has about 25 more
sites that use NumPy byte-string dtypes or similar.
