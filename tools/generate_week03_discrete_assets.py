"""Generate explanatory SVGs for grid indexing and a discrete Laplacian."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week03/images"
OUT.mkdir(parents=True, exist_ok=True)


def grid_index_svg():
    n, size, x0, y0 = 5, 76, 120, 80
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="680" height="540">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="340" y="35" text-anchor="middle" font-family="DejaVu Sans" font-size="24" fill="#1B2A4C">A continuous field sampled on a grid</text>',
    ]
    for i in range(n):
        for j in range(n):
            selected = i == 2 and j == 3
            fill = "#EDCC55" if selected else ("#E7EDF6" if (i+j) % 2 == 0 else "#F7F9FC")
            x, y = x0 + j*size, y0 + i*size
            parts.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{fill}" stroke="#8DA0BD" stroke-width="2"/>')
            label = "U₂,₃" if selected else f"U{i},{j}"
            parts.append(f'<text x="{x+size/2}" y="{y+size/2+7}" text-anchor="middle" font-family="Georgia" font-size="20" fill="#1B2A4C">{label}</text>')
    parts += [
        '<text x="82" y="275" text-anchor="middle" font-family="DejaVu Sans" font-size="20" fill="#5A6685" transform="rotate(-90 82 275)">row index i</text>',
        '<text x="310" y="495" text-anchor="middle" font-family="DejaVu Sans" font-size="20" fill="#5A6685">column index j</text>',
        '<text x="525" y="310" font-family="DejaVu Sans" font-size="19" fill="#1B2A4C">Uᵢ,ⱼ ≈ U(xᵢ,yⱼ,t)</text>',
        '</svg>',
    ]
    return "".join(parts)


def laplacian_svg():
    values = [[0, 2, 0], [1, 4, 3], [0, 2, 0]]
    weights = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="980" height="420">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="190" y="38" text-anchor="middle" font-family="DejaVu Sans" font-size="23" fill="#1B2A4C">local field values</text>',
        '<text x="500" y="38" text-anchor="middle" font-family="DejaVu Sans" font-size="23" fill="#1B2A4C">five-point stencil L</text>',
    ]
    for block, data, x0 in (("field", values, 70), ("weights", weights, 380)):
        for i in range(3):
            for j in range(3):
                x, y = x0+j*78, 70+i*78
                active = weights[i][j] != 0
                fill = "#EDCC55" if (block == "field" and i == 1 and j == 1) else ("#DDE6F2" if active else "#FFFFFF")
                parts.append(f'<rect x="{x}" y="{y}" width="78" height="78" fill="{fill}" stroke="#8DA0BD" stroke-width="2"/>')
                parts.append(f'<text x="{x+39}" y="{y+48}" text-anchor="middle" font-family="DejaVu Sans" font-size="25" fill="#1B2A4C">{data[i][j]}</text>')
    parts += [
        '<text x="335" y="205" text-anchor="middle" font-family="Georgia" font-size="38" fill="#1B2A4C">∗</text>',
        '<text x="655" y="205" text-anchor="middle" font-family="Georgia" font-size="38" fill="#1B2A4C">=</text>',
        '<text x="800" y="150" text-anchor="middle" font-family="DejaVu Sans" font-size="23" fill="#1B2A4C">2 + 1 + 3 + 2 − 4(4)</text>',
        '<text x="800" y="205" text-anchor="middle" font-family="DejaVu Sans" font-size="38" font-weight="bold" fill="#1B2A4C">−8</text>',
        '<text x="800" y="255" text-anchor="middle" font-family="DejaVu Sans" font-size="20" fill="#5A6685">negative: the centre is a local peak</text>',
        '<text x="490" y="355" text-anchor="middle" font-family="DejaVu Sans" font-size="20" fill="#1B2A4C">The convolution repeats this weighted neighbour comparison at every grid cell.</text>',
        '</svg>',
    ]
    return "".join(parts)


(OUT / "grid_indexing_Uij.svg").write_text(grid_index_svg())
(OUT / "laplacian_convolution_example.svg").write_text(laplacian_svg())
