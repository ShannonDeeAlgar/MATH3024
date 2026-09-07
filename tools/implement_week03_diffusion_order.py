from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def find_cell(nb, cell_id):
    for cell in nb.cells:
        if cell.get("id") == cell_id:
            return cell
    raise KeyError(cell_id)


def main():
    nb = nbformat.read(NOTEBOOK, as_version=4)

    random_walk = find_cell(nb, "b7c839be-6ee3-4fef-9aae-72b880dbb4b9")
    random_walk.source = random_walk.source.replace(
        "### Random walk: a discrete model",
        "# Understanding diffusion\n\n## Random walk: a discrete model",
        1,
    )
    random_walk.metadata["slideshow"] = {"slide_type": "slide"}

    random_walk_reader = find_cell(nb, "week03-random-walk-detail-reader")
    random_walk_reader.source = random_walk_reader.source.replace(
        "#### Reading the three walks", "### Reading the three walks", 1
    )

    ensemble = find_cell(nb, "bf26cf2d")
    ensemble.source = '''### From one path to an ensemble

<img src="images/brownian_ensemble_msd.svg" alt="Squared displacement for individual Brownian paths at D equals 0.25, their ensemble mean and the theoretical diffusion law" style="display:block;width:70%;max-height:330px;object-fit:contain;margin:0 auto;">

<p class="small-note"><strong>Here, <i>D</i> = 0.25.</strong> Individual squared displacements vary widely. Their average is the <strong>mean-square displacement (MSD)</strong>.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over walkers:</strong> the MSD approaches 4<i>Dt</i>.</span></div>'''

    sweep = find_cell(nb, "25b5d7f3")
    sweep.source = '''### Sweep the diffusion coefficient

<img src="images/brownian_diffusion_sweep.svg" alt="Ensemble mean-square displacement for six diffusion coefficients, including D equals 0.25, with run-to-run bands" style="display:block;width:82%;max-height:430px;object-fit:contain;margin:0 auto;">

<p class="small-note">The value from the previous slide, <i>D</i> = 0.25, is retained as one member of the sweep.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over a parameter:</strong> compare ensembles across several values of <em>D</em> to reveal a systematic change in spreading rate.</span></div>'''

    compressed = find_cell(nb, "a241f850")
    compressed.source = '''### Compress each ensemble trajectory

<img src="images/brownian_slope_vs_D.svg" alt="Fitted mean-square-displacement slope against diffusion coefficient; error bars show standard deviation across independent batches" style="display:block;width:70%;max-height:420px;object-fit:contain;margin:0 auto;">

<p class="small-note"><strong>MSD</strong> means mean-square displacement. Each point is the mean fitted MSD slope from 14 independent batches; its error bar is one standard deviation across those fitted slopes.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up again:</strong> replace each ensemble curve by its fitted slope. The relationship slope = <em>4D</em> is now directly testable.</span></div>'''

    gray_scott = find_cell(nb, "week03-gray-scott-history")
    gray_scott.source = gray_scott.source.replace(
        "# Understanding particle motion\n\n## A concrete particle story: Gray–Scott",
        "# Add reaction: the Gray–Scott model\n\n## A concrete particle story",
        1,
    )

    # Diffusion first: move the Gray–Scott reaction/background pair to immediately
    # after the final Brownian-motion abstraction slide.
    gray_reader = find_cell(nb, "week03-gray-scott-history-reader")
    nb.cells.remove(gray_scott)
    nb.cells.remove(gray_reader)
    target = nb.cells.index(compressed) + 1
    nb.cells[target:target] = [gray_scott, gray_reader]

    grid_index = find_cell(nb, "09eb9036-81a5-4e05-8806-69d16664865b")
    grid_index.source = grid_index.source.replace(
        "### Index the grid before approximating derivatives",
        "## Index the grid before approximating derivatives",
        1,
    )

    # Keep the principal section hierarchy visually and semantically consistent.
    for cell in nb.cells:
        first = next(
            (line.strip() for line in cell.source.splitlines() if line.strip().startswith("#")),
            "",
        )
        if first.startswith("# "):
            cell.metadata.setdefault("slideshow", {})["slide_type"] = "slide"

    nbformat.write(nb, NOTEBOOK)


if __name__ == "__main__":
    main()
