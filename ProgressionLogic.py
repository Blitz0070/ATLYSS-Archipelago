"""
Equipment tier helpers and fill constraints (Phase A of fork port plan).
"""
from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from BaseClasses import Item, ItemClassification
from worlds.generic.Rules import add_item_rule

from .AccessData import parse_shop_buy_location, shop_slot_tier_level
from .GoalScope import _get_location_min_grind_levels
from .ItemTiers import get_item_tier, get_progressive_item_tiers
from .Locations import _HIGH_LEVEL_JUNK_MILESTONES, location_grind_data


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

    parsed_shop = parse_shop_buy_location(location_name)
    if parsed_shop is not None:
        slot, merchant = parsed_shop
        return shop_slot_tier_level(merchant, slot)

    parsed = _get_location_min_grind_levels().get(location_name)
    if parsed is not None:
        return parsed

    return 1


def get_location_max_tier(location_name: str, region_name: str) -> int:
    """Max equipment tier allowed at a check.

    Menu milestones and shop rows use explicit level bands.  Quests/achievements
    listed under the generic ``Sanctum`` region must not use REGION_MAX_TIER for
    ``Sanctum``(0,0 grind row → tier 1 only); use each check's min grind level
    and the destination region's band, whichever is higher.
    """
    if parse_shop_buy_location(location_name) is not None:
        return level_to_max_tier(get_menu_location_effective_level(location_name))
    if region_name == "Menu":
        return level_to_max_tier(get_menu_location_effective_level(location_name))
    named_min = _get_location_min_grind_levels().get(location_name)
    if named_min is not None:
        region_tier = REGION_MAX_TIER.get(region_name, 1)
        return max(region_tier, level_to_max_tier(named_min))
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
    tiered_items: List[Tuple[Item, int]] = []
    remaining_pool: List[Item] = []
    progressive_copy_counts: Dict[str, int] = {}

    for item in world.multiworld.itempool:
        if item.player != player:
            remaining_pool.append(item)
            continue

        tier = get_item_tier(item.name)
        # Progressive AP items are abstract names; tier them by copy index so
        # late concrete rewards (e.g. class armor) cannot be placed early.
        progressive_tiers = get_progressive_item_tiers(item.name)
        if tier is None and progressive_tiers is not None:
            copy_index = progressive_copy_counts.get(item.name, 0)
            tier = progressive_tiers[min(copy_index, len(progressive_tiers) - 1)]
            progressive_copy_counts[item.name] = copy_index + 1

        if tier is None:
            remaining_pool.append(item)
        else:
            tiered_items.append((item, tier))

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
    tiered_items.sort(key=lambda entry: entry[1], reverse=True)

    used_indices: Set[int] = set()
    for item, tier in tiered_items:
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

    pool = world.multiworld.itempool
    pool.clear()
    pool.extend(remaining_pool)


def _random_filler_item(world):
    from .Items import pick_filler_item_name

    return world.create_item(pick_filler_item_name(world.random))


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
    """Low-tier useful for gated pool rebalance (not item_counts_useful — those are gen-only)."""
    from .ItemClassAffinity import item_passes_class_filter
    from .Items import useful_items

    class_filter = world.options.class_filter.value
    tier12 = [
        name for name in useful_items
        if item_passes_class_filter(class_filter, name)
        and get_item_tier(name) is not None
        and get_item_tier(name) <= 2
    ]
    if tier12:
        return world.create_item(world.random.choice(tier12))
    tiered = [
        name for name in useful_items
        if item_passes_class_filter(class_filter, name)
        and get_item_tier(name) is not None
    ]
    if tiered:
        return world.create_item(world.random.choice(tiered))
    filtered = [name for name in useful_items if item_passes_class_filter(class_filter, name)]
    return world.create_item(world.random.choice(filtered))


def _item_fits_any_unfilled(world, item: Item, unfilled) -> bool:
    return any(_item_can_fit_unfilled_location(world, item, loc) for loc in unfilled)


def rebalance_gated_pool_for_junk_slots(world) -> None:
    """After pre_fill, match pool filler/non-filler counts to unfilled slot types."""
    if world.options.equipment_progression.value != 0:
        return

    player = world.player
    pool = world.multiworld.itempool

    for idx, item in enumerate(pool):
        if item.player == player and (get_item_tier(item.name) is not None or get_progressive_item_tiers(item.name) is not None):
            pool[idx] = _random_filler_item(world)

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

def apply_progression_rules(world) -> None:
    set_profession_junk_rules(world)
    if world.options.equipment_progression.value == 0:
        set_gated_filler_reserved_for_junk_rules(world)
        set_equipment_item_rules(world)
