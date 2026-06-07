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
        # GIAI ĐOẠN 2: LÀN SÓNG 1 - PRE-TRAINING COMPUTING
        # =====================================================================
        # Highlight trục X
        flash_x = Arrow(origin_pt, origin_pt + RIGHT * 4.2, color=YELLOW, buff=0, stroke_width=5)
        
        # Thẻ thông tin làn sóng 1
        card_w, card_h = 4.6, 1.8
        card_x = 4.5
        
        pt_card_bg = RoundedRectangle(width=card_w, height=card_h, color=PURPLE, fill_color="#181124", fill_opacity=0.9, corner_radius=0.1)
        pt_card_bg.move_to(RIGHT * card_x + UP * 1.8)
        pt_card_title = create_text("1. Làn sóng Pre-training", font_size=10, color=PURPLE_A)
        pt_card_title.next_to(pt_card_bg.get_top(), DOWN, buff=0.15)
        pt_card_desc = create_markup_text(
            "• Mở rộng kích thước mô hình &amp; dữ liệu\n"
            "• Tài liệu tham khảo chính:\n"
            "  - Kaplan et al., 2020 (Scaling Laws)\n"
            "  - Hoffmann et al., 2022 (Chinchilla)",
            font_size=7.5, line_spacing=1.2
        ).next_to(pt_card_title, DOWN, buff=0.12).align_to(pt_card_bg, LEFT).shift(RIGHT * 0.3)
        pt_card = VGroup(pt_card_bg, pt_card_title, pt_card_desc)

        self.play(FadeIn(flash_x), run_time=0.4)
        self.play(FadeIn(pt_card, shift=LEFT * 0.3), run_time=1.0)
        self.wait(15.0)
        self.play(FadeOut(flash_x), run_time=0.4)

        # =====================================================================
        # GIAI ĐOẠN 3: LÀN SÓNG 2 - POST-TRAINING COMPUTING
        # =====================================================================
        # Highlight trục Y
        flash_y = Arrow(origin_pt, origin_pt + UP * 3.5, color=YELLOW, buff=0, stroke_width=5)
        
        post_card_bg = RoundedRectangle(width=card_w, height=card_h, color=GREEN, fill_color="#0e1612", fill_opacity=0.9, corner_radius=0.1)
        post_card_bg.move_to(RIGHT * card_x + UP * 0.0)
        post_card_title = create_text("2. Làn sóng Post-training", font_size=10, color=GREEN_A)
        post_card_title.next_to(post_card_bg.get_top(), DOWN, buff=0.15)
        post_card_desc = create_markup_text(
            "• Tinh chỉnh dựa trên cặp (input, output)\n"
            "• Học hướng dẫn &amp; Căn chỉnh (RLHF/DPO)\n"
            "• Tài liệu tham khảo chính:\n"
            "  - Chung et al., 2022 (Scaling Post-training)",
            font_size=7.5, line_spacing=1.2
        ).next_to(post_card_title, DOWN, buff=0.12).align_to(post_card_bg, LEFT).shift(RIGHT * 0.3)
        post_card = VGroup(post_card_bg, post_card_title, post_card_desc)

        self.play(FadeIn(flash_y), run_time=0.4)
        self.play(FadeIn(post_card, shift=LEFT * 0.3), run_time=1.0)
        self.wait(15.0)
        self.play(FadeOut(flash_y), run_time=0.4)

        # =====================================================================
        # GIAI ĐOẠN 4: LÀN SÓNG 3 - TEST-TIME COMPUTING
        # =====================================================================
        # Highlight trục Z
        flash_z = Arrow(origin_pt, origin_pt + DR * 2.0, color=YELLOW, buff=0, stroke_width=5)
        
        tt_card_bg = RoundedRectangle(width=card_w, height=card_h, color=BLUE, fill_color="#0b1324", fill_opacity=0.9, corner_radius=0.1)
        tt_card_bg.move_to(RIGHT * card_x + DOWN * 1.8)
        tt_card_title = create_text("3. Làn sóng Test-time compute", font_size=10, color=BLUE_A)
        tt_card_title.next_to(tt_card_bg.get_top(), DOWN, buff=0.15)
        tt_card_desc = create_markup_text(
            "• Tăng lượng tính toán trong lúc sinh token\n"
            "• Tìm kiếm giải pháp, lập luận nhiều bước\n"
            "• Tài liệu tham khảo chính:\n"
            "  - OpenAI, 2024 (o1); Welleck et al., 2024",
            font_size=7.5, line_spacing=1.2
        ).next_to(tt_card_title, DOWN, buff=0.12).align_to(tt_card_bg, LEFT).shift(RIGHT * 0.3)
        tt_card = VGroup(tt_card_bg, tt_card_title, tt_card_desc)

        self.play(FadeIn(flash_z), run_time=0.4)
        self.play(FadeIn(tt_card, shift=LEFT * 0.3), run_time=1.0)
        self.wait(18.0)
        self.play(FadeOut(flash_z), run_time=0.4)

        # =====================================================================
        # GIAI ĐOẠN 5: TỔNG KẾT & QUAY LẠI HỆ TRỤC 3D TOÀN CẢNH
        # =====================================================================
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
        self.wait(18.0)


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
