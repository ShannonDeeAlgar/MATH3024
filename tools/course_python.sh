#!/usr/bin/env bash
# Resolve the Python runtime used for every executable teaching asset.
#
# Source this file from build scripts, then use $COURSE_PYTHON rather than a
# bare `python`/`python3`.  MATH3024_PYTHON remains an explicit override for
# another machine or CI runner.

set -euo pipefail

_course_python_has_build_stack() {
    "$1" -c 'import IPython, ipykernel, ipywidgets, matplotlib, nbconvert, numpy, PIL, tqdm' \
        >/dev/null 2>&1
}

_course_python_candidates=()
if [[ -n "${MATH3024_PYTHON:-}" ]]; then
    _course_python_candidates+=("$MATH3024_PYTHON")
fi
if [[ -n "${CONDA_PREFIX:-}" ]]; then
    _course_python_candidates+=("$CONDA_PREFIX/bin/python")
fi
_course_python_candidates+=(
    "/opt/miniconda3/envs/math3024/bin/python"
    "$(command -v python3 2>/dev/null || true)"
)

COURSE_PYTHON=""
for _candidate in "${_course_python_candidates[@]}"; do
    [[ -n "$_candidate" && -x "$_candidate" ]] || continue
    if _course_python_has_build_stack "$_candidate"; then
        COURSE_PYTHON="$_candidate"
        break
    fi
done

if [[ -z "$COURSE_PYTHON" ]]; then
    cat >&2 <<'EOF'
Could not find a Python environment containing the MATH3024 build stack.

Activate the course environment, or set MATH3024_PYTHON to its Python binary.
The required packages are listed in requirements.txt.
EOF
    return 1 2>/dev/null || exit 1
fi

export COURSE_PYTHON

# Matplotlib otherwise attempts to write to ~/.matplotlib during clean builds.
export MPLCONFIGDIR="${MPLCONFIGDIR:-${TMPDIR:-/tmp}/math3024-matplotlib-cache}"
mkdir -p "$MPLCONFIGDIR"

course_prepare_kernel() {
    local root="$1"
    local kernel_dir="$root/kernels/math3024-build"
    mkdir -p "$kernel_dir"
    "$COURSE_PYTHON" - "$kernel_dir/kernel.json" <<'PY'
import json
from pathlib import Path
import sys

target = Path(sys.argv[1])
target.write_text(json.dumps({
    "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
    "display_name": "MATH3024 build kernel",
    "language": "python",
    "metadata": {"debugger": False},
}, indent=2))
PY
    export JUPYTER_PATH="$root${JUPYTER_PATH:+:$JUPYTER_PATH}"
}

