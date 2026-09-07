from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def find_cell(nb, cell_id):
    return next(cell for cell in nb.cells if cell.get("id") == cell_id)


nb = nbformat.read(NOTEBOOK, as_version=4)

# Merge the storage prompt into the preceding representation slide.
particle_cell = find_cell(nb, "4f8c9362")
particle_cell.source = r'''# The particle story is not the simulation

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Could the explorable be updating every molecule, collision and three-particle encounter?</span></div>

An exact particle simulation would update an enormous number of random trajectories, detect molecular encounters and decide which encounters react. That is far more microscopic detail and computation than our pattern question requires.

We instead change the state representation:

$$
\text{many particle positions}
\quad\longrightarrow\quad
U(\mathbf x,t),\;V(\mathbf x,t),
$$

where the two fields record local concentrations averaged over many particles.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over particles:</strong> discard individual histories and retain the amount of each chemical at each location.</span></div>'''

storage_cell = find_cell(nb, "d67005af-86fe-4102-b7b8-0cf9f629d586")
nb.cells.remove(storage_cell)

# Guarantee a side-by-side field description in both the Reader and slides.
field_cell = find_cell(nb, "1c111a8d-516f-4637-95c0-080efdec3d90")
field_cell.source = r'''## Continuous description: a diffusion field

<div style="display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);gap:1rem;align-items:center;">
  <div class="text-panel">
    <p>The field $C(\mathbf x,t)$ records concentration at every location and time. The diffusion coefficient $D$ controls the ensemble spreading rate.</p>
    <p>In one dimension, a positive second derivative means the value sits below its surroundings; diffusion raises it. A negative second derivative marks a local peak; diffusion lowers it.</p>
    <p>The Laplacian $\nabla^2C$ generalises this curvature comparison to several directions. It is positive in a local valley, negative at a local peak and zero on a locally linear field.</p>
    $$
    \frac{\partial C}{\partial t}=D\nabla^2C.
    $$
  </div>
  <div class="image-panel"><img src="images/Ficks_diffusion_micro_macro.gif" alt="Microscopic particle motion and macroscopic concentration spreading" style="display:block;width:100%;max-height:360px;object-fit:contain;margin:0 auto;"></div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace individual paths by a field equation that preserves their collective spreading.</span></div>'''

# State the conceptual condition before introducing the general equations.
general = find_cell(nb, "week03-turing-paper-scope")
condition = find_cell(nb, "week03-turing-six-modes")
nb.cells.remove(condition)
general_index = nb.cells.index(general)
nb.cells.insert(general_index, condition)

nbformat.write(nb, NOTEBOOK)
