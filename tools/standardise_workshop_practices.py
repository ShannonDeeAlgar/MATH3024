#!/usr/bin/env python3
"""Standardise the secondary modelling-practice objective in workshops 1–10."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTCOMES = {
    1: "By the end, you should be able to use seeds for reproducible examples, matched comparisons, and independent ensembles without mistaking one seeded run for general evidence.",
    2: "By the end, you should be able to explain why a finite dimension estimate changes with resolution, alignment, construction depth, and fitting range.",
    3: "By the end, you should be able to separate an implementation error from a model result using operator tests and a refinement comparison.",
    4: "By the end, you should be able to estimate a simulation's workload and justify how a fixed computational budget is divided among world size, runtime, rule coverage, and repeated initial conditions.",
    5: "By the end, you should be able to compare two defensible implementations of noise using matched parameter sweeps and stochastic ensembles.",
    6: "By the end, you should be able to explain how the distribution of individual frequencies and finite population size alter the observed onset of collective synchronisation.",
    7: "By the end, you should be able to evaluate a stochastic optimiser across repeated runs using more than its single best outcome.",
    8: "By the end, you should be able to challenge a scaling claim by changing the fitting range and system size rather than relying on a straight-looking log–log plot.",
    9: "By the end, you should be able to state what an entropy calculation retains, what it discards, and how that depends on the chosen representation.",
    10: "By the end, you should be able to test whether an evolutionary outcome survives changes to initial composition and the population update rule.",
}


for week, outcome in OUTCOMES.items():
    notebook = next((ROOT / "notebooks" / f"week{week:02d}").glob("WS_*.ipynb"))
    data = json.loads(notebook.read_text())
    cell = next(c for c in data["cells"] if "**Modelling focus:**" in "".join(c.get("source", [])))
    source = "".join(cell["source"])
    source = source.replace("**Modelling focus:**", "**Modelling practice:**")
    if week == 5:
        source = source.replace(
            "**Why it matters:** Small coding choices can alter a phase transition, while reliable comparisons consume finite computation time.",
            "**Why it matters:** Two plausible ways of adding noise can produce different collective transitions, so the stochastic rule is part of the model rather than incidental code.",
        )
    generic = "It is developed through the canonical model rather than as a separate exercise."
    if generic in source:
        source = source.replace(generic, outcome)
    elif outcome not in source:
        source = source.rstrip() + "\n\n" + outcome + "\n"
    cell["source"] = source.splitlines(keepends=True)
    notebook.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print(notebook.relative_to(ROOT))
