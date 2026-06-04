from typing import Any, Dict

from .Options import (
    Achievements,
    ClassFilter,
    CrownMultiplier,
    EquipmentProgression,
    ExperienceMultiplier,
    Goal,
    ProfessionTools,
    RandomPortals,
    ShopSanity,
)

_all_random: Dict[str, Any] = {
    "progression_balancing": "random",
    "accessibility": "random",
    "death_link": "random",
    Goal.internal_name: "random",
    RandomPortals.internal_name: "random",
    ShopSanity.internal_name: "random",
    Achievements.internal_name: "random",
    EquipmentProgression.internal_name: "random",
    ProfessionTools.internal_name: "random",
    ClassFilter.internal_name: "random",
    ExperienceMultiplier.internal_name: "random",
    CrownMultiplier.internal_name: "random",
}

_default: Dict[str, Any] = {
    Goal.internal_name: "slime_diva",
    RandomPortals.internal_name: "false",
    ShopSanity.internal_name: "true",
    Achievements.internal_name: "true",
    EquipmentProgression.internal_name: "unrestricted",
    ProfessionTools.internal_name: "static",
    ClassFilter.internal_name: "all_classes",
    ExperienceMultiplier.internal_name: "x1_0",
    CrownMultiplier.internal_name: "x1_0",
}

_short_run: Dict[str, Any] = {
    Goal.internal_name: "slime_diva",
    RandomPortals.internal_name: "false",
    ShopSanity.internal_name: "true",
    Achievements.internal_name: "false",
    EquipmentProgression.internal_name: "gated",
    ProfessionTools.internal_name: "static",
    ClassFilter.internal_name: "all_classes",
    ExperienceMultiplier.internal_name: "x2_0",
    CrownMultiplier.internal_name: "x1_0",
}

_boss_hunter: Dict[str, Any] = {
    Goal.internal_name: "all_bosses",
    RandomPortals.internal_name: "false",
    ShopSanity.internal_name: "true",
    Achievements.internal_name: "false",
    EquipmentProgression.internal_name: "unrestricted",
    ProfessionTools.internal_name: "static",
    ClassFilter.internal_name: "all_classes",
    ExperienceMultiplier.internal_name: "x1_0",
    CrownMultiplier.internal_name: "x1_0",
}

_full_adventure: Dict[str, Any] = {
    Goal.internal_name: "all_quests",
    RandomPortals.internal_name: "false",
    ShopSanity.internal_name: "true",
    Achievements.internal_name: "true",
    EquipmentProgression.internal_name: "gated",
    ProfessionTools.internal_name: "pool",
    ClassFilter.internal_name: "all_classes",
    ExperienceMultiplier.internal_name: "x1_0",
    CrownMultiplier.internal_name: "x0_75",
}

_random_portals: Dict[str, Any] = {
    Goal.internal_name: "galius",
    RandomPortals.internal_name: "true",
    ShopSanity.internal_name: "true",
    Achievements.internal_name: "true",
    EquipmentProgression.internal_name: "gated",
    ProfessionTools.internal_name: "static",
    ClassFilter.internal_name: "all_classes",
    ExperienceMultiplier.internal_name: "x1_0",
    CrownMultiplier.internal_name: "x1_0",
}

atlyss_options_presets: Dict[str, Dict[str, Any]] = {
    "All Random": _all_random,
    "Default": _default,
    "Short Run": _short_run,
    "Boss Hunter": _boss_hunter,
    "Full Adventure": _full_adventure,
    "Random Portals": _random_portals,
}
