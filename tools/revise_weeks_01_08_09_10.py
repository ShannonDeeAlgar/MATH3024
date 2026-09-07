#!/usr/bin/env python3
"""Focused editorial revision for Weeks 1, 8, 9 and 10."""

from __future__ import annotations

import json
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(rel: str):
    path = ROOT / rel
    return path, json.loads(path.read_text())


def save(path: Path, nb: dict):
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


def md(source: str, *, cell_id: str | None = None, slide: str = ""):
    metadata = {}
    if slide:
        metadata["slideshow"] = {"slide_type": slide}
    return {
        "cell_type": "markdown",
        "id": cell_id or uuid.uuid4().hex[:8],
        "metadata": metadata,
        "source": source.strip() + "\n",
    }


def code(source: str, *, cell_id: str | None = None):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id or uuid.uuid4().hex[:8],
        "metadata": {},
        "outputs": [],
        "source": source.strip() + "\n",
    }


def find(cells, text):
    return next(i for i, c in enumerate(cells) if text in "".join(c.get("source", "")))


def revise_week01():
    path, nb = load("notebooks/week01/L_Introduction_to_complex_systems.ipynb")
    cells = nb["cells"]
    i = find(cells, "## Canonical models at a glance · Schelling segregation and planetary motion")
    src = "".join(cells[i]["source"])
    src = src.replace("### Planetary motion", "#### Pseudocode: Schelling segregation\n\n" +
        "```text\nINITIALISE a grid of agents and empty sites\nREPEAT until the stopping rule is met:\n    identify agents below the similarity threshold\n    visit those agents in a stated order\n    move each one to an allowed empty site\n    record segregation and movement summaries\nEND REPEAT\n```\n\n### Planetary motion", 1)
    marker = "# Canonical models in pseudocode"
    if marker in src:
        tail = src.split(marker, 1)[1]
        # Retain only the planetary algorithm from the old detached block.
        if "### Planetary motion" in tail:
            planet = tail.split("### Planetary motion", 1)[1].strip()
            src = src.split(marker, 1)[0].rstrip() + "\n\n#### Pseudocode: planetary motion\n\n" + planet + "\n"
        else:
            src = src.split(marker, 1)[0].rstrip() + "\n"
    cells[i]["source"] = src
    save(path, nb)


def revise_week08_workshop():
    path, old = load("notebooks/week08/WS_Critical_phenomena.ipynb")
    cells = [
        md("""
# Week 8 workshop · Avalanches and finite systems

This workshop uses the Abelian sandpile to investigate how a finite simulation can support, or weaken, a claim about scale-free behaviour.
""", cell_id="w8-title"),
        md("""
## Two objectives, one investigation

**Canonical model:** Abelian sandpile.  
**Modelling practice:** finite-size effects and defensible scaling ranges.

You will implement the local toppling rule, measure avalanche sizes, repeat the experiment, and compare more than one lattice size. The definitions of criticality, power laws and self-organised criticality belong in the lecture and Reader; here we use them.
""", cell_id="w8-objectives"),
        md("""
# Build the sandpile

Each site stores an integer height. Add one grain at a randomly selected site. Whenever a site reaches the threshold, it loses four grains and gives one to each edge-sharing neighbour. Grains sent beyond the open boundary leave the system.

The order in which unstable sites are processed does not change the final stable state. That is the **Abelian** property.
""", cell_id="w8-build"),
        code("""
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

rng = np.random.default_rng(3024)

def add_grain_and_relax(pile, rng):
    # Add one grain; return avalanche size and number of parallel relaxation steps.
    L = pile.shape[0]
    i, j = rng.integers(0, L, size=2)
    pile[i, j] += 1
    queue = deque([(i, j)]) if pile[i, j] >= 4 else deque()
    topplings = 0
    waves = 0
    while queue:
        waves += 1
        for _ in range(len(queue)):
            x, y = queue.popleft()
            while pile[x, y] >= 4:
                pile[x, y] -= 4
                topplings += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    u, v = x + dx, y + dy
                    if 0 <= u < L and 0 <= v < L:
                        pile[u, v] += 1
                        if pile[u, v] >= 4:
                            queue.append((u, v))
    return topplings, waves

def run_sandpile(L=32, additions=30_000, burn_in=8_000, seed=3024):
    local_rng = np.random.default_rng(seed)
    pile = np.zeros((L, L), dtype=int)
    sizes, durations = [], []
    for step in range(additions):
        size, duration = add_grain_and_relax(pile, local_rng)
        if step >= burn_in and size > 0:
            sizes.append(size)
            durations.append(duration)
    return pile, np.asarray(sizes), np.asarray(durations)
""", cell_id="w8-code"),
        md("""
## Check the local rule

Run a modest system first. Inspect the final height field and verify that every site is stable. This is a code check, not yet evidence of criticality.
""", cell_id="w8-check"),
        code("""
pile, sizes, durations = run_sandpile(L=32, additions=25_000, burn_in=6_000)
assert pile.max() < 4

fig, ax = plt.subplots(figsize=(5.5, 4.5))
im = ax.imshow(pile, cmap="viridis", vmin=0, vmax=3)
ax.set(title="Stable sandpile after repeated driving", xlabel="Column", ylabel="Row")
fig.colorbar(im, ax=ax, label="Height")
plt.show()

print(f"Recorded {len(sizes):,} non-zero avalanches")
""", cell_id="w8-check-code"),
        md("""
# Measure avalanches

The avalanche size $S$ is the number of topplings caused by one added grain. A complementary duration measure counts parallel relaxation steps. Plot the full distribution before fitting anything.
""", cell_id="w8-measure"),
        code("""
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(sizes, bins=50, color="#20345b")
axes[0].set(xlabel="Avalanche size, S", ylabel="Count", title="Linear axes")

bins = np.logspace(0, np.log10(max(sizes.max(), 2)), 28)
axes[1].hist(sizes, bins=bins, color="#20345b")
axes[1].set(xscale="log", yscale="log", xlabel="Avalanche size, S", ylabel="Count", title="The same data on log–log axes")
plt.tight_layout()
plt.show()
""", cell_id="w8-distribution"),
        md("""
## Do not fit the whole picture blindly

Choose a candidate scaling range and state it. The smallest events are strongly discrete; the largest events are constrained by the finite lattice. Compare at least two defensible ranges rather than selecting the straightest-looking segment after seeing the result.
""", cell_id="w8-range"),
        code("""
def log_binned_counts(values, bins=24):
    edges = np.logspace(0, np.log10(values.max()), bins + 1)
    counts, edges = np.histogram(values, bins=edges)
    centres = np.sqrt(edges[:-1] * edges[1:])
    keep = counts > 0
    return centres[keep], counts[keep]

def fit_log_slope(values, lower, upper):
    x, y = log_binned_counts(values)
    keep = (x >= lower) & (x <= upper)
    slope, intercept = np.polyfit(np.log10(x[keep]), np.log10(y[keep]), 1)
    return slope, intercept, x, y, keep

for lower, upper in [(3, 80), (8, 180)]:
    slope, *_ = fit_log_slope(sizes, lower, upper)
    print(f"range {lower:>3}–{upper:<3}: fitted slope {slope:.3f}")
""", cell_id="w8-fit"),
        md("""
# Compare finite systems

A cutoff that moves when the lattice size changes is a finite-size effect, not a characteristic avalanche scale of an infinite system. Repeat the same procedure for at least two values of $L$. Keep the driving, burn-in rule, binning, and fitting rule visible.
""", cell_id="w8-finite"),
        code("""
results = {}
for L, additions, burn_in in [(24, 22_000, 5_000), (48, 45_000, 10_000)]:
    _, sample, _ = run_sandpile(L=L, additions=additions, burn_in=burn_in, seed=3024 + L)
    results[L] = sample

fig, ax = plt.subplots(figsize=(7, 4.8))
for L, sample in results.items():
    x, y = log_binned_counts(sample)
    ax.plot(x, y / y.sum(), marker="o", ms=4, lw=1.4, label=f"L={L}")
ax.set(xscale="log", yscale="log", xlabel="Avalanche size, S", ylabel="Relative binned count")
ax.legend(title="Lattice width")
plt.show()
""", cell_id="w8-finite-code"),
        md("""
## Modelling decision

Which conclusion survives both the fitting-range change and the system-size change? Report the range of avalanche sizes actually supported by the simulation. A heavy tail over a finite range is a defensible observation; an exact asymptotic power law requires stronger evidence.
""", cell_id="w8-decision"),
        md("""
# Further investigation

Choose one extension:

- compare avalanche size with duration;
- change the boundary condition and explain what physical system it represents;
- compare two burn-in lengths;
- estimate uncertainty by repeating independent runs;
- increase $L$ while keeping a record of runtime and event count.

Your conclusion should distinguish a change in the model from a change in the measurement procedure.
""", cell_id="w8-extension"),
        md("""
# Take-away

The local toppling rule is simple. The empirical scaling claim is not. It depends on equilibration, event definition, sample size, fitting range and the finite lattice.
""", cell_id="w8-takeaway"),
    ]
    old["cells"] = cells
    save(path, old)


def revise_week09():
    path, nb = load("notebooks/week09/L_InformationTheory.ipynb")
    cells = nb["cells"]

    cells[0]["source"] = """# Information Theory
## MATH3024 · Week 9

<div class="canonical-model-marker"><span>Core measures</span><strong>Shannon entropy and mutual information</strong></div>

<div class="modelling-practice-marker"><span>Modelling practice</span><strong>What a summary retains and discards</strong></div>
"""

    i = find(cells, "## Measures used so far")
    cells[i]["source"] = """## Measures used so far

We have already compressed complex behaviour in several different ways.

| Measure | What it retained |
|---|---|
| Local state and event counts | who moved, toppled, survived, or changed state |
| Ensemble mean and spread | typical behaviour and run-to-run variability |
| Mean-square displacement | the spreading rate of many random trajectories |
| Fractal dimension and scaling exponents | how measured structure changes with scale |
| Order parameters | collective alignment, synchrony, or occupancy |
| Correlations and fitted transition locations | dependence and changes between regimes |
| Distributions and tail summaries | the frequency of small and large events |

These are not interchangeable. Each keeps one aspect of the data and discards others. Information theory gives us measures of uncertainty, dependence and information flow, but the same representational question remains.
"""

    i = find(cells, "# Model details")
    cells[i]["source"] = "# Core measures\n"

    for c in cells:
        src = "".join(c.get("source", ""))
        if "more probable events are less surprising ($h(x)\\propto 1/P(x)$)" in src:
            src = src.replace(
                "more probable events are less surprising ($h(x)\\propto 1/P(x)$)",
                "more probable events are less surprising: if $P(x_1)>P(x_2)$, then $h(x_1)<h(x_2)$",
            )
            c["source"] = src

    i = find(cells, "Test your understanding:")
    cells[i]["source"] = """<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Assuming both devices are fair, which has higher entropy: one coin toss or one roll of a six-sided die?</span></div>
"""
    j = find(cells, "Rolling a die has higher entropy")
    cells[j]["source"] = """```{dropdown} My answer
A fair coin has $H=\log_2 2=1$ bit. A fair six-sided die has

$$
H=\log_2 6\approx 2.585\text{ bits}.
$$

The die has higher entropy because one observation must distinguish among six equally likely outcomes rather than two. Fairness and independence are part of the comparison.
```
"""

    # Insert an explicit interactive distribution before binary entropy.
    k = find(cells, "## Binary entropy")
    explorer = md("""
## Explore a distribution

Entropy belongs to a probability distribution, not to the name of a system. Adjust the four outcome weights below. The widget normalises them to probabilities and updates Shannon entropy in bits.

<iframe src="entropy_distribution_explorer.html" title="Interactive Shannon entropy explorer" style="width:100%;height:520px;border:1px solid #c9d3e4;border-radius:8px;background:white"></iframe>

Notice that entropy is largest at the uniform distribution and falls as probability concentrates on fewer outcomes.
""", cell_id="w9-distribution-explorer", slide="subslide")
    if not any(c.get("id") == explorer["id"] for c in cells):
        cells.insert(k, explorer)

    # Add research examples immediately after the Applications introduction.
    k = find(cells, "## Applications") + 1
    research = md("""
## Information measures in research

| Research question | Measure and example |
|---|---|
| How much visual information is carried by a neural spike train? | Entropy rate and mutual information in fly visual neurons: [Strong et al. (1998)](https://doi.org/10.1103/PhysRevLett.80.197). |
| Which subsystem is driving another through time? | Transfer entropy separates directed influence from shared history: [Schreiber (2000)](https://doi.org/10.1103/PhysRevLett.85.461). |
| Can irregular time series be compared without choosing amplitude bins? | Permutation entropy uses the frequencies of ordinal patterns: [Bandt and Pompe (2002)](https://doi.org/10.1103/PhysRevLett.88.174102). |
| Why is randomness not the same thing as complexity? | Statistical complexity complements entropy by retaining predictive structure: [Crutchfield and Young (1989)](https://doi.org/10.1103/PhysRevLett.63.105). |

The measure follows the question. High entropy can mean broad uncertainty while saying very little about memory, causal direction, or organised structure.
""", cell_id="w9-research-examples", slide="subslide")
    if not any(c.get("id") == research["id"] for c in cells):
        cells.insert(k, research)

    i = find(cells, "## Canonical model at a glance · Shannon communication model")
    cells[i]["source"] = """## Information measures at a glance · Shannon entropy

**Object being summarised:** a stated discrete random variable or observed symbol sequence.  
**Representation:** outcomes and their probabilities; changing bins, symbols, blocks, or time windows changes the question.  
**Measure:** $H(X)=-\sum_x p(x)\log_2 p(x)$.  
**Units:** bits when the logarithm has base 2.  
**Reference cases:** $H=0$ for a certain outcome; $H=\log_2 k$ for $k$ equally likely outcomes.  
**What it retains:** average uncertainty in the chosen outcomes.  
**What it discards:** labels, temporal ordering, spatial arrangement, and mechanism unless they are included in the representation.  
**Checks:** probabilities sum to one; zero-probability terms contribute zero; estimates are tested against sample size and alternative representations.

**Original source:** Shannon, C. E. (1948), [A Mathematical Theory of Communication](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x).

Week 9 is deliberately a measures week rather than another canonical-model week. The executable calculation belongs in the workshop, but entropy itself is not a dynamical model of the system that generated the observations.
"""
    save(path, nb)


def revise_week09_workshop():
    path, nb = load("notebooks/week09/WS_Information_theory.ipynb")
    cells = [
        md("""
# Week 9 workshop · What does entropy retain?

This shorter workshop calculates Shannon entropy for known distributions and then applies it to letter sequences from two public-domain books.
""", cell_id="w9w-title"),
        md("""
## Two objectives, one investigation

**Core measure:** Shannon entropy.  
**Modelling practice:** representation determines what a summary can retain.

You will check the calculation on distributions with known answers, estimate probabilities from text, and compare single-letter with short-block descriptions.
""", cell_id="w9w-objectives"),
        code("""
from collections import Counter
from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt

def shannon_entropy(probabilities):
    p = np.asarray(probabilities, dtype=float)
    p = p[p > 0]
    p = p / p.sum()
    return -np.sum(p * np.log2(p))

assert np.isclose(shannon_entropy([1, 0]), 0)
assert np.isclose(shannon_entropy([0.5, 0.5]), 1)
assert np.isclose(shannon_entropy(np.ones(6)), np.log2(6))
""", cell_id="w9w-function"),
        md("""
# Begin with distributions

Compare a certain outcome, a fair coin, a loaded coin, and a fair die. Plot the probabilities beside their entropy values. The graph makes clear that entropy depends on the whole distribution, not simply the number of named outcomes.
""", cell_id="w9w-distributions"),
        code("""
distributions = {
    "certain": np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    "fair coin": np.array([0.5, 0.5, 0, 0, 0, 0]),
    "loaded coin": np.array([0.9, 0.1, 0, 0, 0, 0]),
    "fair die": np.ones(6) / 6,
}

fig, axes = plt.subplots(1, 4, figsize=(12, 3.2), sharey=True)
for ax, (name, p) in zip(axes, distributions.items()):
    ax.bar(np.arange(1, 7), p, color="#355c8a")
    ax.set(title=f"{name}\nH={shannon_entropy(p):.3f} bits", xlabel="Outcome", ylim=(0, 1))
axes[0].set_ylabel("Probability")
plt.tight_layout()
plt.show()
""", cell_id="w9w-distribution-plot"),
        md("""
# Estimate a distribution from text

The files are public-domain texts from Project Gutenberg: *Alice's Adventures in Wonderland* (eBook 11) and *Pride and Prejudice* (eBook 1342). We will keep letters only and ignore case. Those are representational choices, not neutral preprocessing.
""", cell_id="w9w-text"),
        code("""
def data_path(filename):
    candidates = [Path("notebooks/week09/data") / filename, Path("data") / filename]
    return next(path for path in candidates if path.exists())

def letters_only(text):
    return re.sub("[^a-z]", "", text.lower())

texts = {
    "Alice": letters_only(data_path("alice_in_wonderland.txt").read_text(encoding="utf-8")),
    "Pride and Prejudice": letters_only(data_path("pride_and_prejudice.txt").read_text(encoding="utf-8")),
}

def symbol_probabilities(sequence):
    counts = Counter(sequence)
    symbols = sorted(counts)
    p = np.array([counts[s] for s in symbols], dtype=float)
    return symbols, p / p.sum()

for name, sequence in texts.items():
    _, p = symbol_probabilities(sequence)
    print(f"{name:20s}: {len(sequence):,} letters, H1={shannon_entropy(p):.3f} bits/letter")
""", cell_id="w9w-load-text"),
        md("""
## Inspect the estimated letter distributions

Plotting the distribution prevents the entropy value from becoming detached from the data that produced it.
""", cell_id="w9w-letter-distribution"),
        code("""
fig, ax = plt.subplots(figsize=(10, 4.2))
for name, sequence in texts.items():
    symbols, p = symbol_probabilities(sequence)
    ax.plot(symbols, p, marker="o", lw=1.5, label=name)
ax.set(xlabel="Letter", ylabel="Estimated probability")
ax.legend()
plt.show()
""", cell_id="w9w-letter-plot"),
        md("""
# A deliberate failure

Shuffle every letter in *Alice*. The single-letter distribution, and therefore its single-letter entropy, is unchanged even though the text has lost its words, syntax and story. This is not a failure of the formula. We asked it a question that excluded order.
""", cell_id="w9w-failure"),
        code("""
rng = np.random.default_rng(3024)
alice = texts["Alice"]
shuffled = "".join(rng.permutation(list(alice)))

for name, sequence in [("original", alice), ("shuffled", shuffled)]:
    _, p = symbol_probabilities(sequence)
    print(name, shannon_entropy(p))
""", cell_id="w9w-shuffle"),
        md("""
# Retain short-range ordering with blocks

Treat overlapping groups of $m$ letters as outcomes. Block entropy can retain local ordering, but the number of possible blocks grows rapidly and finite data become a problem.
""", cell_id="w9w-blocks"),
        code("""
def block_entropy(sequence, block_length):
    blocks = [sequence[i:i + block_length] for i in range(len(sequence) - block_length + 1)]
    _, p = symbol_probabilities(blocks)
    return shannon_entropy(p)

for m in range(1, 5):
    original_rate = block_entropy(alice, m) / m
    shuffled_rate = block_entropy(shuffled, m) / m
    print(f"m={m}: original {original_rate:.3f}, shuffled {shuffled_rate:.3f} bits/letter")
""", cell_id="w9w-block-code"),
        md("""
## Modelling decision

Change one choice: alphabet, punctuation, case, block length, or observation window. Report how the entropy changed and what new distinction the representation retained. Do not search for the largest value; choose a representation that answers a stated question.
""", cell_id="w9w-decision"),
        md("""
# Take-away

Entropy is reproducible once the outcomes and probabilities are defined. The scientific interpretation still depends on how observations were turned into those outcomes.
""", cell_id="w9w-takeaway"),
    ]
    nb["cells"] = cells
    save(path, nb)


def revise_week10():
    path, nb = load("notebooks/week10/L_Game_theory.ipynb")
    cells = nb["cells"]
    banner = find(cells, "# Real-world motivation")
    insertion = [
        md("""
## Cyclic competition in motion

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://konloch.com/demos/rock-paper-scissors" title="Rock paper scissors emoji arena" style="width:100%;height:430px;border:0"></iframe></div>
<div class="text-panel"><p>Moving rock, paper and scissors agents convert one another on contact. The local payoff rule is cyclic: each type beats one and loses to one.</p><p>A finite run may eventually contain only one type. That outcome is produced by movement, collisions, boundaries and chance as well as by the payoff table.</p><p><a href="https://konloch.com/demos/rock-paper-scissors" target="_blank">Open the simulation in a new tab</a>.</p></div>
</div>
""", cell_id="w10-rps-arena", slide="subslide"),
        md("""
## Games in biological systems

Game theory is useful whenever success depends on what others do.

| System | Strategic tension |
|---|---|
| Side-blotched lizards | Three male mating strategies form a rock–paper–scissors cycle: [Sinervo and Lively (1996)](https://doi.org/10.1038/380240a0). |
| Yeast populations | Cooperation and cheating can produce snowdrift-game dynamics: [Gore, Youk and van Oudenaarden (2009)](https://doi.org/10.1038/nature07921). |
| Shared resources | Individual incentives can conflict with collective persistence, motivating public-goods and commons games. |

The game specifies incentives. Population structure, learning, movement and repeated interaction determine how those incentives unfold through time.
""", cell_id="w10-real-games", slide="subslide"),
    ]
    if not any(c.get("id") == "w10-rps-arena" for c in cells):
        cells[banner + 1:banner + 1] = insertion
    save(path, nb)


def write_entropy_widget():
    path = ROOT / "notebooks/week09/entropy_distribution_explorer.html"
    path.write_text("""<!doctype html>
<html><head><meta charset="utf-8"><style>
body{font-family:system-ui,-apple-system,sans-serif;color:#16264a;margin:0;padding:18px;background:#fff}
.wrap{display:grid;grid-template-columns:minmax(260px,.8fr) minmax(320px,1.2fr);gap:28px;align-items:center}
.row{display:grid;grid-template-columns:30px 1fr 48px;gap:10px;align-items:center;margin:13px 0}
input{width:100%}.value{font-variant-numeric:tabular-nums}.entropy{font-size:1.45rem;font-weight:700;margin-top:20px}
.bars{height:320px;display:flex;align-items:flex-end;gap:22px;border-left:2px solid #20345b;border-bottom:2px solid #20345b;padding:0 24px}
.barwrap{flex:1;text-align:center}.bar{background:#3e6f9f;min-height:1px;border-radius:5px 5px 0 0;transition:height .15s}.p{margin-top:6px}.note{font-size:.9rem;color:#53627c;margin-top:14px}
@media(max-width:720px){.wrap{grid-template-columns:1fr}.bars{height:230px}}
</style></head><body><div class="wrap"><section><h2>Adjust outcome weights</h2>
<div id="controls"></div><div class="entropy" id="entropy"></div>
<div class="note">Weights are normalised automatically, so they need not add to one.</div></section>
<section><div class="bars" id="bars"></div></section></div>
<script>
const initial=[1,1,1,1], controls=document.getElementById('controls'), bars=document.getElementById('bars');
initial.forEach((v,i)=>{controls.insertAdjacentHTML('beforeend',`<div class="row"><label>${i+1}</label><input id="w${i}" type="range" min="0" max="100" value="${v*50}"><span class="value" id="v${i}"></span></div>`);bars.insertAdjacentHTML('beforeend',`<div class="barwrap"><div class="bar" id="b${i}"></div><div class="p" id="p${i}"></div></div>`)});
function update(){let w=initial.map((_,i)=>+document.getElementById('w'+i).value), total=w.reduce((a,b)=>a+b,0)||1, p=w.map(x=>x/total), H=-p.reduce((s,x)=>s+(x?x*Math.log2(x):0),0);p.forEach((x,i)=>{document.getElementById('v'+i).textContent=x.toFixed(2);document.getElementById('b'+i).style.height=(x*290)+'px';document.getElementById('p'+i).textContent='p='+x.toFixed(2)});document.getElementById('entropy').textContent='H = '+H.toFixed(3)+' bits'}
document.querySelectorAll('input').forEach(x=>x.addEventListener('input',update));update();
</script></body></html>""")


if __name__ == "__main__":
    revise_week01()
    revise_week08_workshop()
    revise_week09()
    revise_week09_workshop()
    revise_week10()
    write_entropy_widget()
