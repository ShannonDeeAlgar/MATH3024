from pathlib import Path
import nbformat


ROOT = Path(__file__).resolve().parents[1]
WEEK2 = ROOT / "notebooks/week02/L_Fractals.ipynb"
WEEK3 = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
IMAGES = WEEK3.parent / "images"


def md(source, cell_id, slide_type="slide", tags=None):
    cell = nbformat.v4.new_markdown_cell(source.strip())
    cell["id"] = cell_id
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    if tags:
        cell.metadata["tags"] = tags
    return cell


def write_svg(name, body, width=1200, height=680):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
text {{ font-family: "DejaVu Sans", sans-serif; fill: #17284d; }}
.title {{ font-size: 28px; font-weight: 700; }}
.label {{ font-size: 22px; font-weight: 700; }}
.body {{ font-size: 18px; }}
.small {{ font-size: 15px; fill: #52627f; }}
.panel {{ fill: none; stroke: #bcc8dc; stroke-width: 2; }}
.navy {{ stroke: #17284d; fill: none; stroke-width: 5; }}
.blue {{ stroke: #5d7fae; fill: none; stroke-width: 5; }}
.yellow {{ stroke: #efc94c; fill: none; stroke-width: 5; }}
</style>
{body}
</svg>"""
    (IMAGES / name).write_text(svg, encoding="utf-8")


def week2_marker():
    nb = nbformat.read(WEEK2, 4)
    first = nb.cells[0]
    if "canonical-model-marker" not in first.source:
        first.source = """# Fractals
## MATH3024 · Week 2

<div class="canonical-model-marker"><span>Canonical models</span><strong>Cantor set and Sierpiński triangle</strong></div>"""
    nbformat.write(nb, WEEK2)


def assets():
    write_svg(
        "coffee_convection.svg",
        """
<rect x="55" y="70" width="1090" height="500" rx="26" class="panel"/>
<path d="M215 410 C120 300,165 155,300 155 C435 155,480 300,385 410 C310 495,290 495,215 410Z" class="navy"/>
<path d="M470 410 C375 300,420 155,555 155 C690 155,735 300,640 410 C565 495,545 495,470 410Z" class="blue"/>
<path d="M725 410 C630 300,675 155,810 155 C945 155,990 300,895 410 C820 495,800 495,725 410Z" class="yellow"/>
<path d="M268 430 L268 195 M523 430 L523 195 M778 430 L778 195" stroke="#17284d" stroke-width="4" marker-end="url(#a)"/>
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#17284d"/></marker></defs>
<text x="600" y="45" text-anchor="middle" class="title">Rayleigh–Bénard convection</text>
<text x="600" y="620" text-anchor="middle" class="body">Warm fluid rises, cool fluid sinks, and neighbouring rolls organise into cells.</text>
""",
    )

    # Six linear modes described in Turing's 1952 classification.
    panels = []
    labels = [
        ("a", "Long-wave stationary", "broad drift"),
        ("b", "Long-wave oscillation", "whole field pulses"),
        ("c", "Shortest-wave stationary", "neighbours alternate"),
        ("d", "Finite-wave stationary", "fixed spacing"),
        ("e", "Finite-wave travelling", "pattern moves"),
        ("f", "Shortest-wave oscillation", "neighbours alternate in time"),
    ]
    for q, (letter, title, subtitle) in enumerate(labels):
        col, row = q % 3, q // 3
        x, y = 35 + col * 385, 70 + row * 285
        panels.append(f'<rect x="{x}" y="{y}" width="355" height="240" rx="12" class="panel"/>')
        panels.append(f'<text x="{x+18}" y="{y+34}" class="label">({letter}) {title}</text>')
        panels.append(f'<text x="{x+18}" y="{y+218}" class="small">{subtitle}</text>')
        if letter == "a":
            panels.append(f'<path d="M{x+35} {y+155} C{x+120} {y+80},{x+245} {y+80},{x+320} {y+155}" class="navy"/>')
        elif letter == "b":
            panels.append(f'<path d="M{x+35} {y+125} C{x+95} {y+55},{x+155} {y+195},{x+215} {y+125} S{x+300} {y+55},{x+325} {y+125}" class="blue"/>')
        elif letter == "c":
            for j in range(10):
                fill = "#17284d" if j % 2 == 0 else "#efc94c"
                panels.append(f'<rect x="{x+35+j*29}" y="{y+85}" width="29" height="82" fill="{fill}"/>')
        elif letter == "d":
            panels.append(f'<path d="M{x+28} {y+135} C{x+65} {y+65},{x+102} {y+65},{x+139} {y+135} S{x+213} {y+205},{x+250} {y+135} S{x+304} {y+65},{x+327} {y+135}" class="navy"/>')
        elif letter == "e":
            panels.append(f'<path d="M{x+35} {y+150} C{x+80} {y+70},{x+125} {y+70},{x+170} {y+150} S{x+260} {y+230},{x+315} {y+150}" class="blue"/>')
            panels.append(f'<path d="M{x+105} {y+70} L{x+245} {y+70}" stroke="#efc94c" stroke-width="5" marker-end="url(#a)"/>')
        else:
            for j in range(10):
                fill = "#5d7fae" if j % 2 == 0 else "#17284d"
                panels.append(f'<circle cx="{x+48+j*29}" cy="{y+125}" r="{11 if j%2==0 else 22}" fill="{fill}"/>')
    write_svg(
        "turing_six_linear_modes.svg",
        '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#efc94c"/></marker></defs>'
        + '<text x="600" y="38" text-anchor="middle" class="title">Turing’s six linear outcomes</text>'
        + "".join(panels),
        height=660,
    )

    write_svg(
        "gray_scott_model_map.svg",
        """
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#17284d"/></marker></defs>
<text x="600" y="42" text-anchor="middle" class="title">The Gray–Scott model</text>
<rect x="55" y="105" width="245" height="145" rx="15" class="panel"/>
<text x="177" y="150" text-anchor="middle" class="label">Feed</text>
<text x="177" y="190" text-anchor="middle" class="body">U enters at rate f</text>
<rect x="475" y="90" width="255" height="175" rx="15" class="panel"/>
<text x="602" y="135" text-anchor="middle" class="label">Autocatalytic reaction</text>
<text x="602" y="185" text-anchor="middle" class="body">U + 2V → 3V</text>
<text x="602" y="225" text-anchor="middle" class="small">local rate UV²</text>
<rect x="900" y="105" width="245" height="145" rx="15" class="panel"/>
<text x="1022" y="150" text-anchor="middle" class="label">Removal</text>
<text x="1022" y="190" text-anchor="middle" class="body">V leaves at rate f + k</text>
<path d="M300 178 L460 178" stroke="#17284d" stroke-width="5" marker-end="url(#a)"/>
<path d="M730 178 L885 178" stroke="#17284d" stroke-width="5" marker-end="url(#a)"/>
<rect x="110" y="315" width="980" height="105" rx="15" class="panel"/>
<text x="600" y="355" text-anchor="middle" class="label">Diffusion</text>
<text x="600" y="395" text-anchor="middle" class="body">U and V spread through space at rates D<tspan baseline-shift="sub">U</tspan> and D<tspan baseline-shift="sub">V</tspan></text>
<text x="600" y="500" text-anchor="middle" class="body">∂U/∂t = D<tspan baseline-shift="sub">U</tspan>∇²U − UV² + f(1−U)</text>
<text x="600" y="555" text-anchor="middle" class="body">∂V/∂t = D<tspan baseline-shift="sub">V</tspan>∇²V + UV² − (f+k)V</text>
<text x="600" y="625" text-anchor="middle" class="small">Reaction changes concentrations locally. Diffusion couples neighbouring locations. Feed and removal keep the system driven.</text>
""",
        height=660,
    )

    # Representative space-time fields for the six linear mode classes. The
    # patterns are deliberately schematic, not nonlinear Gray–Scott results.
    mode_panels = []
    mode_titles = [
        "(a) long-wave stationary", "(b) long-wave oscillation",
        "(c) shortest-wave stationary", "(d) finite-wave stationary",
        "(e) finite-wave travelling", "(f) shortest-wave oscillation",
    ]
    for q, title in enumerate(mode_titles):
        col, row = q % 3, q // 3
        x0, y0 = 45 + col * 385, 75 + row * 285
        mode_panels.append(f'<rect x="{x0}" y="{y0}" width="350" height="235" rx="10" class="panel"/>')
        mode_panels.append(f'<text x="{x0+175}" y="{y0+30}" text-anchor="middle" class="label">{title}</text>')
        # A compact heatmap-like representation with time running upward.
        for iy in range(12):
            for ix in range(18):
                if q == 0:
                    value = ix < 9
                elif q == 1:
                    value = (iy // 2) % 2 == 0
                elif q == 2:
                    value = ix % 2 == 0
                elif q == 3:
                    value = (ix // 3) % 2 == 0
                elif q == 4:
                    value = ((ix - iy) // 3) % 2 == 0
                else:
                    value = (ix + iy) % 2 == 0
                colour = "#17284d" if value else "#efc94c"
                mode_panels.append(
                    f'<rect x="{x0+18+ix*17}" y="{y0+46+iy*13}" width="17" height="13" fill="{colour}"/>'
                )
        mode_panels.append(f'<text x="{x0+175}" y="{y0+222}" text-anchor="middle" class="small">space → · time ↑</text>')
    write_svg(
        "turing_six_mode_evolution.svg",
        '<text x="600" y="38" text-anchor="middle" class="title">Representative evolution of Turing’s six linear modes</text>'
        + "".join(mode_panels),
        height=660,
    )


def week3_revise():
    nb = nbformat.read(WEEK3, 4)
    by_id = {c.get("id"): c for c in nb.cells}

    remove = {
        "9253675a-2529-494e-b524-48a841f31a6d",  # dull Pattern formation opener
        "aa5c1c67-775b-4c33-a738-d67e5ff040b1",
        "19b18f71-7c97-4558-b5d5-9b7b5ec19b55",
        "ab306a33-821c-4d0f-a6e1-f145d0688da8",
        "week03-many-pattern-mechanisms",
        "a5a1b98b-07e0-4417-be77-e1090bcfd254",
        "461b78ee-5bb0-43e7-bf03-63d7fcdd6874",
        "d0523d87-a29f-493f-b63c-7ba22a0e04e8",
        "7793fce9-8449-4370-9fc9-d242315fe91b",
        "d794ddf0-4409-4ee1-abd9-7623be05e5d6",
        "cdf38106-a059-4da5-8d31-b2a4bf6e06a7",
        "cf9b7d43-46c3-4357-a3d2-78ca52b34262",
        "0183b6c2-709d-47ed-89b6-202700b27ec6",
        "491e85da-c778-4d46-ad4c-9a89210e42a4",
        "26286a64",
        "3eb4d29c-82d2-467c-99b2-70ff7945b37d",
        "4aeacfff",
        "afdf9f9c-ad1a-4efd-9aef-d7b036bf0cc6",
        "1416a205-8ab4-435c-b931-cc379bc572cb",
        "5bc43079",
        "e5f79f48-d91b-473c-a24a-2d442239d788",
        "e6b584f8-26c4-45c2-8873-a6be6658da5a",
        "db1a470f",
        "c5c3ba5e",
        "41bc5b10-40b8-4223-9cef-57fbdf5e8f77",
        "aa81f828-45bd-4d17-a25b-eab81f382f2d",
        "07950304-3a76-41bc-8ad5-4dfe3a8647a8",
        "259fd509",
        "18ce876a-1c28-4ae0-ad58-ecc520a84871",
        "0e5a68cf-2fac-4c44-b359-6a6055253a03",
        "f7ee60e4",
        "3c79bb52-29de-454b-a8b6-7f8aaa3525e2",
        "46796b54",
        "78500506-7c93-46a4-a0f6-c639fa9285d4",
        "ee05f8af",
        "6ae25a88",
        "9988c7d6",
        "e8dcc61b-bf48-4883-8aad-f10062a3ecc9",
        "be885d2d-a4ed-4acd-8bb7-ae9156784b88",
        "150735d5",
        "41e54183",
        "e568a57f-c749-47ab-8fe7-fb411fa60a0e",
        "05ae13c3-a003-461f-bf27-470d8c028aa4",
        "095f1046-4e61-4e60-9f8b-19666e8ba127",
        "343066e2-df03-4412-bce6-9202be5d263a",
        "0d3639e9",
        "cf3a6cdf-3b03-4aa5-a15f-67cbf35f26b3",
        "359763fd-9713-4e44-86c4-a9e23615cc1e",
        "week03-pattern-family",
        "a45a0945-5b93-4ba3-9345-168dd54d526c",
        "d5cb018d-702d-462f-b281-49a412e736f5",
    }
    nb.cells = [c for c in nb.cells if c.get("id") not in remove]

    # Replace the coffee/garlic comparison with two static, reliably rendered images.
    by_id["7347319d-2e0d-49d0-a1c3-ac02ffcd446d"].source = """# Similar form, different mechanisms

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/coffee_convection.svg" alt="Schematic convection cells in a heated liquid"></div>
<div class="image-panel"><img src="images/Garlic_intersection.jpeg" alt="Cell-like pattern in a cut garlic bulb"></div>
</div>

The patterns look similar. The mechanisms are not: fluid circulation produces convection cells, while biological growth partitions the garlic tissue.

<p class="figure-reference">Right: section through a garlic bulb. Left: schematic of Rayleigh–Bénard convection.</p>"""

    by_id["a0a1efe7-e26e-4f6d-a529-3db70b3fe94f"].source = """# Turing’s question: how does form emerge?

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/turing_1952_first_page.png" alt="First page of Turing's 1952 paper"></div>
<div class="text-panel">
<p>An embryo begins close to uniform, yet organised differences appear. Turing asked whether reacting and diffusing chemicals could create spatial structure without a pre-drawn template.</p>
</div>
</div>

<p class="figure-reference">A. M. Turing (1952), <a href="https://doi.org/10.1098/rstb.1952.0012">“The Chemical Basis of Morphogenesis”</a>, <em>Philosophical Transactions of the Royal Society B</em> 237, 37–72.</p>"""

    by_id["b72f5b93"].source = """## Reaction and diffusion

Turing’s proposal combines two familiar processes:

- **Reaction** changes chemical concentrations locally. Feedback can reinforce or suppress a small difference.
- **Diffusion** transports chemicals through space. If the chemicals diffuse at different rates, a local change can influence nearby and more distant locations differently.

Diffusion normally smooths a field. In a suitable coupled system, however, unequal diffusion can destabilise a uniform state. This is the Turing instability."""

    by_id["d112f5d4"].source = """## Build the Turing mechanism

<div class="analysis-perspectives">
<div><strong>Local activation</strong><br>A small increase promotes further increase nearby.</div>
<div><strong>Longer-range inhibition</strong><br>A faster-spreading influence suppresses the change farther away.</div>
</div>

Reaction supplies the feedback. Unequal diffusion supplies the different spatial ranges. Neither phrase names a separate ingredient."""

    six = md(
        """## Six possible linear outcomes

<img src="images/turing_six_linear_modes.svg" alt="Schematic of the six classes of linear behaviour described by Turing" style="display:block;width:88%;margin:0 auto">

Turing classified the first response of a uniform state by asking whether it is stationary or oscillatory, and whether its dominant wavelength is long, finite, or as short as the cells allow.

<p class="figure-reference">Schematic summary of cases (a)–(f) in Turing (1952), §6.</p>""",
        "week03-turing-six-modes",
    )
    six_reader = md(
        """### Reading the six cases

Turing’s cases are linear modes near the uniform state, not six finished animal-coat pictures.

| Case | First response |
|---|---|
| (a) | stationary change with a very long wavelength |
| (b) | long-wave oscillation |
| (c) | stationary alternation at the shortest grid wavelength |
| (d) | stationary pattern with a finite wavelength |
| (e) | travelling finite-wavelength pattern |
| (f) | shortest-wave oscillation, with neighbouring cells out of phase |

Case (d) is the familiar stationary Turing-pattern route. Turing noted that travelling waves require at least three morphogens in his linear treatment.""",
        "week03-turing-six-reader",
        tags=["reader-only"],
    )
    dapple = md(
        """## Turing computed a pattern by hand

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Turing_1952_dappled.png" alt="Turing's manually calculated dappled concentration pattern"></div>
<div class="text-panel"><p>Turing wrote that this “dappled” pattern was obtained “in a few hours by a manual computation”. It was a small numerical demonstration that the mechanism could produce spatial structure.</p></div>
</div>

<p class="figure-reference">Turing (1952), Figure 2 and accompanying text, pp. 63–64.</p>""",
        "week03-turing-dappled",
    )

    history = md(
        """# The Gray–Scott model

## Where it came from

“Gray–Scott” names two researchers: **Peter Gray** and **Stephen K. Scott**. Their model described autocatalytic chemistry in a continuously fed reactor. It was not originally proposed as an animal-coat model.

John Pearson’s 1993 simulations showed that the spatial model produces a striking range of spots, stripes, waves, and self-replicating structures. That work helped establish it as a canonical reaction–diffusion model.

<p class="figure-reference">Gray &amp; Scott (1984), <em>Chemical Engineering Science</em> 39; Pearson (1993), <a href="https://doi.org/10.1126/science.261.5118.189">“Complex patterns in a simple system”</a>, <em>Science</em> 261.</p>""",
        "week03-gray-scott-history",
    )

    by_id["8858f425-48a5-492b-9a5a-2d277dacc632"].source = r"""## 1. Reaction

$$U+2V\longrightarrow 3V,\qquad \text{local rate }UV^2.$$

The reaction is autocatalytic: $V$ helps convert $U$ into more $V$. The nonlinear term $UV^2$ makes that local positive feedback explicit.

<div class="analysis-perspectives">
<div><strong><em>U</em></strong><br>feed chemical</div>
<div><strong><em>V</em></strong><br>autocatalytic chemical</div>
</div>"""
    by_id["b7c839be-6ee3-4fef-9aae-72b880dbb4b9"].source = r"""### Random walk: a discrete model

At each step, choose one displacement:

$$
(\pm\Delta x,0),\qquad(0,\pm\Delta x).
$$

After $n$ independent steps, position is the sum of those displacements. Here $n$ is the number of steps."""
    by_id["11879310"].source = r"""### Brownian motion: the physical phenomenon

<div class="two-panel equal-panels">
<div class="image-panel"><iframe width="100%" height="330" src="https://www.youtube.com/embed/cDcprgWiQEY" title="Brownian motion" frameborder="0" allowfullscreen></iframe></div>
<div class="text-panel"><p>A microscopic particle suspended in a fluid moves irregularly because it is continually struck by surrounding molecules.</p></div>
</div>

A $d$-dimensional Brownian motion $\mathbf B(t)$ has continuous paths and independent Gaussian increments:

$$
\mathbf B(t+\Delta t)-\mathbf B(t)
\sim \mathcal N\!\left(\mathbf 0,\,2D\Delta t\,I_d\right).
$$

In two dimensions,

$$
\mathbb E\!\left[\lVert\mathbf B(t)-\mathbf B(0)\rVert^2\right]=4Dt.
$$"""
    by_id["week03-brownian-ensemble"].source = by_id["week03-brownian-ensemble"].source.replace(
        "# From one random walk to diffusion", "### From one random walk to diffusion"
    )
    by_id["562f3685-c727-4a03-ae6e-7e8ed6aaa9c6"].source = r"""## 2. Diffusion

Reaction creates local concentration differences. Diffusion transports those concentrations through space:

$$
\frac{\partial U}{\partial t}=D_U\nabla^2U,\qquad
\frac{\partial V}{\partial t}=D_V\nabla^2V.
$$

$D_U$ and $D_V$ are diffusion coefficients. If they differ, the two chemical influences act over different spatial ranges."""
    by_id["d1f8631e"].source = r"""## 3. Feed and removal

The reactor is driven rather than closed:

$$
\text{feed of }U:\quad f(1-U),
\qquad
\text{removal of }V:\quad -(f+k)V.
$$

The feed rate $f$ replenishes $U$. The removal rate combines dilution at rate $f$ with conversion or loss at rate $k$. Without these terms, the local reaction would simply exhaust its feedstock."""
    by_id["36fa3ed0"].source = """## Putting it all together

<img src="images/gray_scott_model_map.svg" alt="Reaction, diffusion, feed and removal in the Gray–Scott model" style="display:block;width:82%;margin:0 auto">

The result is a coupled system of nonlinear partial differential equations."""

    parameter = md(
        r"""## Explore the parameter space

The model has four main parameters:

$$
D_U,\qquad D_V,\qquad f,\qquad k.
$$

Sampling $m$ values for every parameter requires $m^4$ combinations. If physically justified diffusion coefficients are fixed, a sweep over the directly controlled feed and removal rates requires only $m^2$ combinations.

This is a small example of the **curse of dimensionality**: the number of combinations grows exponentially with the number of varied parameters. Fixing parameters makes exploration easier, but it also narrows the question and can hide other regimes.""",
        "week03-parameter-space",
    )

    # Rebuild the conceptual ordering around Turing first, Gray–Scott second.
    ids = [c.get("id") for c in nb.cells]
    def insert_after(anchor, new_cells):
        idx = next(i for i, c in enumerate(nb.cells) if c.get("id") == anchor)
        nb.cells[idx + 1:idx + 1] = new_cells

    insert_after("d112f5d4", [six, six_reader, dapple, history])
    insert_after("36fa3ed0", [parameter])

    # Move the Gray–Scott reaction/diffusion/regulation block into one section.
    desired = [
        "week03-gray-scott-history",
        "8858f425-48a5-492b-9a5a-2d277dacc632",
        "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6",
        "b7c839be-6ee3-4fef-9aae-72b880dbb4b9",
        "11879310",
        "week03-brownian-ensemble",
        "d1f8631e",
        "36fa3ed0",
        "week03-parameter-space",
        "54e20377-5977-4ea6-a97b-7482a438a6c9",
        "d67005af-86fe-4102-b7b8-0cf9f629d586",
    ]
    picked = {c.get("id"): c for c in nb.cells if c.get("id") in desired}
    nb.cells = [c for c in nb.cells if c.get("id") not in desired]
    anchor = next(i for i, c in enumerate(nb.cells) if c.get("id") == "week03-turing-dappled")
    nb.cells[anchor + 1:anchor + 1] = [picked[i] for i in desired if i in picked]

    # Make the later numerical part a coherent section hierarchy.
    replacements = {
        "4f8c9362": ("# From model to simulation", "The first model was deliberately incomplete"),
        "2ba9c92e-5488-45b4-a697-7aa99f2bc487": ("## One phenomenon, two descriptions", "# One phenomenon, two descriptions"),
        "1c111a8d-516f-4637-95c0-080efdec3d90": ("### Continuous description · Diffusion field", "# Continuous description · Diffusion field"),
        "4fad79e4-e78d-468c-be71-d70d8c4c711e": ("## Transport, smoothing, and local change", "# Transport, smoothing, and local change"),
        "e501ec03-46e5-44ea-8535-46b96a148671": ("## Return to reaction–diffusion", "# Return to reaction–diffusion"),
        "534e95c9-97e8-4864-b3cc-66d3c2e9e0aa": ("## Discretise space", "# Discretise space"),
        "week03-diffusion-numbers-t012": ("### Diffusion on a grid · exact values", "# Diffusion on a grid · exact values"),
        "week03-diffusion-t012": ("### Reveal the spatial pattern", "# Reveal the spatial pattern"),
        "ecd5c9ba-5acd-42ce-9fba-d6a584a56494": ("### Colour is part of the representation", "# Colour is part of the representation"),
        "09eb9036-81a5-4e05-8806-69d16664865b": ("### Approximate the gradient", "# From a continuous gradient to grid differences"),
        "f2e3c94d-6d0e-4d20-992a-8e23122ce6d0": ("### Approximate the Laplacian", "# From a continuous Laplacian to a grid stencil"),
        "2d86506f-baf9-4f97-9a53-63015dd1e05f": ("### Convolve with the five-point stencil", "# Convolve with the five-point stencil"),
        "0ac1d921-5f1e-4b64-8c65-8454c1e70e8f": ("## Gray–Scott regulation terms", "# Gray–Scott regulation terms"),
        "d3786649-2fd4-4766-8d86-df7cd2839294": ("## Assemble the Gray–Scott update", "# Assemble the Gray–Scott update"),
    }
    for cid, (new, old) in replacements.items():
        c = next((x for x in nb.cells if x.get("id") == cid), None)
        if c:
            c.source = c.source.replace(old, new, 1)

    nbformat.write(nb, WEEK3)


def repair_math_only():
    nb = nbformat.read(WEEK3, 4)
    by_id = {c.get("id"): c for c in nb.cells}
    by_id["8858f425-48a5-492b-9a5a-2d277dacc632"].source = r"""## 1. Reaction

$$U+2V\longrightarrow 3V,\qquad \text{local rate }UV^2.$$

The reaction is autocatalytic: $V$ helps convert $U$ into more $V$. The nonlinear term $UV^2$ makes that local positive feedback explicit.

<div class="analysis-perspectives">
<div><strong><em>U</em></strong><br>feed chemical</div>
<div><strong><em>V</em></strong><br>autocatalytic chemical</div>
</div>"""
    by_id["b7c839be-6ee3-4fef-9aae-72b880dbb4b9"].source = r"""### Random walk: a discrete model

At each step, choose one displacement:

$$
(\pm\Delta x,0),\qquad(0,\pm\Delta x).
$$

After $n$ independent steps, position is the sum of those displacements. Here $n$ is the number of steps."""
    by_id["11879310"].source = r"""### Brownian motion: the physical phenomenon

<div class="two-panel equal-panels">
<div class="image-panel"><iframe width="100%" height="330" src="https://www.youtube.com/embed/cDcprgWiQEY" title="Brownian motion" frameborder="0" allowfullscreen></iframe></div>
<div class="text-panel"><p>A microscopic particle suspended in a fluid moves irregularly because it is continually struck by surrounding molecules.</p></div>
</div>

A $d$-dimensional Brownian motion $\mathbf B(t)$ has continuous paths and independent Gaussian increments:

$$
\mathbf B(t+\Delta t)-\mathbf B(t)
\sim \mathcal N\!\left(\mathbf 0,\,2D\Delta t\,I_d\right).
$$

In two dimensions,

$$
\mathbb E\!\left[\lVert\mathbf B(t)-\mathbf B(0)\rVert^2\right]=4Dt.
$$"""
    by_id["562f3685-c727-4a03-ae6e-7e8ed6aaa9c6"].source = r"""## 2. Diffusion

Reaction creates local concentration differences. Diffusion transports those concentrations through space:

$$
\frac{\partial U}{\partial t}=D_U\nabla^2U,\qquad
\frac{\partial V}{\partial t}=D_V\nabla^2V.
$$

$D_U$ and $D_V$ are diffusion coefficients. If they differ, the two chemical influences act over different spatial ranges."""
    by_id["d1f8631e"].source = r"""## 3. Feed and removal

The reactor is driven rather than closed:

$$
\text{feed of }U:\quad f(1-U),
\qquad
\text{removal of }V:\quad -(f+k)V.
$$

The feed rate $f$ replenishes $U$. The removal rate combines dilution at rate $f$ with conversion or loss at rate $k$. Without these terms, the local reaction would simply exhaust its feedstock."""
    by_id["0ac1d921-5f1e-4b64-8c65-8454c1e70e8f"].source = r"""## Gray–Scott regulation terms

The complete continuous model is

$$
\frac{\partial U}{\partial t}
=D_U\nabla^2U-UV^2+f(1-U),
$$

$$
\frac{\partial V}{\partial t}
=D_V\nabla^2V+UV^2-(f+k)V.
$$

- The feed term $f(1-U)$ replenishes $U$ from the reservoir.
- The reaction term $UV^2$ consumes $U$ and produces $V$ at the same local rate.
- The removal term $(f+k)V$ combines outflow with conversion to inert product.

These terms keep the reactor driven away from equilibrium."""
    by_id["d3786649-2fd4-4766-8d86-df7cd2839294"].source = r"""## Assemble the Gray–Scott update

The continuous model is

$$
\frac{\partial U}{\partial t}=D_U\nabla^2U+f(1-U)-UV^2,
\qquad
\frac{\partial V}{\partial t}=D_V\nabla^2V-(f+k)V+UV^2.
$$

Using an explicit time step and a discrete Laplacian $\Delta_h$ gives

$$
U^{n+1}_{i,j}=U^n_{i,j}
+\Delta t\left[
D_U\Delta_hU^n_{i,j}
+f(1-U^n_{i,j})
-U^n_{i,j}(V^n_{i,j})^2
\right],
$$

$$
V^{n+1}_{i,j}=V^n_{i,j}
+\Delta t\left[
D_V\Delta_hV^n_{i,j}
-(f+k)V^n_{i,j}
+U^n_{i,j}(V^n_{i,j})^2
\right].
$$

The same indexed calculation is repeated at every grid cell and through time."""
    if not any(c.get("id") == "week03-turing-six-evolution" for c in nb.cells):
        result = md(
            """## Return to Turing’s classification

<img src="images/turing_six_mode_evolution.svg" alt="Representative space-time evolution of Turing's six linear modes" style="display:block;width:82%;margin:0 auto">

The six cases predict different ways a small disturbance can first grow: stationary or oscillatory, long-wave, finite-wave, or alternating at the shortest available scale.

These panels show representative linear modes rather than six nonlinear Gray–Scott outcomes. They let us compare a later simulation with Turing’s original classification without pretending that every mode must produce an animal-coat pattern.

<p class="figure-reference">Constructed from the linear mode forms classified in Turing (1952), §6.</p>""",
            "week03-turing-six-evolution",
        )
        anchor = next(i for i, c in enumerate(nb.cells)
                      if c.get("id") == "54e20377-5977-4ea6-a97b-7482a438a6c9")
        nb.cells.insert(anchor + 1, result)
    else:
        evolution = next(c for c in nb.cells if c.get("id") == "week03-turing-six-evolution")
        evolution.source = evolution.source.replace(
            "turing_six_mode_evolution.png", "turing_six_mode_evolution.svg"
        )

    # Keep the presentation concise. Fuller historical, mathematical and
    # interpretive prose remains in the Reader.
    slide_markdown = {
        "d0dd3fdf-7bad-4b0c-b3bb-594128690712",
        "a2fe3243",
        "f129ebdb-49b2-451f-94bf-561270f0ee23",
        "week03-same-mechanism-different-pattern",
        "week03-sand-zebra-first",
        "7347319d-2e0d-49d0-a1c3-ac02ffcd446d",
        "37090ea1-8469-43c1-82a4-15f95adc8616",
        "7530f174-b927-4f48-88af-1a06f5b4cfce",
        "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f",
        "b72f5b93",
        "d112f5d4",
        "week03-turing-six-modes",
        "week03-turing-dappled",
        "week03-gray-scott-history",
        "8858f425-48a5-492b-9a5a-2d277dacc632",
        "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6",
        "b7c839be-6ee3-4fef-9aae-72b880dbb4b9",
        "11879310",
        "week03-brownian-ensemble",
        "d1f8631e",
        "36fa3ed0",
        "week03-parameter-space",
        "54e20377-5977-4ea6-a97b-7482a438a6c9",
        "week03-turing-six-evolution",
        "d67005af-86fe-4102-b7b8-0cf9f629d586",
        "4f8c9362",
        "2ba9c92e-5488-45b4-a697-7aa99f2bc487",
        "1c111a8d-516f-4637-95c0-080efdec3d90",
        "4fad79e4-e78d-468c-be71-d70d8c4c711e",
        "e501ec03-46e5-44ea-8535-46b96a148671",
        "954ca579-6444-4529-9190-05fb00912d11",
        "534e95c9-97e8-4864-b3cc-66d3c2e9e0aa",
        "week03-diffusion-numbers-t012",
        "week03-diffusion-t012",
        "ecd5c9ba-5acd-42ce-9fba-d6a584a56494",
        "09eb9036-81a5-4e05-8806-69d16664865b",
        "f2e3c94d-6d0e-4d20-992a-8e23122ce6d0",
        "2d86506f-baf9-4f97-9a53-63015dd1e05f",
        "0ac1d921-5f1e-4b64-8c65-8454c1e70e8f",
        "d3786649-2fd4-4766-8d86-df7cd2839294",
        "week03-gray-scott-world",
    }
    for cell in nb.cells:
        tags = list(cell.metadata.get("tags", []))
        if cell.cell_type == "code":
            if "hide-input" not in tags:
                tags.append("hide-input")
        elif (
            cell.get("id") not in slide_markdown
            and cell.metadata.get("slideshow", {}).get("slide_type") not in {"notes", "skip"}
            and "reader-only" not in tags
        ):
            tags.append("reader-only")
        cell.metadata["tags"] = tags

    # Correct a heading that had inherited an extra Markdown marker.
    model_cell = by_id.get("4f8c9362")
    if model_cell:
        model_cell.source = model_cell.source.replace(
            "# # From model to simulation", "# From model to simulation", 1
        )

    # Remove older duplicated notes that used A/B/C notation after the model
    # had already been defined consistently with U and V.
    obsolete = {
        "955ed279-4fd0-434a-8214-8f51674944ad",
        "31396dc7-148c-4e4d-87bc-2fe57c419337",
        "8087aba4-678b-497f-b40f-e3a4e7ae97d8",
        "3e0aa253-5a6e-4aaf-b3f6-a0613616754c",
        "14e1f12c-4b25-4022-a18b-4cb65eb241b2",
        "b7316f12-8222-4996-bb7e-cfc5657c8f7c",
        "7dbdca5d-8d47-493d-af36-380745a52096",
        "c3353092-7813-44be-b2bc-0be8fa70f119",
        "74c4f181-0028-44ad-ab94-e5de5587583e",
        "07347780-7f53-4ad3-b2e7-ec5d9a6ed5be",
        "90e2f456-84d7-4aea-8f57-d685ba3a26c2",
        "f600b07c-c126-4219-aa01-a6e7901e1452",
        "baec3197-5ef7-46d5-ba13-3aa181bf545f",
        "393a9c21-b045-4cd0-a619-bcc53ab52f29",
        "0d44156b-aabe-499b-8b5d-9e8e4c369775",
        "dff366ba-ebcb-448c-adef-37121903789c",
    }
    nb.cells = [cell for cell in nb.cells if cell.get("id") not in obsolete]
    nbformat.write(nb, WEEK3)


if __name__ == "__main__":
    IMAGES.mkdir(exist_ok=True)
    week2_marker()
    assets()
    current = nbformat.read(WEEK3, 4)
    if any(c.get("id") == "week03-turing-six-modes" for c in current.cells):
        repair_math_only()
    else:
        week3_revise()
