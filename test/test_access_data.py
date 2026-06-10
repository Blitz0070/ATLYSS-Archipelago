"""Unit tests for AccessData / QuestAccess helpers."""
from __future__ import annotations

import unittest
from pathlib import Path

from worlds.atlyss.AccessData import (
    AREA_STORY_QUEST,
    PORTAL_PROGRESSIVE_REQUIREMENTS,
    REGION_ENTRANCE_STORY_QUEST,
    SHOP_AP_ITEMS_PORTAL_GATE,
    SHOP_MERCHANT_STORY_QUEST,
    parse_shop_buy_location,
    quest_requires_fishing_rod,
    quest_requires_pickaxe,
    shop_ap_items_portal_gate,
    shop_slot_tier_level,
    validate_story_quest_names,
)
from worlds.atlyss.Locations import enemy_data, portal_counts
from worlds.atlyss.Rules import _catacombs_gate_for_enemy_areas
from worlds.atlyss.ProgressionLogic import get_location_max_tier
from worlds.atlyss.QuestAccess import AREA_TO_GATE

_WORLD_ROOT = Path(__file__).resolve().parent.parent


class TestAccessData(unittest.TestCase):
    def test_shop_ap_items_single_portal_gate(self) -> None:
        self.assertEqual(shop_ap_items_portal_gate(), SHOP_AP_ITEMS_PORTAL_GATE)
        self.assertEqual(SHOP_AP_ITEMS_PORTAL_GATE, "sanctum_catacombs_f2")

    def test_shop_slot_tier_levels(self) -> None:
        self.assertEqual(shop_slot_tier_level("Sally's Nook", 1), 1)
        self.assertEqual(shop_slot_tier_level("Sally's Nook", 2), 8)
        self.assertEqual(shop_slot_tier_level("Tesh's Wares", 3), 12)

    def test_parse_shop_buy_location(self) -> None:
        self.assertEqual(
            parse_shop_buy_location("Buy Item #3 from Tesh's Wares"),
            (3, "Tesh's Wares"),
        )
        self.assertIsNone(parse_shop_buy_location("Buy Fishing Rod"))

    def test_story_tables_cover_region_entrances(self) -> None:
        self.assertEqual(REGION_ENTRANCE_STORY_QUEST, {})
        self.assertLessEqual(
            REGION_ENTRANCE_STORY_QUEST.items(),
            AREA_STORY_QUEST.items(),
        )
        self.assertNotIn("Sanctum Catacombs lvl 1", AREA_STORY_QUEST)
        self.assertIn("Sanctum Catacombs lvl 2", AREA_STORY_QUEST)
        self.assertNotIn("Crescent Road", AREA_STORY_QUEST)
        self.assertNotIn("Bularr Fortress", AREA_STORY_QUEST)
        self.assertIn("Tesh's Wares", SHOP_MERCHANT_STORY_QUEST)
        self.assertNotIn("Rikko's Treasures", SHOP_MERCHANT_STORY_QUEST)
        validate_story_quest_names({
            "Communing Catacombs",
            "The Keep Within",
            "A Warm Welcome",
        })

    def test_area_to_gate_covers_portal_counts(self) -> None:
        missing = set(portal_counts) - {"Sanctum"} - set(AREA_TO_GATE)
        self.assertFalse(missing, missing)

    def test_quest_requires_pickaxe(self) -> None:
        self.assertTrue(quest_requires_pickaxe("Dense Ingots"))
        self.assertTrue(quest_requires_pickaxe("Amberite Ingots"))
        self.assertTrue(quest_requires_pickaxe("Sapphite Ingots"))
        self.assertFalse(quest_requires_pickaxe("Makin' a Mekspear"))
        self.assertFalse(quest_requires_pickaxe("Summore' Golem Chestpieces"))
        self.assertFalse(quest_requires_pickaxe("Summore' Spectral Powder!"))
        self.assertFalse(quest_requires_pickaxe("A Warm Welcome"))

    def test_portal_progressive_requirements(self) -> None:
        self.assertEqual(
            PORTAL_PROGRESSIVE_REQUIREMENTS["Sanctum Catacombs lvl 2 Portal"],
            (4, 0),
        )
        self.assertEqual(PORTAL_PROGRESSIVE_REQUIREMENTS["Tuul Valley Portal"], (6, 1))
        self.assertEqual(PORTAL_PROGRESSIVE_REQUIREMENTS["Bularr Fortress Portal"], (11, 3))

    def test_quest_requires_fishing_rod(self) -> None:
        self.assertTrue(quest_requires_fishing_rod("Windtail Fish"))
        self.assertTrue(quest_requires_fishing_rod("Bittering Katfish"))
        self.assertTrue(quest_requires_fishing_rod("Turning in Windtail Fish"))
        self.assertFalse(quest_requires_fishing_rod("Dense Ingots"))
        self.assertFalse(quest_requires_fishing_rod("A Warm Welcome"))

    def test_catacombs_f2_quest_gates(self) -> None:
        from worlds.atlyss.QuestAccess import (
            QUEST_ACCESS,
            normalize_after_quest_names,
            normalize_portal_gate_ids,
        )

        for quest in ("The Voice of Zuulneruda", "Purging the Undead"):
            spec = QUEST_ACCESS[quest]
            self.assertEqual(spec.min_level, 6)
            self.assertEqual(spec.after_quest, "Killing Tomb")
            self.assertIsNone(spec.portal_gates)
            self.assertIsNotNone(spec.kill_enemies)

        rattlecage = QUEST_ACCESS["Rattlecage Rage"]
        self.assertEqual(rattlecage.after_quest, "Killing Tomb")
        self.assertEqual(
            normalize_portal_gate_ids(rattlecage.portal_gates),
            ("sanctum_catacombs_f2",),
        )

        killing_tomb = QUEST_ACCESS["Killing Tomb"]
        self.assertIsNone(killing_tomb.portal_gates)
        self.assertEqual(killing_tomb.kill_enemies, ("Mini Geist", "Geist"))

    def test_night_spirits_uses_kill_enemy_requirements(self) -> None:
        from worlds.atlyss.QuestAccess import QUEST_ACCESS

        spec = QUEST_ACCESS["Night Spirits"]
        self.assertEqual(spec.kill_enemies, ("Lesser Wisp", "Greater Wisp"))
        self.assertIsNone(spec.portal_gates)

    def test_dense_ingots_allows_arcwood_or_effold(self) -> None:
        from worlds.atlyss.QuestAccess import QUEST_ACCESS, normalize_portal_gate_ids

        self.assertEqual(
            normalize_portal_gate_ids(QUEST_ACCESS["Dense Ingots"].portal_gates),
            ("arcwood_pass", "effold_terrace"),
        )

    def test_level_only_quest_access_helper(self) -> None:
        from worlds.atlyss.QuestAccess import QUEST_ACCESS, quest_uses_level_access

        self.assertTrue(quest_uses_level_access(QUEST_ACCESS["Call of Fury"]))
        self.assertTrue(quest_uses_level_access(QUEST_ACCESS["Focusin' in"]))
        self.assertFalse(quest_uses_level_access(QUEST_ACCESS["Night Spirits"]))
        self.assertTrue(quest_uses_level_access(QUEST_ACCESS["Mastery of Strength"]))
        self.assertTrue(quest_uses_level_access(QUEST_ACCESS["Mastery of Dexterity"]))
        self.assertFalse(quest_uses_level_access(QUEST_ACCESS["A Warm Welcome"]))

    def test_kill_enemy_or_groups(self) -> None:
        from worlds.atlyss.QuestAccess import QUEST_ACCESS, iter_kill_enemy_names

        spec = QUEST_ACCESS["Makin' a Vile Blade"]
        self.assertEqual(spec.kill_enemies, (("Mouth", "Maw"), "Slimek", "Deathgel"))
        self.assertEqual(
            iter_kill_enemy_names(spec.kill_enemies),
            ("Mouth", "Maw", "Slimek", "Deathgel"),
        )

    def test_after_quest_and_prerequisites(self) -> None:
        from worlds.atlyss.QuestAccess import QUEST_ACCESS, normalize_after_quest_names

        self.assertEqual(
            normalize_after_quest_names(QUEST_ACCESS["Makin' a Ragespear"].after_quest),
            ("Makin' a Mekspear", "Finding Ammagon"),
        )
        self.assertEqual(normalize_after_quest_names("Killing Tomb"), ("Killing Tomb",))

    def test_catacombs_enemy_gate_uses_shallowest_floor(self) -> None:
        self.assertEqual(
            _catacombs_gate_for_enemy_areas(("Sanctum Catacombs lvl 1", "Sanctum Catacombs lvl 2")),
            "sanctum_catacombs",
        )
        self.assertEqual(
            _catacombs_gate_for_enemy_areas(("Sanctum Catacombs lvl 2", "Sanctum Catacombs lvl 3")),
            "sanctum_catacombs_f2",
        )
        self.assertEqual(
            _catacombs_gate_for_enemy_areas(("Sanctum Catacombs lvl 3",)),
            "sanctum_catacombs_f3",
        )

    def test_no_grove_enemy_spans_multiple_floors(self) -> None:
        """Grove uses per-area OR in can_beat_enemy; no max-depth gate helper exists yet."""
        grove_floors: dict[str, set[str]] = {}
        for enemy_name, (_level, areas) in enemy_data.items():
            grove_areas = [area for area in areas if area.startswith("Crescent Grove")]
            if not grove_areas:
                continue
            grove_floors[enemy_name] = set(grove_areas)
        multi_floor = {
            name: floors for name, floors in grove_floors.items() if len(floors) > 1
        }
        self.assertEqual(multi_floor, {})

    def test_location_max_tier_named_sanctum_quests(self) -> None:
        self.assertGreaterEqual(get_location_max_tier("Makin' a Wizwand", "Sanctum"), 2)
        self.assertGreaterEqual(get_location_max_tier("Wicked Wizboars", "Sanctum"), 2)
        self.assertEqual(get_location_max_tier("Scaling the Tower", "Sanctum"), 1)
        self.assertEqual(get_location_max_tier("Killing Tomb", "Arcwood Pass"), 1)
        self.assertEqual(get_location_max_tier("Buy Item #1 from Sally's Nook", "Sanctum"), 1)

    def test_useful_item_name_fits_unfilled_respects_per_location_tier(self) -> None:
        from worlds.atlyss.ProgressionLogic import (
            _location_max_tier,
            _non_junk_unfilled_locations,
            _useful_item_name_fits_unfilled,
        )

        class _Region:
            def __init__(self, name: str) -> None:
                self.name = name

        class _Loc:
            def __init__(self, name: str, region_name: str) -> None:
                self.name = name
                self.parent_region = _Region(region_name)

        unfilled = [
            _Loc("Night Spirits", "Sanctum"),
            _Loc("Reach Level 4", "Menu"),
            _Loc("Fishing Lv. 1", "Menu"),
        ]
        non_junk = _non_junk_unfilled_locations(unfilled)
        self.assertEqual(_location_max_tier(non_junk[0]), 1)
        self.assertTrue(_useful_item_name_fits_unfilled("Ragged Shirt", non_junk))
        self.assertFalse(_useful_item_name_fits_unfilled("Iron Katars", non_junk))
