from BaseClasses import Location, Region, Item, ItemClassification
from rule_builder.rules import True_
from .Locations import *
from .GoalScope import location_in_goal_scope
from .ProfessionToolData import PROFESSION_TOOL_BUYS
from .RegionGraph import region_rule
from .AtlyssRules.catalog import build_location_rule

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

def _goal_value(world) -> int:
    return int(world.options.goal)


def _in_scope(world, location_name: str, region_name: str) -> bool:
    return location_in_goal_scope(_goal_value(world), location_name, region_name)


def gen_create_regions(world):
    options = world.options

    region_map = {
        "Menu": Region("Menu", world.player, world.multiworld),
        "Sanctum": Region("Sanctum", world.player, world.multiworld),
        "Outer Sanctum": Region("Outer Sanctum", world.player, world.multiworld),
        "Arcwood Pass": Region("Arcwood Pass", world.player, world.multiworld),
        "Effold Terrace": Region("Effold Terrace", world.player, world.multiworld),
        "Tuul Valley": Region("Tuul Valley", world.player, world.multiworld),
        "Sanctum Catacombs lvl 1": Region("Sanctum Catacombs lvl 1", world.player, world.multiworld),
        "Sanctum Catacombs lvl 2": Region("Sanctum Catacombs lvl 2", world.player, world.multiworld),
        "Sanctum Catacombs lvl 3": Region("Sanctum Catacombs lvl 3", world.player, world.multiworld),
        "Crescent Road": Region("Crescent Road", world.player, world.multiworld),
        "Tuul Enclave": Region("Tuul Enclave", world.player, world.multiworld),
        "Luvora Garden": Region("Luvora Garden", world.player, world.multiworld),
        "Crescent Keep": Region("Crescent Keep", world.player, world.multiworld),
        "Bularr Fortress": Region("Bularr Fortress", world.player, world.multiworld),
        "Crescent Grove lvl 1": Region("Crescent Grove lvl 1", world.player, world.multiworld),
        "Crescent Grove lvl 2": Region("Crescent Grove lvl 2", world.player, world.multiworld),
    }

    for region in region_map.values():
        world.multiworld.regions.append(region)

    region_map["Menu"].connect(region_map["Sanctum"], rule=True_())
    region_map["Sanctum"].connect(region_map["Outer Sanctum"], rule=region_rule("Outer Sanctum"))
    region_map["Outer Sanctum"].connect(region_map["Arcwood Pass"], rule=region_rule("Arcwood Pass"))
    region_map["Outer Sanctum"].connect(region_map["Effold Terrace"], rule=region_rule("Effold Terrace"))
    region_map["Outer Sanctum"].connect(region_map["Tuul Valley"], rule=region_rule("Tuul Valley"))
    region_map["Arcwood Pass"].connect(
        region_map["Sanctum Catacombs lvl 1"],
        rule=region_rule("Sanctum Catacombs lvl 1"),
    )
    region_map["Sanctum Catacombs lvl 1"].connect(
        region_map["Sanctum Catacombs lvl 2"],
        rule=region_rule("Sanctum Catacombs lvl 2"),
    )
    region_map["Sanctum Catacombs lvl 2"].connect(
        region_map["Sanctum Catacombs lvl 3"],
        rule=region_rule("Sanctum Catacombs lvl 3"),
    )
    region_map["Arcwood Pass"].connect(region_map["Crescent Road"], rule=region_rule("Crescent Road"))
    region_map["Tuul Valley"].connect(region_map["Tuul Enclave"], rule=region_rule("Tuul Enclave"))
    region_map["Crescent Road"].connect(region_map["Luvora Garden"], rule=region_rule("Luvora Garden"))
    region_map["Crescent Road"].connect(region_map["Crescent Keep"], rule=region_rule("Crescent Keep"))
    region_map["Tuul Enclave"].connect(region_map["Bularr Fortress"], rule=region_rule("Bularr Fortress"))
    region_map["Crescent Keep"].connect(
        region_map["Crescent Grove lvl 1"],
        rule=region_rule("Crescent Grove lvl 1"),
    )
    region_map["Crescent Grove lvl 1"].connect(
        region_map["Crescent Grove lvl 2"],
        rule=region_rule("Crescent Grove lvl 2"),
    )

    if options.shop_sanity:
        for name, region_key in merchants:
            if _in_scope(world, name, region_key):
                make_location(world, name, region_map[region_key])

    for name, region_key in quests:
        if _in_scope(world, name, region_key):
            make_location(world, name, region_map[region_key])
    for name, region_key in levels:
        if _in_scope(world, name, region_key):
            make_location(world, name, region_map[region_key])
    for name, region_key in professions:
        if _in_scope(world, name, region_key):
            make_location(world, name, region_map[region_key])

    menu_region = region_map["Menu"]
    for loc_name, item_name in PROFESSION_TOOL_BUYS:
        if not _in_scope(world, loc_name, "Menu"):
            continue
        if options.profession_tools.value == 0:
            location = make_location_adv(
                world,
                loc_name,
                loc_name,
                world.location_name_to_id[loc_name],
                menu_region,
            )
            item_code = world.item_name_to_id[item_name]
            location.place_locked_item(
                Item(item_name, ItemClassification.progression, item_code, world.player))
        else:
            make_location(world, loc_name, menu_region)

    for name, region_key in bosses:
        if _in_scope(world, name, region_key):
            make_location(world, name, region_map[region_key])

    if options.achievements:
        for name, region_key in achievements:
            if _in_scope(world, name, region_key):
                make_location(world, name, region_map[region_key])

    for name, region_key in quests:
        if _in_scope(world, name, region_key):
            make_event_location(world, f"Quest Completion: {name}", name, f"Complete: {name}", None,
                                region_map[region_key])


def make_location(world, location_name, region):
    world.location_count += 1
    return make_location_adv(world, location_name, location_name, world.location_name_to_id[location_name], region)


def make_event_location(world, location_name_a, location_name_b, item_name, id, region):
    location = make_location_adv(world, location_name_a, location_name_b, id, region)
    item_code = world.item_name_to_id.get(item_name)
    location.place_locked_item(Item(item_name, ItemClassification.progression, item_code, world.player))


def make_location_adv(world, location_name_a, location_name_b, id, region):
    location = Location(world.player, location_name_a, id, region)
    region.locations.append(location)

    rule = build_location_rule(location_name_b)
    if rule is not None:
        world.set_rule(location, rule)

    return location
