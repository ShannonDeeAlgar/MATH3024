import importlib.util
from pathlib import Path
import unittest
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tournament', ROOT / 'notebooks/week10/axelrod_tournament.py')
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)


class TournamentTests(unittest.TestCase):
    def test_notebook_is_a_modelling_design_workshop(self):
        notebook = json.loads((ROOT / 'notebooks/week10/WS_Game_theory.ipynb').read_text())
        ids = {c.get('id') for c in notebook['cells']}
        self.assertIn('w10-workshop-process', ids)
        self.assertIn('w10-workshop-questions', ids)
        self.assertIn('w10-workshop-specification', ids)
        self.assertIn('w10-workshop-pseudocode', ids)
        text = '\n'.join(''.join(c.get('source', [])) for c in notebook['cells'])
        self.assertIn('controlled comparison', text)
        self.assertIn('assumptions', text)
        self.assertIn('observables', text)
        self.assertIn('controlled comparison', text)
        self.assertIn('provided; your task', text)
        self.assertTrue((ROOT / 'notebooks/week10/Axelrod_tournament_reference.ipynb').exists())

    def test_known_matches(self):
        for left, right, expected in [
            ('Always Cooperate', 'Always Cooperate', [3, 3]),
            ('Always Defect', 'Always Cooperate', [5, 0]),
            ('Always Defect', 'Always Defect', [1, 1]),
            ('Tit for Tat', 'Tit for Tat', [3, 3]),
            ('Tit for Tat', 'Always Defect', [199/200, 204/200])]:
            np.testing.assert_allclose(game.play_match(left, right)['mean_scores'], expected)

    def test_simultaneous_actions_and_error_response(self):
        m = game.play_match('Tit for Tat', 'Tit for Tat', rounds=5, forced_flips=((1, 0),))
        np.testing.assert_array_equal(m['actions'], [[0,0],[1,0],[0,1],[1,0],[0,1]])

    def test_memory_resets(self):
        game.play_match('Grudger', 'Always Defect')
        np.testing.assert_array_equal(game.play_match('Grudger', 'Always Cooperate')['actions'], 0)

    def test_noise_extremes(self):
        m = game.play_match('Always Cooperate', 'Always Cooperate', noise=1)
        np.testing.assert_array_equal(m['actions'], 1)
        np.testing.assert_array_equal(m['scores'], 1)

    def test_strategy_rules(self):
        rng = np.random.default_rng(0)
        self.assertEqual(game.choose_action('Tit for Two Tats', (0,0), (0,1), rng), 0)
        self.assertEqual(game.choose_action('Tit for Two Tats', (0,0), (1,1), rng), 1)
        for own, other, expected in [(0,0,0),(0,1,1),(1,0,1),(1,1,0)]:
            self.assertEqual(game.choose_action('Win-Stay Lose-Shift',(own,),(other,),rng),expected)

    def test_reproducibility_and_entrant_order(self):
        a = game.run_tournament(rounds=12, repetitions=3, noise=.1)
        b = game.run_tournament(players=game.STRATEGIES[::-1], rounds=12, repetitions=3, noise=.1)
        np.testing.assert_array_equal(a['pair_payoff'], b['pair_payoff'][:,::-1,::-1])
        np.testing.assert_array_equal(a['scores'], game.run_tournament(rounds=12, repetitions=3, noise=.1)['scores'])

    def test_self_play_weight_and_exclusion(self):
        players = ('Always Cooperate','Always Defect')
        a = game.run_tournament(players, repetitions=2)
        np.testing.assert_allclose(a['scores'], [[1.5,3],[1.5,3]])
        b = game.run_tournament(players, repetitions=2, self_play=False)
        np.testing.assert_allclose(b['scores'], [[0,5],[0,5]])
        np.testing.assert_allclose(a['win_fraction'], [[0,1],[0,1]])

    def test_ranges_and_ties(self):
        a=game.run_tournament(('Always Cooperate','Tit for Tat'), repetitions=2)
        self.assertEqual([r['rank'] for r in game.summarise(a)], [1,1])
        self.assertTrue(np.all((a['cooperation']>=0)&(a['cooperation']<=1)))

    def test_evolution_reproducible_and_normalised(self):
        kwargs = dict(
            players=('Always Cooperate', 'Always Defect', 'Tit for Tat', 'Random'),
            generations=8, population_size=500, selection_strength=.08,
            rounds=20, repetitions=6, seed=3024,
        )
        a = game.evolve_population(**kwargs)
        b = game.evolve_population(**kwargs)
        np.testing.assert_array_equal(a['shares'], b['shares'])
        np.testing.assert_allclose(a['shares'].sum(axis=1), 1)
        self.assertEqual(a['shares'].shape, (9, 4))
        self.assertEqual(a['mean_payoffs'].shape, (8, 4))

    def test_evolution_without_mutation_keeps_extinct_types_extinct(self):
        a = game.evolve_population(
            players=('Always Cooperate', 'Always Defect'),
            initial_shares=(1.0, 0.0), generations=4, population_size=100,
            rounds=10, repetitions=3, seed=3024,
        )
        np.testing.assert_allclose(a['shares'][:, 1], 0)

    def test_match_length_comparison_keeps_shared_prefix(self):
        a = game.play_match('Random', 'Tit for Tat', rounds=20, noise=.1, seed=19)
        b = game.play_match('Random', 'Tit for Tat', rounds=200, noise=.1, seed=19)
        np.testing.assert_array_equal(a['actions'], b['actions'][:20])

    def test_invalid_inputs(self):
        for kwargs in ({'rounds':0},{'noise':-1},{'noise':float('nan')},{'payoffs':(1,3,5,0)}):
            with self.assertRaises(ValueError):game.play_match('Tit for Tat','Random',**kwargs)
        with self.assertRaises(ValueError):game.run_tournament(('Random','Random'))


if __name__=='__main__':unittest.main()
