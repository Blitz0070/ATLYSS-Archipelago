"""Build location and completion rules from Atlyss tables."""
from __future__ import annotations

from rule_builder.rules import And, Rule, True_

from worlds.atlyss.GoalCompletion import (
    ALL_BOSSES_REQUIRED,
    ALL_QUESTS_REQUIRED,
    GOAL_TARGET_BOSS,
)
from worlds.atlyss.Locations import merchants
from worlds.atlyss.QuestAccess import (
    FISHING_ROD_REQUIRED_QUESTS,
    PICKAXE_REQUIRED_QUESTS,
    QUEST_ACCESS,
)

from .custom_rules import (
    CanAccessAreaGameplay,
    CanBeatBoss,
    CanGrindFishing,
    CanGrindLevel,
    CanGrindMining,
    HasPortalGate,
    HasProgressionItem,
    HasQuestComplete,
    QuestCheck,
    RequiresFishingRod,
    RequiresPickaxe,
    ShopSlotCheck,
)

_LEVEL_MILESTONES = tuple(range(2, 33, 2))


def _compose_quest_rule(quest_name: str) -> Rule:
    rule: Rule = QuestCheck(quest_name)
    if quest_name in PICKAXE_REQUIRED_QUESTS:
        rule = rule & RequiresPickaxe()
    if quest_name in FISHING_ROD_REQUIRED_QUESTS:
        rule = rule & RequiresFishingRod()
    return rule


def _shop_slot_rule(location_name: str) -> Rule | None:
    prefix = "Buy Item #"
    marker = " from "
    if not location_name.startswith(prefix) or marker not in location_name:
        return None
    slot_text, merchant = location_name[len(prefix):].split(marker, 1)
    return ShopSlotCheck(merchant, int(slot_text))


def _build_static_location_rules() -> dict[str, Rule]:
    rules: dict[str, Rule] = {
        quest_name: _compose_quest_rule(quest_name)
        for quest_name in QUEST_ACCESS
    }

    for level in _LEVEL_MILESTONES:
        rules[f"Reach Level {level}"] = CanGrindLevel(level)

    rules["Buy Fishing Rod"] = CanAccessAreaGameplay("Sanctum")
    rules["Buy Pickaxe"] = CanAccessAreaGameplay("Sanctum")

    for level in range(1, 11):
        rules[f"Fishing Lv. {level}"] = CanGrindFishing(level)
    for level in range(1, 11):
        rules[f"Mining Lv. {level}"] = CanGrindMining(level)

    rules.update({
        "A New Journey": True_(),
        "Clearing Catacombs (1-6)": HasPortalGate("sanctum_catacombs"),
        "Clearing Catacombs (6-12)": HasPortalGate("sanctum_catacombs_f2"),
        "Clearing Catacombs (12-18)": HasPortalGate("sanctum_catacombs_f3"),
        "Clearing Grove (15-20)": HasPortalGate("crescent_grove_colossus"),
        "Clearing Grove (20-25)": HasPortalGate("crescent_grove_lvl2"),
        "Altered Vision": HasProgressionItem("Illusion Stone"),
        "Scaling the Tower": True_(),
        "Rude!": True_(),
        "Fashion Sense": True_(),
        "Trout Master": CanGrindFishing(10),
        "Skill Student": True_(),
        "Slime Diva": CanBeatBoss("Slime Diva"),
        "Lord Zuulneruda": CanBeatBoss("Lord Zuulneruda"),
        "Lord Kaluuz": CanBeatBoss("Lord Kaluuz"),
        "Colossus": CanBeatBoss("Colossus"),
        "Valdur": CanBeatBoss("Valdur"),
        "Galius": CanBeatBoss("Galius"),
    })

    for location_name, _region_name in merchants:
        shop_rule = _shop_slot_rule(location_name)
        if shop_rule is not None:
            rules[location_name] = shop_rule

    return rules


_LOCATION_RULES: dict[str, Rule] = _build_static_location_rules()


def build_location_rule(location_name: str) -> Rule | None:
    """Return the access rule for a location, or None if unrestricted."""
    return _LOCATION_RULES.get(location_name)


def build_completion_rule(goal: int) -> Rule:
    if goal in (0, 1, 2, 3, 4, 5):
        return CanBeatBoss(GOAL_TARGET_BOSS[goal])
    if goal == 6:
        return And(*(CanBeatBoss(name) for name in ALL_BOSSES_REQUIRED))
    if goal == 7:
        return And(*(HasQuestComplete(name) for name in ALL_QUESTS_REQUIRED))
    if goal == 8:
        return CanGrindLevel(32)
    raise ValueError(f"Unknown goal option {goal}")
