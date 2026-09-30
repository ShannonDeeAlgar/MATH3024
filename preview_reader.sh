#!/usr/bin/env bash
# Build the complete Reader from local, uncommitted files and serve it for proofing.
# Usage: ./preview_reader.sh [port]

set -euo pipefail

cd "$(dirname "$0")"
PORT="${1:-8766}"
source "$(pwd)/tools/course_python.sh"

echo "Using course Python: $COURSE_PYTHON"

# The Reader build stages existing .slides.html files but does not create
# them. Regenerate every lecture deck first so the local preview cannot serve
# stale slides after a notebook has changed.
echo "Regenerating lecture slides from the current notebooks..."
for NOTEBOOK in notebooks/week*/L_*.ipynb; do
    [[ -f "$NOTEBOOK" ]] || continue
    DECK="${NOTEBOOK%.ipynb}.slides.html"
    if [[ ! -f "$DECK" || "$NOTEBOOK" -nt "$DECK" ]]; then
        ./generate_slides.sh --fresh "$NOTEBOOK"
    else
        ./generate_slides.sh "$NOTEBOOK"
    fi
done

"$COURSE_PYTHON" tools/audit_teaching_assets.py

./build_reader.sh

echo
echo "Reader preview: http://localhost:$PORT/"
echo "Press Ctrl+C to stop the preview."

"$COURSE_PYTHON" -m http.server "$PORT" --directory _build/html &
SERVER_PID=$!

cleanup() {
    kill "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Give the local server a moment to begin accepting connections, then open it.
sleep 0.5
if ! open -a "Google Chrome" "http://localhost:$PORT/" 2>/dev/null; then
    open "http://localhost:$PORT/"
fi

wait "$SERVER_PID"
