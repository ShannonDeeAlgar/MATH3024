"""Complete the remaining Week 6 requests after the interrupted edit."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def source(text):
    return [line + "\n" for line in text.strip().splitlines()]


def main():
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]
    by_id = {cell.get("id"): cell for cell in cells}

    by_id["w6-coordination-contrast-slide"]["source"] = source(r"""
## Not all synchrony is self-organised

<img src="images/coordination_contrast.svg" alt="Choreographed coordination compared with spontaneous synchronisation" style="display:block;max-height:430px;max-width:100%;margin:0 auto">

Dance and synchronised swimming use a planned sequence and shared cues. Fireflies retain their own clocks and coordinate through interaction.
""")

    by_id["w6-coordination-contrast-reader"]["source"] = source(r"""
### Not all synchrony is self-organised

<img src="images/coordination_contrast.svg" alt="Choreographed coordination compared with spontaneous synchronisation" style="display:block;max-width:92%;margin:1rem auto">

Dance and synchronised swimming can be highly coordinated, but their timing is organised through a planned sequence, rehearsal and shared cues. The examples studied here are different: each component retains its own dynamics and responds to the others. A common rhythm can then arise without a conductor.
""")

    by_id["w6-frequency-heterogeneity-slide"]["source"] = source(r"""
## Different clocks can lock to a common rate

<img src="images/kuramoto_frequency_heterogeneity.gif" alt="Kuramoto phases moving around a circle and coloured by natural frequency beside the frequency distribution" style="display:block;max-height:510px;max-width:100%;margin:0 auto">

Coupling changes realised phase velocities, not the assigned natural frequencies. Slow clocks speed up and fast clocks slow down when they join the locked group.
""")

    reader = by_id["w6-controlled-heterogeneity-reader"]
    reader_text = "".join(reader["source"])
    reader_text = reader_text.replace(
        'src="images/kuramoto_frequency_heterogeneity.svg"',
        'src="images/kuramoto_frequency_heterogeneity.gif"',
    )
    reader["source"] = source(reader_text)

    video_id = "w6-swarmalator-videos-slide"
    video_cell = {
        "cell_type": "markdown",
        "id": video_id,
        "metadata": {
            "tags": ["slides-only"],
            "slideshow": {"slide_type": "subslide"},
        },
        "source": source(r"""
## Swarmalators in motion

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><iframe src="https://www.youtube.com/embed/atLhROLzsFo" title="Swarmalator realisation one" style="width:100%;height:360px;border:0" allowfullscreen></iframe></div>
<div class="image-panel"><iframe src="https://www.youtube.com/embed/Db6aiSa4soU" title="Swarmalator realisation two" style="width:100%;height:360px;border:0" allowfullscreen></iframe></div>
</div>

<p class="figure-credit"><a href="https://www.nature.com/articles/s41467-017-01190-3">O'Keeffe, Hong and Strogatz (2017), “Oscillators that sync and swarm”</a>.</p>
"""),
    }
    existing = next((i for i, cell in enumerate(cells) if cell.get("id") == video_id), None)
    if existing is not None:
        cells[existing] = video_cell
    else:
        swarm_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-swarmalators-slide")
        cells.insert(swarm_index + 1, video_cell)

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
