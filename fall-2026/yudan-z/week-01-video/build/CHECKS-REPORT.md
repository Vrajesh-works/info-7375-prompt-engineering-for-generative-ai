# CHECKS-REPORT.md — written before the first render

11 beats: **10 SHOW / 0 justified-HOLD / 0 PUNT-flagged** (+1 CARD: the B10 title outro).

Teaching arc (nopunt § whole-sheet checklist):
FRAMEWORK ✓ (B01 overview + B02 the move, before any worked numbers) |
WORKED EXAMPLE ✓ (B03 walks [1, 2, 3] through every stage on screen) |
FALSIFIABILITY ✓ (B07, a full beat: [0, -1000] underflow) |
SCAFFOLDED TASK ✓ (B09 prompt + three checks) |
BOOKENDS ✓ (cold open, verdict, your turn, title outro — see deviation 2) |
NO-SOURCE-NO-VERDICT ✓ (every claim beat shows its evidence value or source line)

Known deviations, decided by the author:

1. **No channel identity.** No "in for Bear", no `@NikBearBrown` handle or logo. The corner text is
   "Yudan Zhou · INFO 7375" (LOGO LAW's wordmark fallback, with the author's name instead of a channel).
2. **Outro** is a plain `FormACard` title card, not `ClaudeTitleOutro`. The OUTRO-LOCK card
   hard-codes `@NikBearBrown` and applies to claude-liam reels only. compile.py's skin lint will warn.
3. **Consecutive scheme.** B02→B03 and B06→B07 share `ArrayPipeline` (ILLUSTRATE LAW calls this a
   smell). Accepted: A/B are one lane and E/F are two contrasting lanes, and splitting them across other
   schemes would move evidence off screen.
4. **B01 correction is one word** (`distribution` → `weights — not the distribution`). The registered
   `BrutalistHesitantWriter` matches triggers per whitespace token and splits replacements on commas, so
   the phrase-level correction in the review draft ("makes the math numerically stable") cannot be
   expressed without editing it.
5. **Corner label by overlay** on B00 (disclosure line), B04 and B10. `TypesetMath` and `FormACard`
   have no `brandLabel` prop. `overlay_labels.py` composites the text onto their rendered clips instead
   of editing those components.
