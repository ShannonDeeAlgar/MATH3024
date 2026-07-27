#!/usr/bin/env python3
"""Generate a monochrome Norway/South Africa coastline comparison from Natural Earth."""

from __future__ import annotations

import json
import ssl
import urllib.request
from pathlib import Path

import certifi


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks/week02/images/coastline_extremes.svg"
SOURCE = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_50m_admin_0_countries.geojson"
)


def rings(geometry: dict) -> list[list[list[float]]]:
    if geometry["type"] == "Polygon":
        return [geometry["coordinates"][0]]
    if geometry["type"] == "MultiPolygon":
        return [polygon[0] for polygon in geometry["coordinates"]]
    raise ValueError(f"Unsupported geometry: {geometry['type']}")


def svg_paths(country_rings: list[list[list[float]]], x0: float) -> str:
    points = [point for ring in country_rings for point in ring]
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)
    width, height = max_x - min_x, max_y - min_y
    scale = min(310 / width, 245 / height)
    centre_x, centre_y = (min_x + max_x) / 2, (min_y + max_y) / 2

    paths = []
    for ring in country_rings:
        commands = []
        for index, (longitude, latitude) in enumerate(ring):
            x = x0 + (longitude - centre_x) * scale
            y = 165 - (latitude - centre_y) * scale
            commands.append(f"{'M' if index == 0 else 'L'}{x:.1f},{y:.1f}")
        commands.append("Z")
        paths.append(
            f'<path d="{" ".join(commands)}" fill="#eef1f6" '
            'stroke="#1B2A4C" stroke-width="2.2" vector-effect="non-scaling-stroke"/>'
        )
    return "\n".join(paths)


def main() -> None:
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(SOURCE, context=context) as response:
        dataset = json.load(response)

    selected = {}
    for feature in dataset["features"]:
        properties = feature["properties"]
        code = properties.get("ADM0_A3") or properties.get("ISO_A3")
        if code in {"NOR", "ZAF"}:
            selected[code] = rings(feature["geometry"])

    if selected.keys() != {"NOR", "ZAF"}:
        raise RuntimeError(f"Could not locate both countries: {selected.keys()}")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 360" role="img" aria-labelledby="title desc">
  <title id="title">Coastline outlines of Norway and South Africa</title>
  <desc id="desc">Natural Earth outlines illustrating the highly indented Norwegian coastline and comparatively smoother South African coastline.</desc>
  <rect width="760" height="360" fill="#fff"/>
  <g>{svg_paths(selected["NOR"], 200)}</g>
  <g>{svg_paths(selected["ZAF"], 565)}</g>
  <g font-family="Arial, sans-serif" fill="#1B2A4C" text-anchor="middle">
    <text x="200" y="320" font-size="23" font-weight="700">Norway · 1.37</text>
    <text x="565" y="320" font-size="23" font-weight="700">South Africa · 1.04</text>
    <text x="380" y="350" font-size="15" fill="#64789b">Natural Earth 1:50m outlines · estimates from the cited comparison dataset</text>
  </g>
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
