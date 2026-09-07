"""Report markdown heading jumps in lecture notebooks."""
from pathlib import Path
import re
import nbformat

ROOT = Path(__file__).resolve().parents[1] / "notebooks"
issues = []
for path in sorted(ROOT.glob("week*/L_*.ipynb")):
    previous = None
    for index, cell in enumerate(nbformat.read(path, as_version=4).cells):
        if cell.cell_type != "markdown" or "archive-only" in cell.metadata.get("tags", []):
            continue
        for match in re.finditer(r"^(#{1,6})\s+(.+)$", cell.source, re.MULTILINE):
            level = len(match.group(1))
            if previous is not None and level > previous + 1:
                issues.append(f"{path.relative_to(ROOT)} cell {index}: H{previous} -> H{level} ({match.group(2)})")
            previous = level
if issues:
    print("\n".join(issues))
    raise SystemExit(1)
print("Lecture heading hierarchy: no skipped levels.")
