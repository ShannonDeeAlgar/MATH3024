"""Add concise ensemble-reporting guidance and preserve a drifting oscillator."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from figure_style import BLUE, INK, LIGHT_BLUE, ORANGE, apply_course_figure_style, finish_axes


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
WORKSHOP = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"
IMAGES = ROOT / "notebooks/week06/images"


def generate_summary_comparison() -> None:
    data = np.load(IMAGES / "kuramoto_heterogeneity_width_sweep_data.npz")
    sigmas = data["sigmas"]
    values = data["values"]
    mean = values.mean(axis=1)
    sd = values.std(axis=1, ddof=1)
    median = np.median(values, axis=1)
    q1, q3 = np.quantile(values, [0.25, 0.75], axis=1)

    apply_course_figure_style()
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.2), sharex=True, sharey=True,
                             constrained_layout=True)
    runs_per_condition = values.shape[1]
    fig.suptitle(
        f"{runs_per_condition} simulations at each frequency spread",
        fontsize=14,
        color=INK,
    )
    for ax in axes:
        for run in values.T:
            ax.plot(sigmas, run, color=LIGHT_BLUE, alpha=0.28, lw=0.9)
        ax.set(xlabel=r"Frequency spread, $\sigma_\omega$", ylim=(-0.03, 1.03))
        finish_axes(ax)

    axes[0].plot(sigmas, mean, "o-", color=INK, lw=2.2, ms=4.5,
                 label="mean")
    axes[0].fill_between(sigmas, np.maximum(0, mean - sd), np.minimum(1, mean + sd),
                         color=BLUE, alpha=0.18, label="±1 SD")
    axes[0].set(title="Mean and standard deviation",
                ylabel=r"Long-time coherence, $r_\infty$")

    axes[1].plot(sigmas, median, "o-", color=ORANGE, lw=2.2, ms=4.5,
                 label="median")
    axes[1].fill_between(sigmas, q1, q3, color=ORANGE, alpha=0.18,
                         label="middle 50%")
    axes[1].set(title="Median and quartiles")

    for ax in axes:
        ax.legend(frameon=False, loc="lower left", ncol=2,
                  handlelength=1.8, columnspacing=1.0)

    fig.savefig(IMAGES / "kuramoto_ensemble_summary_choices.svg", transparent=True)
    plt.close(fig)


def lines(text: str) -> list[str]:
    return [line + "\n" for line in text.rstrip().splitlines()]


def markdown(cell_id: str, source: str, tags: list[str] | None = None) -> dict:
    metadata: dict = {}
    if tags:
        metadata["tags"] = tags
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": metadata,
        "source": lines(source),
    }


def load(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def save(path: Path, notebook: dict) -> None:
    with path.open("w") as handle:
        json.dump(notebook, handle, indent=1, ensure_ascii=False)
        handle.write("\n")


def find(cells: list[dict], cell_id: str) -> int:
    return next(i for i, cell in enumerate(cells) if cell.get("id") == cell_id)


lecture = load(LECTURE)
cells = lecture["cells"]
cells[:] = [
    cell
    for cell in cells
    if cell.get("id") not in {
        "w6-ensemble-reporting-slide",
        "w6-ensemble-reporting-reader",
    }
]

slide = markdown(
    "w6-ensemble-reporting-slide",
    r'''## Show the centre and the spread

<img src="images/kuramoto_ensemble_summary_choices.svg" alt="The same Kuramoto ensemble summarised by a mean and standard deviation or by a median and quartiles" style="display:block;max-height:480px;max-width:100%;margin:0 auto">

The individual runs are identical in both panels. The summaries differ most near the transition, where the outcomes are least symmetric.''',
    ["slides-only"],
)
cells.insert(find(cells, "w6-sweep") + 1, slide)

reader = markdown(
    "w6-ensemble-reporting-reader",
    r'''### Report an ensemble

An ensemble needs both a central summary and an indication of run-to-run variation. The best choice depends on the shape of the outcomes and on the claim being made.

- **Mean and standard deviation:** useful for a roughly symmetric, single-cluster distribution when unusually large or small runs are not dominating the result.
- **Median and quartiles:** useful for skewed, bounded or outlier-prone results. The middle 50% band used in the Workshop is the interval from the first to the third quartile.
- **A wider quantile interval:** for example, the 10th to 90th percentiles, when the tails matter but the minimum and maximum would be too sensitive to one run.
- **Minimum and maximum:** useful when the full observed range is itself important, but unstable as estimates of a population range and rarely sufficient on their own.

There is no universal preferred pair. A line with a band, points with error bars, a box plot or the individual run values may all be defensible. The caption must state the number of runs, the central summary and the meaning of the interval. Showing the individual runs faintly is especially helpful for small ensembles, multimodal outcomes or possible failures.

<img src="images/kuramoto_ensemble_summary_choices.svg" alt="The same Kuramoto ensemble summarised by a mean and standard deviation or by a median and quartiles" style="display:block;width:88%;max-width:980px;margin:1rem auto">

These are the same simulated populations. Away from the transition the two summaries are much of a muchness. Near the transition, where different runs can give noticeably different outcomes, retaining the faint individual curves shows what either band compresses.

For a project, “average with a range” is a reasonable minimum expectation, provided that both words are defined. A mean with an interquartile range is mathematically possible but mixes summaries with different interpretations; use it only for a stated reason. A mean with standard deviation or a median with quartiles will usually be easier to justify.''',
    ["reader-only"],
)
cells.insert(find(cells, "parameter-sweep") + 1, reader)

for cell in cells:
    if cell.get("id") == "w6-frequency-heterogeneity-slide":
        cell["source"] = lines(r'''## Natural and realised frequencies

<img src="images/kuramoto_realised_frequency.svg" alt="Natural frequency against long-time realised frequency for a Kuramoto population" style="display:block;max-height:500px;max-width:100%;margin:0 auto">

Most oscillators share a common realised rate. The tail oscillator that remains off the horizontal band continues to drift through the locked group. The number or fraction of drifters is another possible population-level summary.''')
    elif cell.get("id") == "w6-realised-frequency-analysis-reader":
        cell["source"] = lines(r'''### Natural and realised frequencies

<img src="images/kuramoto_realised_frequency.svg" alt="Natural frequency against long-time realised frequency for a Kuramoto population" style="display:block;width:72%;max-width:800px;margin:1rem auto">

The horizontal band contains **frequency-locked** oscillators: their natural frequencies differ, but coupling gives them the same long-time realised rate. The tail point away from that band is a **drifting** oscillator. Its phase continues to slip relative to the locked group.

This suggests another response variable for a sweep: count the drifting oscillators, or report their fraction of the population, at each $K$. Coherence $r_\infty$ records concentration around the phase circle; the drifting fraction asks directly how much of the population has joined the locked group. The two summaries answer related but different questions.''')

save(LECTURE, lecture)

workshop = load(WORKSHOP)
cells = workshop["cells"]
cells[:] = [cell for cell in cells if cell.get("id") != "ensemble-reporting-note"]
note = markdown(
    "ensemble-reporting-note",
    r'''The plot below uses a mean line and a middle-50% band. That is one defensible choice, not a fixed recipe.

- Use mean and standard deviation for roughly symmetric outcomes.
- Use median and quartiles for skewed or outlier-prone outcomes.
- Use a wider quantile interval or the full range when tail behaviour is central to the question.

Whatever you choose, state the number of runs and define the band or error bars. For a small ensemble, keep the individual values visible as well.''',
)
cells.insert(find(cells, "ensemble-intro") + 1, note)
save(WORKSHOP, workshop)
generate_summary_comparison()
