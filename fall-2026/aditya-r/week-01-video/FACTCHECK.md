# FACTCHECK — A Chatbot Is a Loop. (Week 1, Aditya Raj)

Status: checked 2026-09-27 by Claude Code (Claude Opus 5.5) for Aditya Raj; pending Aditya's own read-through.
Mechanical check: `evidence/verify.py` — hashes, full re-run, every on-screen and spoken number (51/51 PASS on 2026-09-27, including a fresh re-run of every experiment; output in evidence/verify-output.txt).

Recorded evidence = `evidence/runs/*.json` (SmolLM2-135M-Instruct @12fd25f7, local CPU). "p" = the model's own softmax probability.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|------|---------------------------|---------|---------------------|-----|
| 1 | B00 | The small model answered "The capital of France is Paris." in 8 passes | PASS | runs/france.json `answer`, `passes` | Labelled "SmolLM2, not Claude" on screen |
| 2 | B00 | The ask was made to Claude Code (Opus 5.5), which ran the model | PASS | This build; model chip shows the model that did the work | Pilot showed a Claude-styled answer; corrected |
| 3 | B01 | A chatbot predicts one token in a loop; it does not look answers up | PASS | Mechanism shown in every run (one forward pass per appended token). Scope: products with search/tools paste retrieved text into the same document; generation is still this loop | Narration kept general |
| 4 | B02 | A probability for every possible next token — "all forty-nine thousand" | PASS | softmax over the vocabulary; `vocab_size` = 49,152 | Spoken as "forty-nine thousand" |
| 5 | B03 | The model sees one document: system line, question, "assistant", blank | PASS | runs/france.json `chat_template_text` (verbatim on screen), 37 tokens | — |
| 6 | B04 | Pass 1: "The" 83%, "Paris" 4% | PASS | france step 1: The 0.8312, Paris 0.0415 | — |
| 7 | B05 | Eight passes build "The capital of France is Paris." | PASS | france steps 1–8 `chosen` | Labels never round p<1 to 100% |
| 8 | B06 | End-of-turn token wins pass 8 with 37% | PASS | france step 8 top: <\|im_end\|> 0.373 | — |
| 9 | B07 | With the stop token banned the loop kept writing; it "wanted to" stop at 37% and later 51% | PASS | runs/no_stop.json: <\|im_end\|> was top at pass 8 (0.373) and pass 44 (0.5137) | "never stops" reworded: capped at 60 passes |
| 10 | B07 | The model wrote Paris has "approximately 2.5 million people" | PASS | no_stop.json `continuation` | — |
| 11 | B07 | Official count ≈ 2.1 million (2,113,705) | PASS | INSEE, *Populations de référence 2022 — Ville de Paris* (Jan 2025), p.1 | — |
| 12 | B08 | Asked who wrote Middlemarch, the model said "Samuel Richardson" | PASS | runs/middlemarch.json `answer` | — |
| 13 | B08 | It was George Eliot (1871–72) | PASS | Project Gutenberg eBook #145: "Eliot, George, 1819-1880"; "a novel published in 1871-1872" | Britannica returned 403; Gutenberg used |
| 14 | B08 | At the name, the top guess had 16% | PASS | middlemarch pass 9 top: " Samuel" 0.1598 | — |
| 15 | B09 | " George" was 8th in line at 3% | PASS | middlemarch pass 9 top-10: " George" rank 8, 0.0313 | — |
| 16 | B09 | Forced in, the next pass puts " Eliot" on top at 43% | PASS | runs/force_george.json pass 10 top: " Eliot" 0.4298 | Probabilities shown are the model's own, before forcing |
| 17 | B10 | Chatbots usually sample; Claude's default is temperature 1 | PASS | Anthropic Messages API docs, `temperature`: "Defaults to `1.0`." (accessed 2026-09-27) | Worded as Claude's default, not all chatbots' settings |
| 18 | B10 | 200 runs, one seed each; 4 named George Eliot | CORRECTED | runs/sample.json (regex: 5) + sample_review.json (manual: seed 42 only mentions her) | 5 → 4 after manual review; outlined dot shows the 5th |
| 19 | B10 | All four invented facts: a Nobel Prize, a Pulitzer | PASS | sample_review.json: seed 9 Nobel, 186 Pulitzer 1885, 127 "1870", 149 "(1811-1885)". Nobel Literature first awarded 1901; Pulitzers first awarded 1917, fiction for American authors (Wikipedia; nobelprize.org and pulitzer.org returned 403) | Weaker source noted |
| 20 | B11 | P(answer) = product of per-pass probabilities | PASS | Chain rule of probability; exact for any sequence | — |
| 21 | B11 | Model rates "Samuel Richardson" ≈ 11× more likely than "George Eliot" | PASS | runs/paths.json: 0.0014319 / 0.000126213 = 11.35 | — |
| 22 | B12 | We measured a small open model, not Claude; Claude's probabilities are not visible to us | PASS | Scope of the evidence | — |
| 23 | B12 | Anthropic's docs list a stop reason called end_turn | PASS | "Stop reasons and fallback": end_turn "Indicates Claude finished its response naturally." | Was "the same stop" — overclaimed; reworded |
| 24 | B12 | The loop does not explain why the probabilities are what they are | PASS | Pretraining and attention are separate Chapter 1 concepts (assignment's own concept list) | — |
| 25 | B13 | A real answer from Claude Opus 5.5 on 2026-09-27; it says George Eliot and names "Ann" as its least-sure word | PASS | evidence/claude-response/response.json + screenshot (SHA-256 recorded); run by Aditya in a fresh claude.ai chat | Date = day it was run (no timestamp in screenshot) |
| 26 | B13 | Her name is recorded as Mary Ann, Mary Anne or Marian (caption) | PASS | Wikipedia, "George Eliot": "Mary Ann Evans (…; alternatively Mary Anne or Marian)" | — |
| 27 | B13 | The "least sure" report is generated text, not a readout of Claude's probabilities | PASS | Follows from the mechanism; Claude's probabilities are not exposed in claude.ai (see row 22) | Worded as "can't check it against them", not "it is wrong" |
| 28 | BVDT | Recap lines | EXEMPT | Generated from rows 1–21 by fill_props.py | — |
| 29 | BHTF | Suggested prompt + two checks | EXEMPT | Handoff | — |
