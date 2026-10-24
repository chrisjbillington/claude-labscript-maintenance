# Engage runmanager's current sequence and wait WAIT seconds, with NLOAD busy processes,
# and with profiling by profile_blacs.py if PROFILE is 1. Prints the per-shot times and
# the CPU time of BLACS, its workers, lyse and runmanager. Run on the lab machine with
# BLACS started as `python $PROF_DIR/profile_blacs.py`, lyse and runmanager running, and
# this directory's scripts in $PROF_DIR:
#
#     ssh HOST bash -s LABEL NLOAD PROFILE WAIT SEQUENCE_PARENT < run_sequence.sh
#
# SEQUENCE_PARENT is the directory that holds the day's sequence directories.
set -u
LABEL=$1; NLOAD=$2; PROF=$3; WAIT=$4; SEQUENCE_PARENT=$5
PROF_DIR=${PROF_DIR:-/tmp/blacsprof}
cd $PROF_DIR
V=~/labscript-suite/dev/.venv/bin
B=$(pgrep -f "^$V/python $PROF_DIR/profile_blacs.py")
cpus() { for p in $B $(pgrep -P $B) $(pgrep -f "^$V/python -m (lyse|runmanager)"); do
  echo "$p $(awk '{print $14+$15}' /proc/$p/stat) $(tr '\0' ' ' < /proc/$p/cmdline | cut -c1-90)"; done; }
LOADPIDS=""
for i in $(seq 1 $NLOAD); do python3 -c "while True: pass" & LOADPIDS="$LOADPIDS $!"; done
sleep 3
cpus > $LABEL.cpu0
[ $PROF = 1 ] && kill -USR1 $B
date +%s.%N > $LABEL.engaged
$V/python -c "import runmanager.remote as r; r.Client().engage()"
sleep $WAIT
[ $PROF = 1 ] && kill -USR2 $B
cpus > $LABEL.cpu1
date +%s.%N > $LABEL.end
[ -n "$LOADPIDS" ] && kill $LOADPIDS
D=$(ls -d $SEQUENCE_PARENT/[0-9]* | tail -1)
echo "$LABEL: $D"
$V/python $PROF_DIR/seqtimes.py $D $LABEL.engaged
python3 - $LABEL <<'PY'
import sys
L=sys.argv[1]
a={l.split()[0]:l.split(None,2) for l in open(L+'.cpu0')}
t=float(open(L+'.end').read())-float(open(L+'.engaged').read())
for l in open(L+'.cpu1'):
    p,c,cmd=l.split(None,2)
    if p in a: print('%6.2f s CPU (%3.0f%%)  %s %s' % ((int(c)-int(a[p][1]))/100, (int(c)-int(a[p][1]))/t, p, cmd.strip()[-60:]))
print('window %.1f s' % t)
PY
ls prof*.txt 2>/dev/null | tail -1
uptime
