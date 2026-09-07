#!/usr/bin/env python3
"""Align Week 3 practice framing and strengthen Week 5 sampling decisions."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]


def markdown(source: str):
    return nbformat.v4.new_markdown_cell(source.strip() + "\n")


def code(source: str):
    return nbformat.v4.new_code_cell(source.strip() + "\n")


# Week 3: its cross-cutting modelling practice is the choice and movement
# between particle, field, and numerical representations.
week03_path = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
week03 = nbformat.read(week03_path, as_version=4)
title = week03.cells[0]
title.source = title.source.replace(
    "<div class=\"modelling-practice-marker\"><span>Modelling practice</span><strong>Numerical verification before interpretation</strong></div>",
    "<div class=\"modelling-practice-marker\"><span>Modelling practice</span><strong>Choosing discrete and continuous representations</strong></div>",
)
nbformat.write(week03, week03_path)


week05_path = ROOT / "notebooks/week05/WS_ABM.ipynb"
week05 = nbformat.read(week05_path, as_version=4)


def find(text: str) -> int:
    return next(i for i, cell in enumerate(week05.cells) if text in cell.source)


pause_i = find("## Pause the process")
week05.cells[pause_i].source = r"""
## Pause the process

Use the time slider to inspect how local headings become coordinated. The representation menu changes only the display, not the stored model state. Direction-coloured arrows are the default because arrow orientation remains readable without colour while cyclic colour makes similarly aligned groups easier to find.

> **Down the ladder:** inspect individual positions, headings, and neighbours before summarising the flock. Use this view to explain the mechanism and to debug it: pause on one update and check that neighbours, headings, motion, and boundary wrapping agree with the rule you intended to code.
""".strip() + "\n"

player_i = find("def vicsek_player(")
week05.cells[player_i].source = r'''
def vicsek_player(
    position_history,
    heading_history,
    box_size,
    element_id="vicsek-player",
    representation="coloured_arrows",
):
    """Interactive Vicsek display with a changeable visual representation."""
    allowed = {"dots", "bars", "arrows", "coloured_arrows"}
    if representation not in allowed:
        raise ValueError(f"representation must be one of {sorted(allowed)}")

    positions_json = json.dumps(np.round(position_history, 4).tolist())
    headings_json = json.dumps(np.round(heading_history, 4).tolist())
    return HTML(f"""
    <div id="{element_id}" style="font-family:Arial,sans-serif;color:#1B2A4C;max-width:900px">
      <canvas width="650" height="650" style="width:min(100%,520px);border:1px solid #C7CEDC"></canvas>
      <div style="display:flex;gap:10px;align-items:center;max-width:650px;flex-wrap:wrap">
        <button type="button">Play</button>
        <input type="range" min="0" max="{len(position_history)-1}" value="0" style="flex:1;min-width:220px;accent-color:#1B2A4C">
        <span></span>
        <label>Representation
          <select>
            <option value="dots">Dots</option>
            <option value="bars">Bars</option>
            <option value="arrows">Arrows</option>
            <option value="coloured_arrows">Direction-coloured arrows</option>
          </select>
        </label>
      </div>
    </div>
    <script>
    (() => {{
      const root=document.getElementById('{element_id}');
      const pos={positions_json}, ang={headings_json}, L={box_size};
      const canvas=root.querySelector('canvas'), ctx=canvas.getContext('2d');
      const slider=root.querySelector('input'), button=root.querySelector('button');
      const label=root.querySelector('span'), select=root.querySelector('select');
      select.value='{representation}';
      let timer=null;

      function arrow(x,y,a,colour,head=true) {{
        const length=13, x2=x+length*Math.cos(a), y2=y-length*Math.sin(a);
        ctx.strokeStyle=colour; ctx.fillStyle=colour; ctx.lineWidth=2;
        ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x2,y2); ctx.stroke();
        if(head) {{
          const h=4.5;
          ctx.beginPath();
          ctx.moveTo(x2,y2);
          ctx.lineTo(x2-h*Math.cos(a-0.55),y2+h*Math.sin(a-0.55));
          ctx.lineTo(x2-h*Math.cos(a+0.55),y2+h*Math.sin(a+0.55));
          ctx.closePath(); ctx.fill();
        }}
      }}

      function draw(k) {{
        ctx.clearRect(0,0,canvas.width,canvas.height);
        ctx.fillStyle='#fff'; ctx.fillRect(0,0,canvas.width,canvas.height);
        const scale=canvas.width/L, mode=select.value;
        pos[k].forEach((p,i)=>{{
          const x=p[0]*scale, y=(L-p[1])*scale, a=ang[k][i];
          if(mode==='dots') {{
            ctx.fillStyle='#1B2A4C'; ctx.beginPath(); ctx.arc(x,y,3.2,0,2*Math.PI); ctx.fill();
          }} else if(mode==='bars') {{
            arrow(x,y,a,'#1B2A4C',false);
          }} else if(mode==='arrows') {{
            arrow(x,y,a,'#1B2A4C',true);
          }} else {{
            const hue=((a%(2*Math.PI)+2*Math.PI)%(2*Math.PI))*180/Math.PI;
            arrow(x,y,a,`hsl(${{hue}},72%,42%)`,true);
          }}
        }});
        label.textContent=`t = ${{k}}`;
      }}
      function stop() {{clearInterval(timer);timer=null;button.textContent='Play';}}
      button.onclick=()=>{{if(timer){{stop();return;}}button.textContent='Pause';timer=setInterval(()=>{{let k=+slider.value;if(k>=pos.length-1){{stop();return;}}slider.value=k+1;draw(k+1);}},100);}};
      slider.oninput=()=>draw(+slider.value);
      select.onchange=()=>draw(+slider.value);
      draw(0);
    }})();
    </script>
    """)


display(vicsek_player(
    positions_history,
    headings_history,
    baseline.box_size,
    representation="coloured_arrows",
))
'''.strip() + "\n"


# After the first ensemble, turn ensemble size into a decision rather than an
# unexplained fixed constant. The pilot deliberately targets the most variable
# coarse-sweep condition, where additional runs are usually most valuable.
ensemble_marker = "## How many runs are enough?"
if not any(ensemble_marker in cell.source for cell in week05.cells):
    insert_at = find("## Compare two noise conventions")
    week05.cells[insert_at:insert_at] = [
        markdown(r"""
## How many runs are enough?

There is no universal sufficient ensemble size. It depends on the variability of the outcome and the precision required for the claim. Begin with a pilot ensemble, then check whether the estimated mean and spread are still changing as runs are added.

The code below chooses the noise value with the widest middle 50% in the coarse sweep. This is a sensible stress test: conditions near a transition often vary more between runs than clearly ordered or disordered conditions.

> **Modelling decision:** specify a tolerance before increasing the ensemble. For example, require the running mean to change by less than 0.02 when the final eight runs are added, while also checking that the estimated standard deviation has stabilised. More runs reduce sampling uncertainty; they do not repair a short runtime, small world, or biased implementation.
"""),
        code(r"""
pilot_size = 32
coarse_iqr = upper - lower
pilot_noise = float(noise_values[np.argmax(coarse_iqr)])
pilot_values = []

for seed in tqdm(np.arange(pilot_size) + SEED, desc="Ensemble-size pilot"):
    params = VicsekParameters(noise=pilot_noise)
    _, headings = simulate_vicsek(params, steps=180, seed=int(seed))
    pilot_values.append(polarisation(headings[-40:]).mean())

pilot_values = np.asarray(pilot_values)
ensemble_sizes = np.arange(2, pilot_size + 1)
running_mean = np.array([pilot_values[:n].mean() for n in ensemble_sizes])
running_sd = np.array([pilot_values[:n].std(ddof=1) for n in ensemble_sizes])

fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), constrained_layout=True)
axes[0].plot(ensemble_sizes, running_mean, color=INK, lw=2)
axes[0].set(ylabel="Running mean polarisation")
axes[1].plot(ensemble_sizes, running_sd, color=BLUE, lw=2)
axes[1].set(ylabel="Running standard deviation")
for ax in axes:
    ax.set(xlabel="Number of runs")
    ax.grid(alpha=0.2)
fig.suptitle(f"Ensemble-size diagnostic at $\\eta={pilot_noise:.2f}$")
plt.show()

mean_change = abs(running_mean[-1] - running_mean[-9])
print(f"Change in mean after adding the final 8 runs: {mean_change:.3f}")
"""),
        markdown(r"""
> **Discuss:** Is the mean alone stable, or has the estimated spread also settled? Would the same number of runs be necessary far from the transition? State what evidence would persuade you that the ensemble is large enough for the precision of your conclusion.
"""),
        markdown(r"""
## Refine the parameter grid where behaviour changes

A coarse sweep should locate broad behaviour first. It should not be mistaken for precise evidence about where or how a transition occurs. Once the steepest interval is identified, add parameter values inside that interval while retaining ensembles at every value.

This is adaptive allocation of a finite budget: use broad coverage to find the interesting region, then spend resolution there. A finer parameter grid without repeated runs can simply resolve stochastic noise more finely.
"""),
        code(r"""
steepest_interval = int(np.argmax(np.abs(np.diff(mean_phi) / np.diff(noise_values))))
left, right = noise_values[steepest_interval:steepest_interval + 2]
refined_noise = np.linspace(left, right, 7)
refined = np.empty((len(refined_noise), len(seeds)))

for row, noise in enumerate(tqdm(refined_noise, desc="Refined ensemble sweep")):
    params = VicsekParameters(noise=float(noise))
    for column, seed in enumerate(seeds):
        _, headings = simulate_vicsek(params, steps=180, seed=int(seed))
        refined[row, column] = polarisation(headings[-40:]).mean()

refined_mean = refined.mean(axis=1)
refined_lower, refined_upper = np.quantile(refined, [0.25, 0.75], axis=1)

fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(noise_values, mean_phi, "o--", color="#8A94A6", label="Coarse sweep")
ax.plot(refined_noise, refined_mean, "o-", color=INK, lw=2, label="Refined sweep")
ax.fill_between(refined_noise, refined_lower, refined_upper, color=BLUE, alpha=0.25,
                label="Refined middle 50%")
ax.axvspan(left, right, color=YELLOW, alpha=0.12)
ax.set(xlabel="Angular noise width, $\\eta$", ylabel="Final mean polarisation",
       ylim=(-0.03, 1.03))
ax.grid(alpha=0.2)
ax.legend(frameon=False)
fig.tight_layout()
plt.show()
"""),
        markdown(r"""
> **Discuss:** Did refinement reveal a feature that the coarse grid concealed, or merely confirm the same broad change? If the goal were to determine the order of the transition, what additional changes to system size, runtime, initialisation and sampling would still be required?
"""),
    ]


# Overlay the two noise-response curves after the faceted view. Facets make
# each uncertainty band readable; the overlay makes displacement and shape
# differences easier to compare directly.
overlay_marker = "## Overlay the two noise responses"
if not any(overlay_marker in cell.source for cell in week05.cells):
    insert_at = find("# Interpret the evidence")
    week05.cells[insert_at:insert_at] = [
        markdown(r"""
## Overlay the two noise responses

The side-by-side panels keep each uncertainty band clear. An overlay can make horizontal shifts and differences in curve shape easier to see, provided the line styles and labels remain distinguishable without colour.
"""),
        code(r"""
fig, ax = plt.subplots(figsize=(7.5, 4))
styles = {"angular": (INK, "o", "-"), "vectorial": (BLUE, "s", "--")}

for mode in ("angular", "vectorial"):
    colour, marker, linestyle = styles[mode]
    values = noise_results[mode]
    mean = values.mean(axis=1)
    lower, upper = np.quantile(values, [0.25, 0.75], axis=1)
    ax.plot(normalised_noise, mean, marker=marker, linestyle=linestyle,
            color=colour, lw=2, label=f"{mode.capitalize()} noise")
    ax.fill_between(normalised_noise, lower, upper, color=colour, alpha=0.14)

ax.set(xlabel="Normalised noise level", ylabel="Final mean polarisation",
       xlim=(-0.03, 1.03), ylim=(-0.03, 1.03))
ax.grid(alpha=0.2)
ax.legend(frameon=False)
fig.tight_layout()
plt.show()
"""),
        markdown(r"""
> **Discuss:** Does the overlay support the same comparison as the separate panels? Normalising both controls to $[0,1]$ aligns their plotting range; it does not make angular and vectorial noise physically identical.
"""),
    ]


nbformat.write(week05, week05_path)
