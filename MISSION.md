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
- Construct a **denoised, cost-aware portfolio** (RMT / Ledoit-Wolf) from multiple signals and report net Sharpe and capacity.
- **Pass the interview gauntlet**: mental math, probability/market-making games, stochastic-calculus derivations, and LeetCode-style DP/graphs under pressure.
- Ship a **capstone**: an end-to-end research project presented as if defending it to a portfolio manager.

## Constraints
- **Pace:** ~1.5–2 hours/day, sustained, over **~3 years** (~2,000 hours). Higher daily intensity than a 1h/day plan; extra time on strong days goes to labs/reproduction, never to skipping exit criteria. See [CURRICULUM.md](./CURRICULUM.md).
- **Starting point:** solid undergrad math (calculus, linear algebra, basic probability) but **no measure theory / SDEs**; **strong programmer** (Python + C++/Rust, data structures, systems); **little to no finance/markets** knowledge. Year 1 therefore rebuilds markets from zero and bridges into stochastic calculus, while labs move fast because you can code.
- **Stack:** Python-first for all research/ML/backtesting labs. C++/Rust appear only in the Year-3 low-latency *systems-awareness* track — enough to speak the language and reason about latency, not to become an HFT core dev.
- Ground every claim in high-trust sources ([RESOURCES.md](./RESOURCES.md)) and reproducible experiments. A unit is "done" only when its lab runs and its quiz/checkpoint passes.

## Out of scope (for now)
- Becoming a low-latency HFT **core** developer (kernel-bypass tuning as a day job). Covered at *awareness* depth only.
- Discretionary/fundamental investing, macro punditry, and get-rich-quick retail trading content.
- Chasing every new arXiv preprint. A paper earns a slot only if it set SOTA, exposed a real failure mode, or is a baseline you must beat.
- Crypto-specific market plumbing and exchange-connectivity engineering, unless a lab needs it.
