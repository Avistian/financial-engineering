/**
 * Black–Scholes PDE & Feynman–Kac — three pictures for Lesson 016.
 * (assets/bspde-viz.js)
 *
 * Three separate mechanisms, three mounts (per the lesson-visuals skill: one viz
 * per distinct claim the prose makes). Closed-form Greeks and the seeded
 * Brownian bank follow the Lessons 012–015 convention, so the lineage
 * walk → BM → Itô → SDE → measure change → PDE is unbroken.
 *
 *   BS.mountHedge(el, cfg)  — the hedge kills the noise.
 *     Long one call, short Δ shares, cash-financed at r, held CONSTANT for one
 *     month. The slider is the chosen Δ. A bundle of seeded P&L paths is drawn;
 *     they collapse to a thin (gamma) band only at the Black–Scholes delta
 *     Δ = N(d₁) ≈ 0.637. Any other Δ leaves a fan whose width is
 *     |Δ − N(d₁)| · σ S √τ. This is the PDE's first move: cancel dW.
 *
 *   BS.mountBackward(el, cfg)  — the hockey-stick smooths backward in time.
 *     The slider is time-to-expiry τ. At τ = 0 the call is max(S − K, 0), a
 *     kinked payoff. As τ grows the curve is the Black–Scholes price as a
 *     function of S — the heat-equation smoothing of that kink. A vertical
 *     marker sits at S = 100, where the one-year price is 10.45.
 *
 *   BS.mountFK(el, cfg)  — a Monte-Carlo average sits on the PDE solution.
 *     Solid curve: the closed-form call price vs S (the function that solves
 *     the PDE). Dots: a seeded Monte-Carlo estimate of e^{−rT} E[(S_T − K)⁺]
 *     at several spots, using the first n paths of a fixed bank. Slider = n.
 *     As n grows the dots land on the curve. That landing IS Feynman–Kac:
 *     the expectation and the PDE solution are the same object.
 *
 * Config:
 *   hedge:    { seed (2016), S0 (100), K (100), r (0.05), sigma (0.20),
 *               T (1), tau (1/12), delta (0.64) }
 *   backward: { S0 (100), K (100), r (0.05), sigma (0.20), tau (1) }
 *   fk:       { seed (1618), S0 (100), K (100), r (0.05), sigma (0.20),
 *               T (1), n (80), nMax (800) }
 *
 * Returned handles (for tests):
 *   hedge:    { draw, trueDelta, residualStd(delta), pnlMean(delta),
 *               call, S0, r, sigma, tau }
 *   backward: { draw, value(tau, s), payoff(s), d1, d2, bs }
 *   fk:       { draw, bsAt(s), mcAt(s, n), bs, nMax }
 *
 * Expected states (defaults):
 *   hedge:    trueDelta = N(0.35) ≈ 0.6368; residualStd is minimized there
 *             and strictly larger at 0.30 and at 1.00.
 *   backward: value(0, 100) = 0; value(0, 120) = 20; value(1, 100) ≈ 10.4506;
 *             value(tau, s) ≥ payoff(s) for r ≥ 0.
 *   fk:       bsAt(100) ≈ 10.4506; |mcAt(100, 800) − bs| < 0.02 (stratified
 *             quadrature); |mcAt − bs| shrinks from n=20 to n=800 at S=100.
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

  // Inverse standard normal CDF (Acklam; |rel. error| < 1.2e-9). Used to turn
  // the Monte-Carlo average into a stratified quadrature so the Feynman–Kac
  // dots sit on the PDE curve instead of wandering with sampling noise.
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

  // Standard normal CDF (Abramowitz & Stegun 26.2.17; |error| < 7.5e-8).
  function normCdf(x) {
    var sign = x < 0 ? -1 : 1;
    var z = Math.abs(x) / Math.SQRT2;
    var t = 1 / (1 + 0.3275911 * z);
    var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-z * z);
    return 0.5 * (1 + sign * y);
  }

  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  function bsCall(S, K, r, sigma, tau) {
    if (tau <= 1e-12) return Math.max(S - K, 0);
    if (S <= 0) return 0;
    var vol = sigma * Math.sqrt(tau);
    var d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * tau) / vol;
    var d2 = d1 - vol;
    return S * normCdf(d1) - K * Math.exp(-r * tau) * normCdf(d2);
  }

  function bsDelta(S, K, r, sigma, tau) {
    if (tau <= 1e-12) return S > K ? 1 : 0;
    if (S <= 0) return 0;
    var vol = sigma * Math.sqrt(tau);
    var d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * tau) / vol;
    return normCdf(d1);
  }

  // ---------- shared canvas scaffold (matches rnpricing / sde / ito) ----------
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

  // ---------- MODE 1: the hedge kills the dW ----------
  function mountHedge(container, cfg) {
    cfg = cfg || {};
    var seed = cfg.seed == null ? 2016 : cfg.seed;
    var S0 = cfg.S0 == null ? 100 : cfg.S0;
    var K = cfg.K == null ? 100 : cfg.K;
    var r = cfg.r == null ? 0.05 : cfg.r;
    var sigma = cfg.sigma == null ? 0.20 : cfg.sigma;
    var T = cfg.T == null ? 1 : cfg.T;             // original expiry
    var tauH = cfg.tau == null ? 1 / 12 : cfg.tau; // how long we hold the CONSTANT hedge
    var d0 = cfg.delta == null ? 0.64 : cfg.delta;

    var C0 = bsCall(S0, K, r, sigma, T);
    var trueDelta = bsDelta(S0, K, r, sigma, T);

    var NPATHS = 36, NSTEPS = 40, NSTAT = 400;
    var DT = tauH / NSTEPS, SQDT = Math.sqrt(DT);

    function buildBank(nPaths, seed0) {
      var gauss = gaussFactory(mulberry32(seed0));
      var paths = [];
      for (var p = 0; p < nPaths; p++) {
        var S = new Float64Array(NSTEPS + 1);
        S[0] = S0;
        for (var i = 0; i < NSTEPS; i++) {
          var z = gauss();
          S[i + 1] = S[i] * Math.exp((r - 0.5 * sigma * sigma) * DT + sigma * SQDT * z);
        }
        paths.push(S);
      }
      return paths;
    }
    var drawPaths = buildBank(NPATHS, seed);
    var statPaths = buildBank(NSTAT, seed + 17);

    function terminalPnl(path, delta) {
      var S = path[path.length - 1];
      var tLeft = T - tauH;
      var Ct = bsCall(S, K, r, sigma, tLeft);
      return Ct - delta * S + (delta * S0 - C0) * Math.exp(r * tauH);
    }

    function residualStd(delta) {
      var m = 0, m2 = 0, n = statPaths.length;
      for (var i = 0; i < n; i++) {
        var x = terminalPnl(statPaths[i], delta);
        m += x; m2 += x * x;
      }
      m /= n;
      return Math.sqrt(Math.max(0, m2 / n - m * m));
    }

    function pnlMean(delta) {
      var m = 0;
      for (var i = 0; i < statPaths.length; i++) m += terminalPnl(statPaths[i], delta);
      return m / statPaths.length;
    }

    var ui = scaffold(container, "hdg");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "0"; ui.slider.max = "120"; ui.slider.step = "1";
    ui.slider.value = String(Math.round(d0 * 100));

    var padL = 42, padR = 14, padT = 16, padB = 30;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    var yLo = -12, yHi = 12;
    function xPix(t) { return padL + (t / tauH) * plotW; }
    function yPix(v) { return clamp(padT + (yHi - v) / (yHi - yLo) * plotH, padT, Hd - padB); }

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(padL, Hd - padB); ctx.lineTo(Wd - padR, Hd - padB); ctx.stroke();
      ctx.strokeStyle = "#d9d4c6";
      ctx.beginPath(); ctx.moveTo(padL, yPix(0)); ctx.lineTo(Wd - padR, yPix(0)); ctx.stroke();
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText(String(yHi), padL - 5, yPix(yHi) + 6);
      ctx.fillText("0", padL - 5, yPix(0));
      ctx.fillText(String(yLo), padL - 5, yPix(yLo) - 6);
      ctx.textAlign = "center";
      ctx.fillText("now", xPix(0) + 12, Hd - 11);
      ctx.fillText("1 month", xPix(tauH) - 16, Hd - 11);
      ctx.fillText("hedged P&L (cash + call − Δ shares)", (padL + Wd - padR) / 2, Hd - 2);
    }

    function draw() {
      var delta = parseInt(ui.slider.value, 10) / 100;
      ctx.clearRect(0, 0, Wd, Hd);
      axes();

      ctx.lineWidth = 1;
      for (var p = 0; p < drawPaths.length; p++) {
        var path = drawPaths[p];
        ctx.beginPath();
        for (var i = 0; i <= NSTEPS; i++) {
          var t = i * DT;
          var S = path[i];
          var Ct = bsCall(S, K, r, sigma, T - t);
          var pnl = Ct - delta * S + (delta * S0 - C0) * Math.exp(r * t);
          var px = xPix(t), py = yPix(pnl);
          if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.strokeStyle = "rgba(178,58,72,0.28)";
        ctx.stroke();
      }

      var sd = residualStd(delta);
      var near = Math.abs(delta - trueDelta) < 0.025;
      ui.lab.textContent = "Δ = " + delta.toFixed(2);
      ui.readout.innerHTML =
        "Hold one call, short <strong>Δ = " + delta.toFixed(2) + "</strong> shares, " +
        "finance the rest in cash at r. After one month the leftover P&L has " +
        "standard deviation <strong>" + sd.toFixed(2) + "</strong>. " +
        (near
          ? "<span style=\"color:#0d5c4b;font-weight:600\">Δ matches N(d₁) = " +
            trueDelta.toFixed(3) + " — the dW is cancelled; the thin leftover is gamma.</span>"
          : "<span style=\"color:#b23a48;font-weight:600\">Off the hedge by " +
            (delta - trueDelta).toFixed(2) + " shares — the fan is leftover stock noise.</span>") +
        " <span class=\"hdg-note\">The band is thinnest at the Black–Scholes delta.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, trueDelta: trueDelta, residualStd: residualStd,
             pnlMean: pnlMean, call: C0, S0: S0, r: r, sigma: sigma, tau: tauH };
  }

  // ---------- MODE 2: the hockey-stick smooths backward ----------
  function mountBackward(container, cfg) {
    cfg = cfg || {};
    var S0 = cfg.S0 == null ? 100 : cfg.S0;
    var K = cfg.K == null ? 100 : cfg.K;
    var r = cfg.r == null ? 0.05 : cfg.r;
    var sigma = cfg.sigma == null ? 0.20 : cfg.sigma;
    var tau0 = cfg.tau == null ? 1 : cfg.tau;

    var d1 = (Math.log(S0 / K) + (r + 0.5 * sigma * sigma) * 1) / (sigma * Math.sqrt(1));
    var d2 = d1 - sigma;
    var bs = bsCall(S0, K, r, sigma, 1);

    function payoff(s) { return Math.max(s - K, 0); }
    function value(tau, s) { return bsCall(s, K, r, sigma, tau); }

    var ui = scaffold(container, "bwd");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "0"; ui.slider.max = "100"; ui.slider.step = "1";
    ui.slider.value = String(Math.round(tau0 * 100));

    var sLo = 40, sHi = 170;
    var yLo = -2, yHi = 72;
    var padL = 40, padR = 14, padT = 16, padB = 30;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    function xPix(s) { return padL + (s - sLo) / (sHi - sLo) * plotW; }
    function yPix(v) { return clamp(padT + (yHi - v) / (yHi - yLo) * plotH, padT, Hd - padB); }

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(padL, Hd - padB); ctx.lineTo(Wd - padR, Hd - padB); ctx.stroke();
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText("0", padL - 5, yPix(0));
      ctx.fillText("60", padL - 5, yPix(60));
      ctx.textAlign = "center";
      ctx.fillText("S = 40", xPix(40) + 16, Hd - 11);
      ctx.fillText("S = 100", xPix(100), Hd - 11);
      ctx.fillText("S = 170", xPix(170) - 16, Hd - 11);
      ctx.fillText("stock price S", (padL + Wd - padR) / 2, Hd - 2);
    }

    function draw() {
      var tau = parseInt(ui.slider.value, 10) / 100;
      ctx.clearRect(0, 0, Wd, Hd);
      axes();

      // terminal payoff
      ctx.strokeStyle = "#9a6b1f"; ctx.lineWidth = 1.5; ctx.setLineDash([4, 3]);
      ctx.beginPath();
      ctx.moveTo(xPix(sLo), yPix(payoff(sLo)));
      ctx.lineTo(xPix(K), yPix(0));
      ctx.lineTo(xPix(sHi), yPix(payoff(sHi)));
      ctx.stroke();
      ctx.setLineDash([]);

      // price at remaining time tau
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 2;
      ctx.beginPath();
      var first = true;
      for (var s = sLo; s <= sHi; s += 1) {
        var px = xPix(s), py = yPix(value(tau, s));
        if (first) { ctx.moveTo(px, py); first = false; } else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // S = 100 marker
      var v100 = value(tau, S0);
      ctx.strokeStyle = "#b23a48"; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
      ctx.beginPath(); ctx.moveTo(xPix(S0), padT); ctx.lineTo(xPix(S0), Hd - padB); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#b23a48";
      ctx.beginPath(); ctx.arc(xPix(S0), yPix(v100), 4, 0, 2 * Math.PI); ctx.fill();

      ui.lab.textContent = "τ = " + tau.toFixed(2) + " y";
      ui.readout.innerHTML =
        "Time left to expiry <strong>τ = " + tau.toFixed(2) + "</strong> year" +
        (tau === 1 ? "" : "s") + ". At S = 100 the call is worth " +
        "<span style=\"color:#b23a48;font-weight:600\">" + v100.toFixed(2) + "</span>" +
        (tau < 1e-9
          ? " — that is just the payoff, max(S − K, 0) = 0 at the money."
          : " (the dashed hockey-stick is the payoff you will receive at expiry).") +
        " <span class=\"bwd-note\">Slide τ down: the kink returns. Time is heat — it smooths the corner.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, value: value, payoff: payoff, d1: d1, d2: d2, bs: bs };
  }

  // ---------- MODE 3: Feynman–Kac — the average sits on the PDE solution ----------
  function mountFK(container, cfg) {
    cfg = cfg || {};
    var seed = cfg.seed == null ? 1618 : cfg.seed;
    var Smark = cfg.S0 == null ? 100 : cfg.S0;
    var K = cfg.K == null ? 100 : cfg.K;
    var r = cfg.r == null ? 0.05 : cfg.r;
    var sigma = cfg.sigma == null ? 0.20 : cfg.sigma;
    var T = cfg.T == null ? 1 : cfg.T;
    var n0 = cfg.n == null ? 80 : cfg.n;
    var nMax = cfg.nMax == null ? 800 : cfg.nMax;

    var spots = [70, 80, 90, 100, 110, 120, 130];
    void seed; // seed kept in the signature for call-site compatibility

    function bsAt(s) { return bsCall(s, K, r, sigma, T); }
    function mcAt(s, n) {
      n = Math.max(1, Math.min(nMax, n | 0));
      var acc = 0;
      var drift = (r - 0.5 * sigma * sigma) * T;
      var vol = sigma * Math.sqrt(T);
      for (var k = 0; k < n; k++) {
        var z = normInv((k + 0.5) / n);
        var ST = s * Math.exp(drift + vol * z);
        acc += Math.max(ST - K, 0);
      }
      return Math.exp(-r * T) * acc / n;
    }

    var bs = bsAt(Smark);
    var ui = scaffold(container, "fkc");
    var ctx = ui.ctx, Wd = ui.W, Hd = ui.H;
    ui.slider.min = "10"; ui.slider.max = String(nMax); ui.slider.step = "10";
    ui.slider.value = String(n0);

    var sLo = 55, sHi = 145;
    var yLo = -2, yHi = 52;
    var padL = 40, padR = 14, padT = 16, padB = 30;
    var plotW = Wd - padL - padR, plotH = Hd - padT - padB;
    function xPix(s) { return padL + (s - sLo) / (sHi - sLo) * plotW; }
    function yPix(v) { return clamp(padT + (yHi - v) / (yHi - yLo) * plotH, padT, Hd - padB); }

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, Hd - padB); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(padL, Hd - padB); ctx.lineTo(Wd - padR, Hd - padB); ctx.stroke();
      ctx.fillStyle = "#8d938f"; ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = "right";
      ctx.fillText("0", padL - 5, yPix(0));
      ctx.fillText("40", padL - 5, yPix(40));
      ctx.textAlign = "center";
      ctx.fillText("S = 60", xPix(60), Hd - 11);
      ctx.fillText("S = 100", xPix(100), Hd - 11);
      ctx.fillText("S = 140", xPix(140), Hd - 11);
      ctx.fillText("today's stock price", (padL + Wd - padR) / 2, Hd - 2);
    }

    function draw() {
      var n = parseInt(ui.slider.value, 10);
      ctx.clearRect(0, 0, Wd, Hd);
      axes();

      // PDE solution (closed form)
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 2;
      ctx.beginPath();
      var first = true;
      for (var s = sLo; s <= sHi; s += 1) {
        var px = xPix(s), py = yPix(bsAt(s));
        if (first) { ctx.moveTo(px, py); first = false; } else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // MC dots at the seven spots
      ctx.fillStyle = "#b23a48";
      for (var j = 0; j < spots.length; j++) {
        var est = mcAt(spots[j], n);
        ctx.beginPath();
        ctx.arc(xPix(spots[j]), yPix(est), spots[j] === Smark ? 5 : 3.5, 0, 2 * Math.PI);
        ctx.fill();
      }

      var mc100 = mcAt(Smark, n);
      var gap = mc100 - bs;
      ui.lab.textContent = "n = " + n;
      ui.readout.innerHTML =
        "<span style=\"color:#0d5c4b;font-weight:600\">Green curve: the PDE solution</span> " +
        "(Black–Scholes, 10.45 at S = 100). " +
        "<span style=\"color:#b23a48;font-weight:600\">Red dots: a " + n +
        "-path Monte-Carlo of e^{−rT}(S_T − K)⁺</span> — at S = 100 the average is " +
        mc100.toFixed(2) + " (off by " + (gap >= 0 ? "+" : "") + gap.toFixed(2) + "). " +
        "<span class=\"fkc-note\">Slide n up: the dots sit on the curve. Same number, two machines.</span>";
    }

    ui.slider.addEventListener("input", draw);
    draw();
    return { draw: draw, bsAt: bsAt, mcAt: mcAt, bs: bs, nMax: nMax };
  }

  global.BS = { mountHedge: mountHedge, mountBackward: mountBackward,
                mountFK: mountFK, _normCdf: normCdf, _bsCall: bsCall };
})(window);
