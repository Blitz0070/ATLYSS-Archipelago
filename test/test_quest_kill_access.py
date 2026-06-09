"""Quest access via kill_enemies and OR portal gates."""
from __future__ import annotations

from BaseClasses import CollectionState

from .bases import AtlyssTestBase
from worlds.atlyss.AtlyssRules.custom_rules import QuestCheck


class TestNightSpiritsKillAccess(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def test_effold_without_arcwood_reaches_night_spirits(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self.assertFalse(state.can_reach("Night Spirits", "Location", self.player))
        for item in self.get_items_by_name(["Outer Sanctum Portal", "Effold Terrace Portal"]):
            state.collect(item)
        self.assertTrue(state.can_reach("Night Spirits", "Location", self.player))

    def test_arcwood_without_effold_reaches_night_spirits(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Outer Sanctum Portal", "Arcwood Pass Portal"]):
            state.collect(item)
        self.assertTrue(state.can_reach("Night Spirits", "Location", self.player))

    def test_catacombs_route_reaches_night_spirits(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(
            [
                "Outer Sanctum Portal",
                "Arcwood Pass Portal",
                "Sanctum Catacombs lvl 1 Portal",
            ]
        ):
            state.collect(item)
        self.assertTrue(state.can_reach("Night Spirits", "Location", self.player))

    def test_outer_sanctum_alone_blocked(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        state.collect(self.get_items_by_name(["Outer Sanctum Portal"])[0])
        self.assertFalse(state.can_reach("Night Spirits", "Location", self.player))


class TestDenseIngotsOrGates(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def test_effold_without_arcwood_reaches_dense_ingots(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Outer Sanctum Portal", "Effold Terrace Portal"]):
            state.collect(item)
        self.assertTrue(state.can_reach("Dense Ingots", "Location", self.player))


class TestRagespearAfterQuests(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    _RAGESPEAR_PORTALS = [
        "Outer Sanctum Portal",
        "Arcwood Pass Portal",
        "Effold Terrace Portal",
        "Sanctum Catacombs lvl 1 Portal",
        "Sanctum Catacombs lvl 2 Portal",
        "Sanctum Catacombs lvl 3 Portal",
        "Tuul Valley Portal",
        "Tuul Enclave Portal",
        "Bularr Fortress Portal",
    ]

    def test_ragespear_requires_both_prerequisite_quests(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(self._RAGESPEAR_PORTALS):
            state.collect(item)
        self.assertFalse(state.can_reach("Makin' a Ragespear", "Location", self.player))
        state.collect(self.get_items_by_name(["Complete: Makin' a Mekspear"])[0])
        self.assertFalse(state.can_reach("Makin' a Ragespear", "Location", self.player))
        state.collect(self.get_items_by_name(["Complete: Finding Ammagon"])[0])
        self.assertTrue(state.can_reach("Makin' a Ragespear", "Location", self.player))

    def test_ragespear_explain_lists_both_prerequisites(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        resolved = QuestCheck("Makin' a Ragespear").resolve(world)
        self.assertIn("Makin' a Mekspear", resolved.base_explain)
        self.assertIn("Finding Ammagon", resolved.base_explain)


class TestVileBladeOrKillGroups(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def test_mouth_path_without_maw_reaches_vile_blade_quest(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(
            [
                "Outer Sanctum Portal",
                "Arcwood Pass Portal",
                "Crescent Road Portal",
                "Effold Terrace Portal",
                "Sanctum Catacombs lvl 1 Portal",
                "Sanctum Catacombs lvl 2 Portal",
            ]
        ):
            state.collect(item)
        self.assertTrue(state.can_reach("Makin' a Vile Blade", "Location", self.player))

    def test_vile_blade_explain_shows_or_group(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        resolved = QuestCheck("Makin' a Vile Blade").resolve(world)
        self.assertIn("Mouth or Maw", resolved.base_explain)
        self.assertIn("Slimek", resolved.base_explain)
        self.assertIn("Deathgel", resolved.base_explain)


class TestLevelOnlyQuestAccess(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_call_of_fury_uses_grind_level_rule(self) -> None:
        from worlds.atlyss.QuestAccess import QUEST_ACCESS, quest_uses_level_access

        spec = QUEST_ACCESS["Call of Fury"]
        self.assertTrue(quest_uses_level_access(spec))
        self.assertEqual(spec.min_level, 4)

    def test_call_of_fury_blocked_without_grind_access(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self.assertFalse(state.can_reach("Call of Fury", "Location", self.player))

    def test_call_of_fury_reachable_with_level_grind_access(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Progressive Sanctum Portal"]):
            state.collect(item)
        self.assertTrue(state.can_reach("Call of Fury", "Location", self.player))

    def test_call_of_fury_explain_mentions_level(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        resolved = QuestCheck("Call of Fury").resolve(world)
        self.assertIn("reach level 4", resolved.base_explain)


class TestNightSpiritsExplain(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_explain_lists_both_wisps(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        resolved = QuestCheck("Night Spirits").resolve(world)
        self.assertIn("Lesser Wisp", resolved.base_explain)
        self.assertIn("Greater Wisp", resolved.base_explain)
