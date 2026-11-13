# 11 - Town-first terrain support contract (P1.4; no island is modelled)

| Requirement | P1.3 | P1.4 |
|---|---|---|
| Developed envelope | x -28.5..42, z -90..8 (70.5 x 98 m) | x -30.5..42, z -90.0..8 (**72.5 x 98 m**) |
| Transport reservation | x -10..10, z 8..24 | unchanged |
| Combined footprint | 70.5 x 114 m | **72.5 x 114 m** |
| Terrain support zone (combined + 10 m, assumption) | 90.5 x 134 m | **92.5 x 134 m** (x -40.5..52, z -100.0..34) |
| Base elevation | y = 0 | y = 0 |
| Raised surfaces | Hall podium +1.0 | **Civic terrace +1.0 (x -14..14, z -74..-62) and hall podium +2.0 (x -14..14, z -90..-74)** |
| How the raised surfaces are made | Town geometry | Either town geometry (as in the blockout) **or** a 1 m terrain step under the terrace and a 2 m step under the hall. To be decided in P4; the steps and skirt stay town geometry either way |
| Foundation zones | 22 | 24 measured envelopes (06) |
| Lookout | Terrace x 30..42, z -62..-52 | unchanged; tea house apron extends to z = -66 |

The 1 m level change is the first vertical demand the town makes on the island. If the terrain supplies it, the ground behind the hall (north) can stay at +1 or +2 and the plinth row is not needed.
No cliff, drop or waterfall inside the support zone except beside the lookout. Likely island size about 112 x 155 m or larger.

Not created: island mesh, cliffs, waterfalls, underside, terrain export.
