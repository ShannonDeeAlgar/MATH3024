#!/usr/bin/env python3
"""Strengthen the Turing-instability spine of the Week 3 lecture/Reader."""

from pathlib import Path
import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def find_cell(nb, cell_id):
    for cell in nb.cells:
        if cell.get("id") == cell_id:
            return cell
    raise KeyError(cell_id)


def markdown(source, cell_id, *, tags=None, slide_type="skip"):
    cell = nbformat.v4.new_markdown_cell(source)
    cell["id"] = cell_id
    cell["metadata"] = {
        "tags": list(tags or ["reader-only"]),
        "slideshow": {"slide_type": slide_type},
    }
    return cell


def main():
    nb = nbformat.read(NOTEBOOK, as_version=4)

    find_cell(nb, "week03-turing-reception-reader").source = r'''### From an unusual proposal to a modern framework

The paper was not entirely unnoticed. The embryologist C. H. Waddington corresponded with Turing about biological applications. Even so, the work received limited attention for several decades. Then molecular genetics changed the centre of gravity of biology. The double-helix model appeared in 1953, and developmental biologists understandably concentrated on genes and molecular mechanisms. Turing's abstract morphogens were difficult to identify or measure, and direct chemical examples were scarce. DNA did not make the reaction–diffusion idea irrelevant, but it made the theory harder to test at the time.

That position has changed. Reaction–diffusion models are now a standard framework for studying spontaneous spatial pattern formation. Experimental support exists in chemical systems and in several developmental settings, including pigment patterns, hair and feather follicles, digits and mammalian palate patterning.

The terminology is now used more carefully. In this unit, a **Turing pattern** is a stationary spatial pattern produced by a **diffusion-driven instability**: a spatially homogeneous equilibrium is stable under the local reaction dynamics, but becomes unstable to at least one spatially varying perturbation after diffusion couples locations. Waves and temporal oscillations are important reaction–diffusion behaviours, but we will not call every such behaviour a Turing pattern.

Reaction–diffusion is not the explanation for every biological pattern, and visual similarity to a simulated pattern is not evidence of the mechanism. Modern studies use the model to make experimentally testable claims about molecules, interactions, transport rates and perturbations.

See Ball (2015), [“Forging patterns and making waves from biology to geology”](https://doi.org/10.1098/rstb.2014.0218), and Kondo (2022), [“The present and future of Turing models in developmental biology”](https://journals.biologists.com/dev/article/149/24/dev200974/286110/The-present-and-future-of-Turing-models-in).'''

    find_cell(nb, "week03-why-reaction-diffusion").source = r'''## Turing’s mechanism: reaction and diffusion

Turing proposed two familiar processes acting together.

<div class="two-panel equal-panels compact-panels">
  <div class="text-panel">
    <p><strong>Reaction:</strong> molecules meet and change identity locally. At particle level, specify which molecular encounter changes what.</p>
    <p><strong>Perturbations:</strong> small departures from a homogeneous state are unavoidable. They may come from molecular noise, neighbouring structures or small geometric irregularities.</p>
  </div>
  <div class="text-panel">
    <p><strong>Diffusion:</strong> irregular molecular motion brings reactants together and carries products elsewhere.</p>
    <p><strong>Spatial coupling:</strong> motion allows a local chemical change to influence nearby tissue.</p>
  </div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Diffusion normally smooths spatial differences. How could adding diffusion make a homogeneous state less stable?</span></div>'''

    find_cell(nb, "week03-turing-six-modes").source = r'''### Diffusion-driven instability

<p><strong>A diffusion-driven instability</strong> occurs when a homogeneous equilibrium is stable to spatially uniform perturbations, but unstable to at least one spatial mode after diffusion couples locations.</p>

$$
\text{stable homogeneous reaction state}
+\text{differential diffusion}
\longrightarrow
\text{selected spatial wavelength grows}
$$

<div class="analysis-perspectives three compact-panels">
  <div class="text-panel"><p><strong>1. Begin near uniform.</strong><br>Small perturbations provide many possible spatial wavelengths.</p></div>
  <div class="text-panel"><p><strong>2. Most differences decay.</strong><br>Reaction alone restores the homogeneous equilibrium.</p></div>
  <div class="text-panel"><p><strong>3. A band grows.</strong><br>Differential diffusion changes the stability of selected spatial modes.</p></div>
</div>

<p class="small-note"><strong>Spatial mode:</strong> a repeating spatial variation with a particular wavelength. In the classical two-species mechanism the diffusion coefficients differ, but unequal diffusion alone is not sufficient.</p>

<div class="definition-panel"><strong>Turing pattern:</strong> the stationary, spatially non-uniform pattern produced when this instability grows and later saturates. Oscillatory and travelling-wave instabilities are related reaction–diffusion phenomena, but are distinct from the stationary pattern studied here.</div>

<p class="small-note">The growth of each mode is determined by a linear stability analysis. Some students may have seen this method before; it is useful context, but it is not assessable in this unit.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace individual molecules with spatial modes and ask which wavelengths grow.</span></div>'''

    math_id = "week03-turing-linear-stability-reader"
    math_source = r'''### The mathematics in Turing’s paper

<div class="reader-note"><strong>Context only: this linear stability analysis is not assessable.</strong></div>

Turing first considered a ring of $N$ cells. Each cell contained two morphogen concentrations and exchanged material with its two neighbours. He then replaced the separate cells by a continuous ring of tissue, with position described by the polar angle $\theta$. The two descriptions ask the same question at different levels of resolution.

Let $(U^\ast,V^\ast)$ be a homogeneous equilibrium and let $\boldsymbol\eta$ be a small perturbation. Near the equilibrium, the local reactions are approximated by their Jacobian $J$:

$$
\frac{d\boldsymbol\eta}{dt}=J\boldsymbol\eta.
$$

The equilibrium is locally stable when every eigenvalue of $J$ has negative real part. A perturbation then decays if all locations are changed in the same way.

On the ring, a spatial perturbation can be decomposed into Fourier modes. A mode with wave number $q$ evolves according to

$$
\frac{d\widehat{\boldsymbol\eta}_q}{dt}
=\left(J-q^2\mathsf D\right)\widehat{\boldsymbol\eta}_q,
\qquad
\mathsf D=
\begin{pmatrix}
D_U&0\\
0&D_V
\end{pmatrix}.
$$

The $-q^2\mathsf D$ term is the effect of diffusion. The surprising case occurs when $J$ is stable, yet $J-q^2\mathsf D$ has an eigenvalue with positive real part for some non-zero $q$. Those wavelengths grow from the initial perturbation. The fastest-growing wave number $q_\ast$ predicts the early spacing,

$$
\lambda_\ast=\frac{2\pi}{q_\ast}.
$$

Linear analysis predicts the onset and selected wavelength, not the final amplitude or detailed morphology. Nonlinear terms eventually limit the growth.

Turing distinguished stationary waves from oscillatory travelling waves. His two-morphogen calculation included spatially uniform temporal oscillation, but he placed finite-wavelength travelling and shortest-wavelength oscillatory cases in the three-or-more-morphogen category. Modern reaction–diffusion theory allows a broader range of oscillatory and wave instabilities. In this unit, **Turing pattern** refers to the stationary diffusion-driven case.

Source: Turing (1952), [“The Chemical Basis of Morphogenesis”](https://doi.org/10.1098/rstb.1952.0012), especially §§6–9.'''

    existing = next((i for i, c in enumerate(nb.cells) if c.get("id") == math_id), None)
    if existing is None:
        anchor = next(i for i, c in enumerate(nb.cells) if c.get("id") == "week03-turing-six-modes")
        nb.cells.insert(anchor + 1, markdown(math_source, math_id))
    else:
        nb.cells[existing].source = math_source

    find_cell(nb, "week03-turing-paper-reader").source = r'''### What else is in the 1952 paper?

The paper is broader and more cautious than the phrase “spots and stripes” suggests.

- Turing defines a **morphogen** simply as a “form producer”. He does not require it to be one particular molecule.
- He focuses on the **onset of instability**, rather than claiming to calculate a complete adult form.
- The six cases classify early linear behaviour near a homogeneous equilibrium. They are not six finished animal-coat patterns.
- His examples include Hydra tentacles, leaf whorls, gastrulation, dappling and phyllotaxis.
- He explicitly says that nonlinear development will require particular computational experiments using digital computers.

Turing's disturbances need not be one prescribed random process. He lists Brownian motion, influences from neighbouring structures and small irregularities of form as possible departures from exact homogeneity. The instability selects which of those small components can grow.

The opening excerpt reproduced earlier is also a concise statement of modelling humility: a model is a simplification, and the modeller must decide which features are important enough to retain.'''

    find_cell(nb, "week03-gray-scott-history").source = r'''# Add reaction: the Gray–Scott model

## A concrete particle story

Turing supplied a general mechanism and a stability test, but not one unique pair of reaction laws. Gray–Scott gives us a particular chemical story that can be simulated and interrogated in detail.

$$u+2v\longrightarrow3v.$$

Existing $v$ is therefore required to make one additional $v$: the product promotes its own production. This is **autocatalysis**. Under the mass-action assumption, encounters occur at a rate proportional to $uv^2$.

The reactor also supplies $u$, removes $v$, and allows both molecular species to move randomly.

<p class="small-note">Peter Gray and Stephen K. Scott developed the reaction model for cubic autocatalysis in an open reactor. Pearson’s later spatial simulations mapped spots, waves, splitting structures and irregular dynamics, helping establish Gray–Scott as a canonical reaction–diffusion model. It belongs to Turing's wider framework, but not every Gray–Scott output is a classical stationary Turing pattern.</p>'''

    find_cell(nb, "36fa3ed0").source = r'''## The continuous Gray–Scott model

The Gray–Scott model is a **pair of coupled nonlinear reaction–diffusion partial differential equations** for the concentration fields $U(\mathbf x,t)$ and $V(\mathbf x,t)$:

$$
\frac{\partial U}{\partial t}=D_U\nabla^2U-UV^2+f(1-U),
\qquad
\frac{\partial V}{\partial t}=D_V\nabla^2V+UV^2-(f+k)V.
$$

**Coupled:** each equation depends on both fields through $UV^2$.  
**Local terms:** reaction, feed and removal change concentrations at one location.  
**Spatial terms:** diffusion couples nearby locations, generally at different rates.

This is the continuous model we intend to solve. We must next choose a finite representation that a computer can update.'''

    nbformat.write(nb, NOTEBOOK)


if __name__ == "__main__":
    main()
