#!/usr/bin/env python3
"""Preserve the current approved Week 2 content after any larger rebuild."""

from __future__ import annotations


def _source(text: str) -> list[str]:
    if text and not text.endswith("\n"):
        text += "\n"
    return text.splitlines(keepends=True)


def _set_source(cell, text: str) -> None:
    cell["source"] = _source(text)


def _markdown(cell_id: str, text: str, *, tag: str, slide_type: str):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {
            "tags": [tag],
            "slideshow": {"slide_type": slide_type},
        },
        "source": _source(text),
    }


def apply_current_week02(notebook) -> None:
    """Apply the latest approved additions, removals, and teaching order."""
    cells = list(notebook["cells"])
    by_id = {cell.get("id"): cell for cell in cells}

    _set_source(
        by_id.setdefault(
            "cezanne-mandelbrot-contrast",
            _markdown(
                "cezanne-mandelbrot-contrast", "", tag="slides", slide_type="slide"
            ),
        ),
        """# From ideal forms to natural complexity

<div class="reader-voice">
  <div class="reader-voice-quote">Everything in nature is modelled according to the sphere, the cone, and the cylinder. You have to learn to paint with reference to these simple shapes; then you can do anything.</div>
  <div class="reader-voice-attr">Paul Cézanne, letter to Émile Bernard (1904), in Michael Doran (ed.), <em>Conversations with Cézanne</em>, University of California Press (2001), p. 63</div>
</div>

## But …

<div class="reader-voice">
  <div class="reader-voice-quote">Clouds are not spheres, mountains are not cones, coastlines are not circles, and bark is not smooth, nor does lightning travel in a straight line.</div>
  <div class="reader-voice-attr">Benoit Mandelbrot, <em>The Fractal Geometry of Nature</em></div>
</div>

Euclidean forms remain useful reference models. Fractal geometry gives us a language for natural structure that stays irregular as scale changes.
""",
    )

    _set_source(
        by_id.setdefault(
            "fractal-properties-core",
            _markdown("fractal-properties-core", "", tag="slides", slide_type="slide"),
        ),
        """# Fractal properties

There is no single, universal definition of a fractal. Instead, fractals are typically recognised by a combination of distinctive properties:

1. **Self-similarity:** parts of the shape resemble the whole. They are made from smaller copies or related versions of itself, often through recursion or iteration.
2. **Infinite complexity:** in a mathematical fractal, detail persists at arbitrarily small scales.
3. **Fractal dimension:** a typically non-integer dimension reflects how the shape scales or fills space.

For natural and empirical forms, self-similarity and complexity hold only approximately over a finite, stated range of scales.
""",
    )

    _set_source(
        by_id["cantor-ifs"],
        r"""## 2A. Cantor set · iterated function system

For the Cantor set, apply both contractions to the current set:

$$f_0(x)=\frac{x}{3},\qquad f_1(x)=\frac{x}{3}+\frac{2}{3}.$$

$$C_{k+1}=f_0(C_k)\cup f_1(C_k).$$
""",
    )

    union_note = by_id.setdefault(
        "cantor-limit-reader",
        _markdown("cantor-limit-reader", "", tag="reader-only", slide_type="skip"),
    )
    union_note["metadata"] = {
        "tags": ["reader-only"],
        "slideshow": {"slide_type": "skip"},
    }
    _set_source(
        union_note,
        r"""### Union versus intersection

The union combines the two retained copies when constructing the **next stage**. The stages are nested,

$$C_0\supset C_1\supset C_2\supset\cdots,$$

so the points that survive **every stage** form the limiting Cantor set:

$$C=\bigcap_{k=0}^{\infty}C_k.$$

The union is therefore part of each update; the intersection defines the final limiting set.
""",
    )

    convergence = by_id["ifs-convergence"]
    convergence["metadata"] = {
        "tags": ["reader-only"],
        "slideshow": {"slide_type": "skip"},
    }

    _set_source(
        by_id["sierpinski-construction"],
        r"""# Sierpiński triangle

<img src="images/Sierpinski_triangle_iterations.png" alt="The first iterations of the Sierpiński triangle construction" style="display:block;max-height:220px;width:auto;max-width:100%;margin:0 auto">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>At depth <em>k</em>, how many triangles remain? What happens to their total area and total perimeter?</span></div>

Let $A_0$ and $P_0$ be the area and perimeter of the initial filled triangle. At depth $k$, there are $3^k$ triangles, each with side length $2^{-k}$ times the original.

<table class="standard-table fragment">
  <colgroup><col style="width:30%"><col style="width:70%"></colgroup>
  <tbody>
    <tr><th>Number</th><td><em>N</em><sub><em>k</em></sub> = 3<sup><em>k</em></sup> triangles</td></tr>
    <tr><th>Side length</th><td>ℓ<sub><em>k</em></sub> = 2<sup>−<em>k</em></sup></td></tr>
    <tr><th>Retained area</th><td><em>A</em><sub><em>k</em></sub>/<em>A</em><sub>0</sub> = (3/4)<sup><em>k</em></sup> → 0</td></tr>
    <tr><th>Total perimeter</th><td><em>P</em><sub><em>k</em></sub>/<em>P</em><sub>0</sub> = 3<sup><em>k</em></sup>2<sup>−<em>k</em></sup> = (3/2)<sup><em>k</em></sup> → ∞</td></tr>
  </tbody>
</table>
""",
    )

    sierpinski_limit_note = by_id.setdefault(
        "sierpinski-limit-reader",
        _markdown(
            "sierpinski-limit-reader", "", tag="reader-only", slide_type="skip"
        ),
    )
    sierpinski_limit_note["metadata"] = {
        "tags": ["reader-only"],
        "slideshow": {"slide_type": "skip"},
    }
    _set_source(
        sierpinski_limit_note,
        r"""### Union versus intersection for the Sierpiński triangle

The same distinction used for the Cantor set applies here. The union of three contracted copies constructs the **next stage**:

$$S_{k+1}=f_1(S_k)\cup f_2(S_k)\cup f_3(S_k).$$

The stages are nested, so the points that survive **every stage** form the limiting Sierpiński triangle:

$$S=\bigcap_{k=0}^{\infty}S_k.$$

The union is part of the update rule; the intersection defines the limiting set.
""",
    )

    sierpinski_ifs_text = "".join(by_id["sierpinski-ifs"]["source"])
    sierpinski_ifs_text = sierpinski_ifs_text.replace(
        "\nThe same distinction applies here: the union of three contracted copies constructs each new stage, while the infinite Sierpiński triangle is the intersection of the nested stages.\n",
        "\n",
    )
    _set_source(by_id["sierpinski-ifs"], sierpinski_ifs_text)

    _set_source(
        by_id["cantor-l-system"],
        """## 3A. Cantor set · L-system

This rule produces the **standard middle-thirds Cantor set**. Other Cantor-like sets use different contraction ratios or removal rules.

<div class="slide-columns lsystem-layout">
  <div class="lsystem-specification">
    <p><strong>Alphabet:</strong> <em>V</em> = {<em>A</em>, <em>B</em>}</p>
    <p><strong>Meaning:</strong> <em>A</em> draws; <em>B</em> moves without drawing</p>
    <p><strong>Initial word:</strong> ω = <em>A</em></p>
    <p><strong>Productions:</strong> <em>A</em> → <em>ABA</em>, <em>B</em> → <em>BBB</em></p>
  </div>
  <div>
    <img src="images/cantor_iterations_clean.svg" alt="Successive Cantor set iterations labelled by depth" style="display:block;width:100%;max-height:285px;object-fit:contain">
    <p>Each finite word describes one stage of the construction.</p>
  </div>
</div>
""",
    )

    _set_source(
        by_id["l-systems"],
        """## 3B. Sierpiński triangle · L-system

<div class="slide-columns lsystem-layout">
  <div class="lsystem-specification">
    <p><strong>Alphabet:</strong> <em>V</em> = {<em>F</em>, <em>G</em>, +, −}</p>
    <p><strong>Meaning:</strong> <em>F</em> and <em>G</em> draw; + turns left by 60°; − turns right by 60°</p>
    <p><strong>Initial word:</strong> ω = <em>F</em></p>
    <p><strong>Productions:</strong> <em>F</em> → <em>G−F−G</em>, <em>G</em> → <em>F+G+F</em></p>
  </div>
  <img src="images/sierpinski_lsystem_iterations.svg" alt="Successive iterations through depth six of the Sierpiński arrowhead L-system" style="display:block;width:100%;max-height:310px;object-fit:contain">
</div>
""",
    )

    _set_source(
        by_id.setdefault(
            "generation-methods-summary",
            _markdown(
                "generation-methods-summary", "", tag="slides", slide_type="slide"
            ),
        ),
        """# Three descriptions, three emphases

<table class="standard-table">
  <colgroup><col style="width:21%"><col style="width:37%"><col style="width:42%"></colgroup>
  <thead><tr><th>Description</th><th>Most useful when</th><th>Real-world connection</th></tr></thead>
  <tbody>
    <tr><td><strong>Replacement</strong></td><td>each piece is replaced by a repeated motif</td><td>an idealised rough boundary that develops structure hierarchically</td></tr>
    <tr><td><strong>IFS</strong></td><td>the whole is composed of transformed smaller copies</td><td>a Barnsley fern describes fern-like geometry efficiently</td></tr>
    <tr><td><strong>L-system</strong></td><td>local instructions generate successive stages</td><td>branching plant growth from active tips</td></tr>
  </tbody>
</table>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="" width="34" height="34"><span>The representation should match the question. Are we exposing a repeated construction, describing self-similar geometry, or proposing a growth mechanism?</span></div>
""",
    )

    generation_summary_reader = by_id.setdefault(
        "generation-methods-summary-reader",
        _markdown(
            "generation-methods-summary-reader",
            "",
            tag="reader-only",
            slide_type="skip",
        ),
    )
    generation_summary_reader["metadata"] = {
        "tags": ["reader-only"],
        "slideshow": {"slide_type": "skip"},
    }
    _set_source(
        generation_summary_reader,
        """## What does each description emphasise?

The three descriptions encode different kinds of repetition. They are not equally literal models of a physical process.

### 1. Initiator and generator

Use replacement when each existing piece is replaced by the same smaller motif. It is useful for controlled models of hierarchical subdivision or increasingly rough boundaries. A Koch-like construction can represent a boundary that repeatedly develops smaller protrusions, but a real coastline does not literally apply one identical generator at every scale.

### 2. Iterated function system

Use an IFS when the whole can be described as a union of smaller transformed copies. The Barnsley fern is a good example: a small collection of affine maps reproduces the stem, leaflets, and tip. This is an efficient description of fern-like geometry, not a model of the biological processes that grow a fern.

### 3. L-system

Use an L-system when components develop through repeated local instructions. It is especially well aligned with branching and growth from active tips. A plant model can rewrite each stem or branch symbol and then interpret the resulting word geometrically. Real plants also respond to hormones, resources, mechanics, and their environment, so even this remains a simplification.

The same mathematical fractal may admit all three descriptions. The best choice depends on whether we want to expose a repeated construction, describe self-similar geometry, or propose a plausible growth mechanism.
""",
    )

    _set_source(
        by_id["euclidean-expectations"],
        """## What Euclidean geometry keeps, and what it misses

**Scale** is the size or resolution at which we observe, measure, or describe a system.

<div class="slide-columns evidence-layout" style="grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="meaning-panel" style="text-align:left;min-width:0;display:flex;flex-direction:column">
    <div style="height:205px;display:flex;align-items:center;justify-content:center">
      <div style="width:140px;height:140px;border:5px solid #1B2A4C;border-radius:50%"></div>
    </div>
    <strong>Circle</strong>
    <p style="margin:0">Its radius is a <strong>characteristic scale</strong>. Magnification reveals a smooth arc, then a locally straight boundary.</p>
  </div>
  <div class="meaning-panel" style="text-align:left;min-width:0;display:flex;flex-direction:column">
    <div style="height:205px;display:flex;align-items:center;justify-content:center;overflow:hidden">
      <img src="images/mandelbrot_scale_symmetry.png" alt="The Mandelbrot set and a miniature copy after deep magnification" style="display:block;width:100%;height:100%;object-fit:contain;margin:0">
    </div>
    <strong>Mandelbrot set</strong>
    <p style="margin:0">No single length organises its boundary. Changing resolution continues to reveal structured detail.</p>
  </div>
</div>

Shape, position, size, and rigid motions still describe both objects. They do not describe how boundary detail changes with resolution.
""",
    )

    linear_scale_note = by_id.setdefault(
        "linear-scale-factor-reader",
        _markdown(
            "linear-scale-factor-reader", "", tag="reader-only", slide_type="skip"
        ),
    )
    linear_scale_note["metadata"] = {
        "tags": ["reader-only"],
        "slideshow": {"slide_type": "skip"},
    }
    _set_source(
        linear_scale_note,
        r""":::{note} Linear scale factor
The linear scale factor $r$ tells us what happens to **every distance** when we make a geometrically similar copy.

For $r=\tfrac12$:

- a line segment of length $1$ becomes one of length $\tfrac12$;
- a square with side length $1$ becomes a square with side length $\tfrac12$;
- a cube with side length $1$ becomes a cube with side length $\tfrac12$.

We scale every direction equally because otherwise the result is not a smaller, geometrically similar copy. Halving only the width of a square produces a rectangle, not a smaller square.

Why choose a **linear** scale? Similarity is defined by what happens to distances. Area and volume then follow automatically:

$$A\mapsto r^2A,\qquad V\mapsto r^3V.$$
:::
""",
    )

    target_dimension_prompt = by_id.setdefault(
        "invent-a-fractal-reader",
        _markdown(
            "invent-a-fractal-reader", "", tag="reader-only", slide_type="skip"
        ),
    )
    target_dimension_prompt["metadata"] = {
        "tags": ["reader-only"],
        "slideshow": {"slide_type": "skip"},
    }
    _set_source(
        target_dimension_prompt,
        r"""### Can we design a fractal with a chosen dimension?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Suppose you want an exact self-similar fractal with dimension <em>D</em> = 1.7. Can you work backwards from <em>N</em> = <em>r</em><sup>−<em>D</em></sup> to choose <em>N</em> and <em>r</em>? What might prevent the resulting copies from forming the fractal you intended?</span></div>

```{dropdown} my answer...
For equal self-similar copies,

$$Nr^D=1,\qquad r=N^{-1/D}.$$

Choose an integer copy number, for example $N=3$. For $D=1.7$,

$$r=3^{-1/1.7}\approx0.524.$$

The integer requirement on $N$ does not restrict us to a disconnected list of dimensions because $r$ can vary continuously. The geometry still imposes constraints:

- the scaled copies must fit in the surrounding space;
- for a separated construction in the plane, the dimension cannot exceed $2$;
- overlap can make the realised dimension smaller than the similarity dimension;
- requirements such as connectedness, symmetry, or alignment to a grid restrict the possible arrangements further.

So the equation supplies candidate scaling parameters. We still have to design contraction maps whose geometry realises them.
```
""",
    )

    _set_source(
        by_id["empirical-transition"],
        """# Exact dimension is not always available

<div class="slide-columns" style="grid-template-columns:.72fr 1.28fr;align-items:center">
  <div>
    <p><strong>This was the problem Mandelbrot was tackling.</strong></p>
    <p>A coastline has no known exact generator, only a finite statistical scaling range.</p>
    <p>A straight ruler resolves some bends and skips others, so ruler length is part of the measurement.</p>
    <p><strong>The smaller ruler reveals additional structure faster than the ruler length decreases.</strong></p>
    <p>We therefore need an empirical procedure that tracks visible structure across resolutions.</p>
  </div>
  <img class="column-image" src="images/Great-britain-coastline-paradox.gif" alt="Successively finer measurements of the British coastline" style="max-height:390px;object-fit:contain">
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>As the ruler shrinks, what happens to the measured length? Must it converge?</span></div>

This returns us to Mandelbrot's motivating problem: **How long is the coast of Britain?**

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down:</strong> inspect what one ruler sees. <strong>Up:</strong> measure the scaling relationship across ruler lengths.</span></div>
""",
    )

    _set_source(
        by_id["coastline-reader"],
        r"""## The coastline paradox

Let $L(\varepsilon)$ be the measured length using rulers of length $\varepsilon$.

For a smooth curve, $L(\varepsilon)$ approaches a finite value as $\varepsilon$ becomes small. For a fractal-like boundary,

$$L(\varepsilon)\propto \varepsilon^{1-D},$$

so a dimension $D>1$ makes the measured length grow as the ruler shrinks. **The smaller ruler reveals additional structure faster than the ruler length decreases.**

The coastline is finite at every chosen resolution. The paradox is that there is no resolution-independent answer supplied by the geometry alone. If the idealised scaling law continued to arbitrarily small rulers, the measured length would diverge. A physical coastline has a lower cut-off at which that model ceases to apply.

Mandelbrot's classic treatment is B. Mandelbrot (1967), [“How Long Is the Coast of Britain? Statistical Self-Similarity and Fractional Dimension”](https://doi.org/10.1126/science.156.3775.636), *Science* 156, 636–638.
""",
    )

    reader_sections = {
        "scale-free-bridge-reader": r"""# From dimension to scale-free behaviour

<div class="slide-columns evidence-layout" style="grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="meaning-panel" style="text-align:left">
    <h3>Measured object</h3>
    <p style="text-align:center;font-size:1.1em"><em>N</em>(ε) ∝ ε<sup>−<em>D</em></sup></p>
    <p>ε is the box width and <em>N</em>(ε) the occupied-box count. The fitted exponent records how the count changes with resolution.</p>
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>Exact self-similarity</h3>
    <p style="text-align:center;font-size:1.1em"><em>N</em> = <em>L</em><sup><em>D</em></sup>, &nbsp; <em>D</em> = log <em>N</em> / log <em>L</em></p>
    <p>Reducing each length to 1/<em>L</em> reveals <em>N</em> copies. The exponent is exact.</p>
  </div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="" width="34" height="34"><span><strong>Fractal dimension is a dimensionless ratio of complexity across scales.</strong> It measures how rapidly visible structure multiplies under magnification, not the object's physical size.</span></div>
""",
        "characteristic-scale-reader": r"""## Characteristic scales

A **characteristic scale** is a length, time, mass, or other magnitude that organises the behaviour of a system. Measurements are naturally compared with it.

<table class="standard-table">
  <colgroup><col style="width:38%"><col style="width:62%"></colgroup>
  <thead><tr><th>Example</th><th>Characteristic scale</th></tr></thead>
  <tbody>
    <tr><td>Circle</td><td>its radius</td></tr>
    <tr><td>Gaussian distribution</td><td>its standard deviation</td></tr>
    <tr><td>Exponential decay</td><td>its decay time</td></tr>
    <tr><td>Simple pendulum</td><td>its period</td></tr>
  </tbody>
</table>

For a circle, magnification eventually reveals either a locally straight boundary or a filled region. Its radius supplies a natural reference length. For an empirical fractal-like object, there may be no single length that organises the structure throughout the observed scaling range.
""",
        "scale-free-definition-reader": r"""## A scaling law is not always self-similarity

<img src="images/circle_vs_scale_free.svg" alt="A family of circles contrasted with an exact self-similar Sierpiński construction" style="display:block;width:94%;max-height:330px;object-fit:contain;margin:.05rem auto .25rem">

<div class="slide-columns evidence-layout" style="grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="meaning-panel" style="text-align:left">
    <strong>Circle</strong>
    <p>Doubling the radius multiplies area by \(2^2=4\). This is a scaling law for a family of circles. A particular circle still contains the characteristic length \(R\).</p>
  </div>
  <div class="meaning-panel" style="text-align:left">
    <strong>Exact fractal</strong>
    <p>Reducing each length to \(1/L\) reveals \(N=L^D\) copies inside the same set. The structure repeats; \(D\) is a dimensionless ratio of complexity across scales, not a physical size.</p>
  </div>
</div>
""",
        "scale-free-circle-reader": r"""## When do we call a relationship scale-free?

<div class="slide-columns evidence-layout" style="grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="meaning-panel" style="text-align:left;font-size:.94em">
    <h3>A particular object</h3>
    <p style="text-align:center;font-size:1.15em"><em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = <em>R</em><sup>2</sup></p>
    <p>The fixed radius <em>R</em> is a preferred length. Magnifying the boundary eventually reveals a smooth one-dimensional arc rather than another complete circle.</p>
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>A relationship across scales</h3>
    <p style="text-align:center;font-size:1.08em"><em>f</em>(<em>ax</em>) = <em>a</em><sup>α</sup><em>f</em>(<em>x</em>)</p>
    <p>A relationship is scale-free when the same rescaling rule holds without introducing a preferred value of <em>x</em>. The factor <em>a</em> is chosen by us. The exponent α remains fixed.</p>
  </div>
</div>

The area relation \(A(R)=\pi R^2\) is homogeneous in \(R\), but this does not make the geometry of one fixed circle self-similar under magnification. Always state **what object or relationship is being rescaled**.
""",
        "return-to-branching-scale-free": r"""## Example 1: Branching trees

<div class="slide-columns evidence-layout" style="grid-template-columns:1.15fr .85fr;align-items:stretch">
  <div class="meaning-panel" style="padding:.35rem">
    <iframe
      src="https://www.complexity-explorables.org/explorables/weeds-and-trees/"
      title="Weeds and Trees branching growth explorable"
      style="width:100%;height:390px;border:0;border-radius:4px"
      loading="lazy"
      allowfullscreen>
    </iframe>
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>What could scale here?</h3>
    <p>Within one tree, compare branch number, length and diameter across branching ranks.</p>
    <p>Across trees, compare height, crown width, foliage or biomass with trunk diameter.</p>
    <p>A repeated branching rule gives us a form. A scaling analysis asks which ratios remain reasonably stable as size or rank changes.</p>
  </div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Change one branching control. Which measurement would reveal its effect across scales?</span></div>
""",
        "tree-allometry-across-trees": r"""## Across forests and trees

<div class="slide-columns evidence-layout" style="grid-template-columns:1.28fr .72fr;align-items:start">
  <div class="meaning-panel" style="padding:.35rem;align-self:start">
    <img src="images/eloy_2017_fig3.jpg" alt="Allometric scaling relationships from the MECHATREE model" style="display:block;width:100%;max-height:430px;object-fit:contain;margin:0 auto">
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>Across forests and trees</h3>
    <p><strong>Figure 3a:</strong> competition for light produces a relationship between stand density and average biomass.</p>
    <p><strong>Figure 3b:</strong> height, crown radius, foliage number and biomass scale with trunk diameter across many simulated trees.</p>
    <p>The trends are approximately allometric, but the height relationship bends for larger trees. Finite size still matters.</p>
  </div>
</div>

<div class="figure-caption">Eloy et al. (2017), <a href="https://doi.org/10.1038/s41467-017-00995-6">“Wind loads and competition for light sculpt trees into self-similar structures”</a>, Fig. 3. CC BY 4.0.</div>
""",
        "tree-allometry-within-tree": r"""## Within one tree

<div class="slide-columns evidence-layout" style="grid-template-columns:1.25fr .75fr;align-items:start">
  <div class="meaning-panel" style="padding:.35rem;align-self:start">
    <img src="images/eloy_2017_fig5.jpg" alt="Branch order and self-similar ratios within one simulated tree" style="display:block;width:100%;max-height:430px;object-fit:contain;margin:0 auto">
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>Across branching ranks</h3>
    <p>Strahler order groups branches by their position in the hierarchy.</p>
    <p>Branch number, mean length, area and diameter follow approximate geometric progressions across ranks.</p>
    <p>The corresponding fractal dimension changes while the tree is young, then becomes more stable as the architecture develops.</p>
  </div>
</div>

<div class="figure-caption">Eloy et al. (2017), <a href="https://doi.org/10.1038/s41467-017-00995-6">Fig. 5</a>. The model includes competition for light, wind loading, growth and pruning. CC BY 4.0.</div>
""",
        "allometry-beyond-fractals": r"""## Across species

<div class="slide-columns evidence-layout" style="grid-template-columns:1.2fr .8fr;align-items:start">
  <div class="meaning-panel" style="padding:.35rem;align-self:start">
    <img src="images/labonte_2024_fig1.png" alt="Maximum running speed across animals of different body masses" style="display:block;width:100%;max-height:430px;object-fit:contain;margin:0 auto">
  </div>
  <div class="meaning-panel" style="text-align:left">
    <p>An <strong>allometric relationship</strong> compares one biological measurement with another, often using body mass as the reference:</p>
    <p style="text-align:center;font-size:1.12em"><em>Y</em> = <em>cM</em><sup>β</sup>.</p>
    <p>A single power law would be scale-free over its fitted range.</p>
    <p>Maximum running speed is a useful counterexample. It rises and then falls with body mass because different physical constraints dominate at different sizes.</p>
  </div>
</div>

<div class="figure-caption">Labonte et al. (2024), <a href="https://doi.org/10.1038/s41467-024-46269-w">“Dynamic similarity and the peculiar allometry of maximum running speed”</a>, Fig. 1. Data span 633 animals; figure reproduced under CC BY 4.0.</div>
""",
        "scale-free-distinctions-reader": r"""# Power laws and scale-free behaviour

<div class="slide-columns evidence-layout" style="grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="meaning-panel" style="text-align:left">
    <h3>The mathematical connection</h3>
    <p>A power law <em>y</em> = <em>Cx</em><sup>α</sup> is scale-free because</p>
    <p style="text-align:center;font-size:1.08em"><em>y</em>(<em>ax</em>) = <em>a</em><sup>α</sup><em>y</em>(<em>x</em>).</p>
    <p>Rescaling changes the magnitude predictably without introducing a preferred value of <em>x</em>. Exact scale invariance in one variable leads to a power law under ordinary regularity assumptions.</p>
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>The empirical distinction</h3>
    <p><strong>Power law</strong> names a precise functional or distributional model.</p>
    <p><strong>Scale-free</strong> is often used more broadly for approximate invariance of a geometry, relationship, or distribution over a stated range.</p>
    <p>A real system can be approximately scale-free without following one exact power law at every scale.</p>
  </div>
</div>

<div class="figure-caption">Clauset, Shalizi and Newman (2009), <a href="https://doi.org/10.1137/070710111">“Power-Law Distributions in Empirical Data”</a>, <em>SIAM Review</em> 51, 661–703.</div>
""",
        "scale-free-broader-note-reader": r""":::{note} Scale-free is the broader claim
An exact one-variable relationship that is unchanged in form under every positive rescaling is, under mild regularity conditions, a power law. In applications, however, **scale-free** is the broader interpretation: it says that the measured relationship or structure has no single preferred scale over the range being studied.

A power law is one precise mathematical model for that behaviour. A real system may be approximately scale-free over a finite range without following one exact power law everywhere. If the evidence establishes only an unusually broad tail, **heavy-tailed** is the safer description.
:::
""",
        "power-law-why-label": r"""## Why the label matters

<p><strong>Power law is not a bad label. It is a strong one.</strong> It claims that the same relative scaling rule continues across the fitted range, with no typical event size organising that range. A lognormal, stretched exponential, or power law with a cut-off may also produce a heavy tail or a nearly straight section on a log-log plot. Use <strong>heavy-tailed</strong> when that is all the evidence supports.</p>

<div class="slide-columns evidence-layout" style="grid-template-columns:repeat(3,1fr);align-items:stretch">
  <div class="meaning-panel" style="text-align:left">
    <h3>Extreme events</h3>
    <p>A pure power law makes very large observations uncommon but not exponentially suppressed. A cut-off can make them far rarer.</p>
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>Extrapolation</h3>
    <p>A power law predicts that the same exponent continues beyond the observed values. A cut-off says that it does not.</p>
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>Mechanism</h3>
    <p>The fitted form constrains an explanation, but the same power law can still arise from several mechanisms.</p>
  </div>
</div>

If the tail is not a power law, a characteristic scale or cut-off may still constrain the largest events. That changes what we predict beyond the observed data. Test a power law against plausible alternatives before making the stronger claim.
""",
        "power-law-data-types": r"""## Power-law data can be discrete or continuous

<div class="slide-columns evidence-layout" style="grid-template-columns:1.12fr .88fr;align-items:start">
  <div class="meaning-panel" style="padding:.35rem;align-self:start">
    <img src="images/power_law_discrete_continuous.svg" alt="Synthetic discrete and continuous power-law data shown through complementary cumulative distributions" style="display:block;width:100%;max-height:390px;object-fit:contain;margin:0 auto">
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>What kind of variable is measured?</h3>
    <p><strong>Discrete:</strong> node degree, word count, branch number, or Strahler order.</p>
    <p><strong>Continuous:</strong> branch length, diameter, height, biomass, body mass, or speed.</p>
    <p>The tree examples contain both. Branch rank and branch number are discrete. Length, diameter and biomass are continuous. The fitting method must respect that distinction.</p>
  </div>
</div>

<div class="figure-caption">Course-generated illustration following the discrete and continuous examples in Clauset, Shalizi and Newman (2009), Fig. 3.1.</div>
""",
        "network-scale-free": r"""## Example 2: Scale-free networks

For a network, $k$ is the number of edges attached to a node. A scale-free network claim usually concerns the degree distribution:

$$P(k)\propto k^{-\gamma}.$$

<div class="slide-columns evidence-layout" style="grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="meaning-panel" style="text-align:left">
    <h3>What it does claim</h3>
    <p>The claim concerns a <strong>distribution of node degrees</strong>. There is no typical degree that organises the idealised distribution.</p>
  </div>
  <div class="meaning-panel" style="text-align:left">
    <h3>What it does not claim</h3>
    <p>The network drawing need not look identical under magnification. A scale-free degree distribution does not make the network a spatial fractal.</p>
  </div>
</div>

The term has often been used too loosely. **Heavy-tailed** is safer unless a power law has been tested against alternatives.

<div class="figure-caption">Barabási and Albert (1999), <a href="https://doi.org/10.1126/science.286.5439.509">“Emergence of Scaling in Random Networks”</a>; Broido and Clauset (2019), <a href="https://doi.org/10.1038/s41467-019-08746-5">“Scale-free networks are rare”</a>.</div>
""",
        "zipf-law": r"""## Example 3: Zipf’s law

<div class="slide-columns evidence-layout" style="grid-template-columns:1.2fr .8fr;align-items:start">
  <div class="meaning-panel" style="align-self:start">
    <img src="images/zipf_pride_prejudice.svg" alt="Log-log rank-frequency plot for words in Pride and Prejudice" style="display:block;width:100%;max-height:345px;object-fit:contain">
  </div>
  <div class="meaning-panel" style="text-align:left">
    <p>Order words from most to least frequent. Zipf’s law proposes</p>
    <p style="text-align:center;font-size:1.12em"><em>f</em>(<em>r</em>) ∝ <em>r</em><sup>−<em>α</em></sup>, &nbsp; often with <em>α</em> near 1.</p>
    <p>This is one illustration of a broader rank-size pattern reported for words, city populations, firm sizes, website activity, and other ordered collections.</p>
    <p>Many local acts of use, growth, competition, or reuse can leave this simple system-level pattern. Zipf's law describes what must be explained; it does not identify the mechanism.</p>
    <p><strong>Qualification:</strong> definitions, finite size, and the fitted range all matter.</p>
  </div>
</div>

<div class="figure-caption">Illustrative word counts from Jane Austen, <em>Pride and Prejudice</em>; ranks 10–1000, not a formal power-law test. See <a href="https://doi.org/10.1038/srep00812">Cristelli, Batty and Pietronero (2012)</a>.</div>
""",
        "scale-free-examples": r"""# Scale-free patterns in real complex systems

Scale-free and approximately scale-free relationships appear in many kinds of system. Here we compare trees, organisms, networks, language, cities, earthquakes, and critical phenomena.

The recurring mathematical question is:

> Does the same relationship remain useful when the scale of observation or system size changes?

The examples need not share a mechanism. The scaling relationship is a system-level pattern that a model must explain.
""",
        "more-scale-free-examples": r"""## More examples

<table class="standard-table">
  <colgroup><col style="width:27%"><col style="width:40%"><col style="width:33%"></colgroup>
  <thead><tr><th>System</th><th>Measured relationship</th><th>Important qualification</th></tr></thead>
  <tbody>
    <tr><td>Language</td><td>word frequency versus rank</td><td>Zipf scaling is approximate and corpus-dependent</td></tr>
    <tr><td>Cities</td><td>population versus rank</td><td>definitions of a “city” and the fitted range matter</td></tr>
    <tr><td>Earthquakes</td><td>event frequency versus size</td><td>catalogue completeness sets a lower cut-off</td></tr>
    <tr><td>Critical systems</td><td>event size or duration distributions</td><td>finite systems impose upper cut-offs</td></tr>
    <tr><td>Networks</td><td>node-degree distributions</td><td>heavy-tailed does not automatically mean power-law</td></tr>
  </tbody>
</table>

<div class="figure-caption">Examples reviewed by Newman (2005), <a href="https://doi.org/10.1080/00107510500052444">“Power laws, Pareto distributions and Zipf’s law”</a>. Earthquake frequency is commonly represented by the Gutenberg–Richter relationship.</div>
""",
        "finite-scale-free-reader": r"""# Real systems are scale-free only over a range

Exact fractals continue through every mathematical generation. Real systems have limits.

<table class="standard-table">
  <colgroup><col style="width:24%"><col style="width:76%"></colgroup>
  <tbody>
    <tr><th>Lower cut-off</th><td>Cell size, grain size, or measurement resolution becomes visible.</td></tr>
    <tr><th>Scaling range</th><td>The same approximate relationship is useful across several scales.</td></tr>
    <tr><th>Upper cut-off</th><td>The finite size and global geometry of the system become important.</td></tr>
  </tbody>
</table>

> The measured quantity is approximately scale-free over a stated range.

That range is part of the result. It must be justified using the system and the measurement process.
""",
        "scale-free-diagnostic-reader": r"""## How would we test a scale-free claim?

An exponential relationship contains a characteristic scale:

$$y(x)=Ce^{-x/\tau}.$$

The parameter $\tau$ is the decay scale. The relationship becomes a straight line on semi-logarithmic axes:

$$\log y=\log C-\frac{x}{\tau}.$$

A power law,

$$y(x)=Cx^{-\alpha},$$

becomes a straight line on logarithmic axes:

$$\log y=\log C-\alpha\log x.$$

A straight-looking section of a log-log plot is a useful diagnostic, not proof of a power law. A credible analysis should report the fitted range, uncertainty, alternative models, and sensitivity to the measurement procedure.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>For a circle, coastline, cauliflower, Gaussian distribution, and power-law event-size distribution: what is being rescaled, is there a characteristic scale, and what evidence would support the claim?</span></div>

For a fuller statistical treatment, see Clauset, Shalizi and Newman (2009), <a href="https://doi.org/10.1137/070710111">“Power-Law Distributions in Empirical Data”</a>, <em>SIAM Review</em> 51, 661–703.
""",
        "scale-free-complex-systems-reader": r"""# Why this matters in Complex Systems

Fractal geometry applies scaling ideas to spatial structure. The same language can describe other quantities, including event sizes, durations, fluctuations, and network measurements.

Scale-free behaviour may arise from several different mechanisms. Later in the unit we will see it in connection with critical phenomena, percolation, and self-organised criticality. Observing a power law does not identify the mechanism by itself. It gives us a compact pattern that the mechanism must explain.
""",
    }
    shared_scale_free = {
        "scale-free-bridge-reader",
        "scale-free-definition-reader",
        "scale-free-circle-reader",
        "return-to-branching-scale-free",
        "tree-allometry-across-trees",
        "tree-allometry-within-tree",
        "allometry-beyond-fractals",
        "scale-free-examples",
        "more-scale-free-examples",
        "finite-scale-free-reader",
        "scale-free-complex-systems-reader",
    }
    for cell_id, text in reader_sections.items():
        shared = cell_id in shared_scale_free
        cell = by_id.setdefault(
            cell_id,
            _markdown(
                cell_id,
                "",
                tag="slides" if shared else "reader-only",
                slide_type="slide" if shared else "skip",
            ),
        )
        cell["metadata"] = {
            "tags": ["slides" if shared else "reader-only"],
            "slideshow": {"slide_type": "slide" if shared else "skip"},
        }
        _set_source(cell, text)

    reminder = by_id.setdefault(
        "project-statistics-reminder",
        _markdown(
            "project-statistics-reminder", "", tag="slides", slide_type="slide"
        ),
    )
    reminder["metadata"] = {
        "tags": ["slides"],
        "slideshow": {"slide_type": "slide"},
    }
    reminder_text = """# A reminder for your project

<img src="images/error_bars.png" alt="A hand-drawn joke showing error bars recursively placed on error bars" style="display:block;width:min(48%,430px);max-height:390px;object-fit:contain;margin:.2rem auto .7rem">

<div class="choice-marker"><img src="images/choice_marker.svg" alt="" width="34" height="34"><span><strong>You will need to run statistics for your project.</strong> Your code needs to be functional early enough to test, diagnose, and revise it.</span></div>
"""
    _set_source(reminder, reminder_text)

    retired = {
        "why_complex_systems",
        "not-all-fractals",
        "three-fractal-roles",
        "fractal-tension",
    }
    ordered = [cell for cell in cells if cell.get("id") not in retired]
    present = {cell.get("id") for cell in ordered}
    for cell_id in (
        "cezanne-mandelbrot-contrast",
        "fractal-properties-core",
        "cantor-limit-reader",
        "sierpinski-limit-reader",
        "generation-methods-summary",
        "generation-methods-summary-reader",
        "linear-scale-factor-reader",
        "invent-a-fractal-reader",
        *reader_sections.keys(),
        "project-statistics-reminder",
    ):
        if cell_id not in present:
            ordered.append(by_id[cell_id])
            present.add(cell_id)

    def move_after(cell_id: str, anchor_id: str) -> None:
        nonlocal ordered
        moving = next(cell for cell in ordered if cell.get("id") == cell_id)
        ordered = [cell for cell in ordered if cell.get("id") != cell_id]
        anchor = next(i for i, cell in enumerate(ordered) if cell.get("id") == anchor_id)
        ordered.insert(anchor + 1, moving)

    move_after("cezanne-mandelbrot-contrast", "dla-natural-comparison")
    move_after("fractal-properties-core", "fractal-visual-test")
    move_after("cantor-limit-reader", "cantor-ifs")
    move_after("sierpinski-limit-reader", "sierpinski-ifs")
    move_after("generation-methods-summary", "l-systems-reader")
    move_after("generation-methods-summary-reader", "generation-methods-summary")
    move_after("linear-scale-factor-reader", "euclidean-scaling")
    move_after("invent-a-fractal-reader", "similarity-dimension")

    # Horizontal arrows introduce a new construction method. Vertical arrows
    # compare examples within that method.
    hierarchy = {
        "initiator-generator-cantor": "slide",
        "initiator-generator-sierpinski": "subslide",
        "cantor-ifs": "slide",
        "sierpinski-ifs": "subslide",
        "chaos-game": "subslide",
        "l-system-definition": "slide",
        "cantor-l-system": "subslide",
        "l-systems": "subslide",
        "euclidean-expectations": "subslide",
        "scale-free-definition-reader": "subslide",
        "scale-free-circle-reader": "subslide",
        "scale-free-examples": "slide",
        "return-to-branching-scale-free": "subslide",
        "tree-allometry-across-trees": "subslide",
        "tree-allometry-within-tree": "subslide",
        "allometry-beyond-fractals": "subslide",
        "more-scale-free-examples": "subslide",
        "finite-scale-free-reader": "slide",
    }
    for cell_id, slide_type in hierarchy.items():
        if cell_id in by_id:
            by_id[cell_id]["metadata"]["slideshow"]["slide_type"] = slide_type

    scale_free_order = (
        "scale-free-bridge-reader",
        "characteristic-scale-reader",
        "scale-free-definition-reader",
        "scale-free-circle-reader",
        "scale-free-distinctions-reader",
        "scale-free-broader-note-reader",
        "power-law-why-label",
        "power-law-data-types",
        "scale-free-examples",
        "return-to-branching-scale-free",
        "tree-allometry-across-trees",
        "tree-allometry-within-tree",
        "allometry-beyond-fractals",
        "network-scale-free",
        "zipf-law",
        "more-scale-free-examples",
        "finite-scale-free-reader",
        "scale-free-diagnostic-reader",
        "scale-free-complex-systems-reader",
    )
    scale_free_anchor = "box-counting-intuition"
    for cell_id in scale_free_order:
        move_after(cell_id, scale_free_anchor)
        scale_free_anchor = cell_id
    move_after("euclidean-expectations", "scale-free-bridge-reader")
    move_after("common-language", scale_free_anchor)
    move_after("complex_system_signatures", "common-language")
    # The shared reminder cell is both the final slide and the final Reader
    # content. Remove an older duplicate reader-only copy if it exists.
    ordered = [
        cell
        for cell in ordered
        if cell.get("id") != "project-statistics-reminder-reader"
    ]

    notebook["cells"] = ordered


if __name__ == "__main__":
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    path = root / "notebooks/week02/L_Fractals.ipynb"
    data = json.loads(path.read_text())
    apply_current_week02(data)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
