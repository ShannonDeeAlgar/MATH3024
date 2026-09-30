#!/usr/bin/env python3
"""Audit notebooks and generated decks before preview or release.

The checks here are deliberately conservative.  They catch invalid notebooks,
saved execution failures, stale slide decks, heading drift, and slides likely
to overflow.  The final visual fit check remains a human proofing task.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.M)
TAG_RE = re.compile(r"<[^>]+>")


def clean_heading(value: str) -> str:
    value = re.sub(r"\{[^}]*\}\s*$", "", value)
    value = re.sub(r"[*_`]+", "", value)
    return " ".join(value.strip().split())


def headings(nb: dict, destination: str) -> set[str]:
    found: set[str] = set()
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        tags = set(cell.get("metadata", {}).get("tags", []))
        if destination == "reader" and tags & {"slides-only", "presenter-notes", "archive-only"}:
            continue
        if destination == "slides" and tags & {"reader-only", "archive-only"}:
            continue
        if destination == "shared" and tags & {
            "slides-only",
            "reader-only",
            "presenter-notes",
            "archive-only",
        }:
            continue
        for _, value in HEADING.findall("".join(cell.get("source", []))):
            found.add(clean_heading(value))
    return found


def slide_blocks(nb: dict) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    title = "(untitled slide)"
    body: list[str] = []
    for cell in nb.get("cells", []):
        tags = set(cell.get("metadata", {}).get("tags", []))
        if tags & {"reader-only", "archive-only", "presenter-notes"}:
            continue
        slide_type = cell.get("metadata", {}).get("slideshow", {}).get("slide_type", "")
        if slide_type == "skip":
            continue
        if slide_type in {"slide", "subslide"} and body:
            blocks.append((title, "\n".join(body)))
            title, body = "(untitled slide)", []
        source = "".join(cell.get("source", []))
        match = HEADING.search(source) if cell.get("cell_type") == "markdown" else None
        if match and title == "(untitled slide)":
            title = clean_heading(match.group(2))
        body.append(source)
    if body:
        blocks.append((title, "\n".join(body)))
    return blocks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="fail on warnings as well as errors")
    args = parser.parse_args()
    errors: list[str] = []
    warnings: list[str] = []

    for path in sorted((ROOT / "tools").glob("*.py")):
        source = path.read_text()
        # ``rebuild_*`` scripts contain notebook source as strings; their
        # resulting notebooks are checked below instead of treating the
        # template itself as a directly executed animation generator.
        if (
            not path.name.startswith("rebuild_")
            and "FuncAnimation" in source
            and "animation = FuncAnimation" in source
        ):
            if "apply_course_figure_style" not in source:
                errors.append(
                    f"{path.relative_to(ROOT)}: animation generator does not apply shared figure style"
                )
            if "style_animation_frame" not in source:
                errors.append(
                    f"{path.relative_to(ROOT)}: animation callback does not reapply shared frame style"
                )

    for path in sorted((ROOT / "notebooks").glob("week*/*.ipynb")):
        try:
            nb = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid notebook JSON ({exc})")
            continue
        # Historical source notebooks remain in the repository for comparison,
        # but only the current lecture/workshop notebooks are release assets.
        is_release_notebook = path.name.startswith(("L_", "WS_")) or path.name == "Getting_Started.ipynb"
        if is_release_notebook:
            for cell in nb.get("cells", []):
                for output in cell.get("outputs", []):
                    if output.get("output_type") == "error":
                        warnings.append(
                            f"{path.relative_to(ROOT)}: saved error output {output.get('ename', '')}"
                        )

        if path.name.startswith("WS_"):
            sources = ["".join(cell.get("source", [])) for cell in nb.get("cells", [])]
            has_student_animation = any(
                re.search(r"def\s+simple(?:_\w+)*_animation\s*\(", source)
                for source in sources
            )
            polished_cells = []
            for cell, source in zip(nb.get("cells", []), sources):
                if "<canvas" in source and "<script" in source:
                    polished_cells.append(cell)
                    tags = set(cell.get("metadata", {}).get("tags", []))
                    if "hide-input" not in tags:
                        errors.append(
                            f"{path.relative_to(ROOT)}: polished HTML player cell "
                            f"'{cell.get('id', 'unknown')}' must be tagged hide-input"
                        )
            if polished_cells and not has_student_animation:
                errors.append(
                    f"{path.relative_to(ROOT)}: polished player has no simple student animation alternative"
                )

        if path.name.startswith("L_"):
            reader = headings(nb, "reader")
            shared = headings(nb, "shared")
            missing_shared = shared - reader
            if missing_shared:
                errors.append(
                    f"{path.relative_to(ROOT)}: shared headings missing from Reader: "
                    + "; ".join(sorted(missing_shared))
                )
            html = path.with_suffix(".slides.html")
            if not html.exists():
                errors.append(f"{path.relative_to(ROOT)}: generated slide deck is missing")
            elif html.stat().st_mtime < path.stat().st_mtime:
                warnings.append(f"{html.relative_to(ROOT)}: older than its notebook")

            for title, source in slide_blocks(nb):
                plain = TAG_RE.sub(" ", source)
                words = len(re.findall(r"\b\w+\b", plain))
                images = len(re.findall(r"!\[|<img\b|<iframe\b", source, re.I))
                tables = source.count("|") >= 8
                if words > 145 or (words > 95 and images) or (words > 105 and tables):
                    warnings.append(
                        f"{path.relative_to(ROOT)}: visual fit check needed for '{title}' "
                        f"({words} words, {images} media items)"
                    )

    print("Teaching asset audit")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN:  {item}")
    print(f"{len(errors)} errors; {len(warnings)} warnings")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
