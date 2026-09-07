# MATH3024 teaching guide

This repository is the source of truth for the Unit Reader, lecture slides, and student workshops. The lecture notebook for each week is deliberately dual-purpose: tagged cells control what appears in the Reader, the projected deck, and the presenter's private notes.

## Weekly teaching rhythm

Use the same sequence whenever the topic permits:

1. **Hook:** an image, phenomenon, claim, or short demonstration.
2. **Predict:** students commit to an expectation before seeing the result.
3. **Model:** identify the system, abstraction, parameters, and update rules.
4. **Manipulate:** vary one meaningful choice and observe what changes.
5. **Discuss:** compare explanations, not merely outputs.
6. **Formalise:** introduce the mathematical language that compresses the observation.
7. **Transfer:** end with a new setting or an exit ticket.

The visual process map at the start of each chapter tells students which version of this rhythm the week uses.

## Notebook conventions

| Tag | Destination | Purpose |
|---|---|---|
| `slides` | Slides | A projected teaching beat |
| `slides-only` | Slides only | A spatially adapted duplicate or in-class instruction |
| `reader-only` | Reader only | Detail, derivation, context, or extended explanation |
| `presenter-notes` | Speaker view only | Timing, questions, misconceptions, and optional material |
| `hide-input` | Both outputs | Show a generated result without implementation detail |
| `hide-output` | Both outputs | Show code without a bulky or transient result |

Do not express destination rules with cell position or manual deletion. Tags are the contract used by the build scripts.

## Reusable visual components

The shared components live in `style.css` and are automatically copied into standalone slides:

- `reader-route`: the conceptual route shown at the start of a week;
- `reader-prompt`: an action, prediction, or discussion question;
- `reader-voice`: a short attributed voice or quotation;
- `reader-emphasis`: one conclusion worth visually pausing on.

Keep inline styling out of new notebook cells. The shared classes make light/dark mode and later redesigns manageable.

### Unit-wide slide grammar

All lecture decks use the Week 1 “Blue Period” format:

- one Baskerville/Georgia serif family for headings and teaching text;
- Arial/Helvetica only for quiet labels, attributions, captions, and interface elements;
- Picasso indigo `#1B2A4C` as the single primary ink colour;
- `#5A6685` for secondary labels and `#C7CEDC` for rules and boundaries;
- a white background, restrained lines, and no decorative coloured boxes;
- a minimal title slide containing the topic and `MATH3024 · Week N`;
- `reader-voice` for quotations, `discussion-marker` for live questions,
  `choice-marker` for assumptions, and `ladder-marker` only when the level of
  abstraction actually changes.

Figures are capped by the shared exporter styling so they fit the 1280 × 720
canvas. Captions and references use the smaller sans-serif role. If a slide
needs more than the shared cap allows, split the teaching beat rather than
shrinking all of its text.

### Course-generated figures

Python figures use `tools/figure_style.py` as their source of truth. The
standard roles are DejaVu Sans 15 pt body text, 18 pt figure titles, 16 pt axis
labels, 13 pt tick labels and 12.5 pt legends. Static figures are exported once
as SVG and reused by both the Reader and slides; do not maintain separate
Reader and slide versions of the same plot. SVG text is converted to vector
paths at export so that a browser cannot silently substitute a different font.
Animated figures use the same DejaVu Sans type roles and course colours, with
raster export only where animation requires it. HTML player controls may use
the browser's interface font, but text inside the animated figure must not.

Use Picasso indigo for axes and principal curves, blue for ordinary data,
orange for a contrasting collective quantity, yellow for a deliberately
highlighted observation, and pale blue for uncertainty. These combinations are
chosen to remain distinguishable without a red–green contrast.

- Keep the data region clear. Put a legend in unused whitespace or immediately
  above/below the axes; never cover a curve, title or annotation.
- A line and its uncertainty band must have separate, explicit meanings, such
  as “ensemble mean” and “±1 SD across 10 populations”.
- Avoid an internal figure title when the surrounding slide or Reader heading
  already supplies it. Put parameters in the surrounding caption unless they
  are needed to interpret the axes.
- Preserve individual runs faintly when an ensemble is small or potentially
  skewed. A summary must state its centre, spread and number of runs.
- Regenerate the shared SVG from its Python source. Do not repair the exported
  SVG by hand and do not edit generated `.slides.html` files.

### Non-negotiable slide constraints

- A projected slide must fit the 1280 × 720 canvas without vertical scrolling.
- Reveal hierarchy carries meaning: a horizontal move (right arrow) begins a genuinely new conceptual section; a vertical move (down arrow) develops, exemplifies, or calculates within the current section. Historical context, successive steps in one model, and worked detail should not become separate horizontal sections.
- Use one main teaching claim per slide. Move derivations, qualifications, and
  extended history to the Reader or presenter notes.
- A live question must not share a slide with its answer. Use a following slide
  when staged fragments are not being used.
- Use a table or equal-height cards for repeated comparisons. Body text inside
  figures, cards, and tables uses the shared compact role rather than ad hoc
  inline font sizes.
- The ladder points **up** when trajectories, states, runs, parameters, or
  spatial detail are compressed to reveal a broader relationship. It points
  **down** when returning to an individual, local update, grid cell, mechanism,
  or debugging example. A change of visual encoding alone is not a ladder move.
- Follow Victor's distinction between **controlling** a parameter and
  **abstracting over** it. Moving a slider and watching the same representation
  stays on one rung. Collecting results across the slider values into a response
  curve, phase diagram, or other relationship moves up. Likewise, running more
  seeds does not itself move up; replacing those runs by an ensemble summary
  does.
- Name each lost dimension when several upward moves are chained. A common
  sequence is individual histories → a collective time series → one summary per
  run → an ensemble summary at one condition → a response across conditions.
  Do not collapse this sequence into “up twice” merely because the final plot
  has two parameter axes.
- Put only one direction in a ladder marker. When an aggregate needs explaining,
  use a later down marker beside the individual run, component, or update that
  supplies that explanation.
- `choice-marker` labels an assumption or modelling decision;
  `discussion-marker` labels a genuine live prompt. Neither is decorative.
- Use lowercase symbols for fields and uppercase symbols for named chemical
  species. For Week 3, $U,V$ are species, $u(\mathbf x,t),v(\mathbf x,t)$ are
  concentration fields, and $u^n_{i,j},v^n_{i,j}$ are numerical values.
- Do not edit generated `.slides.html` files. Correct the notebook or shared
  stylesheet and regenerate the deck.

### Reader and slide heading hierarchy

Use headings to expose the argument rather than to label every teaching beat.

- Level-one headings are broad banners. Most weeks should need only four to
  seven. A useful default sequence is **Real-world motivation**,
  **Explorable**, **Model details**, **Analysis**, and **Scope and
  connections**.
- The Explorable usually comes before the formal model details. It is a
  scene-setting encounter with the phenomenon: students first notice what the
  system does, identify controls, and form questions. The later model section
  then explains what the explorable must contain. Do not turn the first
  encounter into an undocumented technical exercise.
- This sequence is a guide, not a compulsory template. Move the Explorable
  later when students need a small amount of model language before its controls
  are intelligible, or when it is being used to test a model already developed.
  A week may also omit a banner that does no genuine organisational work.
- Level-two headings contain the examples, concepts, model components, and
  calculations that develop one banner.
- Level-three headings are supporting detail within a level-two subsection.
- In slides, a level-one banner begins a horizontal section. Its level-two
  slides develop the argument vertically. Do not promote historical examples,
  successive equations, or individual analysis steps merely to obtain a new
  right-arrow move.
- Reader and slide headings should describe the same conceptual groups, even
  when the Reader contains extra level-three detail or reader-only sections.
- **Qualitative analysis** normally precedes **Quantitative analysis**: first
  establish what the behaviour looks like, then introduce the quantity that
  compresses or compares it.

The default is already expressed in different ways across the unit:

| Week | Scene-setting encounter | Why it appears where it does |
|---|---|---|
| 1 | Parable of the Polygons | encounter segregation before rebuilding the model |
| 2 | Weeds & Trees | follows only the minimal branching prompt needed to read its controls |
| 3 | Gray–Scott parameter space | follows Turing's question and the minimum reaction vocabulary |
| 4 | elementary CA and Game of Life Explorables | each follows the minimum local-rule language needed to interact meaningfully |
| 5 | Ising, XY, and moving-agent Explorables | motivate the move from spins to active agents before the Vicsek construction |
| 6 | Kuramoto Explorable | encounter phase organisation before deriving the Kuramoto equations |
| 7 | no single lecture Explorable | retain the motivation-to-model route; the workshop constructs PSO by extending familiar agent code |
| 8 | Barista's Secret | follows the minimum language of criticality, then motivates the percolation model and its analysis |
| 9 | no single canonical Explorable | demonstrations support particular information measures rather than defining a separate scene-setting section |
| 10 | no dedicated Explorable | begin from strategic situations and payoff choices before formal game analysis |

Later weeks should follow the same principle where an appropriate Explorable
exists. An interactive used for validation, sensitivity analysis, or parameter
measurement belongs under **Analysis**, not under the scene-setting banner.

## Canonical-model summaries

End each Reader topic with a short, consistently ordered summary headed
**Canonical model at a glance · [model name]**. Use the following fields where
they are meaningful:

1. **World** — the domain, topology and boundary conditions. State explicitly
   when the model has no physical spatial world rather than silently omitting it.
2. **State** — the variables required to describe the model at one instant.
3. **Initialisation** — how the starting state is chosen.
4. **Dynamics** — how one state evolves into the next.
5. **Interactions** — which components influence one another and how.
6. **Parameters** — the main quantities controlled by the modeller.
7. **Outputs** — the observables used to interpret the model.

Add one model-specific field only when it is genuinely useful, such as
**Stochastic choices**, **Numerical choices**, or **Stopping condition**. The
shared ordering is a scaffold for comparing models, not a demand that every
model be forced into an inappropriate spatial or agent-based description.

## Week 1 — Modelling complex systems

**Conceptual spine:** models are purposeful abstractions; local rules can produce unexpected collective outcomes.

Suggested live beats:

- Begin with the acknowledgement of Country and *Bilya Kaatajin* map. The complete wording is in presenter notes; do not improvise cultural interpretations of labels on the map.
- Allow 8–10 quiet minutes for the sealed “letter to your Week 12 self.” Mark completion only; do not read or assess the private contents. Store envelopes securely and schedule their return.
- Opening pulse: students choose what to keep and discard from a familiar system.
- Contrast Newton's orbital model with Schelling's segregation model.
- Ask for predictions before each Schelling simulation.
- Keep returning to agents, states, parameters, rules, and observables.
- Exit ticket: micro-level rule versus macro-level pattern.

Likely misconception: “A more detailed model is automatically better.” Ask which question the added detail helps answer and what it costs.

The workshop continues directly from the exit ticket by implementing and stress-testing the one-dimensional Schelling model.

The student workshop is `notebooks/week01/WS_Introduction_to_complex_systems.ipynb`.
It is self-contained and is the only Week 1 workshop file students need. The
maintenance script `tools/rebuild_week01_workshop.py` regenerates that notebook
with stable cell IDs, embedded visual markers, and cleared outputs. Run the
script after editing the workshop template, then execute a copied notebook from
a clean kernel before distribution. Do not distribute the rebuild script as a
student dependency.

Week 1 has no external runtime assets. Some legacy workshops from later weeks
still reference local images or data. Until each is made self-contained, package
the notebook with its required files and preserve their relative paths. No
`tools/rebuild_*.py` script is a student dependency.

## Week 2 — Fractals

**Conceptual spine:** measurement depends on scale, and dimension can be understood as a scaling exponent.

Suggested live beats:

- Begin with the Mandelbrot visual/song prompt, then collect predictions.
- Run the ruler-resolution thought experiment before naming the coastline paradox.
- Treat the Cantor set and Sierpiński triangle as the same question in different clothes: how many copies survive, and how much smaller is each?
- Compare recursion, iterated function systems, and L-systems as alternative descriptions of generation.
- Exit ticket: interpret the Cantor-set dimension between zero and one.

Likely misconception: “Fractal dimension is how visually complicated something looks.” Return to the measured scaling relationship and distinguish exact mathematical fractals from statistical natural ones.

The workshop is intentionally broad. Students should follow one generative route deeply before attempting extensions; completing every cell is not the goal.

## Week 3 — Reaction–diffusion

**Canonical model:** Gray–Scott reaction–diffusion. Random-walk diffusion is a
supporting model, not a second equal-weight canonical model.

**Modelling core:** diffusion as a change of representation. Reaction–diffusion
is the framework through which the representation problem is studied.

### Session 1 · How can a uniform system create a pattern?

- Use a compact gallery to separate visual resemblance from shared mechanism.
- Introduce Turing's biological question and general reaction–diffusion model.
- State the essential Turing condition: the homogeneous equilibrium is stable
  without diffusion and unstable to a spatial mode with unequal diffusion.
- Bridge explicitly from Turing's general framework to the concrete Gray–Scott
  canonical model.
- Explore the Gray–Scott parameter space. Do not imply that every Gray–Scott
  pattern is a classical Turing pattern.

### Session 2 · Which representation should we compute?

- Move from individual random walks to ensemble spreading and concentration
  fields, then down to a numerical grid.
- Keep the particle-level story conceptually real but computationally distinct
  from the concentration-field simulation.
- Pause at one Laplacian stencil and one Euler update before generalising.
- End by revisiting what each representation preserves and hides.

Turing's wider life belongs in the Reader. Slides retain only enough historical
context to motivate the assessable mechanism. The workshop supplies correct
baseline code and asks students to test, refine, measure, and interrogate it.

## Before teaching or publishing

1. Run all code cells from a clean kernel where practical.
2. Check that every local image path resolves and every externally sourced image has attribution.
3. Generate slides with `generate_slides.sh` and serve them with `present_slides.sh`.
4. Confirm videos through the served slide deck, not through a `file://` URL.
5. Verify the Reader through `build_reader.sh` only after committing notebook work; that script temporarily strips slide-only cells and restores notebooks from Git.
6. Scan presenter notes for dates, LMS directions, room-specific comments, and material marked optional.

## Extending the template

`tools/rebuild_getting_started.py` is the source template for the Week 0 student
onboarding chapter. Re-run it after changing that chapter's structure or
wording, then verify the generated notebook from a clean kernel.

Run `python tools/refresh_weeks_01_02.py` only to reproduce the Week 1–2 baseline components. It is idempotent and uses stable cell IDs. For later weeks, copy the component structure and teaching rhythm rather than adding those topics to this migration script.

Run `python tools/standardise_lecture_decks.py` after importing or substantially
editing lecture notebooks from Weeks 2–10. It normalises title metadata,
converts legacy quote and discussion markup, supplies missing Markdown image
descriptions, and distributes the shared marker assets. It does not rewrite
topic content or execute code.

Afterwards regenerate the relevant deck with `generate_slides.sh`. That script
injects the current unit-wide typography and component rules from `style.css`,
so generated HTML should not be edited by hand.

The TCSG light-mode logo is produced non-destructively from the supplied original with `tools/prepare_tcsg_logo.py`; the original JPEG remains available as provenance.
