from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = nbformat.read(PATH, as_version=4)
by_id = {cell.get("id"): cell for cell in nb.cells}

by_id["11879310"].source = r'''### Brownian motion: the physical phenomenon

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><iframe width="100%" height="275" src="https://www.youtube.com/embed/ZNzoTGv_XiQ" title="Microscope recordings of Brownian motion" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>
<div class="text-panel">
<p>Brownian motion is the continuous-time limit of many small random steps.</p>
<p>Individual paths remain irregular; ensembles reveal the diffusion law.</p>
</div>
</div>

$$
\mathbf{B}(t+\Delta t)-\mathbf{B}(t)
\sim \mathcal{N}(\mathbf{0},2D\Delta t\,I_d),
\qquad
\mathbb{E}\!\left[\lVert\mathbf{B}(t)-\mathbf{B}(0)\rVert^2\right]=2dDt.
$$

The first equation describes one interval $\Delta t$; the second describes displacement accumulated over elapsed time $t$. Here $I_d$ is the $d\times d$ identity matrix, so the coordinate increments are independent and have equal variance. In two dimensions, the expected squared distance is $4Dt$.'''

by_id["week03-brownian-video-reader"].source = r'''### Brownian motion under a microscope

<iframe width="100%" height="420" src="https://www.youtube.com/embed/ZNzoTGv_XiQ" title="Microscope recordings of Brownian motion" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

The film contains many short microscope recordings of real Brownian motion. It runs for about 12 minutes; sample the snippets rather than treating it as a required full-length viewing.

Read

$$
\mathbf B(t+\Delta t)-\mathbf B(t)\sim\mathcal N(\mathbf 0,2D\Delta t I_d)
$$

as follows: over one short interval of duration $\Delta t$, the displacement is Gaussian with mean zero and covariance matrix $2D\Delta t I_d$. The matrix $I_d$ is the $d\times d$ identity matrix. It says that the $d$ coordinate increments are independent and each has variance $2D\Delta t$.

The second relationship uses the total elapsed time $t$, not one increment:

$$
\mathbb E\!\left[\lVert\mathbf B(t)-\mathbf B(0)\rVert^2\right]=2dDt.
$$

In two dimensions the two coordinate variances add, giving $4Dt$. The corresponding typical distance is therefore $\sqrt{4Dt}$, which explains the square-root reference curve on the next figure. For a single increment, the analogous scale would be $\sqrt{4D\Delta t}$.'''

by_id["dc08556a"].source = r'''### One path: distance from the origin

<img src="images/brownian_distance_sqrt.svg" alt="Two Brownian trajectories beginning at the yellow point and their distances from the origin compared with square-root reference curves" style="display:block;width:82%;max-height:400px;object-fit:contain;margin:0 auto;">

<p class="small-note">The yellow marker is the shared starting point, $\mathbf B(0)=\mathbf 0$.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Stay low:</strong> one path is irregular. Its typical distance from the start grows in proportion to $\sqrt{t}$.</span></div>'''

by_id["bf26cf2d"].source = r'''### From one path to an ensemble

<img src="images/brownian_ensemble_msd.svg" alt="Squared displacement for individual Brownian paths, their ensemble mean and the theoretical diffusion law" style="display:block;width:70%;max-height:330px;object-fit:contain;margin:0 auto;">

<p class="small-note">Individual squared displacements vary widely. Averaging many walkers reveals the stable law.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over walkers:</strong> the mean-square displacement approaches $4Dt$.</span></div>'''

by_id["week03-particle-open-reactor"].source = r'''## Keep the particle system driven

Without a continuing supply, the autocatalytic reaction consumes its available $u$ and stops.

<div class="analysis-perspectives three">
  <div><strong>Feed</strong><p>Introduce $u$ from an external reservoir.</p></div>
  <div><strong>Reaction</strong><p>Encounters convert $u$ into additional $v$.</p></div>
  <div><strong>Removal</strong><p>Flow removes material; $v$ may also decay.</p></div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>For a continuously stirred flow reactor, represent constant throughput by memoryless feed and removal rates. Another physical system could require pulsed input, a finite reservoir, spatially localised feed or nonlinear loss.</span></div>'''

# Insert the intentionally particle-labelled model immediately before the explorable.
explorable_index = next(i for i, c in enumerate(nb.cells) if c.get("id") == "54e20377-5977-4ea6-a97b-7482a438a6c9")
if not any(c.get("id") == "week03-lowercase-full-model" for c in nb.cells):
    cell = nbformat.v4.new_markdown_cell(r'''## The full story we appear to be simulating

$$
\frac{\partial u}{\partial t}=D_u\nabla^2u-uv^2+f(1-u),
\qquad
\frac{\partial v}{\partial t}=D_v\nabla^2v+uv^2-(f+k)v.
$$

<div class="analysis-perspectives three">
  <div><strong>Move</strong><p>$D_u$ and $D_v$ control random motion.</p></div>
  <div><strong>React</strong><p>$uv^2$ represents $u+2v\rightarrow3v$.</p></div>
  <div><strong>Enter or leave</strong><p>$f$ and $k$ maintain the open reactor.</p></div>
</div>

For now, read the lower-case symbols as though the explorable tracks the particles in this story.''')
    cell["id"] = "week03-lowercase-full-model"
    cell.metadata["slideshow"] = {"slide_type": "subslide"}
    cell.metadata["tags"] = ["slides"]
    nb.cells.insert(explorable_index, cell)

by_id["week03-feed-kill-reader"].source = r'''### Intuition for feed and kill

The Gray–Scott model represents an **open reactor**. Fresh feed solution tends to restore the $U$ concentration to its nondimensional reservoir value, $U=1$. This gives

$$f(1-U)=f-fU.$$

The term is linear in $U$. It adds material at rate $f$ when the cell is empty of $U$, becomes weaker as $U$ approaches the reservoir concentration, and vanishes at $U=1$. If $U>1$, the same term pulls the concentration back down towards the reservoir value.

Flow also washes out a fixed fraction of the local $V$ concentration per unit time, giving $-fV$. This is linear, first-order loss: doubling $V$ doubles the expected amount removed. The additional **kill** parameter $k$ represents another first-order loss mechanism, giving $-kV$. Together they become

$$-(f+k)V.$$

Here “kill” is conventional Gray–Scott terminology for removal or decay. The linear forms assume constant-rate, memoryless throughput and loss. They are appropriate for the ideal open reactor used to define the canonical model, but they are still modelling choices. A different application might require saturating, delayed, pulsed or spatially localised input and removal.'''

nbformat.write(nb, PATH)
print(PATH)
