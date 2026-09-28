# SHOTLIST: seed-repeatable-not-correct

| Beat | Type | Source | Scene | Audio (s, with holds) | Fill |
|---|---|---|---|---|---|
| B00 | GRAPHIC: intro card (what this video explains) + seed freeze | Manim | `B00_Intro` | 19.67 | scenes.py (user-requested opener) |
| B01 | GRAPHIC: lottery + hook | Manim | `B01_Lottery` | 33.88 | scenes.py (box widths from seeded_sampler.softmax) |
| B02 | GRAPHIC: two recorded runs + stamp | Manim | `B02_TwoRuns` | 37.46 | scenes.py reads evidence/run1.txt, run2.txt |
| B03 | GRAPHIC: sticky note, dot grid, inputs, stamp strike | Manim | `B03_Twist` | 46.69 | scenes.py (real draw sequence, run100.txt) |
| B04 | GRAPHIC: mock chat + badge strike | Manim | `B04_Chat` | 25.84 | scenes.py (labelled illustration) |
| B05 | CARD: boundary statement | Manim | `B05_Boundary` | 17.99 | scenes.py |

No pantry media, no Remotion beats, no slates. Audio order: generate_audio_kokoro.py → pad_holds.py → cues.py.
