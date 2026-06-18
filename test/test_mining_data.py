"""Mining train band table validation."""
from __future__ import annotations

import unittest

from worlds.atlyss.MiningData import (
    MINING_TRAIN_BANDS,
    iter_mining_train_portal_gates,
    mining_bands_for_training_step,
)


class TestMiningTrainBands(unittest.TestCase):
    def test_each_step_two_through_ten_has_a_band(self) -> None:
        for to_level in range(2, 11):
            bands = mining_bands_for_training_step(to_level - 1, to_level)
            self.assertTrue(bands, f"step {to_level - 1} → {to_level}")

    def test_hefty_stone_band(self) -> None:
        hefty = next(b for b in MINING_TRAIN_BANDS if b.nodes == ("Hefty Stone",))
        self.assertEqual(hefty.min_mine_level, 1)
        self.assertEqual(hefty.max_train_level, 3)
        self.assertEqual(hefty.portal_gates, ("arcwood_pass", "effold_terrace"))

    def test_dense_stone_band(self) -> None:
        dense = next(b for b in MINING_TRAIN_BANDS if b.nodes == ("Dense Stone",))
        self.assertEqual(dense.min_mine_level, 2)
        self.assertEqual(dense.max_train_level, 3)
        self.assertEqual(
            dense.portal_gates,
            ("arcwood_pass", "effold_terrace", "outer_sanctum", "crescent_keep", "tuul_enclave"),
        )

    def test_amberite_ore_band(self) -> None:
        amberite = next(b for b in MINING_TRAIN_BANDS if b.nodes == ("Amberite Ore",))
        self.assertEqual(amberite.min_mine_level, 3)
        self.assertEqual(amberite.max_train_level, 6)
        self.assertEqual(amberite.portal_gates, ("tuul_valley", "crescent_keep"))

    def test_sapphite_ore_band(self) -> None:
        sapphite = next(b for b in MINING_TRAIN_BANDS if b.nodes == ("Sapphite Ore",))
        self.assertEqual(sapphite.min_mine_level, 6)
        self.assertEqual(sapphite.max_train_level, 10)
        self.assertEqual(sapphite.portal_gates, ("tuul_enclave",))

    def test_hefty_trains_one_to_three_not_four(self) -> None:
        self.assertTrue(mining_bands_for_training_step(1, 2))
        self.assertTrue(mining_bands_for_training_step(2, 3))
        hefty_steps = [
            b for b in mining_bands_for_training_step(3, 4) if b.nodes == ("Hefty Stone",)
        ]
        self.assertFalse(hefty_steps)

    def test_amberite_starts_at_step_three_to_four(self) -> None:
        amberite_to_three = [
            b for b in mining_bands_for_training_step(2, 3) if b.nodes == ("Amberite Ore",)
        ]
        self.assertFalse(amberite_to_three)
        self.assertTrue(mining_bands_for_training_step(3, 4))

    def test_sapphite_starts_at_step_six_to_seven(self) -> None:
        sapphite_steps = [
            b for b in mining_bands_for_training_step(5, 6) if b.nodes == ("Sapphite Ore",)
        ]
        self.assertFalse(sapphite_steps)
        self.assertTrue(mining_bands_for_training_step(6, 7))

    def test_level_three_step_uses_hefty_or_dense_not_amberite(self) -> None:
        nodes = {band.nodes[0] for band in mining_bands_for_training_step(2, 3)}
        self.assertEqual(nodes, {"Hefty Stone", "Dense Stone"})

    def test_portal_gates_include_outer_sanctum_and_crescent_keep(self) -> None:
        gates = iter_mining_train_portal_gates()
        self.assertIn("outer_sanctum", gates)
        self.assertIn("crescent_keep", gates)


if __name__ == "__main__":
    unittest.main()
