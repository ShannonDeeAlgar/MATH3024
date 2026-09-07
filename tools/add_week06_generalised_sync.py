"""Add generalised synchronisation to the Week 6 taxonomy."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"

nb = json.loads(PATH.read_text())
by_id = {cell.get("id"): cell for cell in nb["cells"]}

slide = by_id["sync-types-slide"]
slide["source"] = [
    line + "\n"
    for line in r"""
## Several forms of synchronisation

<img src="images/synchronisation_types.svg" alt="Seven phase-circle and time-series comparisons of forms of synchronisation" style="display:block;width:96%;max-height:510px;margin:0 auto">

**Generalised synchronisation:** the states maintain a functional relationship, such as $y(t)=F(x(t))$, without becoming equal.
""".strip().splitlines()
]

reader = by_id["w6-types-of-synchronisation-reader"]
text = "".join(reader["source"])
addition = r"""

**Generalised synchronisation:** the states maintain a stable functional relationship

$$
\mathbf y(t)=F\!\left(\mathbf x(t)\right),
$$

without requiring equal states or equal observable signals. Complete synchronisation, $\mathbf y=\mathbf x$, and projective synchronisation, $\mathbf y=a\mathbf x$, are special cases. A relationship such as $y(t)=\sin(x(t))$ would count if coupling establishes and maintains it.

An observed relationship alone is not sufficient evidence: two uncoupled systems driven by the same external signal may also trace a consistent relationship. The synchronisation claim concerns a relationship maintained by the coupled dynamics.
"""

if "**Generalised synchronisation:**" not in text:
    text = text.rstrip() + addition + "\n"
reader["source"] = [line + "\n" for line in text.rstrip().splitlines()]

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
