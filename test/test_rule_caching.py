"""Rule-builder caching: fill, copy, and reachability."""
from __future__ import annotations

import time

from BaseClasses import CollectionState
from Fill import distribute_items_restrictive

from .bases import AtlyssTestBase


class TestRuleCachingEnabled(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_world_has_caching_enabled(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        self.assertTrue(world.rule_caching_enabled)

    def test_progression_collect_clears_rule_cache_before_sweep(self) -> None:
        """World.collect clears cache; state.collect then sweep repopulates with fresh results."""
        self.world_setup()
        state = CollectionState(self.multiworld)
        wicked = self.multiworld.get_location("Wicked Wizboars", self.player)
        _ = wicked.access_rule(state)
        self.assertGreater(len(state.rule_builder_cache[self.player]), 0)
        items = self.get_items_by_name(["Progressive Sanctum Portal", "Progressive Tuul Portal"])
        world = self.multiworld.worlds[self.player]
        for item in items:
            world.collect(state, item)
            self.assertEqual(len(state.rule_builder_cache[self.player]), 0)
        for item in items:
            state.collect(item)
        self.assertTrue(state.can_reach("Wicked Wizboars", "Location", self.player))

    def test_state_copy_clears_rule_cache(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        loc = self.multiworld.get_location("Wicked Wizboars", self.player)
        _ = loc.access_rule(state)
        self.assertGreater(len(state.rule_builder_cache[self.player]), 0)
        copy = state.copy()
        self.assertEqual(len(copy.rule_builder_cache[self.player]), 0)

    def test_fill_succeeds_with_caching_on_regression_seeds(self) -> None:
        for seed in (
            47215607589033149358,
            10851523903115954330,
            999707401169759378,
        ):
            with self.subTest(seed=seed):
                self.world_setup(seed)
                distribute_items_restrictive(self.multiworld)

    def test_catacombs_entrance_reachable_after_quest_in_all_state(self) -> None:
        self.options = {
            **self.options,
            "goal": "galius",
            "shop_sanity": "true",
        }
        self.world_setup(999707401169759378)
        state = self.multiworld.get_all_state(False)
        entrance = self.multiworld.get_entrance(
            "Sanctum Catacombs lvl 1 -> Sanctum Catacombs lvl 2",
            self.player,
        )
        self.assertTrue(entrance.can_reach(state))
        self.assertTrue(
            state.can_reach("Buy Item #1 from Tesh's Wares", "Location", self.player),
        )

    def test_get_all_state_completes_within_reasonable_time(self) -> None:
        """Regression guard for UT-style ``get_all_state`` sweeps (not a strict perf budget)."""
        self.options = {
            **self.options,
            "goal": "galius",
            "shop_sanity": "true",
        }
        self.world_setup(999707401169759378)
        t0 = time.perf_counter()
        state = self.multiworld.get_all_state(False)
        elapsed = time.perf_counter() - t0
        self.assertLess(elapsed, 30.0, "get_all_state took too long; profile with scripts/profile_get_all_state.py")
        self.assertTrue(state.can_reach("Wicked Wizboars", "Location", self.player))
