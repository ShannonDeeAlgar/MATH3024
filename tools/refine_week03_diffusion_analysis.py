from pathlib import Path

import matplotlib.pyplot as plt
import nbformat
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
IMAGES = ROOT / "notebooks/week03/images"
NAVY = "#1b2a4c"
YELLOW = "#f1d255"
BLUE = "#5f80b2"
GRID = "#d8dfeb"


def configure_plot_style():
    """Apply the lecture-deck typography to generated analysis figures."""
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 13,
        "axes.titlesize": 17,
        "axes.titleweight": "semibold",
        "axes.labelsize": 14,
        "legend.fontsize": 12,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "text.color": NAVY,
        "axes.labelcolor": NAVY,
        "axes.titlecolor": NAVY,
        "axes.edgecolor": NAVY,
        "xtick.color": NAVY,
        "ytick.color": NAVY,
    })


def style_axis(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=GRID, linewidth=0.8, alpha=0.75)
    ax.set_axisbelow(True)


def simulate(seed, diffusion, walkers, steps):
    rng = np.random.default_rng(seed)
    increments = rng.normal(
        scale=np.sqrt(2 * diffusion), size=(walkers, steps, 2)
    )
    positions = np.concatenate(
        [np.zeros((walkers, 1, 2)), np.cumsum(increments, axis=1)], axis=1
    )
    return np.sum(positions**2, axis=2)


def make_walk_ensemble_figure():
    diffusion, steps = 0.25, 240
    squared_radius = simulate(3024, diffusion, 500, steps)
    time = np.arange(steps + 1)
    mean_msd = squared_radius.mean(axis=0)

    fig, ax = plt.subplots(figsize=(8.8, 4.7), constrained_layout=True)
    for path in squared_radius[:40]:
        ax.plot(time, path, color=BLUE, alpha=0.12, linewidth=0.9)
    ax.plot(time, mean_msd, color=NAVY, linewidth=2.6,
            label=f"mean of {squared_radius.shape[0]} walkers")
    ax.plot(time, 4 * diffusion * time, color=YELLOW, linewidth=3,
            linestyle="--", label=r"theory: $4Dt$")
    ax.set(xlabel="Simulation time step", ylabel=r"Squared displacement, $R^2(t)$")
    ax.set_ylim(bottom=0)
    style_axis(ax)
    ax.legend(frameon=False, ncols=2)
    fig.savefig(IMAGES / "brownian_ensemble_msd.svg", transparent=True)
    plt.close(fig)


def make_distance_figure():
    steps = 900
    time = np.arange(steps + 1)
    cases = [(0.10, "slower", "#c65b17"), (0.35, "faster", "#2878a8")]
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4), constrained_layout=True)
    for index, (diffusion, label, colour) in enumerate(cases):
        rng = np.random.default_rng(1200 + index)
        increments = rng.normal(scale=np.sqrt(2 * diffusion), size=(steps, 2))
        path = np.vstack([np.zeros(2), np.cumsum(increments, axis=0)])
        radius = np.linalg.norm(path, axis=1)
        axes[0].plot(path[:, 0], path[:, 1], color=colour, linewidth=1.1,
                     alpha=0.85, label=label)
        axes[1].plot(time, radius, color=colour, linewidth=1.15, alpha=0.82,
                     label=f"one {label} path")
        axes[1].plot(time, np.sqrt(4 * diffusion * time), color=colour,
                     linewidth=2.1, linestyle="--",
                     label=fr"typical scale $\sqrt{{4Dt}}$, $D={diffusion:.2f}$")
    axes[0].scatter([0], [0], s=55, color=YELLOW, edgecolor=NAVY, zorder=5)
    axes[0].annotate(
        "shared start",
        xy=(0, 0),
        xytext=(8, -15),
        textcoords="offset points",
        fontsize=9,
        color=NAVY,
    )
    axes[0].set(xlabel="$x$", ylabel="$y$", aspect="equal")
    axes[1].set(xlabel="Simulation time step", ylabel=r"Distance from origin, $R(t)$")
    axes[1].set_ylim(bottom=0)
    for ax in axes:
        style_axis(ax)
        ax.legend(frameon=False, fontsize=8)
    fig.savefig(IMAGES / "brownian_distance_sqrt.svg", transparent=True)
    plt.close(fig)


def make_diffusion_sweep_figures():
    rates = np.array([0.05, 0.10, 0.20, 0.25, 0.35, 0.50])
    steps, batches, walkers_per_batch = 220, 14, 180
    time = np.arange(steps + 1)
    # A single perceptually ordered map makes increasing D easy to trace:
    # dark purple is slow diffusion and yellow is fast diffusion.
    colours = plt.colormaps["viridis"](np.linspace(0.08, 0.92, len(rates)))
    slopes, slope_spread = [], []

    fig, ax = plt.subplots(figsize=(8.8, 4.7), constrained_layout=True)
    for index, (diffusion, colour) in enumerate(zip(rates, colours)):
        batch_curves = []
        batch_slopes = []
        for batch in range(batches):
            r2 = simulate(7300 + 100 * index + batch, diffusion,
                          walkers_per_batch, steps)
            curve = r2.mean(axis=0)
            batch_curves.append(curve)
            batch_slopes.append(np.polyfit(time[20:], curve[20:], 1)[0])
        batch_curves = np.asarray(batch_curves)
        centre = batch_curves.mean(axis=0)
        lower, upper = np.quantile(batch_curves, [0.25, 0.75], axis=0)
        ax.fill_between(time, lower, upper, color=colour, alpha=0.16)
        ax.plot(time, centre, color=colour, linewidth=2.2, label=fr"$D={diffusion:.2f}$")
        slopes.append(np.mean(batch_slopes))
        slope_spread.append(np.std(batch_slopes, ddof=1))
    ax.set(xlabel="Simulation time step", ylabel="Ensemble mean-square displacement")
    ax.set_ylim(bottom=0)
    style_axis(ax)
    # Keep the parameter values in ascending order, left to right.
    ax.legend(frameon=False, ncols=len(rates), loc="upper left",
              columnspacing=0.9, handlelength=1.4)
    fig.savefig(IMAGES / "brownian_diffusion_sweep.svg", transparent=True)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.5), constrained_layout=True)
    ax.errorbar(
        rates,
        slopes,
        yerr=slope_spread,
        fmt="o",
        color=NAVY,
        ecolor=BLUE,
        capsize=4,
        markersize=7,
        label="_nolegend_",
    )
    guide = np.linspace(0, 0.54, 100)
    ax.plot(guide, 4 * guide, color=YELLOW, linewidth=3, linestyle="--",
            label=r"theory: slope $=4D$")
    d_reference = 0.25
    reference_index = int(np.flatnonzero(np.isclose(rates, d_reference))[0])
    ax.scatter(
        [d_reference], [slopes[reference_index]], s=105, facecolor="white",
        edgecolor=NAVY, linewidth=2, zorder=5,
    )
    ax.annotate(
        r"$D=0.25$", (d_reference, slopes[reference_index]),
        xytext=(10, -18), textcoords="offset points", color=NAVY, fontsize=11,
    )
    ax.set(xlabel=r"Diffusion coefficient, $D$", ylabel="Fitted MSD slope")
    ax.set(xlim=(0, 0.54), ylim=(0, 2.25))
    style_axis(ax)
    ax.legend(frameon=False)
    fig.savefig(IMAGES / "brownian_slope_vs_D.svg", transparent=True)
    plt.close(fig)


def markdown_cell(source, slide_type="subslide", tags=None):
    cell = nbformat.v4.new_markdown_cell(source)
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    cell.metadata["tags"] = tags or ["slides"]
    return cell


def update_notebook():
    nb = nbformat.read(NOTEBOOK, as_version=4)

    # Replace the formatted paraphrase with the original excerpt image.
    for cell in nb.cells:
        if "His description of modelling is also unusually direct:" in cell.source:
            before = cell.source.split("His description of modelling is also unusually direct:")[0]
            cell.source = before + (
                "His description of modelling is also unusually direct:\n\n"
                '<img src="images/Turing_1952_quote.png" alt="Opening paragraph of Turing’s '
                '1952 paper describing a model as a simplification and idealisation" '
                'style="display:block;width:72%;max-width:780px;margin:0.8rem auto;">\n\n'
                "*Opening paragraph of Turing (1952).*"
            )

    # Keep the reproducible analysis code in the Reader, but display curated figures in the flow.
    for cell in nb.cells:
        if cell.cell_type == "code" and "n_walkers, n_steps = 2000, 500" in cell.source:
            cell.metadata["tags"] = ["archive-only", "hide-input"]
            cell.metadata["slideshow"] = {"slide_type": ""}
            cell.outputs = []
            cell.execution_count = None
        if cell.cell_type == "code" and 'diffusion_rates = {"slower"' in cell.source:
            cell.metadata["tags"] = ["archive-only", "hide-input"]
            cell.metadata["slideshow"] = {"slide_type": ""}
            cell.outputs = []
            cell.execution_count = None

    # Remove the obsolete black-grid output and leave the numerical code collapsed.
    for cell in nb.cells:
        if cell.cell_type == "code" and "def diffuse_periodic" in cell.source:
            first_plot = cell.source.index("fig, axes = plt.subplots")
            try:
                second_plot = cell.source.index("fig, axes = plt.subplots", first_plot + 1)
            except ValueError:
                second_plot = None
            if second_plot is not None:
                cell.source = cell.source[:first_plot] + cell.source[second_plot:]
            cell.metadata["tags"] = ["archive-only", "hide-input"]
            cell.outputs = []
            cell.execution_count = None

    # Split the accessibility story into question/story first, guidance second.
    for cell in nb.cells:
        if cell.cell_type == "markdown" and cell.source.startswith("### Colour is part"):
            cell.source = '''### Can everyone see the same information?
<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/Colourblind.png" alt="A pseudo-Ishihara colour-vision image" style="display:block;width:72%;max-height:390px;object-fit:contain;margin:0 auto;">
</div>
<div class="text-panel">
<p>I did my PhD, and continue to work, with someone who is red-green colour blind. He cannot see the number inside this circle.</p>
<p>While I am marking your projects I can see a full rainbow. Your figures should not require every reader to see colour in the same way.</p>
</div>
</div>'''
        if cell.cell_type == "markdown" and cell.source.startswith("## Colour must not"):
            cell.source = '''## Can everyone see the same information?

<img src="images/Colourblind.png" alt="A pseudo-Ishihara colour-vision image" style="display:block;width:44%;max-width:500px;margin:0 auto;">

I did my PhD, and continue to work, with someone who is red-green colour blind. He cannot see the number inside this circle. While I am marking your projects I can see a full rainbow. Your figures should not require every reader to see colour in the same way.

### Design colour deliberately

Colour is part of the representation, not decoration.

- Use a perceptually ordered sequential map for concentration. Matplotlib provides accessible defaults including `viridis`, `cividis` and `plasma`.
- Avoid rainbow scales and red-green contrasts.
- Check that ordering remains legible in greyscale and for common colour-vision deficiencies.

See [Matplotlib: Choosing Colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html), [Nature's brief guide](https://www.nature.com/articles/d41586-021-02696-z), and the [ASCB guide to accessible scientific figures](https://www.ascb.org/science-news/how-to-make-scientific-figures-accessible-to-readers-with-color-blindness/).'''

    # Insert new analytical sequence after "What would we measure?".
    for cell in nb.cells:
        if cell.cell_type == "markdown" and cell.source.startswith("### What would we measure?"):
            marker = cell.source.find("- **Mean displacement**")
            if marker != -1:
                cell.source = "### What would we measure?\n\n" + cell.source[marker:]
    insert_at = next(i for i, c in enumerate(nb.cells) if c.source.startswith("### What would we measure?")) + 1
    # Remove previous generated versions if rerun.
    nb.cells = [c for c in nb.cells if not c.source.startswith("### From one path to an ensemble")
                and not c.source.startswith("### Sweep the diffusion coefficient")
                and not c.source.startswith("### Compress each ensemble trajectory")
                and not c.source.startswith("### One path: distance from the origin")
                and "Design colour deliberately" not in c.source]
    brownian_index = next(i for i, c in enumerate(nb.cells) if c.source.startswith("### Brownian motion: the physical phenomenon")) + 1
    nb.cells[brownian_index:brownian_index] = [markdown_cell('''### One path: distance from the origin

<img src="images/brownian_distance_sqrt.svg" alt="Two Brownian trajectories and their distances from the origin compared with square-root reference curves" style="display:block;width:86%;max-height:430px;object-fit:contain;margin:0 auto;">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Stay low:</strong> one path is irregular. Its distance does not follow a smooth curve, but its typical scale grows in proportion to the square root of time.</span></div>''')]
    insert_at = next(i for i, c in enumerate(nb.cells) if c.source.startswith("### What would we measure?")) + 1
    new_cells = [
        markdown_cell('''### From one path to an ensemble

<img src="images/brownian_ensemble_msd.svg" alt="Squared displacement for individual Brownian paths, their ensemble mean and the theoretical diffusion law" style="display:block;width:82%;max-height:440px;object-fit:contain;margin:0 auto;">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over walkers and random histories:</strong> individual paths vary widely, while their mean-square displacement approaches <em>4Dt</em>.</span></div>'''),
        markdown_cell('''### Sweep the diffusion coefficient

<img src="images/brownian_diffusion_sweep.svg" alt="Ensemble mean-square displacement for five diffusion coefficients with run-to-run bands" style="display:block;width:82%;max-height:430px;object-fit:contain;margin:0 auto;">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over a parameter:</strong> compare ensembles across several values of <em>D</em> to reveal a systematic change in spreading rate.</span></div>'''),
        markdown_cell('''### Compress each ensemble trajectory

<img src="images/brownian_slope_vs_D.svg" alt="Fitted mean-square-displacement slope against diffusion coefficient" style="display:block;width:70%;max-height:420px;object-fit:contain;margin:0 auto;">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up again:</strong> replace each ensemble curve by its fitted slope. The relationship slope = <em>4D</em> is now directly testable.</span></div>'''),
    ]
    nb.cells[insert_at:insert_at] = new_cells

    # Add the practical colour guidance as its own slide after the personal story.
    colour_index = next(i for i, c in enumerate(nb.cells) if c.source.startswith("### Can everyone see")) + 1
    nb.cells[colour_index:colour_index] = [markdown_cell('''### Design colour deliberately

Colour is part of the representation, not decoration.

- Use a perceptually ordered sequential map for concentration. Matplotlib provides accessible defaults including `viridis`, `cividis` and `plasma`.
- Avoid rainbow scales and red-green contrasts.
- Check that ordering remains legible in greyscale and for common colour-vision deficiencies.

<p class="figure-ref"><a href="https://matplotlib.org/stable/users/explain/colors/colormaps.html">Matplotlib: Choosing Colormaps</a> · <a href="https://www.nature.com/articles/d41586-021-02696-z">Nature guide</a> · <a href="https://www.ascb.org/science-news/how-to-make-scientific-figures-accessible-to-readers-with-color-blindness/">ASCB guide</a></p>''')]

    nbformat.write(nb, NOTEBOOK)


if __name__ == "__main__":
    IMAGES.mkdir(parents=True, exist_ok=True)
    configure_plot_style()
    make_walk_ensemble_figure()
    make_distance_figure()
    make_diffusion_sweep_figures()
    update_notebook()
