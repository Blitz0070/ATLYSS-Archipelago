from BaseClasses import ItemClassification
from .Locations import *
from .Options import *
from .ProgressionLogic import (
    compute_tier_budgets,
    count_junk_locations,
    tier_selection_would_overflow,
)
from .ItemTiers import get_item_tier
from .ItemClassAffinity import item_passes_class_filter
from .ProfessionToolData import PROFESSION_TOOL_BUYS

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

any_progressives = {
	"Progressive Any Weapon": 5,
	"Progressive Any Helmet": 6,
	"Progressive Any Cape": 5,
	"Progressive Any Chest Piece": 5,
	"Progressive Any Leggings": 5,
	"Progressive Any Trinket": 6
}

fighter_progressives = {
	"Progressive Fighter Weapon": 6,
	"Progressive Fighter Chest Piece": 3,
	"Progressive Fighter Leggings": 3
}

mystic_progressives = {
	"Progressive Mystic Weapon": 5,
	"Progressive Mystic Helmet": 1,
	"Progressive Mystic Chest Piece": 3,
	"Progressive Mystic Leggings": 2
}

bandit_progressives = {
	"Progressive Bandit Weapon": 6,
	"Progressive Bandit Chest Piece": 3,
	"Progressive Bandit Leggings": 3
}

CLASS_FILTER_CLASSES = {
	0: {"fighter", "mystic", "bandit"},
	1: {"fighter"},
	2: {"mystic"},
	3: {"bandit"},
	4: {"fighter", "mystic"},
	5: {"fighter", "bandit"},
	6: {"mystic", "bandit"},
}

item_counts_useful = {
	"Tome of Naivety": 2,
	"Tome of Unlearning": 2,
	"Agility Stone": 1,
	"Angela's Tear": 1,
	"Flux Stone": 1,
	"Might Stone": 1,
	"Soul Pearl": 1
}

item_counts_filler = {
}

item_counts_progression = {
	"Experience Bond": 1,
	"Illusion Stone": 1,
}

filler_items = [
	"Agility Potion Pack",
	"Agility Vial Pack",
	"Bolster Potion Pack",
	"Bolster Vial Pack",
	"Bunbag Pack",
	"Bunjar Pack",
	"Bunpot Pack",
	"Carrot Cake Pack",
	"Magiclove Pack",
	"Magiflower Pack",
	"Magileaf Pack",
	"Minchroom Juice Pack",
	"Regen Potion Pack",
	"Regen Vial Pack",
	"Spectral Powder Pack",
	"Stamstar",
	"Wisdom Potion Pack",
	"Wisdom Vial Pack",
	"Festive Hat",
	"Fishin Hat",
	"Orefinder Hat",
	"Spooky Hat",
	"Top Hat",
	"Wizard Hat",
	"Bunhost Garb",
	"Festive Coat",
	"Fisher Overalls",
	"Noble Shirt",
	"Orefinder Vest",
	"Ritualist Garb",
	"Silken Top",
	"Spooky Garment",
	"Test Chestpiece",
	"Vampiric Coat",
	"Bunhost Leggings",
	"Festive Trousers",
	"Noble Pants",
	"Orefinder",
	"Ritualist Straps",
	"Silken Loincloth",
	"Test Pants",
	"Vampiric Leggings",
	"Aqua Muchroom Cap",
	"Barknaught Face",
	"Blue Minchroom Cap",
	"Boomboar Gear",
	"Boomboar Head",
	"Boomboar Pouch",
	"Burnrose",
	"Carbuncle Foot",
	"Cursed Note",
	"Deathgel Core",
	"Deathknight Gauntlet",
	"Demigolem Core",
	"Demigolem Gem",
	"Diva Necklace",
	"Firebreath Gland",
	"Fluxfern",
	"Gale Muchroom Cap",
	"Geist Collar",
	"Ghostdust",
	"Golem Core",
	"Golem Gem",
	"Green Lipstick",
	"Hellsludge Core",
	"Maw Eye",
	"Mekboar Head",
	"Mekboar Spear",
	"Monolith Core",
	"Monolith Gem",
	"Mouth Bittertooth",
	"Mouth Eye",
	"Rageboar Head",
	"Rageboar Spear",
	"Red Minchroom Cap",
	"Rock",
	"Slime Core",
	"Slime Diva Ears",
	"Slime Ears",
	"Slimek Core",
	"Slimek Ears",
	"Slimek Eye",
	"Vinethorn",
	"Vout Antennae",
	"Vout Wing",
	"Warboar Axe",
	"Warboar Head",
	"Wizboar Head",
	"Wizboar Scepter",
	"Amberite Ore",
	"Bittering Katfish",
	"Bonefish",
	"Coal",
	"Copper Cluster",
	"Dense Ore",
	"Iron Cluster",
	"Mithril Cluster",
	"Old Boot",
	"Sapphite Ore",
	"Smiling Wrellfish",
	"Squangfish",
	"Sugeel",
	"Sugshrimp",
	"Windtail Fish",
	"Crowns (Small)",
	"Crowns (Medium)",
	"Crowns (Large)",
	"Crowns (Huge)"
]

useful_items = [
	"Tome of Experience",
	"Tome of Greater Experience",
	"Tome of Lesser Experience",
	"Tome of Naivety",
	"Tome of Unlearning",
	"Amberite Ingot",
	"Dense Ingot",
	"Sapphite Ingot",
	"Starlight Gem",
	"Big Wan",
	"Coldgeist Badge",
	"Earthcore Badge",
	"Geistlord Badge",
	"Windcore Badge",
	"Crypt Blade",
	"Femur Club",
	"Ironbark Sword",
	"Slimecrust Blade",
	"Gilded Sword",
	"Splitbark Club",
	"Demicrypt Blade",
	"Dense Mace",
	"Iron Sword",
	"Dawn Mace",
	"Rude Blade",
	"Vile Blade",
	"Amberite Sword",
	"Nethercrypt Blade",
	"Coldgeist Blade",
	"Mithril Sword",
	"Serrated Blade",
	"Nulrok Mace",
	"Firebreath Blade",
	"Valdur Blade",
	"Fier Blade",
	"Slimek Axehammer",
	"Dense Hammer",
	"Iron Axehammer",
	"Crypt Pounder",
	"Quake Pummeler",
	"Mini Geist Scythe",
	"Geist Scythe",
	"Stone Greatblade",
	"Amberite Warstar",
	"Dolkin's Axe",
	"Poltergeist Scythe",
	"Coldgeist Punisher",
	"Mithril Greatsword",
	"Deathknight Runeblade",
	"Ryzer Greataxe",
	"Dense Spear",
	"Iron Spear",
	"Cryptsinge Halberd",
	"Mekspear",
	"Amberite Halberd",
	"Necroroyal Halberd",
	"Sinner Bardiche",
	"Mithril Halberd",
	"Ragespear",
	"Serrated Spear",
	"Sapphite Spear",
	"Nulrok Spear",
	"Cryotribe Spear",
	"Flametribe Spear",
	"Marrow Bauble",
	"Splitbark Scepter",
	"Demicrypt Bauble",
	"Iron Scepter",
	"Cryo Cane",
	"Slime Diva Baton",
	"Pyre Cane",
	"Wizwand",
	"Nethercrypt Bauble",
	"Aquapetal Staff",
	"Flamepetal Staff",
	"Mithril Scepter",
	"Sapphite Scepter",
	"Voalstark Wand",
	"Cryptcall Bell",
	"Iron Bell",
	"Coldgeist Frostcaller",
	"Mithril Bell",
	"Colossus Tone",
	"Sapphite Bell",
	"Slimecrust Katars",
	"Cryptsinge Katars",
	"Slimek Shivs",
	"Deathgel Shivs",
	"Dense Katars",
	"Iron Katars",
	"Runic Katars",
	"Geistlord Claws",
	"Hellsludge Shivs",
	"Mithril Katars",
	"Frostbite Claws",
	"Serrated Knuckles",
	"Rummok Bladerings",
	"Sapphite Katars",
	"Golemfist Katars",
	"Crypt Bow",
	"Demicrypt Bow",
	"Iron Bow",
	"Mekspike Bow",
	"Menace Bow",
	"Petrified Bow",
	"Mithril Bow",
	"Necroroyal Bow",
	"Coldgeist Bow",
	"Serrated Longbow",
	"Torrentius Longbow",
	"Amberite Boomstick",
	"Magitek Burstgun",
	"Follycannon",
	"Agility Ears",
	"Leather Cap",
	"Newfold Halo",
	"Acolyte Hood",
	"Cryptsinge Halo",
	"Initiate Spectacles",
	"Demicrypt Halo",
	"Dense Helm",
	"Diva Crown",
	"Iron Halo",
	"Necromancer Hood",
	"Geistlord Crown",
	"Journeyman Spectacles",
	"Amberite Helm",
	"Focus Circlet",
	"Magistrate Circlet",
	"Rage Circlet",
	"Focusi Glasses",
	"Nethercrypt Halo",
	"Carbuncle Hat",
	"Geistlord Eye",
	"Glyphgrift Halo",
	"Jestercast Memory",
	"Knightguard Halo",
	"Mithril Halo",
	"Sapphite Mindhat",
	"Dire Helm",
	"Druidic Halo",
	"Guardel Helm",
	"Leathen Cap",
	"Boarus Helm",
	"Deathknight Helm",
	"Emerock Halo",
	"Wizlad Hood",
	"Boarus Torment",
	"Initiate Cloak",
	"Slimewoven Cloak",
	"Nokket Cloak",
	"Rugged Cloak",
	"Regazuul Cape",
	"Flux Cloak",
	"Cozy Cloak",
	"Nethercrypt Cloak",
	"Cobblerage Cloak",
	"Deathward Cape",
	"Forlorn Cloak",
	"Meshlink Cape",
	"Sagecaller Cape",
	"Roudon Cape",
	"Blueversa Cape",
	"Greenversa Cape",
	"Nulversa Cape",
	"Redversa Cape",
	"Windgolem Cloak",
	"Mekwar Drape",
	"Aero Top",
	"Leather Top",
	"Necro Marrow",
	"Nutso Top",
	"Sagecloth Top",
	"Ghostly Tabard",
	"Poacher Cloth",
	"Ragged Shirt",
	"Slimecrust Chest",
	"Worn Robe",
	"Cryptsinge Chest",
	"Journeyman Vest",
	"Slimek Chest",
	"Dense Chestpiece",
	"Trodd Tunic",
	"Iron Chestpiece",
	"Tattered Battlerobe",
	"Apprentice Robe",
	"Duelist Garb",
	"Skywrill Tabard",
	"Sleeper's Robe",
	"Warrior Chest",
	"Amberite Breastplate",
	"Golem Chestpiece",
	"Lord Breastplate",
	"Nethercrypt Tabard",
	"Reapsow Garb",
	"Witchlock Robe",
	"Chainmail Guard",
	"Ornamented Battlerobe",
	"Carbuncle Robe",
	"Chainscale Chest",
	"Gemveil Raiment",
	"King Breastplate",
	"Mercenary Vestment",
	"Mithril Chestpiece",
	"Reaper Gi",
	"Witchwizard Robe",
	"Berserker Chestpiece",
	"Fuguefall Duster",
	"Magilord Overalls",
	"Monolith Chestpiece",
	"Sapphite Guard",
	"Druidic Robe",
	"Emerock Chestpiece",
	"Fortified Chestpiece",
	"Roudon Chestpiece",
	"Earthbind Tabard",
	"Gemveil Breastplate",
	"Roudon Robe",
	"Ruggrok Vest",
	"Executioner Vestment",
	"Fender Garb",
	"Wizlad Robe",
	"Aero Pants",
	"Leather Britches",
	"Necro Caustics",
	"Nutso Pants",
	"Sagecloth Shorts",
	"Ghostly Legwraps",
	"Journeyman Shorts",
	"Slimecrust Leggings",
	"Journeyman Leggings",
	"Slimek Leggings",
	"Dense Leggings",
	"Sash Leggings",
	"Warrior Leggings",
	"Amberite Leggings",
	"Chainmail Leggings",
	"Darkcloth Pants",
	"Lord Greaves",
	"Reapsow Pants",
	"Witchlock Loincloth",
	"King Greaves",
	"Mercenary Leggings",
	"Reaper Leggings",
	"Stridebond Pants",
	"Witchwizard Garterbelt",
	"Berserker Leggings",
	"Fuguefall Pants",
	"Magilord Boots",
	"Sapphite Leggings",
	"Jadewail Trousers",
	"Temrak Britches",
	"Eschek Greaves",
	"Gemveil Leggings",
	"Executioner Leggings",
	"Fender Leggings",
	"Crypt Buckler",
	"Slimek Shield",
	"Demicrypt Buckler",
	"Dense Shield",
	"Iron Shield",
	"Iris Shield",
	"Omen Shield",
	"Amberite Shield",
	"Slabton Shield",
	"Mithril Shield",
	"Nethercrypt Shield",
	"Rustweary Shield",
	"Rustwise Shield",
	"Sapphite Shield",
	"Rigor Buckler",
	"Daemon Shield",
	"Irisun Shield",
	"Old Ring",
	"Ring Of Ambition",
	"Test Ring",
	"Nograd's Amulet",
	"The One Ring",
	"Ambersquire Ring",
	"Emeraldfocus Ring",
	"Sapphireweave Ring",
	"Edon's Pendant",
	"Geistlord Ring",
	"Students Ring",
	"Pearlpond Ring",
	"Slitherwraith Ring",
	"Geistlord Band",
	"Jadetrout Ring",
	"Orbos Ring",
	"Valor Ring",
	"Earthwoken Ring",
	"Noji Talisman",
	"Valdur Effigy",
	"Glyphik Booklet",
	"Tessellated Drive",
	"Agility Stone",
	"Angela's Tear",
	"Flux Stone",
	"Might Stone",
	"Soul Pearl"
]

progression_items = [
	"Experience Bond",
	"Illusion Stone",
	"Fishing Rod",
	"Pickaxe",
]

filler_weights = {
	"Agility Potion Pack": 1,
	"Agility Vial Pack": 1,
	"Bolster Potion Pack": 1,
	"Bolster Vial Pack": 1,
	"Bunbag Pack": 1,
	"Bunjar Pack": 1,
	"Bunpot Pack": 1,
	"Carrot Cake Pack": 1,
	"Magiclove Pack": 1,
	"Magiflower Pack": 1,
	"Magileaf Pack": 1,
	"Minchroom Juice Pack": 1,
	"Regen Potion Pack": 1,
	"Regen Vial Pack": 1,
	"Spectral Powder Pack": 1,
	"Stamstar": 1,
	"Tome of Experience": 2,
	"Tome of Greater Experience": 2,
	"Tome of Lesser Experience": 2,
	"Wisdom Potion Pack": 1,
	"Wisdom Vial Pack": 1,
	"Amberite Ingot": 2,
	"Dense Ingot": 2,
	"Sapphite Ingot": 2,
	"Starlight Gem": 2,
	"Big Wan": 2,
	"Coldgeist Badge": 2,
	"Earthcore Badge": 2,
	"Geistlord Badge": 2,
	"Windcore Badge": 2,
	"Crowns (Small)": 20,
	"Crowns (Medium)": 14,
	"Crowns (Large)": 8,
	"Crowns (Huge)": 4
}

portals = [
	"Outer Sanctum Portal",
	"Arcwood Pass Portal",
	"Effold Terrace Portal",
	"Tuul Valley Portal",
	"Sanctum Catacombs lvl 1 Portal",
	"Sanctum Catacombs lvl 2 Portal",
	"Sanctum Catacombs lvl 3 Portal",
	"Cresent Road Portal",
	"Tuul Enclave Portal",
	"Luvora Garden Portal",
	"Cresent Keep Portal",
	"Bularr Fortress Portal",
	"Cresent Grove lvl 1 Portal",
	"Cresent Grove lvl 2 Portal",
]

item_table = {
	**{item: ItemClassification.useful for item in any_progressives},
	**{item: ItemClassification.useful for item in fighter_progressives},
	**{item: ItemClassification.useful for item in mystic_progressives},
	**{item: ItemClassification.useful for item in bandit_progressives},
	**{item: ItemClassification.filler for item in filler_items},
	**{item: ItemClassification.useful for item in useful_items},
	**{item: ItemClassification.progression for item in progression_items},
	**{item: ItemClassification.progression for item in portals},
	"Progressive Portal": ItemClassification.progression
}

raw_items = [item for item, classification in item_table.items()]

def _is_filler_item_name(name: str) -> bool:
	return item_table[name] == ItemClassification.filler


def _class_filter_allows_progressive(filter_value: int, class_name: str) -> bool:
	return class_name in CLASS_FILTER_CLASSES.get(filter_value, CLASS_FILTER_CLASSES[0])


def _balance_gated_pool(world, pool, max_non_filler: int, junk_count: int,
                        filler_names, filler_weightings, random) -> None:
	"""Ensure junk slots can receive filler and cap optional useful items."""
	player = world.player
	replaceable = [
		i for i in pool
		if i.player == player
		and i.classification not in (ItemClassification.progression, ItemClassification.filler)
	]

	def filler_count() -> int:
		return sum(
			1 for i in pool
			if i.player == player and i.classification == ItemClassification.filler
		)

	while len(replaceable) > max_non_filler or filler_count() < junk_count:
		if not replaceable:
			break
		item = replaceable.pop()
		idx = pool.index(item)
		pool[idx] = world.create_item(random.choices(filler_names, filler_weightings)[0])


def gen_create_items(world):
	pool = world.multiworld.itempool
	options = world.options
	random = world.random
	gated = options.equipment_progression.value == 0
	class_filter = options.class_filter.value
	total_locations = world.location_count
	junk_count = count_junk_locations(world) if gated else 0
	max_non_filler = total_locations - junk_count if gated else total_locations
	non_filler_count = 0

	def _append_item(name: str, *, required: bool = False) -> None:
		nonlocal non_filler_count
		if not required and world.location_count <= 0:
			return
		is_filler = _is_filler_item_name(name)
		if gated and not is_filler and not required and non_filler_count >= max_non_filler:
			return
		pool.append(world.create_item(name))
		world.location_count -= 1
		if not is_filler:
			non_filler_count += 1

	filler_item_names = [key for key, value in filler_weights.items()]
	filler_weightings = [value for key, value in filler_weights.items()]

	if gated:
		for item, amt in any_progressives.items():
			for _ in range(amt):
				_append_item(item, required=True)
		class_progressive_pools = (
			("fighter", fighter_progressives),
			("mystic", mystic_progressives),
			("bandit", bandit_progressives),
		)
		for class_name, class_pool in class_progressive_pools:
			if not _class_filter_allows_progressive(class_filter, class_name):
				continue
			for item, amt in class_pool.items():
				for _ in range(amt):
					_append_item(item, required=True)
	for item, amt in item_counts_useful.items():
		for _ in range(amt):
			_append_item(item)
	for item, amt in item_counts_filler.items():
		for _ in range(amt):
			_append_item(item)
	for item, amt in item_counts_progression.items():
		for _ in range(amt):
			_append_item(item, required=True)
	if options.profession_tools.value == 1:
		for _location_name, item_name in PROFESSION_TOOL_BUYS:
			_append_item(item_name, required=True)
	if options.random_portals:
		for item in portals:
			_append_item(item, required=True)
	else:
		for _ in range(14):
			_append_item("Progressive Portal", required=True)

	if gated and world.location_count > 0:
		tier_budgets = compute_tier_budgets(world)
		tier_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
		candidates = list(useful_items)
		random.shuffle(candidates)
		for item_name in candidates:
			if world.location_count <= 0 or non_filler_count >= max_non_filler:
				break
			if not item_passes_class_filter(class_filter, item_name):
				continue
			tier = get_item_tier(item_name)
			if tier is not None and tier_selection_would_overflow(tier, tier_counts, tier_budgets):
				continue
			if tier is not None:
				tier_counts[tier] += 1
			_append_item(item_name)
	elif world.location_count > 0:
		candidates = [
			item_name for item_name in useful_items
			if get_item_tier(item_name) is not None
			and item_passes_class_filter(class_filter, item_name)
		]
		random.shuffle(candidates)
		for item_name in candidates:
			if world.location_count <= 0:
				break
			_append_item(item_name)

	if gated:
		_balance_gated_pool(world, pool, max_non_filler, junk_count, filler_item_names, filler_weightings, random)

	for _ in range(world.location_count):
		pool.append(world.create_item(random.choices(filler_item_names, filler_weightings)[0]))