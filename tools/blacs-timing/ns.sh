#!/bin/bash
# Run a command in a mount and network namespace in which $HOME is a directory of
# symlinks to the real home, except labscript-suite, which is a scratch profile. Run
# with unshare -rmn. Only loopback is up, so the zlock and zlog servers that BLACS
# starts are its own and write into the scratch profile. They are killed afterwards.
set -e
S=${BENCH_SCRATCH:?set BENCH_SCRATCH to a scratch directory outside /home}
ip link set lo up
mount --bind $HOME $S/realhome
for e in $S/realhome/* $S/realhome/.[!.]*; do
  n=$(basename "$e")
  [ "$n" = labscript-suite ] && continue
  ln -sfn "$S/realhome/$n" "$S/home/$n"
done
mount --bind $S/home $HOME
set +e
"$@"
status=$?
mine=$(readlink /proc/self/ns/net)
for p in /proc/[0-9]*; do
  pid=${p#/proc/}
  [ "$pid" = "$$" ] && continue
  [ "$(readlink $p/ns/net 2>/dev/null)" = "$mine" ] && kill $pid 2>/dev/null
done
sleep 1
exit $status
