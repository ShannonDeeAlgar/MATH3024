"""Add the Week 6 frequency-width experiment and make the numerical update explicit."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from figure_style import BLUE, INK, LIGHT_BLUE, apply_course_figure_style, finish_axes


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
WORKSHOP = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"
IMAGES = ROOT / "notebooks/week06/images"

ORANGE = "#D95F3B"
GRID = "#D7DFED"


def source(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_source(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True)


def markdown(cell_id: str, text: str, tags: list[str] | None = None) -> dict:
    metadata = {}
    if tags:
        metadata["tags"] = tags
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": metadata,
        "source": text.splitlines(keepends=True),
    }


def code(cell_id: str, text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def insert_after(cells: list[dict], after_id: str, new_cell: dict) -> None:
    cells[:] = [cell for cell in cells if cell.get("id") != new_cell["id"]]
    index = next(i for i, cell in enumerate(cells) if cell.get("id") == after_id)
    cells.insert(index + 1, new_cell)


def render_width_sweep(
    sigmas: np.ndarray,
    values: np.ndarray,
    *,
    n: int,
    coupling: float,
    dt: float,
) -> None:
    """Render stored ensemble outcomes without rerunning the simulation."""
    repeats = values.shape[1]
    mean = values.mean(axis=1)
    sd = values.std(axis=1, ddof=1)
    apply_course_figure_style()
    fig, ax = plt.subplots(figsize=(9.0, 4.9), constrained_layout=True)
    ax.plot(sigmas, mean, "o-", color=INK, lw=2.6, ms=6,
            label="ensemble mean")
    ax.fill_between(
        sigmas,
        np.maximum(0, mean - sd),
        np.minimum(1, mean + sd),
        color=LIGHT_BLUE,
        alpha=0.30,
        label=f"±1 SD across {repeats} populations",
    )
    ax.set(
        xlabel=r"Natural-frequency standard deviation, $\sigma_\omega$",
        ylabel=r"Long-time coherence, $r_\infty$",
        ylim=(-0.03, 1.03),
    )
    finish_axes(ax)
    ax.legend(frameon=False, loc="lower left", ncol=2,
              handlelength=2.2, columnspacing=1.4)
    fig.savefig(IMAGES / "kuramoto_heterogeneity_width_sweep.svg", transparent=True)
    plt.close(fig)


def simulate_width_sweep() -> None:
    rng = np.random.default_rng(302406)
    n = 180
    repeats = 10
    coupling = 2.4
    mean_frequency = 3.0
    dt = 0.02
    sigmas = np.linspace(0.15, 1.75, 11)
    burn_steps = 2200
    sample_steps = 400

    values = np.empty((len(sigmas), repeats))
    for row, sigma in enumerate(sigmas):
        for repeat in range(repeats):
            theta = rng.uniform(-np.pi, np.pi, n)
            offsets = rng.normal(0.0, sigma, n)
            offsets -= offsets.mean()
            omega = mean_frequency + offsets
            total = 0.0
            for step in range(burn_steps + sample_steps):
                z = np.mean(np.exp(1j * theta))
                theta += dt * (omega + coupling * np.imag(z * np.exp(-1j * theta)))
                theta %= 2 * np.pi
                if step >= burn_steps:
                    total += abs(np.mean(np.exp(1j * theta)))
            values[row, repeat] = total / sample_steps

    np.savez(
        IMAGES / "kuramoto_heterogeneity_width_sweep_data.npz",
        sigmas=sigmas,
        values=values,
        coupling=coupling,
        n=n,
        dt=dt,
    )
    render_width_sweep(sigmas, values, n=n, coupling=coupling, dt=dt)


def update_lecture() -> None:
    nb = json.loads(LECTURE.read_text())
    cells = nb["cells"]

    assumptions = next(cell for cell in cells if cell.get("id") == "w6-assumptions")
    text = source(assumptions)
    if "Numerical method" not in text:
        text = text.replace(
            "| Observable | coherence $r$ |",
            "| Observable | coherence $r$ |\n| Numerical method | forward Euler with $\\Delta t=0.02$ unless stated otherwise |",
        )
    set_source(assumptions, text)

    numerical_slide = markdown(
        "w6-discrete-evolution-slide",
        r"""## Discrete evolution used in the simulations

With $t_n=n\Delta t$, forward Euler gives

$$
\theta_i^{n+1}
=\left[\theta_i^n+\Delta t\left(
\omega_i+\frac{K}{N}\sum_{j=1}^{N}\sin(\theta_j^n-\theta_i^n)
\right)\right]\bmod 2\pi.
$$

Unless stated otherwise, the numerical examples use $\Delta t=0.02$. The displayed time is $t_n$, not the frame number $n$.
""",
        ["slides-only"],
    )
    insert_after(cells, "w6-natural-frequency-before-analysis-slide", numerical_slide)

    width_slide = markdown(
        "w6-heterogeneity-width-sweep-slide",
        r"""## Sweep the heterogeneity

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_heterogeneity_width_sweep.svg" alt="Long-time Kuramoto coherence as the natural-frequency distribution is widened"></div>
<div class="text-panel">
<p>Hold the mean frequency, coupling, population size and numerical method fixed.</p>
<p>Increasing <i>σ</i><sub>ω</sub> gives the interaction a wider range of intrinsic rates to overcome.</p>
<p>For this fixed <i>K</i>, collective coherence weakens as the population becomes more heterogeneous.</p>
</div>
</div>
""",
        ["slides-only"],
    )
    insert_after(cells, "w6-sweep", width_slide)

    reader_update = markdown(
        "w6-discrete-evolution-reader",
        r"""### Numerical evolution

The differential equation defines continuous-time dynamics. The animations and parameter sweeps require a numerical approximation. With $t_n=n\Delta t$, forward Euler gives

$$
\theta_i^{n+1}
=\left[\theta_i^n+\Delta t\left(
\omega_i+\frac{K}{N}\sum_{j=1}^{N}\sin(\theta_j^n-\theta_i^n)
\right)\right]\bmod 2\pi.
$$

The modulo operation places the updated phase back on the circle. Unless stated otherwise, the numerical examples use $\Delta t=0.02$, so frame $n$ represents physical simulation time $t_n=n\Delta t$. The time step is a numerical choice, not a parameter in the continuous Kuramoto model; it should still be reported and checked for convergence.
""",
    )
    reader_update["metadata"]["slideshow"] = {"slide_type": "skip"}
    reader_update["metadata"]["tags"] = ["reader-only"]
    insert_after(cells, "w6-natural-frequency-before-analysis-reader", reader_update)

    width_reader = markdown(
        "w6-heterogeneity-width-sweep-reader",
        r"""### Sweep the heterogeneity

<img src="images/kuramoto_heterogeneity_width_sweep.svg" alt="Long-time Kuramoto coherence as the natural-frequency distribution is widened" style="display:block;width:78%;max-width:900px;margin:1rem auto">

Here the natural frequencies follow $\mathcal N(3,\sigma_\omega^2)$. The experiment holds $K=2.4$, $N=180$, $\Delta t=0.02$, the interaction rule and the observation window fixed, then varies only the width $\sigma_\omega$. Each point summarises ten independently sampled populations; the band shows one standard deviation.

At small $\sigma_\omega$, most intrinsic rates are similar and the fixed coupling readily produces a coherent population. Widening the distribution adds increasingly fast and slow oscillators. The same $K$ can no longer lock the whole population, so $r_\infty$ falls. This is the modelling focus of the week made into a controlled experiment: heterogeneity is a parameter of the population, not background decoration.

Changing the shape of $g(\omega)$ is a separate question. A bimodal population is not simply a wider normal population and may form two frequency groups.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace each heterogeneous population by its long-time coherence, then compare those summaries as the population distribution widens.</span></div>
""",
    )
    width_reader["metadata"]["slideshow"] = {"slide_type": "skip"}
    width_reader["metadata"]["tags"] = ["reader-only"]
    insert_after(cells, "parameter-sweep", width_reader)

    canonical = next(cell for cell in cells if cell.get("id") == "canonical-pseudocode")
    text = source(canonical)
    text = text.replace(
        "**Parameters:** population size $N$, coupling $K$, frequency distribution and numerical time step.",
        "**Parameters:** population size $N$, coupling $K$, natural-frequency distribution $g(\\omega)$ and numerical time step $\\Delta t$; the numerical examples use $\\Delta t=0.02$ unless stated otherwise.",
    )
    set_source(canonical, text)

    LECTURE.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


def update_workshop() -> None:
    nb = json.loads(WORKSHOP.read_text())
    cells = nb["cells"]

    specification = next(cell for cell in cells if cell.get("id") == "specification")
    text = source(specification)
    if "Time step" not in text:
        text = text.replace(
            "| Numerical update | synchronous forward Euler |",
            "| Numerical update | synchronous forward Euler |\n| Time step | $\\Delta t=0.02$ unless deliberately varied |",
        )
    text = text.replace(
        "The animation below uses a positive mean frequency and coupling above the onset of collective locking so that the oscillators continue around the circle while their phases organise.",
        "The animation below uses a positive mean frequency and coupling above the onset of collective locking so that the oscillators continue around the circle while their phases organise. Frame $n$ represents time $t_n=n\\Delta t$; the frame number is not itself the simulation time.",
    )
    set_source(specification, text)

    player = next(cell for cell in cells if cell.get("id") == "player")
    text = source(player)
    text = text.replace(
        'def kuramoto_player(history: np.ndarray, element_id="kuramoto-player", highlight_index: int | None = None):',
        'def kuramoto_player(history: np.ndarray, dt: float = 0.02, element_id="kuramoto-player", highlight_index: int | None = None):',
    )
    text = text.replace(
        'label.textContent=`t = ${{k}}`;',
        'label.textContent=`t = ${{(k * ' + "{dt}" + ').toFixed(1)}}`;',
    )
    text = text.replace("display(kuramoto_player(phase_history))", "display(kuramoto_player(phase_history, dt=baseline.dt))")
    set_source(player, text)

    width_intro = markdown(
        "heterogeneity-width-sweep-intro",
        r"""## Widen the frequency distribution

The previous sweep changed the interaction strength. Now hold $K$, $N$, $\Delta t$, the network and the observation window fixed, and vary the natural-frequency standard deviation $\sigma_\omega$.

This isolates the modelling focus of the week. A change in collective behaviour can arise because the population became more heterogeneous even though no individual update rule changed.

> **Up the ladder over populations:** reduce each run to $r_\infty$, then compare repeated populations across $\sigma_\omega$.
""",
    )
    width_code = code(
        "heterogeneity-width-sweep-code",
        r'''frequency_sds = np.linspace(0.15, 1.75, 9)
width_seeds = np.arange(8) + SEED
fixed_coupling = 2.4
width_results = np.empty((len(frequency_sds), len(width_seeds)))

for row, frequency_sd in enumerate(frequency_sds):
    for column, seed in enumerate(width_seeds):
        params = KuramotoParameters(
            n_oscillators=180,
            coupling=fixed_coupling,
            dt=0.02,
            frequency_mean=3.0,
            frequency_sd=float(frequency_sd),
        )
        history, _ = simulate_kuramoto(params, steps=2600, seed=int(seed))
        r, _ = coherence(history[-400:])
        width_results[row, column] = r.mean()

mean_width = width_results.mean(axis=1)
sd_width = width_results.std(axis=1, ddof=1)

fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(frequency_sds, mean_width, "o-", color=INK, lw=2)
ax.fill_between(
    frequency_sds,
    np.maximum(0, mean_width - sd_width),
    np.minimum(1, mean_width + sd_width),
    color=BLUE,
    alpha=0.25,
    label="Mean ± one SD",
)
ax.set(
    xlabel=r"Natural-frequency standard deviation, $\sigma_\omega$",
    ylabel=r"Long-time coherence, $r_\infty$",
    ylim=(-0.03, 1.03),
    title=rf"Fixed coupling $K={fixed_coupling}$",
)
ax.grid(alpha=0.2)
ax.legend(frameon=False)
fig.tight_layout()
plt.show()
''',
    )
    insert_after(cells, "ensemble-code", width_intro)
    insert_after(cells, "heterogeneity-width-sweep-intro", width_code)

    comparison_intro = next(cell for cell in cells if cell.get("id") == "heterogeneity-comparison-intro")
    text = source(comparison_intro)
    text = text.replace(
        "# Compare populations, not only coupling values",
        "## Change the shape of the distribution",
    )
    text = text.replace(
        "The standard deviation $\\sigma_\\omega$ controls the spread of a unimodal frequency distribution. A bimodal population is different in kind, not merely broader: it contains two frequency groups. The experiment below holds the coupling rule, timestep, seeds, and observation window fixed while changing the population distribution and finite population size.\n\n> **Up the ladder over populations:** compare how a distribution-level assumption changes the collective response.",
        "Width is not the only form of heterogeneity. A bimodal population is different in kind, not merely broader: it contains two frequency groups. Compare it with narrow and broad unimodal populations while keeping the coupling rule, time step, seeds and observation window fixed.",
    )
    set_source(comparison_intro, text)

    WORKSHOP.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    simulate_width_sweep()
    update_lecture()
    update_workshop()
    print(IMAGES / "kuramoto_heterogeneity_width_sweep.svg")
    print(LECTURE)
    print(WORKSHOP)
