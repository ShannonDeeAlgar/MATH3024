"""Generate a self-contained GIF of Kuramoto phases organising."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.colors import Normalize, to_hex
from matplotlib.font_manager import FontProperties, findfont
from figure_style import BLUE, GRID as PALE, INK as NAVY, ORANGE, apply_course_figure_style

SUMMARY_GREY = "#667085"


def simulate(n=36, coupling=1.65, dt=0.04, steps=300, seed=3024):
    rng = np.random.default_rng(seed)
    # A non-zero centre keeps the locked group visibly rotating in the
    # laboratory frame; heterogeneity is the spread about that common scale.
    omega = rng.normal(3.0, 0.48, n)
    theta = rng.uniform(0, 2 * np.pi, n)
    history = np.empty((steps, n))
    order = np.empty(steps)
    for step in range(steps):
        history[step] = theta
        z = np.mean(np.exp(1j * theta))
        order[step] = abs(z)
        theta = (theta + dt * (omega + coupling * np.imag(z * np.exp(-1j * theta)))) % (2 * np.pi)
    return history, order, dt, omega


def font(size, bold=False):
    """Use the same DejaVu Sans files as the course Matplotlib style."""
    path = findfont(FontProperties(family="DejaVu Sans", weight="bold" if bold else "normal"))
    return ImageFont.truetype(path, size)


def main():
    history, order, dt, omega = simulate()
    norm = Normalize(vmin=float(omega.min()), vmax=float(omega.max()))
    colours = [to_hex(colormaps["coolwarm"](norm(value))) for value in omega]
    sampled = np.linspace(0, len(history) - 1, 64, dtype=int)
    duration = (len(history) - 1) * dt
    time = np.arange(len(history)) * dt
    unwrapped = np.unwrap(history, axis=0)
    mean_phase = np.unwrap(np.angle(np.mean(np.exp(1j * history), axis=1)))
    # The circular mean is defined modulo 2π. Put it on the same unwrapped
    # branch as the individual histories before plotting it with them.
    individual_centre = np.mean(unwrapped, axis=1)
    mean_phase += 2 * np.pi * np.round((individual_centre - mean_phase) / (2 * np.pi))

    qualitative_frames = []
    quantitative_frames = []
    for k in sampled:
        # Qualitative view: show the same phases in two visual encodings. The
        # left panel is phase space. The right panel keeps nodes fixed and
        # represents crossing phase zero as a brief flash.
        image = Image.new("RGB", (1200, 540), "white")
        draw = ImageDraw.Draw(image)
        centre, radius = (285, 280), 180
        draw.text((105, 18), "Position in the cycle", fill=NAVY, font=font(31, bold=True))
        draw.text((166, 60), "phase-space view", fill=NAVY, font=font(20))
        draw.ellipse((centre[0]-radius, centre[1]-radius, centre[0]+radius, centre[1]+radius), outline=NAVY, width=5)
        theta = history[k]
        for value, colour in zip(theta, colours):
            x, y = centre[0] + radius*np.cos(value), centre[1] - radius*np.sin(value)
            draw.ellipse((x-8, y-8, x+8, y+8), fill=colour, outline="white", width=2)
        draw.text((720, 18), "Fixed nodes that flash", fill=NAVY, font=font(31, bold=True))
        draw.text((795, 60), "fixed-node view", fill=NAVY, font=font(20))
        cols = 6
        spacing_x, spacing_y = 88, 78
        x0, y0 = 665, 115
        # Brightness is largest as a clock passes phase zero. This changes the
        # display, not the simulated state or interaction rule.
        brightness = np.exp(-0.5 * (np.angle(np.exp(1j * theta)) / 0.32) ** 2)
        for index, (value, colour, level) in enumerate(zip(theta, colours, brightness)):
            row, col = divmod(index, cols)
            x, y = x0 + col * spacing_x, y0 + row * spacing_y
            base = np.array([235, 237, 241])
            lit = np.array([245, 178, 45])
            rgb = tuple((base * (1-level) + lit * level).astype(int))
            draw.ellipse((x-18, y-18, x+18, y+18), fill=rgb, outline=NAVY, width=2)
        draw.text((548, 508), f"t = {k*dt:4.1f}", fill=NAVY, font=font(25))
        qualitative_frames.append(image)

        # Quantitative view: retain the moving points, then add their vector
        # average and time-series summaries without hiding the individuals.
        image = Image.new("RGB", (1500, 760), "white")
        draw = ImageDraw.Draw(image)
        centre, radius = (330, 385), 225
        draw.text((150, 25), "Current phases", fill=NAVY, font=font(36, bold=True))
        draw.text((700, 25), "Individual histories and collective summaries", fill=NAVY, font=font(29, bold=True))
        draw.text((115, 78), "colour: natural frequency", fill=NAVY, font=font(19))
        draw.text((115, 108), "grey: vector average", fill=SUMMARY_GREY, font=font(19))
        draw.ellipse((centre[0]-radius, centre[1]-radius, centre[0]+radius, centre[1]+radius), outline=NAVY, width=5)
        for value, colour in zip(theta, colours):
            x, y = centre[0] + radius*np.cos(value), centre[1] - radius*np.sin(value)
            draw.ellipse((x-7, y-7, x+7, y+7), fill=colour, outline="white", width=1)
        z = np.mean(np.exp(1j * theta))
        draw.line((centre, (centre[0]+radius*z.real, centre[1]-radius*z.imag)), fill=SUMMARY_GREY, width=7)
        left, right = 700, 1435
        phase_top, phase_bottom = 120, 410
        coherence_top, coherence_bottom = 505, 700
        for top, bottom in ((phase_top, phase_bottom), (coherence_top, coherence_bottom)):
            draw.line((left, bottom, right, bottom), fill=NAVY, width=3)
            draw.line((left, top, left, bottom), fill=NAVY, width=3)
        draw.text((710, 78), "individual phase histories", fill=NAVY, font=font(19))
        draw.text((1090, 78), "mean phase", fill=SUMMARY_GREY, font=font(19))
        draw.text((620, 235), "phase", fill=NAVY, font=font(25))
        draw.text((620, 585), "r(t)", fill=NAVY, font=font(27))
        draw.text((1030, 715), "time", fill=NAVY, font=font(24))

        # For this combined view, phase is a position within a cycle. Plot it
        # modulo 2π so the traces and the circle use the same representation.
        wrapped = history % (2 * np.pi)
        wrapped_mean = np.angle(np.mean(np.exp(1j * history), axis=1)) % (2 * np.pi)
        phase_min, phase_max = 0.0, 2 * np.pi
        phase_span = phase_max - phase_min
        xcoords = left + (time[:k+1] / duration) * (right-left)
        for trajectory, colour in zip(wrapped.T, colours):
            values = trajectory[:k+1]
            ycoords = phase_bottom - (values-phase_min)/phase_span*(phase_bottom-phase_top)
            coords = list(zip(xcoords, ycoords))
            if len(coords) > 1:
                draw.line(coords, fill=colour, width=1)
        mean_values = wrapped_mean[:k+1]
        mean_y = phase_bottom - (mean_values-phase_min)/phase_span*(phase_bottom-phase_top)
        mean_coords = list(zip(xcoords, mean_y))
        if len(mean_coords) > 1:
            draw.line(mean_coords, fill=SUMMARY_GREY, width=5)

        for level in (0.0, 0.5, 1.0):
            y = coherence_bottom - level*(coherence_bottom-coherence_top)
            draw.line((left, y, right, y), fill=PALE, width=2)
        coherence_y = coherence_bottom - order[:k+1]*(coherence_bottom-coherence_top)
        coherence_coords = list(zip(xcoords, coherence_y))
        if len(coherence_coords) > 1:
            draw.line(coherence_coords, fill=SUMMARY_GREY, width=5)
        draw.text((655, coherence_bottom-16), "0", fill=NAVY, font=font(21))
        draw.text((655, coherence_top-12), "1", fill=NAVY, font=font(21))
        quantitative_frames.append(image)

    output_dir = Path(__file__).resolve().parents[1] / "notebooks/week06/images"
    qualitative_output = output_dir / "kuramoto_phase_circle.gif"
    qualitative_frames[0].save(
        qualitative_output, save_all=True, append_images=qualitative_frames[1:],
        duration=240, loop=0, optimize=False,
    )
    output = output_dir / "kuramoto_phase_organisation.gif"
    quantitative_frames[0].save(
        output, save_all=True, append_images=quantitative_frames[1:],
        duration=240, loop=0, optimize=False,
    )

    # Also retain a static version for print and accessibility.
    apply_course_figure_style()
    fig, axes = plt.subplots(
        2, 1, figsize=(11.5, 6.8), sharex=True,
        gridspec_kw={"height_ratios": (1.7, 1)}, constrained_layout=True,
    )
    for trajectory, colour in zip(unwrapped.T, colours):
        axes[0].plot(time, trajectory, color=colour, lw=0.8, alpha=0.28)
    axes[0].plot(time, mean_phase, color=SUMMARY_GREY, lw=3.2, label=r"collective mean phase, $\psi(t)$")
    axes[0].set(ylabel="unwrapped phase")
    axes[0].legend(frameon=False, loc="upper left")
    axes[1].plot(time, order, color=SUMMARY_GREY, lw=3.2)
    axes[1].set(xlabel="time", ylabel=r"coherence, $r(t)$", ylim=(0, 1.03))
    for axis in axes:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(color=PALE, lw=0.8, alpha=0.8)
    fig.savefig(output.with_name("kuramoto_phase_trajectories_coherence.svg"), transparent=True, bbox_inches="tight")
    plt.close(fig)

    # Natural versus realised frequency: the horizontal band identifies the
    # locked group, while oscillators outside it continue to drift.
    realised = (unwrapped[-1] - unwrapped[len(unwrapped)//2]) / (
        time[-1] - time[len(time)//2]
    )
    locked_rate = float(np.median(realised))
    locked = np.abs(realised - locked_rate) < 0.08
    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    bounds = [float(omega.min()) - 0.15, float(omega.max()) + 0.15]
    ax.plot(bounds, bounds, color="#AAB5C8", lw=2, label=r"without coupling: $\Omega_i=\omega_i$")
    ax.axhline(locked_rate, color=NAVY, ls="--", lw=2, label="locked-group rate")
    ax.scatter(omega[~locked], realised[~locked], s=55, color="#F4C542", edgecolor=NAVY,
               label="drifting")
    ax.scatter(omega[locked], realised[locked], s=55, color=BLUE, edgecolor="white",
               label="frequency locked")
    ax.set(xlabel=r"Natural frequency, $\omega_i$",
           ylabel=r"Realised long-time frequency, $\Omega_i$")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=PALE, lw=0.8, alpha=0.8)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=2,
              fontsize=12.5, handlelength=2.4, columnspacing=1.4)
    fig.savefig(output.with_name("kuramoto_realised_frequency.svg"), transparent=True,
                bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
