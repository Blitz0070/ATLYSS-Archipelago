"""
Region entrance rules (Phase B): portal access plus minimum grind level per area.

Keeps baseline region names / portal item spellings; adds fork-style level gates on
entrances so logic cannot treat high-level zones as reachable with portals alone.
"""
from __future__ import annotations

from typing import Callable, Dict

from .Locations import location_grind_data

# region name -> minimum character level to treat the area as enterable
REGION_MIN_ENTRY_LEVEL: Dict[str, int] = {
    area_name: min_level for area_name, min_level, _max_level in location_grind_data
}


def can_access_region(state, player: int, region_name: str) -> bool:
    """Portal unlock (or progressive count) and area min level from grind tables."""
    from .Rules import can_grind_level, has_area

    if not has_area(state, player, region_name):
        return False
    min_level = REGION_MIN_ENTRY_LEVEL.get(region_name, 1)
    if min_level <= 1:
        return True
    return can_grind_level(state, player, min_level)


def region_rule(player: int, region_name: str, extra: Callable | None = None):
    """Build an entrance access_rule with optional quest / story predicate."""

    def rule(state, p=player, rn=region_name, ex=extra):
        if not can_access_region(state, p, rn):
            return False
        return ex(state) if ex is not None else True

    return rule
