# REVIEW-LOG — watch and revise

The course video guide asks for *"one review/revision record"*: a timestamp, the problem, and
the requested fix. These are the problems **Akshit reported after watching the review cut**,
in their own words, with what changed and how it was checked. Organized by Claude Code from the
session record.

| When | Beat / time | Problem as reported | Fix | Checked by |
|---|---|---|---|---|
| 2026-09-27 | B03 · 00:00:52.8 | "there is overlapping text with the title" (screenshot) | `CONSTRUCTED` banner moved from `top: 66` to `top: 120`, clear of the title line | re-sampled the same timestamp |
| 2026-09-27 | B00 | header should greet students in another language; remove "reading chapter 1" | greeting *"Kia ora, students"*; running line removed | frame read |
| 2026-09-27 | B02 | "audio is fast while video is taking time to match that speed" | every reveal cued to the spoken word (`mp3/words.json`); step 4 had lagged by **2.56 s** | cue times printed against the transcript |
| 2026-09-27 | B05 | "keep smooth transition effects… more visual effects" | bars move through all 601 real steps; dashed corpus targets, live loss curve, leader glow, truth outline | step-50 frame checked equal to row 50 of `code/trajectory.json` |
| 2026-09-27 | B07 | "the graph is not correctly being created" | real 601-step curve, log-scale x-axis, y ticks, progressive draw, zoom inset | frame read; labels checked for collisions |
| 2026-09-27 | B11 | say it was created by Akshit Verma for INFO 7375 and the subject | author-credit card; narration says the same | frame read |
| 2026-09-27 | all | add captions | 100 captions from the aligned narration, burned in; `captions.srt` sidecar | inside the safe area, no collisions |
| 2026-09-27 | all | remove the footer (e.g. "B00 GRAPHIC VIDEO") | built with `ART_BURNIN=0`; also removes the timecode | frame read |

Found during these fixes, not reported by the viewer: B01's correction had never fired, so the
summary beat displayed the misconception. Fixed and timed to land on the spoken "followed".
