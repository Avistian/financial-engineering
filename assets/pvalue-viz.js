/**
 * The p-value as a tail area under the null (assets/pvalue-viz.js)
 *
 * Draws the sampling distribution of a test statistic *assuming the null hypothesis is true*
 * (H0: no edge). For a t-statistic on a reasonably long sample this is ~ standard normal. The
 * learner drags the observed statistic |t| and watches the shaded tail(s) — that shaded area IS
 * the (two-sided) p-value: the probability, if there were truly no edge, of seeing a statistic at
 * least this extreme. The faint band beyond ±1.96 marks the classic 5% rejection region, so the
 * learner sees "p < 0.05" as "the observed line sits outside the ±1.96 fences."
 *
 * Usage:
 *   <div id="pval"></div>
 *   <script src="../assets/pvalue-viz.js"></script>
 *   PValue.mount(document.getElementById("pval"), { t: 1.4 });
 *
 * Expected state: default observed |t| ≈ 1.4 → p ≈ 0.16 (not significant, line inside the fences).
 * Sliding to |t| = 1.96 gives p ≈ 0.05; |t| = 3.0 gives p ≈ 0.0027 (deep in the tail).
 */
(function (global) {
  "use strict";

  // Standard normal pdf and cdf (erf via Abramowitz-Stegun 7.1.26, |err| < 1.5e-7).
  function pdf(x) { return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI); }
  function erf(x) {
    var s = x < 0 ? -1 : 1; x = Math.abs(x);
    var t = 1 / (1 + 0.3275911 * x);
    var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return s * y;
  }
  function cdf(x) { return 0.5 * (1 + erf(x / Math.SQRT2)); }

  var XMIN = -4, XMAX = 4, W = 460, H = 210;

  function mount(container, config) {
    config = config || {};
    var tObs = config.t != null ? config.t : 1.4;

    container.innerHTML = "";
    container.classList.add("pval-viz");

    var readout = document.createElement("div");
    readout.className = "pval-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "pval-canvas";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "pval-controls";
    var lab = document.createElement("span");
    lab.className = "pval-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "0"; slider.max = "4"; slider.step = "0.05";
    slider.value = String(tObs); slider.className = "pval-slider";
    controls.appendChild(lab); controls.appendChild(slider);
    container.appendChild(controls);

    function xpix(x) {
      var pad = 10;
      return pad + (x - XMIN) / (XMAX - XMIN) * (W - 2 * pad);
    }
    var ymax = pdf(0) * 1.12;
    function ypix(y) {
      var top = 14, base = H - 24;
      return base - (y / ymax) * (base - top);
    }

    function draw() {
      var t = Math.abs(parseFloat(slider.value));
      var dpr = global.devicePixelRatio || 1;
      canvas.width = W * dpr; canvas.height = H * dpr;
      canvas.style.width = "100%"; canvas.style.maxWidth = W + "px"; canvas.style.height = "auto";
      var ctx = canvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      var base = H - 24;

      // 5% rejection region (|x| > 1.96), faint red band under the curve.
      function fillRegion(a, b, color) {
        ctx.beginPath();
        ctx.moveTo(xpix(a), base);
        for (var x = a; x <= b + 1e-9; x += (b - a) / 60) ctx.lineTo(xpix(x), ypix(pdf(x)));
        ctx.lineTo(xpix(b), base); ctx.closePath();
        ctx.fillStyle = color; ctx.fill();
      }
      fillRegion(1.96, XMAX, "rgba(154,107,31,0.10)");
      fillRegion(XMIN, -1.96, "rgba(154,107,31,0.10)");

      // p-value tails (|x| > t), solid red.
      if (t < XMAX) { fillRegion(t, XMAX, "rgba(146,43,33,0.30)"); fillRegion(XMIN, -t, "rgba(146,43,33,0.30)"); }

      // the null curve
      ctx.beginPath();
      for (var x2 = XMIN; x2 <= XMAX + 1e-9; x2 += (XMAX - XMIN) / 240) {
        var px = xpix(x2), py = ypix(pdf(x2));
        if (x2 === XMIN) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.strokeStyle = "#3f5566"; ctx.lineWidth = 1.75; ctx.stroke();

      // axis
      ctx.strokeStyle = "#d9d6cd"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(xpix(XMIN), base); ctx.lineTo(xpix(XMAX), base); ctx.stroke();
      ctx.fillStyle = "#5a635f"; ctx.font = "10px system-ui, sans-serif"; ctx.textAlign = "center";
      [-3, -1.96, 0, 1.96, 3].forEach(function (v) {
        ctx.fillText(v === 1.96 ? "1.96" : (v === -1.96 ? "-1.96" : v.toFixed(0)), xpix(v), H - 8);
        ctx.strokeStyle = "#eee"; ctx.beginPath(); ctx.moveTo(xpix(v), base); ctx.lineTo(xpix(v), base + 3); ctx.stroke();
      });

      // ±1.96 critical fences (dashed gold)
      ctx.strokeStyle = "#9a6b1f"; ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
      [-1.96, 1.96].forEach(function (v) {
        ctx.beginPath(); ctx.moveTo(xpix(v), 14); ctx.lineTo(xpix(v), base); ctx.stroke();
      });
      ctx.setLineDash([]);

      // observed |t| lines (solid teal)
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 1.75;
      [-t, t].forEach(function (v) {
        ctx.beginPath(); ctx.moveTo(xpix(v), 14); ctx.lineTo(xpix(v), base); ctx.stroke();
      });
      ctx.fillStyle = "#0d5c4b"; ctx.font = "600 11px system-ui, sans-serif"; ctx.textAlign = "center";
      ctx.fillText("t = " + t.toFixed(2), xpix(t), 11);

      var p = 2 * (1 - cdf(t));
      var sig = p < 0.05;
      lab.textContent = "Observed |t| = " + t.toFixed(2);
      readout.innerHTML = "Two-sided p-value = shaded tail area = <strong>" + p.toFixed(4) +
        "</strong> — " + (sig
          ? "<span class=\"pval-sig\">below 0.05: the line is outside the ±1.96 fences (reject H0).</span>"
          : "<span class=\"pval-nsig\">above 0.05: inside the fences (cannot reject \u201cno edge\u201d).</span>");
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw };
  }

  global.PValue = { mount: mount };
})(window);
