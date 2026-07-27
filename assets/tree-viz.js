/**
 * Binomial PATH tree — information (filtration) and conditional expectation
 * (assets/tree-viz.js)
 *
 * One reusable component, mounted in two modes because it carries two different
 * mechanisms in Lesson 011:
 *
 *   mode: "filtration"  — the tree of PATHS (non-recombining: 2^t nodes at time t).
 *     Edges up to time t are solid ("already revealed"); later edges are faint.
 *     Shaded bands group the leaves that are still indistinguishable at time t —
 *     i.e. the ATOMS (cells) of F_t. Sliding t refines the partition: 1 cell of 8
 *     outcomes at t=0, then 2, 4, and finally 8 singletons at t=3. Readout reports
 *     the number of atoms (2^t) and the number of answerable yes/no questions
 *     (|F_t| = 2^(2^t)).
 *
 *   mode: "condexp"     — the same tree, but every node is labelled with the
 *     conditional expectation E[X | F_level] of the chosen payoff, obtained by
 *     backward averaging (each node = p·up-child + (1-p)·down-child). Level 3 is X
 *     itself; the highlighted column at time t is the random variable E[X | F_t],
 *     which is constant on each cell. Readout lists its values and re-averages them
 *     to demonstrate the tower property.
 *
 * Config:
 *   mode    "filtration" | "condexp"   (default "filtration")
 *   n       periods (default 3; the lesson uses 3 → 8 leaves)
 *   s0, u, d, p   binomial parameters (default 100, 1.1, 0.9, 0.5)
 *   payoff  "price" | "call"           (default "price"; "call" uses strike K)
 *   K       strike for the call payoff (default 100)
 *   t       initial slider value (default 1)
 *
 * Usage:
 *   <div id="filt"></div>
 *   <script src="../assets/tree-viz.js"></script>
 *   Tree.mount(document.getElementById("filt"), { mode: "filtration", t: 1 });
 *
 * Expected states (defaults, n=3, u=1.1, d=0.9, p=0.5):
 *   filtration: t=0 → 1 atom (all 8 paths), "you know nothing"; t=1 → 2 atoms of 4;
 *     t=2 → 4 atoms of 2; t=3 → 8 singletons, full information.
 *   condexp with payoff "call", K=100: leaves 33.1, 8.9, 8.9, 0, 8.9, 0, 0, 0;
 *     t=2 → 21.00, 4.45, 4.45, 0.00; t=1 → 12.725, 2.225; t=0 → 7.475 (= E[V]).
 *   condexp with payoff "price": every node equals its own S_t (E[S_3|F_t] = S_t),
 *     because (u+d)/2 = 1 makes the price a martingale under p = 0.5.
 */
(function (global) {
  "use strict";

  function pathLabel(idx, level) {
    // idx = index among the 2^level nodes at this level; bit (level-1-k) is flip k
    var s = "";
    for (var k = 0; k < level; k++) {
      var bit = (idx >> (level - 1 - k)) & 1;
      s += bit === 0 ? "H" : "T";
    }
    return s === "" ? "\u2014" : s;
  }

  function mount(container, config) {
    config = config || {};
    var mode = config.mode === "condexp" ? "condexp" : "filtration";
    var n = config.n || 3;
    var s0 = config.s0 == null ? 100 : config.s0;
    var u = config.u == null ? 1.1 : config.u;
    var d = config.d == null ? 0.9 : config.d;
    var p = config.p == null ? 0.5 : config.p;
    var payoff = config.payoff === "call" ? "call" : "price";
    var K = config.K == null ? 100 : config.K;
    var t0 = config.t == null ? 1 : config.t;

    container.innerHTML = "";
    container.classList.add("tree-viz");

    var readout = document.createElement("div");
    readout.className = "tree-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "tree-canvas";
    var W = 440, H = 300;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "tree-controls";
    var lab = document.createElement("span");
    lab.className = "tree-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "0"; slider.max = String(n); slider.step = "1";
    slider.value = String(Math.max(0, Math.min(n, t0)));
    slider.className = "tree-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    // ---- prices S[level][idx] on the PATH tree (bit 0 of the path = first flip) ----
    var S = [];
    for (var level = 0; level <= n; level++) {
      var row = [];
      for (var i = 0; i < (1 << level); i++) {
        var val = s0;
        for (var k = 0; k < level; k++) {
          var bit = (i >> (level - 1 - k)) & 1;
          val *= bit === 0 ? u : d;
        }
        row.push(val);
      }
      S.push(row);
    }

    // ---- X at the leaves, then backward averaging: V[level][idx] = E[X | F_level] ----
    var V = [];
    for (level = 0; level <= n; level++) V.push(new Array(1 << level).fill(0));
    for (i = 0; i < (1 << n); i++) {
      V[n][i] = payoff === "call" ? Math.max(S[n][i] - K, 0) : S[n][i];
    }
    for (level = n - 1; level >= 0; level--) {
      for (i = 0; i < (1 << level); i++) {
        V[level][i] = p * V[level + 1][2 * i] + (1 - p) * V[level + 1][2 * i + 1];
      }
    }

    var ctx = canvas.getContext("2d");
    var padL = 26, padR = 66, padT = 18, padB = 30;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var leaves = 1 << n;
    var leafH = plotH / leaves;
    var colW = plotW / n;

    function nodeX(level) { return padL + level * colW; }
    function nodeY(level, idx) {
      var span = leaves >> level;              // leaves under this node
      var first = idx * span;
      return padT + (first + span / 2) * leafH;
    }

    function fmt(v) {
      if (Math.abs(v) >= 100) return v.toFixed(1);
      if (Math.abs(v) >= 10) return v.toFixed(2);
      return v.toFixed(3).replace(/0$/, "");
    }

    function draw() {
      var t = parseInt(slider.value, 10);
      ctx.clearRect(0, 0, W, H);
      ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle";

      // ---- information cells (atoms of F_t): shaded bands over the leaves ----
      if (mode === "filtration") {
        var cells = 1 << t;
        var span = leaves >> t;
        for (var c = 0; c < cells; c++) {
          var y0 = padT + c * span * leafH;
          ctx.fillStyle = c % 2 === 0 ? "rgba(13,92,75,0.10)" : "rgba(154,107,31,0.10)";
          ctx.fillRect(nodeX(t), y0 + 1, W - padR - nodeX(t) + 52, span * leafH - 2);
          ctx.strokeStyle = "rgba(13,92,75,0.35)"; ctx.lineWidth = 1;
          ctx.strokeRect(nodeX(t), y0 + 1, W - padR - nodeX(t) + 52, span * leafH - 2);
        }
      }

      // ---- edges ----
      for (var level = 0; level < n; level++) {
        for (var i = 0; i < (1 << level); i++) {
          for (var b = 0; b < 2; b++) {
            var known = level < t;             // this flip has already been observed
            ctx.strokeStyle = known ? "#0d5c4b" : "#c9c4b6";
            ctx.lineWidth = known ? 1.6 : 1;
            ctx.beginPath();
            ctx.moveTo(nodeX(level) + 9, nodeY(level, i));
            ctx.lineTo(nodeX(level + 1) - 9, nodeY(level + 1, 2 * i + b));
            ctx.stroke();
          }
        }
      }

      // ---- nodes ----
      for (level = 0; level <= n; level++) {
        for (i = 0; i < (1 << level); i++) {
          var x = nodeX(level), y = nodeY(level, i);
          var value = mode === "condexp" ? V[level][i] : S[level][i];
          var highlight = mode === "condexp" ? (level === t) : (level <= t);
          var txt = fmt(value);
          var wBox = 8 + txt.length * 5.4;
          ctx.fillStyle = highlight ? "#e6f2ef" : "#fffdf8";
          ctx.strokeStyle = highlight ? "#0d5c4b" : "#c9c4b6";
          ctx.lineWidth = highlight ? 1.6 : 1;
          ctx.beginPath();
          if (ctx.roundRect) ctx.roundRect(x - wBox / 2, y - 8, wBox, 16, 3);
          else ctx.rect(x - wBox / 2, y - 8, wBox, 16);
          ctx.fill(); ctx.stroke();
          ctx.fillStyle = highlight ? "#17201d" : "#7d8480";
          ctx.textAlign = "center";
          ctx.fillText(txt, x, y);
        }
      }

      // ---- path labels at the right edge (the 8 outcomes of Omega) ----
      ctx.textAlign = "left";
      for (i = 0; i < leaves; i++) {
        ctx.fillStyle = "#5a635f";
        ctx.font = "10px 'SF Mono', Consolas, monospace";
        ctx.fillText(pathLabel(i, n), W - padR + 22, padT + (i + 0.5) * leafH);
      }

      // ---- time axis ----
      ctx.font = "10px system-ui, sans-serif";
      ctx.textAlign = "center";
      for (level = 0; level <= n; level++) {
        ctx.fillStyle = level === t ? "#0d5c4b" : "#8d938f";
        ctx.fillText("t=" + level, nodeX(level), H - 12);
      }

      // ---- readout ----
      var vals = V[t].map(fmt).join(", ");
      if (mode === "filtration") {
        var atoms = 1 << t;
        var perAtom = leaves >> t;
        var questions = Math.pow(2, atoms);
        lab.textContent = "information at time t = " + t;
        readout.innerHTML =
          "At <strong>t = " + t + "</strong> you have seen " + t + " flip" + (t === 1 ? "" : "s") +
          ". \u2131<sub>" + t + "</sub> has <strong>" + atoms + " atom" + (atoms === 1 ? "" : "s") +
          "</strong> (shaded), each still containing <strong>" + perAtom + "</strong> of the " + leaves +
          " outcomes \u2014 you cannot see <em>inside</em> a shaded band. " +
          "Yes/no questions you can answer: |\u2131<sub>" + t + "</sub>| = 2<sup>" + atoms + "</sup> = <strong>" +
          questions.toLocaleString() + "</strong>." +
          (t === 0
            ? " <span class=\"tree-note\">t=0: one atom = you know nothing but \u03a9 itself.</span>"
            : t === n
              ? " <span class=\"tree-note\">t=" + n + ": every atom is a single path \u2014 full information.</span>"
              : "");
      } else {
        var back = V[Math.max(0, t - 1)].map(fmt).join(", ");
        lab.textContent = "conditioning time t = " + t;
        readout.innerHTML =
          "<strong>E[X | \u2131<sub>" + t + "</sub>]</strong> takes the value" + (V[t].length === 1 ? " " : "s ") +
          "<strong>" + vals + "</strong> \u2014 one per atom of \u2131<sub>" + t + "</sub>, so it is a <em>random " +
          "variable</em>, constant on each cell. " +
          (t === n
            ? "<span class=\"tree-note\">At t=" + n + " nothing is left to average: E[X|\u2131<sub>" + n +
              "</sub>] = X.</span>"
            : "Each node is the average of its two children (p = " + p + ").") +
          (t > 0
            ? " Averaging these back one step reproduces E[X|\u2131<sub>" + (t - 1) + "</sub>] = " + back +
              " \u2014 <span class=\"tree-note\">the tower property.</span>"
            : " <span class=\"tree-note\">t=0: a single number, the unconditional E[X].</span>");
      }
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw, S: S, V: V };
  }

  global.Tree = { mount: mount };
})(window);
