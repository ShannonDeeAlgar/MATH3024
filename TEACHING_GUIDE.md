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
