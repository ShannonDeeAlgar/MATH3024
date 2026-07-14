#!/usr/bin/env bash
# Serves a slide deck over local HTTP and opens it in the browser.
#
# Opening a .slides.html file directly (file://) breaks YouTube embeds --
# browsers send a null origin for local files, which YouTube's Error 153
# rejects regardless of referrerpolicy. Serving over http:// (even locally)
# fixes this, and also makes reveal.js speaker notes (press 's') sync
# reliably between windows.
#
# Usage: ./present_slides.sh notebooks/week01/L_Introduction_to_complex_systems.slides.html

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <notebook.slides.html>" >&2
    exit 1
fi

FILE="$1"
DIR="$(dirname "$FILE")"
NAME="$(basename "$FILE")"
PORT="${PORT:-8123}"

cd "$DIR"
python3 -m http.server "$PORT" &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null' EXIT

sleep 1
open "http://localhost:$PORT/$NAME"

echo "Serving at http://localhost:$PORT/$NAME -- press Ctrl+C to stop."
wait $SERVER_PID
