"""
Quest access plus shared portal gates.

PORTAL_GATES are reusable portal-route profiles. Any rule that needs a specific
route (quests, shops, achievements, bosses, professions) should reference the
same gate id instead of rebuilding named/progressive portal logic locally.

Progressive mode: two lines (Sanctum 11, Tuul 3). Gates store (sanctum_count, tuul_count).
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple, Union

from typing_extensions import NamedTuple

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


PortalGateRef = Union[str, Tuple[str, ...]]

# One AND slot: str = must reach that creep; inner tuple = reach any one (OR).
KillEnemyGroup = Union[str, Tuple[str, ...]]
KillEnemyRequirements = Tuple[KillEnemyGroup, ...]

# str = one prerequisite quest; tuple = all listed quests must be complete (AND).
AfterQuestRef = Union[str, Tuple[str, ...]]


class QuestAccessSpec(NamedTuple):
    """Quest access metadata. min_level trims goals; also gates logic when no portal/kill reqs."""

    min_level: int
    after_quest: Optional[AfterQuestRef] = None
    portal_gates: Optional[PortalGateRef] = None
    kill_enemies: Optional[KillEnemyRequirements] = None


def normalize_after_quest_names(after_quest: Optional[AfterQuestRef]) -> Tuple[str, ...]:
    if after_quest is None:
        return ()
    if isinstance(after_quest, str):
        return (after_quest,)
    if not after_quest:
        raise ValueError("after_quest tuple cannot be empty")
    return after_quest


def normalize_portal_gate_ids(portal_gates: Optional[PortalGateRef]) -> Tuple[str, ...]:
    if portal_gates is None:
        return ()
    if isinstance(portal_gates, str):
        return (portal_gates,)
    return portal_gates


def iter_kill_enemy_names(kill_enemies: KillEnemyRequirements) -> Tuple[str, ...]:
    """Flatten every creep name referenced in kill_enemies groups."""
    names: list[str] = []
    for group in kill_enemies:
        if isinstance(group, str):
            names.append(group)
        elif isinstance(group, tuple):
            names.extend(group)
        else:
            raise TypeError(f"Invalid kill_enemies group type: {type(group)!r}")
    return tuple(names)


def quest_uses_level_access(spec: QuestAccessSpec) -> bool:
    """Level-only quests: no kill_enemies or portal_gates; min_level > 1 uses CanGrindLevel."""
    return (
        spec.min_level > 1
        and not spec.kill_enemies
        and not normalize_portal_gate_ids(spec.portal_gates)
    )


# kill_enemies: AND between top-level entries; str = one creep, tuple = OR among those creeps.
# after_quest: str = one prerequisite; tuple = all prerequisites (AND).
# portal_gates: OR between routes when multiple gate ids are given.
# min_level only: no kill_enemies and no portal_gates, min_level > 1 → CanGrindLevel (same model as Reach Level N).
QUEST_ACCESS: Dict[str, QuestAccessSpec] = {
    # --- Tutorial / main story ---
    "A Warm Welcome": QuestAccessSpec(1),
    "Communing Catacombs": QuestAccessSpec(1, after_quest="A Warm Welcome", portal_gates="sanctum_catacombs"),
    "Diva Must Die": QuestAccessSpec(4, after_quest="Communing Catacombs", kill_enemies=("Slimek", "Slime Diva")),
    "Cleaning Terrace": QuestAccessSpec(5, after_quest="Diva Must Die", kill_enemies=("Slimek", "Slime Diva")),
    "The Keep Within": QuestAccessSpec(8, after_quest="Diva Must Die", portal_gates="crescent_keep"),
    "Ancient Beings": QuestAccessSpec(8, after_quest="The Keep Within", kill_enemies=("Mini Golem", "Golem")),
    "Tethering Grove": QuestAccessSpec(15, after_quest="The Keep Within", portal_gates="crescent_grove_colossus"),
    "The Colossus": QuestAccessSpec(15, after_quest="The Keep Within", kill_enemies=("Colossus",)),
    "Purging the Grove": QuestAccessSpec(15, after_quest="The Colossus", kill_enemies=("Deadwood", "Carbuncle", "Red Minichroom", "Blue Minichroom", "Monolith")),
    "Spiraling In The Grove": QuestAccessSpec(15, after_quest="Tethering Grove", portal_gates="crescent_grove_colossus"),
    "Hell In The Grove": QuestAccessSpec(20, after_quest="Tethering Grove", portal_gates="crescent_grove_lvl2"),
    "Cleansing the Grove": QuestAccessSpec(20, after_quest="The Colossus", kill_enemies=("Barknaught", "Death Knight", "Aqua Muchroom", "Gale Muchroom", "Demigolem")),
    "Finding Ammagon": QuestAccessSpec(14, portal_gates="bularr_fortress"),
    "The Glyphik Booklet": QuestAccessSpec(24, after_quest="Finding Ammagon", portal_gates="glyphik_route"),
    # --- Side / kill quests ---
    "Night Spirits": QuestAccessSpec(1, kill_enemies=("Lesser Wisp", "Greater Wisp")),
    "Ridding Slimes": QuestAccessSpec(1, kill_enemies=("Slime",)),
    "Ghostly Goods": QuestAccessSpec(1, after_quest="A Warm Welcome", kill_enemies=("Lesser Wisp", "Mini Geist")),
    "Killing Tomb": QuestAccessSpec(1, kill_enemies=("Mini Geist", "Geist")),
    "Summore' Spectral Powder!": QuestAccessSpec(1, after_quest="Ghostly Goods", kill_enemies=("Lesser Wisp", "Mini Geist")),
    "The Voice of Zuulneruda": QuestAccessSpec(6, after_quest="Killing Tomb", kill_enemies=("Lord Zuulneruda",)),
    "Purging the Undead": QuestAccessSpec(6, after_quest="Killing Tomb", kill_enemies=("Toxin", "Deathgel", "Geist")),
    "Rattlecage Rage": QuestAccessSpec(6, after_quest="Killing Tomb", portal_gates="sanctum_catacombs_f2"),
    "Consumed Madness": QuestAccessSpec(12, after_quest="The Voice of Zuulneruda", portal_gates="sanctum_catacombs_f3"),
    "Eradicating the Undead": QuestAccessSpec(12, after_quest="The Voice of Zuulneruda", kill_enemies=("Miasma", "Poltergeist", "Hellsludge")),
    "Call of Fury": QuestAccessSpec(4),
    "Focusin' in": QuestAccessSpec(4),
    "Huntin' Hogs": QuestAccessSpec(7, after_quest="A Warm Welcome", kill_enemies=("Mekboar",)),
    "Wicked Wizboars": QuestAccessSpec(10, kill_enemies=("Wizboar",)),
    "Mastery of Strength": QuestAccessSpec(10),
    "Mastery of Dexterity": QuestAccessSpec(10),
    "Mastery of Mind": QuestAccessSpec(10),
    "Beckoning Foes": QuestAccessSpec(12),
    "Whatta' Rush!": QuestAccessSpec(12),
    # --- Mining turn-ins ---
    "Dense Ingots": QuestAccessSpec(1, portal_gates=("arcwood_pass", "effold_terrace")),
    "Amberite Ingots": QuestAccessSpec(6, after_quest="Dense Ingots", portal_gates=("tuul_valley", "crescent_keep")),
    "Sapphite Ingots": QuestAccessSpec(8, after_quest="Amberite Ingots", portal_gates=("arcwood_pass", "effold_terrace", "tuul_valley", "tuul_enclave")),
    # --- Crafting chains ---
    "Makin' a Mekspear": QuestAccessSpec(7, kill_enemies=("Mekboar", "Slimek")),
    "Makin' More Mekspears": QuestAccessSpec(7, after_quest="Makin' a Mekspear", kill_enemies=("Mekboar", "Slimek")),
    "Makin' a Wizwand": QuestAccessSpec(10, kill_enemies=("Wizboar", "Blightwood")),
    "Makin' More Wizwands": QuestAccessSpec(10, after_quest="Makin' a Wizwand", kill_enemies=("Wizboar", "Blightwood")),
    "Makin' a Vile Blade": QuestAccessSpec(10, kill_enemies=(("Mouth", "Maw"), "Slimek", "Deathgel")),
    "Makin' More Vile Blades": QuestAccessSpec(10, after_quest="Makin' a Vile Blade", kill_enemies=(("Mouth", "Maw"), "Slimek", "Deathgel")),
    "Makin' a Golem Chestpiece": QuestAccessSpec(12, after_quest="The Keep Within", kill_enemies=("Golem", "Mini Golem")),
    "Summore' Golem Chestpieces": QuestAccessSpec(12, after_quest="Makin' a Golem Chestpiece", kill_enemies=("Golem", "Mini Golem")),
    "Makin' a Ragespear": QuestAccessSpec(
        15,
        after_quest=("Makin' a Mekspear", "Finding Ammagon"),
        kill_enemies=("Rageboar", "Hellsludge"),
    ),
    "Makin' More Ragespears": QuestAccessSpec(15, after_quest="Makin' a Ragespear", kill_enemies=("Rageboar", "Hellsludge")),
    "Makin' a Monolith Chestpiece": QuestAccessSpec(16, after_quest="Makin' a Golem Chestpiece", kill_enemies=("Monolith", "Carbuncle")),
    "Summore' Monolith Chestpieces": QuestAccessSpec(16, after_quest="Makin' a Monolith Chestpiece", kill_enemies=("Monolith", "Carbuncle")),
    "Makin' a Firebreath Blade": QuestAccessSpec(20, kill_enemies=("Firebreath", "Carbuncle")),
    "Summore' Firebreath Blades": QuestAccessSpec(20, after_quest="Makin' a Firebreath Blade", kill_enemies=("Firebreath", "Carbuncle")),
    "Makin' a Follycannon": QuestAccessSpec(24, after_quest="Finding Ammagon", kill_enemies=("Boomboar", ("Mekboar", "Wizboar", "Rageboar"))),
    "Makin' More Follycannons": QuestAccessSpec(24, after_quest="Makin' a Follycannon", kill_enemies=("Boomboar", ("Mekboar", "Wizboar", "Rageboar"))),
    # --- Bularr / Galius ---
    "Reviling the Rageboars": QuestAccessSpec(14, after_quest="Finding Ammagon", kill_enemies=("Rageboar",)),
    "Reviling more Rageboars": QuestAccessSpec(14, after_quest=("Reviling the Rageboars", "Finding Ammagon"), kill_enemies=("Rageboar",)),
    "Facing Foes": QuestAccessSpec(18, after_quest="Finding Ammagon", kill_enemies=("Rageboar", "Boomboar", "Warboar")),
    "Gatling Galius": QuestAccessSpec(22, after_quest="Finding Ammagon", kill_enemies=("Galius",)),
    "The Gall of Galius": QuestAccessSpec(22, after_quest=("Finding Ammagon", "Gatling Galius"), kill_enemies=("Galius",)),
    # --- Grove nulversa (any one of the three in-game quests completes this AP check) ---
    "Nulversa": QuestAccessSpec(20, portal_gates="crescent_grove_lvl2"),
}


def _validate_quest_table() -> None:
    from .Locations import enemy_data

    quest_names = {name for name, _region in quests}
    missing = quest_names - QUEST_ACCESS.keys()
    extra = QUEST_ACCESS.keys() - quest_names
    if missing:
        raise ValueError(f"QUEST_ACCESS missing quests: {sorted(missing)}")
    if extra:
        raise ValueError(f"QUEST_ACCESS unknown quests: {sorted(extra)}")
    for spec in QUEST_ACCESS.values():
        if spec.kill_enemies and spec.portal_gates:
            raise ValueError("Quest access cannot set both kill_enemies and portal_gates")
        for gate_id in normalize_portal_gate_ids(spec.portal_gates):
            if gate_id not in PORTAL_GATES:
                raise ValueError(f"Unknown portal gate id: {gate_id}")
        if spec.kill_enemies:
            for group in spec.kill_enemies:
                if isinstance(group, str):
                    if group not in enemy_data:
                        raise ValueError(f"Quest kill_enemies references unknown creep: {group}")
                elif isinstance(group, tuple):
                    if not group:
                        raise ValueError("Quest kill_enemies OR group cannot be empty")
                    for enemy_name in group:
                        if not isinstance(enemy_name, str):
                            raise TypeError(f"Invalid kill_enemies OR entry: {enemy_name!r}")
                        if enemy_name not in enemy_data:
                            raise ValueError(f"Quest kill_enemies references unknown creep: {enemy_name}")
                else:
                    raise TypeError(f"Invalid kill_enemies group type: {type(group)!r}")
        for prerequisite in normalize_after_quest_names(spec.after_quest):
            if prerequisite not in quest_names:
                raise ValueError(f"Quest after_quest references unknown quest: {prerequisite}")


def _validate_area_to_gate() -> None:
    missing = set(portal_counts) - {"Sanctum"} - set(AREA_TO_GATE)
    if missing:
        raise ValueError(f"AREA_TO_GATE missing portal_counts regions: {sorted(missing)}")
    unknown = set(AREA_TO_GATE.values()) - set(PORTAL_GATES)
    if unknown:
        raise ValueError(f"AREA_TO_GATE references unknown gates: {sorted(unknown)}")


def _validate_portal_gates_referenced() -> None:
    """Every PORTAL_GATES profile must be reachable from quest/area/catalog/route rules."""
    from .AccessData import SHOP_AP_ITEMS_PORTAL_GATE

    referenced: set[str] = set(AREA_TO_GATE.values())
    for spec in QUEST_ACCESS.values():
        referenced.update(normalize_portal_gate_ids(spec.portal_gates))
    referenced.add(SHOP_AP_ITEMS_PORTAL_GATE)
    # Achievement locations (AtlyssRules/catalog.py) and Rules.py mining/fishing routes.
    referenced.update({
        "arcwood_pass",
        "effold_terrace",
        "tuul_valley",
        "tuul_enclave",
        "sanctum_catacombs",
        "sanctum_catacombs_f2",
        "sanctum_catacombs_f3",
        "crescent_grove_colossus",
        "crescent_grove_lvl2",
    })
    orphan = set(PORTAL_GATES) - referenced
    if orphan:
        raise ValueError(f"PORTAL_GATES never referenced: {sorted(orphan)}")


_validate_quest_table()
_validate_area_to_gate()
_validate_portal_gates_referenced()
validate_story_quest_names({name for name, _region in quests})

PICKAXE_REQUIRED_QUESTS = frozenset(
    name for name in QUEST_ACCESS if quest_requires_pickaxe(name)
)
FISHING_ROD_REQUIRED_QUESTS = frozenset(
    name for name in QUEST_ACCESS if quest_requires_fishing_rod(name)
)


