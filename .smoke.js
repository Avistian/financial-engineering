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

console.log(ok ? "\nALL WIDGETS OK" : "\nSMOKE FAILED");
process.exit(ok ? 0 : 1);
