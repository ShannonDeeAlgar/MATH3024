#!/usr/bin/env bash
# Copy standalone lecture slides and their local assets into a built Reader.
# Usage: ./stage_slides.sh [site-root]

set -euo pipefail

cd "$(dirname "$0")"
SITE_ROOT="${1:-_build/html}"

# Discover every week containing a rendered lecture deck. This avoids the
# recurring failure where a new week exists but is omitted from deployment.
for SOURCE_ROOT in notebooks/week*; do
    [[ -d "$SOURCE_ROOT" ]] || continue
    compgen -G "$SOURCE_ROOT/L_*.slides.html" >/dev/null || continue

    WEEK="$(basename "$SOURCE_ROOT")"
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
