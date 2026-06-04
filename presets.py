from typing import Any, Dict

# Keys match AtlyssOptions field names (YAML under `Atlyss:`).

_all_random: Dict[str, Any] = {
    "progression_balancing": "random",
    "accessibility": "random",
    "death_link": "random",
    "goal": "random",
    "random_portals": "random",
    "shop_sanity": "random",
    "achievements": "random",
    "equipment_progression": "random",
    "profession_tools": "random",
    "class_filter": "random",
    "experience_multiplier": "random",
    "crown_multiplier": "random",
}

_default: Dict[str, Any] = {
    "goal": "slime_diva",
    "random_portals": "false",
    "shop_sanity": "true",
    "achievements": "true",
    "equipment_progression": "unrestricted",
    "profession_tools": "static",
    "class_filter": "all_classes",
    "experience_multiplier": "x1_0",
    "crown_multiplier": "x1_0",
}

_short_run: Dict[str, Any] = {
    "goal": "slime_diva",
    "random_portals": "false",
    "shop_sanity": "true",
    "achievements": "false",
    "equipment_progression": "gated",
    "profession_tools": "static",
    "class_filter": "all_classes",
    "experience_multiplier": "x2_0",
    "crown_multiplier": "x1_0",
}

_boss_hunter: Dict[str, Any] = {
    "goal": "all_bosses",
    "random_portals": "false",
    "shop_sanity": "true",
    "achievements": "false",
    "equipment_progression": "unrestricted",
    "profession_tools": "static",
    "class_filter": "all_classes",
    "experience_multiplier": "x1_0",
    "crown_multiplier": "x1_0",
}

_full_adventure: Dict[str, Any] = {
    "goal": "all_quests",
    "random_portals": "false",
    "shop_sanity": "true",
    "achievements": "true",
    "equipment_progression": "gated",
    "profession_tools": "pool",
    "class_filter": "all_classes",
    "experience_multiplier": "x1_0",
    "crown_multiplier": "x0_75",
}

_random_portals: Dict[str, Any] = {
    "goal": "galius",
    "random_portals": "true",
    "shop_sanity": "true",
    "achievements": "true",
    "equipment_progression": "gated",
    "profession_tools": "static",
    "class_filter": "all_classes",
    "experience_multiplier": "x1_0",
    "crown_multiplier": "x1_0",
}

atlyss_options_presets: Dict[str, Dict[str, Any]] = {
    "All Random": _all_random,
    "Default": _default,
    "Short Run": _short_run,
    "Boss Hunter": _boss_hunter,
    "Full Adventure": _full_adventure,
    "Random Portals": _random_portals,
}
