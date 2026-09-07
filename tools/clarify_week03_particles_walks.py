from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"

nb = nbformat.read(PATH, as_version=4)
by_id = {cell.get("id"): cell for cell in nb.cells}

by_id["week03-sand-zebra-first"].source = r'''# Similar patterns, different mechanisms

<div class="two-panel equal-panels compact-panels">
  <div class="image-panel">
    <img src="images/sand_ridges_only.png" alt="Parallel ridges in wind-blown sand" style="display:block;width:100%;height:285px;object-fit:cover;margin:0 auto;">
    <p><strong>Sand ridges</strong></p>
    <p>Transport, erosion and deposition organise the stripes.</p>
  </div>
  <div class="image-panel">
    <img src="images/Zebras.png" alt="Zebra coat stripes" style="display:block;width:100%;height:285px;object-fit:cover;margin:0 auto;">
    <p><strong>Zebra stripes</strong></p>
    <p>Developmental interactions between cells and signals organise the stripes.</p>
  </div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What observations would distinguish a shared form from a shared mechanism?</span></div>'''

by_id["week03-why-reaction-diffusion"].source = r'''## Turing’s proposed solution

Turing proposed two familiar processes acting together.

<div class="two-panel equal-panels compact-panels">
  <div class="text-panel">
    <p><strong>Reaction</strong></p>
    <p>Molecules meet and change identity locally.</p>
    <p><strong>At particle level:</strong> ask which molecules must encounter one another, what the encounter produces, and whether material enters or leaves the system.</p>
  </div>
  <div class="text-panel">
    <p><strong>Diffusion</strong></p>
    <p>Molecules follow irregular trajectories, carrying local chemical changes through tissue.</p>
    <p><strong>Perturbations:</strong> small fluctuations are unavoidable. The coupled system determines whether they decay or grow.</p>
  </div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Diffusion usually disperses differences. Could reactions between moving molecules make a difference grow instead?</span></div>'''

by_id["week03-gray-scott-history"].source = r'''# A concrete particle story: Gray–Scott

Turing supplied a general idea. Gray–Scott gives us a particular chemical story to follow.

$$u+2v\longrightarrow3v.$$

One reaction event consumes one $u$ molecule and requires two existing $v$ molecules. It produces three $v$ molecules, so the net change is

$$\Delta u=-1,\qquad \Delta v=+1.$$

Existing $v$ is therefore required to make one additional $v$: the product promotes its own production. This is **autocatalysis**. Under the mass-action assumption, encounters occur at a rate proportional to $uv^2$.

The reactor also supplies $u$, removes $v$, and allows both molecular species to move randomly.

<p class="small-note">Peter Gray and Stephen K. Scott developed the reaction model for cubic autocatalysis in an open reactor. Pearson’s later spatial simulations made it a canonical pattern-forming model.</p>'''

by_id["week03-gray-scott-history-reader"].source = r'''## Why Gray–Scott?

Turing supplied a general framework rather than a single chemical scheme. Peter Gray and Stephen K. Scott studied **cubic autocatalysis** in an open, continuously stirred reactor. Their problem concerned the dynamics and multiple steady states of a continuously fed chemical system, not animal coats.

At the particle level, the reaction story is

$$u+2v\longrightarrow3v.$$

One event consumes one $u$ and two existing $v$, then produces three $v$. The net change is therefore $\Delta u=-1$ and $\Delta v=+1$. Because existing $v$ is required and there is one more $v$ afterwards, $v$ promotes its own production. That is the sense in which the reaction is **autocatalytic**.

For an ideal well-mixed system, the **mass-action assumption** says that the encounter rate is proportional to the product of the reactant abundances. Requiring one $u$ and two $v$ molecules therefore gives a rate proportional to $uv^2$. This is a modelling assumption about random mixing and encounters, not a statement that every microscopic collision reacts.

The reactor supplies $u$, removes $v$, and the molecules move. John Pearson later simulated the spatially extended model and mapped spots, waves, splitting structures and irregular dynamics. A short rule, inexpensive numerical implementation and rich parameter space made Gray–Scott a useful canonical reaction–diffusion model.

Gray–Scott belongs to Turing's broader reaction–diffusion framework, but not every Gray–Scott pattern is a classical **Turing pattern**. That narrower label requires a uniform equilibrium that is stable without diffusion and destabilised by differential diffusion.

*Gray and Scott (1983, 1984) studied cubic autocatalysis in a continuously stirred tank reactor; Pearson (1993) established the now-familiar spatial pattern catalogue.*'''

# The particle actions are now embedded in Turing's reaction/diffusion boxes.
particle_cell = by_id["week03-particle-reaction-story"]
particle_cell.metadata.setdefault("slideshow", {})["slide_type"] = "skip"
particle_cell.source = r'''### The particle-level reading

Turing's two processes can be read at particle level. Reaction specifies what a suitable molecular encounter changes. Diffusion describes the irregular motion that brings molecules together and carries products elsewhere. In an open Gray–Scott reactor, feed and removal add two further particle events.'''

walk_cell = by_id["b7c839be-6ee3-4fef-9aae-72b880dbb4b9"]
walk_cell.source = r'''### Random walk: a discrete model

<img src="images/random_walk_types_stats.svg" alt="Unbiased, biased and persistent random walks shown with the same 45 unit-length steps and the same spatial scale" style="display:block;width:96%;max-height:360px;object-fit:contain;margin:0 auto;">

$$
\mathbf{X}_n=\sum_{m=1}^{n}\boldsymbol{\xi}_m,
\qquad
\mathbb{E}[\boldsymbol{\xi}_m]=\mathbf{0}
\quad\text{for an unbiased walk}.
$$

Here $\boldsymbol{\xi}_m$ is the displacement on step $m$. Every panel uses $n=45$ steps with $\lVert\boldsymbol{\xi}_m\rVert=1$, so every walker travels a total path length of 45. The biased and persistent walks extend farther from the origin because their directions align, not because their steps are longer or more numerous.

Unit steps automatically have finite variance. Infinite step variance requires unbounded, sufficiently heavy-tailed step lengths, as in an ideal Lévy flight; bias or persistence alone does not cause it.'''

nbformat.write(nb, PATH)
print(PATH)
