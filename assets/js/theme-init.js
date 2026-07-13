/* Apply the saved/system theme before CSS paint to avoid a light-mode flash. */
(function () {
  "use strict";
  try {
    var saved = window.localStorage.getItem("theme");
    var systemDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.setAttribute("data-theme", saved || (systemDark ? "dark" : "light"));
  } catch (error) {
    document.documentElement.setAttribute("data-theme", "light");
  }
})();
