"""
Victory conditions and goal index contract (Phase D).

Indices MUST match Options.Goal, fill_slot_data['goal'], and the mod
(AtlyssArchipelagoPlugin goalOption / goal chat lines). Do not reorder
without updating ArchipelagoGameDataTables and Connection.cs.

Fork Improved-Logic uses 7 goals (no Lord Kaluuz / Valdur singles); see FORK_GOAL_INDEX.
"""
from __future__ import annotations

from typing import Callable, Dict, List, Tuple

from .GoalScope import GOAL_TARGET_BOSS
from .Locations import quests
from .Rules import can_beat_enemy, can_grind_level, has_quest

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


def _all_quests_complete(state, player: int) -> bool:
    return all(has_quest(state, player, name) for name in ALL_QUESTS_REQUIRED)


def _all_bosses_complete(state, player: int) -> bool:
    return all(can_beat_enemy(state, player, name) for name in ALL_BOSSES_REQUIRED)


def apply_completion_condition(world) -> None:
    """Set multiworld.completion_condition for this player from options.goal."""
    player = world.player
    goal = int(world.options.goal)

    conditions: Dict[int, Callable] = {
        0: lambda state, p=player: can_beat_enemy(state, p, GOAL_TARGET_BOSS[0]),
        1: lambda state, p=player: can_beat_enemy(state, p, GOAL_TARGET_BOSS[1]),
        2: lambda state, p=player: can_beat_enemy(state, p, GOAL_TARGET_BOSS[2]),
        3: lambda state, p=player: can_beat_enemy(state, p, GOAL_TARGET_BOSS[3]),
        4: lambda state, p=player: can_beat_enemy(state, p, GOAL_TARGET_BOSS[4]),
        5: lambda state, p=player: can_beat_enemy(state, p, GOAL_TARGET_BOSS[5]),
        6: lambda state, p=player: _all_bosses_complete(state, p),
        7: lambda state, p=player: _all_quests_complete(state, p),
        8: lambda state, p=player: can_grind_level(state, p, 32),
    }

    if goal not in conditions:
        raise ValueError(f"Unknown goal option {goal} for player {player}")
    world.multiworld.completion_condition[player] = conditions[goal]
