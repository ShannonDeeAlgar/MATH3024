"""Generate a box-counting diagnostic from the Week 2 Britain silhouette."""

from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "notebooks/week02/images/British_coastline.png"
TARGET = ROOT / "notebooks/week02/images/britain_boxcount_diagnostic.svg"


def occupied_box_count(mask: np.ndarray, box_size: int) -> int:
    """Count boxes crossed by the land/background boundary."""
    height, width = mask.shape
    padded_height = int(np.ceil(height / box_size) * box_size)
    padded_width = int(np.ceil(width / box_size) * box_size)
    padded = np.zeros((padded_height, padded_width), dtype=bool)
    padded[:height, :width] = mask
    blocks = padded.reshape(
        padded_height // box_size,
        box_size,
        padded_width // box_size,
        box_size,
    ).transpose(0, 2, 1, 3)
    return int(
        np.count_nonzero(
            blocks.any(axis=(2, 3)) & (~blocks).any(axis=(2, 3))
        )
    )


rgba = np.asarray(Image.open(SOURCE).convert("RGBA"))
land = (rgba[..., 3] > 20) & (rgba[..., :3].mean(axis=2) < 210)
box_sizes = np.array([2, 4, 8, 16, 32, 64, 128, 256], dtype=int)
counts = np.array([occupied_box_count(land, size) for size in box_sizes])
x = np.log(1 / box_sizes.astype(float))
y = np.log(counts)

fit_indices = np.arange(1, 6)
slope, intercept = np.polyfit(x[fit_indices], y[fit_indices], 1)

width, height = 1000, 620
left, right, top, bottom = 105, 55, 72, 100
plot_width = width - left - right
plot_height = height - top - bottom
x_min, x_max = x.min() - 0.15, x.max() + 0.15
y_min, y_max = y.min() - 0.2, y.max() + 0.2


def sx(value: float) -> float:
    return left + (value - x_min) / (x_max - x_min) * plot_width


def sy(value: float) -> float:
    return top + (y_max - value) / (y_max - y_min) * plot_height


fit_x0, fit_x1 = x[fit_indices].min(), x[fit_indices].max()
fit_y0, fit_y1 = slope * fit_x0 + intercept, slope * fit_x1 + intercept
points = "\n".join(
    f'<circle cx="{sx(xv):.1f}" cy="{sy(yv):.1f}" r="8" fill="#1B2A4C"/>'
    for xv, yv in zip(x, y)
)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{width/2}" y="38" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#1B2A4C">Box counting of a rasterised British coastline</text>
<rect x="{sx(fit_x1):.1f}" y="{top}" width="{sx(fit_x0)-sx(fit_x1):.1f}" height="{plot_height}" fill="#D5A62A" opacity="0.10"/>
<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#1B2A4C" stroke-width="2"/>
<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#1B2A4C" stroke-width="2"/>
<line x1="{sx(fit_x0):.1f}" y1="{sy(fit_y0):.1f}" x2="{sx(fit_x1):.1f}" y2="{sy(fit_y1):.1f}" stroke="#D5A62A" stroke-width="5"/>
{points}
<text x="{width/2}" y="{height-25}" text-anchor="middle" font-family="Arial, sans-serif" font-size="23" fill="#1B2A4C">log(1/ε)</text>
<text x="28" y="{top+plot_height/2}" text-anchor="middle" transform="rotate(-90 28 {top+plot_height/2})" font-family="Arial, sans-serif" font-size="23" fill="#1B2A4C">log N(ε)</text>
<text x="{sx((fit_x0+fit_x1)/2):.1f}" y="{sy(slope*((fit_x0+fit_x1)/2)+intercept)-28:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#1B2A4C">intermediate-scale fit: slope ≈ {slope:.2f}</text>
<text x="{sx(x[0]):.1f}" y="{sy(y[0])+42:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="#64789B">fine-scale pixel effects</text>
<text x="{sx(x[-1]):.1f}" y="{sy(y[-1])-34:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="#64789B">coarse-scale finite-size effects</text>
</svg>
"""
TARGET.write_text(svg)
print(TARGET)
