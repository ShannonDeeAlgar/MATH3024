from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def replace_math_block(source):
    marker = "In two or more dimensions we generalise the derivatives with the gradient and Laplacian operators:"
    if marker not in source:
        return source
    prefix = source.split(marker)[0]
    return prefix + r'''In two or more dimensions, the one-dimensional derivative is replaced by the gradient and Laplacian operators.

The flux is

$$
\mathbf J=-D\nabla C,
$$

and conservation of mass gives the diffusion equation

$$
\frac{\partial C}{\partial t}=D\nabla^2C.
$$

The gradient points in the direction of greatest increase in concentration. The minus sign therefore sends flux down the concentration gradient. The Laplacian records whether a location is high or low relative to its surroundings.'''


nb = nbformat.read(PATH, as_version=4)

# Remove the later duplicate microscopic/macroscopic diffusion GIF.
nb.cells = [
    c for c in nb.cells
    if not (c.source.startswith("e.g., we can consider a flux") and "Ficks_diffusion_micro_macro.gif" in c.source)
]

for cell in nb.cells:
    if cell.source.startswith("# Alan Mathison Turing"):
        cell.source = '''# Alan Turing

Turing helped establish theoretical computer science, worked in wartime cryptanalysis, designed early stored-program computers, and asked how machines might exhibit intelligence.

His work on morphogenesis asked a different question: can a simple physical mechanism generate biological form?'''

    if cell.source.startswith("## Alan Turing: a wider scientific life"):
        cell.source = cell.source.replace("Alan **Mathison** Turing", "Alan Turing")

    if cell.source.startswith("# Turing’s question: how does form emerge?"):
        cell.source = '''# Turing’s question: how does form emerge?

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Turing_and_imitation_game.png" alt="Alan Turing and representations of his work" style="display:block;width:88%;max-height:410px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>At Manchester, Turing turned to mathematical biology: how can an initially near-uniform embryo develop organised form?</p>
<p>This was a modelling proposal, not a report of one embryo he had observed. In the abstract of his 1952 paper he wrote that a system that was initially “quite homogeneous” might later develop structure after random disturbances destabilised the homogeneous equilibrium.</p>
<p>His candidate mechanism joined local chemical reaction to spatial diffusion. No pre-drawn spatial template was required.</p>
</div>
</div>'''

    if cell.source.startswith("## Fick's laws"):
        cell.source = replace_math_block(cell.source)

    if cell.source.startswith("## The sequence of representations"):
        cell.source = '''## The sequence of representations

Reaction and diffusion occur through microscopic interactions, but the useful macroscopic variables are concentrations. We describe those concentrations continuously with PDEs, then discretise the PDEs so a computer can update a finite array.

1. **Discrete particles:** molecules move and interact.
2. **Continuous description:** concentration fields $U(\mathbf x,t)$ and $V(\mathbf x,t)$ obey PDEs.
3. **Discrete computation:** arrays $U^{(n)}_{i,j}$ and $V^{(n)}_{i,j}$ approximate those fields on a grid.

Here $i$ and $j$ identify the grid cell. The superscript $n$ is the time-step index: $n=0$ is the initial array, $n=1$ is the array after one numerical update, and so on. Parentheses around $(n)$ emphasise that it is an index, not a power.

None of these is simply “the real model”. Each retains some features and suppresses others.'''

    if cell.source.startswith("### Which cells count as neighbours?"):
        cell.source = '''### Which cells count as neighbours?

<img src="images/grid_neighbourhoods.svg" alt="Von Neumann and Moore neighbourhoods on square grids" style="display:block;width:72%;max-height:340px;object-fit:contain;margin:0 auto .35rem;">

<div class="two-panel equal-panels">
<div class="text-panel"><p><strong>Von Neumann</strong></p><p>Four edge-sharing cells. It aligns naturally with a five-point finite-difference Laplacian and conserves a compact local stencil.</p></div>
<div class="text-panel"><p><strong>Moore</strong></p><p>Eight surrounding cells. It is useful when diagonal influence is part of the rule or when carefully chosen weights improve rotational symmetry.</p></div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Use the neighbourhood that represents the intended interaction or numerical operator. Adding diagonals without choosing their weights changes the model.</span></div>'''

    if cell.source.startswith("### Moore and von Neumann neighbourhoods"):
        cell.source = '''### Moore and von Neumann neighbourhoods

<img src="images/grid_neighbourhoods.svg" alt="Von Neumann and Moore neighbourhoods on square grids" style="display:block;width:66%;max-width:760px;margin:0 auto;">

A **von Neumann neighbourhood** contains the four cells sharing an edge with the focal cell. It is the natural choice for the standard five-point finite-difference Laplacian. It is also appropriate when the model permits movement or interaction only across shared edges.

A **Moore neighbourhood** also contains the four diagonal cells. It is appropriate when diagonal interactions are genuinely part of the local rule. In numerical diffusion, edge and diagonal cells require deliberately chosen weights; equal weights do not automatically approximate the same continuous Laplacian.

The neighbourhood is both a modelling choice and a numerical choice. It specifies which local information can affect one update and can change directional artefacts on the grid.'''

    if cell.source.startswith("# Reaction–diffusion beyond the simulation"):
        cell.source = '''# Reaction–diffusion beyond the simulation

<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/cima_experimental_turing_patterns.webp" alt="Experimental setup and stationary patterns in a CIMA gel reactor" style="display:block;width:100%;height:330px;object-fit:cover;object-position:center bottom;">
<p><strong>CIMA gel reactor</strong></p>
<p>Reactants diffuse through an unstirred gel supplied by reservoirs. Starch binds iodide and slows its effective diffusion. Within part of the operating range, the initially uniform reactor develops stationary hexagons or labyrinths. The experiment tests diffusion-driven symmetry breaking in a real chemical system.</p>
</div>
<div class="image-panel">
<img src="images/Zebrafish.jpg" alt="Zebrafish pigment stripes" style="display:block;width:100%;height:330px;object-fit:cover;">
<p><strong>Zebrafish pigment pattern</strong></p>
<p>Pigment cells interact over short and longer ranges as the fish grows. Models and experiments test whether those interactions reproduce stripe formation and repair. The mechanism is not Gray–Scott chemistry, even when the morphology is Turing-like.</p>
</div>
</div>

<p class="figure-reference">These examples test mechanisms, not visual resemblance alone. The CIMA system supplied early experimental evidence for stationary chemical Turing patterns; zebrafish provide a biological comparison involving interacting cells.</p>'''

    if cell.source.startswith("## Evidence, mechanism and morphology"):
        cell.source = '''## What is being tested?

The chemical reactor asks whether reaction, differential transport and sustained driving can break spatial symmetry under controlled conditions. The biological studies ask whether measured cell interactions can explain the formation, movement and repair of pigment stripes.

Similar-looking patterns do not establish a shared mechanism. The comparison is useful because it separates three questions: what pattern appears, which local processes can generate it, and what evidence distinguishes competing explanations?'''

# Put the literature in one Reader reference section.
reference_source = '''# References

- Turing, A. M. (1952), [“The Chemical Basis of Morphogenesis”](https://doi.org/10.1098/rstb.1952.0012), *Philosophical Transactions of the Royal Society B* 237, 37–72.
- De Kepper, P. et al. (1991), [“Turing-type chemical patterns in the chlorite–iodide–malonic acid reaction”](https://doi.org/10.1016/0167-2789(91)90204-M), *Physica D* 49, 161–169.
- Kondo, S. and Asai, R. (1995), [“A reaction–diffusion wave on the skin of the marine angelfish”](https://www.nature.com/articles/376765a0), *Nature* 376, 765–768.
- Nakamasu, A. et al. (2009), “Interactions between zebrafish pigment cells responsible for the generation of Turing patterns”, *Proceedings of the National Academy of Sciences* 106, 8429–8434.
- Economou, A. D. et al. (2012), [“Periodic stripe formation by a Turing mechanism operating at growth zones in the mammalian palate”](https://www.nature.com/articles/ng.1090), *Nature Genetics* 44, 348–351.
- Volkening, A. and Sandstede, B. (2018), “Iridophores as a source of robustness in zebrafish stripes and variability in Danio patterns”, *Nature Communications* 9, 3231.
'''
if not any(c.source.startswith("# References") for c in nb.cells):
    ref = nbformat.v4.new_markdown_cell(reference_source)
    ref.metadata["tags"] = ["reader-only"]
    ref.metadata["slideshow"] = {"slide_type": ""}
    nb.cells.append(ref)
else:
    for cell in nb.cells:
        if cell.source.startswith("# References"):
            cell.source = reference_source

nbformat.write(nb, PATH)
