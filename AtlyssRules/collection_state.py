"""CollectionState hooks for Atlyss rule-builder caching during fill."""
from __future__ import annotations

from BaseClasses import CollectionState
from worlds.AutoWorld import AutoLogicRegister


class AtlyssCollectionState(metaclass=AutoLogicRegister):
    """Fill copies CollectionState; inherited rule caches must not carry stale And results."""

    def copy_mixin(self, ret: CollectionState) -> CollectionState:
        if hasattr(ret, "rule_builder_cache"):
            ret.rule_builder_cache = {player: {} for player in ret.rule_builder_cache}
        return ret
