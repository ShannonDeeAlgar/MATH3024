#!/usr/bin/env python3
"""Build the static teaching panels used in the Week 1 slide narrative."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap, ListedColormap


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week01/images"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#1B2A4C"
SOFT = "#5A6685"
YELLOW = "#EDCC55"
BLUE = "#5879AA"
GRID = "#C7CEDC"
CMAP = ListedColormap(["white", YELLOW, BLUE])


def neighbourhood(grid, i, j):
    rows, cols = grid.shape
    return grid[max(0, i - 1):min(rows, i + 2), max(0, j - 1):min(cols, j + 2)]


def similarity_ratios(grid):
    values = []
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 0:
                continue
            local = neighbourhood(grid, i, j)
            occupied = np.count_nonzero(local) - 1
            if occupied:
                similar = np.count_nonzero(local == grid[i, j]) - 1
                values.append(similar / occupied)
    return np.asarray(values)


def local_similarity_grid(grid):
    """Return each occupied agent's local similarity ratio in its grid cell."""
    ratios = np.full(grid.shape, np.nan, dtype=float)
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 0:
                continue
            local = neighbourhood(grid, i, j)
            occupied = np.count_nonzero(local) - 1
            similar = np.count_nonzero(local == grid[i, j]) - 1
            # An isolated agent has no evidence of a similar neighbour.
            ratios[i, j] = similar / occupied if occupied else 0.0
    return ratios


def msr(grid):
    values = similarity_ratios(grid)
    return float(values.mean()) if len(values) else 0.0


def dissatisfied(grid, threshold=0.5):
    out = []
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 0:
                continue
            local = neighbourhood(grid, i, j)
            occupied = np.count_nonzero(local) - 1
            ratio = (np.count_nonzero(local == grid[i, j]) - 1) / occupied if occupied else 0
            if ratio < threshold:
                out.append((i, j))
    return out


def simulate(grid, seed=1, threshold=0.5, max_iterations=200):
    rng = np.random.default_rng(seed)
    grid = grid.copy()
    msr_history = [msr(grid)]
    dissatisfied_history = [len(dissatisfied(grid, threshold))]
    frames = [grid.copy()]
    for _ in range(max_iterations):
        unhappy = dissatisfied(grid, threshold)
        if not unhappy:
            break
        i, j = unhappy[rng.integers(len(unhappy))]
        empty = np.argwhere(grid == 0)
        if not len(empty):
            break
        m, n = empty[rng.integers(len(empty))]
        grid[m, n], grid[i, j] = grid[i, j], 0
        frames.append(grid.copy())
        msr_history.append(msr(grid))
        dissatisfied_history.append(len(dissatisfied(grid, threshold)))
    return grid, np.asarray(msr_history), np.asarray(dissatisfied_history), frames


def draw_grid(ax, grid, title=None, mark_dissatisfied=False):
    ax.imshow(grid, cmap=CMAP, vmin=0, vmax=2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1), minor=True)
    ax.grid(which="minor", color=GRID, linewidth=0.35)
    ax.tick_params(which="minor", bottom=False, left=False)
    if title:
        ax.set_title(title, color=INK, fontsize=15, pad=10)
    if mark_dissatisfied:
        bad = dissatisfied(grid)
        if bad:
            rows, cols = zip(*bad)
            ax.scatter(cols, rows, marker="x", s=80, linewidths=2, color=INK)
    for spine in ax.spines.values():
        spine.set_color(GRID)
        spine.set_linewidth(0.6)


def save_local_similarity(initial, threshold=0.5):
    """Show the move from categorical agent states to a local observable."""
    ratios = local_similarity_grid(initial)
    similarity_cmap = LinearSegmentedColormap.from_list(
        "local_similarity", ["#F8F3F7", "#C58AB8", "#6E285F"]
    )
    similarity_cmap.set_bad("white")

    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.2), dpi=180)
    draw_grid(axes[0], initial, "Agent state")
    image = axes[1].imshow(ratios, cmap=similarity_cmap, vmin=0, vmax=1)
    axes[1].set_title(r"Local similarity $r_i=n_{s,i}/n_i$", color=INK, fontsize=15, pad=10)
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    axes[1].set_xticks(np.arange(-0.5, initial.shape[1], 1), minor=True)
    axes[1].set_yticks(np.arange(-0.5, initial.shape[0], 1), minor=True)
    axes[1].grid(which="minor", color=GRID, linewidth=0.35)
    axes[1].tick_params(which="minor", bottom=False, left=False)

    for i, j in np.argwhere(initial != 0):
        value = ratios[i, j]
        text_colour = "white" if value >= 0.62 else INK
        axes[1].text(j, i, f"{value:.2f}", ha="center", va="center",
                     color=text_colour, fontsize=9.5, fontweight="semibold")
        if value < threshold:
            axes[1].scatter(j + 0.29, i - 0.29, marker="x", s=48, linewidths=1.7,
                            color="#111111", zorder=4)

    for spine in axes[1].spines.values():
        spine.set_color(GRID)
        spine.set_linewidth(0.6)
    colourbar = fig.colorbar(image, ax=axes[1], fraction=0.046, pad=0.04)
    colourbar.set_label("local similarity", color=INK)
    colourbar.set_ticks([0, 0.5, 1])
    fig.text(0.73, 0.015, r"×  dissatisfied when $r_i<0.5$",
             ha="center", color=INK, fontsize=11)
    fig.tight_layout(rect=[0, 0.055, 1, 1], w_pad=2.0)
    fig.savefig(OUT / "schelling_local_similarity.png", facecolor="white",
                bbox_inches="tight")
    plt.close(fig)


def save_animation(frames, threshold=0.5):
    """Create the teaching animation with only grid state and dissatisfied crosses."""
    images = []
    for step, grid in enumerate(frames):
        fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=100)
        draw_grid(ax, grid, mark_dissatisfied=True)
        ax.set_title(f"Simulation time step {step}", color=INK, fontsize=15, pad=9)
        fig.tight_layout()
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba()).copy()
        images.append(Image.fromarray(rgba).convert("RGB"))
        plt.close(fig)
    images[0].save(
        ROOT / "notebooks/week01/simulation2.gif",
        save_all=True,
        append_images=images[1:],
        duration=650,
        loop=0,
        optimize=True,
    )


def save_frustrated_run():
    """Show a second seed that remains unsettled with the same threshold."""
    rng = np.random.default_rng(2)
    initial = rng.choice([0, 1, 2], (5, 5), p=[0.15, 0.425, 0.425])
    _, history, bad_history, _ = simulate(initial, seed=2, threshold=0.5, max_iterations=100)
    x = np.arange(len(history))
    fig, ax = plt.subplots(figsize=(8.2, 4.25), dpi=180)
    points = ax.scatter(x, history, c=bad_history, cmap="magma_r", s=24, zorder=3)
    ax.plot(x, history, color=INK, lw=1.45, alpha=0.72)
    ax.set(xlabel="Simulation time step", ylabel="Mean similarity ratio", ylim=(0, 1.02))
    ax.axhline(0.5, color=SOFT, ls="--", lw=1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=GRID, alpha=0.45, lw=0.7)
    cbar = fig.colorbar(points, ax=ax, pad=0.02)
    cbar.set_label("Dissatisfied individuals")
    ax.set_title("A different seed: movement continues without settling", color=INK)
    fig.tight_layout()
    fig.savefig(OUT / "schelling_frustrated_time_series.png", facecolor="white", bbox_inches="tight")
    plt.close(fig)
    return history, bad_history


def example_grids():
    a = np.array([
        [2, 2, 2, 2, 2, 2], [2, 1, 1, 1, 1, 2], [2, 1, 1, 1, 1, 2],
        [2, 1, 1, 1, 1, 2], [2, 1, 1, 1, 1, 2], [2, 2, 2, 2, 2, 2],
    ])
    b = np.indices((6, 6)).sum(axis=0) % 2 + 1
    c = np.array([[1] * 6, [2] * 6, [2] * 6, [2] * 6, [2] * 6, [1] * 6])
    d = np.array([[1, 1, 1, 2, 2, 2]] * 6)
    e = np.array([
        [1, 1, 1, 2, 1, 1], [1, 2, 2, 2, 2, 1], [2, 2, 1, 1, 2, 2],
        [1, 2, 1, 2, 1, 2], [2, 2, 2, 2, 1, 1], [1, 1, 1, 2, 2, 1],
    ])
    return [a, b, c, d, e]


def save_initialisation(initial):
    fig, ax = plt.subplots(figsize=(5.4, 4.4), dpi=180)
    draw_grid(ax, initial, "A reproducible initial state")
    handles = [mpatches.Patch(color="white", ec=INK, label="Empty"),
               mpatches.Patch(color=YELLOW, label="Group 1"),
               mpatches.Patch(color=BLUE, label="Group 2")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.05),
              ncol=3, frameon=False, fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "schelling_initialisation.png", transparent=False, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_qualitative(initial, final):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.4), dpi=180)
    draw_grid(axes[0], initial, f"Initial\n{len(dissatisfied(initial))} dissatisfied", True)
    draw_grid(axes[1], final, f"Final\n{len(dissatisfied(final))} dissatisfied", True)
    fig.tight_layout(w_pad=2)
    fig.savefig(OUT / "schelling_initial_final.png", facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_comparison(grids, reveal=False):
    fig, axes = plt.subplots(1, 5, figsize=(13, 2.9), dpi=180)
    values = [msr(g) for g in grids]
    labels = "ABCDE"
    for label, ax, grid, value in zip(labels, axes, grids, values):
        title = f"{label}\nMSR {value:.3f}" if reveal else label
        draw_grid(ax, grid, title)
    fig.tight_layout(w_pad=1)
    name = "schelling_five_grids_values.png" if reveal else "schelling_five_grids_prompt.png"
    fig.savefig(OUT / name, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_time_series(msr_history, dissatisfied_history):
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.3), dpi=180, sharex=True)
    x = np.arange(len(msr_history))
    axes[0].plot(x, dissatisfied_history, color=INK, lw=2)
    axes[0].fill_between(x, 0, dissatisfied_history, color=INK, alpha=0.08)
    axes[0].set_ylabel("Dissatisfied\nagents", color=INK)
    axes[0].set_ylim(bottom=0)
    axes[1].plot(x, msr_history, color=INK, lw=2)
    axes[1].axhline(0.5, color=SOFT, lw=1, ls="--", label="random 50:50 benchmark")
    axes[1].axhline(1.0, color=SOFT, lw=1, ls=":", label="raw upper bound")
    axes[1].set_ylabel("MSR", color=INK)
    axes[1].set_xlabel("Simulation time step", color=INK)
    axes[1].set_ylim(0, 1.03)
    axes[1].legend(frameon=False, fontsize=9, loc="lower right")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(colors=SOFT)
        ax.grid(axis="y", color="#C7CEDC", alpha=0.45, lw=0.7)
    fig.tight_layout(h_pad=0.6)
    fig.savefig(OUT / "schelling_time_series.png", facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_single_run_msr(msr_history, dissatisfied_history):
    x = np.arange(len(msr_history))
    fig, ax = plt.subplots(figsize=(8.2, 4.2), dpi=180)
    points = ax.scatter(x, msr_history, c=dissatisfied_history, cmap="magma_r", s=28, zorder=3)
    ax.plot(x, msr_history, color=INK, lw=1.6, alpha=0.7)
    ax.set(xlabel="Simulation time step", ylabel="Mean similarity ratio", ylim=(0, 1.02))
    ax.axhline(0.5, color=SOFT, ls="--", lw=1)
    cbar = fig.colorbar(points, ax=ax, pad=0.02)
    cbar.set_label("Dissatisfied individuals")
    ax.set_title("One run: the aggregate rises, but the agents are not yet settled", color=INK)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "schelling_single_run_msr.png", facecolor="white", bbox_inches="tight")
    plt.close(fig)


def parameter_study():
    thresholds = np.arange(0.2, 0.81, 0.1)
    seeds = range(5)
    final_msr, final_bad, moves, trajectories = {}, {}, {}, {}
    examples = {}
    for threshold in thresholds:
        final_msr[threshold], final_bad[threshold], moves[threshold], trajectories[threshold] = [], [], [], []
        for seed in seeds:
            rng = np.random.default_rng(seed)
            initial = rng.choice([0, 1, 2], (5, 5), p=[0.15, 0.425, 0.425])
            final, history, bad_history, frames = simulate(
                initial, seed=seed + 1000, threshold=float(threshold), max_iterations=100
            )
            final_msr[threshold].append(history[-1])
            occupied = max(1, np.count_nonzero(final))
            final_bad[threshold].append(bad_history[-1] / occupied)
            moves[threshold].append(len(history) - 1)
            trajectories[threshold].append(history)
            rounded = round(float(threshold), 1)
            if seed == 1 and rounded in (0.2, 0.5, 0.8):
                examples[rounded] = final
    return thresholds, final_msr, final_bad, moves, examples, trajectories


def save_ensemble_trajectories(thresholds, trajectories):
    fig, ax = plt.subplots(figsize=(8.4, 4.6), dpi=180)
    colours = plt.colormaps["viridis"](np.linspace(0.08, 0.92, len(thresholds)))
    budget = 101
    for threshold, colour in zip(thresholds, colours):
        padded = np.vstack([
            np.pad(run, (0, budget - len(run)), mode="edge")[:budget]
            for run in trajectories[threshold]
        ])
        mean = padded.mean(axis=0)
        low, high = np.quantile(padded, [0.25, 0.75], axis=0)
        x = np.arange(budget)
        ax.plot(x, mean, color=colour, lw=2, label=f"{threshold:.0%}")
        ax.fill_between(x, low, high, color=colour, alpha=0.13)
    ax.set(xlabel="Simulation time step", ylabel="Mean similarity ratio", ylim=(0.25, 1.02))
    ax.legend(title="Threshold", ncol=2, frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Ensemble parameter sweep: mean trajectory and middle 50%", color=INK)
    fig.tight_layout()
    fig.savefig(OUT / "schelling_ensemble_trajectories.png", facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_parameter_trajectories(thresholds, trajectories):
    """Show one representative trajectory per parameter before aggregating runs."""
    fig, ax = plt.subplots(figsize=(8.4, 4.6), dpi=180)
    colours = plt.colormaps["viridis"](np.linspace(0.08, 0.92, len(thresholds)))
    for threshold, colour in zip(thresholds, colours):
        run = trajectories[threshold][0]
        ax.plot(np.arange(len(run)), run, color=colour, lw=2,
                label=f"{threshold:.0%}")
    ax.set(xlabel="Simulation time step", ylabel="Mean similarity ratio",
           ylim=(0.25, 1.02))
    ax.legend(title="Threshold", ncol=2, frameon=False, fontsize=9)
    ax.grid(axis="y", color=GRID, alpha=0.45, lw=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Parameter sweep: one run per threshold", color=INK)
    fig.tight_layout()
    fig.savefig(OUT / "schelling_parameter_trajectories.png", facecolor="white",
                bbox_inches="tight")
    plt.close(fig)


def save_parameter_summary(thresholds, final_msr, final_bad, moves):
    x = thresholds * 100
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 7.2), dpi=180, sharex=True)
    for ax, data, ylabel in [
        (axes[0], final_msr, "Final MSR"),
        (axes[1], final_bad, "Dissatisfied fraction after 100 steps"),
    ]:
        means = np.array([np.mean(data[t]) for t in thresholds])
        q25 = np.array([np.quantile(data[t], 0.25) for t in thresholds])
        q75 = np.array([np.quantile(data[t], 0.75) for t in thresholds])
        ax.plot(x, means, marker="o", color=INK, lw=2)
        ax.fill_between(x, q25, q75, color=BLUE, alpha=0.22, label="middle 50% of runs")
        ax.set(ylabel=ylabel)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylim(0, 1.02)
    axes[1].set_ylim(0, 1.02)
    axes[1].set_xlabel("Similarity threshold (%)")
    axes[1].legend(frameon=False, fontsize=9)
    fig.suptitle("Five independent runs per threshold", color=INK, fontsize=16)
    fig.tight_layout(h_pad=0.8)
    fig.savefig(OUT / "schelling_parameter_ensemble.png", facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_time_summaries(thresholds, trajectories, moves):
    """Summarise when peak segregation occurs and when movement stops."""
    x = thresholds * 100
    time_to_peak = {
        threshold: [int(np.argmax(run)) for run in trajectories[threshold]]
        for threshold in thresholds
    }
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 7.2), dpi=180, sharex=True)
    for ax, data, ylabel in [
        (axes[0], time_to_peak, "Step of maximum MSR"),
        (axes[1], moves, "Steps until stop or budget"),
    ]:
        medians = np.array([np.median(data[t]) for t in thresholds])
        q25 = np.array([np.quantile(data[t], 0.25) for t in thresholds])
        q75 = np.array([np.quantile(data[t], 0.75) for t in thresholds])
        ax.plot(x, medians, marker="o", color=INK, lw=2)
        ax.fill_between(x, q25, q75, color=BLUE, alpha=0.22,
                        label="middle 50% of runs")
        ax.set_ylabel(ylabel)
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", color=GRID, alpha=0.45, lw=0.7)
        ax.spines[["top", "right"]].set_visible(False)
    axes[1].axhline(100, color=SOFT, ls="--", lw=1, label="100-step budget")
    axes[1].set_xlabel("Similarity threshold (%)")
    axes[1].legend(frameon=False, fontsize=9)
    fig.suptitle("Event times across five independent runs", color=INK, fontsize=16)
    fig.tight_layout(h_pad=0.8)
    fig.savefig(OUT / "schelling_time_summaries.png", facecolor="white",
                bbox_inches="tight")
    plt.close(fig)


def save_parameter_examples(examples):
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5), dpi=180)
    for ax, threshold in zip(axes, [0.2, 0.5, 0.8]):
        grid = examples[threshold]
        bad = len(dissatisfied(grid, threshold))
        draw_grid(ax, grid, f"Threshold {threshold:.0%}\nMSR {msr(grid):.2f} · {bad} dissatisfied")
    fig.tight_layout(w_pad=1.5)
    fig.savefig(OUT / "schelling_parameter_examples.png", facecolor="white", bbox_inches="tight")
    plt.close(fig)


def main():
    rng = np.random.default_rng(1)
    initial = rng.choice([0, 1, 2], size=(5, 5), p=[0.15, 0.425, 0.425])
    final, msr_history, dissatisfied_history, frames = simulate(initial, seed=1)
    grids = example_grids()
    save_initialisation(initial)
    save_local_similarity(initial)
    save_qualitative(initial, final)
    save_comparison(grids, reveal=False)
    save_comparison(grids, reveal=True)
    save_time_series(msr_history, dissatisfied_history)
    save_single_run_msr(msr_history, dissatisfied_history)
    save_animation(frames)
    frustrated_msr, frustrated_bad = save_frustrated_run()
    thresholds, final_msr, final_bad, moves, examples, trajectories = parameter_study()
    save_parameter_trajectories(thresholds, trajectories)
    save_ensemble_trajectories(thresholds, trajectories)
    save_parameter_summary(thresholds, final_msr, final_bad, moves)
    save_time_summaries(thresholds, trajectories, moves)
    save_parameter_examples(examples)
    print("MSR values:", ", ".join(f"{v:.6f}" for v in map(msr, grids)))
    print(f"Simulation: {len(msr_history)-1} moves, MSR {msr_history[0]:.3f} → {msr_history[-1]:.3f}")
    print(f"Frustrated run: {len(frustrated_msr)-1} moves, {frustrated_bad[-1]} still dissatisfied")


if __name__ == "__main__":
    main()
