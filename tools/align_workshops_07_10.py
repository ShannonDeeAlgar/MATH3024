#!/usr/bin/env python3
"""Bring Workshops 7--10 into the current workshop structure and language."""

from __future__ import annotations

import json
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": text.rstrip() + "\n",
    }


def source(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else value


def set_source(cell: dict, text: str) -> None:
    cell["source"] = text.rstrip() + "\n"


def insert_after(cells: list[dict], prefix: str, additions: list[dict]) -> None:
    addition_prefix = source(additions[0]).splitlines()[0]
    if any(source(cell).startswith(addition_prefix) for cell in cells):
        return
    for index, cell in enumerate(cells):
        if source(cell).startswith(prefix):
            cells[index + 1:index + 1] = additions
            return
    raise ValueError(f"Could not find heading beginning {prefix!r}")


def replace_prefix(cells: list[dict], old: str, new: str) -> None:
    for cell in cells:
        text = source(cell)
        if text.startswith(old):
            set_source(cell, new + text[len(old):])
            return


def update_week07(path: Path) -> None:
    notebook = json.loads(path.read_text())
    cells = notebook["cells"]

    # The current modelling focus is working with data, not code reuse itself.
    for cell in cells:
        text = source(cell)
        if text.startswith("**Canonical model"):
            set_source(cell, """**Canonical models:** ant colony optimisation and particle swarm optimisation.

**Modelling practice:** represent, evaluate and compare collective search.

ACO constructs routes through a graph and stores shared evidence in pheromone on its edges. PSO moves candidate solutions through a numerical search space and shares a global best-so-far record. The workshop makes both algorithms explicit in pseudocode, then uses PSO for the implementation and student-led investigation.""")

    insert_after(cells, "# Simulate and inspect", [md("""## Animate the search

The simulation stores particle positions and the best point found at every iteration. The animation simply displays that saved history. This is the same student-level pattern used earlier: update existing Matplotlib artists rather than writing a separate presentation interface. A polished player would not add anything needed for this investigation.""")])
    replace_prefix(cells, "### Rastrigin search over time", "### Rastrigin search")
    replace_prefix(cells, "### 5. Repeat the run", "## Repeat across seeds")

    for cell in cells:
        text = source(cell)
        if cell["cell_type"] == "code" and "from matplotlib.animation import FuncAnimation" in text:
            if "from tqdm.auto import tqdm" in text and "except ImportError" not in text:
                text = text.replace(
                    "from tqdm.auto import tqdm\n",
                    "try:\n"
                    "    from tqdm.auto import tqdm\n"
                    "except ImportError:\n"
                    "    def tqdm(iterable, **kwargs):\n"
                    "        return iterable\n",
                )
                set_source(cell, text)
            elif "from tqdm.auto import tqdm" not in text:
                text = text.replace(
                    "from IPython.display import HTML\n",
                    "from IPython.display import HTML\n"
                    "try:\n"
                    "    from tqdm.auto import tqdm\n"
                    "except ImportError:\n"
                    "    def tqdm(iterable, **kwargs):\n"
                    "        return iterable\n",
                )
                set_source(cell, text)
        if cell["cell_type"] == "code" and text.startswith("runs = [run_pso"):
            set_source(cell, text.replace(
                "runs = [run_pso(seed=seed, steps=100) for seed in range(40)]",
                "runs = [run_pso(seed=seed, steps=100)\n        for seed in tqdm(range(40), desc=\"Repeated PSO runs\")]",
            ))

    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


def update_week08(path: Path) -> None:
    notebook = json.loads(path.read_text())
    cells = notebook["cells"]

    for cell in cells:
        text = source(cell)
        if text.startswith("**Canonical model:** Abelian sandpile"):
            set_source(cell, """**Canonical model:** Abelian sandpile.

**Modelling practice:** reuse and extend an existing lattice model.

Borrowing code is normal mathematical and scientific work. With proper attribution, the useful question is not whether reuse is allowed, but whether it is valid. Here we retain the Week 4 lattice and neighbourhood machinery, replace the stored state and update rule, and add tests that check the inherited scaffold still represents the new model.

The avalanche analysis then asks a separate scientific question: which claims about scale-free behaviour are actually supported by a finite simulation?""")

    insert_after(cells, "# Simulate and inspect", [md("""## Animate one avalanche

The model records the lattice after each parallel relaxation step. A compact Matplotlib animation is enough to inspect that update sequence. The step-by-step display is a numerical convention, not a claim that a physical sandpile topples in perfectly synchronous rounds.""")])
    replace_prefix(cells, "### Begin with slow driving", "### Begin with slow driving")

    for cell in cells:
        text = source(cell)
        if cell["cell_type"] == "code" and text.lstrip().startswith("import numpy as np"):
            if "from tqdm.auto import tqdm" in text and "except ImportError" not in text:
                text = text.replace(
                    "from tqdm.auto import tqdm\n",
                    "try:\n"
                    "    from tqdm.auto import tqdm\n"
                    "except ImportError:\n"
                    "    def tqdm(iterable, **kwargs):\n"
                    "        return iterable\n",
                )
                set_source(cell, text)
            elif "from tqdm.auto import tqdm" not in text:
                text = text.replace(
                    "from collections import deque\n",
                    "from collections import deque\n"
                    "try:\n"
                    "    from tqdm.auto import tqdm\n"
                    "except ImportError:\n"
                    "    def tqdm(iterable, **kwargs):\n"
                    "        return iterable\n",
                )
                set_source(cell, text)
        if cell["cell_type"] == "code" and "for L, additions, burn_in in [(24" in text:
            text = text.replace(
                "for L, additions, burn_in in [(24, 8_000, 2_000), (40, 14_000, 3_500)]:",
                "conditions = [(24, 8_000, 2_000), (40, 14_000, 3_500)]\nfor L, additions, burn_in in tqdm(conditions, desc=\"Finite-size comparison\"):",
            )
            set_source(cell, text)

    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


def update_week09(path: Path) -> None:
    notebook = json.loads(path.read_text())
    cells = notebook["cells"]

    for cell in cells:
        text = source(cell)
        if text.startswith("**Core measure:** Shannon entropy"):
            set_source(cell, """**Core measure:** Shannon entropy.

**Modelling practice:** representation determines what a summary can retain.

This shorter workshop checks entropy on known distributions and then estimates distributions from two public-domain books. There is deliberately no canonical time-stepping animation: the computational object is a probability distribution, and the main decision is how observations are converted into outcomes before entropy is calculated.""")

    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


def update_week10(path: Path) -> None:
    notebook = json.loads(path.read_text())
    cells = notebook["cells"]

    replacements = {
        "## EvolutionTo evolve is to change over time": "## Evolution changes populations\n\nTo evolve is to change over time",
        "### Explaining global/macroscopic observationsi.e. the output": "### What evolution explains",
        "### Mechanisms for evolutioni.e. the inputs required": "### Mechanisms required for evolution",
        "#### FitnessEvolution is a change": "#### Fitness\n\nEvolution is a change",
        "#### Remember...Agents don't move": "#### Agents do not move across the fitness landscape\n\nAgents don't move",
        "### Building the required mechanisms for adaptation into the model1.": "### Build the mechanisms into the model\n\n1.",
        "### Successful strategiesSuccessful strategies": "### Successful strategies\n\nSuccessful strategies",
        "#### Tit for TatOne strategy": "#### Tit for Tat\n\nOne strategy",
        "### AnalysisWhat sorts of questions": "## Questions the model can address\n\nWhat sorts of questions",
    }
    for cell in cells:
        text = source(cell)
        for old, new in replacements.items():
            if text.startswith(old):
                set_source(cell, new + text[len(old):])
                break

    insert_after(cells, "# Simulate and inspect", [md("""## Animate population change

The simulation stores one vector of strategy frequencies per generation. The animation updates a bar chart from that history. This is a student-level inspection tool; no separate polished player is needed.""")])
    replace_prefix(cells, "### Inspect the evolving population", "### Strategy frequencies by generation")
    replace_prefix(cells, "### Path-dependence checkpoint", "## Compare evolutionary histories")

    # Keep the course sign-off at the actual end of the final workshop.
    signoff = None
    cleaned = []
    for cell in cells:
        text = source(cell)
        if text.strip() == 'print("Lectures completed successfully!")':
            continue
        if "Tiger got to hunt, bird got to fly" in text:
            signoff = cell
            continue
        cleaned.append(cell)
    cells[:] = cleaned
    if signoff is not None:
        cells.append(signoff)

    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


def main() -> None:
    update_week07(ROOT / "notebooks/week07/WS_Intelligent_systems.ipynb")
    update_week08(ROOT / "notebooks/week08/WS_Critical_phenomena.ipynb")
    update_week09(ROOT / "notebooks/week09/WS_Information_theory.ipynb")
    update_week10(ROOT / "notebooks/week10/WS_Game_theory.ipynb")


if __name__ == "__main__":
    main()
