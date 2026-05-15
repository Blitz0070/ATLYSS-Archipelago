import math
from .Locations import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

def has_fishing_tool_for_logic(state, player) -> bool:
    return state.has("Fishing Rod", player, 1)


def has_mining_tool_for_logic(state, player) -> bool:
    return state.has("Pickaxe", player, 1)


def get_rule_map(player):
    return {
        "A Warm Welcome": lambda state: can_grind_level(state, player, 1),
        "Communing Catacombs": lambda state: can_grind_level(state, player, 1) and has_quest(state, player,
                                                                                             "A Warm Welcome")
        and has_catacombs_route(state, player),
        "Diva Must Die": lambda state: can_grind_level(state, player, 4) and has_quest(state, player,
                                                                                       "Communing Catacombs"),
        "The Keep Within": lambda state: can_grind_level(state, player, 8) and has_quest(state, player,
                                                                                         "Diva Must Die"),
        "Tethering Grove": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                          "The Keep Within")
        and has_grove_colossus_route(state, player),
        "The Glyphik Booklet": lambda state: can_grind_level(state, player, 24) and has_quest(state, player,
                                                                                              "Finding Ammagon")
        and has_portal_route(state, player, ("Luvora Garden", "Tuul Enclave", "Cresent Grove lvl 2")),
        "Cleaning Terrace": lambda state: can_grind_level(state, player, 5) and has_quest(state, player,
                                                                                          "Diva Must Die")
        and has_effold_route(state, player),
        "Ancient Beings": lambda state: can_grind_level(state, player, 8) and has_quest(state, player,
                                                                                        "The Keep Within")
        and has_crescent_road_keep_route(state, player),
        "Wicked Wizboars": lambda state: can_grind_level(state, player, 10) and has_tuul_valley_route(state, player),
        "Spiraling In The Grove": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                                 "Tethering Grove")
        and has_grove_colossus_route(state, player),
        "Hell In The Grove": lambda state: can_grind_level(state, player, 20) and has_quest(state, player,
                                                                                            "Tethering Grove")
        and has_portal_route(state, player, ("Cresent Grove lvl 1", "Cresent Grove lvl 2")),
        "Nulversa Magica": lambda state: can_grind_level(state, player, 20),
        "Finding Ammagon": lambda state: can_grind_level(state, player, 14) and has_bularr_route(state, player),
        "The Colossus": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                       "The Keep Within")
        and has_grove_colossus_route(state, player),
        "Night Spirits": lambda state: can_grind_level(state, player, 1) and has_arcwood_route(state, player),
        "Ridding Slimes": lambda state: can_grind_level(state, player, 1) and has_outer_sanctum_route(state, player),
        "Huntin' Hogs": lambda state: can_grind_level(state, player, 7) and has_tuul_valley_route(state, player),
        "Purging the Grove": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                            "The Colossus")
        and has_grove_colossus_route(state, player),
        "Cleansing the Grove": lambda state: can_grind_level(state, player, 20) and has_quest(state, player,
                                                                                              "The Colossus")
        and has_portal_route(state, player, ("Cresent Grove lvl 1", "Cresent Grove lvl 2")),
        "Nulversa Viscera": lambda state: can_grind_level(state, player, 20),
        "Call of Fury": lambda state: can_grind_level(state, player, 4) and has_outer_sanctum_route(state, player),
        "Mastery of Strength": lambda state: can_grind_level(state, player, 10),
        "Beckoning Foes": lambda state: can_grind_level(state, player, 12),
        "Ghostly Goods": lambda state: can_grind_level(state, player, 1) and has_quest(state, player,
                                                                                       "A Warm Welcome")
        and has_catacombs_route(state, player),
        "Makin' a Mekspear": lambda state: can_grind_level(state, player, 7) and has_mekspear_route(state, player),
        "Makin' a Wizwand": lambda state: can_grind_level(state, player, 10) and has_wizwand_route(state, player),
        "Makin' a Vile Blade": lambda state: can_grind_level(state, player, 10) and has_vile_blade_route(state, player),
        "Makin' a Golem Chestpiece": lambda state: can_grind_level(state, player, 12) and has_quest(state, player,
                                                                                                    "The Keep Within")
        and has_golem_chest_route(state, player),
        "Makin' a Ragespear": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                             "Makin' a Mekspear")
        and has_ragespear_route(state, player),
        "Makin' a Monolith Chestpiece": lambda state: can_grind_level(state, player, 16) and has_quest(state, player,
                                                                                                       "Makin' a Golem Chestpiece"),
        "Makin' a Firebreath Blade": lambda state: can_grind_level(state, player, 20),
        "Makin' a Follycannon": lambda state: can_grind_level(state, player, 24),
        "Summore' Spectral Powder!": lambda state: can_grind_level(state, player, 1) and has_quest(state, player,
                                                                                                   "Ghostly Goods")
        and has_catacombs_route(state, player),
        "Makin' More Mekspears": lambda state: can_grind_level(state, player, 7) and has_quest(state, player,
                                                                                               "Makin' a Mekspear")
        and has_mekspear_route(state, player),
        "Makin' More Wizwands": lambda state: can_grind_level(state, player, 10) and has_quest(state, player,
                                                                                               "Makin' a Wizwand")
        and has_wizwand_route(state, player),
        "Makin' More Vile Blades": lambda state: can_grind_level(state, player, 10) and has_quest(state, player,
                                                                                                  "Makin' a Vile Blade")
        and has_vile_blade_route(state, player),
        "Summore' Golem Chestpieces": lambda state: can_grind_level(state, player, 12) and has_quest(state, player,
                                                                                                     "Makin' a Golem Chestpiece")
        and has_golem_chest_route(state, player),
        "Makin' More Ragespears": lambda state: can_grind_level(state, player, 15) and has_quest(state, player,
                                                                                                 "Makin' a Ragespear")
        and has_ragespear_route(state, player),
        "Summore' Monolith Chestpieces": lambda state: can_grind_level(state, player, 16) and has_quest(state, player,
                                                                                                        "Makin' a Monolith Chestpiece"),
        "Nulversa, Greenversa!": lambda state: can_grind_level(state, player, 20),
        "Summore' Firebreath Blades": lambda state: can_grind_level(state, player, 20) and has_quest(state, player,
                                                                                                     "Makin' a Firebreath Blade"),
        "Makin' More Follycannons": lambda state: can_grind_level(state, player, 24) and has_quest(state, player,
                                                                                                   "Makin' a Follycannon"),
        "Focusin' in": lambda state: can_grind_level(state, player, 4) and has_outer_sanctum_route(state, player),
        "Mastery of Dexterity": lambda state: can_grind_level(state, player, 10),
        "Whatta' Rush!": lambda state: can_grind_level(state, player, 12),
        "The Voice of Zuulneruda": lambda state: can_grind_level(state, player, 6) and has_quest(state, player,
                                                                                                 "Killing Tomb"),
        "Killing Tomb": lambda state: can_grind_level(state, player, 1) and has_catacombs_route(state, player),
        "Purging the Undead": lambda state: can_grind_level(state, player, 6) and has_quest(state, player,
                                                                                            "Killing Tomb")
        and has_catacombs_route(state, player),
        "Rattlecage Rage": lambda state: can_grind_level(state, player, 6) and has_quest(state, player, "Killing Tomb")
        and has_catacombs_route(state, player),
        "Consumed Madness": lambda state: can_grind_level(state, player, 12) and has_quest(state, player,
                                                                                           "The Voice of Zuulneruda")
        and has_catacombs_route(state, player),
        "Eradicating the Undead": lambda state: can_grind_level(state, player, 12) and has_quest(state, player,
                                                                                                 "The Voice of Zuulneruda")
        and has_catacombs_route(state, player),
        "Reviling the Rageboars": lambda state: can_grind_level(state, player, 14) and has_bularr_route(state, player),
        "Gatling Galius": lambda state: can_grind_level(state, player, 22),
        "Reviling more Rageboars": lambda state: can_grind_level(state, player, 14) and has_quest(state, player,
                                                                                                  "Reviling the Rageboars")
        and has_bularr_route(state, player),
        "Facing Foes": lambda state: can_grind_level(state, player, 18),
        "The Gall of Galius": lambda state: can_grind_level(state, player, 22) and has_quest(state, player,
                                                                                             "Gatling Galius"),
        "Dense Ingots": lambda state: can_grind_level(state, player, 1) and has_arcwood_route(state, player),
        "Amberite Ingots": lambda state: can_grind_level(state, player, 6) and has_quest(state, player,
                                                                                         "Dense Ingots")
        and has_tuul_valley_route(state, player),
        "Sapphite Ingots": lambda state: can_grind_level(state, player, 8) and has_quest(state, player,
                                                                                         "Amberite Ingots")
        and has_tuul_enclave_route(state, player),
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
        "Buy Item #1 from Frankie's Goods": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #2 from Frankie's Goods": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #3 from Frankie's Goods": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #4 from Frankie's Goods": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #5 from Frankie's Goods": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #1 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #2 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #3 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #4 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #5 from Dye Merchant": lambda state: has_area(state, player, "Sanctum"),
        "Buy Item #1 from Tesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #2 from Tesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #3 from Tesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #4 from Tesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #5 from Tesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #1 from Nesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #2 from Nesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #3 from Nesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #4 from Nesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #5 from Nesh's Wares": lambda state: has_arcwood_shop_route(state, player),
        "Buy Item #1 from Rikko's Treasures": lambda state: has_grove_colossus_route(state, player),
        "Buy Item #2 from Rikko's Treasures": lambda state: has_grove_colossus_route(state, player),
        "Buy Item #3 from Rikko's Treasures": lambda state: has_grove_colossus_route(state, player),
        "Buy Item #4 from Rikko's Treasures": lambda state: has_grove_colossus_route(state, player),
        "Buy Item #5 from Rikko's Treasures": lambda state: has_grove_colossus_route(state, player),
        "Buy Item #1 from Cotoo's Treasures": lambda state: has_grove_full_route(state, player),
        "Buy Item #2 from Cotoo's Treasures": lambda state: has_grove_full_route(state, player),
        "Buy Item #3 from Cotoo's Treasures": lambda state: has_grove_full_route(state, player),
        "Buy Item #4 from Cotoo's Treasures": lambda state: has_grove_full_route(state, player),
        "Buy Item #5 from Cotoo's Treasures": lambda state: has_grove_full_route(state, player),
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
        "A New Journey": lambda state: can_grind_level(state, player, 0),
        "Clearing Catacombs (1-6)": lambda state: can_grind_level(state, player, 1) and has_area(state, player,
                                                                                                 "Sanctum Catacombs lvl 1"),
        "Clearing Catacombs (6-12)": lambda state: can_grind_level(state, player, 6) and has_area(state, player,
                                                                                                  "Sanctum Catacombs lvl 2"),
        "Becoming a Fighter": lambda state: can_grind_level(state, player, 10),
        "Becoming a Mystic": lambda state: can_grind_level(state, player, 10),
        "Becoming a Bandit": lambda state: can_grind_level(state, player, 10),
        "Clearing Catacombs (12-18)": lambda state: can_grind_level(state, player, 12) and has_area(state, player,
                                                                                                    "Sanctum Catacombs lvl 3"),
        "Clearing Grove (15-20)": lambda state: can_grind_level(state, player, 15) and has_area(state, player,
                                                                                                "Cresent Grove lvl 1"),
        "Clearing Grove (20-25)": lambda state: can_grind_level(state, player, 20) and has_area(state, player,
                                                                                                "Cresent Grove lvl 2"),
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


# Fork parity: every region on the route must be reachable (all portals on path in random mode).
_CATACOMBS_ROUTE = ("Outer Sanctum", "Arcwood Pass", "Sanctum Catacombs lvl 1")
_ARCWOOD_ROUTE = ("Outer Sanctum", "Arcwood Pass")
_OUTER_SANCTUM_ROUTE = ("Outer Sanctum",)
_EFFOLD_ROUTE = ("Effold Terrace",)
_TUUL_VALLEY_ROUTE = ("Tuul Valley",)
_TUUL_ENCLAVE_ROUTE = ("Tuul Valley", "Tuul Enclave")
_BULARR_ROUTE = ("Tuul Valley", "Tuul Enclave", "Bularr Fortress")
_CRESCENT_ROAD_KEEP_ROUTE = ("Cresent Road", "Cresent Keep")
_GROVE_COLOSSUS_ROUTE = ("Cresent Grove lvl 1", "Cresent Road", "Cresent Keep")
_GROVE_FULL_ROUTE = ("Cresent Grove lvl 1", "Cresent Grove lvl 2", "Cresent Road", "Cresent Keep")
_MEKSPEAR_ROUTE = ("Tuul Valley", "Effold Terrace", "Outer Sanctum", "Arcwood Pass", "Sanctum Catacombs lvl 1")
_WIZWAND_ROUTE = ("Cresent Road", "Effold Terrace", "Tuul Valley", "Outer Sanctum", "Arcwood Pass", "Sanctum Catacombs lvl 1")
_VILE_BLADE_ROUTE = ("Cresent Road", "Effold Terrace", "Outer Sanctum", "Arcwood Pass", "Sanctum Catacombs lvl 1")
_GOLEM_CHEST_ROUTE = ("Cresent Road", "Cresent Keep", "Effold Terrace", "Outer Sanctum", "Arcwood Pass", "Sanctum Catacombs lvl 1")
_RAGESPEAR_ROUTE = ("Bularr Fortress", "Outer Sanctum", "Tuul Valley", "Tuul Enclave")
# Fork shop/profession portal matrix (Improved-Logic rules.py SHOP + PROFESSION blocks).
_ARCWOOD_SHOP_ROUTE = _ARCWOOD_ROUTE
_FISHING_MID_ROUTE = _CATACOMBS_ROUTE
_FISHING_HIGH_ROUTE = (
    "Cresent Road", "Effold Terrace", "Outer Sanctum", "Arcwood Pass", "Sanctum Catacombs lvl 1"
)
_MINING_EARLY_ROUTE = _ARCWOOD_ROUTE
_MINING_MID_ROUTE = ("Tuul Valley", "Outer Sanctum")
_MINING_HIGH_ROUTE = ("Tuul Valley", "Outer Sanctum", "Tuul Enclave")


def has_any_area(state, player, areas) -> bool:
    return any(has_area(state, player, area) for area in areas)


def has_all_areas(state, player, areas) -> bool:
    return all(has_area(state, player, area) for area in areas)


def has_portal_route(state, player, areas: tuple) -> bool:
    """All regions on route: per-area portal_counts in progressive mode, all named portals in random mode."""
    if not state.multiworld.worlds[player].options.random_portals:
        return all(has_area(state, player, area) for area in areas)
    return has_all_areas(state, player, areas)


def has_catacombs_route(state, player) -> bool:
    return has_portal_route(state, player, _CATACOMBS_ROUTE)


def has_arcwood_route(state, player) -> bool:
    return has_portal_route(state, player, _ARCWOOD_ROUTE)


def has_outer_sanctum_route(state, player) -> bool:
    return has_portal_route(state, player, _OUTER_SANCTUM_ROUTE)


def has_effold_route(state, player) -> bool:
    return has_portal_route(state, player, _EFFOLD_ROUTE)


def has_tuul_valley_route(state, player) -> bool:
    return has_portal_route(state, player, _TUUL_VALLEY_ROUTE)


def has_tuul_enclave_route(state, player) -> bool:
    return has_portal_route(state, player, _TUUL_ENCLAVE_ROUTE)


def has_bularr_route(state, player) -> bool:
    return has_portal_route(state, player, _BULARR_ROUTE)


def has_crescent_road_keep_route(state, player) -> bool:
    return has_portal_route(state, player, _CRESCENT_ROAD_KEEP_ROUTE)


def has_grove_colossus_route(state, player) -> bool:
    return has_portal_route(state, player, _GROVE_COLOSSUS_ROUTE)


def has_mekspear_route(state, player) -> bool:
    return has_portal_route(state, player, _MEKSPEAR_ROUTE)


def has_wizwand_route(state, player) -> bool:
    return has_portal_route(state, player, _WIZWAND_ROUTE)


def has_vile_blade_route(state, player) -> bool:
    return has_portal_route(state, player, _VILE_BLADE_ROUTE)


def has_golem_chest_route(state, player) -> bool:
    return has_portal_route(state, player, _GOLEM_CHEST_ROUTE)


def has_ragespear_route(state, player) -> bool:
    return has_portal_route(state, player, _RAGESPEAR_ROUTE)


def has_arcwood_shop_route(state, player) -> bool:
    return has_portal_route(state, player, _ARCWOOD_SHOP_ROUTE)


def has_grove_full_route(state, player) -> bool:
    return has_portal_route(state, player, _GROVE_FULL_ROUTE)


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
        return has_catacombs_route(state, player)
    if areas == ["Effold Terrace"]:
        return has_effold_route(state, player)
    if areas == ["Cresent Grove lvl 1"]:
        return has_grove_colossus_route(state, player)
    if areas == ["Cresent Grove lvl 2"]:
        return has_portal_route(state, player, _GROVE_FULL_ROUTE)
    if areas == ["Bularr Fortress"]:
        return has_bularr_route(state, player)
    return has_portal_route(state, player, tuple(areas))


def has_item(state, player, item, count) -> bool:
    return state.has(item, player, count)