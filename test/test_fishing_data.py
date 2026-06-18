"""Fishing train band table validation."""
from __future__ import annotations

import unittest

from worlds.atlyss.FishingData import (
    FISHING_TRAIN_BANDS,
    iter_fishing_train_portal_gates,
    fishing_bands_for_training_step,
)


class TestFishingTrainBands(unittest.TestCase):
    def test_each_step_two_through_ten_has_a_band(self) -> None:
        for to_level in range(2, 11):
            bands = fishing_bands_for_training_step(to_level - 1, to_level)
            self.assertTrue(bands, f"step {to_level - 1} → {to_level}")

    def test_sanctum_spot_band(self) -> None:
        sanctum = FISHING_TRAIN_BANDS[0]
        self.assertEqual(sanctum.spots, ("Sanctum",))
        self.assertEqual(sanctum.min_fish_level, 1)
        self.assertEqual(sanctum.max_train_level, 3)
        self.assertEqual(sanctum.portal_gates, ())

    def test_arcwood_spot_band(self) -> None:
        arcwood = FISHING_TRAIN_BANDS[1]
        self.assertEqual(arcwood.spots, ("Arcwood Pass",))
        self.assertEqual(arcwood.min_fish_level, 3)
        self.assertEqual(arcwood.max_train_level, 6)
        self.assertEqual(arcwood.portal_gates, ("arcwood_pass",))

    def test_crescent_road_spot_band(self) -> None:
        road = FISHING_TRAIN_BANDS[2]
        self.assertEqual(road.spots, ("Crescent Road",))
        self.assertEqual(road.min_fish_level, 6)
        self.assertEqual(road.max_train_level, 10)
        self.assertEqual(road.portal_gates, ("crescent_road",))

    def test_sanctum_trains_through_three_not_four(self) -> None:
        self.assertTrue(fishing_bands_for_training_step(2, 3))
        sanctum_to_four = [
            b for b in fishing_bands_for_training_step(3, 4) if b.spots == ("Sanctum",)
        ]
        self.assertFalse(sanctum_to_four)

    def test_arcwood_starts_at_step_three_to_four(self) -> None:
        arcwood_to_three = [
            b for b in fishing_bands_for_training_step(2, 3) if b.spots == ("Arcwood Pass",)
        ]
        self.assertFalse(arcwood_to_three)
        self.assertTrue(fishing_bands_for_training_step(3, 4))

    def test_crescent_road_starts_at_step_six_to_seven(self) -> None:
        road_to_six = [
            b for b in fishing_bands_for_training_step(5, 6) if b.spots == ("Crescent Road",)
        ]
        self.assertFalse(road_to_six)
        self.assertTrue(fishing_bands_for_training_step(6, 7))

    def test_portal_gates_include_arcwood_and_crescent_road(self) -> None:
        gates = iter_fishing_train_portal_gates()
        self.assertEqual(gates, ("arcwood_pass", "crescent_road"))


if __name__ == "__main__":
    unittest.main()
