import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

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
def create_text(text, font_size=24, font="Segoe UI", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)

# Note: visual/narration alignment comment translated from Vietnamese.
def create_markup_text(text, font_size=24, font="Segoe UI", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)

# Note: visual/narration alignment comment translated from Vietnamese.
def get_propto(color=WHITE, stroke_width=2.0):
    propto = VMobject(color=color, stroke_width=stroke_width)
    propto.set_points_smoothly([
        RIGHT * 0.12 + UP * 0.08,
        ORIGIN + DOWN * 0.07,
        LEFT * 0.1 + DOWN * 0.07,
        LEFT * 0.15 + ORIGIN,
        LEFT * 0.1 + UP * 0.08,
        ORIGIN + UP * 0.08,
        RIGHT * 0.12 + DOWN * 0.09
    ])
    return propto


class Scene2_5(Scene):
    def construct(self):
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.camera.background_color = "#111111"

        # Voiceover audio is scheduled from actual MP3 durations.
        voiceover_end = 0.0
        voiceover_end = add_voiceover(self, "sc25_1.mp3", voiceover_end, 20.976)
        voiceover_end = add_voiceover(self, "sc25_2.mp3", voiceover_end, 20.846)
        voiceover_end = add_voiceover(self, "sc25_3.mp3", voiceover_end, 24.320)
        voiceover_end = add_voiceover(self, "sc25_4.mp3", voiceover_end, 28.447)
        voiceover_end = add_voiceover(self, "sc25_5.mp3", voiceover_end, 17.398)
        voiceover_end = add_voiceover(self, "sc25_6.mp3", voiceover_end, 17.084)
        voiceover_end = add_voiceover(self, "sc25_7.mp3", voiceover_end, 20.741)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        chapter_title = create_text("Sampling Adapters & Constrained decoding", font_size=24, color=YELLOW)
        chapter_sub = create_text("(Sampling Adapters & Constrained Decoding)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        sub_title = create_text("Sampling Adapters & Constrained decoding", font_size=16, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
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
        part1_title = create_text("1. Sampling adapters & Contrastive Decoding (Contrastive Decoding)", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part1_title), run_time=0.8)
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        intro_box = RoundedRectangle(width=11.6, height=3.8, color=BLUE_B, fill_color="#101720", fill_opacity=0.95, corner_radius=0.08).move_to(DOWN * 0.1)
        intro_title = create_text("Sampling adapters (Sampling Adapters)", font_size=13, color=BLUE_A, weight=BOLD).next_to(intro_box.get_top(), DOWN, buff=0.15)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        headers = VGroup(
            create_markup_text("<b>Method</b>", font_size=9.5, color=YELLOW),
            create_markup_text("<b>Formula / Purpose</b>", font_size=9.5, color=YELLOW),
            create_markup_text("<b>Adapter Type</b>", font_size=9.5, color=YELLOW)
        )
        headers[0].move_to(LEFT * 4.6 + UP * 1.0, aligned_edge=LEFT)
        headers[1].move_to(LEFT * 1.4 + UP * 1.0, aligned_edge=LEFT)
        headers[2].move_to(RIGHT * 2.3 + UP * 1.0, aligned_edge=LEFT)
        
        rows = VGroup()
        row_y_starts = 0.6
        row_spacing = 0.36
        
        table_data = [
            ("Typical sampling", "y ~ q(p<sub>θ</sub>)", "Truncation (entropy)"),
            ("Mirostat decoding", "Target perplexity", "Truncation (adaptive top-k)"),
            ("Basis-aware sampling", "y ~ q(p<sub>θ</sub>)", "Truncation (linear program)"),
            ("Contrastive decoding", "y ~ q(p<sub>θ</sub>) | log p<sub>θ'</sub> - log p<sub>θ</sub>", "Contrastive & truncation"),
            ("DExperts", "y ~ q*(· | x, c) ∝ p<sub>θ</sub> · (p<sub>θ+</sub> / p<sub>θ-</sub>)<sup>α</sup>", "Logits adjustment"),
            ("Inference-time adapters", "y ~ q* ∝ r(y) ∝ (p<sub>θ</sub> · p<sub>θ'</sub>)<sup>α</sup>", "Logits adjustment"),
            ("Proxy tuning", "y ~ q*(· | x, c) ∝ p<sub>θ</sub> · (p<sub>θ+</sub> / p<sub>θ-</sub>)<sup>α</sup>", "Logits adjustment")
        ]
        
        for idx, (m, f, a) in enumerate(table_data):
            y_pos = row_y_starts - idx * row_spacing
            col1 = create_text(m, font_size=8.5, color=WHITE)
            col1.move_to(LEFT * 4.6 + UP * y_pos, aligned_edge=LEFT)
            
            col2 = create_markup_text(f, font_size=8.5, color=BLUE_A)
            col2.move_to(LEFT * 1.4 + UP * y_pos, aligned_edge=LEFT)
            
            col3 = create_text(a, font_size=8.5, color=GRAY_A)
            col3.move_to(RIGHT * 2.3 + UP * y_pos, aligned_edge=LEFT)
            
            rows.add(VGroup(col1, col2, col3))
            
        intro_group = VGroup(intro_box, intro_title, headers, rows)
        
        self.play(FadeIn(intro_group, shift=UP * 0.15), run_time=1.2)
        self.wait(10.0)
        self.play(FadeOut(intro_group), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        intro_text = create_text(
            "Contrastive Decoding combines a large model (Expert) and a small model (Anti-expert)\n"
            "to remove dull repeated words and sharpen the probability distribution.",
            font_size=13, color=WHITE
        ).move_to(UP * 1.5)
        self.play(Write(intro_text), run_time=2.0)
        self.wait(4.0)
        self.play(FadeOut(intro_text), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        tokens = ["smart", "repetitive", "the", "book", "is"]
        
        chart_expert_title = create_text("Expert Model (Large)", font_size=12, color=BLUE_A)
        chart_expert_title.move_to(LEFT * 3.5 + UP * 2.2)
        
        chart_anti_title = create_text("Anti-expert Model (Small)", font_size=12, color=ORANGE)
        chart_anti_title.move_to(LEFT * 3.5 + DOWN * 0.1)

        # Note: visual/narration alignment comment translated from Vietnamese.
        base_expert = Line(LEFT * 3.9 + UP * 0.38, LEFT * 0.3 + UP * 0.38, color=GRAY_D, stroke_width=1.5)
        # Note: visual/narration alignment comment translated from Vietnamese.
        base_anti = Line(LEFT * 3.9 + DOWN * 1.72, LEFT * 0.3 + DOWN * 1.72, color=GRAY_D, stroke_width=1.5)

        self.play(
            FadeIn(chart_expert_title), FadeIn(base_expert),
            FadeIn(chart_anti_title), FadeIn(base_anti),
            run_time=1.0
        )

        expert_bars = VGroup()
        anti_bars = VGroup()
        expert_probs = [0.45, 0.25, 0.15, 0.10, 0.05]
        anti_probs = [0.10, 0.50, 0.20, 0.15, 0.05]
        expert_colors = [BLUE_D, BLUE_D, BLUE_D, BLUE_D, BLUE_D]
        anti_colors = [ORANGE, ORANGE, ORANGE, ORANGE, ORANGE]

        expert_labels = VGroup()
        anti_labels = VGroup()

        for i, token in enumerate(tokens):
            x_pos = -4.8 + i * 0.7
            
            # Expert Bar
            h_exp = expert_probs[i] * 3.0
            bar_exp = Rectangle(
                width=0.35, height=max(h_exp, 0.05),
                color=expert_colors[i], fill_color=expert_colors[i], fill_opacity=0.8
            )
            bar_exp.move_to(LEFT * (3.5 - i * 0.7) + UP * (0.4 + h_exp/2.0))
            expert_bars.add(bar_exp)
            
            lbl_exp = create_text(token, font_size=9, color=WHITE)
            lbl_exp.next_to(bar_exp, DOWN, buff=0.1)
            expert_labels.add(lbl_exp)

            # Anti-expert Bar
            h_anti = anti_probs[i] * 3.0
            bar_anti = Rectangle(
                width=0.35, height=max(h_anti, 0.05),
                color=anti_colors[i], fill_color=anti_colors[i], fill_opacity=0.8
            )
            bar_anti.move_to(LEFT * (3.5 - i * 0.7) + DOWN * (1.7 - h_anti/2.0))
            anti_bars.add(bar_anti)

            lbl_anti = create_text(token, font_size=9, color=WHITE)
            lbl_anti.next_to(bar_anti, DOWN, buff=0.1)
            anti_labels.add(lbl_anti)

        self.play(
            LaggedStart(
                *[Create(b) for b in expert_bars], lag_ratio=0.1
            ),
            LaggedStart(
                *[Create(b) for b in anti_bars], lag_ratio=0.1
            ),
            run_time=1.5
        )
        self.play(Write(expert_labels), Write(anti_labels), run_time=1.0)
        self.wait(8.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        formula_box = RoundedRectangle(
            width=5.8, height=3.8, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1
        )
        formula_box.move_to(RIGHT * 3.4 + UP * 0.2)
        
        formula_title = create_text("Sampling formula", font_size=12, color=YELLOW)
        formula_title.next_to(formula_box.get_top(), DOWN, buff=0.2)
 
        # eq1: p(· | x) \propto p_expert(· | x) / p_antiexpert(· | x)
        eq1_lhs = create_markup_text("p(· | x) ∝ ", font_size=15, color=WHITE)
        eq1_num = create_markup_text("p<sub>expert</sub>(· | x)", font_size=12, color=BLUE_A)
        eq1_den = create_markup_text("p<sub>antiexpert</sub>(· | x)", font_size=12, color=ORANGE)
        
        w_line = max(eq1_num.width, eq1_den.width) * 0.5 + 0.1
        eq1_line = Line(LEFT * w_line, RIGHT * w_line, color=WHITE, stroke_width=1.5)
        
        eq1_line.next_to(eq1_lhs, RIGHT, buff=0.1)
        eq1_num.next_to(eq1_line, UP, buff=0.08)
        eq1_den.next_to(eq1_line, DOWN, buff=0.08)
        
        eq1 = VGroup(eq1_lhs, eq1_line, eq1_num, eq1_den)
        eq1.next_to(formula_title, DOWN, buff=0.25).shift(LEFT * 0.35)
 
        # eq2: log p_CD = log p_theta' - log p_theta
        eq2 = create_markup_text("log p<sub>CD</sub>(· | x) = log p<sub>θ'</sub>(· | x) - log p<sub>θ</sub>(· | x)", font_size=10, color=LIGHT_GREY)
        eq2.next_to(eq1, DOWN, buff=0.3)
 
        # Note: visual/narration alignment comment translated from Vietnamese.
        eq3 = create_markup_text("y ~ q* ∝ r(y) ∝ (p<sub>θ</sub> · p<sub>θ'</sub>)<sup>α</sup>", font_size=10, color=LIGHT_GREY)
        eq3.next_to(eq2, DOWN, buff=0.3)
 
        alpha_text = create_text(
            "CD (eq 1, 2) penalizes repeated tokens from the anti-expert.\n"
            "Inference-time adapters (eq 3) is orchestrated by r(y).",
            font_size=8.5, color=GRAY_A, line_spacing=1.3
        )
        alpha_text.next_to(eq3, DOWN, buff=0.25)
 
        self.play(
            FadeIn(formula_box),
            Write(formula_title),
            run_time=1.0
        )
        self.play(Write(eq1), run_time=1.0)
        self.wait(4.0)
        self.play(Write(eq2), run_time=1.2)
        self.play(Write(eq3), run_time=1.2)
        self.play(FadeIn(alpha_text, shift=UP * 0.1), run_time=0.8)
        self.wait(8.0)  # Note: visual/narration alignment comment translated from Vietnamese.
 
        # Note: visual/narration alignment comment translated from Vietnamese.
        chart_cd_title = create_text("Contrastive Distribution (Adjusted)", font_size=12, color=GREEN)
        chart_cd_title.move_to(RIGHT * 3.2 + UP * 1.8)
 
        # Note: visual/narration alignment comment translated from Vietnamese.
        base_cd = Line(RIGHT * 1.5 + DOWN * 1.22, RIGHT * 4.9 + DOWN * 1.22, color=GRAY_D, stroke_width=1.5)
        
        cd_probs = [0.83, 0.03, 0.06, 0.05, 0.03]
        cd_bars = VGroup()
        cd_labels = VGroup()
 
        for i, token in enumerate(tokens):
            h_cd = cd_probs[i] * 2.5
            bar_cd = Rectangle(
                width=0.35, height=max(h_cd, 0.05),
                color=GREEN, fill_color=GREEN, fill_opacity=0.8
            )
            bar_cd.move_to(RIGHT * (1.9 + i * 0.7) + DOWN * (1.2 - h_cd/2.0))
            cd_bars.add(bar_cd)
 
            lbl_cd = create_text(token, font_size=9, color=WHITE)
            lbl_cd.next_to(bar_cd, DOWN, buff=0.1)
            cd_labels.add(lbl_cd)
 
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(formula_box), FadeOut(formula_title),
            FadeOut(eq1), FadeOut(eq2), FadeOut(eq3), FadeOut(alpha_text),
            FadeIn(chart_cd_title), FadeIn(base_cd),
            run_time=1.0
        )
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        arrow_exp_rep = Arrow(start=LEFT*2.1 + UP*1.8, end=expert_bars[1].get_top(), color=RED, buff=0.1, stroke_width=3)
        arrow_anti_rep = Arrow(start=LEFT*2.1 + DOWN*0.8, end=anti_bars[1].get_top(), color=RED, buff=0.1, stroke_width=3)
        
        self.play(Create(arrow_exp_rep), Create(arrow_anti_rep), run_time=0.8)
        self.wait(5.0)
        self.play(FadeOut(arrow_exp_rep), FadeOut(arrow_anti_rep), run_time=0.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            LaggedStart(
                *[Create(b) for b in cd_bars], lag_ratio=0.1
            ),
            Write(cd_labels),
            run_time=1.5
        )
        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        comparison_box = RoundedRectangle(
            width=12.0, height=1.1, color=GRAY_E, fill_color="#141517", fill_opacity=0.9, corner_radius=0.08
        )
        comparison_box.move_to(DOWN * 3.0)

        text_normal = create_markup_text(
            "Typical: <i>\"The book is on the table and the table is...\"</i> <span color='#ff5555'>(Infinite repetition)</span>",
            font_size=11, color=LIGHT_GREY
        )
        text_normal.move_to(comparison_box.get_center() + UP * 0.22)

        text_cd = create_markup_text(
            "CD: <i>\"The book is on the table, which I read yesterday.\"</i> <span color='#55ff55'>(Sharp, diverse)</span>",
            font_size=11, color=LIGHT_GREY
        )
        text_cd.move_to(comparison_box.get_center() + DOWN * 0.22)

        self.play(FadeIn(comparison_box), run_time=0.8)
        self.play(Write(text_normal), run_time=1.5)
        self.wait(4.0)
        self.play(Write(text_cd), run_time=1.5)
        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(part1_title),
            FadeOut(chart_expert_title), FadeOut(base_expert),
            FadeOut(chart_anti_title), FadeOut(base_anti),
            FadeOut(expert_bars), FadeOut(anti_bars),
            FadeOut(expert_labels), FadeOut(anti_labels),
            FadeOut(chart_cd_title), FadeOut(base_cd),
            FadeOut(cd_bars), FadeOut(cd_labels),
            FadeOut(comparison_box), FadeOut(text_normal), FadeOut(text_cd),
            run_time=1.2
        )
        self.wait(2.0)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #
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
        part2_title = create_text("2. Constrained decoding (Constrained Decoding) & JSON state machine", font_size=13, color=GREEN)
        part2_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part2_title), run_time=0.8)
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        schema_box = RoundedRectangle(
            width=3.2, height=3.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08
        )
        schema_box.move_to(LEFT * 4.8 + UP * 0.8)

        schema_title = create_markup_text("<b>JSON Schema</b>", font_size=11, color=YELLOW)
        schema_title.next_to(schema_box.get_top(), DOWN, buff=0.15)

        schema_code = create_text(
            "{\n"
            '  "name": "string",\n'
            '  "birth year": "int"\n'
            "}",
            font_size=11, color=LIGHT_GREY, line_spacing=1.3
        )
        schema_code.next_to(schema_title, DOWN, buff=0.2)

        self.play(FadeIn(schema_box), Write(schema_title), Write(schema_code), run_time=1.2)
        self.wait(8.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        s0_pos = LEFT * 2.2 + UP * 1.8
        s1_pos = LEFT * 0.6 + UP * 1.8
        s2_pos = RIGHT * 1.0 + UP * 1.8
        s6_pos = RIGHT * 2.6 + UP * 1.8
        s4_pos = LEFT * 0.6 + UP * 0.0
        s7_pos = RIGHT * 1.0 + UP * 0.0
        s8_pos = RIGHT * 2.6 + UP * 0.0

        def make_node(label_text, pos, is_double=False):
            circle = Circle(radius=0.26, color=WHITE, stroke_width=2)
            circle.move_to(pos)
            lbl = create_text(label_text, font_size=9, color=WHITE)
            lbl.move_to(pos)
            if is_double:
                circle_in = Circle(radius=0.20, color=WHITE, stroke_width=1.5)
                circle_in.move_to(pos)
                return VGroup(circle, circle_in, lbl)
            return VGroup(circle, lbl)

        node0 = make_node("S0", s0_pos)
        node1 = make_node("S1", s1_pos)
        node2 = make_node("S2", s2_pos)
        node6 = make_node("S6", s6_pos)
        node4 = make_node("S4", s4_pos)
        node7 = make_node("S7", s7_pos)
        node8 = make_node("S8", s8_pos, is_double=True)

        nodes = VGroup(node0, node1, node2, node6, node4, node7, node8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        def make_arrow(start_pos, end_pos, label_text, edge_buff=0.27, label_side=UP, label_buff=0.12):
            arrow = Arrow(start=start_pos, end=end_pos, color=GRAY_A, stroke_width=1.5, buff=edge_buff, max_tip_length_to_length_ratio=0.15)
            lbl = create_text(label_text, font_size=7, color=GRAY_B)
            lbl.next_to(arrow, label_side, buff=label_buff)
            return VGroup(arrow, lbl)

        arr0_1 = make_arrow(s0_pos, s1_pos, "'{'", label_side=UP)
        arr1_2 = make_arrow(s1_pos, s2_pos, '"name": "', label_side=UP)
        arr2_6 = make_arrow(s2_pos, s6_pos, "[A-Za-z]", label_side=UP)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        loop6 = Arc(radius=0.15, start_angle=-30*DEGREES, angle=240*DEGREES, color=GRAY_A, stroke_width=1.5)
        loop6.next_to(node6, UP, buff=0.01).shift(RIGHT * 0.1)
        loop6_tip = ArrowTriangleFilledTip(color=GRAY_A).scale(0.12)
        loop6_tip.move_to(loop6.get_start()).rotate(-70*DEGREES)
        loop6_lbl = create_text("[A-Za-z]", font_size=6, color=GRAY_B).next_to(loop6, UP, buff=0.05)
        loop6_group = VGroup(loop6, loop6_tip, loop6_lbl)

        arr6_4 = make_arrow(s6_pos, s4_pos, '", "birth year": ', label_side=LEFT, label_buff=0.02)
        arr4_7 = make_arrow(s4_pos, s7_pos, "\\d", label_side=DOWN)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        loop7 = Arc(radius=0.15, start_angle=-30*DEGREES, angle=240*DEGREES, color=GRAY_A, stroke_width=1.5)
        loop7.next_to(node7, UP, buff=0.01).shift(RIGHT * 0.1)
        loop7_tip = ArrowTriangleFilledTip(color=GRAY_A).scale(0.12)
        loop7_tip.move_to(loop7.get_start()).rotate(-70*DEGREES)
        
        loop7.rotate(180 * DEGREES, about_point=s7_pos)
        loop7_tip.rotate(180 * DEGREES, about_point=s7_pos)
        
        loop7_lbl = create_text("\\d", font_size=6, color=GRAY_B).next_to(loop7, DOWN, buff=0.05)
        loop7_group = VGroup(loop7, loop7_tip, loop7_lbl)

        arr7_8 = make_arrow(s7_pos, s8_pos, "'}'", label_side=DOWN)

        arrows = VGroup(arr0_1, arr1_2, arr2_6, loop6_group, arr6_4, arr4_7, loop7_group, arr7_8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(FadeIn(nodes), FadeIn(arrows), run_time=1.5)
        self.wait(10.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        vocab_box = RoundedRectangle(
            width=3.6, height=4.2, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08
        )
        vocab_box.move_to(RIGHT * 5.0 + UP * 0.2)
        
        vocab_title = create_text("Vocabulary & Probabilities", font_size=11, color=YELLOW)
        vocab_title.next_to(vocab_box.get_top(), DOWN, buff=0.15)
        
        self.play(FadeIn(vocab_box), Write(vocab_title), run_time=1.0)
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        result_box = RoundedRectangle(
            width=12.5, height=1.0, color=GRAY_E, fill_color="#141517", fill_opacity=0.9, corner_radius=0.08
        )
        result_box.move_to(DOWN * 2.8)
        
        result_label = create_text("Generated JSON:", font_size=11, color=GRAY_B)
        result_label.move_to(result_box.get_left() + RIGHT * 1.2)
        
        self.play(FadeIn(result_box), FadeIn(result_label), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        current_node_highlight = Circle(radius=0.28, color=GREEN, stroke_width=3)
        current_node_highlight.move_to(s0_pos)
        self.play(Create(current_node_highlight), run_time=0.5)
        self.wait(8.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        def show_vocab_list(items, chosen_idx):
            # Note: visual/narration alignment comment translated from Vietnamese.
            list_group = VGroup()
            for i, (tok, pr, lg, valid) in enumerate(items):
                # Note: visual/narration alignment comment translated from Vietnamese.
                tok_color = GREEN if valid else RED
                tok_lbl = create_text(f"\"{tok}\"", font_size=10, color=tok_color)
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                if i == chosen_idx:
                    tok_lbl.set_color(YELLOW)
                    bg_highlight = BackgroundRectangle(tok_lbl, color=YELLOW, fill_opacity=0.15, buff=0.05)
                    item_v = VGroup(bg_highlight, tok_lbl)
                else:
                    item_v = VGroup(tok_lbl)
                
                pr_lbl = create_text(f"P: {pr}", font_size=9, color=WHITE if valid else RED)
                lg_lbl = create_text(f"Logit: {lg}", font_size=9, color=WHITE if valid else RED)
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                item_row = VGroup(item_v, pr_lbl, lg_lbl)
                item_row.arrange(RIGHT, buff=0.3)
                item_row.move_to(RIGHT * 5.0 + UP * (1.2 - i * 0.75))
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                if not valid:
                    strike_line = Line(
                        item_row.get_left() - LEFT*0.1, item_row.get_right() + LEFT*0.1,
                        color=RED_E, stroke_width=1.5
                    )
                    item_row.add(strike_line)
                
                list_group.add(item_row)
            return list_group

        # Note: visual/narration alignment comment translated from Vietnamese.
        current_json_text = ""
        json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        json_display.next_to(result_label, RIGHT, buff=0.3)
        self.add(json_display)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        vocab_items_1 = [
            ("\\n", "0.36", "1.20", False),
            ("\"", "0.16", "0.80", False),
            ("{", "0.026", "0.10", True),
            ("https", "0.025", "0.08", False)
        ]
        
        vocab_list_1 = show_vocab_list(vocab_items_1, chosen_idx=2)
        self.play(FadeIn(vocab_list_1), run_time=1.0)
        self.wait(10.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        current_json_text += "{"
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)
        
        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s1_pos),
            arr0_1[0].animate.set_color(GREEN),
            run_time=1.2
        )
        json_display = new_json_display
        self.wait(5.0)
        self.play(FadeOut(vocab_list_1), run_time=0.5)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        vocab_items_2 = [
            ("name\": \"", "0.31", "1.10", True),
            ("date\": \"", "0.069", "0.20", False),
            ("\"", "0.039", "0.12", False),
            ("id\": \"", "0.033", "0.10", False)
        ]

        vocab_list_2 = show_vocab_list(vocab_items_2, chosen_idx=0)
        self.play(FadeIn(vocab_list_2), run_time=1.0)
        self.wait(10.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        current_json_text += ' "name": "'
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)

        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s2_pos),
            arr1_2[0].animate.set_color(GREEN),
            run_time=1.2
        )
        json_display = new_json_display
        self.wait(5.0)
        self.play(FadeOut(vocab_list_2), run_time=0.5)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        vocab_items_3 = [
            ("Taylor Swift", "0.85", "2.10", True),
            ("1989", "0.01", "-0.90", False),
            ("The", "0.022", "0.05", False),
            ("...", "...", "...", False)
        ]

        vocab_list_3 = show_vocab_list(vocab_items_3, chosen_idx=0)
        self.play(FadeIn(vocab_list_3), run_time=1.0)
        self.wait(10.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        current_json_text += 'Taylor Swift'
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)

        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s6_pos),
            arr2_6[0].animate.set_color(GREEN),
            run_time=1.2
        )
        json_display = new_json_display
        self.wait(5.0)
        self.play(FadeOut(vocab_list_3), run_time=0.5)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        vocab_items_4 = [
            ("\", \"birth year\": ", "0.85", "2.10", True),
            ("\"", "0.024", "0.06", False),
            (",", "0.022", "0.05", False),
            ("},", "0.005", "-1.20", False)
        ]

        vocab_list_4 = show_vocab_list(vocab_items_4, chosen_idx=0)
        self.play(FadeIn(vocab_list_4), run_time=1.0)
        self.wait(10.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        current_json_text += '", "birth year": '
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)

        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s4_pos),
            arr6_4[0].animate.set_color(GREEN),
            run_time=1.2
        )
        json_display = new_json_display
        self.wait(5.0)
        self.play(FadeOut(vocab_list_4), run_time=0.5)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        vocab_items_5 = [
            ("1989", "0.02", "-0.20", True),
            ("\"", "0.46", "1.50", False),
            ("int", "0.041", "0.30", False),
            ("year", "0.008", "-1.10", False)
        ]

        vocab_list_5 = show_vocab_list(vocab_items_5, chosen_idx=0)
        self.play(FadeIn(vocab_list_5), run_time=1.0)
        self.wait(10.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        current_json_text += '1989'
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)

        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s7_pos),
            arr4_7[0].animate.set_color(GREEN),
            run_time=1.2
        )
        json_display = new_json_display
        self.wait(5.0)
        self.play(FadeOut(vocab_list_5), run_time=0.5)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        vocab_items_6 = [
            ("}", "0.34", "1.20", True),
            (",", "0.39", "1.30", False),
            ("},", "0.11", "0.40", False),
            ("...", "...", "...", False)
        ]

        vocab_list_6 = show_vocab_list(vocab_items_6, chosen_idx=0)
        self.play(FadeIn(vocab_list_6), run_time=1.0)
        self.wait(10.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        current_json_text += '}'
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)

        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s8_pos),
            arr7_8[0].animate.set_color(GREEN),
            run_time=1.2
        )
        json_display = new_json_display
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        success_flash = Circle(radius=0.36, color=GREEN, stroke_width=4).move_to(s8_pos)
        self.play(Create(success_flash), run_time=0.5)
        self.play(FadeOut(success_flash), run_time=0.5)
        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(part2_title),
            FadeOut(schema_box), FadeOut(schema_title), FadeOut(schema_code),
            FadeOut(nodes), FadeOut(arrows),
            FadeOut(vocab_box), FadeOut(vocab_title),
            FadeOut(result_box), FadeOut(result_label),
            FadeOut(json_display), FadeOut(current_node_highlight),
            FadeOut(vocab_list_6),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        side_effects_title = create_text("Side effects of Constrained decoding", font_size=13, color=BLUE_A)
        side_effects_title.next_to(sub_title, DOWN, buff=0.3)
        
        self.play(Write(side_effects_title), run_time=0.8)
        self.wait(1.5)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        slide_box = RoundedRectangle(
            width=8.0, height=3.5, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1
        )
        slide_box.move_to(ORIGIN)
        
        slide_header = create_text("Side effects of templated/constrained decoding", font_size=12, color=YELLOW)
        slide_header.next_to(slide_box.get_top(), DOWN, buff=0.2)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        bullet_speedup = create_markup_text(
            "• <span color='#55ff55'>Generation speedup</span>: Speeds up generation\n"
            "  (Automatically fills code spans with only one valid path)",
            font_size=11, color=WHITE
        )
        bullet_performance = create_markup_text(
            "• <span color='#ffaa55'>Reduced performance</span>: Reduced performance\n"
            "  (Because unnatural token boundaries are forced)",
            font_size=11, color=WHITE
        )
        
        bullets = VGroup(bullet_speedup, bullet_performance)
        bullets.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        bullets.next_to(slide_header, DOWN, buff=0.4).shift(LEFT * 0.5)
        
        self.play(
            FadeIn(slide_box),
            Write(slide_header),
            run_time=1.0
        )
        self.wait(2.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(Write(bullet_speedup), run_time=1.2)
        self.wait(4.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(Write(bullet_performance), run_time=1.2)
        self.wait(6.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(side_effects_title),
            FadeOut(slide_box),
            FadeOut(slide_header),
            FadeOut(bullets),
            run_time=1.0
        )
        self.wait(1.5)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        part3_title = create_text("3. Token Boundary Shift & Token Healing (Token Healing)", font_size=13, color=ORANGE)
        part3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part3_title), run_time=0.8)
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        prompt_title = create_text("Prompt ends with a forced prefix:", font_size=12, color=GRAY_A)
        prompt_title.move_to(UP * 1.6)
        
        prompt_val = create_text('"The URL is http:"', font_size=18, color=YELLOW)
        prompt_val.next_to(prompt_title, DOWN, buff=0.2)
        
        self.play(FadeIn(prompt_title), Write(prompt_val), run_time=1.0)
        self.wait(10.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        puzzle_label = create_text("Normal token segmentation (Boundary-shifted):", font_size=11, color=GRAY_B)
        puzzle_label.move_to(UP * 0.2 + LEFT * 2.5)
        self.play(FadeIn(puzzle_label), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        def make_block(text, width, pos, color=BLUE_D):
            rect = RoundedRectangle(
                width=width, height=0.6, corner_radius=0.08,
                color=color, fill_color=color, fill_opacity=0.8
            )
            rect.move_to(pos)
            lbl = create_text(text, font_size=10, color=WHITE)
            lbl.move_to(pos)
            return VGroup(rect, lbl)

        # Note: visual/narration alignment comment translated from Vietnamese.
        b1 = make_block("The", 0.8, LEFT * 3.5 + DOWN * 0.4)
        b2 = make_block(" URL", 0.9, LEFT * 2.6 + DOWN * 0.4)
        b3 = make_block(" is", 0.7, LEFT * 1.75 + DOWN * 0.4)
        b4 = make_block(" http", 1.0, LEFT * 0.85 + DOWN * 0.4)
        b5 = make_block(":", 0.45, RIGHT * 0.0 + DOWN * 0.4, color=RED)

        blocks_group_1 = VGroup(b1, b2, b3, b4, b5)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=UP * 0.15) for b in blocks_group_1], lag_ratio=0.15
            ),
            run_time=1.5
        )
        self.wait(6.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        b_next_wrong = make_block("//", 0.7, RIGHT * 0.9 + DOWN * 0.4, color=RED_E)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        warning_icon = create_markup_text(
            "<b>[!] Segmentation error</b>\nToken sequence <i>[http] + [:] + [//]</i> never appeared during pretraining!",
            font_size=9, color=RED
        )
        warning_icon.next_to(b_next_wrong, RIGHT, buff=0.4).shift(UP * 0.2)

        self.play(FadeIn(b_next_wrong, shift=LEFT * 0.15), run_time=0.8)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        warn_border = RoundedRectangle(width=2.5, height=1.0, color=RED, stroke_width=2.5).move_to(RIGHT * 0.55 + DOWN * 0.4)
        self.play(Create(warn_border), FadeIn(warning_icon), run_time=0.8)
        self.wait(12.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(b_next_wrong), FadeOut(warn_border), FadeOut(warning_icon),
            run_time=0.8
        )
        self.wait(1.0)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        healing_label = create_text("Token Healing solution (Boundary healing):", font_size=11, color=GREEN)
        healing_label.move_to(UP * 0.2 + LEFT * 2.5)

        self.play(
            ReplacementTransform(puzzle_label, healing_label),
            run_time=1.0
        )
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            b5[0].animate.set_color(WHITE).set_opacity(0.3),
            run_time=0.8
        )
        self.wait(2.0)
        self.play(FadeOut(b5), run_time=0.6)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        prompt_val_healed = create_text('"The URL is http"', font_size=18, color=GREEN)
        prompt_val_healed.move_to(prompt_val.get_center())
        
        self.play(
            ReplacementTransform(prompt_val, prompt_val_healed),
            run_time=1.0
        )
        self.wait(8.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        candidates_box = RoundedRectangle(
            width=5.0, height=2.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08
        )
        candidates_box.move_to(RIGHT * 3.5 + DOWN * 0.4)

        cand_title = create_text("Candidates in Vocabulary", font_size=10, color=YELLOW)
        cand_title.next_to(candidates_box.get_top(), DOWN, buff=0.15)

        cand_1 = create_markup_text("s:// <span color='#ffaa55'>(Filtered out: does not match ':')</span>", font_size=9, color=WHITE)
        cand_1.next_to(cand_title, DOWN, buff=0.25).align_to(cand_title, LEFT).shift(LEFT * 0.5)

        cand_2 = create_markup_text("<b>://</b> <span color='#55ff55'>(Matches ':')</span>", font_size=9, color=WHITE)
        cand_2.next_to(cand_1, DOWN, buff=0.2).align_to(cand_1, LEFT)

        self.play(
            FadeIn(candidates_box), Write(cand_title),
            Write(cand_1), Write(cand_2),
            run_time=1.2
        )
        self.wait(6.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        strike_cand1 = Line(
            cand_1.get_left(), cand_1.get_right(), color=RED, stroke_width=1.5
        )
        self.play(
            Create(strike_cand1),
            cand_1.animate.set_opacity(0.4),
            run_time=0.8
        )
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        b_next_healed = make_block("://", 0.7, RIGHT * 0.12 + DOWN * 0.4, color=GREEN)
        self.play(
            cand_2.animate.set_color(YELLOW),
            FadeIn(b_next_healed, shift=LEFT * 0.1),
            run_time=0.8
        )
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(candidates_box), FadeOut(cand_title),
            FadeOut(cand_1), FadeOut(cand_2), FadeOut(strike_cand1),
            run_time=0.8
        )

        # Note: visual/narration alignment comment translated from Vietnamese.
        success_label = create_text("Perfect token boundary (The model understands correctly)", font_size=12, color=GREEN)
        success_label.move_to(DOWN * 1.3)
        
        self.play(Write(success_label), run_time=1.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        flash_rect = RoundedRectangle(width=4.5, height=0.8, color=GREEN, stroke_width=2.5).move_to(LEFT * 1.6 + DOWN * 0.4)
        self.play(Create(flash_rect), run_time=0.6)
        self.play(FadeOut(flash_rect), run_time=0.6)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        regularization_note = create_markup_text(
            "<span color='#88bbff'>Other solution:</span> Tokenizer regularization during training [Kudo, 2018]",
            font_size=11, color=LIGHT_GREY
        )
        regularization_note.move_to(DOWN * 2.2)
        
        self.play(Write(regularization_note), run_time=1.2)
        self.wait(8.0)  # Note: visual/narration alignment comment translated from Vietnamese.

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        self.play(
            FadeOut(part3_title), FadeOut(prompt_title), FadeOut(prompt_val_healed),
            FadeOut(healing_label), FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b4),
            FadeOut(b_next_healed), FadeOut(success_label), FadeOut(regularization_note), FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(2.0)
        finish_voiceovers(self, voiceover_end)
