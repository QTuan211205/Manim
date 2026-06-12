import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_3_4_DURATIONS = {
    "sc34_001.mp3": 3.622313,
    "sc34_002.mp3": 3.065034,
    "sc34_003.mp3": 3.854512,
    "sc34_004.mp3": 5.990748,
    "sc34_005.mp3": 5.712109,
    "sc34_006.mp3": 7.291066,
    "sc34_007.mp3": 3.900952,
    "sc34_008.mp3": 4.597551,
    "sc34_009.mp3": 10.681179,
    "sc34_010.mp3": 4.643991,
    "sc34_011.mp3": 4.736871,
    "sc34_012.mp3": 10.681179,
    "sc34_013.mp3": 6.269388,
    "sc34_014.mp3": 14.442812,
    "sc34_015.mp3": 3.157914,
    "sc34_016.mp3": 7.616145,
    "sc34_017.mp3": 7.894785,
    "sc34_018.mp3": 12.027937,
    "sc34_019.mp3": 9.938141,
}
SCENE_3_4_VOICEOVERS = tuple(SCENE_3_4_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc34_*.mp3"))
    expected = sorted(SCENE_3_4_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 3.4 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_3_4_DURATIONS:
        raise KeyError(f"Unexpected Scene 3.4 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 3.4 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_3_4_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_3_4_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 3.4 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
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


class Scene3_4(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (filename, duration) in enumerate(SCENE_3_4_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        # --- Chapter Title (Cue 1) ---
        chapter_title = create_text("Chapter 3: High-Level Orchestrators", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 3.4: Refinement & Self-Correction", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub).move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)
        self.wait_until(cue_start[2])

        # --- Cue 2: Transform to sub_title ---
        sub_title = create_text("Refinement & Self-Correction", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=1.0)
        self.wait_until(cue_start[4])

        # --- Cue 4: Part 1 Title & Intro ---
        part1_title = create_text("1. Extrinsic Feedback Loop", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)
        
        intro_text = create_markup_text(
            "<b>Extrinsic Feedback:</b> The model receives objective feedback\n"
            "from the external environment (such as a compiler or code runner)\n"
            "and uses the error message to locate and fix the bug automatically.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)

        self.play(
            Write(part1_title),
            Write(intro_text),
            run_time=1.2
        )
        self.wait_until(cue_start[5])

        # --- Cue 5: LLM / Compiler boxes ---
        llm_box = RoundedRectangle(width=2.5, height=1.3, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        llm_box.move_to(LEFT * 4.2 + DOWN * 0.5)
        llm_lbl = create_text("LLM Generator", font_size=12, color=BLUE_A).move_to(llm_box.get_center())

        compiler_box = RoundedRectangle(width=2.5, height=1.3, color=RED_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        compiler_box.move_to(RIGHT * 4.2 + DOWN * 0.5)
        compiler_lbl = create_text("Rust Compiler", font_size=12, color=WHITE).move_to(compiler_box.get_center())

        arrow_to_comp = Arrow(start=llm_box.get_right() + UP * 0.25, end=compiler_box.get_left() + UP * 0.25, color=BLUE_B, stroke_width=1.5, buff=0.05)
        
        arrow_back = CurvedArrow(
            compiler_box.get_left() + DOWN * 0.25, 
            llm_box.get_right() + DOWN * 0.25, 
            angle=0.4, 
            color=RED_B, 
            stroke_width=1.5,
            tip_length=0.08
        )

        self.play(
            FadeIn(llm_box), Write(llm_lbl),
            FadeIn(compiler_box), Write(compiler_lbl),
            run_time=1.2
        )
        self.wait_until(cue_start[6])

        # --- Cue 6: Code compilation error & correction loop ---
        # 1. Draft 1 (with error)
        res_box = RoundedRectangle(width=2.2, height=0.7, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        res_box.move_to(LEFT * 0.8 + UP * 0.7)
        res_lbl = create_text("String memory region \"hello\"", font_size=8, color=WHITE).move_to(res_box.get_center())

        s_var = RoundedRectangle(width=0.8, height=0.4, color=GRAY_A, fill_color="#141517", fill_opacity=0.95, corner_radius=0.04)
        s_var.move_to(LEFT * 2.6 + UP * 1.2)
        s_lbl = create_text("Variable s", font_size=8, color=WHITE).move_to(s_var.get_center())

        s_ptr = Arrow(start=s_var.get_bottom(), end=res_box.get_left() + UP * 0.15, color=BLUE_A, stroke_width=2, max_tip_length_to_length_ratio=0.15, buff=0.05)

        code_1_box = RoundedRectangle(width=3.8, height=1.6, color=GRAY_D, fill_color="#141517", fill_opacity=0.95, corner_radius=0.06)
        code_1_box.move_to(RIGHT * 2.2 + UP * 0.7)
        code_1_lbl = create_markup_text(
            "<b>Draft 1 (error):</b>\n"
            "<span foreground='#FF8888'>fn main() {\n"
            "  let s = String::from(\"hello\");\n"
            "  let y = s; // moved s here\n"
            "  println!(\"{}\", s); // error: use of moved value s\n"
            "}</span>",
            font_size=9, line_spacing=1.1
        ).move_to(code_1_box.get_center())

        self.play(
            FadeIn(code_1_box),
            Write(code_1_lbl),
            FadeIn(res_box), Write(res_lbl),
            FadeIn(s_var), Write(s_lbl),
            Create(s_ptr),
            run_time=1.0
        )
        self.wait(1.0)

        # 2. Add y_var and move pointer
        y_var = RoundedRectangle(width=0.8, height=0.4, color=GRAY_A, fill_color="#141517", fill_opacity=0.95, corner_radius=0.04)
        y_var.move_to(LEFT * 2.6 + UP * 0.2)
        y_lbl = create_text("Variable y", font_size=8, color=WHITE).move_to(y_var.get_center())

        y_ptr = Arrow(start=y_var.get_right(), end=res_box.get_left() + DOWN * 0.15, color=GREEN_B, stroke_width=2, max_tip_length_to_length_ratio=0.15, buff=0.05)
        s_cross = get_crossmark(color=RED, stroke_width=3).scale(1.5).move_to(s_ptr.get_center())

        self.play(
            FadeIn(y_var), Write(y_lbl),
            Create(y_ptr),
            Create(s_cross),
            s_ptr.animate.set_color(RED),
            run_time=0.8
        )
        self.wait(0.5)

        # 3. Compiler detects error
        error_box = RoundedRectangle(width=4.4, height=0.9, color=RED, fill_color="#3c1414", fill_opacity=0.9, corner_radius=0.05)
        error_box.move_to(DOWN * 1.6)
        error_lbl = create_markup_text(
            "<b>Compiler Error (Rust Borrow Checker):</b>\n"
            "<span foreground='#FF5555'>error[E0382]: borrow of moved value: 's'</span>",
            font_size=8, line_spacing=1.1
        ).move_to(error_box.get_center())

        self.play(
            Create(arrow_to_comp),
            FadeOut(code_1_box, target_position=compiler_box.get_center()),
            FadeOut(code_1_lbl, target_position=compiler_box.get_center()),
            FadeOut(res_box), FadeOut(res_lbl),
            FadeOut(s_var), FadeOut(s_lbl), FadeOut(s_ptr), FadeOut(s_cross),
            FadeOut(y_var), FadeOut(y_lbl), FadeOut(y_ptr),
            compiler_box.animate.set_stroke(color=RED).set_fill(color="#551a1a", opacity=0.9),
            FadeIn(error_box), Write(error_lbl),
            run_time=1.0
        )
        self.wait(0.8)

        # 4. Loop back and fix
        self.play(
            Create(arrow_back),
            FadeOut(error_box, target_position=llm_box.get_center()),
            FadeOut(error_lbl, target_position=llm_box.get_center()),
            run_time=0.8
        )
        self.wait(0.2)

        code_2_box = RoundedRectangle(width=3.8, height=1.6, color=GREEN, fill_color="#141517", fill_opacity=0.95, corner_radius=0.06)
        code_2_box.move_to(RIGHT * 2.2 + UP * 0.7)
        code_2_lbl = create_markup_text(
            "<b>Draft 2 (fixed):</b>\n"
            "<span foreground='#88FF88'>fn main() {\n"
            "  let s = String::from(\"hello\");\n"
            "  let y = &amp;s; // borrow reference\n"
            "  println!(\"{}\", s); // compiled successfully!\n"
            "}</span>",
            font_size=9, line_spacing=1.1
        ).move_to(code_2_box.get_center())

        res_box_2 = RoundedRectangle(width=2.2, height=0.7, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        res_box_2.move_to(LEFT * 0.8 + UP * 0.7)
        res_lbl_2 = create_text("String memory region \"hello\"", font_size=8, color=WHITE).move_to(res_box_2.get_center())

        s_var_2 = RoundedRectangle(width=0.8, height=0.4, color=GRAY_A, fill_color="#141517", fill_opacity=0.95, corner_radius=0.04)
        s_var_2.move_to(LEFT * 2.6 + UP * 1.2)
        s_lbl_2 = create_text("Variable s", font_size=8, color=WHITE).move_to(s_var_2.get_center())

        s_ptr_2 = Arrow(start=s_var_2.get_bottom(), end=res_box_2.get_left() + UP * 0.15, color=BLUE_A, stroke_width=2, max_tip_length_to_length_ratio=0.15, buff=0.05)

        y_var_2 = RoundedRectangle(width=0.8, height=0.4, color=GRAY_A, fill_color="#141517", fill_opacity=0.95, corner_radius=0.04)
        y_var_2.move_to(LEFT * 2.6 + UP * 0.2)
        y_lbl_2 = create_text("Variable y", font_size=8, color=WHITE).move_to(y_var_2.get_center())

        y_borrow_ptr = Arrow(start=y_var_2.get_top(), end=s_var_2.get_bottom(), color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.15, buff=0.05)
        borrow_lbl = create_text("Borrow (&s)", font_size=7, color=GREEN).next_to(y_borrow_ptr, RIGHT, buff=0.1)

        success_icon = get_checkmark(color=GREEN, stroke_width=3).next_to(compiler_lbl, RIGHT, buff=0.15)

        self.play(
            FadeIn(code_2_box), Write(code_2_lbl),
            FadeIn(res_box_2), Write(res_lbl_2),
            FadeIn(s_var_2), Write(s_lbl_2),
            Create(s_ptr_2),
            FadeIn(y_var_2), Write(y_lbl_2),
            Create(y_borrow_ptr), Write(borrow_lbl),
            run_time=0.8
        )
        self.wait(0.5)

        self.play(
            FadeOut(code_2_box, target_position=compiler_box.get_center()),
            FadeOut(code_2_lbl, target_position=compiler_box.get_center()),
            FadeOut(res_box_2), FadeOut(res_lbl_2),
            FadeOut(s_var_2), FadeOut(s_lbl_2), FadeOut(s_ptr_2),
            FadeOut(y_var_2), FadeOut(y_lbl_2), FadeOut(y_borrow_ptr), FadeOut(borrow_lbl),
            compiler_box.animate.set_stroke(color=GREEN).set_fill(color="#143c14", opacity=0.9),
            FadeIn(success_icon),
            run_time=1.0
        )
        self.wait_until(cue_start[7])

        # --- Cue 7: Part 2 Title & Intro ---
        self.play(
            FadeOut(intro_text),
            FadeOut(llm_box), FadeOut(llm_lbl),
            FadeOut(compiler_box), FadeOut(compiler_lbl), FadeOut(success_icon),
            FadeOut(arrow_to_comp), FadeOut(arrow_back),
            FadeOut(part1_title),
            run_time=0.8
        )
        
        part2_title = create_text("2. Prompted Intrinsic Feedback & Noisy Feedback Traps", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)

        intro_part2 = create_markup_text(
            "<b>Intrinsic Feedback:</b> Ask the model to find and fix its own errors.\n"
            "If prompting alone is used for logical reasoning, the model can suffer\n"
            "<b>Feedback Hallucination:</b> turning a correct answer into a wrong one.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)

        self.play(
            Write(part2_title),
            Write(intro_part2),
            run_time=1.2
        )
        self.wait_until(cue_start[8])

        # --- Cue 8: Re-prompting example (Prompt & Draft) ---
        sim_llm_box = RoundedRectangle(width=1.6, height=0.6, color=BLUE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        sim_llm_box.move_to(LEFT * 4.6 + UP * 0.9)
        sim_llm_lbl = create_text("LLM Generator", font_size=10, color=BLUE_A).move_to(sim_llm_box.get_center())

        prompt_box = RoundedRectangle(width=4.0, height=0.5, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        prompt_box.move_to(LEFT * 3.4 + UP * 0.1)
        prompt_lbl = create_text("Prompt: Solve 17 + 25 = ?", font_size=9, color=YELLOW).move_to(prompt_box.get_center())

        ans1_box = RoundedRectangle(width=4.0, height=0.5, color=GREEN, fill_color="#143c14", fill_opacity=0.8, corner_radius=0.05)
        ans1_box.next_to(prompt_box, DOWN, buff=0.15)
        ans1_lbl = create_markup_text("<b>LLM (Draft):</b> Answer is <span foreground='#88FF88'>42</span> (Correct)", font_size=9).move_to(ans1_box.get_center())

        self.play(
            FadeIn(sim_llm_box), Write(sim_llm_lbl),
            FadeIn(prompt_box), Write(prompt_lbl),
            FadeIn(ans1_box), Write(ans1_lbl),
            run_time=1.0
        )
        self.wait_until(cue_start[9])

        # --- Cue 9: Self-critique & revision (wrong correction) ---
        critique_box = RoundedRectangle(width=4.0, height=0.5, color=BLUE_C, fill_color="#141c2b", fill_opacity=0.8, corner_radius=0.05)
        critique_box.next_to(ans1_box, DOWN, buff=0.15)
        critique_lbl = create_text("Self-evaluation prompt: Is the answer above correct?", font_size=9, color=WHITE).move_to(critique_box.get_center())

        halluc_box = RoundedRectangle(width=4.0, height=0.5, color=RED, fill_color="#3c1414", fill_opacity=0.8, corner_radius=0.05)
        halluc_box.next_to(critique_box, DOWN, buff=0.15)
        halluc_lbl = create_markup_text("<b>LLM (Critique):</b> Incorrect, 17+25 should be <span foreground='#FF8888'>32</span>", font_size=8).move_to(halluc_box.get_center())

        ans2_box = RoundedRectangle(width=4.0, height=0.5, color=RED, fill_color="#3c1414", fill_opacity=0.8, corner_radius=0.05)
        ans2_box.next_to(halluc_box, DOWN, buff=0.15)
        ans2_lbl = create_markup_text("<b>LLM (Final):</b> Revise it to <span foreground='#FF8888'>32</span> (Completely wrong!)", font_size=9).move_to(ans2_box.get_center())

        self.play(FadeIn(critique_box), Write(critique_lbl), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(halluc_box), Write(halluc_lbl), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(ans2_box), Write(ans2_lbl), run_time=0.8)
        self.wait_until(cue_start[10])

        # --- Cue 10: Confusion Matrix ---
        matrix_center = RIGHT * 3.6 + DOWN * 0.4
        
        matrix_title = create_text("Self-correction Matrix (Confusion Matrix)", font_size=10, color=GOLD_B)
        matrix_title.move_to(matrix_center + UP * 2.1)

        lbl_init = create_text("Initial draft", font_size=9, color=BLUE_A)
        lbl_init.move_to(matrix_center + LEFT * 1.9 + UP * 0.7)
        
        lbl_init_correct = create_text("Correct", font_size=9, color=WHITE)
        lbl_init_correct.move_to(matrix_center + LEFT * 1.1 + UP * 0.45)
        lbl_init_incorrect = create_text("Incorrect", font_size=9, color=WHITE)
        lbl_init_incorrect.move_to(matrix_center + LEFT * 1.1 + DOWN * 0.45)

        lbl_fin = create_text("After Self-Correction", font_size=9, color=BLUE_A)
        lbl_fin.move_to(matrix_center + UP * 1.6)

        lbl_fin_correct = create_text("Correct", font_size=9, color=WHITE)
        lbl_fin_correct.move_to(matrix_center + LEFT * 0.45 + UP * 1.1)
        lbl_fin_incorrect = create_text("Incorrect", font_size=9, color=WHITE)
        lbl_fin_incorrect.move_to(matrix_center + RIGHT * 0.45 + UP * 1.1)

        cell_size = 0.9
        cells = VGroup()
        cell_texts = VGroup()

        cell_data = [
            ("85%", GREEN_E, 0.6, LEFT * 0.45 + UP * 0.45),
            ("15%", RED_E, 0.6, RIGHT * 0.45 + UP * 0.45),
            ("35%", GREEN_E, 0.6, LEFT * 0.45 + DOWN * 0.45),
            ("65%", RED_E, 0.6, RIGHT * 0.45 + DOWN * 0.45)
        ]

        for percent_str, color, opacity, pos_offset in cell_data:
            cell = Square(side_length=cell_size, color=GRAY_D, stroke_width=1, fill_color=color, fill_opacity=opacity)
            cell.move_to(matrix_center + pos_offset)
            txt = create_text(percent_str, font_size=10, color=WHITE).move_to(cell.get_center())
            cells.add(cell)
            cell_texts.add(txt)

        highlight_halluc = RoundedRectangle(width=0.92, height=0.92, color=RED, stroke_width=3, fill_opacity=0).move_to(cells[1].get_center())
        halluc_note = create_markup_text(
            "<span foreground='#FF5555'><b>Feedback Hallucination (15%)</b></span>\n"
            "The LLM destroys a correct answer on its own.",
            font_size=8, line_spacing=1.2
        ).next_to(cells, DOWN, buff=0.4)


        self.play(
            Write(matrix_title),
            Write(lbl_init), Write(lbl_init_correct), Write(lbl_init_incorrect),
            Write(lbl_fin), Write(lbl_fin_correct), Write(lbl_fin_incorrect),
            Create(cells),
            run_time=1.0
        )

        # Quick Dot animation
        import random
        random.seed(42)
        dots = VGroup()
        dot_anims = []

        for i in range(20):
            dot = Dot(color=GREEN, radius=0.04)
            dot.move_to(matrix_center + UP * 2.3 + LEFT * 0.45 + np.array([random.uniform(-0.15, 0.15), random.uniform(-0.1, 0.1), 0]))
            dots.add(dot)
            if i < 17:
                target_pos = cells[0].get_center() + np.array([random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0])
                dot_anims.append(dot.animate(run_time=0.6).move_to(target_pos))
            else:
                target_pos = cells[1].get_center() + np.array([random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0])
                dot_anims.append(dot.animate(run_time=0.6).move_to(target_pos).set_color(RED))

        for i in range(20):
            dot = Dot(color=RED, radius=0.04)
            dot.move_to(matrix_center + UP * 2.3 + RIGHT * 0.45 + np.array([random.uniform(-0.15, 0.15), random.uniform(-0.1, 0.1), 0]))
            dots.add(dot)
            if i < 7:
                target_pos = cells[2].get_center() + np.array([random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0])
                dot_anims.append(dot.animate(run_time=0.6).move_to(target_pos).set_color(GREEN))
            else:
                target_pos = cells[3].get_center() + np.array([random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0])
                dot_anims.append(dot.animate(run_time=0.6).move_to(target_pos))

        self.play(FadeIn(dots), run_time=0.3)
        self.play(*dot_anims, run_time=0.8)
        self.play(
            Write(cell_texts),
            Create(highlight_halluc),
            Write(halluc_note),
            run_time=0.8
        )

        warning_lbl = create_markup_text(
            "<span foreground='#FF3333'><b>INTRINSIC FEEDBACK IS TOO NOISY</b></span>",
            font_size=11
        ).move_to(DOWN * 3.2)
        self.play(FadeIn(warning_lbl, shift=UP * 0.2), run_time=0.5)

        self.wait_until(cue_start[11])

        # --- Cue 11: Part 3 Title & Intro ---
        self.play(
            FadeOut(intro_part2),
            FadeOut(sim_llm_box), FadeOut(sim_llm_lbl),
            FadeOut(prompt_box), FadeOut(prompt_lbl),
            FadeOut(ans1_box), FadeOut(ans1_lbl),
            FadeOut(critique_box), FadeOut(critique_lbl),
            FadeOut(halluc_box), FadeOut(halluc_lbl),
            FadeOut(ans2_box), FadeOut(ans2_lbl),
            FadeOut(matrix_title), FadeOut(lbl_init), FadeOut(lbl_init_correct), FadeOut(lbl_init_incorrect),
            FadeOut(lbl_fin), FadeOut(lbl_fin_correct), FadeOut(lbl_fin_incorrect),
            FadeOut(cells), FadeOut(cell_texts), FadeOut(dots),
            FadeOut(highlight_halluc), FadeOut(halluc_note),
            FadeOut(warning_lbl),
            FadeOut(part2_title),
            run_time=0.8
        )

        part3_title = create_text("3. Training a Corrector & the SCoRe Algorithm", font_size=13, color=BLUE_A)
        part3_title.next_to(sub_title, DOWN, buff=0.3)

        intro_part3 = create_markup_text(
            "To handle noise, we can <b>fine-tune</b> the model to self-correct.\n"
            "However, ordinary reinforcement learning (RL) can lead to behavior collapse.\n"
            "The **SCoRe** algorithm (Google DeepMind) makes training stable and effective.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)

        self.play(
            Write(part3_title),
            Write(intro_part3),
            run_time=1.2
        )
        self.wait_until(cue_start[12])

        # --- Cue 12: Corrector Formula ---
        formula_box = RoundedRectangle(width=8.2, height=1.0, color=BLUE_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        formula_box.move_to(UP * 0.9)
        formula_txt = create_markup_text(
            "Refinement correction policy:  <span foreground='#00FF7F'><i>p</i><sub>θ</sub>( <span foreground='#FFFF00'>better</span> | <span foreground='#FF7F7F'>bad</span> )</span>",
            font_size=13
        ).move_to(formula_box.get_center())

        self.play(
            FadeIn(formula_box),
            Write(formula_txt),
            run_time=1.2
        )
        self.wait_until(cue_start[13])

        # --- Cue 13: SCoRe training curve ---
        self.play(FadeOut(formula_box), FadeOut(formula_txt), run_time=0.5)

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.0, 0.2],
            x_length=7.5,
            y_length=2.5,
            axis_config={"color": GRAY_C, "stroke_width": 2},
            tips=False
        ).move_to(DOWN * 1.3)

        x_lbl = create_text("RL training step", font_size=9, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.12)
        y_lbl = create_text("Self-correction performance", font_size=9, color=GRAY_A).next_to(axes.y_axis.get_top(), LEFT, buff=0.15)

        origin_pt = axes.c2p(0, 0)
        top_right_pt = axes.c2p(10, 0.8)
        
        safe_zone = Rectangle(
            width=top_right_pt[0] - origin_pt[0],
            height=top_right_pt[1] - origin_pt[1],
            stroke_width=0,
            fill_color=GREEN_E,
            fill_opacity=0.15
        ).move_to(axes.c2p(5, 0.4))

        kl_limit_line = DashedLine(
            start=axes.c2p(0, 0.8),
            end=axes.c2p(10, 0.8),
            color=GREEN,
            stroke_width=1.5
        )
        kl_limit_lbl = create_text("KL safe region (KL Regularization)", font_size=8, color=GREEN_B).move_to(axes.c2p(3.2, 0.85))

        self.play(
            Create(axes), Write(x_lbl), Write(y_lbl),
            FadeIn(safe_zone), Create(kl_limit_line), Write(kl_limit_lbl),
            run_time=1.0
        )

        standard_rl_points = [
            axes.c2p(0, 0.3),
            axes.c2p(1.5, 0.52),
            axes.c2p(3, 0.65),
            axes.c2p(4.5, 0.45),
            axes.c2p(6, 0.15),
            axes.c2p(8, 0.05),
            axes.c2p(10, 0.02)
        ]
        standard_rl_curve = VMobject(color=RED, stroke_width=3.5).set_points_smoothly(standard_rl_points)

        std_rl_lbl = create_markup_text(
            "<span foreground='#FF5555'><b>Standard RL</b></span>\n(Behavior Collapse)",
            font_size=9
        ).move_to(axes.c2p(5.2, 0.45))

        std_rl_cross = get_crossmark(color=RED, stroke_width=3.0).scale(1.2).move_to(axes.c2p(6.5, 0.12))
        collapse_warning = create_text("Behavior Collapse", font_size=8, color=RED).next_to(std_rl_cross, RIGHT, buff=0.1)

        score_points = [
            axes.c2p(0, 0.3),
            axes.c2p(1.5, 0.46),
            axes.c2p(3, 0.58),
            axes.c2p(5.0, 0.68),
            axes.c2p(7.0, 0.73),
            axes.c2p(9.0, 0.75),
            axes.c2p(10, 0.75)
        ]
        score_curve = VMobject(color=GREEN, stroke_width=3.5).set_points_smoothly(score_points)

        score_lbl = create_markup_text(
            "<span foreground='#00FF7F'><b>SCoRe solution</b></span>\n(Stable &amp; optimized)",
            font_size=9
        ).move_to(axes.c2p(6.5, 0.9))
        score_check = get_checkmark(color=GREEN, stroke_width=3.0).scale(1.2).next_to(score_lbl, LEFT, buff=0.1)

        self.play(
            Create(standard_rl_curve), Write(std_rl_lbl), Create(std_rl_cross), Write(collapse_warning),
            Create(score_curve), Write(score_lbl), Create(score_check),
            run_time=1.8
        )

        self.wait_until(cue_start[14])

        # --- Cue 14: Summary Table ---
        self.play(
            FadeOut(intro_part3),
            FadeOut(axes), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(safe_zone), FadeOut(kl_limit_line), FadeOut(kl_limit_lbl),
            FadeOut(standard_rl_curve), FadeOut(std_rl_lbl), FadeOut(std_rl_cross), FadeOut(collapse_warning),
            FadeOut(score_curve), FadeOut(score_lbl), FadeOut(score_check),
            FadeOut(part3_title),
            run_time=0.8
        )

        recap_title = create_text("Summary: Refinement & Self-Correction Mechanisms", font_size=13, color=YELLOW)
        recap_title.next_to(sub_title, DOWN, buff=0.3)

        comparison_table = VGroup()
        headers = ["Method", "Feedback mechanism", "Properties / traps"]
        header_colors = [BLUE_A, WHITE, RED]
        
        header_group = VGroup()
        for idx, h_text in enumerate(headers):
            cell = RoundedRectangle(width=3.2, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            cell.move_to(LEFT * (3.4 * (1 - idx)) + UP * 1.0)
            lbl = create_text(h_text, font_size=11, color=header_colors[idx]).move_to(cell.get_center())
            header_group.add(VGroup(cell, lbl))
        comparison_table.add(header_group)

        table_rows = [
            ("Extrinsic feedback", "From compiler / external environment", "High accuracy, very effective"),
            ("Intrinsic - prompted", "Model re-prompts itself to self-correct", "Feedback hallucination, noisy"),
            ("Intrinsic - trained", "Self-tuning RL (SCoRe)", "KL regularization helps prevent behavior collapse")
        ]

        row_y_coords = [0.2, -0.6, -1.4]
        for r_idx, row_data in enumerate(table_rows):
            row_group = VGroup()
            for c_idx, cell_text in enumerate(row_data):
                cell = RoundedRectangle(width=3.2, height=0.6, color=GRAY_E, fill_color="#121315", fill_opacity=0.8, corner_radius=0.04)
                cell.move_to(LEFT * (3.4 * (1 - c_idx)) + UP * row_y_coords[r_idx])
                t_color = RED if c_idx == 2 else (GREEN if c_idx == 1 else WHITE)
                lbl = create_text(cell_text, font_size=9, color=t_color).move_to(cell.get_center())
                row_group.add(VGroup(cell, lbl))
            comparison_table.add(row_group)

        self.play(
            Write(recap_title),
            FadeIn(comparison_table),
            run_time=1.5
        )
        self.wait_until(cue_start[15])

        # --- Cue 15: Feedback Clarification Intro ---
        self.play(
            FadeOut(comparison_table),
            FadeOut(recap_title),
            run_time=0.8
        )

        clarify_title = create_text("Feedback: Extrinsic vs. Intrinsic", font_size=15, color=YELLOW)
        clarify_title.next_to(sub_title, DOWN, buff=0.3)

        self.play(Write(clarify_title), run_time=0.8)
        self.wait_until(cue_start[16])

        # --- Cue 16: Extrinsic Feedback Clarification ---
        ext_clarify_box = RoundedRectangle(width=5.5, height=2.4, color=BLUE_B, fill_color="#0b1324", fill_opacity=0.9, corner_radius=0.08)
        ext_clarify_box.move_to(LEFT * 3.1 + DOWN * 0.8)
        ext_clarify_title = create_text("Extrinsic Feedback", font_size=12, color=BLUE_A).next_to(ext_clarify_box.get_top(), DOWN, buff=0.15)
        ext_clarify_text = create_markup_text(
            "• Provides new outside information\n"
            "• Not already contained within model weights\n"
            "• Verifier / compiler can localize errors\n"
            "• Strongly anchors the generation",
            font_size=10, line_spacing=1.3
        ).next_to(ext_clarify_title, DOWN, buff=0.15).align_to(ext_clarify_box, LEFT).shift(RIGHT * 0.3)
        ext_group = VGroup(ext_clarify_box, ext_clarify_title, ext_clarify_text)

        self.play(FadeIn(ext_group, shift=UP * 0.15), run_time=1.0)
        self.wait_until(cue_start[17])

        # --- Cue 17: Intrinsic Feedback Clarification ---
        int_clarify_box = RoundedRectangle(width=5.5, height=2.4, color=RED_C, fill_color="#1f0c0c", fill_opacity=0.9, corner_radius=0.08)
        int_clarify_box.move_to(RIGHT * 3.1 + DOWN * 0.8)
        int_clarify_title = create_text("Intrinsic Feedback", font_size=12, color=RED_B).next_to(int_clarify_box.get_top(), DOWN, buff=0.15)
        int_clarify_text = create_markup_text(
            "• Relies entirely on internal knowledge\n"
            "• Risk of creator and judge being identical\n"
            "• Often fails to identify subtle logical bugs\n"
            "• Prone to feedback hallucination",
            font_size=10, line_spacing=1.3
        ).next_to(int_clarify_title, DOWN, buff=0.15).align_to(int_clarify_box, LEFT).shift(RIGHT * 0.3)
        int_group = VGroup(int_clarify_box, int_clarify_title, int_clarify_text)

        self.play(FadeIn(int_group, shift=UP * 0.15), run_time=1.0)
        self.wait_until(cue_start[18])

        # --- Cue 18: Toy Example "TAYLORSWIFT" ---
        self.play(
            FadeOut(ext_group), FadeOut(int_group), FadeOut(clarify_title),
            run_time=0.8
        )

        toy_title = create_text("Toy Example: Generate the string \"TAYLORSWIFT\"", font_size=14, color=YELLOW).to_edge(UP, buff=1.0)
        self.play(FadeIn(toy_title), run_time=0.8)

        draft_letters = ["T", "A", "Y", "L", "O", "R", "S", "W", "I", "P", "T"]
        letter_boxes = VGroup()
        for idx, char in enumerate(draft_letters):
            color = RED if idx == 9 else BLUE
            box = RoundedRectangle(width=0.6, height=0.6, color=color, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
            box.move_to(LEFT * 3.5 + idx * 0.7 * RIGHT + UP * 0.2)
            lbl = create_text(char, font_size=12, color=WHITE).move_to(box.get_center())
            letter_boxes.add(VGroup(box, lbl))

        self.play(FadeIn(letter_boxes, lag_ratio=0.08), run_time=1.2)

        feedback_box = RoundedRectangle(width=6.0, height=0.8, color=RED, fill_color="#2b1414", fill_opacity=0.9, corner_radius=0.06)
        feedback_box.move_to(DOWN * 0.8)
        feedback_lbl = create_markup_text(
            "<b>Feedback:</b> The 10th character <span foreground='#FF5555'>'P'</span> is wrong. Fix it.",
            font_size=10, color=WHITE
        ).move_to(feedback_box.get_center())

        arrow_feedback = Arrow(start=feedback_box.get_top(), end=letter_boxes[9].get_bottom(), color=RED, stroke_width=2)

        self.play(
            FadeIn(feedback_box), Write(feedback_lbl), Create(arrow_feedback),
            run_time=1.0
        )
        self.wait_until(cue_start[19])

        # --- Cue 19: Fix incorrect letter ---
        new_lbl = create_text("F", font_size=12, color=WHITE).move_to(letter_boxes[9][0].get_center())

        self.play(
            letter_boxes[9][0].animate.set_color(GREEN).set_fill(color="#143c14", opacity=0.9),
            FadeOut(letter_boxes[9][1]),
            FadeIn(new_lbl),
            FadeOut(arrow_feedback),
            FadeOut(feedback_box),
            FadeOut(feedback_lbl),
            run_time=1.0
        )
        letter_boxes[9].remove(letter_boxes[9][1])
        letter_boxes[9].add(new_lbl)

        final_lbl = create_markup_text(
            "Final result: <b>TAYLORSWIFT</b>", font_size=12, color=GREEN
        ).move_to(DOWN * 0.8)
        self.play(Write(final_lbl), run_time=0.8)

        self.wait_until(voiceover_end + 0.25)
        
        self.play(
            FadeOut(letter_boxes),
            FadeOut(final_lbl),
            FadeOut(toy_title),
            FadeOut(sub_title),
            run_time=1.0
        )

        assert_all_scene_voiceovers_played(self)
