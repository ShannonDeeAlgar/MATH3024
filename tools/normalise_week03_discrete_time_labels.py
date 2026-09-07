"""Use n for discrete time levels in the Week 3 grid assets."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "notebooks/week03/images"

for name in ("diffusion_grid_numbers_t012.svg", "diffusion_grid_t012.svg"):
    path = ROOT / name
    text = path.read_text()
    for value in (0, 1, 2):
        text = text.replace(f">t = {value}<", f">n = {value}<")
    path.write_text(text)
