import json
import uuid
from pathlib import Path

path = Path(__file__).parents[1] / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = json.loads(path.read_text())


def body(cell):
    return "".join(cell.get("source", []))


def replace_cell(prefix, replacements):
    for cell in nb["cells"]:
        if body(cell).lstrip().startswith(prefix):
            source = body(cell)
            for old, new in replacements:
                source = source.replace(old, new)
            cell["source"] = source.splitlines(keepends=True)
            return
    raise RuntimeError(prefix)


replace_cell("## A general reaction–diffusion model", [
    ("$R_u$ and $R_v$", "$R_U$ and $R_V$"),
])

replace_cell("## From particle motion to Fick’s laws", [
    ("$\\mathbf J=-D\\nabla u$", "$\\mathbf J=-D\\nabla C$"),
    ("\\frac{\\partial u}{\\partial t}", "\\frac{\\partial C}{\\partial t}"),
    ("D\\nabla^2u", "D\\nabla^2C"),
])

replace_cell("## Reader extension: transport as well as diffusion", [
    ("\\frac{\\partial u}{\\partial t}", "\\frac{\\partial C}{\\partial t}"),
    ("\\mathbf w u", "\\mathbf w C"),
    ("D\\nabla^2u+R(u)", "D\\nabla^2C+R(C)"),
    ("$D\\nabla^2u$", "$D\\nabla^2C$"),
    ("$R(u)$", "$R(C)$"),
])

replace_cell("## The parameter space", [
    ("In practice we often fix $D_U$ and $D_V$ using physical knowledge, then sweep the experimentally controllable feed and removal rates $(f,k)$.",
     "In this teaching model we often fix a plausible diffusion ratio, then sweep $f$ and $k$. These are effective nondimensional parameters; in a laboratory system they must be related carefully to measurable controls."),
])

replace_cell("## The sequence of representations", [
    ("$V^{(n)}_{i,j}$", "$V^n_{i,j}$"),
    ("Parentheses around $(n)$ emphasise that it is an index, not a power. ", ""),
])

replace_cell("### Return to the complete simulated system", [
    ("producing (V)", "producing $V$"),
    ("only the (V) panel", "only the $V$ panel"),
])

# Add stable notebook IDs to the two cells inserted during the audit.
for cell in nb["cells"]:
    cell.setdefault("id", uuid.uuid4().hex[:8])

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(path)
