#!/bin/bash
# Compile the default profile's example experiment and read the shot back with lyse.
# Usage: compile-example.sh <python version> <directory holding the repo clones> <work directory>
# Expects the venv made by install-and-import.sh and a labscript profile (labscript-profile-create).
PY=$1
R=$2
S=$3
export VIRTUAL_ENV=$S/venv$PY PATH=$S/venv$PY/bin:$PATH QT_QPA_PLATFORM=offscreen QT_ENV=PySide6
set -x
echo "=============== labscript compile of the default-profile example"
W=$S/work$PY; rm -rf $W; mkdir -p $W/shots
cp -r $R/labscript-utils/labscript_profile/default_profile/userlib/labscriptlib/example_apparatus $W/example_apparatus
cd $W
python -W default - <<'PYEOF'
import os, sys, warnings
import labscript_utils.h5_lock, h5py
import runmanager
from labscript_utils.labconfig import LabConfig
cfg = LabConfig()
script = os.path.abspath('example_apparatus/example_experiment.py')
h5path = os.path.abspath('shots/test_shot.h5')
sequence_attrs, shot_basename = runmanager.new_sequence_details(script, config=cfg, increment_sequence_index=False)
print('sequence_attrs', sequence_attrs)
runmanager.make_single_run_file(h5path, {}, {}, sequence_attrs, 0, 1)
ok = runmanager.compile_labscript_with_globals_files(script, [], h5path)
print('compile result', ok)
with h5py.File(h5path, 'r') as f:
    print('groups', list(f.keys()))
    print('devices', list(f['devices'].keys()))
    print('connection table rows', len(f['connection table']))
PYEOF
echo "=============== lyse Run API on the compiled shot"
python -W default -c "
import labscript_utils.h5_lock, h5py, lyse, os
r = lyse.Run(os.path.abspath('shots/test_shot.h5'), no_write=True)
print('globals', r.get_globals()); print('ok lyse.Run')
"
echo "=============== done"
