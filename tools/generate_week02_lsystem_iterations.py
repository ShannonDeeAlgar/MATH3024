#!/usr/bin/env python3
"""Generate a crisp, labelled Sierpiński arrowhead L-system construction."""

from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks/week02/images/sierpinski_lsystem_iterations.svg"


def rewrite(word: str) -> str:
    rules = {"F": "G-F-G", "G": "F+G+F"}
    return "".join(rules.get(symbol, symbol) for symbol in word)


def points_for(word: str) -> list[tuple[float, float]]:
    x = y = angle = 0.0
    points = [(x, y)]
    for symbol in word:
        if symbol in "FG":
            x += math.cos(math.radians(angle))
            y -= math.sin(math.radians(angle))
            points.append((x, y))
        elif symbol == "+":
            angle += 60
        elif symbol == "-":
            angle -= 60
    # Rotate so the two endpoints form a horizontal base, then place the
    # construction above that base.
    x0, y0 = points[0]
    x1, y1 = points[-1]
    angle = math.atan2(y1 - y0, x1 - x0)
    cosine, sine = math.cos(-angle), math.sin(-angle)
    rotated = [
        ((x - x0) * cosine - (y - y0) * sine,
         (x - x0) * sine + (y - y0) * cosine)
        for x, y in points
    ]
    base_y = (rotated[0][1] + rotated[-1][1]) / 2
    if sum(y for _, y in rotated) / len(rotated) > base_y:
        rotated = [(x, 2 * base_y - y) for x, y in rotated]
    return rotated


def polyline(points, x0, y0, width, height, scale) -> str:
    xs, ys = zip(*points)
    span_x = max(xs) - min(xs)
    span_y = max(ys) - min(ys)
    used_w, used_h = span_x * scale, span_y * scale
    ox = x0 + (width - used_w) / 2
    # Align every approximation on the same baseline. In particular, k = 0
    # should sit with the bases of the later triangular approximations rather
    # than floating halfway up its panel.
    oy = y0 + height - used_h
    return " ".join(
        f"{ox + (x - min(xs)) * scale:.1f},{oy + (y - min(ys)) * scale:.1f}"
        for x, y in points
    )


depths = [0, 1, 2, 4, 6]
all_words = ["F"]
for _ in range(max(depths)):
    all_words.append(rewrite(all_words[-1]))
words = [all_words[depth] for depth in depths]
# Each rewrite doubles the number of forward steps along a side. Halving the
# turtle step at each depth keeps every approximation in the same physical
# frame, so the sequence shows convergence rather than simple enlargement.
point_sets = [
    [(x * 0.5**depth, y * 0.5**depth) for x, y in points_for(word)]
    for depth, word in zip(depths, words)
]

width, height = 1000, 360
column_x = [25, 220, 415, 610, 805]
plot_width, plot_height = 160, 220
max_span_x = max(max(x for x, _ in points) - min(x for x, _ in points) for points in point_sets)
max_span_y = max(max(y for _, y in points) - min(y for _, y in points) for points in point_sets)
common_scale = min(plot_width / max_span_x, plot_height / max_span_y)
elements = ["""<style>
.curve { fill: none; stroke: #172B54; }
.depth-label { fill: #64789B; }
@media (prefers-color-scheme: dark) {
  .curve { stroke: #E7ECF5; }
  .depth-label { fill: #B8C5DE; }
}
</style>"""]
for depth, points, x in zip(depths, point_sets, column_x):
    elements.append(
        f'<text x="{x + plot_width / 2}" y="330" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="24" '
        f'class="depth-label">k = {depth}</text>'
    )
    elements.append(
        f'<polyline points="{polyline(points, x, 55, plot_width, plot_height, common_scale)}" '
        f'class="curve" stroke-width="5" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )

OUTPUT.write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    + "\n".join(elements)
    + "\n</svg>\n",
    encoding="utf-8",
)
print(OUTPUT)
