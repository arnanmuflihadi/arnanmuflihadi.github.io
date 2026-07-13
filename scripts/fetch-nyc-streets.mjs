import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const output = path.join(root, "assets", "data", "home", "nyc-streets.geojson");
const service = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/ArcGIS/rest/services/DCM_Street_Center_Line/FeatureServer/0/query";
const pageSize = 2000;
const bbox = [-74.04, 40.67, -73.9, 40.88];

const features = [];
for (let offset = 0; ; offset += pageSize) {
  const params = new URLSearchParams({
    where: "1=1",
    geometry: bbox.join(","),
    geometryType: "esriGeometryEnvelope",
    inSR: "4326",
    outSR: "4326",
    spatialRel: "esriSpatialRelIntersects",
    outFields: "OBJECTID,Borough,Street_NM,Route_Type",
    returnGeometry: "true",
    geometryPrecision: "5",
    maxAllowableOffset: "0.00002",
    resultOffset: String(offset),
    resultRecordCount: String(pageSize),
    orderByFields: "OBJECTID",
    f: "geojson",
  });
  const response = await fetch(`${service}?${params}`);
  if (!response.ok) throw new Error(`NYC street request failed: ${response.status} ${response.statusText}`);
  const page = await response.json();
  if (!Array.isArray(page.features)) throw new Error(`NYC street request returned no features at offset ${offset}`);
  features.push(...page.features.filter((feature) => feature.geometry));
  process.stdout.write(`Fetched ${features.length} NYC street segments\r`);
  if (page.features.length < pageSize) break;
}

if (features.length < 5000) throw new Error(`Expected a dense New York street field; received only ${features.length} features`);

await mkdir(path.dirname(output), { recursive: true });
await writeFile(output, JSON.stringify({
  type: "FeatureCollection",
  name: "NYC Digital City Map street centerlines — Manhattan and inner boroughs",
  source: "NYC Department of City Planning, Digital City Map (DCM) Street Center Line",
  source_url: "https://www.nyc.gov/content/planning/pages/resources/datasets/digital-city-map",
  service_url: service,
  bbox,
  features,
}));
process.stdout.write(`\nSaved ${features.length} street segments to ${path.relative(root, output)}\n`);
