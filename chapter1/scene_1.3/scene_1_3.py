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


class Scene1_3(Scene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B (Loại bỏ hoàn toàn lưới nền để không còn dấu cộng chia màn hình)
        self.camera.background_color = "#111111"


        # Tiêu đề chính của Phân cảnh 1.3
        main_title = create_text("Các Phương Thức Mở Rộng Tính Toán Lúc Suy Luận", font_size=20, color=BLUE_A)
        main_title.to_edge(UP, buff=0.4)
        self.play(Write(main_title))
        self.wait(1.5)


        # =====================================================================
        # GIAI ĐOẠN 1: CHUỖI SUY NGHĨ (CHAIN OF THOUGHT - COT)
        # =====================================================================
        sub_title1 = create_text("1. Generate extra tokens [Wei et al., 2022]", font_size=12, color=GREEN_A)
        sub_title1.next_to(main_title, DOWN, buff=0.2)
        self.play(FadeIn(sub_title1, shift=DOWN*0.1))
        self.wait(2.0)

        # Cột bên trái: Standard Prompting (Direct Output) - Định vị dịch xuống y = -0.8
        left_group = VGroup()
        left_bg = RoundedRectangle(width=5.8, height=4.2, color=RED, fill_color="#1a1112", fill_opacity=0.8, corner_radius=0.1)
        left_bg.shift(LEFT * 3.3 + DOWN * 0.8)
        
        left_title = create_text("Standard Prompting (Direct Output)", font_size=11, color=RED_A)
        left_title.next_to(left_bg.get_top(), DOWN, buff=0.25)
        
        # Căn giữa văn bản câu hỏi trong hộp bên trái
        left_q = create_text("Prompt / Input x", font_size=11, color=WHITE)
        left_q.next_to(left_title, DOWN, buff=0.35)
        
        # Mô phỏng quá trình sinh trực tiếp (Sử dụng Line + add_tip cho đồng bộ tuyệt đối)
        left_arrow = Line(
            left_q.get_bottom(), left_q.get_bottom() + DOWN * 0.7, 
            color=GRAY, stroke_width=2.5, 
            buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)
        
        # Hộp kết quả đầu ra (Căn giữa)
        left_out_box = RoundedRectangle(width=5.2, height=1.0, color=RED_C, fill_color="#2c1a1b", fill_opacity=0.9, corner_radius=0.08)
        left_out_box.next_to(left_arrow, DOWN, buff=0.15)
        left_out_text = create_text("Direct Output y\n(No intermediate thoughts)", font_size=9, color=RED_A)
        left_out_text.move_to(left_out_box.get_center())
        
        left_group.add(left_bg, left_title, left_q)

        # Cột bên phải: Chain of Thought (CoT) - Định vị dịch xuống y = -0.8
        right_group = VGroup()
        right_bg = RoundedRectangle(width=5.8, height=4.2, color=GREEN, fill_color="#111c13", fill_opacity=0.8, corner_radius=0.1)
        right_bg.shift(RIGHT * 3.3 + DOWN * 0.8)
        
        right_title = create_text("Chain of Thought (CoT)", font_size=11, color=GREEN_A)
        right_title.next_to(right_bg.get_top(), DOWN, buff=0.25)
        
        # Căn giữa văn bản câu hỏi trong hộp bên phải
        right_q = create_text("Prompt / Input x", font_size=11, color=WHITE)
        right_q.next_to(right_title, DOWN, buff=0.25)
        
        right_group.add(right_bg, right_title, right_q)

        # Hiển thị nền hai phương án
        self.play(
            FadeIn(left_bg, shift=RIGHT * 0.2), Write(left_title), FadeIn(left_q),
            FadeIn(right_bg, shift=LEFT * 0.2), Write(right_title), FadeIn(right_q),
            run_time=1.5
        )
        self.wait(2.0)

        # Hoạt họa kết quả Standard (Sử dụng Create thay thế GrowArrow để tránh crash)
        self.play(Create(left_arrow), run_time=0.6)
        self.play(Create(left_out_box), Write(left_out_text), run_time=1.0)
        self.play(Flash(left_out_box, color=RED, flash_radius=0.2), run_time=0.8)
        self.wait(4.0)

        # Hoạt họa sinh CoT step-by-step (Căn giữa hoàn hảo theo cột bên phải)
        step_box_w, step_box_h = 5.2, 0.45
        step1_box = RoundedRectangle(width=step_box_w, height=step_box_h, color=GREEN_C, fill_color="#182c1b", fill_opacity=0.9, corner_radius=0.06)
        step1_box.next_to(right_q, DOWN, buff=0.2)
        step1_text = create_text("Intermediate Thought Token 1", font_size=9, color=GREEN_A)
        step1_text.move_to(step1_box.get_center())
        
        step2_box = RoundedRectangle(width=step_box_w, height=step_box_h, color=GREEN_C, fill_color="#182c1b", fill_opacity=0.9, corner_radius=0.06)
        step2_box.next_to(step1_box, DOWN, buff=0.15)
        step2_text = create_text("Intermediate Thought Token 2", font_size=9, color=GREEN_A)
        step2_text.move_to(step2_box.get_center())

        step3_box = RoundedRectangle(width=step_box_w, height=step_box_h, color=GREEN_C, fill_color="#182c1b", fill_opacity=0.9, corner_radius=0.06)
        step3_box.next_to(step2_box, DOWN, buff=0.15)
        step3_text = create_text("Intermediate Thought Token 3", font_size=9, color=GREEN_A)
        step3_text.move_to(step3_box.get_center())

        final_box = RoundedRectangle(width=step_box_w, height=0.55, color=YELLOW, fill_color="#302d18", fill_opacity=0.9, corner_radius=0.06)
        final_box.next_to(step3_box, DOWN, buff=0.2)
        final_text = create_text("Final Output y", font_size=9, color=YELLOW)
        final_text.move_to(final_box.get_center())

        # Animate step-by-step
        self.play(Create(step1_box), Write(step1_text), run_time=1.0)
        self.wait(2.0)
        self.play(Create(step2_box), Write(step2_text), run_time=1.0)
        self.wait(2.0)
        self.play(Create(step3_box), Write(step3_text), run_time=1.0)
        self.wait(2.0)
        self.play(Create(final_box), Write(final_text), run_time=1.2)
        self.play(Flash(final_box, color=YELLOW, flash_radius=0.25), run_time=0.8)
        self.wait(15.0)

        # Dọn dẹp giai đoạn 1
        stage1_mobjects = VGroup(
            sub_title1, left_group, left_arrow, left_out_box, left_out_text,
            right_group, step1_box, step1_text, step2_box, step2_text, step3_box, step3_text, final_box, final_text
        )
        self.play(FadeOut(stage1_mobjects), run_time=1.0)
        self.wait(0.5)


        # =====================================================================
        # GIAI ĐOẠN 2: LẤY MẪU SONG SONG & LỌC (PARALLEL SAMPLING - ALPHACODE)
        # =====================================================================
        sub_title2 = create_text("2. Call generator multiple times (e.g., AlphaCode [Li et al., 2022])", font_size=12, color=YELLOW)
        sub_title2.next_to(main_title, DOWN, buff=0.2)
        self.play(FadeIn(sub_title2, shift=DOWN*0.1))
        self.wait(1.5)

        # Hiển thị đề bài toán lập trình ở trên (y = 2.3)
        problem_bg = RoundedRectangle(width=8.0, height=0.8, color=BLUE_A, fill_color="#121824", fill_opacity=0.8, corner_radius=0.08)
        problem_bg.shift(UP * 2.3)
        problem_text = create_text("Input / Query", font_size=12, color=WHITE)
        problem_text.move_to(problem_bg.get_center())

        self.play(Create(problem_bg), Write(problem_text), run_time=1.0)
        self.wait(1.5)
        # Cấu hình các điểm đích của các hộp ở y = -0.1 (dịch chuyển xuống để kéo dài mũi tên và tạo khoảng thoáng)
        endpoints = [
            LEFT * 4.5 + DOWN * 0.1,
            LEFT * 2.2 + DOWN * 0.1,
            LEFT * 0.0 + DOWN * 0.1,
            RIGHT * 2.2 + DOWN * 0.1,
            RIGHT * 4.5 + DOWN * 0.1
        ]

        # Vẽ chùm mũi tên kết nối từ một gốc chung duy nhất ở problem_bg.get_bottom() (ở y = 1.9)
        # Điểm đầu chung gốc 100% (không dùng buff ở start), chỉ dịch chuyển ở end để tạo khoảng hở với hộp code
        arrows = VGroup()
        for idx, pt in enumerate(endpoints):
            start = problem_bg.get_bottom()
            end = pt + UP * 0.5
            
            # Đặt độ dày và độ mờ cho đường thẳng đứng ở giữa để đồng bộ thị giác với các đường xiên (tránh hiện tượng nét đứng sắc cạnh trông dày hơn nét xiên do không có anti-aliasing)
            sw = 0.6 if idx == 2 else 1.5
            op = 0.6 if idx == 2 else 1.0
            line = Line(
                start, end, 
                color=GRAY_A, stroke_width=sw,
                stroke_opacity=op
            )
            line.add_tip(tip_length=0.12, tip_width=0.12)
            if hasattr(line, "tip") and line.tip is not None:
                line.tip.set_opacity(op)
            arrows.add(line)

        self.play(Create(arrows), run_time=1.2)
        self.wait(1.0)

        # Tạo các hộp ứng viên mã nguồn (Code candidates) ở y = 0.2
        code_boxes = VGroup()
        code_labels = VGroup()
        for idx, pt in enumerate(endpoints):
            box = RoundedRectangle(width=1.8, height=1.0, color=GRAY, fill_color="#1e1e1e", fill_opacity=0.9, corner_radius=0.06)
            box.move_to(pt)
            label = create_text(f"Candidate {idx+1}\n(Random Sample)", font_size=10, color=WHITE)
            label.move_to(box.get_center())
            code_boxes.add(box)
            code_labels.add(label)

        self.play(
            FadeIn(code_boxes, shift=DOWN*0.2),
            Write(code_labels),
            run_time=1.5
        )
        self.wait(3.0)

        # Lưới lọc (Unit Test) đặt ở y = -1.0 để các hộp di chuyển qua hoàn toàn
        filter_line = Line(LEFT * 6.0 + DOWN * 1.0, RIGHT * 6.0 + DOWN * 1.0, color=GREEN, stroke_width=3.5)
        filter_label = create_text("VERIFIER / EVALUATOR", font_size=9, color=GREEN_A).next_to(filter_line, UP, aligned_edge=RIGHT, buff=0.1)
        
        self.play(Create(filter_line), Write(filter_label), run_time=1.0)
        self.wait(2.0)

        # Animate các mẫu code đi xuống hẳn dưới lưới lọc (xuống y = -2.4)
        anims_down = []
        for box, label in zip(code_boxes, code_labels):
            anims_down.append(box.animate.move_to(box.get_center() + DOWN * 2.6))
            anims_down.append(label.animate.move_to(label.get_center() + DOWN * 2.6))
        self.play(*anims_down, run_time=1.5)
        self.wait(1.5)

        # Đánh giá các mẫu code (lúc này đã nằm dưới lưới lọc ở y = -2.4)
        eval_anims = []
        for idx, (box, label) in enumerate(zip(code_boxes, code_labels)):
            if idx == 2: # Mẫu code số 3 đúng
                eval_anims.append(box.animate.set_color(GREEN).set_fill("#112413"))
                eval_anims.append(label.animate.set_color(GREEN_A))
            else:
                eval_anims.append(box.animate.set_color(RED).set_fill("#241112"))
                eval_anims.append(label.animate.set_color(RED_A))
                
        self.play(*eval_anims, run_time=1.0)
        self.play(
            Flash(code_boxes[2].get_center(), color=GREEN, flash_radius=0.35, num_lines=10),
            run_time=0.8
        )
        self.wait(2.0)

        # Biến mất các mẫu sai và toàn bộ 5 mũi tên (để không bị thừa mũi tên chỉ vào khoảng trống)
        fadeouts = [FadeOut(arrows)]
        for idx in [0, 1, 3, 4]:
            fadeouts.append(FadeOut(code_boxes[idx]))
            fadeouts.append(FadeOut(code_labels[idx]))
        self.play(*fadeouts, run_time=0.8)
        self.wait(1.5)

        # Zoom mẫu đúng lên (y = -2.0)
        self.play(
            code_boxes[2].animate.move_to(DOWN * 2.0).scale(1.2),
            code_labels[2].animate.move_to(DOWN * 2.0).scale(1.2),
            run_time=1.2
        )
        final_arrow = Line(
            code_boxes[2].get_bottom(), code_boxes[2].get_bottom() + DOWN * 0.6, 
            color=YELLOW, stroke_width=2.5
        ).add_tip(tip_length=0.12, tip_width=0.12)
        final_out_lbl = create_text("Best candidate selected as Output", font_size=11, color=YELLOW).next_to(final_arrow, DOWN, buff=0.1)
        self.play(Create(final_arrow), Write(final_out_lbl), run_time=0.8)
        self.wait(18.0)

        # Dọn dẹp giai đoạn 2
        stage2_mobjects = VGroup(
            sub_title2, problem_bg, problem_text, arrows, filter_line, filter_label,
            code_boxes[2], code_labels[2], final_arrow, final_out_lbl
        )
        self.play(FadeOut(stage2_mobjects), run_time=1.0)
        self.wait(0.5)


        # =====================================================================
        # GIAI ĐOẠN 3: HỆ THỐNG AI PHỨC HỢP & CÔNG CỤ NGOÀI (COMPOUND AI & TOOLS)
        # =====================================================================
        sub_title3 = create_text("3. Incorporate other models/tools [Zaharia et al., 2024]", font_size=12, color=BLUE_A)
        sub_title3.next_to(main_title, DOWN, buff=0.2)
        self.play(FadeIn(sub_title3, shift=DOWN*0.1))
        self.wait(1.5)

        # 1. Hộp LLM ở giữa (y = 0.4)
        llm_box = RoundedRectangle(width=2.8, height=1.2, color=BLUE, fill_color="#121824", fill_opacity=0.9, corner_radius=0.08)
        llm_box.shift(UP * 0.4)
        llm_text = create_text("Language Model\n(Generator)", font_size=11, color=BLUE_A).move_to(llm_box.get_center())

        # 2. Hộp Tool: Calculator (y = -1.8)
        calc_box = RoundedRectangle(width=2.5, height=1.1, color=GREEN, fill_color="#0e1a10", fill_opacity=0.9, corner_radius=0.08)
        calc_box.shift(LEFT * 3.3 + DOWN * 1.8)
        calc_text = create_text("Tool: Search Engine", font_size=11, color=GREEN_A).move_to(calc_box.get_center())

        # 3. Hộp Tool: Python Interpreter (y = -1.8)
        python_box = RoundedRectangle(width=2.5, height=1.1, color=ORANGE, fill_color="#24190e", fill_opacity=0.9, corner_radius=0.08)
        python_box.shift(RIGHT * 3.3 + DOWN * 1.8)
        python_text = create_text("Tool: Code Interpreter", font_size=11, color=ORANGE).move_to(python_box.get_center())

        # Mũi tên kết nối hai chiều (Sử dụng Line kết hợp add_tip cho đồng bộ hoàn hảo)
        arrow_calc_out = Line(
            llm_box.get_left() + DOWN * 0.1, calc_box.get_top() + RIGHT * 0.2, 
            color=GRAY, stroke_width=2
        ).add_tip(tip_length=0.12, tip_width=0.12)
        arrow_calc_in = Line(
            calc_box.get_top() + LEFT * 0.1, llm_box.get_left() + UP * 0.1, 
            color=GRAY, stroke_width=2
        ).add_tip(tip_length=0.12, tip_width=0.12)
        
        arrow_py_out = Line(
            llm_box.get_right() + DOWN * 0.1, python_box.get_top() + LEFT * 0.2, 
            color=GRAY, stroke_width=2
        ).add_tip(tip_length=0.12, tip_width=0.12)
        arrow_py_in = Line(
            python_box.get_top() + RIGHT * 0.1, llm_box.get_right() + UP * 0.1, 
            color=GRAY, stroke_width=2
        ).add_tip(tip_length=0.12, tip_width=0.12)

        self.play(
            Create(llm_box), Write(llm_text),
            Create(calc_box), Write(calc_text),
            Create(python_box), Write(python_text),
            run_time=1.5
        )
        self.play(
            Create(arrow_calc_out), Create(arrow_calc_in),
            Create(arrow_py_out), Create(arrow_py_in),
            run_time=1.0
        )
        self.wait(2.0)

        # Hiển thị câu hỏi đầu vào ở y = 2.0 (Dưới tiêu đề phụ để tránh đè chữ)
        user_input_bg = RoundedRectangle(width=5.0, height=0.6, color=GRAY, fill_color="#222", fill_opacity=0.8, corner_radius=0.06)
        user_input_bg.shift(UP * 2.0)
        user_input_txt = create_text("Query / Input", font_size=11, color=WHITE)
        user_input_txt.move_to(user_input_bg.get_center())

        self.play(Create(user_input_bg), Write(user_input_txt), run_time=0.8)
        self.wait(2.0)

        # LLM nhận dạng và sinh lệnh gọi máy tính (y = -0.5)
        call_msg_bg = RoundedRectangle(width=2.5, height=0.5, color=GREEN, fill_color="#0e1a10", fill_opacity=0.9, corner_radius=0.06)
        call_msg_bg.shift(DOWN * 0.5)
        call_msg_txt = create_text("[Call Tool with Query]", font_size=10, color=GREEN_A)
        call_msg_txt.move_to(call_msg_bg.get_center())

        self.play(Create(call_msg_bg), Write(call_msg_txt), run_time=0.8)
        self.wait(1.5)

        # Hạt dữ liệu chạy từ LLM sang Calculator
        data_dot = Dot(point=llm_box.get_left(), color=GREEN_A, radius=0.08)
        self.play(FadeIn(data_dot))
        self.play(data_dot.animate.move_to(calc_box.get_top()), run_time=1.0)
        self.play(Flash(calc_box.get_top(), color=GREEN, flash_radius=0.2), run_time=0.6)
        self.play(FadeOut(data_dot))

        # Calculator xuất kết quả ở y = -2.8
        calc_out_bg = RoundedRectangle(width=2.2, height=0.5, color=GREEN_C, fill_color="#182c1b", fill_opacity=0.9, corner_radius=0.06)
        calc_out_bg.shift(DOWN * 2.8 + LEFT * 3.3)
        calc_out_txt = create_text("Tool Output / Results", font_size=10, color=GREEN_A)
        calc_out_txt.move_to(calc_out_bg.get_center())
        
        self.play(Create(calc_out_bg), Write(calc_out_txt), run_time=0.8)
        self.wait(1.5)

        # Hạt dữ liệu mang kết quả chạy ngược lại LLM
        data_dot2 = Dot(point=calc_box.get_top(), color=GREEN_A, radius=0.08)
        self.play(FadeIn(data_dot2))
        self.play(data_dot2.animate.move_to(llm_box.get_left()), run_time=1.0)
        self.play(Flash(llm_box.get_left(), color=GREEN, flash_radius=0.2), run_time=0.6)
        self.play(FadeOut(data_dot2))

        # LLM nhận kết quả và đưa ra câu trả lời cuối: FADE OUT hộp yêu cầu và THAY THẾ bằng hộp kết quả ở y = 2.0
        final_answer_bg = RoundedRectangle(width=5.5, height=0.6, color=YELLOW, fill_color="#302d18", fill_opacity=0.9, corner_radius=0.06)
        final_answer_bg.shift(UP * 2.0)
        final_answer_txt = create_text("Final Answer (incorporating tool output)", font_size=11, color=YELLOW)
        final_answer_txt.move_to(final_answer_bg.get_center())

        self.play(
            FadeOut(user_input_bg), FadeOut(user_input_txt),
            FadeOut(call_msg_bg), FadeOut(call_msg_txt),
            run_time=0.8
        )
        self.play(
            Create(final_answer_bg), Write(final_answer_txt),
            run_time=1.2
        )
        self.play(Flash(final_answer_bg, color=YELLOW, flash_radius=0.3), run_time=0.8)
        self.wait(20.0)

        # Dọn dẹp giai đoạn 3
        stage3_mobjects = VGroup(
            sub_title3, llm_box, llm_text, calc_box, calc_text, python_box, python_text,
            arrow_calc_out, arrow_calc_in, arrow_py_out, arrow_py_in,
            calc_out_bg, calc_out_txt, final_answer_bg, final_answer_txt
        )
        self.play(FadeOut(stage3_mobjects), run_time=1.0)
        self.wait(0.5)


        # =====================================================================
        # GIAI ĐOẠN 4: TỔNG KẾT BA PHƯƠNG PHÁP (SUMMARY CARDS)
        # =====================================================================
        summary_title = create_text("Mở Rộng Lúc Suy Luận = Sinh thêm Token, Sinh song song & Sử dụng Công cụ", font_size=11, color=BLUE_A)
        summary_title.next_to(main_title, DOWN, buff=0.3)
        self.play(Write(summary_title))

        # Phóng to kích thước thẻ và tăng kích thước chữ hiển thị
        sum_card_w, sum_card_h = 4.1, 2.8
        
        card1 = RoundedRectangle(width=sum_card_w, height=sum_card_h, color=GREEN, fill_color="#111c13", fill_opacity=0.8, corner_radius=0.1)
        card1.shift(LEFT * 4.4 + DOWN * 0.8)
        card1_title = create_text("1. Sinh Lập Luận", font_size=13, color=GREEN_A).next_to(card1.get_top(), DOWN, buff=0.15)
        card1_desc = create_text("- Chuỗi suy nghĩ (CoT)\n- Phân bổ thêm token\n- Tăng tính biểu đạt\n- Tối ưu hóa suy luận", font_size=10, color=WHITE).next_to(card1_title, DOWN, buff=0.25, aligned_edge=LEFT)
        card1_desc.shift(LEFT * 0.2)
        c1_group = VGroup(card1, card1_title, card1_desc)

        card2 = RoundedRectangle(width=sum_card_w, height=sum_card_h, color=YELLOW, fill_color="#262312", fill_opacity=0.8, corner_radius=0.1)
        card2.shift(LEFT * 0.0 + DOWN * 0.8)
        card2_title = create_text("2. Tìm Kiếm & Biểu Quyết", font_size=13, color=YELLOW).next_to(card2.get_top(), DOWN, buff=0.15)
        card2_desc = create_text("- Sinh song song N mẫu\n- Đánh giá bằng Reward Model\n- Biểu quyết số đông\n- Rủi ro Bayes tối thiểu", font_size=10, color=WHITE).next_to(card2_title, DOWN, buff=0.25, aligned_edge=LEFT)
        card2_desc.shift(LEFT * 0.35)
        c2_group = VGroup(card2, card2_title, card2_desc)

        card3 = RoundedRectangle(width=sum_card_w, height=sum_card_h, color=BLUE, fill_color="#121824", fill_opacity=0.8, corner_radius=0.1)
        card3.shift(RIGHT * 4.4 + DOWN * 0.8)
        card3_title = create_text("3. Hệ AI Phức Hợp", font_size=13, color=BLUE_A).next_to(card3.get_top(), DOWN, buff=0.15)
        card3_desc = create_text("- Gọi công cụ ngoài\n- Tối ưu hóa tài nguyên\n- Gọi máy tính / viết code\n- Giảm thiểu lỗi số học", font_size=10, color=WHITE).next_to(card3_title, DOWN, buff=0.25, aligned_edge=LEFT)
        card3_desc.shift(LEFT * 0.25)
        c3_group = VGroup(card3, card3_title, card3_desc)

        self.play(
            FadeIn(c1_group, shift=UP*0.2),
            FadeIn(c2_group, shift=UP*0.2),
            FadeIn(c3_group, shift=UP*0.2),
            run_time=2.0
        )
        self.wait(15.0)

        # Dọn dẹp kết thúc toàn bộ video Scene 1.3
        self.play(
            FadeOut(main_title),
            FadeOut(summary_title),
            FadeOut(c1_group),
            FadeOut(c2_group),
            FadeOut(c3_group),
            run_time=1.5
        )
        self.wait(1.0)
