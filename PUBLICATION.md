# Publication boundary

This update includes Weeks 1–8, Getting Started, the welcome page and glossary.
It includes the revised practice answers and workshops. Weeks 9–10 remain
outside the publication boundary.

The public Reader currently stops at Week 8. Local previews retain all weeks.
The deployment workflow runs `tools/prepare_publication.py` in its disposable
CI checkout before rendering. It removes later-week entries and directories
there, so slide staging cannot accidentally publish them. The script refuses
to run in a normal local session. Change `MAX_WEEK` only when another week is
explicitly cleared for publication.

## Release checks

Review the selected changes before committing; the authoring checkout also
contains unrelated work. In particular, include the new figure assets:

- `notebooks/week07/images/aco_tsp_benchmark.svg`
- `notebooks/week07/images/aco_tsp_progress.svg`
- `notebooks/week07/images/pso_single_swarm.svg`
- `notebooks/week07/images/pso_ensemble.svg`
- `notebooks/week07/images/pso_population_evaluation_progress.png`

Include the modified notebook, regenerated deck and figures, their generators,
shared styles, requirements and deployment workflow, plus the build/check
helpers they reference. Some helpers are new files, notably
`course_python.sh`, `execute_notebook.py`, `check_equation_consistency.py`,
`equation_consistency.json`, `test_equation_consistency.py`,
`test_week07_presentation.py` and `prepare_publication.py` in `tools/`.
`check_publication_assets.py` verifies the final site, including the repository
URL prefix and both trailing-slash forms of the Reader route.

Run the equation check, equation tests, Week 7 presentation tests and Week 8
preparation and instructor checks. Rebuild all released lecture decks from a
fresh kernel, then build the Reader and check its references and publication
assets. Inspect the rendered pages and slides for maths rendering and layout.
