"""Build the four-panel percolation applications image from published sources."""

from io import BytesIO
import os
from pathlib import Path
from urllib.request import Request, urlopen

import certifi
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageOps


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "images" / "percolation_applications.png"
USER_AGENT = "MATH3024-reader-figure/1.0"

SOURCES = {
    "coffee": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Caf%C3%A9_molido.jpg",
    "grid": "https://upload.wikimedia.org/wikipedia/commons/c/ca/500kV_3-Phase_Transmission_Lines.png",
    "epidemic": "https://upload.wikimedia.org/wikipedia/commons/8/82/Early_spread_of_COVID-19_in_Romania_-_imported_cases_from_Italy_and_human-to-human_transmission_networks.pdf",
    "fire": "https://upload.wikimedia.org/wikipedia/commons/6/67/Aerial_photography_of_forest_fire_and_smoke.jpg",
}


LOCAL_NAMES = {
    SOURCES["coffee"]: "percolation_coffee.jpg",
    SOURCES["grid"]: "percolation_grid.png",
    SOURCES["epidemic"]: "epidemic.pdf",
    SOURCES["fire"]: "percolation_fire.jpg",
}


def download(url):
    cache = os.environ.get("PERCOLATION_SOURCE_DIR")
    if cache:
        local_file = Path(cache) / LOCAL_NAMES[url]
        if local_file.exists():
            return local_file.read_bytes()
    request = Request(url, headers={"User-Agent": USER_AGENT})
    import ssl
    context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(request, context=context) as response:
        return response.read()


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def epidemic_network(pdf_bytes):
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = document[4]
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2.4, 2.4), alpha=False)
    page_image = Image.open(BytesIO(pixmap.tobytes("png"))).convert("RGB")
    # Figure 2a: observed human-to-human transmission networks.
    w, h = page_image.size
    return page_image.crop((int(0.10 * w), int(0.045 * h), int(0.64 * w), int(0.36 * h)))


def cover(image, size, focus=(0.5, 0.5)):
    return ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS,
                        centering=focus)


def main():
    images = {
        "coffee": Image.open(BytesIO(download(SOURCES["coffee"]))),
        "grid": Image.open(BytesIO(download(SOURCES["grid"]))),
        "epidemic": epidemic_network(download(SOURCES["epidemic"])),
        "fire": Image.open(BytesIO(download(SOURCES["fire"]))),
    }

    panels = [
        ("coffee", "Coffee extraction", "connected pores carry flow", (0.50, 0.46)),
        ("grid", "Network connectivity", "failures can disconnect a system", (0.50, 0.48)),
        ("epidemic", "Epidemic reach", "contact paths determine spread", (0.48, 0.43)),
        ("fire", "Fire spread", "connected fuel permits propagation", (0.50, 0.50)),
    ]

    width, height = 1600, 420
    margin, gutter = 18, 14
    panel_width = (width - 2 * margin - 3 * gutter) // 4
    panel_height = height - 2 * margin
    header_height, footer_height = 58, 52
    image_height = panel_height - header_height - footer_height
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    title_font = font(27, bold=True)
    note_font = font(19)

    for index, (key, title, note, focus) in enumerate(panels):
        x = margin + index * (panel_width + gutter)
        y = margin
        draw.rounded_rectangle(
            (x, y, x + panel_width, y + panel_height), radius=18,
            fill="#f7f9fc", outline="#cbd5e5", width=3,
        )
        picture = cover(images[key], (panel_width - 6, image_height), focus)
        canvas.paste(picture, (x + 3, y + header_height))
        draw.text((x + panel_width / 2, y + header_height / 2), title,
                  font=title_font, fill="#182c55", anchor="mm")
        draw.text((x + panel_width / 2, y + panel_height - footer_height / 2), note,
                  font=note_font, fill="#536887", anchor="mm")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
