#!/usr/bin/env python3
"""Apply the agreed Week 6--10 lecture-slide audit.

The Reader remains the narrative source.  Reader-only cells are retained in
the notebooks and excluded only from slide export.  Fixed cell ids make this
safe to rerun while the lecture notebooks continue to evolve.
"""

from __future__ import annotations

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]


def tags(cell):
    return list(cell.metadata.get("tags", []))


def add_tag(cell, tag):
    current = tags(cell)
    if tag not in current:
        current.append(tag)
    cell.metadata["tags"] = current


def remove_tag(cell, tag):
    cell.metadata["tags"] = [item for item in tags(cell) if item != tag]


def set_slide_type(cell, slide_type):
    cell.metadata["slideshow"] = {"slide_type": slide_type}


def slide_cell(cell_id, source, slide_type="subslide"):
    cell = nbformat.v4.new_markdown_cell(source=source, id=cell_id)
    cell.metadata["tags"] = ["slides-only"]
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


def by_id(nb):
    return {cell.get("id"): cell for cell in nb.cells}


def upsert_after(nb, anchor_id, cell):
    ids = by_id(nb)
    existing = ids.get(cell.id)
    if existing is not None:
        nb.cells.remove(existing)
    anchor = by_id(nb).get(anchor_id)
    if anchor is None:
        raise KeyError(f"Missing anchor {anchor_id}")
    nb.cells.insert(nb.cells.index(anchor) + 1, cell)


def move_after(nb, cell_id, anchor_id):
    ids = by_id(nb)
    cell = ids.get(cell_id)
    anchor = ids.get(anchor_id)
    if cell is None or anchor is None:
        raise KeyError(f"Cannot move {cell_id} after {anchor_id}")
    nb.cells.remove(cell)
    anchor = by_id(nb)[anchor_id]
    nb.cells.insert(nb.cells.index(anchor) + 1, cell)


def hide_from_slides(nb, *cell_ids):
    ids = by_id(nb)
    for cell_id in cell_ids:
        cell = ids.get(cell_id)
        if cell is not None:
            add_tag(cell, "reader-only")
            remove_tag(cell, "slides-only")


def save(path, nb):
    nbformat.write(nb, path)
    print(f"updated {path.relative_to(ROOT)}")


def week06():
    path = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
    nb = nbformat.read(path, as_version=4)
    ids = by_id(nb)

    # Let the phase-oscillator definition flow directly from Model details.
    one = ids.get("w6-one")
    banner = ids.get("w6-model-details-slide")
    if one is not None and banner is not None:
        body = one.source
        if body.lstrip().startswith("## A phase oscillator"):
            body = body.replace("## A phase oscillator", "", 1).lstrip()
        marker = "<!-- phase-oscillator-definition -->"
        if marker not in banner.source:
            banner.source = banner.source.rstrip() + f"\n\n{marker}\n\n" + body
        add_tag(one, "archive-only")

    # Complete the population model before opening Analysis.
    anchor = "w6-coupling"
    for cell_id in [
        "sync-types-slide",
        "sync-types-collective-slide",
        "w6-specify",
        "w6-kuramoto",
        "w6-assumptions",
        "w6-natural-frequency-before-analysis-slide",
        "w6-discrete-evolution-slide",
    ]:
        move_after(nb, cell_id, anchor)
        anchor = cell_id
    move_after(nb, "w6-relative", anchor)

    if "w6-sweep" in ids:
        ids["w6-sweep"].source = ids["w6-sweep"].source.replace(
            "Sweep coupling and population size",
            "Sweep coupling and population size separately",
        )

    # The full continuum derivation is retained as optional Reader material.
    hide_from_slides(
        nb,
        "w6-dynamic-to-stationary-slide",
        "w6-onset-result-slide",
        "w6-ensemble",
        "w6-coupling-heterogeneity-slide",
        "w6-second-order-kuramoto-slide",
        "w6-drone-shows-slide",
    )

    network = by_id(nb).get("w6-network-variant-slide")
    if network is not None:
        network.source = """## Networks can change too

**Dynamics on a network:** oscillator phases change while the edges stay fixed.  Kuramoto oscillators on a prescribed graph are the example here.

**Dynamics of a network:** the network itself changes, as in a growing preferential-attachment network.

**Adaptive network:** states and edges change together.  Behaviour can alter epidemic contacts while infection risk alters behaviour.

These are different model classes.  Replacing all-to-all coupling by a fixed graph is the first, simplest extension."""

    save(path, nb)


def week07():
    path = ROOT / "notebooks/week07/L_Intelligent_systems.ipynb"
    nb = nbformat.read(path, as_version=4)

    move_after(nb, "w7-synthesis-after-sweep", "w7-aco-update")
    closer = slide_cell(
        "w7-toolkit-close-slide",
        """## What Week 7 adds to the toolkit

- **ACO:** agents leave environmental memory on a network.
- **PSO:** agents retain personal memory and use time-delayed shared information.
- **Collective intelligence:** distributed agents produce useful computation without a central controller.

The design question is not whether a system looks intelligent. It is where information is stored, how it moves, and what task the collective process solves.""",
    )
    upsert_after(nb, "w7-synthesis", closer)
    save(path, nb)


def week08():
    path = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"
    nb = nbformat.read(path, as_version=4)

    hide_from_slides(
        nb,
        "29f6e3a1",
        "1688c8df",
        "bba65e0b-cdd4-4d39-bca2-c72a8fbce982",
        "40949b83-6a08-4aeb-814d-25c07e0aac0d",
    )

    analysis_id = "c13d03d6-f14c-49e0-abaa-603e87235d25"
    analysis = by_id(nb).get(analysis_id)
    if analysis is not None:
        analysis.source = "# Analysis"
        set_slide_type(analysis, "slide")

    explorable = by_id(nb).get("w8-abelian-sandpile-explorable")
    if explorable is not None:
        body = explorable.source
        body = body.replace("### Explore the Abelian sandpile", "# Explorable", 1)
        explorable.source = body
        set_slide_type(explorable, "slide")

    qualitative = slide_cell(
        "w8-qualitative-analysis-slide",
        """## Qualitative analysis

![An avalanche propagating through the course Abelian sandpile simulation](images/sandpile_avalanche.gif){width=72%}

One added grain can produce no topplings, a small local rearrangement, or an avalanche spanning much of the lattice.  We first inspect that variation before compressing it into event statistics.""",
    )
    upsert_after(nb, analysis_id, qualitative)

    for cell_id, title in [
        ("1bc8a371-5d9f-4701-9530-6c588265ddb1", "## Random overfull initial condition"),
        ("4e00ef41-61b4-4cb0-8ae3-4f8c96782794", "## Uniform overfull initial condition"),
        ("5afe6b3c-eddf-4e0e-b53f-ca066fc623ea", "## One added grain"),
    ]:
        cell = by_id(nb).get(cell_id)
        if cell is not None and not cell.source.lstrip().startswith("#"):
            cell.source = title + "\n\n" + cell.source
        if cell is not None:
            # Each initialisation is a distinct comparison slide.  Without an
            # explicit boundary Reveal groups all three beneath the qualitative
            # animation, producing a single scrolling slide.
            set_slide_type(cell, "subslide")

    # Preserve the detailed Reader definition while presenting a spare slide.
    detailed = by_id(nb).get("3cdcf36d-eddc-4976-973b-e53a589762af")
    if detailed is not None:
        add_tag(detailed, "reader-only")
        remove_tag(detailed, "slides-only")
    event_defs = slide_cell(
        "w8-avalanche-definitions-slide",
        """## Describe each avalanche

- **Size $S$:** total number of toppling events.
- **Area $A$:** number of distinct sites that topple.
- **Duration $T$:** number of parallel relaxation steps before stability returns.

These summaries discard different parts of the same event.  A scaling claim must say which quantity was measured.""",
    )
    upsert_after(nb, "ff17bec4-36da-4b5c-9a64-3f11b2ffab2f", event_defs)

    fingerprints = by_id(nb).get("965627a4-2957-4331-a9a9-91bb3653fa05")
    if fingerprints is not None:
        fingerprints.source = """## Three views of the same dynamics

- **Space:** which sites participated, and with what final heights?
- **Time:** when did topplings occur and how long did relaxation last?
- **Events:** how are avalanche sizes, areas and durations distributed?

No single plot establishes critical behaviour.  The views provide different evidence from the same simulation."""

    save(path, nb)


def week09():
    path = ROOT / "notebooks/week09/L_InformationTheory.ipynb"
    nb = nbformat.read(path, as_version=4)

    measures = slide_cell(
        "w9-measures-so-far-slide",
        """## Measures used so far

- **Fractal dimension:** how spatial detail changes with scale.
- **Order parameters:** how microscopic states combine into collective organisation.
- **Avalanche distributions:** how event sizes and durations vary.
- **Ensemble summaries:** how outcomes vary across repeated runs.

Information measures add a new question: how much uncertainty or dependence remains after deciding what the symbols represent?""",
    )
    upsert_after(nb, "w9-motivation-banner", measures)

    hide_from_slides(nb, "w9-research-examples")
    coordination = slide_cell(
        "w9-research-coordination-slide",
        r"""## Information measures in research · coordination

$$
I(X;Y)=\sum_{x,y}p(x,y)\log_2\!\frac{p(x,y)}{p(x)p(y)}
$$

**Mutual information** measures shared variation.  **Transfer entropy** asks whether the past of one process improves prediction of another beyond that process's own past.

Leader--follower studies use these measures to compare directional predictive information between moving animals.  Predictive direction is not, by itself, proof of causation.""",
    )
    dynamics = slide_cell(
        "w9-research-dynamics-slide",
        r"""## Information measures in research · dynamics

**Permutation entropy** replaces numerical values by their ordinal patterns:

$$
H_{\mathrm{perm}}=-\sum_{\pi}p(\pi)\log_2 p(\pi).
$$

It measures temporal structure without requiring a detailed dynamical model.  Entropy rate instead asks how much new uncertainty arrives per observation.

These are optional project methods.  Their estimates depend on sampling, time lag and the amount of data available.""",
    )
    upsert_after(nb, "w9-analysis-banner", coordination)
    upsert_after(nb, coordination.id, dynamics)
    save(path, nb)


def week10():
    path = ROOT / "notebooks/week10/L_Game_theory.ipynb"
    nb = nbformat.read(path, as_version=4)

    # Reader explanations remain complete; the lecture deck uses a smaller
    # selection so that each slide carries one claim rather than a paragraph.
    compact_replacements = [
        (
            "w10-real-games",
            "w10-real-games-slide",
            """## Games outside the classroom

- Side-blotched lizards: three mating strategies form a rock--paper--scissors cycle.
- Yeast: cooperation and cheating can produce snowdrift-game dynamics.
- Shared resources: individual incentives can conflict with collective persistence.

The payoff rule specifies incentives.  Population structure and repeated interaction determine what follows.""",
        ),
        (
            "cf863523",
            "w10-read-payoff-slide",
            """## Read one payoff entry

Player 1 chooses a row and Player 2 a column.  The selected cell contains

$$
(\text{Player 1 payoff},\;\text{Player 2 payoff}).
$$

In the Prisoner's Dilemma, $(D,C)$ gives the defector the tempting payoff while the cooperator receives the sucker's payoff.  The whole game is read one cell at a time.""",
        ),
        (
            "w10-evolution-bridge",
            "w10-evolution-bridge-slide",
            """# From games to evolution

The Prisoner's Dilemma remains the canonical game.  We add:

1. repeated encounters;
2. strategies that use the history of play;
3. accumulated payoff across a population; and
4. a rule connecting payoff to representation in the next generation.

Tournament success and evolutionary success are different claims.""",
        ),
        (
            "w10-payoff-to-fitness",
            "w10-repeated-play-slide",
            """## Repeated play

A strategy is now a rule that maps interaction history to the next action.

- **Always Cooperate** and **Always Defect** ignore history.
- **Tit for Tat** cooperates first, then copies its opponent's previous action.

An immediate gain can therefore change many later rounds.""",
        ),
        (
            "week10-pathway",
            "w10-axelrod-slide",
            """## Axelrod's tournaments

Submitted strategies played repeated matches against a fixed field of opponents.

Tit for Tat won despite being extremely short and never outscoring an opponent head-to-head.  It accumulated a strong total across the field.

This is a tournament result, not yet an evolutionary result.""",
        ),
        (
            "w10-evolutionary-ipd",
            "w10-tournament-evolution-slide",
            """## Tournament success and evolutionary success

**Tournament:** which strategy scores best against a fixed collection?

**Evolution:** which strategy becomes more common as the population changes?

Evolution requires an explicit payoff-to-fitness rule, inheritance and mutation.  A high payoff does not cause copying or reproduction unless the model says how.""",
        ),
    ]
    for original_id, replacement_id, source in compact_replacements:
        original = by_id(nb).get(original_id)
        if original is not None:
            add_tag(original, "reader-only")
            remove_tag(original, "slides-only")
            upsert_after(nb, original_id, slide_cell(replacement_id, source))

    rps = by_id(nb).get("w10-rps-local-game-slide")
    if rps is not None:
        rps.source = """## Rock--paper--scissors is a game

One encounter has a payoff matrix: a win gives $+1$, a loss $-1$, and a draw $0$.

| Player 1 \\ Player 2 | Rock | Paper | Scissors |
|---|---:|---:|---:|
| Rock | $(0,0)$ | $(-1,+1)$ | $(+1,-1)$ |
| Paper | $(+1,-1)$ | $(0,0)$ | $(-1,+1)$ |
| Scissors | $(-1,+1)$ | $(+1,-1)$ | $(0,0)$ |

The moving population adds local encounters, conversion, finite numbers and boundaries.  Those details determine which pairwise games are actually played."""
    hide_from_slides(nb, "w10-rps-population-slide", "w10-rps-population")

    # Keep one compact statement of the generic framework.
    hide_from_slides(
        nb,
        "a7aa8aa3",
        "802fd871-454e-4fff-986f-608025913ed8",
        "9578e5bd-40d6-435f-83b2-a65f77bb3e37",
        "8ff83c61-0097-43d3-ac1a-e5f5fef2995b",
    )
    nash = by_id(nb).get("894680c8-6d78-4117-b994-6b42b5c64ffe")
    if nash is not None:
        nash.source = nash.source.replace("**Nash equilibrium.**", "## Nash equilibrium")

    explorable_banner = slide_cell("w10-explorable-banner-slide", "# Explorable", "slide")
    explorable = slide_cell(
        "w10-prisoners-kaleidoscope-slide",
        """## Prisoner's Kaleidoscope

<iframe class="full-bleed-frame" src="https://www.complexity-explorables.org/explorables/prisoners-kaleidoscope/" title="Prisoner's Kaleidoscope explorable"></iframe>""",
    )
    hide_from_slides(nb, "a7e5e594")
    upsert_after(nb, "f95edecc", explorable_banner)
    upsert_after(nb, explorable_banner.id, explorable)

    fitness = slide_cell(
        "w10-payoff-fitness-link-slide",
        """### From payoff to fitness

An evolutionary model needs an explicit link from game payoff to expected copying or reproductive success.

- **Selection:** how payoff changes the expected number of descendants or copies.
- **Inheritance:** whether descendants receive the parent's strategy.
- **Mutation:** how copied strategies change or new strategies appear.

A high payoff does not cause reproduction unless the model supplies this rule.""",
    )
    inheritance = slide_cell(
        "w10-selection-inheritance-mutation-slide",
        """### Selection changes the population

1. Agents play the Prisoner's Dilemma and accumulate payoff.
2. Strategies with greater fitness are copied more often.
3. Copies inherit a strategy, with occasional mutation.
4. The new population changes the opponents encountered next.

Tournament success tests a fixed field of opponents.  Evolutionary success changes that field.""",
    )
    upsert_after(nb, "w10-tournament-evolution-slide", fitness)
    upsert_after(nb, fitness.id, inheritance)

    save(path, nb)


def main():
    for fn in [week06, week07, week08, week09, week10]:
        fn()


if __name__ == "__main__":
    main()
