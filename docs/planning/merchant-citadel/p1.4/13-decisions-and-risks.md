# 13 - Remaining design decisions and risks (P1.4)

## Decisions for the owner

1. **P1.4 against P1.3.** Both are complete and separate; either can go forward.
2. **The level change.** A raised terrace is the largest single change. It adds steps to the primary route and a vertical demand on the island (11).
3. **Custom cloth.** Awnings, pennants and the paving seal are authored, not downloaded. They carry much of the atmosphere; without them the bazaar keeps its form but loses colour.
4. **Straight or bent street.** D is selected; E (bent) is measured in 04 and would need a further pass.
5. **Carried over, still open:** the P1.2 look (seal, burgundy and blue, sign pictograms), the Syntaxes of Play and Avramania sources, a triangle and draw-call budget.
6. **Authorisation to start P2.** Not assumed.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Triangle load (968,466; +6% on P1.3) | Medium to high | Substitutions project 532,062; measure early; turrets and the inn are the first things to simplify |
| Camera clear on fewer directions (35 of 84) | Medium | Decide whether cloth and pennants are in the camera collision set; adjust the inn balcony; engine test |
| Steps on the primary route | Low to medium | Five risers of about 0.2 m, as on the hall steps already validated; engine test; a ramp proxy is possible |
| Custom cloth looks flat beside painted textures | Medium | Woven texture and vertex-colour stripes in P2 |
| References not located (R02, R03, R05, R08, R09) | Certain | Their principles came from the brief's text; if the owner supplies links, the board can be completed |
| Alefran-like packs tempting later | Low | Licence recorded in 03; do not adopt without written permission from the creator |
| Hall still made of house modules | Certain | Accept, or commission a small custom civic module set |
| Secondary quarters least improved | Certain | A distinct workshop type in a later pass |

## Not verified

Nothing was loaded in Three.js. Appearance, collision, camera and performance in the game are untested. The massing metrics for E are from boxes, not assets.

## Scope confirmation

No production town implementation, island terrain, Three.js change, first-island asset reuse, gameplay system, GLB export, deployment or commit. One pack was downloaded for inspection and not adopted.

**MERCHANT CITADEL P1.4 - PENDING HUMAN VISUAL APPROVAL. STOP.**
