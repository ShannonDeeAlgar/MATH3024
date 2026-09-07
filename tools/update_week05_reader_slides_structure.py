import json
from pathlib import Path


path = Path("notebooks/week05/L_ABM.ipynb")
notebook = json.loads(path.read_text())
cells = notebook["cells"]


def source(cell):
    return "".join(cell.get("source", []))


def find(prefix):
    for cell in cells:
        if source(cell).lstrip().startswith(prefix):
            return cell
    raise ValueError(f"Missing cell beginning {prefix!r}")


def set_source(cell, text):
    cell["source"] = text.splitlines(keepends=True)


# Remove two slide-only interruptions. Retain their useful ideas in the surrounding
# Reader prose without creating extra top-level headings.
already_agents = find("# We have already used agents")
cells.remove(already_agents)
self_organisation = find("## What is self-organisation?")
cells.remove(self_organisation)

reader_intro = find("Agent-based modelling is useful")
set_source(
    reader_intro,
    """Agent-based modelling is useful when individuals remain distinguishable and their locations, attributes, decisions, or interaction partners matter. An agent has agency in the modelling sense: its next action depends on its own state and locally available information. This need not imply conscious choice. A self-propelled particle has an effectively available energy supply, whereas a person, animal or robot may follow goals and hierarchical decision rules.\n\nIt is not automatically the best description. The modelling question determines whether individual variation should be retained or averaged away.\n\nThis week uses collective motion to define agents and their environment, inspect one update, choose a system-level observable, sweep a parameter, and repeat across random runs.\n""",
)

crowd_reader = find("Franklin's hundredth goal")
set_source(
    crowd_reader,
    """Franklin's hundredth goal establishes the modelling problem: coordinated system-level motion can arise without a central controller, while congestion, social cues, goals and boundaries still matter.\n\n**Self-organisation** occurs when interactions among lower-level components produce a global spatial, temporal or functional pattern without a central controller specifying that pattern. External driving and constraints may still be essential: the crowd has a field and a milestone; a flock has an environment; active matter consumes energy.\n\nAt the microscopic level we could record positions, headings, neighbours and decisions. At the macroscopic level we see a surge, a stream or a jam. An agent-based model keeps enough of the first description to ask how the second emerges.\n""",
)

starling_context = find("Mathematically, “flocking”")
set_source(
    starling_context,
    """Mathematically, “flocking” is used more broadly than its biological collective noun. It can describe coherent local motion in fish, bacteria, cells, robots and synthetic active matter. The shared observation is ordered movement; the mechanism must still be established for each system.\n\nEuropean starlings in North America descend in part from nineteenth-century releases, including birds released by Eugene Schieffelin in Central Park in 1890 and 1891. The familiar claim that he wanted to introduce every bird mentioned by Shakespeare is a later story for which historians have found no contemporary evidence. North American starlings also form murmurations; there is no good basis for a continent-wide claim that they do not swirl in the way European flocks do.\n\nWestern Australia works hard to prevent invasive starlings from establishing, while native budgerigars provide a striking local example of collective motion.\n\n<p class=\"media-credit\">Sources: Folger Shakespeare Library, <a href=\"https://www.folger.edu/blogs/collation/murmuration-shakespeare-in-flight/\">“Murmuration: Shakespeare in Flight”</a>; Cornell Lab of Ornithology, <a href=\"https://www.allaboutbirds.org/guide/European_Starling/overview\">European Starling overview</a>.</p>\n""",
)

overview = find("# One phenomenon, three modelling purposes")
set_source(
    overview,
    """# Three modelling purposes\n\n| Route | Motivation | What counts as success? |\n|---|---|---|\n| A · Reynolds (1987) | Computer graphics | Local rules produce controllable, believable motion. |\n| B · Vicsek et al. (1995) | Statistical physics | A minimal model exposes collective order and its transition. |\n| C · Couzin et al. (2002) | Behavioural biology | Assumptions connect to observations, mechanisms and function. |\n\nThe question determines what the model retains and how it should be analysed. We use Vicsek because it isolates alignment and noise most simply.\n""",
)

short_bridge = find("Craig Reynolds introduced boids")
set_source(
    short_bridge,
    """The following examples use similar-looking collective motion to ask three different questions: can local rules make motion believable, can a minimal interaction generate an ordered phase, and which local behaviours explain observations of real groups?\n""",
)

long_explanation = find("### Motivation changes the model")
cells.remove(long_explanation)

graphics = find("## Computer graphics")
set_source(graphics, source(graphics).replace(
    "## Computer graphics · make motion believable",
    "## A · Computer graphics — Reynolds (1987)",
    1,
))

physics = find("# Statistical physics")
set_source(physics, source(physics).replace(
    "# Statistical physics · isolate collective order",
    "## B · Statistical physics — Vicsek et al. (1995)",
    1,
))

ising = find("## From Ising")
moving = find("## Let the orientations")
moving_spin = find("## A moving spin model")
heisenberg = find("### What does the Heisenberg")
for cell in [ising, moving, moving_spin]:
    set_source(cell, source(cell).replace("## ", "### ", 1))

biology = find("## Behavioural and applied models")
biology_text = source(biology).replace(
    "## Behavioural and applied models · explain local decisions",
    "## C · Behavioural biology — Couzin et al. (2002)",
    1,
)
biology_text = biology_text.replace(
    "<h3>Hanoi traffic</h3>",
    "<h3>From animal decisions to Hanoi traffic</h3>",
).replace(
    "<p>Dense motion can remain flowing even when lanes and central control are weak. Drivers respond to nearby vehicles, gaps, expected motion and collision risk.</p>",
    "<p>Couzin's repulsion, alignment and attraction zones turn behavioural hypotheses into testable group-level predictions. The same agent-based approach extends to people and vehicles, although their perception, goals and rules differ.</p><p>Dense Hanoi traffic can remain flowing even when lanes and central control are weak. Drivers respond to nearby vehicles, gaps, expected motion and collision risk.</p>",
)
set_source(biology, biology_text)

applied = find("### Behavioural and applied explorables")

# Place the three routes in their labelled order: Reynolds, Vicsek, Couzin.
route_cells = [graphics, physics, ising, moving, moving_spin, heisenberg, biology, applied]
for cell in route_cells:
    cells.remove(cell)
insert_after = cells.index(short_bridge) + 1
cells[insert_after:insert_after] = route_cells

# Use the established Reader/slide quotation treatment.
set_source(
    moving_spin,
    """### A moving spin model

<div class="reader-voice">
  <div class="reader-voice-quote">...I had designed the moving version of the Heisenberg model.</div>
  <div class="reader-voice-attr">Tamás Vicsek (2016)</div>
</div>

Fixed orientations become self-propelled particles whose interaction partners change as they move.

<p class="media-credit">Vicsek, T. (2016), <a href="https://www.nature.com/articles/529016a">“Universality in non-equilibrium systems”</a>, <em>Nature</em> 529, 16–17.</p>
""",
)

# Present model reduction as two compact statements instead of two competing columns.
build = find("# Build the Vicsek model")
set_source(
    build,
    """# Build the Vicsek model

Vicsek and colleagues asked what happens when self-propelled particles align with nearby particles while noise perturbs their headings.

- **Retain:** positions, headings, local neighbours and noise.
- **Remove:** aerodynamics, body shape, vision, memory, leadership and attraction.

The model isolates local alignment as a possible mechanism for collective motion.
""",
)

ingredients = find("## What goes into an agent-based model?")
set_source(ingredients, source(ingredients).replace("## What goes", "# What goes", 1))
ingredients.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "slide"

history = find("# History can matter")
history.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "slide"

# Keep the two implementations and their physical interpretations, while defining
# every symbol needed to read the vectorial expression.
noise = find("## Where is the noise added?")
set_source(
    noise,
    r"""## Where is the noise added?

<div class="two-panel equal-panels compact-panels">
<div class="text-panel">
<h3>Angular noise</h3>

$$
\theta_i'=\bar\theta_i+\xi_i,
\qquad \xi_i\sim U[-\eta/2,\eta/2].
$$

The agent estimates the local mean heading $\bar\theta_i$, then makes a turning error. This represents uncertainty in executing a chosen direction.
</div>
<div class="text-panel">
<h3>Vectorial noise</h3>

$$
\theta_i'=\operatorname{Arg}\!\left(\mathbf m_i+\eta n_i e^{\mathrm i\chi_i}\right).
$$

$\mathbf m_i=\sum_{j\in\mathcal N_i}e^{\mathrm i\theta_j}$ is the local heading signal, $n_i$ is the neighbour count, and $\chi_i$ is a random direction. This represents noise in sensing or in the local force before a direction is chosen.
</div>
</div>

Both implementations are defensible, but they describe uncertainty entering at different points in the mechanism.
""",
)

# Replace the text-only contrast with the published finite-system comparison.
transition = find("## Why did the transition debate matter?")
set_source(
    transition,
    """## Continuous or discontinuous?

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/pimentel_2008_noise_transitions.png" alt="Order parameter against noise for angular and vectorial noise conventions"></div>
<div class="text-panel">
<p><strong>(a) Angular noise:</strong> the finite simulation appears smooth.</p>
<p><strong>(b) Vectorial noise:</strong> the order parameter shows a clear jump.</p>
<p>The curves are evidence about these implementations and this finite system, not a universal verdict. Larger angular-noise simulations can also reveal discontinuity and travelling bands.</p>
</div>
</div>

<p class="media-credit">Pimentel et al. (2008), <a href="https://arxiv.org/abs/0802.3879">“Intrinsic and extrinsic noise effects on the phase transition of swarming systems and related network models”</a>, Fig. 1. $N=20{,}000$, $L=32$, $R=0.4$, $v=0.05$.</p>
""",
)

# Add the comparison paper to the single consolidated reference list.
references = find("# References")
reference_text = source(references)
if "Pimentel" not in reference_text:
    reference_text = reference_text.replace(
        "- Grégoire, G. and Chaté, H. (2004)",
        "- Pimentel, J. A., Aldana, M., Huepe, C. and Larralde, H. (2008), [“Intrinsic and extrinsic noise effects on the phase transition of swarming systems and related network models”](https://arxiv.org/abs/0802.3879), *Physical Review E* 77, 061138.\n- Grégoire, G. and Chaté, H. (2004)",
        1,
    )
set_source(references, reference_text)

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
