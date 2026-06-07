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


class Scene1_4(Scene):
    def construct(self):
        # =========================================================================
        # VOICEOVER (Scene 1.4) [Trích từ full_video_script.md]
        # Lời thoại:
        #   - "Generator là bất kỳ thuật toán nào nhận một input sequence và language
        #     model rồi sinh ra output sequence. Khi gọi một LLM API thông thường, ta
        #     có thể xem đó là một generator."
        # 
        #   - "Meta-generator là chiến lược cấp cao hơn: gọi generator nhiều lần, dùng
        #     external information, hoặc chọn output tốt nhất bằng một mô hình riêng.
        #     Lý do dùng meta-generator là để generate more nhằm cải thiện task
        #     performance, kết hợp nhiều mô hình như verifier hay retriever, và đưa
        #     thông tin bên ngoài như tools hay feedback vào generation."
        # 
        #   - "Nội dung chính của chúng ta gồm ba phần: primitive generators,
        #     meta-generators, và efficient meta-generation, tiếp theo là buổi thảo
        #     luận panel. Chúng ta cũng có thể truy cập các tài nguyên trực tuyến để
        #     xem slide, ví dụ code và danh sách tài liệu đọc thêm."
        # 
        #   - "Từ "primitive" ở đây không có nghĩa là các phương pháp này không quan
        #     trọng. Chúng ta có thể hiểu chúng là các primitives theo nghĩa building
        #     blocks – tức là những khối cơ bản để xây dựng các thuật toán
        #     meta-generation phức tạp hơn. Vì thế, trước khi nói về meta-generator,
        #     chúng ta phải hiểu cách một generator sinh ra một chuỗi đơn lẻ."
        # =========================================================================

        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH
        # =====================================================================
        main_title = create_text("Khung Khái Niệm Generator & Meta-Generator", font_size=20, color=BLUE_A)
        main_title.to_edge(UP, buff=0.4)
        self.play(Write(main_title))
        self.wait(2.0)

        # Tọa độ gốc cho sơ đồ khối bên trái
        # Dịch sang LEFT * 2.9 (x = -2.9) để ngăn chặn Output (y) đè lên khung Định nghĩa toán học
        diag_center = LEFT * 2.9 + DOWN * 0.4

        # =====================================================================
        # BƯỚC 2: DỰNG SƠ ĐỒ KHỐI GENERATOR (BỘ SINH CƠ BẢN g)
        # VOICEOVER [Trích từ full_video_script.md]
        # Lời thoại: "Generator là bất kỳ thuật toán nào nhận một input sequence và 
        # language model rồi sinh ra output sequence. Khi gọi một LLM API thông thường, 
        # chúng ta có thể xem đó là một generator."
        # =====================================================================
        # 1. Hộp Generator (g)
        gen_box = RoundedRectangle(width=2.8, height=1.1, color=BLUE_C, fill_color="#0e1b29", fill_opacity=0.9, corner_radius=0.08)
        gen_box.move_to(diag_center + UP * 0.9)
        gen_title = create_text("Bộ Sinh", font_size=10, color=WHITE)
        gen_sub = create_text("Generator (g)", font_size=8.5, color=BLUE_A)
        gen_sub.next_to(gen_title, DOWN, buff=0.06)
        gen_text = VGroup(gen_title, gen_sub)
        gen_text.move_to(gen_box.get_center())
        gen_group = VGroup(gen_box, gen_text)

        # 2. Hộp Đầu vào (Input x) bên ngoài
        in_box = RoundedRectangle(width=1.5, height=0.7, color=GRAY_A, fill_color="#1e1e1e", fill_opacity=0.9, corner_radius=0.06)
        in_box.move_to(diag_center + LEFT * 2.6 + UP * 0.9)
        in_text = create_text("Input (x)", font_size=10, color=WHITE)
        in_text.move_to(in_box.get_center())
        in_group = VGroup(in_box, in_text)

        # 3. Hộp Đầu ra (Output y) tạm thời ở ngang hàng (Giai đoạn Generator đơn lẻ)
        out_temp_box = RoundedRectangle(width=1.5, height=0.7, color=GRAY_A, fill_color="#1e1e1e", fill_opacity=0.9, corner_radius=0.06)
        out_temp_box.move_to(diag_center + RIGHT * 2.6 + UP * 0.9)
        out_temp_text = create_text("Output (y)", font_size=10, color=WHITE)
        out_temp_text.move_to(out_temp_box.get_center())
        out_temp_group = VGroup(out_temp_box, out_temp_text)

        # Mũi tên từ Input vào Generator
        arrow_in = Line(
            in_box.get_right(), gen_box.get_left(), 
            color=GRAY_A, stroke_width=1.8, buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)

        # Mũi tên tạm thời từ Generator ra Output y
        arrow_out_temp = Line(
            gen_box.get_right(), out_temp_box.get_left(),
            color=GRAY_A, stroke_width=1.8, buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)

        # Hoạt họa hiển thị hệ Generator cơ bản
        self.play(
            FadeIn(in_group, shift=RIGHT * 0.2),
            FadeIn(gen_group, shift=RIGHT * 0.2),
            Create(arrow_in),
            run_time=1.0
        )
        self.play(
            Create(arrow_out_temp),
            FadeIn(out_temp_group, shift=RIGHT * 0.2),
            run_time=1.0
        )
        self.wait(4.0)


        # =====================================================================
        # BƯỚC 3: HIỂN THỊ CÔNG THỨC GENERATOR (g) VÀ CHÚ THÍCH NGOẶC NHỌN (BRACES)
        # =====================================================================
        # Tiêu đề khu vực công thức (Đưa vào trong khung)
        eq_title = create_text("Định Nghĩa Toán Học", font_size=11, color=GRAY_A)
        eq_title.move_to(RIGHT * 3.4 + UP * 1.7)
        self.play(Write(eq_title), run_time=0.8)

        # Tạo Khung chứa công thức toán học (Tăng chiều cao lên 2.0 để chứa được Brace giải thích)
        eq_box = RoundedRectangle(width=5.2, height=2.0, color=BLUE_E, fill_color="#0e1726", fill_opacity=0.6, corner_radius=0.08)
        eq_box.move_to(RIGHT * 3.4 + UP * 1.0)
        self.play(FadeIn(eq_box), run_time=0.8)

        # Xây dựng công thức Generator g từng thành phần rời rạc xếp ngang để gán Brace chính xác
        # y ~ g(y | x; p_θ, φ)
        y_part = create_markup_text("<span color='#ffff00'><i>y</i></span>", font_size=18)
        sim_part = create_text(" ~ ", font_size=18, color=GRAY_A)
        g_part = create_markup_text("<span color='#88c0d0'><i>g</i></span>", font_size=18)
        lparen_part = create_text("(", font_size=18, color=WHITE)
        y2_part = create_markup_text("<span color='#ffff00'><i>y</i></span>", font_size=18)
        pipe_part = create_text(" | ", font_size=18, color=WHITE)
        x_part = create_markup_text("<span color='#ffffff'><i>x</i></span>", font_size=18)
        semi_part = create_text("; ", font_size=18, color=WHITE)
        p_part = create_markup_text("<span color='#8fbcbb'><i>p</i><sub><i>θ</i></sub></span>", font_size=18)
        comma_part = create_text(", ", font_size=18, color=WHITE)
        phi_part = create_markup_text("<span color='#d08770'><i>φ</i></span>", font_size=18)
        rparen_part = create_text(")", font_size=18, color=WHITE)

        gen_eq = VGroup(
            y_part, sim_part, g_part, lparen_part, y2_part, pipe_part, x_part, semi_part, p_part, comma_part, phi_part, rparen_part
        )
        gen_eq.arrange(RIGHT, buff=0.04)
        gen_eq.move_to(RIGHT * 3.4 + UP * 1.1)

        # Viết công thức ra màn hình bên trong khung
        self.play(Write(gen_eq), run_time=1.2)
        self.wait(3.0)

        # 1. Chú thích ngoặc nhọn cho g (Thuật toán chọn từ / decoding)
        brace_g = Brace(g_part, direction=DOWN, color=BLUE_A, buff=0.1)
        lbl_g = create_text("Chiến lược chọn từ\n(decoding)", font_size=8, color=BLUE_A)
        lbl_g.next_to(brace_g, DOWN, buff=0.05)
        
        self.play(Create(brace_g), Write(lbl_g), run_time=0.8)
        self.wait(4.5)

        # 2. Chú thích cho p_θ (Mô hình ngôn ngữ) - Ẩn chú thích cũ để tránh đè chữ
        brace_p = Brace(p_part, direction=DOWN, color=GREEN_A, buff=0.1)
        lbl_p = create_text("Mô hình ngôn ngữ\n(Causal LLM)", font_size=8, color=GREEN_A)
        lbl_p.next_to(brace_p, DOWN, buff=0.05)

        self.play(
            FadeOut(brace_g), FadeOut(lbl_g),
            Create(brace_p), Write(lbl_p),
            run_time=0.8
        )
        self.wait(4.5)

        # 3. Chú thích cho φ (Siêu tham số)
        brace_phi = Brace(phi_part, direction=DOWN, color=ORANGE, buff=0.1)
        lbl_phi = create_text("Siêu tham số\n(Temp, Top-p, Top-k...)", font_size=8, color=ORANGE)
        lbl_phi.next_to(brace_phi, DOWN, buff=0.05)

        self.play(
            FadeOut(brace_p), FadeOut(lbl_p),
            Create(brace_phi), Write(lbl_phi),
            run_time=0.8
        )
        self.wait(4.5)
        self.play(FadeOut(brace_phi), FadeOut(lbl_phi), run_time=0.6)

        # 4. Hiển thị bảng ví dụ cho g ở phía dưới (Dịch chuyển xuống DOWN * 1.5 để tránh đè chữ)
        eg_bg = RoundedRectangle(width=5.2, height=1.6, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.8, corner_radius=0.08)
        eg_bg.move_to(RIGHT * 3.4 + DOWN * 1.5)
        
        eg_title = create_text("Ví dụ thuật toán bộ sinh g:", font_size=9, color=BLUE_A)
        eg_item1 = create_text("• Giải mã tham lam (Greedy decoding)", font_size=8, color=WHITE)
        eg_item2 = create_text("• Lấy mẫu nhiệt độ (Temperature sampling)", font_size=8, color=WHITE)
        eg_item3 = create_text("• Tìm kiếm chùm (Beam search)", font_size=8, color=WHITE)
        
        eg_items_group = VGroup(eg_title, eg_item1, eg_item2, eg_item3).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        eg_items_group.move_to(eg_bg.get_center() + LEFT * 0.2)
        eg_group = VGroup(eg_bg, eg_items_group)

        self.play(FadeIn(eg_group, shift=UP * 0.15), run_time=1.0)
        self.wait(6.0)


        # =====================================================================
        # BƯỚC 4: CHUYỂN ĐỔI SANG META-GENERATOR (BỘ ĐIỀU PHỐI G)
        # VOICEOVER [Trích từ full_video_script.md]
        # Lời thoại: "Meta-generator là chiến lược cấp cao hơn: gọi generator nhiều lần, 
        # dùng thông tin bên ngoài, hoặc chọn output tốt nhất bằng một mô hình riêng. 
        # Lý do chúng ta dùng meta-generator là để sinh thêm nhằm cải thiện hiệu năng 
        # của hệ thống sinh, kết hợp nhiều mô hình như verifier hay retriever, và đưa 
        # thông tin bên ngoài như công cụ hoặc phản hồi vào quá trình sinh."
        # =====================================================================
        # 1. Biến đổi sơ đồ khối bên trái
        # Chuẩn bị hộp Evaluator (v) màu xanh lá
        eval_box = RoundedRectangle(width=2.8, height=1.1, color=GREEN_C, fill_color="#0d2417", fill_opacity=0.9, corner_radius=0.08)
        eval_box.move_to(diag_center + DOWN * 1.3)
        eval_title = create_text("Bộ Đánh Giá", font_size=10, color=WHITE)
        eval_sub = create_text("Evaluator (v)", font_size=8.5, color=GREEN_A)
        eval_sub.next_to(eval_title, DOWN, buff=0.06)
        eval_text = VGroup(eval_title, eval_sub)
        eval_text.move_to(eval_box.get_center())
        eval_group = VGroup(eval_box, eval_text)

        # Hộp Đầu ra thực tế dịch xuống hàng của Evaluator
        out_box = RoundedRectangle(width=1.5, height=0.7, color=GRAY_A, fill_color="#1e1e1e", fill_opacity=0.9, corner_radius=0.06)
        out_box.move_to(diag_center + LEFT * 2.6 + DOWN * 1.3)
        out_text = create_text("Output (y)", font_size=10, color=WHITE)
        out_text.move_to(out_box.get_center())
        out_group = VGroup(out_box, out_text)

        # Mũi tên nối Generator xuống Evaluator
        arrow_down = Line(
            gen_box.get_bottom(), eval_box.get_top(), 
            color=GRAY_A, stroke_width=1.8, buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)
        arrow_down_label = create_text("Mẫu sinh (y)", font_size=8, color=GRAY_A)
        arrow_down_label.next_to(arrow_down, RIGHT, buff=0.1)

        # Vòng lặp phản hồi (Feedback loop) uốn cong ra phía NGOÀI (bên Phải)
        # Sửa đổi angle=PI/2.5 (dương) để cong sang phải, tránh đè lên các hộp
        arrow_loop = CurvedArrow(
            eval_box.get_right() + RIGHT * 0.1, gen_box.get_right() + RIGHT * 0.1, 
            angle=PI/2.5, color=YELLOW_B, stroke_width=1.8
        )
        loop_line1 = create_text("Phản hồi /", font_size=8, color=YELLOW_B)
        loop_line2 = create_text("Thử lại", font_size=8, color=YELLOW_B)
        loop_label = VGroup(loop_line1, loop_line2).arrange(DOWN, buff=0.05)
        # Định vị nhãn nằm sát lề phải của vòng cung
        loop_label.next_to(arrow_loop, RIGHT, buff=0.15)

        # Mũi tên từ Evaluator ra Output mới
        arrow_out_new = Line(
            eval_box.get_left(), out_box.get_right(),
            color=GRAY_A, stroke_width=1.8, buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)

        # Hộp Meta-Generator G màu vàng lớn bao bọc cụm bên trong
        # Chiều rộng 4.4, đặt tại LEFT * 2.3 để ôm sát sơ đồ và vòng lặp phản hồi, tránh thừa lề phải
        meta_box = RoundedRectangle(width=4.4, height=4.2, color=YELLOW_C, fill_color="#1c1b0c", fill_opacity=0.4, corner_radius=0.12)
        meta_box.move_to(LEFT * 2.3 + DOWN * 0.6)
        meta_box_title = create_text("Bộ Điều Phối (Meta-Generator) G", font_size=11, color=YELLOW_B)
        meta_box_title.next_to(meta_box.get_top(), DOWN, buff=0.15)
        meta_group = VGroup(meta_box, meta_box_title)

        # Khung chứa công thức toán học mới cho Meta-Generator G (Tăng chiều cao lên 2.0)
        eq_box_G = RoundedRectangle(width=5.2, height=2.0, color=YELLOW_E, fill_color="#1c1b0c", fill_opacity=0.6, corner_radius=0.08)
        eq_box_G.move_to(RIGHT * 3.4 + UP * 1.0)

        # Bắt đầu chạy hiệu ứng chuyển đổi sơ đồ khối bên trái
        self.play(
            FadeOut(arrow_out_temp),
            FadeOut(out_temp_group, shift=LEFT * 0.2),
            run_time=0.8
        )
        self.play(
            FadeIn(eval_group, shift=UP * 0.2),
            Create(arrow_down),
            Write(arrow_down_label),
            run_time=1.0
        )
        self.play(
            Create(arrow_loop),
            Write(loop_label),
            run_time=0.8
        )
        self.play(
            Create(meta_box),
            Write(meta_box_title),
            run_time=1.0
        )
        self.play(
            Create(arrow_out_new),
            FadeIn(out_group, shift=LEFT * 0.2),
            run_time=0.8
        )
        self.wait(3.0)

        # 2. Chuyển đổi công thức toán học bên phải
        # Xây dựng các cụm rời rạc cho công thức Meta-Generator: y ~ G(y | x; g1, g2, ..., gG, φ)
        y_part_G = create_markup_text("<span color='#ffff00'><i>y</i></span>", font_size=18)
        sim_part_G = create_text(" ~ ", font_size=18, color=GRAY_A)
        G_part_G = create_markup_text("<span color='#ebcb8b'><i>G</i></span>", font_size=18)
        lparen_part_G = create_text("(", font_size=18, color=WHITE)
        y2_part_G = create_markup_text("<span color='#ffff00'><i>y</i></span>", font_size=18)
        pipe_part_G = create_text(" | ", font_size=18, color=WHITE)
        x_part_G = create_markup_text("<span color='#ffffff'><i>x</i></span>", font_size=18)
        semi_part_G = create_text("; ", font_size=18, color=WHITE)
        g_list_part = create_markup_text("<span color='#88c0d0'><i>g</i><sub>1</sub>, <i>g</i><sub>2</sub>, ..., <i>g</i><sub><i>G</i></sub></span>", font_size=18)
        comma_part_G = create_text(", ", font_size=18, color=WHITE)
        phi_part_G = create_markup_text("<span color='#d08770'><i>φ</i></span>", font_size=18)
        rparen_part_G = create_text(")", font_size=18, color=WHITE)

        meta_eq = VGroup(
            y_part_G, sim_part_G, G_part_G, lparen_part_G, y2_part_G, pipe_part_G, x_part_G, semi_part_G, g_list_part, comma_part_G, phi_part_G, rparen_part_G
        )
        meta_eq.arrange(RIGHT, buff=0.04)
        meta_eq.move_to(RIGHT * 3.4 + UP * 1.1)

        # Chuyển đổi đồng bộ cả công thức và khung chứa sang màu vàng của Meta-Generator G
        self.play(
            ReplacementTransform(gen_eq, meta_eq),
            ReplacementTransform(eq_box, eq_box_G),
            run_time=1.5
        )
        self.wait(3.0)

        # 3. Chú thích ngoặc nhọn cho công thức Meta-Generator G
        # Chú thích cho G (Chiến lược điều phối cấp cao)
        brace_G_lbl = Brace(G_part_G, direction=DOWN, color=YELLOW_A, buff=0.1)
        lbl_G_desc = create_text("Chiến lược điều phối cấp cao\n(Chain, Parallel, Tree...)", font_size=8, color=YELLOW_A)
        lbl_G_desc.next_to(brace_G_lbl, DOWN, buff=0.05)

        self.play(Create(brace_G_lbl), Write(lbl_G_desc), run_time=0.8)
        self.wait(4.5)

        # Chú thích cho các bộ sinh g_i
        brace_gi = Brace(g_list_part, direction=DOWN, color=BLUE_A, buff=0.1)
        lbl_gi_desc = create_text("Các bộ sinh cơ bản\n(coi như Black-box)", font_size=8, color=BLUE_A)
        lbl_gi_desc.next_to(brace_gi, DOWN, buff=0.05)

        self.play(
            FadeOut(brace_G_lbl), FadeOut(lbl_G_desc),
            Create(brace_gi), Write(lbl_gi_desc),
            run_time=0.8
        )
        self.wait(4.5)

        # Chú thích cho φ (Bộ đánh giá và công cụ ngoài)
        brace_phi_G = Brace(phi_part_G, direction=DOWN, color=ORANGE, buff=0.1)
        lbl_phi_G_desc = create_text("Bộ đánh giá (Reward model),\ncông cụ ngoài, số mẫu sinh...", font_size=8, color=ORANGE)
        lbl_phi_G_desc.next_to(brace_phi_G, DOWN, buff=0.05)

        self.play(
            FadeOut(brace_gi), FadeOut(lbl_gi_desc),
            Create(brace_phi_G), Write(lbl_phi_G_desc),
            run_time=0.8
        )
        self.wait(4.5)
        self.play(FadeOut(brace_phi_G), FadeOut(lbl_phi_G_desc), run_time=0.6)

        # 4. Thay đổi bảng ví dụ ở dưới sang Meta-Generator (Dịch xuống DOWN * 1.5, đồng bộ width=5.2)
        eg_bg_G = RoundedRectangle(width=5.2, height=2.0, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.8, corner_radius=0.08)
        eg_bg_G.move_to(RIGHT * 3.4 + DOWN * 1.5)

        eg_title_G = create_text("Chiến lược của Meta-Generator G:", font_size=9, color=YELLOW_A)
        eg_item1_G = create_text("• Chuỗi lập luận (Chaining - CoT, Self-Ask)", font_size=8, color=WHITE)
        eg_item2_G = create_text("• Lấy mẫu song song & Lọc (Best-of-N, Voting)", font_size=8, color=WHITE)
        eg_item3_G = create_text("• Duyệt cây & Quay lui (ToT, MCTS)", font_size=8, color=WHITE)
        eg_item4_G = create_text("• Tinh chỉnh & Tự sửa lỗi (Self-Correction)", font_size=8, color=WHITE)

        eg_items_group_G = VGroup(eg_title_G, eg_item1_G, eg_item2_G, eg_item3_G, eg_item4_G).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        eg_items_group_G.move_to(eg_bg_G.get_center() + LEFT * 0.2)
        eg_group_G = VGroup(eg_bg_G, eg_items_group_G)

        self.play(
            ReplacementTransform(eg_group, eg_group_G),
            run_time=1.2
        )
        self.wait(8.0)

        # Dọn dẹp giai đoạn 1 & 2 để chuẩn bị xuất hiện đề cương khóa học
        all_stage1_2 = VGroup(
            in_group, gen_group, eval_group, out_group, meta_group,
            arrow_in, arrow_down, arrow_down_label, arrow_loop, loop_label, arrow_out_new,
            eq_title, meta_eq, eg_group_G, eq_box_G
        )
        self.play(FadeOut(all_stage1_2, shift=DOWN * 0.2), run_time=1.2)
        self.wait(1.0)


        # =====================================================================
        # BƯỚC 5: ĐỀ CƯƠNG CHI TIẾT LOẠT VIDEO (SỰ KIỆN KẾT THÚC CHƯƠNG I)
        # VOICEOVER [Trích từ full_video_script.md]
        # Lời thoại: "Nội dung chính của chúng ta gồm ba phần: primitive generators, 
        # meta-generators, và efficient meta-generation, tiếp theo là buổi thảo luận panel. 
        # Chúng ta cũng có thể truy cập các tài nguyên trực tuyến để xem slide, ví dụ code 
        # và danh sách tài liệu đọc thêm. Từ 'primitive' ở đây không có nghĩa là các 
        # phương pháp này không quan trọng. Chúng ta có thể hiểu chúng là các primitives 
        # theo nghĩa building blocks – tức là những khối cơ bản để xây dựng các thuật toán 
        # meta-generation phức tạp hơn. Vì thế, trước khi nói về meta-generator, chúng ta 
        # phải hiểu cách một generator sinh ra một chuỗi đơn lẻ."
        # =====================================================================
        outline_title = create_markup_text("ĐỀ CƯƠNG CHI TIẾT LOẠT BÀI HỌC", font_size=20, color=BLUE_A)
        outline_title.move_to(UP * 2.5)
        
        outline_underline = Line(
            outline_title.get_left() + DOWN * 0.15,
            outline_title.get_right() + DOWN * 0.15,
            color=BLUE_C, stroke_width=1.8
        )

        self.play(
            Write(outline_title),
            Create(outline_underline),
            run_time=1.2
        )
        self.wait(1.5)

        # Định vị các phần trong đề cương giữa màn hình
        outline_y_positions = [1.2, 0.3, -0.6, -1.5, -2.4]
        
        # Danh sách đề cương loạt bài học chi tiết nhất
        items_data = [
            {
                "part": "Chương I",
                "title": "Kỷ nguyên mở rộng tính toán lúc suy luận (Inference Scaling Laws)",
                "speaker": "Giới thiệu chung & Vai trò của Test-Time Compute | Diễn giả: Sean Welleck (CMU)",
                "color": BLUE_B
            },
            {
                "part": "Chương II",
                "title": "Bộ sinh cơ bản ở cấp độ Token (Primitive Generators)",
                "speaker": "Greedy, Beam Search, Temperature, Truncation & Ràng buộc | Diễn giả: Matthew Finlayson (USC)",
                "color": GREEN_A
            },
            {
                "part": "Chương III",
                "title": "Bộ điều phối cấp cao ở cấp độ Chuỗi (Meta-Generators)",
                "speaker": "Kỹ thuật Chaining, Parallel (Voting, MBR), Tree Search & Self-Correction | Diễn giả: Sean Welleck (CMU)",
                "color": YELLOW_A
            },
            {
                "part": "Chương IV",
                "title": "Hiệu năng hệ thống phần cứng (Systems Efficiency)",
                "speaker": "Memory-bound vs Compute-bound, KV Cache & Speculative Decoding | Diễn giả: Hailey Schoelkopf",
                "color": ORANGE
            },
            {
                "part": "Tọa Đàm",
                "title": "Phiên thảo luận nhóm Panel của các chuyên gia hàng đầu",
                "speaker": "Định hướng tương lai Test-time compute | Điều phối: Ilia Kulikov (Meta AI)",
                "color": RED_A
            }
        ]

        outline_group = VGroup()
        chapter_mobjects = []

        for idx, data in enumerate(items_data):
            y_pos = outline_y_positions[idx]
            
            # Tiêu đề chương
            item_header = create_markup_text(
                f"<b>{data['part']}:</b> {data['title']}", 
                font_size=9.5, 
                color=data['color']
            )
            item_header.move_to(LEFT * 5.0 + UP * y_pos, aligned_edge=LEFT)
            
            # Chi tiết nội dung và tên diễn giả bên dưới
            item_speaker = create_text(
                data['speaker'], 
                font_size=8.0, 
                color=GRAY_A
            )
            item_speaker.next_to(item_header, DOWN, buff=0.06, aligned_edge=LEFT)
            
            item_group = VGroup(item_header, item_speaker)
            chapter_mobjects.append(item_group)
            outline_group.add(item_group)

            # Hiệu ứng highlight động: làm mờ các chương trước để làm nổi bật chương đang hiển thị
            if idx > 0:
                self.play(
                    *[item.animate.set_opacity(0.35) for item in chapter_mobjects[:-1]],
                    FadeIn(item_group, shift=LEFT * 0.2),
                    run_time=1.0
                )
            else:
                self.play(FadeIn(item_group, shift=LEFT * 0.2), run_time=1.0)
            
            self.wait(4.5)

        # Kết thúc chương: Sáng lại toàn bộ các phần để tổng kết
        self.play(
            *[item.animate.set_opacity(1.0) for item in chapter_mobjects],
            run_time=1.2
        )
        self.wait(6.0)

        # Trượt toàn bộ đề cương biến mất để kết thúc chương I
        self.play(
            FadeOut(outline_title),
            FadeOut(outline_underline),
            FadeOut(outline_group, shift=UP * 0.2),
            run_time=1.5
        )
        self.wait(1.5)
