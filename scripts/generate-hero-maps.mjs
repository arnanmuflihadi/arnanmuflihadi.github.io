import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const outDir = path.join(root, "assets", "img", "maps");
await mkdir(outDir, { recursive: true });

const readJSON = async (relativePath) => JSON.parse(await readFile(path.join(root, relativePath), "utf8"));
const round = (value) => Number(value.toFixed(2));

function coordinatePairs(geometry, into = []) {
  if (!geometry) return into;
  const visit = (coordinates) => {
    if (!Array.isArray(coordinates)) return;
    if (typeof coordinates[0] === "number" && typeof coordinates[1] === "number") {
      into.push(coordinates);
      return;
    }
    coordinates.forEach(visit);
  };
  visit(geometry.coordinates);
  return into;
}

function boundsFor(features) {
  const pairs = features.flatMap((feature) => coordinatePairs(feature.geometry));
  return pairs.reduce(
    (bounds, [x, y]) => ({
      minX: Math.min(bounds.minX, x),
      minY: Math.min(bounds.minY, y),
      maxX: Math.max(bounds.maxX, x),
      maxY: Math.max(bounds.maxY, y),
    }),
    { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity },
  );
}

function projector(bounds, width = 1200, height = 720, padding = 54) {
  const dataWidth = Math.max(0.000001, bounds.maxX - bounds.minX);
  const dataHeight = Math.max(0.000001, bounds.maxY - bounds.minY);
  const scale = Math.min((width - padding * 2) / dataWidth, (height - padding * 2) / dataHeight);
  const offsetX = (width - dataWidth * scale) / 2;
  const offsetY = (height - dataHeight * scale) / 2;
  return ([x, y]) => [round(offsetX + (x - bounds.minX) * scale), round(height - offsetY - (y - bounds.minY) * scale)];
}

function simplifyRing(ring, maxPoints = 70) {
  if (ring.length <= maxPoints) return ring;
  const step = Math.ceil(ring.length / maxPoints);
  const simplified = ring.filter((_, index) => index % step === 0);
  simplified.push(ring[ring.length - 1]);
  return simplified;
}

function pathForRing(ring, project, close = true) {
  const points = simplifyRing(ring).map(project);
  if (!points.length) return "";
  return `M${points.map(([x, y]) => `${x},${y}`).join("L")}${close ? "Z" : ""}`;
}

function geometryPath(geometry, project) {
  if (!geometry) return "";
  if (geometry.type === "Polygon") return geometry.coordinates.map((ring) => pathForRing(ring, project)).join("");
  if (geometry.type === "MultiPolygon") {
    return geometry.coordinates.flatMap((polygon) => polygon.map((ring) => pathForRing(ring, project))).join("");
  }
  if (geometry.type === "LineString") return pathForRing(geometry.coordinates, project, false);
  if (geometry.type === "MultiLineString") return geometry.coordinates.map((line) => pathForRing(line, project, false)).join("");
  return "";
}

function svgDocument({ title, description, body, width = 1200, height = 720 }) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" color="#f4f4f2" role="img" aria-labelledby="title desc">
  <title id="title">${title}</title>
  <desc id="desc">${description}</desc>
  <g fill="none" stroke="currentColor" stroke-linecap="square" stroke-linejoin="round" vector-effect="non-scaling-stroke">
${body}
  </g>
</svg>
`;
}

function mapArtwork(features, options = {}) {
  const bounds = boundsFor(features);
  const project = projector(bounds);
  return features.map((feature, index) => {
    const d = geometryPath(feature.geometry, project);
    if (!d) return "";
    const filled = options.fillEvery && index % options.fillEvery === options.fillOffset;
    return `    <path d="${d}" stroke-width="${filled ? 1.35 : 0.8}" stroke-opacity="${filled ? 0.82 : 0.4}"${filled ? ' fill="currentColor" fill-opacity="0.055"' : ""}/>`;
  }).join("\n");
}

async function makeHomeCityGrid() {
  const nyc = await readJSON("assets/data/home/nyc-streets.geojson");
  const features = nyc.features.filter((feature) => feature.geometry);
  const project = projector(boundsFor(features), 1200, 1600, 38);
  const streets = features.map((feature) => {
    const route = feature.properties?.Route_Type || feature.properties?.route_type || "";
    const name = feature.properties?.Street_NM || feature.properties?.street_nm || "";
    const isBroadway = /broadway/i.test(name);
    const style = isBroadway ? [2.7, .92]
      : route === "Artrl" ? [2.35, .82]
        : route === "Mjr_st" ? [1.5, .66]
          : route === "Gen_use" ? [.58, .28]
            : [.76, .4];
    return `    <path d="${geometryPath(feature.geometry, project)}" stroke-width="${style[0]}" stroke-opacity="${style[1]}"/>`;
  }).join("\n");

  const labels = [
    ["MANHATTAN", [-73.982, 40.775]],
    ["BRONX", [-73.925, 40.85]],
    ["BROOKLYN", [-73.985, 40.687]],
    ["QUEENS", [-73.915, 40.735]],
  ].map(([label, coordinates]) => {
    const [x, y] = project(coordinates);
    return `    <text x="${x}" y="${y}" fill="currentColor" fill-opacity=".64" stroke="none" font-family="monospace" font-size="13" letter-spacing="3">${label}</text>`;
  }).join("\n");

  const body = `${streets}
    <g opacity=".72">${labels}</g>
    <path d="M38 52H180M1020 1548h142" stroke-width="2" stroke-opacity=".84"/>
    <text x="38" y="35" fill="currentColor" fill-opacity=".7" stroke="none" font-family="monospace" font-size="11" letter-spacing="2">NYC / 40.7128° N</text>
    <text x="930" y="1574" fill="currentColor" fill-opacity=".7" stroke="none" font-family="monospace" font-size="11" letter-spacing="2">74.0060° W</text>`;
  await writeFile(path.join(outDir, "city-grid.svg"), svgDocument({
    title: "New York City street map",
    description: "Official New York City street centerlines across Manhattan and the inner boroughs.",
    body,
    width: 1200,
    height: 1600,
  }));
}

async function makeProjectMaps() {
  const kelurahan = await readJSON("maps/data/transit/kelurahan.geojson");
  const transitLines = await readJSON("maps/data/transit/transit_lines.geojson");
  const transitFeatures = [...kelurahan.features, ...transitLines.features.filter((_, index) => index % 3 === 0)];
  const transitProject = projector(boundsFor(transitFeatures));
  const transitBoundaries = kelurahan.features.map((feature) => `    <path d="${geometryPath(feature.geometry, transitProject)}" stroke-width="0.7" stroke-opacity="0.34"/>`).join("\n");
  const transitRoutes = transitLines.features.filter((_, index) => index % 3 === 0).map((feature, index) => `    <path d="${geometryPath(feature.geometry, transitProject)}" stroke-width="${index % 5 === 0 ? 2.4 : 1.35}" stroke-opacity="${index % 5 === 0 ? 0.84 : 0.56}"/>`).join("\n");
  await writeFile(path.join(outDir, "hero-transit.svg"), svgDocument({
    title: "Jakarta transit field",
    description: "DKI Jakarta urban-village boundaries crossed by public-transit routes.",
    body: `${transitBoundaries}\n${transitRoutes}`,
  }));

  const panganAreas = await readJSON("maps/data/pangan/pangan_kabkota.geojson");
  const panganOD = await readJSON("maps/data/pangan/pangan_od.geojson");
  const panganFeatures = [...panganAreas.features, ...panganOD.features];
  const panganProject = projector(boundsFor(panganFeatures));
  const areaPaths = panganAreas.features.map((feature, index) => `    <path d="${geometryPath(feature.geometry, panganProject)}" stroke-width="${index % 4 === 0 ? 1.3 : 0.8}" stroke-opacity="${index % 4 === 0 ? 0.7 : 0.38}"${index % 6 === 0 ? ' fill="currentColor" fill-opacity="0.035"' : ""}/>`).join("\n");
  const odPaths = panganOD.features.filter((_, index) => index % 2 === 0).map((feature, index) => `    <path d="${geometryPath(feature.geometry, panganProject)}" stroke-width="${index % 9 === 0 ? 1.8 : 0.72}" stroke-opacity="${index % 9 === 0 ? 0.68 : 0.24}"/>`).join("\n");
  await writeFile(path.join(outDir, "hero-pangan.svg"), svgDocument({
    title: "West Java food network",
    description: "West Java administrative areas linked by origin-destination food flows.",
    body: `${areaPaths}\n${odPaths}`,
  }));

  await writeFile(path.join(outDir, "hero-mbr.svg"), svgDocument({
    title: "Jakarta housing morphology",
    description: "A monochrome urban morphology field derived from Jakarta urban-village boundaries.",
    body: mapArtwork(kelurahan.features, { fillEvery: 9, fillOffset: 2 }),
  }));

  const cbdRaw = await readJSON("assets/data/cbd/indonesia_cbd.json");
  const cbdRows = Array.isArray(cbdRaw) ? cbdRaw : (cbdRaw.data || cbdRaw.records || cbdRaw.features || []);
  const normalized = cbdRows.map((row) => row.properties ? { ...row.properties, ...(row.geometry?.coordinates ? { center_lon: row.geometry.coordinates[0], center_lat: row.geometry.coordinates[1] } : {}) } : row)
    .filter((row) => Number.isFinite(Number(row.center_lon ?? row.longitude ?? row.lon)) && Number.isFinite(Number(row.center_lat ?? row.latitude ?? row.lat)))
    .map((row) => ({
      lon: Number(row.center_lon ?? row.longitude ?? row.lon),
      lat: Number(row.center_lat ?? row.latitude ?? row.lat),
      size: Number(row.n_poi ?? row.poi_count ?? row.count ?? 1),
    }));
  const points = normalized.length ? normalized : [
    { lon: 95.3, lat: 5.5, size: 8 }, { lon: 106.8, lat: -6.2, size: 26 }, { lon: 112.7, lat: -7.3, size: 18 },
    { lon: 116.1, lat: -8.6, size: 7 }, { lon: 119.4, lat: -5.1, size: 10 }, { lon: 123.6, lat: -10.2, size: 5 }, { lon: 140.7, lat: -2.6, size: 4 },
  ];
  const cbdFeatures = points.map((point) => ({ geometry: { type: "Point", coordinates: [point.lon, point.lat] } }));
  const projectPoint = projector(boundsFor(cbdFeatures), 1200, 720, 70);
  const sorted = [...points].sort((a, b) => a.lon - b.lon);
  const network = sorted.slice(1).map((point, index) => {
    const previous = sorted[index];
    const [x1, y1] = projectPoint([previous.lon, previous.lat]);
    const [x2, y2] = projectPoint([point.lon, point.lat]);
    return `    <path d="M${x1},${y1}Q${round((x1 + x2) / 2)},${round(Math.min(y1, y2) - 22 - index % 4 * 9)} ${x2},${y2}" stroke-width="1.1" stroke-opacity="0.5"/>`;
  }).join("\n");
  const maxSize = Math.max(...points.map((point) => point.size), 1);
  const hubs = points.map((point, index) => {
    const [x, y] = projectPoint([point.lon, point.lat]);
    const radius = round(2.4 + Math.sqrt(Math.max(0, point.size) / maxSize) * 10);
    return `    <circle cx="${x}" cy="${y}" r="${radius}" stroke-width="${index % 7 === 0 ? 2 : 1.2}" stroke-opacity="${index % 7 === 0 ? 0.98 : 0.74}"${index % 7 === 0 ? ' fill="currentColor" fill-opacity="0.12"' : ""}/>`;
  }).join("\n");
  await writeFile(path.join(outDir, "hero-cbd.svg"), svgDocument({
    title: "Indonesia commercial-center network",
    description: "A monochrome network of commercial-center observations across Indonesia.",
    body: `${network}\n${hubs}`,
  }));
}

await makeHomeCityGrid();
await makeProjectMaps();
console.log(`Generated five vector map assets in ${path.relative(root, outDir)}`);
