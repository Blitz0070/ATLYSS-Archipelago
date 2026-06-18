"""Export resolved access rules as JSON for Universal Tracker / debugging.

Schema (``LOGIC_EXPORT_SCHEMA_VERSION``):

.. code-block:: json

    {
      "schema_version": 1,
      "game": "Atlyss",
      "player": 1,
      "meta": {
        "goal": 0,
        "random_portals": false,
        "shop_sanity": true,
        "equipment_progression": 0,
        "item_mapping": { "Outer Sanctum Portal": "Progressive Sanctum Portal", ... }
      },
      "locations": [
        { "name": "Wicked Wizboars", "region": "Sanctum", "rule": { "rule": "And", ... } }
      ],
      "entrances": [
        {
          "name": "Sanctum -> Outer Sanctum",
          "from_region": "Sanctum",
          "to_region": "Outer Sanctum",
          "rule": { "rule": "...", ... }
        }
      ],
      "completion": { "rule": "Or", ... }
    }

Each ``rule`` field is either:

* A Rule Builder ``to_dict()`` tree (``Has``, ``And``, ``Or``, …), round-trippable via
  ``Atlyss.rule_from_dict``.
* A fallback object ``{"rule": "<qualname>", "text": "<str(rule)>"}`` only when no Atlyss
  template exists. Eval-only wrappers (``CanGrindLevel``, ``CanBeatBoss``, ``RegionTagged``,
  ``HasProgressionItem``, tool gates, …) rebuild via ``_atlyss_rule_template`` → ``to_dict()``.
  Composed builtins (``HasAllCounts.Resolved``, ``And``, ``Or``) recurse; ``QuestCheck`` /
  ``HasPortalGate`` / ``ShopSlotCheck`` round-trip the same way.
* The string ``"<callable>"`` if a legacy lambda remains (should not occur on locations).

UT / external tools should use ``meta`` for option context. ``meta.item_mapping`` maps
concrete portal item names to progressive logical names (display only; access rules use
``Has("Progressive … Portal", count)`` in progressive mode).

Generation writes ``{output_directory}/atlyss_logic_p{player}.json`` when
``should_export_logic(world)`` is true (UT ``re_gen_passthrough`` includes ``"Atlyss"``, or
player setting ``export_logic: true``).
"""
from __future__ import annotations

import json
from typing import Any, TYPE_CHECKING

from rule_builder.rules import And, False_, Has, HasAll, HasAllCounts, Or, Rule, True_

if TYPE_CHECKING:
    from worlds.atlyss import Atlyss

LOGIC_EXPORT_SCHEMA_VERSION = 1

# Representative checks for UT smoke / round-trip tests (stable names).
EXPORT_ANCHOR_LOCATIONS = (
    "Wicked Wizboars",
    "Buy Item #1 from Sally's Nook",
    "Slime Diva",
)

EXPORT_ANCHOR_ENTRANCES = (
    "Sanctum -> Outer Sanctum",
    "Sanctum Catacombs lvl 1 -> Sanctum Catacombs lvl 2",
)


def _atlyss_rule_template(access_rule: Rule.Resolved) -> Rule["Atlyss"] | None:
    """Rebuild unresolved Atlyss rules from thin Resolved wrappers (for export / round-trip)."""
    from worlds.atlyss.AtlyssRules.custom_rules import (
        CanAccessAreaGameplay,
        CanBeatBoss,
        CanGrindLevel,
        CanGrindMineLevel,
        HasPortalGate,
        HasProgressionItem,
        HasQuestComplete,
        QuestCheck,
        RequiresFishingRod,
        RequiresPickaxe,
        ShopSlotCheck,
    )

    name = access_rule.rule_name
    if name == "QuestCheck":
        return QuestCheck(access_rule.quest_name)
    if name == "HasPortalGate":
        return HasPortalGate(access_rule.gate_id)
    if name == "ShopSlotCheck":
        return ShopSlotCheck(access_rule.merchant, access_rule.slot)
    if name == "CanGrindLevel":
        return CanGrindLevel(access_rule.level)
    if name == "CanGrindMineLevel":
        return CanGrindMineLevel(access_rule.level)
    if name == "CanBeatBoss":
        return CanBeatBoss(access_rule.enemy_name)
    if name == "HasProgressionItem":
        return HasProgressionItem(access_rule.item_name, access_rule.count)
    if name == "RequiresFishingRod":
        return RequiresFishingRod()
    if name == "RequiresPickaxe":
        return RequiresPickaxe()
    if name == "HasQuestComplete":
        return HasQuestComplete(access_rule.quest_name)
    if name in ("RegionTagged", "CanAccessAreaGameplay.RegionTagged"):
        return CanAccessAreaGameplay(access_rule.area_name)
    return None


def _resolved_rule_to_dict(access_rule: Rule.Resolved) -> dict[str, Any]:
    to_dict = getattr(access_rule, "to_dict", None)
    if callable(to_dict):
        return to_dict()

    template = _atlyss_rule_template(access_rule)
    if template is not None:
        return template.to_dict()

    if isinstance(access_rule, HasAllCounts.Resolved):
        return HasAllCounts(dict(access_rule.item_counts)).to_dict()
    if isinstance(access_rule, Has.Resolved):
        return Has(access_rule.item_name, access_rule.count).to_dict()
    if isinstance(access_rule, HasAll.Resolved):
        return HasAll(*access_rule.item_names).to_dict()
    if isinstance(access_rule, And.Resolved):
        return {
            "rule": "And",
            "options": [],
            "filtered_resolution": False,
            "children": [_resolved_rule_to_dict(child) for child in access_rule.children],
        }
    if isinstance(access_rule, Or.Resolved):
        return {
            "rule": "Or",
            "options": [],
            "filtered_resolution": False,
            "children": [_resolved_rule_to_dict(child) for child in access_rule.children],
        }
    if access_rule.rule_name == "True_":
        return True_().to_dict()
    if access_rule.rule_name == "False_":
        return False_().to_dict()
    return {
        "rule": access_rule.rule_name,
        "text": str(access_rule),
    }


def _rule_payload(access_rule: object) -> dict[str, Any] | str | None:
    if isinstance(access_rule, Rule.Resolved):
        data = _resolved_rule_to_dict(access_rule)
        if "text" in data:
            return data
        return data
    if callable(access_rule):
        return "<callable>"
    return None


def _meta_payload(world: "Atlyss") -> dict[str, Any]:
    return {
        "goal": int(world.options.goal),
        "random_portals": bool(world.options.random_portals),
        "shop_sanity": bool(world.options.shop_sanity),
        "equipment_progression": int(world.options.equipment_progression),
        "item_mapping": dict(world.item_mapping),
    }


def build_logic_package(world: "Atlyss") -> dict[str, Any]:
    """JSON-serializable logic snapshot for this player."""
    locations: list[dict[str, Any]] = []
    for region in world.multiworld.get_regions(world.player):
        for location in region.locations:
            if location.player != world.player:
                continue
            locations.append({
                "name": location.name,
                "region": region.name,
                "rule": _rule_payload(location.access_rule),
            })

    entrances: list[dict[str, Any]] = []
    for region in world.multiworld.get_regions(world.player):
        for entrance in region.entrances:
            if entrance.player != world.player:
                continue
            target = entrance.connected_region
            entrances.append({
                "name": entrance.name,
                "from_region": region.name,
                "to_region": target.name if target else None,
                "rule": _rule_payload(entrance.access_rule),
            })

    completion = world.multiworld.completion_condition.get(world.player)
    return {
        "schema_version": LOGIC_EXPORT_SCHEMA_VERSION,
        "game": world.game,
        "player": world.player,
        "meta": _meta_payload(world),
        "locations": locations,
        "entrances": entrances,
        "completion": _rule_payload(completion),
    }


def write_logic_export(world: "Atlyss", output_directory: str) -> str:
    import os

    payload = build_logic_package(world)
    path = os.path.join(output_directory, f"atlyss_logic_p{world.player}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    return path


def should_export_logic(world: "Atlyss") -> bool:
    if getattr(world.settings, "export_logic", False):
        return True
    passthrough = getattr(world.multiworld, "re_gen_passthrough", None)
    return passthrough is not None and "Atlyss" in passthrough


def rule_payload_has_text_fallback(rule_payload: object) -> bool:
    """True if export used the non-round-trip ``text`` fallback anywhere in this tree."""
    if not isinstance(rule_payload, dict):
        return False
    if "text" in rule_payload:
        return True
    children = rule_payload.get("children")
    if isinstance(children, list):
        return any(rule_payload_has_text_fallback(child) for child in children)
    return False


def collect_text_fallback_location_names(package: dict[str, Any]) -> list[str]:
    """Location names whose exported rule still uses a ``text`` fallback (UT quality check)."""
    names: list[str] = []
    for entry in package.get("locations", ()):
        if rule_payload_has_text_fallback(entry.get("rule")):
            names.append(entry["name"])
    return names


def location_rule_entry(world: "Atlyss", location_name: str) -> dict[str, Any] | None:
    """Lookup a single location rule tree from a built package (for tests / UT tools)."""
    try:
        location = world.get_location(location_name)
    except KeyError:
        return None
    return {
        "name": location.name,
        "region": location.parent_region.name if location.parent_region else None,
        "rule": _rule_payload(location.access_rule),
    }
