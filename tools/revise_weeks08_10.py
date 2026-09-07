"""Targeted structural and formatting revisions for Weeks 8 and 10."""

from copy import deepcopy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    with path.open() as f:
        return json.load(f)


def save(path, data):
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")


def src(cell):
    value = cell.get("source", [])
    return value if isinstance(value, str) else "".join(value)


def set_src(cell, text):
    cell["source"] = text


def find(cells, needle):
    return next(i for i, cell in enumerate(cells) if needle in src(cell))


def markdown(text, slide_type=""):
    meta = {}
    if slide_type:
        meta["slideshow"] = {"slide_type": slide_type}
    return {"cell_type": "markdown", "metadata": meta, "source": text}


def revise_week08():
    path = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"
    data = load(path)
    cells = data["cells"]

    i = find(cells, "Downey reports box-counting estimates")
    set_src(cells[i], """<div class=\"discussion-marker\"><img src=\"images/discussion_marker.svg\" alt=\"Check the estimate\"><span>A box-counting estimate for a subset of a two-dimensional image is greater than 2. What does that tell us about the calculation?</span></div>

```{dropdown} Show the dimension bound
For any subset of $\\mathbb{R}^2$, both its box-counting dimension and Hausdorff dimension are bounded by the dimension of the surrounding plane:

$$
0 \\leq D \\leq 2.
$$

An estimate above 2 is therefore a diagnostic of an unsuitable scale range, an implementation error, or a mismatch between the quantity counted and the dimension claimed. It is not evidence of an unusually complicated planar set.
```
""")
    # The following anonymous dropdown repeated the same bound.
    cells[find(cells, "For a subset of $\\mathbb{R}^2$")]["metadata"].setdefault("tags", []).append("remove-cell")

    i = find(cells, "A sandpile doesn’t form a perfect square")
    set_src(cells[i], """<div class=\"discussion-marker\"><img src=\"images/discussion_marker.svg\" alt=\"Discussion prompt\"><span>Suppose grains occupied independently chosen sites with a non-zero limiting area fraction. What box-counting dimension would you expect?</span></div>""")
    i = find(cells, "For a random (i.i.d.) distribution")
    set_src(cells[i], """```{dropdown} Show the reasoning
For an independent random occupation with a non-zero limiting area fraction, the occupied set fills the plane statistically and has box-counting dimension $D=2$.

A value below 2 requires a set that becomes sparse as resolution increases, such as a curve, a critical cluster boundary, or another set with zero area. Visual roughness alone does not imply a non-integer dimension.
```
""")

    i = find(cells, "Alter the state transition scenarios")
    set_src(cells[i], """<div class=\"discussion-marker\"><img src=\"images/discussion_marker.svg\" alt=\"Discussion prompt\"><span>How would the mean-field transition probabilities change for Conway’s B3/S23 rule?</span></div>""")
    i = find(cells, "Within a sand pile model, large avalanches occur")
    set_src(cells[i], """```{dropdown} Two levels of explanation
The added grain is the immediate trigger: without it, that avalanche would not begin at that moment.

The slowly driven, marginally stable state explains why one grain can sometimes trigger a system-wide cascade. The same-sized perturbation can therefore produce no toppling, a small event, or a large avalanche.
```
""")

    replacements = {
        "images/Downey_sand_fractals.png": "images/sandpile_height_subsets.png",
        "images/Downey_sand_fractals_box_counting.png": "images/sandpile_box_counting.png",
        "images/Downey_sand_avalanche_quantified_linear.png": "images/sandpile_avalanche_distributions.png",
        "images/Downey_sand_power_spectra.png": "images/sandpile_activity_spectrum.png",
    }
    for cell in cells:
        text = src(cell)
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = text.replace("Image from <a href=\"https://greenteapress.com/wp-content/uploads/2017/03/thinkcomplexity2.pdf\">Allen Downey's <em>Think Complexity</em></a>.", "Generated from the Abelian sandpile implementation used in this unit.")
        text = text.replace("Image from [Allen Downey's Think Complexity](https://greenteapress.com/wp/think-complexity-2e/) (he also provides code).", "Generated from the Abelian sandpile implementation used in this unit.")
        set_src(cell, text)
    # The old separate log-axis image is superseded by the two-panel course figure.
    for cell in cells:
        if "Downey_sand_avalanche_quantified_log.png" in src(cell):
            cell["metadata"].setdefault("tags", []).append("remove-cell")

    save(path, data)


def revise_week10():
    path = ROOT / "notebooks/week10/L_Game_theory.ipynb"
    data = load(path)
    cells = data["cells"]

    i = find(cells, "Moving rock, paper and scissors agents")
    text = src(cells[i]).replace(
        "Moving rock, paper and scissors agents convert one another on contact. The local payoff rule is cyclic: each type beats one and loses to one.",
        "Rock–paper–scissors is a game in the game-theoretic sense: each strategy defeats one alternative and loses to the other. This simulation adds agents, movement and conversion on contact to that cyclic payoff rule."
    )
    set_src(cells[i], text)

    explorable_i = find(cells, "The Prisoner's Kaleidoscope")
    explorable = deepcopy(cells[explorable_i])
    cells[explorable_i]["metadata"].setdefault("tags", []).append("remove-cell")

    i = find(cells, "A \"game\" is not about entertainment")
    set_src(cells[i], """## Games

A game is a representation of strategic decisions: the outcome for each player depends on what all players do.

The model specifies

$$
G=(P,\\{A_i\\}_{i=1}^{n},\\{u_i\\}_{i=1}^{n}),
$$

where $P$ is the set of players, $A_i$ is player $i$’s action set, and $u_i$ assigns that player a payoff to every action profile.
""")

    i = find(cells, "'Unilaterally'")
    set_src(cells[i], """“Unilaterally” means that a player changes only their own action while the actions of everyone else remain fixed.

After a Nash equilibrium has been played, no player could obtain a higher payoff by changing their action alone.
""")
    j = find(cells, "Let the actions of $p_1$")
    set_src(cells[j], """Let $A_1$ and $A_2$ be the players’ action sets. An action profile $(a_1^*,a_2^*)$ is a Nash equilibrium when

$$
u_1(a_1^*,a_2^*) \\geq u_1(a_1,a_2^*)
\\qquad \\text{for every } a_1\\in A_1,
$$

and


$$
u_2(a_1^*,a_2^*) \\geq u_2(a_1^*,a_2)
\\qquad \\text{for every } a_2\\in A_2.
$$
""")
    cells[j]["metadata"].get("slideshow", {})["slide_type"] = ""

    i = find(cells, "## Frame the Prisoner’s Dilemma as a game")
    set_src(cells[i], """## Frame the Prisoner’s Dilemma as a game

| Component | Specification |
|---|---|
| Players | $P=\\{p_1,p_2\\}$ |
| Actions | $A_1=A_2=\\{C,D\\}$ |
| Utilities | $u_i(a_1,a_2)$ is the negative prison sentence, so a less negative value is better. |
""")

    i = find(cells, "## Payoff structure")
    set_src(cells[i], """## Payoff structure

Using negative years in prison as utility gives

$$
\\begin{aligned}
u_1(D,C)&=0, & u_1(C,D)&=-3, & u_1(D,D)&=-2, & u_1(C,C)&=-1,\\\\
u_2(C,D)&=0, & u_2(D,C)&=-3, & u_2(D,D)&=-2, & u_2(C,C)&=-1.
\\end{aligned}
$$

Higher utility now consistently means a better outcome. The same game can instead be written with positive years in prison, but then the players minimise cost rather than maximise utility.
""")

    atlas_i = find(cells, "## The Prisoner’s Dilemma is one 2 × 2 game")
    guide = markdown("""## Read a $2\\times2$ payoff table

Player 1 chooses a row and Player 2 chooses a column. The selected cell contains the ordered pair

$$
(\\text{Player 1 payoff},\\;\\text{Player 2 payoff}).
$$

| Example | Selected actions | Read the entry | Strategic feature |
|---|---|---|---|
| Prisoner’s Dilemma | Player 1 defects; Player 2 cooperates | $(0,-3)$: Player 1 goes free and Player 2 serves three years | Defection is individually tempting even though mutual cooperation is collectively better than mutual defection. |
| Coordination game | Both select the same convention | A diagonal entry gives both players the larger payoff | Two equilibria exist; the problem is agreeing which one to use. |
| Matching pennies | Player 1 wants a match; Player 2 wants a mismatch | Improving one player’s payoff worsens the other’s | No pure-action Nash equilibrium exists. |

Large atlases of $2\\times2$ games repeat this same reading procedure. What changes is the ordering of the four payoff pairs.
""", "subslide")
    cells.insert(atlas_i, guide)
    # Place the spatial explorable only after the Prisoner's Dilemma has been defined and read.
    cells.insert(atlas_i + 1, explorable)

    save(path, data)


def revise_week09():
    path = ROOT / "notebooks/week09/L_InformationTheory.ipynb"
    data = load(path)
    cells = data["cells"]

    # Introduce the two-outcome case before generalising with the widget.
    binary_i = find(cells, "## Binary entropy")
    binary = cells.pop(binary_i)
    widget_i = find(cells, "## Explore parameterised distributions")
    cells.insert(widget_i, binary)
    set_src(binary, """## Binary entropy

<img src=\"images/Binary_entropy_plot.png\" alt=\"Binary entropy as a function of probability\" style=\"display:block;max-height:360px;margin:0 auto\">

A binary variable has probabilities $p$ and $1-p$.

$$
H_2(p)=-p\\log_2p-(1-p)\\log_2(1-p).
$$

The entropy is zero when the outcome is certain and reaches one bit at $p=1/2$.
""")

    i = find(cells, "We need to be clear about what variable")
    set_src(cells[i], """```{dropdown} Show the comparison
The answer depends on the variable being measured.

For heading angles at one instant, $H(\\Theta)$ is high for both random motion and rotational milling because headings cover the circle. It is low for a strongly polarised group.

For the angular momentum of the whole group, $H(L)$ distinguishes the two cases: persistent milling concentrates $L$ near a non-zero value, whereas random motion fluctuates around zero.

Entropy is therefore not a label attached to a system. It summarises a stated random variable and representation.
```
""")

    i = find(cells, "## Information measures in research")
    set_src(cells[i], """## Information measures in research

| Measure | Mathematical form | What it asks | Research example |
|---|---|---|---|
| Entropy rate | $h_\\mu=\\lim_{n\\to\\infty}H(X_n\\mid X_1,\\ldots,X_{n-1})$ | How much new uncertainty arrives per observation? | Neural spike trains: [Strong et al. (1998)](https://doi.org/10.1103/PhysRevLett.80.197). |
| Mutual information | $I(X;Y)=\\sum p(x,y)\\log_2\\!\\frac{p(x,y)}{p(x)p(y)}$ | How much does one variable tell us about another? | Neural coding and stimulus reconstruction in Strong et al. (1998). |
| Permutation entropy | $H_{\\mathrm{perm}}=-\\sum_\\pi p(\\pi)\\log_2p(\\pi)$ | How diverse are the ordinal patterns in a time series? | [Bandt and Pompe (2002)](https://doi.org/10.1103/PhysRevLett.88.174102). |
| Transfer entropy | $T_{X\\to Y}=I(X_t;Y_{t+1}\\mid Y_t)$ | Does the past of $X$ improve prediction of $Y$ beyond the past of $Y$? | Leader–follower inference in zebrafish: [Butail, Mwaffo and Porfiri (2016)](https://doi.org/10.1103/PhysRevE.93.042411). |
| Statistical complexity | $C_\\mu=H(S)$ for predictive causal states $S$ | How much stored information is needed for optimal prediction? | [Crutchfield and Young (1989)](https://doi.org/10.1103/PhysRevLett.63.105). |

Transfer entropy and the other extensions below are optional project tools, not directly assessed. They require careful choices about time lag, sampling, conditioning variables and estimation. Directional predictive information is not, by itself, proof of causation.
""")

    # Keep the worked examples together under the research banner.
    for old, new in {
        "## Time series analysis": "### Time-series measures",
        "### Permutation Entropy": "### Permutation entropy",
        "## Permutation entropy: a small example": "### Permutation entropy: a small example",
        "### Transfer entropy": "### Transfer entropy",
    }.items():
        for cell in cells:
            if old in src(cell):
                set_src(cell, src(cell).replace(old, new))

    # Remove stray emphasis while retaining genuine term definitions and mini-headings.
    substitutions = {
        "**Fair die**": "Fair die",
        "**Loaded die**": "Loaded die",
        "**Details**": "Details",
        "**low** $H$": "Low $H$",
        "**high** $H$": "High $H$",
        "**Maximum entropy**": "Maximum entropy",
        "**Normalisation**": "Normalisation",
    }
    for cell in cells:
        text = src(cell)
        for old, new in substitutions.items():
            text = text.replace(old, new)
        set_src(cell, text)

    save(path, data)


if __name__ == "__main__":
    revise_week08()
    revise_week09()
    revise_week10()
