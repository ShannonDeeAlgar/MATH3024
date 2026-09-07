#!/usr/bin/env python3
"""Tighten Week 8 initialisation, spatial figures, and scale terminology."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"
WORKSHOP = ROOT / "notebooks/week08/WS_Critical_phenomena.ipynb"


def source(cell):
    return "".join(cell.get("source", []))


def set_source(cell, text):
    cell["source"] = text.rstrip().splitlines(keepends=True)
    if cell["source"]:
        cell["source"][-1] += "\n"


def markdown(text, cell_id, tags=None):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": list(tags or [])},
        "source": text.rstrip().splitlines(keepends=True),
    }


def find(cells, prefix):
    return next(i for i, cell in enumerate(cells) if source(cell).lstrip().startswith(prefix))


def update_lecture():
    nb = json.loads(LECTURE.read_text())
    cells = nb["cells"]

    try:
        scale_i = find(cells, "### Scale invariance (aka scale-free behaviour)")
    except StopIteration:
        scale_i = find(cells, "### Scale language used here")
    set_source(cells[scale_i], r"""
### Scale language used here

These terms overlap, but they are not interchangeable.

- **Scale invariance** describes a relationship that keeps the same form after rescaling, perhaps multiplied by a constant. A power law has this property because $f(cx)=c^{-\alpha}f(x)$.
- **Scale-free** is the broader claim that no single characteristic scale dominates the quantity being studied over a stated range. Empirical systems are normally scale-free only over a finite range.
- **Self-similar** describes a geometric or statistical resemblance across scales. It may be exact, as for an ideal fractal, or approximate.
- A **power law** is one mathematical form that can produce scale invariance. A straight-looking log–log plot alone is not enough to establish one.
- **Critical** describes the regime near a transition where correlations can extend across many scales. It is not simply another word for scale-free.

Authors do not always use this vocabulary consistently. When reading more widely, check which quantity is being rescaled, over what range, and whether the claim is exact or empirical.
""")

    try:
        perturb_i = find(cells, "### Perturbations")
    except StopIteration:
        perturb_i = find(cells, "### Two ways to reach an active pile")
    set_source(cells[perturb_i], """
### Two ways to reach an active pile

Starting from an empty lattice and adding one grain at a time is faithful to the slow-driving story, but initially almost every addition merely loads the pile. Visible avalanches are rare and a useful sample takes a long time to accumulate.

For demonstration we can instead assign deliberately overfull heights, relax the entire lattice, and use the resulting stable pile as a prepared initial condition. This reaches an active state quickly. It is a computational shortcut, not proof that the prepared state is already a representative sample of the long-run dynamics, so a short additional burn-in is still required before measuring avalanche statistics.

<img src="images/sandpile_initialisation_comparison.png" width="82%" alt="Slow driving from an empty sandpile compared with relaxation of an overfull initial state">
""")

    qualitative_i = find(cells, "### Qualitative behaviour")
    # Legacy animation construction cells are useful in the lecture deck but
    # should not create Source/Output drawers in the Reader.
    for cell in cells[qualitative_i + 1:]:
        text = source(cell).lstrip()
        if text.startswith("### Quantitative behaviour"):
            break
        tags = cell.setdefault("metadata", {}).setdefault("tags", [])
        if "slides-only" not in tags:
            tags.append("slides-only")

    height_i = find(cells, '<div class="two-panel equal-panels compact-panels">\n<div class="image-panel"><img src="images/sandpile_height_subsets.png"')
    fractal = markdown(r"""
### A deliberately symmetric pile

Random driving is useful for avalanche statistics, but it can hide the geometry. If many grains are placed at one central site and the pile is allowed to relax, the stable configurations expose nested spatial structure much more clearly.

<img src="images/sandpile_fractal_stills.png" width="94%" alt="Three stable Abelian sandpiles formed by adding increasing numbers of grains at one central site">

These are deliberately symmetric demonstrations, not typical snapshots from the randomly driven stationary process. They make the fractal-like spatial organisation visible; the later box-counting calculation asks whether that impression survives measurement.
""", "week08-sandpile-fractal-stills", ["reader-only"])
    if not any(c.get("id") == fractal["id"] for c in cells):
        cells.insert(height_i + 1, fractal)

    # Remove a loose statement that treated all related terms as synonyms.
    for cell in cells:
        if source(cell).lstrip().startswith("A few things to note:"):
            set_source(cell, r"""
A few things to note:

- Increasing the lattice size lets us test whether the fitted range extends while the estimated exponent remains reasonably stable. That is stronger evidence for scale-free behaviour than one system size alone.
- A large sample is required. Most added grains cause no toppling at all, so record both the fraction of zero events and the conditional distribution of avalanche sizes given that an avalanche occurred.
""")

    LECTURE.write_text(json.dumps(nb, indent=1) + "\n")


def update_workshop():
    nb = json.loads(WORKSHOP.read_text())
    cells = nb["cells"]

    code_i = find(cells, "import numpy as np")
    set_source(cells[code_i], r'''
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

rng = np.random.default_rng(3024)

def stabilise(pile):
    """Relax all unstable sites; grains leaving an open edge are lost."""
    pile = np.asarray(pile, dtype=np.int64).copy()
    topplings = 0
    while np.any(pile >= 4):
        count = pile // 4
        pile %= 4
        topplings += int(count.sum())
        pile[1:, :] += count[:-1, :]
        pile[:-1, :] += count[1:, :]
        pile[:, 1:] += count[:, :-1]
        pile[:, :-1] += count[:, 1:]
    return pile, topplings

def prepare_active_pile(L=32, seed=3024):
    """Create an overfull state and relax it once to a stable state."""
    local_rng = np.random.default_rng(seed)
    overfull = local_rng.integers(0, 8, size=(L, L))
    return stabilise(overfull)

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

def run_sandpile(L=32, additions=30_000, burn_in=2_000, seed=3024, initial=None):
    local_rng = np.random.default_rng(seed)
    pile = np.zeros((L, L), dtype=int) if initial is None else initial.copy()
    sizes, durations = [], []
    for step in range(additions):
        size, duration = add_grain_and_relax(pile, local_rng)
        if step >= burn_in and size > 0:
            sizes.append(size)
            durations.append(duration)
    return pile, np.asarray(sizes), np.asarray(durations)
''')

    try:
        check_i = find(cells, "## Check the local rule")
    except StopIteration:
        check_i = find(cells, "## Begin with slow driving")
    set_source(cells[check_i], """
## Begin with slow driving

Start with an empty lattice and add grains one at a time. This is the model's natural driving process, but at first very little happens: most additions only raise a stable height by one. Record that apparent inactivity rather than silently waiting through it.
""")

    demo_code = cells[check_i + 1]
    set_source(demo_code, r'''
L = 32
slow_pile = np.zeros((L, L), dtype=int)
slow_rng = np.random.default_rng(8030)
slow_sizes = []
for _ in range(800):
    size, _ = add_grain_and_relax(slow_pile, slow_rng)
    slow_sizes.append(size)

print(f"Slow drive: {sum(s > 0 for s in slow_sizes)} of 800 additions triggered any toppling.")

prepared_pile, preparation_topplings = prepare_active_pile(L=L, seed=8031)
print(f"Prepared state: relaxed through {preparation_topplings:,} topplings; maximum stable height = {prepared_pile.max()}.")

fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), constrained_layout=True)
for ax, field, title in [
    (axes[0], slow_pile, "800 slow additions from empty"),
    (axes[1], prepared_pile, "Relaxed overfull initial state"),
]:
    im = ax.imshow(field, cmap="viridis", vmin=0, vmax=3)
    ax.set(title=title, xlabel="Column", ylabel="Row")
fig.colorbar(im, ax=axes, label="Stable height", shrink=.82)
plt.show()
''')

    comparison = markdown("""
The second route fast-tracks the long loading transient. It does not make equilibration irrelevant. Before collecting statistics, continue driving the prepared pile for a shorter burn-in so that the measurements are not dominated by the arbitrary overfull initialisation.

This is a general simulation decision: distinguish the physical process used to define the model from the computational method used to prepare a useful starting state.
""", "week08-prepared-state-qualification")
    if not any(c.get("id") == comparison["id"] for c in cells):
        cells.insert(check_i + 2, comparison)

    # Indices may have shifted; insert a concise statistics cell immediately
    # before the avalanche-measurement section.
    measure_i = find(cells, "# Measure avalanches")
    stats_code = {
        "cell_type": "code",
        "execution_count": None,
        "id": "week08-run-prepared-pile",
        "metadata": {},
        "outputs": [],
        "source": r'''
pile, sizes, durations = run_sandpile(
    L=L,
    additions=12_000,
    burn_in=2_000,
    seed=8032,
    initial=prepared_pile,
)
assert pile.max() < 4
print(f"Recorded {len(sizes):,} non-zero avalanches after the additional burn-in.")
'''.lstrip().splitlines(keepends=True),
    }
    if not any(c.get("id") == stats_code["id"] for c in cells):
        cells.insert(measure_i, stats_code)

    # Reuse the prepared state for the inspectable avalanche rather than
    # spending another 18,000 additions rebuilding one from empty.
    for cell in cells:
        if cell.get("cell_type") == "code" and "animation_pile, _, _ = run_sandpile" in source(cell):
            text = source(cell).replace(
                "animation_pile, _, _ = run_sandpile(L=27, additions=18_000, burn_in=0, seed=806)\n",
                "animation_pile, _ = prepare_active_pile(L=27, seed=806)\n"
            )
            set_source(cell, text)

    WORKSHOP.write_text(json.dumps(nb, indent=1) + "\n")


if __name__ == "__main__":
    update_lecture()
    update_workshop()
