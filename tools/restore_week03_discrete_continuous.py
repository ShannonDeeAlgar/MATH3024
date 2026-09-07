from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def md(source, slide_type="", tags=None, cell_id=None):
    cell = nbformat.v4.new_markdown_cell(source=source)
    if cell_id:
        cell.id = cell_id
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    if tags:
        cell.metadata["tags"] = tags
    return cell


nb = nbformat.read(NOTEBOOK, as_version=4)

# Strengthen the first discrete/continuous question without pre-empting the reveal.
nb.cells[36].source = r'''# Is the world discrete or continuous?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>What would we have to track if we modelled every reacting and diffusing particle directly?</span></div>

So far I have encouraged you to picture particles moving, colliding and reacting. That is a useful microscopic story. It is not, however, the representation used by the simulation we have been exploring.
'''

# Restore the deliberate reveal in the middle of the narrative.
nb.cells[40].source = r'''# I have been lying to you. A little.

I have described the model as though we were going to simulate individual particles and their interactions.

That microscopic model is conceivable, but a useful domain contains an enormous number of particles. Tracking every position, collision and reaction would require far more computation than we need for the question we are asking.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Replace individual particles with local concentrations: how much $U$ and $V$ is present near each location?</span></div>
'''

nb.cells[41].source = r'''## From particles to concentrations

The particle story is a microscopic interpretation of the chemistry. It is not the state representation used in the Gray–Scott PDE.

An explicit particle simulation would need to store and update the locations of very many molecules, resolve random motion and collisions, and decide which encounters produce a reaction. That detail is computationally expensive and is not needed if our question is whether large-scale spots, stripes or labyrinths emerge.

We therefore **coarse-grain** the system. A field such as $U(\mathbf x,t)$ records the local concentration of chemical $U$, averaging over many particles near position $\mathbf x$. The model moves up the ladder from individual trajectories to collective fields.

This is the same scientific move used when statistical physics describes a gas through temperature, pressure and density rather than the location of every molecule.
'''

# Replace the scattered reader-only fragments with a clear transition.
nb.cells[67].source = r'''# From equations to a simulation

The reaction–diffusion PDEs are nonlinear and generally do not have a useful analytic solution.

We now make a second change of representation:

$$
\text{continuous concentration fields}
\quad\longrightarrow\quad
\text{values on a finite grid at finite time steps}.
$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Grid spacing, time step, neighbourhood, boundary conditions and numerical stencil become part of the model we actually compute.</span></div>
'''

nb.cells[68].source = r'''## The sequence of representations

Reaction and diffusion occur through microscopic interactions, but the useful macroscopic variables are concentrations. We describe those concentrations continuously with PDEs, then discretise the PDEs so a computer can update a finite array.

1. **Discrete particles:** molecules move and interact.
2. **Continuous description:** concentration fields $U(\mathbf x,t)$ and $V(\mathbf x,t)$ obey PDEs.
3. **Discrete computation:** arrays $U^n_{i,j}$ and $V^n_{i,j}$ approximate those fields on a grid.

None of these is simply “the real model”. Each retains some features and suppresses others.
'''
nb.cells[69].source = r'''### Microscopic reality

Chemical reactions and diffusion-driven pattern formation arise from interactions among discrete particles.
'''
nb.cells[70].source = r'''### Macroscopic model

Instead of tracking those particles, the reaction–diffusion PDE describes continuous concentration fields. This aggregation makes the collective dynamics tractable.
'''
nb.cells[71].source = r'''### Numerical model

To compute an approximation to the continuous PDE, we sample space and time. The simulation is discrete again, but its cells store **concentrations**, not individual particles.
'''

# Explain neighbourhoods before they are used in the finite-difference stencil.
neighbourhood_slide = md(r'''### Which cells count as neighbours?

<div class="two-panel equal-panels">
<div class="text-panel">
<p><strong>Von Neumann neighbourhood</strong></p>
<p>The four cells sharing an edge with the focal cell: north, south, east and west.</p>
<p>The standard five-point Laplacian stencil uses these four neighbours plus the centre.</p>
</div>
<div class="text-panel">
<p><strong>Moore neighbourhood</strong></p>
<p>The eight surrounding cells: the four edge-sharing cells and the four diagonals.</p>
<p>It can support a nine-point stencil, but the weights must be chosen deliberately. Simply adding diagonals changes the numerical operator.</p>
</div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>A neighbourhood is a modelling and numerical choice. It controls which local information can influence one update and can introduce directional artefacts.</span></div>
''', "subslide", ["slides"], "week03-neighbourhoods")
nb.cells.insert(96, neighbourhood_slide)

# The indices below account for the inserted neighbourhood cell.
colour_index = next(i for i, c in enumerate(nb.cells) if c.id == "85c3b79f") if any(c.id == "85c3b79f" for c in nb.cells) else None
for i, c in enumerate(nb.cells):
    if c.cell_type == "markdown" and c.source.startswith("### Colour is part of the representation"):
        c.source = r'''### Colour is part of the representation
<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/Colourblind.png" alt="A pseudo-Ishihara colour-vision image in which the number 74 is formed from green dots among orange dots" style="display:block;width:72%;max-height:390px;object-fit:contain;margin:0 auto;">
<p>Can everyone in the room recover the same information from this image?</p>
</div>
<div class="text-panel">
<p><strong>Colour is part of the representation, not decoration.</strong></p>
<p>Use a perceptually ordered sequential map for concentration. Matplotlib provides accessible defaults including <code>viridis</code>, <code>cividis</code> and <code>plasma</code>.</p>
<p>Avoid rainbow scales and red–green contrasts. Check that ordering remains legible in greyscale and for common colour-vision deficiencies.</p>
<p><a href="https://matplotlib.org/stable/users/explain/colors/colormaps.html">Matplotlib: Choosing Colormaps</a></p>
</div>
</div>
'''
        break

# End by returning to the question, after the empirical examples.
final_slide = md(r'''# So, is the world discrete or continuous?

<div class="analysis-perspectives">
<div><strong>Microscopic interpretation</strong><p>Discrete particles undergo stochastic motion and local reactions.</p></div>
<div><strong>Macroscopic model</strong><p>Continuous concentration fields expose collective reaction–diffusion dynamics.</p></div>
<div><strong>Numerical implementation</strong><p>Discrete grid values approximate the continuous fields at finite resolution.</p></div>
</div>

The useful question is not which description is universally true. It is which details must be retained for the question being asked, and what changes when we move between descriptions.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Where did we gain tractability, and what information did we give up, at each move?</span></div>
''', "slide", ["slides"], "week03-final-discrete-continuous")
nb.cells.append(final_slide)

final_reader = md(r'''## Returning to the modelling choice

The path through this model was

$$
\text{particles}
\longrightarrow
\text{concentration fields}
\longrightarrow
\text{grid values}.
$$

Moving from particles to fields is a coarse-graining step. It makes the collective dynamics visible and greatly reduces the state we must track, but it removes individual trajectories and fluctuations. Moving from continuous fields to a grid makes numerical calculation possible, but introduces resolution, time-step, neighbourhood, stencil and boundary-condition choices.

The discrete and continuous descriptions answer different questions. A careful model states which level it uses, why that level is adequate, and which features might be artefacts of the approximation.
''', "", ["reader-only"], "week03-final-discrete-continuous-reader")
nb.cells.append(final_reader)

nbformat.write(nb, NOTEBOOK)
print(f"Updated {NOTEBOOK}")
