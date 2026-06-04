"""
Region entrance rules: portal route plus story/quest gates.
"""
from __future__ import annotations

from typing import Callable


def can_access_region(state, player: int, region_name: str) -> bool:
    """Portal route + story quest gates (no grind/level gating)."""
    from .Rules import has_area_for_gameplay

    return has_area_for_gameplay(state, player, region_name)


def region_rule(player: int, region_name: str, extra: Callable | None = None):
    """Build an entrance access_rule with optional quest / story predicate."""

    def rule(state, p=player, rn=region_name, ex=extra):
        if not can_access_region(state, p, rn):
            return False
        return ex(state) if ex is not None else True

    return rule
