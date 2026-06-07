import os
import tempfile
import random
from manim import *

# Cấu hình thư mục tạm thời cho text và tex để tránh lỗi phân quyền trên Windows
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

# Hàm hỗ trợ tạo Text đảm bảo hiển thị chuẩn xác trên Windows
def create_text(text, font_size=24, font="Segoe UI", color=WHITE, **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    t = Text(text, font_size=base_size, font=font, color=color, **kwargs)
    t.scale(scale_factor)
    return t

# Hàm hỗ trợ tạo MarkupText đảm bảo hiển thị chuẩn xác trên Windows
def create_markup_text(text, font_size=24, font="Segoe UI", **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    t = MarkupText(text, font_size=base_size, font=font, **kwargs)
    t.scale(scale_factor)
    return t


class Scene4_2(Scene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH
        # =====================================================================
        chapter_title = create_text("Chương 4: Hiệu năng hệ thống (Systems Efficiency)", font_size=24, color=YELLOW)
        chapter_sub = create_text("Phần 4.2: Giải mã đầu cơ (Speculative Decoding)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(15.0)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Giải mã đầu cơ (Speculative Decoding)", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(10.0)

        # =====================================================================
        # BƯỚC 2: SỰ KẾT HỢP GIỮA DRAFT MODEL & TARGET MODEL
        # =====================================================================
        intro_text = create_markup_text(
            "<b>Điểm nghẽn VRAM &amp; Băng thông (Memory Bottleneck)</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 1.8)
        self.play(Write(intro_text), run_time=2.0)
        self.wait(25.0)

        # Tạo mô hình nháp Draft Model (Màu cam, nhỏ bên trái)
        draft_box = RoundedRectangle(width=2.0, height=1.4, color=ORANGE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        draft_box.move_to(LEFT * 3.5 + DOWN * 0.8)
        draft_lbl = create_markup_text("<b>Draft Model</b>\n<span foreground=\"#FFA500\">Mô hình Nháp (1B)</span>", font_size=10, color=ORANGE, line_spacing=1.2).next_to(draft_box, UP, buff=0.15)
        
        # Vẽ các lõi tính toán nhỏ trong Draft Model
        draft_cores = VGroup()
        for r in range(2):
            for c in range(2):
                core = Square(side_length=0.2, color=ORANGE, fill_color=ORANGE, fill_opacity=0.15, stroke_width=0.8)
                core.move_to(draft_box.get_center() + RIGHT * (c - 0.5) * 0.4 + UP * (r - 0.5) * 0.4)
                draft_cores.add(core)

        # Tạo mô hình chính Target Model (Màu xanh dương, lớn bên phải)
        target_box = RoundedRectangle(width=3.6, height=2.6, color=BLUE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        target_box.move_to(RIGHT * 3.5 + DOWN * 0.8)
        target_lbl = create_markup_text("<b>Target Model</b>\n<span foreground=\"#33AAFF\">Mô hình Đích (70B)</span>", font_size=10, color=BLUE, line_spacing=1.2).next_to(target_box, UP, buff=0.15)

        # Vẽ các lõi tính toán trong Target Model (nhiều và to hơn)
        target_cores = VGroup()
        for r in range(4):
            for c in range(4):
                core = Square(side_length=0.22, color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=0.8)
                core.move_to(target_box.get_center() + RIGHT * (c - 1.5) * 0.45 + UP * (r - 1.5) * 0.42)
                target_cores.add(core)

        self.play(
            FadeIn(draft_box), FadeIn(draft_lbl), FadeIn(draft_cores),
            FadeIn(target_box), FadeIn(target_lbl), FadeIn(target_cores),
            run_time=1.8
        )
        self.wait(10.0)

        # Minh họa việc truyền dữ liệu tải trọng số từ VRAM (Giả định VRAM ở ngoài màn hình)
        # Draft model nạp siêu nhanh
        draft_packets = VGroup(*[
            Dot(color=ORANGE, radius=0.06).move_to(draft_box.get_center() + LEFT * 3 + UP * 2)
            for _ in range(4)
        ])
        
        # Target model nạp rất chậm
        target_packets = VGroup(*[
            Rectangle(width=0.4, height=0.25, color=BLUE_A, fill_color=BLUE, fill_opacity=0.8, stroke_width=1).move_to(target_box.get_center() + RIGHT * 3 + UP * 2)
            for _ in range(4)
        ])

        # Chạy hoạt ảnh nạp bộ nhớ song song
        self.play(
            LaggedStart(
                *[p.animate(run_time=0.8, rate_func=smooth).move_to(draft_box.get_center()) for p in draft_packets],
                lag_ratio=0.15
            ),
            LaggedStart(
                *[p.animate(run_time=3.5, rate_func=linear).move_to(target_box.get_center()) for p in target_packets],
                lag_ratio=0.6
            ),
            run_time=4.0
        )

        # Draft cores phát sáng nhấp nháy nhanh biểu thị nạp xong hoạt động liền
        self.play(
            *[c.animate(run_time=0.3).set_fill(ORANGE, opacity=0.8) for c in draft_cores]
        )
        self.play(
            *[c.animate(run_time=0.3).set_fill(ORANGE, opacity=0.15) for c in draft_cores],
            FadeOut(draft_packets)
        )
        
        # Target cores sáng nhấp nháy chậm hơn biểu thị nạp weights nặng nề
        self.play(
            *[c.animate(run_time=0.5).set_fill(BLUE, opacity=0.8) for c in target_cores]
        )
        self.play(
            *[c.animate(run_time=0.5).set_fill(BLUE, opacity=0.15) for c in target_cores],
            FadeOut(target_packets)
        )
        self.wait(35.0)

        # Dọn dẹp sơ đồ giới thiệu để chuẩn bị sang mô phỏng băng chuyền
        self.play(
            FadeOut(intro_text),
            FadeOut(draft_box), FadeOut(draft_lbl), FadeOut(draft_cores),
            FadeOut(target_box), FadeOut(target_lbl), FadeOut(target_cores),
            run_time=1.0
        )
        self.wait(2.0)

        # =====================================================================
        # BƯỚC 3: BĂNG CHUYỀN DRAFT GENERATION (K = 5)
        # =====================================================================
        draft_gen_text = create_markup_text(
            "<b>Bước 1: Sinh chuỗi nháp (Draft Generation, K = 5)</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(draft_gen_text), run_time=1.5)
        self.wait(25.0)

        # Vẽ băng chuyền (conveyor belt) ở giữa màn hình
        belt_line = Line(start=LEFT * 5.0 + DOWN * 0.8, end=RIGHT * 5.0 + DOWN * 0.8, color=GRAY_D, stroke_width=4)
        belt_roller_left = Dot(LEFT * 5.0 + DOWN * 0.8, color=GRAY_B, radius=0.12)
        belt_roller_right = Dot(RIGHT * 5.0 + DOWN * 0.8, color=GRAY_B, radius=0.12)
        conveyor_belt = VGroup(belt_line, belt_roller_left, belt_roller_right)

        # Hiện lại Draft Model thu nhỏ ở góc trái phía trên để chỉ ra nguồn phát sinh token
        draft_model_mini = RoundedRectangle(width=1.5, height=1.0, color=ORANGE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        draft_model_mini.move_to(LEFT * 4.0 + UP * 0.6)
        draft_model_lbl = create_text("Draft Model", font_size=8, color=ORANGE).move_to(draft_model_mini.get_center())
        draft_mini = VGroup(draft_model_mini, draft_model_lbl)

        self.play(
            Create(conveyor_belt),
            FadeIn(draft_mini),
            run_time=1.2
        )
        self.wait(5.0)

        # Sinh nhanh 5 token đặt trên băng chuyền từ trái sang phải
        tokens_content = ["Hôm", "nay", "trời", "rất", "nắng"]
        token_boxes = VGroup()
        token_lbls = VGroup()

        # Tạo hiệu ứng nhả token từ Draft Model rơi xuống băng chuyền và chạy sang phải
        for i, tok_text in enumerate(tokens_content):
            # Tạo hộp token màu cam nhạt
            tok_box = RoundedRectangle(width=1.0, height=0.55, color=ORANGE, fill_color="#2b2014", fill_opacity=0.9, corner_radius=0.04)
            tok_box.move_to(draft_model_mini.get_center())
            
            tok_lbl = create_text(tok_text, font_size=10, color=WHITE).move_to(tok_box.get_center())
            token_boxes.add(tok_box)
            token_lbls.add(tok_lbl)

            dest_x = -3.2 + i * 1.6
            dest_pos = np.array([dest_x, -0.8, 0])

            # Chạy hoạt ảnh nhả token
            self.play(
                # Sáng nhẹ Draft model mini
                draft_model_mini.animate(run_time=0.15).set_color(YELLOW),
                FadeIn(tok_box), FadeIn(tok_lbl),
                run_time=0.25
            )
            self.play(
                draft_model_mini.animate(run_time=0.1).set_color(ORANGE),
                VGroup(tok_box, tok_lbl).animate(run_time=0.6, rate_func=smooth).move_to(dest_pos),
                run_time=0.6
            )
            self.wait(0.2)

        self.wait(35.0)

        # Dọn dẹp để chuẩn bị sang phần Target Verification
        self.play(
            FadeOut(draft_gen_text),
            run_time=0.8
        )
        self.wait(1.0)

        # =====================================================================
        # BƯỚC 4: KIỂM TRA SONG SONG (TARGET VERIFICATION)
        # =====================================================================
        verify_text = create_markup_text(
            "<b>Bước 2: Phê duyệt song song (Parallel Verification)</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(verify_text), run_time=1.5)
        self.wait(25.0)

        # Hiện Target Model lớn ở góc phải phía trên
        target_model_mini = RoundedRectangle(width=2.0, height=1.3, color=BLUE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        target_model_mini.move_to(RIGHT * 3.5 + UP * 0.6)
        target_model_lbl = create_text("Target Model", font_size=9, color=BLUE).move_to(target_model_mini.get_center())
        
        # Vẽ lõi tính toán bên trong Target Model mini
        target_mini_cores = VGroup()
        for r in range(2):
            for c in range(3):
                core = Square(side_length=0.18, color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=0.6)
                core.move_to(target_model_mini.get_center() + RIGHT * (c - 1.0) * 0.35 + UP * (r - 0.5) * 0.35)
                target_mini_cores.add(core)
        
        target_mini_group = VGroup(target_model_mini, target_model_lbl, target_mini_cores)

        self.play(
            FadeIn(target_mini_group),
            run_time=1.0
        )
        self.wait(5.0)

        # Hoạt ảnh cả 5 token nháp trên băng chuyền đồng loạt bắn luồng dữ liệu lên Target Model
        verify_lines = VGroup()
        for i in range(5):
            start_p = token_boxes[i].get_top()
            end_p = target_model_mini.get_bottom()
            line = Line(start=start_p, end=end_p, color=BLUE_A, stroke_width=1.5).set_opacity(0.6)
            verify_lines.add(line)

        # Tạo hiệu ứng luồng hạt sáng chạy từ các token lên Target Model
        particles = VGroup()
        for line in verify_lines:
            p = Dot(color=YELLOW, radius=0.05).move_to(line.get_start())
            particles.add(p)

        self.play(
            Create(verify_lines),
            FadeIn(particles),
            run_time=0.6
        )

        # Các hạt sáng bay đồng loạt lên mô hình lớn
        self.play(
            *[p.animate(run_time=1.2, rate_func=smooth).move_to(line.get_end()) for p, line in zip(particles, verify_lines)],
        )

        # Target Model phát sáng rực rỡ thể hiện hoạt động hết công suất (Compute-bound)
        self.play(
            *[c.animate(run_time=0.4).set_fill(ORANGE, opacity=0.9).set_color(ORANGE) for c in target_mini_cores],
            FadeOut(particles),
            FadeOut(verify_lines),
            run_time=0.8
        )
        self.wait(10.0)

        # Trả lại trạng thái bình thường cho Target Model
        self.play(
            *[c.animate(run_time=0.5).set_fill(BLUE, opacity=0.15).set_color(BLUE) for c in target_mini_cores],
            run_time=0.8
        )
        self.wait(25.0)

        # Dọn dẹp để chuẩn bị sang toán học của Rejection Sampling
        self.play(
            FadeOut(verify_text),
            FadeOut(target_mini_group),
            FadeOut(draft_mini),
            FadeOut(conveyor_belt),
            FadeOut(token_boxes), FadeOut(token_lbls),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # BƯỚC 5: THUẬT TOÁN CHẤP NHẬN / TỪ CHỐI (REJECTION SAMPLING)
        # =====================================================================
        math_intro = create_markup_text(
            "<b>Lấy mẫu loại bỏ (Rejection Sampling)</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.1)
        self.play(Write(math_intro), run_time=1.5)
        self.wait(25.0)

        # Hiển thị công thức Speculative Sampling (Xây dựng đúng định dạng toán học)
        formula_box = RoundedRectangle(width=8.4, height=0.85, color=GOLD_A, fill_color="#1a1814", fill_opacity=0.9, corner_radius=0.06)
        formula_box.move_to(UP * 1.1)

        left_part = create_markup_text(
            "Xác suất chấp nhận:  <i>P</i><sub>chấp nhận</sub>(<i>x</i>)  =  min  (  1  ,",
            font_size=10.5, color=WHITE
        )
        num_txt = create_markup_text("<i>P</i><sub>đích</sub>(<i>x</i>)", font_size=10, color=BLUE_A)
        den_txt = create_markup_text("<i>P</i><sub>nháp</sub>(<i>x</i>)", font_size=10, color=ORANGE)

        frac_width = max(num_txt.width, den_txt.width) + 0.2
        fraction_line = Line(
            start=LEFT * frac_width / 2,
            end=RIGHT * frac_width / 2,
            stroke_width=1.5,
            color=WHITE
        )

        close_paren = create_text(")", font_size=11, color=WHITE)

        # Định vị các phần tử theo trục ngang và dọc một cách chuẩn xác
        left_part.move_to(LEFT * 1.8)
        fraction_line.next_to(left_part, RIGHT, buff=0.18)
        close_paren.next_to(fraction_line, RIGHT, buff=0.18)

        num_txt.next_to(fraction_line, UP, buff=0.06)
        den_txt.next_to(fraction_line, DOWN, buff=0.06)

        formula_txt = VGroup(left_part, fraction_line, num_txt, den_txt, close_paren)
        formula_txt.move_to(formula_box.get_center())

        self.play(
            FadeIn(formula_box),
            Write(formula_txt),
            run_time=1.2
        )
        self.wait(10.0)

        # Biểu đồ so sánh phân phối xác suất tại vị trí thứ 4 (Token "rất") - Đặt bên phải màn hình
        pos4_lbl = create_markup_text(
            "<b>Xét vị trí thứ 4 trên chuỗi nháp:</b>",
            font_size=10, color=WHITE
        ).move_to(LEFT * 3.5 + UP * 0.1)

        # Vẽ biểu đồ cột
        # Draft Model chọn "rất" với xác suất 0.8
        draft_bar_rect = Rectangle(width=1.0, height=2.4, color=ORANGE, fill_color=ORANGE, fill_opacity=0.7)
        # Target Model chọn "rất" với xác suất 0.2
        target_bar_rect = Rectangle(width=1.0, height=0.6, color=BLUE, fill_color=BLUE, fill_opacity=0.7)
        # Target Model chọn "mưa" làm dự đoán tối ưu hơn (0.7)
        target_alt_rect = Rectangle(width=1.0, height=2.1, color=GREEN_C, fill_color=GREEN_C, fill_opacity=0.7)

        # Đặt vị trí các cột trước, căn đáy chung tại baseline_y = -2.6
        baseline_y = -2.6
        draft_bar_rect.move_to(np.array([0.8, baseline_y + 2.4 / 2, 0]))
        target_bar_rect.move_to(np.array([2.2, baseline_y + 0.6 / 2, 0]))
        target_alt_rect.move_to(np.array([3.6, baseline_y + 2.1 / 2, 0]))

        # Vẽ đường kẻ ngang chạm sát phía dưới cùng của các cột
        ground_y = baseline_y - 0.025
        ground_line = Line(
            start=np.array([0.1, ground_y, 0]),
            end=np.array([4.3, ground_y, 0]),
            color=GRAY, stroke_width=2
        )

        draft_bar_lbl = create_text("P_nháp('rất')\n= 0.8", font_size=8, color=ORANGE).next_to(draft_bar_rect, UP, buff=0.1)
        target_bar_lbl = create_text("P_đích('rất')\n= 0.2", font_size=8, color=BLUE).next_to(target_bar_rect, UP, buff=0.1)
        target_alt_lbl = create_text("P_đích('mưa')\n= 0.7", font_size=8, color=GREEN_B).next_to(target_alt_rect, UP, buff=0.1)

        self.play(
            Write(pos4_lbl),
            Create(ground_line),
            FadeIn(draft_bar_rect), FadeIn(draft_bar_lbl),
            FadeIn(target_bar_rect), FadeIn(target_bar_lbl),
            FadeIn(target_alt_rect), FadeIn(target_alt_lbl),
            run_time=1.5
        )
        self.wait(15.0)

        # Giải thích tỷ lệ chấp nhận: P_đích / P_nháp = 0.2 / 0.8 = 25% (đặt bên trái, không chồng lấn)
        explain_box = RoundedRectangle(width=4.0, height=1.0, color=RED, fill_color="#2b1414", fill_opacity=0.9, corner_radius=0.05)
        explain_box.move_to(LEFT * 3.5 + DOWN * 0.8)
        explain_txt = create_markup_text(
            "Tỷ lệ chấp nhận = <sup>0.2</sup>/<sub>0.8</sub> = 25%\n"
            "<span foreground=\"#FF5555\"><b>Nguy cơ từ chối cao (75%)</b></span>",
            font_size=8, color=WHITE, line_spacing=1.2
        ).move_to(explain_box.get_center())

        self.play(
            FadeIn(explain_box),
            Write(explain_txt),
            run_time=1.0
        )
        self.wait(30.0)

        # Từ chối token (đặt dưới explain_box, bên trái màn hình)
        reject_label = create_text("TỪ CHỐI (REJECT)", font_size=12, color=RED, weight=BOLD).move_to(LEFT * 3.5 + DOWN * 1.8)
        self.play(Write(reject_label), run_time=0.8)
        self.wait(15.0)

        # Dọn dẹp để chuẩn bị sang hoạt ảnh cắt laser thực tế
        self.play(
            FadeOut(math_intro),
            FadeOut(formula_box), FadeOut(formula_txt),
            FadeOut(pos4_lbl), FadeOut(ground_line),
            FadeOut(draft_bar_rect), FadeOut(draft_bar_lbl),
            FadeOut(target_bar_rect), FadeOut(target_bar_lbl),
            FadeOut(target_alt_rect), FadeOut(target_alt_lbl),
            FadeOut(explain_box), FadeOut(explain_txt),
            FadeOut(reject_label),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # BƯỚC 6: HIỆU ỨNG LASER CUT & SỬA ĐỔI
        # =====================================================================
        laser_intro = create_markup_text(
            "<b>Bước 3: Cắt tia Laser &amp; Sửa đổi chuỗi</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(laser_intro), run_time=1.5)
        self.wait(25.0)

        # Vẽ lại băng chuyền ở giữa
        self.play(Create(conveyor_belt), run_time=0.8)

        # Vẽ lại 5 token trên băng chuyền
        belt_tokens = VGroup()
        belt_lbls = VGroup()
        for i, tok_text in enumerate(tokens_content):
            dest_x = -3.2 + i * 1.6
            tok_box = RoundedRectangle(width=1.0, height=0.55, color=ORANGE, fill_color="#2b2014", fill_opacity=0.9, corner_radius=0.04)
            tok_box.move_to(np.array([dest_x, -0.8, 0]))
            tok_lbl = create_text(tok_text, font_size=10, color=WHITE).move_to(tok_box.get_center())
            belt_tokens.add(tok_box)
            belt_lbls.add(tok_lbl)

        self.play(
            FadeIn(belt_tokens), FadeIn(belt_lbls),
            run_time=1.0
        )
        self.wait(10.0)

        # Chấp nhận 3 token đầu tiên: chuyển sang màu xanh lá
        self.play(
            *[belt_tokens[i].animate(run_time=0.5).set_color(GREEN).set_fill("#142b1a", opacity=0.9) for i in range(3)],
            *[belt_lbls[i].animate(run_time=0.5).set_color(GREEN_A) for i in range(3)],
        )
        self.wait(5.0)

        # Token thứ 4 và 5 chuyển sang màu đỏ (bị từ chối)
        self.play(
            *[belt_tokens[i].animate(run_time=0.5).set_color(RED).set_fill("#2b1414", opacity=0.9) for i in range(3, 5)],
            *[belt_lbls[i].animate(run_time=0.5).set_color(RED_A) for i in range(3, 5)],
        )
        self.wait(10.0)

        # Vẽ đường tia laser màu đỏ tươi từ trên xuống (cắt ngay trước vị trí thứ 4, X = 1.0)
        laser_beam = Line(start=UP * 1.0 + RIGHT * 0.8, end=DOWN * 2.2 + RIGHT * 0.8, color=RED, stroke_width=6)
        
        # Điểm sáng phát lửa tại giao điểm giữa laser và băng chuyền
        laser_spark = Star(color=YELLOW, fill_color=YELLOW, fill_opacity=1.0, stroke_width=1).scale(0.25).move_to(RIGHT * 0.8 + DOWN * 0.8)

        self.play(
            Create(laser_beam),
            FadeIn(laser_spark),
            run_time=0.3
        )
        # Hiệu ứng tia lửa giật giật nhấp nháy
        self.play(
            laser_spark.animate(run_time=0.25).scale(1.8),
            laser_beam.animate(run_time=0.25).set_color(YELLOW),
        )
        self.play(
            laser_spark.animate(run_time=0.25).scale(0.55),
            laser_beam.animate(run_time=0.25).set_color(RED),
        )
        self.wait(10.0)

        # Hai token bị từ chối sụp đổ và biến mất hoàn toàn
        self.play(
            # Laser cắt đứt
            VGroup(belt_tokens[3], belt_lbls[3]).animate(run_time=0.8, rate_func=smooth).scale(0.1).shift(DOWN * 1.5).set_opacity(0),
            VGroup(belt_tokens[4], belt_lbls[4]).animate(run_time=0.8, rate_func=smooth).scale(0.1).shift(DOWN * 1.5).set_opacity(0),
            FadeOut(laser_beam), FadeOut(laser_spark),
            run_time=0.8
        )
        self.wait(10.0)

        # Chèn chữ "mưa" vào vị trí thứ 4 (màu xanh dương phát sáng)
        corrected_box = RoundedRectangle(width=1.0, height=0.55, color=BLUE, fill_color="#14202b", fill_opacity=0.9, corner_radius=0.04)
        corrected_box.move_to(RIGHT * 1.6 + DOWN * 0.8)
        corrected_lbl = create_text("mưa", font_size=10, color=BLUE_A).move_to(corrected_box.get_center())

        success_arrow = Arrow(start=RIGHT * 1.6 + UP * 0.5, end=RIGHT * 1.6 + DOWN * 0.4, color=BLUE_A, stroke_width=2.5)
        success_lbl = create_text("Sửa đổi thành công!", font_size=8, color=BLUE_B).next_to(success_arrow, UP, buff=0.1)

        self.play(
            FadeIn(corrected_box), FadeIn(corrected_lbl),
            Create(success_arrow), Write(success_lbl),
            run_time=1.2
        )
        self.wait(25.0)

        # Thu được chuỗi token hoàn chỉnh dưới dạng kết quả hiển thị lớn
        final_seq_box = RoundedRectangle(width=6.8, height=0.9, color=GREEN_B, fill_color="#111111", fill_opacity=0.95, corner_radius=0.08)
        final_seq_box.move_to(DOWN * 2.1)
        final_seq_txt = create_text("Kết quả sinh: \"Hôm nay trời mưa\"", font_size=14, color=WHITE).move_to(final_seq_box.get_center())

        self.play(
            FadeIn(final_seq_box),
            Write(final_seq_txt),
            run_time=1.2
        )
        self.wait(10.0)

        # Dọn dẹp hết để sang phần Tốc Độ thực tế và Tổng kết
        self.play(
            FadeOut(laser_intro),
            FadeOut(conveyor_belt),
            *[FadeOut(belt_tokens[i]) for i in range(3)],
            *[FadeOut(belt_lbls[i]) for i in range(3)],
            FadeOut(corrected_box), FadeOut(corrected_lbl),
            FadeOut(success_arrow), FadeOut(success_lbl),
            FadeOut(final_seq_box), FadeOut(final_seq_txt),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # BƯỚC 7: TỐC ĐỘ THỰC TẾ & ĐÁNH ĐỔI
        # =====================================================================
        conclusion_title = create_text("Đánh giá hiệu suất của Giải mã đầu cơ", font_size=13, color=YELLOW)
        conclusion_title.to_edge(UP, buff=0.4)
        self.play(
            ReplacementTransform(sub_title, conclusion_title),
            run_time=1.0
        )
        self.wait(1.0)

        # Tạo bảng so sánh hiệu năng
        comparison_table = VGroup()
        headers = ["Phương pháp giải mã", "Thời gian nạp weights", "Token sinh / 1 lượt chạy", "Hiệu suất tốc độ"]
        header_colors = [WHITE, WHITE, WHITE, GREEN]
        
        # Dòng tiêu đề
        header_group = VGroup()
        for idx, h_text in enumerate(headers):
            cell = RoundedRectangle(width=2.5, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            cell.move_to(LEFT * (2.7 * (1.5 - idx)) + UP * 1.0)
            lbl = create_text(h_text, font_size=8.5, color=header_colors[idx]).move_to(cell.get_center())
            header_group.add(VGroup(cell, lbl))
        comparison_table.add(header_group)

        # 2 dòng dữ liệu so sánh
        table_rows = [
            ("Giải mã Tiêu chuẩn", "Nạp 70B Weights liên tục", "1 Token", "1.0x (Trục cơ sở)"),
            ("Giải mã Đầu cơ", "Nạp 70B Weights 1 lần duy nhất", "4 Token (3 accepted + 1 corrected)", "2.0x - 3.0x Tốc độ")
        ]

        row_y_coords = [0.1, -0.9]
        row_colors = [GRAY, GREEN_B]
        for r_idx, row_data in enumerate(table_rows):
            row_group = VGroup()
            for c_idx, cell_text in enumerate(row_data):
                cell = RoundedRectangle(width=2.5, height=0.8, color=GRAY_E, fill_color="#121315", fill_opacity=0.8, corner_radius=0.04)
                cell.move_to(LEFT * (2.7 * (1.5 - c_idx)) + UP * row_y_coords[r_idx])
                
                t_color = row_colors[r_idx] if c_idx == 3 else WHITE
                lbl = create_text(cell_text, font_size=8.5, color=t_color).move_to(cell.get_center())
                
                row_group.add(VGroup(cell, lbl))
            comparison_table.add(row_group)

        tradeoff_note = create_markup_text(
            "<b>Lưu ý:</b> Nếu mô hình nháp dự đoán sai nhiều, tỷ lệ chấp nhận giảm sút,\n"
            "hiệu suất tốc độ sẽ bị ảnh hưởng do tốn thêm chi phí chạy mô hình nháp vô ích.",
            font_size=9.5, color=WHITE, line_spacing=1.2
        ).move_to(DOWN * 2.1)

        self.play(
            FadeIn(comparison_table),
            Write(tradeoff_note),
            run_time=1.8
        )
        self.wait(15.0)

        # =====================================================================
        # BƯỚC 7.2: ĐÁNH ĐỔI THÔNG LƯỢNG & ĐỘ DÀI NGỮ CẢNH (MAGICDEC)
        # =====================================================================
        magicdec_title = create_text("Thông lượng vs. Độ dài ngữ cảnh (MagicDec)", font_size=13, color=YELLOW)
        magicdec_title.to_edge(UP, buff=0.4)
        
        self.play(
            FadeOut(comparison_table),
            FadeOut(tradeoff_note),
            ReplacementTransform(conclusion_title, magicdec_title),
            run_time=1.0
        )
        self.wait(1.0)

        # Trực quan hóa bằng biểu đồ đường 2D (Axes)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 8, 2],
            x_length=6.5,
            y_length=3.5,
            axis_config={"color": GRAY_C, "stroke_width": 2},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        ).move_to(DOWN * 0.2)

        # Nhãn cho trục
        x_lbl = create_text("Độ dài ngữ cảnh (Context Length)", font_size=8, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.25)
        y_lbl = create_text("Thông lượng (Throughput)", font_size=8, color=GRAY_A).next_to(axes.y_axis, LEFT, buff=0.25).rotate(90 * DEGREES)

        # Curve 1: Standard Decoding (Màu xanh dương)
        std_curve = axes.plot(lambda x: 3.5 - 0.05 * x, x_range=[0, 10], color=BLUE, stroke_width=3)

        # Curve 2: Speculative Decoding (Màu xanh lá)
        spec_curve = axes.plot(lambda x: 1.8 + 1.4 * (x ** 0.5), x_range=[0, 10], color=GREEN, stroke_width=4)

        # Tạo bảng chú thích (Legend) ở góc trên bên trái đồ thị để tránh chồng chéo
        legend_std_line = Line(start=LEFT * 0.2, end=RIGHT * 0.2, color=BLUE, stroke_width=3)
        legend_std_lbl = create_text("Giải mã thường (Standard)", font_size=7, color=BLUE)
        legend_std = VGroup(legend_std_line, legend_std_lbl).arrange(RIGHT, buff=0.12)

        legend_spec_line = Line(start=LEFT * 0.2, end=RIGHT * 0.2, color=GREEN, stroke_width=4)
        legend_spec_lbl = create_text("Giải mã đầu cơ (Speculative)", font_size=7, color=GREEN)
        legend_spec = VGroup(legend_spec_line, legend_spec_lbl).arrange(RIGHT, buff=0.12)

        legend = VGroup(legend_std, legend_spec).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        legend.move_to(axes.c2p(2.2, 6.8))

        # Annotations (Vùng ngữ cảnh ngắn & Ngữ cảnh dài) - Đặt phía ngoài các đường cong
        low_ctx_dot = Dot(axes.c2p(1, 1.8 + 1.4), color=RED, radius=0.06)
        low_ctx_arrow = Arrow(start=axes.c2p(1.0, 1.0), end=axes.c2p(1.0, 2.9), color=RED, stroke_width=2)
        low_ctx_lbl = create_text("Giảm thông lượng\n(do phí Draft)", font_size=6, color=RED).next_to(low_ctx_arrow, DOWN, buff=0.1)

        long_ctx_dot = Dot(axes.c2p(8, 1.8 + 1.4 * (8**0.5)), color=GREEN, radius=0.06)
        long_ctx_arrow = Arrow(start=axes.c2p(8.0, 7.2), end=axes.c2p(8.0, 6.0), color=GREEN, stroke_width=2)
        long_ctx_lbl = create_markup_text("<b>Tăng cả Throughput &amp; Latency\n(MagicDec)</b>", font_size=6, color=GREEN).next_to(long_ctx_arrow, UP, buff=0.1)

        self.play(
            Create(axes),
            Write(x_lbl), Write(y_lbl),
            run_time=1.5
        )
        self.wait(1.0)

        self.play(
            Create(std_curve),
            Create(spec_curve),
            FadeIn(legend),
            run_time=2.0
        )
        self.wait(2.0)

        # Chú thích
        self.play(
            FadeIn(low_ctx_dot),
            Create(low_ctx_arrow),
            Write(low_ctx_lbl),
            run_time=1.0
        )
        self.wait(5.0)

        self.play(
            FadeIn(long_ctx_dot),
            Create(long_ctx_arrow),
            Write(long_ctx_lbl),
            run_time=1.0
        )
        self.wait(20.0)

        # Dọn dẹp đồ thị để chuyển sang phần code mẫu
        self.play(
            FadeOut(axes), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(std_curve), FadeOut(spec_curve), FadeOut(legend),
            FadeOut(low_ctx_dot), FadeOut(low_ctx_arrow), FadeOut(low_ctx_lbl),
            FadeOut(long_ctx_dot), FadeOut(long_ctx_arrow), FadeOut(long_ctx_lbl),
            FadeOut(magicdec_title),
            run_time=1.2
        )
        self.wait(1.0)

        # =====================================================================
        # BƯỚC 8: MÃ NGUỒN THUẬT TOÁN (SLIDE 213-214)
        # =====================================================================
        code_title = create_text("Mã nguồn thuật toán (Slides 213-214)", font_size=13, color=YELLOW)
        code_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(code_title), run_time=0.8)

        # Cửa sổ Code giả lập IDE
        code_window = RoundedRectangle(width=9.0, height=4.2, color=GRAY_A, fill_color="#0d0e11", fill_opacity=0.95, corner_radius=0.08)
        code_window.move_to(DOWN * 0.2)

        # Thanh tiêu đề IDE
        title_bar = Rectangle(width=9.0, height=0.4, color=GRAY_A, fill_color="#1e1f22", fill_opacity=1.0, stroke_width=0.5)
        title_bar.move_to(code_window.get_top() + DOWN * 0.2)
        
        dots = VGroup(*[Dot(radius=0.06, color=c) for c in [RED, YELLOW, GREEN]])
        dots.arrange(RIGHT, buff=0.12).next_to(title_bar.get_left(), RIGHT, buff=0.25)
        file_name = create_text("speculative_decode.py", font_size=8, color=GRAY_A).next_to(dots, RIGHT, buff=0.4)

        # Code text sử dụng markup để làm nổi bật từ khóa
        code_content = create_markup_text(
            "<span foreground=\"#CC7832\">def</span> <span foreground=\"#FFC66D\">speculative_decode</span>(tgt_m, drf_m, tok, inp, max_tok):\n"
            "    gen = inp\n"
            "    <span foreground=\"#CC7832\">while</span> gen.shape[1] &lt; max_len:\n"
            "        <span foreground=\"#808080\"># Sinh chuỗi nháp từ Draft Model</span>\n"
            "        spec_id, spec_lprob = generate(drf_m, tok, gen, spec_size)\n"
            "        <span foreground=\"#808080\"># Phê duyệt song song từ Target Model</span>\n"
            "        tgt_lprob = tgt_m(spec_id)\n"
            "        <span foreground=\"#808080\"># Lấy mẫu loại bỏ (Rejection Sampling)</span>\n"
            "        rejs = compute_ll_rejs(tgt_lprob, spec_lprob)\n"
            "        accepted = spec_id[:, :rejs[0]]\n"
            "        gen = torch.cat([gen, accepted, next_tok])\n"
            "    <span foreground=\"#CC7832\">return</span> gen",
            font_size=9, font="Consolas", color=WHITE, line_spacing=1.3
        ).move_to(code_window.get_center() + DOWN * 0.1)

        self.play(
            FadeIn(code_window), FadeIn(title_bar), FadeIn(dots), FadeIn(file_name),
            Write(code_content),
            run_time=2.0
        )
        self.wait(5.0)

        # Khung highlight chạy qua các phần chính của code
        highlight_box = SurroundingRectangle(code_content, color=GOLD, stroke_width=2, corner_radius=0.04)
        
        self.play(Create(highlight_box), run_time=1.0)
        self.wait(25.0)

        self.play(
            FadeOut(code_window), FadeOut(title_bar), FadeOut(dots), FadeOut(file_name),
            FadeOut(code_content), FadeOut(highlight_box),
            FadeOut(code_title),
            run_time=1.2
        )
        self.wait(2.0)
        self.wait(2.0)
