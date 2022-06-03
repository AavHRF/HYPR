#!/usr/bin/env bash
set -eo pipefail
CHANGED_FILES=$(git diff --name-only --cached --diff-filter=ACMR)
get_pattern_files() {
    pattern=$(echo "$*" | sed "s/ /\$\\\|/g")
    echo "$CHANGED_FILES" | { grep "$pattern$" || true; }
}
PY_FILES=$(get_pattern_files .py)

if [[ -n "$PY_FILES" ]]
then
    # Run black against changed python files for this commit
    black --check $PY_FILES
    echo "Black run completed, re-commit if necessary"
fi