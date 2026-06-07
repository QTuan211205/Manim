import os
import tempfile
from manim import *
import numpy as np

# Cấu hình thư mục tạm thời cho text và tex để tránh lỗi phân quyền (Access is denied) trên Windows
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

# Hàm hỗ trợ định vị một chuỗi ký tự con trong MarkupText/Text để vẽ SurroundingRectangle chính xác
def get_text_part(mobject, substring):
    raw_text = getattr(mobject, "text", "")
    if not raw_text:
        for sub in mobject.submobjects:
            if hasattr(sub, "text"):
                raw_text = sub.text
                mobject = sub
                break

    # Loại bỏ các thẻ HTML để lấy chuỗi ký tự hiển thị thực tế
    clean_chars = []
    in_tag = False
    for char in raw_text:
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        elif not in_tag:
            clean_chars.append(char)
    clean_text = "".join(clean_chars)

    # Thử tìm kiếm không dấu cách phòng trường hợp Pango tự loại bỏ hoặc thêm khoảng trắng
    clean_text_no_spaces = clean_text.replace(" ", "")
    sub_no_spaces = substring.replace(" ", "")
    start_idx_no_spaces = clean_text_no_spaces.find(sub_no_spaces)
    if start_idx_no_spaces == -1:
        raise ValueError(f"Không tìm thấy chuỗi '{substring}' trong '{clean_text}' (raw: '{raw_text}')")

    # Ánh xạ chỉ số từ không dấu cách về có dấu cách ban đầu
    mapping = []
    for idx, char in enumerate(clean_text):
        if char != ' ':
            mapping.append(idx)
            
    start_idx = mapping[start_idx_no_spaces]
    end_idx = mapping[start_idx_no_spaces + len(sub_no_spaces) - 1] + 1
    return mobject[start_idx:end_idx]



class Scene1_2(MovingCameraScene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # Lưới tọa độ mờ nền sau tạo kết cấu đồ họa chuyên nghiệp (Bỏ trục tung và trục hoành chính)
        grid = VGroup()
        for x in np.arange(-7.5, 8.0, 0.5):
            if abs(x) > 0.01:
                grid.add(Line(UP * 4.5, DOWN * 4.5, stroke_width=0.4, color=GRAY, stroke_opacity=0.06))
        for y in np.arange(-4.5, 5.0, 0.5):
            if abs(y) > 0.01:
                grid.add(Line(LEFT * 7.5, RIGHT * 7.5, stroke_width=0.4, color=GRAY, stroke_opacity=0.06))
        self.add(grid)

        # Tiêu đề chính hiển thị cố định ở đầu màn hình
        main_title = create_text("Ba Làn Sóng Mở Rộng Quy Mô LLM", font_size=20, color=BLUE_A)
        main_title.to_edge(UP, buff=0.4)
        self.play(Write(main_title))
        self.wait(1.5)


        # =====================================================================
        # GIAI ĐOẠN 1: GIỚI THIỆU HỆ TRỤC TỌA ĐỘ 3D ẢO
        # =====================================================================
        # Đặt gốc tọa độ dịch về bên trái để tránh đè các thẻ bên phải
        origin_pt = LEFT * 3.5 + DOWN * 1.5
        origin = Dot(point=origin_pt, color=GRAY, radius=0.08)

        # Lưới sàn 3D phối cảnh (X-Z plane)
        floor_grid = VGroup()
        for i in range(6):
            start = origin_pt + DR * 0.4 * i
            end = start + RIGHT * 4.2
            floor_grid.add(Line(start, end, color=GRAY, stroke_width=0.8, stroke_opacity=0.15))
        for i in range(10):
            start = origin_pt + RIGHT * 0.42 * i
            end = start + DR * 2.0
            floor_grid.add(Line(start, end, color=GRAY, stroke_width=0.8, stroke_opacity=0.15))

        # Khởi tạo các trục 3D
        axis_x = Arrow(origin_pt, origin_pt + RIGHT * 4.2, color=PURPLE, buff=0, stroke_width=3)
        label_x = create_text("X: Huấn luyện sơ khởi (Pre-training)", font_size=9, color=PURPLE)
        label_x.next_to(axis_x, DOWN, aligned_edge=RIGHT, buff=0.15)

        axis_y = Arrow(origin_pt, origin_pt + UP * 3.5, color=GREEN, buff=0, stroke_width=3)
        label_y = create_text("Y: Tinh chỉnh sau huấn luyện (Post-training)", font_size=9, color=GREEN)
        label_y.next_to(axis_y, LEFT, aligned_edge=UP, buff=0.15)

        axis_z = Arrow(origin_pt, origin_pt + DR * 2.0, color=BLUE, buff=0, stroke_width=3)
        label_z = create_text("Z: Tính toán khi suy luận (Test-time)", font_size=9, color=BLUE)
        label_z.next_to(axis_z.get_end(), DR, buff=0.1)

        # Vẽ hệ trục và lưới
        self.play(FadeIn(origin), Create(floor_grid), run_time=1.2)
        self.play(
            GrowArrow(axis_x), Write(label_x),
            GrowArrow(axis_y), Write(label_y),
            GrowArrow(axis_z), Write(label_z),
            run_time=2.0
        )
        self.wait(15.0) # Đợi lời thoại giới thiệu tổng quan về 3 làn sóng mở rộng quy mô


        # =====================================================================
        # GIAI ĐOẠN 2: TRỰC QUAN HÓA LUẬT LŨY THỪA (PRE-TRAINING SCALING LAWS)
        # =====================================================================
        # Mờ dần hệ trục 3D để tập trung vào đồ thị 2D của Pre-training
        stage1_mobjects = VGroup(origin, floor_grid, axis_x, label_x, axis_y, label_y, axis_z, label_z)
        self.play(FadeOut(stage1_mobjects), run_time=1.0)
        self.wait(0.5)

        # Dựng đồ thị 2D: Test Loss vs Compute Budget
        axes_pt = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 4, 1],
            x_length=7,
            y_length=4.2,
            axis_config={"color": PURPLE, "stroke_width": 2},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []}
        )
        axes_pt.shift(LEFT * 2.0 + DOWN * 0.2)
        
        # Nhãn cho đồ thị
        label_pt_x = create_text("Tài nguyên tính toán (Compute / N, D) >", font_size=9, color=WHITE)
        label_pt_x.next_to(axes_pt.x_axis, DOWN, aligned_edge=RIGHT, buff=0.1)
        label_pt_y = create_text("Test Loss (Sai số) >", font_size=9, color=WHITE).rotate(PI/2)
        label_pt_y.next_to(axes_pt.y_axis, LEFT, buff=0.15)

        self.play(Create(axes_pt), Write(label_pt_x), Write(label_pt_y), run_time=1.5)

        # Vẽ đường cong lũy thừa (Chinchilla Loss Curve): L = E + A/x^0.45
        loss_curve = axes_pt.plot(
            lambda x: 0.5 + 2.8 / (x ** 0.45),
            x_range=[1.2, 9.5],
            color=PURPLE_B,
            stroke_width=3
        )
        self.play(Create(loss_curve), run_time=1.5)

        # Tạo các chấm mô hình GPT chạy dọc trên đường cong
        gpt1_dot = Dot(point=axes_pt.c2p(2, 0.5 + 2.8 / (2 ** 0.45)), color=WHITE, radius=0.1)
        gpt1_label = create_text("GPT-1", font_size=8).next_to(gpt1_dot, UR, buff=0.08)

        gpt2_dot = Dot(point=axes_pt.c2p(4.5, 0.5 + 2.8 / (4.5 ** 0.45)), color=WHITE, radius=0.1)
        gpt2_label = create_text("GPT-2", font_size=8).next_to(gpt2_dot, UR, buff=0.08)

        gpt3_dot = Dot(point=axes_pt.c2p(8.5, 0.5 + 2.8 / (8.5 ** 0.45)), color=YELLOW, radius=0.12)
        gpt3_label = create_text("GPT-3 (Khổng lồ)", font_size=9, color=YELLOW)
        gpt3_label.next_to(gpt3_dot, UR, buff=0.1)

        # Hiển thị các thế hệ mô hình trượt dọc theo đường Loss giảm
        self.play(FadeIn(gpt1_dot, shift=UP*0.1), Write(gpt1_label), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(gpt2_dot, shift=UP*0.1), Write(gpt2_label), run_time=0.8)
        self.wait(1.0)
        self.play(
            Transform(gpt2_dot.copy(), gpt3_dot),
            FadeIn(gpt3_dot),
            Write(gpt3_label),
            run_time=1.2
        )
        
        # Thẻ công thức Chinchilla ở cột bên phải
        card_x = 4.6
        card_w, card_h = 4.6, 1.7
        pt_card_bg = RoundedRectangle(width=card_w, height=card_h, color=PURPLE, fill_color="#181124", fill_opacity=0.9, corner_radius=0.1)
        pt_card_bg.move_to(RIGHT * card_x + UP * 2.1)
        pt_card_title = create_text("1. Huấn luyện sơ khởi (Chinchilla)", font_size=9, color=PURPLE_A)
        pt_card_title.next_to(pt_card_bg.get_top(), DOWN, buff=0.15)
        
        pt_card_formula = create_markup_text(
            "<i>L</i>(<i>N</i>, <i>D</i>) = <i>E</i> + <i>A</i>/<i>N</i><sup><i>α</i></sup> + <i>B</i>/<i>D</i><sup><i>β</i></sup>",
            font_size=10
        )
        pt_card_formula.next_to(pt_card_title, DOWN, buff=0.2)
        pt_card = VGroup(pt_card_bg, pt_card_title, pt_card_formula)

        self.play(FadeIn(pt_card, shift=LEFT * 0.3), run_time=1.0)
        self.wait(2.0)

        rect_e = SurroundingRectangle(get_text_part(pt_card_formula, "E"), color=YELLOW, stroke_width=1.5, buff=0.03) # highlight E
        explain_e = create_text("E: Sai số tối thiểu (Entropy ngôn ngữ)", font_size=7, color=YELLOW).next_to(pt_card_bg, DOWN, aligned_edge=LEFT, buff=0.1)
        
        rect_n = SurroundingRectangle(get_text_part(pt_card_formula, "A/Nα"), color=PURPLE_A, stroke_width=1.5, buff=0.03) # highlight A/N^α
        explain_n = create_text("A/N^α: Hiệu quả từ số tham số N", font_size=7, color=PURPLE_A).next_to(explain_e, DOWN, aligned_edge=LEFT, buff=0.08)

        rect_d = SurroundingRectangle(get_text_part(pt_card_formula, "B/Dβ"), color=BLUE_A, stroke_width=1.5, buff=0.03) # highlight B/D^β
        explain_d = create_text("B/D^β: Hiệu quả từ số lượng token D", font_size=7, color=BLUE_A).next_to(explain_n, DOWN, aligned_edge=LEFT, buff=0.08)

        self.play(Create(rect_e), FadeIn(explain_e, shift=UP*0.1), run_time=0.8)
        self.wait(4.0)
        self.play(Create(rect_n), FadeIn(explain_n, shift=UP*0.1), run_time=0.8)
        self.wait(4.0)
        self.play(Create(rect_d), FadeIn(explain_d, shift=UP*0.1), run_time=0.8)
        self.wait(15.0) # Đợi lời thoại giải thích cặn kẽ về luật lũy thừa và giới hạn compute pre-training

        # Dọn dẹp giai đoạn 2
        stage2_mobjects = VGroup(
            axes_pt, label_pt_x, label_pt_y, loss_curve, gpt1_dot, gpt1_label, gpt2_dot, gpt2_label, gpt3_dot, gpt3_label, 
            pt_card, rect_e, explain_e, rect_n, explain_n, rect_d, explain_d
        )
        self.play(FadeOut(stage2_mobjects), run_time=1.0)
        self.wait(0.5)


        # =====================================================================
        # GIAI ĐOẠN 3: CƠ CHẾ CĂN CHỈNH HÀNH VI (POST-TRAINING ALIGNMENT FILTER)
        # =====================================================================
        base_box = RoundedRectangle(width=2.2, height=1.3, color=PURPLE, fill_color="#181124", fill_opacity=0.8)
        base_box.shift(LEFT * 5.0 + DOWN * 0.5)
        base_text = create_text("Base LLM\n(GPT-3 thô)", font_size=10, color=PURPLE_A).move_to(base_box.get_center())

        filter_line = Line(UP * 2.2, DOWN * 2.5, color=GREEN, stroke_width=4)
        filter_line.shift(LEFT * 2.0)
        filter_label = create_text("Màng lọc Căn chỉnh\n(SFT & RLHF / DPO)", font_size=9, color=GREEN)
        filter_label.next_to(filter_line, UP, buff=0.15)

        chat_box = RoundedRectangle(width=2.2, height=1.3, color=GREEN, fill_color="#0e1612", fill_opacity=0.8)
        chat_box.shift(RIGHT * 1.0 + DOWN * 0.5)
        chat_text = create_text("Chat LLM\n(GPT-4 trợ lý)", font_size=10, color=GREEN_A).move_to(chat_box.get_center())

        prompt_box = RoundedRectangle(width=3.6, height=0.7, color=GRAY, fill_color="#222", fill_opacity=0.9, corner_radius=0.08)
        prompt_box.shift(LEFT * 5.0 + UP * 1.5)
        prompt_text = create_text("Prompt: Hãy giúp tôi...", font_size=9, color=WHITE).move_to(prompt_box.get_center())

        self.play(
            Create(base_box), Write(base_text),
            Create(filter_line), Write(filter_label),
            Create(chat_box), Write(chat_text),
            Create(prompt_box), Write(prompt_text),
            run_time=1.5
        )
        self.wait(1.0)

        # Chạy hoạt ảnh dòng chảy các hạt
        p1_start = base_box.get_right()
        p1_unsafe_end = filter_line.get_center() + DOWN * 0.8
        p1_gibberish_end = filter_line.get_center() + UP * 0.6
        p1_safe_end = chat_box.get_left()

        dot_safe = Dot(point=p1_start, color=WHITE, radius=0.08)
        dot_unsafe = Dot(point=p1_start, color=WHITE, radius=0.08)
        dot_gibberish = Dot(point=p1_start, color=WHITE, radius=0.08)

        lbl_safe = create_text("Hữu ích & An toàn", font_size=7, color=WHITE)
        lbl_safe.next_to(dot_safe, UP, buff=0.05)
        lbl_unsafe = create_text("Độc hại / Nguy hiểm", font_size=7, color=WHITE)
        lbl_unsafe.next_to(dot_unsafe, UP, buff=0.05)
        lbl_gibberish = create_text("Vòng lặp vô nghĩa", font_size=7, color=WHITE)
        lbl_gibberish.next_to(dot_gibberish, UP, buff=0.05)

        # Hạt 1: Độc hại
        self.play(
            dot_unsafe.animate.move_to(p1_unsafe_end),
            FadeIn(lbl_unsafe, shift=RIGHT * 0.1),
            run_time=1.0
        )
        self.play(
            dot_unsafe.animate.set_color(RED),
            lbl_unsafe.animate.set_color(RED),
            Flash(dot_unsafe, color=RED, flash_radius=0.15, num_lines=6),
            run_time=0.4
        )
        self.play(FadeOut(dot_unsafe), FadeOut(lbl_unsafe), run_time=0.4)

        # Hạt 2: Vô nghĩa
        self.play(
            dot_gibberish.animate.move_to(p1_gibberish_end),
            FadeIn(lbl_gibberish, shift=RIGHT * 0.1),
            run_time=1.0
        )
        self.play(
            dot_gibberish.animate.set_color(RED),
            lbl_gibberish.animate.set_color(RED),
            Flash(dot_gibberish, color=RED, flash_radius=0.15, num_lines=6),
            run_time=0.4
        )
        self.play(FadeOut(dot_gibberish), FadeOut(lbl_gibberish), run_time=0.4)

        # Hạt 3: Hữu ích
        self.play(
            dot_safe.animate.move_to(filter_line.get_center()),
            FadeIn(lbl_safe, shift=RIGHT * 0.1),
            run_time=1.0
        )
        self.play(
            dot_safe.animate.set_color(GREEN).move_to(p1_safe_end),
            lbl_safe.animate.set_color(GREEN).next_to(chat_box, UP, buff=0.1),
            Flash(filter_line.get_center(), color=GREEN, flash_radius=0.2, num_lines=8),
            run_time=1.0
        )
        self.play(Flash(chat_box, color=GREEN, flash_radius=0.4), run_time=0.6)
        self.wait(1.5)

        # Thẻ công thức Post-training ở bên phải (Căn ở x=4.6, thêm công thức KL-Divergence để tăng tính toán học)
        post_card_bg = RoundedRectangle(width=card_w, height=card_h, color=GREEN, fill_color="#0e1612", fill_opacity=0.9, corner_radius=0.1)
        post_card_bg.move_to(RIGHT * card_x + UP * 0.15)
        post_card_title = create_text("2. Căn chỉnh hành vi (Alignment)", font_size=9, color=GREEN_A)
        post_card_title.next_to(post_card_bg.get_top(), DOWN, buff=0.15)
        
        post_card_formula = create_markup_text(
            "max <i>E</i>[<i>R</i>(<i>x</i>,<i>y</i>)] - <i>β</i> KL(<i>P</i> || <i>P</i><sub>ref</sub>)",
            font_size=9
        )
        post_card_formula.next_to(post_card_title, DOWN, buff=0.2)
        post_card = VGroup(post_card_bg, post_card_title, post_card_formula)

        self.play(FadeIn(post_card, shift=LEFT * 0.3), run_time=1.0)
        self.wait(2.0)

        # PHÂN TÍCH CHI TIẾT TOÁN HỌC: Giải thích hàm phạt KL-Divergence
        rect_kl = SurroundingRectangle(get_text_part(post_card_formula, "β KL(P || Pref)"), color=GREEN_B, stroke_width=1.5, buff=0.03) # highlight KL term
        explain_kl = create_text("KL: Phạt mô hình lệch quá xa mô hình gốc", font_size=7, color=GREEN_B).next_to(post_card_bg, DOWN, aligned_edge=LEFT, buff=0.1)
        
        rect_r = SurroundingRectangle(get_text_part(post_card_formula, "E[R(x,y)]"), color=YELLOW, stroke_width=1.5, buff=0.03) # highlight E[R]
        explain_r = create_text("E[R]: Tối đa hóa điểm thưởng phản hồi", font_size=7, color=YELLOW).next_to(explain_kl, DOWN, aligned_edge=LEFT, buff=0.08)

        self.play(Create(rect_kl), FadeIn(explain_kl, shift=UP*0.1), run_time=0.8)
        self.wait(5.0)
        self.play(Create(rect_r), FadeIn(explain_r, shift=UP*0.1), run_time=0.8)
        self.wait(20.0) # Đợi lời thoại giải thích về mục tiêu hậu huấn luyện và cơ chế KL-divergence

        # Dọn dẹp giai đoạn 3
        stage3_mobjects = VGroup(base_box, base_text, filter_line, filter_label, chat_box, chat_text, prompt_box, prompt_text, dot_safe, lbl_safe, post_card, rect_kl, explain_kl, rect_r, explain_r)
        self.play(FadeOut(stage3_mobjects), run_time=1.0)
        self.wait(0.5)


        # =====================================================================
        # GIAI ĐOẠN 4: ĐỒ THỊ MỞ RỘNG THỜI ĐIỂM SUY LUẬN (TEST-TIME COMPUTE)
        # =====================================================================
        # Dựng đồ thị 2D: Accuracy vs Inference Compute Budget (Dịch trái x=-2.0)
        axes_tt = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 10],
            x_length=7,
            y_length=4.2,
            axis_config={"color": BLUE, "stroke_width": 2},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []}
        )
        axes_tt.shift(LEFT * 2.0 + DOWN * 0.2)

        label_tt_x = create_text("Thời gian suy nghĩ / Số mẫu (Inference Compute N) >", font_size=9, color=WHITE)
        label_tt_x.next_to(axes_tt.x_axis, DOWN, aligned_edge=RIGHT, buff=0.1)
        label_tt_y = create_text("Độ chính xác tác vụ (%) >", font_size=9, color=WHITE).rotate(PI/2)
        label_tt_y.next_to(axes_tt.y_axis, LEFT, buff=0.15)

        self.play(Create(axes_tt), Write(label_tt_x), Write(label_tt_y), run_time=1.5)

        # Vẽ đường cong Accuracy của Best-of-N và Search uốn cong hướng lên
        accuracy_curve = axes_tt.plot(
            lambda x: 20 + 65 * (1 - np.exp(-0.4 * (x - 1))),
            x_range=[1, 9.5],
            color=BLUE_B,
            stroke_width=3
        )
        self.play(Create(accuracy_curve), run_time=1.5)

        # Chấm điểm suy luận chuẩn (Standard decoding)
        std_dot = Dot(point=axes_tt.c2p(1, 20), color=RED, radius=0.1)
        std_label = create_text("Standard Decoding (1 Pass)", font_size=8, color=RED)
        std_label.next_to(std_dot, DR, buff=0.08)

        # Chấm điểm o1/R1 với compute suy luận cực lớn
        reason_dot = Dot(point=axes_tt.c2p(8, 20 + 65 * (1 - np.exp(-0.4 * (8 - 1)))), color=YELLOW, radius=0.12)
        reason_label = create_text("Reasoning (o1 / DeepSeek-R1)", font_size=9, color=YELLOW)
        reason_label.next_to(reason_dot, UL, buff=0.1)

        # Gióng đường từ Standard lên Reasoning để làm nổi bật độ chênh lệch
        growth_line = Arrow(std_dot.get_center(), reason_dot.get_center(), color=YELLOW, stroke_width=2.5, buff=0.1)
        angle = np.arctan2(reason_dot.get_center()[1] - std_dot.get_center()[1], reason_dot.get_center()[0] - std_dot.get_center()[0])
        growth_text = create_text("+60% Accuracy Delta", font_size=9, color=YELLOW)
        growth_text.next_to(growth_line, LEFT, buff=0.1).rotate(angle)

        self.play(FadeIn(std_dot, shift=UP*0.1), Write(std_label), run_time=0.8)
        self.wait(1.5)
        self.play(
            GrowArrow(growth_line),
            FadeIn(reason_dot, shift=UR*0.15),
            Write(reason_label),
            Write(growth_text),
            run_time=1.5
        )
        self.play(Flash(reason_dot, color=YELLOW, flash_radius=0.25, num_lines=12), run_time=0.8)
        self.wait(1.5)

        # Thẻ công thức Test-time ở bên phải (Căn ở x=4.6, y=-1.8)
        tt_card_bg = RoundedRectangle(width=card_w, height=card_h, color=BLUE, fill_color="#0b1324", fill_opacity=0.9, corner_radius=0.1)
        tt_card_bg.move_to(RIGHT * card_x + DOWN * 1.8)
        tt_card_title = create_text("3. Mở rộng lúc suy luận (Best-of-N)", font_size=9, color=BLUE_A)
        tt_card_title.next_to(tt_card_bg.get_top(), DOWN, buff=0.15)
        
        tt_card_formula = create_markup_text(
            "<i>P</i>(correct) = 1 - (1 - <i>p</i>)<sup><i>N</i></sup>",
            font_size=10
        )
        tt_card_formula.next_to(tt_card_title, DOWN, buff=0.2)
        tt_card = VGroup(tt_card_bg, tt_card_title, tt_card_formula)

        self.play(FadeIn(tt_card, shift=LEFT * 0.3), run_time=1.0)
        self.wait(2.0)

        # PHÂN TÍCH CHI TIẾT TOÁN HỌC: Giải thích các biến số trong công thức xác suất Best-of-N
        rect_n_samples = SurroundingRectangle(get_text_part(tt_card_formula, "N"), color=BLUE_A, stroke_width=1.5, buff=0.03) # highlight N
        explain_n_samples = create_text("N: Số mẫu sinh ra lúc suy luận", font_size=7, color=BLUE_A).next_to(tt_card_bg, DOWN, aligned_edge=LEFT, buff=0.1)
        
        rect_p_single = SurroundingRectangle(get_text_part(tt_card_formula, "p"), color=YELLOW, stroke_width=1.5, buff=0.03) # highlight p
        explain_p_single = create_text("p: Xác suất 1 mẫu đơn lẻ giải đúng", font_size=7, color=YELLOW).next_to(explain_n_samples, DOWN, aligned_edge=LEFT, buff=0.08)

        self.play(Create(rect_n_samples), FadeIn(explain_n_samples, shift=UP*0.1), run_time=0.8)
        self.wait(5.0)
        self.play(Create(rect_p_single), FadeIn(explain_p_single, shift=UP*0.1), run_time=0.8)
        self.wait(22.0) # Đợi lời thoại giải thích về Best-of-N và test-time compute scaling laws

        # Dọn dẹp giai đoạn 4
        stage4_mobjects = VGroup(
            axes_tt, accuracy_curve, std_dot, std_label, reason_dot, reason_label, growth_line, growth_text, 
            tt_card, label_tt_x, label_tt_y, rect_n_samples, explain_n_samples, rect_p_single, explain_p_single
        )
        self.play(FadeOut(stage4_mobjects), run_time=1.0)
        self.wait(0.5)


        # =====================================================================
        # GIAI ĐOẠN 5: TỔNG KẾT & QUAY LẠI HỆ TRỤC 3D TOÀN CẢNH
        # =====================================================================
        # Hiển thị lại hệ trục và lưới phối cảnh 3D
        self.play(FadeIn(origin), Create(floor_grid), run_time=1.0)
        self.play(
            GrowArrow(axis_x), Write(label_x),
            GrowArrow(axis_y), Write(label_y),
            GrowArrow(axis_z), Write(label_z),
            run_time=1.2
        )

        # Định vị các điểm tọa độ 3D chính xác
        gpt3_pt = origin_pt + RIGHT * 2.5
        gpt4_pt = origin_pt + RIGHT * 2.5 + UP * 1.8
        o1_pt = gpt4_pt + DR * 1.0
        
        o1_floor = gpt3_pt + DR * 1.0
        o1_y_shifted = (origin_pt + UP * 1.8) + DR * 1.0
        o1_z = origin_pt + DR * 1.0
        proj_y_gpt4 = origin_pt + UP * 1.8

        gpt3_dot = Dot(point=gpt3_pt, color=PURPLE_A, radius=0.12)
        gpt3_label = create_text("GPT-3 (Base)", font_size=8, color=PURPLE_A).next_to(gpt3_dot, UL, buff=0.12)

        gpt4_dot = Dot(point=gpt4_pt, color=GREEN_A, radius=0.12)
        gpt4_label = create_text("GPT-4 (Chat)", font_size=8, color=GREEN_A).next_to(gpt4_dot, UL, buff=0.12)
        link_y = DashedLine(gpt3_dot.get_center(), gpt4_dot.get_center(), color=GRAY_A, stroke_width=1.5)

        o1_dot = Dot(point=o1_pt, color=BLUE_A, radius=0.12)
        o1_label = create_text("o1 / DeepSeek-R1", font_size=9, color=YELLOW).next_to(o1_dot, UR, buff=0.15)
        link_z = DashedLine(gpt4_dot.get_center(), o1_dot.get_center(), color=GRAY_A, stroke_width=1.5)
        link_gpt4_to_o1 = Arrow(gpt4_pt, o1_pt, color=YELLOW, stroke_width=2.5, buff=0.1)

        # Các đường gióng hộp tọa độ 3D của o1
        proj_o1_floor_to_o1 = DashedLine(o1_pt, o1_floor, color=BLUE, stroke_width=1.2, stroke_opacity=0.3)
        proj_o1_floor_to_gpt3 = DashedLine(o1_floor, gpt3_pt, color=BLUE, stroke_width=1.2, stroke_opacity=0.3)
        proj_o1_floor_to_z = DashedLine(o1_floor, o1_z, color=BLUE, stroke_width=1.2, stroke_opacity=0.3)
        proj_o1_to_yshifted = DashedLine(o1_pt, o1_y_shifted, color=BLUE, stroke_width=1.2, stroke_opacity=0.3)
        proj_yshifted_to_y = DashedLine(o1_y_shifted, proj_y_gpt4, color=BLUE, stroke_width=1.2, stroke_opacity=0.3)
        proj_yshifted_to_z = DashedLine(o1_y_shifted, o1_z, color=BLUE, stroke_width=1.2, stroke_opacity=0.3)

        self.play(
            FadeIn(gpt3_dot), Write(gpt3_label),
            Create(link_y), FadeIn(gpt4_dot), Write(gpt4_label),
            run_time=1.5
        )
        self.play(
            Create(proj_o1_floor_to_z), Create(proj_o1_floor_to_gpt3), Create(proj_o1_floor_to_o1),
            Create(proj_o1_to_yshifted), Create(proj_yshifted_to_y), Create(proj_yshifted_to_z),
            Create(link_gpt4_to_o1),
            FadeIn(o1_dot), Write(o1_label),
            run_time=2.0
        )
        self.play(Flash(o1_dot, color=YELLOW, flash_radius=0.25, num_lines=12), run_time=1.0)
        self.wait(18.0) # Đợi lời thoại tổng kết lại mối quan hệ giữa 3 trục mở rộng và hướng đi tương lai

        # Dọn dẹp toàn bộ màn hình kết thúc phân cảnh
        self.play(
            FadeOut(main_title),
            FadeOut(origin), FadeOut(floor_grid),
            FadeOut(axis_x), FadeOut(label_x), FadeOut(gpt3_dot), FadeOut(gpt3_label),
            FadeOut(axis_y), FadeOut(label_y), FadeOut(gpt4_dot), FadeOut(gpt4_label), FadeOut(link_y),
            FadeOut(axis_z), FadeOut(label_z), FadeOut(o1_dot), FadeOut(o1_label),
            FadeOut(proj_o1_floor_to_o1), FadeOut(proj_o1_floor_to_gpt3), FadeOut(proj_o1_floor_to_z),
            FadeOut(proj_o1_to_yshifted), FadeOut(proj_yshifted_to_y), FadeOut(proj_yshifted_to_z),
            FadeOut(link_gpt4_to_o1),
            run_time=1.5
        )
        self.wait(1.0)
