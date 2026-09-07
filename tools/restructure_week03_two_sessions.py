import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def source(text: str):
    return [line + "\n" for line in text.rstrip().splitlines()]


def markdown(cell_id: str, text: str, slide_type="slide", tags=None):
    metadata = {"slideshow": {"slide_type": slide_type}}
    if tags is not None:
        metadata["tags"] = tags
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": metadata,
        "source": source(text),
    }


nb = json.loads(NOTEBOOK.read_text())
cells = nb["cells"]
by_id = {cell.get("id"): cell for cell in cells}


def set_text(cell_id: str, text: str):
    by_id[cell_id]["source"] = source(text)


set_text(
    "week03-why-reaction-diffusion",
    r"""## Turing’s proposed solution

Turing proposed two familiar processes acting together.

<div class="analysis-perspectives three">
  <div><strong>Reaction</strong><p>Molecules meet, react and change identity locally.</p></div>
  <div><strong>Diffusion</strong><p>Molecules move randomly and carry those local changes through tissue.</p></div>
  <div><strong>Perturbations</strong><p>Small fluctuations are unavoidable. They may decay or grow.</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Diffusion usually disperses differences. Could reactions between moving molecules make a difference grow instead?</span></div>""",
)

set_text(
    "week03-gray-scott-history",
    r"""# A concrete particle story: Gray–Scott

Turing supplied a general idea. Gray–Scott gives us a particular chemical story to follow.

$$U+2V\longrightarrow3V.$$

One $U$ molecule and two $V$ molecules meet. The $U$ is converted, leaving three $V$ molecules. The product therefore helps make more of itself: **autocatalysis**.

The reactor also supplies $U$, removes $V$, and allows both molecular species to move randomly.

<p class="small-note">Peter Gray and Stephen K. Scott developed the reaction model for cubic autocatalysis in an open reactor. Pearson’s later spatial simulations made it a canonical pattern-forming model.</p>""",
)

set_text(
    "week03-gray-scott-history-reader",
    r"""## Why Gray–Scott?

Turing supplied a general framework rather than a single chemical scheme. Peter Gray and Stephen K. Scott studied **cubic autocatalysis** in an open, continuously stirred reactor. Their problem concerned the dynamics and multiple steady states of a continuously fed chemical system, not animal coats.

At the particle level, the reaction story is

$$U+2V\longrightarrow3V.$$

The product helps produce more of itself. The reactor supplies $U$, removes $V$, and the molecules move. John Pearson later simulated the spatially extended model and mapped spots, waves, splitting structures and irregular dynamics. A short rule, inexpensive numerical implementation and rich parameter space made Gray–Scott a useful canonical reaction–diffusion model.

Gray–Scott belongs to Turing's broader reaction–diffusion framework, but not every Gray–Scott pattern is a classical **Turing pattern**. That narrower label requires a uniform equilibrium that is stable without diffusion and destabilised by differential diffusion.

*Gray and Scott (1983, 1984) studied cubic autocatalysis in a continuously stirred tank reactor; Pearson (1993) established the now-familiar spatial pattern catalogue.*""",
)

particle_reaction = markdown(
    "week03-particle-reaction-story",
    r"""## What would the particles do?

<div class="analysis-perspectives three">
  <div><strong>Move</strong><p>Each molecule follows an irregular trajectory produced by many collisions.</p></div>
  <div><strong>React</strong><p>A suitable encounter between one $U$ and two $V$ molecules can produce another $V$.</p></div>
  <div><strong>Enter or leave</strong><p>The open reactor supplies $U$ and removes material.</p></div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Stay low:</strong> begin with the entities and events that physically produce the system.</span></div>""",
    slide_type="subslide",
    tags=["slides"],
)

particle_open = markdown(
    "week03-particle-open-reactor",
    r"""## Keep the particle system driven

Without a continuing supply, the autocatalytic reaction eventually consumes its available $U$ and stops.

<div class="analysis-perspectives three">
  <div><strong>Feed</strong><p>Introduce new $U$ molecules.</p></div>
  <div><strong>Reaction</strong><p>Encounters can convert $U$ into $V$.</p></div>
  <div><strong>Removal</strong><p>Allow $V$ and other material to leave.</p></div>
</div>

The explorable appears to simulate this literal particle story. For the moment, treat it as a black box and ask what the controls do to the visible pattern.""",
    slide_type="subslide",
    tags=["slides"],
)

set_text(
    "54e20377-5977-4ea6-a97b-7482a438a6c9",
    r"""## First encounter with the Gray–Scott system

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Hopfed_turingles.png" alt="Interactive Gray–Scott patterns" style="width:100%;"></div>
<div class="text-panel">
<p>Use the explorable as a black box. Hold most controls fixed, change one control, and describe what happens to the morphology.</p>
<p><a href="https://www.complexity-explorables.org/explorables/hopfed-turingles/">Open the Complexity Explorable</a></p>
<p>So far our explanation has been entirely particle-level: molecules move, meet, react, enter and leave. In the next session we ask whether that is what the computer can actually be tracking.</p>
</div>
</div>""",
)

set_text(
    "d67005af-86fe-4102-b7b8-0cf9f629d586",
    r"""# What is the simulation actually storing?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Could the explorable be updating every molecule, collision and three-particle encounter?</span></div>

The particle story explains the physical mechanism. It does not tell us which state representation is computationally sensible.""",
)

set_text(
    "4f8c9362",
    r"""# The particle story is not the simulation

An exact particle simulation would update an enormous number of random trajectories, detect molecular encounters and decide which encounters react. That is far more microscopic detail and computation than our pattern question requires.

We instead change the state representation:

$$
\text{many particle positions}
\quad\longrightarrow\quad
u(\mathbf x,t),\;v(\mathbf x,t),
$$

where the two fields record local concentrations averaged over many particles.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over particles:</strong> discard individual histories and retain the amount of each chemical at each location.</span></div>""",
)

set_text(
    "762e37bb-dee7-495f-9fc4-9b7b764656c9",
    r"""## From particles to concentrations

The microscopic story remains the physical interpretation, but it is no longer the simulated state. The fields $u(\mathbf x,t)$ and $v(\mathbf x,t)$ record the local concentrations of chemicals $U$ and $V$, averaged over many particles near position $\mathbf x$.

This is **coarse-graining**. It is the same move used when a gas is described by density, temperature and pressure rather than every molecular trajectory. We lose individual histories and gain a tractable description of collective transport and reaction.""",
)

set_text(
    "8858f425-48a5-492b-9a5a-2d277dacc632",
    r"""## 1. Reaction at the concentration level

The particle story was

$$U+2V\longrightarrow3V.$$

At the aggregate level, let $u(\mathbf x,t)$ and $v(\mathbf x,t)$ denote concentrations. Under the **mass-action assumption**, treating the event as an elementary reaction gives a local rate proportional to $uv^2$:

$$
\frac{\partial u}{\partial t}=-uv^2,
\qquad
\frac{\partial v}{\partial t}=+uv^2.
$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The mechanism and mass-action description are modelling choices. Given them, the powers of $u$ and $v$ follow from the molecular counts in the proposed elementary reaction.</span></div>""",
)

set_text(
    "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6",
    r"""## 2. Diffusion at the concentration level

Random motion spreads the two particle populations. At the aggregate level this becomes

$$
\frac{\partial u}{\partial t}=D_u\nabla^2u,
\qquad
\frac{\partial v}{\partial t}=D_v\nabla^2v.
$$

The Laplacian compares a location with its surroundings. Peaks spread out and troughs fill in. The coefficients $D_u$ and $D_v$ retain the different ensemble spreading rates of the two molecular species.""",
)

set_text(
    "d1f8631e",
    r"""## 3. Feed and removal at the concentration level

The open-reactor story becomes

$$
\text{feed of }U:\quad f(1-u),
\qquad
\text{removal of }V:\quad -(f+k)v.
$$

- $f$ replenishes $U$ towards the reservoir concentration $u=1$.
- The same flow dilutes $V$ at rate $f$.
- $k$ supplies additional removal of $V$.

Without these terms, the autocatalytic reaction would consume its available material and stop.""",
)

set_text(
    "83145c3c-d8d8-4002-acdc-2bd46b355ee3",
    r"""## Two concentrations occupy every grid location

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/two_concentration_fields.svg" alt="Aligned U and V concentration grids showing that each grid location stores two values" style="display:block;width:100%;max-height:450px;object-fit:contain;"></div>
<div class="text-panel">
<p>At cell $(i,j)$ and time level $n$, the state is the pair $(u^n_{i,j},v^n_{i,j})$. The two arrays use the same spatial grid.</p>
<p>We can show $u$ and $v$ in separate panels, encode one derived quantity such as $v/(u+v)$, or design a bivariate display. Separate sequential maps are usually the clearest starting point.</p>
<p>A single colour map displays only one field. Its label must say which field is shown.</p>
</div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Visualisation is another representation choice. It does not change the simulated state, but it changes what patterns we can see.</span></div>""",
)
by_id["83145c3c-d8d8-4002-acdc-2bd46b355ee3"]["metadata"] = {
    "slideshow": {"slide_type": "subslide"},
    "tags": ["slides"],
}

set_text(
    "week03-return-to-simulation",
    r"""## Return to the Gray–Scott simulation

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/gray_scott_two_fields.png" alt="The U and V concentration fields from one Gray–Scott simulation" style="display:block;width:100%;max-height:470px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>This is a simulation of the complete discrete Gray–Scott equations, not diffusion alone.</p>
<p>Both images describe the same run and the same grid. The left panel displays $u$; the right displays $v$. Where autocatalytic $V$ is concentrated, $U$ has generally been depleted.</p>
<p>The apparent pattern depends on which field and colour scale we display. The simulated state contains both arrays.</p>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> after checking the local update, compare fields, runs and parameter choices to identify robust morphology.</span></div>""",
)


# Rebuild the two-session argument without duplicating any existing cell.
front_end_id = "week03-why-reaction-diffusion"
front_index = next(i for i, c in enumerate(cells) if c.get("id") == front_end_id)
prefix = [
    cell
    for cell in cells[: front_index + 1]
    if cell.get("id") != "week03-choosing-representation-reader"
]

session_one_ids = [
    "week03-gray-scott-history",
    "week03-gray-scott-history-reader",
]
session_one = [by_id[i] for i in session_one_ids] + [particle_reaction]
session_one += [by_id[i] for i in [
    "b7c839be-6ee3-4fef-9aae-72b880dbb4b9",
    "11879310",
    "dc08556a",
    "week03-brownian-ensemble",
    "bf26cf2d",
    "25b5d7f3",
    "a241f850",
]]
session_one += [particle_open, by_id["54e20377-5977-4ea6-a97b-7482a438a6c9"]]

session_two_ids = [
    "d67005af-86fe-4102-b7b8-0cf9f629d586",
    "4f8c9362",
    "762e37bb-dee7-495f-9fc4-9b7b764656c9",
    "week03-choosing-representation-reader",
    "2ba9c92e-5488-45b4-a697-7aa99f2bc487",
    "1c111a8d-516f-4637-95c0-080efdec3d90",
    "week03-turing-six-modes",
    "week03-turing-paper-scope",
    "b72f5b93",
    "d112f5d4",
    "week03-turing-six-reader",
    "week03-turing-dappled",
    "8858f425-48a5-492b-9a5a-2d277dacc632",
    "week03-mass-action-reader",
    "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6",
    "d1f8631e",
    "36fa3ed0",
    "week03-parameter-space",
    "week03-turing-six-evolution",
]
session_two = [by_id[i] for i in session_two_ids]

managed = {c.get("id") for c in prefix + session_one + session_two}
managed.update({"week03-particle-reaction-story", "week03-particle-open-reactor"})
remainder = [c for c in cells if c.get("id") not in managed]

# Put the two-field representation immediately after the continuous-to-grid transition.
two_field = by_id["83145c3c-d8d8-4002-acdc-2bd46b355ee3"]
remainder = [c for c in remainder if c.get("id") != two_field.get("id")]
insert_at = next(i for i, c in enumerate(remainder) if c.get("id") == "954ca579-6444-4529-9190-05fb00912d11") + 1
remainder.insert(insert_at, two_field)

nb["cells"] = prefix + session_one + session_two + remainder
NOTEBOOK.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Reordered and revised {NOTEBOOK}")
