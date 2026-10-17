"""Create a labscript profile with `labscript-profile-create`, point its shared drive at
the work directory and add the runmanager test fixtures to its labscriptlib."""

import configparser
import shutil

from _common import FIXTURES, PROFILE_MARKER, WORK, check, fail, finish, profile_dir, save_state

profile = profile_dir()
print('profile directory:', profile)

from labscript_profile import default_labconfig_path
from labscript_profile.create import create_profile

# A zlock or zlog server started by a previous run keeps running with that run's shared
# secret, so the secret is carried over to the new profile.
old_secret = None
if profile.exists():
    if (profile / PROFILE_MARKER).exists():
        print('removing the profile left by a previous harness run')
        keys = list((profile / 'labconfig').glob('zpsecret-*.key'))
        if keys:
            old_secret = keys[0].read_text()
        shutil.rmtree(profile, ignore_errors=True)
        if profile.exists():
            left = [str(p) for p in profile.rglob('*') if p.is_file()]
            fail(f'could not remove the old profile; files still present: {left}')
            finish()
    else:
        fail(f'{profile} exists and was not created by the harness; move it away first')
        finish()

create_profile()
(profile / PROFILE_MARKER).write_text('')
check(default_labconfig_path().exists(), f'labconfig written to {default_labconfig_path()}')
if old_secret is not None:
    for key in (profile / 'labconfig').glob('zpsecret-*.key'):
        key.write_text(old_secret)
    print('kept the shared secret of the previous profile')

# Shots and the compiled connection table go under the work directory.
shared_drive = WORK / 'shared_drive'
shared_drive.mkdir(parents=True, exist_ok=True)
config = configparser.ConfigParser(interpolation=None)
config.read(default_labconfig_path())
config.set('DEFAULT', 'shared_drive', str(shared_drive))
with open(default_labconfig_path(), 'w') as f:
    config.write(f)

from labscript_utils.labconfig import LabConfig

labconfig = LabConfig()
storage = labconfig.get('DEFAULT', 'experiment_shot_storage')
check(storage.startswith(str(shared_drive)), f'experiment_shot_storage is {storage}')
check(labconfig.get('paths', 'connection_table_py').endswith('connection_table.py'),
      'labconfig names the example connection table')

fixtures = FIXTURES / 'runmanager_test'
dest = profile / 'userlib' / 'labscriptlib' / 'runmanager_test'
shutil.copytree(fixtures, dest)
check((dest / 'experiment.py').exists(), f'runmanager test fixtures copied to {dest}')

save_state(profile=str(profile), labconfig=str(default_labconfig_path()))
finish()
