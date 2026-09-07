#!/usr/bin/env python3
"""Add the unit's cumulative modelling-toolkit signal to lecture openings."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ADDITIONS = {
    1: (
        "Explicit model ingredients: world, state, local rules and observables; "
        "random seeds make stochastic comparisons reproducible."
    ),
    2: (
        "Recursive construction and scale-dependent measurement; resolution and "
        "the chosen scaling range become part of the evidence."
    ),
    3: (
        "Continuous fields, local reaction and spatial transport; differential "
        "equations are translated into grid updates without confusing the numerical "
        "representation with the model itself."
    ),
    4: (
        "Finite-state dynamics on a fixed lattice; synchronous updating, rule and "
        "state spaces, and computational cost can now be examined explicitly."
    ),
    5: (
        "The agents become mobile and carry vector-valued headings. Noise enters as "
        "a modelling choice, and collective order is assessed across repeated runs."
    ),
    6: (
        "Each agent now has intrinsic dynamics even in isolation. Heterogeneity also "
        "moves beyond Schelling's two categorical types to a parameter distributed "
        "across the population."
    ),
    7: (
        "Agents evaluate an environment, retain personal memory and share discoveries. "
        "Unlike Kuramoto's instantaneous global mean, PSO's global information is a "
        "best-so-far record accumulated through time."
    ),
    8: (
        "Slow driving is separated from fast event relaxation. Event-size distributions "
        "become outputs, while an existing lattice implementation is audited, reused "
        "and extended."
    ),
    9: (
        "The representation and measurement pipeline become the focus: outcomes are "
        "turned into probability distributions, uncertainty and dependence measures."
    ),
    10: (
        "Interactions now produce payoffs, repeated encounters create path dependence, "
        "and strategies themselves can change through selection, inheritance and mutation."
    ),
}


def lecture_path(week: int) -> Path:
    paths = list((ROOT / "notebooks" / f"week{week:02d}").glob("L_*.ipynb"))
    if len(paths) != 1:
        raise RuntimeError(f"Expected one lecture notebook for Week {week}, found {paths}")
    return paths[0]


def update_notebook(week: int) -> None:
    path = lecture_path(week)
    notebook = json.loads(path.read_text())
    cell = notebook["cells"][0]
    source = "".join(cell.get("source", []))

    # This script is safe to rerun when wording is revised later.
    source = re.sub(
        r'(?:<br>)?<span class="toolkit-addition">.*?</span>',
        "",
        source,
        flags=re.DOTALL,
    )

    signal = (
        '<span class="toolkit-addition"><strong>Added to the toolkit:</strong> '
        + ADDITIONS[week]
        + "</span>"
    )

    if '<p class="week-emphasis">' in source:
        close = source.index("</p>", source.index('<p class="week-emphasis">'))
        source = source[:close] + "<br>" + signal + source[close:]
    else:
        source = source.rstrip() + f'\n\n<p class="week-emphasis">{signal}</p>'

    cell["source"] = source
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


def main() -> None:
    for week in ADDITIONS:
        update_notebook(week)


if __name__ == "__main__":
    main()
