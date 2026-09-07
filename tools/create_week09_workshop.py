"""Create the Week 9 workshop on entropy and representation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def md(text, cell_id):
    return {"cell_type": "markdown", "id": cell_id, "metadata": {},
            "source": text.splitlines(keepends=True)}

def code(text, cell_id):
    return {"cell_type": "code", "execution_count": None, "id": cell_id,
            "metadata": {}, "outputs": [], "source": text.splitlines(keepends=True)}

cells = [
md("""# Week 9 workshop · What does an information measure retain?

The lecture and Reader introduce Shannon entropy and related information measures. Here we calculate them, test their limits, and use them to compare data that look different.
""", "week09-title"),
md("""## Two objectives, one investigation

**Canonical model:** Shannon entropy of a discrete source.

**Modelling focus:** A quantitative summary is useful only when we understand what it retains and what it discards.

**Why it matters:** Two systems can share one entropy value while having very different ordering, dependence, or mechanisms.

**How it appears here:** We verify entropy on known distributions, then compare single-symbol and block descriptions of binary sequences.

It is developed through the canonical model rather than as a separate exercise.
""", "transferable-modelling-focus"),
md("""# Begin with a distribution

For probabilities $p_1,\ldots,p_n$, Shannon entropy in bits is

$$H=-\sum_i p_i\log_2 p_i,$$

where zero-probability terms contribute zero. Before using the function on data, check cases whose answers we know: a certain outcome has entropy $0$; a fair binary outcome has entropy $1$ bit.
""", "entropy-definition"),
code('''import numpy as np
import matplotlib.pyplot as plt

def shannon_entropy(probabilities):
    """Return Shannon entropy in bits for a discrete probability vector."""
    p = np.asarray(probabilities, dtype=float)
    if np.any(p < 0) or not np.isclose(p.sum(), 1.0):
        raise ValueError("Probabilities must be non-negative and sum to one.")
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())

assert np.isclose(shannon_entropy([1, 0]), 0)
assert np.isclose(shannon_entropy([0.5, 0.5]), 1)
for p in ([1, 0], [0.9, 0.1], [0.5, 0.5], [0.25] * 4):
    print(f"p={p}: H={shannon_entropy(p):.3f} bits")
''', "entropy-function"),
md("""# Move from a model distribution to observations

Estimate symbol probabilities from counts. This introduces a modelling choice: which observations count as the same symbol?
""", "observed-symbols"),
code('''def entropy_of_symbols(symbols):
    """Estimate single-symbol entropy from an observed sequence."""
    _, counts = np.unique(np.asarray(symbols), return_counts=True)
    return shannon_entropy(counts / counts.sum())

rng = np.random.default_rng(3024)
n = 200
sequences = {
    "constant": np.zeros(n, dtype=int),
    "alternating": np.arange(n) % 2,
    "two blocks": np.repeat([0, 1], n // 2),
    "random": rng.integers(0, 2, size=n),
}
for name, sequence in sequences.items():
    print(f"{name:12s} H1={entropy_of_symbols(sequence):.3f} bits")
''', "sequence-entropies"),
md("""## A deliberate failure

The alternating, blocked, and random sequences contain almost the same proportions of zeros and ones, so their **single-symbol entropy** is almost the same. Yet their temporal organisation is visibly different.

> **Discussion:** What conclusion would be lost if each sequence were replaced by $H_1$ alone?
""", "deliberate-failure"),
code('''fig, axes = plt.subplots(len(sequences), 1, figsize=(9, 3.8), sharex=True)
for ax, (name, sequence) in zip(axes, sequences.items()):
    ax.imshow(sequence[np.newaxis, :], cmap="binary", vmin=0, vmax=1,
              aspect="auto", interpolation="nearest")
    ax.set_ylabel(name, rotation=0, ha="right", va="center")
    ax.set_yticks([])
axes[-1].set_xlabel("Position in sequence")
fig.suptitle("Similar symbol counts can hide different organisation")
fig.tight_layout()
plt.show()
''', "sequence-plot"),
md("""# Retain short-range ordering with blocks

Treat consecutive pairs as the outcomes $00$, $01$, $10$, and $11$. The resulting block entropy records more local order than the single-symbol calculation.
""", "block-entropy-heading"),
code('''def block_entropy(sequence, block_length=2):
    """Entropy of overlapping blocks of a fixed length, in bits per block."""
    sequence = np.asarray(sequence)
    blocks = [tuple(sequence[i:i + block_length])
              for i in range(len(sequence) - block_length + 1)]
    _, counts = np.unique(blocks, axis=0, return_counts=True)
    return shannon_entropy(counts / counts.sum())

for name, sequence in sequences.items():
    h1 = entropy_of_symbols(sequence)
    h2 = block_entropy(sequence, 2)
    print(f"{name:12s} H1={h1:.3f} bits/symbol, H2={h2:.3f} bits/pair")
''', "block-entropy-code"),
md("""# Test sensitivity to representation

Choose one dataset and change one representational decision: bin width for continuous values, alphabet size, block length, or observation window. Record both the resulting entropy and the scientific interpretation.

The aim is not to find the largest entropy. It is to decide which representation retains the structure relevant to the question.
""", "representation-test"),
code('''block_lengths = range(1, 7)
fig, ax = plt.subplots(figsize=(7, 4))
for name in ("alternating", "two blocks", "random"):
    values = [block_entropy(sequences[name], length) / length
              for length in block_lengths]
    ax.plot(block_lengths, values, marker="o", label=name)
ax.set(xlabel="Block length", ylabel="Entropy per symbol (bits)")
ax.legend(frameon=False)
fig.tight_layout()
plt.show()
''', "block-sweep"),
md("""# Take-away

The entropy calculation is reproducible; its interpretation still depends on the outcomes, scale, and dependencies represented. Report those choices whenever an information measure supports a claim.
""", "take-away"),
]

notebook = {"cells": cells, "metadata": {"kernelspec": {
    "display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3"}},
    "nbformat": 4, "nbformat_minor": 5}
out = ROOT / "notebooks/week09/WS_Information_theory.ipynb"
out.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
print(out.relative_to(ROOT))
