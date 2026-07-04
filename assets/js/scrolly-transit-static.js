/* ============================================================
   Transit case-study scrollytelling: data-driven SVG layers
   ============================================================ */
(function () {
  "use strict";

  var DATA_VERSION = "?v=7";
  var NS = "http://www.w3.org/2000/svg";
  var MAP_W = 1000;
  var MAP_H = 720;
  var MAP_PAD = 76;

  var scrolly = document.querySelector("[data-transit-scrolly]");
  if (!scrolly) return;

  var stage = scrolly.querySelector(".scrolly-static-stage");
  var steps = Array.prototype.slice.call(scrolly.querySelectorAll("[data-scrolly-step]"));
  var note = scrolly.querySelector("[data-scrolly-note]");
  var kicker = scrolly.querySelector("[data-scrolly-kicker]");
  var caption = scrolly.querySelector("[data-scrolly-legend]");
  var progress = scrolly.querySelector("[data-scrolly-progress]");
  var mapRoot = scrolly.querySelector("[data-transit-data-map]");
  var status = scrolly.querySelector("[data-map-status]");
  var summaryBox = scrolly.querySelector("[data-map-summary]");
  var legendBox = scrolly.querySelector("[data-map-legend]");
  var clipRect = scrolly.querySelector("[data-compare-clip]");
  var labelLayer = scrolly.querySelector("[data-map-labels]");
  var layerNodes = {};

  Array.prototype.forEach.call(scrolly.querySelectorAll("[data-map-layer]"), function (node) {
    layerNodes[node.getAttribute("data-map-layer")] = node;
  });

  if (!stage || !steps.length || !mapRoot || !labelLayer) return;

  var activeIndex = -1;
  var activeTarget = "overview";
  var ticking = false;
  var mapReady = false;
  var mapFeatures = [];
  var recordsByName = {};
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function setText(el, value) {
    if (el && value && el.textContent !== value) el.textContent = value;
  }

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"]/g, function (m) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;"}[m];
    });
  }

  function fmt(value, digits) {
    return Number(value).toLocaleString("en-US", {
      minimumFractionDigits: digits == null ? 2 : digits,
      maximumFractionDigits: digits == null ? 2 : digits
    });
  }

  function key(parts) {
    return parts.map(function (value) {
      return String(value || "").trim().toUpperCase();
    }).join("|");
  }

  function nameKey(value) {
    return String(value || "").trim().toUpperCase().replace(/[^A-Z0-9]/g, "");
  }

  function eachRing(geometry, callback) {
    if (!geometry) return;
    if (geometry.type === "Polygon") {
      geometry.coordinates.forEach(callback);
      return;
    }
    if (geometry.type === "MultiPolygon") {
      geometry.coordinates.forEach(function (poly) {
        poly.forEach(callback);
      });
    }
  }

  function geometryBounds(features) {
    var minX = Infinity;
    var minY = Infinity;
    var maxX = -Infinity;
    var maxY = -Infinity;
    features.forEach(function (feature) {
      eachRing(feature.geometry, function (ring) {
        ring.forEach(function (coord) {
          minX = Math.min(minX, coord[0]);
          maxX = Math.max(maxX, coord[0]);
          minY = Math.min(minY, coord[1]);
          maxY = Math.max(maxY, coord[1]);
        });
      });
    });
    return {minX: minX, minY: minY, maxX: maxX, maxY: maxY};
  }

  function createProjection(bounds) {
    var scale = Math.min(
      (MAP_W - MAP_PAD * 2) / Math.max(bounds.maxX - bounds.minX, 0.0001),
      (MAP_H - MAP_PAD * 2) / Math.max(bounds.maxY - bounds.minY, 0.0001)
    );
    var mapWidth = (bounds.maxX - bounds.minX) * scale;
    var mapHeight = (bounds.maxY - bounds.minY) * scale;
    var offsetX = (MAP_W - mapWidth) / 2;
    var offsetY = (MAP_H - mapHeight) / 2;

    return function project(coord) {
      return [
        offsetX + (coord[0] - bounds.minX) * scale,
        offsetY + (bounds.maxY - coord[1]) * scale
      ];
    };
  }

  function pathFromGeometry(geometry, project) {
    var d = "";
    eachRing(geometry, function (ring) {
      ring.forEach(function (coord, index) {
        var p = project(coord);
        d += (index ? "L" : "M") + p[0].toFixed(2) + " " + p[1].toFixed(2);
      });
      d += "Z";
    });
    return d;
  }

  function centroidFromPathBounds(feature) {
    return {
      x: (feature.bounds.minX + feature.bounds.maxX) / 2,
      y: (feature.bounds.minY + feature.bounds.maxY) / 2
    };
  }

  function projectedBounds(geometry, project) {
    var minX = Infinity;
    var minY = Infinity;
    var maxX = -Infinity;
    var maxY = -Infinity;
    eachRing(geometry, function (ring) {
      ring.forEach(function (coord) {
        var p = project(coord);
        minX = Math.min(minX, p[0]);
        maxX = Math.max(maxX, p[0]);
        minY = Math.min(minY, p[1]);
        maxY = Math.max(maxY, p[1]);
      });
    });
    return {minX: minX, minY: minY, maxX: maxX, maxY: maxY};
  }

  function scoreColor(value) {
    if (value == null || Number.isNaN(Number(value))) return "#2f3331";
    var v = Number(value);
    if (v < 10) return "#efe7cf";
    if (v < 20) return "#d8dba2";
    if (v < 40) return "#9fc78f";
    if (v < 60) return "#4f9a8b";
    if (v < 75) return "#1f6678";
    return "#12364f";
  }

  function deltaColor(value) {
    if (value == null || Number.isNaN(Number(value))) return "#2f3331";
    var v = Number(value);
    if (v < 2) return "#f1ecd0";
    if (v < 5) return "#cfe7b5";
    if (v < 10) return "#85c98d";
    if (v < 15) return "#3b9e78";
    return "#0f6655";
  }

  function categoryColor(value) {
    return {
      "Sangat Rendah": "#d7191c",
      "Rendah": "#fdae61",
      "Sedang": "#ffffbf",
      "Tinggi": "#a6d96a",
      "Sangat Tinggi": "#1a9641"
    }[value] || "#3a3f3f";
  }

  function hotspotColor(value) {
    return {
      "Hot Spot 99%": "#a50026",
      "Hot Spot 95%": "#f46d43",
      "Tidak Signifikan": "#f0f0f0",
      "Cold Spot 95%": "#74add1",
      "Cold Spot 99%": "#313695"
    }[value] || "#f0f0f0";
  }

  function createPath(feature, fill, className) {
    var path = document.createElementNS(NS, "path");
    path.setAttribute("d", feature.path);
    path.setAttribute("class", className || "transit-map-path");
    path.setAttribute("fill", fill);
    path.setAttribute("fill-rule", "evenodd");
    path.setAttribute("data-name", feature.record.kelurahan);

    var title = document.createElementNS(NS, "title");
    title.textContent = feature.record.kelurahan + " · A " + fmt(feature.record.skor_A) +
      " · B " + fmt(feature.record.skor_B) + " · delta " + fmt(feature.record.delta);
    path.appendChild(title);
    return path;
  }

  function appendLayer(name, fillFn, opacityFn) {
    var layer = layerNodes[name];
    if (!layer) return;
    layer.textContent = "";
    mapFeatures.forEach(function (feature) {
      var path = createPath(feature, fillFn(feature), "transit-map-path");
      if (opacityFn) path.setAttribute("opacity", opacityFn(feature));
      layer.appendChild(path);
    });
  }

  function renderOutline() {
    var outline = scrolly.querySelector("[data-map-outline]");
    if (!outline) return;
    outline.textContent = "";
    mapFeatures.forEach(function (feature) {
      outline.appendChild(createPath(feature, "none", "transit-map-path"));
    });
  }

  function renderMapLayers() {
    appendLayer("overview", function (feature) { return scoreColor(feature.record.skor_B); }, function () { return 0.92; });
    appendLayer("scenario-a", function (feature) { return scoreColor(feature.record.skor_A); });
    appendLayer("scenario-b", function (feature) { return scoreColor(feature.record.skor_B); });
    appendLayer("delta", function (feature) { return deltaColor(feature.record.delta); });
    appendLayer("categories", function (feature) { return categoryColor(feature.record.kat_B); });
    appendLayer("hotspot", function (feature) { return hotspotColor(feature.record.hs_skor_B); }, function (feature) {
      return feature.record.hs_skor_B === "Tidak Signifikan" ? 0.38 : 1;
    });
    appendLayer("compare-a", function (feature) { return scoreColor(feature.record.skor_A); });
    appendLayer("compare-b", function (feature) { return scoreColor(feature.record.skor_B); });
    renderOutline();
  }

  function labelRecord(name, kecamatan) {
    var prefix = String(name || "").toUpperCase();
    var kec = kecamatan ? String(kecamatan).toUpperCase() : "";
    var match = mapFeatures.find(function (feature) {
      return nameKey(feature.record.kelurahan) === nameKey(prefix) && (!kec || feature.record.kecamatan === kec);
    });
    return match || null;
  }

  function stateLabels(target) {
    if (target === "scenario-a") {
      return [
        {name: "KARET SEMANGGI", text: "Highest baseline", sub: "73.62"},
        {name: "ROROTAN", text: "Low periphery", sub: "1.43"}
      ];
    }
    if (target === "scenario-b" || target === "overview") {
      return [
        {name: "PETAMBURAN", text: "Highest access", sub: "84.23"},
        {name: "PONDOK RANGGON", text: "Lowest access", sub: "2.47"}
      ];
    }
    if (target === "delta" || target === "compare") {
      return [
        {name: "SUKABUMI UTARA", text: "Largest uplift", sub: "+32.83"}
      ];
    }
    if (target === "hotspot") {
      return [
        {name: "PETAMBURAN", text: "Hot Spot 99%", sub: "84.23"},
        {name: "KARET SEMANGGI", text: "Hot Spot 99%", sub: "80.47"},
        {name: "PONDOK RANGGON", text: "Cold Spot 99%", sub: "2.47"}
      ];
    }
    if (target === "synthesis") {
      return [
        {name: "PETAMBURAN", text: "Ceiling", sub: "84.23"},
        {name: "PONDOK RANGGON", text: "Floor", sub: "2.47"},
        {name: "SUKABUMI UTARA", text: "Max gain", sub: "+32.83"}
      ];
    }
    return [];
  }

  function renderLabels(target) {
    if (!mapReady) return;
    labelLayer.textContent = "";

    stateLabels(target).forEach(function (label, index) {
      var feature = labelRecord(label.name);
      if (!feature) return;
      var c = centroidFromPathBounds(feature);
      var anchorRight = c.x > MAP_W * 0.55;
      var dx = anchorRight ? -20 : 20;
      var dy = index % 2 ? 18 : -16;
      var textX = c.x + dx;
      var textY = c.y + dy;
      var g = document.createElementNS(NS, "g");
      g.setAttribute("class", "transit-map-label");

      var line = document.createElementNS(NS, "line");
      line.setAttribute("x1", c.x.toFixed(2));
      line.setAttribute("y1", c.y.toFixed(2));
      line.setAttribute("x2", textX.toFixed(2));
      line.setAttribute("y2", textY.toFixed(2));
      g.appendChild(line);

      var dot = document.createElementNS(NS, "circle");
      dot.setAttribute("cx", c.x.toFixed(2));
      dot.setAttribute("cy", c.y.toFixed(2));
      dot.setAttribute("r", "5.5");
      g.appendChild(dot);

      var text = document.createElementNS(NS, "text");
      text.setAttribute("x", textX.toFixed(2));
      text.setAttribute("y", textY.toFixed(2));
      text.setAttribute("text-anchor", anchorRight ? "end" : "start");
      text.textContent = label.text;
      var sub = document.createElementNS(NS, "tspan");
      sub.setAttribute("x", textX.toFixed(2));
      sub.setAttribute("dy", "16");
      sub.textContent = label.sub + " · " + label.name;
      text.appendChild(sub);
      g.appendChild(text);
      labelLayer.appendChild(g);
    });
  }

  function legendRows(title, rows) {
    return "<b>" + esc(title) + "</b>" + rows.map(function (row) {
      return "<div class=\"scrolly-map-legend__row\"><span class=\"scrolly-map-legend__swatch\" style=\"background:" +
        row[0] + "\"></span>" + esc(row[1]) + "</div>";
    }).join("");
  }

  function updateLegend(target) {
    if (!legendBox) return;
    if (target === "delta" || target === "compare") {
      legendBox.innerHTML = legendRows("Delta B - A", [
        ["#f1ecd0", "0-2 points"],
        ["#cfe7b5", "2-5"],
        ["#85c98d", "5-10"],
        ["#3b9e78", "10-15"],
        ["#0f6655", "15+"]
      ]);
      return;
    }
    if (target === "categories") {
      legendBox.innerHTML = legendRows("Scenario B category", [
        ["#d7191c", "Sangat Rendah"],
        ["#fdae61", "Rendah"],
        ["#ffffbf", "Sedang"],
        ["#a6d96a", "Tinggi"],
        ["#1a9641", "Sangat Tinggi"]
      ]);
      return;
    }
    if (target === "hotspot") {
      legendBox.innerHTML = legendRows("Getis-Ord Gi*", [
        ["#a50026", "Hot Spot 99%"],
        ["#f46d43", "Hot Spot 95%"],
        ["#f0f0f0", "Not significant"],
        ["#74add1", "Cold Spot 95%"],
        ["#313695", "Cold Spot 99%"]
      ]);
      return;
    }
    legendBox.innerHTML = legendRows(target === "scenario-a" ? "Scenario A score" : "Scenario B score", [
      ["#efe7cf", "0-10"],
      ["#d8dba2", "10-20"],
      ["#9fc78f", "20-40"],
      ["#4f9a8b", "40-60"],
      ["#1f6678", "60-75"]
    ]);
  }

  function summaryHtml(target) {
    if (!mapFeatures.length) return "Joining score records to kelurahan geometry…";
    var s = mapFeatures.summary;
    if (target === "scenario-a") {
      return "<span class=\"metric\">mean " + fmt(s.mean_skor_A) + "</span><span class=\"metric\">median " +
        fmt(s.median_skor_A) + "</span><strong>Scenario A</strong> maps the backbone network before Mikrotrans feeders.";
    }
    if (target === "scenario-b" || target === "overview") {
      return "<span class=\"metric\">mean " + fmt(s.mean_skor_B) + "</span><span class=\"metric\">max " +
        fmt(s.max_skor_B) + "</span><strong>Scenario B</strong> adds the full Jaklingko/Mikrotrans network.";
    }
    if (target === "delta") {
      return "<span class=\"metric\">mean +" + fmt(s.mean_delta) + "</span><span class=\"metric\">max +" +
        fmt(s.max_delta) + "</span><strong>Sukabumi Utara</strong> records the strongest Mikrotrans gain.";
    }
    if (target === "categories") {
      return "<span class=\"metric\">32 leave Very Low</span><span class=\"metric\">3 Very High</span>Scenario B remains dominated by low-access categories despite the feeder uplift.";
    }
    if (target === "hotspot") {
      return "<span class=\"metric\">75 Hot Spots</span><span class=\"metric\">77 Cold Spots</span>Getis-Ord Gi* confirms a broad core-periphery cluster pattern.";
    }
    if (target === "compare") {
      return "<span class=\"metric\">A mean " + fmt(s.mean_skor_A) + "</span><span class=\"metric\">B mean " +
        fmt(s.mean_skor_B) + "</span>The split view compares both score surfaces with identical geometry.";
    }
    return "<span class=\"metric\">34x gap</span><span class=\"metric\">rho 0.92-0.98</span>The final layer highlights the accessibility ceiling, floor, and strongest feeder gain.";
  }

  function setMapState(target) {
    activeTarget = target || "overview";
    if (mapRoot) mapRoot.setAttribute("data-map-state", activeTarget);

    Object.keys(layerNodes).forEach(function (name) {
      var on = name === activeTarget;
      if (activeTarget === "overview") on = name === "overview";
      if (activeTarget === "synthesis") on = name === "scenario-b";
      if (activeTarget === "compare") on = name === "compare-a" || name === "compare-b";
      layerNodes[name].classList.toggle("is-active", on);
    });

    if (summaryBox) summaryBox.innerHTML = summaryHtml(activeTarget);
    updateLegend(activeTarget);
    renderLabels(activeTarget);
  }

  function setActive(index) {
    index = clamp(index, 0, steps.length - 1);
    var step = steps[index];
    var target = step.getAttribute("data-layer-target") || "overview";
    var state = step.getAttribute("data-state") || target;

    if (index !== activeIndex) {
      activeIndex = index;
      steps.forEach(function (item, i) {
        item.classList.toggle("active", i === index);
        if (i === index) item.setAttribute("aria-current", "step");
        else item.removeAttribute("aria-current");
      });
      scrolly.setAttribute("data-state", state);
      setText(note, step.getAttribute("data-note"));
      setText(kicker, step.getAttribute("data-kicker"));
      setText(caption, step.getAttribute("data-legend"));
      if (progress) progress.style.width = (((index + 1) / steps.length) * 100).toFixed(2) + "%";
      setMapState(target);
    }

    stage.style.setProperty("--scrolly-scale", reduceMotion ? "1" : (step.getAttribute("data-scale") || "1"));
    stage.style.setProperty("--scrolly-pan-x", reduceMotion ? "0%" : (step.getAttribute("data-pan-x") || "0%"));
    stage.style.setProperty("--scrolly-pan-y", reduceMotion ? "0%" : (step.getAttribute("data-pan-y") || "0%"));
  }

  function closestStepIndex() {
    var viewport = window.innerHeight || document.documentElement.clientHeight;
    var anchor = viewport * 0.46;
    var best = 0;
    var bestDistance = Infinity;

    steps.forEach(function (step, i) {
      var rect = step.getBoundingClientRect();
      var focusLine = rect.top + rect.height * 0.38;
      var distance = Math.abs(focusLine - anchor);
      if (distance < bestDistance) {
        bestDistance = distance;
        best = i;
      }
    });

    return best;
  }

  function updateCompareSplit(index) {
    var step = steps[index];
    var target = step.getAttribute("data-layer-target");
    if (target !== "compare") {
      stage.style.setProperty("--split", step.getAttribute("data-split") || "50%");
      if (clipRect) {
        clipRect.setAttribute("x", MAP_W * 0.5);
        clipRect.setAttribute("width", MAP_W * 0.5);
      }
      return;
    }

    var rect = step.getBoundingClientRect();
    var viewport = window.innerHeight || document.documentElement.clientHeight;
    var local = clamp((viewport * 0.72 - rect.top) / (rect.height + viewport * 0.25), 0, 1);
    var split = 34 + local * 42;
    var splitX = MAP_W * split / 100;
    stage.style.setProperty("--split", split.toFixed(1) + "%");
    if (clipRect) {
      clipRect.setAttribute("x", splitX.toFixed(2));
      clipRect.setAttribute("width", (MAP_W - splitX).toFixed(2));
    }
  }

  function update() {
    ticking = false;
    var index = closestStepIndex();
    setActive(index);
    updateCompareSplit(index);
  }

  function requestUpdate() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  async function loadMapData() {
    try {
      var base = "maps/data/transit/";
      var responses = await Promise.all([
        fetch(base + "kelurahan.geojson" + DATA_VERSION).then(function (r) { return r.json(); }),
        fetch(base + "kelurahan_accessibility_60m.json" + DATA_VERSION).then(function (r) { return r.json(); })
      ]);
      var kelurahan = responses[0];
      var accessibility = responses[1];
      var recordMap = new Map();
      accessibility.records.forEach(function (record) {
        recordMap.set(key([record.kelurahan, record.kecamatan, record.kotamadya]), record);
        [record.kelurahan, record.kelurahan_source].concat(record.aliases || []).forEach(function (name) {
          if (name) recordMap.set(nameKey(name), record);
        });
      });
      var project = createProjection(geometryBounds(kelurahan.features));

      mapFeatures = kelurahan.features.map(function (feature) {
        var p = feature.properties || {};
        var record = recordMap.get(key([p.kel, p.kec, p.kota])) || recordMap.get(nameKey(p.kel));
        if (!record) {
          record = {
            kelurahan: p.kel || "UNKNOWN",
            kecamatan: p.kec || "",
            kotamadya: p.kota || "",
            skor_A: null,
            skor_B: null,
            delta: null,
            kat_B: "",
            hs_skor_B: "",
            core_skor_B: ""
          };
        }
        return {
          geometry: feature.geometry,
          record: record,
          path: pathFromGeometry(feature.geometry, project),
          bounds: projectedBounds(feature.geometry, project)
        };
      });
      mapFeatures.summary = accessibility.summary;
      mapFeatures.forEach(function (feature) {
        recordsByName[feature.record.kelurahan] = feature;
      });

      renderMapLayers();
      mapReady = true;
      mapRoot.classList.add("is-ready");
      setMapState(activeTarget);
    } catch (error) {
      if (status) status.textContent = "The accessibility map data could not be loaded. Check the local data files and reload.";
      console.error("Transit scrolly data load failed", error);
    }
  }

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate);

  if (window.matchMedia) {
    var motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    var onMotionChange = function () {
      reduceMotion = motionQuery.matches;
      requestUpdate();
    };
    if (motionQuery.addEventListener) motionQuery.addEventListener("change", onMotionChange);
    else if (motionQuery.addListener) motionQuery.addListener(onMotionChange);
  }

  setActive(0);
  loadMapData();
  requestUpdate();
})();
