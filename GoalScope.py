"""
Goal-scoped location placement.

Omit checks beyond the selected victory condition so generation does not place
items on locations the player would never need for that goal (e.g. Slime Diva
drops late bosses, grove merchants, and high level milestones).

Quest min-levels come from QuestAccess.QUEST_ACCESS; other checks parsed from Rules.py.
"""
from __future__ import annotations

import re
from typing import Dict, Optional, Set

from .Locations import bosses, enemy_data, location_grind_data

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


def _load_rules_source() -> str:
    """Load Rules.py text from the apworld package (works inside .apworld zips)."""
    pkg = __package__ or "atlyss"
    try:
        from importlib import resources
        return resources.files(pkg).joinpath("Rules.py").read_text(encoding="utf-8")
    except Exception:
        import inspect
        from . import Rules
        return inspect.getsource(Rules)


def _parse_min_grind_levels_from_rules(rules_text: str) -> Dict[str, int]:
    levels: Dict[str, int] = {}
    patterns = (
        r'"([^"]+)":\s*lambda[^:]*can_grind_level\(state,\s*player,\s*(\d+)\)',
        r'"([^"]+)":\s*lambda[^:]*can_grind_fish\(state,\s*player,\s*(\d+)\)',
        r'"([^"]+)":\s*lambda[^:]*can_grind_mine\(state,\s*player,\s*(\d+)\)',
    )
    for pattern in patterns:
        for match in re.finditer(pattern, rules_text):
            name, level = match.group(1), int(match.group(2))
            if name not in levels or level < levels[name]:
                levels[name] = level
    return levels


def _get_location_min_grind_levels() -> Dict[str, int]:
    global _location_min_grind_levels
    if _location_min_grind_levels is None:
        from .QuestAccess import QUEST_ACCESS

        levels = {name: level for name, (level, _after, _gate) in QUEST_ACCESS.items()}
        parsed = _parse_min_grind_levels_from_rules(_load_rules_source())
        for name, level in parsed.items():
            if name not in levels or level < levels[name]:
                levels[name] = level
        _location_min_grind_levels = levels
    return _location_min_grind_levels


def _region_min_entry_level(region_name: str) -> int:
    for area_name, min_level, _max_level in location_grind_data:
        if area_name == region_name:
            return min_level
    return 0


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
