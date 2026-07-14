#!/usr/bin/env bash
# Builds the Reader locally for preview, temporarily stripping
# slides-only/presenter-notes cells so the local build matches what CI
# produces. Always restores the real notebooks afterward via git, even if
# the build fails or is interrupted.
#
# Usage: ./build_reader.sh

set -uo pipefail

cd "$(dirname "$0")"

restore() {
    echo "Restoring notebooks/ from git..."
    git checkout -- notebooks/
}
trap restore EXIT

python3 prepare_reader_build.py
jupyter-book build --html --execute
