"""Add a consistent Explorable banner where an interactive is a real section."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def source(text):
    return text.splitlines(keepends=True)


def banner(cid, tags):
    return {"cell_type": "markdown", "id": cid,
            "metadata": {"tags": tags, "slideshow": {"slide_type": "slide" if "slides-only" in tags else "skip"}},
            "source": source("# Explorable\n")}


def add(path, targets):
    nb = json.loads(path.read_text()); cells = nb["cells"]
    for target, cid, tags in targets:
        if any(c.get("id") == cid for c in cells):
            continue
        i = next(i for i, c in enumerate(cells) if c.get("id") == target)
        cells.insert(i, banner(cid, tags))
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")


add(ROOT / "notebooks/week04/L_Cellular_automata.ipynb", [
    ("w4-kelp", "w4-explorable-banner-slide", ["slides-only"]),
    ("week04-app-kelp", "w4-explorable-banner-reader", ["reader-only"]),
])
add(ROOT / "notebooks/week07/L_Intelligent_systems.ipynb", [
    ("w7-pso-watch", "w7-explorable-banner-slide", ["slides-only"]),
    ("ebb75231-ca35-4a44-9ee7-1c71ff41973f", "w7-explorable-banner-reader", ["reader-only"]),
])
add(ROOT / "notebooks/week09/L_InformationTheory.ipynb", [
    ("w9-distribution-explorer", "w9-explorable-banner-reader", ["reader-only"]),
])

# Week 9's slide copy has no stable id.
p = ROOT / "notebooks/week09/L_InformationTheory.ipynb"
nb = json.loads(p.read_text()); cells = nb["cells"]
if not any(c.get("id") == "w9-explorable-banner-slide" for c in cells):
    i = next(i for i,c in enumerate(cells) if "slides-only" in c.get("metadata",{}).get("tags",[]) and "## Explore parameterised distributions" in "".join(c.get("source",[])))
    cells.insert(i, banner("w9-explorable-banner-slide", ["slides-only"]))
p.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")

# The Prisoner's Kaleidoscope is deliberately placed after the game is defined.
p = ROOT / "notebooks/week10/L_Game_theory.ipynb"
nb = json.loads(p.read_text()); cells = nb["cells"]
if not any(c.get("id") == "w10-explorable-banner" for c in cells):
    i = next(i for i,c in enumerate(cells) if c.get("id") is None and "prisoners-kaleidoscope" in "".join(c.get("source",[])) and "remove-cell" not in c.get("metadata",{}).get("tags",[]))
    cells.insert(i, banner("w10-explorable-banner", []))
p.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
