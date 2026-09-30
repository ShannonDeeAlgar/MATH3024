"""Start the general game comparison as a new horizontal slide stream."""

from pathlib import Path
import json


NOTEBOOK = Path("notebooks/week10/L_Game_theory.ipynb")
TARGET_ID = "w10-comparing-game-types"


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    for cell in notebook["cells"]:
        if cell.get("id") == TARGET_ID:
            metadata = cell.setdefault("metadata", {})
            slideshow = metadata.setdefault("slideshow", {})
            slideshow["slide_type"] = "slide"
            break
    else:
        raise SystemExit(f"Could not find cell {TARGET_ID}")

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
