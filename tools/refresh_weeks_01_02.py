#!/usr/bin/env python3
"""Apply the Week 1–2 teaching template without disturbing existing cells."""

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def md(source, tags=None, slide_type=None, marker=None):
    metadata = {}
    if tags:
        metadata["tags"] = tags
    if slide_type:
        metadata["slideshow"] = {"slide_type": slide_type}
    cell = {"cell_type": "markdown", "metadata": metadata, "source": source.splitlines(keepends=True)}
    if marker:
        cell["id"] = marker
    return cell


def load(path):
    return json.loads(path.read_text())


def save(path, notebook):
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


def add_image_alt_text(notebook):
    """Give legacy images useful filename-derived alt text for accessible exports."""
    def label(src):
        return Path(src).stem.replace("_", " ").replace("-", " ").strip()
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        text = "".join(cell.get("source", []))
        text = re.sub(r"!\[\]\(([^)]+)\)", lambda m: f"![{label(m.group(1))}]({m.group(1)})", text)
        text = re.sub(
            r'<img\s+(?![^>]*\balt=)([^>]*?)src="([^"]+)"([^>]*)>',
            lambda m: f'<img {m.group(1)}src="{m.group(2)}" alt="{label(m.group(2))}"{m.group(3)}>',
            text,
        )
        cell["source"] = text.splitlines(keepends=True)


def insert_once(cells, after, marker, cell):
    if any(c.get("id") == marker for c in cells):
        return
    cells.insert(after + 1, cell)


def insert_after_id(cells, after_id, marker, cell):
    if any(c.get("id") == marker for c in cells):
        return
    after = next(i for i, c in enumerate(cells) if c.get("id") == after_id)
    cells.insert(after + 1, cell)


def refresh_week01_lecture():
    path = ROOT / "notebooks/week01/L_Introduction_to_complex_systems.ipynb"
    nb = load(path)
    cells = nb["cells"]
    cells[0]["source"] = ["# Welcome to MATH3024\n", "## (Modelling) complex systems\n", "*Week 1 · From observations to useful models*"]
    insert_after_id(cells, cells[0].get("id"), "week01-country-slide", md("""## We begin on Whadjuk Noongar Boodjar

<div class="slide-columns country-slide-grid">
  <div><img src="images/Bilya_Kaatajin_UWA_Masterplan_p43.png" alt="Bilya Kaatajin cultural map of UWA Crawley campus and Derbarl Yerrigan" class="country-map"></div>
  <div>
    <div class="country-acknowledgement">We recognise the Whadjuk Noongar people as the Traditional Owners and continuing custodians of this land and its waters. We pay respect to Elders past and present.</div>
    <div class="reader-prompt-footnote"><em>Bilya Kaatajin</em><br>“learning on the river”<br><br>Figure 48, <a href="https://www.uwa.edu.au/about/-/media/project/uwa/uwa/about/docs/campus-management/uwa-2020-crawley-campus-masterplan-web-version.pdf" target="_blank">2020 UWA Crawley Campus Masterplan</a>, p. 43.</div>
  </div>
</div>
""", ["slides"], "slide", "week01-country-slide"))
    insert_after_id(cells, "week01-country-slide", "week01-country-notes", md("""Before we begin, I acknowledge that we are meeting on Whadjuk Noongar Boodjar. I recognise the Whadjuk Noongar people as the Traditional Owners and continuing custodians of this land and its waters. I pay my respects to Elders past and present, and extend that respect to any Aboriginal and Torres Strait Islander people here today.

I have chosen to show this particular map because it locates our learning very precisely. It is *Bilya Kaatajin*, or “learning on the river”, an evolving cultural map of the Crawley campus. The Mathematics building appears within it, not as an isolated academic building, but among language, pathways, vegetation, meeting places, stories and connections leading towards the Derbarl Yerrigan.

This is not only a map of the campus as it is. It is also intended to shape how the campus develops. UWA’s masterplan says that its design principles grew from the Cultural Heritage Mapping project and propose spatial directions influenced by local Whadjuk Noongar knowledge. One priority is to repair the campus’s weak visual and spatial relationship with the river. The east–west connections across the campus are part of that intention. In particular, *Bilya Biddi*, or the River Walk, is proposed from the western edge of campus near EZONE, past Reid Library, and towards the river north of Law. Its route follows the indicative location of an original stream identified through the mapping process.

The proposal is therefore about more than making it easier to walk from one side of campus to the other. It links pathways and meeting places with natural wayfinding, local plants and animals, and the re-establishment of a riverine urban forest. These planning decisions show Indigenous knowledge contributing to the future form of the campus, rather than being added later as decoration or interpretation. The masterplan also describes this as an ongoing relationship. It recommends continuing Whadjuk Noongar input as the living map and the campus evolve.

I am still learning what all of the words and markings on this map mean, and I do not want to pretend to speak with knowledge or authority that I do not have. What I can recognise is that this map makes visible relationships that a conventional campus map does not. It reminds us that every representation of a place or a system emphasises some things and leaves others unseen.

That has particular meaning as we begin Complex Systems. Throughout this unit, we will ask what is lost when we isolate parts of a system from their relationships, histories and environments. We will learn that the behaviour of a whole cannot always be understood by examining its components separately, and that the way we choose to represent a system shapes what we are able to see.

I do not want to appropriate Indigenous knowledge by treating it as an example of our mathematics, or suggest that these knowledge traditions are equivalent. I do want us to begin with humility. The forms of knowledge taught within a university are not the only traditions of careful observation, learning and thought about interconnected worlds.

We therefore begin by recognising the Country on which our learning takes place, the continuing knowledge and custodianship of Whadjuk Noongar people, and our own responsibility to learn here with attention and respect.

The map is described by UWA as a living document that places Whadjuk Noongar tradition, knowledge and culture at the centre of campus planning. It maps the campus as a network of pathways, meeting places, stories, native flora and fauna, with a renewed connection to the river.
""", ["presenter-notes", "remove-cell"], "notes", "week01-country-notes"))
    insert_after_id(cells, "week01-country-notes", "week01-country-reader", md("""## Learning on Whadjuk Noongar Boodjar

We recognise the Whadjuk Noongar people as the Traditional Owners and continuing custodians of the land and waters on which our learning takes place. We pay respect to Elders past and present.

*Bilya Kaatajin* (“learning on the river”) locates the Crawley campus within language, pathways, vegetation, meeting places, stories, and connections to the Derbarl Yerrigan. It reminds us that representations are choices: they make some relationships visible and leave others unseen. We begin the unit with humility, recognising both the continuing knowledge and custodianship of Whadjuk Noongar people and our responsibility to learn here with attention and respect.

*Source: Figure 48, 2020 UWA Crawley Campus Masterplan, p. 43.*
""", ["reader-only"], marker="week01-country-reader"))
    insert_once(cells, 0, "week01-learning-map", md("""<div class="reader-route">
  <div class="reader-route-label">This week</div>
  <div class="reader-route-body"><strong>Notice</strong> a pattern → <strong>choose</strong> a useful abstraction → <strong>simulate</strong> local rules → <strong>interrogate</strong> the result.</div>
</div>

By the end of this week, you should be able to:

- explain why models are judged by purpose rather than by whether they are simply “true”;
- identify agents, states, parameters, rules, and observables in a simple model;
- distinguish qualitative from quantitative model analysis; and
- explain how local preferences can generate an unintended system-level pattern.
""", ["reader-only"], marker="week01-learning-map"))
    insert_once(cells, 3, "week01-opening-pulse", md("""<div class="reader-prompt">
  <div class="reader-prompt-label">Opening pulse · 90 seconds</div>
  <div class="reader-prompt-body"><strong>Where is the model?</strong> Choose a familiar system. Name one detail you would keep, one you would discard, and the question your simplified model could answer.</div>
</div>
""", ["slides"], "subslide", "week01-opening-pulse"))
    insert_after_id(cells, "week01-opening-pulse", "week01-take-stock-slide", md("""# Take stock

## A letter to your Week 12 self

<div class="reader-prompt">
  <div class="reader-prompt-label">Your starting point · 1% participation task</div>
  <div class="reader-prompt-body">What do you currently think complex systems is? What feels comfortable or difficult in mathematics? What do you hope to learn, unlearn, or become more confident doing? Name one way you want to be more deliberate about your remaining time at UWA.</div>
</div>

Write honestly. Seal the letter. We will return it to you in Week 12.
""", ["slides"], "slide", "week01-take-stock-slide"))
    insert_after_id(cells, "week01-take-stock-slide", "week01-take-stock-notes", md("""Before we begin, I want you to take a moment to notice where you are now.

For many of you, this may be one of your final semesters at university. It is very easy to move through a degree from one deadline to the next, focusing on whatever is most urgent and rarely pausing to take stock. You may have spent much of the past few years simply keeping up. That is understandable, but I want to invite you to approach this semester a little more deliberately.

You have already learned a great deal, but you have also developed habits about what mathematics is, what a good problem looks like and what it means to understand something. Over the next twelve weeks, some of those habits will serve you well. Others may need to be stretched, revised or unlearned.

Complex Systems can be a bit of a rollercoaster. We will move across different models, disciplines and ways of thinking. There will be moments when the mathematics feels familiar, and others when the system refuses to behave in the neat way you expect. You will learn new ideas, but you may also have to let go of the expectation that every important question has a single clean method or answer.

So I want you to register your starting point. What do you currently think mathematics is for? How comfortable are you with ambiguity, modelling choices and incomplete information? How confident are you in using code, interpreting unexpected behaviour and defending a judgement rather than reproducing a method?

I also want you to think about what you still want from your time at UWA. Who do you want to learn from? What kinds of questions do you want to become better at asking? What opportunities have you not yet taken? What do you want to be able to say about yourself at the end of this semester that you cannot quite say now?

At the end of the twelve weeks, I will ask you to return to these questions. My hope is not simply that you know more. It is that you can see how your way of thinking has changed, and that this semester feels like something you chose to engage with rather than something you merely completed.

**Delivery:** Allow 8–10 quiet minutes. Provide paper and envelopes. Ask students to put their name and student number on the outside only. Collect and store securely for return in Week 12. Confirm the 1% participation arrangement in the LMS and unit outline before delivery; assess completion, not the private content of the letter.
""", ["presenter-notes", "remove-cell"], "notes", "week01-take-stock-notes"))
    insert_after_id(cells, "week01-take-stock-notes", "week01-take-stock-reader", md("""## Your starting point

Before the semester gathers pace, record where you are now:

- What do you currently think complex systems is?
- What feels comfortable or difficult in mathematics?
- What habits of thought do you expect to rely on?
- What do you hope to learn, unlearn, or become more confident doing over the next twelve weeks?
- What is one way you want to be more deliberate about your remaining time at UWA?

Write this as a private letter to your Week 12 self. Seal it and submit the envelope in class. The task is marked for completion; the contents are not assessed.
""", ["reader-only"], marker="week01-take-stock-reader"))
    end = md("""# One-minute model audit

Before you leave, complete these three sentences:

1. A model is useful when …
2. In Schelling's model, the micro-level rule is …
3. The surprising macro-level outcome is …

<div class="reader-prompt-footnote">Keep this response: it is the conceptual starting point for the workshop.</div>
""", ["slides"], "slide", "week01-exit-ticket")
    if not any(c.get("id") == "week01-exit-ticket" for c in cells):
        cells.append(end)
    editorial_pass_week01(nb)
    add_image_alt_text(nb)
    save(path, nb)


def set_markdown(cells, cell_id, source, tags=None, slide_type=None):
    cell = next(c for c in cells if c.get("id") == cell_id)
    cell["source"] = source.splitlines(keepends=True)
    if tags is not None:
        cell.setdefault("metadata", {})["tags"] = tags
    if slide_type is not None:
        cell.setdefault("metadata", {})["slideshow"] = {"slide_type": slide_type}


def set_code(cells, cell_id, source, tags=None, slide_type=None, clear_output=False):
    cell = next(c for c in cells if c.get("id") == cell_id)
    cell["source"] = source.splitlines(keepends=True)
    if tags is not None:
        cell.setdefault("metadata", {})["tags"] = tags
    if slide_type is not None:
        cell.setdefault("metadata", {})["slideshow"] = {"slide_type": slide_type}
    if clear_output:
        cell["outputs"] = []
        cell["execution_count"] = None


def editorial_pass_week01(nb):
    """Focused narrative and interaction pass requested after slide review."""
    cells = nb["cells"]
    cells[:] = [c for c in cells if c.get("id") not in {
        "week01-opening-pulse",
        "week01-take-stock-slide",
        "week01-take-stock-notes",
        "week01-take-stock-reader",
        "5d1294ac-777c-4cc0-92d4-443b15fb8309",
        "week01-planet-familiar",
        "53dfba25-2263-4c3a-9bd3-6cd3a840ef01",
    }]

    set_markdown(cells, "week01-country-slide", """## We begin on Whadjuk Noongar Boodjar

<img src="images/Bilya_Kaatajin_UWA_Masterplan_p43.png" alt="Bilya Kaatajin cultural map of UWA Crawley campus and Derbarl Yerrigan" class="country-map country-map-large">

<div class="figure-reference"><em>Bilya Kaatajin</em>, “learning on the river”. Figure 48, <a href="https://www.uwa.edu.au/about/-/media/project/uwa/uwa/about/docs/campus-management/uwa-2020-crawley-campus-masterplan-web-version.pdf" target="_blank">2020 UWA Crawley Campus Masterplan</a>, p. 43.</div>
""", ["slides-only", "remove-cell"], "subslide")
    set_markdown(cells, "week01-country-reader", """## Learning on Whadjuk Noongar Boodjar

![Bilya Kaatajin cultural map of UWA Crawley campus and Derbarl Yerrigan](images/Bilya_Kaatajin_UWA_Masterplan_p43.png)

We recognise the Whadjuk Noongar people as the Traditional Owners and continuing custodians of the land and waters on which our learning takes place. We pay respect to Elders past and present.

*Bilya Kaatajin* (“learning on the river”) locates the Crawley campus within language, pathways, vegetation, meeting places, stories, and connections to the Derbarl Yerrigan. It reminds us that representations are choices. They make some relationships visible and leave others unseen. We begin the unit with humility, recognising both the continuing knowledge and custodianship of Whadjuk Noongar people and our responsibility to learn here with attention and respect.

*Source: Figure 48, 2020 UWA Crawley Campus Masterplan, p. 43.*
""", ["reader-only"], "")
    set_markdown(cells, "2ca6c30f-9341-4575-be08-fef1c9de3fb0", """## Why study Complex Systems at UWA?

<div class="slide-columns group-slide-grid">
  <div><img src="images/TCSG_ZahraViva.png" alt="Members of The Complex Systems Group at UWA" class="group-photo"></div>
  <div><img src="images/TCSG_logo_clean.svg" alt="The Complex Systems Group logo" class="group-logo"></div>
</div>

<div class="group-caption">An active research community at UWA. Current research will be woven through this unit.</div>
""", ["slides"], "subslide")

    set_markdown(cells, "f86cefb9-805c-4e22-b3c8-412ba7ee3348", """# Two systems. Two modelling attempts.

All of science relies on models.

1. **Planetary motion**
2. **Segregation**

""", ["slides"], "slide")

    set_markdown(cells, "08b863b0-c2a7-477c-8a73-95a4e4a72001", """## How to use this unit

- Unit essentials can all be found on LMS.
- Slides will be minimal and unpublished.
- Key material from lectures is all in the Reader.
""", ["slides"], "subslide")

    set_markdown(cells, "dc351632-e1e8-4816-a3b3-d3e241eba428", """## Work actively with the Reader

<div class="reader-emphasis"><p>To really learn the material, interact with it. Annotate the Reader or make your own notes by hand.</p></div>

<div class="two-perspectives">
  <div><strong>Longhand notes</strong><p>Students processed ideas more deeply, retained concepts better, and performed better on conceptual questions.</p></div>
  <div><strong>Typed notes</strong><p>Students recorded more words, but were more likely to transcribe verbatim and showed shallower conceptual processing.</p></div>
</div>

<div class="figure-reference">Mueller, P. A. and Oppenheimer, D. M. (2014), <a href="https://doi.org/10.1177/0956797614524581" target="_blank">“The Pen Is Mightier Than the Keyboard: Advantages of Longhand Over Laptop Note Taking”</a>, <em>Psychological Science</em>.</div>
""", ["reader-only"], "")

    set_markdown(cells, "e36db449-7e49-4a35-82f0-29c66512be9d", """<h2 class="system-title">1. Planetary motion <span>The familiar mathematical route</span></h2>

**Kepler's observation:** From Tycho Brahe's measurements, Kepler inferred that every planet follows an ellipse, with the Sun at one focus.

**Newton's question:** Can familiar mathematical principles explain Kepler's empirical law?
""", ["slides"], "subslide")
    insert_after_id(cells, "e36db449-7e49-4a35-82f0-29c66512be9d", "week01-planet-assumptions", md(r"""## Simplify first

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Modelling choices</span></div>

Treat the Sun and planet as point masses. Ignore other planets and relativistic effects.

Then combine two familiar laws:

$$
\vec F=-\frac{GMm}{r^2}\hat r,
\qquad
\vec F=m\ddot{\vec r}.
$$

<div class="process-note">→ A physical observation has become assumptions, variables, and a differential equation.</div>
""", ["slides"], "subslide", "week01-planet-assumptions"))
    planet_assumptions = next(c for c in cells if c.get("id") == "week01-planet-assumptions")
    planet_assumptions_source = "".join(planet_assumptions["source"])
    if "choice-marker" not in planet_assumptions_source:
        planet_assumptions_source = planet_assumptions_source.replace(
            "## Simplify first\n",
            "## Simplify first\n\n<div class=\"choice-marker\"><img src=\"images/choice_marker.svg\" alt=\"Modelling choice\"><span>Modelling choices</span></div>\n",
            1,
        )
        planet_assumptions["source"] = planet_assumptions_source.splitlines(keepends=True)
    insert_after_id(cells, "week01-planet-assumptions", "week01-planet-solve", md(r"""## Solve the equation

Using conservation of angular momentum and $u=1/r$ gives

$$
\frac{d^2u}{d\theta^2}+u=\frac{GM}{h^2}.
$$

Its solution is

$$
r(\theta)=\frac{h^2/GM}{1+e\cos\theta}.
$$

For $0<e<1$, this is an ellipse. Observation explained. QED.
""", ["slides"], "subslide", "week01-planet-solve"))
    set_markdown(cells, "week01-planet-solve", r"""## Solve and conclude

<div class="planet-process">
  <div class="process-sequence">
    <div class="process-step"><span>1</span><p><strong>Choose the evolving state.</strong><br>$\vec r(t)$ is the planet's position relative to the Sun. Its magnitude $r(t)$ is the orbital radius.</p></div>
    <div class="process-step"><span>2</span><p><strong>Change variables.</strong><br>Use polar angle $\theta$ instead of time and define $u(\theta)=1/r(\theta)$.</p></div>
    <div class="process-step"><span>3</span><p><strong>Solve.</strong><br>$\displaystyle \frac{d^2u}{d\theta^2}+u=\frac{GM}{h^2}$</p></div>
    <div class="process-step"><span>4</span><p><strong>Return to the physical variable.</strong><br>$\displaystyle r(\theta)=\frac{h^2/GM}{1+e\cos\theta}$</p></div>
    <div class="process-step qed"><span>5</span><p><strong>Conclusion →</strong> For $0&lt;e&lt;1$, the orbit is an ellipse. Kepler's observation is explained. <strong>QED.</strong></p></div>
  </div>
  <aside class="variable-strip"><strong>Notation for completeness</strong><span>$t$ time</span><span>$\theta$ polar angle</span><span>$r$ Sun–planet distance</span><span>$u=1/r$ transformed variable</span><span>$h$ specific angular momentum</span><span>$e$ eccentricity</span></aside>
</div>
""", ["slides"], "subslide")
    insert_after_id(cells, "week01-planet-solve", "week01-planet-familiar", md("""## This is the mathematics you know

- Start with a phenomenon.
- State simplifying assumptions.
- Apply a general law.
- Write an equation.
- Solve it.
- Interpret the solution.

The path is idealised, but it feels orderly and reassuring.
""", ["slides"], "subslide", "week01-planet-familiar"))
    cells[:] = [c for c in cells if c.get("id") != "week01-planet-familiar"]

    set_markdown(cells, "b00298cd-daf7-40d4-bfaa-1c6a7463cc93", """<h2 class="system-title">2. Segregation <span>The familiar recipe breaks down entirely</span></h2>

<div class="slide-columns">
  <div><img src="images/Chicago_map_2016.jpg" alt="Map showing racial residential patterns in Chicago" class="column-image"><div class="figure-reference">Map: A. C. Mellnik, T. Gamio and D. Keating, <a href="https://www.washingtonpost.com/graphics/2018/national/segregation-us-cities/" target="_blank">“America is more diverse than ever, but still segregated”</a>, <em>The Washington Post</em> (2018), using 2016 ACS estimates and the University of Virginia Racial Dot Map.</div></div>
  <div>
    <div class="reader-voice">
      <div class="reader-voice-quote">I can calculate the motion of planets but not the madness of people.</div>
      <div class="reader-voice-attr">— Newton</div>
    </div>
  </div>
</div>
""", ["slides-only", "remove-cell"], "subslide")

    set_markdown(cells, "1a0291c1-6eb5-4256-b48f-46b812e1ed2e", """## Complex Systems: the field

<div class="slide-columns">
  <div>
    <p>Also called <strong>Complexity Science</strong>.</p>
    <p>It studies how interactions generate collective behaviour across nature, society, and technology.</p>
    <p>Think of it as a flexible mathematical and computational toolkit.</p>
  </div>
  <div><img src="images/Complex_systems_organizational_map.jpg" alt="Topics and methods connected within Complex Systems" class="column-image"></div>
</div>
""", ["slides-only", "remove-cell"], "subslide")

    set_markdown(cells, "e5aefc5a-20a2-4e41-a239-4aa7f51ebfc6", """# Complex Systems

<div class="reader-voice">
  <div class="reader-voice-quote">I think the next (21st) century will be the century of complexity.</div>
  <div class="reader-voice-attr">— Stephen Hawking</div>
</div>
""", ["slides"], "slide")

    complexity_copy = """**Complexity** comes from the Latin word *“plexus”*, indicating that components cannot be understood as fully separable.

<img src="images/complexity_components_order_plane_network.png" alt="Monochrome conceptual plane with a heterogeneous hub-and-community network between planetary motion, Brownian motion, a crystal lattice and an ideal gas" width="92%">

Complex systems occupy an awkward middle.
"""
    set_markdown(cells, "5c072fd4-39b9-4d04-ba12-d816b0e22471", complexity_copy, ["reader-only"], "")
    set_markdown(cells, "4605e182-9ee6-48a1-bd6e-34167f0f6688", "## Where complexity sits\n\n" + complexity_copy, ["slides-only", "remove-cell"], "subslide")

    set_markdown(cells, "8571e887-b28f-4574-883d-51c4cb3ed3e8", """## A classic example: a starling murmuration
""", ["slides"], "subslide")
    video = next(c for c in cells if c.get("id") == "f9a995a9-0b0c-433b-b0bf-9d3f92b587f1")
    video.setdefault("metadata", {})["slideshow"] = {"slide_type": "fragment"}

    thinkers = """<h4>Complex Systems thinkers see things differently</h4>

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><img src="images/Complex_systems_thinkers_see_things_differently.png" alt="Complex Systems thinkers group systems by interaction patterns across disciplines"></div>
  <div class="meaning-panel"><ul>
    <li>Traditional disciplines often group systems by what their components are.</li>
    <li>Complex Systems also groups them by how components interact.</li>
    <li>Similar organising principles can appear in very different domains.</li>
  </ul></div>
</div>

<div class="reader-prompt-footnote">Adapted from A. F. Siegenfeld and Y. Bar-Yam, “An Introduction to Complex Systems Science and Its Applications” (2020).</div>
"""
    set_markdown(cells, "b6c7c6ba-f622-4baa-987c-99dac869f0a9", thinkers, ["reader-only"], "")
    set_markdown(cells, "7aada832-1583-4c44-9c90-259761a269b9", thinkers, ["slides-only", "remove-cell"], "subslide")

    set_markdown(cells, "6e417ebe-e83f-4c10-a573-b28ada4dee33", """### Rules, laws, and ingredients

<div class="reader-voice">
  <div class="reader-voice-quote">There are laws of physics and there are rules of life — and rules are meant to be broken.</div>
  <div class="reader-voice-attr">— David Krakauer, <em>Foundational Papers in Complexity Science</em>, Vol. 1, p. 6</div>
</div>

""", ["slides"], "subslide")
    set_markdown(cells, "5403f858-2e4e-4dbf-af93-91c0f8f20df6", """### What goes in to a model?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>What ingredients can you identify?</span></div>

<ul class="fragment">
  <li><strong>Time:</strong> What counts as one step?</li>
  <li><strong>Structure:</strong> Where can agents exist and who can interact?</li>
  <li><strong>Data:</strong> What must be specified at the beginning?</li>
  <li><strong>Inputs:</strong> Which choices could we vary?</li>
  <li><strong>Dynamics:</strong> What rule changes the state?</li>
</ul>

<p class="fragment">We will use your answers to build the model specification.</p>
""", ["slides"], "subslide")

    set_markdown(cells, "af524424-7678-4c83-bfbe-fdfa04748c67", """### What comes out of a model?

<div class="analysis-perspectives">
  <div><strong>Qualitative perspective</strong><p>Inspect grids, animations, trajectories, and exceptional cases. Use them to recognise patterns and explain mechanisms.</p></div>
  <div><strong>Quantitative perspective</strong><p>Construct observables, time series, distributions, and ensemble summaries. Use them to compare conditions and test robustness.</p></div>
</div>

Complex Systems needs both. Representations compress different features of the same behaviour, so we move between them rather than treating one as definitive.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>The ladder of abstraction:</strong> we will repeatedly move between local rules and system-level summaries.</span></div>
""", ["slides"], "subslide")

    set_markdown(cells, "f03405ed-22fd-4232-bf3f-ea7ce1d94fb6", """### Model details: the original Parable of the Polygons

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>What are the details of the original Parable?</span></div>

<div class="model-specification">
  <div class="fragment"><strong>World</strong><span>a bounded 20 × 20 square grid</span></div>
  <div class="fragment"><strong>Agents and states</strong><span>blue or yellow polygons, plus location; sites are occupied or empty</span></div>
  <div class="fragment"><strong>Initialisation</strong><span>a random arrangement; exact proportions are not documented</span></div>
  <div class="fragment"><strong>Neighbourhood</strong><span>occupied sites in the local Moore neighbourhood</span></div>
  <div class="fragment"><strong>Dynamics</strong><span>move to a random empty site when fewer than one third of neighbours are similar</span></div>
  <div class="fragment"><strong>Observable</strong><span>segregation over time; the original interactive does not define it precisely</span></div>
</div>

<div class="choice-marker fragment"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Every line above is a choice</span></div>
""", ["slides"], "subslide")

    set_markdown(cells, "c717f021-8b82-42e3-8972-f18050210d0f", r"""<h2 class="system-title">The Parable I <span>Start small</span></h2>

Before exploring a large system, we build a $5\times5$ version that we can inspect by eye.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down the ladder:</strong> replace the full system with a small region we can inspect directly.</span></div>
""", ["slides"], "subslide")
    set_markdown(cells, "46bfaf9a-aedf-4ebe-8662-afb6af3936e6", r"""### Initialisation

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>What must be specified before anything can happen?</span></div>

<div class="slide-columns initialisation-layout">
  <div class="qa-grid">
    <div class="qa-row"><p class="qa-question">What is the world?</p><p class="qa-answer fragment">A fixed 5 × 5 square grid.</p></div>
    <div class="qa-row"><p class="qa-question">What states can a site have?</p><p class="qa-answer fragment">Empty, or occupied by a yellow or blue agent.</p></div>
    <div class="qa-row"><p class="qa-question">How is the first configuration generated?</p><p class="qa-answer fragment">Independently at each site, with probabilities $[0.15, 0.425, 0.425]$ for empty, yellow and blue.</p></div>
  </div>
  <div><img src="images/schelling_initialisation.png" alt="Reproducible five by five Schelling initial grid" class="column-image"></div>
</div>
""", ["slides"], "subslide")
    set_code(cells, "ccde3006-cc53-45a6-ae76-de44d03b763e", "plot_schelling_grid(init_grid)\n", ["hide-input", "reader-only"], "", clear_output=True)
    set_markdown(cells, "87b3c690-aa70-4a4e-89e1-3cd0f4d9e045", r"""### Dynamics

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>How should one local step work?</span></div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Choose a local judgement and update rule</span></div>

<div class="qa-grid">
  <div class="qa-row"><p class="qa-question">Who counts as a neighbour?</p><p class="qa-answer fragment">The Moore neighbourhood, excluding the focal agent.</p></div>
  <div class="qa-row"><p class="qa-question">How does an agent judge its environment?</p><p class="qa-answer fragment">Its local similarity is $r_i=n_{s,i}/n_i$. Define unhappiness by $h_i=1$ when $r_i&lt;\theta_r$, and $h_i=0$ otherwise. Initially $\theta_r=50\%$.</p></div>
  <div class="qa-row"><p class="qa-question">What happens when it is dissatisfied?</p><p class="qa-answer fragment">Select one dissatisfied agent at random and move it to a random empty site.</p></div>
</div>
""", ["slides"], "subslide")
    set_code(cells, "1951e092-2531-494d-ab6c-f90ac87a288a", """plot_grid_with_dissatisfied(
    grid=init_grid,
    threshold_percentage=50,
    find_dissatisfied_indices=find_dissatisfied_indices
)
""", ["hide-input", "reader-only"], "", clear_output=True)

    set_code(cells, "9a41008b-1035-43a5-ab0b-1fb188cf0b11", """# The fixed-speed GIF has been retired.
# Use interactive_schelling.html so time can be paused, slowed, and scrubbed.
""", ["hide-input", "hide-output"], "", clear_output=True)

    set_markdown(cells, "562ed9ae-fec2-4387-86b9-6ff3ddefae84", """<iframe src="interactive_schelling.html" title="Interactive Schelling simulation with time and speed controls" class="schelling-interactive"></iframe>
""", ["reader-only"], "")

    set_markdown(cells, "5d9f7001-82f0-4251-b6c8-5996386fd882", """The simulation above replaces the old fixed-speed GIF. Pause it, slow it down, or scrub backwards to inspect individual transitions.

A GIF fixes the pace and hides individual transitions. We want direct control of **time**:

- press play or pause;
- drag the time slider to inspect any state;
- increase the delay to slow the simulation down and watch one move at a time.
""", ["reader-only"], "")

    set_code(cells, "7f2ac2f3-42fe-4725-ae85-d2bdcab5a6b0", '''# INTERACTIVE CONTROL OF TIME

init_rng = default_rng(seed)
init_grid = init_rng.choice([0, 1, 2], (grid_size, grid_size), p=state_probs)
sim_rng = default_rng(seed)
final_grid, frames, moves = run_one_simulation(
    init_grid,
    find_dissatisfied_indices=find_dissatisfied_indices,
    threshold_percentage=threshold_percentage,
    collect_data=False,
    collect_frames=True,
    sim_rng=sim_rng,
    max_iterations=200,
)

max_frame = len(frames) - 1
cmap = ListedColormap(["white", "#EDCC55", "#5879AA"])
out = widgets.Output()

def show_frame(frame_index):
    with out:
        clear_output(wait=True)
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(frames[frame_index], cmap=cmap, vmin=0, vmax=2)
        ax.set_xticks([])
        ax.set_yticks([])
        dissatisfied = find_dissatisfied_indices(frames[frame_index], threshold_percentage)
        if dissatisfied:
            rows, cols = zip(*dissatisfied)
            ax.scatter(cols, rows, marker="x", s=90, c="#1B2A4C", linewidths=2)
        ax.set_xticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax.grid(which="minor", color="#C7CEDC", linewidth=0.7)
        ax.tick_params(which="minor", bottom=False, left=False)
        plt.tight_layout()
        plt.show()
        print(f"Step {frame_index} of {max_frame} · {len(dissatisfied)} dissatisfied agents")

time_slider = widgets.IntSlider(
    value=0, min=0, max=max_frame, step=1,
    description="Time", continuous_update=True,
    layout=widgets.Layout(width="520px"),
)
play_pause = widgets.Play(
    interval=500, value=0, min=0, max=max_frame, step=1,
    description="Play",
)
delay_slider = widgets.FloatSlider(
    value=0.5, min=0.1, max=2.0, step=0.1,
    description="Delay (s)", readout_format=".1f",
    continuous_update=True, layout=widgets.Layout(width="360px"),
)

widgets.jslink((play_pause, "value"), (time_slider, "value"))
time_slider.observe(lambda change: show_frame(change["new"]), names="value")

def update_playback_delay(change):
    play_pause.interval = int(1000 * change["new"])

delay_slider.observe(update_playback_delay, names="value")

show_frame(0)
controls = widgets.VBox([
    widgets.HBox([play_pause, time_slider]),
    delay_slider,
])
display(out, controls)
''')
    insert_after_id(cells, "562ed9ae-fec2-4387-86b9-6ff3ddefae84", "week01-dynamics-panel", md("""### Qualitative analysis

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><iframe src="interactive_schelling.html?autoplay=1&amp;minimal=1&amp;speed=350" title="Schelling simulation evolving through time" class="simulation-preview"></iframe></div>
  <div class="meaning-panel">
    <div class="reader-prompt-label">One relocation step</div>
    <ol>
      <li>Find the dissatisfied agents.</li>
      <li>Select one at random.</li>
      <li>Move it to a random empty site.</li>
      <li>Recalculate every affected neighbourhood.</li>
    </ol>
    <p>Location is part of state. Movement changes the interaction network.</p>
  </div>
</div>
""", ["slides"], "subslide", "week01-dynamics-panel"))

    cells[:] = [c for c in cells if c.get("id") != "week01-interactive-time"]
    insert_after_id(cells, "week01-dynamics-panel", "week01-interactive-time", md("""### Pause the process

<iframe src="interactive_schelling.html?compact=1" title="Interactive Schelling simulation with time and speed controls" class="schelling-interactive compact-simulation"></iframe>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Stay low:</strong> slow the model down and explain exactly what changes in one step.</span></div>
""", ["slides"], "subslide", "week01-interactive-time"))

    set_markdown(cells, "752e1cdd-2806-4794-ac28-bfb085d3e53c", """### Qualitative analysis

The simulation has run. Now compare what we started with and what emerged.
""", ["reader-only"], "")
    set_code(cells, "670570eb-677c-4f5c-a499-4404a74b5152", "# Static teaching panel generated by tools/build_week01_figures.py\n", ["hide-input", "reader-only"], "", clear_output=True)
    insert_after_id(cells, "670570eb-677c-4f5c-a499-4404a74b5152", "week01-qualitative-panel", md("""### Stage 3: compare before and after

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><img src="images/schelling_initial_final.png" alt="Initial and final Schelling grids with dissatisfaction and MSR summaries"></div>
  <div class="meaning-panel">
    <div class="reader-prompt-label">What can we claim?</div>
    <ul>
      <li>The final grid looks more clustered.</li>
      <li>No agents remain dissatisfied.</li>
      <li>The mean local similarity increased.</li>
    </ul>
    <p><strong>It looks segregated, but “looks” is not yet a definition.</strong></p>
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up one rung:</strong> move from individual relocations to a system-level pattern.</span></div>
  </div>
</div>
""", ["slides"], "subslide", "week01-qualitative-panel"))

    set_code(cells, "f97c0b78-8124-4a06-963f-726fe6ffaf73", "# Example grids are generated by tools/build_week01_figures.py\n", ["hide-input", "reader-only"], "", clear_output=True)
    insert_after_id(cells, "f97c0b78-8124-4a06-963f-726fe6ffaf73", "week01-rank-grids", md("""### Which society is more segregated?

<img src="images/schelling_five_grids_prompt.png" alt="Five blue and yellow arrangements labelled A to E" width="100%">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Which arrangement looks most segregated, and why?</span></div>

- Propose an ordering from least to most segregated. What criterion are you using?
- What would the most well-mixed society look like?
- What would the most segregated society look like?
- What numerical value should each endpoint receive?
""", ["slides"], "subslide", "week01-rank-grids"))

    set_markdown(cells, "ab5f3973-4e59-403a-b3dd-842d30b1e292", """The raw mean similarity ratio has mathematical bounds from 0 to 1, but those bounds are not the same as the most typical endpoints for this model.

- In a large, randomly mixed 50:50 population, expected MSR is approximately 0.5.
- In large separated domains, MSR approaches 1 because the boundary becomes small relative to the domains.
- A finite two-block grid need not equal 1. Agents along its interface still have unlike neighbours.
- Empty sites can separate the groups completely, allowing every occupied agent to have similarity ratio 1.

This is why the two-block example below has MSR 0.872, while a simulation can legitimately rise above it.
""", ["reader-only"], "")
    set_code(cells, "6cc63f19-b6ab-46fe-8e76-46a6b871b424", '''def get_local_similarity(grid):
    """Return a grid containing each occupied agent's local similarity ratio."""
    rows, cols = grid.shape
    ratios = np.full(grid.shape, np.nan, dtype=float)
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 0:
                continue
            neighbourhood = grid[max(0, i-1):min(rows, i+2),
                                 max(0, j-1):min(cols, j+2)]
            occupied_neighbours = np.count_nonzero(neighbourhood) - 1
            similar_neighbours = np.count_nonzero(neighbourhood == grid[i, j]) - 1
            ratios[i, j] = (
                similar_neighbours / occupied_neighbours
                if occupied_neighbours else 0.0
            )
    return ratios


def get_unhappiness(grid, threshold):
    """Return 1 for a dissatisfied agent, 0 for a satisfied agent, and NaN if empty."""
    ratios = get_local_similarity(grid)
    return np.where(np.isnan(ratios), np.nan, (ratios < threshold).astype(float))


def get_mean_similarity(grid):
    """Average the local similarity ratios over occupied agents."""
    ratios = get_local_similarity(grid)
    return float(np.nanmean(ratios)) if np.any(~np.isnan(ratios)) else 0.0
''', ["hide-input", "hide-output"])
    set_code(cells, "acecd6e4-f406-4ada-b2e1-1a82983dade7", "# Correct values are generated by tools/build_week01_figures.py\n", ["hide-input", "reader-only"], "", clear_output=True)
    insert_after_id(cells, "acecd6e4-f406-4ada-b2e1-1a82983dade7", "week01-rank-grids-reveal", md("""### One measure, one ordering

<img src="images/schelling_five_grids_values.png" alt="Five arrangements with corrected mean similarity ratios" width="100%">

Using raw MSR gives B &lt; E &lt; A &lt; C &lt; D.

MSR ranges from 0, when every occupied neighbour is unlike, to 1, when every occupied neighbour is alike.

For a large random 50:50 mixture, MSR is usually near 0.5. Zero is a mathematical bound, not the usual well-mixed value.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up the ladder:</strong> compress an entire grid into one number.</span></div>
""", ["slides"], "subslide", "week01-rank-grids-reveal"))

    set_code(cells, "b3d1ae4f-07a6-4d8c-b817-b391784b9d97", "# Static teaching panel generated by tools/build_week01_figures.py\n", ["hide-input", "reader-only"], "", clear_output=True)
    insert_after_id(cells, "b3d1ae4f-07a6-4d8c-b817-b391784b9d97", "week01-time-series-panel", md("""### Stage 4: track system-level quantities

<img src="images/schelling_time_series.png" alt="Dissatisfied agent count and mean similarity ratio over simulation time" width="72%">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Abstract over agents, retain time:</strong> at each time step, compress the grid into two system-level observables. The time series does not average over time.</span></div>
""", ["slides"], "subslide", "week01-time-series-panel"))
    insert_after_id(cells, "week01-time-series-panel", "week01-single-run-msr", md("""### A different seed, an unsettled trajectory

<img src="images/schelling_frustrated_time_series.png" alt="Oscillatory mean similarity ratio with dissatisfied agents remaining" width="78%">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down the ladder:</strong> return to the agents and inspect what prevents the trajectory from settling.</span></div>
""", ["slides"], "subslide", "week01-single-run-msr"))
    set_markdown(cells, "31ef076a-40f2-4535-8411-48bd478b7db1", """### Read two different observables together

- **Dissatisfied count** falls to zero because the relocation rule explicitly targets dissatisfied agents. It tells us when this simulation stops.
- **MSR** rises because those moves tend to increase local similarity. It is one possible measure of the pattern we call segregation.
- We could choose other observables and learn something different from the same run.
- The dashed 0.5 line is a random-mixing benchmark, not a hard minimum.
- The 1.0 line is the raw upper bound, not the value of every visibly divided grid.

One trajectory describes one initial condition and one random sequence of moves. It is evidence, not yet a general result.
""", ["slides"], "subslide")
    set_code(cells, "a404984f-72ed-400b-b22a-7032d66f36fc", "# A second seed remains available for live comparison in the Reader.\n", ["hide-input", "reader-only"], "", clear_output=True)
    set_markdown(cells, "24d40c94-9e93-4839-9c55-a1163db0f562", """### One run is not enough

Was this trajectory typical, or did the initial state and random moves make it unusual?

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span>Inspect another trajectory. <strong>Then up:</strong> compare an ensemble of runs.</span></div>
""", ["slides"], "subslide")
    insert_after_id(cells, "24d40c94-9e93-4839-9c55-a1163db0f562", "week01-frustrated-run", md("""### Inspect the unsettled run

<iframe src="interactive_schelling.html?seed=2&amp;autoplay=1&amp;speed=180" title="Interactive unsettled Schelling simulation" class="schelling-interactive"></iframe>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Stay low:</strong> pause, scrub backwards, and identify which local moves recreate dissatisfaction.</span></div>
""", ["slides"], "subslide", "week01-frustrated-run"))

    # Explicitly refresh inserted cells, whose stable ids otherwise preserve older wording.
    cells[:] = [c for c in cells if c.get("id") != "week01-initialisation-panel"]
    set_markdown(cells, "week01-dynamics-panel", """### Qualitative analysis

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><iframe src="interactive_schelling.html?autoplay=1&amp;minimal=1&amp;speed=350" title="Schelling simulation evolving through time" class="simulation-preview"></iframe></div>
  <div class="meaning-panel">
    <div class="reader-prompt-label">One relocation step</div>
    <ol><li>Find the dissatisfied agents.</li><li>Select one at random.</li><li>Move it to a random empty site.</li><li>Recalculate every affected neighbourhood.</li></ol>
    <p>Location is part of state. Movement changes the interaction network.</p>
  </div>
</div>
""", ["slides"], "subslide")
    set_markdown(cells, "week01-time-series-panel", """### Stage 4: track system-level quantities

<img src="images/schelling_time_series.png" alt="Dissatisfied agent count and mean similarity ratio over simulation time" width="72%">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Abstract over agents, retain time:</strong> at each time step, compress the grid into two system-level observables. The time series does not average over time.</span></div>
""", ["slides"], "subslide")
    set_markdown(cells, "week01-single-run-msr", """### A different seed, an unsettled trajectory

<img src="images/schelling_frustrated_time_series.png" alt="Oscillatory mean similarity ratio with dissatisfied agents remaining" width="78%">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down the ladder:</strong> return to the agents and inspect what prevents the trajectory from settling.</span></div>
""", ["slides"], "subslide")
    set_markdown(cells, "week01-frustrated-run", """### Inspect the unsettled run

<iframe src="interactive_schelling.html?seed=2&amp;autoplay=1&amp;speed=180" title="Interactive unsettled Schelling simulation" class="schelling-interactive"></iframe>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Stay low:</strong> pause, scrub backwards, and identify which local moves recreate dissatisfaction.</span></div>
""", ["slides"], "subslide")

    # Put the concrete animation immediately after the oscillatory trajectory it explains.
    frustrated_cell = next(c for c in cells if c.get("id") == "week01-frustrated-run")
    cells.remove(frustrated_cell)
    unsettled_index = next(i for i, c in enumerate(cells) if c.get("id") == "week01-single-run-msr")
    cells.insert(unsettled_index + 1, frustrated_cell)

    rank_cell = next(c for c in cells if c.get("id") == "week01-rank-grids")
    rank_cell["source"] = """### Which society is more segregated?

<img src="images/schelling_five_grids_prompt.png" alt="Five blue and yellow arrangements labelled A to E" width="100%">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Which arrangement looks most segregated, and why?</span></div>

- Propose an ordering from least to most segregated. What criterion are you using?
- What would the most well-mixed society look like?
- What would the most segregated society look like?
- What numerical value should each endpoint receive?
""".splitlines(keepends=True)
    reveal_cell = next(c for c in cells if c.get("id") == "week01-rank-grids-reveal")
    reveal_cell["source"] = """### One measure, one ordering

<img src="images/schelling_five_grids_values.png" alt="Five arrangements with corrected mean similarity ratios" width="100%">

Using raw MSR gives B &lt; E &lt; A &lt; C &lt; D.

MSR ranges from 0, when every occupied neighbour is unlike, to 1, when every occupied neighbour is alike.

For a large random 50:50 mixture, MSR is usually near 0.5. Zero is a mathematical bound, not the usual well-mixed value.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up the ladder:</strong> compress an entire grid into one number.</span></div>
""".splitlines(keepends=True)

    set_markdown(cells, "f4e7fa1c-9c10-4881-b6cd-8196c7082c13", """# Our turn: build the model

1. **Initialise:** create a reproducible state.
2. **Evolve:** apply one local update rule repeatedly.
3. **Compare:** inspect what changed between before and after.
4. **Measure:** replace visual impressions with explicit observables.

""", ["slides"], "slide")

    # Keep the rules/laws quote at the point where dynamics must be chosen.
    krakauer_cell = next(c for c in cells if c.get("id") == "6e417ebe-e83f-4c10-a573-b28ada4dee33")
    cells.remove(krakauer_cell)
    initialisation_index = next(i for i, c in enumerate(cells) if c.get("id") == "46bfaf9a-aedf-4ebe-8662-afb6af3936e6")
    cells.insert(initialisation_index + 1, krakauer_cell)

    qualitative_panel = next(c for c in cells if c.get("id") == "week01-qualitative-panel")
    qualitative_source = "".join(qualitative_panel["source"])
    qualitative_source = qualitative_source.replace(
        "### Stage 3: compare before and after",
        "# Analyse one run",
        1,
    )
    qualitative_source = qualitative_source.replace("## Compare before and after\n", "")
    qualitative_panel["source"] = qualitative_source.splitlines(keepends=True)
    qualitative_panel.setdefault("metadata", {})["slideshow"] = {"slide_type": "slide"}

    set_markdown(cells, "0b11763d-2cdf-41e8-ba71-1530cd1e843d", """# Generalise across parameters and ensembles

One trajectory is one initial condition and one random sequence of moves. We now ask which conclusions survive changes in parameters and initial conditions.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span>One run → an ensemble → a parameter sweep of ensembles.</span></div>
""", ["slides"], "slide")

    set_markdown(cells, "069229ca-29bb-41c0-ac2c-08014f009791", """## Pause and compute

Time for us to have a break, and our machines to go to work.

<div class="reader-emphasis"><p>This is why you must get started on your Projects early!</p></div>
""", ["slides"], "subslide")
    # Rebuild this local-to-global sequence on every refresh so its order is stable.
    cells[:] = [c for c in cells if c.get("id") != "week01-local-similarity"]
    insert_after_id(cells, "3138e854-88cb-4cb5-b168-2cfc42e4fa78", "week01-local-similarity", md(r"""### Give every agent a local value

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><img src="images/schelling_local_similarity.png" alt="The same Schelling grid shown as agent types and as local similarity ratios, with dissatisfied agents crossed"></div>
  <div class="meaning-panel">
    <p>For occupied square $i$, define</p>
    $$r_i=\frac{n_{s,i}}{n_i}.$$
    <p>$n_{s,i}$ counts similar occupied neighbours and $n_i$ counts all occupied neighbours.</p>
    <p>The colour and number belong to one agent. This is a <strong>local similarity ratio</strong>, not yet the MSR.</p>
  </div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Abstract over neighbours:</strong> replace one agent's neighbourhood with the scalar $r_i$.</span></div>
""", ["slides"], "subslide", "week01-local-similarity"))

    set_markdown(cells, "88dc7a87-2adb-417c-adce-33daacb8db0f", r"""### From local judgement to collective behaviour

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>How could we move up the ladder from individual happiness to describe the collective?</span></div>

<div class="aggregate-definitions">
  <div><strong>Dissatisfaction</strong><p>Sum the already-defined local indicators: $\displaystyle D=\sum_{i=1}^{N}h_i$. The model stops when $D=0$.</p></div>
  <div><strong>Local similarity</strong><p>Average the local ratios: $\displaystyle \mathcal{MSR}=\frac{1}{N}\sum_{i=1}^{N}r_i$. This is one possible measure of segregation.</p></div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>The dissatisfied count follows the update rule; MSR is an additional observable chosen to describe the spatial pattern.</span></div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Abstract over agents:</strong> combine $N$ local values into one system-level number at a fixed time.</span></div>
""", ["slides"], "subslide")

    aggregate_cell = next(c for c in cells if c.get("id") == "88dc7a87-2adb-417c-adce-33daacb8db0f")
    cells.remove(aggregate_cell)
    local_index = next(i for i, c in enumerate(cells) if c.get("id") == "week01-local-similarity")
    cells.insert(local_index + 1, aggregate_cell)

    set_markdown(cells, "week01-exit-ticket", """# Take it with you
## A short transfer exercise

<div class="transfer-slide"></div>

Choose a familiar system and complete these prompts:

1. What question would your model answer?
2. What would you keep, and what would you deliberately leave out?
3. What are the agents or components, states, inputs, rules, and observables?
4. What micro-level rule might create a surprising macro-level pattern?
5. What would make the model useful, even though it is incomplete?

Bring it to the workshop.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span>Read Bret Victor's <a href="https://worrydream.com/LadderOfAbstraction/" target="_blank">Up and Down the Ladder of Abstraction</a> before the workshop.</span></div>
""", ["slides"], "slide")

    insert_after_id(cells, "0a1e1cb5-92ff-4331-a1c3-77efec7242ac", "week01-paradigm-video", md("""## A new scientific paradigm

The tools, questions, and criteria for a useful model are changing.
""", ["slides"], "subslide", "week01-paradigm-video"))
    paradigm_video = next(c for c in cells if c.get("id") == "952712ac-3d3c-4af3-9080-f172de826c1a")
    paradigm_video.setdefault("metadata", {})["slideshow"] = {"slide_type": "fragment"}

    set_markdown(cells, "19a55b90-0ef6-4afc-807c-9a88d2531b17" if any(c.get("id") == "19a55b90-0ef6-4afc-807c-9a88d2531b17" for c in cells) else "19a55b90-0ef6-4afc-8072-417fe7905334", """### Vary an important parameter

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Interrogate a modelling choice</span></div>

Why is the similarity threshold 50%? It is a modelling choice, and it may control the behaviour.

We now sweep across threshold values and compare the resulting trajectories.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up the ladder:</strong> abstract over a parameter instead of following one run.</span></div>

This is called a **parameter sweep**.
""", ["slides"], "subslide")

    parameter_intro_id = "19a55b90-0ef6-4afc-807c-9a88d2531b17" if any(c.get("id") == "19a55b90-0ef6-4afc-807c-9a88d2531b17" for c in cells) else "19a55b90-0ef6-4afc-8072-417fe7905334"
    insert_after_id(cells, parameter_intro_id, "week01-ensemble-trajectories", md("""### An ensemble for every parameter value

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><img src="images/schelling_ensemble_trajectories.png" alt="Mean MSR trajectories and middle fifty percent bands for an ensemble at each threshold"></div>
  <div class="meaning-panel">
    <ul>
      <li>For each threshold, run five independently initialised simulations.</li>
      <li>The line is the ensemble mean trajectory.</li>
      <li>The band is the middle 50% of runs.</li>
      <li>We now compare aggregate statistics for every parameter in the sweep.</li>
    </ul>
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up:</strong> one run → an ensemble. <strong>Across:</strong> repeat the ensemble for each threshold.</span></div>
  </div>
</div>
""", ["slides"], "subslide", "week01-ensemble-trajectories"))
    insert_after_id(cells, "week01-ensemble-trajectories", "week01-parameter-ensemble", md("""### Aggregate over initial conditions

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><img src="images/schelling_parameter_ensemble.png" alt="Ensemble summaries of final MSR and remaining dissatisfied agents across thresholds"></div>
  <div class="meaning-panel">
    <ul>
      <li>Each point averages five independently initialised runs.</li>
      <li>The band shows the middle 50% of runs, not plotting uncertainty.</li>
      <li>Higher thresholds can raise local similarity while leaving many agents perpetually dissatisfied.</li>
    </ul>
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up:</strong> replace individual runs with a distribution.</span></div>
  </div>
</div>
""", ["slides"], "subslide", "week01-parameter-ensemble"))
    insert_after_id(cells, "week01-parameter-ensemble", "week01-parameter-examples", md("""### Check the mechanism at three thresholds

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><img src="images/schelling_parameter_examples.png" alt="Final Schelling grids at low, medium and high similarity thresholds"></div>
  <div class="meaning-panel">
    <ul>
      <li><strong>20%:</strong> most agents accept the initial mixture, so little changes.</li>
      <li><strong>50%:</strong> movement can resolve dissatisfaction and produce clusters.</li>
      <li><strong>80%:</strong> the demand is often impossible to satisfy on a finite mixed grid.</li>
    </ul>
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down:</strong> use concrete grids to explain the ensemble pattern.</span></div>
  </div>
</div>
""", ["slides"], "subslide", "week01-parameter-examples"))
    insert_after_id(cells, "week01-parameter-examples", "week01-ensemble-definition", md("""### From one run to an ensemble

An **ensemble** is a collection of runs made with the same model and parameter values, but independently generated initial states and random update sequences.

<div class="analysis-perspectives">
  <div><strong>One run</strong><p>Shows one possible history. It helps us inspect mechanisms, but it may be atypical.</p></div>
  <div><strong>An ensemble</strong><p>Shows a distribution of possible histories. It lets us estimate what is typical, how variable outcomes are, and how often the system fails to settle.</p></div>
</div>

We use five runs here to make the construction visible. A substantive analysis would use enough runs for the summaries to stabilise.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up the ladder:</strong> replace a particular random history with a distribution over possible histories.</span></div>
""", ["slides"], "subslide", "week01-ensemble-definition"))

    set_markdown(cells, "week01-parameter-examples", """### Check the mechanism at three thresholds

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><img src="images/schelling_parameter_examples.png" alt="Final five by five Schelling grids at low, medium and high similarity thresholds"></div>
  <div class="meaning-panel">
    <ul>
      <li><strong>20%:</strong> most agents accept the initial mixture, so little changes.</li>
      <li><strong>50%:</strong> movement can resolve dissatisfaction and produce clusters.</li>
      <li><strong>80%:</strong> the demand is often impossible to satisfy on a finite mixed grid.</li>
    </ul>
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down:</strong> use concrete grids to predict what the parameter sweep may show.</span></div>
  </div>
</div>
""", ["slides"], "subslide")
    set_markdown(cells, "week01-ensemble-definition", """### From one run to an ensemble

An **ensemble** repeats the same model and parameters with independent initial states and random update sequences.

<div class="analysis-perspectives ensemble-comparison">
  <div>
    <strong>One run</strong>
    <p>Reveals one possible history and its mechanism.</p>
    <p>At 80%, frustrated agents keep moving because acceptable sites are scarce.</p>
    <p>But this run may be atypical.</p>
  </div>
  <div>
    <strong>An ensemble</strong>
    <p>Tests whether the mechanism recurs across independent runs.</p>
    <p>Shows what is typical, how outcomes vary, and how often the model fails to settle.</p>
    <p>Use enough runs for these summaries to stabilise.</p>
  </div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up the ladder:</strong> replace a particular random history with a distribution over possible histories.</span></div>
""", ["slides"], "subslide")

    cells[:] = [c for c in cells if c.get("id") not in {
        "week01-threshold-80-simulation", "week01-threshold-80-reader"
    }]
    insert_after_id(cells, "week01-parameter-examples", "week01-threshold-80-simulation", md("""### Inspect the frustrated 80% run

<iframe src="interactive_schelling.html?threshold=0.8&amp;seed=1&amp;autoplay=1&amp;speed=450&amp;compact=1" title="Interactive Schelling simulation at an eighty percent similarity threshold" class="schelling-interactive compact-simulation"></iframe>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Back down the ladder:</strong> follow individual agents. Some remain dissatisfied but cannot find an empty site that meets the demanding threshold, so movement continues and MSR need not settle at a plateau.</span></div>
""", ["slides-only", "remove-cell"], "subslide", "week01-threshold-80-simulation"))
    insert_after_id(cells, "week01-threshold-80-simulation", "week01-threshold-80-reader", md("""### Inspect the frustrated 80% run

<iframe src="../interactive_schelling.html?threshold=0.8&amp;seed=1&amp;autoplay=1&amp;speed=450&amp;compact=1" title="Interactive Schelling simulation at an eighty percent similarity threshold" class="schelling-interactive compact-simulation"></iframe>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Back down the ladder:</strong> follow individual agents. Some remain dissatisfied but cannot find an empty site that meets the demanding threshold, so movement continues and MSR need not settle at a plateau.</span></div>

This run reveals a plausible mechanism. It does not yet establish a general pattern. We next use an ensemble to ask whether the same unsettled behaviour appears across independently generated initial states and random update sequences.
""", ["reader-only"], marker="week01-threshold-80-reader"))
    set_markdown(cells, "week01-ensemble-trajectories", """### Repeat the ensemble at every threshold

<div class="slide-columns evidence-layout">
  <div class="evidence-panel">
    <img src="images/schelling_ensemble_trajectories.png" alt="Mean MSR trajectories and middle fifty percent bands for an ensemble at each threshold">
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Back up the ladder as we abstract over time:</strong> replace each trajectory with a small set of outcome statistics.</span></div>
  </div>
  <div class="meaning-panel">
    <ul>
      <li>Five independent runs at each threshold.</li>
      <li>Line: ensemble mean MSR.</li>
      <li>Band: middle 50% of runs, not a confidence interval.</li>
    </ul>
    <p>This is messy and difficult to interpret. Let’s collapse each time series to a summary statistic.</p>
  </div>
</div>
""", ["slides"], "subslide")

    cells[:] = [c for c in cells if c.get("id") != "week01-parameter-trajectories"]
    insert_after_id(cells, parameter_intro_id, "week01-parameter-trajectories", md("""### First, sweep the parameter

<div class="slide-columns evidence-layout">
  <div class="evidence-panel"><img src="images/schelling_parameter_trajectories.png" alt="One mean similarity ratio trajectory for each similarity threshold"></div>
  <div class="meaning-panel">
    <p>Hold the initial seed and update sequence fixed. Change only the similarity threshold.</p>
    <p>Each line is one run, so the figure exposes how the parameter changes the trajectory without yet showing run-to-run variation.</p>
    <p>The comparison is useful, but any one line could be atypical.</p>
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Across the ladder:</strong> retain time while varying one modelling choice.</span></div>
  </div>
</div>
""", ["slides"], "subslide", "week01-parameter-trajectories"))
    set_markdown(cells, "week01-parameter-ensemble", """### Compare outcomes across thresholds

<div class="slide-columns evidence-layout parameter-outcomes-layout">
  <div class="evidence-panel">
    <img src="images/schelling_parameter_ensemble.png" alt="Ensemble mean final MSR and dissatisfied fraction across similarity thresholds">
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Abstract over time and random runs:</strong> replace each trajectory with its outcome after 100 steps, then summarise across runs. The threshold remains on the horizontal axis.</span></div>
  </div>
  <div class="meaning-panel">
    <p><strong>Top:</strong> final local similarity rises through intermediate thresholds, then falls when demanding preferences keep the system moving.</p>
    <p><strong>Bottom:</strong> the fraction still dissatisfied after 100 steps shows when those demands become difficult to satisfy.</p>
    <p>This is not a search for a “best” threshold. A best value exists only after we specify an objective and acceptable trade-offs.</p>
  </div>
</div>
""", ["slides"], "subslide")

    # The Reader needs a continuous prose route. Slide layouts use raw HTML,
    # which does not reliably render mathematics in MyST, so provide dedicated
    # Reader cells with ordinary Markdown and display mathematics.
    set_markdown(cells, "dc351632-e1e8-4816-a3b3-d3e241eba428", """## Working actively and working with evidence

This Reader is designed for active use. Annotate it, pause at the prompts, and make notes in your own words.

This is also our first example of how research evidence will appear throughout the unit. I will frequently link the source behind a factual claim. These links ground our statements in evidence and help you become familiar with the conventions of research writing. You do not need to read every paper immediately, but you should learn to notice what is being claimed, what evidence supports it, and where that evidence came from.

### What one study found

Mueller and Oppenheimer compared different approaches to note-taking:

- **Longhand notes:** students processed ideas more deeply and performed better on conceptual questions.
- **Typed notes:** students recorded more words, but were more likely to transcribe verbatim and showed shallower conceptual processing.

The practical lesson for this unit is to avoid passive transcription. Handwriting is one useful way to force yourself to select, summarise, and connect ideas.

Mueller, P. A. and Oppenheimer, D. M. (2014), [“The Pen Is Mightier Than the Keyboard: Advantages of Longhand Over Laptop Note Taking”](https://doi.org/10.1177/0956797614524581), *Psychological Science*.
""", ["reader-only"], "")

    set_markdown(cells, "0f879eca-474c-497c-8a6f-44d17566325d", """## Why models?

A model lets us reason from assumptions about a system's structure to conclusions about what we expect to observe, what may happen under specified conditions, or what could change after an intervention.

We turn to models when the system itself is difficult to work with directly. It may be too large, too small, too costly to test, too difficult to manipulate, or too complicated to understand all at once.

The skill lies in deciding what to retain, what to omit, and how to revise the model when it no longer serves its purpose. A model should not reproduce the full richness of the world. The world already does that. A useful model gives us a partial description that can answer a particular question.

Modelling therefore requires comfort with approximation, incomplete descriptions, and conclusions with a limited scope. These are not defects. They are what make a model tractable and useful.

[A short introduction to this view of modelling](https://www.youtube.com/watch?v=Pgm65hYglpg)
""", ["reader-only"], "")

    set_markdown(cells, "9832bced-defa-4e8e-856e-b083b23dd61e", """## System 2: Segregation

<div class="reader-voice">
  <div class="reader-voice-quote">I can calculate the motion of planets but not the madness of people.</div>
  <div class="reader-voice-attr">— Newton</div>
</div>

### Schelling's observation

<img src="images/Chicago_map_2016.jpg" alt="Racial dot map of Chicago" class="reader-map">

<div class="figure-reference">A. C. Mellnik, T. Gamio and D. Keating, <a href="https://www.washingtonpost.com/graphics/2018/national/segregation-us-cities/" target="_blank">“America is more diverse than ever, but still segregated”</a>, <em>The Washington Post</em> (2018), using 2016 ACS estimates and the University of Virginia Racial Dot Map.</div>

The spatial pattern is unmistakable, but there is no single familiar law that turns this observation directly into an equation we can solve. The classical route used for planetary motion breaks down. We need another way to connect individual decisions with a collective pattern.
""", ["reader-only"], "")

    set_markdown(cells, "d391db61-327a-4d7f-85f3-20ae45f224a6", """### A second perspective on complexity

```{iframe} https://www.youtube.com/embed/JR93X7xK05o
:width: 100%
```

David Krakauer describes fields by the weight they place on quantitative, compressive, reductionist, and historicist explanations. As you watch, notice which of these traits he associates with Complexity Science and how he distinguishes explanation from prediction.

<div class="reader-prompt">
  <div class="reader-prompt-label">Pause and consider</div>
  <div class="reader-prompt-body">Why do systems in the middle of the complexity plane resist both exact reduction and simple statistical averaging?</div>
</div>
""", ["reader-only"], "")

    set_markdown(cells, "2c7a4ca7-fb5b-4b53-9e87-19b84603f109", """## The ladder of abstraction

Modelling is an interactive process. We move down to inspect individual components and local rules, then move up to recognise patterns and construct system-level summaries.

<div class="reader-prompt">
  <div class="reader-prompt-label">Read</div>
  <div class="reader-prompt-body"><a href="http://worrydream.com/LadderOfAbstraction" target="_blank">Bret Victor's “Up and Down the Ladder of Abstraction”</a></div>
</div>

<img src="images/Ladder_of_abstraction.png" alt="Ladder of abstraction" width="60%">

Neither view is sufficient by itself. A high-level pattern needs a mechanism, while a local mechanism needs a view of its collective consequences. We will repeatedly move between the two.
""", ["reader-only"], "")

    reader_replacements = {
        "week01-planet-solve-reader": ("week01-planet-solve", r"""### Solve and conclude

1. **Choose the evolving state.** The vector $\vec r(t)$ is the planet's position relative to the Sun, and $r(t)$ is its orbital radius.
2. **Change variables.** Use polar angle $\theta$ in place of time and define $u(\theta)=1/r(\theta)$.
3. **Solve.**

   $$
   \frac{d^2u}{d\theta^2}+u=\frac{GM}{h^2}.
   $$

4. **Return to the physical variable.**

   $$
   r(\theta)=\frac{h^2/GM}{1+e\cos\theta}.
   $$

5. **Conclude.** For $0<e<1$, the orbit is an ellipse. Kepler's observation is explained. QED.

Here $t$ is time, $\theta$ is polar angle, $r$ is Sun–planet distance, $u$ is a transformed variable, $h$ is specific angular momentum, and $e$ is eccentricity.
"""),
        "week01-initialisation-reader": ("46bfaf9a-aedf-4ebe-8662-afb6af3936e6", r"""### Initialisation

Before anything changes, we must specify the world and generate its first state.

- **World:** a fixed 5 × 5 square grid.
- **Site states:** empty, occupied by a yellow agent, or occupied by a blue agent.
- **Initial probabilities:** independently assign each site using probabilities $[0.15,0.425,0.425]$ for empty, yellow, and blue.

![A reproducible five by five Schelling initial grid](images/schelling_initialisation.png)
"""),
        "week01-dynamics-reader": ("87b3c690-aa70-4a4e-89e1-3cd0f4d9e045", r"""### Dynamics

One time step applies a local judgement and an update rule.

- **Neighbourhood:** the Moore neighbourhood, excluding the focal agent.
- **Local similarity:** for agent $i$, let

  $$
  r_i=\frac{n_{s,i}}{n_i},
  $$

  where $n_{s,i}$ is the number of similar occupied neighbours and $n_i$ is the number of occupied neighbours.
- **Unhappiness:** define $h_i=1$ when $r_i<\theta_r$, and $h_i=0$ otherwise. We begin with $\theta_r=50\%$.
- **Update:** choose one dissatisfied agent at random and move it to a random empty site.
"""),
        "week01-local-similarity-reader": ("week01-local-similarity", r"""### Give every agent a local value

![Agent states beside each occupied agent's local similarity ratio](images/schelling_local_similarity.png)

For each occupied square $i$, the local similarity ratio is

$$
r_i=\frac{n_{s,i}}{n_i}.
$$

This number compresses one neighbourhood into one local observable. It belongs to an individual agent. It is not yet a measure of the whole society.
"""),
        "week01-collective-reader": ("88dc7a87-2adb-417c-adce-33daacb8db0f", r"""### From local judgement to collective behaviour

We can aggregate the local values in two different ways.

The total number of dissatisfied agents is

$$
D=\sum_{i=1}^{N}h_i.
$$

This quantity belongs to the update rule. The model stops when $D=0$.

The mean similarity ratio is

$$
\mathcal{MSR}=\frac{1}{N}\sum_{i=1}^{N}r_i.
$$

MSR is an additional observable chosen to summarise the spatial pattern. It is one possible measure of segregation, not a quantity forced on us by the model.
"""),
    }
    for marker in reader_replacements:
        cells[:] = [c for c in cells if c.get("id") != marker]
    for marker, (after_id, source) in reader_replacements.items():
        original = next(c for c in cells if c.get("id") == after_id)
        original.setdefault("metadata", {})["tags"] = ["slides-only", "remove-cell"]
        insert_after_id(cells, after_id, marker, md(source, ["reader-only"], marker=marker))

    # Reader iframe paths are relative to the generated page route. Keep the
    # slide versions separate so each output receives a valid path.
    for slide_id in ("week01-dynamics-panel", "week01-interactive-time", "week01-frustrated-run"):
        slide_cell = next(c for c in cells if c.get("id") == slide_id)
        slide_cell.setdefault("metadata", {})["tags"] = ["slides-only", "remove-cell"]
    cells[:] = [c for c in cells if c.get("id") not in {
        "week01-reader-interactive", "week01-reader-unsettled"
    }]
    insert_after_id(cells, "week01-dynamics-reader", "week01-reader-interactive", md("""### Observe the process

<iframe src="../interactive_schelling.html?compact=1" title="Interactive Schelling simulation" class="schelling-interactive compact-simulation"></iframe>

Pause the simulation, slow it down, or scrub backwards. Inspect individual transitions before moving up the ladder to system-level summaries.
""", ["reader-only"], marker="week01-reader-interactive"))
    insert_after_id(cells, "week01-single-run-msr", "week01-reader-unsettled", md("""### Inspect the unsettled run

<iframe src="../interactive_schelling.html?seed=2&amp;autoplay=1&amp;speed=180" title="Interactive unsettled Schelling simulation" class="schelling-interactive"></iframe>

Return to the agents and inspect which local moves recreate dissatisfaction.
""", ["reader-only"], marker="week01-reader-unsettled"))

    # Preserve obsolete exploratory analysis for provenance without publishing
    # stale outputs or duplicate summary plots.
    archive_ids = {
        "873012ad-a84f-4b3d-8c2b-dd332fe04c91", "01730675-1d30-47fb-98f0-2ca1cb1047e3",
        "cc411d6e-4672-4230-be0e-5b6dd717d4af", "cc59ce63-8ff8-478a-9ba0-9939f145fda9",
        "3f3a8622-bfaa-4cce-8b3f-50000ac18f01", "c9b6e2c7-5416-4cf2-8ede-38de1d878552",
        "739e3f8b-7d8e-4de0-9938-f3fac7b45c3a", "fee653a6-6258-4900-86d8-4743c8eb7c31",
        "b3f277c1-40b0-4aef-ba04-3a2e2d38ea57", "8f7e2618-c206-420d-b4ee-e6a84a57d6b1",
        "b40d0b96-c740-418f-8b8c-d07cdb0008ad", "72588c28-633c-4fd1-bc4a-d8ca27b67776",
        "e079670d-fea9-479b-a72c-2e830ef7283b", "dc21a40e-f81f-4332-bb2c-6ba530011a52",
        "ef46b424-e3c0-4ba8-aded-e5ee0a01b1d5", "562ed9ae-fec2-4387-86b9-6ff3ddefae84",
    }
    for cell in cells:
        if cell.get("id") in archive_ids:
            cell.setdefault("metadata", {})["tags"] = ["archive-only", "remove-cell"]

    cells[:] = [c for c in cells if c.get("id") != "week01-time-summaries"]
    insert_after_id(cells, "week01-parameter-ensemble", "week01-time-summaries", md("""### When does the outcome emerge?

<div class="slide-columns evidence-layout">
  <div class="evidence-panel">
    <img src="images/schelling_time_summaries.png" alt="Time of maximum similarity and time until settling across thresholds">
    <div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Abstract over time:</strong> replace a trajectory with an event time, then abstract over random runs.</span></div>
  </div>
  <div class="meaning-panel">
    <p><strong>Top:</strong> the simulation time step at which each run first reaches its maximum MSR.</p>
    <p><strong>Bottom:</strong> the number of steps until no agents are dissatisfied. Runs that remain active are capped at the 100-step budget.</p>
    <p>These summaries answer different questions. Maximum similarity can occur before movement stops.</p>
  </div>
</div>
""", ["slides-only", "remove-cell"], "subslide", "week01-time-summaries"))

    insert_after_id(cells, "week01-time-summaries", "week01-time-summaries-reader", md("""### When does the outcome emerge?

![Time of maximum similarity and time until settling across thresholds](images/schelling_time_summaries.png)

The top panel records when each run first reaches its maximum MSR. The bottom panel records when movement stops because no agents remain dissatisfied. A run that is still active is capped at the 100-step simulation budget.

These are different event times. Maximum similarity can occur before movement stops. Each trajectory is first compressed into an event time, then the event times are summarised across independent runs.
""", ["reader-only"], marker="week01-time-summaries-reader"))

    # Earlier reordering moves the parameter-outcome cell. Keep the two time
    # summary cells immediately after it in both outputs.
    for marker in ("week01-time-summaries", "week01-time-summaries-reader"):
        moving = next(c for c in cells if c.get("id") == marker)
        cells.remove(moving)
        after = "week01-parameter-ensemble" if marker == "week01-time-summaries" else "week01-time-summaries"
        index = next(i for i, c in enumerate(cells) if c.get("id") == after)
        cells.insert(index + 1, moving)

    # Teach the parameter mechanism before introducing ensemble statistics.
    ordered_parameter_cells = [
        next(c for c in cells if c.get("id") == marker)
        for marker in (
            "week01-parameter-trajectories", "week01-parameter-examples",
            "week01-threshold-80-simulation", "week01-threshold-80-reader",
            "week01-ensemble-definition",
            "week01-ensemble-trajectories", "week01-parameter-ensemble",
            "week01-time-summaries", "week01-time-summaries-reader",
        )
    ]
    for ordered_cell in ordered_parameter_cells:
        cells.remove(ordered_cell)
    parameter_index = next(i for i, c in enumerate(cells) if c.get("id") == parameter_intro_id)
    for offset, ordered_cell in enumerate(ordered_parameter_cells, start=1):
        cells.insert(parameter_index + offset, ordered_cell)

    # Retain superseded exploratory cells inside the notebook for provenance,
    # but publish neither their code nor their stale output figures.
    for result_id in {
        "01730675-1d30-47fb-98f0-2ca1cb1047e3", "cc59ce63-8ff8-478a-9ba0-9939f145fda9",
        "3f3a8622-bfaa-4cce-8b3f-50000ac18f01", "c9b6e2c7-5416-4cf2-8ede-38de1d878552",
        "e079670d-fea9-479b-a72c-2e830ef7283b", "dc21a40e-f81f-4332-bb2c-6ba530011a52",
        "ef46b424-e3c0-4ba8-aded-e5ee0a01b1d5",
    }:
        result_cell = next((c for c in cells if c.get("id") == result_id), None)
        if result_cell:
            result_cell.setdefault("metadata", {})["tags"] = ["archive-only", "remove-cell"]
            result_cell.setdefault("metadata", {})["slideshow"] = {"slide_type": ""}

    set_code(cells, "b40d0b96-c740-418f-8b8c-d07cdb0008ad", '''def run_msr_ensemble(thresholds, seeds=range(5), grid_size=5,
                     state_probs=(0.15, 0.425, 0.425), max_iterations=100):
    """Return one list of reproducible MSR trajectories per threshold."""
    results = {}
    for threshold in thresholds:
        results[threshold] = []
        for seed in seeds:
            init_rng = default_rng(seed)
            sim_rng = default_rng(seed + 1000)
            initial = init_rng.choice([0, 1, 2], (grid_size, grid_size), p=state_probs)
            msr_history, _, _ = run_one_simulation(
                initial,
                find_dissatisfied_indices=find_dissatisfied_indices,
                get_mean_similarity=get_mean_similarity,
                threshold_percentage=threshold,
                force_iterate=False,
                collect_data=True,
                collect_frames=False,
                sim_rng=sim_rng,
                max_iterations=max_iterations,
            )
            results[threshold].append(np.asarray(msr_history))
    return results

threshold_values = list(range(20, 81, 10))
msr_ensemble_results = run_msr_ensemble(threshold_values)
''', ["archive-only", "remove-cell"], "")

    set_code(cells, "e079670d-fea9-479b-a72c-2e830ef7283b", '''# Aggregate statistics for every parameter in the sweep.
fig, ax = plt.subplots(figsize=(8.4, 4.6))
colours = plt.colormaps["viridis"](np.linspace(0.08, 0.92, len(threshold_values)))
budget = 101
for threshold, colour in zip(threshold_values, colours):
    padded = np.vstack([
        np.pad(run, (0, budget - len(run)), mode="edge")[:budget]
        for run in msr_ensemble_results[threshold]
    ])
    mean = padded.mean(axis=0)
    low, high = np.quantile(padded, [0.25, 0.75], axis=0)
    steps = np.arange(budget)
    ax.plot(steps, mean, color=colour, label=f"{threshold}%")
    ax.fill_between(steps, low, high, color=colour, alpha=0.13)
ax.set(xlabel="Simulation time step", ylabel="Mean similarity ratio")
ax.legend(title="Threshold", ncol=2, frameon=False)
plt.show()
''', ["archive-only", "remove-cell"], "")

    # Select the inline backend before pyplot is imported. On macOS, importing
    # pyplot first can initialise the GUI backend in a background process and
    # trigger repeated "Python quit unexpectedly" dialogs.
    imports = next(c for c in cells if c.get("id") == "9a2fe70d-c520-4fc6-94c8-53a0ac3c209a")
    import_source = "".join(imports["source"])
    import_source = import_source.replace("%matplotlib inline\n", "")
    imports["source"] = ("%matplotlib inline\n\n" + import_source.lstrip()).splitlines(keepends=True)

    # The later reusable simulation widget should expose the same time controls.
    packaged = next(c for c in cells if c.get("id") == "4764082c-7506-4beb-ad04-8e1ee70167d3")
    packaged_source = "".join(packaged["source"])
    old_controls = '''    # Create slider and playback
    slider = widgets.IntSlider(value=0, min=0, max=max_frame, step=1, description='Time')
    play   = widgets.Play(interval=400, value=0, min=0, max=max_frame, step=1)  # Slower default
    widgets.jslink((play, 'value'), (slider, 'value'))
    slider.observe(lambda change: show_frame(change['new']) if 'new' in change else None, names='value')
'''
    new_controls = '''    # Time, play/pause, and playback-speed controls
    slider = widgets.IntSlider(
        value=0, min=0, max=max_frame, step=1, description="Time",
        layout=widgets.Layout(width="520px"),
    )
    play = widgets.Play(interval=500, value=0, min=0, max=max_frame, step=1)
    delay = widgets.FloatSlider(
        value=0.5, min=0.1, max=2.0, step=0.1,
        description="Delay (s)", readout_format=".1f",
        layout=widgets.Layout(width="360px"),
    )
    widgets.jslink((play, "value"), (slider, "value"))
    slider.observe(lambda change: show_frame(change["new"]), names="value")
    delay.observe(
        lambda change: setattr(play, "interval", int(1000 * change["new"])),
        names="value",
    )
'''
    if old_controls in packaged_source:
        packaged_source = packaged_source.replace(old_controls, new_controls)
    packaged_source = packaged_source.replace(
        "simulation_box = widgets.VBox([out, widgets.HBox([play, slider])])",
        "simulation_box = widgets.VBox([out, widgets.HBox([play, slider]), delay])",
    )
    packaged["source"] = packaged_source.splitlines(keepends=True)

    # Prefer short sentences to parenthetical em dashes. Preserve quoted cells.
    for cell in cells:
        text = "".join(cell.get("source", []))
        text = text.replace("$5\times5$", "5 × 5").replace("$20\times20$", "20 × 20")
        text = text.replace("*Definition:* Segregation is", "Segregation is")
        text = text.replace("#FFD700", "#EDCC55").replace("#4682B4", "#5879AA")
        text = text.replace("Relocation step", "Simulation time step")
        text = text.replace("Note that I will typically capitalise the discipline and use lower case for a system that is complex.\n", "")
        text = text.replace("**B < E < A < C < D**", "B < E < A < C < D")
        if "reader-voice" not in text:
            text = text.replace(" — ", ". ").replace("—", ".").replace("&mdash;", ";")
            text = text.replace("notes. by hand", "notes by hand.")
            text = text.replace("notes by hand. \n", "notes by hand.\n")
            cell["source"] = text.splitlines(keepends=True)

    # These cells contain quotations, so the general pass above leaves them alone.
    for cell_id in ("bc090311-842b-4624-b243-0139b21a68d4",):
        cell = next(c for c in cells if c.get("id") == cell_id)
        text = "".join(cell.get("source", []))
        text = text.replace(
            "foundational tools—probability, differential equations, information theory, networks—for quantitative reasoning",
            "foundational tools of probability, differential equations, information theory, and networks. These support quantitative reasoning",
        )
        cell["source"] = text.splitlines(keepends=True)


def refresh_week02_lecture():
    path = ROOT / "notebooks/week02/L_Fractals.ipynb"
    nb = load(path)
    cells = nb["cells"]
    insert_once(cells, 0, "week02-learning-map", md("""<div class="reader-route">
  <div class="reader-route-label">This week</div>
  <div class="reader-route-body"><strong>Measure</strong> → <strong>zoom</strong> → <strong>generate</strong> → <strong>infer dimension</strong>.</div>
</div>

By the end of this week, you should be able to:

- explain why measured length can depend on resolution;
- recognise exact and statistical self-similarity;
- generate classic fractals using recursion, iterated functions, and L-systems; and
- derive or estimate a fractal dimension and interpret what it measures.
""", ["reader-only"], marker="week02-learning-map"))
    # Replace the long song excerpt with a lawful, more active opening.
    opening = next(c for c in cells if c.get("id") == "94007fbd-a8cf-444c-bdbb-24489ec9f641")
    opening["source"] = ["# Week 2: Fractals\n", "## Measuring the immeasurable"]
    song = cells[2]
    if song.get("cell_type") == "markdown":
        song["source"] = """<div class="reader-prompt">
  <div class="reader-prompt-label">Listen, look, predict</div>
  <div class="reader-prompt-body">As the <a href="https://www.youtube.com/watch?v=6tsutU92rrE" target="_blank">Mandelbrot Set song</a> begins, write down two visual features that feel “natural” and one mathematical rule you suspect could generate them.</div>
  <div class="reader-prompt-footnote">We will return to the mismatch between simple rules and intricate outcomes.</div>
</div>
""".splitlines(keepends=True)
    # Convert the first legacy blue question box to the shared prompt component.
    for c in cells:
        joined = "".join(c.get("source", []))
        if "Theoretical Question:" in joined and "coast of Britain" in joined:
            c["source"] = """<div class="reader-prompt">
  <div class="reader-prompt-label">Predict before measuring</div>
  <div class="reader-prompt-body">If the ruler length is halved, what happens to the number of rulers needed for (a) a square and (b) the coast of Britain? Sketch the relationship you expect on log–log axes.</div>
</div>
""".splitlines(keepends=True)
    checkpoint = md("""## Resolution experiment

In pairs, choose a jagged boundary in the room, on a map, or in an image.

1. Predict how its measured length changes as the ruler shrinks.
2. Decide which observations you would plot.
3. State what slope you expect and what that slope would mean.

<div class="reader-emphasis"><p>A dimension is a scaling relationship, not merely a label.</p></div>
""", ["slides"], "subslide", "week02-resolution-experiment")
    # Place directly after the coastline explanation if absent.
    if not any(c.get("id") == "week02-resolution-experiment" for c in cells):
        coast_index = next(i for i, c in enumerate(cells) if c.get("id") == "b9536d34-55fd-49e2-b17e-36aaf68b6732")
        cells.insert(coast_index + 1, checkpoint)
    if not any(c.get("id") == "week02-exit-ticket" for c in cells):
        cells.append(md(r"""# Exit ticket · explain the exponent

The Cantor set keeps $N=2$ pieces, each scaled by $r=1/3$.

- Predict its dimension without calculating.
- Calculate $D=\log N/\log(1/r)$.
- Explain, in one sentence, why the result lies between a point and a line.
""", ["slides"], "slide", "week02-exit-ticket"))
    add_image_alt_text(nb)
    save(path, nb)


def refresh_workshop(path, week, title, outcomes, route):
    nb = load(path)
    cells = nb["cells"]
    marker = f"week{week:02d}-workshop-guide"
    if not any(c.get("id") == marker for c in cells):
        guide = md(f"""# Week {week} workshop · {title}

<div class="reader-route">
  <div class="reader-route-label">Suggested route</div>
  <div class="reader-route-body">{route}</div>
</div>

## Learning outcomes

{outcomes}

## How to work

For each section: **predict first**, run the smallest useful experiment, record what changed, then explain the result to a partner. Code that runs is not yet an explanation.
""", marker=marker)
        cells.insert(0, guide)
    save(path, nb)


def refresh_workshops():
    refresh_workshop(
        ROOT / "notebooks/week01/WS_Introduction_to_complex_systems.ipynb", 1,
        "From local preferences to segregation",
        "- implement and test a one-dimensional Schelling model;\n- separate parameters, update rules, and observables;\n- compare qualitative and quantitative evidence;\n- test whether a conclusion is robust to initial conditions.",
        "Build → test one move → iterate → measure → challenge an assumption"
    )
    source = ROOT.parents[1] / "Workshops/WS_Fractals.ipynb"
    target = ROOT / "notebooks/week02/WS_Fractals.ipynb"
    if not target.exists():
        shutil.copy2(source, target)
    refresh_workshop(
        target, 2, "Build, measure, explain",
        "- implement recursive and iterative fractal generators;\n- compare three generative descriptions;\n- estimate box-counting dimension from data;\n- connect a fitted exponent to geometric complexity.",
        "Choose a generator → predict the pattern → run it → estimate dimension → explain the exponent"
    )
    nb = load(target)
    for cell in nb["cells"]:
        if cell.get("cell_type") == "markdown" and "# New stuff" in "".join(cell.get("source", [])):
            cell["source"] = ["# Tools for this week\n", "We use recursion and iteration to turn a compact rule into structure across scales."]
            break
    save(target, nb)


if __name__ == "__main__":
    refresh_week01_lecture()
    refresh_week02_lecture()
    refresh_workshops()
    print("Refreshed Week 1 and Week 2 lecture/workshop notebooks")
