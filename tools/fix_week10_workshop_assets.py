import json
from pathlib import Path

p = Path("notebooks/week10/WS_Game_theory.ipynb")
nb = json.loads(p.read_text())

missing = {
    '<img src="DarwinsFinches.jpeg" width="300"/>',
    '<img src="Evolution_ApeMan_Linear.png" width="300"/>',
    '<img src="Evolution_ApeMan_Proper.jpeg" width="300"/>',
    '<img src="Axelrod_PD.png" width="300"/>',
    '<img src="Axelrod_TournamentResults.png" width="600"/>',
    '<img src="LecturesCompleted_PythonScreenShot.png" width="400"/>',
}

for cell in nb["cells"]:
    src = "".join(cell.get("source", []))
    for image in missing:
        src = src.replace(image, "")
    src = src.replace(
        '<img src="Iterated_Prisoners_Dilemma_Venn-Diagram.svg" width="600"/>',
        '<img src="images/Iterated_Prisoners_Dilemma_Venn-Diagram.png" width="600"/>',
    )
    cell["source"] = src.splitlines(keepends=True)

p.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
