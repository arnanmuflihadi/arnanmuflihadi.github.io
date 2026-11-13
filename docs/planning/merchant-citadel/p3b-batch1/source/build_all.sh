#!/bin/bash
# Rebuild the whole island pipeline: model -> Blender meshes/GLB -> runtime grids -> preview data. Run from the repository root.
#   bash docs/planning/merchant-citadel/p3b-batch1/source/build_all.sh [work_dir]
set -euo pipefail
SRC=docs/planning/merchant-citadel/p3b-batch1/source; WORK=${1:-.asset-inspection/merchant-citadel-p1/p3b/build}; EV=docs/planning/merchant-citadel/p3b-batch1/evidence
mkdir -p "$WORK" "$EV"
/Applications/Blender.app/Contents/MacOS/Blender --background --python $SRC/p3b_blender_build.py -- "$WORK" --scene merchant-citadel-p2a/data/scene.json
python3 $SRC/p3b_export_runtime.py "$WORK/runtime" "$WORK/top-mesh.npz" "$EV"
cp "$WORK/runtime/island-terrain.json" "$WORK/runtime/island-terrain.bin" "$WORK/runtime/island-mask.bin" "$WORK/island-instances.json" merchant-citadel-p2a/data/
cp "$WORK/merchant-citadel-p3b-island.glb" merchant-citadel-p2a/models/
cp "$WORK/island-build-stats.json" $EV/island-build-stats.json
echo "preview data updated"
