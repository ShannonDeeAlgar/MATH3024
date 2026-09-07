import json
from pathlib import Path


path = Path("notebooks/week05/L_ABM.ipynb")
notebook = json.loads(path.read_text())

for cell in notebook["cells"]:
    text = "".join(cell.get("source", []))
    if text.lstrip().startswith("## What goes into an agent-based model?"):
        text = text.replace("## What goes into an agent-based model?", "# What goes into an agent-based model?", 1)
        cell["source"] = text.splitlines(keepends=True)
        cell.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "slide"
    elif text.lstrip().startswith("# History can matter"):
        cell.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "slide"

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
