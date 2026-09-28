# FRICTIONAL: Inside One Prediction Step

Honest log of what got in the way, what I tried, and what I did instead.
Drafted by Claude Code from the build session; reviewed and edited by Chethan.
<!-- TODO(Chethan): read every entry, correct anything that doesn't match your
     experience, and add your own reactions. This log is graded as yours. -->

## 2026-09-26: Which rules, and whose name on it?

- **Friction:** The toolkit's own submission guide is for Humanitarians AI fellows (4K, a 9:16 vertical version, videos on Drive), not for this course. Its `ai-explainer` skill also hard-codes "Liam, in for Bear" as the narrator line and an `@NikBearBrown` outro, which would credit my assignment to someone else's channel.
- **Did instead:** Followed the course deliverables. Kept the repo's style and structure, but the opening names me and says the voice is an AI narrator (Kokoro), and the outro card credits me.

## 2026-09-27: Two builds thrown away before this one

- **Friction:** I finished two complete review cuts before this video. The first worked scaled dot-product attention through by hand. The second covered the course's Subtopic 5 using hand-picked toy vectors. Neither matched what I wanted, so I deleted both entirely and wrote a precise brief (items 1–9) instead.
- **What carried over:** Lessons, not files. The toolkit's checks had stopped earlier renders repeatedly (text a hair outside the safe area, pale fills read as low contrast, a silent outro with no audio flag). This time every scene was audited before the 4K render.

## 2026-09-27: "Don't add numbers" vs. "build it by hand"

- **Friction:** My brief says to keep every fact exactly as stated and add no numbers. It also says the last step is small enough to build by hand with [1, 2, 3]. You can't show a hand-built softmax without its output.
- **Decision:** I approved exactly two derived values: softmax([1, 2, 3]) = 0.09 / 0.24 / 0.67 (from actually running the code) and 36 + 59 = 95. Everything else that could look like data is drawn without values and labelled schematic, illustrative, or "not to scale": the bank vectors, the attention arrow thicknesses, the parameter bar, and the logit bars.

## 2026-09-27: Repo spine vs. my closing line

- **Friction:** The repo's fixed ending is verdict → "Your turn" prompt → silent outro. My brief says item 9 is the closing line.
- **Decision:** The verdict beat ends on "The model decided X because Y is a story, not a measurement." The Your-turn prompt and title card follow, per the repo.

## 2026-09-27: Preview collisions

- **Friction:** The first low-res previews had overlaps:
  - B02: a citation sat on top of a lane title.
  - B03: the 12,288 label, the position tags and the "≠" sign crowded each other.
  - B05: the query → weights row ran off the left edge.
  - B06: the parameter bar's label overflowed.
  - B10: the two "parallel pathway" arrows crossed, twice. Flipping the curve direction didn't fix it.
  
  The layout audit then flagged four labels just outside the safe area.
- **Did instead:** Three fix passes. For B10, replaced the curved arrows with explicit lines out to each side and down to 95.

## 2026-09-27: Longer than 3 minutes, then longer still

- **Friction:** The target was about 3 minutes. The measured narration came to 3 min 13 s, plus a 6 s title card. In this repo the audio is the clock ("duration is an output, never a target"), so the video can't be squeezed to fit.
- **Status:** Left as is for review. Adding the architecture section (B02A, 33.6 s; B02B, 15.3 s) after my review took it to 4 min 08 s. I chose the extra content over the 3-minute target. The "Your turn" beat (20.7 s) is the easiest cut if the length matters.

## 2026-09-27: Changing an example that isn't mine to change

- **Friction:** I asked for different examples everywhere, including the addition trace. The river/bank and dog/man examples were just illustrations. But 36 + 59 is the specific case the Anthropic 2025 paper actually traced, so replacing it with another sum would have credited the paper with a result it never reported.
- **Decision:** Swapped the illustrations freely: "Alice paid Bob" / "Bob paid Alice" for position, and "bat" after cricket vs after fruit for attention. For the paper's case, I chose to describe it as "a two-digit addition problem" and draw empty digit boxes instead of numbers.

## 2026-09-27: Rebalancing without shrinking

- **Friction:** I wanted more architecture without making the video shorter, and each architecture beat under 30 s. B02A was 33.6 s.
- **Did instead:** Tightened B03–B06 (the step-by-step walkthrough), about 53 s down to 42 s. Added the encoder–decoder detail as two beats (B02B, 16.7 s; B02C, 9.7 s). Trimmed B02A to 28.8 s. The final is 4 min 04 s.
