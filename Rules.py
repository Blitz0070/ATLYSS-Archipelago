import math
from .Locations import *


# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

def get_rule_map(player):
    return {
        "A Warm Welcome": lambda state: can_grind_level(state, player, 1),
        "Communing Catacombs": lambda state: can_grind_level(state, player, 1) and has_quest(state, player,
                                                                                             "A Warm Welcome"),
        "Diva Must Die": lambda state: can_grind_level(state, player, 4) and has_quest(state, player,
                                                                                       "Communing Catacombs"),
        "The Keep Within": lambda state: can_grind_level(state, player, 8) and has_quest(state, player,
                                                                                         "Diva Must Die"),
        "Tethering Grove": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                          "The Keep Within"),
        "The Glyphik Booklet": lambda state: can_grind_level(state, player, 24) and has_quest(state, player,
                                                                                              "Finding Ammagon") and has_all_areas(
            state, player, ["Luvora Garden", "Tuul Enclave", "Cresent Grove lvl 2"]),
        "Cleaning Terrace": lambda state: can_grind_level(state, player, 5) and has_quest(state, player,
                                                                                          "Diva Must Die"),
        "Ancient Beings": lambda state: can_grind_level(state, player, 8) and has_quest(state, player,
                                                                                        "The Keep Within"),
        "Wicked Wizboars": lambda state: can_grind_level(state, player, 10) and has_any_area(state, player,
                                                                                             ["Tuul Valley",
                                                                                              "Cresent Keep"]),
        "Spiraling In The Grove": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                                 "Tethering Grove"),
        "Hell In The Grove": lambda state: can_grind_level(state, player, 20) and has_quest(state, player,
                                                                                            "Tethering Grove"),
        "Nulversa Magica": lambda state: can_grind_level(state, player, 20),
        "Finding Ammagon": lambda state: can_grind_level(state, player, 14),
        "The Colossus": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                       "The Keep Within"),
        "Night Spirits": lambda state: can_grind_level(state, player, 1) and has_any_area(state, player,
                                                                                          ["Arcwood Pass",
                                                                                           "Effold Terrace"]),
        "Ridding Slimes": lambda state: can_grind_level(state, player, 1),
        "Huntin' Hogs": lambda state: can_grind_level(state, player, 7) and has_any_area(state, player, ["Tuul Valley",
                                                                                                         "Cresent Keep"]),
        "Purging the Grove": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                            "The Colossus"),
        "Cleansing the Grove": lambda state: can_grind_level(state, player, 20) and has_quest(state, player,
                                                                                              "The Colossus"),
        "Nulversa Viscera": lambda state: can_grind_level(state, player, 20),
        "Call of Fury": lambda state: can_grind_level(state, player, 4),
        "Mastery of Strength": lambda state: can_grind_level(state, player, 10),
        "Beckoning Foes": lambda state: can_grind_level(state, player, 12),
        "Ghostly Goods": lambda state: can_grind_level(state, player, 1) and has_quest(state, player,
                                                                                       "A Warm Welcome") and has_any_area(
            state, player, ["Sanctum Catacombs lvl 1", "Sanctum Catacombs lvl 2", "Sanctum Catacombs lvl 3"]),
        "Makin' a Mekspear": lambda state: can_grind_level(state, player, 7) and has_area(state, player,
                                                                                          'Effold Terrace') and has_any_area(
            state, player, ["Tuul Valley", "Cresent Keep", "Effold Terrace"]),
        "Makin' a Wizwand": lambda state: can_grind_level(state, player, 10) and has_all_areas(state, player,
                                                                                               ["Tuul Valley",
                                                                                                "Cresent Road"]),
        "Makin' a Vile Blade": lambda state: can_grind_level(state, player, 10) and has_all_areas(state, player,
                                                                                                  ["Cresent Road",
                                                                                                   "Effold Terrace",
                                                                                                   "Sanctum Catacombs lvl 2"]),
        "Makin' a Golem Chestpiece": lambda state: can_grind_level(state, player, 12) and has_quest(state, player,
                                                                                                    "The Keep Within"),
        "Makin' a Ragespear": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                             "Makin' a Mekspear") and has_all_areas(
            state, player, ["Effold Terrace", "Sanctum Catacombs lvl 3", "Bularr Fortress"]),
        "Makin' a Monolith Chestpiece": lambda state: can_grind_level(state, player, 16) and has_quest(state, player,
                                                                                                       "Makin' a Golem Chestpiece"),
        "Makin' a Firebreath Blade": lambda state: can_grind_level(state, player, 20),
        "Makin' a Follycannon": lambda state: can_grind_level(state, player, 24),
        "Summore' Spectral Powder!": lambda state: can_grind_level(state, player, 1) and has_quest(state, player,
                                                                                                   "Ghostly Goods") and has_any_area(
            state, player, ["Sanctum Catacombs lvl 1", "Sanctum Catacombs lvl 2", "Sanctum Catacombs lvl 3"]),
        "Makin' More Mekspears": lambda state: can_grind_level(state, player, 7) and has_quest(state, player,
                                                                                               "Makin' a Mekspear") and has_area(
            state, player, 'Effold Terrace') and has_any_area(state, player,
                                                              ["Tuul Valley", "Cresent Keep", "Effold Terrace"]),
        "Makin' More Wizwands": lambda state: can_grind_level(state, player, 10) and has_quest(state, player,
                                                                                               "Makin' a Wizwand") and has_all_areas(
            state, player, ["Tuul Valley", "Cresent Road"]),
        "Makin' More Vile Blades": lambda state: can_grind_level(state, player, 10) and has_quest(state, player,
                                                                                                  "Makin' a Vile Blade") and has_all_areas(
            state, player, ["Cresent Road", "Effold Terrace", "Sanctum Catacombs lvl 2"]),
        "Summore' Golem Chestpieces": lambda state: can_grind_level(state, player, 12) and has_quest(state, player,
                                                                                                     "Makin' a Golem Chestpiece"),
        "Makin' More Ragespears": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                                 "Makin' a Ragespear") and has_all_areas(
            state, player, ["Effold Terrace", "Sanctum Catacombs lvl 3", "Bularr Fortress"]),
        "Summore' Monolith Chestpieces": lambda state: can_grind_level(state, player, 16) and has_quest(state, player,
                                                                                                        "Makin' a Monolith Chestpiece"),
        "Nulversa, Greenversa!": lambda state: can_grind_level(state, player, 20),
        "Summore' Firebreath Blades": lambda state: can_grind_level(state, player, 20) and has_quest(state, player,
                                                                                                     "Makin' a Firebreath Blade"),
        "Makin' More Follycannons": lambda state: can_grind_level(state, player, 24) and has_quest(state, player,
                                                                                                   "Makin' a Follycannon"),
        "Focusin' in": lambda state: can_grind_level(state, player, 4),
        "Mastery of Dexterity": lambda state: can_grind_level(state, player, 10),
        "Whatta' Rush!": lambda state: can_grind_level(state, player, 12),
        "The Voice of Zuulneruda": lambda state: can_grind_level(state, player, 6) and has_quest(state, player,
                                                                                                 "Killing Tomb"),
        "Killing Tomb": lambda state: can_grind_level(state, player, 1),
        "Purging the Undead": lambda state: can_grind_level(state, player, 6) and has_quest(state, player,
                                                                                            "Killing Tomb"),
        "Rattlecage Rage": lambda state: can_grind_level(state, player, 6) and has_quest(state, player, "Killing Tomb"),
        "Consumed Madness": lambda state: can_grind_level(state, player, 12) and has_quest(state, player,
                                                                                           "The Voice of Zuulneruda"),
        "Eradicating the Undead": lambda state: can_grind_level(state, player, 12) and has_quest(state, player,
                                                                                                 "The Voice of Zuulneruda"),
        "Reviling the Rageboars": lambda state: can_grind_level(state, player, 14),
        "Gatling Galius": lambda state: can_grind_level(state, player, 22),
        "Reviling more Rageboars": lambda state: can_grind_level(state, player, 14) and has_quest(state, player,
                                                                                                  "Reviling the Rageboars"),
        "Facing Foes": lambda state: can_grind_level(state, player, 18),
        "The Gall of Galius": lambda state: can_grind_level(state, player, 22) and has_quest(state, player,
                                                                                             "Gatling Galius"),
        "Dense Ingots": lambda state: can_grind_level(state, player, 1),
        "Amberite Ingots": lambda state: can_grind_level(state, player, 6) and has_quest(state, player,
                                                                                         "Dense Ingots") and has_any_area(
            state, player, ["Cresent Keep", "Tuul Valley"]),
        "Sapphite Ingots": lambda state: can_grind_level(state, player, 8) and has_quest(state, player,
                                                                                         "Amberite Ingots"),
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
        "Buy Item #1 from Frankie's Goods": lambda state: has_area(state, player, "Arcwood Pass"),
        "Buy Item #2 from Frankie's Goods": lambda state: has_area(state, player, "Arcwood Pass"),
        "Buy Item #3 from Frankie's Goods": lambda state: has_area(state, player, "Arcwood Pass"),
        "Buy Item #4 from Frankie's Goods": lambda state: has_area(state, player, "Arcwood Pass"),
        "Buy Item #5 from Frankie's Goods": lambda state: has_area(state, player, "Arcwood Pass"),
        "Buy Item #1 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #2 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #3 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #4 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #5 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #1 from Tesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 2"),
        "Buy Item #2 from Tesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 2"),
        "Buy Item #3 from Tesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 2"),
        "Buy Item #4 from Tesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 2"),
        "Buy Item #5 from Tesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 2"),
        "Buy Item #1 from Nesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 3"),
        "Buy Item #2 from Nesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 3"),
        "Buy Item #3 from Nesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 3"),
        "Buy Item #4 from Nesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 3"),
        "Buy Item #5 from Nesh's Wares": lambda state: has_area(state, player, "Sanctum Catacombs lvl 3"),
        "Buy Item #1 from Rikko's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 1"),
        "Buy Item #2 from Rikko's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 1"),
        "Buy Item #3 from Rikko's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 1"),
        "Buy Item #4 from Rikko's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 1"),
        "Buy Item #5 from Rikko's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 1"),
        "Buy Item #1 from Cotoo's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 2"),
        "Buy Item #2 from Cotoo's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 2"),
        "Buy Item #3 from Cotoo's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 2"),
        "Buy Item #4 from Cotoo's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 2"),
        "Buy Item #5 from Cotoo's Treasures": lambda state: has_area(state, player, "Cresent Grove lvl 2"),
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
        "Fishing Lv. 1": lambda state: can_grind_fish(state, player, 1),
        "Fishing Lv. 2": lambda state: can_grind_fish(state, player, 2),
        "Fishing Lv. 3": lambda state: can_grind_fish(state, player, 3),
        "Fishing Lv. 4": lambda state: can_grind_fish(state, player, 4),
        "Fishing Lv. 5": lambda state: can_grind_fish(state, player, 5),
        "Fishing Lv. 6": lambda state: can_grind_fish(state, player, 6),
        "Fishing Lv. 7": lambda state: can_grind_fish(state, player, 7),
        "Fishing Lv. 8": lambda state: can_grind_fish(state, player, 8),
        "Fishing Lv. 9": lambda state: can_grind_fish(state, player, 9),
        "Fishing Lv. 10": lambda state: can_grind_fish(state, player, 10),
        "Mining Lv. 1": lambda state: can_grind_mine(state, player, 1),
        "Mining Lv. 2": lambda state: can_grind_mine(state, player, 2),
        "Mining Lv. 3": lambda state: can_grind_mine(state, player, 3),
        "Mining Lv. 4": lambda state: can_grind_mine(state, player, 4),
        "Mining Lv. 5": lambda state: can_grind_mine(state, player, 5),
        "Mining Lv. 6": lambda state: can_grind_mine(state, player, 6),
        "Mining Lv. 7": lambda state: can_grind_mine(state, player, 7),
        "Mining Lv. 8": lambda state: can_grind_mine(state, player, 8),
        "Mining Lv. 9": lambda state: can_grind_mine(state, player, 9),
        "Mining Lv. 10": lambda state: can_grind_mine(state, player, 10),
        "A New Journey": lambda state: can_grind_level(state, player, 0),
        "Clearing Catacombs (1-6)": lambda state: can_grind_level(state, player, 1) and has_area(state, player,
                                                                                                 "Sanctum Catacombs lvl 1"),
        "Clearing Catacombs (6-12)": lambda state: can_grind_level(state, player, 6) and has_area(state, player,
                                                                                                  "Sanctum Catacombs lvl 2"),
        "Clearing Catacombs (12-18)": lambda state: can_grind_level(state, player, 12) and has_area(state, player,
                                                                                                    "Sanctum Catacombs lvl 3"),
        "Clearing Grove (15-20)": lambda state: can_grind_level(state, player, 15) and has_area(state, player,
                                                                                                "Cresent Grove lvl 1"),
        "Clearing Grove (20-25)": lambda state: can_grind_level(state, player, 20) and has_area(state, player,
                                                                                                "Cresent Grove lvl 2"),
        "Altered Vision": lambda state: can_grind_level(state, player, 0) and has_item(state, player, "Illusion Stone",
                                                                                       1),
        "Scaling the Tower": lambda state: can_grind_level(state, player, 0),
        "Rude!": lambda state: can_grind_level(state, player, 0),
        "Fashion Sense": lambda state: can_grind_level(state, player, 0),
        "Trout Master": lambda state: can_grind_fish(state, player, 10),
        "Skill Student": lambda state: can_grind_level(state, player, 10),
        "Slime Diva": lambda state: can_beat_enemy(state, player, "Slime Diva"),
        "Lord Zuulneruda": lambda state: can_beat_enemy(state, player, "Lord Zuulneruda"),
        "Lord Kaluuz": lambda state: can_beat_enemy(state, player, "Lord Kaluuz"),
        "Colossus": lambda state: can_beat_enemy(state, player, "Colossus"),
        "Valdur": lambda state: can_beat_enemy(state, player, "Valdur"),
        "Galius": lambda state: can_beat_enemy(state, player, "Galius"),
    }


def has_area(state, player, area) -> bool:
    if not state.multiworld.worlds[player].options.random_portals:
        return state.has("Progressive Portal", player, portal_counts[area])
    if area.startswith("Sanctum Catacombs"):
        area = "Catacombs"
    portal = f"{area} Portal"
    return state.has(portal, player, 1)


def has_any_area(state, player, areas) -> bool:
    return any(has_area(state, player, area) for area in areas)


def has_all_areas(state, player, areas) -> bool:
    return all(has_area(state, player, area) for area in areas)


def has_quest(state, player, quest) -> bool:
    return state.has(f"Complete: {quest}", player, 1)


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
    return can_grind_level(state, player, enemy_data[enemy_name][0]) and has_any_area(state, player,
                                                                                      enemy_data[enemy_name][1])


def has_item(state, player, item, count) -> bool:
    return state.has(item, player, count)