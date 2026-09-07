from pathlib import Path

import nbformat


path = Path("notebooks/week03/L_Reaction_diffusion.ipynb")
notebook = nbformat.read(path, as_version=4)

for cell in notebook.cells:
    if cell.cell_type != "markdown":
        continue

    if cell.source.startswith("# Turing’s general model"):
        cell.source = r'''# Turing’s general model

Turing considered chemical substances, or **morphogens**, whose local concentrations affect one another and diffuse through tissue:

$$
\frac{\partial a}{\partial t}=F(a,b)+D_a\nabla^2a,
\qquad
\frac{\partial b}{\partial t}=G(a,b)+D_b\nabla^2b.
$$

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/turing_1952_first_page.png" alt="First page of Turing's 1952 paper" style="display:block;width:72%;max-height:350px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p><em>F</em> and <em>G</em> describe local reactions. <em>D</em><sub>a</sub> and <em>D</em><sub>b</sub> describe spatial spreading.</p>
<p>A uniform equilibrium may be stable to local reaction alone yet become unstable once the substances diffuse at different rates. Small perturbations can then select a spatial mode and grow into pattern.</p>
</div>
</div>

<p class="figure-reference">A. M. Turing, <a href="https://doi.org/10.1098/rstb.1952.0012">“The Chemical Basis of Morphogenesis”</a> (1952).</p>'''

    if "U^{n+1}_{i,j}=U^n_{i,j}" in cell.source:
        cell.source = (
            cell.source
            .replace("U^{n+1}_{i,j}=U^n_{i,j}", "U^{(n+1)}_{i,j}=U^{(n)}_{i,j}")
            .replace("V^{n+1}_{i,j}=V^n_{i,j}", "V^{(n+1)}_{i,j}=V^{(n)}_{i,j}")
            .replace("U^n", "U^{(n)}")
            .replace("V^n", "V^{(n)}")
        )

    if cell.source.startswith("### Which cells count as neighbours?"):
        cell.metadata["tags"] = ["slides-only"]

nbformat.write(notebook, path)
