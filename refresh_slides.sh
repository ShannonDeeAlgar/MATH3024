#!/usr/bin/env bash
# Execute every lecture notebook from a clean kernel and rebuild its deck.
# This is the release path; it deliberately ignores saved notebook outputs.

set -euo pipefail
cd "$(dirname "$0")"
source "$(pwd)/tools/course_python.sh"

for NOTEBOOK in notebooks/week*/L_*.ipynb; do
    [[ -f "$NOTEBOOK" ]] || continue
    ./generate_slides.sh --fresh "$NOTEBOOK"
done

"$COURSE_PYTHON" tools/audit_teaching_assets.py
