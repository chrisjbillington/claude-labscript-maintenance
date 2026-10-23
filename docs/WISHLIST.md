# Feature wishlist

Features that the maintainer may want to consider. None of them is planned or started.
Each entry states the feature and the use case that the maintainer gave for it.

## lyse: multishot routines that request another pass

A multishot routine can report that it has done some of its processing but has more to
do. lyse then runs more single-shot routines if there are shots waiting for them, and
otherwise runs the multishot routines again.

Use case: a multishot routine can do its processing in stages, so its plots update while
it runs, and an error in an early stage shows up sooner.

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

## runmanager: group and output status shown on the tabs

The tab of each globals group shows the status of the group, for example an icon or bold
text if the group has globals with expansions, and red text if a global in the group has
an error. The output tab shows an icon or red text if there was an error.

A group tab already has an exclamation icon while one of its globals fails to evaluate
(`runmanager/__main__.py:798`, runmanager 7e692f4). The output tab has no status
indication.
