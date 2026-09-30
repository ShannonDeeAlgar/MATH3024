"""Small networked PD laboratory: payoffs fixed, behavioural rules replaceable."""
import numpy as np

C, D = 0, 1


def lattice(side):
    """Four distinct neighbours on a periodic square; no self-interactions."""
    if side < 3:
        raise ValueError('Use side >= 3.')
    ids = np.arange(side * side).reshape(side, side)
    return np.stack([np.roll(ids, 1, 0), np.roll(ids, -1, 0),
                     np.roll(ids, 1, 1), np.roll(ids, -1, 1)], axis=-1).reshape(-1, 4)


def payoff_matrix(temptation=3.4):
    """Rows are own action, columns opponent: C=0, D=1."""
    if temptation <= 3:
        raise ValueError('Strict PD requires T > R=3 > P=1 > S=0.')
    return np.array([[3., 0.], [float(temptation), 1.]])


def scores(state, neighbours, payoffs):
    return payoffs[state[:, None], state[neighbours]].sum(axis=1)


def copy_best(state, totals, neighbours, rng):
    """Copy a maximum-score candidate, including self; break ties uniformly."""
    candidates = np.column_stack([np.arange(len(state)), neighbours])
    values = totals[candidates]
    tied = values == values.max(axis=1, keepdims=True)
    chosen = np.argmax(np.where(tied, rng.random(tied.shape), -1), axis=1)
    return state[candidates[np.arange(len(state)), chosen]].copy()


def copy_one_reference(state, totals, neighbours, rng):
    """Sample one neighbour; copy only if strictly better; ties keep the current action."""
    selected = neighbours[np.arange(len(state)), rng.integers(neighbours.shape[1], size=len(state))]
    return np.where(totals[selected] > totals, state[selected], state).copy()


def initial_state(side=24, fraction_c=0.5, seed=0):
    """Same exact initial C count in each run, independently shuffled positions."""
    if not 0 <= fraction_c <= 1:
        raise ValueError('fraction_c must be in [0, 1].')
    state = np.full(side * side, D, dtype=int)
    state[:round(fraction_c * len(state))] = C
    np.random.default_rng(seed).shuffle(state)
    return state


def simulate(initial, neighbours, rule=copy_best, temptation=3.4, steps=160, seed=1000):
    """Every score and decision uses the same old state; record generation zero."""
    state = np.array(initial, dtype=int, copy=True)
    rng = np.random.default_rng(seed)
    payoffs = payoff_matrix(temptation)
    history = [state.copy()]
    for _ in range(steps):
        totals = scores(state, neighbours, payoffs)
        state = np.asarray(rule(state, totals, neighbours, rng), dtype=int)
        if state.shape != history[0].shape or not np.isin(state, [C, D]).all():
            raise ValueError('The rule must return one C/D action for each agent.')
        history.append(state.copy())
    return np.array(history)


def experiment(rule, temptation=3.4, side=24, steps=160, repeats=12, root_seed=3024):
    """Matched initial configurations across conditions; reproducible update streams."""
    neighbours = lattice(side)
    histories = []
    for run in range(repeats):
        initial = initial_state(side, seed=root_seed + run)
        history = simulate(initial, neighbours, rule, temptation, steps,
                           seed=root_seed + 10000 + run)
        histories.append((history == C).mean(axis=1))
    return np.array(histories)
