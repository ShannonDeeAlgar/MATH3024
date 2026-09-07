"""Reduce question-like and one-paragraph headings in the lecture Readers.

The replacements are deliberately explicit: this is a narrative edit, not a
rule that every question mark or short section heading is automatically wrong.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


HEADING_REPLACEMENTS = {
    "week01/L_Introduction_to_complex_systems.ipynb": {
        "## Why study Complex Systems at UWA?": "## Studying complex systems at UWA",
        "## Why models?": "## Models as explanations",
        "### What goes in to a model?": "### Model inputs",
        "### What comes out of a model?": "### Model outputs",
        "### Which society is more segregated?": "### Comparing segregation",
        "### When does the outcome emerge?": "### Time to outcome",
        "### How could we continue to improve our understanding?": "### Extending the analysis",
        "#### We'll need a different approach...": "**A different approach is needed.**",
        "### What one study found": "**Evidence from one study.**",
        "### Solve and conclude": "**Solve and conclude.**",
        "### Schelling’s observation": "**Schelling’s observation.**",
        "### A second perspective": "**A second perspective.**",
        "### Model inputs": "**Model inputs.**",
        "### Model outputs": "**Model outputs.**",
        "### Watch the process": "**Watch the process.**",
        "### Pause the process": "**Pause the process.**",
        "### Give every agent a local value": "**Give every agent a local value.**",
        "### From local judgement to collective behaviour": "**From local judgement to collective behaviour.**",
        "### One measure, one ordering": "**One measure, one ordering.**",
        "### Track system-level quantities": "**Track system-level quantities.**",
        "### A different seed, an unsettled trajectory": "**A different seed, an unsettled trajectory.**",
        "### Inspect the unsettled run": "**Inspect the unsettled run.**",
        "### Read two different observables together": "**Read two different observables together.**",
        "### First, sweep the parameter": "**First, sweep the parameter.**",
        "### Check the mechanism at three thresholds": "**Check the mechanism at three thresholds.**",
        "### Inspect the frustrated 80% run": "**Inspect the frustrated 80% run.**",
        "### One run is not enough": "**One run is not enough.**",
        "### From one run to an ensemble": "**From one run to an ensemble.**",
        "### Repeat the ensemble at every threshold": "**Repeat the ensemble at every threshold.**",
        "### Compare outcomes across thresholds": "**Compare outcomes across thresholds.**",
    },
    "week02/L_Fractals.ipynb": {
        "## Why begin here?": "## A first generative model",
        "## What are we looking at here?": "## Interpreting the image",
        "## What evidence counts as fractal?": "## Evidence for fractal structure",
        "## 2. Why does an IFS converge?": "## 2. Convergence of an IFS",
        "## What do we mean by dimension?": "## Dimension",
        "## Can we design a fractal with a chosen dimension?": "## Designing a fractal with a chosen dimension",
        "## Why can a count reveal dimension?": "## Box counting as a dimension estimate",
        "## When do we call a relationship scale-free?": "## Scale-free relationships",
        "## How would we test a scale-free claim?": "## Testing a scale-free claim",
        "## But …": "**Natural forms add further complications.**",
        "### A useful error": "**A useful error.**",
        "### Interpreting the coin": "**Interpreting the coin.**",
        "### Interpreting the plate": "**Interpreting the plate.**",
        "### Example 1A: the Cantor set": "**Example 1A: the Cantor set.**",
        "### Example 1B: the Sierpiński triangle": "**Example 1B: the Sierpiński triangle.**",
        "### Example 2A: the Cantor set": "**Example 2A: the Cantor set.**",
        "### Example 2B: the Sierpiński triangle": "**Example 2B: the Sierpiński triangle.**",
        "### Example 2C: the Koch curve": "**Example 2C: the Koch curve.**",
        "### Example 3A: the Cantor set": "**Example 3A: the Cantor set.**",
        "### Example 3B: the Sierpiński triangle": "**Example 3B: the Sierpiński triangle.**",
        "### Summary 1": "**Summary 1.**",
        "### Summary 2": "**Summary 2.**",
        "### Summary 3": "**Summary 3.**",
        "### Dimension of the Cantor set": "**Dimension of the Cantor set.**",
        "### Dimension of the Sierpiński triangle": "**Dimension of the Sierpiński triangle.**",
        "### Branching trees": "**Branching trees.**",
        "### Scale-free networks": "**Scale-free networks.**",
        "### Zipf's law": "**Zipf's law.**",
        "### More examples": "**Further examples.**",
        "### First interpretation: a coin": "**First interpretation: a coin.**",
        "### Second interpretation: a dinner plate": "**Second interpretation: a dinner plate.**",
        "## Symmetry of a Euclidean object": "**Symmetry of a Euclidean object.**",
        "## Symmetry of a fractal object": "**Symmetry of a fractal object.**",
        "## An empirical form: cauliflower": "**An empirical form: cauliflower.**",
        "## 1A. Cantor set · initiator and generator": "**1A. Cantor set: initiator and generator.**",
        "## 1B. Sierpiński triangle · initiator and generator": "**1B. Sierpiński triangle: initiator and generator.**",
        "## 2A. Cantor set · iterated function system": "**2A. Cantor set: iterated function system.**",
        "## 2B. Sierpiński triangle · iterated function system": "**2B. Sierpiński triangle: iterated function system.**",
        "## 2C. Sierpiński triangle · chaos game": "**2C. Sierpiński triangle: chaos game.**",
        "## 3A. Cantor set · L-system": "**3A. Cantor set: L-system.**",
        "## 3B. Sierpiński triangle · L-system": "**3B. Sierpiński triangle: L-system.**",
        "### Union versus intersection": "**Union versus intersection.**",
        "### Union versus intersection for the Sierpiński triangle": "**Union versus intersection for the Sierpiński triangle.**",
        "### 1. Initiator and generator": "**1. Initiator and generator.**",
        "### 2. Iterated function system": "**2. Iterated function system.**",
        "### 3. L-system": "**3. L-system.**",
        "## Cantor set": "**Cantor set.**",
        "## Sierpiński triangle": "**Sierpiński triangle.**",
        "## Cantor set dimension": "**Cantor set dimension.**",
        "## Sierpiński triangle dimension": "**Sierpiński triangle dimension.**",
        "## Example 1: Branching trees": "**Example 1: branching trees.**",
        "## Across forests and trees": "**Across forests and trees.**",
        "## Within one tree": "**Within one tree.**",
        "## Across species": "**Across species.**",
        "## Example 2: Scale-free networks": "**Example 2: scale-free networks.**",
        "## Example 3: Zipf’s law": "**Example 3: Zipf’s law.**",
        "## More examples": "**Further examples.**",
    },
    "week03/L_Reaction_diffusion.ipynb": {
        "### How does form emerge?": "### Emergence of form",
        "## What exactly is a pattern?": "## Describing a pattern",
        "## What changes when we coarse-grain?": "## Consequences of coarse-graining",
        "### Which cells count as neighbours?": "### Choice of neighbourhood",
        "### Why does this produce diffusion?": "### Why the stencil produces diffusion",
        "### What counts as an explanation here?": "### Evidence for the mechanism",
        "#### Can everyone recover the same information?": "#### Recovering the stored field",
        "#### 1. Reaction": "**1. Reaction.**",
        "#### 2. Diffusion": "**2. Diffusion.**",
        "#### 3. Feed and removal": "**3. Feed and removal.**",
        "#### Feed $f$": "**Feed $f$.**",
        "#### Kill $k$": "**Kill $k$.**",
        "#### Inspect the stored values": "**Inspect the stored values.**",
        "#### Recovering the stored field": "**Recovering the stored field.**",
        "#### Design colour deliberately": "**Design colour deliberately.**",
        "## Related mechanisms, different patterns": "**Related mechanisms, different patterns.**",
        "## Similar patterns, different mechanisms": "**Similar patterns, different mechanisms.**",
        "## Convection cells": "**Convection cells.**",
        "## Cell-like partitions": "**Cell-like partitions.**",
        "## Folded surfaces": "**Folded surfaces.**",
        "## Travelling waves": "**Travelling waves.**",
        "### Brownian motion: the physical phenomenon": "**Brownian motion: the physical phenomenon.**",
        "### One path: distance from the origin": "**One path: distance from the origin.**",
        "### From one path to an ensemble": "**From one path to an ensemble.**",
        "### Sweep the diffusion coefficient": "**Sweep the diffusion coefficient.**",
        "### Compress each ensemble trajectory": "**Compress each ensemble trajectory.**",
        "### Particle-level ingredients and controls": "**Particle-level ingredients and controls.**",
    },
    "week04/L_Cellular_automata.ipynb": {
        "## Have we already seen cellular-automaton ideas?": "## Earlier cellular-automaton ideas",
        "#### An aside: Do you know binary?": "#### Binary notation",
        "#### An aside: Do you know modulo arithmetic?": "#### Modular arithmetic",
        "### An aside: Do you know what a Turing machine is?": "### Turing machines",
        "### Why Rule 90 damage is exactly a Sierpiński pattern": "### Rule 90 damage forms a Sierpiński pattern",
        "## (Game of) Life is full of surprises!": "## Emergent structures in Game of Life",
        "#### Binary notation": "**Binary notation.**",
        "#### Modular arithmetic": "**Modular arithmetic.**",
        "### Game of Life in action": "**Game of Life in action.**",
        "### Related rules": "**Related rules.**",
        "### Enumerate the state space": "**Enumerate the state space.**",
    },
    "week05/L_ABM.ipynb": {
        "## When is a group a flock?": "## Recognising collective motion",
        "### What does the Heisenberg comparison mean?": "### The Heisenberg comparison",
        "## What goes into an agent-based model?": "## Agent-based model specification",
        "### Why average with complex exponentials?": "### Averaging headings with complex exponentials",
        "## Where is the noise added? · angular noise": "## Angular noise",
        "### Why did the order of the transition become a debate?": "### The debate over transition order",
        "## Where is the noise added? · vectorial noise": "## Vectorial noise",
        "## Continuous or discontinuous?": "## Diagnosing transition order",
        "## Why did the diagnosis change?": "## Why the diagnosis changed",
        "### Finite-size scaling: benchmark or phenomenon?": "### Finite-size scaling",
        "## What does the model establish?": "## What the model establishes",
        "### What happened after the minimal model?": "### Later Vicsek variants",
    },
    "week06/L_Synchronisation.ipynb": {
        "### What the analytical result adds": "### Role of the analytical result",
        "##### What changes with $N$?": "##### Effect of population size",
        "### Drone shows: choreography or swarm?": "### Drone shows: choreography and swarm control",
    },
    "week07/L_Intelligent_systems.ipynb": {
        "## What is an intelligent system?": "## Defining an intelligent system",
        "## So how would you model this?": "## Modelling ant search",
        "### From ant routes to the travelling salesman problem": "**From ant routes to the travelling salesman problem.**",
        "### Data": "**Data.**",
        "### Models": "**Models.**",
        "## Form (shape/structure)": "**Form: shape and structure.**",
        "## Process (behaviour/mechanism)": "**Process: behaviour and mechanism.**",
        "## System (relationships/ecology)": "**System: relationships and ecology.**",
        "### The search space ": "**The search space.**",
        "### Fitness function (aka objective function, cost function)": "**Fitness function (objective or cost function).**",
        "### Moving through the search space": "**Moving through the search space.**",
        "### Exploration and Exploitation": "**Exploration and exploitation.**",
        "### Velocity update": "**Velocity update.**",
        "### Randomness": "**Randomness.**",
        "### Limitations and considerations": "**Limitations and considerations.**",
        "### Read the original PSO paper": "**Read the original PSO paper.**",
    },
    "week08/L_Critical_phenomena.ipynb": {
        "## What changes at a critical point?": "## Behaviour near a critical point",
        "## Why coarse-grain?": "## Coarse-graining",
        "### Behaviour in Space": "### Spatial structure",
        "### Behaviour in events": "### Avalanche sizes",
        "### Behaviour in Time": "### Avalanche activity over time",
        "### Noise & spectra (quick recap)": "### Power spectra",
        "### Finding $\\beta$": "### Estimating the spectral exponent",
        "### Summary": "### Evidence for scale-free behaviour",
        "#### A slightly more complicated model: with regrowth of trees": "#### Regrowth variant",
        "### Diverging correlations": "**Diverging correlations.**",
        "### Scale language": "**Scale language.**",
        "### Critical exponents": "**Critical exponents.**",
        "#### Regrowth variant": "**Regrowth variant.**",
    },
    "week09/L_InformationTheory.ipynb": {
        "# Information Theory": "# Information theory",
        "## WHAT exactly is 'complexity'?": "## Meanings of complexity",
        "## WHERE is 'complexity'?": "## Locating complexity",
        "## WHY do we want to measure 'complexity'?": "## Reasons to measure complexity",
        "## HOW do we measure 'complexity'?": "## Measuring complexity",
        "### Why call it entropy?": "### The name entropy",
        "## A fair die": "### Fair die",
        "## A loaded die": "### Loaded die",
        "## What should surprise do?": "## Self-information",
        "### Recall: Expected value": "**Recall: expected value.**",
        "### Shannon Entropy, $H(X)$": "### Shannon entropy, $H(X)$",
        "### Examples": "**Examples.**",
        "#### Comparing": "**Comparing distributions.**",
        "### Summarising": "**Summary.**",
        "### Absolute meaning": "**Absolute interpretation.**",
        "### Relative meaning": "**Relative interpretation.**",
        "### Interpretation in practice": "**In practice.**",
        "### Permutation entropy: a small example": "**Small example.**",
        "## A brief origin story": "## Origins of information theory",
        "## Many others too": "## Further information measures",
        "## Putting it all together": "## Relationships among information measures",
        "## Applications": "## Estimating information from data",
        "## Data in general": "## Choosing the variables",
        "### Fair die": "**Fair die.**",
        "### Loaded die": "**Loaded die.**",
        "### Entropy as expected surprise": "**Entropy as expected surprise.**",
        "### Time-series measures": "**Time-series measures.**",
    },
    "week10/L_Game_theory.ipynb": {
        "## What should each player choose?": "## Individual incentives",
        "## What about the greater good?": "## Collective outcomes",
        "## Games": "## Elements of a game",
        "## Reality": "## Limits of the model",
        "### Strategy": "**Strategy.**",
        "### Payoff functions": "**Payoff functions.**",
        "### Payoff matrix": "**Payoff matrix.**",
        "## One encounter is a game": "**One encounter is a game.**",
        "## From one game to a population": "**From one game to a population.**",
        "## Elements of a game played by agents on a lattice": "**Elements of a game played by agents on a lattice.**",
        "## Elements of a game in biological systems": "**Elements of a game in biological systems.**",
        "## Assumptions": "**Assumptions.**",
        "## Outcomes": "**Outcomes.**",
        "## Frame the Prisoner’s Dilemma as a game": "**Frame the Prisoner’s Dilemma as a game.**",
        "## The rules of the game": "**The rules of the game.**",
        "## Payoff structure": "**Payoff structure.**",
        "## Payoff matrix (normal form)": "**Payoff matrix (normal form).**",
        "## Payoff plane": "**Payoff plane.**",
        "## Individual incentives": "**Individual incentives.**",
        "## Nash equilibrium": "**Nash equilibrium.**",
        "## Pareto optimum": "**Pareto optimum.**",
        "## Collective outcomes": "**Collective outcomes.**",
        "## Generalising the payoff": "**Generalising the payoff.**",
        "## Prisoner’s dilemmas outside prison": "**Prisoner’s dilemmas outside prison.**",
        "## Read a $2\\times2$ payoff table": "**Read a $2\\times2$ payoff table.**",
        "## The Prisoner’s Dilemma is one 2 × 2 game": "**The Prisoner’s Dilemma is one $2\\times2$ game.**",
        "## Limits of the model": "**Limits of the model.**",
    },
}


DISCUSSION = (
    '<div class="discussion-marker"><img src="images/discussion_marker.svg" '
    'alt="Discussion prompt"><span>{}</span></div>'
)


def update_notebook(relative: str, replacements: dict[str, str]) -> None:
    path = ROOT / "notebooks" / relative
    notebook = json.loads(path.read_text())

    for index, cell in enumerate(notebook["cells"]):
        if cell.get("cell_type") != "markdown":
            continue
        source = "".join(cell.get("source", []))
        for old, new in replacements.items():
            source = source.replace(old, new)

        if relative.startswith("week01/"):
            source = source.replace(
                "**Newton's question:** Can familiar mathematical principles explain Kepler's empirical law?",
                "**Newton's problem:** explain Kepler's empirical law using general mathematical principles.",
            )
            prompt = "Was this trajectory typical, or did the initial state and random moves make it unusual?"
            rendered_prompt = DISCUSSION.format(prompt)
            if rendered_prompt not in source:
                source = source.replace(prompt, rendered_prompt)
            source = source.replace("## Take it with you\n## A short transfer exercise", "## A short transfer exercise")
            if index == 34 and source.startswith("## Complex systems as a field"):
                source = source[len("## Complex systems as a field"):].lstrip("\n")

        if relative.startswith("week02/"):
            source = source.replace(
                "To identify one location to a chosen precision, how many independent numbers must we provide?",
                "The number of independent coordinates needed to locate a point provides a useful starting interpretation of dimension.",
            )
            source = source.replace(
                "The recurring mathematical question is:\n\n> Does the same relationship remain useful when the scale of observation or system size changes?",
                "The recurring mathematical test is whether the same relationship remains useful when the scale of observation or system size changes.",
            )
            source = source.replace(
                "<h3>What kind of variable is measured?</h3>",
                "<p><strong>Variable type.</strong></p>",
            ).replace(
                "<h3>What could scale here?</h3>",
                "<p><strong>Candidate scaling quantities.</strong></p>",
            ).replace(
                "<h3>Across forests and trees</h3>",
                "<p><strong>Across forests and trees.</strong></p>",
            )
            if index == 51:
                source = source.replace("## Three descriptions, three emphases\n\n", "")

        if relative.startswith("week03/") and index == 108:
            source = source.replace("## Return to the Gray–Scott simulation\n\n", "")

        if relative.startswith("week04/"):
            source = source.replace(
                '<div style="border-left: 4px solid #1e70bf; padding: 0.75em; background-color: #eaf3fb; margin-bottom: 1em;">\n'
                '  <strong>Play:</strong><br>\n'
                '    Can you find an undiscovered emergent pattern like a glider gun or puffer train? \n'
                '</div>',
                DISCUSSION.format(
                    "Can you find an emergent pattern such as a glider gun or puffer train?"
                ),
            )
            if index == 43 and source.startswith("## Cellular automata"):
                source = source[len("## Cellular automata"):].lstrip("\n")

        if relative.startswith("week08/"):
            if index == 24:
                source = source.replace("## Sandpile models\n\n", "")
            if index == 32:
                tags = cell.setdefault("metadata", {}).setdefault("tags", [])
                if "slides-only" not in tags:
                    tags.append("slides-only")

        if relative.startswith("week06/"):
            source = source.replace(
                "Why stop at two?\n\nFor $N$ all-to-all coupled phase oscillators, the Kuramoto model is",
                "The same idea extends from a pair to a population. For $N$ all-to-all coupled phase oscillators, the Kuramoto model is",
            )
            source = source.replace(
                "> **Discuss:** Is Spin Wheels an agent-based model or a cellular automaton?",
                DISCUSSION.format("Is Spin Wheels an agent-based model or a cellular automaton?"),
            )

        if relative.startswith("week09/"):
            source = source.replace(
                "<h3>What do we mean by complexity?</h3>",
                "<p><strong>Complexity in this topic.</strong></p>",
            )
            source = source.replace(
                '<p>Suppose 2 occurs with probability $2/3$ and every other face with probability $1/15$.</p>'
                '<p>Seeing 2 is less surprising than seeing 5.</p>'
                '<p><strong>How should surprise depend on probability?</strong></p>',
                '<p>Suppose 2 occurs with probability 2⁄3 and every other face with probability 1⁄15. '
                'Seeing 2 is less surprising than seeing 5.</p>'
                + DISCUSSION.format("How should surprise depend on probability?"),
            )
            source = source.replace(
                "Having defined the surprise of a single outcome, we now ask: *What is the average surprise if we observe the system many times?*",
                "Having defined the surprise of one outcome, we now average it over many observations.",
            )
            if source.strip() == "So which dice - the fair or the loaded one - has a higher entropy?":
                source = DISCUSSION.format("Which has higher entropy: the fair die or the loaded die?")
            source = source.replace(
                '<div class="image-panel"><img src="images/Entropy_VennDiagram.png" alt="Relationship between joint, conditional and mutual information" style="max-height:390px"></div>\n'
                '<div class="text-panel"><p>Joint entropy contains uncertainty from both variables.</p><p>Mutual information is the shared part: how much knowing one variable reduces uncertainty about the other.</p></div>',
                '<div class="image-panel"><img src="images/Entropy_VennDiagram.png" alt="Relationship between joint, conditional and mutual information" style="max-height:250px"></div>\n'
                '<div class="text-panel"><p>Joint entropy is the union of the two circles.</p>'
                '<p>Mutual information is the shared part: how much knowing one variable reduces uncertainty about the other.</p></div>\n'
                '</div>\n\n'
                '$$H(X,Y)=H(X\\mid Y)+I(X;Y)+H(Y\\mid X).$$',
            )
            source = source.replace(
                '<div class="text-panel"><h3>From values to ordinal patterns</h3><p>Short windows are replaced by the order in which their values occur.',
                '<div class="text-panel"><p>Short windows are replaced by the order in which their values occur.',
            )
            source = source.replace(
                '<div class="text-panel"><h3>Animal interactions</h3><p>Trajectory time series can reveal',
                '<div class="text-panel"><p>Trajectory time series can reveal',
            )
            source = source.replace(
                '$$H(X,Y)=H(X\\mid Y)+I(X;Y)+H(Y\\mid X).$$\n</div>',
                '$$H(X,Y)=H(X\\mid Y)+I(X;Y)+H(Y\\mid X).$$',
            )
            source = source.replace(
                'src="images/Entropy_VennDiagram.png"',
                'src="images/Entropy_VennDiagram.svg"',
            ).replace(
                'style="max-height:250px"',
                'style="width:min(100%,520px);max-height:220px"',
            ).replace(
                'style="max-height:220px"',
                'style="width:min(100%,520px);max-height:220px"',
            )

        cell["source"] = source

    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


def main() -> None:
    for relative, replacements in HEADING_REPLACEMENTS.items():
        update_notebook(relative, replacements)


if __name__ == "__main__":
    main()
