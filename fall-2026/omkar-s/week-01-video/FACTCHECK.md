# FACTCHECK — max-subtraction-softmax

Status: every row checked by Claude Code against the saved evidence files on 2026-09-24. Omkar Salian must re-check and sign off before submission (see FRICTIONAL.md).

Evidence files (all in `evidence/`): `main_py_output.txt` (the course's `main.py`), `tests_output.txt` (the lesson's 6 unit tests), `max_shift_output.txt` (output of `max_shift_evidence.py`, which imports the course's `probabilities()`). Python 3.14.2, course commit `e6c6c49`.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | B00 | The course's `probabilities()` subtracts the max score before exponentiating | PASS | `main.py` lines `peak = max(logits)` and `math.exp((x - peak) / temperature)` | — |
| 2 | B00 | Code on screen is the real function | PASS | Verbatim except input checks elided and one line wrapped; both labelled on screen | — |
| 3 | B01 | Scores [1, 2, 3] are chosen, not model output | PASS | Chapter 1: "In this example I have chosen them; no model produced them." | — |
| 4 | B01 | Plain weights 2.718282, 7.389056, 20.085537; total 30.192875 | PASS | `max_shift_output.txt`, section A, naive weights | — |
| 5 | B01 | Probabilities 0.0900, 0.2447, 0.6652 ("about sixty six and a half percent") | PASS | `main_py_output.txt`: 0.09003…, 0.24472…, 0.66524… | — |
| 6 | B02 | Shifted scores −2, −1, 0; weights 0.135335, 0.367879, 1.000000; total 1.503215 | PASS | `max_shift_output.txt`, section A, shifted; also Chapter 1 text | — |
| 7 | B02 | Both routes give the same probabilities | PASS | `max_shift_output.txt` section A (agree to rounding; qualified in B06) | — |
| 8 | B03 | Each shifted weight = plain weight ÷ e³ ≈ 20.085537; total likewise | PASS | exp(3) = 20.0855369…; 30.192875 / 20.085537 = 1.503215; 2.718282 / 20.085537 = 0.135335 | — |
| 9 | B03 | 20.085537/30.192875 = 0.6652 and 1.000000/1.503215 = 0.6652 | PASS | 0.665241 and 0.665241 (4-dp display) | — |
| 10 | B03 | The common factor cancels | PASS | Chapter 1 derivation, "The common factor cancels." | — |
| 11 | B04 | `math.exp(1003)` raises `OverflowError: math range error` | PASS | `max_shift_output.txt`, section B (verbatim) | — |
| 12 | B04 | Largest float ≈ e^709.78 | PASS | `max_shift_output.txt`: `log(largest float) = 709.7827` | — |
| 13 | B04 | [1001,1002,1003] gives exactly the same probabilities as [1,2,3] | PASS | `max_shift_output.txt`: `A == B exactly: True` | — |
| 14 | B05 | Lesson test: [1000, 1000] → [0.5, 0.5], test passes | PASS | `test_main.py` test_02; `tests_output.txt`: `test_02 … ok` | — |
| 15 | B06 | Plain vs shifted outcome 0: 0.09003057317038045 vs 0.09003057317038046 | PASS | `max_shift_output.txt`, section A | — |
| 16 | B06 | They differ in the 16th significant digit | CORRECTED | First draft said 17th; counted: 9003057317038045 is 16 significant digits | Narration and on-screen label say "sixteenth" |
| 17 | B07 | probabilities([0, −1000]) returns [1.0, 0.0], second value exactly 0.0 | PASS | `max_shift_output.txt`, section D + `is exactly zero: True` | — |
| 18 | B07 | exp(−1000) is about 5.1e−435 (spoken: "about ten to the minus four hundred thirty four"); smallest positive float 5e−324 | PASS | `decimal` at 30 digits: 5.07596e−435, i.e. 10^−434.29; `max_shift_output.txt`: `smallest positive float: 5e-324` | — |
| 19 | B07 | One passing test is not proof of "numerically stable" for every input | PASS | Chapter 1: "Keep the tested claim narrower than the slogan 'numerically stable.'" | — |
| 20 | B08 | The voice is synthetic | PASS | Kokoro `af_bella`, `generate_audio_kokoro.py` | — |
