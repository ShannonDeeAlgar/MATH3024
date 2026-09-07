"""Complete the remaining narrative and workshop checks for Week 8."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(cell):
    return "".join(cell.get("source", []))


def set_source(cell, text):
    cell["source"] = text.splitlines(keepends=True)


reader_path = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"
reader = json.loads(reader_path.read_text())

for cell in reader["cells"]:
    if cell.get("id") == "standardised-title-context":
        set_source(
            cell,
            """## Events across many scales

Earthquakes provide the motivating picture. Most recorded events are small, but a few release vastly more energy and affect much larger regions. Similar questions arise for blackouts, landslides and neuronal avalanches: is there a characteristic event size, or does the system produce events across a broad range of scales?

A broad distribution is an observation, not yet an explanation. Detection limits hide the smallest events, finite systems limit the largest, and several different distributions can look approximately straight on log–log axes. This week develops the model and the evidence together: first a tuned critical system, then a slowly driven system that approaches a critical regime without an experimenter tuning it to one special control value.
""",
        )

    if cell.get("id") == "3cdcf36d-eddc-4976-973b-e53a589762af":
        set_source(
            cell,
            """### Behaviour in events

Avalanche sizes range from tiny local rearrangements to events limited by the lattice itself. Before fitting a power law, inspect the full distribution and identify the region actually supported by the simulation:

- the smallest recorded events depend on the event definition and measurement resolution;
- the largest events are limited by the finite lattice;
- the apparent straight region between them may span only a restricted range; and
- a heavy tail is not, by itself, proof of an asymptotic power law.

The useful test is comparative. Repeat the analysis for several lattice sizes and ask whether the upper cutoff moves outward while the fitted behaviour over the shared range remains reasonably stable.
""",
        )

reader_path.write_text(json.dumps(reader, indent=1, ensure_ascii=False) + "\n")


workshop_path = ROOT / "notebooks/week08/WS_Critical_phenomena.ipynb"
workshop = json.loads(workshop_path.read_text())

for cell in workshop["cells"]:
    if cell.get("id") == "w8-takeaway":
        set_source(
            cell,
            """## Validation record

The local toppling rule is simple. The empirical scaling claim is not. Before reusing this model or reporting a scaling result, record:

- **implementation checks:** central topplings conserve grains, boundary topplings dissipate them, and every recorded avalanche ends in a stable lattice;
- **initialisation:** lattice size, starting state, random seed and burn-in;
- **measurement:** avalanche definition, number of grain additions, size and duration definitions, and treatment of zero-toppling additions; and
- **claim limits:** fitted range, finite-size cutoff, sensitivity to lattice size, and plausible alternative explanations for the tail.

This is enough to make borrowed code inspectable and the resulting claim reproducible.
""",
        )

workshop_path.write_text(json.dumps(workshop, indent=1, ensure_ascii=False) + "\n")


checklist_path = ROOT / "COURSE_AUDIT_CHECKLIST.md"
text = checklist_path.read_text()
text = text.replace(
    "- [ ] Open with a concrete event or system in which behaviour spans several scales.",
    "- [x] Open with a concrete event or system in which behaviour spans several scales.",
)
text = text.replace(
    "- [ ] Explain cutoffs, finite systems, and defensible scaling ranges before fitting a power law.",
    "- [x] Explain cutoffs, finite systems, and defensible scaling ranges before fitting a power law.",
)
text = text.replace(
    "- [ ] Animate at least one avalanche with an inspectable student-level animation.",
    "- [x] Animate at least one avalanche with an inspectable student-level animation.",
)
text = text.replace(
    "- [ ] End with a short validation record students could reuse in a project.",
    "- [x] End with a short validation record students could reuse in a project.",
)
checklist_path.write_text(text)
