"""Create clean vector zooms of the Prisoner's Dilemma and Stag Hunt atlas blocks."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week10/images"
INK = "#1B2A4C"
RULE = "#C7CEDC"
RED = "#C94A4A"
BLUE = "#2C6DA4"
PAPER = "#F4F7FB"


def write_svg(name, rows, cols, pairs, arrows=()):
    x0, y0, cw, ch = 78, 46, 116, 78
    width, height = 350, 236
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">',
        '<defs>',
        f'<marker id="red-head" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="{RED}"/></marker>',
        f'<marker id="blue-head" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="{BLUE}"/></marker>',
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<rect x="{x0}" y="{y0}" width="{2*cw}" height="{2*ch}" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>',
        f'<line x1="{x0+cw}" y1="{y0}" x2="{x0+cw}" y2="{y0+2*ch}" stroke="{RULE}" stroke-width="1.5"/>',
        f'<line x1="{x0}" y1="{y0+ch}" x2="{x0+2*cw}" y2="{y0+ch}" stroke="{RULE}" stroke-width="1.5"/>',
    ]
    for j, label in enumerate(cols):
        out.append(f'<text x="{x0+cw*(j+0.5)}" y="25" text-anchor="middle" font-family="DejaVu Sans" font-size="16" fill="{INK}">{label}</text>')
    for i, label in enumerate(rows):
        out.append(f'<text x="{x0-17}" y="{y0+ch*(i+0.5)+5}" text-anchor="end" font-family="DejaVu Sans" font-size="15" fill="{INK}">{label}</text>')
    for i in range(2):
        for j in range(2):
            a, b = pairs[i][j]
            out.append(f'<text x="{x0+cw*(j+0.5)}" y="{y0+ch*(i+0.5)+6}" text-anchor="middle" font-family="DejaVu Sans" font-size="22" fill="{INK}">({a}, {b})</text>')
    for colour, x1, y1, x2, y2 in arrows:
        marker = "red-head" if colour == RED else "blue-head"
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="4" stroke-linecap="round" marker-end="url(#{marker})"/>')
    out.append('</svg>')
    (OUT / name).write_text("\n".join(out))


def main():
    x0, y0, cw, ch = 78, 46, 116, 78
    pd_arrows = [
        (RED, x0+20, y0+ch-10, x0+20, y0+ch+28),
        (BLUE, x0+cw-20, y0+20, x0+cw+28, y0+20),
        (RED, x0+cw+20, y0+ch-10, x0+cw+20, y0+ch+28),
        (BLUE, x0+cw-20, y0+ch+ch-20, x0+cw+28, y0+ch+ch-20),
    ]
    stag_arrows = [
        (RED, x0+cw+20, y0+ch-10, x0+cw+20, y0+ch+28),
        (BLUE, x0+cw-20, y0+20, x0+cw-68, y0+20),
        (RED, x0+20, y0+ch+ch-20, x0+20, y0+ch+ch-58),
        (BLUE, x0+cw-20, y0+ch+ch-20, x0+cw+28, y0+ch+ch-20),
    ]
    pd = (((3, 3), (1, 4)), ((4, 1), (2, 2)))
    stag = (((4, 4), (1, 3)), ((3, 1), (2, 2)))
    write_svg("atlas_pd_105.svg", ("C", "D"), ("C", "D"), pd)
    write_svg("atlas_pd_106.svg", ("C", "D"), ("C", "D"), pd, pd_arrows)
    write_svg("atlas_stag_105.svg", ("Stag", "Hare"), ("Stag", "Hare"), stag)
    write_svg("atlas_stag_106.svg", ("Stag", "Hare"), ("Stag", "Hare"), stag, stag_arrows)


if __name__ == "__main__":
    main()
