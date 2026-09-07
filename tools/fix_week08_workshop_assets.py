#!/usr/bin/env python3
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "notebooks/week08/WS_Critical_phenomena.ipynb"
data = json.loads(path.read_text())

assets = {
    'src="Sand_Distributions2.png"': 'src="images/Downey_sand_avalanche_quantified_log.png"',
    'src="Sand_Fractals.png"': 'src="images/Downey_sand_fractals.png"',
    'src="Sand_FractalBoxCounting.png"': 'src="images/Downey_sand_fractals_box_counting.png"',
    'src="Sand_PowerSpectra.png"': 'src="images/Downey_sand_power_spectra.png"',
    'src="Renormalisation_Sayama.png"': 'src="images/Sayama_renormalisation_scale2.png"',
    'src="Renormalisation2_Sayama.png"': 'src="images/Sayama_renormalisation_scale4.png"',
}

for cell in data["cells"]:
    value = "".join(cell.get("source", []))
    for old, new in assets.items():
        value = value.replace(old, new)
    value = value.replace("\\begin{equation*}\n", "$$\n").replace("\\end{equation*}\n", "$$\n")
    value = value.replace("a straight line with slope $\\beta$", "a straight line with slope $-\\beta$")
    value = value.replace("Binarised sand piles for $z=\\{0,1,2,3\\}$:", "Binarised sandpile subsets at grain levels 0, 1, 2 and 3:")
    cell["source"] = value.splitlines(keepends=True)

path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
