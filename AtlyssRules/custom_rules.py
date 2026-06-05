"""Atlyss-specific Rule Builder rules."""
from __future__ import annotations

import dataclasses
from typing import ClassVar, TYPE_CHECKING

from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import Has, Rule, True_

from .portal_compose import (
    build_area_gameplay_rule,
    build_fishing_route_rule,
    build_mining_route_rule,
    build_portal_gate_rule,
    build_shop_slot_rule,
    caching_enabled,
    portal_gate_explain_label,
)

if TYPE_CHECKING:
    from worlds.atlyss import Atlyss


@dataclasses.dataclass()
class HasPortalGate(Rule["Atlyss"], game="Atlyss"):
    gate_id: str

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        child = build_portal_gate_rule(world, self.gate_id).resolve(world)
        return self.Resolved(
            self.gate_id,
            child,
            portal_gate_explain_label(world, self.gate_id),
            player=world.player,
            caching_enabled=caching_enabled(world),
        )

    class Resolved(Rule.Resolved):
        gate_id: str
        child: Rule.Resolved
        portal_label: str
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.child(state)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return self.child.item_dependencies()

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            color = "green" if state and self(state) else "salmon" if state else "white"
            return [
                {"type": "text", "text": "Portals ("},
                {"type": "color", "color": color, "text": self.portal_label},
                {"type": "text", "text": ")"},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            prefix = ""
            if state is not None:
                prefix = ("Open: " if self(state) else "Locked: ") + "portals — "
            return prefix + self.portal_label


@dataclasses.dataclass()
class HasQuestComplete(Rule["Atlyss"], game="Atlyss"):
    quest_name: str

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        return Has(f"Complete: {self.quest_name}").resolve(world)


@dataclasses.dataclass()
class QuestCheck(Rule["Atlyss"], game="Atlyss"):
    quest_name: str

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        from worlds.atlyss.QuestAccess import QUEST_ACCESS

        _min_level, after, gate = QUEST_ACCESS[self.quest_name]
        parts: list[Rule] = []
        if after is not None:
            parts.append(HasQuestComplete(after))
        if gate is not None:
            parts.append(HasPortalGate(gate))
        if not parts:
            child = True_().resolve(world)
        else:
            combined = parts[0]
            for part in parts[1:]:
                combined = combined & part
            child = combined.resolve(world)
        return self.Resolved(
            self.quest_name,
            child,
            quest_check_explain_str(world, self.quest_name),
            player=world.player,
            caching_enabled=caching_enabled(world),
        )

    class Resolved(Rule.Resolved):
        quest_name: str
        child: Rule.Resolved
        base_explain: str
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.child(state)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return self.child.item_dependencies()

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": self.base_explain}]
            color = "green" if self(state) else "salmon"
            return [
                {"type": "color", "color": color, "text": "Reachable" if self(state) else "Blocked"},
                {"type": "text", "text": ": " + self.base_explain},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return self.base_explain
            prefix = "Reachable: " if self(state) else "Blocked: "
            return prefix + self.base_explain


def quest_check_explain_str(world: "Atlyss", quest_name: str, state: CollectionState | None = None) -> str:
    from worlds.atlyss.QuestAccess import QUEST_ACCESS

    _min_level, after, gate = QUEST_ACCESS[quest_name]
    parts = [f"Quest {quest_name}"]
    if after is not None:
        parts.append(f"after {after}")
    if gate is not None:
        parts.append(f"portals ({portal_gate_explain_label(world, gate)})")
    text = parts[0] + (" — " + ", ".join(parts[1:]) if len(parts) > 1 else "")
    if state is not None:
        rule = QuestCheck(quest_name).resolve(world)
        text = ("Reachable: " if rule(state) else "Blocked: ") + text
    return text


@dataclasses.dataclass()
class CanAccessAreaGameplay(Rule["Atlyss"], game="Atlyss"):
    """Entrance rule: composed portal/story access plus region_dependencies for indirects."""

    area_name: str

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        child = build_area_gameplay_rule(world, self.area_name).resolve(world)
        return self.RegionTagged(
            self.area_name,
            child,
            player=world.player,
            caching_enabled=caching_enabled(world),
        )

    class RegionTagged(Rule.Resolved):
        """Delegates evaluation to composed rule; tags region for cache invalidation / indirects."""

        area_name: str
        child: Rule.Resolved
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.child(state)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return self.child.item_dependencies()

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {self.area_name: {id(self)}}


@dataclasses.dataclass()
class CanGrindLevel(Rule["Atlyss"], game="Atlyss"):
    level: int

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        return self.Resolved(self.level, player=world.player, caching_enabled=caching_enabled(world))

    class Resolved(Rule.Resolved):
        level: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            from worlds.atlyss.Rules import can_grind_level

            return can_grind_level(state, self.player, self.level)

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            color = "green" if state and self(state) else "salmon"
            return [
                {"type": "text", "text": "Reach Level "},
                {"type": "color", "color": color, "text": str(self.level)},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            prefix = "Reach Level " if state is None or self(state) else "Cannot reach Level "
            return prefix + str(self.level)


@dataclasses.dataclass()
class CanGrindFishing(Rule["Atlyss"], game="Atlyss"):
    level: int

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        return (
            RequiresFishingRod()
            & build_fishing_route_rule(world, self.level)
            & CanGrindLevel(self.level)
        ).resolve(world)


@dataclasses.dataclass()
class CanGrindMining(Rule["Atlyss"], game="Atlyss"):
    level: int

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        return (
            RequiresPickaxe()
            & build_mining_route_rule(world, self.level)
            & CanGrindLevel(self.level)
        ).resolve(world)


@dataclasses.dataclass()
class CanBeatBoss(Rule["Atlyss"], game="Atlyss"):
    enemy_name: str

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        return self.Resolved(self.enemy_name, player=world.player, caching_enabled=caching_enabled(world))

    class Resolved(Rule.Resolved):
        enemy_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            from worlds.atlyss.Rules import can_beat_enemy

            return can_beat_enemy(state, self.player, self.enemy_name)

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            color = "green" if state and self(state) else "salmon"
            return [
                {"type": "text", "text": "Beat "},
                {"type": "color", "color": color, "text": self.enemy_name},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            prefix = "Beat " if state is None or self(state) else "Cannot beat "
            return prefix + self.enemy_name


@dataclasses.dataclass()
class HasProgressionItem(Rule["Atlyss"], game="Atlyss"):
    item_name: str
    count: int = 1

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        return self.Resolved(self.item_name, self.count, player=world.player, caching_enabled=caching_enabled(world))

    class Resolved(Rule.Resolved):
        item_name: str
        count: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            from worlds.atlyss.Rules import has_item

            return has_item(state, self.player, self.item_name, self.count)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: {id(self)}}


@dataclasses.dataclass()
class ShopSlotCheck(Rule["Atlyss"], game="Atlyss"):
    merchant: str
    slot: int

    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        child = build_shop_slot_rule(world, self.merchant, self.slot).resolve(world)
        return self.Resolved(
            self.merchant,
            self.slot,
            child,
            shop_slot_explain_str(world, self.merchant, self.slot),
            player=world.player,
            caching_enabled=caching_enabled(world),
        )

    class Resolved(Rule.Resolved):
        merchant: str
        slot: int
        child: Rule.Resolved
        base_explain: str
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.child(state)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return self.child.item_dependencies()

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": self.base_explain}]
            color = "green" if self(state) else "salmon"
            return [
                {"type": "color", "color": color, "text": "Open" if self(state) else "Locked"},
                {"type": "text", "text": ": " + self.base_explain},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return self.base_explain
            prefix = "Open: " if self(state) else "Locked: "
            return prefix + self.base_explain


def shop_slot_explain_str(world: "Atlyss", merchant: str, slot: int, state: CollectionState | None = None) -> str:
    from worlds.atlyss.AccessData import SHOP_AP_ITEMS_PORTAL_GATE

    portal_label = portal_gate_explain_label(world, SHOP_AP_ITEMS_PORTAL_GATE)
    prefix = f"Buy from {merchant} #{slot}"
    if state is not None:
        rule = ShopSlotCheck(merchant, slot).resolve(world)
        prefix = ("Open: " if rule(state) else "Locked: ") + prefix
    return f"{prefix} — portals: {portal_label}"


@dataclasses.dataclass()
class RequiresFishingRod(Rule["Atlyss"], game="Atlyss"):
    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        return self.Resolved(player=world.player, caching_enabled=caching_enabled(world))

    class Resolved(Rule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            from worlds.atlyss.Rules import has_fishing_tool_for_logic

            return has_fishing_tool_for_logic(state, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {"Fishing Rod": {id(self)}}


@dataclasses.dataclass()
class RequiresPickaxe(Rule["Atlyss"], game="Atlyss"):
    @override
    def _instantiate(self, world: "Atlyss") -> Rule.Resolved:
        return self.Resolved(player=world.player, caching_enabled=caching_enabled(world))

    class Resolved(Rule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            from worlds.atlyss.Rules import has_mining_tool_for_logic

            return has_mining_tool_for_logic(state, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {"Pickaxe": {id(self)}}
