import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_3_1_DURATIONS = {
    "sc31_001.mp3": 5.154830,
    "sc31_002.mp3": 4.643991,
    "sc31_003.mp3": 3.018594,
    "sc31_004.mp3": 9.659501,
    "sc31_005.mp3": 10.727619,
    "sc31_006.mp3": 9.009342,
    "sc31_007.mp3": 4.365351,
    "sc31_008.mp3": 15.046531,
    "sc31_009.mp3": 9.566621,
    "sc31_010.mp3": 7.105306,
    "sc31_011.mp3": 4.272472,
    "sc31_012.mp3": 12.213696,
    "sc31_013.mp3": 5.201270,
    "sc31_014.mp3": 5.712109,
    "sc31_015.mp3": 7.848345,
    "sc31_016.mp3": 7.894785,
    "sc31_017.mp3": 5.433469,
    "sc31_018.mp3": 7.105306,
    "sc31_019.mp3": 8.730703,
    "sc31_020.mp3": 9.055782,
    "sc31_021.mp3": 5.526349,
    "sc31_022.mp3": 8.080544,
}
SCENE_3_1_VOICEOVERS = tuple(SCENE_3_1_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc31_*.mp3"))
    expected = sorted(SCENE_3_1_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 3.1 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_3_1_DURATIONS:
        raise KeyError(f"Unexpected Scene 3.1 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 3.1 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_3_1_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_3_1_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 3.1 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


def create_text(text, font_size=24, font="Noto Sans", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)


def create_markup_text(text, font_size=24, font="Noto Sans", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)


def get_checkmark(color=GREEN, stroke_width=2.5):
    checkmark = VMobject(color=color, stroke_width=stroke_width)
    checkmark.set_points_as_corners([
        LEFT * 0.12 + DOWN * 0.05,
        ORIGIN + DOWN * 0.15,
        RIGHT * 0.2 + UP * 0.15
    ])
    return checkmark


def get_crossmark(color=RED, stroke_width=2.5):
    cross = VGroup()
    line1 = Line(LEFT * 0.12 + UP * 0.12, RIGHT * 0.12 + DOWN * 0.12, color=color, stroke_width=stroke_width)
    line2 = Line(LEFT * 0.12 + DOWN * 0.12, RIGHT * 0.12 + UP * 0.12, color=color, stroke_width=stroke_width)
    cross.add(line1, line2)
    return cross


class Scene3_1(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def replace_content(self, old_group, new_group, run_time=0.55):
        if old_group is None:
            self.play(FadeIn(new_group, shift=UP * 0.12), run_time=run_time)
        else:
            self.play(FadeOut(old_group, shift=DOWN * 0.08), FadeIn(new_group, shift=UP * 0.08), run_time=run_time)
        return new_group

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (filename, duration) in enumerate(SCENE_3_1_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        # --- Chapter Title ---
        chapter_title = create_text("Chapter 3: High-Level Orchestrators", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 3.1: Evaluator Models & Chaining Techniques", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub).move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)
        self.wait(3.0)

        sub_title = create_text("Evaluator models & Chaining techniques", font_size=16, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=1.0)
        
        content = None

        # --- Cue 1: Goal of Generator G ---
        self.wait_until(cue_start[1] + 0.2)
        intro_pill = VGroup(
            create_text("Goal: Generator System G that produces acceptable outputs y", font_size=14, color=WHITE),
            create_markup_text("Evaluator <span color='#33ccff'>A(y)</span>: Scores acceptability (correctness / preference)", font_size=13, color=GRAY_A)
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.4)
        content = self.replace_content(content, intro_pill)

        # --- Cue 2: Expected Acceptability Objective ---
        self.wait_until(cue_start[2] + 0.2)
        objective_group = VGroup(
            create_text("Objective: Maximize Expected Acceptability", font_size=14, color=YELLOW),
            create_markup_text(
                "arg max<sub>G</sub>   E<sub>y ~ G(·|x)</sub> [ A(y) ]",
                font_size=16, color=WHITE
            )
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.4)
        content = self.replace_content(content, objective_group)

        # --- Cue 3: Definition of Acceptability ---
        self.wait_until(cue_start[3] + 0.2)
        acceptability_group = VGroup(
            create_text("Acceptability A(y) can measure:", font_size=14, color=WHITE),
            create_markup_text("• Correctness (e.g. external code/math verifiers)", font_size=12, color=GREEN),
            create_markup_text("• Human Preference (e.g. RLHF reward models)", font_size=12, color=BLUE)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 0.4)
        content = self.replace_content(content, acceptability_group)

        # --- Cue 4: black box generator ---
        self.wait_until(cue_start[4] + 0.25)
        
        black_box = RoundedRectangle(width=3.2, height=1.4, color=GRAY_D, fill_color="#1a1c20", fill_opacity=0.9, corner_radius=0.08).move_to(DOWN * 0.5)
        black_box_lbl = create_text("Base Generator\n(LLM Black Box)", font_size=11, color=WHITE).move_to(black_box.get_center())
        
        token_x = create_text("Input x", font_size=11, color=GREEN).next_to(black_box, LEFT, buff=1.2)
        arrow_in = Arrow(start=token_x.get_right(), end=black_box.get_left(), color=GREEN, stroke_width=2, buff=0.1)
        
        token_y = create_text("Output y", font_size=11, color=YELLOW).next_to(black_box, RIGHT, buff=1.2)
        arrow_out = Arrow(start=black_box.get_right(), end=token_y.get_left(), color=YELLOW, stroke_width=2, buff=0.1)
        
        black_box_group = VGroup(black_box, black_box_lbl, token_x, arrow_in, token_y, arrow_out)
        content = self.replace_content(content, black_box_group)

        # --- Cue 5: Meta-generation controller ---
        self.wait_until(cue_start[5] + 0.25)
        
        controller_frame = RoundedRectangle(width=9.6, height=3.8, color=BLUE_A, fill_color=BLUE_E, fill_opacity=0.08, corner_radius=0.15, stroke_width=2).move_to(DOWN * 0.5)
        controller_lbl = create_text("Meta-Generation Controller", font_size=13, color=BLUE_A).next_to(controller_frame.get_top(), DOWN, buff=0.18)
        
        # External Evaluator block in feedback loop
        eval_box = RoundedRectangle(width=2.4, height=0.8, color=BLUE_A, fill_color="#181e28", fill_opacity=0.95, corner_radius=0.06).move_to(DOWN * 1.8)
        eval_lbl = create_markup_text("<b>Evaluator A(y)</b>", font_size=9.5, color=BLUE_A).move_to(eval_box.get_center())
        eval_group = VGroup(eval_box, eval_lbl)
        
        arrow_y_eval = CurvedArrow(
            start_point=token_y.get_bottom() + DOWN * 0.05,
            end_point=eval_box.get_right() + RIGHT * 0.05,
            angle=-PI/3,
            color=BLUE_A,
            stroke_width=1.5
        )
        arrow_eval_x = CurvedArrow(
            start_point=eval_box.get_left() + LEFT * 0.05,
            end_point=token_x.get_bottom() + DOWN * 0.05,
            angle=-PI/3,
            color=BLUE_A,
            stroke_width=1.5
        )
        
        feedback_lbl = create_text("Feedback loop with Evaluator", font_size=9, color=BLUE_A).next_to(eval_box, DOWN, buff=0.1)
        
        controller_group = VGroup(controller_frame, controller_lbl, eval_group, arrow_y_eval, arrow_eval_x, feedback_lbl)
        self.play(FadeIn(controller_group), run_time=0.8)

        # --- Cue 6: Terminology and Equivalences ---
        self.wait_until(cue_start[6] + 0.2)
        
        term_box = RoundedRectangle(width=9.5, height=2.6, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.1).move_to(DOWN * 0.5)
        term_title = create_text("Terminology & Equivalences (Slide 91-92)", font_size=13, color=YELLOW).next_to(term_box.get_top(), DOWN, buff=0.18)
        term_text = create_markup_text(
            "<b>Evaluator  ≈  Critic  ≈  Verifier  ≈  Value  ≈  Reward Model  ≈  Scoring Model</b>\n\n"
            "Approximates acceptability:  <span color='#55ff55'>v(y) ≈ A(y)</span>",
            font_size=11, color=WHITE, line_spacing=1.4
        ).next_to(term_title, DOWN, buff=0.25)
        
        term_group = VGroup(term_box, term_title, term_text)
        
        self.play(FadeOut(controller_group), run_time=0.4)
        content = self.replace_content(content, term_group)

        # --- Cue 7-8: Oracle Verifier Loop ---
        self.wait_until(cue_start[7] + 0.25)
        
        flow_x = create_text("Input x", font_size=11, color=GREEN).move_to(LEFT * 4.5 + DOWN * 0.5)
        flow_gen = RoundedRectangle(width=2.2, height=1.2, color=BLUE, fill_color="#1a1c20", fill_opacity=0.9, corner_radius=0.08).move_to(LEFT * 1.5 + DOWN * 0.5)
        flow_gen_lbl = create_text("Generator", font_size=11, color=WHITE).move_to(flow_gen.get_center())
        flow_y = create_markup_text("Answer y\n<i>y ~ p<sub>θ</sub>(y|x,z)</i>", font_size=9, color=YELLOW).move_to(RIGHT * 1.2 + DOWN * 0.5)
        flow_ver = RoundedRectangle(width=2.2, height=1.2, color=ORANGE, fill_color="#1a1c20", fill_opacity=0.9, corner_radius=0.08).move_to(RIGHT * 4.2 + DOWN * 0.5)
        flow_ver_lbl = create_text("Verifier\n(A(y) = 1?)", font_size=10, color=WHITE).move_to(flow_ver.get_center())
        
        arr_x_gen = Arrow(flow_x.get_right(), flow_gen.get_left(), color=GRAY_C, stroke_width=1.5, buff=0.1)
        arr_gen_y = Arrow(flow_gen.get_right(), flow_y.get_left(), color=GRAY_C, stroke_width=1.5, buff=0.1)
        arr_y_ver = Arrow(flow_y.get_right() + LEFT * 0.1, flow_ver.get_left(), color=GRAY_C, stroke_width=1.5, buff=0.1)
        
        # Stop Arrow
        flow_stop = create_text("Stop (Correct)", font_size=10, color=GREEN).next_to(flow_ver, UP, buff=0.9)
        arr_ver_stop = Arrow(flow_ver.get_top(), flow_stop.get_bottom(), color=GREEN, stroke_width=1.5, buff=0.1)
        
        # Loop Arrow
        loop_back = CurvedArrow(start_point=flow_ver.get_bottom() + DOWN * 0.1, end_point=flow_gen.get_bottom() + DOWN * 0.1, angle=-PI/2, color=RED)
        loop_lbl = create_markup_text("Incorrect: Generate <i>z ~ p<sub>θ</sub>(z|x)</i>", font_size=9, color=RED).next_to(loop_back, DOWN, buff=0.12)
        
        oracle_loop_group = VGroup(
            flow_x, flow_gen, flow_gen_lbl, flow_y, flow_ver, flow_ver_lbl,
            arr_x_gen, arr_gen_y, arr_y_ver, flow_stop, arr_ver_stop, loop_back, loop_lbl
        )
        content = self.replace_content(content, oracle_loop_group)

        # --- Cue 9-11: Mathematical Formalization ---
        self.wait_until(cue_start[9] + 0.2)
        
        formal_title = create_text("Formalization of Meta-Generator: Example", font_size=13, color=YELLOW).move_to(UP * 2.3)
        
        cropped_image_path = Path(__file__).resolve().parent / "assets" / "cropped_math_example.png"
        slide_image = ImageMobject(str(cropped_image_path))
        slide_image.set(width=7.5)
        slide_image.next_to(formal_title, DOWN, buff=0.25)
        
        source_text = create_text("https://neurips.cc/virtual/2024/tutorial/99522", font_size=8.5, color=GRAY_A)
        source_text.next_to(slide_image, DOWN, buff=0.15)
        
        formal_group = Group(formal_title, slide_image, source_text)
        content = self.replace_content(content, formal_group)

        # --- Cue 12: Chaining Definition ---
        self.wait_until(cue_start[12] + 0.2)
        
        chain_title = create_text("Chaining: Ordered Composition of Generators", font_size=14, color=YELLOW).move_to(UP * 1.0)
        box_g1 = RoundedRectangle(width=2.5, height=1.0, color=BLUE_A, fill_color="#1a1c20", fill_opacity=0.9, corner_radius=0.08).move_to(LEFT * 4.0 + DOWN * 0.5)
        lbl_g1 = create_markup_text("<b>g<sub>1</sub>(x)</b>\n→ y<sub>1</sub>", font_size=10, color=WHITE).move_to(box_g1.get_center())
        
        box_g2 = RoundedRectangle(width=2.8, height=1.0, color=BLUE_B, fill_color="#1a1c20", fill_opacity=0.9, corner_radius=0.08).move_to(DOWN * 0.5)
        lbl_g2 = create_markup_text("<b>g<sub>2</sub>(x, y<sub>1</sub>)</b>\n→ y<sub>2</sub>", font_size=10, color=WHITE).move_to(box_g2.get_center())
        
        box_g3 = RoundedRectangle(width=2.8, height=1.0, color=BLUE_C, fill_color="#1a1c20", fill_opacity=0.9, corner_radius=0.08).move_to(RIGHT * 4.0 + DOWN * 0.5)
        lbl_g3 = create_markup_text("<b>g<sub>3</sub>(x, y<sub>2</sub>)</b>\n→ y<sub>3</sub>", font_size=10, color=WHITE).move_to(box_g3.get_center())
        
        arr_1_2 = Arrow(box_g1.get_right(), box_g2.get_left(), color=GRAY_C, stroke_width=1.5, buff=0.1)
        arr_2_3 = Arrow(box_g2.get_right(), box_g3.get_left(), color=GRAY_C, stroke_width=1.5, buff=0.1)
        
        formula_chain = create_markup_text(
            "Formula:   <span color='#33ccff'>y<sub>1</sub> ~ g<sub>1</sub>(x)</span>,   "
            "<span color='#33ccff'>y<sub>2</sub> ~ g<sub>2</sub>(x, y<sub>1</sub>)</span>,   "
            "<span color='#33ccff'>y<sub>3</sub> ~ g<sub>3</sub>(x, y<sub>2</sub>)</span>",
            font_size=11, color=WHITE
        ).move_to(DOWN * 1.8)
        
        chain_flow_group = VGroup(chain_title, box_g1, lbl_g1, box_g2, lbl_g2, box_g3, lbl_g3, arr_1_2, arr_2_3, formula_chain)
        content = self.replace_content(content, chain_flow_group)

        # --- Cue 13-14: Chain of Thought & Memory Tape ---
        self.wait_until(cue_start[13] + 0.2)
        
        cot_lbl = create_text("Chain-of-Thought & Scratchpad Memory Tape", font_size=14, color=YELLOW).move_to(UP * 0.8)
        tape_boxes = VGroup()
        for j in range(7):
            box = Square(side_length=0.7, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.8)
            tape_boxes.add(box)
        tape_boxes.arrange(RIGHT, buff=0.08).move_to(DOWN * 0.4)
        
        rw_head = Triangle(color=BLUE_A, fill_color=BLUE_A, fill_opacity=0.6).scale(0.18).rotate(180 * DEGREES)
        rw_head.next_to(tape_boxes[0], UP, buff=0.1)
        
        cot_group = VGroup(cot_lbl, tape_boxes, rw_head)
        content = self.replace_content(content, cot_group)
        
        # Write thought tokens
        self.wait_until(cue_start[14] + 0.2)
        z_tokens = ["z1", "z2", "z3", "z4", "", "", ""]
        z_texts = VGroup()
        for j, tok in enumerate(z_tokens):
            if tok:
                txt = create_text(tok, font_size=12, color=BLUE_B)
                txt.move_to(tape_boxes[j].get_center())
                z_texts.add(txt)
                
        self.play(
            rw_head.animate.next_to(tape_boxes[3], UP, buff=0.1),
            Write(z_texts),
            run_time=1.2
        )

        # --- Cue 15-16: Self-Ask Workflow ---
        self.wait_until(cue_start[15] + 0.2)
        self.play(FadeOut(z_texts), run_time=0.3)
        
        question_box = RoundedRectangle(width=8.5, height=0.7, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08).move_to(UP * 0.8)
        question_text = create_markup_text("<b>Prompt x:</b> <i>\"Who is the president's spouse?\"</i>", font_size=11, color=YELLOW).move_to(question_box.get_center())
        
        sub_q1 = RoundedRectangle(width=4.5, height=0.6, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.05).move_to(LEFT * 2.2 + DOWN * 0.2)
        sub_q1_lbl = create_text("Self-Ask 1: Who is the president?", font_size=10, color=WHITE).move_to(sub_q1.get_center())
        
        tool_box = RoundedRectangle(width=2.8, height=1.6, color=ORANGE, fill_color=ORANGE, fill_opacity=0.08, corner_radius=0.1, stroke_width=2).move_to(RIGHT * 4.0 + DOWN * 0.8)
        tool_title = create_text("Search Engine\n/ Tools", font_size=11, color=ORANGE).move_to(tool_box.get_center())
        
        arrow_to_tool = Arrow(start=sub_q1.get_right(), end=tool_box.get_left() + UP * 0.3, color=ORANGE, stroke_width=1.5, buff=0.1)
        ans_val = create_text("Sub-answer: Joe Biden", font_size=10, color=GREEN).next_to(sub_q1, DOWN, buff=0.15)
        
        sub_q2 = RoundedRectangle(width=4.5, height=0.6, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.05).move_to(LEFT * 2.2 + DOWN * 1.5)
        sub_q2_lbl = create_text("Self-Ask 2: Who is Joe Biden's spouse?", font_size=10, color=WHITE).move_to(sub_q2.get_center())
        
        arrow_to_tool2 = Arrow(start=sub_q2.get_right(), end=tool_box.get_left() + DOWN * 0.3, color=ORANGE, stroke_width=1.5, buff=0.1)
        
        self_ask_group = VGroup(
            question_box, question_text, sub_q1, sub_q1_lbl, tool_box, tool_title,
            arrow_to_tool, ans_val, sub_q2, sub_q2_lbl, arrow_to_tool2
        )
        content = self.replace_content(content, self_ask_group)

        # --- Cue 17-18: Model Probability vs Acceptability ---
        self.wait_until(cue_start[17] + 0.2)
        
        prob_title = create_text("Model Probability vs. Acceptability (Slide 91)", font_size=13, color=YELLOW).move_to(UP * 2.0)
        
        card_prob = RoundedRectangle(width=4.8, height=2.4, color=RED, fill_color="#181212", fill_opacity=0.9, corner_radius=0.06)
        card_prob.move_to(LEFT * 2.8 + DOWN * 0.2)
        lbl_prob = create_markup_text(
            "<b>Model Probability p<sub>θ</sub>(y|x)</b>\n\n"
            "• Repetitive loops (e.g. \"the cow the cow...\")\n"
            "• Plausible-looking but incorrect reasoning\n"
            "• High local likelihood under LM objective",
            font_size=8.5, color=WHITE, line_spacing=1.3
        ).move_to(card_prob.get_center())
        
        card_acc = RoundedRectangle(width=4.8, height=2.4, color=GREEN, fill_color="#121812", fill_opacity=0.9, corner_radius=0.06)
        card_acc.move_to(RIGHT * 2.8 + DOWN * 0.2)
        lbl_acc = create_markup_text(
            "<b>Acceptability A(y)</b>\n\n"
            "• Correct mathematical / logical outputs\n"
            "• Safe, helpful, or human-preferred outputs\n"
            "• Evaluated by external critic, tests, or humans",
            font_size=8.5, color=WHITE, line_spacing=1.3
        ).move_to(card_acc.get_center())
        
        prob_vs_acc_group = VGroup(prob_title, card_prob, lbl_prob, card_acc, lbl_acc)
        content = self.replace_content(content, prob_vs_acc_group)

        # --- Cue 19: Overview Grid ---
        self.wait_until(cue_start[19] + 0.25)
        
        preview_title = create_text("Overview of High-Level Orchestrators (Meta-Generation)", font_size=13, color=YELLOW)
        preview_title.to_edge(UP, buff=1.0)
        
        def get_chain_icon(color):
            g = VGroup()
            c1 = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(LEFT * 0.45)
            c2 = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5)
            c3 = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(RIGHT * 0.45)
            a1 = Arrow(start=c1.get_right(), end=c2.get_left(), color=color, stroke_width=1.5, buff=0.02, max_tip_length_to_length_ratio=0.3)
            a2 = Arrow(start=c2.get_right(), end=c3.get_left(), color=color, stroke_width=1.5, buff=0.02, max_tip_length_to_length_ratio=0.3)
            g.add(c1, c2, c3, a1, a2)
            return g

        def get_parallel_icon(color):
            g = VGroup()
            for dy in [0.25, 0, -0.25]:
                arr = Arrow(start=LEFT*0.35 + UP*dy, end=RIGHT*0.35 + UP*dy, color=color, stroke_width=1.5, buff=0, max_tip_length_to_length_ratio=0.25)
                g.add(arr)
            return g

        def get_tree_icon(color):
            g = VGroup()
            r = Circle(radius=0.07, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(UP * 0.3)
            c_l = Circle(radius=0.07, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(DOWN * 0.35 + LEFT * 0.35)
            c_r = Circle(radius=0.07, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(DOWN * 0.35 + RIGHT * 0.35)
            l1 = Line(r.get_bottom() + LEFT*0.02, c_l.get_top() + RIGHT*0.02, color=color, stroke_width=1.5)
            l2 = Line(r.get_bottom() + RIGHT*0.02, c_r.get_top() + LEFT*0.02, color=color, stroke_width=1.5)
            g.add(r, c_l, c_r, l1, l2)
            return g

        def get_correction_icon(color):
            g = VGroup()
            node = Circle(radius=0.09, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5)
            loop = CurvedArrow(
                start_point=UP*0.11 + RIGHT*0.11,
                end_point=UP*0.11 + LEFT*0.11,
                angle=270 * DEGREES,
                color=color,
                stroke_width=1.5,
                tip_length=0.08
            ).shift(UP * 0.35)
            g.add(node, loop)
            return g

        def make_grid_cell(title_str, desc_str, pos, icon_creator, color=BLUE_A):
            cell = RoundedRectangle(width=5.2, height=1.6, color=color, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
            cell.move_to(pos)
            
            icon = icon_creator(color)
            icon.move_to(pos + LEFT * 1.8)
            
            title = create_text(title_str, font_size=11, color=color)
            title.move_to(pos + UP * 0.3)
            title.align_to(cell, LEFT)
            title.shift(RIGHT * 1.4)
            
            desc = create_text(desc_str, font_size=9, color=WHITE, line_spacing=1.3)
            desc.move_to(pos + DOWN * 0.3)
            desc.align_to(cell, LEFT)
            desc.shift(RIGHT * 1.4)
            
            return VGroup(cell, icon, title, desc)

        c1 = make_grid_cell("1. Chaining & CoT (Chaining)", "Decompose multi-step logical reasoning.\nGenerate z tokens as a scratchpad.", LEFT * 2.8 + UP * 0.5, get_chain_icon, color=BLUE_A)
        c2 = make_grid_cell("2. Parallel (Sinh song song)", "Best-of-N, Majority Voting, MBR.\nVote and integrate a reward model.", RIGHT * 2.8 + UP * 0.5, get_parallel_icon, color=GREEN)
        c3 = make_grid_cell("3. Tree Search (Tree search)", "Traverse trees ToT, MCTS, Backtracking.\nUse PRM to score each reasoning step.", LEFT * 2.8 + DOWN * 1.3, get_tree_icon, color=ORANGE)
        c4 = make_grid_cell("4. Self-Correction (Self-correction)", "The model revises its own draft.\nReceive extrinsic / intrinsic feedback.", RIGHT * 2.8 + DOWN * 1.3, get_correction_icon, color=PURPLE_A)

        grid_group = VGroup(preview_title, c1, c2, c3, c4)
        content = self.replace_content(content, grid_group)

        # --- Cue 20-22: CoT Decomposition, Writable Tape, and Meta-Generator Frame ---
        self.wait_until(cue_start[20] + 0.25)

        cot_prog_title = create_text("Chain-of-Thought: Decompose, Then Answer", font_size=14, color=YELLOW).move_to(UP * 2.35)

        meta_frame = RoundedRectangle(
            width=11.2,
            height=4.25,
            color=BLUE_A,
            fill_color=BLUE_E,
            fill_opacity=0.06,
            corner_radius=0.12,
            stroke_width=1.8,
        ).move_to(DOWN * 0.15)
        meta_label = create_text("Meta-generator", font_size=11, color=BLUE_A)
        meta_label.next_to(meta_frame.get_top(), DOWN, buff=0.12)

        prompt_box = RoundedRectangle(width=1.65, height=0.75, color=GREEN, fill_color="#132018", fill_opacity=0.9, corner_radius=0.08)
        prompt_box.move_to(LEFT * 4.55 + UP * 0.35)
        prompt_label = create_text("Prompt x", font_size=10.5, color=GREEN).move_to(prompt_box.get_center())

        thought_box = RoundedRectangle(width=2.55, height=0.85, color=BLUE_A, fill_color="#151d27", fill_opacity=0.95, corner_radius=0.08)
        thought_box.move_to(LEFT * 1.35 + UP * 0.35)
        thought_label = create_text("Generate thought z", font_size=10.5, color=BLUE_A).move_to(thought_box.get_center())

        combine_box = RoundedRectangle(width=1.65, height=0.75, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        combine_box.move_to(RIGHT * 1.75 + UP * 0.35)
        combine_label = create_text("Use x + z", font_size=10.5, color=WHITE).move_to(combine_box.get_center())

        answer_box = RoundedRectangle(width=1.75, height=0.75, color=YELLOW, fill_color="#242112", fill_opacity=0.9, corner_radius=0.08)
        answer_box.move_to(RIGHT * 4.65 + UP * 0.35)
        answer_label = create_text("Answer y", font_size=10.5, color=YELLOW).move_to(answer_box.get_center())

        arr_prompt_thought = Arrow(prompt_box.get_right(), thought_box.get_left(), color=GRAY_C, stroke_width=1.7, buff=0.12)
        arr_thought_combine = Arrow(thought_box.get_right(), combine_box.get_left(), color=GRAY_C, stroke_width=1.7, buff=0.12)
        arr_combine_answer = Arrow(combine_box.get_right(), answer_box.get_left(), color=GRAY_C, stroke_width=1.7, buff=0.12)

        pipeline_group = VGroup(
            prompt_box, prompt_label,
            thought_box, thought_label,
            combine_box, combine_label,
            answer_box, answer_label,
            arr_prompt_thought, arr_thought_combine, arr_combine_answer,
        )

        tape_label = create_text("Writable tape / scratchpad", font_size=10.5, color=GRAY_A).move_to(LEFT * 3.25 + DOWN * 1.05)
        tape_boxes = VGroup()
        for _ in range(6):
            box = Square(side_length=0.58, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.82, stroke_width=1.4)
            tape_boxes.add(box)
        tape_boxes.arrange(RIGHT, buff=0.08).move_to(DOWN * 1.65)

        tape_arrow_down = Arrow(thought_box.get_bottom(), tape_boxes[1].get_top(), color=BLUE_A, stroke_width=1.5, buff=0.12)
        tape_arrow_up = Arrow(tape_boxes[4].get_top(), combine_box.get_bottom(), color=BLUE_A, stroke_width=1.5, buff=0.12)

        tape_group = VGroup(tape_label, tape_boxes, tape_arrow_down, tape_arrow_up)

        cot_program_group = VGroup(cot_prog_title, meta_frame, meta_label, pipeline_group, tape_group)
        content = self.replace_content(content, cot_program_group)

        z_texts = VGroup()
        for idx, token in enumerate(["z1", "z2", "z3"]):
            token_text = create_text(token, font_size=11, color=BLACK).move_to(tape_boxes[idx].get_center())
            z_texts.add(token_text)

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        tape_boxes[idx].animate.set_color(BLUE_A),
                        FadeIn(z_texts[idx], scale=0.9),
                    )
                    for idx in range(3)
                ],
                lag_ratio=0.28,
            ),
            run_time=1.4,
        )
        
        # Cue 21: show variable-length intermediate work
        self.wait_until(cue_start[21] + 0.2)
        more_text = create_text("...", font_size=12, color=BLACK).move_to(tape_boxes[3].get_center())
        extra_text = create_text("z4", font_size=11, color=BLACK).move_to(tape_boxes[4].get_center())
        self.play(
            tape_boxes[3].animate.set_color(BLUE_A),
            tape_boxes[4].animate.set_color(BLUE_A),
            FadeIn(more_text, scale=0.9),
            FadeIn(extra_text, scale=0.9),
            thought_box.animate.set_color(BLUE_B),
            thought_label.animate.set_color(BLACK),
            run_time=1.0,
        )
        
        # Cue 22: the outer process coordinates inner calls
        self.wait_until(cue_start[22] + 0.2)
        inner_call_1 = create_text("Generator call", font_size=8.8, color=BLUE_A).next_to(thought_box, UP, buff=0.12)
        inner_call_2 = create_text("Generator / tool call", font_size=8.8, color=BLUE_A).next_to(combine_box, UP, buff=0.12)
        self.play(
            answer_box.animate.set_color(YELLOW),
            answer_label.animate.set_color(BLACK),
            meta_frame.animate.set_stroke(color=YELLOW, width=2.4),
            FadeIn(inner_call_1, shift=UP * 0.08),
            FadeIn(inner_call_2, shift=UP * 0.08),
            run_time=1.0,
        )
        cot_program_group.add(z_texts, more_text, extra_text, inner_call_1, inner_call_2)

        # --- End of Scene ---
        self.wait_until(voiceover_end + 0.35)
        self.play(
            FadeOut(cot_program_group),
            FadeOut(sub_title),
            run_time=0.8
        )
        assert_all_scene_voiceovers_played(self)
