# Atlyss Setup Guide

## Requirements

* **Archipelago 0.6.5 or later** — [releases](https://github.com/ArchipelagoMW/Archipelago/releases)
* **ATLYSS** (Steam) with **BepInEx 5.4+**
* **Atlyss Archipelago** mod (BepInEx plugin) and this world's **`atlyss.apworld`**

## Install Archipelago and the world

1. Install Archipelago from the official release page.
2. Copy **`atlyss.apworld`** into your Archipelago install folder under **`custom_worlds/`**.
3. When hosting or playing on WebHost, select game **Atlyss** and configure your slot.

## Install the game mod

### Manual

1. Install [BepInEx](https://docs.bepinex.dev/) for ATLYSS and run the game once so folders are
   created.
2. Place **AtlyssArchipelagoWIP.dll** (release build) in
   `ATLYSS/BepInEx/plugins/` (or the Thunderstore mod folder if you use that layout).
3. Launch the game modded at least once before connecting.

### r2modman (recommended)

1. Install [r2modman](https://thunderstore.io/package/ebkr/r2modman/) and create an **ATLYSS**
   profile pointed at your game folder.
2. Install **AtlyssArchipelago** (and **BepInExPack** if prompted) from Thunderstore.
3. If Thunderstore lags behind GitHub, replace the profile's plugin DLL with the latest release
   from the project's GitHub page.
4. Use **Start modded** to launch.

Archipelago itself is **not** installed through r2modman — add the `.apworld` separately as above.

## Configuring your YAML file

### What is a YAML and why do I need one?

See the [basic multiworld setup guide](/tutorial/Archipelago/setup/en) on the Archipelago site for
how YAML files work.

### Where do I get a YAML?

Use the [Atlyss player options page](/games/Atlyss/player-options) to build a YAML in the browser,
or edit a template by hand. Set `game: Atlyss` and your slot name under the `Atlyss:` section.

Important options to review:

* **goal** — what counts as a win.
* **random_portals** — progressive portal lines vs per-area portal items.
* **shop_sanity** — shops send checks when enabled.
* **achievements** — include achievement locations (on by default).
* **equipment_progression** — gated tier logic vs unrestricted gear.
* **class_filter** — limit class gear in the pool.
* **profession_tools** — static tools on checks vs tools in the multiworld pool.
* **experience_multiplier** / **crown_multiplier** — in-game scaling from the mod.

Upload the generated YAML when joining a multiworld on WebHost or place it in your player config
folder for local play.

## Joining an Archipelago session

### Before you connect

1. Launch ATLYSS **modded**.
2. Open **Settings → Archipelago** and enter:
   * **Server** — hostname or `host:port` (e.g. `archipelago.gg:38281`).
   * **Slot** — must match your YAML slot name.
   * **Password** — room password if required (not saved to disk by the mod; re-enter each session).
3. Load a character: **Singleplayer → Create / Select Character**. Connection is blocked on the
   main menu without a loaded save.

### Connect

Press **F5** (default) to connect after your character is in the world. Chat will confirm the link
and show your goal. If the socket drops, press **F5** again to reconnect; quest and level progress
from your save are polled again for missed checks.

### Gameplay tips

* Pick up items from **Spike's storage** after receiving AP gear.
* Portal items unlock regions on the world map; watch chat for unlock messages.
* With **Shop Sanity**, buying certain shop lines sends location checks — plan crown income
  accordingly.
* Use in-game AP chat for hints and `/help` for client commands supported by your server.

### Optional: text client

You can also run the Archipelago **text client** from your Archipelago install for chat and
commands alongside the game. See the
[commands guide](/tutorial/Archipelago/commands/en).

## Troubleshooting

* **"Load a character first"** — create or select a character, then press F5.
* **Login failed** — verify slot name, password, server address, and that the room generated with
  game **Atlyss**.
* **No items or checks** — confirm BepInEx loaded the plugin (check `BepInEx/LogOutput.log` for
  `[AtlyssAP]` lines).
* **Wrong Archipelago version** — this world requires **0.6.5+**; update Archipelago and the
  `.apworld` from the latest release.
