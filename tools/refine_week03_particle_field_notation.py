import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = json.loads(PATH.read_text())


def set_source(cell, text):
    cell["source"] = [line + "\n" for line in text.strip().splitlines()]


def md(cell_id, text):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": ["reader-only"], "slideshow": {"slide_type": "skip"}},
        "source": [line + "\n" for line in text.strip().splitlines()],
    }


by_id = {c.get("id"): c for c in nb["cells"]}

# Give the generated image and its explanation comparable space.
set_source(by_id["f129ebdb-49b2-451f-94bf-561270f0ee23"], r"""
<div class="slide-columns" style="grid-template-columns:minmax(0,.78fr) minmax(0,1.22fr);align-items:center;gap:1.1rem;">
  <img class="column-image" src="images/ChatGPT_Cheetah.png" alt="AI-generated striped cheetah" style="display:block;width:auto;max-width:100%;max-height:430px;object-fit:contain;margin:0 auto;">
  <div><p><strong>An AI-generated answer</strong></p><p>The requested appearance is plausible, but the image does not explain how a biological pattern develops.</p><p class="figure-reference">Image generated with ChatGPT.</p></div>
</div>
""")

# Lowercase labels denote individual particles throughout session one.
for cid in ["week03-gray-scott-history", "week03-gray-scott-history-reader", "week03-particle-reaction-story", "week03-particle-open-reactor"]:
    c = by_id[cid]
    s = "".join(c["source"])
    for old, new in [("U+2V", "u+2v"), ("3V", "3v"), ("$U$", "$u$"), ("$V$", "$v$")]:
        s = s.replace(old, new)
    set_source(c, s)

set_source(by_id["b7c839be-6ee3-4fef-9aae-72b880dbb4b9"], r"""
### Random walk: a discrete model

<img src="images/random_walk_types_stats.svg" alt="Unbiased, biased and persistent random walks shown with the same unit step length and spatial scale" style="display:block;width:96%;max-height:390px;object-fit:contain;margin:0 auto;">

$$
\mathbf{X}_n=\sum_{m=1}^{n}\boldsymbol{\xi}_m,
\qquad
\mathbb{E}[\boldsymbol{\xi}_m]=\mathbf{0}
\quad\text{for an unbiased walk}.
$$

Here $\boldsymbol{\xi}_m$ is the displacement vector taken on step $m$. The three examples use the same unit step length. They differ in the distribution of direction and in whether successive directions are independent.

For diffusion we begin with independent, unbiased increments of finite variance.
""")

set_source(by_id["11879310"], r"""
### Brownian motion: the physical phenomenon

<div class="two-panel equal-panels">
<div class="image-panel"><iframe width="100%" height="300" src="https://www.youtube.com/embed/ZNzoTGv_XiQ" title="Microscope recordings of Brownian motion" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>
<div class="text-panel">
<p>Brownian motion is the continuous-time stochastic limit of many small, independent random steps.</p>
<p>One path remains irregular. The predictable diffusion law appears in an ensemble or probability density.</p>
</div>
</div>

$$
\mathbf{B}(t+\Delta t)-\mathbf{B}(t)
\sim \mathcal{N}(\mathbf{0},2D\Delta t\,I_d),
\qquad
\mathbb{E}\!\left[\lVert\mathbf{B}(t)-\mathbf{B}(0)\rVert^2\right]=2dDt.
$$

In two dimensions, the two coordinate variances each contribute $2Dt$, so the expected squared distance is $4Dt$.
""")

brownian_reader = md("week03-brownian-video-reader", r"""
### Brownian motion under a microscope

<iframe width="100%" height="420" src="https://www.youtube.com/embed/ZNzoTGv_XiQ" title="Microscope recordings of Brownian motion" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

The film contains many short microscope recordings of real Brownian motion. It runs for about 12 minutes; sample the snippets rather than treating it as a required full-length viewing.

For a two-dimensional Brownian motion, each coordinate contributes variance $2Dt$. Squared distance adds the two coordinate contributions, giving

\[
\mathbb E\!\left[\lVert\mathbf B(t)-\mathbf B(0)\rVert^2\right]=2Dt+2Dt=4Dt.
\]
""")

# The first session ends with the explorable. The reveal follows immediately.
set_source(by_id["54e20377-5977-4ea6-a97b-7482a438a6c9"], r"""
## Gray–Scott model simulation

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Hopfed_turingles.png" alt="Interactive Gray–Scott patterns" style="display:block;width:100%;max-height:430px;object-fit:contain;"></div>
<div class="text-panel">
<p>Use the explorable as a black box. Hold most controls fixed, change one control, and describe what happens to the morphology.</p>
<p><a href="https://www.complexity-explorables.org/explorables/hopfed-turingles/">Open the Complexity Explorable</a></p>
<p>So far our explanation has been entirely particle-level: particles move, meet, react, enter and leave.</p>
</div>
</div>
""")

set_source(by_id["4f8c9362"], r"""
# The particle story is not the simulation

An exact particle simulation would update an enormous number of random trajectories, detect molecular encounters and decide which encounters react. That is far more microscopic detail and computation than our pattern question requires.

We instead change the state representation:

$$
\text{many particle positions}
\quad\longrightarrow\quad
U(\mathbf x,t),\;V(\mathbf x,t),
$$

where the two fields record local concentrations averaged over many particles.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over particles:</strong> discard individual histories and retain the amount of each chemical at each location.</span></div>
""")

set_source(by_id["762e37bb-dee7-495f-9fc4-9b7b764656c9"], r"""
## From particles to concentrations

The microscopic story remains the physical interpretation, but it is no longer the simulated state. The fields $U(\mathbf x,t)$ and $V(\mathbf x,t)$ record local concentrations, averaged over many particles near position $\mathbf x$.

This is **coarse-graining**. It is the same move used when a gas is described by density, temperature and pressure rather than every molecular trajectory. We lose individual histories and gain a tractable description of collective transport and reaction.
""")

set_source(by_id["week03-reader-two-fields"], r"""
### Two concentrations occupy every grid location

At the aggregate level, one grid cell does not contain either $U$ or $V$. It carries both concentrations. At time step $n$, the state at location $(i,j)$ is the pair

\[
\left(U^n_{i,j},V^n_{i,j}\right).
\]

![Two aligned grids showing the U and V concentrations stored at every spatial location](images/two_concentration_fields.svg)

We cannot show both scalar fields with one ordinary colour map. A clear default is therefore to show two aligned panels, one for $U$ and one for $V$, with a separate labelled colour scale for each. A derived image, such as $V-U$ or a thresholded pattern, is another modelling and visualisation choice. It should be labelled as a derived quantity rather than presented as the state itself.
""")

set_source(by_id["8858f425-48a5-492b-9a5a-2d277dacc632"], r"""
## 1. Reaction at the concentration level

The particle story was

$$u+2v\longrightarrow3v.$$

At the aggregate level, let $U(\mathbf x,t)$ and $V(\mathbf x,t)$ denote concentrations. The **mass-action assumption** treats the particles as well mixed locally: the chance of an elementary encounter is proportional to how much of each reactant is present. Doubling $U$ doubles the encounter rate; requiring two $v$ particles contributes two factors of $V$. The local rate is therefore proportional to $UV^2$:

$$
\frac{\partial U}{\partial t}=-UV^2,
\qquad
\frac{\partial V}{\partial t}=+UV^2.
$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Mass action assumes a locally well-mixed elementary reaction. With that assumption, the powers follow from the particle counts in the proposed encounter.</span></div>
""")

set_source(by_id["week03-mass-action-reader"], r"""
## Why does the rate contain $UV^2$?

For an **elementary reaction** governed by mass-action kinetics, the reaction rate is proportional to the product of the reactant concentrations raised to their stoichiometric powers. The intuition is probabilistic. In a locally well-mixed region, finding one $u$ particle is proportional to $U$; finding the two required $v$ particles contributes two factors of $V$. Treating

\[
u+2v\longrightarrow3v
\]

as one elementary event therefore gives $r=KUV^2$. The Gray–Scott equations are normally nondimensionalised so that $K$ is absorbed into the units, leaving $UV^2$.

This is conditional on two modelling decisions: the proposed reaction mechanism and the mass-action approximation. Once those decisions are made, however, $UV^2$ is not an arbitrary term chosen to produce an attractive pattern.
""")

set_source(by_id["d1f8631e"], r"""
## 3. Feed and removal at the concentration level

The open-reactor story becomes

$$
\text{feed of }U:\quad f(1-U),
\qquad
\text{removal of }V:\quad -(f+k)V.
$$

- $f(1-U)$ relaxes $U$ towards the reservoir value $U=1$: feed is strong when the cell is depleted and vanishes when it matches the reservoir.
- Flow also washes out a fraction $fV$ of the local $V$ concentration.
- $kV$ represents additional first-order loss of $V$, such as decay or removal.

Without this continuing throughput, the reaction would consume its available material and stop.
""")

feed_reader = md("week03-feed-kill-reader", r"""
### Intuition for feed and kill

The Gray–Scott model represents an **open reactor**. Fresh feed solution tends to restore the $U$ concentration to its nondimensional reservoir value, $U=1$. This produces $f(1-U)$: it is large where $U$ has been depleted and zero where the local concentration already equals the feed.

Outflow removes whatever $V$ is locally present, giving $-fV$. The additional **kill** parameter $k$ represents first-order loss of $V$, giving $-kV$. Together these become $-(f+k)V$. Here “kill” is conventional Gray–Scott terminology for removal or decay, not a separate reaction encounter.
""")

set_source(by_id["36fa3ed0"], r"""
## The continuous Gray–Scott model

$$
\frac{\partial U}{\partial t}=D_U\nabla^2U-UV^2+f(1-U),
\qquad
\frac{\partial V}{\partial t}=D_V\nabla^2V+UV^2-(f+k)V.
$$

**Local terms:** reaction, feed and removal change concentrations at one location.  
**Spatial terms:** diffusion couples neighbouring locations, generally at different rates.

This is the model we intend to solve. We must next choose a finite representation that a computer can update.
""")

# Apply the uppercase field convention to later explanatory Markdown. Code keeps
# conventional local variable names and is not rewritten mechanically.
boundary = next(i for i, c in enumerate(nb["cells"]) if c.get("id") == "4f8c9362")
for c in nb["cells"][boundary + 1:]:
    if c["cell_type"] != "markdown":
        continue
    s = "".join(c.get("source", []))
    replacements = [
        ("D_u", "D_U"), ("D_v", "D_V"),
        ("uv^2", "UV^2"), ("u(v^n)^2", "U(V^n)^2"),
        ("u(\\mathbf", "U(\\mathbf"), ("v(\\mathbf", "V(\\mathbf"),
        ("u^{n", "U^{n"), ("v^{n", "V^{n"),
        ("u^n", "U^n"), ("v^n", "V^n"),
        ("u_{i", "U_{i"), ("v_{i", "V_{i"),
        ("$u$", "$U$"), ("$v$", "$V$"),
        ("u=1", "U=1"), ("1-u", "1-U"), ("1 - u", "1 - U"),
        ("(f+k)v", "(f+k)V"), ("(f + k)v", "(f + k)V"),
        ("v-u", "V-U"), ("v - u", "V - U"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    set_source(c, s)

# Keep lowercase symbols when explicitly referring back to individual particle
# types, while uppercase symbols denote their aggregate concentrations.
for cid in ["8858f425-48a5-492b-9a5a-2d277dacc632", "week03-mass-action-reader"]:
    c = by_id[cid]
    s = "".join(c["source"])
    s = s.replace("requiring two $V$ particles", "requiring two individual $v$ particles")
    s = s.replace("finding one $U$ particle", "finding one individual $u$ particle")
    s = s.replace("finding the two required $V$ particles", "finding the two required individual $v$ particles")
    set_source(c, s)

# Reinsert managed Reader cells and fix the session-two slide order.
managed = {brownian_reader["id"]: brownian_reader, feed_reader["id"]: feed_reader}
cells = [c for c in nb["cells"] if c.get("id") not in managed]
idx = next(i for i, c in enumerate(cells) if c.get("id") == "11879310")
cells.insert(idx + 1, brownian_reader)
idx = next(i for i, c in enumerate(cells) if c.get("id") == "week03-mass-action-reader")
cells.insert(idx + 1, feed_reader)

# Explorable -> reveal -> representation question.
for cid in ["4f8c9362", "d67005af-86fe-4102-b7b8-0cf9f629d586"]:
    cell = next(c for c in cells if c.get("id") == cid)
    cells.remove(cell)
explore_idx = next(i for i, c in enumerate(cells) if c.get("id") == "54e20377-5977-4ea6-a97b-7482a438a6c9")
cells[explore_idx + 1:explore_idx + 1] = [by_id["4f8c9362"], by_id["d67005af-86fe-4102-b7b8-0cf9f629d586"]]

nb["cells"] = cells
PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
