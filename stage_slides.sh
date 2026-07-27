#!/usr/bin/env bash
# Copy standalone lecture slides and their local assets into a built Reader.
# Usage: ./stage_slides.sh [site-root]

set -euo pipefail

cd "$(dirname "$0")"
SITE_ROOT="${1:-_build/html}"
for WEEK in week01 week02 week03 week04 week05 week06; do
    SOURCE_ROOT="notebooks/$WEEK"
    SLIDE_ROOT="$SITE_ROOT/slides/$WEEK"

    mkdir -p "$SLIDE_ROOT"
    find "$SOURCE_ROOT" -maxdepth 1 -name 'L_*.slides.html' -exec cp {} "$SLIDE_ROOT/" \;

    if [[ -d "$SOURCE_ROOT/images" ]]; then
        rm -rf "$SLIDE_ROOT/images"
        cp -R "$SOURCE_ROOT/images" "$SLIDE_ROOT/images"
    fi

    # Week 1 uses this local interactive from within the slide deck.
    if [[ -f "$SOURCE_ROOT/interactive_schelling.html" ]]; then
        cp "$SOURCE_ROOT/interactive_schelling.html" "$SLIDE_ROOT/"
        # Reader pages resolve the same interactive beside their generated
        # week directory. MyST does not copy loose HTML assets itself.
        mkdir -p "$SITE_ROOT/notebooks/$WEEK"
        cp "$SOURCE_ROOT/interactive_schelling.html" \
            "$SITE_ROOT/notebooks/$WEEK/interactive_schelling.html"
    fi
    if [[ -f "$SOURCE_ROOT/simulation2.gif" ]]; then
        cp "$SOURCE_ROOT/simulation2.gif" "$SLIDE_ROOT/"
    fi

    echo "Slides staged for $WEEK at: $SLIDE_ROOT"
done
