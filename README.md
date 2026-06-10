# ATLYSS Archipelago

Archipelago randomizer implementation for ATLYSS. Enables multiworld randomizer gameplay with randomizable items, quest and level-based location checks, and configurable progression options.

## About

This is a **fork** of [AzraeL0534's original Atlyss Archipelago mod and apworld](https://thunderstore.io/c/atlyss/p/AzraeL0534/AtlyssArchipelago/), actively maintained and **still in development** under **blitz0070** (Rule Builder logic, progression options, and ongoing fixes). Expect changes between releases.

The in-game BepInEx client is on Thunderstore as [**AtlyssArchipelago**](https://thunderstore.io/c/atlyss/p/blitz0070/AtlyssArchipelago/) (author **blitz0070**).

## Installation

### Manual Installation

1. **Install Archipelago** — Download and install [Archipelago 0.6.7 or later](https://github.com/ArchipelagoMW/Archipelago/releases) (Rule Builder support required).

2. **Install the world** — Place `atlyss.apworld` in your Archipelago installation folder under `custom_worlds/`.

3. **Install BepInEx** — Download BepInEx 5.4.23.4 and extract it to your ATLYSS game directory. Run the game once to initialize BepInEx.

4. **Install the mod** — Install from the [AtlyssArchipelago Thunderstore listing](https://thunderstore.io/c/atlyss/p/blitz0070/AtlyssArchipelago/), or copy `AtlyssArchipelago.dll` from the latest [GitHub release](https://github.com/Blitz0070/ATLYSS-Archipelago/releases) into `ATLYSS/BepInEx/plugins/`.

5. **Connect in-game** — Launch ATLYSS and go into **Settings** > **Archipelago**, enter your server address, slot name, and password as needed. Go into **Singleplayer** > **Create your Character**, **Select Character** afterwards and press F5 to connect to your Archipelago server.

### Mod Manager (r2modman)

1. **Install r2modman** — Download from [Thunderstore Mod Manager](https://thunderstore.io/package/ebkr/r2modman/) and install it, or use your distro/package manager if you prefer.

2. **Create an ATLYSS profile** — Open r2modman, choose **Select game** → **ATLYSS**, then **Create profile**. Set **Browse** to your ATLYSS install folder (the directory that contains the game executable).

3. **Install dependencies** — In that profile, open **Online**, install [**AtlyssArchipelago**](https://thunderstore.io/c/atlyss/p/blitz0070/AtlyssArchipelago/) (author **blitz0070**). Install **BepInExPack** if prompted. Start the game once from **Start modded** so BepInEx can generate its folders.

4. **Match the GitHub release DLL** — Thunderstore may lag behind GitHub. Download the **AtlyssArchipelago** DLL from the latest release on this project’s GitHub page and paste it over the **AtlyssArchipelago** DLL in your r2modman profile (under the `BepInEx/plugins` path where r2modman installed the mod—replace the existing file).

5. **Install Archipelago and the world** — r2modman does not manage Archipelago. Install Archipelago 0.6.7 or later separately, then add `atlyss.apworld` under `custom_worlds/` as in [Manual Installation](#manual-installation).

6. **Connect in-game** — Launch ATLYSS via **Start modded**, go into **Settings** > **Archipelago**, enter your server address, slot name, and password as needed. Go into **Singleplayer** > **Create your Character**, **Select Character** afterwards and press F5 to connect to your Archipelago server.

## Credits

This project was made possible with help from:

- AtlyssModdingCentral Discord server
- Mickemoose - Technical assistance and code contributions  
- Catman - Guidance and project support
- Nichologeam - Azrael's Coding partner (major help with this project)
- AzraeL0534 - Original project creator
- Maude - Patching up the logic in separate fork
- Blitz0 - Current Project lead and maintainer
- Twilly - Blitz's testing buddy
