#!/usr/bin/env python3
"""Replace Week 7's slides-only layer without changing the Reader narrative."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week07/L_Intelligent_systems.ipynb"


def slide(source: str, cell_id: str, slide_type: str = "subslide"):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n", id=cell_id)
    cell.metadata["tags"] = ["slides", "slides-only"]
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


SLIDES = [
    slide(r"""
# Intelligent systems

<div class="canonical-model-marker"><span><strong>Canonical models</strong> Ant colony optimisation and particle swarm optimisation</span></div>
<div class="modelling-practice-marker"><span><strong>Modelling practice</strong> Represent, evaluate and compare collective search</span></div>

<div class="guiding-question"><span>Guiding question</span><p>How can simple agents store and share information so that a population searches more effectively than one agent?</p></div>
""", "w7-slide-title", "slide"),

    slide(r"""
## The colony as a superorganism

A **superorganism** is a highly integrated society in which specialised individuals cooperate so closely that important functions belong to the colony rather than to any one member.

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p><strong>Ant colonies</strong></p><p>Build trails, regulate traffic, construct living structures and allocate workers without a route planner or foreman.</p></div>
<div class="text-panel"><p><strong>Honeybee colonies</strong></p><p>Share food locations, regulate hive temperature and collectively select new nest sites without a colony-wide map.</p></div>
</div>

<p><strong>The modelling inspiration:</strong> information and control can be distributed across individuals, their interactions and their environment.</p>
""", "w7-slide-superorganism", "slide"),

    slide(r"""
## Honeybees communicate a location

<div class="two-panel wide-left">
<div class="image-panel"><iframe width="100%" height="455" src="https://www.youtube-nocookie.com/embed/-7ijI-g4jHg?rel=0" title="Bee Dance (Waggle Dance)" frameborder="0" allowfullscreen></iframe></div>
<div class="text-panel">
<p><strong>Direction:</strong> the waggle-run angle encodes direction relative to the Sun.</p>
<p><strong>Distance:</strong> waggle duration encodes how far to fly.</p>
<p><strong>Collective effect:</strong> one forager's discovery recruits others to a resource none of them was centrally assigned to find.</p>
</div>
</div>

<p class="media-credit">Video: <a href="https://www.youtube.com/watch?v=-7ijI-g4jHg" target="_blank" rel="noopener">Bee Dance (Waggle Dance)</a>.</p>
""", "w7-slide-waggle-dance"),

    slide(r"""
## From collective motion to collective search

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p><strong>Collective motion</strong></p><p>Vicsek agents use neighbours' headings.</p><p>The question is whether local alignment produces ordered motion.</p></div>
<div class="text-panel"><p><strong>Collective search</strong></p><p>ACO and PSO share evidence about candidate solutions.</p><p>The question is whether interaction helps solve an explicit problem.</p></div>
</div>

The population now interacts with an objective as well as with other agents.
""", "w7-slide-motion-to-search", "slide"),

    slide(r"""
## Collective behaviour takes many forms

<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;align-items:start">
<figure style="margin:0"><img src="images/fire_ant_raft.jpg" alt="Fire ants joined together in a floating raft" style="display:block;width:100%;height:245px;object-fit:cover"><figcaption style="font-size:0.62em;margin-top:0.35rem"><strong>Flood survival.</strong> Fire ants link their bodies into a floating raft.</figcaption></figure>
<figure style="margin:0"><img src="images/weaver_ants_nest.jpg" alt="Weaver ants stitching leaves while constructing a nest" style="display:block;width:100%;height:245px;object-fit:cover"><figcaption style="font-size:0.62em;margin-top:0.35rem"><strong>Collective construction.</strong> Weaver ants pull leaves together and join them with larval silk.</figcaption></figure>
<figure style="margin:0"><img src="images/leafcutter_fungus_garden.jpg" alt="Leafcutter ants tending a fungus garden" style="display:block;width:100%;height:245px;object-fit:cover"><figcaption style="font-size:0.62em;margin-top:0.35rem"><strong>Environmental engineering.</strong> Leafcutters collect plant material to cultivate a mutualistic fungus.</figcaption></figure>
</div>

<p><strong>Each task uses a different collective mechanism.</strong> The bodies, environmental traces and interaction rules depend on the task.</p>

<p class="media-credit">Images: Oo Uui (CC0); PHGCOM (CC BY-SA 4.0); Alex Wild (CC0), via Wikimedia Commons.</p>
""", "w7-slide-ant-diversity"),

    slide(r"""
## Collective intelligence in ants

<div class="image-panel"><iframe width="100%" height="480" src="https://www.youtube-nocookie.com/embed/pa5UnI279Es" title="Ants making a bridge" frameborder="0" allowfullscreen></iframe></div>

<p class="media-credit">Video: Arjunc369, “Ants making bridge, team work”.</p>
""", "w7-slide-ant-video"),

    slide(r"""
## Stigmergy · information stored in the environment

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Double_bridge_experiment_ants.png" alt="Double-bridge experiment with ants" style="max-height:430px"></div>
<div class="text-panel">
<p>Ants deposit pheromone on travelled paths.</p>
<p>Later ants favour stronger trails.</p>
<p>Evaporation weakens unused information.</p>
<p><strong>The environment becomes a shared, changing memory.</strong></p>
</div>
</div>
""", "w7-slide-stigmergy"),

    slide(r"""
## From army-ant data to an individual-based model

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Couzin_lane_formation_data.png" alt="Observed lane formation and trajectories in army ants" style="max-height:385px"><p><strong>Experiment:</strong> filmed trajectories measured speed, turning and interaction distances.</p></div>
<div class="image-panel"><img src="images/Couzin_lane_formation_model.png" alt="Individual-based model of army-ant lane formation" style="max-height:385px"><p><strong>Model:</strong> calibrated local responses reproduce organised three-lane traffic.</p></div>
</div>

The model is evaluated at the population level: do local responses estimated from individual trajectories reproduce the observed three-lane flow, even though no ant is assigned a lane?

<p class="media-credit">Couzin &amp; Franks (2003), <em>Self-organized lane formation and optimized traffic flow in army ants</em>.</p>
""", "w7-slide-couzin-ants"),

    slide(r"""
## Local rules can also amplify failure

<div class="image-panel"><iframe width="100%" height="470" src="https://www.youtube-nocookie.com/embed/LEKwQxO4EZU" title="Why army ants get trapped in death circles" frameborder="0" allowfullscreen></iframe></div>

Following nearby ants normally supports collective foraging. If the trail closes into a loop, the same feedback can trap the group in a rotating mill.

<p class="media-credit">Video: Amaze Lab, “Why army ants get trapped in ‘death circles’”.</p>
""", "w7-slide-ant-death-spiral"),

    slide(r"""
## Optimisation · solution space and fitness

$$
\min_{x\in\mathcal X} f(x)
$$

- **Candidate** $x$: one possible solution.
- **Solution space** $\mathcal X$: all allowed candidates, including any constraints.
- **Objective or fitness** $f(x)$: a numerical score of candidate quality; here, lower is better.
- **Evaluation budget**: the number of candidates the algorithm may score.

If the original score $g(x)$ is to be maximised, define $f(x)=-g(x)$ and minimise $f$.

The solution space is usually abstract: its coordinates are decision variables. A particle's “position” need not be a location in physical space.
""", "w7-slide-optimisation", "slide"),

    slide(r"""
## Canonical model 1 · Ant colony optimisation

<iframe src="images/aco_network_explorer.html" title="Ant colony optimisation learning a route through a network" style="display:block;width:100%;height:545px;border:0;margin:0 auto;"></iframe>
""", "w7-slide-aco-explorer", "slide"),

    slide(r"""
## Specify the ACO model

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p><strong>Problem and state</strong></p>
<p>$G=(V,E)$: graph of allowed connections.</p>
<p>$d_e>0$: fixed cost or length of edge $e$.</p>
<p>$s,T$: start and target nodes.</p>
<p>$\tau_e(n)$: pheromone on edge $e$ at generation $n$.</p>
</div>
<div class="text-panel"><p><strong>Parameters</strong></p>
<p>$N$: ants constructing routes per generation.</p>
<p>$\alpha$: weight given to pheromone.</p>
<p>$\beta$: weight given to the fixed heuristic $\eta_e=1/d_e$.</p>
<p>$\rho$: pheromone evaporation fraction; $Q$: deposit scale.</p>
</div>
</div>

Stop after a stated number of generations or objective evaluations, or when a declared route-cost target is reached.

""", "w7-slide-aco-specification"),

    slide(r"""
## ACO objective · the value of a complete route

If ant $a$ constructs route $R_a$, its objective value is the sum of its edge costs:

$$
L_a=\sum_{e\in R_a}d_e.
$$

Lower $L_a$ is better. In the explorable, the three available routes have costs 6, 8 and 10, so the route of cost 6 is the known optimum.

ACO does not require a separate “fitness” for each ant. The completed route is the candidate solution; $L_a$ measures its quality. The deposit $Q/L_a$ converts lower cost into stronger reinforcement.

For another problem, $L_a$ could instead combine travel time, schedule delay, constraint penalties or another explicitly defined objective.
""", "w7-slide-aco-objective"),

    slide(r"""
## Choose the next edge

For an ant currently at node $i$, $P(e\mid i)$ is the probability that its next selected edge is $e$:

$$
P(e\mid i)=
\frac{\tau_e^{\alpha}\eta_e^{\beta}}
{\displaystyle\sum_{e'\in\mathcal A(i)}\tau_{e'}^{\alpha}\eta_{e'}^{\beta}}.
$$

$\mathcal A(i)$ is the set of currently allowed outgoing edges. Edges that would violate the route constraints are excluded. Sampling from this distribution is repeated until the ant reaches the target and has constructed one complete candidate route.
""", "w7-slide-aco-choice"),

    slide(r"""
## One discrete ACO generation

1. Hold $\tau_e(n)$ fixed while all $N$ ants construct complete routes.
2. Evaluate route $a$ using its total cost $L_a$.
3. Evaporate pheromone and then reward the edges used by shorter routes:

$$
\tau_e(n+1)=(1-\rho)\tau_e(n)+
\sum_{a=1}^{N}\Delta\tau_e^{(a)}
\qquad
\Delta\tau_e^{(a)}=
\begin{cases}
Q/L_a,&e\text{ lies on route }a,\\
0,&\text{otherwise.}
\end{cases}
$$

This is a synchronous generation-level update; there is no physical $\Delta t$.

In the explorable, 30 ants construct routes through successive local edge choices. Their displayed travel along an edge is visual interpolation of the chosen route.
""", "w7-slide-aco-update"),

    slide(r"""
## Assessing ACO search

ACO seeks a low-cost complete route.

| Measurement | Interpretation |
|---|---|
| best route cost | solution quality |
| fraction of runs finding a target-cost route | reliability across stochastic runs |
| completed routes evaluated before first success | search efficiency |
| pheromone concentration and route diversity | how continued search is distributed across the graph |

Once a declared route-cost target is reached, the algorithm can stop and return the best route. While the optimum remains uncertain, repeated route construction reinforces useful edges and tests alternatives. Stochastic choice and evaporation keep alternative routes available. Pheromone concentration can indicate focused refinement or early lock-in, so interpret it alongside the best route cost.
""", "w7-slide-aco-evidence"),

    slide(r"""
## Canonical model 2 · Particle swarm optimisation

Each particle $i$ stores four things:

| State | Meaning |
|---|---|
| $x_i$ | current candidate solution |
| $v_i$ | proposed movement through the search space |
| $p_i$ | particle's personal best position |
| $g$ | best position shared by the swarm |

Particles repeatedly move, evaluate the objective and update these records.
""", "w7-slide-pso-state", "slide"),

    slide(r"""
## The PSO update

For particle $i$ in a $D$-dimensional search space,

$$
x_i^n,\;v_i^n,\;p_i,\;g\in\mathbb R^D.
$$

Here $n$ is an algorithm iteration—not physical time—and $v_i^n$ is a displacement per iteration despite its conventional name “velocity”. PSO is already discrete, so no $\Delta t$ is omitted. The scalar weights $w$, $c_1$ and $c_2$ control inertia, personal memory and shared information respectively.

For every particle and iteration, draw fresh random multipliers $r_{1,i}^n,r_{2,i}^n$ and set

$$
v_i^{n+1}=
\underbrace{w v_i^n}_{\text{inertia}}
+\underbrace{c_1r_{1,i}^n(p_i-x_i^n)}_{\text{personal memory}}
+\underbrace{c_2r_{2,i}^n(g-x_i^n)}_{\text{shared information}},
$$

$$
x_i^{n+1}=x_i^n+v_i^{n+1}.
$$

<p style="font-size:0.72em;color:#5B6780"><strong>Notation:</strong> the coordinate subscript $d$ is suppressed here. The update is applied coordinate by coordinate, with independent $r_{1,i,d}^n,r_{2,i,d}^n\sim\operatorname{Uniform}(0,1)$ draws.</p>
""", "w7-slide-pso-update"),

    slide(r"""
## Exploration and exploitation

Every new objective evaluation can either gather evidence elsewhere or refine what already looks promising.

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p><strong>Exploration</strong> means visiting new or weakly sampled regions and preserving differences between candidate solutions.</p></div>
<div class="text-panel"><p><strong>Exploitation</strong> means concentrating evaluations near the best solutions found so far.</p></div>
</div>

Too much exploration wastes evaluations. Too much exploitation produces <strong>premature convergence</strong>: the population agrees before it has searched sufficiently widely.

PSO balances these tendencies through inertia, personal memory and shared information.

The weights $w$, $c_1$ and $c_2$ are independent coefficients—not proportions. They need not lie in $[0,1]$ or sum to one, and changing one does not automatically change another. Exploration and exploitation are behaviours emerging from their combined effect, the random multipliers and the objective landscape.
""", "w7-slide-exploration-exploitation"),

    slide(r"""
## Rastrigin objective landscape

<img src="images/rastrigin_landscape.png" alt="Two-dimensional Rastrigin objective landscape with many local minima and a global minimum at the origin" style="display:block;max-height:475px;width:auto;margin:0 auto;">

This surface pictures the score assigned to each candidate in a two-dimensional solution space. The axes are candidate variables—not physical coordinates. PSO works the same way when the solution has more dimensions than we can draw.
""", "w7-slide-pso-landscape"),

    slide(r"""
## Interactive particle swarm optimisation

<iframe src="images/pso_explorer.html" title="Interactive particle swarm optimisation explorer" style="display:block;width:100%;height:535px;border:1px solid #C7CEDC;margin:0 auto;"></iframe>
""", "w7-slide-pso-explorer", "slide"),

    slide(r"""
## Quantitative analysis at three levels

<img src="images/pso_analysis_levels.png" alt="PSO results at particle, swarm and ensemble levels" style="display:block;max-height:440px;width:auto;margin:0 auto;">

One trajectory explains an update. One swarm shows a transient. Repeated runs tell us whether the performance is dependable.
""", "w7-slide-pso-analysis", "slide"),

    slide(r"""
## Search reliability and final convergence

<img src="images/pso_exploration_exploitation_sweep.png" alt="Ensemble sweep over personal-memory and shared-information weights" style="display:block;max-height:535px;width:auto;margin:0 auto;">

Each cell represents 20 runs with the same two weights. A run succeeds when the best position found by any particle reaches $f(x)<10^{-2}$. Darker cells on the left mean a larger fraction of runs succeeded. On the right, darker cells mean that particles finished farther from their swarm centroid.

PSO seeks a high-quality solution. The left panel measures reliability across repeated searches. Time or evaluations to first reach the target would measure efficiency. The right panel measures final concentration, which helps diagnose exploration, local refinement and premature convergence. Weak shared information leaves the particles dispersed and makes success less reliable in this experiment.
""", "w7-slide-pso-sweep"),

    slide(r"""
## ACO and PSO use different information pathways

| | ACO | PSO |
|---|---|---|
| candidate | path through a graph | point in a continuous search space |
| memory | pheromone on edges | personal and shared best positions |
| communication | indirect, through the environment | best-so-far record is shared globally |
| main risk | reinforcing a poor route | collapsing too early around a local minimum |

<div style="display:flex;align-items:center;justify-content:center;gap:0.45em;margin-top:0.8em;font-size:0.8em"><strong>Generate a candidate</strong><span style="color:#D69E1E">→</span><strong>Evaluate it</strong><span style="color:#D69E1E">→</span><strong>Update stored information</strong><span style="color:#D69E1E">→</span><strong>Guide the next candidate</strong><span style="color:#D69E1E">↺</span></div>
""", "w7-slide-aco-pso-compare", "slide"),

    slide(r"""
## Agent-based models in retrospect

| Model | Each agent retains | Interaction or shared information | Collective question |
|---|---|---|---|
| Vicsek | position and heading | local alignment with nearby headings, plus noise | when does coherent motion emerge? |
| Kuramoto | phase and natural frequency | phase coupling, usually with the whole population | when can coupling overcome differences between internal clocks? |
| ACO and PSO | a path or candidate solution, plus some form of memory | pheromone in the environment or a shared best position | can a population search for a useful solution? |

The framework is reusable; changing the state, interaction or memory changes the scientific claim.
""", "w7-slide-abm-retrospective", "slide"),

    slide(r"""
## Prediction and explanation

<div class="image-panel" style="max-width:920px;margin:0 auto 0.35em"><img src="images/intelligent_systems_schism.svg" alt="Complexity science and machine learning as complementary approaches to intelligent systems"></div>

David Krakauer describes a scientific **schism** between approaches that retain high-dimensional detail for prediction and approaches that compress a system to expose mechanisms and useful scales.

<p class="figure-source">David Krakauer, <a href="https://complexity.simplecast.com/episodes/1">“The Landscape of 21st Century Science”</a>; see also <a href="https://doi.org/10.3389/fcpxs.2023.1235202">Gilpin et al. (2023)</a>.</p>
""", "w7-slide-schism-return", "slide"),

]


def main():
    notebook = nbf.read(NOTEBOOK, as_version=4)

    kept = []
    for cell in notebook.cells:
        tags = set(cell.metadata.get("tags", []))
        if "slides-only" in tags:
            continue
        if cell is notebook.cells[0]:
            tags.add("reader-only")
            tags.discard("slides")
            cell.metadata["tags"] = sorted(tags)
            cell.metadata.pop("slideshow", None)
        kept.append(cell)

    notebook.cells = SLIDES + kept
    nbf.write(notebook, NOTEBOOK)


if __name__ == "__main__":
    main()
