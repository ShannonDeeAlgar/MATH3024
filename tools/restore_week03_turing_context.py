import json
from pathlib import Path


path = Path("notebooks/week03/L_Reaction_diffusion.ipynb")
notebook = json.loads(path.read_text())
cells = notebook["cells"]


def source(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def markdown_cell(cell_id: str, text: str, tags: list[str], slide_type: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {
            "tags": tags,
            "slideshow": {"slide_type": slide_type},
        },
        "source": source(text),
    }


by_id = {cell.get("id"): cell for cell in cells}

by_id["week03-turing-life-reader"]["source"] = source(
    """## Alan Turing: a wider scientific life

Alan Turing (1912–1954) moved repeatedly between abstract mathematics and concrete mechanisms. His 1936 work on computable numbers introduced the mathematical machine now called a Turing machine. During the Second World War he worked at Bletchley Park on German naval Enigma. He later designed the Automatic Computing Engine at the National Physical Laboratory, worked on the Manchester computers, and published *Computing Machinery and Intelligence* in 1950.

Morphogenesis was a marked change of scientific direction. At Manchester, Turing began asking how physical and chemical processes could generate biological form. The question was outside the areas for which he was already known, but it continued a recurring concern in his work: how can a compact set of rules produce organised behaviour?

Turing was prosecuted in 1952 for a homosexual relationship and subjected to hormonal treatment. He died in 1954. The British government apologised for his treatment in 2009, and he received a posthumous royal pardon in 2013. His life should not be reduced either to tragedy or to codebreaking. His work on morphogenesis belongs beside his work on computation as an attempt to understand what rules can generate.
"""
)

by_id["week03-why-reaction-diffusion"]["source"] = source(
    """## Turing’s proposed solution

Turing proposed two familiar processes acting together.

<div class="two-panel equal-panels compact-panels">
  <div class="text-panel">
    <p><strong>Reaction:</strong> molecules meet and change identity locally.</p>
    <p><strong>At particle level:</strong> ask which molecules must encounter one another, what the encounter produces, and whether material enters or leaves the system.</p>
  </div>
  <div class="text-panel">
    <p><strong>Diffusion:</strong> molecules follow irregular trajectories, carrying local chemical changes through tissue.</p>
    <p><strong>Perturbations:</strong> small fluctuations are unavoidable. The coupled system determines whether they decay or grow.</p>
  </div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Diffusion usually disperses differences. Could reactions between moving molecules make a difference grow instead?</span></div>
"""
)

by_id["week03-brownian-video-reader"]["source"] = source(
    """#### Reading the Brownian-motion notation

The film above contains many short microscope recordings of real Brownian motion. It runs for about 12 minutes; sample the snippets rather than treating it as required full-length viewing.

In the first relationship, $\\Delta t$ is one short time interval. The matrix $I_d$ is the $d\\times d$ identity matrix, so the $d$ coordinate increments are independent and have the same variance. The second relationship uses the total elapsed time $t$. In two dimensions the two coordinate variances add, giving mean-square displacement $4Dt$ and a typical distance proportional to $\\sqrt{4Dt}$.
"""
)

by_id["dc08556a"]["source"] = source(
    """### One path: distance from the origin

<img src="images/brownian_distance_sqrt.svg" alt="Two Brownian trajectories beginning at the yellow point and their distances from the origin compared with square-root reference curves" style="display:block;width:82%;max-height:400px;object-fit:contain;margin:0 auto;">

The yellow marker is the shared starting point, $\\mathbf{B}(0)=\\mathbf{0}$.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Stay low:</strong> one path is irregular. Its typical distance from the start follows a square-root scale.</span></div>
"""
)

by_id["week03-turing-paper-reader"]["source"] = source(
    """## What else is in the 1952 paper?

The paper is broader and more cautious than the phrase “spots and stripes” suggests.

- Turing defines a **morphogen** simply as a “form producer”. He does not require it to be one particular molecule.
- He develops both a **discrete cell model** and a **continuous tissue model**. That choice anticipates our later movement between random walks, concentration fields, and numerical grids.
- He focuses on the **onset of instability**. Small random departures from symmetry matter because an unstable mode can amplify them.
- The six cases classify early linear behaviour near a homogeneous equilibrium. They are not six finished animal-coat patterns.
- His examples include Hydra tentacles, leaf whorls, gastrulation, dappling, and phyllotaxis.
- He explicitly says that nonlinear development will require particular computational experiments using digital computers.

The opening excerpt reproduced earlier is also a concise statement of modelling humility: a model is a simplification, and the modeller must decide which features are important enough to retain.
"""
)

new_ids = {
    "week03-turing-model-excerpt",
    "week03-turing-reference-list",
    "week03-turing-reception-reader",
}
cells[:] = [cell for cell in cells if cell.get("id") not in new_ids]

question_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f")
new_cells = [
    markdown_cell(
        "week03-turing-model-excerpt",
        """## A model is a deliberate simplification

<img src="images/Turing_1952_quote.png" alt="Turing describes the embryo model as a simplification and idealisation" style="display:block;width:86%;max-height:205px;object-fit:contain;margin:0.5rem auto 0.8rem;">

Turing begins by stating what the model will leave out. The question is whether the retained features capture the mechanism that matters.

<p class="figure-reference">Turing (1952), opening of Section 1.</p>
""",
        ["slides"],
        "slide",
    ),
    markdown_cell(
        "week03-turing-reference-list",
        """## A remarkably short reference list

<div class="two-panel image-wide compact-panels">
  <div class="image-panel"><img src="images/TuringReferences.png" alt="The six references in Turing's 1952 morphogenesis paper" style="width:100%;height:245px;object-fit:contain;"></div>
  <div class="text-panel"><p><strong>Six references.</strong></p><p>Five are books. The only journal paper is Michaelis and Menten’s work on enzyme kinetics.</p><p>The list gives a sense of how little established reaction–diffusion biology Turing had to cite.</p></div>
</div>

<p class="figure-reference">Reference list from Turing (1952).</p>
""",
        ["slides"],
        "slide",
    ),
    markdown_cell(
        "week03-turing-reception-reader",
        """## From an unusual proposal to a modern framework

The paper was not entirely unnoticed. The embryologist C. H. Waddington corresponded with Turing about biological applications. Even so, it was largely neglected for several decades. Molecular genetics redirected much of developmental biology, direct chemical examples were scarce, and the proposed morphogens could not yet be identified experimentally.

That position has changed. Reaction–diffusion models are now a standard framework for studying spontaneous spatial pattern formation. Experimental support exists in chemical systems and in several developmental settings, including pigment patterns, hair and feather follicles, digits and mammalian palate patterning. A **Turing pattern** now has a precise meaning: a spatial pattern produced when diffusion destabilises a state that would remain uniform under the local reaction dynamics alone.

The qualification still matters. Reaction–diffusion is not the explanation for every biological pattern, and visual similarity to a simulated pattern is not evidence of the mechanism. Modern studies use the model to make experimentally testable claims about the molecules, interactions, transport rates and perturbations involved.

See Ball (2015), [“Forging patterns and making waves from biology to geology”](https://doi.org/10.1098/rstb.2014.0218), and Kondo (2022), [“The present and future of Turing models in developmental biology”](https://journals.biologists.com/dev/article/149/24/dev200974/286110/The-present-and-future-of-Turing-models-in).
""",
        ["reader-only"],
        "skip",
    ),
]
cells[question_index + 1:question_index + 1] = new_cells

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
