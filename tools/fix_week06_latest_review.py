import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
WORKSHOP = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"


def text(cell):
    return "".join(cell.get("source", []))


def set_text(cell, value):
    cell["source"] = value.rstrip().splitlines(keepends=True)
    if cell["source"]:
        cell["source"][-1] += "\n"


def find(cells, needle, tag=None):
    for i, cell in enumerate(cells):
        if needle in text(cell) and (tag is None or tag in cell.get("metadata", {}).get("tags", [])):
            return i
    raise ValueError(f"Could not find {needle!r} ({tag})")


# Put the two hands-on examples together under the explicit Explorable banner.
nb = json.loads(LECTURE.read_text())
cells = nb["cells"]
for tag in ("slides-only", "reader-only"):
    banner = cells.pop(find(cells, "# Explorable", tag))
    fireflies = cells.pop(find(cells, "Nicky Case", tag))
    bridge = cells.pop(find(cells, "## From fireflies to Kuramoto", tag))
    cycle = cells.pop(find(cells, "## Explore the Kuramoto model", tag))

    firefly_source = text(fireflies)
    if tag == "slides-only":
        firefly_source = firefly_source.replace(
            "## Fireflies · clocks that influence clocks",
            "## Nicky Case · Fireflies",
        )
        set_text(
            bridge,
            """## From fireflies to Kuramoto

Kuramoto keeps an internal clock, differences between intrinsic rates, and interactions that alter timing.

It replaces flash pulses by smooth phase coupling and spatial visibility by equal all-to-all interaction. Brightness, movement, occlusion and physiology are omitted.

The model asks whether coupling can overcome heterogeneity in the clocks. Pulse-coupled and spatial models return later when those omissions matter.""",
        )
    else:
        firefly_source = firefly_source.replace("## Fireflies", "## Nicky Case · Fireflies")
        # The supplied wording is already present; remove the now-redundant ladder marker.
        bridge_source = text(bridge).split('<div class="ladder-marker">', 1)[0].rstrip()
        set_text(bridge, bridge_source)
    set_text(fireflies, firefly_source)
    set_text(cycle, text(cycle).replace("## Explore the Kuramoto model", "## Kuramotocycle"))

    insert_at = find(cells, "# Model details", tag)
    cells[insert_at:insert_at] = [banner, fireflies, bridge, cycle]

# Keep the two-oscillator diagram subordinate to its explanation in the Reader.
reader_two = cells[find(cells, "## Two uncoupled oscillators", "reader-only")]
set_text(
    reader_two,
    text(reader_two).replace(
        'style="max-height:300px"',
        'style="display:block;width:72%;max-width:430px;max-height:235px;margin:0 auto"',
    ),
)
LECTURE.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


nb = json.loads(WORKSHOP.read_text())
cells = nb["cells"]

# Use a colour that is actually defined in the workshop palette.
coherence = cells[find(cells, "psi_periodic")]
set_text(coherence, text(coherence).replace("color=ORANGE", "color=YELLOW"))

# Permit the same player to identify an oscillator selected by the analysis.
player = cells[find(cells, "def kuramoto_player")]
source = text(player)
source = source.replace(
    'def kuramoto_player(history: np.ndarray, element_id="kuramoto-player"):',
    'def kuramoto_player(history: np.ndarray, element_id="kuramoto-player", highlight_index: int | None = None):',
)
source = source.replace(
    'data = json.dumps(np.round(history, 4).tolist())',
    'data = json.dumps(np.round(history, 4).tolist())\n    highlight = "null" if highlight_index is None else str(int(highlight_index))',
)
source = source.replace(
    'const root=document.getElementById(\'{element_id}\'), states={data};',
    'const root=document.getElementById(\'{element_id}\'), states={data}, highlight={highlight};',
)
source = source.replace(
    "phases.forEach(a=>{{mx+=Math.cos(a);my+=Math.sin(a);ctx.fillStyle='#5879AA';ctx.beginPath();ctx.arc(cx+R*Math.cos(a),cy-R*Math.sin(a),4,0,2*Math.PI);ctx.fill();}});",
    "phases.forEach((a,i)=>{{mx+=Math.cos(a);my+=Math.sin(a);ctx.fillStyle=(i===highlight?'#EDCC55':'#5879AA');ctx.strokeStyle='#1B2A4C';ctx.lineWidth=(i===highlight?1.5:0);ctx.beginPath();ctx.arc(cx+R*Math.cos(a),cy-R*Math.sin(a),(i===highlight?7:4),0,2*Math.PI);ctx.fill();if(i===highlight)ctx.stroke();}});",
)
set_text(player, source)

# Return from the aggregate frequency plot to the one oscillator that fails to lock.
inspect = cells[find(cells, "def simulate_given_population")]
source = text(inspect)
source += """

drifting_indices = np.flatnonzero(~locked)
if len(drifting_indices):
    highlighted_drifter = int(drifting_indices[np.argmax(omega[drifting_indices])])
    print(
        f"Yellow oscillator: natural rate {omega[highlighted_drifter]:.2f}; "
        f"realised rate {realised_rate[highlighted_drifter]:.2f}."
    )
    display(kuramoto_player(
        locked_history,
        element_id="drifting-oscillator-player",
        highlight_index=highlighted_drifter,
    ))
"""
set_text(inspect, source)

inspect_intro = cells[find(cells, "# Inspect natural and realised frequencies")]
set_text(
    inspect_intro,
    text(inspect_intro) + "\n\nAfter locating a drifting point in the frequency plot, return to the individual simulation. The same oscillator is highlighted in yellow. Its unusually fast internal clock keeps pulling it through the locked group rather than allowing a fixed phase relationship.\n",
)

# Use a colourblind-friendly cyclic palette for phase and name graph edges consistently.
for cell in cells:
    source = text(cell)
    source = source.replace("corresponding edge is drawn as a line", "corresponding edge is drawn")
    source = source.replace("<strong>Line:</strong>", "<strong>Edge:</strong>")
    source = source.replace(
        "background:linear-gradient(90deg,hsl(0,68%,48%),hsl(60,68%,48%),hsl(120,68%,48%),hsl(180,68%,48%),hsl(240,68%,48%),hsl(300,68%,48%),hsl(360,68%,48%))",
        "background:linear-gradient(90deg,#3B4CC0,#688AE8,#B9D6F2,#F2C14E,#E07A5F,#8C4A8C,#3B4CC0)",
    )
    source = source.replace(
        "function colour(a) {{return `hsl(${{(a+Math.PI)*180/Math.PI}},68%,48%)`;}}",
        "function colour(a) {{const p=['#3B4CC0','#688AE8','#B9D6F2','#F2C14E','#E07A5F','#8C4A8C']; return p[Math.floor((((a+Math.PI)/(2*Math.PI))%1+1)%1*p.length)];}}",
    )
    set_text(cell, source)
    if cell.get("cell_type") == "code":
        cell["outputs"] = []
        cell["execution_count"] = None

WORKSHOP.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
