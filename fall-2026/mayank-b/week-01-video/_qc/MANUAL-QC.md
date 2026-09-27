# Manual visual QC (2026-09-23), frames read by eye

Frames sampled at 15/50/85% of every beat (`sheet1-3.png`), plus B01 at 2.5/4.5/6.5/9.0/11.2 s (`fixsheet.png`).
(`REPORT.md` in this folder is the toolkit's automatic Gate V report, which overwrites itself on each compile.)

| # | Beat | Severity | Defect | Fix | Status |
|---|---|---|---|---|---|
| 1 | B01 | BLOCKER | the correction never appeared on screen; typing unfinished at beat end | single-word trigger, 32 ms/char | fixed, re-checked |
| 2 | B00, BHTF | MAJOR | composer text undersized | `largeText: true` | fixed, re-checked |
| 3 | B04 | MAJOR | "54.60×" clipped past the right safe edge (test still) | bar max 520 px | fixed |
| 4 | B06 | MAJOR | count legends collided (test still) | label-over-number columns | fixed |
| 5 | B07 | MINOR | honesty stamp wrapped onto two lines | nowrap, wider box | fixed |
| 6 | B08 | MINOR | dead space under the claims | bigger cards/type | fixed |
| 7 | BVDT | MINOR | library recap page's text is smallish; component has no size prop | — | open |
| 8 | B08 50% | — | cards overlap mid-flight while sorting | intended motion; settles by 85% | not a defect |

## v5 (2026-09-27)
| # | Beat | Severity | Defect | Fix | Status |
|---|---|---|---|---|---|
| 9 | B01A | MAJOR | "Paris" landed beside the blank, not in it (test still) | measured end position | fixed |
| 10 | B01A | MAJOR | flying word crossed the bar and label mid-flight | fade-and-rise instead of a flight | fixed, re-checked (`sheet-v5-B01A.png`) |
| 11 | B01A | MINOR | two terracotta elements | "softmax" in bold ink | fixed |
| 12 | B01 | MAJOR | last line still typing at the cut ("…answer is tr") | charMs 32 → 26 | fixed, re-checked (`sheet-v5-B01.png`) |

## v6 (2026-09-27)
Frames: `sheet-v6.png` (B02 and B03 at 15/50/85%, B08 at 85%, BVDT → BOUT join).
| # | Beat | Severity | Defect | Fix | Status |
|---|---|---|---|---|---|
| 13 | B02, B03 | MINOR | footers wrapped to two lines (test stills) | shorter text, nowrap | fixed |
| 14 | B02 | MINOR | "e^z" as raw caret text in the footer (math rule) | "direct exponentials" | fixed |
All numbers on screen checked against `code/build_props.py` output. BVDT → BOUT join clean.

## v7 (2026-09-27)
`sheet-v7.png`: B00 chip, outro card, and the lower-right corner of every beat. @Mayank everywhere a
handle appears; no @NikBearBrown on screen. Gate V: 0 BLOCKER / 0 MAJOR.

## v8 (2026-09-27)
`sheet-v8.png`: B00 new question; B02 at 30/60/95%; B02B end; B07 end (✕ centred on the line, formula in card);
B08 end (SHOWN green, NOT SHOWN red); BVDT end; BOUT. One fix before render: B07 card header wrapped → shortened.
Gate V: 0 BLOCKER / 0 MAJOR.
