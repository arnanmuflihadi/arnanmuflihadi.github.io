/*
  Collapsible methodology summaries
  ---------------------------------
  Add data-method-collapsible to a prose container whose paragraphs start with
  <strong>Section title.</strong>. The script groups each titled paragraph and
  its following content into a native <details> block. Without JavaScript, the
  original full text remains visible.
*/
(function () {
  "use strict";

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function isElement(node) {
    return node && node.nodeType === 1;
  }

  function headingStrong(paragraph) {
    if (!isElement(paragraph) || paragraph.tagName !== "P") return null;
    var first = paragraph.firstElementChild;
    return first && first.tagName === "STRONG" ? first : null;
  }

  function cleanHeading(text) {
    return String(text || "")
      .replace(/[:.]\s*$/, "")
      .trim();
  }

  function summarizeParagraph(paragraph, heading) {
    var clone = paragraph.cloneNode(true);
    var strong = clone.querySelector("strong");
    if (strong) strong.remove();
    var text = clone.textContent.replace(/\s+/g, " ").trim();
    if (!text) text = heading;
    if (text.length > 154) text = text.slice(0, 151).trim() + "...";
    return text;
  }

  function enhance(container) {
    if (!container || container.dataset.methodEnhanced === "true") return;
    var children = Array.prototype.slice.call(container.children);
    var groups = [];
    var current = null;
    var intro = [];

    children.forEach(function (child) {
      var strong = headingStrong(child);
      if (strong) {
        current = {
          title: cleanHeading(strong.textContent),
          summary: summarizeParagraph(child, strong.textContent),
          nodes: [child]
        };
        groups.push(current);
      } else if (current) {
        current.nodes.push(child);
      } else {
        intro.push(child);
      }
    });

    if (groups.length < 2) return;
    container.dataset.methodEnhanced = "true";
    container.textContent = "";

    intro.forEach(function (node) {
      container.appendChild(node);
    });

    groups.forEach(function (group, index) {
      var details = document.createElement("details");
      details.className = "method-fold";
      details.style.setProperty("--fold-index", index);

      var summary = document.createElement("summary");
      summary.innerHTML = [
        '<span class="method-fold__title">',
        escapeHtml(group.title),
        "</span>",
        '<small class="method-fold__summary">',
        escapeHtml(group.summary),
        "</small>",
        '<span class="method-fold__icon" aria-hidden="true">expand_more</span>'
      ].join("");

      var body = document.createElement("div");
      body.className = "method-fold__body";
      group.nodes.forEach(function (node) {
        body.appendChild(node);
      });

      details.appendChild(summary);
      details.appendChild(body);
      details.addEventListener("toggle", function () {
        details.classList.toggle("is-open", details.open);
      });
      container.appendChild(details);
    });
  }

  function init() {
    document.querySelectorAll("[data-method-collapsible]").forEach(enhance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
