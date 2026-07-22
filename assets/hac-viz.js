/**
 * Autocorrelated errors & Newey-West (HAC) standard errors (assets/hac-viz.js)
 *
 * Overlapping-horizon returns and persistent signals produce SERIALLY CORRELATED
 * regression errors. Here the errors follow an AR(1): e_t = φ·e_{t-1} + √(1−φ²)·η_t
 * (unit unconditional variance), and the slider sets φ. The panel plots the realized
 * error path — visibly "sticky" when φ is high — and the readout compares the standard
 * error of the sample mean three ways:
 *   • naïve   SE = s/√n                          (assumes i.i.d. — ignores the stickiness)
 *   • Newey-West SE = √(LRV_hat / n), LRV_hat = γ̂₀ + 2Σ_{l=1}^{L}(1−l/(L+1))·γ̂_l  (Bartlett)
 *   • true    SE = √(LRV / n),  LRV = (1+φ)/(1−φ) (the closed-form AR(1) long-run variance)
 * Positive autocorrelation makes the naïve SE too small, so the t-stat is overstated by
 * √[(1+φ)/(1−φ)]. Newey-West's HAC estimate tracks the true (inflated) SE.
 *
 * Usage:
 *   <div id="hac"></div>
 *   <script src="../assets/hac-viz.js"></script>
 *   HAC.mount(document.getElementById("hac"), { phi: 0.5 });
 *
 * Expected state: φ = 0 -> the three SEs coincide (ratio ≈ 1). φ = 0.5 -> VIF = 3, so the
 * true/NW SE are ≈ √3 ≈ 1.73× the naïve SE. φ -> 0.8 -> VIF = 9, ≈ 3× inflation; a naïve
 * t of 3 is really ≈ 1.
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
    var seed = config.seed || 3;
    var N = config.n || 300;
    var L = config.lags || 25;
    var phi0 = config.phi == null ? 0.5 : config.phi;

    container.innerHTML = "";
    container.classList.add("hac-viz");

    var readout = document.createElement("div");
    readout.className = "hac-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "hac-canvas";
    var W = 420, H = 240;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "hac-controls";
    var lab = document.createElement("span");
    lab.className = "hac-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "0"; slider.max = "85"; slider.step = "5";
    slider.value = String(Math.round(phi0 * 100)); slider.className = "hac-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    // fixed innovations so only the persistence changes with φ
    var rng = mulberry32(seed);
    var eta = [];
    for (var i = 0; i < N; i++) eta.push(randn(rng));

    var ctx = canvas.getContext("2d");
    var padL = 30, padR = 12, padT = 14, padB = 26;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var yLo = -3.6, yHi = 3.6;
    function px(t) { return padL + t / (N - 1) * plotW; }
    function py(y) { return padT + plotH - (y - yLo) / (yHi - yLo) * plotH; }

    function draw() {
      var phi = parseInt(slider.value, 10) / 100;
      // build AR(1) with unit unconditional variance
      var e = new Array(N);
      e[0] = eta[0];
      var sd = Math.sqrt(1 - phi * phi);
      for (var t = 1; t < N; t++) e[t] = phi * e[t - 1] + sd * eta[t];

      // sample moments
      var mean = 0; for (t = 0; t < N; t++) mean += e[t]; mean /= N;
      var g0 = 0; for (t = 0; t < N; t++) g0 += (e[t] - mean) * (e[t] - mean); g0 /= N;

      // Newey-West long-run variance with Bartlett weights
      var lrv = g0;
      for (var l = 1; l <= L; l++) {
        var gl = 0;
        for (t = l; t < N; t++) gl += (e[t] - mean) * (e[t - l] - mean);
        gl /= N;
        lrv += 2 * (1 - l / (L + 1)) * gl;
      }
      if (lrv < 1e-9) lrv = 1e-9;

      var seNaive = Math.sqrt(g0 / N);
      var seNW = Math.sqrt(lrv / N);
      var vifTrue = (1 + phi) / (1 - phi);
      var seTrue = Math.sqrt(vifTrue / N); // unit unconditional variance -> g0≈1

      ctx.clearRect(0, 0, W, H);
      // zero line
      ctx.strokeStyle = "#e4e1d8"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(px(0), py(0)); ctx.lineTo(px(N - 1), py(0)); ctx.stroke();

      // AR(1) path
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 1.3;
      ctx.beginPath();
      for (t = 0; t < N; t++) {
        var yy = Math.max(yLo, Math.min(yHi, e[t]));
        if (t === 0) ctx.moveTo(px(t), py(yy)); else ctx.lineTo(px(t), py(yy));
      }
      ctx.stroke();

      ctx.fillStyle = "#5a635f"; ctx.font = "11px system-ui, sans-serif";
      ctx.fillText("error e\u209c over time  (n = " + N + ")", padL + 4, H - 8);

      lab.textContent = "error autocorrelation \u03c6 = " + phi.toFixed(2);
      readout.innerHTML =
        "Variance-inflation factor (1+\u03c6)/(1\u2212\u03c6) = <strong>" + vifTrue.toFixed(1) + "</strong>. &nbsp;" +
        "SE(mean): naïve <strong>" + seNaive.toFixed(3) + "</strong>, " +
        "Newey-West <strong>" + seNW.toFixed(3) + "</strong> (L = " + L + " lags), true " + seTrue.toFixed(3) + ". " +
        "<span class=\"hac-verdict\">Naïve t-stat overstated \u2248 " + Math.sqrt(vifTrue).toFixed(2) + "\u00d7.</span>";
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw };
  }

  global.HAC = { mount: mount };
})(window);
