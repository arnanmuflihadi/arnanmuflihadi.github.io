# 09 - Terrain interface contract (P1.3; no island is modelled)

| Requirement | P1.2 | P1.3 |
|---|---|---|
| Developed envelope | x -28.5..46, z -90..8 (74.5 x 98 m) | x -28.5..42, z -90..8 (**70.5 x 98 m**) |
| Future transport reservation | x -10..10, z 8..24 (20 x 16 m) | unchanged |
| Combined footprint the terrain must carry | 74.5 x 114 m | **70.5 x 114 m** |
| Terrain support zone (combined + 10 m each side, assumption) | 94.5 x 134 m | **90.5 x 134 m** (x -38.5..52, z -100..34) |
| Base elevation | y = 0 everywhere except the podium | unchanged |
| Only raised surface | Exchange Hall podium, y = +1.0, x -14..14, z -90..-74 | unchanged |
| Building foundation zones | 17 measured envelopes | 22 measured envelopes (05) |
| Lookout | Terrace x 34..46, z -54..-44, faces east | **Terrace x 30..42, z -62..-52**; fence on the east (x = 42) and south (z = -52) sides; faces east and south |
| Surface treatments (terrain material, not geometry) | Two back courts | Three packed-earth yards behind the street rows and the counting house |

The support zone is 4 m narrower than P1.2's and the same length. The lookout moved 4 m west and 8 m north, so the island edge that the terrace overlooks moves with it:
the edge may come to about 3 m east and south of the terrace fence. No cliff, drop or waterfall inside the support zone otherwise.
If the transport pad becomes a landing, the island edge may meet its south side. Likely island size: about 110 x 155 m or larger; silhouette not fixed.

Not created: island mesh, cliffs, waterfalls, underside, terrain export.
