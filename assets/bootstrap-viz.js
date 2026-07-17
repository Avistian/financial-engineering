/**
 * Bootstrap distribution of a statistic (assets/bootstrap-viz.js)
 *
 * Shows the plug-in idea in motion. We have ONE sample of returns (top strip). We cannot draw
 * fresh samples from the market, so we resample WITH REPLACEMENT from the data we have: some
 * observations get picked several times, others not at all. Each resample yields one value of
 * the statistic (here the annualised Sharpe ratio, mean/std·√12). Collecting thousands of them
 * traces the bootstrap sampling distribution (bottom histogram); its 2.5th–97.5th percentiles
 * are a 95% bootstrap confidence interval — an error bar for the Sharpe with no normality
 * assumption.
 *
 * Usage:
 *   <div id="boot"></div>
 *   <script src="../assets/bootstrap-viz.js"></script>
 *   Bootstrap.mount(document.getElementById("boot"), { seed: 11 });
 *
 * Expected state: a fixed original sample; "Resample once" highlights the picks and drops one
 * bar on the histogram; "Add 1000 resamples" fills the histogram and marks the point estimate
 * plus the percentile CI; "Reset" clears the accumulated distribution.
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
  function mean(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]; return s / a.length; }
  function std(a) {
    var m = mean(a), s = 0;
    for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m);
    return Math.sqrt(s / (a.length - 1));
  }
  var ANN = Math.sqrt(12);
  function sharpe(a) { var sd = std(a); return sd === 0 ? 0 : (mean(a) / sd) * ANN; }
  function quantile(sorted, q) {
    if (!sorted.length) return NaN;
    var idx = q * (sorted.length - 1), lo = Math.floor(idx), hi = Math.ceil(idx);
    if (lo === hi) return sorted[lo];
    return sorted[lo] + (idx - lo) * (sorted[hi] - sorted[lo]);
  }

  var LO = -1.0, HI = 3.0, BINS = 24; // fixed Sharpe axis for the histogram

  function mount(container, config) {
    config = config || {};
    var baseSeed = config.seed || 11;
    var n = config.n || 30;

    // Build one fixed original sample of monthly returns.
    var srng = mulberry32(baseSeed);
    var data = [];
    for (var i = 0; i < n; i++) data.push(0.010 + 0.040 * gauss(srng));
    var pointEst = sharpe(data);
    var rmin = Math.min.apply(null, data), rmax = Math.max.apply(null, data);

    container.innerHTML = "";
    container.classList.add("boot-viz");

    var lab = document.createElement("div");
    lab.className = "boot-label";
    lab.innerHTML = "Original sample — <strong>" + n + "</strong> monthly returns · " +
      "sample Sharpe = <strong>" + pointEst.toFixed(2) + "</strong>";
    container.appendChild(lab);

    var stripCanvas = document.createElement("canvas");
    stripCanvas.className = "boot-strip";
    container.appendChild(stripCanvas);

    var resampleLab = document.createElement("div");
    resampleLab.className = "boot-resample-lab";
    resampleLab.textContent = "Click \u201cResample once\u201d: pick 30 returns with replacement (repeats grow taller).";
    container.appendChild(resampleLab);

    var histCanvas = document.createElement("canvas");
    histCanvas.className = "boot-hist";
    container.appendChild(histCanvas);

    var ciLab = document.createElement("div");
    ciLab.className = "boot-ci-lab";
    container.appendChild(ciLab);

    var controls = document.createElement("div");
    controls.className = "boot-controls";
    var b1 = document.createElement("button"); b1.type = "button"; b1.className = "boot-btn"; b1.textContent = "Resample once";
    var b2 = document.createElement("button"); b2.type = "button"; b2.className = "boot-btn"; b2.textContent = "Add 1000 resamples";
    var b3 = document.createElement("button"); b3.type = "button"; b3.className = "boot-btn boot-btn-ghost"; b3.textContent = "Reset";
    controls.appendChild(b1); controls.appendChild(b2); controls.appendChild(b3);
    container.appendChild(controls);

    var stats = [];      // accumulated bootstrap Sharpe values
    var counts = new Array(BINS).fill(0);
    var rng = mulberry32(baseSeed + 12345);

    var stripW = 440, stripH = 84;
    var histW = 440, histH = 150;

    function xret(v) {
      var pad = 16;
      return pad + (v - rmin) / ((rmax - rmin) || 1) * (stripW - 2 * pad);
    }
    function drawStrip(picks) {
      var dpr = global.devicePixelRatio || 1;
      stripCanvas.width = stripW * dpr; stripCanvas.height = stripH * dpr;
      stripCanvas.style.width = "100%"; stripCanvas.style.maxWidth = stripW + "px"; stripCanvas.style.height = "auto";
      var ctx = stripCanvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, stripW, stripH);
      var axisY = stripH - 20;
      ctx.strokeStyle = "#d9d6cd"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(10, axisY); ctx.lineTo(stripW - 10, axisY); ctx.stroke();
      // zero tick
      ctx.strokeStyle = "#e6f2ef";
      ctx.beginPath(); ctx.moveTo(xret(0), 8); ctx.lineTo(xret(0), axisY); ctx.stroke();
      ctx.fillStyle = "#5a635f"; ctx.font = "10px system-ui, sans-serif"; ctx.textAlign = "center";
      ctx.fillText("0%", xret(0), stripH - 4);
      ctx.fillText((rmax * 100).toFixed(0) + "%", xret(rmax), stripH - 4);
      ctx.fillText((rmin * 100).toFixed(0) + "%", xret(rmin), stripH - 4);
      // dots (stacked by multiplicity if picks given)
      for (var i = 0; i < data.length; i++) {
        var c = picks ? picks[i] : 1;
        var x = xret(data[i]);
        if (!picks) {
          ctx.beginPath(); ctx.arc(x, axisY - 6, 3, 0, 2 * Math.PI);
          ctx.fillStyle = "rgba(63,85,102,0.8)"; ctx.fill();
        } else {
          for (var k = 0; k < c; k++) {
            ctx.beginPath(); ctx.arc(x, axisY - 6 - k * 6, 3, 0, 2 * Math.PI);
            ctx.fillStyle = c > 0 ? "rgba(154,107,31,0.85)" : "#ccc"; ctx.fill();
          }
          if (c === 0) {
            ctx.beginPath(); ctx.arc(x, axisY - 6, 2.5, 0, 2 * Math.PI);
            ctx.strokeStyle = "#c9c4b8"; ctx.lineWidth = 1; ctx.stroke();
          }
        }
      }
    }

    function xstat(v) {
      var pad = 8;
      return pad + (v - LO) / (HI - LO) * (histW - 2 * pad);
    }
    function drawHist() {
      var dpr = global.devicePixelRatio || 1;
      histCanvas.width = histW * dpr; histCanvas.height = histH * dpr;
      histCanvas.style.width = "100%"; histCanvas.style.maxWidth = histW + "px"; histCanvas.style.height = "auto";
      var ctx = histCanvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, histW, histH);
      var axisY = histH - 20, top = 10;
      var maxc = Math.max(1, Math.max.apply(null, counts));

      // CI band (if enough samples).
      var sorted = stats.slice().sort(function (a, b) { return a - b; });
      var loCI = null, hiCI = null;
      if (stats.length >= 50) {
        loCI = quantile(sorted, 0.025); hiCI = quantile(sorted, 0.975);
        ctx.fillStyle = "rgba(13,92,75,0.08)";
        ctx.fillRect(xstat(loCI), top, xstat(hiCI) - xstat(loCI), axisY - top);
      }

      // bars
      var bw = (histW - 16) / BINS;
      for (var i = 0; i < BINS; i++) {
        if (!counts[i]) continue;
        var h = (counts[i] / maxc) * (axisY - top);
        var x = 8 + i * bw;
        ctx.fillStyle = "rgba(63,85,102,0.65)";
        ctx.fillRect(x + 0.5, axisY - h, bw - 1, h);
      }
      // axis
      ctx.strokeStyle = "#d9d6cd"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(8, axisY); ctx.lineTo(histW - 8, axisY); ctx.stroke();
      ctx.fillStyle = "#5a635f"; ctx.font = "10px system-ui, sans-serif"; ctx.textAlign = "center";
      [-1, 0, 1, 2, 3].forEach(function (t) { ctx.fillText(t.toFixed(0), xstat(t), histH - 5); });
      ctx.fillText("bootstrap Sharpe", xstat(2.0), top + 4);

      // point estimate line
      ctx.strokeStyle = "#0d5c4b"; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(xstat(pointEst), top); ctx.lineTo(xstat(pointEst), axisY); ctx.stroke();

      if (loCI != null) {
        ctx.strokeStyle = "#922b21"; ctx.setLineDash([4, 3]);
        [loCI, hiCI].forEach(function (v) {
          ctx.beginPath(); ctx.moveTo(xstat(v), top); ctx.lineTo(xstat(v), axisY); ctx.stroke();
        });
        ctx.setLineDash([]);
      }
      return { loCI: loCI, hiCI: hiCI };
    }

    function addOne(silent) {
      var pick = [], counted = new Array(n).fill(0);
      for (var i = 0; i < n; i++) {
        var j = Math.floor(rng() * n);
        if (j >= n) j = n - 1;
        counted[j] += 1;
        pick.push(data[j]);
      }
      var s = sharpe(pick);
      stats.push(s);
      var bin = Math.floor((s - LO) / (HI - LO) * BINS);
      if (bin < 0) bin = 0; if (bin >= BINS) bin = BINS - 1;
      counts[bin] += 1;
      if (!silent) {
        drawStrip(counted);
        resampleLab.innerHTML = "This resample\u2019s Sharpe = <strong>" + s.toFixed(2) +
          "</strong> (from " + n + " draws with replacement). Total resamples: " + stats.length + ".";
      }
      return s;
    }

    function updateCILab(ci) {
      if (ci && ci.loCI != null) {
        ciLab.innerHTML = "95% bootstrap CI (2.5th\u201397.5th percentile): <strong>[" +
          ci.loCI.toFixed(2) + ", " + ci.hiCI.toFixed(2) + "]</strong> from " + stats.length +
          " resamples. Point estimate " + pointEst.toFixed(2) + " (teal line).";
        ciLab.className = "boot-ci-lab shown";
      } else {
        ciLab.innerHTML = "Add resamples to build the distribution; the CI appears once there are enough.";
        ciLab.className = "boot-ci-lab";
      }
    }

    b1.addEventListener("click", function () { addOne(false); updateCILab(drawHist()); });
    b2.addEventListener("click", function () {
      for (var i = 0; i < 1000; i++) addOne(true);
      resampleLab.innerHTML = "Added 1000 resamples. Total: " + stats.length + ". Each one is a Sharpe from a with-replacement draw.";
      updateCILab(drawHist());
    });
    b3.addEventListener("click", function () {
      stats = []; counts = new Array(BINS).fill(0); rng = mulberry32(baseSeed + 12345);
      drawStrip(null); drawHist(); updateCILab(null);
      resampleLab.textContent = "Reset. Click \u201cResample once\u201d to draw with replacement again.";
    });

    drawStrip(null);
    drawHist();
    updateCILab(null);
    return { addOne: addOne };
  }

  global.Bootstrap = { mount: mount };
})(window);
