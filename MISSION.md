# Mission: Quantitative Research (Systematic Trading)

## Why
Land — and thrive in — a **Quantitative Researcher** role at a top systematic trading firm
(Two Sigma, DE Shaw, Cubist, Citadel/GQS, Jane Street QR, HRT, and peers). Not "learn about
quant finance" in the abstract: reach the level where you can independently take a raw idea →
data → validated signal → capacity-aware strategy → a defense that survives a skeptical PM and
a leakage/overfitting audit. The whole plan is built so that when you claim an edge, you know
exactly what you are standing on.

## Success looks like
- Turn a market hypothesis into a **backtest that survives CPCV, PBO, and a deflated Sharpe ratio** — not a data-mined mirage.
- Derive and price a European option **three independent ways** (closed form, Monte Carlo, PDE) and explain Girsanov / Feynman-Kac without hand-waving.
- Build the full **López de Prado pipeline** end to end: information-driven bars → fractional differentiation → triple-barrier + meta-labeling → sample-weighted, leakage-free model.
- Reproduce a **microstructure result** (OFI→impact, a Hawkes intensity, a DeepLOB-style predictor) with correct temporal splits and honest limitations.
- Construct a **denoised, cost-aware portfolio** (RMT / Ledoit-Wolf) from multiple signals and report net Sharpe and capacity; stress joint losses with **copulas**, not just linear correlation.
- **Pass the interview gauntlet**: mental math, probability/market-making games, stochastic-calculus derivations, and LeetCode-style DP/graphs under pressure.
- Ship a **Year-3 capstone**: an end-to-end research project presented as if defending it to a portfolio manager.
- Ship a **Year-4 exit** (after the offer-level track): a point-in-time **store** plus a walk-forward monthly **long-only** book through a constrained optimizer. The full PM defense of that book is Year 5 Q1 (unit 170). Plain-language map: [reference/long-only-mid-horizon.html](./reference/long-only-mid-horizon.html). Teaching plan: [reference/year-4-lessons.html](./reference/year-4-lessons.html).
- Ship a **Year-5 exit**: defend the monthly book, then the same long-only + ML + optimizer job on an **hours-to-days** clock through an ADV-capped optimizer. The full daily PM defense is Year 6 Q1 (unit 210). Plain-language map: [reference/long-only-mid-frequency.html](./reference/long-only-mid-frequency.html). Teaching plan: [reference/year-5-lessons.html](./reference/year-5-lessons.html).
- Ship a **Year-6 capstone**: defend the daily book, then twenty paper or tiny-live days with a reconciled ledger, a kill-switch test, and no silent as-of break. Teaching plan: [reference/year-6-lessons.html](./reference/year-6-lessons.html).

## Constraints
- **Pace:** ~1.5–2 hours/day, sustained, over **~6 years** (~4,000 hours). Years 1–3 are the original ~2,000-hour QR track (unchanged). **Years 4–6 are extra calendar**, not a swap. Unit numbers match study order: data kit (121–130), monthly long-only book, daily long-only book, then paper and a tiny live desk. Higher daily intensity than a 1h/day plan; extra time on strong days goes to labs/reproduction, never to skipping exit criteria. See [CURRICULUM.md](./CURRICULUM.md). Do not skip to Year 4, 5, or 6 from Year 1 — the validation, impact, and portfolio math live in Years 2–3. Labs for units 121–240 are not written yet; the teaching plans say what each lesson must teach.
- **Starting point:** solid undergrad math (calculus, linear algebra, basic probability) but **no measure theory / SDEs**; **strong programmer** (Python + C++/Rust, data structures, systems); **little to no finance/markets** knowledge. Year 1 therefore rebuilds markets from zero and bridges into stochastic calculus, while labs move fast because you can code.
- **Stack:** Python-first for all research/ML/backtesting labs. C++/Rust appear only in the Year-3 low-latency *systems-awareness* track — enough to speak the language and reason about latency, not to become an HFT core dev.
- Ground every claim in high-trust sources ([RESOURCES.md](./RESOURCES.md)) and reproducible experiments. A unit is "done" only when its lab runs and its quiz/checkpoint passes.

## Out of scope (for now)
- Becoming a low-latency HFT **core** developer (kernel-bypass tuning as a day job). Covered at *awareness* depth only.
- Discretionary/fundamental investing, macro punditry, and get-rich-quick retail trading content.
- Chasing every new arXiv preprint. A paper earns a slot only if it set SOTA, exposed a real failure mode, or is a baseline you must beat.
- Crypto-specific market plumbing and exchange-connectivity engineering, unless a lab needs it.
