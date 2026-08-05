/**
 * Brownian motion — scaled random walk convergence AND quadratic variation.
 * (assets/bm-viz.js)
 *
 * One reusable component, mounted in two modes because it carries two distinct
 * mechanisms in Lesson 012. Both modes draw the SAME fixed Brownian path (a fine
 * ±1 random walk, seeded so it is reproducible and the smoke test is stable), so
 * the visual lineage from Lesson 011's coin-flip tree is unbroken: up/down flips,
 * now ADDED (and rescaled by 1/√n) instead of multiplied.
 *
 *   BM.mountPaths(el, cfg)  — the scaled random walk W^(n)_t = (1/√n)·(sum of n
 *     ±1 flips) as a function of time on [0, 1]. The slider is the number of steps
 *     n = 2^k (k = 1..KMAX). As n grows the jagged walk fills in and converges to
 *     the fixed continuous limit — a Brownian path (Donsker's theorem). The key
 *     invariant shown in the readout: Var(W^(n)_t) = t at EVERY resolution, which
 *     is exactly why the scaling must be 1/√n.
 *
 *   BM.mountQVar(el, cfg)   — quadratic variation. Partition [0, 1] into m = 2^k
 *     equal pieces and sum the SQUARED increments of the same path. For the
 *     Brownian path this sum → t = 1 (it does NOT vanish); for a smooth function
 *     f(t) = t it → 0 (each squared increment is (1/m)² and there are m of them,
 *     so the sum is 1/m). That contrast — squared increments matter for BM,
 *     vanish for smooth curves — is the seed of "(dW)² = dt" and all of Itô.
 *
 * Config (both modes):
 *   seed   PRNG seed for the fixed path (default 2322)
 *   k      initial slider value 1..KMAX (default 3 → n or m = 8)
 *   kMax   max exponent (default 9 → 512 = the finest / underlying path resolution)
 *
 * Returned handle (for tests): { draw, tFine, wFine, maxAbs, qvBM(m), qvSmooth(m) }.
 *
 * Expected states (default seed 2322, kMax 9, nFine 512):
 *   paths: at k=1 a 2-step zig-zag; at k=kMax the full fine Brownian path.
 *          The endpoint W_1 = -0.707 is the same at every k (same underlying path).
 *   qvar : qvSmooth(m) = 1/m exactly (1, 0.5, 0.25, …); qvBM(m) hugs 1 (0.89, 1.09,
 *          1.02, 1.09, 1.02 for m = 4..64) and qvBM(512) = 1 exactly (each ±1/√512
 *          step squared is 1/512, ×512 = 1).
 */
(function (global) {
  "use strict";

  // Small deterministic PRNG (mulberry32) so the path is fixed and reproducible.
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // A fine ±1 random walk on [0, 1] with nFine steps, rescaled by 1/√nFine so that
  // Var(W_t) = t. Returns the cumulative path sampled at nFine + 1 grid points.
  function buildFineWalk(seed, nFine) {
    var rng = mulberry32(seed);
    var step = 1 / Math.sqrt(nFine);
    var w = new Array(nFine + 1);
    var t = new Array(nFine + 1);
    w[0] = 0; t[0] = 0;
    for (var i = 1; i <= nFine; i++) {
      w[i] = w[i - 1] + (rng() < 0.5 ? step : -step);
      t[i] = i / nFine;
    }
    return { t: t, w: w, nFine: nFine };
  }

  function fmt(v, dp) {
    var s = v.toFixed(dp == null ? 3 : dp);
    return (v >= 0 ? "+" : "") + s;
  }

  function core(container, cfg, mode) {
    cfg = cfg || {};
    var seed = cfg.seed == null ? 2322 : cfg.seed;
    var kMax = cfg.kMax == null ? 9 : cfg.kMax;
    var nFine = Math.pow(2, kMax);
    var k0 = Math.max(1, Math.min(kMax, cfg.k == null ? 3 : cfg.k));

    var path = buildFineWalk(seed, nFine);
    var maxAbs = 0;
    for (var i = 0; i <= nFine; i++) maxAbs = Math.max(maxAbs, Math.abs(path.w[i]));
    var yMax = Math.max(0.5, maxAbs * 1.15);

    var prefix = mode === "qvar" ? "qv" : "bm";
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
    slider.type = "range"; slider.min = "1"; slider.max = String(kMax); slider.step = "1";
    slider.value = String(k0);
    slider.className = prefix + "-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    var ctx = canvas.getContext("2d");
    var padL = 40, padR = 16, padT = 16, padB = 28;
    var plotW = W - padL - padR, plotH = H - padT - padB;

    function xPix(tt) { return padL + tt * plotW; }
    function yPix(ww) { return padT + (yMax - ww) / (2 * yMax) * plotH; }

    // Subsample the fine path at n+1 equally spaced grid points.
    function subsample(n) {
      var xs = [];
      for (var j = 0; j <= n; j++) {
        var idx = Math.round(j * nFine / n);
        if (idx > nFine) idx = nFine;
        xs.push({ t: j / n, w: path.w[idx] });
      }
      return xs;
    }

    function qvBM(m) {
      var pts = subsample(m), s = 0;
      for (var j = 1; j < pts.length; j++) {
        var dw = pts[j].w - pts[j - 1].w; s += dw * dw;
      }
      return s;
    }
    function qvSmooth(m) { return 1 / m; } // f(t)=t: each (Δf)²=(1/m)², ×m intervals

    function axes() {
      ctx.strokeStyle = "#c9c4b6"; ctx.lineWidth = 1;
      // zero line
      ctx.beginPath(); ctx.moveTo(padL, yPix(0)); ctx.lineTo(W - padR, yPix(0)); ctx.stroke();
      // y axis
      ctx.beginPath(); ctx.moveTo(padL, padT); ctx.lineTo(padL, H - padB); ctx.stroke();
      ctx.fillStyle = "#8d938f";
      ctx.font = "10px system-ui, sans-serif";
      ctx.textBaseline = "middle";
      ctx.textAlign = "right";
      ctx.fillText("+" + yMax.toFixed(1), padL - 5, yPix(yMax) + 5);
      ctx.fillText("0", padL - 5, yPix(0));
      ctx.fillText("-" + yMax.toFixed(1), padL - 5, yPix(-yMax) - 5);
      ctx.textAlign = "center";
      ctx.fillText("t=0", xPix(0), H - 10);
      ctx.fillText("0.5", xPix(0.5), H - 10);
      ctx.fillText("t=1", xPix(1), H - 10);
    }

    function polyline(pts, color, width) {
      ctx.strokeStyle = color; ctx.lineWidth = width;
      ctx.beginPath();
      for (var j = 0; j < pts.length; j++) {
        var x = xPix(pts[j].t), y = yPix(pts[j].w);
        if (j === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }

    function dots(pts, color, r) {
      ctx.fillStyle = color;
      for (var j = 0; j < pts.length; j++) {
        ctx.beginPath();
        ctx.arc(xPix(pts[j].t), yPix(pts[j].w), r, 0, 2 * Math.PI);
        ctx.fill();
      }
    }

    function drawPaths() {
      var n = Math.pow(2, parseInt(slider.value, 10));
      ctx.clearRect(0, 0, W, H);
      axes();
      // faint reference: the fine limiting path
      polyline(subsample(nFine), "#cfe4dd", 1);
      // the current scaled random walk
      var pts = subsample(n);
      polyline(pts, "#0d5c4b", 1.6);
      if (n <= 64) dots(pts, "#0d5c4b", 2);
      var dt = 1 / n;
      lab.textContent = "steps n = " + n;
      readout.innerHTML =
        "<strong>W<sup>(n)</sup><sub>t</sub></strong> = (1/&radic;n) &times; (sum of the first n &plusmn;1 flips), " +
        "n = <strong>" + n + "</strong> steps of width &Delta;t = 1/n = <strong>" + dt.toFixed(dt < 0.01 ? 4 : 3) +
        "</strong>. Each step moves &plusmn;1/&radic;n = &plusmn;<strong>" + (1 / Math.sqrt(n)).toFixed(3) +
        "</strong>, so its standard deviation over &Delta;t is &radic;&Delta;t. " +
        (n >= nFine
          ? "<span class=\"" + prefix + "-note\">This is the finest walk \u2014 a Brownian path.</span>"
          : "Slide right and the jagged walk fills in toward the fixed pale limit \u2014 " +
            "<span class=\"" + prefix + "-note\">the same path, seen at finer resolution.</span>") +
        " Note the spread: <strong>Var(W<sup>(n)</sup><sub>t</sub>) = t</strong> at every resolution \u2014 that is what the 1/&radic;n scaling buys.";
    }

    function drawQVar() {
      var m = Math.pow(2, parseInt(slider.value, 10));
      ctx.clearRect(0, 0, W, H);
      axes();
      // faint full path for reference
      polyline(subsample(nFine), "#cfe4dd", 1);
      // the coarse sampling whose squared increments we are summing
      var pts = subsample(m);
      // partition ticks on the zero line
      ctx.strokeStyle = "#d9c9a3"; ctx.lineWidth = 1;
      for (var j = 0; j < pts.length; j++) {
        var x = xPix(pts[j].t);
        ctx.beginPath(); ctx.moveTo(x, yPix(0) - 4); ctx.lineTo(x, yPix(0) + 4); ctx.stroke();
      }
      polyline(pts, "#0d5c4b", 1.6);
      if (m <= 64) dots(pts, "#9a6b1f", 2.2);
      var qb = qvBM(m), qs = qvSmooth(m);
      lab.textContent = "partition m = " + m;
      readout.innerHTML =
        "Partition [0, 1] into <strong>m = " + m + "</strong> equal pieces and add up the <em>squared</em> " +
        "increments. Brownian path: &Sigma;(&Delta;W)&sup2; = <strong>" + qb.toFixed(4) + "</strong> " +
        "(&rarr; t = 1, it does <em>not</em> vanish). Smooth line f(t)=t: &Sigma;(&Delta;f)&sup2; = 1/m = <strong>" +
        qs.toFixed(4) + "</strong> " +
        (m >= nFine
          ? "<span class=\"" + prefix + "-note\">At the finest mesh &Sigma;(&Delta;W)&sup2; = 1 exactly, while the smooth sum \u2192 0.</span>"
          : "(&rarr; 0). <span class=\"" + prefix + "-note\">Refine the mesh: the Brownian sum locks onto t, the smooth sum collapses.</span>");
    }

    var draw = mode === "qvar" ? drawQVar : drawPaths;
    slider.addEventListener("input", draw);
    draw();
    return { draw: draw, tFine: path.t, wFine: path.w, maxAbs: maxAbs, qvBM: qvBM, qvSmooth: qvSmooth };
  }

  global.BM = {
    mountPaths: function (el, cfg) { return core(el, cfg, "paths"); },
    mountQVar: function (el, cfg) { return core(el, cfg, "qvar"); }
  };
})(window);
