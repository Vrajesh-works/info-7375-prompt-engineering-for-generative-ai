# FRICTIONAL — low-temperature-is-not-argmax

Dated log of everything that broke during the build, what it turned out to
be, and what fixed it. Per the assignment: "If the toolkit fails on your
machine, that is a legitimate Frictional entry and not an automatic loss of
points... A working video made another way, with an honest log of why, is
worth more than a broken Brutalist build submitted silently."

---

**2026-09-26 — Missing `pip`**
`./setup --install` failed: `No module named pip` for the Homebrew Python
3.11 install. Fixed with `python3.11 -m ensurepip --upgrade`, then reran
`./setup --install` successfully (Kokoro, Manim, Remotion node deps all
installed; a handful of unrelated `pip` dependency-conflict warnings from
other, already-installed packages on the machine — not caused by this
install and not blocking).

**2026-09-26 — Missing `ffmpeg`**
First Manim render (`manim -pql scenes.py B04_RefusalAndConcentration`)
failed: `RuntimeError: Manim could not find ffmpeg`. Fixed with
`brew install ffmpeg`. Both target scenes rendered cleanly afterward.

**2026-09-26 — Text-shaping glitch in rendered Manim text**
Multiple words in the first Manim render showed a spurious space mid-word
("sample()" → "samp le()", "variance" → "v ariance"). This is a known
Pango/HarfBuzz text-shaping issue on some macOS Manim installs. Worked around
by wrapping every `Text()` call in a helper that forces an explicit installed
font (`Oswald`, already installed by Brutalist's own `./setup --install`) and
disables ligature-based shaping. Confirmed improved on re-render; one
remaining minor artifact was accepted as a cosmetic tradeoff rather than
chased further.

**2026-09-26 — Toolkit schema mismatch**
My first-draft `beat_sheet.json` did not match the `cli-explainer` skill's
actual required schema (beat spine, Remotion component names/props). Diagnosed
by reading the toolkit's own `SKILL.md` and two of its worked examples
(`brand-palette-accessibility-auditor`), then rebuilt the beat sheet to match
the real required spine: INTRO → PROBLEM → ASK → CODE → OUTPUT → CHANGE
(revision) → OUTPUT (revised) → SUMMARY → NEXT STEPS → OUTRO.

**2026-09-26 — Kokoro voice code error**
`generate_audio_kokoro.py` failed: `unknown voice(s): claude-liam`. The beat
sheet's metadata used a persona/channel name instead of a real Kokoro voice
code. Fixed by checking `--list-voices` and correcting the field to
`am_onyx`.

**2026-09-26 — Gate A: "shapes never change" (repeated-animation defect)**
`./art run`'s static pre-flight check failed on `B04_RefusalAndConcentration`:
all three bars in the bar-chart scene were added to the scene in a single
`self.play()` call with their final geometry already baked in, so nothing
ever visibly changed after that — mechanically identical to the "one drawing
held for the whole video" defect the gate is designed to catch. Fixed by
restructuring `_bars_for()` to reveal each bar in its own `self.play()` call,
so the shape set genuinely grows step by step. Confirmed via
`static_scene_check.py` before re-rendering.

**2026-09-26 — Gate W: chapter number on slide**
Gate W (WCAG/layout/text checks) flagged on-screen text containing the
substring "chap-" (a house rule against showing chapter numbers on screen —
name the topic, not the chapter). Several on-screen fields (a `topic` label
repeated across 5 beats, a `runningText`, a card `title`, and a card `sub`
line) said things like "CHAPTER 1 · ..." or "the chapter's reference
implementation." Fixed by rewording all of them to name the topic
("Randomness and First Prompts") or the artifact ("reference implementation")
instead of the word "chapter."

**2026-09-26 — Missing toolkit asset: FormBCard icons 404**
`./art run` failed rendering B01 (`FormBCard`): three icon files
(`zap.svg`, `target.svg`, `list-checks.svg`) returned 404. Diagnosed as a bug
in the shared toolkit itself — `FormBCard.tsx` looks for icons in
`runtime/remotion/public/form-b-icons/`, a folder that does not exist in a
fresh clone and is not created by any setup script, even though the
component's own two worked examples in the repo use the exact same icons and
would hit the same failure. Fixed locally only: copied the three icons (plus
a fourth, `check-circle.svg`, added later for a 4-item card) from the
toolkit's own `icons/svg/` into the folder the component expects. No shared
toolkit source file was modified; the icon copy is untracked and specific to
this machine.

**2026-09-26 — Gate F: missing FACTCHECK.md / SHOTLIST.md / PROMPTS.md**
`./art run` refused with `GATE F FAILED` before rendering anything, requiring
these three files to exist before any render — even a previz. Used the
documented previz-only bypass `ART_FACTS=0` to iterate on the review cut, per
the toolkit's own stated exception; `./art final` (the real master export)
correctly refuses this bypass and requires all three files for real, which is
why they were written properly before the final render (see below).

**2026-09-26 — Gate B: layout audit, edge-pinned text out of the safe area**
B04 and B06's title/caption text sat 0.1–0.2 units outside the ±3.4 safe
band on the top/bottom edges. Fixed by increasing the edge buffer
(`EDGE_BUFF = 0.7`) on all edge-anchored text in `scenes.py`.

**2026-09-26 — Gate V: canvas-fill failures on three separate beats**
The frame-level visual QC gate (55% minimum non-background content coverage
in the title-safe area, sampled at 50%/85% of each beat) failed on:
- **B01** (FormBCard, 3 items): the component's fixed 3-item layout never
  reaches 55% fill; the toolkit's own 4-item layout was previously widened to
  pass this same gate, but the 3-item layout was not. Fixed by adding a
  fourth card item rather than modifying the shared component.
- **B04 and B06** (Manim): the compiler was stretching each clip 2.7×–3.1×
  to match narration length no longer aligned to actual animation length,
  producing long stretches of near-static frames. Fixed by re-timing both
  scenes to read real measured narration durations and pace the reveals
  against them.
- **B07**: this beat had no scene at all — a placeholder slate, not the
  equation card the beat sheet's own `visual_intent` called for. Built an
  actual `TypesetMath`-based Remotion scene showing the ratio formula and the
  boundary statement, since Manim's equation renderer needs a LaTeX install
  this machine doesn't have.
- **B09**: after removing three duplicate closing beats (see below) and
  replacing the outro with a card carrying real recap content, the card's
  height-driven layout initially filled only ~8–29% of the frame with a
  single short line. Fixed by restoring a 5-line recap (drawn from the
  removed beats' own already-verified content) to fill the card properly —
  confirmed 60.5% fill at both required samples, a solid margin above the
  55% minimum, versus an earlier attempt that passed one sample by 0.1% and
  failed the other on compression noise.

**2026-09-26 — Removed three duplicate closing beats**
The beat sheet, copied from a worked-example schema, included `BVDT`
(verdict), `BHTF` (handoff), and `BOUT` (outro) beats with no narration text
— these duplicated content the sheet's own `B07`/`B08`/`B09` beats already
covered properly. `./art run` refused to compile with silent, unexplained
beats (`missing required audio or media`). Removed all three from the beat
sheet and its metadata rather than writing throwaway narration for content
that was already covered.

**2026-09-26 — Toolkit's own persona/branding hardcoded into worked examples**
The beat sheet, built from the `cli-explainer` skill's worked examples,
inherited the toolkit's own default persona narration ("This is Liam, in for
Bear") and a hardcoded `@NikBearBrown` handle in several composer beats and
the title-outro component. "Bear" (Nik Bear Brown) is this course's own
instructor — not something that belongs in a homework submission regardless.
Fixed: reworded all narration to remove the persona framing entirely;
removed the handle from every composer beat (`folderLabel`); swapped the
title-outro component (`ClaudeTitleOutro`, whose handle is hardcoded in the
component itself, not settable from the beat sheet) for `ClaudeVerdictArtifact`,
a component with no default branding, on the toolkit's own documented
library-first principle rather than editing the shared component. Changed
`metadata.channel` from `claude-liam` to the neutral `claude`.

**2026-09-27 — Central claim fact-checked and found false; corrected**
Before permitting `./art final`, the toolkit's own required fact-check step
(writing `FACTCHECK.md`) required verifying every claim in the narration
against the reference implementation. This caught a real error: the video's
claim that "temperature never produces zero variance" is false. Running
`sample()` at `temperature=0.1` and `temperature=0.001` (beyond the single
`T=0.5` value actually shown running on screen) showed that low positive
temperatures both routinely produce, and — via real floating-point
underflow below roughly T ≈ 0.00134 for these scores — can produce
*exactly* zero variance, computationally identical to `argmax_select()`'s
output. The corrected version (in the final narration): in exact mathematics
every outcome keeps a positive probability at any T > 0, so the distribution
never has to become one-hot; in practice, a finite sample can land on one
outcome by chance, and real floating-point code can make the other
probabilities compute to exactly zero. Reworded B05–B09's narration and two
on-screen card lines to reflect this; one further correction was needed
after the first revision (B09's "sampling only looked that way in this one
run" contradicted the video's own earlier statement that 151/1000 draws
missed the top outcome) — caught before the final render, reworded to
"sampling can look that way at lower temperatures," which is what the
fact-check data actually supports.
