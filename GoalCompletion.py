"""
Victory conditions and goal index contract (Phase D).

Indices MUST match Options.Goal, fill_slot_data['goal'], and the mod
(AtlyssArchipelagoPlugin goalOption / goal chat lines). Do not reorder
without updating ArchipelagoGameDataTables and Connection.cs.

Fork Improved-Logic uses 7 goals (no Lord Kaluuz / Valdur singles); see FORK_GOAL_INDEX.
"""
from __future__ import annotations

from typing import Dict, Tuple

from .GoalScope import GOAL_TARGET_BOSS
from .Locations import quests

# yaml option key -> slot_data / Options value
GOAL_KEYS: Tuple[str, ...] = (
    "slime_diva",
    "lord_zuulneruda",
    "colossus",
    "galius",
    "lord_kaluuz",
    "valdur",
    "all_bosses",
    "all_quests",
    "level_32",
)

GOAL_COUNT = len(GOAL_KEYS)

# Mod AllBossGoalNames order
ALL_BOSSES_REQUIRED: Tuple[str, ...] = (
    "Slime Diva",
    "Lord Zuulneruda",
    "Colossus",
    "Galius",
    "Lord Kaluuz",
    "Valdur",
)

# Same set as ArchipelagoGameDataTables.AllQuestToLocation (Locations.quests)
ALL_QUESTS_REQUIRED: Tuple[str, ...] = tuple(name for name, _region in quests)

# Fork option index -> baseline index (None = no direct equivalent)
FORK_GOAL_INDEX: Dict[int, int] = {
    0: 0,  # slime_diva
    1: 1,  # lord_zuulneruda
    2: 2,  # colossus
    3: 3,  # galius
    4: 6,  # all_bosses (fork: 4 bosses, we: 6)
    5: 7,  # all_quests
    6: 8,  # level_32
}


def apply_completion_condition(world) -> None:
    """Set completion rule for this player from options.goal."""
    from .AtlyssRules.catalog import build_completion_rule

    goal = int(world.options.goal)
    world.set_completion_rule(build_completion_rule(goal))
