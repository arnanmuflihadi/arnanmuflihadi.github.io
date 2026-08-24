/* Apply the saved/system theme before CSS paint to avoid a light-mode flash. */
(function () {
  "use strict";
  try {
    var saved = window.localStorage.getItem("theme");
    document.documentElement.setAttribute("data-theme", saved === "dark" ? "dark" : "light");
  } catch (error) {
    document.documentElement.setAttribute("data-theme", "light");
  }
})();
