/**
 * The spurious-signal autopsy: how a gaudy t-statistic dies under audit (assets/autopsy-viz.js)
 *
 * The Q1-checkpoint synthesis widget. A "discovery" arrives with a headline t-statistic (t0). We
 * then subject it to the two statistical-hygiene audits of the quarter, in order, and watch the
 * honest t collapse:
 *   1. Reported t                  = t0                         (what the notebook proudly prints)
 *   2. - Overlap (Newey-West)      = t0 / INFL                  (Lesson 009: overlapping/persistent
 *                                                                errors inflate the naïve SE by INFL,
 *                                                                so the honest t is smaller)
 *   3. - Search (best-of-M)        = t_nw - E[max of M nulls]   (Lesson 007: the t was the best of M
 *                                                                tried signals; the fair bar is the
 *                                                                expected maximum of M draws under H0,
 *                                                                not 1.96 — subtract it as a haircut)
 * A dashed line marks the naïve single-test bar t = 1.96. The slider sets M (log scale, 1 -> 1000).
 * E[max of M standard normals] is computed by direct numerical integration of ∫ x·M·φ(x)·Φ(x)^{M-1} dx
 * (not a crude √(2 ln M) asymptotic), so small-M values are honest.
 *
 * Usage:
 *   <div id="autopsy"></div>
 *   <script src="../assets/autopsy-viz.js"></script>
 *   Autopsy.mount(document.getElementById("autopsy"), { t0: 6.2, infl: 2.7, m: 50 });
 *
 * Expected state: with t0 = 6.2 and INFL = 2.7 the overlap audit alone drops t to ≈ 2.3 (still
 * "significant"). At M = 1 the survivor is ≈ 2.3 (a real, marginal edge). At M = 10 the best-of-M
 * bar is ≈ 1.54, so the survivor ≈ 0.76 -> DEAD. At M = 50 (default) and M = 100 it is at/below
 * zero -> DEAD: the "discovery" was a heteroskedastic, overlap-inflated, cherry-picked mirage.
 */
(function (global) {
  "use strict";

  // Standard normal pdf / cdf (Abramowitz-Stegun 26.2.17, |err| < 7.5e-8).
  function phi(x) { return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI); }
  function Phi(x) {
    if (x < 0) return 1 - Phi(-x);
    var t = 1 / (1 + 0.2316419 * x);
    var d = phi(x);
    var p = d * t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 +
            t * (-1.821255978 + t * 1.330274429))));
    return 1 - p;
  }
  // E[max of M i.i.d. standard normals] = ∫ x·M·φ(x)·Φ(x)^{M-1} dx (numeric).
  function expectedMax(M) {
    if (M <= 1) return 0;
    var lo = -6, hi = 9, steps = 1500, dx = (hi - lo) / steps, s = 0;
    for (var i = 0; i <= steps; i++) {
      var x = lo + i * dx;
      var w = (i === 0 || i === steps) ? 0.5 : 1; // trapezoid
      s += w * x * M * phi(x) * Math.pow(Phi(x), M - 1);
    }
    return s * dx;
  }

  function mount(container, config) {
    config = config || {};
    var t0 = config.t0 == null ? 6.2 : config.t0;      // headline reported t-stat
    var INFL = config.infl == null ? 2.7 : config.infl; // Newey-West SE inflation (overlap)
    var m0 = config.m == null ? 50 : config.m;          // number of strategies searched
    var BAR = 1.96;                                      // naïve single-test threshold

    container.innerHTML = "";
    container.classList.add("autopsy-viz");

    var readout = document.createElement("div");
    readout.className = "autopsy-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "autopsy-canvas";
    var W = 460, H = 260;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "autopsy-controls";
    var lab = document.createElement("span");
    lab.className = "autopsy-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "0"; slider.max = "100"; slider.step = "1";
    // map M -> slider position on a log10 scale over [1, 1000]
    slider.value = String(Math.round(100 * Math.log10(Math.max(1, m0)) / 3));
    slider.className = "autopsy-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    var ctx = canvas.getContext("2d");
    var padL = 40, padR = 14, padT = 28, padB = 50;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var yMax = Math.max(7, Math.ceil(t0));
    function py(t) { return padT + plotH - (Math.max(0, t) / yMax) * plotH; }

    function draw() {
      var pos = parseInt(slider.value, 10) / 100;      // 0..1
      var M = Math.max(1, Math.round(Math.pow(10, pos * 3))); // 1..1000
      var emax = expectedMax(M);

      var tReport = t0;
      var tNW = t0 / INFL;
      var tFinal = tNW - emax;                          // surviving margin over the best-of-M bar
      var alive = tFinal >= BAR;

      var bars = [
        { label: "Reported", t: tReport, sub: "naïve t", color: "#b23b3b" },
        { label: "\u2212 Overlap", t: tNW, sub: "Newey\u2013West", color: "#c98a1a" },
        { label: "\u2212 Search", t: Math.max(0, tFinal), sub: "best-of-" + M, color: alive ? "#0d5c4b" : "#b23b3b" }
      ];

      ctx.clearRect(0, 0, W, H);

      // y-axis ticks
      ctx.fillStyle = "#5a635f"; ctx.font = "10px system-ui, sans-serif";
      ctx.strokeStyle = "#efece3"; ctx.lineWidth = 1;
      for (var g = 0; g <= yMax; g++) {
        var gy = py(g);
        ctx.beginPath(); ctx.moveTo(padL, gy); ctx.lineTo(W - padR, gy); ctx.stroke();
        ctx.fillText(String(g), 6, gy + 3);
      }

      // bars
      var slot = plotW / bars.length;
      var bw = slot * 0.5;
      for (var i = 0; i < bars.length; i++) {
        var b = bars[i];
        var cx = padL + slot * (i + 0.5);
        var x0 = cx - bw / 2;
        var top = py(b.t);
        ctx.fillStyle = b.color;
        ctx.fillRect(x0, top, bw, py(0) - top);
        // value on top
        ctx.fillStyle = "#2b2b2b"; ctx.font = "bold 12px system-ui, sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(b.t.toFixed(2), cx, top - 6);
        // labels under axis
        ctx.fillStyle = "#2b2b2b"; ctx.font = "11px system-ui, sans-serif";
        ctx.fillText(b.label, cx, H - 28);
        ctx.fillStyle = "#5a635f"; ctx.font = "10px system-ui, sans-serif";
        ctx.fillText(b.sub, cx, H - 15);
        ctx.textAlign = "left";
      }

      // significance line t = 1.96
      var by = py(BAR);
      ctx.strokeStyle = "#7a7f7c"; ctx.lineWidth = 1.2;
      ctx.setLineDash([5, 4]);
      ctx.beginPath(); ctx.moveTo(padL, by); ctx.lineTo(W - padR, by); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#5a635f"; ctx.font = "10px system-ui, sans-serif";
      ctx.fillText("t = 1.96", W - padR - 46, by - 4);

      lab.textContent = "strategies searched M = " + M;
      readout.innerHTML =
        "Reported <strong>" + tReport.toFixed(2) + "</strong> \u2192 " +
        "after Newey\u2013West <strong>" + tNW.toFixed(2) + "</strong> (overlap SE \u00d7" + INFL.toFixed(1) + ") \u2192 " +
        "minus the best-of-" + M + " bar (E[max]=" + emax.toFixed(2) + ") = " +
        "<strong>" + tFinal.toFixed(2) + "</strong>. " +
        "<span class=\"autopsy-verdict " + (alive ? "alive" : "dead") + "\">" +
        (alive ? "Survives the audit." : "DEAD \u2014 spurious.") + "</span>";
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw };
  }

  global.Autopsy = { mount: mount };
})(window);
