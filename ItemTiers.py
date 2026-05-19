"""Equipment metadata for gated fill and class filtering."""
from __future__ import annotations
from typing import Dict, Optional, Tuple

# class group -> item type -> tier -> item names
ITEM_DATA: Dict[str, Dict[str, Dict[int, Tuple[str, ...]]]] = {
    # Universal / no class filter
    'universal': {
        # Helmet
        'helmet': {
            1: ('Acolyte Hood', 'Agility Ears', 'Cryptsinge Halo', 'Leather Cap', 'Newfold Halo', 'Initiate Spectacles'),
            2: ('Demicrypt Halo', 'Dense Helm', 'Diva Crown', 'Geistlord Crown', 'Iron Halo', 'Journeyman Spectacles', 'Necromancer Hood'),
            3: ('Amberite Helm', 'Magistrate Circlet', 'Nethercrypt Halo', 'Rage Circlet'),
            4: ('Carbuncle Hat', 'Geistlord Eye', 'Glyphgrift Halo', 'Jestercast Memory', 'Knightguard Halo', 'Mithril Halo'),
            5: ('Boarus Helm', 'Boarus Torment', 'Deathknight Helm', 'Dire Helm', 'Druidic Halo', 'Emerock Halo', 'Guardel Helm', 'Leathen Cap'),
        },
        # Cape
        'cape': {
            1: ('Initiate Cloak', 'Slimewoven Cloak'),
            2: ('Nokket Cloak', 'Regazuul Cape', 'Rugged Cloak'),
            3: ('Cozy Cloak', 'Flux Cloak', 'Nethercrypt Cloak'),
            4: ('Blueversa Cape', 'Cobblerage Cloak', 'Deathward Cape', 'Forlorn Cloak', 'Greenversa Cape', 'Meshlink Cape', 'Nulversa Cape', 'Redversa Cape', 'Roudon Cape', 'Sagecaller Cape'),
            5: ('Mekwar Drape', 'Windgolem Cloak'),
        },
        # Chest piece
        'chest_piece': {
            1: ('Aero Top', 'Cryptsinge Chest', 'Ghostly Tabard', 'Journeyman Vest', 'Leather Top', 'Necro Marrow', 'Nutso Top', 'Poacher Cloth', 'Ragged Shirt', 'Sagecloth Top', 'Slimecrust Chest', 'Slimek Chest', 'Worn Robe'),
            2: ('Apprentice Robe', 'Dense Chestpiece', 'Duelist Garb', 'Skywrill Tabard', "Sleeper's Robe", 'Tattered Battlerobe', 'Trodd Tunic', 'Iron Chestpiece', 'Warrior Chest'),
            3: ('Amberite Breastplate', 'Chainmail Guard', 'Golem Chestpiece', 'Nethercrypt Tabard', 'Ornamented Battlerobe'),
            4: ('Carbuncle Robe', 'Chainscale Chest', 'Druidic Robe', 'Emerock Chestpiece', 'Fortified Vestment', 'Gemveil Raiment', 'Mercenary Vestment', 'Mithril Chestpiece', 'Monolith Chestpiece', 'Roudon Chestpiece', 'Sapphite Guard'),
            5: ('Earthbind Tabard', 'Gemveil Breastplate', 'Roudon Robe', 'Ruggrok Vest'),
        },
        # Leggings
        'leggings': {
            1: ('Aero Pants', 'Ghostly Legwraps', 'Journeyman Leggings', 'Journeyman Shorts', 'Leather Britches', 'Necro Caustics', 'Nutso Pants', 'Sagecloth Shorts', 'Slimecrust Leggings', 'Slimek Leggings'),
            2: ('Dense Leggings', 'Sash Leggings', 'Warrior Leggings'),
            3: ('Amberite Leggings', 'Chainmail Leggings', 'Darkcloth Pants'),
            4: ('Mercenary Leggings', 'Sapphite Leggings', 'Stridebond Pants', 'Jadewail Trousers', 'Temrak Britches'),
            5: ('Eschek Greaves', 'Gemveil Leggings'),
        },
        # Trinket / ring
        'trinket': {
            1: ("Nograd's Amulet", 'Old Ring', 'Ring Of Ambition', 'The One Ring'),
            2: ('Ambersquire Ring', "Edon's Pendant", 'Emeraldfocus Ring', 'Sapphireweave Ring'),
            3: ('Geistlord Ring', 'Pearlpond Ring', 'Slitherwraith Ring', 'Students Ring'),
            4: ('Earthwoken Ring', 'Geistlord Band', 'Jadetrout Ring', 'Noji Talisman', 'Orbos Ring', 'Valor Ring'),
            5: ('Glyphik Booklet', 'Tessellated Drive', 'Valdur Effigy'),
        },
    },

    # Fighter
    'fighter': {
        # Weapon
        'weapon': {
            1: ('Crypt Blade', 'Femur Club', 'Gilded Sword', 'Ironbark Sword', 'Mini Geist Scythe', 'Slimecrust Blade', 'Slimek Axehammer', 'Splitbark Club'),
            2: ('Crypt Pounder', 'Cryptsinge Halberd', 'Dawn Mace', 'Demicrypt Blade', 'Dense Hammer', 'Dense Mace', 'Dense Spear', 'Geist Scythe', 'Iron Axehammer', 'Iron Spear', 'Iron Sword', 'Mekspear', 'Rude Blade', 'Stone Greatblade', 'Vile Blade'),
            3: ('Amberite Halberd', 'Amberite Sword', 'Amberite Warstar', "Dolkin's Axe", 'Necroroyal Halberd', 'Nethercrypt Blade', 'Poltergeist Scythe', 'Sinner Bardiche'),
            4: ('Coldgeist Blade', 'Coldgeist Punisher', 'Mithril Greatsword', 'Deadwood Axe', 'Mithril Halberd', 'Mithril Sword', 'Nulrok Mace', 'Nulrok Spear', 'Quake Pummeler', 'Ragespear', 'Sapphite Spear', 'Serrated Blade', 'Serrated Spear'),
            5: ('Cryotribe Spear', 'Deathknight Runeblade', 'Fier Blade', 'Firebreath Blade', 'Flametribe Spear', 'Ryzer Greataxe', 'Valdur Blade'),
        },
        # Chest piece
        'chest_piece': {
            3: ('Lord Breastplate',),
            4: ('Berserker Chestpiece', 'King Breastplate'),
            5: ('Executioner Vestment',),
        },
        # Leggings
        'leggings': {
            3: ('Lord Greaves',),
            4: ('Berserker Leggings', 'King Greaves'),
            5: ('Executioner Leggings',),
        },
    },

    # Mystic
    'mystic': {
        # Weapon
        'weapon': {
            1: ('Marrow Bauble', 'Splitbark Scepter'),
            2: ('Cryo Cane', 'Cryptcall Bell', 'Demicrypt Bauble', 'Iron Bell', 'Iron Scepter', 'Slime Diva Baton'),
            3: ('Nethercrypt Bauble', 'Pyre Cane', 'Wizwand'),
            4: ('Aquapetal Staff', 'Coldgeist Frostcaller', 'Colossus Tone', 'Flamepetal Staff', 'Mithril Bell', 'Mithril Scepter', 'Sapphite Bell', 'Sapphite Scepter'),
            5: ('Voalstark Wand',),
        },
        # Helmet
        'helmet': {
            3: ('Focus Circlet', 'Focusi Glasses'),
            4: ('Sapphite Mindhat',),
            5: ('Wizlad Hood',),
        },
        # Chest piece
        'chest_piece': {
            3: ('Witchlock Robe',),
            4: ('Magilord Overalls', 'Witchwizard Robe'),
            5: ('Wizlad Robe',),
        },
        # Leggings
        'leggings': {
            3: ('Witchlock Loincloth',),
            4: ('Magilord Boots', 'Witchwizard Garterbelt'),
        },
    },

    # Bandit
    'bandit': {
        # Weapon
        'weapon': {
            1: ('Crypt Bow', 'Cryptsinge Katars', 'Slimecrust Katars', 'Slimek Shivs'),
            2: ('Deathgel Shivs', 'Demicrypt Bow', 'Dense Katars', 'Iron Bow', 'Iron Katars', 'Mekspike Bow', 'Menace Bow', 'Runic Katars'),
            3: ('Amberite Boomstick', 'Geistlord Claws', 'Hellsludge Shivs', 'Mithril Bow', 'Mithril Katars', 'Necroroyal Bow', 'Petrified Bow'),
            4: ('Frostbite Claws', 'Golemfist Katars', 'Magitek Burstgun', 'Rummok Bladerings', 'Sapphite Katars', 'Serrated Knuckles', 'Coldgeist Bow', 'Serrated Longbow'),
            5: ('Follycannon', 'Torrentius Longbow'),
        },
        # Chest piece
        'chest_piece': {
            3: ('Reapsow Garb',),
            4: ('Fuguefall Duster', 'Reaper Gi'),
            5: ('Fender Garb',),
        },
        # Leggings
        'leggings': {
            3: ('Reapsow Pants',),
            4: ('Fuguefall Pants', 'Reaper Leggings'),
            5: ('Fender Leggings',),
        },
    },

    # Fighter / Mystic
    'fighter_mystic': {
        # Shield
        'shield': {
            1: ('Wooden Shield', 'Crypt Buckler', 'Slimek Shield'),
            2: ('Demicrypt Buckler', 'Dense Shield', 'Iris Shield', 'Iron Shield', 'Omen Shield'),
            3: ('Amberite Shield', 'Mithril Shield', 'Nethercrypt Shield', 'Slabton Shield'),
            4: ('Rigor Buckler', 'Rustweary Shield', 'Rustwise Shield', 'Sapphite Shield'),
            5: ('Daemon Shield', 'Irisun Shield'),
        },
    },
}

ITEM_CLASS_AFFINITY_BY_GROUP: Dict[str, Optional[str]] = {
    'universal': None,
    'fighter': 'F',
    'mystic': 'M',
    'bandit': 'B',
    'fighter_mystic': 'FM',
}

def _build_item_tier() -> Dict[str, int]:
    item_tier: Dict[str, int] = {}
    for class_groups in ITEM_DATA.values():
        for type_groups in class_groups.values():
            for tier, item_names in type_groups.items():
                for item_name in item_names:
                    if item_name in item_tier:
                        raise ValueError(f"Duplicate item tier entry: {item_name}")
                    item_tier[item_name] = tier
    return item_tier


def _build_item_class_affinity() -> Dict[str, str]:
    item_class_affinity: Dict[str, str] = {}
    for class_group, type_groups in ITEM_DATA.items():
        affinity = ITEM_CLASS_AFFINITY_BY_GROUP[class_group]
        if affinity is None:
            continue
        for tier_groups in type_groups.values():
            for item_names in tier_groups.values():
                for item_name in item_names:
                    if item_name in item_class_affinity:
                        raise ValueError(f"Duplicate item affinity entry: {item_name}")
                    item_class_affinity[item_name] = affinity
    return item_class_affinity


ITEM_TIER: Dict[str, int] = _build_item_tier()
ITEM_CLASS_AFFINITY: Dict[str, str] = _build_item_class_affinity()

# Progressive equipment copy tiers used by gated generation.
PROGRESSIVE_ITEM_TIERS: Dict[str, Tuple[int, ...]] = {
    'Progressive Any Cape': (2, 4, 4, 5, 5),
    'Progressive Any Chest Piece': (1, 2, 4, 4, 5),
    'Progressive Any Helmet': (1, 2, 2, 4, 5, 5),
    'Progressive Any Leggings': (1, 2, 3, 4, 5),
    'Progressive Any Trinket': (1, 3, 4, 4, 4, 5),
    'Progressive Any Weapon': (1, 2, 4, 3, 5),
    'Progressive Bandit Chest Piece': (3, 4, 5),
    'Progressive Bandit Leggings': (3, 4, 5),
    'Progressive Bandit Weapon': (1, 2, 3, 4, 5, 5),
    'Progressive Fighter Chest Piece': (3, 4, 5),
    'Progressive Fighter Leggings': (3, 4, 5),
    'Progressive Fighter Weapon': (2, 2, 3, 4, 5, 5),
    'Progressive Mystic Chest Piece': (3, 4, 5),
    'Progressive Mystic Helmet': (5,),
    'Progressive Mystic Leggings': (3, 4),
    'Progressive Mystic Weapon': (2, 2, 4, 4, 5),
}


def get_item_tier(item_name: str) -> Optional[int]:
    return ITEM_TIER.get(item_name)


def get_progressive_item_tiers(item_name: str) -> Optional[Tuple[int, ...]]:
    return PROGRESSIVE_ITEM_TIERS.get(item_name)
