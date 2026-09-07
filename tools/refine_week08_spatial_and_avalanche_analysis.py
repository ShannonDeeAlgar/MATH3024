"""Refine the Week 8 Reader's spatial and avalanche analysis."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks" / "week08" / "L_Critical_phenomena.ipynb"


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = notebook["cells"]

    by_id = {cell.get("id"): cell for cell in cells}

    # The randomly driven snapshot previously appeared before the deliberately
    # symmetric example. Keep the spatial question together under the latter.
    old_subset = by_id["a1e274ff-bbbe-4952-a618-d75c7fa5a6d5"]
    cells.remove(old_subset)

    symmetric = by_id["week08-sandpile-fractal-stills"]
    symmetric["source"] = """
### A deliberately symmetric pile

Random driving is useful for avalanche statistics, but it can hide the geometry. If many grains are placed at one central site and the pile is allowed to relax, the stable configurations expose nested spatial structure much more clearly.

<img src="images/sandpile_fractal_stills.png" width="86%" alt="Three stable Abelian sandpiles formed by adding increasing numbers of grains at one central site">

These are deliberately symmetric demonstrations, not typical snapshots from the randomly driven stationary process. They make the spatial organisation visible. Box counting then tests how each height class occupies the image across the available scales.

<img src="images/sandpile_height_subsets.png" width="72%" alt="Four height classes from one symmetric sandpile, labelled with finite-scale box-counting estimates">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Should the four height classes have the same box-counting dimension? What should happen to the dimensions of a set and its complement?</span></div>

<details class="reader-answer">
<summary>My answer</summary>
<div>

The four measured slopes are similar in scale but not equal. In this finite image they are approximately 1.50, 1.41, 1.81 and 1.92 for heights 0, 1, 2 and 3. The result depends on the lattice, the number of grains and the fitted box sizes, so these are finite-scale descriptors rather than exact dimensions of four limiting fractals.

Dimensions do not add like area fractions. A set and its complement can both have box-counting dimension 2. More generally, the dimension of a finite union is governed by the largest component dimension, not the sum. A height class that occupies a non-zero fraction of sites throughout a growing two-dimensional region is expected to have dimension 2 in the large-system limit, even when its arrangement looks intricate. Non-integer scaling may instead be clearer in an interface, an avalanche frontier or another sparse subset.

There is also a digital-image caveat: a fixed finite collection of pixels has mathematical box-counting dimension 0 if resolution is taken arbitrarily fine. The slopes shown here describe the limited scales available in the simulated image.

</div>
</details>
""".strip()

    box_intro = by_id["78b85e52-c9a2-4839-bb22-ecfece4d5065"]
    box_intro["source"] = (
        "Visual resemblance is not enough. We need to test how the number of occupied boxes "
        "changes with box width and state which scales are used for the fit."
    )

    box_plot = by_id["d9689493-fe6d-4c11-98e4-7cb1ecfc711e"]
    box_plot["source"] = """
To estimate the **box-counting dimension**, cover each height class with boxes at several scales and count the occupied boxes. A nearly linear region on log–log axes provides the finite range used for the estimate.

<img src="images/sandpile_box_counting.png" width="66%" alt="Box-counting diagnostics for four height classes, with fitted scale range and estimated slopes">

The single shaded band marks the common fitted range. The same four box widths are used for every height class, making the slopes directly comparable. If diagnostics supported different linear regions, each estimate would need its own stated fit range. The useful common range is the largest defensible intersection, since an arbitrarily narrow range leaves too little information for a reliable slope.
""".strip()

    bound = by_id["f56573c1-f10f-4fe7-8ba6-2a74e719c1d2"]
    bound["source"] = """
<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Check the estimate"><span>A box-counting estimate for a subset of a two-dimensional image is greater than 2. What does that tell us about the calculation?</span></div>

<details class="reader-answer">
<summary>My answer</summary>
<div>

Any subset of the plane has box-counting dimension between 0 and 2. An estimate above 2 is therefore a diagnostic: the fitted scale range is unsuitable, the counting implementation is wrong, or the stated quantity is not the one actually being measured. It is not evidence of an unusually complicated planar set.

</div>
</details>
""".strip()

    random_answer = by_id["1a47a88f-f5de-4265-9494-aac0ca739021"]
    random_answer["source"] = """
<details class="reader-answer">
<summary>My answer</summary>
<div>

An independently occupied set with a non-zero limiting area fraction fills the plane statistically, so its box-counting dimension is 2. A value below 2 requires a subset that becomes sparse as resolution increases, such as a curve, a critical cluster boundary or another zero-area set. Visual roughness alone does not imply a non-integer dimension.

</div>
</details>
""".strip()

    avalanche_heading = by_id["3cdcf36d-eddc-4976-973b-e53a589762af"]
    avalanche_heading["source"] = r"""
### Avalanche size and duration

One grain addition is one trial. If it triggers toppling, define:

- **avalanche size** \(S\): the total number of topplings, including repeated topplings of the same site;
- **avalanche duration** \(T\): the number of parallel relaxation steps before the lattice is stable again.

These definitions depend on the update convention. A queue that processes unstable sites one at a time has a useful computational order, but its queue length is not the physical duration used here.

Before fitting a power law, inspect the full distributions. The smallest events depend on the event definition and measurement resolution; the largest are limited by the finite lattice. A straight-looking middle region may span only a restricted range. A heavy tail is not, by itself, proof of an asymptotic power law.
""".strip()

    choice = by_id["15a11b61-9ef2-4b11-be9b-3024de480314"]
    choice["source"] = (
        '<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice">'
        '<span>Record both <i>S</i> and <i>T</i>. Also record additions that cause no toppling, '
        'even though the conditional plots below show only non-zero avalanches.</span></div>'
    )

    scaling = by_id["4ef815da-7df1-4d08-a36c-f5593e8edd2c"]
    scaling["source"] = r"""
Candidate scaling laws are

\[
p(S)\propto S^{-\tau_S},
\qquad
p(T)\propto T^{-\tau_T}.
\]

The exponents \(\tau_S\) and \(\tau_T\) need not match because size and duration measure different aspects of an event.
""".strip()

    distributions = by_id["6ef6999f-aeb2-47d9-a94d-4f405a74be02"]
    distributions["source"] = """
<img src="images/sandpile_avalanche_distributions.png" width="88%" alt="Ordinary histograms and log-binned probability densities for avalanche size and duration">

Each row uses the same non-zero avalanche sample twice. The ordinary histogram reports the **number of avalanches per equal-width bin**. The log–log panel uses logarithmically spaced bins and divides each bin count by both the number of avalanches and the bin width. Its vertical axis is therefore an estimated **probability density**: the area represented by a bin, rather than its height alone, gives the estimated probability.

The grey bands mark illustrative scaling ranges and the lines report fitted slopes. They are diagnostics, not declarations of universal exponents. A defensible scaling claim requires repeating the calculation for larger lattices and checking whether the cutoff moves while the shared fitted region remains reasonably stable.
""".strip()

    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
