"""Manim body beats for "Subtract the Max" (INFO 7375, Week 1).

Every number on screen is read from code/evidence.json (written by
code/evidence.py, which runs the course's own main.py). Nothing is typed in.
Equations are typeset with matplotlib mathtext -> SVG (no LaTeX install).
Scene length = the beat's measured narration length from beat_sheet.json, and
each reveal is cued to where its phrase falls in that beat's narration.

Render one beat (from the reel folder):
    ./render_manim.sh B02   (or: manim -r 1920,1080 --fps 30 scenes.py B02TwoRoutes)
"""
import hashlib
import json
import os
from pathlib import Path

import manimpango
from manim import (DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, ORIGIN, Create, FadeIn,
                   FadeOut, Line, ReplacementTransform, Scene, SVGMobject, Text,
                   TransformMatchingShapes, VGroup, Write, config, Arrow,
                   SurroundingRectangle, Rectangle, Brace, GrowFromEdge)

REEL = Path(__file__).resolve().parent
# Fonts come from the brutalist.art checkout: $BRUTALIST_HOME, else a sibling folder.
TOOLKIT = Path(os.environ.get("BRUTALIST_HOME", REEL.parent / "brutalist.art"))
EV = json.loads((REEL / "code" / "evidence.json").read_text(encoding="utf-8"))
SHEET = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
BEATS = {b["beat_id"]: b for b in SHEET["beats"]}

# Claude fidelity palette (runtime/remotion/src/tokens/claude.ts)
PAGE, INK, INK_SOFT, SPARK = "#FAF9F5", "#3D3929", "#73705F", "#D97757"
# Text colours that pass WCAG 4.5:1 on PAGE (GATE T): SPARK itself is 2.96:1, so it is used
# only for drawn marks (asterisk, strike-throughs, braces); accent TEXT uses a deeper step.
ACCENT, WARN = "#B4532F", "#8C3B24"   # 4.72:1 and 7.21:1
config.background_color = PAGE
config.pixel_width, config.pixel_height, config.frame_rate = 1920, 1080, 30

FONTS = TOOLKIT / "runtime" / "fonts"
for ttf in [*FONTS.glob("EB_Garamond/static/*.ttf"), *FONTS.glob("Lato/static/*.ttf"),
            FONTS / "PT_Mono" / "PTMono-Regular.ttf"]:
    manimpango.register_font(str(ttf))
SERIF, SANS, MONO = "EB Garamond", "Lato", "PT Mono"

RUN = EV["run"]
FOOTER = f"Printed by evidence.py, Python {RUN['python']}, {RUN['date']}"


def f4(x):
    return f"{x:.4f}"


def f3(x):
    return f"{x:.3f}"


def signed(x):
    return f"{x:g}".replace("-", "−")


def arr(xs, fmt=signed):
    return "[" + ", ".join(fmt(x) for x in xs) + "]"


def T(s, size=40, color=INK, font=SANS, weight="NORMAL"):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def N(s, size=52, color=INK):
    return Text(s, font=MONO, font_size=size, color=color)


MATH_DIR = REEL / "_math"


def M(expr, height=0.9, color=INK):
    """Structured math: matplotlib mathtext -> outlined SVG -> SVGMobject."""
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import mathtext
    from matplotlib.font_manager import FontProperties
    MATH_DIR.mkdir(exist_ok=True)
    path = MATH_DIR / (hashlib.sha1(expr.encode()).hexdigest()[:12] + ".svg")
    if not path.exists():
        with matplotlib.rc_context({"mathtext.fontset": "stix", "svg.fonttype": "path",
                                    "svg.hashsalt": "subtract-the-max",
                                    "savefig.transparent": True}):
            mathtext.math_to_image("$" + expr + "$", str(path),
                                   prop=FontProperties(size=48), format="svg", color=INK)
    mob = SVGMobject(str(path))
    # Drop matplotlib's figure-background patch: a plain rectangle covering most of the figure.
    W, H = mob.width, mob.height
    for parent in mob.get_family():
        for part in list(parent.submobjects):
            if part.has_points() and len(part.points) <= 16 and part.width * part.height > 0.5 * W * H:
                parent.remove(part)
    mob.set_fill(color, opacity=1).set_stroke(width=0)
    mob.scale_to_fit_height(height)
    return mob


def spark(size=0.42, color=SPARK):
    """The terracotta asterisk, drawn (EB Garamond has no U+2731 glyph)."""
    import numpy as np
    return VGroup(*[Line(ORIGIN, size / 2 * np.array([np.cos(a), np.sin(a), 0]),
                         color=color, stroke_width=7)
                    for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)])


def labeled(mob, label, y):
    """An input and its provenance tag, centered as one group (never off-frame)."""
    return VGroup(mob, label).arrange(RIGHT, buff=0.45).move_to([0, y, 0])


def maps(a, b, size=48, color=INK):
    """`a` then a drawn arrow then `b` (a drawn arrow stays legible where the glyph is thin)."""
    left, right = N(a, size, color), N(b, size, color)
    arrow = Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, color=INK_SOFT, stroke_width=5,
                  max_tip_length_to_length_ratio=0.35)
    return VGroup(left, arrow, right).arrange(RIGHT, buff=0.25)


# Title-safe inset (brutalist runtime/remotion/src/tokens/layout.ts SAFE: x 96-1824, y 54-1026 px
# at 1920x1080). In Manim units: 96 px = 0.711, 54 px = 0.4. Anchor corners a little inside it.
SAFE_X, SAFE_Y = 0.78, 0.46


def safe_corner(mob, corner):
    mob.to_edge(LEFT if corner[0] < 0 else RIGHT, buff=SAFE_X)
    mob.to_edge(UP if corner[1] > 0 else DOWN, buff=SAFE_Y)
    return mob


def tag(s, color=ACCENT):
    t = T(s, 26, color, weight="BOLD")
    box = SurroundingRectangle(t, color=color, buff=0.12, stroke_width=2, corner_radius=0)
    return VGroup(box, t)


class Beat(Scene):
    BEAT = ""
    HEADING = ""

    def setup(self):
        beat = BEATS[self.BEAT]
        self.dur = float(beat["actual_duration_s"])
        self.text = beat["narration_text"]
        self.t = 0.0
        heading = VGroup(spark(), T(self.HEADING, 52, INK, SERIF))
        safe_corner(heading.arrange(RIGHT, buff=0.25), UL)
        foot = safe_corner(T(FOOTER, 36, INK_SOFT), DL)
        # Author credit lives in B00, the composer chips and the outro; body beats keep the
        # corners free so long headings never collide with it.
        self.add(heading, foot)

    def cue(self, phrase):
        """Time (s) at which `phrase` is spoken, by its position in the narration."""
        i = self.text.find(phrase)
        assert i >= 0, f"{self.BEAT}: cue phrase not in narration: {phrase!r}"
        return self.dur * i / len(self.text)

    def play_at(self, when, *anims, run_time=0.8):
        if when > self.t:
            self.wait(when - self.t)
            self.t = when
        self.play(*anims, run_time=run_time)
        self.t += run_time

    def finish(self):
        if self.dur - self.t > 0.02:
            self.wait(self.dur - self.t)


class B02TwoRoutes(Beat):
    BEAT, HEADING = "B02", "Two routes, one answer"

    def construct(self):
        c = EV["cases"]["chapter"]
        d, s = c["direct"], c["shifted"]
        z = N(arr(c["logits"]), 60)
        ztag = tag("constructed input (Chapter 1) · T = 1")
        labeled(z, ztag, 2.05)
        self.play_at(0.2, FadeIn(z), FadeIn(ztag))

        xl, xr = -3.6, 3.6
        hl = M(r"e^{z}", 0.75).move_to([xl, 1.2, 0])
        hr = M(r"e^{z-3}", 0.75).move_to([xr, 1.2, 0])
        ys = [0.25, -0.6, -1.45]
        left = VGroup(*[maps(f"{zi}", f3(w)).move_to([xl, y, 0])
                        for zi, w, y in zip(c["logits"], d["weights"], ys)])
        right = VGroup(*[maps(signed(si), f3(w)).move_to([xr, y, 0])
                         for si, w, y in zip(s["shifted"], s["weights"], ys)])
        tl = N(f"total {f3(d['total'])}", 40, INK_SOFT).move_to([xl, -2.35, 0])
        tr = N(f"total {f3(s['total'])}", 40, INK_SOFT).move_to([xr, -2.35, 0])

        t = self.cue("Left route")
        self.play_at(t, FadeIn(hl, shift=DOWN * 0.2), run_time=0.6)
        for i, row in enumerate(left):
            self.play_at(self.cue(["two point seven", "seven point four", "twenty point one"][i]),
                         FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
        self.play_at(self.t + 0.1, FadeIn(tl), run_time=0.4)

        self.play_at(self.cue("Right route"), FadeIn(hr, shift=DOWN * 0.2), run_time=0.6)
        for i, row in enumerate(right):
            self.play_at(self.cue(["minus two", "minus one", "zero, which"][i]),
                         FadeIn(row, shift=LEFT * 0.3), run_time=0.5)
        self.play_at(self.cue("Different weights"), FadeIn(tr), run_time=0.4)

        pl = VGroup(*[N(f4(p), 52).move_to([xl, y, 0]) for p, y in zip(d["probs"], ys)])
        pr = VGroup(*[N(f4(p), 52).move_to([xr, y, 0]) for p, y in zip(s["probs"], ys)])
        dl = N(f"÷ {f3(d['total'])}", 40, ACCENT).move_to(tl)
        dr = N(f"÷ {f3(s['total'])}", 40, ACCENT).move_to(tr)
        self.play_at(self.cue("Now divide"), ReplacementTransform(tl, dl), ReplacementTransform(tr, dr),
                     run_time=0.6)
        self.play_at(self.t + 0.3, ReplacementTransform(left, pl), ReplacementTransform(right, pr),
                     run_time=1.2)
        eq = VGroup(*[T("=", 64, ACCENT, weight="BOLD").move_to([0, y, 0]) for y in ys])
        same = T("same", 48, ACCENT, weight="BOLD").move_to([0, 1.2, 0])
        self.play_at(self.cue("Both columns"), FadeIn(eq), FadeIn(same), run_time=0.7)
        self.finish()


class B03Cancel(Beat):
    BEAT, HEADING = "B03", "Why it cancels"

    def construct(self):
        c = EV["cases"]["chapter"]
        d, s = c["direct"], c["shifted"]
        ident = M(r"e^{z_i - m} \;=\; e^{z_i}\, e^{-m}", 0.75).move_to(UP * 2.05)
        self.play_at(0.2, Write(ident), run_time=1.0)

        xs = [-3.8, 0, 3.8]
        top = VGroup(*[N(f3(w), 56).move_to([x, 0.75, 0]) for w, x in zip(d["weights"], xs)])
        factor = VGroup(T("×", 48, ACCENT), M(r"e^{-3}", 0.6, ACCENT),
                        N(f"= {EV['factor_exp_minus_3']:.4f}", 40, ACCENT)).arrange(RIGHT, buff=0.2)
        factor.move_to(UP * 0.0)
        bottom = VGroup(*[N(f3(w), 56).move_to([x, 0.75, 0]) for w, x in zip(s["weights"], xs)])
        self.play_at(self.cue("multiplies every weight"), FadeIn(top), run_time=0.6)
        self.play_at(self.cue("e to the minus three"), FadeIn(factor), run_time=0.6)
        self.play_at(self.cue("Twenty point one times"), ReplacementTransform(top, bottom),
                     run_time=1.2)

        # The fraction, composed so the cancelled factor can be struck in place.
        num = VGroup(M(r"e^{z_i}", 0.85), M(r"e^{-m}", 0.85)).arrange(RIGHT, buff=0.15)
        den = VGroup(M(r"\sum_j e^{z_j}", 1.3), M(r"e^{-m}", 0.85)).arrange(RIGHT, buff=0.15)
        frac = VGroup(num, den).arrange(DOWN, buff=0.45)
        bar = Line(LEFT, RIGHT, color=INK, stroke_width=4).set_width(den.width + 0.3)
        bar.move_to((num.get_bottom() + den.get_top()) / 2)
        fr = VGroup(M(r"p_i", 0.7), T("=", 56), VGroup(frac, bar)).arrange(RIGHT, buff=0.3)
        fr.move_to(DOWN * 1.75 + LEFT * 3.4)
        self.play_at(self.cue("The top of the fraction"),
                     FadeOut(factor), bottom.animate.scale(0.85), FadeIn(fr), run_time=0.8)
        strikes = VGroup(*[Line(m.get_corner(DL), m.get_corner(UR), color=SPARK, stroke_width=6)
                           for m in (num[1], den[1])])
        self.play_at(self.cue("so it cancels"), Create(strikes), run_time=0.6)

        r1 = d["weights"][2] / d["weights"][1]
        r2 = s["weights"][2] / s["weights"][1]
        ratios = VGroup(N(f"{f3(d['weights'][2])} / {f3(d['weights'][1])} = {f3(r1)}", 32),
                        N(f"{f3(s['weights'][2])} / {f3(s['weights'][1])} = {f3(r2)}", 32, ACCENT)
                        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 1.85 + RIGHT * 2.9)
        rl = T("ratio unchanged", 28, INK_SOFT).next_to(ratios, UP, buff=0.3)
        self.play_at(self.cue("The ratios"), FadeIn(ratios), FadeIn(rl), run_time=0.8)
        self.finish()


class B04Overflow(Beat):
    BEAT, HEADING = "B04", "Where it matters"

    def construct(self):
        c = EV["cases"]["test_02"]
        z = N(arr(c["logits"]), 56)
        ztag = tag("lesson test input \u00b7 test_02")
        labeled(z, ztag, 2.05)
        self.play_at(self.cue("a thousand and"), FadeIn(z), FadeIn(ztag), run_time=0.6)

        xl, xr = -3.4, 3.4
        hl = T("direct", 32, INK_SOFT, weight="BOLD").move_to([xl, 1.05, 0])
        hr = T("shifted (main.py)", 32, INK_SOFT, weight="BOLD").move_to([xr, 1.05, 0])
        call = N(">>> math.exp(1000)", 34).move_to([xl, 0.35, 0])
        err = N(EV["exp_1000_traceback_last_line"], 24, WARN).move_to([xl + 0.3, -0.3, 0])
        self.play_at(self.cue("Direct route"), FadeIn(hl), FadeIn(call), run_time=0.6)
        self.play_at(self.cue("raises an OverflowError"), FadeIn(err, scale=1.1), run_time=0.5)

        e709 = N(f"exp(709) = {EV['exp_709']:.3e}   fits", 26).move_to([xl, -1.2, 0])
        e710 = N(f"exp(710)   {EV['exp_710'].split(':')[0]}", 26, WARN)
        e710.next_to(e709, DOWN, buff=0.22).align_to(e709, LEFT)
        self.play_at(self.cue("seven hundred nine"), FadeIn(e709), run_time=0.5)
        self.play_at(self.cue("seven hundred ten"), FadeIn(e710), run_time=0.5)

        s_ = c["shifted"]
        steps = [N(arr(s_["shifted"]), 40), N(arr(s_["weights"]), 40), N(arr(s_["probs"]), 48, ACCENT)]
        for k, st in enumerate(steps):
            st.move_to([xr, 0.35 - 0.9 * k, 0])
        arrows = VGroup(*[Arrow(steps[k].get_bottom(), steps[k + 1].get_top(), buff=0.06,
                                color=INK_SOFT, stroke_width=3, max_tip_length_to_length_ratio=0.3)
                          for k in range(2)])
        self.play_at(self.cue("Shifted route"), FadeIn(hr), FadeIn(steps[0]), run_time=0.5)
        self.play_at(self.cue("then one and one"), FadeIn(arrows[0]), FadeIn(steps[1]), run_time=0.5)
        self.play_at(self.cue("then one half"), FadeIn(arrows[1]), FadeIn(steps[2]), run_time=0.5)

        lt = EV["lesson_tests"]
        res = N(f"python -m unittest: Ran {lt['ran']} tests, {'OK' if lt['ok'] else 'FAILED'}", 26,
                ACCENT).move_to([0, -2.65, 0])
        self.play_at(self.cue("the test passes"), FadeIn(res), run_time=0.5)
        self.finish()


class B05Offset(Beat):
    BEAT, HEADING = "B05", "Only the gaps matter"

    def construct(self):
        a, b = EV["cases"]["chapter"], EV["cases"]["offset"]
        ra = N(arr(a["logits"]), 48).move_to([-2.9, 1.55, 0])
        rb = N(arr(b["logits"]), 48).move_to([-2.9, 0.45, 0])
        tg = tag("constructed input").next_to(rb, RIGHT, buff=0.4)
        self.play_at(0.2, FadeIn(ra), run_time=0.5)
        self.play_at(self.cue("Add a thousand"), FadeIn(rb), FadeIn(tg), run_time=0.6)
        crash = N(f"direct: {b['direct']['error'].split(':')[0]}", 28, WARN).next_to(tg, DOWN, buff=0.3)
        crash.align_to(tg, LEFT)
        self.play_at(self.cue("The direct route crashes"), FadeIn(crash), run_time=0.5)

        sa = N(arr(a["shifted"]["shifted"]), 48).move_to([-2.9, -1.1, 0])
        sb = sa.copy()
        lab = T("both, after subtracting their max", 26, INK_SOFT).next_to(sa, DOWN, buff=0.3)
        self.play_at(self.cue("The shifted route produces"),
                     ReplacementTransform(ra.copy(), sa), ReplacementTransform(rb.copy(), sb),
                     FadeIn(lab), run_time=1.3)
        probs = VGroup(Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=INK_SOFT, stroke_width=5,
                               max_tip_length_to_length_ratio=0.35),
                         N(arr(a["shifted"]["probs"], f4), 30, INK)).arrange(RIGHT, buff=0.2).next_to(sa, RIGHT, buff=0.3)
        self.play_at(self.cue("the very same distribution"), FadeIn(probs), run_time=0.6)

        gaps = VGroup()
        for row in (ra, rb):
            b1 = Brace(row, UP, buff=0.08, color=SPARK)
            gaps.add(VGroup(b1, T("gaps: 1, 1", 26, ACCENT, weight="BOLD").next_to(b1, UP, buff=0.05)))
        gaps[1].shift(DOWN * 0.02)
        offset = T("the shared +1000 offset carries no preference", 28, INK_SOFT).move_to([0, -2.6, 0])
        self.play_at(self.cue("An offset shared"), FadeIn(offset), FadeIn(gaps[0]), run_time=0.7)
        self.play_at(self.cue("only listens to the gaps"), offset.animate.set_opacity(0.45), run_time=0.6)
        self.finish()


class B06Boundary(Beat):
    BEAT, HEADING = "B06", "What this does not establish"

    def construct(self):
        c = EV["cases"]["boundary"]
        z = N(arr(c["logits"]), 56)
        tg = tag("constructed input")
        VGroup(z, tg).arrange(RIGHT, buff=0.4).move_to([-1.9, 2.05, 0])
        self.play_at(self.cue("Constructed case"), FadeIn(z), FadeIn(tg), run_time=0.6)

        mant, exp = EV["true_exp_minus_1000"].split("E")
        rows = VGroup(
            VGroup(T("true value", 30, INK_SOFT),
                   M(r"\approx %s \times 10^{%s}" % (mant, int(exp)), 0.8)).arrange(RIGHT, buff=0.35),
            VGroup(T("Python, direct", 30, INK_SOFT), N(f"{c['direct']['probs'][1]}", 44, WARN)
                   ).arrange(RIGHT, buff=0.35),
            VGroup(T("Python, main.py", 30, INK_SOFT),
                   N(f"{c['shifted']['probs'][1]}", 44, WARN)).arrange(RIGHT, buff=0.35),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([-1.8, -0.2, 0])
        cap = T("second probability", 26, INK_SOFT).next_to(rows, UP, buff=0.2).align_to(rows, LEFT)
        self.play_at(self.cue("The true second"), FadeIn(cap), FadeIn(rows[0]), run_time=0.6)
        self.play_at(self.cue("Python returns exactly zero"), FadeIn(rows[1]), FadeIn(rows[2]), run_time=0.6)

        # Float range: overflow fixed at the top, underflow untouched at the bottom.
        x = 4.3
        axis = Line([x, 1.5, 0], [x, -0.35, 0], color=INK, stroke_width=3)
        top = VGroup(T("overflow above: fixed", 26, ACCENT, weight="BOLD"),
                     N(f"exp(709) = {EV['exp_709']:.1e}", 26)
                     ).arrange(DOWN, buff=0.08).next_to(axis.get_top(), UP, buff=0.1)
        bot = VGroup(N(f"exp(−745) = {EV['exp_minus_745']}", 26),
                     N(f"exp(−746) = {EV['exp_minus_746']}", 26, WARN),
                     T("underflow below: not fixed", 26, WARN, weight="BOLD")
                     ).arrange(DOWN, buff=0.08).next_to(axis.get_bottom(), DOWN, buff=0.1)
        self.play_at(self.cue("protects the top"), Create(axis), FadeIn(top), run_time=0.7)
        self.play_at(self.cue("not the bottom"), FadeIn(bot), run_time=0.6)

        diff = EV["chapter_direct_minus_shifted"]
        dl = VGroup(T("[1, 2, 3]  direct − shifted:", 28, INK_SOFT),
                    N(", ".join(f"{v:.3g}".replace("-", "−") for v in diff), 32)
                    ).arrange(RIGHT, buff=0.3).move_to([0, -2.3, 0])
        note = T("equal in algebra, not bit for bit", 30, ACCENT, weight="BOLD").next_to(dl, DOWN, buff=0.18)
        self.play_at(self.cue("And even for one"), FadeIn(dl), run_time=0.6)
        self.play_at(self.cue("equal in algebra"), FadeIn(note), run_time=0.5)
        self.finish()


class BOUTTitle(Scene):
    def construct(self):
        dur = float(BEATS["BOUT"]["actual_duration_s"])
        title = VGroup(T("Subtract the Max", 130, INK, SERIF), T(".", 130, SPARK, SERIF)).arrange(RIGHT, buff=0.05)
        title[1].align_to(title[0], DOWN)
        sub = T("It changes the weights, not the answer.", 54, INK_SOFT, SERIF).next_to(title, DOWN, buff=0.9)
        who = T("Siddi Kommuri, INFO 7375, Week 1, Fall 2026", 44, INK_SOFT).next_to(sub, DOWN, buff=1.3)
        VGroup(title, sub, who).move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(sub), FadeIn(who), run_time=0.6)
        self.wait(max(dur - 1.4, 0.1))
