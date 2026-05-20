"""
Quest access plus shared portal gates.

PORTAL_GATES are reusable portal-route profiles. Any rule that needs a specific
route (quests, shops, achievements, bosses, professions) should reference the
same gate id instead of rebuilding named/progressive portal logic locally.

Progressive mode: two lines (Sanctum 11, Tuul 3). Gates store (sanctum_count, tuul_count).
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

from .AccessData import (
    quest_requires_fishing_rod,
    quest_requires_pickaxe,
    validate_story_quest_names,
)
from .Locations import portal_counts, quests

OUTER_SANCTUM_PORTAL = "Outer Sanctum Portal"
CATACOMBS_LVL1_PORTAL = "Sanctum Catacombs lvl 1 Portal"
CATACOMBS_LVL2_PORTAL = "Sanctum Catacombs lvl 2 Portal"
CATACOMBS_LVL3_PORTAL = "Sanctum Catacombs lvl 3 Portal"
GROVE_LVL1_PORTAL = "Crescent Grove lvl 1 Portal"
GROVE_LVL2_PORTAL = "Crescent Grove lvl 2 Portal"

# (random_mode_portal_items, progressive_sanctum_count, progressive_tuul_count)
PortalGate = Tuple[Tuple[str, ...], int, int]

# Gate ids name portals/areas, not story beats.
PORTAL_GATES: Dict[str, PortalGate] = {
    "outer_sanctum": ((OUTER_SANCTUM_PORTAL,), 1, 0),
    "arcwood_pass": ((OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal"), 2, 0),
    "sanctum_catacombs": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", CATACOMBS_LVL1_PORTAL), 3, 0,
    ),
    "sanctum_catacombs_f2": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", CATACOMBS_LVL1_PORTAL, CATACOMBS_LVL2_PORTAL), 4, 0,
    ),
    "sanctum_catacombs_f3": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal",
            CATACOMBS_LVL1_PORTAL, CATACOMBS_LVL2_PORTAL, CATACOMBS_LVL3_PORTAL,
        ),
        5, 0,
    ),
    "effold_terrace": ((OUTER_SANCTUM_PORTAL, "Effold Terrace Portal"), 6, 0),
    "tuul_valley": ((OUTER_SANCTUM_PORTAL, "Tuul Valley Portal"), 6, 1),
    "crescent_road": ((OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal"), 7, 1),
    "crescent_keep": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal", "Crescent Keep Portal"), 9, 1,
    ),
    "tuul_enclave": ((OUTER_SANCTUM_PORTAL, "Tuul Valley Portal", "Tuul Enclave Portal"), 9, 2),
    "luvora_garden": ((OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal", "Luvora Garden Portal"), 8, 1),
    "crescent_grove_colossus": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal", "Crescent Keep Portal", GROVE_LVL1_PORTAL
        ),
        10, 2,
    ),
    "crescent_grove_lvl2": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal", "Crescent Keep Portal", GROVE_LVL1_PORTAL, GROVE_LVL2_PORTAL), 11, 2,
    ),
    "bularr_fortress": (
        (
            OUTER_SANCTUM_PORTAL, "Tuul Valley Portal",
            "Tuul Enclave Portal", "Bularr Fortress Portal",
        ),
        11, 3,
    ),
    "craft_mekspear": (
        (
            OUTER_SANCTUM_PORTAL, "Tuul Valley Portal", "Effold Terrace Portal",
        ),
        6, 1,
    ),
    "craft_wizwand": (
        (
            OUTER_SANCTUM_PORTAL, "Tuul Valley Portal", "Arcwood Pass Portal", "Crescent Road Portal",
        ),
        7, 1,
    ),
    "craft_vile_blade": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", CATACOMBS_LVL1_PORTAL, CATACOMBS_LVL2_PORTAL,
            "Crescent Road Portal", "Effold Terrace Portal",
        ),
        7, 1,
    ),
    "craft_golem_chest": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal"
        ),
        9, 1,
    ),
    "craft_ragespear": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Effold Terrace Portal",
            CATACOMBS_LVL1_PORTAL, CATACOMBS_LVL2_PORTAL, CATACOMBS_LVL3_PORTAL, "Tuul Valley Portal", "Tuul Enclave Portal", "Bularr Fortress Portal",
        ),
        11, 3,
    ),
    "craft_monolith_chest": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal", "Crescent Keep Portal", GROVE_LVL1_PORTAL),
        10, 2,
    ),
    "craft_firebreath_blade": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal", "Crescent Keep Portal", GROVE_LVL1_PORTAL, GROVE_LVL2_PORTAL),
        11, 2,
    ),
    "craft_follycannon": (
        (OUTER_SANCTUM_PORTAL, "Tuul Valley Portal", "Tuul Enclave Portal", "Bularr Fortress Portal"),
        11, 3,
    ),
    "glyphik_route": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Crescent Road Portal", "Crescent Keep Portal", "Luvora Garden Portal", "Tuul Valley Portal", "Tuul Enclave Portal",
            GROVE_LVL1_PORTAL, GROVE_LVL2_PORTAL, "Bularr Fortress Portal",
        ),
        11, 3,
    ),
}

# Region names (portal_counts / grind tables) -> PORTAL_GATES key (random_portals full route).
AREA_TO_GATE: Dict[str, str] = {
    "Outer Sanctum": "outer_sanctum",
    "Arcwood Pass": "arcwood_pass",
    "Sanctum Catacombs lvl 1": "sanctum_catacombs",
    "Sanctum Catacombs lvl 2": "sanctum_catacombs_f2",
    "Sanctum Catacombs lvl 3": "sanctum_catacombs_f3",
    "Effold Terrace": "effold_terrace",
    "Tuul Valley": "tuul_valley",
    "Crescent Road": "crescent_road",
    "Luvora Garden": "luvora_garden",
    "Crescent Keep": "crescent_keep",
    "Tuul Enclave": "tuul_enclave",
    "Crescent Grove lvl 1": "crescent_grove_colossus",
    "Crescent Grove lvl 2": "crescent_grove_lvl2",
    "Bularr Fortress": "bularr_fortress",
}


def get_area_portal_gate(area_name: str) -> Optional[str]:
    """PORTAL_GATES id for a grind/region area, or None (caller may fall back)."""
    return AREA_TO_GATE.get(area_name)


def _random_portals_for_gate(random_items: tuple) -> tuple:
    """Random portals: Outer Sanctum required before any other area portal."""
    if OUTER_SANCTUM_PORTAL not in random_items:
        return (OUTER_SANCTUM_PORTAL,) + random_items
    return random_items


def get_portal_gate(gate_id: str) -> PortalGate:
    """Return (random named portals, sanctum prog count, tuul prog count) for a gate id."""
    random_items, sanctum, tuul = PORTAL_GATES[gate_id]
    return _random_portals_for_gate(random_items), sanctum, tuul

# quest_name -> (min_level, after_quest, portal_gate_id) — gate ids match PORTAL_GATES keys
QUEST_ACCESS: Dict[str, Tuple[int, Optional[str], Optional[str]]] = {
    # --- Tutorial / main story ---
    "A Warm Welcome": (1, None, None),
    "Communing Catacombs": (1, "A Warm Welcome", "sanctum_catacombs"),
    "Diva Must Die": (4, "Communing Catacombs", "effold_terrace"),
    "Cleaning Terrace": (5, "Diva Must Die", "effold_terrace"),
    "The Keep Within": (8, "Diva Must Die", "crescent_keep"),
    "Ancient Beings": (8, "The Keep Within", "crescent_keep"),
    "Tethering Grove": (15, "The Keep Within", "crescent_grove_colossus"),
    "The Colossus": (15, "The Keep Within", "crescent_grove_colossus"),
    "Purging the Grove": (15, "The Colossus", "crescent_grove_colossus"),
    "Spiraling In The Grove": (15, "Tethering Grove", "crescent_grove_colossus"),
    "Hell In The Grove": (20, "Tethering Grove", "crescent_grove_lvl2"),
    "Cleansing the Grove": (20, "The Colossus", "crescent_grove_lvl2"),
    "Finding Ammagon": (14, None, "bularr_fortress"),
    "The Glyphik Booklet": (24, "Finding Ammagon", "glyphik_route"),
    # --- Side / kill quests (Improved-Logic portal rules) ---
    "Night Spirits": (1, None, "arcwood_pass"),
    "Ridding Slimes": (1, None, "outer_sanctum"),
    "Ghostly Goods": (1, "A Warm Welcome", "sanctum_catacombs"),
    "Killing Tomb": (1, None, "sanctum_catacombs"),
    "Summore' Spectral Powder!": (1, "Ghostly Goods", "sanctum_catacombs"),
    "The Voice of Zuulneruda": (6, "Killing Tomb", "sanctum_catacombs_f2"),
    "Purging the Undead": (6, "Killing Tomb", "sanctum_catacombs_f2"),
    "Rattlecage Rage": (6, "Killing Tomb", "sanctum_catacombs_f2"),
    "Consumed Madness": (12, "The Voice of Zuulneruda", "sanctum_catacombs_f3"),
    "Eradicating the Undead": (12, "The Voice of Zuulneruda", "sanctum_catacombs_f3"),
    "Call of Fury": (4, None, "outer_sanctum"),
    "Focusin' in": (4, None, "outer_sanctum"),
    "Huntin' Hogs": (7, "Diva Must Die", "tuul_valley"),
    "Wicked Wizboars": (10, None, "tuul_valley"),
    "Mastery of Strength": (10, None, "crescent_road"),
    "Mastery of Dexterity": (10, None, "crescent_road"),
    "Beckoning Foes": (12, None, "luvora_garden"),
    "Whatta' Rush!": (12, None, "luvora_garden"),
    # --- Mining turn-ins ---
    "Dense Ingots": (1, None, "arcwood_pass"),
    "Amberite Ingots": (6, "Dense Ingots", "tuul_valley"),
    "Sapphite Ingots": (8, "Amberite Ingots", "tuul_enclave"),
    # --- Crafting chains ---
    "Makin' a Mekspear": (7, None, "craft_mekspear"),
    "Makin' More Mekspears": (7, "Makin' a Mekspear", "craft_mekspear"),
    "Makin' a Wizwand": (10, None, "craft_wizwand"),
    "Makin' More Wizwands": (10, "Makin' a Wizwand", "craft_wizwand"),
    "Makin' a Vile Blade": (10, None, "craft_vile_blade"),
    "Makin' More Vile Blades": (10, "Makin' a Vile Blade", "craft_vile_blade"),
    "Makin' a Golem Chestpiece": (12, "The Keep Within", "craft_golem_chest"),
    "Summore' Golem Chestpieces": (12, "Makin' a Golem Chestpiece", "craft_golem_chest"),
    "Makin' a Ragespear": (15, "Makin' a Mekspear", "craft_ragespear"),
    "Makin' More Ragespears": (15, "Makin' a Ragespear", "craft_ragespear"),
    "Makin' a Monolith Chestpiece": (16, "Makin' a Golem Chestpiece", "craft_monolith_chest"),
    "Summore' Monolith Chestpieces": (16, "Makin' a Monolith Chestpiece", "craft_monolith_chest"),
    "Makin' a Firebreath Blade": (20, None, "craft_firebreath_blade"),
    "Summore' Firebreath Blades": (20, "Makin' a Firebreath Blade", "craft_firebreath_blade"),
    "Makin' a Follycannon": (24, None, "craft_follycannon"),
    "Makin' More Follycannons": (24, "Makin' a Follycannon", "craft_follycannon"),
    # --- Bularr / Galius ---
    "Reviling the Rageboars": (14, None, "bularr_fortress"),
    "Reviling more Rageboars": (14, "Reviling the Rageboars", "bularr_fortress"),
    "Facing Foes": (18, None, "bularr_fortress"),
    "Gatling Galius": (22, None, "bularr_fortress"),
    "The Gall of Galius": (22, "Gatling Galius", "bularr_fortress"),
    # --- Grove nulversa (level-gated; same areas as late grove) ---
    "Nulversa Magica": (20, None, "crescent_grove_lvl2"),
    "Nulversa Viscera": (20, None, "crescent_grove_lvl2"),
    "Nulversa, Greenversa!": (20, None, "crescent_grove_lvl2"),
}


def _validate_quest_table() -> None:
    quest_names = {name for name, _region in quests}
    missing = quest_names - QUEST_ACCESS.keys()
    extra = QUEST_ACCESS.keys() - quest_names
    if missing:
        raise ValueError(f"QUEST_ACCESS missing quests: {sorted(missing)}")
    if extra:
        raise ValueError(f"QUEST_ACCESS unknown quests: {sorted(extra)}")
    for gate_id in {g for _, _, g in QUEST_ACCESS.values() if g}:
        if gate_id not in PORTAL_GATES:
            raise ValueError(f"Unknown portal gate id: {gate_id}")


def _validate_area_to_gate() -> None:
    missing = set(portal_counts) - {"Sanctum"} - set(AREA_TO_GATE)
    if missing:
        raise ValueError(f"AREA_TO_GATE missing portal_counts regions: {sorted(missing)}")
    unknown = set(AREA_TO_GATE.values()) - set(PORTAL_GATES)
    if unknown:
        raise ValueError(f"AREA_TO_GATE references unknown gates: {sorted(unknown)}")


_validate_quest_table()
_validate_area_to_gate()
validate_story_quest_names({name for name, _region in quests})

PICKAXE_REQUIRED_QUESTS = frozenset(
    name for name in QUEST_ACCESS if quest_requires_pickaxe(name)
)
FISHING_ROD_REQUIRED_QUESTS = frozenset(
    name for name in QUEST_ACCESS if quest_requires_fishing_rod(name)
)


def _make_quest_rule(player: int, level: int, after: Optional[str], gate_id: Optional[str]):
    if gate_id:
        random_items, sanctum_prog, tuul_prog = get_portal_gate(gate_id)
    else:
        random_items, sanctum_prog, tuul_prog = (), 0, 0

    def rule(state):
        from .Rules import can_grind_level, has_portal_access, has_quest

        if not can_grind_level(state, player, level):
            return False
        if after is not None and not has_quest(state, player, after):
            return False
        if gate_id is not None:
            if not has_portal_access(state, player, random_items, sanctum_prog, tuul_prog):
                return False
        return True

    return rule


def get_quest_rule_map(player: int) -> dict:
    """Access rules for every entry in Locations.quests."""
    rules = {
        name: _make_quest_rule(player, level, after, gate)
        for name, (level, after, gate) in QUEST_ACCESS.items()
    }
    for name in PICKAXE_REQUIRED_QUESTS:
        base = rules[name]

        def pickaxe_rule(state, _base=base):
            from .Rules import has_mining_tool_for_logic

            return _base(state) and has_mining_tool_for_logic(state, player)

        rules[name] = pickaxe_rule
    for name in FISHING_ROD_REQUIRED_QUESTS:
        base = rules[name]

        def fishing_rod_rule(state, _base=base):
            from .Rules import has_fishing_tool_for_logic

            return _base(state) and has_fishing_tool_for_logic(state, player)

        rules[name] = fishing_rod_rule
    return rules
