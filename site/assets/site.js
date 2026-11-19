/* Symbology site — cookies, links, page automation. No backend. */
(function () {
  "use strict";

  var STATE_COOKIE = "auc_state";
  var DAYS = 180;

  function readState() {
    var m = document.cookie.match(new RegExp("(?:^|; )" + STATE_COOKIE + "=([^;]*)"));
    if (!m) return { v: [], last: null, tour: false };
    try {
      var s = JSON.parse(decodeURIComponent(m[1]));
      return {
        v: Array.isArray(s.v) ? s.v : [],
        last: s.last || null,
        tour: !!s.tour
      };
    } catch (err) {
      return { v: [], last: null, tour: false };
    }
  }

  function writeState(s) {
    if (s.v.length > 80) s.v = s.v.slice(-80);
    document.cookie = STATE_COOKIE + "=" + encodeURIComponent(JSON.stringify(s)) +
      "; path=/; max-age=" + (DAYS * 86400) + "; SameSite=Lax";
  }

  var state = readState();
  var pageId = document.body.getAttribute("data-page") || "";

  function visit(id) {
    if (!id || state.v.indexOf(id) !== -1) return;
    state.v.push(id);
    writeState(state);
    paintBar();
  }

  function remember(unitId) {
    state.last = { page: pageId, unit: unitId || null, at: Date.now() };
    writeState(state);
  }

  function paintBar() {
    var bar = document.getElementById("cookiebar");
    if (!bar) return;
    var parts = [];
    parts.push(state.v.length + (state.v.length === 1 ? " unit visited" : " units visited"));
    if (state.tour) parts.push("tour on");
    bar.textContent = parts.join(" \u00b7 ");
    var cont = document.getElementById("continue");
    if (cont && state.last) {
      var target = state.last.page + (state.last.unit ? "#u-" + state.last.unit : "");
      cont.setAttribute("href", target);
      cont.textContent = "Continue at " + (state.last.unit ? state.last.unit : state.last.page);
    }
  }

  /* ------------------------------------------------------------ walking */
  var walkTimer = null;
  var walkIndex = 0;

  function rows() {
    return Array.prototype.slice.call(document.querySelectorAll("tr.row"));
  }

  function activate(index, scroll) {
    var list = rows();
    if (!list.length) return;
    if (index < 0) index = list.length - 1;
    if (index >= list.length) index = 0;
    walkIndex = index;
    list.forEach(function (row, i) {
      row.classList.toggle("is-active", i === index);
    });
    var row = list[index];
    if (scroll) row.scrollIntoView({ block: "center", behavior: "smooth" });
    row.focus({ preventScroll: true });
    var unit = row.getAttribute("data-unit");
    if (unit) visit(unit);
    remember(unit);
  }

  function startWalk(delay) {
    stopWalk();
    var list = rows();
    if (!list.length) return;
    var start = 0;
    list.forEach(function (row, i) {
      if (row.classList.contains("is-active")) start = i;
    });
    activate(start, true);
    walkTimer = setInterval(function () {
      if (walkIndex + 1 >= rows().length) {
        stopWalk();
        return;
      }
      activate(walkIndex + 1, true);
    }, delay || 2200);
  }

  function stopWalk() {
    if (walkTimer) clearInterval(walkTimer);
    walkTimer = null;
  }

  /* ------------------------------------------------------------ the tour */
  var tourTimer = null;
  var tourLeft = 0;

  function nextHref() {
    var link = document.querySelector('.pagenav a[rel="next"]');
    return link ? link.getAttribute("href") : null;
  }

  function tickTour() {
    tourLeft -= 1;
    var bar = document.getElementById("cookiebar");
    if (bar) {
      bar.textContent = "tour on \u00b7 next page in " + tourLeft + "s";
    }
    if (tourLeft <= 0) {
      var href = nextHref();
      if (!href) {
        stopTour();
        return;
      }
      location.href = href;
    }
  }

  function startTour() {
    var href = nextHref();
    if (!href) return;
    state.tour = true;
    writeState(state);
    paintBar();
    tourLeft = 6;
    if (tourTimer) clearInterval(tourTimer);
    tourTimer = setInterval(tickTour, 1000);
    var bar = document.getElementById("cookiebar");
    if (bar) bar.textContent = "tour on \u00b7 next page in 6s";
  }

  function stopTour() {
    if (tourTimer) clearInterval(tourTimer);
    tourTimer = null;
    state.tour = false;
    writeState(state);
    paintBar();
  }

  /* ------------------------------------------------------------ wiring */
  document.addEventListener("click", function (event) {
    var walkButton = event.target.closest("[data-walk]");
    if (walkButton) {
      if (walkButton.getAttribute("data-walk") === "start") startWalk(2200);
      else stopWalk();
      return;
    }
    var tourButton = event.target.closest("[data-tour]");
    if (tourButton) {
      if (tourButton.getAttribute("data-tour") === "start") startTour();
      else stopTour();
      return;
    }
    var deconstruct = event.target.closest(".deconstruct");
    if (deconstruct) {
      var expr = deconstruct.getAttribute("data-expr") || "";
      document.cookie = "auc_handoff=" + encodeURIComponent(expr) +
        "; path=/; max-age=600; SameSite=Lax";
      location.href = "../learner.html";
      return;
    }
    var link = event.target.closest("a[href^='#u-']");
    if (link) {
      var id = link.getAttribute("href").replace("#u-", "");
      visit(id);
      remember(id);
    }
  });

  document.addEventListener("keydown", function (event) {
    var tag = (event.target.tagName || "").toLowerCase();
    if (tag === "textarea" || tag === "input" || tag === "select") return;
    if (event.key === "j" || event.key === "ArrowDown") {
      event.preventDefault();
      stopWalk();
      activate(walkIndex + 1, true);
    } else if (event.key === "k" || event.key === "ArrowUp") {
      event.preventDefault();
      stopWalk();
      activate(walkIndex - 1, true);
    } else if (event.key === "Enter") {
      var active = document.querySelector("tr.row.is-active");
      var related = active && active.querySelector("td.def .rel a");
      if (related) {
        event.preventDefault();
        related.click();
      }
    } else if (event.key === "Escape") {
      stopWalk();
    }
  });

  document.addEventListener("focusin", function (event) {
    var row = event.target.closest && event.target.closest("tr.row");
    if (!row) return;
    var list = rows();
    walkIndex = list.indexOf(row);
    list.forEach(function (r, i) { r.classList.toggle("is-active", i === walkIndex); });
    var unit = row.getAttribute("data-unit");
    if (unit) visit(unit);
    remember(unit);
  });

  /* ------------------------------------------------------------ on load */
  paintBar();

  if (state.tour) {
    tourLeft = 6;
    tourTimer = setInterval(tickTour, 1000);
  }

  var hash = location.hash;
  if (hash && hash.indexOf("#u-") === 0) {
    var row = document.getElementById(hash.slice(1));
    if (row) {
      var list = rows();
      walkIndex = list.indexOf(row);
      row.classList.add("is-active");
      row.scrollIntoView({ block: "center" });
    }
  }

  // a page visit is a visit to every unit on it, once the reader has been there
  // a moment — this keeps the cookie small on the large ASCII pages
  setTimeout(function () {
    rows().slice(0, 40).forEach(function (row) {
      var unit = row.getAttribute("data-unit");
      if (unit) visit(unit);
    });
    remember(null);
  }, 1500);
})();
