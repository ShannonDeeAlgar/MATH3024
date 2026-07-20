#!/usr/bin/env bash
# Builds the Reader locally for preview without modifying the working copy.
# A temporary copy of the project is made, slides-only/presenter-notes cells
# are stripped there, and the finished site is copied back to _build/html.
#
# Usage: ./build_reader.sh

set -euo pipefail

cd "$(dirname "$0")"

BUILD_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/math3024-reader.XXXXXX")"
export NPM_CONFIG_CACHE="$BUILD_ROOT/.npm-cache"

cleanup() {
    rm -rf "$BUILD_ROOT"
}
trap cleanup EXIT INT TERM

echo "Preparing a temporary Reader workspace..."
rsync -a \
    --exclude '.git/' \
    --exclude '_build/' \
    --exclude '.jupyter_cache/' \
    --exclude '**/.ipynb_checkpoints/' \
    ./ "$BUILD_ROOT/"

if jupyter-book --version 2>/dev/null | grep -q '^v2\.'; then
    JUPYTER_BOOK=(jupyter-book)
else
    # The Python package named jupyter-book is the legacy v1 application.
    # Jupyter Book 2 is distributed through npm, as in the deploy workflow.
    JUPYTER_BOOK=(npx --yes jupyter-book)
fi

(
    cd "$BUILD_ROOT"
    python3 prepare_reader_build.py
    "${JUPYTER_BOOK[@]}" build --html --execute
)

echo "Copying the completed Reader to _build/html..."
mkdir -p _build
rm -rf _build/html
cp -R "$BUILD_ROOT/_build/html" _build/html

# Local HTML interactives are referenced by Reader pages but are not copied by
# the book builder because they are not Markdown assets.
cp notebooks/week01/interactive_schelling.html \
    _build/html/notebooks/week01/interactive_schelling.html
./stage_slides.sh _build/html

echo "Reader ready at: $(pwd)/_build/html/index.html"
