# MATH3024 Reader

Jupyter Book 2 / MyST source for the MATH3024 unit reader.

## Building & previewing

**`./build_reader.sh`** is the only way to see what actually publishes. It copies the project to a temporary workspace, strips `slides-only`/`presenter-notes` cells there (via `prepare_reader_build.py`), and builds the Reader. The live notebooks are never modified, so the command is safe to run with uncommitted work. The finished site is copied to `_build/html`.

**`jupyter-book start`** (the plain MyST dev server) does *not* do that stripping — it serves the raw notebooks as-is. This means `slides-only` cells (the "sized for slides" duplicates of a reader-only section, e.g. Week 1's two "Segregation" cells) show up alongside their `reader-only` counterpart, so the same subsection heading appears twice in the sidebar table of contents. This is a dev-preview artifact only, not a bug in the content — `./build_reader.sh` correctly shows each heading once. Use `jupyter-book start` for fast style/layout iteration, but check anything content- or structure-related (duplicate sections, missing content) against `./build_reader.sh` before concluding something is broken.

Avoid running `prepare_reader_build.py` directly in the working project because it edits notebooks in place. Use `build_reader.sh`, which only invokes it inside the disposable workspace.

## Slides

**`./generate_slides.sh <notebook.ipynb>`** builds a reveal.js deck from a lecture notebook (excluding `reader-only` cells, hiding `hide-input`/`hide-output` cells), at a 16:9 canvas so it fills widescreen displays. It also injects the Reader's typography and `.reader-*` component styles (Voice/Prompt/Emphasis) from `style.css` into the generated slide deck (via `inject_slide_styles.py`), since standalone nbconvert output doesn't load any external stylesheet on its own.

**Always view a generated deck with `./present_slides.sh <notebook.slides.html>`, never by double-clicking the file.** It serves the deck over local HTTP and opens it there. Opening a `.slides.html` file directly (`file://`) gives it a null origin, which breaks every YouTube embed with Error 153 ("Video player configuration error") regardless of `referrerpolicy` — this isn't fixable from the embed side, only by not using `file://`.

The GitHub Pages deployment publishes the Reader at the site root and stages the standalone Week 1 deck at `slides/week01/L_Introduction_to_complex_systems.slides.html`. `stage_slides.sh` copies the deck, its images, and the interactive simulation into the built site after the Reader is generated.

## Changing the visual style

Colours, fonts, and the Voice/Prompt/Emphasis component boxes are all defined once in **`style.css`** — notebook cells use `class="reader-voice"` / `"reader-prompt"` / `"reader-emphasis"` etc. rather than inline styles (confirmed: MyST's HTML sanitizer preserves `class` and `style` on `<div>`, unlike on `<img>` where `style` is stripped — see `fix_image_sizing.py`). `generate_slides.sh` copies the relevant rules out of `style.css` into each generated slide deck automatically, so a single edit there covers both the Reader and slides — no notebook changes needed to restyle. Only week01 has been re-skinned to this system so far; weeks 2–10 still carry the old teal styling.
