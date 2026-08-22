# Lesson 016 published — The Black–Scholes PDE & Feynman–Kac (Q2 continues)

Learner marked **Lesson 015 done** (2026-08-22) and asked for Lesson 016. Shipped
**Lesson 016 — "The Black–Scholes PDE & Feynman–Kac"**
(`lessons/0016-black-scholes-pde-feynman-kac.html`) and its lab
(`labs/0016-black-scholes-pde.ipynb`, 7 tasks). This is **Unit 016**, the sixth unit of
**Year 1 Q2**, the curriculum's designated topic "The Black-Scholes PDE & Feynman-Kac:
PDEs ↔ expectations," primary source **Shreve II Ch. 6** (§6.2–6.4). Lab brief matched
exactly: "Derive BS PDE; state Feynman-Kac."

No cold 015 teach-back was graded this session. The three 015 derivations (replication,
`p*`, `θ = (μ−r)/σ`) and the `P`/`Q` probe remain owed before they go into
"Derivations I own."

## The one skill, and the order it is built in
Load-bearing idea: **the PDE and today's expectation are the same object.** The lesson
refuses to state Feynman–Kac until the learner has seen the hedge kill `dW` and
no-arbitrage force the leftover to earn `r`, so the chain is:

1. Re-warm Itô on a surface `V(t, s)` — time slope (theta), space slope (delta),
   curvature (gamma). Under `Q`, `dS = rS dt + σS dW̃`.
2. **Kill the noise.** Book `Π = V − V_s S`. The `σS V_s dW̃` terms cancel. Leftover
   is `(V_t + ½σ²S² V_ss) dt` — a riskless trickle.
3. **No free lunch.** `dΠ = r Π dt` rearranges to the Black–Scholes PDE
   `V_t + rS V_s + ½σ²S² V_ss − rV = 0`.
4. **Four-term budget** at the running point `(0, 100)`:
   `−6.414 + 3.184 + 3.752 − 0.523 = 0`. Same numbers as 015's `10.4506` call.
5. **`μ` never appears** — it cancels in the hedge, the continuous-time face of
   "p never entered the two replication equations." Damaged residual
   `(μ−r)S V_s = +6.368`.
6. **Terminal condition** `V(T,s) = (s−K)⁺` is a finish line, not a start. Edges
   `V(t,0)=0` and `V ≈ s − Ke^{-r(T-t)}` for large `s`.
7. **Feynman–Kac:** this PDE + that payoff **is**
   `E_Q[e^{-r(T-t)}(S_T−K)⁺ | S_t = s]`. Two machines, one number.
8. The closed form solves the PDE because it *is* that expectation. Heat-equation
   transformation is the second-order reason `N(d₁)` appears.
9. What the PDE cannot do: American free boundary, jumps / stochastic vol
   (incompleteness from 015), discrete hedging (017).

Pacing devices per the 2026-08-13 standing decision: **`.plain` notes and `.numplay`
boxes** on every load-bearing equation; every derivation in the slow lane with each
step's licence stated. The first 016 draft was too short; the learner pointed at
Lessons 013–015 as the detail template. The rewrite adds an hour map, the hedge
algebra with every cancellation written out (014-style), a four-step Feynman–Kac
proof (ride the surface → PDE kills the sure pile → martingale), the heat-equation
clock-flip with the four-term budget, and a put as worked example 2 (same PDE,
parity as the sanity check).

## Failure-mode-first
Six traps: `μ` in the PDE; dropping `½σ²S²V_ss` (ordinary calculus, residual
`−3.752`); payoff as a starting condition; dropping `−rV` (residual `+0.523`);
reading the PDE as a forecast; European solver on an American ticket.

## Three visualizations, one per distinct mechanism (per `lesson-visuals`)
Delivered as one reusable asset `assets/bspde-viz.js` (`global.BS`):
- **`BS.mountHedge`** — slider is the chosen `Δ`. P&L paths of a one-month
  constant-mix book collapse only at `Δ = N(d₁) ≈ 0.637`.
- **`BS.mountBackward`** — slider is time-to-expiry. Hockey-stick at `τ=0`
  smooths into the price curve; ATM 1y is `10.45`.
- **`BS.mountFK`** — green curve is the PDE solution; red dots are a seeded
  Monte-Carlo of the discounted payoff. Slider = path count. The landing
  *is* Feynman–Kac.

## Verification
`.smoke.js` extended to **39 checks** (from 33): `bspde-viz.js` added to the eval list plus six traps —
geometry in bounds at every slider position for all three widgets, and numeric checks: hedge
`trueDelta ≈ 0.6368` with residual std minimized on a 0.05-grid at `0.65`; backward
`value(0,100)=0`, `value(0,120)=20`, `value(1,100)≈10.4506`, European call above payoff;
FK `bs=10.4506`, stratified quadrature `|mc(800)−bs|<0.02` and the gap shrinking from `n=20`
to `n=800`. **All 39 pass.** The filled solution executed cell-by-cell in the venv: **all 7 CHECK
groups + EXIT ticket pass** — Itô drift of `V` equals `rV = 0.5225`; PDE residual machine-zero
on a 3×3 grid; damaged residuals `μ`-in `+6.368`, no-gamma `−3.752`, no-fund `+0.523`;
antithetic MC under `Q` **10.5428** (gap `+0.092`); one-step CRR node recovers today's price
to `8e-6`. Student `.ipynb` rendered to `labs/html/0016-black-scholes-pde.html`.

## Wiring
manifest → **v13** (lesson 16, `year 1 / quarter 2`, `labPath` set);
`index.html` / `notebooks.html` version meta bumped to 13 and the Feynman–Kac
cheat sheet added to the Reference nav; Lesson 015's forward-nav now points at
Lesson 016; **five** `retrieval-pool.js` items added (`l016-pde-r-not-mu`
[misconception], `l016-ito-curvature`, `l016-feynman-kac`, `l016-terminal`
[misconception], `l016-residual`) — 67 items total; eight `GLOSSARY.md` rows;
`labs/README.md` index entry; `RESOURCES.md` gained the unit-016 pointer into
Shreve II Ch. 6. New reference sheet `reference/feynman-kac.html`. Builder kept
as `scripts/_gen_lab_0016.py`.

## Watch-points for next sessions
1. **Grade the PDE cold.** Ask the learner to derive
   `V_t + rS V_s + ½σ²S² V_ss − rV = 0` from the hedge, unaided, and to say why
   `μ` cancels. Then one sentence of Feynman–Kac. All three ⇒ "the Black–Scholes
   PDE" and "Feynman–Kac" go into "Derivations I own."
2. **The four-term budget should become automatic.**
   `−6.414 + 3.184 + 3.752 − 0.523 = 0`, and each damaged residual names the
   missing term.
3. **015 teach-backs are still owed.** Replication / `p*` / `θ`, and the
   "is 56% a forecast?" probe.
4. **017 arrives next with a real, discrete hedge.** Preview already in the
   hedge widget: even at the right `Δ`, a frozen mix leaves a gamma band.
5. **Glossary drill still owed** (006–016). Lesson 010 still self-reported.
