# Notes — preferences & working scratchpad

## Learner profile (from intake interview, 2026-07-06)
- **Target role:** Quant Researcher / systematic alpha (buy-side). Not primarily QT or QD.
- **Math:** solid undergrad (calculus, linear algebra, basic probability). **No** measure theory or SDEs yet — Year 1 Q2 is the bridge, don't assume it.
- **Programming:** strong — Python + C++/Rust, data structures, systems. Labs can move fast on code; the learning is in the *finance/stats*, not the syntax.
- **Finance:** near zero. Year 1 Q1 builds markets vocabulary from scratch; never assume prior market knowledge.
- **Time:** ~1.5–2 h/day, sustained, **~6-year horizon** (Years 1–3 original QR track + Year 4 store and monthly long-only book + Year 5 defend monthly / daily research + Year 6 defend daily / go live).
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

## Standing decision — "even more basic" (still in math terms) (from 2026-08-13)
- **Feedback:** the learner had difficulty understanding Lessons 012 and 013 and asked to make lessons
  "even more basic (still in math terms though)." So this is *not* a request to drop the math — it is a
  request for the math to be **grounded harder** before it is used. Clarity, not length, is the lever.
- **Two required devices on every math-heavy lesson (retro-fit where the learner revisits):**
  1. **In-plain-words note (`.plain`, tagged "In plain words")** right after every load-bearing equation —
     the equation restated as one plain sentence, symbol by symbol, no new notation. (The learner disliked
     the earlier "say it aloud" framing — 2026-08-13 — so the label reads "In plain words," not "aloud.")
  2. **With-real-numbers box (`.numplay`)** — plug in actual small numbers and compute a step by hand so
     the formula *does something* concrete before it is trusted abstractly.
- Both are lesson-local CSS classes (copy from Lesson 014's `<style>`). First applied in **Lesson 014**;
  retro-fitted to **Lesson 013** (three boxes added: simple lemma, `d(W²)` numbers, general lemma) since
  the learner said they will revisit 013.
- Encoded in `.agents/skills/lesson-pedagogy/SKILL.md` ("Even more basic"). Applies to all future
  math-heavy lessons. Does **not** weaken retrieval/quiz rigor.

## Length A/B — provisional resolution (2026-08-13)
- The learner did not pick a KB target; instead they said 012/013 were hard to *understand*. Reading that
  as "the problem was clarity, not length," I am treating length as **"as long as the scaffolding needs"**
  and pouring the extra budget into `.plain` / `.numplay` grounding rather than more prose. Lesson 014
  landed ~ the 012/013 size band but denser with worked micro-examples. If the learner still finds a
  lesson long *and* unclear, split it; if unclear but fine on length, add more grounding boxes. Keep
  asking only if a future lesson feels genuinely too long in one sitting. **Update (015):** Lesson 015 ran
  to ~72 KB — the longest since 011 — because the replication → `p*` → Girsanov chain refuses to skip a
  link. If the learner reports it clear *but long*, the next lever is splitting Lesson 016, not trimming
  the `.plain`/`.numplay` boxes.
  **Update (016):** The first 016 draft was too short. The learner pointed at Lessons
  013–015 as the detail template, so 016 was rewritten to that slow-lane standard
  (hour map, every hedge cancellation written out, four-step Feynman–Kac proof, heat
  flip with numbers, put as worked example 2) and now sits above 015's size. Re-open
  a split only if 016 feels too long *in one sitting*.

## Standing weekly habits (don't let these lapse)
- 10 mental-math drills + 5 probability brainteasers/week (Green Book / Heard on the Street).
- 3–5 LeetCode problems/week from Year 1 (rotating arrays → DP → graphs → trees).
- After each math/pricing unit, add one derivation to "Derivations I own" below.

## Derivations I own (interview-ready, from memory)
- _(empty — add Itô's lemma, Black-Scholes PDE, Girsanov, OU solution, etc. as you master them)_

## Optional (◆) paper notes — "when it wins / when it breaks"
- _(one paragraph per ◆ paper as you skim it)_

## Standing decision — Years 4–6 are extra calendar (from 2026-08-22)
- **Feedback:** the learner asked whether long-only mid-term stock strategies exist, then asked
  to add curriculum tailored to that style, using **ML + optimization**, and to **extend time
  rather than swap**. They accepted a fourth year. They then asked to **extend the same
  long-only job to mid-frequency** (hours–days) as well, then asked for **data-prep and
  everything needed to start trading**, and then asked for a **lesson-by-lesson teaching
  plan only** — do **not** generate labs now.
- **Year 4:** Q1 is the data kit (units 121–130). Q2–Q4 are the monthly long-only
  book through the optimizer (131–160). Sheet: `reference/long-only-mid-horizon.html`.
  Teaching plan: `reference/year-4-lessons.html`.
- **Year 5:** Q1 defends the monthly book (161–170). Q2–Q4 are the same rules on an
  hours-to-days clock through the daily optimizer (171–200). Sheet:
  `reference/long-only-mid-frequency.html`. Teaching plan: `reference/year-5-lessons.html`.
- **Year 6:** Q1 defends the daily book (201–210). Q2–Q4 are paper and a tiny live
  desk (211–240). Teaching plan: `reference/year-6-lessons.html`.
- **Study order is the unit numbers.** The old "do 201–210 before Year 4" exception
  is gone — that kit is now 121–130.
- **What did not change:** Years 1–3 (units 001–120) stay in place, in order. Do not skip
  to Year 4, 5, or 6 from Year 1. Y2 Q2 (validation), Y2 Q3 (impact), Y3 Q1 (Grinold–Kahn),
  and Y3 Q2 (execution) are the on-ramps. Year 5 also needs Year 4's mandate language
  and optimizer (especially 131, 151–160, 163).
- **Name the horizon correctly:** everyday "mid-term" = this course's **low frequency**
  (weeks+) = the monthly book (Year 4 Q2 through Year 5 Q1). **Mid-frequency** =
  minutes–days = Year 5 Q2 through Year 6 Q1 (the Q1 lab's clock, without the shorts).
- **No labs authored for 121–240.** The teaching plans are the contract for future
  lesson authors: one skill, ordered beats, trap. Do not generate notebooks until asked.
- Encoded in `CURRICULUM.md` Years 4–6, both mandate sheets, the three teaching-plan
  pages, `MISSION.md`, and `RESOURCES.md` (QEPM, Gu–Kelly–Xiu, Jegadeesh 1990, Lehmann 1990,
  Bernard–Thomas, Amihud, Lou–Polk–Skouras, Boyd 2017, Gârleanu–Pedersen).

## Standing decision — Years 4–6 unit numbers match study order (from 2026-08-22)
- The data kit used to be numbered 201–210 (Year 6 Q1) with a note to do it *before*
  Year 4. That exception was a sequencing bug: anyone following unit numbers would
  backtest before they had a store.
- **Fix:** 121–130 is the data kit; 131–170 the monthly book (research through
  defense); 171–210 the daily book; 211–240 paper and live. Years 1–3 unchanged.
- Pedagogical order that was already right, and is now also the numbering:
  foundations → honest store → slower book → faster book → desk.

## Open questions / parking lot
- Secure real LOB data (LOBSTER / Databento / FI-2010) before Year 2 Q3.
- Decide on a compute setup for PyTorch labs (units 073–080) — local GPU vs Colab/cloud.
- **Length A/B — provisionally resolved (2026-08-13):** the learner's real signal was *clarity*, not
  length (012/013 hard to understand). Treating length as "as long as the scaffolding needs" and spending
  the budget on `.plain`/`.numplay` grounding. See the standing decision above. Only re-open if a future
  lesson feels too long *in one sitting*.
- **Learner marked Lesson 015 done (2026-08-22)** and asked for Lesson 016. No cold teach-back was
  graded in this session — still owed: the three 015 derivations (replication, `p*`, `θ = (μ−r)/σ`)
  and the `P`/`Q` probe ("is 56% a forecast?"). Glossary rows for 006–016 remain blank.
- **The `−½σ²` sign is now in its third costume (Lesson 016).** Same rule, opposite curvature: `log S`
  drags down `−½σ²`; a call's `½σ²S²V_ss` is a *lift* because `V_ss > 0`. The four-term budget at
  `(0,100)` is `−6.414 + 3.184 + 3.752 − 0.523 = 0`. Grade cold: derive the PDE from the hedge
  (`Δ = V_s`, then `dΠ = rΠ dt`), say why `μ` cancels, and state Feynman–Kac in one sentence. If those
  land, "the Black–Scholes PDE" and "Feynman–Kac" go into "Derivations I own."
- **New for 015 (Girsanov / risk-neutral pricing).** Three things to grade cold, not by MCQ: (1) set up
  and solve the two replication equations (`Δ = 0.5`, `B = −45`, price `5` — and note `p` never appears);
  (2) derive `p* = (R−d)/(u−d)` by regrouping the replication cost; (3) derive `θ = (μ−r)/σ` by
  substituting `dW = dW̃ − θdt` into `dS = μS dt + σS dW`. All three ⇒ "the risk-neutral price" goes into
  "Derivations I own." Watch two specific confusions: **`N(d₂) = 56%` is a pricing weight, not the 74%
  real-world chance of exercise** (same error as quoting a risk-neutral default probability as a default
  rate), and **Girsanov moves the drift but can never move `σ`** (quadratic variation is path-wise, and
  equivalent measures agree on almost-sure facts — the same reason `μ` needs ~400 years of data to pin
  down while `σ` does not).
- **Browser verification is owed for Lesson 015's three widgets** (skipped at the learner's request when
  015 shipped) **and for Lesson 016's three widgets** if this session cannot eyeball them. `.smoke.js`
  geometry traps cover layout regressions, but nothing has been eyeballed at 375px.
- **New for 014:** watch that the learner keeps the two OU spreads distinct (mean → `m` vs wobble →
  `σ²/2θ`), reads `θ(m−X)` as a pull *toward* `m`, and remembers the small-sample θ bias (short fits
  overestimate reversion) — that bias is the lab's punchline and a real pairs-trade trap.
- **Glossary drill owed:** rows for 006–016 are all still blank (67 terms now). Do one cold-definition pass
  and fill only what the learner defines unaided.
- Lesson 010 was **self-reported** as passed (no EXIT TICKET graded here) — offer a fresh checkpoint
  scenario at the next natural break.
- **New for 016 (Black–Scholes PDE / Feynman–Kac).** Grade cold, not by MCQ: (1) write Itô on
  `V(t,S)` under `Q` and form `Π = V − V_s S` until `dW` dies; (2) impose `dΠ = rΠ dt` and rearrange
  to `V_t + rS V_s + ½σ²S² V_ss − rV = 0`; (3) state Feynman–Kac in one sentence (PDE + terminal
  condition **is** the discounted `Q`-average). Watch three confusions: **`μ` in the PDE** (residual
  `+6.368` at the running point), **dropping the curvature term** (ordinary calculus, residual
  `−3.752`), and **writing the payoff as a starting condition**. The four-term budget
  `−6.414 + 3.184 + 3.752 − 0.523 = 0` should become as automatic as `−½σ²`.
