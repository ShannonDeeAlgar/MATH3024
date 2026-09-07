"""Keep display equations visually clean and flag malformed delimiters."""

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def clean_display(match):
    body = match.group(1)
    # The course style treats a displayed equation as a visual block. Sentence
    # punctuation belongs in the surrounding prose, where it cannot appear as
    # a stray dot beside an automatically generated equation number.
    body = re.sub(r"([,.;:])(?=\s*$)", "", body)
    return "$$" + body + "$$"


for path in sorted((ROOT / "notebooks").glob("week*/L_*.ipynb")):
    data = json.loads(path.read_text())
    changed = False
    for cell in data.get("cells", []):
        source = cell.get("source", [])
        text = source if isinstance(source, str) else "".join(source)
        revised = re.sub(r"\$\$(.*?)\$\$", clean_display, text, flags=re.S)
        # Repair the common typo that creates visible delimiters in prose.
        revised = revised.replace("$$.", "$$").replace("$$,", "$$")
        if revised != text:
            cell["source"] = revised
            changed = True
    if changed:
        path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
