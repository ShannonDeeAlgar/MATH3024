"""Place the synchronisation taxonomy beside its figures and before phase reduction."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def lines(text):
    return text.splitlines(keepends=True)


nb = json.loads(PATH.read_text())
cells = nb["cells"]
by_id = {cell.get("id"): cell for cell in cells}

reader = by_id["w6-types-of-synchronisation-reader"]
reader["metadata"] = {"tags": ["reader-only"], "slideshow": {"slide_type": "skip"}}
reader["source"] = lines(r'''## Several forms of synchronisation

The phase-circle snapshot and the adjoining time series show the same oscillators in two representations.

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(430px,1fr));gap:1rem;margin:1rem 0">
  <div style="display:flex;align-items:center;gap:1rem"><img src="images/synchronisation_types/in_phase.svg" alt="In-phase oscillators" style="width:48%;min-width:210px"><p><strong>In-phase synchronisation:</strong> phases coincide, so their difference is (0) modulo (2\pi).</p></div>
  <div style="display:flex;align-items:center;gap:1rem"><img src="images/synchronisation_types/anti_phase.svg" alt="Anti-phase oscillators" style="width:48%;min-width:210px"><p><strong>Anti-phase synchronisation:</strong> two oscillators remain half a cycle apart, with phase difference (\pi).</p></div>
  <div style="display:flex;align-items:center;gap:1rem"><img src="images/synchronisation_types/phase_locked.svg" alt="Phase-locked oscillators" style="width:48%;min-width:210px"><p><strong>Phase locking:</strong> phase differences remain constant. The constant need not be (0) or (\pi).</p></div>
  <div style="display:flex;align-items:center;gap:1rem"><img src="images/synchronisation_types/frequency_entrained.svg" alt="Frequency-entrained oscillators" style="width:48%;min-width:210px"><p><strong>Frequency entrainment:</strong> oscillators share a long-time average frequency, although their phase difference may fluctuate.</p></div>
  <div style="display:flex;align-items:center;gap:1rem"><img src="images/synchronisation_types/two_clusters.svg" alt="Two synchronised clusters" style="width:48%;min-width:210px"><p><strong>Cluster synchronisation:</strong> subsets lock internally while different clusters retain different phases or rates.</p></div>
  <div style="display:flex;align-items:center;gap:1rem"><img src="images/synchronisation_types/partial_synchrony.svg" alt="Partial synchronisation" style="width:48%;min-width:210px"><p><strong>Partial synchronisation:</strong> a locked group coexists with drifting oscillators.</p></div>
  <div style="display:flex;align-items:center;gap:1rem"><img src="images/synchronisation_types/chimera_like.svg" alt="Chimera-like synchronisation" style="width:48%;min-width:210px"><p><strong>Chimera state:</strong> coherent and incoherent subsets persist together. Classic chimeras usually need spatially organised or non-local coupling.</p></div>
</div>

**Generalised synchronisation:** the states maintain a stable functional relationship

$$
\mathbf y(t)=F\!\left(\mathbf x(t)\right),
$$

without requiring equal states or equal observable signals. Complete synchronisation, (\mathbf y=\mathbf x), and projective synchronisation, (\mathbf y=a\mathbf x), are special cases. A relationship such as (y(t)=\sin(x(t))) counts only when the coupled dynamics establish and maintain it.
''')

# The old Reader-only composite image is now redundant.
cells[:] = [cell for cell in cells if cell.get("id") != "sync-types-reader"]


def move_before(cell_id, target_id):
    cell = next(cell for cell in cells if cell.get("id") == cell_id)
    cells.remove(cell)
    target = next(i for i, item in enumerate(cells) if item.get("id") == target_id)
    cells.insert(target, cell)


# Slides and Reader tell the same story: recognise the possible relationships,
# then reduce the two-oscillator equations to their relative phase.
move_before("sync-types-slide", "w6-relative")
move_before("w6-types-of-synchronisation-reader", "phase-difference")

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Updated {PATH.relative_to(ROOT)}")
