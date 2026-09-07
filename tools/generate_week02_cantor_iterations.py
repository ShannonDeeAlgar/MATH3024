"""Generate a clean, labelled Cantor-set construction for Week 2."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "notebooks/week02/images/cantor_iterations_clean.svg"

width, height = 1000, 330
left, right = 110, 30
row_y = [55, 125, 195, 265]
line_width = 12


def intervals(depth: int) -> list[tuple[float, float]]:
    current = [(0.0, 1.0)]
    for _ in range(depth):
        current = [
            interval
            for start, end in current
            for interval in (
                (start, start + (end - start) / 3),
                (end - (end - start) / 3, end),
            )
        ]
    return current


elements = [
    f'<rect width="{width}" height="{height}" fill="white"/>',
]
for depth, y in enumerate(row_y):
    elements.append(
        f'<text x="22" y="{y + 7}" font-family="Arial, sans-serif" '
        f'font-size="24" fill="#64789B">k = {depth}</text>'
    )
    for start, end in intervals(depth):
        x1 = left + start * (width - left - right)
        x2 = left + end * (width - left - right)
        elements.append(
            f'<line x1="{x1:.2f}" y1="{y}" x2="{x2:.2f}" y2="{y}" '
            f'stroke="#111111" stroke-width="{line_width}" stroke-linecap="butt"/>'
        )

TARGET.write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    + "\n".join(elements)
    + "\n</svg>\n"
)
print(TARGET)
