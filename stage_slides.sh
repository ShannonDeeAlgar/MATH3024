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

# Fail the build if a Reader slide page and its deployed deck drift apart.
# Reader links are deliberately relative so the same page opens the freshly
# built local deck during preview and the staged deck on GitHub Pages.
for SLIDES_PAGE in notebooks/week*/Slides.md; do
    [[ -f "$SLIDES_PAGE" ]] || continue
    WEEK="$(basename "$(dirname "$SLIDES_PAGE")")"
    EXPECTED_PREFIX="../../slides/$WEEK/"
    LINK="$(sed -n 's/.*href="\([^"]*\.slides\.html\)".*/\1/p' "$SLIDES_PAGE" | head -n 1)"

    if [[ -z "$LINK" || "$LINK" != "$EXPECTED_PREFIX"* ]]; then
        echo "Invalid slide link in $SLIDES_PAGE: ${LINK:-<missing>}" >&2
        echo "Expected a relative link beginning with $EXPECTED_PREFIX" >&2
        exit 1
    fi

    DECK="${LINK##*/}"
    if [[ ! -f "$SITE_ROOT/slides/$WEEK/$DECK" ]]; then
        echo "Slide link target was not staged: $SITE_ROOT/slides/$WEEK/$DECK" >&2
        exit 1
    fi
done
