# 06 - Measured town masterplan (P1.2)

Drawing: [visuals/orthographic-town-plan.png](visuals/orthographic-town-plan.png). Data: `blender-inspection/town_data.py`. P1.2 keeps the plan the owner
approved in P1.1: no building, stall, walking node or paved surface was moved. What changed is on and around the buildings.

## Coordinates

Metres. Origin = centre of the arrival court. Plan axes: x = east, n = north. Project / Three.js: **(x, y, z) = (x, elevation, -n)**, +y up.
`rotation_y`: 0 = front faces south (+z), 90 = east, -90 = west, 180 = north.

## Size

Developed envelope (nominal): x -28.5..46 (74.5 m), z -90..8 (98 m). With the transport reservation: 74.5 x 114 m (10).

## Programme

**17 permanent buildings, 8 archetypes (two with an eaves-to-street variant), 12 market stalls, 1 split gateway, 1 market cross.**
All counts are those of the approved P1.1. (The brief's baseline of 10 stalls is the P1.0 figure; P1.1 raised it to 12 and P1.2 keeps 12.)

## What changed in P1.2, and why

Positions and rotations: **none changed**. The P1.1 change table is kept in the P1.1 documents (`.asset-inspection/merchant-citadel-p1/p1.1/docs/`).

| Element | Change | Spatial reason |
|---|---|---|
| A03 shophouses (B07, B09, B16) | Upper floor jettied 1.12 m towards the street; measured envelope 10.54 to 11.85 m deep | Gives the street a second, closer layer at first-floor height; the ground-floor line and the 8 m clear width are unchanged |
| A03b, A04 (B05, B06, B14) | Timber shopfront canopy across the front | Marks shop entrances at eye level |
| Exchange Hall B01 | Gabled porch 6 x 2 m in front of the doors, inside the existing podium | Gives the entrance a depth and a centre; no footprint change (still 28 x 16 m podium) |
| Market halls B02, B03 | Interiors restocked as two different kits; aisle and cross-passage kept clear | Halls now differ by trade |
| Stalls | Same 12 positions; kinds changed (07b) | Variety without moving anything |
| Hall corners, bazaar | Goods stacked at the four inner hall corners, outside the arcades | Fills the dead corners beside the stall rows; clear of every walking edge |
| Back courts | Shown as packed earth; a well in the west court | Reads as yards, not leftover grass |
| Tea terrace | Cafe furniture replaces the bench set | A place to sit, as the brief asks |

## Building positions, nominal footprint and measured envelope

| ID | Archetype | Name | Position (x, y, z) | rotation_y | Front faces | Nominal footprint on plan (m) | Measured envelope incl. roof, signs, props (m) |
|---|---|---|---|---|---|---|---|
| B01 | A01 | Exchange Hall | (0, 1.0, -84) | 0 | south | 28 x 18 | 28.09 x 18.0 |
| B02 | A02 | Market Hall West (provisions) | (-13, 0.0, -50) | 0 | south | 8 x 12 | 9.95 x 15.42 |
| B03 | A02 | Market Hall East (crafts and general trade) | (13, 0.0, -50) | 0 | south | 8 x 12 | 9.95 x 15.42 |
| B04 | A05 | Gate Corner House (money changer) | (-9, 0.0, -14) | 0 | south | 8 x 8 | 10.36 x 10.46 |
| B05 | A03b | Shophouse W1, eaves to street (baker) | (-8, 0.0, -25) | 90 | east | 6 x 8 | 8.64 x 9.68 |
| B06 | A04 | Compact Shop W2 (dry goods) | (-8, 0.0, -33.5) | 90 | east | 6 x 4 | 8.31 x 5.51 |
| B07 | A03 | Jettied Shophouse E1 (map and book seller) | (9, 0.0, -13) | -90 | west | 8 x 6 | 11.85 x 8.25 |
| B08 | A04b | Compact Shop E2, eaves to street (potter) | (7, 0.0, -22.5) | -90 | west | 4 x 6 | 6.14 x 7.59 |
| B09 | A03 | Jettied Shophouse E3 (provisioner) | (9, 0.0, -32) | -90 | west | 8 x 6 | 11.85 x 8.25 |
| B10 | A06 | Workshop South (smith) | (-25.5, 0.0, -13) | 90 | east | 6 x 6 | 8.75 x 8.51 |
| B11 | A04b | Lane Shop, eaves to lane (potter's yard) | (-24.5, 0.0, -22.5) | 90 | east | 4 x 6 | 6.14 x 7.59 |
| B12 | A06 | Workshop North (joiner) | (-25.5, 0.0, -31.5) | 90 | east | 6 x 6 | 8.75 x 8.51 |
| B13 | A07 | Guild Warehouse | (29.5, 0.0, -18) | -90 | west | 14 x 8 | 16.23 x 12.96 |
| B14 | A04 | Registry Office (guild) | (25.5, 0.0, -29) | -90 | west | 6 x 4 | 8.31 x 5.51 |
| B15 | A05 | Court Corner House (assay office, guild) | (-22, 0.0, -67) | 90 | east | 8 x 8 | 10.46 x 10.36 |
| B16 | A03 | Court Shophouse (chart maker) | (22, 0.0, -67) | -90 | west | 8 x 6 | 11.85 x 8.25 |
| B17 | A08 | Tea House | (40, 0.0, -58) | 0 | south | 6 x 8 | 8.5 x 9.04 |

The measured envelope is the axis-aligned bound of everything attached to the building in the assembled scene. It is what must be kept clear, and it
is drawn dashed on the plan. Roofs overhang the wall lines by 0.8 to 1.1 m on each side; the A03 jetty adds 1.12 m at the front above 3 m. Full figures: [07-building-placement-schedule.csv](07-building-placement-schedule.csv).

## Paved surfaces (2 m tiles; later rows overlay earlier ones)

| Surface | x | z | Size (m) | Tile |
|---|---|---|---|---|
| D1 Arrival court | -10..10 | -8..8 | 20 x 16 | MV-Floor_UnevenBrick |
| D1 Gate forecourt | -14..14 | -10..-6 | 28 x 4 | MV-Floor_UnevenBrick |
| D2 Merchant street | -6..6 | -36..-8 | 12 x 28 | MV-Floor_UnevenBrick |
| South cross lane W | -22..-10 | -6..-2 | 12 x 4 | MV-Floor_UnevenBrick |
| South cross lane E | 10..22 | -6..-2 | 12 x 4 | MV-Floor_UnevenBrick |
| D6 Artisan lane (red brick) | -22..-18 | -36..-6 | 4 x 30 | MV-Floor_RedBrick |
| D7 Warehouse lane | 18..22 | -36..-6 | 4 x 30 | MV-Floor_UnevenBrick |
| D3 Bazaar plaza | -22..22 | -62..-36 | 44 x 26 | MV-Floor_UnevenBrick |
| Market Hall West floor | -18..-8 | -56..-44 | 10 x 12 | MV-Floor_Brick |
| Market Hall East floor | 8..18 | -56..-44 | 10 x 12 | MV-Floor_Brick |
| Hall-to-hall cross-passage | -8..8 | -50..-48 | 16 x 2 | MV-Floor_Brick |
| Guild way (axis band) | -2..2 | -62..0 | 4 x 62 | MV-Floor_Brick |
| D4 Civic court | -18..18 | -74..-62 | 36 x 12 | MV-Floor_Brick |
| D8 Lookout path | 22..34 | -52..-48 | 12 x 4 | MV-Floor_UnevenBrick |
| D8 Lookout terrace (red brick) | 34..46 | -54..-44 | 12 x 10 | MV-Floor_RedBrick |
| Tea house veranda floor | 36..44 | -56..-54 | 8 x 2 | MV-Floor_RedBrick |

Reserved, no construction: future transport pad x -10..10, z 8..24.

## Checks

- Nominal checks (`town_data.py`): **PASS** - footprint overlaps, clear corridors, paved entrance approaches, stalls on paving, graph connectivity.
- Checks on actual geometry (`validate_envelopes.py`): reported in 09. Roof gaps failing: 0; hanging objects too low: 0; walking edges failing: 0 of 38 built.
