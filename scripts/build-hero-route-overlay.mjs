#!/usr/bin/env node
/* Deterministically projects the verified route 1 Blok M–Kota LineString. */
import { readFileSync, writeFileSync } from 'node:fs';
const source = JSON.parse(readFileSync(new URL('../maps/data/transit/transit_lines.geojson', import.meta.url)));
const matches = source.features.filter(({ properties: p }) => p.route === '1' && p.name === 'Blok M - Kota' && p.mode === 'BRT');
if (matches.length !== 2) throw new Error(`Expected two verified route segments; received ${matches.length}.`);
const line = matches.find((f) => f.geometry.coordinates[0][1] > f.geometry.coordinates.at(-1)[1]);
if (!line) throw new Error('Unable to choose the Blok M to Kota direction.');
const coords = line.geometry.coordinates;
const lonMin = 106.79, lonMax = 106.83, latMin = -6.25, latMax = -6.12;
const point = ([lon, lat]) => [((lon - lonMin) / (lonMax - lonMin) * 1000).toFixed(1), ((latMax - lat) / (latMax - latMin) * 700).toFixed(1)];
const pts = coords.map(point); const path = `M${pts.map((p, i) => `${i ? 'L' : ''}${p.join(' ')}`).join('')}`;
const stops = Array.from({ length: 12 }, (_, i) => pts[Math.round(i * (pts.length - 1) / 11)]);
const symbols = stops.map((p, i) => `<g id="stop-${String(i + 1).padStart(2, '0')}"><circle cx="${p[0]}" cy="${p[1]}" r="7"/></g>`).join('');
writeFileSync(new URL('../assets/img/maps/hero-transit-route-1-overlay.svg', import.meta.url), `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700"><defs><path id="route-1-blok-m-kota" d="${path}" fill="none" stroke="#a83f37" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>${symbols}</defs></svg>\n`);
