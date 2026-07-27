#!/usr/bin/env python3
"""Extract Figure 1 from Mandelbrot's 1980 paper for the Week 2 Reader."""

from pathlib import Path

import fitz
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PDF = Path("/tmp/mandelbrot_1980.pdf")
OUTPUT = ROOT / "notebooks/week02/images/mandelbrot_1980_figure1.png"

document = fitz.open(PDF)
page = document[1]
pixmap = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), alpha=False)
page_image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)

# Retain the historical parameter-plane image and its original caption.
figure = page_image.crop((65, 205, 985, 1195))
figure.save(OUTPUT, optimize=True)
print(f"Wrote {OUTPUT}")
