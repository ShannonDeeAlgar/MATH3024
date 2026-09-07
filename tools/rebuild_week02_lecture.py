#!/usr/bin/env python3
"""Rebuild the Week 2 fractals lecture as a dual Reader and slide source."""

from pathlib import Path

import nbformat as nbf

from finalise_week02_current import apply_current_week02


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "notebooks/week02/L_Fractals.ipynb"


def md(source: str, cell_id: str, *, tags=(), slide_type="subslide"):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = list(tags)
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


def code(source: str, cell_id: str, *, tags=(), slide_type="subslide"):
    cell = nbf.v4.new_code_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = list(tags)
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


def notes(source: str, cell_id: str):
    return md(source, cell_id, tags=("presenter-notes",), slide_type="notes")


def main():
    notebook = nbf.v4.new_notebook()
    notebook.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "math3024_slide_format": "blue-period-v3",
    }
    notebook.cells = [
        md(r"""
# Fractals
## MATH3024 · Week 2
""", "week02-title", tags=("slides",), slide_type="slide"),

        md(r"""
# Listen first · “Mandelbrot Set”

<iframe
  width="800"
  height="450"
  src="https://www.youtube.com/embed/nVIYiBdfGwE"
  title="Jonathan Coulton's Mandelbrot Set song"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen
  style="display:block;max-width:100%;margin:0 auto">
</iframe>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt=""><span>The recurrence sounds plausible. Which quantity labels the point in the picture, and where should its orbit begin?</span></div>
<p class="figure-reference">Technical caveat: the song conflates the parameter <em>c</em> with the initial state <em>z</em><sub>0</sub>. The next slide gives the precise definition.</p>
""", "opening-song", tags=("slides",), slide_type="slide"),

        md(r"""
# Why begin here?

The Mandelbrot set is not a complex system in the strongest sense used in this unit. It has no population of interacting agents, adaptive components, or physical network.

It is nevertheless an unusually pure illustration of several central ideas:

- a short nonlinear rule generates intricate global organisation;
- each output becomes the next input, creating feedback through iteration;
- nearby parameter values can produce qualitatively different long-term behaviour;
- stable, periodic, and escaping regimes occupy one structured parameter plane; and
- organised detail persists across arbitrarily fine mathematical scales.

Complex systems often create structure spanning many scales too. Fractal geometry gives us language for describing that structure. We must then ask a separate question: **which interactions, growth processes, or repeated local rules generated it?**
""", "week02-route", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Build a controlled fractal
The motivating systems are finite, noisy, and dependent on their mechanisms. To understand scaling and dimension cleanly, we now remove that messiness on purpose.

<div class="reader-route">
  <div class="reader-route-body">empirical patterns → exact calibration models → dimension → return to data</div>
</div>

The Cantor set and Sierpiński triangle are **not complex systems in this unit**. They are controlled mathematical constructions. Their exact rules let us establish what scaling quantities mean before estimating them in branching forms and coastlines.
""", "session2-controlled-fractals", tags=("slides",), slide_type="slide"),

        md(r"""
# The Mandelbrot set

<iframe
  width="800"
  height="450"
  src="https://www.youtube.com/embed/b005iHf8Z3g"
  title="Fractal zoom"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen
  style="display:block;margin:0 auto">
</iframe>

$$z_{n+1}=z_n^2+c,\qquad z_0=0.$$

The Mandelbrot set contains the values $c$ for which this orbit remains bounded (black). Outside the set, colour usually records how quickly the orbit escapes: points with similar escape times receive similar colours.
""", "opening-video-slides", tags=("slides-only",), slide_type="subslide"),

        md(r"""
## The Mandelbrot set under magnification

<iframe
  width="960"
  height="540"
  src="https://www.youtube.com/embed/b005iHf8Z3g"
  title="Fractal zoom showing repeated structure across scales"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen
  style="display:block;max-width:100%;margin:0 auto">
</iframe>

Black marks the set itself. The colours outside it encode escape time: how many iterations are required before an orbit is judged to be diverging. Different palettes can colour the same Mandelbrot set differently.

For every complex parameter $c$, begin at $z_0=0$ and iterate

$$z_{n+1}=z_n^2+c.$$

Each value of $c$ specifies a different dynamical system. The Mandelbrot set contains precisely those parameter values whose orbit remains bounded. It is best understood as a **map of a family of dynamical systems**, rather than as one trajectory.

### A useful error in the song

The song uses a point called $z$ as the point being classified, while retaining a separate parameter $c$. That is ambiguous. For the Mandelbrot set, the plotted point is $c$ and every orbit begins at the critical point $z_0=0$. If $c$ is fixed while the initial value $z_0$ varies, the bounded points instead form the **filled Julia set** for that value of $c$. The song becomes essentially correct if its plotted point is reinterpreted as $c$ and the missing initial condition $z_0=0$ is supplied. Coulton later acknowledged that the sung description was incomplete or wrong.

Mandelbrot's 1980 paper used the equivalent logistic family

$$z_{n+1}=\lambda z_n(1-z_n),$$

and studied how its behaviour changes across the complex parameter plane. With the affine change of variable $w=\lambda/2-\lambda z$, the iteration becomes

$$w_{n+1}=w_n^2+c,\qquad c=\frac{\lambda}{2}-\frac{\lambda^2}{4}.$$

Figure 1 is therefore an early $\lambda$-plane parameter map related to the modern Mandelbrot set, not the familiar picture in its current coordinates and orientation.

<figure class="reader-figure reader-figure-small">
  <img src="images/mandelbrot_1980_figure1.png" alt="Figure 1 from Mandelbrot's 1980 paper, showing a complex parameter-plane domain" style="display:block;width:100%">
  <figcaption>Figure 1 from Mandelbrot's 1980 study of the complex logistic family. The white central disc was intentionally left blank to expose the surrounding structure.</figcaption>
</figure>

B. B. Mandelbrot (1980), [“Fractal aspects of the iteration of $z\mapsto\lambda z(1-z)$ for complex $\lambda$ and $z$”](https://people.ucsc.edu/~rmont/classes/chao/2013/Orig_Papers/Mandelbrot.pdf), *Annals of the New York Academy of Sciences* 357, 249–259. Jonathan Coulton discusses the mathematical caveat in [“And I Couldn’t Even Get the Math Right”](https://www.jonathancoulton.com/2010/10/18/and-i-couldnt-even-get-the-math-right/).
""", "opening-video-reader", tags=("reader-only",), slide_type="skip"),

        notes(r"""
While the video runs, say:

“Every point in this picture represents one complex number $c$. Starting from $z_0=0$, we repeatedly apply the same very short rule, $z_{n+1}=z_n^2+c$. The black set contains values for which the resulting orbit remains bounded. The colour records how quickly other orbits escape.

Watch the boundary rather than trying to follow one location. At each magnification, familiar bulbs and miniature ‘snowmen’ return, but they are surrounded by new filaments and spirals. The same deterministic rule produces recognisable organisation and apparently inexhaustible detail.

The video can continue zooming because this is a mathematical object, not a digital photograph of a physical surface. The displayed pixels are finite, but the definition is not tied to one pixel size. Today we will ask what it means for structure to persist as scale changes, how we measure that persistence, and when a similar claim is defensible for finite natural systems.”

Afterwards, ask what changed and what remained recognisably similar. Collect language such as repetition, nested structure, irregular boundary, and new detail. Distinguish direct observations from the inference of infinite mathematical detail.
""", "opening-notes"),

        md(r"""
# What Euclidean geometry keeps, and what it misses

**Scale** is the size or resolution at which we observe, measure, or describe a system.

<div class="slide-columns evidence-layout" style="grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="meaning-panel" style="text-align:left;min-width:0;display:flex;flex-direction:column">
    <div style="height:230px;display:flex;align-items:center;justify-content:center">
      <div style="width:150px;height:150px;border:5px solid #1B2A4C;border-radius:50%"></div>
    </div>
    <strong>Circle</strong>
    <p style="margin:0">One radius is a <strong>characteristic scale</strong>: it organises every other length. Magnification reveals the same smooth arc. Its boundary has dimension 1.</p>
  </div>
  <div class="meaning-panel" style="text-align:left;min-width:0;display:flex;flex-direction:column">
    <div style="height:230px;display:flex;align-items:center;justify-content:center;overflow:hidden">
      <img src="images/mandelbrot_scale_symmetry.png" alt="The Mandelbrot set and a miniature copy after deep magnification" style="display:block;width:100%;height:100%;object-fit:contain;margin:0">
    </div>
    <strong>Mandelbrot set</strong>
    <p style="margin:0">No single length organises its boundary. Scale is expressed through changing resolution and repeated ratios. Magnification reveals further structure.</p>
  </div>
</div>

Shape, position, size, and rigid-motion invariance still make sense for both objects. What fails is their sufficiency: those descriptions do not capture how Mandelbrot-boundary detail changes with resolution.
""", "euclidean-expectations", tags=("slides",), slide_type="slide"),

        md(r"""
# What is scale?

**Scale is the size or resolution at which we observe, measure, or describe a system.**

<div class="qa-grid">
  <div class="qa-row"><p class="qa-question">A physical object</p><p class="qa-answer">millimetres, metres, or kilometres</p></div>
  <div class="qa-row"><p class="qa-question">A changing process</p><p class="qa-answer">microseconds, days, or generations</p></div>
  <div class="qa-row"><p class="qa-question">A mathematical construction</p><p class="qa-answer">magnification, subdivision depth, or ruler length</p></div>
</div>

Changing scale means changing the comparison length, time interval, or resolution through which structure is visible.
""", "scale-intuition", tags=("slides",), slide_type="slide"),

        md(r"""
## When is a scale “characteristic”?

A scale is **characteristic** when one value organises an object's important geometry or behaviour.

<div class="qa-grid">
  <div class="qa-row"><p class="qa-question">Circle</p><p class="qa-answer">its radius fixes every other length</p></div>
  <div class="qa-row"><p class="qa-question">Wave or cycle</p><p class="qa-answer">a dominant wavelength or period</p></div>
  <div class="qa-row"><p class="qa-question">Interacting system</p><p class="qa-answer">an interaction range or correlation length</p></div>
  <div class="qa-row"><p class="qa-question">Exact fractal</p><p class="qa-answer">no single organising length; only a repeated ratio between levels</p></div>
  <div class="qa-row"><p class="qa-question">Empirical fractal-like system</p><p class="qa-answer">lower and upper cut-offs bound a scaling range; between them, no single length captures all visible structure</p></div>
</div>

The unit of measurement is external to the object. How the measurement changes with scale records its geometry.
""", "characteristic-scale", tags=("slides",), slide_type="subslide"),

        md(r"""
# What do we mean by dimension?

![A point extended successively into a line, square, and cube](images/dimension_extension.svg)

Each new dimension adds an **independent direction** in which a point can vary.
""", "dimension-directions", tags=("slides",), slide_type="slide"),

        md(r"""
## Dimension as information

To identify one location to a chosen precision, how many independent numbers must we provide?

<table class="standard-table">
  <colgroup><col style="width:28%"><col style="width:72%"></colgroup>
  <thead><tr><th>Space</th><th>Information needed</th></tr></thead>
  <tbody>
    <tr><td>Line</td><td>one coordinate: $x$</td></tr>
    <tr><td>Plane</td><td>two coordinates: $(x,y)$</td></tr>
    <tr><td>Space</td><td>three coordinates: $(x,y,z)$</td></tr>
    <tr><td>$\mathbb{R}^n$</td><td>$n$ independent coordinates: $(x_1,\ldots,x_n)$</td></tr>
  </tbody>
</table>
""", "dimension-information", tags=("slides",), slide_type="subslide"),

        md(r"""
## Dimension as a scaling count

<div class="slide-columns" style="grid-template-columns:1.35fr .65fr;align-items:center">
  <div>
    <img src="images/dimension_scaling.svg" alt="Lines, squares, and cubes divided at two resolutions" style="width:100%;max-height:390px;object-fit:contain">
    <p style="white-space:nowrap;font-size:.86em"><strong>Halve the length scale:</strong> a line needs 2 copies, a square 4, and a cube 8.</p>
  </div>
  <div class="scaling-variables">
    <p><em>m</em>: pieces along each direction</p>
    <p><em>r</em> = 1/<em>m</em>: linear scale of one copy</p>
    <p><em>d</em>: dimension</p>
    <p><em>N</em>: copies needed</p>
  </div>
</div>

For Euclidean objects, $N=m^d=r^{-d}$.
""", "euclidean-scaling", tags=("slides",), slide_type="subslide"),

        md(r"""
These three views describe the same Euclidean dimension:

- the number of independent directions available;
- the number of coordinates needed to locate a point;
- the exponent connecting resolution to the number of cells required.

For a Euclidean object that can be decomposed into $N$ identical copies, each scaled by a linear factor $r$,

$$N=r^{-d}, \qquad d=\frac{\log N}{\log(1/r)}.$$

At resolution $r$, choosing one of $N(r)$ cells requires roughly

$$\log_2 N(r)=d\log_2(1/r)$$

bits. This information view becomes especially useful for high-dimensional data. The scaling form will also survive when $d$ is no longer an integer.
""", "euclidean-scaling-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# One length is no longer enough
## How long is a coastline?

A straight ruler resolves some bends and skips others. Changing its length changes which structure is counted.

![Successively finer measurements of the British coastline](images/Great-britain-coastline-paradox.gif)

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>As the ruler shrinks, what happens to the measured length? Must it converge?</span></div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down the ladder:</strong> inspect what one ruler does locally. <strong>Up the ladder:</strong> compress the relationship between ruler length and total count.</span></div>
""", "coastline-question", tags=("slides",), slide_type="slide"),

        md(r"""
## The coastline paradox

Let $L(\varepsilon)$ be the measured length using rulers of length $\varepsilon$.

For a smooth curve, $L(\varepsilon)$ approaches a finite value as $\varepsilon$ becomes small. For a fractal-like boundary,

$$L(\varepsilon)\propto \varepsilon^{1-D},$$

so a dimension $D>1$ makes the measured length grow as the ruler shrinks.

The coastline is finite at every chosen resolution. The paradox is that there is no resolution-independent answer supplied by the geometry alone.

Mandelbrot's classic treatment is B. Mandelbrot (1967), [“How Long Is the Coast of Britain? Statistical Self-Similarity and Fractional Dimension”](https://doi.org/10.1126/science.156.3775.636), *Science* 156, 636–638.
""", "coastline-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# What are we looking at here?

<img src="images/Happisburgh_footprints_cropped.jpg" alt="A cropped view of water-filled Happisburgh footprints" style="display:block;width:78%;max-height:500px;object-fit:contain;margin:0 auto .45rem">

<div class="discussion-marker" style="width:78%;margin:.25rem auto 0"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span><strong>What is the scale?</strong> Nanometres, centimetres, or kilometres?</span></div>
""", "happisburgh-cropped", tags=("slides-only",), slide_type="slide"),

        md(r"""
# A Euclidean object in the photo helps

<div class="slide-columns">
  <img class="column-image" src="images/Happisburgh_scale_coin.png" alt="Happisburgh footprints with a coin-sized reference object">
  <div>
    <p>The photographer included a penny.</p>
    <p>Its known diameter acts as a Euclidean ruler, supplying one characteristic length against which every other length can be compared.</p>
  </div>
</div>
""", "happisburgh-coin", tags=("slides-only",), slide_type="subslide"),

        md(r"""
# I lied

<div class="slide-columns">
  <img class="column-image" src="images/Happisburgh_scale_plate.png" alt="Happisburgh footprints with a dinner-plate reference object">
  <div>
    <p>That was not a coin. It was a dinner plate.</p>
    <p>This is a giant footprint, left by something that once walked across this land.</p>
    <div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Why can an equally plausible reference object reverse our interpretation?</span></div>
  </div>
</div>
""", "happisburgh-plate", tags=("slides-only",), slide_type="subslide"),

        md(r"""
# Now the truth

<div class="slide-columns">
  <img class="column-image" src="images/Happisburgh_footprints.jpg" alt="Happisburgh footprints with a lens cap providing a reference scale">
  <div>
    <p>The photographed object is a lens cap.</p>
    <p>These are the Happisburgh hominin footprints, preserved in Early Pleistocene deposits on the Norfolk coast.</p>
    <p>They provide evidence of early human presence in northern Europe more than 800,000 years ago.</p>
  </div>
</div>

<div class="figure-caption">Photograph: Martin Bates, Happisburgh Project. See Ashton et al. (2014), “Hominin Footprints from Early Pleistocene Deposits at Happisburgh, UK,” <em>PLOS ONE</em> 9, e88329.</div>
""", "happisburgh-context", tags=("slides-only",), slide_type="subslide"),

        md(r"""
## What are we looking at here?

![Cropped view of the Happisburgh footprints](images/Happisburgh_footprints_cropped.jpg)

The cropped water-filled footprints are difficult to interpret because there is no reference length. In the lecture I deliberately exploit that ambiguity. I first claim that the image shows a baby's footprint and that the circle is a coin. I then admit that this was a lie, claim that the circle is a dinner plate, and recast the mark as a giant footprint. Both stories are inventions. The same apparent circle supports radically different physical interpretations because the image alone does not supply its scale.

<div class="analysis-perspectives">
  <div><strong>Coin interpretation</strong><p>The familiar object is assumed to be only a few centimetres wide, so the footprint appears small.</p></div>
  <div><strong>Plate interpretation</strong><p>The equally large image is assumed to represent an object tens of centimetres wide, so the footprint appears enormous.</p></div>
</div>

### First interpretation: a coin

![Scale interpretation using a coin](images/Happisburgh_scale_coin.png)

### Second interpretation: a dinner plate

![Scale interpretation using a dinner plate](images/Happisburgh_scale_plate.png)

The genuine photograph reveals that the object was a lens cap. Once its diameter is known, all other lengths scale in direct proportion, areas with its square, and volumes with its cube. Changing magnification changes the numerical measurements, but it does not reveal a new hierarchy of geometric structure.

![The genuine Happisburgh photograph with a lens cap providing scale](images/Happisburgh_footprints.jpg)

<div class="figure-caption">Photograph: Martin Bates, Happisburgh Project. See Ashton et al. (2014), “Hominin Footprints from Early Pleistocene Deposits at Happisburgh, UK,” <em>PLOS ONE</em> 9, e88329.</div>

This is a useful warning for empirical fractal analysis. A scaling range must be justified from the system and measurement process, not selected from an attractive plot alone.
""", "happisburgh-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Symmetry of a Euclidean object

<div class="qa-grid">
  <div class="qa-row"><p class="qa-question">Reflect a circle through its centre</p><p class="qa-answer">the image is unchanged</p></div>
  <div class="qa-row"><p class="qa-question">Rotate a circle about its centre</p><p class="qa-answer">the image is unchanged</p></div>
  <div class="qa-row"><p class="qa-question">Magnify its boundary</p><p class="qa-answer">a smooth edge becomes locally one-dimensional</p></div>
  <div class="qa-row"><p class="qa-question">Magnify its interior</p><p class="qa-answer">a filled region becomes locally two-dimensional</p></div>
</div>

Magnification is not a symmetry of the circle. At sufficiently high magnification, neither its edge nor its interior still looks like a circle.
""", "scale-symmetry", tags=("slides",), slide_type="slide"),

        md(r"""
# Symmetry of a fractal object

<div class="slide-columns" style="grid-template-columns:.8fr 1.2fr;align-items:center">
  <img class="column-image" src="images/mandelbrot_scale_symmetry.png" alt="The Mandelbrot set and a miniature copy found after deep magnification" style="max-height:190px">
  <div><p><strong>Symmetry under magnification:</strong> after a large change in scale, related Mandelbrot organisation reappears. It is recognisable without being an identical copy of its entire neighbourhood.</p></div>
</div>

<div class="reader-voice">
  <div class="reader-voice-quote">Nature exhibits not simply a higher degree but an altogether different level of complexity.</div>
  <div class="reader-voice-attr">Benoit Mandelbrot, <em>The Fractal Geometry of Nature</em> (1982)</div>
</div>

For empirical forms, resemblance under magnification is approximate and holds only across a finite range of scales.
""", "fractal-scale-symmetry", tags=("slides",), slide_type="slide"),

        md(r"""
![A Romanesco cauliflower showing branching at multiple scales](images/Cauliflower_AVM.jpg)

Natural objects are not exact mathematical fractals. A cauliflower has a smallest biological scale and a largest organism scale. Within a finite range, however, branching motifs recur and scaling descriptions can be informative.

<div class="figure-caption">Photograph: AVM, <a href="https://commons.wikimedia.org/wiki/File:Cauliflower_Fractal_AVM.JPG">“Cauliflower Fractal AVM”</a>, Wikimedia Commons, CC BY-SA 3.0.</div>

This distinction matters throughout the unit:

- **exact self-similarity** is a property of an ideal mathematical construction;
- **statistical self-similarity** describes distributions or summary patterns that remain similar across a range of scales.
""", "scale-symmetry-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# When smoothness fails
## An early mathematical “monster”

<div class="slide-columns" style="grid-template-columns:1.25fr .75fr;align-items:center">
  <img class="column-image" src="images/WeierstrassFunction.png" alt="A graph of a Weierstrass nowhere-differentiable function" style="max-height:430px;object-fit:contain">
  <div>
    <p>For suitable <em>a</em> between 0 and 1 and integer <em>b</em> greater than 1, higher-frequency waves enter with smaller amplitudes.</p>
    <p>The sum is continuous, but no point settles into a straight local tangent.</p>
  </div>
</div>

$$W(x)=\sum_{n=0}^{\infty}a^n\cos\!\left(b^n\pi x\right).$$

Cantor, Sierpiński, and Weierstrass were all associated with the nineteenth- and early twentieth-century tradition of mathematical “monsters”: exact counterexamples that exposed limits in familiar geometric and analytic intuition. Weierstrass challenges tangents, Cantor challenges length and cardinality, and Sierpiński challenges area and boundary.

<div class="reader-voice"><div class="reader-voice-quote">A rebellion against calculus.</div><div class="reader-voice-attr">Grant Sanderson, 3Blue1Brown</div></div>
""", "weierstrass-monster", tags=("slides",), slide_type="slide"),

        md(r"""
The function introduced by Karl Weierstrass in the nineteenth century became a canonical example of a continuous function that is nowhere differentiable. It was not the first object retrospectively associated with fractal geometry, so it is safer to treat it as an important early mathematical “monster” rather than “the first fractal”.

Its significance was not recreational. Nineteenth-century mathematicians often treated continuity as if it normally implied local smoothness except at isolated exceptional points. Weierstrass supplied a counterexample and helped force sharper definitions of continuity, limits, and differentiability.

For partial sums, every plotted approximation is smooth. The nowhere-differentiable claim concerns the infinite limit: successively higher-frequency terms prevent difference quotients from converging to one tangent slope. A smooth curve becomes locally straight under sufficient magnification. This function does not.
""", "weierstrass-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Recursion is not enough
## A finite imitation beside a genuine fractal

<div class="analysis-perspectives" style="align-items:stretch">
  <div><img src="images/Fractal_hands.jpg" alt="A finite recursive image of hands drawing hands" style="width:100%;height:250px;object-fit:contain"><strong>Finite recursive image</strong><p>Intricate and self-referential, but the recursion visibly stops. This image alone supplies neither an extended scaling range nor an infinite limiting construction.</p></div>
  <div><img src="images/Von_Koch_curve.gif" alt="Successive iterations of the Koch construction" style="width:100%;height:250px;object-fit:contain"><strong>Koch curve: an exact fractal</strong><p>A specified replacement rule continues without bound and gives exact self-similarity and a calculable non-integer dimension.</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>What additional evidence would the finite image need before we called it fractal-like?</span></div>

Fractal tools can still provide **finite-scale shape descriptors** for a non-fractal object. That is useful comparison, but it is not evidence of one scale-independent fractal dimension.
""", "fractal-provocation", tags=("slides",), slide_type="slide"),

        md(r"""
Multiscale fractal methods are also used pragmatically to describe and classify shapes that are not mathematical fractals. In that setting the output is a scale-dependent signature or complexity descriptor, not proof that the object has an asymptotic fractal dimension.

Examples include [“Measuring the complexity of non-fractal shapes by a fractal method”](https://doi.org/10.1016/S0167-8655(00)00061-1), *Pattern Recognition Letters* 21 (2000), and A. R. Backes, J. B. Florindo and O. M. Bruno, [“Shape analysis using fractal dimension: A curvature based approach”](https://doi.org/10.1063/1.4757226), *Chaos* 22 (2012).
""", "nonfractal-descriptors-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Exact fractals and fractal-like forms

<div class="compact-card-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:.55rem;align-items:stretch">
  <div class="meaning-panel"><img src="images/Von_Koch_curve.gif" alt="Successive exact iterations of the Koch curve" style="width:100%;height:135px;object-fit:contain"><strong>Exact · Koch curve</strong><p>A precise rule continues without bound and its dimension can be calculated.</p></div>
  <div class="meaning-panel"><img src="images/Fractal_hands.jpg" alt="A finite recursive image of hands drawing hands" style="width:100%;height:135px;object-fit:contain"><strong>Finite recursion</strong><p>Like a fern, motifs recur for only finitely many levels. A scaling claim needs measurements across that finite range.</p></div>
  <div class="meaning-panel"><img src="images/British_coastline.png" alt="The rough coastline of Great Britain"><strong>Rough · coastline</strong><p>Fractal geometry can be an effective finite-scale description, but roughness alone does not establish one fractal dimension. The estimate remains range- and representation-dependent.</p></div>
</div>
""", "fractal-visual-test", tags=("slides",), slide_type="subslide"),

        md(r"""
# What evidence counts as fractal?

Euclidean descriptions do not always capture how structure is distributed across scales. A visual resemblance is a starting observation, not evidence of fractal scaling.

Look for a defensible combination of:

1. **multiscale persistence:** detail or irregularity remains meaningful as resolution changes;
2. **scaling structure:** exact self-similarity or a statistical scaling relationship holds over a stated range;
3. **geometric consequence:** measured amount, roughness, occupancy, or branching changes predictably with scale;
4. **fractal quantifier:** a dimension or spectrum is stable enough to summarise that range;
5. **generative support:** iteration, growth, interaction, or another mechanism plausibly produces the pattern.

No single item proves fractality. A non-integer dimension is common, but not required. We will return to this checklist when assessing cauliflower, branching, and coastlines.
""", "fractal-properties", tags=("reader-only",), slide_type="skip"),

        md(r"""
# What evidence would count?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Before calling one of the previous objects fractal-like, what would we need to measure rather than recognise by eye?</span></div>

<div class="analysis-perspectives three" style="align-items:stretch">
  <div><strong>1. Name the feature</strong><p>Boundary roughness, occupied mass, branching, or another measurable quantity.</p></div>
  <div><strong>2. Change resolution</strong><p>Test whether its scaling is stable across several defensible scales.</p></div>
  <div><strong>3. State the limits</strong><p>Report cut-offs, uncertainty, and sensitivity to representation.</p></div>
</div>

<p><strong>A convincing claim links a visible pattern to a reproducible scaling measurement over a stated range.</strong></p>
""", "fractal-properties-slide", tags=("slides-only",), slide_type="slide"),

        md(r"""
## Organised complexity, not a contradiction

<div class="analysis-perspectives">
  <div><strong>Regularity and structure</strong><p>Self-similarity means that a recognisable organisation persists as scale changes.</p></div>
  <div><strong>Complexity and detail</strong><p>New structure continues to appear at progressively finer scales.</p></div>
</div>

A fractal is not simply irregular. The repeated rule or scaling relationship is the regular part. The new structure revealed at each finer scale is the detailed part.

The two coexist because a compact rule can be applied repeatedly without the resulting geometry becoming simple.
""", "fractal-tension", tags=("slides",), slide_type="subslide"),

        md(r"""
## An empirical form: cauliflower

<div class="slide-columns">
  <img class="column-image" src="images/Cauliflower_AVM.jpg" alt="A Romanesco cauliflower whose branching pattern recurs across scales">
  <div>
    <p>Smaller branching structures resemble the larger form, but not exactly.</p>
    <p>Growth, finite cell size, damage, and environmental variation limit the scaling range.</p>
    <p>The useful claim is statistical similarity across stated scales, not infinite exact replication.</p>
  </div>
</div>

<p><strong>Evidence check:</strong> identify a scaling range, a measurable recurring feature, and the physical cut-offs.</p>

<div class="figure-caption">Photograph: AVM, <a href="https://commons.wikimedia.org/wiki/File:Cauliflower_Fractal_AVM.JPG">“Cauliflower Fractal AVM”</a>, Wikimedia Commons, CC BY-SA 3.0.</div>
""", "empirical-form", tags=("slides",), slide_type="subslide"),

        md(r"""
# Very different (complex) systems

<div class="compact-card-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:.45rem;align-items:stretch">
  <div class="meaning-panel"><img src="images/paenibacillus_branching.png" alt="Branching bacterial colony"><strong>Colony growth</strong><p>Cells alter local resources and the frontier available to later growth.</p></div>
  <div class="meaning-panel"><img src="images/critical_percolation_cluster.svg" alt="Largest connected cluster in a site-percolation realisation near the critical threshold"><strong>Critical percolation</strong><p>Local occupancy produces connected clusters and voids across many sizes near the transition.</p></div>
  <div class="meaning-panel"><img src="images/normal_retinal_vasculature.jpg" alt="Normal retinal blood vessels branching from the optic disc"><strong>Retinal vasculature</strong><p>A nested physiological network distributes blood across the retinal surface.</p></div>
  <div class="meaning-panel"><img src="images/rock_fracture_surface.jpg" alt="Measured three-dimensional morphology of a rock fracture surface"><strong>Rough fracture surface</strong><p>Material heterogeneity and fracture propagation create structure across a finite range of scales.</p></div>
  <div class="meaning-panel"><img src="images/snowflake_sublimation_reversed.gif" alt="Snow-crystal growth"><strong>Crystal growth</strong><p>Local attachment and environmental conditions amplify branching instabilities.</p></div>
  <div class="meaning-panel"><img src="images/leaf_venation.png" alt="Multiscale venation in a leaf"><strong>Distribution networks</strong><p>Nested pathways distribute material while remaining robust to local damage.</p></div>
</div>

Fractal descriptions appear in growth, transport networks, rough materials, physiological branching, and critical phenomena. In each case, local events accumulate into a system-level structure that was not specified component by component.

Fractal geometry asks a common question across these systems: **how does measured structure change with scale?** Their mechanisms differ, and empirical scaling usually holds only approximately over a finite range.

<div class="figure-caption">Critical percolation: generated site-percolation realisation near \(p_c\approx0.5927\). Retina: National Eye Institute, National Institutes of Health, public domain. Rock fracture surface: Feng et al. (2014), CC BY 4.0.</div>
""", "common-language", tags=("slides",), slide_type="subslide"),

        md(r"""
## Description is not explanation

<div class="analysis-perspectives">
  <div><strong>Fractal geometry contributes</strong><p>measurements, models, and representations for multiscale structures that one Euclidean length, area, or smooth surface cannot adequately summarise.</p></div>
  <div><strong>Complex Systems contributes</strong><p>mechanisms: interactions, feedback, constraints, stochasticity, growth, and collective dynamics that may generate the observed scaling.</p></div>
</div>

An estimated dimension gives diverse phenomena a common descriptive language. It does not prove that they share the same mechanism.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>If two systems have the same estimated dimension, what have we learned, and what remains unknown?</span></div>
""", "why_complex_systems", tags=("slides",), slide_type="subslide"),

        md(r"""
## Complex system signatures in fractals

An empirical fractal-like pattern may display some of these signatures, not necessarily all of them:

<div class="model-specification wide-description-table">
  <div><strong>Interacting components</strong><span>earlier components alter what later ones encounter</span></div>
  <div><strong>Local rules</strong><span>attachment, growth, erosion, transport, or activation uses nearby information</span></div>
  <div><strong>Feedback and history</strong><span>existing structure redirects later change</span></div>
  <div><strong>Emergence</strong><span>global branching and scaling are not prescribed piece by piece</span></div>
  <div><strong>Stochasticity</strong><span>realisations vary while ensemble geometry remains similar</span></div>
  <div><strong>Organisation across scales</strong><span>local events accumulate across a range of lengths</span></div>
</div>

Fractality is not an additional item on this list. It can be a measurable system-level consequence of these processes.
""", "complex_system_signatures", tags=("slides",), slide_type="subslide"),

        md(r"""
## Are all fractals complex systems?

<div class="analysis-perspectives">
  <div><strong>No</strong><p>The Cantor set or Sierpiński triangle can be generated by one externally prescribed recursive rule. They are fractals, but they need not contain many interacting components or emergent collective behaviour.</p></div>
  <div><strong>Sometimes</strong><p>A percolation cluster, branching colony, river network, or critical domain can be a fractal-like outcome of interacting components and feedback.</p></div>
</div>

Likewise, many complex systems are not usefully fractal.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="34" height="34"><span>A fractal pattern is evidence of multiscale organisation, not automatic evidence of a particular complex system mechanism.</span></div>
""", "not-all-fractals", tags=("slides",), slide_type="subslide"),

        md(r"""
# Three roles for three kinds of example

<div class="model-specification">
  <div><strong>Exact calibration</strong><span>Cantor set and Sierpiński triangle: known generator, exact self-similarity, analytic dimension</span></div>
  <div><strong>Generative Complex Systems model</strong><span>branching growth: repeated local development produces an organised multiscale form</span></div>
  <div><strong>Empirical comparison</strong><span>coastlines, branching tissues, rivers, and other finite noisy forms measured across a justified scaling range</span></div>
</div>

The exact constructions teach us what the measurement means. Branching connects a local growth process to multiscale form. Empirical systems test how far the language transfers.
""", "three-fractal-roles", tags=("slides",), slide_type="slide"),

        md(r"""
# Diffusion-limited aggregation
## Our canonical Complex Systems model

<div class="slide-columns">
  <img class="column-image" src="images/particularly_stuck_image1.png" alt="A branching diffusion-limited aggregate">
  <div>
    <p><strong>Initialise:</strong> place one occupied seed.</p>
    <p><strong>Diffuse:</strong> release a particle and let it take random local steps.</p>
    <p><strong>Attach:</strong> when it touches the aggregate, it sticks permanently.</p>
    <p><strong>Repeat:</strong> the aggregate becomes the environment encountered by later particles.</p>
  </div>
</div>

The rule does not prescribe branches, gaps, screening, or a fractal dimension.

<div class="figure-caption">Image adapted from Schöneberger and Brockmann, <a href="https://www.complexity-explorables.org/explorables/particularly-stuck/">“Particularly Stuck”</a>, Complexity Explorables, CC BY 2.0 DE.</div>
""", "dla-model", tags=("slides",), slide_type="subslide"),

        md(r"""
## From random walks to collective geometry

<div class="analysis-perspectives">
  <div><strong>Local process</strong><p>Each mobile particle follows a stochastic trajectory and reacts only when it encounters the existing aggregate.</p></div>
  <div><strong>Collective outcome</strong><p>Exposed tips intercept walkers and grow, while screened interior regions receive fewer particles. Branching amplifies itself.</p></div>
</div>

The aggregate stores the history of every previous attachment. Later particles therefore move independently, but not in an unchanged environment.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down:</strong> one random step and one attachment. <strong>Up:</strong> screening, branching morphology, mass-radius scaling, and estimated dimension.</span></div>
""", "dla-emergence", tags=("slides",), slide_type="subslide"),

        md(r"""
# Explore Diffusion-limited aggregation
## Particularly Stuck

<iframe
  width="960"
  height="500"
  src="https://www.complexity-explorables.org/explorables/particularly-stuck/#particularly_stuck_container"
  title="Particularly Stuck diffusion-limited aggregation explorable"
  frameborder="0"
  loading="lazy"
  style="display:block;max-width:100%;margin:0 auto">
</iframe>

<div class="figure-caption">Interactive by Janina Schöneberger and Dirk Brockmann, Complexity Explorables, CC BY 2.0 DE.</div>
""", "dla-explorable-slides", tags=("slides-only",), slide_type="slide"),

        md(r"""
## Why do the particles appear to fall inward?

<div class="analysis-perspectives">
  <div><strong>Standard idealisation</strong><p>In textbook Diffusion-limited aggregation, each step is unbiased. There is no attractive force towards the seed.</p></div>
  <div><strong>This explorable</strong><p>Particles are injected around the periphery, and the authors add adjustable inward drift and rotational drift so growth becomes visible sooner.</p></div>
</div>

Even without explicit attraction, an absorbing central aggregate creates a net inward flux: trajectories that reach it disappear from the mobile population. That population-level flux is not the same as an inward bias in each random step.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="34" height="34"><span>Set attraction and twist to zero to approach unbiased diffusion. Increasing either parameter changes the model as well as the speed of the demonstration.</span></div>
""", "dla-drift-explanation", tags=("slides",), slide_type="subslide"),

        md(r"""
## Particularly Stuck: interactive Diffusion-limited aggregation

Use the [Particularly Stuck explorable](https://www.complexity-explorables.org/explorables/particularly-stuck/) by Janina Schöneberger and Dirk Brockmann.

<iframe
  width="960"
  height="620"
  src="https://www.complexity-explorables.org/explorables/particularly-stuck/#particularly_stuck_container"
  title="Particularly Stuck diffusion-limited aggregation explorable"
  frameborder="0"
  loading="lazy"
  style="display:block;max-width:100%;margin:0 auto">
</iframe>

The explorable is Diffusion-limited aggregation-inspired rather than a display of strictly unbiased Brownian aggregation. Its description states that pure diffusion takes a long time to collide with the central nucleus, so weak attraction towards the centre and a rotational drift were added. The controls expose those additions:

- **attraction** adds inward radial drift;
- **twist** adds rotational drift;
- **twist mix** changes the balance of clockwise and anticlockwise motion;
- **wiggle** controls the stochastic component;
- **speed** accelerates the visualisation.

This creates a valuable modelling discussion. A visualisation may alter the process to make an outcome observable within classroom time. Those alterations must be identified because they can change the resulting morphology.

In unbiased Diffusion-limited aggregation, individual increments have zero mean. Nevertheless, releasing particles on an outer boundary and absorbing them at a central aggregate establishes a concentration gradient and a net diffusive flux towards the aggregate. In addition, the paths we notice attaching are a selected subset of all random walks. Neither effect means that an individual particle is deterministically pulled inward.

The original kinetic aggregation model is T. A. Witten and L. M. Sander, [“Diffusion-Limited Aggregation, a Kinetic Critical Phenomenon”](https://doi.org/10.1103/PhysRevLett.47.1400), *Physical Review Letters* 47 (1981).
""", "dla-explorable-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Another route to fractal-like growth

Material arrives from outside the growing structure.

<div class="compact-card-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:.55rem;align-items:stretch">
  <div class="meaning-panel" style="display:grid;grid-template-rows:160px 2.6rem 1fr;text-align:left"><img src="images/particularly_stuck_image1.png" alt="A simulated diffusion-limited aggregate" style="display:block;width:100%;height:160px;object-fit:contain;margin:0"><strong style="align-self:center">Diffusion-limited aggregation</strong><p style="margin:0">Randomly transported particles attach irreversibly. Exposed regions intercept more arrivals and screen the interior.</p></div>
  <div class="meaning-panel" style="display:grid;grid-template-rows:160px 2.6rem 1fr;text-align:left"><img src="images/copper_electrodeposition_dendrite.png" alt="Dendritic copper formed by electrodeposition" style="display:block;width:100%;height:160px;object-fit:contain;margin:0"><strong style="align-self:center">Electrodeposition</strong><p style="margin:0">Ions travel through solution and deposit preferentially at exposed tips.</p></div>
  <div class="meaning-panel" style="display:grid;grid-template-rows:160px 2.6rem 1fr;text-align:left"><div style="display:grid;grid-template-columns:1fr 1fr;gap:.2rem;height:160px;overflow:hidden"><img src="images/beijing_1978_landsat.jpg" alt="Beijing observed by Landsat in 1978" style="display:block;width:100%;height:160px;object-fit:cover;margin:0"><img src="images/beijing_2011_landsat.jpg" alt="Beijing observed by Landsat in 2011" style="display:block;width:100%;height:160px;object-fit:cover;margin:0"></div><strong style="align-self:center">Urban growth</strong><p style="margin:0">Many constrained decisions produce irregular advancing boundaries and corridors.</p></div>
</div>

Unlike developmental branching, mass arrives from outside. Similar morphology suggests a comparison, not a shared mechanism. We return to this model after Brownian motion and agent-based modelling.

<div class="figure-caption">Copper electrodeposition image via Wikimedia Commons, CC BY-SA 4.0. Beijing: NASA Earth Observatory images by Robert Simmon using Landsat 3 and 5 data from the USGS Global Visualization Viewer, 1978 and 2011.</div>
""", "dla-natural-comparison", tags=("slides",), slide_type="slide"),

        md(r"""
# Our generative model · A local branching rule

<img src="images/fractal_weeds_public_domain.jpg" alt="Four fractal-like weeds generated from different repeated branching rules" style="display:block;width:62%;max-height:340px;object-fit:contain;margin:0 auto">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>How does nature generate all these different forms of wheat?</span></div>

<div class="figure-caption">Fractal-like weeds generated using an iterated branching system, Solkoll, Wikimedia Commons, public domain.</div>
""", "branching-contrast", tags=("slides",), slide_type="slide"),

        md(r"""
# Branching from a local grammar
## Weeds & Trees

A root branch of length $L_0$ carries three shorter branches with lengths $l_i$ and angles $\theta_i$. Every open tip is then treated as a new root and receives a smaller copy of the branching structure.

<div class="model-specification">
  <div><strong>State</strong><span>the current collection of branches and open tips</span></div>
  <div><strong>Local update</strong><span>replace each open tip by a scaled branching motif</span></div>
  <div><strong>Parameters</strong><span>relative lengths, angles, width taper, iteration depth, and noise</span></div>
  <div><strong>Outcome</strong><span>a self-similar or statistically self-similar branching form</span></div>
</div>

The explorable stops after eight iterations. Infinite detail belongs to the idealised rule, not the finite visualisation.

A deterministic grammar can define an exact limiting fractal only when fixed replacement and scaling rules continue indefinitely. The displayed tree is a finite approximation. A biological tree is finite, variable, and shaped by its environment.
""", "branching-model", tags=("slides",), slide_type="subslide"),

        md(r"""
# Explore branching
## Weeds & Trees

<iframe
  width="960"
  height="500"
  src="https://www.complexity-explorables.org/explorables/weeds-and-trees/#cxpbox_weeds-and-trees_display"
  title="Weeds and Trees branching growth explorable"
  frameborder="0"
  loading="lazy"
  style="display:block;max-width:100%;margin:0 auto">
</iframe>

<div class="figure-caption">Interactive by Dirk Brockmann, Complexity Explorables, CC BY 2.0 DE.</div>
""", "branching-explorable-slides", tags=("slides-only",), slide_type="slide"),

        md(r"""
# Same form, different systems

<div class="compact-card-grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:.45rem;align-items:stretch">
  <div class="meaning-panel"><img src="images/Fern.png" alt="A fern with repeated branching" style="width:100%;height:155px;object-fit:contain"><strong>Fern</strong><p>Development from active tips.</p></div>
  <div class="meaning-panel"><img src="images/lightning_branches.jpg" alt="Branching lightning channels" style="width:100%;height:155px;object-fit:cover"><strong>Lightning</strong><p>Propagation through an electric field.</p></div>
  <div class="meaning-panel"><img src="images/mississippi_delta_branching.jpg" alt="Satellite image of the Mississippi River Delta" style="width:100%;height:155px;object-fit:cover"><strong>River delta</strong><p>Flow, deposition, and changing channels.</p></div>
  <div class="meaning-panel"><img src="images/All_roads_lead_to_rome.webp" alt="Routes from across Europe converging on Rome" style="width:100%;height:155px;object-fit:cover"><strong>Road network</strong><p>Human decisions constrained by geography, cost, and shared destinations.</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Why does branching recur in biological, physical, geological, and human systems operating at very different scales?</span></div>

Branching can distribute or collect material and connect many local sites to larger pathways. Similar form does not imply identical mechanism.

<div class="figure-caption">Image sources: Brad Caldwell, <a href="https://commons.wikimedia.org/wiki/File:Lightning_over_Oradea_Romania_3.jpg">lightning photograph</a>, Wikimedia Commons, CC0; NASA/METI/AIST/Japan Space Systems and the U.S./Japan ASTER Science Team, Mississippi River Delta satellite image, public domain; Roads to Rome visualisation derived from OpenStreetMap data and GraphHopper routing.</div>
""", "branching-natural-comparison", tags=("slides",), slide_type="subslide"),

        md(r"""
## Weeds & Trees: model and mechanism

<div class="reader-explorable">
<iframe
  src="https://www.complexity-explorables.org/explorables/weeds-and-trees/#cxpbox_weeds-and-trees_display"
  title="Weeds and Trees branching growth explorable"
  loading="lazy"
  style="display:block;width:100%;height:680px;border:1px solid #C7CEDC;margin:.6rem auto 1rem">
</iframe>
</div>

If the embedded controls do not load in your browser, [open Weeds & Trees in a new tab](https://www.complexity-explorables.org/explorables/weeds-and-trees/).

The explorable by Dirk Brockmann begins with a root branch, attaches three shorter branches with adjustable lengths and angles, and repeatedly replaces every open tip by a smaller copy of that structure. Angle and length noise perturb the repeated motif, while width taper makes the output appear more tree-like.

This makes the distinction between a geometric growth rule and a biological mechanism especially clear. A real plant does not simply execute a geometric replacement rule. Branching is regulated by growth at meristems, gene expression, hormones, resource transport, mechanics, competition for light, and environmental history. The simplified rule captures architecture produced by repeated local development without representing all of those causal processes.

Why might nature reuse a local rule at all? Growing organisms cannot position every final branch from a completed global blueprint. Local developmental signals can be reused at many tips, respond to nearby resources and damage, and build a large adaptive structure from limited instructions. Evolution need not optimise for “being fractal”; multiscale branching can arise because repeated local growth efficiently distributes or collects material across space.

The river delta is a different case. Its branching geometry is generated by flow and sediment transport rather than a developmental rule. Similar geometry supports comparison, but not mechanistic equivalence.
""", "branching-explorable-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# A different geometric language

<div class="reader-voice">
  <div class="reader-voice-quote">Nature exhibits not simply a higher degree but an altogether different level of complexity.</div>
  <div class="reader-voice-attr">Benoit Mandelbrot, <em>The Fractal Geometry of Nature</em> (1982)</div>
</div>

The claim is not that nature is merely more intricate than a circle or polygon. It is that Euclidean ideas such as one characteristic length, smoothness under magnification, and integer dimension can fail to describe how structure is distributed across scales.
""", "mandelbrot-quote", tags=("slides",), slide_type="slide"),

        md(r"""
# Exact fractals

<div class="analysis-perspectives" style="align-items:stretch">
  <div style="display:flex;flex-direction:column">
    <strong>Cantor set</strong>
    <img src="images/cantor_iterations_clean.svg" alt="The first four iterations of the Cantor set" style="width:100%;height:210px;object-fit:contain;margin-top:.45rem">
    <p>Keep two copies, each scaled by one third.</p>
  </div>
  <div style="display:flex;flex-direction:column">
    <strong>Sierpiński triangle</strong>
    <img src="images/Sierpinski_triangle_iterations.png" alt="The first iterations of the Sierpiński triangle" style="width:100%;height:210px;object-fit:contain;margin-top:.45rem">
    <p>Keep three copies, each scaled by one half.</p>
  </div>
</div>

These are not themselves complex systems. Their exact rules let us isolate ideas that empirical and emergent patterns express only approximately.
""", "canonical-constructions", tags=("slides",), slide_type="slide"),

        md(r"""
# Infinite detail changes what “size” means

<div class="analysis-perspectives">
  <div><strong>Cantor set</strong><p>It lies on a line and contains uncountably many points, yet its total length is zero.</p></div>
  <div><strong>Sierpiński triangle</strong><p>Its area tends to zero while its boundary length diverges.</p></div>
</div>

Count, length, area, boundary, and scaling dimension measure different geometric features. Calling these objects a collection of points, a curve, or a region hides the behaviour we want to compare.

**Dimension is exactly the property we need:** it records how the amount of visible structure grows as resolution increases. We will first reconstruct that scaling meaning for ordinary Euclidean objects, then allow its exponent to be non-integer for a fractal.

""", "why-dimension", tags=("slides",), slide_type="slide"),

        md(r"""
# Cantor set

<img src="images/cantor_iterations_clean.svg" alt="The first four iterations of the middle-thirds Cantor construction" style="display:block;max-height:250px;width:auto;max-width:100%;margin:0 auto .8rem">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>What could “size” mean for this set? Compare count, total length, the length of one piece, and how much detail appears under magnification. Which answers the question you care about?</span></div>

<div class="qa-grid fragment">
  <div class="qa-row"><p class="qa-question">Number</p><p class="qa-answer">Nₖ = 2ᵏ intervals</p></div>
  <div class="qa-row"><p class="qa-question">Length of each</p><p class="qa-answer">ℓₖ = 3⁻ᵏ</p></div>
  <div class="qa-row"><p class="qa-question">Total length</p><p class="qa-answer">Lₖ = Nₖℓₖ = (2/3)ᵏ → 0</p></div>
</div>

""", "cantor-construction", tags=("slides",), slide_type="slide"),

        md(r"""
The standard middle-thirds Cantor set begins with $C_0=[0,1]$. At every step, remove the open middle third of every surviving interval. The limiting set is

$$C=\bigcap_{k=0}^{\infty} C_k.$$

At depth $k$, there are $2^k$ intervals of length $3^{-k}$. Their total length is $(2/3)^k$, which tends to zero. The remaining set is still uncountable: points in $C$ can be represented by ternary expansions containing only the digits 0 and 2, giving a correspondence with infinite binary sequences.

This combination is one reason early fractals were called mathematical monsters. Cardinality, measure, topology, and scaling dimension describe different aspects of size.
""", "cantor-detail-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Sierpiński triangle

<img src="images/Sierpinski_triangle_iterations.png" alt="The first iterations of the Sierpiński triangle construction" style="display:block;max-height:230px;width:auto;max-width:100%;margin:0 auto">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>At depth k, how many triangles remain? What fraction of area survives?</span></div>

Let $A_0$ be the area of the initial filled triangle and $A_k$ the total area of all triangles retained after $k$ removals. The ratio $A_k/A_0$ removes the arbitrary size of the starting triangle.

<div class="qa-grid fragment">
  <div class="qa-row"><p class="qa-question">Number</p><p class="qa-answer">Nₖ = 3ᵏ triangles</p></div>
  <div class="qa-row"><p class="qa-question">Side length</p><p class="qa-answer">ℓₖ = 2⁻ᵏ</p></div>
  <div class="qa-row"><p class="qa-question">Retained area</p><p class="qa-answer">Aₖ/A₀ = (3/4)ᵏ → 0</p></div>
</div>

""", "sierpinski-construction", tags=("slides",), slide_type="slide"),

        md(r"""
If every boundary of every remaining triangle is counted, the total boundary length at depth $k$ is proportional to

$$3^k 2^{-k}=\left(\frac{3}{2}\right)^k,$$

which diverges. Meanwhile the total area tends to zero. This is not a contradiction. Length and area measure different geometric features.

The apparent shape changes less with each iteration when viewed at fixed resolution. Mathematically, however, each iteration adds new structure at a smaller scale.
""", "sierpinski-detail-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Similarity dimension from self-similarity

For an exact self-similar fractal, the **similarity dimension** keeps the Euclidean scaling rule but no longer assumes an integer exponent:

$$N=r^{-D}$$

so

$$D=\frac{\log N}{\log(1/r)}.$$

Here $N$ is the number of self-similar copies and $r$ is the linear scale of each copy relative to the whole. Both remain meaningful beyond these exact examples: we can count visible pieces and state the resolution at which we observed them.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up the ladder:</strong> replace an infinite construction with one scaling exponent.</span></div>
""", "similarity-dimension", tags=("slides",), slide_type="slide"),

        md(r"""
## Cantor set dimension

Two copies remain, each scaled by one third:

$$D_C=\frac{\log 2}{\log 3}\approx0.631.$$

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>If magnification triples, a line reveals three times as many pieces. The Cantor set reveals only two. Where should its scaling exponent sit?</span></div>

It grows in visible detail faster than isolated points, but more slowly than a complete line: $0\lt D_C\lt 1$.
""", "cantor-dimension", tags=("slides",), slide_type="subslide"),

        md(r"""
## Sierpiński triangle dimension

Three copies remain, each scaled by one half:

$$D_S=\frac{\log 3}{\log 2}\approx1.585.$$

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>If magnification doubles, a curve reveals two times as much detail and a filled region reveals four. The triangle reveals three. Where should its exponent sit?</span></div>

It grows in visible detail faster than a curve, but more slowly than a filled region: $1\lt D_S\lt 2$.
""", "sierpinski-dimension", tags=("slides",), slide_type="subslide"),

        md(r"""
The similarity-dimension calculation assumes exact self-similarity, non-overlapping copies, and a common contraction ratio. More general constructions require more general definitions. Similarity dimension is therefore a model-specific route into fractal dimension, not a universal recipe for every dataset.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="34" height="34"><span>Choose a dimension definition suited to the object and question</span></div>
""", "dimension-caveat-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Three descriptions of an exact fractal

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;align-items:stretch">
  <div class="meaning-panel"><strong>1. Replacement</strong><p>Replace one piece with smaller pieces.</p><p><strong>Next:</strong> 1A Cantor set and 1B Sierpiński triangle.</p></div>
  <div class="meaning-panel"><strong>2. Iterated function system</strong><p>Shrink and reposition points or sets using contraction maps.</p><p><strong>Next:</strong> 2A Cantor IFS, 2B Sierpiński IFS, then the chaos game as random iteration of that IFS.</p></div>
  <div class="meaning-panel"><strong>3. L-system</strong><p>Rewrite symbols, then interpret the resulting word geometrically.</p><p><strong>Next:</strong> Cantor and Sierpiński symbolic constructions.</p></div>
</div>

For Cantor and Sierpiński these are alternative mathematical encodings. A causal interpretation must be justified separately.
""", "multiple-descriptions", tags=("slides",), slide_type="slide"),

        md(r"""
## 1A. Cantor set · initiator and generator

<div class="slide-columns">
  <img class="column-image" src="images/Cantor_initiator_generator.png" alt="Cantor set initiator and generator">
  <div>
    <p><strong>Initiator:</strong> the starting object.</p>
    <p><strong>Generator:</strong> the replacement rule applied at every scale.</p>
  </div>
</div>
""", "initiator-generator-cantor", tags=("slides",), slide_type="subslide"),

        md(r"""
## 1B. Sierpiński triangle · initiator and generator

<div class="slide-columns">
  <img class="column-image" src="images/Sierpinski_initiator_generator.png" alt="Sierpiński triangle initiator and generator">
  <div>
    <p><strong>Initiator:</strong> one filled triangle.</p>
    <p><strong>Generator:</strong> replace it with three half-scale corner triangles.</p>
  </div>
</div>
""", "initiator-generator-sierpinski", tags=("slides",), slide_type="subslide"),

        md(r"""
## 2A. Cantor set · iterated function system

For the Cantor set, apply both contractions to the current set:

$$f_0(x)=\frac{x}{3},\qquad f_1(x)=\frac{x}{3}+\frac{2}{3}.$$

$$C_{k+1}=f_0(C_k)\cup f_1(C_k).$$

The Cantor set is the invariant set approached under repeated application.
""", "cantor-ifs", tags=("slides",), slide_type="subslide"),

        md(r"""
## 2. Why does an IFS converge?

Each map is a contraction: it brings points closer together by a fixed factor smaller than one.

<div class="qa-grid">
  <div class="qa-row"><p class="qa-question">Point dynamics</p><p class="qa-answer">repeated contraction forgets the initial separation</p></div>
  <div class="qa-row"><p class="qa-question">Set dynamics</p><p class="qa-answer">the union of contracted copies approaches an invariant set</p></div>
  <div class="qa-row"><p class="qa-question">Fixed set</p><p class="qa-answer">the attractor $K$ satisfies $\mathcal F(K)=K$</p></div>
</div>

If the contractions are $f_1,\ldots,f_N$, define the set-map

$$\mathcal F(A)=\bigcup_{i=1}^{N}f_i(A).$$

Repeatedly applying $\mathcal F$ to a non-empty compact starting set approaches the unique compact attractor $K$. For the Cantor construction, that attractor is $C$, so $\mathcal F(C)=C$.
""", "ifs-convergence", tags=("slides",), slide_type="subslide"),

        md(r"""
## 2B. Sierpiński triangle · iterated function system

<div class="slide-columns" style="grid-template-columns:.82fr 1.18fr;align-items:center">
  <div>
    <p>Let $P_1,P_2,P_3$ be the vertices of the initial triangle. Define</p>

$$f_i(x)=\frac{1}{2}x+\frac{1}{2}P_i,\qquad i=1,2,3.$$

    <p>Each map contracts towards one vertex. Their union produces the three half-scale copies.</p>
  </div>
  <img src="images/Sierpinski_IFS.gif" alt="Repeated contraction maps generating the Sierpiński triangle" style="display:block;width:100%;max-height:350px;object-fit:contain">
</div>
""", "sierpinski-ifs", tags=("slides",), slide_type="subslide"),

        md(r"""
## 2C. Sierpiński triangle · chaos game

The chaos game is a **random iteration algorithm for the same IFS**, not a fourth description.

<div class="slide-columns" style="grid-template-columns:.9fr 1.1fr;align-items:center">
  <div>
    <p>Instead of applying all three maps to a set, repeatedly choose one map at random and apply it to a single point.</p>
    <div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Where does the structure come from if the choices are random?</span></div>
    <p>The randomness selects a path. The contraction maps constrain the possible long-run geometry.</p>
  </div>
  <img class="column-image" src="images/sierpinski_chaos_game_clean.gif" alt="Chaos game points progressively revealing the Sierpiński triangle" style="max-height:410px;object-fit:contain">
</div>
""", "chaos-game", tags=("slides",), slide_type="subslide"),

        md(r"""
The random iteration algorithm is:

1. choose any initial point;
2. select one contraction map $f_i$;
3. replace the point by $f_i(x)$;
4. record it after a short burn-in;
5. repeat.

Under standard contractivity conditions, the sampled points approach the same attractor defined by the full IFS. The seed, probabilities, burn-in, and number of sampled points are computational choices. They affect the finite picture, not the mathematical attractor defined by the maps.
""", "chaos-game-reader", tags=("reader-only",), slide_type="skip"),

        code(r'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def chaos_game(n_points=6_000, seed=3024):
    """Generate points by repeatedly choosing a random contraction."""
    vertices = np.array([[0.5, np.sqrt(3) / 2], [0.0, 0.0], [1.0, 0.0]])
    rng = np.random.default_rng(seed)
    points = np.empty((n_points, 2))
    points[0] = (0.47, 0.41)
    for step, vertex in enumerate(rng.integers(0, 3, n_points - 1), start=1):
        points[step] = 0.5 * (points[step - 1] + vertices[vertex])
    return points

points = chaos_game()
frame_ends = np.unique(np.geomspace(20, len(points), 45).astype(int))
fig, ax = plt.subplots(figsize=(6.4, 5.2))
scatter = ax.scatter([], [], s=2, color="#172b54")
ax.set(xlim=(-0.03, 1.03), ylim=(-0.03, 0.91), aspect="equal")
ax.axis("off")

def update(frame_end):
    scatter.set_offsets(points[20:frame_end])  # discard a short burn-in
    ax.set_title(f"{frame_end:,} random contractions")
    return (scatter,)

animation = FuncAnimation(fig, update, frames=frame_ends, interval=140, blit=True)
animation.save("sierpinski_chaos_game.gif", writer=PillowWriter(fps=7))
plt.close(fig)
''', "chaos-game-code-reader", tags=("reader-only", "hide-input", "hide-output"), slide_type="skip"),

        md(r"""
## 3. L-systems: symbols first, geometry second

An L-system rewrites a word in parallel. We specify

$$G=(V,\omega,P),$$

where $V$ is the alphabet, $\omega$ is the axiom or initial word, and $P$ is the set of production rules. Every symbol in the current word is replaced simultaneously.

The word has no geometric length by itself. A separate turtle interpretation assigns actions to symbols, a turning angle, and a step length. If the step length is fixed, the drawing grows with each rewrite. To compare successive approximations inside the same frame, we shorten the step at generation $k$.
""", "l-system-definition", tags=("slides",), slide_type="slide"),

        md(r"""
## 3A. Cantor set · L-system

This rule produces the **standard middle-thirds Cantor set**. Other Cantor-like sets use different contraction ratios or removal rules.

<div class="slide-columns lsystem-layout">
  <div class="lsystem-specification">
    <p><strong>Alphabet:</strong> <code>V = {A, B}</code></p>
    <p><strong>Meaning:</strong> <code>A</code> draws; <code>B</code> moves without drawing</p>
    <p><strong>Initial word:</strong> <code>ω = A</code></p>
    <p><strong>Productions:</strong> <code>A → ABA</code>, <code>B → BBB</code></p>
    <p><strong>Step length:</strong> 3<sup>−<em>k</em></sup> of the initial length at generation <em>k</em></p>
  </div>
  <div>
    <img src="images/cantor_iterations_clean.svg" alt="Successive Cantor set iterations labelled by depth" style="display:block;width:100%;max-height:285px;object-fit:contain">
    <p class="compact-equation">Finite words describe <em>C</em><sub><em>k</em></sub>; the limit is <em>C</em> = ⋂<sub><em>k</em>=0</sub><sup>∞</sup> <em>C</em><sub><em>k</em></sub>.</p>
  </div>
</div>
""", "cantor-l-system", tags=("slides",), slide_type="subslide"),

        md(r"""
## 3B. Sierpiński triangle · L-system

<div class="slide-columns lsystem-layout">
  <div class="lsystem-specification">
    <p><strong>Alphabet:</strong> <code>V = {F, G, +, −}</code></p>
    <p><strong>Meaning:</strong> <code>F,G</code> draw; <code>+</code> turns left; <code>−</code> turns right</p>
    <p><strong>Initial word:</strong> <code>ω = F</code></p>
    <p><strong>Productions:</strong> <code>F → G−F−G</code>, <code>G → F+G+F</code></p>
    <p><strong>Geometry:</strong> turn 60°; step length 2<sup>−<em>k</em></sup> at generation <em>k</em></p>
  </div>
  <img src="images/sierpinski_lsystem_iterations.svg" alt="Successive iterations through depth six of the Sierpiński arrowhead L-system" style="display:block;width:100%;max-height:310px;object-fit:contain">
</div>
""", "l-systems", tags=("slides",), slide_type="subslide"),

        md(r"""
The Sierpiński arrowhead curve uses symbols for forward motion and turns. Its finite curves differ from the filled-triangle approximations, but both approach the Sierpiński triangle.

L-systems suit descriptions built from repeated local instructions, such as branching plant forms. IFS descriptions instead emphasise contraction maps. We choose the representation that makes the relevant construction or mechanism easiest to inspect.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>How could the branching rule in Weeds &amp; Trees be written as an L-system? Propose an alphabet, an initial word, production rules, and a turtle meaning for drawing, turning, and branching.</span></div>

For the relationship between the Sierpiński triangle and arrowhead constructions, see Martínez-Cruz et al. (2024), [“Some Insights into the Sierpiński Triangle Paradox”](https://doi.org/10.3390/fractalfract8110655), *Fractal and Fractional* 8, 655.

Lindenmayer introduced parallel rewriting to model filamentous development. Turtle graphics later supplied a standard geometric interpretation: A. Lindenmayer (1968), [“Mathematical models for cellular interactions in development I”](https://doi.org/10.1016/0022-5193(68)90079-9), *Journal of Theoretical Biology* 18; P. Prusinkiewicz (1986), [“Graphical applications of L-systems”](https://algorithmicbotany.org/papers/graphical.gi86.pdf).

For interactive exploration, see [Hokus Fractus](https://www.complexity-explorables.org/explorables/hokus-fractus/) from Complexity Explorables.
""", "l-systems-reader", tags=("reader-only",), slide_type="skip"),

        code(r'''
import numpy as np
import matplotlib.pyplot as plt

RULES = {"F": "G-F-G", "G": "F+G+F"}

def rewrite_lsystem(word, iterations):
    """Return every symbolic iteration, including the axiom."""
    history = [word]
    for _ in range(iterations):
        word = "".join(RULES.get(symbol, symbol) for symbol in word)
        history.append(word)
    return history

def turtle_points(word, turn_degrees=60):
    """Interpret F/G as forward moves and +/- as turns."""
    position = np.array([0.0, 0.0])
    heading = 0.0
    points = [position.copy()]
    for symbol in word:
        if symbol in {"F", "G"}:
            direction = np.array([np.cos(np.deg2rad(heading)),
                                  np.sin(np.deg2rad(heading))])
            position = position + direction
            points.append(position.copy())
        elif symbol == "+":
            heading += turn_degrees
        elif symbol == "-":
            heading -= turn_degrees
    return np.asarray(points)

history = rewrite_lsystem("F", iterations=5)
fig, axes = plt.subplots(2, 3, figsize=(11, 6))
for depth, (word, ax) in enumerate(zip(history, axes.flat)):
    points = turtle_points(word)
    baseline = points[-1] - points[0]
    angle = np.arctan2(baseline[1], baseline[0])
    rotation = np.array([[np.cos(angle), -np.sin(angle)],
                         [np.sin(angle),  np.cos(angle)]])
    points = (points - points[0]) @ rotation
    if points[:, 1].mean() < 0:
        points[:, 1] *= -1
    ax.plot(points[:, 0], points[:, 1], color="#172b54", linewidth=1.5)
    ax.set_title(f"k = {depth}")
    ax.set_aspect("equal")
    ax.axis("off")
plt.tight_layout()
''', "l-systems-code-reader", tags=("reader-only", "hide-input", "hide-output"), slide_type="skip"),

        md(r"""
# Level 1: what the mathematics does
## Three descriptions of an exact fractal

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;align-items:stretch">
  <div class="meaning-panel"><strong>1. Replacement</strong><p>Replace one geometric piece with several smaller pieces.</p><p><strong>Provides:</strong> a transparent construction and direct copy-counting.</p></div>
  <div class="meaning-panel"><strong>2. Contraction maps</strong><p>Apply maps that shrink and reposition points or sets.</p><p><strong>Provides:</strong> an invariant set and a dynamical-systems description.</p></div>
  <div class="meaning-panel"><strong>3. Symbolic grammar</strong><p>Rewrite symbols, then interpret the resulting word geometrically.</p><p><strong>Provides:</strong> local instructions and an explicit construction history.</p></div>
</div>

<p><strong>For Cantor and Sierpiński:</strong> these are alternative encodings of controlled mathematical objects. They expose different features of the same exact geometry.</p>
""", "representations-compared", tags=("slides",), slide_type="slide"),

        md(r"""
# Level 2: what process might it represent?
## A geometric encoding is not automatically a mechanism

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;align-items:stretch">
  <div class="meaning-panel"><strong>Replacement</strong><p><strong>Mathematical action:</strong> delete or replace pieces.</p><p><strong>Possible process:</strong> repeated fragmentation, pruning, exclusion, or survival.</p></div>
  <div class="meaning-panel"><strong>Contraction maps</strong><p><strong>Mathematical action:</strong> shrink and relocate copies.</p><p><strong>Possible role:</strong> compactly describe an attractor. Nature need not perform affine contractions.</p></div>
  <div class="meaning-panel"><strong>Symbolic grammar</strong><p><strong>Mathematical action:</strong> rewrite local symbols.</p><p><strong>Possible process:</strong> repeated developmental instructions, branching, or cell-state updates.</p></div>
</div>

<p><strong>Shared idea:</strong> repeated local operations can organise structure across scales. The causal interpretation must be justified separately.</p>
""", "representations-processes", tags=("slides",), slide_type="subslide"),

        md(r"""
## Controlled geometry vs stochastic iteration

<div class="analysis-perspectives" style="align-items:stretch">
  <div><img src="images/Sierpinski_triangle_iterations.png" alt="Controlled removal construction of a Sierpiński triangle" style="width:100%;height:220px;object-fit:contain"><strong>Controlled model</strong><p>Cantor and Sierpiński let us isolate infinite iteration, scaling and dimension exactly. The removed middle is a mathematical construction, not necessarily a literal history.</p></div>
  <div><img src="images/sierpinski_chaos_game_clean.gif" alt="Sierpiński pattern emerging in the chaos game" style="width:100%;height:220px;object-fit:contain"><strong>Stochastic iteration</strong><p>One point follows randomly selected contraction maps. This is a dynamical construction, not an interacting many-agent system.</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Does reproducing the same geometry mean two models represent the same real process?</span></div>
""", "controlled-to-dynamics", tags=("slides",), slide_type="subslide"),

        md(r"""
The middle-removal pictures are controlled mathematical constructions. Natural systems need not remove precisely the middle third or middle triangle at every generation for these models to be useful.

There are, however, more defensible process connections:

- In an **open dynamical system**, trajectories that enter an escape region are removed. The set of points that survive indefinitely can have Cantor-like structure. Here “removal” represents escape, but the connection is abstract rather than a universal physical mechanism.
- **Elementary cellular automaton Rule 90** generates a Sierpiński triangle from local XOR interactions. No triangle is manually removed. The apparent holes emerge from the update rule. This is a stronger complex systems bridge and prepares us for cellular automata later in the unit.
- The **chaos game** reaches the Sierpiński attractor through constrained random iteration. It demonstrates that the same limiting geometry can arise from a very different construction.

These examples sharpen the modelling lesson: matching geometry is evidence worth explaining, not proof of a shared mechanism.
""", "controlled-to-dynamics-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
## Infinite complexity is a limiting claim

At every finite depth, the construction contains only finitely many pieces. The mathematical fractal is the limiting object obtained by allowing the iteration depth to increase without bound.

<div class="qa-grid">
  <div class="qa-row"><p class="qa-question">Finite iteration</p><p class="qa-answer">a computable approximation with a smallest represented feature</p></div>
  <div class="qa-row"><p class="qa-question">Infinite limit</p><p class="qa-answer">new structure exists at arbitrarily small scales</p></div>
  <div class="qa-row"><p class="qa-question">Empirical system</p><p class="qa-answer">scaling can hold only between physical lower and upper cut-offs</p></div>
</div>

This is why an image cannot by itself demonstrate infinite complexity.
""", "infinite-complexity", tags=("slides",), slide_type="subslide"),

        md(r"""
# Exact dimension is not always available

<div class="slide-columns" style="grid-template-columns:.72fr 1.28fr;align-items:center">
  <div>
    <p><strong>This was the problem Mandelbrot was tackling.</strong></p>
    <p>A coastline has no known exact generator, only a finite statistical scaling range.</p>
    <p>A straight ruler resolves some bends and skips others, so ruler length is part of the measurement.</p>
    <p><strong>We need an empirical procedure that tracks visible structure across resolutions.</strong></p>
  </div>
  <img class="column-image" src="images/Great-britain-coastline-paradox.gif" alt="Successively finer measurements of the British coastline" style="max-height:390px;object-fit:contain">
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>As the ruler shrinks, what happens to the measured length? Must it converge?</span></div>

This returns us to Mandelbrot's motivating problem: **How long is the coast of Britain?**

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down:</strong> inspect what one ruler sees. <strong>Up:</strong> measure the scaling relationship across ruler lengths.</span></div>
""", "empirical-transition", tags=("slides",), slide_type="slide"),

        md(r"""
## Dimension is not one universal object

<div class="model-specification wide-description-table">
  <div><strong>Topological dimension</strong><span>how many local coordinates are needed in a topological sense</span></div>
  <div><strong>Similarity dimension</strong><span>the exponent from exact copies with a common contraction ratio</span></div>
  <div><strong>Hausdorff dimension</strong><span>an intrinsic covering definition that allows arbitrarily varied covering sets</span></div>
  <div><strong>Box-counting dimension</strong><span>a grid-based scaling limit that is often easier to estimate</span></div>
</div>

For many familiar self-similar sets these dimensions agree. In general they need not.
""", "dimension-hierarchy", tags=("reader-only",), slide_type="skip"),

        md(r"""
## Hausdorff dimension: an intrinsic definition

For $s\geq0$, cover a set $X$ by countably many sets $U_i$ with diameters at most $\delta$. The least possible covering cost is

$$\mathcal H^s_\delta(X)=
\inf\left\{
\sum_i\bigl(\operatorname{diam}U_i\bigr)^s:
X\subseteq\bigcup_iU_i,
\operatorname{diam}U_i\leq\delta
\right\}.$$

Then let the permitted covering diameter shrink:

$$\mathcal H^s(X)=\lim_{\delta\downarrow0}\mathcal H^s_\delta(X).$$

The Hausdorff dimension is the critical exponent

$$\dim_H X
=\inf\{s:\mathcal H^s(X)=0\}
=\sup\{s:\mathcal H^s(X)=\infty\}.$$

Below this exponent the covering cost is infinite; above it the cost is zero. At the critical exponent, the Hausdorff measure may be zero, finite and positive, or infinite. Some conventions include a constant factor in the measure; that factor does not change the dimension.

The definition optimises over coverings and handles highly irregular sets, but it is usually difficult to calculate directly from finite empirical data. Box counting replaces this optimisation with a regular grid. It is more computable, but more sensitive to representation and scale choices.

**Hausdorff dimension provides mathematical context only and will not be assessed in this unit.**
""", "hausdorff-dimension", tags=("reader-only",), slide_type="skip"),

        md(r"""
Hausdorff dimension uses optimised coverings rather than boxes from one fixed grid.

For bounded subsets of $\mathbb R^n$, Hausdorff dimension is no greater than upper box-counting dimension. For self-similar sets satisfying the open set condition, Hausdorff dimension equals the similarity dimension. The middle-thirds Cantor set and Sierpiński triangle satisfy this condition. Equality is not automatic for arbitrary sets.

See J. E. Hutchinson (1981), [“Fractals and Self Similarity”](https://doi.org/10.1512/iumj.1981.30.30055), *Indiana University Mathematics Journal* 30, 713–747.
""", "hausdorff-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Box counting

<div class="slide-columns" style="grid-template-columns:1.05fr .95fr;align-items:center">
  <div>
    <img src="images/BoxCounting_Wiki.png" alt="Box coverings at multiple resolutions" style="width:100%;max-height:430px;object-fit:contain">
  </div>
  <div>
    <p>Cover the object using boxes of side length ε. Count the occupied boxes N(ε).</p>
    <p>If the count follows a power law, a log-log plot has slope D.</p>
    <p>This is the <strong>box-counting</strong>, or <strong>Minkowski–Bouligand</strong>, dimension.</p>
  </div>
</div>

$$D_B=\lim_{\varepsilon\to0}\frac{\log N(\varepsilon)}{\log(1/\varepsilon)},
\qquad
\log N(\varepsilon)\approx D\log(1/\varepsilon)+c\quad\text{for finite data}.$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="34" height="34"><span>Resolution, grid origin, threshold, and fitted scale range all matter</span></div>

<div class="figure-caption">Figure: <a href="https://commons.wikimedia.org/wiki/File:Great_Britain_Box.svg">Great Britain box coverings</a>, Wikimedia Commons. This is the source image linked from the Minkowski–Bouligand dimension article.</div>
""", "box-counting-intro", tags=("slides",), slide_type="slide"),

        md(r"""
## Why can a count reveal dimension?

Halve the box width and ask how the occupied count multiplies:

<div class="qa-grid">
  <div class="qa-row"><p class="qa-question">Smooth curve</p><p class="qa-answer">about 2 times as many boxes: 2¹</p></div>
  <div class="qa-row"><p class="qa-question">Filled region</p><p class="qa-answer">about 4 times as many boxes: 2²</p></div>
  <div class="qa-row"><p class="qa-question">Fractal boundary</p><p class="qa-answer">between 2 and 4 times: 2ᴰ, with 1 &lt; D &lt; 2</p></div>
</div>

Dimension is the exponent that makes the multiplication of visible detail predictable across scales. Taking logarithms turns that repeated multiplication into a slope.

For an ideal object the ratio may converge as $\varepsilon\to0$. For empirical data, we instead look for a stable slope across a justified finite scaling range.
""", "box-counting-intuition", tags=("slides",), slide_type="subslide"),

        md(r"""
## The box-counting dimension

$$D_B=\lim_{\varepsilon\to0}\frac{\log N(\varepsilon)}{\log(1/\varepsilon)}.$$

For finite data, we estimate

$$\log N(\varepsilon)\approx D\log(1/\varepsilon)+c$$

over a selected range of scales.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="34" height="34"><span>Resolution, grid origin, threshold, and fitted scale range all matter</span></div>
""", "box-counting-definition", tags=("slides",), slide_type="subslide"),

        md(r"""
## Better depends on the question

<div class="model-specification">
  <div><strong>Spatial support</strong><span>box-counting or Minkowski dimension</span></div>
  <div><strong>Point cloud or attractor</strong><span>correlation dimension</span></div>
  <div><strong>Uneven mass across scales</strong><span>information and generalised dimensions; multifractal spectrum</span></div>
  <div><strong>Time series or rough signal</strong><span>methods matched to the signal, such as correlation sums, DFA, Higuchi, or wavelet scaling</span></div>
</div>

There is no universally best estimator. Validate against known examples and test sensitivity to scale range, noise, sample size, and preprocessing.

For box counting in particular, grid placement, thresholding, finite resolution, and the fitted scale range can dominate the estimate. Use it when occupied spatial geometry is the target and several credible resolutions are available.
""", "dimension-method-choice", tags=("reader-only",), slide_type="skip"),

        md(r"""
The limit defines an idealised box-counting dimension. A computational estimate replaces that limit with a finite regression. A responsible report therefore includes:

- how the object was represented or binarised;
- image resolution and physical scale, if known;
- box sizes and grid alignment;
- the scale range included in the fit;
- sensitivity to reasonable alternative choices;
- uncertainty or run-to-run variability where sampling is stochastic.

Box-counting estimators remain useful, but their bias and variance depend on the estimator and data-generating process. See P. Hall and A. Wood, [“On the performance of box-counting estimators of fractal dimension”](https://doi.org/10.1093/biomet/80.1.246), *Biometrika* 80 (1993). For attractors and time-series data, a recent comparative treatment is G. Datseris et al., [“Estimating fractal dimensions: a comparative review and open source implementations”](https://arxiv.org/abs/2109.05937).

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down:</strong> inspect pixels and occupied boxes. <strong>Up:</strong> compress their scaling relationship into an estimated exponent.</span></div>
""", "box-counting-practice-reader", tags=("reader-only",), slide_type="skip"),

        md(r"""
# Different coastlines

<div class="slide-columns evidence-layout compact-evidence-layout" style="grid-template-columns:1.18fr .82fr">
  <div class="evidence-panel"><img src="images/coastline_country_comparison.svg" alt="Estimated coastline fractal dimensions for seven countries"></div>
  <div class="meaning-panel">
    <img src="images/coastline_extremes.svg" alt="Natural Earth outlines comparing Norway and South Africa" style="width:100%;max-height:190px;object-fit:contain">
    <p><strong>A larger estimate means:</strong> occupied coastline detail grows faster as the map resolution becomes finer.</p>
    <p><strong>It does not mean:</strong> a better coast, a longer coast at every stated resolution, or one universal geological mechanism.</p>
    <p><strong>The useful next question:</strong> do fjords, islands, erosion, lithology, glaciation, tides, or mapping choices explain the contrast?</p>
  </div>
</div>

<p><strong>Evidence check:</strong> one exponent is useful only if a stable scaling range and measurement protocol are reported.</p>

<div class="figure-caption">Selected values from the <a href="https://datarepository.wolframcloud.com/resources/WolframSummerCamp_Coastline-Fractal-Dimensions/">Wolfram Data Repository coastline dataset</a>. Country outlines from Natural Earth, public domain. Treat these as one method-dependent comparison, not definitive national constants.</div>
""", "australian-coast", tags=("slides",), slide_type="slide"),

        md(r"""
## A straight line is not enough

<div class="slide-columns" style="grid-template-columns:1.25fr .75fr;align-items:center">
  <img src="images/britain_boxcount_diagnostic.svg" alt="Illustrative box-counting log-log plot for a rasterised British coastline" style="width:100%;max-height:450px;object-fit:contain">
  <div>
    <p>A fitted slope is credible only across a justified scaling range.</p>
    <p>Fine scales can saturate at pixel resolution. Coarse scales feel the finite size of the country.</p>
    <p>Too few scales, thresholding, grid placement, or a crossover between mechanisms can also create an apparently straight region.</p>
  </div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Which points would you fit, and what evidence justifies excluding the others?</span></div>

Scaling is a claim to interrogate, not a visual effect to admire.

<div class="figure-caption">Illustrative diagnostic calculated from the rasterised Britain silhouette used in this Reader. The estimate is representation- and range-dependent, not a definitive dimension for Britain.</div>
""", "scaling-caution", tags=("slides",), slide_type="subslide"),

        md(r"""
## Reproduce the Britain diagnostic

The code below repeats the calculation used for the preceding figure. It counts grid boxes crossed by the land/background boundary, then fits only a stated intermediate range. This makes the representation, box sizes, and fitted points inspectable rather than hiding them inside the finished graphic.
""", "scaling-caution-code-intro", tags=("reader-only",), slide_type="skip"),

        code(r'''
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def occupied_boundary_boxes(mask, box_size):
    """Count grid boxes containing both land and background pixels."""
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
    return np.count_nonzero(
        blocks.any(axis=(2, 3)) & (~blocks).any(axis=(2, 3))
    )


image_path = Path("images/British_coastline.png")
rgba = np.asarray(Image.open(image_path).convert("RGBA"))
land = (rgba[..., 3] > 20) & (rgba[..., :3].mean(axis=2) < 210)

box_sizes = np.array([2, 4, 8, 16, 32, 64, 128, 256])
counts = np.array([
    occupied_boundary_boxes(land, size) for size in box_sizes
])

x = np.log(1 / box_sizes.astype(float))
y = np.log(counts)
fit_indices = np.arange(1, 6)
slope, intercept = np.polyfit(x[fit_indices], y[fit_indices], 1)

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(x, y, color="#1B2A4C", zorder=3)
ax.plot(
    x[fit_indices],
    slope * x[fit_indices] + intercept,
    color="#D5A62A",
    linewidth=3,
    label=f"intermediate-scale slope = {slope:.2f}",
)
ax.set(xlabel=r"$\log(1/\varepsilon)$", ylabel=r"$\log N(\varepsilon)$")
ax.legend(frameon=False)
plt.show()
''', "scaling-caution-code", tags=("reader-only", "hide-input"), slide_type="skip"),

        md(r"""
# From pattern back to mechanism

Fractal analysis can **constrain explanations** by identifying patterns that a proposed mechanism should reproduce. It cannot recover one unique mechanism from geometry alone.

<div class="analysis-perspectives">
  <div><strong>A fractal dimension can tell us</strong><p>how occupied structure changes with resolution over a stated range of scales.</p></div>
  <div><strong>It cannot tell us alone</strong><p>which interactions generated the pattern, whether the scaling continues, or whether two matching exponents imply the same process.</p></div>
</div>

<p><strong>Description is evidence, not a complete explanation.</strong> A shared exponent can motivate comparison, but it does not establish a shared mechanism.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Return down the ladder:</strong> use the measured pattern to decide which local mechanisms and model assumptions deserve investigation.</span></div>
""", "pattern-to-mechanism", tags=("slides",), slide_type="slide"),

        md(r"""
The methods developed this week become tools for interrogating later models.

## Connections across the unit

<div class="model-specification">
  <div><strong>Cellular automata</strong><span>local update rules can generate branching, rough boundaries, nested structure, and scale-dependent patterns</span></div>
  <div><strong>Critical phenomena</strong><span>percolation supplies a canonical fractal cluster at its critical threshold</span></div>
  <div><strong>Self-organised criticality</strong><span>avalanche sizes and spatial footprints can exhibit scaling over broad ranges</span></div>
</div>

## Connections to earlier units

<div class="analysis-perspectives">
  <div><strong>Chaotic dynamics · MATH3021</strong><p>Dimension summarises how strange attractors occupy state space.</p></div>
  <div><strong>Networks · MATH3002</strong><p>Some networks are self-similar under box-covering. Scale-free degree alone does not imply fractality.</p></div>
</div>

""", "fractals-return", tags=("reader-only",), slide_type="skip"),

        md(r"""
References for these connections: Grassberger and Procaccia, [strange-attractor dimension](https://doi.org/10.1103/PhysRevLett.50.346); Song, Havlin and Makse, [self-similarity of complex networks](https://doi.org/10.1038/nature03248). Percolation and self-organised criticality are different mechanisms, but both connect criticality, scaling, and fractal geometry.
""", "fractals-return-reader", tags=("reader-only",), slide_type="skip"),
    ]

    # The source is organised in thematic blocks above, while this explicit
    # order records the intended teaching narrative. Keeping the sequence here
    # makes later handover edits auditable without relying on notebook position.
    teaching_order = [
        "week02-title",
        "opening-song",
        "opening-video-slides", "opening-video-reader", "opening-notes",
        "week02-route",
        "branching-contrast", "branching-explorable-slides",
        "branching-natural-comparison", "branching-explorable-reader",
        "dla-natural-comparison",
        "common-language", "complex_system_signatures",
        "euclidean-expectations",
        "happisburgh-cropped", "happisburgh-coin", "happisburgh-plate",
        "happisburgh-context", "happisburgh-reader",
        "scale-symmetry", "fractal-scale-symmetry",
        "empirical-form", "fractal-visual-test", "fractal-properties", "fractal-properties-slide",
        "session2-controlled-fractals",
        "weierstrass-monster", "weierstrass-reader",
        "nonfractal-descriptors-reader",
        "canonical-constructions",
        "multiple-descriptions",
        "initiator-generator-cantor", "initiator-generator-sierpinski",
        "cantor-ifs", "sierpinski-ifs", "ifs-convergence",
        "chaos-game", "chaos-game-reader", "chaos-game-code-reader",
        "controlled-to-dynamics", "controlled-to-dynamics-reader",
        "l-system-definition", "cantor-l-system", "l-systems", "l-systems-reader", "l-systems-code-reader",
        "infinite-complexity",
        "cantor-construction", "cantor-detail-reader",
        "sierpinski-construction", "sierpinski-detail-reader",
        "why-dimension",
        "dimension-directions", "dimension-information", "euclidean-scaling",
        "euclidean-scaling-reader",
        "similarity-dimension", "cantor-dimension", "sierpinski-dimension",
        "dimension-caveat-reader",
        "empirical-transition", "coastline-reader",
        "dimension-hierarchy",
        "hausdorff-dimension", "hausdorff-reader",
        "box-counting-intro", "scaling-caution",
        "scaling-caution-code-intro", "scaling-caution-code",
        "dimension-method-choice", "box-counting-practice-reader",
        "australian-coast",
        "box-counting-intuition",
        "pattern-to-mechanism", "fractals-return", "fractals-return-reader",
    ]
    cells_by_id = {cell["id"]: cell for cell in notebook.cells}
    missing = [cell_id for cell_id in teaching_order if cell_id not in cells_by_id]
    retired = {
        "dla-model", "dla-emergence", "dla-explorable-slides",
        "dla-drift-explanation", "dla-explorable-reader",
        "scale-intuition", "characteristic-scale", "why_complex_systems",
        "not-all-fractals", "fractal-provocation", "representations-compared",
        "representations-processes", "fractals-backwards",
        "branching-model", "fractals_in_complex_systems",
        "fractal-tension", "mandelbrot-quote",
        "coastline-question", "box-counting-definition",
        "infinite-detail",
        "scale-symmetry-reader", "three-fractal-roles",
    }
    unplaced = [cell_id for cell_id in cells_by_id if cell_id not in teaching_order and cell_id not in retired]
    if missing or unplaced:
        raise ValueError(f"Week 2 teaching order mismatch. Missing={missing}; unplaced={unplaced}")
    notebook.cells = [cells_by_id[cell_id] for cell_id in teaching_order]

    # Preserve the latest approved Week 2 additions, reader-only material, and
    # teaching order after this broader legacy rebuild has done its work.
    apply_current_week02(notebook)
    nbf.write(notebook, TARGET)
    print(f"Wrote {TARGET} ({len(notebook.cells)} cells)")


if __name__ == "__main__":
    main()
