# FACTCHECK — one-word-same-answer

Status: checked 2026-09-27 by Weiting W (with Claude). Every figure below is recomputed by `analyze_responses.py` from `evidence/run*/responses.json`, which are verbatim transcriptions of the screenshots in `evidence/run*/screenshots/`. `scenes.py` asserts against `evidence/analysis.json` and refuses to render if a number drifts.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | B02 | The reading compares a one-sentence deck prompt with a one-word capital prompt | PASS | Chapter 1, "First prompts: the same experiment, one floor up", prompts 1 and 2 (verbatim prompt text) | — |
| 2 | B02 | In our runs, one-word answers all agreed; deck sentences did not | PASS | analysis.json: B distinct = 1 in both runs; D distinct = 4 in both runs | Worded as "in our runs", not as the chapter's claim |
| 3 | B03 | 4 new chats per prompt, first reply kept, no regeneration; Opus 5.5 Medium; 2026-09-27 | PASS | 24 screenshots (model label visible); responses.json procedure field | — |
| 4 | B03 | Incognito turns off Claude's memory | PASS | support.claude.com/en/articles/12260368 ("Starting an incognito chat won't use Claude's existing memory") | — |
| 5 | B03 | Personal preferences stayed on in both runs | PASS | Author's statement; recorded in both responses.json files | — |
| 6 | B04 | Run 1 free capital replies: 6 words each, same words, 2 distinct strings | PASS | analysis.json run1 A: words_each [6,6,6,6], overlap 1.0, distinct 2 | — |
| 7 | B05 | Run 2 free capital replies: about 30 words, 4 distinct, mention 1908 and 1927 | PASS | analysis.json run2 A: words 29–34 (mean 31.8), distinct 4, years_asserted [1908, 1927] | "like 1908 and 1927": 1908 appears in one reply, 1927 in all four |
| 8 | B05 | With the one-word rule, all four replies were "Canberra" (both runs) | PASS | analysis.json B: distinct 1, words 1 | — |
| 9 | B05 | Reason: one word leaves few likely continuations, so replies converge | PASS | Chapter 1, prompt 2 discussion ("fewer high-probability continuations to choose among, so the answers converge") | Shown as "the course reading's reason" |
| 10 | B06 | Canberra is the capital of Australia (checked outside the chat) | PASS | https://en.wikipedia.org/wiki/Canberra ("capital city of Australia"), checked 2026-09-27 | — |
| 11 | B06 | Deck replies quoted "about 225 bits", "about 2^225", "about 2^226" | PASS | analysis.json deck_size_phrases: run1 {225 bits, 2^226}, run2 {225 bits, 2^225} | Quoted verbatim, sans font so the caret shows |
| 12 | B06 | log2(52!) = 225.58 | PASS | analyze_responses.py: math.lgamma(53)/math.log(2) = 225.581… | — |
| 13 | B07 | Dates 1908/1927 and the "seven shuffles" claim are not verified here | EXEMPT | Narration states explicitly that these were not verified; they are shown only as things the replies asserted | Boundary, by design |
| 14 | B07 | Cause of short run-1 replies is not isolated (incognito may change more than memory) | PASS | support.claude.com/en/articles/12260368 note: incognito opens in the previous chat experience; run-1 and run-2 interfaces differ in screenshots | Stated as a scope limit |
| 15 | B08 | "four times ... four more times" (instructions to the viewer) | EXEMPT | An instruction for the Your Turn exercise, not a factual claim | — |


Editorial lines (no verification needed): "That feels like progress" (B00), "No format rule checked any of this. We did." (B06).
