from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Toggle


# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

class Goal(Choice):
    """
	What is required to complete the game.
	Slime Diva: Defeat the Slime Diva boss (level 10).
	Lord Zuulneruda: Defeat Lord Zuulneruda in the Catacombs (level 12).
	Colossus: Defeat the Colossus in Crescent Grove (level 20).
	Galius: Defeat Galius in Bularr Fortress (level 26) - DEFAULT.
	Lord Kaluuz: Defeat Lord Kaluuz in Catacombs Floor 3 (level 18).
	Valdur: Defeat Valdur the dragon (level 25+).
	All Bosses: Defeat all 6 major bosses.
	All Quests: Complete every quest in the game.
	Level 32: Reach the maximum level.
	"""
    display_name = "Goal"
    option_slime_diva = 0
    option_lord_zuulneruda = 1
    option_colossus = 2
    option_galius = 3
    option_lord_kaluuz = 4
    option_valdur = 5
    option_all_bosses = 6
    option_all_quests = 7
    option_level_32 = 8
    default = 0


class RandomPortals(Toggle):
    """
	How area portals are unlocked.
	Off (default): Progressive Portals - find "Progressive Sanctum Portal" and
	"Progressive Tuul Portal" items (two lines). Sanctum line unlocks most areas;
	Tuul line unlocks Tuul Valley, Tuul Enclave, and Bularr Fortress.
	On: Random Portals - find individual portal items (e.g. "Outer Sanctum Portal",
	"Sanctum Catacombs lvl 1 Portal", etc.) to unlock specific areas and dungeon floors independently.
	"""
    display_name = "Random Portals"


class ShopSanity(DefaultOnToggle):
    """
	Whether shop items can contain Archipelago items from other worlds.
	When enabled, buying items from shops sends checks to other players.
	"""
    display_name = "Shop Sanity"


class Achievements(DefaultOnToggle):
    """
	Whether in-game achievements are tracked as Archipelago locations.
	When enabled (default), unlocking achievements such as 'A New Journey',
	'Trout Master', 'Skill Student', dungeon clears, 'Altered Vision',
	'Rude!', etc. sends checks to other players (up to 12 locations with
	goal trim; more without early goals).
	When disabled, no achievement locations are placed in this slot and the
	mod will not send their checks during play; pick this for a shorter or
	more boss/quest-focused run.
    """
    display_name = "Achievements"


class ClassFilter(Choice):
    """
	Filter equipment pool by class (progressive class gear and non-progressive
	weapons/armor affinity).
	All Classes: no filter. Single/dual class: only matching class gear.
	Universal trinkets, consumables, and "Progressive Any" items are never filtered.
    """
    display_name = "Class Filter"
    option_all_classes = 0
    option_fighter = 1
    option_mystic = 2
    option_bandit = 3
    option_fighter_mystic = 4
    option_fighter_bandit = 5
    option_mystic_bandit = 6
    default = 0


class EquipmentProgression(Choice):
    """
	How equipment is distributed.
	Gated: progressive equipment is in the pool and gear placement follows
	level/tier logic.
	Unrestricted: progressive equipment is removed; individual gear pieces are
	randomized directly and can appear on any check.
    """
    display_name = "Equipment Progression"
    option_gated = 0
    option_unrestricted = 1
    default = 1


class ProfessionTools(Choice):
    """
    First Fishing Rod / Pickaxe purchase at any merchant sends one global check each.
    Static: those checks hold the real tools. Pool: first purchase sends the check and a
    multiworld item instead of the vanilla tool (later buys at any shop are normal).
    """
    display_name = "Profession Tools"
    option_static = 0
    option_pool = 1
    default = 0


class ExperienceMultiplier(Choice):
    """
	How fast you gain experience in-game (Atlyss mod).
	Scales XP from killing creeps and completing quests only (not XP tomes).
	Does not change crown income or shop prices. Higher XP still helps you reach
	Reach Level checks sooner.
	Same tiers as Crown Multiplier (x8 / x4 / x2 / x1 / x0.75 / x0.5).
	"""
    display_name = "Experience Multiplier"
    option_x8_0 = 0
    option_x4_0 = 1
    option_x2_0 = 2
    option_x1_0 = 3
    option_x0_75 = 4
    option_x0_5 = 5
    default = 3


class CrownMultiplier(Choice):
    """
	Crown income scaled in the Atlyss mod: creep coin drops and quest crown rewards.
	Shop resells and Archipelago crown items are not scaled.
	Same tiers as Experience Multiplier (x8 / x4 / x2 / x1 / x0.75 / x0.5).
	"""
    display_name = "Crown Multiplier"
    option_x8_0 = 0
    option_x4_0 = 1
    option_x2_0 = 2
    option_x1_0 = 3
    option_x0_75 = 4
    option_x0_5 = 5
    default = 3


@dataclass
class AtlyssOptions(PerGameCommonOptions):
    goal: Goal
    random_portals: RandomPortals
    shop_sanity: ShopSanity
    achievements: Achievements
    equipment_progression: EquipmentProgression
    profession_tools: ProfessionTools
    class_filter: ClassFilter
    experience_multiplier: ExperienceMultiplier
    crown_multiplier: CrownMultiplier


atlyss_option_groups = [
    OptionGroup("Goal & Checks", [
        Goal,
        Achievements,
    ]),
    OptionGroup("World Access", [
        RandomPortals,
        ShopSanity,
    ]),
    OptionGroup("Item Pool", [
        EquipmentProgression,
        ClassFilter,
        ProfessionTools,
    ]),
    OptionGroup("Gameplay Modifiers", [
        ExperienceMultiplier,
        CrownMultiplier,
    ]),
]
