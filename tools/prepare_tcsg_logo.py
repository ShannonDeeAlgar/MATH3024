#!/usr/bin/env python3
"""Create the light-mode TCSG logo from the supplied raster, preserving its mark."""

import sys
from pathlib import Path
from PIL import Image


source, target = map(Path, sys.argv[1:3])
im = Image.open(source).convert("RGBA")
px = im.load()
w, h = im.size
bg = px[0, 0][:3]

for y in range(h):
    for x in range(w):
        r, g, b, _ = px[x, y]
        # Remove the nearly uniform charcoal field with a soft antialiased edge.
        distance = ((r-bg[0])**2 + (g-bg[1])**2 + (b-bg[2])**2) ** 0.5
        if distance < 35:
            px[x, y] = (0, 0, 0, 0)
            continue
        edge_alpha = max(0, min(255, round((distance - 35) / 55 * 255)))
        # Recolour only the T/S/G and subtitle; retain white network lines in C.
        is_letter_region = (y > h * 0.62) or (h * 0.31 < y < h * 0.61 and (x < w * 0.25 or x > w * 0.48))
        if is_letter_region and min(r, g, b) > 175 and max(r, g, b) - min(r, g, b) < 20:
            px[x, y] = (0, 0, 0, edge_alpha)
        else:
            px[x, y] = (r, g, b, edge_alpha)

target.parent.mkdir(parents=True, exist_ok=True)
im.save(target)
print(f"Saved {target} ({w}x{h}, RGBA)")
