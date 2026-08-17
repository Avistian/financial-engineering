/**
 * Risk-neutral pricing & the change of measure — three pictures for Lesson 015.
 * (assets/rnpricing-viz.js)
 *
 * Three separate mechanisms, three mounts (per the lesson-visuals skill: one viz per
 * distinct claim the prose makes). All three are driven by the same seeded Brownian
 * bank convention used in Lessons 012–014, so the lineage random walk → Brownian
 * motion → Itô → SDE → measure change is unbroken.
 *
 *   RN.mountReplication(el, cfg)  — the price does NOT depend on the real probability.
 *     A one-period binomial (S0=100, up 110, down 90, call struck at 100, zero rates).
 *     The slider is the REAL-WORLD probability p of an up move. Two curves:
 *       • the replication price (flat line): buy Δ=(Cu−Cd)/(Su−Sd) shares, borrow the
 *         rest; that portfolio pays the option in BOTH states, so its cost IS the price.
 *         It never moves as p slides.
 *       • the discounted expected payoff under p (rising line): moves with p, and equals
 *         the replication price at exactly ONE p — the risk-neutral probability
 *         p* = (R − d)/(u − d), marked with a dashed vertical line.
 *
 *   RN.mountWeights(el, cfg)  — Girsanov: re-weight the paths, do not move them.
 *     A bundle of GBM paths driven by a FIXED seeded Brownian bank. The slider is the
 *     real-world drift μ. Each path is drawn with opacity/width set by its Radon–Nikodym
 *     weight Z = exp(−θW_T − ½θ²T) with market price of risk θ = (μ − r)/σ: paths that
 *     ended high count for LESS under Q, paths that ended low count for MORE. The solid
 *     curve is the P-mean S0e^{μt}; the dashed curve is the WEIGHTED (Q) mean, which sits
 *     on S0e^{rt} for every μ. Nothing about the paths changes — only their weights.
 *
 *   RN.mountConvergence(el, cfg)  — the binomial price → the Black–Scholes price.
 *     CRR tree (u = e^{σ√Δt}, d = 1/u, p* = (e^{rΔt} − d)/(u − d)) priced by the
 *     risk-neutral expectation of the terminal payoff, for every step count n. The
 *     slider is n. Dots are tree prices, the dashed line is the closed-form Black–Scholes
 *     value; the dots oscillate (odd/even) and close in on it as n grows.
 *
 * Config:
 *   replication: { S0 (100), u (1.1), d (0.9), K (100), R (1.0 growth factor), p (0.7) }
 *   weights:     { seed (2718), S0 (100), mu (0.15), r (0.05), sigma (0.20), T (1),
 *                  muMin (0), muMax (0.20) }
 *   convergence: { S0 (100), K (100), r (0.05), sigma (0.20), T (1), n (8), nMax (120) }
 *
 * Returned handles (for tests):
 *   replication: { draw, price, expPrice(p), pStar, delta, bond }
 *   weights:     { draw, theta(mu), meanP(mu), meanQ(mu), weightedMeanAt(mu, i),
 *                  weightOf(WT, mu), NSTEPS, S0, r, sigma, T }
 *   convergence: { draw, bs, binom(n), nMax }
 *
 * Expected states (defaults):
 *   replication: price = 5.00 for EVERY p; expPrice(0.5) = 5.00 = price; pStar = 0.5.
 *   weights:     meanP(mu) = S0e^{μT} rises with μ; meanQ(mu) ≈ S0e^{rT} = 105.13 for all μ
 *                (within Monte-Carlo error); theta(0.15) = 0.5.
 *   convergence: bs = 10.4506 (S0=K=100, r=5%, σ=20%, T=1); |binom(n) − bs| shrinks
 *                roughly like 1/n and binom(400) is within 0.02 of bs.
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

  // Standard normal CDF (Abramowitz & Stegun 26.2.17; |error| < 7.5e-8).
  function normCdf(x) {
    var sign = x < 0 ? -1 : 1;
    var z = Math.abs(x) / Math.SQRT2;
    var t = 1 / (1 + 0.3275911 * z);
    var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-z * z);
    return 0.5 * (1 + sign * y);
  }

  // Inverse standard normal CDF (Acklam's rational approximation; |rel. error| < 1.2e-9).
  // Used to lay the terminal Brownian values on equally-likely strata, so the
  // Girsanov-weighted average is a clean quadrature rather than a noisy sample mean.
  function normInv(p) {
    var a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
             1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00];
    var b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
             6.680131188771972e+01, -1.328068155288572e+01];
    var c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
             -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00];
    var dd = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
              3.754408661907416e+00];
    var pl = 0.02425, q, x;
    if (p < pl) {
      q = Math.sqrt(-2 * Math.log(p));
      x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
          ((((dd[0] * q + dd[1]) * q + dd[2]) * q + dd[3]) * q + 1);
    } else if (p <= 1 - pl) {
      q = p - 0.5; var rr = q * q;
      x = (((((a[0] * rr + a[1]) * rr + a[2]) * rr + a[3]) * rr + a[4]) * rr + a[5]) * q /
          (((((b[0] * rr + b[1]) * rr + b[2]) * rr + b[3]) * rr + b[4]) * rr + 1);
    } else {
      q = Math.sqrt(-2 * Math.log(1 - p));
      x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
           ((((dd[0] * q + dd[1]) * q + dd[2]) * q + dd[3]) * q + 1);
    }
    return x;
  }

  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  // ---------- shared canvas scaffold (matches sde-viz / ito-viz / bm-viz) ----------
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

  // ---------- MODE 1: replication — the real probability does not set the price ----------
  function mountReplication(container, cfg) {
    cfg = cfg || {};
    var S0 = cfg.S0 == null ? 100 : cfg.S0;
    var u = cfg.u == null ? 1.1 : cfg.u;
    var d = cfg.d == null ? 0.9 : cfg.d;
    var K = cfg.K == null ? 100 : cfg.K;
    var R = cfg.R == null ? 1.0 : cfg.R;      // one-period growth of cash, e^{rΔt}
    var p0 = cfg.p == null ? 0.7 : cfg.p;

    var Su = S0 * u, Sd = S0 * d;
    var Cu = Math.max(Su - K, 0), Cd = Math.max(Sd - K, 0);
    var delta = (Cu - Cd) / (Su - Sd);          // shares in the replicating portfolio
    var bond = (Cd - delta * Sd) / R;           // cash today (negative = borrow)
    var price = delta * S0 + bond;              // cost of the replicating portfolio
    var pStar = (R - d) / (u - d);              // risk-neutral probability

    function expPrice(p) { return (p * Cu + (1 - p) * Cd) / R; }

    var ui = scaffold(container, "rep");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "0"; ui.slider.max = "100"; ui.slider.step = "1";
    ui.slider.value = String(Math.round(p0 * 100));

    var padL = 40, padR = 16, padT = 18, padB = 30;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    var yMax = Math.max(expPrice(1), price) * 1.25;
    function xPix(p) { return padL + p * plotW; }
    function yPix(v) { return clamp(padT + (yMax - v) / yMax * plotH, padT, Hd - padB); }

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(padL, Hd - padB); ctx.lineTo(Wd - padR, Hd - padB); ctx.stroke();
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText("0", padL - 5, yPix(0));
      ctx.fillText(yMax.toFixed(0), padL - 5, yPix(yMax) + 6);
      ctx.textAlign = "center";
      ctx.fillText("p = 0", xPix(0) + 8, Hd - 11);
      ctx.fillText("p = 1", xPix(1) - 8, Hd - 11);
      ctx.fillText("real-world probability of an up move", (padL + Wd - padR) / 2, Hd - 2);
    }

    function draw() {
      var p = parseInt(ui.slider.value, 10) / 100;
      ctx.clearRect(0, 0, Wd, Hd);
      axes();

      // p* marker
      ctx.strokeStyle = "#9a6b1f"; ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(xPix(pStar), padT); ctx.lineTo(xPix(pStar), Hd - padB); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#9a6b1f"; ctx.font = "10px system-ui, sans-serif"; ctx.textAlign = "center";
      ctx.fillText("p* = " + pStar.toFixed(2), clamp(xPix(pStar), padL + 22, Wd - padR - 22), padT + 6);

      // the moving "expected payoff under p, discounted" line
      ctx.strokeStyle = "#b23a48"; ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(xPix(0), yPix(expPrice(0)));
      ctx.lineTo(xPix(1), yPix(expPrice(1)));
      ctx.stroke();

      // the flat replication price
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(xPix(0), yPix(price)); ctx.lineTo(xPix(1), yPix(price));
      ctx.stroke();

      // current-p markers
      ctx.fillStyle = "#b23a48";
      ctx.beginPath(); ctx.arc(xPix(p), yPix(expPrice(p)), 4, 0, 2 * Math.PI); ctx.fill();
      ctx.fillStyle = "#0d5c4b";
      ctx.beginPath(); ctx.arc(xPix(p), yPix(price), 4, 0, 2 * Math.PI); ctx.fill();

      var gap = expPrice(p) - price;
      ui.lab.textContent = "p = " + p.toFixed(2);
      ui.readout.innerHTML =
        "Replicating portfolio: hold <strong>\u0394 = " + delta.toFixed(2) + "</strong> shares and " +
        (bond < 0 ? "borrow <strong>" + Math.abs(bond).toFixed(2) + "</strong>" :
                    "lend <strong>" + bond.toFixed(2) + "</strong>") +
        " \u2014 it pays the option in <em>both</em> states, so the " +
        "<span style=\"color:#0d5c4b;font-weight:600\">price is its cost, " + price.toFixed(2) +
        "</span>, for every p. " +
        "<span style=\"color:#b23a48;font-weight:600\">Discounted expected payoff under p = " +
        p.toFixed(2) + " is " + expPrice(p).toFixed(2) + "</span>" +
        (Math.abs(gap) < 5e-3
          ? " \u2014 they agree, because p is exactly p*."
          : " \u2014 off by " + gap.toFixed(2) + ", a free " + Math.abs(gap).toFixed(2) +
            " to anyone who trades against it.") +
        " <span class=\"rep-note\">The two lines meet only at p* = (R \u2212 d)/(u \u2212 d) = " +
        pStar.toFixed(2) + " \u2014 the risk-neutral probability.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, price: price, expPrice: expPrice, pStar: pStar,
             delta: delta, bond: bond };
  }

  // ---------- MODE 2: Girsanov — same paths, different weights ----------
  function mountWeights(container, cfg) {
    cfg = cfg || {};
    var seed = cfg.seed == null ? 2718 : cfg.seed;
    var S0 = cfg.S0 == null ? 100 : cfg.S0;
    var r = cfg.r == null ? 0.05 : cfg.r;
    var sigma = cfg.sigma == null ? 0.20 : cfg.sigma;
    var T = cfg.T == null ? 1 : cfg.T;
    var mu0 = cfg.mu == null ? 0.15 : cfg.mu;
    var muMin = cfg.muMin == null ? 0 : cfg.muMin;
    var muMax = cfg.muMax == null ? 0.20 : cfg.muMax;

    var NDRAW = 26, NSTAT = 3200, NSTEPS = 60;
    var DT = T / NSTEPS, SQDT = Math.sqrt(DT);

    // A seeded bank of Brownian paths whose TERMINAL values sit on equally-likely
    // strata (Brownian bridge onto W_T = √T·Φ⁻¹((k+½)/N)). Stratifying the endpoint is
    // what keeps the Girsanov-weighted average pinned to S₀e^{rT} at every slider
    // position instead of wandering with Monte-Carlo noise.
    var Wpaths = [];
    (function build() {
      var gauss = gaussFactory(mulberry32(seed));
      var raw = new Float64Array(NSTEPS + 1);
      for (var k = 0; k < NSTAT; k++) {
        var WT = Math.sqrt(T) * normInv((k + 0.5) / NSTAT);
        raw[0] = 0;
        for (var i = 1; i <= NSTEPS; i++) raw[i] = raw[i - 1] + SQDT * gauss();
        var path = new Float64Array(NSTEPS + 1);
        for (var j = 0; j <= NSTEPS; j++) {
          var frac = j / NSTEPS;                       // bridge: pin the endpoint to WT
          path[j] = raw[j] - frac * raw[NSTEPS] + frac * WT;
        }
        Wpaths.push(path);
      }
    })();

    // Draw a spread of the bank (one path from every NSTAT/NDRAW-th stratum), so the
    // faint bundle on screen is representative rather than all-low or all-high.
    var drawIdx = [];
    for (var q = 0; q < NDRAW; q++) drawIdx.push(Math.floor((q + 0.5) * NSTAT / NDRAW));

    function theta(mu) { return (mu - r) / sigma; }
    // Radon–Nikodym weight accumulated up to time t: Z_t = exp(−θW_t − ½θ²t).
    function weightAt(Wt, mu, t) {
      var th = theta(mu);
      return Math.exp(-th * Wt - 0.5 * th * th * t);
    }
    function weightOf(WT, mu) { return weightAt(WT, mu, T); }
    function pathValue(W, mu, i) {
      return S0 * Math.exp((mu - 0.5 * sigma * sigma) * (i * DT) + sigma * W[i]);
    }
    function meanP(mu) { return S0 * Math.exp(mu * T); }
    function weightedMeanAt(mu, i) {
      var num = 0, den = 0, t = i * DT;
      for (var p = 0; p < NSTAT; p++) {
        var w = weightAt(Wpaths[p][i], mu, t);
        num += w * pathValue(Wpaths[p], mu, i);
        den += w;
      }
      return num / den;
    }
    function meanQ(mu) { return weightedMeanAt(mu, NSTEPS); }

    var ui = scaffold(container, "rnw");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = String(Math.round(muMin * 100));
    ui.slider.max = String(Math.round(muMax * 100));
    ui.slider.step = "1";
    ui.slider.value = String(Math.round(mu0 * 100));

    var padL = 40, padR = 14, padT = 16, padB = 28;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    var yMin = 50, yMax = 190;
    function xPix(t) { return padL + t / T * plotW; }
    function yPix(v) { return clamp(padT + (yMax - v) / (yMax - yMin) * plotH, padT, Hd - padB); }

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.setLineDash([2, 3]);
      ctx.beginPath(); ctx.moveTo(padL, yPix(S0)); ctx.lineTo(Wd - padR, yPix(S0)); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText("S\u2080=" + S0, padL - 5, yPix(S0));
      ctx.fillText("150", padL - 5, yPix(150));
      ctx.textAlign = "center";
      ctx.fillText("t=0", xPix(0), Hd - 10);
      ctx.fillText("t=" + T, xPix(T), Hd - 10);
    }

    function drawPath(W, mu, color, alpha, width) {
      ctx.strokeStyle = color; ctx.globalAlpha = alpha; ctx.lineWidth = width;
      ctx.beginPath();
      for (var i = 0; i <= NSTEPS; i++) {
        var px = xPix(i * DT), py = yPix(pathValue(W, mu, i));
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();
      ctx.globalAlpha = 1;
    }

    function draw() {
      var mu = parseInt(ui.slider.value, 10) / 100;
      var th = theta(mu);
      ctx.clearRect(0, 0, Wd, Hd);
      axes();

      // every path is drawn at its Q-WEIGHT: heavy where Q counts it more.
      for (var p = 0; p < NDRAW; p++) {
        var W = Wpaths[drawIdx[p]];
        var w = weightOf(W[NSTEPS], mu);
        var a = clamp(0.12 + 0.42 * w, 0.08, 0.9);
        var lw = clamp(0.5 + 1.5 * w, 0.5, 3);
        drawPath(W, mu, "#7fa89c", a, lw);
      }

      // P-mean: S0 e^{μt}
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 2;
      ctx.beginPath();
      for (var i = 0; i <= NSTEPS; i++) {
        var t = i * DT, px = xPix(t), py = yPix(S0 * Math.exp(mu * t));
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // Q-mean: the SAME paths, averaged with the Girsanov weights (lands on S0 e^{rt})
      ctx.strokeStyle = "#b23a48"; ctx.lineWidth = 2; ctx.setLineDash([5, 4]);
      ctx.beginPath();
      for (var j = 0; j <= NSTEPS; j += 2) {
        var pxq = xPix(j * DT), pyq = yPix(weightedMeanAt(mu, j));
        if (j === 0) ctx.moveTo(pxq, pyq); else ctx.lineTo(pxq, pyq);
      }
      ctx.stroke(); ctx.setLineDash([]);

      var mq = meanQ(mu);
      ui.lab.textContent = "\u03bc = " + (mu * 100).toFixed(0) + "%";
      ui.readout.innerHTML =
        "Real-world drift <strong>\u03bc = " + (mu * 100).toFixed(0) + "%</strong>, cash rate r = " +
        (r * 100).toFixed(0) + "%, \u03c3 = " + (sigma * 100).toFixed(0) + "% \u21d2 market price of risk " +
        "<strong>\u03b8 = (\u03bc \u2212 r)/\u03c3 = " + th.toFixed(2) + "</strong>. " +
        "<span style=\"color:#0d5c4b;font-weight:600\">P-average ends at " + meanP(mu).toFixed(1) +
        "</span> (= S\u2080e^{\u03bcT}); " +
        "<span style=\"color:#b23a48;font-weight:600\">weighted Q-average ends at " + mq.toFixed(1) +
        "</span> \u2014 on S\u2080e^{rT} = " + (S0 * Math.exp(r * T)).toFixed(1) + " whatever \u03bc is. " +
        "<span class=\"rnw-note\">No path moved: darker/thicker = counts more under Q.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, theta: theta, meanP: meanP, meanQ: meanQ,
             weightedMeanAt: weightedMeanAt, weightOf: weightOf, NSTEPS: NSTEPS,
             S0: S0, r: r, sigma: sigma, T: T };
  }

  // ---------- MODE 3: the binomial price converges to Black–Scholes ----------
  function mountConvergence(container, cfg) {
    cfg = cfg || {};
    var S0 = cfg.S0 == null ? 100 : cfg.S0;
    var K = cfg.K == null ? 100 : cfg.K;
    var r = cfg.r == null ? 0.05 : cfg.r;
    var sigma = cfg.sigma == null ? 0.20 : cfg.sigma;
    var T = cfg.T == null ? 1 : cfg.T;
    var nMax = cfg.nMax == null ? 120 : cfg.nMax;
    var n0 = cfg.n == null ? 8 : cfg.n;

    var d1 = (Math.log(S0 / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
    var d2 = d1 - sigma * Math.sqrt(T);
    var bs = S0 * normCdf(d1) - K * Math.exp(-r * T) * normCdf(d2);

    // CRR tree priced as the risk-neutral expectation of the terminal payoff.
    function binom(n) {
      var dt = T / n;
      var uu = Math.exp(sigma * Math.sqrt(dt)), dd = 1 / uu;
      var R = Math.exp(r * dt);
      var pS = (R - dd) / (uu - dd);
      var qS = 1 - pS;
      var prob = Math.pow(qS, n);              // probability of j = 0 up-moves
      var sum = 0;
      for (var j = 0; j <= n; j++) {
        var ST = S0 * Math.pow(uu, j) * Math.pow(dd, n - j);
        if (ST > K) sum += prob * (ST - K);
        prob = prob * ((n - j) / (j + 1)) * (pS / qS);
      }
      return Math.exp(-r * T) * sum;
    }

    var ui = scaffold(container, "conv");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "1"; ui.slider.max = String(nMax); ui.slider.step = "1";
    ui.slider.value = String(n0);

    var padL = 44, padR = 14, padT = 18, padB = 30;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    var yLo = bs - 1.4, yHi = bs + 2.1;
    function xPix(n) { return padL + (n - 1) / (nMax - 1) * plotW; }
    function yPix(v) { return clamp(padT + (yHi - v) / (yHi - yLo) * plotH, padT, Hd - padB); }

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(padL, Hd - padB); ctx.lineTo(Wd - padR, Hd - padB); ctx.stroke();
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText(yHi.toFixed(1), padL - 5, yPix(yHi) + 6);
      ctx.fillText(yLo.toFixed(1), padL - 5, yPix(yLo) - 6);
      ctx.textAlign = "center";
      ctx.fillText("n = 1", xPix(1) + 10, Hd - 11);
      ctx.fillText("n = " + nMax, xPix(nMax) - 12, Hd - 11);
      ctx.fillText("steps in the tree", (padL + Wd - padR) / 2, Hd - 2);
    }

    function draw() {
      var n = parseInt(ui.slider.value, 10);
      ctx.clearRect(0, 0, Wd, Hd);
      axes();

      // Black–Scholes level
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 2; ctx.setLineDash([5, 4]);
      ctx.beginPath(); ctx.moveTo(padL, yPix(bs)); ctx.lineTo(Wd - padR, yPix(bs)); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#0d5c4b"; ctx.font = "10px system-ui, sans-serif"; ctx.textAlign = "left";
      ctx.fillText("Black\u2013Scholes " + bs.toFixed(3), padL + 6, yPix(bs) - 8);

      // tree prices for every n
      ctx.fillStyle = "#b23a48";
      for (var k = 1; k <= nMax; k++) {
        var v = binom(k);
        ctx.globalAlpha = k === n ? 1 : 0.35;
        ctx.beginPath(); ctx.arc(xPix(k), yPix(v), k === n ? 4 : 1.6, 0, 2 * Math.PI); ctx.fill();
      }
      ctx.globalAlpha = 1;

      var price = binom(n);
      ui.lab.textContent = "n = " + n;
      ui.readout.innerHTML =
        "<strong>" + n + "-step</strong> CRR tree (u = e^{\u03c3\u221a\u0394t}, d = 1/u, " +
        "p* = (e^{r\u0394t} \u2212 d)/(u \u2212 d)) prices the call at " +
        "<span style=\"color:#b23a48;font-weight:600\">" + price.toFixed(3) + "</span> vs the " +
        "<span style=\"color:#0d5c4b;font-weight:600\">Black\u2013Scholes value " + bs.toFixed(3) +
        "</span> \u2014 gap " + (price - bs).toFixed(3) + ". " +
        "<span class=\"conv-note\">Slide n up: the dots zig-zag (odd/even) and close in. Same idea, finer grid.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, bs: bs, binom: binom, nMax: nMax, normCdf: normCdf, d1: d1, d2: d2 };
  }

  global.RN = { mountReplication: mountReplication, mountWeights: mountWeights,
                mountConvergence: mountConvergence, _normCdf: normCdf };
})(window);
