#!/usr/bin/env python3
"""Generate a reproducible critical site-percolation cluster for Week 2."""

from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks/week02/images/critical_percolation_cluster.svg"

size = 96
probability = 0.5927
rng = np.random.default_rng(3024)
occupied = rng.random((size, size)) < probability
visited = np.zeros_like(occupied, dtype=bool)
clusters: list[list[tuple[int, int]]] = []

for row in range(size):
    for col in range(size):
        if not occupied[row, col] or visited[row, col]:
            continue
        cluster: list[tuple[int, int]] = []
        queue = deque([(row, col)])
        visited[row, col] = True
        while queue:
            current_row, current_col = queue.popleft()
            cluster.append((current_row, current_col))
            for delta_row, delta_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = current_row + delta_row
                next_col = current_col + delta_col
                if (
                    0 <= next_row < size
                    and 0 <= next_col < size
                    and occupied[next_row, next_col]
                    and not visited[next_row, next_col]
                ):
                    visited[next_row, next_col] = True
                    queue.append((next_row, next_col))
        clusters.append(cluster)

largest = set(max(clusters, key=len))
cell = 5
margin = 12
canvas = size * cell + 2 * margin
rectangles = []
for row in range(size):
    for col in range(size):
        if not occupied[row, col]:
            continue
        css_class = "largest" if (row, col) in largest else "other"
        rectangles.append(
            f'<rect class="{css_class}" x="{margin + col * cell}" '
            f'y="{margin + row * cell}" width="{cell}" height="{cell}"/>'
        )

OUTPUT.write_text(
    f"""<svg xmlns="http://www.w3.org/2000/svg" width="{canvas}" height="{canvas}"
viewBox="0 0 {canvas} {canvas}">
<style>
  .largest {{ fill: #172B54; }}
  .other {{ fill: #C7D2E5; }}
  @media (prefers-color-scheme: dark) {{
    .largest {{ fill: #EDCC55; }}
    .other {{ fill: #536786; }}
  }}
</style>
{''.join(rectangles)}
</svg>
""",
    encoding="utf-8",
)
print(OUTPUT)
