# Upstream bug reports and pull requests

Bugs and fixes in projects outside the labscript suite that affect the suite, with their
state. A session that files, drafts or sees one closed updates the row. Drafts that the
maintainer has not posted yet are under "Drafts" below.

## Open

| Filed | Project | Report or pull request | Effect on the suite | Our record |
|---|---|---|---|---|
| 2026-10-24 | h5py | [h5py #3008](https://github.com/h5py/h5py/pull/3008), pull request: build the extension modules with optimization in Linux wheels | Since h5py 3.13.0 the Linux wheels build their Cython extensions with `-g1` and no `-O`, so small HDF5 operations (opening a file, reading an attribute) take about 1.5 times as long | `TESTING.md`, "h5py Linux wheels build their extension modules without optimisation" |
| 2026-10-24 | pyzmq | [pyzmq #2227](https://github.com/zeromq/pyzmq/issues/2227), issue: large CURVE performance penalty on Linux due to unoptimised libsodium build | The pyzmq Linux wheels build libsodium (and libzmq) without `-O`, so CURVE encryption, which the suite uses for every ZMQ connection when a shared secret is set, is about ten times slower | `TESTING.md`, "pyzmq Linux wheels build libsodium without optimisation" |
| not filed | PySide6 | Draft below: crash in `QStandardItemModel.clear()` after `horizontalHeaderItem()` | lyse crashes when routines add columns (the Edit columns dialog), on every Python version | `DEFECTS.md` D39 |
| not filed | PySide6 | Draft below: calls that return `None` decrement the reference count of `None` on Python 3.11 | Every suite application with PySide6 6.12.0 on Python 3.10 or 3.11 aborts eventually | `DEFECTS.md` D42 |

## Closed

| Filed | Project | Report or pull request | State | Our record |
|---|---|---|---|---|

## Drafts

Both PySide drafts are for the Qt bug tracker, https://bugreports.qt.io, project "Qt for
Python" (PYSIDE), component PySide, affects version 6.12.0. Both reproducers were run on
2026-10-24 on Arch Linux x86_64 with the PyPI wheels of PySide6-Essentials, in uv venvs.

### PySide6: crash in QStandardItemModel.clear() after horizontalHeaderItem()

**Title:** Crash in QStandardItemModel.clear() after retrieving a header item created by
setHorizontalHeaderLabels() (regression in 6.12.0)

**Description:**

Disclosure: Claude (Anthropic's AI model) found and narrowed down this bug and wrote this
report. I've run the reproducer myself and it crashes for me as described.

Since 6.12.0, our application crashes in `QStandardItemModel.clear()` when the model is
repeatedly cleared and repopulated, and something has called `horizontalHeaderItem()` on
one of the header items. The crash is a segfault in
`Shiboken::BindingManager::unregisterWrapper`, called from `QStandardItem::~QStandardItem`.
Sometimes glibc aborts with `malloc(): unaligned tcache chunk detected` or
`malloc_consolidate(): unaligned fastbin chunk detected` instead. It happens in lyse, part
of the labscript suite, whose dialog for choosing visible columns is rebuilt this way each
time a column is added.

This reproduces it:

```python
from PySide6.QtGui import QStandardItem, QStandardItemModel

model = QStandardItemModel()
for i in range(300):
    model.clear()
    model.setHorizontalHeaderLabels(['a', 'b'])
    model.horizontalHeaderItem(0)
    for j in range(i):
        model.appendRow([QStandardItem(), QStandardItem()])
    print(i, end=' ', flush=True)
print('\nno crash')
```

On 6.12.0 it crashes every time, for me at iteration 167 on Python 3.12 and at iteration
69 on Python 3.14. On 6.8.3, 6.9.3, 6.10.2, 6.11.0 and 6.11.2 it prints "no crash". Without
the `horizontalHeaderItem(0)` line it doesn't crash on 6.12.0 either.

As far as I can tell, the wrapper that `horizontalHeaderItem()` returns is kept alive by
the model, and is never invalidated when `clear()` deletes the C++ item, since the item
was created on the C++ side. `Shiboken.isValid()` on it still returns True after
`clear()`, and that's the same on 6.11.2. So the stale wrapper isn't new, but on 6.12.0
something now trips over it. My guess, which I haven't checked, is that it's related to
the change for PYSIDE-3365 (commit 50ab3a831), which stopped `clear()` from taking the rows
and releasing their wrappers itself before Qt deletes them.

Environment: Linux x86_64 (Arch), Python 3.12.14 and 3.14.8, PySide6-Essentials 6.12.0
from PyPI. I've seen the crash on GitHub Actions Ubuntu runners as well. I haven't run
the reproducer on Windows or macOS.

### PySide6: None's reference count decremented on Python 3.11

**Title:** Calling a method that returns None decrements the reference count of None on
Python 3.10/3.11, leading to "deallocating None" (6.12.0)

**Description:**

Disclosure: Claude (Anthropic's AI model) found and narrowed down this bug and wrote this
report. I've run the reproducer myself and it behaves as described.

With 6.12.0 on Python 3.11, every call of a PySide6 method that returns `None` seems to
decrement the reference count of `None` without having incremented it. Once the count
reaches zero, Python aborts with:

```
Fatal Python error: none_dealloc: deallocating None: bug likely caused by a refcount error in a C extension
```

This shows it:

```python
import sys
from PySide6.QtCore import QObject

obj = QObject()
before = sys.getrefcount(None)
for i in range(1000):
    obj.setObjectName('x')
print('change in refcount of None:', sys.getrefcount(None) - before, flush=True)

# Keep going until None is deallocated:
while True:
    obj.setObjectName('x')
```

On 6.12.0 with Python 3.11.17 it prints `change in refcount of None: -1000` and then
aborts with the error above. On 6.11.2 with the same Python it prints -1 (the change from
the loop variable and so on) and runs until it's killed. It isn't specific to
`setObjectName`: `QWidget.setEnabled`, `QStandardItemModel.clear`,
`QStandardItemModel.setHorizontalHeaderLabels` and `QStandardItem.setData` all do the
same thing, one decrement per call.

On Python 3.12 and later `None` is immortal, so I assume that's why it hasn't been
noticed. But the 6.12.0 wheels are `cp310-abi3` and declare `Requires-Python >=3.10`, so
pip installs them on 3.10 and 3.11, and there any long-running application aborts
eventually. We hit it in our GUI applications on Ubuntu with Python 3.11. I've only tested
3.11; I'd expect 3.10 to be the same.

Environment: Linux x86_64 (Arch), Python 3.11.17 (uv's standalone build),
PySide6-Essentials 6.12.0 from PyPI. I've seen the abort on GitHub Actions Ubuntu runners
with Python 3.11 as well.
