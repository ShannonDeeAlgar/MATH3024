# Publication boundary

This branch updates Week 7 and its required shared support only. Earlier-week
lecture notebooks/decks remain at the published versions. The workflow rebuilds
Week 7 slides; its equation manifest explicitly covers that week.

The public Reader currently stops at Week 7. Local previews retain all weeks.
The deployment workflow runs `tools/prepare_publication.py` in its disposable
CI checkout before rendering. It removes later-week entries and directories
there, so slide staging cannot accidentally publish them. The script refuses
to run in a normal local session. Change `MAX_WEEK` only when another week is
explicitly cleared for publication.

## Week 7 release check

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

Run the equation check and both test files, then inspect the rebuilt Reader
and slides. Tests check figure numbering, asset existence and source structure;
browser inspection remains necessary for maths rendering and layout.
