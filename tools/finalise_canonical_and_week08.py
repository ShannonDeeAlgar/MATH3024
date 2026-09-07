#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCES = {
    "week01": {
        "### Schelling segregation": "**Original source:** Schelling, T. C. (1971), [Dynamic Models of Segregation](https://doi.org/10.1080/0022250X.1971.9989794).",
        "### Planetary motion": "**Original source:** Newton, I. (1687), *Philosophiæ Naturalis Principia Mathematica*.",
    },
    "week02": {
        "### Cantor set": "**Original source:** Cantor, G. (1883), *Über unendliche, lineare Punktmannigfaltigkeiten V*.",
        "### Sierpiński triangle": "**Original source:** Sierpiński, W. (1915), *Sur une courbe cantorienne qui contient une image biunivoque et continue de toute courbe donnée*.",
    },
    "week03": {
        "## Canonical model at a glance · Gray–Scott reaction–diffusion": "**Original sources:** Gray, P. and Scott, S. K. (1983), [Autocatalytic reactions in the isothermal, continuous stirred tank reactor](https://doi.org/10.1016/0009-2509(83)80132-8); Pearson, J. E. (1993), [Complex patterns in a simple system](https://doi.org/10.1126/science.261.5118.189).",
    },
    "week04": {
        "### Elementary cellular automata": "**Original source:** Wolfram, S. (1983), [Statistical mechanics of cellular automata](https://doi.org/10.1103/RevModPhys.55.601).",
        "### Conway's Game of Life": "**Original source:** Conway’s rule was introduced publicly by Gardner, M. (1970), [Mathematical Games: The fantastic combinations of John Conway’s new solitaire game “Life”](https://doi.org/10.1038/scientificamerican1070-120).",
    },
    "week05": {
        "## Canonical model at a glance · Vicsek model": "**Original source:** Vicsek, T. et al. (1995), [Novel type of phase transition in a system of self-driven particles](https://doi.org/10.1103/PhysRevLett.75.1226).",
    },
    "week06": {
        "## Canonical model at a glance · Kuramoto model": "**Original source:** Kuramoto, Y. (1975), *Self-entrainment of a population of coupled non-linear oscillators*, in *International Symposium on Mathematical Problems in Theoretical Physics*.",
    },
    "week07": {
        "# Canonical models in pseudocode": "**Original sources:** Dorigo, M., Maniezzo, V. and Colorni, A. (1996), [Ant system: optimization by a colony of cooperating agents](https://doi.org/10.1109/3477.484436); Kennedy, J. and Eberhart, R. (1995), [Particle swarm optimization](https://doi.org/10.1109/ICNN.1995.488968).",
    },
    "week09": {
        "## Canonical model at a glance · Shannon communication model": "**Original source:** Shannon, C. E. (1948), [A Mathematical Theory of Communication](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x).",
    },
    "week10": {
        "## Canonical model at a glance · iterated Prisoner’s Dilemma": "**Original source:** Axelrod, R. and Hamilton, W. D. (1981), [The evolution of cooperation](https://doi.org/10.1126/science.7466396).",
    },
}


def src(cell):
    return "".join(cell.get("source", []))


def set_src(cell, text):
    cell["source"] = text.splitlines(keepends=True)


def insert_source(text, marker, citation):
    if citation in text:
        return text
    start = text.find(marker)
    if start < 0:
        return text
    next_heading = text.find("\n### ", start + len(marker))
    pseudo = text.find("\n# Canonical model", start + len(marker))
    ends = [x for x in (next_heading, pseudo) if x >= 0]
    end = min(ends) if ends else len(text)
    return text[:end].rstrip() + "\n\n" + citation + "\n" + text[end:]


for week, entries in SOURCES.items():
    files = list((ROOT / "notebooks" / week).glob("L_*.ipynb"))
    if not files:
        continue
    path = files[0]
    data = json.loads(path.read_text())
    for cell in data["cells"]:
        text = src(cell)
        if "Canonical model" not in text or "at a glance" not in text:
            continue
        for marker, citation in entries.items():
            text = insert_source(text, marker, citation)
        set_src(cell, text)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


# Week 8: retain a short bridge from Week 5, then centre percolation and sandpiles.
path = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"
data = json.loads(path.read_text())
cells = data["cells"]

# Remove the long reprise of the Vicsek transition debate and its detailed finite-size figures.
remove = set(range(3, 18)) | set(range(28, 44))
cells = [c for i, c in enumerate(cells) if i not in remove]

# Replace the opening with a concise bridge that makes Week 8's question explicit.
bridge = {
    "cell_type": "markdown",
    "metadata": {"slideshow": {"slide_type": "slide"}, "tags": ["slides"]},
    "source": [
        "## From collective order to critical behaviour\n",
        "\n",
        "In Week 5, the Vicsek order parameter changed sharply as noise increased. That example motivates the language of phase transitions, but the detailed dispute over the transition belongs with the Vicsek model.\n",
        "\n",
        "This week asks two new questions: what is special about a continuous critical point, and can a system approach critical behaviour without tuning an external control parameter?\n",
    ],
    "id": "w8-brief-vicsek-bridge",
}
insert_at = 3
cells.insert(insert_at, bridge)

# Repair proof/check presentation and mathematical prose.
for cell in cells:
    text = src(cell)
    if "<strong>Proof:</strong>" in text:
        text = (
            '<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Check the scaling">'
            '<span>Verify that rescaling the input of a power law changes its amplitude but not its functional form.</span></div>\n'
        )
    if text.startswith("```{dropdown}\n\nTake a power law"):
        text = text.replace("```{dropdown}\n", "```{dropdown} Show the calculation\n", 1)
    text = text.replace("http://www.complexity-explorables.org/explorables/baristas-secret/", "https://www.complexity-explorables.org/explorables/baristas-secret/")
    text = text.replace("<p>These three initialisations use $p=59.22\\%<p_c$.</p>", "<p>These three initialisations use an occupation probability just below the threshold.</p>")
    text = text.replace("<p>These three initialisations use $p=59.22%<p_c$.</p>", "<p>These three initialisations use an occupation probability just below the threshold.</p>")
    text = text.replace("## A familiar example: the Ising model", "## Supporting comparison · the Ising model")
    set_src(cell, text)

# Replace the sandpile setup and tuning explanation with precise, consistently formatted notation.
for cell in cells:
    text = src(cell)
    if text.startswith("### Bak et. al's model: the details"):
        text = "### Abelian sandpile · model details\n\n**Model type:** two-dimensional cellular automaton.\n"
    elif text.startswith("**state of each cell"):
        text = "**State:** $z_{ij}$ is the integer number of grains stored at lattice site $(i,j)$.\n"
    elif text.startswith("**boundary of grid"):
        text = "**Boundary:** open edges dissipate grains that leave the lattice. This loss balances the slow addition of grains.\n"
    elif text.startswith("**dynamics**:"):
        text = """**Dynamics:** add one grain at a chosen site. A site is unstable when $z_{ij}\\ge z_c$. On the square lattice we use $z_c=4$ and the toppling rule

$$
z_{ij} \\mapsto z_{ij}-4,
$$

$$
z_{i\\pm1,j} \\mapsto z_{i\\pm1,j}+1,
$$

$$
z_{i,j\\pm1} \\mapsto z_{i,j\\pm1}+1.
$$

Continue legal topplings until every site is stable, then add the next grain. The separation between slow driving and rapid relaxation is part of the model, not a plotting choice.
"""
    elif "Why is setting $K_c$" in text:
        text = text.replace("$K_c$", "$z_c$")
    elif text.startswith("```{dropdown}\nWe set $K_c$"):
        text = """```{dropdown} My answer
The occupation probability <i>p</i> in percolation is a control parameter: changing it moves the system towards or away from the percolation threshold <i>p</i><sub>c</sub>. The sandpile threshold <i>z</i><sub>c</sub> defines when one local update occurs. With slow driving, conservative redistribution in the interior and dissipation at the boundary, the model repeatedly approaches marginally stable configurations without an experimenter tuning a control parameter to one special value.

This does not mean that every threshold rule produces the same critical behaviour. Changing the lattice, redistribution rule, driving or dissipation can change the model and sometimes its scaling class.
```
"""
    set_src(cell, text)

# Canonical summary: percolation and Abelian sandpile are the two carried models.
for cell in cells:
    text = src(cell)
    if text.startswith("## Canonical models at a glance"):
        ising_start = text.find("### Ising model")
        perc_start = text.find("### Site percolation")
        if ising_start >= 0 and perc_start >= 0:
            text = "## Canonical models at a glance · site percolation and Abelian sandpile\n\n" + text[perc_start:]
        text = text.replace(
            "**Outputs:** clusters, spanning events and finite-size scaling summaries.\n",
            "**Outputs:** clusters, spanning events and finite-size scaling summaries.\n\n**Original source:** Broadbent, S. R. and Hammersley, J. M. (1957), [Percolation processes I. Crystals and mazes](https://doi.org/10.1017/S0305004100032680).\n",
        )
        text = text.replace(
            "**Outputs:** stable states and avalanche size, area and duration.\n",
            "**Outputs:** stable states and avalanche size, area and duration.\n\n**Original sources:** Bak, P., Tang, C. and Wiesenfeld, K. (1987), [Self-organized criticality: an explanation of 1/f noise](https://doi.org/10.1103/PhysRevLett.59.381); Dhar, D. (1990), [Self-organized critical state of sandpile automaton models](https://doi.org/10.1103/PhysRevLett.64.1613), which established the Abelian formulation.\n",
        )
        # Remove the Ising pseudocode and fix the introductory sentence.
        a = text.find("## Ising model: one Monte Carlo sweep")
        b = text.find("## Site percolation", a)
        if a >= 0 and b >= 0:
            text = text[:a] + text[b:]
        text = text.replace(
            "Critical phenomena use different computational clocks. The Ising model samples proposed events; percolation constructs a random configuration; the sandpile processes an event queue until the system is stable.",
            "The two models use different computational clocks. Percolation constructs one random configuration; the sandpile alternates slow driving with complete relaxation back to stability.",
        )
        set_src(cell, text)

data["cells"] = cells
path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
