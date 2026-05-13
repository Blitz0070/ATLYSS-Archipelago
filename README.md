# ATLYSS Archipelago

Archipelago randomizer implementation for ATLYSS. Enables multiworld randomizer gameplay with randomizable items, quest and level-based location checks, and configurable progression options.

## Installation

### Manual Installation

1. **Install Archipelago** — Download and install Archipelago 0.5.0 or later from the official Archipelago releases.

2. **Install the world** — Place `atlyss.apworld` in your Archipelago installation folder under `custom_worlds/`.

3. **Install BepInEx** — Download BepInEx 5.4.23.4 and extract it to your ATLYSS game directory. Run the game once to initialize BepInEx.

4. **Install the mod** — Place the DLL files from the `Plugin` folder into `ATLYSS/BepInEx/plugins/`.

5. **Connect in-game** — Launch ATLYSS and go into **Settings** > **Archipelago**, enter your server address, slot name, and password as needed. Go into **Singleplayer** > **Create your Character**, **Select Character** afterwards and press F5 to connect to your Archipelago server.

### Mod Manager (r2modman)

1. **Install r2modman** — Download from [Thunderstore Mod Manager](https://thunderstore.io/package/ebkr/r2modman/) and install it, or use your distro/package manager if you prefer.

2. **Create an ATLYSS profile** — Open r2modman, choose **Select game** → **ATLYSS**, then **Create profile**. Set **Browse** to your ATLYSS install folder (the directory that contains the game executable).

3. **Install dependencies** — In that profile, open **Online** (or **Get mods**), install **AtlyssArchipelago** (should prompt to install BepInExPack, if not, search and install it). Start the game once from **Start modded** so BepInEx can generate its folders.

4. **Install Archipelago and the world** — r2modman does not manage Archipelago. Install Archipelago 0.5.0 or later separately, then add `atlyss.apworld` under `custom_worlds/` under Archipelago's root directory as in [Manual Installation](#manual-installation).

5. **Connect in-game** — Launch ATLYSS via **Start modded**, go into **Settings** > **Archipelago**, enter your server address, slot name, and password as needed. Go into **Singleplayer** > **Create your Character**, **Select Character** afterwards and press F5 to connect to your Archipelago server.

## Configuration

The mod supports several gameplay options configurable through your Archipelago YAML:

**Goal Options:** Level-based progression (4, 8, 16, 24, or 32) or boss defeats (Colossus, Galius, Lord Kaluuz, or Valdur)

**Area Access:** Locked portals requiring items, fully unlocked areas, or progressive unlocking

**Shop Sanity:** Optional randomization of shop inventories

## Credits

This project was made possible with help from:

- AtlyssModdingCentral Discord server
- Mickemoose - Technical assistance and code contributions  
- Catman - Guidance and project support
- Nichologeam - AzraeL's Coding Partner (major help with this project)
- AzraeL0534 - Previous Project Lead and Creator
