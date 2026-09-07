#!/usr/bin/env python3
"""Tighten Reader subheaders and make workshop numerical sections implementation-specific."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def load(relative: str):
    path = NOTEBOOKS / relative
    return path, json.loads(path.read_text())


def save(path: Path, notebook: dict) -> None:
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


def source(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_source(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True)


def markdown(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def find_cell(nb: dict, needle: str) -> int:
    matches = [i for i, cell in enumerate(nb["cells"]) if needle in source(cell)]
    if len(matches) != 1:
        raise ValueError(f"Expected one cell containing {needle!r}; found {matches}")
    return matches[0]


def remove_heading(text: str, heading: str) -> str:
    lines = text.splitlines()
    if heading not in lines:
        return text
    index = lines.index(heading)
    del lines[index]
    while index < len(lines) and lines[index] == "":
        del lines[index]
    return "\n".join(lines).rstrip() + "\n"


def remove_paragraph(text: str, paragraph: str) -> str:
    if paragraph not in text:
        raise ValueError(f"Missing paragraph {paragraph!r}")
    return text.replace(paragraph, "").replace("\n\n\n", "\n\n")


def replace_numerical(relative: str, heading: str, replacement: str) -> None:
    path, nb = load(relative)
    index = find_cell(nb, heading)
    set_source(nb["cells"][index], replacement.strip() + "\n")
    save(path, nb)


def insert_after(relative: str, needle: str, text: str) -> None:
    path, nb = load(relative)
    new_source = text.strip() + "\n"
    if any(source(cell) == new_source for cell in nb["cells"]):
        return
    index = find_cell(nb, needle)
    nb["cells"].insert(index + 1, markdown(new_source))
    save(path, nb)


def deduplicate_exact_cells(relative: str) -> None:
    path, nb = load(relative)
    seen: set[tuple[str, str]] = set()
    cells = []
    for cell in nb["cells"]:
        normalised = source(cell).replace("$Delta", "$\\Delta")
        key = (cell.get("cell_type", ""), normalised)
        if key in seen:
            continue
        seen.add(key)
        cells.append(cell)
    nb["cells"] = cells
    save(path, nb)


def tidy_reader() -> None:
    path, nb = load("week06/L_Synchronisation.ipynb")
    for i in (56, 60):
        text = source(nb["cells"][i])
        heading = "## Specify the model" if i == 56 else "## A phase oscillator"
        set_source(nb["cells"][i], remove_heading(text, heading))

    text = source(nb["cells"][74])
    text = text.replace(
        "#### Sweep coupling and population size",
        "#### Sweep coupling and population size separately",
    )
    text = text.replace(
        "Response curves across <i>K</i> and <i>N</i> explore this ensemble-level representation rather than creating another rung.",
        "Response curves across $K$ and $N$ explore this ensemble-level representation rather than creating another rung.",
    )
    set_source(nb["cells"][74], text)
    save(path, nb)

    # This heading only repeats the banner immediately above it; the table is
    # the useful introduction and now follows the Analysis banner directly.
    path, nb = load("week04/L_Cellular_automata.ipynb")
    matches = [i for i, cell in enumerate(nb["cells"]) if "## Analysing cellular automata" in source(cell)]
    if matches:
        index = matches[0]
        set_source(nb["cells"][index], remove_heading(source(nb["cells"][index]), "## Analysing cellular automata"))
    save(path, nb)


def revise_workshops() -> None:
    for relative in (
        "week02/WS_Fractals.ipynb",
        "week04/WS_Cellular_automata.ipynb",
        "week09/WS_Information_theory.ipynb",
    ):
        deduplicate_exact_cells(relative)

    replace_numerical(
        "week01/WS_Introduction_to_complex_systems.ipynb",
        "### Numerical evolution",
        r"""
### Numerical evolution

The Schelling model already has a discrete update; there is no differential equation or numerical time step to approximate.

- Store the lattice as one integer array and use a seeded random-number generator.
- Count occupied Moore neighbours. At an outer edge, ignore positions beyond the grid; the world does not wrap.
- Move one randomly chosen dissatisfied agent at a time. Later moves therefore use the lattice left by earlier moves.
- Define one sweep as $N$ update attempts, where $N$ is the number of agents.
- Stop when no agent is dissatisfied or the sweep budget is reached. Record summaries after complete sweeps, not after an arbitrary number of individual moves.
""",
    )

    insert_after(
        "week02/WS_Fractals.ipynb",
        "### Pseudocode · nested initiator–generator construction",
        r"""
### Numerical construction

This model is a finite geometric construction rather than a time evolution.

- Store triangle vertices as coordinate triples.
- At each generation, calculate the three edge midpoints and replace every parent by its three corner children.
- Complete the whole generation before replacing the retained collection.
- There is no $\Delta t$, boundary condition or stochastic update in the canonical construction.
- Record the geometry at each requested depth; numerical precision and image resolution affect the rendered approximation, not the mathematical generator.
""",
    )

    replace_numerical(
        "week03/WS_Reaction_diffusion.ipynb",
        "### Numerical evolution",
        r"""
### Numerical evolution

Here the continuous PDE must be turned into a grid calculation.

- Choose $N$, $\Delta x$ and $\Delta t$ explicitly.
- Replace each Laplacian by the five-point finite-difference stencil, dividing by $(\Delta x)^2$.
- Implement periodic boundaries by wrapping array indices in both directions.
- Use forward Euler: add $\Delta t$ times the complete reaction–diffusion right-hand side.
- Calculate $u^{n+1}$ and $v^{n+1}$ from the same old arrays, then replace both together.
- Check that reducing $\Delta t$ or refining the grid does not materially change the claimed pattern. Record fields less often if storage or display is the limiting cost.
""",
    )

    # Cellular automata are exact discrete updates, but each canonical model
    # still needs its boundary and simultaneous-update convention stated.
    insert_after(
        "week04/WS_Cellular_automata.ipynb",
        "### Pseudocode · a lookup-table update",
        r"""
### Numerical evolution

The elementary cellular automaton is already discrete in space, state and time.

- Store the world as a binary row of length $L$.
- Use periodic indexing for the left and right neighbours.
- Decode the rule number once, then use the resulting lookup table at every site.
- Calculate the entire next row from the same current row before replacing it.
- One generation is one exact rule application; no $\Delta t$ or numerical integrator is required.
""",
    )
    insert_after(
        "week04/WS_Cellular_automata.ipynb",
        "### Pseudocode · a decision rule",
        r"""
### Numerical evolution

Game of Life also uses an exact synchronous update.

- Store the world as a two-dimensional binary array.
- Count the eight Moore neighbours using periodic wrap-around in both directions.
- Apply B3/S23 to every cell using the same old grid, then replace the grid once.
- Record the initial state as generation zero and state the generation budget or stopping test.
""",
    )

    replace_numerical(
        "week05/WS_ABM.ipynb",
        "### Numerical evolution",
        r"""
### Numerical evolution

The Vicsek rule is a discrete-time agent update; the main implementation choices are geometry and ordering.

- Calculate neighbour sets with the minimum-image distance on the periodic square.
- Average the neighbours' heading vectors, not their angle values directly.
- Draw the declared noise independently from the seeded generator.
- Use one snapshot of positions and headings for every agent in a step. Calculate all new headings and displacements before replacing the population.
- Wrap each new coordinate modulo $L$. With the workshop convention $\Delta t=1$, each displacement has length $v_0$; if $\Delta t$ is changed, use $v_0\Delta t$.
- Record positions, headings and polarisation at the declared interval.
""",
    )

    replace_numerical(
        "week06/WS_Synchronisation.ipynb",
        "### Numerical evolution",
        r"""
### Numerical evolution

The Kuramoto equations are continuous, so the workshop integrates them numerically.

- Draw and retain one natural frequency $\omega_i$ for every oscillator.
- At step $n$, calculate every coupling sum from the same phase vector $\boldsymbol\theta^n$ on the complete, equally weighted network.
- Use forward Euler,
  $\theta_i^{n+1}=\theta_i^n+\Delta t\,\dot\theta_i^n$,
  with $\Delta t=0.02$ unless the cell states otherwise.
- Wrap stored phases modulo $2\pi$ for display and circular statistics. This is a phase convention, not a physical boundary.
- Record simulated time as $t_n=n\Delta t$, together with phases, coherence $r$ and mean phase $\psi$. Reduce $\Delta t$ to check any result that looks jumpy or changes abruptly.
""",
    )

    replace_numerical(
        "week07/WS_Intelligent_systems.ipynb",
        "### Numerical evolution",
        r"""
### Numerical evolution

PSO advances by algorithmic iterations rather than physical time.

- Evaluate all current positions and update the stored personal and shared bests.
- Draw the random coefficients from the declared seeded generator.
- Calculate every new velocity using the same shared best, then move all particles.
- Apply the declared boundary rule consistently; this workshop clips positions and states what happens to the corresponding velocity component.
- Stop at the evaluation or iteration budget. Record objective evaluations as the computational cost, plus shared best and diversity after each complete iteration.
""",
    )

    replace_numerical(
        "week08/WS_Critical_phenomena.ipynb",
        "### Numerical evolution",
        r"""
### Numerical evolution

The Abelian sandpile uses an exact event-driven update rather than a numerical time step.

- Add a grain only when the lattice is stable.
- Use a queue to process unstable sites; each toppling sends one grain to each in-domain von Neumann neighbour.
- Discard grains that cross an open boundary. That loss is the dissipation mechanism.
- Finish the complete avalanche before adding the next grain. The final stable state is independent of legal queue order, although intermediate animation frames are not.
- Treat one grain addition as one driving event. Discard the declared burn-in and then record avalanche size, duration and area using fixed definitions.
""",
    )

    insert_after(
        "week09/WS_Information_theory.ipynb",
        "### Pseudocode · an analysis workflow",
        r"""
### Numerical measurement

This workshop estimates a measure from finite observations rather than evolving a canonical model.

- Define the symbols, blocks, bins or windows before counting.
- Convert counts to empirical probabilities and verify that they sum to one.
- Omit zero-probability terms from $p\log_2p$ and report entropy in bits.
- State the sample size. Repeated estimates across blocks or resamples expose finite-sample variation.
- Changing the representation changes the random variable and therefore the question being measured.
""",
    )

    replace_numerical(
        "week10/WS_Game_theory.ipynb",
        "### Numerical evolution",
        r"""
### Numerical evolution

The evolutionary extension uses generations as a discrete clock.

- Complete all match or expected-payoff calculations from the same current population.
- Translate payoff into the declared selection rule, normalise the new strategy frequencies, then apply mutation.
- Replace the whole population together so that loop order does not change the game.
- The baseline is well mixed and has no physical boundary. If a spatial network is introduced, its neighbourhood and update schedule must be stated.
- Stop after the declared generation budget and record strategy frequencies and payoff summaries at generation zero and after every update.
""",
    )

    # Remove later one-line reminders now made redundant by the focused section.
    removals = {
        "week01/WS_Introduction_to_complex_systems.ipynb": "**Numerical evolution:** one sweep is $N$ asynchronous update attempts. Record whether order within a sweep is randomised.\n",
        "week02/WS_Fractals.ipynb": "**Numerical evolution:** one iteration is one geometric construction generation, not a unit of physical time.\n",
        "week03/WS_Reaction_diffusion.ipynb": "**Numerical evolution:** calculate both new concentration arrays from the same old arrays, then replace them together; one step represents $\\Delta t$.\n",
        "week04/WS_Cellular_automata.ipynb": "**Numerical evolution:** one synchronous step applies the rule to every cell from the same previous configuration.\n",
        "week05/WS_ABM.ipynb": "**Numerical evolution:** calculate all new headings first, then move all agents. Changing that order changes the model.\n",
        "week07/WS_Intelligent_systems.ipynb": "**Numerical evolution:** evaluate positions, update memory, calculate velocities and then move. State exactly when the shared best is refreshed.\n",
        "week08/WS_Critical_phenomena.ipynb": "**Numerical evolution:** distinguish slow driving from fast relaxation. Add one grain, topple until stable and record that complete cascade as one avalanche.\n",
        "week10/WS_Game_theory.ipynb": "**Numerical evolution:** complete interactions and payoffs before selection, replacement and mutation form the next generation.\n",
    }
    for relative, paragraph in removals.items():
        path, nb = load(relative)
        matches = [i for i, cell in enumerate(nb["cells"]) if paragraph.strip() in source(cell)]
        if not matches:
            continue
        index = matches[0]
        text = remove_paragraph(source(nb["cells"][index]), paragraph)
        set_source(nb["cells"][index], text)
        save(path, nb)


if __name__ == "__main__":
    tidy_reader()
    revise_workshops()
