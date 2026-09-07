# MATH3024 course audit checklist

This file records the remaining curriculum work across the Reader, lecture
slides, and workshops. It complements `TEACHING_GUIDE.md`:

- the teaching guide records reusable standards and settled design rules;
- this checklist records week-specific diagnoses, decisions, and completion.

Do not copy detailed formatting rules into this file. When a local correction
reveals a reusable rule, add that rule to the teaching guide and link to it here.

## Unit-wide release checks

- [ ] The Reader, slides, and workshop tell the same central story for each week.
- [ ] Reader and slide section headings use the same wording where the content is the same.
- [ ] Core, optional, and project-extension material are visibly distinguished.
- [ ] Each simulated model states its world or network, state, initialisation,
      parameters, numerical update, boundary treatment, stopping rule, and outputs.
- [ ] Each workshop contains a clearly labelled pseudocode section whose form is
      natural for that week's model and sufficiently complete to reproduce it.
- [ ] Ladder markers appear only when the represented object or level of summary changes.
- [ ] Figures and animations use the shared course typography and colour system.
- [ ] Every ensemble summary states its centre, spread, and number of runs.
- [ ] Slides fit the 1280 x 720 canvas without scrolling.
- [ ] Generated outputs are rebuilt from source; no stale notebook images are released.
- [ ] Local Reader slide links open local uncommitted slides; published links open GitHub Pages.
- [ ] Canonical notebooks parse, execute from a clean kernel, and have no missing assets.
- [ ] Only intended weeks and generated assets are staged for release.

## Week-by-week work

| Week | Settled curriculum decision | Main remaining work | Status |
|---|---|---|---|
| 0 | Orient students to the weekly model and the second modelling-practice curriculum. | Add the unit map and the minimum reproducibility requirements for pseudocode. | Pending |
| 1 | Schelling is the canonical model; seeds and reproducibility are the modelling focus. | Tighten the Reader and identify an essential first-workshop route. | Pending |
| 2 | Fractal construction and finite scaling evidence form one story; scaling-range choice belongs here. | Reduce scope, remove duplicate hierarchy, and make transformations explicit in pseudocode. | Pending |
| 3 | Gray-Scott is canonical; particle, field, PDE, and grid are successive representations. | Remove remaining repetition and strengthen the analysis of simulated patterns. | Pending |
| 4 | Elementary CA and Game of Life are both retained; computational budget is the modelling focus. | Organise the several analysis methods into one escalating sequence. | Pending |
| 5 | Vicsek is canonical; noise implementation is the modelling focus. | Protect the ABM core and visibly tier finite-size and transition-order extensions. | Pending |
| 6 | Kuramoto is canonical; heterogeneity is the modelling focus. | Keep the lean workshop route stable while the remaining Reader/slide audit is completed. | In progress |
| 7 | PSO is canonical; fair, reproducible comparison of stochastic algorithms is the modelling focus. | Keep supplied baseline checks as scaffold and centre student decisions on the ensemble experiment. | Pending |
| 8 | Sandpile is canonical; percolation is the tuned contrast; borrowing and validating code is the modelling focus. | Rebuild the Reader/slide narrative and align the workshop around validation. | In progress |
| 9 | This is a measurement week, not a canonical-model week. | Build one coherent worked analysis and complete the workshop ending. | Pending |
| 10 | Prisoner's Dilemma is the canonical game; repeated play and evolutionary population updating extend it. | Complete the Reader/slide audit around the newly consolidated pathway. | In progress |

## Week 8 acceptance checklist

### Reader and slides

- [x] Open with a concrete event or system in which behaviour spans several scales.
- [x] Introduce percolation as a system that becomes critical when a parameter is tuned.
- [x] Define correlation length/time and scale language only when the percolation evidence needs them.
- [x] Use the Ising model as brief supporting context, not a third model to develop.
- [x] State the contrast explicitly: percolation is tuned; the sandpile is slowly driven and self-organises.
- [x] Name the Abelian sandpile as the canonical model.
- [x] Introduce the code-reuse question immediately before the sandpile implementation.
- [x] State that borrowing referenced code is normal; the substantive question is whether the borrowed implementation is valid for the present model and claim.
- [x] Present sandpile qualitative behaviour before its quantitative observables.
- [x] Organise quantitative analysis as space, events, and time without repeating definitions.
- [x] Explain cutoffs, finite systems, and defensible scaling ranges before fitting a power law.
- [x] Move renormalisation/forest-fire material to a clearly optional Reader extension or remove it from the core lecture route.
- [ ] Remove duplicated headings, stray dropdowns, and code-output scaffolding from the Reader.
- [x] Keep slides to the core comparison and sandpile evidence; extended derivations remain Reader-only.

### Workshop

- [x] Context names both the sandpile model and code validation as the two workshop objectives.
- [x] Specify the complete model before implementation.
- [x] Pseudocode uses a queue or explicit relaxation waves and includes boundaries, dissipation, stopping, and recorded avalanche quantities.
- [x] Validate toppling, grain accounting, boundary loss, and order independence before running the full model.
- [x] Show why genuinely slow driving takes time to reach an active regime.
- [x] Provide the defensible fast-start alternative: create an overfull configuration, relax it, then use the stable state as the starting condition.
- [x] Animate at least one avalanche with an inspectable student-level animation.
- [x] Analyse avalanche size and duration across repeated grain additions.
- [x] Treat finite-size comparison and scaling-range selection as analysis choices, not automatic proof of criticality.
- [x] End with a short validation record students could reuse in a project.

## Week 6 workshop acceptance checklist

- [x] Keep one runnable route through specification, simulation, coherence, a coupling sweep, repeated runs, and a heterogeneity-width experiment.
- [x] Remove polished figures that simply reproduce Reader or slide outputs.
- [x] Move alternative phase, flashing, and network representations into the Reader's qualitative-analysis discussion.
- [x] Retain the warning that low global coherence can conceal two coherent groups, but make it an interpretation question rather than another simulation branch.
- [x] Move adaptive networks, heterogeneous responsiveness, distribution shape, and spatial motion into optional extension choices.
- [x] Replace generic workshop language such as “a compact toolkit” with direct instructions tied to the actual comparison.
- [ ] Recheck the rendered Reader and slide placement of the newly consolidated qualitative representations.

## Decision log

- **2026-08-26:** Use a checklist for outstanding work and keep reusable rules in
  `TEACHING_GUIDE.md`.
- **2026-08-26:** Week 8 uses percolation as a tuned comparison and the Abelian
  sandpile as the canonical model.
- **2026-08-26:** Week 8's modelling-practice focus is borrowing, inspecting,
  testing, and validating existing code—not asking whether borrowing code is
  permissible when it is properly acknowledged.
- **2026-08-26:** Week 6's Workshop is an investigation of coupling and
  heterogeneity, not a second copy of the lecture. Polished alternative
  representations belong in the Reader; model changes belong in the Workshop
  only when students use them to answer a comparison question.
- **2026-08-26:** Week 10 has one canonical game, the Prisoner's Dilemma.
  Repeated play supplies history-dependent strategies and the evolutionary
  update changes their population frequencies; neither is a competing
  canonical model.
