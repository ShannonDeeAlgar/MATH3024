"""Finish the Week 6 analysis and standardise canonical-model summaries."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def md(cell_id: str, source: str, tags: list[str], slide_type: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": tags, "slideshow": {"slide_type": slide_type}},
        "source": source.splitlines(keepends=True),
    }


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def save(path: Path, notebook: dict) -> None:
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Week 6: move from the observable to an actual analysis of onset.
# ---------------------------------------------------------------------------
path = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
nb = load(path)
cells = nb["cells"]

if not any(c.get("id") == "w6-heterogeneity-analysis-slide" for c in cells):
    i = next(i for i, c in enumerate(cells) if c.get("id") == "w6-ensemble")
    cells[i:i] = [
        md(
            "w6-heterogeneity-analysis-slide",
            """## Heterogeneity sets the synchronisation challenge

The natural frequencies are sampled from a distribution $g(\\omega)$.

| Narrow $g(\\omega)$ | Wide $g(\\omega)$ |
|---|---|
| oscillators have similar preferred rates | preferred rates differ strongly |
| weaker coupling can recruit a coherent group | stronger coupling is required |

For a symmetric unimodal distribution in the large-population limit,

$$
K_c=\\frac{2}{\\pi g(\\bar\\omega)}.
$$

The threshold depends on the population being coupled, not on $K$ alone.
""",
            ["slides-only"],
            "subslide",
        ),
        md(
            "w6-finite-large-n-slide",
            """## Finite $N$ and the large-population limit

**Finite simulation:** below onset, random phase imbalance leaves $r$ small but not exactly zero. The apparent transition is noisy and rounded.

**Large-$N$ limit:** replace one sampled population by a frequency density $g(\\omega)$. A sharp onset and analytic threshold can then be derived.

Large $N$ is central to the classical analysis. Finite $N$ is central when interpreting an actual simulation or finite system.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>When estimating the onset numerically, what should be repeated besides the initial phases?</span></div>
""",
            ["slides-only"],
            "subslide",
        ),
    ]

if not any(c.get("id") == "w6-onset-analysis-reader" for c in cells):
    i = next(i for i, c in enumerate(cells) if c.get("id") == "ensemble")
    cells.insert(
        i,
        md(
            "w6-onset-analysis-reader",
            """## What controls the onset of collective synchronisation?

The order parameter makes a coupling sweep measurable, but the curve is not determined by $K$ alone. The natural frequencies are sampled from a distribution $g(\\omega)$. A narrow distribution gives oscillators similar preferred rates, so relatively weak coupling can recruit them. A broad distribution creates a stronger competing tendency and generally requires larger coupling.

For a symmetric, unimodal frequency distribution in the classical all-to-all model, the large-population calculation gives

$$
K_c=\\frac{2}{\\pi g(\\bar\\omega)},
$$

where $\\bar\\omega$ is the centre of the distribution. For a Lorentzian distribution with half-width $\\Delta$, this reduces to $K_c=2\\Delta$. This is the cleanest expression of the week’s modelling focus: heterogeneity changes the collective threshold.

### Why do treatments distinguish finite and large $N$?

For finite $N$, the sampled frequencies and initial phases vary between runs. Even below the onset of collective locking, random phase imbalance usually leaves $r$ small but non-zero, with fluctuations of typical scale $N^{-1/2}$. The observed transition is therefore rounded and its estimated location varies between finite samples.

The limit $N\\to\\infty$ replaces one finite list of frequencies by the density $g(\\omega)$. That continuum description permits a self-consistency analysis and produces a sharp critical coupling. It is paramount to the classical analytic result, but it does not make finite systems unimportant: simulations and empirical populations still require finite-size and ensemble checks.

The essential undergraduate analysis is therefore:

1. choose and report $g(\\omega)$;
2. simulate long enough to estimate the long-time order parameter;
3. sweep $K$;
4. repeat across initial phases and sampled frequency populations;
5. compare several $N$ before interpreting an apparent threshold.

This is sufficient here. Deriving the self-consistency equation or studying finite-size scaling formally is useful extension material, not assumed assessable content.

*Further reading:* [Acebrón et al. (2005), “The Kuramoto model: a simple paradigm for synchronization phenomena”](https://doi.org/10.1103/RevModPhys.77.137) and [Dörfler and Bullo (2012), “On the critical coupling for Kuramoto oscillators”](https://doi.org/10.1137/10081530X).
""",
            ["reader-only"],
            "skip",
        ),
    )

save(path, nb)


# ---------------------------------------------------------------------------
# Canonical summaries: familiar fields, explicit model names, and a world.
# Fields that do not apply are said to be absent rather than silently omitted.
# ---------------------------------------------------------------------------
summaries = {
    "week01/L_Introduction_to_complex_systems.ipynb": """## Canonical models at a glance · Schelling segregation and planetary motion

### Schelling segregation

**World:** a finite grid with a stated neighbourhood and boundary rule.  
**State:** agent types and empty sites.  
**Initialisation:** assign vacancies and agent types, usually using a recorded random seed.  
**Dynamics:** agents below a local-similarity threshold relocate.  
**Interactions:** each agent responds to the composition of its local neighbourhood.  
**Parameters:** population mix, vacancy fraction, neighbourhood, threshold and update convention.  
**Outputs:** configurations, relocation history and segregation summaries.

### Planetary motion

**World:** continuous physical space; the chosen coordinate frame and time interval must be stated.  
**State:** position and velocity.  
**Initialisation:** an initial position and velocity.  
**Dynamics:** gravitational acceleration changes velocity, which changes position.  
**Interactions:** gravitational attraction to the specified masses.  
**Parameters:** masses, gravitational constant and numerical time step.  
**Outputs:** the trajectory through time.
""",
    "week02/L_Fractals.ipynb": """## Canonical models at a glance · Cantor set and Sierpiński triangle

### Cantor set

**World:** no simulation domain or boundary is required; the construction acts on an initial interval.  
**State:** the collection of intervals retained at depth $k$.  
**Initialisation:** one closed interval.  
**Dynamics:** replace every interval by its left and right thirds.  
**Interactions:** none; copies are generated independently by the same rule.  
**Parameters:** initiator, generator and construction depth.  
**Outputs:** a finite approximation to the limiting Cantor set.

### Sierpiński triangle

**World:** no simulation domain or boundary is required; the construction acts on an initial triangle.  
**State:** the collection of triangles retained at depth $k$.  
**Initialisation:** one filled triangle.  
**Dynamics:** replace every triangle by three half-scale corner copies.  
**Interactions:** none; copies are generated independently by the same rule.  
**Parameters:** initiator, generator and construction depth.  
**Outputs:** a finite approximation to the limiting Sierpiński triangle.
""",
    "week03/L_Reaction_diffusion.ipynb": """## Canonical model at a glance · Gray–Scott reaction–diffusion

**World:** a continuous spatial domain with specified geometry and boundary conditions.  
**State:** concentration fields $U(\\mathbf{x},t)$ and $V(\\mathbf{x},t)$.  
**Initialisation:** nearly uniform fields plus a stated perturbation.  
**Dynamics:** local Gray–Scott reactions act alongside diffusion of both fields.  
**Interactions:** diffusion couples neighbouring locations; reaction couples $U$ and $V$ locally.  
**Parameters:** $D_U$, $D_V$, feed $f$ and kill $k$.  
**Outputs:** evolving concentration fields and their spatial morphology.  
**Numerical choices:** grid spacing, time step and discrete Laplacian.
""",
    "week04/L_Cellular_automata.ipynb": """## Canonical models at a glance · elementary CA and Conway’s Game of Life

### Elementary cellular automata

**World:** a one-dimensional lattice with stated size and boundary condition.  
**State:** one binary value at each site.  
**Initialisation:** a specified row, often a single seed or reproducible random state.  
**Dynamics:** update all cells synchronously using one elementary rule table.  
**Interactions:** each next state depends on the left, centre and right cells.  
**Parameters:** rule number, world size and boundary condition.  
**Outputs:** configurations through time and a space–time diagram.

### Conway's Game of Life

**World:** a two-dimensional grid with stated size and boundary condition.  
**State:** dead or alive at every site.  
**Initialisation:** a specified finite motif or reproducible random configuration.  
**Dynamics:** apply the synchronous outer-totalistic rule B3/S23.  
**Interactions:** each cell responds to its eight-cell Moore neighbourhood.  
**Parameters:** world size and boundary condition; B3/S23 defines the canonical rule.  
**Outputs:** configurations through time and persistent, oscillating or moving structures.
""",
    "week05/L_ABM.ipynb": """## Canonical model at a glance · Vicsek model

**World:** a two-dimensional periodic domain of stated size.  
**State:** every agent's position $\\mathbf{x}_i$ and heading $\\theta_i$.  
**Initialisation:** random positions and headings generated from a recorded seed.  
**Dynamics:** align, apply a stated noise convention, then move at fixed speed.  
**Interactions:** metric neighbours within radius $R$ contribute to local alignment.  
**Parameters:** $N$, domain size, $R$, $v_0$, $\\eta$, time step and noise convention.  
**Outputs:** trajectories, spatial configurations and collective order $\\Phi$.  
**Stochastic element:** initial states and noise realisations.
""",
    "week06/L_Synchronisation.ipynb": """## Canonical model at a glance · Kuramoto model

**World:** no physical spatial domain or boundary is required; phases live on the circle and the canonical population is coupled all-to-all.  
**State:** oscillator phases $\\theta_i$.  
**Initialisation:** initial phases and intrinsic frequencies sampled from a stated distribution $g(\\omega)$.  
**Dynamics:** intrinsic rotation plus coupling to phase differences.  
**Interactions:** every oscillator couples sinusoidally to every other oscillator with strength $K/N$.  
**Parameters:** population size $N$, coupling $K$, frequency distribution and numerical time step.  
**Outputs:** phase trajectories, realised frequencies and the synchronisation order parameter $r$.  
**Heterogeneity:** the finite collection or distribution of intrinsic frequencies.
""",
    "week07/L_Intelligent_systems.ipynb": """## Canonical models at a glance · ACO and PSO

### Ant colony optimisation

**World:** a weighted graph with start and target nodes.  
**State:** each ant's partial route and pheromone stored on graph edges.  
**Dynamics:** successive local edge choices followed by evaporation and route-quality reinforcement.  
**Outputs:** the best complete route and its cost.

### Particle swarm optimisation

**World:** a bounded numerical solution space with an explicit boundary rule.  
**State:** each particle's position, velocity and personal best, plus the swarm's global best.  
**Dynamics:** retained motion, personal memory and globally shared information update velocity and position.  
**Outputs:** the best candidate and objective value found so far.
""",
    "week08/L_Critical_phenomena.ipynb": """## Canonical models at a glance · Ising, percolation and Abelian sandpile

### Ising model

**World:** a lattice with specified size, neighbourhood and boundary condition.  
**State:** one binary spin at each site.  
**Initialisation:** a stated ordered or random spin configuration.  
**Dynamics:** propose spin flips and accept them using energy change and temperature.  
**Interactions:** neighbouring spins contribute to local energy.  
**Parameters:** coupling, temperature and update rule.  
**Outputs:** configurations, magnetisation, energy and fluctuations.

### Site percolation

**World:** a lattice with specified size, neighbourhood and boundaries.  
**State:** occupied or empty sites.  
**Initialisation:** independent Bernoulli draws at occupation probability $p$.  
**Dynamics:** one configuration is generated, then connected clusters are identified.  
**Interactions:** adjacency defines cluster connectivity; sites are sampled independently.  
**Parameters:** $p$ and lattice choices.  
**Outputs:** clusters, spanning events and finite-size scaling summaries.

### Abelian sandpile

**World:** a lattice with a specified dissipative boundary.  
**State:** grain count at every site.  
**Initialisation:** a stated stable configuration.  
**Dynamics:** add a grain, then topple unstable sites until stability returns.  
**Interactions:** toppling distributes grains to neighbouring sites.  
**Parameters:** lattice, threshold and driving rule.  
**Outputs:** stable states and avalanche size, area and duration.
""",
    "week09/L_InformationTheory.ipynb": """## Canonical model at a glance · Shannon communication model

**World:** no spatial domain is required; the setting is a source, channel and receiver.  
**State:** a message and its encoded, transmitted, received and decoded representations.  
**Initialisation:** sample or supply a message under a stated source distribution.  
**Dynamics:** source encoding, channel encoding, noisy transmission and decoding.  
**Interactions:** the channel transforms transmitted symbols according to its noise model.  
**Parameters:** source distribution, code, channel model and noise level.  
**Outputs:** reconstructed messages, error rates and information summaries.  
**Estimator:** entropy compresses a distribution to its expected information content.
""",
    "week10/L_Game_theory.ipynb": """## Canonical model at a glance · iterated Prisoner’s Dilemma

**World:** a repeated-interaction setting defined by the payoff matrix, pairing protocol and number of rounds.  
**State:** both players' action histories and accumulated scores.  
**Initialisation:** choose strategies, empty histories and zero scores.  
**Dynamics:** each strategy selects an action, then payoffs update both scores.  
**Interactions:** paired players affect one another through their actions and remembered histories.  
**Parameters:** payoff matrix, strategies, rounds, pairing protocol and implementation noise.  
**Outputs:** histories, scores and tournament-level performance summaries.  
**Stopping condition:** the specified number of rounds or matches.
""",
}

for relative, replacement in summaries.items():
    target = ROOT / "notebooks" / relative
    nb = load(target)
    matches = [
        c for c in nb["cells"]
        if c.get("cell_type") == "markdown"
        and "Canonical model" in "".join(c.get("source", []))
        and "at a glance" in "".join(c.get("source", [])).lower()
    ]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one canonical summary in {target}, found {len(matches)}")
    cell = matches[0]
    original = "".join(cell["source"])
    pseudocode_marker = "# Canonical model"
    positions = [original.find("\n# Canonical model in pseudocode"), original.find("\n# Canonical models in pseudocode")]
    positions = [p for p in positions if p >= 0]
    if not positions:
        positions = [original.find("\n## Canonical model in pseudocode")]
        positions = [p for p in positions if p >= 0]
    if not positions:
        raise RuntimeError(f"Cannot find pseudocode boundary in {target}")
    boundary = min(positions)
    cell["source"] = (replacement.rstrip() + "\n" + original[boundary:]).splitlines(keepends=True)
    save(target, nb)
