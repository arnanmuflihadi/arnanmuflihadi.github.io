# 10 - Terrain interface contract (P1.2; no island is modelled)

Sequence: approve town, construct buildings, assemble town, derive the terrain envelope, sculpt the island around the settlement.

## Measured requirements

| Requirement | Value |
|---|---|
| Developed envelope (paving and nominal footprints) | x -28.5..46, z -90..8 (74.5 x 98 m) |
| Future transport reservation | x -10..10, z 8..24 (20 x 16 m), level, joined to node N01 |
| **Combined footprint the terrain must carry** | x -28.5..46, z -90..24 (**74.5 x 114 m**) |
| Largest measured building envelope beyond the developed envelope | Roofs overhang wall lines by 0.8-1.1 m; the furthest any measured envelope reaches outside the developed envelope is 0.94 m |
| Base elevation | y = 0.0 for every street, court, lane, building floor and the reservation |
| Only raised surface | Exchange Hall podium, y = +1.0, x -14..14, z -90..-74 |
| Building foundation zones | The 17 measured envelopes in 07; each needs a level pad at y = 0 |
| Lookout orientation | Terrace faces east (+x); fence line x = 46 and z = -44 |
| Surface treatments | Packed earth in the two back courts (x -18..-10 and 10..18, z -36..-10): a terrain material, not geometry |

**Unchanged in P1.2** (no footprint moved; jetties and the porch stay inside the P1.1 envelope). **Correction made in P1.1:** the P1.0 support zone was drawn around the developed envelope only (94.5 x 118 m) and left the southern half of the transport
reservation outside it. The zone below includes the reservation.

## Assumptions (to confirm in P4)

| Assumption | Value |
|---|---|
| Terrain support zone | Combined footprint plus 10 m on every side: **94.5 x 134 m** of buildable, near-level ground (x -38.5..56, z -100..34) |
| Cliff exclusion | No cliff edge, drop or waterfall inside the support zone, except beside the lookout |
| Lookout exception | The island edge may come to about 3 m east and south of the terrace fence |
| Arrival side | If the transport pad becomes a landing or dock, the island edge may meet its south side; that replaces the 10 m margin there |
| Likely island size | About 115 x 155 m or larger; silhouette not fixed |

Not created: island mesh, cliffs, waterfalls, underside, terrain export.
