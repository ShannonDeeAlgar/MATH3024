import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def lines(text: str):
    return text.splitlines(keepends=True)


def markdown(text: str):
    return {"cell_type": "markdown", "metadata": {}, "source": lines(text)}


def code(text: str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines(text),
    }


reader_path = ROOT / "notebooks/week05/L_ABM.ipynb"
reader = json.loads(reader_path.read_text())

for cell in reader["cells"]:
    source = "".join(cell.get("source", []))
    if source.startswith("The Franklin example is collective behaviour"):
        cell["source"] = lines(
            "Franklin's hundredth goal establishes the modelling problem: coordinated system-level motion can arise without a central controller, while congestion, social cues, goals and boundaries still matter.\n\n"
            "At the microscopic level we could record positions, headings, neighbours and decisions. At the macroscopic level we see a surge, a stream or a jam. An agent-based model keeps enough of the first description to ask how the second emerges.\n"
        )
    if "flock of birds<br>murmuration of starlings" in source:
        source = source.replace(
            '<p>Everyday language treats the group as an entity:</p>\n<p>flock of birds<br>murmuration of starlings<br>parliament of owls<br>chatter of budgerigars</p>',
            '<p>Everyday language treats the group as an entity:</p>\n\n'
            '| Group | Animals |\n'
            '|---|---|\n'
            '| flock | birds |\n'
            '| murmuration | starlings |\n'
            '| parliament | owls |\n'
            '| chatter | budgerigars |\n'
        )
        source = source.replace(
            '| Group | Animals |\n|---|---|\n| flock | birds |\n| murmuration | starlings |\n| parliament | owls |\n| chatter | budgerigars |\n',
            '<table class="collective-nouns">\n'
            '<thead><tr><th>Group</th><th>Animals</th></tr></thead>\n'
            '<tbody>\n'
            '<tr><td>flock</td><td>birds</td></tr>\n'
            '<tr><td>murmuration</td><td>starlings</td></tr>\n'
            '<tr><td>parliament</td><td>owls</td></tr>\n'
            '<tr><td>chatter</td><td>budgerigars</td></tr>\n'
            '</tbody>\n'
            '</table>\n'
        )
        cell["source"] = lines(source)
    if "| Group | Animals |" in source:
        source = source.replace(
            '| Group | Animals |\n|---|---|\n| flock | birds |\n| murmuration | starlings |\n| parliament | owls |\n| chatter | budgerigars |\n',
            '<table class="collective-nouns">\n'
            '<thead><tr><th>Group</th><th>Animals</th></tr></thead>\n'
            '<tbody>\n'
            '<tr><td>flock</td><td>birds</td></tr>\n'
            '<tr><td>murmuration</td><td>starlings</td></tr>\n'
            '<tr><td>parliament</td><td>owls</td></tr>\n'
            '<tr><td>chatter</td><td>budgerigars</td></tr>\n'
            '</tbody>\n'
            '</table>\n'
        )
        cell["source"] = lines(source)

reader_path.write_text(json.dumps(reader, indent=1, ensure_ascii=False) + "\n")


workshop_path = ROOT / "notebooks/week05/WS_ABM.ipynb"
workshop = json.loads(workshop_path.read_text())

for cell in workshop["cells"]:
    source = "".join(cell.get("source", []))
    if source.startswith("## Compare two noise conventions"):
        cell["source"] = lines(
            "## Compare two noise conventions\n\n"
            "Noise can enter the update in different places.\n\n"
            "- **Angular noise:** first calculate the local mean direction, then rotate it by a random angle of width $\\eta$.\n"
            "- **Vectorial noise:** add a random vector of relative magnitude $\\xi$ to the local mean vector, then calculate the resulting angle.\n\n"
            "These are different stochastic models. We sweep the normalised coordinates $\\eta/(2\\pi)$ and $\\xi$ from zero to one, use the same seeds, and compare their finite-system order–disorder curves.\n\n"
            "This first comparison is deliberately responsive: $N=80$ agents, 220 steps, nine noise values and eight runs per value. It can show that the noise convention changes the curve, but it is **not large or long enough to establish whether either transition is continuous or discontinuous**. In a finite system, averaging independent runs can also smooth over switching or coexistence.\n\n"
            "> **Discuss:** Does changing where noise enters merely shift the apparent transition, or also alter its shape and run-to-run variation? What evidence would be required before calling either transition continuous or discontinuous?\n"
        )

insert_after = None
for index, cell in enumerate(workshop["cells"]):
    source = "".join(cell.get("source", []))
    if source.startswith("> **Discuss:** Does the overlay support"):
        insert_after = index
        break

extension_cells = [
    markdown(
        "## Optional extension · look for a finite-system discontinuity\n\n"
        "Vectorial noise is associated with a more abrupt, first-order transition in sufficiently large Vicsek systems. That does not mean a small finite simulation must display a vertical jump. The discontinuity is tied to phase coexistence and travelling density bands, and it becomes clearer as the domain and observation time increase.\n\n"
        "A stronger diagnostic therefore changes the experiment as well as the noise rule:\n\n"
        "1. keep density fixed while increasing the number of agents and box size;\n"
        "2. use a finer noise grid near the transition and run longer;\n"
        "3. sweep upward from an ordered state and downward from a disordered state, carrying the final state forward;\n"
        "4. inspect spatial snapshots and the distribution of polarisation, not only its mean.\n\n"
        "Different upward and downward branches provide finite-system evidence of hysteresis. Bimodal polarisation or ordered bands coexisting with disorder provide evidence of phase coexistence. A convincing claim about transition order would still require several system sizes and finite-size analysis.\n\n"
        "> **Computational choice:** This extension is off by default because the transparent all-pairs neighbour calculation scales approximately as $N^2$ per step. Set `RUN_LARGE_SYSTEM_EXTENSION = True` when you have time to run it, and reduce `large_n`, `steps_per_level`, or the number of noise levels when testing the code.\n"
    ),
    code(
        "RUN_LARGE_SYSTEM_EXTENSION = False\n\n"
        "large_n = 320\n"
        "large_density = 2.0\n"
        "large_box = np.sqrt(large_n / large_density)\n"
        "vectorial_levels = np.linspace(0.35, 0.85, 17)\n"
        "steps_per_level = 600\n"
        "sample_window = 150\n\n"
        "def vectorial_continuation(levels, ordered_start, seed):\n"
        "    rng = np.random.default_rng(seed)\n"
        "    params0 = VicsekParameters(\n"
        "        n_agents=large_n, box_size=large_box, speed=0.5, radius=1.0,\n"
        "        noise=float(levels[0]), noise_mode=\"vectorial\"\n"
        "    )\n"
        "    positions, headings = initialise_vicsek(params0, rng)\n"
        "    if ordered_start:\n"
        "        headings[:] = 0.0\n"
        "    branch_phi, branch_states = [], []\n"
        "    for level in tqdm(levels, desc=\"Continuation\"):\n"
        "        params = VicsekParameters(\n"
        "            n_agents=large_n, box_size=large_box, speed=0.5, radius=1.0,\n"
        "            noise=float(level), noise_mode=\"vectorial\"\n"
        "        )\n"
        "        recent_phi = []\n"
        "        for step in range(steps_per_level):\n"
        "            positions, headings = vicsek_step(positions, headings, params, rng)\n"
        "            if step >= steps_per_level - sample_window:\n"
        "                recent_phi.append(polarisation(headings))\n"
        "        branch_phi.append(np.mean(recent_phi))\n"
        "        branch_states.append((positions.copy(), headings.copy()))\n"
        "    return np.asarray(branch_phi), branch_states\n\n"
        "if RUN_LARGE_SYSTEM_EXTENSION:\n"
        "    upward_phi, upward_states = vectorial_continuation(\n"
        "        vectorial_levels, ordered_start=True, seed=SEED\n"
        "    )\n"
        "    downward_reversed_phi, downward_reversed_states = vectorial_continuation(\n"
        "        vectorial_levels[::-1], ordered_start=False, seed=SEED + 1\n"
        "    )\n"
        "    downward_phi = downward_reversed_phi[::-1]\n"
        "    downward_states = downward_reversed_states[::-1]\n\n"
        "    fig, ax = plt.subplots(figsize=(7.2, 4.2))\n"
        "    ax.plot(vectorial_levels, upward_phi, \"o-\", color=INK, label=\"Increasing noise · ordered start\")\n"
        "    ax.plot(vectorial_levels, downward_phi, \"s--\", color=BLUE, label=\"Decreasing noise · disordered start\")\n"
        "    ax.set(xlabel=r\"Vectorial noise, $\\xi$\", ylabel=r\"Mean polarisation, $\\Phi$\", ylim=(-0.03, 1.03))\n"
        "    ax.grid(alpha=0.2)\n"
        "    ax.legend(frameon=False)\n"
        "    fig.tight_layout()\n"
        "    plt.show()\n"
        "else:\n"
        "    print(\"Optional larger-system continuation not run. Set RUN_LARGE_SYSTEM_EXTENSION = True to enable it.\")\n"
    ),
    markdown(
        "If the two branches separate, inspect the corresponding configurations rather than treating the gap alone as proof. Travelling high-density bands and switching between ordered and disordered states are part of the mechanism that a small box may suppress. If the branches do not separate, increase the system size and runtime before concluding that the transition is continuous.\n\n"
        "> **Discuss:** Which changed ingredient—system size, duration, initialisation, noise resolution, or observable—most alters the conclusion? What additional evidence would you require before extrapolating from these finite simulations to a large-system phase transition?\n"
    ),
]

if insert_after is None:
    raise RuntimeError("Could not find noise comparison insertion point")

# Avoid duplicating the extension if the updater is run twice.
if not any("Optional extension · look for a finite-system discontinuity" in "".join(c.get("source", [])) for c in workshop["cells"]):
    workshop["cells"][insert_after + 1:insert_after + 1] = extension_cells

workshop_path.write_text(json.dumps(workshop, indent=1, ensure_ascii=False) + "\n")
