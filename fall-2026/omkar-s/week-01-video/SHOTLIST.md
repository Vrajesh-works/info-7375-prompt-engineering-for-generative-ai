# SHOTLIST — max-subtraction-softmax

Every slot is filled by the pipeline (Manim, `scenes.py`). No human-supplied media, no stills, no AI video, no screen recordings.

| Beat | Type | Scene | Slot | What the viewer watches |
|---|---|---|---|---|
| B00 | MANIM | `B00_TheLine` | `manim/B00.mp4` | Real `probabilities()` excerpt; max-subtraction lines highlight; the question |
| B01 | MANIM | `B01_NaiveRoute` | `manim/B01.mp4` | Scores → e^score weights → total → probabilities (plain recipe) |
| B02 | MANIM | `B02_ShiftedRoute` | `manim/B02.mp4` | Scores slide right, −3 applied, new weights, new total, same probabilities |
| B03 | MANIM | `B03_WhyItCancels` | `manim/B03.mp4` | ÷ 20.085537 arrows from each plain weight and total to the shifted ones; fraction with e³ struck out |
| B04 | MANIM | `B04_Overflow` | `manim/B04.mp4` | +1000 scores; real OverflowError; exponent axis with the 709.78 ceiling; dots slide back to −2, −1, 0 |
| B05 | MANIM | `B05_LessonTest` | `manim/B05.mp4` | [1000,1000] → [0,0] → [1,1] → [0.5,0.5]; real assertion + `test_02 … ok` |
| B06 | MANIM | `B06_Rounding` | `manim/B06.mp4` | Two 17-character floats, last digit boxed |
| B07 | MANIM | `B07_Boundary` | `manim/B07.mp4` | [0, −1000] → [1.0, 0.0]; log-scale axis with the float floor; true p drops to 0.0 |
| B08 | MANIM | `B08_Recap` | `manim/B08.mp4` | Three recap lines; sources + disclosure card |
