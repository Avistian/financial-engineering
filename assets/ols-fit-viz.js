/**
 * OLS as projection — least squares minimizes the sum of squared residuals
 * (assets/ols-fit-viz.js)
 *
 * A fixed cloud of (x, y) points. A candidate regression line is drawn through the
 * data's centre of mass (x̄, ȳ) — every OLS line passes through that point — and the
 * slider rotates it. The vertical red stubs are the residuals; the readout reports the
 * sum of squared residuals (SSR) for the candidate vs. the OLS minimum. The learner
 * sees SSR bottom out exactly when the candidate slope equals the OLS slope
 * b = Cov(x,y)/Var(x): least squares is the projection of y onto the column space of X,
 * so the residual vector is orthogonal to x and no other line does better.
 *
 * Usage:
 *   <div id="ols"></div>
 *   <script src="../assets/ols-fit-viz.js"></script>
 *   OLSFit.mount(document.getElementById("ols"), { seed: 7 });
 *
 * Expected state: on load the candidate slope starts away from OLS, so SSR > SSR_min and
 * the "minimum" badge is off. Drag the slider to the OLS slope (~1.0 for the default seed)
 * and SSR reaches its minimum, the badge lights up, and the residuals balance around the line.
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
    var seed = config.seed || 7;
    var N = config.n || 36;
    var bTrue = config.bTrue == null ? 1.0 : config.bTrue;

    container.innerHTML = "";
    container.classList.add("ols-viz");

    var readout = document.createElement("div");
    readout.className = "ols-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "ols-canvas";
    var W = 420, H = 300;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "ols-controls";
    var lab = document.createElement("span");
    lab.className = "ols-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "0"; slider.max = "100"; slider.step = "1";
    slider.value = "18"; slider.className = "ols-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    // ---- fixed data ----
    var rng = mulberry32(seed);
    var xs = [], ys = [];
    for (var i = 0; i < N; i++) {
      var x = -2.2 + 4.4 * rng();
      var y = bTrue * x + 1.1 * randn(rng);
      xs.push(x); ys.push(y);
    }
    var xbar = xs.reduce(function (s, v) { return s + v; }, 0) / N;
    var ybar = ys.reduce(function (s, v) { return s + v; }, 0) / N;
    var Sxx = 0, Sxy = 0;
    for (i = 0; i < N; i++) { Sxx += (xs[i] - xbar) * (xs[i] - xbar); Sxy += (xs[i] - xbar) * (ys[i] - ybar); }
    var bOLS = Sxy / Sxx;

    function ssr(b) {
      var s = 0;
      for (var k = 0; k < N; k++) {
        var yhat = ybar + b * (xs[k] - xbar);
        var e = ys[k] - yhat;
        s += e * e;
      }
      return s;
    }
    var ssrMin = ssr(bOLS);

    // slider 0..100 -> slope in [bOLS-2, bOLS+2]
    function sliderToB(v) { return bOLS - 2 + (v / 100) * 4; }

    var ctx = canvas.getContext("2d");
    var padL = 34, padR = 14, padT = 16, padB = 30;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var xLo = -2.7, xHi = 2.7, yLo = -3.8, yHi = 3.8;
    function px(x) { return padL + (x - xLo) / (xHi - xLo) * plotW; }
    function py(y) { return padT + plotH - (y - yLo) / (yHi - yLo) * plotH; }

    function draw() {
      var b = sliderToB(parseInt(slider.value, 10));
      ctx.clearRect(0, 0, W, H);

      // axes through origin
      ctx.strokeStyle = "#e4e1d8"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(px(xLo), py(0)); ctx.lineTo(px(xHi), py(0)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(px(0), py(yLo)); ctx.lineTo(px(0), py(yHi)); ctx.stroke();
      ctx.fillStyle = "#5a635f"; ctx.font = "11px system-ui, sans-serif";
      ctx.fillText("signal x", W - 66, py(0) - 6);
      ctx.fillText("return y", px(0) + 6, 12);

      // residual stubs
      ctx.strokeStyle = "rgba(146,43,33,0.55)"; ctx.lineWidth = 1.2;
      for (var k = 0; k < N; k++) {
        var yhat = ybar + b * (xs[k] - xbar);
        ctx.beginPath();
        ctx.moveTo(px(xs[k]), py(ys[k]));
        ctx.lineTo(px(xs[k]), py(yhat));
        ctx.stroke();
      }

      // candidate line
      ctx.strokeStyle = "#9a6b1f"; ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(px(xLo), py(ybar + b * (xLo - xbar)));
      ctx.lineTo(px(xHi), py(ybar + b * (xHi - xbar)));
      ctx.stroke();

      // points
      ctx.fillStyle = "rgba(13,92,75,0.75)";
      for (k = 0; k < N; k++) {
        ctx.beginPath(); ctx.arc(px(xs[k]), py(ys[k]), 2.6, 0, 2 * Math.PI); ctx.fill();
      }

      // centre of mass
      ctx.fillStyle = "#17201d";
      ctx.beginPath(); ctx.arc(px(xbar), py(ybar), 3.4, 0, 2 * Math.PI); ctx.fill();

      var cur = ssr(b);
      var atMin = Math.abs(b - bOLS) < 0.03;
      lab.textContent = "candidate slope b = " + b.toFixed(2);
      readout.innerHTML =
        "Line through (x\u0304, \u0233). Candidate slope <strong>b = " + b.toFixed(2) + "</strong>. " +
        "SSR = <strong>" + cur.toFixed(1) + "</strong> vs. minimum " + ssrMin.toFixed(1) +
        " (at the OLS slope b\u0302 = Cov/Var = " + bOLS.toFixed(2) + "). " +
        (atMin
          ? "<span class=\"ols-min\">Minimum \u2014 residuals \u22a5 x: this is the projection (least-squares) line.</span>"
          : "<span class=\"ols-off\">Not minimal \u2014 rotate toward b\u0302 to shrink SSR.</span>");
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw, bOLS: bOLS };
  }

  global.OLSFit = { mount: mount };
})(window);
