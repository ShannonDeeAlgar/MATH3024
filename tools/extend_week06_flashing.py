import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/WS_Synchronisation.ipynb"
notebook = json.loads(path.read_text())

for cell in notebook["cells"]:
    source = "".join(cell.get("source", []))
    if "def simulate_adaptive_kuramoto" in source:
        source = source.replace(
            "dt=0.05, steps=700, rewire_every=5, seed=SEED",
            "dt=0.05, steps=1400, rewire_every=5, seed=SEED",
        )
        cell["source"] = source.splitlines(keepends=True)
        break
else:
    raise RuntimeError("Adaptive Kuramoto simulation cell not found")

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
