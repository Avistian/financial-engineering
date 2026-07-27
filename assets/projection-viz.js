/**
 * Conditional expectation as an L² projection (assets/projection-viz.js)
 *
 * A 2-D slice of the space of random variables. The horizontal line is the set of
 * candidate guesses that are measurable with respect to the information you have —
 * parameterised as Y(s) = E[X|F] + s·Z for a fixed measurable direction Z with
 * E[Z²] = 1. The point X sits OFF that line, at perpendicular distance
 * rmse = √E[(X − E[X|F])²]: the part of X your information cannot explain.
 *
 * Because the residual X − E[X|F] is orthogonal to every measurable Z (that is the
 * defining property of conditional expectation), Pythagoras gives exactly
 *
 *     E[(X − Y(s))²] = E[(X − E[X|F])²] + s²  =  mseMin + s²,
 *
 * so the numeric readout and the picture agree step for step: the squared distance
 * bottoms out precisely at the foot of the perpendicular, s = 0, where the error
 * vector meets the subspace at 90°. Sliding s off zero shows the penalty s² grow.
 *
 * Config:
 *   mseMin  minimum mean squared error E[(X − E[X|F])²]  (default 83.217, the
 *           Lesson 011 tree value for the call payoff V conditioned on F₁)
 *   sMax    slider half-range for s (default 12)
 *   s       initial slider value (default 7, i.e. deliberately off the minimum)
 *   xName   label for the target variable (default "V")
 *   yName   label for the projection (default "E[V|F₁]")
 *
 * Usage:
 *   <div id="proj"></div>
 *   <script src="../assets/projection-viz.js"></script>
 *   Projection.mount(document.getElementById("proj"), { mseMin: 83.217, s: 7 });
 *
 * Expected states: s = 0 → readout shows the minimum (83.22), the angle reads 90°,
 * the right-angle marker appears and the verdict turns green ("this is E[V|F₁]").
 * s = ±7 → 83.22 + 49 = 132.22, angle ≈ 52.5°, verdict amber. s = ±12 → 227.22.
 */
(function (global) {
  "use strict";

  function mount(container, config) {
    config = config || {};
    var mseMin = config.mseMin == null ? 83.217 : config.mseMin;
    var sMax = config.sMax == null ? 12 : config.sMax;
    var s0 = config.s == null ? 7 : config.s;
    var xName = config.xName || "V";
    var yName = config.yName || "E[V|\u2131\u2081]";

    container.innerHTML = "";
    container.classList.add("proj-viz");

    var readout = document.createElement("div");
    readout.className = "proj-readout";
    container.appendChild(readout);

    var canvas = document.createElement("canvas");
    canvas.className = "proj-canvas";
    var W = 440, H = 260;
    canvas.width = W; canvas.height = H;
    canvas.style.width = "100%";
    canvas.style.maxWidth = W + "px";
    container.appendChild(canvas);

    var controls = document.createElement("div");
    controls.className = "proj-controls";
    var lab = document.createElement("span");
    lab.className = "proj-slider-label";
    var slider = document.createElement("input");
    slider.type = "range";
    slider.min = String(-sMax); slider.max = String(sMax); slider.step = "1";
    slider.value = String(s0);
    slider.className = "proj-slider";
    controls.appendChild(lab);
    controls.appendChild(slider);
    container.appendChild(controls);

    var ctx = canvas.getContext("2d");
    var rmse = Math.sqrt(mseMin);
    var originX = W / 2, originY = H - 70;     // foot of the perpendicular (s = 0)
    var unit = Math.min((W / 2 - 60) / sMax, (originY - 46) / rmse);

    function sx(s) { return originX + s * unit; }

    function draw() {
      var s = parseInt(slider.value, 10);
      var mse = mseMin + s * s;
      var atMin = s === 0;
      var angle = Math.atan2(rmse, Math.abs(s)) * 180 / Math.PI;

      ctx.clearRect(0, 0, W, H);
      ctx.font = "11px system-ui, sans-serif";
      ctx.textBaseline = "middle";

      // the subspace of measurable guesses
      ctx.strokeStyle = "#9a6b1f"; ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(originX - sMax * unit - 24, originY);
      ctx.lineTo(originX + sMax * unit + 24, originY);
      ctx.stroke();
      ctx.fillStyle = "#9a6b1f"; ctx.textAlign = "left";
      ctx.fillText("guesses your information allows:  Y(s) = " + yName + " + s\u00b7Z",
        originX - sMax * unit - 22, originY + 26);

      var Xx = originX, Xy = originY - rmse * unit;
      var Yx = sx(s);

      // the residual (perpendicular) leg
      ctx.strokeStyle = "rgba(146,43,33,0.55)"; ctx.lineWidth = 1.4;
      ctx.setLineDash([4, 3]);
      ctx.beginPath(); ctx.moveTo(Xx, Xy); ctx.lineTo(originX, originY); ctx.stroke();
      ctx.setLineDash([]);

      // the error vector X - Y(s)
      ctx.strokeStyle = atMin ? "#1e6b3c" : "#922b21"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(Yx, originY); ctx.lineTo(Xx, Xy); ctx.stroke();

      // right-angle marker at the foot when s = 0
      if (atMin) {
        ctx.strokeStyle = "#1e6b3c"; ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(originX + 10, originY);
        ctx.lineTo(originX + 10, originY - 10);
        ctx.lineTo(originX, originY - 10);
        ctx.stroke();
      }

      // X, the projection, and the candidate
      ctx.fillStyle = "#0d5c4b";
      ctx.beginPath(); ctx.arc(Xx, Xy, 4.5, 0, 2 * Math.PI); ctx.fill();
      ctx.textAlign = "center";
      ctx.fillText(xName + "  (the thing you are guessing)", Xx, Xy - 16);

      ctx.fillStyle = "#17201d";
      ctx.beginPath(); ctx.arc(originX, originY, 4, 0, 2 * Math.PI); ctx.fill();
      ctx.fillText(yName, originX, originY + 46);

      ctx.fillStyle = atMin ? "#1e6b3c" : "#922b21";
      ctx.beginPath(); ctx.arc(Yx, originY, 4, 0, 2 * Math.PI); ctx.fill();
      if (!atMin) {
        ctx.textAlign = s > 0 ? "left" : "right";
        ctx.fillText("Y(s)", Yx + (s > 0 ? 8 : -8), originY - 14);
      }

      // the perpendicular distance label (right-aligned so it never runs off the canvas)
      ctx.fillStyle = "#8d938f"; ctx.textAlign = "right";
      ctx.fillText(rmse.toFixed(2) + " = what you cannot know", originX - 8, (Xy + originY) / 2);

      lab.textContent = "step along the subspace: s = " + s;
      readout.innerHTML =
        "E[(" + xName + " \u2212 Y)\u00b2] = <strong>" + mse.toFixed(2) + "</strong> = " +
        mseMin.toFixed(2) + " + s\u00b2 &nbsp;(s = " + s + "). " +
        "Angle between the error and the subspace: <strong>" + angle.toFixed(1) + "\u00b0</strong>. " +
        (atMin
          ? "<span class=\"proj-min\">Minimum \u2014 the error is orthogonal to every measurable guess. " +
            "That is exactly what makes " + yName + " the conditional expectation.</span>"
          : "<span class=\"proj-off\">Not minimal \u2014 you pay s\u00b2 = " + (s * s) +
            " extra for stepping off the projection.</span>");
    }

    slider.addEventListener("input", draw);
    draw();
    return { draw: draw };
  }

  global.Projection = { mount: mount };
})(window);
