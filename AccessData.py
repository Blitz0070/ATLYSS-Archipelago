"""
Shared access tables for Rules, ProgressionLogic, GoalScope, and Regions.

Shop AP row unlock + tier levels (must match client ArchipelagoShopSlotAccess).
Story quest keys must match Regions.py entrance gates and QuestAccess quest names.
"""
from __future__ import annotations

from typing import Dict

# All AP shop rows unlock together at Catacombs lvl 2 (crown grind band). Playtest gate; may split per-slot later.
SHOP_AP_ITEMS_PORTAL_GATE = "sanctum_catacombs_f2"

# Tier budgets / goal trim only (not used for slot visibility).
SHOP_SLOT_TIER_LEVELS = (4, 8, 12, 16, 20)

# Regions.py entrance extras (destination region -> completed quest event required).
REGION_ENTRANCE_STORY_QUEST: Dict[str, str] = {
    "Effold Terrace": "Communing Catacombs",
    "Sanctum Catacombs lvl 1": "Communing Catacombs",
    "Cresent Road": "The Keep Within",
    "Bularr Fortress": "Finding Ammagon",
    "Cresent Grove lvl 1": "The Keep Within",
}

# Gameplay access (grind spawns, fishing spots): same gates plus deeper zones on those routes.
AREA_STORY_QUEST: Dict[str, str] = {
    **REGION_ENTRANCE_STORY_QUEST,
    "Sanctum Catacombs lvl 2": "Communing Catacombs",
    "Sanctum Catacombs lvl 3": "Communing Catacombs",
    "Cresent Grove lvl 2": "The Keep Within",
}

# Off-Sanctum shop merchants that sit behind story routes (portal gate alone is not enough).
SHOP_MERCHANT_STORY_QUEST: Dict[str, str] = {
    "Tesh's Wares": "Communing Catacombs",
    "Nesh's Wares": "Communing Catacombs",
    "Rikko's Treasures": "The Keep Within",
    "Cotoo's Treasures": "The Keep Within",
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
    """Ore turn-ins and forge craft chains need a pickaxe to gather materials."""
    if quest_name.endswith(" Ingots"):
        return True
    if quest_name.startswith("Makin'"):
        return True
    return quest_name in (
        "Summore' Golem Chestpieces",
        "Summore' Monolith Chestpieces",
        "Summore' Firebreath Blades",
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
