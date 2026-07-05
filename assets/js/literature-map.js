/*
  Literature Map component
  ------------------------
  Edit assets/data/literature-maps.json to add nodes or edges. Keep the visual
  curated: the full academic references stay in each HTML page below the map.
*/
(function () {
  "use strict";

  var DATA_URL = "assets/data/literature-maps.json?v=2";
  var CATEGORY_ORDER = [
    "Core Method",
    "Dataset / Data Source",
    "Software / Tool",
    "Validation / Benchmark",
    "Policy / Planning Context",
    "Background / Interpretation"
  ];
  var PHASE_LABELS = {
    1: "Research question",
    2: "Core methods",
    3: "Data foundations",
    4: "Implementation tools",
    5: "Validation and context",
    6: "Connections",
    7: "Explore"
  };
  var CLUSTER_CENTERS = {
    "Core Method": { x: 500, y: 112 },
    "Dataset / Data Source": { x: 770, y: 215 },
    "Software / Tool": { x: 738, y: 468 },
    "Validation / Benchmark": { x: 500, y: 538 },
    "Policy / Planning Context": { x: 240, y: 455 },
    "Background / Interpretation": { x: 232, y: 210 }
  };
  var CATEGORY_PHASE = {
    "Core Method": 2,
    "Dataset / Data Source": 3,
    "Software / Tool": 4,
    "Validation / Benchmark": 5,
    "Policy / Planning Context": 5,
    "Background / Interpretation": 5
  };
  var CENTER = { x: 500, y: 320 };
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function slug(value) {
    return String(value || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
  }

  function yearLabel(node) {
    return node.year == null || node.year === "" ? "n.d." : String(node.year);
  }

  function shortLabel(label) {
    var words = String(label || "").split(/\s+/).filter(Boolean);
    if (words.length <= 4) return label || "Source";
    return words.slice(0, 4).join(" ") + "...";
  }

  function categoryMeta(data, category) {
    return (data.categories && data.categories[category]) || {
      label: category || "Evidence",
      color: "#68645d",
      shape: "circle",
      description: "Supporting evidence used by this case study."
    };
  }

  function phaseForNode(node) {
    return CATEGORY_PHASE[node.category] || 5;
  }

  function visibleForPhase(node, phase) {
    return phase >= phaseForNode(node);
  }

  function edgeVisible(edge, byId, phase) {
    if (phase < 6) {
      var target = byId[edge.target] || byId[edge.source];
      return target ? visibleForPhase(target, phase) : phase >= 6;
    }
    return true;
  }

  function nodeRadius(node) {
    return 8 + Math.max(1, Math.min(5, Number(node.importance) || 2)) * 2.8;
  }

  function nodePositions(project) {
    var grouped = {};
    project.nodes.forEach(function (node) {
      if (!grouped[node.category]) grouped[node.category] = [];
      grouped[node.category].push(node);
    });

    return project.nodes.map(function (node) {
      var group = grouped[node.category] || [node];
      var index = group.indexOf(node);
      var count = group.length;
      var cluster = CLUSTER_CENTERS[node.category] || CENTER;
      var radius = count < 3 ? 58 : 74;
      var angle = count === 1 ? -Math.PI / 2 : (-Math.PI / 2) + (index / count) * Math.PI * 2;
      var jitter = index % 2 ? 18 : -8;

      return {
        node: node,
        x: Math.max(72, Math.min(928, cluster.x + Math.cos(angle) * (radius + jitter))),
        y: Math.max(70, Math.min(570, cluster.y + Math.sin(angle) * (radius + jitter)))
      };
    });
  }

  function pathBetween(a, b) {
    var dx = b.x - a.x;
    var dy = b.y - a.y;
    var curve = Math.min(90, Math.max(30, Math.abs(dx) * 0.18));
    return [
      "M", a.x.toFixed(1), a.y.toFixed(1),
      "C", (a.x + dx * 0.45).toFixed(1), (a.y + dy * 0.45 - curve).toFixed(1),
      (a.x + dx * 0.58).toFixed(1), (a.y + dy * 0.58 + curve).toFixed(1),
      b.x.toFixed(1), b.y.toFixed(1)
    ].join(" ");
  }

  function lineLabelPosition(a, b) {
    return {
      x: a.x + (b.x - a.x) * 0.56,
      y: a.y + (b.y - a.y) * 0.56
    };
  }

  function detailMarkup(item, edge) {
    if (!item) return "";
    var title = item.title || item.label;
    var link = item.url ? '<a href="' + escapeHtml(item.url) + '" target="_blank" rel="noopener">Open source</a>' : "";
    var relation = edge ? edge.relationship : "selected source";
    return [
      '<span class="literature-map__detail-kicker">',
      escapeHtml(item.category || item.type),
      " · ",
      escapeHtml(yearLabel(item)),
      "</span>",
      "<h4>",
      escapeHtml(title),
      "</h4>",
      "<p>",
      escapeHtml(item.role || item.title || item.label),
      "</p>",
      "<dl>",
      "<div><dt>Relationship</dt><dd>",
      escapeHtml(relation),
      "</dd></div>",
      "<div><dt>Importance</dt><dd>",
      escapeHtml(item.importance ? item.importance + " / 5" : "center"),
      "</dd></div>",
      "<div><dt>Type</dt><dd>",
      escapeHtml(item.type || "reference"),
      "</dd></div>",
      "</dl>",
      link
    ].join("");
  }

  function legendMarkup(data) {
    return CATEGORY_ORDER.map(function (category) {
      var meta = categoryMeta(data, category);
      return [
        '<button class="literature-map__legend-item" type="button" data-literature-category="',
        escapeHtml(category),
        '" style="--cat-color:',
        escapeHtml(meta.color),
        '" data-shape="',
        escapeHtml(meta.shape),
        '"><i aria-hidden="true"></i><span>',
        escapeHtml(meta.label),
        "</span></button>"
      ].join("");
    }).join("");
  }

  function fallbackMarkup(data, project) {
    return [
      '<div class="literature-map__fallback">',
      "<h4>Text summary of evidence categories</h4>",
      CATEGORY_ORDER.map(function (category) {
        var meta = categoryMeta(data, category);
        var items = project.nodes
          .filter(function (node) { return node.category === category; })
          .slice(0, 4)
          .map(function (node) { return escapeHtml(node.label); })
          .join("; ");
        return [
          "<p><strong>",
          escapeHtml(meta.label),
          ":</strong> ",
          escapeHtml(meta.description),
          items ? " <span>Key sources: " + items + ".</span>" : "",
          "</p>"
        ].join("");
      }).join(""),
      "</div>"
    ].join("");
  }

  function metricsMarkup(data, project) {
    var usedCategories = {};
    (project.nodes || []).forEach(function (node) {
      usedCategories[node.category] = true;
    });
    var clusterCount = Object.keys(usedCategories).length;

    return [
      '<div class="literature-map__metrics" aria-label="Literature network summary">',
      '<span><b>',
      escapeHtml((project.nodes || []).length + 1),
      "</b> nodes</span>",
      '<span><b>',
      escapeHtml((project.edges || []).length),
      "</b> relationships</span>",
      '<span><b>',
      escapeHtml(clusterCount),
      "</b> evidence clusters</span>",
      "</div>"
    ].join("");
  }

  function stepMarkup(project) {
    return (project.steps || []).map(function (step, index) {
      return [
        '<article class="literature-map__step" data-literature-step="',
        escapeHtml(step.phase),
        '" style="--delay:',
        (index * 0.04).toFixed(2),
        's">',
        "<span>",
        String(index + 1).padStart(2, "0"),
        "</span>",
        "<h4>",
        escapeHtml(step.title),
        "</h4>",
        "<p>",
        escapeHtml(step.body),
        "</p>",
        "</article>"
      ].join("");
    }).join("");
  }

  function graphMarkup(data, project) {
    var positions = nodePositions(project);
    var byId = {};
    var center = project.center || { id: "center", label: project.title, title: project.title, type: "Research Question" };
    byId[center.id] = { node: center, x: CENTER.x, y: CENTER.y, center: true };
    positions.forEach(function (position) { byId[position.node.id] = position; });

    var edgeMarkup = project.edges.map(function (edge, index) {
      var source = byId[edge.source] || byId[center.id];
      var target = byId[edge.target] || byId[center.id];
      var targetNode = target.node && target.node.id !== center.id ? target.node : source.node;
      var phase = targetNode && targetNode.category ? phaseForNode(targetNode) : 6;
      var labelPosition = lineLabelPosition(source, target);
      return [
        '<g class="literature-map__edge-group" data-edge-source="',
        escapeHtml(edge.source),
        '" data-edge-target="',
        escapeHtml(edge.target),
        '" data-edge-category="',
        escapeHtml(targetNode.category || ""),
        '" data-min-phase="',
        escapeHtml(Math.max(phase, 6)),
        '" style="--delay:',
        (index * 0.035).toFixed(3),
        's">',
        '<path class="literature-map__edge" d="',
        escapeHtml(pathBetween(source, target)),
        '"></path>',
        '<text class="literature-map__edge-label" x="',
        labelPosition.x.toFixed(1),
        '" y="',
        labelPosition.y.toFixed(1),
        '">',
        escapeHtml(edge.relationship),
        "</text>",
        "</g>"
      ].join("");
    }).join("");

    var clusterMarkup = CATEGORY_ORDER.map(function (category) {
      var centerPoint = CLUSTER_CENTERS[category];
      var meta = categoryMeta(data, category);
      if (!centerPoint) return "";
      return [
        '<g class="literature-map__cluster-label" data-min-phase="',
        escapeHtml(CATEGORY_PHASE[category]),
        '" style="--cat-color:',
        escapeHtml(meta.color),
        '">',
        '<circle cx="',
        centerPoint.x,
        '" cy="',
        centerPoint.y,
        '" r="84"></circle>',
        '<text x="',
        centerPoint.x,
        '" y="',
        centerPoint.y - 92,
        '">',
        escapeHtml(meta.label),
        "</text>",
        "</g>"
      ].join("");
    }).join("");

    var nodeMarkup = positions.map(function (position, index) {
      var node = position.node;
      var meta = categoryMeta(data, node.category);
      var radius = nodeRadius(node);
      var label = [node.title || node.label, yearLabel(node), node.category, node.role].filter(Boolean).join(" · ");
      return [
        '<g class="literature-map__node" role="button" tabindex="0" aria-label="',
        escapeHtml(label),
        '" data-node-id="',
        escapeHtml(node.id),
        '" data-node-category="',
        escapeHtml(node.category),
        '" data-min-phase="',
        escapeHtml(phaseForNode(node)),
        '" style="--cat-color:',
        escapeHtml(meta.color),
        ';--delay:',
        (0.06 + index * 0.045).toFixed(3),
        's">',
        '<circle cx="',
        position.x.toFixed(1),
        '" cy="',
        position.y.toFixed(1),
        '" r="',
        radius.toFixed(1),
        '"></circle>',
        '<text x="',
        position.x.toFixed(1),
        '" y="',
        (position.y + radius + 15).toFixed(1),
        '">',
        escapeHtml(shortLabel(node.label)),
        "</text>",
        "</g>"
      ].join("");
    }).join("");

    return [
      '<svg class="literature-map__svg" viewBox="0 0 1000 640" role="img" aria-label="Literature network graph">',
      '<rect class="literature-map__plot-bg" x="0" y="0" width="1000" height="640" rx="28"></rect>',
      '<g class="literature-map__center-halo" aria-hidden="true">',
      '<circle cx="',
      CENTER.x,
      '" cy="',
      CENTER.y,
      '" r="124"></circle>',
      '<circle cx="',
      CENTER.x,
      '" cy="',
      CENTER.y,
      '" r="206"></circle>',
      "</g>",
      clusterMarkup,
      edgeMarkup,
      '<g class="literature-map__center" data-node-id="',
      escapeHtml(center.id),
      '">',
      '<circle cx="',
      CENTER.x,
      '" cy="',
      CENTER.y,
      '" r="46"></circle>',
      '<text x="',
      CENTER.x,
      '" y="',
      CENTER.y - 6,
      '">Research</text>',
      '<text x="',
      CENTER.x,
      '" y="',
      CENTER.y + 13,
      '">question</text>',
      "</g>",
      nodeMarkup,
      "</svg>"
    ].join("");
  }

  function getNode(project, id) {
    if (project.center && project.center.id === id) return project.center;
    return (project.nodes || []).find(function (node) { return node.id === id; });
  }

  function relatedEdges(project, id) {
    return (project.edges || []).filter(function (edge) {
      return edge.source === id || edge.target === id;
    });
  }

  function setPhase(root, project, phase) {
    var numericPhase = Number(phase) || 1;
    root.setAttribute("data-phase", String(numericPhase));
    root.querySelector("[data-literature-phase-label]").textContent = PHASE_LABELS[numericPhase] || "Explore";
    root.querySelectorAll("[data-min-phase]").forEach(function (el) {
      var minPhase = Number(el.getAttribute("data-min-phase"));
      var isVisible = reduceMotion || numericPhase >= minPhase;
      el.classList.toggle("is-visible", isVisible);
    });
    root.querySelectorAll("[data-literature-step]").forEach(function (step) {
      step.classList.toggle("is-active", Number(step.getAttribute("data-literature-step")) === numericPhase);
    });
    if (numericPhase >= 7) {
      root.classList.add("is-explorable");
    } else {
      root.classList.remove("is-explorable");
    }
  }

  function clearHighlight(root) {
    root.classList.remove("is-filtered");
    root.querySelectorAll(".is-related, .is-selected, .is-muted").forEach(function (el) {
      el.classList.remove("is-related", "is-selected", "is-muted");
    });
  }

  function selectNode(root, project, id) {
    var node = getNode(project, id);
    if (!node) return;
    var edges = relatedEdges(project, id);
    var related = {};
    related[id] = true;
    edges.forEach(function (edge) {
      related[edge.source] = true;
      related[edge.target] = true;
    });

    root.classList.add("is-filtered");
    root.querySelectorAll("[data-node-id]").forEach(function (el) {
      var nodeId = el.getAttribute("data-node-id");
      el.classList.toggle("is-selected", nodeId === id);
      el.classList.toggle("is-related", !!related[nodeId] && nodeId !== id);
      el.classList.toggle("is-muted", !related[nodeId]);
    });
    root.querySelectorAll(".literature-map__edge-group").forEach(function (el) {
      var isRelated = el.getAttribute("data-edge-source") === id || el.getAttribute("data-edge-target") === id;
      el.classList.toggle("is-related", isRelated);
      el.classList.toggle("is-muted", !isRelated);
    });

    var detail = root.querySelector("[data-literature-detail]");
    if (detail) detail.innerHTML = detailMarkup(node, edges[0]);
  }

  function filterCategory(root, category) {
    root.classList.add("is-filtered");
    root.querySelectorAll("[data-node-category]").forEach(function (el) {
      var match = el.getAttribute("data-node-category") === category;
      el.classList.toggle("is-selected", match);
      el.classList.toggle("is-muted", !match);
    });
    root.querySelectorAll(".literature-map__edge-group").forEach(function (el) {
      var match = el.getAttribute("data-edge-category") === category;
      el.classList.toggle("is-related", match);
      el.classList.toggle("is-muted", !match);
    });
  }

  function installStepObserver(root, project) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      setPhase(root, project, 7);
      root.classList.add("is-visible", "is-reduced");
      return;
    }

    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        root.classList.add("is-visible");
        revealObserver.unobserve(root);
      });
    }, { threshold: 0.2 });
    revealObserver.observe(root);

    var stepObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        setPhase(root, project, entry.target.getAttribute("data-literature-step"));
      });
    }, { rootMargin: "-38% 0px -48% 0px", threshold: 0.01 });

    root.querySelectorAll("[data-literature-step]").forEach(function (step) {
      stepObserver.observe(step);
    });
  }

  function centerScrollableGraphic(root) {
    var graphic = root.querySelector(".literature-map__graphic");
    if (!graphic || graphic.scrollWidth <= graphic.clientWidth) return;
    graphic.scrollLeft = Math.max(0, (graphic.scrollWidth - graphic.clientWidth) / 2);
  }

  function render(root, key, data) {
    var project = data.projects && data.projects[key];
    if (!project) {
      root.innerHTML = '<p class="literature-map__fallback">Literature map data is not available. The full references remain below.</p>';
      return;
    }

    var center = project.center || { label: project.title, title: project.title, type: "Research Question" };
    root.classList.add("literature-map--ready");
    root.setAttribute("aria-busy", "false");
    root.innerHTML = [
      '<div class="literature-map__intro">',
      '<div class="literature-map__intro-copy">',
      '<span class="literature-map__eyebrow">Literature map</span>',
      "<h3>Evidence &amp; Literature Map</h3>",
      "<p>",
      escapeHtml(project.summary),
      "</p>",
      metricsMarkup(data, project),
      '<div class="literature-map__legend" aria-label="Literature map categories">',
      legendMarkup(data),
      "</div>",
      "</div>",
      '<div class="literature-map__detail" data-literature-detail aria-live="polite">',
      detailMarkup({
        title: center.label,
        label: center.label,
        type: center.type,
        category: center.type,
        role: center.title,
        importance: null
      }),
      "</div>",
      "</div>",
      '<div class="literature-map__story">',
      '<div class="literature-map__graphic">',
      '<div class="literature-map__status"><span data-literature-phase-label>Research question</span><em>Select nodes or category chips to filter</em><button type="button" data-literature-reset>Reset</button></div>',
      graphMarkup(data, project),
      "</div>",
      '<div class="literature-map__steps" aria-label="Literature map reveal steps">',
      stepMarkup(project),
      "</div>",
      "</div>",
      fallbackMarkup(data, project)
    ].join("");

    root.querySelectorAll("[data-node-id]").forEach(function (el) {
      var id = el.getAttribute("data-node-id");
      el.addEventListener("click", function () { selectNode(root, project, id); });
      el.addEventListener("focus", function () { selectNode(root, project, id); });
      el.addEventListener("mouseenter", function () { selectNode(root, project, id); });
    });
    root.querySelectorAll("[data-literature-category]").forEach(function (el) {
      var category = el.getAttribute("data-literature-category");
      el.addEventListener("mouseenter", function () { filterCategory(root, category); });
      el.addEventListener("focus", function () { filterCategory(root, category); });
      el.addEventListener("mouseleave", function () { clearHighlight(root); });
      el.addEventListener("blur", function () { clearHighlight(root); });
    });
    var reset = root.querySelector("[data-literature-reset]");
    if (reset) reset.addEventListener("click", function () { clearHighlight(root); setPhase(root, project, 7); });

    setPhase(root, project, 1);
    installStepObserver(root, project);
    window.requestAnimationFrame(function () { centerScrollableGraphic(root); });
  }

  function init() {
    var roots = Array.prototype.slice.call(document.querySelectorAll("[data-literature-map]"));
    if (!roots.length) return;
    roots.forEach(function (root) { root.setAttribute("aria-busy", "true"); });

    fetch(DATA_URL)
      .then(function (response) {
        if (!response.ok) throw new Error("Literature map data request failed");
        return response.json();
      })
      .then(function (data) {
        roots.forEach(function (root) {
          render(root, root.getAttribute("data-literature-map"), data);
        });
      })
      .catch(function () {
        roots.forEach(function (root) {
          root.setAttribute("aria-busy", "false");
          root.innerHTML = '<p class="literature-map__fallback">Literature map could not load. The full references remain available below.</p>';
        });
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}());
