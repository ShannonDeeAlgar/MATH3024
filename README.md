# MATH3024 Reader

Jupyter Book 2 / MyST source for the MATH3024 unit reader.

## Building & previewing

**`./build_reader.sh`** is the only way to see what actually publishes. It strips `slides-only`/`presenter-notes` cells (via `prepare_reader_build.py`) before building, matching what CI produces, then restores the real notebooks afterward via `git checkout -- notebooks/`.

**`jupyter-book start`** (the plain MyST dev server) does *not* do that stripping — it serves the raw notebooks as-is. This means `slides-only` cells (the "sized for slides" duplicates of a reader-only section, e.g. Week 1's two "Segregation" cells) show up alongside their `reader-only` counterpart, so the same subsection heading appears twice in the sidebar table of contents. This is a dev-preview artifact only, not a bug in the content — `./build_reader.sh` correctly shows each heading once. Use `jupyter-book start` for fast style/layout iteration, but check anything content- or structure-related (duplicate sections, missing content) against `./build_reader.sh` before concluding something is broken.

Because `build_reader.sh` reverts `notebooks/` on exit (even mid-session, including any of your own uncommitted edits), avoid running `prepare_reader_build.py` directly outside of it, and commit notebook edits before re-running a verification build.

## Slides

**`./generate_slides.sh <notebook.ipynb>`** builds a reveal.js deck from a lecture notebook (excluding `reader-only` cells, hiding `hide-input`/`hide-output` cells), at a 16:9 canvas so it fills widescreen displays. It also injects the Reader's typography and `.reader-*` component styles (Voice/Prompt/Emphasis) from `style.css` into the generated slide deck (via `inject_slide_styles.py`), since standalone nbconvert output doesn't load any external stylesheet on its own.

## Changing the visual style

Colours, fonts, and the Voice/Prompt/Emphasis component boxes are all defined once in **`style.css`** — notebook cells use `class="reader-voice"` / `"reader-prompt"` / `"reader-emphasis"` etc. rather than inline styles (confirmed: MyST's HTML sanitizer preserves `class` and `style` on `<div>`, unlike on `<img>` where `style` is stripped — see `fix_image_sizing.py`). `generate_slides.sh` copies the relevant rules out of `style.css` into each generated slide deck automatically, so a single edit there covers both the Reader and slides — no notebook changes needed to restyle. Only week01 has been re-skinned to this system so far; weeks 2–10 still carry the old teal styling.

**`./present_slides.sh <notebook.slides.html>`** serves a generated deck over local HTTP and opens it — opening a `.slides.html` file directly (`file://`) breaks YouTube embeds (null origin rejected by YouTube).
