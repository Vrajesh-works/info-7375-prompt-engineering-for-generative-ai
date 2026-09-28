# TYPECHECK.md — GATE T

Reel: `subtract-the-max`  |  Checked: 2026-09-27T01:01  |  Overall: **FAIL**  |  Beats checked: 10  |  FAILs: 6

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | ? | light | min-size §8.1: min text-run height 92px >= floor 41px | PASS | — |
| B02 | ? | light | kerning §8.4: max inter-glyph gap 60px > threshold 14px (15.5× expected 4px) — check kern … | **FAIL** | Add font='EB Garamond' to all Text() in scenes.py |
| B03 | ? | light | kerning §8.4: max inter-glyph gap 233px > threshold 26px (31.4× expected 7px) — check kern… | **FAIL** | Add font='EB Garamond' to all Text() in scenes.py |
| B04 | ? | light | kerning §8.4: max inter-glyph gap 97px > threshold 24px (14.4× expected 7px) — check kern … | **FAIL** | Add font='EB Garamond' to all Text() in scenes.py |
| B05 | ? | light | kerning §8.4: max inter-glyph gap 87px > threshold 21px (14.3× expected 6px) — check kern … | **FAIL** | Add font='EB Garamond' to all Text() in scenes.py |
| B06 | ? | light | min-size §8.1: smallest text run 9px < floor 20px (1.9% of 1080px logical); likely a capti… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| BVDT | BOOKEND | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | BOOKEND | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | BOOKEND | light | kerning §8.4: max inter-glyph gap 76px > threshold 37px (7.1× expected 11px) — check kern … | **FAIL** | Add font='EB Garamond' to all Text() in scenes.py |

---

## Failures requiring action before cut

### B02 (?)
- **kerning §8.4**: max inter-glyph gap 60px > threshold 14px (15.5× expected 4px) — check kern tables or Pango shaping for this font at this size
- **Fix:** Add font='EB Garamond' to all Text() in scenes.py

### B03 (?)
- **kerning §8.4**: max inter-glyph gap 233px > threshold 26px (31.4× expected 7px) — check kern tables or Pango shaping for this font at this size
- **Fix:** Add font='EB Garamond' to all Text() in scenes.py

### B04 (?)
- **kerning §8.4**: max inter-glyph gap 97px > threshold 24px (14.4× expected 7px) — check kern tables or Pango shaping for this font at this size
- **Fix:** Add font='EB Garamond' to all Text() in scenes.py

### B05 (?)
- **kerning §8.4**: max inter-glyph gap 87px > threshold 21px (14.3× expected 6px) — check kern tables or Pango shaping for this font at this size
- **Fix:** Add font='EB Garamond' to all Text() in scenes.py

### B06 (?)
- **min-size §8.1**: smallest text run 9px < floor 20px (1.9% of 1080px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### BOUT (BOOKEND)
- **kerning §8.4**: max inter-glyph gap 76px > threshold 37px (7.1× expected 11px) — check kern tables or Pango shaping for this font at this size
- **Fix:** Add font='EB Garamond' to all Text() in scenes.py

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 10 | 1 |
| overflow §8.2 | 10 | 0 |
| contrast §8.3 | 10 | 0 |
| contrast-local §8.3b | 10 | 0 |
| bbox-overlap §8.6b | 10 | 0 |
| card-clip §8.13 | 10 | 0 |
| kerning §8.4 | 6 | 5 |
| redundancy §8.10 (advisory) | 1 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
