"""Rule Builder dependency registration."""
from __future__ import annotations

from .bases import AtlyssTestBase


class TestRuleDependencies(AtlyssTestBase):
    options = {
        "goal": "galius",
        "shop_sanity": "true",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_portal_items_registered_for_quest_and_shop(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        self.assertIn("Progressive Sanctum Portal", world.rule_item_dependencies)
        wicked_deps = world.rule_item_dependencies.get("Progressive Sanctum Portal", set())
        self.assertTrue(wicked_deps, "portal collection should register quest/shop rules")

    def test_quest_completion_item_registered(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        key = "Complete: Communing Catacombs"
        self.assertIn(key, world.rule_item_dependencies)

    def test_anchor_locations_register_portal_deps(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        wicked = self.multiworld.get_location("Wicked Wizboars", self.player)
        self.assertIsInstance(wicked.access_rule, object)
        self.assertIn(
            "Progressive Sanctum Portal",
            wicked.access_rule.item_dependencies(),  # type: ignore[union-attr]
        )

    def test_shop_anchor_registers_portal_and_story_deps(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        shop = self.multiworld.get_location("Buy Item #1 from Sally's Nook", self.player)
        deps = shop.access_rule.item_dependencies()  # type: ignore[union-attr]
        self.assertIn("Progressive Sanctum Portal", deps)

    def test_outer_sanctum_entrance_has_region_dependency(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        entrance = self.multiworld.get_entrance("Sanctum -> Outer Sanctum", self.player)
        regions = entrance.access_rule.region_dependencies()  # type: ignore[union-attr]
        self.assertIn("Outer Sanctum", regions)
        self.assertIn(
            "Outer Sanctum",
            world.rule_region_dependencies,
        )
