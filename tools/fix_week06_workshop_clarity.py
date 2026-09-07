import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def set_source(cell, text):
    cell["source"] = [line + "\n" for line in text.splitlines()]


# Reader and slides source
lecture_path = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
lecture = json.loads(lecture_path.read_text())
for cell in lecture["cells"]:
    if cell.get("id") == "w6-watch":
        set_source(cell, r'''# Qualitative analysis

## Watch the phases organise

<img src="images/kuramoto_phase_circle.gif" alt="Kuramoto oscillators moving around the phase circle and organising under coupling" style="display:block;max-height:350px;max-width:70%;width:auto;margin:0 auto">

This is a **phase-circle display**: angle around the circle is the oscillator phase $\theta_i$. It is a picture of the model's phase space, not a map of physical positions. At this level we retain every oscillator and watch how the phases reorganise.''')
    elif cell.get("id") == "kuramoto-video":
        set_source(cell, r'''## Qualitative analysis · watch the phases organise

<img src="images/kuramoto_phase_circle.gif" alt="Kuramoto oscillators moving around the phase circle and organising under coupling" style="display:block;width:34%;max-width:330px;margin:0.7rem auto">

This is a **phase-circle display**. The angle around the circle records phase $\theta_i$; it is not a map of physical position. The moving display retains every oscillator, so clustering and frequency locking remain visible before we replace them with a collective summary.''')
lecture_path.write_text(json.dumps(lecture, ensure_ascii=False, indent=1) + "\n")


# Workshop
workshop_path = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"
workshop = json.loads(workshop_path.read_text())
for cell in workshop["cells"]:
    cid = cell.get("id")
    if cid == "coherence-code":
        set_source(cell, r'''def coherence(phases: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return coherence magnitude r and mean phase psi."""
    phases = np.asarray(phases, dtype=float)
    if phases.ndim not in (1, 2):
        raise ValueError("phases must be one- or two-dimensional")
    order = np.mean(np.exp(1j * phases), axis=-1)
    return np.abs(order), np.angle(order)


r_history, psi_history = coherence(phase_history)
time = np.arange(len(r_history)) * baseline.dt
psi_periodic = np.mod(psi_history, 2 * np.pi)

fig, axes = plt.subplots(2, 1, figsize=(7, 4.8), sharex=True,
                         gridspec_kw={"height_ratios": [1.15, 1]})
axes[0].plot(time, r_history, color=INK, lw=2)
axes[0].set(ylabel="Coherence, $r$", ylim=(-0.03, 1.03))
axes[1].plot(time, psi_periodic, color=ORANGE, lw=1.8)
axes[1].set(xlabel="Simulation time", ylabel=r"Mean phase, $\psi$",
            ylim=(-0.12, 2 * np.pi + 0.12), yticks=[0, np.pi, 2 * np.pi],
            yticklabels=["0", r"$\pi$", r"$2\pi$"])
for ax in axes:
    ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()''')
    elif cid == "extensions":
        text = ''.join(cell.get('source', []))
        text += ("\nThe natural frequency $\\omega_i$ is how quickly oscillator $i$ would rotate "
                 "in isolation. Its **realised long-time frequency** $\\Omega_i$ is measured from "
                 "the simulated phase trajectory after transients. The diagonal in the next plot is "
                 "only the no-adjustment reference $\\Omega_i=\\omega_i$; the points are the realised "
                 "rates. Frequency-locked oscillators share the horizontal group rate. Oscillators "
                 "below that rate have been sped up and those above it have been slowed down. A "
                 "**drifting oscillator** is not locked to the group: its phase continues to slip "
                 "relative to the locked cluster.\n")
        set_source(cell, text.rstrip())
    elif cid == "visualise-frequency-heterogeneity":
        src = ''.join(cell.get('source', []))
        src = src.replace('label="drifting"', 'label="drifting: not locked"')
        src = src.replace('label="frequency locked"', 'label="locked: shared rate"')
        src = src.replace('label="realised = natural"', 'label="no coupling: $\\Omega_i=\\omega_i$"')
        src = src.replace('ylabel="Long-time realised frequency"', 'ylabel=r"Realised long-time frequency, $\\Omega_i$"')
        src = src.replace('axes[1].legend(frameon=False, fontsize=9)', 'axes[1].legend(frameon=False, fontsize=8.5, loc="upper left")')
        set_source(cell, src.rstrip())
    elif cid == "adaptive-network-intro":
        set_source(cell, r'''# Let the interaction network evolve

So far, the interaction network has been fixed and complete. In many systems the state also changes who interacts: agreement can strengthen a connection, disagreement can break one, or spatial motion can create and remove neighbours. This creates an **adaptive network**: oscillator states change the network, and the network changes the oscillator states.

Two oscillators are connected when the adjacency matrix has $A_{ij}=1$; the corresponding edge is drawn as a line. The initial graph is sparse. Each possible pair is connected independently with probability $p=\langle k\rangle/(N-1)$, giving expected mean degree $\langle k\rangle$. Connectivity is therefore a modelled relationship, not a consequence of the nodes being close on the page.

At each rewiring event, the code removes only one existing edge and adds only one absent edge. Removal is sampled from the 20% of existing edges with the largest phase differences; addition is sampled from the 20% of absent pairs with the smallest differences. The edge count stays fixed. This is a partial, stochastic rewiring rule, so two nearby phases are not automatically connected and the graph does not become a complete graph of similar oscillators.

The paired display shows the same graph in two layouts. Fixed node positions make changed edges easier to trace. In the phase layout, the angle of each node is its phase. Movement there is movement through phase space, not through a physical domain. Node colour also records phase.

> **Modelling decision:** What process should create or remove a connection in the system you want to represent?''')
    elif cid == "adaptive-network-analysis":
        set_source(cell, r'''## Analyse the network as well as the phases

The animation and the diagnostics below come from the same stored run.

Global coherence $r$ combines every phase vector. If two internally aligned groups sit on different parts of the phase circle, their vectors partly cancel and $r$ can rise and fall even though most connected neighbours agree.

The **phase-similar edge fraction** is the proportion of the edges that currently exist whose endpoints differ by less than $\pi/6$. It says whether linked oscillators have similar phases; it does not count how many possible edges exist. It can approach one while old edges continue to be replaced because the model keeps the edge count fixed.

The final panel records the fraction of the original edges still present. A falling curve confirms that the graph is being rewired. A plateau would indicate that the network has become stable under this particular rewiring rule.''')
    elif cid == "8d9ee696":
        src = ''.join(cell.get('source', []))
        src = src.replace('ax.legend(frameon=False)', 'ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.01))')
        set_source(cell, src.rstrip())

workshop_path.write_text(json.dumps(workshop, ensure_ascii=False, indent=1) + "\n")
