"""Add the beats audio and make the Week 6 analysis hierarchy explicit."""

import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
notebook = json.loads(path.read_text())
cells = notebook["cells"]


def source(cell):
    return "".join(cell.get("source", []))


def set_source(cell, text):
    cell["source"] = text.splitlines(keepends=True)


def markdown(cell_id, text, slide_type="skip", tags=None):
    metadata = {"slideshow": {"slide_type": slide_type}}
    if tags:
        metadata["tags"] = tags
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": metadata,
        "source": text.splitlines(keepends=True),
    }


by_id = {cell.get("id"): cell for cell in cells}
audio = '''
<div style="max-width:720px;margin:0.35rem auto 0;text-align:center">
<audio controls preload="metadata" src="audio/uncoupled_beats_440_443.wav" style="width:100%">
Your browser does not support embedded audio.
</audio>
<p class="figure-credit">Two fixed tones at 440 Hz and 443 Hz. Listen for the changing loudness: neither tone adjusts its frequency.</p>
</div>
'''

for cell_id in ("w6-beats", "reader-beats"):
    text = source(by_id[cell_id])
    if "uncoupled_beats_440_443.wav" not in text:
        set_source(by_id[cell_id], text.rstrip() + "\n\n" + audio)

if "w6-quantitative-analysis" not in by_id:
    watch_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-watch")
    cells.insert(
        watch_index + 1,
        markdown(
            "w6-quantitative-analysis",
            "# Quantitative analysis\n",
            slide_type="subslide",
            tags=["slides-only"],
        ),
    )

if "reader-quantitative-analysis" not in {cell.get("id") for cell in cells}:
    video_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "kuramoto-video")
    cells.insert(
        video_index + 1,
        markdown(
            "reader-quantitative-analysis",
            "## Quantitative analysis\n\nThe animation shows phases organising. We now compress that configuration into a collective measure and use it to compare runs and parameter values.\n",
            slide_type="skip",
            tags=["reader-only"],
        ),
    )

# Keep the standard model summary and pseudocode beside the model account,
# immediately before analysis rather than after the extensions.
canonical = next(cell for cell in cells if cell.get("id") == "canonical-pseudocode")
cells.remove(canonical)
analysis_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-e3d28ed62b")
cells.insert(analysis_index, canonical)

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
