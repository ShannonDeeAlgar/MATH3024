from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks/week03/images/gray_scott_two_fields.png"


def laplacian(field: np.ndarray) -> np.ndarray:
    """Five-point periodic Laplacian with unit grid spacing."""
    return (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4.0 * field
    )


def simulate(size=150, steps=12_000, seed=7):
    du, dv, feed, kill, dt = 0.16, 0.08, 0.035, 0.065, 1.0
    rng = np.random.default_rng(seed)
    u = np.ones((size, size), dtype=float)
    v = np.zeros_like(u)

    # Several small perturbations make the spatial mechanism visible without
    # imposing the final morphology.
    for _ in range(12):
        i, j = rng.integers(15, size - 15, size=2)
        radius = int(rng.integers(3, 7))
        u[i - radius : i + radius, j - radius : j + radius] = 0.50
        v[i - radius : i + radius, j - radius : j + radius] = 0.25
    u += rng.normal(0.0, 0.004, size=u.shape)
    v += rng.normal(0.0, 0.002, size=v.shape)

    for _ in range(steps):
        uvv = u * v * v
        u += dt * (du * laplacian(u) - uvv + feed * (1.0 - u))
        v += dt * (dv * laplacian(v) + uvv - (feed + kill) * v)
        np.clip(u, 0.0, 1.0, out=u)
        np.clip(v, 0.0, 1.0, out=v)
    return u, v, (du, dv, feed, kill)


u, v, params = simulate()
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12})
fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6), constrained_layout=True)
for ax, field, title, cmap in zip(
    axes,
    (u, v),
    (r"$U$: feed concentration", r"$V$: autocatalytic concentration"),
    ("Blues_r", "magma"),
):
    image = ax.imshow(field, cmap=cmap, origin="lower", interpolation="nearest")
    ax.set_title(title, color="#1b2a4c", fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    bar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.025)
    bar.set_label("concentration")
fig.suptitle(
    rf"One Gray–Scott run: $D_u={params[0]}$, $D_v={params[1]}$, $f={params[2]}$, $k={params[3]}$",
    color="#1b2a4c",
    fontweight="bold",
)
fig.savefig(OUTPUT, dpi=180, transparent=True)
print(OUTPUT)
