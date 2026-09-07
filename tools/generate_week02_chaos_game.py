#!/usr/bin/env python3
"""Generate the clean Week 2 Sierpiński chaos-game animation."""

from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks/week02/images/sierpinski_chaos_game_clean.gif"
WIDTH, HEIGHT = 760, 560
NAVY = "#172b54"
GOLD = "#f2cf57"
PALE = "#d6deeb"


def font(size: int):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main():
    vertices = [(380.0, 52.0), (82.0, 490.0), (678.0, 490.0)]
    rng = random.Random(3024)
    point = (351.0, 277.0)
    points = []
    for _ in range(6200):
        vx, vy = rng.choice(vertices)
        point = ((point[0] + vx) / 2, (point[1] + vy) / 2)
        points.append(point)

    frame_counts = [20, 40, 80, 140, 240, 400, 650, 1000, 1500, 2200, 3100, 4200, 5400, 6200]
    frames = []
    title_font, small_font = font(27), font(20)
    for count in frame_counts:
        image = Image.new("RGB", (WIDTH, HEIGHT), "white")
        draw = ImageDraw.Draw(image)
        draw.line(vertices + [vertices[0]], fill=PALE, width=2)
        for vx, vy in vertices:
            draw.ellipse((vx - 6, vy - 6, vx + 6, vy + 6), fill=GOLD, outline=NAVY, width=2)
        radius = 2 if count < 1200 else 1
        for x, y in points[20:count]:
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=NAVY)
        x, y = points[count - 1]
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=GOLD, outline=NAVY, width=2)
        draw.text((24, 18), "Chaos game", fill=NAVY, font=title_font)
        draw.text((24, 52), f"{count:,} random contractions", fill="#5d6d8d", font=small_font)
        frames.append(image)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=[520] * 8 + [650] * 5 + [1300],
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
