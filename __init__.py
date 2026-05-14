from worlds.AutoWorld import World
from .Locations import *
from .Rules import *
from .Options import *
from .Items import *
from .Regions import *
from .Settings import *
from typing import *


# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

class Atlyss(World):
    """
	Atlyss
	"""
    game = "Atlyss"
    options_dataclass = AtlyssOptions
    options: AtlyssOptions
    settings: ClassVar[AtlyssSettings]
    location_name_to_id = {value: location_dict.index(value) + 1 for value in location_dict}
    item_name_to_id = {value: raw_items.index(value) + 1 for value in raw_items}
    topology_present = True
    ut_can_gen_without_yaml = True
    gen_puml = False

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.location_count = 0

    def generate_early(self):
        options = self.options
        # Universal Tracker sets re_gen_passthrough; apply it before validate_option_errors / check_options.
        # Vanilla gen never has this attribute, so duplicate main+secondary still errors below.
        if getattr(self.multiworld, "re_gen_passthrough", None) is not None:
            if "Atlyss" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Atlyss"]
                if "goal" in passthrough:
                    options.goal = Goal(passthrough["goal"])

                if "random_portals" in passthrough:
                    options.random_portals = RandomPortals(passthrough["random_portals"])

                if "shop_sanity" in passthrough:
                    options.shop_sanity = ShopSanity(passthrough["shop_sanity"])

                if "achievements" in passthrough:
                    options.achievements = Achievements(passthrough["achievements"])

                if "main_class" in passthrough:
                    options.main_class = MainClass(passthrough["main_class"])

                if "secondary_class" in passthrough:
                    options.secondary_class = SecondaryClass(passthrough["secondary_class"])

                if "experience_multiplier" in passthrough:
                    options.experience_multiplier = ExperienceMultiplier(passthrough["experience_multiplier"])

            # UT defaults (and YAML slot edge cases) can leave main == secondary; SecondaryClass.option_none = 3.
            if options.main_class.value == options.secondary_class.value:
                options.secondary_class = SecondaryClass(3)

        check_options(self)

    def create_regions(self):
        gen_create_regions(self)

    def create_item(self, name: str):
        return Item(name, item_table[name], self.item_name_to_id[name], self.player)

    def create_items(self):
        gen_create_items(self)

    def set_rules(self):
        player = self.player
        options = self.options
        match options.goal:
            case 0:  # silme_diva
                self.multiworld.completion_condition[self.player] = lambda state: can_beat_enemy(state, player,
                                                                                                 'Slime Diva')
            case 1:  # lord_zuulneruda
                self.multiworld.completion_condition[self.player] = lambda state: can_beat_enemy(state, player,
                                                                                                 'Lord Zuulneruda')
            case 2:  # colossus
                self.multiworld.completion_condition[self.player] = lambda state: can_beat_enemy(state, player,
                                                                                                 'Colossus')
            case 3:  # galius
                self.multiworld.completion_condition[self.player] = lambda state: can_beat_enemy(state, player,
                                                                                                 'Galius')
            case 4:  # lord_kaluuz
                self.multiworld.completion_condition[self.player] = lambda state: can_beat_enemy(state, player,
                                                                                                 'Lord Kaluuz')
            case 5:  # valdur
                self.multiworld.completion_condition[self.player] = lambda state: can_beat_enemy(state, player,
                                                                                                 'Valdur')
            case 6:  # all_bosses
                self.multiworld.completion_condition[self.player] = lambda state: can_beat_enemy(state, player,
                                                                                                 "Slime Diva") and can_beat_enemy(
                    state, player, "Lord Zuulneruda") and can_beat_enemy(state, player,
                                                                         "Lord Kaluuz") and can_beat_enemy(state,
                                                                                                           player,
                                                                                                           "Colossus") and can_beat_enemy(
                    state, player, "Valdur") and can_beat_enemy(state, player, "Galius")
            case 7:  # all_quests
                self.multiworld.completion_condition[self.player] = lambda state: has_quest(state, player,
                                                                                            "The Glyphik Booklet") and has_quest(
                    state, player, "Cleaning Terrace") and has_quest(state, player, "Ancient Beings") and has_quest(
                    state, player, "Wicked Wizboars") and has_quest(state, player,
                                                                    "Spiraling In The Grove") and has_quest(state,
                                                                                                            player,
                                                                                                            "Hell In The Grove") and has_quest(
                    state, player, "Nulversa Magica") and has_quest(state, player, "Night Spirits") and has_quest(state,
                                                                                                                  player,
                                                                                                                  "Ridding Slimes") and has_quest(
                    state, player, "Huntin' Hogs") and has_quest(state, player, "Purging the Grove") and has_quest(
                    state, player, "Cleansing the Grove") and has_quest(state, player,
                                                                        "Nulversa Viscera") and has_quest(state, player,
                                                                                                          "Call of Fury") and has_quest(
                    state, player, "Mastery of Strength") and has_quest(state, player, "Beckoning Foes") and has_quest(
                    state, player, "Summore' Spectral Powder!") and has_quest(state, player,
                                                                              "Makin' More Mekspears") and has_quest(
                    state, player, "Makin' More Wizwands") and has_quest(state, player,
                                                                         "Makin' More Vile Blades") and has_quest(state,
                                                                                                                  player,
                                                                                                                  "Summore' Golem Chestpieces") and has_quest(
                    state, player, "Makin' More Ragespears") and has_quest(state, player,
                                                                           "Summore' Monolith Chestpieces") and has_quest(
                    state, player, "Nulversa, Greenversa!") and has_quest(state, player,
                                                                          "Summore' Firebreath Blades") and has_quest(
                    state, player, "Makin' More Follycannons") and has_quest(state, player,
                                                                             "Focusin' in") and has_quest(state, player,
                                                                                                          "Mastery of Dexterity") and has_quest(
                    state, player, "Whatta' Rush!") and has_quest(state, player, "Purging the Undead") and has_quest(
                    state, player, "Rattlecage Rage") and has_quest(state, player, "Consumed Madness") and has_quest(
                    state, player, "Eradicating the Undead") and has_quest(state, player,
                                                                           "Reviling more Rageboars") and has_quest(
                    state, player, "Facing Foes") and has_quest(state, player, "The Gall of Galius") and has_quest(
                    state, player, "Sapphite Ingots")
            case 8:  # level_32
                self.multiworld.completion_condition[self.player] = lambda state: can_grind_level(state, player, 32)

    def fill_slot_data(self):
        slot_data = {
            "goal": int(self.options.goal),
            "random_portals": bool(self.options.random_portals),
            "shop_sanity": bool(self.options.shop_sanity),
            "achievements": bool(self.options.achievements),
            "main_class": int(self.options.main_class),
            "secondary_class": int(self.options.secondary_class),
            "experience_multiplier": int(self.options.experience_multiplier)
        }
        return slot_data

    def generate_output(self, output_directory: str):
        if self.gen_puml:
            from Utils import visualize_regions
            state = self.multiworld.get_all_state(False)
            state.update_reachable_regions(self.player)
            visualize_regions(self.get_region("Menu"), f"{self.player_name}_world.puml",
                              show_entrance_names=True,
                              regions_to_highlight=state.reachable_regions[self.player])