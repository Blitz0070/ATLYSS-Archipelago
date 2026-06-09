"""Fill-side progression rules (``ProgressionLogic`` lambdas, not Rule Builder access).

Uses ``auto_construct = False`` so each test builds its own world. Fill regressions
live in ``TestGatedFillSmoke`` (including seed ``90343505581788154822``: tier-1 checks
must not receive tier-2+ concrete gear from fill).
"""
from __future__ import annotations

from BaseClasses import Item, ItemClassification, Location
from Fill import distribute_items_restrictive

from .bases import AtlyssTestBase
from worlds.atlyss.ItemTiers import get_item_tier
from worlds.atlyss.ProgressionLogic import get_location_max_tier


class TestGatedEquipmentItemRules(AtlyssTestBase):
    """Item-rule lambdas only — no WorldTestBase fill/all_state (see ``TestGatedFillSmoke``)."""

    auto_construct = False

    def test_gated_locations_use_item_rule_lambdas(self) -> None:
        self.options = {
            "goal": "slime_diva",
            "random_portals": "false",
            "equipment_progression": "gated",
        }
        self.world_setup()
        loc = self.multiworld.get_location("Wicked Wizboars", self.player)
        self.assertIsNot(loc.item_rule, Location.item_rule)

    def test_tier_item_rule_blocks_over_tier_equipment(self) -> None:
        self.options = {
            "goal": "slime_diva",
            "random_portals": "false",
            "equipment_progression": "gated",
        }
        self.world_setup()
        loc = self.multiworld.get_location("Buy Item #1 from Sally's Nook", self.player)
        max_tier = get_location_max_tier(loc.name, loc.parent_region.name)
        high_tier_item = Item("Iron Katars", ItemClassification.useful, None, self.player)
        item_tier = get_item_tier(high_tier_item.name)
        self.assertIsNotNone(item_tier)
        assert item_tier is not None
        self.assertGreater(item_tier, max_tier)
        self.assertFalse(loc.item_rule(high_tier_item))

    def test_unrestricted_allows_over_tier_equipment_at_shop(self) -> None:
        self.options = {
            "goal": "slime_diva",
            "random_portals": "false",
            "equipment_progression": "unrestricted",
        }
        self.world_setup()
        loc = self.multiworld.get_location("Buy Item #1 from Sally's Nook", self.player)
        high_tier_item = Item("Iron Katars", ItemClassification.useful, None, self.player)
        self.assertTrue(loc.item_rule(high_tier_item))


class TestGatedFillSmoke(AtlyssTestBase):
    """Explicit gated fill on seeds that already pass with caching (``test_rule_caching``)."""

    auto_construct = False

    def test_fill_succeeds_on_regression_seeds(self) -> None:
        self.options = {
            "goal": "slime_diva",
            "shop_sanity": "true",
            "equipment_progression": "gated",
            "random_portals": "false",
        }
        for seed in (
            47215607589033149358,
            10851523903115954330,
            999707401169759378,
            90343505581788154822,
        ):
            with self.subTest(seed=seed):
                self.world_setup(seed)
                distribute_items_restrictive(self.multiworld)

    def test_rebalance_leaves_no_tiered_items_in_pool(self) -> None:
        self.options = {
            "goal": "slime_diva",
            "equipment_progression": "gated",
            "random_portals": "false",
        }
        self.world_setup(90343505581788154822)
        for item in self.multiworld.itempool:
            if item.player != self.player:
                continue
            self.assertIsNone(
                get_item_tier(item.name),
                f"concrete tiered gear must be pre-placed or stripped, not pooled: {item.name}",
            )

    def test_gated_fill_places_no_concrete_tiered_gear(self) -> None:
        from worlds.atlyss.Items import useful_items

        self.options = {
            "goal": "slime_diva",
            "shop_sanity": "true",
            "equipment_progression": "gated",
            "random_portals": "false",
            "class_filter": "all_classes",
        }
        concrete_tiered = {
            name for name in useful_items if get_item_tier(name) is not None
        }
        self.world_setup(90343505581788154822)
        distribute_items_restrictive(self.multiworld)
        for location in self.multiworld.get_filled_locations(self.player):
            item = location.item
            if item is None:
                continue
            self.assertNotIn(
                item.name,
                concrete_tiered,
                f"gated fill must not place standalone gear AP names: {location.name}",
            )
