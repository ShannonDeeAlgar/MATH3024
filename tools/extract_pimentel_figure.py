from pathlib import Path

import fitz
from PIL import Image


source = Path("/tmp/pimentel_2008.pdf")
page_output = Path("/tmp/pimentel_2008_page3.png")

document = fitz.open(source)
page = document[2]
pixmap = page.get_pixmap(matrix=fitz.Matrix(5, 5), alpha=False)
pixmap.save(page_output)

image = Image.open(page_output)
# Figure 1 and its caption occupy the upper-left part of the rendered page.
figure = image.crop((200, 175, 1317, 1125))
figure_output = Path("notebooks/week05/images/pimentel_2008_noise_transitions.png")
figure_output.parent.mkdir(parents=True, exist_ok=True)
figure.save(figure_output)

print(figure_output)
