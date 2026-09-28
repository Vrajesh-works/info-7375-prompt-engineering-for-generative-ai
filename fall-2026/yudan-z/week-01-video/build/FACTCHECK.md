# FACTCHECK.md — week01-max-subtraction-yudan-z

Evidence record: `C:\Users\zyud0\info-7375\fall-2026\yudan-z\week-01-video\evidence\evidence_output.json`
(sha256 `a7a9cc36ec18c2e1b11c228f97a1c63371caa4f1fe338ac92e7ef04cbdb3168b`), produced 2026-09-27 by
`max_subtraction_evidence.py` on Windows 11, CPython 3.14.2. Course repo commit `62992c0`.

## On-screen numbers — machine-checked

`build_sheet.py` copies every on-screen value from the JSON with `json.dumps` (the same text the file
holds) and refuses to write the sheet if any number token on screen is missing from the file. Last run:
60 tokens checked, 0 missing. Negative test (2026-09-27): substituting SCRIPT.md's 10-digit rounded
weights (`0.1353352832`, `0.3678794412`) made the script refuse. Exempt tokens: `7375` (course number),
`11` ("Windows 11"), `1`/`2`/`3` ("Check 1/2/3" labels).

## Claims

| Beat | Claim | Source | Status |
|---|---|---|---|
| A | The reference implementation subtracts the maximum before `exp` | `lessons/01-.../code/main.py`: `peak = max(logits)`, `math.exp((x - peak) / temperature)` | ✓ |
| A | `[1, 2, 3]` → peak `3` → `[-2, -1, 0]` | case A `intermediates` | ✓ |
| B | Largest shifted score is `0`, its weight exactly `1.0`; others < 1 | case A `weights` `[0.1353352832366127, 0.36787944117144233, 1.0]` | ✓ |
| B | Total "one point five oh three two" (spoken rounding) | case A `total` `1.5032147244080551` (on screen in full) | ✓ |
| C | `exp((zᵢ−m)/T) / Σⱼ exp((zⱼ−m)/T) = exp(zᵢ/T)exp(−m/T) / (exp(−m/T) Σⱼ exp(zⱼ/T)) = exp(zᵢ/T) / Σⱼ exp(zⱼ/T)` | Chapter 1 lines 152–164 | ✓ algebra below |
| D | Shifted and direct routes differ by at most `1.1102230246251565e-16` on `[1, 2, 3]` | case A `max_abs_difference` | ✓ |
| D | "The evidence script computed…" (not "I computed") | narrator is synthetic; the script did the computing | ✓ edit |
| E | Direct route on `[1000, 1000]` raises `OverflowError: math range error` | case B `direct_unshifted.error` | ✓ |
| E | Shifted route: `[0, 0]` → `[1.0, 1.0]` → `2.0` → `[0.5, 0.5]` | case B `intermediates` | ✓ |
| F | "keep the claim narrower than 'numerically stable'" | Chapter 1 line 186 | ✓ quoted on screen (11 words) |
| F | `[0, -1000]` returns `[1.0, 0.0]`, with no exception | case C `reference_shifted`; the script called `probabilities` unguarded and did not stop | ✓ |
| F | float `exp(-1000)` = `0.0`; decimal `exp(-1000)` = `5.07595889755E-435` | case C | ✓ |
| F | "The real second probability is about 5.08 × 10⁻⁴³⁵" | true p₂ = e⁻¹⁰⁰⁰/(1+e⁻¹⁰⁰⁰); the denominator differs from 1 by ~5e-435, so p₂ equals `decimal exp(-1000)` to every printed digit. On screen the row is labelled `decimal exp(-1000)`, as the JSON names it. | ✓ |

## Algebra (MATH-TYPESETTING.md: verified separately from the typography)

- Domain: `T > 0` (shown on screen); `m = maxⱼ zⱼ`, a constant across `i` and `j`.
- `exp((zᵢ−m)/T) = exp(zᵢ/T)·exp(−m/T)` — exponent of a difference. `j` is bound by the sum; `i` is free.
- `exp(−m/T)` does not depend on `j`, so it factors out of `Σⱼ`; it is nonzero, so it cancels.
- Every relation shown is an equality in exact arithmetic (no `≈`).
- Numerical case (Python `decimal`, 50 digits, `z = [1, 2, 3]`): max |row1 − row2| = 3E-50,
  max |row1 − row3| = 1E-50 at T = 1; 3E-50 at T = 0.5; 2E-50 at T = 2. Row 1 at T = 1 is
  `[0.09003057317038045799…, 0.24472847105479765247…, 0.66524095577482188952…]`, consistent with
  case A's float values.

## Algebra corrections applied

None needed. Narration edit: "e to the z over T" → "e to the z-i over T", to match the subscript on screen.
