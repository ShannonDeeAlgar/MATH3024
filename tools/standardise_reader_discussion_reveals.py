#!/usr/bin/env python3
"""Combine Reader discussion prompts and supplied responses into one reveal.

Standalone prompts remain visible discussion markers.  Only prompts with a
supplied response are converted; calculation and optional-detail reveals keep
their existing semantics.
"""

from __future__ import annotations

import re
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
LECTURES = sorted((ROOT / "notebooks").glob("week*/L_*.ipynb"))

MARKER_RE = re.compile(
    r'<div class="discussion-marker"[^>]*>\s*<img[^>]*>\s*<span>(.*?)</span>\s*</div>',
    re.IGNORECASE | re.DOTALL,
)
PROMPT_RE = re.compile(
    r'<div class="reader-prompt">.*?<div class="reader-prompt-body(?: italic)?">'
    r'(.*?)</div>\s*</div>',
    re.IGNORECASE | re.DOTALL,
)
FOUNDATION_RE = re.compile(
    r'<div style="border-left:\s*4px solid #1e70bf;.*?">\s*'
    r'<strong>Check your foundational understanding:</strong><br>\s*'
    r'(.*?)\s*</div>',
    re.IGNORECASE | re.DOTALL,
)
ADMONITION_RE = re.compile(
    r':::\{admonition\}\s*Discussion\s*\n:class:\s*discussion\s*\n'
    r'(.*?)\n:::',
    re.IGNORECASE | re.DOTALL,
)
DROPDOWN_RE = re.compile(
    r'```\{dropdown\}\s*my answers?\.{0,3}\s*\n(.*?)\n```',
    re.IGNORECASE | re.DOTALL,
)
DETAILS_RE = re.compile(
    r'<details(?P<attrs>[^>]*)>\s*<summary>(?P<summary>.*?)</summary>'
    r'(?P<body>.*?)</details>',
    re.IGNORECASE | re.DOTALL,
)


def clean_question(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def clean_answer(text: str) -> str:
    answer = text.strip()
    wrapper = re.fullmatch(
        r'<div class="discussion-answer">\s*(.*?)\s*</div>',
        answer,
        re.IGNORECASE | re.DOTALL,
    )
    if wrapper:
        answer = wrapper.group(1).strip()
    return answer


def reveal(question: str, answer: str) -> str:
    question = clean_question(question)
    answer = clean_answer(answer)
    return f'''<details class="discussion-reveal">
<summary><img src="images/discussion_marker.svg" alt=""><span class="discussion-reveal-heading"><span class="discussion-reveal-label">Discussion question</span><span class="discussion-reveal-question">{question}</span></span></summary>
<div class="discussion-answer">

{answer}

</div>
</details>'''


def extract_question(source: str):
    """Return (question, source_without_prompt), or (None, source)."""
    for pattern in (MARKER_RE, PROMPT_RE, FOUNDATION_RE, ADMONITION_RE):
        match = pattern.search(source)
        if match:
            without = source[: match.start()] + source[match.end() :]
            return match.group(1), without.rstrip()
    return None, source


def details_answer(match: re.Match) -> str | None:
    summary = clean_question(match.group("summary"))
    attrs = match.group("attrs")
    if "discussion-reveal" in attrs:
        return match.group("body")
    if re.fullmatch(r"my answers?\.{0,3}", summary, re.IGNORECASE):
        return match.group("body")
    if "reader-answer" in attrs and summary.lower() != "show the calculation":
        return match.group("body")
    return None


def convert_same_cell(source: str):
    """Convert a prompt and supplied answer that occupy one markdown cell."""
    question_match = None
    for pattern in (MARKER_RE, ADMONITION_RE):
        candidate = pattern.search(source)
        if candidate and (question_match is None or candidate.start() < question_match.start()):
            question_match = candidate
    if not question_match:
        return source, False

    dropdown = DROPDOWN_RE.search(source, question_match.end())
    details = DETAILS_RE.search(source, question_match.end())
    answer_match = None
    answer = None
    if dropdown and (not details or dropdown.start() < details.start()):
        answer_match = dropdown
        answer = dropdown.group(1)
    elif details:
        candidate = details_answer(details)
        if candidate is not None:
            answer_match = details
            answer = candidate
    if answer_match is None:
        return source, False

    combined = reveal(question_match.group(1), answer)
    updated = source[: question_match.start()] + combined + source[answer_match.end() :]
    return updated.strip(), True


def normalise_existing(source: str):
    changed = False

    def replacement(match: re.Match):
        nonlocal changed
        if "discussion-reveal" not in match.group("attrs"):
            return match.group(0)
        # A rerun should leave the shared component unchanged.
        if "discussion-reveal-heading" in match.group("summary"):
            return match.group(0)
        changed = True
        return reveal(match.group("summary"), match.group("body"))

    return DETAILS_RE.sub(replacement, source), changed


def main():
    totals = {"combined": 0, "normalised": 0}
    for path in LECTURES:
        notebook = nbformat.read(path, as_version=4)
        file_changed = False

        # First handle prompt/answer pairs contained in a single cell.
        for cell in notebook.cells:
            if cell.cell_type != "markdown":
                continue
            cell.source, changed = convert_same_cell(cell.source)
            totals["combined"] += int(changed)
            file_changed = file_changed or changed

        # Then handle an answer cell immediately following its prompt cell.
        for index in range(1, len(notebook.cells)):
            answer_cell = notebook.cells[index]
            prompt_cell = notebook.cells[index - 1]
            if answer_cell.cell_type != "markdown" or prompt_cell.cell_type != "markdown":
                continue

            answer = None
            dropdown = DROPDOWN_RE.fullmatch(answer_cell.source.strip())
            details = DETAILS_RE.fullmatch(answer_cell.source.strip())
            if dropdown:
                answer = dropdown.group(1)
            elif details:
                answer = details_answer(details)
            if answer is None:
                continue

            question, shortened = extract_question(prompt_cell.source)
            if question is None:
                continue
            prompt_cell.source = shortened
            answer_cell.source = reveal(question, answer)
            totals["combined"] += 1
            file_changed = True

        # Finally give pre-combined discussion reveals the full shared markup.
        for cell in notebook.cells:
            if cell.cell_type != "markdown":
                continue
            cell.source, changed = normalise_existing(cell.source)
            totals["normalised"] += int(changed)
            file_changed = file_changed or changed

        if file_changed:
            nbformat.validate(notebook)
            nbformat.write(notebook, path)

    print(
        f"Combined {totals['combined']} prompt/answer pairs and normalised "
        f"{totals['normalised']} existing discussion reveals."
    )


if __name__ == "__main__":
    main()
