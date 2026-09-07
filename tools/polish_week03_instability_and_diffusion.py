from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def set_cell(cell, source, slide_type=None, tags=None):
    cell.source = source.strip() + "\n"
    if slide_type is not None:
        cell.metadata["slideshow"] = {"slide_type": slide_type}
    if tags is not None:
        cell.metadata["tags"] = tags


nb = nbformat.read(PATH, as_version=4)
by_id = {cell.id: cell for cell in nb.cells}

set_cell(
    by_id["week03-turing-six-modes"],
    r'''
### Diffusion-driven instability

<div class="definition-panel"><strong>Diffusion-driven instability:</strong> a homogeneous reaction state is stable without spatial variation, but diffusion makes at least one spatial wavelength grow.</div>

$$
\text{stable homogeneous reaction state}
+\text{differential diffusion}
\longrightarrow
\text{a selected spatial wavelength grows}
$$

<div class="analysis-perspectives three compact-panels">
  <div class="text-panel"><p><strong>1. Begin near uniform.</strong><br>Small perturbations contain many wavelengths.</p></div>
  <div class="text-panel"><p><strong>2. Most decay.</strong><br>Reaction restores most differences.</p></div>
  <div class="text-panel"><p><strong>3. Some grow.</strong><br>Diffusion changes the stability of selected wavelengths.</p></div>
</div>

<p><strong>Spatial mode:</strong> a repeating spatial variation with a particular wavelength.</p>

<p><strong>Turing pattern:</strong> the stationary spatial pattern that remains after a growing mode saturates.</p>

<p class="small-note">Different diffusion coefficients are required in the classical two-species mechanism, but that difference alone does not guarantee instability. Linear stability analysis determines which modes grow; it is useful context, but is not assessable here.</p>
''',
)

set_cell(
    by_id["b7c839be-6ee3-4fef-9aae-72b880dbb4b9"],
    r'''
# Understanding diffusion

## Random walk: a discrete model

<img src="images/random_walk_types_stats.svg" alt="Unbiased, biased and persistent random walks, each shown with 45 unit-length steps on the same spatial scale" style="display:block;width:94%;max-height:390px;object-fit:contain;margin:0 auto;">

<p class="small-note">Each path contains 45 unit-length steps and uses the same axes. The rule for choosing the next direction is the only difference.</p>
''',
)

set_cell(
    by_id["bf26cf2d"],
    r'''
### From one path to an ensemble

<img src="images/brownian_ensemble_msd.svg" alt="Individual squared displacements, their ensemble mean at D equals 0.25, and the theoretical diffusion law" style="display:block;width:68%;max-height:325px;object-fit:contain;margin:0 auto;">

<p class="small-note"><i>D</i> = 0.25. The mean-square displacement (MSD) averages squared displacement across the walkers.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over walkers:</strong> the MSD approaches 4<i>Dt</i>.</span></div>
''',
)

set_cell(
    by_id["25b5d7f3"],
    r'''
### Sweep the diffusion coefficient

<img src="images/brownian_diffusion_sweep.svg" alt="Ensemble mean-square displacement for six diffusion coefficients, including D equals 0.25" style="display:block;width:80%;max-height:420px;object-fit:contain;margin:0 auto;">

<p class="small-note"><i>D</i> = 0.25 remains in the sweep, so the previous ensemble can be compared with the wider pattern.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over a parameter:</strong> compare ensembles across values of <i>D</i>.</span></div>
''',
)

set_cell(
    by_id["a241f850"],
    r'''
### Compress each ensemble trajectory

<img src="images/brownian_slope_vs_D.svg" alt="Fitted mean-square-displacement slope against diffusion coefficient, including D equals 0.25" style="display:block;width:68%;max-height:400px;object-fit:contain;margin:0 auto;">

<p class="small-note">Each point is the mean fitted MSD slope; each error bar shows one standard deviation across independent batches. The highlighted point is <i>D</i> = 0.25.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up again:</strong> replace each ensemble curve by its fitted slope and test slope = 4<i>D</i>.</span></div>
''',
)

set_cell(
    by_id["week03-gray-scott-history"],
    r'''
# Add reaction: the Gray–Scott model

Turing supplied a general mechanism, not one unique reaction law. Gray–Scott gives us a particular reaction to explore.

$$u+2v\longrightarrow3v.$$

Existing $v$ is required to produce one additional $v$, so the product promotes its own production. This is <strong>autocatalysis</strong>. Under mass action, the encounter rate is proportional to $uv^2$.
''',
)

# The fuller historical paragraph already lives in the Reader-only
# ``week03-gray-scott-history-reader`` cell.
set_cell(
    by_id["week03-particle-open-reactor"],
    "",
    slide_type="skip",
    tags=["archive-only"],
)

set_cell(
    by_id["week03-lowercase-full-model"],
    r'''
## Particle-level ingredients and controls

At this stage, read the explorable as a story about particles that move, meet, react, enter and leave.

<div class="analysis-perspectives four compact-panels">
  <div><strong>Move</strong><p><i>D</i><sub><i>u</i></sub> and <i>D</i><sub><i>v</i></sub> set how rapidly the species spread.</p></div>
  <div><strong>React</strong><p><i>u</i> + 2<i>v</i> → 3<i>v</i> creates one additional <i>v</i>.</p></div>
  <div><strong>Feed</strong><p><i>f</i> supplies fresh <i>u</i>.</p></div>
  <div><strong>Kill</strong><p><i>k</i>, with outflow, removes <i>v</i>.</p></div>
</div>

<p class="small-note">Feed and removal keep the reactor away from equilibrium. Without them, reactant is exhausted and the transient reaction runs down.</p>
''',
)

# Retain this useful comparison in the Reader, but not as a slide.
by_id["2ba9c92e-5488-45b4-a697-7aa99f2bc487"].metadata["slideshow"] = {"slide_type": "skip"}
by_id["2ba9c92e-5488-45b4-a697-7aa99f2bc487"].metadata["tags"] = ["reader-only"]

set_cell(
    by_id["1c111a8d-516f-4637-95c0-080efdec3d90"],
    r'''
## Diffusion as a concentration field

<div style="display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);gap:1rem;align-items:center;">
  <div class="text-panel">
    <p>The field <i>C</i>(<b>x</b>, <i>t</i>) records concentration at every location and time. The diffusion coefficient <i>D</i> sets the spreading rate inherited from the random walks.</p>
    <p>The Laplacian ∇²<i>C</i> compares a location with its surroundings. It is negative at a local peak and positive in a local valley.</p>
    <p>For positive <i>D</i>, the term <i>D</i>∇²<i>C</i> therefore decreases peaks and increases valleys. The Laplacian determines the direction of smoothing; <i>D</i> controls how quickly it occurs.</p>
  </div>
  <div class="image-panel"><img src="images/Ficks_diffusion_micro_macro.gif" alt="Microscopic particle motion and macroscopic concentration spreading" style="display:block;width:100%;max-height:340px;object-fit:contain;margin:0 auto;"></div>
</div>

$$
\frac{\partial C}{\partial t}=D\nabla^2C.
$$

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace individual paths by a field equation that preserves their collective spreading.</span></div>
''',
)

nbformat.write(nb, PATH)
print(PATH)
