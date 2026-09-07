import json
from pathlib import Path


path = Path("notebooks/week06/L_Synchronisation.ipynb")
nb = json.loads(path.read_text())


def set_md(index: int, text: str) -> None:
    assert nb["cells"][index]["cell_type"] == "markdown"
    nb["cells"][index]["source"] = text.splitlines(keepends=True)


set_md(1, '''# Real-world motivation

<iframe style="display:block;width:78%;height:440px;margin:0 auto" src="https://www.youtube.com/embed/JWToUATLGzs" title="Metronomes synchronising through a shared platform" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>How are the metronomes coordinating their behaviour?</span></div>
''')

set_md(2, '''## Huygens · the sympathy of two clocks

Huygens was developing pendulum clocks for determining longitude at sea. Ships were to carry more than one clock so that a working timekeeper remained if another stopped or needed cleaning.

In 1665 he noticed that two such clocks, suspended from the same support, settled into a stable timing relationship.

<div class="reader-voice">
  <div class="reader-voice-quote">A wonderful effect that nobody could have thought of before.</div>
  <div class="reader-voice-attr">— Christiaan Huygens, letter to Constantijn Huygens, 26 February 1665</div>
</div>

Small movements of the shared support allowed each clock to affect the other. When the clocks were separated, the coordination disappeared.

<p class="figure-credit"><a href="https://www.dbnl.org/tekst/huyg003oeuv05_01/huyg003oeuv05_01_0141.php">Huygens's February 1665 correspondence</a>; maritime context in <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC5627120/">Oliveira and Melo (2015)</a>.</p>
''')

set_md(3, '''## Synchrony can help or harm

| System | Oscillating components | Effect of coordination |
|---|---|---|
| Heart | pacemaker cells | coordinated contraction |
| Circadian system | biological clocks | timing across tissues |
| Power grid | electrical generators | stable shared frequency |
| Brain | neural populations | communication, but excessive synchrony can be pathological |
| Footbridge and crowd | bridge motion and pedestrian responses | feedback can amplify unwanted wobble |

The examples include both useful coordination and damaging feedback. Synchrony is not automatically desirable.
''')

set_md(4, '''## The wobbling Millennium Bridge

<div class="two-panel wide-left compact-panels">
<div class="image-panel">
<iframe style="display:block;width:100%;height:410px;margin:0 auto" src="https://www.youtube.com/embed/y2FaOJxWqLE" title="The Millennium Bridge wobbling shortly after opening in June 2000" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>
<div class="text-panel">
<p>Pedestrians responded to lateral bridge motion, and their response fed energy back into the bridge.</p>
<p>The wobble did not require the whole crowd to march in step.</p>
</div>
</div>

<p class="figure-credit">Opening-day footage filmed in June 2000. <a href="https://www.youtube.com/watch?v=y2FaOJxWqLE">The Wibbly Wobbly Millennium Bridge in London</a>.</p>
''')

set_md(7, '''## Specify the model

| Ingredient | Representation |
|---|---|
| Individual state | phase within a cycle |
| Internal dynamics | natural angular frequency |
| Interaction | phase-dependent coupling |
| Network | who can influence whom |
| Observable | collective phase coherence |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>We keep timing and omit amplitude, waveform and biological detail.</span></div>
''')

set_md(17, '''## Kuramoto model · assumptions

| Element | Kuramoto choice |
|---|---|
| State | phase $\\theta_i$ |
| Internal dynamics | natural frequency $\\omega_i$ |
| Network | complete graph |
| Interaction | sinusoidal attraction |
| Control parameter | coupling $K$ |
| Observable | coherence $r$ |

Mechanical, electrical, chemical and informational coupling are properties of the system. The modelling choice is how to represent that mechanism and which details to omit.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The standard Kuramoto model represents coupling as equal, instantaneous and all-to-all. Other systems require different networks, weights or delays.</span></div>
''')

set_md(29, '''## From pendulum clocks to living systems

Huygens was developing pendulum clocks for determining longitude at sea. His instructions called for ships to carry at least two clocks: if one stopped or needed cleaning, another would still be running. In 1665, while observing two such clocks suspended from the same support, he noticed that their pendulums settled into a stable timing relationship. When he separated the clocks, the effect disappeared. The shared support allowed the clocks to influence one another.

[Huygens's February 1665 correspondence](https://www.dbnl.org/tekst/huyg003oeuv05_01/huyg003oeuv05_01_0141.php) records the observation. The maritime purpose and need for redundant clocks are discussed by [Oliveira and Melo (2015)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5627120/).

Similar coordination occurs in very different systems:

- pacemaker cells coordinate contraction in the heart;
- interacting biological clocks coordinate circadian timing;
- generators must remain coordinated within a power grid;
- lasers and Josephson-junction arrays can develop collective coherence;
- neural populations can synchronise, although excessive or abnormally persistent synchrony is associated with epileptic seizures and pathological beta-band activity in Parkinson's disease.

The examples above include both useful coordination and coupling-driven instability. Synchrony is not automatically desirable.
''')

set_md(30, '''### The wobbling Millennium Bridge

<iframe style="display:block;width:78%;height:360px;margin:0 auto" src="https://www.youtube.com/embed/y2FaOJxWqLE" title="The Millennium Bridge wobbling shortly after opening in June 2000" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<p class="figure-credit">Opening-day footage filmed in June 2000. <a href="https://www.youtube.com/watch?v=y2FaOJxWqLE">The Wibbly Wobbly Millennium Bridge in London</a>.</p>

When London's Millennium Bridge opened in 2000, feedback between pedestrians and the bridge produced large lateral oscillations. Early explanations emphasised walkers synchronising their footsteps with the bridge. Later models and measurements showed that the whole crowd need not march in step: pedestrian responses to bridge motion can reduce the structure's effective damping, and above a sufficiently large crowd the wobble grows.

Both sides have dynamics. Pedestrians adjust their gait in response to the moving bridge, while the bridge responds mechanically to the pedestrians.

*Further reading:* [Strogatz et al. (2005), *Theoretical mechanics: Crowd synchrony on the Millennium Bridge*](https://doi.org/10.1038/438043a) and [Belykh et al. (2021), *Emergence of the London Millennium Bridge instability without synchronisation*](https://doi.org/10.1038/s41467-021-27568-y).
''')

set_md(31, '''## Fireflies

<iframe style="display:block;width:100%;height:520px;margin:0 auto 1rem auto" src="https://www.youtube.com/embed/0BOjTMkyfIA" title="Real synchronous fireflies in the Great Smoky Mountains" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<p class="figure-credit">Real <em>Photinus carolinus</em> fireflies. National Geographic, 2016.</p>

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Nicky_Case_fireflies.png" alt="Fireflies represented by individual internal clocks"></div>
<div class="text-panel">
<p>Each firefly continues through its own flashing cycle even in isolation: it has internal dynamics as well as an interaction rule.</p>
<p>A perceived flash can shift another firefly's clock.</p>
<p>Coherent flashing emerges from those local adjustments.</p>
</div>
</div>

*Explore: [Nicky Case, “Fireflies”](https://ncase.me/fireflies/).*
''')

set_md(32, '''## Represent the firefly clocks

| Ingredient | Firefly interpretation |
|---|---|
| Individual state | position within a flashing cycle |
| Internal dynamics | its natural flashing rate, present without neighbours |
| Interaction network | which flashes it can perceive |
| Coupling | how a perceived flash shifts its cycle |
| Observable | collective coherence |

A repeating internal clock can be represented by its position within a cycle.
''')

set_md(43, '''### Coupling in the system and in the model

Mechanical, electrical, chemical and informational coupling describe different physical systems. Coupling may act one way or both ways, locally or globally, continuously or in pulses, immediately or after a delay. These features belong to the system being represented. The modeller decides how to encode them and which details can be omitted.

Occasional alignment is not enough to establish synchronisation. The interaction must alter the dynamics and maintain a relationship between their timings.

| Element | Kuramoto choice |
|---|---|
| Node state | phase $\\theta_i$ |
| Internal dynamics | natural frequency $\\omega_i$ |
| Network | complete graph |
| Interaction | sinusoidal phase attraction |
| Control parameter | coupling strength $K$ |
| Observable | phase coherence $r$ |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The complete graph and equal coupling weights are simplifying assumptions, not properties of synchronisation itself.</span></div>
''')

# Remove a few stock phrases elsewhere without changing the mathematical argument.
replacements = {
    "This exact reduction relies on all-to-all sinusoidal coupling.": "The reduction relies on all-to-all sinusoidal coupling.",
    "This is sufficient here.": "That level of analysis is sufficient here.",
    "The ladder remains useful: move down to inspect phases and coupling; move up to coherence, transitions, and ensemble behaviour.": "Individual phases and coupling sit below coherence, parameter sweeps and ensemble behaviour on the ladder of abstraction.",
    "Many oscillating systems repeatedly pass through the same sequence of states. If the cycle is stable and timing is the question, position within that cycle can be represented by one angle.": "Many oscillating systems repeatedly pass through the same sequence of states. If the cycle repeats reliably and only timing matters, one angle is enough to represent position within the cycle.",
    "Many systems repeatedly pass through approximately the same sequence of states: a flashing cycle, a heartbeat or a chemical oscillation. When that cycle is stable and timing is the main question, position within it can be represented by an angle.": "Many systems repeatedly pass through approximately the same sequence of states: a flashing cycle, a heartbeat or a chemical oscillation. If the cycle repeats reliably and only timing matters, an angle can represent position within it.",
    "Amplitude is deliberately omitted. This is reasonable when disturbances decay back towards the same stable cycle and we care chiefly about whether the timings coordinate.": "Amplitude is omitted. The reduction is reasonable when disturbances decay back towards the same stable cycle and only the timing is of interest.",
    "The order parameter makes a coupling sweep measurable, but the curve is not determined by $K$ alone.": "The order parameter lets us compare a sweep over coupling strength, but the curve is not determined by $K$ alone.",
    "This is the cleanest expression of the week’s modelling focus: heterogeneity changes the collective threshold.": "Heterogeneity therefore changes the collective threshold.",
    "This is why a parameter sweep should be followed by repeated runs.": "A parameter sweep should therefore be followed by repeated runs.",
    "Separating `omega` from `phase_rate` makes the modelling focus visible: agents can differ intrinsically even though they obey the same coupling rule.": "Separating `omega` from `phase_rate` records the heterogeneity explicitly: agents can differ intrinsically even though they obey the same coupling rule.",
}
for cell in nb["cells"]:
    if cell["cell_type"] != "markdown":
        continue
    text = "".join(cell["source"])
    for old, new in replacements.items():
        text = text.replace(old, new)
    cell["source"] = text.splitlines(keepends=True)

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
