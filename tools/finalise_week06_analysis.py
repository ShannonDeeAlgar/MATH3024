"""Apply the final Week 6 narrative, notation and deployment edits."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def lines(text):
    return text.strip("\n").splitlines(keepends=True)


def markdown(cell_id, text, tags):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": tags, "slideshow": {"slide_type": "subslide"}},
        "source": lines(text),
    }


nb = json.loads(PATH.read_text(encoding="utf-8"))
cells = nb["cells"]
by_id = {cell.get("id"): cell for cell in cells}


def replace(cell_id, text):
    by_id[cell_id]["source"] = lines(text)


replace(
    "w6-huygens",
    r"""
## Huygens · the sympathy of two clocks

In 1665 Christiaan Huygens noticed that two pendulum clocks mounted on one support settled into a persistent temporal relationship.

<div class="reader-voice">
  <div class="reader-voice-quote">A wonderful effect that nobody could have thought of before.</div>
  <div class="reader-voice-attr">— Christiaan Huygens, letter to Constantijn Huygens, 26 February 1665</div>
</div>

Imperceptible movement of the shared support transferred influence between the clocks.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Would the clocks still coordinate on separate walls?</span></div>

<p class="figure-credit"><a href="https://www.dbnl.org/tekst/huyg003oeuv05_01/huyg003oeuv05_01_0141.php">Huygens's February 1665 correspondence</a>.</p>
""",
)

replace(
    "w6-fireflies",
    r"""
## Fireflies · clocks that influence clocks

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Nicky_Case_fireflies.png" alt="Fireflies represented by internal clocks" style="max-height:360px"></div>
<div class="text-panel">
<p>Each firefly has its own flashing rhythm even when isolated: it has internal dynamics.</p>
<p>A perceived flash can shift another firefly's clock.</p>
<p>Coherent flashing is a collective outcome, not a command.</p>
<p>The biological interaction is pulse-like, not the continuous sinusoidal coupling used later in Kuramoto's model.</p>
<p><a href="https://ncase.me/fireflies/">Explore Nicky Case's interactive fireflies</a>.</p>
</div>
</div>
""",
)

replace(
    "w6-assumptions",
    r"""
## Kuramoto model · assumptions

| Element | Kuramoto choice |
|---|---|
| State | phase $\theta_i$ |
| Internal dynamics | natural frequency $\omega_i$ |
| Network | complete graph |
| Interaction | sinusoidal attraction |
| Control parameter | coupling $K$ |
| Observable | coherence $r$ |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The standard model uses equal, instantaneous, all-to-all coupling. Other systems require different interaction networks, weights or delays.</span></div>
""",
)

replace(
    "w6-watch",
    r"""
## Qualitative analysis · watch phases organise

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><video controls preload="metadata" style="display:block;max-height:390px;max-width:100%;margin:auto"><source src="videos/Kuramoto_phase_locking.webm" type="video/webm">Open the <a href="videos/Kuramoto_phase_locking.webm">phase-locking animation</a>.</video></div>
<div class="text-panel"><p>Follow individual phases around the circle and watch coherent groups form.</p><div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> inspect individual phases before compressing them into one statistic.</span></div></div>
</div>
""",
)

mean_field_slide_1 = markdown(
    "w6-mean-field-return",
    r"""
## Return to mean field

Tracking every phase is useful for seeing locking, but it is awkward for describing the population as a whole.

In Week 4, the Game of Life mean-field map assumed that neighbouring cell states were independent. That approximation discarded spatial correlations.

The all-to-all Kuramoto model is different. Its interaction term already sums over the whole population, and the complex order parameter stores exactly the two collective quantities that sum needs:

$$
r e^{i\psi}=\frac{1}{N}\sum_{j=1}^{N}e^{i\theta_j}.
$$

$r$ measures coherence and $\psi$ gives the population's mean phase.
""",
    ["slides-only"],
)

replace(
    "w6-mean-field",
    r"""
## Rewrite the interaction using the mean field

Multiply the order parameter by $e^{-i\theta_i}$:

$$
r e^{i(\psi-\theta_i)}
=\frac{1}{N}\sum_{j=1}^{N}e^{i(\theta_j-\theta_i)}.
$$

Taking imaginary parts gives

$$
r\sin(\psi-\theta_i)
=\frac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i).
$$

Therefore

$$
\dot\theta_i=\omega_i+Kr\sin(\psi-\theta_i).
$$

This is an exact rewriting for the all-to-all model, not a mean-field approximation.
""",
)

replace(
    "w6-sweep",
    r"""
## Parameter sweep · large-population prediction

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Param_sweep.png" alt="Long-time Kuramoto coherence predicted by the continuum mean-field analysis" style="max-height:365px"></div>
<div class="text-panel">
<p><em>r</em><sub>∞</sub> is the long-time coherence.</p>
<p>This is the large-population mean-field prediction, not the result of one finite simulation.</p>
<p>Below <em>K</em><sub>c</sub>, heterogeneous natural frequencies prevent collective locking. Above <em>K</em><sub>c</sub>, a coherent group grows.</p>
<p class="figure-credit">Adapted from Strogatz (2000).</p>
</div>
</div>
""",
)

replace(
    "w6-ensemble",
    r"""
## Compare the prediction with finite simulations

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_ensemble_sweep.svg" alt="Finite Kuramoto ensemble sweep compared with the large-population onset"></div>
<div class="text-panel">
<p>Each faint line is one finite population with <em>N</em> = 180 and frequencies drawn from a standard normal distribution.</p>
<p>Points show the ensemble mean; bars show one standard deviation across ten runs.</p>
<p>The dashed line marks the large-population prediction <em>K</em><sub>c</sub> = 2/[π<em>g</em>(0)].</p>
<p>Finite populations round the transition and vary between samples.</p>
</div>
</div>
""",
)

replace(
    "w6-spatial-fireflies-slide",
    r"""
## Return to the fireflies · put them in space

The phase circle displays each oscillator's internal clock. It is not a map of the fireflies' positions.

Give firefly $i$ a position $\mathbf x_i$ and let coupling depend on separation:

$$
\dot\theta_i=\omega_i+\frac{K}{\sum_j w_{ij}}\sum_j w_{ij}\sin(\theta_j-\theta_i),
\qquad w_{ij}=W(\lVert\mathbf x_j-\mathbf x_i\rVert).
$$

If the fireflies also move, the model needs a second equation for $\dot{\mathbf x}_i$.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What happens if the oscillators move through physical space? How should position enter the state, the interaction rule and the motion rule?</span></div>
""",
)

replace(
    "kuramoto-video",
    r"""
## Qualitative analysis · watch phases organise

<video controls preload="metadata" style="display:block;max-height:500px;max-width:100%;margin:auto">
  <source src="videos/Kuramoto_phase_locking.webm" type="video/webm">
  Open the <a href="videos/Kuramoto_phase_locking.webm">phase-locking animation</a>.
</video>

*Points represent oscillator phases on the unit circle.*
""",
)

replace(
    "mean-field",
    r"""
### Return to mean field

We used a mean-field description for the Game of Life in Week 4. There it was an approximation: replacing a neighbourhood by the global live-cell density assumed away the spatial correlations that make the cellular automaton interesting.

For the standard all-to-all Kuramoto model, the reduction is much better founded. Every oscillator already couples to a sum over the entire population. The complex order parameter

$$
r e^{i\psi}=\frac{1}{N}\sum_{j=1}^{N}e^{i\theta_j}
$$

records the magnitude and direction of that collective phase vector. Multiply both sides by $e^{-i\theta_i}$:

$$
r e^{i(\psi-\theta_i)}
=\frac{1}{N}\sum_{j=1}^{N}e^{i(\theta_j-\theta_i)}.
$$

Taking imaginary parts gives

$$
r\sin(\psi-\theta_i)
=\frac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i).
$$

The $N$-oscillator model can therefore be rewritten exactly as

$$
\dot\theta_i=\omega_i+Kr\sin(\psi-\theta_i).
$$

This is not the independence approximation used for the cellular automaton. It is an exact identity for sinusoidal, all-to-all coupling. The reduction explains the feedback: greater coherence produces a stronger collective pull, while oscillators far from the mean phase experience a larger turning influence.
""",
)

replace(
    "parameter-sweep",
    r"""
## Parameter sweep

<img src="images/Param_sweep.png" alt="Long-time Kuramoto coherence predicted by the continuum mean-field analysis">

Here

$$
r_\infty=\lim_{t\to\infty}r(t)
$$

is the long-time coherence. The curve is the large-population mean-field prediction: it is not one numerical trajectory. Below the critical coupling $K_c$, the incoherent state persists. Above $K_c$, an increasingly large fraction of the population becomes phase locked.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over coupling:</strong> compare long-time coherence across $K$ to reveal the transition towards synchronisation.</span></div>

*Adapted from Strogatz (2000).*
""",
)

replace(
    "ensemble",
    r"""
### Compare theory with finite simulations

<img src="images/kuramoto_ensemble_sweep.svg" alt="Finite-population Kuramoto ensemble sweep compared with the large-population onset">

The figure uses $N=180$ oscillators with $\omega_i\sim\mathcal N(0,1)$. Each faint line is one independently sampled population and initial condition. Points are ensemble means and error bars are one standard deviation across ten runs. For this frequency density, the continuum prediction is

$$
K_c=\frac{2}{\pi g(0)}.
$$

The finite simulations follow the predicted onset but do not produce a perfectly sharp corner. Sampled frequencies, initial phases and finite $N$ introduce variation and round the transition. This is why a parameter sweep should be followed by repeated runs.
""",
)

replace(
    "scope",
    r"""
# Scope and connections

## What the model explains

The Kuramoto model demonstrates how coupling can recruit oscillators with different natural frequencies into a coherent group.

Its standard assumptions are not universal. Fireflies are pulse-coupled; neural and power-grid networks are sparse; delays and noise may matter.

Related Explorables change those assumptions: [**Spin Wheels**](https://www.complexity-explorables.org/explorables/spin-wheels/) places oscillators on a lattice, [**Swårmalätørs**](https://www.complexity-explorables.org/explorables/swarmalators/) couples phase with motion, and [**Dr. Fibryll & Mr. Glyde**](https://www.complexity-explorables.org/explorables/dr-fibryll-and-mr-glyde/) uses pulse-like oscillators.
""",
)

replace(
    "w6-spatial-fireflies-reader",
    r"""
## Return to the fireflies: phase is not physical position

In the standard Kuramoto visualisation, oscillators are arranged around a circle according to phase. Two nearby points have similar internal clock readings; they are not necessarily nearby fireflies. The all-to-all model has no physical spatial domain.

To model fireflies distributed through a forest, give each firefly both a phase $\theta_i$ and a position $\mathbf x_i$. A first extension is to let interaction strength decrease with separation:

$$
\dot\theta_i=\omega_i+\frac{K}{\sum_j w_{ij}}\sum_j w_{ij}\sin(\theta_j-\theta_i),
\qquad
w_{ij}=W(\lVert\mathbf x_j-\mathbf x_i\rVert).
$$

$W$ might impose a fixed visual range or decay gradually with distance. Obstacles, occlusion and delays can then alter who influences whom.

If the fireflies move, position must also evolve:

$$
\dot{\mathbf x}_i=\mathbf v_i(\mathbf x,\theta,t).
$$

When phase affects motion and the changing positions affect phase coupling, the result is a coupled phase-and-motion model, often called a **swarmalator** model. Pulse coupling and individual differences in visual response provide further biologically motivated extensions.

::: {.discussion}
What happens if the oscillators move through physical space? How should position enter the state, the interaction rule and the motion rule?
:::
""",
)

# Remove the redundant Millennium Bridge text slide and the slide-only scope
# summary. Insert the motivation slide immediately before the derivation.
new_cells = []
for cell in cells:
    if cell.get("id") in {"w6-b84357403f", "w6-scope", "w6-mean-field-return"}:
        continue
    if cell.get("id") == "w6-mean-field":
        new_cells.append(mean_field_slide_1)
    new_cells.append(cell)

nb["cells"] = new_cells
PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(PATH)
