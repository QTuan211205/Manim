import os
import tempfile
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


class Scene2_2(MovingCameraScene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH & MỤC TIÊU MAP (00:00 - 00:30)
        # =====================================================================
        chapter_title = create_text("Tối ưu hóa trong Giải mã", font_size=24, color=BLUE_A)
        chapter_sub = create_text("(Decoding as Optimization)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(3.2)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Tham lam vs. Tìm kiếm chùm (Greedy vs. Beam Search)", font_size=16, color=BLUE_B)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(2.2)

        # Công thức MAP Objective
        map_title = create_text("Mục tiêu cực đại hóa xác suất hậu nghiệm (MAP Objective)", font_size=13, color=GRAY_A)
        map_title.next_to(sub_title, DOWN, buff=0.4)
        
        map_formula = create_markup_text(
            "<span color='#ebcb8b'>argmax<sub><i>x</i></sub></span> "
            "<span color='#8fbcbb'><i>p</i><sub><i>θ</i></sub>(<i>x</i>)</span>",
            font_size=24
        )
        map_formula.move_to(UP * 0.8)
        
        map_box = RoundedRectangle(
            width=3.6, 
            height=0.9, 
            color=BLUE_E, 
            fill_color="#181a1e", 
            fill_opacity=0.8, 
            corner_radius=0.08
        )
        map_box.move_to(map_formula.get_center())
        map_group = VGroup(map_box, map_formula)

        self.play(
            Write(map_title),
            FadeIn(map_group, shift=UP * 0.2),
            run_time=1.2
        )
        self.wait(3.2)

        # Thêm các Brace chú thích
        brace_x = Brace(map_box, DOWN, color=BLUE_C)
        lbl_x = create_text("Chuỗi token đầu ra hoàn chỉnh", font_size=10, color=BLUE_A)
        lbl_x.next_to(brace_x, DOWN, buff=0.1)
        
        self.play(
            Create(brace_x),
            Write(lbl_x),
            run_time=0.8
        )
        self.wait(5.0)

        # Dọn dẹp để sang giải mã Tham lam
        self.play(
            FadeOut(map_title),
            FadeOut(map_group),
            FadeOut(brace_x),
            FadeOut(lbl_x),
            run_time=1.0
        )
        self.wait(1.5)


        # =====================================================================
        # BƯỚC 2: GIẢI MÃ THAM LAM (GREEDY DECODING) & TÍNH CẬN THỊ (01:45 - 03:00)
        # =====================================================================
        greedy_header = create_text("1. Giải mã Tham lam (Greedy Decoding)", font_size=13, color=BLUE_B)
        greedy_header.next_to(sub_title, DOWN, buff=0.3)
        
        # Chú ý: Sử dụng "in V" thay vì symbol "∈" để tránh lỗi Cairo square box
        greedy_formula = create_markup_text(
            "<i>x</i><sub><i>t</i></sub> = "
            "<span color='#ebcb8b'>argmax<sub><i>w in V</i></sub></span> "
            "<i>p</i><sub><i>θ</i></sub>(<i>w</i> | <i>x</i><sub>&lt;<i>t</i></sub>)",
            font_size=20
        )
        greedy_formula.move_to(UP * 1.7)
        greedy_formula_box = RoundedRectangle(width=4.2, height=0.7, color=BLUE_E, fill_color="#121820", fill_opacity=0.9, corner_radius=0.06)
        greedy_formula_box.move_to(greedy_formula.get_center())
        greedy_formula_group = VGroup(greedy_formula_box, greedy_formula)

        self.play(
            Write(greedy_header),
            FadeIn(greedy_formula_group, shift=DOWN * 0.15),
            run_time=1.0
        )
        self.wait(4.0)

        # Phân chia màn hình: Cây ở bên trái, Bảng xác suất bên phải
        divider_line = Line(np.array([1.5, 1.2, 0]), np.array([1.5, -3.2, 0]), color=GRAY, stroke_width=1.5).set_stroke(opacity=0.4)
        self.play(Create(divider_line), run_time=0.6)

        # Cây Quyết Định (Phía trái, dịch chuyển trung tâm sang x = -2.0)
        # Root node
        root_box = RoundedRectangle(width=1.8, height=0.4, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        root_box.move_to(np.array([-2.0, 1.0, 0]))
        root_txt = create_text("Taylor Swift is", font_size=9, color=WHITE)
        root_txt.move_to(root_box.get_center())
        root_node = VGroup(root_box, root_txt)

        self.play(FadeIn(root_node, shift=UP * 0.15), run_time=0.8)
        self.wait(2.2)

        # Định nghĩa hàm helper tạo Sidebar
        def get_sidebar(step_title, candidates, active_idx=0):
            sidebar_group = VGroup()
            title = create_text(step_title, font_size=10, color=BLUE_A)
            sidebar_group.add(title)
            
            rows_group = VGroup()
            for idx, (word, prob) in enumerate(candidates):
                color = YELLOW if idx == active_idx else WHITE
                word_txt = create_text(f'"{word}"', font_size=9, color=color)
                prob_txt = create_text(f"{prob:.3f}", font_size=9, color=color)
                row = VGroup(word_txt, prob_txt).arrange(RIGHT, buff=0.8)
                
                if idx == active_idx:
                    row_bg = RoundedRectangle(width=3.2, height=0.35, color=YELLOW, fill_color=YELLOW, fill_opacity=0.15, stroke_width=1, corner_radius=0.04)
                    row_bg.move_to(row.get_center())
                    row = VGroup(row_bg, row)
                rows_group.add(row)
            
            rows_group.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            sidebar_group.add(rows_group)
            sidebar_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            sidebar_group.move_to(np.array([4.2, 0.5, 0]))
            return sidebar_group

        step1_cands = [("an", 0.80), ("a", 0.13), ("the", 0.06), ("to", 0.0004)]
        sb1 = get_sidebar("Dự đoán Bước 1 (t=1)", step1_cands, active_idx=0)
        self.play(FadeIn(sb1), run_time=0.8)
        self.wait(2.7)

        # Vẽ nhánh "an" trong Cây
        an_box = RoundedRectangle(width=0.6, height=0.4, color=GRAY_B, fill_color="#202022", fill_opacity=0.9, corner_radius=0.04)
        an_box.move_to(np.array([-2.0, 0.0, 0]))
        an_txt = create_text("an", font_size=9, color=WHITE)
        an_txt.move_to(an_box.get_center())
        an_prob = create_text("0.80", font_size=8, color=GRAY_A).next_to(an_box, RIGHT, buff=0.1)
        an_node = VGroup(an_box, an_txt, an_prob)
        line_root_an = Line(root_box.get_bottom(), an_box.get_top(), color=GRAY_C, stroke_width=1.5)

        self.play(
            Create(line_root_an),
            FadeIn(an_node, shift=DOWN * 0.1),
            run_time=0.8
        )
        self.wait(2.7)

        # BƯỚC 2 (t=2)
        step2_cands = [("American", 0.02), ("artist", 0.01)]
        sb2 = get_sidebar("Dự đoán Bước 2 (t=2)", step2_cands, active_idx=0)
        
        self.play(
            FadeOut(sb1),
            FadeIn(sb2),
            run_time=0.8
        )
        self.wait(2.7)

        # Vẽ nhánh "American" (Tham lam)
        american_box = RoundedRectangle(width=1.3, height=0.4, color=BLUE_C, fill_color="#0f1b2b", fill_opacity=0.9, corner_radius=0.04)
        american_box.move_to(np.array([-3.2, -1.0, 0]))
        american_txt = create_text("American", font_size=8, color=WHITE)
        american_txt.move_to(american_box.get_center())
        american_prob = create_text("0.02", font_size=8, color=BLUE_A).next_to(american_box, LEFT, buff=0.05)
        american_node = VGroup(american_box, american_txt, american_prob)
        line_an_american = Line(an_box.get_bottom(), american_box.get_top(), color=BLUE_D, stroke_width=2.5)

        self.play(
            Create(line_an_american),
            FadeIn(american_node, shift=LEFT * 0.1 + DOWN * 0.1),
            run_time=0.8
        )
        self.wait(2.7)

        # BƯỚC 3 (t=3)
        step3_cands = [("singer", 0.05), ("songwriter", 0.01)]
        sb3 = get_sidebar("Dự đoán Bước 3 (t=3)", step3_cands, active_idx=0)

        self.play(
            FadeOut(sb2),
            FadeIn(sb3),
            run_time=0.8
        )
        self.wait(2.7)

        # Vẽ nhánh "singer"
        singer_box = RoundedRectangle(width=0.9, height=0.4, color=BLUE_C, fill_color="#0f1b2b", fill_opacity=0.9, corner_radius=0.04)
        singer_box.move_to(np.array([-3.2, -2.0, 0]))
        singer_txt = create_text("singer", font_size=9, color=WHITE)
        singer_txt.move_to(singer_box.get_center())
        singer_prob = create_text("0.05", font_size=8, color=BLUE_A).next_to(singer_box, LEFT, buff=0.05)
        singer_node = VGroup(singer_box, singer_txt, singer_prob)
        line_american_singer = Line(american_box.get_bottom(), singer_box.get_top(), color=BLUE_D, stroke_width=2.5)

        self.play(
            Create(line_american_singer),
            FadeIn(singer_node, shift=DOWN * 0.1),
            run_time=0.8
        )
        self.wait(2.7)

        # BƯỚC 4 (t=4)
        step4_cands = [("<eos>", 1.0), ("and", 0.0)]
        sb4 = get_sidebar("Dự đoán Bước 4 (t=4)", step4_cands, active_idx=0)

        self.play(
            FadeOut(sb3),
            FadeIn(sb4),
            run_time=0.8
        )
        self.wait(2.7)

        # Vẽ nhánh "<eos>"
        eos_box = RoundedRectangle(width=0.8, height=0.4, color=BLUE_C, fill_color="#0f1b2b", fill_opacity=0.9, corner_radius=0.04)
        eos_box.move_to(np.array([-3.2, -3.0, 0]))
        eos_txt = create_text("<eos>", font_size=9, color=WHITE)
        eos_txt.move_to(eos_box.get_center())
        eos_prob = create_text("1.0", font_size=8, color=BLUE_A).next_to(eos_box, LEFT, buff=0.05)
        eos_node = VGroup(eos_box, eos_txt, eos_prob)
        line_singer_eos = Line(singer_box.get_bottom(), eos_box.get_top(), color=BLUE_D, stroke_width=2.5)

        self.play(
            Create(line_singer_eos),
            FadeIn(eos_node, shift=DOWN * 0.1),
            run_time=0.8
        )
        self.wait(2.7)

        # Tính xác suất tích lũy cho Tham lam
        greedy_cum_label = create_markup_text(
            "<span color='#ff6b6b'><i>p</i><sub>cum</sub> = 8.00 × 10<sup>-4</sup></span>",
            font_size=12
        )
        greedy_cum_label.next_to(eos_box, DOWN, buff=0.15)
        greedy_bad_txt = create_text("Cận thị (Shortsighted)", font_size=10, color="#ff6b6b")
        greedy_bad_txt.next_to(greedy_cum_label, DOWN, buff=0.08)
        greedy_bad_group = VGroup(greedy_cum_label, greedy_bad_txt)
        # Thêm nền bán trong suốt để chữ nổi bật hơn
        greedy_bad_bg = RoundedRectangle(
            width=greedy_bad_group.get_width() + 0.3,
            height=greedy_bad_group.get_height() + 0.15,
            color=RED_E, fill_color="#2c1618", fill_opacity=0.85,
            corner_radius=0.05, stroke_width=1.5
        )
        greedy_bad_bg.move_to(greedy_bad_group.get_center())
        greedy_bad_group = VGroup(greedy_bad_bg, greedy_cum_label, greedy_bad_txt)

        self.play(
            FadeIn(greedy_bad_group, shift=UP * 0.1),
            run_time=0.8
        )
        self.wait(3.2)

        # SO SÁNH VỚI NHÁNH KHÔNG THAM LAM (singer)
        self.play(FadeOut(sb4), run_time=0.4)
        
        # Vẽ nhánh "a"
        a_box = RoundedRectangle(width=0.6, height=0.4, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
        a_box.move_to(np.array([-0.8, 0.0, 0]))
        a_txt = create_text("a", font_size=9, color=WHITE)
        a_txt.move_to(a_box.get_center())
        a_prob = create_text("0.13", font_size=8, color=GRAY_A).next_to(a_box, RIGHT, buff=0.05)
        a_node = VGroup(a_box, a_txt, a_prob)
        line_root_a = Line(root_box.get_bottom(), a_box.get_top(), color=GRAY_C, stroke_width=1.5)

        self.play(
            Create(line_root_a),
            FadeIn(a_node, shift=RIGHT * 0.1 + DOWN * 0.1),
            run_time=0.8
        )
        self.wait(2.7)

        # Vẽ nhánh "singer"
        singer_non_box = RoundedRectangle(width=0.9, height=0.4, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
        singer_non_box.move_to(np.array([-0.8, -1.0, 0]))
        singer_non_txt = create_text("singer", font_size=9, color=WHITE)
        singer_non_txt.move_to(singer_non_box.get_center())
        singer_non_prob = create_text("0.90", font_size=8, color=GRAY_A).next_to(singer_non_box, RIGHT, buff=0.05)
        singer_non_node = VGroup(singer_non_box, singer_non_txt, singer_non_prob)
        line_a_singer_non = Line(a_box.get_bottom(), singer_non_box.get_top(), color=GRAY_C, stroke_width=1.5)

        self.play(
            Create(line_a_singer_non),
            FadeIn(singer_non_node, shift=RIGHT * 0.1 + DOWN * 0.1),
            run_time=0.8
        )
        self.wait(2.7)

        # Phân phối tiếp của "singer": "," (0.26)
        comma_box = RoundedRectangle(width=0.5, height=0.4, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
        comma_box.move_to(np.array([-0.8, -2.0, 0]))
        comma_txt = create_text(",", font_size=9, color=WHITE)
        comma_txt.move_to(comma_box.get_center())
        comma_prob = create_text("0.26", font_size=8, color=GRAY_A).next_to(comma_box, RIGHT, buff=0.05)
        comma_node = VGroup(comma_box, comma_txt, comma_prob)
        line_singer_comma = Line(singer_non_box.get_bottom(), comma_box.get_top(), color=GRAY_C, stroke_width=1.5)

        self.play(
            Create(line_singer_comma),
            FadeIn(comma_node, shift=DOWN * 0.1),
            run_time=0.8
        )
        self.wait(2.7)

        # Phân phối tiếp của ",": "songwriter" (0.80)
        songwriter_box = RoundedRectangle(width=1.3, height=0.4, color=GREEN_C, fill_color="#0e2316", fill_opacity=0.9, corner_radius=0.04)
        songwriter_box.move_to(np.array([-0.8, -3.0, 0]))
        songwriter_txt = create_text("songwriter", font_size=8, color=WHITE)
        songwriter_txt.move_to(songwriter_box.get_center())
        songwriter_prob = create_text("0.80", font_size=8, color=GREEN_A).next_to(songwriter_box, RIGHT, buff=0.05)
        songwriter_node = VGroup(songwriter_box, songwriter_txt, songwriter_prob)
        line_comma_songwriter = Line(comma_box.get_bottom(), songwriter_box.get_top(), color=GREEN_D, stroke_width=2.5)

        self.play(
            Create(line_comma_songwriter),
            FadeIn(songwriter_node, shift=DOWN * 0.1),
            run_time=0.8
        )
        self.wait(2.7)

        # Tính xác suất tích lũy cho Non-greedy
        nongreedy_cum_label = create_markup_text(
            "<span color='#2ecc71'><i>p</i><sub>cum</sub> = 2.43 × 10<sup>-2</sup></span>",
            font_size=12
        )
        nongreedy_cum_label.next_to(songwriter_box, DOWN, buff=0.15)
        # Thêm nền bán trong suốt để chữ nổi bật hơn
        nongreedy_cum_bg = RoundedRectangle(
            width=nongreedy_cum_label.get_width() + 0.3,
            height=nongreedy_cum_label.get_height() + 0.15,
            color=GREEN_E, fill_color="#0e2316", fill_opacity=0.85,
            corner_radius=0.05, stroke_width=1.5
        )
        nongreedy_cum_bg.move_to(nongreedy_cum_label.get_center())
        
        self.play(
            FadeIn(nongreedy_cum_bg),
            Write(nongreedy_cum_label),
            run_time=0.8
        )
        self.wait(3.2)

        # So sánh 2 nhánh
        vs_label = create_text("Cao hơn 30 lần!", font_size=14, color="#2ecc71")
        vs_label.move_to(np.array([4.0, -0.5, 0]))
        vs_label_bg = RoundedRectangle(
            width=vs_label.get_width() + 0.4,
            height=vs_label.get_height() + 0.25,
            color=GREEN, fill_color="#0e2316", fill_opacity=0.9,
            corner_radius=0.06, stroke_width=2
        )
        vs_label_bg.move_to(vs_label.get_center())
        vs_label = VGroup(vs_label_bg, vs_label)
        
        self.play(
            Write(vs_label),
            nongreedy_cum_label.animate.scale(1.2),
            songwriter_box.animate.set_color(GREEN).set_stroke(width=3),
            an_box.animate.set_color(RED).set_stroke(width=2),
            american_box.animate.set_color(RED_D),
            singer_box.animate.set_color(RED_D),
            eos_box.animate.set_color(RED_D),
            run_time=1.2
        )
        self.wait(5.5)

        # Dọn dẹp chuẩn bị phần Beam Search
        self.play(
            FadeOut(greedy_header),
            FadeOut(greedy_formula_group),
            FadeOut(divider_line),
            FadeOut(root_node),
            FadeOut(line_root_an),
            FadeOut(an_node),
            FadeOut(line_an_american),
            FadeOut(american_node),
            FadeOut(line_american_singer),
            FadeOut(singer_node),
            FadeOut(line_singer_eos),
            FadeOut(eos_node),
            FadeOut(greedy_bad_group),
            FadeOut(line_root_a),
            FadeOut(a_node),
            FadeOut(line_a_singer_non),
            FadeOut(singer_non_node),
            FadeOut(line_singer_comma),
            FadeOut(comma_node),
            FadeOut(line_comma_songwriter),
            FadeOut(songwriter_node),
            FadeOut(nongreedy_cum_label),
            FadeOut(nongreedy_cum_bg),
            FadeOut(vs_label),
            run_time=1.2
        )
        self.wait(1.5)


        # =====================================================================
        # BƯỚC 3: THUẬT TOÁN TÌM KIẾM CHÙM (BEAM SEARCH, K=2) (03:00 - 04:30)
        # =====================================================================
        beam_header = create_text("2. Tìm kiếm Chùm (Beam Search, K = 2)", font_size=13, color=YELLOW)
        beam_header.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(beam_header), run_time=0.8)

        # Divider line
        divider_line_bs = Line(np.array([1.5, 1.2, 0]), np.array([1.5, -3.2, 0]), color=GRAY, stroke_width=1.5).set_stroke(opacity=0.4)
        self.play(Create(divider_line_bs), run_time=0.6)

        # Config box/card at bottom-left
        config_box = RoundedRectangle(width=4.0, height=1.1, color=BLUE_E, fill_color="#181a1e", fill_opacity=0.85, corner_radius=0.06, stroke_width=1.5)
        config_box.move_to(np.array([-2.75, -2.6, 0]))
        
        lbl_gpt2 = create_text("Cấu hình: GPT2, beam size 2 (K = 2)", font_size=9, color=BLUE_A)
        lbl_bfs = create_text("Thuật toán: width-limited BFS", font_size=9, color=BLUE_A)
        lbl_greedy_note = create_text("Ghi chú: Beam size 1 là Greedy decoding", font_size=8, color=GRAY_A)
        
        config_texts = VGroup(lbl_gpt2, lbl_bfs, lbl_greedy_note).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        config_texts.move_to(config_box.get_center())
        config_group = VGroup(config_box, config_texts)
        
        self.play(FadeIn(config_group, shift=UP * 0.15), run_time=0.8)

        # Root node (Dịch chuyển trung tâm sang trái x = -2.75)
        bs_root_box = RoundedRectangle(width=1.8, height=0.4, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        bs_root_box.move_to(np.array([-2.75, 2.6, 0]))
        bs_root_txt = create_text("Taylor Swift is", font_size=9, color=WHITE)
        bs_root_txt.move_to(bs_root_box.get_center())
        bs_root_node = VGroup(bs_root_box, bs_root_txt)
        
        self.play(FadeIn(bs_root_node, shift=UP * 0.1), run_time=0.8)
        self.wait(2.7)

        # Hàm helper tạo Queue xếp hạng ứng viên ở Sidebar (Đã sửa lỗi đè chữ)
        def get_queue_sidebar(step_title, candidates, active_k=2):
            sidebar_group = VGroup()
            title = create_text(step_title, font_size=10, color=YELLOW)
            sidebar_group.add(title)
            
            content_group = VGroup()
            for idx, (path_name, score) in enumerate(candidates):
                color = YELLOW if idx < active_k else GRAY_B
                path_txt = create_text(f'"{path_name}"', font_size=8, color=color)
                score_txt = create_text(f"{score:.4f}", font_size=8, color=color)
                row = VGroup(path_txt, score_txt).arrange(RIGHT, buff=0.4)
                
                # Vẽ khung chùm cho các ứng viên được chọn
                if idx < active_k:
                    row_bg = RoundedRectangle(width=3.4, height=0.35, color=YELLOW, fill_color=YELLOW, fill_opacity=0.08, stroke_width=1, corner_radius=0.04)
                    row_bg.move_to(row.get_center())
                    row = VGroup(row_bg, row)
                
                # Chèn đường cắt tỉa (pruning line) ngay giữa phần được chọn (active) và bị loại
                if idx == active_k:
                    prune_line = Line(LEFT * 1.7, RIGHT * 1.7, color=RED, stroke_width=1.5).set_stroke(opacity=0.7)
                    prune_lbl = create_text("Cắt tỉa (Pruned) > K", font_size=7, color=RED)
                    prune_lbl.next_to(prune_line, RIGHT, buff=0.1)
                    prune_group = VGroup(prune_line, prune_lbl)
                    content_group.add(prune_group)
                
                content_group.add(row)
            
            content_group.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            content_group.next_to(title, DOWN, buff=0.3)
            sidebar_group.add(content_group)
            sidebar_group.move_to(np.array([4.2, -0.6, 0]))
            return sidebar_group

        # BƯỚC 1 (t=1): Mở rộng 4 nhánh con
        # Khởi tạo các Node
        bs_nodes_t1 = []
        bs_lines_t1 = []
        labels_t1 = ["an", "a", "the", "to"]
        probs_t1 = [0.80, 0.13, 0.06, 0.0004]
        x_coords_t1 = [-5.0, -3.5, -2.0, -0.5]
        
        for idx, (label, p, x_val) in enumerate(zip(labels_t1, probs_t1, x_coords_t1)):
            color = YELLOW if idx < 2 else GRAY_C
            box = RoundedRectangle(width=0.6 if len(label)<3 else 0.8, height=0.4, color=color, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            box.move_to(np.array([x_val, 1.2, 0]))
            txt = create_text(label, font_size=9, color=WHITE)
            txt.move_to(box.get_center())
            p_lbl = create_text(f"{p}", font_size=8, color=color).next_to(box, DOWN, buff=0.05)
            
            node_grp = VGroup(box, txt, p_lbl)
            line = Line(bs_root_box.get_bottom(), box.get_top(), color=color, stroke_width=2.5 if idx<2 else 1.5)
            
            bs_nodes_t1.append(node_grp)
            bs_lines_t1.append(line)

        # Sidebar xếp hạng bước 1
        bs_q1 = get_queue_sidebar("Hàng đợi Bước 1 (t=1)", [("an", 0.80), ("a", 0.13), ("the", 0.06), ("to", 0.0004)])
        
        self.play(
            LaggedStart(*[Create(l) for l in bs_lines_t1], lag_ratio=0.1),
            LaggedStart(*[FadeIn(n, shift=DOWN*0.1) for n in bs_nodes_t1], lag_ratio=0.1),
            FadeIn(bs_q1),
            run_time=1.5
        )
        self.wait(3.2)

        # Vẽ Hộp Chùm bao quanh "an" và "a" ở cây
        beam_box_1 = RoundedRectangle(
            width=2.5, 
            height=1.0, 
            color=YELLOW, 
            fill_color=YELLOW, 
            fill_opacity=0.05, 
            stroke_width=2, 
            corner_radius=0.08
        )
        beam_box_1.move_to(np.array([-4.25, 1.05, 0]))
        lbl_beam_1 = create_text("Chùm K=2", font_size=8, color=YELLOW).next_to(beam_box_1, UP, buff=0.05)

        self.play(
            Create(beam_box_1),
            Write(lbl_beam_1),
            run_time=0.8
        )
        self.wait(2.7)

        # Cắt tỉa nhánh "the" và "to" (mờ đi)
        self.play(
            bs_nodes_t1[2].animate.set_opacity(0.15),
            bs_nodes_t1[3].animate.set_opacity(0.15),
            bs_lines_t1[2].animate.set_opacity(0.15),
            bs_lines_t1[3].animate.set_opacity(0.15),
            run_time=0.8
        )
        self.wait(3.2)

        # BƯỚC 2 (t=2): Mở rộng 2 chùm active thành 4 nhánh con
        # 1. "an" -> "American" (0.80*0.02 = 0.016), "artist" (0.80*0.01 = 0.008)
        # 2. "a" -> "singer" (0.13*0.90 = 0.117), "songwriter" (0.13*0.80 = 0.104)
        bs_nodes_t2 = []
        bs_lines_t2 = []
        labels_t2 = [("American", 0.02, 0.016), ("artist", 0.01, 0.008), ("singer", 0.90, 0.117), ("songwriter", 0.80, 0.104)]
        x_coords_t2 = [-5.75, -4.55, -3.35, -2.15]
        parent_indices = [0, 0, 1, 1] # Chỉ số của node cha trong bs_nodes_t1

        for idx, ((lbl, p_trans, p_cum), x_val, p_idx) in enumerate(zip(labels_t2, x_coords_t2, parent_indices)):
            color = YELLOW if idx >= 2 else GRAY_C  # singer và songwriter (idx=2,3) là chùm được giữ lại
            box = RoundedRectangle(width=0.8 if len(lbl)<6 else 1.1, height=0.4, color=color, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            box.move_to(np.array([x_val, -0.2, 0]))
            txt = create_text(lbl, font_size=8, color=WHITE)
            txt.move_to(box.get_center())
            p_lbl = create_markup_text(f"<i>p</i><sub>cum</sub> = {p_cum:.3f}", font_size=7, color=color).next_to(box, DOWN, buff=0.05)
            
            node_grp = VGroup(box, txt, p_lbl)
            line = Line(bs_nodes_t1[p_idx][0].get_bottom(), box.get_top(), color=color, stroke_width=2.0 if idx>=2 else 1.2)
            
            bs_nodes_t2.append(node_grp)
            bs_lines_t2.append(line)

        # Sidebar xếp hạng bước 2
        bs_q2 = get_queue_sidebar(
            "Hàng đợi Bước 2 (t=2)", 
            [("a singer", 0.1170), ("a songwriter", 0.1040), ("an American", 0.0160), ("an artist", 0.0080)]
        )

        self.play(
            FadeOut(bs_q1),
            FadeIn(bs_q2),
            LaggedStart(*[Create(l) for l in bs_lines_t2], lag_ratio=0.08),
            LaggedStart(*[FadeIn(n, shift=DOWN*0.1) for n in bs_nodes_t2], lag_ratio=0.08),
            run_time=1.5
        )
        self.wait(4.0)

        # Di chuyển hộp chùm sang phía bên phải Level 2 (singer và songwriter)
        beam_box_2 = RoundedRectangle(
            width=2.6, 
            height=1.1, 
            color=YELLOW, 
            fill_color=YELLOW, 
            fill_opacity=0.05, 
            stroke_width=2, 
            corner_radius=0.08
        )
        beam_box_2.move_to(np.array([-2.75, -0.35, 0]))

        self.play(
            ReplacementTransform(beam_box_1, beam_box_2),
            lbl_beam_1.animate.next_to(beam_box_2, UP, buff=0.05),
            run_time=1.0
        )
        self.wait(2.7)

        # Cắt tỉa các nhánh bắt đầu từ "an" (American, artist) và node cha "an" (lựa chọn tham lam!)
        self.play(
            bs_nodes_t2[0].animate.set_opacity(0.15),
            bs_nodes_t2[1].animate.set_opacity(0.15),
            bs_lines_t2[0].animate.set_opacity(0.15),
            bs_lines_t2[1].animate.set_opacity(0.15),
            bs_nodes_t1[0].animate.set_opacity(0.15), # Node "an" bị mờ đi
            bs_lines_t1[0].animate.set_opacity(0.15),
            run_time=0.8
        )
        self.wait(3.2)

        # Highlight hai nhánh sống sót: Taylor Swift is -> a -> singer/songwriter
        self.play(
            bs_nodes_t2[2][0].animate.set_color(GREEN).set_stroke(width=3),
            bs_nodes_t2[3][0].animate.set_color(GREEN).set_stroke(width=3),
            bs_nodes_t1[1][0].animate.set_color(GREEN).set_stroke(width=2.5),
            bs_lines_t2[2].animate.set_color(GREEN).set_stroke(width=3.5),
            bs_lines_t2[3].animate.set_color(GREEN).set_stroke(width=3.5),
            bs_lines_t1[1].animate.set_color(GREEN).set_stroke(width=3.5),
            run_time=1.2
        )
        self.wait(2.0)

        # Nhãn giải thích việc cắt tỉa đường đi tham lam
        prune_explain = create_text("Chùm K=2 chuyển hướng, loại bỏ nhánh 'an' (lựa chọn tham lam bị prune!)", font_size=10, color=GREEN_A)
        prune_explain.next_to(beam_box_2, DOWN, buff=0.45).shift(LEFT * 0.2)
        
        self.play(
            FadeIn(prune_explain, shift=UP * 0.15),
            run_time=0.8
        )
        self.wait(6.0)

        # Dọn dẹp toàn bộ để sang phần Summary
        self.play(
            FadeOut(beam_header),
            FadeOut(divider_line_bs),
            FadeOut(bs_root_node),
            FadeOut(bs_nodes_t1[0]), FadeOut(bs_nodes_t1[1]), FadeOut(bs_nodes_t1[2]), FadeOut(bs_nodes_t1[3]),
            FadeOut(bs_lines_t1[0]), FadeOut(bs_lines_t1[1]), FadeOut(bs_lines_t1[2]), FadeOut(bs_lines_t1[3]),
            FadeOut(beam_box_2),
            FadeOut(lbl_beam_1),
            FadeOut(bs_nodes_t2[0]), FadeOut(bs_nodes_t2[1]), FadeOut(bs_nodes_t2[2]), FadeOut(bs_nodes_t2[3]),
            FadeOut(bs_lines_t2[0]), FadeOut(bs_lines_t2[1]), FadeOut(bs_lines_t2[2]), FadeOut(bs_lines_t2[3]),
            FadeOut(bs_q2),
            FadeOut(prune_explain),
            FadeOut(config_group),
            run_time=1.2
        )
        self.wait(1.5)


        # =====================================================================
        # BƯỚC 5: TỔNG KẾT & QUY LUẬT CHÙM (05:00 - 05:30)
        # =====================================================================
        summary_title = create_text("Tóm tắt Quy luật Tìm kiếm Chùm", font_size=16, color=BLUE_B)
        summary_title.to_edge(UP, buff=1.0)
        
        rule_1 = create_markup_text("• Khi <color color='#e67e22'>K = 1</color>: Beam Search trở thành <b>Giải mã Tham lam (Greedy)</b>", font_size=12)
        rule_2 = create_markup_text("• Khi <color color='#2ecc71'>K tăng lên</color>: Tăng độ chính xác (MAP), mở rộng không gian tìm kiếm", font_size=12)
        rule_3 = create_markup_text("• <color color='#e74c3c'>Chi phí phần cứng</color>: Độ phức tạp tính toán tăng <b>tuyến tính với K</b>", font_size=12)
        
        rules_group = VGroup(rule_1, rule_2, rule_3).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        rules_group.move_to(ORIGIN)

        self.play(Write(summary_title), run_time=0.8)
        self.wait(2.7)
        
        for rule in rules_group:
            self.play(FadeIn(rule, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(4.0)

        self.wait(4.5)

        # FadeOut toàn bộ
        self.play(
            FadeOut(summary_title),
            FadeOut(rules_group),
            FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(2.7)
