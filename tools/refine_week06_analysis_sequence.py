"""Refine the Week 6 beats, coupling, phase-reduction and animation sequence."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def lines(text):
    return text.splitlines(keepends=True)


def set_cell(cells, cell_id, text):
    cell = next(cell for cell in cells if cell.get("id") == cell_id)
    cell["source"] = lines(text.rstrip() + "\n")


def main():
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]

    set_cell(cells, "w6-beats", r"""## Beats are not synchronisation

<img src="images/phase_signals_uncoupled.svg" alt="Two uncoupled oscillatory signals, their sum and their drifting phase difference" style="display:block;max-height:500px;max-width:100%;margin:0 auto">

Several slow beat cycles are visible in the sum. Neither oscillator responds to the other: the phase difference continues to drift.""")

    set_cell(cells, "w6-coupling", r"""## Add coupling

Suppose oscillator 2 influences oscillator 1:

$$
\dot{\theta}_1=\omega_1+K\sin(\theta_2-\theta_1),
$$

$$
\dot{\theta}_2=\omega_2.
$$

The sine is the simplest smooth, periodic interaction with the required symmetry: no correction when phases agree, opposite corrections for leading and lagging, and the same rule after a full turn. $K$ controls its strength.

<img src="images/phase_signals_coupled.svg" alt="Two coupled oscillatory signals, their sum and a phase difference approaching a constant" style="display:block;max-height:335px;max-width:100%;margin:0 auto">""")

    set_cell(cells, "w6-relative", r"""## Reduce to their relative phase

The two phases contain more information than we need to decide whether they lock. A useful analysis should remove their shared rotation and retain only their separation.

With $\phi=\theta_1-\theta_2$ and $\Delta\omega=\omega_1-\omega_2$,

$$
\dot\phi=\Delta\omega-K\sin\phi.
$$

A locked separation $\phi^*$ requires

$$
\sin\phi^*=\frac{\Delta\omega}{K},
$$

so locking is possible only when $|\Delta\omega|\le K$.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace two trajectories with one equation for their separation.</span></div>""")

    set_cell(cells, "w6-watch", r"""## Qualitative analysis · watch phases organise

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_phase_organisation.gif" alt="Simulation of Kuramoto phases organising while collective coherence increases" style="display:block;max-height:410px;max-width:100%;margin:auto"></div>
<div class="text-panel"><p>Each point is one oscillator phase. The orange vector is their mean.</p><p>Follow both the individual phases and the coherence $r$.</p><div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> inspect individual phases before compressing them into one statistic.</span></div></div>
</div>""")

    set_cell(cells, "reader-beats", r"""Beats arise from adding two uncoupled oscillatory signals with nearby frequencies. The envelope varies slowly, but neither oscillator changes its frequency in response to the other. That is not spontaneous synchronisation. The longer time window below shows several beat cycles. Once coupling is added, one oscillator can adjust its instantaneous frequency; if phase locking occurs, the phase difference approaches a constant.

<img src="images/phase_signal_comparison.svg" alt="Uncoupled and coupled oscillators compared through their signals, summed signal and phase difference" style="display:block;max-width:100%;margin:0 auto">""")

    set_cell(cells, "two-coupled", r"""## Add coupling

Suppose oscillator 2 drives oscillator 1:

$$
\dot{\theta}_1=\omega_1+K\sin(\theta_2-\theta_1),
$$

$$
\dot{\theta}_2=\omega_2.
$$

Why a sine? The phase difference is an angle, so the interaction should be periodic. The simplest non-constant Fourier term is $\sin\phi$. It is zero at agreement, changes sign when the leader changes, and produces the strongest correction at a quarter-cycle separation. It is also the leading-order interaction obtained for many weakly coupled oscillators after reducing their dynamics to phase.

This is a useful minimal choice, not the only possible coupling law. A general phase model could use

$$
\dot\theta_i=\omega_i+K\,\Gamma(\theta_j-\theta_i),
$$

with another periodic function $\Gamma$: higher harmonics can favour several phase clusters; pulse coupling is more natural for brief flashes; delays, asymmetric influence and distance-dependent weights can also be included. $K$ controls coupling strength.""")

    set_cell(cells, "phase-difference", r"""## Reduce to phase difference

Tracking both phases is useful for reconstructing their motion, but synchronisation concerns their relationship. We can reduce the two-dimensional state $(\theta_1,\theta_2)$ to the single relative phase

$$
\phi=\theta_1-\theta_2.
$$

This removes the rotation shared by both oscillators and keeps the quantity that distinguishes drift from locking. With $\Delta\omega=\omega_1-\omega_2$,

$$
\dot{\phi}=\Delta\omega-K\sin\phi.
$$

A phase-locked state requires $\dot\phi=0$, so

$$
\sin\phi^\ast=\frac{\Delta\omega}{K}.
$$

Locking is possible only when $|\Delta\omega|\le K$.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> two trajectories become one equation for their relative phase. Dimension reduction is especially transparent here because there are only two oscillators.</span></div>""")

    set_cell(cells, "kuramoto-video", r"""## Qualitative analysis · watch phases organise

<img src="images/kuramoto_phase_organisation.gif" alt="Simulation of Kuramoto phases organising while collective coherence increases" style="display:block;max-height:540px;max-width:100%;margin:auto">

*Each point is one oscillator phase. The orange vector is their mean; the time series records its length $r$.*""")

    # The local animation supersedes the old external/static follow-up.
    set_cell(cells, "w6-3465fc0be5", r"""### From phases to coherence

The animation shows the two levels of description together. Individual phases remain visible on the circle, while the order parameter $r$ records their collective alignment. This prepares the move from qualitative inspection to a quantitative measure.""")

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
