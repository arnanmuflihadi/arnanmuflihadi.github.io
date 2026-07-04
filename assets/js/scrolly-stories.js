/* ============================================================
   Case-study data stories — Pangan, MBR, CBD
   GitHub Pages-safe vanilla JS, no build step
   ============================================================ */
(function () {
  "use strict";

  var SVG_NS = "http://www.w3.org/2000/svg";

  function $(selector, root) {
    return (root || document).querySelector(selector);
  }

  function $$(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  function svgEl(name, attrs) {
    var el = document.createElementNS(SVG_NS, name);
    Object.keys(attrs || {}).forEach(function (key) {
      el.setAttribute(key, attrs[key]);
    });
    return el;
  }

  function setText(root, selector, value) {
    var el = $(selector, root);
    if (el) el.textContent = value || "";
  }

  function formatNumber(value, digits) {
    var n = Number(value);
    if (!isFinite(n)) return String(value || "");
    return n.toLocaleString("en-US", {
      maximumFractionDigits: digits == null ? 0 : digits
    });
  }

  function fetchJson(url) {
    return fetch(url).then(function (res) {
      if (!res.ok) throw new Error("Failed to load " + url + " (" + res.status + ")");
      return res.json();
    });
  }

  function bindStory(root, onActive) {
    var steps = $$(".story-step", root);
    var progress = $("[data-story-progress]", root);
    var dots = [];
    var active = -1;

    if (progress && steps.length) {
      steps.forEach(function () {
        var dot = document.createElement("span");
        progress.appendChild(dot);
        dots.push(dot);
      });
    }

    function activate(index) {
      if (index < 0 || index >= steps.length || index === active) return;
      active = index;
      steps.forEach(function (step, i) {
        step.classList.toggle("is-active", i === index);
      });
      dots.forEach(function (dot, i) {
        dot.classList.toggle("is-active", i === index);
        dot.classList.toggle("is-done", i < index);
      });
      onActive(steps[index], index);
    }

    activate(0);

    if ("IntersectionObserver" in window && steps.length) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) activate(steps.indexOf(entry.target));
        });
      }, { threshold: 0, rootMargin: "-38% 0px -38% 0px" });
      steps.forEach(function (step) { io.observe(step); });
    }

    return {
      activate: activate,
      getActiveStep: function () { return steps[active] || steps[0]; }
    };
  }

  function setPane(root, name, attrName) {
    $$("[" + attrName + "]", root).forEach(function (pane) {
      pane.classList.toggle("is-active", pane.getAttribute(attrName) === name);
    });
  }

  function collectCoords(geometry, out) {
    if (!geometry || !geometry.coordinates) return;
    function walk(coords) {
      if (!coords) return;
      if (typeof coords[0] === "number") {
        out.push(coords);
      } else {
        coords.forEach(walk);
      }
    }
    walk(geometry.coordinates);
  }

  function makeProjection(collections) {
    var pts = [];
    collections.forEach(function (fc) {
      (fc.features || []).forEach(function (feature) {
        collectCoords(feature.geometry, pts);
      });
    });

    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    pts.forEach(function (pt) {
      var x = Number(pt[0]);
      var y = Number(pt[1]);
      if (!isFinite(x) || !isFinite(y)) return;
      minX = Math.min(minX, x);
      minY = Math.min(minY, y);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    });

    if (!isFinite(minX) || !isFinite(minY) || !isFinite(maxX) || !isFinite(maxY)) {
      minX = 105; maxX = 109; minY = -8; maxY = -5;
    }

    var dx = maxX - minX || 1;
    var dy = maxY - minY || 1;
    minX -= dx * 0.045;
    maxX += dx * 0.045;
    minY -= dy * 0.06;
    maxY += dy * 0.06;

    return function project(coord) {
      var x = 38 + ((coord[0] - minX) / (maxX - minX)) * 924;
      var y = 686 - ((coord[1] - minY) / (maxY - minY)) * 632;
      return [x, y];
    };
  }

  function linePath(coords, project) {
    if (!coords || coords.length < 2) return "";
    var stride = coords.length > 80 ? Math.ceil(coords.length / 80) : 1;
    var parts = [];
    coords.forEach(function (coord, i) {
      if (i !== 0 && i !== coords.length - 1 && i % stride !== 0) return;
      var p = project(coord);
      parts.push((parts.length ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1));
    });
    return parts.join(" ");
  }

  function geometryPath(geometry, project) {
    if (!geometry) return "";
    if (geometry.type === "LineString") return linePath(geometry.coordinates, project);
    if (geometry.type === "MultiLineString") {
      return geometry.coordinates.map(function (line) { return linePath(line, project); }).join(" ");
    }
    if (geometry.type === "Polygon") {
      return geometry.coordinates.map(function (ring) { return linePath(ring, project) + " Z"; }).join(" ");
    }
    if (geometry.type === "MultiPolygon") {
      return geometry.coordinates.map(function (poly) {
        return poly.map(function (ring) { return linePath(ring, project) + " Z"; }).join(" ");
      }).join(" ");
    }
    return "";
  }

  function centroid(geometry) {
    var pts = [];
    collectCoords(geometry, pts);
    if (!pts.length) return null;
    var sx = 0, sy = 0, n = 0;
    pts.forEach(function (pt) {
      if (isFinite(pt[0]) && isFinite(pt[1])) {
        sx += pt[0];
        sy += pt[1];
        n += 1;
      }
    });
    return n ? [sx / n, sy / n] : null;
  }

  function featureProp(feature, key, fallback) {
    return feature && feature.properties && feature.properties[key] != null ? feature.properties[key] : fallback;
  }

  function drawPangan(root, data) {
    var project = makeProjection([data.kabkota, data.sentra, data.nodes, data.priority]);
    var svg = $(".story-map-svg", root);
    if (!svg) return;

    var groups = {
      kabkota: $('[data-layer="kabkota"]', svg),
      sentra: $('[data-layer="sentra"]', svg),
      nodes: $('[data-layer="nodes"]', svg),
      od: $('[data-layer="od"]', svg),
      flows: $('[data-layer="flows"]', svg),
      priority: $('[data-layer="priority"]', svg),
      labels: $('[data-layer="labels"]', svg)
    };

    Object.keys(groups).forEach(function (key) {
      if (groups[key]) groups[key].textContent = "";
    });

    (data.kabkota.features || []).forEach(function (feature) {
      var props = feature.properties || {};
      var status = String(props.kondisi || "").toLowerCase();
      var path = svgEl("path", {
        "class": "story-map-unit story-map-unit--" + (status.indexOf("surplus") >= 0 ? "surplus" : "deficit"),
        d: geometryPath(feature.geometry, project)
      });
      path.appendChild(svgEl("title", {})).textContent = props.name + " · " + props.kondisi + " · gap " + formatNumber(props.gap, 0) + " ha";
      groups.kabkota.appendChild(path);
    });

    var sentra = (data.sentra.features || []).slice().sort(function (a, b) {
      return Number(featureProp(b, "prod_ton", 0)) - Number(featureProp(a, "prod_ton", 0));
    }).slice(0, 160);
    var maxSentra = sentra.reduce(function (max, feature) {
      return Math.max(max, Number(featureProp(feature, "prod_ton", 0)) || 0);
    }, 1);
    sentra.forEach(function (feature) {
      var c = centroid(feature.geometry);
      if (!c) return;
      var p = project(c);
      var val = Number(featureProp(feature, "prod_ton", 0)) || 0;
      var radius = 2.1 + Math.sqrt(val / maxSentra) * 8;
      var node = svgEl("circle", {
        "class": "story-map-sentra",
        cx: p[0].toFixed(1),
        cy: p[1].toFixed(1),
        r: radius.toFixed(2)
      });
      node.appendChild(svgEl("title", {})).textContent = featureProp(feature, "kecamatan", "Production center") + " · " + formatNumber(val, 0) + " tons";
      groups.sentra.appendChild(node);
    });

    var od = (data.od.features || []).slice().sort(function (a, b) {
      return Number(featureProp(b, "flow", 0)) - Number(featureProp(a, "flow", 0));
    }).slice(0, 190);
    var maxOd = od.reduce(function (max, feature) {
      return Math.max(max, Number(featureProp(feature, "flow", 0)) || 0);
    }, 1);
    od.forEach(function (feature) {
      var flow = Number(featureProp(feature, "flow", 0)) || 0;
      var path = svgEl("path", {
        "class": "story-map-line story-map-od",
        d: geometryPath(feature.geometry, project),
        "stroke-width": (0.45 + Math.sqrt(flow / maxOd) * 5.8).toFixed(2)
      });
      path.appendChild(svgEl("title", {})).textContent = featureProp(feature, "origin", "Origin") + " → " + featureProp(feature, "dest", "Destination") + " · " + formatNumber(flow, 0);
      groups.od.appendChild(path);
    });

    var flows = (data.flows.features || []).slice().sort(function (a, b) {
      return Number(featureProp(b, "flow", 0)) - Number(featureProp(a, "flow", 0));
    }).slice(0, 900);
    var maxFlow = flows.reduce(function (max, feature) {
      return Math.max(max, Number(featureProp(feature, "flow", 0)) || 0);
    }, 1);
    flows.forEach(function (feature) {
      var flow = Number(featureProp(feature, "flow", 0)) || 0;
      var path = svgEl("path", {
        "class": "story-map-line story-map-flow",
        d: geometryPath(feature.geometry, project),
        "stroke-width": (0.35 + Math.log1p(flow) / Math.log1p(maxFlow) * 5.4).toFixed(2)
      });
      path.appendChild(svgEl("title", {})).textContent = featureProp(feature, "road", "Road segment") + " · flow " + formatNumber(flow, 0);
      groups.flows.appendChild(path);
    });

    var priority = (data.priority.features || []).slice().sort(function (a, b) {
      return Number(featureProp(a, "rank", 999)) - Number(featureProp(b, "rank", 999));
    });
    var maxScore = priority.reduce(function (max, feature) {
      return Math.max(max, Number(featureProp(feature, "score", 0)) || 0);
    }, 1);
    priority.forEach(function (feature, index) {
      var score = Number(featureProp(feature, "score", 0)) || 0;
      var path = svgEl("path", {
        "class": "story-map-line story-map-priority",
        d: geometryPath(feature.geometry, project),
        "stroke-width": (1.8 + Math.sqrt(score / maxScore) * 5.2).toFixed(2)
      });
      path.appendChild(svgEl("title", {})).textContent = "#" + featureProp(feature, "rank", "?") + " · " + featureProp(feature, "road", "Priority road") + " · score " + formatNumber(score, 1);
      groups.priority.appendChild(path);

      if (index < 5) {
        var c = centroid(feature.geometry);
        if (c) {
          var p = project(c);
          var label = svgEl("text", {
            "class": "story-map-label",
            x: p[0].toFixed(1),
            y: p[1].toFixed(1)
          });
          label.textContent = "#" + featureProp(feature, "rank", "?");
          groups.labels.appendChild(label);
        }
      }
    });

    (data.nodes.features || []).forEach(function (feature) {
      var c = centroid(feature.geometry);
      if (!c) return;
      var p = project(c);
      var cat = String(featureProp(feature, "cat", "node"));
      var radius = cat === "center" ? 3.1 : (cat === "bulog" || cat === "mrmp" ? 4.6 : 3.5);
      var node = svgEl("circle", {
        "class": "story-map-node story-map-node--" + cat,
        cx: p[0].toFixed(1),
        cy: p[1].toFixed(1),
        r: radius.toFixed(1)
      });
      node.appendChild(svgEl("title", {})).textContent = featureProp(feature, "name", "Supply-chain node") + " · " + cat.replace("_", " ");
      groups.nodes.appendChild(node);
    });
  }

  function initPangan(root) {
    var paths = {
      kabkota: "maps/data/pangan/pangan_kabkota.geojson",
      sentra: "maps/data/pangan/pangan_sentra.geojson",
      nodes: "maps/data/pangan/pangan_nodes.geojson",
      od: "maps/data/pangan/pangan_od.geojson",
      flows: "maps/data/pangan/pangan_flows.geojson",
      priority: "maps/data/pangan/pangan_priority.geojson"
    };
    var data = {};
    var story = bindStory(root, function (step) {
      var layers = (step.getAttribute("data-layers") || "").split(",").map(function (d) { return d.trim(); });
      $$(".story-map-layer", root).forEach(function (layer) {
        layer.classList.toggle("is-visible", layers.indexOf(layer.getAttribute("data-layer")) >= 0);
      });
      setText(root, "[data-story-kpi]", step.getAttribute("data-kpi"));
      setText(root, "[data-story-label]", step.getAttribute("data-label"));
      setText(root, "[data-story-note]", step.getAttribute("data-note"));
    });

    Promise.all(Object.keys(paths).map(function (key) {
      return fetchJson(paths[key]).then(function (json) { data[key] = json; });
    })).then(function () {
      drawPangan(root, data);
      root.classList.add("is-loaded");
      story.activate($$(".story-step", root).indexOf(story.getActiveStep()));
      var active = story.getActiveStep();
      if (active) {
        setText(root, "[data-story-kpi]", active.getAttribute("data-kpi"));
        setText(root, "[data-story-label]", active.getAttribute("data-label"));
        setText(root, "[data-story-note]", active.getAttribute("data-note"));
      }
    }).catch(function (err) {
      var status = $("[data-story-status]", root);
      if (status) status.textContent = "The story data could not load. Static figures below remain available.";
      console.error(err);
    });
  }

  function initImageStory(root) {
    var img = $("[data-story-image]", root);
    var caption = $("[data-story-caption]", root);
    if (!img) return;

    bindStory(root, function (step) {
      var src = step.getAttribute("data-image");
      var alt = step.getAttribute("data-alt") || step.querySelector("h4") && step.querySelector("h4").textContent || "";
      var cap = step.getAttribute("data-caption") || "";
      if (src && img.getAttribute("src") !== src) {
        img.classList.add("is-swapping");
        window.setTimeout(function () {
          img.src = src;
          img.alt = alt;
          img.classList.remove("is-swapping");
        }, 120);
      }
      if (caption) caption.textContent = cap;
      setText(root, "[data-story-kpi]", step.getAttribute("data-kpi"));
      setText(root, "[data-story-label]", step.getAttribute("data-label"));
      setText(root, "[data-story-note]", step.getAttribute("data-note"));
    });

    root.classList.add("is-loaded");
  }

  function truncate(text, max) {
    text = String(text || "");
    return text.length > max ? text.slice(0, max - 1) + "…" : text;
  }

  function renderCbdBars(svg, rows, metric) {
    if (!svg || !rows || !rows.length) return;
    var metricLabel = metric === "density_km2" ? "CBD density (POI/km²)" : "CBD POI count";
    var valueDigits = metric === "density_km2" ? 1 : 0;
    var sorted = rows.slice().sort(function (a, b) {
      return Number(b[metric]) - Number(a[metric]);
    }).slice(0, 12);
    var max = sorted.reduce(function (m, row) { return Math.max(m, Number(row[metric]) || 0); }, 1);
    var palette = {
      "Jawa": "#b35a3a",
      "Sumatera": "#6f7f52",
      "Bali & Nusa": "#466b8a",
      "Sulawesi": "#8a6c3d",
      "Kalimantan": "#5c518a",
      "Maluku": "#69716f",
      "Papua": "#94705c"
    };

    svg.textContent = "";
    svg.setAttribute("viewBox", "0 0 940 560");
    svg.appendChild(svgEl("text", {
      "class": "story-chart-title",
      x: 42,
      y: 52
    })).textContent = metricLabel;
    svg.appendChild(svgEl("text", {
      "class": "story-chart-subtitle",
      x: 42,
      y: 78
    })).textContent = "Top 12 provinces from processed OSM + DBSCAN output";
    svg.appendChild(svgEl("line", {
      "class": "story-chart-axis",
      x1: 228,
      y1: 104,
      x2: 228,
      y2: 516
    }));

    sorted.forEach(function (row, i) {
      var y = 112 + i * 33;
      var val = Number(row[metric]) || 0;
      var w = Math.max(3, (val / max) * 590);
      var color = palette[row.island] || "#6a665d";
      var label = svgEl("text", {
        "class": "story-chart-label",
        x: 42,
        y: y + 16
      });
      label.textContent = truncate(row.province, 23);
      svg.appendChild(label);

      var bar = svgEl("rect", {
        "class": "story-chart-bar",
        x: 230,
        y: y,
        width: w.toFixed(1),
        height: 21,
        fill: color
      });
      bar.appendChild(svgEl("title", {})).textContent = row.province + " · " + metricLabel + ": " + formatNumber(val, valueDigits) + " · " + row.island;
      svg.appendChild(bar);

      var value = svgEl("text", {
        "class": "story-chart-value",
        x: 900,
        y: y + 16
      });
      value.textContent = formatNumber(val, valueDigits);
      svg.appendChild(value);
    });
  }

  function initCbd(root) {
    var rows = null;
    var barsSvg = $("[data-cbd-bars]", root);
    var activeMetric = "n_poi";
    var story = bindStory(root, function (step) {
      var pane = step.getAttribute("data-pane") || "bars";
      var metric = step.getAttribute("data-metric") || activeMetric;
      activeMetric = metric;
      setPane(root, pane, "data-cbd-pane");
      setText(root, "[data-story-kpi]", step.getAttribute("data-kpi"));
      setText(root, "[data-story-label]", step.getAttribute("data-label"));
      setText(root, "[data-story-note]", step.getAttribute("data-note"));
      if (rows && pane === "bars") renderCbdBars(barsSvg, rows, metric);
    });

    fetchJson("assets/data/cbd/indonesia_cbd.json").then(function (json) {
      rows = Array.isArray(json) ? json : [];
      root.classList.add("is-loaded");
      var active = story.getActiveStep();
      if (active) {
        renderCbdBars(barsSvg, rows, active.getAttribute("data-metric") || activeMetric);
      }
    }).catch(function (err) {
      var status = $("[data-story-status]", root);
      if (status) status.textContent = "The CBD data could not load. Static figures and maps below remain available.";
      console.error(err);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    $$("[data-pangan-scrolly]").forEach(initPangan);
    $$("[data-image-scrolly]").forEach(initImageStory);
    $$("[data-cbd-scrolly]").forEach(initCbd);
  });
})();
