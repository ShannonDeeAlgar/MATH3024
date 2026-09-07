"""Extend Week 10's rock-paper-scissors example from a game to a population model."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week10/L_Game_theory.ipynb"


def markdown(
    cell_id: str,
    source: str,
    slide_type: str = "subslide",
    tags: list[str] | None = None,
) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {
            "slideshow": {"slide_type": slide_type},
            **({"tags": tags} if tags else {}),
        },
        "source": source,
    }


nb = json.loads(PATH.read_text())
cells = nb["cells"]

# Make repeated runs idempotent.
new_ids = {
    "w10-rps-local-game",
    "w10-rps-local-game-slide",
    "w10-rps-population",
    "w10-rps-population-slide",
}
cells[:] = [cell for cell in cells if cell.get("id") not in new_ids]

arena = next(i for i, cell in enumerate(cells) if cell.get("id") == "w10-rps-arena")

local_game = markdown(
    "w10-rps-local-game",
    r"""## One encounter is a game

For one encounter, each player chooses rock, paper or scissors. Give a win payoff (+1), a loss payoff (-1), and a draw payoff (0):

| Player 1 \ Player 2 | Rock | Paper | Scissors |
|---|---:|---:|---:|
| Rock | ((0,0)) | ((-1,+1)) | ((+1,-1)) |
| Paper | ((+1,-1)) | ((0,0)) | ((-1,+1)) |
| Scissors | ((-1,+1)) | ((+1,-1)) | ((0,0)) |

The ordered pair gives ((u_1,u_2)). This is a symmetric zero-sum game: one player's gain is the other's loss. No pure strategy is best against everything. Each strategy defeats one alternative and is defeated by another.

The mixed Nash equilibrium chooses each strategy with probability (1/3). Against that mixture, rock, paper and scissors have the same expected payoff.
""",
    tags=["reader-only"],
)

local_game_slide = markdown(
    "w10-rps-local-game-slide",
    r"""## One encounter is a game

Win (=+1), loss (=-1), draw (=0).

| Player 1 \ Player 2 | Rock | Paper | Scissors |
|---|---:|---:|---:|
| Rock | ((0,0)) | ((-1,+1)) | ((+1,-1)) |
| Paper | ((+1,-1)) | ((0,0)) | ((-1,+1)) |
| Scissors | ((-1,+1)) | ((+1,-1)) | ((0,0)) |

No pure strategy is best against everything. The symmetric mixed equilibrium uses each strategy with probability (1/3).
""",
    tags=["slides-only"],
)

population = markdown(
    "w10-rps-population",
    r"""## From one game to a population

The emoji arena is not merely a larger payoff matrix. It adds a population process:

1. each agent carries one of the three types;
2. agents move through a finite domain;
3. nearby agents encounter one another;
4. the cyclic rule determines the local winner;
5. the defeated agent is converted to the winner's type.

The payoff matrix determines **who defeats whom in one encounter**. It does not determine the population history by itself. Movement, collision rate, spatial clustering, boundary conditions, update order, initial numbers and chance all affect which encounters happen.

This also explains an apparently strange route to victory. Scissors cannot remove rock directly. For scissors to fill the arena, paper may first need to eliminate the rocks; scissors can then invade the remaining paper population. A type's prospects therefore depend on the abundance and spatial arrangement of all three types. This is **frequency-dependent selection** with cyclic dominance.

In a large well-mixed deterministic model, the three frequencies can keep cycling rather than selecting one permanent winner. Extinction in a finite agent simulation is a population-level outcome produced by demographic fluctuations and the implementation of space and interaction, not a new entry in the payoff matrix.

::: {admonition} Discussion
If every agent follows a fixed type rather than choosing an action, in what sense are the agents “playing” a game? Which parts belong to game theory, and which belong to the population model built around it?
:::
""",
    tags=["reader-only"],
)

population_slide = markdown(
    "w10-rps-population-slide",
    r"""## From one game to a population

**Local rule:** rock defeats scissors, scissors defeats paper, paper defeats rock.

The arena adds movement, local encounters, conversion, finite numbers and boundaries. These determine which games are actually played.

Scissors cannot remove rock directly. Paper may first eliminate rock, leaving a population that scissors can invade.

::: {admonition} Discussion
Does the payoff matrix determine the eventual winner?
:::
""",
    tags=["slides-only"],
)

cells[arena + 1 : arena + 1] = [
    local_game,
    local_game_slide,
    population,
    population_slide,
]
PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
