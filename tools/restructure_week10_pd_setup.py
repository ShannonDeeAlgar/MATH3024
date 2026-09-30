"""Make the Prisoner's Dilemma introduction follow situation -> game specification."""

import json
from pathlib import Path

from nbconvert.filters import markdown2html


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week10/L_Game_theory.ipynb"


def lines(text: str) -> list[str]:
    return text.strip().splitlines(keepends=True)


notebook = json.loads(PATH.read_text())
cells = notebook["cells"]
by_id = {cell["id"]: cell for cell in cells}

by_id["d9bf6664"]["source"] = lines(
    r"""
## Prisoner's dilemma

*Two suspects are arrested after a burglary. The police can prove only the lesser offence of trespassing unless one suspect testifies against the other. They are interrogated separately and cannot communicate.*

Their sentences depend on both choices.
"""
)

by_id["66c07965-eb0d-4b59-8c59-fb65f6caf6e0"]["source"] = lines(
    r"""
## Sentence outcomes

| What happens | Sentence |
|---|---|
| One testifies; the other stays silent | The testifying suspect goes free; the silent suspect serves 3 years |
| Both testify | 2 years each |
| Both stay silent | 1 year each |

Each suspect can shorten their own sentence by testifying, whatever the other does, although both are better off if both stay silent. We now represent this situation as a game.
"""
)

by_id["8309b600-a5e3-4836-853a-d685bf85dd2f"]["source"] = lines(
    r"""
## Setting it up as a game

This is a **one-shot game**: each prisoner makes one choice, with no later rounds.

| Component | Specification |
|---|---|
| Players | $P=\{1,2\}$ |
| Actions | $A_1=A_2=\{C,D\}$, where $C$ means cooperate by staying silent and $D$ means defect by testifying |
| Payoffs (utilities) | $u_1$ and $u_2$ are negative prison sentences, so a less negative value is better |

Because there is only one decision, choosing $C$ or $D$ is also a **pure strategy**.

> Notation warning: here $C$ means cooperate (stay silent) and $D$ means defect (testify). Some versions instead use $C$ for confess and $D$ for don't confess. The letters then mean the exact opposite, so always check the action definitions.
"""
)

by_id["185e0fc7-41d0-47a3-b5e9-cdedc9619297"]["source"] = lines(
    r"""
### Action profiles

The set of **action profiles** contains all possible action pairs:

$$
S=\{C,D\}\times\{C,D\}=\{(C,C),(C,D),(D,C),(D,D)\}
$$

For each profile in $S$, the payoff functions $u_1$ and $u_2$ give the two prisoners' utilities.
"""
)

by_id["185e0fc7-41d0-47a3-b5e9-cdedc9619297-notation-slide"]["source"] = lines(
    r"""
### Action profiles

The set of **action profiles** contains all possible action pairs:

<!-- reader-equation: 185e0fc7-41d0-47a3-b5e9-cdedc9619297:0 -->

For each profile in $S$, $u_1$ and $u_2$ give the two prisoners' utilities.

<p style="font-size:0.68em;color:#5B6780"><strong>Notation:</strong> $S$ is the set of action pairs; $\times$ forms the Cartesian product. The first entry is Player 1's action.</p>
"""
)

by_id["e190c160-09b7-46d5-8983-6aa6f397daf4"]["source"] = lines(
    r"""
### Payoffs

Using negative years in prison as utility gives

$$
\begin{aligned}
u_1(D,C)&=0, & u_1(C,D)&=-3, & u_1(D,D)&=-2, & u_1(C,C)&=-1,\\
u_2(C,D)&=0, & u_2(D,C)&=-3, & u_2(D,D)&=-2, & u_2(C,C)&=-1.
\end{aligned}
$$

Here $u_i(a_1,a_2)$ is Player $i$'s **payoff** for the action profile $(a_1,a_2)$. Higher utility means a better outcome.

The same sentence can be represented in equivalent ways:

| Quantity shown | Interpretation | Player's objective | Value for a 1-year sentence |
|---|---|---|---:|
| $t_i$ | Years in prison: a cost | Minimise | $1$ |
| $u_i=-t_i$ | Negative prison years: a payoff | Maximise | $-1$ |
| $u_i=3-t_i$ | Years saved from the 3-year maximum: a payoff | Maximise | $2$ |

All three give the same ranking of outcomes. This chapter uses $u_i=-t_i$. Strictly, a payoff or utility is maximised; prison time itself is a cost to minimise.
"""
)

by_id["e190c160-09b7-46d5-8983-6aa6f397daf4-notation-slide"]["source"] = lines(
    r"""
### Payoffs

Using negative years in prison as utility gives

<!-- reader-equation: e190c160-09b7-46d5-8983-6aa6f397daf4:0 -->

| Quantity shown | Objective | 1-year sentence |
|---|---|---:|
| Prison years $t_i$ | Minimise | $1$ |
| Payoff $u_i=-t_i$ | Maximise | $-1$ |
| Payoff $u_i=3-t_i$ | Maximise | $2$ |

<p style="font-size:0.64em;color:#5B6780"><strong>Convention:</strong> All three rank the outcomes identically. This chapter uses $u_i=-t_i$. Prison time is a cost to minimise; payoff or utility is maximised.</p>
"""
)

by_id["a7aa8aa3"]["source"] = lines(
    r"""
### Assumptions for the one-shot analysis

We assume each prisoner is a **rational agent** who knows the actions and payoffs and maximises expected payoff. Each also has **self-regarding preferences**: only their own sentence enters their payoff. They cannot communicate or make enforceable agreements, and there are no later rounds for reward or retaliation.
"""
)

by_id["5bae5727-5f69-4a88-8374-011f404fd785"]["source"] = lines(
    r"""
This is a **symmetric game**: swapping the prisoners' roles swaps their payoffs without changing the incentives. Symmetry does not require equal payoffs when they choose different actions.
"""
)

by_id["c1cd393a-fb79-4969-886d-91559cef052a"]["source"] = lines(
    r"""
### Payoff matrix

Player 1 chooses a row and Player 2 chooses a column; each cell gives the ordered payoff pair $(u_1,u_2)$.

$$
\begin{array}{c|c|c|}
 & C & D \\
\hline
C & (-1,-1) & (-3,0) \\
\hline
D & (0,-3) & (-2,-2) \\
\hline
\end{array}
$$
"""
)

by_id["b45337ad-0c4a-4ffc-b1b7-3c330bdf79ce"]["source"] = lines(
    r"""
### Best responses

A **best response** is the action that gives a player the highest payoff after the other player's action is held fixed.

- For Player 1, fix Player 2's column and compare the first number down that column.
- For Player 2, fix Player 1's row and compare the second number across that row.

The larger number is better because these payoffs are negative years in prison.
"""
)

by_id["5cddb19c"]["source"] = lines(
    r"""
### Read across a row: Player 2

<!-- reader-equation: c1cd393a-fb79-4969-886d-91559cef052a:0 -->

Read the **second** number and hold Player 1's row fixed.

- If Player 1 chooses $C$: $0>-1$, so Player 2 chooses $D$.
- If Player 1 chooses $D$: $-2>-3$, so Player 2 again chooses $D$.

Thus $D$ is Player 2's best response to either row.
"""
)
by_id["5cddb19c"]["metadata"]["tags"] = ["slides", "slides-only"]

by_id["f328572a"]["source"] = lines(
    r"""
### Reading best responses from the matrix

Hold the other player's action fixed, then compare only the payoff entries belonging to the player whose decision you are analysing. Move across one row for Player 2 or down one column for Player 1, rather than comparing all four cells at once.
"""
)

by_id["4c60edf4-5607-4ff8-a279-e6770d3a517b"]["source"] = lines(
    r"""
#### Worked comparisons

For Player 2, read the second number across each fixed row:

| Player 1 fixed at | Player 2 compares | Player 2's best response |
|---|---|---|
| $C$ | $u_2(C,C)=-1$ with $u_2(C,D)=0$ | $D$ |
| $D$ | $u_2(D,C)=-3$ with $u_2(D,D)=-2$ | $D$ |

For Player 1, read the first number down each fixed column:

| Player 2 fixed at | Player 1 compares | Player 1's best response |
|---|---|---|
| $C$ | $u_1(C,C)=-1$ with $u_1(D,C)=0$ | $D$ |
| $D$ | $u_1(C,D)=-3$ with $u_1(D,D)=-2$ | $D$ |

Defection is therefore a best response to either action of the other player.
"""
)

by_id["5c9c5f1b-240a-40d7-af94-04ffc2412d2e"]["source"] = lines(
    r"""
<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Now analyse Player 1 without appealing to symmetry. Which payoff entry should you read, which direction should you move through the table, and which action is best in each column?</span></div>
"""
)
by_id["5c9c5f1b-240a-40d7-af94-04ffc2412d2e"]["metadata"]["tags"] = ["slides"]
by_id["5c9c5f1b-240a-40d7-af94-04ffc2412d2e"]["metadata"]["slideshow"]["slide_type"] = "subslide"

by_id["e902a40e-5ac1-4db4-ad7c-a606d1f0f688"]["source"] = lines(
    r"""
### Read down a column: Player 1

<!-- reader-equation: c1cd393a-fb79-4969-886d-91559cef052a:0 -->

Read the **first** number and hold Player 2's column fixed.

- If Player 2 chooses $C$: $0>-1$, so Player 1 chooses $D$.
- If Player 2 chooses $D$: $-2>-3$, so Player 1 again chooses $D$.

Both players therefore choose $D$, giving the action profile $(D,D)$.
"""
)
by_id["e902a40e-5ac1-4db4-ad7c-a606d1f0f688"]["metadata"]["tags"] = ["slides", "slides-only"]

by_id["894680c8-6d78-4117-b994-6b42b5c64ffe"]["source"] = lines(
    r"""
### Dominance and Nash equilibrium

An action is a **strictly dominant strategy** when it gives a higher payoff than every alternative for every action of the other player. An action is a **strictly dominated strategy** when another action gives a higher payoff against every possible action of the other player. Here $D$ strictly dominates $C$ for both players.

A **unilateral deviation** changes only one player's action while holding the other player's action fixed. A **Nash equilibrium** is an action profile where no player can improve their payoff by such a change. At $(D,D)$, either player who switches alone moves from $-2$ to $-3$, so $(D,D)$ is the Nash equilibrium.
"""
)

by_id["80d8c077-b0d1-4dfc-a437-c013e3d791c3"]["source"] = lines(
    r"""
The analysed payoff plane collects the same comparisons into one picture. An open point has at least one outgoing arrow: a player can improve their payoff by changing action alone. The filled point has no outgoing improvement arrow.
"""
)

for cell_id in (
    "23b5f14b-0e4a-4022-aac7-58f12afc629a",
):
    by_id[cell_id]["source"] = lines(
        r"""
<img class="game-plane-figure" src="images/pd_best_response_plane.svg" alt="Prisoner's Dilemma payoff plane with arrows marking profitable unilateral deviations">

<p class="figure-caption" id="fig-w10-1"><strong>Figure 10.1.</strong> Red arrows change Row / Player 1's action; blue arrows change Column / Player 2's. Each open point has an outgoing profitable-deviation arrow and is not a Nash equilibrium. The filled (D, D) point has none and is the Nash equilibrium. Here “stable” means stable against a one-player payoff-improving change, not dynamically stable.</p>
"""
    )

pareto = by_id["23f6c473"]
pareto["metadata"]["tags"] = ["slides", "reader-only"]
heading, body = "".join(pareto["source"]).split("\n\n", 1)
figure = "".join(by_id["23b5f14b-0e4a-4022-aac7-58f12afc629a"]["source"])
pareto_slide = by_id["23b5f14b-0e4a-4022-aac7-58f12afc629a-notation-slide"]
pareto_slide["metadata"]["slideshow"]["slide_type"] = "subslide"
pareto_slide["source"] = lines(
    heading + '\n\n<div class="two-panel compact-panels image-text">\n'
    '<div class="text-panel">' + str(markdown2html(body)) + '</div>\n'
    '<div class="image-panel">' + figure + '</div>\n</div>\n'
)

by_id["25badfda-ee10-490f-9007-aeb412118a43"]["source"] = lines(
    r"""
### Why use a payoff plane?

<div class="two-panel wide-left compact-panels image-text">
<div class="image-panel"><img class="game-plane-figure" src="images/pd_payoff_plane.svg" alt="The four Prisoner's Dilemma outcomes plotted on axes for Player 1 and Player 2 payoffs" style="max-height:440px">

<p class="figure-caption" id="fig-w10-1"><strong>Figure 10.1.</strong> Each action profile is plotted at its ordered payoff pair. Labels give the actions (Row / Player 1, Column / Player 2); red lines compare a change by Row / Player 1 and blue lines a change by Column / Player 2. The lines are comparisons, not time trajectories.</p></div>
<div class="text-panel"><p>The matrix lists the outcomes; the plane makes changes easier to compare.</p><p>Moving right improves Player 1's payoff. Moving up improves Player 2's payoff.</p></div>
</div>
"""
)

by_id["25badfda-ee10-490f-9007-aeb412118a43-notation-slide"]["source"] = lines(
    r"""
## Why use a payoff plane?

<div class="two-panel wide-left compact-panels image-text">
<div class="image-panel"><img class="game-plane-figure" src="images/pd_payoff_plane.svg" alt="The four Prisoner's Dilemma outcomes plotted on axes for Player 1 and Player 2 payoffs" style="max-height:440px">

<p class="figure-caption" id="fig-w10-1"><strong>Figure 10.1.</strong> Each action profile is plotted at its ordered payoff pair. Labels give the actions (Row / Player 1, Column / Player 2); red lines compare a change by Row / Player 1 and blue lines a change by Column / Player 2. The lines are comparisons, not time trajectories.</p></div>
<div class="text-panel"><p>The matrix lists the outcomes; the plane makes changes easier to compare.</p><p><strong>Right:</strong> better for Player 1.<br><strong>Up:</strong> better for Player 2.</p></div>
</div>

<p style="font-size:0.64em;color:#5B6780"><strong>Notation:</strong> Utilities are negative prison years, so higher is better. $C,D$ denote cooperate and defect.</p>
"""
)
by_id["25badfda-ee10-490f-9007-aeb412118a43-notation-slide"]["metadata"]["slideshow"]["slide_type"] = "subslide"

for cell_id in (
    "f95edecc",
    "2a16b0f2-d6af-4646-8603-d1d5c9de546c",
    "6c783eae-c501-4a37-aeb4-7c037290d6a8",
    "8fd073a2",
    "1c3345d1-ec3e-4ed8-9ee5-3d1a9a8dcbe4",
    "8c417d1a-1188-4e62-9112-014e89519f9f",
    "7bdbf41a-8b53-4d71-ba7a-ebcc172d8430",
    "25badfda-ee10-490f-9007-aeb412118a43",
    "25badfda-ee10-490f-9007-aeb412118a43-notation-slide",
    "8b0725c7-1a6e-4d1d-afdb-7540f8a4f4f8",
):
    cell = by_id[cell_id]
    tags = cell.setdefault("metadata", {}).setdefault("tags", [])
    if "remove-cell" not in tags:
        tags.append("remove-cell")
    cell["source"] = []

# Removing the duplicated illustrated matrix makes the payoff plane Figure 10.1.
for cell_id, old, new in (
    ("25badfda-ee10-490f-9007-aeb412118a43", "2", "1"),
    ("25badfda-ee10-490f-9007-aeb412118a43-notation-slide", "2", "1"),
    ("5cddb19c", "3", "2"),
    ("23b5f14b-0e4a-4022-aac7-58f12afc629a", "4", "3"),
    ("23b5f14b-0e4a-4022-aac7-58f12afc629a-notation-slide", "4", "3"),
    ("2adb1aca", "5", "4"),
    ("2adb1aca-notation-slide", "5", "4"),
    ("09fa3a4f", "6", "5"),
    ("58cc6953-ea1f-4aa3-a62a-84db0c251324", "7", "6"),
):
    cell = by_id[cell_id]
    source = "".join(cell.get("source", []))
    source = source.replace(f"fig-w10-{old}", f"fig-w10-{new}")
    source = source.replace(f"Figure 10.{old}", f"Figure 10.{new}")
    cell["source"] = source.splitlines(keepends=True)

# With the unanalysed payoff plane and the illustrated matrix removed, the
# best-response plane is the first numbered figure in the Prisoner's Dilemma.
for cell_id, old, new in (
    ("23b5f14b-0e4a-4022-aac7-58f12afc629a", "3", "1"),
    ("23b5f14b-0e4a-4022-aac7-58f12afc629a-notation-slide", "3", "1"),
    ("2adb1aca", "4", "2"),
    ("2adb1aca-notation-slide", "4", "2"),
    ("09fa3a4f", "5", "3"),
    ("58cc6953-ea1f-4aa3-a62a-84db0c251324", "6", "4"),
):
    cell = by_id[cell_id]
    source = "".join(cell.get("source", []))
    source = source.replace(f"fig-w10-{old}", f"fig-w10-{new}")
    source = source.replace(f"Figure 10.{old}", f"Figure 10.{new}")
    cell["source"] = source.splitlines(keepends=True)

# Keep the entire formal specification together, before behavioural assumptions.
ordered_ids = [
    "d9bf6664",
    "66c07965-eb0d-4b59-8c59-fb65f6caf6e0",
    "8309b600-a5e3-4836-853a-d685bf85dd2f",
    "185e0fc7-41d0-47a3-b5e9-cdedc9619297",
    "185e0fc7-41d0-47a3-b5e9-cdedc9619297-notation-slide",
    "e190c160-09b7-46d5-8983-6aa6f397daf4",
    "e190c160-09b7-46d5-8983-6aa6f397daf4-notation-slide",
    "f95edecc",
    "c1cd393a-fb79-4969-886d-91559cef052a",
    "5bae5727-5f69-4a88-8374-011f404fd785",
    "a7aa8aa3",
    "1c3345d1-ec3e-4ed8-9ee5-3d1a9a8dcbe4",
    "8c417d1a-1188-4e62-9112-014e89519f9f",
    "7bdbf41a-8b53-4d71-ba7a-ebcc172d8430",
]

first = min(i for i, cell in enumerate(cells) if cell["id"] in ordered_ids)
remaining = [cell for cell in cells if cell["id"] not in ordered_ids]
notebook["cells"] = remaining[:first] + [by_id[cell_id] for cell_id in ordered_ids] + remaining[first:]

# Teach normal-form analysis as a repeatable navigation procedure before naming
# dominance and Nash equilibrium formally.
cells = notebook["cells"]
analysis_ids = [
    "20f32550-7878-493e-bd45-ffd7f5de6487",
    "b45337ad-0c4a-4ffc-b1b7-3c330bdf79ce",
    "f328572a",
    "5cddb19c",
    "5c9c5f1b-240a-40d7-af94-04ffc2412d2e",
    "4c60edf4-5607-4ff8-a279-e6770d3a517b",
    "e902a40e-5ac1-4db4-ad7c-a606d1f0f688",
    "894680c8-6d78-4117-b994-6b42b5c64ffe",
    "158d453b-9b8e-4425-bc1f-ff9552462e97",
    "b091f920-71fa-423d-bcca-802cdfc18199",
    "b091f920-71fa-423d-bcca-802cdfc18199-notation-slide",
    "f733ac87-0914-43f0-af38-cab5d6089b72",
]
analysis_by_id = {cell["id"]: cell for cell in cells if cell["id"] in analysis_ids}
analysis_first = min(i for i, cell in enumerate(cells) if cell["id"] in analysis_ids)
analysis_remaining = [cell for cell in cells if cell["id"] not in analysis_ids]
notebook["cells"] = (
    analysis_remaining[:analysis_first]
    + [analysis_by_id[cell_id] for cell_id in analysis_ids]
    + analysis_remaining[analysis_first:]
)

PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")
