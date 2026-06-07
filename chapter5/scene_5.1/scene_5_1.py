import os
import tempfile
import numpy as np
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


class Scene5_1(Scene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ CHƯƠNG KẾT LUẬN
        # =====================================================================
        chapter_title = create_text(
            "Kết luận & Phiên thảo luận Panel",
            font_size=22, color=YELLOW
        )
        chapter_sub = create_text(
            "Conclusion & Panel Session (NeurIPS 2024 Tutorial)",
            font_size=14, color=GRAY_A
        )
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        # Đường trang trí phía trên và dưới tiêu đề
        line_top = Line(LEFT * 4, RIGHT * 4, color=YELLOW, stroke_width=1.5).next_to(chapter_header, UP, buff=0.3)
        line_bot = Line(LEFT * 4, RIGHT * 4, color=YELLOW, stroke_width=1.5).next_to(chapter_header, DOWN, buff=0.3)

        self.play(
            Create(line_top), Create(line_bot),
            FadeIn(chapter_header, shift=UP * 0.3),
            run_time=1.5
        )
        self.wait(6.0)

        # Thu nhỏ tiêu đề lên góc trên
        sub_title = create_text(
            "Kết luận & Panel Session",
            font_size=13, color=YELLOW
        )
        sub_title.to_edge(UP, buff=0.4)

        self.play(
            FadeOut(line_top), FadeOut(line_bot),
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # BƯỚC 2: TỔNG KẾT HÀNH TRÌNH 4 CHƯƠNG
        # =====================================================================
        recap_title = create_markup_text(
            '<b>Tổng kết hành trình: 4 Chương chính</b>',
            font_size=12, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(recap_title), run_time=1.0)
        self.wait(1.5)

        # 4 hộp đại diện cho 4 chương
        # Chương 1: Scaling Laws
        ch1_box = RoundedRectangle(width=2.4, height=1.6, color=PURPLE, fill_color="#1a0e2e", fill_opacity=0.9, corner_radius=0.06)
        ch1_box.move_to(LEFT * 3.8 + DOWN * 0.2)
        ch1_icon = create_text("I", font_size=18, color=PURPLE).move_to(ch1_box.get_center() + UP * 0.3)
        ch1_lbl = create_markup_text(
            '<b>Kỷ nguyên mở rộng</b>\n<span foreground="#BB88FF">Scaling Laws</span>\nPre-train / Post-train\nTest-time Compute',
            font_size=5.5, color=WHITE, line_spacing=1.2
        ).move_to(ch1_box.get_center() + DOWN * 0.2)
        ch1_grp = VGroup(ch1_box, ch1_icon, ch1_lbl)

        # Chương 2: Primitive Generators
        ch2_box = RoundedRectangle(width=2.4, height=1.6, color=BLUE, fill_color="#0e1a2e", fill_opacity=0.9, corner_radius=0.06)
        ch2_box.move_to(LEFT * 1.27 + DOWN * 0.2)
        ch2_icon = create_text("II", font_size=18, color=BLUE).move_to(ch2_box.get_center() + UP * 0.3)
        ch2_lbl = create_markup_text(
            '<b>Bộ sinh cơ bản</b>\n<span foreground="#88BBFF">Generators</span>\nGreedy / Beam Search\nSampling / Truncation',
            font_size=5.5, color=WHITE, line_spacing=1.2
        ).move_to(ch2_box.get_center() + DOWN * 0.2)
        ch2_grp = VGroup(ch2_box, ch2_icon, ch2_lbl)

        # Chương 3: Meta-Generation
        ch3_box = RoundedRectangle(width=2.4, height=1.6, color=GREEN, fill_color="#0e2e1a", fill_opacity=0.9, corner_radius=0.06)
        ch3_box.move_to(RIGHT * 1.27 + DOWN * 0.2)
        ch3_icon = create_text("III", font_size=18, color=GREEN).move_to(ch3_box.get_center() + UP * 0.3)
        ch3_lbl = create_markup_text(
            '<b>Điều phối cấp cao</b>\n<span foreground="#88FFBB">Meta-Generation</span>\nBest-of-N / Tree Search\nRefinement / Verifier',
            font_size=5.5, color=WHITE, line_spacing=1.2
        ).move_to(ch3_box.get_center() + DOWN * 0.2)
        ch3_grp = VGroup(ch3_box, ch3_icon, ch3_lbl)

        # Chương 4: Systems Efficiency
        ch4_box = RoundedRectangle(width=2.4, height=1.6, color=ORANGE, fill_color="#2e1a0e", fill_opacity=0.9, corner_radius=0.06)
        ch4_box.move_to(RIGHT * 3.8 + DOWN * 0.2)
        ch4_icon = create_text("IV", font_size=18, color=ORANGE).move_to(ch4_box.get_center() + UP * 0.3)
        ch4_lbl = create_markup_text(
            '<b>Hiệu năng hệ thống</b>\n<span foreground="#FFBB88">Systems Efficiency</span>\nKV Cache / Batching\nPrefix Sharing',
            font_size=5.5, color=WHITE, line_spacing=1.2
        ).move_to(ch4_box.get_center() + DOWN * 0.2)
        ch4_grp = VGroup(ch4_box, ch4_icon, ch4_lbl)

        # Hoạt ảnh lần lượt hiện 4 chương
        self.play(FadeIn(ch1_grp, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(ch2_grp, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(ch3_grp, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(ch4_grp, shift=UP * 0.2), run_time=0.8)
        self.wait(3.0)

        # Mũi tên kết nối 4 chương
        arrow_1_2 = Arrow(ch1_box.get_right(), ch2_box.get_left(), color=GRAY_C, stroke_width=2, buff=0.08)
        arrow_2_3 = Arrow(ch2_box.get_right(), ch3_box.get_left(), color=GRAY_C, stroke_width=2, buff=0.08)
        arrow_3_4 = Arrow(ch3_box.get_right(), ch4_box.get_left(), color=GRAY_C, stroke_width=2, buff=0.08)
        self.play(
            Create(arrow_1_2), Create(arrow_2_3), Create(arrow_3_4),
            run_time=1.0
        )
        self.wait(2.0)

        # Nhãn tổng kết phía dưới
        recap_note = create_markup_text(
            'Từ bộ sinh token cơ bản, đến điều phối Meta-Generation,\n'
            'và cuối cùng là <b>tối ưu phần cứng hệ thống</b> để vận hành hiệu quả.',
            font_size=7.5, color=GRAY_A, line_spacing=1.3
        ).move_to(DOWN * 1.8)
        self.play(Write(recap_note), run_time=1.5)
        self.wait(20.0)

        # Dọn dẹp Bước 2
        chapters_all = VGroup(ch1_grp, ch2_grp, ch3_grp, ch4_grp, arrow_1_2, arrow_2_3, arrow_3_4)
        self.play(
            FadeOut(recap_title), FadeOut(chapters_all), FadeOut(recap_note),
            run_time=1.0
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 3: GIỚI THIỆU PANEL SESSION & CÁC CHUYÊN GIA
        # =====================================================================
        panel_title = create_markup_text(
            '<b>Phiên thảo luận Panel — NeurIPS 2024</b>',
            font_size=12, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(panel_title), run_time=1.2)
        self.wait(2.0)

        # 5 thẻ chuyên gia + 1 điều phối viên
        def make_expert_card(name, org, color, x_pos, y_pos):
            card_bg = RoundedRectangle(
                width=2.0, height=1.05, color=color,
                fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.05
            )
            card_bg.move_to(RIGHT * x_pos + UP * y_pos)
            # Vòng tròn avatar placeholder
            avatar = Circle(radius=0.18, color=color, fill_color=color, fill_opacity=0.25)
            avatar.move_to(card_bg.get_center() + UP * 0.18)
            # Chữ cái đầu tên
            initial = create_text(name[0], font_size=10, color=color).move_to(avatar.get_center())
            name_lbl = create_text(name, font_size=6.5, color=WHITE).move_to(card_bg.get_center() + DOWN * 0.1)
            org_lbl = create_text(org, font_size=5.5, color=color).move_to(card_bg.get_center() + DOWN * 0.3)
            return VGroup(card_bg, avatar, initial, name_lbl, org_lbl)

        expert_noam = make_expert_card("Noam Brown", "OpenAI", "#FF6B6B", -4.0, 0.5)
        expert_nouha = make_expert_card("Nouha Dziri", "AI2", "#6BCB77", -1.6, 0.5)
        expert_jakob = make_expert_card("Jakob Foerster", "Oxford / Meta AI", "#4D96FF", 0.9, 0.5)
        expert_beidi = make_expert_card("Beidi Chen", "CMU", "#FFD93D", 3.5, 0.5)
        expert_rishabh = make_expert_card("Rishabh Agarwal", "DeepMind / McGill", "#C780FF", -2.8, -0.8)
        # Điều phối viên
        moderator = make_expert_card("Ilia Kulikov", "Meta AI (Moderator)", GRAY_A, 0.9, -0.8)

        experts = VGroup(expert_noam, expert_nouha, expert_jakob, expert_beidi, expert_rishabh, moderator)
        self.play(
            LaggedStart(*[FadeIn(e, shift=UP * 0.15) for e in experts], lag_ratio=0.2),
            run_time=2.5
        )
        self.wait(15.0)

        # Dọn dẹp expert cards
        self.play(FadeOut(experts), FadeOut(panel_title), run_time=1.0)
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 4: CÂU HỎI 1 — MÔ HÌNH LỚN HƠN CÓ LOẠI BỎ META-GENERATION?
        # =====================================================================
        q1_title = create_markup_text(
            '<b>Câu hỏi 1: Mô hình lớn hơn có loại bỏ Meta-Generation?</b>',
            font_size=11, color=YELLOW
        ).move_to(UP * 2.3)
        self.play(Write(q1_title), run_time=1.2)
        self.wait(2.0)

        # Câu trả lời từ Nouha Dziri
        dziri_box = RoundedRectangle(width=10.5, height=1.5, color="#6BCB77", fill_color="#0e2e1a", fill_opacity=0.9, corner_radius=0.05)
        dziri_box.move_to(UP * 0.8)
        dziri_name = create_markup_text('<b>Nouha Dziri (AI2):</b>', font_size=8, color="#6BCB77")
        dziri_name.move_to(dziri_box.get_center() + UP * 0.4 + LEFT * 3.5, aligned_edge=LEFT)
        dziri_text = create_markup_text(
            '"Không. Dù mô hình lớn đến đâu vẫn đối mặt 2 giới hạn cốt lõi:\n'
            '<b>1. Snowballing of Error</b> — một lỗi nhỏ ban đầu làm lệch toàn bộ suy luận\n'
            '<b>2. Difficulty of Look-ahead</b> — khó dự đoán hệ quả nhiều bước phía trước"',
            font_size=6.5, color=WHITE, line_spacing=1.25
        ).move_to(dziri_box.get_center() + DOWN * 0.1)
        dziri_grp = VGroup(dziri_box, dziri_name, dziri_text)
        self.play(FadeIn(dziri_grp, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(18.0)

        # Câu trả lời từ Noam Brown
        brown_box = RoundedRectangle(width=10.5, height=1.3, color="#FF6B6B", fill_color="#2e0e0e", fill_opacity=0.9, corner_radius=0.05)
        brown_box.move_to(DOWN * 1.0)
        brown_name = create_markup_text('<b>Noam Brown (OpenAI):</b>', font_size=8, color="#FF6B6B")
        brown_name.move_to(brown_box.get_center() + UP * 0.35 + LEFT * 3.5, aligned_edge=LEFT)
        brown_text = create_markup_text(
            '"Inference compute là <b>ranh giới vô hạn</b>. Hiện ta chỉ tốn &lt;1 xu/câu hỏi.\n'
            'Nhưng bài toán quan trọng nhất nhân loại sẵn sàng trả $1 triệu cho 1 câu trả lời.\n'
            '<span foreground=\"#FF6B6B\">Khoảng cách 8 bậc quy mô = không gian mở rộng khổng lồ.</span>"',
            font_size=6.5, color=WHITE, line_spacing=1.25
        ).move_to(brown_box.get_center() + DOWN * 0.05)
        brown_grp = VGroup(brown_box, brown_name, brown_text)
        self.play(FadeIn(brown_grp, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(22.0)

        # Dọn dẹp Q1
        self.play(FadeOut(q1_title), FadeOut(dziri_grp), FadeOut(brown_grp), run_time=1.0)
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 5: CÂU HỎI 2 — GIỚI HẠN CỦA INFERENCE SCALING
        # =====================================================================
        q2_title = create_markup_text(
            '<b>Câu hỏi 2: Giới hạn của Inference Scaling</b>',
            font_size=11, color=YELLOW
        ).move_to(UP * 2.3)
        self.play(Write(q2_title), run_time=1.2)
        self.wait(2.0)

        # Sơ đồ: Verifiable vs Non-verifiable tasks
        ver_box = RoundedRectangle(width=4.5, height=1.8, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.05)
        ver_box.move_to(LEFT * 2.8 + UP * 0.3)
        ver_title = create_markup_text('<b>Tac vu xac minh duoc</b>', font_size=8, color=GREEN)
        ver_title.move_to(ver_box.get_center() + UP * 0.55)
        ver_items = create_markup_text(
            '* Math / Coding: Verifier ro rang\n'
            '* Inference scaling hieu qua cao\n'
            '* <span foreground="#33FF55">Best-of-N + PRM = tang manh</span>',
            font_size=6, color=WHITE, line_spacing=1.3
        ).move_to(ver_box.get_center() + DOWN * 0.15)
        ver_grp = VGroup(ver_box, ver_title, ver_items)

        nonver_box = RoundedRectangle(width=4.5, height=1.8, color=RED, fill_color="#2b1414", fill_opacity=0.9, corner_radius=0.05)
        nonver_box.move_to(RIGHT * 2.8 + UP * 0.3)
        nonver_title = create_markup_text('<b>Tac vu kho xac minh</b>', font_size=8, color=RED)
        nonver_title.move_to(nonver_box.get_center() + UP * 0.55)
        nonver_items = create_markup_text(
            '* Van ban mo / Sang tao: Khong co verifier\n'
            '* False positive kho phan biet\n'
            '* <span foreground="#FF3333">Scaling bi gioi han boi chat luong verifier</span>',
            font_size=6, color=WHITE, line_spacing=1.3
        ).move_to(nonver_box.get_center() + DOWN * 0.15)
        nonver_grp = VGroup(nonver_box, nonver_title, nonver_items)

        self.play(FadeIn(ver_grp, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(3.0)
        self.play(FadeIn(nonver_grp, shift=LEFT * 0.2), run_time=1.0)
        self.wait(5.0)

        # Quote từ Nouha Dziri về verification
        dziri_q2 = create_markup_text(
            '<b>Nouha Dziri:</b> "Co nhung bai toan ma verification kho hon generation.\n'
            'Vi du: kiem tra chuong trinh an toan voi MOI dau vao kha thi — day la bai toan\n'
            'ma verification thuc su kho hon viec sinh ra chuong trinh ban dau."',
            font_size=6.5, color="#6BCB77", line_spacing=1.25
        ).move_to(DOWN * 1.5)
        self.play(Write(dziri_q2), run_time=1.5)
        self.wait(22.0)

        # Dọn dẹp Q2
        self.play(FadeOut(q2_title), FadeOut(ver_grp), FadeOut(nonver_grp), FadeOut(dziri_q2), run_time=1.0)
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 6: CÂU HỎI 3 — PHẦN CỨNG & TƯƠNG LAI
        # =====================================================================
        q3_title = create_markup_text(
            '<b>Câu hỏi 3: Phần cứng GPU & Tương lai tối ưu hóa suy luận</b>',
            font_size=11, color=YELLOW
        ).move_to(UP * 2.3)
        self.play(Write(q3_title), run_time=1.2)
        self.wait(2.0)

        # Sơ đồ Training vs Inference paradigm shift
        # Thanh cân đối hiện tại
        bar_bg = RoundedRectangle(width=9.0, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
        bar_bg.move_to(UP * 1.0)
        bar_lbl = create_text("Phan bo Compute hien tai", font_size=8, color=GRAY_B).next_to(bar_bg, UP, buff=0.08)

        # Thanh training chiếm 80%
        train_bar = RoundedRectangle(width=7.2, height=0.45, color=PURPLE, fill_color="#2e1a4e", fill_opacity=0.9, corner_radius=0.03)
        train_bar.move_to(bar_bg.get_center() + LEFT * 0.9)
        train_lbl = create_text("Training (phan lon)", font_size=6.5, color=PURPLE_A).move_to(train_bar.get_center())

        infer_bar = RoundedRectangle(width=1.6, height=0.45, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.03)
        infer_bar.move_to(bar_bg.get_center() + RIGHT * 3.7)
        infer_lbl = create_text("Inference", font_size=6.5, color=GREEN_A).move_to(infer_bar.get_center())

        current_bar = VGroup(bar_bg, bar_lbl, train_bar, train_lbl, infer_bar, infer_lbl)
        self.play(FadeIn(current_bar, shift=DOWN * 0.15), run_time=1.2)
        self.wait(4.0)

        # Thanh tương lai: Inference chiếm phần lớn
        bar_bg2 = RoundedRectangle(width=9.0, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
        bar_bg2.move_to(DOWN * 0.2)
        bar_lbl2 = create_text("Xu huong tuong lai", font_size=8, color=GRAY_B).next_to(bar_bg2, UP, buff=0.08)

        train_bar2 = RoundedRectangle(width=2.5, height=0.45, color=PURPLE, fill_color="#2e1a4e", fill_opacity=0.9, corner_radius=0.03)
        train_bar2.move_to(bar_bg2.get_center() + LEFT * 3.25)
        train_lbl2 = create_text("Training", font_size=6.5, color=PURPLE_A).move_to(train_bar2.get_center())

        infer_bar2 = RoundedRectangle(width=6.3, height=0.45, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.03)
        infer_bar2.move_to(bar_bg2.get_center() + RIGHT * 1.35)
        infer_lbl2 = create_text("Inference (phan lon chi phi)", font_size=6.5, color=GREEN_A).move_to(infer_bar2.get_center())

        future_bar = VGroup(bar_bg2, bar_lbl2, train_bar2, train_lbl2, infer_bar2, infer_lbl2)

        # Mũi tên chuyển đổi
        shift_arrow = Arrow(start=bar_bg.get_bottom(), end=bar_bg2.get_top(), color=YELLOW, stroke_width=2.5)
        shift_lbl = create_text("Paradigm Shift", font_size=7, color=YELLOW).next_to(shift_arrow, RIGHT, buff=0.1)

        self.play(Create(shift_arrow), FadeIn(shift_lbl), FadeIn(future_bar, shift=DOWN * 0.15), run_time=1.5)
        self.wait(5.0)

        # Quote từ Noam Brown về phần cứng
        brown_hw = RoundedRectangle(width=10.5, height=1.0, color="#FF6B6B", fill_color="#2e0e0e", fill_opacity=0.9, corner_radius=0.05)
        brown_hw.move_to(DOWN * 1.5)
        brown_hw_text = create_markup_text(
            '<b>Noam Brown (OpenAI):</b> "Phan cung hien tai thiet ke cho Training nang + Inference re.\n'
            'Tuong lai can <b>tai thiet ke phan cung toi uu cho Inference</b> — day la co hoi nghien cuu lon nhat."',
            font_size=6.5, color=WHITE, line_spacing=1.25
        ).move_to(brown_hw.get_center())
        brown_hw_grp = VGroup(brown_hw, brown_hw_text)
        self.play(FadeIn(brown_hw_grp, shift=UP * 0.15), run_time=1.2)
        self.wait(5.0)

        # Quote từ Beidi Chen
        chen_hw = RoundedRectangle(width=10.5, height=1.0, color="#FFD93D", fill_color="#2e2b14", fill_opacity=0.9, corner_radius=0.05)
        chen_hw.move_to(DOWN * 2.65)
        chen_hw_text = create_markup_text(
            '<b>Beidi Chen (CMU):</b> "Test-time scaling cho them mot bac tu do de co-design\n'
            'giua <b>thuat toan + phan cung</b>. Day la ky nguyen thu vi cho algorithm-hardware co-design."',
            font_size=6.5, color=WHITE, line_spacing=1.25
        ).move_to(chen_hw.get_center())
        chen_hw_grp = VGroup(chen_hw, chen_hw_text)
        self.play(FadeIn(chen_hw_grp, shift=UP * 0.15), run_time=1.2)
        self.wait(25.0)

        # Dọn dẹp Q3
        self.play(
            FadeOut(q3_title), FadeOut(current_bar), FadeOut(future_bar),
            FadeOut(shift_arrow), FadeOut(shift_lbl),
            FadeOut(brown_hw_grp), FadeOut(chen_hw_grp),
            run_time=1.0
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 7: THÔNG ĐIỆP KẾT THÚC CHUNG
        # =====================================================================
        # Jakob Foerster quote
        jakob_box = RoundedRectangle(width=10.5, height=1.3, color="#4D96FF", fill_color="#0e1a2e", fill_opacity=0.9, corner_radius=0.05)
        jakob_box.move_to(UP * 1.3)
        jakob_text = create_markup_text(
            '<b>Jakob Foerster (Oxford):</b> "He thong Hybrid (code + trained components) se la tuong lai.\n'
            'Chung ta se <b>tai phat minh toan bo pipeline</b> khi inference tokens >> training tokens."',
            font_size=6.5, color=WHITE, line_spacing=1.25
        ).move_to(jakob_box.get_center())
        jakob_grp = VGroup(jakob_box, jakob_text)
        self.play(FadeIn(jakob_grp, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(12.0)

        # Nouha Dziri kết luận
        dziri_final = RoundedRectangle(width=10.5, height=1.3, color="#6BCB77", fill_color="#0e2e1a", fill_opacity=0.9, corner_radius=0.05)
        dziri_final.move_to(DOWN * 0.3)
        dziri_final_text = create_markup_text(
            '<b>Nouha Dziri (AI2):</b> "Can bang giua Pre-training Compute va Inference Compute\n'
            'la huong di then chot. Mo hinh <b>nho gon + chuyen biet + Meta-Generation</b> = suc manh lon."',
            font_size=6.5, color=WHITE, line_spacing=1.25
        ).move_to(dziri_final.get_center())
        dziri_final_grp = VGroup(dziri_final, dziri_final_text)
        self.play(FadeIn(dziri_final_grp, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(15.0)

        # Dọn dẹp quotes
        self.play(FadeOut(jakob_grp), FadeOut(dziri_final_grp), run_time=1.0)
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 8: THÔNG ĐIỆP CUỐI CÙNG & LỜI CẢM ƠN
        # =====================================================================
        # Hộp thông điệp cuối cùng
        final_box = RoundedRectangle(width=10.0, height=2.0, color=YELLOW, fill_color="#201c14", fill_opacity=0.95, corner_radius=0.08)
        final_box.move_to(UP * 0.3)
        final_msg = create_markup_text(
            '<b>Thong diep cot loi:</b>\n\n'
            '"Tuong lai cua AI khong chi nam o viec xay dung cac mo hinh lon hon,\n'
            'ma nam o viec thiet ke cac <span foreground="#FFDD33">he thong thong minh</span>\n'
            'biet cach <span foreground="#33FF55">suy nghi va phan bo tai nguyen suy luan</span>\n'
            'mot cach toi uu."',
            font_size=8, color=WHITE, line_spacing=1.3
        ).move_to(final_box.get_center())
        final_grp = VGroup(final_box, final_msg)
        self.play(FadeIn(final_grp, shift=UP * 0.3), run_time=1.5)
        self.wait(8.0)

        # Tài liệu tham khảo
        ref_box = RoundedRectangle(width=9.5, height=0.65, color=BLUE, fill_color="#14202b", fill_opacity=0.95, corner_radius=0.04)
        ref_box.move_to(DOWN * 1.6)
        ref_text = create_markup_text(
            '<b>Tai lieu:</b> Survey Paper (TMLR 2024) &amp; Slides/Code:\n'
            '<span foreground="#33CCFF"><b>https://llm-meta-generation.github.io</b></span>',
            font_size=7.5, color=WHITE, line_spacing=1.2
        ).move_to(ref_box.get_center())
        ref_grp = VGroup(ref_box, ref_text)
        self.play(FadeIn(ref_grp, shift=UP * 0.2), run_time=1.0)
        self.wait(5.0)

        # Lời cảm ơn
        thanks = create_text(
            "Cam on cac ban da theo doi!",
            font_size=16, color=YELLOW
        ).move_to(DOWN * 2.6)
        self.play(Write(thanks), run_time=1.0)
        self.wait(15.0)

        # Fade out toàn bộ
        self.play(
            FadeOut(sub_title), FadeOut(final_grp),
            FadeOut(ref_grp), FadeOut(thanks),
            run_time=1.5
        )
        self.wait(2.0)
