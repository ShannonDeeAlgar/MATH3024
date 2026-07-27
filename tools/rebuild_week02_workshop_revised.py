#!/usr/bin/env python3
"""Build the student-facing Week 2 fractals workshop."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "notebooks/week02/WS_Fractals.ipynb"


def md(source: str, cell_id: str):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def code(source: str, cell_id: str):
    cell = nbf.v4.new_code_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def main() -> None:
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "math3024_workshop_format": "blue-period-v3",
    }
    nb.cells = [
        md(r"""
# Week 2 workshop · Build, measure, explain

> **Exact object to finite estimate:** Construct → check → rasterise → count boxes → estimate dimension → test sensitivity.

## Workshop focus

The lecture and Reader introduce the ideas. Here you will actively reconstruct and test them by:

- implementing the Sierpiński construction;
- checking the implementation against its known scaling relationships;
- estimating its box-counting dimension from a finite raster;
- testing how measurement choices affect that estimate.
""", "week02-revised-guide"),

        md(r"""
# From the lecture to the workshop

The lecture used the Cantor set and Sierpiński triangle to ask how visible detail changes with scale. Here we will focus on the Sierpiński triangle, to carry the full calculation from an exact construction to a finite estimate.

The exact dimension is our benchmark. The difference between that benchmark and a finite estimate helps us diagnose sampling, resolution, and scale-range effects.
""", "lecture-connection"),

        code(r'''
import sys
from typing import Sequence

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from PIL import Image, ImageDraw

SEED = 3024
INK = "#1B2A4C"
YELLOW = "#EDCC55"
BLUE = "#5879AA"

print(f"Python {sys.version_info.major}.{sys.version_info.minor} · NumPy {np.__version__} · Matplotlib {matplotlib.__version__}")
print(f"Reproducible baseline seed: {SEED}")
''', "setup"),

        md(r"""
# Construct the Sierpiński triangle

At each step, replace one triangle by three half-scale copies.

> **Discuss:** Use the known relationships at depth \(d\) to specify checks that the construction code must pass.
""", "sierpinski-intro"),

        code(r'''
EQUILATERAL = np.array(
    [[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3.0) / 2.0]]
)


def sierpinski_triangles(depth: int, triangle: np.ndarray = EQUILATERAL) -> np.ndarray:
    """Return the filled triangles remaining after `depth` recursive subdivisions."""
    if not isinstance(depth, (int, np.integer)) or depth < 0:
        raise ValueError("depth must be a non-negative integer")
    triangle = np.asarray(triangle, dtype=float)
    if triangle.shape != (3, 2):
        raise ValueError("triangle must contain three 2D vertices")
    if depth == 0:
        return triangle[np.newaxis, :, :]

    a, b, c = triangle
    ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
    children = (
        np.array([a, ab, ca]),
        np.array([ab, b, bc]),
        np.array([ca, bc, c]),
    )
    return np.concatenate([sierpinski_triangles(depth - 1, child) for child in children])
''', "sierpinski-function"),

        code(r'''
def triangle_area(triangle: np.ndarray) -> float:
    a, b, c = triangle
    twice_area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return abs(twice_area) / 2


original_area = triangle_area(EQUILATERAL)
for depth in range(6):
    triangles = sierpinski_triangles(depth)
    assert len(triangles) == 3**depth
    remaining_area = sum(triangle_area(t) for t in triangles)
    assert np.isclose(remaining_area / original_area, (3.0 / 4.0) ** depth)

print("All Sierpiński-triangle tests passed.")
''', "sierpinski-tests"),

        code(r'''
def plot_sierpinski_iterations(depths: Sequence[int] = range(6)):
    fig, axes = plt.subplots(1, len(depths), figsize=(12, 2.4))
    axes = np.atleast_1d(axes)
    for ax, depth in zip(axes, depths):
        collection = PolyCollection(
            sierpinski_triangles(depth), facecolor=INK, edgecolor="none"
        )
        ax.add_collection(collection)
        ax.set(xlim=(0, 1), ylim=(0, np.sqrt(3)/2), aspect="equal", title=f"Depth {depth}")
        ax.axis("off")
    fig.tight_layout()
    return fig, axes


plot_sierpinski_iterations()
plt.show()
''', "plot-sierpinski"),

        md(r"""
The exact similarity dimension follows directly from three copies scaled by one half:

$$D_{\mathrm{exact}}=\frac{\log 3}{\log 2}\approx1.585.$$

We will now treat a finite rendering as data and see how closely box counting recovers this benchmark.
""", "exact-dimension"),

        md(r"""
# Create a finite observation

Box counting operates on finite observations. We therefore rasterise a finite-depth Sierpiński triangle directly, without saving and reloading a plot with axes, margins, or antialiasing.

> **Modelling choice:** Construction depth, raster resolution, padding, and grid alignment are measurement choices.
""", "ifs-intro"),

        code(r'''
def rasterise_triangles(
    triangles: np.ndarray,
    resolution: int = 512,
    padding_fraction: float = 0.02,
) -> np.ndarray:
    """Rasterise filled triangles directly into a square Boolean array."""
    if resolution < 2:
        raise ValueError("resolution must be at least two")
    if not 0 <= padding_fraction < 0.5:
        raise ValueError("padding_fraction must lie in [0, 0.5)")

    image = Image.new("1", (resolution, resolution), 0)
    draw = ImageDraw.Draw(image)
    usable = 1 - 2 * padding_fraction
    for triangle in np.asarray(triangles):
        pixels = [
            (
                resolution * (padding_fraction + usable * x),
                resolution * (1 - padding_fraction - usable * y / (np.sqrt(3) / 2)),
            )
            for x, y in triangle
        ]
        draw.polygon(pixels, fill=1)
    return np.asarray(image, dtype=bool)


fractal_image = rasterise_triangles(sierpinski_triangles(depth=7), resolution=512)
assert fractal_image.shape == (512, 512)
print(f"occupied pixels: {fractal_image.sum():,} of {fractal_image.size:,}")
plt.figure(figsize=(5, 5))
plt.imshow(fractal_image, cmap="Greys", origin="upper")
plt.axis("off")
plt.show()
''', "chaos-game"),

        md(r"""
# Count occupied boxes

For box width $\varepsilon$, let $N(\varepsilon)$ be the number of boxes containing at least one occupied pixel. If

$$N(\varepsilon)\propto\varepsilon^{-D},$$

then the slope of $\log N$ against $\log(1/\varepsilon)$ estimates $D$.

The implementation reshapes the array into blocks and reduces each block once. It does not create thousands of plotting rectangles.
""", "box-count-intro"),

        code(r'''
def occupied_blocks(image: np.ndarray, box_size: int) -> np.ndarray:
    """Return a Boolean grid indicating which non-overlapping boxes are occupied."""
    image = np.asarray(image, dtype=bool)
    if image.ndim != 2:
        raise ValueError("image must be two-dimensional")
    height, width = image.shape
    if box_size < 1 or height % box_size or width % box_size:
        raise ValueError("box_size must be a positive divisor of both image dimensions")
    return image.reshape(
        height // box_size, box_size, width // box_size, box_size
    ).any(axis=(1, 3))


def box_counts(image: np.ndarray, box_sizes: Sequence[int]) -> np.ndarray:
    """Count occupied boxes at each requested scale."""
    sizes = np.asarray(box_sizes, dtype=int)
    if sizes.ndim != 1 or sizes.size < 2:
        raise ValueError("provide at least two box sizes")
    return np.array([occupied_blocks(image, int(size)).sum() for size in sizes])


test_image = np.eye(8, dtype=bool)
assert np.array_equal(box_counts(test_image, [1, 2, 4]), [8, 4, 2])
print("Box-counting test passed.")
''', "box-count-functions"),

        code(r'''
box_sizes = np.array([2, 4, 8, 16, 32, 64])
counts = box_counts(fractal_image, box_sizes)

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
for ax, size in zip(axes, [8, 32, 64]):
    blocks = occupied_blocks(fractal_image, size)
    ax.imshow(blocks, cmap="Greys", interpolation="nearest", origin="upper")
    ax.set(title=f"Box width {size}\n{blocks.sum()} occupied", xticks=[], yticks=[])
fig.tight_layout()
plt.show()
''', "visualise-boxes"),

        code(r'''
def fit_box_dimension(
    image: np.ndarray,
    box_sizes: Sequence[int],
) -> tuple[float, float, np.ndarray]:
    """Return slope, intercept, and counts for a specified finite scale range."""
    sizes = np.asarray(box_sizes, dtype=int)
    counts = box_counts(image, sizes)
    if np.any(counts <= 0):
        raise ValueError("all selected scales must contain occupied boxes")
    inverse_scale = image.shape[0] / sizes
    slope, intercept = np.polyfit(np.log(inverse_scale), np.log(counts), 1)
    return float(slope), float(intercept), counts


estimate, intercept, counts = fit_box_dimension(fractal_image, box_sizes)
exact = np.log(3) / np.log(2)
x = np.log(fractal_image.shape[0] / box_sizes)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, np.log(counts), "o", color=BLUE, label="Measured counts")
ax.plot(x, estimate * x + intercept, color=INK, label=f"Fit: D = {estimate:.3f}")
ax.set(xlabel=r"$\log(1/\varepsilon)$", ylabel=r"$\log N(\varepsilon)$")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False)
plt.show()

print(f"finite raster estimate: {estimate:.4f}")
print(f"exact similarity dimension: {exact:.4f}")
print(f"absolute difference: {abs(estimate-exact):.4f}")
assert abs(estimate - exact) < 0.1
''', "estimate-dimension"),

        md(r"""
# How sensitive is the estimate?

The estimate should not equal the exact dimension perfectly. We have replaced an infinite set and a limit as $\varepsilon\to0$ with:

- a finite construction depth;
- a finite pixel grid;
- square boxes aligned to one origin;
- a short and subjective scale range;
- an ordinary least-squares line fit.

> **Discuss:** Which of these choices could move the estimate up or down? Which can be checked without knowing the exact answer?
""", "bias-discussion"),

        code(r'''
scale_ranges = {
    "fine to medium": [2, 4, 8, 16, 32],
    "middle": [4, 8, 16, 32],
    "medium to coarse": [8, 16, 32, 64],
}

for label, sizes in scale_ranges.items():
    dimension, _, _ = fit_box_dimension(fractal_image, sizes)
    print(f"{label:>16}: D = {dimension:.4f}")
''', "scale-sensitivity"),

        md(r"""
> **The ladder of abstraction:** Move down to inspect pixels and occupied boxes. Move up to compress their scaling relationship into one estimated exponent.

A dimension estimate without its resolution, scale range, and uncertainty is incomplete evidence.
""", "ladder-summary"),

        md(r"""
# Choose an extension

### A · Resolution and depth

Repeat the estimate at several construction depths and raster resolutions. Identify where finite-depth detail or pixel resolution limits the fitted range.

### B · Grid sensitivity

Shift the box-grid origin or change raster resolution. Identify a scale range that is reasonably stable.

### C · Another construction

Implement the Sierpiński carpet. Compare its exact similarity dimension with a finite raster estimate.

### D · Natural data

Apply the method to a supplied coastline or branching image. Document thresholding, cropping, resolution, and the scale range used.

""", "extensions"),

        code(r'''
# Your extension goes here.

''', "student-extension"),

        md(r"""
# Exit ticket

In three sentences:

1. State the scaling relationship used to define or estimate dimension.
2. Name one computational choice that affected the estimate.
3. Explain why a straight-looking log–log plot is not sufficient evidence on its own.
""", "exit-ticket"),
    ]

    nbf.write(nb, TARGET)
    print(f"Wrote {TARGET} ({len(nb.cells)} cells)")


if __name__ == "__main__":
    main()
