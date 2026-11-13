# 01 - Urban morphology diagnosis: why the P1.2 town does not hold together

P1.2 passed every spatial check and still reads as separate buildings along one street. The reasons can be measured. "Enclosure" below is the share
of a street or court edge that has a building wall within 3-4 m of it; "active" is the share that has a building's door side facing it
(method: `layouts_p13.enclosure`, sampled every 0.5 m on nominal footprints).

| Edge | Length tested | Wall enclosure | Active frontage | What that means on the ground |
|---|---|---|---|---|
| Merchant street, west side | 26.0 m | 77% | 77% | The one edge that works: three buildings a side with 2.5-3.5 m gaps |
| Merchant street, east side | 26.0 m | 69% | 69% | As above |
| Artisan lane, outer side | 30.0 m | 60% | 60% | Three workshops with 3-5 m gaps |
| Artisan lane, inner side | 30.0 m | 0% | 0% | **Nothing.** An 8 m strip of back court and fence separates the lane from the street row |
| Warehouse lane, outer side | 30.0 m | 40% | 40% | Only the warehouse and registry, 14 m apart |
| Warehouse lane, inner side | 30.0 m | 0% | 0% | **Nothing.** Back court again |
| Bazaar, west edge | 26.0 m | 0% | 0% | **Open.** Trees and grass |
| Bazaar, east edge | 26.0 m | 0% | 0% | **Open.** A path leaves for the tea house |
| Bazaar, south edge | 44.0 m | 32% | 0% | Only the ends of two street buildings |
| Bazaar, north edge | 44.0 m | 18% | 0% | Open to the court; its two side buildings stand outside the tested band |
| Arrival court, west edge | 16.0 m | 0% | 0% | **Open.** Two gate lodges are the only structures |
| Arrival court, east edge | 16.0 m | 0% | 0% | **Open** |
| Civic court, west edge | 12.0 m | 67% | 67% | One corner house 36 m from its opposite number |
| Civic court, east edge | 12.0 m | 50% | 50% | One shophouse |

**Overall: 28% of the tested edges are enclosed and 22% are active.** Buildings cover 18.4% of the developed envelope.

## Six findings

1. **Only the merchant street is a street.** It is 10 m between facades with 6 m eaves (height to width 0.6) and 73% enclosed. Everything else is a path beside buildings.
2. **Both lanes are one-sided.** Each has buildings on its outer side and an 8 m wide strip of back court on its inner side. A walker sees fence, yard and the backs of the street row.
3. **The bazaar is a field with two halls in it.** Its 44 x 26 m plaza has 16% of its 140 m perimeter enclosed and no shopfront facing it at all. The halls define the middle, nothing defines the edge.
4. **Arrival has no walls.** The 20 x 16 m court has two open lodges and nothing on either side, so the town begins 10 m further north, at the first shophouses.
5. **The secondary destinations are detached.** The warehouse stands behind a back court; the tea house is 18 m beyond the plaza edge at the end of a path with no building on it; the two court buildings face each other across 36 m.
6. **There is one route.** The street has no side opening in its 26 m length. The walking graph has 9 loops, but most are inside the bazaar; to go from the street to either lane the player must return to the arrival court or reach the bazaar.

## Camera

In P1.2, 48 of 76 travel directions were fully clear in the ray test. The severe cases (camera under 2 m) were all the same kind: walking
away from a door or out from under a roof (tea-house veranda 0.9 m, court corner houses 1.1 m). Those are addressed in 08; they are a property of
entering and leaving buildings, not of the layout, and they cannot be removed by layout alone.

## What follows from this

The defects are of form, not of dressing: fill the back courts or move the lanes onto them, give the bazaar and the arrival court edges, open the
street sideways, and bring the warehouse and tea house inside the cluster. Three ways of doing that are tested in 02.
