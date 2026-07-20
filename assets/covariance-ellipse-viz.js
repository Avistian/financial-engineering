/**
 * Covariance ellipse & eigenvectors (assets/covariance-ellipse-viz.js)
 *
 * A cloud of two correlated asset returns (x = asset A, y = asset B). Overlaid:
 *   - the 2-sigma covariance ellipse (the shape the covariance matrix describes),
 *   - the two eigenvectors of the covariance matrix, drawn from the centre and
 *     scaled by sqrt(eigenvalue) = the standard deviation ALONG that direction.
 * The correlation slider re-draws the cloud. As |rho| -> 1 the ellipse becomes a
 * thin cigar: almost all variance collapses onto the first principal axis (PC1),
 * so lambda_1 / (lambda_1 + lambda_2) -> 1. This is the geometry PCA exploits.
 *
 * Usage:
 *   <div id="cov"></div>
 *   <script src="../assets/covariance-ellipse-viz.js"></script>
 *   CovEllipse.mount(document.getElementById("cov"), { rho: 0.7 });
 *
 * Expected state: rho = 0.7, sx = 1.0, sy = 0.6 -> a tilted ellipse; PC1 explains
 * ~85%+ of variance. Slide rho to 0 -> upright axis-aligned ellipse, PCs align with
 * the raw axes. Slide rho to 0.95 -> near-line, PC1 explains ~95%+.
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

  // Eigen-decomposition of a symmetric 2x2 [[a,b],[b,c]] -> {l1,l2,v1,v2}, l1>=l2.
  function eig2(a, b, c) {
    var tr = a + c, det = a * c - b * b;
    var disc = Math.sqrt(Math.max(0, tr * tr / 4 - det));
    var l1 = tr / 2 + disc, l2 = tr / 2 - disc;
    function vecFor(l) {
      // (A - lI)v = 0
      var vx, vy;
      if (Math.abs(b) > 1e-9) { vx = l - c; vy = b; }
      else { vx = (Math.abs(a - l) < Math.abs(c - l)) ? 1 : 0; vy = 1 - vx; }
      var n = Math.hypot(vx, vy) || 1;
      return [vx / n, vy / n];
    }
    return { l1: l1, l2: l2, v1: vecFor(l1), v2: vecFor(l2) };
  }

  function mount(container, config) {
    config = config || {};
    var rho = config.rho == null ? 0.7 : config.rho;
    var sx = config.sx || 1.0;
    var sy = config.sy || 0.6;
    var seed = config.seed || 11;
    var N = config.n || 320;

    container.innerHTML = "";
    container.classList.add("cov-viz");

    var readout = document.createElement("div");
    readout.className = "cov-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "cov-canvas";
    var W = 420, H = 300;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "cov-controls";
    var lab = document.createElement("span");
    lab.className = "cov-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "-95"; slider.max = "95"; slider.step = "5";
    slider.value = String(Math.round(rho * 100)); slider.className = "cov-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    var ctx = canvas.getContext("2d");
    var cx = W / 2, cy = H / 2;
    var scale = 34; // px per unit of return (std)

    function toPx(x, y) { return [cx + x * scale, cy - y * scale]; }

    function draw() {
      rho = parseInt(slider.value, 10) / 100;
      var cov = rho * sx * sy;
      var a = sx * sx, b = cov, c = sy * sy;
      var e = eig2(a, b, c);
      var total = e.l1 + e.l2;
      var pc1pct = 100 * e.l1 / total;

      ctx.clearRect(0, 0, W, H);

      // axes
      ctx.strokeStyle = "#d9d6cd"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(W, cy); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, H); ctx.stroke();
      ctx.fillStyle = "#5a635f"; ctx.font = "11px system-ui, sans-serif";
      ctx.fillText("return A", W - 60, cy - 6);
      ctx.fillText("return B", cx + 6, 12);

      // point cloud (correlated Gaussian via z1, z2)
      var rng = mulberry32(seed);
      ctx.fillStyle = "rgba(13,92,75,0.42)";
      for (var i = 0; i < N; i++) {
        var z1 = randn(rng), z2 = randn(rng);
        var x = sx * z1;
        var y = sy * (rho * z1 + Math.sqrt(1 - rho * rho) * z2);
        var p = toPx(x, y);
        ctx.beginPath(); ctx.arc(p[0], p[1], 2.1, 0, 2 * Math.PI); ctx.fill();
      }

      // 2-sigma covariance ellipse: axes = 2*sqrt(lambda) along eigenvectors
      var k = 2;
      ctx.strokeStyle = "#9a6b1f"; ctx.lineWidth = 2;
      ctx.beginPath();
      for (var t = 0; t <= 360; t += 4) {
        var th = t * Math.PI / 180;
        var ex = k * Math.sqrt(e.l1) * Math.cos(th);
        var ey = k * Math.sqrt(e.l2) * Math.sin(th);
        var wx = e.v1[0] * ex + e.v2[0] * ey;
        var wy = e.v1[1] * ex + e.v2[1] * ey;
        var pp = toPx(wx, wy);
        if (t === 0) ctx.moveTo(pp[0], pp[1]); else ctx.lineTo(pp[0], pp[1]);
      }
      ctx.stroke();

      // eigenvectors from centre, length = sqrt(lambda) (1 std along axis)
      function arrow(v, l, color, label) {
        var ex = v[0] * Math.sqrt(l), ey = v[1] * Math.sqrt(l);
        var p0 = toPx(0, 0), p1 = toPx(ex, ey);
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(p0[0], p0[1]); ctx.lineTo(p1[0], p1[1]); ctx.stroke();
        var ang = Math.atan2(p1[1] - p0[1], p1[0] - p0[0]);
        ctx.beginPath();
        ctx.moveTo(p1[0], p1[1]);
        ctx.lineTo(p1[0] - 8 * Math.cos(ang - 0.4), p1[1] - 8 * Math.sin(ang - 0.4));
        ctx.lineTo(p1[0] - 8 * Math.cos(ang + 0.4), p1[1] - 8 * Math.sin(ang + 0.4));
        ctx.closePath(); ctx.fill();
        ctx.font = "bold 11px system-ui, sans-serif";
        ctx.fillText(label, p1[0] + 5, p1[1] - 5);
      }
      arrow(e.v1, e.l1, "#922b21", "PC1");
      arrow(e.v2, e.l2, "#0d5c4b", "PC2");

      lab.textContent = "correlation \u03c1 = " + rho.toFixed(2);
      readout.innerHTML =
        "Covariance matrix \u03a3 = [[" + a.toFixed(2) + ", " + b.toFixed(2) +
        "], [" + b.toFixed(2) + ", " + c.toFixed(2) + "]] &nbsp;\u2192&nbsp; " +
        "eigenvalues <strong>\u03bb\u2081 = " + e.l1.toFixed(2) + "</strong>, " +
        "<strong>\u03bb\u2082 = " + e.l2.toFixed(2) + "</strong>. " +
        "PC1 explains <strong>" + pc1pct.toFixed(0) + "%</strong> of total variance.";
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw };
  }

  global.CovEllipse = { mount: mount };
})(window);
