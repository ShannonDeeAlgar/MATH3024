"""Week 8 instructor checks and full ensemble investigation.

Follow the workshop questions in order:
Read the functions: starting-pile options, addition sites and boundary loss.
1. Code checks 1–5: individual topplings, known cases, an avalanche trace,
   recorded runs and seed correspondence. Optional diagnostics follow.
2. How many runs? Questions 1–7: precision, fresh batches, domain size,
   upper-tail contributors and longer records, with the three requested displays.

The default starts with 20 runs at each L, adds batches of ten where needed,
and checks the precision target with a fresh batch. The budget is 60 runs per L. It also
compares 1,500 and 3,000 recorded trials for four of the same seeds at L=32.
Use --checks-only to run just the verification examples, or --initial-only to
show only the starting ensembles. --record-length-check adds the longer-record
comparison to --initial-only; it is already included in the full run.
Add --100-runs for an extra precision plot through 100 runs at every L.
It reuses the existing runs and leaves the workshop stopping decisions unchanged.

Law (2015), https://informs-sim.org/wsc15papers/188.pdf, discusses independent
replications and precision. His examples use Student-t intervals; our supplied
mean_interval helper resamples run summaries. Students use its bounds; the
statistical method is outside this investigation. Target and batch sizes are
teaching choices.
"""

from pathlib import Path
import ast
import json
import sys
import time

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Rectangle
import numpy as np


NOTEBOOK = Path(__file__).with_name("WS_Critical_phenomena.ipynb")


def load_workshop_code():
    notebook = json.loads(NOTEBOOK.read_text())
    wanted = {
        "week08-sandpile-implementation",
        "week08-analysis-helpers",
    }
    namespace = {}
    found = set()
    for cell in notebook["cells"]:
        cell_id = cell.get("id")
        if cell_id in wanted:
            exec("".join(cell["source"]), namespace)
            found.add(cell_id)
    missing = wanted - found
    if missing:
        raise RuntimeError(f"Missing workshop code cells: {sorted(missing)}")
    return namespace


ns = load_workshop_code()
relax_pile = ns["relax_pile"]
add_grain_and_relax = ns["add_grain_and_relax"]
prepare_active_pile = ns["prepare_active_pile"]
run_sandpile = ns["run_sandpile"]
run_sandpile_ensemble = ns["run_sandpile_ensemble"]
empirical_ccdf = ns["empirical_ccdf"]
mean_interval = ns["mean_interval"]


def assert_event(event, *, size, area, duration):
    assert event["size"] == size
    assert event["area"] == area
    assert event["duration"] == duration


def section(title):
    print(f"\n{title}")


def verification_section(question, title):
    section(f"Code check {question}: {title}")


def show_figure(title, figure):
    """Keep notebook headings beside their plots; show CLI figures together at the end."""
    section(title)
    figure.canvas.manager.set_window_title(title)
    if "ipykernel" in sys.modules:
        plt.show()
    return figure


def instrument_relax_pile():
    """Add observation hooks to the supplied function, leaving its rules unchanged."""
    notebook = json.loads(NOTEBOOK.read_text())
    cell = next(cell for cell in notebook["cells"]
                if cell.get("id") == "week08-sandpile-implementation")
    tree = ast.parse("".join(cell["source"]))
    function = next(node for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == "relax_pile")
    waves = [node for node in ast.walk(function)
             if isinstance(node, ast.While) and isinstance(node.test, ast.Name)
             and node.test.id == "current"]
    assert len(waves) == 1, "Expected one parallel-wave loop in supplied relax_pile"
    wave = waves[0]
    toppling_loops = [node for node in wave.body
                     if isinstance(node, ast.For) and isinstance(node.iter, ast.Name)
                     and node.iter.id == "ordered"]
    assert len(toppling_loops) == 1, "Expected one individual-toppling loop"
    toppling = toppling_loops[0]
    assert ast.unparse(toppling.target) == "(x, y)"

    function.name = "relax_pile_with_trace"
    function.args.kwonlyargs.append(ast.arg(arg="observe"))
    function.args.kw_defaults.append(None)
    wave.body[:0] = ast.parse(
        'observe("parallel_before", duration + 1, None, pile.copy())'
    ).body
    wave.body.extend(ast.parse(
        'observe("parallel_after", duration, None, pile.copy())'
    ).body)
    toppling.body[:0] = ast.parse(
        'observe("toppling_before", duration, (int(x), int(y)), pile.copy())'
    ).body
    toppling.body.extend(ast.parse(
        'observe("toppling_after", duration, (int(x), int(y)), pile.copy())'
    ).body)
    traced_tree = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    namespace = ns.copy()
    exec(compile(traced_tree, str(NOTEBOOK), "exec"), namespace)
    return namespace[function.name]


relax_pile_with_trace = instrument_relax_pile()


def trace_supplied_relaxation(initial, site_order="forward"):
    """Record the actual supplied function's individual updates and parallel waves."""
    pile = initial.copy()
    waves, topplings = [], []

    def observe(stage, k, site, state):
        if stage == "parallel_before":
            assert k == len(waves) + 1
            waves.append({"before": state, "sites": []})
        elif stage == "toppling_before":
            assert k == len(waves)
            topplings.append({"k": k, "site": site, "before": state})
            waves[-1]["sites"].append(site)
        elif stage == "toppling_after":
            update = topplings[-1]
            assert (update["k"], update["site"]) == (k, site)
            update["after"] = state
            update["loss"] = int(update["before"].sum() - state.sum())
        elif stage == "parallel_after":
            assert k == len(waves)
            wave = waves[-1]
            wave["after"] = state
            wave["loss"] = int(wave["before"].sum() - state.sum())
        else:
            raise ValueError(f"Unknown observation stage: {stage}")

    event = relax_pile_with_trace(pile, site_order=site_order, observe=observe)
    assert event == event_from_trace(waves)
    assert initial.sum() == pile.sum() + sum(update["loss"] for update in topplings)
    assert len(topplings) == event["size"]
    return pile, event, waves, topplings


def trace_parallel_relaxation(initial, max_steps=1_000):
    """Independent whole-lattice updates, with one record per parallel step."""
    pile = initial.copy()
    trace = []
    while np.any(pile >= 4):
        if len(trace) >= max_steps:
            raise RuntimeError("Diagnostic relaxation exceeded its step limit")
        before = pile.copy()
        active = (before >= 4).astype(np.int64)
        # Every initially unstable site loses four and sends one in each direction.
        pile = before - 4 * active
        pile[1:, :] += active[:-1, :]
        pile[:-1, :] += active[1:, :]
        pile[:, 1:] += active[:, :-1]
        pile[:, :-1] += active[:, 1:]
        # A corner sends grains beyond two edges.
        loss = int(active[0, :].sum() + active[-1, :].sum()
                   + active[:, 0].sum() + active[:, -1].sum())
        trace.append({
            "before": before,
            "sites": [tuple(int(coordinate) for coordinate in site)
                      for site in np.argwhere(active)],
            "loss": loss,
            "after": pile.copy(),
        })
        assert before.sum() == pile.sum() + loss
    return pile, trace


def event_from_trace(trace):
    """Count all topplings, distinct sites and active parallel steps."""
    sites = [site for step in trace for site in step["sites"]]
    return {"size": len(sites), "area": len(set(sites)), "duration": len(trace)}


def check_starting_piles():
    section("Read the functions: starting-pile options")
    L, seed = 5, 127
    empty = run_sandpile(L=L, additions=0, burn_in=0, seed=seed)
    assert empty["pile"].shape == (L, L)
    assert np.array_equal(empty["pile"], np.zeros((L, L), dtype=np.int64))
    assert empty["recorded_additions"] == 0
    for field in ("size", "area", "duration", "mean_load"):
        assert empty[field].size == 0

    supplied = np.full((L, L), 2, dtype=np.int64)
    supplied_before = supplied.copy()
    copied = run_sandpile(L=L, additions=0, burn_in=0, seed=seed, initial=supplied)
    assert np.array_equal(copied["pile"], supplied_before)
    assert np.array_equal(supplied, supplied_before)
    assert not np.shares_memory(copied["pile"], supplied)

    overfull = np.random.default_rng(seed).integers(0, 8, size=(L, L), dtype=np.int64)
    expected_pile, trace = trace_parallel_relaxation(overfull)
    prepared, preparation = prepare_active_pile(L=L, seed=seed)
    repeated, repeated_preparation = prepare_active_pile(L=L, seed=seed)
    assert np.array_equal(prepared, expected_pile)
    assert preparation == event_from_trace(trace)
    assert np.array_equal(repeated, prepared)
    assert repeated_preparation == preparation
    assert prepared.min() >= 0 and prepared.max() < 4
    print("  Default: an empty L x L pile. A supplied stable pile is copied.")
    print("  Overfull preparation: seeded loads 0-7, followed by complete relaxation.")
    print("  Preparation ends at stability; burn-in uses subsequent grain additions.")
    print("  Addition sites and boundary loss are checked below in Code checks 4 and 1-2.")


def check_individual_topplings():
    verification_section(1, "Inspect individual topplings")

    pile = np.zeros((3, 3), dtype=np.int64)
    pile[1, 1] = 3
    before = pile.copy()
    assert_event(relax_pile(pile), size=0, area=0, duration=0)
    assert np.array_equal(pile, before)
    event = add_grain_and_relax(pile, np.random.default_rng(1), site=(1, 1))
    expected = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert np.array_equal(pile, expected)
    assert_event(event, size=1, area=1, duration=1)

    pile = np.zeros((3, 3), dtype=np.int64)
    event = add_grain_and_relax(pile, np.random.default_rng(1), site=(1, 1))
    assert_event(event, size=0, area=0, duration=0)
    assert event["trigger"] == (1, 1)

    cases = [
        ("interior", (1, 1), 0, np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])),
        ("edge", (0, 1), 1, np.array([[1, 0, 1], [0, 1, 0], [0, 0, 0]])),
        ("corner", (0, 0), 2, np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]])),
    ]
    figure, axes = plt.subplots(3, 2, figsize=(7.3, 7.6), constrained_layout=True)
    colour_map = ListedColormap(["#f5f0e6", "#edc17f", "#e78542", "#823c34", "#8656a3"])
    colour_scale = BoundaryNorm(np.arange(-0.5, 5.5), colour_map.N, clip=True)
    for row, (name, site, expected_loss, expected) in enumerate(cases):
        pile = np.zeros((3, 3), dtype=np.int64)
        pile[site] = 4
        before = pile.copy()
        event = relax_pile(pile)
        assert np.array_equal(pile, expected)
        assert before.sum() - pile.sum() == expected_loss
        assert_event(event, size=1, area=1, duration=1)
        for column, state in enumerate((before, pile)):
            axis = axes[row, column]
            image = axis.imshow(state, cmap=colour_map, norm=colour_scale)
            axis.set_xticks(range(3))
            axis.set_yticks(range(3))
            axis.tick_params(labelsize=11)
            axis.set_title(f"{name.capitalize()}: " + (
                "before" if column == 0 else f"after; loss = {expected_loss}"
            ), fontsize=12)
            axis.add_patch(Rectangle((site[1] - 0.5, site[0] - 0.5), 1, 1,
                                     fill=False, edgecolor="#152544", linewidth=2.3))
            for x, y in np.ndindex(state.shape):
                axis.text(y, x, str(state[x, y]), ha="center", va="center",
                          fontsize=14, color="white" if state[x, y] >= 3 else "#152544")
        print(f"  {name.capitalize()}: site {site} loses four; "
              f"{4 - expected_loss} grains reach neighbours, {expected_loss} leave.")
    colour_bar = figure.colorbar(image, ax=axes, ticks=range(5), shrink=0.75, pad=0.025)
    colour_bar.ax.set_yticklabels(["0", "1", "2", "3", "4+: unstable"])
    colour_bar.ax.tick_params(labelsize=11)
    colour_bar.set_label("Load at each site", fontsize=12)
    print("  Threshold: load 3 stays stable; one added grain triggers load 4.")
    show_figure("Code check 1: Before and after one toppling; outlined site topples", figure)


def check_known_small_cases():
    verification_section(2, "Reproduce the five known small cases")

    notebook = json.loads(NOTEBOOK.read_text())
    reference_cell = next(cell for cell in notebook["cells"]
                          if cell.get("id") == "week08-validation-task")
    reference_rows = [line for line in reference_cell["source"] if "`[[" in line]
    assert len(reference_rows) == 5, "Expected five student reference cases"
    for row in reference_rows:
        name, starting, final, counts, loss = [
            part.strip() for part in row.split("|")[1:-1]
        ]
        initial = np.array(ast.literal_eval(starting.strip("`")), dtype=np.int64)
        expected = np.array(ast.literal_eval(final.strip("`")), dtype=np.int64)
        size, area, duration = ast.literal_eval(counts.strip("`"))
        expected_event = {"size": size, "area": area, "duration": duration}
        expected_loss = int(loss)
        traced_pile, trace = trace_parallel_relaxation(initial)
        assert np.array_equal(traced_pile, expected), f"{name}: reference pile differs"
        assert event_from_trace(trace) == expected_event, f"{name}: reference counts differ"
        assert sum(step["loss"] for step in trace) == expected_loss
        for order in ("forward", "reverse"):
            pile = initial.copy()
            event = relax_pile(pile, site_order=order)
            assert np.array_equal(pile, expected), f"{name}: final pile differs"
            assert event == expected_event, f"{name}: event measurements differ"
            assert initial.sum() - pile.sum() == expected_loss
        print(f"  {name}: (S, A_av, T) = {size, area, duration}; "
              f"loss = {expected_loss}. Final pile and both orders match.")

    # Further cases: a two-step cascade and two simultaneous interior sites.
    pile = np.zeros((5, 5), dtype=np.int64)
    pile[2, 2] = 4
    pile[2, 3] = 3
    event = relax_pile(pile)
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ])
    assert np.array_equal(pile, expected)
    assert_event(event, size=2, area=2, duration=2)
    assert pile.sum() == 7
    assert pile.max() < 4

    initial = np.zeros((5, 5), dtype=np.int64)
    initial[2, 2:4] = 4
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ])
    for order in ("forward", "reverse"):
        pile = initial.copy()
        event = relax_pile(pile, site_order=order)
        assert np.array_equal(pile, expected)
        assert_event(event, size=2, area=2, duration=1)

    initial = np.random.default_rng(82).integers(0, 10, size=(8, 8), dtype=np.int64)
    forward, reverse = initial.copy(), initial.copy()
    event_forward = relax_pile(forward, site_order="forward")
    event_reverse = relax_pile(reverse, site_order="reverse")
    assert np.array_equal(forward, reverse)
    assert event_forward == event_reverse
    assert forward.max() < 4
    print("  Further cases: cascade, simultaneous interior topplings and "
          "an overfull 8×8 pile also match.")


def check_avalanche_trace():
    verification_section(3, "Reconstruct measurements from an avalanche trace")

    repeated = np.zeros((3, 3), dtype=np.int64)
    repeated[1, 1] = 8
    simultaneous = np.zeros((5, 5), dtype=np.int64)
    simultaneous[2, 2:4] = 4
    cascade = np.zeros((5, 5), dtype=np.int64)
    cascade[2, 2] = 4
    cascade[2, 3] = 3
    cases = (("Repeated toppling", repeated),
             ("Two simultaneous sites", simultaneous), ("Cascade", cascade))
    figure, axes = plt.subplots(3, 3, figsize=(9.2, 8), constrained_layout=True)
    colour_map = ListedColormap([
        "#f5f0e6", "#edc17f", "#e78542", "#823c34", "#8656a3",
        "#774c94", "#694286", "#5d3679", "#512c6d",
    ])
    colour_scale = BoundaryNorm(np.arange(-0.5, 9.5), colour_map.N)
    for row, (name, initial) in enumerate(cases):
        expected_pile, independent_trace = trace_parallel_relaxation(initial)
        expected_event = event_from_trace(independent_trace)
        for order in ("forward", "reverse"):
            observed_pile, event, trace, individual_updates = trace_supplied_relaxation(
                initial, site_order=order,
            )
            unlogged_pile = initial.copy()
            unlogged_event = relax_pile(unlogged_pile, site_order=order)
            assert np.array_equal(observed_pile, unlogged_pile)
            assert np.array_equal(observed_pile, expected_pile)
            assert event == unlogged_event == expected_event
            assert len(trace) == len(independent_trace)
            for observed, independent in zip(trace, independent_trace):
                assert set(observed["sites"]) == set(independent["sites"])
                assert observed["loss"] == independent["loss"]
                assert np.array_equal(observed["before"], independent["before"])
                assert np.array_equal(observed["after"], independent["after"])
            observed_sites = {update["site"] for update in individual_updates}
            observed_steps = {update["k"] for update in individual_updates}
            assert event == {"size": len(individual_updates),
                             "area": len(observed_sites), "duration": len(observed_steps)}
            print(f"  {name}, {order} order:")
            for update in individual_updates:
                print(f"    k={update['k']}: site {update['site']} topples; "
                      f"loss={update['loss']}; before/after piles recorded.")
            print(f"    Counted (S, A_av, T) = "
                  f"{event['size'], event['area'], event['duration']}; "
                  "matches the unlogged function and whole-lattice check.")
            if order == "forward":
                states = [initial] + [wave["after"] for wave in trace]
                for column, axis in enumerate(axes[row]):
                    if column >= len(states):
                        axis.set_visible(False)
                        continue
                    state = states[column]
                    image = axis.imshow(state, cmap=colour_map, norm=colour_scale)
                    axis.set_xticks(range(state.shape[1]))
                    axis.set_yticks(range(state.shape[0]))
                    axis.tick_params(labelsize=10)
                    axis.set_title("Initial" if column == 0 else f"After k={column}",
                                   fontsize=12)
                    if column == 0:
                        axis.set_ylabel(name, fontsize=12)
                    if column < len(trace):
                        for x, y in trace[column]["sites"]:
                            axis.add_patch(Rectangle((y - 0.5, x - 0.5), 1, 1,
                                                     fill=False, edgecolor="#152544",
                                                     linewidth=2))
                    for x, y in np.ndindex(state.shape):
                        axis.text(y, x, str(state[x, y]), ha="center", va="center",
                                  fontsize=12,
                                  color="white" if state[x, y] >= 3 else "#152544")
        assert initial.sum() == expected_pile.sum() + sum(
            step["loss"] for step in independent_trace
        )
    colour_bar = figure.colorbar(image, ax=axes, ticks=range(9), shrink=0.8, pad=0.02)
    colour_bar.ax.tick_params(labelsize=11)
    colour_bar.set_label("Load at each site; loads 4–8 are unstable", fontsize=12)
    show_figure("Code check 3: Parallel steps; outlined sites topple in the next step", figure)


def check_short_recorded_run():
    verification_section(4, "Rebuild a short run and check its records")

    initial = np.zeros((8, 8), dtype=np.int64)
    initial_before = initial.copy()
    settings = dict(L=8, additions=800, burn_in=200, seed=88, initial=initial)
    run_1 = run_sandpile(**settings)
    run_2 = run_sandpile(**settings)
    assert np.array_equal(initial, initial_before)
    assert np.array_equal(run_1["pile"], run_2["pile"])
    assert run_1["recorded_additions"] == 600
    for key in ("size", "area", "duration", "mean_load"):
        assert len(run_1[key]) == 600
        assert np.array_equal(run_1[key], run_2[key])
    assert np.all(run_1["size"] >= run_1["area"])
    assert np.all(run_1["size"] >= run_1["duration"])
    assert np.array_equal(run_1["size"] == 0, run_1["area"] == 0)
    assert np.array_equal(run_1["size"] == 0, run_1["duration"] == 0)
    assert run_1["pile"].max() < 4
    assert np.all((run_1["mean_load"] >= 0) & (run_1["mean_load"] <= 3))
    assert run_1["mean_load"][-1] == run_1["pile"].mean()
    assert np.any(run_1["size"] == 0)

    run = run_sandpile(L=1, additions=9, burn_in=2, seed=88)
    expected = np.array([0, 1, 0, 0, 0, 1, 0])
    assert run["recorded_additions"] == 7
    for key in ("size", "area", "duration"):
        assert np.array_equal(run[key], expected)
    assert run["pile"][0, 0] == 1

    actual_rng, expected_rng = np.random.default_rng(128), np.random.default_rng(128)
    pile = np.zeros((5, 5), dtype=np.int64)
    for _ in range(30):
        expected_site = tuple(expected_rng.integers(0, 5, size=2))
        event = add_grain_and_relax(pile, actual_rng)
        assert event["trigger"] == expected_site

    # Dense but stable: the record contains unequal S, A_av and T.
    initial = np.full((5, 5), 3, dtype=np.int64)
    initial_before = initial.copy()
    manual_pile = initial.copy()
    manual_rng = np.random.default_rng(129)
    manual_records = {key: [] for key in ("size", "area", "duration", "mean_load")}
    additions, burn_in = 70, 10
    for trial in range(additions):
        event = add_grain_and_relax(manual_pile, manual_rng)
        if trial >= burn_in:
            for key in ("size", "area", "duration"):
                manual_records[key].append(event[key])
            manual_records["mean_load"].append(manual_pile.mean())
    recorded = run_sandpile(
        L=5, additions=additions, burn_in=burn_in, seed=129, initial=initial,
    )
    assert np.array_equal(initial, initial_before)
    assert recorded["recorded_additions"] == additions - burn_in
    assert np.array_equal(recorded["pile"], manual_pile)
    for key, values in manual_records.items():
        assert np.array_equal(recorded[key], np.asarray(values)), f"Recorded {key} differs"
    assert np.any(recorded["size"] != recorded["area"])
    assert np.any(recorded["area"] != recorded["duration"])
    print("  70 individual trials: all 60 post-burn-in records and final pile match.")
    print("  Seeded addition sites, inclusion of no-toppling trials, omission of burn-in "
          "trials, repeatability and unchanged input checked.")
    return run_1


def check_small_ensemble():
    verification_section(5, "Compare ensemble members with their requested seeds")

    check_seeds = (130, 131, 132)
    check_settings = dict(L=5, additions=120, burn_in=20)
    # This tiny check needs no progress display; the simulation code is unchanged.
    progress_display = ns["tqdm"]
    ns["tqdm"] = lambda values, **kwargs: values
    try:
        small_ensemble = run_sandpile_ensemble(
            check_seeds, description="Seed correspondence check", **check_settings,
        )
    finally:
        ns["tqdm"] = progress_display
    assert len(small_ensemble) == len(check_seeds)
    for seed, member in zip(check_seeds, small_ensemble):
        individual = run_sandpile(seed=seed, **check_settings)
        assert member["recorded_additions"] == individual["recorded_additions"]
        for key in ("pile", "size", "area", "duration", "mean_load"):
            assert np.array_equal(member[key], individual[key]), f"Seed {seed}: {key} differs"
        print(f"  Seed {seed}: every recorded field and final pile match its individual run.")
    assert not np.array_equal(small_ensemble[0]["size"], small_ensemble[1]["size"])
    print("  Different seeds produce different histories.")


def check_optional_diagnostics(short_run):
    section("Optional: further down the ladder — boundary account and one CCDF point")

    initial = np.zeros((3, 3), dtype=np.int64)
    initial[0, 0:2] = 3
    loaded = initial.copy()
    loaded[0, 1] += 1
    expected_pile, trace = trace_parallel_relaxation(loaded)
    assert [step["sites"] for step in trace] == [[(0, 1)], [(0, 0)]]
    assert [step["loss"] for step in trace] == [1, 2]
    assert initial.sum() + 1 == expected_pile.sum() + sum(
        step["loss"] for step in trace
    )
    pile = initial.copy()
    event = add_grain_and_relax(pile, np.random.default_rng(1), site=(0, 1))
    assert np.array_equal(pile, expected_pile)
    assert {key: event[key] for key in ("size", "area", "duration")} == event_from_trace(trace)
    assert pile.max() < 4
    print("  Edge-to-corner cascade: loss 1 then 2; load before + 1 = load after + 3.")

    x, probability = empirical_ccdf(np.array([0, 1, 1, 3]))
    assert np.array_equal(x, np.array([1, 3]))
    assert np.allclose(probability, np.array([1.0, 1.0 / 3.0]))

    short_runs = [short_run] + [
        run_sandpile(L=8, additions=800, burn_in=200, seed=seed)
        for seed in (89, 90, 91)
    ]
    pooled = np.concatenate([run["size"] for run in short_runs])
    non_zero = np.sort(pooled[pooled > 0])
    threshold = int(non_zero[95 * len(non_zero) // 100])
    counts = np.array([np.count_nonzero(run["size"] >= threshold) for run in short_runs])
    numerator = int(counts.sum())
    denominator = sum(np.count_nonzero(run["size"] > 0) for run in short_runs)
    contributing_runs = int(np.count_nonzero(counts))
    x, probability = empirical_ccdf(pooled)
    index = np.searchsorted(x, threshold)
    assert x[index] == threshold
    assert np.isclose(probability[index], numerator / denominator)
    assert 0 < contributing_runs <= len(short_runs)
    print(f"  CCDF point at S >= {threshold}: {numerator}/{denominator} non-zero events, "
          f"from {contributing_runs}/{len(short_runs)} runs; direct count matches.")


def run_verification_checks():
    """Check starting options, follow the five student checks, then optional diagnostics."""
    check_starting_piles()
    check_individual_topplings()
    check_known_small_cases()
    check_avalanche_trace()
    short_run = check_short_recorded_run()
    check_small_ensemble()
    check_optional_diagnostics(short_run)
    print("\nAll reference verification checks passed.")


run_verification_checks()

if "--checks-only" in sys.argv:
    if "ipykernel" not in sys.modules:
        plt.show()
    raise SystemExit(0)


# %% Investigation settings
# Match "Investigation" and "How many runs are enough?" in the student notebook.
lattice_sizes = (16, 24, 32)
initial_runs = 20
batch_size = 10
max_runs = 60
recorded_additions = 1_500
confidence = 0.90
relative_interval_width_target = 0.05  # Full interval width / absolute mean.
minimum_runs_for_precision_check = initial_runs
initial_only = "--initial-only" in sys.argv
compare_100_runs = "--100-runs" in sys.argv


def run_tail_percentile(run):
    """Size exceeded by about 5% of one run's non-zero avalanches."""
    non_zero = run["size"][run["size"] > 0]
    return np.quantile(non_zero, 0.95) if non_zero.size else 0.0


def precision_checkpoints(run_count, minimum_runs=20):
    """Early prefixes, followed by the batches actually run."""
    if run_count < 1 or minimum_runs < 1:
        raise ValueError("Run counts must be positive")
    counts = {count for count in (5, 10, 15, minimum_runs) if count <= run_count}
    counts.update(range(minimum_runs + 10, run_count + 1, 10))
    counts.add(run_count)
    return np.array(sorted(counts), dtype=int)


def relative_interval_width(mean, interval):
    """Full interval width / |mean|; undefined precision is infinite."""
    interval = np.asarray(interval, dtype=float)
    if (interval.shape != (2,) or not np.isfinite(mean) or mean == 0
            or not np.all(np.isfinite(interval)) or interval[1] < interval[0]):
        return np.inf
    return (interval[1] - interval[0]) / abs(mean)


def precision_target_met(mean, interval, run_count, target, minimum_runs=20):
    """Check the interval-width target; confirmation needs another batch."""
    width = relative_interval_width(mean, interval)
    return bool(run_count >= minimum_runs and np.isfinite(width) and width <= target)


def precision_record(L, values, confidence=0.90):
    values = np.asarray(values, dtype=float)
    interval = mean_interval(values, confidence=confidence, seed=3024 + L + len(values))
    mean = values.mean()
    return {
        "mean": mean,
        "interval": interval,
        "relative_width": relative_interval_width(mean, interval),
        "relative_spread": values.std(ddof=1) / abs(mean) if mean != 0 else np.inf,
    }


def tail_counts(runs, threshold):
    """Count events and independent contributors above one fixed threshold."""
    positive_count = sum(np.count_nonzero(run["size"] > 0) for run in runs)
    counts = np.array([np.count_nonzero(run["size"] >= threshold) for run in runs])
    largest = max(int(run["size"].max()) for run in runs)
    largest_counts = np.array([np.count_nonzero(run["size"] == largest) for run in runs])
    x, probability = empirical_ccdf(np.concatenate([run["size"] for run in runs]))
    index = np.searchsorted(x, threshold)
    measured = probability[index] if index < len(x) else 0.0
    assert np.isclose(measured, counts.sum() / positive_count)
    return {
        "threshold": threshold,
        "events": int(counts.sum()),
        "positive_events": int(positive_count),
        "contributing_runs": int(np.count_nonzero(counts)),
        "largest": largest,
        "largest_events": int(largest_counts.sum()),
        "largest_contributing_runs": int(np.count_nonzero(largest_counts)),
    }


# %% Run the protocol once; reuse these records for every question and plot.
def run_ensemble_investigation():
    ensembles, records, decisions, thresholds = {}, {}, {}, {}
    initial_tails, final_tails = {}, {}
    section("Run the investigation: initial ensembles and fresh batches")
    print(f"L={lattice_sizes}; {recorded_additions} recorded trials per run; "
          f"budget={max_runs} runs per L.")
    started = time.perf_counter()
    for L in lattice_sizes:
        burn_in = 8 * L**2
        seed_start = 10_000 + 100 * L
        runs = run_sandpile_ensemble(
            np.arange(initial_runs) + seed_start,
            L=L, additions=burn_in + recorded_additions, burn_in=burn_in,
            description=f"Initial ensemble L={L}",
        )
        ensembles[L] = runs
        values = np.array([run_tail_percentile(run) for run in runs])
        records[L] = {
            int(count): precision_record(L, values[:count], confidence)
            for count in precision_checkpoints(len(runs), initial_runs)
        }
        positive = np.concatenate([run["size"][run["size"] > 0] for run in runs])
        thresholds[L] = int(np.ceil(np.quantile(positive, 0.995)))
        initial_tails[L] = tail_counts(runs, thresholds[L])
        first_crossing = pending_crossing = confirmed_count = None
        while True:
            count = len(runs)
            record = records[L][count]
            met = precision_target_met(
                record["mean"], record["interval"], count,
                relative_interval_width_target, initial_runs,
            )
            if met:
                if first_crossing is None:
                    first_crossing = count
                if pending_crossing is not None:
                    confirmed_count = count
                pending_crossing = count
            else:
                pending_crossing = None
            print(f"  L={L}: {count} runs completed; "
                  f"interval width={100 * record['relative_width']:.2f}% of mean.")
            if initial_only or confirmed_count is not None or count >= max_runs:
                break
            fresh_seeds = np.arange(count, min(count + batch_size, max_runs)) + seed_start
            runs.extend(run_sandpile_ensemble(
                fresh_seeds,
                L=L, additions=burn_in + recorded_additions, burn_in=burn_in,
                description=f"Fresh batch L={L}",
            ))
            values = np.array([run_tail_percentile(run) for run in runs])
            records[L][len(runs)] = precision_record(L, values, confidence)
        decisions[L] = {
            "first_crossing": first_crossing,
            "confirmed_count": confirmed_count,
            "target_met": met,
            "budget_exhausted": len(runs) >= max_runs and confirmed_count is None,
        }
        final_tails[L] = tail_counts(runs, thresholds[L])
    print(f"Protocol completed in {time.perf_counter() - started:.1f} s.")
    return ensembles, records, decisions, thresholds, initial_tails, final_tails


def run_precision_comparison(ensembles, records, run_count=100):
    """Extend the same seed sequence for an optional fixed-count comparison."""
    if run_count < max(len(runs) for runs in ensembles.values()):
        raise ValueError("Comparison count must include all existing runs")
    section(f"Optional instructor comparison: {run_count} independent runs at each L")
    print("Same burn-in, record length, confidence and target; earlier stopping counts unchanged.")
    comparison_ensembles = {L: list(runs) for L, runs in ensembles.items()}
    comparison_records = {L: dict(checkpoints) for L, checkpoints in records.items()}
    for L, runs in comparison_ensembles.items():
        burn_in = 8 * L**2
        seed_start = 10_000 + 100 * L
        original_count = len(runs)
        while len(runs) < run_count:
            start = len(runs)
            seeds = np.arange(start, min(start + batch_size, run_count)) + seed_start
            runs.extend(run_sandpile_ensemble(
                seeds, L=L, additions=burn_in + recorded_additions, burn_in=burn_in,
                description=f"Optional comparison L={L}: {start}->{start + len(seeds)} runs",
            ))
            for run in runs[start:]:
                assert run["recorded_additions"] == recorded_additions
                assert run["pile"].max() < 4
                for field in ("size", "area", "duration", "mean_load"):
                    assert len(run[field]) == recorded_additions
            values = np.array([run_tail_percentile(run) for run in runs])
            comparison_records[L][len(runs)] = precision_record(L, values, confidence)
        before = records[L][original_count]
        after = comparison_records[L][run_count]
        print(f"  L={L}, {original_count}->{run_count} runs: mean "
              f"{before['mean']:.1f}->{after['mean']:.1f}; width "
              f"{100 * before['relative_width']:.2f}%->{100 * after['relative_width']:.2f}%.")
    return comparison_ensembles, comparison_records


def report_protocol_checks(ensembles):
    section("Investigation protocol: records, stability and loading drift")
    for L, runs in ensembles.items():
        for run in runs:
            assert run["recorded_additions"] == recorded_additions
            assert run["pile"].max() < 4
            for field in ("size", "area", "duration", "mean_load"):
                assert len(run[field]) == recorded_additions
        load_changes = np.array([
            run["mean_load"][recorded_additions // 2:].mean()
            - run["mean_load"][:recorded_additions // 2].mean()
            for run in runs
        ])
        print(f"  L={L}: burn-in={8 * L**2}; mean-load change between record halves="
              f"{load_changes.mean():+.4f}, range "
              f"{load_changes.min():+.4f} to {load_changes.max():+.4f}.")
    print("Inspect consistent loading drift; extend burn-in and rerun if needed.")


# %% The three plots requested under "Investigation".
def plot_time_series(ensembles):
    L = max(lattice_sizes)
    shown_runs = ensembles[L][:4]
    window = min(500, recorded_additions)
    fig, axes = plt.subplots(len(shown_runs), 1, figsize=(10, 6), sharex=True)
    for index, (axis, run) in enumerate(zip(axes, shown_runs), start=1):
        axis.plot(np.arange(1, window + 1), run["size"][:window], lw=0.8)
        axis.set_yscale("symlog", linthresh=1)
        axis.set_ylabel(f"run {index}\n$S_n$")
    axes[-1].set_xlabel("recorded grain addition, $n$")
    fig.suptitle(f"Independent avalanche-size records at $L={L}$")
    fig.tight_layout()
    return fig


def plot_run_summaries(ensembles, records):
    fig, axis = plt.subplots(figsize=(7, 4.5))
    rng = np.random.default_rng(3024)
    means, lower, upper = [], [], []
    for L in lattice_sizes:
        runs = ensembles[L]
        values = np.array([run_tail_percentile(run) for run in runs])
        jitter = rng.normal(0, 0.18, size=len(values))
        axis.scatter(L + jitter, values, alpha=0.65, s=28,
                     label="run" if L == lattice_sizes[0] else None)
        final = records[L][len(runs)]
        means.append(final["mean"])
        lower.append(final["mean"] - final["interval"][0])
        upper.append(final["interval"][1] - final["mean"])
    axis.errorbar(
        lattice_sizes, means, yerr=np.array([lower, upper]),
        color="black", marker="o", capsize=4, lw=1.5,
        label=f"mean and {100 * confidence:g}% confidence interval",
    )
    axis.set_xlabel("lattice width, $L$")
    axis.set_ylabel("Run-level 95th percentile of non-zero $S$")
    axis.legend(loc="upper left", bbox_to_anchor=(0, 1.19), frameon=False, fontsize=10)
    fig.tight_layout()
    return fig


def plot_ccdfs(ensembles):
    fig, axis = plt.subplots(figsize=(7, 5))
    for L in lattice_sizes:
        sizes = np.concatenate([run["size"] for run in ensembles[L]])
        x, probability = empirical_ccdf(sizes)
        axis.loglog(x, probability, marker=".", linestyle="none",
                    label=f"$L={L}$ ({len(ensembles[L])} runs)")
    axis.set_xlabel("avalanche-size threshold, $s$ (topplings)")
    axis.set_ylabel(r"$\Pr(S\geq s\mid S>0)$")
    axis.legend(frameon=False, fontsize=11)
    fig.tight_layout()
    return fig


def plot_ensemble_precision(values_by_size, target=0.05, minimum_runs=20,
                            confidence=0.90, records=None, decisions=None,
                            comparison=False):
    """Show the estimates, interval widths and observed confirmation decisions."""
    if not np.isfinite(target) or target <= 0:
        raise ValueError("Choose a positive finite relative interval-width target")
    if not values_by_size:
        raise ValueError("Provide at least one lattice size")
    fig, axes = plt.subplots(
        2, len(values_by_size), figsize=(12, 7), sharex="col", squeeze=False,
    )
    diagnostics = {}
    for column, (L, values) in enumerate(values_by_size.items()):
        values = np.asarray(values, dtype=float)
        if values.ndim != 1 or values.size == 0:
            raise ValueError("Each lattice size needs a non-empty array of run summaries")
        checkpoints = records[L] if records is not None else {
            int(count): precision_record(L, values[:count], confidence)
            for count in precision_checkpoints(len(values), minimum_runs)
        }
        counts = np.array(sorted(checkpoints))
        means = np.array([checkpoints[count]["mean"] for count in counts])
        intervals = np.array([checkpoints[count]["interval"] for count in counts])
        relative_widths = np.array([checkpoints[count]["relative_width"] for count in counts])
        met = precision_target_met(means[-1], intervals[-1], counts[-1], target, minimum_runs)
        diagnostics[L] = {
            "run_counts": counts, "means": means, "intervals": intervals,
            "relative_widths": relative_widths, "target_met": met,
        }
        decision = decisions.get(L, {}) if decisions is not None else {}
        confirmed_count = decision.get("confirmed_count")
        confirmed = confirmed_count is not None
        top, bottom = axes[:, column]
        top.plot(counts, means, marker="o", label="mean")
        top.fill_between(
            counts, intervals[:, 0], intervals[:, 1], alpha=0.2,
            label=f"{100 * confidence:g}% confidence interval",
        )
        top.set_title(f"$L={L}$")
        plotted_widths = np.where(np.isfinite(relative_widths), 100 * relative_widths, np.nan)
        bottom.plot(counts, plotted_widths, marker="o", label="full interval width")
        bottom.axhline(
            100 * target, color="tab:orange", ls="--", lw=1.5,
            label=f"Chosen target: {100 * target:g}% full width",
        )
        if np.isfinite(plotted_widths[-1]):
            bottom.scatter(
                counts[-1], plotted_widths[-1], s=65,
                color="tab:blue", zorder=3,
            )
        if confirmed:
            index = int(np.flatnonzero(counts == confirmed_count)[0])
            bottom.scatter(confirmed_count, plotted_widths[index], s=65,
                           color="tab:green", zorder=4,
                           label="Another batch confirmed target")
        first = decision.get("first_crossing")
        if first is not None:
            index = int(np.flatnonzero(counts == first)[0])
            bottom.scatter(first, plotted_widths[index], s=90,
                           facecolors="none", edgecolors="tab:orange", zorder=4,
                           label="First assessed batch meeting target")
        status = "confirmed" if confirmed else ("meets target; unconfirmed" if met else "target unmet")
        if comparison:
            status = "comparison; meets target" if met else "comparison; target unmet"
        if counts[-1] < minimum_runs:
            status = "exploratory"
        bottom.set_title(f"{counts[-1]} runs: {status}", loc="left", fontsize=11)
        bottom.set_xlabel("independent runs")
        ticks = counts
        if len(counts) > 8:
            ticks = sorted({int(counts[0]), minimum_runs, int(counts[-1]),
                            *range(40, int(counts[-1]) + 1, 20),
                            *[int(count) for count in (first, confirmed_count) if count is not None]})
        bottom.set_xticks(ticks)
        bottom.grid(axis="y", alpha=0.2)
    finite_widths = np.concatenate([
        100 * item["relative_widths"][np.isfinite(item["relative_widths"])]
        for item in diagnostics.values()
    ])
    upper = max(100 * target * 2, finite_widths.max() if finite_widths.size else 0) * 1.2
    for bottom in axes[1]:
        bottom.set_ylim(0, upper)
    axes[0, 0].set_ylabel("Mean run-level 95th percentile\nof non-zero $S$")
    axes[1, 0].set_ylabel(f"Full {100 * confidence:g}% interval width\n(% of absolute mean)")
    axes[0, 0].legend(frameon=False, fontsize=10)
    legend_items = {}
    for bottom in axes[1]:
        handles, labels = bottom.get_legend_handles_labels()
        legend_items.update(zip(labels, handles))
    fig.legend(legend_items.values(), legend_items.keys(), loc="lower center",
               ncol=2, frameon=False, fontsize=10)
    fig.tight_layout(rect=(0, 0.09, 1, 1))
    return fig, diagnostics


# %% "How many runs are enough?" — answers follow the seven student questions.
def report_precision_questions(ensembles, records, decisions):
    section("How many runs? Q1: What precision is useful, and why?")
    print("Quantity: mean of the run-level 95th percentiles of non-zero avalanche sizes.")
    print(f"Example choice: {100 * confidence:g}% confidence; "
          f"{100 * relative_interval_width_target:g}% full interval width relative to the mean.")
    print(f"A {100 * relative_interval_width_target:g}% full width is about "
          f"+/-{50 * relative_interval_width_target:g}% of the mean. Compare this with "
          "the differences between lattice summaries when judging useful precision.")

    section("How many runs? Q2: Which lattice sizes meet the target at 20 runs?")
    for L in lattice_sizes:
        record = records[L][initial_runs]
        met = precision_target_met(record["mean"], record["interval"], initial_runs,
                                   relative_interval_width_target, initial_runs)
        print(f"  L={L}: mean={record['mean']:.1f}; width="
              f"{100 * record['relative_width']:.2f}%; "
              f"{'meets target' if met else 'target unmet'}.")
    print("Check the interval even if the mean barely moves.")

    section("How many runs? Q3: What changes after 10 fresh runs?")
    for L in lattice_sizes:
        counts = sorted(count for count in records[L] if count >= initial_runs)
        if len(counts) == 1:
            print(f"  L={L}: fresh batches omitted by --initial-only.")
        for before, after in zip(counts, counts[1:]):
            old, new = records[L][before], records[L][after]
            met = precision_target_met(new["mean"], new["interval"], after,
                                       relative_interval_width_target, initial_runs)
            print(f"  L={L}, {before}->{after} runs: mean {old['mean']:.1f}->{new['mean']:.1f}; "
                  f"width {100 * old['relative_width']:.2f}%->"
                  f"{100 * new['relative_width']:.2f}%; "
                  f"{'meets target' if met else 'target unmet'}.")

    section("How many runs? Q4: How does the required run count change with L?")
    for L in lattice_sizes:
        decision = decisions[L]
        final = records[L][len(ensembles[L])]
        first, confirmed = decision["first_crossing"], decision["confirmed_count"]
        print(f"  L={L}: first assessed count meeting target="
              f"{first if first is not None else 'none'}; confirmed total="
              f"{confirmed if confirmed is not None else 'none'}; "
              f"final spread between run summaries (SD/mean)="
              f"{100 * final['relative_spread']:.2f}%.")
        if decision["budget_exhausted"]:
            print(f"    {max_runs}-run budget reached; target or confirmation remains unmet.")
    print("Confidence, relative target and record length are the same at every L. "
          "Larger spread relative to the mean generally needs more runs.")
    print("Precision decisions start at 20 runs; smaller plotted counts are prefixes "
          "of that initial batch.")


def report_tail_questions(ensembles, initial_tails, final_tails):
    section("How many runs? Q5: How many events and independent runs support the far tail?")
    print("Each threshold comes from the initial ensemble's upper 0.5% and stays fixed.")
    for L in lattice_sizes:
        before, after = initial_tails[L], final_tails[L]
        print(f"  L={L}, S>={after['threshold']}: initial {before['events']}/"
              f"{before['positive_events']} events from {before['contributing_runs']}/"
              f"{initial_runs} runs; final {after['events']}/{after['positive_events']} "
              f"events from {after['contributing_runs']}/{len(ensembles[L])} runs.")

    section("How many runs? Q6: Does the percentile target also check the largest avalanches?")
    for L in lattice_sizes:
        tail = final_tails[L]
        print(f"  L={L}: largest observed S={tail['largest']}; "
              f"{tail['largest_events']} event(s) from "
              f"{tail['largest_contributing_runs']}/{len(ensembles[L])} runs.")
    print("The precision target checks the mean run-level percentile. "
          "These contributor counts show how little data may support the observed maximum.")


def check_record_length(ensembles):
    section("How many runs? Q7: Do longer records change the percentiles?")
    if initial_only and "--record-length-check" not in sys.argv:
        print("Omitted by --initial-only; add --record-length-check to include it.")
        return []
    L = max(lattice_sizes)
    seeds = np.arange(4) + 10_000 + 100 * L
    burn_in = 8 * L**2
    longer_runs = run_sandpile_ensemble(
        seeds, L=L, additions=burn_in + 2 * recorded_additions,
        burn_in=burn_in, description=f"Record-length check L={L}",
    )
    print(f"Same four seeds at L={L}, same burn-in: "
          f"{recorded_additions} versus {2 * recorded_additions} recorded trials.")
    results = []
    for seed, short, longer in zip(seeds, ensembles[L], longer_runs):
        for field in ("size", "area", "duration", "mean_load"):
            assert np.array_equal(short[field], longer[field][:recorded_additions])
        old, new = run_tail_percentile(short), run_tail_percentile(longer)
        change = new - old
        results.append({"seed": int(seed), "short": old, "long": new, "change": change})
        print(f"  Seed {seed}: percentile {old:.1f}->{new:.1f}; "
              f"change={100 * change / old:+.1f}%.")
    changes = np.array([100 * result["change"] / result["short"] for result in results])
    print(f"Four-seed changes range from {changes.min():+.1f}% to {changes.max():+.1f}%. "
          "Extend this check if those changes affect your conclusion.")
    return results


def report_conclusion(ensembles, records, decisions, tails):
    section("Interpret the comparison / What can you conclude?")
    means = np.array([records[L][len(ensembles[L])]["mean"] for L in lattice_sizes])
    maxima = np.array([tails[L]["largest"] for L in lattice_sizes])
    if np.all(np.diff(means) > 0) and np.all(np.diff(maxima) > 0):
        print("Both the mean run-level percentile and largest observed avalanche increase with L.")
    for L in lattice_sizes:
        final = records[L][len(ensembles[L])]
        print(f"  L={L}: {len(ensembles[L])} runs; mean={final['mean']:.1f}; "
              f"interval=[{final['interval'][0]:.1f}, {final['interval'][1]:.1f}]; "
              f"{'target confirmed' if decisions[L]['confirmed_count'] else 'not confirmed'}.")
    print("Checked: local rules, reference cases, event counts, recording and requested seeds.")
    print("Follow up: loading drift, record-length sensitivity and sparse very large events.")
    print("The observed run counts apply to this quantity, protocol and seed sequence.")


# %% Full instructor run
(ensembles, checkpoint_records, decisions, tail_thresholds,
 initial_tail_diagnostics, tail_diagnostics) = run_ensemble_investigation()
report_protocol_checks(ensembles)
figures = {}
figures["time_series"] = show_figure(
    "Investigation plot 1: four aligned avalanche-size time series",
    plot_time_series(ensembles),
)
figures["run_summaries"] = show_figure(
    "Investigation plot 2: run-level percentiles across L",
    plot_run_summaries(ensembles, checkpoint_records),
)
figures["ccdfs"] = show_figure(
    "Investigation plot 3: CCDFs across L",
    plot_ccdfs(ensembles),
)

report_precision_questions(ensembles, checkpoint_records, decisions)
values_by_size = {
    L: np.array([run_tail_percentile(run) for run in ensembles[L]])
    for L in lattice_sizes
}
precision_figure, precision_diagnostics = plot_ensemble_precision(
    values_by_size, target=relative_interval_width_target,
    minimum_runs=minimum_runs_for_precision_check, confidence=confidence,
    records=checkpoint_records, decisions=decisions,
)
figures["precision"] = show_figure(
    "How many runs? Questions 2-4: estimates and interval widths against the target",
    precision_figure,
)
report_tail_questions(ensembles, initial_tail_diagnostics, tail_diagnostics)
length_diagnostics = check_record_length(ensembles)
report_conclusion(ensembles, checkpoint_records, decisions, tail_diagnostics)
if compare_100_runs:
    comparison_ensembles, comparison_records = run_precision_comparison(
        ensembles, checkpoint_records,
    )
    comparison_values = {
        L: np.array([run_tail_percentile(run) for run in runs])
        for L, runs in comparison_ensembles.items()
    }
    comparison_figure, comparison_diagnostics = plot_ensemble_precision(
        comparison_values, target=relative_interval_width_target,
        minimum_runs=minimum_runs_for_precision_check, confidence=confidence,
        records=comparison_records, decisions=decisions, comparison=True,
    )
    figures["precision_100"] = show_figure(
        "Optional instructor comparison: estimates and interval widths through 100 runs",
        comparison_figure,
    )
if "ipykernel" not in sys.modules:
    plt.show()
