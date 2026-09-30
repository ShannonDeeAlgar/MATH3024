"""Clarify pairwise outcomes in the Week 10 lizard RPS example."""

from __future__ import annotations

import json
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "notebooks/week10/L_Game_theory.ipynb"


READER = r'''### A biological rock–paper–scissors game

Male side-blotched lizards (*Uta stansburiana*) have three throat-colour types, or morphs, associated with different mating strategies. In the population studied by [Sinervo and Lively (1996)](https://doi.org/10.1038/380240a0):

- Orange males defend large territories and displace blue males.
- Blue males guard mates closely and prevent yellow males from sneaking matings.
- Yellow males mimic females and sneak matings within orange males’ territories.

This gives the cycle:

| Pair of morphs | Higher expected mating success | Why |
|---|---|---|
| Orange and blue | Orange | Orange males can displace blue males. |
| Blue and yellow | Blue | Blue males guard mates from yellow males. |
| Yellow and orange | Yellow | Yellow males can sneak matings in orange territories. |

Here “wins” means greater expected reproductive success in that matchup, not that one lizard wins every encounter. The payoff is the number of offspring sired, and it depends on which morphs are common. The simplified cycle is orange → blue → yellow → orange, so no morph has an advantage against all the others.

| Game element | Biological meaning |
|---|---|
| **Players** | Competing male side-blotched lizards |
| **Strategies** | Territory defence, mate guarding or sneaking, associated with throat-colour morphs |
| **Payoff** | Number of offspring sired, depending on the other males' strategies |


<div style="position:relative;overflow:hidden;width:320px;max-width:100%;aspect-ratio:208/159;margin:1rem auto 0.4rem;"><img src="images/sinervo-morphs-source.jpeg" alt="Orange-, blue- and yellow-throated male side-blotched lizards, left to right, photographed from the side and beneath." style="position:absolute;width:250% !important;max-width:none !important;height:auto !important;left:-129.8077%;top:-77.3585%;margin:0 !important;"></div>
<p class="figure-caption">Photo source: Barry Sinervo, Fig. 1D in <a href="https://doi.org/10.1111/evo.14416">Svensson et al. (2022), <em>In Memoriam: Barry Sinervo 1961–2021</em></a>, <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>; displayed crop.</p>

The biological payoffs differ from the hand game's zero-sum scores. Differential reproduction changes morph frequencies across generations. See also [Friedman et al. (2017)](https://doi.org/10.1371/journal.pone.0184052).
'''


SLIDE = r'''### A biological rock–paper–scissors game

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><div class="lizard-photo-anchor"><img src="images/sinervo-morphs-source.jpeg" alt="Orange-, blue- and yellow-throated male side-blotched lizards, left to right."></div><p class="figure-reference">Photo source: Barry Sinervo, Fig. 1D in <a href="https://doi.org/10.1111/evo.14416">Svensson et al. (2022)</a>; <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>; displayed crop.</p></div>
<div class="text-panel"><table style="width:100%;table-layout:fixed"><colgroup><col style="width:30%"><col style="width:70%"></colgroup><thead><tr><th>Pair</th><th>Higher expected reproductive success</th></tr></thead><tbody><tr><td>Orange–blue</td><td>Orange displaces blue.</td></tr><tr><td>Blue–yellow</td><td>Blue guards mates from yellow.</td></tr><tr><td>Yellow–orange</td><td>Yellow sneaks matings in orange territories.</td></tr></tbody></table></div>
</div>

“Wins” means higher expected offspring in that matchup, not a guaranteed victory in every encounter. The cycle is orange → blue → yellow → orange. Reproduction changes morph frequencies across generations.
'''


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cells["w10-lizard-morphs"]["source"] = READER.splitlines(keepends=True)
    cells["w10-real-games-slide"]["source"] = SLIDE.splitlines(keepends=True)
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
