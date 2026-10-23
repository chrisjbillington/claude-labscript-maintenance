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

## BLACS: close one worker process without closing BLACS

BLACS can end the worker process of a single device tab while the rest of BLACS keeps
running.

Use case: hardware that only one process at a time can access can be released for
another process to use.

## BLACS: further performance improvements

Look for more places where BLACS can be made faster.

## BLACS: simpler and faster asynchronous architecture

Overhaul the asynchronous architecture of BLACS, if possible, so that it is simpler and
faster.

## BLACS: faster queue handling

Look for performance gains in the way BLACS handles the shot queue.

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
