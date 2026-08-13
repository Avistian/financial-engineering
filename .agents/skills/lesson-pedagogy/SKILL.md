---
name: lesson-pedagogy
description: >-
  Author or revise financial-engineering lessons, labs, and tutor explanations.
  Use whenever writing lesson HTML, lab notebooks, glossaries, or teaching from
  this curriculum — enforces plain language, full definitions, and slow pacing.
---

# Lesson pedagogy (financial-engineering)

Read `NOTES.md` standing decisions before writing. Those are authoritative; this skill is the checklist.

## Plain language for every term (2026-07-27 — mandatory)

The learner still finds language and concepts unclear when prose stays specialist.

**Before any jargon or formula:**

1. Everyday picture in one sentence.
2. Then the standard name.
3. Then the symbol / formula (if needed).
4. Then one tiny concrete example.

**Litmus test:** after one short plain sentence, can a strong programmer with near-zero finance
vocabulary say what the word *literally means here*? If not, rewrite.

**Define on first use in the same breath** — not later, not via other jargon, not "as we saw."
Flag when a word’s finance sense differs from everyday English (*book*, *security*, *option*,
*hedge*, *signal*, *the market*).

Hard quizzes stay hard. Only the *way in* gets simpler.

## Explain everything you introduce (2026-07-17)

No naked jargon. No "see later." No symbol before it is defined. Thoroughness overrides brevity.
Longer self-contained lessons beat terse skeletons.

## Pace for understanding (2026-07-23)

1. Intuition before symbols.
2. One new idea per beat; split dense paragraphs.
3. Re-warm prerequisites inline (do not assume undergrad math or earlier lessons are fresh).
4. Slow lane for derivations: every algebra step annotated with *why* it is legal.

Retrieval (warm-ups, predict, teach-back, quizzes) stays effortful. Slow the teaching, not the testing.

## Even more basic (2026-08-13 — mandatory on math-heavy lessons)

The learner reported that Lessons 012–013 were still hard to *understand* even with plain language and
slow pacing. Plain language and depth are necessary but not sufficient; the remaining gap is that abstract
symbols never touch ground. Two concrete devices are now required on every math-heavy lesson (and
retro-fitted where the learner revisits):

1. **In-plain-words note (`.plain`).** Immediately after *every* load-bearing equation, add a short note
   (tagged "In plain words") that restates the equation as one plain English sentence, symbol by symbol
   ("how f changes = slope times step, plus half the curvature times the step length"). No new notation,
   no jargon — just the plain translation. (Do **not** call it "say it aloud" — the learner disliked that
   framing, 2026-08-13.)
2. **With-real-numbers box (`.numplay`).** Before or right after an abstract result, plug in actual small
   numbers and compute a step or two by hand (e.g. θ=2, m=100, X=80 ⇒ pull = +40). The learner should see
   the formula *do something* on concrete values before trusting it in the abstract.

Both are lesson-local CSS classes (`.plain`, `.numplay`) — copy the block from Lesson 014's `<style>`.
Keep them short (2–4 sentences). This does not replace the slow-lane derivation; it wraps it so each
symbol arrives already grounded. Rigor of quizzes/teach-backs is unchanged.

## Also always

- Failure-mode first (`.trap` is mandatory).
- One skill per lesson; labs keep peripheral code PROVIDED.
- Cite `RESOURCES.md` for moving parts; no hand-waving on TFMs / deep LOB / RL.
- Feed `assets/retrieval-pool.js` when a durable idea ships (stable ids).
