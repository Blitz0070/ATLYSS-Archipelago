"""Rule Builder access tests."""
from __future__ import annotations

from BaseClasses import CollectionState

from rule_builder.rules import Rule

from .bases import AtlyssTestBase
from worlds.atlyss.AtlyssRules.custom_rules import (
    HasPortalGate,
    QuestCheck,
    ShopSlotCheck,
    quest_check_explain_str,
)
from worlds.atlyss.AtlyssRules.portal_compose import portal_gate_explain_label

# Random-portal route through Tuul Valley — no Tuul Enclave (reported false-positive case).
TUUL_VALLEY_ONLY_RANDOM_PORTALS = (
    "Outer Sanctum Portal",
    "Arcwood Pass Portal",
    "Effold Terrace Portal",
    "Tuul Valley Portal",
)

LATE_MINING_CHECKS = tuple(f"Mining Lv. {level}" for level in range(7, 11))
EARLY_MINING_CHECKS = ("Mining Lv. 1", "Mining Lv. 2")
# Mining train bands: Lv 1 pickaxe; Lv 2–3 hefty|dense routes; Lv 3–6 amberite; Lv 6–10 sapphite (MiningData).
EARLY_ROUTE_MINING_CHECKS = ("Mining Lv. 2", "Mining Lv. 3")
MID_MINING_CHECKS = tuple(f"Mining Lv. {level}" for level in range(4, 7))

ARCWOOD_ROUTE_RANDOM_PORTALS = (
    "Outer Sanctum Portal",
    "Arcwood Pass Portal",
)
EFFOLD_ROUTE_RANDOM_PORTALS = (
    "Outer Sanctum Portal",
    "Effold Terrace Portal",
)
TUUL_ENCLAVE_ROUTE_RANDOM_PORTALS = (
    "Outer Sanctum Portal",
    "Tuul Valley Portal",
    "Tuul Enclave Portal",
)
CRESCENT_ROAD_ROUTE_RANDOM_PORTALS = (
    "Outer Sanctum Portal",
    "Arcwood Pass Portal",
    "Crescent Road Portal",
)

EARLY_FISHING_CHECKS = ("Fishing Lv. 2", "Fishing Lv. 3")
MID_FISHING_CHECKS = tuple(f"Fishing Lv. {level}" for level in range(4, 7))
LATE_FISHING_CHECKS = tuple(f"Fishing Lv. {level}" for level in range(7, 11))


def _mark_quest_complete(state: CollectionState, player: int, quest_name: str) -> None:
    state.add_item(f"Complete: {quest_name}", player)
    state.stale[player] = True
    state.rule_builder_cache[player].clear()


class TestProgressivePortalQuestAccess(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_wicked_wizboars_requires_progressive_portals(self) -> None:
        self.assertAccessDependency(
            ["Wicked Wizboars"],
            [["Progressive Sanctum Portal"]],
            only_check_listed=True,
        )


class TestRandomPortalQuestAccess(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def test_wicked_wizboars_requires_named_portals(self) -> None:
        self.assertAccessDependency(
            ["Wicked Wizboars"],
            [["Outer Sanctum Portal", "Tuul Valley Portal"]],
            only_check_listed=True,
        )


class TestShopSlotAccess(AtlyssTestBase):
    options = {
        "goal": "galius",
        "shop_sanity": "true",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_catacombs_shop_row_requires_portal_progression(self) -> None:
        self.assertAccessDependency(
            ["Buy Item #1 from Sally's Nook"],
            [["Progressive Sanctum Portal"]],
            only_check_listed=True,
        )


class TestPortalExplain(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_progressive_portal_explain_mentions_progressive_item(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        label = portal_gate_explain_label(world, "tuul_valley")
        self.assertIn("Progressive Sanctum Portal", label)
        self.assertIn("Progressive Tuul Portal", label)

    def test_quest_explain_mentions_portals(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        text = quest_check_explain_str(world, "Dense Ingots")
        self.assertIn("Dense Ingots", text)
        self.assertIn("Progressive", text)

    def test_wicked_wizboars_location_rule_is_quest_check_resolved(self) -> None:
        self.world_setup()
        loc = self.multiworld.get_location("Wicked Wizboars", self.player)
        rule = loc.access_rule
        self.assertIsInstance(rule, Rule.Resolved)
        assert isinstance(rule, Rule.Resolved)
        self.assertEqual(rule.rule_name, "QuestCheck")

    def test_quest_check_explain_json_uses_color_when_state_given(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        resolved = QuestCheck("Wicked Wizboars").resolve(world)
        parts = resolved.explain_json(state)
        colors = {p["color"] for p in parts if p.get("type") == "color"}
        self.assertIn("salmon", colors)
        for item in self.get_items_by_name(["Progressive Sanctum Portal", "Progressive Tuul Portal"]):
            state.collect(item)
        parts_open = resolved.explain_json(state)
        colors_open = {p["color"] for p in parts_open if p.get("type") == "color"}
        self.assertIn("green", colors_open)

    def test_portal_gate_explain_json_structure(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        resolved = HasPortalGate("tuul_valley").resolve(world)
        parts = resolved.explain_json()
        self.assertTrue(any(p.get("type") == "color" for p in parts))
        self.assertTrue(any("Portal" in p.get("text", "") for p in parts))


class TestRandomPortalExplain(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def test_random_portal_explain_lists_named_portals(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        label = portal_gate_explain_label(world, "tuul_valley")
        self.assertIn("Outer Sanctum Portal", label)
        self.assertIn("Tuul Valley Portal", label)


class TestRuleCacheInvalidation(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_collecting_portal_updates_reachability(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self.assertFalse(state.can_reach("Wicked Wizboars", "Location", self.player))
        items = self.get_items_by_name(["Progressive Sanctum Portal", "Progressive Tuul Portal"])
        for item in items:
            state.collect(item)
        self.assertTrue(state.can_reach("Wicked Wizboars", "Location", self.player))


class TestEarlyMidFishingChecks(AtlyssTestBase):
    """Fishing Lv. 1–10 spot train bands (random portals)."""

    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
        "profession_tools": "pool",
    }

    def _collect_rod(self, state: CollectionState) -> None:
        for item in self.get_items_by_name(["Fishing Rod"]):
            state.collect(item)

    def _collect_named_portals(self, state: CollectionState, portal_names: tuple[str, ...]) -> None:
        for item in self.get_items_by_name(list(portal_names)):
            state.collect(item)

    def test_fishing_lv1_requires_rod_only(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self.assertFalse(state.can_reach("Fishing Lv. 1", "Location", self.player))
        self._collect_rod(state)
        self.assertTrue(state.can_reach("Fishing Lv. 1", "Location", self.player))

    def test_sanctum_spot_unlocks_fishing_two_three(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_rod(state)
        for check_name in EARLY_FISHING_CHECKS:
            with self.subTest(check=check_name):
                self.assertTrue(state.can_reach(check_name, "Location", self.player))

    def test_arcwood_unlocks_mid_blocks_late(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_rod(state)
        self._collect_named_portals(state, ARCWOOD_ROUTE_RANDOM_PORTALS)
        for check_name in MID_FISHING_CHECKS:
            with self.subTest(check=check_name):
                self.assertTrue(state.can_reach(check_name, "Location", self.player))
        for check_name in LATE_FISHING_CHECKS:
            with self.subTest(check=check_name):
                self.assertFalse(state.can_reach(check_name, "Location", self.player))

    def test_rod_only_cannot_reach_mid_fishing(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_rod(state)
        for check_name in MID_FISHING_CHECKS:
            with self.subTest(check=check_name):
                self.assertFalse(state.can_reach(check_name, "Location", self.player))

    def test_crescent_road_unlocks_late_fishing(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_rod(state)
        self._collect_named_portals(state, CRESCENT_ROAD_ROUTE_RANDOM_PORTALS)
        for check_name in LATE_FISHING_CHECKS:
            with self.subTest(check=check_name):
                self.assertTrue(state.can_reach(check_name, "Location", self.player))


class TestEarlyMidMiningChecks(AtlyssTestBase):
    """Mining Lv. 1–6 route + profession-grind bands (random portals)."""

    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
        "profession_tools": "pool",
    }

    def _collect_pickaxe(self, state: CollectionState) -> None:
        for item in self.get_items_by_name(["Pickaxe"]):
            state.collect(item)

    def _collect_named_portals(self, state: CollectionState, portal_names: tuple[str, ...]) -> None:
        for item in self.get_items_by_name(list(portal_names)):
            state.collect(item)

    def test_mining_lv1_requires_pickaxe_only(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self.assertFalse(state.can_reach("Mining Lv. 1", "Location", self.player))
        self._collect_pickaxe(state)
        self.assertTrue(state.can_reach("Mining Lv. 1", "Location", self.player))

    def test_early_mining_reachable_via_arcwood_or_effold(self) -> None:
        self.world_setup()
        for route_name, portals in (
            ("arcwood", ARCWOOD_ROUTE_RANDOM_PORTALS),
            ("effold", EFFOLD_ROUTE_RANDOM_PORTALS),
        ):
            with self.subTest(route=route_name):
                state = CollectionState(self.multiworld)
                self._collect_pickaxe(state)
                self._collect_named_portals(state, portals)
                for check_name in EARLY_ROUTE_MINING_CHECKS:
                    self.assertTrue(
                        state.can_reach(check_name, "Location", self.player),
                        f"{check_name} blocked on {route_name} route",
                    )

    def test_outer_sanctum_only_cannot_reach_mining_two(self) -> None:
        """1→2 needs Hefty Stone (arcwood|effold); Dense Stone starts at mining level 2."""
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_pickaxe(state)
        state.collect(self.get_item_by_name("Outer Sanctum Portal"))
        self.assertFalse(state.can_reach("Mining Lv. 2", "Location", self.player))
        self.assertFalse(state.can_reach("Mining Lv. 3", "Location", self.player))

    def test_mid_mining_reachable_at_tuul_valley(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_pickaxe(state)
        self._collect_named_portals(state, TUUL_VALLEY_ONLY_RANDOM_PORTALS)
        for check_name in MID_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertTrue(
                    state.can_reach(check_name, "Location", self.player),
                    f"{check_name} blocked at Tuul Valley route",
                )

    def test_mid_mining_blocked_without_tuul_valley(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_pickaxe(state)
        self._collect_named_portals(state, ARCWOOD_ROUTE_RANDOM_PORTALS)
        for check_name in MID_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertFalse(
                    state.can_reach(check_name, "Location", self.player),
                    f"{check_name} reachable on arcwood-only route",
                )

    def test_effold_route_does_not_unlock_late_mining_regression(self) -> None:
        """Old bug: character grind on Effold [1–10] green-lit Mining 7+ without Enclave."""
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_pickaxe(state)
        self._collect_named_portals(state, EFFOLD_ROUTE_RANDOM_PORTALS)
        for check_name in LATE_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertFalse(
                    state.can_reach(check_name, "Location", self.player),
                    f"{check_name} reachable on Effold-only route (regression)",
                )

    def test_valley_route_unlocks_mid_blocks_late(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_pickaxe(state)
        self._collect_named_portals(state, TUUL_VALLEY_ONLY_RANDOM_PORTALS)
        for check_name in MID_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertTrue(state.can_reach(check_name, "Location", self.player))
        for check_name in LATE_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertFalse(state.can_reach(check_name, "Location", self.player))


class TestEarlyMidMiningChecksProgressive(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
        "profession_tools": "pool",
    }

    def test_progressive_arcwood_unlocks_early_mining(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Pickaxe"]):
            state.collect(item)
        for _ in range(2):
            state.collect(self.get_item_by_name("Progressive Sanctum Portal"))
        for check_name in EARLY_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertTrue(state.can_reach(check_name, "Location", self.player))

    def test_progressive_valley_unlocks_mid_blocks_late(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Pickaxe"]):
            state.collect(item)
        for _ in range(6):
            state.collect(self.get_item_by_name("Progressive Sanctum Portal"))
        state.collect(self.get_item_by_name("Progressive Tuul Portal"))
        for check_name in MID_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertTrue(state.can_reach(check_name, "Location", self.player))
        for check_name in LATE_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertFalse(state.can_reach(check_name, "Location", self.player))


class TestTuulValleyOnlyNotInLogic(AtlyssTestBase):
    """Valley route without Enclave must not reach late mining or Sapphite."""

    options = {
        "goal": "all_quests",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
        "profession_tools": "pool",
    }

    def _collect_tuul_valley_route_random(self, state: CollectionState) -> None:
        for item in self.get_items_by_name(["Pickaxe", *TUUL_VALLEY_ONLY_RANDOM_PORTALS]):
            state.collect(item)

    def test_random_portals_valley_only_not_in_logic(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_tuul_valley_route_random(state)
        for check_name in LATE_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertFalse(
                    state.can_reach(check_name, "Location", self.player),
                    f"{check_name} reachable with Tuul Valley only (random portals)",
                )
        _mark_quest_complete(state, self.player, "Dense Ingots")
        _mark_quest_complete(state, self.player, "Amberite Ingots")
        self.assertFalse(
            state.can_reach("Sapphite Ingots", "Location", self.player),
            "Sapphite reachable with Tuul Valley only (random portals)",
        )

    def test_random_portals_enclave_unlocks_late_mining(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self._collect_tuul_valley_route_random(state)
        state.collect(self.get_item_by_name("Tuul Enclave Portal"))
        for check_name in LATE_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertTrue(
                    state.can_reach(check_name, "Location", self.player),
                    f"{check_name} blocked after Tuul Enclave unlock",
                )


class TestTuulValleyOnlyNotInLogicProgressive(AtlyssTestBase):
    options = {
        "goal": "all_quests",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
        "profession_tools": "pool",
    }

    def test_progressive_valley_only_not_in_logic(self) -> None:
        """6 Sanctum + 1 Tuul opens Valley, not Enclave (9 + 2)."""
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Pickaxe"]):
            state.collect(item)
        for _ in range(6):
            state.collect(self.get_item_by_name("Progressive Sanctum Portal"))
        state.collect(self.get_item_by_name("Progressive Tuul Portal"))
        for check_name in LATE_MINING_CHECKS:
            with self.subTest(check=check_name):
                self.assertFalse(
                    state.can_reach(check_name, "Location", self.player),
                    f"{check_name} reachable at progressive Valley tier",
                )
        _mark_quest_complete(state, self.player, "Dense Ingots")
        _mark_quest_complete(state, self.player, "Amberite Ingots")
        self.assertFalse(
            state.can_reach("Sapphite Ingots", "Location", self.player),
            "Sapphite reachable at progressive Valley tier",
        )


class TestSapphiteTuulEnclaveGate(AtlyssTestBase):
    """Sapphite only needs tuul_enclave portal gate (materials farm there)."""

    options = {
        "goal": "all_quests",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def _prime_sapphite_quest_prereqs(self, state: CollectionState) -> None:
        _mark_quest_complete(state, self.player, "Dense Ingots")
        _mark_quest_complete(state, self.player, "Amberite Ingots")

    def test_sapphite_blocked_without_tuul_enclave(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Pickaxe", *TUUL_VALLEY_ONLY_RANDOM_PORTALS]):
            state.collect(item)
        self._prime_sapphite_quest_prereqs(state)
        self.assertFalse(state.can_reach("Sapphite Ingots", "Location", self.player))

    def test_sapphite_reachable_with_tuul_enclave_gate(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Pickaxe", *TUUL_ENCLAVE_ROUTE_RANDOM_PORTALS]):
            state.collect(item)
        self._prime_sapphite_quest_prereqs(state)
        self.assertTrue(state.can_reach("Sapphite Ingots", "Location", self.player))


class TestSapphiteTuulEnclaveGateProgressive(AtlyssTestBase):
    options = {
        "goal": "all_quests",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_progressive_enclave_unlocks_sapphite(self) -> None:
        """9 Sanctum + 2 Tuul = tuul_enclave gate."""
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Pickaxe"]):
            state.collect(item)
        for _ in range(9):
            state.collect(self.get_item_by_name("Progressive Sanctum Portal"))
        for _ in range(2):
            state.collect(self.get_item_by_name("Progressive Tuul Portal"))
        _mark_quest_complete(state, self.player, "Dense Ingots")
        _mark_quest_complete(state, self.player, "Amberite Ingots")
        self.assertTrue(state.can_reach("Sapphite Ingots", "Location", self.player))
