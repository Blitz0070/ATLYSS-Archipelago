"""
Shared access tables for Rules, ProgressionLogic, GoalScope, and Regions.

Shop AP row unlock + tier levels (must match client ArchipelagoShopSlotAccess).
Story quest keys must match QuestAccess quest names (AREA_STORY_QUEST / shop tables).
"""
from __future__ import annotations

from typing import Dict, Tuple

# Progressive portal lines (must match ArchipelagoGameDataTables.cs).
PROGRESSIVE_SANCTUM_PORTAL_ITEM = "Progressive Sanctum Portal"
PROGRESSIVE_TUUL_PORTAL_ITEM = "Progressive Tuul Portal"
PROGRESSIVE_SANCTUM_PORTAL_COUNT = 11
PROGRESSIVE_TUUL_PORTAL_COUNT = 3

PROGRESSIVE_SANCTUM_PORTAL_ORDER = (
    "Outer Sanctum Portal",
    "Arcwood Pass Portal",
    "Sanctum Catacombs lvl 1 Portal",
    "Sanctum Catacombs lvl 2 Portal",
    "Sanctum Catacombs lvl 3 Portal",
    "Effold Terrace Portal",
    "Crescent Road Portal",
    "Luvora Garden Portal",
    "Crescent Keep Portal",
    "Crescent Grove lvl 1 Portal",
    "Crescent Grove lvl 2 Portal",
)

PROGRESSIVE_TUUL_PORTAL_ORDER = (
    "Tuul Valley Portal",
    "Tuul Enclave Portal",
    "Bularr Fortress Portal",
)

# Minimum progressive line counts per named portal (must match ArchipelagoGameDataTables.cs).
PORTAL_PROGRESSIVE_REQUIREMENTS: Dict[str, Tuple[int, int]] = {
    "Outer Sanctum Portal": (1, 0),
    "Arcwood Pass Portal": (2, 0),
    "Sanctum Catacombs lvl 1 Portal": (3, 0),
    "Sanctum Catacombs lvl 2 Portal": (4, 0),
    "Sanctum Catacombs lvl 3 Portal": (5, 0),
    "Effold Terrace Portal": (6, 0),
    "Tuul Valley Portal": (6, 1),
    "Crescent Road Portal": (7, 1),
    "Luvora Garden Portal": (8, 1),
    "Crescent Keep Portal": (9, 1),
    "Tuul Enclave Portal": (9, 2),
    "Crescent Grove lvl 1 Portal": (10, 2),
    "Crescent Grove lvl 2 Portal": (11, 2),
    "Bularr Fortress Portal": (11, 3),
}

# All AP shop rows unlock together at Catacombs lvl 2 (crown grind band). Playtest gate; may split per-slot later.
SHOP_AP_ITEMS_PORTAL_GATE = "sanctum_catacombs_f2"

# Tier budgets / goal trim only (not used for slot visibility).
SHOP_SLOT_TIER_LEVELS = (4, 8, 12, 16, 20)

# First visit to a zone: portal route only (Regions.py uses region_rule / has_area).
# Do not gate an entrance on a quest that completes inside that zone.
REGION_ENTRANCE_STORY_QUEST: Dict[str, str] = {}

# Deeper gameplay on a route after a story beat (not first portal hop).
AREA_STORY_QUEST: Dict[str, str] = {
    "Sanctum Catacombs lvl 2": "Communing Catacombs",
    "Sanctum Catacombs lvl 3": "Communing Catacombs",
    "Crescent Grove lvl 2": "The Keep Within",
}

# Extra shop gates beyond portal route (catacombs vendors after Communing ritual).
SHOP_MERCHANT_STORY_QUEST: Dict[str, str] = {
    "Tesh's Wares": "Communing Catacombs",
    "Nesh's Wares": "Communing Catacombs",
}

SHOP_MERCHANT_AREA = {
    "Sally's Nook": "Sanctum",
    "Skrit's Sikrit Market": "Sanctum",
    "Dye Merchant": "Sanctum",
    "Ruka's Furnace": "Sanctum",
    "Torta's Fishing Shack": "Sanctum",
    "Mad Statue's Gift": "Sanctum",
}

SHOP_MERCHANT_GATE = {
    "Frankie's Goods": "arcwood_pass",
    "Tesh's Wares": "sanctum_catacombs_f2",
    "Nesh's Wares": "sanctum_catacombs_f3",
    "Rikko's Treasures": "crescent_grove_colossus",
    "Cotoo's Treasures": "crescent_grove_lvl2",
}


def progressive_requirements_for_portal(portal_name: str) -> Tuple[int, int]:
    """Minimum sanctum/tuul progressive counts to unlock a named portal in progressive mode."""
    return PORTAL_PROGRESSIVE_REQUIREMENTS.get(portal_name, (0, 0))


def shop_ap_items_portal_gate() -> str:
    """Portal gate id shared by every AP shop slot (client uses the same gate)."""
    return SHOP_AP_ITEMS_PORTAL_GATE


def shop_slot_tier_level(merchant: str, slot: int) -> int:
    """Effective level for equipment tier placement on shop checks."""
    if merchant == "Sally's Nook" and slot == 1:
        return 1
    index = max(1, min(slot, len(SHOP_SLOT_TIER_LEVELS))) - 1
    return SHOP_SLOT_TIER_LEVELS[index]


def parse_shop_buy_location(location_name: str) -> tuple[int, str] | None:
    prefix = "Buy Item #"
    marker = " from "
    if not location_name.startswith(prefix) or marker not in location_name:
        return None
    slot_text, merchant = location_name[len(prefix):].split(marker, 1)
    return int(slot_text), merchant


def validate_story_quest_names(quest_names: set[str]) -> None:
    required = set(AREA_STORY_QUEST.values()) | set(SHOP_MERCHANT_STORY_QUEST.values())
    missing = required - quest_names
    if missing:
        raise ValueError(f"Story quest gates reference unknown quests: {sorted(missing)}")
    if not REGION_ENTRANCE_STORY_QUEST.items() <= AREA_STORY_QUEST.items():
        raise ValueError("AREA_STORY_QUEST must include all REGION_ENTRANCE_STORY_QUEST entries")


def quest_requires_pickaxe(quest_name: str) -> bool:
    """Mining turn-in quests only (mob-drop Sally forge quests use kill_enemies, not pickaxe)."""
    return quest_name in (
        "Dense Ingots",
        "Amberite Ingots",
        "Sapphite Ingots",
    )


# Fish trade-in quest names match these caught-fish items (TRADEITEM_* in the mod).
FISH_TRADE_QUEST_NAMES = frozenset({
    "Bittering Katfish",
    "Bonefish",
    "Smiling Wrellfish",
    "Squangfish",
    "Sugeel",
    "Sugshrimp",
    "Windtail Fish",
    "Old Boot",
})


def quest_requires_fishing_rod(quest_name: str) -> bool:
    """Fish turn-in quests need a fishing rod to catch trade fish."""
    if quest_name in FISH_TRADE_QUEST_NAMES:
        return True
    return quest_name.endswith(" Fish")
