"""Multiworld generation tests."""
from __future__ import annotations

from .bases import AtlyssTestBase


class TestDefaultOptions(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "random_portals": "false",
        "shop_sanity": "true",
        "achievements": "true",
        "equipment_progression": "unrestricted",
        "profession_tools": "static",
        "class_filter": "all_classes",
        "experience_multiplier": "x1_0",
        "crown_multiplier": "x1_0",
    }


class TestShortRunOptions(AtlyssTestBase):
    options = {
        "goal": "slime_diva",
        "achievements": "false",
        "equipment_progression": "gated",
        "experience_multiplier": "x2_0",
    }


class TestAllQuestsGated(AtlyssTestBase):
    options = {
        "goal": "all_quests",
        "equipment_progression": "gated",
        "profession_tools": "pool",
        "crown_multiplier": "x0_75",
    }


class TestAllBossesUnrestricted(AtlyssTestBase):
    options = {
        "goal": "all_bosses",
        "achievements": "false",
        "equipment_progression": "unrestricted",
    }


class TestRandomPortalsGated(AtlyssTestBase):
    options = {
        "goal": "galius",
        "random_portals": "true",
        "equipment_progression": "gated",
    }


class TestLevel32Gated(AtlyssTestBase):
    options = {
        "goal": "level_32",
        "equipment_progression": "gated",
    }
