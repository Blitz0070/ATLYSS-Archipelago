"""
Fishing profession train bands — one fishing spot per band, mapped to portal route gates.

Each band describes one spot tier:
  min_fish_level   — minimum profession level required to fish this spot.
  max_train_level  — highest level this spot can still train toward efficiently.
  portal_gates     — OR routes to reach the spot; empty means Sanctum hub (no portal).

To reach profession level N (N > 1), find a band for step (N-1) → N with portal access
and can_grind_fish(N-1) recursively. Level 1 is fishing-rod-only (base case).
"""
from __future__ import annotations

from typing import Tuple

from typing_extensions import NamedTuple


class FishingTrainBand(NamedTuple):
    min_fish_level: int
    max_train_level: int
    portal_gates: Tuple[str, ...]
    spots: Tuple[str, ...]


FISHING_TRAIN_BANDS: Tuple[FishingTrainBand, ...] = (
    FishingTrainBand(1, 3, (), ("Sanctum",)),
    FishingTrainBand(3, 6, ("arcwood_pass",), ("Arcwood Pass",)),
    FishingTrainBand(6, 10, ("crescent_road",), ("Crescent Road",)),
)


def iter_fishing_train_portal_gates() -> Tuple[str, ...]:
    """Every PORTAL_GATES id referenced by fishing train bands (stable order)."""
    seen: set[str] = set()
    names: list[str] = []
    for band in FISHING_TRAIN_BANDS:
        for gate_id in band.portal_gates:
            if gate_id not in seen:
                seen.add(gate_id)
                names.append(gate_id)
    return tuple(names)


def fishing_bands_for_training_step(from_level: int, to_level: int) -> Tuple[FishingTrainBand, ...]:
    """Bands that can grind profession level from_level → to_level (one step)."""
    if to_level != from_level + 1:
        return ()
    return tuple(
        band for band in FISHING_TRAIN_BANDS
        if band.min_fish_level <= from_level and to_level <= band.max_train_level
    )


def _validate_fishing_train_bands() -> None:
    from .QuestAccess import PORTAL_GATES

    if not FISHING_TRAIN_BANDS:
        raise ValueError("FISHING_TRAIN_BANDS cannot be empty")
    for band in FISHING_TRAIN_BANDS:
        if band.min_fish_level > band.max_train_level:
            raise ValueError(
                f"Fishing band min_fish_level > max_train_level: "
                f"{band.min_fish_level}>{band.max_train_level}"
            )
        if len(band.spots) != 1:
            raise ValueError(f"Fishing band {band.spots!r} must have exactly one spot")
        for gate_id in band.portal_gates:
            if gate_id not in PORTAL_GATES:
                raise ValueError(f"Unknown fishing train portal gate: {gate_id}")
    for to_level in range(2, 11):
        from_level = to_level - 1
        if not fishing_bands_for_training_step(from_level, to_level):
            raise ValueError(
                f"No fishing train band covers profession step {from_level} → {to_level}"
            )


_validate_fishing_train_bands()
