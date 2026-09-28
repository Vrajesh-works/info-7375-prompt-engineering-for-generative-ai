# DEFENSE-NOTES — how to explain every part of this video

The course may ask me to explain any part of the video, the beat sheet, or the build.
These notes are the answers, in the order a TA is likely to ask. Each answer points to
the file that backs it.

---

## 1. The concept in two sentences

A chatbot is trained in two stages. **Pre-training** nudges it toward the next piece of
text that really came next. **Preference tuning** nudges it toward the reply a human
picked. Neither stage is given an answer key, so when the people picking can't check the
facts and prefer the reply that *sounds* surer, the training moves toward a confident
wrong answer. The code works fine; it is simply following the votes.

Source: Chapter 1, Part 1, "Where the numbers come from", and Figure 1.3.

## 2. Why this concept (and not temperature, seed, etc.)

- It is on the assignment's list ("Why preference tuning can prefer a confident wrong
  answer").
- Nobody else in the posted cohort had picked it. Temperature, seed, max-subtraction and
  expected-vs-observed each already had 3–5 videos.
- It needs no maths beyond "bigger score → bigger chance", so a first-year student can
  follow it. It is also the most practical Chapter 1 idea for anyone using a chatbot:
  sounding sure is not evidence.

## 3. What the toy actually computes (walk through `evidence/preference_toy.py`)

1. Two replies with scores `[0.0, 0.0]`. The chapter's own `probabilities()` turns the
   scores into chances: `[0.5, 0.5]`.
2. For each of 1,000 votes, `rng.random() < 0.3` decides whether this reviewer can check.
   `rater_pick()` returns 0 (Canberra) if they can check, else 1 (Sydney, the surer
   reply). **This rule is constructed** by us; it is not data.
3. `nudge(scores, picked, learning_rate)` computes
   `step = 0.02 * (1 - chance of the picked reply)`, adds `step` to the picked score and
   subtracts it from the other.
4. After 1,000 votes (336 for Canberra, 664 for Sydney) the chances are **32.6% / 67.4%**.

Rerun it: `python3 preference_toy.py`. It prints exactly `preference_toy_output.json`, and
the test `test_recorded_output_matches_a_fresh_run` checks that.

## 4. "Why does `step` have `(1 - chance)` in it?" (the one bit of maths)

For two replies, the chapter's `probabilities([a, b])[0]` equals the logistic function
σ(a − b). If we want to raise log(chance of the picked reply), the slope with respect to
the picked score is `1 − chance`. So `nudge` is one gradient-ascent step on
log(probability of the picked reply). It moves more when the pick was a surprise.

This is the same loss real reward models are trained with on pairwise comparisons,
−log σ(r_winner − r_loser) (Bradley–Terry; Ouyang et al. 2022). In our toy, one pair of
numbers plays both roles: it is the "reward model" and the "policy". Real systems keep
those separate (see §7).

## 5. Why does the learned chance land *near* the vote share?

If the chance of Canberra were p and Canberra got a fraction v of the votes, the average
nudge is zero when v(1 − p) = (1 − v)p, which means **p = v**. So the scores drift until the
chance matches the vote share, and then they jiggle around it because each step has a
fixed size. The truth doesn't appear anywhere in that equation.

It is **near, not equal**. My first test demanded a gap under 0.03 and failed at share
0.6 (0.6632 vs 0.633; see `evidence/preference_toy_tests_output_FIRST_RUN_FAILED.txt`).
With a fixed step the scores act like a moving average of roughly the last hundred votes,
so the final number jiggles. The tolerance was then **loosened to 0.05, and that holds for
seed 7 only.** An independent review ran more seeds, and so did I (`seed_spread.py`, seeds
0–499):

- The gap to the vote share is typically 0.01–0.02; the 95th percentile is 0.04–0.06 and
  the maximum is 0.10.
- At 30% able to check, the wrong reply is favoured in **500 of 500** seeds (learned chance
  25–35%). At 70% the correct one wins in 500 of 500.
- At 50% it's a coin flip: the wrong reply is favoured in 54% of seeds, and the favourite
  matches the vote majority in only 63%. So "the favourite is the reply with more votes"
  is **not** a general law near 50/50.

What the video claims ("near the share of votes"; the wrong reply wins when most can't
check) holds across seeds. The exact seed-7 numbers are one typical run.

## 6. What is real and what is constructed

| On screen | Status |
|---|---|
| The two replies, the Canberra question, the "3 in 10 can check" rule | **Constructed**; labelled "CONSTRUCTED EXAMPLE" / "CONSTRUCTED ASSUMPTION" |
| 336/664 votes, 32.6%/67.4%, checkpoints, the sweep 22.5/42.4/66.3/81.7% | **Real output** of our script, seed 7, reproducible |
| The code in B03 and the rule line in B04 | **Real source**, exported with `inspect.getsource` (docstring trimmed and labelled) |
| `probabilities()` | The **course's own** function, imported from `lessons/01-.../main.py` |
| Hosking et al. 2023 quotes (and the Sharma footer) | **Verbatim** from the raw arXiv abstracts (`evidence/source_abstracts_2026-09-27.txt`) |
| The "Your turn" composer | **Reconstructed interface**, with a suggested prompt and **no response** |
| Any Claude response | **None shown** |

## 7. The one thing this does not establish

**It shows that a confident wrong answer *can* win. It does not show how *often* that
happens in real training.** Our reviewers and their rule are made up. The toy also says
nothing about how Claude was trained, and it skips the real pipeline: real systems train
a separate reward model on comparisons and then optimise the chatbot against it with
reinforcement learning (Ouyang et al. 2022). For *real* evidence the video cites Hosking,
Blunsom & Bartolo 2023 (arXiv:2309.16349). They found that "the assertiveness of an output
skews the perceived rate of factuality errors", and they offer *preliminary* evidence that
training on human feedback "disproportionately increases the assertiveness of model
outputs". That is the confident-vs-hedged effect itself. Sharma et al. 2023 (sycophancy)
appears only as a *related* finding. Both are findings about those authors' experiments,
not rates I can apply to any model.

## 8. Likely questions and short answers

- **"The assignment says use what `main.py` prints. Where is that?"** `main.py` computes
  only Part 2's softmax and sampler, so it prints nothing about preference tuning, which is a
  Part 1 concept. The toy imports its `probabilities()` unchanged, and B03 shows `main.py`'s own
  output for [1, 2, 3] (0.090, 0.245, 0.665). The 50/50 start is the same equal-scores
  property the chapter tests with [1000, 1000] → [0.5, 0.5]. The concept itself is on the
  assignment's list: "Why preference tuning can prefer a confident wrong answer".
- **"A real model already knows Canberra. Isn't the example unrealistic?"** Yes, on purpose.
  The toy starts at 50/50 and leaves out pre-training (said on screen in B05) so the voting
  step is the only thing moving. The point is the mechanism. It doesn't claim real models
  get this particular question wrong.
- **"3 in 10 can check, so why 336 votes and not 300?"** Each vote is a random draw with
  chance 0.3; 336 is what seed 7 produced (said on screen).

- **"Isn't the result obvious from your assumption?"** Partly, and that is the point.
  The update rule has no answer-key input, so the only thing that can move it is who
  voted. The sweep in B06 shows it directly: the answer is fixed in every run, and the
  outcome follows the vote share across 50%.
- **"Why seed 7?"** It matches the course's `sample()` default. A seed makes the run
  repeatable. It does not make the result true (that's a different Chapter 1 idea).
  `seed_spread.py` shows seed 7 is a typical run, not a lucky one.
- **"Why 1,000 votes and step 0.02?"** They give a smooth curve that settles near the
  vote share. They are illustrative choices, not tuned to any real system.
- **"Why does the voice say 'reviewers' when the chapter says 'raters'?"** The Kokoro
  voice's "raters" was transcribed as "raiders" every time, and respelling didn't help
  (FRICTIONAL.md). The screen says "the chapter calls them 'raters'".
- **"Is 'preference tuning' the same as RLHF?"** RLHF is one way to do it (Christiano et
  al. 2017; Ouyang et al. 2022). The chapter uses the general term, and so do I.
- **"Why is 42.4% shown as 'forty-two' but 22.5% as 'twenty-two'?"** The narration rounds
  and says "near". The screen shows the exact recorded value.
