import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_3_5_DURATIONS = {
    "sc35_001.mp3": 5.897868,
    "sc35_002.mp3": 3.436553,
    "sc35_003.mp3": 3.622313,
    "sc35_004.mp3": 11.517098,
    "sc35_005.mp3": 10.30966,
    "sc35_006.mp3": 6.919546,
    "sc35_007.mp3": 2.739955,
    "sc35_008.mp3": 3.808073,
    "sc35_009.mp3": 3.482993,
    "sc35_010.mp3": 7.523265,
    "sc35_011.mp3": 5.572789,
    "sc35_012.mp3": 4.179592,
    "sc35_013.mp3": 7.755465,
    "sc35_014.mp3": 8.777143,
    "sc35_015.mp3": 8.823583,
    "sc35_016.mp3": 2.647075,
    "sc35_017.mp3": 9.148662,
    "sc35_018.mp3": 6.780227,
}
SCENE_3_5_VOICEOVERS = tuple(SCENE_3_5_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc35_*.mp3"))
    expected = sorted(SCENE_3_5_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 3.5 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_3_5_DURATIONS:
        raise KeyError(f"Unexpected Scene 3.5 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 3.5 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_3_5_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_3_5_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 3.5 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
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


def create_slider(label, value_label, start_text, end_text, dot_ratio=0.5, width=4.0):
    slider = VGroup()
    line = Line(LEFT * (width / 2), RIGHT * (width / 2), color=GRAY_D, stroke_width=4)
    dot_pos = line.get_left() + dot_ratio * (line.get_right() - line.get_left())
    dot = Dot(color=BLUE_A, radius=0.12).move_to(dot_pos)
    lbl = create_text(label, font_size=11, color=WHITE).next_to(line, LEFT, buff=0.3)
    val = create_text(value_label, font_size=10, color=YELLOW).next_to(line, RIGHT, buff=0.3)
    st = create_text(start_text, font_size=8, color=GRAY_B).next_to(line.get_left(), DOWN, buff=0.1)
    en = create_text(end_text, font_size=8, color=GRAY_B).next_to(line.get_right(), DOWN, buff=0.1)
    slider.add(line, dot, lbl, val, st, en)
    return slider


class Scene3_5(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (filename, duration) in enumerate(SCENE_3_5_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        # --- Chapter Title (Cue 1) ---
        chapter_title = create_text("Chapter 3: High-Level Orchestrators", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 3.5: Scaling Meta-Generators & Compute Allocation", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub).move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)
        self.wait_until(cue_start[2])

        # --- Cue 2: Transform to sub_title ---
        sub_title = create_text("Scaling Meta-Generators & Compute Allocation", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=1.0)
        self.wait_until(cue_start[3])

        # --- Cue 3: Cost description text ---
        intro_text = create_markup_text(
            "<b>Scaling meta-generators:</b> How should we allocate test-time compute budget?\n"
            "We choose inference strategies based on task performance and cost.\n"
            "Cost is a function of the <b>model size</b> and the <b>number of generated tokens</b>.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 1.5)

        self.play(Write(intro_text), run_time=1.5)
        self.wait_until(cue_start[4])

        # --- Cue 4: Compute-Optimal Inference Problem ---
        self.play(FadeOut(intro_text), run_time=0.8)

        part1_title = create_text("1. Compute-Optimal Inference Problem", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)

        objective_box = RoundedRectangle(width=8.5, height=1.6, color=BLUE_B, fill_color="#0b1324", fill_opacity=0.9, corner_radius=0.1)
        objective_box.move_to(UP * 0.8)
        objective_lbl = create_text("Inference optimization objective", font_size=11, color=BLUE_A).next_to(objective_box.get_top(), DOWN, buff=0.15)
        
        objective_formula = create_markup_text(
            "argmin<sub>N, T, S</sub>  Error(N, T, S)    s.t.  Cost(N, T, S) = C",
            font_size=12, color=YELLOW
        ).move_to(objective_box.get_center() + DOWN * 0.1)
        objective_group = VGroup(objective_box, objective_lbl, objective_formula)

        self.play(
            Write(part1_title),
            FadeIn(objective_group, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait_until(cue_start[5])

        # --- Cue 5: Sliders Dashboard (N, T, S knobs) ---
        sliders_box = RoundedRectangle(width=8.5, height=2.4, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.08)
        sliders_box.move_to(DOWN * 1.6)
        sliders_title = create_text("Test-time Compute Allocation (Cost = C)", font_size=10, color=GOLD_B).next_to(sliders_box.get_top(), DOWN, buff=0.12)

        # 3 sliders
        slider_n = create_slider("Model Size (N)", "7B Params", "Smaller", "Larger", dot_ratio=0.3, width=3.5)
        slider_t = create_slider("Gen Length (T)", "512 Tokens", "Shorter", "Longer", dot_ratio=0.6, width=3.5)
        slider_s = create_slider("Strategy (S)", "Tree Search", "Greedy", "Advanced", dot_ratio=0.8, width=3.5)

        slider_n.move_to(DOWN * 1.2 + LEFT * 2.1)
        slider_t.move_to(DOWN * 1.2 + RIGHT * 2.1)
        slider_s.move_to(DOWN * 2.2 + LEFT * 0.0)

        sliders_group = VGroup(sliders_box, sliders_title, slider_n, slider_t, slider_s)

        self.play(FadeIn(sliders_group, shift=UP * 0.15), run_time=1.2)
        self.wait_until(cue_start[6])

        # --- Cue 6: Trade-off Title ---
        self.play(
            FadeOut(objective_group),
            FadeOut(sliders_group),
            FadeOut(part1_title),
            run_time=0.8
        )

        part2_title = create_text("2. Model Size vs. Inference Generations Trade-off", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)

        self.play(Write(part2_title), run_time=0.8)
        self.wait_until(cue_start[7])

        # --- Cue 7: Plotting the Pareto Frontier ---
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.0, 0.2],
            x_length=6.0,
            y_length=3.5,
            axis_config={"color": GRAY_C, "stroke_width": 2},
            tips=False
        ).move_to(LEFT * 3.3 + DOWN * 0.4)

        x_lbl = create_text("Compute Cost (FLOPs)", font_size=8, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.12)
        y_lbl = create_text("Performance (Accuracy)", font_size=8, color=GRAY_A).next_to(axes.y_axis.get_top(), LEFT, buff=0.15)

        # Draw the curve
        frontier_curve = axes.plot(
            lambda x: 0.95 - 0.78 / (x + 1),
            x_range=[0.0, 10.0],
            color=GREEN,
            stroke_width=4
        )
        frontier_lbl = create_text("Compute-Optimal Frontier", font_size=8, color=GREEN_B).move_to(axes.c2p(7.0, 0.92))

        self.play(
            Create(axes), Write(x_lbl), Write(y_lbl),
            Create(frontier_curve), Write(frontier_lbl),
            run_time=1.5
        )

        # Question on the right
        right_panel = VGroup()
        q1_txt = create_markup_text(
            "<b>Question 1:</b>\n"
            "Small model + more generations\n"
            "vs. Large model + fewer generations?",
            font_size=10, color=WHITE, line_spacing=1.3
        ).move_to(RIGHT * 3.3 + UP * 0.8)
        
        a1_txt = create_markup_text(
            "<span foreground='#00FF7F'><b>Answer:</b> Smaller models can be\n"
            "compute-optimal in some settings\n"
            "[Wu et al., 2024b]</span>",
            font_size=10, line_spacing=1.3
        ).next_to(q1_txt, DOWN, buff=0.25).align_to(q1_txt, LEFT)

        self.play(Write(q1_txt), run_time=0.8)
        self.wait(0.5)
        self.play(Write(a1_txt), run_time=1.0)
        self.wait_until(cue_start[8])

        # --- Cue 8: Question 2 (Which strategy is compute-optimal) ---
        q2_txt = create_markup_text(
            "<b>Question 2:</b>\n"
            "Which meta-generation strategy\n"
            "is compute-optimal?",
            font_size=10, color=WHITE, line_spacing=1.3
        ).next_to(a1_txt, DOWN, buff=0.25).align_to(a1_txt, LEFT)

        self.play(Write(q2_txt), run_time=0.8)
        self.wait_until(cue_start[9])

        # --- Cue 9: Answer 2 (Tree search/Rebase) ---
        a2_txt = create_markup_text(
            "<span foreground='#00FF7F'><b>Answer:</b> Tree search (Rebase)\n"
            "can be compute-optimal\n"
            "[Wu et al., 2024b]</span>",
            font_size=10, line_spacing=1.3
        ).next_to(q2_txt, DOWN, buff=0.2).align_to(q2_txt, LEFT)

        # Highlight a point on the plot
        rebase_point = Dot(color=YELLOW, radius=0.12).move_to(axes.c2p(4.0, 0.79))
        rebase_lbl = create_text("Rebase (Tree Search)", font_size=8, color=YELLOW).next_to(rebase_point, UP, buff=0.15)

        self.play(
            Write(a2_txt),
            Create(rebase_point), Write(rebase_lbl),
            run_time=1.2
        )
        self.wait_until(cue_start[10])

        # --- Cue 10: Recap slide 162-163 (Cards creation) ---
        self.play(
            FadeOut(axes), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(frontier_curve), FadeOut(frontier_lbl),
            FadeOut(q1_txt), FadeOut(a1_txt), FadeOut(q2_txt), FadeOut(a2_txt),
            FadeOut(rebase_point), FadeOut(rebase_lbl),
            FadeOut(part2_title),
            run_time=0.8
        )

        part3_title = create_text("3. Recap of Meta-Generation Compute Scaling", font_size=13, color=BLUE_A)
        part3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part3_title), run_time=0.8)

        card1_box = RoundedRectangle(width=5.5, height=1.1, color=BLUE_B, fill_color="#0b1324", fill_opacity=0.9, corner_radius=0.06)
        card1_box.move_to(LEFT * 3.1 + UP * 0.8)
        card1_title = create_text("Compute Scaling", font_size=11, color=BLUE_A).next_to(card1_box.get_top(), DOWN, buff=0.1)
        card1_text = create_text("Performance improves with compute, but depends on model/strategy.", font_size=9, color=WHITE).next_to(card1_title, DOWN, buff=0.1)
        card1 = VGroup(card1_box, card1_title, card1_text)

        self.play(FadeIn(card1, shift=UP * 0.15), run_time=1.0)
        self.wait_until(cue_start[11])

        # --- Cue 11: Card 2 ---
        card2_box = RoundedRectangle(width=5.5, height=1.1, color=GREEN_B, fill_color="#0c1f13", fill_opacity=0.9, corner_radius=0.06)
        card2_box.move_to(RIGHT * 3.1 + UP * 0.8)
        card2_title = create_text("Model Trade-off", font_size=11, color=GREEN_A).next_to(card2_box.get_top(), DOWN, buff=0.1)
        card2_text = create_text("Smaller models sometimes perform better under tight cost budgets.", font_size=9, color=WHITE).next_to(card2_title, DOWN, buff=0.1)
        card2 = VGroup(card2_box, card2_title, card2_text)

        self.play(FadeIn(card2, shift=UP * 0.15), run_time=1.0)
        self.wait_until(cue_start[12])

        # --- Cue 12: Card 3 ---
        card3_box = RoundedRectangle(width=5.5, height=1.1, color=GOLD_B, fill_color="#24190b", fill_opacity=0.9, corner_radius=0.06)
        card3_box.move_to(LEFT * 3.1 + DOWN * 0.8)
        card3_title = create_text("Universal Strategy", font_size=11, color=GOLD_A).next_to(card3_box.get_top(), DOWN, buff=0.1)
        card3_text = create_text("Long-term goal: design universally optimal strategies.", font_size=9, color=WHITE).next_to(card3_title, DOWN, buff=0.1)
        card3 = VGroup(card3_box, card3_title, card3_text)

        self.play(FadeIn(card3, shift=UP * 0.15), run_time=1.0)
        self.wait_until(cue_start[13])

        # --- Cue 13: Card 4 ---
        card4_box = RoundedRectangle(width=5.5, height=1.1, color=PURPLE_B, fill_color="#1d0b24", fill_opacity=0.9, corner_radius=0.06)
        card4_box.move_to(RIGHT * 3.1 + DOWN * 0.8)
        card4_title = create_text("System Bridge", font_size=11, color=PURPLE_A).next_to(card4_box.get_top(), DOWN, buff=0.1)
        card4_text = create_text("Next big question: how to generate tokens quickly and efficiently?", font_size=9, color=WHITE).next_to(card4_title, DOWN, buff=0.1)
        card4 = VGroup(card4_box, card4_title, card4_text)

        self.play(FadeIn(card4, shift=UP * 0.15), run_time=1.0)
        self.wait_until(cue_start[14])

        # --- Cue 14: Compute-Optimal Frontier Details (Dominance) ---
        self.play(
            FadeOut(card1), FadeOut(card2), FadeOut(card3), FadeOut(card4),
            FadeOut(part3_title),
            run_time=0.8
        )

        part4_title = create_text("4. Defining the Compute-Optimal Frontier", font_size=13, color=BLUE_A)
        part4_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part4_title), run_time=0.8)

        axes_2 = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.0, 0.2],
            x_length=6.0,
            y_length=3.5,
            axis_config={"color": GRAY_C, "stroke_width": 2},
            tips=False
        ).move_to(LEFT * 3.3 + DOWN * 0.4)

        x_lbl_2 = create_text("Compute Cost (FLOPs)", font_size=8, color=GRAY_A).next_to(axes_2.x_axis, DOWN, buff=0.12)
        y_lbl_2 = create_text("Performance (Accuracy)", font_size=8, color=GRAY_A).next_to(axes_2.y_axis.get_top(), LEFT, buff=0.15)

        # Plot curve
        curve_2 = axes_2.plot(
            lambda x: 0.95 - 0.78 / (x + 1),
            x_range=[0.0, 10.0],
            color=GREEN,
            stroke_width=4
        )
        curve_lbl_2 = create_text("Compute-Optimal Frontier", font_size=8, color=GREEN_B).move_to(axes_2.c2p(7.0, 0.92))

        # Show points: A (dominated), B (better performance at same cost), C (lower cost at same performance)
        pt_a = Dot(color=RED, radius=0.1).move_to(axes_2.c2p(4.0, 0.55))
        lbl_a = create_text("A (Dominated config)", font_size=8, color=RED).next_to(pt_a, DOWN, buff=0.1)

        pt_b = Dot(color=GREEN, radius=0.1).move_to(axes_2.c2p(4.0, 0.79))
        lbl_b = create_text("B (Same Cost, Better Acc)", font_size=8, color=GREEN).next_to(pt_b, UP, buff=0.12)

        pt_c = Dot(color=GREEN, radius=0.1).move_to(axes_2.c2p(0.73, 0.55))
        lbl_c = create_text("C (Same Acc, Lower Cost)", font_size=8, color=GREEN).next_to(pt_c, LEFT, buff=0.1)

        # Draw arrows from A to B and C
        arrow_to_b = Arrow(start=pt_a.get_top(), end=pt_b.get_bottom(), color=GREEN, stroke_width=2, buff=0.08)
        arrow_to_c = Arrow(start=pt_a.get_left(), end=pt_c.get_right(), color=GREEN, stroke_width=2, buff=0.08)

        # Explanatory text on the right
        explain_txt = create_markup_text(
            "<b>Pareto Dominance:</b>\n"
            "Configurations on the frontier are\n"
            "<b>not dominated</b>. For any point\n"
            "below the frontier (like A):\n"
            "• We can get higher accuracy (B)\n"
            "• Or we can reduce compute cost (C).",
            font_size=10, line_spacing=1.3
        ).move_to(RIGHT * 3.3 + UP * 0.2)

        self.play(
            Create(axes_2), Write(x_lbl_2), Write(y_lbl_2),
            Create(curve_2), Write(curve_lbl_2),
            Create(pt_a), Write(lbl_a),
            Write(explain_txt),
            run_time=1.5
        )
        self.wait(1.5)

        self.play(
            Create(pt_b), Write(lbl_b), Create(arrow_to_b),
            Create(pt_c), Write(lbl_c), Create(arrow_to_c),
            run_time=1.5
        )
        self.wait_until(cue_start[15])

        # --- Cue 15: Not simply the largest possible model ---
        # Add budget constraint visual
        budget_line = DashedLine(
            start=axes_2.c2p(4.0, 0),
            end=axes_2.c2p(4.0, 1.0),
            color=YELLOW,
            stroke_width=2
        )
        budget_lbl = create_text("Compute Budget Limit C", font_size=8, color=YELLOW_B).move_to(axes_2.c2p(4.3, 0.2)).rotate(np.pi/2)

        self.play(
            Create(budget_line), Write(budget_lbl),
            run_time=1.2
        )
        self.wait_until(cue_start[16])

        # --- Cue 16: Systems Efficiency Bridge ---
        self.play(
            FadeOut(axes_2), FadeOut(x_lbl_2), FadeOut(y_lbl_2),
            FadeOut(curve_2), FadeOut(curve_lbl_2),
            FadeOut(pt_a), FadeOut(lbl_a),
            FadeOut(pt_b), FadeOut(lbl_b), FadeOut(arrow_to_b),
            FadeOut(pt_c), FadeOut(lbl_c), FadeOut(arrow_to_c),
            FadeOut(budget_line), FadeOut(budget_lbl),
            FadeOut(explain_txt),
            FadeOut(part4_title),
            run_time=0.8
        )

        part5_title = create_text("5. The Systems Efficiency Bridge", font_size=13, color=BLUE_A)
        part5_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part5_title), run_time=0.8)
        self.wait_until(cue_start[17])

        # --- Cue 17: Sequential vs. Parallel execution comparison ---
        seq_box = RoundedRectangle(width=5.8, height=3.0, color=RED, fill_color="#1f0c0c", fill_opacity=0.9, corner_radius=0.08)
        seq_box.move_to(LEFT * 3.3 + DOWN * 0.6)
        seq_title = create_text("System A: Sequential Execution", font_size=11, color=RED).next_to(seq_box.get_top(), DOWN, buff=0.15)
        
        # Draw sequential tokens
        t_seq = VGroup()
        for idx in range(3):
            tok = RoundedRectangle(width=1.0, height=0.5, color=GRAY_D, fill_color="#121315", fill_opacity=0.9, corner_radius=0.04)
            lbl = create_text(f"Token {idx+1}", font_size=8, color=WHITE).move_to(tok.get_center())
            t_seq.add(VGroup(tok, lbl))
        t_seq.arrange(RIGHT, buff=0.4).next_to(seq_title, DOWN, buff=0.4)

        # arrows connecting them
        arrows_seq = VGroup()
        for idx in range(2):
            arr = Arrow(start=t_seq[idx].get_right(), end=t_seq[idx+1].get_left(), color=RED, stroke_width=2, max_tip_length_to_length_ratio=0.2)
            arrows_seq.add(arr)

        latency_seq = create_text("High Latency: Time = 3 units", font_size=9, color=RED).next_to(t_seq, DOWN, buff=0.4)
        seq_group = VGroup(seq_box, seq_title, t_seq, arrows_seq, latency_seq)

        # Parallel
        par_box = RoundedRectangle(width=5.8, height=3.0, color=GREEN, fill_color="#0c1f13", fill_opacity=0.9, corner_radius=0.08)
        par_box.move_to(RIGHT * 3.3 + DOWN * 0.6)
        par_title = create_text("System B: Parallel & Prefix Shared", font_size=11, color=GREEN).next_to(par_box.get_top(), DOWN, buff=0.15)

        prefix_tok = RoundedRectangle(width=1.3, height=0.5, color=GREEN, fill_color="#143c14", fill_opacity=0.9, corner_radius=0.04)
        prefix_lbl = create_text("Prefix", font_size=8, color=WHITE).move_to(prefix_tok.get_center())
        prefix_group = VGroup(prefix_tok, prefix_lbl).next_to(par_title, DOWN, buff=0.4).shift(LEFT * 1.5)

        t_par = VGroup()
        for idx in range(3):
            tok = RoundedRectangle(width=1.0, height=0.4, color=GRAY_D, fill_color="#121315", fill_opacity=0.9, corner_radius=0.04)
            lbl = create_text(f"Branch {idx+1}", font_size=7, color=WHITE).move_to(tok.get_center())
            t_par.add(VGroup(tok, lbl))
        t_par.arrange(DOWN, buff=0.25).next_to(par_title, DOWN, buff=0.15).shift(RIGHT * 1.5)

        arrows_par = VGroup()
        for idx in range(3):
            arr = Arrow(start=prefix_group.get_right(), end=t_par[idx].get_left(), color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.15)
            arrows_par.add(arr)

        latency_par = create_text("Low Latency (Shared Cache): Time = 1 unit", font_size=9, color=GREEN).next_to(t_par, DOWN, buff=0.3).align_to(par_box, LEFT).shift(RIGHT * 0.4)
        par_group = VGroup(par_box, par_title, prefix_group, t_par, arrows_par, latency_par)

        self.play(
            FadeIn(seq_group),
            FadeIn(par_group),
            run_time=1.5
        )
        self.wait_until(cue_start[18])

        # --- Cue 18: Cost-performance trade-off conclusion ---
        conclusion_lbl = create_markup_text(
            "<b>Conclusion:</b> Real cost depends on both <b>Algorithm</b> and <b>System Execution</b>.",
            font_size=12, color=YELLOW
        ).move_to(DOWN * 3.0)

        self.play(
            Write(conclusion_lbl),
            run_time=1.0
        )
        self.wait_until(voiceover_end + 0.25)

        # Cleanup
        self.play(
            FadeOut(seq_group),
            FadeOut(par_group),
            FadeOut(conclusion_lbl),
            FadeOut(part5_title),
            FadeOut(sub_title),
            run_time=1.0
        )

        assert_all_scene_voiceovers_played(self)
