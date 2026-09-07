import json
from pathlib import Path

path = Path("notebooks/week07/L_Intelligent_systems.ipynb")
nb = json.loads(path.read_text())


def source(cell):
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else value


def replace_start(prefix, text):
    matches = [cell for cell in nb["cells"] if source(cell).startswith(prefix)]
    if not matches and any(source(cell) == text for cell in nb["cells"]):
        return
    if len(matches) != 1:
        raise RuntimeError(f"Expected one cell beginning {prefix!r}; found {len(matches)}")
    matches[0]["source"] = text


def clear_start(prefix):
    matches = [cell for cell in nb["cells"] if source(cell).startswith(prefix)]
    if not matches:
        return
    if len(matches) != 1:
        raise RuntimeError(f"Expected one cell beginning {prefix!r}; found {len(matches)}")
    matches[0]["source"] = ""


replace_start(
    "## Optimisation is a modelling problem",
    """## Optimisation is a modelling problem

PSO needs a scalar **objective function**

$$
f:\\mathcal X\\longrightarrow\\mathbb R,
$$

which assigns a numerical value to every feasible candidate $\\mathbf{x}\\in\\mathcal X$. In this Reader we use the minimisation convention,

$$
\\min_{\\mathbf{x}\\in\\mathcal X} f(\\mathbf{x}).
$$

| Object | Meaning |
|---|---|
| $\\mathbf{x}$ | one candidate solution |
| $\\mathcal X$ | feasible search space |
| $f(\\mathbf{x})$ | objective value; smaller is better |
| constraints | conditions defining acceptable candidates |

Some literature calls $f$ a fitness function and maximises it. These are equivalent conventions: maximising a score $S$ can be written as minimising $-S$. Here, *fitness* is used only as the general idea of solution quality; the equations and figures consistently report the objective $f$.

The objective does not merely record success. It defines what success means to the algorithm.
""",
)

replace_start(
    "## Optimisation\n",
    r"""## Optimisation

PSO must be told what a candidate solution is and how its quality will be measured. Let $\mathcal X\subseteq\mathbb R^n$ be the feasible search space. A scalar **objective function**

$$
f:\mathcal X\longrightarrow\mathbb R
$$

assigns a value to each candidate $\mathbf x\in\mathcal X$. We use the minimisation convention,

$$
\min_{\mathbf x\in\mathcal X} f(\mathbf x).
$$

Here $\mathbf x$ is the vector of design variables and the constraints define which values belong to $\mathcal X$. Some sources instead define a fitness score to maximise. The conventions are equivalent: maximising $S(\mathbf x)$ can be written as minimising $f(\mathbf x)=-S(\mathbf x)$.

The objective is part of the model, not merely a measurement added afterwards. It determines which visited positions each particle remembers and which discovery the swarm shares.
""",
)

# The formal statement above replaces four short, overlapping fragments.
clear_start("Generically:")
clear_start("**The objective function**, $f_i(x)$:")
clear_start("$$\n\\min_{x\\in \\mathbb{R}^n} f_i(x)")
clear_start("**The design variables**, $x$:")

replace_start(
    "**Fitness function (objective or cost function).**",
    """**Evaluating a candidate.**

At every visited position, PSO computes $f(\\mathbf{x}_i)$. A particle updates its personal record when

$$
f(\\mathbf{x}_i(t))<f(\\mathbf p_i),
$$

and the shared record is the best personal record,

$$
\\mathbf g=\\arg\\min_{\\mathbf p_i} f(\\mathbf p_i).
$$

The objective is therefore part of the dynamics: it determines which positions are remembered and shared.
""",
)

replace_start(
    "The algorithm aims to find the solution(s) with the highest fitness.",
    """In the worked example,

$$
f(\\mathbf{x})=20+\\sum_{d=1}^{2}\\left[x_d^2-10\\cos(2\\pi x_d)\\right]
$$

is the two-dimensional Rastrigin objective. Its global minimum is $f(\\mathbf 0)=0$, but its many local minima make the search non-trivial. The analysis records the best value of this same $f$ found through time and across repeated runs.
""",
)

replace_start(
    "**Velocity update.**",
    """**Velocity update.**

The random factors are independently drawn for every particle and coordinate. Writing the update for coordinate $d$ avoids introducing a separate element-wise-product symbol:

$$
v_{i,d}(t+1)=w v_{i,d}(t)
+c_1 r_{1,i,d}(t)\\bigl[p_{i,d}-x_{i,d}(t)\\bigr]
+c_2 r_{2,i,d}(t)\\bigl[g_d-x_{i,d}(t)\\bigr],
$$

where $r_{1,i,d},r_{2,i,d}\\sim\\operatorname{Uniform}(0,1)$. Position then changes by

$$
x_{i,d}(t+1)=x_{i,d}(t)+v_{i,d}(t+1).
$$
""",
)

# Add the population-size comparison after the exploration/exploitation sweep.
analysis = next(
    cell
    for cell in nb["cells"]
    if source(cell).startswith("# Analysis")
    and "## Sweep personal and shared influence" in source(cell)
)
text = source(analysis)
addition = """

## Is the swarm doing more than one particle?

With $N=1$, the shared best and personal best belong to the same particle. There is no population across which discoveries can spread. The remaining motion and memory can still search, but this is no longer collective intelligence.

<img src="images/pso_population_size_sweep.png" alt="Ensemble sweep over PSO population size at fixed evaluation budget" style="display:block;width:88%;height:auto;margin:1rem auto;">

This comparison fixes the total number of objective evaluations, not the number of iterations. A larger swarm samples more positions per iteration but receives fewer iterations at the same computational cost. The single-particle baseline is substantially less reliable on this landscape; a modest population benefits from sharing discoveries. Beyond that, more particles are not automatically better. Population size should therefore be treated as a model and computational-budget choice, and claims should be based on repeated runs.
"""
if "## Is the swarm doing more than one particle?" not in text:
    analysis["source"] = text.rstrip() + addition

# Use each canonical DOI exactly once. The body links are sufficient for the generated list.
for cell in nb["cells"]:
    if source(cell).startswith("# Scope and connections"):
        cell["source"] = "# Scope and connections\n"

for cell in nb["cells"]:
    value = source(cell)
    value = value.replace(
        "See Dorigo et al. (1996), [Ant system: optimization by a colony of cooperating agents](https://ieeexplore.ieee.org/document/484436).",
        "See Dorigo, Maniezzo and Colorni (1996), [Ant system: optimization by a colony of cooperating agents](https://doi.org/10.1109/3477.484436).",
    )
    # Keep the PSO DOI in its first substantive occurrence only.
    value = value.replace(
        "Kennedy and Eberhart describe this development in the original [particle swarm optimisation paper](https://doi.org/10.1109/ICNN.1995.488968).",
        "Kennedy and Eberhart describe this development in the original [particle swarm optimisation paper](https://doi.org/10.1109/ICNN.1995.488968).",
    )
    cell["source"] = value

path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
print(path)
