import json
from pathlib import Path


path = Path("notebooks/week05/L_ABM.ipynb")
notebook = json.loads(path.read_text())

for cell in notebook["cells"]:
    source = "".join(cell.get("source", []))

    if source.startswith("## C · Behavioural biology — Couzin et al. (2002)"):
        replacement = '''## C · Behavioural biology — Couzin et al. (2002)

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://www.youtube.com/embed/LzjifmHavAQ" title="Self-organised traffic in Hanoi" style="width:100%;height:300px;border:0;" allowfullscreen></iframe></div>
<div class="text-panel">
<h3>Explain local decisions</h3>
<p><strong>Model:</strong> repulsion, alignment and attraction encode behavioural hypotheses.</p>
<p><strong>Test:</strong> compare predicted group shape, movement and sorting with observations.</p>
<p>People and vehicles are also agents, but require different perception and decision rules.</p>
</div>
</div>

<p class="media-credit">Video: Yoav Ben-Dov, “Self-organization in Hanoi traffic”.</p>
'''
        cell["source"] = replacement.splitlines(keepends=True)

    if source.startswith("## Where is the noise added? · vectorial noise"):
        replacement = r'''## Where is the noise added? · vectorial noise

$$
\theta_i'=\operatorname{Arg}\!\left(\mathbf m_i+\eta n_i e^{\mathrm i\chi_i}\right),
\qquad
\mathbf m_i=\sum_{j\in\mathcal N_i}e^{\mathrm i\theta_j}.
$$

<table style="table-layout:fixed;width:100%;">
<colgroup><col style="width:28%;"><col style="width:72%;"></colgroup>
<thead><tr><th>Symbol</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>$\mathbf m_i$</td><td>local alignment signal</td></tr>
<tr><td>$n_i$</td><td>number of neighbours</td></tr>
<tr><td>$\eta$</td><td>relative noise strength</td></tr>
<tr><td>$\chi_i\sim U(0,2\pi)$</td><td>random direction</td></tr>
</tbody>
</table>

**Interpretation:** noise perturbs the sensed alignment signal before the agent chooses its direction.
'''
        cell["source"] = replacement.splitlines(keepends=True)

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
