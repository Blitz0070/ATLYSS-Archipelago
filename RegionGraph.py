"""
Region entrance rules: portal route plus story/quest gates.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Rule

from .AtlyssRules.custom_rules import CanAccessAreaGameplay

if TYPE_CHECKING:
    pass


def region_entrance_rule(region_name: str, extra: Rule | None = None) -> Rule:
    """Entrance access: portal route + optional extra rule composition."""
    rule: Rule = CanAccessAreaGameplay(region_name)
    if extra is not None:
        rule = rule & extra
    return rule


def region_rule(region_name: str, extra: Rule | None = None) -> Rule:
    """Alias used by Regions.py for entrance connect() rules."""
    return region_entrance_rule(region_name, extra)
