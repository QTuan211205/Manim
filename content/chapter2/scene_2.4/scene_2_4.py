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

# Note: visual/narration alignment comment translated from Vietnamese.
def create_p_theta(vars_text, font_size=20, color=WHITE, theta_color=BLUE_A):
    p_text = create_text("p", font_size=font_size, color=theta_color)
    open_paren = create_text("(", font_size=font_size, color=color)
    open_paren.next_to(p_text, RIGHT, buff=0.18)
    
    vars_m = create_markup_text(vars_text, font_size=font_size)
    vars_m.next_to(open_paren, RIGHT, buff=0.03)
    
    close_paren = create_text(")", font_size=font_size, color=color)
    close_paren.next_to(vars_m, RIGHT, buff=0.03)
    
    theta_sub = get_theta(color=theta_color, stroke_width=1.2).scale(font_size / 50.0)
    theta_sub.next_to(p_text.get_corner(DOWN + RIGHT), RIGHT, buff=0.01).shift(DOWN * (font_size * 0.002))
    
    return VGroup(p_text, theta_sub, open_paren, vars_m, close_paren)


class Scene2_4(MovingCameraScene):
    def construct(self):
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.camera.background_color = "#111111"

        # Voiceover audio is scheduled from actual MP3 durations.
        voiceover_end = 0.0
        voiceover_end = add_voiceover(self, "sc24_1.mp3", voiceover_end, 17.398)
        voiceover_end = add_voiceover(self, "sc24_2.mp3", voiceover_end, 15.961)
        voiceover_end = add_voiceover(self, "sc24_3.mp3", voiceover_end, 18.991)
        voiceover_end = add_voiceover(self, "sc24_4.mp3", voiceover_end, 19.775)
        voiceover_end = add_voiceover(self, "sc24_5.mp3", voiceover_end, 32.679)
        voiceover_end = add_voiceover(self, "sc24_6.mp3", voiceover_end, 18.469)
        voiceover_end = add_voiceover(self, "sc24_7.mp3", voiceover_end, 14.341)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        chapter_title = create_text("Sampling & Truncation", font_size=24, color=YELLOW)
        chapter_sub = create_text("(Sampling & Truncation)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        sub_title = create_text("Sampling & Truncation (Top-k vs. Top-p & Temperature)", font_size=16, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(1.0)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step1_title = create_text("1. Ancestral Sampling (Ancestral Sampling) & Heavy Tail", font_size=13, color=BLUE_A)
        step1_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step1_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        y_t_sim = create_markup_text("y<sub><i>t</i></sub> ~ ", font_size=20, color=YELLOW)
        p_t_term = create_p_theta("· | <i>x</i>, <i>y</i><sub>&lt;<i>t</i></sub>", font_size=20)
        p_t_term.next_to(y_t_sim, RIGHT, buff=0.1)
        ancestral_step = VGroup(y_t_sim, p_t_term)
        ancestral_step.move_to(UP * 0.7 + LEFT * 3.0)

        lhs = create_p_theta("<i>y</i>", font_size=18)
        eq_sign = create_text(" = ", font_size=18)
        eq_sign.next_to(lhs, RIGHT, buff=0.1)
        p1 = create_p_theta("<i>y</i><sub>1</sub>", font_size=18)
        p1.next_to(eq_sign, RIGHT, buff=0.1)
        p2 = create_p_theta("<i>y</i><sub>2</sub> | <i>y</i><sub>1</sub>", font_size=18)
        p2.next_to(p1, RIGHT, buff=0.08)
        dots = create_text(" ... ", font_size=18)
        dots.next_to(p2, RIGHT, buff=0.08)
        pT = create_p_theta("<i>y</i><sub><i>T</i></sub> | <i>y</i><sub>&lt;<i>T</i></sub>", font_size=18)
        pT.next_to(dots, RIGHT, buff=0.08)
        ancestral_seq = VGroup(lhs, eq_sign, p1, p2, dots, pT)
        ancestral_seq.move_to(UP * 0.7 + RIGHT * 2.2)

        self.play(
            FadeIn(ancestral_step, shift=RIGHT * 0.15),
            FadeIn(ancestral_seq, shift=LEFT * 0.15),
            run_time=1.2
        )
        self.wait(2.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        tail_explain = create_text(
            "What is wrong with ancestral sampling?\n"
            "• Greedy decoding causes repetition traps\n"
            "• But ancestral sampling causes incoherence. Why?\n"
            "  - Low-probability tokens are too likely\n"
            "  - I.e., the next-token distribution has a heavy tail.",
            font_size=11, line_spacing=0.5
        )
        tail_explain.move_to(DOWN * 1.2)
        
        self.play(FadeIn(tail_explain, shift=UP * 0.15), run_time=1.0)
        self.wait(5.0)
        
        # Clear the screen to show comparison
        comp_title = create_text("Text generation behavior of decoding methods", font_size=13, color=BLUE_A)
        comp_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(
            FadeOut(ancestral_step),
            FadeOut(ancestral_seq),
            FadeOut(tail_explain),
            ReplacementTransform(step1_title, comp_title),
            run_time=1.0
        )
        self.wait(0.5)
        
        # 3 containers
        box_y = -0.5
        box_greedy = RoundedRectangle(width=4.1, height=3.5, color=RED_D, fill_color="#240d0d", fill_opacity=0.9, corner_radius=0.08)
        box_greedy.move_to(LEFT * 4.3 + UP * box_y)
        
        box_ancestral = RoundedRectangle(width=4.1, height=3.5, color=ORANGE, fill_color="#24160d", fill_opacity=0.9, corner_radius=0.08)
        box_ancestral.move_to(ORIGIN + UP * box_y)
        
        box_topk = RoundedRectangle(width=4.1, height=3.5, color=GREEN_D, fill_color="#0d2413", fill_opacity=0.9, corner_radius=0.08)
        box_topk.move_to(RIGHT * 4.3 + UP * box_y)
        
        # Titles for boxes
        title_greedy = create_markup_text("<b>Greedy Decoding</b>\n<span color='#ffaa55'>(Repetition trap - Repetitive)</span>", font_size=10, color=RED_A)
        title_greedy.next_to(box_greedy.get_top(), DOWN, buff=0.2)
        
        title_ancestral = create_markup_text("<b>Ancestral Sampling</b>\n<span color='#ffaa55'>(Incoherent - Incoherent)</span>", font_size=10, color=ORANGE)
        title_ancestral.next_to(box_ancestral.get_top(), DOWN, buff=0.2)
        
        title_topk = create_markup_text("<b>Top-k Truncation</b>\n<span color='#55ff55'>(Acceptable - Acceptable)</span>", font_size=10, color=GREEN_A)
        title_topk.next_to(box_topk.get_top(), DOWN, buff=0.2)
        
        # Text inside boxes
        txt_greedy = create_text(
            "\"Taylor Swift is a former\n"
            "contestant on the reality\n"
            "show... I think it's a very\n"
            "sad day for the show, he\n"
            "said. It's a very sad day\n"
            "for the show...\"",
            font_size=9, color=WHITE
        ).next_to(title_greedy, DOWN, buff=0.2)
        
        txt_ancestral = create_text(
            "\"Taylor Swift is a huge\n"
            "fan of her latest album\n"
            "'Famous.' The singer got\n"
            "her first reaction when\n"
            "she uploaded to Twitter\n"
            "... Beyonce.\"",
            font_size=9, color=WHITE
        ).next_to(title_ancestral, DOWN, buff=0.2)
        
        txt_topk = create_text(
            "\"Taylor Swift is a writer\n"
            "for IGN and a member of\n"
            "IGN's Television Critics\n"
            "Association. You can\n"
            "follow her on Twitter at\n"
            "@_MsSwift...\"",
            font_size=9, color=WHITE
        ).next_to(title_topk, DOWN, buff=0.2)
        
        self.play(
            FadeIn(box_greedy), Write(title_greedy), Write(txt_greedy),
            FadeIn(box_ancestral), Write(title_ancestral), Write(txt_ancestral),
            FadeIn(box_topk), Write(title_topk), Write(txt_topk),
            run_time=1.5
        )
        self.wait(6.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        trunc_title = create_text("Distribution truncation methods (Truncation)", font_size=13, color=BLUE_A)
        trunc_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(
            FadeOut(box_greedy), FadeOut(title_greedy), FadeOut(txt_greedy),
            FadeOut(box_ancestral), FadeOut(title_ancestral), FadeOut(txt_ancestral),
            FadeOut(box_topk), FadeOut(title_topk), FadeOut(txt_topk),
            ReplacementTransform(comp_title, trunc_title),
            run_time=1.0
        )
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        trunc_box = RoundedRectangle(width=9.5, height=3.6, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        trunc_box.move_to(DOWN * 0.5)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        header_method = create_markup_text("<b>Method (Method)</b>", font_size=11, color=YELLOW)
        header_strategy = create_markup_text("<b>Threshold strategy (Threshold strategy)</b>", font_size=11, color=YELLOW)
        
        header_method.move_to(LEFT * 3.5 + UP * 0.8, aligned_edge=LEFT)
        header_strategy.move_to(LEFT * 0.5 + UP * 0.8, aligned_edge=LEFT)
        
        row_data = [
            ("Top-k", "Sample from the k highest-probability tokens"),
            ("Top-p (Nucleus)", "Cumulative probability reaches at most p"),
            ("Epsilon (ε)", "Token probability is greater than threshold epsilon"),
            ("Eta (η)", "Minimum probability threshold proportional to entropy"),
            ("Min-p", "Minimum probability proportional to the highest token probability")
        ]
        
        rows_group = VGroup()
        for idx, (method, strategy) in enumerate(row_data):
            y_pos = 0.3 - idx * 0.45
            m_txt = create_text(method, font_size=10, color=BLUE_C)
            m_txt.move_to(LEFT * 3.5 + UP * y_pos, aligned_edge=LEFT)
            
            s_txt = create_text(strategy, font_size=10, color=WHITE)
            s_txt.move_to(LEFT * 0.5 + UP * y_pos, aligned_edge=LEFT)
            
            rows_group.add(VGroup(m_txt, s_txt))
            
        self.play(
            FadeIn(trunc_box),
            FadeIn(header_method),
            FadeIn(header_strategy),
            Write(rows_group),
            run_time=1.5
        )
        self.wait(8.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(trunc_title),
            FadeOut(trunc_box),
            FadeOut(header_method),
            FadeOut(header_strategy),
            FadeOut(rows_group),
            run_time=1.0
        )
        self.wait(0.5)


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
        step2_title = create_text("2. Adjust the distribution with Temperature (Temperature)", font_size=13, color=BLUE_A)
        step2_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step2_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        temp_formula_box = RoundedRectangle(width=6.0, height=1.4, color=GREEN_E, fill_color="#0d2417", fill_opacity=0.4, corner_radius=0.08)
        temp_formula_box.move_to(UP * 1.8)
        
        # Build Softmax formula manually to format as fraction
        lhs = create_markup_text("Softmax(z, τ)<sub>i</sub> = ", font_size=20, color="#8fbcbb")
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        num_e = create_text("e", font_size=20, color=YELLOW)
        num_pow = create_markup_text("z<sub>i</sub>/τ", font_size=13, color=YELLOW)
        num_pow.next_to(num_e.get_corner(UP + RIGHT), RIGHT, buff=0.01).shift(UP * 0.03)
        numerator = VGroup(num_e, num_pow)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        sigma = get_sigma(color="#88c0d0", stroke_width=1.5).scale(0.65)
        j_sub_sigma = create_text("j", font_size=12, color="#88c0d0")
        j_sub_sigma.next_to(sigma, DOWN, buff=0.04)
        
        den_e = create_text("e", font_size=20, color="#88c0d0")
        den_pow = create_markup_text("z<sub>j</sub>/τ", font_size=13, color="#88c0d0")
        den_pow.next_to(den_e.get_corner(UP + RIGHT), RIGHT, buff=0.01).shift(UP * 0.03)
        den_term = VGroup(den_e, den_pow)
        den_term.next_to(sigma, RIGHT, buff=0.1)
        denominator = VGroup(sigma, j_sub_sigma, den_term)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        fraction_line = Line(LEFT * 0.6, RIGHT * 0.6, color=WHITE, stroke_width=1.5)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        numerator.move_to(UP * 0.35)
        fraction_line.move_to(ORIGIN)
        denominator.move_to(DOWN * 0.35)
        
        fraction = VGroup(numerator, fraction_line, denominator)
        fraction.next_to(lhs, RIGHT, buff=0.15)
        
        temp_formula = VGroup(lhs, fraction)
        temp_formula.move_to(temp_formula_box.get_center())

        self.play(
            FadeIn(temp_formula_box),
            Write(temp_formula),
            run_time=1.0
        )
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        slider_line = Line(LEFT * 2.5 + DOWN * 2.5, RIGHT * 2.5 + DOWN * 2.5, color=GRAY, stroke_width=3.0)
        slider_lbl = create_text("Temperature τ = 1.0", font_size=11, color=YELLOW)
        slider_lbl.move_to(DOWN * 2.1)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        temp_tracker = ValueTracker(1.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        def get_slider_x(val):
            return -2.5 + (val - 0.2) / (2.0 - 0.2) * 5.0

        slider_handle = always_redraw(lambda: Dot(
            point=np.array([get_slider_x(temp_tracker.get_value()), -2.5, 0]), 
            radius=0.12, 
            color=YELLOW
        ))
        
        slider_text = always_redraw(lambda: create_text(
            f"Temperature τ = {temp_tracker.get_value():.1f}", 
            font_size=11, 
            color=YELLOW
        ).move_to(DOWN * 2.1))

        self.play(
            Create(slider_line),
            FadeIn(slider_handle),
            FadeIn(slider_text),
            run_time=0.8
        )
        self.wait(1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        logits = [3.0, 2.2, 1.5, 0.5, 0.2]
        words = ["a", "the", "an", "not", "one"]
        colors = [BLUE_D, GRAY_C, GRAY_C, RED_D, RED_E]
        chart_base_y = -1.6
        
        def get_dynamic_bars():
            temp = temp_tracker.get_value()
            scaled_logits = [l / temp for l in logits]
            # Note: visual/narration alignment comment translated from Vietnamese.
            scaled_logits = [np.clip(sl, -50.0, 50.0) for sl in scaled_logits]
            exp_logits = [np.exp(sl) for sl in scaled_logits]
            sum_exp = sum(exp_logits)
            probs = [el / sum_exp for el in exp_logits]
            
            bars_group = VGroup()
            for idx, p in enumerate(probs):
                x_pos = -3.0 + idx * 1.5
                height = p * 1.8
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                rect = Rectangle(
                    width=0.6, 
                    height=max(height, 0.05), 
                    color=colors[idx], 
                    fill_color=colors[idx], 
                    fill_opacity=0.85,
                    stroke_width=1.0
                )
                rect.move_to(np.array([x_pos, chart_base_y + max(height, 0.05)/2.0, 0]))
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                lbl = create_text(f'"{words[idx]}"', font_size=9, color=WHITE)
                lbl.move_to(np.array([x_pos, chart_base_y - 0.25, 0]))
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                val = create_text(f"{p*100:.0f}%", font_size=8.5, color=colors[idx])
                val.move_to(np.array([x_pos, chart_base_y + max(height, 0.05) + 0.18, 0]))
                
                bars_group.add(VGroup(rect, lbl, val))
            return bars_group

        dynamic_chart = always_redraw(get_dynamic_bars)
        
        self.play(FadeIn(dynamic_chart), run_time=1.0)
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        info_txt = create_text("τ = 2.0 (High): Flat distribution, diverse but prone to incoherence", font_size=10, color=GRAY_A)
        info_txt.move_to(UP * 0.9)
        
        self.play(
            temp_tracker.animate.set_value(2.0),
            FadeIn(info_txt, shift=UP * 0.1),
            run_time=2.0
        )
        self.wait(3.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            temp_tracker.animate.set_value(1.0),
            FadeOut(info_txt),
            run_time=1.5
        )
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        info_txt2 = create_text("τ = 0.2 (Low): Sharp distribution, high confidence but prone to repetition (Greedy)", font_size=10, color=GRAY_A)
        info_txt2.move_to(UP * 0.9)
        
        self.play(
            temp_tracker.animate.set_value(0.2),
            FadeIn(info_txt2, shift=UP * 0.1),
            run_time=2.5
        )
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            temp_tracker.animate.set_value(1.0),
            FadeOut(info_txt2),
            run_time=1.5
        )
        self.wait(0.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.remove(dynamic_chart, slider_handle, slider_text)
        self.play(
            FadeOut(temp_formula_box),
            FadeOut(temp_formula),
            FadeOut(slider_line),
            run_time=1.0
        )
        temp_table_title = create_text("Comparison table for the effect of Temperature", font_size=13, color=BLUE_A)
        temp_table_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(
            ReplacementTransform(step2_title, temp_table_title),
            run_time=0.8
        )
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        table_box = RoundedRectangle(width=8.5, height=2.8, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        table_box.move_to(DOWN * 0.5)
        
        h_param = create_markup_text("<b>Temperature (Parameter)</b>", font_size=11, color=YELLOW)
        h_pro = create_markup_text("<b>Pros (Pro)</b>", font_size=11, color=YELLOW)
        h_con = create_markup_text("<b>Cons (Con)</b>", font_size=11, color=YELLOW)
        
        h_param.move_to(LEFT * 2.5 + UP * 0.5)
        h_pro.move_to(ORIGIN + UP * 0.5)
        h_con.move_to(RIGHT * 2.5 + UP * 0.5)
        
        row_high = VGroup(
            create_text("High (High τ ≥ 1.0)", font_size=10, color=BLUE_C).move_to(LEFT * 2.5 + DOWN * 0.1),
            create_text("Diverse (Diverse)", font_size=10, color=GREEN_C).move_to(ORIGIN + DOWN * 0.1),
            create_text("Incoherent (Incoherent)", font_size=10, color=RED_C).move_to(RIGHT * 2.5 + DOWN * 0.1)
        )
        
        row_low = VGroup(
            create_text("Low (Low τ < 1.0)", font_size=10, color=BLUE_C).move_to(LEFT * 2.5 + DOWN * 0.7),
            create_text("Coherent (Coherent)", font_size=10, color=GREEN_C).move_to(ORIGIN + DOWN * 0.7),
            create_text("Repetitive (Repetitive)", font_size=10, color=RED_C).move_to(RIGHT * 2.5 + DOWN * 0.7)
        )
        
        self.play(
            FadeIn(table_box),
            FadeIn(h_param), FadeIn(h_pro), FadeIn(h_con),
            Write(row_high), Write(row_low),
            run_time=1.5
        )
        self.wait(6.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(temp_table_title),
            FadeOut(table_box),
            FadeOut(h_param), FadeOut(h_pro), FadeOut(h_con),
            FadeOut(row_high), FadeOut(row_low),
            run_time=1.0
        )
        self.wait(0.5)


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
        step3_title = create_text("3. Truncate the distribution: Top-k vs. Top-p (Nucleus)", font_size=13, color=BLUE_A)
        step3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step3_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        sharp_words = ["is", ",", "and", "has", "here", "?", "means", "in"]
        sharp_probs = [0.68, 0.15, 0.05, 0.02, 0.01, 0.01, 0.01, 0.01]
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        flat_words = [",", "and", "is", "(", "\\n", "said", "in", "had"]
        flat_probs = [0.12, 0.11, 0.10, 0.09, 0.08, 0.08, 0.07, 0.07]

        # Note: visual/narration alignment comment translated from Vietnamese.
        left_container = RoundedRectangle(width=5.8, height=4.2, color=BLUE_E, fill_color="#0e1726", fill_opacity=0.3, corner_radius=0.08)
        left_container.move_to(LEFT * 3.3 + DOWN * 0.6)
        left_title = create_text("Sharp distribution (Sharp) \"Taylor Swift is\"", font_size=9, color=BLUE_C)
        left_title.next_to(left_container.get_top(), DOWN, buff=0.15)
        left_group = VGroup(left_container, left_title)

        right_container = RoundedRectangle(width=5.8, height=4.2, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.7, corner_radius=0.08)
        right_container.move_to(RIGHT * 3.3 + DOWN * 0.6)
        right_title = create_text("Flat distribution (Flat) \"My name\"", font_size=9, color=GRAY_B)
        right_title.next_to(right_container.get_top(), DOWN, buff=0.15)
        right_group = VGroup(right_container, right_title)

        self.play(
            FadeIn(left_group, shift=RIGHT * 0.15),
            FadeIn(right_group, shift=LEFT * 0.15),
            run_time=1.0
        )
        self.wait(1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        def get_vocab_list(words, probs, center_x, chart_color):
            list_group = VGroup()
            start_y = 0.7
            spacing = 0.4
            
            bars_list = []
            for idx in range(8):
                y_pos = start_y - idx * spacing
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                lbl = create_text(f'"{words[idx]}"', font_size=9.5, color=WHITE)
                lbl.move_to(np.array([center_x - 2.1, y_pos, 0]), aligned_edge=LEFT)
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                # Note: visual/narration alignment comment translated from Vietnamese.
                bar_len = probs[idx] * 2.5 + 0.05
                bar = RoundedRectangle(
                    width=bar_len, 
                    height=0.22, 
                    color=chart_color, 
                    fill_color=chart_color, 
                    fill_opacity=0.9, 
                    corner_radius=0.02
                )
                bar.next_to(lbl, RIGHT, buff=0.2)
                bars_list.append(bar)
                
                # Note: visual/narration alignment comment translated from Vietnamese.
                val = create_text(f"{probs[idx]*100:.0f}%", font_size=9, color=chart_color)
                val.next_to(bar, RIGHT, buff=0.12)
                
                row = VGroup(lbl, bar, val)
                list_group.add(row)
            return list_group, bars_list

        sharp_list, sharp_bars = get_vocab_list(sharp_words, sharp_probs, -3.3, BLUE_C)
        flat_list, flat_bars = get_vocab_list(flat_words, flat_probs, 3.3, GRAY_C)

        self.play(
            FadeIn(sharp_list, shift=UP * 0.1),
            FadeIn(flat_list, shift=UP * 0.1),
            run_time=1.2
        )
        self.wait(2.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        topk_txt = create_text("Top-K (K = 5): Fixed number of selected words", font_size=11, color=YELLOW)
        topk_txt.next_to(step3_title, DOWN, buff=0.15)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        cut_y = 0.7 - 4.5 * 0.4
        cut_line_left = Line(LEFT * 5.9 + UP * cut_y, LEFT * 0.7 + UP * cut_y, color=RED, stroke_width=2.0)
        cut_line_right = Line(RIGHT * 0.7 + UP * cut_y, RIGHT * 5.9 + UP * cut_y, color=RED, stroke_width=2.0)
        
        lbl_k_left = create_text("K=5", font_size=8.5, color=RED).next_to(cut_line_left, UP, buff=0.05, aligned_edge=RIGHT)
        lbl_k_right = create_text("K=5", font_size=8.5, color=RED).next_to(cut_line_right, UP, buff=0.05, aligned_edge=RIGHT)

        self.play(
            Write(topk_txt),
            Create(cut_line_left),
            Create(cut_line_right),
            FadeIn(lbl_k_left),
            FadeIn(lbl_k_right),
            run_time=1.0
        )
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        play_fade_tail = []
        for idx in range(5, 8):
            play_fade_tail.append(sharp_list[idx].animate.set_opacity(0.25))
            play_fade_tail.append(flat_list[idx].animate.set_opacity(0.25))
        self.play(*play_fade_tail, run_time=0.8)
        self.wait(2.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        highlight_box = RoundedRectangle(width=5.2, height=0.96, color=RED_D, fill_color=RED, fill_opacity=0.1, corner_radius=0.06)
        highlight_box.move_to(RIGHT * 3.3 + DOWN * 1.72)
        
        problem_txt = create_text("Wasteful: \"said\", \"in\", \"had\" are removed despite similar probabilities!", font_size=9, color=RED_A)
        problem_txt.next_to(right_container, DOWN, buff=0.15)

        self.play(
            Create(highlight_box),
            Write(problem_txt),
            run_time=0.8
        )
        self.wait(4.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        play_restore = []
        for idx in range(5, 8):
            play_restore.append(sharp_list[idx].animate.set_opacity(1.0))
            play_restore.append(flat_list[idx].animate.set_opacity(1.0))
            
        self.play(
            FadeOut(topk_txt),
            FadeOut(cut_line_left),
            FadeOut(cut_line_right),
            FadeOut(lbl_k_left),
            FadeOut(lbl_k_right),
            FadeOut(highlight_box),
            FadeOut(problem_txt),
            *play_restore,
            run_time=1.0
        )
        self.wait(0.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        topp_txt = create_text("Top-P (p = 0.90): Cumulative probability (Flexible dynamic threshold)", font_size=11, color=GREEN_A)
        topp_txt.next_to(step3_title, DOWN, buff=0.15)
        self.play(Write(topp_txt), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        sharp_box = RoundedRectangle(width=5.3, height=1.6, color=GREEN_C, fill_color=GREEN, fill_opacity=0.1, corner_radius=0.06)
        sharp_box.move_to(LEFT * 3.3 + UP * 0.1)
        sharp_box_lbl = create_text("Cumulative = 90% (Keep 4 words)", font_size=8.5, color=GREEN_A)
        sharp_box_lbl.move_to(np.array([-3.3, -2.55, 0]))
        
        play_fade_sharp_tail = []
        for idx in range(4, 8):
            play_fade_sharp_tail.append(sharp_list[idx].animate.set_opacity(0.25))

        self.play(
            Create(sharp_box),
            Write(sharp_box_lbl),
            *play_fade_sharp_tail,
            run_time=1.0
        )
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        flat_box = RoundedRectangle(width=5.3, height=3.2, color=GREEN_C, fill_color=GREEN, fill_opacity=0.1, corner_radius=0.06)
        flat_box.move_to(RIGHT * 3.3 + DOWN * 0.7)
        flat_box_lbl = create_text("Cumulative = 90% (Keep all)", font_size=8.5, color=GREEN_A)
        flat_box_lbl.move_to(np.array([3.3, -2.55, 0]))

        self.play(
            Create(flat_box),
            Write(flat_box_lbl),
            run_time=1.0
        )
        self.wait(4.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        summary_txt = create_text("Result: Top-P shrinks in sharp regions and expands in flat regions!", font_size=9.5, color=GREEN_A)
        summary_txt.next_to(left_container, DOWN, buff=0.15)
        self.play(Write(summary_txt), run_time=0.8)
        self.wait(6.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(step3_title),
            FadeOut(left_group),
            FadeOut(right_group),
            FadeOut(sharp_list),
            FadeOut(flat_list),
            FadeOut(topp_txt),
            FadeOut(sharp_box),
            FadeOut(sharp_box_lbl),
            FadeOut(flat_box),
            FadeOut(flat_box_lbl),
            FadeOut(summary_txt),
            run_time=1.2
        )
        self.wait(0.5)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step4_title = create_text("Code for sampling methods", font_size=13, color=BLUE_A)
        step4_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step4_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        code_box = RoundedRectangle(width=8.8, height=4.5, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.1)
        code_box.move_to(DOWN * 0.5)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        code_header = create_text("sampling_implementations.py", font_size=9.5, color=GRAY_B)
        code_header.next_to(code_box.get_top(), DOWN, buff=0.15).align_to(code_box.get_left(), LEFT).shift(RIGHT * 0.4)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        code_lines_text = [
            "1  probs = model(sequence)",
            "2",
            "3  # Greedy (Greedy decoding)",
            "4  indices, weights = probs.argmax(keepdim=True), None",
            "5",
            "6  # Ancestral (Ancestral Sampling)",
            "7  indices, weights = vocab_size, probs",
            "8",
            "9  # Top-k",
            "10 topk = probs.topk(k)",
            "11 indices, weights = topk.indices, topk.values",
            "12",
            "13 # Top-p (Nucleus)",
            "14 argsort = probs.argsort(descending=True)",
            "15 top_p = (argsort.values.cumsum() < p).sum() + 1",
            "16 indices, weights = argsort.indices[:top_p], argsort.values[:top_p]",
            "17",
            "18 # Epsilon (Probability threshold truncation)",
            "19 indices, weights = vocab_size, probs * (probs > epsilon)",
            "20",
            "21 # Temperature (Temperature)",
            "22 indices, weights = vocab_size, (logits / temp).softmax(-1)",
            "23",
            "24 # Sample (Randomly sample from the distribution)",
            "25 next_token = random.choices(indices, weights=weights, k=1)"
        ]

        code_lines_mobs = VGroup()
        for idx, line in enumerate(code_lines_text):
            # Note: visual/narration alignment comment translated from Vietnamese.
            if "#" in line:
                col = GRAY_A
            elif "top_p" in line or "topk" in line or "argmax" in line or "softmax" in line or "random.choices" in line:
                col = YELLOW_A
            else:
                col = WHITE
            
            # Escape HTML special characters for Pango markup
            line_escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            lbl = create_markup_text(f"<span font_family='Courier New'>{line_escaped}</span>", font_size=7.2, color=col)
            code_lines_mobs.add(lbl)
            
        code_lines_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        code_lines_mobs.next_to(code_header, DOWN, buff=0.25).align_to(code_header, LEFT)

        self.play(
            FadeIn(code_box),
            FadeIn(code_header),
            LaggedStart(*[Write(line) for line in code_lines_mobs], lag_ratio=0.02),
            run_time=2.0
        )
        self.wait(2.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        greedy_group = VGroup(code_lines_mobs[2], code_lines_mobs[3])
        topk_group = VGroup(code_lines_mobs[8], code_lines_mobs[9], code_lines_mobs[10])
        topp_group = VGroup(code_lines_mobs[12], code_lines_mobs[13], code_lines_mobs[14], code_lines_mobs[15])
        temp_group = VGroup(code_lines_mobs[20], code_lines_mobs[21])
        sample_group = VGroup(code_lines_mobs[23], code_lines_mobs[24])

        # Highlight Greedy
        hl_greedy = RoundedRectangle(width=8.2, height=greedy_group.get_height() + 0.18, color=YELLOW, fill_color=YELLOW, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_greedy.move_to(np.array([0, greedy_group.get_center()[1], 0]))
        self.play(Create(hl_greedy), run_time=0.6)
        self.wait(1.5)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        hl_topk = RoundedRectangle(width=8.2, height=topk_group.get_height() + 0.18, color=BLUE, fill_color=BLUE, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_topk.move_to(np.array([0, topk_group.get_center()[1], 0]))
        self.play(ReplacementTransform(hl_greedy, hl_topk), run_time=0.8)
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        hl_topp = RoundedRectangle(width=8.2, height=topp_group.get_height() + 0.18, color=GREEN, fill_color=GREEN, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_topp.move_to(np.array([0, topp_group.get_center()[1], 0]))
        self.play(ReplacementTransform(hl_topk, hl_topp), run_time=0.8)
        self.wait(3.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        hl_temp = RoundedRectangle(width=8.2, height=temp_group.get_height() + 0.18, color=ORANGE, fill_color=ORANGE, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_temp.move_to(np.array([0, temp_group.get_center()[1], 0]))
        self.play(ReplacementTransform(hl_topp, hl_temp), run_time=0.8)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        hl_sample = RoundedRectangle(width=8.2, height=sample_group.get_height() + 0.18, color=YELLOW, fill_color=YELLOW, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_sample.move_to(np.array([0, sample_group.get_center()[1], 0]))
        self.play(ReplacementTransform(hl_temp, hl_sample), run_time=0.8)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(hl_sample),
            *[FadeOut(line) for line in code_lines_mobs],
            FadeOut(code_header),
            run_time=0.8
        )
        
        framework_title = create_text("Use built-in inference libraries", font_size=13, color=BLUE_A)
        framework_title.move_to(step4_title.get_center())
        
        self.play(
            ReplacementTransform(step4_title, framework_title),
            run_time=0.8
        )
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        framework_code_text = [
            "# vLLM Framework",
            "from vllm import LLM, SamplingParams",
            "llm = LLM(model=\"facebook/opt-125m\")",
            "prompts = [\"Hello, my name is\"]",
            "sampling_params = SamplingParams(temperature=0.8, top_p=0.95)",
            "outputs = llm.generate(prompts, sampling_params)",
            " ",
            "# Huggingface (transformers)",
            "from transformers import AutoModelForCausalLM, AutoTokenizer",
            "model = AutoModelForCausalLM.from_pretrained(\"gpt2\")",
            "tokenizer = AutoTokenizer.from_pretrained(\"gpt2\")",
            "text = \"Hello, my name is\"",
            "tokens = tokenizer(text, return_tensors=\"pt\")",
            "output = model(**tokens).generate(temperature=0.8, top_p=0.95, do_sample=True)"
        ]
        
        fw_lines_mobs = VGroup()
        for idx, line in enumerate(framework_code_text):
            if line.strip() == "":
                lbl = VMobject()
                lbl.set_points_as_corners([ORIGIN, UP * 0.15])
                lbl.set_opacity(0)
            else:
                if "#" in line:
                    col = GRAY_A
                elif "from" in line or "import" in line:
                    col = BLUE_B
                elif "generate" in line or "SamplingParams" in line:
                    col = YELLOW_A
                else:
                    col = WHITE
                    
                line_escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                lbl = create_markup_text(f"<span font_family='Courier New'>{line_escaped}</span>", font_size=7.5, color=col)
            fw_lines_mobs.add(lbl)
            
        fw_lines_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        fw_lines_mobs.move_to(code_box.get_center())
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            Write(fw_lines_mobs),
            run_time=2.0
        )
        self.wait(6.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            *[FadeOut(line) for line in fw_lines_mobs],
            FadeOut(code_box),
            FadeOut(framework_title),
            run_time=1.0
        )
        self.wait(0.5)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        heavy_tail_title = create_text("Why do LLM distributions have heavy tails?", font_size=13, color=BLUE_A)
        heavy_tail_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(heavy_tail_title), run_time=0.8)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        ht_box = RoundedRectangle(width=8.8, height=3.8, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        ht_box.move_to(DOWN * 0.5)
        
        ht_subtitle = create_text("Why are next-token distributions heavy-tailed?", font_size=12, color=YELLOW)
        ht_subtitle.next_to(ht_box.get_top(), DOWN, buff=0.25)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        item1 = create_markup_text(
            "1. <span color='#ffaa55'>Under-training</span>: Insufficient training",
            font_size=10, color=WHITE
        )
        item2 = create_markup_text(
            "2. <span color='#ffaa55'>Mode-seeking behavior</span>: Cross-entropy heavily penalizes missing-probability errors",
            font_size=10, color=WHITE
        )
        item3 = create_markup_text(
            "3. <span color='#ffaa55'>Low-rank constraints</span>: Rank limits in the final-layer representation matrix",
            font_size=10, color=WHITE
        )
        
        items = VGroup(item1, item2, item3)
        items.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        items.next_to(ht_subtitle, DOWN, buff=0.35).shift(LEFT * 0.4)
        
        self.play(
            FadeIn(ht_box),
            Write(ht_subtitle),
            run_time=1.0
        )
        self.wait(1.5)
        
        self.play(Write(item1), run_time=1.0)
        self.wait(3.0)
        self.play(Write(item2), run_time=1.0)
        self.wait(4.0)
        self.play(Write(item3), run_time=1.0)
        self.wait(6.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(heavy_tail_title),
            FadeOut(ht_box),
            FadeOut(ht_subtitle),
            FadeOut(items),
            FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(1.5)
        finish_voiceovers(self, voiceover_end)
