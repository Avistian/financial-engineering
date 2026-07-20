/**
 * Scree plot & variance explained (assets/scree-viz.js)
 *
 * PCA of an N-asset returns panel under the "equicorrelation" model: every asset
 * has unit variance and every pair has the same correlation rho. That covariance
 * matrix has a closed-form spectrum, which is why it is the perfect teaching case:
 *   lambda_1 = 1 + (N-1)*rho        (the market / level factor)
 *   lambda_2 = ... = lambda_N = 1 - rho
 * so PC1 explains (1 + (N-1)*rho) / N of the total variance. As rho rises, PC1
 * eats the panel — the empirical fact that a single "market" factor dominates
 * equity returns. The bars are eigenvalues (scree); the line is cumulative %.
 *
 * Usage:
 *   <div id="scree"></div>
 *   <script src="../assets/scree-viz.js"></script>
 *   Scree.mount(document.getElementById("scree"), { n: 20, rho: 0.4 });
 *
 * Expected state: N = 20, rho = 0.4 -> lambda_1 = 8.6, PC1 = 43%. rho -> 0.7 ->
 * lambda_1 = 14.3, PC1 = 71%. rho -> 0 -> all eigenvalues 1, PC1 = 5% (a flat
 * scree: no structure, nothing to reduce).
 */
(function (global) {
  "use strict";

  function mount(container, config) {
    config = config || {};
    var N = config.n || 20;
    var rho = config.rho == null ? 0.4 : config.rho;

    container.innerHTML = "";
    container.classList.add("scree-viz");

    var readout = document.createElement("div");
    readout.className = "scree-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "scree-canvas";
    var W = 420, H = 260;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "scree-controls";
    var lab = document.createElement("span");
    lab.className = "scree-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "0"; slider.max = "90"; slider.step = "5";
    slider.value = String(Math.round(rho * 100)); slider.className = "scree-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    var ctx = canvas.getContext("2d");
    var padL = 38, padR = 38, padT = 18, padB = 34;
    var plotW = W - padL - padR, plotH = H - padT - padB;

    function draw() {
      rho = parseInt(slider.value, 10) / 100;
      var l1 = 1 + (N - 1) * rho;
      var rest = 1 - rho;
      var eig = [l1];
      for (var i = 1; i < N; i++) eig.push(rest);
      var total = N; // trace = sum of variances = N (unit variances)

      ctx.clearRect(0, 0, W, H);

      var barW = plotW / N;
      var maxEig = l1;

      // bars = eigenvalues
      var cum = 0;
      ctx.font = "10px system-ui, sans-serif";
      for (var j = 0; j < N; j++) {
        var h = (eig[j] / maxEig) * plotH;
        var x = padL + j * barW;
        var y = padT + plotH - h;
        ctx.fillStyle = j === 0 ? "#922b21" : "#0d5c4b";
        ctx.fillRect(x + 1, y, Math.max(1, barW - 2), h);
      }

      // cumulative-% line (right axis 0..100)
      cum = 0;
      ctx.strokeStyle = "#9a6b1f"; ctx.lineWidth = 2;
      ctx.beginPath();
      for (var m = 0; m < N; m++) {
        cum += eig[m] / total * 100;
        var px = padL + (m + 0.5) * barW;
        var py = padT + plotH - (cum / 100) * plotH;
        if (m === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // axes
      ctx.strokeStyle = "#d9d6cd"; ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padL, padT); ctx.lineTo(padL, padT + plotH); ctx.lineTo(padL + plotW, padT + plotH);
      ctx.stroke();
      ctx.fillStyle = "#5a635f";
      ctx.fillText("eigenvalue \u03bb", 2, padT + 8);
      ctx.fillText("cum %", W - 34, padT + 8);
      ctx.fillText("principal component (PC1 \u2026 PC" + N + ")", padL + 6, H - 8);

      var pc1pct = 100 * l1 / total;
      lab.textContent = "avg correlation \u03c1 = " + rho.toFixed(2);
      readout.innerHTML =
        "<strong>" + N + "</strong> assets, each pair correlated \u03c1 = " + rho.toFixed(2) +
        ". &nbsp;\u03bb\u2081 = <strong>" + l1.toFixed(1) + "</strong> (the market factor), " +
        "\u03bb\u2082\u2026\u03bb" + N + " = " + rest.toFixed(2) + " each. " +
        "<span class=\"scree-pc1\">PC1 explains " + pc1pct.toFixed(0) + "%</span> of total variance.";
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw };
  }

  global.Scree = { mount: mount };
})(window);
