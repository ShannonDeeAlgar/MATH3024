from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def find_cell(nb, cell_id):
    return next(cell for cell in nb.cells if cell.get("id") == cell_id)


def main():
    nb = nbformat.read(NOTEBOOK, as_version=4)

    # Session 1 remains entirely at particle level. The field equation belongs
    # after the deliberate change of representation in Session 2.
    nb.cells = [
        cell for cell in nb.cells
        if cell.get("id") != "week03-random-motion-laplacian-bridge"
    ]

    apparent_model = find_cell(nb, "week03-lowercase-full-model")
    apparent_model.source = '''## Particle-level ingredients and controls

At this stage, read the explorable as a story about particles that move, meet, react, enter and leave.

<div class="analysis-perspectives four">
  <div><strong>Move</strong><p><i>D</i><sub><i>u</i></sub> and <i>D</i><sub><i>v</i></sub> control how rapidly the two particle species spread.</p></div>
  <div><strong>React</strong><p><i>u</i> + 2<i>v</i> → 3<i>v</i>: encounters create one additional <i>v</i>.</p></div>
  <div><strong>Feed</strong><p><i>f</i> controls how rapidly fresh <i>u</i> enters from the reservoir.</p></div>
  <div><strong>Kill</strong><p><i>k</i>, together with outflow, controls how rapidly <i>v</i> is removed.</p></div>
</div>

<p class="small-note">The feed and kill controls are needed because this is an open reactor. They maintain the supply of reactant and prevent product from accumulating indefinitely.</p>'''

    explorable = find_cell(nb, "54e20377-5977-4ea6-a97b-7482a438a6c9")
    explorable.source = explorable.source.replace(
        "So far our explanation has been entirely particle-level: particles move, meet, react, enter and leave.",
        "Use the controls as particle-level ideas for now: spreading, reaction, supply and removal. The next session asks what the simulation must actually store.",
    )

    nbformat.write(nb, NOTEBOOK)


if __name__ == "__main__":
    main()
