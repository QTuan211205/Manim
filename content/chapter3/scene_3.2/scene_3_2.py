import os
import tempfile
from pathlib import Path
from manim import *

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[2] / "voiceover" / "generated_unsorted"


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    return time_offset + duration


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
def get_checkmark(color=GREEN, stroke_width=2.5):
    checkmark = VMobject(color=color, stroke_width=stroke_width)
    checkmark.set_points_as_corners([
        LEFT * 0.12 + DOWN * 0.05,
        ORIGIN + DOWN * 0.15,
        RIGHT * 0.2 + UP * 0.15
    ])
    return checkmark

# Note: visual/narration alignment comment translated from Vietnamese.
def get_crossmark(color=RED, stroke_width=2.5):
    cross = VGroup()
    line1 = Line(LEFT * 0.12 + UP * 0.12, RIGHT * 0.12 + DOWN * 0.12, color=color, stroke_width=stroke_width)
    line2 = Line(LEFT * 0.12 + DOWN * 0.12, RIGHT * 0.12 + UP * 0.12, color=color, stroke_width=stroke_width)
    cross.add(line1, line2)
    return cross

# Note: visual/narration alignment comment translated from Vietnamese.
def get_voter_icon(color=BLUE_A):
    voter = VGroup()
    # Note: visual/narration alignment comment translated from Vietnamese.
    body = RoundedRectangle(width=0.24, height=0.2, corner_radius=0.03, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.2)
    # Note: visual/narration alignment comment translated from Vietnamese.
    head = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=0.5, stroke_width=1.2)
    head.next_to(body, UP, buff=0.04)
    # Note: visual/narration alignment comment translated from Vietnamese.
    eye_l = Circle(radius=0.015, color=WHITE, fill_color=WHITE, fill_opacity=1.0).move_to(head.get_center() + LEFT * 0.03 + UP * 0.015)
    eye_r = Circle(radius=0.015, color=WHITE, fill_color=WHITE, fill_opacity=1.0).move_to(head.get_center() + RIGHT * 0.03 + UP * 0.015)
    # Note: visual/narration alignment comment translated from Vietnamese.
    antenna = Line(start=head.get_top(), end=head.get_top() + UP * 0.05, color=color, stroke_width=1.2)
    antenna_dot = Circle(radius=0.012, color=color, fill_color=color, fill_opacity=1.0).move_to(antenna.get_end())
    
    voter.add(body, head, eye_l, eye_r, antenna, antenna_dot)
    return voter

# Note: visual/narration alignment comment translated from Vietnamese.
class Speedometer(VGroup):
    def __init__(self, radius=0.6, title="Reward Model", **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.current_score = 0.0
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.arc = Arc(
            start_angle=PI, 
            angle=-PI, 
            radius=radius, 
            stroke_width=4, 
            color=GRAY_D
        )
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.red_zone = Arc(start_angle=PI, angle=-PI/3, radius=radius, stroke_width=4, color=RED)
        self.yellow_zone = Arc(start_angle=2*PI/3, angle=-PI/3, radius=radius, stroke_width=4, color=YELLOW)
        self.green_zone = Arc(start_angle=PI/3, angle=-PI/3, radius=radius, stroke_width=4, color=GREEN)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.ticks = VGroup()
        for val in [0.0, 0.25, 0.5, 0.75, 1.0]:
            angle = PI - val * PI
            tick = Line(
                start=ORIGIN,
                end=UP * 0.08,
                color=GRAY_A,
                stroke_width=1.2
            )
            tick.shift(UP * (radius - 0.08))
            tick.rotate(angle - PI/2, about_point=ORIGIN)
            self.ticks.add(tick)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.center_dot = Dot(point=ORIGIN, radius=0.05, color=WHITE)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.needle = Line(
            start=ORIGIN, 
            end=LEFT * (radius - 0.08), 
            color=WHITE, 
            stroke_width=2.2
        )
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.title_lbl = create_text(title, font_size=8, color=BLUE_B)
        self.title_lbl.next_to(self.center_dot, DOWN, buff=0.1)
        
        self.add(self.arc, self.red_zone, self.yellow_zone, self.green_zone, self.ticks, self.center_dot, self.needle, self.title_lbl)


class Scene3_2(Scene):
    def construct(self):
        # =========================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #     h(y^(1), ..., y^(N))`."
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #     et al., 2024]."
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #     `over-optimization` trong slide."
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =========================================================================

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.camera.background_color = "#111111"

        # Voiceover audio is scheduled from actual MP3 durations.
        voiceover_end = 0.0
        voiceover_end = add_voiceover(self, "sc32_1.mp3", voiceover_end, 8.542)
        voiceover_end = add_voiceover(self, "sc32_2.mp3", voiceover_end, 30.589)
        voiceover_end = add_voiceover(self, "sc32_3.mp3", voiceover_end, 27.402)
        voiceover_end = add_voiceover(self, "sc32_4.mp3", voiceover_end, 23.406)
        voiceover_end = add_voiceover(self, "sc32_5.mp3", voiceover_end, 22.895)
        voiceover_end = add_voiceover(self, "sc32_6.mp3", voiceover_end, 27.632)
        voiceover_end = add_voiceover(self, "sc32_7.mp3", voiceover_end, 24.613)


        # =====================================================================
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        chapter_title = create_text("Chapter 3: High-Level Orchestrators", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 3.2: Parallel Generation Algorithms (Best-of-N, Voting, MBR)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(5.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        sub_title = create_text("Parallel generation algorithms (Best-of-N, Voting, MBR)", font_size=16, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(3.0)

        # =====================================================================
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        part1_title = create_text("1. Best-of-N parallel generation & reward hacking traps", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part1_title), run_time=0.8)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        bon_intro = create_markup_text(
            "<b>Best-of-N (Rejection Sampling):</b> Generate <i>N</i> independent answers in parallel,\n"
            "score them with a reward model, and select the best one.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.3)
        self.play(Write(bon_intro), run_time=2.0)
        self.wait(10.0)

        # RM training box
        rm_train_box = RoundedRectangle(width=8.4, height=2.4, color=BLUE_B, fill_color="#141c2b", fill_opacity=0.9, corner_radius=0.1)
        rm_train_box.move_to(DOWN * 0.2)
        rm_train_title = create_text("Reward Model Training Data", font_size=12, color=BLUE_A).next_to(rm_train_box.get_top(), DOWN, buff=0.15)
        
        data1_title = create_markup_text("<b>1. Classification (Correct/Incorrect)</b>", font_size=9.5, color=WHITE)
        data1_detail = create_markup_text(
            "• (x, y) → y is correct (reward = 1)\n"
            "• (x, y) → y is incorrect (reward = 0)\n"
            "<span foreground='#888888'>[Cobbe et al., 2021]</span>",
            font_size=8, line_spacing=1.2
        )
        data1_group = VGroup(data1_title, data1_detail).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        data2_title = create_markup_text("<b>2. Preference Data (RLHF/DPO)</b>", font_size=9.5, color=WHITE)
        data2_detail = create_markup_text(
            "• (x, y<sub>w</sub>, y<sub>l</sub>) where y<sub>w</sub> > y<sub>l</sub>\n"
            "• Optimizing pairwise ranking loss\n"
            "<span foreground='#888888'>[Stiennon et al., 2020]</span>",
            font_size=8, line_spacing=1.2
        )
        data2_group = VGroup(data2_title, data2_detail).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        data_split = VGroup(data1_group, data2_group).arrange(RIGHT, buff=0.6)
        data_split.move_to(rm_train_box.get_center() + DOWN * 0.15)
        rm_train_group = VGroup(rm_train_box, rm_train_title, data_split)

        self.play(FadeIn(rm_train_group, shift=UP * 0.15), run_time=1.2)
        self.wait(12.0)
        self.play(FadeOut(rm_train_group), run_time=0.8)

        # Best-of-N formula box
        bon_formula_box = RoundedRectangle(width=8.0, height=1.6, color=BLUE_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        bon_formula_box.move_to(DOWN * 0.2)
        bon_formula_title = create_text("Formula Best-of-N", font_size=11, color=BLUE_B).next_to(bon_formula_box.get_top(), DOWN, buff=0.15)
        
        bon_formula_txt = create_markup_text(
            "Best-of-N = argmax<sub>y in {y<sup>(1)</sup>,...,y<sup>(N)</sup>}</sub>  v(y)\n"
            "Best-of-N ≈ argmax<sub>y</sub> v(y) ≈ argmax<sub>y</sub> A(y)",
            font_size=11, line_spacing=1.3
        ).move_to(bon_formula_box.get_center() + DOWN * 0.1)
        bon_formula_group = VGroup(bon_formula_box, bon_formula_title, bon_formula_txt)

        self.play(FadeIn(bon_formula_group, shift=UP * 0.15), run_time=1.2)
        self.wait(10.0)
        self.play(FadeOut(bon_formula_group), run_time=0.8)

        # Prompt x
        prompt_box = RoundedRectangle(width=2.2, height=1.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        prompt_box.move_to(LEFT * 5.0 + DOWN * 0.3)
        prompt_lbl = create_text("Prompt x", font_size=12, color=GREEN).move_to(prompt_box.get_center())

        self.play(FadeIn(prompt_box), Write(prompt_lbl), run_time=1.0)
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        y_y_coords = [1.3, 0.5, -0.3, -1.1, -1.9]
        y_boxes = VGroup()
        y_texts = VGroup()
        y_arrows = VGroup()

        y_texts_str = [
            'y(1): "The result is 42"',
            'y(2): "17 + 25 = 42"',
            'y(3): "John has 42 items"',
            'y(4): "17 + 25 = 32"',
            'y(5): "Answer y(5)"'
        ]

        for idx, y_val in enumerate(y_y_coords):
            box = RoundedRectangle(width=2.8, height=0.6, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.06)
            box.move_to(LEFT * 1.0 + UP * y_val)
            lbl = create_text(y_texts_str[idx], font_size=9, color=WHITE).move_to(box.get_center())
            arrow = Arrow(start=prompt_box.get_right(), end=box.get_left(), color=GRAY_D, stroke_width=1.5, buff=0.08)
            
            y_boxes.add(box)
            y_texts.add(lbl)
            y_arrows.add(arrow)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            Create(y_arrows),
            FadeIn(y_boxes),
            Write(y_texts),
            run_time=2.0
        )
        self.wait(12.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        rm_box = RoundedRectangle(width=2.4, height=2.2, color=BLUE_A, fill_color="#141c2b", fill_opacity=0.9, corner_radius=0.08)
        rm_box.move_to(RIGHT * 4.6 + DOWN * 0.3)
        
        speedometer = Speedometer(radius=0.7, title="Reward Model (Scoring)")
        speedometer.move_to(rm_box.get_center() + UP * 0.25)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        digital_score_lbl = create_text("Score: 0.00", font_size=10, color=GRAY_A)
        digital_score_lbl.next_to(speedometer.center_dot, DOWN, buff=0.45)

        self.play(
            FadeIn(rm_box),
            FadeIn(speedometer),
            FadeIn(digital_score_lbl),
            run_time=1.0
        )
        self.wait(6.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        score_colors = [RED, GREEN, YELLOW, GREEN_B, GREEN]
        score_values = [0.15, 0.88, 0.45, 0.62, 0.99]
        score_labels = VGroup()
        rm_flow_arrows = VGroup()

        for idx, y_val in enumerate(y_y_coords):
            # Note: visual/narration alignment comment translated from Vietnamese.
            flow_arrow = Line(start=y_boxes[idx].get_right(), end=rm_box.get_left() + UP * y_val * 0.25, color=BLUE_A, stroke_width=1.2)
            rm_flow_arrows.add(flow_arrow)

            # Note: visual/narration alignment comment translated from Vietnamese.
            lbl = create_text(f"Score: {score_values[idx]:.2f}", font_size=10, color=score_colors[idx])
            lbl.next_to(y_boxes[idx], RIGHT, buff=0.15)
            
            # Note: visual/narration alignment comment translated from Vietnamese.
            mask = SurroundingRectangle(lbl, color="#111111", fill_color="#111111", fill_opacity=1.0, stroke_width=0, buff=0.04)
            label_group = VGroup(mask, lbl)
            score_labels.add(label_group)

        # Note: visual/narration alignment comment translated from Vietnamese.
        for idx in range(5):
            # Note: visual/narration alignment comment translated from Vietnamese.
            target_score = score_values[idx]
            delta_angle = - (target_score - speedometer.current_score) * PI
            speedometer.current_score = target_score
            
            new_digital_lbl = create_text(f"Score: {target_score:.2f}", font_size=10, color=score_colors[idx])
            new_digital_lbl.next_to(speedometer.center_dot, DOWN, buff=0.45)

            self.play(
                Create(rm_flow_arrows[idx]),
                Rotate(speedometer.needle, angle=delta_angle, about_point=speedometer.center_dot.get_center()),
                Transform(digital_score_lbl, new_digital_lbl),
                FadeIn(score_labels[idx]),
                run_time=0.8
            )
            self.wait(2.0)

        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        selection_box = RoundedRectangle(width=2.9, height=0.7, color=GREEN, stroke_width=2.5, fill_opacity=0.0, corner_radius=0.08).move_to(y_boxes[1].get_center())
        self.play(Create(selection_box), run_time=0.8)
        self.wait(10.0)
        self.play(FadeOut(selection_box), run_time=0.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        y5_hacking_text = create_text('"...the the the the the..."', font_size=8, color=RED)
        y5_hacking_text.move_to(y_boxes[4].get_center())
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        hacking_warn_box = RoundedRectangle(width=3.2, height=0.8, color=RED, fill_color=RED_E, fill_opacity=0.3, corner_radius=0.08)
        hacking_warn_box.next_to(y_boxes[4], DOWN, buff=0.4)
        hacking_warn_lbl = create_text("Reward Hacking\n(Reward-model exploit)", font_size=10, color=RED).move_to(hacking_warn_box.get_center())

        # Note: visual/narration alignment comment translated from Vietnamese.
        arrow_to_hacking = Arrow(start=hacking_warn_box.get_top(), end=y_boxes[4].get_bottom(), color=RED, stroke_width=1.5, buff=0.05)

        # Note: visual/narration alignment comment translated from Vietnamese.
        warning_icon = VGroup()
        triangle = Polygon(UP * 0.15, DOWN * 0.1 + LEFT * 0.15, DOWN * 0.1 + RIGHT * 0.15, color=RED, fill_color=RED, fill_opacity=0.9, stroke_width=1)
        excl = create_text("!", font_size=8, color=WHITE).move_to(triangle.get_center() + DOWN * 0.01)
        warning_icon.add(triangle, excl)
        warning_icon.next_to(digital_score_lbl, RIGHT, buff=0.1)

        self.play(
            ReplacementTransform(y_texts[4], y5_hacking_text),
            y_boxes[4].animate.set_stroke(color=RED).set_fill(color="#551a1a", opacity=0.9),
            # Note: visual/narration alignment comment translated from Vietnamese.
            Rotate(speedometer.needle, angle=- (0.99 - speedometer.current_score) * PI, about_point=speedometer.center_dot.get_center()),
            Transform(digital_score_lbl, create_text("Score: 0.99 !!!", font_size=10, color=RED).next_to(speedometer.center_dot, DOWN, buff=0.45)),
            FadeIn(warning_icon),
            run_time=1.0
        )
        speedometer.current_score = 0.99
        self.wait(6.0)

        self.play(
            FadeIn(hacking_warn_box),
            Write(hacking_warn_lbl),
            Create(arrow_to_hacking),
            run_time=1.0
        )
        self.wait(30.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        overopt_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.2, 0.2],
            x_length=6.0,
            y_length=3.0,
            axis_config={"color": GRAY, "stroke_width": 1.5}
        ).move_to(DOWN * 0.5)
        
        overopt_x_label = create_text("Inference Compute N", font_size=8, color=GRAY_A).next_to(overopt_axes.x_axis, DOWN, buff=0.25, aligned_edge=RIGHT)
        overopt_y_label = create_text("Score / Acceptability", font_size=8, color=GRAY_A).next_to(overopt_axes.y_axis, LEFT, buff=0.2).rotate(90 * DEGREES)
        
        rm_curve = overopt_axes.plot(lambda x: 1.0 - np.exp(-0.4 * x), x_range=[0.1, 9.5], color=BLUE, stroke_width=2.5)
        rm_lbl = create_text("Reward Model Score", font_size=8, color=BLUE).next_to(rm_curve.get_end(), UR, buff=0.1)
        
        acc_curve = overopt_axes.plot(lambda x: 1.25 * x * np.exp(-0.35 * x), x_range=[0.1, 9.5], color=GREEN, stroke_width=2.5)
        acc_lbl = create_text("True Acceptability", font_size=8, color=GREEN).next_to(overopt_axes.c2p(2.8, 1.25*2.8*np.exp(-0.35*2.8)), UP, buff=0.1)
        
        overopt_region = DashedLine(overopt_axes.c2p(3.0, 0), overopt_axes.c2p(3.0, 1.0), color=RED, stroke_width=1.5)
        overopt_region_lbl = create_markup_text(
            "<span color='#FF5555'>Over-optimization\n(Reward Hacking)</span>", 
            font_size=7, color=RED
        ).next_to(overopt_region, RIGHT, buff=0.15).shift(UP * 0.5)
        
        overopt_group = VGroup(overopt_axes, overopt_x_label, overopt_y_label, rm_curve, rm_lbl, acc_curve, acc_lbl, overopt_region, overopt_region_lbl)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(prompt_box), FadeOut(prompt_lbl),
            FadeOut(y_boxes), FadeOut(y_texts), FadeOut(y_arrows),
            FadeOut(rm_box), FadeOut(speedometer), FadeOut(digital_score_lbl), FadeOut(warning_icon),
            FadeOut(rm_flow_arrows), FadeOut(score_labels), FadeOut(y5_hacking_text),
            FadeOut(hacking_warn_box), FadeOut(hacking_warn_lbl), FadeOut(arrow_to_hacking),
            run_time=1.0
        )
        self.play(FadeIn(overopt_group), run_time=1.2)
        self.wait(15.0)
        self.play(
            FadeOut(overopt_group),
            FadeOut(bon_intro),
            FadeOut(part1_title),
            run_time=1.0
        )
        self.wait(1.0)

        # =====================================================================
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        part2_title = create_text("2. Majority Voting (Majority Voting) & Self-Consistency method", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part2_title), run_time=0.8)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        voting_intro = create_markup_text(
            "<b>Self-Consistency (Majority Voting):</b> Generate many intermediate reasoning chains\n"
            "and vote for the final answer that appears most often.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.0)
        self.play(Write(voting_intro), run_time=2.0)
        self.wait(16.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        math_question_box = RoundedRectangle(width=9.0, height=0.6, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        math_question_box.move_to(UP * 0.9)
        math_question_lbl = create_markup_text("<b>Math question:</b> <i>\"John has 17 apples. John buys 25 more apples. How many apples does John have?\"</i>", font_size=11, color=YELLOW)
        math_question_lbl.move_to(math_question_box.get_center())

        self.play(FadeIn(math_question_box), Write(math_question_lbl), run_time=1.0)
        self.wait(10.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        cot_y_coords = [0.1, -0.6, -1.3, -2.0]
        cot_boxes = VGroup()
        cot_texts = VGroup()

        cot_data = [
            ("Reasoning z1: 17 + 20 = 37, 37 + 5 = 42", "y = 42", "#87FF87"),
            ("Reasoning z2: 17 + 5 = 22, 22 + 20 = 42", "y = 42", "#87FF87"),
            ("Reasoning z3: 10 + 20 = 30, 7 + 5 = 12 -> 42", "y = 42", "#87FF87"),
            ("Reasoning z4: 17 + 25 = 17 + 20 + 5 = 32", "y = 32 (Sai)", "#FF8787")
        ]

        # Note: visual/narration alignment comment translated from Vietnamese.
        voters = VGroup()
        for idx in range(4):
            v = get_voter_icon(color=[BLUE_B, BLUE_C, BLUE_D, RED_C][idx])
            v.move_to(LEFT * 4.1 + UP * cot_y_coords[idx])
            voters.add(v)

        for idx, (z_str, y_str, col_str) in enumerate(cot_data):
            box = RoundedRectangle(width=7.4, height=0.5, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.05)
            box.move_to(RIGHT * 0.2 + UP * cot_y_coords[idx])
            
            # Note: visual/narration alignment comment translated from Vietnamese.
            text_str = f"{z_str}  →  <span foreground='{col_str}'><b>{y_str}</b></span>"
            lbl = create_markup_text(text_str, font_size=10).move_to(box.get_center())
            
            cot_boxes.add(box)
            cot_texts.add(lbl)

        self.play(
            FadeIn(voters),
            FadeIn(cot_boxes),
            Write(cot_texts),
            run_time=2.0
        )
        self.wait(18.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        
        voter_ans_lbls = VGroup()
        voter_dest_coords = [LEFT * 3.0, LEFT * 1.0, RIGHT * 1.0, RIGHT * 3.0]
        
        for idx in range(4):
            ans_text = "y = 42" if idx < 3 else "y = 32"
            ans_color = GREEN if idx < 3 else RED
            lbl = create_text(ans_text, font_size=10, color=ans_color)
            lbl.move_to(voter_dest_coords[idx] + UP * 0.20)
            voter_ans_lbls.add(lbl)

        # Note: visual/narration alignment comment translated from Vietnamese.
        voter_sub_boxes = VGroup()
        for idx in range(4):
            box = RoundedRectangle(width=1.6, height=1.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.8, corner_radius=0.06)
            box.move_to(voter_dest_coords[idx] + UP * 0.45)
            voter_sub_boxes.add(box)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(math_question_box), FadeOut(math_question_lbl),
            FadeOut(cot_boxes), FadeOut(cot_texts),
            voters[0].animate.move_to(voter_dest_coords[0] + UP * 0.65),
            voters[1].animate.move_to(voter_dest_coords[1] + UP * 0.65),
            voters[2].animate.move_to(voter_dest_coords[2] + UP * 0.65),
            voters[3].animate.move_to(voter_dest_coords[3] + UP * 0.65),
            FadeIn(voter_sub_boxes),
            FadeIn(voter_ans_lbls),
            run_time=1.5
        )
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        bin_42 = RoundedRectangle(width=3.6, height=1.6, color=GREEN, fill_color=GREEN_E, fill_opacity=0.1, corner_radius=0.08)
        bin_42.move_to(LEFT * 2.0 + DOWN * 1.4)
        bin_42_lbl = create_text("Group y = 42", font_size=11, color=GREEN).next_to(bin_42.get_top(), DOWN, buff=0.15)
        
        bin_32 = RoundedRectangle(width=3.6, height=1.6, color=RED, fill_color=RED_E, fill_opacity=0.1, corner_radius=0.08)
        bin_32.move_to(RIGHT * 2.0 + DOWN * 1.4)
        bin_32_lbl = create_text("Group y = 32", font_size=11, color=RED).next_to(bin_32.get_top(), DOWN, buff=0.15)

        self.play(
            FadeIn(bin_42), Write(bin_42_lbl),
            FadeIn(bin_32), Write(bin_32_lbl),
            run_time=1.0
        )
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        ballots = VGroup()
        ballot_targets = [
            bin_42.get_center() + DOWN * 0.3 + LEFT * 0.8,
            bin_42.get_center() + DOWN * 0.3 + ORIGIN,
            bin_42.get_center() + DOWN * 0.3 + RIGHT * 0.8,
            bin_32.get_center() + DOWN * 0.3
        ]
        
        for idx in range(4):
            color = GREEN if idx < 3 else RED
            # Note: visual/narration alignment comment translated from Vietnamese.
            card = RoundedRectangle(width=0.5, height=0.4, color=color, fill_color=color, fill_opacity=0.8, corner_radius=0.04)
            card.move_to(voters[idx].get_center())
            card_lbl = create_text("+1", font_size=8, color=WHITE).move_to(card.get_center())
            ballots.add(VGroup(card, card_lbl))

        # Note: visual/narration alignment comment translated from Vietnamese.
        count_42_lbl = create_text("0 votes", font_size=12, color=GREEN).next_to(bin_42, DOWN, buff=0.2)
        count_32_lbl = create_text("0 votes", font_size=12, color=RED).next_to(bin_32, DOWN, buff=0.2)
        self.play(FadeIn(count_42_lbl), FadeIn(count_32_lbl), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        for idx in range(4):
            target_pos = ballot_targets[idx]
            self.play(
                ballots[idx].animate.move_to(target_pos),
                run_time=0.8
            )
            # Note: visual/narration alignment comment translated from Vietnamese.
            if idx < 3:
                new_cnt_lbl = create_text(f"{idx+1} votes", font_size=12, color=GREEN).next_to(bin_42, DOWN, buff=0.2)
                self.play(Transform(count_42_lbl, new_cnt_lbl), run_time=0.3)
            else:
                new_cnt_lbl = create_text("1 votes", font_size=12, color=RED).next_to(bin_32, DOWN, buff=0.2)
                self.play(Transform(count_32_lbl, new_cnt_lbl), run_time=0.3)
            self.wait(1.5)

        self.wait(10.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        winner_highlight = RoundedRectangle(width=3.9, height=2.8, color=GREEN, stroke_width=3.5, fill_opacity=0, corner_radius=0.1).move_to(
            LEFT * 2.0 + DOWN * 1.85
        )
        winner_tag = create_text("HIGH CONSENSUS - SELECT Y = 42", font_size=10, color=GREEN).next_to(count_42_lbl, DOWN, buff=0.2)

        self.play(Create(winner_highlight), Write(winner_tag), run_time=1.0)
        self.wait(12.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(voters), FadeOut(voter_sub_boxes), FadeOut(voter_ans_lbls),
            FadeOut(bin_42), FadeOut(bin_42_lbl),
            FadeOut(bin_32), FadeOut(bin_32_lbl),
            FadeOut(ballots), FadeOut(count_42_lbl), FadeOut(count_32_lbl),
            FadeOut(winner_highlight), FadeOut(winner_tag),
            run_time=1.0
        )
        self.wait(1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        voting_formula_box = RoundedRectangle(width=8.5, height=2.0, color=BLUE_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        voting_formula_box.move_to(DOWN * 0.4)
        voting_formula_title = create_text("Formula Voting & Weighted Voting", font_size=12, color=BLUE_B).next_to(voting_formula_box.get_top(), DOWN, buff=0.15)
        
        voting_formula_txt = create_markup_text(
            "Voting:   argmax<sub>a</sub>  ∑<sub>i=1</sub><sup>N</sup>  <b>1</b>{y<sup>(i)</sup> = a}\n"
            "Weighted Voting:   argmax<sub>a</sub>  ∑<sub>i=1</sub><sup>N</sup>  v(y<sup>(i)</sup>) · <b>1</b>{y<sup>(i)</sup> = a}",
            font_size=11, line_spacing=1.3
        ).move_to(voting_formula_box.get_center() + DOWN * 0.1)
        voting_formula_group = VGroup(voting_formula_box, voting_formula_title, voting_formula_txt)

        self.play(FadeIn(voting_formula_group, shift=UP * 0.15), run_time=1.2)
        self.wait(11.0)
        self.play(FadeOut(voting_formula_group), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        formula_box = RoundedRectangle(width=9.0, height=2.8, color=BLUE_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        formula_box.move_to(DOWN * 0.4)
        formula_title = create_text("Mathematical nature: Operation marginalization (Marginalization)", font_size=12, color=BLUE_B).next_to(formula_box.get_top(), DOWN, buff=0.2)

        # Note: visual/narration alignment comment translated from Vietnamese.
        formula_txt = create_markup_text(
            "argmax<sub>y</sub>  ∑<sub>z</sub>  P( <span foreground='#FFFF00'>y</span>, <span foreground='#5CD65C'>z</span> | X )",
            font_size=24
        ).move_to(formula_box.get_center() + UP * 0.1)

        # Note: visual/narration alignment comment translated from Vietnamese.
        ex_lbl = create_markup_text(
            "Where:\n"
            "  • <span foreground='#5CD65C'><b>z</b></span>: Reasoning chains trung gian (Chain of Thought / Scratchpad)\n"
            "  • <span foreground='#FFFF00'><b>y</b></span>: final answer at the terminal point",
            font_size=11, line_spacing=1.3
        ).next_to(formula_box.get_bottom(), UP, buff=0.25)
        ex_lbl.align_to(formula_box, LEFT).shift(RIGHT * 0.8)

        self.play(
            FadeIn(formula_box),
            Write(formula_title),
            Write(formula_txt),
            Write(ex_lbl),
            run_time=1.5
        )
        self.wait(15.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(formula_box), FadeOut(formula_title),
            FadeOut(formula_txt), FadeOut(ex_lbl),
            run_time=1.0
        )
        self.wait(1.0)

        # Convergence Theorem & Takeaways
        convergence_box = RoundedRectangle(width=9.2, height=3.4, color=BLUE_B, fill_color="#0b1324", fill_opacity=0.9, corner_radius=0.1)
        convergence_box.move_to(DOWN * 0.3)
        convergence_title = create_text("Convergence theorem & takeaways", font_size=12, color=BLUE_A).next_to(convergence_box.get_top(), DOWN, buff=0.18)
        
        convergence_formula = create_markup_text(
            "Accuracy →  1/M ∑<sub>i=1</sub><sup>M</sup>  <b>I</b> [ a<sub>i</sub><sup>*</sup> = argmax<sub>a</sub>  ∑<sub>z</sub>  v(x, z, a) g(z, a | x) ]",
            font_size=9.5, color=YELLOW
        ).move_to(convergence_box.get_center() + UP * 0.7)
        
        takeaways_list = VGroup(
            create_markup_text("• <b>Takeaway 1:</b> Accuracy converges gradually instead of increasing forever with N.", font_size=8.5, color=WHITE),
            create_markup_text("• <b>Takeaway 2:</b> Weighted voting beats ordinary voting when <i>v · g</i> concentrates weight correctly.", font_size=8.5, color=WHITE),
            create_markup_text("• <b>Takeaway 3:</b> To improve the performance ceiling, improve verifier <i>v</i> or generator <i>g</i>.", font_size=8.5, color=WHITE)
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(convergence_formula, DOWN, buff=0.25).shift(LEFT * 0.2)
        convergence_group = VGroup(convergence_box, convergence_title, convergence_formula, takeaways_list)

        self.play(FadeIn(convergence_group, shift=UP * 0.15), run_time=1.2)
        self.wait(22.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(voting_intro), FadeOut(convergence_group), FadeOut(part2_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        part3_title = create_text("3. Minimum Bayes risk (Minimum Bayes Risk - MBR)", font_size=13, color=BLUE_A)
        part3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part3_title), run_time=0.8)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        mbr_intro = create_markup_text(
            "<b>Minimum Bayes Risk (MBR):</b> Instead of exact word matching,\n"
            "MBR compares answer semantics pairwise to select the highest-consensus answer.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.0)
        self.play(Write(mbr_intro), run_time=2.0)
        self.wait(18.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        mbr_formula_box = RoundedRectangle(width=7.5, height=1.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        mbr_formula_box.move_to(UP * 0.7)
        mbr_formula_txt = create_markup_text(
            "argmax<sub>y</sub>  ∑<sub>j</sub>  U( <span foreground='#FFFF00'>y</span>, <span foreground='#A0A0A0'>y<sup>(j)</sup></span> )",
            font_size=20
        ).move_to(mbr_formula_box.get_center())

        self.play(FadeIn(mbr_formula_box), Write(mbr_formula_txt), run_time=1.2)
        self.wait(22.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        cluster_center = LEFT * 3.8 + DOWN * 1.5
        cluster_title = create_text("Semantic space of answers", font_size=10, color=BLUE_A)
        cluster_title.move_to(LEFT * 3.8 + DOWN * 0.1)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        node_coords = {
            1: cluster_center + UP * 0.0 + LEFT * 0.0,      # Note: visual/narration alignment comment translated from Vietnamese.
            2: cluster_center + UP * 0.5 + LEFT * 1.0,      # Note: visual/narration alignment comment translated from Vietnamese.
            4: cluster_center + DOWN * 0.6 + RIGHT * 0.9,   # Note: visual/narration alignment comment translated from Vietnamese.
            3: cluster_center + DOWN * 0.8 + LEFT * 1.1,    # y(3) xa (outlier)
            5: cluster_center + UP * 0.8 + RIGHT * 1.1      # y(5) xa (outlier)
        }

        # Note: visual/narration alignment comment translated from Vietnamese.
        connections = VGroup()
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        connections.add(Line(node_coords[1], node_coords[2], color=GREEN, stroke_width=2.5))
        connections.add(Line(node_coords[1], node_coords[4], color=GREEN, stroke_width=2.5))
        connections.add(Line(node_coords[2], node_coords[4], color=GREEN, stroke_width=2.0))

        # Note: visual/narration alignment comment translated from Vietnamese.
        connections.add(DashedLine(node_coords[1], node_coords[3], color=RED, stroke_width=1.0, dash_length=0.08))
        connections.add(DashedLine(node_coords[1], node_coords[5], color=RED, stroke_width=1.0, dash_length=0.08))
        connections.add(DashedLine(node_coords[2], node_coords[3], color=RED, stroke_width=1.0, dash_length=0.08))
        connections.add(DashedLine(node_coords[4], node_coords[5], color=RED, stroke_width=1.0, dash_length=0.08))
        
        connections.set_z_index(1)

        # Note: visual/narration alignment comment translated from Vietnamese.
        weight_labels = VGroup()
        weight_data = [
            ("0.92", node_coords[1]*0.5 + node_coords[2]*0.5 + UP*0.1),
            ("0.88", node_coords[1]*0.5 + node_coords[4]*0.5 + DOWN*0.1),
            ("0.20", node_coords[1]*0.5 + node_coords[3]*0.5 + LEFT*0.1),
            ("0.15", node_coords[1]*0.5 + node_coords[5]*0.5 + RIGHT*0.1)
        ]
        for w_val, w_pos in weight_data:
            w_lbl = create_text(w_val, font_size=8, color=GRAY_A)
            w_lbl.move_to(w_pos)
            mask = SurroundingRectangle(w_lbl, color="#111111", fill_color="#111111", fill_opacity=1.0, stroke_width=0, buff=0.02)
            weight_labels.add(VGroup(mask, w_lbl))
            
        weight_labels.set_z_index(2)

        # Note: visual/narration alignment comment translated from Vietnamese.
        nodes = VGroup()
        node_colors = [YELLOW, GREEN_B, RED_A, GREEN_C, RED_B]
        
        for idx in range(5):
            y_idx = idx + 1
            pos = node_coords[y_idx]
            circle = Circle(radius=0.25, color=node_colors[idx], fill_color="#141517", fill_opacity=1.0, stroke_width=1.5)
            circle.move_to(pos)
            lbl = create_text(f"y({y_idx})", font_size=9, color=WHITE).move_to(pos)
            nodes.add(VGroup(circle, lbl))
            
        nodes.set_z_index(3)

        self.play(
            FadeIn(cluster_title),
            FadeIn(nodes),
            Create(connections),
            FadeIn(weight_labels),
            run_time=2.0
        )
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        matrix_center = RIGHT * 1.6 + DOWN * 1.5
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        row_labels = VGroup()
        col_labels = VGroup()

        cell_size = 0.55
        start_x = -1.1
        start_y = 0.4

        for r in range(5):
            lbl_r = create_text(f"y({r+1})", font_size=9, color=YELLOW)
            lbl_r.move_to(matrix_center + LEFT * 1.6 + UP * (start_y - r * cell_size))
            row_labels.add(lbl_r)

            lbl_c = create_text(f"y({r+1})", font_size=9, color=YELLOW)
            lbl_c.move_to(matrix_center + RIGHT * (start_x + r * cell_size) + UP * 0.8)
            col_labels.add(lbl_c)

        # Note: visual/narration alignment comment translated from Vietnamese.
        matrix_data = [
            ["1.00", "0.92", "0.20", "0.88", "0.15"],  # y1
            ["0.92", "1.00", "0.15", "0.85", "0.12"],  # y2
            ["0.20", "0.15", "1.00", "0.18", "0.25"],  # y3
            ["0.88", "0.85", "0.18", "1.00", "0.15"],  # y4
            ["0.15", "0.12", "0.25", "0.15", "1.00"]   # y5
        ]

        matrix_cells = VGroup()
        matrix_texts = VGroup()

        for r in range(5):
            for c in range(5):
                cell_x = start_x + c * cell_size
                cell_y = start_y - r * cell_size
                pos = matrix_center + RIGHT * cell_x + UP * cell_y

                # Note: visual/narration alignment comment translated from Vietnamese.
                val = float(matrix_data[r][c])
                if r == c:
                    cell_color = GRAY_D
                    fill_opacity = 0.5
                    text_color = WHITE
                elif val > 0.8:
                    cell_color = GREEN_E
                    fill_opacity = 0.35
                    text_color = GREEN
                else:
                    cell_color = RED_E
                    fill_opacity = 0.15
                    text_color = GRAY_B

                square = Square(side_length=cell_size, color=GRAY_E, stroke_width=0.8, fill_color=cell_color, fill_opacity=fill_opacity)
                square.move_to(pos)
                matrix_cells.add(square)

                txt = create_text(matrix_data[r][c], font_size=7, color=text_color).move_to(pos)
                matrix_texts.add(txt)

        # Note: visual/narration alignment comment translated from Vietnamese.
        legend_bar = VGroup()
        legend_colors = [GREEN, GREEN_B, YELLOW, ORANGE, RED]
        legend_labels = ["1.0", "0.8", "0.5", "0.3", "0.0"]
        legend_x = start_x + 6.3 * cell_size

        for idx, color in enumerate(legend_colors):
            rect = Rectangle(width=0.15, height=0.3, stroke_width=0, fill_color=color, fill_opacity=0.8)
            rect.move_to(matrix_center + RIGHT * legend_x + UP * (0.6 - idx * 0.3))
            
            lbl = create_text(legend_labels[idx], font_size=7, color=GRAY_A)
            lbl.next_to(rect, RIGHT, buff=0.1)
            
            legend_bar.add(VGroup(rect, lbl))

        self.play(
            Write(row_labels),
            Write(col_labels),
            Create(matrix_cells),
            FadeIn(legend_bar),
            run_time=1.8
        )
        self.wait(5.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(Write(matrix_texts), run_time=2.0)
        self.wait(19.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        avg_header = create_text("Avg Utility", font_size=9, color=BLUE_A)
        avg_header.move_to(matrix_center + RIGHT * (start_x + 5.2 * cell_size) + UP * 0.8)
        self.play(Write(avg_header), run_time=0.8)

        avg_values = ["0.63", "0.61", "0.36", "0.61", "0.33"]
        avg_texts = VGroup()

        for r in range(5):
            cell_x = start_x + 5.2 * cell_size
            cell_y = start_y - r * cell_size
            pos = matrix_center + RIGHT * cell_x + UP * cell_y

            box = RoundedRectangle(width=0.8, height=0.4, color=BLUE_B, fill_color=BLACK, fill_opacity=0.5, corner_radius=0.03, stroke_width=1)
            box.move_to(pos)
            
            txt_color = GREEN if r == 0 else WHITE
            txt = create_text(avg_values[r], font_size=8, color=txt_color).move_to(pos)
            
            avg_texts.add(VGroup(box, txt))

        # Note: visual/narration alignment comment translated from Vietnamese.
        for r in range(5):
            self.play(FadeIn(avg_texts[r]), run_time=0.5)
        self.wait(22.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        winner_row_rect = RoundedRectangle(width=4.3, height=0.62, color=GREEN, stroke_width=2.5, fill_opacity=0, corner_radius=0.08).move_to(
            matrix_center + RIGHT * 0.23 + UP * start_y
        )
        winner_tag = create_text("SELECT Y(1)", font_size=10, color=GREEN).next_to(row_labels[0], LEFT, buff=0.25)

        # Note: visual/narration alignment comment translated from Vietnamese.
        winner_node_glow = Circle(radius=0.38, color=GREEN, stroke_width=3, fill_opacity=0.15).move_to(node_coords[1])
        winner_node_glow.set_z_index(2)

        self.play(
            Create(winner_row_rect),
            Write(winner_tag),
            Create(winner_node_glow),
            run_time=1.0
        )
        self.wait(24.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(mbr_intro), FadeOut(mbr_formula_box), FadeOut(mbr_formula_txt),
            FadeOut(cluster_title), FadeOut(nodes), FadeOut(connections), FadeOut(weight_labels), FadeOut(winner_node_glow),
            FadeOut(row_labels), FadeOut(col_labels), FadeOut(matrix_cells), FadeOut(legend_bar),
            FadeOut(matrix_texts), FadeOut(avg_header), FadeOut(avg_texts),
            FadeOut(winner_row_rect), FadeOut(winner_tag),
            FadeOut(part3_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        recap_title = create_text("Summary: Pros and cons of parallel generation techniques", font_size=13, color=YELLOW)
        recap_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(recap_title), run_time=0.8)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        comparison_table = VGroup()
        headers = ["Technique", "Core principle", "Traps / limits"]
        header_colors = [BLUE_A, WHITE, RED]
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        header_group = VGroup()
        for idx, h_text in enumerate(headers):
            cell = RoundedRectangle(width=3.2, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            cell.move_to(LEFT * (3.4 * (1 - idx)) + UP * 1.0)
            lbl = create_text(h_text, font_size=11, color=header_colors[idx]).move_to(cell.get_center())
            header_group.add(VGroup(cell, lbl))
        comparison_table.add(header_group)

        # Note: visual/narration alignment comment translated from Vietnamese.
        table_rows = [
            ("1. Best-of-N", "Choose the highest-RM-scored answer", "Reward Hacking"),
            ("2. Majority Voting", "Majority vote over CoT chains", "Not applicable to free-form text"),
            ("3. MBR (Bayes)", "Pairwise cross-similarity comparison", "High N^2 compute cost")
        ]

        row_y_coords = [0.2, -0.6, -1.4]
        for r_idx, row_data in enumerate(table_rows):
            row_group = VGroup()
            for c_idx, cell_text in enumerate(row_data):
                cell = RoundedRectangle(width=3.2, height=0.6, color=GRAY_E, fill_color="#121315", fill_opacity=0.8, corner_radius=0.04)
                cell.move_to(LEFT * (3.4 * (1 - c_idx)) + UP * row_y_coords[r_idx])
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                t_color = RED if c_idx == 2 else (GREEN if c_idx == 1 else WHITE)
                lbl = create_text(cell_text, font_size=9, color=t_color).move_to(cell.get_center())
                
                row_group.add(VGroup(cell, lbl))
            comparison_table.add(row_group)

        self.play(FadeIn(comparison_table), run_time=1.8)
        self.wait(35.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(comparison_table),
            FadeOut(recap_title),
            FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(2.0)
        finish_voiceovers(self, voiceover_end)
