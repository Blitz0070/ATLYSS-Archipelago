from BaseClasses import Location, Region, Item, ItemClassification, LocationProgressType
from .Locations import *
from .Rules import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

priority_map = []


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
    region_map["Sanctum"].connect(region_map["Outer Sanctum"],
                                  rule=lambda state: has_area(state, player, "Outer Sanctum"))
    region_map["Outer Sanctum"].connect(region_map["Arcwood Pass"],
                                        rule=lambda state: has_area(state, player, "Arcwood Pass"))
    region_map["Outer Sanctum"].connect(region_map["Effold Terrace"],
                                        rule=lambda state: has_area(state, player, "Effold Terrace") and has_quest(
                                            state, player, "Diva Must Die"))
    region_map["Outer Sanctum"].connect(region_map["Tuul Valley"],
                                        rule=lambda state: has_area(state, player, "Tuul Valley"))
    region_map["Arcwood Pass"].connect(region_map["Sanctum Catacombs lvl 1"], rule=lambda state: has_area(state, player,
                                                                                                          "Sanctum Catacombs lvl 1") and has_quest(
        state, player, "Communing Catacombs"))
    region_map["Sanctum Catacombs lvl 1"].connect(region_map["Sanctum Catacombs lvl 2"],
                                                  rule=lambda state: has_area(state, player, "Sanctum Catacombs lvl 2"))
    region_map["Sanctum Catacombs lvl 2"].connect(region_map["Sanctum Catacombs lvl 3"],
                                                  rule=lambda state: has_area(state, player, "Sanctum Catacombs lvl 3"))
    region_map["Arcwood Pass"].connect(region_map["Cresent Road"],
                                       rule=lambda state: has_area(state, player, "Cresent Road") and has_quest(state,
                                                                                                                player,
                                                                                                                "The Keep Within"))
    region_map["Tuul Valley"].connect(region_map["Tuul Enclave"],
                                      rule=lambda state: has_area(state, player, "Tuul Enclave"))
    region_map["Cresent Road"].connect(region_map["Luvora Garden"],
                                       rule=lambda state: has_area(state, player, "Luvora Garden"))
    region_map["Cresent Road"].connect(region_map["Cresent Keep"],
                                       rule=lambda state: has_area(state, player, "Cresent Keep"))
    region_map["Tuul Enclave"].connect(region_map["Bularr Fortress"],
                                       rule=lambda state: has_area(state, player, "Bularr Fortress") and has_quest(
                                           state, player, "Finding Ammagon"))
    region_map["Cresent Keep"].connect(region_map["Cresent Grove lvl 1"],
                                       rule=lambda state: has_area(state, player, "Cresent Grove lvl 1") and has_quest(
                                           state, player, "The Keep Within"))
    region_map["Cresent Grove lvl 1"].connect(region_map["Cresent Grove lvl 2"],
                                              rule=lambda state: has_area(state, player, "Cresent Grove lvl 2"))
    if options.shop_sanity:
        for location in merchants:
            make_location(world, location[0], region_map[location[1]], rule_map)

    for location in quests:
        make_location(world, location[0], region_map[location[1]], rule_map)
    for location in levels:
        make_location(world, location[0], region_map[location[1]], rule_map)
    for location in professions:
        make_location(world, location[0], region_map[location[1]], rule_map)
    for location in bosses:
        make_location(world, location[0], region_map[location[1]], rule_map)

    # Achievement locations: opt-in via the `achievements` yaml toggle (default on). When disabled, none of these
    # are placed in the world and the C# mod also short-circuits SendAchievementCheck via slot data, so a slot
    # generated with achievements=false will not receive nor emit achievement checks during play.
    if options.achievements:
        make_location(world, "A New Journey", region_map["Sanctum"], rule_map)
        make_location(world, "Clearing Catacombs (1-6)", region_map["Sanctum Catacombs lvl 1"], rule_map)
        make_location(world, "Clearing Catacombs (6-12)", region_map["Sanctum Catacombs lvl 2"], rule_map)
        make_location(world, "Clearing Catacombs (12-18)", region_map["Sanctum Catacombs lvl 3"], rule_map)
        make_location(world, "Clearing Grove (15-20)", region_map["Cresent Grove lvl 1"], rule_map)
        make_location(world, "Clearing Grove (20-25)", region_map["Cresent Grove lvl 2"], rule_map)
        make_location(world, "Altered Vision", region_map["Sanctum"], rule_map)
        make_location(world, "Scaling the Tower", region_map["Sanctum"], rule_map)
        make_location(world, "Rude!", region_map["Sanctum"], rule_map)
        make_location(world, "Fashion Sense", region_map["Sanctum"], rule_map)
        make_location(world, "Trout Master", region_map["Sanctum"], rule_map)
        make_location(world, "Skill Student", region_map["Sanctum"], rule_map)

    for location in quests:
        make_event_location(world, f"Quest Completion: {location[0]}", location[0], f"Complete: {location[0]}", None,
                            region_map[location[1]], rule_map)

    # Class-specific achievement locations are gated by both the achievements toggle AND the active class set.
    if options.achievements and options.is_class("fighter"):
        make_location(world, "Becoming a Fighter", region_map["Sanctum"], rule_map)
        make_location(world, "Judgement", region_map["Sanctum"], rule_map)

    if options.achievements and options.is_class("mystic"):
        make_location(world, "Becoming a Mystic", region_map["Sanctum"], rule_map)
        make_location(world, "Corrupted Arcana", region_map["Sanctum"], rule_map)
        make_location(world, "Holier than Thou", region_map["Sanctum"], rule_map)

    if options.achievements and options.is_class("bandit"):
        make_location(world, "Becoming a Bandit", region_map["Sanctum"], rule_map)

    for region in region_map.values():
        world.multiworld.regions.append(region)


def make_location(world, location_name, region, rule_map):
    world.location_count += 1
    return make_location_adv(world, location_name, location_name, world.location_name_to_id[location_name], region,
                             rule_map)


def make_event_location(world, location_name_a, location_name_b, item_name, id, region, rule_map):
    location = make_location_adv(world, location_name_a, location_name_b, id, region, rule_map)
    location.place_locked_item(Item(item_name, ItemClassification.progression, None, world.player))


def make_location_adv(world, location_name_a, location_name_b, id, region, rule_map):
    location = Location(world.player, location_name_a, id, region)
    region.locations.append(location)

    if location_name_b in rule_map:
        location.access_rule = rule_map[location_name_b]

    if location_name_a in priority_map:
        location.progress_type = priority_map[location_name_a]

    return location