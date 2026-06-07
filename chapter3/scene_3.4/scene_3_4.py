import os
import tempfile
from manim import *

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

# Hàm vẽ ký hiệu Checkmark (dạng vector)
def get_checkmark(color=GREEN, stroke_width=2.5):
    checkmark = VMobject(color=color, stroke_width=stroke_width)
    checkmark.set_points_as_corners([
        LEFT * 0.12 + DOWN * 0.05,
        ORIGIN + DOWN * 0.15,
        RIGHT * 0.2 + UP * 0.15
    ])
    return checkmark

# Hàm vẽ ký hiệu Crossmark (dạng vector)
def get_crossmark(color=RED, stroke_width=2.5):
    cross = VGroup()
    line1 = Line(LEFT * 0.12 + UP * 0.12, RIGHT * 0.12 + DOWN * 0.12, color=color, stroke_width=stroke_width)
    line2 = Line(LEFT * 0.12 + DOWN * 0.12, RIGHT * 0.12 + UP * 0.12, color=color, stroke_width=stroke_width)
    cross.add(line1, line2)
    return cross


class Scene3_4(Scene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH
        # =====================================================================
        chapter_title = create_text("Chương 3: Bộ điều phối cấp cao", font_size=24, color=YELLOW)
        chapter_sub = create_text("Phần 3.4: Tinh chỉnh & Tự sửa lỗi (Refinement & Self-Correction)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(5.0)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Tinh chỉnh & Tự sửa lỗi (Refinement & Self-Correction)", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(3.0)

        # =====================================================================
        # PHẦN 1: PHẢN HỒI NGOẠI SINH (EXTRINSIC FEEDBACK LOOP)
        # =====================================================================
        part1_title = create_text("1. Phản hồi ngoại sinh (Extrinsic Feedback Loop)", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part1_title), run_time=0.8)
        self.wait(3.0)

        # Giải thích khái niệm Extrinsic Feedback
        intro_text = create_markup_text(
            "<b>Phản hồi ngoại sinh (Extrinsic Feedback):</b> Mô hình nhận phản hồi khách quan\n"
            "từ môi trường bên ngoài (như Trình biên dịch - Compiler hoặc máy chạy code)\n"
            "và sử dụng thông báo lỗi này để khoanh vùng lỗi rồi tự động sửa chữa.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)
        self.play(Write(intro_text), run_time=2.0)
        self.wait(20.0)

        # Sơ đồ LLM <-> Compiler
        llm_box = RoundedRectangle(width=2.5, height=1.3, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        llm_box.move_to(LEFT * 4.2 + DOWN * 0.5)
        llm_lbl = create_text("LLM Generator", font_size=12, color=BLUE_A).move_to(llm_box.get_center())

        compiler_box = RoundedRectangle(width=2.5, height=1.3, color=RED_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        compiler_box.move_to(RIGHT * 4.2 + DOWN * 0.5)
        compiler_lbl = create_text("Rust Compiler", font_size=12, color=WHITE).move_to(compiler_box.get_center())

        arrow_to_comp = Arrow(start=llm_box.get_right() + UP * 0.25, end=compiler_box.get_left() + UP * 0.25, color=BLUE_B, stroke_width=1.5, buff=0.05)
        
        # Mũi tên phản hồi lỗi quay ngược từ Compiler về LLM (ở phía dưới)
        arrow_back = CurvedArrow(
            compiler_box.get_left() + DOWN * 0.25, 
            llm_box.get_right() + DOWN * 0.25, 
            angle=0.4, 
            color=RED_B, 
            stroke_width=1.5
        )

        self.play(
            FadeIn(llm_box), Write(llm_lbl),
            FadeIn(compiler_box), Write(compiler_lbl),
            run_time=1.5
        )
        self.wait(6.0)

        # Sơ đồ biểu diễn Bộ nhớ và Con trỏ Ownership ở giữa (Y=0.7)
        res_box = RoundedRectangle(width=2.2, height=0.7, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        res_box.move_to(LEFT * 0.8 + UP * 0.7)
        res_lbl = create_text("Vùng nhớ String \"hello\"", font_size=8, color=WHITE).move_to(res_box.get_center())

        s_var = RoundedRectangle(width=0.8, height=0.4, color=GRAY_A, fill_color="#141517", fill_opacity=0.95, corner_radius=0.04)
        s_var.move_to(LEFT * 2.6 + UP * 1.2)
        s_lbl = create_text("Biến s", font_size=8, color=WHITE).move_to(s_var.get_center())

        s_ptr = Arrow(start=s_var.get_bottom(), end=res_box.get_left() + UP * 0.15, color=BLUE_A, stroke_width=2, max_tip_length_to_length_ratio=0.15, buff=0.05)

        # --- LẦN SINH 1 (LỖI) ---
        # LLM sinh code lỗi
        code_1_box = RoundedRectangle(width=3.8, height=1.6, color=GRAY_D, fill_color="#141517", fill_opacity=0.95, corner_radius=0.06)
        code_1_box.move_to(RIGHT * 2.2 + UP * 0.7)
        code_1_lbl = create_markup_text(
            "<b>Bản nháp 1 (Lỗi):</b>\n"
            "<span color='#FF8888'>fn main() {\n"
            "  let s = String::from(\"hello\");\n"
            "  let y = s; // moved s ở đây\n"
            "  println!(\"{}\", s); // Lỗi sử dụng lại s\n"
            "}</span>",
            font_size=9, line_spacing=1.1
        ).move_to(code_1_box.get_center())

        self.play(
            FadeIn(code_1_box),
            Write(code_1_lbl),
            run_time=1.5
        )
        self.wait(3.0)

        # Hiển thị sơ đồ bộ nhớ ban đầu
        self.play(
            FadeIn(res_box), Write(res_lbl),
            FadeIn(s_var), Write(s_lbl),
            Create(s_ptr),
            run_time=1.2
        )
        self.wait(3.0)

        # Khai báo biến y và di chuyển quyền sở hữu
        y_var = RoundedRectangle(width=0.8, height=0.4, color=GRAY_A, fill_color="#141517", fill_opacity=0.95, corner_radius=0.04)
        y_var.move_to(LEFT * 2.6 + UP * 0.2)
        y_lbl = create_text("Biến y", font_size=8, color=WHITE).move_to(y_var.get_center())

        y_ptr = Arrow(start=y_var.get_right(), end=res_box.get_left() + DOWN * 0.15, color=GREEN_B, stroke_width=2, max_tip_length_to_length_ratio=0.15, buff=0.05)

        # Con trỏ s bị gạch chéo đỏ biểu thị lỗi đứt gãy ownership
        s_cross = get_crossmark(color=RED, stroke_width=3).scale(1.5).move_to(s_ptr.get_center())

        # Show y và đứt gãy ownership
        self.play(
            FadeIn(y_var), Write(y_lbl),
            Create(y_ptr),
            Create(s_cross),
            s_ptr.animate.set_color(RED),
            run_time=1.2
        )
        self.wait(3.0)

        # Gửi sang Compiler và đồng thời xóa sơ đồ bộ nhớ
        self.play(
            Create(arrow_to_comp),
            FadeOut(code_1_box, target_position=compiler_box.get_center()),
            FadeOut(code_1_lbl, target_position=compiler_box.get_center()),
            FadeOut(res_box), FadeOut(res_lbl),
            FadeOut(s_var), FadeOut(s_lbl), FadeOut(s_ptr), FadeOut(s_cross),
            FadeOut(y_var), FadeOut(y_lbl), FadeOut(y_ptr),
            run_time=1.5
        )
        self.wait(3.0)

        # Compiler báo lỗi biên dịch
        error_box = RoundedRectangle(width=4.4, height=0.9, color=RED, fill_color="#3c1414", fill_opacity=0.9, corner_radius=0.05)
        error_box.move_to(DOWN * 1.6)
        error_lbl = create_markup_text(
            "<b>Compiler Error (Rust Borrow Checker):</b>\n"
            "<span color='#FF5555'>error[E0382]: borrow of moved value: 's'</span>",
            font_size=8, line_spacing=1.1
        ).move_to(error_box.get_center())

        self.play(
            compiler_box.animate.set_stroke(color=RED).set_fill(color="#551a1a", opacity=0.9),
            FadeIn(error_box),
            Write(error_lbl),
            run_time=1.0
        )
        self.wait(12.0)

        # Gửi lỗi về lại LLM (di chuyển sang LLM và biến mất hoàn toàn)
        self.play(
            Create(arrow_back),
            FadeOut(error_box, target_position=llm_box.get_center()),
            FadeOut(error_lbl, target_position=llm_box.get_center()),
            run_time=1.5
        )
        self.wait(8.0)

        # --- LẦN SINH 2 (SỬA LỖI THÀNH CÔNG) ---
        code_2_box = RoundedRectangle(width=3.8, height=1.6, color=GREEN, fill_color="#141517", fill_opacity=0.95, corner_radius=0.06)
        code_2_box.move_to(RIGHT * 2.2 + UP * 0.7)
        # Sử dụng &amp; thay thế cho & để tránh lỗi XML parser của Pango
        code_2_lbl = create_markup_text(
            "<b>Bản nháp 2 (Đã sửa):</b>\n"
            "<span color='#88FF88'>fn main() {\n"
            "  let s = String::from(\"hello\");\n"
            "  let y = &amp;s; // Mượn tham chiếu\n"
            "  println!(\"{}\", s); // Biên dịch thành công!\n"
            "}</span>",
            font_size=9, line_spacing=1.1
        ).move_to(code_2_box.get_center())

        self.play(
            FadeIn(code_2_box),
            Write(code_2_lbl),
            run_time=1.5
        )
        self.wait(3.0)

        # Vẽ sơ đồ tham chiếu mượn
        res_box_2 = RoundedRectangle(width=2.2, height=0.7, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        res_box_2.move_to(LEFT * 0.8 + UP * 0.7)
        res_lbl_2 = create_text("Vùng nhớ String \"hello\"", font_size=8, color=WHITE).move_to(res_box_2.get_center())

        s_var_2 = RoundedRectangle(width=0.8, height=0.4, color=GRAY_A, fill_color="#141517", fill_opacity=0.95, corner_radius=0.04)
        s_var_2.move_to(LEFT * 2.6 + UP * 1.2)
        s_lbl_2 = create_text("Biến s", font_size=8, color=WHITE).move_to(s_var_2.get_center())

        s_ptr_2 = Arrow(start=s_var_2.get_bottom(), end=res_box_2.get_left() + UP * 0.15, color=BLUE_A, stroke_width=2, max_tip_length_to_length_ratio=0.15, buff=0.05)

        y_var_2 = RoundedRectangle(width=0.8, height=0.4, color=GRAY_A, fill_color="#141517", fill_opacity=0.95, corner_radius=0.04)
        y_var_2.move_to(LEFT * 2.6 + UP * 0.2)
        y_lbl_2 = create_text("Biến y", font_size=8, color=WHITE).move_to(y_var_2.get_center())

        # Mượn tham chiếu: y trỏ tới s
        y_borrow_ptr = Arrow(start=y_var_2.get_top(), end=s_var_2.get_bottom(), color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.15, buff=0.05)
        borrow_lbl = create_text("Mượn (&s)", font_size=7, color=GREEN).next_to(y_borrow_ptr, RIGHT, buff=0.1)

        self.play(
            FadeIn(res_box_2), Write(res_lbl_2),
            FadeIn(s_var_2), Write(s_lbl_2),
            Create(s_ptr_2),
            FadeIn(y_var_2), Write(y_lbl_2),
            Create(y_borrow_ptr), Write(borrow_lbl),
            run_time=1.2
        )
        self.wait(3.0)

        # Gửi lại sang compiler (di chuyển sang compiler và biến mất hoàn toàn, đồng thời xóa sơ đồ bộ nhớ)
        self.play(
            FadeOut(code_2_box, target_position=compiler_box.get_center()),
            FadeOut(code_2_lbl, target_position=compiler_box.get_center()),
            FadeOut(res_box_2), FadeOut(res_lbl_2),
            FadeOut(s_var_2), FadeOut(s_lbl_2), FadeOut(s_ptr_2),
            FadeOut(y_var_2), FadeOut(y_lbl_2), FadeOut(y_borrow_ptr), FadeOut(borrow_lbl),
            run_time=1.5
        )

        # Compiler chuyển sang xanh lá và báo thành công
        success_icon = get_checkmark(color=GREEN, stroke_width=3).next_to(compiler_lbl, RIGHT, buff=0.15)
        
        self.play(
            compiler_box.animate.set_stroke(color=GREEN).set_fill(color="#143c14", opacity=0.9),
            FadeIn(success_icon),
            run_time=1.0
        )
        self.wait(18.0)

        # Dọn dẹp phần 1
        self.play(
            FadeOut(intro_text),
            FadeOut(llm_box), FadeOut(llm_lbl),
            FadeOut(compiler_box), FadeOut(compiler_lbl), FadeOut(success_icon),
            FadeOut(arrow_to_comp), FadeOut(arrow_back),
            FadeOut(part1_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # PHẦN 2: PHẢN HỒI NỘI SINH DẠNG PROMPT (SELF-REFINE & NOISY FEEDBACK)
        # =====================================================================
        part2_title = create_text("2. Phản hồi nội sinh dạng Prompt & Cạm bẫy Nhiễu phản hồi (Noisy Feedback)", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part2_title), run_time=0.8)
        self.wait(3.0)

        # Giải thích khái niệm Intrinsic Feedback và cạm bẫy của nó
        intro_part2 = create_markup_text(
            "<b>Phản hồi nội sinh (Intrinsic Feedback):</b> Yêu cầu mô hình tự tìm lỗi và tự sửa.\n"
            "Nếu chỉ dùng prompt (như Self-Refine) cho lập luận logic, mô hình dễ bị\n"
            "<b>Ảo giác phản hồi (Feedback Hallucination)</b> - biến đáp án đúng thành sai.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)
        self.play(Write(intro_part2), run_time=2.0)
        self.wait(24.0)

        # Mô phỏng quá trình tự sửa lỗi của mô hình đơn lẻ bên trái
        sim_llm_box = RoundedRectangle(width=1.6, height=0.6, color=BLUE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        sim_llm_box.move_to(LEFT * 4.6 + UP * 0.9)
        sim_llm_lbl = create_text("LLM Generator", font_size=10, color=BLUE_A).move_to(sim_llm_box.get_center())

        self.play(FadeIn(sim_llm_box), Write(sim_llm_lbl), run_time=0.8)
        self.wait(4.0)

        # Bước 1: Prompt ban đầu
        prompt_box = RoundedRectangle(width=4.0, height=0.5, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        prompt_box.move_to(LEFT * 3.4 + UP * 0.1)
        prompt_lbl = create_text("Prompt: Hãy giải 17 + 25 = ?", font_size=9, color=YELLOW).move_to(prompt_box.get_center())

        # Nháp 1 (Đúng)
        ans1_box = RoundedRectangle(width=4.0, height=0.5, color=GREEN, fill_color="#143c14", fill_opacity=0.8, corner_radius=0.05)
        ans1_box.next_to(prompt_box, DOWN, buff=0.15)
        ans1_lbl = create_markup_text("<b>LLM (Draft):</b> Đáp án là <span color='#88FF88'>42</span> (Đúng)", font_size=9).move_to(ans1_box.get_center())

        self.play(FadeIn(prompt_box), Write(prompt_lbl), run_time=0.8)
        self.play(FadeIn(ans1_box), Write(ans1_lbl), run_time=0.8)
        self.wait(8.0)

        # Bước 2: Prompt tự đánh giá
        critique_box = RoundedRectangle(width=4.0, height=0.5, color=BLUE_C, fill_color="#141c2b", fill_opacity=0.8, corner_radius=0.05)
        critique_box.next_to(ans1_box, DOWN, buff=0.15)
        critique_lbl = create_text("Prompt tự đánh giá: Câu trả lời trên đã đúng chưa?", font_size=9, color=WHITE).move_to(critique_box.get_center())

        self.play(FadeIn(critique_box), Write(critique_lbl), run_time=0.8)
        self.wait(8.0)

        # LLM tự nhận định sai (Hallucination)
        halluc_box = RoundedRectangle(width=4.0, height=0.5, color=RED, fill_color="#3c1414", fill_opacity=0.8, corner_radius=0.05)
        halluc_box.next_to(critique_box, DOWN, buff=0.15)
        halluc_lbl = create_markup_text("<b>LLM (Critique):</b> Chưa đúng, 17+25 phải bằng <span color='#FF8888'>32</span>", font_size=8).move_to(halluc_box.get_center())

        self.play(FadeIn(halluc_box), Write(halluc_lbl), run_time=0.8)
        self.wait(12.0)

        # Sửa lại thành đáp án sai
        ans2_box = RoundedRectangle(width=4.0, height=0.5, color=RED, fill_color="#3c1414", fill_opacity=0.8, corner_radius=0.05)
        ans2_box.next_to(halluc_box, DOWN, buff=0.15)
        ans2_lbl = create_markup_text("<b>LLM (Final):</b> Sửa lại là <span color='#FF8888'>32</span> (Sai hoàn toàn!)", font_size=9).move_to(ans2_box.get_center())

        self.play(FadeIn(ans2_box), Write(ans2_lbl), run_time=0.8)
        self.wait(12.0)

        # --- MA TRẬN CONFUSION MATRIX Ở BÊN PHẢI ---
        # Trực quan hóa thống kê kết quả tự sửa lỗi
        matrix_center = RIGHT * 3.6 + DOWN * 0.4
        
        matrix_title = create_text("Ma trận Tự sửa lỗi (Confusion Matrix)", font_size=10, color=GOLD_B)
        matrix_title.move_to(matrix_center + UP * 2.1)

        # Nhãn hàng (Trạng thái ban đầu)
        lbl_init = create_text("Nháp ban đầu", font_size=9, color=BLUE_A)
        lbl_init.move_to(matrix_center + LEFT * 1.9 + UP * 0.7)
        
        lbl_init_correct = create_text("Đúng", font_size=9, color=WHITE)
        lbl_init_correct.move_to(matrix_center + LEFT * 1.1 + UP * 0.45)
        lbl_init_incorrect = create_text("Sai", font_size=9, color=WHITE)
        lbl_init_incorrect.move_to(matrix_center + LEFT * 1.1 + DOWN * 0.45)

        # Nhãn cột (Kết quả sau khi tự sửa)
        lbl_fin = create_text("Sau khi Tự sửa lỗi", font_size=9, color=BLUE_A)
        lbl_fin.move_to(matrix_center + UP * 1.6)

        lbl_fin_correct = create_text("Đúng", font_size=9, color=WHITE)
        lbl_fin_correct.move_to(matrix_center + LEFT * 0.45 + UP * 1.1)
        lbl_fin_incorrect = create_text("Sai", font_size=9, color=WHITE)
        lbl_fin_incorrect.move_to(matrix_center + RIGHT * 0.45 + UP * 1.1)

        # Vẽ các ô của ma trận (2x2)
        cell_size = 0.9
        cells = VGroup()
        cell_texts = VGroup()

        cell_data = [
            # Hàng 1 (Đúng -> ...) - Sử dụng đồng nhất 2 màu (Xanh lá / Đỏ) với độ mờ 0.6 và Y=0.45 để không chồng lấn
            ("85%", GREEN_E, 0.6, LEFT * 0.45 + UP * 0.45),
            ("15%", RED_E, 0.6, RIGHT * 0.45 + UP * 0.45),  # Ảo giác phản hồi
            # Hàng 2 (Sai -> ...)
            ("35%", GREEN_E, 0.6, LEFT * 0.45 + DOWN * 0.45),  # Sửa đúng thành công
            ("65%", RED_E, 0.6, RIGHT * 0.45 + DOWN * 0.45)
        ]

        for idx, (percent_str, color, opacity, pos_offset) in enumerate(cell_data):
            cell = Square(side_length=cell_size, color=GRAY_D, stroke_width=1, fill_color=color, fill_opacity=opacity)
            cell.move_to(matrix_center + pos_offset)
            txt = create_text(percent_str, font_size=10, color=WHITE).move_to(cell.get_center())
            
            cells.add(cell)
            cell_texts.add(txt)

        # Khung đỏ làm nổi bật cạm bẫy 15% (Đúng -> Sai)
        highlight_halluc = RoundedRectangle(width=0.92, height=0.92, color=RED, stroke_width=3, fill_opacity=0).move_to(cells[1].get_center())
        halluc_note = create_markup_text(
            "<span color='#FF5555'><b>Ảo giác phản hồi (15%)</b></span>\n"
            "LLM tự ý hủy hoại đáp án đúng.",
            font_size=8, line_spacing=1.2
        ).next_to(highlight_halluc, RIGHT, buff=0.25)

        # Bắt đầu vẽ khung ma trận
        self.play(
            Write(matrix_title),
            Write(lbl_init), Write(lbl_init_correct), Write(lbl_init_incorrect),
            Write(lbl_fin), Write(lbl_fin_correct), Write(lbl_fin_incorrect),
            Create(cells),
            run_time=2.0
        )
        self.wait(2.0)

        # --- DÒNG CHẢY HẠT ĐỘNG (PARTICLE FLOW) ---
        import random
        import numpy as np
        random.seed(42)  # Đảm bảo phân phối hạt ổn định

        dots = VGroup()
        dot_anims = []

        # Stream A (20 hạt Xanh lá - Nháp ban đầu Đúng) xuất hiện ở trên
        for i in range(20):
            dot = Dot(color=GREEN, radius=0.04)
            dot.move_to(matrix_center + UP * 2.3 + LEFT * 0.45 + np.array([random.uniform(-0.15, 0.15), random.uniform(-0.1, 0.1), 0]))
            dots.add(dot)
            # Rẽ nhánh dựa trên phân phối
            if i < 17:  # 85% giữ Đúng
                target_pos = cells[0].get_center() + np.array([random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0])
                dot_anims.append(dot.animate(run_time=random.uniform(1.2, 2.0)).move_to(target_pos))
            else:  # 15% bị sửa thành Sai (đổi màu sang Đỏ khi rơi)
                target_pos = cells[1].get_center() + np.array([random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0])
                dot_anims.append(dot.animate(run_time=random.uniform(1.2, 2.0)).move_to(target_pos).set_color(RED))

        # Stream B (20 hạt Đỏ - Nháp ban đầu Sai) xuất hiện ở trên
        for i in range(20):
            dot = Dot(color=RED, radius=0.04)
            dot.move_to(matrix_center + UP * 2.3 + RIGHT * 0.45 + np.array([random.uniform(-0.15, 0.15), random.uniform(-0.1, 0.1), 0]))
            dots.add(dot)
            # Rẽ nhánh dựa trên phân phối
            if i < 7:  # 35% sửa thành Đúng (đổi màu sang Xanh lá)
                target_pos = cells[2].get_center() + np.array([random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0])
                dot_anims.append(dot.animate(run_time=random.uniform(1.2, 2.0)).move_to(target_pos).set_color(GREEN))
            else:  # 65% vẫn giữ Sai (giữ màu Đỏ)
                target_pos = cells[3].get_center() + np.array([random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0])
                dot_anims.append(dot.animate(run_time=random.uniform(1.2, 2.0)).move_to(target_pos))

        self.play(FadeIn(dots), run_time=0.6)
        self.play(*dot_anims)
        self.wait(1.5)

        # Hiển thị số liệu phần trăm và nhãn ảo giác
        self.play(
            Write(cell_texts),
            Create(highlight_halluc),
            Write(halluc_note),
            run_time=1.5
        )
        self.wait(15.0)

        # Nhãn cảnh báo Nhiễu phản hồi màu đỏ nhấp nháy bên dưới
        warning_lbl = create_markup_text(
            "<span color='#FF3333'><b>PHẢN HỒI NỘI SINH QUÁ NHIỄU (NOISY FEEDBACK)</b></span>",
            font_size=11
        ).move_to(DOWN * 3.2)

        self.play(FadeIn(warning_lbl, shift=UP * 0.2), run_time=0.8)
        # Hiệu ứng nhấp nháy (Pulsing)
        for _ in range(3):
            self.play(warning_lbl.animate.set_opacity(0.3), run_time=0.5)
            self.play(warning_lbl.animate.set_opacity(1.0), run_time=0.5)
        self.wait(20.0)

        # Dọn dẹp phần 2 (bao gồm cả các hạt)
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
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # PHẦN 3: HUẤN LUYỆN TỰ SỬA LỖI (TRAINED CORRECTOR) & THUẬT TOÁN SCORE
        # =====================================================================
        part3_title = create_text("3. Huấn luyện Bộ tự sửa lỗi (Trained Corrector) & Giải thuật SCoRe", font_size=13, color=BLUE_A)
        part3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part3_title), run_time=0.8)
        self.wait(3.0)

        # Lời giới thiệu phương pháp huấn luyện
        intro_part3 = create_markup_text(
            "Để giải quyết nhiễu, ta có thể <b>Huấn luyện (Fine-tune)</b> mô hình để tự sửa lỗi.\n"
            "Tuy nhiên, nếu dùng học tăng cường (RL) thông thường mô hình dễ bị sụp đổ hành vi.\n"
            "Giải thuật **SCoRe** (Google DeepMind) giúp huấn luyện ổn định và hiệu quả.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)
        self.play(Write(intro_part3), run_time=2.0)
        self.wait(24.0)

        # Công thức mục tiêu học tinh chỉnh
        formula_box = RoundedRectangle(width=8.2, height=1.0, color=BLUE_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        formula_box.move_to(UP * 0.9)
        formula_txt = create_markup_text(
            "Tinh chỉnh chính sách sửa lỗi:  <span color='#00FF7F'><i>p</i><sub>θ</sub>( <span color='#FFFF00'>better_correction</span> | <span color='#FF7F7F'>bad_draft</span> )</span>",
            font_size=13
        ).move_to(formula_box.get_center())

        self.play(
            FadeIn(formula_box),
            Write(formula_txt),
            run_time=1.5
        )
        self.wait(24.0)

        # --- ĐỒ THỊ SO SÁNH STANDARD RL vs SCORE (POLICY DRIFT & COLLAPSE) ---
        # Khởi tạo hệ trục tọa độ
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.0, 0.2],
            x_length=7.5,
            y_length=2.5,
            axis_config={"color": GRAY_C, "stroke_width": 2},
            tips=False
        )
        axes.move_to(DOWN * 1.3)

        # Nhãn cho hệ trục tọa độ (không dùng LaTeX để tránh lỗi trên Windows)
        x_lbl = create_text("Bước huấn luyện RL", font_size=9, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.12)
        y_lbl = create_text("Hiệu năng tự sửa lỗi", font_size=9, color=GRAY_A).next_to(axes.y_axis.get_top(), LEFT, buff=0.15)

        self.play(
            Create(axes),
            Write(x_lbl), Write(y_lbl),
            run_time=1.5
        )
        self.wait(2.0)

        # Vẽ vùng an toàn KL Regularization (KL Regularization Safe Zone)
        # Giới hạn an toàn tại Y = 0.8
        origin_pt = axes.c2p(0, 0)
        top_right_pt = axes.c2p(10, 0.8)
        
        safe_zone = Rectangle(
            width=top_right_pt[0] - origin_pt[0],
            height=top_right_pt[1] - origin_pt[1],
            stroke_width=0,
            fill_color=GREEN_E,
            fill_opacity=0.15
        )
        safe_zone.move_to(axes.c2p(5, 0.4))

        kl_limit_line = DashedLine(
            start=axes.c2p(0, 0.8),
            end=axes.c2p(10, 0.8),
            color=GREEN,
            stroke_width=1.5
        )
        kl_limit_lbl = create_text("Vùng an toàn KL (KL Regularization)", font_size=8, color=GREEN_B).move_to(axes.c2p(3.2, 0.85))

        self.play(
            FadeIn(safe_zone),
            Create(kl_limit_line),
            Write(kl_limit_lbl),
            run_time=1.5
        )
        self.wait(3.0)

        # --- ĐƯỜNG CONG STANDARD RL (SỤP ĐỔ HÀNH VI) ---
        standard_rl_points = [
            axes.c2p(0, 0.3),
            axes.c2p(1.5, 0.52),
            axes.c2p(3, 0.65),
            axes.c2p(4.5, 0.45),
            axes.c2p(6, 0.15),
            axes.c2p(8, 0.05),
            axes.c2p(10, 0.02)
        ]
        standard_rl_curve = VMobject(color=RED, stroke_width=3.5)
        standard_rl_curve.set_points_smoothly(standard_rl_points)

        std_rl_lbl = create_markup_text(
            "<span color='#FF5555'><b>Standard RL</b></span>\n(Sụp đổ hành vi)",
            font_size=9
        ).move_to(axes.c2p(5.2, 0.45))

        # Hiệu ứng vẽ đường cong Standard RL
        self.play(
            Create(standard_rl_curve),
            Write(std_rl_lbl),
            run_time=3.0
        )
        self.wait(2.0)

        # Thêm cảnh báo sụp đổ hành vi
        std_rl_cross = get_crossmark(color=RED, stroke_width=3.0).scale(1.2).move_to(axes.c2p(6.5, 0.12))
        collapse_warning = create_text("Sụp đổ hành vi (Behavior Collapse)", font_size=8, color=RED).next_to(std_rl_cross, RIGHT, buff=0.1)

        self.play(
            Create(std_rl_cross),
            Write(collapse_warning),
            run_time=1.0
        )
        self.wait(25.0)

        # --- ĐƯỜNG CONG SCORE (ỔN ĐỊNH & TỐI ƯU) ---
        score_points = [
            axes.c2p(0, 0.3),
            axes.c2p(1.5, 0.46),
            axes.c2p(3, 0.58),
            axes.c2p(5.0, 0.68),
            axes.c2p(7.0, 0.73),
            axes.c2p(9.0, 0.75),
            axes.c2p(10, 0.75)
        ]
        score_curve = VMobject(color=GREEN, stroke_width=3.5)
        score_curve.set_points_smoothly(score_points)

        score_lbl = create_markup_text(
            "<span color='#00FF7F'><b>Giải pháp SCoRe</b></span>\n(Ổn định &amp; Tối ưu)",
            font_size=9
        ).move_to(axes.c2p(6.5, 0.9))

        score_check = get_checkmark(color=GREEN, stroke_width=3.0).scale(1.2).next_to(score_lbl, LEFT, buff=0.1)

        # Hiệu ứng vẽ đường cong SCoRe
        self.play(
            Create(score_curve),
            Write(score_lbl),
            Create(score_check),
            run_time=3.0
        )
        self.wait(35.0)

        # Dọn dẹp phần 3
        self.play(
            FadeOut(intro_part3),
            FadeOut(formula_box), FadeOut(formula_txt),
            FadeOut(axes), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(safe_zone), FadeOut(kl_limit_line), FadeOut(kl_limit_lbl),
            FadeOut(standard_rl_curve), FadeOut(std_rl_lbl), FadeOut(std_rl_cross), FadeOut(collapse_warning),
            FadeOut(score_curve), FadeOut(score_lbl), FadeOut(score_check),
            FadeOut(part3_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # PHẦN 4: TỔNG KẾT PHÂN CẢNH 3.4
        # =====================================================================
        recap_title = create_text("Tổng kết: Các cơ chế Tinh chỉnh & Tự sửa lỗi (Refinement)", font_size=13, color=YELLOW)
        recap_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(recap_title), run_time=0.8)
        self.wait(3.0)

        # Vẽ bảng so sánh
        comparison_table = VGroup()
        headers = ["Phương pháp", "Cơ chế phản hồi", "Đặc trưng / Cạm bẫy"]
        header_colors = [BLUE_A, WHITE, RED]
        
        # Dòng tiêu đề
        header_group = VGroup()
        for idx, h_text in enumerate(headers):
            cell = RoundedRectangle(width=3.2, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            cell.move_to(LEFT * (3.4 * (1 - idx)) + UP * 1.0)
            lbl = create_text(h_text, font_size=11, color=header_colors[idx]).move_to(cell.get_center())
            header_group.add(VGroup(cell, lbl))
        comparison_table.add(header_group)

        # 3 dòng dữ liệu
        table_rows = [
            ("Phản hồi Ngoại sinh", "Từ Compiler / Môi trường bên ngoài", "Độ chính xác cao, rất hiệu quả"),
            ("Nội sinh - Prompted", "Mô hình tự re-prompt tự sửa", "Ảo giác phản hồi, nhiễu (Noisy)"),
            ("Nội sinh - Trained", "Tự tinh chỉnh RL (SCoRe)", "KL Reg giúp chống sụp đổ hành vi")
        ]

        row_y_coords = [0.2, -0.6, -1.4]
        for r_idx, row_data in enumerate(table_rows):
            row_group = VGroup()
            for c_idx, cell_text in enumerate(row_data):
                cell = RoundedRectangle(width=3.2, height=0.6, color=GRAY_E, fill_color="#121315", fill_opacity=0.8, corner_radius=0.04)
                cell.move_to(LEFT * (3.4 * (1 - c_idx)) + UP * row_y_coords[r_idx])
                
                # Tô màu nhãn giới hạn ở cột 3
                t_color = RED if c_idx == 2 else (GREEN if c_idx == 1 else WHITE)
                lbl = create_text(cell_text, font_size=9, color=t_color).move_to(cell.get_center())
                
                row_group.add(VGroup(cell, lbl))
            comparison_table.add(row_group)

        self.play(FadeIn(comparison_table), run_time=1.8)
        self.wait(45.0)

        # Dọn dẹp kết thúc toàn bộ video của Phân cảnh 3.4
        self.play(
            FadeOut(comparison_table),
            FadeOut(recap_title),
            FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(2.0)
