"""Repair Week 6 video fallbacks and clarify the unwrapped phase plot."""

import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
NOTEBOOK = BOOK / "notebooks/week06/L_Synchronisation.ipynb"


def linked_video(video_id: str, title: str, width: str = "82%") -> str:
    """Use a privacy-enhanced player with a visible fallback link."""
    return f'''<div style="width:{width};margin:0 auto;text-align:center">
<iframe src="https://www.youtube-nocookie.com/embed/{video_id}" title="{title}" style="display:block;width:100%;height:455px;border:0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>'''


data = json.loads(NOTEBOOK.read_text())
cells = {cell.get("id"): cell for cell in data["cells"]}

cells["w6-hook"]["source"] = (
    "# Real-world motivation\n\n"
    + linked_video("JWToUATLGzs", "Metronomes synchronising through a shared platform", "78%")
    + "\n\n<div class=\"discussion-marker\"><img src=\"images/discussion_marker.svg\" alt=\"Discussion prompt\"><span>How are the metronomes coordinating their behaviour?</span></div>\n"
).splitlines(keepends=True)

cells["w6-choreographed-swimmers"]["source"] = (
    "## Choreographed synchronisation\n\n"
    + linked_video("qsRmVtvbrAE", "Synchronised swimmers")
    + "\n\nThe swimmers coordinate through rehearsal, shared timing and a planned sequence. The synchronisation studied later arises from interacting systems that retain their own dynamics.\n"
).splitlines(keepends=True)

cells["metronome-hook"]["source"] = (
    "# Real-world motivation\n\n## Spontaneous synchronisation\n\n"
    "Synchronisation is coordination in time produced through coupling.\n\n"
    + linked_video("JWToUATLGzs", "Spontaneous synchronisation", "100%")
    + "\n"
).splitlines(keepends=True)

cells["w6-coordination-contrast-reader"]["source"] = (
    "### Choreographed coordination\n\n"
    + linked_video("qsRmVtvbrAE", "Choreographed synchronisation", "100%")
    + "\n\nDance and synchronised swimming can be precisely coordinated, but their timing follows choreography, rehearsal and shared cues. The systems studied here are different: each component retains its own dynamics and responds to the others. A common rhythm can then arise without a conductor.\n"
).splitlines(keepends=True)

slide_note = (
    "Several slow beat cycles are visible in the sum. Neither oscillator responds to the other: "
    "the unwrapped phase difference continues to drift. Phase is defined modulo $2\\pi$; wrapping "
    "the same curve would produce a sawtooth rather than a constant phase difference.\n"
)
source = "".join(cells["w6-beats"]["source"])
start = source.index("Several slow beat cycles")
end = source.index("\n\n\n<div", start)
source = source[:start] + slide_note + source[end:]
cells["w6-beats"]["source"] = source.splitlines(keepends=True)

reader = "".join(cells["reader-beats"]["source"])
needle = "That is not spontaneous synchronisation."
replacement = (
    "That is not spontaneous synchronisation. The phase-difference panel is deliberately unwrapped: "
    "its steady drift makes the absence of phase locking easy to see. Because phase is defined modulo "
    "$2\\pi$, wrapping it would give a sawtooth carrying the same circular information."
)
reader = reader.replace(needle, replacement)
cells["reader-beats"]["source"] = reader.splitlines(keepends=True)

NOTEBOOK.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
