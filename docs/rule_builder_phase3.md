# Rule Builder — Phase 3 roadmap

**Prerequisite (done):** Phase 1 migration (`set_rule`, `AtlyssRules/`, `minimum_ap_version` 0.6.7) and Phase 2 (`CachedRuleBuilderWorld`, composed portal/shop/area rules, `export_logic`, caching fixes). See `.cursor/rules/archipelago-apworld-standards.mdc`.

**Verify gate (unchanged):** pytest green; 10k fuzz gated FillError **≤ 0.30%**. Do not chase 0% without a pool/fill change.

**Status (Jun 2026):** Phase 3 complete — ready for playtest after repack. Repack `atlyss.apworld` from this repo before hosting.

---

## Hybrid logic model (access vs fill)

Archipelago exposes **two** rule systems. Atlyss uses both by design — not a temporary gap.

| Layer | API | Evaluates | Atlyss home |
|-------|-----|-----------|-------------|
| **Location / entrance access** | `world.set_rule(spot, Rule)` → `Rule.Resolved` | `CollectionState` — “can player reach this check?” | `AtlyssRules/` (quests, portals, shops, areas) |
| **Item placement (fill)** | `add_item_rule(location, ItemRule)` | `Item` — “may this pool item be placed here?” | `ProgressionLogic.py` (tier caps, junk-only, filler reservation) |

References:

- [Rule Builder](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/rule%20builder.md) — access rules only (`set_rule`, `Has`, `CanReach*`, caching on **collection**).
- [World API — Setting Rules](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md) — `add_item_rule`, `forbid_item` for fill.

`Has("Iron Bow")` in Rule Builder means the player **collected** that item for logic. It does **not** restrict which item fill places on a location. Tier/junk/filler constraints stay on `location.item_rule` lambdas (same pattern as OOT, KH2, Earthbound, etc.).

**Pool/fill helpers** (`prefill_tiered_equipment`, gated rebalance, `_strip_tiered_items_from_pool`) complement item rules; they do not replace them.

There is **no** `set_item_rule` / Rule Builder integration for fill in AP 0.6.7. Migrating placement to `Rule` trees would require a new upstream API (`Item` + fill + export), not a small refactor.

---

## Phase 2 recap — what is already shipped

| Area | Status |
|------|--------|
| `CachedRuleBuilderWorld` + `item_mapping` | On `Atlyss`; progression/useful `clear()` on collect; filler scoped invalidation; empty cache on `copy_mixin` |
| Composed portal/shop/quest access | `Has` / `HasAll` via `portal_compose.py` |
| Entrance story + portals | `CanAccessAreaGameplay` → `build_area_gameplay_rule` + `RegionTagged` |
| Logic JSON export | `atlyss_logic_pN.json` on UT regen or `export_logic: true` |
| Custom `explain_json` | Quest / portal / shop wrappers + boss/grind |
| **Location access** | Rule Builder |
| **Item placement (fill)** | `ProgressionLogic` + `add_item_rule` (intentional) |

---

## Phase 3 tracks

### A — Universal Tracker consumer (apworld) ✅

- [x] Schema in `export_logic.py`; UT regen / `export_logic`; round-trip tests; `meta.item_mapping`

### B — Explain polish (apworld) ✅

- [x] `QuestCheck`, `HasPortalGate`, `ShopSlotCheck` explain wrappers + structure tests

### C — Cache / perf tuning (apworld) ✅

- [x] Hybrid `Atlyss.collect` (progression/useful clear; filler dep invalidation); `copy_mixin` unchanged
- [x] Profile hot paths — `scripts/profile_get_all_state.py`; pytest guard on `get_all_state` duration

### D — `ProgressionLogic` / fill (apworld) ✅

- [x] Gated rebalance: `_gated_rebalance_useful_item`, no second prefill, end strip; regression seeds + 10k fuzz
- [x] **Hybrid documented:** access = Rule Builder; placement = `add_item_rule` — **not** deferred due to missing AP item rules; **by design** until upstream adds fill Rule API
- [x] `test/test_progression_logic.py` — item-rule lambdas + fill smoke

### E — Client / ops

| Item | Where | Status |
|------|-------|--------|
| Auto-reconnect after unexpected disconnect | `AtlyssAP` plugin | Done (`Connection.AutoReconnect`) |
| WebHost / setup docs | `docs/setup_en.md`, host `en_Atlyss.md` | Done |
| Repack `atlyss.apworld` | Manual after SOT changes | User |

---

## Explicit non-goals (Phase 3)

- Rewriting `Rules.py` parity helpers away
- Migrating `add_item_rule` to Rule Builder without upstream fill support
- Changing item pool / `fill_slot_data` without mod + `GoalCompletion` sync
- Chasing 0% fuzz without a documented pool change
- Editing `AtlyssAP/dev-archipelago-source/worlds/atlyss/` for feature work (SOT only)

---

## Quick reference

| Topic | Status |
|-------|--------|
| `CachedRuleBuilderWorld` + portals | **Done** |
| UT logic export | **Done** — custom eval rules export via `_atlyss_rule_template` |
| Explain on quest/portal/shop | **Done** (track B) |
| `add_item_rule` / tier+junk fill | **Done** (track D) — stays lambdas, shared tier tables with access |

---

## Suggested PR order (historical)

A → B → D → C shipped on apworld. **E** is separate (`AtlyssAP/`).
