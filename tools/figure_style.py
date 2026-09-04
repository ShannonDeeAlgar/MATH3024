"""Shared Matplotlib styling for course-generated MATH3024 figures.

Static figures are exported once as SVG and reused by the Reader and slides.
The typography is therefore chosen to remain legible on a 1280 x 720 slide,
not tuned separately for each destination.
"""

from __future__ import annotations

import matplotlib as mpl
from collections.abc import Iterable


INK = "#1B2A4C"
SECONDARY = "#5A6685"
RULE = "#C7CEDC"
GRID = "#D7DFED"
BLUE = "#2C7FB8"
LIGHT_BLUE = "#8CB9D8"
ORANGE = "#D95F3B"
YELLOW = "#F4C542"
GREY = "#AAB5C8"


COURSE_RCPARAMS = {
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
    "svg.fonttype": "path",
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
}


def apply_course_figure_style() -> None:
    """Apply the unit-wide figure typography and restrained visual grammar."""
    mpl.rcParams.update(COURSE_RCPARAMS)


def style_figure(fig) -> None:
    """Reapply course typography to an existing static or animated figure.

    Animation callbacks often replace titles, labels, legends or annotations
    after a figure is created.  Calling this at the end of each frame prevents
    those new artists from falling back to a different font or size.
    """
    apply_course_figure_style()
    for text in fig.findobj(match=mpl.text.Text):
        text.set_fontfamily("DejaVu Sans")
        text.set_fontstretch("normal")
    for ax in fig.axes:
        ax.title.set_fontsize(COURSE_RCPARAMS["axes.titlesize"])
        ax.xaxis.label.set_fontsize(COURSE_RCPARAMS["axes.labelsize"])
        ax.yaxis.label.set_fontsize(COURSE_RCPARAMS["axes.labelsize"])
        for tick in (*ax.get_xticklabels(), *ax.get_yticklabels()):
            tick.set_fontsize(COURSE_RCPARAMS["xtick.labelsize"])
        legend = ax.get_legend()
        if legend is not None:
            for text in legend.get_texts():
                text.set_fontsize(COURSE_RCPARAMS["legend.fontsize"])


def style_animation_frame(fig, axes: Iterable | None = None) -> None:
    """Finish an animation frame with the same rules as a static figure."""
    style_figure(fig)
    for ax in axes if axes is not None else fig.axes:
        # Polar and other specialist axes do not expose the rectangular
        # top/right spines used by ``finish_axes``.
        if ax.name == "rectilinear":
            finish_axes(ax)


def finish_axes(ax, *, grid: bool = True) -> None:
    """Apply the standard finishing treatment to one Cartesian axis."""
    ax.spines[["top", "right"]].set_visible(False)
    if grid:
        ax.grid(color=GRID, linewidth=0.8, alpha=0.9)
        ax.set_axisbelow(True)
