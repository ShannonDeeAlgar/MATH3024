#!/usr/bin/env bash
# Build the complete Reader from local, uncommitted files and serve it for proofing.
# Usage: ./preview_reader.sh [port]

set -euo pipefail

cd "$(dirname "$0")"
PORT="${1:-8766}"

# The Reader build stages existing .slides.html files but does not create
# them. Regenerate every lecture deck first so the local preview cannot serve
# stale slides after a notebook has changed.
echo "Regenerating lecture slides from the current notebooks..."
for NOTEBOOK in notebooks/week*/L_*.ipynb; do
    [[ -f "$NOTEBOOK" ]] || continue
    ./generate_slides.sh "$NOTEBOOK"
done

./build_reader.sh

echo
echo "Reader preview: http://localhost:$PORT/"
echo "Press Ctrl+C to stop the preview."

python3 -m http.server "$PORT" --directory _build/html &
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
