---
name: lesson-pedagogy
description: Apply retrieval practice, spacing, interleaving, and prediction-before-reveal so lessons build storage strength (durable memory), not just in-the-moment fluency. Use when authoring or editing any lesson HTML.
---

Use when creating or editing a lesson. Knowledge and skills only stick if the lesson is built for
**storage strength** (long-term retention), not **fluency** (feeling fluent while re-reading). The
`teach` skill names fluency as the enemy. Three cheap, reusable mechanisms enforce this, and every
lesson from 002 on should carry all three.

## Lesson depth (this learner's standing preference)

This learner wants **long, substantial lessons — ~22–30 KB, ~55–60 min, 8–12 `<h2>` sections** — not
terse skeletons. Prefer more text and more worked detail. For each major idea: motivate it, develop it
in full prose with a worked numeric example, show a second-order consequence or subtlety, name its
failure mode in a `.trap`, and connect it forward in the curriculum. Never compress a conceptual beat
into a single table row when it deserves a paragraph. (This overrides the generic "keep lessons short"
default in the `teach` skill for this workspace — see `NOTES.md`.)

### Explain everything you introduce (standing decision, 2026-07-17, Lesson 006 on)

**Thoroughness overrides brevity.** Every term, symbol, formula, or method a lesson *introduces* must be
fully explained where it first appears — defined in plain words, motivated (why it exists / when you reach
for it), and grounded in at least one worked numeric example. No naked jargon, no symbol used before it is
defined, no "we'll cover this later" hand-wave for something the current lesson actually relies on. If a
concept is only *previewed* (developed in a later unit), say so explicitly and give the one-line intuition
anyway. It is better to overrun the ~22–30 KB / ~55–60 min band than to leave anything introduced
under-explained — treat that band as a floor for depth, not a cap. This is the learner's explicit standing
preference (see `NOTES.md`) and applies to every future lesson.

## 1. Open every lesson with a spaced-retrieval warm-up (`assets/retrieval-bank.js`)

Before new material, make the learner recall **older** material from memory. Spacing + interleaving +
effortful retrieval are the highest-leverage retention levers.

```html
<h2>Warm up</h2>
<div id="warmup"></div>
...
<script src="../assets/retrieval-pool.js"></script>
<script src="../assets/retrieval-bank.js"></script>
<script>
  RetrievalBank.mount(document.getElementById("warmup"), { upTo: 3, count: 3 });
</script>
```

- `upTo` = **this** lesson's number. The bank only draws from lessons *before* it (spacing), never the
  fresh material. Lesson 001 has nothing earlier, so it shows the empty state — that is fine.
- It is Leitner-scheduled in `localStorage` (`fe-retrieval`): a missed item returns next session, a
  mastered one returns much later. Nothing to configure per lesson.
- **Feed the pool** (`assets/retrieval-pool.js`) whenever a lesson ships a durable, testable idea — add
  one or two items with a **stable `id`** (never renumber; Leitner state is keyed on it). Options must be
  similar length (quiz-fairness standard). Tag `misconception: true` for items that mirror a known trap.

## 2. Add a prediction-before-reveal prompt before any result (`assets/predict.js`)

Where a lesson reveals a number or an outcome (a walked-book average fill, a kurtosis value, a
"which is bigger" comparison), make the learner **commit a prediction first** (the pretesting effect).
Place it *above* the reveal.

```html
<div id="predict1"></div>
<script src="../assets/predict.js"></script>
<script>
  Predict.mount(document.getElementById("predict1"), {
    prompt: "Before reading: a market buy for 500 lots against this book fills, on average, at…",
    options: [ { label: "Exactly the best ask", value: "best" }, { label: "Worse than the best ask", value: "worse" } ],
    correct: "worse",
    reveal: "It walks the book (level 1, then level 2), so the average fill is worse than the top quote — that gap is slippage."
  });
</script>
```

Use it once or twice per lesson, on the genuinely non-obvious results — not on every table.

## 3. Add one teach-back / Feynman prompt per lesson (`assets/teachback.js`)

Recognition (multiple choice) is the weakest retrieval; **explaining a concept in your own words** is the
strongest, and it trains the mission goal ("defend an edge to a skeptical PM without hand-waving"). Once
per lesson, on the *load-bearing* idea, make the learner write an explanation before revealing a model
answer + a self-check list of the points a good answer hits.

```html
<div id="teachback1"></div>
<script src="../assets/teachback.js"></script>
<script>
  Teachback.mount(document.getElementById("teachback1"), {
    prompt: "In your own words: why is direction nearly unpredictable while volatility is forecastable?",
    points: ["Raw returns show ~0 linear autocorrelation", "So naive momentum on returns fails", "But |returns| are autocorrelated — vol clusters", "So GARCH/HAR can forecast vol, not sign"],
    model: "A model answer to compare against."
  });
</script>
```

The reveal is gated until the learner writes something (forces an attempt). Static HTML can't grade prose,
so the widget nudges the learner to paste their explanation to the teacher (chat) for real feedback — when
they do, grade it and, if they can explain it cold, add the term to `GLOSSARY.md`.

## Cross-cutting artifacts to keep current

- **`GLOSSARY.md`** — the ubiquitous language. Every lesson must use terms consistently with it; add a row
  when a lesson introduces a term (alpha, spread, slippage, kurtosis, filtration, …).
- **`NOTES.md` → "Derivations I own"** — after each math/pricing unit, the learner adds one derivation they
  can reproduce from memory. Lessons that build toward a derivation should remind them.
- **Watch-points (misconceptions).** When a quiz, warm-up, or lab exposes a wrong belief, add a matching
  `misconception: true` item to `assets/retrieval-pool.js` so the wrong belief re-enters the spaced rotation
  until it is gone.

## Failure-mode-first (mission-specific, non-negotiable)

Per `NOTES.md`, every method is taught **with the way it breaks** (leakage, overfitting, non-stationarity).
The `.trap` box is mandatory in every lesson, not decorative. Prefer to also encode that trap as a
`misconception: true` pool item so it keeps returning.

## Verification

Open the lesson in a browser (`file://` or a local server) and confirm all three widgets mount without
console errors, the warm-up draws only from earlier lessons, the predict widget gates Reveal behind a
commit, and the teach-back gates Reveal behind an attempt. See `lesson-visuals` for the full checklist.

## Reference implementation

**Lesson 004 ("Returns & the Stylized Facts")** carries a spaced-retrieval warm-up, a prediction-before-reveal
(on the kurtosis / fat-tail result), and a teach-back (on direction-vs-volatility predictability). Copy its pattern.
