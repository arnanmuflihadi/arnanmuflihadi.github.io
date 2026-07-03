# Vehicle Model Sources

These models are local copies of Quaternius CC0 transport assets used by the close-zoom Three.js
`vehicles-model-layer`.

## Sources

- Quaternius Public Transport Pack: https://quaternius.com/packs/publictransport.html
  - Author: Quaternius
  - License: CC0
  - Date accessed: 2026-06-29
  - Local files: `quaternius/public-transport/Bus.obj`, `Bus.mtl`, `Train.obj`, `Train.mtl`
  - Used for: TransJakarta bus models and MRT/KRL repeated train consists.
- Quaternius Modular Train Pack: https://quaternius.com/packs/modulartrain.html
  - Author: Quaternius
  - License: CC0
  - Date accessed: 2026-06-29
  - Local files: `quaternius/modular-train/HighSpeed_Front.obj`, `HighSpeed_Front.mtl`,
    `HighSpeed_Wagon.obj`, `HighSpeed_Wagon.mtl`
  - Used for: LRT Jakarta, LRT Jabodebek, and airport rail front-and-wagon consists.
  - Local files: `Locomotive_Front.*` and `Locomotive_PassengerWagon.*` are retained as alternate
    rail assets for future tuning.

Both source pages list the license as CC0 and describe the assets as free for personal and commercial
projects. Refresh with:

```bash
python scripts/download_vehicle_models.py
```
