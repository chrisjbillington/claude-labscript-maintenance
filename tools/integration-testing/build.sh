#!/bin/bash
# Rebuild the integration-testing branch of each component in `branches` and push it to
# the component's origin. Components that have no entry get no integration-testing
# branch, and an existing one is deleted.
#
# usage: build.sh WORKDIR [COMPONENT ...]
#
# Each component is cloned into WORKDIR/COMPONENT from the origin of its clone under
# repos/ (or under $REPOS if set). The clone's rr-cache is rr-cache/COMPONENT in this directory, so that
# recorded conflict resolutions are reused. If a merge has a conflict that has no
# recorded resolution, the script stops with the merge in progress. Resolve it in the
# clone, commit, add the new rr-cache entries to this repository, and run the script
# again.
#
# After the merges, the patches in patches/COMPONENT are applied in name order. They
# adapt one merged branch to another where the merge has no conflict but the result
# needs a change.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repos=$(cd "${REPOS:-$here/../../repos}" && pwd)
work=$1
shift
components=("$@")
if [ ${#components[@]} -eq 0 ]; then
    components=(blacs desktop-app labscript labscript-devices labscript-utils lyse
                qtutils runmanager runviewer zprocess)
fi
mkdir -p "$work"

for c in "${components[@]}"; do
    refs=$(sed 's/#.*//' "$here/branches" | awk -v c="$c" '$1 == c {print $2}')
    url=$(git -C "$repos/$c" remote get-url origin)
    pushurl=$(git -C "$repos/$c" remote get-url --push origin)
    if [ -z "$refs" ]; then
        if git ls-remote --exit-code -q "$url" refs/heads/integration-testing; then
            git push -q "$pushurl" --delete integration-testing
            echo "$c: deleted integration-testing"
        else
            echo "$c: nothing to merge"
        fi
        continue
    fi

    clone=$work/$c
    rm -rf "$clone"
    git clone -q "$url" "$clone"
    mkdir -p "$here/rr-cache/$c"
    ln -s "$here/rr-cache/$c" "$clone/.git/rr-cache"
    git -C "$clone" remote set-url --push origin "$pushurl"
    git -C "$clone" config rerere.enabled true
    git -C "$clone" config rerere.autoUpdate true
    git -C "$clone" config gc.rerereResolved 36500
    git -C "$clone" config user.name Claude
    git -C "$clone" config user.email noreply@anthropic.com
    git -C "$clone" checkout -q -B integration-testing origin/master

    for ref in $refs; do
        if ! git -C "$clone" merge -q --no-ff -m "Merge $ref for integration testing" \
                "origin/$ref" > /dev/null; then
            if [ -n "$(git -C "$clone" diff --name-only --diff-filter=U)" ]; then
                echo "$c: conflict merging $ref in $clone" >&2
                exit 1
            fi
            git -C "$clone" commit -q --no-edit
            echo "$c: merged $ref with a recorded resolution"
        fi
    done
    for patch in "$here/patches/$c"/*.patch; do
        [ -e "$patch" ] || continue
        git -C "$clone" am -q "$patch"
        echo "$c: applied $(basename "$patch")"
    done

    # Push only if master or a merged branch has changed, or the result differs.
    inputs=(origin/master $(printf 'origin/%s ' $refs))
    unchanged=false
    if git -C "$clone" rev-parse -q --verify origin/integration-testing > /dev/null &&
            git -C "$clone" diff --quiet origin/integration-testing HEAD; then
        unchanged=true
        for i in "${inputs[@]}"; do
            git -C "$clone" merge-base --is-ancestor "$i" origin/integration-testing ||
                unchanged=false
        done
    fi
    if $unchanged; then
        echo "$c: integration-testing is up to date"
    else
        git -C "$clone" push -q -f origin integration-testing
        echo "$c: pushed integration-testing $(git -C "$clone" rev-parse --short HEAD)"
    fi
done
