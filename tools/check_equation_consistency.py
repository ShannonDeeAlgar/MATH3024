#!/usr/bin/env python3
"""Check audited reader/slide mathematics before either build.

Reader cells are canonical. Exact duplicate displays must agree; deliberately
shortened derivations carry a reviewed source reference. Inline mathematics is
also fingerprinted so notation changes cannot silently bypass the check.
This checks consistency, not mathematical truth.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools/equation_consistency.json"
DISPLAY = re.compile(r"\$\$(.*?)\$\$", re.S)
REFERENCE = re.compile(r"<!-- reader-equation: ([\w-]+):(\d+) -->")
MATH = re.compile(
    r"\$\$(.*?)\$\$|(?<!\\)\$(?!\$)(.*?)(?<!\\)\$"
    r"|\\\[(.*?)\\\]|\\\((.*?)\\\)|\{math\}\x60([^\x60]+)\x60", re.S)


def normalise(s):
    return re.sub(r"\s+", "", s)


def math_signature(source):
    # Code examples are literal; MyST containers (dropdowns, notes, etc.)
    # contain teaching mathematics and must remain in the audit.
    kept, fences = [], []
    for line in source.splitlines(keepends=True):
        fence = re.match(r"^\s*([`~]{3,})(.*)$", line)
        literal = bool(fences and fences[-1][1])
        if fence:
            marker, info = fence.groups()
            if fences and not info.strip() and marker[0] == fences[-1][0][0] and len(marker) >= len(fences[-1][0]):
                fences.pop()
            elif not literal:
                fences.append((marker, not info.lstrip().startswith('{')))
            if literal or (fences and fences[-1][1]):
                continue
        elif literal:
            continue
        kept.append(line)
    source = ''.join(kept)
    values = [normalise(next(g for g in m.groups() if g is not None))
              for m in MATH.finditer(source)]
    values += [normalise(m[1]) for m in
               re.finditer(r"\x60{3}\{math\}[^\n]*\n(.*?)\x60{3}", source, re.S)]
    return hashlib.sha256(json.dumps(values).encode()).hexdigest() if values else None


def load_cells(path):
    return {c["id"]: c for c in json.loads(path.read_text())["cells"]
            if c["cell_type"] == "markdown"
            and not set(c.get("metadata", {}).get("tags", []))
            & {"remove-cell", "archive-only", "presenter-notes"}}


def resolved_source(cell, cells):
    """Insert exact reader displays into slide-only placeholders."""
    def replace(match):
        canonical = cells[match[1]]
        if "slides-only" in canonical.get("metadata", {}).get("tags", []):
            raise ValueError("An equation source must belong to the reader.")
        return list(DISPLAY.finditer("".join(canonical["source"])))[int(match[2])][0]
    return REFERENCE.sub(replace, "".join(cell["source"]))


def materialize(notebook, output):
    data = json.loads(notebook.read_text())
    cells = load_cells(notebook)
    for cell in data["cells"]:
        if cell["cell_type"] == "markdown":
            cell["source"] = resolved_source(cell, cells).splitlines(keepends=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def check(root=ROOT, manifest_path=MANIFEST, notebook=None):
    manifest = json.loads(manifest_path.read_text())
    errors = []
    paths = sorted((root / "notebooks").glob("week*/L_*.ipynb"))
    if manifest.get('scope'):
        paths = [p for p in paths if str(p.relative_to(root)) in manifest['scope']]
    if notebook:
        paths = [p for p in paths if p.resolve() == Path(notebook).resolve()]
        if not paths:
            return ["No lecture notebook matched the requested equation check."]
    for path in paths:
        key = str(path.relative_to(root))
        cells = load_cells(path)
        try:
            sources = {i: resolved_source(c, cells) for i, c in cells.items()}
        except (KeyError, IndexError, ValueError) as exc:
            errors.append(f"{key}: broken reader equation placeholder: {exc}")
            continue
        entry = manifest["notebooks"].get(key)
        if entry is None:
            errors.append(f"{key}: missing equation audit")
            continue
        signatures = {i: sig for i, c in cells.items()
                      if (sig := math_signature(sources[i]))}
        for i in signatures.keys() | entry["math_signatures"].keys():
            if signatures.get(i) != entry["math_signatures"].get(i):
                errors.append(f"{key}:{i}: mathematics changed; review reader, slides and notation together")
        actual = {(i, j) for i, c in cells.items()
                  if "slides-only" in c.get("metadata", {}).get("tags", [])
                  for j, _ in enumerate(DISPLAY.finditer(sources[i]))}
        covered = {(x["slide"], x["index"]) for x in entry["displays"]}
        if actual != covered:
            errors.append(f"{key}: slide display coverage changed: {actual ^ covered}")
        for link in entry["displays"]:
            if link["mode"] != "exact":
                if not link.get("reason") or not link.get("reader_cells"):
                    errors.append(f"{key}: undocumented equation variation")
                continue
            try:
                placeholder = f"<!-- reader-equation: {link['reader']}:{link['reader_index']} -->"
                if placeholder not in "".join(cells[link["slide"]]["source"]):
                    errors.append(f"{key}:{link['slide']}: restore the canonical reader reference instead of copying the equation")
                slide = list(DISPLAY.finditer(sources[link["slide"]]))[link["index"]][1]
                reader = list(DISPLAY.finditer("".join(cells[link["reader"]]["source"])))[link["reader_index"]][1]
                if "slides-only" in cells[link["reader"]].get("metadata", {}).get("tags", []):
                    raise ValueError("canonical cell is slides-only")
                if normalise(slide) != normalise(reader):
                    errors.append(f"{key}:{link['slide']} display {link['index']}: differs from reader {link['reader']}")
            except (KeyError, IndexError, ValueError) as exc:
                errors.append(f"{key}: broken canonical equation reference: {exc}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path)
    parser.add_argument("--materialize", type=Path, help="Build a temporary slide notebook with reader equations inserted")
    args = parser.parse_args()
    errors = check(notebook=args.notebook)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print("Do not refresh the audit automatically. Check the canonical reader "
              "equation and every affected slide before updating the manifest.", file=sys.stderr)
        sys.exit(1)
    print("Reader/slide equation consistency check passed.")
    if args.materialize:
        if not args.notebook:
            parser.error("--materialize requires --notebook")
        materialize(args.notebook, args.materialize)
