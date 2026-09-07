#!/usr/bin/env python3
"""Restore the Week 5 motivational arc before the Vicsek construction."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week05/L_ABM.ipynb"


def markdown(source: str, slide_type: str = "", tags=None):
    cell = nbformat.v4.new_markdown_cell(source.strip() + "\n")
    if slide_type:
        cell.metadata["slideshow"] = {"slide_type": slide_type}
    if tags:
        cell.metadata["tags"] = tags
    return cell


nb = nbformat.read(NOTEBOOK, as_version=4)

# Replace the former thin "Collective behaviour" and "classic example" cells,
# then insert the recovered examples.  A marker makes this script idempotent.
start = next(i for i, c in enumerate(nb.cells) if "# Collective behaviour" in c.source)
end = next(i for i, c in enumerate(nb.cells) if "# From fixed spins to moving agents" in c.source)

motivation = [
    markdown(
        """
# Collective behaviour without a conductor

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/franklin_crowd_1000.jpg" alt="Thousands of spectators moving onto the field around Lance Franklin"></div>
<div class="text-panel">
<h3>A crowd becomes the event</h3>
<p>When Lance Franklin kicked his 1000th AFL goal in 2022, thousands of spectators moved onto the SCG almost at once.</p>
<p>No one specified every path. Individuals responded to the milestone, nearby people, gaps, barriers and the motion already under way.</p>
<p><a href="https://www.afl.com.au/video/726376/extraordinary-angles-of-the-crowd-swarm?videoId=726376" target="_blank" rel="noopener">Watch the AFL crowd-swarm footage</a></p>
</div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What would we need to retain to model the crowd: every person, the density of people, or both?</span></div>

<p class="media-credit">Image and video: AFL, “Extraordinary angles of the crowd swarm”, 25 March 2022.</p>
""",
        "subslide",
    ),
    markdown(
        """
The Franklin example is collective behaviour rather than a claim that a football crowd obeys the Vicsek rule. It establishes the modelling problem: coordinated system-level motion can arise without a central controller, while congestion, social cues, goals and boundaries still matter.

At the microscopic level we could record positions, headings, neighbours and decisions. At the macroscopic level we see a surge, a stream or a jam. An agent-based model keeps enough of the first description to ask how the second emerges.
""",
        tags=["reader-only"],
    ),
    markdown(
        """
## When is a group a flock?

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://www.youtube.com/embed/V4f_1_r80RY" title="A starling murmuration" style="width:100%;height:330px;border:0;" allowfullscreen></iframe></div>
<div class="text-panel">
<p>Everyday language treats the group as an entity:</p>
<p><strong>flock</strong> of birds<br><strong>murmuration</strong> of starlings<br><strong>parliament</strong> of owls<br><strong>chatter</strong> of budgerigars</p>
<p>For modelling, the useful feature is <strong>locally ordered collective motion</strong>, not the species name.</p>
</div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>How can a flock look like one object when no bird can observe the whole group?</span></div>

<p class="media-credit">Video: National Geographic, “Flight of the Starlings”.</p>
""",
        "subslide",
    ),
    markdown(
        """
Mathematically, “flocking” is used more broadly than its biological collective noun. It can describe coherent local motion in fish, bacteria, cells, robots and synthetic active matter. The shared observation is ordered movement; the mechanism must still be established for each system.

Starlings are a particularly convenient spectacle, but they are not the only starting point. Western Australia works hard to prevent invasive starlings from establishing, while native budgerigars provide a striking local example of collective motion.
""",
        tags=["reader-only"],
    ),
    markdown(
        """
## Budgerigars in the outback

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/outback_budgies.jpg" alt="A large flock of budgerigars gathering at an outback water source"></div>
<div class="text-panel">
<p>After favourable rain, budgerigar populations can increase rapidly. As the country dries, many smaller flocks converge on scarce water and food.</p>
<p>The visible flock is therefore shaped by local interaction <em>and</em> a changing environment. Collective motion is not produced by alignment alone.</p>
<p><a href="https://www.abc.net.au/news/2021-08-01/bumper-budgie-season-red-centre/100338202" target="_blank" rel="noopener">Read the ABC account</a></p>
</div>
</div>

<p class="media-credit">Photograph: ABC Alice Springs / Emma Haskin, 2021.</p>
""",
        "subslide",
    ),
    markdown(
        """
# Three disciplines, three modelling questions

| Perspective | Canonical model | Question retained |
|---|---|---|
| Computer graphics | Reynolds' boids | Which local rules create convincing coordinated motion? |
| Statistical physics | Vicsek et al. | What minimal ingredients produce order and a phase transition? |
| Behavioural biology | Couzin et al. | Which interaction zones reproduce observed animal groups? |

All three are agent-based models, but they are not interchangeable explanations. We use Vicsek because it most clearly isolates the competition between local alignment and noise (and is the simplest).
""",
        "slide",
    ),
    markdown(
        """
Craig Reynolds introduced boids for behavioural animation in the 1980s: separation avoids collisions, alignment matches nearby motion and cohesion pulls an agent towards neighbours. Vicsek and colleagues stripped collective motion back further to alignment, self-propulsion and noise. Couzin and colleagues instead used zones of repulsion, alignment and attraction to connect a model more directly to animal behaviour.

These are three answers to three related questions. A visually convincing flock need not identify the mechanism used by birds; a minimal phase-transition model need not reproduce every behavioural detail.
""",
        tags=["reader-only"],
    ),
    markdown(
        """
## Local rules changed what films could animate

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><iframe src="https://www.youtube.com/embed/Mo_1rAaj7FE" title="Boid-like swarm effects in Batman Returns" style="width:100%;height:275px;border:0;" allowfullscreen></iframe><p><strong>Batman Returns (1992):</strong> modified boid software was used for computer-generated bat swarms and marching penguins.</p></div>
<div class="image-panel"><iframe src="https://www.youtube.com/embed/lvBmrMEd254" title="Bird flock scene from Jurassic Park" style="width:100%;height:275px;border:0;" allowfullscreen></iframe><p><strong>Jurassic Park (1993):</strong> “Bet you'll never look at birds the same way.” The scene turns flocking into a clue about extinct collective behaviour.</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Does reproducing the motion explain the biological mechanism—or only show that the chosen rules are sufficient?</span></div>

<p class="media-credit">Boids history: Craig Reynolds, <a href="https://www.red3d.com/cwr/boids/" target="_blank" rel="noopener">Boids</a>. Film excerpts are used for teaching and commentary.</p>
""",
        "subslide",
    ),
    markdown(
        """
## Beyond birds: people and traffic

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><iframe src="https://www.youtube.com/embed/LzjifmHavAQ" title="Self-organised traffic in Hanoi" style="width:100%;height:315px;border:0;" allowfullscreen></iframe></div>
<div class="text-panel">
<h3>Hanoi traffic</h3>
<p>Dense motion can remain flowing even when lanes and central control are weak. Drivers respond to nearby vehicles, gaps, expected motion and collision risk.</p>
<p>The same vocabulary—agents, local interaction, boundaries and emergent flow—applies, but the rules and objectives differ from a bird flock.</p>
</div>
</div>

<p class="media-credit">Video: Yoav Ben-Dov, “Self-organization in Hanoi traffic”.</p>
""",
        "subslide",
    ),
    markdown(
        """
### Explore collective motion in other settings

- [The Walking Head](https://www.complexity-explorables.org/explorables/the-walking-head/) — pedestrian motion and local avoidance.
- [Berlin 8:00 AM](https://www.complexity-explorables.org/explorables/berlin-8-am/) — traffic flow and congestion.
- [I Herd You](https://www.complexity-explorables.org/explorables/i-herd-you/) — collective decisions and social influence.
- [Flock'n Roll](https://www.complexity-explorables.org/explorables/flockn-roll/) — zones of repulsion, alignment and attraction.

These are not interchangeable demonstrations of one rule. They are prompts to identify the agents, retained state, interaction network, environment and system-level behaviour in each model.
""",
        "subslide",
    ),
]

nb.cells[start:end] = motivation

# The recovered "Three disciplines" slide supersedes the thinner table that
# previously appeared after the Ising/XY bridge.
nb.cells = [
    cell for cell in nb.cells if "# Three routes to flocking" not in cell.source
]

nbformat.write(nb, NOTEBOOK)
