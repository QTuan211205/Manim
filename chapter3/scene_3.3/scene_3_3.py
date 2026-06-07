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


class Scene3_3(Scene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH
        # =====================================================================
        chapter_title = create_text("Chương 3: Bộ điều phối cấp cao", font_size=24, color=YELLOW)
        chapter_sub = create_text("Phần 3.3: Tìm kiếm trên cây & Quay lui (Tree Search & Backtracking)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(3.0)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Tìm kiếm trên cây & Quay lui (Tree Search & Backtracking)", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # PHẦN 1: SỰ LÃNG PHÍ CỦA PHƯƠNG PHÁP SONG SONG & KHÁI NIỆM TREE SEARCH
        # =====================================================================
        part1_title = create_text("1. Sự lãng phí của giải mã song song & Cơ chế Tree Search", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part1_title), run_time=0.8)
        self.wait(2.0)

        # Mô tả lý do chuyển dịch
        intro_text = create_text(
            "Nếu mô hình ngôn ngữ phạm sai lầm ngay từ bước lập luận đầu tiên,\n"
            "việc tiếp tục sinh các token phía sau sẽ gây lãng phí tài nguyên tính toán.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)
        self.play(Write(intro_text), run_time=2.0)
        self.wait(9.0)

        # Vẽ sơ đồ lãng phí tính toán (Wasted Compute)
        prompt_box = RoundedRectangle(width=1.8, height=0.7, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        prompt_box.move_to(LEFT * 5.0 + DOWN * 0.6)
        prompt_lbl = create_text("Prompt x", font_size=11, color=GREEN).move_to(prompt_box.get_center())

        self.play(FadeIn(prompt_box), Write(prompt_lbl), run_time=1.0)
        self.wait(3.0)

        # Nhánh 1 (Lỗi): đi lên
        y_top = 0.5
        box1_1 = RoundedRectangle(width=1.6, height=0.5, color=RED, fill_color="#3c1414", fill_opacity=0.8, corner_radius=0.05)
        box1_1.move_to(LEFT * 2.2 + UP * y_top)
        lbl1_1 = create_text("Bước 1: Sai", font_size=10, color=RED).move_to(box1_1.get_center())
        arrow1_1 = Arrow(start=prompt_box.get_right(), end=box1_1.get_left(), color=RED, stroke_width=1.5, buff=0.05)

        box1_2 = RoundedRectangle(width=1.6, height=0.5, color=GRAY_D, fill_color="#141517", fill_opacity=0.8, corner_radius=0.05)
        box1_2.move_to(LEFT * 0.1 + UP * y_top)
        lbl1_2 = create_text("Bước 2", font_size=10, color=GRAY_B).move_to(box1_2.get_center())
        arrow1_2 = Arrow(start=box1_1.get_right(), end=box1_2.get_left(), color=GRAY_D, stroke_width=1.2, buff=0.05)

        box1_3 = RoundedRectangle(width=1.6, height=0.5, color=GRAY_D, fill_color="#141517", fill_opacity=0.8, corner_radius=0.05)
        box1_3.move_to(RIGHT * 2.0 + UP * y_top)
        lbl1_3 = create_text("Bước 3", font_size=10, color=GRAY_B).move_to(box1_3.get_center())
        arrow1_3 = Arrow(start=box1_2.get_right(), end=box1_3.get_left(), color=GRAY_D, stroke_width=1.2, buff=0.05)

        result1_box = RoundedRectangle(width=1.8, height=0.5, color=RED_D, fill_color="#141517", fill_opacity=0.8, corner_radius=0.05)
        result1_box.move_to(RIGHT * 4.3 + UP * y_top)
        result1_lbl = create_text("ORM Score: 0.15", font_size=9, color=RED).move_to(result1_box.get_center())
        arrow1_4 = Arrow(start=box1_3.get_right(), end=result1_box.get_left(), color=RED_D, stroke_width=1.2, buff=0.05)

        # Nhánh 2 (Đúng): đi xuống
        y_bot = -1.5
        box2_1 = RoundedRectangle(width=1.6, height=0.5, color=GREEN, fill_color="#143c14", fill_opacity=0.8, corner_radius=0.05)
        box2_1.move_to(LEFT * 2.2 + UP * y_bot)
        lbl2_1 = create_text("Bước 1: Đúng", font_size=10, color=GREEN).move_to(box2_1.get_center())
        arrow2_1 = Arrow(start=prompt_box.get_right(), end=box2_1.get_left(), color=GREEN, stroke_width=1.5, buff=0.05)

        box2_2 = RoundedRectangle(width=1.6, height=0.5, color=GRAY_D, fill_color="#141517", fill_opacity=0.8, corner_radius=0.05)
        box2_2.move_to(LEFT * 0.1 + UP * y_bot)
        lbl2_2 = create_text("Bước 2", font_size=10, color=WHITE).move_to(box2_2.get_center())
        arrow2_2 = Arrow(start=box2_1.get_right(), end=box2_2.get_left(), color=GREEN, stroke_width=1.2, buff=0.05)

        box2_3 = RoundedRectangle(width=1.6, height=0.5, color=GRAY_D, fill_color="#141517", fill_opacity=0.8, corner_radius=0.05)
        box2_3.move_to(RIGHT * 2.0 + UP * y_bot)
        lbl2_3 = create_text("Bước 3", font_size=10, color=WHITE).move_to(box2_3.get_center())
        arrow2_3 = Arrow(start=box2_2.get_right(), end=box2_3.get_left(), color=GREEN, stroke_width=1.2, buff=0.05)

        result2_box = RoundedRectangle(width=1.8, height=0.5, color=GREEN_D, fill_color="#141517", fill_opacity=0.8, corner_radius=0.05)
        result2_box.move_to(RIGHT * 4.3 + UP * y_bot)
        result2_lbl = create_text("ORM Score: 0.88", font_size=9, color=GREEN).move_to(result2_box.get_center())
        arrow2_4 = Arrow(start=box2_3.get_right(), end=result2_box.get_left(), color=GREEN_D, stroke_width=1.2, buff=0.05)

        self.play(
            Create(arrow1_1), Create(arrow2_1),
            FadeIn(box1_1), FadeIn(box2_1),
            Write(lbl1_1), Write(lbl2_1),
            run_time=2.0
        )
        self.wait(8.0)

        # Vẽ tiếp các bước sau của cả 2 nhánh
        self.play(
            Create(arrow1_2), Create(arrow2_2),
            Create(arrow1_3), Create(arrow2_3),
            Create(arrow1_4), Create(arrow2_4),
            FadeIn(box1_2), FadeIn(box2_2),
            FadeIn(box1_3), FadeIn(box2_3),
            FadeIn(result1_box), FadeIn(result2_box),
            Write(lbl1_2), Write(lbl2_2),
            Write(lbl1_3), Write(lbl2_3),
            Write(result1_lbl), Write(result2_lbl),
            run_time=2.5
        )
        self.wait(9.0)

        # Vẽ khung đỏ biểu thị tính toán lãng phí của nhánh 1
        wasted_rect = RoundedRectangle(width=6.5, height=0.9, color=RED, stroke_width=2, fill_opacity=0, corner_radius=0.08)
        wasted_rect.move_to(RIGHT * 2.15 + UP * y_top)
        wasted_lbl = create_text("Tính toán lãng phí (Wasted Compute)", font_size=9, color=RED)
        wasted_lbl.next_to(wasted_rect, UP, buff=0.1)

        self.play(
            Create(wasted_rect),
            FadeIn(wasted_lbl, shift=DOWN * 0.1),
            run_time=1.0
        )
        self.wait(11.0)

        # Xóa các thành phần và giới thiệu 4 yếu tố thiết kế Tree Search
        self.play(
            FadeOut(prompt_box), FadeOut(prompt_lbl),
            FadeOut(box1_1), FadeOut(box1_2), FadeOut(box1_3), FadeOut(box2_1), FadeOut(box2_2), FadeOut(box2_3),
            FadeOut(lbl1_1), FadeOut(lbl1_2), FadeOut(lbl1_3), FadeOut(lbl2_1), FadeOut(lbl2_2), FadeOut(lbl2_3),
            FadeOut(arrow1_1), FadeOut(arrow1_2), FadeOut(arrow1_3), FadeOut(arrow1_4),
            FadeOut(arrow2_1), FadeOut(arrow2_2), FadeOut(arrow2_3), FadeOut(arrow2_4),
            FadeOut(result1_box), FadeOut(result2_box), FadeOut(result1_lbl), FadeOut(result2_lbl),
            FadeOut(wasted_rect), FadeOut(wasted_lbl),
            FadeOut(intro_text),
            run_time=1.2
        )

        design_title = create_text("4 yếu tố thiết kế Tree Search cơ bản:", font_size=14, color=YELLOW).move_to(UP * 2.0)
        self.play(Write(design_title), run_time=1.0)

        design_items = VGroup(
            create_markup_text("• <b>Trạng thái (States <i>s</i>):</b> Tiền tố lập luận đã sinh.", font_size=12),
            create_markup_text("• <b>Bước chuyển (Transitions <i>s → s'</i>):</b> Khám phá bước tiếp theo.", font_size=12),
            create_markup_text("• <b>Điểm đánh giá (Scores <i>v(s)</i>):</b> Xác định tiềm năng của bước hiện tại.", font_size=12),
            create_markup_text("• <b>Chiến lược duyệt (Strategy):</b> Tìm kiếm theo chiều sâu (DFS), chiều rộng (BFS), ...", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.3)

        for item in design_items:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(3.5)

        self.wait(6.0)

        # Dọn dẹp phần 1
        self.play(
            FadeOut(design_title),
            FadeOut(design_items),
            FadeOut(part1_title),
            run_time=1.2
        )
        self.wait(1.0)

        # =====================================================================
        # PHẦN 2: PROCESS-BASED REWARD MODEL (PRM)
        # =====================================================================
        part2_title = create_text("2. Process-based Reward Model (PRM)", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part2_title), run_time=0.8)
        self.wait(2.0)

        # Lược đồ phân biệt ORM và PRM
        intro_part2 = create_text(
            "PRM chấm điểm trên từng bước lập luận trung gian để kiểm soát tiến trình,\n"
            "khác biệt hoàn toàn với ORM vốn chỉ chấm điểm ở kết quả cuối cùng.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)
        self.play(Write(intro_part2), run_time=2.0)
        self.wait(14.0)

        # Khối so sánh ORM (trái) và PRM (phải)
        box_width, box_height = 3.6, 2.0
        
        # ORM Block
        orm_box = RoundedRectangle(width=box_width, height=box_height, color=BLUE_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        orm_box.move_to(LEFT * 3.6 + DOWN * 0.4)
        orm_lbl = create_text("Outcome-based RM\n(ORM)", font_size=13, color=BLUE_A).move_to(orm_box.get_center() + UP * 0.5)
        orm_desc = create_text("Đánh giá toàn bộ câu trả lời y\nv(y) thuộc [0, 1] ở cuối chặng", font_size=10, color=GRAY_B).move_to(orm_box.get_center() + DOWN * 0.4)
        
        orm_group = VGroup(orm_box, orm_lbl, orm_desc)

        # Input / Output ORM
        orm_input = create_text("Chuỗi y", font_size=11, color=WHITE).next_to(orm_box, LEFT, buff=0.6)
        orm_in_arrow = Arrow(start=orm_input.get_right(), end=orm_box.get_left(), color=BLUE_B, stroke_width=1.5, buff=0.08)
        orm_output = create_text("Score: 0.88", font_size=11, color=GREEN).next_to(orm_box, RIGHT, buff=0.6)
        orm_out_arrow = Arrow(start=orm_box.get_right(), end=orm_output.get_left(), color=GREEN, stroke_width=1.5, buff=0.08)

        # PRM Block
        prm_box = RoundedRectangle(width=box_width, height=box_height, color=GOLD_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        prm_box.move_to(RIGHT * 3.6 + DOWN * 0.4)
        prm_lbl = create_text("Process-based RM\n(PRM)", font_size=13, color=GOLD_A).move_to(prm_box.get_center() + UP * 0.5)
        prm_desc = create_text("Đánh giá từng bước lập luận s(t)\nv(x, s1, ..., st) thuộc [0, 1]", font_size=10, color=GRAY_B).move_to(prm_box.get_center() + DOWN * 0.4)
        
        prm_group = VGroup(prm_box, prm_lbl, prm_desc)

        # Input / Output PRM
        prm_input = create_text("Bước s(t)", font_size=11, color=WHITE).next_to(prm_box, LEFT, buff=0.6)
        prm_in_arrow = Arrow(start=prm_input.get_right(), end=prm_box.get_left(), color=GOLD_B, stroke_width=1.5, buff=0.08)
        prm_output = create_text("Score: 0.95", font_size=11, color=GREEN).next_to(prm_box, RIGHT, buff=0.6)
        prm_out_arrow = Arrow(start=prm_box.get_right(), end=prm_output.get_left(), color=GREEN, stroke_width=1.5, buff=0.08)

        # Hiển thị ORM trước
        self.play(
            FadeIn(orm_group),
            FadeIn(orm_input), Create(orm_in_arrow),
            run_time=1.5
        )
        self.play(FadeIn(orm_output), Create(orm_out_arrow), run_time=1.0)
        self.wait(14.0)

        # Hiển thị PRM sau
        self.play(
            FadeIn(prm_group),
            FadeIn(prm_input), Create(prm_in_arrow),
            run_time=1.5
        )
        self.play(FadeIn(prm_output), Create(prm_out_arrow), run_time=1.0)
        self.wait(18.0)

        # Hiển thị công thức PRM lên phía trên thay thế intro
        prm_formula_box = RoundedRectangle(width=5.8, height=0.8, color=GOLD, fill_color="#16171a", fill_opacity=0.9, corner_radius=0.08)
        prm_formula_box.move_to(UP * 2.1)
        prm_formula_txt = create_markup_text(
            "Công thức PRM:  <span color='#FFD700'><i>v</i>(<i>x</i>, <i>s</i><sub>1</sub>, <i>s</i><sub>2</sub>, ..., <i>s</i><sub><i>t</i></sub>) → [0, 1]</span>",
            font_size=13
        ).move_to(prm_formula_box.get_center())

        self.play(
            FadeOut(intro_part2),
            FadeIn(prm_formula_box),
            Write(prm_formula_txt),
            run_time=1.2
        )
        self.wait(24.3)

        # Dọn dẹp phần 2
        self.play(
            FadeOut(prm_formula_box), FadeOut(prm_formula_txt),
            FadeOut(orm_group), FadeOut(orm_input), FadeOut(orm_in_arrow), FadeOut(orm_output), FadeOut(orm_out_arrow),
            FadeOut(prm_group), FadeOut(prm_input), FadeOut(prm_in_arrow), FadeOut(prm_output), FadeOut(prm_out_arrow),
            FadeOut(part2_title),
            run_time=1.2
        )
        self.wait(1.0)

        # =====================================================================
        # PHẦN 3: HOẠT HỌA TÌM KIẾM & QUAY LUI (BACKTRACKING)
        # =====================================================================
        part3_title = create_text("3. Hoạt họa Tìm kiếm & Quay lui (Backtracking)", font_size=13, color=BLUE_A)
        part3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part3_title), run_time=0.8)
        self.wait(2.0)

        # Tiêu đề nhỏ mô tả ngữ cảnh
        tree_intro = create_markup_text(
            "PRM chấm điểm trên từng bước lập luận: các bước điểm thấp bị loại bỏ,\n"
            "thuật toán thực hiện <b>Quay lui (Backtracking)</b> để đi theo nhánh tốt hơn.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 2.1)
        self.play(Write(tree_intro), run_time=2.0)
        self.wait(14.0)

        # Vẽ cây quyết định
        # Vị trí các nút
        root_pos = UP * 0.8 + ORIGIN
        s1_pos = LEFT * 2.5 + DOWN * 0.4
        s2_pos = RIGHT * 2.5 + DOWN * 0.4
        s3_pos = LEFT * 2.5 + DOWN * 1.8
        s4_pos = RIGHT * 2.5 + DOWN * 1.8

        # Nút dạng hình tròn
        node_radius = 0.45
        root_circle = Circle(radius=node_radius, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        root_circle.move_to(root_pos)
        root_lbl = create_text("x", font_size=14, color=YELLOW).move_to(root_pos)

        s1_circle = Circle(radius=node_radius, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        s1_circle.move_to(s1_pos)
        s1_lbl = create_text("s1", font_size=13, color=WHITE).move_to(s1_pos)

        s2_circle = Circle(radius=node_radius, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        s2_circle.move_to(s2_pos)
        s2_lbl = create_text("s2", font_size=13, color=WHITE).move_to(s2_pos)

        s3_circle = Circle(radius=node_radius, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        s3_circle.move_to(s3_pos)
        s3_lbl = create_text("s3", font_size=13, color=WHITE).move_to(s3_pos)

        s4_circle = Circle(radius=node_radius, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        s4_circle.move_to(s4_pos)
        s4_lbl = create_text("s4", font_size=13, color=WHITE).move_to(s4_pos)

        # Các đường kết nối ban đầu (xám nhạt)
        line_root_s1 = Line(start=root_pos + DOWN * node_radius, end=s1_pos + UP * node_radius, color=GRAY_E, stroke_width=2)
        line_root_s2 = Line(start=root_pos + DOWN * node_radius, end=s2_pos + UP * node_radius, color=GRAY_E, stroke_width=2)
        line_s1_s3 = Line(start=s1_pos + DOWN * node_radius, end=s3_pos + UP * node_radius, color=GRAY_E, stroke_width=1.5)
        line_s2_s4 = Line(start=s2_pos + DOWN * node_radius, end=s4_pos + UP * node_radius, color=GRAY_E, stroke_width=1.5)

        # Hiển thị cây cơ bản
        self.play(
            Create(line_root_s1), Create(line_root_s2),
            Create(line_s1_s3), Create(line_s2_s4),
            FadeIn(root_circle), FadeIn(s1_circle), FadeIn(s2_circle), FadeIn(s3_circle), FadeIn(s4_circle),
            Write(root_lbl), Write(s1_lbl), Write(s2_lbl), Write(s3_lbl), Write(s4_lbl),
            run_time=2.5
        )
        self.wait(14.0)

        # Bước 1: Thuật toán đi thử theo nhánh s2 (phải)
        path_root_s2 = Line(start=root_pos + DOWN * node_radius, end=s2_pos + UP * node_radius, color=YELLOW, stroke_width=4.0)
        self.play(
            Create(path_root_s2),
            s2_circle.animate.set_color(YELLOW),
            run_time=1.0
        )
        self.wait(9.0)

        # PRM đánh giá s2 điểm thấp
        s2_score = create_text("PRM: 0.20", font_size=11, color=RED).next_to(s2_circle, RIGHT, buff=0.15)
        s2_cross = get_crossmark().next_to(s2_score, RIGHT, buff=0.1)

        self.play(
            FadeIn(s2_score),
            Create(s2_cross),
            s2_circle.animate.set_color(RED),
            run_time=1.0
        )
        self.wait(8.0)

        # Bước 2: Backtracking - Quay lui
        # Chuyển nhánh sang đỏ rồi co rút về root
        backtrack_path = Line(start=s2_pos + UP * node_radius, end=root_pos + DOWN * node_radius, color=RED, stroke_width=4.0)
        
        self.play(
            ReplacementTransform(path_root_s2, backtrack_path),
            run_time=0.5
        )
        self.play(
            FadeOut(backtrack_path),
            s2_circle.animate.set_color(GRAY_D),
            run_time=1.0
        )
        self.wait(11.0)

        # Bước 3: Thuật toán đi theo nhánh s1 (trái)
        path_root_s1 = Line(start=root_pos + DOWN * node_radius, end=s1_pos + UP * node_radius, color=GREEN, stroke_width=4.0)
        self.play(
            Create(path_root_s1),
            s1_circle.animate.set_color(GREEN),
            run_time=1.0
        )
        self.wait(8.0)

        # PRM đánh giá s1 điểm cao
        s1_score = create_text("PRM: 0.95", font_size=11, color=GREEN).next_to(s1_circle, LEFT, buff=0.15)
        s1_check = get_checkmark().next_to(s1_score, LEFT, buff=0.1)

        self.play(
            FadeIn(s1_score),
            Create(s1_check),
            s1_circle.animate.set_color(GREEN),
            run_time=1.0
        )
        self.wait(9.0)

        # Bước 4: Tiếp tục đi xuống s3
        path_s1_s3 = Line(start=s1_pos + DOWN * node_radius, end=s3_pos + UP * node_radius, color=GREEN, stroke_width=4.0)
        self.play(
            Create(path_s1_s3),
            s3_circle.animate.set_color(GREEN),
            run_time=1.0
        )
        self.wait(8.0)

        # PRM đánh giá s3 điểm tốt -> tìm ra đáp án đúng
        s3_score = create_text("PRM: 0.85", font_size=11, color=GREEN).next_to(s3_circle, LEFT, buff=0.15)
        s3_check = get_checkmark().next_to(s3_score, LEFT, buff=0.1)

        self.play(
            FadeIn(s3_score),
            Create(s3_check),
            s3_circle.animate.set_color(GREEN),
            run_time=1.0
        )
        self.wait(8.0)

        # Kết quả cuối y_correct
        y_box = RoundedRectangle(width=2.4, height=0.6, color=GREEN, fill_color="#143c14", fill_opacity=0.9, corner_radius=0.06)
        y_box.move_to(LEFT * 2.5 + DOWN * 2.8)
        y_lbl = create_text("y_correct (Đáp án)", font_size=11, color=WHITE).move_to(y_box.get_center())
        arrow_to_y = Arrow(start=s3_circle.get_bottom(), end=y_box.get_top(), color=GREEN, stroke_width=1.5, buff=0.05)

        self.play(
            FadeIn(y_box),
            Write(y_lbl),
            Create(arrow_to_y),
            run_time=1.5
        )
        self.wait(18.0)

        # Dọn dẹp phần 3
        self.play(
            FadeOut(tree_intro),
            FadeOut(root_circle), FadeOut(root_lbl),
            FadeOut(s1_circle), FadeOut(s1_lbl), FadeOut(s1_score), FadeOut(s1_check),
            FadeOut(s2_circle), FadeOut(s2_lbl), FadeOut(s2_score), FadeOut(s2_cross),
            FadeOut(s3_circle), FadeOut(s3_lbl), FadeOut(s3_score), FadeOut(s3_check),
            FadeOut(s4_circle), FadeOut(s4_lbl),
            FadeOut(line_root_s1), FadeOut(line_root_s2), FadeOut(line_s1_s3), FadeOut(line_s2_s4),
            FadeOut(path_root_s1), FadeOut(path_s1_s3), FadeOut(y_box), FadeOut(y_lbl), FadeOut(arrow_to_y),
            FadeOut(part3_title),
            run_time=1.2
        )
        self.wait(1.0)

        # =====================================================================
        # PHẦN 4: GIẢI THUẬT REBASE (REWARD BALANCED SEARCH)
        # =====================================================================
        part4_title = create_text("4. Giải thuật Rebase (Reward Balanced Search)", font_size=13, color=BLUE_A)
        part4_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part4_title), run_time=0.8)
        self.wait(2.0)

        # Trực quan hóa công thức Rebase
        rebase_formula_box = RoundedRectangle(width=8.0, height=1.1, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        rebase_formula_box.move_to(UP * 1.5)
        
        # Viết công thức Rebase sử dụng MarkupText thay thế LaTeX
        rebase_txt = create_markup_text(
            "Công thức Rebase:  <span color='#87CEFA'>explore<sub><i>i</i></sub> = Round( Budget × </span>"
            "<span color='#00FF7F'>e<sup><i>v</i>(<i>s</i><sub><i>i</i></sub>)/τ</sup></span> / "
            "<span color='#FFD700'>∑<sub><i>j</i></sub> e<sup><i>v</i>(<i>s</i><sub><i>j</i></sub>)/τ</sup></span><span color='#87CEFA'> )</span>",
            font_size=13
        ).move_to(rebase_formula_box.get_center())

        self.play(
            FadeIn(rebase_formula_box),
            Write(rebase_txt),
            run_time=1.5
        )
        self.wait(19.0)

        # Annotations các biến giải thích
        annotations = VGroup(
            create_markup_text("<span color='#87CEFA'>• <b>explore<sub><i>i</i></sub>:</b></span> Số lượng luồng tính toán phân bổ cho nhánh <i>s<sub>i</sub></i>.", font_size=11),
            create_markup_text("<span color='#FFFFFF'>• <b>Budget:</b></span> Tổng ngân sách luồng tính toán tại thời điểm suy luận.", font_size=11),
            create_markup_text("<span color='#00FF7F'>• <b><i>v</i>(<i>s</i><sub><i>i</i></sub>):</b></span> Điểm số PRM phản ánh độ hứa hẹn của trạng thái <i>s<sub>i</sub></i>.", font_size=11),
            create_markup_text("<span color='#FFA500'>• <b>τ (Nhiệt độ):</b></span> Tham số điều phối: τ nhỏ -> tập trung; τ lớn -> đa dạng.", font_size=11)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 0.3)

        self.play(FadeIn(annotations, shift=UP * 0.2), run_time=2.5)
        self.wait(27.0)

        # Xóa annotations để hiện ví dụ phân bổ
        self.play(FadeOut(annotations), run_time=1.0)
        self.wait(1.0)

        # Mô phỏng phân bổ thực tế
        sim_title = create_text("Ví dụ: Ngân sách Budget = 10 luồng | Nhiệt độ τ = 0.3", font_size=12, color=YELLOW).move_to(UP * 0.5)
        self.play(Write(sim_title), run_time=1.0)

        # Node A
        node_a = RoundedRectangle(width=2.5, height=0.7, color=GREEN, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        node_a.move_to(LEFT * 3.8 + DOWN * 0.8)
        lbl_a = create_text("Nhánh sA (PRM: 0.90)", font_size=10, color=GREEN).move_to(node_a.get_center())

        # Node B
        node_b = RoundedRectangle(width=2.5, height=0.7, color=RED, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        node_b.move_to(RIGHT * 3.8 + DOWN * 0.8)
        lbl_b = create_text("Nhánh sB (PRM: 0.30)", font_size=10, color=RED).move_to(node_b.get_center())

        self.play(
            FadeIn(node_a), Write(lbl_a),
            FadeIn(node_b), Write(lbl_b),
            run_time=1.5
        )
        self.wait(9.0)

        # Kết quả tính toán phân bổ
        alloc_a = create_markup_text("Phân bổ: <span color='#00FF00'><b>9 luồng</b></span> (90% compute)", font_size=11)
        alloc_a.next_to(node_a, DOWN, buff=0.25)

        alloc_b = create_markup_text("Phân bổ: <span color='#FF0000'><b>1 luồng</b></span> (10% compute)", font_size=11)
        alloc_b.next_to(node_b, DOWN, buff=0.25)

        self.play(
            FadeIn(alloc_a, shift=UP * 0.15),
            FadeIn(alloc_b, shift=UP * 0.15),
            run_time=1.5
        )
        self.wait(15.0)

        # Vẽ các luồng sinh tỏa ra từ 2 nút biểu thị compute allocation
        arrows_a = VGroup()
        arrows_b = VGroup()

        # 9 luồng từ node_a
        for idx in range(9):
            angle = (-30 + idx * 7.5) * DEGREES
            arr = Arrow(
                start=node_a.get_right(),
                end=node_a.get_right() + RIGHT * 1.5 + UP * np.sin(angle) * 0.8,
                color=GREEN, stroke_width=1.0, buff=0.05
            )
            arrows_a.add(arr)

        # 1 luồng từ node_b
        arr_b = Arrow(
            start=node_b.get_right(),
            end=node_b.get_right() + RIGHT * 1.5,
            color=RED, stroke_width=1.0, buff=0.05
        )
        arrows_b.add(arr_b)

        self.play(
            Create(arrows_a),
            Create(arrows_b),
            run_time=2.0
        )
        self.wait(18.0)

        # Dọn dẹp phần 4
        self.play(
            FadeOut(rebase_formula_box), FadeOut(rebase_txt),
            FadeOut(sim_title),
            FadeOut(node_a), FadeOut(lbl_a), FadeOut(node_b), FadeOut(lbl_b),
            FadeOut(alloc_a), FadeOut(alloc_b),
            FadeOut(arrows_a), FadeOut(arrows_b),
            FadeOut(part4_title),
            run_time=1.2
        )
        self.wait(1.0)

        # =====================================================================
        # PHẦN 5: CÁC KỸ THUẬT DUYỆT CÂY & ỨNG DỤNG
        # =====================================================================
        part5_title = create_text("5. Các giải thuật duyệt cây & Ứng dụng thực tế", font_size=13, color=BLUE_A)
        part5_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(part5_title), run_time=0.8)
        self.wait(2.0)

        # Sơ đồ Grid / Mindmap
        center_box = RoundedRectangle(width=3.2, height=0.8, color=YELLOW, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        center_box.move_to(ORIGIN)
        center_lbl = create_text("Tree Search", font_size=13, color=YELLOW).move_to(center_box.get_center())

        # Nhánh trái: Thuật toán
        left_box = RoundedRectangle(width=3.4, height=1.6, color=BLUE_B, fill_color="#141517", fill_opacity=0.8, corner_radius=0.06)
        left_box.move_to(LEFT * 3.8)
        left_lbl = create_text("Thuật toán phổ biến", font_size=11, color=BLUE_A).move_to(left_box.get_center() + UP * 0.5)
        left_desc = create_markup_text(
            "• DFS (Chiều sâu)\n• BFS (Chiều rộng)\n• Tree of Thoughts (ToT)\n• Monte Carlo Tree Search (MCTS)",
            font_size=9, line_spacing=1.2
        ).move_to(left_box.get_center() + DOWN * 0.25)
        arrow_left = Arrow(start=center_box.get_left(), end=left_box.get_right(), color=BLUE_B, stroke_width=1.5, buff=0.05)

        # Nhánh phải: Ứng dụng
        right_box = RoundedRectangle(width=3.4, height=1.6, color=GREEN_B, fill_color="#141517", fill_opacity=0.8, corner_radius=0.06)
        right_box.move_to(RIGHT * 3.8)
        right_lbl = create_text("Lĩnh vực ứng dụng", font_size=11, color=GREEN_A).move_to(right_box.get_center() + UP * 0.5)
        right_desc = create_markup_text(
            "• Chơi cờ Go (AlphaGo)\n• Chứng minh toán (AlphaProof)\n• Lập trình viết mã nguồn\n• AI Agents (Web / Tool)",
            font_size=9, line_spacing=1.2
        ).move_to(right_box.get_center() + DOWN * 0.25)
        arrow_right = Arrow(start=center_box.get_right(), end=right_box.get_left(), color=GREEN_B, stroke_width=1.5, buff=0.05)

        self.play(
            FadeIn(center_box), Write(center_lbl),
            run_time=1.2
        )
        self.play(
            Create(arrow_left), FadeIn(left_box), Write(left_lbl), Write(left_desc),
            Create(arrow_right), FadeIn(right_box), Write(right_lbl), Write(right_desc),
            run_time=2.0
        )
        self.wait(27.0)

        # Panel discussion recap box ở dưới đáy
        panel_box = RoundedRectangle(width=9.5, height=1.3, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.08)
        panel_box.move_to(DOWN * 2.2)
        panel_title = create_text("Nhận định từ phiên thảo luận Panel của các chuyên gia NeurIPS 2024:", font_size=10, color=GOLD_B)
        panel_title.move_to(panel_box.get_center() + UP * 0.4)
        panel_desc = create_markup_text(
            "<i>\"Inference Compute là một ranh giới vô hạn. Đối với các bài toán quan trọng nhất của nhân loại,\n"
            "người ta sẵn sàng chi trả hàng ngàn đô la cho một câu trả lời chính xác thông qua Tree Search.\"</i>  -- Noam Brown",
            font_size=9, color=WHITE, line_spacing=1.3
        ).move_to(panel_box.get_center() + DOWN * 0.25)

        self.play(
            FadeIn(panel_box),
            Write(panel_title),
            Write(panel_desc),
            run_time=2.0
        )
        self.wait(32.0)

        # Dọn dẹp kết thúc toàn bộ phân cảnh
        self.play(
            FadeOut(center_box), FadeOut(center_lbl),
            FadeOut(left_box), FadeOut(left_lbl), FadeOut(left_desc), FadeOut(arrow_left),
            FadeOut(right_box), FadeOut(right_lbl), FadeOut(right_desc), FadeOut(arrow_right),
            FadeOut(panel_box), FadeOut(panel_title), FadeOut(panel_desc),
            FadeOut(part5_title),
            FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(1.0)
