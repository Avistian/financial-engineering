// Minimal DOM + canvas stub to smoke-test the lesson widgets in Node (no browser).
const fs = require("fs");

function makeCtx() {
  return new Proxy({}, {
    get(t, k) {
      if (k in t) return t[k];
      return function () {}; // any canvas method is a no-op
    },
    set(t, k, v) { t[k] = v; return true; }
  });
}

function makeEl(tag) {
  const listeners = {};
  const el = {
    tagName: tag, children: [], _listeners: listeners,
    style: {}, dataset: {}, _cls: new Set(),
    classList: {
      add: (...c) => c.forEach(x => el._cls.add(x)),
      remove: (...c) => c.forEach(x => el._cls.delete(x)),
      toggle: (c, on) => { on ? el._cls.add(c) : el._cls.delete(c); },
      contains: c => el._cls.has(c),
    },
    appendChild(c) { this.children.push(c); return c; },
    addEventListener(ev, cb) { (listeners[ev] = listeners[ev] || []).push(cb); },
    setAttribute() {}, getAttribute() { return null; },
    querySelectorAll() { return []; },
    getContext() { return makeCtx(); },
    dispatch(ev) { (listeners[ev] || []).forEach(cb => cb({})); },
    set innerHTML(v) { this._html = v; this.children = []; },
    get innerHTML() { return this._html || ""; },
    set textContent(v) { this._text = v; },
    get textContent() { return this._text || ""; },
    get firstChild() { return this.children[0] || null; },
    width: 0, height: 0, value: "0",
  };
  return el;
}

global.window = global;
global.devicePixelRatio = 2;
global.document = {
  createElement: makeEl,
  getElementById: () => makeEl("div"),
};

const files = [
  "assets/pvalue-viz.js",
  "assets/multiple-testing-viz.js",
  "assets/haircut-viz.js",
  "assets/covariance-ellipse-viz.js",
  "assets/scree-viz.js",
  "assets/ols-fit-viz.js",
  "assets/hsk-viz.js",
  "assets/hac-viz.js",
  "assets/autopsy-viz.js",
  "assets/tree-viz.js",
  "assets/projection-viz.js",
  "assets/bm-viz.js",
  "assets/ito-viz.js",
  "assets/sde-viz.js",
  "assets/rnpricing-viz.js",
  "assets/bspde-viz.js",
];
files.forEach(f => { eval(fs.readFileSync(f, "utf8")); });

let ok = true;
function trap(name, fn) {
  try { fn(); console.log("  OK   " + name); }
  catch (e) { ok = false; console.log("  FAIL " + name + " -> " + e.message + "\n" + e.stack); }
}

trap("PValue.mount + slide", () => {
  const el = makeEl("div");
  const w = window.PValue.mount(el, { t: 1.4 });
  el.children.forEach(c => { if (c.tagName === "input") { c.value = "2.5"; c.dispatch("input"); } });
  el.children.forEach(c => { if (c.tagName === "input") { c.value = "0"; c.dispatch("input"); } });
});

trap("MultipleTesting.mount + rerun + bonferroni + slide", () => {
  const el = makeEl("div");
  window.MultipleTesting.mount(el, { seed: 4, m: 100 });
  // find buttons and slider among children
  const btns = el.children.filter(c => c.tagName === "button");
  const wrap = el.children.filter(c => c._cls.has("mt-controls"))[0];
  btns.forEach(b => b.dispatch("click"));
  // slider is nested; dispatch on any input found recursively
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "500"; i.dispatch("input"); });
  btns.forEach(b => b.dispatch("click")); // toggle bonferroni back etc.
});

trap("Haircut.mount + slide", () => {
  const el = makeEl("div");
  window.Haircut.mount(el, { m: 100 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "1000"; i.dispatch("input"); i.value = "0"; i.dispatch("input"); });
});

trap("CovEllipse.mount + slide", () => {
  const el = makeEl("div");
  window.CovEllipse.mount(el, { rho: 0.7 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "-95"; i.dispatch("input"); i.value = "0"; i.dispatch("input"); i.value = "95"; i.dispatch("input"); });
});

trap("Scree.mount + slide", () => {
  const el = makeEl("div");
  window.Scree.mount(el, { n: 20, rho: 0.4 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "90"; i.dispatch("input"); });
});

trap("OLSFit.mount + slide", () => {
  const el = makeEl("div");
  window.OLSFit.mount(el, { seed: 7 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "50"; i.dispatch("input"); i.value = "100"; i.dispatch("input"); });
});

trap("HSK.mount + slide", () => {
  const el = makeEl("div");
  window.HSK.mount(el, { k: 1.2 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "100"; i.dispatch("input"); });
});

trap("HAC.mount + slide", () => {
  const el = makeEl("div");
  window.HAC.mount(el, { phi: 0.5 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "85"; i.dispatch("input"); });
});

trap("Autopsy.mount + slide", () => {
  const el = makeEl("div");
  window.Autopsy.mount(el, { t0: 6.2, infl: 2.7, m: 50 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "50"; i.dispatch("input"); i.value = "100"; i.dispatch("input"); });
});

// ---- geometry harness: record canvas draw calls and assert they stay in bounds ----
// The stub above makes every canvas method a no-op, which catches crashes but not layout
// bugs (labels running off the edge, bands wider than the canvas). This records the
// coordinates instead and checks them, since we cannot open a browser here.
function withRecordedCanvas(fn) {
  const canvases = [];
  const realCreate = global.document.createElement;
  global.document.createElement = function (tag) {
    const el = realCreate(tag);
    if (tag === "canvas") {
      const calls = [];
      const store = {};
      el.getContext = () => new Proxy({}, {
        get(t, k) {
          if (k in store) return store[k];
          return function () { calls.push({ op: k, args: Array.from(arguments) }); };
        },
        set(t, k, v) { store[k] = v; return true; }
      });
      el._calls = calls;
      canvases.push(el);
    }
    return el;
  };
  try { fn(); } finally { global.document.createElement = realCreate; }
  return canvases;
}

function assertInBounds(canvas, label) {
  const W = canvas.width, H = canvas.height, m = 2;
  const pts = [];
  canvas._calls.forEach(c => {
    const a = c.args;
    switch (c.op) {
      case "moveTo": case "lineTo": pts.push([a[0], a[1], c.op]); break;
      case "arc": pts.push([a[0], a[1], "arc"]); break;
      case "fillText": pts.push([a[1], a[2], "text:" + a[0]]); break;
      case "fillRect": case "strokeRect": case "rect": case "roundRect":
        pts.push([a[0], a[1], c.op]); pts.push([a[0] + a[2], a[1] + a[3], c.op]); break;
      default: break;
    }
  });
  if (!pts.length) throw new Error(label + ": nothing was drawn");
  pts.forEach(([x, y, op]) => {
    if (!(x >= -m && x <= W + m && y >= -m && y <= H + m)) {
      throw new Error(label + ": " + op + " draws outside the " + W + "x" + H +
        " canvas at (" + Math.round(x) + ", " + Math.round(y) + ")");
    }
  });
  return pts.length;
}

trap("Tree geometry stays inside the canvas (both modes, every t)", () => {
  ["filtration", "condexp"].forEach(mode => {
    for (let t = 0; t <= 3; t++) {
      const canvases = withRecordedCanvas(() => {
        window.Tree.mount(makeEl("div"), { mode: mode, payoff: "call", K: 100, t: t });
      });
      assertInBounds(canvases[0], "Tree[" + mode + ", t=" + t + "]");
    }
  });
});

trap("Projection geometry stays inside the canvas (s = -12..12)", () => {
  for (let s = -12; s <= 12; s += 4) {
    const canvases = withRecordedCanvas(() => {
      window.Projection.mount(makeEl("div"), { mseMin: 83.217, s: s });
    });
    assertInBounds(canvases[0], "Projection[s=" + s + "]");
  }
});

trap("Tree.mount (filtration) + slide", () => {
  const el = makeEl("div");
  window.Tree.mount(el, { mode: "filtration", t: 1 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "2"; i.dispatch("input"); i.value = "3"; i.dispatch("input"); });
});

trap("Tree.mount (condexp, call payoff) + backward averaging values", () => {
  const el = makeEl("div");
  const w = window.Tree.mount(el, { mode: "condexp", payoff: "call", K: 100, t: 2 });
  const near = (a, b) => Math.abs(a - b) < 1e-9;
  if (!near(w.V[3][0], 33.100000000000009) && !near(w.V[3][0], 33.1)) throw new Error("leaf HHH payoff wrong: " + w.V[3][0]);
  if (!near(Math.round(w.V[2][0] * 1e6) / 1e6, 21)) throw new Error("E[V|F2] at HH should be 21, got " + w.V[2][0]);
  if (!near(Math.round(w.V[1][0] * 1e6) / 1e6, 12.725)) throw new Error("E[V|F1] at H should be 12.725, got " + w.V[1][0]);
  if (!near(Math.round(w.V[0][0] * 1e6) / 1e6, 7.475)) throw new Error("E[V] should be 7.475, got " + w.V[0][0]);
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "3"; i.dispatch("input"); });
});

trap("Tree.mount (condexp, price payoff) is a martingale under p = 0.5", () => {
  const el = makeEl("div");
  const w = window.Tree.mount(el, { mode: "condexp", payoff: "price", t: 1 });
  for (let level = 0; level <= 3; level++) {
    for (let i = 0; i < (1 << level); i++) {
      if (Math.abs(w.V[level][i] - w.S[level][i]) > 1e-9) {
        throw new Error("E[S3|Ft] != St at level " + level + " idx " + i);
      }
    }
  }
});

trap("Projection.mount + slide", () => {
  const el = makeEl("div");
  window.Projection.mount(el, { mseMin: 83.217, s: 7 });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "-12"; i.dispatch("input"); i.value = "12"; i.dispatch("input"); });
});

trap("BM paths geometry stays inside the canvas (every n)", () => {
  for (let k = 1; k <= 9; k++) {
    const canvases = withRecordedCanvas(() => {
      window.BM.mountPaths(makeEl("div"), { k: k });
    });
    assertInBounds(canvases[0], "BMpaths[k=" + k + "]");
  }
});

trap("BM qvar geometry stays inside the canvas (every m)", () => {
  for (let k = 1; k <= 9; k++) {
    const canvases = withRecordedCanvas(() => {
      window.BM.mountQVar(makeEl("div"), { k: k });
    });
    assertInBounds(canvases[0], "BMqvar[k=" + k + "]");
  }
});

trap("BM quadratic variation numbers (smooth -> 0, BM -> t)", () => {
  const el = makeEl("div");
  const w = window.BM.mountQVar(el, { k: 3 });
  const near = (a, b, tol) => Math.abs(a - b) < (tol || 1e-9);
  if (!near(w.qvSmooth(4), 0.25)) throw new Error("qvSmooth(4) should be 0.25, got " + w.qvSmooth(4));
  if (!near(w.qvSmooth(512), 1 / 512)) throw new Error("qvSmooth(512) wrong: " + w.qvSmooth(512));
  if (!near(w.qvBM(512), 1.0)) throw new Error("qvBM(512) should be exactly 1, got " + w.qvBM(512));
  if (!near(w.wFine[w.wFine.length - 1], -0.70710678, 1e-4)) throw new Error("W_1 endpoint drift: " + w.wFine[w.wFine.length - 1]);
  if (!(w.maxAbs > 1.2 && w.maxAbs < 1.35)) throw new Error("maxAbs drift: " + w.maxAbs);
  // BM's squared-increment sum stays O(1) at every mesh (never collapses toward 0 like the smooth curve)
  for (let k = 2; k <= 9; k++) {
    const q = w.qvBM(2 ** k);
    if (!(q > 0.6 && q < 1.7)) throw new Error("qvBM(" + (2 ** k) + ")=" + q + " out of the O(1) band");
    if (!(w.qvSmooth(2 ** k) < q)) throw new Error("smooth sum should stay below the BM sum at m=" + (2 ** k));
  }
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "1"; i.dispatch("input"); i.value = "9"; i.dispatch("input"); });
});

trap("BM.mountPaths + slide", () => {
  const el = makeEl("div");
  const w = window.BM.mountPaths(el, { k: 3 });
  if (!(w.wFine.length === 513 && w.wFine[0] === 0)) throw new Error("fine path should have 513 points starting at 0");
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "1"; i.dispatch("input"); i.value = "9"; i.dispatch("input"); });
});

trap("Ito drift geometry stays inside the canvas (every N)", () => {
  for (let k = 1; k <= 8; k++) {
    const canvases = withRecordedCanvas(() => {
      window.Ito.mountDrift(makeEl("div"), { k: k });
    });
    assertInBounds(canvases[0], "ItoDrift[k=" + k + "]");
  }
});

trap("Ito GBM geometry stays inside the canvas (every sigma)", () => {
  for (let s = 5; s <= 80; s += 5) {
    const canvases = withRecordedCanvas(() => {
      window.Ito.mountGBM(makeEl("div"), { sigmaPct: s });
    });
    assertInBounds(canvases[0], "ItoGBM[sigma=" + s + "]");
  }
});

trap("Ito drift numbers: E[W^2] -> t = 1, E[integral 2W dW] -> 0 (martingale)", () => {
  const el = makeEl("div");
  const w = window.Ito.mountDrift(el, { k: 8 });
  const N = w.NPATHS;
  // the whole rise of E[W^2] is the (dW)^2=dt drift; the Ito integral stays a martingale at 0
  if (!(Math.abs(w.meanW2(N) - 1.0) < 0.15)) throw new Error("meanW2(all) should be ~1 = t, got " + w.meanW2(N));
  if (!(Math.abs(w.meanIto(N)) < 0.15)) throw new Error("meanIto(all) should be ~0 (martingale), got " + w.meanIto(N));
  // decomposition: E[W^2] - E[∫2W dW] must equal the quadratic-variation drift (~t=1)
  if (!(Math.abs((w.meanW2(N) - w.meanIto(N)) - 1.0) < 0.05)) {
    throw new Error("E[W^2] - E[∫2W dW] should be the QV drift ~1, got " + (w.meanW2(N) - w.meanIto(N)));
  }
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "1"; i.dispatch("input"); i.value = "8"; i.dispatch("input"); });
});

trap("Ito GBM numbers: median drift = mu - 1/2 sigma^2 decreases with sigma; mean fixed", () => {
  const el = makeEl("div");
  const w = window.Ito.mountGBM(el, { sigmaPct: 20 });
  const near = (a, b) => Math.abs(a - b) < 1e-9;
  if (!near(w.meanRate, 0.10)) throw new Error("meanRate should be mu = 0.10, got " + w.meanRate);
  if (!near(w.medianRate(0.2), 0.10 - 0.5 * 0.04)) throw new Error("medianRate(0.2) wrong: " + w.medianRate(0.2));
  if (!near(w.drag(0.4), 0.08)) throw new Error("drag(0.4) should be 0.08, got " + w.drag(0.4));
  // median growth strictly falls as volatility rises (the whole point of the drag)
  let prev = 1e9;
  for (let s = 5; s <= 80; s += 5) {
    const r = w.medianRate(s / 100);
    if (!(r < prev)) throw new Error("median drift must decrease with sigma at sigma=" + s);
    prev = r;
  }
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "5"; i.dispatch("input"); i.value = "80"; i.dispatch("input"); });
});

trap("SDE OU geometry stays inside the canvas (every theta)", () => {
  for (let s = 5; s <= 100; s += 5) {
    const canvases = withRecordedCanvas(() => {
      window.SDE.mountOU(makeEl("div"), { theta: s / 10 });
    });
    assertInBounds(canvases[0], "SDEou[theta=" + (s / 10) + "]");
  }
});

trap("SDE explosion geometry stays inside the canvas (every x0)", () => {
  for (let s = 20; s <= 200; s += 10) {
    const canvases = withRecordedCanvas(() => {
      window.SDE.mountExplosion(makeEl("div"), { x0: s / 100 });
    });
    assertInBounds(canvases[0], "SDEexpl[x0=" + (s / 100) + "]");
  }
});

trap("SDE OU numbers: mean -> m, stationary std shrinks with theta, half-life = ln2/theta", () => {
  const el = makeEl("div");
  const w = window.SDE.mountOU(el, { theta: 2 });
  const near = (a, b, tol) => Math.abs(a - b) < (tol || 1e-9);
  // mean pulls from X0=80 toward m=100; at t=1 it sits strictly between the two
  if (!(w.endMean(2) > w.X0 && w.endMean(2) < w.m)) throw new Error("OU mean must sit between X0 and m, got " + w.endMean(2));
  // stronger pull => mean is closer to m by t=1, and the stationary band is tighter
  let prevMean = -1e9, prevStd = 1e9;
  for (let th = 0.5; th <= 10; th += 0.5) {
    const em = w.endMean(th), sd = w.statStd(th);
    if (!(em > prevMean)) throw new Error("endMean must increase toward m as theta grows at theta=" + th);
    if (!(sd < prevStd)) throw new Error("stationary std must decrease as theta grows at theta=" + th);
    if (!near(w.halfLife(th), Math.log(2) / th)) throw new Error("halfLife wrong at theta=" + th);
    prevMean = em; prevStd = sd;
  }
  // stationary variance identity sigma^2 / (2 theta) with sigma=10
  if (!near(w.statStd(2), Math.sqrt(100 / 4))) throw new Error("statStd(2) should be sqrt(sigma^2/2theta) = 2.5, got " + w.statStd(2));
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "5"; i.dispatch("input"); i.value = "100"; i.dispatch("input"); });
});

trap("SDE explosion numbers: blow-up time t* = 1/x0 decreases as x0 grows", () => {
  const el = makeEl("div");
  const w = window.SDE.mountExplosion(el, { x0: 0.8 });
  const near = (a, b) => Math.abs(a - b) < 1e-9;
  if (!near(w.blowupTime(0.5), 2.0)) throw new Error("blowupTime(0.5) should be 2, got " + w.blowupTime(0.5));
  if (!near(w.blowupTime(2.0), 0.5)) throw new Error("blowupTime(2.0) should be 0.5, got " + w.blowupTime(2.0));
  let prev = 1e9;
  for (let s = 20; s <= 200; s += 10) {
    const ts = w.blowupTime(s / 100);
    if (!(ts < prev)) throw new Error("blow-up time must decrease as x0 grows at x0=" + (s / 100));
    prev = ts;
  }
  // the linear-growth solution stays finite over the whole window
  if (!(w.linearAt(2.0, w.T) < 1e3)) throw new Error("linear-growth drift must stay finite over [0,T]");
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "20"; i.dispatch("input"); i.value = "200"; i.dispatch("input"); });
});

trap("RN replication geometry stays inside the canvas (every p)", () => {
  for (let p = 0; p <= 100; p += 5) {
    const canvases = withRecordedCanvas(() => {
      window.RN.mountReplication(makeEl("div"), { p: p / 100 });
    });
    assertInBounds(canvases[0], "RNrep[p=" + (p / 100) + "]");
  }
});

trap("RN Girsanov-weights geometry stays inside the canvas (every mu)", () => {
  for (let m = 0; m <= 20; m += 2) {
    const canvases = withRecordedCanvas(() => {
      window.RN.mountWeights(makeEl("div"), { mu: m / 100 });
    });
    assertInBounds(canvases[0], "RNweights[mu=" + (m / 100) + "]");
  }
});

trap("RN convergence geometry stays inside the canvas (every n)", () => {
  for (let n = 1; n <= 120; n += 7) {
    const canvases = withRecordedCanvas(() => {
      window.RN.mountConvergence(makeEl("div"), { n: n });
    });
    assertInBounds(canvases[0], "RNconv[n=" + n + "]");
  }
});

trap("RN replication numbers: the price is 5 for EVERY p; only p* agrees with the average", () => {
  const el = makeEl("div");
  const w = window.RN.mountReplication(el, { p: 0.7 });
  const near = (a, b, tol) => Math.abs(a - b) < (tol || 1e-9);
  if (!near(w.delta, 0.5)) throw new Error("hedge ratio should be (10-0)/(110-90) = 0.5, got " + w.delta);
  if (!near(w.bond, -45)) throw new Error("cash leg should be -45 (borrow), got " + w.bond);
  if (!near(w.price, 5)) throw new Error("replication cost should be 5, got " + w.price);
  if (!near(w.pStar, 0.5)) throw new Error("p* = (1-0.9)/(1.1-0.9) = 0.5, got " + w.pStar);
  // the forecast-based price moves with p, the replication price does not
  if (!near(w.expPrice(w.pStar), w.price)) throw new Error("expPrice(p*) must equal the replication price");
  if (!near(w.expPrice(0.7), 7)) throw new Error("expPrice(0.7) should be 7, got " + w.expPrice(0.7));
  let prev = -1e9;
  for (let p = 0; p <= 1.0001; p += 0.05) {
    const e = w.expPrice(p);
    if (!(e > prev)) throw new Error("expected-payoff price must rise with p at p=" + p);
    prev = e;
  }
  // with 2% interest the risk-neutral weight moves to 0.6 though beliefs never changed
  const w2 = window.RN.mountReplication(makeEl("div"), { R: 1.02 });
  if (!near(w2.pStar, 0.6, 1e-9)) throw new Error("p* at R=1.02 should be 0.6, got " + w2.pStar);
  if (!near(w2.price, 6 / 1.02, 1e-9)) throw new Error("price at R=1.02 should be 6/1.02, got " + w2.price);
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "100"; i.dispatch("input"); });
});

trap("RN Girsanov numbers: theta = (mu-r)/sigma; the weighted mean sits on S0 e^{rt} for every mu", () => {
  const el = makeEl("div");
  const w = window.RN.mountWeights(el, { mu: 0.15 });
  const near = (a, b, tol) => Math.abs(a - b) < (tol || 1e-9);
  if (!near(w.theta(0.15), 0.5)) throw new Error("theta(0.15) should be (0.15-0.05)/0.2 = 0.5, got " + w.theta(0.15));
  if (!near(w.theta(0.05), 0)) throw new Error("a stock earning r needs no shift: theta(r) = 0");
  // re-weighting moves the average onto the cash-rate curve, at EVERY time and every mu
  for (let m = 0; m <= 20; m += 2) {
    const mu = m / 100;
    if (!near(w.meanP(mu), w.S0 * Math.exp(mu * w.T), 1e-9)) throw new Error("P-mean must be S0 e^{mu T} at mu=" + mu);
    for (let i = 0; i <= w.NSTEPS; i += 10) {
      const t = i / w.NSTEPS * w.T;
      const target = w.S0 * Math.exp(w.r * t);
      if (!near(w.weightedMeanAt(mu, i), target, 0.25)) {
        throw new Error("Q-weighted mean must track S0 e^{rt} (mu=" + mu + ", t=" + t.toFixed(2) +
          "): got " + w.weightedMeanAt(mu, i).toFixed(3) + " vs " + target.toFixed(3));
      }
    }
  }
  // higher mu ⇒ bigger shift ⇒ a path that ended HIGH is discounted harder under Q
  let prevW = 1e9;
  for (let m = 0; m <= 20; m += 2) {
    const wt = w.weightOf(1.0, m / 100);
    if (!(wt < prevW)) throw new Error("weight of an up-path must fall as mu (hence theta) grows at mu=" + (m / 100));
    prevW = wt;
  }
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "20"; i.dispatch("input"); });
});

trap("RN convergence numbers: CRR tree -> Black-Scholes 10.4506 as n grows", () => {
  const el = makeEl("div");
  const w = window.RN.mountConvergence(el, { n: 8 });
  const near = (a, b, tol) => Math.abs(a - b) < (tol || 1e-9);
  // the closed form for S=K=100, r=5%, sigma=20%, T=1 (d1 = 0.35, d2 = 0.15)
  if (!near(w.d1, 0.35, 1e-12)) throw new Error("d1 should be 0.35, got " + w.d1);
  if (!near(w.d2, 0.15, 1e-12)) throw new Error("d2 should be 0.15, got " + w.d2);
  if (!near(w.bs, 10.4506, 1e-3)) throw new Error("Black-Scholes price should be ~10.4506, got " + w.bs);
  if (!near(window.RN._normCdf(0), 0.5, 1e-8)) throw new Error("normCdf(0) must be 0.5");
  if (!near(window.RN._normCdf(1.96), 0.9750021, 1e-6)) throw new Error("normCdf(1.96) must be ~0.9750021");
  // a one-step tree is a crude caricature; a fine tree is not
  if (!(Math.abs(w.binom(1) - w.bs) > 1) ) throw new Error("a 1-step tree should be far from BS");
  if (!(Math.abs(w.binom(400) - w.bs) < 0.02)) throw new Error("a 400-step tree should be within 0.02 of BS, got " + w.binom(400));
  // convergence: same-parity step counts close in monotonically (the odd/even zig-zag)
  [1, 2].forEach(parity => {
    let prevGap = 1e9;
    for (let n = 8 + parity; n <= 120; n += 2) {
      const gap = Math.abs(w.binom(n) - w.bs);
      if (!(gap < prevGap)) throw new Error("gap to BS must shrink along parity " + parity + " at n=" + n);
      prevGap = gap;
    }
  });
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "1"; i.dispatch("input"); i.value = "120"; i.dispatch("input"); });
});

trap("BS hedge geometry stays inside the canvas (every delta)", () => {
  for (let d = 0; d <= 120; d += 10) {
    const canvases = withRecordedCanvas(() => {
      window.BS.mountHedge(makeEl("div"), { delta: d / 100 });
    });
    assertInBounds(canvases[0], "BShedge[delta=" + (d / 100) + "]");
  }
});

trap("BS backward geometry stays inside the canvas (every tau)", () => {
  for (let t = 0; t <= 100; t += 10) {
    const canvases = withRecordedCanvas(() => {
      window.BS.mountBackward(makeEl("div"), { tau: t / 100 });
    });
    assertInBounds(canvases[0], "BSback[tau=" + (t / 100) + "]");
  }
});

trap("BS Feynman-Kac geometry stays inside the canvas (every n)", () => {
  for (let n = 10; n <= 800; n += 70) {
    const canvases = withRecordedCanvas(() => {
      window.BS.mountFK(makeEl("div"), { n: n });
    });
    assertInBounds(canvases[0], "BSfk[n=" + n + "]");
  }
});

trap("BS hedge numbers: residual std is smallest near N(d1) = 0.6368", () => {
  const el = makeEl("div");
  const w = window.BS.mountHedge(el, { delta: 0.64 });
  const near = (a, b, tol) => Math.abs(a - b) < (tol || 1e-3);
  if (!near(w.trueDelta, 0.6368, 5e-4)) throw new Error("trueDelta should be N(0.35) ≈ 0.6368, got " + w.trueDelta);
  if (!near(w.call, 10.4506, 1e-3)) throw new Error("ATM 1y call should be ~10.4506, got " + w.call);
  const atTrue = w.residualStd(w.trueDelta);
  const atLow = w.residualStd(0.30);
  const atHigh = w.residualStd(1.00);
  if (!(atTrue < atLow)) throw new Error("residualStd at true delta must beat 0.30: " + atTrue + " vs " + atLow);
  if (!(atTrue < atHigh)) throw new Error("residualStd at true delta must beat 1.00: " + atTrue + " vs " + atHigh);
  // a coarse scan: the minimum on a 0.05 grid sits at 0.65 (nearest to 0.6368)
  let bestD = -1, bestSd = 1e9;
  for (let d = 0; d <= 1.2001; d += 0.05) {
    const sd = w.residualStd(d);
    if (sd < bestSd) { bestSd = sd; bestD = d; }
  }
  if (Math.abs(bestD - 0.65) > 1e-9) throw new Error("min residualStd on 0.05-grid should be at 0.65, got " + bestD);
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "120"; i.dispatch("input"); });
});

trap("BS backward numbers: hockey-stick at tau=0, 10.4506 at tau=1, time value >= 0", () => {
  const el = makeEl("div");
  const w = window.BS.mountBackward(el, { tau: 1 });
  const near = (a, b, tol) => Math.abs(a - b) < (tol || 1e-9);
  if (!near(w.value(0, 100), 0)) throw new Error("payoff ATM is 0, got " + w.value(0, 100));
  if (!near(w.value(0, 120), 20)) throw new Error("payoff at 120 is 20, got " + w.value(0, 120));
  if (!near(w.value(1, 100), 10.4506, 1e-3)) throw new Error("one-year ATM call should be ~10.4506, got " + w.value(1, 100));
  if (!near(w.d1, 0.35, 1e-12)) throw new Error("d1 should be 0.35, got " + w.d1);
  if (!near(w.d2, 0.15, 1e-12)) throw new Error("d2 should be 0.15, got " + w.d2);
  // European call with r >= 0 sits above its payoff
  for (const s of [60, 80, 100, 120, 150]) {
    for (const tau of [0, 0.25, 0.5, 1]) {
      if (w.value(tau, s) + 1e-9 < w.payoff(s)) {
        throw new Error("C(tau,s) must be >= payoff at s=" + s + " tau=" + tau);
      }
    }
  }
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "0"; i.dispatch("input"); i.value = "100"; i.dispatch("input"); });
});

trap("BS Feynman-Kac numbers: MC dots approach the PDE solution 10.4506", () => {
  const el = makeEl("div");
  const w = window.BS.mountFK(el, { n: 80 });
  const near = (a, b, tol) => Math.abs(a - b) < (tol || 1e-9);
  if (!near(w.bs, 10.4506, 1e-3)) throw new Error("bs should be ~10.4506, got " + w.bs);
  if (!near(w.bsAt(100), w.bs, 1e-12)) throw new Error("bsAt(100) must equal bs");
  if (!near(w.bsAt(120), window.BS._bsCall(120, 100, 0.05, 0.20, 1), 1e-12)) {
    throw new Error("bsAt(120) must match the closed form");
  }
  if (!(Math.abs(w.mcAt(100, 800) - w.bs) < 0.02)) {
    throw new Error("800-node quadrature at S=100 should be within 0.02 of BS, got " + w.mcAt(100, 800));
  }
  // finer strata, smaller gap (deterministic inverse-CDF quadrature)
  if (!(Math.abs(w.mcAt(100, 800) - w.bs) < Math.abs(w.mcAt(100, 20) - w.bs))) {
    throw new Error("gap to BS should shrink from n=20 to n=800");
  }
  function inputs(node, acc) { (node.children || []).forEach(c => { if (c.tagName === "input") acc.push(c); inputs(c, acc); }); return acc; }
  inputs(el, []).forEach(i => { i.value = "10"; i.dispatch("input"); i.value = "800"; i.dispatch("input"); });
});

console.log(ok ? "\nALL WIDGETS OK" : "\nSMOKE FAILED");
process.exit(ok ? 0 : 1);
