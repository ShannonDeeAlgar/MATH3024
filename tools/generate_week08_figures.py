"""Generate course-owned Week 8 sandpile figures from the canonical model."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import BoundaryNorm, ListedColormap

from figure_style import apply_course_figure_style, finish_axes, style_animation_frame


OUT = Path(__file__).resolve().parents[1] / "notebooks" / "week08" / "images"
NAVY = "#172A50"
BLUE = "#3C78A8"
YELLOW = "#F2CF4A"
CORAL = "#D95F3D"
GRID = "#D9E2EF"

apply_course_figure_style()


def add_and_relax(pile, rng, record_frames=False):
    """Add one grain and relax in parallel steps.

    Size is the total number of topplings. Duration is the number of parallel
    parallel relaxation steps. Grains that leave the open boundary are lost.
    """
    L = pile.shape[0]
    i, j = rng.integers(0, L, size=2)
    pile[i, j] += 1
    topplings = 0
    duration = 0
    mask = np.zeros_like(pile, dtype=bool)
    frames = [pile.copy()] if record_frames else []
    while np.any(pile >= 4):
        count = pile // 4
        active = count > 0
        mask |= active
        pile %= 4
        topplings += int(count.sum())
        duration += 1
        pile[1:, :] += count[:-1, :]
        pile[:-1, :] += count[1:, :]
        pile[:, 1:] += count[:, :-1]
        pile[:, :-1] += count[:, 1:]
        if record_frames:
            frames.append(pile.copy())
    return topplings, duration, mask, frames


def simulate(L=48, additions=70_000, burn=12_000, seed=3024):
    rng = np.random.default_rng(seed)
    pile = np.zeros((L, L), dtype=int)
    sizes = []
    durations = []
    activity = []
    largest = np.zeros_like(pile, dtype=bool)
    for n in range(additions):
        size, duration, mask, _ = add_and_relax(pile, rng)
        if n >= burn:
            activity.append(size)
            if size:
                sizes.append(size)
                durations.append(duration)
                if size > largest.sum():
                    largest = mask.copy()
    # Find a clear example avalanche without paying the cost of retaining
    # frames for every event in the statistical run.
    longest_frames = []
    for _ in range(2_500):
        _, _, _, frames = add_and_relax(pile, rng, record_frames=True)
        if len(frames) > len(longest_frames):
            longest_frames = frames
    return (pile, np.asarray(sizes), np.asarray(durations),
            np.asarray(activity), largest, longest_frames)


def relax_all(pile):
    """Relax every unstable site in parallel; grains leave at open edges."""
    pile = np.asarray(pile, dtype=np.int64).copy()
    topplings = 0
    while np.any(pile >= 4):
        count = pile // 4
        pile %= 4
        topplings += int(count.sum())
        pile[1:, :] += count[:-1, :]
        pile[:-1, :] += count[1:, :]
        pile[:, 1:] += count[:, :-1]
        pile[:, :-1] += count[:, 1:]
    return pile, topplings


def centred_pile(L, grains):
    pile = np.zeros((L, L), dtype=np.int64)
    pile[L // 2, L // 2] = grains
    return relax_all(pile)[0]


def style(ax):
    finish_axes(ax)


def box_counts(mask):
    L = mask.shape[0]
    scales = np.array([1, 2, 4, 8, 16, 32])
    counts = []
    for b in scales:
        n = int(np.ceil(L / b))
        count = 0
        for i in range(n):
            for j in range(n):
                if mask[i*b:min((i+1)*b, L), j*b:min((j+1)*b, L)].any():
                    count += 1
        counts.append(count)
    return scales, np.asarray(counts)


def finite_scale_dimension(mask, fit_indices=slice(1, 5)):
    """Return scales, counts and the fitted finite-scale box-counting slope."""
    scales, counts = box_counts(mask)
    x = np.log(1 / scales[fit_indices])
    y = np.log(counts[fit_indices])
    slope, intercept = np.polyfit(x, y, 1)
    return scales, counts, slope, intercept


def log_binned_density(values, bins=28):
    values = np.asarray(values)
    values = values[values > 0]
    edges = np.logspace(np.log10(values.min()), np.log10(values.max()), bins + 1)
    counts, edges = np.histogram(values, bins=edges)
    widths = np.diff(edges)
    density = counts / (values.size * widths)
    centres = np.sqrt(edges[:-1] * edges[1:])
    keep = counts > 0
    return centres[keep], density[keep]


def fit_scaling_region(x, density, lower_q=.18, upper_q=.72):
    """Fit a visibly populated middle range, excluding discreteness and cutoff."""
    lo, hi = np.quantile(x, [lower_q, upper_q])
    use = (x >= lo) & (x <= hi) & (density > 0)
    slope, intercept = np.polyfit(np.log10(x[use]), np.log10(density[use]), 1)
    return use, slope, intercept


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pile, sizes, durations, activity, largest, avalanche_frames = simulate()

    # A longer avalanche, displayed a little faster than the old animation.
    # Repeating the stable final frame gives students time to inspect the result.
    if avalanche_frames:
        frames = avalanche_frames + [avalanche_frames[-1]] * 5
        cmap = ListedColormap(["#F7F8FB", BLUE, YELLOW, CORAL])
        norm = BoundaryNorm(np.arange(-0.5, 4.5, 1), cmap.N)
        fig, ax = plt.subplots(figsize=(5.3, 5.1), constrained_layout=True)
        im = ax.imshow(frames[0], cmap=cmap, norm=norm, interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([])
        title = ax.set_title("")

        def draw(k):
            im.set_data(frames[k])
            title.set_text(f"Parallel relaxation step {min(k, len(avalanche_frames)-1)} of {len(avalanche_frames)-1}")
            style_animation_frame(fig, [ax])
            matplotlib.rcParams["savefig.bbox"] = "standard"
            return im, title

        anim = FuncAnimation(fig, draw, frames=len(frames), interval=135, blit=False)
        # Animations require a fixed canvas; the static-figure default uses a
        # tight bounding box, which can vary slightly from frame to frame.
        with matplotlib.rc_context({"savefig.bbox": "standard"}):
            anim.save(OUT / "sandpile_avalanche.gif", writer=PillowWriter(fps=7.4), dpi=105)
        plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(9, 8), constrained_layout=True)
    for level, ax in enumerate(axes.flat):
        ax.imshow(pile == level, cmap="binary", interpolation="nearest")
        ax.set_title(f"Sites at height {level}")
        ax.set_xticks([]); ax.set_yticks([])
    fig.savefig(OUT / "sandpile_height_subsets.png", dpi=220, transparent=True)
    plt.close(fig)

    # Two ways of reaching an active stable pile. Slow driving is faithful but
    # spends many additions loading an initially empty system. An overfull
    # state can instead be relaxed once, then driven briefly before sampling.
    rng = np.random.default_rng(8031)
    slow = np.zeros((42, 42), dtype=int)
    nonzero = 0
    for _ in range(700):
        size, _, _, _ = add_and_relax(slow, rng)
        nonzero += size > 0
    prepared_raw = rng.integers(0, 8, size=(42, 42))
    prepared, preparation_topplings = relax_all(prepared_raw)
    cmap = ListedColormap(["#F7F8FB", BLUE, YELLOW, CORAL])
    norm = BoundaryNorm(np.arange(-0.5, 4.5, 1), cmap.N)
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.1), constrained_layout=True)
    for ax, field, title in [
        (axes[0], slow, "Slow drive\nfrom an empty lattice"),
        (axes[1], prepared, "Relax a deliberately\noverfull lattice"),
    ]:
        im = ax.imshow(field, cmap=cmap, norm=norm, interpolation="nearest")
        ax.set_title(title, pad=7)
        ax.set_xticks([]); ax.set_yticks([])
    cbar = fig.colorbar(im, ax=axes, ticks=range(4), shrink=.82, label="Stable height")
    axes[0].text(.5, -.09, f"700 additions; {nonzero} triggered topplings",
                 transform=axes[0].transAxes, ha="center", color=NAVY)
    axes[1].text(.5, -.09, f"{preparation_topplings:,} topplings during preparation",
                 transform=axes[1].transAxes, ha="center", color=NAVY)
    fig.savefig(OUT / "sandpile_initialisation_comparison.png", dpi=220, transparent=True)
    plt.close(fig)

    # Central additions give especially legible nested spatial structure. The
    # sequence complements the statistically typical height subsets above; it
    # is not presented as a typical random-drive snapshot.
    grain_counts = [2**12, 2**14, 2**16]
    fields = [centred_pile(121, n) for n in grain_counts]
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.9), constrained_layout=True)
    for ax, field, grains in zip(axes, fields, grain_counts):
        im = ax.imshow(field, cmap=cmap, norm=norm, interpolation="nearest")
        ax.set_title(f"$2^{{{int(np.log2(grains))}}}$ grains at the centre")
        ax.set_xticks([]); ax.set_yticks([])
    fig.colorbar(im, ax=axes, ticks=range(4), shrink=.78, label="Stable height")
    fig.savefig(OUT / "sandpile_fractal_stills.png", dpi=220, transparent=True)
    plt.close(fig)

    # Use the largest symmetric pile for the height-class comparison. These
    # are finite-resolution slopes, not continuum dimensions of a finite image.
    symmetric = fields[-1]
    dimensions = []
    level_colours = ["#F7F8FB", BLUE, YELLOW, CORAL]
    fig, axes = plt.subplots(1, 4, figsize=(14.8, 3.55), constrained_layout=True)
    for level, (ax, colour) in enumerate(zip(axes, level_colours)):
        _, _, dim, _ = finite_scale_dimension(symmetric == level)
        dimensions.append(dim)
        # Height zero is white in the preceding stable-height figure, so use a
        # navy ground in that panel to keep its white sites visible. The other
        # panels use the same blue, yellow and coral height colours on white.
        background = NAVY if level == 0 else "#FFFFFF"
        subset_cmap = ListedColormap([background, colour])
        ax.imshow(symmetric == level, cmap=subset_cmap,
                  interpolation="nearest", vmin=0, vmax=1)
        ax.set_title(f"Height {level}\nfinite-scale $D\\approx{dim:.2f}$", pad=7)
        ax.set_xticks([]); ax.set_yticks([])
    fig.savefig(OUT / "sandpile_height_subsets.png", dpi=220, transparent=True)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True)
    for level, color in zip(range(4), [NAVY, BLUE, CORAL, YELLOW]):
        scales, counts, dim, intercept = finite_scale_dimension(symmetric == level)
        ax.loglog(1/scales, counts, "o-", color=color,
                  label=f"height {level}: $D\\approx{dim:.2f}$")
        fit_scales = scales[1:5]
        ax.loglog(1/fit_scales, np.exp(intercept)*(1/fit_scales)**dim,
                  color=color, lw=3, alpha=.35)
    ax.axvspan(1/16, 1/2, color="#EEF2F7", zorder=-2)
    ax.text(
        0.5, 0.97, "shaded: common fitted scales", transform=ax.transAxes,
        ha="center", va="top", color="#5A6685", fontsize=11,
    )
    ax.set(xlabel="Inverse box width, $1/\\varepsilon$", ylabel="Occupied boxes, $N(\\varepsilon)$")
    style(ax); ax.legend(frameon=False, ncol=2)
    fig.savefig(OUT / "sandpile_box_counting.png", dpi=220, transparent=True)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8.2), constrained_layout=True)
    for row, (values, symbol, label, color) in enumerate([
        (sizes, "S", "size (topplings)", BLUE),
        (durations, "T", "duration (avalanche time steps)", CORAL),
    ]):
        axes[row, 0].hist(values, bins=55, color=color, alpha=.88)
        axes[row, 0].set(xlabel=f"Avalanche {label}, ${symbol}$", ylabel="Number of avalanches",
                         title=f"Ordinary histogram of ${symbol}$")
        centres, density = log_binned_density(values)
        use, slope, intercept = fit_scaling_region(centres, density)
        axes[row, 1].loglog(centres, density, "o", color=color, ms=5,
                            label="log-binned probability density")
        fit_x = centres[use]
        exponent = -slope
        axes[row, 1].loglog(fit_x, 10**intercept * fit_x**slope, color=NAVY, lw=2.4,
                            label=(f"descriptive fit: $\\hat{{\\tau}}_{symbol}"
                                   f"\\approx {exponent:.2f}$ (slope $=-\\hat{{\\tau}}_{symbol}$)"))
        axes[row, 1].axvspan(fit_x.min(), fit_x.max(), color="#EEF2F7", zorder=-2,
                             label="illustrative fitted range")
        axes[row, 1].set(xlabel=f"Avalanche {label}, ${symbol}$",
                         ylabel=f"Probability density, $p({symbol})$",
                         title=f"Log-binned density of ${symbol}$")
        axes[row, 1].legend(frameon=False, fontsize=10, loc="best")
    for ax in axes.flat: style(ax)
    fig.suptitle(f"The same {len(sizes):,} non-zero avalanches, summarised four ways", fontsize=17)
    fig.savefig(OUT / "sandpile_avalanche_distributions.png", dpi=220, transparent=True)
    plt.close(fig)

    x = activity - activity.mean()
    power = np.abs(np.fft.rfft(x))**2
    freq = np.fft.rfftfreq(len(x))[1:]
    power = power[1:]
    fig, ax = plt.subplots(figsize=(6.6, 4.8), constrained_layout=True)
    ax.loglog(freq, power, color=BLUE, linewidth=1.2)
    ax.set(xlabel="Frequency", ylabel="Power", title="Fluctuations in avalanche activity")
    style(ax)
    fig.savefig(OUT / "sandpile_activity_spectrum.png", dpi=220, transparent=True)
    plt.close(fig)

    # Renormalisation map. Calculate, rather than position by eye, the
    # non-trivial fixed point of Phi(p) = p^2(2-p)^2.
    def phi(p):
        return p**4 + 4*p**3*(1-p) + 4*p**2*(1-p)**2

    roots = np.roots([1, -4, 4, -1])
    interior = [z.real for z in roots if abs(z.imag) < 1e-10 and 0 < z.real < 1 - 1e-9]
    pc = min(interior)
    x = np.linspace(0, 1, 600)
    fig, ax = plt.subplots(figsize=(6.7, 5.2), constrained_layout=True)
    ax.plot(x, x, "--", color="#92A7C3", lw=2, label="$P_{s+1}=P_s$")
    ax.plot(x, phi(x), color=NAVY, lw=3, label="$P_{s+1}=\\Phi(P_s)$")
    p = 0.28
    for _ in range(12):
        q = phi(p)
        ax.plot([p, p], [p, q], color=CORAL, lw=2)
        ax.plot([p, q], [q, q], color=CORAL, lw=2)
        p = q
    ax.scatter([pc], [pc], s=115, color=YELLOW, edgecolor=NAVY, zorder=5)
    ax.annotate(f"unstable fixed point\n$P^*=(3-\\sqrt{{5}})/2\\approx{pc:.3f}$",
                xy=(pc, pc), xytext=(.56, .27), textcoords="axes fraction",
                arrowprops={"arrowstyle": "-", "color": NAVY, "lw": 1.5},
                fontsize=13)
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="$P_s$", ylabel="$P_{s+1}$")
    style(ax)
    ax.legend(frameon=False, loc="upper left")
    fig.savefig(OUT / "rga_cobweb_course.png", dpi=220, transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    main()
