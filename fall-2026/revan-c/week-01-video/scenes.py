"""
Manim scenes for tokens-not-words (INFO 7375 Week 1 explainer).

Every token split and ID drawn here is read from evidence/tokens.json at render
time (produced by evidence/tokenize_examples.py, tiktoken 0.14.0, o200k_base).
Nothing is typed in by hand. Each scene's length is read from the measured
narration in beat_sheet.json (audio is the master clock).

B02_QuestionToTokens  the question → 8 tokens → 8 IDs
B03_LettersVsID       10 letters (3 r's) vs one ID, 101830
B04_SameWordThreeWays ' strawberry' / 'strawberry' / 'Strawberry'
B05_CheckTheChapter   the chapter's 'unbelievable' claim, checked
B06_SpellItOut        's t r a w b e r r y' → ' r' = 428, three times
B07_Boundary          what this does NOT establish
B10_TitleOutro        outro card with @RevanChonnad (replaces the toolkit outro, which hardcodes @NikBearBrown)
"""

import json
import os
from pathlib import Path

from manim import *

# Brutalist's static gate copies scenes.py alone into a temp dir, so the reel
# folder can be given explicitly: export TOKENS_REEL_DIR=/path/to/week-01-video
HERE = Path(os.environ.get("TOKENS_REEL_DIR") or Path(__file__).resolve().parent)
TOKENS = json.loads((HERE / "evidence" / "tokens.json").read_text())
ENC = "o200k_base"
EXAMPLES = {row["text"]: row for row in TOKENS["encodings"][ENC]["examples"]}
SHEET = json.loads((HERE / "beat_sheet.json").read_text())
DUR = {b["beat_id"]: float(b.get("actual_duration_s") or b["estimated_duration_s"]) for b in SHEET["beats"]}

BG = "#FAF9F5"
INK = "#3D3929"
MUTED = "#6B6557"
ACCENT = "#D97757"       # fills and arrows only
ACCENT_TEXT = "#A44A32"  # accent for text and outlines: 5.6:1 on BG (WCAG AA)
BOX = "#FFFFFF"
SERIF = "EB Garamond"
MONO = "Menlo"
SOURCE_NOTE = f"Real output · tiktoken {TOKENS['tiktoken_version']} · {ENC} · evidence/tokens.json"


def show_space(piece):
    """Make a leading space visible: ' strawberry' → '␣strawberry'."""
    return piece.replace(" ", "␣")


def token_box(piece, font_size=40, highlight=False):
    label = Text(show_space(piece), font=MONO, font_size=font_size, color=INK)
    ref = Text("Ayg|", font=MONO, font_size=font_size)
    rect = Rectangle(
        width=label.width + 0.45, height=ref.height + 0.45,
        stroke_color=ACCENT_TEXT if highlight else INK, stroke_width=4 if highlight else 2.5,
        fill_color=BOX, fill_opacity=1,
    )
    label.move_to(rect)
    return VGroup(rect, label)


def id_label(token_id, font_size=34, color=INK):
    return Text(str(token_id), font=MONO, font_size=font_size, color=color, weight="BOLD")


class Timeline:
    """Schedule events at fractions of the beat's measured narration length."""

    def __init__(self, scene, beat):
        self.scene = scene
        self.total = DUR[beat]
        self.clock = 0.0
        scene.camera.background_color = BG

    def at(self, fraction, *animations, run_time=0.8):
        target = fraction * self.total
        if target > self.clock:
            self.scene.wait(target - self.clock)
            self.clock = target
        if animations:
            self.scene.play(*animations, run_time=run_time)
            self.clock += run_time

    def finish(self):
        if self.total > self.clock:
            self.scene.wait(self.total - self.clock)

    def heading(self, text):
        h = Text(text, font=SERIF, font_size=54, color=INK).to_edge(UP, buff=0.75)
        self.scene.add(h)
        return h

    def source_note(self, text=SOURCE_NOTE):
        n = Text(text, font=SERIF, font_size=24, color=MUTED).to_edge(DOWN, buff=0.7)
        self.scene.add(n)
        return n


class B02_QuestionToTokens(Scene):
    def construct(self):
        t = Timeline(self, "B02")
        row = EXAMPLES["How many r's are in strawberry?"]
        t.heading("What the model receives")
        t.source_note()

        question = Text(row["text"], font=MONO, font_size=46, color=INK).move_to(UP * 0.6)
        t.at(0.0, FadeIn(question), run_time=0.6)

        boxes = VGroup(*[token_box(p, 38, highlight=(p == " strawberry")) for p in row["pieces"]])
        boxes.arrange(RIGHT, buff=0.18).move_to(UP * 0.6)
        if boxes.width > 12.6:
            boxes.scale_to_fit_width(12.6)
        for box in boxes:
            box[0].set_stroke(INK, 2.5)
        counter = Text(f"{row['n_tokens']} tokens", font=SERIF, font_size=44, color=INK).next_to(boxes, UP, buff=0.6)

        t.at(0.21, ReplacementTransform(question, boxes), FadeIn(counter), run_time=1.0)

        # 'How.' 'Many.' 'R.' Apostrophe-s — point at each as it is named
        for i, frac in enumerate([0.33, 0.37, 0.41, 0.45]):
            t.at(frac, Indicate(boxes[i], color=ACCENT_TEXT, scale_factor=1.12), run_time=0.5)

        straw = boxes[row["pieces"].index(" strawberry")]
        t.at(0.55, straw[0].animate.set_stroke(ACCENT_TEXT, 5), Indicate(straw, color=ACCENT_TEXT, scale_factor=1.1), run_time=0.9)

        ids = VGroup(*[
            id_label(i, 34, ACCENT_TEXT if p == " strawberry" else INK).move_to([b.get_center()[0], boxes.get_bottom()[1] - 0.75, 0])
            for i, p, b in zip(row["ids"], row["pieces"], boxes)
        ])
        arrows = VGroup(*[Arrow(b.get_bottom(), l.get_top(), buff=0.06, stroke_width=3, color=MUTED,
                                 max_tip_length_to_length_ratio=0.35) for b, l in zip(boxes, ids)])
        t.at(0.68, LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(l, shift=DOWN * 0.2))
                                    for a, l in zip(arrows, ids)], lag_ratio=0.12), run_time=1.6)

        bracket = Text("[ " + "  ".join(str(i) for i in row["ids"]) + " ]", font=MONO, font_size=40,
                       color=INK, weight="BOLD").move_to(DOWN * 2.3)
        if bracket.width > 12.4:
            bracket.scale_to_fit_width(12.4)
        t.at(0.82, boxes.animate.set_opacity(0.45), FadeOut(arrows), FadeIn(bracket, shift=UP * 0.2), run_time=1.0)
        t.finish()


class B03_LettersVsID(Scene):
    def construct(self):
        t = Timeline(self, "B03")
        t.heading("Two views of the same word")
        t.source_note()
        divider = Line(UP * 2.4, DOWN * 1.6, color=MUTED, stroke_width=2)
        left_title = Text("What you see", font=SERIF, font_size=44, color=INK).move_to(LEFT * 3.6 + UP * 1.9)
        right_title = Text("What the model receives", font=SERIF, font_size=40, color=INK).move_to(RIGHT * 3.4 + UP * 1.9)
        t.at(0.0, FadeIn(divider), FadeIn(left_title), run_time=0.6)

        letters = VGroup(*[
            VGroup(Square(0.56, stroke_color=INK, stroke_width=2, fill_color=BOX, fill_opacity=1),
                   Text(ch, font=MONO, font_size=36, color=INK))
            for ch in "strawberry"
        ])
        for tile in letters:
            tile[1].move_to(tile[0])
        letters.arrange(RIGHT, buff=0.06).move_to(LEFT * 3.35 + UP * 0.4)
        t.at(0.05, LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in letters], lag_ratio=0.08), run_time=1.2)

        r_tiles = [t for t in letters if t[1].text == "r"]
        r_count = Text(f"letters: {len(letters)}   r: {len(r_tiles)}", font=SERIF, font_size=44, color=INK)
        r_count.move_to(LEFT * 3.6 + DOWN * 1.15)
        t.at(0.2, *[tile[0].animate.set_fill(ACCENT, 1).set_stroke(ACCENT) for tile in r_tiles],
                FadeIn(r_count), run_time=0.9)

        row = EXAMPLES[" strawberry"]
        model_id = Text(f"[ {row['ids'][0]} ]", font=MONO, font_size=62, color=ACCENT_TEXT, weight="BOLD")
        model_id.move_to(RIGHT * 3.35 + UP * 0.4)
        id_note = Text(f"{row['n_tokens']} token: '{show_space(row['pieces'][0])}'", font=MONO, font_size=28, color=MUTED)
        id_note.next_to(model_id, DOWN, buff=0.3)
        t.at(0.36, FadeIn(right_title), FadeIn(model_id, scale=0.8), FadeIn(id_note), run_time=0.9)

        zero = Text("letters: 0   r: 0", font=SERIF, font_size=44, color=INK).move_to(RIGHT * 3.6 + DOWN * 1.15)
        t.at(0.58, FadeIn(zero), Indicate(model_id, color=ACCENT_TEXT), run_time=0.9)

        take1 = Text("Spelling has to be learned about the token —", font=SERIF, font_size=36, color=INK)
        take2 = Text("it can't be read off the input.", font=SERIF, font_size=36, color=INK)
        takeaway = VGroup(take1, take2).arrange(DOWN, buff=0.15).move_to(DOWN * 2.25)
        t.at(0.74, FadeIn(takeaway, shift=UP * 0.2), run_time=0.9)
        t.finish()


class B04_SameWordThreeWays(Scene):
    def construct(self):
        t = Timeline(self, "B04")
        t.heading("Same word, three inputs")
        t.source_note()
        rows = [EXAMPLES[" strawberry"], EXAMPLES["strawberry"], EXAMPLES["Strawberry"]]
        fracs = [0.14, 0.34, 0.58]
        counts = []
        for k, (row, frac) in enumerate(zip(rows, fracs)):
            y = 1.75 - k * 1.85
            label = Text(f"'{show_space(row['text'])}'", font=MONO, font_size=32, color=MUTED)
            label.move_to(LEFT * 4.55 + UP * y)
            boxes = VGroup(*[token_box(p, 36, highlight=(len(row["pieces"]) == 1)) for p in row["pieces"]])
            boxes.arrange(RIGHT, buff=0.14).move_to(RIGHT * 0.35 + UP * y)
            ids = Text("  ".join(str(i) for i in row["ids"]), font=MONO, font_size=30, color=INK)
            ids.next_to(boxes, DOWN, buff=0.15)
            count = Text(f"{row['n_tokens']} token" + ("" if row["n_tokens"] == 1 else "s"),
                         font=SERIF, font_size=42, color=INK, weight="BOLD").move_to(RIGHT * 4.95 + UP * y)
            counts.append(count)
            t.at(frac, FadeIn(label), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in boxes], lag_ratio=0.2),
                    FadeIn(ids), FadeIn(count), run_time=1.0)

        t.at(0.75, *[Indicate(c, color=ACCENT_TEXT, scale_factor=1.2) for c in counts], run_time=1.0)
        t.finish()


class B05_CheckTheChapter(Scene):
    def construct(self):
        t = Timeline(self, "B05")
        t.heading("Checking the course reading")
        t.source_note()
        quote = Text("“unbelievable might arrive in three pieces.”", font=SERIF, font_size=46,
                     color=INK, slant="ITALIC").move_to(UP * 1.85)
        cite = Text("— course reading, \"Randomness and first prompts\"", font=SERIF, font_size=26, color=MUTED)
        cite.next_to(quote, DOWN, buff=0.15)
        t.at(0.0, FadeIn(quote), FadeIn(cite), run_time=0.7)

        bare = EXAMPLES["unbelievable"]
        spaced = EXAMPLES[" unbelievable"]

        def result_row(row, y, note):
            label = Text(f"'{show_space(row['text'])}'", font=MONO, font_size=30, color=MUTED).move_to(LEFT * 4.3 + UP * y)
            boxes = VGroup(*[token_box(p, 36) for p in row["pieces"]]).arrange(RIGHT, buff=0.14).move_to(RIGHT * 0.75 + UP * y)
            ids = Text("  ".join(str(i) for i in row["ids"]), font=MONO, font_size=28, color=INK).next_to(boxes, DOWN, buff=0.15)
            verdict = Text(note, font=SERIF, font_size=40, color=INK, weight="BOLD").move_to(RIGHT * 5.2 + UP * y)
            return label, boxes, ids, verdict

        l1, b1, i1, v1 = result_row(bare, 0.25, f"{bare['n_tokens']} ✓")
        t.at(0.36, FadeIn(l1), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in b1], lag_ratio=0.25),
                FadeIn(i1), FadeIn(v1), run_time=1.1)

        l2, b2, i2, v2 = result_row(spaced, -1.3, f"{spaced['n_tokens']}")
        b2[0][0].set_stroke(ACCENT_TEXT, 4)
        t.at(0.6, FadeIn(l2), FadeIn(b2, shift=RIGHT * 0.2), FadeIn(i2), FadeIn(v2), run_time=1.0)

        caption = Text("Holds — and the leading space decides which case you get.", font=SERIF,
                       font_size=36, color=ACCENT_TEXT).move_to(DOWN * 2.65)
        t.at(0.8, FadeIn(caption, shift=UP * 0.2), run_time=0.8)
        t.finish()


class B06_SpellItOut(Scene):
    def construct(self):
        t = Timeline(self, "B06")
        row = EXAMPLES["s t r a w b e r r y"]
        t.heading("Spell it out")
        t.source_note()
        text = Text(f"'{row['text']}'", font=MONO, font_size=50, color=INK).move_to(UP * 1.0)
        t.at(0.0, FadeIn(text), run_time=0.6)

        boxes = VGroup(*[token_box(p, 36) for p in row["pieces"]]).arrange(RIGHT, buff=0.14).move_to(UP * 1.0)
        if boxes.width > 12.6:
            boxes.scale_to_fit_width(12.6)
        ids = VGroup(*[id_label(i, 28).next_to(b, DOWN, buff=0.3) for i, b in zip(row["ids"], boxes)])
        count = Text(f"{row['n_tokens']} tokens", font=SERIF, font_size=44, color=INK).next_to(boxes, UP, buff=0.55)
        t.at(0.12, ReplacementTransform(text, boxes), FadeIn(count), run_time=1.0)
        t.at(0.22, LaggedStart(*[FadeIn(l, shift=DOWN * 0.15) for l in ids], lag_ratio=0.08), run_time=1.0)

        r_idx = [k for k, p in enumerate(row["pieces"]) if p.strip() == "r"]
        tally = VGroup()
        for n, k in enumerate(r_idx, start=1):
            mark = Text(str(n), font=SERIF, font_size=40, color=ACCENT_TEXT, weight="BOLD").next_to(ids[k], DOWN, buff=0.25)
            mark.shift(UP * 0.3)
            tally.add(mark)
            boxes[k][0].set_stroke(ACCENT_TEXT, 5)
            t.at(0.32 + 0.06 * (n - 1), boxes[k].animate.shift(UP * 0.3), ids[k].animate.shift(UP * 0.3).set_color(ACCENT_TEXT),
                 FadeIn(mark, scale=1.3), run_time=0.5)

        same = Text(f"' r' = {row['ids'][r_idx[0]]}, three times — the r's are in the input now",
                    font=SERIF, font_size=38, color=INK).move_to(DOWN * 1.55)
        if same.width > 12.4:
            same.scale_to_fit_width(12.4)
        links = VGroup(*[Arrow(m.get_bottom(), same.get_top(), buff=0.12, stroke_width=3, color=ACCENT,
                               max_tip_length_to_length_ratio=0.12) for m in tally])
        t.at(0.5, FadeIn(same, shift=UP * 0.2), LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.2), run_time=1.0)

        caveat = Text("visible ≠ verified", font=SERIF, font_size=46, color=ACCENT_TEXT, slant="ITALIC").move_to(DOWN * 2.4)
        t.at(0.8, FadeIn(caveat, shift=UP * 0.2), run_time=0.8)
        t.finish()


class B07_Boundary(Scene):
    def construct(self):
        t = Timeline(self, "B07")
        t.heading("What this does NOT establish")

        def card(title, body, y):
            title_text = Text(title, font=SERIF, font_size=46, color=INK, weight="BOLD")
            body_text = Text(body, font=SERIF, font_size=34, color=INK, line_spacing=0.9)
            content = VGroup(title_text, body_text).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            rect = Rectangle(width=12.4, height=content.height + 0.7, stroke_color=INK, stroke_width=2.5,
                             fill_color=BOX, fill_opacity=1)
            rect.move_to(UP * y)
            content.move_to(rect).align_to(rect, LEFT).shift(RIGHT * 0.5)
            marker = Rectangle(width=0.14, height=rect.height, stroke_width=0, fill_color=ACCENT, fill_opacity=1)
            marker.move_to(rect).align_to(rect, LEFT)
            return VGroup(rect, marker, content)

        c1 = card("1 · This is not Claude's tokenizer",
                  "Shown: OpenAI's open o200k_base and cl100k_base.\nClaude's tokenizer is not public, so its splits may differ.", 1.27)
        c2 = card("2 · It does not predict failure",
                  "Many models answer \"three\" correctly. This explains why\nletter-counting is awkward — not that a model will get it wrong.", -1.67)
        t.at(0.12, FadeIn(c1, shift=UP * 0.2), run_time=0.9)
        t.at(0.43, FadeIn(c2, shift=UP * 0.2), run_time=0.9)
        t.finish()


class B10_TitleOutro(Scene):
    def construct(self):
        t = Timeline(self, "B10")
        body = Text("Tokens, Not Words", font=SERIF, font_size=116, color=INK)
        dot = Text(".", font=SERIF, font_size=116, color=ACCENT_TEXT)
        dot.next_to(body, RIGHT, buff=0.04).align_to(body[-1], DOWN)  # sit on the baseline of the final "s"
        title = VGroup(body, dot).move_to(UP * 1.35)
        handle = Text("@RevanChonnad", font=SERIF, font_size=84, color=INK).next_to(title, DOWN, buff=0.7)
        rule = Line(LEFT * 2.6, RIGHT * 2.6, color=ACCENT, stroke_width=5).next_to(handle, DOWN, buff=0.5)
        course = Text("INFO 7375 · Week 1", font=SERIF, font_size=48, color=MUTED).next_to(rule, DOWN, buff=0.45)
        t.at(0.0, FadeIn(title, shift=UP * 0.2), run_time=0.8)
        t.at(0.3, FadeIn(handle, shift=UP * 0.15), Create(rule), FadeIn(course), run_time=0.8)
        t.finish()
