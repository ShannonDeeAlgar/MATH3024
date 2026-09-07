"""Execute self-contained Week 3 display cells and retain their outputs."""
from copy import deepcopy
from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
TARGETS = {
    "17066138-6d3a-4b3a-bde7-a0eff02be124",
    "b5d00706-c39f-46f7-81a4-13163ae17b2c",
    "8144df44-2247-4e76-9a97-88e785929c07",
}
nb = nbformat.read(PATH, as_version=4)
for cell in nb.cells:
    if cell.id not in TARGETS:
        continue
    mini = nbformat.v4.new_notebook(cells=[deepcopy(cell)])
    ExecutePreprocessor(timeout=180, kernel_name="python3").preprocess(
        mini, {"metadata": {"path": str(PATH.parent)}}
    )
    cell.outputs = mini.cells[0].outputs
    cell.execution_count = mini.cells[0].execution_count
nbformat.write(nb, PATH)
