import json
from copy import deepcopy
from pathlib import Path


path = Path("notebooks/week09/L_InformationTheory.ipynb")
nb = json.loads(path.read_text())
cells = nb["cells"]


def tags(cell):
    return cell.setdefault("metadata", {}).setdefault("tags", [])


def reader_only(i):
    t = tags(cells[i])
    if "reader-only" not in t:
        t.append("reader-only")
    cells[i].setdefault("metadata", {}).pop("slideshow", None)


def slide_cell(source, slide_type="subslide", extra_tags=None):
    return {
        "cell_type": "markdown",
        "metadata": {
            "slideshow": {"slide_type": slide_type},
            "tags": list(extra_tags or ["slides-only"]),
        },
        "source": [line + "\n" for line in source.strip().splitlines()],
    }


# The lecture has one hour. Keep the full argument in the Reader, but replace
# four separate framing slides with one concise question-led slide.
for i in (4, 6, 8, 11, 13):
    reader_only(i)

framing = slide_cell(r"""
## Why measure information?

Across the unit we have repeatedly replaced a detailed system by a smaller description:

- counts and distributions,
- ensemble averages and variation,
- scaling exponents and fractal dimension,
- order parameters, correlations and transition locations.

Information theory asks what these summaries retain, what they discard, and how uncertain the remaining outcomes are.
""")
cells.insert(4, framing)

# Indices below refer to the original notebook, so account for the insertion.
def old(i):
    return i + 1 if i >= 4 else i


# Reader-rich material that need not become an individual lecture slide.
for i in (19, 25, 27, 29, 34, 38, 39, 40, 41, 42, 59, 60, 61, 62,
          72, 77, 80, 82, 83, 84, 86):
    reader_only(old(i))

# Keep the surprise requirements together rather than staging six clicks.
cells[old(37)]["source"] = [line + "\n" for line in r"""
## What should surprise do?

For an outcome $x$, a sensible surprise $h(x)$ should:

1. decrease as $P(x)$ increases;
2. be zero for a certain event;
3. add for independent events; and
4. vary continuously with probability.

These requirements lead to $h(x)=-\log P(x)$.
""".strip().splitlines()]

# Reader iframe path is relative to the built page directory. Slides need a
# same-directory path, so give each output its own cell.
widget_i = old(52)
reader_only(widget_i)
reader_src = "".join(cells[widget_i]["source"]).replace(
    'src="entropy_distribution_explorer.html"',
    'src="../entropy_distribution_explorer.html"',
)
cells[widget_i]["source"] = reader_src.splitlines(keepends=True)
slide_src = reader_src.replace(
    'src="../entropy_distribution_explorer.html"',
    'src="entropy_distribution_explorer.html"',
)
cells.insert(widget_i + 1, slide_cell(slide_src))

# Repair accidental control characters introduced in the dropdown equation.
for cell in cells:
    src = "".join(cell.get("source", []))
    src = src.replace("\\log_2 6\x07pprox 2.585\text{ bits}",
                      "\\log_2 6 \\approx 2.585\\,\\text{bits}")
    src = src.replace("\\log_2 6\x07pprox 2.585\text{ bits}",
                      "\\log_2 6 \\approx 2.585\\,\\text{bits}")
    src = src.replace("\\log_2 6\x07pprox 2.585\text{ bits}",
                      "\\log_2 6 \\approx 2.585\\,\\text{bits}")
    # Also handle literal bell/tab characters.
    src = src.replace("\\log_2 6\a pprox 2.585\t ext{ bits}",
                      "\\log_2 6 \\approx 2.585\\,\\text{bits}")
    src = src.replace("\\log_2 6\a", "\\log_2 6 \\a")
    src = src.replace("pprox 2.585\text{ bits}", "pprox 2.585\\,\\text{bits}")
    cell["source"] = src.splitlines(keepends=True)

# The final summary is useful in both outputs and should be the final slide.
for cell in cells:
    if "Information measures at a glance · Shannon entropy" in "".join(cell.get("source", [])):
        cell.setdefault("metadata", {})["slideshow"] = {"slide_type": "slide"}
        break

nb["cells"] = cells
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
