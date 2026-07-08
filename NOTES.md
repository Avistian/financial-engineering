# Notes — preferences & working scratchpad

## Learner profile (from intake interview, 2026-07-06)
- **Target role:** Quant Researcher / systematic alpha (buy-side). Not primarily QT or QD.
- **Math:** solid undergrad (calculus, linear algebra, basic probability). **No** measure theory or SDEs yet — Year 1 Q2 is the bridge, don't assume it.
- **Programming:** strong — Python + C++/Rust, data structures, systems. Labs can move fast on code; the learning is in the *finance/stats*, not the syntax.
- **Finance:** near zero. Year 1 Q1 builds markets vocabulary from scratch; never assume prior market knowledge.
- **Time:** ~1.5–2 h/day, sustained, ~3-year horizon.
- **Lab stack:** Python-first (numpy/pandas/scikit-learn/statsmodels/PyTorch). C++/Rust only in the Year-3 systems-awareness track.

## Teaching preferences
- **Failure-mode first.** Every method is taught *with the way it breaks* (leakage, overfitting, non-stationarity). The `.trap` box in lessons is mandatory, not decorative.
- Keep working memory small: one skill per lesson; peripheral boilerplate is PROVIDED in labs.
- Cite sources inline (link to RESOURCES.md entries). No parametric hand-waving on the moving parts (TFMs, deep LOB, RL).
- Quiz answers must be equal length (words/chars) so formatting leaks no hint.
- Be strict at checkpoints: no advancing past a failed exit criterion.

## Lesson authoring patterns (adopted from the `relational` workspace, 2026-07-08)
- Lessons should be **long and substantial (~22–30 KB, target ~55–60 min)** — the learner prefers
  more text to learn efficiently in one sitting, not terse skeletons. Every conceptual beat gets full
  prose, not a one-line table row: multiple worked numeric examples, several deep-dive subsections per
  major idea, a "Common questions (and honest answers)" `<dl class="objections">`, a no-peek `.reflect`
  block, active reading instructions, and a "Where you are in the arc" closer.
- Depth checklist per lesson: (1) motivate the idea, (2) develop it with prose + a worked example,
  (3) show at least one *second-order* consequence or subtlety, (4) name the failure mode (`.trap`),
  (5) connect it forward to where it's used later in the curriculum. Aim for 8–12 `<h2>` sections.
- Every lesson from 002 on opens with a spaced-retrieval **warm-up** (`retrieval-bank.js` +
  `retrieval-pool.js`, `upTo` = lesson number) drawing only from earlier lessons.
- One **predict-before-reveal** (`predict.js`) on a non-obvious result, placed above the reveal.
- One **teach-back** (`teachback.js`) on the load-bearing idea.
- The two authoring skills encode this: `.agents/skills/lesson-pedagogy` and `lesson-visuals`.
- Feed `assets/retrieval-pool.js` (stable ids, never renumber) whenever a lesson ships a durable idea.

## Standing weekly habits (don't let these lapse)
- 10 mental-math drills + 5 probability brainteasers/week (Green Book / Heard on the Street).
- 3–5 LeetCode problems/week from Year 1 (rotating arrays → DP → graphs → trees).
- After each math/pricing unit, add one derivation to "Derivations I own" below.

## Derivations I own (interview-ready, from memory)
- _(empty — add Itô's lemma, Black-Scholes PDE, Girsanov, OU solution, etc. as you master them)_

## Optional (◆) paper notes — "when it wins / when it breaks"
- _(one paragraph per ◆ paper as you skim it)_

## Open questions / parking lot
- Secure real LOB data (LOBSTER / Databento / FI-2010) before Year 2 Q3.
- Decide on a compute setup for PyTorch labs (units 073–080) — local GPU vs Colab/cloud.
