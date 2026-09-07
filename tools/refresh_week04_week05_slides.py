#!/usr/bin/env python3
"""Refresh the Week 4 and Week 5 slide paths without thinning the Reader."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
WEEK04 = ROOT / "notebooks/week04/L_Cellular_automata.ipynb"
WEEK05 = ROOT / "notebooks/week05/L_ABM.ipynb"


def md(source: str, cell_id: str, *, slide_type: str = "subslide"):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = ["slides-only"]
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


def reader_md(source: str, cell_id: str):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = ["reader-only"]
    cell.metadata["slideshow"] = {"slide_type": "skip"}
    return cell


def reader_code(source: str, cell_id: str):
    cell = nbf.v4.new_code_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = ["reader-only", "hide-input"]
    cell.metadata["slideshow"] = {"slide_type": "skip"}
    return cell


def keep_reader_remove_old_slides(nb):
    """Keep old explanatory cells in the Reader but remove their old slide path."""
    for cell in nb.cells[1:]:
        slide_type = cell.metadata.get("slideshow", {}).get("slide_type", "")
        if slide_type in {"slide", "subslide", "fragment"}:
            tags = list(cell.metadata.get("tags", []))
            tags = [tag for tag in tags if tag != "slides"]
            if "reader-only" not in tags:
                tags.append("reader-only")
            cell.metadata["tags"] = tags
            cell.metadata["slideshow"] = {"slide_type": "skip"}


def prepare_week04_reader(nb):
    """Keep the Week 4 Reader hierarchy and argument stable across refreshes."""
    by_id = {cell.get("id"): cell for cell in nb.cells}

    # Begin with cellular automata, then define their ingredients without
    # interrupting that sequence with a second historical introduction.
    by_id["0df9920e"]["source"] = r"""# Cellular automata

An **automaton** is a system whose state changes according to a rule. A **cellular automaton** places many automata on a lattice and couples them through local neighbourhoods. To define one we must specify its world, state set, neighbourhood or network, boundary conditions, update rule and clock.
"""
    by_id["0624ee38"]["source"] = r"""## Von Neumann's cellular automaton

John von Neumann sought a logical model of machine self-reproduction. At Stanislaw Ulam's suggestion he used a grid of interacting cells, establishing the cellular-automaton framework.

Von Neumann's construction is much richer than the binary automata used later in this chapter: each cell has 29 possible states, including states that transmit signals and construct new structures. The full state set and transition rules are summarised on [**Wikipedia's von Neumann cellular automaton page**](https://en.wikipedia.org/wiki/Von_Neumann_cellular_automaton).

![Ulam and von Neumann](images/Ulam_vonNeumann.png)
"""
    by_id["66673adf"]["source"] = r"""Cellular automata are spatially distributed dynamical systems with discrete space, time and state. They are simple to define and straightforward to simulate, but can generate dynamics that are difficult to anticipate.

The ingredients below are modelling choices. A cellular automaton is not specified by its update rule alone.
"""
    by_id["36d6c344-f73f-4ef4-bc91-0735a524724c"]["source"] = r"""## Neighbourhood or network

Which cells can influence a focal cell? The same local neighbourhood template is normally used at every lattice site. Its geometry defines the interaction network.
"""
    by_id["8931ea53"]["source"] = r"""## Update rule, boundary and clock

The states in the neighbourhood feed into a state-transition function. We must also decide what happens at the edge of the world and whether cells update synchronously or asynchronously.
"""

    by_id["8429143f"]["source"] = r"""# Wolfram's elementary cellular automata

Stephen Wolfram studied a deliberately restricted family: a one-dimensional line of binary cells, a radius-one neighbourhood, synchronous time and one deterministic local rule. This gives only 256 possible rules, so the complete rule space can be enumerated rather than sampled.

Wolfram used this small family to ask how much behaviour simple programs can generate. The analysis became extensive: his 2002 book *A New Kind of Science* contains about 800 pages of main text and nearly 400 pages of notes, with cellular automata recurring throughout the argument.

The scale of that study is not evidence that all of its classifications or broader claims are settled. It shows why elementary cellular automata became a major test bed for emergence, computation and unpredictability.

<p class="media-credit">Wolfram, S. (2002), <a href="https://www.wolframscience.com/nks/"> <em>A New Kind of Science</em></a>. The complete book is available online.</p>
"""
    by_id["e129a7c8-4372-4c91-9628-72a15763a134"]["source"] = r"""They are not the first cellular automata. Their value here is that the family is small enough to define exactly while still containing fixed, periodic, chaotic-looking and long-lived localised behaviour.
"""

    # These short preliminary definitions are now absorbed into the coherent
    # cellular-automaton introduction above.
    nb.cells = [
        cell for cell in nb.cells
        if cell.get("id") not in {"aeb107aa", "c38ca9df", "469ee4d7-cc6a-4e8d-bbcb-13e81e53c6b6", "10a99041-5b7f-4114-b153-373b014c7197"}
    ]

    # Classes are parallel categories and therefore belong at one depth.
    for cell_id, label in [
        ("9fab7c50-ed05-482a-a086-60ed70b0ac0a", "Class 1"),
        ("48fbc5aa-a2b7-4fe1-bbe3-b48a347ac44c", "Class 2"),
        ("84735333-07aa-4267-9749-e42f30d8ee60", "Class 3"),
        ("c48d3b6d-6298-43be-8613-1c075c68a78f", "Class 4"),
    ]:
        by_id[cell_id]["source"] = f"### {label}\n"

    # Explain Conway's compression of the local rule space at first use.
    by_id["b76cc4fc-bd13-4eb6-b175-6b3a4dde73d9"]["source"] = r"""A binary Moore neighbourhood has eight neighbours. Their alive/dead arrangements give $2^8=256$ neighbour configurations; including the focal cell's current state gives $2^9=512$ local configurations.

Conway used an **outer-totalistic rule**: the next state depends only on the focal cell's present state and the *number* of live neighbours, not their arrangement. This compresses the lookup table to two current states and nine possible neighbour counts: 18 cases, summarised by B3/S23.
"""

    by_id["9d28cf15"]["source"] = r"""#### Game of Life in action

The videos make the scale of Life constructions easier to appreciate.

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><iframe src="https://www.youtube.com/embed/C2vgICfQawE" title="Large-scale Conway's Game of Life patterns" style="width:100%; height:315px; border:0;" allowfullscreen></iframe><p>Large-scale patterns</p></div>
<div class="image-panel"><iframe src="https://www.youtube.com/embed/3NDAZ5g4EuU?start=13" title="A clock built in Conway's Game of Life" style="width:100%; height:315px; border:0;" allowfullscreen></iframe><p>A clock built from Life components</p></div>
</div>

- [Opus 1984 explorable](https://www.complexity-explorables.org/explorables/nah-dah-dah-nah-nah-opus-1984/)
- [A Sierpiński triangle in Life](https://www.reddit.com/r/math/comments/fwujar/conways_game_of_life_forms_a_sierpiński_triangle/)
- [A comprehensive reference on the Game of Life](https://doi.org/10.1007/978-1-84996-217-9)
"""

    by_id["3cd97a8a"]["source"] = r"""## A cellular automaton in living skin

![Cellular-automaton-like dynamics in ocellated lizard skin](images/Lizard_cellular_automata.png)

As an ocellated lizard develops, individual scales switch between green and black depending on the colours of nearby scales. A discrete scale-level model reproduces these neighbourhood-dependent changes. The model cells are skin scales, not biological cells.

<p class="media-credit">Manukyan, L. et al. (2017), <a href="https://doi.org/10.1038/nature22031">“A living mesoscopic cellular automaton made of skin scales”</a>, <em>Nature</em> 544, 173–179.</p>
"""

    # Present rule space and state space as distinct analysis problems, using
    # the same discussion/answer treatment as the rest of the Reader.
    by_id["d0943696-a64e-4d50-82c3-bb84667c0be3"]["source"] = r"""## Rule space

**Rule space** contains the local update rules available after the state set and neighbourhood have been chosen. If a cell has $k$ possible states and its neighbourhood contains $n$ cells, then there are $k^n$ possible neighbourhood configurations and

$$
k^{k^n}
$$

deterministic local rules.

For an elementary cellular automaton, $k=2$ and $n=3$, so the rule space has $2^{2^3}=256$ members. This can be enumerated. For a binary Moore neighbourhood including the focal cell, $n=9$, so the unrestricted rule space contains $2^{512}$ rules. Exhaustive analysis is no longer reasonable.
"""
    by_id["079918c5-7776-43ae-af9f-03bd78bc2ebb"]["source"] = r"""The formula grows quickly because a rule must assign one of $k$ outputs to every possible local input. Conway's outer-totalistic restriction reduces the binary Moore-neighbourhood rule space from $2^{512}$ unrestricted rules to $2^{18}$ Life-like birth/survival rules.
"""
    by_id["13a0fc9a-f371-4f6c-bd32-e36582053b4e"]["source"] = ""
    by_id["7133d8cf-a293-4f0c-b0a4-b4644a1a6b81"]["source"] = r"""<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>How large are the rule spaces of elementary cellular automata, unrestricted binary Moore-neighbourhood automata, and Life-like outer-totalistic automata?</span></div>
"""
    by_id["fd6b07bc-df79-441f-a093-6380bfdad7e6"]["source"] = r"""<details class="reader-answer"><summary>My answer</summary><div>

- Elementary cellular automata: $2^{2^3}=256$ rules.
- Unrestricted binary Moore-neighbourhood automata: $2^{2^9}=2^{512}$ rules.
- Life-like outer-totalistic automata: $2^9$ birth choices times $2^9$ survival choices, giving $2^{18}=262{,}144$ rules. Conway's Game of Life is B3/S23, one member of this family.

</div></details>
"""
    by_id["16dbb195-7733-4ed4-bf77-3adb37ac31aa"]["source"] = r"""## State space

**State space** contains the complete global configurations available to one chosen rule. A finite $D$-dimensional world with side length $L$ contains $L^D$ cells, so a $k$-state model has

$$
k^{L^D}
$$

global states. For $L$ binary cells in one dimension this is $2^L$; for an $L\times L$ binary world it is $2^{L^2}$.

In principle we can enumerate every state and draw its transition to a successor. In practice this is useful only for very small worlds. A Wolfram state-transition applet can show small one-dimensional cases; even modest two-dimensional worlds become intractable.
"""
    by_id["d95ec0c3-3dc4-4848-b67c-2a95fd9c6733"]["source"] = r"""<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>How does the state-space size change between a binary line of length <em>L</em> and a binary <em>L</em> by <em>L</em> world?</span></div>
"""
    by_id["374ab40f-22df-448b-a8b9-54d51fa4c97f"]["source"] = r"""<details class="reader-answer"><summary>My answer</summary><div>

A binary line has $2^L$ configurations. A binary $L\times L$ world has $2^{L^2}$ configurations. The exponent has changed from the number of cells in a line to the number of cells in the whole two-dimensional world.

</div></details>
"""

    by_id["fc8b2074-95a2-45e1-bbd0-b4dd5b407988"]["source"] = r"""## Analyse a small state space: state-transition diagrams

A **state-transition diagram** treats each complete configuration as a node and the deterministic global update as an arrow to its unique successor. The graph exposes cycles, transient trees, basin sizes and states with no predecessor.

This is a useful exact technique only while the world is small enough to enumerate. The [Wolfram state-transition applet](https://demonstrations.wolfram.com/CellularAutomatonStateTransitionDiagrams/) illustrates finite one-dimensional worlds. It does not scale to a two-dimensional Game of Life world large enough to display its characteristic complexity.
"""
    by_id["4adaf0b1-27b0-4bb2-8c9b-71a33b7855ac"]["source"] = r"""### A. Wolfram cellular automata

For a finite one-dimensional world, enumeration makes the global transition network explicit. Increasing $L$ rapidly makes the diagram too large to draw or inspect.
"""
    by_id["12df2958-9ff7-4d1f-8017-c3d1847e8984"]["source"] = r"""### B. Game of Life: reversibility

The same state-space language lets us ask whether a global update loses information. A configuration has one successor but may have zero, one or several predecessors. A cellular automaton is **reversible** only when every configuration has exactly one predecessor.
"""
    by_id["34543139-cc3e-4d9f-8a34-ca5ec0879265"]["source"] = r"""A reversible global map is both injective and surjective.

![Clean comparison of injective, surjective and bijective mappings](images/injective_surjective_maps.svg)

- Failure of injectivity means distinct histories merge and information is lost.
- Failure of surjectivity means some configurations are unreachable.

The Game of Life is not reversible: many configurations die to the same empty state, and Garden of Eden configurations have no predecessor.
"""
    by_id["877e1e31-49be-4c2f-8261-c2481ef185ca"]["source"] = r"""<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Explore"><span>Rule 240 shifts every state by one cell. Does checking a few small values of <em>L</em> prove reversibility for all larger worlds? What structural argument would?</span></div>
"""
    by_id["18ba9bbb-9d30-4828-b251-7a1743f73ff9"]["source"] = r"""<details class="reader-answer"><summary>My answer</summary><div>

Finite checks alone do not prove the claim. For Rule 240 the local rule is $s_i(t+1)=s_{i-1}(t)$: a shift. On a periodic world its inverse is the opposite shift, so every configuration has exactly one predecessor for every finite $L$.

</div></details>
"""
    by_id["085bafa6-3987-4254-a339-d27ab3ce559b"]["source"] = r"""<div class="reader-note"><strong>Further connection:</strong> cellular automata also motivate the simulation hypothesis and Wheeler's “it from bit” idea. This is an optional conceptual extension, not evidence that the universe is literally a cellular automaton. See <a href="https://theconversation.com/do-we-live-in-a-computer-simulation-like-in-the-matrix-my-proposed-new-law-of-physics-backs-up-the-idea-215552">Do we live in a computer simulation?</a></div>
"""

    # Render the optional video directly; a code cell here created an
    # unnecessary Source dropdown in the published Reader.
    video_id = "f1656c7d-d6a5-4dd7-9a21-b72a41ea7cba"
    video_index = next(i for i, c in enumerate(nb.cells) if c.get("id") == video_id)
    video = nbf.v4.new_markdown_cell(r"""<iframe src="https://www.youtube.com/embed/iE46jKYcI4Y" title="Cellular automata and the simulation hypothesis" style="width:100%; height:480px; border:0;" allowfullscreen></iframe>
""")
    video["id"] = video_id
    video.metadata["tags"] = ["reader-only"]
    video.metadata["slideshow"] = {"slide_type": "skip"}
    nb.cells[video_index] = video

    by_id["a643fbc8-c2d3-4ff3-af94-00873a7f1c82"]["source"] = r"""## Cellular automata as computers

Complicated-looking output is not, by itself, computation. Computation requires patterns that can carry information and interactions that can be organised into reliable operations.

In the Game of Life, gliders can encode signals; collisions can implement logic gates; stable and periodic structures can store or regulate information; and glider guns can provide repeated inputs. These components can be assembled to simulate a universal Turing machine. Rule 110 is also computationally universal, although its elementary update rule is even smaller.

The important implication is not that every complex cellular automaton is a computer. It is that a fixed local rule can support controllable information processing when the right persistent structures and interactions exist.
"""
    by_id["f637dad9-ed6a-4aac-bb13-958c7b216f43"]["source"] = r"""### Turing completeness

A system is **Turing complete** when it can simulate any computation that a Turing machine can perform, given enough time and memory. For cellular automata this is demonstrated by constructing encodings for information, logic and memory inside the evolving cell pattern.

This is a stronger claim than unpredictability, irregularity or long transients. Those behaviours may make a system interesting, but they do not establish computational universality.
"""

    # Put computation after the dynamical and analytical material rather than
    # interrupting the classification sequence.
    computation_ids = {
        "a643fbc8-c2d3-4ff3-af94-00873a7f1c82",
        "f637dad9-ed6a-4aac-bb13-958c7b216f43",
    }
    block = [cell for cell in nb.cells if cell.get("id") in computation_ids]
    nb.cells = [cell for cell in nb.cells if cell.get("id") not in computation_ids]
    target = next(i for i, c in enumerate(nb.cells) if c.get("id") == "8307784e-5171-45a1-add9-2cffdd82a470")
    nb.cells[target:target] = block


def rebuild_week04():
    nb = nbf.read(WEEK04, as_version=4)
    # Remove the compact slide-only sequence produced by an earlier run so the
    # refresh remains idempotent while the deck is refined and regenerated.
    nb.cells = [
        cell for cell in nb.cells
        if not cell.get("id", "").startswith("w4-")
        and not cell.get("id", "").startswith("week04-app-")
        and "Theoretical Question:" not in cell.get("source", "")
        and "my answers" not in cell.get("source", "").lower()
    ]
    prepare_week04_reader(nb)
    keep_reader_remove_old_slides(nb)
    title = nb.cells[0]
    title.metadata["tags"] = ["slides"]
    title.metadata["slideshow"] = {"slide_type": "slide"}

    slides = [
        md(r"""
# A machine with a state

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/self_replicating_machine.png" alt="Von Neumann's self-replicating machine construction" style="max-height:330px"></div>
<div class="text-panel">
<p>An <strong>automaton</strong> is a system whose state changes according to a rule.</p>
<p>A <strong>cellular automaton</strong> places many such systems on a regular lattice and couples them through local neighbourhoods.</p>
<p>Von Neumann's original self-reproducing automaton used 29 cell states. Later canonical models deliberately use much smaller state sets.</p>
</div>
</div>
""", "w4-automaton", slide_type="slide"),

        md(r"""
## Specify the cellular automaton

| Choice | Question |
|---|---|
| World | Where do cells exist? |
| State | What finite information does each cell retain? |
| Neighbourhood or network | Which cells can influence the focal cell? |
| Boundary | What happens at the edge of the world? |
| Update rule | How is the next state determined? |
| Clock | Are updates synchronous or asynchronous? |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>A cellular automaton is specified by this complete set of choices, not by its update rule alone.</span></div>
""", "w4-four-choices"),

        md(r"""
## One local rule, applied everywhere

<p><strong>Local:</strong> a cell reads only its neighbourhood.</p>
<p><strong>Homogeneous:</strong> every cell uses the same rule.</p>
<p><strong>Discrete:</strong> space, time and state are represented by finite steps.</p>
<p><strong>Synchronous:</strong> all next states are calculated from the same current configuration.</p>

The global pattern is generated by repeating the local update; it is not drawn in advance.
""", "w4-local-global"),

        md(r"""
## A family resemblance across earlier weeks

| Earlier example | What carries over | Is it a standard cellular automaton? |
|---|---|---|
| Cantor dust | repeated local geometric replacement | no: the construction rescales nested sets rather than updating finite cell states on one fixed lattice |
| Rule 90 | binary states, a fixed line of cells and one local synchronous rule | yes: its space--time history from a single seed forms a Sierpiński pattern |
| Discretised Gray--Scott | a fixed grid and synchronous local updates | not usually: each cell stores continuous concentrations, so it is better described as a continuous-state lattice model |

This week makes the strict cellular-automaton ingredients explicit: a fixed lattice, finite states, discrete time and a local transition rule.
""", "w4-family-resemblance"),

        md(r"""
# Why cellular automata?

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Ulam_vonNeumann.png" alt="Stanislaw Ulam and John von Neumann" style="max-height:360px"></div>
<div class="text-panel">
<p>John von Neumann asked what a machine would require in order to reproduce itself.</p>
<p>Stanislaw Ulam suggested replacing continuous space with a lattice of interacting cells.</p>
<p>The result became a framework for asking how complicated organisation can arise from simple local rules.</p>
</div>
</div>
""", "w4-history", slide_type="slide"),

        md(r"""
# Wolfram's elementary cellular automata

Wolfram restricted the general framework to a family that can be searched exhaustively:

| Choice | Elementary cellular automaton |
|---|---|
| World | a one-dimensional line |
| State | binary: $0$ or $1$ |
| Neighbourhood | left, focal and right cells |
| Clock and rule | synchronous and deterministic |

The eight possible neighbourhoods require eight binary outputs, giving $2^8=256$ rules.

His 2002 *A New Kind of Science* contains about 800 pages of main text and nearly 400 pages of notes. Elementary cellular automata are the small test bed used repeatedly to study how simple programs generate complicated behaviour.

<p class="media-credit">Wolfram, S. (2002), <a href="https://www.wolframscience.com/nks/"><em>A New Kind of Science</em></a>.</p>
""", "w4-eca", slide_type="slide"),

        md(r"""
## Rule 90 reconnects to Sierpiński

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/rule_90_plot.png" alt="Rule 90 space-time history forming a Sierpiński triangle pattern" style="max-height:410px"></div>
<div class="text-panel">
<p>Rule 90 updates the focal cell using the exclusive-or of its left and right neighbours:</p>
<p>$$x_i^{t+1}=x_{i-1}^{t}\mathbin{\mathrm{XOR}}x_{i+1}^{t}.$$</p>
<p>From one live seed, its space--time history reproduces the Sierpiński pattern seen in Week 2.</p>
<p>The fractal is now generated dynamically on a fixed lattice.</p>
</div>
</div>
""", "w4-rule90-sierpinski"),

        md(r"""
## Read Rule 30 from its rule number

| Neighbourhood | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Rule 30 output | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |

For Rule 30, reading the eight outputs as a binary number gives

$$00011110_2=30_{10}.$$

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>For Rule 30, which three cells form the neighbourhood, and what output should the focal cell take for neighbourhood 011?</span></div>
""", "w4-rule-number"),

        md(r"""
## Rule 50: read a complete trajectory

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/Rule50.png" alt="Space-time history generated by elementary cellular automaton Rule 50" style="max-height:430px"></div>
<div class="text-panel">
<p>One row is the state of the whole line.</p>
<p>The next row is produced by applying Rule 50 simultaneously at every site.</p>
<p>Repeating motifs and their boundaries are clearer in the space--time history than in one configuration.</p>
</div>
</div>
""", "w4-rule50"),

        md(r"""
## Turn time into a second spatial axis

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Class_3.png" alt="Space-time diagram for an irregular elementary cellular automaton" style="max-height:420px"></div>
<div class="text-panel">
<p>Each row is one complete configuration.</p>
<p>The row below is obtained by applying the same local rule once.</p>
<p>This representation compresses the trajectory into one image and makes growth, repetition and irregularity visible.</p>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over time:</strong> stack successive states to reveal a system-level pattern.</span></div>
""", "w4-space-time"),

        md(r"""
## Explore a one-dimensional cellular automaton

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://www.complexity-explorables.org/explorables/kelp/" title="Kelp one-dimensional cellular automaton explorable" style="width:100%; height:430px; border:1px solid #C7CEDC;"></iframe></div>
<div class="text-panel">
<p><strong>Kelp</strong> grows a two-dimensional record from a one-dimensional local rule.</p>
<p>The resulting branching form also reconnects this week to fractals: repeated local updates create structure across several visible scales.</p>
<p><a href="https://www.complexity-explorables.org/explorables/kelp/" target="_blank" rel="noopener">Open the explorable in a new tab</a></p>
</div>
</div>
""", "w4-kelp"),

        md(r"""
## Classify behaviour when enumeration fails

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/All_classes.png" alt="Examples of the four Wolfram behaviour classes" style="max-height:420px"></div>
<div class="text-panel">
<p><strong>Class 1:</strong> approaches a uniform state.</p>
<p><strong>Class 2:</strong> settles into fixed or periodic structures.</p>
<p><strong>Class 3:</strong> produces persistent irregularity.</p>
<p><strong>Class 4:</strong> supports long-lived local structures and interactions.</p>
</div>
</div>
""", "w4-classes"),

        md(r"""
# Conway's Game of Life

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Conway_notes.webp" alt="John Conway's notes for the Game of Life" style="max-height:390px"></div>
<div class="text-panel">
<p><strong>World:</strong> a two-dimensional square lattice.</p>
<p><strong>State:</strong> dead or alive.</p>
<p><strong>Neighbourhood:</strong> eight surrounding cells.</p>
<p><strong>Clock:</strong> synchronous discrete updates.</p>
</div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Eight binary neighbours have $2^8=256$ possible arrangements. Including the focal cell gives $2^9=512$ local configurations. How might Conway compress that rule table?</span></div>
""", "w4-gol", slide_type="slide"),

        md(r"""
## The update rule · B3/S23

| Current state | Live neighbours | Next state |
|---|---:|---|
| Dead | exactly 3 | alive: birth |
| Alive | 2 or 3 | alive: survival |
| Any other case | otherwise | dead |

The shorthand B3/S23 records the birth and survival counts.

This is an <strong>outer-totalistic</strong> rule: only the focal cell's current state and the number of live neighbours matter, not their arrangement.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Predict the next state of one small configuration before running the model.</span></div>
""", "w4-gol-rule"),

        md(r"""
## Explore a two-dimensional cellular automaton

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://www.complexity-explorables.org/explorables/nah-dah-dah-nah-nah-opus-1984/" title="Opus 1984 two-dimensional cellular automaton explorable" style="width:100%; height:430px; border:1px solid #C7CEDC;"></iframe></div>
<div class="text-panel">
<p>Opus 1984 provides an interactive two-dimensional cellular automaton.</p>
<p><a href="https://www.complexity-explorables.org/explorables/nah-dah-dah-nah-nah-opus-1984/" target="_blank" rel="noopener">Open the explorable in a new tab</a></p>
</div>
</div>
""", "w4-opus"),

        md(r"""
## A small rule supports several kinds of object

| Object | Example | Behaviour |
|---|---|---|
| Still life | <img src="images/Beehive.png" alt="A stable beehive pattern" style="height:105px"> | unchanged |
| Oscillator | <img src="images/Toad.png" alt="A period-two toad oscillator" style="height:105px"> | repeats in place |
| Spaceship | <img src="images/Animated_glider_emblem.gif" alt="A moving glider" style="height:105px"> | repeats after translating |
""", "w4-gol-objects"),

        md(r"""
## Interactions create computation

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Gospers_glider_gun.gif" alt="Gosper glider gun producing gliders" style="max-height:390px"></div>
<div class="text-panel">
<p>A glider gun periodically emits moving structures.</p>
<p>Signals can collide, persist, disappear or redirect one another.</p>
<p>Carefully constructed glider streams and collisions can implement logic gates and memory. That controllable information processing, not visual complexity alone, makes the Game of Life computationally universal.</p>
</div>
</div>
""", "w4-gol-computation"),

        md(r"""
## A long transient from a tiny seed

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/r_pentomino.png" alt="The R-pentomino initial pattern" style="max-height:300px"></div>
<div class="text-panel">
<p>The R-pentomino contains only five live cells but takes 1,103 generations to stabilise.</p>
<p>Small initial differences can therefore create long, difficult-to-predict transients.</p>
<p>Local simplicity does not imply short or transparent global behaviour.</p>
</div>
</div>
""", "w4-methuselah"),

        md(r"""
# Rule 30 and a growing shell

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Class_3.png" alt="Rule 30 space-time evolution"><p><strong>Rule 30:</strong> each new row is produced from a one-dimensional local rule.</p></div>
<div class="image-panel"><img src="images/Textile_cone.jpeg" alt="Pattern on a textile cone snail"><p><strong>Textile cone:</strong> each new band of shell records pigment activity along a one-dimensional growing edge.</p></div>
</div>

The representation is biologically meaningful, but resemblance does not establish that the animal uses Rule 30 or the same local mechanism.
""", "w4-real-rule30", slide_type="slide"),

        md(r"""
## A shell records its growth history

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Textile_cone.jpeg" alt="Pigmentation pattern on a textile cone shell" style="max-height:390px"></div>
<div class="text-panel">
<p>New shell is laid down along the growing edge. The finished surface is therefore a space–time record of pigment activity along that edge.</p>
<p>Cellular automata can reproduce shell-like bands, waves and irregular motifs. Rule 30 is a useful comparison, not an identified biological rule.</p>
</div>
</div>
<p class="media-credit">Kusch, I. and Markus, M. (1996), <a href="https://doi.org/10.1006/jtbi.1996.0029">“Mollusc shell pigmentation: cellular automaton simulations and evidence for undecidability”</a>, <em>Journal of Theoretical Biology</em> 178, 333–340; Boettiger, A. N., Ermentrout, B. and Oster, G. (2009), <a href="https://doi.org/10.1073/pnas.0810311106">“The neural origins of shell structure and pattern in aquatic mollusks”</a>, <em>PNAS</em> 106, 6837–6842.</p>
""", "w4-shell"),

        md(r"""
# Traffic on one lane

The Nagel–Schreckenberg model represents a <strong>single lane as a one-dimensional periodic lattice</strong>. Each site is empty or contains one car with an integer speed.

| Synchronous step | Local rule |
|---|---|
| Accelerate | increase speed towards $v_{\max}$ |
| Avoid collision | limit speed to the empty gap ahead |
| Brake randomly | reduce a positive speed by one with probability $p$ |
| Move | advance by the updated speed |

There is no overtaking, lane changing or interaction across lanes in the original model.
""", "w4-traffic-rule", slide_type="slide"),

        md(r"""
## The original space–time diagrams

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/nagel_schreckenberg_original_excerpt.png" alt="Character-based space-time diagrams from Nagel and Schreckenberg" style="max-height:430px"></div>
<div class="text-panel">
<p>Each row is the road one step later. A dot is empty road; a digit is a car's speed.</p>
<p>The encoding exposes individual updates, but the jam boundary and aggregate change are difficult to compare by eye.</p>
</div>
</div>
<p class="media-credit">Nagel, K. and Schreckenberg, M. (1992), <a href="https://doi.org/10.1051/jp1:1992277">“A cellular automaton model for freeway traffic”</a>, <em>Journal de Physique I</em> 2, 2221–2229, Figures 1–2.</p>
""", "w4-traffic-original"),

        md(r"""
## Replot the same model

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/nagel_schreckenberg_redesign.png" alt="Modern space-time and flow-density visualisations of the Nagel-Schreckenberg model" style="max-height:430px"></div>
<div class="text-panel">
<p><strong>Site state:</strong> empty or occupied.</p>
<p><strong>Density:</strong> the fraction of all road sites occupied.</p>
<p><strong>Flow:</strong> cars passing a location per time step.</p>
<p>The local view reveals backward-moving jams; the aggregate view reveals the capacity peak.</p>
</div>
</div>
""", "w4-traffic-redesign"),

        md(r"""
## A cellular automaton in living skin

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Lizard_cellular_automata.png" alt="Cellular-automaton-like dynamics in ocellated lizard skin" style="max-height:390px"></div>
<div class="text-panel">
<p>Ocellated-lizard scales switch colour as the animal develops.</p>
<p>A discrete scale-level model can reproduce the observed neighbourhood-dependent dynamics.</p>
<p>The cells of the model are scales, not biological cells.</p>
</div>
</div>
<p class="media-credit">Manukyan, L. et al. (2017), <a href="https://doi.org/10.1038/nature22031">“A living mesoscopic cellular automaton made of skin scales”</a>, <em>Nature</em> 544, 173–179.</p>
""", "w4-lizard"),

        md(r"""
# Two spaces organise the analysis

<div class="two-panel equal-panels compact-panels">
<div class="text-panel">
<h3>Rule space</h3>
<p>All possible local update rules for a chosen state set and neighbourhood.</p>
<p>For elementary CA: 256 rules.</p>
</div>
<div class="text-panel">
<h3>State space</h3>
<p>All possible global configurations for a chosen finite world.</p>
<p>For $L$ binary cells: $2^L$ states.</p>
</div>
</div>

For $k$ states and a neighbourhood of $n$ cells, rule space has $k^{k^n}$ deterministic rules. A finite $D$-dimensional world of side length $L$ has $k^{L^D}$ global states.

Changing the local rule moves through rule space. Evolving one chosen rule moves through state space.
""", "w4-two-spaces", slide_type="slide"),

        md(r"""
## A. Small 1D worlds · state-transition diagrams

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Rule110_state_transition_L5.png" alt="State-transition diagram for Rule 110 on five cells" style="max-height:390px"></div>
<div class="text-panel">
<p>Each node is a complete configuration.</p>
<p>Each arrow points to its unique successor.</p>
<p>A state may have zero, one or several predecessors.</p>
<p>Cycles, basins and unreachable states become visible.</p>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over configurations:</strong> replace individual trajectories with the architecture of the whole state space.</span></div>
""", "w4-transition"),

        md(r"""
## B. Game of Life · reversibility

<div class="two-panel equal-panels compact-panels">
<div class="text-panel">
<p>A global update is <strong>reversible</strong> only when every state has exactly one predecessor.</p>
<p>Most interesting cellular automata merge histories and are therefore irreversible.</p>
</div>
<div class="image-panel"><img src="images/Garden_of_Eden_pattern.png" alt="A Garden of Eden pattern in Conway's Game of Life" style="max-height:300px"><p>A <strong>Garden of Eden</strong> state has no predecessor.</p></div>
</div>
""", "w4-reversibility"),

        md(r"""
# Coarse-grain the Game of Life

Let $p_t$ be the fraction of cells alive at time $t$. If neighbours were independent, the probability of exactly $k$ live neighbours would be binomial. A mean-field update is

$$
p_{t+1}=(1-p_t)\binom83p_t^3(1-p_t)^5
+p_t\!\left[\binom82p_t^2(1-p_t)^6+\binom83p_t^3(1-p_t)^5\right].
$$

The spatial grid has been replaced by one average density.
""", "w4-mean-field", slide_type="slide"),

        md(r"""
## What did the average remove?

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/GoL_meanfield.png" alt="Mean-field approximation compared with Game of Life simulation" style="max-height:390px"></div>
<div class="text-panel">
<p>The approximation can describe a population-level tendency.</p>
<p>It cannot represent gliders, oscillators, collisions or spatial correlations.</p>
<p>Coarse-graining is useful only when the discarded structure is not needed for the question.</p>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over cells:</strong> replace the configuration with an average. <strong>Down:</strong> return to local structure when the average fails.</span></div>
""", "w4-mean-field-loss"),

    ]

    # Establish the concept and its von Neumann origin before enumerating the
    # modelling ingredients. Preserve the remaining argument order.
    opening_ids = [
        "w4-automaton", "w4-history", "w4-four-choices",
        "w4-local-global", "w4-family-resemblance",
    ]
    slide_by_id = {cell.get("id"): cell for cell in slides}
    slides = [slide_by_id[cell_id] for cell_id in opening_ids] + [
        cell for cell in slides if cell.get("id") not in opening_ids
    ]
    # Behaviour classes are an analysis strategy used after exact state-space
    # enumeration has become impractical, not part of the initial definition.
    classes_slide = next(cell for cell in slides if cell.get("id") == "w4-classes")
    slides.remove(classes_slide)
    reversibility_index = next(
        i for i, cell in enumerate(slides) if cell.get("id") == "w4-reversibility"
    )
    slides.insert(reversibility_index + 1, classes_slide)
    nb.cells[1:1] = slides

    # Add fuller, durable Reader material beside the existing real-world examples.
    insertion = next(
        i for i, cell in enumerate(nb.cells)
        if cell.get("id") == "1206cfbb-e19c-4ed5-8b4e-deef02921750"
    ) + 1
    reader_cells = [
        reader_md(r"""
## Have we already seen cellular-automaton ideas?

A cellular automaton in the standard sense has a fixed regular lattice, a finite set of cell states, discrete time, and a local transition rule applied across the lattice. Some earlier models share only part of this structure.

**Cantor dust:** its repeated retain-or-remove construction resembles a local rewrite, but it is not normally classified as a cellular automaton. Each generation describes a newly resolved nested set rather than finite states evolving on one fixed lattice.

**Rule 90 and the Sierpiński triangle:** Rule 90 is a genuine elementary cellular automaton. Each binary cell becomes the exclusive-or of its left and right neighbours. Starting from one live cell, the space--time history forms the Sierpiński pattern. This gives us two routes to similar geometry: an exact replacement construction in Week 2 and a dynamical cellular automaton here.

**The discretised Gray--Scott model:** Week 3 also used a fixed grid, synchronous time steps and local neighbour coupling. The resemblance is useful, but each cell stored real-valued concentrations rather than one of finitely many states, and the update was chosen to approximate a reaction--diffusion PDE. It is therefore better described as a continuous-state lattice dynamical system, or a coupled map lattice, rather than a standard cellular automaton.

These distinctions matter because visually similar algorithms may represent different mathematical objects. This week focuses on the strict finite-state case, while retaining the modelling questions already encountered: what does a cell store, who influences it, how is time updated, and what happens at the boundary?
""", "week04-app-family-resemblance"),
        reader_md(r"""
### Explore a one-dimensional cellular automaton

The [**Kelp explorable**](https://www.complexity-explorables.org/explorables/kelp/) uses a one-dimensional local rule to build a two-dimensional history. Adjust the rule and initial state, then read downwards through time. The branching output also reconnects cellular automata to Week 2: fractal-like structure can be generated by repeated local updates rather than drawn directly.

<iframe src="https://www.complexity-explorables.org/explorables/kelp/" title="Kelp one-dimensional cellular automaton explorable" style="width:100%; height:560px; border:1px solid #C7CEDC;"></iframe>
""", "week04-app-kelp"),
        reader_md(r"""
### Shell pigmentation: a space–time record

A mollusc shell grows by adding new material along its mantle edge. Pigment activity varies along that one-dimensional edge, and successive additions remain fixed in the shell. One direction across the finished shell therefore records position along the growth edge; the other approximately records growth time. This makes a one-dimensional local model biologically meaningful.

The resemblance between the textile cone and Rule 30 is still only a generative analogy. It does not show that the animal implements Rule 30. Kusch and Markus (1996) showed that other local activation and inhibition rules can generate stationary bands, travelling pigment waves and irregular motifs resembling several mollusc shells. The model cells represent positions along the growing edge, not biological cells inside the animal.

The example also gives an important warning. Similar output does not establish a shared mechanism. Boettiger, Ermentrout and Oster (2009) argued that shell patterns should be tied to a physiologically plausible pigment-producing network, because many arbitrary cellular automata can imitate the same finished morphology. The shell is evidence to explain, not proof of one particular rule.

<p class="media-credit">Shell photograph: <em>Conus textile</em>. Kusch, I. and Markus, M. (1996), <a href="https://doi.org/10.1006/jtbi.1996.0029">“Mollusc shell pigmentation: cellular automaton simulations and evidence for undecidability”</a>, <em>Journal of Theoretical Biology</em> 178, 333–340; Boettiger, A. N., Ermentrout, B. and Oster, G. (2009), <a href="https://doi.org/10.1073/pnas.0810311106">“The neural origins of shell structure and pattern in aquatic mollusks”</a>, <em>PNAS</em> 106, 6837–6842.</p>
""", "week04-app-shell"),
        reader_md(r"""
## Traffic as a one-dimensional cellular automaton

Nagel and Schreckenberg's highly cited traffic model is deliberately minimal. The road is a one-dimensional lattice of $L$ sites arranged as a ring. A site is either empty or occupied by one car, and each car has an integer speed $v\in\{0,\ldots,v_{\max}\}$. The original model contains one lane: cars interact only through the empty gap to the next car ahead. It has no overtaking, lane changing or cross-lane interaction. Multi-lane cellular automata are later extensions with additional lane-changing rules.

At every time step all cars update synchronously:

1. **Accelerate:** $v\leftarrow\min(v+1,v_{\max})$.
2. **Avoid collision:** if the gap ahead is $g$, set $v\leftarrow\min(v,g)$.
3. **Brake randomly:** if $v>0$, reduce $v$ by one with probability $p$.
4. **Move:** $x\leftarrow x+v\pmod L$.

The random-braking probability represents small unresolved variations in driver behaviour. Nothing in the rule explicitly creates a traffic jam. At sufficient density, however, a chance brake can force the following car to brake, and that disturbance can propagate backwards while the cars themselves move forwards.

![Character-based traffic diagrams from the original paper](images/nagel_schreckenberg_original_excerpt.png)

The original 1992 figures encode empty sites as dots and cars by digits giving their speeds. This is ingenious and makes the state definition literal, but it is demanding to parse. The congested diagram contains the backward-moving jam, yet its boundary competes visually with hundreds of characters. This is partly a consequence of print conventions at the time, not a flaw in the underlying analysis.

We can retain the model and improve the visual hierarchy. In the plot below, position runs horizontally and time vertically. Moving and stopped cars have distinct encodings. The second panel then moves up the ladder: it replaces each run by its mean flow and compares an ensemble across density.

![A clearer implementation of the Nagel–Schreckenberg model](images/nagel_schreckenberg_redesign.png)

The two views answer different questions. The space–time plot shows *how* a jam forms and travels. The **fundamental diagram** shows the system-level relationship between density and flow: adding cars initially increases throughput, but after the capacity peak congestion reduces it.

Here **density is not the state of one site**. A site is still binary: empty or occupied. Density is the global fraction of road sites occupied by cars, $\rho=N_{\mathrm{cars}}/L$. **Flow** is the average number of cars passing a fixed road position per time step (equivalently, density multiplied by mean speed in this periodic model). The fundamental diagram therefore compares one aggregate measurement from each simulation across different global occupancies.

<p class="media-credit">Nagel, K. and Schreckenberg, M. (1992), <a href="https://doi.org/10.1051/jp1:1992277">“A cellular automaton model for freeway traffic”</a>, <em>Journal de Physique I</em> 2, 2221–2229. Original figure excerpts are reproduced for scholarly discussion; the redesigned plots use the implementation below.</p>
""", "week04-app-traffic"),
        reader_code(r"""
import numpy as np

def nasch_step(positions, speeds, road_length, vmax, brake_probability, rng):
    # Advance a periodic, single-lane Nagel--Schreckenberg model by one step.
    speeds = np.minimum(speeds + 1, vmax)
    gaps = (np.roll(positions, -1) - positions - 1) % road_length
    speeds = np.minimum(speeds, gaps)

    random_brake = (speeds > 0) & (rng.random(len(speeds)) < brake_probability)
    speeds = speeds - random_brake
    positions = (positions + speeds) % road_length

    order = np.argsort(positions)
    return positions[order], speeds[order]
""", "week04-app-traffic-code"),
        reader_md(r"""
### Explore a two-dimensional cellular automaton

The [**Opus 1984 explorable**](https://www.complexity-explorables.org/explorables/nah-dah-dah-nah-nah-opus-1984/) provides an interactive example of a two-dimensional cellular automaton.

<iframe src="https://www.complexity-explorables.org/explorables/nah-dah-dah-nah-nah-opus-1984/" title="Opus 1984 two-dimensional cellular automaton explorable" style="width:100%; height:560px; border:1px solid #C7CEDC;"></iframe>
""", "week04-app-opus"),
    ]
    nb.cells[insertion:insertion] = reader_cells
    nbf.write(nb, WEEK04)


def refresh_week05():
    nb = nbf.read(WEEK05, as_version=4)
    by_id = {cell.get("id"): cell for cell in nb.cells}

    # Remove lecture material that now belongs in the active workshop, and the
    # explicit workflow recap.  The workflow is demonstrated by the sequence
    # of the lecture rather than stated as a separate object.
    nb.cells = [
        cell for cell in nb.cells
        if cell.get("id") not in {"pause-process", "workflow"}
    ]
    by_id = {cell.get("id"): cell for cell in nb.cells}

    major = {
        "title", "agents-before", "three-routes", "vicsek-intro",
        "qualitative", "parameter-sweep",
    }
    for cell in nb.cells:
        if cell.get("id") in major:
            cell.metadata["slideshow"] = {"slide_type": "slide"}
        elif "slides" in cell.metadata.get("tags", []):
            cell.metadata["slideshow"] = {"slide_type": "subslide"}

    by_id["agents-before"].source = r"""
# We have already used agents

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p>Schelling's segregation model represented people individually. Each agent read a local neighbourhood and followed a local update rule.</p></div>
<div class="text-panel"><p>Continuous fields average over individuals. Agent-based models retain identities, locations, attributes and interaction partners.</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What information becomes unavailable when individuals are replaced by a population average?</span></div>
"""

    by_id["flocking-video"].source = r"""
## A classic example: flocking

<iframe width="900" height="455" src="https://www.youtube.com/embed/V4f_1_r80RY" title="Flocking birds" frameborder="0" allowfullscreen></iframe>

Many birds coordinate without a leader or a global view of the flock.
"""

    by_id["three-routes"].source = r"""
# Three routes to flocking

| Perspective | Model | Retained mechanism |
|---|---|---|
| Computer graphics | Reynolds' boids | separation, alignment, cohesion |
| Statistical physics | Vicsek et al. | alignment, noise, phase transition |
| Behavioural biology | Couzin et al. | zones of repulsion, alignment, attraction |

Similar collective motion can arise from different abstractions. We use Vicsek because it isolates the competition between local alignment and noise (and is the simplest).
"""

    # MyST does not parse dollar-delimited mathematics nested inside raw HTML.
    # These compact panels therefore use Unicode for their short expressions;
    # the surrounding mathematical definitions remain proper display maths.
    by_id["ising-to-vicsek"].source = r"""
# From fixed spins to moving agents

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://www.complexity-explorables.org/explorables/i-sing-well-tempered/" title="Ising model explorable" style="width:100%;height:350px;border:1px solid #C7CEDC;"></iframe></div>
<div class="text-panel">
<h3>Ising model</h3>
<p>Each fixed site carries a binary spin, sᵢ ∈ {−1,+1}.</p>
<p>Neighbour agreement lowers the interaction energy; temperature disrupts alignment.</p>
<p>The competition produces ordered and disordered phases.</p>
<p><a href="https://www.complexity-explorables.org/explorables/i-sing-well-tempered/" target="_blank" rel="noopener">Open I Sing Well-Tempered</a></p>
</div>
</div>
"""

    by_id["xy-model"].source = r"""
## From Ising to the XY model

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://www.complexity-explorables.org/explorables/if-you-ask-your-xy/" title="XY model explorable" style="width:100%;height:350px;border:1px solid #C7CEDC;"></iframe></div>
<div class="text-panel">
<p>The <strong>XY model</strong> replaces each binary spin by a continuous angle θᵢ.</p>
<p>Equivalently, each site stores the unit vector (cos θᵢ, sin θᵢ).</p>
<p>Neighbouring orientations tend to align, while temperature introduces disorder. Continuous orientation also permits vortices.</p>
<p><a href="https://www.complexity-explorables.org/explorables/if-you-ask-your-xy/" target="_blank" rel="noopener">Open If You Ask Your XY</a></p>
</div>
</div>
"""

    by_id["abm-ingredients"].source = r"""
## What goes into an agent-based model?

| Ingredient | Question |
|---|---|
| World and state | Where can agents exist, and what does each retain? |
| Interaction network | Who can affect whom? |
| Dynamics and clock | How and when are states updated? |
| Observable | What collective behaviour will be recorded? |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Initialisation, boundaries and random variation are part of these choices too.</span></div>
"""

    by_id["vicsek-intro"].source = r"""
# Build the Vicsek model

Vicsek and colleagues asked what happens when self-propelled particles align with nearby particles while noise perturbs their headings.

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p><strong>Retain:</strong> positions, headings, local neighbours and noise.</p></div>
<div class="text-panel"><p><strong>Remove:</strong> aerodynamics, body shape, vision, memory, leadership and attraction.</p></div>
</div>

The model isolates local alignment as a possible mechanism for collective motion.
"""

    by_id["vicsek-initialise"].source = r"""
## 1. Initialise the world

| Ingredient | Choice |
|---|---|
| World | periodic square of side length $L$ |
| Agents | $N$ point particles with positions $\mathbf x_i$ |
| Motion | constant speed $v$ and heading $\theta_i$ |
| Initial state | random positions and headings |

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Which quantities evolve, and which remain fixed?</span></div>
"""

    by_id["vicsek-neighbours"].source = r"""
## 2. Define the interaction network

$$\mathcal N_i(t)=\{j:d_{\mathrm{torus}}(\mathbf x_i,\mathbf x_j)\le R\}.$$

Agent $j$ influences agent $i$ when their periodic distance is at most $R$. The network changes as the agents move.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Metric distance is one choice. Empirical flocks are often better described by a fixed number of nearest neighbours.</span></div>
"""

    by_id["vicsek-update"].source = r"""
## 3. Apply one synchronous update

$$
\theta_i(t+\Delta t)
=\operatorname{Arg}\!\left(\sum_{j\in\mathcal N_i(t)}e^{\mathrm i\theta_j(t)}\right)+\xi_i(t),
\qquad \xi_i\sim U[-\eta/2,\eta/2].
$$

$$
\mathbf x_i(t+\Delta t)
=\mathbf x_i(t)+v\Delta t(\cos\theta_i(t),\sin\theta_i(t)).
$$

All new headings and positions are calculated from the same state at time $t$, then wrapped into the periodic square.
"""

    by_id["polarisation"].source = r"""
## Quantify collective alignment

$$
\Phi(t)=\frac1N\left|\sum_{i=1}^{N}e^{\mathrm i\theta_i(t)}\right|.
$$

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p><strong>Φ ≈ 0:</strong> headings cancel.</p></div>
<div class="text-panel"><p><strong>Φ ≈ 1:</strong> agents move in nearly the same direction.</p></div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over agents:</strong> replace all individual headings by one system-level measure of alignment.</span></div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Can a visibly organised state still have low polarisation?</span></div>
"""

    by_id["parameter-sweep"].source = r"""
# First sweep the noise

<img src="images/Vicsek_parameter_sweeps.jpeg" alt="Vicsek order parameter as noise and density change" style="max-height:430px">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder again:</strong> compare the system-level order parameter across noise values to reveal a transition.</span></div>
"""

    by_id["ensemble"].source = r"""
## Then repeat each condition

| One run | Ensemble |
|---|---|
| one possible history | a distribution of possible histories |
| exposes local mechanisms | estimates typical behaviour and variation |
| may be atypical | tests whether the pattern recurs |

The sweep asks how behaviour changes across $\eta$. The ensemble asks how reliably those conditions can be compared.
"""

    by_id["improving"].source = r"""
## What does the model establish?

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Cavagna_robust_to_attack.png" alt="Empirical topological interaction network in a starling flock" style="max-height:390px"></div>
<div class="text-panel">
<p>The Vicsek model shows that alignment plus noise can generate collective motion.</p>
<p>It does not establish that real birds use metric-distance alignment.</p>
<p>Starling data instead support interaction with a roughly fixed number of neighbours.</p>
</div>
</div>
"""

    # Restore the historical and scientific argument that linked the spin
    # models to Vicsek, then showed that the noise convention changes the
    # model rather than merely changing its numerical implementation.
    ids = {cell.get("id") for cell in nb.cells}
    if "vicsek-moving-spin-history" not in ids:
        anchor = next(i for i, cell in enumerate(nb.cells) if cell.get("id") == "moving-xy-vicsek")
        history_cell = md(r"""
## A moving spin model

Vicsek later recalled: “...I had designed the moving version of the Heisenberg model.”

The phrase captures the idea: orientations that previously sat on fixed sites now move through space. More precisely, planar headings make the standard Vicsek model XY-like; a Heisenberg spin has three components.

<p class="media-credit">Vicsek, T. (2016), <a href="https://www.nature.com/articles/529016a">“Universality in non-equilibrium systems”</a>, <em>Nature</em> 529, 16–17.</p>
""", "vicsek-moving-spin-history", slide_type="subslide")
        history_cell.metadata["tags"] = ["slides"]
        nb.cells.insert(anchor + 1, history_cell)

    ids = {cell.get("id") for cell in nb.cells}
    if "vicsek-noise-conventions" not in ids:
        anchor = next(i for i, cell in enumerate(nb.cells) if cell.get("id") == "vicsek-update")
        noise_cell = md(r"""
## Where is the noise added?

| Angular noise | Vectorial noise |
|---|---|
| perturb the heading after averaging | perturb the local velocity vector before taking its direction |
| an individual makes a directional error | the locally estimated signal is noisy |

These are different stochastic models, not interchangeable implementations of one rule.
""", "vicsek-noise-conventions", slide_type="subslide")
        noise_cell.metadata["tags"] = ["slides"]
        nb.cells.insert(anchor + 1, noise_cell)
        nb.cells.insert(anchor + 2, reader_md(r"""
The distinction became central to a long debate about the transition. Vicsek et al. (1995) reported a continuous order–disorder transition for their original angular-noise model. Grégoire and Chaté (2004) reported a discontinuous transition and showed that density bands, system size and boundary conditions can obscure the asymptotic behaviour. Other studies found that angular and vectorial noise can produce different apparent transition orders.

The durable lesson is not a single slogan about the order of every Vicsek transition. It is that the noise convention, finite system size, boundaries and sampling protocol are part of the model and of the scientific claim.

<p class="media-credit">Vicsek, T. et al. (1995), <a href="https://doi.org/10.1103/PhysRevLett.75.1226">“Novel Type of Phase Transition in a System of Self-Driven Particles”</a>, <em>Physical Review Letters</em> 75, 1226–1229. Grégoire, G. and Chaté, H. (2004), <a href="https://doi.org/10.1103/PhysRevLett.92.025702">“Onset of Collective and Cohesive Motion”</a>, <em>Physical Review Letters</em> 92, 025702.</p>
""", "vicsek-transition-debate"))

    nbf.write(nb, WEEK05)


if __name__ == "__main__":
    rebuild_week04()
    refresh_week05()
    print("Refreshed Week 4 and Week 5 lecture slide paths.")
