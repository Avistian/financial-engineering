/**
 * The false-discovery factory (assets/multiple-testing-viz.js)
 *
 * A field of M "strategies" that ALL have zero true edge (every null hypothesis is true). Each
 * gets one honest test, which under the null produces a p-value drawn Uniform(0,1) — the key fact
 * that makes multiple testing bite. A cell lights red when its p-value falls below the decision
 * threshold, i.e. it is a *false* discovery (there is no edge to find). At the nominal 5% level
 * roughly 5% of the field lights up no matter what; the tally shows observed vs the expected
 * count α·M. Toggle "Bonferroni" to tighten the threshold to α/M and watch the false discoveries
 * collapse toward zero (family-wise error control). "Re-run" redraws the p-values so the learner
 * sees the count fluctuate around its expectation.
 *
 * Usage:
 *   <div id="mt"></div>
 *   <script src="../assets/multiple-testing-viz.js"></script>
 *   MultipleTesting.mount(document.getElementById("mt"), { seed: 4, m: 100 });
 *
 * Expected state: 100 tests, α = 0.05 → about 5 red cells (expected 5.0). Bonferroni on → almost
 * always 0 red. Slider raises M up to 500 → ~25 expected false positives at nominal 5%.
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

  function mount(container, config) {
    config = config || {};
    var baseSeed = config.seed || 4;
    var m = config.m || 100;
    var alpha = config.alpha || 0.05;
    var bonferroni = false;
    var seedTick = 0;

    container.innerHTML = "";
    container.classList.add("mt-viz");

    var tally = document.createElement("div");
    tally.className = "mt-tally";
    container.appendChild(tally);

    var grid = document.createElement("div");
    grid.className = "mt-grid";
    container.appendChild(grid);

    var controls = document.createElement("div");
    controls.className = "mt-controls";

    var sizeWrap = document.createElement("span");
    sizeWrap.className = "mt-slider-label";
    var slider = document.createElement("input");
    slider.type = "range"; slider.min = "20"; slider.max = "500"; slider.step = "20";
    slider.value = String(m); slider.className = "mt-slider";
    sizeWrap.appendChild(slider);

    var rerun = document.createElement("button");
    rerun.type = "button"; rerun.className = "mt-btn"; rerun.textContent = "Re-run tests";

    var bonf = document.createElement("button");
    bonf.type = "button"; bonf.className = "mt-btn mt-btn-ghost"; bonf.textContent = "Bonferroni: off";

    controls.appendChild(sizeWrap);
    controls.appendChild(rerun);
    controls.appendChild(bonf);
    container.appendChild(controls);

    function draw() {
      m = parseInt(slider.value, 10);
      var thresh = bonferroni ? alpha / m : alpha;
      var rng = mulberry32(baseSeed + seedTick * 7919);
      grid.innerHTML = "";
      var falsePos = 0;
      for (var i = 0; i < m; i++) {
        var p = rng(); // Uniform(0,1): the null p-value distribution
        var cell = document.createElement("span");
        cell.className = "mt-cell";
        if (p < thresh) { cell.classList.add("mt-hit"); falsePos++; }
        cell.title = "p = " + p.toFixed(3);
        grid.appendChild(cell);
      }
      var expected = alpha * m;
      var label = "mt-slider-label";
      tally.innerHTML =
        "<strong>" + m + "</strong> worthless strategies · threshold = <strong>" +
        (bonferroni ? "&alpha;/M = " + thresh.toExponential(1) : "&alpha; = 0.05") + "</strong><br>" +
        "<span class=\"mt-count\">" + falsePos + "</span> \u201csignificant\u201d results \u2014 " +
        "<em>every one is false</em> (there is no edge). " +
        (bonferroni
          ? "Bonferroni controls the chance of <em>any</em> false positive at \u2264 5%."
          : "Expected at nominal 5%: <strong>" + expected.toFixed(1) + "</strong>.");
      slider.setAttribute("aria-label", m + " tests");
    }

    slider.addEventListener("input", draw);
    rerun.addEventListener("click", function () { seedTick++; draw(); });
    bonf.addEventListener("click", function () {
      bonferroni = !bonferroni;
      bonf.textContent = "Bonferroni: " + (bonferroni ? "on" : "off");
      bonf.classList.toggle("mt-btn-active", bonferroni);
      draw();
    });

    draw();
    return { draw: draw };
  }

  global.MultipleTesting = { mount: mount };
})(window);
