from BaseClasses import Location, Region, Item, ItemClassification
from .Locations import *
from .Rules import *
from .GoalScope import location_in_goal_scope
from .ProfessionToolData import PROFESSION_TOOL_BUYS
from .RegionGraph import region_rule

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

def _goal_value(world) -> int:
    return int(world.options.goal)


def _in_scope(world, location_name: str, region_name: str) -> bool:
    return location_in_goal_scope(_goal_value(world), location_name, region_name)


def gen_create_regions(world):
    player = world.player
    options = world.options
    rule_map = get_rule_map(world.player)

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
        "Cresent Road": Region("Cresent Road", world.player, world.multiworld),
        "Tuul Enclave": Region("Tuul Enclave", world.player, world.multiworld),
        "Luvora Garden": Region("Luvora Garden", world.player, world.multiworld),
        "Cresent Keep": Region("Cresent Keep", world.player, world.multiworld),
        "Bularr Fortress": Region("Bularr Fortress", world.player, world.multiworld),
        "Cresent Grove lvl 1": Region("Cresent Grove lvl 1", world.player, world.multiworld),
        "Cresent Grove lvl 2": Region("Cresent Grove lvl 2", world.player, world.multiworld),
    }

    region_map["Menu"].connect(region_map["Sanctum"], rule=lambda state: True)
    region_map["Sanctum"].connect(region_map["Outer Sanctum"], rule=region_rule(player, "Outer Sanctum"))
    region_map["Outer Sanctum"].connect(region_map["Arcwood Pass"], rule=region_rule(player, "Arcwood Pass"))
    region_map["Outer Sanctum"].connect(
        region_map["Effold Terrace"],
        rule=region_rule(player, "Effold Terrace", lambda s: has_quest(s, player, "Communing Catacombs")),
    )
    region_map["Outer Sanctum"].connect(region_map["Tuul Valley"], rule=region_rule(player, "Tuul Valley"))
    region_map["Arcwood Pass"].connect(
        region_map["Sanctum Catacombs lvl 1"],
        rule=region_rule(player, "Sanctum Catacombs lvl 1", lambda s: has_quest(s, player, "Communing Catacombs")),
    )
    region_map["Sanctum Catacombs lvl 1"].connect(
        region_map["Sanctum Catacombs lvl 2"],
        rule=region_rule(player, "Sanctum Catacombs lvl 2"),
    )
    region_map["Sanctum Catacombs lvl 2"].connect(
        region_map["Sanctum Catacombs lvl 3"],
        rule=region_rule(player, "Sanctum Catacombs lvl 3"),
    )
    region_map["Arcwood Pass"].connect(
        region_map["Cresent Road"],
        rule=region_rule(player, "Cresent Road", lambda s: has_quest(s, player, "The Keep Within")),
    )
    region_map["Tuul Valley"].connect(region_map["Tuul Enclave"], rule=region_rule(player, "Tuul Enclave"))
    region_map["Cresent Road"].connect(region_map["Luvora Garden"], rule=region_rule(player, "Luvora Garden"))
    region_map["Cresent Road"].connect(region_map["Cresent Keep"], rule=region_rule(player, "Cresent Keep"))
    region_map["Tuul Enclave"].connect(
        region_map["Bularr Fortress"],
        rule=region_rule(player, "Bularr Fortress", lambda s: has_quest(s, player, "Finding Ammagon")),
    )
    region_map["Cresent Keep"].connect(
        region_map["Cresent Grove lvl 1"],
        rule=region_rule(player, "Cresent Grove lvl 1", lambda s: has_quest(s, player, "The Keep Within")),
    )
    region_map["Cresent Grove lvl 1"].connect(
        region_map["Cresent Grove lvl 2"],
        rule=region_rule(player, "Cresent Grove lvl 2"),
    )

    if options.shop_sanity:
        for name, region_key in merchants:
            if _in_scope(world, name, region_key):
                make_location(world, name, region_map[region_key], rule_map)

    for name, region_key in quests:
        if _in_scope(world, name, region_key):
            make_location(world, name, region_map[region_key], rule_map)
    for name, region_key in levels:
        if _in_scope(world, name, region_key):
            make_location(world, name, region_map[region_key], rule_map)
    for name, region_key in professions:
        if _in_scope(world, name, region_key):
            make_location(world, name, region_map[region_key], rule_map)

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
                rule_map,
            )
            item_code = world.item_name_to_id[item_name]
            location.place_locked_item(
                Item(item_name, ItemClassification.progression, item_code, world.player))
        else:
            make_location(world, loc_name, menu_region, rule_map)

    for name, region_key in bosses:
        if _in_scope(world, name, region_key):
            make_location(world, name, region_map[region_key], rule_map)

    if options.achievements:
        for name, region_key in achievements:
            if _in_scope(world, name, region_key):
                make_location(world, name, region_map[region_key], rule_map)

    for name, region_key in quests:
        if _in_scope(world, name, region_key):
            make_event_location(world, f"Quest Completion: {name}", name, f"Complete: {name}", None,
                                region_map[region_key], rule_map)

    for region in region_map.values():
        world.multiworld.regions.append(region)


def make_location(world, location_name, region, rule_map):
    world.location_count += 1
    return make_location_adv(world, location_name, location_name, world.location_name_to_id[location_name], region,
                             rule_map)


def make_event_location(world, location_name_a, location_name_b, item_name, id, region, rule_map):
    location = make_location_adv(world, location_name_a, location_name_b, id, region, rule_map)
    item_code = world.item_name_to_id.get(item_name)
    location.place_locked_item(Item(item_name, ItemClassification.progression, item_code, world.player))


def make_location_adv(world, location_name_a, location_name_b, id, region, rule_map):
    location = Location(world.player, location_name_a, id, region)
    region.locations.append(location)

    if location_name_b in rule_map:
        location.access_rule = rule_map[location_name_b]

    return location
