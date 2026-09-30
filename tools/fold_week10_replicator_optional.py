"""Move the worked Week 10 replicator example into the optional reader box."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week10/L_Game_theory.ipynb"
MANIFEST = ROOT / "tools/equation_consistency.json"


OPTIONAL = r'''```{dropdown} Optional · non-assessed detail: a simple frequency model
<div class="optional-reader-flag"><strong>Optional · non-assessed detail</strong> This is a standard idealised model, included for students who want the formal version. For a worked computational treatment, see Allen Downey’s <a href="https://greenteapress.com/wp/think-complexity-2e/"><em>Think Complexity</em></a>.</div>

Replicator dynamics describes how the shares of fixed strategies change when they earn different expected payoffs. It is a population model, not another rule for choosing an action within a match.

In a **well-mixed population**, agents meet random opponents. During one generation each agent keeps its strategy and receives its expected payoff. Between generations, strategies with higher payoff are copied or reproduced more often. The model does not specify one named copier and one named role model; it describes the average change in the population. With no mutation, a strategy that is absent cannot reappear.

Let $x_s$ be the fraction using strategy $s$, and let $pi_s(mathbf{x})$ be its expected payoff in the current mixture. The population mean payoff is

$$
\bar\pi(\mathbf{x})=\sum_s x_s\pi_s(\mathbf{x}).
$$

The standard continuous-time **replicator equation** is

$$
\dot{x}_s=x_s\left[\pi_s(\mathbf{x})-\bar\pi(\mathbf{x})\right].
$$

The share grows when the strategy earns more than the population mean and falls when it earns less. The factor $x_s$ means that a strategy can only increase from copies that already exist. This equation assumes a large, well-mixed population, faithful inheritance and deterministic expected payoffs; finite populations add sampling noise.

This is the standard deterministic mean-field starting point, not the only evolutionary model. Finite-population Moran or Wright–Fisher models make birth, replacement and sampling explicit.

For a simple discrete simulation, use an Euler step of this equation. Let $x_t$ be the share using Cooperate in a Prisoner’s Dilemma. The expected payoffs in one random encounter are

$$
\pi_C=x_tR+(1-x_t)S,\qquad \pi_D=x_tT+(1-x_t)P,
$$

and

$$
\bar{\pi}=x_t\pi_C+(1-x_t)\pi_D,\qquad x_{t+1}=x_t+\eta x_t(\pi_C-\bar{\pi}),\qquad \eta=0.2.
$$

Here $\eta$ is a step size, not a new payoff parameter. With $(T,R,P,S)=(5,3,1,0)$, Defect has the higher expected payoff at every mixture. Starting from equal shares, cooperation falls from $0.50$ to about $0.065$ by generation 10 and $0.001$ by generation 30. This result follows from this payoff, matching and update rule; it is not a general prediction for every population model.

<div class="image-panel"><img src="images/pd_replicator_dynamics.svg" alt="Discrete replicator dynamics in a well-mixed Prisoner's Dilemma population: cooperation falls and defection rises from several initial mixtures." style="width:100%;max-height:330px;object-fit:contain"><p class="figure-caption" id="fig-w10-9"><strong>Figure 10.9.</strong> Discrete replicator update for the Prisoner’s Dilemma. Cooperation falls and defection rises from several initial mixtures.</p></div>

This is one possible update rule. Changing the matching, inheritance, mutation or selection rule changes the population model and may change the result.

```
'''


def math_signature(source: str) -> str | None:
    math = re.compile(r"\$\$(.*?)\$\$|(?<!\\)\$(?!\$)(.*?)(?<!\\)\$|\\\[(.*?)\\\]|\\\((.*?)\\\)", re.S)
    values = []
    for match in math.finditer(source):
        value = next(group for group in match.groups() if group is not None)
        values.append(re.sub(r"\s+", "", value))
    if not values:
        return None
    return hashlib.sha256(json.dumps(values).encode()).hexdigest()


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cells["w10-evolution-action"]["source"] = [""]
    cells["w10-evolutionary-ipd"]["source"] = [
        "### Letting tournament strategies change\n",
        "\n",
        "After the fixed-strategy comparison, let payoff-dependent copying or reproduction change the shares of those strategies. The population then supplies a changing opponent field.\n",
        "\n",
        "Evolution changes strategy frequencies, so the opponents encountered also change. **Fitness** means expected reproductive or copying success. We specify how payoff affects fitness and how the population updates.\n",
        "\n",
        "Figure 10.8 gives one finite, well-mixed implementation using payoff-dependent copying. Other choices of matching, inheritance, mutation or selection give different population models.\n",
        "\n",
        "| Process | Model decision |\n",
        "|---|---|\n",
        "| **Selection** | how payoff changes the expected number of descendants or copies |\n",
        "| **Inheritance** | how strategies pass to descendants |\n",
        "| **Mutation** | whether copied strategies can change, and how often |\n",
    ]
    cells["w10-spatial-evolution"]["source"] = OPTIONAL.splitlines(keepends=True)
    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    manifest = json.loads(MANIFEST.read_text())
    signatures = manifest["notebooks"]["notebooks/week10/L_Game_theory.ipynb"]["math_signatures"]
    signatures.pop("w10-evolution-action", None)
    signatures["w10-spatial-evolution"] = math_signature(OPTIONAL)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
