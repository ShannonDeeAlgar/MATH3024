"""Check the preparation clock and open-boundary load accounting."""

import unittest

import numpy as np

from generate_week08_tuned_vs_driven import relax_open


class SandpilePreparationTests(unittest.TestCase):
    def test_stable_state_requires_no_preparation_steps(self):
        initial = np.full((4, 4), 3)
        final, density, active, loss = relax_open(initial, record=True)
        np.testing.assert_array_equal(final, initial)
        np.testing.assert_array_equal(density, [3])
        np.testing.assert_array_equal(active, [0])
        self.assertEqual(loss.size, 0)

    def test_corner_toppling_loses_two_grains(self):
        initial = np.zeros((3, 3), dtype=int)
        initial[0, 0] = 4
        final, _, active, loss = relax_open(initial, record=True)
        expected = np.zeros_like(initial)
        expected[1, 0] = expected[0, 1] = 1
        np.testing.assert_array_equal(final, expected)
        np.testing.assert_array_equal(active, [1, 0])
        np.testing.assert_array_equal(loss, [2])
        self.assertEqual(initial[0, 0], 4)

    def test_one_toppling_per_site_per_parallel_step(self):
        initial = np.array([[8]])
        _, density, active, loss = relax_open(initial, record=True)
        np.testing.assert_array_equal(density, [8, 4, 0])
        np.testing.assert_array_equal(active, [1, 1, 0])
        np.testing.assert_array_equal(loss, [4, 4])

    def test_displayed_preparation_history(self):
        initial = np.random.default_rng(8031).integers(0, 8, size=(16, 16))
        final, density, active, loss = relax_open(initial, record=True)
        self.assertEqual(loss.size, 106)
        self.assertEqual(loss[0], 30)
        self.assertEqual(loss.sum(), 345)
        self.assertEqual(active[-1], 0)
        self.assertLess(final.max(), 4)
        self.assertEqual(initial.sum() - final.sum(), loss.sum())
        np.testing.assert_allclose(np.diff(density) * initial.size, -loss)

    def test_final_state_matches_legal_batched_relaxation(self):
        for seed in range(5):
            initial = np.random.default_rng(seed).integers(0, 16, size=(8, 8))
            batched = initial.copy()
            while np.any(batched >= 4):
                topplings = batched // 4
                batched -= 4 * topplings
                batched[1:] += topplings[:-1]
                batched[:-1] += topplings[1:]
                batched[:, 1:] += topplings[:, :-1]
                batched[:, :-1] += topplings[:, 1:]
            np.testing.assert_array_equal(relax_open(initial), batched)


if __name__ == "__main__":
    unittest.main()
