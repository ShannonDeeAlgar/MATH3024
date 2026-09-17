#!/usr/bin/env python3
"""Rebuild the student-facing Getting Started chapter."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "notebooks/week00/Getting_Started.ipynb"


def markdown(source: str, cell_id: str):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def code(source: str, cell_id: str):
    cell = nbf.v4.new_code_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def main():
    notebook = nbf.v4.new_notebook()
    notebook["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    }
    notebook["cells"] = [
        markdown(r"""
# Welcome to MATH3024

MATH3024 is organised as a sequence of weekly topics. Each topic uses a **canonical model** to make particular ideas concrete enough to specify, simulate, analyse and revise.

<div class="reader-route">
  <div class="reader-route-label">The modelling process</div>
  <div class="reader-route-body">Observe and ask → specify → simulate → analyse → revise and communicate</div>
</div>

Every topic moves through this process, but not with equal emphasis. Some weeks concentrate on representation or model specification; others spend more time on simulation, analysis or evidence. Across the unit, those different emphases build a fuller modelling practice.

The lecture, Reader and workshop have different jobs:

| Resource | What it contributes | How to use it |
|---|---|---|
| **Lecture and slides** | The shared encounter with the phenomenon, live questions, predictions, and the first construction of the model | Participate, predict, and record the reasoning that is developed in the room. Slides are deliberately minimal and are not a substitute for the lecture. |
| **Reader** | The durable account of the ideas, definitions, evidence, derivations, references, and interpretations | Read actively. Annotate it or keep handwritten notes beside it. Return to it before and after the workshop. |
| **Workshop notebook** | The executable version of the model, small tests, parameter changes, and extensions | Predict before running. Inspect intermediate states. Change one choice at a time, then explain what changed and why. |

The lecture introduces and discusses the central ideas. The Reader provides the complete account and references. The workshop is where you implement the model, inspect its behaviour and make modelling decisions.
""", "weekly-learning-thread"),

        markdown(r"""
## Optional material in the Reader

The main argument of each week is written to stand on its own. Some chapters also retain material that is useful on a second pass but is not required for the unit core: a longer derivation, wider scientific context, a model variant, or a possible project method.

<div class="optional-reader-flag"><strong>Optional · extension</strong> Dashed grey flags mark this material. Unless a chapter states otherwise, it is not directly assessable.</div>

This material is retained rather than deleted because it can make an assumption inspectable, connect the canonical model to mathematics studied elsewhere, or provide a defensible starting point for a project. **Optional does not mean unimportant or unreliable.** It means that you can follow the assessable weekly argument without it, then return when the connection is useful.
""", "weekly-rhythm"),

        markdown(r"""
# Running workshop notebooks

Jupyter notebooks combine explanatory text, equations, executable code, figures, and your own observations in one `.ipynb` file.

## Python throughout the unit

All computational work in MATH3024 is done in **Python**. We use it to implement models, inspect individual updates, run simulations, vary parameters, construct ensembles, and visualise results. You are not expected to arrive as a Python expert. The aim is to make the code sufficiently clear and testable that it supports your mathematical reasoning.

<img src="images/python_comic.png" alt="XKCD comic in which Python makes programming feel unexpectedly powerful" style="display:block;max-width:520px;width:100%;margin:1rem auto">

<div style="text-align:center;font-size:.82em;color:#5A6685">Randall Munroe, <a href="https://xkcd.com/353/">“Python”</a>, xkcd 353, licensed under CC BY-NC 2.5.</div>

## Recommended setup: run locally

A scientific Python distribution such as Anaconda provides Python, Jupyter, NumPy, Matplotlib, SciPy, and other libraries used in this unit.

1. Install a current Python 3 distribution with Jupyter.
2. Download the weekly workshop notebook and any stated support files from LMS.
3. Open Jupyter Notebook or JupyterLab.
4. Navigate to the downloaded `.ipynb` file.
5. Run a cell with **Shift + Enter**.

Keep the notebook in a folder where you have permission to save changes. Save a new copy before making a substantial extension.

If local installation is temporarily unavailable, Google Colab can open a notebook in a browser. Local Jupyter remains the supported and strongly recommended setup for this unit.
""", "running-notebooks"),

        markdown(r"""
## Test your environment

Run the next cell. A successful run prints the package versions and produces a short logistic-map trajectory.
""", "environment-check-intro"),

        code(r'''
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

print(f"Python {sys.version_info.major}.{sys.version_info.minor}")
print(f"NumPy {np.__version__}")
print(f"Matplotlib {matplotlib.__version__}")

r = 3.7
x = 0.5
trajectory = []
for _ in range(100):
    x = r * x * (1 - x)
    trajectory.append(x)

fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(trajectory, color="#1B2A4C", linewidth=1.5)
ax.set(xlabel="Simulation time step", ylabel="$x_t$", title="Logistic-map test run")
ax.spines[["top", "right"]].set_visible(False)
plt.show()
''', "environment-check"),

        markdown(r"""
## If something goes wrong

Try these checks in order:

1. Confirm that the cell containing the imports and parameters has been run.
2. Select **Kernel → Restart kernel and run all cells**. The wording varies slightly between Jupyter and Colab.
3. Read the final line of the error message first. It usually identifies the immediate problem.
4. Check that you have not changed a variable name in one cell but not another.
5. Return to the last small test that worked.
6. Bring the error message, the relevant code, and what you expected to the workshop.

A notebook that only works because cells were run in a particular accidental order is not reproducible. Before submitting or sharing work, restart the kernel and run every cell from top to bottom.
""", "troubleshooting"),

        markdown(r"""
# Code as a tool for thinking

> “The purpose of computing is insight, not numbers.”<br>
> Richard Hamming

You are not expected to become a software engineer in this unit. Code is one part of the modelling process: it lets you specify a model precisely, test small cases, inspect intermediate behaviour and compare evidence across runs. Keep initialisation, dynamics, measurement and plotting separate where possible; record random seeds; and confirm that a notebook runs from top to bottom before sharing it.

Online examples and generative AI can help you understand syntax, errors, and alternative implementations. You remain responsible for checking the code, understanding every claim you make, following the unit's assessment rules, and acknowledging assistance where required.
""", "code-for-thinking"),

        markdown(r"""
## Pseudocode

Pseudocode describes computational logic without tying it to Python syntax. There is no required house style. A useful version makes the order of operations and important decisions visible; a complete version must be precise enough that another person could implement the same model without guessing.

For a complete simulation, state or name the world or domain, boundary conditions, stored state, parameters, initialisation and seed, interaction set, update order, stopping rule, and recorded output. Not every model has a physical boundary or numerical time step; say explicitly when an item does not apply.

Each workshop includes a clearly labelled pseudocode section near the model specification. Across the unit, the examples become more technical and use several legitimate forms. The aim is to learn how to communicate a reproducible algorithm, not to memorise one notation.
""", "pseudocode-example"),
    ]

    nbf.write(notebook, TARGET)
    print(f"Wrote {TARGET} ({len(notebook['cells'])} cells)")


if __name__ == "__main__":
    main()
