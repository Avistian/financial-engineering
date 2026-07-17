/**
 * Likelihood curve & the MLE (assets/likelihood-viz.js)
 *
 * The maximum-likelihood estimate is the parameter value that makes the observed data most
 * probable — the PEAK of the likelihood curve. This widget estimates the probability p of an
 * up-day from n Bernoulli observations (true p = 0.55). Slide n up and three things happen at
 * once, each a named property of the MLE:
 *   - the peak (the MLE p̂ = k/n) settles toward the true value        -> CONSISTENCY
 *   - the curve turns from a broad hill into a sharp spike             -> FISHER INFORMATION
 *     (curvature at the peak = how much the data "pin down" p)
 *   - the 95% interval p̂ ± 1.96·√(p̂(1−p̂)/n) narrows like 1/√n         -> ASYMPTOTIC NORMALITY
 * A flat curve = little information = wide error bar; a sharp curve = lots of information =
 * tight error bar. That is the whole intuition behind the standard error of an MLE.
 *
 * Usage:
 *   <div id="mle"></div>
 *   <script src="../assets/likelihood-viz.js"></script>
 *   Likelihood.mount(document.getElementById("mle"), { seed: 5 });
 *
 * Expected state: a likelihood curve with the MLE (teal) and true value (dashed) marked and a
 * shaded 95% interval; an n-slider that sharpens the curve and shrinks the interval as n grows.
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

  var NS = [5, 10, 25, 50, 100, 250, 500, 1000];
  var TRUE_P = 0.55;

  function mount(container, config) {
    config = config || {};
    var baseSeed = config.seed || 5;

    container.innerHTML = "";
    container.classList.add("mle-viz");

    var readout = document.createElement("div");
    readout.className = "mle-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "mle-canvas";
    container.appendChild(canvas);

    var row = document.createElement("div");
    row.className = "mle-controls";
    var label = document.createElement("label");
    label.className = "mle-slider-label";
    label.textContent = "sample size n";
    var slider = document.createElement("input");
    slider.type = "range";
    slider.min = "0"; slider.max = String(NS.length - 1); slider.step = "1"; slider.value = "3";
    slider.className = "mle-slider";
    row.appendChild(label);
    row.appendChild(slider);
    container.appendChild(row);

    var W = 440, H = 190, padL = 34, padR = 12, padT = 12, padB = 26;

    function xp(p) { return padL + p * (W - padL - padR); }

    function countUp(n) {
      // Deterministic per n: fixed number of up-days from Bernoulli(TRUE_P).
      var rng = mulberry32(baseSeed + n * 7 + 3);
      var k = 0;
      for (var i = 0; i < n; i++) if (rng() < TRUE_P) k++;
      return k;
    }

    function draw(nIndex) {
      var n = NS[nIndex];
      var k = countUp(n);
      var phat = k / n;
      var se = Math.sqrt(Math.max(phat * (1 - phat), 1e-6) / n);
      var lo = Math.max(0, phat - 1.96 * se), hi = Math.min(1, phat + 1.96 * se);

      var dpr = global.devicePixelRatio || 1;
      canvas.width = W * dpr; canvas.height = H * dpr;
      canvas.style.width = "100%"; canvas.style.maxWidth = W + "px"; canvas.style.height = "auto";
      var ctx = canvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      var baseY = H - padB, topY = padT;

      // CI band on the p-axis.
      ctx.fillStyle = "rgba(146,43,33,0.10)";
      ctx.fillRect(xp(lo), topY, xp(hi) - xp(lo), baseY - topY);

      // relative likelihood L(p)/L(phat) = exp( k ln(p/phat) + (n-k) ln((1-p)/(1-phat)) )
      ctx.beginPath();
      var first = true;
      for (var i = 0; i <= 300; i++) {
        var p = i / 300;
        var val;
        if (p <= 0 || p >= 1) {
          val = (k === 0 && p === 0) || (k === n && p === 1) ? 1 : 0;
        } else {
          var ll = k * Math.log(p / phat) + (n - k) * Math.log((1 - p) / (1 - phat));
          val = Math.exp(ll);
        }
        var x = xp(p), y = baseY - val * (baseY - topY);
        if (first) { ctx.moveTo(x, y); first = false; } else { ctx.lineTo(x, y); }
      }
      ctx.strokeStyle = "#3f5566"; ctx.lineWidth = 2; ctx.stroke();

      // axis
      ctx.strokeStyle = "#d9d6cd"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(padL, baseY); ctx.lineTo(W - padR, baseY); ctx.stroke();
      ctx.fillStyle = "#5a635f"; ctx.font = "10px system-ui, sans-serif"; ctx.textAlign = "center";
      [0, 0.25, 0.5, 0.75, 1].forEach(function (t) { ctx.fillText(t.toFixed(2), xp(t), H - 8); });
      ctx.save(); ctx.translate(10, (topY + baseY) / 2); ctx.rotate(-Math.PI / 2);
      ctx.fillText("likelihood", 0, 0); ctx.restore();

      // true value (dashed) and MLE (solid teal)
      ctx.strokeStyle = "#9a6b1f"; ctx.setLineDash([4, 3]); ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(xp(TRUE_P), topY); ctx.lineTo(xp(TRUE_P), baseY); ctx.stroke();
      ctx.setLineDash([]);
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(xp(phat), topY); ctx.lineTo(xp(phat), baseY); ctx.stroke();

      readout.innerHTML = "n = <strong>" + n + "</strong> · up-days k = " + k +
        " · MLE p&#770; = <strong>" + phat.toFixed(3) + "</strong> · 95% interval [" +
        lo.toFixed(3) + ", " + hi.toFixed(3) + "] (width " + (hi - lo).toFixed(3) +
        ") · true p = 0.55 (dashed)";
    }

    draw(parseInt(slider.value, 10));
    slider.addEventListener("input", function () { draw(parseInt(slider.value, 10)); });
    return { redraw: draw };
  }

  global.Likelihood = { mount: mount };
})(window);
