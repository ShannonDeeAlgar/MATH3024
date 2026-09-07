"""Refine the Week 6 adaptive-network workshop and time-series discussion."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def save(path: Path, notebook: dict) -> None:
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


def cell(notebook: dict, cell_id: str) -> dict:
    return next(c for c in notebook["cells"] if c.get("id") == cell_id)


def set_source(notebook: dict, cell_id: str, source: str) -> None:
    cell(notebook, cell_id)["source"] = source.splitlines(keepends=True)


workshop_path = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"
workshop = load(workshop_path)

set_source(
    workshop,
    "adaptive-network-player",
    r'''def adaptive_network_player(phase_frames, edge_frames, coherence_history, element_id="adaptive-network-player"):
    phases_json = json.dumps(np.round(phase_frames, 4).tolist())
    edges_json = json.dumps(edge_frames)
    coherence_json = json.dumps(np.round(coherence_history, 4).tolist())
    return HTML(f"""
    <div id="{element_id}" style="font-family:Arial,sans-serif;color:#1B2A4C;max-width:780px;margin:0 auto">
      <p style="margin:0 0 6px 0"><strong>Line:</strong> <em>A</em><sub>ij</sub> = 1. <strong>Node colour:</strong> oscillator phase.</p>
      <div style="width:100%;height:9px;border-radius:5px;background:linear-gradient(90deg,hsl(0,68%,48%),hsl(60,68%,48%),hsl(120,68%,48%),hsl(180,68%,48%),hsl(240,68%,48%),hsl(300,68%,48%),hsl(360,68%,48%));margin-bottom:8px"></div>
      <div style="display:flex;gap:12px;align-items:flex-start">
        <div style="flex:1;min-width:0"><div style="font-weight:600;margin-bottom:3px">Fixed layout</div><canvas class="fixed" width="360" height="320" style="width:100%;border:1px solid #C7CEDC"></canvas></div>
        <div style="flex:1;min-width:0"><div style="font-weight:600;margin-bottom:3px">Phase layout</div><canvas class="phase" width="360" height="320" style="width:100%;border:1px solid #C7CEDC"></canvas></div>
      </div>
      <p style="margin:5px 0;color:#506080;font-size:.92em">The right-hand nodes move in phase space, not through a physical domain.</p>
      <div style="display:flex;gap:8px;align-items:center">
        <button type="button">Play</button>
        <input type="range" min="0" max="{len(phase_frames)-1}" value="0" style="flex:1;accent-color:#1B2A4C">
        <span style="min-width:120px"></span>
      </div>
    </div>
    <script>
    (() => {{
      const root=document.getElementById('{element_id}'), phases={phases_json}, edges={edges_json}, coherence={coherence_json};
      const fixed=root.querySelector('canvas.fixed'), moving=root.querySelector('canvas.phase');
      const slider=root.querySelector('input'), button=root.querySelector('button'), label=root.querySelector('span');
      const n=phases[0].length; let timer=null;
      function colour(a) {{return `hsl(${{(a+Math.PI)*180/Math.PI}},68%,48%)`;}}
      function positions(canvas,k,mode) {{
        const cx=canvas.width/2, cy=canvas.height/2, R=124;
        return Array.from({{length:n}},(_,i)=>{{const a=mode==='fixed' ? 2*Math.PI*i/n : phases[k][i]; return [cx+R*Math.cos(a),cy-R*Math.sin(a)];}});
      }}
      function panel(canvas,k,mode) {{
        const ctx=canvas.getContext('2d'), xy=positions(canvas,k,mode), cx=canvas.width/2, cy=canvas.height/2;
        ctx.clearRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);
        if(mode==='phase'){{ctx.strokeStyle='#D9DFEA';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(cx,cy,124,0,2*Math.PI);ctx.stroke();}}
        ctx.strokeStyle='rgba(88,121,170,0.24)';ctx.lineWidth=1;
        edges[k].forEach(e=>{{ctx.beginPath();ctx.moveTo(...xy[e[0]]);ctx.lineTo(...xy[e[1]]);ctx.stroke();}});
        phases[k].forEach((a,i)=>{{ctx.fillStyle=colour(a);ctx.strokeStyle='#1B2A4C';ctx.lineWidth=.8;ctx.beginPath();ctx.arc(xy[i][0],xy[i][1],4.8,0,2*Math.PI);ctx.fill();ctx.stroke();}});
      }}
      function draw(k) {{panel(fixed,k,'fixed');panel(moving,k,'phase');label.textContent=`frame ${{k}}; r = ${{coherence[k].toFixed(2)}}`;}}
      function stop() {{clearInterval(timer);timer=null;button.textContent='Play';}}
      button.onclick=()=>{{if(timer){{stop();return;}}button.textContent='Pause';timer=setInterval(()=>{{let k=+slider.value;if(k>=phases.length-1){{stop();return;}}slider.value=k+1;draw(k+1);}},130);}};
      slider.oninput=()=>draw(+slider.value);draw(0);
    }})();
    </script>
    """)


frame_r = adaptive_r[::5][:len(adaptive_phases)]
display(adaptive_network_player(adaptive_phases, adaptive_edges, frame_r))
''',
)

set_source(
    workshop,
    "adaptive-network-analysis",
    r'''## Analyse the network as well as the phases

The animation and the diagnostics below come from the same stored run.

Global coherence $r$ combines every phase vector. If two internally aligned groups sit on different parts of the phase circle, their vectors partly cancel and $r$ can rise and fall even though most connected neighbours agree. The live value of $r$ is now shown beside the animation controls so this can be checked directly.

The **phase-similar edge fraction** is the proportion of current edges whose endpoints differ by less than $\pi/6$. It can approach one while rewiring continues: the model removes a dissimilar edge and replaces it with a similar one, but keeps the total number of edges fixed.

The final panel records the fraction of the original edges still present. A falling curve confirms that the network is changing. A plateau would indicate that rewiring has effectively stopped under this rule.
''',
)

set_source(
    workshop,
    "adaptive-network-analysis-code",
    r'''similar_edge_fraction = []
initial_edges = {tuple(edge) for edge in adaptive_edges[0]}
initial_edge_retention = []

for phases, edges in zip(adaptive_phases, adaptive_edges):
    gaps = [abs(np.angle(np.exp(1j * (phases[i] - phases[j])))) for i, j in edges]
    similar_edge_fraction.append(np.mean(np.asarray(gaps) < np.pi / 6))
    current_edges = {tuple(edge) for edge in edges}
    initial_edge_retention.append(len(initial_edges & current_edges) / len(initial_edges))

frame_time = np.arange(len(adaptive_phases)) * 5 * 0.05
frame_r = adaptive_r[::5][:len(adaptive_phases)]

fig, axes = plt.subplots(1, 3, figsize=(11, 3.25))
axes[0].plot(frame_time, frame_r, color=INK)
axes[0].set(xlabel="Simulation time", ylabel="Global coherence, $r$", ylim=(-0.03, 1.03))
axes[1].plot(frame_time, similar_edge_fraction, color=BLUE)
axes[1].set(xlabel="Simulation time", ylabel="Phase-similar edge fraction", ylim=(-0.03, 1.03))
axes[2].plot(frame_time, initial_edge_retention, color="#DF6338")
axes[2].set(xlabel="Simulation time", ylabel="Original edges retained", ylim=(-0.03, 1.03))
for ax in axes:
    ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()
''',
)

save(workshop_path, workshop)


reader_path = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
reader = load(reader_path)

beats = cell(reader, "w6-beats")
beats_text = "".join(beats["source"])
mod_note = (
    "\nA familiar example of modular arithmetic is the seven-day week: moving forward or "
    "backward wraps around modulo 7. Phase works the same way modulo $2\\pi$; angles that "
    "differ by one complete turn represent the same point in the cycle.\n"
)
anchor = "Phase is defined modulo $2\\pi$; wrapping the same curve would produce a sawtooth rather than a constant phase difference."
if mod_note.strip() not in beats_text and anchor in beats_text:
    beats_text = beats_text.replace(anchor, anchor + mod_note)
    beats["source"] = beats_text.splitlines(keepends=True)

types = cell(reader, "w6-types-of-synchronisation-reader")
types_text = "".join(types["source"])
time_series = r'''

#### Detecting synchronisation from measured time series

In an experiment we may not observe an oscillator's phase directly. Instead, we record signals such as light intensity, displacement, voltage, breathing or heartbeat timing. Phase can be estimated from repeated events or reconstructed from a smoothly oscillating signal. We can then test whether a phase difference remains concentrated around a constant value, whether average frequencies agree, or whether an $n:m$ relationship persists.

This detects coordination; it does not by itself identify the coupling mechanism. Schäfer et al. used heartbeat and respiratory time series to identify intervals in which heartbeats occurred at preferred phases of the breathing cycle ([*Heartbeat synchronized with ventilation*, 1998](https://doi.org/10.1038/32567)). The same distinction applies here: the Kuramoto model proposes a mechanism, whereas time-series analysis asks whether synchronisation is present in observations.
'''
if "#### Detecting synchronisation from measured time series" not in types_text:
    types_text = types_text.rstrip() + time_series + "\n"
    types["source"] = types_text.splitlines(keepends=True)

save(reader_path, reader)
