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
from worlds.atlyss.Locations import portal_counts
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
        self.assertTrue(quest_requires_pickaxe("Makin' a Mekspear"))
        self.assertTrue(quest_requires_pickaxe("Summore' Golem Chestpieces"))
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
        source = (_WORLD_ROOT / "QuestAccess.py").read_text(encoding="utf-8")
        for quest in ("The Voice of Zuulneruda", "Purging the Undead", "Rattlecage Rage"):
            self.assertIn(
                f'"{quest}": (6, "Killing Tomb", "sanctum_catacombs_f2"),',
                source,
                quest,
            )
        self.assertIn('"Killing Tomb": (1, None, "sanctum_catacombs"),', source)

    def test_location_max_tier_named_sanctum_quests(self) -> None:
        self.assertGreaterEqual(get_location_max_tier("Makin' a Wizwand", "Sanctum"), 2)
        self.assertGreaterEqual(get_location_max_tier("Wicked Wizboars", "Sanctum"), 2)
        self.assertGreaterEqual(get_location_max_tier("Skill Student", "Sanctum"), 2)
        self.assertEqual(get_location_max_tier("Killing Tomb", "Arcwood Pass"), 1)
        self.assertEqual(get_location_max_tier("Buy Item #1 from Sally's Nook", "Sanctum"), 1)
