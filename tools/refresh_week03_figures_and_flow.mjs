import fs from "node:fs/promises";
import path from "node:path";

const ROOT = "/Users/sam/Desktop/TEACHING/MATH3024/JL_Reader/my-complex-systems-book";
const NOTEBOOK = path.join(ROOT, "notebooks/week03/L_Reaction_diffusion.ipynb");
const IMAGE_DIR = path.join(ROOT, "notebooks/week03/images");

const navy = "#1b2a4c";
const blue = "#5f80b2";
const gold = "#f1d255";
const pale = "#f5f7fb";
const line = "#c9d3e3";

const sourceText = cell =>
  Array.isArray(cell.source) ? cell.source.join("") : (cell.source || "");

const setSource = (cell, source) => {
  cell.source = source.split(/(?<=\n)/);
};

const slideMeta = type => ({ slideshow: { slide_type: type } });

function markdownCell(id, source, type = "slide", tags = []) {
  return {
    cell_type: "markdown",
    id,
    metadata: { ...slideMeta(type), tags },
    source: source.split(/(?<=\n)/),
  };
}

function findCell(nb, id) {
  const cell = nb.cells.find(c => c.id === id);
  if (!cell) throw new Error(`Missing notebook cell ${id}`);
  return cell;
}

function insertBefore(nb, anchorId, cells) {
  const oldIds = new Set(cells.map(c => c.id));
  nb.cells = nb.cells.filter(c => !oldIds.has(c.id));
  const index = nb.cells.findIndex(c => c.id === anchorId);
  if (index < 0) throw new Error(`Missing insertion anchor ${anchorId}`);
  nb.cells.splice(index, 0, ...cells);
}

function makeDiffusionSvg(showNumbers = false) {
  const n = 7;
  let field = Array.from({ length: n }, () => Array(n).fill(0));
  field[3][3] = 1;
  const frames = [field];
  const step = a => Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => {
      const up = a[(i - 1 + n) % n][j];
      const down = a[(i + 1) % n][j];
      const left = a[i][(j - 1 + n) % n];
      const right = a[i][(j + 1) % n];
      return 0.5 * a[i][j] + 0.125 * (up + down + left + right);
    })
  );
  field = step(field); frames.push(field);
  field = step(field); frames.push(field);

  const W = 1100, H = 360, cell = 38, gap = 70;
  const panelW = n * cell;
  const startX = (W - (3 * panelW + 2 * gap)) / 2;
  const y0 = 58;
  const colour = v => {
    const t = Math.max(0, Math.min(1, v));
    const a = [245, 247, 251], b = [27, 42, 76];
    return `rgb(${a.map((x, k) => Math.round(x + t * (b[k] - x))).join(",")})`;
  };
  let body = "";
  frames.forEach((a, k) => {
    const x0 = startX + k * (panelW + gap);
    body += `<text x="${x0 + panelW / 2}" y="34" text-anchor="middle" class="title">t = ${k}</text>`;
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const value = a[i][j];
      body += `<rect x="${x0 + j * cell}" y="${y0 + i * cell}" width="${cell}" height="${cell}" fill="${showNumbers ? "white" : colour(value)}" stroke="${line}" stroke-width="1.3"/>`;
      if (showNumbers) body += `<text x="${x0 + (j + .5) * cell}" y="${y0 + (i + .63) * cell}" text-anchor="middle" class="number">${value.toFixed(3).replace(/^0/, "")}</text>`;
    }
  });
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<style>.title{font:600 24px Arial,sans-serif;fill:${navy}}.label{font:18px Arial,sans-serif;fill:${navy}}.number{font:12px Arial,sans-serif;fill:${navy}}</style>
<rect width="100%" height="100%" fill="white"/>
${body}
<text x="${W / 2}" y="348" text-anchor="middle" class="label">The same material is redistributed locally; total concentration remains 1.</text>
</svg>`;
}

function rng(seed = 3024) {
  let x = seed >>> 0;
  return () => {
    x = (1664525 * x + 1013904223) >>> 0;
    return x / 4294967296;
  };
}

function normal(random) {
  const u = Math.max(random(), 1e-12), v = random();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

function makeBrownianSvg() {
  const random = rng();
  const steps = 260, walkers = 700, D = 0.25, dt = 1;
  const sample = [[0, 0]];
  const msd = Array(steps + 1).fill(0);
  for (let w = 0; w < walkers; w++) {
    let x = 0, y = 0;
    for (let t = 1; t <= steps; t++) {
      x += Math.sqrt(2 * D * dt) * normal(random);
      y += Math.sqrt(2 * D * dt) * normal(random);
      msd[t] += x * x + y * y;
      if (w === 0) sample.push([x, y]);
    }
  }
  for (let t = 0; t <= steps; t++) msd[t] /= walkers;
  const W = 1100, H = 410;
  const left = { x: 70, y: 65, w: 430, h: 280 };
  const right = { x: 620, y: 65, w: 410, h: 280 };
  const xs = sample.map(p => p[0]), ys = sample.map(p => p[1]);
  const xmin = Math.min(...xs), xmax = Math.max(...xs), ymin = Math.min(...ys), ymax = Math.max(...ys);
  const sx = x => left.x + (x - xmin) / (xmax - xmin || 1) * left.w;
  const sy = y => left.y + left.h - (y - ymin) / (ymax - ymin || 1) * left.h;
  const tx = t => right.x + t / steps * right.w;
  const maxY = 4 * D * steps * 1.08;
  const ty = y => right.y + right.h - y / maxY * right.h;
  const pathData = sample.map((p, i) => `${i ? "L" : "M"}${sx(p[0]).toFixed(1)},${sy(p[1]).toFixed(1)}`).join(" ");
  const msdData = msd.map((y, t) => `${t ? "L" : "M"}${tx(t).toFixed(1)},${ty(y).toFixed(1)}`).join(" ");
  const theoryData = `M${tx(0)},${ty(0)} L${tx(steps)},${ty(4 * D * steps)}`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<style>.title{font:600 24px Arial,sans-serif;fill:${navy}}.axis{stroke:${navy};stroke-width:2}.label{font:18px Arial,sans-serif;fill:${navy}}.small{font:16px Arial,sans-serif;fill:${navy}}</style>
<rect width="100%" height="100%" fill="white"/>
<text x="${left.x + left.w / 2}" y="32" text-anchor="middle" class="title">One possible trajectory</text>
<line x1="${left.x}" y1="${left.y + left.h}" x2="${left.x + left.w}" y2="${left.y + left.h}" class="axis"/>
<line x1="${left.x}" y1="${left.y}" x2="${left.x}" y2="${left.y + left.h}" class="axis"/>
<path d="${pathData}" fill="none" stroke="${blue}" stroke-width="3"/>
<circle cx="${sx(0)}" cy="${sy(0)}" r="6" fill="${gold}" stroke="${navy}" stroke-width="2"/>
<circle cx="${sx(xs.at(-1))}" cy="${sy(ys.at(-1))}" r="6" fill="${navy}"/>
<text x="${left.x + left.w / 2}" y="392" text-anchor="middle" class="label">x position</text>
<text x="22" y="${left.y + left.h / 2}" text-anchor="middle" transform="rotate(-90 22 ${left.y + left.h / 2})" class="label">y position</text>
<text x="${right.x + right.w / 2}" y="32" text-anchor="middle" class="title">Many walks recover the diffusion law</text>
<line x1="${right.x}" y1="${right.y + right.h}" x2="${right.x + right.w}" y2="${right.y + right.h}" class="axis"/>
<line x1="${right.x}" y1="${right.y}" x2="${right.x}" y2="${right.y + right.h}" class="axis"/>
<path d="${theoryData}" fill="none" stroke="${gold}" stroke-width="7"/>
<path d="${msdData}" fill="none" stroke="${navy}" stroke-width="3"/>
<text x="${right.x + right.w / 2}" y="392" text-anchor="middle" class="label">Simulation time step</text>
<text x="568" y="${right.y + right.h / 2}" text-anchor="middle" transform="rotate(-90 568 ${right.y + right.h / 2})" class="label">Mean squared displacement</text>
<line x1="790" y1="85" x2="830" y2="85" stroke="${navy}" stroke-width="3"/><text x="840" y="91" class="small">ensemble</text>
<line x1="790" y1="112" x2="830" y2="112" stroke="${gold}" stroke-width="7"/><text x="840" y="118" class="small">4Dt</text>
</svg>`;
}

const nb = JSON.parse(await fs.readFile(NOTEBOOK, "utf8"));

// Remove the route slide requested for deletion.
nb.cells = nb.cells.filter(c => c.id !== "week03-route");

// No reveal fragments: material now appears with its slide.
for (const cell of nb.cells) {
  if (cell.metadata?.slideshow?.slide_type === "fragment") {
    cell.metadata.slideshow.slide_type = "";
  }
  if (cell.cell_type === "markdown") {
    setSource(cell, sourceText(cell).replaceAll("choice-marker fragment", "choice-marker"));
  }
}

setSource(findCell(nb, "9253675a-2529-494e-b524-48a841f31a6d"), `# Pattern formation

And it is not just a cheetah's spots. Patterns appear all around us, including in systems that seem to share nothing in common.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt=""><span>What regularity do you notice, and what would count as evidence that it is more than coincidence?</span></div>`);

const oldSand = findCell(nb, "19b18f71-7c97-4558-b5d5-9b7b5ec19b55");
oldSand.metadata.tags = [...new Set([...(oldSand.metadata.tags || []), "archive-only"])];
oldSand.metadata.slideshow = { slide_type: "" };
for (const id of ["aa5c1c67-775b-4c33-a738-d67e5ff040b1", "ab306a33-821c-4d0f-a6e1-f145d0688da8"]) {
  const cell = findCell(nb, id);
  cell.metadata.tags = [...new Set([...(cell.metadata.tags || []), "archive-only"])];
  cell.metadata.slideshow = { slide_type: "" };
}

setSource(findCell(nb, "ec366d2b"), `## What exactly is a pattern?

A pattern is a reproducible regularity in space, time, or state. Describing one is not yet explaining how it formed.

Useful questions are: what repeats, at what scale, how stable is it, and which measurements would distinguish one proposed mechanism from another?`);

// Retire the hand-drawn grid sequence now that the same steps are generated
// reproducibly below.
for (const id of [
  "3bb95a1f-c611-4d3c-81c0-2979c25b5203",
  "740494a5-6c65-4522-94ff-c47ef77b43fb",
]) {
  const cell = findCell(nb, id);
  cell.metadata.tags = [...new Set([...(cell.metadata.tags || []), "archive-only"])];
  cell.metadata.slideshow = { slide_type: "" };
}

insertBefore(nb, "a5a1b98b-07e0-4417-be77-e1090bcfd254", [
  markdownCell("week03-same-mechanism-different-pattern", `# Similar mechanisms, different patterns

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Cheetah_vs_leopard_vs_jaguar.jpg" alt="Different mammalian coat patterns" style="width:100%;"></div>
<div class="text-panel">
<p><strong>One reaction–diffusion family can select spots, stripes, labyrinths, or nearly uniform states.</strong></p>
<p>Parameters, geometry, growth, and initial perturbations change which mode survives.</p>
<p>That makes reaction–diffusion a plausible explanation for the cheetah hook, not proof that it is the biological mechanism.</p>
</div>
</div>`, "subslide"),
  markdownCell("week03-sand-zebra-first", `# Similar patterns, different mechanisms

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Sand_and_zebra_stripes.png" alt="Wind ripples in sand beside zebra stripes" style="width:100%;"></div>
<div class="text-panel">
<p><strong>The resemblance is real. The mechanism need not be shared.</strong></p>
<p>Wind transports grains across sand. Developing tissue coordinates cells and chemical signals.</p>
<p>Similar morphology is a clue that suggests measurements. It does not identify a cause.</p>
</div>
</div>`, "subslide"),
  markdownCell("week03-many-pattern-mechanisms", `# Similar patterns, different mechanisms

<div class="analysis-perspectives four">
<div><strong>Reaction and diffusion</strong><br>Local activation and inhibition can create spots, stripes and labyrinths.</div>
<div><strong>Transport and flow</strong><br>Wind ripples and convection organise material through motion.</div>
<div><strong>Mechanical instability</strong><br>Buckling, wrinkling and differential growth create folds.</div>
<div><strong>Growth and competition</strong><br>Moving fronts, cell sorting and aggregation build domains and branches.</div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt=""><span>Similar morphology is a clue, not proof of a shared mechanism. What observation would distinguish these explanations?</span></div>`, "subslide"),
]);
const howPatterns = findCell(nb, "a5a1b98b-07e0-4417-be77-e1090bcfd254");
howPatterns.metadata.tags = [...new Set([...(howPatterns.metadata.tags || []), "archive-only"])];
howPatterns.metadata.slideshow = { slide_type: "" };

setSource(findCell(nb, "37090ea1-8469-43c1-82a4-15f95adc8616"), `# The same instability in tissue and gel

<div class="two-panel equal-panels">
<div class="text-panel">
<p><strong>Brain cortex</strong></p>
<p>The outer layer grows faster than the tissue beneath it. Compression can buckle a smooth surface into folds.</p>
</div>
<div class="image-panel">
<img src="images/brain_folding_gel.gif" alt="A physical gel model developing brain-like folds" style="width:100%;">
<p><strong>Swelling gel model</strong></p>
<p>A synthetic layered gel reproduces similar folds through differential swelling.</p>
</div>
</div>

<p class="figure-reference">Physical gel models make the mechanical hypothesis testable. See Tallinen et al. (2016) and the open-access review by Greiner, Kaessmair & Budday (2021).</p>`);

setSource(findCell(nb, "7530f174-b927-4f48-88af-1a06f5b4cfce"), `# Travelling waves organise living cells

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/dictyostelium_aggregation_waves.png" alt="Chemical waves and aggregation streams in Dictyostelium" style="width:100%;"></div>
<div class="text-panel">
<p><strong>Starving amoebae relay pulses of cAMP.</strong></p>
<p>Target and spiral waves travel through the colony. Cells move up the signal gradient and collect into streams.</p>
<p>This combines an excitable chemical wave with directed cell motion. It is a biological counterpart to laboratory wave patterns, not simply another BZ reaction.</p>
</div>
</div>

<p class="figure-reference">Durston et al.; image sequence adapted from the open-access analysis in *Scientific Reports* 9, 2019.</p>`);
for (const id of ["d595aea9-d487-42a3-a0e8-df8978faf96a", "3bbaffca-5bec-4d52-afc1-caae472deca7", "04b87a77-5a04-4ace-bbe4-5d4d2fe2a7c1"]) {
  const cell = findCell(nb, id); cell.metadata.tags = [...new Set([...(cell.metadata.tags || []), "archive-only"])]; cell.metadata.slideshow = { slide_type: "" };
}

// Put Turing's paper before the mechanism claim, and distinguish a decisive
// mathematical contribution from the much older question of morphogenesis.
const turingIds = ["a0a1efe7-e26e-4f6d-a529-3db70b3fe94f", "26286a64", "b72f5b93", "3eb4d29c-82d2-467c-99b2-70ff7945b37d"];
const turingCells = nb.cells.filter(c => turingIds.includes(c.id));
nb.cells = nb.cells.filter(c => !turingIds.includes(c.id));
insertBefore(nb, "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6", turingCells);
setSource(findCell(nb, "b72f5b93"), `## Turing's 1952 proposal

The question of how biological form develops was much older. D'Arcy Thompson and others had already sought mathematical and physical explanations of growth.

Turing's decisive step was to show mathematically that reacting and diffusing morphogens can make a uniform state unstable. Small perturbations can then grow into organised spatial structure.

<p class="figure-reference">A. M. Turing, “The Chemical Basis of Morphogenesis”, <em>Philosophical Transactions of the Royal Society B</em> 237 (1952), 37–72.</p>`);
setSource(findCell(nb, "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6"), `# Diffusion can create instability

Reaction–diffusion systems can generate spots, stripes, and waves without a pre-drawn template.

Turing's proposal was surprising because diffusion usually smooths differences. Coupled to the right local reactions, unequal diffusion rates can instead amplify selected perturbations.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt=""><span>What must the reactions do locally if diffusion is not to erase every difference?</span></div>`);

setSource(findCell(nb, "8858f425-48a5-492b-9a5a-2d277dacc632"), `# Build the Gray–Scott model · 1. Reaction

We now turn Turing's general mechanism into this week's canonical reaction–diffusion model.

The Gray–Scott reactions transform two concentrations, \(u\) and \(v\), locally. At this stage nothing moves between grid cells.`);
setSource(findCell(nb, "c5c3ba5e"), `# Build the Gray–Scott model · 2. Diffusion

Diffusion transports each concentration down its own spatial gradient. The two diffusion coefficients need not be equal.`);
setSource(findCell(nb, "d1f8631e"), `# Build the Gray–Scott model · 3. Regulation

Feed and kill terms keep the system away from chemical equilibrium and select which patterns can persist.`);

// Replace the old, non-conservative grid demo with code that is suitable for students.
const diffusionCode = findCell(nb, "8144df44-2247-4e76-9a97-88e785929c07");
diffusionCode.metadata.tags = [...new Set([...(diffusionCode.metadata.tags || []), "reader-only"])];
diffusionCode.metadata.slideshow = { slide_type: "" };
diffusionCode.execution_count = null;
diffusionCode.outputs = [];
setSource(diffusionCode, `import numpy as np
import matplotlib.pyplot as plt

SLIDE_STYLE = {
    "font.size": 15,
    "axes.titlesize": 19,
    "axes.labelsize": 16,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
}
plt.rcParams.update(SLIDE_STYLE)

def diffuse_periodic(field, mixing_fraction=0.5):
    """Perform one mass-conserving diffusion step on a periodic square grid."""
    if not 0 <= mixing_fraction <= 1:
        raise ValueError("mixing_fraction must lie between 0 and 1")
    neighbour_mean = (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
    ) / 4
    return (1 - mixing_fraction) * field + mixing_fraction * neighbour_mean

field = np.zeros((7, 7), dtype=float)
field[3, 3] = 1.0
snapshots = [field.copy()]
for _ in range(2):
    field = diffuse_periodic(field)
    snapshots.append(field.copy())

assert all(np.isclose(frame.sum(), 1.0) for frame in snapshots)

fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.3), constrained_layout=True)
for time, (ax, frame) in enumerate(zip(axes, snapshots)):
    ax.imshow(np.ones_like(frame), cmap="Greys", vmin=0, vmax=1)
    for (row, col), value in np.ndenumerate(frame):
        ax.text(col, row, f"{value:.3f}", ha="center", va="center", fontsize=9)
    ax.set_title(f"$t={time}$: exact values")
    ax.set_xticks([]); ax.set_yticks([])
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.3), constrained_layout=True)
for time, (ax, frame) in enumerate(zip(axes, snapshots)):
    image = ax.imshow(frame, cmap="Blues", vmin=0, vmax=1, interpolation="nearest")
    ax.set_title(f"$t={time}$")
    ax.set_xticks(np.arange(-0.5, 7, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 7, 1), minor=True)
    ax.grid(which="minor", color="#c9d3e3", linewidth=0.8)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
fig.colorbar(image, ax=axes, label="Concentration", shrink=0.82)
plt.show()
`);

insertBefore(nb, "8144df44-2247-4e76-9a97-88e785929c07", [
  markdownCell("week03-diffusion-numbers-t012", `# Diffusion on a grid · exact values

<img src="images/diffusion_grid_numbers_t012.svg" alt="The numerical concentration in every grid cell at times zero, one and two" style="display:block;width:94%;margin:0 auto;">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt=""><span>The values are precise. Can you see the spatial pattern quickly?</span></div>`, "subslide", ["slides-only"]),
  markdownCell("week03-diffusion-t012", `# Diffusion on a grid · replace numbers with colour

<img src="images/diffusion_grid_t012.svg" alt="Code-generated concentration grids at times zero, one and two" style="display:block;width:92%;margin:0 auto;">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Down the ladder:</strong> colour sacrifices exact values but makes local redistribution visible. A useful visualisation depends on the question.</span></div>`, "subslide", ["slides-only"]),
]);

// Replace misleading single-trajectory comparisons with a reproducible ensemble test.
const walkCode = findCell(nb, "17066138-6d3a-4b3a-bde7-a0eff02be124");
walkCode.metadata.tags = [...new Set([...(walkCode.metadata.tags || []), "reader-only"])];
walkCode.metadata.slideshow = { slide_type: "" };
walkCode.execution_count = null;
walkCode.outputs = [];
setSource(walkCode, `import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(3024)
n_walkers, n_steps = 2000, 500
D, dt = 0.25, 1.0

increments = rng.normal(
    loc=0.0,
    scale=np.sqrt(2 * D * dt),
    size=(n_walkers, n_steps, 2),
)
positions = np.concatenate(
    [np.zeros((n_walkers, 1, 2)), np.cumsum(increments, axis=1)],
    axis=1,
)
mean_squared_displacement = np.mean(np.sum(positions**2, axis=2), axis=0)
time = np.arange(n_steps + 1) * dt

fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), constrained_layout=True)
axes[0].plot(*positions[0].T, color="#5f80b2", linewidth=1.6)
axes[0].scatter(*positions[0, 0], color="#f1d255", edgecolor="#1b2a4c", s=65, zorder=3)
axes[0].set(title="One possible trajectory", xlabel="$x$", ylabel="$y$", aspect="equal")

axes[1].plot(time, mean_squared_displacement, color="#1b2a4c", linewidth=2.5, label="ensemble")
axes[1].plot(time, 4 * D * time, color="#f1d255", linewidth=4, label="$4Dt$")
axes[1].set(
    title="Many walks recover the diffusion law",
    xlabel="Simulation time step",
    ylabel="Mean squared displacement",
)
axes[1].legend(frameon=False)
plt.show()
`);

const oldDistance = findCell(nb, "268dc768-98b9-496a-b555-9980cb86844d");
oldDistance.metadata.tags = [...new Set([...(oldDistance.metadata.tags || []), "archive-only"])];
oldDistance.metadata.slideshow = { slide_type: "" };

insertBefore(nb, "17066138-6d3a-4b3a-bde7-a0eff02be124", [
  markdownCell("week03-brownian-ensemble", `# From one random walk to diffusion

<img src="images/brownian_ensemble_msd.svg" alt="One Brownian trajectory and an ensemble mean-square-displacement comparison with four D t" style="display:block;width:94%;margin:0 auto;">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder:</strong> average over many possible trajectories. The macroscopic law is visible in the ensemble, not in every individual path.</span></div>`, "subslide", ["slides-only"]),
]);

// Keep the two-rate comparison as Reader enrichment, but remove its old staged slide.
const rateCode = findCell(nb, "b5d00706-c39f-46f7-81a4-13163ae17b2c");
rateCode.metadata.tags = [...new Set([...(rateCode.metadata.tags || []), "reader-only"])];
rateCode.metadata.slideshow = { slide_type: "" };
rateCode.execution_count = null;
rateCode.outputs = [];
setSource(rateCode, `import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(3024)
n_walkers, n_steps = 1500, 400
time = np.arange(n_steps + 1)
diffusion_rates = {"slower": 0.10, "faster": 0.45}

fig, ax = plt.subplots(figsize=(7.8, 4.6), constrained_layout=True)
for label, D in diffusion_rates.items():
    increments = rng.normal(
        scale=np.sqrt(2 * D),
        size=(n_walkers, n_steps, 2),
    )
    positions = np.concatenate(
        [np.zeros((n_walkers, 1, 2)), np.cumsum(increments, axis=1)],
        axis=1,
    )
    msd = np.mean(np.sum(positions**2, axis=2), axis=0)
    ax.plot(time, msd, linewidth=2.5, label=f"{label}: $D={D}$")
    ax.plot(time, 4 * D * time, linewidth=1.5, linestyle="--", alpha=0.75)

ax.set(
    xlabel="Simulation time step",
    ylabel="Mean squared displacement",
    title="Diffusion rate changes the ensemble spreading rate",
)
ax.legend(frameon=False)
plt.show()
`);

// Two legacy implementations repeated the same finite-difference calculation
// and used different boundary behaviour. The tested implementation above is
// now the single source of truth.
for (const id of [
  "2ed906af-cf26-424b-9c08-752ab6f99e41",
  "185a81bb-3356-4da3-97b0-b2e8b7857530",
]) {
  const cell = findCell(nb, id);
  cell.metadata.tags = [...new Set([...(cell.metadata.tags || []), "archive-only"])];
  cell.metadata.slideshow = { slide_type: "" };
}

// The former post-conclusion comparison belongs in the Reader, not after the ending.
for (const id of [
  "07347780-7f53-4ad3-b2e7-ec5d9a6ed5be",
  "90e2f456-84d7-4aea-8f57-d685ba3a26c2",
]) {
  const cell = findCell(nb, id);
  cell.metadata.tags = [...new Set([...(cell.metadata.tags || []), "reader-only"])];
  cell.metadata.slideshow = { slide_type: "" };
}

insertBefore(nb, "a45a0945-5b93-4ba3-9345-168dd54d526c", [
  markdownCell("week03-gray-scott-world", `# Gray–Scott-like patterns in the world

<div class="analysis-perspectives three">
<div><img src="images/Zebrafish.jpg" alt="Zebrafish pigment pattern"><strong>Pigment patterns</strong><br>Reaction–diffusion is a useful hypothesis, but experiments show that cell movement and contact also matter.</div>
<div><img src="images/Hydra-Foto.jpg" alt="Hydra"><strong>Developmental organisation</strong><br>Activator–inhibitor feedback can organise repeated biological features.</div>
<div><img src="images/Garlic_intersection.jpeg" alt="Cellular pattern in a garlic cross-section"><strong>Cellular domains</strong><br>Similar spots and labyrinths can also arise through growth, packing or mechanical constraints.</div>
</div>

<p class="figure-reference">Examples of reaction–diffusion evidence include Kondo & Asai (1995), Economou et al. (2012), and Nakamasu et al. (2009). These are <em>Turing-type</em> comparisons, not claims that nature literally implements the Gray–Scott equations.</p>`, "subslide"),
  markdownCell("week03-gray-scott-citations", `### Evidence, mechanism and morphology

- Kondo, S. and Asai, R. (1995), [A reaction–diffusion wave on the skin of the marine angelfish](https://www.nature.com/articles/376765a0), *Nature*.
- Economou, A. D. et al. (2012), [Periodic stripe formation by a Turing mechanism operating at growth zones in the mammalian palate](https://www.nature.com/articles/ng.1090), *Nature Genetics*.
- Nakamasu, A. et al. (2009), an agent-based account of zebrafish pigment-cell interactions, with later experimental refinement by Volkening & Sandstede (2018).

The responsible mechanism must be tested. Similar morphology alone does not identify it.`, "", ["reader-only"]),
  markdownCell("week03-pattern-family", `# Reaction–diffusion is one route to pattern

<div class="two-panel equal-panels">
<div class="text-panel">
<p><strong>Other pattern-generating families</strong></p>
<ul>
<li>phase separation and coarsening</li>
<li>convection and other flow instabilities</li>
<li>mechanical buckling and differential growth</li>
<li>excitable and oscillatory waves</li>
<li>aggregation, branching and moving fronts</li>
<li>cell sorting, migration and external templates</li>
</ul>
</div>
<div class="text-panel">
<p><strong>Fit for purpose means discriminating among them.</strong></p>
<p>Ask which variables move, what is conserved, what sets the wavelength, whether the pattern travels, and how it responds to perturbation.</p>
<div class="choice-marker"><img src="images/choice_marker.svg" alt=""><span>Choosing a mechanism is a modelling decision supported by evidence.</span></div>
</div>
</div>`, "subslide"),
]);

setSource(findCell(nb, "a45a0945-5b93-4ba3-9345-168dd54d526c"), `# Simulate, inspect, then generalise

The aim is not to predict the exact location of every stripe. It is to understand which behaviours the mechanism can produce and which observations would challenge it.

<div class="analysis-perspectives three">
<div><strong>Inspect locally</strong><br>Check diffusion, reaction and boundary updates separately.</div>
<div><strong>Explore parameters</strong><br>Vary feed, kill and diffusion rates systematically.</div>
<div><strong>Compare evidence</strong><br>Measure wavelength, stability, motion and response to perturbation.</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Move deliberately:</strong> down to debug a mechanism; up to identify robust pattern classes.</span></div>`);

setSource(findCell(nb, "d5cb018d-702d-462f-b281-49a412e736f5"), `# Take it with you

<div class="analysis-perspectives">
<div><strong>Microscopic and macroscopic descriptions can both be useful.</strong><br>A random walk and a diffusion equation answer different questions about the same transport process.</div>
<div><strong>Pattern is evidence, not explanation.</strong><br>Gray–Scott shows how local reaction and diffusion can organise global form, but similar forms can come from other mechanisms.</div>
</div>

<p class="takeaway"><strong>Next question:</strong> what measurements would let you distinguish two mechanisms that make visually similar patterns?</p>`);

// Clean a repeated prose typo globally.
for (const cell of nb.cells) {
  if (cell.cell_type !== "markdown") continue;
  setSource(cell, sourceText(cell)
    .replaceAll("complex-systems", "complex systems")
    .replaceAll("complex-system", "complex system"));
}

await fs.writeFile(path.join(IMAGE_DIR, "diffusion_grid_t012.svg"), makeDiffusionSvg());
await fs.writeFile(path.join(IMAGE_DIR, "diffusion_grid_numbers_t012.svg"), makeDiffusionSvg(true));
await fs.writeFile(path.join(IMAGE_DIR, "brownian_ensemble_msd.svg"), makeBrownianSvg());
await fs.writeFile(NOTEBOOK, JSON.stringify(nb, null, 1) + "\n");

console.log(`Updated ${NOTEBOOK}`);
console.log(`Cells: ${nb.cells.length}; fragments remaining: ${nb.cells.filter(c => c.metadata?.slideshow?.slide_type === "fragment").length}`);
