"""
Goal-scoped location placement.

Omit checks beyond the selected victory condition so generation does not place
items on locations the player would never need for that goal (e.g. Slime Diva
drops late bosses, grove merchants, and high level milestones).

Quest min-levels come from QuestAccess.QUEST_ACCESS; other checks use static metadata tables.
"""
from __future__ import annotations

from typing import Dict, Optional, Set

from .AccessData import parse_shop_buy_location, shop_slot_tier_level
from .Locations import (
    achievements,
    merchants,
    bosses,
    enemy_data,
    location_grind_data,
)

# Goal option value -> level cap for trimming (see Options.Goal).
GOAL_LEVEL_CAP: Dict[int, int] = {
    0: 10,   # Slime Diva
    1: 12,   # Lord Zuulneruda
    2: 20,   # Colossus
    3: 26,   # Galius
    4: 18,   # Lord Kaluuz
    5: 25,   # Valdur
    6: 32,   # All Bosses
    7: 32,   # All Quests
    8: 32,   # Level 32
}

GOAL_TARGET_BOSS: Dict[int, str] = {
    0: "Slime Diva",
    1: "Lord Zuulneruda",
    2: "Colossus",
    3: "Galius",
    4: "Lord Kaluuz",
    5: "Valdur",
}

BOSS_LOCATION_NAMES: Set[str] = {row[0] for row in bosses}

# Full location set — no trimming.
_NO_TRIM_GOALS: Set[int] = {6, 7}

_location_min_grind_levels: Optional[Dict[str, int]] = None


_MILESTONE_LEVELS = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32)


def _region_min_entry_level(region_name: str) -> int:
    for area_name, min_level, _max_level in location_grind_data:
        if area_name == region_name:
            return min_level
    return 0


def _region_max_level(region_name: str) -> int:
    for area_name, _min_level, max_level in location_grind_data:
        if area_name == region_name:
            return max_level
    return 0


def _achievement_min_level(name: str, region_name: str) -> int:
    # Preserve old “recommended level” metadata purely for goal trimming.
    if "Catacombs" in name:
        if "(1-6)" in name:
            return 6
        if "(6-12)" in name:
            return 12
        if "(12-18)" in name:
            return 18
    if "Grove" in name:
        if "(15-20)" in name:
            return 20
        if "(20-25)" in name:
            return 25
    if name == "Skill Student":
        return 10
    if name == "Trout Master":
        return 10
    # Default: use region band max (e.g., Sanctum=0 -> becomes 0, treated as always in scope)
    return max(1, _region_max_level(region_name))


def _get_location_min_grind_levels() -> Dict[str, int]:
    global _location_min_grind_levels
    if _location_min_grind_levels is None:
        from .QuestAccess import QUEST_ACCESS

        levels = {name: spec.min_level for name, spec in QUEST_ACCESS.items()}
        # Level milestone locations.
        for level in _MILESTONE_LEVELS:
            levels.setdefault(f"Reach Level {level}", level)

        # Profession grind locations.
        for i in range(1, 11):
            levels.setdefault(f"Fishing Lv. {i}", i)
            levels.setdefault(f"Mining Lv. {i}", i)

        # Shop buy locations: treat as their slot tier for trimming.
        for location_name, _region in merchants:
            parsed = parse_shop_buy_location(location_name)
            if parsed is None:
                continue
            slot, merchant = parsed
            levels.setdefault(location_name, shop_slot_tier_level(merchant, slot))

        # Achievements: keep previous “recommended level” metadata for trimming.
        for location_name, region in achievements:
            levels.setdefault(location_name, _achievement_min_level(location_name, region))

        _location_min_grind_levels = levels
    return _location_min_grind_levels


def should_trim_locations_for_goal(goal: int) -> bool:
    return goal not in _NO_TRIM_GOALS


def location_in_goal_scope(goal: int, location_name: str, region_name: str) -> bool:
    if not should_trim_locations_for_goal(goal):
        return True

    cap = GOAL_LEVEL_CAP.get(goal, 32)

    if location_name in BOSS_LOCATION_NAMES:
        if goal == 6:
            return True
        return location_name == GOAL_TARGET_BOSS.get(goal)

    if location_name.startswith("Reach Level "):
        try:
            milestone = int(location_name.rsplit(" ", 1)[-1])
        except ValueError:
            return True
        return milestone <= cap

    min_level: Optional[int] = _get_location_min_grind_levels().get(location_name)
    if min_level is None and location_name in enemy_data:
        min_level = enemy_data[location_name][0]

    if min_level is not None:
        return min_level <= cap

    if region_name != "Menu":
        return _region_min_entry_level(region_name) <= cap

    return True
