# FRICTIONAL — Week 1 Explainer Video

## Entry 1

**Date and what I was working on:** 2026-09-23 → 2026-09-24. Reading the assignment, choosing a concept, setting up the toolkit, generating the token evidence.

**I tried / expected:**
Chose "the unit is a token, not a word — and why that breaks letter-counting prompts" (Chapter 1, Part 1, §"One question, asked over and over").
Prediction: I thought `strawberry` would be split into its letters, one piece per letter. I did not think about the leading space at all.

**What happened:**
- In `How many r's are in strawberry?`, ` strawberry` is **one** token (ID 101830 in `o200k_base`). Bare `strawberry` is three (`st|raw|berry`).
- The chapter's `unbelievable` "might arrive in three pieces" holds only without a leading space: `un|bel|ievable` = 3, ` unbelievable` = 1.
- The first version of the assignment text I read named `fall-2025/first-name-last-initial/week-01-video/`; the repo uses `fall-2026/revan-c/`. The assignment text was later corrected to `fall-2026/` (seen 2026-09-27). Used `fall-2026/revan-c/week-01-video/`.
- Assignment's policy note cites "instructor decisions, item 7"; `docs/instructor-decisions.md` only has items 1–6 (item 6 still calls explainers optional). Followed Canvas, which lists this as 25 points.
- Machine had only Python 3.14; Brutalist pins `manim<0.19`, which I did not expect to install on 3.14.
- `./setup --install` (brutalist.art commit `6a8380a`) installed everything, then exited before the readiness table: its ElevenLabs guard flagged the toolkit's own `youtube/brutalist/...` files (e.g. `claude-liam-brutalist-command-setup/beat_sheet.json`).
- `./art smoke` failed at GATE 0: `[kokoro] REFUSED: metadata.slug must be a filename, not a path`. The fixture's slug is `_smoke`; `build_safety.py:186` requires the first character to be a letter or digit.
- No LaTeX (`pdflatex`/`dvisvgm`) — only needed for Manim equation beats; this video has none.

**What I did:**
- Wrote `evidence/tokenize_examples.py` (tiktoken 0.14.0) and saved its output as `evidence/tokens.json`; the video uses only numbers from that file.
- Installed Python 3.12 with Homebrew and put the toolkit in a project `.venv` instead of running `./setup --install` against the system Python (the script uses `pip install --break-system-packages`).
- Installed `ffmpeg`, `cairo`, `pango`, `pkg-config` via Homebrew for rendering.
- Since setup's table never printed, checked each dependency by hand: imported PIL 10.4.0, manim 0.18.1, faster_whisper 1.2.1, kokoro_onnx, mutagen; `runtime/scripts/setup_smoke_kokoro.py` → "kokoro synth OK — mean_volume -21.8 dB"; `runtime/remotion/node_modules` present. Did not edit the toolkit to make the smoke test pass; my own slug (`tokens-not-words`) passes the check.

**What Claude or another person contributed:**
Claude (Claude Code) located the Chapter 1 text and the tokens passage in the course repo, suggested the concept shortlist, wrote the tokenizer script, and ran the installs.
I chose tokens over the other options (the next-token loop, the Part 2 sampling concepts) because I wanted to know how the model actually reads words. Claude first recommended a Part 2 concept (because `main.py` prints real numbers for those); I rejected that and chose Part 1. Among the Part 1 options, Claude recommended tokens and I accepted.

**What I understand now / still do not understand:**
In my words: there is no R in the number 101830, so how would you count it? It would only work if there were a code number for R itself. Afterwards I saw that this is exactly what spelling it out does: each ` r` becomes its own token, 428, three times (B06).
Still open: Claude's own tokenizer is not public, so I cannot show Claude's actual split; I do not know whether it also keeps ` strawberry` as one token.

**Evidence and next step:**
`evidence/tokens.json`; `python3 evidence/tokenize_examples.py`. Next: finish Brutalist install, write `beat_sheet.json`.

## Entry 2

**Date and what I was working on:** 2026-09-24. First full build of the video (`./art run`, then `./art final`).

**I tried / expected:**
I did not know what to expect from the build.

**What happened:** (each item is a gate message from the build log)
- First `./art run`: "nothing to render". The Manim scenes were never picked up; run.sh only finds classes written literally as `class B02_Name(Scene)`, and mine inherited from a helper class.
- GATE A: `FileNotFoundError ... evidence/tokens.json`. The gate copies `scenes.py` alone into a temp dir, so relative paths break. Then `NameError: name 'BOLD' is not defined` (the gate's stub Manim has no `BOLD`/`ITALIC`).
- GATE A on B06: "shapes never change", because only colours changed.
- GATE W: "CHAPTER-ON-SLIDE". The toolkit forbids the word "chapter" on screen.
- GATE B: heading, footnote and question text outside the title-safe area.
- GATE T: "terracotta accent #D97757 on cream 2.74:1 < 4.5:1". A real contrast failure for my orange text.
- GATE V: B07 edge-bleed and B01 underfill. After every gate passed, I sampled frames by hand and found B07's first card covering the heading, which no gate had caught.

**What I did:**
- Switched to a `Timeline` helper object so every scene is `(Scene)`. Added `TOKENS_REEL_DIR` so scenes can find the evidence from any directory. Used `weight="BOLD"` strings.
- B06: the three ` r` tokens now lift out of the row and arrows link them to the "428, three times" line (a real motion, not decoration).
- Renamed B05's heading to "Checking the course reading" and cited the reading by title.
- Text accent changed to `#A44A32` (5.6:1); `#D97757` kept only for fills and arrows.
- Tried `ART_STRICT=0` to get past B01's underfill; `./art final` ignores it, so I abandoned that and fixed B01 properly (faster typing plus two context cards).
- Measured B07's card edges in code and re-placed them. Final: GATE V 0 BLOCKER / 0 MAJOR, GATE T PASS, 143.9 s.

**What Claude or another person contributed:**
Claude wrote `scenes.py`, diagnosed each gate failure and applied the fixes.
After watching the first cut: I liked the content, but the voice felt robotic and the narration needed more flow. I accepted the content and the visuals. The voice was not changed; the free pipeline only offers Kokoro `am_onyx` and `af_bella`.

**What I understand now / still do not understand:**
The build is gated: Brutalist refuses to render until each check passes, and a passing gate still did not catch the B07 overlap. Only looking at the frames did.
Still open: the B00/B09 composer UI (toolkit chrome) showed a model label ("Fable 5 · High") that I did not choose. It is part of Brutalist's `ClaudeComposerAsk` skin, not a record of which model ran the tokenizer. (Resolved in Entry 3.)

**Evidence and next step:**
`_qc/REPORT.md` (0 BLOCKER / 0 MAJOR), `TYPECHECK.md` (PASS), `tokens-not-words.mp4`. Next: Revan reviews the cut; write README, SOURCES, BUILD-PROMPT; push to `fall-2026/revan-c/week-01-video/`.

## Entry 3

**Date and what I was working on:** 2026-09-25 → 2026-09-27. Watching the cut, testing the prompts in real chat apps, requesting revisions, and checking the video against the assignment and the prerequisite guides.

**I tried / expected:**
Ran the video's two prompts myself: "How many R's in strawberry? Show me exactly what the model receives." and the B09 spell-it-out prompt.
Prediction: I assumed Claude would get 3 right, because models are really good now.

**What happened:**
- Claude (screenshot `evidence/claude-strawberry-screenshot.png`): answered **3 R's** correctly, but said strawberry is "not as 7 separate letters (s-t-r-a-w-b-e-r-r-y)". The word has **10** letters, and it listed all ten in the same sentence. It also said the word is "likely" one or two tokens, which is a guess about its own input. The spell-out prompt gave 10 numbered lines and 3 r's (lines 3, 8, 9).
- ChatGPT (same two prompts, extra comparison only; the course is Claude-only, so it is not in the video): also answered 3. It read "what the model receives" as hidden system instructions and showed my message as plain text, not tokens. It trusted the counting step least; Claude trusted the spelling step least.
- A check against `prerequisites/brutalist-video.md` found four problems in my cut: the synthetic voice was never disclosed; the reconstructed Claude UI showed a model chip "Fable 5 · High"; B02 said the eight IDs are "everything the model receives", which ignores system prompts and role markers (Chapter 1: roles are text in the document); and the guide asks for a 1080p final, while mine was 4K.

**What I did:** (changes I requested after watching)
- Greeting "Namaste, Liam" → "Hi, Liam"; handle @NikBearBrown → @RevanChonnad on B00, B08, B09; outro now says "At Revan Chonnad". Brutalist's `ClaudeTitleOutro` hardcodes @NikBearBrown, so B10 became my own Manim card instead of an edit to the toolkit.
- Narrator line "Liam, in for Bear" → "Hi, this is Liam, a synthetic voice, narrating for Revan Chonnad."
- Composer model chip → "Reconstructed UI".
- B02 → "That row of eight numbers is how your question reaches the model."
- Final exported with `--height 1080 --out final/` (1920×1080, 144.8 s). Speech-to-text of B00 heard my surname as "Chauned"; I listened and the pronunciation is acceptable.
I did not have a strong view on which change mattered most for understanding. The disclosure, "Reconstructed UI", B02 and 1080p changes came from Claude's audit against the guides, and I approved them. The greeting, handle and name changes were my own requests and are about identity, not understanding.

**What Claude or another person contributed:**
Claude compared the two screenshots, found the "7 letters" error, audited the cut against the assignment and prerequisite guides, and applied the requested changes. I ran both chat tests myself.
I accepted all four audit fixes. I followed Claude's advice to keep ChatGPT out of the video because of the course's Claude-only rule. I have not yet decided whether to add my Claude screenshot as a scene.

**What I understand now / still do not understand:**
Claude counted correctly but described its own input wrongly ("7 letters"), so a correct answer does not mean the explanation around it is correct.
Still open: how Claude gets from a token number to the letters inside it. My guess is that it might run Python code to spell the word. I have not checked this, and nothing in this video tests it.
Also open: I ran each prompt once per app, so I cannot tell whether "7 letters" is a repeatable error or one sample.

**Evidence and next step:**
`evidence/claude-strawberry-screenshot.png`; `_qc/REPORT.md` (0 BLOCKER / 0 MAJOR); `TYPECHECK.md` (PASS); `final/tokens-not-words.mp4`. Next: README, SOURCES, BUILD-PROMPT; push to `fall-2026/revan-c/week-01-video/`.
