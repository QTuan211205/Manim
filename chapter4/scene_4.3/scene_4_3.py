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


class Scene4_3(Scene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH
        # =====================================================================
        chapter_title = create_text("Chương 4: Hiệu năng hệ thống (Systems Efficiency)", font_size=22, color=YELLOW)
        chapter_sub = create_text("Phần 4.3: Tối ưu hóa tiền tố dùng chung (Shared Prefix Optimizations)", font_size=16, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(8.0)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Tối ưu hóa tiền tố dùng chung (Shared Prefix)", font_size=13, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(5.0)

        # =====================================================================
        # BƯỚC 2: BÀI TOÁN TRÙNG LẶP KV CACHE & LÃNG PHÍ VRAM
        # =====================================================================
        step1_title = create_markup_text(
            "<b>1. Vấn đề dư thừa bộ nhớ KV Cache (Redundant KV Cache)</b>",
            font_size=12, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(step1_title), run_time=1.5)
        self.wait(2.0)

        # Tạo 3 Prompt Boxes đại diện cho 3 luồng sinh song song (Best-of-N)
        prompt_boxes = VGroup()
        for idx in range(3):
            box = RoundedRectangle(width=3.2, height=0.8, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            box.move_to(LEFT * (3.5 * (1 - idx)) + UP * 0.8)
            
            # System prompt dùng chung (Màu xám)
            sys_part = RoundedRectangle(width=1.8, height=0.6, color=GRAY_B, fill_color=GRAY_E, fill_opacity=0.7, corner_radius=0.03)
            sys_part.move_to(box.get_center() + LEFT * 0.55)
            sys_lbl = create_text("System Prompt (1000t)", font_size=6, color=WHITE).move_to(sys_part.get_center())
            sys_grp = VGroup(sys_part, sys_lbl)
            
            # Query riêng biệt (Màu vàng)
            query_part = RoundedRectangle(width=0.9, height=0.6, color=YELLOW_D, fill_color=YELLOW_E, fill_opacity=0.7, corner_radius=0.03)
            query_part.move_to(box.get_center() + RIGHT * 0.95)
            query_lbl = create_text(f"Query {idx+1}", font_size=6, color=WHITE).move_to(query_part.get_center())
            query_grp = VGroup(query_part, query_lbl)
            
            prompt_boxes.add(VGroup(box, sys_grp, query_grp))

        self.play(FadeIn(prompt_boxes, shift=DOWN * 0.2), run_time=1.5)
        self.wait(5.0)

        # Trực quan hóa VRAM Memory ở dưới
        vram_bg = RoundedRectangle(width=11.2, height=1.6, color=GRAY_C, fill_color="#0e0f11", fill_opacity=0.95, corner_radius=0.06)
        vram_bg.move_to(DOWN * 1.5)
        vram_title = create_text("Bộ nhớ GPU VRAM", font_size=8, color=GRAY_B).next_to(vram_bg, UP, buff=0.05, aligned_edge=LEFT).shift(RIGHT * 0.2)
        
        # 3 khối KV Cache trùng lặp được ghi vào VRAM
        vram_caches = VGroup()
        arrows = VGroup()
        for idx in range(3):
            # Khối KV Cache trong VRAM
            cache_box = RoundedRectangle(width=3.0, height=0.8, color=RED, fill_color="#2b1414", fill_opacity=0.9, corner_radius=0.04)
            cache_box.move_to(LEFT * (3.5 * (1 - idx)) + DOWN * 1.5)
            
            cache_lbl = create_markup_text(
                f"<b>KV Cache Luồng {idx+1}</b>\n<span foreground=\"#FF3333\">Có 1000t System Prompt</span>",
                font_size=6, color=WHITE, line_spacing=1.1
            ).move_to(cache_box.get_center())
            
            vram_caches.add(VGroup(cache_box, cache_lbl))
            
            # Mũi tên từ Prompt xuống VRAM
            arrow = Arrow(start=prompt_boxes[idx].get_bottom(), end=cache_box.get_top(), color=RED, stroke_width=2)
            arrows.add(arrow)

        wasted_label = create_markup_text(
            "<b>CẢNH BÁO: Lãng phí VRAM! (Wasted Memory)</b>\n"
            "System Prompt bị nhân bản làm 3 bản sao giống hệt nhau trong bộ nhớ đệm.",
            font_size=8, color=RED, line_spacing=1.2
        ).move_to(DOWN * 2.6)

        self.play(
            FadeIn(vram_bg), FadeIn(vram_title),
            run_time=1.0
        )
        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2),
            LaggedStart(*[FadeIn(c, shift=DOWN*0.1) for c in vram_caches], lag_ratio=0.2),
            run_time=1.5
        )
        self.play(Write(wasted_label), run_time=1.2)
        self.wait(35.0)

        # Dọn dẹp Step 1
        self.play(
            FadeOut(step1_title),
            FadeOut(prompt_boxes),
            FadeOut(vram_caches),
            FadeOut(arrows),
            FadeOut(wasted_label),
            FadeOut(vram_bg), FadeOut(vram_title),
            run_time=1.0
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 3: CƠ CHẾ PAGEDATTENTION (vLLM)
        # =====================================================================
        step2_title = create_markup_text(
            "<b>2. Giải pháp PagedAttention (vLLM) — Chia sẻ block vật lý</b>",
            font_size=12, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(step2_title), run_time=1.2)
        self.wait(2.0)

        # 3 Block logic ở bên trái
        logical_blocks = VGroup()
        for idx in range(3):
            lbl_box = RoundedRectangle(width=2.5, height=0.5, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.03)
            lbl_box.move_to(LEFT * 3.5 + UP * (0.6 - 0.7 * idx))
            lbl_txt = create_text(f"Block Logic {idx+1}", font_size=8, color=WHITE).move_to(lbl_box.get_center())
            logical_blocks.add(VGroup(lbl_box, lbl_txt))
            
        # 1 Block vật lý ở bên phải đại diện cho phần dùng chung
        physical_block = RoundedRectangle(width=3.2, height=1.0, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.04)
        physical_block.move_to(RIGHT * 2.5 + UP * 0.0)
        physical_lbl = create_markup_text(
            "<b>Block Vật Lý (Physical Block)</b>\n<span foreground=\"#33FF55\">Lưu duy nhất 1 bản KV Cache\ncủa System Prompt trong VRAM</span>",
            font_size=6.5, color=WHITE, line_spacing=1.2
        ).move_to(physical_block.get_center())
        physical_grp = VGroup(physical_block, physical_lbl)

        # Mapping arrows
        mapping_arrows = VGroup()
        for idx in range(3):
            arrow = Arrow(start=logical_blocks[idx].get_right(), end=physical_block.get_left(), color=GREEN, stroke_width=2)
            mapping_arrows.add(arrow)

        paged_note = create_markup_text(
            "PagedAttention hoạt động như <b>Bộ nhớ ảo (Virtual Memory)</b>:\n"
            "Ánh xạ nhiều luồng yêu cầu logic về cùng một khối bộ nhớ vật lý dùng chung.\n"
            "<span foreground=\"#33FF55\">=> Tiết kiệm bộ nhớ vượt trội, cho phép tăng kích thước Batch Size.</span>",
            font_size=8, color=WHITE, line_spacing=1.3
        ).move_to(DOWN * 1.8)

        self.play(
            FadeIn(logical_blocks, shift=RIGHT * 0.2),
            FadeIn(physical_grp, shift=LEFT * 0.2),
            run_time=1.5
        )
        self.play(
            LaggedStart(*[Create(a) for a in mapping_arrows], lag_ratio=0.25),
            run_time=1.2
        )
        self.play(Write(paged_note), run_time=1.5)
        self.wait(35.0)

        # Dọn dẹp Step 2
        self.play(
            FadeOut(step2_title),
            FadeOut(logical_blocks),
            FadeOut(physical_grp),
            FadeOut(mapping_arrows),
            FadeOut(paged_note),
            run_time=1.0
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 4: RADIXATTENTION (SGLANG) & CÂY TIỀN TỐ (RADIX TREE)
        # =====================================================================
        step3_title = create_markup_text(
            "<b>3. RadixAttention (SGLang) — Cây tiền tố đa cấp &amp; LRU Eviction</b>",
            font_size=12, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(step3_title), run_time=1.2)
        self.wait(2.0)

        # Vẽ cấu trúc cây Radix
        # Nút gốc (Root): System Prompt
        root_rect = RoundedRectangle(width=3.6, height=0.55, color=BLUE, fill_color="#14202b", fill_opacity=0.9, corner_radius=0.04)
        root_rect.move_to(UP * 1.0)
        root_lbl = create_text("Root: System Prompt (1000t)", font_size=8, color=BLUE_A).move_to(root_rect.get_center())
        root_node = VGroup(root_rect, root_lbl)

        # Nút con cấp 1: Few-shot Examples
        fewshot_rect = RoundedRectangle(width=3.2, height=0.5, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.04)
        fewshot_rect.move_to(UP * 0.0)
        fewshot_lbl = create_text("Few-shot Examples (500t)", font_size=8, color=GREEN_A).move_to(fewshot_rect.get_center())
        fewshot_node = VGroup(fewshot_rect, fewshot_lbl)

        # Nút con cấp 2: Câu hỏi (Queries)
        qa_rect = RoundedRectangle(width=2.0, height=0.45, color=YELLOW, fill_color="#2b2b14", fill_opacity=0.9, corner_radius=0.03)
        qa_rect.move_to(LEFT * 2.4 + DOWN * 0.9)
        qa_lbl = create_text("Question A (100t)", font_size=7, color=YELLOW_A).move_to(qa_rect.get_center())
        qa_node = VGroup(qa_rect, qa_lbl)

        qb_rect = RoundedRectangle(width=2.0, height=0.45, color=YELLOW, fill_color="#2b2b14", fill_opacity=0.9, corner_radius=0.03)
        qb_rect.move_to(RIGHT * 2.4 + DOWN * 0.9)
        qb_lbl = create_text("Question B (100t)", font_size=7, color=YELLOW_A).move_to(qb_rect.get_center())
        qb_node = VGroup(qb_rect, qb_lbl)

        # Nút lá cấp 3: Câu trả lời sinh ra (Answers)
        ansa1_rect = RoundedRectangle(width=1.6, height=0.4, color=ORANGE, fill_color="#2b2014", fill_opacity=0.9, corner_radius=0.03)
        ansa1_rect.move_to(LEFT * 3.4 + DOWN * 1.8)
        ansa1_lbl = create_text("Answer A1 (Candidate)", font_size=6, color=ORANGE).move_to(ansa1_rect.get_center())
        ansa1_node = VGroup(ansa1_rect, ansa1_lbl)

        ansa2_rect = RoundedRectangle(width=1.6, height=0.4, color=ORANGE, fill_color="#2b2014", fill_opacity=0.9, corner_radius=0.03)
        ansa2_rect.move_to(LEFT * 1.4 + DOWN * 1.8)
        ansa2_lbl = create_text("Answer A2 (Candidate)", font_size=6, color=ORANGE).move_to(ansa2_rect.get_center())
        ansa2_node = VGroup(ansa2_rect, ansa2_lbl)

        ansb1_rect = RoundedRectangle(width=1.6, height=0.4, color=ORANGE, fill_color="#2b2014", fill_opacity=0.9, corner_radius=0.03)
        ansb1_rect.move_to(RIGHT * 2.4 + DOWN * 1.8)
        ansb1_lbl = create_text("Answer B1 (Candidate)", font_size=6, color=ORANGE).move_to(ansb1_rect.get_center())
        ansb1_node = VGroup(ansb1_rect, ansb1_lbl)

        # Các đường nối (Connection lines)
        line_root_few = Line(root_rect.get_bottom(), fewshot_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_few_qa = Line(fewshot_rect.get_bottom(), qa_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_few_qb = Line(fewshot_rect.get_bottom(), qb_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_qa_ansa1 = Line(qa_rect.get_bottom(), ansa1_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_qa_ansa2 = Line(qa_rect.get_bottom(), ansa2_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_qb_ansb1 = Line(qb_rect.get_bottom(), ansb1_rect.get_top(), color=GRAY_C, stroke_width=1.5)

        tree_lines = VGroup(line_root_few, line_few_qa, line_few_qb, line_qa_ansa1, line_qa_ansa2, line_qb_ansb1)
        tree_nodes = VGroup(root_node, fewshot_node, qa_node, qb_node, ansa1_node, ansa2_node, ansb1_node)

        # Hiện cây
        self.play(
            LaggedStart(
                *[Create(l) for l in tree_lines],
                *[FadeIn(n) for n in tree_nodes],
                lag_ratio=0.1
            ),
            run_time=2.0
        )
        self.wait(8.0)

        # Hoạt họa hạt sáng chuyển động (Kiểm tra và tái sử dụng tiền tố)
        search_dot = Dot(color=YELLOW, radius=0.08)
        search_dot.move_to(root_rect.get_center())
        
        self.play(FadeIn(search_dot), run_time=0.4)
        self.play(search_dot.animate.move_to(fewshot_rect.get_center()), run_time=0.8)
        self.play(search_dot.animate.move_to(qa_rect.get_center()), run_time=0.8)
        self.play(search_dot.animate.move_to(ansa1_rect.get_center()), run_time=0.8)
        self.play(FadeOut(search_dot), run_time=0.4)
        self.wait(12.0)

        # Giải thích RadixTree giữ nguyên root và thu hồi lá (LRU Eviction)
        evict_lbl = create_markup_text(
            "<b>Cơ chế LRU Eviction:</b> Khi bộ nhớ đầy, các nút lá ít truy cập nhất\n"
            "sẽ bị thu hồi trước (ví dụ <b>Answer B1</b>) để nhường chỗ cho yêu cầu mới.",
            font_size=8, color=RED, line_spacing=1.25
        ).move_to(DOWN * 2.5)
        
        self.play(Write(evict_lbl), run_time=1.2)
        self.wait(2.0)

        # Lá B1 đổi màu đỏ để biểu thị chuẩn bị thu hồi
        self.play(
            ansb1_rect.animate.set_color(RED).set_fill(RED, opacity=0.3),
            ansb1_lbl.animate.set_color(RED),
            run_time=0.8
        )
        self.play(Flash(ansb1_rect, color=RED, num_lines=8, flash_radius=0.4), run_time=0.8)
        
        # Biến mất lá B1 và đường nối tương ứng
        self.play(
            FadeOut(ansb1_node),
            FadeOut(line_qb_ansb1),
            run_time=1.0
        )
        self.wait(25.0)

        # Dọn dẹp Step 3
        self.play(
            FadeOut(step3_title),
            FadeOut(tree_nodes),
            FadeOut(tree_lines),
            FadeOut(evict_lbl),
            run_time=1.0
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 5: CƠ CHẾ TĂNG TỐC HYDRAGEN & ĐỒ THỊ HIỆU NĂNG
        # =====================================================================
        step4_title = create_text("4. Tận dụng Tensor Cores: Cơ chế của Hydragen", font_size=13, color=YELLOW)
        step4_title.to_edge(UP, buff=0.4)
        self.play(ReplacementTransform(sub_title, step4_title), run_time=1.0)
        self.wait(2.0)

        # --- PHẦN 1: CÔNG THỨC SO SÁNH (BÊN TRÁI) ---
        formula_left_margin = -3.8
        
        # 1. Truyền thống
        trad_title = create_text("1. Phương pháp truyền thống (vLLM / SGLang):", font_size=9, color=RED).move_to(LEFT * 3.5 + UP * 1.3, aligned_edge=LEFT)
        trad_formula = create_markup_text(
            "<span foreground=\"#FF3333\">q<sub>i</sub> * K<sup>T</sup></span>  (cho từng luồng <i>i</i>)",
            font_size=9.5, font="Consolas"
        ).next_to(trad_title, DOWN, buff=0.15, aligned_edge=LEFT)
        
        trad_desc = create_markup_text(
            "• Phép nhân <b>Ma Trận - Vector</b> độc lập.\n"
            "• KV Cache của tiền tố phải tải từ VRAM vào\n"
            "  bộ xử lý nhiều lần (bị giới hạn <i>Memory-bound</i>).",
            font_size=7, color=GRAY_A, line_spacing=1.2
        ).next_to(trad_formula, DOWN, buff=0.15, aligned_edge=LEFT)

        trad_grp = VGroup(trad_title, trad_formula, trad_desc)

        # 2. Hydragen
        hydra_title = create_text("2. Giải pháp của Hydragen:", font_size=9, color=GREEN).move_to(LEFT * 3.5 + DOWN * 0.5, aligned_edge=LEFT)
        hydra_formula = create_markup_text(
            "<span foreground=\"#33FF55\">Q<sub>batch</sub> * K<sup>T</sup></span>  (Matrix-Matrix)",
            font_size=9.5, font="Consolas"
        ).next_to(hydra_title, DOWN, buff=0.15, aligned_edge=LEFT)
        
        hydra_desc = create_markup_text(
            "• Gộp truy vấn của các luồng thành ma trận <b>Q</b>.\n"
            "• Tải KV Cache của tiền tố vào thanh ghi đúng 1 lần.\n"
            "• Phép nhân <b>Ma Trận - Ma Trận</b> cực nhanh nhờ\n"
            "  tận dụng lõi <b>Tensor Cores</b> (<i>Compute-bound</i>).",
            font_size=7, color=GRAY_A, line_spacing=1.2
        ).next_to(hydra_formula, DOWN, buff=0.15, aligned_edge=LEFT)

        hydra_grp = VGroup(hydra_title, hydra_formula, hydra_desc)

        # --- PHẦN 2: ĐỒ THỊ HIỆU NĂNG (BÊN PHẢI) ---
        axes = Axes(
            x_range=[0, 8, 2],
            y_range=[0, 8, 2],
            x_length=4.5,
            y_length=3.0,
            axis_config={"color": GRAY_C, "stroke_width": 2},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        ).move_to(RIGHT * 3.2 + DOWN * 0.4)

        # Nhãn đồ thị
        graph_title = create_text("Thông lượng (Throughput) vs. Batch Size", font_size=8.5, color=YELLOW).next_to(axes, UP, buff=0.2)
        x_lbl = create_text("Batch Size", font_size=7, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.15)
        y_lbl = create_text("Throughput", font_size=7, color=GRAY_A).next_to(axes.y_axis, LEFT, buff=0.15).rotate(90 * DEGREES)

        # Curves
        # 1. vLLM (Màu đỏ)
        vllm_curve = axes.plot(lambda x: 0.5 + 0.9 * (x**0.55), x_range=[0, 8], color=RED, stroke_width=3)
        # 2. Hydragen (Màu xanh lá)
        hydragen_curve = axes.plot(lambda x: 0.5 + 1.8 * (x**0.65), x_range=[0, 8], color=GREEN, stroke_width=4)
        # 3. Upper Bound (Đường đứt nét màu xanh dương)
        upper_bound = DashedLine(
            start=axes.c2p(0, 7.2), end=axes.c2p(8, 7.2),
            color=BLUE, stroke_width=2
        )
        upper_lbl = create_text("Giới hạn lý thuyết (Attention-free)", font_size=6, color=BLUE).next_to(upper_bound, UP, buff=0.05).shift(LEFT * 0.4)

        # Legend chú thích
        leg_vllm_line = Line(start=LEFT*0.15, end=RIGHT*0.15, color=RED, stroke_width=3)
        leg_vllm_txt = create_text("vLLM (PagedAttention)", font_size=6.5, color=RED)
        leg_vllm = VGroup(leg_vllm_line, leg_vllm_txt).arrange(RIGHT, buff=0.1)

        leg_hydra_line = Line(start=LEFT*0.15, end=RIGHT*0.15, color=GREEN, stroke_width=4)
        leg_hydra_txt = create_text("Hydragen", font_size=6.5, color=GREEN)
        leg_hydra = VGroup(leg_hydra_line, leg_hydra_txt).arrange(RIGHT, buff=0.1)

        legend = VGroup(leg_vllm, leg_hydra).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        legend.move_to(axes.c2p(0.8, 5.5))

        self.play(
            FadeIn(trad_grp, shift=RIGHT * 0.25),
            run_time=1.5
        )
        self.wait(15.0)

        self.play(
            FadeIn(hydra_grp, shift=RIGHT * 0.25),
            run_time=1.5
        )
        self.wait(20.0)

        self.play(
            Create(axes), Write(graph_title), Write(x_lbl), Write(y_lbl),
            run_time=1.5
        )
        self.play(
            Create(vllm_curve), Create(hydragen_curve),
            Create(upper_bound), FadeIn(upper_lbl),
            FadeIn(legend),
            run_time=2.0
        )
        self.wait(40.0)

        # Dọn dẹp Step 4 để sang Step 5
        self.play(
            FadeOut(trad_grp), FadeOut(hydra_grp),
            FadeOut(axes), FadeOut(graph_title), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(vllm_curve), FadeOut(hydragen_curve),
            FadeOut(upper_bound), FadeOut(upper_lbl),
            FadeOut(legend),
            FadeOut(step4_title),
            run_time=1.2
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 5: KỸ THUẬT LOẠI BỎ TOKEN (TOKEN DROPPING)
        # =====================================================================
        step5_title = create_text("5. Loại bỏ Token (Token Dropping)", font_size=13, color=YELLOW)
        step5_title.to_edge(UP, buff=0.4)
        self.play(Write(step5_title), run_time=1.0)
        self.wait(2.0)

        # Hiển thị công thức tính kích thước KV Cache (Tránh dùng VGroup chứa label khi cần Transform để tránh lỗi đè chữ)
        formula_bg = RoundedRectangle(width=8.5, height=0.6, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04).move_to(UP * 1.0)
        formula_lbl = create_markup_text(
            'Size = (batch * <span foreground="#FF3333">n<sub>ctx</sub></span>) * (2 * n<sub>layer</sub> * n<sub>heads</sub> * head<sub>dim</sub>) * n<sub>bytes</sub>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeIn(formula_bg, shift=DOWN * 0.2), FadeIn(formula_lbl, shift=DOWN * 0.2), run_time=1.2)
        self.wait(3.5)

        # Vẽ hàng token KV Cache
        tokens = VGroup()
        for i in range(8):
            tok = RoundedRectangle(width=0.8, height=0.65, color=GRAY_D, fill_color="#1e2025", fill_opacity=0.9, corner_radius=0.04)
            tok.move_to(LEFT * (3.5 - 1.0 * i) + DOWN * 0.2)
            lbl = create_text(f"T{i+1}", font_size=8, color=WHITE).move_to(tok.get_center())
            tokens.add(VGroup(tok, lbl))
        self.play(FadeIn(tokens, shift=UP * 0.1), run_time=1.2)
        self.wait(2.5)

        # Hiện attention scores
        scores = [0.05, 0.42, 0.08, 0.35, 0.03, 0.51, 0.07, 0.48]
        score_labels = VGroup()
        for i, s in enumerate(scores):
            col = RED if s < 0.1 else GREEN
            score_lbl = create_text(f"{s:.2f}", font_size=7, color=col).next_to(tokens[i], DOWN, buff=0.1)
            score_labels.add(score_lbl)
        self.play(FadeIn(score_labels, shift=UP * 0.15), run_time=1.0)
        self.wait(5.0)

        # Chọn và loại bỏ các token kém quan trọng (T1, T3, T5, T7)
        drop_indices = [0, 2, 4, 6]
        self.play(
            *[tokens[idx][0].animate.set_color(RED).set_fill(RED, opacity=0.3) for idx in drop_indices],
            run_time=0.8
        )
        self.wait(1.5)
        self.play(
            *[FadeOut(tokens[idx]) for idx in drop_indices],
            *[FadeOut(score_labels[idx]) for idx in drop_indices],
            run_time=1.0
        )
        self.wait(1.5)

        # Di chuyển các token còn lại sát lại với nhau
        keep_indices = [1, 3, 5, 7]
        self.play(
            *[tokens[idx].animate.move_to(LEFT * (1.5 - 1.0 * i) + DOWN * 0.2) for i, idx in enumerate(keep_indices)],
            *[score_labels[idx].animate.move_to(LEFT * (1.5 - 1.0 * i) + DOWN * 0.7) for i, idx in enumerate(keep_indices)],
            run_time=1.2
        )
        self.wait(3.0)

        # Cập nhật công thức: n_ctx giảm (sử dụng FadeOut/FadeIn an toàn tránh lỗi chồng chữ)
        formula_lbl_new = create_markup_text(
            'Size = (batch * <span foreground="#FF3333">n<sub>ctx</sub> (giảm 50%)</span>) * (2 * n<sub>layer</sub> * n<sub>heads</sub> * head<sub>dim</sub>) * n<sub>bytes</sub>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeOut(formula_lbl), FadeIn(formula_lbl_new), run_time=0.8)
        formula_lbl = formula_lbl_new
        self.wait(4.0)

        # Nhãn hạn chế cảnh báo
        warning_box = RoundedRectangle(width=9.5, height=0.75, color=ORANGE, fill_color="#2b1b14", fill_opacity=0.9, corner_radius=0.04).move_to(DOWN * 1.9)
        warning_lbl = create_markup_text(
            '<b>Hạn chế:</b> Mô hình dễ bị mất ngữ cảnh (brittle) nếu loại bỏ nhầm token quan trọng\n'
            'hoặc khi nội dung thảo luận thay đổi đột ngột (do đã xóa vector KV Cache tương ứng).',
            font_size=7, color=WHITE, line_spacing=1.2
        ).move_to(warning_box.get_center())
        warning_grp = VGroup(warning_box, warning_lbl)
        self.play(FadeIn(warning_grp, shift=UP * 0.2), run_time=1.2)
        self.wait(28.0)

        # Dọn dẹp Step 5
        self.play(
            FadeOut(step5_title), FadeOut(formula_bg), FadeOut(formula_lbl),
            *[FadeOut(tokens[idx]) for idx in keep_indices],
            *[FadeOut(score_labels[idx]) for idx in keep_indices],
            FadeOut(warning_grp),
            run_time=1.0
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 6: LƯỢNG TỬ HÓA BỘ NHỚ ĐỆM (QUANTIZATION)
        # =====================================================================
        step6_title = create_text("6. Lượng tử hóa bộ nhớ đệm (KV Cache Quantization)", font_size=13, color=YELLOW)
        step6_title.to_edge(UP, buff=0.4)
        self.play(Write(step6_title), run_time=1.0)
        self.wait(2.0)

        # Công thức nổi bật n_bytes
        formula_bg = RoundedRectangle(width=8.5, height=0.6, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04).move_to(UP * 1.0)
        formula_lbl = create_markup_text(
            'Size = (batch * n<sub>ctx</sub>) * (2 * n<sub>layer</sub> * n<sub>heads</sub> * head<sub>dim</sub>) * <span foreground="#33FF55">n<sub>bytes</sub></span>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeIn(formula_bg, shift=DOWN * 0.2), FadeIn(formula_lbl, shift=DOWN * 0.2), run_time=1.2)
        self.wait(3.5)

        # Vẽ khối dữ liệu nén
        fp16_box = RoundedRectangle(width=3.6, height=0.8, color=BLUE, fill_color="#14202b", fill_opacity=0.9, corner_radius=0.04).move_to(LEFT * 2.2 + DOWN * 0.3)
        fp16_lbl = create_markup_text("<b>FP16 (2 Bytes)</b>\nĐộ chính xác cao ban đầu", font_size=7.5, color=WHITE).move_to(fp16_box.get_center())
        fp16_grp = VGroup(fp16_box, fp16_lbl)
        self.play(FadeIn(fp16_grp, shift=RIGHT * 0.25), run_time=1.2)
        self.wait(3.0)

        arrow = Arrow(start=fp16_box.get_right(), end=RIGHT * 0.2 + DOWN * 0.3, color=GREEN, stroke_width=2.5)
        
        int8_box = RoundedRectangle(width=1.8, height=0.8, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.04).move_to(RIGHT * 1.3 + DOWN * 0.3)
        int8_lbl = create_markup_text("<b>INT8 (1B)</b>\nNén 2x", font_size=7, color=WHITE).move_to(int8_box.get_center())
        int8_grp = VGroup(int8_box, int8_lbl)

        int4_box = RoundedRectangle(width=0.9, height=0.8, color=YELLOW, fill_color="#2b2b14", fill_opacity=0.9, corner_radius=0.04).move_to(RIGHT * 3.1 + DOWN * 0.3)
        int4_lbl = create_markup_text("<b>INT4</b>\nNén 4x", font_size=6, color=WHITE).move_to(int4_box.get_center())
        int4_grp = VGroup(int4_box, int4_lbl)

        self.play(Create(arrow), FadeIn(int8_grp, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(int4_grp, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(3.0)

        # Cập nhật công thức: n_bytes giảm (sử dụng FadeOut/FadeIn tránh lỗi đè chữ)
        formula_lbl_new = create_markup_text(
            'Size = (batch * n<sub>ctx</sub>) * (2 * n<sub>layer</sub> * n<sub>heads</sub> * head<sub>dim</sub>) * <span foreground="#33FF55">n<sub>bytes</sub> (giảm 2x - 4x)</span>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeOut(formula_lbl), FadeIn(formula_lbl_new), run_time=0.8)
        formula_lbl = formula_lbl_new
        self.wait(4.0)

        # Hộp nhãn lợi ích
        benefit_box = RoundedRectangle(width=9.5, height=0.75, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.04).move_to(DOWN * 1.9)
        benefit_lbl = create_markup_text(
            '<b>Lợi ích:</b> Cho phép lưu trữ nhiều vector KV Cache hơn trên cùng 1 GPU.\n'
            '<span foreground="#33FF55">=> Vận hành Batch Size lớn hơn, tăng thông lượng (Throughput) tối đa.</span>',
            font_size=7, color=WHITE, line_spacing=1.2
        ).move_to(benefit_box.get_center())
        benefit_grp = VGroup(benefit_box, benefit_lbl)
        self.play(FadeIn(benefit_grp, shift=UP * 0.2), run_time=1.2)
        self.wait(26.0)

        # Dọn dẹp Step 6
        self.play(
            FadeOut(step6_title), FadeOut(formula_bg), FadeOut(formula_lbl),
            FadeOut(fp16_grp), FadeOut(arrow), FadeOut(int8_grp), FadeOut(int4_grp),
            FadeOut(benefit_grp),
            run_time=1.0
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 7: THAY ĐỔI KIẾN TRÚC MÔ HÌNH (MQA VS. GQA)
        # =====================================================================
        step7_title = create_text("7. Tối ưu cấu trúc: Multi-Query & Grouped-Query Attention", font_size=13, color=YELLOW)
        step7_title.to_edge(UP, buff=0.4)
        self.play(Write(step7_title), run_time=1.0)
        self.wait(2.0)

        # Công thức nổi bật n_heads
        formula_bg = RoundedRectangle(width=8.5, height=0.6, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04).move_to(UP * 1.1)
        formula_lbl = create_markup_text(
            'Size = (batch * n<sub>ctx</sub>) * (2 * n<sub>layer</sub> * <span foreground="#33CCFF">n<sub>heads</sub></span> * head<sub>dim</sub>) * n<sub>bytes</sub>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeIn(formula_bg, shift=DOWN * 0.2), FadeIn(formula_lbl, shift=DOWN * 0.2), run_time=1.2)
        self.wait(3.5)

        # Vẽ 3 cột so sánh kiến trúc
        # Cột MHA
        mha_lbl = create_text("MHA (Truyền thống)", font_size=7, color=WHITE).move_to(LEFT * 4.0 + UP * 0.25)
        mha_q_heads = VGroup(*[Circle(radius=0.08, color=ORANGE, fill_color=ORANGE, fill_opacity=0.8).move_to(LEFT * 4.4 + UP * (0.0 - 0.25 * j)) for j in range(4)])
        mha_kv_heads = VGroup(*[Circle(radius=0.08, color=GREEN, fill_color=GREEN, fill_opacity=0.8).move_to(LEFT * 3.6 + UP * (0.0 - 0.25 * j)) for j in range(4)])
        mha_lines = VGroup(*[Line(mha_q_heads[j].get_right(), mha_kv_heads[j].get_left(), color=GRAY_B, stroke_width=1.2) for j in range(4)])
        mha_grp = VGroup(mha_lbl, mha_q_heads, mha_kv_heads, mha_lines)

        # Cột MQA
        mqa_lbl = create_text("MQA (Multi-Query)", font_size=7, color=WHITE).move_to(UP * 0.25)
        mqa_q_heads = VGroup(*[Circle(radius=0.08, color=ORANGE, fill_color=ORANGE, fill_opacity=0.8).move_to(LEFT * 0.4 + UP * (0.0 - 0.25 * j)) for j in range(4)])
        mqa_kv_heads = VGroup(Circle(radius=0.08, color=GREEN, fill_color=GREEN, fill_opacity=0.8).move_to(RIGHT * 0.4 - UP * 0.38))
        mqa_lines = VGroup(*[Line(mqa_q_heads[j].get_right(), mqa_kv_heads[0].get_left(), color=GRAY_B, stroke_width=1.2) for j in range(4)])
        mqa_grp = VGroup(mqa_lbl, mqa_q_heads, mqa_kv_heads, mqa_lines)

        # Cột GQA
        gqa_lbl = create_text("GQA (Grouped-Query)", font_size=7, color=WHITE).move_to(RIGHT * 4.0 + UP * 0.25)
        gqa_q_heads = VGroup(*[Circle(radius=0.08, color=ORANGE, fill_color=ORANGE, fill_opacity=0.8).move_to(RIGHT * 3.6 + UP * (0.0 - 0.25 * j)) for j in range(4)])
        gqa_kv_heads = VGroup(*[Circle(radius=0.08, color=GREEN, fill_color=GREEN, fill_opacity=0.8).move_to(RIGHT * 4.4 + UP * (-0.12 - 0.5 * j)) for j in range(2)])
        gqa_lines = VGroup(
            Line(gqa_q_heads[0].get_right(), gqa_kv_heads[0].get_left(), color=GRAY_B, stroke_width=1.2),
            Line(gqa_q_heads[1].get_right(), gqa_kv_heads[0].get_left(), color=GRAY_B, stroke_width=1.2),
            Line(gqa_q_heads[2].get_right(), gqa_kv_heads[1].get_left(), color=GRAY_B, stroke_width=1.2),
            Line(gqa_q_heads[3].get_right(), gqa_kv_heads[1].get_left(), color=GRAY_B, stroke_width=1.2)
        )
        gqa_grp = VGroup(gqa_lbl, gqa_q_heads, gqa_kv_heads, gqa_lines)

        self.play(FadeIn(mha_grp, shift=UP*0.1), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(mqa_grp, shift=UP*0.1), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(gqa_grp, shift=UP*0.1), run_time=1.2)
        self.wait(3.0)

        # Cập nhật công thức: n_heads giảm (sử dụng FadeOut/FadeIn tránh lỗi đè chữ)
        formula_lbl_new = create_markup_text(
            'Size = (batch * n<sub>ctx</sub>) * (2 * n<sub>layer</sub> * <span foreground="#33CCFF">n<sub>heads</sub> (giảm 4x - 8x)</span> * head<sub>dim</sub>) * n<sub>bytes</sub>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeOut(formula_lbl), FadeIn(formula_lbl_new), run_time=0.8)
        formula_lbl = formula_lbl_new
        self.wait(4.0)

        # Hộp nhãn giải thích
        arch_note = create_markup_text(
            'MQA và GQA chia sẻ đầu <b>Key và Value</b> cho nhiều đầu Query khác nhau.\n'
            '<span foreground="#33CCFF">=> Thu nhỏ dung lượng KV Cache sinh ra đáng kể cho mỗi sequence ngữ cảnh dài.</span>',
            font_size=7.5, color=WHITE, line_spacing=1.25
        ).move_to(DOWN * 1.9)
        self.play(Write(arch_note), run_time=1.2)
        self.wait(32.0)

        # Dọn dẹp Step 7
        self.play(
            FadeOut(step7_title), FadeOut(formula_bg), FadeOut(formula_lbl),
            FadeOut(mha_grp), FadeOut(mqa_grp), FadeOut(gqa_grp), FadeOut(arch_note),
            run_time=1.0
        )
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 8: TỔNG KẾT & ĐÁNH GIÁ HIỆU NĂNG META-GENERATOR
        # =====================================================================
        step8_title = create_text("8. Tổng kết: Đánh giá hiệu năng Meta-generator", font_size=13, color=YELLOW)
        step8_title.to_edge(UP, buff=0.4)
        self.play(Write(step8_title), run_time=1.0)
        self.wait(2.0)

        # Bảng so sánh
        header_box = RoundedRectangle(width=10.0, height=0.55, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.03).move_to(UP * 1.0)
        header_txt = create_markup_text("<b>Thuật toán</b>  |  <b>Song song hóa (Parallelizable)</b>  |  <b>Chia sẻ tiền tố (Prefix-shareable)</b>", font_size=7.5, color=WHITE).move_to(header_box.get_center())
        header_grp = VGroup(header_box, header_txt)

        row1_box = RoundedRectangle(width=10.0, height=0.5, color=GRAY_E, fill_color="#111215", fill_opacity=0.8, corner_radius=0.02).move_to(UP * 0.45)
        row1_txt = create_markup_text("Chained (Chuỗi)  |  ❌ Không (Tuần tự)  |  ❌ Không", font_size=7, color=WHITE).move_to(row1_box.get_center())

        row2_box = RoundedRectangle(width=10.0, height=0.5, color=GRAY_E, fill_color="#111215", fill_opacity=0.8, corner_radius=0.02).move_to(DOWN * 0.1)
        row2_txt = create_markup_text("Parallel (Song song)  |   Có (Tối đa)  |   Có (Tốt)", font_size=7, color=WHITE).move_to(row2_box.get_center())

        row3_box = RoundedRectangle(width=10.0, height=0.5, color=GRAY_E, fill_color="#111215", fill_opacity=0.8, corner_radius=0.02).move_to(DOWN * 0.65)
        row3_txt = create_markup_text("Tree Search (Cây)  |  ⚠️ Bán song song  |   Có (Rất cao)", font_size=7, color=WHITE).move_to(row3_box.get_center())

        row4_box = RoundedRectangle(width=10.0, height=0.5, color=GRAY_E, fill_color="#111215", fill_opacity=0.8, corner_radius=0.02).move_to(DOWN * 1.2)
        row4_txt = create_markup_text("Refinement (Tinh chỉnh)  |  ❌ Không (Tuần tự)  |  ❌ Không", font_size=7, color=WHITE).move_to(row4_box.get_center())

        table = VGroup(header_grp, row1_box, row1_txt, row2_box, row2_txt, row3_box, row3_txt, row4_box, row4_txt)
        self.play(FadeIn(table, shift=UP*0.1), run_time=1.5)
        self.wait(6.0)

        # Dòng kết luận quote
        quote_box = RoundedRectangle(width=10.0, height=0.65, color=YELLOW_D, fill_color="#201c14", fill_opacity=0.9, corner_radius=0.04).move_to(DOWN * 2.05)
        quote_lbl = create_markup_text(
            '<b>Thông điệp:</b> Ngân sách token chỉ là sự đơn giản hóa! Cấu trúc câu nhắc (prompt)\n'
            'và cơ chế tối ưu hóa hệ thống quyết định phần lớn hiệu năng suy luận thực tế.',
            font_size=7.5, color=YELLOW_A, line_spacing=1.2
        ).move_to(quote_box.get_center())
        quote_grp = VGroup(quote_box, quote_lbl)
        self.play(FadeIn(quote_grp, shift=UP * 0.15), run_time=1.2)
        self.wait(28.0)

        # Dọn dẹp Step 8
        self.play(FadeOut(step8_title), FadeOut(table), FadeOut(quote_grp), run_time=1.0)
        self.wait(1.5)

        # =====================================================================
        # BƯỚC 9: HƯỚNG PHÁT TRIỂN TƯƠNG LAI (LOOKING AHEAD)
        # =====================================================================
        step9_title = create_text("9. Hướng phát triển tương lai (Looking Ahead)", font_size=13, color=YELLOW)
        step9_title.to_edge(UP, buff=0.4)
        self.play(Write(step9_title), run_time=1.0)
        self.wait(2.0)

        # Các gạch đầu dòng
        bullets = VGroup(
            create_markup_text("• <b>Hệ thống lai (Hybrid Systems):</b> Phối hợp song song và cải thiện tuần tự (ví dụ: AlphaVerus).", font_size=7.5),
            create_markup_text("• <b>Học cách tự tìm kiếm (Learning to search):</b> LLM tự khám phá, quay lui (backtrack) và tự sửa lỗi.", font_size=7.5),
            create_markup_text("• <b>Tối ưu hóa Agent:</b> Tương tác động với môi trường bên ngoài và nhận phản hồi đa chiều.", font_size=7.5),
            create_markup_text("• <b>Phân bổ Compute:</b> Quyết định chi phí tính toán linh hoạt thích ứng cho câu khó/dễ.", font_size=7.5)
        )
        bullets.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(UP * 0.1 + LEFT * 0.2)

        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT*0.2) for b in bullets], lag_ratio=0.5),
            run_time=2.5
        )
        self.wait(8.0)

        # Tài liệu nghiên cứu
        paper_box = RoundedRectangle(width=9.5, height=0.65, color=BLUE, fill_color="#14202b", fill_opacity=0.95, corner_radius=0.04).move_to(DOWN * 1.85)
        paper_lbl = create_markup_text(
            '<b>Tài liệu nghiên cứu:</b> Survey Paper (TMLR 2024) &amp; Code/Slides tại trang web:\n'
            '<span foreground="#33CCFF"><b>cmu-l3.github.io/neurips2024-inference-tutorial</b></span>',
            font_size=7.5, color=WHITE, line_spacing=1.2
        ).move_to(paper_box.get_center())
        paper_grp = VGroup(paper_box, paper_lbl)
        self.play(FadeIn(paper_grp, shift=UP*0.2), run_time=1.2)
        self.wait(35.0)

        # Dọn dẹp kết thúc toàn bộ
        self.play(
            FadeOut(step9_title),
            FadeOut(bullets),
            FadeOut(paper_grp),
            run_time=1.0
        )
        self.wait(2.0)
