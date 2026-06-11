import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VOICEOVER_DIR = PROJECT_ROOT / "voiceover" / "generated_sentence_level"

SCENE_2_1_DURATIONS = {
    "sc21_001.mp3": 3.483,
    "sc21_002.mp3": 7.802,
    "sc21_003.mp3": 5.944,
    "sc21_004.mp3": 4.226,
    "sc21_005.mp3": 4.087,
    "sc21_006.mp3": 1.161,
    "sc21_007.mp3": 1.300,
    "sc21_008.mp3": 2.508,
    "sc21_009.mp3": 9.288,
    "sc21_010.mp3": 6.548,
    "sc21_011.mp3": 9.660,
    "sc21_012.mp3": 5.480,
    "sc21_013.mp3": 4.272,
    "sc21_014.mp3": 6.641,
    "sc21_015.mp3": 6.827,
}
SCENE_2_1_VOICEOVERS = tuple(SCENE_2_1_DURATIONS)
SCENE_2_1_TIMING_SCALE = 0.87


def rt(seconds):
    return seconds * SCENE_2_1_TIMING_SCALE


def wait_until(scene, target_time):
    current_time = getattr(scene.renderer, "time", 0.0)
    if current_time < target_time:
        scene.wait(target_time - current_time)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc21_*.mp3"))
    expected = sorted(SCENE_2_1_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 2.1 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_2_1_DURATIONS:
        raise KeyError(f"Unexpected Scene 2.1 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 2.1 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_2_1_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    if played != SCENE_2_1_VOICEOVERS:
        missing = [filename for filename in SCENE_2_1_VOICEOVERS if filename not in played]
        raise RuntimeError(
            f"Scene 2.1 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


def finish_voiceovers(scene, voiceover_end, padding=0.25):
    current_time = getattr(scene.renderer, "time", 0.0)
    remaining = voiceover_end + padding - current_time
    if remaining > 0:
        scene.wait(remaining)


# Note: visual/narration alignment comment translated from Vietnamese.
def create_text(text, font_size=24, font="Arial", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)

# Note: visual/narration alignment comment translated from Vietnamese.
def create_markup_text(text, font_size=24, font="Arial", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)


# Note: visual/narration alignment comment translated from Vietnamese.
def get_checkmark(color=GREEN_A, stroke_width=2.0):
    checkmark = VMobject(color=color, stroke_width=stroke_width)
    checkmark.set_points_as_corners([
        LEFT * 0.12 + DOWN * 0.04,
        ORIGIN + DOWN * 0.12,
        RIGHT * 0.16 + UP * 0.12
    ])
    return checkmark

# Note: visual/narration alignment comment translated from Vietnamese.
def get_infinity(color=WHITE, stroke_width=2.0):
    left_circle = Circle(radius=0.07, color=color, stroke_width=stroke_width)
    right_circle = Circle(radius=0.07, color=color, stroke_width=stroke_width)
    left_circle.move_to(LEFT * 0.06)
    right_circle.move_to(RIGHT * 0.06)
    return VGroup(left_circle, right_circle)

# Note: visual/narration alignment comment translated from Vietnamese.
def get_minus_infinity(color=RED_A, stroke_width=1.8):
    minus = Line(LEFT * 0.06, RIGHT * 0.06, color=color, stroke_width=stroke_width)
    inf = get_infinity(color=color, stroke_width=stroke_width)
    inf.scale(0.8)
    minus.next_to(inf, LEFT, buff=0.03)
    return VGroup(minus, inf)

# Note: visual/narration alignment comment translated from Vietnamese.
def get_theta(color=WHITE, stroke_width=2.0):
    ellipse = Ellipse(width=0.15, height=0.22, color=color, stroke_width=stroke_width)
    line = Line(LEFT * 0.06, RIGHT * 0.06, color=color, stroke_width=stroke_width)
    line.move_to(ellipse.get_center())
    return VGroup(ellipse, line)

# Note: visual/narration alignment comment translated from Vietnamese.
def get_sigma(color=WHITE, stroke_width=2.0):
    sigma = VMobject(color=color, stroke_width=stroke_width)
    sigma.set_points_as_corners([
        RIGHT * 0.12 + UP * 0.14,
        LEFT * 0.12 + UP * 0.14,
        RIGHT * 0.04 + ORIGIN,
        LEFT * 0.12 + DOWN * 0.14,
        RIGHT * 0.12 + DOWN * 0.14
    ])
    return sigma


class Scene2_1(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Voiceover audio is scheduled from actual MP3 durations.
        voiceover_end = schedule_scene_voiceovers(self)

        chapter_title = create_text("CHAPTER II: PRIMITIVE GENERATORS", font_size=24, color=GREEN_A)
        chapter_sub = create_text("Token-level generation", font_size=18, color=GRAY_A)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.arrange(DOWN, buff=0.18).move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=rt(1.2))
        self.wait(rt(2.0))

        sub_title = create_text("Primitive Generators - Autoregressive Token Generation", font_size=16, color=GREEN_B)
        sub_title.to_edge(UP, buff=0.4)
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=rt(1.0))

        prefix_label = create_text("prefix x_<t", font_size=13, color=BLUE_A)
        prefix_box = RoundedRectangle(width=4.9, height=1.15, color=BLUE_C, fill_color="#0e1726", fill_opacity=0.85, corner_radius=0.06)
        prefix_text = create_text('"Taylor Alison Swift ... is"', font_size=15, color=WHITE)
        prefix_text.move_to(prefix_box.get_center())
        prefix_body = VGroup(prefix_box, prefix_text)

        lm_box = RoundedRectangle(width=2.35, height=1.35, color=GREEN_C, fill_color="#0d2417", fill_opacity=0.9, corner_radius=0.06)
        lm_text = create_text("causal LM", font_size=18, color=GREEN_A)
        lm_text.move_to(lm_box.get_center())
        lm_group = VGroup(lm_box, lm_text).move_to(ORIGIN + UP * 0.6)

        formula_box = RoundedRectangle(width=3.25, height=0.8, color=GRAY_B, fill_color="#181a1e", fill_opacity=0.88, corner_radius=0.06)
        formula_text = create_text('predict next: "an"', font_size=16, color=YELLOW)
        formula_text.move_to(formula_box.get_center())
        formula_group = VGroup(formula_box, formula_text)

        prefix_body.next_to(lm_group, LEFT, buff=0.45)
        formula_group.next_to(lm_group, RIGHT, buff=0.45)
        prefix_label.next_to(prefix_body, UP, buff=0.16)
        prefix_group = VGroup(prefix_body, prefix_label)

        arrow_in = Arrow(prefix_box.get_right(), lm_box.get_left(), buff=0.22, color=GRAY_B, stroke_width=2.0)
        arrow_out = Arrow(lm_box.get_right(), formula_box.get_left(), buff=0.22, color=GRAY_B, stroke_width=2.0)

        self.play(
            FadeIn(prefix_group, shift=RIGHT * 0.2),
            FadeIn(lm_group, shift=UP * 0.15),
            Create(arrow_in),
            run_time=rt(1.4),
        )
        self.play(Create(arrow_out), FadeIn(formula_group, shift=LEFT * 0.2), run_time=rt(1.1))
        self.wait(rt(6.0))

        dist_title = create_text("next-token distribution", font_size=13, color=GRAY_A)
        dist_title.next_to(formula_group, DOWN, buff=0.45)
        distribution = build_bar_chart(
            [
                {"word": '"an"', "prob": 0.80, "color": BLUE_C},
                {"word": '"a"', "prob": 0.13, "color": GRAY_C},
                {"word": '"the"', "prob": 0.06, "color": GRAY_C},
                {"word": '"best"', "prob": 0.02, "color": GRAY_C},
            ],
            0.0,
        )
        distribution.scale(0.82)
        distribution.next_to(dist_title, DOWN, buff=0.2).align_to(dist_title, LEFT)

        self.play(Write(dist_title), FadeIn(distribution, shift=UP * 0.15), run_time=rt(1.2))
        self.wait(rt(5.8))

        rule_text = create_text("decoding rule: choose the next token", font_size=14, color=YELLOW)
        rule_text.move_to(DOWN * 2.05)
        rule_group = VGroup(rule_text)

        selected = SurroundingRectangle(distribution[0], color=YELLOW, buff=0.08, stroke_width=2.5)
        token_an = create_text('"an"', font_size=18, color=YELLOW)
        token_an.next_to(rule_group, DOWN, buff=0.18)

        self.play(FadeIn(rule_group, shift=UP * 0.2), run_time=rt(0.9))
        self.play(Create(selected), FadeIn(token_an, shift=RIGHT * 0.15), run_time=rt(1.1))
        wait_until(self, 21.45)

        current_panel = VGroup(
            prefix_group,
            lm_group,
            formula_group,
            arrow_in,
            arrow_out,
            dist_title,
            distribution,
            rule_group,
            selected,
            token_an,
        )

        search_title = create_text("Decoding is search", font_size=18, color=BLUE_A)
        search_title.move_to(UP * 2.55)
        search_subtitle = create_text("Each time-step during decoding requires a choice.", font_size=13, color=GRAY_A)
        search_subtitle.next_to(search_title, DOWN, buff=0.28)

        root_node = RoundedRectangle(width=2.25, height=0.5, color=BLUE_D, fill_color="#0e1726", fill_opacity=0.9, corner_radius=0.04)
        root_text = create_text("Taylor Swift is", font_size=10, color=WHITE)
        root_text.move_to(root_node.get_center())
        root_group = VGroup(root_node, root_text).move_to(LEFT * 4.35 + UP * 0.25)

        first_choices = VGroup()
        first_arrows = VGroup()
        for word, y_pos in [("a", 0.85), ("the", -0.35)]:
            node = RoundedRectangle(width=0.9, height=0.38, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            text = create_text(word, font_size=9, color=WHITE)
            text.move_to(node.get_center())
            group = VGroup(node, text).move_to(LEFT * 2.65 + UP * y_pos)
            first_choices.add(group)
            first_arrows.add(Line(root_node.get_right(), node.get_left(), color=GRAY_B, stroke_width=1.2).add_tip(tip_length=0.06, tip_width=0.06))

        middle_words = VGroup(
            create_text("former", font_size=9, color=GRAY_A),
            create_text("contestant", font_size=9, color=GRAY_A),
            create_text("- song", font_size=9, color=GRAY_A),
            create_text("actress", font_size=9, color=GRAY_A),
            create_text("singer", font_size=9, color=GRAY_A),
            create_text("writer", font_size=9, color=GRAY_A),
            create_text("and", font_size=9, color=GRAY_A),
            create_text("producer", font_size=9, color=GRAY_A),
            create_text("song", font_size=9, color=GRAY_A),
        ).arrange_in_grid(rows=3, cols=3, buff=(0.42, 0.42))
        middle_words.move_to(RIGHT * 0.15 + UP * 0.15)

        right_words = VGroup(
            create_text("member", font_size=9, color=GRAY_A),
            create_text("of", font_size=9, color=GRAY_A),
            create_text('" The', font_size=9, color=GRAY_A),
            create_text("on", font_size=9, color=GRAY_A),
            create_text("the", font_size=9, color=GRAY_A),
            create_text(".", font_size=9, color=GRAY_A),
            create_text("who", font_size=9, color=GRAY_A),
            create_text("has", font_size=9, color=GRAY_A),
            create_text("is", font_size=9, color=GRAY_A),
            create_text("was", font_size=9, color=GRAY_A),
        ).arrange_in_grid(rows=4, cols=3, buff=(0.55, 0.35))
        right_words.move_to(RIGHT * 3.7 + UP * 0.05)

        choice_links = VGroup(
            Line(first_choices[0].get_right(), middle_words[0].get_left(), color=GRAY_D, stroke_width=0.8),
            Line(first_choices[0].get_right(), middle_words[2].get_left(), color=GRAY_D, stroke_width=0.8),
            Line(first_choices[1].get_right(), middle_words[4].get_left(), color=GRAY_D, stroke_width=0.8),
            Line(first_choices[1].get_right(), middle_words[5].get_left(), color=GRAY_D, stroke_width=0.8),
            Line(middle_words[0].get_right(), right_words[0].get_left(), color=GRAY_D, stroke_width=0.8),
            Line(middle_words[1].get_right(), right_words[3].get_left(), color=GRAY_D, stroke_width=0.8),
            Line(middle_words[5].get_right(), right_words[5].get_left(), color=GRAY_D, stroke_width=0.8),
            Line(middle_words[6].get_right(), right_words[6].get_left(), color=GRAY_D, stroke_width=0.8),
        )

        objective_question = VGroup(
            create_text("But a search for what? What is our objective?", font_size=12, color=YELLOW),
            create_text("How do we make local choices that achieve the objective?", font_size=12, color=YELLOW),
        ).arrange(DOWN, buff=0.15)
        objective_question.move_to(DOWN * 2.05)

        self.play(FadeOut(current_panel, shift=DOWN * 0.2), run_time=0.2)
        self.play(
            FadeIn(search_title, shift=DOWN * 0.15),
            FadeIn(search_subtitle, shift=DOWN * 0.15),
            FadeIn(root_group, shift=RIGHT * 0.15),
            run_time=0.3,
        )
        self.play(Create(first_arrows), FadeIn(first_choices, shift=RIGHT * 0.12), run_time=rt(1.1))
        self.play(Create(choice_links), FadeIn(middle_words, shift=RIGHT * 0.12), FadeIn(right_words, shift=RIGHT * 0.12), run_time=rt(1.6))
        self.play(FadeIn(objective_question, shift=UP * 0.12), run_time=rt(1.0))
        wait_until(self, 30.51)

        search_group = VGroup(
            search_title,
            search_subtitle,
            root_group,
            first_choices,
            first_arrows,
            middle_words,
            right_words,
            choice_links,
            objective_question,
        )

        outline_title = create_text("Token-level generation (outline)", font_size=17, color=BLUE_A)
        outline_title.move_to(UP * 2.25)
        objective_title = create_text("Objectives for decoding", font_size=15, color=GRAY_A)
        objective_title.next_to(outline_title, DOWN, buff=0.55)
        objective_items = VGroup(
            create_text("• Optimization", font_size=14, color=WHITE),
            create_text("• Sampling", font_size=14, color=WHITE),
            create_text("• Constrained generation, structured outputs", font_size=14, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        objective_items.next_to(objective_title, DOWN, buff=0.45)

        outline_group = VGroup(outline_title, objective_title, objective_items)
        self.play(FadeOut(search_group, shift=DOWN * 0.2), FadeIn(outline_title, shift=DOWN * 0.12), FadeIn(objective_title, shift=DOWN * 0.12), run_time=rt(1.0))
        self.play(FadeIn(objective_items, shift=UP * 0.15), run_time=rt(1.1))
        wait_until(self, 39.80)

        comparison_title = create_text("Language model vs decoding algorithm", font_size=17, color=GREEN_A)
        comparison_title.move_to(UP * 2.35)

        lm_card = RoundedRectangle(width=4.6, height=2.3, color=GREEN_C, fill_color="#0d2417", fill_opacity=0.82, corner_radius=0.06)
        lm_card.move_to(LEFT * 2.75 + DOWN * 0.15)
        lm_card_title = create_text("Language model", font_size=13, color=GREEN_A)
        lm_card_title.next_to(lm_card.get_top(), DOWN, buff=0.18)
        lm_card_text = create_text("provides a next-token distribution", font_size=11, color=WHITE)
        lm_card_text.move_to(lm_card.get_center() + UP * 0.22)
        lm_card_items = VGroup(
            create_text('"an"  0.80', font_size=10, color=BLUE_A),
            create_text('"a"   0.13', font_size=10, color=GRAY_A),
            create_text('"the" 0.06', font_size=10, color=GRAY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lm_card_items.move_to(lm_card.get_center() + DOWN * 0.55)

        decoder_card = RoundedRectangle(width=4.6, height=2.3, color=YELLOW, fill_color="#211c10", fill_opacity=0.72, corner_radius=0.06)
        decoder_card.move_to(RIGHT * 2.75 + DOWN * 0.15)
        decoder_card_title = create_text("Decoding algorithm", font_size=13, color=YELLOW)
        decoder_card_title.next_to(decoder_card.get_top(), DOWN, buff=0.18)
        decoder_card_text = create_text("decides which token to take", font_size=11, color=WHITE)
        decoder_card_text.move_to(decoder_card.get_center() + UP * 0.2)
        decoder_choice = create_text('take "an"', font_size=15, color=YELLOW)
        decoder_choice.move_to(decoder_card.get_center() + DOWN * 0.55)

        comparison_group = VGroup(
            comparison_title,
            lm_card,
            lm_card_title,
            lm_card_text,
            lm_card_items,
            decoder_card,
            decoder_card_title,
            decoder_card_text,
            decoder_choice,
        )
        self.play(FadeOut(outline_group, shift=DOWN * 0.2), FadeIn(comparison_group, shift=UP * 0.15), run_time=rt(1.0))
        wait_until(self, 56.01)

        same_model_title = create_text("Same model, different decoding rules", font_size=17, color=GREEN_A)
        same_model_title.move_to(UP * 2.35)
        method_items = VGroup(
            create_text("greedy decoding", font_size=14, color=WHITE),
            create_text("beam search", font_size=14, color=WHITE),
            create_text("sampling", font_size=14, color=WHITE),
            create_text("constrained decoding", font_size=14, color=WHITE),
        ).arrange(RIGHT, buff=0.55)
        method_items.next_to(same_model_title, DOWN, buff=0.55)
        same_model_group = VGroup(same_model_title, method_items)
        self.play(FadeOut(comparison_group, shift=DOWN * 0.2), FadeIn(same_model_group, shift=UP * 0.15), run_time=rt(1.0))
        wait_until(self, 61.49)

        choice_tree_note = create_text("not just choosing one token and stopping", font_size=15, color=YELLOW)
        choice_tree_note.move_to(DOWN * 2.25)
        tree_recap_group = VGroup(search_title, search_subtitle, root_group, first_choices, first_arrows, middle_words, right_words, choice_links, choice_tree_note)
        self.play(FadeOut(same_model_group, shift=DOWN * 0.2), FadeIn(tree_recap_group, shift=UP * 0.15), run_time=rt(1.0))
        wait_until(self, 65.76)

        local_title = create_text("A local choice changes the prefix", font_size=17, color=BLUE_A)
        local_title.move_to(UP * 2.35)
        local_prefix_1 = create_text("current prefix", font_size=12, color=BLUE_A)
        local_choice = create_text('choose "an"', font_size=14, color=YELLOW)
        local_prefix_2 = create_text("new prefix", font_size=12, color=BLUE_A)
        local_dist = create_text("new next-token distribution", font_size=12, color=GREEN_A)
        local_row = VGroup(local_prefix_1, local_choice, local_prefix_2, local_dist).arrange(RIGHT, buff=0.55)
        local_row.move_to(UP * 0.3)
        local_arrows = VGroup(
            Arrow(local_prefix_1.get_right(), local_choice.get_left(), buff=0.12, color=GRAY_B, stroke_width=1.6),
            Arrow(local_choice.get_right(), local_prefix_2.get_left(), buff=0.12, color=GRAY_B, stroke_width=1.6),
            Arrow(local_prefix_2.get_right(), local_dist.get_left(), buff=0.12, color=GRAY_B, stroke_width=1.6),
        )
        local_group = VGroup(local_title, local_row, local_arrows)
        self.play(FadeOut(tree_recap_group, shift=DOWN * 0.2), FadeIn(local_group, shift=UP * 0.15), run_time=rt(1.0))
        wait_until(self, 72.40)

        final_line = create_text("Connect local choices into a final sequence.", font_size=17, color=YELLOW)
        final_line.move_to(UP * 0.45)
        final_subline = create_text("according to the chosen objective", font_size=14, color=GRAY_A)
        final_subline.next_to(final_line, DOWN, buff=0.28)
        final_group = VGroup(final_line, final_subline)
        self.play(FadeOut(local_group, shift=DOWN * 0.2), FadeIn(final_group, shift=UP * 0.15), run_time=rt(1.0))
        finish_voiceovers(self, voiceover_end)
        self.play(
            FadeOut(final_group),
            FadeOut(sub_title),
            run_time=rt(0.6),
        )
        assert_all_scene_voiceovers_played(self)


# Note: visual/narration alignment comment translated from Vietnamese.
def build_bar_chart(candidates, base_y):
    group = VGroup()
    for idx, item in enumerate(candidates):
        y_pos = base_y - idx * 0.7
        
        lbl = create_text(item["word"], font_size=10, color=WHITE)
        lbl.move_to(RIGHT * 1.5 + UP * y_pos, aligned_edge=LEFT)
        
        bar_len = item["prob"] * 3.0 + 0.05
        bar = RoundedRectangle(width=bar_len, height=0.22, color=item["color"], fill_color=item["color"], fill_opacity=0.9, corner_radius=0.02)
        bar.next_to(lbl, RIGHT, buff=0.2)
        
        val = create_text(f'{item["prob"]:.2f}', font_size=9.5, color=item["color"])
        val.next_to(bar, RIGHT, buff=0.15)
        
        row = VGroup(lbl, bar, val)
        group.add(row)
    return group
