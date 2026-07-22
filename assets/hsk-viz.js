/**
 * Heteroskedasticity — why naïve OLS standard errors lie (assets/hsk-viz.js)
 *
 * A regression y = a + b·x + ε where the error variance is NOT constant: it fans out
 * with |x| (the slider sets the strength). OLS refits on the realized sample each time.
 * The readout compares three standard errors for the slope b̂:
 *   • classical  SE = sqrt( σ̂²      / Sxx )          — assumes constant variance (WRONG here)
 *   • White HC0  SE = sqrt( Σ xc²·e² / Sxx² )         — heteroskedasticity-robust (uses residuals)
 *   • true       SE = sqrt( Σ xc²·σ² / Sxx² )          — the real sampling SD (we know each σ here)
 * Because the loudest errors sit at the high-leverage edges, the classical SE understates
 * the truth, so the naïve t-stat is overstated. White's robust SE tracks the true SE.
 * OLS's *coefficient* stays unbiased throughout — only its reported precision is the lie.
 *
 * Usage:
 *   <div id="hsk"></div>
 *   <script src="../assets/hsk-viz.js"></script>
 *   HSK.mount(document.getElementById("hsk"), { k: 1.2 });
 *
 * Expected state: k = 0 -> homoskedastic; classical ≈ White ≈ true SE (ratio ≈ 1). Raise k
 * -> the cloud fans at the edges, true & White SE climb above classical, ratio > 1, and the
 * verdict reports the naïve t-stat inflation factor.
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
  function randn(rng) {
    var u = 0, v = 0;
    while (u === 0) u = rng();
    while (v === 0) v = rng();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function mount(container, config) {
    config = config || {};
    var seed = config.seed || 5;
    var N = config.n || 120;
    var bTrue = config.bTrue == null ? 0.30 : config.bTrue;
    var base = config.base == null ? 0.8 : config.base;
    var KMAX = 4;
    var k0 = config.k == null ? 2.5 : config.k;

    container.innerHTML = "";
    container.classList.add("hsk-viz");

    var readout = document.createElement("div");
    readout.className = "hsk-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "hsk-canvas";
    var W = 420, H = 300;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "hsk-controls";
    var lab = document.createElement("span");
    lab.className = "hsk-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "0"; slider.max = "100"; slider.step = "2";
    slider.value = String(Math.round(k0 / KMAX * 100)); slider.className = "hsk-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    // fixed x design + base shocks (so only the variance profile changes with k)
    var rng = mulberry32(seed);
    var xs = [], z = [];
    for (var i = 0; i < N; i++) { xs.push(-2.3 + 4.6 * rng()); z.push(randn(rng)); }
    var xbar = xs.reduce(function (s, v) { return s + v; }, 0) / N;
    var xc = xs.map(function (v) { return v - xbar; });
    var Sxx = xc.reduce(function (s, v) { return s + v * v; }, 0);
    var xmaxc = Math.max.apply(null, xc.map(Math.abs));

    var ctx = canvas.getContext("2d");
    var padL = 34, padR = 14, padT = 16, padB = 30;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var xLo = -2.7, xHi = 2.7, yLo = -5, yHi = 5;
    function px(x) { return padL + (x - xLo) / (xHi - xLo) * plotW; }
    function py(y) { return padT + plotH - (y - yLo) / (yHi - yLo) * plotH; }

    function draw() {
      var k = parseInt(slider.value, 10) / 100 * KMAX; // 0..KMAX
      var sig = [], ys = [];
      for (var j = 0; j < N; j++) {
        var s = base * (1 + k * Math.abs(xc[j]) / xmaxc);
        sig.push(s);
        ys.push(bTrue * xs[j] + s * z[j]);
      }
      var ybar = ys.reduce(function (a, v) { return a + v; }, 0) / N;
      var Sxy = 0;
      for (j = 0; j < N; j++) Sxy += xc[j] * (ys[j] - ybar);
      var bHat = Sxy / Sxx;
      var aHat = ybar - bHat * xbar;

      var ssr = 0, whiteNum = 0, trueNum = 0;
      for (j = 0; j < N; j++) {
        var e = ys[j] - (aHat + bHat * xs[j]);
        ssr += e * e;
        whiteNum += xc[j] * xc[j] * e * e;
        trueNum += xc[j] * xc[j] * sig[j] * sig[j];
      }
      var sig2 = ssr / (N - 2);
      var seClassical = Math.sqrt(sig2 / Sxx);
      var seWhite = Math.sqrt(whiteNum) / Sxx;
      var seTrue = Math.sqrt(trueNum) / Sxx;

      ctx.clearRect(0, 0, W, H);

      // axes
      ctx.strokeStyle = "#e4e1d8"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(px(xLo), py(0)); ctx.lineTo(px(xHi), py(0)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(px(0), py(yLo)); ctx.lineTo(px(0), py(yHi)); ctx.stroke();
      ctx.fillStyle = "#5a635f"; ctx.font = "11px system-ui, sans-serif";
      ctx.fillText("x", W - 22, py(0) - 6);
      ctx.fillText("y", px(0) + 6, 12);

      // ±2σ fan around the fitted line
      ctx.fillStyle = "rgba(154,107,31,0.10)";
      ctx.beginPath();
      var steps = 60, xp;
      for (var t = 0; t <= steps; t++) {
        xp = xLo + (xHi - xLo) * t / steps;
        var sxp = base * (1 + k * Math.abs(xp - xbar) / xmaxc);
        ctx.lineTo(px(xp), py(aHat + bHat * xp + 2 * sxp));
      }
      for (t = steps; t >= 0; t--) {
        xp = xLo + (xHi - xLo) * t / steps;
        var sxp2 = base * (1 + k * Math.abs(xp - xbar) / xmaxc);
        ctx.lineTo(px(xp), py(aHat + bHat * xp - 2 * sxp2));
      }
      ctx.closePath(); ctx.fill();

      // points
      ctx.fillStyle = "rgba(13,92,75,0.7)";
      for (j = 0; j < N; j++) { ctx.beginPath(); ctx.arc(px(xs[j]), py(ys[j]), 2.4, 0, 2 * Math.PI); ctx.fill(); }

      // fitted OLS line
      ctx.strokeStyle = "#922b21"; ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(px(xLo), py(aHat + bHat * xLo));
      ctx.lineTo(px(xHi), py(aHat + bHat * xHi));
      ctx.stroke();

      var ratio = seWhite / seClassical;
      lab.textContent = "heteroskedasticity k = " + k.toFixed(2);
      readout.innerHTML =
        "b\u0302 = <strong>" + bHat.toFixed(3) + "</strong> (still unbiased in expectation \u2014 just noisier as k grows). &nbsp;" +
        "SE(b\u0302): classical <strong>" + seClassical.toFixed(3) + "</strong>, " +
        "White <strong>" + seWhite.toFixed(3) + "</strong>, true " + seTrue.toFixed(3) + ". " +
        "<span class=\"hsk-verdict\">robust SE is " + ratio.toFixed(2) + "\u00d7 the naïve one</span> " +
        "(classical t = " + (bHat / seClassical).toFixed(2) + " vs robust t = " + (bHat / seWhite).toFixed(2) + ").";
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw };
  }

  global.HSK = { mount: mount };
})(window);
