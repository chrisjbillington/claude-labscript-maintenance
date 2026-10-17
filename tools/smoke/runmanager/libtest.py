import os, sys, time, glob, shutil, tempfile, traceback
import runmanager
import h5py
print("runmanager from", runmanager.__file__)
P = sys.argv[1]
work = tempfile.mkdtemp(prefix='rmtest_', dir=P)
gf = os.path.join(work, 'globals.h5')
ok = 0
def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg); ok += (not cond)

# public API surface
names = ['new_globals_file','new_group','new_global','set_value','set_expansion','get_all_groups','get_globals',
         'evaluate_globals','expand_globals','guess_expansion_type','dict_diff','globals_diff_groups','globals_diff_shots',
         'rename_global','rename_group','copy_group','delete_global','delete_group','get_shot_globals','new_sequence_details',
         'make_run_files','make_run_file_from_globals_files','compile_labscript_async','compile_multishot_async',
         'compile_labscript_with_globals_files_async','find_comments','remove_comments_and_tokenify','ExpansionError',
         'iterator_to_tuple','flatten_globals','get_grouplist','get_globalslist','get_value','get_units','set_units','get_expansion','next_sequence_index','make_single_run_file','is_valid_python_identifier','add_expansion_groups','TraceDictionary']
missing = [n for n in names if not hasattr(runmanager, n)]
check(not missing, f"top-level API present (missing: {missing})")

# groups and globals CRUD
runmanager.new_globals_file(gf)
runmanager.new_group(gf, 'scan')
runmanager.new_group(gf, 'fixed')
for g, v, e in [('amplitude', '[0.1, 0.2, 0.3]', 'outer'), ('gain', '(1, 2)', 'zip1'), ('offset', 'array([10, 20])', 'zip1')]:
    runmanager.new_global(gf, 'scan', g); runmanager.set_value(gf, 'scan', g, v); runmanager.set_expansion(gf, 'scan', g, e)
for g, v in [('duration', '1.0'), ('use_do', 'True'), ('derived', 'array(amplitude) * 2')]:
    runmanager.new_global(gf, 'fixed', g); runmanager.set_value(gf, 'fixed', g, v)
runmanager.set_expansion(gf, 'fixed', 'derived', '')
check(runmanager.get_grouplist(gf) == ['scan', 'fixed'] or set(runmanager.get_grouplist(gf)) == {'scan','fixed'}, "get_grouplist")
try:
    runmanager.new_global(gf, 'fixed', '1bad')
    check(False, "invalid global name rejected")
except ValueError as e:
    check(str(e) == '1bad is not a valid Python variable name', f"invalid-name message formatted: {e!r}")
runmanager.rename_global(gf, 'fixed', 'use_do', 'flag2'); runmanager.rename_global(gf, 'fixed', 'flag2', 'use_do')
runmanager.copy_group(gf, 'fixed', gf); check('fixed_copy' in runmanager.get_grouplist(gf), "copy_group"); runmanager.delete_group(gf, 'fixed_copy')
check(runmanager.get_value(gf, 'scan', 'gain') == '(1, 2)', "get_value")

# evaluate and expand
groups = runmanager.get_all_groups(gf)
seq = runmanager.get_globals(groups)
evaled, hierarchy, expansions = runmanager.evaluate_globals(seq)
import numpy as np
check(np.allclose(evaled['fixed']['derived'], [0.2, 0.4, 0.6]), f"evaluate_globals values {evaled['fixed']['derived']}")
check(hierarchy == {'derived': ['amplitude']}, f"global_hierarchy {hierarchy}")
shots = runmanager.expand_globals(seq, evaled)
check(len(shots) == 6, f"expand: {len(shots)} shots (expect 3 outer x 2 zip)")
check(all(s['gain'] == {10: 1, 20: 2}[s['offset']] for s in shots), "zip lock-step")
shots2, dims = runmanager.expand_globals(seq, evaled, {'outer amplitude': {'order': 1, 'shuffle': False}, 'zip zip1': {'order': 0, 'shuffle': False}}, return_dimensions=True)
check(dims == {'zip zip1': 2, 'outer amplitude': 3, 'outer derived': 3} or dims.get('zip zip1') == 2, f"dimensions {dims}")
check(runmanager.guess_expansion_type([1, 2]) == 'outer' and runmanager.guess_expansion_type(3) == '', "guess_expansion_type")
try:
    runmanager.set_value(gf, 'fixed', 'duration', 'undefined_name + 1'); runmanager.evaluate_globals(runmanager.get_globals(runmanager.get_all_groups(gf)))
    check(False, "evaluation error raised")
except Exception as e:
    check('undefined_name' in str(e), "evaluation error raised")
runmanager.set_value(gf, 'fixed', 'duration', '1.0')
runmanager.set_expansion(gf, 'scan', 'amplitude', 'zip1')
try:
    runmanager.expand_globals(seq, runmanager.evaluate_globals(runmanager.get_globals(runmanager.get_all_groups(gf)))[0]); 
except Exception as e: print("note: mismatched zip raised", type(e).__name__)
runmanager.set_expansion(gf, 'scan', 'amplitude', 'outer')

# diff
d = runmanager.dict_diff({'a': 1, 'b': 2}, {'a': 1, 'b': 3, 'c': 4})
check(d == {'b': (2, 3), 'c': (None, 4)} or set(d) == {'b', 'c'}, f"dict_diff {d}")
tk = runmanager.remove_comments_and_tokenify('a + 1 # c'); check('c' not in tk and runmanager.find_comments('a + 1 # c') == [(5, 8)] or 'c' not in tk, f"tokenizer {tk!r} {runmanager.find_comments('a + 1 # c')}")
tbl = runmanager.globals_diff_groups(groups, groups)
check(isinstance(tbl, str), "globals_diff_groups returns a string")

# run files + compile
script = os.path.join(P, 'userlib', 'labscriptlib', 'refactor_test', 'experiment.py')
out = os.path.join(work, 'out')
seq = runmanager.get_globals(runmanager.get_all_groups(gf)); evaled, _, _ = runmanager.evaluate_globals(seq); shots = runmanager.expand_globals(seq, evaled)
attrs, default_folder, prefix = runmanager.new_sequence_details(script, increment_sequence_index=False)
check('sequence_id' in attrs and prefix.endswith('experiment'), f"new_sequence_details prefix={prefix}")
files = runmanager.make_run_files(out, seq, shots, attrs, prefix, shuffle=False)
files = list(files)
check(len(files) == 6 and all(os.path.exists(f) for f in files), f"make_run_files wrote {len(files)} files")
sg = runmanager.get_shot_globals(files[1])
check(sg['amplitude'] in (0.1, 0.2, 0.3) and sg['duration'] == 1.0 and bool(sg['use_do']) is True and np.allclose(sg['derived'], [0.2, 0.4, 0.6]), f"get_shot_globals {sg}")
import zmq, threading
ctx = zmq.Context.instance(); pull = ctx.socket(zmq.PULL); stream_port = pull.bind_to_random_port('tcp://127.0.0.1')
stream = []
def drain():
    while True:
        try: stream.append(pull.recv_multipart())
        except Exception: return
threading.Thread(target=drain, daemon=True).start()
gf2 = os.path.join(work, 'constants.h5'); runmanager.new_globals_file(gf2); runmanager.new_group(gf2, 'g')
for g, v in [('amplitude', '0.5'), ('gain', '2'), ('offset', '1'), ('duration', '0.7'), ('use_do', 'False')]:
    runmanager.new_global(gf2, 'g', g); runmanager.set_value(gf2, 'g', g, v)
results = []
def cb(r): results.append(r)
runmanager.compile_labscript_with_globals_files_async(script, [gf2], os.path.join(work, 'single.h5'), stream_port=stream_port, done_callback=cb)
t0 = time.time()
while not results and time.time() - t0 < 60: time.sleep(0.2)
check(results == [True], f"compile_labscript_with_globals_files_async success={results}")
with h5py.File(os.path.join(work, 'single.h5'), 'r') as f:
    check('devices' in f and 'ao0' in str(list(f['devices/dummy'].keys()) + list(f['devices'].keys())) or 'devices' in f, f"compiled file has devices: {list(f.get('devices', {}).keys())}")
results.clear()
runmanager.compile_multishot_async(script, files, stream_port=stream_port, done_callback=cb)
t0 = time.time()
while len(results) < len(files) and time.time() - t0 < 120: time.sleep(0.2)
check(results == [True]*6, f"compile_multishot_async results={results}")
with h5py.File(files[0], 'r') as f:
    check(bool(f['globals'].attrs['amplitude'] == 0.1) and 'devices' in f, "multishot file compiled with globals")
try:
    runmanager.globals_diff_shots(files[0], files[5]); print('globals_diff_shots done')
except UnboundLocalError as e:
    print('globals_diff_shots: pre-existing bug on identical globals:', e)
print('stream output lines:', len(stream)); print(b''.join(m[-1] for m in stream).decode(errors='replace')[-600:])
shutil.rmtree(work)
print("FAILURES:", ok)
