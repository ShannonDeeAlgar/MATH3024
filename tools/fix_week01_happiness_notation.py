"""Make h_i consistently denote happiness, never unhappiness, in Week 1."""
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]
paths = [
    ROOT / "notebooks/week01/L_Introduction_to_complex_systems.ipynb",
    ROOT / "notebooks/week01/WS_Introduction_to_complex_systems.ipynb",
]

replacements = {
    "Define unhappiness by $h_i=1$ when $s_i&lt;\\\\theta_s$, and $h_i=0$ otherwise.":
        "Define happiness by $h_i=1$ when $s_i\\\\geq\\\\theta_s$, and $h_i=0$ otherwise. An agent moves when $h_i=0$.",
    "**Unhappiness:** define $h_i=1$ when $s_i<\\\\theta_s$, and $h_i=0$ otherwise.":
        "**Happiness:** define $h_i=1$ when $s_i\\\\geq\\\\theta_s$, and $h_i=0$ otherwise. An agent is dissatisfied when $h_i=0$.",
    "$\\displaystyle D=\\sum_{i=1}^{N}h_i$":
        "$\\displaystyle D=\\sum_{i=1}^{N}(1-h_i)$",
    "D=\\\\sum_{i=1}^{N}h_i.":
        "D=\\\\sum_{i=1}^{N}(1-h_i).",
    "def get_unhappiness(grid, threshold):":
        "def get_happiness(grid, threshold):",
    '\"\"\"Return 1 for a dissatisfied agent, 0 for a satisfied agent, and NaN if empty.\"\"\"':
        '\"\"\"Return 1 for a satisfied agent, 0 for a dissatisfied agent, and NaN if empty.\"\"\"',
    "np.where(np.isnan(ratios), np.nan, (ratios < threshold).astype(float))":
        "np.where(np.isnan(ratios), np.nan, (ratios >= threshold).astype(float))",
}

for path in paths:
    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        for old, new in replacements.items():
            cell.source = cell.source.replace(old, new)
        cell.source = cell.source.replace(
            r"Define unhappiness by $h_i=1$ when $s_i&lt;\theta_s$, and $h_i=0$ otherwise.",
            r"Define happiness by $h_i=1$ when $s_i\geq\theta_s$, and $h_i=0$ otherwise. An agent moves when $h_i=0$.",
        )
        cell.source = cell.source.replace(
            r"**Unhappiness:** define $h_i=1$ when $s_i<\theta_s$, and $h_i=0$ otherwise.",
            r"**Happiness:** define $h_i=1$ when $s_i\geq\theta_s$, and $h_i=0$ otherwise. An agent is dissatisfied when $h_i=0$.",
        )
        cell.source = cell.source.replace(
            r"D=\sum_{i=1}^{N}h_i.",
            r"D=\sum_{i=1}^{N}(1-h_i).",
        )
    nbformat.write(nb, path)
