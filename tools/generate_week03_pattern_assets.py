"""Generate lightweight, reproducible SVG assets for Week 3."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week03/images"
OUT.mkdir(parents=True, exist_ok=True)


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def colour(t, stops=((0, 32, 76), (64, 105, 146), (144, 151, 118), (255, 233, 69))):
    t = min(1.0, max(0.0, float(t)))
    p = t * (len(stops) - 1)
    i = min(int(p), len(stops) - 2)
    return "#%02x%02x%02x" % mix(stops[i], stops[i + 1], p - i)


def gray_scott(n=72, steps=900, seed=7):
    rng = np.random.default_rng(seed)
    u, v = np.ones((n, n)), np.zeros((n, n))
    q, c = n // 12, n // 2
    u[c-q:c+q, c-q:c+q], v[c-q:c+q, c-q:c+q] = 0.50, 0.25
    v += 0.015 * rng.random((n, n))
    for _ in range(steps):
        lu = sum(np.roll(u, s, a) for s, a in ((1, 0), (-1, 0), (1, 1), (-1, 1))) - 4*u
        lv = sum(np.roll(v, s, a) for s, a in ((1, 0), (-1, 0), (1, 1), (-1, 1))) - 4*v
        r = u*v*v
        u += 0.16*lu - r + 0.035*(1-u)
        v += 0.08*lv + r - 0.100*v
    return v


v = gray_scott()
lo, hi = np.quantile(v, [0.02, 0.98])
z = np.clip((v-lo)/(hi-lo), 0, 1)
cell, left, top = 7, 40, 60
rects = []
for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        rects.append(f'<rect x="{left+j*cell}" y="{top+i*cell}" width="{cell+0.2}" height="{cell+0.2}" fill="{colour(z[i,j])}"/>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="590" viewBox="0 0 720 590">
<rect width="720" height="590" fill="white"/>
<text x="360" y="34" text-anchor="middle" font-family="DejaVu Sans" font-size="24" fill="#1B2A4C">One Gray–Scott simulation</text>
{''.join(rects)}
<text x="590" y="285" font-family="DejaVu Sans" font-size="17" fill="#1B2A4C" transform="rotate(90 590 285)">concentration of V</text>
<defs><linearGradient id="g"><stop stop-color="#00204c"/><stop offset=".5" stop-color="#909776"/><stop offset="1" stop-color="#ffe945"/></linearGradient></defs>
<rect x="550" y="90" width="22" height="390" fill="url(#g)"/>
</svg>'''
(OUT / "gray_scott_classic.svg").write_text(svg)

rows = []
palettes = {
    "viridis": ("#440154", "#21918c", "#fde725"),
    "cividis": ("#00204c", "#7c7b78", "#ffe945"),
    "plasma": ("#0d0887", "#cc4778", "#f0f921"),
}
for k, (name, stops) in enumerate(palettes.items()):
    y = 55 + 65*k
    rows.append(f'<text x="105" y="{y+20}" text-anchor="end" font-family="DejaVu Sans" font-size="20" fill="#1B2A4C">{name}</text>')
    for j in range(360):
        t = j/359
        c = colour(t, tuple(tuple(int(s[i:i+2],16) for i in (1,3,5)) for s in stops))
        rows.append(f'<rect x="{125+j}" y="{y}" width="1.4" height="28" fill="{c}"/>')
(OUT / "accessible_matplotlib_colormaps.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" width="540" height="260">'
    '<rect width="100%" height="100%" fill="white"/>'
    '<text x="270" y="28" text-anchor="middle" font-family="DejaVu Sans" font-size="21" fill="#1B2A4C">Perceptually ordered Matplotlib colour maps</text>'
    + ''.join(rows) + '</svg>'
)
