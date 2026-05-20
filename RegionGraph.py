"""
Region entrance rules: portal route (has_area) plus grind band for region min entry level.
"""
from __future__ import annotations

from typing import Callable, Dict

from .Locations import location_grind_data

# region name -> minimum grind level for that area (from location_grind_data)
REGION_MIN_ENTRY_LEVEL: Dict[str, int] = {
    area_name: min_level for area_name, min_level, _max_level in location_grind_data
}


def can_access_region(state, player: int, region_name: str) -> bool:
    """Portal route (has_area_for_gameplay) plus can_grind_level for region min entry."""
    from .Rules import can_grind_level, has_area_for_gameplay

    if not has_area_for_gameplay(state, player, region_name):
        return False
    min_level = REGION_MIN_ENTRY_LEVEL.get(region_name, 1)
    return can_grind_level(state, player, min_level)


def region_rule(player: int, region_name: str, extra: Callable | None = None):
    """Build an entrance access_rule with optional quest / story predicate."""

    def rule(state, p=player, rn=region_name, ex=extra):
        if not can_access_region(state, p, rn):
            return False
        return ex(state) if ex is not None else True

    return rule
