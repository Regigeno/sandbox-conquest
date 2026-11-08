# Sandbox Conquest — Design Document (v0.1)

> Working title. "TABS meets Age of Conquest IV" — a 2D top-down territory conquest sandbox with chaotic, customizable battles.

## 1. Core Fantasy
You are a warlord (or god) shaping a continent. You drop armies onto a map, watch them clash with emergent, slightly-chaotic combat, and conquer territory. No rigid campaign — just a sandbox where you can set up scenarios, tweak factions, and watch (or orchestrate) the world burn.

## 2. High-Level Loop
1. **Map view** — see the continent, faction territories, army stacks.
2. **Recruit / arrange** — spend resources to raise units in owned territory; drag units to form armies.
3. **Invade** — move an army stack into enemy territory → triggers a **Battle**.
4. **Battle** — units fight on a local battlefield; outcome decided by numbers, unit types, terrain, morale.
5. **Resolve** — winner takes territory; loser retreats/routed; resources redistributed.
6. **Repeat** — sandbox: no hard win/lose, but milestones (conquer X%, unite continent, etc.).

## 3. Factions (v1: 4)
| Faction | Theme | Strength | Weakness |
|---|---|---|---|
| Iron Legion | Heavy infantry, discipline | Defense, formation holding | Slow, low mobility |
| Steppe Horde | Cavalry, raiders | Speed, flanking, pursuit | Fragile in prolonged melee |
| Arcane Covenant | Magic, ranged | Area damage, morale shock | Low HP, needs protection |
| Wildfolk | Beasts, swarm | Numbers, terrain bonuses (forest) | Disorganized, poor vs. armor |

Each faction has a color, flag, and 3–5 unit types.

## 4. Units
Unit stats: HP, Attack, Defense, Speed, Range, Morale, Cost (gold), Upkeep.

- **Infantry** (Iron): swordsmen, pikemen, shield wall
- **Cavalry** (Steppe): light riders, lancers
- **Ranged** (Arcane/Wildfolk): archers, mages, slingers
- **Special**: siege (breaks fortifications), beasts (high damage, low control), healers

Units are grouped into **stacks** (armies). A stack has a commander (optional) granting a buff.

## 5. Map
- Grid of **provinces** (hex or square tiles). v1: ~60–100 provinces.
- Each province: owner (faction), terrain (plains, forest, mountains, river, city), resource yield (gold, manpower), fortification level.
- Terrain affects movement speed and battle modifiers (forest = Wildfolk bonus, mountains = defense bonus).

## 6. Combat (the TABS flavor)
Battles occur in a small local arena generated from the province terrain.

- **Auto-resolve default**: weighted outcome by stats + terrain + morale + random variance.
- **"Watch battle" mode**: spawn units on the arena, run a lightweight real-time sim (units move toward enemies, attack in range, morale breaks → rout). Slightly chaotic: friendly fire possible for mages, cavalry can trample, etc.
- **Player influence**: can place units pre-battle, pick terrain, set aggressiveness. (No micromanagement mid-fight in v1; maybe in v2.)

Morale: units rout when HP or allies drop below threshold. Routed units flee; if caught, destroyed.

## 7. Economy
- Gold: from provinces + tribute. Spends on recruitment, upgrades, mercs.
- Manpower: pool for recruiting; regenerates slowly per province.
- Upkeep: armies cost gold/turn; unpaid armies desert.

## 8. AI (enemy factions)
- Simple priority AI: expand into weak neighbors, defend threatened borders, ally against the leader (basic diplomacy).
- Difficulty = aggression + economic bonus.

## 9. UI / Controls (2D, tkinter or pygame)
- **Map view**: pan/zoom, click province for info, drag armies.
- **Side panel**: selected faction/army stats, recruit buttons, end-turn.
- **Battle view**: arena with units as colored circles/squares, HP bars, speed controls (1x/2x/pause), "auto-resolve" button.
- **Menus**: new game (pick faction, map size, AI count), settings, save/load.

## 10. Tech Stack (proposed)
- Python 3.14
- Rendering: pygame (need install) or tkinter canvas. Prefer pygame for smoother animation; tkinter fallback.
- Data: JSON for factions/units/maps; save games as JSON.
- No network in v1.

## 11. Milestones
- **M1**: Map renders, provinces clickable, armies movable (no combat).
- **M2**: Auto-resolve battles + territory capture.
- **M3**: Watch-battle mode with real-time sim.
- **M4**: Economy, recruitment, upkeep, AI turns.
- **M5**: Polish: sound, save/load, scenario editor.

## 12. Open Questions
- Hex vs. square provinces?
- Real-time full game or turn-based (AoC is turn-based-ish)? → Recommend turn-based map, real-time battles.
- How "TABS" should the battles feel? (ragdoll physics is hard in 2D; propose simple emergent unit AI instead.)
- Multiplayer? → v2+.

## 13. Out of Scope (v1)
3D, modding API, multiplayer, deep diplomacy trees, naval combat.

---

**Next step if approved:** M1 — map + movement, no combat.