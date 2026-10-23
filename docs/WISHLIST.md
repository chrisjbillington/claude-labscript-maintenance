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
