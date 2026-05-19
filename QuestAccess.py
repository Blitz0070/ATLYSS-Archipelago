"""
Quest access plus shared portal gates.

PORTAL_GATES are reusable portal-route profiles. Any rule that needs a specific
route (quests, shops, achievements, bosses, professions) should reference the
same gate id instead of rebuilding named/progressive portal logic locally.

See Rules.py header for progressive portal order (1=Outer … 14=Bularr).
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

from .Locations import quests

OUTER_SANCTUM_PORTAL = "Outer Sanctum Portal"
CATACOMBS_LVL1_PORTAL = "Sanctum Catacombs lvl 1 Portal"
CATACOMBS_LVL2_PORTAL = "Sanctum Catacombs lvl 2 Portal"
CATACOMBS_LVL3_PORTAL = "Sanctum Catacombs lvl 3 Portal"
GROVE_LVL1_PORTAL = "Cresent Grove lvl 1 Portal"
GROVE_LVL2_PORTAL = "Cresent Grove lvl 2 Portal"

# (random_mode_portal_items, progressive_unlock_count)
# Random mode: every gate below includes Outer Sanctum (hub exit). Progressive
# mode: unlock count only (Outer is always unlock #1 in the chain).
PortalGate = Tuple[Tuple[str, ...], int]

# Gate ids name portals/areas, not story beats.
PORTAL_GATES: Dict[str, PortalGate] = {
    "outer_sanctum": ((OUTER_SANCTUM_PORTAL,), 1),
    "arcwood_pass": ((OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal"), 2),
    "sanctum_catacombs": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", CATACOMBS_LVL1_PORTAL), 3,
    ),
    "sanctum_catacombs_f2": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", CATACOMBS_LVL1_PORTAL, CATACOMBS_LVL2_PORTAL), 4,
    ),
    "sanctum_catacombs_f3": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal",
            CATACOMBS_LVL1_PORTAL, CATACOMBS_LVL2_PORTAL, CATACOMBS_LVL3_PORTAL,
        ),
        5,
    ),
    "effold_terrace": ((OUTER_SANCTUM_PORTAL, "Effold Terrace Portal"), 6),
    "tuul_valley": ((OUTER_SANCTUM_PORTAL, "Tuul Valley Portal"), 7),
    "crescent_road": ((OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Cresent Road Portal"), 8),
    "crescent_keep": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Cresent Road Portal", "Cresent Keep Portal"), 10,
    ),
    "tuul_enclave": ((OUTER_SANCTUM_PORTAL, "Tuul Valley Portal", "Tuul Enclave Portal"), 11),
    "luvora_garden": ((OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Cresent Road Portal", "Luvora Garden Portal"), 9),
    "crescent_grove_colossus": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Cresent Road Portal", "Cresent Keep Portal", GROVE_LVL1_PORTAL
        ),
        12,
    ),
    "crescent_grove_lvl2": (
        (OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Cresent Road Portal", "Cresent Keep Portal", GROVE_LVL1_PORTAL, GROVE_LVL2_PORTAL), 13,
    ),
    "bularr_fortress": (
        (
            OUTER_SANCTUM_PORTAL, "Tuul Valley Portal",
            "Tuul Enclave Portal", "Bularr Fortress Portal",
        ),
        14,
    ),
    "craft_mekspear": (
        (
            OUTER_SANCTUM_PORTAL, "Tuul Valley Portal", "Effold Terrace Portal",
        ),
        7,
    ),
    "craft_wizwand": (
        (
            OUTER_SANCTUM_PORTAL, "Tuul Valley Portal", "Arcwood Pass Portal", "Cresent Road Portal", 
        ),
        8,
    ),
    "craft_vile_blade": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", CATACOMBS_LVL1_PORTAL, CATACOMBS_LVL2_PORTAL,
            "Cresent Road Portal", "Effold Terrace Portal",
        ),
        8,
    ),
    "craft_golem_chest": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Cresent Road Portal"
        ),
        10,
    ),
    "glyphik_route": (
        (
            OUTER_SANCTUM_PORTAL, "Arcwood Pass Portal", "Cresent Road Portal", "Cresent Keep Portal", "Luvora Garden Portal", "Tuul Valley Portal", "Tuul Enclave Portal",
            GROVE_LVL1_PORTAL, GROVE_LVL2_PORTAL, "Bularr Fortress Portal",
        ),
        14,
    ),
}


def _random_portals_for_gate(random_items: tuple) -> tuple:
    """Random portals: Outer Sanctum required before any other area portal."""
    if OUTER_SANCTUM_PORTAL not in random_items:
        return (OUTER_SANCTUM_PORTAL,) + random_items
    return random_items


def get_portal_gate(gate_id: str) -> PortalGate:
    """Return (random named portals, progressive count) for a shared gate id."""
    random_items, progressive = PORTAL_GATES[gate_id]
    return _random_portals_for_gate(random_items), progressive

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
    "The Voice of Zuulneruda": (6, "Killing Tomb", "sanctum_catacombs"),
    "Purging the Undead": (6, "Killing Tomb", "sanctum_catacombs"),
    "Rattlecage Rage": (6, "Killing Tomb", "sanctum_catacombs"),
    "Consumed Madness": (12, "The Voice of Zuulneruda", "sanctum_catacombs_f2"),
    "Eradicating the Undead": (12, "The Voice of Zuulneruda", "sanctum_catacombs_f2"),
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
    "Makin' a Ragespear": (15, "Makin' a Mekspear", "bularr_fortress"),
    "Makin' More Ragespears": (15, "Makin' a Ragespear", "bularr_fortress"),
    "Makin' a Monolith Chestpiece": (16, "Makin' a Golem Chestpiece", "bularr_fortress"),
    "Summore' Monolith Chestpieces": (16, "Makin' a Monolith Chestpiece", "bularr_fortress"),
    "Makin' a Firebreath Blade": (20, None, "crescent_grove_lvl2"),
    "Summore' Firebreath Blades": (20, "Makin' a Firebreath Blade", "crescent_grove_lvl2"),
    "Makin' a Follycannon": (24, None, "bularr_fortress"),
    "Makin' More Follycannons": (24, "Makin' a Follycannon", "bularr_fortress"),
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


_validate_quest_table()


def _make_quest_rule(player: int, level: int, after: Optional[str], gate_id: Optional[str]):
    if gate_id:
        random_items, progressive = get_portal_gate(gate_id)
    else:
        random_items, progressive = (), 0

    def rule(state):
        from .Rules import can_grind_level, has_portal_access, has_quest

        if not can_grind_level(state, player, level):
            return False
        if after is not None and not has_quest(state, player, after):
            return False
        if gate_id is not None:
            return has_portal_access(state, player, random_items, progressive)
        return True

    return rule


def get_quest_rule_map(player: int) -> dict:
    """Access rules for every entry in Locations.quests."""
    return {
        name: _make_quest_rule(player, level, after, gate)
        for name, (level, after, gate) in QUEST_ACCESS.items()
    }
