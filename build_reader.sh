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

# MyST launches the notebook kernel through a command named `python`.
# Some macOS installations provide only `python3`, so expose a private shim
# inside the temporary build rather than requiring students to change their
# system-wide Python installation.
if ! command -v python >/dev/null 2>&1; then
    PYTHON3="$(command -v python3)"
    mkdir -p "$BUILD_ROOT/.bin"
    ln -s "$PYTHON3" "$BUILD_ROOT/.bin/python"
    export PATH="$BUILD_ROOT/.bin:$PATH"
fi

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

# The checked-in slide links deliberately use their full GitHub Pages URLs so
# the published Reader retains the repository prefix (`/MATH3024`) and avoids
# the recurring 404. A local preview must instead open the freshly generated,
# uncommitted decks staged under this local server. Rewrite links only inside
# the temporary build; the working copy and the deployed links are unchanged.
python3 - "$BUILD_ROOT" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
published = "https://shannondeealgar.github.io/MATH3024/slides/"
local = "/slides/"

rewritten = 0
for path in sorted((root / "notebooks").glob("week*/Slides.md")):
    text = path.read_text()
    updated = text.replace(published, local)
    if updated != text:
        path.write_text(updated)
        rewritten += 1

print(f"Repointed {rewritten} slide pages to local preview decks")
PY

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

# Week 9 uses a small self-contained entropy explorer embedded by iframe.
# Raw HTML assets are not always copied by the book builder, so stage it
# explicitly beside the Reader page.
mkdir -p _build/html/notebooks/week09
cp notebooks/week09/entropy_distribution_explorer.html \
    _build/html/notebooks/week09/entropy_distribution_explorer.html

# MyST preserves image URLs used inside raw HTML and notebook Markdown, but it
# does not always copy those files beside the nested Reader route. Keep the
# Week 3 Reader self-contained so its paired concentration-field figures work
# in the local preview and on GitHub Pages.
mkdir -p _build/html/notebooks/week03/l-reaction-diffusion/images
cp -R notebooks/week03/images/. \
    _build/html/notebooks/week03/l-reaction-diffusion/images/
./stage_slides.sh _build/html

echo "Reader ready at: $(pwd)/_build/html/index.html"
