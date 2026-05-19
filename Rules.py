from .Locations import *
from .QuestAccess import get_portal_gate, get_quest_rule_map

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

# =============================================================================
# Portal access (YAML: random_portals) — used by region routes and QuestAccess.py
#
# Progressive unlock order:
#   1 Outer  2 Arcwood  3–5 Catacombs lvl 1–3  6 Effold  7 Tuul  8 Road
#   9 Luvora  10 Keep  11 Enclave  12 Grove lvl 1  13 Grove lvl 2  14 Bularr
# =============================================================================

def _use_random_portals(state, player) -> bool:
    return state.multiworld.worlds[player].options.random_portals


def has_named_portals(state, player, portal_items: tuple) -> bool:
    return all(state.has(portal, player, 1) for portal in portal_items)


def has_progressive_portals(state, player, unlock_count: int) -> bool:
    return state.has("Progressive Portal", player, unlock_count)


def has_portal_access(state, player, random_portal_items: tuple, progressive_unlock_count: int) -> bool:
    if _use_random_portals(state, player):
        return has_named_portals(state, player, random_portal_items)
    return has_progressive_portals(state, player, progressive_unlock_count)


def has_portal_gate(state, player, gate_id: str) -> bool:
    """Shared portal access profile from QuestAccess.PORTAL_GATES."""
    random_items, progressive = get_portal_gate(gate_id)
    return has_portal_access(state, player, random_items, progressive)


def has_fishing_tool_for_logic(state, player) -> bool:
    return state.has("Fishing Rod", player, 1)


def has_mining_tool_for_logic(state, player) -> bool:
    return state.has("Pickaxe", player, 1)


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
        # ----- Shops -----
        "Buy Item #1 from Sally's Nook": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #2 from Sally's Nook": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #3 from Sally's Nook": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #4 from Sally's Nook": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #5 from Sally's Nook": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #1 from Skrit's Sikrit Market": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #2 from Skrit's Sikrit Market": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #3 from Skrit's Sikrit Market": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #4 from Skrit's Sikrit Market": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #5 from Skrit's Sikrit Market": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #1 from Frankie's Goods": lambda state: has_portal_gate(state, player, "arcwood_pass"),
        "Buy Item #2 from Frankie's Goods": lambda state: has_portal_gate(state, player, "arcwood_pass"),
        "Buy Item #3 from Frankie's Goods": lambda state: has_portal_gate(state, player, "arcwood_pass"),
        "Buy Item #4 from Frankie's Goods": lambda state: has_portal_gate(state, player, "arcwood_pass"),
        "Buy Item #5 from Frankie's Goods": lambda state: has_portal_gate(state, player, "arcwood_pass"),
        "Buy Item #1 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #2 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #3 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #4 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #5 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #1 from Tesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f2"),
        "Buy Item #2 from Tesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f2"),
        "Buy Item #3 from Tesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f2"),
        "Buy Item #4 from Tesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f2"),
        "Buy Item #5 from Tesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f2"),
        "Buy Item #1 from Nesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f3"),
        "Buy Item #2 from Nesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f3"),
        "Buy Item #3 from Nesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f3"),
        "Buy Item #4 from Nesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f3"),
        "Buy Item #5 from Nesh's Wares": lambda state: has_portal_gate(state, player, "sanctum_catacombs_f3"),
        "Buy Item #1 from Rikko's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_colossus"),
        "Buy Item #2 from Rikko's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_colossus"),
        "Buy Item #3 from Rikko's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_colossus"),
        "Buy Item #4 from Rikko's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_colossus"),
        "Buy Item #5 from Rikko's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_colossus"),
        "Buy Item #1 from Cotoo's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_lvl2"),
        "Buy Item #2 from Cotoo's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_lvl2"),
        "Buy Item #3 from Cotoo's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_lvl2"),
        "Buy Item #4 from Cotoo's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_lvl2"),
        "Buy Item #5 from Cotoo's Treasures": lambda state: has_portal_gate(state, player, "crescent_grove_lvl2"),
        "Buy Item #1 from Ruka's Furnace": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #2 from Ruka's Furnace": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #3 from Ruka's Furnace": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #4 from Ruka's Furnace": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #5 from Ruka's Furnace": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #1 from Torta's Fishing Shack": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #2 from Torta's Fishing Shack": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #3 from Torta's Fishing Shack": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #4 from Torta's Fishing Shack": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #5 from Torta's Fishing Shack": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #1 from Mad Statue's Gift": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #2 from Mad Statue's Gift": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #3 from Mad Statue's Gift": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #4 from Mad Statue's Gift": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #5 from Mad Statue's Gift": lambda state: has_area(state, player, "Sanctum"),
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
        "A New Journey": lambda state: can_grind_level(state, player, 0),
        "Clearing Catacombs (1-6)": lambda state: can_grind_level(state, player, 1)
        and has_portal_gate(state, player, "sanctum_catacombs"),
        "Clearing Catacombs (6-12)": lambda state: can_grind_level(state, player, 6)
        and has_portal_gate(state, player, "sanctum_catacombs_f2"),
        "Clearing Catacombs (12-18)": lambda state: can_grind_level(state, player, 12)
        and has_portal_gate(state, player, "sanctum_catacombs_f3"),
        "Clearing Grove (15-20)": lambda state: can_grind_level(state, player, 15)
        and has_portal_gate(state, player, "crescent_grove_colossus"),
        "Clearing Grove (20-25)": lambda state: can_grind_level(state, player, 20)
        and has_portal_gate(state, player, "crescent_grove_lvl2"),
        "Judgement": lambda state: can_grind_level(state, player, 28) and has_item(state, player, "Experience Bond", 1),
        "Corrupted Arcana": lambda state: can_grind_level(state, player, 28) and has_item(state, player,
                                                                                          "Experience Bond", 1),
        "Holier than Thou": lambda state: can_grind_level(state, player, 28) and has_item(state, player,
                                                                                          "Experience Bond", 1),
        "Altered Vision": lambda state: can_grind_level(state, player, 0) and has_item(state, player, "Illusion Stone",
                                                                                       1),
        "Scaling the Tower": lambda state: can_grind_level(state, player, 0),
        "Rude!": lambda state: can_grind_level(state, player, 0),
        "Fashion Sense": lambda state: can_grind_level(state, player, 0),
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
    return rules


# =============================================================================
# Region / route helpers (area names → portal_counts or named portal items)
# =============================================================================

def has_area(state, player, area) -> bool:
    if area == "Sanctum":
        return True
    if not state.multiworld.worlds[player].options.random_portals:
        return state.has("Progressive Portal", player, portal_counts[area])
    if area == "Cresent Grove lvl 2":
        return (
            state.has("Cresent Grove lvl 1 Portal", player, 1)
            and state.has("Cresent Grove lvl 2 Portal", player, 1)
        )
    portal = f"{area} Portal"
    return state.has(portal, player, 1)


# Fork shop/profession portal matrix (Improved-Logic rules.py SHOP + PROFESSION blocks).
_FISHING_MID_ROUTE = ("Outer Sanctum", "Arcwood Pass", "Sanctum Catacombs lvl 1")
_FISHING_HIGH_ROUTE = (
    "Cresent Road", "Effold Terrace", "Outer Sanctum", "Arcwood Pass", "Sanctum Catacombs lvl 1"
)
_MINING_EARLY_ROUTE = ("Outer Sanctum", "Arcwood Pass")
_MINING_MID_ROUTE = ("Tuul Valley", "Outer Sanctum")
_MINING_HIGH_ROUTE = ("Tuul Valley", "Outer Sanctum", "Tuul Enclave")


def has_all_areas(state, player, areas) -> bool:
    return all(has_area(state, player, area) for area in areas)


def has_portal_route(state, player, areas: tuple) -> bool:
    """All regions on route: per-area portal_counts in progressive mode, all named portals in random mode."""
    if not state.multiworld.worlds[player].options.random_portals:
        return all(has_area(state, player, area) for area in areas)
    return has_all_areas(state, player, areas)


def has_fishing_mid_route(state, player) -> bool:
    return has_portal_route(state, player, _FISHING_MID_ROUTE)


def has_fishing_high_route(state, player) -> bool:
    return has_portal_route(state, player, _FISHING_HIGH_ROUTE)


def has_mining_early_route(state, player) -> bool:
    return has_portal_route(state, player, _MINING_EARLY_ROUTE)


def has_mining_mid_route(state, player) -> bool:
    return has_portal_route(state, player, _MINING_MID_ROUTE)


def has_mining_high_route(state, player) -> bool:
    return has_portal_route(state, player, _MINING_HIGH_ROUTE)


def has_quest(state, player, quest) -> bool:
    return state.has(f"Complete: {quest}", player, 1)


# =============================================================================
# Level grind + boss access
# =============================================================================

def can_grind(state, player, level, area_data) -> bool:
    if level > 30: return can_grind(state, player, 30, area_data)
    if level <= 1: return True

    for area in area_data:
        if not has_area(state, player, area[0]): continue
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
        route = ("Outer Sanctum", "Arcwood Pass") + tuple(areas)
        return has_portal_route(state, player, route)
    if areas == ["Effold Terrace"]:
        return has_portal_gate(state, player, "effold_terrace")
    if areas == ["Cresent Grove lvl 1"]:
        return has_portal_gate(state, player, "crescent_grove_colossus")
    if areas == ["Cresent Grove lvl 2"]:
        return has_portal_gate(state, player, "crescent_grove_lvl2")
    if areas == ["Bularr Fortress"]:
        return has_portal_gate(state, player, "bularr_fortress")
    return has_portal_route(state, player, tuple(areas))


def has_item(state, player, item, count) -> bool:
    return state.has(item, player, count)