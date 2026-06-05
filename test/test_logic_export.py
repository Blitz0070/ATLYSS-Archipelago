"""Logic export JSON (Phase 3 track A — UT / external consumers)."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from rule_builder.rules import Rule

from .bases import AtlyssTestBase
from worlds.atlyss.AtlyssRules.custom_rules import CanGrindLevel, QuestCheck
from worlds.atlyss.AtlyssRules.export_logic import (
    EXPORT_ANCHOR_ENTRANCES,
    EXPORT_ANCHOR_LOCATIONS,
    LOGIC_EXPORT_SCHEMA_VERSION,
    build_logic_package,
    collect_text_fallback_location_names,
    location_rule_entry,
    rule_payload_has_text_fallback,
    should_export_logic,
    write_logic_export,
)
from worlds.atlyss.AtlyssRules.portal_compose import build_portal_gate_rule


class TestLogicExportPackage(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "equipment_progression": "unrestricted",
    }

    def test_schema_version_and_meta(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        package = build_logic_package(world)
        self.assertEqual(package["schema_version"], LOGIC_EXPORT_SCHEMA_VERSION)
        self.assertEqual(package["game"], "Atlyss")
        self.assertEqual(package["player"], self.player)
        meta = package["meta"]
        self.assertIn("goal", meta)
        self.assertIn("random_portals", meta)
        self.assertIn("item_mapping", meta)
        self.assertIn("Outer Sanctum Portal", meta["item_mapping"])
        self.assertEqual(
            meta["item_mapping"]["Outer Sanctum Portal"],
            "Progressive Sanctum Portal",
        )

    def test_package_size_and_anchor_locations_present(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        package = build_logic_package(world)
        encoded = json.dumps(package)
        self.assertLess(len(encoded), 500_000)
        names = {loc["name"] for loc in package["locations"]}
        for anchor in EXPORT_ANCHOR_LOCATIONS:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, names)

    def test_anchor_entrances_present(self) -> None:
        self.world_setup()
        package = build_logic_package(self.multiworld.worlds[self.player])
        names = {ent["name"] for ent in package["entrances"]}
        for anchor in EXPORT_ANCHOR_ENTRANCES:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, names)

    def test_portal_gate_rule_round_trip_dict(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        rule = build_portal_gate_rule(world, "tuul_valley")
        data = rule.to_dict()
        restored = world.rule_from_dict(data)
        self.assertEqual(restored.to_dict(), data)

    def test_quest_location_rule_round_trip_when_composed(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        entry = location_rule_entry(world, "Wicked Wizboars")
        self.assertIsNotNone(entry)
        assert entry is not None
        rule_data = entry["rule"]
        self.assertIsInstance(rule_data, dict)
        assert isinstance(rule_data, dict)
        self._assert_round_trip(world, rule_data)

    def test_entrance_catacombs_rule_round_trip_when_composed(self) -> None:
        self.options = {**self.options, "goal": "galius", "shop_sanity": "true"}
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        entrance_name = "Sanctum Catacombs lvl 1 -> Sanctum Catacombs lvl 2"
        entrance = world.get_entrance(entrance_name)
        rule_data = entrance.access_rule
        if isinstance(rule_data, Rule.Resolved) and callable(getattr(rule_data, "to_dict", None)):
            self._assert_round_trip(world, rule_data.to_dict())

    def test_quest_check_unresolved_round_trip(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        data = QuestCheck("Wicked Wizboars").to_dict()
        restored = world.rule_from_dict(data)
        self.assertEqual(restored.to_dict(), data)

    def test_grind_level_export_round_trip(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        entry = location_rule_entry(world, "Reach Level 4")
        self.assertIsNotNone(entry)
        assert entry is not None
        rule_data = entry["rule"]
        self.assertIsInstance(rule_data, dict)
        assert isinstance(rule_data, dict)
        self.assertFalse(rule_payload_has_text_fallback(rule_data))
        self._assert_round_trip(world, rule_data)

    def test_boss_location_export_round_trip(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        entry = location_rule_entry(world, "Slime Diva")
        self.assertIsNotNone(entry)
        assert entry is not None
        rule_data = entry["rule"]
        self.assertIsInstance(rule_data, dict)
        assert isinstance(rule_data, dict)
        self.assertFalse(rule_payload_has_text_fallback(rule_data))
        self._assert_round_trip(world, rule_data)

    def test_can_grind_level_rule_direct_round_trip(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        data = CanGrindLevel(8).to_dict()
        restored = world.rule_from_dict(data)
        self.assertEqual(restored.to_dict(), data)

    def test_package_has_no_text_fallback_on_grind_and_boss_anchors(self) -> None:
        self.options = {**self.options, "goal": "galius", "shop_sanity": "true"}
        self.world_setup()
        package = build_logic_package(self.multiworld.worlds[self.player])
        fallbacks = collect_text_fallback_location_names(package)
        for anchor in (
            "Reach Level 4",
            "Reach Level 32",
            "Slime Diva",
            "Galius",
            "Fishing Lv. 3",
            "Buy Fishing Rod",
            "A New Journey",
        ):
            with self.subTest(anchor=anchor):
                self.assertNotIn(anchor, fallbacks)

    def _assert_round_trip(self, world, rule_data: dict) -> None:
        restored = world.rule_from_dict(rule_data)
        self.assertEqual(restored.to_dict(), rule_data)


class TestLogicExportTriggers(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "equipment_progression": "unrestricted",
    }

    def test_should_export_when_settings_enabled(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        world.settings.export_logic = True
        self.assertTrue(should_export_logic(world))

    def test_should_export_when_ut_regen_passthrough(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        world.settings.export_logic = False
        world.multiworld.re_gen_passthrough = {"Atlyss": {"goal": 0}}
        self.assertTrue(should_export_logic(world))

    def test_should_not_export_by_default(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        self.assertFalse(should_export_logic(world))

    def test_write_logic_export_creates_valid_json(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        world.settings.export_logic = True
        with tempfile.TemporaryDirectory() as tmp:
            path = write_logic_export(world, tmp)
            self.assertTrue(path.endswith(f"atlyss_logic_p{self.player}.json"))
            with open(path, encoding="utf-8") as handle:
                loaded = json.load(handle)
            self.assertEqual(loaded["schema_version"], LOGIC_EXPORT_SCHEMA_VERSION)
            self.assertEqual(loaded["player"], self.player)

    def test_generate_output_writes_file_when_export_enabled(self) -> None:
        self.world_setup()
        world = self.multiworld.worlds[self.player]
        world.settings.export_logic = True
        with tempfile.TemporaryDirectory() as tmp:
            world.generate_output(tmp)
            out = Path(tmp) / f"atlyss_logic_p{self.player}.json"
            self.assertTrue(out.is_file())
