from .AccessData import (
    AREA_STORY_QUEST,
    SHOP_MERCHANT_AREA,
    SHOP_MERCHANT_GATE,
    SHOP_MERCHANT_STORY_QUEST,
    SHOP_AP_ITEMS_PORTAL_GATE,
)
from .Locations import *
from .QuestAccess import get_area_portal_gate, get_portal_gate

# Parity helpers for portal/grind/boss checks. Access rules live in AtlyssRules/ (Rule Builder);
# custom Rule._evaluate and test_portal_compose.py call into this module.

# =============================================================================
# Portal access (YAML: random_portals) — mirrors portal_compose / QuestAccess gates
#
# random_portals: has_area() -> QuestAccess.AREA_TO_GATE -> has_portal_gate() (full hub chain).
# progressive: has_area() -> PORTAL_GATES via AREA_TO_GATE (Sanctum + Tuul lines).
# has_area_for_gameplay(): has_area + AccessData.AREA_STORY_QUEST (deeper zones only; entrances are portal-only).
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


def _catacombs_floor_depth(area: str) -> int:
    if "lvl 3" in area:
        return 3
    if "lvl 2" in area:
        return 2
    return 1


def _catacombs_gate_for_enemy_areas(areas) -> str:
    """Shallowest listed floor — multi-floor spawns are OR routes (e.g. Toxin on f2 or f3)."""
    depth = min(_catacombs_floor_depth(area) for area in areas)
    if depth >= 3:
        return "sanctum_catacombs_f3"
    if depth >= 2:
        return "sanctum_catacombs_f2"
    return "sanctum_catacombs"


def _catacombs_story_access_ok(state, player, areas) -> bool:
    if any(has_area_for_gameplay(state, player, area) for area in areas):
        return True
    gate = _catacombs_gate_for_enemy_areas(areas)
    if not has_portal_gate(state, player, gate):
        return False
    # Lvl 1 has no AREA_STORY_QUEST — min-depth portal is enough (Killing Tomb geists).
    if gate == "sanctum_catacombs":
        return True
    # Match portal_gates quest bands: f2 after Killing Tomb, f3 after Voice (Rattlecage / Consumed Madness).
    if gate == "sanctum_catacombs_f3":
        return has_quest(state, player, "The Voice of Zuulneruda")
    if gate == "sanctum_catacombs_f2":
        return has_quest(state, player, "Killing Tomb")
    return False


def has_all_areas(state, player, areas) -> bool:
    return all(has_area(state, player, area) for area in areas)


def has_portal_route(state, player, areas: tuple) -> bool:
    """Every area on the route must satisfy has_area (portal chain per AREA_TO_GATE)."""
    return has_all_areas(state, player, areas)


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
    """Fishing profession level via spot train bands (FishingData.FISHING_TRAIN_BANDS)."""
    from .AtlyssRules.profession_grind_compose import evaluate_fishing_grind

    return evaluate_fishing_grind(state, player, level)


def can_grind_mine(state, player, level) -> bool:
    """Mining profession level via node train bands (MiningData.MINING_TRAIN_BANDS)."""
    from .AtlyssRules.profession_grind_compose import evaluate_mining_grind

    return evaluate_mining_grind(state, player, level)


def can_beat_enemy(state, player, enemy_name) -> bool:
    level, areas = enemy_data[enemy_name]
    if not areas:
        return True
    if all(a.startswith("Sanctum Catacombs") for a in areas):
        gate = _catacombs_gate_for_enemy_areas(areas)
        if not has_portal_gate(state, player, gate):
            return False
        return _catacombs_story_access_ok(state, player, areas)
    return any(has_area_for_gameplay(state, player, area) for area in areas)


def has_item(state, player, item, count) -> bool:
    return state.has(item, player, count)