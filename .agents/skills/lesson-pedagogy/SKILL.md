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

## Also always

- Failure-mode first (`.trap` is mandatory).
- One skill per lesson; labs keep peripheral code PROVIDED.
- Cite `RESOURCES.md` for moving parts; no hand-waving on TFMs / deep LOB / RL.
- Feed `assets/retrieval-pool.js` when a durable idea ships (stable ids).
