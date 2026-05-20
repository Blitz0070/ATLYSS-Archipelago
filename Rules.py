from .AccessData import (
    AREA_STORY_QUEST,
    SHOP_MERCHANT_AREA,
    SHOP_MERCHANT_GATE,
    SHOP_MERCHANT_STORY_QUEST,
    SHOP_AP_ITEMS_PORTAL_GATE,
)
from .Locations import *
from .QuestAccess import get_area_portal_gate, get_portal_gate, get_quest_rule_map

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

# =============================================================================
# Portal access (YAML: random_portals) — used by region routes and QuestAccess.py
#
# random_portals: has_area() -> QuestAccess.AREA_TO_GATE -> has_portal_gate() (full hub chain).
# progressive: has_area() -> PORTAL_GATES via AREA_TO_GATE (Sanctum + Tuul lines).
# has_area_for_gameplay(): has_area + AccessData.AREA_STORY_QUEST (matches Regions.py).
#
# Progressive unlock order:
# Sanctum line (11): Outer, Arcwood, Catacombs 1–3, Effold, Road, Luvora, Keep, Grove 1–2
# Tuul line (3): Tuul Valley, Tuul Enclave, Bularr Fortress
# =============================================================================

def _use_random_portals(state, player) -> bool:
    return state.multiworld.worlds[player].options.random_portals


def has_named_portals(state, player, portal_items: tuple) -> bool:
    return all(state.has(portal, player, 1) for portal in portal_items)


def has_progressive_portal_lines(state, player, sanctum_count: int, tuul_count: int) -> bool:
    from .AccessData import PROGRESSIVE_SANCTUM_PORTAL_ITEM, PROGRESSIVE_TUUL_PORTAL_ITEM

    return (
        state.has(PROGRESSIVE_SANCTUM_PORTAL_ITEM, player, sanctum_count)
        and state.has(PROGRESSIVE_TUUL_PORTAL_ITEM, player, tuul_count)
    )


def has_portal_access(
    state, player, random_portal_items: tuple, progressive_sanctum: int, progressive_tuul: int,
) -> bool:
    if _use_random_portals(state, player):
        return has_named_portals(state, player, random_portal_items)
    return has_progressive_portal_lines(state, player, progressive_sanctum, progressive_tuul)


def has_portal_gate(state, player, gate_id: str) -> bool:
    """Shared portal access profile from QuestAccess.PORTAL_GATES."""
    random_items, sanctum_prog, tuul_prog = get_portal_gate(gate_id)
    return has_portal_access(state, player, random_items, sanctum_prog, tuul_prog)


def has_quest(state, player, quest) -> bool:
    return state.has(f"Complete: {quest}", player, 1)


def has_fishing_tool_for_logic(state, player) -> bool:
    return state.has("Fishing Rod", player, 1)


def has_mining_tool_for_logic(state, player) -> bool:
    return state.has("Pickaxe", player, 1)


def has_shop_access(state, player, merchant: str) -> bool:
    gate_id = SHOP_MERCHANT_GATE.get(merchant)
    if gate_id is not None:
        if not has_portal_gate(state, player, gate_id):
            return False
    else:
        area = SHOP_MERCHANT_AREA.get(merchant)
        if area is None or not has_area(state, player, area):
            return False
    story_quest = SHOP_MERCHANT_STORY_QUEST.get(merchant)
    if story_quest is not None and not has_quest(state, player, story_quest):
        return False
    return True


def has_shop_slot_portal_unlock(state, player, merchant: str, slot: int) -> bool:
    return has_portal_gate(state, player, SHOP_AP_ITEMS_PORTAL_GATE)


def has_shop_slot_progress(state, player, merchant: str, slot: int) -> bool:
    return has_shop_access(state, player, merchant) and has_shop_slot_portal_unlock(state, player, merchant, slot)


def apply_shop_slot_rules(rules: dict, player) -> None:
    for location_name, _region_name in merchants:
        prefix = "Buy Item #"
        marker = " from "
        if not location_name.startswith(prefix) or marker not in location_name:
            continue
        slot_text, merchant = location_name[len(prefix):].split(marker, 1)
        slot = int(slot_text)
        rules[location_name] = (
            lambda state, merchant=merchant, slot=slot: has_shop_slot_progress(state, player, merchant, slot)
        )


def get_rule_map(player):
    rules = get_quest_rule_map(player)
    rules.update({
        # ----- Level milestones -----
        "Reach Level 2": lambda state: can_grind_level(state, player, 2),
        "Reach Level 4": lambda state: can_grind_level(state, player, 4),
        "Reach Level 6": lambda state: can_grind_level(state, player, 6),
        "Reach Level 8": lambda state: can_grind_level(state, player, 8),
        "Reach Level 10": lambda state: can_grind_level(state, player, 10),
        "Reach Level 12": lambda state: can_grind_level(state, player, 12),
        "Reach Level 14": lambda state: can_grind_level(state, player, 14),
        "Reach Level 16": lambda state: can_grind_level(state, player, 16),
        "Reach Level 18": lambda state: can_grind_level(state, player, 18),
        "Reach Level 20": lambda state: can_grind_level(state, player, 20),
        "Reach Level 22": lambda state: can_grind_level(state, player, 22),
        "Reach Level 24": lambda state: can_grind_level(state, player, 24),
        "Reach Level 26": lambda state: can_grind_level(state, player, 26),
        "Reach Level 28": lambda state: can_grind_level(state, player, 28),
        "Reach Level 30": lambda state: can_grind_level(state, player, 30),
        "Reach Level 32": lambda state: can_grind_level(state, player, 32),
        # Shop buy rules: apply_shop_slot_rules() below (merchant access + Catacombs lvl 2 portal gate).
        "Buy Fishing Rod": lambda state: has_area(state, player, "Sanctum"),
        "Buy Pickaxe": lambda state: has_area(state, player, "Sanctum"),
        # ----- Professions -----
        "Fishing Lv. 1": lambda state: can_grind_fish(state, player, 1)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 2": lambda state: can_grind_fish(state, player, 2)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 3": lambda state: can_grind_fish(state, player, 3)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 4": lambda state: can_grind_fish(state, player, 4) and has_fishing_mid_route(state, player)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 5": lambda state: can_grind_fish(state, player, 5) and has_fishing_mid_route(state, player)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 6": lambda state: can_grind_fish(state, player, 6) and has_fishing_mid_route(state, player)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 7": lambda state: can_grind_fish(state, player, 7) and has_fishing_high_route(state, player)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 8": lambda state: can_grind_fish(state, player, 8) and has_fishing_high_route(state, player)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 9": lambda state: can_grind_fish(state, player, 9) and has_fishing_high_route(state, player)
        and has_fishing_tool_for_logic(state, player),
        "Fishing Lv. 10": lambda state: can_grind_fish(state, player, 10) and has_fishing_high_route(state, player)
        and has_fishing_tool_for_logic(state, player),
        "Mining Lv. 1": lambda state: can_grind_mine(state, player, 1)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 2": lambda state: can_grind_mine(state, player, 2) and has_mining_early_route(state, player)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 3": lambda state: can_grind_mine(state, player, 3) and has_mining_early_route(state, player)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 4": lambda state: can_grind_mine(state, player, 4) and has_mining_mid_route(state, player)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 5": lambda state: can_grind_mine(state, player, 5) and has_mining_mid_route(state, player)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 6": lambda state: can_grind_mine(state, player, 6) and has_mining_mid_route(state, player)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 7": lambda state: can_grind_mine(state, player, 7) and has_mining_high_route(state, player)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 8": lambda state: can_grind_mine(state, player, 8) and has_mining_high_route(state, player)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 9": lambda state: can_grind_mine(state, player, 9) and has_mining_high_route(state, player)
        and has_mining_tool_for_logic(state, player),
        "Mining Lv. 10": lambda state: can_grind_mine(state, player, 10) and has_mining_high_route(state, player)
        and has_mining_tool_for_logic(state, player),
        # ----- Achievements -----
        "A New Journey": lambda state: can_grind_level(state, player, 1),
        "Clearing Catacombs (1-6)": lambda state: can_grind_level(state, player, 6)
        and has_portal_gate(state, player, "sanctum_catacombs"),
        "Clearing Catacombs (6-12)": lambda state: can_grind_level(state, player, 12)
        and has_portal_gate(state, player, "sanctum_catacombs_f2"),
        "Clearing Catacombs (12-18)": lambda state: can_grind_level(state, player, 18)
        and has_portal_gate(state, player, "sanctum_catacombs_f3"),
        "Clearing Grove (15-20)": lambda state: can_grind_level(state, player, 20)
        and has_portal_gate(state, player, "crescent_grove_colossus"),
        "Clearing Grove (20-25)": lambda state: can_grind_level(state, player, 25)
        and has_portal_gate(state, player, "crescent_grove_lvl2"),
        "Judgement": lambda state: can_grind_level(state, player, 28) and has_item(state, player, "Experience Bond", 1),
        "Corrupted Arcana": lambda state: can_grind_level(state, player, 28) and has_item(state, player,
                                                                                          "Experience Bond", 1),
        "Holier than Thou": lambda state: can_grind_level(state, player, 28) and has_item(state, player,
                                                                                          "Experience Bond", 1),
        "Altered Vision": lambda state: can_grind_level(state, player, 1) and has_item(state, player, "Illusion Stone",
                                                                                       1),
        "Scaling the Tower": lambda state: can_grind_level(state, player, 1),
        "Rude!": lambda state: can_grind_level(state, player, 1),
        "Fashion Sense": lambda state: can_grind_level(state, player, 1),
        "Trout Master": lambda state: can_grind_fish(state, player, 10),
        "Skill Student": lambda state: can_grind_level(state, player, 10),
        # ----- Boss checks -----
        "Slime Diva": lambda state: can_beat_enemy(state, player, "Slime Diva"),
        "Lord Zuulneruda": lambda state: can_beat_enemy(state, player, "Lord Zuulneruda"),
        "Lord Kaluuz": lambda state: can_beat_enemy(state, player, "Lord Kaluuz"),
        "Colossus": lambda state: can_beat_enemy(state, player, "Colossus"),
        "Valdur": lambda state: can_beat_enemy(state, player, "Valdur"),
        "Galius": lambda state: can_beat_enemy(state, player, "Galius"),
    })
    apply_shop_slot_rules(rules, player)
    return rules


# =============================================================================
# Region / route helpers (area names → portal_counts or named portal items)
# =============================================================================

def has_area(state, player, area) -> bool:
    if area == "Sanctum":
        return True
    if not _use_random_portals(state, player):
        gate_id = get_area_portal_gate(area)
        if gate_id is not None:
            return has_portal_gate(state, player, gate_id)
        from .AccessData import progressive_requirements_for_portal

        sanctum, tuul = progressive_requirements_for_portal(f"{area} Portal")
        return has_progressive_portal_lines(state, player, sanctum, tuul)
    gate_id = get_area_portal_gate(area)
    if gate_id is not None:
        return has_portal_gate(state, player, gate_id)
    portal = f"{area} Portal"
    return state.has(portal, player, 1)


def has_area_for_gameplay(state, player, area: str) -> bool:
    """Portal route plus story quest gates that match Regions.py entrances."""
    if not has_area(state, player, area):
        return False
    story_quest = AREA_STORY_QUEST.get(area)
    if story_quest is None:
        return True
    return has_quest(state, player, story_quest)


def _catacombs_gate_for_enemy_areas(areas) -> str:
    if any("lvl 3" in area for area in areas):
        return "sanctum_catacombs_f3"
    if any("lvl 2" in area for area in areas):
        return "sanctum_catacombs_f2"
    return "sanctum_catacombs"


def has_all_areas(state, player, areas) -> bool:
    return all(has_area(state, player, area) for area in areas)


def has_portal_route(state, player, areas: tuple) -> bool:
    """Every area on the route must satisfy has_area (portal chain per AREA_TO_GATE)."""
    return has_all_areas(state, player, areas)


def has_fishing_mid_route(state, player) -> bool:
    return has_area_for_gameplay(state, player, "Sanctum Catacombs lvl 1")


def has_fishing_high_route(state, player) -> bool:
    return (
        has_area_for_gameplay(state, player, "Sanctum Catacombs lvl 1")
        and has_area_for_gameplay(state, player, "Crescent Road")
        and has_area_for_gameplay(state, player, "Effold Terrace")
    )


def has_mining_early_route(state, player) -> bool:
    return has_portal_gate(state, player, "arcwood_pass")


def has_mining_mid_route(state, player) -> bool:
    return has_portal_gate(state, player, "tuul_valley")


def has_mining_high_route(state, player) -> bool:
    return has_portal_gate(state, player, "tuul_enclave")


# =============================================================================
# Level grind + boss access
# =============================================================================

def can_grind(state, player, level, area_data) -> bool:
    if level > 30: return can_grind(state, player, 30, area_data)
    if level <= 1: return True

    for area in area_data:
        if not has_area_for_gameplay(state, player, area[0]): continue
        if area[1] <= level <= area[2]: return can_grind(state, player, area[1] - 1, area_data)

    return False


def can_grind_level(state, player, level) -> bool:
    return can_grind(state, player, level, location_grind_data)


def can_grind_fish(state, player, level) -> bool:
    return can_grind(state, player, level, fishing_grind_data)


def can_grind_mine(state, player, level) -> bool:
    return can_grind(state, player, level, mining_grind_data)


def can_beat_enemy(state, player, enemy_name) -> bool:
    level, areas = enemy_data[enemy_name]
    if not can_grind_level(state, player, level):
        return False
    if not areas:
        return True
    if all(a.startswith("Sanctum Catacombs") for a in areas):
        gate = _catacombs_gate_for_enemy_areas(areas)
        if not has_portal_gate(state, player, gate):
            return False
        return has_quest(state, player, "Communing Catacombs")
    return any(has_area_for_gameplay(state, player, area) for area in areas)


def has_item(state, player, item, count) -> bool:
    return state.has(item, player, count)