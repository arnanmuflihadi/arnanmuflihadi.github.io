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
  const leftGrid = [];
  const islandGrid = [];
  const rightGrid = [];
  for (let y = 34, index = 0; y < 1580; y += index % 6 === 0 ? 32 : 18, index += 1) {
    const major = index % 8 === 0;
    leftGrid.push(`<path d="M-30 ${y} C130 ${y - 18} 290 ${y + 20} 482 ${y - 8}" stroke-width="${major ? 1.8 : .58}" stroke-opacity="${major ? .64 : .28}"/>`);
    rightGrid.push(`<path d="M772 ${y + 14} C930 ${y - 28} 1060 ${y + 26} 1230 ${y - 10}" stroke-width="${major ? 1.8 : .58}" stroke-opacity="${major ? .64 : .27}"/>`);
  }
  for (let x = -20, index = 0; x < 500; x += index % 7 === 0 ? 31 : 18, index += 1) {
    const major = index % 9 === 0;
    leftGrid.push(`<path d="M${x} -20 C${x + 42} 390 ${x - 34} 790 ${x + 28} 1620" stroke-width="${major ? 1.7 : .58}" stroke-opacity="${major ? .62 : .27}"/>`);
  }
  for (let x = 770, index = 0; x < 1230; x += index % 6 === 0 ? 29 : 17, index += 1) {
    const major = index % 8 === 0;
    rightGrid.push(`<path d="M${x} -20 C${x - 48} 360 ${x + 36} 820 ${x - 24} 1620" stroke-width="${major ? 1.7 : .58}" stroke-opacity="${major ? .62 : .27}"/>`);
  }
  for (let y = 42, index = 0; y < 1570; y += index % 10 === 0 ? 30 : 15, index += 1) {
    islandGrid.push(`<path d="M500 ${y} C585 ${y - 9} 682 ${y + 10} 800 ${y - 4}" stroke-width="${index % 11 === 0 ? 1.7 : .66}" stroke-opacity="${index % 11 === 0 ? .76 : .38}"/>`);
  }
  for (let x = 536, index = 0; x < 790; x += 17, index += 1) {
    islandGrid.push(`<path d="M${x} 10 C${x - 34} 520 ${x + 30} 1040 ${x - 16} 1590" stroke-width="${index % 5 === 0 ? 1.8 : .7}" stroke-opacity="${index % 5 === 0 ? .72 : .38}"/>`);
  }
  const body = `    <defs>
      <clipPath id="west-bank"><path d="M-40 70L332 18L404 218L374 438L430 684L382 910L448 1170L392 1570L-40 1620Z"/></clipPath>
      <clipPath id="central-island"><path d="M638 24L754 12L748 248L774 464L752 698L786 930L748 1170L722 1514L612 1582L590 1370L612 1130L586 890L612 646L590 416L618 192Z"/></clipPath>
      <clipPath id="east-bank"><path d="M832 4H1240V1620H824L790 1390L832 1164L798 916L838 678L804 426L842 210Z"/></clipPath>
    </defs>
    <g clip-path="url(#west-bank)">
${leftGrid.map((street) => `      ${street}`).join("\n")}
      <path d="M54 1570C190 1320 94 1060 300 824S142 360 356 54" stroke-width="4" stroke-opacity=".82"/>
      <path d="M-20 1210C176 1120 246 1000 434 962M-12 610C144 566 294 520 404 418" stroke-width="2.8" stroke-opacity=".72"/>
    </g>
    <g clip-path="url(#central-island)">
${islandGrid.map((street) => `      ${street}`).join("\n")}
      <path d="M632 1570C700 1260 638 1070 730 848S654 386 724 26" stroke-width="4.4" stroke-opacity=".94"/>
      <path d="M600 1118L762 1038M600 760L768 704M604 356L760 304" stroke-width="2.4" stroke-opacity=".82"/>
    </g>
    <g clip-path="url(#east-bank)">
${rightGrid.map((street) => `      ${street}`).join("\n")}
      <path d="M890 1586C1018 1350 900 1110 1090 862S950 338 1172 64" stroke-width="4" stroke-opacity=".82"/>
      <path d="M804 1260C940 1190 1080 1178 1224 1080M804 540C948 474 1082 500 1222 390" stroke-width="2.8" stroke-opacity=".7"/>
    </g>
    <path d="M-40 70L332 18L404 218L374 438L430 684L382 910L448 1170L392 1570M638 24L754 12L748 248L774 464L752 698L786 930L748 1170L722 1514L612 1582M832 4L804 426L838 678L798 916L832 1164L790 1390L824 1620" stroke-width="1.8" stroke-opacity=".92"/>
    <path d="M392 318C472 304 548 290 614 278M414 520C488 504 550 488 604 470M430 684C498 666 550 652 608 636M382 910C482 892 540 876 588 852M448 1170C510 1150 558 1136 612 1118M774 464C820 448 862 432 914 416M786 930C834 914 880 900 936 884M748 1170C808 1154 862 1140 920 1118" stroke-width="3.2" stroke-opacity=".86"/>
    <g stroke-width=".9" stroke-opacity=".54">
      <path d="M596 310H568M596 342H560M602 520H570M604 552H564M590 886H556M594 918H550M612 1190H574M610 1222H566"/>
      <path d="M776 326H810M780 358H818M760 708H806M764 740H816M782 962H826M776 994H834"/>
    </g>`;
  await writeFile(path.join(outDir, "city-grid.svg"), svgDocument({
    title: "Abstract city street grid",
    description: "A monochrome vector street network inspired by dense coastal cities.",
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
