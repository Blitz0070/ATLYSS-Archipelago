"""Compose portal and shop access from Rule Builder builtins."""
from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import And, Has, HasAll, Rule, True_

if TYPE_CHECKING:
    from worlds.atlyss import Atlyss


def caching_enabled(world: "Atlyss") -> bool:
    return getattr(world, "rule_caching_enabled", False)


def portal_gate_item_names(gate_id: str) -> tuple[str, ...]:
    from worlds.atlyss.AccessData import (
        PROGRESSIVE_SANCTUM_PORTAL_ITEM,
        PROGRESSIVE_TUUL_PORTAL_ITEM,
    )
    from worlds.atlyss.QuestAccess import get_portal_gate

    random_items, sanctum_prog, tuul_prog = get_portal_gate(gate_id)
    names: list[str] = list(random_items)
    if sanctum_prog:
        names.append(PROGRESSIVE_SANCTUM_PORTAL_ITEM)
    if tuul_prog:
        names.append(PROGRESSIVE_TUUL_PORTAL_ITEM)
    return tuple(names)


def build_portal_gate_rule(world: "Atlyss", gate_id: str) -> Rule:
    """Portal gate as HasAll (random) or progressive Has counts — matches Rules.has_portal_gate."""
    from worlds.atlyss.AccessData import (
        PROGRESSIVE_SANCTUM_PORTAL_ITEM,
        PROGRESSIVE_TUUL_PORTAL_ITEM,
    )
    from worlds.atlyss.QuestAccess import get_portal_gate

    random_items, sanctum_count, tuul_count = get_portal_gate(gate_id)
    if world.options.random_portals:
        return HasAll(*random_items)
    parts: list[Rule] = []
    if sanctum_count > 0:
        parts.append(Has(PROGRESSIVE_SANCTUM_PORTAL_ITEM, sanctum_count))
    if tuul_count > 0:
        parts.append(Has(PROGRESSIVE_TUUL_PORTAL_ITEM, tuul_count))
    if not parts:
        return True_()
    combined = parts[0]
    for part in parts[1:]:
        combined = combined & part
    return combined


def portal_gate_explain_label(world: "Atlyss", gate_id: str) -> str:
    from worlds.atlyss.AccessData import (
        PROGRESSIVE_SANCTUM_PORTAL_ITEM,
        PROGRESSIVE_TUUL_PORTAL_ITEM,
    )
    from worlds.atlyss.QuestAccess import get_portal_gate

    random_items, sanctum_count, tuul_count = get_portal_gate(gate_id)
    if world.options.random_portals:
        return ", ".join(random_items)
    parts: list[str] = []
    if sanctum_count > 0:
        parts.append(f"{PROGRESSIVE_SANCTUM_PORTAL_ITEM} x{sanctum_count}")
    if tuul_count > 0:
        parts.append(f"{PROGRESSIVE_TUUL_PORTAL_ITEM} x{tuul_count}")
    return " and ".join(parts) if parts else "no portal requirement"


def build_has_area_rule(world: "Atlyss", area_name: str) -> Rule:
    """Portal route only — matches Rules.has_area (no AREA_STORY_QUEST)."""
    from worlds.atlyss.AccessData import progressive_requirements_for_portal
    from worlds.atlyss.QuestAccess import get_area_portal_gate

    if area_name == "Sanctum":
        return True_()
    gate_id = get_area_portal_gate(area_name)
    if gate_id is not None:
        return build_portal_gate_rule(world, gate_id)
    if world.options.random_portals:
        return Has(f"{area_name} Portal")
    sanctum, tuul = progressive_requirements_for_portal(f"{area_name} Portal")
    parts: list[Rule] = []
    from worlds.atlyss.AccessData import (
        PROGRESSIVE_SANCTUM_PORTAL_ITEM,
        PROGRESSIVE_TUUL_PORTAL_ITEM,
    )

    if sanctum > 0:
        parts.append(Has(PROGRESSIVE_SANCTUM_PORTAL_ITEM, sanctum))
    if tuul > 0:
        parts.append(Has(PROGRESSIVE_TUUL_PORTAL_ITEM, tuul))
    if not parts:
        return True_()
    combined = parts[0]
    for part in parts[1:]:
        combined = combined & part
    return combined


def build_shop_merchant_access_rule(world: "Atlyss", merchant: str) -> Rule:
    """Merchant area/gate + optional story quest — matches Rules.has_shop_access (no AP slot gate)."""
    from worlds.atlyss.AccessData import SHOP_MERCHANT_AREA, SHOP_MERCHANT_GATE, SHOP_MERCHANT_STORY_QUEST

    parts: list[Rule] = []
    gate_id = SHOP_MERCHANT_GATE.get(merchant)
    if gate_id is not None:
        parts.append(build_portal_gate_rule(world, gate_id))
    else:
        area = SHOP_MERCHANT_AREA.get(merchant)
        if area is not None and not has_area_always_open(area):
            parts.append(build_has_area_rule(world, area))
    story_quest = SHOP_MERCHANT_STORY_QUEST.get(merchant)
    if story_quest is not None:
        parts.append(Has(f"Complete: {story_quest}"))
    if not parts:
        return True_()
    combined = parts[0]
    for part in parts[1:]:
        combined = combined & part
    return combined


def has_area_always_open(area_name: str) -> bool:
    return area_name == "Sanctum"


def build_shop_slot_rule(world: "Atlyss", merchant: str, slot: int) -> Rule:
    """Matches Rules.has_shop_slot_progress (slot unused until per-slot gates exist)."""
    from worlds.atlyss.AccessData import SHOP_AP_ITEMS_PORTAL_GATE

    _ = slot
    return (
        build_portal_gate_rule(world, SHOP_AP_ITEMS_PORTAL_GATE)
        & build_shop_merchant_access_rule(world, merchant)
    )


def build_area_gameplay_rule(world: "Atlyss", area_name: str) -> Rule:
    """Portal route + AREA_STORY_QUEST — matches Rules.has_area_for_gameplay."""
    from worlds.atlyss.AccessData import AREA_STORY_QUEST

    base = build_has_area_rule(world, area_name)
    story_quest = AREA_STORY_QUEST.get(area_name)
    if story_quest is not None:
        base = base & Has(f"Complete: {story_quest}")
    return base


def build_fishing_route_rule(world: "Atlyss", level: int) -> Rule:
    if level >= 7:
        return (
            build_area_gameplay_rule(world, "Sanctum Catacombs lvl 1")
            & build_area_gameplay_rule(world, "Crescent Road")
            & build_area_gameplay_rule(world, "Effold Terrace")
        )
    if level >= 4:
        return build_area_gameplay_rule(world, "Sanctum Catacombs lvl 1")
    return True_()


def build_mining_route_rule(world: "Atlyss", level: int) -> Rule:
    if level >= 7:
        return build_portal_gate_rule(world, "tuul_enclave")
    if level >= 4:
        return build_portal_gate_rule(world, "tuul_valley")
    if level >= 2:
        return (
            build_portal_gate_rule(world, "arcwood_pass")
            | build_portal_gate_rule(world, "effold_terrace")
        )
    return True_()
