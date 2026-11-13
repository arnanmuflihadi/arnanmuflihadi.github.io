#!/bin/bash
# Batch 2 rebuild: island meshes (no procedural vegetation) -> runtime grids -> third-party flora library -> scatter and habitats. Run from the repository root.
# Needs: Blender, python3 (numpy, scipy, Pillow), and the Quaternius Stylized Nature MegaKit Standard unzipped at $NATURE (see 06-assets-and-licences).
set -euo pipefail
B1=docs/planning/merchant-citadel/p3b-batch1/source; B2=docs/planning/merchant-citadel/p3b-batch2/source; WORK=${1:-.asset-inspection/merchant-citadel-p1/p3b2/build}; EV=docs/planning/merchant-citadel/p3b-batch2/evidence
NATURE=${NATURE:-.asset-inspection/merchant-citadel-p1/p3b2/quaternius/nature-standard}; mkdir -p "$WORK" "$EV"
BL=/Applications/Blender.app/Contents/MacOS/Blender
$BL --background --python $B1/p3b_blender_build.py -- "$WORK" --scene merchant-citadel-p2a/data/scene.json --no-veg
python3 $B1/p3b_export_runtime.py "$WORK/runtime" "$WORK/top-mesh.npz" "$EV/terrain"
cp "$WORK/runtime/island-terrain.json" "$WORK/runtime/island-terrain.bin" "$WORK/runtime/island-mask.bin" "$WORK/island-instances.json" merchant-citadel-p2a/data/
cp "$WORK/merchant-citadel-p3b-island.glb" merchant-citadel-p2a/models/
python3 $B2/p3b2_prepare_flora.py "$NATURE" "$WORK/flora-src"
$BL --background --python $B2/p3b2_flora_build.py -- "$WORK/flora-src" merchant-citadel-p2a/assets-p3b2/flora.glb
python3 $B2/p3b2_scatter.py merchant-citadel-p2a/data/scene.json merchant-citadel-p2a/data/island-flora.json "$EV"
echo "batch 2 data updated"
