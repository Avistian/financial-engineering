/**
 * Bias–variance dartboard (assets/biasvariance-viz.js)
 *
 * Renders the classic 2x2 of estimator behaviour on a target whose bullseye is the TRUE
 * parameter. Each shot is one estimate from one sample; the cluster's CENTRE (hollow ring)
 * is the estimator's expected value, so its distance from the bullseye is BIAS and the
 * spread of shots is VARIANCE. The four panels are:
 *   - low bias,  low variance   (accurate + precise — what you want)
 *   - low bias,  high variance  (unbiased but noisy)
 *   - high bias, low variance   (precise but wrong — the seductive trap)
 *   - high bias, high variance  (wrong and noisy)
 *
 * Deterministic given a seed; "Re-sample shots" reseeds so the scatter changes but the
 * bias/variance character of each panel stays fixed.
 *
 * Usage:
 *   <div id="bv"></div>
 *   <script src="../assets/biasvariance-viz.js"></script>
 *   BiasVariance.mount(document.getElementById("bv"), { seed: 7 });
 *
 * Expected state: four square targets in a responsive grid (2x2 on desktop, still 2x2 and
 * readable at 375px), each with a caption; a button re-draws the shots.
 */
(function (global) {
  "use strict";

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Standard normal via Box–Muller, driven by a uniform RNG.
  function gauss(rng) {
    var u = 1 - rng(), v = 1 - rng();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  var PANELS = [
    { key: "ll", title: "Low bias · low variance", note: "accurate & precise", bias: 0.00, spread: 0.10 },
    { key: "lh", title: "Low bias · high variance", note: "unbiased but noisy", bias: 0.00, spread: 0.30 },
    { key: "hl", title: "High bias · low variance", note: "precise but wrong", bias: 0.45, spread: 0.10 },
    { key: "hh", title: "High bias · high variance", note: "wrong & noisy", bias: 0.45, spread: 0.30 }
  ];

  function drawPanel(canvas, panel, rng) {
    var css = 150;
    var dpr = global.devicePixelRatio || 1;
    canvas.width = css * dpr;
    canvas.height = css * dpr;
    canvas.style.width = css + "px";
    canvas.style.height = css + "px";
    var ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, css, css);

    var cx = css / 2, cy = css / 2;
    var R = css / 2 - 6; // outer ring radius; parameter space maps [-1,1] -> [-R,R]

    // Concentric rings.
    var rings = [1.0, 0.66, 0.33];
    ctx.lineWidth = 1;
    rings.forEach(function (f, i) {
      ctx.beginPath();
      ctx.arc(cx, cy, R * f, 0, 2 * Math.PI);
      ctx.strokeStyle = i === rings.length - 1 ? "#0d5c4b" : "#d9d6cd";
      ctx.stroke();
    });
    // Bullseye = the true parameter.
    ctx.beginPath();
    ctx.arc(cx, cy, 3, 0, 2 * Math.PI);
    ctx.fillStyle = "#0d5c4b";
    ctx.fill();
    // Cross-hairs.
    ctx.strokeStyle = "#e6f2ef";
    ctx.beginPath();
    ctx.moveTo(cx - R, cy); ctx.lineTo(cx + R, cy);
    ctx.moveTo(cx, cy - R); ctx.lineTo(cx, cy + R);
    ctx.stroke();

    // Bias direction fixed (down-right) so panels are comparable.
    var bx = panel.bias * 0.7071, by = panel.bias * 0.7071;
    var n = 24, sx = 0, sy = 0;
    for (var i = 0; i < n; i++) {
      var px = bx + panel.spread * gauss(rng);
      var py = by + panel.spread * gauss(rng);
      sx += px; sy += py;
      var X = cx + px * R, Y = cy + py * R;
      ctx.beginPath();
      ctx.arc(X, Y, 2.4, 0, 2 * Math.PI);
      ctx.fillStyle = "rgba(154,107,31,0.75)"; // gold shots
      ctx.fill();
    }
    // Centroid = estimator's expected value; its gap from bullseye is the bias.
    var mx = cx + (sx / n) * R, my = cy + (sy / n) * R;
    ctx.beginPath();
    ctx.arc(mx, my, 5, 0, 2 * Math.PI);
    ctx.lineWidth = 2;
    ctx.strokeStyle = "#922b21";
    ctx.stroke();
  }

  function mount(container, config) {
    config = config || {};
    var baseSeed = config.seed || 7;

    container.innerHTML = "";
    container.classList.add("bv-viz");

    var grid = document.createElement("div");
    grid.className = "bv-grid";
    container.appendChild(grid);

    var canvases = [];
    PANELS.forEach(function (panel) {
      var cell = document.createElement("figure");
      cell.className = "bv-cell";
      var cv = document.createElement("canvas");
      cell.appendChild(cv);
      var cap = document.createElement("figcaption");
      cap.innerHTML = "<strong>" + panel.title + "</strong><span>" + panel.note + "</span>";
      cell.appendChild(cap);
      grid.appendChild(cell);
      canvases.push(cv);
    });

    var legend = document.createElement("div");
    legend.className = "bv-legend";
    legend.innerHTML =
      "<span><i class=\"bv-dot bv-truth\"></i> true value (bullseye)</span>" +
      "<span><i class=\"bv-dot bv-shot\"></i> one estimate per sample</span>" +
      "<span><i class=\"bv-dot bv-mean\"></i> average estimate (bias = gap to bullseye)</span>";
    container.appendChild(legend);

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "bv-btn";
    btn.textContent = "Re-sample shots";
    container.appendChild(btn);

    var draw = function (seed) {
      canvases.forEach(function (cv, i) {
        drawPanel(cv, PANELS[i], mulberry32(seed + i * 101));
      });
    };
    draw(baseSeed);

    var clicks = 0;
    btn.addEventListener("click", function () {
      clicks += 1;
      draw(baseSeed + clicks * 977);
    });

    return { redraw: draw };
  }

  global.BiasVariance = { mount: mount };
})(window);
