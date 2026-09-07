import json
from pathlib import Path


ROOT = Path("notebooks")


def load(path):
    return json.loads(path.read_text())


def save(path, nb):
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


def prepend_after_heading(source, heading, addition):
    if addition.strip() in source:
        return source
    return source.replace(heading, heading + "\n\n" + addition, 1)


# Week 0: tell students what changes across the unit, without presenting the
# forms as a rigid syntax they need to memorise.
p = ROOT / "week00/Getting_Started.ipynb"
nb = load(p)
for cell in nb["cells"]:
    src = "".join(cell.get("source", []))
    if src.startswith("## Pseudocode example"):
        old = "Each topic Reader ends with its canonical model in pseudocode. The notation becomes progressively more technical across the unit: recipes give way to nested loops, named procedures, state declarations, event queues, contracts and validation checks. These are different legitimate ways to communicate computational logic, not different programming languages that need to be memorised."
        new = """Each topic Reader ends with a different pseudocode form. The progression is deliberate:

| Week | Form emphasised | What it makes visible |
|---|---|---|
| 1 | recipe and counted loop | order of operations |
| 2 | nested construction | recursion across generations |
| 3 | flowchart and named procedure | decisions and the route from fields to updates |
| 4 | lookup/decision table | a finite local rule and synchronous updating |
| 5 | agent-state algorithm | stored state and a two-phase population update |
| 6 | vector/array update | one mathematical operation applied to a population |
| 7 | modular procedure with contracts | reusable components, inputs, outputs and checks |
| 8 | event queue | activity that continues until no events remain |
| 9 | analysis pipeline | how raw observations become an information measure |
| 10 | strategy interface and tournament | interchangeable behaviours coordinated by an evaluation protocol |

These are legitimate ways of communicating computational logic, not separate programming languages to memorise. Choose the form that exposes the decisions and dependencies that matter for the problem."""
        src = src.replace(old, new)
        cell["source"] = src.splitlines(keepends=True)
save(p, nb)


forms = {
    1: ("#### Pseudocode: Schelling segregation", "**Pseudocode form: recipe with a stopping rule.** This is close to ordinary instructions: perform the actions in order and stop when the stated condition is met."),
    2: ("# Canonical models in pseudocode", "**Pseudocode form: nested construction.** An outer loop advances the generation; an inner loop applies the same generator to every retained object."),
    3: ("# Canonical model in pseudocode", "**Pseudocode forms: flowchart and named procedure.** The flowchart exposes the update cycle; the procedure states the same logic compactly enough to implement."),
    4: ("# Canonical models in pseudocode", "**Pseudocode form: lookup or decision table with parallel assignment.** This is useful when the next state is selected from a finite set of neighbourhood cases."),
    5: ("# Canonical model in pseudocode", "**Pseudocode form: agent-state algorithm.** Declare what every agent stores, compute all decisions from one snapshot, then update the population together."),
    6: ("## Canonical model in pseudocode", "**Pseudocode form: vector/array update.** Indexed state is retained, but the population-level calculation is expressed as one mathematical update."),
    7: ("# Canonical models in pseudocode", "**Pseudocode form: parallel modular procedures.** The two algorithms expose common inputs, outputs and stopping checks while keeping their candidate representations and memory architectures distinct."),
    8: ("# Canonical models in pseudocode", "**Pseudocode form: event-driven queue.** The clock is not simply a fixed number of steps: one addition triggers events until the queue of unstable sites is empty."),
    10: ("# Canonical model in pseudocode", "**Pseudocode form: strategy interface plus orchestration.** A strategy obeys a common input/output contract; separate match and tournament procedures evaluate those interchangeable behaviours."),
}

for week, (heading, addition) in forms.items():
    p = next(ROOT.glob(f"week{week:02d}/L_*.ipynb"))
    nb = load(p)
    for cell in nb["cells"]:
        src = "".join(cell.get("source", []))
        if heading in src:
            src = prepend_after_heading(src, heading, addition)
            cell["source"] = src.splitlines(keepends=True)
            break
    save(p, nb)


# Week 3: include a genuine flowchart rather than merely naming one.
p = ROOT / "week03/L_Reaction_diffusion.ipynb"
nb = load(p)
for cell in nb["cells"]:
    src = "".join(cell.get("source", []))
    if "# Canonical model in pseudocode" in src and "gray_scott_flowchart.svg" not in src:
        marker = "This version separates model equations from their numerical implementation by naming the operations applied to the concentration fields."
        replacement = """![Flowchart for one Gray–Scott simulation step](images/gray_scott_flowchart.svg)

The diamonds are decisions; rectangles are operations; arrows show control flow. The flowchart is useful for checking sequence and repetition, while the structured procedure below is easier to translate into code.

This version separates model equations from their numerical implementation by naming the operations applied to the concentration fields."""
        src = src.replace(marker, replacement)
        cell["source"] = src.splitlines(keepends=True)
        break
save(p, nb)


# Week 9: retain the no-canonical-model decision, but show the computational
# pipeline used to estimate entropy from observations.
p = ROOT / "week09/L_InformationTheory.ipynb"
nb = load(p)
for cell in nb["cells"]:
    src = "".join(cell.get("source", []))
    if "## Information measures at a glance · Shannon entropy" in src and "Analysis pipeline" not in src:
        addition = r"""

### Analysis pipeline rather than model pseudocode

```text
INPUT observations
CHOOSE a representation: symbols, bins, blocks or time windows
COUNT occurrences in that representation
NORMALISE counts to probabilities p(x)
CHECK that probabilities sum to one and sample sizes are adequate
COMPUTE H = -SUM_x p(x) log2 p(x)
REPEAT for defensible alternative representations
REPORT the estimate together with those choices and sensitivity checks
```

This pipeline does not generate the system. It specifies how observations are converted into an information measure.
"""
        src += addition
        cell["source"] = src.splitlines(keepends=True)
        break
save(p, nb)


# Week 10: a second spatial game complements the moving cyclic RPS example.
p = ROOT / "week10/L_Game_theory.ipynb"
nb = load(p)
if not any("The Prisoner's Kaleidoscope" in "".join(c.get("source", [])) for c in nb["cells"]):
    insert_at = next(i for i, c in enumerate(nb["cells"]) if "## Games in biological systems" in "".join(c.get("source", [])))
    source = """## Games played by agents on a lattice

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://www.complexity-explorables.org/explorables/prisoners-kaleidoscope/" title="The Prisoner's Kaleidoscope spatial game" style="width:100%;height:430px;border:0"></iframe></div>
<div class="text-panel"><p><em>The Prisoner's Kaleidoscope</em> places cooperating and defecting agents on a lattice. Each agent plays its neighbours, accumulates payoff, then adopts the locally most successful strategy.</p><p>Unlike the moving rock–paper–scissors agents, the players occupy fixed sites and update synchronously. Spatial arrangement is now part of the game: clusters can protect cooperation and produce persistent invasion patterns.</p><p><a href="https://www.complexity-explorables.org/explorables/prisoners-kaleidoscope/" target="_blank">Open the explorable in a new tab</a>.</p></div>
</div>

The model follows the spatial Prisoner's Dilemma studied by Nowak and May (1992), [Evolutionary games and spatial chaos](https://doi.org/10.1038/359826a0).
"""
    nb["cells"].insert(insert_at, {
        "cell_type": "markdown",
        "metadata": {"slideshow": {"slide_type": "subslide"}},
        "source": source.splitlines(keepends=True),
    })
save(p, nb)
