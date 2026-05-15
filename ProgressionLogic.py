"""
Equipment tier helpers and fill constraints (Phase A of fork port plan).
"""
from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from BaseClasses import Item, ItemClassification
from worlds.generic.Rules import add_item_rule

from .GoalScope import _get_location_min_grind_levels
from .ItemTiers import get_item_tier
from .Locations import location_grind_data


def level_to_max_tier(level: int) -> int:
    if level <= 5:
        return 1
    if level <= 10:
        return 2
    if level <= 15:
        return 3
    if level <= 20:
        return 4
    return 5


REGION_MAX_TIER: dict[str, int] = {
    area_name: level_to_max_tier(max_level)
    for area_name, _min_level, max_level in location_grind_data
}

_SHOP_MERCHANT_MIN_LEVEL: dict[str, int] = {
    "Sally's Nook": 1,
    "Skrit's Sikrit Market": 1,
    "Frankie's Goods": 1,
    "Dye Merchant": 1,
    "Ruka's Furnace": 1,
    "Torta's Fishing Shack": 1,
    "Mad Statue's Gift": 1,
    "Tesh's Wares": 6,
    "Nesh's Wares": 12,
    "Rikko's Treasures": 15,
    "Cotoo's Treasures": 20,
}

_HIGH_LEVEL_JUNK_MILESTONES = frozenset({"Reach Level 28", "Reach Level 30", "Reach Level 32"})


def is_junk_only_location(location_name: str) -> bool:
    return (
        location_name.startswith("Fishing Lv.")
        or location_name.startswith("Mining Lv.")
        or location_name in _HIGH_LEVEL_JUNK_MILESTONES
    )


def get_menu_location_effective_level(location_name: str) -> int:
    if location_name.startswith("Reach Level "):
        return int(location_name.split()[-1])

    if location_name.startswith("Fishing Lv."):
        fl = int(location_name.rsplit(" ", 1)[-1])
        if fl <= 3:
            return 1
        if fl <= 6:
            return 4
        return 8

    if location_name.startswith("Mining Lv."):
        ml = int(location_name.rsplit(" ", 1)[-1])
        if ml <= 3:
            return 1
        if ml <= 6:
            return 8
        return 12

    if location_name.startswith("Buy Item #") and " from " in location_name:
        merchant = location_name.split(" from ", 1)[1]
        if merchant in _SHOP_MERCHANT_MIN_LEVEL:
            return _SHOP_MERCHANT_MIN_LEVEL[merchant]
        for key, level in _SHOP_MERCHANT_MIN_LEVEL.items():
            if key in merchant:
                return level

    parsed = _get_location_min_grind_levels().get(location_name)
    if parsed is not None:
        return parsed

    return 1


def get_location_max_tier(location_name: str, region_name: str) -> int:
    if region_name == "Menu":
        return level_to_max_tier(get_menu_location_effective_level(location_name))
    return REGION_MAX_TIER.get(region_name, 1)


def compute_tier_budgets(world) -> Dict[int, int]:
    """Cumulative location budgets per tier (gated pool must not exceed these)."""
    tier_location_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    player = world.player

    for region in world.multiworld.regions:
        if region.player != player:
            continue
        for location in region.locations:
            if location.item is not None or is_junk_only_location(location.name):
                continue
            max_tier = get_location_max_tier(location.name, region.name)
            tier_location_counts[max_tier] += 1

    cumulative: Dict[int, int] = {}
    running = 0
    for tier in range(5, 0, -1):
        running += tier_location_counts[tier]
        cumulative[tier] = running
    return cumulative


def count_junk_locations(world) -> int:
    count = 0
    player = world.player
    for region in world.multiworld.regions:
        if region.player != player:
            continue
        for location in region.locations:
            if is_junk_only_location(location.name):
                count += 1
    return count


def tier_selection_would_overflow(tier: int, tier_counts: Dict[int, int], tier_budgets: Dict[int, int]) -> bool:
    for check_tier in range(1, tier + 1):
        cumul = sum(tier_counts[t] for t in range(check_tier, 6))
        if cumul + 1 > tier_budgets[check_tier]:
            return True
    return False


def set_profession_junk_rules(world) -> None:
    player = world.player
    for region in world.multiworld.regions:
        if region.player != player:
            continue
        for location in region.locations:
            if not is_junk_only_location(location.name):
                continue
            add_item_rule(
                location,
                lambda item, p=player: (
                    item.player != p or item.classification == ItemClassification.filler
                ),
            )


# Filler-class items required on non-junk checks (logic uses has_item).
GATED_NON_JUNK_FILLER_LOCATIONS = frozenset({"Altered Vision"})


def set_gated_filler_reserved_for_junk_rules(world) -> None:
    """Gated: filler may only fill fishing/mining checks, not shops or quests."""
    if world.options.equipment_progression.value != 0:
        return
    player = world.player
    for region in world.multiworld.regions:
        if region.player != player:
            continue
        for location in region.locations:
            if is_junk_only_location(location.name):
                continue
            if location.name in GATED_NON_JUNK_FILLER_LOCATIONS:
                continue
            add_item_rule(
                location,
                lambda item, p=player: (
                    item.player != p or item.classification != ItemClassification.filler
                ),
            )


def set_equipment_item_rules(world) -> None:
    """Gated mode: tiered equipment only at checks whose max tier allows it."""
    player = world.player

    for region in world.multiworld.regions:
        if region.player != player:
            continue
        for location in region.locations:
            max_tier = get_location_max_tier(location.name, region.name)
            if max_tier >= 5:
                continue
            add_item_rule(
                location,
                lambda item, mt=max_tier, p=player: (
                    item.player != p
                    or get_item_tier(item.name) is None
                    or get_item_tier(item.name) <= mt
                ),
            )


def prefill_tiered_equipment(world) -> None:
    """Place tiered pool items before main fill so non-tier items cannot steal slots."""
    if world.options.equipment_progression.value != 0:
        return

    player = world.player
    tiered_items: List[Item] = []
    remaining_pool: List[Item] = []

    for item in world.multiworld.itempool:
        if item.player == player and get_item_tier(item.name) is not None:
            tiered_items.append(item)
        else:
            remaining_pool.append(item)

    if not tiered_items:
        return

    location_slots: List[Tuple] = []
    for loc in world.multiworld.get_unfilled_locations(player):
        if is_junk_only_location(loc.name):
            continue
        region_name = loc.parent_region.name if loc.parent_region else "Menu"
        location_slots.append((loc, get_location_max_tier(loc.name, region_name)))

    world.random.shuffle(location_slots)
    location_slots.sort(key=lambda x: x[1], reverse=True)

    world.random.shuffle(tiered_items)
    tiered_items.sort(key=lambda i: get_item_tier(i.name) or 0, reverse=True)

    used_indices: Set[int] = set()
    for item in tiered_items:
        tier = get_item_tier(item.name)
        if tier is None:
            remaining_pool.append(item)
            continue
        placed = False
        for i, (loc, max_tier) in enumerate(location_slots):
            if i in used_indices:
                continue
            if max_tier >= tier:
                loc.place_locked_item(item)
                used_indices.add(i)
                placed = True
                break
        if not placed:
            remaining_pool.append(_random_filler_item(world))

    world.multiworld.itempool = remaining_pool


def _random_filler_item(world):
    from .Items import filler_weights

    names = list(filler_weights.keys())
    weights = list(filler_weights.values())
    return world.create_item(world.random.choices(names, weights)[0])


def _item_can_fit_unfilled_location(world, item: Item, loc) -> bool:
    player = world.player
    if item.player != player:
        return True
    if is_junk_only_location(loc.name):
        return item.classification == ItemClassification.filler
    if item.classification == ItemClassification.filler:
        return False
    tier = get_item_tier(item.name)
    if tier is None:
        return True
    region_name = loc.parent_region.name if loc.parent_region else "Menu"
    return tier <= get_location_max_tier(loc.name, region_name)


def _safe_pool_useful_item(world):
    """Low-tier / universal useful for pool rebalance (avoids tier-blocked fill)."""
    from .ItemClassAffinity import item_passes_class_filter
    from .Items import item_counts_useful, useful_items

    class_filter = world.options.class_filter.value
    for name in item_counts_useful:
        if item_passes_class_filter(class_filter, name):
            return world.create_item(name)
    tier12 = [
        name for name in useful_items
        if item_passes_class_filter(class_filter, name)
        and (get_item_tier(name) or 0) <= 2
    ]
    if tier12:
        return world.create_item(world.random.choice(tier12))
    return world.create_item(world.random.choice(list(useful_items)))


def _item_fits_any_unfilled(world, item: Item, unfilled) -> bool:
    return any(_item_can_fit_unfilled_location(world, item, loc) for loc in unfilled)


def rebalance_gated_pool_for_junk_slots(world) -> None:
    """After pre_fill, match pool filler/non-filler counts to unfilled slot types."""
    if world.options.equipment_progression.value != 0:
        return

    player = world.player
    pool = world.multiworld.itempool

    for idx, item in enumerate(pool):
        if item.player == player and get_item_tier(item.name) is not None:
            pool[idx] = _random_filler_item(world)

    _prefill_illusion_stone_for_altered_vision(world, pool, player)

    unfilled = list(world.multiworld.get_unfilled_locations(player))
    junk_unfilled = sum(1 for loc in unfilled if is_junk_only_location(loc.name))
    non_junk_unfilled = len(unfilled) - junk_unfilled
    if junk_unfilled == 0 and non_junk_unfilled == 0:
        return

    def count_filler() -> int:
        return sum(
            1 for i in pool
            if i.player == player and i.classification == ItemClassification.filler
        )

    def count_non_filler() -> int:
        return sum(
            1 for i in pool
            if i.player == player and i.classification != ItemClassification.filler
        )

    def replaceable_non_filler():
        return [
            i for i in pool
            if i.player == player
            and i.classification != ItemClassification.progression
            and i.classification != ItemClassification.filler
        ]

    def filler_indices():
        return [
            i for i, it in enumerate(pool)
            if it.player == player and it.classification == ItemClassification.filler
        ]

    for _ in range(len(pool) * 3):
        f, n, j, k = count_filler(), count_non_filler(), junk_unfilled, non_junk_unfilled
        if f == j and n == k:
            break
        if f > j and filler_indices():
            pool[filler_indices()[0]] = _safe_pool_useful_item(world)
            continue
        rep = replaceable_non_filler()
        if f < j and rep:
            pool[pool.index(rep[-1])] = _random_filler_item(world)
            continue
        if n > k and f < j and rep:
            pool[pool.index(rep[-1])] = _random_filler_item(world)
            continue
        break

    unfilled = list(world.multiworld.get_unfilled_locations(player))
    for idx, item in enumerate(pool):
        if item.player != player or _item_fits_any_unfilled(world, item, unfilled):
            continue
        if count_filler() < junk_unfilled:
            pool[idx] = _random_filler_item(world)
        else:
            pool[idx] = _safe_pool_useful_item(world)


def _prefill_illusion_stone_for_altered_vision(world, pool, player: int) -> None:
    """Altered Vision logic requires Illusion Stone; reserve it before main fill."""
    for loc in world.multiworld.get_unfilled_locations(player):
        if loc.name != "Altered Vision":
            continue
        stone_idx = next((i for i, it in enumerate(pool) if it.player == player and it.name == "Illusion Stone"), None)
        if stone_idx is not None:
            loc.place_locked_item(pool.pop(stone_idx))
        else:
            loc.place_locked_item(world.create_item("Illusion Stone"))
            # Locked fill does not pull from the pool; drop one item so pool size matches unfilled slots.
            drop_idx = next(
                (
                    i
                    for i, it in enumerate(pool)
                    if it.player == player and it.classification == ItemClassification.filler
                ),
                None,
            )
            if drop_idx is not None:
                pool.pop(drop_idx)
            elif pool:
                pool.pop()
        return


def apply_progression_rules(world) -> None:
    set_profession_junk_rules(world)
    if world.options.equipment_progression.value == 0:
        set_gated_filler_reserved_for_junk_rules(world)
        set_equipment_item_rules(world)
