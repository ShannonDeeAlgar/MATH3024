from pathlib import Path

import nbformat


root = Path(__file__).resolve().parents[1]
path = root / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = nbformat.read(path, as_version=4)


def replace_start(prefix, source, slide_type=None, tags=None):
    for cell in nb.cells:
        if cell.cell_type == "markdown" and cell.source.lstrip().startswith(prefix):
            cell.source = source
            if slide_type is not None:
                cell.metadata["slideshow"] = {"slide_type": slide_type}
            if tags is not None:
                cell.metadata["tags"] = tags
            return cell
    raise RuntimeError(f"Could not find {prefix!r}")


replace_start("# What Turing actually proposed", r'''# Turing’s general model

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/turing_1952_first_page.png" alt="First page of Turing's 1952 paper" style="display:block;width:78%;max-height:430px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>Turing considered chemical substances, or <strong>morphogens</strong>, whose local concentrations affect one another and diffuse through tissue.</p>
$$
\frac{\partial a}{\partial t}=F(a,b)+D_a\nabla^2a,
\qquad
\frac{\partial b}{\partial t}=G(a,b)+D_b\nabla^2b.
$$
<p>$F$ and $G$ describe local reactions. $D_a$ and $D_b$ describe spatial spreading.</p>
<p>A uniform equilibrium may be stable to local reaction alone yet become unstable once the substances diffuse at different rates. Small perturbations can then select a spatial mode and grow into pattern.</p>
</div>
</div>

<p class="figure-reference">A. M. Turing, <a href="https://doi.org/10.1098/rstb.1952.0012">“The Chemical Basis of Morphogenesis”</a> (1952).</p>
''')

replace_start("## Six possible linear outcomes", r'''## What can happen near the uniform state?

Turing classified the ways a small disturbance can initially evolve. At a high level it may:

1. **decay**, returning the system to a uniform state;
2. **grow uniformly**, changing concentration without selecting a spatial pattern;
3. **oscillate in time**;
4. **amplify a spatial mode**, producing a stationary or oscillating pattern.

The last case is the one now usually meant by a **Turing instability**: diffusion helps destabilise the uniform state and selects a spatial wavelength.

This is a prediction about the onset of pattern. Nonlinear dynamics determine the later, visible form.
''', "slide", ["slides"])

replace_start("### Reading the six cases", r'''### Turing’s linear analysis

Turing’s six cases distinguish whether the dominant eigenvalues are real or complex, positive or negative, and associated with uniform or spatial modes. They classify the initial response near equilibrium rather than six finished animal-coat patterns.

For this unit, retain the central contrast: perturbations may disappear, spread uniformly, oscillate, or be amplified into spatial structure. We will not assess the six-case eigenvalue classification.
''', "", ["reader-only"])

replace_start("# The Gray–Scott model", r'''# From Turing’s idea to the Gray–Scott model

## Why change models?

Turing supplied a **general mechanism**, not one unique pair of reaction functions $F$ and $G$. Many reaction systems can realise the same reaction–diffusion logic.

We use Gray–Scott because it gives us a compact, explicit and widely studied nonlinear system that produces spots, stripes, labyrinths, waves and replication-like behaviour. It is a canonical model for exploring the mechanism, not the chemistry Turing originally calculated.

“Gray–Scott” names two researchers: **Peter Gray** and **Stephen K. Scott**. Their continuously fed autocatalytic reactor model was later mapped computationally across parameter space, notably by Pearson (1993).
''')

replace_start("## 1. Reaction", r'''## 1. Reaction: local positive feedback

$$
U+2V\longrightarrow 3V,
\qquad \text{local rate }UV^2.
$$

Two units of $V$ help convert one unit of $U$ into an additional $V$. Because $V$ participates in producing more $V$, the reaction is **autocatalytic**.

- $U$ is the supplied reactant or **feed chemical**.
- $V$ is the autocatalytic product.
- The rate $UV^2$ is large only where both chemicals are present, and is especially sensitive to $V$.

Locally, the reaction removes $U$ and adds $V$ at exactly the same rate:

$$
R_U=-UV^2,
\qquad
R_V=+UV^2.
$$
''')

replace_start("## 2. Diffusion", r'''## 2. Diffusion: spatial coupling

Reaction changes concentrations at one location. Diffusion couples nearby locations:

$$
\frac{\partial U}{\partial t}=D_U\nabla^2U,
\qquad
\frac{\partial V}{\partial t}=D_V\nabla^2V.
$$

$D_U$ and $D_V$ control how rapidly each field spreads. Unequal diffusion is central to the Turing mechanism because local reinforcement and longer-range spreading act over different spatial scales.

Where does this smooth diffusion term come from if matter moves as individual particles? Begin with a random walk.
''')

replace_start("### Random walk: a discrete model", r'''### Random walk: a discrete model

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/random_walk_types_stats.svg" alt="Unbiased, biased and persistent random walks with the statistics used to compare them" style="display:block;width:100%;max-height:430px;object-fit:contain;"></div>
<div class="text-panel">
<p>A random walk is a sum of random increments:</p>
$$
\mathbf X_n=\sum_{m=1}^{n}\boldsymbol\xi_m.
$$
<p><strong>Unbiased:</strong> no preferred direction, so $\mathbb E[\boldsymbol\xi_m]=\mathbf0$.</p>
<p><strong>Biased:</strong> a non-zero mean step creates drift.</p>
<p><strong>Persistent or correlated:</strong> successive directions are related, producing straighter local motion.</p>
</div>
</div>

For diffusion we begin with independent, unbiased increments of finite variance.
''')

replace_start("### Brownian motion: the physical phenomenon", r'''### Brownian motion: the physical phenomenon

<div class="two-panel equal-panels">
<div class="image-panel"><iframe width="100%" height="315" src="https://www.youtube.com/embed/cDCbcR8FsH8" title="Brownian motion" frameborder="0" allowfullscreen></iframe></div>
<div class="text-panel">
<p>Brownian motion is the continuous-time stochastic limit of many small, independent random steps.</p>
$$
\mathbf B(t+\Delta t)-\mathbf B(t)
\sim\mathcal N(\mathbf0,2D\Delta t\,I_d).
$$
<p>In $d$ dimensions,</p>
$$
\mathbb E\lVert\mathbf B(t)-\mathbf B(0)\rVert^2=2dDt.
$$
<p>One path remains irregular. The predictable diffusion law appears in an ensemble or probability density.</p>
</div>
</div>
''')

replace_start("### From one random walk to diffusion", r'''### What would we measure?

<img src="images/brownian_ensemble_msd.svg" alt="One Brownian trajectory and an ensemble mean-square-displacement comparison with four D t" style="display:block;width:78%;max-height:440px;object-fit:contain;margin:0 auto;">

- **Mean displacement** detects drift and is zero for an unbiased walk.
- **Mean-square displacement** measures spreading and grows linearly: $\mathbb E[R^2(t)]=2dDt$.
- **Endpoint distribution** approaches a Gaussian under the usual finite-variance assumptions.
- **First-passage time** asks when a path first reaches a target or boundary.
- **Step and turning-angle statistics** distinguish unbiased, biased and persistent motion.

The diffusion equation describes how the ensemble density evolves, not where one walker will go.
''', "subslide", ["slides"])

replace_start("## 3. Feed and removal", r'''## 3. Feed and removal: keep the reactor driven

Gray–Scott is an **open-flow reactor**, not a closed mixture.

$$
\text{feed of }U:\quad f(1-U),
\qquad
\text{removal of }V:\quad -(f+k)V.
$$

- Fresh $U$ flows in at concentration scaled to $1$. The deficit $1-U$ determines how strongly the feed restores it.
- Material leaves through the flow at rate $f$.
- $V$ also converts to an inert product at rate $k$, conventionally called the **kill rate**.

Feed and removal prevent simple exhaustion and maintain the system away from equilibrium, allowing reaction and diffusion to organise sustained spatial behaviour.
''')

replace_start("## Putting it all together", r'''## The complete Gray–Scott mechanism

<img src="images/gray_scott_model_map.svg" alt="Reaction, diffusion, feed and removal in the Gray–Scott model" style="display:block;width:92%;max-height:540px;object-fit:contain;margin:0 auto">
''')

replace_start("## Return to Turing’s classification", r'''## Return to Turing’s question

Gray–Scott specifies one particular pair of nonlinear reaction functions, then adds unequal diffusion, feed and removal.

The computational question is the same one Turing posed more generally:

> Can a nearly uniform state amplify small spatial differences into an organised pattern?

The parameter sweep shows that the answer depends on the reaction rates, diffusion rates, initial perturbation, domain and numerical choices. Similar visible patterns can arise from several parameter combinations, so morphology alone does not identify a unique mechanism.
''')

nbformat.write(nb, path)
print(f"Updated {path}")
