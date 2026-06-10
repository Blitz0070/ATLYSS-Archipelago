"""Quest access via kill_enemies and OR portal gates."""
from __future__ import annotations

from BaseClasses import CollectionState

from .bases import AtlyssTestBase
from worlds.atlyss.AtlyssRules.custom_rules import QuestCheck


def _quest_completion_location(quest_name: str) -> str:
    return f"Quest Completion: {quest_name}"


def _add_quest_complete(state: CollectionState, player: int, quest_name: str) -> None:
    """HasQuestComplete checks prog_items by Complete: name, not pool items."""
    state.add_item(f"Complete: {quest_name}", player)
    state.stale[player] = True
    state.rule_builder_cache[player].clear()


def _collect_without_sweep(state: CollectionState, item) -> None:
    """Avoid sweep auto-collecting reachable Quest Completion event items."""
    state.collect(item, prevent_sweep=True)


class TestNightSpiritsKillAccess(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def test_effold_without_arcwood_reaches_night_spirits(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach(_quest_completion_location("Night Spirits"), "Location", self.player),
        )
        for item in self.get_items_by_name(["Outer Sanctum Portal", "Effold Terrace Portal"]):
            state.collect(item)
        self.assertTrue(
            state.can_reach(_quest_completion_location("Night Spirits"), "Location", self.player),
        )

    def test_arcwood_without_effold_reaches_night_spirits(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Outer Sanctum Portal", "Arcwood Pass Portal"]):
            state.collect(item)
        self.assertTrue(
            state.can_reach(_quest_completion_location("Night Spirits"), "Location", self.player),
        )

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
        self.assertTrue(
            state.can_reach(_quest_completion_location("Night Spirits"), "Location", self.player),
        )

    def test_outer_sanctum_alone_blocked(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        state.collect(self.get_items_by_name(["Outer Sanctum Portal"])[0])
        self.assertFalse(
            state.can_reach(_quest_completion_location("Night Spirits"), "Location", self.player),
        )


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
        self.assertTrue(
            state.can_reach(_quest_completion_location("Dense Ingots"), "Location", self.player),
        )


class TestRagespearAfterQuests(AtlyssTestBase):
    options = {
        "goal": "all_quests",
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
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        rule = QuestCheck("Makin' a Ragespear").resolve(world)

        for item in self.get_items_by_name(self._RAGESPEAR_PORTALS):
            _collect_without_sweep(state, item)
        _add_quest_complete(state, self.player, "Communing Catacombs")

        self.assertFalse(rule(state))
        _add_quest_complete(state, self.player, "Makin' a Mekspear")
        self.assertFalse(rule(state))
        _add_quest_complete(state, self.player, "Finding Ammagon")
        self.assertTrue(rule(state))

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
        self.assertTrue(
            state.can_reach(_quest_completion_location("Makin' a Vile Blade"), "Location", self.player),
        )

    def test_vile_blade_explain_shows_or_group(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        resolved = QuestCheck("Makin' a Vile Blade").resolve(world)
        self.assertIn("Mouth", resolved.base_explain)
        self.assertIn("Maw", resolved.base_explain)
        self.assertIn(" or ", resolved.base_explain)
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
        self.assertFalse(
            state.can_reach(_quest_completion_location("Call of Fury"), "Location", self.player),
        )

    def test_call_of_fury_reachable_with_level_grind_access(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Progressive Sanctum Portal"]):
            state.collect(item)
        self.assertTrue(
            state.can_reach(_quest_completion_location("Call of Fury"), "Location", self.player),
        )

    def test_call_of_fury_explain_mentions_level(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        resolved = QuestCheck("Call of Fury").resolve(world)
        self.assertIn("reach level 4", resolved.base_explain)


class TestKillingTombKillEnemiesF1(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def test_f1_portals_reach_killing_tomb_kill_quest(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(
            [
                "Outer Sanctum Portal",
                "Arcwood Pass Portal",
                "Sanctum Catacombs lvl 1 Portal",
            ]
        ):
            _collect_without_sweep(state, item)
        self.assertTrue(
            state.can_reach(_quest_completion_location("Killing Tomb"), "Location", self.player),
        )

    def test_killing_tomb_explain_lists_geists(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        resolved = QuestCheck("Killing Tomb").resolve(world)
        self.assertIn("Mini Geist", resolved.base_explain)
        self.assertIn("Geist", resolved.base_explain)

    def test_arcwood_without_catacombs_blocked(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Outer Sanctum Portal", "Arcwood Pass Portal"]):
            _collect_without_sweep(state, item)
        self.assertFalse(
            state.can_reach(_quest_completion_location("Killing Tomb"), "Location", self.player),
        )


class TestPurgingUndeadAfterKillingTomb(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    _F2_CATACOMBS_PORTALS = [
        "Outer Sanctum Portal",
        "Arcwood Pass Portal",
        "Sanctum Catacombs lvl 1 Portal",
        "Sanctum Catacombs lvl 2 Portal",
    ]

    def test_purging_reachable_after_killing_tomb_without_communing_prog(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(self._F2_CATACOMBS_PORTALS):
            _collect_without_sweep(state, item)
        _add_quest_complete(state, self.player, "Killing Tomb")
        self.assertTrue(
            state.can_reach(_quest_completion_location("Purging the Undead"), "Location", self.player),
        )

    def test_voice_of_zuulneruda_same_f2_band(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(self._F2_CATACOMBS_PORTALS):
            _collect_without_sweep(state, item)
        _add_quest_complete(state, self.player, "Killing Tomb")
        self.assertTrue(
            state.can_reach(
                _quest_completion_location("The Voice of Zuulneruda"),
                "Location",
                self.player,
            ),
        )

    def test_purging_blocked_without_killing_tomb(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(self._F2_CATACOMBS_PORTALS):
            _collect_without_sweep(state, item)
        self.assertFalse(
            state.can_reach(_quest_completion_location("Purging the Undead"), "Location", self.player),
        )


class TestEradicatingUndeadAfterVoice(AtlyssTestBase):
    options = {
        "goal": "all_quests",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    _F3_CATACOMBS_PORTALS = [
        "Outer Sanctum Portal",
        "Arcwood Pass Portal",
        "Sanctum Catacombs lvl 1 Portal",
        "Sanctum Catacombs lvl 2 Portal",
        "Sanctum Catacombs lvl 3 Portal",
    ]

    def test_eradicating_reachable_after_voice_without_communing_prog(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(self._F3_CATACOMBS_PORTALS):
            _collect_without_sweep(state, item)
        _add_quest_complete(state, self.player, "The Voice of Zuulneruda")
        self.assertTrue(
            state.can_reach(
                _quest_completion_location("Eradicating the Undead"),
                "Location",
                self.player,
            ),
        )

    def test_eradicating_blocked_without_voice(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(self._F3_CATACOMBS_PORTALS):
            _collect_without_sweep(state, item)
        self.assertFalse(
            state.can_reach(
                _quest_completion_location("Eradicating the Undead"),
                "Location",
                self.player,
            ),
        )


class TestMakinQuestsNoPickaxeGate(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "true",
        "equipment_progression": "unrestricted",
    }

    def test_mekspear_without_pickaxe(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Outer Sanctum Portal", "Effold Terrace Portal", "Tuul Valley Portal"]):
            state.collect(item)
        self.assertTrue(
            state.can_reach(_quest_completion_location("Makin' a Mekspear"), "Location", self.player),
        )

    def test_mekspear_tuul_route_without_crescent_road(self) -> None:
        """Mekboar is Tuul Valley OR Crescent Keep — Crescent Road must not be required."""
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(["Outer Sanctum Portal", "Effold Terrace Portal", "Tuul Valley Portal"]):
            _collect_without_sweep(state, item)
        self.assertTrue(
            state.can_reach(_quest_completion_location("Makin' a Mekspear"), "Location", self.player),
        )
        resolved = QuestCheck("Makin' a Mekspear").resolve(world)
        self.assertIn("Tuul Valley", resolved.base_explain)
        self.assertNotIn("Crescent Road", resolved.base_explain)

    def test_wizwand_without_pickaxe(self) -> None:
        self.world_setup()
        state = CollectionState(self.multiworld)
        for item in self.get_items_by_name(
            ["Outer Sanctum Portal", "Arcwood Pass Portal", "Crescent Road Portal", "Tuul Valley Portal"]
        ):
            state.collect(item)
        self.assertTrue(
            state.can_reach(_quest_completion_location("Makin' a Wizwand"), "Location", self.player),
        )


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
