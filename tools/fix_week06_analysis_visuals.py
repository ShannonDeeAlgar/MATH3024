import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
nb = json.loads(path.read_text())


def source(cell):
    return "".join(cell.get("source", []))


def set_source(cell, text):
    cell["source"] = text.rstrip().splitlines(keepends=True)
    if cell["source"]:
        cell["source"][-1] += "\n"


for cell in nb["cells"]:
    text = source(cell)

    if text.startswith("# Qualitative analysis\n"):
        set_source(cell, r'''# Qualitative analysis

<img src="images/kuramoto_phase_circle.gif" alt="The same Kuramoto phases shown as positions around a phase circle and as fixed nodes that flash" style="display:block;max-height:430px;max-width:94%;margin:0 auto">

The left view places each oscillator at its current position in the cycle. The right view keeps every node fixed and uses a flash to show when its clock completes a cycle. These are two displays of the same simulated phases; neither is physical movement.''')

    elif text.startswith("## Qualitative analysis\n"):
        set_source(cell, r'''## Qualitative analysis

<img src="images/kuramoto_phase_circle.gif" alt="The same Kuramoto phases shown as positions around a phase circle and as fixed nodes that flash" style="display:block;width:68%;max-width:760px;margin:1rem auto">

The phase-circle view shows each oscillator's position in its cycle. The fixed-node view instead makes a node flash as its clock passes phase zero. Both show the same simulation and neither places the oscillators in physical space.''')

    elif text.startswith("## Quantitative analysis\n"):
        text = text.replace(
            'style="display:block;width:72%;max-width:840px;margin:1rem auto"',
            'style="display:block;width:82%;max-width:980px;margin:1rem auto"',
        )
        set_source(cell, text)

    if "<strong>Up the ladder twice:</strong> phase trajectories become" in text:
        set_source(cell, text.replace(
            '<span><strong>Up the ladder twice:</strong> phase trajectories become $r_\\infty$ for one run; repeated runs then become an ensemble curve across $K$ and $N$.</span>',
            '<span><strong>Up the ladder twice:</strong> first summarise one run by its long-time coherence <i>r</i><sub>∞</sub>; then summarise repeated runs across <i>K</i> and <i>N</i>.</span>',
        ))

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
