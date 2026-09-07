#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("notebooks/week06/L_Synchronisation.ipynb")
nb = json.loads(path.read_text())
cells = nb["cells"]

def get(cid): return next(c for c in cells if c.get("id") == cid)
def src(cid): return "".join(get(cid).get("source", []))
def setsrc(cid, text): get(cid)["source"] = text.splitlines(keepends=True)
def remove(cid): cells.remove(get(cid))
def move_after(cid, anchor):
    c = get(cid); cells.remove(c); cells.insert(cells.index(get(anchor)) + 1, c)

# Slides removed; the historical and comparative context remains in the Reader.
for cid in ["w6-coordination-contrast-slide", "w6-huygens", "w6-synchrony-examples",
            "w6-1657fb237d", "w6-swarmalator-videos-slide"]:
    remove(cid)

# Introduce the firefly interpretation, then ask students to specify a model,
# before revealing Kuramoto's implementation in the explorable.
move_after("w6-firefly-kuramoto", "w6-fireflies")
move_after("w6-model-banner", "w6-firefly-kuramoto")
move_after("w6-specify", "w6-model-banner")
move_after("w6-kuramoto-explorable", "w6-specify")

setsrc("w6-beats", r'''## Beats are not synchronisation

<img src="images/phase_signals_uncoupled.svg" alt="Two uncoupled oscillatory signals, their sum and their drifting phase difference" style="display:block;max-height:435px;max-width:94%;margin:0 auto">

Several slow beat cycles are visible in the sum. Neither oscillator responds to the other: the phase difference continues to drift.
''')

setsrc("w6-coupling", r'''## Add coupling

Suppose oscillator 2 influences oscillator 1:

$$
\dot{\theta}_1=\omega_1+K\sin(\theta_2-\theta_1),
\qquad
\dot{\theta}_2=\omega_2.
$$

The sine is the simplest smooth periodic interaction with the required symmetry. It gives no correction when phases agree, opposite corrections for leading and lagging, and the same rule after a full turn. $K$ controls its strength.

<img src="images/phase_signals_coupled.svg" alt="Two coupled oscillatory signals, their sum and a phase difference approaching a constant" style="display:block;max-height:315px;max-width:96%;margin:0 auto">
''')

setsrc("w6-relative", r'''## Reduce to their relative phase

For two oscillators, subtracting the equations removes their shared rotation and retains only their separation.

With $\phi=\theta_1-\theta_2$ and $\Delta\omega=\omega_1-\omega_2$,

$$
\dot\phi=\Delta\omega-K\sin\phi.
$$

A locked separation $\phi^*$ requires $\sin\phi^*=\Delta\omega/K$, so locking is possible only when $|\Delta\omega|\le K$.

For the full population there are many relative phases, so no single $\phi$ closes the system. Later, the complex mean field provides a different reduction: every oscillator is compared with the population mean phase $\psi$.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace two trajectories with one equation for their separation.</span></div>
''')

s = src("w6-order")
s = s.replace("<div class=\"two-panel wide-left compact-panels\">", "<p>This is the phase-oscillator counterpart of the polarisation order parameter used for Vicsek agents: both are magnitudes of an average of unit direction vectors.</p>\n\n<div class=\"two-panel wide-left compact-panels\">")
setsrc("w6-order", s)

setsrc("w6-ensemble", r'''## Compare mean field with simulation

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_meanfield_comparison.svg" alt="Continuum Kuramoto mean-field curve compared with a finite numerical ensemble"></div>
<div class="text-panel">
<p>The grey curve is the direct numerical ensemble for \(N=600\).</p>
<p>The orange curve solves the continuum self-consistency equation for the same standard-normal frequency distribution.</p>
<p>Here \(g(0)\) is the height of that frequency-density curve at its centre. The dashed line marks \(K_c=2/[\pi g(0)]\).</p>
</div>
</div>
''')

setsrc("w6-spatial-fireflies-slide", r'''## Put the oscillators back into space

The Kuramoto phase circle is not a physical map.

<table class="compact-table">
<tbody>
<tr><th>Kuramoto</th><td>phase only; all-to-all coupling</td></tr>
<tr><th>Spin Wheels</th><td>fixed positions; local spatial coupling</td></tr>
<tr><th>Swarmalators</th><td>positions and phases both evolve</td></tr>
</tbody>
</table>
''')

# Reader links for the two reductions, Vicsek comparison and g(0).
s = src("phase-difference")
s = s.replace("Locking is possible only when $|\\Delta\\omega|\\le K$.",
              "Locking is possible only when $|\\Delta\\omega|\\le K$.\n\nThis one-variable reduction is special to the two-oscillator problem. For a population there are many pairwise differences, so one relative phase is not enough. The mean-field analysis later introduces $r$ and $\\psi$, comparing each oscillator with the population mean rather than tracking every pair.")
setsrc("phase-difference", s)

s = src("order-parameter")
s = s.replace("This quantity is the **Kuramoto order parameter**.",
              "This quantity is the **Kuramoto order parameter**. It has the same geometry as Vicsek's polarisation order parameter: both take the magnitude of an average of unit direction vectors. The vectors represent headings in Vicsek and phases here.")
setsrc("order-parameter", s)

s = src("mean-field")
s = s.replace("For a symmetric unimodal distribution centred at $\\bar\\omega$, the onset occurs at",
              "For a symmetric unimodal distribution centred at $\\bar\\omega$, the onset occurs at\n\nHere $g(\\bar\\omega)$ is the probability-density height at the centre of the natural-frequency distribution. A taller central peak means more oscillators have similar frequencies and therefore require less coupling to lock. In the rotating frame $\\bar\\omega=0$, so this becomes $g(0)$.\n\nThe onset occurs at")
setsrc("mean-field", s)

path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
