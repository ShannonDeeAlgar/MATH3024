from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
IMAGE = ROOT / "notebooks/week06/images/kuramoto_independent_noise.svg"

INK = "#152a55"
BLUE = "#2f86bd"
ORANGE = "#e35d36"
GOLD = "#f2c14e"
GRID = "#d8e2f0"


def simulate(noise: float, seed: int, *, n: int = 120, coupling: float = 1.8,
             dt: float = 0.03, duration: float = 30.0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    omega = rng.normal(3.0, 0.55, n)
    theta = rng.uniform(0.0, 2 * np.pi, n)
    times = np.arange(0.0, duration + dt, dt)
    coherence = np.empty(times.size)
    for k in range(times.size):
        z = np.mean(np.exp(1j * theta))
        coherence[k] = abs(z)
        theta += (
            omega + coupling * np.imag(z * np.exp(-1j * theta))
        ) * dt + np.sqrt(2 * noise * dt) * rng.normal(size=n)
    return times, coherence


def first_sustained_crossing(values: np.ndarray, dt: float, threshold: float = 0.75,
                             window_time: float = 1.5) -> float:
    """First time raw coherence stays above threshold for the whole interval."""
    window = max(1, int(round(window_time / dt)))
    sustained = np.convolve((values >= threshold).astype(int),
                            np.ones(window, dtype=int), mode="valid")
    crossings = np.flatnonzero(sustained == window)
    return float(crossings[0] * dt) if crossings.size else np.nan


def make_figure() -> None:
    levels = [0.0, 0.10, 0.20]
    colours = [INK, BLUE, ORANGE]
    runs = 24
    all_runs: dict[float, np.ndarray] = {}
    times = None
    for level in levels:
        histories = []
        for seed in range(runs):
            times, coherence = simulate(level, seed)
            histories.append(coherence)
        all_runs[level] = np.asarray(histories)

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2), gridspec_kw={"width_ratios": [1.8, 1, 1]})
    ax = axes[0]
    for level, colour in zip(levels, colours):
        histories = all_runs[level]
        mean = histories.mean(axis=0)
        sd = histories.std(axis=0)
        ax.plot(times, mean, color=colour, lw=2.4, label=fr"$D={level:.2f}$")
        ax.fill_between(times, mean - sd, mean + sd, color=colour, alpha=0.12, linewidth=0)
    ax.axhline(0.75, color=GOLD, lw=1.7, ls="--",
               label=r"$r\geq0.75$ for 1.5 time units")
    ax.set(xlabel="simulation time", ylabel=r"coherence, $r(t)$", ylim=(0, 1.03))
    ax.legend(frameon=False, ncol=2, loc="lower right", fontsize=10)
    ax.set_title("Independent phase noise slows and weakens ordering", loc="left")

    late_means = []
    late_sds = []
    sync_medians = []
    sync_q1 = []
    sync_q3 = []
    for level in levels:
        histories = all_runs[level]
        late = histories[:, -200:].mean(axis=1)
        late_means.append(late.mean())
        late_sds.append(late.std())
        crossings = np.array([first_sustained_crossing(row, 0.03) for row in histories])
        crossings = crossings[np.isfinite(crossings)]
        sync_medians.append(np.median(crossings))
        sync_q1.append(np.quantile(crossings, 0.25))
        sync_q3.append(np.quantile(crossings, 0.75))

    x = np.arange(len(levels))
    axes[1].errorbar(x, late_means, yerr=late_sds, fmt="o", ms=8, capsize=4,
                     color=INK, ecolor=BLUE, lw=2)
    axes[1].set(xticks=x, xticklabels=[f"{d:.2f}" for d in levels], xlabel=r"noise intensity, $D$",
                      ylabel="late-time coherence", ylim=(0.75, 1.0))
    axes[1].set_title("Amount of synchrony", loc="left")

    lower = np.asarray(sync_medians) - np.asarray(sync_q1)
    upper = np.asarray(sync_q3) - np.asarray(sync_medians)
    axes[2].errorbar(x, sync_medians, yerr=np.vstack([lower, upper]), fmt="o", ms=8,
                     capsize=4, color=INK, ecolor=ORANGE, lw=2)
    axes[2].set(xticks=x, xticklabels=[f"{d:.2f}" for d in levels], xlabel=r"noise intensity, $D$",
                      ylabel=r"median time to sustained $r\geq0.75$")
    axes[2].set_title("Run-by-run crossing times", loc="left")

    for panel in axes:
        panel.grid(True, color=GRID, lw=0.8)
        panel.spines[["top", "right"]].set_visible(False)
        panel.tick_params(labelsize=10)
        panel.title.set_color(INK)
    fig.suptitle(r"Matched Kuramoto simulations: $N=120$, $K=1.8$, 24 runs per condition",
                 color=INK, fontsize=14, y=1.02)
    fig.tight_layout()
    IMAGE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGE, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def markdown_cell(cell_id: str, source: str, tags: list[str] | None = None) -> dict:
    metadata = {}
    if tags:
        metadata["tags"] = tags
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": metadata,
        "source": source.splitlines(keepends=True),
    }


def replace_or_insert_after(cells: list[dict], after_id: str, cell: dict) -> None:
    existing = next((i for i, c in enumerate(cells) if c.get("id") == cell["id"]), None)
    if existing is not None:
        cells.pop(existing)
    target = next(i for i, c in enumerate(cells) if c.get("id") == after_id)
    cells.insert(target + 1, cell)


def update_notebook() -> None:
    nb = json.loads(LECTURE.read_text())
    cells = nb["cells"]

    # The distinction previously appeared before the analytical work and without
    # the network equation. Remove that orphaned copy and consolidate it below.
    cells[:] = [c for c in cells if c.get("id") != "reader-network-types"]

    noise_slide = markdown_cell(
        "w6-independent-noise-slide",
        r"""## Independent phase noise

$$
d\theta_i
=\left[\omega_i+\frac{K}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i)\right]dt
+\sqrt{2D}\,dW_i.
$$

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_independent_noise.svg" alt="Matched simulations comparing Kuramoto coherence and time to synchrony under three independent phase-noise intensities" style="max-height:470px"></div>
<div class="text-panel"><p><i>D</i> controls independent clock noise.</p><p>At fixed <i>K</i>, more noise usually lowers sustained coherence and delays a sustained threshold crossing.</p><p>Common or correlated noise is a different model and can sometimes increase synchrony.</p></div>
</div>
""",
        ["slides-only"],
    )
    noise_slide["metadata"]["slideshow"] = {"slide_type": "subslide"}
    replace_or_insert_after(cells, "w6-model-variants-slide", noise_slide)

    noise_reader = markdown_cell(
        "w6-independent-noise-reader",
        r"""### Independent phase noise

The deterministic model assumes that the phase update is exact. A simple stochastic variant gives each oscillator an independent random perturbation,

$$
d\theta_i
=\left[
\omega_i
+\frac{K}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i)
\right]dt
+\sqrt{2D}\,dW_i.
$$

Here $W_i(t)$ are independent Wiener processes and $D$ is the phase-noise intensity. This is not another way of writing heterogeneity in $\omega_i$. Natural-frequency heterogeneity is a persistent difference between clocks; this noise changes from one time interval to the next.

<img src="images/kuramoto_independent_noise.svg" alt="Matched simulations comparing Kuramoto coherence and time to synchrony under three independent phase-noise intensities" style="display:block;max-width:96%;margin:1rem auto">

For these matched simulations, increasing $D$ lowers the late-time value of $r$ and delays synchrony. The first panel shows the mean trajectory and one standard deviation across runs. The time-to-synchrony panel is calculated differently: the sustained threshold crossing is found separately for every run, then summarised by its median and interquartile range. Its points therefore should not be read as intersections of the mean curves with the yellow line.

That direction is typical for independent white phase noise at fixed $K$, but it is not a rule for every stochastic oscillator model. Noise correlation matters. Shared or carefully correlated noise can synchronise oscillators, whereas independent noise continually separates their phases. The question “does noise help?” is incomplete until the source, correlation and point of entry of the noise have been specified. See the review by [Acebrón et al. (2005)](https://doi.org/10.1103/RevModPhys.77.137) and, for an explicit comparison of noise processes, [Bag, Petrosyan and Hu (2007)](https://doi.org/10.1103/PhysRevE.76.056210).

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Decide what “time to synchrony” means before comparing runs: the first threshold crossing, a sustained crossing, or a fitted relaxation time need not give the same answer.</span></div>
""",
        ["reader-only"],
    )
    replace_or_insert_after(cells, "w6-model-variants-reader", noise_reader)

    slide = next(c for c in cells if c.get("id") == "w6-network-variant-slide")
    slide["source"] = r"""## Networks: fixed, changing or adaptive

$$
\dot{\theta}_i
=\omega_i+\frac{K}{k_i}\sum_{j=1}^{N}A_{ij}\sin(\theta_j-\theta_i),
\qquad
k_i=\sum_{j=1}^{N}A_{ij}.
$$

<div class="analysis-perspectives three">
<div><strong>Dynamics on a network</strong><p>The phases evolve while a fixed $A_{ij}$ records who influences whom.</p></div>
<div><strong>Dynamics of a network</strong><p>Edges or nodes change; the network itself is the evolving object.</p></div>
<div><strong>Adaptive network</strong><p>Phases alter the edges and the changed edges alter later phase dynamics.</p></div>
</div>

Hold $g(\omega)$ and the coupling law fixed when comparing complete, local, sparse or modular networks.
""".splitlines(keepends=True)

    reader = next(c for c in cells if c.get("id") == "w6-network-variant-reader")
    reader["source"] = r"""### Networks: fixed, changing or adaptive

Mechanical, electrical, chemical and informational coupling describe different physical systems. Coupling may act one way or both ways, locally or globally, continuously or in pulses, immediately or after a delay. These are properties of the system being represented. The modelling choice is how much of that structure to retain.

For a network rather than all-to-all coupling, let $A_{ij}$ record whether oscillator $j$ influences oscillator $i$, and let $w_{ij}$ give the strength of that influence. One normalised form is

$$
\dot{\theta}_i
=\omega_i
+\frac{K}{s_i}\sum_{j=1}^{N}A_{ij}w_{ij}\sin(\theta_j-\theta_i),
\qquad
s_i=\sum_{j=1}^{N}A_{ij}w_{ij}.
$$

The complete, equally weighted network recovers the standard Kuramoto interaction. Sparse, local or modular choices change who can coordinate with whom. Keep $g(\omega)$ and the coupling law fixed when comparing them.

- **Dynamics on a network:** the phases evolve while $A_{ij}$ and $w_{ij}$ remain fixed.
- **Dynamics of a network:** edges, weights or nodes change, so the network itself evolves.
- **Adaptive or co-evolving network:** the node states affect the network and the changed network feeds back into the node dynamics.

The rewiring investigation in the workshop is adaptive when phase similarity changes the edges and those new edges alter subsequent phase updates. Epidemic-behaviour models provide another example: infection changes behaviour, behaviour changes contacts, and the altered contact network changes transmission.
""".splitlines(keepends=True)

    LECTURE.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    make_figure()
    update_notebook()
    print(f"Updated {LECTURE.relative_to(ROOT)}")
    print(f"Wrote {IMAGE.relative_to(ROOT)}")
