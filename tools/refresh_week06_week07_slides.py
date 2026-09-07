#!/usr/bin/env python3
"""Create compact Week 6 and Week 7 slide paths while preserving Reader detail."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
WEEK06 = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
WEEK07 = ROOT / "notebooks/week07/L_Intelligent_systems.ipynb"


def md(source: str, cell_id: str, *, slide_type: str = "subslide"):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = ["slides-only"]
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


def preserve_reader(nb, prefix: str):
    nb.cells = [cell for cell in nb.cells if not cell.get("id", "").startswith(prefix)]
    for cell in nb.cells[1:]:
        if cell.metadata.get("slideshow", {}).get("slide_type") in {"slide", "subslide", "fragment"}:
            tags = [tag for tag in cell.metadata.get("tags", []) if tag not in {"slides", "slides-only"}]
            if "reader-only" not in tags:
                tags.append("reader-only")
            cell.metadata["tags"] = tags
            cell.metadata["slideshow"] = {"slide_type": "skip"}


def rebuild_week06():
    nb = nbf.read(WEEK06, as_version=4)
    preserve_reader(nb, "w6-")
    title = nb.cells[0]
    title.metadata["tags"] = ["slides"]
    title.metadata["slideshow"] = {"slide_type": "slide"}

    slides = [
        md(r"""
# Spontaneous synchronisation

<div class="two-panel equal-panels compact-panels">
<div class="text-panel">
<p><strong>Synchronisation</strong> is coordination in time produced through coupling.</p>
<p>The oscillators need not be identical, centrally controlled, or initially aligned.</p>
</div>
<div class="text-panel">
<p>What must be retained?</p>
<p>An internal clock, its natural rate, an interaction rule and a measure of collective timing.</p>
</div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>How can several independent rhythms become coordinated?</span></div>
""", "w6-hook", slide_type="slide"),

        md(r"""
## Fireflies · clocks that influence clocks

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Nicky_Case_fireflies.png" alt="Fireflies represented by internal clocks" style="max-height:390px"></div>
<div class="text-panel">
<p>Each firefly has its own flashing rhythm.</p>
<p>A perceived flash can shift another firefly's clock.</p>
<p>Coherent flashing is a collective outcome, not a command.</p>
</div>
</div>
""", "w6-fireflies"),

        md(r"""
## Specify the model

| Ingredient | Representation |
|---|---|
| Individual state | phase within a cycle |
| Internal dynamics | natural angular frequency |
| Interaction | phase-dependent coupling |
| Network | who can influence whom |
| Observable | collective phase coherence |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>A phase model retains timing and deliberately discards amplitude and biological detail.</span></div>
""", "w6-specify"),

        md(r"""
# Begin with one phase oscillator

A point on the unit circle records position within a cycle:

$$
\dot{\theta}=\omega,
\qquad
\theta(t)=\theta_0+\omega t \pmod{2\pi}.
$$

| Symbol | Meaning |
|---|---|
| $\theta$ | phase |
| $\omega$ | natural angular frequency |
| $T=2\pi/|\omega|$ | period |
""", "w6-one", slide_type="slide"),

        md(r"""
## Two oscillators without coupling

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Two_simple_oscillators.jpeg" alt="Two independent phase oscillators" style="max-height:390px"></div>
<div class="text-panel">
<p>Let $\phi=\theta_1-\theta_2$.</p>
<p>$$\dot\phi=\omega_1-\omega_2.$$</p>
<p>The phase difference drifts unless the natural frequencies match.</p>
</div>
</div>
""", "w6-uncoupled"),

        md(r"""
## Add coupling

Suppose oscillator 2 influences oscillator 1:

$$
\dot{\theta}_1=\omega_1+K\sin(\theta_2-\theta_1),
\qquad
\dot{\theta}_2=\omega_2.
$$

The sine term is zero when phases agree, changes sign when the leader changes, and is strongest at a quarter-cycle separation. The parameter $K$ controls coupling strength.
""", "w6-coupling"),

        md(r"""
## Reduce to their relative phase

With $\Delta\omega=\omega_1-\omega_2$,

$$
\dot\phi=\Delta\omega-K\sin\phi.
$$

A locked separation $\phi^*$ requires

$$
\sin\phi^*=\frac{\Delta\omega}{K},
$$

so locking is possible only when $|\Delta\omega|\le K$.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace two trajectories with one equation for their separation.</span></div>
""", "w6-relative"),

        md(r"""
# Canonical model · Kuramoto oscillators

For $N$ all-to-all coupled phase oscillators,

$$
\dot{\theta}_i
=\omega_i+\frac{K}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i),
\qquad i=1,\ldots,N.
$$

Natural frequencies make the population heterogeneous. Coupling encourages alignment. The factor $1/N$ keeps the total influence comparable as the population grows.
""", "w6-kuramoto", slide_type="slide"),

        md(r"""
## Make the assumptions visible

| Element | Kuramoto choice |
|---|---|
| State | phase $\theta_i$ |
| Internal dynamics | natural frequency $\omega_i$ |
| Network | complete graph |
| Interaction | sinusoidal attraction |
| Control parameter | coupling $K$ |
| Observable | coherence $r$ |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>All-to-all, equal, instantaneous coupling is a simplifying choice rather than a universal property of synchronisation.</span></div>
""", "w6-assumptions"),

        md(r"""
## Watch phases organise

<video controls style="display:block;max-height:480px;max-width:92%;margin:auto">
  <source src="videos/Kuramoto_phase_locking.webm" type="video/webm">
</video>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> follow individual phases before compressing them into one statistic.</span></div>
""", "w6-watch"),

        md(r"""
# Measure collective coherence

$$
r(t)e^{\mathrm{i}\psi(t)}
=\frac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p><strong>$\psi$:</strong> mean phase.</p><p><strong>$r\approx0$:</strong> phases cancel around the circle.</p><p><strong>$r\approx1$:</strong> phases are tightly aligned.</p></div>
<div class="image-panel"><img src="images/Geometric_interpretation_of_order_param.png" alt="Complex phase vectors and their average" style="max-height:330px"></div>
</div>
""", "w6-order", slide_type="slide"),

        md(r"""
## Replace many interactions with a mean field

The order parameter gives the exact identity

$$
\frac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i)
=r\sin(\psi-\theta_i).
$$

Hence

$$
\dot\theta_i=\omega_i+Kr\sin(\psi-\theta_i).
$$

Each oscillator responds to the collective field $(r,\psi)$ rather than to a list of pairwise terms.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over interactions:</strong> compress the population into a mean field.</span></div>
""", "w6-mean-field"),

        md(r"""
# Sweep coupling strength

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Param_sweep.png" alt="Coherence across coupling strengths" style="max-height:390px"></div>
<div class="text-panel">
<p>Small $K$: heterogeneous natural frequencies dominate.</p>
<p>Larger $K$: a coherent group is recruited.</p>
<p>The sweep reveals a system-level transition that is difficult to see from one trajectory.</p>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over a parameter:</strong> compare outcomes across $K$.</span></div>
""", "w6-sweep", slide_type="slide"),

        md(r"""
## Then repeat each condition

| One run | Ensemble |
|---|---|
| one frequency sample and initial state | many independent samples |
| one route towards coherence | typical coherence and variation |
| useful for inspecting locking | tests whether the transition is reproducible |

First use a sweep to reveal a possible pattern. Then use an ensemble to test its robustness.
""", "w6-ensemble"),

        md(r"""
# What survives beyond the toy model?

Coupling can recruit heterogeneous oscillators into coherent motion.

The exact details need not survive: fireflies are pulse-coupled, neural and power-grid networks are sparse, and delays or noise may matter.

A useful model isolates a mechanism and makes its assumptions and scope visible.
""", "w6-scope", slide_type="slide"),
    ]

    nb.cells = [title] + slides + nb.cells[1:]
    nbf.write(nb, WEEK06)


def rebuild_week07():
    nb = nbf.read(WEEK07, as_version=4)
    preserve_reader(nb, "w7-")
    title = nb.cells[0]
    title.metadata["tags"] = ["slides"]
    title.metadata["slideshow"] = {"slide_type": "slide"}

    slides = [
        md(r"""
# What makes a system intelligent?

An intelligent system acquires information and uses it to change what it does.

The intelligence may belong to a machine, an individual, or a collective whose members are individually simple.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Where is the intelligence stored: in an agent, its connections, its environment, or all three?</span></div>
""", "w7-question", slide_type="slide"),

        md(r"""
## Two scientific aims

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><h3>Complexity science</h3><p>Explain how adaptive or intelligent behaviour emerges from interactions among many parts.</p></div>
<div class="text-panel"><h3>Machine learning and AI</h3><p>Build systems that learn from data and perform tasks requiring prediction or decision-making.</p></div>
</div>

Intelligent-systems research often combines explanation with construction.
""", "w7-two-aims"),

        md(r"""
# Supporting model · The perceptron

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Artificial_neuron.png" alt="Artificial neuron" style="max-height:360px"></div>
<div class="text-panel">
<p>A perceptron combines inputs with learned weights and applies a threshold.</p>
<p>Geometrically, it learns a linear decision boundary.</p>
<p>It is a model inspired by neurons, not a faithful copy of one.</p>
</div>
</div>
""", "w7-perceptron", slide_type="slide"),

        md(r"""
## What a linear classifier can and cannot do

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/XOR_linear_classifier.png" alt="Linear separation and the XOR problem" style="max-height:390px"></div>
<div class="text-panel">
<p>A single perceptron can separate classes divided by a line or hyperplane.</p>
<p>It cannot represent XOR with one linear boundary.</p>
<p>Model architecture limits what can be learned, even with perfect data.</p>
</div>
</div>
""", "w7-xor"),

        md(r"""
## Successful prediction is not understanding

AI systems may learn shortcuts that work in training data: a background, hospital label, camera artefact, or other unintended cue.

| Requirement | Question |
|---|---|
| Explainable | Why did this output occur? |
| Fair | Whose errors are larger? |
| Transparent | What data and model produced it? |
| Accountable | Who owns the consequences? |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Choosing a performance measure also chooses what the system is rewarded for learning.</span></div>
""", "w7-ai-limits"),

        md(r"""
# Collective intelligence

Intelligent behaviour can emerge from information shared among interacting agents.

No individual needs a global map, a complete plan, or even a rich internal model. The collective can solve a problem that its members cannot solve alone.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> move from individual actions to the computation performed by the group.</span></div>
""", "w7-collective", slide_type="slide"),

        md(r"""
## Ants communicate through the environment

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Double_bridge_experiment_ants.png" alt="Double bridge experiment with ants" style="max-height:380px"></div>
<div class="text-panel">
<p>Ants deposit pheromone on travelled paths.</p>
<p>Later ants are more likely to follow stronger trails.</p>
<p>Evaporation weakens unused information.</p>
<p>This indirect communication is <strong>stigmergy</strong>.</p>
</div>
</div>
""", "w7-stigmergy"),

        md(r"""
## Positive feedback can reveal a short path

Shorter routes can be completed more often in the same time, so they receive pheromone reinforcement more frequently. More ants then choose them.

$$
\text{individual choices}
\longrightarrow
\text{shared trail}
\longrightarrow
\text{changed future choices}.
$$

The environment acts as an external collective memory.
""", "w7-shortest"),

        md(r"""
## Similar agents can self-organise traffic

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Couzin_lane_formation_data.png" alt="Observed lane formation in army ants" style="max-height:370px"><p><strong>Data:</strong> three traffic lanes form.</p></div>
<div class="image-panel"><img src="images/Couzin_lane_formation_model.png" alt="Model of lane formation in army ants" style="max-height:370px"><p><strong>Model:</strong> local turning and pheromone rules.</p></div>
</div>
""", "w7-lanes"),

        md(r"""
# Biomimicry · copy a principle, not an appearance

| Level | What is borrowed? | Example |
|---|---|---|
| Form | shape or structure | kingfisher-inspired train nose |
| Process | mechanism or behaviour | self-cleaning lotus surface |
| System | relationships and cycles | industrial symbiosis |

Biological inspiration is a source of candidate mechanisms. It is not evidence that the engineered system works.
""", "w7-biomimicry", slide_type="slide"),

        md(r"""
# Canonical model 1 · Ant colony optimisation

ACO turns the ant mechanism into a search algorithm:

1. agents construct candidate paths;
2. path quality determines pheromone deposition;
3. pheromone evaporates;
4. future paths are biased by accumulated pheromone.

The problem must first be represented as movement through a graph.
""", "w7-aco", slide_type="slide"),

        md(r"""
## Make a local edge choice

At a node, an agent balances a fixed heuristic $\eta_e$ with learned pheromone $\tau_e$:

$$
P(e\mid i)
=\frac{\tau_e^{\alpha}\eta_e^{\beta}}
{\sum_{e'\in\mathcal A(i)}\tau_{e'}^{\alpha}\eta_{e'}^{\beta}}.
$$

$\mathcal A(i)$ is the set of available edges. Parameters $\alpha$ and $\beta$ control the balance between social memory and problem-specific information.
""", "w7-aco-choice"),

        md(r"""
## Update the shared memory

After candidate solutions are evaluated,

$$
\tau_e\leftarrow(1-\rho)\tau_e+\sum_{a=1}^{N}\Delta\tau_e^{(a)}.
$$

| Term | Role |
|---|---|
| $\rho$ | evaporation; forget old evidence |
| $\Delta\tau_e^{(a)}$ | reward edge $e$ from agent $a$ |
| $N$ | number of candidate-building agents |

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> inspect one edge choice and one pheromone update.</span></div>
""", "w7-aco-update"),

        md(r"""
# Optimisation is a modelling problem

$$
\min_{x\in\mathcal X} f(x).
$$

| Object | Meaning |
|---|---|
| $x$ | one candidate solution |
| $\mathcal X$ | feasible search space |
| $f(x)$ | objective or fitness |
| constraints | unacceptable candidates or behaviours |

The objective does not merely measure success. It defines what success means to the algorithm.
""", "w7-optimisation", slide_type="slide"),

        md(r"""
## Local and global search

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><h3>Exploitation</h3><p>Refine a promising region using what has already worked.</p><p>Efficient, but can become trapped near a local optimum.</p></div>
<div class="text-panel"><h3>Exploration</h3><p>Search new regions and preserve diversity.</p><p>Discovers alternatives, but can waste evaluations.</p></div>
</div>

Good search balances both behaviours over time.
""", "w7-explore-exploit"),

        md(r"""
# Canonical model 2 · Particle swarm optimisation

Each particle stores:

- its current position $x_i$ and velocity $v_i$;
- its personal best position $p_i$;
- a social best position $g$ shared by the swarm or neighbourhood.

The swarm searches by repeatedly moving, evaluating and sharing discoveries.
""", "w7-pso", slide_type="slide"),

        md(r"""
## The PSO update

$$
v_i^{t+1}
=w v_i^t
+c_1r_1(p_i-x_i^t)
+c_2r_2(g-x_i^t),
$$

$$
x_i^{t+1}=x_i^t+v_i^{t+1}.
$$

| Component | Interpretation |
|---|---|
| $w v_i^t$ | inertia |
| $c_1r_1(p_i-x_i^t)$ | personal experience |
| $c_2r_2(g-x_i^t)$ | social information |
""", "w7-pso-update"),

        md(r"""
## Watch information reshape motion

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/ParticleSwarmArrowsAnimation.gif" alt="Particle swarm optimisation animation" style="max-height:420px"></div>
<div class="text-panel">
<p>Particles do not follow the gradient directly.</p>
<p>Previously successful positions act as moving attractors.</p>
<p>Random coefficients preserve variation in the search.</p>
</div>
</div>
""", "w7-pso-watch"),

        md(r"""
## Parameter choices change collective behaviour

| Choice | Too small | Too large |
|---|---|---|
| inertia $w$ | premature settling | persistent overshoot |
| personal weight $c_1$ | weak individual search | particles ignore the group |
| social weight $c_2$ | poor information sharing | rapid collapse to one region |
| neighbourhood | slow communication | loss of diversity |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The topology of information sharing is part of the optimiser.</span></div>
""", "w7-pso-parameters"),

        md(r"""
# The common mechanism

| System | Local information | Shared information | Collective outcome |
|---|---|---|---|
| perceptron | one labelled example | learned weights | classification |
| ant colony | one path choice | pheromone field | route discovery |
| particle swarm | one particle's history | social best | optimisation |

Intelligence appears here as information accumulated, communicated and used to alter future behaviour.
""", "w7-synthesis", slide_type="slide"),

        md(r"""
# What should we ask of an intelligent system?

1. What information can each component access?
2. Where is memory stored?
3. How does experience change future behaviour?
4. What objective or feedback defines success?
5. What fails when information is biased, delayed or prematurely shared?

These questions apply whether the system is biological, social or engineered.
""", "w7-close", slide_type="slide"),
    ]

    nb.cells = [title] + slides + nb.cells[1:]
    nbf.write(nb, WEEK07)


if __name__ == "__main__":
    rebuild_week06()
    rebuild_week07()
    print("Refreshed Week 6 and Week 7 slide paths.")
