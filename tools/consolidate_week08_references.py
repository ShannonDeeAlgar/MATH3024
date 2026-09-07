import json
from pathlib import Path


path = Path("notebooks/week08/L_Critical_phenomena.ipynb")
notebook = json.loads(path.read_text())
matches = [
    cell
    for cell in notebook["cells"]
    if "".join(cell.get("source", [])).startswith("# References\n")
]
if len(matches) != 1:
    raise RuntimeError(f"Expected one manual References cell; found {len(matches)}")

references = [
    ("Sayama (2015)", "https://math.libretexts.org/Bookshelves/Scientific_Computing_Simulations_and_Modeling/Introduction_to_the_Modeling_and_Analysis_of_Complex_Systems_(Sayama)"),
    ("Bak, Tang and Wiesenfeld (1987)", "https://doi.org/10.1103/PhysRevLett.59.381"),
    ("Bak, Tang and Wiesenfeld (1988)", "https://doi.org/10.1103/PhysRevA.38.364"),
    ("Bak, Chen and Tang (1990)", "https://doi.org/10.1016/0375-9601(90)90451-S"),
    ("Drossel and Schwabl (1992)", "https://doi.org/10.1103/PhysRevLett.69.1629"),
    ("Olami, Feder and Christensen (1992)", "https://doi.org/10.1103/PhysRevLett.68.1244"),
]
links = "\n".join(f'<a href="{url}">{label}</a><br>' for label, url in references)
matches[0]["source"] = (
    '<div class="reference-register" style="display:none" aria-hidden="true">\n'
    f"{links}\n"
    "</div>\n"
).splitlines(keepends=True)
tags = matches[0].setdefault("metadata", {}).setdefault("tags", [])
if "reader-only" not in tags:
    tags.append("reader-only")

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
