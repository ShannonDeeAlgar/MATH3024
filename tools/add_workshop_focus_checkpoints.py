"""Make the stated modelling focus operational without adding a separate activity."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKPOINTS = {
    "week07/WS_Intelligent_systems.ipynb": (
        "evidence-checkpoint-pso",
        """## Evidence checkpoint

When you run PSO, keep the objective and computational budget fixed and repeat the run with several seeds. Record the best objective value, the iteration at which it was found, and the fraction of runs that reach a stated target. Use the particle trajectories to explain *why* two parameter choices differ; do not select a method from its single best run.
""",
        21,
    ),
    "week08/WS_Critical_phenomena.ipynb": (
        "evidence-checkpoint-scaling",
        """## Scaling checkpoint

For the same avalanche data, compare at least two defensible fitting ranges. Then repeat the measurement on a second lattice size. Report the fitted slope together with the range and system size: a stable relationship across these choices is stronger evidence than a straight-looking log–log plot.
""",
        12,
    ),
    "week10/WS_Game_theory.ipynb": (
        "evidence-checkpoint-evolution",
        """## Path-dependence checkpoint

Hold the payoff matrix fixed and change one evolutionary implementation choice: initial strategy frequencies, mutation rate, selection strength, or synchronous versus asynchronous replacement. Repeat each condition. A strategy that dominates in one history is not yet a general evolutionary conclusion.
""",
        25,
    ),
}

for relative, (cell_id, text, index) in CHECKPOINTS.items():
    path = ROOT / "notebooks" / relative
    nb = json.loads(path.read_text())
    nb["cells"] = [c for c in nb["cells"] if c.get("id") != cell_id]
    cell = {"cell_type": "markdown", "id": cell_id, "metadata": {},
            "source": text.splitlines(keepends=True)}
    nb["cells"].insert(min(index, len(nb["cells"])), cell)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    print(path.relative_to(ROOT))
