"""Manim scenes for seed-repeatable-not-correct (INFO7375).

B00_Intro    — what this video explains, then what a seed does (opener)
B01_Lottery  — three boxes sized by the real softmax probabilities + the hook
B02_TwoRuns  — recorded output of two separate runs, stamped IDENTICAL
B03_Twist    — a self-declared answer key (sticky note), the real draw sequence
               as a hit/miss dot grid, the inputs, IDENTICAL ≠ CORRECT
B04_Chat     — mock chat (illustration), 'reproducible' badge crossed out
B05_Boundary — scope of the claim, verbatim

Timing: every beat conforms to its measured (hold-padded) narration via
mp3/cues.json (pad_holds.py -> cues.py). Numbers come from the evidence files
or from importing evidence/seeded_sampler.py itself; nothing is retyped.
"""
import filecmp
import json
import random
import re
import sys
from pathlib import Path

import numpy as np
from manim import *

REEL = Path(__file__).resolve().parent
EV = REEL / "evidence"
sys.path.insert(0, str(EV))
import seeded_sampler as S  # noqa: E402  (the script whose output the video shows)

CUES = json.loads((REEL / "mp3/cues.json").read_text())
PROBS = S.softmax(S.SCORES, S.TEMPERATURE)

BG, INK, ACCENT = "#F2F0E9", "#3D3929", "#D97757"
MUTED, PANEL, RULE, SOFT = "#5E5847", "#FBFAF6", "#CFC9B8", "#E4DFD2"
STICKY, STICKY_EDGE, RED, GREEN = "#F7DE72", "#D9B93F", "#C0392B", "#3F7A52"
TEAL = "#1F6F78"   # credit line on the B00 title card (user request); ~5:1 on cream
SERIF, MONO, HAND = "EB Garamond", "Menlo", "Marker Felt"
STAMP_FONT = "Avenir Next Condensed"
SAFE_X, SAFE_Y = 6.4, 3.6


def serif(s, size=40, color=INK, **kw):
    return Text(s, font=SERIF, font_size=size, color=color, **kw)


def mono(s, size=30, color=INK):
    return Text(s, font=MONO, font_size=size, color=color)


def fit(mob, max_w=2 * SAFE_X - 0.2):
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


# ---------------------------------------------------------------- clock
class Timed(Scene):
    BID = ""

    def setup(self):
        self.camera.background_color = BG
        self.cues = CUES[self.BID]["cues"]
        self.dur = CUES[self.BID]["duration"]

    def until(self, t):
        now = self.renderer.time
        if t > now + 1e-3:
            self.wait(t - now)

    def at(self, k, extra=0.0):
        self.until(self.cues[k] + extra)

    def finish(self):
        self.until(self.dur)


# run.sh discovers beat scenes by regex on the literal base-class name "Scene",
# so every beat must subclass a name spelled Scene. Rebind it to the timed base.
Scene = Timed


# ---------------------------------------------------------------- pieces
def lottery(total_w=12.2, h=2.9, equal=False, accent=True):
    """Three rounded boxes; widths proportional to the real softmax probabilities."""
    gap = 0.18
    usable = total_w - 2 * gap
    widths = [usable / 3] * 3 if equal else [usable * p for p in PROBS]
    boxes = VGroup()
    for i, w in enumerate(widths):
        fill = ACCENT if (i == 2 and not equal and accent) else SOFT
        r = RoundedRectangle(corner_radius=min(0.22, w / 3), width=w, height=h,
                             fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4)
        lab = Text(str(i), font=SERIF, font_size=110, color=INK)
        if lab.width > w - 0.15:
            lab.scale_to_fit_width(w - 0.15)
        boxes.add(VGroup(r, lab.move_to(r)))
    boxes.arrange(RIGHT, buff=gap)
    return boxes


def stamp(text, color=ACCENT, size=110, angle=-7 * DEGREES):
    t = Text(text, font=STAMP_FONT, weight=HEAVY, font_size=size, color=color)
    frame = RoundedRectangle(corner_radius=0.2, width=t.width + 0.8, height=t.height + 0.55,
                             stroke_color=color, stroke_width=12, fill_color=BG, fill_opacity=0.92)
    g = VGroup(frame, t.move_to(frame))
    g.rotate(angle)
    return g


def slam(scene, mob, run_time=0.35):
    # one animation only: FadeIn(scale=) starts 1.5x and lands at the final size
    scene.play(FadeIn(mob, scale=1.5), run_time=run_time, rate_func=rate_functions.ease_in_quad)
    scene.play(mob.animate.shift(0.06 * RIGHT), run_time=0.05)
    scene.play(mob.animate.shift(0.06 * LEFT), run_time=0.05)


def red_x(mob, color=RED, width=16):
    a, b = mob.get_corner(UL), mob.get_corner(DR)
    c, d = mob.get_corner(DL), mob.get_corner(UR)
    s1 = ArcBetweenPoints(a + [-0.1, 0.1, 0], b + [0.1, -0.1, 0], angle=-0.12,
                          color=color, stroke_width=width)
    s2 = ArcBetweenPoints(c + [-0.1, -0.1, 0], d + [0.1, 0.1, 0], angle=0.1,
                          color=color, stroke_width=width)
    return VGroup(s1, s2)


def counts_of(line):
    return {int(k): int(v) for k, v in re.findall(r"(\d+):\s*(\d+)", line.split("=", 1)[1])}


# ---------------------------------------------------------------- B00
class B00_Intro(Scene):
    """What this video explains (user-requested opener), then what a seed does."""
    BID = "B00"

    def construct(self):
        kicker = serif("This video explains:", 46, MUTED)
        title = serif("Seeded randomness", 118)
        sub = VGroup(serif("why a seed makes a run repeatable,", 54),
                     serif("but not necessarily correct", 54)).arrange(DOWN, buff=0.14)
        card = VGroup(kicker, title, sub).arrange(DOWN, buff=0.45)
        fit(card, 12.0).move_to([0, 0.35, 0])
        credit_rule = Line(LEFT * 1.6, RIGHT * 1.6, color=TEAL, stroke_width=3)
        credit = serif("Made by Aditya Hasija", 44, TEAL, slant=ITALIC)
        credit_g = VGroup(credit_rule, credit).arrange(DOWN, buff=0.22).move_to([0, -2.75, 0])

        self.at(0)
        self.play(FadeIn(kicker, shift=0.2 * DOWN), run_time=0.5)
        self.play(Write(title), run_time=1.3)
        self.at(0, 3.2)
        self.play(FadeIn(sub, shift=0.2 * UP), run_time=0.7)
        self.play(Create(credit_rule), FadeIn(credit, shift=0.15 * UP), run_time=0.6)

        # cue 1: card moves up; a seed setting beside a cloud of jittering dots
        self.at(1)
        head = VGroup(kicker, title)
        target = head.copy().scale(0.62)
        target.shift([-target.get_center()[0], (SAFE_Y - 0.12) - target.get_top()[1], 0])
        rng = np.random.default_rng(7)
        box = [-5.65, -1.05, -1.95, 1.25]                  # x0, x1, y0, y1 of the cloud
        def scatter():
            return [np.array([rng.uniform(box[0], box[1]), rng.uniform(box[2], box[3]), 0]) for _ in range(46)]
        dots = VGroup(*[Dot(p, radius=0.09, color=INK) for p in scatter()])
        field = SurroundingRectangle(VGroup(Dot([box[0], box[2], 0]), Dot([box[1], box[3], 0])),
                                     buff=0.3, corner_radius=0.2, color=RULE, stroke_width=3)
        chip_t = mono("seed: 7", 44)
        chip = VGroup(RoundedRectangle(corner_radius=0.3, width=chip_t.width + 0.8, height=1.0,
                                       fill_color=PANEL, fill_opacity=1, stroke_color=INK, stroke_width=4),
                      chip_t)
        chip_t.move_to(chip[0])
        chip.move_to([2.7, 1.1, 0])
        self.play(FadeOut(sub, shift=0.2 * UP), FadeOut(credit_g), Transform(head, target), FadeIn(field),
                  LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02), run_time=0.9)
        self.play(FadeIn(chip, scale=1.3), run_time=0.35, rate_func=rate_functions.ease_out_back)
        for _ in range(3):                                   # randomness: the cloud keeps moving
            new = scatter()
            self.play(*[d.animate.move_to(p) for d, p in zip(dots, new)], run_time=0.4,
                      rate_func=rate_functions.linear)

        # cue 2: the seed freezes it; the same output twice
        self.at(2)
        body = RoundedRectangle(corner_radius=0.08, width=0.75, height=0.6, fill_color=INK,
                                fill_opacity=1, stroke_width=0)
        shackle = Arc(radius=0.26, start_angle=0, angle=PI, color=INK, stroke_width=9)
        shackle.next_to(body, UP, buff=-0.02).shift(0.3 * UP)
        lock = VGroup(body, shackle).next_to(chip, RIGHT, buff=0.5)
        self.play(FadeIn(lock), run_time=0.25)
        self.play(shackle.animate.shift(0.3 * DOWN), field.animate.set_stroke(INK), run_time=0.25)
        outs = VGroup()
        for label in ("run 1", "run 2"):
            frame = RoundedRectangle(corner_radius=0.15, width=2.3, height=1.55, fill_color=PANEL,
                                     fill_opacity=1, stroke_color=RULE, stroke_width=3)
            mini = dots.copy().scale_to_fit_height(1.0).move_to(frame)
            outs.add(VGroup(frame, mini, serif(label, 30, MUTED).next_to(frame, DOWN, buff=0.08)))
        outs.arrange(RIGHT, buff=0.75).move_to([3.35, -0.75, 0])
        eq = serif("=", 60).move_to(VGroup(outs[0][0], outs[1][0]).get_center())
        self.play(FadeIn(outs[0], shift=0.2 * UP), run_time=0.35)
        self.play(FadeIn(outs[1], shift=0.2 * UP), FadeIn(eq), run_time=0.35)

        # cue 3: feels like reliability
        self.at(3)
        rel = serif("reliable?", 64)
        rel_box = SurroundingRectangle(rel, buff=0.18, corner_radius=0.12, color=ACCENT, stroke_width=6)
        rel_g = VGroup(rel_box, rel).move_to([4.0, -2.4, 0])
        self.play(FadeIn(rel, shift=0.15 * UP), Create(rel_box), run_time=0.5)

        # cue 4: the experiment
        self.at(4)
        tag = serif("a quick experiment, with recorded Python runs", 32, MUTED)
        tag.move_to([box[0] - 0.3 + tag.width / 2, -3.0, 0])
        self.play(FadeIn(tag), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- B01
class B01_Lottery(Scene):
    BID = "B01"

    def construct(self):
        eq = lottery(equal=True).move_to([0, 0.35, 0])
        real = lottery().move_to([0, 0.35, 0])
        tags_txt = ["about 1 in 10", "about 1 in 4", "about 2 in 3"]
        tags = VGroup(*[serif(t, 40, MUTED) for t in tags_txt])
        for tg, bx in zip(tags, real):
            tg.next_to(bx, DOWN, buff=0.3)
        # the sliver's tag sits on a second row, left-aligned, with a leader line
        tags[0].next_to(real[0], DOWN, buff=1.05).align_to(real[0], LEFT)
        leader = Line(real[0].get_bottom() + [0, -0.08, 0], tags[0].get_top() + [0.3 - tags[0].width / 2, 0.06, 0],
                      color=MUTED, stroke_width=3)
        tags[0] = VGroup(tags[0], leader)

        self.at(0)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in eq], lag_ratio=0.25),
                  run_time=1.2, rate_func=rate_functions.ease_out_back)
        self.at(1)
        self.play(ReplacementTransform(eq, real), run_time=0.7,
                  rate_func=rate_functions.ease_out_back)
        self.at(2, 0.5)
        self.play(FadeIn(tags[2], shift=0.2 * UP), run_time=0.5)
        self.at(3)
        self.play(FadeIn(tags[1], shift=0.2 * UP), run_time=0.5)
        self.play(FadeIn(tags[0], shift=0.2 * UP), run_time=0.5)

        # cue 4: a few playful draws (illustration, not the recorded run)
        self.at(4)
        for target in (2, 1, 2):
            ball = Circle(radius=0.26, fill_color=INK, fill_opacity=1, stroke_width=0)
            top = real[target].get_top() + [0, 1.2, 0]
            ball.move_to(top)
            self.play(FadeIn(ball, run_time=0.1))
            self.play(ball.animate.move_to(real[target].get_center() + [0, 0.75, 0]),
                      run_time=0.35, rate_func=rate_functions.ease_in_quad)
            self.play(ball.animate.shift(0.35 * UP), run_time=0.15, rate_func=rate_functions.ease_out_quad)
            self.play(ball.animate.shift(0.35 * DOWN), run_time=0.15, rate_func=rate_functions.ease_in_quad)
            self.play(FadeOut(ball), run_time=0.2)

        # cue 5: the seed + a lock
        self.at(5)
        seed = VGroup(Ellipse(width=0.62, height=0.9, fill_color="#8A6A3F", fill_opacity=1,
                              stroke_color=INK, stroke_width=3).rotate(-20 * DEGREES),
                      serif("seed = 7", 42))
        seed[1].next_to(seed[0], RIGHT, buff=0.25)
        body = RoundedRectangle(corner_radius=0.08, width=0.75, height=0.6, fill_color=INK,
                                fill_opacity=1, stroke_width=0)
        shackle = Arc(radius=0.26, start_angle=0, angle=PI, color=INK, stroke_width=9)
        shackle.next_to(body, UP, buff=-0.02).shift(0.3 * UP)
        lock = VGroup(body, shackle)
        badge = VGroup(seed, lock).arrange(RIGHT, buff=0.6).move_to([0, 2.95, 0])
        self.play(FadeIn(seed, shift=0.6 * DOWN), run_time=0.5, rate_func=rate_functions.ease_out_bounce)
        self.play(FadeIn(lock), run_time=0.3)
        self.play(shackle.animate.shift(0.3 * DOWN), run_time=0.2)

        # cue 6/7: the hook question
        self.at(6)
        whole = VGroup(real, tags, badge)
        target = whole.copy().scale(0.6)
        target.shift([-target.get_center()[0], (SAFE_Y - 0.15) - target.get_top()[1], 0])
        q1 = fit(serif("Same seed → same result.", 104), 12.0).move_to([0, -0.85, 0])
        self.play(Transform(whole, target), FadeIn(q1, shift=0.3 * UP), run_time=0.7)
        self.at(7)
        q2a = serif("Does that mean:", 88)
        q2b = serif("correct", 104, ACCENT)
        q2c = serif("?", 120, ACCENT)
        q2 = VGroup(q2a, q2b, q2c).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        fit(q2, 11.6).move_to([0, -2.65, 0])
        self.play(FadeIn(q2a, shift=0.2 * UP), FadeIn(q2b, shift=0.2 * UP), run_time=0.5)
        self.play(FadeIn(q2c, scale=1.8), run_time=0.35, rate_func=rate_functions.ease_out_back)
        for ang in (0.2, -0.35, 0.3, -0.15):
            self.play(Rotate(q2c, ang), run_time=0.18)
        self.finish()


# ---------------------------------------------------------------- terminals
def display_rows(name):
    """Captured file -> display rows. Display-only: the one long settings line is
    wrapped after 'temperature=1.0' so it fits a half-width panel (disclosed)."""
    rows = []
    for line in (EV / name).read_text().splitlines():
        if line.startswith("scores="):
            a, b = line.split(" seed=")
            rows += [("set", a), ("set", "seed=" + b)]
        elif line.startswith("counts"):
            rows.append(("counts", line))
        elif line.startswith("[exit"):
            rows.append(("exit", line))
        elif line.startswith("$"):
            rows.append(("cmd", line))
        else:
            rows.append(("probs", line))
    return rows


class RunPanel(VGroup):
    def __init__(self, title, rows, center, width=6.15, height=5.45):
        super().__init__()
        self.box = RoundedRectangle(corner_radius=0.16, width=width, height=height,
                                    fill_color=PANEL, fill_opacity=1, stroke_color=RULE,
                                    stroke_width=3).move_to(center)
        self.head = serif(title, 44).move_to(self.box.get_top() + [0, -0.42, 0])
        self.rule = Line(self.box.get_corner(UL) + [0.2, -0.82, 0],
                         self.box.get_corner(UR) + [-0.2, -0.82, 0], color=RULE, stroke_width=2)
        self.add(self.box, self.head, self.rule)
        left = self.box.get_left()[0] + 0.3
        self.lines, self.keys = [], []
        y = self.box.get_top()[1] - 1.2
        for key, text in rows:
            t = mono(text, 34, MUTED if key == "exit" else INK)
            t.move_to([left + t.width / 2, y, 0])
            self.lines.append(t); self.keys.append(key)
            y -= 0.5
        self.left = left
        self.counts = counts_of([t for k, t in rows if k == "counts"][0])
        # mini bar chart of the parsed counts
        base_y = self.box.get_bottom()[1] + 0.45
        self.bars, self.bar_labels = VGroup(), VGroup()
        bw, max_h, cx0 = 0.95, 1.0, self.box.get_center()[0] - 0.1
        for i in range(3):
            h = max_h * self.counts[i] / 630
            bar = Rectangle(width=bw, height=h, fill_color=ACCENT if i == 2 else SOFT,
                            fill_opacity=1, stroke_color=INK, stroke_width=3)
            bar.move_to([cx0 + 1.15 * i, base_y + h / 2, 0])
            num = serif(str(self.counts[i]), 34).next_to(bar, UP, buff=0.08)
            idx = serif(f"box {i}", 26, MUTED).next_to(bar, DOWN, buff=0.06)
            self.bars.add(bar); self.bar_labels.add(VGroup(num, idx))

    def row(self, key, n=0):
        return [l for l, k in zip(self.lines, self.keys) if k == key][n]


def fit_panels(*panels):
    k = min(1.0, *[(P.box.width - 0.6) / max(l.width for l in P.lines) for P in panels])
    for P in panels:
        for l in P.lines:
            l.scale(k, about_point=[P.left, l.get_center()[1], 0])


def grow_bar(bar, run_time):
    return GrowFromEdge(bar, DOWN, run_time=run_time)


class B02_TwoRuns(Scene):
    BID = "B02"

    def construct(self):
        L = RunPanel("run 1", display_rows("run1.txt"), [-3.2, 0.62, 0])
        R = RunPanel("run 2", display_rows("run2.txt"), [3.2, 0.62, 0])
        fit_panels(L, R)
        env = {k.strip(): v.strip() for k, v in
               (l.split(":", 1) for l in (EV / "ENV.txt").read_text().splitlines())}
        py = env["python"].split("(")[0].strip()
        cap = fit(serif(f"Recorded output  ·  {py}  ·  "
                        "2 separate runs  ·  long line wrapped", 28, MUTED))
        cap.move_to([-SAFE_X + cap.width / 2, -3.45, 0])

        def type_setup(P):
            self.play(AddTextLetterByLetter(P.row("cmd"), time_per_char=0.03), run_time=0.9)
            self.play(*[FadeIn(P.row("set", n)) for n in (0, 1)], FadeIn(P.row("probs")), run_time=0.5)

        self.at(0)
        self.play(FadeIn(L, shift=0.4 * RIGHT), FadeIn(cap), run_time=0.8)
        self.at(1)
        type_setup(L)
        seed_row = L.row("set", 1)
        ul = Underline(seed_row[:6], color=ACCENT, stroke_width=5, buff=0.06)
        self.play(Create(ul), run_time=0.4)
        self.at(2)
        self.play(FadeIn(L.row("counts"), shift=0.1 * UP), run_time=0.5)
        for i in range(3):
            self.play(grow_bar(L.bars[i], 0.7), FadeIn(L.bar_labels[i]))
            self.wait(0.9)
        self.play(FadeIn(L.row("exit")), run_time=0.3)
        self.at(3)
        self.play(FadeIn(R, shift=0.4 * LEFT), run_time=0.6)
        type_setup(R)
        self.at(4)
        self.play(FadeIn(R.row("counts"), shift=0.1 * UP), run_time=0.4)
        for i in range(3):
            self.play(grow_bar(R.bars[i], 0.45), FadeIn(R.bar_labels[i]))
            self.play(Indicate(L.bar_labels[i][0], color=ACCENT), Indicate(R.bar_labels[i][0], color=ACCENT),
                      run_time=0.45)
        self.play(FadeIn(R.row("exit")), run_time=0.2)
        self.at(5)
        st = stamp("IDENTICAL", size=96, angle=-4 * DEGREES).move_to([0, -1.72, 0])
        slam(self, st)
        self.at(6)
        same = filecmp.cmp(EV / "run1.txt", EV / "run2.txt", shallow=False)
        note = serif("run1.txt == run2.txt  (byte-identical)" if same
                     else "run1.txt != run2.txt", 30, INK)
        note.move_to([0, -2.98, 0])
        self.play(FadeIn(note, shift=0.1 * UP), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- B03
def sticky_note():
    paper = Polygon([-2.7, -1.45, 0], [2.7, -1.45, 0], [2.7, 1.12, 0], [2.33, 1.45, 0],
                    [-2.7, 1.45, 0], fill_color=STICKY, fill_opacity=1,
                    stroke_color=STICKY_EDGE, stroke_width=3)
    shadow = paper.copy().set_fill(INK, 0.18).set_stroke(width=0).shift([0.1, -0.12, 0])
    tape = Rectangle(width=1.3, height=0.36, fill_color=WHITE, fill_opacity=0.55,
                     stroke_width=0).move_to([0, 1.45, 0]).rotate(4 * DEGREES)
    l1 = Text("outcome 0 = the correct answer", font=HAND, font_size=46, color=INK)
    l2 = Text("(I\u2019m declaring this myself,", font=HAND, font_size=40, color=INK)
    l3 = Text("for this experiment)", font=HAND, font_size=40, color=INK)
    words = VGroup(l1, l2, l3).arrange(DOWN, buff=0.14)
    if words.width > 4.95:
        words.scale_to_fit_width(4.95)
    words.move_to(paper.get_center() + [0, -0.05, 0])
    return VGroup(shadow, paper, words, tape)


def draw_sequence():
    """The exact 1000 draws seeded_sampler.py makes (same seed, same call)."""
    picks = random.Random(S.SEED).choices(range(len(PROBS)), weights=PROBS, k=S.COUNT)
    counts = {i: picks.count(i) for i in range(3)}
    assert counts == S.sample(PROBS, S.SEED, S.COUNT)
    return picks, counts


class B03_Twist(Scene):
    BID = "B03"

    def construct(self):
        picks, counts = draw_sequence()
        hits, misses = counts[0], S.COUNT - counts[0]
        lot = lottery(total_w=6.0, h=1.7, accent=False).move_to([3.1, 2.4, 0])  # B03's focus is box 0
        note = sticky_note().scale(0.9).rotate(4 * DEGREES).move_to([-3.75, 2.1, 0])
        arrow = CurvedArrow(note[1].get_right() + [0.12, -0.2, 0], lot[0].get_left() + [-0.08, 0.0, 0],
                            angle=0.6, color=INK, stroke_width=6, tip_length=0.28)
        tag = serif("HYPOTHETICAL: stipulated by me, not by the program", 30, INK, slant=ITALIC)
        tagbox = DashedVMobject(SurroundingRectangle(tag, buff=0.14, color=INK, stroke_width=3),
                                num_dashes=60)
        tagg = VGroup(tagbox, tag)
        fit(tagg, 9.4)
        tagg.move_to([-SAFE_X + 0.15 + tagg.width / 2, 0.36, 0])

        # 1000-dot grid of the real draw sequence: box-0 draws (hits) ink, others grey
        cols, rows_, sp = 50, 20, 0.14
        dots = VGroup(*[Dot(radius=0.056, color=INK if p == 0 else "#A39B86") for p in picks])
        for k, d in enumerate(dots):
            d.move_to([-SAFE_X + 0.2 + (k % cols) * sp, -0.3 - (k // cols) * sp, 0])
        grid = dots
        tally = VGroup(
            VGroup(serif(str(hits), 96), serif("picks of box 0", 34, MUTED)).arrange(DOWN, buff=0.05),
            VGroup(serif(str(misses), 96, MUTED), serif("misses", 34, MUTED)).arrange(DOWN, buff=0.05),
        ).arrange(DOWN, buff=0.35).move_to([4.75, -1.85, 0])
        cap = serif(f"The real {S.COUNT} draws, in order (seed {S.SEED})", 32, MUTED)
        cap.next_to(grid, DOWN, buff=0.12).align_to(grid, LEFT)

        self.at(0)
        self.play(FadeIn(lot, shift=0.3 * LEFT), run_time=0.7)
        self.at(1)
        self.play(FadeIn(note, scale=1.25), run_time=0.3, rate_func=rate_functions.ease_in_quad)
        self.play(Create(arrow), run_time=0.5)
        self.at(2)
        self.play(FadeIn(tagg, shift=0.1 * UP), run_time=0.5)
        self.at(3)
        self.play(LaggedStart(*[FadeIn(d) for d in grid], lag_ratio=0.004), run_time=2.8)
        self.play(FadeIn(tally[0], shift=0.2 * UP), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(tally[1], shift=0.2 * UP), run_time=0.5)

        # cue 4: 100 of 100 runs identical (evidence/run100.txt)
        self.at(4)
        lines = (EV / "run100.txt").read_text().splitlines()
        cl = [l for l in lines if "counts =" in l]
        n_same = int(cl[0].split()[0]) if len(cl) == 1 else 0
        label = serif(f"{n_same} of 100 runs: identical", 44)
        cards = VGroup()
        for k in range(6):
            c = RoundedRectangle(corner_radius=0.1, width=5.0, height=0.85, fill_color=PANEL,
                                 fill_opacity=1, stroke_color=RULE, stroke_width=2)
            txt = mono(cl[0].split(None, 1)[1], 30).scale_to_fit_width(4.7).move_to(c)
            cards.add(VGroup(c, txt).move_to([3.85, -1.0 - 0.07 * k, 0]))
        label = fit(label, 5.0).next_to(cards, DOWN, buff=0.35)
        self.play(FadeOut(tally, shift=0.2 * DOWN), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=0.5 * DOWN) for c in cards], lag_ratio=0.25),
                  run_time=1.3)
        self.play(FadeIn(label, scale=1.2), run_time=0.4)

        # cue 5: the only inputs
        self.at(5)
        self.play(*[FadeOut(m) for m in (lot, note, arrow, tagg, grid, cap, cards, label)], run_time=0.5)
        chips_txt = [f"scores = {S.SCORES}", f"temperature = {S.TEMPERATURE}",
                     f"seed = {S.SEED}", f"count = {S.COUNT}"]
        chips = VGroup()
        for t in chips_txt:
            tx = mono(t, 36)
            box = RoundedRectangle(corner_radius=0.25, width=tx.width + 0.6, height=0.85,
                                   fill_color=PANEL, fill_opacity=1, stroke_color=INK, stroke_width=3)
            chips.add(VGroup(box, tx.move_to(box)))
        chips.arrange(DOWN, buff=0.35, aligned_edge=RIGHT)
        fit(chips, 4.3)
        chips.shift([-1.75 - chips.get_right()[0], 0.6 - chips.get_center()[1], 0])
        sampler = VGroup(RoundedRectangle(corner_radius=0.3, width=3.4, height=2.2, fill_color=SOFT,
                                          fill_opacity=1, stroke_color=INK, stroke_width=5),
                         serif("sampler", 56)).move_to([1.2, 0.6, 0])
        sampler[1].move_to(sampler[0])
        recorded = (EV / "run1.txt").read_text().split("counts = ")[1].splitlines()[0]
        out = VGroup(serif("output: counts", 36, MUTED), mono(recorded, 36)).arrange(DOWN, buff=0.12)
        out.move_to([1.2, -2.35, 0])
        arrows = VGroup(*[Arrow(c.get_right(), sampler[0].get_left(), buff=0.12, color=INK,
                                stroke_width=4, tip_length=0.2) for c in chips])
        out_arrow = Arrow(sampler[0].get_bottom(), out.get_top(), buff=0.12, color=INK,
                          stroke_width=5, tip_length=0.25)
        self.play(LaggedStart(*[FadeIn(c, shift=0.4 * RIGHT) for c in chips], lag_ratio=0.25),
                  FadeIn(sampler), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=0.8)
        self.play(GrowArrow(out_arrow), FadeIn(out), run_time=0.5)

        # cue 6: answer key is not an input
        self.at(6)
        gt = serif("answer key?", 40, MUTED, slant=ITALIC)
        gbox = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=gt.width + 0.6, height=0.85,
                                               stroke_color=MUTED, stroke_width=3), num_dashes=40)
        ghost = VGroup(gbox, gt.move_to(gbox)).move_to([4.6, 3.0, 0])
        self.play(FadeIn(ghost, shift=0.3 * DOWN), run_time=0.4)
        self.play(ghost.animate.move_to([3.35, 1.55, 0]), run_time=0.45, rate_func=rate_functions.ease_in_quad)
        self.play(ghost.animate.move_to([4.6, 2.2, 0]), run_time=0.4, rate_func=rate_functions.ease_out_quad)
        nope = serif("not an input", 40, RED).next_to(ghost, DOWN, buff=0.25)
        self.play(FadeIn(nope), ghost.animate.set_opacity(0.45), run_time=0.4)

        # cue 7/8: IDENTICAL -> red X -> IDENTICAL ≠ CORRECT
        self.at(7)
        self.play(*[FadeOut(m) for m in (chips, arrows, sampler, out, out_arrow, ghost, nope)],
                  run_time=0.3)
        st = stamp("IDENTICAL", size=130)
        fit(st, 11.0).move_to([0, 0.2, 0])
        slam(self, st, run_time=0.3)
        self.at(8)
        x = red_x(st[0])
        self.play(Create(x[0]), run_time=0.22)
        self.play(Create(x[1]), run_time=0.22)
        final = VGroup(Text("IDENTICAL", font=STAMP_FONT, weight=HEAVY, font_size=120, color=INK),
                       Text("≠", font=SERIF, font_size=150, color=ACCENT),
                       Text("CORRECT", font=STAMP_FONT, weight=HEAVY, font_size=120, color=INK)
                       ).arrange(RIGHT, buff=0.4)
        fit(final, 12.0).move_to([0, -2.25, 0])
        self.play(VGroup(st, x).animate.scale(0.72).move_to([0, 1.3, 0]), run_time=0.45)
        self.play(FadeIn(final[0], shift=0.2 * UP), run_time=0.3)
        self.play(FadeIn(final[1], scale=1.6), run_time=0.3, rate_func=rate_functions.ease_out_back)
        self.play(FadeIn(final[2], shift=0.2 * UP), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------- B04
def bubble(text, user, width_max=5.6):
    t = Text(text, font="Avenir Next", font_size=40, color=INK if not user else BG)
    if t.width > width_max - 0.6:
        t.scale_to_fit_width(width_max - 0.6)
    b = RoundedRectangle(corner_radius=0.32, width=t.width + 0.7, height=t.height + 0.55,
                         fill_color=INK if user else PANEL, fill_opacity=1,
                         stroke_color=INK, stroke_width=2 if not user else 0)
    return VGroup(b, t.move_to(b))


class B04_Chat(Scene):
    BID = "B04"

    def construct(self):
        win = RoundedRectangle(corner_radius=0.3, width=7.6, height=6.35, fill_color=PANEL,
                               fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to([-2.35, 0.2, 0])
        bar = VGroup(*[Dot(radius=0.07, color=RULE) for _ in range(3)]).arrange(RIGHT, buff=0.12)
        bar.move_to(win.get_corner(UL) + [0.55, -0.35, 0])
        title = serif("chat (mock)", 30, MUTED).move_to(win.get_top() + [0, -0.35, 0])
        avatar = lambda: VGroup(Circle(radius=0.3, fill_color=SOFT, fill_opacity=1, stroke_color=INK,
                                       stroke_width=2), Text("AI", font="Avenir Next", weight=BOLD,
                                                             font_size=24, color=INK))
        left, right = win.get_left()[0] + 0.35, win.get_right()[0] - 0.35
        ys = [1.9, 0.85, -0.35, -1.4]

        def user_b(y):
            b = bubble("What\u2019s the capital of Australia?", True)
            return b.move_to([right - b.width / 2, y, 0])

        def ai_b(y):
            a = avatar(); a[1].move_to(a[0])
            b = bubble("Sydney.", False)
            g = VGroup(a, b).arrange(RIGHT, buff=0.2)
            return g.move_to([left + g.width / 2, y, 0])

        cap = serif("Illustration: mock chat, not a real transcript", 28, MUTED)
        cap.move_to([-SAFE_X + cap.width / 2, -3.45, 0])

        self.at(0)
        self.play(FadeIn(win, scale=0.95), FadeIn(bar), FadeIn(title), FadeIn(cap), run_time=0.5)
        u1 = user_b(ys[0])
        self.play(FadeIn(u1, shift=0.2 * UP), run_time=0.35)
        self.wait(0.5)
        a1 = ai_b(ys[1])
        self.play(FadeIn(a1, shift=0.2 * UP, scale=0.9), run_time=0.35, rate_func=rate_functions.ease_out_back)
        self.at(1)
        u2 = user_b(ys[2])
        self.play(FadeIn(u2, shift=0.2 * UP), run_time=0.35)
        self.wait(0.6)
        a2 = ai_b(ys[3])
        self.play(FadeIn(a2, shift=0.2 * UP, scale=0.9), run_time=0.35, rate_func=rate_functions.ease_out_back)
        self.play(Indicate(a1[1][1], color=INK, scale_factor=1.12), Indicate(a2[1][1], color=INK, scale_factor=1.12),
                  run_time=0.6)

        # cue 2: reproducible badge
        self.at(2)
        tick = VMobject(stroke_color=GREEN, stroke_width=10).set_points_as_corners(
            [[-0.25, 0, 0], [-0.05, -0.22, 0], [0.32, 0.25, 0]])
        word = serif("reproducible", 50, GREEN)
        inner = VGroup(tick, word).arrange(RIGHT, buff=0.25)
        frame = RoundedRectangle(corner_radius=0.4, width=inner.width + 0.8, height=inner.height + 0.6,
                                 stroke_color=GREEN, stroke_width=7, fill_color=BG, fill_opacity=1)
        badge = VGroup(frame, inner.move_to(frame))
        fit(badge, 4.4).rotate(5 * DEGREES).move_to([4.05, 2.2, 0])
        slam(self, badge, run_time=0.3)

        # cue 3: crossed out
        self.at(3)
        x = red_x(badge[0], width=13)
        self.play(Create(x[0]), run_time=0.2)
        self.play(Create(x[1]), run_time=0.2)
        sub = VGroup(serif("describes the process,", 38), serif("not the answer", 38)).arrange(DOWN, buff=0.1)
        sub.move_to([4.05, 0.75, 0])
        self.play(FadeIn(sub, shift=0.1 * UP), run_time=0.5)

        # cue 4: the fact
        self.at(4)
        fact_box = RoundedRectangle(corner_radius=0.25, width=4.3, height=2.1, fill_color=PANEL,
                                    fill_opacity=1, stroke_color=ACCENT, stroke_width=6)
        fact = VGroup(serif("Actual capital:", 38, MUTED), serif("Canberra", 72, ACCENT)).arrange(DOWN, buff=0.1)
        card = VGroup(fact_box, fact.move_to(fact_box)).move_to([4.05, -1.55, 0])
        self.play(FadeIn(card, shift=0.4 * LEFT), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- B05
class B05_Boundary(Scene):
    BID = "B05"

    def construct(self):
        head = serif("What this example does, and doesn\u2019t, show", 60)
        s1 = VGroup(serif("This example uses a constructed answer key", 48),
                    serif("I assigned myself, not a real fact-check.", 48)).arrange(DOWN, buff=0.14)
        s2 = VGroup(serif("It shows one thing clearly: repeatability and correctness", 48),
                    serif("are answers to different questions.", 48)).arrange(DOWN, buff=0.14)
        s3 = VGroup(serif("It does not claim seeds are bad,", 48),
                    serif("or that this failure happens every time.", 48)).arrange(DOWN, buff=0.14)
        foot = serif("Kokoro narration (local)  \u00b7  Manim  \u00b7  evidence in evidence/", 28, MUTED)
        card = VGroup(head, s1, s2, s3, foot)
        for a, b, g in ((head, s1, 0.55), (s1, s2, 0.5), (s2, s3, 0.5), (s3, foot, 0.5)):
            b.next_to(a, DOWN, buff=g)
        if card.height > 2 * SAFE_Y - 0.2:
            card.scale_to_fit_height(2 * SAFE_Y - 0.2)
        fit(card, 12.0)
        card.move_to([0.2, 0, 0])
        sents = [s1, s2, s3]
        for s_ in sents:
            s_.set_color(MUTED)
        mark = Line(UP, DOWN, color=ACCENT, stroke_width=10)

        def bar_for(s_):
            return Line(s_.get_corner(UL) + [-0.35, 0, 0], s_.get_corner(DL) + [-0.35, 0, 0],
                        color=ACCENT, stroke_width=10)

        self.at(0)
        mark.become(bar_for(s1))
        self.play(FadeIn(head), *[FadeIn(s_) for s_ in sents], FadeIn(foot), run_time=0.6)
        self.play(s1.animate.set_color(INK), Create(mark), run_time=0.4)
        for k, s_ in ((1, s2), (2, s3)):
            self.at(k)
            self.play(sents[k - 1].animate.set_color(MUTED), s_.animate.set_color(INK),
                      mark.animate.become(bar_for(s_)), run_time=0.5)
        self.finish()
