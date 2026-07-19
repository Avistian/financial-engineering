/**
 * The rising significance bar / t-stat haircut (assets/haircut-viz.js)
 *
 * When you search over M strategies, keeping the overall false-positive rate at 5% forces the
 * per-test hurdle far above the familiar single-test t = 1.96. This plots the required two-sided
 * |t| threshold against the number of independent tests M (log x-axis, 1 → 1000) for the
 * Bonferroni rule (per-test p = 0.05/M). A flat reference line marks the naive single-test 1.96,
 * and a second marks Harvey-Liu-Zhu's recommended ~3.0 hurdle for a "new factor." Hover/point moves
 * a marker along the Bonferroni curve; the readout reports the hurdle at the selected M and how
 * much a nominal t = 2.5 "discovery" gets haircut once the search is accounted for.
 *
 * Usage:
 *   <div id="hc"></div>
 *   <script src="../assets/haircut-viz.js"></script>
 *   Haircut.mount(document.getElementById("hc"), { m: 100 });
 *
 * Expected state: at M = 1 the Bonferroni curve sits on 1.96; at M = 100 it is ≈ 3.5 (above the
 * HLZ 3.0 line); at M = 1000 it is ≈ 4.0. So a t = 2.5 found after trying 100 ideas is NOT
 * significant once corrected — that is the haircut.
 */
(function (global) {
  "use strict";

  // Inverse standard normal CDF (Acklam's rational approximation, |err| < 1.15e-9).
  function normInv(p) {
    if (p <= 0) return -Infinity; if (p >= 1) return Infinity;
    var a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02, 1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00];
    var b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02, 6.680131188771972e+01, -1.328068155288572e+01];
    var c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00, -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00];
    var d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00];
    var plow = 0.02425, phigh = 1 - plow, q, r;
    if (p < plow) { q = Math.sqrt(-2 * Math.log(p)); return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1); }
    if (p <= phigh) { q = p - 0.5; r = q * q; return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1); }
    q = Math.sqrt(-2 * Math.log(1 - p)); return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
  }
  // Bonferroni two-sided |t| hurdle for M tests at overall level alpha.
  function hurdle(M, alpha) { return normInv(1 - (alpha / M) / 2); }

  var W = 460, H = 250, ALPHA = 0.05;
  var MMIN = 1, MMAX = 1000, TMIN = 1.5, TMAX = 4.2;

  function mount(container, config) {
    config = config || {};
    var mSel = config.m || 100;

    container.innerHTML = "";
    container.classList.add("hc-viz");

    var readout = document.createElement("div");
    readout.className = "hc-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "hc-canvas";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "hc-controls";
    var lab = document.createElement("span");
    lab.className = "hc-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "0"; slider.max = "1000"; slider.step = "1";
    slider.value = String(Math.round(Math.log10(mSel) / 3 * 1000)); slider.className = "hc-slider";
    controls.appendChild(lab); controls.appendChild(slider);
    container.appendChild(controls);

    function sliderToM() { return Math.max(1, Math.round(Math.pow(10, parseInt(slider.value, 10) / 1000 * 3))); }
    function xpix(M) {
      var pad = 40;
      return pad + (Math.log10(M) - Math.log10(MMIN)) / (Math.log10(MMAX) - Math.log10(MMIN)) * (W - pad - 14);
    }
    function ypix(t) {
      var top = 16, base = H - 28;
      return base - (t - TMIN) / (TMAX - TMIN) * (base - top);
    }

    function draw() {
      var M = sliderToM();
      var dpr = global.devicePixelRatio || 1;
      canvas.width = W * dpr; canvas.height = H * dpr;
      canvas.style.width = "100%"; canvas.style.maxWidth = W + "px"; canvas.style.height = "auto";
      var ctx = canvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      var base = H - 28, left = 40;

      // axes
      ctx.strokeStyle = "#d9d6cd"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(left, 16); ctx.lineTo(left, base); ctx.lineTo(W - 14, base); ctx.stroke();
      ctx.fillStyle = "#5a635f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textAlign = "right";
      [2, 2.5, 3, 3.5, 4].forEach(function (t) { ctx.fillText(t.toFixed(1), left - 5, ypix(t) + 3); });
      ctx.textAlign = "center";
      [1, 10, 100, 1000].forEach(function (M2) { ctx.fillText(M2 === 1 ? "1" : String(M2), xpix(M2), H - 12); });
      ctx.fillText("number of strategies tested (M, log scale)", (left + W - 14) / 2, H - 1);
      ctx.save(); ctx.translate(11, (16 + base) / 2); ctx.rotate(-Math.PI / 2);
      ctx.fillText("required |t|", 0, 0); ctx.restore();

      // reference lines: single-test 1.96, HLZ ~3.0
      ctx.strokeStyle = "#9a6b1f"; ctx.setLineDash([4, 3]); ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(left, ypix(1.96)); ctx.lineTo(W - 14, ypix(1.96)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(left, ypix(3.0)); ctx.lineTo(W - 14, ypix(3.0)); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#9a6b1f"; ctx.textAlign = "left"; ctx.font = "9px system-ui, sans-serif";
      ctx.fillText("single-test 1.96", left + 4, ypix(1.96) - 4);
      ctx.fillText("Harvey-Liu-Zhu \u2248 3.0", left + 4, ypix(3.0) - 4);

      // Bonferroni curve
      ctx.beginPath();
      for (var k = 0; k <= 240; k++) {
        var mm = Math.pow(10, (k / 240) * 3);
        var t = hurdle(mm, ALPHA);
        var px = xpix(mm), py = ypix(Math.min(TMAX, t));
        if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 2; ctx.stroke();

      // marker at selected M
      var tM = hurdle(M, ALPHA);
      ctx.fillStyle = "#0d5c4b";
      ctx.beginPath(); ctx.arc(xpix(M), ypix(Math.min(TMAX, tM)), 4, 0, 2 * Math.PI); ctx.fill();

      lab.textContent = "M = " + M + " strategies";
      var haircut = tM > 2.5;
      readout.innerHTML = "Testing <strong>" + M + "</strong> ideas \u2192 Bonferroni hurdle |t| = <strong>" +
        tM.toFixed(2) + "</strong> (per-test p = " + (ALPHA / M).toExponential(1) + "). " +
        "A backtest with t = 2.5 found after this search is " +
        (haircut ? "<span class=\"hc-fail\">no longer significant</span>" : "<span class=\"hc-ok\">still significant</span>") +
        " once the search is accounted for.";
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw };
  }

  global.Haircut = { mount: mount };
})(window);
