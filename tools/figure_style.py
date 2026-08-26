"""Shared Matplotlib styling for course-generated MATH3024 figures.

Static figures are exported once as SVG and reused by the Reader and slides.
The typography is therefore chosen to remain legible on a 1280 x 720 slide,
not tuned separately for each destination.
"""

from __future__ import annotations

import matplotlib as mpl


INK = "#1B2A4C"
SECONDARY = "#5A6685"
RULE = "#C7CEDC"
GRID = "#D7DFED"
BLUE = "#2C7FB8"
LIGHT_BLUE = "#8CB9D8"
ORANGE = "#D95F3B"
YELLOW = "#F4C542"
GREY = "#AAB5C8"


def apply_course_figure_style() -> None:
    """Apply the unit-wide figure typography and restrained visual grammar."""
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.stretch": "normal",
            "mathtext.fontset": "dejavusans",
            "font.size": 15,
            "axes.titlesize": 18,
            "axes.titleweight": "normal",
            "axes.labelsize": 16,
            "axes.labelcolor": INK,
            "axes.edgecolor": INK,
            "axes.linewidth": 1.1,
            "xtick.labelsize": 13,
            "ytick.labelsize": 13,
            "xtick.color": INK,
            "ytick.color": INK,
            "legend.fontsize": 12.5,
            "legend.labelspacing": 0.45,
            "text.color": INK,
            # Preserve the chosen typeface inside exported SVGs. Mathematical
            # labels use the matching DejaVu Sans math set above, so ordinary
            # text and symbols do not appear to come from different families.
            "svg.fonttype": "path",
            "savefig.facecolor": "white",
            "savefig.bbox": "tight",
        }
    )


def finish_axes(ax, *, grid: bool = True) -> None:
    """Apply the standard finishing treatment to one Cartesian axis."""
    ax.spines[["top", "right"]].set_visible(False)
    if grid:
        ax.grid(color=GRID, linewidth=0.8, alpha=0.9)
        ax.set_axisbelow(True)
