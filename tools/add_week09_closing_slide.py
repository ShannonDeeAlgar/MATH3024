import json
from pathlib import Path

p = Path("notebooks/week09/L_InformationTheory.ipynb")
nb = json.loads(p.read_text())

source = r"""
# Shannon entropy at a glance

**Object:** a stated random variable or observed symbol sequence.

**Representation:** outcomes and their probabilities.

**Measure:**

$$
H(X)=-\sum_x P(x)\log_2 P(x).
$$

Entropy retains average uncertainty and discards outcome meaning and temporal order unless those are built into the chosen symbols.
""".strip()

if not any("# Shannon entropy at a glance" in "".join(c.get("source", [])) for c in nb["cells"]):
    nb["cells"].append({
        "cell_type": "markdown",
        "metadata": {
            "tags": ["slides-only"],
            "slideshow": {"slide_type": "slide"},
        },
        "source": [line + "\n" for line in source.splitlines()],
    })

p.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
