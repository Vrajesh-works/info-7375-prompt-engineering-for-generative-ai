"""
Manim scenes for seeded-not-true (INFO 7375 Week 1).

Every figure is real output of lessons/01-randomness-and-first-prompts/code/main.py
captured 2026-09-27 and re-checked by evidence/verify_claims.py (7/7).

B01_SeedMechanism   — constructed diagram, LABELLED constructed
B02_SameSeed        — run A and run B, identical
B03_DifferentSeed   — seed 10, counts move
B04_ExpectedVsObserved — 665.24 vs 630, the core beat
B05_GapsSumToZero   — the three gaps are constrained

Text() only, never Tex() — no LaTeX on this machine.
"""

from manim import *

BG = "#FAF9F5"
INK = "#3D3929"
ACCENT = "#D97757"
DIM = "#9B8EAA"
GOOD = "#4A7C59"

PROBS = [0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
SEED7 = {0: 102, 1: 268, 2: 630}
SEED10 = {0: 97, 1: 213, 2: 690}
N = 1000


def mono(t, size=32, color=INK, weight="NORMAL"):
    return Text(t, font="Menlo", font_size=size, color=color, weight=weight)


def label(t, size=28, color=INK, weight="NORMAL"):
    return Text(t, font_size=size, color=color, weight=weight)


class B01_SeedMechanism(Scene):
    """Constructed illustration — labelled as such on screen."""

    def construct(self):
        self.camera.background_color = BG

        # inside the safe area (half-extents +/-6.3 x, +/-3.4 y)
        tag = label("CONSTRUCTED ILLUSTRATION", size=20, color=DIM)
        tag.move_to(LEFT * 4.0 + UP * 3.1)
        self.add(tag)

        src = VGroup(
            mono("def sample(logits, count=1000, seed=7, ...)", size=26),
            mono("    rng = random.Random(seed)", size=26, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        src.move_to(UP * 2.0)
        self.play(FadeIn(src[0]), run_time=1)
        self.play(Write(src[1]), run_time=1.2)
        self.wait(0.8)

        note = label("its own generator, not the global random state",
                     size=30, color=DIM)
        note.next_to(src, DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1)

        box = RoundedRectangle(width=4.4, height=1.8, corner_radius=0.15,
                               color=INK, fill_opacity=0.06)
        box_t = label("generator state", size=30)
        box_t.move_to(box)
        gen = VGroup(box, box_t).shift(DOWN * 0.6)
        seed_dot = VGroup(
            Circle(radius=0.6, color=ACCENT, fill_opacity=0.15),
            label("7", size=38, color=ACCENT),
        )
        seed_dot.next_to(gen, LEFT, buff=1.3)
        arrow = Arrow(seed_dot.get_right(), gen.get_left(),
                      buff=0.15, color=INK, stroke_width=3)

        self.play(FadeIn(seed_dot), run_time=0.6)
        self.play(GrowArrow(arrow), FadeIn(gen), run_time=0.9)
        self.wait(0.5)

        draws = VGroup(*[
            label(d, size=40, color=DIM)
            for d in ["2", "2", "1", "2", "0", "2", "1", "..."]
        ]).arrange(RIGHT, buff=0.7)
        draws.next_to(gen, DOWN, buff=0.9)
        out_arrow = Arrow(gen.get_bottom(), draws.get_top(),
                          buff=0.15, color=INK, stroke_width=3)
        self.play(GrowArrow(out_arrow), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d) for d in draws], lag_ratio=0.15),
                  run_time=1.6)
        self.wait(1.5)


class B02_SameSeed(Scene):
    def construct(self):
        self.camera.background_color = BG

        head = label("seed 7, run twice", size=46, weight="BOLD")
        head.move_to(UP * 3.1)
        self.add(head)

        def panel(title, counts):
            t = label(title, size=34, color=DIM)
            rows = VGroup(*[
                mono(f'"{k}": {counts[k]}', size=48)
                for k in (1, 2, 0)
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
            g = VGroup(t, rows).arrange(DOWN, buff=0.45)
            return g

        a = panel("run-A.txt", SEED7)
        b = panel("run-B.txt", SEED7)
        pair = VGroup(a, b).arrange(RIGHT, buff=2.2).shift(UP * 0.3)

        self.play(FadeIn(a), run_time=0.9)
        self.wait(0.6)
        self.play(FadeIn(b), run_time=0.9)
        self.wait(1.2)

        cmd = mono("$ diff run-A.txt run-B.txt", size=36, color=DIM)
        cmd.next_to(pair, DOWN, buff=0.9)
        self.play(FadeIn(cmd), run_time=0.7)
        self.wait(1.0)

        res = label("no output - byte for byte identical",
                    size=40, color=GOOD, weight="BOLD")
        res.next_to(cmd, DOWN, buff=0.4)
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.8)
        self.wait(2)


class B03_DifferentSeed(Scene):
    def construct(self):
        self.camera.background_color = BG

        head = label("change the seed", size=46, weight="BOLD")
        head.move_to(UP * 3.1)
        self.add(head)

        old = mono("seed=7", size=54, color=DIM)
        new = mono("seed=10", size=54, color=ACCENT)
        old.move_to(UP * 1.5)
        new.move_to(UP * 1.5)

        self.play(FadeIn(old), run_time=0.6)
        self.wait(0.6)
        self.play(Transform(old, new), run_time=0.9)
        self.wait(0.6)

        rows = VGroup()
        for k in (0, 1, 2):
            left = mono(f'"{k}": {SEED7[k]}', size=46, color=DIM)
            arrow = label("->", size=40, color=DIM)
            right = mono(f'{SEED10[k]}', size=46,
                         color=ACCENT if k == 2 else INK)
            rows.add(VGroup(left, arrow, right).arrange(RIGHT, buff=0.8))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.7).shift(DOWN * 0.5)

        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3),
                  run_time=1.8)
        self.wait(2)


class B04_ExpectedVsObserved(Scene):
    """The core beat. Continuous motion — a climbing counter, a growing gap."""

    def construct(self):
        self.camera.background_color = BG

        line1 = mono("p = 0.6652", size=48)
        line1.move_to(UP * 3.0)
        self.play(FadeIn(line1), run_time=0.7)

        line2 = mono("p x 1000 = 665.24", size=48)
        line2.move_to(UP * 2.2)
        self.play(Write(line2), run_time=1.2)

        # expected marker, drawn as a bar that grows to full width
        exp_cap = label("expected 665.24", size=34, color=DIM)
        exp_cap.move_to(UP * 1.2)
        exp_bar = Line(LEFT * 4.5 + UP * 0.75, RIGHT * 4.5 + UP * 0.75,
                       color=INK, stroke_width=3)
        self.play(FadeIn(exp_cap), run_time=0.4)
        self.play(Create(exp_bar), run_time=1.0)

        # the counter climbs — genuine frame-to-frame change
        tracker = ValueTracker(0)
        counter = always_redraw(
            lambda: mono(str(int(tracker.get_value())), size=92, color=ACCENT)
            .move_to(DOWN * 0.3)
        )
        obs_cap = label("observed", size=34, color=DIM)
        obs_cap.move_to(DOWN * 1.4)
        self.add(counter, obs_cap)
        self.play(tracker.animate.set_value(630), run_time=5.0)
        self.wait(0.4)

        # the shortfall bar grows from the counter up toward the expected line
        gap_bar = Line(DOWN * 0.3, UP * 0.75, color=ACCENT, stroke_width=8)
        gap_bar.shift(RIGHT * 2.6)
        self.play(GrowFromEdge(gap_bar, DOWN), run_time=1.0)

        gap_lab = mono("-35.24", size=54, color=ACCENT, weight="BOLD")
        gap_lab.move_to(RIGHT * 4.6 + UP * 0.2)
        self.play(FadeIn(gap_lab, shift=LEFT * 0.4), run_time=0.7)
        self.wait(0.6)

        # run it again: the counter resets and climbs to the identical number
        again = label("run it again with seed 7", size=36, color=INK)
        again.move_to(DOWN * 2.5)
        self.play(FadeIn(again), run_time=0.6)
        self.play(tracker.animate.set_value(0), run_time=0.8)
        self.play(tracker.animate.set_value(630), run_time=3.0)

        same = label("the same 630, the same -35.24", size=38, color=ACCENT,
                     weight="BOLD")
        same.move_to(DOWN * 3.1)
        self.play(FadeIn(same), run_time=0.7)
        self.play(Indicate(gap_lab, color=ACCENT, scale_factor=1.3),
                  run_time=0.9)
        self.wait(1.2)


class B05_GapsSumToZero(Scene):
    """The constraint. The three gaps travel in and collapse to zero."""

    def construct(self):
        self.camera.background_color = BG

        head = label("all three, seed 7", size=42, weight="BOLD")
        head.move_to(UP * 3.2)
        self.play(FadeIn(head), run_time=0.5)

        xs = [-4.6, -1.6, 1.4, 4.2]
        cols = ["token", "expected", "observed", "gap"]
        header = VGroup()
        for c, x in zip(cols, xs):
            h = label(c, size=32, color=DIM)
            h.move_to(RIGHT * x + UP * 2.2)
            header.add(h)
        self.play(LaggedStart(*[FadeIn(h) for h in header], lag_ratio=0.12),
                  run_time=0.8)

        gap_texts = []
        gaps = []
        for i, k in enumerate((0, 1, 2)):
            exp = PROBS[k] * N
            g = SEED7[k] - exp
            gaps.append(g)
            y = 1.3 - i * 0.85
            cells = []
            for val, x in zip(
                [str(k), f"{exp:.2f}", str(SEED7[k]), f"{g:+.2f}"], xs
            ):
                c = mono(val, size=42,
                         color=ACCENT if x == xs[3] else INK)
                c.move_to(RIGHT * x + UP * y)
                cells.append(c)
            gap_texts.append(cells[3])
            row = VGroup(*cells)
            self.play(FadeIn(row, shift=RIGHT * 0.5), run_time=0.55)

        self.wait(0.5)

        # the three gaps travel to the centre and merge
        target = mono("0.00", size=76, color=GOOD, weight="BOLD")
        target.move_to(DOWN * 1.6)

        # converge to three distinct slots, never stacking on one point
        slots = [LEFT * 2.4 + DOWN * 1.6, DOWN * 1.6, RIGHT * 2.4 + DOWN * 1.6]
        movers = [g.copy() for g in gap_texts]
        self.add(*movers)
        self.play(
            *[m.animate.move_to(slot).scale(0.75)
              for m, slot in zip(movers, slots)],
            run_time=1.8,
        )
        self.wait(0.4)
        self.play(
            *[FadeOut(m, scale=0.3, target_position=DOWN * 1.6)
              for m in movers],
            run_time=0.7,
        )
        self.play(FadeIn(target, scale=1.6), run_time=0.6)
        self.wait(0.6)

        sum_cap = label("sum of gaps", size=34, color=DIM)
        sum_cap.move_to(DOWN * 0.75)
        self.play(FadeIn(sum_cap), run_time=0.4)

        why = label("counts total 1000, probabilities total 1 - they have to",
                    size=30, color=DIM)
        why.move_to(DOWN * 2.4)
        self.play(Write(why), run_time=1.6)

        note = label("not three independent observations",
                     size=34, color=INK, weight="BOLD")
        note.move_to(DOWN * 3.0)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.7)
        self.wait(1.5)
