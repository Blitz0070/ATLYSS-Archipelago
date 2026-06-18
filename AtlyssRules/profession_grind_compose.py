"""Compose mining/fishing profession grind rules from train-band tables."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Protocol, Tuple

from rule_builder.rules import False_, Rule, True_

from .portal_compose import portal_gate_explain_label

if TYPE_CHECKING:
    from worlds.atlyss import Atlyss


class _TrainBand(Protocol):
    portal_gates: Tuple[str, ...]


class _FishingTrainBand(Protocol):
    portal_gates: Tuple[str, ...]
    spots: Tuple[str, ...]


def _format_training_spots(bands: Tuple[_FishingTrainBand, ...]) -> str:
    """Spot names for fishing bands on this train step (one spot per band)."""
    names: list[str] = []
    seen: set[str] = set()
    for band in bands:
        for spot in band.spots:
            if spot not in seen:
                seen.add(spot)
                names.append(spot)
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return " OR ".join(names)


def _format_gate_ids_player_explain(world: "Atlyss", gate_ids: Tuple[str, ...]) -> str:
    """Player-facing route text per gate id (matches quest portal explains)."""
    if not gate_ids:
        return ""
    if len(gate_ids) == 1:
        return portal_gate_explain_label(world, gate_ids[0])
    return " OR ".join(
        f"({portal_gate_explain_label(world, gate_id)})" for gate_id in gate_ids
    )


def _build_train_step_rule(
    world: "Atlyss",
    bands: Tuple[_TrainBand, ...],
    build_lower_level: Callable[["Atlyss", int], Rule],
    from_level: int,
) -> Rule:
    from worlds.atlyss.AtlyssRules.custom_rules import HasAnyPortalGate, HasPortalGate

    if not bands:
        return False_()

    options: list[Rule] = []
    for band in bands:
        parts: list[Rule] = [build_lower_level(world, from_level)]
        if band.portal_gates:
            if len(band.portal_gates) == 1:
                parts.insert(0, HasPortalGate(band.portal_gates[0]))
            else:
                parts.insert(0, HasAnyPortalGate(band.portal_gates))
        combined = parts[0]
        for part in parts[1:]:
            combined = combined & part
        options.append(combined)

    result = options[0]
    for option in options[1:]:
        result = result | option
    return result


def _format_level_step_portals_explain(world: "Atlyss", bands: Tuple[_TrainBand, ...]) -> str:
    """Portal OR options for the single train step into this level (no prior levels)."""
    options: list[str] = []
    for band in bands:
        route = _format_gate_ids_player_explain(world, band.portal_gates)
        if route:
            options.append(f"portals ({route})")
    if not options:
        return ""
    if len(options) == 1:
        return options[0]
    return "(" + " OR ".join(options) + ")"


def build_mining_grind_rule(world: "Atlyss", level: int) -> Rule:
    from worlds.atlyss.MiningData import mining_bands_for_training_step

    if level <= 1:
        return True_()
    if level > 30:
        return build_mining_grind_rule(world, 30)
    from_level = level - 1
    bands = mining_bands_for_training_step(from_level, level)
    return _build_train_step_rule(world, bands, build_mining_grind_rule, from_level)


def format_mining_grind_explain(world: "Atlyss", level: int) -> str:
    from worlds.atlyss.MiningData import mining_bands_for_training_step

    if level <= 1:
        return "Mining Lv. 1"
    if level > 30:
        return format_mining_grind_explain(world, 30)
    bands = mining_bands_for_training_step(level - 1, level)
    portal_part = _format_level_step_portals_explain(world, bands)
    if portal_part:
        return f"Mining Lv. {level} — {portal_part}"
    return f"Mining Lv. {level}"


def build_fishing_grind_rule(world: "Atlyss", level: int) -> Rule:
    from worlds.atlyss.FishingData import fishing_bands_for_training_step

    if level <= 1:
        return True_()
    if level > 30:
        return build_fishing_grind_rule(world, 30)
    from_level = level - 1
    bands = fishing_bands_for_training_step(from_level, level)
    return _build_train_step_rule(world, bands, build_fishing_grind_rule, from_level)


def format_fishing_grind_explain(world: "Atlyss", level: int) -> str:
    from worlds.atlyss.FishingData import fishing_bands_for_training_step

    if level <= 1:
        return "Fishing Lv. 1"
    if level > 30:
        return format_fishing_grind_explain(world, 30)
    bands = fishing_bands_for_training_step(level - 1, level)
    portal_part = _format_level_step_portals_explain(world, bands)
    if portal_part:
        spot = _format_training_spots(bands)
        if spot:
            return f"Fishing Lv. {level} — {spot} — {portal_part}"
        return f"Fishing Lv. {level} — {portal_part}"
    spot = _format_training_spots(bands)
    if spot:
        return f"Fishing Lv. {level} ({spot})"
    return f"Fishing Lv. {level}"


def evaluate_mining_grind(state, player: int, level: int) -> bool:
    from worlds.atlyss.MiningData import MINING_TRAIN_BANDS
    from worlds.atlyss.Rules import has_portal_gate

    if level > 30:
        return evaluate_mining_grind(state, player, 30)
    if level <= 1:
        return True
    from_level = level - 1
    for band in MINING_TRAIN_BANDS:
        if band.min_mine_level <= from_level and level <= band.max_train_level:
            if any(has_portal_gate(state, player, gate_id) for gate_id in band.portal_gates):
                return evaluate_mining_grind(state, player, from_level)
    return False


def evaluate_fishing_grind(state, player: int, level: int) -> bool:
    from worlds.atlyss.FishingData import FISHING_TRAIN_BANDS
    from worlds.atlyss.Rules import has_portal_gate

    if level > 30:
        return evaluate_fishing_grind(state, player, 30)
    if level <= 1:
        return True
    from_level = level - 1
    for band in FISHING_TRAIN_BANDS:
        if band.min_fish_level <= from_level and level <= band.max_train_level:
            if not band.portal_gates or any(
                has_portal_gate(state, player, gate_id) for gate_id in band.portal_gates
            ):
                return evaluate_fishing_grind(state, player, from_level)
    return False
