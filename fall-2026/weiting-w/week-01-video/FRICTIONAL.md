# FRICTIONAL — One Word, Same Answer

Dated log of what broke and what I did instead. Per the assignment: a working video made with an honest log of the friction is worth more than a silent, broken build. Nothing here is invented; where a problem was worked around rather than fully solved, that is said.

## 2026-09-27 — Concept selection

- Started with a softmax beat sheet ("three scores are not yet three chances"). Found it overlapped closely with a classmate's already-submitted video, so it was not viable. Switched to the Chapter 1 Part 2 concept "constraining the output format narrows the spread without checking anything," which no one in the group had taken.

## 2026-09-27 — Experiment method

- The chapter's original comparison (deck sentence vs. one-word capital) changes two variables at once (question and format). Added a control — the same capital question with no format rule — so each comparison changes only one thing.
- Ran the set twice: Run 1 in a normal account, Run 2 in incognito (memory off; personal preferences on in both). Run 1's free answers came back unexpectedly short (~6 words), while Run 2's were ~32 words. This showed something outside the prompt was already narrowing answers in the normal account, and it became the video's main finding. The cause is not isolated (incognito may change more than memory); this limit is stated on screen in B07.

## 2026-09-27 — Toolkit friction

- `./art doctor` exits early on ElevenLabs references inside Brutalist's own example files (not mine). Did not block my reel; noted and moved on.
- Manim serif letter spacing (EB Garamond) rendered unevenly — letters inside a word spaced differently. This is a known ManimPango issue at small point sizes (Pango rounds each glyph's position to a whole pixel; the smaller the layout size, the larger the relative error). Changing fonts and reinstalling did not fix it, because the cause is layout point size, not the font. The documented workaround is to lay text out oversized and scale it down. I judged the residual kerning cosmetically imperfect but acceptable, and shipped rather than restructure every text object under the deadline. Recorded here as a known, unresolved cosmetic limitation.

## 2026-09-27 — Quality gates (the long part)

- **GATE B (post-render layout audit).** B05 and then B06 failed with "layout errors." Cause: Run 2's free replies are long (~30 words), and scenes that stacked four of them ran past the bottom safe margin. Fix: measure each block's real rendered height at build time and scale it to fit a fixed band, without cutting any verbatim text.
- **`./art final` refused with "10 slates."** Learned that `final` does not render — it only assembles beats that `./art run` has already rendered into `manim/` and `media/`. Running `final` on a cleared cache produced ten slate placeholders, which a clean master rejects by design. Correct order: `./art run` first (renders clean beats), then `./art final`.
- **Slate vs. clean master confusion.** `./art run` writes a review cut named `<slug>-slate.mp4` with a debug label burned into the corner of every beat; the clean master is a separate file, written by `./art final` into `renders/<slug>.mp4` with no label. I mistook the slate review cut for the final more than once before finding the clean file in `renders/`.
- **GATE T (type-lock, strict on `final`).** Two failures: B02 had a text run 1 px under the 41 px minimum (a serif run — serif renders shorter than sans at the same size), and B03 used the bright accent color for a thin arrow at 2.74:1 contrast (< 4.5:1). Fixes: raised the serif prompt text and used the darker contrast-safe accent for the arrow. Raising the serif to clear the floor took two passes, because the first pass raised the wrong (sans) labels.
- **GATE V (frame-level, strict on `final`, no lenient downgrade).** Four edge-bleed blockers (card borders crossing the 5% title-safe inset on B02, B05, B06) and two underfill majors (B02, B03 sparse at their mid-beat sample). Fixes: pulled the card borders inward using the safe box read from the toolkit's own `final_frame_check.py`; and declared B02/B03 `qc.sparse_by_design` with written reasons, which is the toolkit's sanctioned waiver for beats that reveal content gradually. GATE V passed clean (BLOCKER 0, MAJOR 0), and `./art final` wrote the verified master.

## Result

Clean 4K master, 198.5 s, sha256 `2aff490b2d4f0b1550eb65212813f4af454427324f652687f73e6d7e8d58b0f9`, written 2026-09-28 (UTC). No labels, all ten beats, real audio.
