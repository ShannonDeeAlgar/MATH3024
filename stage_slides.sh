#!/usr/bin/env bash
# Copy standalone lecture slides and their local assets into a built Reader.
# Usage: ./stage_slides.sh [site-root]

set -euo pipefail

cd "$(dirname "$0")"
SITE_ROOT="${1:-_build/html}"
SLIDE_ROOT="$SITE_ROOT/slides/week01"

mkdir -p "$SLIDE_ROOT"
cp notebooks/week01/L_Introduction_to_complex_systems.slides.html "$SLIDE_ROOT/"
cp notebooks/week01/interactive_schelling.html "$SLIDE_ROOT/"
cp notebooks/week01/simulation2.gif "$SLIDE_ROOT/"
rm -rf "$SLIDE_ROOT/images"
cp -R notebooks/week01/images "$SLIDE_ROOT/images"

echo "Week 1 slides staged at: $SLIDE_ROOT/L_Introduction_to_complex_systems.slides.html"
