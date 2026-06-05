"""Portal gate composed rules match Rules.has_portal_gate."""
from __future__ import annotations

import unittest

from BaseClasses import CollectionState

from .bases import AtlyssTestBase
from worlds.atlyss.AtlyssRules.custom_rules import CanAccessAreaGameplay
from worlds.atlyss.AtlyssRules.portal_compose import build_portal_gate_rule, build_shop_slot_rule
from worlds.atlyss.Rules import has_area_for_gameplay
from worlds.atlyss.AccessData import parse_shop_buy_location
from worlds.atlyss.QuestAccess import PORTAL_GATES
from worlds.atlyss.Rules import has_portal_gate, has_shop_slot_progress


class TestPortalGateParity(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "equipment_progression": "unrestricted",
    }

    def _parity_for_gate(self, gate_id: str, random_portals: bool) -> None:
        self.options = {**self.options, "random_portals": "true" if random_portals else "false"}
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        composed = build_portal_gate_rule(world, gate_id).resolve(world)
        self.assertEqual(
            composed(state),
            has_portal_gate(state, self.player, gate_id),
            f"gate={gate_id} random_portals={random_portals}",
        )

    def test_progressive_portal_gates(self) -> None:
        for gate_id in ("outer_sanctum", "tuul_valley", "sanctum_catacombs_f2", "crescent_grove_colossus"):
            with self.subTest(gate_id=gate_id):
                self._parity_for_gate(gate_id, False)

    def test_random_portal_gates(self) -> None:
        for gate_id in ("outer_sanctum", "tuul_valley", "sanctum_catacombs_f2"):
            with self.subTest(gate_id=gate_id):
                self._parity_for_gate(gate_id, True)

    def test_area_gameplay_entrance_matches_helper(self) -> None:
        self.options = {**self.options, "random_portals": "false"}
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        for area in ("Sanctum Catacombs lvl 2", "Crescent Grove lvl 2"):
            with self.subTest(area=area):
                composed = CanAccessAreaGameplay(area).resolve(world)
                self.assertEqual(
                    composed(state),
                    has_area_for_gameplay(state, self.player, area),
                )

    def test_shop_slot_composed_matches_helper(self) -> None:
        self.options = {
            **self.options,
            "goal": "galius",
            "shop_sanity": "true",
            "random_portals": "false",
        }
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        parsed = parse_shop_buy_location("Buy Item #1 from Sally's Nook")
        self.assertIsNotNone(parsed)
        slot, merchant = parsed
        composed = build_shop_slot_rule(world, merchant, slot).resolve(world)
        self.assertEqual(
            composed(state),
            has_shop_slot_progress(state, self.player, merchant, slot),
        )

    def test_all_portal_gates_registered(self) -> None:
        self.options = {**self.options, "random_portals": "false"}
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        for gate_id in PORTAL_GATES:
            with self.subTest(gate_id=gate_id):
                composed = build_portal_gate_rule(world, gate_id).resolve(world)
                self.assertEqual(composed(state), has_portal_gate(state, self.player, gate_id))
