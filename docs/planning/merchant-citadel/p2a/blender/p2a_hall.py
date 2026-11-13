"""Exchange Hall (archetype A01) split into reusable architectural modules for the production kit (P2-B batch 1).

The P1.4 A01 archetype is one list of parts (main hall, tower, two wings, porch) plus extras. The podium floor and the stairs among the
extras already live in the PODIUM node and are excluded here. Each module keeps the hall's local origin, so every module is placed at
the same transform and the hall is assembled exactly as in the P1.4 Blender world.
"""
HALL_NODES = ("A01_main", "A01_wing_w", "A01_wing_e", "A01_porch", "A01_tower")


def hall_modules(a01):
    parts = {p["id"]: p for p in a01["parts"]}
    keep = [e for e in a01["extras"] if not e["asset"].startswith(("MV-Floor_Brick", "MV-Stairs_"))]
    seals = [e for e in keep if e["asset"].startswith("CUS-Seal")]
    tower_seals = [e for e in seals if e["pos"][2] > 10]
    porch_seals = [e for e in seals if e["pos"][2] <= 10]
    main_extras = [e for e in keep if e["asset"].startswith(("MV-Roof_Dormer", "FP-Banner", "FP-Lantern"))]
    return {
        "A01_main": {"parts": [parts["main"]], "extras": main_extras},
        "A01_wing_w": {"parts": [parts["wing_w"]], "extras": []},
        "A01_wing_e": {"parts": [parts["wing_e"]], "extras": []},
        "A01_porch": {"parts": [parts["porch"]], "extras": porch_seals},
        "A01_tower": {"parts": [parts["tower"]], "extras": tower_seals},
    }
