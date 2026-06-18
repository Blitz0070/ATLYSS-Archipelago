"""Validate static location tables."""
from __future__ import annotations

import unittest

from worlds.atlyss.Locations import location_dict, location_name_groups


class TestDatapackage(unittest.TestCase):
    def test_location_name_groups_reference_known_locations(self) -> None:
        for group_name, names in location_name_groups.items():
            for loc_name in names:
                self.assertIn(loc_name, location_dict, f"{group_name}: {loc_name}")

    def test_location_groups_cover_core_categories(self) -> None:
        self.assertIn("Slime Diva", location_name_groups["Bosses"])
        self.assertIn("Reach Level 32", location_name_groups["Levels"])
        self.assertIn("A Warm Welcome", location_name_groups["Quests"])

    def test_quest_names_match_location_dict_prefix(self) -> None:
        from worlds.atlyss.Locations import _TRAILING_QUEST_LOCATION_NAMES, quests

        quest_names = [entry[0] for entry in quests]
        spread_quest_names = [
            name for name in quest_names if name not in _TRAILING_QUEST_LOCATION_NAMES
        ]
        self.assertEqual(spread_quest_names, location_dict[: len(spread_quest_names)])
        for trailing in _TRAILING_QUEST_LOCATION_NAMES:
            self.assertIn(trailing, quest_names)
            self.assertIn(trailing, location_dict)
        trailing_start = len(location_dict) - len(_TRAILING_QUEST_LOCATION_NAMES)
        self.assertEqual(
            list(_TRAILING_QUEST_LOCATION_NAMES),
            location_dict[trailing_start:],
        )
        self.assertIn("Mastery of Mind", quest_names)
