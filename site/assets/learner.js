/* The learner: deconstruct a definition to its basic units, rebuild it, train.
 *
 * The model is small on purpose, and it runs entirely in the page:
 *
 *   attention  — every rule scores the words of the sentence it recognises;
 *                a softmax over those scores is the attention.
 *   binding    — an operand is bound to the unit whose definition shares the
 *                most words with it (the same overlap the pages use for links).
 *   perceptron — "right" / "wrong" nudges the word weights, and the weights
 *                live in a cookie, so the model keeps what it learned.
 */
(function () {
  "use strict";

  var CORPUS = window.AUC || { units: [], rules: [], combos: [], pages: [] };
  var W_COOKIE = "auc_model";
  var S_COOKIE = "auc_stats";
  var LR = 0.15;

  /* ------------------------------------------------------------- cookies */
  function readJSON(name, fallback) {
    var m = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
    if (!m) return fallback;
    try { return JSON.parse(decodeURIComponent(m[1])); } catch (e) { return fallback; }
  }
  function writeJSON(name, value, days) {
    document.cookie = name + "=" + encodeURIComponent(JSON.stringify(value)) +
      "; path=/; max-age=" + ((days || 180) * 86400) + "; SameSite=Lax";
  }
  function dropCookie(name) {
    document.cookie = name + "=; path=/; max-age=0; SameSite=Lax";
  }

  var W = readJSON(W_COOKIE, {});
  var stats = readJSON(S_COOKIE, { trials: 0, correct: 0 });

  /* ------------------------------------------------------------ features */
  function tokens(text) {
    return (String(text).toLowerCase().match(/[a-z][a-z\-]{1,}/g) || []);
  }
  function tokenSet(text) {
    var set = {};
    tokens(text).forEach(function (word) { set[word] = (set[word] || 0) + 1; });
    return set;
  }
  function normalize(text) {
    return String(text)
      .replace(/[\u00ab\u00bb]/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .replace(/[.\s]+$/, "");
  }

  var UNIT_INDEX = CORPUS.units.map(function (unit) {
    return { unit: unit, set: tokenSet(unit.def) };
  });

  function ruleKey(ruleId, word) { return ruleId + ":" + word; }

  function ruleScore(rule, set) {
    var score = 0;
    rule.trigger.forEach(function (word) {
      if (set[word]) score += 1 + (W[ruleKey(rule.id, word)] || 0);
    });
    var seen = {};
    tokens(rule.template).forEach(function (word) {
      if (seen[word]) return;
      seen[word] = 1;
      if (set[word]) score += 0.35;
    });
    return score;
  }

  function rankRules(text) {
    var set = tokenSet(text);
    var scored = CORPUS.rules.map(function (rule) {
      return { rule: rule, score: ruleScore(rule, set) };
    });
    var max = 0;
    scored.forEach(function (row) { if (row.score > max) max = row.score; });
    var total = 0;
    scored.forEach(function (row) {
      row.p = Math.exp((row.score - max));
      total += row.p;
    });
    scored.forEach(function (row) { row.p = row.p / total; });
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored;
  }

  function bindUnit(text) {
    var set = tokenSet(text);
    var words = Object.keys(set);
    var best = null;
    UNIT_INDEX.forEach(function (entry) {
      var mine = Object.keys(entry.set);
      var shared = 0;
      mine.forEach(function (word) { if (set[word]) shared += 1; });
      var union = mine.length + words.length - shared;
      var score = union ? shared / union : 0;
      if (!best || score > best.score) best = { unit: entry.unit, score: score };
    });
    return best && best.score >= 0.06 ? best : null;
  }

  /* -------------------------------------------------------------- parsing */
  function splitWith(rule, text) {
    var t = normalize(text);
    if (rule.arity === 1 && rule.affix) {
      var m = new RegExp(rule.affix, "i").exec(t);
      if (m) {
        var inner = (m.groups && m.groups.x) || m[1];
        if (inner) return [inner];
      }
      return null;
    }
    if (rule.arity === 2 && rule.glue) {
      var re = new RegExp(rule.glue, "i");
      var hit = re.exec(t);
      if (hit && hit.length >= 3) return [hit[1], hit[2]];
      var parts = t.split(re);
      if (parts.length === 2) return parts;
    }
    return null;
  }

  function leafNode(text) {
    var bound = bindUnit(text);
    var clean = normalize(text);
    return { kind: "leaf", text: clean, unit: bound ? bound.unit : null,
             placeholder: /^[pq]$/.test(clean),
             score: bound ? bound.score : 0 };
  }

  function parse(text, depth) {
    depth = depth || 0;
    if (depth > 6) return leafNode(text);
    var ranked = rankRules(text);
    for (var i = 0; i < ranked.length; i++) {
      if (ranked[i].p < 0.03) continue;
      var rule = ranked[i].rule;
      var parts = splitWith(rule, text);
      if (!parts) continue;
      var kids = parts.map(function (part) { return parse(part, depth + 1); });
      var unresolved = kids.filter(function (kid) {
        return kid.kind === "leaf" && !kid.unit && !kid.placeholder;
      });
      if (unresolved.length) continue;
      return { kind: "op", rule: rule, kids: kids, p: ranked[i].p, ranked: ranked };
    }
    return leafNode(text);
  }

  function rebuild(node) {
    if (node.kind === "leaf") return node.unit ? node.unit.def : node.text;
    var args = node.kids.map(rebuild);
    var out = node.rule.template;
    out = out.replace("{0}", "\u00ab" + args[0] + "\u00bb");
    if (args.length > 1) out = out.replace("{1}", "\u00ab" + args[1] + "\u00bb");
    return out;
  }

  function leaves(node, out) {
    out = out || [];
    if (node.kind === "leaf") out.push(node);
    else node.kids.forEach(function (kid) { leaves(kid, out); });
    return out;
  }

  function fidelity(input, rebuilt) {
    var a = tokenSet(input), b = tokenSet(rebuilt);
    var keys = Object.keys(a);
    var shared = 0;
    keys.forEach(function (word) { if (b[word]) shared += 1; });
    var union = keys.length + Object.keys(b).length - shared;
    return union ? shared / union : 0;
  }

  /* ------------------------------------------------------------ rendering */
  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  var SVG_NS = "http://www.w3.org/2000/svg";
  function svgEl(tag, attrs) {
    var node = document.createElementNS(SVG_NS, tag);
    Object.keys(attrs || {}).forEach(function (name) {
      node.setAttribute(name, attrs[name]);
    });
    return node;
  }

  function layout(node) {
    var cursor = { x: 0 };
    var nodes = [];
    var edges = [];

    function walk(n, depth) {
      n.depth = depth;
      if (n.kind === "leaf") {
        n.x = cursor.x * 150 + 60;
        cursor.x += 1;
      } else {
        n.kids.forEach(function (kid) { walk(kid, depth + 1); });
        n.x = (n.kids[0].x + n.kids[n.kids.length - 1].x) / 2;
      }
      nodes.push(n);
    }
    walk(node, 0);

    nodes.forEach(function (n) {
      if (n.kind === "op") {
        n.kids.forEach(function (kid) {
          edges.push({ x1: n.x, y1: n.depth * 76 + 34, x2: kid.x, y2: kid.depth * 76 + 18 });
        });
      }
    });
    return { nodes: nodes, edges: edges, width: Math.max(cursor.x * 150, 220),
             height: (Math.max.apply(null, nodes.map(function (n) { return n.depth; })) + 1) * 76 + 20 };
  }

  function drawTree(node) {
    var box = document.getElementById("ltree");
    box.innerHTML = "";
    var plan = layout(node);
    var svg = svgEl("svg", {
      viewBox: "0 0 " + plan.width + " " + plan.height,
      width: plan.width, height: plan.height,
      role: "img", "aria-label": "decomposition tree"
    });
    plan.edges.forEach(function (edge) {
      svg.appendChild(svgEl("line", {
        x1: edge.x1, y1: edge.y1, x2: edge.x2, y2: edge.y2
      }));
    });
    plan.nodes.forEach(function (n) {
      var y = n.depth * 76;
      if (n.kind === "leaf") {
        var label = n.unit ? n.unit.char + "  " + n.unit.name : (n.text || "?").slice(0, 22);
        var width = Math.min(146, Math.max(64, label.length * 7.4));
        var group = svgEl("g", { "class": "leaf" + (n.unit ? " is-picked" : "") });
        group.appendChild(svgEl("rect", {
          x: n.x - width / 2, y: y + 12, width: width, height: 34, rx: 8
        }));
        var text = svgEl("text", { x: n.x, y: y + 34, "text-anchor": "middle" });
        text.textContent = label;
        group.appendChild(text);
        if (n.unit) {
          group.appendChild(svgEl("title", {})).textContent =
            n.unit.name + " \u2014 " + n.unit.cp;
        }
        svg.appendChild(group);
      } else {
        var t = svgEl("text", { x: n.x, y: y + 8, "text-anchor": "middle" });
        t.textContent = n.rule.name;
        svg.appendChild(t);
      }
    });
    box.appendChild(svg);
  }

  function drawAttention(ranked, chosen) {
    var box = document.getElementById("lattn");
    box.innerHTML = "";
    ranked.slice(0, 7).forEach(function (row) {
      var line = el("div", "bar");
      line.appendChild(el("span", "", row.rule.name));
      var track = el("span", "track");
      var fill = el("span", "fill");
      fill.style.width = Math.max(1, Math.round(row.p * 100)) + "%";
      fill.style.opacity = row.rule === chosen ? "1" : "0.45";
      track.appendChild(fill);
      line.appendChild(track);
      line.appendChild(el("span", "num", Math.round(row.p * 100) + "%"));
      box.appendChild(line);
    });
  }

  function drawStats() {
    var box = document.getElementById("lstats");
    box.innerHTML = "";
    var accuracy = stats.trials ? Math.round((stats.correct / stats.trials) * 100) : 0;
    var pairs = [
      ["trials", stats.trials],
      ["right", stats.correct],
      ["accuracy", accuracy + "%"],
      ["weights", Object.keys(W).length]
    ];
    pairs.forEach(function (pair) {
      var span = el("span");
      span.appendChild(el("b", "", String(pair[1])));
      span.appendChild(document.createTextNode(" " + pair[0]));
      box.appendChild(span);
    });
    var model = document.getElementById("lmodel");
    var keys = Object.keys(W).sort();
    model.textContent = keys.length
      ? keys.map(function (k) { return k + "  " + W[k].toFixed(2); }).join("\n")
      : "no weights yet \u2014 every rule starts at its own word count";
  }

  /* ------------------------------------------------------------ the run */
  var current = null;

  function run(text) {
    var status = document.getElementById("lstatus");
    var clean = normalize(text);
    if (!clean) {
      status.className = "status bad";
      status.textContent = "Type a definition first.";
      return;
    }
    var ranked = rankRules(clean);
    var tree = parse(clean);
    current = { text: clean, tree: tree, ranked: ranked };

    drawTree(tree);
    drawAttention(ranked, tree.kind === "op" ? tree.rule : null);

    var built = rebuild(tree);
    var score = fidelity(clean, built);
    var units = leaves(tree);
    var named = units.filter(function (leaf) { return leaf.unit; });

    var fidelityBox = document.getElementById("lfidelity");
    fidelityBox.textContent =
      units.length + " basic unit" + (units.length === 1 ? "" : "s") +
      " (" + named.length + " matched) \u00b7 rebuild fidelity " +
      Math.round(score * 100) + "%" +
      (score > 0.999 ? " \u2014 exact round trip" : "");

    status.className = "status good";
    status.textContent = tree.kind === "op"
      ? "Top rule: " + tree.rule.name + " at " + Math.round(tree.p * 100) + "% attention."
      : "No rule fits; read as one unit.";
    drawStats();
  }

  function train(good) {
    if (!current) return;
    var tree = current.tree;
    var status = document.getElementById("lstatus");
    if (tree.kind !== "op") {
      status.className = "status bad";
      status.textContent = "Nothing to train: no rule was applied.";
      return;
    }
    var set = tokenSet(current.text);
    CORPUS.rules.forEach(function (rule) {
      var present = rule.trigger.filter(function (word) { return set[word]; });
      present.forEach(function (word) {
        var key = ruleKey(rule.id, word);
        var delta = rule === tree.rule ? (good ? 1 : -1) : (good ? -0.25 : 0.25);
        W[key] = (W[key] || 0) + LR * delta;
        if (Math.abs(W[key]) < 0.001) delete W[key];
      });
    });
    stats.trials += 1;
    if (good) stats.correct += 1;
    writeJSON(W_COOKIE, W);
    writeJSON(S_COOKIE, stats);
    status.className = "status good";
    status.textContent = good
      ? "Reinforced " + tree.rule.name + "."
      : "Moved weight away from " + tree.rule.name + ".";
    run(current.text);
  }

  /* ------------------------------------------------------------- wiring */
  var input = document.getElementById("ldef");

  document.getElementById("ldeconstruct").addEventListener("click", function () {
    run(input.value);
  });
  document.getElementById("lreconstruct").addEventListener("click", function () {
    if (!current) run(input.value);
    if (!current) return;
    var built = rebuild(current.tree);
    document.getElementById("lfidelity").textContent =
      "Rebuilt: " + built;
  });
  document.getElementById("lexample").addEventListener("click", function () {
    var pick = CORPUS.combos[Math.floor(Math.random() * CORPUS.combos.length)];
    if (!pick) return;
    input.value = pick.definition;
    run(pick.definition);
  });
  document.getElementById("lreset").addEventListener("click", function () {
    W = {};
    stats = { trials: 0, correct: 0 };
    dropCookie(W_COOKIE);
    dropCookie(S_COOKIE);
    drawStats();
    if (current) run(current.text);
  });
  document.getElementById("lfeedback").addEventListener("click", function (event) {
    var button = event.target.closest("[data-feedback]");
    if (!button) return;
    train(button.getAttribute("data-feedback") === "1");
  });

  /* a combination page can hand a definition straight over */
  var handoff = readJSON("auc_handoff", null);
  if (handoff) {
    dropCookie("auc_handoff");
    input.value = handoff;
    run(handoff);
  } else {
    drawStats();
    var first = CORPUS.combos[0];
    if (first) input.placeholder = first.definition;
  }
})();
