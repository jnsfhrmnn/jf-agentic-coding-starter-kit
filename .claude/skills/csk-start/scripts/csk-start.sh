#!/bin/sh
set -eu

tool_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tool="$tool_dir/csk_start.py"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$tool" "$@"
fi
if command -v python >/dev/null 2>&1; then
    exec python "$tool" "$@"
fi
if command -v py >/dev/null 2>&1; then
    exec py -3 "$tool" "$@"
fi

printf '%s\n' '{"error":"CSK tooling requires Python 3.10+; tried python3, python, and py -3. Start remains read-only."}' >&2
exit 127
