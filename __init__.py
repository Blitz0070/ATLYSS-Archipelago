from worlds.AutoWorld import World
from .Locations import *
from .Rules import *
from .Options import *
from .Items import *
from .Regions import *
from .Settings import *
from .GoalCompletion import apply_completion_condition
from .ProgressionLogic import (
    apply_progression_rules,
    prefill_tiered_equipment,
    rebalance_gated_pool_for_junk_slots,
)
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

                if "profession_tools" in passthrough:
                    from .Options import ProfessionTools as ProfessionToolsOption
                    options.profession_tools = ProfessionToolsOption(passthrough["profession_tools"])

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

    def pre_fill(self):
        prefill_tiered_equipment(self)
        rebalance_gated_pool_for_junk_slots(self)

    def set_rules(self):
        apply_completion_condition(self)
        apply_progression_rules(self)

    def fill_slot_data(self):
        slot_data = {
            "goal": int(self.options.goal),
            "random_portals": bool(self.options.random_portals),
            "shop_sanity": bool(self.options.shop_sanity),
            "achievements": bool(self.options.achievements),
            "equipment_progression": int(self.options.equipment_progression),
            "profession_tools": int(self.options.profession_tools),
            "class_filter": int(self.options.class_filter),
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