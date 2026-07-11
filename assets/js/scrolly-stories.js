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

  function updateStoryLegend(root, step) {
    var legend = $("[data-story-legend]", root);
    if (!legend || !step) return;
    var target = $("[data-story-legend-items]", legend) || legend;
    var raw = step.getAttribute("data-legend") || "";
    var entries = raw.split(";").map(function (entry) {
      var pair = entry.split("=");
      return {
        label: (pair[0] || "").trim(),
        type: (pair[1] || pair[0] || "").trim().toLowerCase().replace(/[^a-z0-9_-]+/g, "-")
      };
    }).filter(function (entry) { return entry.label; });

    target.textContent = "";
    legend.hidden = !entries.length;
    if (entries.length) {
      legend.setAttribute("aria-label", "Active layers: " + entries.map(function (entry) { return entry.label; }).join(", "));
    } else {
      legend.removeAttribute("aria-label");
    }
    entries.forEach(function (entry) {
      var item = document.createElement("span");
      item.className = "story-layer-legend__item";

      var swatch = document.createElement("i");
      swatch.className = "story-layer-legend__swatch story-layer-legend__swatch--" + entry.type;
      swatch.setAttribute("aria-hidden", "true");
      item.appendChild(swatch);
      item.appendChild(document.createTextNode(entry.label));
      target.appendChild(item);
    });
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
    var manualNavUntil = 0;

    if (progress && steps.length) {
      progress.removeAttribute("aria-hidden");
      progress.setAttribute("role", "navigation");
      progress.setAttribute("aria-label", "Story chapters");
      steps.forEach(function (step, i) {
        var heading = step.querySelector("h4");
        var dot = document.createElement("button");
        dot.type = "button";
        dot.setAttribute("aria-label", "Jump to step " + (i + 1) + (heading ? ": " + heading.textContent : ""));
        dot.addEventListener("click", function () {
          manualNavUntil = Date.now() + 700;
          step.scrollIntoView({ behavior: "auto", block: "center" });
          activate(i);
        });
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
        if (i === index) dot.setAttribute("aria-current", "step");
        else dot.removeAttribute("aria-current");
      });
      updateStoryLegend(root, steps[index]);
      onActive(steps[index], index);
    }

    activate(0);

    if ("IntersectionObserver" in window && steps.length) {
      var io = new IntersectionObserver(function (entries) {
        if (Date.now() < manualNavUntil) return;
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

  function renderCompactBars(svg, rows, options) {
    if (!svg || !rows || !rows.length) return;
    options = options || {};
    var width = 520;
    var height = 310;
    var left = 148;
    var top = 78;
    var rowH = Math.min(32, Math.floor((height - top - 24) / rows.length));
    var max = rows.reduce(function (m, row) { return Math.max(m, Math.abs(Number(row.value)) || 0); }, 1);
    var min = rows.reduce(function (m, row) { return Math.min(m, Number(row.value) || 0); }, 0);
    var hasNegative = min < 0;
    var zeroX = hasNegative ? left + 150 : left;
    var maxW = hasNegative ? 300 : 330;
    svg.textContent = "";
    svg.setAttribute("viewBox", "0 0 " + width + " " + height);

    svg.appendChild(svgEl("text", {
      "class": "story-chart-title story-chart-title--small",
      x: 24,
      y: 34
    })).textContent = options.title || "";
    svg.appendChild(svgEl("text", {
      "class": "story-chart-subtitle",
      x: 24,
      y: 56
    })).textContent = options.subtitle || "";

    if (hasNegative) {
      svg.appendChild(svgEl("line", {
        "class": "story-chart-axis",
        x1: zeroX,
        y1: top - 8,
        x2: zeroX,
        y2: height - 20
      }));
    }

    rows.forEach(function (row, i) {
      var y = top + i * rowH;
      var val = Number(row.value) || 0;
      var w = Math.max(3, Math.abs(val) / max * maxW);
      var x = hasNegative && val < 0 ? zeroX - w : zeroX;
      var color = row.color || options.color || "var(--accent)";

      var label = svgEl("text", {
        "class": "story-chart-label",
        x: 24,
        y: y + 16
      });
      label.textContent = truncate(row.label, 18);
      svg.appendChild(label);

      var bar = svgEl("rect", {
        "class": "story-chart-bar",
        x: x.toFixed(1),
        y: y,
        width: w.toFixed(1),
        height: Math.max(16, rowH - 10),
        fill: color
      });
      bar.appendChild(svgEl("title", {})).textContent = row.label + ": " + formatNumber(val, options.digits || 0) + (options.suffix || "");
      svg.appendChild(bar);

      var value = svgEl("text", {
        "class": "story-chart-value",
        x: 500,
        y: y + 16
      });
      value.textContent = formatNumber(val, options.digits || 0) + (options.suffix || "");
      svg.appendChild(value);
    });
  }

  function renderLineChart(svg, rows, options) {
    if (!svg || !rows || !rows.length) return;
    options = options || {};
    var width = 760;
    var height = 480;
    var left = 60, right = 32, top = 86, bottom = 54;
    var values = [];
    rows.forEach(function (row) {
      ["mean", "q1", "q3"].forEach(function (key) {
        if (isFinite(Number(row[key]))) values.push(Number(row[key]));
      });
    });
    var min = Math.min.apply(Math, values);
    var max = Math.max.apply(Math, values);
    var pad = (max - min || 1) * 0.14;
    min -= pad;
    max += pad;
    function x(i) { return left + i / Math.max(1, rows.length - 1) * (width - left - right); }
    function y(v) { return height - bottom - ((v - min) / (max - min || 1)) * (height - top - bottom); }
    function pathFor(key) {
      return rows.map(function (row, i) {
        return (i ? "L" : "M") + x(i).toFixed(1) + " " + y(Number(row[key])).toFixed(1);
      }).join(" ");
    }

    svg.textContent = "";
    svg.setAttribute("viewBox", "0 0 " + width + " " + height);
    svg.appendChild(svgEl("text", { "class": "story-chart-title", x: 42, y: 48 })).textContent = options.title || "";
    svg.appendChild(svgEl("text", { "class": "story-chart-subtitle", x: 42, y: 73 })).textContent = options.subtitle || "";

    [0, .25, .5, .75, 1].forEach(function (t) {
      var yy = top + t * (height - top - bottom);
      svg.appendChild(svgEl("line", { "class": "story-chart-axis", x1: left, y1: yy.toFixed(1), x2: width - right, y2: yy.toFixed(1) }));
    });

    var area = pathFor("q3") + " " + rows.slice().reverse().map(function (row, i) {
      var idx = rows.length - 1 - i;
      return "L" + x(idx).toFixed(1) + " " + y(Number(row.q1)).toFixed(1);
    }).join(" ") + " Z";
    svg.appendChild(svgEl("path", { d: area, fill: "var(--accent-soft)", opacity: .68 }));
    svg.appendChild(svgEl("path", { d: pathFor("q1"), fill: "none", stroke: "var(--outline)", "stroke-width": 1.2 }));
    svg.appendChild(svgEl("path", { d: pathFor("q3"), fill: "none", stroke: "var(--outline)", "stroke-width": 1.2 }));
    svg.appendChild(svgEl("path", { d: pathFor("mean"), fill: "none", stroke: "var(--accent)", "stroke-width": 4, "stroke-linecap": "round", "stroke-linejoin": "round" }));

    rows.forEach(function (row, i) {
      var label = svgEl("text", { "class": "story-chart-label", x: x(i), y: height - 24, "text-anchor": "middle" });
      label.textContent = row.year;
      svg.appendChild(label);
      svg.appendChild(svgEl("circle", { cx: x(i).toFixed(1), cy: y(Number(row.mean)).toFixed(1), r: 4, fill: "var(--accent)" }));
    });
  }

  function nodeCategoryLabel(cat) {
    return {
      gudang: "Warehouses",
      center: "Centers",
      pasar_rakyat: "Public markets",
      pasar: "Central markets",
      bulog: "Bulog",
      mrmp: "MRMP"
    }[cat] || cat;
  }

  function renderPanganChart(root, data, type) {
    var svg = $("[data-pangan-chart]", root);
    if (!svg || !data.kabkota) return;
    var rows = [];
    var opts = {};
    if (type === "production") {
      rows = (data.sentra.features || []).slice().sort(function (a, b) {
        return Number(featureProp(b, "prod_ton", 0)) - Number(featureProp(a, "prod_ton", 0));
      }).slice(0, 6).map(function (feature) {
        return { label: featureProp(feature, "kecamatan", ""), value: Number(featureProp(feature, "prod_ton", 0)), color: "var(--viz-sentra)" };
      });
      opts = { title: "Largest Rice Centers", subtitle: "Top kecamatan by modeled production", suffix: " t", digits: 0 };
    } else if (type === "nodes") {
      var counts = {};
      (data.nodes.features || []).forEach(function (feature) {
        var cat = featureProp(feature, "cat", "node");
        counts[cat] = (counts[cat] || 0) + 1;
      });
      rows = Object.keys(counts).map(function (cat) {
        return { label: nodeCategoryLabel(cat), value: counts[cat], color: cat === "center" ? "var(--viz-node-center)" : cat === "gudang" ? "var(--viz-node-gudang)" : "var(--viz-node-market)" };
      }).sort(function (a, b) { return b.value - a.value; });
      opts = { title: "Supply-Chain Nodes", subtitle: "Channels and destinations in the model" };
    } else if (type === "od") {
      rows = (data.od.features || []).slice().sort(function (a, b) {
        return Number(featureProp(b, "flow", 0)) - Number(featureProp(a, "flow", 0));
      }).slice(0, 6).map(function (feature) {
        return { label: featureProp(feature, "origin", "") + " → " + featureProp(feature, "dest", ""), value: Number(featureProp(feature, "flow", 0)), color: "var(--viz-route)" };
      });
      opts = { title: "Largest OD Links", subtitle: "Top modeled desire-line flows", suffix: " t", digits: 0 };
    } else if (type === "flows") {
      var roads = {};
      (data.flows.features || []).forEach(function (feature) {
        var name = featureProp(feature, "road", "Unnamed road");
        roads[name] = (roads[name] || 0) + (Number(featureProp(feature, "flow", 0)) || 0);
      });
      rows = Object.keys(roads).map(function (name) { return { label: name, value: roads[name], color: "var(--viz-flow)" }; })
        .sort(function (a, b) { return b.value - a.value; }).slice(0, 6);
      opts = { title: "Highest-Load Roads", subtitle: "Flow summed by road name", suffix: " t", digits: 0 };
    } else {
      rows = (data.priority.features || []).slice().sort(function (a, b) {
        return Number(featureProp(a, "rank", 999)) - Number(featureProp(b, "rank", 999));
      }).slice(0, 6).map(function (feature) {
        return { label: "#" + featureProp(feature, "rank", "?") + " " + featureProp(feature, "road", ""), value: Number(featureProp(feature, "score", 0)), color: "var(--accent)" };
      });
      opts = { title: "Priority Score", subtitle: "Top ranked intervention candidates", digits: 1 };
    }
    renderCompactBars(svg, rows, opts);
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
      renderPanganChart(root, data, step.getAttribute("data-chart"));
    });

    function loadPanganData() {
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
          renderPanganChart(root, data, active.getAttribute("data-chart"));
        }
      }).catch(function (err) {
        var status = $("[data-story-status]", root);
        if (status) status.textContent = "The story data could not load. Static figures below remain available.";
        console.error(err);
      });
    }

    // Combined pangan geojson layers run ~2.5MB — only fetch once the story
    // section is about to enter view, not on initial page load.
    if ("IntersectionObserver" in window) {
      var panganObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            panganObserver.disconnect();
            loadPanganData();
          }
        });
      }, { rootMargin: "600px 0px" });
      panganObserver.observe(root);
    } else {
      loadPanganData();
    }
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

  function renderMbrModel(svg, data) {
    var model = data.modelSummary && data.modelSummary[0];
    if (!model) return;
    renderCompactBars(svg, [
      { label: "R² out-of-fold", value: model.r2, color: "var(--accent)" },
      { label: "Spearman ρ", value: model.spearman, color: "#466b8a" },
      { label: "MAE", value: model.mae, color: "#6f7f52" }
    ], {
      title: "Stage 1 Model Fit",
      subtitle: model.features + " AlphaEarth features · " + model.model,
      digits: 3
    });
  }

  function renderMbrQuintiles(svg, data) {
    var rows = (data.wealthQuintiles || []).map(function (row) {
      return {
        label: row.quintile.replace("_", " "),
        value: row.avg_deprivation,
        color: row.quintile.indexOf("Q1") === 0 ? "var(--accent)" : row.quintile.indexOf("Q2") === 0 ? "#c48662" : row.quintile.indexOf("Q3") === 0 ? "#d3b36d" : row.quintile.indexOf("Q4") === 0 ? "#7f9f93" : "#466b8a"
      };
    });
    renderCompactBars(svg, rows, {
      title: "Economic Quintile Gradient",
      subtitle: "Average deprivation score by calibrated wealth quintile",
      digits: 1
    });
  }

  function renderMbrIpks(svg, data) {
    var rows = (data.ipksCorrelations || []).filter(function (row) {
      return row.rho !== null && row.rho !== undefined;
    }).map(function (row) {
      return {
        label: row.code + " · " + row.dimension,
        value: row.rho,
        color: row.significant ? "var(--accent)" : "#8a8177"
      };
    });
    renderCompactBars(svg, rows, {
      title: "IPKS Validation",
      subtitle: "Spearman correlation with official deprivation dimensions",
      digits: 3
    });
  }

  function renderMbrChart(root, data, chart) {
    var svg = $("[data-mbr-chart]", root);
    if (!svg || !data) return;
    if (chart === "trajectory") {
      renderLineChart(svg, data.smoothedTrajectory || [], {
        title: "Smoothed Trajectory Envelope",
        subtitle: "Mean and interquartile range, 2017-2024"
      });
    } else if (chart === "quintile") {
      renderMbrQuintiles(svg, data);
    } else if (chart === "ipks") {
      renderMbrIpks(svg, data);
    } else {
      renderMbrModel(svg, data);
    }
  }

  function initMbr(root) {
    var storyData = null;
    var story = bindStory(root, function (step) {
      var pane = step.getAttribute("data-pane") || "chart";
      var chart = step.getAttribute("data-chart") || "model";
      setPane(root, pane, "data-mbr-pane");
      setText(root, "[data-story-kpi]", step.getAttribute("data-kpi"));
      setText(root, "[data-story-label]", step.getAttribute("data-label"));
      setText(root, "[data-story-note]", step.getAttribute("data-note"));
      if (storyData && pane === "chart") renderMbrChart(root, storyData, chart);
    });

    fetchJson("assets/data/mbr/mbr_story.json").then(function (json) {
      storyData = json;
      root.classList.add("is-loaded");
      var active = story.getActiveStep();
      if (active && (active.getAttribute("data-pane") || "chart") === "chart") {
        renderMbrChart(root, storyData, active.getAttribute("data-chart") || "model");
      }
    }).catch(function (err) {
      var status = $("[data-story-status]", root);
      if (status) status.textContent = "The MBR story data could not load. Exported figures remain available in the story.";
      console.error(err);
    });
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
      "Jawa": "var(--viz-region-jawa)",
      "Sumatera": "var(--viz-region-sumatera)",
      "Bali & Nusa": "var(--viz-region-bali-nusa)",
      "Sulawesi": "var(--viz-region-sulawesi)",
      "Kalimantan": "var(--viz-region-kalimantan)",
      "Maluku": "var(--viz-region-maluku)",
      "Papua": "var(--viz-region-papua)"
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
    $$("[data-mbr-scrolly]").forEach(initMbr);
    $$("[data-image-scrolly]").forEach(initImageStory);
    $$("[data-cbd-scrolly]").forEach(initCbd);
  });
})();
