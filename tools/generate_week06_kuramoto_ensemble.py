"""Generate Week 6 numerical sweeps and their mean-field comparison."""

from pathlib import Path

import numpy as np


NAVY = "#172A52"
BLUE = "#4A90C2"
LIGHT_BLUE = "#8CB9D8"
ORANGE = "#D95F3B"
GOLD = "#F2C94C"
GREY = "#9AA7B8"
GRID = "#D7DFED"
OUT = Path(__file__).resolve().parents[1] / "notebooks/week06/images"


def sweep_population(rng, n, repeats, couplings, dt=0.04, burn=900, sample=240):
    """Use the same sampled populations across K, but restart each condition."""
    omega = rng.normal(0.0, 1.0, (repeats, n))
    initial = rng.uniform(0.0, 2.0 * np.pi, (repeats, n))
    values = np.empty((len(couplings), repeats))
    for index, coupling in enumerate(couplings):
        theta = initial.copy()
        total = np.zeros(repeats)
        for step in range(burn + sample):
            z = np.mean(np.exp(1j * theta), axis=1)
            theta += dt * (omega + coupling * np.imag(z[:, None] * np.exp(-1j * theta)))
            theta %= 2.0 * np.pi
            if step >= burn:
                total += np.abs(np.mean(np.exp(1j * theta), axis=1))
        values[index] = total / sample
    return values


def normal_density(x):
    return np.exp(-0.5 * x * x) / np.sqrt(2.0 * np.pi)


def mean_field_coherence(coupling):
    """Solve the Gaussian Kuramoto self-consistency equation for non-zero r."""
    critical = np.sqrt(8.0 / np.pi)
    if coupling <= critical:
        return 0.0
    x = np.linspace(-1.0, 1.0, 4001)
    weight = np.sqrt(np.maximum(0.0, 1.0 - x * x))

    def residual(r):
        integral = coupling * r * np.trapezoid(weight * normal_density(coupling * r * x), x)
        return integral - r

    lo, hi = 1e-7, 1.0
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def polygon_band(couplings, mean, sd, sx, sy):
    upper = [(sx(k), sy(min(1.0, m + s))) for k, m, s in zip(couplings, mean, sd)]
    lower = [(sx(k), sy(max(0.0, m - s))) for k, m, s in zip(couplings, mean, sd)][::-1]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in upper + lower)


def base_svg():
    width, height = 1000, 570
    left, right, top, bottom = 105, 35, 105, 75
    plot_w, plot_h = width-left-right, height-top-bottom
    sx = lambda value: left + plot_w * value / 4.0
    sy = lambda value: top + plot_h * (1.0-value)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<style>text{{font-family:DejaVu Sans,sans-serif;fill:{NAVY}}}.axis{{stroke:{NAVY};stroke-width:2}}.grid{{stroke:{GRID};stroke-width:1}}</style>',
    ]
    for tick in np.linspace(0, 1, 6):
        y = sy(tick)
        svg += [f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/>',
                f'<text x="{left-15}" y="{y+7:.1f}" text-anchor="end" font-size="21">{tick:.1f}</text>']
    for tick in range(5):
        x = sx(tick)
        svg += [f'<line class="grid" x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}"/>',
                f'<text x="{x:.1f}" y="{height-bottom+31}" text-anchor="middle" font-size="21">{tick}</text>']
    svg += [
        f'<line class="axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}"/>',
        f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}"/>',
        f'<text x="{left+plot_w/2:.1f}" y="{height-15}" text-anchor="middle" font-size="26">Coupling, K</text>',
        f'<text x="27" y="{top+plot_h/2:.1f}" text-anchor="middle" font-size="25" transform="rotate(-90 27 {top+plot_h/2:.1f})">Long-time coherence, r∞</text>',
    ]
    return svg, sx, sy, width, height, top, bottom


def numerical_figure(couplings, results):
    svg, sx, sy, width, height, top, bottom = base_svg()
    colours = {60: LIGHT_BLUE, 180: BLUE, 600: NAVY}
    legend_x = 185
    for index, n in enumerate((60, 180, 600)):
        values = results[n]
        mean, sd = values.mean(axis=1), values.std(axis=1, ddof=1)
        colour = colours[n]
        svg.append(f'<polygon points="{polygon_band(couplings, mean, sd, sx, sy)}" fill="{colour}" opacity="0.13"/>')
        points = " ".join(f"{sx(k):.1f},{sy(v):.1f}" for k, v in zip(couplings, mean))
        svg.append(f'<polyline points="{points}" fill="none" stroke="{colour}" stroke-width="3"/>')
        for k, value in zip(couplings, mean):
            svg.append(f'<circle cx="{sx(k):.1f}" cy="{sy(value):.1f}" r="3.5" fill="{colour}"/>')
        x = legend_x + index*220
        svg += [f'<line x1="{x}" y1="47" x2="{x+45}" y2="47" stroke="{colour}" stroke-width="4"/>',
                f'<text x="{x+55}" y="55" font-size="22">N = {n}</text>']
    svg.append('</svg>')
    (OUT / "kuramoto_numerical_sweep.svg").write_text("\n".join(svg))


def comparison_figure(couplings, results):
    svg, sx, sy, width, height, top, bottom = base_svg()
    values = results[600]
    mean, sd = values.mean(axis=1), values.std(axis=1, ddof=1)
    svg.append(f'<polygon points="{polygon_band(couplings, mean, sd, sx, sy)}" fill="{GREY}" opacity="0.17"/>')
    points = " ".join(f"{sx(k):.1f},{sy(v):.1f}" for k, v in zip(couplings, mean))
    svg.append(f'<polyline points="{points}" fill="none" stroke="{GREY}" stroke-width="3"/>')
    theory_k = np.linspace(0.0, 4.0, 161)
    theory_r = np.array([mean_field_coherence(k) for k in theory_k])
    theory_points = " ".join(f"{sx(k):.1f},{sy(v):.1f}" for k, v in zip(theory_k, theory_r))
    svg.append(f'<polyline points="{theory_points}" fill="none" stroke="{ORANGE}" stroke-width="5"/>')
    critical = np.sqrt(8.0/np.pi)
    svg.append(f'<line x1="{sx(critical):.1f}" y1="{top}" x2="{sx(critical):.1f}" y2="{height-bottom}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="9 7"/>')
    svg.append(
        f'<text x="{sx(critical)+10:.1f}" y="{top+26}" font-size="22">'
        'critical coupling <tspan font-style="italic">K</tspan>'
        '<tspan baseline-shift="sub" font-size="15">c</tspan></text>'
    )
    svg += [
        f'<line x1="115" y1="47" x2="160" y2="47" stroke="{GREY}" stroke-width="4"/><text x="170" y="55" font-size="22">finite simulation, N = 600</text>',
        f'<line x1="525" y1="47" x2="570" y2="47" stroke="{ORANGE}" stroke-width="5"/><text x="580" y="55" font-size="22">continuum mean-field</text>',
        '</svg>',
    ]
    (OUT / "kuramoto_meanfield_comparison.svg").write_text("\n".join(svg))


def main():
    rng = np.random.default_rng(3024)
    couplings = np.linspace(0.0, 4.0, 17)
    specifications = {60: 14, 180: 10, 600: 6}
    results = {n: sweep_population(rng, n, repeats, couplings) for n, repeats in specifications.items()}
    numerical_figure(couplings, results)
    comparison_figure(couplings, results)
    np.savez(OUT / "kuramoto_sweep_data.npz", couplings=couplings, **{f"N{n}": values for n, values in results.items()})
    print(OUT / "kuramoto_numerical_sweep.svg")
    print(OUT / "kuramoto_meanfield_comparison.svg")


if __name__ == "__main__":
    main()
