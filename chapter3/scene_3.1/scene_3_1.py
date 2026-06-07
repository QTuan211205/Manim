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


class Scene3_1(Scene):
    def construct(self):
        # (Lời thoại đã được phân phối xuống từng phần cụ thể bên dưới)

        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH
        # =====================================================================
        chapter_title = create_text("Chương 3: Bộ điều phối cấp cao", font_size=24, color=YELLOW)
        chapter_sub = create_text("Phần 3.1: Các mô hình đánh giá & Kỹ thuật Chaining", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(5.0)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Các mô hình đánh giá & Kỹ thuật Chaining", font_size=16, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(3.0)

        # =====================================================================
        # LỜI THOẠI: "Mục tiêu của system designer là thiết kế một hệ thống G sinh ra các
        # acceptable sequences. Slide viết mục tiêu là tối ưu kỳ vọng acceptability A(y)
        # trên output của G: arg max_G E[A(y)]. Acceptability có thể là correctness hoặc human preferences."
        # =====================================================================
        # PHẦN 1: GIỚI THIỆU BỘ ĐIỀU PHỐI CẤP CAO (META-GENERATION INTRO)
        # =====================================================================
        part1_title = create_text("1. Bộ điều phối cấp cao (Meta-Generation Strategies)", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part1_title), run_time=0.8)
        self.wait(3.0)

        # Mô tả khái quát
        intro_text = create_text(
            "Coi toàn bộ các thuật toán sinh tự hồi quy cơ bản ở Chương 2\n"
            "như một chiếc 'Hộp đen' (Black-box) và xây dựng bộ điều phối bên ngoài.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.3)
        self.play(Write(intro_text), run_time=2.0)
        self.wait(12.0)

        # Vẽ Hộp đen Base Generator
        black_box = RoundedRectangle(
            width=4.0, height=2.2, color=GRAY_D, fill_color="#1a1c20", fill_opacity=0.9, corner_radius=0.1
        )
        black_box.move_to(DOWN * 0.5)
        black_box_lbl = create_text("Base Generator\n(LLM)", font_size=14, color=WHITE).move_to(black_box.get_center())
        
        # Token x và y đại diện
        token_x = create_text("Prompt x", font_size=12, color=GREEN)
        token_x.next_to(black_box, LEFT, buff=1.2)
        arrow_in = Arrow(start=token_x.get_right(), end=black_box.get_left(), color=GREEN, stroke_width=2, buff=0.1)
        
        token_y = create_text("Output y", font_size=12, color=YELLOW)
        token_y.next_to(black_box, RIGHT, buff=1.2)
        arrow_out = Arrow(start=black_box.get_right(), end=token_y.get_left(), color=YELLOW, stroke_width=2, buff=0.1)

        self.play(
            FadeIn(black_box), Write(black_box_lbl),
            FadeIn(token_x), Create(arrow_in),
            run_time=1.2
        )
        self.play(Create(arrow_out), FadeIn(token_y), run_time=1.0)
        self.wait(16.0)

        # Khung bao bọc ngoài: Meta-Generation Controller
        controller_frame = RoundedRectangle(
            width=9.8, height=4.3, color=BLUE_A, fill_color=BLUE_E, fill_opacity=0.08, corner_radius=0.15, stroke_width=2
        )
        controller_frame.move_to(DOWN * 0.5)
        controller_lbl = create_text("Meta-Generation Controller", font_size=14, color=BLUE_A)
        controller_lbl.next_to(controller_frame.get_top(), DOWN, buff=0.2)

        # Mũi tên phản hồi vòng lại từ Output y về Prompt x
        feedback_arrow = CurvedArrow(
            start_point=token_y.get_bottom() + DOWN * 0.2,
            end_point=token_x.get_bottom() + DOWN * 0.2,
            angle=-PI/2,
            color=BLUE_A
        )
        feedback_lbl = create_text("Phản hồi vĩ mô (Feedback Loop)", font_size=9, color=BLUE_A)
        feedback_lbl.next_to(feedback_arrow, DOWN, buff=0.15)

        self.play(
            Create(controller_frame), Write(controller_lbl),
            Create(feedback_arrow), Write(feedback_lbl),
            run_time=1.5
        )
        self.wait(10.0)

        # Bổ sung công thức formalization (Slides 97-98)
        formal_box = RoundedRectangle(
            width=6.6, height=2.4, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.1
        ).move_to(ORIGIN)
        formal_title = create_text("Định nghĩa toán học", font_size=11, color=YELLOW).next_to(formal_box.get_top(), DOWN, buff=0.18)
        
        formula_meta = create_markup_text(
            "Meta-generator:   <span foreground='#33CCFF'>y ~ G(y | x; g<sub>1</sub>, g<sub>2</sub>, ..., g<sub>G</sub>, φ)</span>",
            font_size=9.5, color=WHITE
        )
        formula_special = create_markup_text(
            "Special case (Token-level):   <span foreground='#AAAAAA'>y ~ g(y | x; p<sub>θ</sub>, φ)</span>",
            font_size=9.5, color=WHITE
        )
        formulas_group = VGroup(formula_meta, formula_special).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(formal_title, DOWN, buff=0.25)
        
        formal_grp = VGroup(formal_box, formal_title, formulas_group)
        
        self.play(
            FadeOut(black_box), FadeOut(black_box_lbl),
            FadeOut(token_x), FadeOut(arrow_in),
            FadeOut(token_y), FadeOut(arrow_out),
            FadeOut(controller_frame), FadeOut(controller_lbl),
            FadeOut(feedback_arrow), FadeOut(feedback_lbl),
            FadeIn(formal_grp, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait(10.0)

        # Dọn dẹp phần 1
        self.play(
            FadeOut(formal_grp),
            FadeOut(part1_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # LỜI THOẠI: "Chúng ta đã biết cách sinh probable outputs y ~ pθ(y|x), nhưng nếu các
        # output probable đó không acceptable thì cần thêm chiến lược. Ý tưởng đầu tiên của meta-generation
        # là tận dụng thông tin bên ngoài, ví dụ học một evaluator v(y) ≈ A(y) và dùng nó khi sinh.
        # Slide 91-92 nhấn mạnh sự tương đương thuật ngữ: Evaluator ≈ critic ≈ verifier ≈ value ≈ reward model ≈ scoring model.
        #
        # Điểm quan trọng của acceptability là nó không nhất thiết trùng với probability của mô hình.
        # Một output có thể probable theo pθ nhưng không correct, không được con người thích, hoặc không
        # đáp ứng yêu cầu của hệ thống. Meta-generation được đưa vào để tìm cách sinh ra sequences acceptable hơn."
        # =====================================================================
        # PHẦN 2: MÔ HÌNH PHẦN THƯỞNG ĐÁNH GIÁ KẾT QUẢ (OUTCOME-BASED RM)
        # =====================================================================
        part2_title = create_text("2. Mô hình phần thưởng đánh giá kết quả (Outcome-based Reward Model)", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part2_title), run_time=0.8)
        self.wait(3.0)

        # Giải thích bằng văn bản
        rm_intro = create_text(
            "Outcome-based Reward Model (Evaluator / Verifier) được huấn luyện\n"
            "dưới dạng một bộ phân loại (Classifier) để chấm điểm câu trả lời hoàn chỉnh.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 1.5)
        self.play(Write(rm_intro), run_time=2.0)
        self.wait(16.0)

        # Vẽ sơ đồ Classifier chấm điểm các câu đúng/sai
        classifier_box = RoundedRectangle(
            width=3.6, height=2.0, color=GRAY_D, fill_color="#1a1c20", fill_opacity=0.9, corner_radius=0.1
        )
        classifier_box.move_to(ORIGIN)
        classifier_lbl = create_text("Classifier\n(Reward Model)", font_size=13, color=WHITE).move_to(classifier_box.get_center())

        # Các khối câu trả lời đúng (xanh lá) và sai (đỏ)
        sample_correct = VGroup(
            RoundedRectangle(width=2.5, height=0.9, color=GREEN, fill_color=GREEN_E, fill_opacity=0.3, corner_radius=0.08),
            create_text("Đáp án A\n(Chính xác)", font_size=10, color=WHITE),
            get_checkmark().shift(RIGHT * 0.9 + UP * 0.25)
        )
        sample_correct[1].move_to(sample_correct[0].get_center())
        sample_correct.move_to(LEFT * 4.2 + UP * 0.6)

        sample_incorrect = VGroup(
            RoundedRectangle(width=2.5, height=0.9, color=RED, fill_color=RED_E, fill_opacity=0.3, corner_radius=0.08),
            create_text("Đáp án B\n(Sai sót)", font_size=10, color=WHITE),
            get_crossmark().shift(RIGHT * 0.9 + UP * 0.25)
        )
        sample_incorrect[1].move_to(sample_incorrect[0].get_center())
        sample_incorrect.move_to(LEFT * 4.2 + DOWN * 1.0)

        self.play(
            FadeIn(classifier_box), Write(classifier_lbl),
            FadeIn(sample_correct), FadeIn(sample_incorrect),
            run_time=1.2
        )
        self.wait(16.0)

        # Thanh hiển thị điểm Reward Score ở bên phải
        score_bg = RoundedRectangle(width=0.4, height=3.0, color=GRAY_E, fill_color=BLACK, fill_opacity=0.5, corner_radius=0.05)
        score_bg.move_to(RIGHT * 4.2)
        score_lbl = create_text("Reward Score", font_size=9, color=GRAY_B).next_to(score_bg, UP, buff=0.15)
        
        self.play(Create(score_bg), Write(score_lbl), run_time=1.0)

        # 1. Minh họa đánh giá Đáp án A (Đúng) -> Điểm 95%
        arrow_flow_1 = Arrow(start=sample_correct.get_right(), end=classifier_box.get_left() + UP * 0.4, color=GREEN, stroke_width=2, buff=0.1)
        self.play(Create(arrow_flow_1), run_time=0.8)
        
        # Cột điểm tăng lên màu xanh lá
        score_fill_1 = Rectangle(width=0.36, height=3.0 * 0.95, color=GREEN, fill_color=GREEN, fill_opacity=0.8)
        score_fill_1.align_to(score_bg, DOWN).shift(UP * 0.02).move_to(score_bg.get_center())
        score_val_1 = create_text("95%", font_size=10, color=GREEN).next_to(score_bg, RIGHT, buff=0.15)
        
        self.play(
            FadeIn(score_fill_1, shift=UP * 0.2),
            Write(score_val_1),
            run_time=1.2
        )
        self.wait(10.0)

        # Clear điểm 1
        self.play(FadeOut(arrow_flow_1), FadeOut(score_fill_1), FadeOut(score_val_1), run_time=0.6)

        # 2. Minh họa đánh giá Đáp án B (Sai) -> Điểm 12%
        arrow_flow_2 = Arrow(start=sample_incorrect.get_right(), end=classifier_box.get_left() + DOWN * 0.4, color=RED, stroke_width=2, buff=0.1)
        self.play(Create(arrow_flow_2), run_time=0.8)

        score_fill_2 = Rectangle(width=0.36, height=3.0 * 0.12, color=RED, fill_color=RED, fill_opacity=0.8)
        # Căn chỉnh để cột mọc từ đáy lên
        score_fill_2.align_to(score_bg, DOWN).shift(UP * 0.02)
        score_val_2 = create_text("12%", font_size=10, color=RED).next_to(score_bg, RIGHT, buff=0.15)

        self.play(
            FadeIn(score_fill_2, shift=UP * 0.05),
            Write(score_val_2),
            run_time=1.2
        )
        self.wait(10.0)

        # Xóa luồng đánh giá Đáp án B
        self.play(FadeOut(arrow_flow_2), FadeOut(score_fill_2), FadeOut(score_val_2), run_time=0.6)

        # Hiển thị chú thích đặc tính "Outcome-based" quan trọng dưới đáy
        outcome_lbl = create_markup_text(
            "<b>Đặc tính cốt lõi (Outcome-based):</b> Chỉ đánh giá điểm số một lần duy nhất tại vị trí kết thúc\n"
            "toàn bộ chuỗi văn bản. Không giám sát quá trình lập luận trung gian từng bước.",
            font_size=12, color=YELLOW
        ).move_to(DOWN * 2.8)

        self.play(FadeIn(outcome_lbl, shift=UP * 0.15), run_time=1.0)
        self.wait(24.0)

        # Dọn dẹp phần 2
        self.play(
            FadeOut(rm_intro), FadeOut(classifier_box), FadeOut(classifier_lbl),
            FadeOut(sample_correct), FadeOut(sample_incorrect),
            FadeOut(score_bg), FadeOut(score_lbl), FadeOut(outcome_lbl),
            FadeOut(part2_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # LỜI THOẠI: "Chaining compose các generators theo thứ tự: y1 ~ g1(x), y2 ~ g2(x,y1),
        # y3 ~ g3(x,y2). Chain-of-thought là ví dụ điển hình: chúng ta sinh intermediate thought z,
        # rồi dùng z để sinh answer a. Chúng ta ví von CoT như một dải băng ghi chép (writeable tape)
        # giúp tăng tính biểu diễn nhờ độ dài đầu ra linh hoạt (variable output length).
        #
        # Với chain-of-thought, đây là một decomposition đơn giản nhưng có tác động sâu: hệ thống
        # cho phép sinh một intermediate thought z, rồi dùng z để sinh answer a. Slide cũng nói
        # chain-of-thought tăng expressivity vì output length có thể biến đổi, tương tự một writable tape."
        # =====================================================================
        # PHẦN 3: KỸ THUẬT CHAINING & CHAIN OF THOUGHT (CoT)
        # =====================================================================
        part3_title = create_text("3. Kỹ thuật Chaining & Chuỗi suy nghĩ (Chain of Thought)", font_size=13, color=BLUE_A)
        part3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part3_title), run_time=0.8)
        self.wait(3.0)

        # Ý tưởng chính
        chain_intro = create_markup_text(
            "Phân rã bài toán lập luận phức tạp thành các bước giải tuần tự:\n"
            "Prompt <i>x</i> → Suy nghĩ trung gian <i>z</i> → Đáp án cuối cùng <i>y</i>",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 1.5)
        self.play(Write(chain_intro), run_time=2.0)
        self.wait(16.0)

        # So sánh Direct Generation vs Chaining
        compare_lbl_1 = create_text("Cách 1: Giải trực tiếp (Direct)", font_size=11, color=GRAY_A)
        compare_lbl_1.move_to(LEFT * 3.6 + UP * 0.3)

        direct_flow = VGroup(
            create_text("Prompt x", font_size=10, color=GREEN),
            Arrow(start=LEFT*0.5, end=RIGHT*0.5, color=GRAY_D, stroke_width=1.5),
            create_text("Đáp án y", font_size=10, color=RED),
            get_crossmark().scale(0.8)
        )
        direct_flow.arrange(RIGHT, buff=0.2)
        direct_flow.move_to(LEFT * 3.6 + DOWN * 0.4)
        direct_flow[3].next_to(direct_flow[2], RIGHT, buff=0.15)

        compare_lbl_2 = create_text("Cách 2: Chuỗi lập luận (Chaining/CoT)", font_size=11, color=GRAY_A)
        compare_lbl_2.move_to(RIGHT * 3.6 + UP * 0.3)

        chain_flow = VGroup(
            create_text("Prompt x", font_size=10, color=GREEN),
            Arrow(start=LEFT*0.3, end=RIGHT*0.3, color=GRAY_D, stroke_width=1.5),
            create_text("Trung gian z", font_size=10, color=BLUE_B),
            Arrow(start=LEFT*0.3, end=RIGHT*0.3, color=GRAY_D, stroke_width=1.5),
            create_text("Đáp án y", font_size=10, color=GREEN),
            get_checkmark().scale(0.8)
        )
        chain_flow.arrange(RIGHT, buff=0.15)
        chain_flow.move_to(RIGHT * 3.6 + DOWN * 0.4)
        chain_flow[5].next_to(chain_flow[4], RIGHT, buff=0.15)

        chain_formulas = create_markup_text(
            "Công thức:  y<sub>1</sub> ~ g<sub>1</sub>(x),   y<sub>2</sub> ~ g<sub>2</sub>(x, y<sub>1</sub>),   y<sub>3</sub> ~ g<sub>3</sub>(x, y<sub>2</sub>)",
            font_size=9, color=BLUE_A
        ).next_to(chain_flow, DOWN, buff=0.25)

        self.play(
            FadeIn(compare_lbl_1), Create(direct_flow),
            FadeIn(compare_lbl_2), Create(chain_flow),
            FadeIn(chain_formulas, shift=UP * 0.1),
            run_time=1.5
        )
        self.wait(20.0)

        # Xóa dòng so sánh để tập trung giải thích bộ nhớ băng ghi (Scratchpad)
        self.play(
            FadeOut(compare_lbl_1), FadeOut(direct_flow),
            FadeOut(compare_lbl_2), FadeOut(chain_flow),
            FadeOut(chain_formulas),
            run_time=0.8
        )
        self.wait(1.0)

        # Trực quan hóa Scratchpad (Turing Machine Tape)
        scratchpad_lbl = create_text("Băng ghi trung gian (Scratchpad Memory Tape)", font_size=12, color=YELLOW)
        scratchpad_lbl.move_to(UP * 0.4)

        # Vẽ các ô băng ghi
        tape_boxes = VGroup()
        for j in range(7):
            box = Square(side_length=0.7, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.8)
            tape_boxes.add(box)
        tape_boxes.arrange(RIGHT, buff=0.08)
        tape_boxes.move_to(DOWN * 0.5)

        # Con trỏ đọc ghi (Read/Write Head)
        rw_head = Triangle(color=BLUE_A, fill_color=BLUE_A, fill_opacity=0.6).scale(0.18).rotate(180*DEGREES)
        # Đặt mũi nhọn chỉ vào ô trung tâm (ô index 3)
        rw_head.next_to(tape_boxes[3], UP, buff=0.1)

        self.play(
            Write(scratchpad_lbl),
            Create(tape_boxes),
            FadeIn(rw_head),
            run_time=1.2
        )
        self.wait(8.0)

        # Điền các token trung gian z1, z2, z3 vào băng ghi
        z_tokens = ["z1", "z2", "z3", "", "", "", ""]
        z_texts = VGroup()
        for j, tok in enumerate(z_tokens):
            if tok:
                txt = create_text(tok, font_size=12, color=BLUE_B)
                txt.move_to(tape_boxes[j].get_center())
                z_texts.add(txt)

        self.play(
            Write(z_texts),
            run_time=1.0
        )
        self.wait(6.0)

        # Hoạt họa băng ghi trượt sang trái khi con trỏ di chuyển (mô phỏng đọc ghi token mới z4)
        z4_text = create_text("z4", font_size=12, color=BLUE_B)
        z4_text.move_to(tape_boxes[3].get_center())
        
        self.play(
            VGroup(tape_boxes, z_texts).animate.shift(LEFT * 0.78),
            run_time=1.2
        )
        self.play(Write(z4_text), run_time=0.8)
        self.wait(12.0)

        # Giải thích tính toán ngôn ngữ (Turing machine expressiveness)
        express_lbl = create_markup_text(
            "<b>Khả năng biểu đạt (Turing Machine Expressiveness):</b> Việc sinh ra các token trung gian\n"
            "như <i>z<sub>1</sub>, z<sub>2</sub>, z<sub>3</sub></i> đóng vai trò như một bộ nhớ phụ, cung cấp tài nguyên tính toán\n"
            "giúp mô hình vượt qua giới hạn độ sâu kiến trúc cố định của mạng Transformer.",
            font_size=11, color=LIGHT_GREY, line_spacing=1.3
        ).move_to(DOWN * 2.5)

        self.play(FadeIn(express_lbl, shift=UP * 0.15), run_time=1.0)
        self.wait(32.0)

        # Dọn dẹp phần 3
        self.play(
            FadeOut(chain_intro), FadeOut(scratchpad_lbl), FadeOut(tape_boxes),
            FadeOut(z_texts), FadeOut(z4_text), FadeOut(rw_head), FadeOut(express_lbl),
            FadeOut(part3_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # LỜI THOẠI: "Chaining có thể mở rộng sang Self-Ask, Demonstrate-Search-Predict (DSP),
        # System-2 Attention và Draft-Sketch-Prove. Takeaway: chaining phân rã quá trình sinh và tích hợp
        # công cụ hoặc mô hình ngoài, nhưng chaining đơn thuần không giúp khám phá output space."
        # =====================================================================
        # PHẦN 4: SƠ ĐỒ TỰ HỎI (SELF-ASK) & GỌI CÔNG CỤ (TOOL USE)
        # =====================================================================
        part4_title = create_text("4. Quy trình Tự hỏi (Self-Ask) & Gọi công cụ (Tool Use)", font_size=13, color=BLUE_A)
        part4_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part4_title), run_time=0.8)
        self.wait(3.0)

        # Đặt câu hỏi ví dụ x
        question_box = RoundedRectangle(
            width=10.0, height=0.8, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08
        )
        question_box.move_to(UP * 1.5)
        question_text = create_markup_text(
            "<b>Prompt x:</b> <i>\"Complex Question (Requires Multi-step Reasoning)\"</i>",
            font_size=12, color=YELLOW
        )
        question_text.move_to(question_box.get_center())

        self.play(FadeIn(question_box), Write(question_text), run_time=1.0)
        self.wait(16.0)

        # Khối chức năng Tool bên phải
        tool_box = RoundedRectangle(
            width=3.0, height=2.2, color=ORANGE, fill_color=ORANGE, fill_opacity=0.08, corner_radius=0.1, stroke_width=2
        )
        tool_box.move_to(RIGHT * 4.5 + DOWN * 0.6)
        tool_title = create_text("Tìm kiếm / Công cụ\n(Search Engine / API)", font_size=11, color=ORANGE).move_to(tool_box.get_center())
        
        self.play(FadeIn(tool_box), Write(tool_title), run_time=1.0)
        self.wait(4.0)

        # Quy trình bước 1: Tự hỏi câu hỏi phụ 1
        step1_box = RoundedRectangle(width=4.8, height=0.6, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.05)
        step1_box.move_to(LEFT * 2.2 + UP * 0.3)
        step1_lbl = create_text("Self-Ask 1: Sub-question 1", font_size=10, color=WHITE)
        step1_lbl.move_to(step1_box.get_center())

        self.play(FadeIn(step1_box), Write(step1_lbl), run_time=0.8)
        self.wait(12.0)

        # Mũi tên gọi sang công cụ
        arrow_to_tool1 = Arrow(start=step1_box.get_right(), end=tool_box.get_left(), color=ORANGE, stroke_width=1.5, buff=0.1)
        self.play(Create(arrow_to_tool1), run_time=0.6)
        self.wait(4.0)

        # Phản hồi từ công cụ về bước 1
        step1_res = create_text("Sub-answer 1 (API Response)", font_size=10, color=GREEN)
        step1_res.next_to(step1_box, DOWN, buff=0.15)
        
        self.play(Write(step1_res), run_time=0.8)
        self.wait(12.0)

        # Quy trình bước 2: Tự hỏi câu hỏi phụ 2
        step2_box = RoundedRectangle(width=4.8, height=0.6, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.05)
        step2_box.move_to(LEFT * 2.2 + DOWN * 0.9)
        step2_lbl = create_text("Self-Ask 2: Sub-question 2 (dependent)", font_size=10, color=WHITE)
        step2_lbl.move_to(step2_box.get_center())

        self.play(FadeIn(step2_box), Write(step2_lbl), run_time=0.8)
        self.wait(12.0)

        # Mũi tên gọi sang công cụ 2
        arrow_to_tool2 = Arrow(start=step2_box.get_right(), end=tool_box.get_left(), color=ORANGE, stroke_width=1.5, buff=0.1)
        self.play(Create(arrow_to_tool2), run_time=0.6)
        self.wait(4.0)

        # Phản hồi từ công cụ về bước 2
        step2_res = create_text("Sub-answer 2 (API Response)", font_size=10, color=GREEN)
        step2_res.next_to(step2_box, DOWN, buff=0.15)

        self.play(Write(step2_res), run_time=0.8)
        self.wait(14.0)

        # Kết luận đáp án cuối cùng y
        final_ans_box = RoundedRectangle(
            width=12.0, height=0.7, color=GREEN, fill_color="#141517", fill_opacity=0.9, corner_radius=0.08
        )
        final_ans_box.move_to(DOWN * 2.8)
        final_ans_text = create_markup_text(
            "<b>Đáp án y:</b> <i>\"Final Answer (Aggregated from sub-answers)\"</i>",
            font_size=11, color=GREEN
        )
        final_ans_text.move_to(final_ans_box.get_center())

        self.play(FadeIn(final_ans_box), Write(final_ans_text), run_time=1.0)
        self.wait(22.0)

        # Dọn dẹp phần 4
        self.play(
            FadeOut(question_box), FadeOut(question_text), FadeOut(tool_box), FadeOut(tool_title),
            FadeOut(step1_box), FadeOut(step1_lbl), FadeOut(arrow_to_tool1), FadeOut(step1_res),
            FadeOut(step2_box), FadeOut(step2_lbl), FadeOut(arrow_to_tool2), FadeOut(step2_res),
            FadeOut(final_ans_box), FadeOut(final_ans_text), FadeOut(part4_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # LỜI THOẠI: "Ý tưởng thứ hai là gọi generator nhiều hơn một lần để search for good sequences.
        # Với oracle verifier loop, chúng ta có thể lặp: sinh intermediate z ~ pθ(z|x), sinh answer
        # y ~ pθ(y|x,z), rồi dừng khi verifier xác nhận answer correct.
        #
        # Formalization của slide là y ~ G(y|x; g1, g2, ..., gG, φ). Design choices gồm chiến lược G,
        # lựa chọn các generators g1 đến gG, và các parameter khác như số lượng token."
        # =====================================================================
        # BƯỚC 5: TỔNG QUAN PHÂN LẠI CHIẾN LƯỢC MÔ HÌNH (PREVIEW SLIDE)
        # =====================================================================
        preview_title = create_text("Tổng quan về Bộ điều phối cấp cao (Meta-Generation)", font_size=13, color=YELLOW)
        preview_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(preview_title), run_time=0.8)
        self.wait(3.0)

        # Vẽ bảng phân loại 4 hướng tiếp cận
        grid_elements = VGroup()
        
        # Hàm vẽ các biểu tượng trực quan (visual icons) cho slide tổng kết
        def get_chain_icon(color):
            g = VGroup()
            c1 = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(LEFT * 0.45)
            c2 = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5)
            c3 = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(RIGHT * 0.45)
            a1 = Arrow(start=c1.get_right(), end=c2.get_left(), color=color, stroke_width=1.5, buff=0.02, max_tip_length_to_length_ratio=0.3)
            a2 = Arrow(start=c2.get_right(), end=c3.get_left(), color=color, stroke_width=1.5, buff=0.02, max_tip_length_to_length_ratio=0.3)
            g.add(c1, c2, c3, a1, a2)
            return g

        def get_parallel_icon(color):
            g = VGroup()
            for dy in [0.25, 0, -0.25]:
                arr = Arrow(start=LEFT*0.35 + UP*dy, end=RIGHT*0.35 + UP*dy, color=color, stroke_width=1.5, buff=0, max_tip_length_to_length_ratio=0.25)
                g.add(arr)
            return g

        def get_tree_icon(color):
            g = VGroup()
            r = Circle(radius=0.07, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(UP * 0.3)
            c_l = Circle(radius=0.07, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(DOWN * 0.35 + LEFT * 0.35)
            c_r = Circle(radius=0.07, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5).shift(DOWN * 0.35 + RIGHT * 0.35)
            l1 = Line(r.get_bottom() + LEFT*0.02, c_l.get_top() + RIGHT*0.02, color=color, stroke_width=1.5)
            l2 = Line(r.get_bottom() + RIGHT*0.02, c_r.get_top() + LEFT*0.02, color=color, stroke_width=1.5)
            g.add(r, c_l, c_r, l1, l2)
            return g

        def get_correction_icon(color):
            g = VGroup()
            node = Circle(radius=0.09, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.5)
            loop = CurvedArrow(
                start_point=UP*0.08 + RIGHT*0.08,
                end_point=UP*0.08 + LEFT*0.08,
                angle=270*DEGREES,
                color=color,
                stroke_width=1.5
            ).scale(1.4).shift(UP * 0.25)
            g.add(node, loop)
            return g

        def make_grid_cell(title_str, desc_str, pos, icon_creator, color=BLUE_A):
            cell = RoundedRectangle(width=5.2, height=1.6, color=color, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
            cell.move_to(pos)
            
            icon = icon_creator(color)
            icon.move_to(pos + LEFT * 1.8)
            
            title = create_text(title_str, font_size=11, color=color)
            title.move_to(pos + UP * 0.3)
            title.align_to(cell, LEFT)
            title.shift(RIGHT * 1.4)
            
            desc = create_text(desc_str, font_size=9, color=WHITE, line_spacing=1.3)
            desc.move_to(pos + DOWN * 0.3)
            desc.align_to(cell, LEFT)
            desc.shift(RIGHT * 1.4)
            
            return VGroup(cell, icon, title, desc)

        c1 = make_grid_cell("1. Chaining & CoT (Chuỗi hóa)", "Phân rã lập luận logic đa bước.\nSinh các token z làm băng đệm.", LEFT * 2.8 + UP * 0.5, get_chain_icon, color=BLUE_A)
        c2 = make_grid_cell("2. Parallel (Sinh song song)", "Best-of-N, Majority Voting, MBR.\nBiểu quyết, tích hợp mô hình phần thưởng.", RIGHT * 2.8 + UP * 0.5, get_parallel_icon, color=GREEN)
        c3 = make_grid_cell("3. Tree Search (Tìm kiếm trên cây)", "Duyệt cây ToT, MCTS, Backtracking.\nSử dụng PRM đánh giá từng bước lập luận.", LEFT * 2.8 + DOWN * 1.5, get_tree_icon, color=ORANGE)
        c4 = make_grid_cell("4. Self-Correction (Tự sửa lỗi)", "Mô hình tự chỉnh sửa bản nháp.\nNhận feedback ngoại sinh / nội sinh.", RIGHT * 2.8 + DOWN * 1.5, get_correction_icon, color=PURPLE_A)

        self.play(
            FadeIn(c1), FadeIn(c2),
            FadeIn(c3), FadeIn(c4),
            run_time=1.8
        )
        self.wait(35.0)  # Thuyết minh tổng kết chương 3

        # Dọn dẹp kết thúc phân cảnh
        self.play(
            FadeOut(c1), FadeOut(c2), FadeOut(c3), FadeOut(c4),
            FadeOut(preview_title), FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(2.0)
