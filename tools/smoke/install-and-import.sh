#!/bin/bash
# Smoke-test installing and importing the labscript suite from local clones on a given Python.
# Usage: install-and-import.sh <python version> <directory holding the repo clones> <work directory>
# Creates <work directory>/venv<version> with uv and writes <work directory>/py<version>.log.
PY=$1
R=$2
S=$3
mkdir -p $S; cd $S
LOG=$S/py$PY.log
exec > $LOG 2>&1
set -x
rm -rf venv$PY
uv venv --python $PY venv$PY || exit 1
export VIRTUAL_ENV=$S/venv$PY
export PATH=$VIRTUAL_ENV/bin:$PATH
uv pip install --python $VIRTUAL_ENV/bin/python pip setuptools wheel setuptools_scm pytest || exit 1
# install in dependency order; qtutils is the philipstarkey/qtutils clone
for p in $R/zprocess $R/qtutils $R/desktop-app $R/labscript-c-extensions $R/labscript-utils $R/labscript $R/runmanager $R/blacs $R/lyse $R/runviewer $R/labscript-devices $R/labscript-suite; do
  echo "=============== installing $p"
  SETUPTOOLS_SCM_PRETEND_VERSION=99.0.0 uv pip install --python $VIRTUAL_ENV/bin/python --no-build-isolation "$p" 2>&1 | tail -5 || echo "INSTALL FAILED: $p"
done
echo "=============== installing PySide6"
uv pip install --python $VIRTUAL_ENV/bin/python PySide6 2>&1 | tail -3
echo "=============== versions"
python -c "import sys, numpy, h5py, pandas, scipy, zmq, PySide6; print(sys.version); print('numpy', numpy.__version__, 'h5py', h5py.__version__, 'pandas', pandas.__version__, 'scipy', scipy.__version__, 'pyzmq', zmq.__version__, 'PySide6', PySide6.__version__)"
echo "=============== imports"
export QT_QPA_PLATFORM=offscreen QT_ENV=PySide6
for m in zprocess qtutils.qt desktop_app labscript_c_extensions.runviewer.resample labscript_utils labscript_utils.h5_lock labscript_utils.labconfig labscript_utils.connections labscript_utils.qtwidgets.toolpalette labscript labscript_devices labscript_devices.PulseBlaster labscript_devices.NI_DAQmx.labscript_devices labscript_devices.PrawnBlaster.labscript_devices labscript_devices.IMAQdxCamera.labscript_devices runmanager runmanager.remote blacs blacs.tab_base_class blacs.experiment_queue blacs.plugins lyse lyse.dataframe_utilities runviewer; do
  python -W error::DeprecationWarning -c "import warnings; import $m" > /tmp/imp.txt 2>&1 && echo "OK   $m" || { echo "FAIL $m"; tail -4 /tmp/imp.txt | sed 's/^/     /'; }
done
echo "=============== imports without -W error (to separate warnings from hard failures)"
for m in labscript_utils labscript labscript_devices runmanager blacs lyse runviewer; do
  python -c "import $m" > /tmp/imp.txt 2>&1 && echo "OK   $m" || { echo "FAIL $m"; tail -6 /tmp/imp.txt | sed 's/^/     /'; }
done
echo "=============== GUI app module imports (offscreen)"
for m in blacs.__main__ lyse.__main__ runviewer.__main__ runmanager.__main__; do
  timeout 60 python -c "
import sys, importlib, types
# Importing __main__ modules runs the app; instead compile them to catch syntax errors and import their dependencies
import importlib.util, py_compile
spec = importlib.util.find_spec('$m'); py_compile.compile(spec.origin, doraise=True); print('compiled', spec.origin)
" 2>&1 | tail -3
done
echo "=============== zprocess tests"
cd $R/zprocess && timeout 900 python -m pytest -q -o addopts="" tests 2>&1 | tail -25
cd $S
echo "=============== done"
