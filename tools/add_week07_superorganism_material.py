#!/usr/bin/env python3
"""Strengthen Week 7's early superorganism framing and add the waggle dance."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week07/L_Intelligent_systems.ipynb"
FRAMING_ID = "5aa96f13"
WAGGLE_ID = "week07-waggle-dance-reader"
HIRO_VIDEO_ID = "872c458e"
ANT_BRIDGE_VIDEO_ID = "37d055ce"

FRAMING = r"""
**The basic idea** is that information available to one member can alter what other members do. Repeated across a population, communication can give the group access to discoveries and responses that no individual possesses alone.

<div class="reader-voice">
  <div class="reader-voice-quote">In theory at least, individual members of the school can profit from the discoveries and previous experience of all other members of the school during the search for food. This advantage can become decisive, outweighing the disadvantages of competition for food items, whenever the resource is unpredictably distributed in patches.</div>
  <div class="reader-voice-attr">E. O. Wilson, <em>Sociobiology: The New Synthesis</em> (1975)</div>
</div>

Ants, honeybees and termites are often described as **superorganisms**. Their colonies have persistent organisation, division of labour and specialised reproductive roles, and many useful functions belong to the colony rather than to any one member. Calling the individuals “simple” is only shorthand: each animal has its own sensory and behavioural capacities. The important modelling fact is that no individual holds all of the colony's information or directs the complete response.

A honeybee colony can regulate hive temperature and choose a new nest site; ants can organise traffic, construct nests and living bridges, or assemble into a raft during a flood. These outcomes depend on interactions among individuals and, often, information stored or transmitted through their environment. This is the biological inspiration for distributed computation: useful group behaviour without a central controller.
""".strip()

WAGGLE = r"""
### Honeybees: information carried by a dance

When a successful honeybee forager returns to the hive, her **waggle dance** can recruit other foragers to the resource. The angle of the waggle run relative to vertical represents the direction of travel relative to the Sun, while its duration represents distance. The dance therefore communicates information about a place that is currently outside the hive and out of sight.

<div class="video-embed"><iframe width="720" height="405" src="https://www.youtube-nocookie.com/embed/-7ijI-g4jHg?rel=0" title="Bee Dance (Waggle Dance)" frameborder="0" allowfullscreen></iframe>
<p class="media-credit">Video: <a href="https://www.youtube.com/watch?v=-7ijI-g4jHg" target="_blank" rel="noopener">Bee Dance (Waggle Dance)</a>.</p></div>

This is a useful contrast with ant pheromone trails. The bee performs a signal to nearby nestmates; an ant trail leaves a changing trace in the environment that later ants can encounter. Both distribute information, but they use different media, persist for different lengths of time and support different collective decisions.
""".strip()

HIRO_VIDEO = r"""
<div class="video-embed"><iframe width="720" height="405" src="https://www.youtube-nocookie.com/embed/fsVJuN75vzE" title="Hiro Hamada's microbots presentation in Big Hero 6" frameborder="0" allowfullscreen></iframe>
<p class="media-credit">Film excerpt: Walt Disney Animation Studios, <a href="https://www.youtube.com/watch?v=fsVJuN75vzE" target="_blank" rel="noopener"><em>Big Hero 6</em> (2014), “Hiro Hamada’s microbots presentation”</a>.</p></div>
""".strip()

ANT_BRIDGE_VIDEO = r"""
<div class="video-embed"><iframe width="720" height="405" src="https://www.youtube-nocookie.com/embed/pa5UnI279Es" title="Ants making a bridge" frameborder="0" allowfullscreen></iframe>
<p class="media-credit">Video: <a href="https://www.youtube.com/watch?v=pa5UnI279Es" target="_blank" rel="noopener">Arjunc369, “Ants making bridge, team work”</a>.</p></div>
""".strip()


def main():
    notebook = nbf.read(NOTEBOOK, as_version=4)
    framing_index = next(
        (i for i, cell in enumerate(notebook.cells) if cell.id == FRAMING_ID), None
    )
    if framing_index is None:
        raise RuntimeError(f"Could not find Week 7 framing cell {FRAMING_ID}")

    notebook.cells[framing_index].source = FRAMING

    existing = next(
        (cell for cell in notebook.cells if cell.id == WAGGLE_ID), None
    )
    if existing is not None:
        existing.source = WAGGLE
        existing.metadata["tags"] = ["reader-only"]
    else:
        cell = nbf.v4.new_markdown_cell(WAGGLE, id=WAGGLE_ID)
        cell.metadata["tags"] = ["reader-only"]
        notebook.cells.insert(framing_index + 1, cell)

    hiro_video = next(
        (cell for cell in notebook.cells if cell.id == HIRO_VIDEO_ID), None
    )
    if hiro_video is None:
        raise RuntimeError(f"Could not find Hiro Hamada video cell {HIRO_VIDEO_ID}")
    hiro_video.source = HIRO_VIDEO

    ant_bridge_video = next(
        (cell for cell in notebook.cells if cell.id == ANT_BRIDGE_VIDEO_ID), None
    )
    if ant_bridge_video is None:
        raise RuntimeError(f"Could not find ant bridge video cell {ANT_BRIDGE_VIDEO_ID}")
    ant_bridge_video.source = ANT_BRIDGE_VIDEO

    nbf.write(notebook, NOTEBOOK)


if __name__ == "__main__":
    main()
