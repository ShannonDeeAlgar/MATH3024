#!/usr/bin/env bash
# Full release validation: execute lectures, rebuild slides, audit assets,
# then execute and build the complete Reader in a clean temporary workspace.

set -euo pipefail
cd "$(dirname "$0")"
source "$(pwd)/tools/course_python.sh"

echo "MATH3024 release validation"
echo "Python: $COURSE_PYTHON"
echo

echo "[1/3] Executing lectures and rebuilding slide decks"
./refresh_slides.sh

echo
echo "[2/3] Building and executing the complete Reader"
./build_reader.sh

echo
echo "[3/3] Re-running the teaching-asset audit"
"$COURSE_PYTHON" tools/audit_teaching_assets.py

echo
echo "Validation complete. Reader: $(pwd)/_build/html/index.html"
