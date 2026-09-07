"""Clarify the rotating frame and solution branches in Week 6."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


READER = r'''## Analytical mean-field analysis

### What the analytical result adds

The numerical analysis describes chosen finite populations, observation times and parameter values. The analytical calculation asks a broader question: in an idealised infinite, all-to-all population with a known distribution of natural frequencies, when can a coherent state exist?

It can predict a critical coupling and provide a benchmark for the numerical ensemble. It does not retain finite-population fluctuations, transient times, irregular networks, noise or a particular initial condition.

### Exact collective-field rewriting

For the finite all-to-all model, define

$$
r(t)e^{\mathrm{i}\psi(t)}=\dfrac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

This is a definition. It allows the interaction sum to be rewritten exactly as

$$
\dot\theta_i=\omega_i+Kr(t)\sin\bigl(\psi(t)-\theta_i\bigr).
$$

No mean-field approximation has yet been made. The continuum step replaces the finite frequency sample by a probability density.

### Move with the collective rotation

Suppose the coherent population rotates at long-time angular frequency $\Omega$. Define the frequency relative to that collective rotation by

$$
\nu=\omega-\Omega.
$$

Let $h(\nu)$ be the density of these relative frequencies. It is the original laboratory-frame density shifted along the horizontal axis:

$$
h(\nu)=g(\Omega+\nu).
$$

Thus $h(0)=g(\Omega)$ is simply the height of the natural-frequency density at the collective frequency. For the symmetric distributions used here, $\Omega$ is the centre of the distribution. The earlier notation $\bar\omega$ referred to this centre; using $\Omega$ and $\nu$ keeps the population rotation distinct from an individual frequency.

In this rotating frame, a frequency-locked oscillator has a constant relative phase $\phi$ satisfying

$$
\nu=Kr\sin\phi.
$$

Therefore only oscillators with $|\nu|\le Kr$ can lock. Oscillators further into the tails continue to drift.

### The self-consistency equation has two branches

For a symmetric unimodal density, the locked oscillators contribute

$$
r=Kr\int_{-\pi/2}^{\pi/2}\cos^2\phi\;h\bigl(Kr\sin\phi\bigr)\,\mathrm d\phi.
$$

This form makes an important point visible: $r=0$ is a solution for every $K$. It is the incoherent branch.

To find a non-zero coherent branch, assume $r>0$ and divide by $r$:

$$
1=K\int_{-\pi/2}^{\pi/2}\cos^2\phi\;h\bigl(Kr\sin\phi\bigr)\,\mathrm d\phi.
$$

Dividing by $r$ removes the $r=0$ solution from view. This is why the second equation alone does not look piecewise.

At the onset of coherence, the non-zero branch approaches $r\to0^+$. Hence $h(Kr\sin\phi)\to h(0)$ and

$$
1=K_c h(0)\int_{-\pi/2}^{\pi/2}\cos^2\phi\,\mathrm d\phi
=K_c h(0)\frac{\pi}{2}.
$$

It follows that

$$
K_c=\frac{2}{\pi h(0)}=\frac{2}{\pi g(\Omega)}.
$$

Below $K_c$, the stable solution is the incoherent branch $r_\infty=0$. Above $K_c$, that branch loses stability and a stable positive solution appears. The physically relevant continuum prediction is therefore

$$
r_\infty(K)=
\begin{cases}
0, & K\le K_c,\\
\text{the positive solution of the self-consistency equation}, & K>K_c.
\end{cases}
$$

This derivation is useful context but is not assessable. See [Strogatz (2000), “From Kuramoto to Crawford”](https://doi.org/10.1016/S0167-2789(00)00094-4) for the full stability analysis.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace one finite list of natural frequencies by the population density <i>h</i>(<i>ν</i>).</span></div>
'''


COMPARISON = r'''### Compare analytical and numerical results

<img src="images/kuramoto_meanfield_comparison.svg" alt="Continuum Kuramoto curve compared with a finite numerical ensemble">

Both results use natural frequencies drawn from $\mathcal N(3,1)$. The collective frequency is therefore $\Omega=3$, and the relative frequencies $\nu=\omega-3$ have the standard-normal density

$$
h(\nu)=\frac{1}{\sqrt{2\pi}}e^{-\nu^2/2}.
$$

At the centre,

$$
h(0)=\frac{1}{\sqrt{2\pi}},
\qquad
K_c=\frac{2}{\pi h(0)}=\sqrt{\frac{8}{\pi}}.
$$

The orange continuum curve is produced as follows:

1. set $r_\infty=0$ for $K\le K_c$;
2. for each $K>K_c$, solve the positive-branch self-consistency equation numerically for $r_\infty$.

The grey curve is an ensemble of finite simulations with $N=600$. It approaches the continuum result but retains sampling variation and a rounded onset. The orange curve is therefore not one simulated trajectory, and for a Gaussian frequency distribution it is not a simple closed-form formula above $K_c$.
'''


SLIDE = r'''## Heterogeneity sets the onset

Move with the collective rotation at rate $\Omega$ and define

$$
\nu=\omega-\Omega,
\qquad
h(\nu)=g(\Omega+\nu).
$$

Here $h(0)$ is the height of the natural-frequency density at its centre. The onset of coherence is

$$
K_c=\frac{2}{\pi h(0)}.
$$

The self-consistency equation has two branches:

$$
r_\infty=0 \quad (K\le K_c),
$$

while for $K>K_c$, $r_\infty$ is the positive solution. The derivation is reader-only and not assessable.
'''


def source(text):
    return text.splitlines(keepends=True)


nb = json.loads(PATH.read_text())
found = set()
for cell in nb["cells"]:
    cid = cell.get("id")
    if cid == "mean-field":
        cell["source"] = source(READER)
        found.add(cid)
    elif cid == "ensemble":
        cell["source"] = source(COMPARISON)
        found.add(cid)
    elif cid == "w6-onset-result-slide":
        cell["source"] = source(SLIDE)
        found.add(cid)

expected = {"mean-field", "ensemble", "w6-onset-result-slide"}
if found != expected:
    raise RuntimeError(f"Expected {expected}; found {found}")

PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
print(PATH)
