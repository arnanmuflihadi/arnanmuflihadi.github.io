# 04 - Selected layout design bible (P1.3, alternative B)

Plan: [orthographic-town-plan.png](visuals/orthographic-town-plan.png). Data: `blender-inspection/layouts_p13.py` and `town_data.py`.
The architectural language, palette, signage and goods are those of the P1.2 design bible and style specification (`../p1/01`, `../p1/05`); this
document covers what P1.3 changes: the form of the town.

## The town in one paragraph

A visitor arrives in a court with a shop on the left and a two-storey merchant house on the right, passes between the gate lodges and walks up a
street of shopfronts. Half way, a cross street opens on both sides: left to the lantern lane of workshops, right through a small pocket court to
the warehouse lane, where the guild warehouse and the counting house face each other across a service court. The street ends in the bazaar, now
edged by corner houses, a perimeter shop and the registry. Between the two stone corner houses the court narrows to the width of the hall's
podium. From the bazaar's north-east corner a short lane passes a tea merchant's shop and opens onto the lookout terrace.

## Coordinates and size

Metres. Origin = centre of the arrival court. Plan x = east, n = north; project (x, y, z) = (x, elevation, -n). `rotation_y`: 0 = front faces south, 90 = east, -90 = west, 180 = north.
Developed envelope: x -28.5..42 (70.5 m), z -90..8 (98 m). P1.2 was 74.5 x 98 m: the town is 4 m narrower with five more buildings.

## Six clusters

| Cluster | Buildings | Form |
|---|---|---|
| A Arrival merchants | E01, E02, gate lodges, B04, B07 | Court 20 x 16 m with a single-storey shop west and a two-storey house east; lodges; the first two street buildings behind |
| B Merchant street | B04-B09 | Facades 10 m apart, 6 m eaves; gated 2 m gaps; a 4 m cross street at mid-length with a pocket court on its east side |
| C Bazaar district | B02, B03, B06, B09, B14, B15, B16, E03, E05 | 44 x 26 m plaza; halls in the middle; corner houses north, shop ends south, perimeter shop west, registry and tea route house east |
| D Civic exchange | B01, B15, B16 | Court 28 x 12 m between two stone corner houses, aligned with the podium |
| E Secondary trade quarters | B10-B13, E04 | Lanes 4 m wide directly behind the street rows; artisan workyard at the north end of one, service court on the other |
| F Scenic edge | B17, E05 | Tea lane 8 m long, terrace 12 x 10 m, tea house on its north side |

## Spatial sequence on the primary route

| Step | Space | Width between buildings | Character |
|---|---|---|---|
| 1 | Arrival court | 20 m | Open, two fronts |
| 2 | Gate | 4 m lane between lodges | Threshold |
| 3 | Street, south half | 10 m | Enclosed, shopfronts |
| 4 | Simpang Timbangan | 10 m with 4 m openings and an 8 x 6 m pocket | Junction: first choice of route |
| 5 | Street, north half | 10 m | Enclosed |
| 6 | Bazaar | 44 m, 9 m between stall rows | Wide, busy, hall roofs either side |
| 7 | Civic court | 28 m | Formal, stone, no stalls |
| 8 | Podium and porch | - | Arrival |

## Street enclosure (wall-top height to facade distance)

| Street | Facade to facade | Wall-top heights | Ratio | Reading |
|---|---|---|---|---|
| Merchant street | 10 m | 6 m and 3 m | 0.3-0.6 | Comfortably enclosed at the 6.6 m high camera |
| Lanes | 4.5-7.5 m (lane plus yard) | 3 m workshops, 6 m street backs | 0.4-1.3 | Intimate; yards keep the 6 m backs 1-3 m off the lane so sky stays open |
| Cross street | 4 m | 6 m and 3 m | 0.75-1.5 | Short and tight by intent (9 m each side) |
| Civic court | 28 m | 6 m sides, 7 m hall | 0.2-0.25 | Formal forecourt; was 36 m |

No route was narrowed below the P1.2 gameplay widths: lanes stay 4 m, the street keeps 8 m clear.

## Building positions

| ID | Archetype | Name | Position (x, y, z) | rotation_y | Nominal footprint (m) | Measured envelope (m) | Change since P1.2 |
|---|---|---|---|---|---|---|---|
| B01 | A01 | Exchange Hall | (0, 1.0, -84) | 0 | 28 x 18 | 28.09 x 18.0 | kept |
| B02 | A02 | Market Hall West (provisions) | (-13, 0.0, -50) | 0 | 8 x 12 | 9.95 x 15.42 | kept |
| B03 | A02 | Market Hall East (crafts and general trade) | (13, 0.0, -50) | 0 | 8 x 12 | 9.95 x 15.42 | kept |
| B04 | A05 | Junction Corner House (money changer) | (-9, 0.0, -14) | 90 | 8 x 8 | 10.46 x 10.36 | rotated 0 to 90 |
| B05 | A03b | Shophouse W1, eaves to street (baker) | (-8, 0.0, -26) | 90 | 6 x 8 | 8.64 x 9.68 | moved from (-8, -25) by 1.0 m |
| B06 | A04 | Compact Shop W2 (dry goods) | (-8, 0.0, -34.4) | 90 | 6 x 4 | 8.31 x 5.51 | moved from (-8, -33.5) by 0.9 m |
| B07 | A03 | Jettied Shophouse E1 (map and book seller) | (9, 0.0, -13) | -90 | 8 x 6 | 11.85 x 8.25 | kept |
| B08 | A04b | Compact Shop E2, eaves to street (potter) | (7, 0.0, -25) | -90 | 4 x 6 | 6.14 x 7.59 | moved from (7, -22.5) by 2.5 m |
| B09 | A03 | Jettied Shophouse E3 (provisioner) | (9, 0.0, -33.6) | -90 | 8 x 6 | 11.85 x 8.25 | moved from (9, -32) by 1.6 m |
| B15 | A05 | Court Corner House West (assay office, guild) | (-18, 0.0, -67) | 0 | 8 x 8 | 10.36 x 10.46 | moved from (-22, -67) by 4.0 m; rotated 90 to 0 |
| B10 | A06 | Workshop South (smith) | (-21.5, 0.0, -11) | 90 | 6 x 6 | 8.75 x 8.51 | moved from (-25.5, -13) by 4.5 m |
| B11 | A04b | Lane Shop closing the cross street (potter's yard) | (-20.5, 0.0, -20) | 90 | 4 x 6 | 6.14 x 7.59 | moved from (-24.5, -22.5) by 4.7 m |
| B12 | A06 | Workshop North (joiner) | (-21.5, 0.0, -29) | 90 | 6 x 6 | 8.75 x 8.51 | moved from (-25.5, -31.5) by 4.7 m |
| B13 | A07 | Guild Warehouse | (25.5, 0.0, -12) | -90 | 14 x 8 | 16.23 x 12.96 | moved from (29.5, -18) by 7.2 m |
| B14 | A04 | Registry Office (guild), on the bazaar edge | (25.5, 0.0, -41) | -90 | 6 x 4 | 8.31 x 5.51 | moved from (25.5, -29) by 12.0 m |
| B16 | A05 | Court Corner House East (chart maker) | (18, 0.0, -67) | -90 | 8 x 8 | 10.46 x 10.36 | re-typed A03 to A05; moved from (22, -67) by 4.0 m |
| B17 | A08 | Tea House | (36, 0.0, -67) | 0 | 6 x 8 | 8.5 x 9.04 | moved from (40, -58) by 9.8 m |
| E01 | A04b | South Gateway Shop (traveller's outfitter) | (-12, 0.0, 1) | 90 | 4 x 6 | 6.14 x 7.59 | new |
| E02 | A03c | Arrival Corner Merchant House (carrier's office) | (12, 0.0, 2) | -90 | 4 x 8 | 6.28 x 9.68 | new |
| E03 | A03b | Bazaar Perimeter Shop West (grain and oil merchant) | (-25.5, 0.0, -46) | 90 | 6 x 8 | 8.64 x 9.68 | new |
| E04 | A05 | Merchant Counting House (guild) | (22.5, 0.0, -28) | -90 | 8 x 8 | 10.46 x 10.36 | new |
| E05 | A04b | Tea Route Merchant House (tea and spice seller) | (25.5, 0.0, -53.5) | 180 | 6 x 4 | 7.59 x 6.14 | new |

**18 of 22 buildings are new, moved, rotated or re-typed; 4 are where P1.2 had them** (the hall, both market halls, B07). No building was deleted. Full figures: [05-building-schedule.csv](05-building-schedule.csv).

## Keeping reused archetypes from reading as copies

Five additions come from four existing archetypes and one new variant. They differ by orientation, storey count on the plot, sign pictogram and per-building
additions: the counting house and the assay office carry the guild seal, the counting house a burgundy banner, the perimeter shop a vine and grain sacks,
the tea route shop a keg and a menu stand. A05 is now used four times (two court corners, junction corner, counting house); that repetition is deliberate for the
stone civic-commercial class but is the first candidate for a second corner variant if it reads as repetitive in play.

## Stalls

12 stalls, unchanged in number and kind. Two moved 2.1 m north and two 0.7 m south so the paths from the lanes and to the court pass them with clearance (05b).
The count was not raised: the bazaar's weakness was its edge, not the number of stalls.
