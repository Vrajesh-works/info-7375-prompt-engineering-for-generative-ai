# SHOTLIST — typed work order (generated from beat_sheet.json)

| Beat | Lane | Source | Seconds | What the viewer watches |
|---|---|---|---:|---|
| B00 | remotion | ClaudeComposerAsk | 15.49 | Composer types the question (the student's question, not a Claude reply); Footer shows the real command and its real printed output: $ python main.py -> [0.0900, 0.2447, 0.6652] |
| B01 | remotion | BrutalistHesitantWriter | 9.92 | Writer types the three-line overview; Writer first types the misconception 'nudges the answer slightly', deletes it, types 'changes the weights, not the answer' |
| B02 | manim | B02TwoRoutes | 20.14 | Scores [1, 2, 3] appear, tagged 'constructed input (Chapter 1)'; Left column: each score flows through exp to 2.718, 7.389, 20.086; total 30.193; Right column: each score drops by 3 to -2, -1, 0, then exp to 0.135, 0.368, 1.000; total 1.503; Each column divides by its total; both morph into 0.0900, 0.2447, 0.6652 and a terracotta '=' joins them |
| B03 | manim | B03Cancel | 17.96 | Typeset identity exp(z_i - m) = exp(z_i) exp(-m); Direct weights multiply by exp(-3) = 0.0498 and visibly become the shifted weights (20.086 -> 1.000); Full fraction appears; exp(-m) in numerator and denominator is struck through in terracotta; Ratio bars: 20.086/7.389 and 1.000/0.368 both show 2.718 |
| B04 | manim | B04Overflow | 19.11 | [1000, 1000] tagged 'lesson test input (test_02)'; Left: math.exp(1000) -> real error line 'OverflowError: math range error' stamps in; A float ceiling line: exp(709) = 8.218e+307 fits, exp(710) OverflowError; Right: [0, 0] -> [1, 1] -> [0.5, 0.5]; Real unittest output: 'Ran 6 tests ... OK' |
| B05 | manim | B05Offset | 19.61 | [1, 2, 3] and [1001, 1002, 1003] stacked, tagged 'constructed input'; Direct route on the second row stamps OverflowError; Both rows slide down by their max and collapse onto the same [-2, -1, 0]; Gap brackets of 1 and 1 highlighted in terracotta; the 1000 offset fades as 'carries no preference' |
| B06 | manim | B06Boundary | 27.19 | Header 'What this does not establish'; [0, -1000] tagged 'constructed input'; true value 5.0760e-435 (Decimal) vs Python 0.0 for both routes; Underflow floor: exp(-745) = 5e-324, exp(-746) = 0.0; Direct minus shifted for [1,2,3]: -1.39e-17, 0.0, 1.11e-16 |
| BVDT | own | ClaudeVerdictArtifact | 9.02 | — |
| BHTF | own | ClaudeComposerAsk | 26.51 | — |
| BOUT | manim | BOUTTitle | 3.8 | Title restate 'Subtract the Max.' with terracotta period; author and course line beneath |
