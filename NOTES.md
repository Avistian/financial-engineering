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
- **Plain language first (2026-07-27).** See standing decision below — terms and concepts must be
  explained in simple everyday words before any jargon or formula sticks.

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

## Standing decision — explain everything introduced, in full (from 2026-07-17, Lesson 006 on)
- **Thoroughness overrides brevity.** Every term, symbol, formula, or method a lesson *introduces* must be
  fully explained on the spot — defined in words, motivated, and shown with a worked numeric example — even
  if it makes the lesson longer. No naked jargon, no "see later," no symbol used before it is defined.
- The learner explicitly prefers **longer, self-contained lessons** to terse ones: it is better to run past
  the ~30 KB / ~60 min guideline than to leave anything introduced under-explained. Treat the size band in
  the skills as a floor for depth, not a ceiling on it.
- Applies to **all future lessons**, not just 006. Encoded in `.agents/skills/lesson-pedagogy/SKILL.md`
  ("Explain everything you introduce").

## Standing decision — pace for a struggling learner; depth over length (from 2026-07-23)
- **The learner finds quant hard at the current pace and wants even better explanations, explicitly
  accepting longer lessons as the cost.** This *strengthens* the 2026-07-17 "explain everything"
  decision: the size band is now firmly a floor, not a target — never trade clarity for brevity.
- **The four levers the learner asked for (apply to every lesson, hardest on math-heavy units):**
  1. **Intuition before symbols.** Open each concept with a plain-English picture / analogy / the
     problem it solves. No symbol appears before the reader already has the mental image it names.
  2. **Smaller steps.** One new idea per beat. Never stack two hard concepts in a single paragraph;
     split a dense idea into several short sub-steps, each with its own mini-takeaway.
  3. **Re-warm the prerequisite inline.** Do NOT assume prior undergrad math/prob (or an earlier
     lesson) is fresh. Before using a building block, recall it in a sentence or two (+ link to where
     it was taught) so the learner never hits an unexplained dependency.
  4. **A "slow lane" for derivations.** For any multi-line derivation, show *every* algebra step and
     annotate *why* each step is legal (what rule/assumption licenses it). No "it can be shown that."
- **Where it bites most:** the math-heavy lessons. The learner named **008 (linear algebra/PCA)** and
  **009 (regression)** as the hardest. Q2 (011–020: measure theory → Brownian motion → Itô → SDEs →
  pricing) is the densest math yet — treat it as the primary test of this decision: slower ramp, more
  scaffolding, a geometric/probabilistic picture for every abstraction, and a worked slow-lane
  derivation for Itô's lemma, the BS PDE, etc.
- **Retrieval unchanged in rigor.** Easier *exposition* does not mean easier *retrieval* — keep the
  warm-ups, predict-before-reveal, teach-backs and quizzes as effortful as ever (desirable difficulty
  is the point). We slow the teaching, not the testing.
- Encoded in `.agents/skills/lesson-pedagogy/SKILL.md` ("Pace for understanding"). Applies to all
  future lessons.

## Standing decision — plain language for every term (from 2026-07-27)
- **Feedback:** even with the "explain everything" and "pace for understanding" decisions in place,
  the learner still finds the **language and concepts unclear**. Thoroughness alone is not enough
  if the prose stays in specialist register.
- **Rule for all future lessons, labs, memos, and tutor answers:** write as if explaining to a
  strong programmer with **near-zero finance vocabulary**. Every load-bearing word gets a simple
  definition *in the same breath it appears* — not a later glossary dump, not "as we saw," not a
  circular definition that uses other jargon.
- **Litmus test (must pass before a section ships):** could the learner answer *"what does this
  word literally mean here?"* after one short plain sentence, without needing markets experience?
  If the answer is no, rewrite. Examples of words that failed this recently: *book*, *the market*,
  *neutralize*, *exposure*, *alpha*, *beta*, *PC1 as portfolio weights*.
- **How to write a term the first time it appears:**
  1. Everyday picture in one sentence ("the book = the portfolio of positions you hold right now").
  2. Then the standard name, if useful ("traders call that your book").
  3. Then, only if needed, the symbol / formula.
  4. One tiny numeric or concrete example before moving on.
- **Forbidden shortcuts:** assuming the reader half-knows a term; defining jargon with more jargon;
  using a word in a finance-specific sense without flagging that the everyday meaning differs
  (*book*, *security*, *option*, *hedge*, *signal*).
- **Does not weaken rigor.** Quizzes, teach-backs, and CHECK cells stay hard. Only the *way in*
  gets simpler.
- Encoded in `.agents/skills/lesson-pedagogy/SKILL.md` ("Plain language for every term") and
  `.cursor/rules/lesson-plain-language.mdc`. Applies to **all future lessons** (and to tutor chat
  when teaching from this curriculum).

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
- **Length A/B — ask the learner directly.** Lesson 011 was ~70 KB (four-layer build); Lesson 012 was
  deliberately leaner at ~49 KB / 15 `<h2>` (one idea per beat, no repeated scaffold). Ask which felt
  better in one sitting and record it — this is the real datapoint to calibrate units 013–020 on, not my
  assumption. (Depth-over-length still stands; the question is only how much per lesson.)
- **`(dW)² = dt` must be automatic before Lesson 013.** Itô's lemma is just this substitution inside a
  Taylor expansion. Grade the 012 teach-back for *why* `(dW)²` survives while `dW·dt` and `(dt)²` are
  dropped. Also watch for the two-variances confusion (`Var(W_t)=t` across paths vs `[W]_t=t` per path).
- **Glossary drill owed:** rows for 006–012 are all still blank (32 terms). Do one cold-definition pass
  and fill only what the learner defines unaided.
- Lesson 010 was **self-reported** as passed (no EXIT TICKET graded here) — offer a fresh checkpoint
  scenario at the next natural break.
