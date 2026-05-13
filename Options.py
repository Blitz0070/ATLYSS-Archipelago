from dataclasses import dataclass
from Options import *


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
	Off (default): Progressive Portals - find "Progressive Portal" items to unlock
	areas in a fixed sequence. Each portal found opens the next area in order.
	On: Random Portals - find individual portal items (e.g. "Outer Sanctum Portal",
	"Catacombs Portal") to unlock specific areas independently.
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
	'Rude!', etc. sends checks to other players (12 locations).
	When disabled, no achievement locations are placed in this slot and the
	mod will not send their checks during play; pick this for a shorter or
	more boss/quest-focused run.
    """
    display_name = "Achievements"


class ExperienceMultiplier(Choice):
    """
	Experience gain multiplier applied in the Atlyss mod.
	x8.0: Extremely fast leveling.
	x4.0: Very fast leveling.
	x2.0: Fast leveling.
	x1.0: Vanilla/default leveling.
	x0.75: Slower leveling.
	x0.5: Much slower leveling.
	"""
    display_name = "Experience Multiplier"
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
    experience_multiplier: ExperienceMultiplier