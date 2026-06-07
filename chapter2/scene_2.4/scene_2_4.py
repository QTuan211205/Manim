import os
import tempfile
from manim import *
import numpy as np

# Cấu hình thư mục tạm thời cho text và tex để tránh lỗi phân quyền trên Windows
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

# Hàm hỗ trợ tạo Text đảm bảo không bị lỗi mất dấu tiếng Việt khi hiển thị kích thước nhỏ trên Windows
def create_text(text, font_size=24, font="Arial", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)

# Hàm hỗ trợ tạo MarkupText đảm bảo không bị lỗi mất dấu tiếng Việt khi hiển thị kích thước nhỏ trên Windows
def create_markup_text(text, font_size=24, font="Arial", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)

# Hàm vẽ ký hiệu Theta vector
def get_theta(color=WHITE, stroke_width=2.0):
    ellipse = Ellipse(width=0.15, height=0.22, color=color, stroke_width=stroke_width)
    line = Line(LEFT * 0.06, RIGHT * 0.06, color=color, stroke_width=stroke_width)
    line.move_to(ellipse.get_center())
    return VGroup(ellipse, line)

# Hàm vẽ ký hiệu Sigma vector
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

# Hàm hỗ trợ tạo p_theta(x) giữ baseline thẳng hàng
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
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH
        # =====================================================================
        chapter_title = create_text("Lấy mẫu & Truncation", font_size=24, color=YELLOW)
        chapter_sub = create_text("(Sampling & Truncation)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(2.0)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Lấy mẫu & Truncation (Top-k vs. Top-p & Nhiệt độ)", font_size=16, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(1.0)


        # =====================================================================
        # BƯỚC 1B: LẤY MẪU TỔ TIÊN & ĐUÔI NẶNG (HEAVY TAIL) (00:00 - 00:45)
        # =====================================================================
        step1_title = create_text("1. Lấy mẫu tổ tiên (Ancestral Sampling) & Đuôi nặng", font_size=13, color=BLUE_A)
        step1_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step1_title), run_time=0.8)

        # Công thức Lấy mẫu tổ tiên trên một dòng thẳng hàng
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

        # Mô tả phân phối Đuôi nặng (Heavy Tail)
        tail_box = RoundedRectangle(width=8.0, height=3.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        tail_box.move_to(DOWN * 1.2)
        
        # Biểu đồ cột xác suất từ vựng
        tail_words = ["\"is\"", "\",\"", "\"and\"", "\"has\"", "\"here\"", "\"actor\"", "\"award\"", "\"Beyoncé\""]
        tail_probs = [0.45, 0.20, 0.10, 0.05, 0.03, 0.015, 0.015, 0.01]
        tail_colors = [BLUE_D, BLUE_D, BLUE_D, GRAY_C, GRAY_C, RED_D, RED_D, RED_E]
        
        bars = []
        labels = []
        vals = []
        chart_base_y = -2.3
        
        for i in range(8):
            x_pos = -3.5 + i * 1.0
            height = tail_probs[i] * 4.0
            bar = Rectangle(
                width=0.45, 
                height=max(height, 0.04), 
                color=tail_colors[i], 
                fill_color=tail_colors[i], 
                fill_opacity=0.9
            )
            bar.move_to(np.array([x_pos, chart_base_y + max(height, 0.04)/2.0, 0]))
            bars.append(bar)
            
            lbl = create_text(tail_words[i], font_size=8, color=WHITE)
            lbl.move_to(np.array([x_pos, chart_base_y - 0.25, 0]))
            labels.append(lbl)
            
            val = create_text(f"{tail_probs[i]*100:.1f}%", font_size=7.5, color=tail_colors[i])
            val.move_to(np.array([x_pos, chart_base_y + height + 0.18, 0]))
            vals.append(val)
            
        bar_group = VGroup(*bars)
        label_group = VGroup(*labels)
        val_group = VGroup(*vals)
        chart_group = VGroup(bar_group, label_group, val_group)
        chart_group.move_to(DOWN * 1.2)

        self.play(
            FadeIn(tail_box),
            FadeIn(chart_group, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait(3.0)

        # Giải thích cạm bẫy đuôi nặng: Highlighter quét ngẫu nhiên và bốc trúng Beyoncé
        selector_line = Line(UP * 0.1, DOWN * 0.1, color=YELLOW, stroke_width=2.5)
        selector_line.move_to(bars[0].get_top() + UP * 0.1)
        
        self.play(FadeIn(selector_line), run_time=0.4)
        
        # Di chuyển bộ chọn quét qua lại rồi dừng ở Beyoncé
        self.play(
            selector_line.animate.move_to(bars[2].get_top() + UP * 0.1),
            run_time=0.5
        )
        self.play(
            selector_line.animate.move_to(bars[4].get_top() + UP * 0.1),
            run_time=0.4
        )
        self.play(
            selector_line.animate.move_to(bars[7].get_top() + UP * 0.1),
            run_time=0.6
        )
        self.wait(0.5)

        # Highlight cột Beyoncé và hiển thị văn bản incoherent
        self.play(
            bars[7].animate.set_color(YELLOW).set_fill(YELLOW, opacity=1.0),
            FadeOut(selector_line),
            run_time=0.5
        )
        
        # Clear the screen to show comparison
        comp_title = create_text("Hành vi sinh văn bản của các phương pháp giải mã", font_size=13, color=BLUE_A)
        comp_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(
            FadeOut(ancestral_step),
            FadeOut(ancestral_seq),
            FadeOut(tail_box),
            FadeOut(chart_group),
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
        title_greedy = create_markup_text("<b>Greedy Decoding</b>\n<span color='#ffaa55'>(Bẫy lặp từ - Repetitive)</span>", font_size=10, color=RED_A)
        title_greedy.next_to(box_greedy.get_top(), DOWN, buff=0.2)
        
        title_ancestral = create_markup_text("<b>Ancestral Sampling</b>\n<span color='#ffaa55'>(Mất nhất quán - Incoherent)</span>", font_size=10, color=ORANGE)
        title_ancestral.next_to(box_ancestral.get_top(), DOWN, buff=0.2)
        
        title_topk = create_markup_text("<b>Top-k Truncation</b>\n<span color='#55ff55'>(Hợp lý - Acceptable)</span>", font_size=10, color=GREEN_A)
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
            "... Beyoncé.\"",
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

        # Chuyển tiếp sang Slide 55: Truncation sampling table
        trunc_title = create_text("Các phương pháp cắt đuôi phân phối (Truncation)", font_size=13, color=BLUE_A)
        trunc_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(
            FadeOut(box_greedy), FadeOut(title_greedy), FadeOut(txt_greedy),
            FadeOut(box_ancestral), FadeOut(title_ancestral), FadeOut(txt_ancestral),
            FadeOut(box_topk), FadeOut(title_topk), FadeOut(txt_topk),
            ReplacementTransform(comp_title, trunc_title),
            run_time=1.0
        )
        
        # Vẽ bảng Truncation
        trunc_box = RoundedRectangle(width=9.5, height=3.6, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        trunc_box.move_to(DOWN * 0.5)
        
        # Header hàng đầu tiên
        header_method = create_markup_text("<b>Phương pháp (Method)</b>", font_size=11, color=YELLOW)
        header_strategy = create_markup_text("<b>Chiến lược ngưỡng (Threshold strategy)</b>", font_size=11, color=YELLOW)
        
        header_method.move_to(LEFT * 3.5 + UP * 0.8, aligned_edge=LEFT)
        header_strategy.move_to(LEFT * 0.5 + UP * 0.8, aligned_edge=LEFT)
        
        row_data = [
            ("Top-k", "Lấy mẫu từ k token có xác suất cao nhất"),
            ("Top-p (Nucleus)", "Tổng xác suất tích lũy đạt tối đa p"),
            ("Epsilon (ε)", "Xác suất của token lớn hơn ngưỡng ε"),
            ("Eta (η)", "Ngưỡng xác suất tối thiểu tỷ lệ thuận với Entropy"),
            ("Min-p", "Xác suất tối thiểu tỷ lệ với xác suất của token lớn nhất")
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
        
        # Dọn dẹp Slide 55
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
        # BƯỚC 2: NHIỆT ĐỘ (TEMPERATURE SAMPLING) (00:45 - 01:30)
        # =====================================================================
        step2_title = create_text("2. Điều chỉnh phân phối bằng Nhiệt độ (Temperature)", font_size=13, color=BLUE_A)
        step2_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step2_title), run_time=0.8)

        # Hộp chứa công thức Softmax có nhiệt độ
        temp_formula_box = RoundedRectangle(width=6.0, height=1.4, color=GREEN_E, fill_color="#0d2417", fill_opacity=0.4, corner_radius=0.08)
        temp_formula_box.move_to(UP * 1.8)
        
        # Build Softmax formula manually to format as fraction
        lhs = create_markup_text("Softmax(z, τ)<sub>i</sub> = ", font_size=20, color="#8fbcbb")
        
        # Tử số exp(z_i / tau)
        num_e = create_text("e", font_size=20, color=YELLOW)
        num_pow = create_markup_text("z<sub>i</sub>/τ", font_size=13, color=YELLOW)
        num_pow.next_to(num_e.get_corner(UP + RIGHT), RIGHT, buff=0.01).shift(UP * 0.03)
        numerator = VGroup(num_e, num_pow)
        
        # Mẫu số (sử dụng custom Sigma)
        sigma = get_sigma(color="#88c0d0", stroke_width=1.5).scale(0.65)
        j_sub_sigma = create_text("j", font_size=12, color="#88c0d0")
        j_sub_sigma.next_to(sigma, DOWN, buff=0.04)
        
        den_e = create_text("e", font_size=20, color="#88c0d0")
        den_pow = create_markup_text("z<sub>j</sub>/τ", font_size=13, color="#88c0d0")
        den_pow.next_to(den_e.get_corner(UP + RIGHT), RIGHT, buff=0.01).shift(UP * 0.03)
        den_term = VGroup(den_e, den_pow)
        den_term.next_to(sigma, RIGHT, buff=0.1)
        denominator = VGroup(sigma, j_sub_sigma, den_term)
        
        # Đường gạch phân số
        fraction_line = Line(LEFT * 0.6, RIGHT * 0.6, color=WHITE, stroke_width=1.5)
        
        # Canh lề dọc
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

        # Khởi tạo Slider trực quan cho Nhiệt độ
        slider_line = Line(LEFT * 2.5 + DOWN * 2.5, RIGHT * 2.5 + DOWN * 2.5, color=GRAY, stroke_width=3.0)
        slider_lbl = create_text("Nhiệt độ τ = 1.0", font_size=11, color=YELLOW)
        slider_lbl.move_to(DOWN * 2.1)
        
        # Tracker điều khiển giá trị nhiệt độ
        temp_tracker = ValueTracker(1.0)
        
        # Bộ chuyển đổi tọa độ từ giá trị Tracker sang trục X của Slider
        # τ chạy từ 0.2 (trái) đến 2.0 (phải)
        def get_slider_x(val):
            return -2.5 + (val - 0.2) / (2.0 - 0.2) * 5.0

        slider_handle = always_redraw(lambda: Dot(
            point=np.array([get_slider_x(temp_tracker.get_value()), -2.5, 0]), 
            radius=0.12, 
            color=YELLOW
        ))
        
        slider_text = always_redraw(lambda: create_text(
            f"Nhiệt độ τ = {temp_tracker.get_value():.1f}", 
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

        # Thiết lập biểu đồ cột động
        logits = [3.0, 2.2, 1.5, 0.5, 0.2]
        words = ["a", "the", "an", "not", "one"]
        colors = [BLUE_D, GRAY_C, GRAY_C, RED_D, RED_E]
        chart_base_y = -1.6
        
        def get_dynamic_bars():
            temp = temp_tracker.get_value()
            scaled_logits = [l / temp for l in logits]
            # Giới hạn giá trị lũy thừa tránh tràn số
            scaled_logits = [np.clip(sl, -50.0, 50.0) for sl in scaled_logits]
            exp_logits = [np.exp(sl) for sl in scaled_logits]
            sum_exp = sum(exp_logits)
            probs = [el / sum_exp for el in exp_logits]
            
            bars_group = VGroup()
            for idx, p in enumerate(probs):
                x_pos = -3.0 + idx * 1.5
                height = p * 1.8
                
                # Cột xác suất
                rect = Rectangle(
                    width=0.6, 
                    height=max(height, 0.05), 
                    color=colors[idx], 
                    fill_color=colors[idx], 
                    fill_opacity=0.85,
                    stroke_width=1.0
                )
                rect.move_to(np.array([x_pos, chart_base_y + max(height, 0.05)/2.0, 0]))
                
                # Nhãn từ
                lbl = create_text(f'"{words[idx]}"', font_size=9, color=WHITE)
                lbl.move_to(np.array([x_pos, chart_base_y - 0.25, 0]))
                
                # Nhãn phần trăm
                val = create_text(f"{p*100:.0f}%", font_size=8.5, color=colors[idx])
                val.move_to(np.array([x_pos, chart_base_y + max(height, 0.05) + 0.18, 0]))
                
                bars_group.add(VGroup(rect, lbl, val))
            return bars_group

        dynamic_chart = always_redraw(get_dynamic_bars)
        
        self.play(FadeIn(dynamic_chart), run_time=1.0)
        self.wait(2.0)

        # 1. ANimation TĂNG Nhiệt độ (τ = 2.0) -> Trở nên Phẳng (Flat/Diverse)
        info_txt = create_text("τ = 2.0 (High): Phân phối phẳng, đa dạng nhưng dễ mất nhất quán", font_size=10, color=GRAY_A)
        info_txt.move_to(UP * 0.9)
        
        self.play(
            temp_tracker.animate.set_value(2.0),
            FadeIn(info_txt, shift=UP * 0.1),
            run_time=2.0
        )
        self.wait(3.5)

        # 2. ANimation GIẢM Nhiệt độ về bình thường (τ = 1.0)
        self.play(
            temp_tracker.animate.set_value(1.0),
            FadeOut(info_txt),
            run_time=1.5
        )
        self.wait(1.5)

        # 3. ANimation GIẢM Nhiệt độ cực thấp (τ = 0.2) -> Trở nên Nhọn (Sharp/Greedy)
        info_txt2 = create_text("τ = 0.2 (Low): Phân phối nhọn, tự tin cao nhưng dễ lặp lại (Greedy)", font_size=10, color=GRAY_A)
        info_txt2.move_to(UP * 0.9)
        
        self.play(
            temp_tracker.animate.set_value(0.2),
            FadeIn(info_txt2, shift=UP * 0.1),
            run_time=2.5
        )
        self.wait(4.0)

        # Quay về 1.0 để dọn dẹp
        self.play(
            temp_tracker.animate.set_value(1.0),
            FadeOut(info_txt2),
            run_time=1.5
        )
        self.wait(0.5)

        # Ẩn biểu đồ động và thanh trượt để hiện bảng Pro/Con
        self.remove(dynamic_chart, slider_handle, slider_text)
        self.play(
            FadeOut(temp_formula_box),
            FadeOut(temp_formula),
            FadeOut(slider_line),
            run_time=1.0
        )
        temp_table_title = create_text("Bảng so sánh tác động của Nhiệt độ", font_size=13, color=BLUE_A)
        temp_table_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(
            ReplacementTransform(step2_title, temp_table_title),
            run_time=0.8
        )
        
        # Vẽ bảng Pro/Con
        table_box = RoundedRectangle(width=8.5, height=2.8, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        table_box.move_to(DOWN * 0.5)
        
        h_param = create_markup_text("<b>Nhiệt độ (Parameter)</b>", font_size=11, color=YELLOW)
        h_pro = create_markup_text("<b>Ưu điểm (Pro)</b>", font_size=11, color=YELLOW)
        h_con = create_markup_text("<b>Nhược điểm (Con)</b>", font_size=11, color=YELLOW)
        
        h_param.move_to(LEFT * 2.5 + UP * 0.5)
        h_pro.move_to(ORIGIN + UP * 0.5)
        h_con.move_to(RIGHT * 2.5 + UP * 0.5)
        
        row_high = VGroup(
            create_text("Cao (High τ ≥ 1.0)", font_size=10, color=BLUE_C).move_to(LEFT * 2.5 + DOWN * 0.1),
            create_text("Đa dạng (Diverse)", font_size=10, color=GREEN_C).move_to(ORIGIN + DOWN * 0.1),
            create_text("Mất nhất quán (Incoherent)", font_size=10, color=RED_C).move_to(RIGHT * 2.5 + DOWN * 0.1)
        )
        
        row_low = VGroup(
            create_text("Thấp (Low τ < 1.0)", font_size=10, color=BLUE_C).move_to(LEFT * 2.5 + DOWN * 0.7),
            create_text("Nhất quán (Coherent)", font_size=10, color=GREEN_C).move_to(ORIGIN + DOWN * 0.7),
            create_text("Lặp từ (Repetitive)", font_size=10, color=RED_C).move_to(RIGHT * 2.5 + DOWN * 0.7)
        )
        
        self.play(
            FadeIn(table_box),
            FadeIn(h_param), FadeIn(h_pro), FadeIn(h_con),
            Write(row_high), Write(row_low),
            run_time=1.5
        )
        self.wait(6.0)
        
        # Dọn dẹp bảng Nhiệt độ
        self.play(
            FadeOut(temp_table_title),
            FadeOut(table_box),
            FadeOut(h_param), FadeOut(h_pro), FadeOut(h_con),
            FadeOut(row_high), FadeOut(row_low),
            run_time=1.0
        )
        self.wait(0.5)


        # =====================================================================
        # BƯỚC 3: TRUNCATION SAMPLING (TOP-K vs. TOP-P) (01:30 - 02:30)
        # =====================================================================
        step3_title = create_text("3. Cắt đuôi phân phối: Top-k vs. Top-p (Nucleus)", font_size=13, color=BLUE_A)
        step3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step3_title), run_time=0.8)

        # Định nghĩa 2 danh sách phân phối đại diện cho: Sharp và Flat
        # Cột trái: Taylor Swift is (Sharp)
        sharp_words = ["is", ",", "and", "has", "here", "?", "means", "in"]
        sharp_probs = [0.68, 0.15, 0.05, 0.02, 0.01, 0.01, 0.01, 0.01]
        
        # Cột phải: My name (Flat)
        flat_words = [",", "and", "is", "(", "\\n", "said", "in", "had"]
        flat_probs = [0.12, 0.11, 0.10, 0.09, 0.08, 0.08, 0.07, 0.07]

        # Khung chứa 2 phân phối
        left_container = RoundedRectangle(width=5.8, height=4.2, color=BLUE_E, fill_color="#0e1726", fill_opacity=0.3, corner_radius=0.08)
        left_container.move_to(LEFT * 3.3 + DOWN * 0.6)
        left_title = create_text("Phân phối Dốc (Sharp) \"Taylor Swift is\"", font_size=9, color=BLUE_C)
        left_title.next_to(left_container.get_top(), DOWN, buff=0.15)
        left_group = VGroup(left_container, left_title)

        right_container = RoundedRectangle(width=5.8, height=4.2, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.7, corner_radius=0.08)
        right_container.move_to(RIGHT * 3.3 + DOWN * 0.6)
        right_title = create_text("Phân phối Phẳng (Flat) \"My name\"", font_size=9, color=GRAY_B)
        right_title.next_to(right_container.get_top(), DOWN, buff=0.15)
        right_group = VGroup(right_container, right_title)

        self.play(
            FadeIn(left_group, shift=RIGHT * 0.15),
            FadeIn(right_group, shift=LEFT * 0.15),
            run_time=1.0
        )
        self.wait(1.0)

        # Hàm vẽ biểu đồ danh sách các từ và thanh ngang
        def get_vocab_list(words, probs, center_x, chart_color):
            list_group = VGroup()
            start_y = 0.7
            spacing = 0.4
            
            bars_list = []
            for idx in range(8):
                y_pos = start_y - idx * spacing
                
                # Nhãn từ
                lbl = create_text(f'"{words[idx]}"', font_size=9.5, color=WHITE)
                lbl.move_to(np.array([center_x - 2.1, y_pos, 0]), aligned_edge=LEFT)
                
                # Thanh ngang biểu thị xác suất
                # max xác suất 0.68 tương ứng độ dài 1.8 đơn vị
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
                
                # Số phần trăm
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

        # -------------------- MINH HỌA TOP-K (K=5) --------------------
        topk_txt = create_text("Top-K (K = 5): Cố định số lượng từ được chọn lọc", font_size=11, color=YELLOW)
        topk_txt.next_to(step3_title, DOWN, buff=0.15)
        
        # Đường cắt gạch ngang ở vị trí K=5 (nằm giữa dòng 4 và 5, y = 0.7 - 4.5 * 0.4 = -1.1)
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
        
        # Làm mờ phần bị loại bỏ (các dòng 5, 6, 7, tức là index từ 5 trở đi)
        play_fade_tail = []
        for idx in range(5, 8):
            play_fade_tail.append(sharp_list[idx].animate.set_opacity(0.25))
            play_fade_tail.append(flat_list[idx].animate.set_opacity(0.25))
        self.play(*play_fade_tail, run_time=0.8)
        self.wait(2.5)

        # Highlight vấn đề của Top-K ở cột Flat
        # Ở cột Flat, các từ "said" (8%), "in" (7%), "had" (7%) bị cắt bỏ vô lý dù xác suất gần bằng "(\n" (8%)
        highlight_box = RoundedRectangle(width=5.2, height=0.96, color=RED_D, fill_color=RED, fill_opacity=0.1, corner_radius=0.06)
        highlight_box.move_to(RIGHT * 3.3 + DOWN * 1.72)
        
        problem_txt = create_text("Lãng phí: \"said\", \"in\", \"had\" bị loại bỏ dù có xác suất tương đồng!", font_size=9, color=RED_A)
        problem_txt.next_to(right_container, DOWN, buff=0.15)

        self.play(
            Create(highlight_box),
            Write(problem_txt),
            run_time=0.8
        )
        self.wait(4.5)

        # Xóa nhãn Top-K để chuyển sang Top-P
        # Khôi phục độ mờ
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

        # -------------------- MINH HỌA TOP-P (P=0.90) --------------------
        topp_txt = create_text("Top-P (p = 0.90): Tổng xác suất tích lũy (Ngưỡng động linh hoạt)", font_size=11, color=GREEN_A)
        topp_txt.next_to(step3_title, DOWN, buff=0.15)
        self.play(Write(topp_txt), run_time=0.8)

        # Cột Sharp: Cộng dồn 90% (is: 68%, ,: 15%, and: 5%, has: 2% = 90% -> lấy 4 từ đầu)
        # Vẽ hộp bao quanh các từ được giữ lại ở cột trái (4 từ đầu)
        sharp_box = RoundedRectangle(width=5.3, height=1.6, color=GREEN_C, fill_color=GREEN, fill_opacity=0.1, corner_radius=0.06)
        sharp_box.move_to(LEFT * 3.3 + UP * 0.1)
        sharp_box_lbl = create_text("Tích lũy = 90% (Giữ 4 từ)", font_size=8.5, color=GREEN_A)
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

        # Cột Flat: Cộng dồn 90% (12+11+10+9+8+8+7+7+6+5+5 = 88% + ... -> lấy toàn bộ hoặc gần như toàn bộ từ)
        # Hộp bao quanh cột phải (lấy tất cả 8 từ hiển thị)
        flat_box = RoundedRectangle(width=5.3, height=3.2, color=GREEN_C, fill_color=GREEN, fill_opacity=0.1, corner_radius=0.06)
        flat_box.move_to(RIGHT * 3.3 + DOWN * 0.7)
        flat_box_lbl = create_text("Tích lũy = 90% (Giữ toàn bộ)", font_size=8.5, color=GREEN_A)
        flat_box_lbl.move_to(np.array([3.3, -2.55, 0]))

        self.play(
            Create(flat_box),
            Write(flat_box_lbl),
            run_time=1.0
        )
        self.wait(4.5)

        # Giải thích tổng kết Top-P co giãn dynamic
        summary_txt = create_text("Kết quả: Top-P tự co lại ở vùng dốc (sharp) và giãn rộng ở vùng phẳng (flat)!", font_size=9.5, color=GREEN_A)
        summary_txt.next_to(left_container, DOWN, buff=0.15)
        self.play(Write(summary_txt), run_time=0.8)
        self.wait(6.0)

        # Thu dọn bước 3
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
        # BƯỚC 4: BẢNG MÃ PYTHON IMPLEMENTATION (02:30 - 03:00)
        # =====================================================================
        step4_title = create_text("Đoạn mã lập trình các phương pháp Lấy mẫu", font_size=13, color=BLUE_A)
        step4_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step4_title), run_time=0.8)

        # Vẽ bảng Code panel
        code_box = RoundedRectangle(width=8.8, height=4.5, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.1)
        code_box.move_to(DOWN * 0.5)
        
        # Tiêu đề code panel
        code_header = create_text("sampling_implementations.py", font_size=9.5, color=GRAY_B)
        code_header.next_to(code_box.get_top(), DOWN, buff=0.15).align_to(code_box.get_left(), LEFT).shift(RIGHT * 0.4)
        
        # Các dòng code mẫu
        code_lines_text = [
            "1  probs = model(sequence)",
            "2",
            "3  # Greedy (Giải mã tham lam)",
            "4  indices, weights = probs.argmax(keepdim=True), None",
            "5",
            "6  # Ancestral (Lấy mẫu tổ tiên)",
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
            "18 # Epsilon (Cắt ngưỡng xác suất)",
            "19 indices, weights = vocab_size, probs * (probs > epsilon)",
            "20",
            "21 # Temperature (Nhiệt độ)",
            "22 indices, weights = vocab_size, (logits / temp).softmax(-1)",
            "23",
            "24 # Sample (Bốc thăm ngẫu nhiên từ phân phối)",
            "25 next_token = random.choices(indices, weights=weights, k=1)"
        ]

        code_lines_mobs = VGroup()
        for idx, line in enumerate(code_lines_text):
            # Chọn màu cho comments
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

        # Định nghĩa các nhóm dòng code tương ứng để highlight chính xác (bao gồm cả comment)
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
        
        # Chuyển Highlight sang Top-k
        hl_topk = RoundedRectangle(width=8.2, height=topk_group.get_height() + 0.18, color=BLUE, fill_color=BLUE, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_topk.move_to(np.array([0, topk_group.get_center()[1], 0]))
        self.play(ReplacementTransform(hl_greedy, hl_topk), run_time=0.8)
        self.wait(2.0)

        # Chuyển Highlight sang Top-p
        hl_topp = RoundedRectangle(width=8.2, height=topp_group.get_height() + 0.18, color=GREEN, fill_color=GREEN, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_topp.move_to(np.array([0, topp_group.get_center()[1], 0]))
        self.play(ReplacementTransform(hl_topk, hl_topp), run_time=0.8)
        self.wait(3.5)

        # Chuyển Highlight sang Temperature
        hl_temp = RoundedRectangle(width=8.2, height=temp_group.get_height() + 0.18, color=ORANGE, fill_color=ORANGE, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_temp.move_to(np.array([0, temp_group.get_center()[1], 0]))
        self.play(ReplacementTransform(hl_topp, hl_temp), run_time=0.8)
        self.wait(3.0)

        # Chuyển Highlight sang final Sample step
        hl_sample = RoundedRectangle(width=8.2, height=sample_group.get_height() + 0.18, color=YELLOW, fill_color=YELLOW, fill_opacity=0.1, corner_radius=0.03, stroke_width=1.0)
        hl_sample.move_to(np.array([0, sample_group.get_center()[1], 0]))
        self.play(ReplacementTransform(hl_temp, hl_sample), run_time=0.8)
        self.wait(3.0)

        # Dọn dẹp panel code thủ công để hiện code thư viện (Slide 62)
        self.play(
            FadeOut(hl_sample),
            *[FadeOut(line) for line in code_lines_mobs],
            FadeOut(code_header),
            run_time=0.8
        )
        
        framework_title = create_text("Sử dụng các thư viện inference tích hợp sẵn", font_size=13, color=BLUE_A)
        framework_title.move_to(step4_title.get_center())
        
        self.play(
            ReplacementTransform(step4_title, framework_title),
            run_time=0.8
        )
        
        # Tạo các dòng code của vLLM và HF
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
        
        # Hiện code framework
        self.play(
            Write(fw_lines_mobs),
            run_time=2.0
        )
        self.wait(6.0)
        
        # Dọn dẹp Slide 62
        self.play(
            *[FadeOut(line) for line in fw_lines_mobs],
            FadeOut(code_box),
            FadeOut(framework_title),
            run_time=1.0
        )
        self.wait(0.5)

        # =====================================================================
        # BƯỚC MỚI: TẠI SAO PHÂN PHỐI LẠI CÓ ĐUÔI NẶNG? (Slide 63-65)
        # =====================================================================
        heavy_tail_title = create_text("Tại sao phân phối LLM có Đuôi Nặng?", font_size=13, color=BLUE_A)
        heavy_tail_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(heavy_tail_title), run_time=0.8)
        
        # Vẽ hộp slide
        ht_box = RoundedRectangle(width=8.8, height=3.8, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        ht_box.move_to(DOWN * 0.5)
        
        ht_subtitle = create_text("Why are next-token distributions heavy-tailed?", font_size=12, color=YELLOW)
        ht_subtitle.next_to(ht_box.get_top(), DOWN, buff=0.25)
        
        # Các gạch đầu dòng giải thích lý do
        item1 = create_markup_text(
            "1. <span color='#ffaa55'>Under-training</span>: Huấn luyện chưa đủ độ chín",
            font_size=10, color=WHITE
        )
        item2 = create_markup_text(
            "2. <span color='#ffaa55'>Mode-seeking behavior</span>: Hàm cross-entropy phạt nặng lỗi thiếu xác xuất",
            font_size=10, color=WHITE
        )
        item3 = create_markup_text(
            "3. <span color='#ffaa55'>Low-rank constraints</span>: Giới hạn hạng ma trận biểu diễn ở lớp cuối cùng",
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
        
        # Kết thúc toàn bộ phân cảnh
        self.play(
            FadeOut(heavy_tail_title),
            FadeOut(ht_box),
            FadeOut(ht_subtitle),
            FadeOut(items),
            FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(1.5)
