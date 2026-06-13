import os
import tempfile
from pathlib import Path
import random
from manim import *

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_4_2_DURATIONS = {
    "sc42_001.mp3": 4.412,
    "sc42_002.mp3": 2.276,
    "sc42_003.mp3": 3.39,
    "sc42_004.mp3": 4.969,
    "sc42_005.mp3": 4.272,
    "sc42_006.mp3": 5.526,
    "sc42_007.mp3": 1.904,
    "sc42_008.mp3": 9.66,
    "sc42_009.mp3": 5.573,
    "sc42_010.mp3": 6.455,
    "sc42_011.mp3": 2.833,
    "sc42_012.mp3": 6.269,
    "sc42_013.mp3": 2.694,
    "sc42_014.mp3": 4.783,
    "sc42_015.mp3": 6.873,
}
SCENE_4_2_VOICEOVERS = tuple(SCENE_4_2_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc42_*.mp3"))
    expected = sorted(SCENE_4_2_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 4.2 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_4_2_DURATIONS:
        raise KeyError(f"Unexpected Scene 4.2 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 4.2 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_4_2_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_4_2_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 4.2 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


# Note: visual/narration alignment comment translated from Vietnamese.
def create_text(text, font_size=24, font="Segoe UI", color=WHITE, **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    t = Text(text, font_size=base_size, font=font, color=color, **kwargs)
    t.scale(scale_factor)
    return t

# Note: visual/narration alignment comment translated from Vietnamese.
def create_markup_text(text, font_size=24, font="Segoe UI", **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    t = MarkupText(text, font_size=base_size, font=font, **kwargs)
    t.scale(scale_factor)
    return t


class Scene4_2(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (filename, duration) in enumerate(SCENE_4_2_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        # =====================================================================
        # Cue 1 (sc42_001): How to speed up a single generation screen.
        # =====================================================================
        self.wait_until(cue_start[1] + 0.1)
        chapter_title = create_text("Chapter 4: Systems Efficiency", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 4.2: Speculative Decoding", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)

        # =====================================================================
        # Cue 2 (sc42_002): The cow jumped over the moon prediction bottleneck.
        # =====================================================================
        self.wait_until(cue_start[2] + 0.1)
        sub_title = create_text("Speculative Decoding (Speculative Decoding)", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.0
        )

        seq_text_lbl = create_text("Sequential Generation (Bottleneck)", font_size=12, color=RED).move_to(UP * 1.5)
        self.play(Write(seq_text_lbl), run_time=0.8)

        seq_tokens = ["The", "cow", "jumped", "over", "the", "moon", "."]
        seq_boxes = VGroup()
        seq_lbls = VGroup()
        for i, word in enumerate(seq_tokens):
            box = RoundedRectangle(width=0.9, height=0.55, color=GRAY_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            box.move_to(LEFT * 3.3 + RIGHT * i * 1.1 + DOWN * 0.2)
            lbl = create_text(word, font_size=10, color=WHITE).move_to(box.get_center())
            seq_boxes.add(box)
            seq_lbls.add(lbl)

        self.play(
            LaggedStart(
                *[FadeIn(VGroup(box, lbl), shift=UP * 0.15) for box, lbl in zip(seq_boxes, seq_lbls)],
                lag_ratio=0.2
            ),
            run_time=1.2
        )

        # =====================================================================
        # Cue 3 (sc42_003): Spend less time on easier tokens question.
        # =====================================================================
        self.wait_until(cue_start[3] + 0.1)
        question_text = create_markup_text(
            "How can we <span foreground='#33CCFF'>spend less time</span> on easier tokens?",
            font_size=12, color=WHITE
        ).move_to(DOWN * 1.5)
        
        self.play(
            *[seq_boxes[idx].animate.set_color(GREEN) for idx in [0, 1, 2, 3, 4, 6]],
            Write(question_text),
            run_time=1.0
        )

        # =====================================================================
        # Cue 4 (sc42_004): Draft model small proposal generation.
        # =====================================================================
        self.wait_until(cue_start[4] + 0.1)
        self.play(
            FadeOut(seq_text_lbl),
            FadeOut(seq_boxes),
            FadeOut(seq_lbls),
            FadeOut(question_text),
            run_time=0.5
        )

        draft_gen_text = create_markup_text(
            "<b>Step 1: Generate draft sequence (Draft Generation, K = 5)</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(draft_gen_text), run_time=0.8)

        belt_line = Line(start=LEFT * 5.0 + DOWN * 0.8, end=RIGHT * 5.0 + DOWN * 0.8, color=GRAY_D, stroke_width=4)
        belt_roller_left = Dot(LEFT * 5.0 + DOWN * 0.8, color=GRAY_B, radius=0.12)
        belt_roller_right = Dot(RIGHT * 5.0 + DOWN * 0.8, color=GRAY_B, radius=0.12)
        conveyor_belt = VGroup(belt_line, belt_roller_left, belt_roller_right)

        draft_model_mini = RoundedRectangle(width=1.5, height=1.0, color=ORANGE, fill_color="#2a1a0f", fill_opacity=0.9, corner_radius=0.05)
        draft_model_mini.move_to(LEFT * 4.0 + UP * 0.6)
        draft_model_lbl = create_text("Draft Model", font_size=8, color=WHITE).move_to(draft_model_mini.get_center())
        draft_mini = VGroup(draft_model_mini, draft_model_lbl)
        
        self.play(
            Create(conveyor_belt),
            FadeIn(draft_mini),
            run_time=0.6
        )

        tokens_content = ["The", "cow", "jumped", "over", "the", "sun", "."]
        token_boxes = VGroup()
        token_lbls = VGroup()

        for i, tok_text in enumerate(tokens_content):
            color = GRAY_A if i < 2 else ORANGE
            fill_color = "#1a1c1e" if i < 2 else "#2b2014"
            tok_box = RoundedRectangle(width=0.9, height=0.55, color=color, fill_color=fill_color, fill_opacity=0.9, corner_radius=0.04)
            tok_box.move_to(draft_model_mini.get_center())
            
            tok_lbl = create_text(tok_text, font_size=10, color=WHITE).move_to(tok_box.get_center())
            token_boxes.add(tok_box)
            token_lbls.add(tok_lbl)

            dest_x = -4.0 + i * 1.33
            dest_pos = np.array([dest_x, -0.8, 0])

            self.play(
                draft_model_mini.animate(run_time=0.08).set_color(YELLOW),
                FadeIn(tok_box), FadeIn(tok_lbl),
                run_time=0.12
            )
            self.play(
                draft_model_mini.animate(run_time=0.08).set_color(ORANGE),
                VGroup(tok_box, tok_lbl).animate(run_time=0.25, rate_func=smooth).move_to(dest_pos),
                run_time=0.25
            )

        # =====================================================================
        # Cue 5 (sc42_005): Main generator parallel verification.
        # =====================================================================
        self.wait_until(cue_start[5] + 0.1)
        verify_text = create_markup_text(
            "<b>Step 2: Parallel verification (Parallel Verification)</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(
            FadeOut(draft_gen_text),
            Write(verify_text),
            run_time=0.8
        )

        target_model_mini = RoundedRectangle(width=2.0, height=1.3, color=BLUE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        target_model_mini.move_to(RIGHT * 3.5 + UP * 0.6)
        target_model_lbl = create_text("Target Model", font_size=9, color=BLUE).move_to(target_model_mini.get_center())
        
        target_mini_cores = VGroup()
        for r in range(2):
            for c in range(3):
                core = Square(side_length=0.18, color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=0.6)
                core.move_to(target_model_mini.get_center() + RIGHT * (c - 1.0) * 0.35 + UP * (r - 0.5) * 0.35)
                target_mini_cores.add(core)
        
        target_mini_group = VGroup(target_model_mini, target_model_lbl, target_mini_cores)

        self.play(
            FadeIn(target_mini_group),
            run_time=0.6
        )

        verify_lines = VGroup()
        for i in range(2, 7):
            start_p = token_boxes[i].get_top()
            end_p = target_model_mini.get_bottom()
            line = Line(start=start_p, end=end_p, color=BLUE_A, stroke_width=1.5).set_opacity(0.6)
            verify_lines.add(line)

        particles = VGroup()
        for line in verify_lines:
            p = Dot(color=YELLOW, radius=0.05).move_to(line.get_start())
            particles.add(p)

        self.play(
            Create(verify_lines),
            FadeIn(particles),
            run_time=0.4
        )

        self.play(
            *[p.animate(run_time=0.8, rate_func=smooth).move_to(line.get_end()) for p, line in zip(particles, verify_lines)],
        )

        self.play(
            *[c.animate(run_time=0.3).set_fill(ORANGE, opacity=0.9).set_color(ORANGE) for c in target_mini_cores],
            FadeOut(particles),
            FadeOut(verify_lines),
            run_time=0.5
        )

        # =====================================================================
        # Cue 6 (sc42_006): Accepted / mismatched proposal coloring.
        # =====================================================================
        self.wait_until(cue_start[6] + 0.1)
        self.play(
            FadeOut(verify_text),
            FadeOut(target_mini_group),
            FadeOut(draft_mini),
            FadeOut(conveyor_belt),
            FadeOut(token_boxes), FadeOut(token_lbls),
            run_time=0.4
        )

        math_intro = create_markup_text(
            "<b>Rejection Sampling (Rejection Sampling)</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.1)
        self.play(Write(math_intro), run_time=0.6)

        formula_box = RoundedRectangle(width=8.4, height=0.85, color=GOLD_A, fill_color="#1a1814", fill_opacity=0.9, corner_radius=0.06)
        formula_box.move_to(UP * 1.1)

        left_part = create_markup_text(
            "Acceptance probability:  <i>P</i><sub>accept</sub>(<i>x</i>)  =  min  (  1  ,",
            font_size=10.5, color=WHITE
        )
        num_txt = create_markup_text("<i>P</i><sub>target</sub>(<i>x</i>)", font_size=10, color=BLUE_A)
        den_txt = create_markup_text("<i>P</i><sub>draft</sub>(<i>x</i>)", font_size=10, color=ORANGE)

        frac_width = max(num_txt.width, den_txt.width) + 0.2
        fraction_line = Line(
            start=LEFT * frac_width / 2,
            end=RIGHT * frac_width / 2,
            stroke_width=1.5,
            color=WHITE
        )
        close_paren = create_text(")", font_size=11, color=WHITE)

        left_part.move_to(LEFT * 1.8)
        fraction_line.next_to(left_part, RIGHT, buff=0.18)
        close_paren.next_to(fraction_line, RIGHT, buff=0.18)
        num_txt.next_to(fraction_line, UP, buff=0.06)
        den_txt.next_to(fraction_line, DOWN, buff=0.06)

        formula_txt = VGroup(left_part, fraction_line, num_txt, den_txt, close_paren)
        formula_txt.move_to(formula_box.get_center())

        self.play(
            FadeIn(formula_box),
            Write(formula_txt),
            run_time=0.6
        )

        pos4_lbl = create_markup_text(
            "<b>Inspect the 4th position in the draft sequence:</b>",
            font_size=10, color=WHITE
        ).move_to(LEFT * 3.5 + UP * 0.1)

        draft_bar_rect = Rectangle(width=1.0, height=2.4, color=ORANGE, fill_color=ORANGE, fill_opacity=0.7)
        target_bar_rect = Rectangle(width=1.0, height=0.6, color=BLUE, fill_color=BLUE, fill_opacity=0.7)
        target_alt_rect = Rectangle(width=1.0, height=2.1, color=GREEN_C, fill_color=GREEN_C, fill_opacity=0.7)

        baseline_y = -2.6
        draft_bar_rect.move_to(np.array([0.8, baseline_y + 2.4 / 2, 0]))
        target_bar_rect.move_to(np.array([2.2, baseline_y + 0.6 / 2, 0]))
        target_alt_rect.move_to(np.array([3.6, baseline_y + 2.1 / 2, 0]))

        ground_y = baseline_y - 0.025
        ground_line = Line(
            start=np.array([0.1, ground_y, 0]),
            end=np.array([4.3, ground_y, 0]),
            color=GRAY, stroke_width=2
        )

        draft_bar_lbl = create_text("P_draft('sun')\n= 0.8", font_size=8, color=ORANGE).next_to(draft_bar_rect, UP, buff=0.1)
        target_bar_lbl = create_text("P_target('sun')\n= 0.2", font_size=8, color=BLUE).next_to(target_bar_rect, UP, buff=0.1)
        target_alt_lbl = create_text("P_target('moon')\n= 0.7", font_size=8, color=GREEN_B).next_to(target_alt_rect, UP, buff=0.1)

        self.play(
            Write(pos4_lbl),
            Create(ground_line),
            FadeIn(draft_bar_rect), FadeIn(draft_bar_lbl),
            FadeIn(target_bar_rect), FadeIn(target_bar_lbl),
            FadeIn(target_alt_rect), FadeIn(target_alt_lbl),
            run_time=0.8
        )

        explain_box = RoundedRectangle(width=4.0, height=1.0, color=RED, fill_color="#2b1414", fill_opacity=0.9, corner_radius=0.05)
        explain_box.move_to(LEFT * 3.5 + DOWN * 0.8)
        explain_txt = create_markup_text(
            "Acceptance ratio = <sup>0.2</sup>/<sub>0.8</sub> = 25%\n"
            "<span foreground=\"#FF5555\"><b>High rejection risk (75%)</b></span>",
            font_size=8, color=WHITE, line_spacing=1.2
        ).move_to(explain_box.get_center())

        self.play(
            FadeIn(explain_box),
            Write(explain_txt),
            run_time=0.5
        )

        reject_label = create_text("REJECT (REJECT)", font_size=12, color=RED, weight=BOLD).move_to(LEFT * 3.5 + DOWN * 1.8)
        self.play(Write(reject_label), run_time=0.4)

        self.play(
            FadeOut(math_intro),
            FadeOut(formula_box), FadeOut(formula_txt),
            FadeOut(pos4_lbl), FadeOut(ground_line),
            FadeOut(draft_bar_rect), FadeOut(draft_bar_lbl),
            FadeOut(target_bar_rect), FadeOut(target_bar_lbl),
            FadeOut(target_alt_rect), FadeOut(target_alt_lbl),
            FadeOut(explain_box), FadeOut(explain_txt),
            FadeOut(reject_label),
            run_time=0.4
        )

        laser_intro = create_markup_text(
            "<b>Step 3: Laser cut &amp; revise the sequence</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(laser_intro), run_time=0.5)

        conveyor_belt = VGroup(belt_line, belt_roller_left, belt_roller_right)
        self.play(Create(conveyor_belt), run_time=0.4)

        belt_tokens = VGroup()
        belt_lbls = VGroup()
        tokens_full = ["The", "cow", "jumped", "over", "the", "sun", "."]
        for i, tok_text in enumerate(tokens_full):
            dest_x = -4.0 + i * 1.33
            color = GRAY_A if i < 2 else ORANGE
            fill_color = "#1a1c1e" if i < 2 else "#2a1a0f"
            tok_box = RoundedRectangle(width=0.9, height=0.55, color=color, fill_color=fill_color, fill_opacity=0.9, corner_radius=0.04)
            tok_box.move_to(np.array([dest_x, -0.8, 0]))
            tok_lbl = create_text(tok_text, font_size=10, color=WHITE).move_to(tok_box.get_center())
            belt_tokens.add(tok_box)
            belt_lbls.add(tok_lbl)

        self.play(
            FadeIn(belt_tokens), FadeIn(belt_lbls),
            run_time=0.5
        )

        self.play(
            *[belt_tokens[i].animate.set_color(GREEN).set_fill("#142b1a", opacity=0.9) for i in range(2, 5)],
            *[belt_lbls[i].animate.set_color(GREEN_A) for i in range(2, 5)],
            run_time=0.3
        )

        self.play(
            *[belt_tokens[i].animate.set_color(RED).set_fill("#2b1414", opacity=0.9) for i in range(5, 7)],
            *[belt_lbls[i].animate.set_color(RED_A) for i in range(5, 7)],
            run_time=0.3
        )

        laser_beam = Line(start=UP * 1.0 + RIGHT * 2.0, end=DOWN * 2.2 + RIGHT * 2.0, color=RED, stroke_width=6)
        laser_spark = Star(color=YELLOW, fill_color=YELLOW, fill_opacity=1.0, stroke_width=1).scale(0.25).move_to(RIGHT * 2.0 + DOWN * 0.8)

        self.play(
            Create(laser_beam),
            FadeIn(laser_spark),
            run_time=0.2
        )
        self.play(
            laser_spark.animate.scale(1.8),
            laser_beam.animate.set_color(YELLOW),
            run_time=0.2
        )
        self.play(
            laser_spark.animate.scale(0.55),
            laser_beam.animate.set_color(RED),
            run_time=0.2
        )

        self.play(
            VGroup(belt_tokens[5], belt_lbls[5]).animate.scale(0.1).shift(DOWN * 1.5).set_opacity(0),
            VGroup(belt_tokens[6], belt_lbls[6]).animate.scale(0.1).shift(DOWN * 1.5).set_opacity(0),
            FadeOut(laser_beam), FadeOut(laser_spark),
            run_time=0.4
        )

        corrected_box = RoundedRectangle(width=0.9, height=0.55, color=BLUE, fill_color="#14202b", fill_opacity=0.9, corner_radius=0.04)
        corrected_box.move_to(RIGHT * 2.67 + DOWN * 0.8)
        corrected_lbl = create_text("Moon", font_size=10, color=BLUE_A).move_to(corrected_box.get_center())

        success_arrow = Arrow(start=RIGHT * 2.67 + UP * 0.5, end=RIGHT * 2.67 + DOWN * 0.4, color=BLUE_A, stroke_width=2.5)
        success_lbl = create_text("Revision successful!", font_size=8, color=BLUE_B).next_to(success_arrow, UP, buff=0.1)

        self.play(
            FadeIn(corrected_box), FadeIn(corrected_lbl),
            Create(success_arrow), Write(success_lbl),
            run_time=0.5
        )

        final_seq_box = RoundedRectangle(width=6.8, height=0.9, color=GREEN_B, fill_color="#111111", fill_opacity=0.95, corner_radius=0.08)
        final_seq_box.move_to(DOWN * 2.1)
        final_seq_txt = create_text("Generated result: \"The cow jumped over the moon\"", font_size=14, color=WHITE).move_to(final_seq_box.get_center())

        self.play(
            FadeIn(final_seq_box),
            Write(final_seq_txt),
            run_time=0.6
        )

        self.play(
            FadeOut(laser_intro),
            FadeOut(conveyor_belt),
            *[FadeOut(belt_tokens[i]) for i in range(5)],
            *[FadeOut(belt_lbls[i]) for i in range(5)],
            FadeOut(corrected_box), FadeOut(corrected_lbl),
            FadeOut(success_arrow), FadeOut(success_lbl),
            FadeOut(final_seq_box), FadeOut(final_seq_txt),
            run_time=0.5
        )

        # =====================================================================
        # Cue 7 (sc42_007): Decoding memory-bound.
        # =====================================================================
        self.wait_until(cue_start[7] + 0.1)
        intro_text = create_markup_text(
            "<b>VRAM &amp; Bandwidth Bottleneck (Memory Bottleneck)</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 1.8)
        self.play(Write(intro_text), run_time=0.5)

        draft_box = RoundedRectangle(width=2.0, height=1.4, color=ORANGE, fill_color="#2a1a0f", fill_opacity=0.9, corner_radius=0.06)
        draft_box.move_to(LEFT * 3.5 + DOWN * 0.8)
        draft_lbl = create_markup_text("<b>Draft Model</b>\n<span foreground=\"#FFA500\">Draft Model (1B)</span>", font_size=10, color=ORANGE, line_spacing=1.2).next_to(draft_box, UP, buff=0.15)
        
        draft_cores = VGroup()
        for r in range(2):
            for c in range(2):
                core = Square(side_length=0.2, color=ORANGE, fill_color=ORANGE, fill_opacity=0.15, stroke_width=0.8)
                core.move_to(draft_box.get_center() + RIGHT * (c - 0.5) * 0.4 + UP * (r - 0.5) * 0.4)
                draft_cores.add(core)

        target_box = RoundedRectangle(width=3.6, height=2.6, color=BLUE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        target_box.move_to(RIGHT * 3.5 + DOWN * 0.8)
        target_lbl = create_markup_text("<b>Target Model</b>\n<span foreground=\"#33AAFF\">Target Model (70B)</span>", font_size=10, color=BLUE, line_spacing=1.2).next_to(target_box, UP, buff=0.15)

        target_cores = VGroup()
        for r in range(4):
            for c in range(4):
                core = Square(side_length=0.22, color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=0.8)
                core.move_to(target_box.get_center() + RIGHT * (c - 1.5) * 0.45 + UP * (r - 1.5) * 0.42)
                target_cores.add(core)

        self.play(
            FadeIn(draft_box), FadeIn(draft_lbl), FadeIn(draft_cores),
            FadeIn(target_box), FadeIn(target_lbl), FadeIn(target_cores),
            run_time=0.6
        )

        draft_packets = VGroup(*[
            Dot(color=ORANGE, radius=0.06).move_to(draft_box.get_center() + LEFT * 3 + UP * 2)
            for _ in range(4)
        ])
        
        target_packets = VGroup(*[
            Rectangle(width=0.4, height=0.25, color=BLUE_A, fill_color=BLUE, fill_opacity=0.8, stroke_width=1).move_to(target_box.get_center() + RIGHT * 3 + UP * 2)
            for _ in range(4)
        ])

        self.play(
            LaggedStart(
                *[p.animate(run_time=0.4, rate_func=smooth).move_to(draft_box.get_center()) for p in draft_packets],
                lag_ratio=0.15
            ),
            LaggedStart(
                *[p.animate(run_time=0.8, rate_func=linear).move_to(target_box.get_center()) for p in target_packets],
                lag_ratio=0.3
            ),
            run_time=1.0
        )

        self.play(
            *[c.animate(run_time=0.15).set_fill(ORANGE, opacity=0.8) for c in draft_cores],
            run_time=0.2
        )
        self.play(
            *[c.animate(run_time=0.15).set_fill(ORANGE, opacity=0.15) for c in draft_cores],
            FadeOut(draft_packets),
            run_time=0.2
        )
        
        self.play(
            *[c.animate(run_time=0.2).set_fill(BLUE, opacity=0.8) for c in target_cores],
            run_time=0.3
        )
        self.play(
            *[c.animate(run_time=0.2).set_fill(BLUE, opacity=0.15).set_color(BLUE) for c in target_cores],
            FadeOut(target_packets),
            run_time=0.3
        )

        # =====================================================================
        # Cue 8 (sc42_008): MagicDec throughput/latency curves analysis.
        # =====================================================================
        self.wait_until(cue_start[8] + 0.1)
        self.play(
            FadeOut(intro_text),
            FadeOut(draft_box), FadeOut(draft_lbl), FadeOut(draft_cores),
            FadeOut(target_box), FadeOut(target_lbl), FadeOut(target_cores),
            run_time=0.5
        )

        magicdec_title = create_text("Throughput vs. Context length (MagicDec)", font_size=13, color=YELLOW)
        magicdec_title.to_edge(UP, buff=0.4)
        
        self.play(FadeIn(magicdec_title), run_time=0.5)

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 8, 2],
            x_length=6.5,
            y_length=3.5,
            axis_config={"color": GRAY_C, "stroke_width": 2},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        ).move_to(DOWN * 0.2)

        x_lbl = create_text("Context length (Context Length)", font_size=8, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.25)
        y_lbl = create_text("Throughput (Throughput)", font_size=8, color=GRAY_A).next_to(axes.y_axis, LEFT, buff=0.25).rotate(90 * DEGREES)

        std_curve = axes.plot(lambda x: 3.5 - 0.05 * x, x_range=[0, 10], color=BLUE, stroke_width=3)
        spec_curve = axes.plot(lambda x: 1.8 + 1.4 * (x ** 0.5), x_range=[0, 10], color=GREEN, stroke_width=4)

        legend_std_line = Line(start=LEFT * 0.2, end=RIGHT * 0.2, color=BLUE, stroke_width=3)
        legend_std_lbl = create_text("Standard decoding (Standard)", font_size=7, color=BLUE)
        legend_std = VGroup(legend_std_line, legend_std_lbl).arrange(RIGHT, buff=0.12)

        legend_spec_line = Line(start=LEFT * 0.2, end=RIGHT * 0.2, color=GREEN, stroke_width=4)
        legend_spec_lbl = create_text("Speculative Decoding (Speculative)", font_size=7, color=GREEN)
        legend_spec = VGroup(legend_spec_line, legend_spec_lbl).arrange(RIGHT, buff=0.12)

        legend = VGroup(legend_std, legend_spec).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        legend.move_to(axes.c2p(2.2, 6.8))

        self.play(
            Create(axes),
            Write(x_lbl), Write(y_lbl),
            Create(std_curve), Create(spec_curve),
            FadeIn(legend),
            run_time=1.5
        )

        # =====================================================================
        # Cue 9 (sc42_009): Speculative decoding sequential-to-parallel conversion concept.
        # =====================================================================
        self.wait_until(cue_start[9] + 0.1)
        self.play(
            FadeOut(axes), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(std_curve), FadeOut(spec_curve), FadeOut(legend),
            FadeOut(magicdec_title),
            run_time=0.5
        )

        conclusion_title = create_text("Performance evaluation of Speculative Decoding", font_size=13, color=YELLOW)
        conclusion_title.to_edge(UP, buff=0.4)
        self.play(
            FadeIn(conclusion_title),
            run_time=0.5
        )

        comparison_table = VGroup()
        headers = ["Decoding method", "Weight loading time", "Tokens generated / pass", "Speed efficiency"]
        header_colors = [WHITE, WHITE, WHITE, GREEN]
        
        header_group = VGroup()
        for idx, h_text in enumerate(headers):
            cell = RoundedRectangle(width=2.5, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            cell.move_to(LEFT * (2.7 * (1.5 - idx)) + UP * 1.0)
            lbl = create_text(h_text, font_size=8.5, color=header_colors[idx]).move_to(cell.get_center())
            header_group.add(VGroup(cell, lbl))
        comparison_table.add(header_group)

        table_rows = [
            ("Standard decoding", "Continuously load 70B weights", "1 Token", "1.0x (baseline axis)"),
            ("Speculative Decoding", "Load 70B weights only once", "4 Token (3 accepted + 1 corrected)", "2.0x - 3.0x speed")
        ]

        row_y_coords = [0.1, -0.9]
        row_colors = [GRAY, GREEN_B]
        for r_idx, row_data in enumerate(table_rows):
            row_group = VGroup()
            for c_idx, cell_text in enumerate(row_data):
                cell = RoundedRectangle(width=2.5, height=0.8, color=GRAY_E, fill_color="#121315", fill_opacity=0.8, corner_radius=0.04)
                cell.move_to(LEFT * (2.7 * (1.5 - c_idx)) + UP * row_y_coords[r_idx])
                
                t_color = row_colors[r_idx] if c_idx == 3 else WHITE
                lbl = create_text(cell_text, font_size=8.5, color=t_color).move_to(cell.get_center())
                
                row_group.add(VGroup(cell, lbl))
            comparison_table.add(row_group)

        tradeoff_note = create_markup_text(
            "<b>Note:</b> If the draft model predicts many tokens incorrectly, the acceptance rate drops,\n"
            "speed efficiency suffers because extra draft-model cost is wasted.",
            font_size=9.5, color=WHITE, line_spacing=1.2
        ).move_to(DOWN * 2.1)

        self.play(
            FadeIn(comparison_table),
            Write(tradeoff_note),
            run_time=1.2
        )

        # =====================================================================
        # Cue 10 (sc42_010): Proposal vs main model differences.
        # =====================================================================
        self.wait_until(cue_start[10] + 0.1)
        self.play(
            comparison_table[2].animate.set_color(YELLOW),
            run_time=1.0
        )
        self.play(
            comparison_table[2].animate.set_color(GRAY_E),
            run_time=1.0
        )

        # =====================================================================
        # Cue 11 (sc42_011): All-at-once verification.
        # =====================================================================
        self.wait_until(cue_start[11] + 0.1)
        code_title = create_text("Algorithm source code", font_size=13, color=YELLOW)
        code_title.to_edge(UP, buff=0.4)
        
        code_window = RoundedRectangle(width=9.0, height=4.2, color=GRAY_A, fill_color="#0d0e11", fill_opacity=0.95, corner_radius=0.08)
        code_window.move_to(DOWN * 0.2)

        title_bar = Rectangle(width=9.0, height=0.4, color=GRAY_A, fill_color="#1e1f22", fill_opacity=1.0, stroke_width=0.5)
        title_bar.move_to(code_window.get_top() + DOWN * 0.2)
        
        dots = VGroup(*[Dot(radius=0.06, color=c) for c in [RED, YELLOW, GREEN]])
        dots.arrange(RIGHT, buff=0.12).next_to(title_bar.get_left(), RIGHT, buff=0.25)
        file_name = create_text("speculative_decode.py", font_size=8, color=GRAY_A).next_to(dots, RIGHT, buff=0.4)

        code_content = create_markup_text(
            "<span foreground=\"#CC7832\">def</span> <span foreground=\"#FFC66D\">speculative_decode</span>(tgt_m, drf_m, tok, inp, max_tok):\n"
            "    gen = inp\n"
            "    <span foreground=\"#CC7832\">while</span> gen.shape[1] &lt; max_len:\n"
            "        <span foreground=\"#808080\"># Generate draft sequence from Draft Model</span>\n"
            "        spec_id, spec_lprob = generate(drf_m, tok, gen, spec_size)\n"
            "        <span foreground=\"#808080\"># Parallel verification by Target Model</span>\n"
            "        tgt_lprob = tgt_m(spec_id)\n"
            "        <span foreground=\"#808080\"># Rejection Sampling (Rejection Sampling)</span>\n"
            "        rejs = compute_ll_rejs(tgt_lprob, spec_lprob)\n"
            "        accepted = spec_id[:, :rejs[0]]\n"
            "        gen = torch.cat([gen, accepted, next_tok])\n"
            "    <span foreground=\"#CC7832\">return</span> gen",
            font_size=9, font="Consolas", color=WHITE, line_spacing=1.3
        ).move_to(code_window.get_center() + DOWN * 0.1)

        self.play(
            FadeOut(conclusion_title), FadeOut(comparison_table), FadeOut(tradeoff_note),
            FadeIn(code_title), FadeIn(code_window), FadeIn(title_bar), FadeIn(dots), FadeIn(file_name),
            Write(code_content),
            run_time=1.5
        )

        # =====================================================================
        # Cue 12 (sc42_012): High-accuracy draft model savings.
        # =====================================================================
        self.wait_until(cue_start[12] + 0.1)
        highlight_box = SurroundingRectangle(code_content, color=GOLD, stroke_width=2, corner_radius=0.04)
        self.play(Create(highlight_box), run_time=1.0)

        # =====================================================================
        # Cue 13 (sc42_013): Not always beneficial warning.
        # =====================================================================
        self.wait_until(cue_start[13] + 0.1)
        self.play(
            FadeOut(code_window), FadeOut(title_bar), FadeOut(dots), FadeOut(file_name),
            FadeOut(code_content), FadeOut(highlight_box), FadeOut(code_title),
            FadeIn(magicdec_title), FadeIn(axes), FadeIn(x_lbl), FadeIn(y_lbl),
            FadeIn(std_curve), FadeIn(spec_curve), FadeIn(legend),
            run_time=1.0
        )

        # =====================================================================
        # Cue 14 (sc42_014): Low context overhead.
        # =====================================================================
        self.wait_until(cue_start[14] + 0.1)
        low_ctx_dot = Dot(axes.c2p(1, 1.8 + 1.4), color=RED, radius=0.06)
        low_ctx_arrow = Arrow(start=axes.c2p(1.0, 1.0), end=axes.c2p(1.0, 2.9), color=RED, stroke_width=2)
        low_ctx_lbl = create_text("Throughput drops\n(due to draft overhead)", font_size=6, color=RED).next_to(low_ctx_arrow, DOWN, buff=0.1)

        self.play(
            FadeIn(low_ctx_dot),
            Create(low_ctx_arrow),
            Write(low_ctx_lbl),
            run_time=1.0
        )

        # =====================================================================
        # Cue 15 (sc42_015): Long context benefits.
        # =====================================================================
        self.wait_until(cue_start[15] + 0.1)
        long_ctx_dot = Dot(axes.c2p(8, 1.8 + 1.4 * (8**0.5)), color=GREEN, radius=0.06)
        long_ctx_arrow = Arrow(start=axes.c2p(8.0, 7.2), end=axes.c2p(8.0, 6.0), color=GREEN, stroke_width=2)
        long_ctx_lbl = create_markup_text("<b>Improve both throughput &amp; latency\n(MagicDec)</b>", font_size=6, color=GREEN).next_to(long_ctx_arrow, UP, buff=0.1)

        self.play(
            FadeIn(long_ctx_dot),
            Create(long_ctx_arrow),
            Write(long_ctx_lbl),
            run_time=1.0
        )

        # =====================================================================
        # End of Scene
        # =====================================================================
        self.wait_until(voiceover_end + 0.35)
        self.play(
            FadeOut(axes), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(std_curve), FadeOut(spec_curve), FadeOut(legend),
            FadeOut(low_ctx_dot), FadeOut(low_ctx_arrow), FadeOut(low_ctx_lbl),
            FadeOut(long_ctx_dot), FadeOut(long_ctx_arrow), FadeOut(long_ctx_lbl),
            FadeOut(magicdec_title),
            run_time=0.8
        )
        assert_all_scene_voiceovers_played(self)
