"""Small, inspectable Axelrod-style tournament; not the historical entry list.

C=0, D=1. Strategies see completed, realised actions only. Payoffs are
(T,R,P,S)=(5,3,1,0); no discounting, horizon information or inter-match memory.
Only NumPy is required. The companion workshop notebook embeds the
fixed-strategy tournament portion of this source; the population updater is
used by the Reader's optional evolutionary figure.
"""
import numpy as np

STRATEGIES = (
    'Always Cooperate', 'Always Defect', 'Tit for Tat', 'Grudger',
    'Tit for Two Tats', 'Random', 'Win-Stay Lose-Shift',
)


def choose_action(name, own, other, rng):
    """Return an intended action from immutable completed histories."""
    if name == 'Always Cooperate':
        return 0
    if name == 'Always Defect':
        return 1
    if name == 'Random':
        return int(rng.integers(2))
    if name == 'Tit for Tat':
        return other[-1] if other else 0
    if name == 'Grudger':
        return int(1 in other)
    if name == 'Tit for Two Tats':
        return int(len(other) >= 2 and other[-2:] == (1, 1))
    if name == 'Win-Stay Lose-Shift':
        # With these PD payoffs, R and T are satisfactory; P and S are not.
        # Start C, then C after CC or DD, D after CD or DC.
        return int(own[-1] != other[-1]) if own else 0
    raise ValueError(f'Unknown strategy: {name}')


def _positive_integer(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError(f'{name} must be a positive integer')


def play_match(left, right, rounds=200, noise=0.0, seed=0,
               payoffs=(5, 3, 1, 0), forced_flips=()):
    """One simultaneous match; noise independently flips each intended action.

    forced_flips is for controlled demonstrations: (zero-based round, seat).
    A forced flip applies after random noise. Histories reset on every call.
    """
    _positive_integer(rounds, 'rounds')
    if left not in STRATEGIES or right not in STRATEGIES:
        raise ValueError('Unknown strategy')
    if not np.isfinite(noise) or not 0 <= noise <= 1:
        raise ValueError('noise must be between 0 and 1')
    T, R, P, S = payoffs
    if not np.all(np.isfinite(payoffs)) or not T > R > P > S:
        raise ValueError('Payoffs must be finite and satisfy T > R > P > S')
    flips = set(forced_flips)
    if any(not (isinstance(t, int) and 0 <= t < rounds and seat in (0, 1)) for t, seat in flips):
        raise ValueError('Invalid forced flip')
    streams = [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(3)]
    reward = np.array([[[R, R], [S, T]], [[T, S], [P, P]]], dtype=float)
    actions = np.empty((rounds, 2), dtype=np.int8)
    intended = np.empty_like(actions)
    scores = np.empty((rounds, 2))
    histories = [(), ()]
    for t in range(rounds):
        a = choose_action(left, histories[0], histories[1], streams[0])
        b = choose_action(right, histories[1], histories[0], streams[1])
        intended[t] = (a, b)
        actual = intended[t] ^ (streams[2].random(2) < noise).astype(np.int8)
        for seat in (0, 1):
            actual[seat] ^= int((t, seat) in flips)
        actions[t] = actual
        scores[t] = reward[actual[0], actual[1]]
        # Update both histories only after both choices have been made.
        histories = [histories[i] + (int(actual[i]),) for i in (0, 1)]
    return {'actions': actions, 'intended': intended, 'scores': scores,
            'cumulative_scores': scores.cumsum(axis=0),
            'mean_scores': scores.mean(axis=0),
            'cooperation': (actions == 0).mean(axis=0)}


def run_tournament(players=STRATEGIES, rounds=200, repetitions=30,
                   noise=0.0, seed=3024, self_play=True, payoffs=(5, 3, 1, 0)):
    """Round robin; equal opponent weights; one independent match per pair.

    Arrays use [repetition, focal strategy, opponent]. Self-play represents
    two separate copies, averaged into one opponent contribution. Missing
    diagonal entries are NaN when self-play is excluded. Stable pair seeds
    make results invariant to the order of the entrants.
    """
    players = tuple(players)
    _positive_integer(rounds, 'rounds')
    _positive_integer(repetitions, 'repetitions')
    if len(players) < 2 or len(set(players)) != len(players) or any(p not in STRATEGIES for p in players):
        raise ValueError('Use at least two distinct known strategies')
    shape = (repetitions, len(players), len(players))
    payoff = np.full(shape, np.nan)
    cooperation = np.full(shape, np.nan)
    wins = np.full(shape, np.nan)
    for r in range(repetitions):
        for i in range(len(players)):
            for j in range(i if self_play else i + 1, len(players)):
                ids = [STRATEGIES.index(players[i]), STRATEGIES.index(players[j])]
                a, b = sorted(ids)
                pair_seed = [int(seed), r, a, b]
                match = play_match(STRATEGIES[a], STRATEGIES[b], rounds, noise, pair_seed, payoffs)
                means, cs = match['mean_scores'], match['cooperation']
                if i == j:
                    payoff[r, i, i] = means.mean()
                    cooperation[r, i, i] = cs.mean()
                else:
                    order = [0, 1] if ids == [a, b] else [1, 0]
                    x, y = means[order]
                    cx, cy = cs[order]
                    payoff[r, i, j], payoff[r, j, i] = x, y
                    cooperation[r, i, j], cooperation[r, j, i] = cx, cy
                    wins[r, i, j], wins[r, j, i] = float(x > y + 1e-12), float(y > x + 1e-12)
    return {'players': players, 'rounds': rounds, 'repetitions': repetitions,
            'noise': noise, 'seed': seed, 'self_play': self_play, 'payoffs': tuple(payoffs),
            'pair_payoff': payoff, 'pair_cooperation': cooperation,
            'scores': np.nanmean(payoff, axis=2),
            'cooperation': np.nanmean(cooperation, axis=2),
            # Self-play is never a head-to-head win. Draws count as zero wins.
            'win_fraction': np.nanmean(wins, axis=2)}


def evolve_population(players=('Always Cooperate', 'Always Defect', 'Tit for Tat', 'Random'),
                      initial_shares=None, generations=60, population_size=2000,
                      selection_strength=0.2, mutation=0.0, rounds=50,
                      repetitions=80, noise=0.0, seed=3024,
                      payoffs=(5, 3, 1, 0)):
    """Evolve fixed tournament strategies in a finite, well-mixed population.

    First estimate a mean pairwise payoff matrix from repeated matches. In each
    generation, strategy ``s`` earns the matrix-weighted payoff against the
    current mixture. The next generation is sampled with probability
    proportional to ``share * exp(selection_strength * payoff)``. Mutation,
    when non-zero, replaces a fraction of that distribution uniformly across
    the listed strategies. Strategies keep the same action rules; only their
    population shares change.
    """
    players = tuple(players)
    _positive_integer(generations, 'generations')
    _positive_integer(population_size, 'population_size')
    _positive_integer(repetitions, 'repetitions')
    if len(players) < 2 or len(set(players)) != len(players) or any(p not in STRATEGIES for p in players):
        raise ValueError('Use at least two distinct known strategies')
    if not np.isfinite(selection_strength) or selection_strength < 0:
        raise ValueError('selection_strength must be non-negative')
    if not np.isfinite(mutation) or not 0 <= mutation <= 1:
        raise ValueError('mutation must be between 0 and 1')

    n = len(players)
    if initial_shares is None:
        shares = np.full(n, 1 / n, dtype=float)
    else:
        shares = np.asarray(initial_shares, dtype=float)
        if shares.shape != (n,) or np.any(shares < 0) or not np.isclose(shares.sum(), 1):
            raise ValueError('initial_shares must be non-negative and sum to one')
        shares = shares.copy()

    tournament = run_tournament(
        players=players, rounds=rounds, repetitions=repetitions,
        noise=noise, seed=seed, self_play=True, payoffs=payoffs,
    )
    pair_payoff = np.nanmean(tournament['pair_payoff'], axis=0)
    history = np.empty((generations + 1, n), dtype=float)
    mean_payoffs = np.empty((generations, n), dtype=float)
    history[0] = shares
    rng = np.random.default_rng(seed + 1)

    for generation in range(generations):
        mean_payoffs[generation] = pair_payoff @ shares
        # An extinct strategy has zero copying weight when mutation is off.
        # Keep its log-weight at -inf without emitting a runtime warning.
        with np.errstate(divide='ignore'):
            log_weight = np.log(np.maximum(shares, 0)) + selection_strength * mean_payoffs[generation]
        log_weight -= np.max(log_weight)
        weights = np.exp(log_weight)
        probabilities = weights / weights.sum()
        if mutation:
            probabilities = (1 - mutation) * probabilities + mutation / n
        shares = rng.multinomial(population_size, probabilities) / population_size
        history[generation + 1] = shares

    return {
        'players': players,
        'shares': history,
        'mean_payoffs': mean_payoffs,
        'pair_payoff': pair_payoff,
        'generations': generations,
        'population_size': population_size,
        'selection_strength': selection_strength,
        'mutation': mutation,
        'rounds': rounds,
        'repetitions': repetitions,
        'noise': noise,
        'seed': seed,
        'payoffs': tuple(payoffs),
    }


def summarise(result):
    """Rank by median score across repetitions; tied medians share a rank."""
    median = np.median(result['scores'], axis=0)
    q1, q3 = np.quantile(result['scores'], [.25, .75], axis=0)
    records = []
    for i in np.argsort(-median, kind='stable'):
        records.append({'strategy': result['players'][i],
                        'rank': 1 + int(np.sum(median > median[i] + 1e-12)),
                        'median_score': float(median[i]), 'q25': float(q1[i]), 'q75': float(q3[i]),
                        'cooperation': float(result['cooperation'][:, i].mean()),
                        'win_fraction': float(result['win_fraction'][:, i].mean())})
    return records
