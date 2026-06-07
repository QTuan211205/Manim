import os
import tempfile
import math
from manim import *
import numpy as np

# Cấu hình thư mục tạm thời cho text và tex để tránh lỗi phân quyền trên Windows
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

# Hàm hỗ trợ tạo Text đảm bảo không bị lỗi mất dấu tiếng Việt khi hiển thị trên Windows
def create_text(text, font_size=24, font="Arial", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)

# Hàm hỗ trợ tạo MarkupText đảm bảo không bị lỗi mất dấu tiếng Việt khi hiển thị trên Windows
def create_markup_text(text, font_size=24, font="Arial", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)


class Scene2_3(MovingCameraScene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH & LỢI ÍCH CỦA MAP (00:00 - 00:35)
        # =====================================================================
        chapter_title = create_text("Các cạm bẫy của Giải mã MAP", font_size=24, color=RED_A)
        chapter_sub = create_text("(Pitfalls of MAP Decoding)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(3.2)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Cạm bẫy của Tối ưu hóa Xác suất (MAP Pitfalls)", font_size=16, color=RED_B)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            FadeOut(chapter_header, shift=UP * 0.1),
            FadeIn(sub_title, shift=UP * 0.1),
            run_time=1.2
        )
        self.wait(2.2)

        # Trực quan hóa Lợi ích của MAP trước khi nói về Pitfalls
        benefit_title = create_text("Giải mã MAP hoạt động tốt cho các tác vụ khép kín (closed-ended):", font_size=12, color=GRAY_A)
        benefit_title.next_to(sub_title, DOWN, buff=0.4)
        
        box_mt = RoundedRectangle(width=3.5, height=1.1, color=BLUE_D, fill_color="#181a1e", fill_opacity=0.8, corner_radius=0.06)
        txt_mt = create_markup_text(
            "<b>Dịch máy</b>\n(Machine Translation)\n<span color='#888888'>[Freitag &amp; Al-Onaizan, 2017]</span>", 
            font_size=8, color=BLUE_A, line_spacing=0.4
        )
        txt_mt.move_to(box_mt.get_center())
        node_mt = VGroup(box_mt, txt_mt).move_to(LEFT * 2.2 + DOWN * 0.2)

        box_qa = RoundedRectangle(width=3.5, height=1.1, color=BLUE_D, fill_color="#181a1e", fill_opacity=0.8, corner_radius=0.06)
        txt_qa = create_markup_text(
            "<b>Trả lời câu hỏi</b>\n(Question Answering)\n<span color='#888888'>[Shi et al., 2024]</span>", 
            font_size=8, color=BLUE_A, line_spacing=0.4
        )
        txt_qa.move_to(box_qa.get_center())
        node_qa = VGroup(box_qa, txt_qa).move_to(RIGHT * 2.2 + DOWN * 0.2)

        self.play(
            Write(benefit_title),
            FadeIn(node_mt, shift=LEFT * 0.2),
            FadeIn(node_qa, shift=RIGHT * 0.2),
            run_time=1.2
        )
        self.wait(4.5)

        # Dọn dẹp để chuẩn bị cho Overview Slide
        self.play(
            FadeOut(benefit_title),
            FadeOut(node_mt),
            FadeOut(node_qa),
            run_time=1.0
        )
        self.wait(0.5)

        # Overview Slide (Page 43)
        overview_title = create_text("Các cạm bẫy của giải mã MAP:", font_size=14, color=GRAY_A)
        overview_title.next_to(sub_title, DOWN, buff=0.4)

        item1 = create_markup_text("• <b>Bẫy lặp (Repetition traps)</b>", font_size=11, color=RED_B)
        item2 = create_markup_text("• <b>Chuỗi ngắn (Short sequences)</b> <span color='#888888'>[Stahlberg &amp; Byrne, 2019]</span>", font_size=11, color=RED_B)
        item3 = create_markup_text("• <b>Tính không điển hình (Atypicality)</b> <span color='#888888'>[Meister et al., 2022]</span>", font_size=11, color=RED_B)

        overview_list = VGroup(item1, item2, item3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        overview_list.move_to(ORIGIN + DOWN * 0.2)

        self.play(Write(overview_title), run_time=1.0)
        self.wait(0.5)
        
        for item in overview_list:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(1.0)
        self.wait(2.5)

        self.play(
            FadeOut(overview_title),
            FadeOut(overview_list),
            run_time=1.0
        )
        self.wait(0.5)


        # =====================================================================
        # BƯỚC 2: CẠM BẪY 1 - BẪY LẶP (REPETITION TRAPS) (00:35 - 01:25)
        # =====================================================================
        pitfall1_title = create_text("1. Bẫy lặp (Repetition Traps)", font_size=13, color=RED_B)
        pitfall1_title.next_to(sub_title, DOWN, buff=0.25)
        self.play(Write(pitfall1_title), run_time=0.8)

        # Hiển thị ví dụ thực tế GPT-2, Beam size 32 từ slide của tác giả
        gpt_box = RoundedRectangle(
            width=7.5, 
            height=1.6, 
            color=GRAY_D, 
            fill_color="#151518", 
            fill_opacity=0.95, 
            corner_radius=0.08,
            stroke_width=1.5
        )
        gpt_box.move_to(UP * 0.4)
        gpt_lbl = create_text("GPT-2, Beam size = 32:", font_size=8, color=GRAY_A).next_to(gpt_box, UP, buff=0.1, aligned_edge=LEFT)
        
        gpt_text_content = (
            "Taylor Alison Swift (born December 13, 1989) is an American "
            "<span color='#ff5555'><b>singer-songwriter</b></span>, "
            "<span color='#ff5555'><b>singer-songwriter</b></span>, "
            "<span color='#ff5555'><b>songwriter</b></span>, and "
            "<span color='#ff5555'><b>songwriter</b></span>. "
            "She is best known for her work as a "
            "<span color='#ff5555'><b>singer-songwriter</b></span>, "
            "<span color='#ff5555'><b>songwriter-songwriter</b></span>..."
        )
        gpt_text = create_markup_text(
            gpt_text_content, 
            font_size=9, 
            line_spacing=0.45
        )
        gpt_text.move_to(gpt_box.get_center())
        # Căn lề trái văn bản bên trong hộp
        gpt_text.shift(LEFT * (gpt_box.get_width() - gpt_text.get_width()) / 2 + RIGHT * 0.3)

        self.play(
            FadeIn(gpt_box),
            FadeIn(gpt_lbl),
            run_time=0.8
        )
        self.wait(2.2)

        # Mô phỏng hiệu ứng chữ xuất hiện từng cụm và nhấp nháy đỏ ở các cụm lặp
        self.play(Write(gpt_text), run_time=3.5)
        self.wait(3.2)

        # Sơ đồ hóa vòng lặp trạng thái vô hạn (singer-songwriter <-> songwriter)
        node_a = RoundedRectangle(width=2.5, height=0.5, color=RED_B, fill_color="#201010", fill_opacity=0.9, corner_radius=0.05)
        txt_a = create_text("singer-songwriter", font_size=8, color=RED_B)
        txt_a.move_to(node_a.get_center())
        g_a = VGroup(node_a, txt_a).move_to(LEFT * 1.8 + DOWN * 0.9)

        node_b = RoundedRectangle(width=2.0, height=0.5, color=RED_B, fill_color="#201010", fill_opacity=0.9, corner_radius=0.05)
        txt_b = create_text("songwriter", font_size=8, color=RED_B)
        txt_b.move_to(node_b.get_center())
        g_b = VGroup(node_b, txt_b).move_to(RIGHT * 1.8 + DOWN * 0.9)

        # Mũi tên từ A -> B
        arrow_ab = CurvedArrow(g_a.get_right() + UP*0.08, g_b.get_left() + UP*0.08, angle=-PI/4, color=RED_A)
        # Mũi tên ngược từ B -> A
        arrow_ba = CurvedArrow(g_b.get_left() + DOWN*0.08, g_a.get_right() + DOWN*0.08, angle=-PI/4, color=RED_A)
        lbl_loop = create_text("Vòng lặp vô hạn", font_size=8, color=RED_A).next_to(arrow_ba, DOWN, buff=0.1)
        state_diagram = VGroup(g_a, g_b, arrow_ab, arrow_ba, lbl_loop)

        self.play(
            FadeIn(state_diagram),
            run_time=1.0
        )
        self.wait(3.0)

        # Hiện biện pháp khắc phục (Remedies)
        remedy_title = create_text("Biện pháp khắc phục (Remedies):", font_size=9, color=YELLOW).move_to(DOWN * 1.6 + LEFT * 2.2)
        
        box_penalty = RoundedRectangle(width=3.6, height=0.6, color=YELLOW, fill_color="#201a0e", fill_opacity=0.9, corner_radius=0.04)
        txt_penalty = create_text("Hình phạt lặp\n(Repetition Penalty)", font_size=8, color=YELLOW)
        txt_penalty.move_to(box_penalty.get_center())
        node_penalty = VGroup(box_penalty, txt_penalty).move_to(LEFT * 1.9 + DOWN * 2.2)

        box_unlikelihood = RoundedRectangle(width=4.0, height=0.6, color=YELLOW, fill_color="#201a0e", fill_opacity=0.9, corner_radius=0.04)
        txt_unlikelihood = create_markup_text(
            "Huấn luyện phi xác suất (Unlikelihood Training)\n<span color='#aaaaaa'>[Welleck et al., 2020]</span>", 
            font_size=7, color=YELLOW, line_spacing=0.35
        )
        txt_unlikelihood.move_to(box_unlikelihood.get_center())
        node_unlikelihood = VGroup(box_unlikelihood, txt_unlikelihood).move_to(RIGHT * 2.1 + DOWN * 2.2)

        self.play(
            Write(remedy_title),
            FadeIn(node_penalty, shift=UP * 0.15),
            FadeIn(node_unlikelihood, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait(6.0)

        # Dọn dẹp để sang Pitfall 2
        self.play(
            FadeOut(pitfall1_title),
            FadeOut(gpt_box),
            FadeOut(gpt_lbl),
            FadeOut(gpt_text),
            FadeOut(state_diagram),
            FadeOut(remedy_title),
            FadeOut(node_penalty),
            FadeOut(node_unlikelihood),
            run_time=1.0
        )
        self.wait(1.5)


        # =====================================================================
        # BƯỚC 3: CẠM BẪY 2 - XU HƯỚNG CHUỒI NGẮN (SHORT SEQUENCES) (01:25 - 02:20)
        # =====================================================================
        pitfall2_title = create_markup_text("2. Xu hướng Chuỗi ngắn (Short Sequences) <span color='#888888'>[Stahlberg &amp; Byrne, 2019]</span>", font_size=13, color=RED_B)
        pitfall2_title.next_to(sub_title, DOWN, buff=0.25)
        self.play(Write(pitfall2_title), run_time=0.8)

        # Minh họa việc tích xác suất giảm dần một cách đơn điệu khi chuỗi dài ra
        prob_explanation = create_text(
            "Mỗi từ sinh ra làm giảm xác suất tổng thể một cách đơn điệu do tích [0, 1].",
            font_size=11, color=GRAY_A
        )
        prob_explanation.move_to(UP * 1.4)
        self.play(Write(prob_explanation), run_time=1.2)
        self.wait(2.7)

        # Đồ thị suy hao xác suất (Probability Decay Graph) - Vẽ chay trục số
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1, 0.2],
            x_length=6.0,
            y_length=2.2,
            axis_config={"color": GRAY, "stroke_width": 1.5}
        ).move_to(DOWN * 0.3 + LEFT * 0.8)
        
        # Nhãn cho trục đặt phía dưới trục số để tránh đè chữ
        x_label = create_text("Độ dài chuỗi (Length L)", font_size=8, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.45, aligned_edge=RIGHT)
        y_label = axes.get_y_axis_label(create_text("Xác suất p(y)", font_size=8, color=GRAY_A)).shift(LEFT * 0.2)
        
        # Tạo nhãn số trục X thủ công để tránh gọi LaTeX/MathTex
        x_ticks = [0, 2, 4, 6, 8, 10]
        x_labels = VGroup()
        for x in x_ticks:
            lbl = create_text(str(x), font_size=8, color=GRAY_A)
            lbl.next_to(axes.c2p(x, 0), DOWN, buff=0.15)
            x_labels.add(lbl)

        # Tạo nhãn số trục Y thủ công
        y_ticks = [0.0, 0.5, 1.0]
        y_labels = VGroup()
        for y in y_ticks:
            lbl = create_text(f"{y:.1f}" if y > 0 else "0", font_size=8, color=GRAY_A)
            lbl.next_to(axes.c2p(0, y), LEFT, buff=0.15)
            y_labels.add(lbl)

        axes_group = VGroup(axes, x_label, y_label, x_labels, y_labels)

        # Đường cong suy giảm y = 0.8^L
        curve = axes.plot(lambda x: 0.8**x, x_range=[0, 10], color=RED_B, stroke_width=2.5)

        # Điểm chấm động chạy dọc theo đồ thị
        dot_tracker = Dot(color=YELLOW, radius=0.08).move_to(axes.c2p(0, 1))

        self.play(
            Create(axes_group),
            run_time=1.0
        )
        self.play(
            Create(curve),
            MoveAlongPath(dot_tracker, curve),
            run_time=3.5
        )
        self.wait(1.5)

        # Highlight chuỗi ngắn (L = 2) vs chuỗi dài (L = 8)
        dot_short = Dot(color=RED, radius=0.08).move_to(axes.c2p(2, 0.8**2))
        lbl_short = create_markup_text(
            "\"Taylor Swift is &lt;eos&gt;\"\n(L=2, p=0.64)", font_size=7, color=RED
        ).next_to(dot_short, UP, buff=0.15)

        dot_long = Dot(color=GREEN, radius=0.08).move_to(axes.c2p(8, 0.8**8))
        lbl_long = create_markup_text(
            "\"Taylor Swift is an American...\"\n(L=8, p=0.17)", font_size=7, color=GREEN
        ).next_to(dot_long, UR, buff=0.15)

        self.play(
            FadeIn(dot_short),
            Write(lbl_short),
            run_time=0.8
        )
        self.wait(1.2)
        self.play(
            FadeIn(dot_long),
            Write(lbl_long),
            run_time=0.8
        )
        self.wait(4.0)

        # Xóa đồ thị để hiện công thức khắc phục
        self.play(
            FadeOut(prob_explanation),
            FadeOut(axes_group),
            FadeOut(curve),
            FadeOut(dot_tracker),
            FadeOut(dot_short),
            FadeOut(lbl_short),
            FadeOut(dot_long),
            FadeOut(lbl_long),
            run_time=0.8
        )
        self.wait(0.5)

        # Giải thích biện pháp chuẩn hóa độ dài (Length Normalization) từ slide
        norm_title = create_text("Giải pháp: Chuẩn hóa độ dài (Length Normalization)", font_size=11, color=YELLOW)
        norm_title.move_to(UP * 0.8)
        
        # Công thức chuẩn hóa độ dài log-xác suất trung bình
        norm_formula = create_markup_text(
            "<span color='#ffff00'>Score(<i>y</i>)</span> = "
            "<span color='#8fbcbb'>1</span> / <span color='#ebcb8b'>|<i>y</i>|</span>  •  "
            "<span color='#a3be8c'>∑<sub><i>t=1</i></sub><sup><i>T</i></sup> log <i>p</i><sub><i>θ</i></sub>(<i>y</i><sub><i>t</i></sub> | <i>y</i><sub>&lt;<i>t</i></sub>)</span>",
            font_size=16
        )
        norm_formula.move_to(ORIGIN)
        norm_formula_box = RoundedRectangle(
            width=5.8, 
            height=0.7, 
            color=YELLOW, 
            fill_color="#181812", 
            fill_opacity=0.9, 
            corner_radius=0.06
        )
        norm_formula_box.move_to(norm_formula.get_center())
        norm_group = VGroup(norm_formula_box, norm_formula)

        self.play(
            Write(norm_title),
            FadeIn(norm_group, shift=UP * 0.15),
            run_time=1.0
        )
        self.wait(6.0)

        # Dọn dẹp để sang Pitfall 3
        self.play(
            FadeOut(pitfall2_title),
            FadeOut(norm_title),
            FadeOut(norm_group),
            run_time=1.0
        )
        self.wait(1.5)


        # =====================================================================
        # BƯỚC 4: CẠM BẪY 3 - TÍNH KHÔNG ĐIỂN HÌNH (ATYPICALITY) (02:20 - 03:40)
        # =====================================================================
        pitfall3_title = create_markup_text("3. Tính không điển hình (Atypicality) <span color='#888888'>[Meister et al., 2022]</span>", font_size=13, color=RED_B)
        pitfall3_title.next_to(sub_title, DOWN, buff=0.25)
        self.play(Write(pitfall3_title), run_time=0.8)

        # Thí nghiệm tư duy đồng xu lệch của tác giả
        coin_setup = create_text(
            "Biased coin: Pr[ H ] = 0.6, Pr[ T ] = 0.4",
            font_size=12, color=YELLOW
        )
        coin_setup.move_to(UP * 1.2)
        self.play(Write(coin_setup), run_time=1.0)
        self.wait(2.0)

        # Hộp hiển thị kết quả 100 lần tung
        outcome_title = create_text(
            "Most likely outcome from 100 flips is all heads:",
            font_size=11, color=GRAY_A
        )
        outcome_title.move_to(UP * 0.4)
        
        all_heads_seq = create_markup_text(
            "H  H  H  H  H  H  H  H  H  H  ...",
            font_size=16, color=YELLOW
        )
        all_heads_seq.move_to(DOWN * 0.2)
        
        atypical_note = create_markup_text(
            "But this outcome is <span color='#ff5555'><b>atypical</b></span>.",
            font_size=12, color=WHITE
        )
        atypical_note.move_to(DOWN * 0.9)

        analog_note = create_text(
            "Similarly, the most likely generation may also be atypical.",
            font_size=11, color=GRAY_A
        )
        analog_note.move_to(DOWN * 1.6)

        self.play(Write(outcome_title), run_time=0.8)
        self.play(FadeIn(all_heads_seq, shift=DOWN*0.1), run_time=1.0)
        self.wait(2.0)
        self.play(Write(atypical_note), run_time=0.8)
        self.wait(2.0)
        self.play(Write(analog_note), run_time=1.0)
        self.wait(4.0)

        # Dọn dẹp để sang bước tổng kết
        self.play(
            FadeOut(coin_setup),
            FadeOut(outcome_title),
            FadeOut(all_heads_seq),
            FadeOut(atypical_note),
            FadeOut(analog_note),
            FadeOut(pitfall3_title),
            run_time=1.0
        )
        self.wait(1.5)


        # =====================================================================
        # BƯỚC 5: TỔNG KẾT & CHUYỂN TIẾP SANG LẤY MẪU (SAMPLING) (03:40 - 04:15)
        # =====================================================================
        takeaway_title = create_text("Tóm tắt Kết luận từ Tác giả", font_size=15, color=BLUE_B)
        takeaway_title.to_edge(UP, buff=1.0)
        
        takeaway_1 = create_markup_text(
            "• Việc cực đại hóa xác suất đơn thuần (MAP) gây ra các lỗi nghiêm trọng về cấu trúc.",
            font_size=11
        )
        takeaway_2 = create_markup_text(
            "• <b>Giải pháp tối ưu thực tế:</b> Sử dụng MAP xấp xỉ <span color='#888888'>[Meister et al., 2020]</span>\n"
            "  (như chùm hẹp / narrow beam search).",
            font_size=11, line_spacing=0.4
        )
        takeaway_3 = create_markup_text(
            "• <b>Giải pháp cốt lõi để sinh tự nhiên:</b> Chuyển sang phương pháp <b>Lấy mẫu (Sampling)</b>.",
            font_size=11
        )
        
        takeaways = VGroup(takeaway_1, takeaway_2, takeaway_3).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        takeaways.move_to(ORIGIN)

        self.play(Write(takeaway_title), run_time=0.8)
        self.wait(2.7)

        for ta in takeaways:
            self.play(FadeIn(ta, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(4.0)
        self.wait(4.5)

        # FadeOut kết thúc phân cảnh
        self.play(
            FadeOut(takeaway_title),
            FadeOut(takeaways),
            FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(2.2)
