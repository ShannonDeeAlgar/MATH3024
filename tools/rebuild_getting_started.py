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
# Getting started

MATH3024 is organised as a sequence of weekly topics. Each topic is explored through a **canonical model**: a deliberately focused model that makes the week's central ideas visible and gives us something concrete to question, implement, and extend.

<div class="reader-route">
  <div class="reader-route-label">One weekly thread</div>
  <div class="reader-route-body">Phenomenon → canonical model → local mechanism → collective behaviour → interpretation → transfer</div>
</div>

You will meet that thread in three connected forms:

| Resource | What it contributes | How to use it |
|---|---|---|
| **Lecture and slides** | The shared encounter with the phenomenon, live questions, predictions, and the first construction of the model | Participate, predict, and record the reasoning that is developed in the room. Slides are deliberately minimal and are not a substitute for the lecture. |
| **Reader** | The durable account of the ideas, definitions, evidence, derivations, references, and interpretations | Read actively. Annotate it or keep handwritten notes beside it. Return to it before and after the workshop. |
| **Workshop notebook** | The executable version of the model, small tests, parameter changes, and extensions | Predict before running. Inspect intermediate states. Change one choice at a time, then explain what changed and why. |

These are not three repetitions of the same material. They are three passes through the same intellectual problem. The lecture establishes the questions, the Reader develops the account, and the workshop turns the account into something you can interrogate.
""", "weekly-learning-thread"),

        markdown(r"""
## Where to find each resource

| Resource | Student access |
|---|---|
| **Unit essentials, announcements, assessment, and weekly links** | LMS is the authoritative location. |
| **Reader** | [shannondeealgar.github.io/MATH3024](https://shannondeealgar.github.io/MATH3024/) |
| **Lecture slides** | Open the link in the relevant LMS weekly module. Published decks are stored with the Reader. For example, [Week 1 slides](https://shannondeealgar.github.io/MATH3024/slides/week01/L_Introduction_to_complex_systems.slides.html). |
| **Workshop notebooks** | Download the file beginning `WS_` from the relevant LMS weekly module. Download any support files listed beside it. |
| **Source repository** | [github.com/ShannonDeeAlgar/MATH3024](https://github.com/ShannonDeeAlgar/MATH3024). This is available for transparency, but students do not need Git or GitHub to complete the unit. |

If an LMS instruction and an older downloaded file disagree, follow the current LMS instruction and download the file again.
""", "resource-locations"),

        markdown(r"""
## A useful weekly rhythm

### Before the lecture

- Open the week's Reader chapter and skim its route, headings, and figures.
- Note unfamiliar language without trying to master everything in advance.

### During the lecture

- Commit to predictions before simulations or results are revealed.
- Record modelling choices and assumptions, not only final equations.
- Mark places where the behaviour conflicts with your expectation.

### After the lecture and during the workshop

- Revisit the relevant Reader section.
- Download the weekly `WS_...ipynb` file and any stated support files from LMS.
- Run it from the beginning in order.
- Use the workshop to reconstruct, test, and challenge the canonical model.
- Finish by connecting a local modelling choice to a system-level result.

The Week 1 workshop notebook is self-contained. If a later workshop needs images or data, they will be supplied with it on LMS. You do **not** need GitHub access or any accompanying `.py` build scripts. Those scripts maintain the teaching materials and are not part of the student exercise.
""", "weekly-rhythm"),

        markdown(r"""
# Running workshop notebooks

Jupyter notebooks combine explanatory text, equations, executable code, figures, and your own observations in one `.ipynb` file.

## Option 1: run locally

A scientific Python distribution such as Anaconda provides Python, Jupyter, NumPy, Matplotlib, SciPy, and other libraries used in this unit.

1. Install a current Python 3 distribution with Jupyter.
2. Download the weekly workshop notebook and any stated support files from LMS.
3. Open Jupyter Notebook or JupyterLab.
4. Navigate to the downloaded `.ipynb` file.
5. Run a cell with **Shift + Enter**.

Keep the notebook in a folder where you have permission to save changes. Save a new copy before making a substantial extension.

## Option 2: use Google Colab

If you cannot install software locally:

1. Go to <https://colab.research.google.com>.
2. Select **File → Upload notebook**.
3. Upload the weekly `WS_...ipynb` file.
4. Run the cells in order.

Browser security can prevent a custom animation control from appearing until its code cell has been run. The mathematical code and static figures will still work.
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

You are not expected to become a software engineer in this unit. You are expected to use code carefully enough that it supports mathematical reasoning rather than obscuring it.

## A reliable process

1. **State the question.** What are you trying to learn from the model?
2. **Write pseudocode.** Describe the logic before worrying about Python syntax.
3. **Start small.** Use a configuration that you can inspect by hand.
4. **Separate responsibilities.** Keep initialisation, update rules, measurement, and plotting in distinct functions.
5. **Test local rules.** Construct tiny cases with known answers.
6. **Make randomness reproducible.** Record seeds and use local random-number generators.
7. **Preserve a baseline.** Change one modelling choice at a time.
8. **Restart and run all.** Confirm that the notebook works from a clean kernel.
9. **Interpret the output.** A figure is evidence to reason from, not a conclusion by itself.

Online examples and generative AI can help you understand syntax, errors, and alternative implementations. You remain responsible for checking the code, understanding every claim you make, following the unit's assessment rules, and acknowledging assistance where required.
""", "code-for-thinking"),

        markdown(r"""
## Pseudocode example

Pseudocode is a plain-language description of an algorithm. It should expose the sequence of decisions without tying the explanation to Python syntax.

For one step of a segregation model:

```text
calculate each occupied agent's local similarity
identify the dissatisfied agents

if no agent is dissatisfied:
    stop
otherwise:
    choose one dissatisfied agent at random
    choose one empty site at random
    move the selected agent to that site
    record the new state and observables
```

This is already useful. It exposes where choices have been made and suggests separate functions that can be tested before the full simulation is run.
""", "pseudocode-example"),
    ]

    nbf.write(notebook, TARGET)
    print(f"Wrote {TARGET} ({len(notebook['cells'])} cells)")


if __name__ == "__main__":
    main()
