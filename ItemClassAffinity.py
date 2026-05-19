"""Equipment class affinity (from Improved-Logic fork item_table)."""
from __future__ import annotations
from typing import Dict, FrozenSet, Optional

from .ItemTiers import ITEM_CLASS_AFFINITY

CLASS_FILTER_MAP: Dict[int, Optional[FrozenSet[str]]] = {
    0: None,
    1: frozenset({"F"}),
    2: frozenset({"M"}),
    3: frozenset({"B"}),
    4: frozenset({"F", "M"}),
    5: frozenset({"F", "B"}),
    6: frozenset({"M", "B"}),
}


def item_passes_class_filter(filter_value: int, item_name: str) -> bool:
    """Universal items (no affinity) always pass."""
    selected = CLASS_FILTER_MAP.get(filter_value)
    if selected is None:
        return True
    affinity = ITEM_CLASS_AFFINITY.get(item_name)
    if affinity is None:
        return True
    return bool(set(affinity) & selected)

