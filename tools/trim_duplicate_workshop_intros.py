"""Keep one concise workshop introduction before the modelling-focus marker."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLES = {
    "week01/WS_Introduction_to_complex_systems.ipynb": "# Week 1 workshop · Schelling segregation\n",
    "week02/WS_Fractals.ipynb": "# Week 2 workshop · Measuring a finite fractal\n",
    "week03/WS_Reaction_diffusion.ipynb": "# Week 3 workshop · Gray–Scott reaction–diffusion\n",
    "week04/WS_Cellular_automata.ipynb": "# Week 4 workshop · Cellular automata\n",
    "week05/WS_ABM.ipynb": "# Week 5 workshop · Vicsek flocking\n",
    "week06/WS_Synchronisation.ipynb": "# Week 6 workshop · Kuramoto synchronisation\n",
    "week07/WS_Intelligent_systems.ipynb": "# Week 7 workshop · Collective search with ACO and PSO\n",
    "week08/WS_Critical_phenomena.ipynb": "# Week 8 workshop · Critical phenomena\n",
    "week10/WS_Game_theory.ipynb": "# Week 10 workshop · Evolutionary game theory\n",
}

for relative, title in TITLES.items():
    path = ROOT / "notebooks" / relative
    nb = json.loads(path.read_text())
    first = nb["cells"][0]
    first["cell_type"] = "markdown"
    first["metadata"] = {}
    first["source"] = [title]
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    print(path.relative_to(ROOT))
