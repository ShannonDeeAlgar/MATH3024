"""Regenerate the course-styled analysis figures used in the Week 8 Reader."""

from collections import deque
from pathlib import Path
import wave

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch, correlate


NAVY = "#20345b"
BLUE = "#4b96c6"
PALE = "#dbe8f5"
ORANGE = "#e45d32"
GOLD = "#f2c94c"
GRID = "#d7e1ef"
OUT = Path(__file__).with_name("images")

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 15,
        "axes.titlesize": 18,
        "axes.labelsize": 16,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "legend.fontsize": 12.5,
        "axes.edgecolor": NAVY,
        "axes.labelcolor": NAVY,
        "xtick.color": NAVY,
        "ytick.color": NAVY,
    }
)


def make_event_montage():
    """Three schematic records that motivate event-size questions."""
    rng = np.random.default_rng(3024)
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.7))

    ax = axes[0]
    t = np.linspace(0, 12, 1800)
    signal = 0.015 * rng.normal(size=t.size)
    for centre, amplitude, width in ((1.6, 0.18, 0.09), (3.2, 0.12, 0.07),
                                     (5.1, 0.30, 0.11), (8.0, 1.0, 0.24),
                                     (10.6, 0.16, 0.08)):
        envelope = amplitude * np.exp(-((t - centre) / width) ** 2)
        signal += envelope * np.sin(55 * (t - centre))
    ax.plot(t, signal, color=NAVY, lw=1.3)
    ax.set(title="Earthquakes", xlabel="time", ylabel="ground motion")

    ax = axes[1]
    n = 28
    xy = rng.uniform(0.05, 0.95, size=(n, 2))
    dist = np.linalg.norm(xy[:, None, :] - xy[None, :, :], axis=2)
    edges = np.argwhere(np.triu(dist < 0.27, 1))
    failed = np.argsort(np.linalg.norm(xy - np.array([0.57, 0.52]), axis=1))[:7]
    failed_set = set(failed.tolist())
    for i, j in edges:
        colour = ORANGE if i in failed_set and j in failed_set else GRID
        ax.plot(xy[[i, j], 0], xy[[i, j], 1], color=colour, lw=1.0, zorder=1)
    colours = [ORANGE if i in failed_set else BLUE for i in range(n)]
    ax.scatter(xy[:, 0], xy[:, 1], s=38, c=colours, edgecolor=NAVY, linewidth=0.5, zorder=2)
    ax.set(title="Cascading failures", xlabel="network position", xticks=[], yticks=[])

    ax = axes[2]
    for neuron in range(24):
        quiet = rng.uniform(0, 12, size=rng.integers(2, 5))
        burst = 7.0 + rng.normal(0, 0.28, size=rng.integers(2, 6))
        times = np.concatenate([quiet, burst])
        ax.vlines(times, neuron + 0.1, neuron + 0.9, color=NAVY, lw=0.8)
    ax.set(title="Neuronal activity", xlabel="time", ylabel="cell", yticks=[])

    for ax in axes:
        ax.title.set_color(NAVY)
        ax.grid(color=GRID, lw=0.7, alpha=0.7)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Many small events, a few much larger ones", color=NAVY, fontsize=18)
    fig.tight_layout()
    fig.savefig(OUT / "events_across_scales.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def add_and_relax(pile, rng):
    """Add one grain and return its toppling count."""
    L = pile.shape[0]
    i, j = rng.integers(0, L, size=2)
    pile[i, j] += 1
    queue = deque([(i, j)]) if pile[i, j] >= 4 else deque()
    topplings = 0
    while queue:
        x, y = queue.popleft()
        while pile[x, y] >= 4:
            pile[x, y] -= 4
            topplings += 1
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                u, v = x + di, y + dj
                if 0 <= u < L and 0 <= v < L:
                    pile[u, v] += 1
                    if pile[u, v] >= 4:
                        queue.append((u, v))
    return topplings


def activity_series(L=48, burn_in=45_000, samples=8_000, seed=3024):
    rng = np.random.default_rng(seed)
    pile = np.zeros((L, L), dtype=int)
    for _ in range(burn_in):
        add_and_relax(pile, rng)
    activity = np.array([add_and_relax(pile, rng) for _ in range(samples)])
    return activity


def relaxation_signal(L=48, burn_in=45_000, target_steps=1800, seed=3024):
    """Record the number of simultaneously toppling cells at each avalanche time step."""
    rng = np.random.default_rng(seed)
    pile = np.zeros((L, L), dtype=int)
    for _ in range(burn_in):
        i, j = rng.integers(0, L, size=2)
        pile[i, j] += 1
        # Burn-in needs only the final stable state. Abelian topplings can
        # be batched here; the measured record below still topples once/step.
        while np.any(pile >= 4):
            count = pile // 4
            pile -= 4 * count
            pile[1:, :] += count[:-1, :]
            pile[:-1, :] += count[1:, :]
            pile[:, 1:] += count[:, :-1]
            pile[:, :-1] += count[:, 1:]

    signal = []
    while len(signal) < target_steps:
        i, j = rng.integers(0, L, size=2)
        pile[i, j] += 1
        while True:
            unstable = pile >= 4
            count = int(unstable.sum())
            signal.append(count)
            if count == 0:
                break
            pile[unstable] -= 4
            pile[1:, :] += unstable[:-1, :]
            pile[:-1, :] += unstable[1:, :]
            pile[:, 1:] += unstable[:, :-1]
            pile[:, :-1] += unstable[:, 1:]
    return np.asarray(signal[:target_steps], dtype=float)


def make_time_index_figure(L=32, burn_in=14_000, seed=3024):
    """Show how within-trial step k maps onto the joined activity index t."""
    rng = np.random.default_rng(seed)
    pile = np.zeros((L, L), dtype=int)

    def run_trial():
        i, j = rng.integers(0, L, size=2)
        pile[i, j] += 1
        counts = []
        while True:
            unstable = pile >= 4
            counts.append(int(unstable.sum()))
            if not unstable.any():
                return counts
            pile[unstable] -= 4
            pile[1:, :] += unstable[:-1, :]
            pile[:-1, :] += unstable[1:, :]
            pile[:, 1:] += unstable[:, :-1]
            pile[:, :-1] += unstable[:, 1:]

    for _ in range(burn_in):
        run_trial()

    trials = [run_trial() for _ in range(240)]
    chosen = None
    for width in (5, 6, 4):
        for start in range(len(trials) - width + 1):
            candidate = trials[start:start + width]
            active = [len(x) - 1 for x in candidate]
            total = sum(len(x) for x in candidate)
            if 13 <= total <= 22 and sum(x > 0 for x in active) >= 3 and max(active) >= 4:
                chosen = candidate
                break
        if chosen is not None:
            break
    if chosen is None:
        raise RuntimeError("Could not find a compact illustrative trial window")

    values = np.asarray([value for trial in chosen for value in trial])
    t = np.arange(values.size)
    fig, ax = plt.subplots(figsize=(11.8, 4.7))
    colours = (PALE, "#f8eadf")
    cursor = 0
    ymax = max(5, int(values.max()))
    for number, trial in enumerate(chosen, start=1):
        end = cursor + len(trial)
        ax.axvspan(cursor - 0.5, end - 0.5, color=colours[(number - 1) % 2], alpha=0.72, zorder=0)
        ax.text((cursor + end - 1) / 2, ymax * 1.08, rf"trial $n={number}$",
                ha="center", va="bottom", color=NAVY, fontsize=12.5)
        for local, x in enumerate(range(cursor, end)):
            if trial[local] > 0:
                ax.text(x, -0.19, rf"$k={local + 1}$", transform=ax.get_xaxis_transform(),
                        ha="center", va="top", color=NAVY, fontsize=9.5)
        cursor = end

    ax.plot(t, values, color=NAVY, lw=2.0, marker="o", ms=5.5, zorder=3)
    ax.set_xticks(t)
    ax.set_xticklabels([str(x) for x in t], fontsize=10)
    ax.set_xlim(-0.5, len(t) - 0.5)
    ax.set_ylim(-0.3, ymax * 1.25)
    ax.set_xlabel(r"Joined record index, $t$", labelpad=38)
    ax.set_ylabel(r"Toppling sites, $A(t)$")
    ax.text(-0.8, -0.19, "within trial:", transform=ax.get_xaxis_transform(),
            ha="right", va="top", color=NAVY, fontsize=10.5)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.subplots_adjust(left=0.085, right=0.99, top=0.84, bottom=0.30)
    fig.savefig(OUT / "sandpile_time_indices.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def make_sandpile_audio(activity=None):
    """Sonify each active parallel step with one activity-scaled chime."""
    if activity is None:
        activity = relaxation_signal()
    activity = activity[:1800]
    sample_rate = 22_050
    step_samples = 360
    tone_samples = 2_200
    audio = np.zeros(activity.size * step_samples, dtype=float)
    scale = np.log1p(activity)
    if scale.max() > 0:
        scale /= scale.max()
    pentatonic = np.array([523.25, 587.33, 659.25, 783.99, 880.00, 1046.50])
    t = np.arange(tone_samples) / sample_rate
    envelope = np.exp(-28 * t) * (1 - np.exp(-180 * t))
    for i, amplitude in enumerate(scale):
        if activity[i] > 0:
            start = i * step_samples
            stop = min(start + tone_samples, audio.size)
            # Pitch and loudness both encode log activity. One onset represents
            # one active parallel step; individual topplings are not sounded.
            note = min(int(amplitude * pentatonic.size), pentatonic.size - 1)
            frequency = pentatonic[note]
            tone = (
                np.sin(2 * np.pi * frequency * t)
                + 0.32 * np.sin(2 * np.pi * 2.01 * frequency * t)
                + 0.12 * np.sin(2 * np.pi * 3.98 * frequency * t)
            ) * envelope
            audio[start:stop] += (0.18 + 0.82 * amplitude) * tone[:stop - start]
    peak = np.max(np.abs(audio))
    pcm = np.int16(audio / peak * 0.85 * np.iinfo(np.int16).max) if peak else np.zeros_like(audio, dtype=np.int16)
    with wave.open(str(OUT / "sandpile_toppling_sound.wav"), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())


def make_tail_comparison():
    x = np.linspace(1, 140, 900)
    power = x ** -1.6
    exponential = np.exp(-x / 13)
    gaussian = np.exp(-(x / 15) ** 2)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    for ax in axes:
        ax.plot(x, power, lw=3, color=ORANGE, label="power law — heavy-tailed")
        ax.plot(x, exponential, lw=2.7, color=BLUE, label="exponential — light-tailed")
        ax.plot(x, gaussian, lw=2.7, color=NAVY, label="Gaussian-like — light-tailed")
        ax.grid(color=GRID, lw=0.8)
        ax.set_xlabel("event size, $x$")
    axes[0].set(xlim=(0, 140), ylim=(-0.02, 1.03), ylabel="relative frequency", title="Linear axes")
    axes[1].set(xscale="log", yscale="log", xlim=(1, 140), ylim=(1e-12, 1.2), title="Log–log axes")
    axes[1].legend(frameon=False, loc="lower left")
    fig.suptitle("The power law has the heavy tail", color=NAVY, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "Tails_comparison.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def make_activity_figure(activity=None):
    if activity is None:
        activity = relaxation_signal(target_steps=131072)
    freq, power = welch(activity, fs=1.0, window="hann", nperseg=2048,
                        noverlap=1024, detrend="constant", scaling="density")
    freq, power = freq[1:], power[1:]

    fig, axes = plt.subplots(2, 1, figsize=(10.5, 6.6), gridspec_kw={"height_ratios": [1, 1.15]})
    window = 1800
    axes[0].plot(np.arange(window), activity[:window], color=NAVY, lw=1.2)
    axes[0].set(
        xlabel="Recorded avalanche time step, $t$",
        ylabel="Toppling sites, $A(t)$",
    )
    axes[1].loglog(freq, power, color=BLUE, lw=1.1, alpha=0.8)
    keep = (freq >= 0.01) & (freq <= 0.1) & (power > 0)
    slope, intercept = np.polyfit(np.log10(freq[keep]), np.log10(power[keep]), 1)
    xf = np.array([freq[keep].min(), freq[keep].max()])
    axes[1].loglog(xf, 10 ** intercept * xf ** slope, color=ORANGE, lw=3, label=f"Descriptive fit: slope {slope:.2f}")
    anchor = np.sqrt(xf.prod())
    anchor_power = 10 ** intercept * anchor ** slope
    axes[1].loglog(xf, np.full_like(xf, anchor_power),
                   color="#7D8799", ls=":", lw=2,
                   label="White-noise reference: slope 0")
    axes[1].loglog(xf, anchor_power * (xf / anchor) ** -2,
                   color=NAVY, ls="--", lw=2,
                   label="Red/Brownian-noise reference: slope −2")
    axes[1].axvspan(*xf, color=PALE, alpha=0.4, zorder=-1)
    axes[1].set(
        xlabel="Frequency (cycles per recorded relaxation step)",
        ylabel="Power spectral density",
    )
    print(f"Activity samples={len(activity)}, spectral slope={slope:.4f}; fit 0.01–0.1 cycles/step")
    axes[1].legend(frameon=False)
    for ax in axes:
        ax.grid(color=GRID, lw=0.7, alpha=0.8)
    fig.tight_layout()
    fig.savefig(OUT / "sandpile_activity_spectrum.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def make_autocorrelation_figure(activity):
    """Measure the same untransformed record used for sound and spectrum."""
    activity = np.asarray(activity, dtype=float)
    delta = activity - activity.mean()
    n = len(delta)
    variance = np.mean(delta**2)
    if variance == 0:
        raise ValueError("Autocorrelation requires non-zero activity variance")
    ac = correlate(delta, delta, mode="full", method="fft")[n - 1:]
    ac = ac / np.arange(n, 0, -1) / variance
    # Check FFT calculation against the defining pair average.
    for lag in [0, 1, 10, 50, 100]:
        expected = np.mean(delta[:n-lag] * delta[lag:]) / variance
        assert np.isclose(ac[lag], expected)
    crossing = np.flatnonzero(ac <= 1 / np.e)[0]
    tau = crossing - 1 + (ac[crossing-1] - 1/np.e) / (ac[crossing-1] - ac[crossing])
    fig, ax = plt.subplots(figsize=(9.2, 4.5), constrained_layout=True)
    lags = np.arange(201)
    ax.plot(lags, ac[:201], color=BLUE, lw=2.2, label="Measured autocorrelation")
    ax.plot(lags, np.exp(-lags / tau), color=ORANGE, ls="--",
            label="Exponential with the same e-folding time (reference)")
    ax.axhline(0, color=NAVY, lw=.8)
    ax.hlines(1/np.e, 0, tau, color=NAVY, ls=":")
    ax.vlines(tau, 0, 1/np.e, color=NAVY, ls=":")
    ax.plot(tau, 1/np.e, "o", color=NAVY)
    ax.annotate(rf"$C_A(\ell)=1/e$ at $\ell\approx{tau:.1f}$ steps",
                xy=(tau, 1/np.e), xytext=(65, .5),
                arrowprops=dict(arrowstyle="->", color=NAVY), color=NAVY)
    ax.set(
        xlabel="Lag, $\ell$ (recorded steps)",
        ylabel=r"Autocorrelation, $C_A(\ell)$",
        xlim=(0, 200),
        ylim=(-.08, 1.04),
    )
    ax.grid(color=GRID, lw=.7, alpha=.8)
    ax.legend(frameon=False, fontsize=12.5, loc="upper right")
    fig.savefig(OUT / "sandpile_autocorrelation.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Autocorrelation e-folding crossing: {tau:.4f} recorded steps")
    return tau


def make_temporal_analysis():
    activity = relaxation_signal(target_steps=131072)
    np.savez_compressed(OUT / "sandpile_temporal_record.npz", activity=activity,
                        lattice_size=48, burn_in=45000, seed=3024)
    make_activity_figure(activity)
    make_autocorrelation_figure(activity)
    make_sandpile_audio(activity)


def phi(p):
    return p**4 + 4 * p**3 * (1 - p) + 4 * p**2 * (1 - p) ** 2


def cobweb(ax, p0, steps, colour, label):
    p = p0
    xs, ys = [p], [0]
    for _ in range(steps):
        q = phi(p)
        xs.extend([p, q])
        ys.extend([q, q])
        p = q
    ax.plot(xs, ys, color=colour, lw=2.2, alpha=0.95, label=label)


def make_rga_cobweb():
    p = np.linspace(0, 1, 1000)
    # Solve R(P) = P, where R(P) = P^2(2-P)^2.  The non-trivial
    # fixed point in (0, 1) is (3-sqrt(5))/2; do not position it by eye.
    roots = np.roots([1, -4, 4, -1])
    pc = min(r.real for r in roots if abs(r.imag) < 1e-9 and 0 < r.real < 1 - 1e-9)
    fig, ax = plt.subplots(figsize=(7.4, 6.2))
    ax.plot(p, phi(p), color=NAVY, lw=3, label="$R(P_m)$")
    ax.plot(p, p, color="#8da0b9", lw=2, ls="--", label="$P_{m+1}=P_m$")
    cobweb(ax, pc - 0.08, 7, BLUE, "below threshold")
    cobweb(ax, pc + 0.08, 7, ORANGE, "above threshold")
    ax.scatter([pc], [pc], s=90, color=GOLD, edgecolor=NAVY, zorder=5)
    ax.annotate(f"unstable fixed point\n$P^*=(3-\\sqrt{{5}})/2\\approx{pc:.3f}$", (pc, pc), xytext=(0.56, 0.29),
                arrowprops={"arrowstyle": "->", "color": NAVY}, color=NAVY)
    ax.set(
        xlim=(0, 1),
        ylim=(0, 1),
        xlabel="current level, $P_m$",
        ylabel="next level, $P_{m+1}$",
    )
    ax.grid(color=GRID, lw=0.8)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "rga_cobweb_course.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_event_montage()
    # Tails_comparison.png is generated from simulated site-percolation
    # clusters by tools/generate_week08_percolation_evidence.py.
    make_temporal_analysis()
    make_time_index_figure()
    make_rga_cobweb()
