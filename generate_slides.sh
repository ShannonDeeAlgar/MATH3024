#!/usr/bin/env bash
# Generates a reveal.js slide deck from a lecture notebook, excluding cells
# tagged reader-only (kept for the Reader, not for slides) -- slides-only
# cells are exactly the opposite (only for slides) so they must NOT be
# stripped here, and hiding code-cell input/output tagged
# hide-input/hide-output.
# presenter-notes cells are left alone here: they're handled via
# slide_type=notes and rendered as hidden speaker notes instead.
#
# Usage: ./generate_slides.sh [--fresh] notebooks/week01/L_Introduction_to_complex_systems.ipynb

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/tools/course_python.sh"

KERNEL_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/math3024-kernel.XXXXXX")"
course_prepare_kernel "$KERNEL_ROOT"

FRESH=0
if [[ "${1:-}" == "--fresh" ]]; then
    FRESH=1
    shift
fi

if [ $# -eq 0 ]; then
    echo "Usage: $0 [--fresh] <notebook.ipynb>" >&2
    exit 1
fi

SOURCE="$1"
INPUT="$SOURCE"
TEMP_NOTEBOOK=""
cleanup() {
    rm -rf "$KERNEL_ROOT"
    if [[ -n "$TEMP_NOTEBOOK" ]]; then
        rm -f "$TEMP_NOTEBOOK" "${TEMP_NOTEBOOK%.ipynb}.slides.html"
    fi
}
trap cleanup EXIT INT TERM
if [[ "$FRESH" -eq 1 ]]; then
    NOTEBOOK_DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
    NOTEBOOK_NAME="$(basename "$SOURCE" .ipynb)"
    TEMP_NOTEBOOK="$NOTEBOOK_DIR/.${NOTEBOOK_NAME}.fresh.$$.ipynb"
    echo "Executing $(basename "$SOURCE") from a clean kernel..."
    "$COURSE_PYTHON" "$SCRIPT_DIR/tools/execute_notebook.py" \
        "$SOURCE" "$TEMP_NOTEBOOK" \
        --kernel math3024-build \
        --timeout 1200
    INPUT="$TEMP_NOTEBOOK"
fi

"$COURSE_PYTHON" -m nbconvert --to slides "$INPUT" \
    --TagRemovePreprocessor.enabled=True \
    --TagRemovePreprocessor.remove_cell_tags='["reader-only", "archive-only", "remove-cell"]' \
    --TagRemovePreprocessor.remove_input_tags='["hide-input"]' \
    --TagRemovePreprocessor.remove_all_outputs_tags='["hide-output"]' \
    --SlidesExporter.reveal_scroll=True \
    --SlidesExporter.reveal_width=1280 \
    --SlidesExporter.reveal_height=720

# nbconvert's slides output is fully self-contained (no external
# stylesheet), so the Reader's typography and .reader-* component
# styles from style.css never reach it on their own -- inject them
# here, derived from style.css so they can't drift.
slides_html="${INPUT%.ipynb}.slides.html"
target_html="${SOURCE%.ipynb}.slides.html"
if [[ "$slides_html" != "$target_html" ]]; then
    mv "$slides_html" "$target_html"
fi
echo "Injecting shared slide styles into $(basename "$target_html")..."
"$COURSE_PYTHON" "$SCRIPT_DIR/inject_slide_styles.py" "$target_html"
echo "Built $target_html"
