#!/usr/bin/env python3
"""Add the functional motivation for near-critical operation to Week 8."""

import json
from pathlib import Path


PATH = Path("notebooks/week08/L_Critical_phenomena.ipynb")


def source(text):
    return text.strip().splitlines(keepends=True)


def markdown(cell_id, text, tags, slide_type="subslide"):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"slideshow": {"slide_type": slide_type}, "tags": tags},
        "source": source(text),
    }


notebook = json.loads(PATH.read_text())
cells = notebook["cells"]

# Make the opening roadmap ask both the functional and mechanistic questions.
opening = next(cell for cell in cells if cell.get("id") == "082eb6fb")
opening_text = "".join(opening["source"])
opening_text = opening_text.replace(
    "The recurring question is: <em>if an ordinary critical point must be tuned, how can critical-like behaviour persist?</em>",
    "The recurring questions are: <em>what can a system gain by operating near a critical point, and how can critical-like behaviour persist?</em>",
)
opening["source"] = source(opening_text)

# Replace any earlier generated copy rather than duplicating it.
new_ids = {"w8-why-critical-slide", "w8-why-critical-reader"}
cells[:] = [cell for cell in cells if cell.get("id") not in new_ids]
insert_at = next(i for i, cell in enumerate(cells) if cell.get("id") == "a5491561-24dd-4854-b885-7488872d7c7b")

shared_slide = markdown(
    "w8-why-critical-slide",
    r"""
## Why operate near a critical point?

Near a continuous transition, a small change can influence activity across much of the system.

| Property near criticality | What it can afford |
|---|---|
| large susceptibility | strong responses to weak signals |
| wide dynamic range | distinguish inputs spanning several orders of magnitude |
| long correlation length | propagate information across the system |
| many accessible collective states | switch flexibly between responses |

These gains come with greater noise amplification, slower relaxation and a higher risk of large cascades. The useful operating point depends on the task and environment.

<p style="font-size:0.58em">Examples studied as near-critical candidates include cortical networks, animal groups and gene-regulatory networks. Evidence and proposed function vary among systems.</p>
""",
    ["slides", "slides-only"],
)

reader = markdown(
    "w8-why-critical-reader",
    r"""
### Why might a system remain near criticality?

Near a continuous critical point, **susceptibility** is large: a weak local input can generate a substantial collective response. A long correlation length allows information about that input to influence distant parts of the system. The system may also respond across a wide **dynamic range**, distinguishing weak and strong inputs without saturating immediately. A broad repertoire of accessible collective states can support flexible switching as conditions change.

These properties are useful for systems that sense, communicate and adapt. They also carry costs. Fluctuations and measurement noise are amplified, relaxation becomes slow, and disturbances can spread into large cascades. Evolution or feedback may therefore place a biological system near a transition at a distance suited to its task, noise level and environment.

Several real systems have motivated this hypothesis:

- Models of excitable neural networks have maximal sensitivity and dynamic range at their critical point. Experiments with cortical slice cultures found the largest dynamic range when activity had neuronal-avalanche statistics ([Kinouchi and Copelli, 2006](https://doi.org/10.1038/nphys289); [Shew *et al.*, 2009](https://doi.org/10.1523/JNEUROSCI.3864-09.2009)).
- Natural midge swarms exhibit correlation lengths that grow with group size and dynamic scaling consistent with near-critical collective motion. This gives a possible route for disturbances to spread across a group ([Cavagna *et al.*, 2017](https://doi.org/10.1038/nphys4153)).
- Gene-regulatory networks are often modelled near the boundary between stable and strongly amplifying dynamics. Noise can shift the best-performing model into the subcritical regime, showing that exact criticality is not always optimal ([Villegas *et al.*, 2016](https://doi.org/10.1038/srep34743)).

The evidence differs across these examples. Neural dynamic range has been manipulated experimentally; near-critical scaling in animal groups has been measured observationally; many claims about regulatory networks depend on inferred networks and models. In each case, criticality is a hypothesis connecting a dynamical regime to a possible function, and the connection needs a system-specific test.
""",
    ["reader-only"],
    "skip",
)

cells[insert_at:insert_at] = [shared_slide, reader]
PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
