/**
 * Itô's lemma — the extra term made visible.
 * (assets/ito-viz.js)
 *
 * One reusable component, mounted in TWO modes because Lesson 013 has two distinct
 * mechanisms. Both modes draw from the SAME seeded bank of Brownian paths (built the
 * way Lesson 012 built them: cumulative √dt·N(0,1) increments), so the lineage
 * tree → walk → Brownian motion → Itô is unbroken.
 *
 *   Ito.mountDrift(el, cfg)  — WHY Itô's lemma needs an extra term, for f(x)=x².
 *     For every path we split W_t² exactly into two running pieces (this is the
 *     algebraic identity behind Itô's lemma, done discretely):
 *
 *         W_t² = Σ 2·W_{i-1}·ΔW_i   +   Σ (ΔW_i)²
 *                └── the Itô integral ∫2W dW ──┘   └─ quadratic variation → t ─┘
 *                     (LEFT endpoint ⇒ a martingale, mean 0)     (Lesson 012)
 *
 *     The slider is the number of paths N = 2^k averaged. The readout / plot show the
 *     ensemble means: E[∫2W dW] hugs 0 (flat — what the NAIVE chain rule keeps), while
 *     E[W_t²] rises along the drift line y = t. The whole rise is the second piece,
 *     the (dW)² = dt term the naive chain rule drops. That surviving term IS the ½f''dt
 *     of Itô's lemma (here ½·f''·t = ½·2·t = t).
 *
 *   Ito.mountGBM(el, cfg)   — the practical payoff: d(log S) = (μ − ½σ²)dt + σ dW.
 *     Geometric Brownian motion S_t = S₀·exp((μ − ½σ²)t + σ W_t). The slider is the
 *     volatility σ. Faint sample paths, the MEAN line E[S_t] = S₀e^{μt} (unchanged by
 *     σ) and the MEDIAN line S₀e^{(μ−½σ²)t}. As σ grows the median falls away below the
 *     mean — the "volatility drag" ½σ², which is exactly the Itô correction on log S.
 *
 * Config:
 *   drift: { seed, k (init 1..kMax), kMax (default 8 → N=256) }
 *   gbm:   { seed, S0 (100), mu (0.10), sigmaPct (init 20), sigmaMax (80) }
 *
 * Returned handle (for tests):
 *   drift: { draw, meanW2(N), meanIto(N), driftLine (=t at t=1 → 1), NPATHS }
 *   gbm:   { draw, medianRate(sig), meanRate, drag(sig), S0, mu }
 *
 * Expected states (default seed 913, NPATHS 256, NSTEPS 64):
 *   drift: meanW2(256) ≈ 1.0 (within ~0.15), meanIto(256) ≈ 0 (within ~0.15).
 *   gbm  : medianRate strictly DECREASES as σ grows (0.10 − ½σ²); meanRate = 0.10 fixed.
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

  // Standard normal via Box–Muller, driven by the seeded uniform stream.
  function gaussFactory(rng) {
    var spare = null;
    return function () {
      if (spare !== null) { var s = spare; spare = null; return s; }
      var u = 0, v = 0;
      while (u === 0) u = rng();
      while (v === 0) v = rng();
      var r = Math.sqrt(-2 * Math.log(u));
      spare = r * Math.sin(2 * Math.PI * v);
      return r * Math.cos(2 * Math.PI * v);
    };
  }

  var NPATHS = 256, NSTEPS = 64, T = 1;
  var DT = T / NSTEPS;
  var SQDT = Math.sqrt(DT);

  // Build the shared bank of Brownian paths once (seeded ⇒ reproducible, stable tests).
  function buildBank(seed) {
    var gauss = gaussFactory(mulberry32(seed));
    var W = [];             // W[p][i], i = 0..NSTEPS
    for (var p = 0; p < NPATHS; p++) {
      var w = new Float64Array(NSTEPS + 1);
      for (var i = 1; i <= NSTEPS; i++) w[i] = w[i - 1] + SQDT * gauss();
      W.push(w);
    }
    var tGrid = new Float64Array(NSTEPS + 1);
    for (var j = 0; j <= NSTEPS; j++) tGrid[j] = j / NSTEPS;
    return { W: W, tGrid: tGrid };
  }

  function fmt(v, dp) {
    var s = v.toFixed(dp == null ? 3 : dp);
    return (v >= 0 ? "+" : "") + s;
  }

  // ---------- shared canvas scaffold ----------
  function scaffold(container, prefix) {
    container.innerHTML = "";
    container.classList.add(prefix + "-viz");

    var readout = document.createElement("div");
    readout.className = prefix + "-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = prefix + "-canvas";
    var W = 440, H = 280;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = prefix + "-controls";
    var lab = document.createElement("span");
    lab.className = prefix + "-slider-label";
    var slider = document.createElement("input");
    slider.type = "range";
    slider.className = prefix + "-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    return { readout: readout, canvas: canvas, ctx: canvas.getContext("2d"),
             lab: lab, slider: slider, W: W, H: H };
  }

  // ---------- MODE 1: the correction term as a visible drift ----------
  function mountDrift(container, cfg) {
    cfg = cfg || {};
    var seed = cfg.seed == null ? 913 : cfg.seed;
    var kMax = cfg.kMax == null ? 8 : cfg.kMax;         // 2^8 = 256 = NPATHS
    var k0 = Math.max(1, Math.min(kMax, cfg.k == null ? 6 : cfg.k));

    var bank = buildBank(seed);
    var W = bank.W, tGrid = bank.tGrid;

    // Per-path running pieces: W2 = W², ito = Σ 2 W_{i-1} ΔW (LEFT endpoint), qv = Σ ΔW².
    var W2 = [], ITO = [];
    for (var p = 0; p < NPATHS; p++) {
      var w = W[p];
      var a = new Float64Array(NSTEPS + 1), b = new Float64Array(NSTEPS + 1);
      for (var i = 1; i <= NSTEPS; i++) {
        var dw = w[i] - w[i - 1];
        a[i] = w[i] * w[i];
        b[i] = b[i - 1] + 2 * w[i - 1] * dw;          // the Itô integral ∫2W dW
      }
      a[0] = 0;
      W2.push(a); ITO.push(b);
    }

    function meanAt(arrBank, N, i) {
      var s = 0; for (var p = 0; p < N; p++) s += arrBank[p][i]; return s / N;
    }
    function meanW2(N) { return meanAt(W2, N, NSTEPS); }
    function meanIto(N) { return meanAt(ITO, N, NSTEPS); }

    var ui = scaffold(container, "ito");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "1"; ui.slider.max = String(kMax); ui.slider.step = "1";
    ui.slider.value = String(k0);

    var padL = 42, padR = 14, padT = 16, padB = 28;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    // y-range is recomputed each draw so the (noisy) small-N averages always fit;
    // it is forced to always contain 0 and +1 so those axis labels stay in bounds.
    var yMin = -0.45, yMax = 1.4;
    function xPix(tt) { return padL + tt * plotW; }
    function yPix(v) { return padT + (yMax - v) / (yMax - yMin) * plotH; }

    function fitRange(N) {
      var lo = 0, hi = 1;
      for (var i = 0; i <= NSTEPS; i++) {
        var a = meanAt(W2, N, i), b = meanAt(ITO, N, i), c = tGrid[i];
        lo = Math.min(lo, a, b, c); hi = Math.max(hi, a, b, c);
      }
      yMin = Math.min(lo, -0.05) - 0.1;
      yMax = Math.max(hi, 1.05) + 0.1;
    }

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, yPix(0)); ctx.lineTo(Wd - padR, yPix(0)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText("+1.0", padL - 5, yPix(1));
      ctx.fillText("0", padL - 5, yPix(0));
      ctx.textAlign = "center";
      ctx.fillText("t=0", xPix(0), Hd - 10);
      ctx.fillText("0.5", xPix(0.5), Hd - 10);
      ctx.fillText("t=1", xPix(1), Hd - 10);
    }

    function line(fn, color, width, dash) {
      ctx.strokeStyle = color; ctx.lineWidth = width;
      ctx.setLineDash(dash || []);
      ctx.beginPath();
      for (var i = 0; i <= NSTEPS; i++) {
        var x = xPix(tGrid[i]), y = yPix(fn(i));
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.setLineDash([]);
    }

    function draw() {
      var N = Math.pow(2, parseInt(ui.slider.value, 10));
      fitRange(N);
      ctx.clearRect(0, 0, Wd, Hd);
      axes();
      // theoretical Itô drift line: ½ f'' t = t
      line(function (i) { return tGrid[i]; }, "#c99a2e", 1.4, [5, 4]);
      // empirical mean of the Itô integral ∫2W dW (the martingale part) — hugs 0
      line(function (i) { return meanAt(ITO, N, i); }, "#9a6b1f", 1.3);
      // empirical mean of W_t² — rises along the drift line
      line(function (i) { return meanAt(W2, N, i); }, "#0d5c4b", 2);

      var mW2 = meanW2(N), mIto = meanIto(N);
      ui.lab.textContent = "paths N = " + N;
      ui.readout.innerHTML =
        "Averaging <strong>N = " + N + "</strong> Brownian paths, for f(W)=W&sup2;. " +
        "The <span style=\"color:#0d5c4b;font-weight:600\">mean of W<sub>t</sub>&sup2;</span> = <strong>" + mW2.toFixed(3) +
        "</strong> climbs the dashed drift line <strong>y = t</strong>. But the " +
        "<span style=\"color:#9a6b1f;font-weight:600\">Itô integral &int;2W&nbsp;dW</span> = <strong>" + fmt(mIto, 3) +
        "</strong> stays flat at 0 &mdash; that is <em>all</em> the naive chain rule keeps. " +
        "<span class=\"ito-note\">The entire rise is the (dW)&sup2;=dt term: &frac12;f''&middot;t = t.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, meanW2: meanW2, meanIto: meanIto, driftLine: 1, NPATHS: NPATHS };
  }

  // ---------- MODE 2: the −½σ² drag on log S (GBM mean vs median) ----------
  function mountGBM(container, cfg) {
    cfg = cfg || {};
    var seed = cfg.seed == null ? 913 : cfg.seed;
    var S0 = cfg.S0 == null ? 100 : cfg.S0;
    var mu = cfg.mu == null ? 0.10 : cfg.mu;
    var sigMax = cfg.sigmaMax == null ? 80 : cfg.sigmaMax;   // percent
    var sig0 = cfg.sigmaPct == null ? 20 : cfg.sigmaPct;
    var nShow = 22;                                          // faint sample paths drawn

    var bank = buildBank(seed);
    var W = bank.W, tGrid = bank.tGrid;

    function medianRate(sig) { return mu - 0.5 * sig * sig; }
    function drag(sig) { return 0.5 * sig * sig; }
    var meanRate = mu;

    var ui = scaffold(container, "gbm");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "5"; ui.slider.max = String(sigMax); ui.slider.step = "5";
    ui.slider.value = String(sig0);

    var padL = 46, padR = 14, padT = 16, padB = 28;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    function xPix(tt) { return padL + tt * plotW; }

    function Sval(p, i, sig) {
      return S0 * Math.exp((mu - 0.5 * sig * sig) * tGrid[i] + sig * W[p][i]);
    }

    function draw() {
      var sig = parseInt(ui.slider.value, 10) / 100;
      ctx.clearRect(0, 0, Wd, Hd);

      // y-scale from the drawn sample paths + the mean line (so everything stays in bounds)
      var yMax = S0 * Math.exp(mu * T);
      for (var p = 0; p < nShow; p++) {
        for (var i = 0; i <= NSTEPS; i++) { var v = Sval(p, i, sig); if (v > yMax) yMax = v; }
      }
      yMax *= 1.08;
      var yMin = S0 * 0.55;
      function yPix(v) { return padT + (yMax - v) / (yMax - yMin) * plotH; }

      // axes + S0 reference
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.setLineDash([2, 3]);
      ctx.beginPath(); ctx.moveTo(padL, yPix(S0)); ctx.lineTo(Wd - padR, yPix(S0)); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText(String(Math.round(yMax)), padL - 5, yPix(yMax) + 6);
      ctx.fillText(String(S0), padL - 5, yPix(S0));
      ctx.textAlign = "center";
      ctx.fillText("t=0", xPix(0), Hd - 10);
      ctx.fillText("t=1", xPix(1), Hd - 10);

      // faint sample GBM paths
      ctx.strokeStyle = "#bcd8cf"; ctx.lineWidth = 1;
      for (var q = 0; q < nShow; q++) {
        ctx.beginPath();
        for (var j = 0; j <= NSTEPS; j++) {
          var x = xPix(tGrid[j]), y = yPix(Sval(q, j, sig));
          if (j === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      // mean line S0 e^{mu t}  and median line S0 e^{(mu - ½σ²) t}
      function curve(rate, color, width, dash) {
        ctx.strokeStyle = color; ctx.lineWidth = width; ctx.setLineDash(dash || []);
        ctx.beginPath();
        for (var i = 0; i <= NSTEPS; i++) {
          var val = S0 * Math.exp(rate * tGrid[i]);
          var x = xPix(tGrid[i]), y = yPix(val);
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.stroke(); ctx.setLineDash([]);
      }
      curve(meanRate, "#0d5c4b", 2, []);                 // mean  E[S_t]
      curve(medianRate(sig), "#b23a48", 2, [5, 4]);      // median

      var medEnd = S0 * Math.exp(medianRate(sig) * T);
      var meanEnd = S0 * Math.exp(meanRate * T);
      ui.lab.textContent = "\u03c3 = " + Math.round(sig * 100) + "%";
      ui.readout.innerHTML =
        "GBM with drift &mu; = <strong>" + (mu * 100).toFixed(0) + "%</strong>, volatility &sigma; = <strong>" +
        Math.round(sig * 100) + "%</strong>. " +
        "<span style=\"color:#0d5c4b;font-weight:600\">Mean</span> E[S<sub>1</sub>] = <strong>" + meanEnd.toFixed(1) +
        "</strong> grows at &mu; (unchanged by &sigma;). " +
        "<span style=\"color:#b23a48;font-weight:600\">Median</span> S<sub>1</sub> = <strong>" + medEnd.toFixed(1) +
        "</strong> grows at &mu; &minus; &frac12;&sigma;&sup2; = <strong>" + (medianRate(sig) * 100).toFixed(1) +
        "%</strong>. " +
        "<span class=\"gbm-note\">The gap is the volatility drag &frac12;&sigma;&sup2; = " +
        (drag(sig) * 100).toFixed(1) + "% &mdash; the It&ocirc; correction on log&nbsp;S.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, medianRate: medianRate, meanRate: meanRate, drag: drag, S0: S0, mu: mu };
  }

  global.Ito = { mountDrift: mountDrift, mountGBM: mountGBM };
})(window);
