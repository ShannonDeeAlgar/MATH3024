#!/usr/bin/env python3
"""Bring the Week 8--10 lecture notebooks onto the shared Reveal blueprint.

The source notebooks are edited rather than the generated HTML so slide
boundaries and typography survive every subsequent rebuild.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = {
    8: ROOT / "notebooks/week08/L_Critical_phenomena.ipynb",
    9: ROOT / "notebooks/week09/L_InformationTheory.ipynb",
    10: ROOT / "notebooks/week10/L_Game_theory.ipynb",
}


def source(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_source(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True)


def set_slide_type(cell: dict, slide_type: str) -> None:
    cell.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = slide_type


def add_tag(cell: dict, tag: str) -> None:
    tags = cell.setdefault("metadata", {}).setdefault("tags", [])
    if tag not in tags:
        tags.append(tag)


def normalise_slide_heading(cell: dict) -> None:
    """Keep slide titles large enough to read and avoid h4/h5 drift."""
    if cell.get("cell_type") != "markdown":
        return
    st = cell.get("metadata", {}).get("slideshow", {}).get("slide_type")
    if st not in {"slide", "subslide"}:
        return
    text = source(cell)
    if re.match(r"^#{4,5}\s", text):
        text = re.sub(r"^#{4,5}\s", "### ", text, count=1)
        set_source(cell, text)


def clean_inline_type(text: str) -> str:
    # Inline font declarations from the old decks override the shared theme.
    text = re.sub(r"\s*font-family:\s*[^;\"']+(?:'[^']*')?\s*;?", "", text, flags=re.I)
    text = re.sub(r"\s*font-size:\s*\d+(?:\.\d+)?px\s*;?", "", text, flags=re.I)
    # Indented blank lines are interpreted as empty code blocks by Markdown.
    text = "".join("\n" if not line.strip() else line for line in text.splitlines(keepends=True))
    return text


def fix_week8(nb: dict) -> None:
    for cell in nb["cells"]:
        if cell.get("cell_type") == "markdown":
            set_source(cell, clean_inline_type(source(cell)))
        normalise_slide_heading(cell)

    if len(nb["cells"]) > 38:
        text = source(nb["cells"][38]).replace("##### How this figure was produced", "#### How this figure was produced", 1)
        set_source(nb["cells"][38], text)

    if len(nb["cells"]) > 56:
        set_source(
            nb["cells"][56],
            """<img src="images/Sandpile_Matemateca_22_screenshot.png" alt="Sand forming a pile as grains are poured onto a surface" style="display:block; max-height:330px; width:auto; margin:0.35em auto 0;" />

<div class="figure-reference">Video of a sandpile: <a href="https://en.wikipedia.org/wiki/Angle_of_repose">angle of repose</a>.</div>
""",
        )

    if len(nb["cells"]) > 105:
        set_source(
            nb["cells"][104],
            """### Mean-field approximation: what it loses

<div class="slide-columns">
<div>

A mean-field approximation averages across the system. It therefore removes spatial relationships and can miss behaviour that depends on local structure.

The approximation can still be useful—but its assumptions must match the mechanism.

</div>
<img class="column-image" src="images/Mean_field_approximation_GoL.png" alt="Mean-field approximation applied to Conway's Game of Life" />
</div>

<div class="figure-reference">Image adapted from Sayama.</div>
""",
        )
        add_tag(nb["cells"][105], "archive-only")
        set_slide_type(nb["cells"][105], "skip")


def fix_week9(nb: dict) -> None:
    for cell in nb["cells"]:
        if cell.get("cell_type") == "markdown":
            text = clean_inline_type(source(cell))
            text = text.replace("Kullback-Liebler", "Kullback–Leibler")
            set_source(cell, text)
        normalise_slide_heading(cell)

    if len(nb["cells"]) > 43:
        text = source(nb["cells"][43]).replace("#### Recall: Expected value", "### Recall: Expected value", 1)
        set_source(nb["cells"][43], text)


def fix_week10(nb: dict) -> None:
    for index, cell in enumerate(nb["cells"]):
        text = source(cell)

        if cell.get("cell_type") == "markdown":
            text = clean_inline_type(text)
            # A presenter-only link had leaked onto the Nash-equilibrium slide.
            text = re.sub(
                r"\n*Khan Academy has a tutorial to point students to:.*?(?=\n\n|\Z)",
                "",
                text,
                flags=re.S,
            )
            set_source(cell, text)

        # The second half of the notebook had lost all Reveal boundaries.  Each
        # cell is already written as one pedagogical unit, so restore boundaries
        # from its leading heading level.
        if index >= 49 and cell.get("cell_type") == "markdown":
            first = text.lstrip().splitlines()[0] if text.strip() else ""
            if first.startswith("# "):
                set_slide_type(cell, "slide")
            elif first.startswith(("## ", "### ", "#### ", "##### ")):
                set_slide_type(cell, "subslide")

        normalise_slide_heading(cell)

    # Remove an obsolete development note and a successful-run printout from
    # both the deck and Reader build.
    for index in (69, 72):
        if index < len(nb["cells"]):
            add_tag(nb["cells"][index], "archive-only")
            set_slide_type(nb["cells"][index], "skip")

    # Keep the YouTube output but never expose its Python source.
    if len(nb["cells"]) > 50:
        add_tag(nb["cells"][50], "hide-input")

    # Replace two vertically overloaded legacy slides with the same information
    # in compact, side-by-side layouts.
    if len(nb["cells"]) > 58:
        set_source(
            nb["cells"][58],
            """# Modelling evolution

<div class="two-panel">
<div class="text-panel">
<h3>Population update</h3>
<ol>
<li>Assign each agent a genotype.</li>
<li>Map genotype to fitness.</li>
<li>Remove some agents.</li>
<li>Create offspring from survivors.</li>
</ol>
</div>
<div class="text-panel">
<h3>Modelling choices</h3>
<ul>
<li>How is genotype represented?</li>
<li>How does genotype determine fitness?</li>
<li>Who survives and reproduces?</li>
<li>How are inheritance and mutation implemented?</li>
</ul>
</div>
</div>
""",
        )

    if len(nb["cells"]) > 59:
        text = source(nb["cells"][59]).replace("### Fitness", "## Fitness", 1)
        set_source(nb["cells"][59], text)

    if len(nb["cells"]) > 68:
        set_source(
            nb["cells"][68],
            """### Tit for Tat

<div class="slide-columns">
<div>

Tit for Tat cooperates first, then copies its opponent's previous move.

- **Nice:** cooperates initially
- **Retaliatory:** answers defection
- **Forgiving:** returns to cooperation
- **Non-envious:** does not try to outscore one opponent

It won Axelrod's original tournament, although later work found stronger strategies in other settings.

</div>
<img class="column-image" src="images/Iterated_Prisoners_Dilemma_Venn-Diagram.png" alt="Venn diagram of properties associated with successful iterated Prisoner's Dilemma strategies" />
</div>
""",
        )


def main() -> None:
    for week, path in NOTEBOOKS.items():
        nb = json.loads(path.read_text())
        {8: fix_week8, 9: fix_week9, 10: fix_week10}[week](nb)
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
        print(f"Updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
