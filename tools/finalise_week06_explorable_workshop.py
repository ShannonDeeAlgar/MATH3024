"""Finish the Week 6 explorable hierarchy and add a flashing-clock workshop view."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def lines(text):
    return text.splitlines(keepends=True)


def md(text, cid, tags, slide_type="skip"):
    return {
        "cell_type": "markdown",
        "id": cid,
        "metadata": {"tags": tags, "slideshow": {"slide_type": slide_type}},
        "source": lines(text.rstrip() + "\n"),
    }


def load(path):
    return json.loads(path.read_text())


def save(path, nb):
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")


lecture = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
nb = load(lecture)
cells = nb["cells"]

def at(cid):
    return next(i for i, c in enumerate(cells) if c.get("id") == cid)

# Slides: a genuine section banner followed by the full-page explorable.
explore = cells.pop(at("w6-kuramoto-explorable"))
explore["source"] = lines("## Explore the Kuramoto model\n\n" + "".join(explore["source"]).split("\n", 1)[1])
model_i = at("w6-model-details-slide")
cells.insert(model_i, md("# Explorable", "w6-explorable-banner-slide", ["slides-only"], "slide"))
cells.insert(model_i + 1, explore)

# Reader: place the explorable between the motivating examples and model detail.
explore = cells.pop(at("kuramoto-video-reader"))
explore["source"] = lines("## Explore the Kuramoto model\n\n" + "".join(explore["source"]).split("\n", 1)[1])
model_i = at("w6-e00ea3001e")
cells.insert(model_i, md("# Explorable", "w6-explorable-banner-reader", ["reader-only"], "skip"))
cells.insert(model_i + 1, explore)

# Several forms of synchronisation is analysis, not model specification.
types_text = cells.pop(at("w6-types-of-synchronisation-reader"))
types_image = cells.pop(at("sync-types-reader"))
types_text["source"] = lines("### Several forms of synchronisation\n\n" + "".join(types_text["source"]).split("\n", 1)[1])
qual_i = at("kuramoto-video")
cells.insert(qual_i + 1, types_text)
cells.insert(qual_i + 2, types_image)

# The slides use the same analysis placement.
types_slide = cells.pop(at("sync-types-slide"))
types_slide["source"] = lines("## Several forms of synchronisation\n\n" + "".join(types_slide["source"]).split("\n", 1)[1])
qual_i = at("w6-watch")
cells.insert(qual_i + 1, types_slide)

# Model questions precede the canonical answer on the slides.
spec = cells.pop(at("w6-specify"))
cells.insert(at("w6-kuramoto"), spec)

save(lecture, nb)


workshop = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"
nb = load(workshop)
cells = nb["cells"]

if not any(c.get("id") == "adaptive-network-flash-player" for c in cells):
    insert_i = next(i for i, c in enumerate(cells) if c.get("id") == "adaptive-network-analysis")
    intro = md(
        """## Show the clocks rather than the phase value

The coloured version makes phase easy to inspect, but fireflies do not display a continuous colour wheel. In the version below every node is grey except for a short flash as its phase passes 12 o'clock. The edges and oscillator dynamics are unchanged.

This representation hides most of the internal state. That is useful: it is closer to the observation that motivated the model and makes it harder to mistake phase-space motion for physical movement.""",
        "adaptive-network-flash-intro", [], "skip"
    )
    code = {
        "cell_type": "code",
        "execution_count": None,
        "id": "adaptive-network-flash-player",
        "metadata": {},
        "outputs": [],
        "source": lines(r'''def flashing_network_player(phase_frames, edge_frames, element_id="flashing-network-player"):
    phases_json = json.dumps(np.round(phase_frames, 4).tolist())
    edges_json = json.dumps(edge_frames)
    return HTML(f"""
    <div id="{element_id}" style="font-family:Arial,sans-serif;color:#1B2A4C;max-width:620px;margin:0 auto">
      <canvas width="620" height="350" style="width:100%;max-height:350px;border:1px solid #C7CEDC"></canvas>
      <div style="display:flex;gap:8px;align-items:center;margin-top:6px">
        <button type="button">Play</button><input type="range" min="0" max="{len(phase_frames)-1}" value="0" style="flex:1;accent-color:#1B2A4C"><span></span>
      </div>
    </div>
    <script>(()=>{{
      const root=document.getElementById('{element_id}'), canvas=root.querySelector('canvas'), ctx=canvas.getContext('2d');
      const phases={phases_json}, edges={edges_json}, slider=root.querySelector('input'), button=root.querySelector('button'), label=root.querySelector('span');
      const n=phases[0].length, cx=310, cy=175, R=135; let timer=null;
      const xy=Array.from({{length:n}},(_,i)=>[cx+R*Math.cos(2*Math.PI*i/n),cy-R*Math.sin(2*Math.PI*i/n)]);
      function draw(k){{
        ctx.clearRect(0,0,620,350);ctx.fillStyle='#fff';ctx.fillRect(0,0,620,350);
        ctx.strokeStyle='rgba(88,121,170,.22)';ctx.lineWidth=1;
        edges[k].forEach(e=>{{ctx.beginPath();ctx.moveTo(...xy[e[0]]);ctx.lineTo(...xy[e[1]]);ctx.stroke();}});
        phases[k].forEach((a,i)=>{{
          const gap=Math.abs(Math.atan2(Math.sin(a-Math.PI/2),Math.cos(a-Math.PI/2)));
          ctx.fillStyle=gap<0.18?'#F4C84A':'#B9C0CB';ctx.strokeStyle='#1B2A4C';ctx.lineWidth=.8;
          ctx.beginPath();ctx.arc(xy[i][0],xy[i][1],gap<0.18?7:4.8,0,2*Math.PI);ctx.fill();ctx.stroke();
        }});label.textContent=`frame ${{k}}`;
      }}
      function stop(){{clearInterval(timer);timer=null;button.textContent='Play';}}
      button.onclick=()=>{{if(timer){{stop();return;}}button.textContent='Pause';timer=setInterval(()=>{{let k=+slider.value;if(k>=phases.length-1){{stop();return;}}slider.value=k+1;draw(k+1);}},130);}};
      slider.oninput=()=>draw(+slider.value);draw(0);
    }})();</script>""")


display(flashing_network_player(adaptive_phases, adaptive_edges))
''')
    }
    cells[insert_i:insert_i] = [intro, code]

save(workshop, nb)
