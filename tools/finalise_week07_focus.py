#!/usr/bin/env python3
"""Tighten Week 7 around unconventional intelligence, biomimicry, ACO and PSO."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week07/L_Intelligent_systems.ipynb"


def md(source: str, cell_id: str, tags: list[str], slide_type: str = "") -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": tags, "slideshow": {"slide_type": slide_type}},
        "source": [line + "\n" for line in source.strip().splitlines()],
    }


nb = json.loads(PATH.read_text())
cells = nb["cells"]


# Remove the obsolete broad-AI/perceptron survey and the duplicated older framing.
remove_ids = {
    "w7-slides-motivation", "w7-question", "w7-two-aims", "w7-slides-model",
    "w7-perceptron", "w7-xor", "w7-ai-limits", "w7-reader-motivation",
    "standardised-title-context", "54b2d404-8aa4-4950-94a5-b886883551f0",
    "a274aed2-cdf5-4c1d-af14-3d87a7bbbe2f", "3322f266",
    "660548bc-e418-458d-9db7-8130dc7b02f9", "da3527b4-fd35-4ae7-944d-21f6a5f793aa",
    "e0aeec0f-bd16-4972-af5b-545dce152e3f", "3765471e-189a-43e1-9ec2-612f5d1e3c43",
    "f6172e26-cae3-44a1-b9c6-42b1b71d0774", "f9a922f2-43b0-4908-9919-ce45328085ca",
    "65ff3029", "75e16371-cdc0-4ca5-af5e-c017a7a4a951", "0fa90d8c-fab8-4dde-8206-6c6a4e58138a",
    "433e53e5-2c94-4efa-b50d-40ec1c32fd9e", "9265590a-99fd-4676-a516-f22b7efd8715",
    "5203643a-c890-4915-9d07-d4533906d424", "53e0b32c-d0e4-4021-b02c-7f937ec17673",
    "90aef3f0-c90b-4d47-9e36-3cb8ba7fda66", "0dca71cd-5ea9-48a5-91c0-2bf4a8636996",
    "66a8c075-4351-4170-aadf-4b6da4d5646f", "957e5392-41ea-4e90-84d5-e5740a50ad3a",
    "w7-reader-model", "18998055", "a1274aaf-3097-4904-ae47-df310fd1fdc6", "4a07fb89",
    "2e2c7053-1b61-4e05-b5a5-77e8a6c66396", "72ec22c0-fcbb-449b-8149-087f43869d35",
    "29f05cf9", "1dcd3871-e715-489e-a737-6efab5d8f101", "b6f58e44-9ed3-4a97-8769-70ce7a1a79ad",
    "d0177c57-0525-4c05-bc97-cd8cccf5ffee", "58a7b197-24df-4541-904e-a45aaa7db09e",
    "f35f34cd", "55e3f780-61b4-4c01-b5a0-b9b955b8734b", "8820788a", "528c222f",
    "3d3d08e9-255b-44e0-ac5f-dbbe5f46c071", "db26c75d-8710-4d0c-aa4b-4f70a6e4f67f",
    "8db128b0-9ce5-44d9-af0f-6160ed9f3eca", "970f32ca", "806dbfcf", "c5b5f6cc",
    "e41646f2-e04c-4742-bc02-d2fd1a407c39", "bc703bda", "a2aea159",
    "d6ccb6b1-b4d6-4961-96c8-2b4802e5c70f", "d22fa3de", "3efd0a07-ac4d-45aa-a865-f95ff83a1de8",
    "e893c272-987d-4013-b695-95fbe11debc8",
}
cells = [cell for cell in cells if cell.get("id") not in remove_ids]


# Remove an earlier run of this finaliser.
generated = {
    "w7-framing-banner", "w7-definition-slide", "w7-schism-slide", "w7-ai-context-slide",
    "w7-real-banner", "w7-reader-framing", "w7-reader-definition", "w7-reader-schism",
    "w7-reader-ai-context", "w7-reader-real-banner", "w7-model-banner-slides", "w7-model-banner-reader",
}
cells = [cell for cell in cells if cell.get("id") not in generated]


# The title should describe the week, not the workshop.
title = next(cell for cell in cells if cell.get("id") == "305e7889")
text = "".join(title["source"])
text = text.replace(
    "The workshop begins with the agent structure used in earlier weeks, then changes what the state, interaction and update mean. Evaluation across repeated runs is used to check the resulting extension.",
    "This week considers intelligence as adaptive, goal-directed behaviour and then develops nature-inspired search through particle swarm optimisation."
)
title["source"] = [line + "\n" for line in text.strip().splitlines()]


title_i = cells.index(title) + 1
framing = [
    md("# Framing intelligent systems", "w7-framing-banner", ["slides", "slides-only"], "slide"),
    md("""
## What is an intelligent system?

An intelligent system receives information, uses it to choose between possible actions, and changes its behaviour in ways that help it pursue a goal or respond effectively to changing conditions.

The system may be natural or artificial. Intelligence need not reside in one central controller: it can arise from interactions among comparatively simple parts.
""", "w7-definition-slide", ["slides", "slides-only"], "slide"),
    md("""
## Two approaches to intelligent systems

<div class="image-panel" style="max-width:1120px;margin:auto"><img src="images/intelligent_systems_schism.svg" alt="Complexity science and machine learning as complementary approaches to intelligent systems"></div>

<p class="figure-source">Framing adapted from David Krakauer's discussion of a scientific schism between explanation and prediction.</p>
""", "w7-schism-slide", ["slides", "slides-only"], "slide"),
    md("""
## Artificial intelligence is one part of the story

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Kasparov_vs_Deep_blue.png" alt="Garry Kasparov playing IBM Deep Blue"></div>
<div class="text-panel">
<p>Artificial intelligence includes systems designed to perform tasks such as classification, prediction, planning and search.</p>
<p>Deep Blue's 1997 win over Garry Kasparov showed that a machine could outperform a world champion at chess. It did not settle what intelligence is, nor how human and machine problem solving should be compared.</p>
</div>
</div>
""", "w7-ai-context-slide", ["slides", "slides-only"], "slide"),
    md("# Real-world motivation", "w7-real-banner", ["slides", "slides-only"], "slide"),
]
cells[title_i:title_i] = framing


# Reader framing comes before the empirical examples.
collective_i = next(i for i, c in enumerate(cells) if c.get("id") == "9012fd46")
reader_framing = [
    md("# Framing intelligent systems", "w7-reader-framing", ["reader-only"], "skip"),
    md("""
## What is an intelligent system?

An **intelligent system** receives information, uses it to choose between possible actions, and changes its behaviour in ways that help it pursue a goal or respond effectively to changing conditions. This definition includes artificial systems, nervous systems and collectives whose members coordinate without a central controller.

The definition is deliberately functional. It asks what information is available, how it affects a decision and whether behaviour changes with experience or conditions. It does not require consciousness or human-like reasoning.
""", "w7-reader-definition", ["reader-only"], "skip"),
    md("""
## Explanation and prediction

<img src="images/intelligent_systems_schism.svg" alt="Complexity science and machine learning as complementary approaches to intelligent systems" style="display:block;width:min(100%,950px);margin:1rem auto">

David Krakauer, President of the Santa Fe Institute, describes a developing scientific **schism**. Machine learning can preserve enormous amounts of detail in a high-dimensional model and make very accurate predictions, while leaving the route to a prediction difficult to explain. Complexity science more often searches for a compressed description that exposes a mechanism or useful scale, accepting that some predictive detail will be lost.

This is the distinction represented in the figure. It is not a choice between a sensible method and a reckless “kitchen sink”. The methods answer different questions and increasingly inform one another. Krakauer argues that science must combine prediction with understanding rather than allow either approach to displace the other.

*Source:* David Krakauer, [“The Landscape of 21st Century Science”](https://complexity.simplecast.com/episodes/1), *COMPLEXITY* podcast; see also [“Unifying complexity science and machine learning”](https://doi.org/10.3389/fcpxs.2023.1235202) (2023).
""", "w7-reader-schism", ["reader-only"], "skip"),
    md("""
## Artificial intelligence in brief

Artificial intelligence is the broad collection of methods used to build systems that perform tasks associated with learning, prediction, planning, classification or search. We will not attempt a taxonomy of the rapidly changing field here.

IBM Deep Blue's 1997 victory over Garry Kasparov is a useful reminder that successful performance and human-like reasoning are different claims. Deep Blue was designed for chess and combined extensive search with carefully designed evaluation. Modern systems solve a much wider range of problems, but performance still depends on the objective, data, representation and conditions under which a system is tested.

AI can be valuable in medical imaging, translation, scientific prediction and many other tasks. It can also learn shortcuts, reproduce bias, fail outside its training conditions or provide confident but unsupported output. “Good” and “bad” are therefore not properties of a technique in isolation. The relevant questions are whether it works for the stated task, under what conditions, how failure is detected and who bears the consequences.

This week follows a different branch of artificial intelligence: **nature-inspired optimisation**. We begin with collective intelligence in ants, identify mechanisms that can be transferred into algorithms, and then study particle swarm optimisation in detail.
""", "w7-reader-ai-context", ["reader-only"], "skip"),
    md("# Real-world motivation", "w7-reader-real-banner", ["reader-only"], "skip"),
]
cells[collective_i:collective_i] = reader_framing

# Two legacy reader-only introduction cells belong with the empirical examples,
# not ahead of the new framing section. Keep their content, but place it directly
# below the Real-world motivation banner.
legacy_collective_ids = ["f0d0beff", "5aa96f13"]
legacy_collective = []
for cell_id in legacy_collective_ids:
    i = next(i for i, c in enumerate(cells) if c.get("id") == cell_id)
    legacy_collective.append(cells.pop(i))
real_banner_i = next(i for i, c in enumerate(cells) if c.get("id") == "w7-reader-real-banner")
cells[real_banner_i + 1:real_banner_i + 1] = legacy_collective


# Model details begin when the natural mechanism becomes an algorithm, not during background.
aco_slide_i = next(i for i, c in enumerate(cells) if c.get("id") == "w7-aco")
cells.insert(aco_slide_i, md("# Model details", "w7-model-banner-slides", ["slides", "slides-only"], "slide"))

aco_reader_i = next(i for i, c in enumerate(cells) if c.get("id") == "e99e6df2")
cells.insert(aco_reader_i, md("# Model details", "w7-model-banner-reader", ["reader-only"], "skip"))


# Clean the PSO-paper callout and make the canonical-model identity unmistakable.
for cell in cells:
    source = "".join(cell.get("source", []))
    if cell.get("id") == "w7-synthesis":
        source = source.replace(
            "| perceptron | one labelled example | learned weights | classification |\n",
            "",
        )

    if cell.get("id") == "w7-close":
        source = source.replace(
            "\nThese questions apply whether the system is biological, social or engineered.\n",
            "\n",
        )

    if cell.get("id") == "123ce5fa-05d3-442e-ac4d-b283a5612b41":
        source = """
### Read the original PSO paper

Kennedy and Eberhart's [“Particle Swarm Optimization”](https://ieeexplore.ieee.org/document/488968) (1995) is unusually readable. It records how an attempt to simulate social behaviour became an optimisation algorithm.

<div class="reader-voice">
  <div class="reader-voice-quote">Two individuals can hold identical attitudes and beliefs without banging together, but two birds cannot occupy the same position in space without colliding.</div>
  <div class="reader-voice-attr">— James Kennedy and Russell Eberhart, “Particle Swarm Optimization” (1995)</div>
</div>
"""

    if "Read the OG PSO paper" in source:
        source = source.replace(
            "<div class=\"reader-choice\">\n  <strong>Read:</strong><br>\n  Read the OG PSO paper[PSO algorithm](https://ieeexplore.ieee.org/document/488968). It's fantastic and full of gems like this...\n</div>",
            "> **Original PSO paper:** Kennedy and Eberhart's [“Particle Swarm Optimization”](https://ieeexplore.ieee.org/document/488968) (1995) is unusually readable and records how the algorithm emerged from experiments with simulated social behaviour."
        )
        source = source.replace(
            "Read the OG PSO paper[PSO algorithm](https://ieeexplore.ieee.org/document/488968). It's fantastic and full of gems like this...",
            "**Original PSO paper:** Kennedy and Eberhart's [“Particle Swarm Optimization”](https://ieeexplore.ieee.org/document/488968) (1995) is unusually readable and records how the algorithm emerged from experiments with simulated social behaviour."
        )
    if cell.get("id") in {"canonical-pseudocode", "w7-canonical-pseudocode"}:
        heading, _, remainder = source.partition("\n")
        heading = "# Canonical models in pseudocode"
        source = heading + (("\n" + remainder) if remainder else "")

    cell["source"] = [line + "\n" for line in source.strip().splitlines()]


nb["cells"] = cells
PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Updated {PATH}")
