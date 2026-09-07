import json
from pathlib import Path


PATH = Path("notebooks/week08/L_Critical_phenomena.ipynb")


def source(cell):
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else value


def set_source(cell, value):
    cell["source"] = value


def answer(label, body):
    return (
        '<details class="reader-answer">\n'
        f'<summary>{label}</summary>\n'
        '<div>\n\n'
        f'{body.strip()}\n\n'
        '</div>\n'
        '</details>'
    )


nb = json.loads(PATH.read_text())
cells = nb["cells"]

for cell in cells:
    text = source(cell)

    if text.startswith("```{dropdown} Show the calculation"):
        body = text.split("\n", 1)[1].rsplit("```", 1)[0]
        set_source(cell, answer("Show the calculation", body))

    elif text.startswith("```{dropdown} My answer") and "occupation probability" in text:
        body = text.split("\n", 1)[1].rsplit("```", 1)[0]
        set_source(cell, answer("Why the thresholds play different roles", body))

    elif "```{dropdown} Show the dimension bound" in text:
        prompt, rest = text.split("```{dropdown} Show the dimension bound", 1)
        body = rest.rsplit("```", 1)[0]
        set_source(cell, prompt.rstrip() + "\n\n" + answer("Show the dimension bound", body))

    elif text.startswith("```{dropdown} Show the reasoning"):
        body = text.split("\n", 1)[1].rsplit("```", 1)[0]
        set_source(cell, answer("Show the reasoning", body))

    elif text.startswith("```{dropdown} Two levels of explanation"):
        body = text.split("\n", 1)[1].rsplit("```", 1)[0]
        set_source(cell, answer("Immediate trigger and system-level cause", body))

    elif text.startswith("**Q:** It looks fractal"):
        set_source(
            cell,
            "The avalanche footprint looks fractal. Visual resemblance is not enough: "
            "we need to test how the occupied count changes with scale.",
        )

    elif text.startswith("**Q:** What 'events' should we measure"):
        set_source(
            cell,
            '<div class="choice-marker"><img src="images/choice_marker.svg" '
            'alt="Modelling choice"><span>What should count as one event, and which event '
            'properties should be recorded?</span></div>',
        )

    elif text.startswith("**A:** For each perturbation"):
        set_source(
            cell,
            "For each added grain, record the avalanche **duration** $T$ and **size** $S$, "
            "then compare their distributions across many additions. A candidate scaling law is\n\n"
            "$$\nD(S)=aS^{-\\alpha}\n$$",
        )

    elif "sandpile_avalanche_distributions.png" in text:
        set_source(
            cell,
            '<div class="two-panel equal-panels compact-panels">\n'
            '<div class="image-panel"><img src="images/sandpile_avalanche_distributions.png" '
            'alt="Course-generated avalanche-size distribution on linear and log-log axes" '
            'style="max-height:410px"></div>\n'
            '<div class="text-panel"><p>Linear axes emphasise the many small events. '
            'Log–log axes make the broad tail and finite-size cutoff easier to inspect.</p>'
            '<p>Course-generated from the Abelian sandpile simulation used in this Reader.</p></div>\n'
            '</div>',
        )

    elif "sandpile_activity_spectrum.png" in text:
        set_source(
            cell,
            '<div class="two-panel equal-panels compact-panels">\n'
            '<div class="image-panel"><img src="images/sandpile_activity_spectrum.png" '
            'alt="Course-generated power spectrum of sandpile avalanche activity" '
            'style="max-height:410px"></div>\n'
            '<div class="text-panel"><p>The spectrum compresses temporal fluctuations into '
            'power at different frequencies. A fitted slope is meaningful only over a stated '
            'range and remains sensitive to system size and sampling.</p>'
            '<p>Course-generated from the Abelian sandpile simulation used in this Reader.</p></div>\n'
            '</div>',
        )

    elif "sandpile_height_subsets.png" in text:
        set_source(
            cell,
            '<div class="two-panel equal-panels compact-panels">\n'
            '<div class="image-panel"><img src="images/sandpile_height_subsets.png" '
            'alt="Course-generated subsets of a sandpile configuration by site height" '
            'style="max-height:410px"></div>\n'
            '<div class="text-panel"><p>Separating sites by height reveals distinct spatial '
            'subsets within one stable pile.</p><p>Course-generated from the Abelian sandpile '
            'simulation used in this Reader.</p></div>\n</div>',
        )

    elif text.startswith("**Box-counting dimension**:"):
        set_source(
            cell,
            "To estimate the **box-counting dimension**, cover the avalanche footprint "
            "with boxes at several scales and count the occupied boxes. A stable, nearly "
            "linear region on log–log axes provides the range used for the estimate.\n\n"
            '<img src="images/sandpile_box_counting.png" width="60%" '
            'alt="Course-generated box-counting diagnostic for a simulated sandpile avalanche footprint">\n\n'
            "Course-generated diagnostic from the Abelian sandpile simulation used in this Reader. "
            "The estimate depends on the finite lattice, the selected avalanche and the fitted scale range.",
        )

    elif "Something else to consider" in text and "what caused the avalanche" in text:
        set_source(
            cell,
            '<div class="discussion-marker"><img src="images/discussion_marker.svg" '
            'alt="Discussion prompt"><span>What caused the avalanche: the final added grain, '
            'or the state of the pile before it was added?</span></div>',
        )

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
