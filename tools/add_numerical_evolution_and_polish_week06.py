"""Make numerical evolution explicit across the unit and finish Week 6 figures."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


READER_NOTES = {
    1: r"""### Numerical evolution

One numerical update selects an agent, checks its local neighbourhood and moves it only if the stated rule requires a move. Because the implementation is asynchronous, later agents in a sweep can encounter a world already changed by earlier updates. One sweep means $N$ attempted updates, where $N$ is the number of agents; it is a bookkeeping convention rather than physical time.

""",
    2: r"""### Numerical evolution

Here an iteration is a construction step, not elapsed physical time. One generation applies the stated replacement or contraction rule to the current geometry. Increasing the number of generations reveals finer scales while also increasing the number of stored pieces or points.

""",
    3: r"""### Numerical evolution

One numerical step computes both concentration fields at time $n+1$ from the two fields at time $n$. The old arrays are retained until every reaction and diffusion term has been evaluated, then both arrays are replaced together. The time represented by one step is $\Delta t$.

""",
    4: r"""### Numerical evolution

One time step applies the local rule once to every cell. The update is synchronous: every new state is calculated from the same old configuration, then the complete row or lattice is replaced. Updating cells in place would define a different cellular automaton.

""",
    5: r"""### Numerical evolution

One step first calculates every new heading from the positions and headings at time $n$, including the chosen noise convention. All agents then move using those new headings. The update is synchronous; changing that order changes the model.

""",
    6: r"""### Numerical evolution

The differential equation is continuous, but the simulation advances in finite steps. With forward Euler, all phase rates are calculated from $\boldsymbol\theta^n$, then

$$
\theta_i^{n+1}=\left[\theta_i^n+\Delta t\left(\omega_i+\frac{K}{N}\sum_j\sin(\theta_j^n-\theta_i^n)\right)\right]\bmod 2\pi.
$$

The examples use $\Delta t=0.02$ unless stated otherwise. A rendered animation frame may combine several numerical steps; frame rate and integration step are not the same quantity.

""",
    7: r"""### Numerical evolution

One PSO iteration evaluates the current positions, updates personal and shared best records, calculates every new velocity and then moves every particle. The iteration order, boundary treatment and moment at which the shared best is updated must be stated because each can change the search.

""",
    8: r"""### Numerical evolution

The sandpile contains two nested update scales. A driving step adds one grain. That addition can trigger many local topplings, which continue until every site is stable; the complete relaxation is one avalanche. Here avalanche duration counts parallel relaxation steps, and the convention must be stated.

""",
    9: r"""### Numerical evaluation

Shannon entropy is not itself a dynamical model. The computation starts from a stated probability distribution, or from counts used to estimate one, and returns a summary. When entropy is evaluated in successive windows of a time series, the window index belongs to the data-analysis procedure rather than to an entropy update rule.

""",
    10: r"""### Numerical evolution

One generation first lets agents play the specified encounters and accumulate payoffs. Selection then uses those payoffs to form the next population, after which mutation may alter inherited strategies. Payoffs must be completed before generational replacement unless an explicitly asynchronous evolutionary process is intended.

""",
}


WORKSHOP_NOTES = {
    1: "**Numerical evolution:** one sweep is $N$ asynchronous update attempts. Record whether order within a sweep is randomised.",
    2: "**Numerical evolution:** one iteration is one geometric construction generation, not a unit of physical time.",
    3: r"**Numerical evolution:** calculate both new concentration arrays from the same old arrays, then replace them together; one step represents $\Delta t$.",
    4: "**Numerical evolution:** one synchronous step applies the rule to every cell from the same previous configuration.",
    5: "**Numerical evolution:** calculate all new headings first, then move all agents. Changing that order changes the model.",
    6: r"**Numerical evolution:** calculate all phase rates from the current phases, then advance every phase by $\Delta t$ and wrap modulo $2\pi$. Rendering frames is separate from integration.",
    7: "**Numerical evolution:** evaluate positions, update memory, calculate velocities and then move. State exactly when the shared best is refreshed.",
    8: "**Numerical evolution:** distinguish slow driving from fast relaxation. Add one grain, topple until stable and record that complete cascade as one avalanche.",
    9: "**Numerical evaluation:** entropy maps a distribution or estimated set of frequencies to a number; there is no model-time update unless the source data themselves evolve.",
    10: "**Numerical evolution:** complete interactions and payoffs before selection, replacement and mutation form the next generation.",
}


def lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def save(path: Path, notebook: dict) -> None:
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


def markdown(text: str, cell_id: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": lines(text.rstrip() + "\n"),
    }


def lecture_path(week: int) -> Path:
    return sorted((ROOT / f"notebooks/week{week:02d}").glob("L_*.ipynb"))[0]


def workshop_path(week: int) -> Path:
    return sorted((ROOT / f"notebooks/week{week:02d}").glob("WS_*.ipynb"))[0]


def insert_reader_note(week: int) -> None:
    path = lecture_path(week)
    nb = load(path)
    cells = nb["cells"]
    marker = "### Numerical evolution" if week != 9 else "### Numerical evaluation"
    # Replace an existing standard summary instead of duplicating it.
    for cell in cells:
        src = "".join(cell.get("source", []))
        if src.startswith(marker):
            cell["source"] = lines(READER_NOTES[week])
            save(path, nb)
            return

    glance_terms = ["Canonical model at a glance", "Canonical models at a glance", "Information measures at a glance"]
    glance = next(i for i, c in enumerate(cells) if any(t in "".join(c.get("source", [])) for t in glance_terms))
    src = "".join(cells[glance].get("source", []))
    positions = [src.find(token) for token in ("# Canonical model in pseudocode", "# Canonical models in pseudocode", "### Analysis pipeline rather than model pseudocode")]
    positions = [p for p in positions if p >= 0]
    if positions:
        p = min(positions)
        cells[glance]["source"] = lines(src[:p] + READER_NOTES[week] + src[p:])
    else:
        cells.insert(glance + 1, markdown(READER_NOTES[week], f"numerical-evolution-week{week:02d}"))
    save(path, nb)


def insert_workshop_note(week: int) -> None:
    path = workshop_path(week)
    nb = load(path)
    cells = nb["cells"]
    cell_id = f"numerical-evolution-week{week:02d}"
    for cell in cells:
        if cell.get("id") == cell_id:
            cell["source"] = lines(WORKSHOP_NOTES[week] + "\n")
            save(path, nb)
            return
    target = "# Construct and inspect distributions" if week == 9 else "# Simulate and inspect"
    idx = next(i for i, c in enumerate(cells) if "".join(c.get("source", [])).strip().startswith(target))
    cells.insert(idx + 1, markdown(WORKSHOP_NOTES[week], cell_id))
    save(path, nb)


def polish_week06() -> None:
    path = lecture_path(6)
    nb = load(path)
    by_id = {c.get("id"): c for c in nb["cells"]}

    # The source SVG is deliberately subordinate to the definitions in both outputs.
    by_id["w6-uncoupled"]["source"] = lines(r"""## Two oscillators without coupling

<div class="two-panel">
<div class="image-panel"><img src="images/two_phase_oscillators.svg" alt="Two independent phase oscillators on the unit circle" style="display:block;width:62%;max-width:285px;max-height:220px;margin:0 auto"></div>
<div class="text-panel">

| Symbol | Meaning |
|---|---|
| $\theta_i$ | position within the cycle |
| $\omega_i$ | isolated rate of phase advance |
| $\phi=\theta_1-\theta_2$ | phase difference |

$$
\dot{\theta}_1=\omega_1, \qquad \dot{\theta}_2=\omega_2.
$$

The separation drifts unless the natural frequencies match.
</div>
</div>
""")
    by_id["uncoupled"]["source"] = lines(r"""## Two uncoupled oscillators

The circle is **phase space**, not a map of physical position. A point moving around it advances through one oscillation cycle.

<div style="display:grid;grid-template-columns:minmax(220px,0.72fr) minmax(0,1.4fr);gap:1.3rem;align-items:center">
<div><img src="images/two_phase_oscillators.svg" alt="Two independent phase oscillators on the unit circle" style="display:block;width:100%;max-width:300px;max-height:230px;margin:0 auto"></div>
<div>

| Symbol | Meaning |
|---|---|
| $\theta_i$ | phase: position within the cycle |
| $\omega_i$ | natural frequency: isolated rate of advance |
| $\phi=\theta_1-\theta_2$ | phase difference |

Without coupling,

$$
\dot{\theta}_1=\omega_1, \qquad \dot{\theta}_2=\omega_2,
$$

so

$$
\dot{\phi}=\omega_1-\omega_2.
$$

Unless the natural frequencies match, the relative phase drifts.
</div>
</div>
""")

    extra_prompt = r'<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What changes if the raw phase difference $\theta_2-\theta_1$ is used instead of $\sin(\theta_2-\theta_1)$?</span></div>'
    for cell_id in ("w6-coupling", "two-coupled"):
        src = "".join(by_id[cell_id]["source"])
        if "What changes if the raw phase difference" not in src:
            anchor = '<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Why might sine be a sensible first choice for the coupling?</span></div>'
            src = src.replace(anchor, anchor + "\n\n" + extra_prompt)
        by_id[cell_id]["source"] = lines(src)

    cards = [
        ("In-phase synchronisation", "Phases coincide, so their difference is 0 modulo 2π.", "in_phase", "In-phase oscillators"),
        ("Anti-phase synchronisation", "Two oscillators remain half a cycle apart, with phase difference π.", "anti_phase", "Anti-phase oscillators"),
        ("Phase locking", "Phase differences remain constant. The constant need not be 0 or π.", "phase_locked", "Phase-locked oscillators"),
        ("Frequency entrainment", "Oscillators share a long-time average frequency, although their phase difference may fluctuate.", "frequency_entrained", "Frequency-entrained oscillators"),
        ("Cluster synchronisation", "Subsets lock internally while different clusters retain different phases or rates.", "two_clusters", "Two synchronised clusters"),
        ("Partial synchronisation", "A locked group coexists with drifting oscillators.", "partial_synchrony", "Partial synchronisation"),
        ("Chimera state", "Coherent and incoherent subsets persist together. Classic chimeras usually need spatially organised or non-local coupling.", "chimera_like", "Chimera-like synchronisation"),
    ]
    html = ['## Several forms of synchronisation\n\nThe image in each entry combines a phase-space snapshot with observable time series.\n\n<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(440px,1fr));gap:1rem;margin:1rem 0">']
    for title, desc, slug, alt in cards:
        html.append(f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(210px,1.15fr);align-items:center;gap:0.8rem"><p><strong>{title}:</strong> {desc}</p><img src="images/synchronisation_types/{slug}.svg" alt="{alt}" style="width:100%;max-width:310px;justify-self:end"></div>')
    html.append('</div>\n\n**Generalised synchronisation:** the states maintain a stable functional relationship\n\n$$\n\\mathbf y(t)=F\\!\\left(\\mathbf x(t)\\right),\n$$\n\nwithout requiring equal states or equal observable signals. Complete synchronisation, $\\mathbf y=\\mathbf x$, and projective synchronisation, $\\mathbf y=a\\mathbf x$, are special cases. A relationship such as $y(t)=\\sin(x(t))$ counts only when the coupled dynamics establish and maintain it.\n')
    by_id["w6-types-of-synchronisation-reader"]["source"] = lines("\n".join(html))

    save(path, nb)


for week in range(1, 11):
    insert_reader_note(week)
    insert_workshop_note(week)
polish_week06()
print("Added numerical-evolution summaries to Weeks 1–10 and polished Week 6.")
