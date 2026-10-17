import sys, time, os, glob, inspect
import runmanager
import h5py
from runmanager.remote import Client
P = sys.argv[1]
fails = 0
def check(cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + msg); fails += (not cond)
sig = inspect.signature(Client.__init__); print("Client signature:", sig)
kw = {}
if 'host' in sig.parameters: kw['host'] = 'localhost'
if 'port' in sig.parameters: kw['port'] = 42623
if 'timeout' in sig.parameters: kw['timeout'] = 15
c = Client(**kw)
for i in range(240):
    try:
        c.say_hello(); break
    except Exception as e:
        err = e; time.sleep(0.5)
else:
    sys.exit(f"runmanager did not start: {err}")
print("started after", i*0.5, "s; version", c.get_version())
check(c.get_labscript_file().endswith('experiment.py'), f"labscript file {c.get_labscript_file()}")
for i in range(120):
    try:
        n = c.n_shots(); break
    except Exception as e:
        err = e; time.sleep(0.5)
else:
    sys.exit(f"n_shots never answered: {err}")
check(n == 6, f"n_shots = {n}")
g = c.get_globals()
check(g['duration'] == 1.0 and list(g['amplitude']) == [0.1, 0.2, 0.3] and g['gain'] == (1, 2), f"get_globals {g}")
raw = c.get_globals(raw=True)
check(raw['derived'] == 'array(amplitude) * 2', f"get_globals raw {raw}")
check(c.error_in_globals() is False, "no error in globals")
c.set_globals({'duration': 0.8})
check(c.get_globals()['duration'] == 0.8, "set_globals evaluated")
c.set_globals({'duration': 'undefined_x + 1'}, raw=True)
check(c.error_in_globals() is True, "error_in_globals after bad expression")
c.set_globals({'duration': 0.8})
check(c.error_in_globals() is False and c.n_shots() == 6, "recovered from bad expression")
check(c.get_shuffle() is False, "shuffle off"); c.set_shuffle(True); check(c.get_shuffle() is True, "shuffle on"); c.set_shuffle(False)
check(c.get_run_shots() is False and c.get_view_shots() is False, "run/view shots off")
check(c.is_output_folder_default() is True, "default output folder")
folder = c.get_shot_output_folder(); print("output folder:", folder)
c.engage()
t0 = time.time(); done = 0
while time.time() - t0 < 180:
    files = sorted(glob.glob(os.path.join(folder, '*.h5')))
    done = 0
    for f in files:
        try:
            with h5py.File(f, 'r') as h:
                done += ('devices' in h and 'dummy' in h['devices'] and len(h['devices/dummy'].keys()) > 0)
        except OSError:
            pass
    if done == 6: break
    time.sleep(1)
check(done == 6 and len(files) == 6, f"engage compiled {done}/{len(files)} shots in {time.time()-t0:.0f}s")
if files:
    with h5py.File(files[0], 'r') as h:
        ga = dict(h['globals'].attrs)
        check(ga['duration'] == 0.8 and ga['amplitude'] in (0.1, 0.2, 0.3), f"shot globals {ga}")
        print("devices:", list(h['devices'].keys()), "dummy tables:", list(h['devices/dummy'].keys()))
check(c.is_output_folder_default() is True and c.get_shot_output_folder() != folder, f"sequence index advanced: {c.get_shot_output_folder()}")
c.set_shot_output_folder(os.path.join(P, 'gui', 'custom_out')); check(c.is_output_folder_default() is False, "custom output folder"); c.reset_shot_output_folder(); check(c.is_output_folder_default() is True, "reset output folder")
c.set_globals({'duration': 1.0})
print("FAILURES:", fails)
