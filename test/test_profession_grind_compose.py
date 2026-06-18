"""Profession grind explain tests (require Archipelago test harness for world options)."""
from __future__ import annotations

from worlds.atlyss.AtlyssRules.custom_rules import CanGrindMining
from worlds.atlyss.AtlyssRules.profession_grind_compose import format_mining_grind_explain

from .bases import AtlyssTestBase


class TestProfessionGrindExplain(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
        "profession_tools": "pool",
    }

    def test_mining_lv4_explain_single_step_player_routes(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        grind = format_mining_grind_explain(world, 4)
        full = CanGrindMining(4).resolve(world).explain_str()
        self.assertEqual(full, f"Pickaxe & {grind}")
        self.assertIn("Progressive Sanctum Portal", grind)
        self.assertIn("Progressive Tuul Portal", grind)
        self.assertNotIn("Mining Lv. 3", grind)
        self.assertNotIn("tuul_valley", grind)

    def test_fishing_lv3_explain_mentions_sanctum_hub(self) -> None:
        from worlds.atlyss.AtlyssRules.custom_rules import CanGrindFishing
        from worlds.atlyss.AtlyssRules.profession_grind_compose import format_fishing_grind_explain

        self.world_setup()
        world = self.multiworld.worlds[self.player]
        grind = format_fishing_grind_explain(world, 3)
        self.assertEqual(grind, "Fishing Lv. 3 (Sanctum)")
        self.assertEqual(
            CanGrindFishing(3).resolve(world).explain_str(),
            "Fishing Rod & Fishing Lv. 3 (Sanctum)",
        )
