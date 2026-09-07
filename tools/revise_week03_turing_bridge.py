#!/usr/bin/env python3
"""Tighten the Week 3 Turing narrative and particle-to-field bridge."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = json.loads(PATH.read_text())
cells = nb["cells"]
by_id = {cell.get("id"): cell for cell in cells}


def set_source(cell_id, text):
    by_id[cell_id]["source"] = text.splitlines(keepends=True)


set_source(
    "a2fe3243",
    r'''# How did the cheetah get its spots?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Why spots rather than stripes? Indeed, what is a pattern?</span></div>
''',
)

set_source(
    "f129ebdb-49b2-451f-94bf-561270f0ee23",
    r'''<div class="slide-columns" style="grid-template-columns:minmax(0,.78fr) minmax(0,1.22fr);align-items:center;gap:1.1rem;">
  <img class="column-image" src="images/ChatGPT_Cheetah.png" alt="AI-generated striped cheetah" style="display:block;width:auto;max-width:100%;max-height:430px;object-fit:contain;margin:0 auto;">
  <div><p><strong>An AI-generated answer</strong></p><p>The requested appearance is plausible, but it doesn't happen on a cheetah.</p><p class="figure-reference">Image generated with ChatGPT.</p></div>
</div>
''',
)

# Restore Turing's identity and motivation to the slide sequence.
turing = by_id["week03-alan-mathison-turing"]
turing["metadata"]["tags"] = ["slides"]
turing["metadata"]["slideshow"] = {"slide_type": "slide"}
set_source(
    "week03-alan-mathison-turing",
    r'''# Alan Turing

<div class="two-panel equal-panels compact-panels">
  <div class="image-panel"><img src="images/Turing_and_imitation_game.png" alt="Alan Turing and a representation of the imitation game" style="display:block;width:100%;height:270px;object-fit:contain;"></div>
  <div class="text-panel"><p>Turing helped establish theoretical computer science, worked in wartime cryptanalysis and designed early computers.</p><p>At Manchester he turned to mathematical biology: could ordinary physical and chemical processes explain how biological form develops?</p></div>
</div>
''',
)

# Merge the two slide-level explanations. The former instability slide remains
# in the Reader as the more detailed account.
set_source(
    "week03-why-reaction-diffusion",
    r'''## Turing’s mechanism: reaction and diffusion

Turing coupled two familiar processes.

<div class="two-panel equal-panels compact-panels">
  <div class="text-panel"><p><strong>Reaction:</strong> molecules meet and change identity locally.</p></div>
  <div class="text-panel"><p><strong>Diffusion:</strong> irregular motion carries chemicals between nearby locations.</p></div>
</div>

Small perturbations supply many possible spatial wavelengths. Reaction makes most decay, but differential diffusion can make a selected wavelength grow.

$$
\text{stable homogeneous reaction state}
+\text{differential diffusion}
\longrightarrow
\text{selected spatial pattern}
$$

<p><strong>Diffusion-driven instability:</strong> diffusion destabilises a spatially uniform state that was stable to uniform perturbations.</p>

<p><strong>Turing pattern:</strong> the stationary spatial pattern left when the growing variation saturates.</p>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Diffusion normally smooths differences. How could it instead help a pattern grow?</span></div>
''',
)

detail = by_id["week03-turing-six-modes"]
detail["metadata"]["tags"] = ["reader-only"]
detail["metadata"]["slideshow"] = {"slide_type": "skip"}

set_source(
    "dc08556a",
    r'''### One path: distance from the origin

<img src="images/brownian_distance_sqrt.svg" alt="Two Brownian trajectories beginning at a shared point and their distances from the origin compared with square-root reference curves" style="display:block;width:80%;max-height:385px;object-fit:contain;margin:0 auto;">

The two examples use $D=0.10$ and $D=0.35$. The diffusion coefficient $D$ sets the variance accumulated per unit time: over an interval $\Delta t$, each coordinate increment has variance $2D\Delta t$. It is not simply the step size or the number of steps, although either can be calibrated to produce a chosen $D$ in a discrete implementation.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Stay low:</strong> one path is irregular; its typical distance from the start has a square-root scale.</span></div>
''',
)

set_source(
    "54e20377-5977-4ea6-a97b-7482a438a6c9",
    r'''## Gray–Scott model simulation

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Hopfed_turingles.png" alt="Interactive Gray–Scott patterns" style="display:block;width:100%;max-height:350px;object-fit:contain;"></div>
<div class="text-panel">
<p>Hold most controls fixed, change one control, and describe what happens to the morphology.</p>
<p><a href="https://www.complexity-explorables.org/explorables/hopfed-turingles/">Open the Complexity Explorable</a></p>
<p>For now, interpret the controls as particle-level processes: spreading, reaction, supply and removal.</p>
</div>
</div>
''',
)

set_source(
    "4f8c9362",
    r'''# From particle motion to continuous equations

<p>The Complexity Explorable is not directly simulating every particle interaction.</p>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Could it update every molecule, collision and three-particle encounter?</span></div>

An exact particle simulation would require an enormous number of random trajectories and collision tests. Statistical physics handles systems like gases in the same spirit: it replaces unknowable microscopic histories with collective quantities that can be predicted and measured.

We therefore <strong>coarse-grain</strong> the state:

$$
\text{many particle positions}
\quad\longrightarrow\quad
U(\mathbf x,t),\;V(\mathbf x,t),
$$

where the fields record local concentrations. We lose individual histories and gain a tractable description of collective transport and reaction.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over particles:</strong> retain how much of each chemical is present at each location.</span></div>
''',
)

PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
print(PATH)
