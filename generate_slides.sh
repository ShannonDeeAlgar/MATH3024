#!/usr/bin/env bash
# Generates a reveal.js slide deck from a lecture notebook, excluding cells
# tagged reader-only (kept for the Reader, not for slides) -- slides-only
# cells are exactly the opposite (only for slides) so they must NOT be
# stripped here, and hiding code-cell input/output tagged
# hide-input/hide-output.
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
    --TagRemovePreprocessor.remove_cell_tags='["reader-only", "archive-only"]' \
    --TagRemovePreprocessor.remove_input_tags='["hide-input"]' \
    --TagRemovePreprocessor.remove_all_outputs_tags='["hide-output"]' \
    --SlidesExporter.reveal_scroll=True \
    --SlidesExporter.reveal_width=1280 \
    --SlidesExporter.reveal_height=720

# nbconvert's slides output is fully self-contained (no external
# stylesheet), so the Reader's typography and .reader-* component
# styles from style.css never reach it on their own -- inject them
# here, derived from style.css so they can't drift.
slides_html="${1%.ipynb}.slides.html"
python3 "$(dirname "$0")/inject_slide_styles.py" "$slides_html"
