#!/bin/bash
# Check out the integration-testing branch, or master if there is none, in each clone in
# DIR on HOST, at the version on origin.
#
# usage: deploy.sh HOST DIR
set -euo pipefail

ssh "$1" bash -s "$2" <<'END'
set -euo pipefail
cd "$1"
for d in */; do
    d=${d%/}
    [ -d "$d/.git" ] || continue
    if [ -n "$(git -C "$d" status --porcelain --untracked-files=no)" ]; then
        echo "$d: has uncommitted changes, not updated" >&2
        continue
    fi
    git -C "$d" fetch -q --prune origin
    if git -C "$d" rev-parse -q --verify origin/integration-testing > /dev/null; then
        git -C "$d" checkout -q -B integration-testing origin/integration-testing
    else
        git -C "$d" checkout -q master
        git -C "$d" merge -q --ff-only origin/master
        git -C "$d" branch -q -D integration-testing 2> /dev/null || true
    fi
    echo "$d: $(git -C "$d" rev-parse --abbrev-ref HEAD) $(git -C "$d" rev-parse --short HEAD)"
done
END
