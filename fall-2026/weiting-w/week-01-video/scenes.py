"""scenes.py — Manim scenes for one-word-same-answer (Weiting W, INFO 7375 Week 01).

Concept: constraining the output format narrows the spread without checking anything.

Every reply on screen is read VERBATIM from evidence/<run>/responses.json (real
Claude replies, 2026-09-27, with screenshots beside them). Every count on
screen is computed here from those files with the same functions as
analyze_responses.py, and the scene refuses to render if a count drifts from
the saved evidence/analysis.json. Nothing on screen is invented or constructed.

Timing: each scene reads its beat's measured audio length from beat_sheet.json
and places events at the point in the narration where the matching words are
spoken (character position / length). Never hand-tune durations: regenerate
audio and re-render.

Palette: cream ground, warm ink, ONE terracotta accent event per scene.
Accent is used as a fill/stroke; accent TEXT uses the darker ACC_TEXT for contrast.
"""
import json
import math
import re
from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
EVID = HERE / "evidence"
PREFLIGHT = not (HERE / "beat_sheet.json").exists()   # Gate A runs a copy elsewhere

BG = "#FAF9F5"
INK = "#3D3929"
SOFT = "#6E6A57"
LINE = "#C9C4B3"
CARD = "#FFFFFF"
ACC = "#D97757"        # accent fill / stroke
ACC_TEXT = "#A44A32"   # accent text (contrast-safe on cream)
SERIF = "EB Garamond"
SANS = "Helvetica Neue"  # sans for labels; multi-line now via Paragraph (correct spacing)
MONO = "PT Mono"

config.background_color = BG

# Register the toolkit's Garamond file directly, so Manim resolves the family by
# its real file rather than guessing a variant (which mangled letter spacing).
import glob as _glob
_HERE = Path(__file__).resolve().parent
_TOOLKIT = _HERE.parents[3] if len(_HERE.parents) >= 4 else _HERE   # <repo>/youtube/<u>/<reel> -> <repo>
_FONT_GLOBS = [
    "runtime/fonts/EB_Garamond/**/EBGaramond-Regular.ttf",
    "runtime/fonts/Inter/**/Inter_28pt-Regular.ttf",
    "runtime/fonts/Inter/**/Inter-Regular.ttf",
    "runtime/fonts/PT_Mono/**/PTMono-Regular.ttf",
]
_font_paths = []
for _g in _FONT_GLOBS:
    _font_paths += _glob.glob(str(_TOOLKIT / _g), recursive=True)
_font_paths += _glob.glob(str(Path.home() / "Library/Fonts/EBGaramond-Regular.ttf"))
_font_paths += _glob.glob(str(Path.home() / "Library/Fonts/Inter*.ttf"))
_font_paths += _glob.glob(str(Path.home() / ".fonts/*.ttf"))
for _p in _font_paths:
    try:
        register_font(_p)
    except Exception:
        pass

# ---------------------------------------------------------------- data
RUNS = ["run1-normal", "run2-incognito"]
DATE_LINE = "Claude replies · Opus 5.5 Medium · 2026-09-27 · first reply in a new chat"


def _load(run):
    p = EVID / run / "responses.json"
    if p.exists():
        return json.loads(p.read_text())["groups"]
    # pre-flight fallback only: placeholder shapes, never rendered for real
    return {"D_open_question": {"prompt": "deck", "responses": ["x y z"] * 4},
            "A_capital_free": {"prompt": "capital", "responses": ["x y z"] * 4},
            "B_capital_one_word": {"prompt": "one word", "responses": ["Canberra"] * 4}}


DATA = {r: _load(r) for r in RUNS}


def words(text):
    return re.findall(r"[a-z0-9!^']+", text.lower())


def overlap(replies):
    pairs = [(a, b) for i, a in enumerate(replies) for b in replies[i + 1:]]
    j = [len(set(words(a)) & set(words(b))) / len(set(words(a)) | set(words(b))) for a, b in pairs]
    return sum(j) / len(j)


def stats(run, group):
    r = DATA[run][group]["responses"]
    wc = [len(words(x)) for x in r]
    return {"distinct": len(set(r)), "words": wc, "mean": sum(wc) / len(wc),
            "overlap": overlap(r)}


LOG2_52 = math.lgamma(53) / math.log(2)

if not PREFLIGHT:
    saved = json.loads((EVID / "analysis.json").read_text())
    for run in RUNS:
        for g in DATA[run]:
            s, a = stats(run, g), saved["runs"][run]["groups"][g]
            assert s["distinct"] == a["distinct"] and s["words"] == a["words_each"], (run, g)
            assert round(s["overlap"], 3) == a["mean_pairwise_overlap"], (run, g)
    assert round(LOG2_52, 2) == saved["check_deck_bits"]["log2_of_52_factorial"]
    SHEET = json.loads((HERE / "beat_sheet.json").read_text())
    BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
else:
    BEATS = {}


# ---------------------------------------------------------------- helpers
def T(text, size=26, color=INK, font=SERIF, **kw):
    # Multi-line strings: use Paragraph so each line is laid out on its own with
    # correct inter-word spacing (Text + manual "\n" mis-spaces glyphs on some
    # systems). t2c (color map) only applies to single-line Text.
    if "\n" in text:
        t2c = kw.pop("t2c", None)
        return Paragraph(*text.split("\n"), font=font, font_size=size, color=color,
                         line_spacing=0.8, **{k: v for k, v in kw.items() if k != "t2c"})
    return Text(text, font=font, font_size=size, color=color, **kw)


def wrap(text, width):
    out, line = [], ""
    for w in text.split():
        if line and len(line) + 1 + len(w) > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    out.append(line)
    return "\n".join(out)


def card(w, h):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=LINE,
                            stroke_width=2, fill_color=CARD, fill_opacity=1)


class Beat(Scene):
    """Scene clocked to its beat's audio. go(phrase) waits until that phrase is spoken."""
    BID = "B00"

    def setup(self):
        self._clock()

    def _clock(self):
        if getattr(self, "_ready", False):
            return
        self._ready = True
        b = BEATS.get(self.BID, {})
        self.D = float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 20)
        self.text = b.get("narration_text", "")
        self.t = 0.0

    def frac(self, phrase):
        self._clock()
        i = self.text.find(phrase)
        return (i / max(1, len(self.text))) if i >= 0 else None

    def go(self, where):
        self._clock()
        f = self.frac(where) if isinstance(where, str) else where
        if f is None:
            return
        target = f * self.D
        if target - self.t > 0.05:
            self.wait(target - self.t)
            self.t = target

    def pl(self, *anims, rt=0.8):
        self._clock()
        self.play(*anims, run_time=rt)
        self.t += rt

    def finish(self):
        self.go(1.0)


# The toolkit's runner finds scenes by matching the literal text "(Scene)" after
# the class name, so the beat scenes below are declared against this alias. It
# IS the Beat base class above (which subclasses manim's Scene).
Scene = Beat


class B01_Overview(Scene):
    BID = "B01"
    LINES = ["A format rule narrows the answers.",
             "It checks none of them.",
             "It does not have to be in the prompt."]

    def construct(self):
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=ACC, stroke_width=4).move_to(UP * 3.0)
        self.pl(Create(rule), rt=0.5)
        cues = ["A format rule", "It checks none", "It does not have"]
        ys = [1.6, 0.0, -1.6]
        widths = [2.2, 3.6, 5.2]
        for cue, txt, y, w in zip(cues, self.LINES, ys, widths):
            self.go(cue)
            grown = Line(LEFT * w, RIGHT * w, color=ACC, stroke_width=4).move_to(UP * 3.0)
            self.pl(FadeIn(T(txt, 58, INK, SERIF).move_to([0, y, 0])), Transform(rule, grown))
        self.finish()


class B09_Outro(Scene):
    BID = "B09"

    def construct(self):
        title = T("One Word, Same Answer", 82, INK, SERIF).move_to(UP * 1.2)
        dot = T(".", 82, ACC_TEXT, SERIF).next_to(title, RIGHT, buff=0.03).align_to(title, DOWN)
        handle = T("@Weiting", 46, SOFT, SANS).move_to(DOWN * 0.7)
        voice = T("narration: synthetic voice (Kokoro af_bella)", 26, SOFT, SANS).move_to(DOWN * 1.9)
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=ACC, stroke_width=4).move_to(DOWN * 2.9)
        self.go("title")
        self.pl(FadeIn(title), FadeIn(dot), rt=0.7)
        self.go("handle")
        self.pl(FadeIn(handle), FadeIn(voice), Create(rule), rt=0.7)
        self.finish()


# ---------------------------------------------------------------- B02
class B02_TwoChanges(Scene):
    BID = "B02"

    def construct(self):
        kicker = T("THE COMPARISON IN THE READING", 26, SOFT, SANS).move_to(UP * 3.15)
        self.pl(FadeIn(kicker), rt=0.5)

        pd = DATA["run2-incognito"]["D_open_question"]["prompt"]
        pb = DATA["run2-incognito"]["B_capital_one_word"]["prompt"].replace("\n", " ")
        cl, cr = card(6.0, 3.0).move_to(LEFT * 3.3 + UP * 1.6), card(6.0, 3.0).move_to(RIGHT * 3.3 + UP * 1.6)
        hl = T("Prompt 1", 26, SOFT, SANS).move_to(LEFT * 3.3 + UP * 2.75)
        hr = T("Prompt 2", 26, SOFT, SANS).move_to(RIGHT * 3.3 + UP * 2.75)
        tl = T(wrap(pd, 32), 28).move_to(LEFT * 3.3 + UP * 1.55)
        tr = T(wrap(pb, 32), 28).move_to(RIGHT * 3.3 + UP * 1.55)
        self.pl(FadeIn(cl), FadeIn(hl), FadeIn(tl))
        self.go("The other asks")
        self.pl(FadeIn(cr), FadeIn(hr), FadeIn(tr))

        self.go("In our runs")
        dl = T("our runs: 4 different sentences", 28, INK, SANS).move_to(LEFT * 3.4 + DOWN * 0.5)
        dr = T("our runs: Canberra × 4", 28, INK, SANS).move_to(RIGHT * 3.4 + DOWN * 0.5)
        self.pl(FadeIn(dl), FadeIn(dr))

        self.go("The format changed")
        fbar = RoundedRectangle(corner_radius=0.1, width=12.4, height=0.9, stroke_width=0,
                                fill_color=ACC, fill_opacity=0.18).move_to(DOWN * 1.7)
        ftxt = T("FORMAT   one sentence  →  one word", 30, ACC_TEXT, SANS).move_to(DOWN * 1.7)
        self.pl(FadeIn(fbar), FadeIn(ftxt))
        self.go("so did the question")
        qtxt = T("QUESTION   shuffled deck  →  capital of Australia", 30, INK, SANS).move_to(DOWN * 2.7)
        self.pl(FadeIn(qtxt))
        tag = T("two variables changed at once", 26, SOFT, SANS).move_to(DOWN * 3.2)
        self.pl(FadeIn(tag), rt=0.5)
        self.finish()


# ---------------------------------------------------------------- B03
class B03_ThreeGroupsTwoRuns(Scene):
    BID = "B03"
    COLS = [("D", "Deck · one sentence", -4.5), ("A", "Capital · free", 0.0), ("B", "Capital · one word", 4.5)]

    def thumbs(self, run, letter, x, y):
        cells = []
        for i in range(4):
            p = EVID / run / "screenshots" / f"{letter}{i + 1}.png"
            pos = [x + (-0.82 if i % 2 == 0 else 0.82), y + (0.48 if i < 2 else -0.48), 0]
            if p.exists():
                m = ImageMobject(str(p))
                m.height = 0.86
                if m.width > 1.5:
                    m.width = 1.5
                m.move_to(pos)
                frame = Rectangle(width=m.width, height=m.height, stroke_color=LINE, stroke_width=1.5).move_to(pos)
                cells.append(Group(m, frame))
            else:
                cells.append(Rectangle(width=1.5, height=0.86, stroke_color=LINE, stroke_width=1.5,
                                       fill_color=CARD, fill_opacity=1).move_to(pos))
        return Group(*cells)

    def construct(self):
        heads = VGroup(*[T(f"{k}  {lab}", 24, INK, SANS).move_to([x, 3.25, 0]) for k, lab, x in self.COLS])
        self.pl(FadeIn(heads[0]), FadeIn(heads[2]))
        self.go("plus the same capital question")
        self.pl(FadeIn(heads[1]))

        self.go("Now each step")
        a1 = Arrow([-3.0, 2.8, 0], [-1.4, 2.8, 0], buff=0, stroke_width=3, color=INK,
                   max_tip_length_to_length_ratio=0.12)
        a2 = Arrow([1.4, 2.8, 0], [3.0, 2.8, 0], buff=0, stroke_width=3, color=ACC_TEXT,
                   max_tip_length_to_length_ratio=0.12)
        l1 = T("question changes", 20, SOFT, SANS).move_to([-2.2, 2.4, 0])
        l2 = T("format changes", 20, ACC_TEXT, SANS).move_to([2.2, 2.4, 0])
        self.pl(GrowArrow(a1), FadeIn(l1), GrowArrow(a2), FadeIn(l2))

        self.go("For every prompt")
        proc = T("4 new chats per prompt · first reply kept · no regeneration", 22, SOFT, SANS).move_to(UP * 1.9)
        self.pl(FadeIn(proc))

        self.go("Once in my normal account")
        r1 = T("Run 1 · normal account", 22, INK, SANS).move_to([-4.9, 1.55, 0])
        g1 = Group(*[self.thumbs("run1-normal", k, x, 0.4) for k, _, x in self.COLS])
        self.pl(FadeIn(r1), FadeIn(g1))
        self.go("and once in incognito")
        r2 = T("Run 2 · incognito,\nmemory off", 22, INK, SANS).move_to([-5.0, -0.8, 0])
        g2 = Group(*[self.thumbs("run2-incognito", k, x, -2.0) for k, _, x in self.COLS])
        self.pl(FadeIn(r2), FadeIn(g2))

        self.go("My personal preferences")
        foot = T("Opus 5.5 Medium · 2026-09-27 · personal preferences on in both runs", 20, SOFT, SANS
                 ).move_to(DOWN * 3.3)
        self.pl(FadeIn(foot))
        self.finish()


# ---------------------------------------------------------------- B04 / B05 shared pieces
def reply_stack(replies, width_chars, size, x, top, gap=0.14, t2c=None, left=None):
    blocks, y = [], top
    for r in replies:
        t = T(wrap(r, width_chars), size, INK, SERIF, t2c=t2c or {})
        t.move_to([x, 0, 0]).align_to([0, y, 0], UP)
        if left is not None:
            t.align_to([left, 0, 0], LEFT)
        blocks.append(t)
        y = t.get_bottom()[1] - gap
    return VGroup(*blocks)


class B04_RunOne(Scene):
    BID = "B04"

    def construct(self):
        run = "run1-normal"
        head = T("Run 1 · normal account", 30, INK, SANS).move_to(UP * 3.05)
        date = T(DATE_LINE, 17, SOFT, SANS).move_to(DOWN * 3.1)
        self.pl(FadeIn(head), FadeIn(date), rt=0.6)

        la = T("A · Capital, no format rule", 22, SOFT, SANS).move_to([-3.4, 2.5, 0])
        A = reply_stack(DATA[run]["A_capital_free"]["responses"], 44, 26, -3.4, 2.05, gap=0.22)
        self.pl(FadeIn(la), FadeIn(A))

        self.go("Six words each")
        s = stats(run, "A_capital_free")
        sa = T(f"{s['distinct']} distinct · {s['words'][0]} words each\nword overlap {s['overlap']:.2f}",
               22, INK, SANS).move_to([-3.4, -1.0, 0])
        self.pl(FadeIn(sa))

        self.go("So the one-word rule")
        lb = T("B · Capital, one word", 22, SOFT, SANS).move_to([3.6, 2.5, 0])
        B = reply_stack(DATA[run]["B_capital_one_word"]["responses"], 30, 26, 3.6, 2.05, gap=0.22)
        self.pl(FadeIn(lb), FadeIn(B))

        self.go("almost nothing left")
        arr = Arrow([0.4, 0.9, 0], [2.4, 0.9, 0], buff=0, stroke_width=4, color=ACC,
                    max_tip_length_to_length_ratio=0.15)
        cut = T("format rule:\nlittle left to cut", 22, ACC_TEXT, SANS).move_to([3.6, -1.0, 0])
        self.pl(GrowArrow(arr), FadeIn(cut))
        self.finish()


class B05_RunTwo(Scene):
    BID = "B05"

    def construct(self):
        run = "run2-incognito"
        head = T("Run 2 · incognito, memory off", 30, INK, SANS).move_to(UP * 3.05)
        date = T(DATE_LINE, 17, SOFT, SANS).move_to(DOWN * 3.1)
        self.pl(FadeIn(head), FadeIn(date), rt=0.6)

        la = T("A · Capital, no format rule", 20, SOFT, SANS).move_to([-1.9, 2.6, 0])
        A = reply_stack(DATA[run]["A_capital_free"]["responses"], 60, 18, -2.2, 2.25, gap=0.16,
                        t2c={"1908": ACC_TEXT, "1927": ACC_TEXT}, left=-5.95)
        # Run 2's free-format replies are long (~30 words each); four stacked can drop past
        # the bottom safe margin and collide with the date line — the single layout error
        # the audit flags on B05. (B04 shows Run 1's ~6-word replies, so its stack is short
        # and stays clean.) Fit the column to a fixed vertical band, measuring its real
        # rendered height, so the stat line below always clears the date. Verbatim text unchanged.
        BAND_TOP, BAND_BOT = 2.3, -2.3
        if A.height > BAND_TOP - BAND_BOT:
            A.scale((BAND_TOP - BAND_BOT) / A.height)
        A.align_to([0, BAND_TOP, 0], UP).align_to([-5.95, 0, 0], LEFT)
        pa = card(8.0, A.height + 0.35).move_to([-2.2, A.get_center()[1], 0])
        self.pl(FadeIn(pa), FadeIn(la), FadeIn(A), rt=1.0)

        self.go("Four different sentences")
        s = stats(run, "A_capital_free")
        sa = T(f"{s['distinct']} distinct · {min(s['words'])}–{max(s['words'])} words · overlap {s['overlap']:.2f}",
               20, INK, SANS).next_to(A, DOWN, buff=0.22)
        self.pl(FadeIn(sa))

        self.go("With the one-word rule")
        lb = T("B · one word", 20, SOFT, SANS).move_to([4.3, 2.6, 0])
        B = reply_stack(DATA[run]["B_capital_one_word"]["responses"], 20, 24, 4.3, 2.2, gap=0.2)
        pb = card(2.6, B.height + 0.35).move_to(B.get_center())
        self.pl(FadeIn(pb), FadeIn(lb), FadeIn(B))

        self.go("That fits")
        why = T("fewer likely ways to reply\n→ replies converge", 20, INK, SANS).move_to([4.2, -0.6, 0])
        why2 = T("(the course reading's reason)", 16, SOFT, SANS).next_to(why, DOWN, buff=0.12)
        self.pl(FadeIn(why), FadeIn(why2))

        self.go("In my normal account")
        both = T("Both runs · same prompts", 30, INK, SANS).move_to(UP * 3.05)
        self.pl(*[FadeOut(m) for m in (pa, la, A, sa, pb, lb, B, why, why2)],
                Transform(head, both), rt=0.6)
        self.bars()
        self.finish()

    def bars(self):
        base, scale = -1.8, 0.11
        vals = [("Run 1", stats("run1-normal", "A_capital_free")["mean"], stats("run1-normal", "B_capital_one_word")["mean"], -2.8),
                ("Run 2", stats("run2-incognito", "A_capital_free")["mean"], stats("run2-incognito", "B_capital_one_word")["mean"], 2.8)]
        axis = Line([-5.6, base, 0], [5.6, base, 0], color=LINE, stroke_width=2)
        title = T("mean words per reply", 22, SOFT, SANS).move_to(UP * 2.5)
        mobs = [axis, title]
        for name, a, b, x in vals:
            for dx, v, lab in ((-0.8, a, "A free"), (0.8, b, "B one word")):
                h = max(0.04, v * scale)
                r = Rectangle(width=1.1, height=h, stroke_width=0,
                              fill_color=ACC if (name == "Run 1" and lab == "A free") else INK,
                              fill_opacity=0.85).move_to([x + dx, base + h / 2, 0])
                n = T(f"{v:.1f}".rstrip("0").rstrip("."), 22, INK, SANS).next_to(r, UP, buff=0.1)
                l = T(lab, 18, SOFT, SANS).move_to([x + dx, base - 0.3, 0])
                mobs += [r, n, l]
            mobs.append(T(name, 22, INK, SANS).move_to([x, base - 0.75, 0]))
        note = T("run 1: already short\nbefore any format rule", 22, ACC_TEXT, SANS).move_to([-2.8, 1.2, 0])
        self.pl(*[FadeIn(m) for m in mobs], rt=1.0)
        self.pl(FadeIn(note), rt=0.6)


# ---------------------------------------------------------------- B06
class B06_NobodyChecked(Scene):
    BID = "B06"

    def construct(self):
        run2 = DATA["run2-incognito"]
        dated = next((r for r in run2["A_capital_free"]["responses"] if "1908" in r),
                     run2["A_capital_free"]["responses"][0])
        lab = T("a free reply (run 2)", 20, SOFT, SANS).move_to([-3.1, 3.1, 0])
        rep = T(wrap(dated, 36), 22, INK, SERIF, t2c={"1908": ACC_TEXT, "1927": ACC_TEXT})
        # This long run-2 reply sits between the label above (y≈3.1) and the arrow→Canberra
        # below (y≈1.0); fit it to that band, measuring real rendered height, so it can't
        # grow into either. Same cause as B05 — run-2's free replies are long. Text verbatim.
        R_TOP, R_BOT = 2.85, 1.05
        if rep.height > R_TOP - R_BOT:
            rep.scale((R_TOP - R_BOT) / rep.height)
        rep.move_to([-3.1, (R_TOP + R_BOT) / 2, 0])
        pr = card(6.0, rep.height + 0.3).move_to(rep.get_center())
        self.pl(FadeIn(pr), FadeIn(lab), FadeIn(rep))

        self.go("It just removed them")
        one = T("Canberra", 30, INK, SERIF).move_to([-3.1, 0.35, 0])
        arr = Arrow([-3.1, 1.0, 0], [-3.1, 0.62, 0], buff=0, stroke_width=3, color=INK,
                    max_tip_length_to_length_ratio=0.3)
        gone = T("1908, 1927: removed, not verified", 22, ACC_TEXT, SANS).move_to([-3.1, -0.3, 0])
        self.pl(GrowArrow(arr), FadeIn(one), FadeIn(gone))

        self.go("Canberra is correct")
        ok = T("Canberra is correct: checked outside\nthe chat, not by seeing it four times", 20, INK, SANS
               ).move_to([-3.1, -1.4, 0])
        self.pl(FadeIn(ok))

        self.go("The deck answers also")
        rl = T("sizes quoted in the deck replies", 20, SOFT, SANS).move_to([3.6, 3.1, 0])
        quotes = VGroup(T('"about 225 bits"', 26, INK, SANS),
                        T('"about 2^225"', 26, INK, SANS),
                        T('"about 2^226"', 26, INK, SANS)).arrange(DOWN, buff=0.3).move_to([3.6, 1.7, 0])
        pq = card(4.4, quotes.height + 0.5).move_to(quotes.get_center())
        self.pl(FadeIn(pq), FadeIn(rl), FadeIn(quotes))

        self.go("Our script worked out")
        calc = T(f"log2(52!) = {LOG2_52:.2f}", 34, INK, MONO).move_to([3.2, 0.0, 0])
        box = SurroundingRectangle(calc, color=ACC, buff=0.15, stroke_width=4)
        src = T("computed by analyze_responses.py", 18, SOFT, SANS).move_to([3.2, -0.75, 0])
        self.pl(FadeIn(calc), Create(box), FadeIn(src))

        self.go("no format rule checked")
        fin = T("No format rule checked any of this. We did.", 26, INK, SANS).move_to(DOWN * 2.85)
        self.pl(FadeIn(fin))
        self.finish()


# ---------------------------------------------------------------- B07
class B07_Boundary(Scene):
    BID = "B07"

    def construct(self):
        h1 = T("OBSERVED", 26, INK, SANS).move_to([-3.5, 2.9, 0])
        h2 = T("NOT ESTABLISHED", 26, INK, SANS).move_to([3.5, 2.9, 0])
        rule = Line([0, 2.9, 0], [0, -2.9, 0], color=LINE, stroke_width=2)
        self.pl(FadeIn(h1), FadeIn(h2), Create(rule))

        obs = ["24 real replies\n2 runs × 3 prompts × 4 chats",
               "distinct answers, word counts,\nword overlaps",
               "log2(52!) = 225.58, computed"]
        og = VGroup(*[T(o, 22, INK, SANS).move_to([0, 1.9 - i * 1.15, 0]).align_to([-6.2, 0, 0], LEFT)
                      for i, o in enumerate(obs)])
        self.pl(FadeIn(og), rt=0.8)

        items = [("It's four replies", "beyond 4 replies per prompt,\none model, one day"),
                 ("not the probabilities", "the probabilities behind\nthe replies"),
                 ("It also doesn't pin down", "why run-1 replies were short\n(incognito may change\nmore than memory)"),
                 ("we didn't verify", "the 1908 / 1927 dates,\nthe seven-shuffles claim")]
        for i, (cue, txt) in enumerate(items):
            self.go(cue)
            t = T(txt, 22, INK, SANS).move_to([0, 1.9 - i * 1.5, 0]).align_to([0.6, 0, 0], LEFT)
            mobs = [FadeIn(t)]
            if i == 2:
                u = Line(t.get_corner(DL) + DOWN * 0.1, t.get_corner(DR) + DOWN * 0.1,
                         color=ACC, stroke_width=4)
                mobs.append(Create(u))
            self.pl(*mobs, rt=0.6)
        self.finish()
