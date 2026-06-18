"""
Mining profession train bands — in-game nodes mapped to portal route gates.

Each band describes one ore/node tier:
  min_mine_level  — minimum profession level required to mine this node.
  max_train_level — highest level this node can still train toward efficiently;
                    above this, the node is impractical (e.g. Hefty Stone caps at 3).

To reach profession level N (N > 1), find a band where you can take the step
(N-1) → N: min_mine_level <= N-1 and N <= max_train_level, with portal access,
and can_grind_mine(N-1) recursively. Level 1 is pickaxe-only (base case).

Overlapping numbers across bands are not OR alternatives at one level — they mark
where one tier ends and the next begins (Hefty trains through 3; Amberite needs 3+).
"""
from __future__ import annotations

from typing import Tuple

from typing_extensions import NamedTuple


class MiningTrainBand(NamedTuple):
    min_mine_level: int
    max_train_level: int
    portal_gates: Tuple[str, ...]
    nodes: Tuple[str, ...]


MINING_TRAIN_BANDS: Tuple[MiningTrainBand, ...] = (
    MiningTrainBand(1, 3, ("arcwood_pass", "effold_terrace"), ("Hefty Stone",)),
    MiningTrainBand(
        2,
        3,
        ("arcwood_pass", "effold_terrace", "outer_sanctum", "crescent_keep", "tuul_enclave"),
        ("Dense Stone",),
    ),
    MiningTrainBand(3, 6, ("tuul_valley", "crescent_keep"), ("Amberite Ore",)),
    MiningTrainBand(6, 10, ("tuul_enclave",), ("Sapphite Ore",)),
)


def iter_mining_train_portal_gates() -> Tuple[str, ...]:
    """Every PORTAL_GATES id referenced by mining train bands (stable order)."""
    seen: set[str] = set()
    names: list[str] = []
    for band in MINING_TRAIN_BANDS:
        for gate_id in band.portal_gates:
            if gate_id not in seen:
                seen.add(gate_id)
                names.append(gate_id)
    return tuple(names)


def mining_bands_for_training_step(from_level: int, to_level: int) -> Tuple[MiningTrainBand, ...]:
    """Bands that can grind profession level from_level → to_level (one step)."""
    if to_level != from_level + 1:
        return ()
    return tuple(
        band for band in MINING_TRAIN_BANDS
        if band.min_mine_level <= from_level and to_level <= band.max_train_level
    )


def _validate_mining_train_bands() -> None:
    from .QuestAccess import PORTAL_GATES

    if not MINING_TRAIN_BANDS:
        raise ValueError("MINING_TRAIN_BANDS cannot be empty")
    for band in MINING_TRAIN_BANDS:
        if band.min_mine_level > band.max_train_level:
            raise ValueError(
                f"Mining band min_mine_level > max_train_level: "
                f"{band.min_mine_level}>{band.max_train_level}"
            )
        if not band.portal_gates:
            raise ValueError(
                f"Mining band {band.nodes} ({band.min_mine_level}-{band.max_train_level}) "
                "has no portal_gates"
            )
        if not band.nodes:
            raise ValueError("Mining band has no nodes")
        for gate_id in band.portal_gates:
            if gate_id not in PORTAL_GATES:
                raise ValueError(f"Unknown mining train portal gate: {gate_id}")
    for to_level in range(2, 11):
        from_level = to_level - 1
        if not mining_bands_for_training_step(from_level, to_level):
            raise ValueError(
                f"No mining train band covers profession step {from_level} → {to_level}"
            )


_validate_mining_train_bands()
