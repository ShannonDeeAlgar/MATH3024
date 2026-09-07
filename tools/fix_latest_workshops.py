#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update_cell(nb, cell_id, transform):
    cell = next(c for c in nb["cells"] if c.get("id") == cell_id)
    cell["source"] = transform("".join(cell["source"]))


def week08():
    path = ROOT / "notebooks/week08/WS_Critical_phenomena.ipynb"
    nb = json.loads(path.read_text())
    update_cell(nb, "w8-check-code", lambda s: s.replace(
        "L=32, additions=25_000, burn_in=6_000",
        "L=32, additions=10_000, burn_in=2_500",
    ))
    update_cell(nb, "w8-fit", lambda s: s.replace(
        "counts, edges = np.histogram(values, bins=edges)\n    centres = np.sqrt(edges[:-1] * edges[1:])\n    keep = counts > 0\n    return centres[keep], counts[keep]",
        "counts, edges = np.histogram(values, bins=edges)\n    centres = np.sqrt(edges[:-1] * edges[1:])\n    density = counts / np.diff(edges)\n    keep = counts > 0\n    return centres[keep], density[keep]",
    ).replace("[(3, 80), (8, 180)]", "[(2, 50), (5, 120)]"))
    update_cell(nb, "w8-finite-code", lambda s: s.replace(
        "[(24, 22_000, 5_000), (48, 45_000, 10_000)]",
        "[(24, 8_000, 2_000), (40, 14_000, 3_500)]",
    ).replace("y / y.sum()", "y / np.trapezoid(y, x)").replace("np.trapz(y, x)", "np.trapezoid(y, x)"))
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


def week09():
    path = ROOT / "notebooks/week09/WS_Information_theory.ipynb"
    nb = json.loads(path.read_text())
    update_cell(nb, "w9w-distribution-plot", lambda s: s.replace(
        'ax.set(title=f"{name}\nH={shannon_entropy(p):.3f} bits", xlabel="Outcome", ylim=(0, 1))',
        'ax.set(title=f"{name}: H={shannon_entropy(p):.3f} bits", xlabel="Outcome", ylim=(0, 1))',
    ))
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    week08()
    week09()
