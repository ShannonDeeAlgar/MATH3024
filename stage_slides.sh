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

    # Keep locally embedded lecture media with the deployed deck. Previously
    # only images were staged, so Week 6's Kuramoto animation worked in the
    # notebook directory but disappeared from the Reader and GitHub Pages.
    if [[ -d "$SOURCE_ROOT/videos" ]]; then
        rm -rf "$SLIDE_ROOT/videos"
        cp -R "$SOURCE_ROOT/videos" "$SLIDE_ROOT/videos"
        # The full Reader can embed the same local media. MyST currently
        # leaves raw HTML video sources unresolved, so stage them beside the
        # generated Reader page as well.
        READER_MEDIA_ROOT="$SITE_ROOT/notebooks/$WEEK/videos"
        mkdir -p "$(dirname "$READER_MEDIA_ROOT")"
        rm -rf "$READER_MEDIA_ROOT"
        cp -R "$SOURCE_ROOT/videos" "$READER_MEDIA_ROOT"
    fi

    if [[ -d "$SOURCE_ROOT/audio" ]]; then
        rm -rf "$SLIDE_ROOT/audio"
        cp -R "$SOURCE_ROOT/audio" "$SLIDE_ROOT/audio"
        READER_AUDIO_ROOT="$SITE_ROOT/notebooks/$WEEK/audio"
        mkdir -p "$(dirname "$READER_AUDIO_ROOT")"
        rm -rf "$READER_AUDIO_ROOT"
        cp -R "$SOURCE_ROOT/audio" "$READER_AUDIO_ROOT"
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
# MyST rewrites source-relative links as domain-root links. On GitHub Pages
# that drops the repository prefix (`/MATH3024`) and produces a 404. Require
# the published address here so a newly added week cannot repeat that failure.
for SLIDES_PAGE in notebooks/week*/Slides.md; do
    [[ -f "$SLIDES_PAGE" ]] || continue
    WEEK="$(basename "$(dirname "$SLIDES_PAGE")")"
    ABSOLUTE_PREFIX="https://shannondeealgar.github.io/MATH3024/slides/$WEEK/"
    LINK="$(sed -n 's/.*href="\([^"]*\.slides\.html\)".*/\1/p' "$SLIDES_PAGE" | head -n 1)"

    if [[ -z "$LINK" ]] || [[ "$LINK" != "$ABSOLUTE_PREFIX"* ]]; then
        echo "Invalid slide link in $SLIDES_PAGE: ${LINK:-<missing>}" >&2
        echo "Expected a link beginning with $ABSOLUTE_PREFIX" >&2
        exit 1
    fi

    DECK="${LINK##*/}"
    if [[ ! -f "$SITE_ROOT/slides/$WEEK/$DECK" ]]; then
        echo "Slide link target was not staged: $SITE_ROOT/slides/$WEEK/$DECK" >&2
        exit 1
    fi
done
