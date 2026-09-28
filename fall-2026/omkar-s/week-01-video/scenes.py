"""
Manim scenes for max-subtraction-softmax (INFO 7375 Week 1 video, Omkar Salian).

One Scene per beat. Every number on screen is copied from evidence/*.txt, which
is the saved output of the course's main.py, its unittest file, and
evidence/max_shift_evidence.py (Python 3.14.2, run 2026-09-24).

Timing: each scene reads its measured narration length (actual_duration_s,
written by generate_audio_kokoro.py) from beat_sheet.json and ends exactly
there. Reveals are cued at the word position of a phrase in the narration.
"""
import json
import re
from pathlib import Path

from manim import *

_SHEET_PATH = Path(__file__).resolve().parent / "beat_sheet.json"
# Real renders run inside the reel folder. Brutalist's GATE A copies scenes.py
# alone into a temp dir to dry-run it; there the clock falls back to a neutral
# placeholder so the geometry can still be checked.
BEATS = ({b["beat_id"]: b for b in json.loads(_SHEET_PATH.read_text())["beats"]}
         if _SHEET_PATH.is_file() else {})

# Palette (cream stage, warm ink, one terracotta accent; darker terracotta for text).
BG = "#F2F0E9"
INK = "#3D3929"
MUTED = "#5E5848"
ACCENT = "#D97757"      # shapes / highlights only
ACCENT_TX = "#A44A32"   # accent-coloured text (contrast-safe on cream)
GOOD = "#2F6B4F"        # shapes only
GOOD_BG = "#D3E4D8"     # pale green plate behind "this matches / passes" text
HILITE = "#F3D9CC"      # pale terracotta fill behind highlighted text

MONO = "Menlo"
SERIF = "EB Garamond"
SANS = "Helvetica Neue"


class Clock:
    """Keeps a scene on its beat's measured audio clock."""

    def __init__(self, scene, bid):
        self.s = scene
        self.dry = bid not in BEATS
        beat = BEATS.get(bid, {"actual_duration_s": 60.0, "narration_text": ""})
        self.dur = float(beat["actual_duration_s"])
        self.lead = float(beat.get("lead_silence_s", 0.0))
        self.words = [re.sub(r"[^a-z0-9]", "", w.lower()) for w in beat["narration_text"].split()]
        self.t = 0.0
        scene.camera.background_color = BG

    def cue(self, phrase):
        if self.dry:
            return self.t + 0.5
        target = [re.sub(r"[^a-z0-9]", "", w.lower()) for w in phrase.split()]
        n = len(target)
        for i in range(len(self.words) - n + 1):
            if self.words[i:i + n] == target:
                return self.lead + (self.dur - self.lead - 0.4) * i / len(self.words)
        raise KeyError(f"cue phrase not in narration: {phrase!r}")

    def at(self, t):
        if isinstance(t, str):
            t = self.cue(t)
        if t > self.t + 1e-3:
            self.s.wait(t - self.t)
            self.t = t

    def play(self, *anims, rt=1.0):
        self.s.play(*anims, run_time=rt)
        self.t += rt

    def finish(self):
        self.at(self.dur)


def txt(s, size=30, color=INK, font=SANS, weight="NORMAL"):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def mono(s, size=30, color=INK, weight="NORMAL"):
    return Text(s, font=MONO, font_size=size, color=color, weight=weight)


def kicker(s):
    return txt(s, 22, MUTED).move_to([-6.1, 3.15, 0], aligned_edge=LEFT)


def footer(s):
    return txt(s, 19, MUTED).move_to([-6.1, -3.2, 0], aligned_edge=LEFT)


def tag(s):
    """Small boxed label, used for 'constructed input' and provenance."""
    t = txt(s, 19, ACCENT_TX)
    box = SurroundingRectangle(t, color=ACCENT_TX, buff=0.1, stroke_width=2)
    return VGroup(box, t)


KICK = "SUBTRACT THE MAX  ·  CHAPTER 1, PART 2"

# Real values (evidence/max_shift_output.txt)
NAIVE_W = ["2.718282", "7.389056", "20.085537"]
NAIVE_SUM = "30.192875"
SHIFT_W = ["0.135335", "0.367879", "1.000000"]
SHIFT_SUM = "1.503215"
PROBS = ["0.0900", "0.2447", "0.6652"]
E3 = "20.085537"


# ---------------------------------------------------------------- B00
class B00_TheLine(Scene):
    def construct(self):
        c = Clock(self, "B00")
        self.add(kicker(KICK))
        src = [
            "def probabilities(logits, temperature=1.0):",
            "    # ... input checks ...",
            "    peak = max(logits)",
            "    weights = [math.exp((x - peak) / temperature)",
            "               for x in logits]",
            "    total = sum(weights)",
            "    return [weight / total for weight in weights]",
        ]
        cw = mono("M" * 20, 25).width / 20
        lines = VGroup(*[mono(s.lstrip(), 25) for s in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for m, s in zip(lines, src):
            m.shift(RIGHT * cw * (len(s) - len(s.lstrip())))
        lines[1].set_color(MUTED)
        lines.move_to([0, 0.95, 0])
        cap = VGroup(
            txt("Excerpt of probabilities() in lessons/01-randomness-and-first-prompts/code/main.py @ e6c6c49", 18, MUTED),
            txt("Input checks elided; the line wrap is mine; otherwise verbatim.", 18, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-6.1, -3.1, 0], aligned_edge=LEFT)
        voice = txt("Narration: synthetic voice (Kokoro af_bella)", 19, MUTED).move_to([6.1, 3.15, 0], aligned_edge=RIGHT)
        self.add(voice)
        c.play(FadeIn(lines, shift=UP * 0.2), FadeIn(cap), rt=1.2)

        c.at("subtracts the largest")
        hl1 = BackgroundRectangle(lines[2], color=HILITE, fill_opacity=1, buff=0.08)
        hl2 = BackgroundRectangle(lines[3], color=HILITE, fill_opacity=1, buff=0.08)
        c.play(FadeIn(hl1), FadeIn(hl2), lines[2].animate.set_color(ACCENT_TX),
               lines[3].animate.set_color(ACCENT_TX), rt=0.8)
        self.bring_to_front(lines)

        c.at("That looks like")
        q = txt("Does subtracting the max change the probabilities?", 38, INK, SERIF)
        q.move_to([0, -1.45, 0])
        c.play(Write(q), rt=1.4)
        c.at("It doesn't")
        a = txt("No. Here is the evidence.", 34, ACCENT_TX, SERIF).next_to(q, DOWN, buff=0.3)
        c.play(FadeIn(a, shift=UP * 0.15), rt=0.8)
        c.finish()


# ------------------------------------------------ shared table (B01-B03)
L_COLS = [-5.2, -3.25, -1.0]    # score, weight, probability (plain recipe)
R_COLS = [1.25, 3.2, 5.35]      # score-3, weight, probability (shifted)
ROWS = [1.15, 0.35, -0.45]
TOTAL_Y = -1.35
HEAD_Y = 1.95
TITLE_Y = 2.6


def panel_titles():
    lt = txt("Plain recipe", 30, INK, SERIF).move_to([-3.2, TITLE_Y, 0])
    rt = txt("Subtract the max first", 30, INK, SERIF).move_to([3.3, TITLE_Y, 0])
    return lt, rt


def headers(cols, labels):
    return VGroup(*[txt(l, 22, MUTED).move_to([x, HEAD_Y, 0]) for x, l in zip(cols, labels)])


def col(values, x, size=28, color=INK):
    return VGroup(*[mono(v, size, color).move_to([x, y, 0]) for v, y in zip(values, ROWS)])


def rule(x0, x1):
    return Line([x0, TOTAL_Y + 0.45, 0], [x1, TOTAL_Y + 0.45, 0], color=MUTED, stroke_width=2)


def build_left(show=True):
    lt, _ = panel_titles()
    head = headers(L_COLS, ["score", "e^score", "probability"])
    sc = col(["1", "2", "3"], L_COLS[0])
    w = col(NAIVE_W, L_COLS[1])
    p = col(PROBS, L_COLS[2], color=ACCENT_TX)
    ln = rule(-4.1, -2.1)
    tot = mono(NAIVE_SUM, 28).move_to([L_COLS[1], TOTAL_Y, 0])
    totl = txt("total", 22, MUTED).move_to([L_COLS[0], TOTAL_Y, 0])
    return dict(title=lt, head=head, sc=sc, w=w, p=p, rule=ln, tot=tot, totl=totl)


def build_right():
    _, rt = panel_titles()
    head = headers(R_COLS, ["score − 3", "e^(score − 3)", "probability"])
    sc = col(["−2", "−1", "0"], R_COLS[0])
    w = col(SHIFT_W, R_COLS[1])
    p = col(PROBS, R_COLS[2], color=ACCENT_TX)
    ln = rule(2.2, 4.2)
    tot = mono(SHIFT_SUM, 28).move_to([R_COLS[1], TOTAL_Y, 0])
    totl = txt("total", 22, MUTED).move_to([R_COLS[0], TOTAL_Y, 0])
    return dict(title=rt, head=head, sc=sc, w=w, p=p, rule=ln, tot=tot, totl=totl)


def divider():
    return Line([0, 2.85, 0], [0, -1.8, 0], color=MUTED, stroke_width=1.5)


# ---------------------------------------------------------------- B01
class B01_NaiveRoute(Scene):
    def construct(self):
        c = Clock(self, "B01")
        self.add(kicker(KICK))
        L = build_left()
        c.play(FadeIn(L["title"]), FadeIn(L["head"][0]), rt=0.6)
        c.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in L["sc"]], lag_ratio=0.3), rt=1.2)
        t = tag("constructed input — I chose these scores; no model produced them").move_to([0, -2.35, 0])
        c.at("I chose them")
        c.play(FadeIn(t), rt=0.6)

        c.at("raises e")
        c.play(FadeIn(L["head"][1]), rt=0.4)
        c.play(LaggedStart(*[TransformFromCopy(s, w) for s, w in zip(L["sc"], L["w"])], lag_ratio=0.35), rt=2.2)

        c.at("Add them up")
        copies = VGroup(*[w.copy() for w in L["w"]])
        c.play(Create(L["rule"]), FadeIn(L["totl"]), rt=0.5)
        c.play(*[cp.animate.move_to(L["tot"]).set_opacity(0) for cp in copies],
               FadeIn(L["tot"], run_time=1.4, rate_func=lambda t: max(0, 2 * t - 1)), rt=1.4)
        self.remove(*copies)
        box = SurroundingRectangle(L["tot"], color=ACCENT, buff=0.12)
        c.play(Create(box), rt=0.5)

        c.at("divide each weight")
        c.play(FadeIn(L["head"][2]), rt=0.4)
        anims = []
        for w, p in zip(L["w"], L["p"]):
            anims.append(TransformFromCopy(VGroup(w, L["tot"]), p))
        c.play(LaggedStart(*anims, lag_ratio=0.4), rt=2.4)
        note = txt("each probability = weight ÷ total", 24, INK).move_to([0, -2.95, 0])
        c.play(FadeIn(note), rt=0.5)

        c.at("Outcome two gets")
        c.play(Indicate(L["p"][2], color=ACCENT_TX, scale_factor=1.25), rt=1.2)
        c.finish()


# ---------------------------------------------------------------- B02
class B02_ShiftedRoute(Scene):
    def construct(self):
        c = Clock(self, "B02")
        self.add(kicker(KICK))
        L = build_left()
        left = VGroup(*L.values())
        self.add(left)
        R = build_right()
        c.play(Create(divider()), FadeIn(R["title"]), rt=0.8)

        c.at("Subtract the largest")
        sc_copy = L["sc"].copy()
        c.play(sc_copy.animate.move_to([R_COLS[0], (ROWS[0] + ROWS[2]) / 2, 0]), rt=1.0)
        minus = txt("− 3", 30, ACCENT_TX, weight="BOLD").next_to(sc_copy, LEFT, buff=0.25)
        c.play(FadeIn(minus), rt=0.5)
        c.at("The scores become")
        c.play(FadeIn(R["head"][0]), ReplacementTransform(sc_copy, R["sc"]), FadeOut(minus), rt=1.2)

        c.at("The weights get")
        c.play(FadeIn(R["head"][1]), rt=0.3)
        c.play(LaggedStart(*[TransformFromCopy(s, w) for s, w in zip(R["sc"], R["w"])], lag_ratio=0.35), rt=2.0)

        c.at("The total is")
        copies = VGroup(*[w.copy() for w in R["w"]])
        c.play(Create(R["rule"]), FadeIn(R["totl"]), rt=0.4)
        c.play(*[cp.animate.move_to(R["tot"]).set_opacity(0) for cp in copies],
               FadeIn(R["tot"], run_time=1.2, rate_func=lambda t: max(0, 2 * t - 1)), rt=1.2)
        self.remove(*copies)

        c.at("Divide")
        c.play(FadeIn(R["head"][2]), rt=0.3)
        c.play(LaggedStart(*[TransformFromCopy(VGroup(w, R["tot"]), p) for w, p in zip(R["w"], R["p"])],
                           lag_ratio=0.35), rt=1.8)
        c.at("come out the same")
        b1 = SurroundingRectangle(L["p"], color=ACCENT, buff=0.15)
        b2 = SurroundingRectangle(R["p"], color=ACCENT, buff=0.15)
        same = txt("Different intermediates. Same probabilities.", 32, INK, SERIF).move_to([0, -2.45, 0])
        c.play(Create(b1), Create(b2), FadeIn(same), rt=1.0)
        c.finish()


# ---------------------------------------------------------------- B03
class B03_WhyItCancels(Scene):
    def construct(self):
        c = Clock(self, "B03")
        self.add(kicker(KICK))
        L, R = build_left(), build_right()
        div = divider()
        table = VGroup(*L.values(), *R.values(), div)
        self.add(table)

        c.at("Every shifted weight")
        arrows, labels = VGroup(), VGroup()
        pairs = list(zip(L["w"], R["w"])) + [(L["tot"], R["tot"])]
        for a, b in pairs:
            ar = Arrow(a.get_right() + RIGHT * 0.1, b.get_left() + LEFT * 0.1, buff=0.05,
                       color=ACCENT, stroke_width=3, max_tip_length_to_length_ratio=0.06)
            arrows.add(ar)
            labels.add(mono("÷ " + E3, 18, ACCENT_TX).next_to(ar, UP, buff=0.16))
        clear = [L["p"], R["sc"], L["head"][2], R["head"][0], R["totl"], div]
        c.play(*[FadeOut(m) for m in clear], rt=0.6)
        c.play(LaggedStart(*[GrowArrow(a) for a in arrows[:3]], lag_ratio=0.3),
               LaggedStart(*[FadeIn(l) for l in labels[:3]], lag_ratio=0.3), rt=1.8)
        e3 = txt("20.085537 = e³ (the max score was 3)", 24, INK).move_to([0, -2.3, 0])
        c.play(FadeIn(e3), rt=0.5)

        c.at("And the total")
        c.play(GrowArrow(arrows[3]), FadeIn(labels[3]),
               Indicate(L["tot"], color=ACCENT_TX), Indicate(R["tot"], color=ACCENT_TX), rt=1.4)

        c.at("A probability is")
        c.play(FadeOut(table), FadeOut(arrows), FadeOut(labels), FadeOut(e3), rt=0.8)
        nw, nf = mono("weight", 60), mono("÷ e³", 60, ACCENT_TX)
        dw, df = mono("total", 60), mono("÷ e³", 60, ACCENT_TX)
        num = VGroup(nw, nf).arrange(RIGHT, buff=0.3)
        den = VGroup(dw, df).arrange(RIGHT, buff=0.3)
        bar = Line(LEFT * 3.4, RIGHT * 3.4, color=INK, stroke_width=5)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.45).move_to([-2.4, 0.55, 0])
        lab = txt("shifted probability", 28, MUTED).move_to([-2.4, 2.55, 0])
        chk = VGroup(
            mono("20.085537 / 30.192875 = 0.6652", 28),
            mono(" 1.000000 /  1.503215 = 0.6652", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        chk.move_to([6.0 - chk.width / 2, -2.55, 0])
        chk_l = txt("outcome two, both routes (from the saved run):", 22, MUTED).next_to(chk, UP, buff=0.2)
        chk_l.align_to(chk, LEFT)
        c.play(FadeIn(lab), Write(num), Create(bar), Write(den), FadeIn(chk_l), FadeIn(chk), rt=1.6)

        c.at("cancels")
        c.play(Indicate(nf, color=ACCENT_TX), Indicate(df, color=ACCENT_TX), rt=0.6)
        gone = txt("same factor, top and bottom: it cancels", 26, ACCENT_TX).move_to([2.9, 2.55, 0])
        c.play(nf.animate.move_to(gone.get_center() + RIGHT * 3.4).set_opacity(0),
               df.animate.move_to(gone.get_center() + RIGHT * 3.4).set_opacity(0),
               FadeIn(gone), nw.animate.move_to([bar.get_center()[0], nw.get_center()[1], 0]),
               dw.animate.move_to([bar.get_center()[0], dw.get_center()[1], 0]), rt=1.0)
        self.remove(nf, df)
        eq = mono("= weight ÷ total", 48, ACCENT_TX)
        eq.move_to([6.0 - eq.width / 2, bar.get_center()[1], 0])
        c.play(FadeIn(eq, shift=LEFT * 0.2), rt=0.8)

        c.at("The intermediates changed")
        c.play(Indicate(chk, color=ACCENT_TX, scale_factor=1.05), rt=1.0)
        c.finish()


# ---------------------------------------------------------------- B04
class B04_Overflow(Scene):
    def construct(self):
        c = Clock(self, "B04")
        self.add(kicker(KICK))
        sc = mono("scores = [1001, 1002, 1003]", 34).move_to([-2.0, 2.45, 0])
        t = tag("constructed input: [1, 2, 3] + 1000").next_to(sc, RIGHT, buff=0.4)
        ax = NumberLine(x_range=[-100, 1100, 100], length=11.4, color=INK, include_numbers=False,
                        stroke_width=3).move_to([0, -0.8, 0])
        nums = VGroup(*[mono(str(v), 20, MUTED).next_to(ax.n2p(v), DOWN, buff=0.3) for v in (0, 500, 1000)])
        axl = txt("exponent passed to math.exp", 22, MUTED).next_to(ax, DOWN, buff=0.75)
        c.play(FadeIn(sc), Create(ax), FadeIn(nums), FadeIn(axl), rt=1.0)
        c.at("The gaps are unchanged")
        c.play(FadeIn(t), rt=0.5)

        c.at("the plain recipe")
        err = VGroup(
            mono("naive   math.exp(1003) -> OverflowError: math range error", 24, ACCENT_TX),
        ).move_to([0, 1.55, 0])
        ebox = SurroundingRectangle(err, color=ACCENT_TX, buff=0.15)
        c.play(FadeIn(err), Create(ebox), rt=1.0)
        src = txt("verbatim from evidence/max_shift_output.txt (Python 3.14.2)", 19, MUTED).next_to(ebox, DOWN, buff=0.12)
        c.play(FadeIn(src), rt=0.4)

        c.at("The largest float")
        ceil_x = 709.78
        ceil = DashedLine(ax.n2p(ceil_x) + UP * 0.9, ax.n2p(ceil_x) + DOWN * 0.3, color=ACCENT_TX, stroke_width=4)
        ceil_l = mono("709.78 = log(largest float)", 20, ACCENT_TX).next_to(ceil, UP, buff=0.08)
        dots = VGroup(*[Dot(ax.n2p(v), radius=0.09, color=ACCENT_TX) for v in (1001, 1002, 1003)])
        c.play(Create(ceil), FadeIn(ceil_l), rt=0.8)
        c.play(FadeIn(dots, scale=1.5), rt=0.6)
        over = txt("past the ceiling", 20, ACCENT_TX).next_to(dots, UP, buff=0.2)
        c.play(FadeIn(over), rt=0.4)

        c.at("subtract the max")
        c.play(FadeOut(over), *[d.animate.move_to(ax.n2p(v)).set_color(GOOD)
                                for d, v in zip(dots, (-2, -1, 0))], rt=1.8)
        res = VGroup(
            mono("shifted  [-2, -1, 0]  ->  [0.0900, 0.2447, 0.6652]", 24),
            mono("A == B exactly: True     (A = [1,2,3], B = [1001,1002,1003])", 22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([0, -2.75, 0])
        c.play(FadeOut(axl), FadeIn(res[0]), rt=0.8)
        c.at("with identical probabilities")
        plate = BackgroundRectangle(res[1], color=GOOD_BG, fill_opacity=1, buff=0.08)
        c.play(FadeIn(plate), FadeIn(res[1]), rt=0.6)
        self.bring_to_front(res[1])
        c.finish()


# ---------------------------------------------------------------- B05
class B05_LessonTest(Scene):
    def construct(self):
        c = Clock(self, "B05")
        self.add(kicker(KICK))
        head = txt("The lesson's own test case", 34, INK, SERIF).move_to([0, 2.45, 0])
        c.play(FadeIn(head), rt=0.6)
        steps = ["[1000, 1000]", "[0, 0]", "[1, 1]", "[0.5, 0.5]"]
        ops = ["− max", "e^x", "÷ total (2)"]
        xs = [-4.6, -1.3, 1.45, 4.5]
        boxes = VGroup()
        for s, x in zip(steps, xs):
            m = mono(s, 30)
            b = SurroundingRectangle(m, color=INK, buff=0.2, stroke_width=2)
            boxes.add(VGroup(b, m).move_to([x, 0.9, 0]))
        boxes[-1][0].set_color(ACCENT)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.1, color=MUTED,
                                stroke_width=3) for i in range(3)])
        olabs = VGroup(*[txt(o, 22, ACCENT_TX).move_to([a.get_center()[0], 1.75, 0]) for o, a in zip(ops, arrows)])
        code = VGroup(
            mono("self.assertEqual(m.probabilities([1000, 1000]), [0.5, 0.5])", 24),
            mono("test_02 (test_main.LessonTests.test_02) ... ok", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -1.25, 0])
        cl = txt("from code/tests/test_main.py; run output saved in evidence/tests_output.txt",
                 20, MUTED).next_to(code, DOWN, buff=0.3)
        c.play(FadeIn(boxes[0]), FadeIn(code[0]), FadeIn(cl), rt=0.8)
        cues = ["Shifted they become", "The weights are", "Divide by two"]
        for i, cu in enumerate(cues):
            c.at(cu)
            c.play(GrowArrow(arrows[i]), FadeIn(olabs[i]), FadeIn(boxes[i + 1], shift=RIGHT * 0.2), rt=0.9)

        c.at("each gets one half")
        plate = BackgroundRectangle(code[1], color=GOOD_BG, fill_opacity=1, buff=0.08)
        c.play(FadeIn(plate), FadeIn(code[1]), rt=0.6)
        self.bring_to_front(code[1])

        c.at("The large shared offset")
        msg = txt("The shared 1000 never reached the weights.", 30, INK, SERIF).move_to([0, -2.85, 0])
        c.play(FadeIn(msg), Indicate(boxes[1], color=ACCENT_TX), rt=1.0)
        c.finish()


# ---------------------------------------------------------------- B06
class B06_Rounding(Scene):
    def construct(self):
        c = Clock(self, "B06")
        self.add(kicker(KICK))
        head = txt("Outcome 0, scores [1, 2, 3]", 32, INK, SERIF).move_to([0, 2.4, 0])
        c.play(FadeIn(head), rt=0.6)
        a = txt("0.09003057317038045", 66)
        b = txt("0.09003057317038046", 66)
        la = txt("plain recipe", 26, MUTED)
        lb = txt("subtract max", 26, MUTED)
        grid = VGroup(la, a, lb, b).arrange_in_grid(rows=2, cols=2, col_alignments="rl", buff=(0.6, 0.45))
        grid.move_to([0, 0.8, 0])
        src = txt("both values printed by evidence/max_shift_evidence.py", 20, MUTED).move_to([0, -3.05, 0])
        c.play(FadeIn(grid), FadeIn(src), rt=1.0)

        c.at("the two routes agree")
        u = Line(b[:-1].get_corner(DL) + DOWN * 0.18, b[:-1].get_corner(DR) + DOWN * 0.18,
                 color=GOOD, stroke_width=6)
        ul = txt("these digits agree", 24, INK).next_to(u, DOWN, buff=0.2).align_to(u, LEFT)
        c.play(Create(u), FadeIn(ul), rt=0.8)
        c.at("sixteenth significant digit")
        d = BackgroundRectangle(VGroup(a[-1], b[-1]), color=HILITE, fill_opacity=1, buff=0.1)
        dl = txt("16th significant digit", 24, ACCENT_TX)
        dl.move_to([min(b[-1].get_center()[0], 6.0 - dl.width / 2), b.get_bottom()[1] - 0.4, 0])
        c.play(FadeIn(d), a[-1].animate.set_color(ACCENT_TX), b[-1].animate.set_color(ACCENT_TX), FadeIn(dl), rt=0.8)
        self.bring_to_front(a, b)

        c.at("So the precise claim")
        claim = txt("Same distribution, up to floating-point rounding.", 40, ACCENT_TX, SERIF).move_to([0, -2.0, 0])
        cbox = SurroundingRectangle(claim, color=ACCENT, buff=0.2)
        c.play(Write(claim), Create(cbox), rt=1.4)
        c.finish()


# ---------------------------------------------------------------- B07
class B07_Boundary(Scene):
    def construct(self):
        c = Clock(self, "B07")
        self.add(kicker(KICK))
        head = txt("What this does NOT establish", 40, ACCENT_TX, SERIF).move_to([0, 2.5, 0])
        c.play(FadeIn(head), rt=0.8)
        c.at("It does nothing for")
        l1 = txt("prevents overflow of the largest weight", 26, INK).move_to([-3.1, 1.75, 0])
        l1p = BackgroundRectangle(l1, color=GOOD_BG, fill_opacity=1, buff=0.08)
        l2 = txt("does nothing for the smallest weights", 26, ACCENT_TX).move_to([3.1, 1.75, 0])
        c.play(FadeIn(l1p), FadeIn(l1), rt=0.5)
        self.bring_to_front(l1)
        c.play(FadeIn(l2), rt=0.5)

        c.at("Take scores zero")
        call = mono("probabilities([0, -1000])  ->  [1.0, 0.0]", 26)
        t = tag("constructed input").next_to(call, RIGHT, buff=0.35)
        row = VGroup(call, t)
        if row.width > 11.8:
            row.scale_to_fit_width(11.8)
        row.move_to([0, 0.95, 0])
        c.play(FadeIn(call), FadeIn(t), rt=0.8)

        c.at("The true probability")
        ax = NumberLine(x_range=[-450, 0, 50], length=11.0, color=INK, stroke_width=3).move_to([0, -0.55, 0])
        nums = VGroup(*[mono(f"1e{v}" if v else "1", 20, MUTED).next_to(ax.n2p(v), DOWN, buff=0.32)
                        for v in (-400, -300, -200, -100, 0)])
        axl = txt("size of a probability (log scale)", 20, MUTED).next_to(ax, DOWN, buff=0.55)
        c.play(Create(ax), FadeIn(nums), FadeIn(axl), rt=1.0)
        floor_x = -323.3
        fl = DashedLine(ax.n2p(floor_x) + UP * 0.95, ax.n2p(floor_x) + DOWN * 0.3, color=INK, stroke_width=4)
        fll = mono("smallest positive float: 5e-324", 20, INK).move_to(ax.n2p(floor_x) + DOWN * 1.4 + RIGHT * 2.7)
        region = Rectangle(width=ax.n2p(0)[0] - ax.n2p(floor_x)[0], height=0.5, fill_color=GOOD,
                           fill_opacity=0.18, stroke_width=0).move_to(
            [(ax.n2p(0)[0] + ax.n2p(floor_x)[0]) / 2, ax.n2p(0)[1], 0])
        rl = txt("representable as a float", 20, INK).move_to(region.get_center() + UP * 0.45)
        c.play(FadeIn(region), Create(fl), FadeIn(fll), FadeIn(rl), rt=1.0)
        dot = Dot(ax.n2p(-434.3), radius=0.1, color=ACCENT_TX)
        dl = VGroup(mono("exp(-1000)", 20, ACCENT_TX), mono("is about 5.1e-435", 20, ACCENT_TX)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        dl.move_to([-5.9, dot.get_center()[1] + 0.3 + dl.height / 2, 0], aligned_edge=LEFT)
        c.play(FadeIn(dot, scale=1.6), FadeIn(dl), rt=0.8)

        c.at("so the code returns")
        zero = mono("0.0", 30, ACCENT_TX, weight="BOLD").move_to(ax.n2p(-434.3) + DOWN * 1.25)
        c.play(ReplacementTransform(dot.copy(), zero), rt=1.0)
        ev = mono("D outcome 1 probability: 0.0 | is exactly zero: True", 22).move_to([0, -2.35, 0])
        c.play(FadeIn(ev), rt=0.6)

        c.at("And one passing test")
        last = txt("One passing test ≠ “numerically stable” for every input.", 28, INK, SERIF).move_to([0, -3.0, 0])
        c.play(FadeIn(last), rt=0.8)
        c.finish()


# ---------------------------------------------------------------- B08
class B08_Recap(Scene):
    def construct(self):
        c = Clock(self, "B08")
        self.add(kicker(KICK))
        lines = VGroup(
            txt("1.  Subtracting the max changes the weights, not the distribution:", 28, INK),
            txt("     one factor, e^max, divides every weight and the total alike.", 28, INK),
            txt("2.  It keeps the exponentials from overflowing.", 28, INK),
            txt("3.  It does not stop tiny probabilities from rounding to 0.0.", 28, ACCENT_TX),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, 1.55, 0])
        card = VGroup(
            txt("Sources", 24, INK, weight="BOLD"),
            txt("Numbers: course main.py, its tests, and evidence/max_shift_evidence.py; Python 3.14.2; run 2026-09-24", 19, INK),
            txt("Course repo nikbearbrown/info-7375-prompt-engineering-for-generative-ai @ e6c6c49  ·  Brutalist @ 6a8380a", 19, INK),
            txt("All score lists are constructed inputs. No Claude responses are shown.", 19, INK),
            txt("Narration: synthetic Kokoro voice af_bella (not a real person).", 19, INK),
            txt("Script, scenes and build drafted with Claude Code; see SOURCES.md for the split.", 19, INK),
            txt("Omkar Salian  ·  INFO 7375, Fall 2026  ·  Week 1", 22, ACCENT_TX),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        box = SurroundingRectangle(card, color=MUTED, buff=0.25, stroke_width=2)
        grp = VGroup(box, card)
        if grp.width > 12.2:
            grp.scale_to_fit_width(12.2)
        grp.move_to([0, -1.75, 0])
        c.play(FadeIn(lines[0]), FadeIn(lines[1]), FadeIn(grp), rt=0.8)
        c.at("It keeps the exponentials")
        c.play(FadeIn(lines[2]), rt=0.6)
        c.at("It does not rescue")
        c.play(FadeIn(lines[3]), rt=0.6)

        c.at("Every number in this")
        c.play(Indicate(box, color=ACCENT), rt=1.0)
        c.finish()
