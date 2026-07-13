#!/usr/bin/env bash
# Generates a reveal.js slide deck from a lecture notebook, excluding cells
# tagged reader-only/slides-only (kept for the Reader, not for slides).
# presenter-notes cells are left alone here: they're handled via
# slide_type=notes and rendered as hidden speaker notes instead.
#
# Usage: ./generate_slides.sh notebooks/week01/L_Introduction_to_complex_systems.ipynb

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <notebook.ipynb>" >&2
    exit 1
fi

jupyter nbconvert --to slides "$1" \
    --TagRemovePreprocessor.enabled=True \
    --TagRemovePreprocessor.remove_cell_tags='["reader-only", "slides-only"]'
