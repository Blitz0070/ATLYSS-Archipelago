from typing import cast

from BaseClasses import CollectionState, Item, ItemClassification, Tutorial
from rule_builder.cached_world import CachedRuleBuilderWorld
from .AtlyssRules.collection_state import AtlyssCollectionState  # noqa: F401 — registers copy_mixin
from worlds.AutoWorld import WebWorld
from .Locations import *
from .Rules import *
from .Options import *
from .presets import atlyss_options_presets
from .Items import *
from .Regions import *
from .Settings import *
from .GoalCompletion import apply_completion_condition
from .ProgressionLogic import (
    apply_progression_rules,
    prefill_tiered_equipment,
    rebalance_gated_pool_for_junk_slots,
)
from typing import ClassVar


# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]


class AtlyssWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to installing the Atlyss Archipelago mod and joining a multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Blitz0", "Nichologeam", "Sterlia", "SW_CreeperKing", "Azrael0534"],
    )]
    game_info_languages = ["en"]
    option_groups = atlyss_option_groups
    options_presets = atlyss_options_presets
    bug_report_page = "https://github.com/Blitz0070/ATLYSS-Archipelago/issues"


class Atlyss(CachedRuleBuilderWorld):
    """Atlyss"""
    game = "Atlyss"
    rule_caching_enabled: ClassVar[bool] = True
    item_mapping: ClassVar[dict[str, str]] = {
        **{name: "Progressive Sanctum Portal" for name in (
            "Outer Sanctum Portal",
            "Arcwood Pass Portal",
            "Sanctum Catacombs lvl 1 Portal",
            "Sanctum Catacombs lvl 2 Portal",
            "Sanctum Catacombs lvl 3 Portal",
            "Effold Terrace Portal",
            "Crescent Road Portal",
            "Luvora Garden Portal",
            "Crescent Keep Portal",
            "Crescent Grove lvl 1 Portal",
            "Crescent Grove lvl 2 Portal",
        )},
        **{name: "Progressive Tuul Portal" for name in (
            "Tuul Valley Portal",
            "Tuul Enclave Portal",
            "Bularr Fortress Portal",
        )},
    }
    web = AtlyssWeb()
    options_dataclass = AtlyssOptions
    options: AtlyssOptions
    settings: ClassVar[AtlyssSettings]
    location_name_to_id = {value: location_dict.index(value) + 1 for value in location_dict}
    item_name_to_id = {value: raw_items.index(value) + 1 for value in raw_items}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    topology_present = True
    ut_can_gen_without_yaml = True
    gen_puml = False
    # External PopTracker pack (ATLYSS-AP-PopTracker). UT uses map JSON + images from pack path.
    tracker_world: ClassVar[dict[str, object]] = {
        "external_pack_key": "atlyss_poptracker_path",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": "locations/locations.json",
    }

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.location_count = 0

    def _invalidate_rule_cache_on_collect(self, state: CollectionState, item: Item) -> None:
        """Drop cached rule results affected by new items (broader than AP False-only)."""
        player_results = cast(
            dict[int, bool],
            state.rule_builder_cache[self.player],  # pyright: ignore[reportAttributeAccessIssue]
        )
        if self.rule_item_dependencies:
            mapped_name = self.item_mapping.get(item.name, "")
            rule_ids = (
                self.rule_item_dependencies[item.name]
                | self.rule_item_dependencies[mapped_name]
            )
            for rule_id in rule_ids:
                player_results.pop(rule_id, None)
        for dep_map in (
            self.rule_region_dependencies,
            self.rule_location_dependencies,
            self.rule_entrance_dependencies,
        ):
            if dep_map:
                for rule_ids in dep_map.values():
                    for rule_id in rule_ids:
                        player_results.pop(rule_id, None)

    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        if not changed or not self.rule_caching_enabled:
            return changed
        player_results = cast(
            dict[int, bool],
            state.rule_builder_cache[self.player],  # pyright: ignore[reportAttributeAccessIssue]
        )
        # Fill / all_state collect many progression items; partial invalidation is unsafe today.
        if item.classification in (
            ItemClassification.progression,
            ItemClassification.useful,
        ):
            player_results.clear()
        else:
            self._invalidate_rule_cache_on_collect(state, item)
        return changed

    def generate_early(self):
        options = self.options
        # Universal Tracker sets re_gen_passthrough before generation.
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

                if "experience_multiplier" in passthrough:
                    options.experience_multiplier = ExperienceMultiplier(passthrough["experience_multiplier"])

                if "crown_multiplier" in passthrough:
                    options.crown_multiplier = CrownMultiplier(passthrough["crown_multiplier"])

                if "profession_tools" in passthrough:
                    from .Options import ProfessionTools as ProfessionToolsOption
                    options.profession_tools = ProfessionToolsOption(passthrough["profession_tools"])

    def create_regions(self):
        gen_create_regions(self)

    def create_item(self, name: str):
        return Item(name, item_table[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        from .Items import pick_filler_item_name
        return pick_filler_item_name(self.random)

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
            "experience_multiplier": int(self.options.experience_multiplier),
            "crown_multiplier": int(self.options.crown_multiplier),
        }
        return slot_data

    def generate_output(self, output_directory: str):
        from .AtlyssRules.export_logic import should_export_logic, write_logic_export

        if should_export_logic(self):
            write_logic_export(self, output_directory)
        if self.gen_puml:
            from Utils import visualize_regions
            state = self.multiworld.get_all_state(False)
            state.update_reachable_regions(self.player)
            visualize_regions(self.get_region("Menu"), f"{self.player_name}_world.puml",
                              show_entrance_names=True,
                              regions_to_highlight=state.reachable_regions[self.player])