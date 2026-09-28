# FRICTIONAL — what broke, what I tried, what I did instead

Dated entries. Everything here happened on this machine (macOS, Apple Silicon)
while building this submission. Nothing was smoothed over after the fact.

**Who did what.** The entries are written in the first person because this is my
log, but most of the diagnosis and fixing below was done by Claude Code working in
my terminal at my direction: reading error logs, finding root causes, and
applying fixes. The one exception is MacTeX's `sudo` install, which I ran myself.
SOURCES.md ("What Claude contributed") has the full split.

---

## 2026-09-14 — `./setup --install` failed: one bad package killed the whole install

Cloned `brutalist.art` and ran `./setup --install`. The readiness table came back
with 5 of 7 features blocked, including things with no obvious relationship to
each other — audio, captions, Manim, slates.

**What broke.** `pip install -r requirements.txt` is a single transaction.
`manimpango` needs the system `pangocairo` library via `pkg-config`, which was not
installed. That one build failure aborted the entire batch, so `kokoro-onnx`,
`Pillow` and `faster-whisper` were never installed either, despite having nothing
to do with Pango.

**What I tried.** `brew install pango`. That fixed `pangocairo` and `manimpango`
built — then the install failed again, differently.

**Lesson.** A single red row in that table can be one root cause wearing five
masks. I stopped fixing rows and started reading the first error.

---

## 2026-09-14 — Python 3.9 could not satisfy `kokoro-onnx` at all

**What broke.** `pip` reported `ResolutionImpossible`: `kokoro-onnx` requires
`onnxruntime>=1.20.1`, and `pip index versions onnxruntime` offered nothing above
`1.19.2`.

**Diagnosis.** The machine's `python3` is `/usr/bin/python3` — macOS
CommandLineTools Python **3.9.6**. `onnxruntime` ≥1.20 publishes no cp39 wheel, so
no resolution existed. The `setup` script hardcodes `python3`, so it was pinned to
that interpreter no matter what else was installed.

**What I did instead.** Created a project virtualenv on Homebrew's Python 3.11
(`python3.11 -m venv .venv`) — new enough for `onnxruntime`, old enough for
`manim<0.19`, which does not support 3.13+. Python 3.11 is the only version in the
intersection.

---

## 2026-09-14 — Anaconda silently broke every C build

**What broke.** Inside the venv, `pycairo` failed to build:

    ../meson.build:1:0: ERROR: Executables created by c compiler
    arm64-apple-darwin20.0.0-clang are not runnable.

Compiling a hello-world with plain `clang` worked fine, so it was not a broken
toolchain in general.

**Diagnosis.** Read the meson log. The build was linking against
`/opt/anaconda3/lib` and the produced binary was `missing LC_LOAD_DYLIB (must link
with at least libSystem.dylib)`. The shell auto-activates conda's `base`
environment, which exports `CC`, `CXX`, `CFLAGS`, `CXXFLAGS`, `CPPFLAGS`,
`LDFLAGS` pointing at conda's cross-compile toolchain wrappers. Meson obeyed `CC`
and produced binaries that could not run.

**What I did instead.** Unset those variables for the install:

    unset CC CXX CFLAGS CXXFLAGS CPPFLAGS LDFLAGS LDFLAGS_LD CC_FOR_BUILD CXX_FOR_BUILD

Every Python dependency then installed cleanly. **This is the single most
load-bearing line in the whole build** — without it nothing that compiles will
build, and the error message points at the compiler rather than at conda.

---

## 2026-09-14 — MacTeX cannot install from a non-interactive shell

**What broke.** `brew install --cask mactex` downloaded all 6.9 GB, installed its
14 dependencies, then died at the final step:

    sudo: a terminal is required to read the password
    Error: mactex: Failure while executing ... /usr/sbin/installer -pkg ...

**What I did instead.** Ran it by hand in a real terminal, where `sudo` could
prompt. The package was already cached so nothing re-downloaded.

**Then a second, quieter failure.** `./setup` still showed LaTeX red after the
install, because `/Library/TeX/texbin` was not on the running shell's PATH.
`eval "$(/usr/libexec/path_helper)"` fixes it — **but only if run BEFORE
`source .venv/bin/activate`.** Run afterwards, `path_helper` rebuilds PATH from
`/etc/paths` and pushes the venv's `python3` behind `/usr/bin/python3`, which
silently un-fixes every Python dependency. Order matters and nothing warns you.

Final state: `./setup` → 7/7 green.

---

## 2026-09-26 — `./art run` refused the build on a real visual defect

GATE V failed the first compile with 4 MAJOR defects. Two were genuine, and one
was not the defect it appeared to be.

- **B01 reported 3% canvas fill.** Not a layout problem. See the next entry.
- **B09 reported 43% fill** on a verdict page that looked completely full. The
  card is `#FFFFFF` on a `#F2F0E9` ground; GATE V counts a pixel as content only
  at `INK_DELTA = 28` per channel, and white-on-cream is 13–22. The card was
  invisible to the gate — only the type inside it counted. Fixed by adding more
  real verdict lines, not by gaming the metric.

**Lesson.** A failing metric is a hypothesis, not a diagnosis. One of these was a
real defect and one was a measurement artifact with a real fix.

---

## 2026-09-26 — The doctrine told me to do something the component cannot do

**What broke.** `ai-explainer/SKILL.md` says that when a misconception lives in a
phrase, put the whole phrase in `triggerWords` so the hesitant writer corrects the
phrase. I did that. The beat rendered, the gate passed the file, and **the
correction never happened** — the beat typed its text and cut.

**Diagnosis.** Read the component. `BrutalistHesitantWriter.buildActs` tokenises
with `text.split(/(\s+)/)` and matches `triggers.indexOf(core.toLowerCase())`
against a single token. A trigger containing a space can never match. The
documented instruction is not implementable by the shipped component, and it fails
**silently** — no error, no warning, just a missing correction.

**What I did instead.** Rebuilt the overview so one token carries the
misconception: `measurement` → `division`. The swap is the video's actual thesis
rather than a synonym.

**Lesson.** The gate caught this only indirectly, as an underfill number. If I had
trusted "0 BLOCKER, 0 MAJOR" I would have shipped a beat whose entire point was
missing.

---

## 2026-09-27 — Caught myself fabricating a Claude transcript

**What broke.** Nothing technical. Auditing my own build against the assignment, I
found that B00 and B10 rendered the Claude composer with output lines beneath the
prompt — lines *I* had written into the beat sheet. They read as a real Claude
response. They were not, they carried no date, and nothing on screen said so.

This is precisely what the assignment warns is a self-defeating failure: a video
about telling fluent output from supported claims, containing a fabricated
transcript to make a cleaner story.

**What I did instead.**
- **B00** now shows a genuine Claude reply, obtained 2026-09-27 from Claude Opus 5,
  with the full response recorded verbatim in `claude-response-B00.md` and only an
  exact excerpt on screen, headed `REAL REPLY · Claude Opus 5 · 2026-09-27 ·
  verbatim excerpt`. The `…` on screen marks an elision.
- **B10** (the Your-turn prompt, renumbered **B11** when the ending was reorganised)
  had its output removed entirely. It is a prompt for the viewer to run; showing a
  result would be inventing one. The composer then read `not run`; that label was
  later removed for visual cleanliness. The slide still shows no output, so nothing
  on screen claims a result.

**Lesson.** The production pipeline made fabrication the path of least resistance —
the brand's COLD OPEN LAW *requires* B00 to show a result, so authoring a
plausible one is the default behaviour. Following the house style and following
the assignment's evidence rules pointed in opposite directions, and the house
style would have lost me the assignment on its own terms.

---

## 2026-09-27 — A blocker I caught before it reached a build

Adding the "what this does not establish" line pushed the verdict card to 8 items,
and the card grows with its content. A test render measured
`BLOCKER edge-bleed — content crosses the title-safe top edge`. Tightened the
seven existing lines so the card fits inside `SAFE`, keeping the boundary
statement at full length. Re-measured clean at 74.5% before rebuilding.

**Lesson.** Rendering one still and measuring it costs ~40 seconds. A full rebuild
costs ~10 minutes. I moved to testing single frames against the gate's own
`analyze_frame` before every rebuild, which turned most of these from failed
builds into caught mistakes.

---

## 2026-09-27 — Fixing one screen broke another

Giving "what this video does not establish" its own screen meant taking that line
out of the verdict card (B09). The next build **failed GATE V: B09 at 49% fill**,
under the 55% floor. The verdict lines had earlier been *shortened* so eight of
them would fit (see the entry above); with only seven left, the block of text was
too small, and the white card is invisible to the gate. The final master export was
refused.

**What I did instead.** Restored the fuller wording of the seven lines, which had
passed before, and replaced one line so it didn't reintroduce "later models:
undisclosed", which I had just asked to remove from B02. Re-measured at both of
the gate's sample points (79.9%) before rebuilding.

**Lesson.** A fix made for one layout silently depended on it. Moving content
between screens needs both screens re-checked, not only the new one.

---

## 2026-09-27 — The TTS read the course number wrong, and I can't hear it

I added a spoken credit: "This video was created by Ethan Gomes from INFO 7375."

**What broke.** Nothing audible to the tools. Neither Claude nor the pipeline can
listen, and the usual check, transcribing the audio with faster-whisper, came back
"info 7375" for every version I tried: the transcriber normalises numbers, so it
can't tell "seven thousand three hundred seventy-five" from "seventy-three
seventy-five". The only clue was length: the literal version was half a second
longer.

**Diagnosis.** Printed Kokoro's own phonemes for each spelling. Written as `7375`,
it says *seven thousand three hundred seventy-five*, which is wrong for a course
number. "INFO" was fine: read as the word, not spelled out.

**What I did instead.** The narration spells it out as "Info seven three seven five"
(digit by digit, which is what I asked for). The captions are built from the
narration text, so `make_captions.py` has a display rule that shows the spoken
phrase as "INFO 7375" on screen.

**Lesson.** A passing transcription check means the words are intelligible, not
that they were said the way I meant. For numbers, check what the voice is *told*
to say (the phonemes), and then listen.

---

## 2026-09-27 — The paperwork drifted behind the video

After a long run of small edits, I asked for a check that every `.md` file matched
the final video. It found problems that no build gate looks at:

- **PROMPTS.md still listed the invented B00 output lines** under the heading
  "Result lines", as though they had been shown, after the video itself had been
  fixed to use a real reply. It was the exact fabrication from the "Caught myself
  fabricating a Claude transcript" entry, surviving in the documentation.
- **SOURCES.md credited me with directing "cutting a beat's narration when it ran
  long"**, which happened while building a different video, not this one.
- **SOURCES.md said "Third-party assets: None."** The video uses EB Garamond (OFL),
  the Kokoro-82M voice model (Apache-2.0) and kokoro-onnx (MIT). The licences were
  then checked against the installed files and listed properly.
- The README's rebuild steps said to register the new components in `Root.tsx`
  without saying how, so they would have failed on a fresh clone. Now there's
  `ROOT-REGISTRATION.md`.

**Lesson.** The video had a visual gate; the claims *about* the video had none. In
a course about the gap between fluent output and supported claims, the write-up
needs the same auditing as the frames.

---

## 2026-09-27 — The toolkit names files its way; the submission needs mine

`./art final` names the master after the project slug
(`claude-liam-hidden-parameter.mp4`), but the submission file is
`ethan_gomes_week1_explainer_video.mp4`. After renaming, the caption script broke:
it looked for the video under the slug name, so it only worked if run *before* the
rename, the opposite of the documented order.

**What I did instead.** `make_captions.py` now takes the final filename as an
argument. Running it in the documented order produced byte-identical captions to
the earlier build. BUILD-PROMPT.md and the README include the rename step.
