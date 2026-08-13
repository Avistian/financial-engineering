/**
 * Stochastic differential equations — two pictures for Lesson 014.
 * (assets/sde-viz.js)
 *
 * One reusable component, mounted in TWO modes because Lesson 014 has two distinct
 * mechanisms the prose treats as separate sections. The OU mode draws from a seeded
 * bank of Brownian increments built exactly the way Lessons 012–013 built them
 * (cumulative √dt·N(0,1)), so the lineage walk → Brownian motion → Itô → SDE is
 * unbroken. The explosion mode is deterministic (no randomness needed to make the
 * existence/uniqueness point).
 *
 *   SDE.mountOU(el, cfg)  — the mean-reverting Ornstein–Uhlenbeck process.
 *     dX = θ(m − X)dt + σ dW, simulated by Euler steps on the shared Brownian bank.
 *     The slider is the pull strength θ. Faint sample paths, the MEAN curve
 *     E[X_t] = X₀e^{−θt} + m(1 − e^{−θt}) (solid), and the equilibrium BAND
 *     m ± √(σ²/2θ) (the stationary spread). As θ grows the paths snap back to m
 *     faster (half-life ln2/θ shrinks) AND the band tightens (√(σ²/2θ) shrinks).
 *
 *   SDE.mountExplosion(el, cfg)  — why the drift must not grow too fast (existence).
 *     Two deterministic drifts from the same start x₀, over [0,T]:
 *       • linear-growth drift  dx/dt = x   → x(t) = x₀e^{t}      (finite for all t)
 *       • super-linear drift   dx/dt = x²  → x(t) = x₀/(1 − x₀t) (BLOWS UP at t*=1/x₀)
 *     The slider is x₀. As x₀ grows the blow-up time t* = 1/x₀ marches left onto the
 *     screen: a super-linear drift can reach infinity in FINITE time, so no global
 *     solution exists. Linear (Lipschitz-style) growth is the condition that rules
 *     this out — the intuition behind existence/uniqueness for SDEs.
 *
 * Config:
 *   ou:        { seed, X0 (80), m (100), sigma (10), theta (init 2.0), thetaMax (10) }
 *   explosion: { x0 (init 0.8), x0Max (2.0), T (2) }
 *
 * Returned handle (for tests):
 *   ou:        { draw, meanAt(theta,t), statStd(theta), halfLife(theta), m, X0, endMean(theta) }
 *   explosion: { draw, blowupTime(x0), linearAt(x0,t), T }
 *
 * Expected states (default seed 913, NPATHS 40, NSTEPS 200, T=1):
 *   ou:        endMean(θ) strictly INCREASES toward m as θ grows (faster pull from X0<m);
 *              statStd(θ) strictly DECREASES as θ grows.
 *   explosion: blowupTime(x0) = 1/x0 strictly DECREASES as x0 grows.
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

  var NPATHS = 40, NSTEPS = 200, T = 1;
  var DT = T / NSTEPS;
  var SQDT = Math.sqrt(DT);

  // Shared bank of Brownian INCREMENTS (seeded ⇒ reproducible, stable tests).
  function buildIncrements(seed) {
    var gauss = gaussFactory(mulberry32(seed));
    var dW = [];
    for (var p = 0; p < NPATHS; p++) {
      var d = new Float64Array(NSTEPS);
      for (var i = 0; i < NSTEPS; i++) d[i] = SQDT * gauss();
      dW.push(d);
    }
    var tGrid = new Float64Array(NSTEPS + 1);
    for (var j = 0; j <= NSTEPS; j++) tGrid[j] = j / NSTEPS * T;
    return { dW: dW, tGrid: tGrid };
  }

  // ---------- shared canvas scaffold (matches ito-viz / bm-viz) ----------
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

  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  // ---------- MODE 1: the mean-reverting Ornstein–Uhlenbeck process ----------
  function mountOU(container, cfg) {
    cfg = cfg || {};
    var seed = cfg.seed == null ? 913 : cfg.seed;
    var X0 = cfg.X0 == null ? 80 : cfg.X0;
    var m = cfg.m == null ? 100 : cfg.m;
    var sigma = cfg.sigma == null ? 10 : cfg.sigma;
    var thetaMax = cfg.thetaMax == null ? 10 : cfg.thetaMax;
    var theta0 = cfg.theta == null ? 2.0 : cfg.theta;

    var bank = buildIncrements(seed);
    var dWbank = bank.dW, tGrid = bank.tGrid;

    function meanAt(theta, t) { return X0 * Math.exp(-theta * t) + m * (1 - Math.exp(-theta * t)); }
    function statStd(theta) { return Math.sqrt(sigma * sigma / (2 * theta)); }
    function stdAt(theta, t) { return Math.sqrt(sigma * sigma / (2 * theta) * (1 - Math.exp(-2 * theta * t))); }
    function halfLife(theta) { return Math.log(2) / theta; }
    function endMean(theta) { return meanAt(theta, T); }

    // Euler simulation of one path on the shared increments.
    function simPath(p, theta) {
      var x = new Float64Array(NSTEPS + 1);
      x[0] = X0;
      for (var i = 1; i <= NSTEPS; i++) {
        x[i] = x[i - 1] + theta * (m - x[i - 1]) * DT + sigma * dWbank[p][i - 1];
      }
      return x;
    }

    var ui = scaffold(container, "ou");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "5"; ui.slider.max = String(thetaMax * 10); ui.slider.step = "5";
    ui.slider.value = String(Math.round(theta0 * 10));

    var padL = 42, padR = 14, padT = 16, padB = 28;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    // Fixed, generous y-window: X0 below m, band around m, room for excursions.
    var yMin = 55, yMax = 125;
    function xPix(tt) { return padL + tt / T * plotW; }
    function yPix(v) { return clamp(padT + (yMax - v) / (yMax - yMin) * plotH, padT, Hd - padB); }

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      // reference lines at m and X0
      ctx.setLineDash([2, 3]);
      ctx.beginPath(); ctx.moveTo(padL, yPix(m)); ctx.lineTo(Wd - padR, yPix(m)); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText("m=" + m, padL - 5, yPix(m));
      ctx.fillText(String(X0), padL - 5, yPix(X0));
      ctx.textAlign = "center";
      ctx.fillText("t=0", xPix(0), Hd - 10);
      ctx.fillText("t=" + T, xPix(T), Hd - 10);
    }

    function draw() {
      var theta = parseInt(ui.slider.value, 10) / 10;
      ctx.clearRect(0, 0, Wd, Hd);
      axes();

      // equilibrium band m ± stationary std (shaded via two dashed edges)
      var sd = statStd(theta);
      ctx.strokeStyle = "#d8c58a"; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(padL, yPix(m + sd)); ctx.lineTo(Wd - padR, yPix(m + sd)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(padL, yPix(m - sd)); ctx.lineTo(Wd - padR, yPix(m - sd)); ctx.stroke();
      ctx.setLineDash([]);

      // faint sample OU paths
      ctx.strokeStyle = "#bcd8cf"; ctx.lineWidth = 1;
      for (var p = 0; p < NPATHS; p++) {
        var x = simPath(p, theta);
        ctx.beginPath();
        for (var i = 0; i <= NSTEPS; i++) {
          var px = xPix(tGrid[i]), py = yPix(x[i]);
          if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
      }

      // mean curve E[X_t] = X0 e^{-θt} + m(1 - e^{-θt})
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 2;
      ctx.beginPath();
      for (var j = 0; j <= NSTEPS; j++) {
        var mx = xPix(tGrid[j]), my = yPix(meanAt(theta, tGrid[j]));
        if (j === 0) ctx.moveTo(mx, my); else ctx.lineTo(mx, my);
      }
      ctx.stroke();

      ui.lab.textContent = "\u03b8 = " + theta.toFixed(1);
      ui.readout.innerHTML =
        "Ornstein\u2013Uhlenbeck: pulled toward <strong>m = " + m + "</strong> from X\u2080 = <strong>" + X0 +
        "</strong> with pull strength <span style=\"color:#0d5c4b;font-weight:600\">\u03b8 = " + theta.toFixed(1) +
        "</span>. " +
        "<span style=\"color:#0d5c4b;font-weight:600\">Mean</span> reaches <strong>" + endMean(theta).toFixed(1) +
        "</strong> by t=" + T + " (half-life ln2/\u03b8 = <strong>" + halfLife(theta).toFixed(2) +
        "</strong>). " +
        "<span class=\"ou-note\">The <span style=\"color:#9a6b1f;font-weight:600\">equilibrium band</span> m \u00b1 \u221a(\u03c3\u00b2/2\u03b8) = \u00b1" +
        sd.toFixed(1) + " tightens as \u03b8 grows \u2014 a stronger spring holds it closer to m.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, meanAt: meanAt, statStd: statStd, halfLife: halfLife,
             endMean: endMean, m: m, X0: X0 };
  }

  // ---------- MODE 2: existence — a drift that grows too fast blows up ----------
  function mountExplosion(container, cfg) {
    cfg = cfg || {};
    var Texp = cfg.T == null ? 2 : cfg.T;
    var x0Max = cfg.x0Max == null ? 2.0 : cfg.x0Max;
    var x00 = cfg.x0 == null ? 0.8 : cfg.x0;

    function blowupTime(x0) { return 1 / x0; }                 // dx/dt = x² ⇒ x = x0/(1−x0 t)
    function linearAt(x0, t) { return x0 * Math.exp(t); }      // dx/dt = x  ⇒ x = x0 e^t
    function superAt(x0, t) {                                  // dx/dt = x²
      var denom = 1 - x0 * t;
      return denom > 1e-6 ? x0 / denom : Infinity;
    }

    var ui = scaffold(container, "expl");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "20"; ui.slider.max = String(Math.round(x0Max * 100)); ui.slider.step = "10";
    ui.slider.value = String(Math.round(x00 * 100));

    var padL = 34, padR = 14, padT = 16, padB = 28;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    var yTop = 8;                     // top of the visible value window
    function xPix(tt) { return padL + tt / Texp * plotW; }
    function yPix(v) { return clamp(padT + (yTop - v) / yTop * plotH, padT, Hd - padB); }

    var NS = 240;

    function axes(tStar) {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(padL, Hd - padB); ctx.lineTo(Wd - padR, Hd - padB); ctx.stroke();
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText(String(yTop), padL - 5, yPix(yTop) + 6);
      ctx.fillText("0", padL - 5, yPix(0));
      ctx.textAlign = "center";
      ctx.fillText("t=0", xPix(0), Hd - 10);
      ctx.fillText("t=" + Texp, xPix(Texp), Hd - 10);
      // mark the blow-up time if it is on screen
      if (tStar <= Texp) {
        ctx.strokeStyle = "#b23a48"; ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(xPix(tStar), padT); ctx.lineTo(xPix(tStar), Hd - padB); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = "#b23a48"; ctx.textAlign = "center";
        ctx.fillText("t*=" + tStar.toFixed(2), clamp(xPix(tStar), padL + 16, Wd - padR - 16), padT + 6);
      }
    }

    function curve(fn, color, width, dash) {
      ctx.strokeStyle = color; ctx.lineWidth = width; ctx.setLineDash(dash || []);
      ctx.beginPath();
      var started = false;
      for (var i = 0; i <= NS; i++) {
        var t = i / NS * Texp;
        var v = fn(t);
        if (!isFinite(v) || v > yTop * 1.02) {           // stop drawing once it leaves the window
          if (started) { var x = xPix(t), y = yPix(yTop); ctx.lineTo(x, y); }
          break;
        }
        var px = xPix(t), py = yPix(v);
        if (!started) { ctx.moveTo(px, py); started = true; } else ctx.lineTo(px, py);
      }
      ctx.stroke(); ctx.setLineDash([]);
    }

    function draw() {
      var x0 = parseInt(ui.slider.value, 10) / 100;
      var tStar = blowupTime(x0);
      ctx.clearRect(0, 0, Wd, Hd);
      axes(tStar);
      curve(function (t) { return linearAt(x0, t); }, "#0d5c4b", 2, []);   // stays finite
      curve(function (t) { return superAt(x0, t); }, "#b23a48", 2, []);    // explodes

      var onScreen = tStar <= Texp;
      ui.lab.textContent = "x\u2080 = " + x0.toFixed(1);
      ui.readout.innerHTML =
        "Same start x\u2080 = <strong>" + x0.toFixed(1) + "</strong>, two drifts. " +
        "<span style=\"color:#0d5c4b;font-weight:600\">dx/dt = x</span> (linear growth) stays finite: x = x\u2080e\u1d57. " +
        "<span style=\"color:#b23a48;font-weight:600\">dx/dt = x\u00b2</span> (grows too fast) reaches \u221e at " +
        "<strong>t* = 1/x\u2080 = " + tStar.toFixed(2) + "</strong>" +
        (onScreen ? " \u2014 on screen." : " \u2014 just off the right edge.") +
        " <span class=\"expl-note\">A drift bounded by linear growth has one solution for all time; a super-linear drift can blow up in finite time \u2014 that is what existence/uniqueness rules out.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, blowupTime: blowupTime, linearAt: linearAt, T: Texp };
  }

  global.SDE = { mountOU: mountOU, mountExplosion: mountExplosion };
})(window);
