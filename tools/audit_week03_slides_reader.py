import json
from pathlib import Path


PATH = Path(__file__).parents[1] / "notebooks/week03/L_Reaction_diffusion.ipynb"


def text(cell):
    return "".join(cell.get("source", []))


def set_text(cell, value):
    cell["source"] = value.splitlines(keepends=True)


def find(cells, prefix):
    return next(i for i, c in enumerate(cells) if text(c).lstrip().startswith(prefix))


def archive(cell):
    tags = cell.setdefault("metadata", {}).setdefault("tags", [])
    for tag in ("archive-only", "remove-cell"):
        if tag not in tags:
            tags.append(tag)
    cell.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "skip"


nb = json.loads(PATH.read_text())
cells = nb["cells"]

# General diffusion uses a generic concentration C. This keeps U and V reserved
# for the two Gray--Scott concentration fields introduced after the particle story.
i = find(cells, "## Continuous description: a diffusion field")
s = text(cells[i])
s = s.replace("field $U(\\mathbf x,t)$", "field $C(\\mathbf x,t)$")
s = s.replace("$\\nabla^2u$", "$\\nabla^2C$")
s = s.replace("\\frac{\\partial u}{\\partial t}=D\\nabla^2u", "\\frac{\\partial C}{\\partial t}=D\\nabla^2C")
set_text(cells[i], s)

# Concentration-level notation is uppercase throughout. Lowercase u and v are
# used only for the particle-level species in Session 1.
i = find(cells, "## A general reaction–diffusion model")
s = text(cells[i])
s = s.replace("\\partial u", "\\partial U").replace("\\partial v", "\\partial V")
s = s.replace("R_u(u,v)", "R_U(U,V)").replace("R_v(u,v)", "R_V(U,V)")
s = s.replace("\\nabla^2u", "\\nabla^2U").replace("\\nabla^2v", "\\nabla^2V")
set_text(cells[i], s)

i = find(cells, "## 2. Diffusion at the concentration level")
s = text(cells[i]).replace("\\partial u", "\\partial U").replace("\\partial v", "\\partial V")
s = s.replace("\\nabla^2u", "\\nabla^2U").replace("\\nabla^2v", "\\nabla^2V")
set_text(cells[i], s)

i = find(cells, "## Two concentrations occupy every grid location")
set_text(cells[i], text(cells[i]).replace("$v/(u+v)$", "$V/(U+V)$"))

i = find(cells, "## The sequence of representations")
s = text(cells[i]).replace("$U^{(n)}_{i,j}$", "$U^n_{i,j}$")
s = s.replace("Parentheses around $n$ emphasise that it is an index, not a power. ", "")
set_text(cells[i], s)

i = find(cells, "### Return to the complete simulated system")
s = text(cells[i])
s = s.replace("Low (u) aligns with high (v)", "Low $U$ aligns with high $V$")
s = s.replace("consumes (U)", "consumes $U$")
set_text(cells[i], s)

# The parameter discussion must not imply that nondimensional teaching-model
# parameters are automatically direct experimental controls.
i = find(cells, "## The parameter space")
s = text(cells[i])
s = s.replace(
    "In practice we often fix $D_U$ and $D_V$ using physical knowledge, then sweep the experimentally controllable parameters $f$ and $k$.",
    "In this teaching model we often fix a plausible diffusion ratio, then sweep $f$ and $k$. These are effective nondimensional parameters; in a laboratory system they would need to be related carefully to measurable controls."
)
set_text(cells[i], s)

# Retire the older Reader fragments that duplicate the rebuilt two-session
# narrative or introduce speculative side paths between it and discretisation.
obsolete_prefixes = [
    "## Remember...",
    "The modeller's purpose is absolutely",
    "If it is discrete, when is pretending",
    "<div style=\"background-color: #ffff88",
    "We have theories for both scenarios",
    "The modelling tools and frameworks",
    "| **Aspect**   | **Nature**",
    "The random walk is a **Markov process**",
    "Diffusion arises from the random motion",
    "Recall that:",
    "<div style=\"border-left: 4px solid #1e70bf",
    "```{dropdown}  my answers",
    "It is the interplay between the reaction",
    "with more concentrations and further coupling",
]
for prefix in obsolete_prefixes:
    try:
        archive(cells[find(cells, prefix)])
    except StopIteration:
        pass

# Two equation-only legacy cells immediately following the old reaction prose.
try:
    old_return = find(cells, "## Return to reaction–diffusion")
    for candidate in cells[old_return + 1:old_return + 5]:
        if text(candidate).lstrip().startswith("$$"):
            archive(candidate)
except StopIteration:
    pass

# The old intuitive grid prose is superseded by the labelled numerical grids,
# indexing diagram, neighbourhood comparison and convolution example.
for prefix in (
    "In a discrete setting, we represent space and time",
    "This doesn’t require full calculus",
    "Before introducing formal operators",
    "Things (particles/concentration/$U$)",
    "We can visualise the numbers",
):
    try:
        archive(cells[find(cells, prefix)])
    except StopIteration:
        pass

# Remove the duplicated Reader heading. The essential-condition slide already
# states the two processes; the following analysis supplies the detail.
for prefix in ("## Reaction and diffusion", "## Build the Turing mechanism"):
    try:
        archive(cells[find(cells, prefix)])
    except StopIteration:
        pass

# Put the useful Reader extensions beside the concepts they extend rather than
# after the whole Gray--Scott development.
def move_after(prefix, after_prefix):
    source_index = find(cells, prefix)
    cell = cells.pop(source_index)
    target_index = find(cells, after_prefix)
    cells.insert(target_index + 1, cell)

move_after("## From a random walk to the diffusion equation", "## Continuous description: a diffusion field")
move_after("## From particle motion to Fick’s laws", "## From a random walk to the diffusion equation")
move_after("## Reader extension: transport as well as diffusion", "## From particle motion to Fick’s laws")
move_after("## What else is in the 1952 paper?", "### Turing calculated a pattern by hand")
move_after("### Intuition for feed and kill", "## 3. Feed and removal at the concentration level")

# Put the general equations before the stability criterion, then retain the
# calculation and historical example as progressively deeper layers.
def move_before(prefix, before_prefix):
    source_index = find(cells, prefix)
    cell = cells.pop(source_index)
    target_index = find(cells, before_prefix)
    cells.insert(target_index, cell)

move_before("## A general reaction–diffusion model", "## The essential condition for a Turing instability")

# Add two concise Reader-only qualifications retained from last year's deck:
# morphology is the target, and numerical instability is not Turing instability.
def markdown(source, tags=None, slide_type="skip"):
    return {
        "cell_type": "markdown",
        "metadata": {"tags": tags or ["reader-only"], "slideshow": {"slide_type": slide_type}},
        "source": source.splitlines(keepends=True),
    }

i = find(cells, "## Return to Turing’s question")
cells.insert(i + 1, markdown(
    "### What counts as an explanation here?\n\n"
    "The model is not expected to reproduce the exact position of every stripe or spot. "
    "The useful comparison is between **morphologies** and mechanisms: which conditions produce spots, stripes, waves or a uniform state, and are those outcomes robust to small changes in initial conditions, geometry and parameters? "
    "A visual resemblance is motivation for a mechanism, not proof that the same mechanism acted in the biological system.\n"
))

i = find(cells, "## Discretise time")
cells.insert(i + 1, markdown(
    "### Numerical stability is a separate question\n\n"
    "The explicit Euler update introduces its own modelling and numerical choices. "
    "If $\\Delta t$ is too large relative to the grid spacing and diffusion coefficients, the computation can become unstable even when the continuous model is not. "
    "Refining $\\Delta t$ and the grid helps distinguish a model result from a numerical artefact. This **numerical instability** is not a Turing instability.\n"
))

# Make the final ladder statement one clear conclusion instead of two competing
# final sections.
i = find(cells, "# The modelling problem underneath the model")
s = text(cells[i])
s += "\nThe same system has been represented at several levels: particles, stochastic paths, concentration fields and numerical arrays. Moving down the ladder exposes implementation and mechanism; moving up reveals ensemble laws, morphologies and parameter-space structure.\n"
set_text(cells[i], s)
try:
    archive(cells[find(cells, "## Returning to the modelling choice")])
except StopIteration:
    pass

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Updated {PATH}")
