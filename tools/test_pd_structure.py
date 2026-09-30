import importlib.util
from pathlib import Path
import unittest
import json
import numpy as np

P = Path(__file__).resolve().parents[1] / 'notebooks/week10/pd_structure.py'
spec = importlib.util.spec_from_file_location('pd_structure', P)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PDTests(unittest.TestCase):
    def test_workshop_is_self_contained_and_executed(self):
        notebook = json.loads(P.with_name('WS_Game_theory.ipynb').read_text())
        cells = {c['id']: c for c in notebook['cells']}
        self.assertIn('w10-workshop-baseline-code', cells)
        self.assertIn('w10-workshop-match-starter', cells)
        self.assertIn('w10-workshop-tournament-starter', cells)
        source = '\n'.join(''.join(c.get('source', [])) for c in cells.values())
        self.assertIn('T, R, P, S = 5, 3, 1, 0', source)
        self.assertIn('def play_match', source)
        self.assertIn('def pairwise_payoffs', source)
        self.assertIn('def random_opponent_tournament', source)
        self.assertIn('Strategies remain fixed', source)

    def test_graph(self):
        n = m.lattice(5)
        for i, row in enumerate(n):
            self.assertEqual(len(set(row)), 4)
            self.assertNotIn(i, row)
            for j in row: self.assertIn(i, n[j])

    def test_payoffs(self):
        n = m.lattice(5)
        np.testing.assert_equal(m.scores(np.zeros(25, int), n, m.payoff_matrix()), 12)
        np.testing.assert_equal(m.scores(np.ones(25, int), n, m.payoff_matrix()), 4)
        s = np.zeros(25, int); s[12] = m.D
        a = m.scores(s, n, m.payoff_matrix())
        self.assertAlmostEqual(a[12], 13.6)
        np.testing.assert_equal(a[n[12]], 9)
        result = m.copy_best(s, a, n, np.random.default_rng(0))
        self.assertEqual(set(np.flatnonzero(result == m.D)), {12, *n[12]})

    def test_absorbing_and_reproducible(self):
        n = m.lattice(5)
        for rule in [m.copy_best, m.copy_one_reference]:
            for action in [m.C, m.D]:
                h = m.simulate(np.full(25, action), n, rule, steps=10)
                np.testing.assert_equal(h, action)
            s = m.initial_state(5, seed=4); old = s.copy()
            a = m.simulate(s, n, rule, steps=10, seed=9)
            np.testing.assert_array_equal(a, m.simulate(s, n, rule, steps=10, seed=9))
            np.testing.assert_array_equal(s, old)

    def test_copy_one_ties_retain(self):
        s = m.initial_state(5)
        np.testing.assert_array_equal(s, m.copy_one_reference(s, np.ones(25), m.lattice(5), np.random.default_rng(0)))


if __name__ == '__main__': unittest.main()
