#!/usr/bin/env python3
"""Execute one notebook with visible cell progress and save the result."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def short_label(cell: dict, index: int) -> str:
    source = cell.get("source", "").strip().splitlines()
    first = source[0].strip() if source else "(empty cell)"
    return f"cell {index}: {first[:88]}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--kernel", default="math3024-build")
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()

    notebook = nbformat.read(args.source, as_version=4)
    started: dict[int, float] = {}
    executable = sum(cell.cell_type == "code" for cell in notebook.cells)
    completed = 0

    def on_start(cell=None, cell_index=None, **_kwargs):
        if cell is None or cell.cell_type != "code":
            return
        started[cell_index] = time.monotonic()
        print(f"  [{completed + 1}/{executable}] {short_label(cell, cell_index)}", flush=True)

    def on_complete(cell=None, cell_index=None, **_kwargs):
        nonlocal completed
        if cell is None or cell.cell_type != "code":
            return
        completed += 1
        elapsed = time.monotonic() - started.get(cell_index, time.monotonic())
        print(f"      completed in {elapsed:.1f}s", flush=True)

    client = NotebookClient(
        notebook,
        kernel_name=args.kernel,
        timeout=args.timeout,
        on_cell_start=on_start,
        on_cell_complete=on_complete,
    )
    began = time.monotonic()
    client.execute(cwd=str(args.source.parent.resolve()))
    nbformat.write(notebook, args.output)
    print(f"  executed {executable} code cells in {time.monotonic() - began:.1f}s", flush=True)


if __name__ == "__main__":
    main()
