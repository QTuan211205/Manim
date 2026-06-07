import os
import tempfile
from manim import *

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

class Scene1_1(Scene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng của 3B1B
        self.camera.background_color = "#111111"

        # Lưới tọa độ mờ nền sau tạo kết cấu đồ họa chuyên nghiệp
        grid = VGroup()
        for x in np.arange(-7.5, 8.0, 0.5):
            grid.add(Line(UP * 4.5, DOWN * 4.5, stroke_width=0.4, color=GRAY, stroke_opacity=0.06))
        for y in np.arange(-4.5, 5.0, 0.5):
            grid.add(Line(LEFT * 7.5, RIGHT * 7.5, stroke_width=0.4, color=GRAY, stroke_opacity=0.06))
        self.add(grid)

        # ================= PART 1: TIÊU ĐỀ VIDEO & GIỚI THIỆU THÀNH VIÊN (00:00 - 01:00) =================
        main_title = create_text("VƯỢT QUA GIỚI HẠN GIẢI MÃ", font_size=28, color=BLUE)
        sub_title = create_text("Thuật toán Meta-Generation cho các Mô hình Ngôn ngữ Lớn", font_size=14, color=GRAY)
        sub_title.next_to(main_title, DOWN, buff=0.3)

        english_title = create_text("Beyond Decoding: Meta-Generation Algorithms for LLMs", font_size=11, color=GRAY_C, slant=ITALIC)
        english_title.next_to(sub_title, DOWN, buff=0.25)

        info_text = create_text("NeurIPS 2024 Tutorial | Phong cách Hoạt họa 3Blue1Brown", font_size=10, color=DARK_GRAY)
        info_text.to_edge(DOWN, buff=0.6)

        # Hiển thị tiêu đề
        self.play(
            Write(main_title),
            FadeIn(sub_title, shift=UP * 0.3),
            FadeIn(english_title, shift=UP * 0.25),
            FadeIn(info_text, shift=UP * 0.2),
            run_time=2.0
        )
        self.wait(15.0) # Đợi lời thoại giới thiệu chung đầu video

        # Hiện danh sách diễn giả thuyết trình
        presenters_title = create_text("Nhóm nghiên cứu & Diễn giả:", font_size=14, color=BLUE_A)
        presenters_title.shift(UP * 0.8)
        
        p1 = create_text("- Matthew Finlayson (University of Southern California)", font_size=11, color=WHITE)
        p2 = create_text("- Sean Welleck (EleutherAI / Anthropic)", font_size=11, color=WHITE)
        p3 = create_text("- Hailey Schoelkopf (EleutherAI)", font_size=11, color=WHITE)
        
        presenters = VGroup(p1, p2, p3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        presenters.next_to(presenters_title, DOWN, buff=0.3)

        self.play(
            FadeOut(main_title),
            FadeOut(sub_title),
            FadeOut(english_title),
            Write(presenters_title),
            FadeIn(presenters, shift=UP * 0.2),
            run_time=1.5
        )
        self.wait(20.0) # Đợi giới thiệu nhóm tác giả và các tổ chức đứng sau

        # Mờ dần tất cả chuẩn bị sang Part 2
        self.play(
            FadeOut(presenters_title),
            FadeOut(presenters),
            FadeOut(info_text),
            run_time=1.0
        )
        self.wait(0.5)


        # ================= PART 2: MÔ PHỎNG SINH CHỮ TỰ HỒI QUY (01:00 - 02:00) =================
        part2_title = create_text("Mô phỏng sinh chữ tự hồi quy (Autoregressive)", font_size=16, color=PURPLE)
        part2_title.to_edge(UP, buff=0.5)
        self.play(Write(part2_title))

        # Khởi tạo mạng Neural tròn
        input_nodes = VGroup(*[Circle(radius=0.18, color=PURPLE, fill_color="#331133", fill_opacity=0.8) for _ in range(3)])
        input_nodes.arrange(DOWN, buff=0.6).shift(LEFT * 4.8 + DOWN * 0.8)

        hidden_nodes = VGroup(*[Circle(radius=0.18, color=GRAY, fill_color="#222222", fill_opacity=0.8) for _ in range(4)])
        hidden_nodes.arrange(DOWN, buff=0.5).shift(LEFT * 2.8 + DOWN * 0.8)

        output_nodes = VGroup(*[Circle(radius=0.18, color=BLUE, fill_color="#112233", fill_opacity=0.8) for _ in range(3)])
        output_nodes.arrange(DOWN, buff=0.6).shift(LEFT * 0.8 + DOWN * 0.8)

        input_label = create_text("Input (Tiền tố)", font_size=11, color=PURPLE).next_to(input_nodes, UP, buff=0.2)
        hidden_label = create_text("Lớp ẩn (Attention/FFN)", font_size=11, color=GRAY).next_to(hidden_nodes, UP, buff=0.2)
        output_label = create_text("Output (Logits)", font_size=11, color=BLUE).next_to(output_nodes, UP, buff=0.2)

        connections_in_to_hidden = VGroup()
        for i_node in input_nodes:
            for h_node in hidden_nodes:
                line = Line(i_node.get_right(), h_node.get_left(), stroke_width=1.5, color=GRAY, stroke_opacity=0.3)
                connections_in_to_hidden.add(line)

        connections_hidden_to_out = VGroup()
        for h_node in hidden_nodes:
            for o_node in output_nodes:
                line = Line(h_node.get_right(), o_node.get_left(), stroke_width=1.5, color=GRAY, stroke_opacity=0.3)
                connections_hidden_to_out.add(line)

        self.play(
            Create(input_nodes), Create(hidden_nodes), Create(output_nodes),
            Create(connections_in_to_hidden), Create(connections_hidden_to_out),
            Write(input_label), Write(hidden_label), Write(output_label),
            run_time=1.2
        )

        # Hộp văn bản kết quả bên phải
        text_box = Rectangle(width=4.5, height=1.6, color=GRAY, fill_color="#1a1a1a", fill_opacity=0.8)
        text_box.shift(RIGHT * 3.8 + DOWN * 1.2)
        text_box_label = create_text("Văn bản được tạo ra:", font_size=11, color=GRAY).next_to(text_box, UP, aligned_edge=LEFT, buff=0.1)
        
        # Hộp phân phối Logits bên phải (ở trên hộp văn bản)
        logits_box = Rectangle(width=4.5, height=1.8, color=YELLOW, fill_color="#1a1a1a", fill_opacity=0.8)
        logits_box.shift(RIGHT * 3.8 + UP * 1.0)
        logits_box_label = create_text("Phân phối xác suất (Logits Top-3):", font_size=11, color=YELLOW).next_to(logits_box, UP, aligned_edge=LEFT, buff=0.1)

        self.play(
            Create(text_box), Write(text_box_label),
            Create(logits_box), Write(logits_box_label),
            run_time=1.2
        )

        # Chạy sinh chuỗi chữ tự hồi quy
        words = ["Taylor", "Swift", "is", "a", "singer", "songwriter"]
        
        # Định nghĩa phân phối logits giả định ở mỗi bước để tăng tính trực quan toán học
        logits_data = [
            [("Taylor", "0.42", GREEN), ("The", "0.15", GRAY_C), ("She", "0.08", GRAY_C)],
            [("Swift", "0.85", GREEN), ("Alison", "0.05", GRAY_C), ("is", "0.02", GRAY_C)],
            [("is", "0.72", GREEN), ("was", "0.18", GRAY_C), ("has", "0.04", GRAY_C)],
            [("a", "0.64", GREEN), ("the", "0.22", GRAY_C), ("popular", "0.05", GRAY_C)],
            [("singer", "0.38", GREEN), ("songwriter", "0.28", GRAY_C), ("musician", "0.14", GRAY_C)],
            [("songwriter", "0.55", GREEN), (",", "0.15", GRAY_C), ("and", "0.12", GRAY_C)]
        ]

        display_str = ""
        display_mobject = create_text("", font_size=15, color=GREEN_B).move_to(text_box.get_center())
        self.add(display_mobject)

        algo_step_label = create_text("Mỗi bước giải mã tiêu tốn 1 lượt truyền xuôi (1 Forward Pass)", font_size=10, color=YELLOW)
        algo_step_label.next_to(text_box, DOWN, buff=0.3)
        self.play(FadeIn(algo_step_label))

        logits_group = VGroup()

        for step, word in enumerate(words):
            # Tạo các hạt xung điện truyền qua mạng neural
            pulses_1 = VGroup(*[Dot(point=line.get_start(), color=YELLOW, radius=0.05) for line in connections_in_to_hidden])
            pulses_2 = VGroup(*[Dot(point=line.get_start(), color=YELLOW, radius=0.05) for line in connections_hidden_to_out])

            # Cập nhật hiển thị phân phối Logits ở góc phải trên
            new_logits_group = VGroup()
            for idx, (tok, prob, col) in enumerate(logits_data[step]):
                tok_lbl = create_text(f"\"{tok}\"", font_size=10, color=col)
                prob_lbl = create_text(f"{prob}", font_size=10, color=col)
                row = VGroup(tok_lbl, prob_lbl).arrange(RIGHT, buff=1.0)
                new_logits_group.add(row)
            new_logits_group.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(logits_box.get_center())

            self.play(
                FadeIn(pulses_1, run_time=0.05),
                *[MoveAlongPath(p, l) for p, l in zip(pulses_1, connections_in_to_hidden)],
                run_time=0.4
            )
            self.remove(pulses_1)

            self.play(
                FadeIn(pulses_2, run_time=0.05),
                *[MoveAlongPath(p, l) for p, l in zip(pulses_2, connections_hidden_to_out)],
                run_time=0.4
            )
            self.remove(pulses_2)

            display_str += " " + word
            new_text = create_text(display_str.strip(), font_size=15, color=GREEN_B).move_to(text_box.get_center())
            
            self.play(
                Transform(display_mobject, new_text),
                Transform(logits_group, new_logits_group),
                Flash(output_nodes[1], color=YELLOW, line_length=0.12, num_lines=6, flash_radius=0.18),
                run_time=0.5
            )
            self.wait(1.5) # Dừng lại giữa các token để tạo sự nhịp nhàng

        self.wait(15.0) # Đợi lời thoại giải thích về chi phí tính toán tự hồi quy

        # Thu dọn Part 2
        self.play(
            FadeOut(part2_title), FadeOut(input_nodes), FadeOut(hidden_nodes), FadeOut(output_nodes),
            FadeOut(connections_in_to_hidden), FadeOut(connections_hidden_to_out),
            FadeOut(input_label), FadeOut(hidden_label), FadeOut(output_label),
            FadeOut(text_box), FadeOut(text_box_label), FadeOut(display_mobject),
            FadeOut(logits_box), FadeOut(logits_box_label), FadeOut(logits_group),
            FadeOut(algo_step_label),
            run_time=1.0
        )
        self.wait(0.5)


        # ================= PART 3: SO SÁNH TRUYỀN THỐNG VS TEST-TIME COMPUTE (02:00 - 03:00) =================
        part3_title = create_text("Phân bổ tài nguyên suy luận (Inference Resource Allocation)", font_size=16, color=BLUE)
        part3_title.to_edge(UP, buff=0.5)
        self.play(Write(part3_title))

        # Đường chia giữa màn hình
        divider = DashedLine(UP * 2, DOWN * 2.8, color=GRAY, stroke_width=1.5)
        self.play(Create(divider))

        # Phía bên trái: Suy luận thông thường (Standard Decoding)
        std_title = create_text("Suy luận thông thường\n(Standard Decoding - 1x)", font_size=12, color=RED).shift(LEFT * 3.5 + UP * 1.5)
        
        prompt_box_l = RoundedRectangle(width=1.3, height=0.7, color=GRAY, fill_color="#222", fill_opacity=0.8).shift(LEFT * 5.2 + UP * 0.1)
        prompt_text_l = create_text("Prompt", font_size=11).move_to(prompt_box_l.get_center())
        
        llm_box_l = RoundedRectangle(width=1.6, height=0.7, color=RED, fill_color="#3c1111", fill_opacity=0.8).shift(LEFT * 3.4 + UP * 0.1)
        llm_text_l = create_text("LLM\n(1 Pass)", font_size=10).move_to(llm_box_l.get_center())
        
        result_box_l = RoundedRectangle(width=1.3, height=0.7, color=GREEN, fill_color="#113311", fill_opacity=0.8).shift(LEFT * 1.6 + UP * 0.1)
        result_text_l = create_text("Kết quả", font_size=11).move_to(result_box_l.get_center())
        
        arrow_l1 = Arrow(prompt_box_l.get_right(), llm_box_l.get_left(), buff=0.1, stroke_width=2.5, color=GRAY_B)
        arrow_l2 = Arrow(llm_box_l.get_right(), result_box_l.get_left(), buff=0.1, stroke_width=2.5, color=GRAY_B)

        std_explain = create_text("Mô hình chỉ chạy một lượt truyền xuôi\nduy nhất để đưa ra đáp án ngay lập tức.", font_size=11, color=GRAY_A).shift(LEFT * 3.4 + DOWN * 1.1)

        self.play(
            Write(std_title),
            Create(prompt_box_l), Write(prompt_text_l),
            Create(llm_box_l), Write(llm_text_l),
            Create(result_box_l), Write(result_text_l),
            GrowArrow(arrow_l1), GrowArrow(arrow_l2),
            Write(std_explain),
            run_time=1.5
        )

        # Phía bên phải: Test-Time Compute (Reasoning / Search / Verifier)
        ttc_title = create_text("Tính toán thời điểm suy luận\n(Test-Time Compute - Nx)", font_size=12, color=BLUE).shift(RIGHT * 3.5 + UP * 1.5)
        
        prompt_box_r = RoundedRectangle(width=1.0, height=0.7, color=GRAY, fill_color="#222", fill_opacity=0.8).shift(RIGHT * 1.1 + UP * 0.1)
        prompt_text_r = create_text("Prompt", font_size=10).move_to(prompt_box_r.get_center())
        
        gen_box_r = RoundedRectangle(width=1.4, height=0.7, color=BLUE, fill_color="#0a1220", fill_opacity=0.8).shift(RIGHT * 2.8 + UP * 0.1)
        gen_text_r = create_text("LLM\nGenerator", font_size=9).move_to(gen_box_r.get_center())
        
        think_box_r = RoundedRectangle(width=1.5, height=0.7, color=ORANGE, fill_color="#331a00", fill_opacity=0.8).shift(RIGHT * 4.6 + UP * 0.1)
        think_text_r = create_text("Suy nghĩ\n/ Lọc", font_size=9).move_to(think_box_r.get_center())
        
        result_box_r = RoundedRectangle(width=1.0, height=0.7, color=GREEN, fill_color="#113311", fill_opacity=0.8).shift(RIGHT * 6.3 + UP * 0.1)
        result_text_r = create_text("Kết quả", font_size=10).move_to(result_box_r.get_center())
        
        arrow_r1 = Arrow(prompt_box_r.get_right(), gen_box_r.get_left(), buff=0.08, stroke_width=2.5, color=GRAY_B)
        arrow_r2 = Arrow(gen_box_r.get_right(), think_box_r.get_left(), buff=0.08, stroke_width=2.5, color=GRAY_B)
        arrow_r3 = Arrow(think_box_r.get_right(), result_box_r.get_left(), buff=0.08, stroke_width=2.5, color=GRAY_B)

        # Đường phản hồi vòng lặp suy nghĩ
        loop_arrow = CurvedArrow(think_box_r.get_top() + LEFT * 0.15, gen_box_r.get_top() + RIGHT * 0.15, angle=TAU/3.2, stroke_width=2, color=YELLOW)
        loop_label = create_text("Sửa sai & Tạo chuỗi suy nghĩ mới (Lặp)", font_size=8, color=YELLOW).next_to(loop_arrow, UP, buff=0.1)

        ttc_explain = create_text("Mô hình sinh thêm các token lập luận,\ngọi công cụ hoặc chạy thử để tự kiểm tra.", font_size=11, color=GRAY_A).shift(RIGHT * 3.7 + DOWN * 1.1)

        self.play(
            Write(ttc_title),
            Create(prompt_box_r), Write(prompt_text_r),
            Create(gen_box_r), Write(gen_text_r),
            Create(think_box_r), Write(think_text_r),
            Create(result_box_r), Write(result_text_r),
            GrowArrow(arrow_r1), GrowArrow(arrow_r2), GrowArrow(arrow_r3),
            Write(ttc_explain),
            run_time=1.5
        )
        
        # Chạy hoạt ảnh vòng lặp suy nghĩ 2 lần để mô phỏng suy nghĩ sâu
        for _ in range(2):
            self.play(Create(loop_arrow), Write(loop_label), run_time=1.0)
            self.play(Flash(gen_box_r, color=YELLOW, flash_radius=0.3), run_time=0.5)
            self.play(FadeOut(loop_arrow), FadeOut(loop_label), run_time=0.4)
            self.wait(1.0)

        self.wait(18.0) # Đợi lời thoại giải thích về lợi ích và xu hướng phân bổ tài nguyên suy luận

        # Thu dọn Part 3
        self.play(
            FadeOut(part3_title), FadeOut(divider),
            FadeOut(std_title),
            FadeOut(prompt_box_l), FadeOut(prompt_text_l),
            FadeOut(llm_box_l), FadeOut(llm_text_l),
            FadeOut(result_box_l), FadeOut(result_text_l),
            FadeOut(arrow_l1), FadeOut(arrow_l2),
            FadeOut(std_explain),
            FadeOut(ttc_title),
            FadeOut(prompt_box_r), FadeOut(prompt_text_r),
            FadeOut(gen_box_r), FadeOut(gen_text_r),
            FadeOut(think_box_r), FadeOut(think_text_r),
            FadeOut(result_box_r), FadeOut(result_text_r),
            FadeOut(arrow_r1), FadeOut(arrow_r2), FadeOut(arrow_r3),
            FadeOut(ttc_explain),
            run_time=1.0
        )
        self.wait(0.5)


        # ================= PART 4: ỨNG DỤNG ĐA DẠNG DƯỚI DẠNG TẠO CHUỖI (03:00 - 04:00) =================
        part4_title = create_text("Tất cả tác vụ đều được biểu diễn dưới dạng sinh chuỗi tuần tự", font_size=15, color=YELLOW)
        part4_title.to_edge(UP, buff=0.5)
        self.play(Write(part4_title))

        # Tạo 3 thẻ tác vụ với khoảng cách cân đối
        card_w, card_h = 3.5, 2.5
        card_1 = RoundedRectangle(width=card_w, height=card_h, color=PURPLE, fill_color="#181124", fill_opacity=0.9).shift(LEFT * 4.0 + DOWN * 0.5)
        card_2 = RoundedRectangle(width=card_w, height=card_h, color=BLUE, fill_color="#0e1624", fill_opacity=0.9).shift(DOWN * 0.5)
        card_3 = RoundedRectangle(width=card_w, height=card_h, color=GREEN, fill_color="#0b1712", fill_opacity=0.9).shift(RIGHT * 4.0 + DOWN * 0.5)

        # Tiêu đề trên mỗi card
        title_1 = create_text("Giải toán (Math Reasoning)", font_size=11, color=PURPLE_A).next_to(card_1.get_top(), DOWN, buff=0.2)
        title_2 = create_text("Lập trình (Code Generation)", font_size=11, color=BLUE_A).next_to(card_2.get_top(), DOWN, buff=0.2)
        title_3 = create_text("Dịch thuật (Translation)", font_size=11, color=GREEN_A).next_to(card_3.get_top(), DOWN, buff=0.2)

        self.play(
            Create(card_1), Write(title_1),
            Create(card_2), Write(title_2),
            Create(card_3), Write(title_3),
            run_time=1.2
        )
        self.wait(0.5)

        # Chạy hoạt ảnh sinh chữ tuần tự bên trong các thẻ tác vụ
        math_content = create_text("Input: 2x + 5 = 15\n\nBước 1: 2x = 10\nBước 2: x = 5", font_size=9, color=WHITE).move_to(card_1.get_center() + DOWN * 0.2)
        code_content = create_text("def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[0] ...", font_size=9, color=WHITE).move_to(card_2.get_center() + DOWN * 0.2)
        translation_content = create_text("English: Hello World!\n\nDịch thuật:\nXin chào Thế giới!", font_size=9, color=WHITE).move_to(card_3.get_center() + DOWN * 0.2)

        # Viết chữ chậm rãi mô phỏng các token sinh ra khớp với voiceover giải thích tính linh hoạt
        self.play(
            Write(math_content),
            Write(code_content),
            Write(translation_content),
            run_time=4.0
        )
        self.wait(18.0) # Đợi lời thoại kết thúc về khả năng ứng dụng rộng lớn

        # Kết thúc Scene 1.1 bằng việc mờ dần mọi thứ
        self.play(
            FadeOut(part4_title),
            FadeOut(card_1), FadeOut(title_1), FadeOut(math_content),
            FadeOut(card_2), FadeOut(title_2), FadeOut(code_content),
            FadeOut(card_3), FadeOut(title_3), FadeOut(translation_content),
            run_time=1.0
        )
        self.wait(1.0)
