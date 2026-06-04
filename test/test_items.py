"""Item table sanity."""
from __future__ import annotations

import unittest

from worlds.atlyss.Items import item_name_groups, item_table
from worlds.atlyss.ProfessionToolData import PROFESSION_TOOL_BUYS

_PROFESSION_TOOL_LOCATIONS = {loc for loc, _ in PROFESSION_TOOL_BUYS}


class TestItemsDatapackage(unittest.TestCase):
    def test_item_name_groups_reference_known_items(self) -> None:
        for group_name, names in item_name_groups.items():
            for item_name in names:
                if group_name == "Profession Tools":
                    self.assertIn(
                        item_name,
                        _PROFESSION_TOOL_LOCATIONS,
                        f"{group_name}: {item_name}",
                    )
                else:
                    self.assertIn(item_name, item_table, f"{group_name}: {item_name}")

    def test_progressive_portals_in_progression_group(self) -> None:
        progression = item_name_groups.get("Progression", ())
        self.assertIn("Progressive Sanctum Portal", progression)
        self.assertIn("Progressive Tuul Portal", progression)
