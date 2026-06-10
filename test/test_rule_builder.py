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
