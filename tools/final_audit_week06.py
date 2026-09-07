"""Editorial and structural audit fixes for the Week 6 Reader and slides."""

import json
from pathlib import Path

path = Path("notebooks/week06/L_Synchronisation.ipynb")
nb = json.loads(path.read_text())
cells = nb["cells"]


def get(cid):
    return next(c for c in cells if c.get("id") == cid)


def source(cid):
    return "".join(get(cid).get("source", []))


def set_source(cid, text):
    get(cid)["source"] = text.splitlines(keepends=True)


def move_before(ids, anchor):
    picked = [get(cid) for cid in ids]
    cells[:] = [c for c in cells if c.get("id") not in ids]
    i = next(i for i, c in enumerate(cells) if c.get("id") == anchor)
    cells[i:i] = picked


# Tone: replace abstract editorial narration with direct description.
replacements = {
    "Kuramoto is not a literal model of flashing fireflies. It isolates one question: can coupling overcome differences in the clocks' intrinsic rates?":
        "Kuramoto is not a literal model of flashing fireflies. It tests whether coupling can overcome differences in the clocks' intrinsic rates.",
    "The resulting model isolates a narrower question: can coupling overcome heterogeneity in the clocks' intrinsic rates?":
        "The resulting model tests whether coupling can overcome heterogeneity in the clocks' intrinsic rates.",
    "A useful analysis should remove their shared rotation and retain only their separation.":
        "Subtracting the two equations removes their shared rotation and retains only their separation.",
    "This prepares the move from qualitative inspection to a quantitative measure.":
        "The next step replaces the full phase configuration by the single coherence measure $r$.",
    "Placing both on the same axes makes clear which conclusions come from simulation and which come from analysis.":
        "On the shared axes, the finite simulation can be compared directly with the continuum prediction.",
    "This is a useful step between all-to-all Kuramoto coupling and a population of mobile fireflies.":
        "This restores spatially local interaction without yet allowing the oscillators to move.",
    "The progression is deliberate: phase-only Kuramoto, fixed spatial coupling in Spin Wheels, then mobile oscillators whose positions and phases co-evolve. Each step adds one new modelling commitment.":
        "Kuramoto retains phase only. Spin Wheels adds fixed spatial neighbours. Swarmalators then allow position and phase to co-evolve.",
}
for c in cells:
    if c.get("cell_type") != "markdown":
        continue
    text = "".join(c.get("source", []))
    for old, new in replacements.items():
        text = text.replace(old, new)
    c["source"] = text.splitlines(keepends=True)

# Specify-model prompt: focus on the actual modelling decisions without grading one as "simplest".
for cid in ("w6-specify", "firefly-model"):
    text = source(cid)
    text = text.replace(
        "There are many possible implementations. Which is the simplest one that remains consistent with what we observed?",
        "How would you represent the clock, its isolated dynamics, the effect of a flash and who can see it?",
    ).replace(
        "Which implementation is simplest while remaining consistent with the observed behaviour?",
        "How would you represent the clock, its isolated dynamics, the effect of a flash and who can see it?",
    )
    set_source(cid, text)

# Correct the heterogeneous-coupling equation (the earlier generated text contained escaped control characters).
set_source("w6-controlled-heterogeneity-reader", r'''### Controlled heterogeneity experiments

The baseline gives every oscillator the same natural frequency. In a frame rotating at that common frequency, the intrinsic drift disappears. With attractive all-to-all coupling, phase differences then arise from initial conditions and the interaction draws the phases together. This is the `variability = 0` case in the Kuramotocycle.

Next vary one ingredient at a time.

**Natural-frequency heterogeneity:** draw $\omega_i$ from $g(\omega)$ while keeping a common $K$. Oscillators with low natural frequencies must speed up and those with high natural frequencies must slow down to join a frequency-locked group. Their intrinsic frequencies do not change; the interaction changes their realised phase velocities.

<img src="images/kuramoto_frequency_heterogeneity.svg" alt="Kuramoto phases coloured by natural frequency beside the frequency distribution" style="display:block;max-width:100%;margin:1rem auto">

**Coupling heterogeneity:** set the natural frequencies equal and assign each oscillator its own $K_i$,

$$
\dot{\theta}_i
=\omega+\frac{K_i}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i).
$$

Now $K_i$ measures responsiveness: large values pull an oscillator towards the group more quickly, while small values make it less influenced by the others.

<img src="images/kuramoto_coupling_heterogeneity.svg" alt="Different coupling strengths produce different rates of relaxation towards the group phase" style="display:block;max-width:82%;margin:1rem auto">

Only after these effects have been separated should both $\omega_i$ and $K_i$ be drawn from distributions. Varying both immediately may be realistic, but it obscures which assumption changed the collective behaviour.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> return from the population average to the intrinsic frequency and responsiveness assigned to each oscillator.</span></div>
''')

# Ladder signalling: one explicit move at each distinct level of analysis.
if "replace the observed group display" not in source("reader-firefly-kuramoto"):
    set_source("reader-firefly-kuramoto", source("reader-firefly-kuramoto") + '''

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> replace the observed group display by a state, intrinsic dynamics, an interaction rule and an interaction network.</span></div>
''')
if "one number measuring collective coherence" not in source("order-parameter"):
    set_source("order-parameter", source("order-parameter") + '''

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace the full phase configuration by one number measuring collective coherence.</span></div>
''')
set_source("mean-field", source("mean-field").replace(
    "This continuum step produces the sharp analytical onset.",
    "This continuum step produces the sharp analytical onset.\n\n<div class=\"ladder-marker\"><img src=\"images/ladder_marker.svg\" alt=\"Ladder of abstraction\"><span><strong>Up the ladder again:</strong> replace one finite list of frequencies by the population density <i>g</i>(<i>ω</i>).</span></div>",
))

# Kc is a quoted continuum result, with an optional derivation sketch rather than an unexplained jump.
set_source("mean-field", r'''## Analytical mean-field analysis

### Return to mean field

The numerical sweep describes finite populations. Mean-field analysis asks whether the collective onset can be predicted without following every trajectory.

We used a mean-field description for the Game of Life in Week 4. There it was an approximation: replacing a neighbourhood by global live-cell density discarded spatial correlations.

For the all-to-all Kuramoto model, the first reduction is exact:

$$
r e^{\mathrm{i}\psi}=\dfrac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j}.
$$

Multiplying by $e^{-\mathrm{i}\theta_i}$ and taking imaginary parts gives

$$
r\sin(\psi-\theta_i)
=\dfrac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i),
$$

and hence

$$
\dot\theta_i=\omega_i+Kr\sin(\psi-\theta_i).
$$

The large-population calculation then replaces one sampled frequency list by a density $g(\omega)$. For a symmetric unimodal distribution centred at $\bar\omega$, the onset occurs at

$$
K_c=\frac{2}{\pi g(\bar\omega)}.
$$

This result is quoted rather than required as a student derivation. Obtaining it needs the continuum self-consistency argument below, not just the finite-sum algebra above. See [Strogatz (2000), “From Kuramoto to Crawford”](https://doi.org/10.1016/S0167-2789(00)00094-4).

```{dropdown} Optional derivation sketch
Work in the rotating frame so that $\bar\omega=0$. A frequency-locked oscillator satisfies

$$
\omega=Kr\sin\theta.
$$

Only oscillators with $|\omega|\le Kr$ can lock. For a symmetric $g(\omega)$, the drifting oscillators cancel in the stationary average and the locked population gives

$$
r=\int_{-Kr}^{Kr}\sqrt{1-\left(\frac{\omega}{Kr}\right)^2}\,g(\omega)\,\mathrm d\omega.
$$

Set $\omega=Kr\sin\theta$:

$$
1=K\int_{-\pi/2}^{\pi/2}\cos^2\theta\,g(Kr\sin\theta)\,\mathrm d\theta.
$$

At onset, $r\to0^+$, so $g(Kr\sin\theta)\to g(0)$. Since

$$
\int_{-\pi/2}^{\pi/2}\cos^2\theta\,\mathrm d\theta=\frac{\pi}{2},
$$

we obtain $1=K_c g(0)\pi/2$ and therefore $K_c=2/[\pi g(0)]$.
```

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder again:</strong> replace one finite list of frequencies by the population density <i>g</i>(<i>ω</i>).</span></div>
''')

# Remove the duplicated list of later Explorables from Scope; keep only the model boundary here.
set_source("scope", '''# Scope and connections

## What the Kuramoto model represents

The standard model shows how coupling can recruit oscillators with different natural frequencies into a coherent group.

Its assumptions are restrictive. Fireflies communicate with flashes rather than continuous sinusoidal signals. Neural and power-grid interactions are not complete graphs. Delays, noise and unequal coupling can also matter. The final section adds spatial structure in two stages.
''')

# Move numerical heterogeneity slides before the analytical banner.
move_before(
    ["w6-heterogeneity-analysis-slide", "w6-frequency-heterogeneity-slide", "w6-coupling-heterogeneity-slide"],
    "w6-mean-field-return",
)

# Slide prose and formatting: reduce bolding and make ladder moves explicit.
set_source("w6-firefly-kuramoto", source("w6-firefly-kuramoto").replace(
    "It isolates one question", "It tests one question"
) + '''

''')
set_source("w6-order", r'''## Measure collective coherence

$$
r(t)e^{\mathrm{i}\psi(t)}
=\dfrac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p>$\psi$: mean phase.</p><p>$r\approx0$: phases cancel around the circle.</p><p>$r\approx1$: phases are tightly aligned.</p><div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> compress the phase configuration to one coherence measure.</span></div></div>
<div class="image-panel"><img src="images/kuramoto_order_parameter_geometry.svg" alt="Complex phase vectors and their average" style="max-height:330px"></div>
</div>
''')
if "compare ensemble summaries across coupling strengths" not in source("w6-sweep"):
    set_source("w6-sweep", source("w6-sweep") + '''

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder again:</strong> compare ensemble summaries across coupling strengths and system sizes.</span></div>
''')
if "replace a finite sample by a continuum" not in source("w6-mean-field-return"):
    set_source("w6-mean-field-return", source("w6-mean-field-return") + '''

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace a finite sample by a continuum frequency distribution.</span></div>
''')

# Keep the pulse-coupled explorable with the other extensions at the end.
if "### Pulse coupling" not in source("w6-spatial-fireflies-reader"):
    set_source("w6-spatial-fireflies-reader", source("w6-spatial-fireflies-reader") + '''

### Pulse coupling

[**Dr. Fibryll & Mr. Glyde**](https://www.complexity-explorables.org/explorables/dr-fibryll-and-mr-glyde/) replaces continuous sinusoidal influence by pulse-like interaction. This changes the interaction law rather than adding physical space.
''')

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
