/**
 * Confidence-interval coverage (assets/ci-coverage-viz.js)
 *
 * Makes the frequentist meaning of "95% confidence" concrete. The TRUE parameter is fixed
 * (vertical line). Each horizontal bar is a 95% CI computed from one fresh random sample.
 * About 95% of the bars cross the true line (teal); the rest miss it (red). The parameter
 * did not move — the INTERVAL is what is random. Redrawing many batches makes the long-run
 * coverage fraction hover near the nominal 95%.
 *
 * Usage:
 *   <div id="ci"></div>
 *   <script src="../assets/ci-coverage-viz.js"></script>
 *   CICoverage.mount(document.getElementById("ci"), { seed: 3, samples: 20, n: 40 });
 *
 * Expected state: ~20 stacked interval bars, a dashed vertical "true value" line, a live
 * "covered X / N" tally, and a button to draw a new batch of samples.
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
  function gauss(rng) {
    var u = 1 - rng(), v = 1 - rng();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function mount(container, config) {
    config = config || {};
    var mu = config.mu != null ? config.mu : 0;
    var sigma = config.sigma != null ? config.sigma : 1;
    var n = config.n || 40;
    var samples = config.samples || 20;
    var z = 1.96; // 95%
    var baseSeed = config.seed || 3;

    container.innerHTML = "";
    container.classList.add("ci-viz");

    var tally = document.createElement("div");
    tally.className = "ci-tally";
    container.appendChild(tally);

    var canvas = document.createElement("canvas");
    canvas.className = "ci-canvas";
    container.appendChild(canvas);

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "ci-btn";
    btn.textContent = "Draw a new batch of samples";
    container.appendChild(btn);

    var se = sigma / Math.sqrt(n);
    var half = z * se;
    var lo = mu - (half + 4 * se), hi = mu + (half + 4 * se);
    var W = 440, padL = 12, padR = 12, padT = 10, padB = 22;
    var rowH = 15;
    var H = padT + padB + samples * rowH;

    function xpix(val) { return padL + (val - lo) / (hi - lo) * (W - padL - padR); }

    function draw(seed) {
      var dpr = global.devicePixelRatio || 1;
      canvas.width = W * dpr;
      canvas.height = H * dpr;
      canvas.style.width = "100%";
      canvas.style.maxWidth = W + "px";
      canvas.style.height = "auto";
      var ctx = canvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      // True-value line.
      var tx = xpix(mu);
      ctx.strokeStyle = "#0d5c4b";
      ctx.setLineDash([4, 3]);
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(tx, padT - 2);
      ctx.lineTo(tx, H - padB + 4);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#0d5c4b";
      ctx.font = "11px system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("true value", tx, H - 6);

      var rng = mulberry32(seed);
      var covered = 0;
      for (var i = 0; i < samples; i++) {
        // Sample mean of n draws ~ Normal(mu, se). Use the CLT form directly.
        var xbar = mu + se * gauss(rng);
        var l = xbar - half, r = xbar + half;
        var hit = l <= mu && mu <= r;
        if (hit) covered++;
        var y = padT + i * rowH + rowH / 2;
        ctx.strokeStyle = hit ? "#1e6b3c" : "#922b21";
        ctx.fillStyle = hit ? "#1e6b3c" : "#922b21";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(xpix(l), y); ctx.lineTo(xpix(r), y);
        ctx.stroke();
        // end caps
        ctx.beginPath();
        ctx.moveTo(xpix(l), y - 3); ctx.lineTo(xpix(l), y + 3);
        ctx.moveTo(xpix(r), y - 3); ctx.lineTo(xpix(r), y + 3);
        ctx.stroke();
        // point estimate
        ctx.beginPath();
        ctx.arc(xpix(xbar), y, 2, 0, 2 * Math.PI);
        ctx.fill();
      }

      var pct = Math.round((covered / samples) * 100);
      tally.innerHTML = "<strong>" + covered + " / " + samples + "</strong> of these 95% intervals " +
        "(" + pct + "%) cover the true value. The rest (red) missed — by bad luck of the draw, not because the value moved.";
      tally.className = "ci-tally" + (covered >= samples - 1 ? " good" : " warn");
    }

    draw(baseSeed);
    var clicks = 0;
    btn.addEventListener("click", function () { clicks++; draw(baseSeed + clicks * 613); });
    return { redraw: draw };
  }

  global.CICoverage = { mount: mount };
})(window);
