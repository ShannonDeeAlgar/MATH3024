#!/usr/bin/env python3
"""Apply the final Week 2 table, evidence, IFS, and roughness revisions."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week02/L_Fractals.ipynb"


def set_source(cell: dict, text: str) -> None:
    cell["source"] = [line for line in text.splitlines(keepends=True)]
    if text and not text.endswith("\n"):
        cell["source"][-1] += "\n"


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}

    set_source(
        cells["scale-symmetry"],
        r"""# Symmetry of a Euclidean object

<table class="standard-table">
  <colgroup><col style="width:50%"><col style="width:50%"></colgroup>
  <tbody>
    <tr><th>Reflect a circle through its centre</th><td>the image is unchanged</td></tr>
    <tr><th>Rotate a circle about its centre</th><td>the image is unchanged</td></tr>
    <tr><th>Magnify its boundary</th><td>a smooth edge becomes locally one-dimensional</td></tr>
    <tr><th>Magnify its interior</th><td>a filled region becomes locally two-dimensional</td></tr>
  </tbody>
</table>

Magnification is not a symmetry of the circle. At sufficiently high magnification, neither its edge nor its interior still looks like a circle.
""",
    )

    set_source(
        cells["fractal-visual-test"],
        r"""# Exact fractals and fractal-like forms

<div class="compact-card-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:.55rem;align-items:stretch">
  <div class="meaning-panel"><img src="images/Von_Koch_curve.gif" alt="Successive exact iterations of the Koch curve" style="width:100%;height:135px;object-fit:contain"><strong>Exact · Koch curve</strong><p>A precise rule continues without bound and its dimension can be calculated.</p></div>
  <div class="meaning-panel"><img src="images/Fractal_hands.jpg" alt="A finite recursive image of hands drawing hands" style="width:100%;height:135px;object-fit:contain"><strong>Finite recursion</strong><p>Like a fern, motifs recur for only finitely many levels. A scaling claim needs measurements across that finite range.</p></div>
  <div class="meaning-panel"><img src="images/wildfire_soot_fractal_aggregates.jpg" alt="Microscopy and scaling analysis of fractal-like wildfire soot aggregates" style="width:100%;height:135px;object-fit:contain"><strong>Statistical · soot aggregates</strong><p>Aggregate mass and radius obey an ensemble scaling law over a measured range; coating changes the estimated dimension.</p></div>
</div>

<div class="figure-caption">Soot aggregate panel adapted from China et al. (2013), “Morphology and mixing state of individual freshly emitted wildfire carbonaceous particles”, <em>Nature Communications</em> 4, 2122, <a href="https://doi.org/10.1038/ncomms3122">doi:10.1038/ncomms3122</a> (open access).</div>
""",
    )

    set_source(
        cells["fractal-properties-slide"],
        r"""# What evidence would count?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Before calling one of the previous objects fractal-like, what would we need to measure rather than recognise by eye?</span></div>

<ol class="evidence-steps">
  <li><strong>Name the feature.</strong> Boundary roughness, occupied mass, branching, or another measurable quantity.</li>
  <li><strong>Change resolution.</strong> Test whether its scaling is stable across several defensible scales.</li>
  <li><strong>State the limits.</strong> Report cut-offs, uncertainty, and sensitivity to representation.</li>
</ol>

<p><strong>A convincing claim links a visible pattern to a reproducible scaling measurement over a stated range.</strong></p>
""",
    )

    set_source(
        cells["cantor-ifs"],
        r"""## 2A. Cantor set · iterated function system

For the Cantor set, apply both contractions to the current set:

$$f_0(x)=\frac{x}{3},\qquad f_1(x)=\frac{x}{3}+\frac{2}{3}.$$

$$C_{k+1}=f_0(C_k)\cup f_1(C_k).$$

> **Union versus intersection.** The union combines the two retained copies when constructing the **next stage**. The stages are nested,
> $C_0\supset C_1\supset C_2\supset\cdots$, so the points that survive **every stage** form the limiting Cantor set:
> $C=\bigcap_{k=0}^{\infty}C_k$.

The union is therefore part of each update; the intersection defines the final limiting set.
""",
    )

    set_source(
        cells["sierpinski-ifs"],
        r"""## 2B. Sierpiński triangle · iterated function system

<div class="slide-columns" style="grid-template-columns:.9fr 1.1fr;align-items:center">
  <div>
    <p>Let <em>P</em><sub>1</sub>, <em>P</em><sub>2</sub>, and <em>P</em><sub>3</sub> be the vertices of the initial triangle.</p>
    <div class="display-equation">
      <math display="block" aria-label="f sub i of x equals one half x plus one half P sub i, for i equals 1, 2, 3">
        <msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>=</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mi>x</mi>
        <mo>+</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><msub><mi>P</mi><mi>i</mi></msub>
        <mo>,</mo><mspace width="1em"/><mi>i</mi><mo>=</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mn>3</mn><mo>.</mo>
      </math>
    </div>
    <p>Each map contracts towards one vertex. The three images together form the next approximation.</p>
  </div>
  <img src="images/Sierpinski_IFS.gif" alt="Repeated contraction maps generating the Sierpiński triangle" style="display:block;width:100%;max-height:330px;object-fit:contain">
</div>

The same distinction applies here: the union of three contracted copies constructs each new stage, while the infinite Sierpiński triangle is the intersection of the nested stages.
""",
    )

    set_source(
        cells["infinite-complexity"],
        r"""## Infinite complexity is a limiting claim

At every finite depth, the construction contains only finitely many pieces. The mathematical fractal is the limiting object obtained by allowing the iteration depth to increase without bound.

<table class="standard-table">
  <colgroup><col style="width:28%"><col style="width:72%"></colgroup>
  <tbody>
    <tr><th>Finite iteration</th><td>a computable approximation with a smallest represented feature</td></tr>
    <tr><th>Infinite limit</th><td>new structure exists at arbitrarily small scales</td></tr>
    <tr><th>Empirical system</th><td>scaling can hold only between physical lower and upper cut-offs</td></tr>
  </tbody>
</table>

This is why an image cannot by itself demonstrate infinite complexity.
""",
    )

    set_source(
        cells["ifs-convergence"],
        r"""## 2. Why does an IFS converge?

Each map is a contraction: it brings points closer together by a fixed factor smaller than one.

<table class="standard-table">
  <colgroup><col style="width:28%"><col style="width:72%"></colgroup>
  <tbody>
    <tr><th>Point dynamics</th><td>repeated contraction forgets the initial separation</td></tr>
    <tr><th>Set dynamics</th><td>the union of contracted copies approaches an invariant set</td></tr>
    <tr><th>Fixed set</th><td>the attractor <em>K</em> satisfies ℱ(<em>K</em>) = <em>K</em></td></tr>
  </tbody>
</table>

If the contractions are $f_1,\ldots,f_N$, define the set-map

$$\mathcal F(A)=\bigcup_{i=1}^{N}f_i(A).$$

Repeatedly applying $\mathcal F$ to a non-empty compact starting set approaches the unique compact attractor $K$. For the Cantor construction, that attractor is $C$, so $\mathcal F(C)=C$.
""",
    )

    set_source(
        cells["cantor-construction"],
        r"""# Cantor set

<img src="images/cantor_iterations_clean.svg" alt="The first four iterations of the middle-thirds Cantor construction" style="display:block;max-height:250px;width:auto;max-width:100%;margin:0 auto .8rem">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>What could “size” mean for this set? Compare count, total length, the length of one piece, and how much detail appears under magnification. Which answers the question you care about?</span></div>

<table class="standard-table fragment">
  <colgroup><col style="width:28%"><col style="width:72%"></colgroup>
  <tbody>
    <tr><th>Number</th><td><em>N</em><sub><em>k</em></sub> = 2<sup><em>k</em></sup> intervals</td></tr>
    <tr><th>Length of each</th><td>ℓ<sub><em>k</em></sub> = 3<sup>−<em>k</em></sup></td></tr>
    <tr><th>Total length</th><td><em>L</em><sub><em>k</em></sub> = <em>N</em><sub><em>k</em></sub>ℓ<sub><em>k</em></sub> = (2/3)<sup><em>k</em></sup> → 0</td></tr>
  </tbody>
</table>
""",
    )

    set_source(
        cells["sierpinski-construction"],
        r"""# Sierpiński triangle

<img src="images/Sierpinski_triangle_iterations.png" alt="The first iterations of the Sierpiński triangle construction" style="display:block;max-height:230px;width:auto;max-width:100%;margin:0 auto">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>At depth <em>k</em>, how many triangles remain? What fraction of area survives?</span></div>

Let $A_0$ be the area of the initial filled triangle and $A_k$ the total area of all triangles retained after $k$ removals. The ratio $A_k/A_0$ removes the arbitrary size of the starting triangle.

<table class="standard-table fragment">
  <colgroup><col style="width:28%"><col style="width:72%"></colgroup>
  <tbody>
    <tr><th>Number</th><td><em>N</em><sub><em>k</em></sub> = 3<sup><em>k</em></sup> triangles</td></tr>
    <tr><th>Side length</th><td>ℓ<sub><em>k</em></sub> = 2<sup>−<em>k</em></sup></td></tr>
    <tr><th>Retained area</th><td><em>A</em><sub><em>k</em></sub>/<em>A</em><sub>0</sub> = (3/4)<sup><em>k</em></sup> → 0</td></tr>
  </tbody>
</table>
""",
    )

    set_source(
        cells["box-counting-intuition"],
        r"""## Why can a count reveal dimension?

Halve the box width and ask how the occupied count multiplies:

<table class="standard-table">
  <colgroup><col style="width:28%"><col style="width:72%"></colgroup>
  <tbody>
    <tr><th>Smooth curve</th><td>about 2 times as many boxes: 2<sup>1</sup></td></tr>
    <tr><th>Filled region</th><td>about 4 times as many boxes: 2<sup>2</sup></td></tr>
    <tr><th>Fractal boundary</th><td>between 2 and 4 times: 2<sup><em>D</em></sup>, with 1 &lt; <em>D</em> &lt; 2</td></tr>
  </tbody>
</table>

Dimension is the exponent that makes the multiplication of visible detail predictable across scales. Taking logarithms turns that repeated multiplication into a slope.

For an ideal object the ratio may converge as $\varepsilon\to0$. For empirical data, we instead look for a stable slope across a justified finite scaling range.
""",
    )

    set_source(
        cells["dimension-information"],
        r"""## Dimension as information

To identify one location to a chosen precision, how many independent numbers must we provide?

<table class="standard-table">
  <colgroup><col style="width:28%"><col style="width:72%"></colgroup>
  <thead><tr><th>Space</th><th>Information needed</th></tr></thead>
  <tbody>
    <tr><td>Line</td><td>one coordinate: <em>x</em></td></tr>
    <tr><td>Plane</td><td>two coordinates: (<em>x</em>, <em>y</em>)</td></tr>
    <tr><td>Space</td><td>three coordinates: (<em>x</em>, <em>y</em>, <em>z</em>)</td></tr>
    <tr><td>ℝ<sup><em>n</em></sup></td><td><em>n</em> independent coordinates: (<em>x</em><sub>1</sub>, …, <em>x</em><sub><em>n</em></sub>)</td></tr>
  </tbody>
</table>
""",
    )

    set_source(
        cells["euclidean-scaling"],
        r"""## Dimension as a scaling count

<div class="slide-columns" style="grid-template-columns:1.35fr .65fr;align-items:center">
  <div>
    <img src="images/dimension_scaling.svg" alt="Lines, squares, and cubes divided at two resolutions" style="width:100%;max-height:390px;object-fit:contain">
    <p style="white-space:nowrap;font-size:.86em"><strong>Halve the length scale:</strong> a line needs 2 copies, a square 4, and a cube 8.</p>
  </div>
  <div class="scaling-variables">
    <p><strong><em>m</em></strong>: pieces along each direction</p>
    <p><strong><em>r</em></strong>: linear scale of one copy, equal to 1/<em>m</em></p>
    <p><strong><em>d</em></strong>: dimension</p>
    <p><strong><em>N</em></strong>: copies needed</p>
  </div>
</div>

For Euclidean objects, $N=m^d=r^{-d}$.
""",
    )

    # Raw HTML is not passed through the Reader's TeX renderer. Keep its
    # mathematical labels HTML-safe and reject unsupported inline delimiters.
    common_language = cells["common-language"]
    common_text = "".join(common_language["source"]).replace(
        r"near \(p_c\approx0.5927\)",
        "near <em>p</em><sub>c</sub> ≈ 0.5927",
    )
    set_source(common_language, common_text.rstrip("\n"))

    remaining_inline = [
        cell.get("id")
        for cell in notebook["cells"]
        if r"\(" in "".join(cell.get("source", []))
        or r"\)" in "".join(cell.get("source", []))
    ]
    if remaining_inline:
        raise RuntimeError(
            "Unsupported backslash-style inline math remains in: "
            + ", ".join(str(cell_id) for cell_id in remaining_inline)
        )

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
