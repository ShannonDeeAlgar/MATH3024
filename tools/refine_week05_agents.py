#!/usr/bin/env python3
"""Refine Week 5 definitions, Vicsek motivation, noise, and analysis slides."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week05/L_ABM.ipynb"


def md(source: str, slide_type: str = "", tags=None):
    cell = nbformat.v4.new_markdown_cell(source.strip() + "\n")
    if slide_type:
        cell.metadata["slideshow"] = {"slide_type": slide_type}
    if tags:
        cell.metadata["tags"] = tags
    return cell


def find(text: str) -> int:
    return next(i for i, cell in enumerate(nb.cells) if text in cell.source)


nb = nbformat.read(NOTEBOOK, as_version=4)

# A single linear argument is clearer here than two competing panels.
nb.cells[find("# We have already used agents")] = md(
    r"""
# We have already used agents

- Schelling's model represented people individually. Each agent read a local neighbourhood and followed an update rule.
- Agent-based models retain identities, locations, attributes and interaction partners that a continuous field would average away.
- An agent has **agency in the modelling sense**: its next action depends on its own state and locally available information.

That agency need not mean conscious choice. An active particle is continually self-propelled—the model treats its energy supply as available—whereas a person, animal or robot may follow hierarchical rules, goals and decisions.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What information becomes unavailable when individuals are replaced by a population average?</span></div>
""",
    "slide",
    ["slides"],
)

# Earlier explanations expose what local-interaction models replaced. Keep
# this Reader-only and historically qualified: these were proposed accounts,
# not a settled scientific consensus.
history_marker = "### Before local-interaction models"
if not any(history_marker in c.source for c in nb.cells):
    insert_at = find("## When is a group a flock?") + 1
    nb.cells.insert(
        insert_at,
        md(
            r"""
### Before local-interaction models

The coordination of a large flock once seemed to require communication across the whole group. Several explanations were considered:

- **Leader or command:** the most immediate analogy was command-and-control—a leading bird signals and the others obey. Edmund Selous described this as the apparently simplest explanation, but his observations of near-simultaneous turns made a single commander increasingly difficult to identify.
- **Thought transference:** Selous eventually proposed that some form of thought transfer might coordinate a flock. His 1931 book *Thought-Transference (or What?) in Birds* documents careful observations, but its proposed mechanism has not survived.
- **A threshold signal:** Davis (1980) proposed that preliminary movements by enough birds could announce an imminent turn.
- **A propagating manoeuvre:** film analysis by Potts (1984) showed that one bird can initiate a turn that travels through the flock as a wave. Each bird responds locally as the wave reaches it—more like a stadium wave than a military order.

The important change was from asking how every bird receives one global instruction to asking how information propagates through local interactions. Modern models test whether those local rules are sufficient; observations are still needed to determine which rules real birds use.

<p class="media-credit">Sources: Selous (1931), <em>Thought-Transference (or What?) in Birds</em>; Potts (1984), <a href="https://doi.org/10.1038/309344a0">“The chorus-line hypothesis of manoeuvre coordination in avian flocks”</a>, <em>Nature</em> 309, 344–345.</p>
""",
            tags=["reader-only"],
        ),
    )
else:
    # Keep this historical enrichment in the Reader rather than the lecture
    # deck, whose role here is to introduce the assessable modelling argument.
    history_i = find(history_marker)
    nb.cells[history_i].metadata.pop("slideshow", None)
    nb.cells[history_i].metadata["tags"] = ["reader-only"]

# Place a usable definition beside the first examples of collective behaviour.
if not any("## What is self-organisation?" in c.source for c in nb.cells):
    insert_at = find("## When is a group a flock?")
    nb.cells.insert(
        insert_at,
        md(
            r"""
## What is self-organisation?

**Self-organisation:** a global spatial, temporal or functional pattern develops through interactions among lower-level components, without that global pattern being specified by a central controller or blueprint.

External driving and constraints may still be essential. The crowd has a field and a milestone; a flock has an environment; active matter consumes energy. “Self-organised” describes where the organisation comes from, not an isolated or energy-free system.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Which part of the Franklin crowd movement was externally triggered, and which part was organised locally?</span></div>

<p class="media-credit">Definition adapted from Camazine et al. (2001), <em>Self-Organization in Biological Systems</em>.</p>
""",
            "subslide",
        ),
    )

# Models from different disciplines retain different mechanisms and answer
# different questions; calling them interchangeable obscures that distinction.
for cell in nb.cells:
    if cell.cell_type != "markdown":
        continue
    cell.source = cell.source.replace(
        "All three are agent-based models, but they are not interchangeable explanations.",
        "All three are agent-based models, but they retain different mechanisms and answer different questions.",
    )
    cell.source = cell.source.replace(
        "These are not interchangeable demonstrations of one rule. They are prompts to identify the agents, retained state, interaction network, environment and system-level behaviour in each model.",
        "Each Explorable changes a different mechanism or setting. Use them to identify the agents, retained state, interaction network, environment and system-level behaviour.",
    )

# Date the three modelling traditions precisely and distinguish their aims,
# assumptions, and evidence rather than treating them as interchangeable
# flocking demonstrations.
comparison_i = next(
    i
    for i, cell in enumerate(nb.cells)
    if "# Three disciplines, three modelling questions" in cell.source
    or "# One phenomenon, three modelling purposes" in cell.source
)
nb.cells[comparison_i] = md(
    r"""
# One phenomenon, three modelling purposes

| Motivation | Representative model | What counts as success? |
|---|---|---|
| Computer graphics | Reynolds' boids (1987) | Local rules produce controllable, believable group motion. |
| Statistical physics | Vicsek et al. (1995) | A minimal model exposes collective order and its transition. |
| Behavioural biology | Couzin et al. (2002) | Assumptions connect to observations, mechanisms and biological function. |

The question determines what the model retains and how it should be analysed. This week uses Vicsek because it isolates alignment and noise most simply.
""",
    "slide",
    ["slides"],
)

for cell in nb.cells:
    if cell.cell_type != "markdown":
        continue
    if "Craig Reynolds introduced boids" in cell.source:
        cell.source = cell.source.replace(
            "Craig Reynolds introduced boids for behavioural animation in the 1980s:",
            "Craig Reynolds introduced boids for behavioural animation in 1987:",
        ).replace(
            "Vicsek and colleagues stripped collective motion back further",
            "Vicsek and colleagues (1995) stripped collective motion back further",
        ).replace(
            "Couzin and colleagues instead used zones",
            "Couzin and colleagues (2002) instead used zones",
        )

# Give the Reader a stronger account of how motivation propagates through
# assumptions, outputs, and analysis.
purpose_marker = "### Motivation changes the model"
if not any(purpose_marker in c.source for c in nb.cells):
    comparison_i = find("# One phenomenon, three modelling purposes")
    nb.cells.insert(
        comparison_i + 2,
        md(
            r"""
### Motivation changes the model

Reynolds was solving a computer-graphics problem. Animating every trajectory by hand was costly and brittle; success meant that a small set of local steering behaviours produced a flock an animator could direct around obstacles. Separation, alignment and cohesion were design choices for believable motion. The Batman and *Jurassic Park* examples belong to this question. Visual plausibility and controllability are therefore legitimate outputs, even though they do not establish how birds perceive one another.

Vicsek and colleagues were asking a statistical-physics question. They deliberately removed cohesion, collision avoidance, leaders and detailed biology, leaving constant-speed self-propulsion, local alignment and noise. The main output is not a realistic bird path but an order parameter and its behaviour as noise, density and system size change. The Ising and XY Explorables, followed by *Horde of the Flies*, belong to this route from microscopic interaction to collective phase.

Couzin and colleagues were asking a behavioural-biological question. Repulsion, alignment and attraction zones encode hypotheses about how animals respond at different separations. Predictions are judged against group shape, polarisation, milling, sorting, leadership and observations of real animals. Bird data, pedestrian decisions, traffic responses and the collective-motion Explorables fit this broader question, although people and vehicles require different perception and decision rules from birds.

The same visual pattern can therefore count as a successful animation, evidence of an ordered phase, or a biological observation requiring explanation. Those are different claims. A model should be assessed against the question that motivated it.
""",
            tags=["reader-only"],
        ),
    )

# Make the slide sequence advertise the modelling purpose of each family.
for cell in nb.cells:
    if cell.cell_type != "markdown":
        continue
    cell.source = cell.source.replace(
        "## Local rules changed what films could animate",
        "## Computer graphics · make motion believable",
    ).replace(
        "## Beyond birds: people and traffic",
        "## Behavioural and applied models · explain local decisions",
    ).replace(
        "### Explore collective motion in other settings",
        "### Behavioural and applied explorables",
    ).replace(
        "# From fixed spins to moving agents",
        "# Statistical physics · isolate collective order",
    )

# Use the established blockquote treatment on the slide, then reserve the
# fuller physics comparison for the Reader.
quote_i = find("## A moving spin model")
nb.cells[quote_i] = md(
    r"""
## A moving spin model

> “...I had designed the moving version of the Heisenberg model.”
>
> — Tamás Vicsek (2016)

Fixed orientations become self-propelled particles whose interaction partners change as they move.

<p class="media-credit">Vicsek, T. (2016), <a href="https://www.nature.com/articles/529016a">“Universality in non-equilibrium systems”</a>, <em>Nature</em> 529, 16–17.</p>
""",
    "subslide",
    ["slides"],
)

heisenberg_marker = "### What does the Heisenberg comparison mean?"
if not any(heisenberg_marker in c.source for c in nb.cells):
    nb.cells.insert(
        quote_i + 1,
        md(
            r"""
### What does the Heisenberg comparison mean?

The classical **Heisenberg model** places a three-component unit spin on every fixed lattice site. Neighbouring spins interact through their dot product, so ferromagnetic coupling favours alignment. The two-component **XY model** is the planar version: each fixed spin is described by an angle.

Vicsek borrowed the alignment idea but changed the physical problem. The headings are planar and therefore XY-like, the particles move through space, neighbours continually change, noise is imposed dynamically, and energy is continually supplied through self-propulsion. It is a driven, non-equilibrium active-matter model rather than an equilibrium magnetic model. Vicsek's phrase is the conceptual bridge, not a claim of mathematical identity.
""",
            tags=["reader-only"],
        ),
    )

# Explain circular averaging immediately after the update equation.
update_i = find("## 3. Apply one synchronous update")
angle_marker = "### Why average with complex exponentials?"
if not any(angle_marker in c.source for c in nb.cells):
    nb.cells.insert(
        update_i + 1,
        md(
            r"""
### Why average with complex exponentials?

Angles wrap around: the ordinary arithmetic mean of $1^\circ$ and $359^\circ$ is $180^\circ$, although both headings point almost due east. Map each heading to the unit vector

$$
e^{\mathrm i\theta_j}=\cos\theta_j+\mathrm i\sin\theta_j.
$$

Adding these vectors separately averages their horizontal and vertical components:

$$
\mathbf m_i(t)=\sum_{j\in\mathcal N_i(t)}e^{\mathrm i\theta_j(t)},
\qquad
\bar\theta_i(t)=\operatorname{Arg}\mathbf m_i(t).
$$

The argument gives the direction of the resultant vector; dividing by the number of neighbours would change its length but not its direction. If the vectors cancel exactly, $\mathbf m_i=0$ and there is no unique mean heading—an implementation must decide how to handle that rare case.
""",
            tags=["reader-only"],
        ),
    )

# Put equations and physical interpretations together rather than separating
# them into a vague comparison table.
noise_i = find("## Where is the noise added?")
nb.cells[noise_i] = md(
    r"""
## Where is the noise added?

<div class="two-panel equal-panels compact-panels">
<div class="text-panel">
<h3>Angular noise</h3>

$$
\theta_i'=\operatorname{Arg}\!\left(\sum_{j\in\mathcal N_i}e^{\mathrm i\theta_j}\right)+\xi_i.
$$

The agent first estimates the local mean, then makes a turning error. This suits uncertainty in executing a chosen heading.
</div>
<div class="text-panel">
<h3>Vectorial noise</h3>

$$
\theta_i'=\operatorname{Arg}\!\left(\sum_{j\in\mathcal N_i}e^{\mathrm i\theta_j}+\eta n_i e^{\mathrm i\chi_i}\right).
$$

Noise perturbs the local alignment signal before its direction is chosen. This suits noisy sensing or a fluctuating local force.
</div>
</div>

Both are defensible models. They represent different locations for uncertainty in the mechanism and can produce different collective transitions.
""",
    "subslide",
    ["slides"],
)

# Restore the scientific transition debate to the main Reader argument.  The
# issue is not trivia: it demonstrates that noise, finite size, geometry, and
# sampling are part of the model and can change the inferred phase behaviour.
debate_text = r"""
### Why did the order of the transition become a debate?

Vicsek et al. (1995) reported a continuous transition: as noise increased, the polarisation appeared to fall smoothly to zero, with behaviour reminiscent of a continuous critical point. That claim mattered because a continuous transition suggests critical scaling, a universality class and no coexistence jump between ordered and disordered phases.

Grégoire and Chaté (2004), followed by larger simulations by Chaté et al. (2008), reported discontinuous, first-order-like behaviour. Near the transition, ordered high-density travelling bands can coexist with a disordered low-density background. In systems too small to accommodate the bands, or runs too short to sample their appearance, the change can look deceptively smooth.

The location of the noise also matters. With angular noise, each agent first computes a local mean direction and then makes a turning error. With vectorial noise, a random vector perturbs the alignment signal before its direction is taken. These are different microscopic models, not two interchangeable ways of coding one equation. Vectorial noise made discontinuity easier to see; the angular-noise case required much larger length and time scales before banding and discontinuity became clear.

Why care? Continuous and discontinuous transitions imply different finite-size scaling, fluctuations, coexistence, hysteresis and responses to perturbation. The debate became a useful warning: a smooth curve from one convenient simulation size is not by itself evidence of a continuous transition. Noise convention, density, speed, boundaries, initialisation, run length and system size belong in the claim.

<p class="media-credit">Vicsek et al. (1995); Grégoire and Chaté (2004); Chaté et al. (2008).</p>
"""

debate_i = next(
    (i for i, c in enumerate(nb.cells) if "The distinction became central to a long debate" in c.source or "### Why did the order of the transition become a debate?" in c.source),
    None,
)
if debate_i is not None:
    nb.cells[debate_i] = md(debate_text, tags=["reader-only"])

transition_slide_marker = "## Why did the transition debate matter?"
if not any(transition_slide_marker in c.source for c in nb.cells):
    insert_at = find("## Then repeat each condition") + 1
    nb.cells.insert(
        insert_at,
        md(
            r"""
## Why did the transition debate matter?

<div class="two-panel equal-panels compact-panels">
<div class="text-panel">
<h3>Continuous?</h3>
<p>Vicsek et al. (1995) observed polarisation falling smoothly with noise and reported critical scaling.</p>
<p>This suggests no jump or phase coexistence.</p>
</div>
<div class="text-panel">
<h3>Discontinuous?</h3>
<p>Larger studies found ordered travelling bands coexisting with a disordered background.</p>
<p>Finite systems can hide the jump and make the curve appear smooth.</p>
</div>
</div>

The order changes what scaling, fluctuations, coexistence and hysteresis we expect near onset.
""",
            "subslide",
            ["slides"],
        ),
    )

implementation_slide_marker = "## What changed the answer?"
if not any(implementation_slide_marker in c.source for c in nb.cells):
    insert_at = find(transition_slide_marker) + 1
    nb.cells.insert(
        insert_at,
        md(
            r"""
## What changed the answer?

1. Noise before or after taking the mean direction represents different uncertainty.
2. Density bands require enough space and time to form and travel.
3. Boundaries, initialisation and sampling affect what the finite simulation reveals.

The debate was not merely about numerical precision. It was about which model had been implemented and whether a finite simulation justified the asymptotic claim.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What evidence would distinguish a steep continuous transition from a small discontinuous jump?</span></div>
""",
            "subslide",
            ["slides"],
        ),
    )

variants_marker = "## The Vicsek model became a family"
if not any(variants_marker in c.source for c in nb.cells):
    insert_at = find(implementation_slide_marker) + 1
    nb.cells.insert(
        insert_at,
        md(
            r"""
## The Vicsek model became a family

| Change | Question exposed |
|---|---|
| Metric → topological neighbours | Do animals respond within a distance or to a fixed number of neighbours? |
| Add attraction and repulsion | When does an open group remain cohesive and avoid collisions? |
| Add informed or heterogeneous agents | How do leadership and individual differences affect collective decisions? |
| Add delay, inertia, obstacles or variable speed | Which physical and sensory constraints change the collective state? |

The minimal model is a baseline. Each extension should be motivated by a mechanism or observation, not by a desire for visual complexity.
""",
            "subslide",
            ["slides"],
        ),
    )

variants_reader_marker = "### What happened after the minimal model?"
if not any(variants_reader_marker in c.source for c in nb.cells):
    insert_at = find(variants_marker) + 1
    nb.cells.insert(
        insert_at,
        md(
            r"""
### What happened after the minimal model?

The Vicsek model became a reference point rather than a final model of flocking. Later work changed one assumption at a time:

- topological neighbours replaced a fixed metric radius after STARFLAG found that starlings responded to roughly six or seven nearest neighbours across flocks of different density;
- attraction and short-range repulsion produced cohesive groups in open space and represented collision avoidance;
- informed individuals, leaders and heterogeneous preferences tested collective decision-making and sorting;
- delays, inertia, variable speed and limited fields of view represented physical and sensory constraints;
- obstacles, predators and external fields tested response rather than spontaneous order alone;
- three-dimensional, species-specific and data-calibrated models asked whether rules inferred from a plane or a toy system survived contact with observations.

STARFLAG also shifted the analysis. Three-dimensional reconstructions made it possible to measure interaction range, anisotropy and correlations rather than judging only whether a simulated flock looked plausible. Ballerini et al. (2008) found evidence for topological interaction, while Cavagna et al. (2010) found that the correlation length of velocity fluctuations grew with flock size. These observations constrain biological models in ways that the minimal Vicsek model was never intended to do.
""",
            tags=["reader-only"],
        ),
    )

# Make the sampling logic explicit: a sweep of single runs is not yet a
# reliable parameter comparison.
ensemble_i = find("## Then repeat each condition")
nb.cells[ensemble_i] = md(
    r"""
## Then repeat each condition

1. **One run at fixed $\eta$:** one possible stochastic history.
2. **An ensemble at fixed $\eta$:** a distribution of outcomes, summarised by a mean and variation.
3. **A parameter sweep of ensembles:** a comparison across $\eta$ that separates systematic change from run-to-run randomness.

A sweep containing only one run per noise value can mistake stochastic variation for a parameter effect.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over random histories:</strong> replace individual trajectories by an estimated response and its uncertainty at each parameter value.</span></div>
""",
    "subslide",
    ["slides"],
)

# Bold type is reserved for terms at their first definition. Remove later
# emphasis and use ordinary prose or italics for titles and structural labels.
for cell in nb.cells:
    if cell.cell_type != "markdown":
        continue
    replacements = {
        "<strong>flock</strong>": "flock",
        "<strong>murmuration</strong>": "murmuration",
        "<strong>parliament</strong>": "parliament",
        "<strong>chatter</strong>": "chatter",
        "<strong>locally ordered collective motion</strong>": "locally ordered collective motion",
        "<strong>Batman Returns (1992):</strong>": "<em>Batman Returns</em> (1992):",
        "<strong>Jurassic Park (1993):</strong>": "<em>Jurassic Park</em> (1993):",
        "<p><strong>Retain:</strong>": "<p>Retain:",
        "<p><strong>Remove:</strong>": "<p>Remove:",
        "<span><strong>Up the ladder over agents:</strong>": "<span>Up the ladder over agents:",
        "<span><strong>Up the ladder again:</strong>": "<span>Up the ladder again:",
        "<span><strong>Up the ladder over random histories:</strong>": "<span>Up the ladder over random histories:",
        "1. **One run at fixed $\\eta$:**": "1. One run at fixed $\\eta$:",
        "2. **An ensemble at fixed $\\eta$:**": "2. An ensemble at fixed $\\eta$:",
        "3. **A parameter sweep of ensembles:**": "3. A parameter sweep of ensembles:",
        "The two-component **XY model**": "The two-component XY model",
        "- **Leader or command:**": "- Leader or command:",
        "- **Thought transference:**": "- Thought transference:",
        "- **A threshold signal:**": "- A threshold signal:",
        "- **A propagating manoeuvre:**": "- A propagating manoeuvre:",
    }
    for old, new in replacements.items():
        cell.source = cell.source.replace(old, new)

# Phi is mathematical notation, not an emphatic prose label.
phi_i = find("## Quantify collective alignment")
nb.cells[phi_i].source = nb.cells[phi_i].source.replace(
    '<div class="two-panel equal-panels compact-panels">\n<div class="text-panel"><p><strong>Φ ≈ 0:</strong> headings cancel.</p></div>\n<div class="text-panel"><p><strong>Φ ≈ 1:</strong> agents move in nearly the same direction.</p></div>\n</div>',
    '<div class="two-panel equal-panels compact-panels">\n<div class="text-panel"><p>$\\Phi\\approx0$: headings cancel.</p></div>\n<div class="text-panel"><p>$\\Phi\\approx1$: agents move in nearly the same direction.</p></div>\n</div>',
)

# End with a proper scholarly reference list. Media credits remain beside the
# relevant figures; this list records the work on which the week's argument is
# based.
references_source = r"""
# References

- Reynolds, C. W. (1987), [“Flocks, herds and schools: A distributed behavioral model”](https://red3d.com/cwr/papers/1987/boids.html), *Computer Graphics* 21(4), 25–34.
- Vicsek, T., Czirók, A., Ben-Jacob, E., Cohen, I. and Shochet, O. (1995), [“Novel type of phase transition in a system of self-driven particles”](https://doi.org/10.1103/PhysRevLett.75.1226), *Physical Review Letters* 75, 1226–1229.
- Grégoire, G. and Chaté, H. (2004), [“Onset of collective and cohesive motion”](https://doi.org/10.1103/PhysRevLett.92.025702), *Physical Review Letters* 92, 025702.
- Chaté, H., Ginelli, F., Grégoire, G. and Raynaud, F. (2008), [“Collective motion of self-propelled particles interacting without cohesion”](https://doi.org/10.1103/PhysRevE.77.046113), *Physical Review E* 77, 046113.
- Couzin, I. D., Krause, J., James, R., Ruxton, G. D. and Franks, N. R. (2002), [“Collective memory and spatial sorting in animal groups”](https://doi.org/10.1006/jtbi.2002.3065), *Journal of Theoretical Biology* 218, 1–11.
- Ballerini, M. et al. (2008), [“Interaction ruling animal collective behavior depends on topological rather than metric distance”](https://doi.org/10.1073/pnas.0711437105), *Proceedings of the National Academy of Sciences* 105, 1232–1237.
- Ballerini, M. et al. (2008), [“Empirical investigation of starling flocks: a benchmark study in collective animal behaviour”](https://doi.org/10.1016/j.anbehav.2008.02.004), *Animal Behaviour* 76, 201–215.
- Cavagna, A. et al. (2010), [“Scale-free correlations in starling flocks”](https://doi.org/10.1073/pnas.1005766107), *Proceedings of the National Academy of Sciences* 107, 11865–11870.
- Potts, W. K. (1984), [“The chorus-line hypothesis of manoeuvre coordination in avian flocks”](https://doi.org/10.1038/309344a0), *Nature* 309, 344–345.
"""
reference_cells = [
    i for i, cell in enumerate(nb.cells)
    if cell.cell_type == "markdown" and cell.source.strip().startswith("# References")
]
reference_cell = md(references_source, tags=["reader-only"])
if reference_cells:
    nb.cells[reference_cells[0]] = reference_cell
    for i in reversed(reference_cells[1:]):
        del nb.cells[i]
else:
    nb.cells.append(reference_cell)

nbformat.write(nb, NOTEBOOK)
