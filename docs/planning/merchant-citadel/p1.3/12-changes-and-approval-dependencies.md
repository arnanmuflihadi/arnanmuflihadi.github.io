# 12 - Changes and approval dependencies (P1.3)

## Differences between P1.2 and P1.3 in brief

P1.2 changed how the town looked (palette, seal, signs, goods, light) and moved nothing. P1.3 changes where things are and how many there are, and leaves the look alone:
five more buildings (22), both lanes moved in behind the street rows, a cross street with a pocket court, corner houses and shops on the bazaar and arrival edges,
a service court for the warehouse, and the tea house brought to within one short lane of the bazaar.

## Files

New folder `docs/planning/merchant-citadel/p1.3/` (this package). The P1.2 package in `../p1/` was not modified.

| File | Content |
|---|---|
| `README.md`, `01`-`04`, `06`-`12` | Documents listed in the README |
| `05-building-schedule.csv`, `05b-market-stall-schedule.csv` | Schedules with measured envelopes and change status |
| `visuals/` | Eight views, four before/after pairs, alternatives plans and massing, selected plan, top render, archetype sheet |
| `asset-evidence/` | Validation results, alternatives metrics, massing ray tests, usage and triangles |
| `blender-inspection/layouts_p13.py` | The three alternatives and the enclosure metric |
| `blender-inspection/massing_p13.py`, `compare_p13.py` | Massing renders, ray tests, comparison |
| `blender-inspection/town_data.py`, `citadel_lib.py`, `build_town.py`, `validate_envelopes.py`, `render_archetypes.py` | Copies of the P1.2 scripts, changed for the selected layout (A03c, per-building additions, new dressing) |
| `blender-inspection/make_p13_package.py` | This package generator |

Workspace (ignored by Git): `.asset-inspection/merchant-citadel-p1/p1.3/` holds the P1.3 data, renders, massing and blockout; `p1.2/` holds a snapshot of the P1.2 data, renders, validation and blockout.

## Scope confirmation

No production town implementation, island terrain, Three.js change, first-island asset reuse, gameplay system, dragon transport, GLB export, deployment or commit. No asset was downloaded in P1.3.

## Approval dependencies

1. **The selected layout (B, 22 buildings)**, or a preference for A, C or B plus E07.
2. **The look carried over from P1.2** was not separately approved before this brief arrived: the burgundy and blue colours, the new seal, the trade-sign pictograms, and the two added asset sources (Syntaxes of Play, Avramania). P1.3 assumes them.
3. **A05 used four times** and **A03c as a new variant**: acceptable, or ask for a second corner variant.
4. **A triangle and draw-call budget.**
5. **Authorisation to start P2.** Not assumed.

**MERCHANT CITADEL P1.3 - PENDING HUMAN REVIEW. STOP.**
