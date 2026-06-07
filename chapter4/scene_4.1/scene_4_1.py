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


class Scene4_1(Scene):
    def construct(self):
        # Thiết lập màu nền tối đặc trưng 3B1B
        self.camera.background_color = "#111111"

        # =====================================================================
        # BƯỚC 1: TIÊU ĐỀ PHÂN CẢNH CHÍNH
        # =====================================================================
        chapter_title = create_text("Chương 4: Hiệu năng hệ thống (Systems Efficiency)", font_size=24, color=YELLOW)
        chapter_sub = create_text("Phần 4.1: Điểm nghẽn phần cứng & Bản chất của KV Cache", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(5.0)

        # Di chuyển tiêu đề lên góc trên cùng làm tiêu đề phụ
        sub_title = create_text("Điểm nghẽn phần cứng &amp; Bản chất của KV Cache", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(3.0)

        # =====================================================================
        # BƯỚC 1.2: ĐỘ TRỄ (LATENCY) VS THÔNG LƯỢNG (THROUGHPUT)
        # =====================================================================
        perf_title = create_markup_text("<b>Độ trễ (Latency) vs. Thông lượng (Throughput)</b>", font_size=14, color=YELLOW).move_to(UP * 2.0)
        
        # Thẻ Latency (Bên trái)
        card_latency = RoundedRectangle(width=4.5, height=2.4, color=BLUE_B, fill_color="#121824", fill_opacity=0.9, corner_radius=0.06)
        card_latency.move_to(LEFT * 2.8 + DOWN * 0.2)
        lbl_latency = create_markup_text(
            "<b>Độ trễ (Latency)</b>\n\n"
            "• Thời gian phản hồi cho 1 request\n"
            "• Đơn vị: mili-giây (ms)\n"
            "• Phù hợp: Trải nghiệm người dùng đơn lẻ",
            font_size=8.5, color=WHITE, line_spacing=1.3
        ).move_to(card_latency.get_center())

        # Thẻ Throughput (Bên phải)
        card_throughput = RoundedRectangle(width=4.5, height=2.4, color=GREEN_B, fill_color="#122418", fill_opacity=0.9, corner_radius=0.06)
        card_throughput.move_to(RIGHT * 2.8 + DOWN * 0.2)
        lbl_throughput = create_markup_text(
            "<b>Thông lượng (Throughput)</b>\n\n"
            "• Lượng request hoàn thành / giây\n"
            "• Đơn vị: requests/giây (RPS)\n"
            "• Phù hợp: Phục vụ số lượng lớn ở quy mô",
            font_size=8.5, color=WHITE, line_spacing=1.3
        ).move_to(card_throughput.get_center())

        self.play(
            FadeIn(perf_title),
            FadeIn(card_latency), Write(lbl_latency),
            FadeIn(card_throughput), Write(lbl_throughput),
            run_time=1.5
        )
        self.wait(8.0)

        self.play(
            FadeOut(perf_title),
            FadeOut(card_latency), FadeOut(lbl_latency),
            FadeOut(card_throughput), FadeOut(lbl_throughput),
            run_time=1.0
        )
        self.wait(1.0)

        # =====================================================================
        # BƯỚC 2: SƠ ĐỒ KHỐI PHẦN CỨNG (GPU CORE & VRAM BRIDGE)
        # =====================================================================
        intro_text = create_markup_text(
            "<b>Sơ đồ khối phần cứng &amp; Băng thông bộ nhớ</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(intro_text), run_time=1.5)
        self.wait(8.0)

        # Tạo khối GPU Core (bên trái)
        gpu_box = RoundedRectangle(width=2.8, height=2.2, color=ORANGE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        gpu_box.move_to(LEFT * 4.0 + DOWN * 0.5)
        gpu_lbl = create_text("LÕI TÍNH TOÁN GPU\n(GPU Core)", font_size=11, color=ORANGE).next_to(gpu_box, UP, buff=0.15)
        
        # Vẽ các nhân tính toán nhỏ bên trong GPU
        gpu_cores = VGroup()
        for r in range(4):
            for c in range(4):
                core = Square(side_length=0.25, color=ORANGE, fill_color=ORANGE, fill_opacity=0.2, stroke_width=1)
                core.move_to(gpu_box.get_center() + RIGHT * (c - 1.5) * 0.45 + UP * (r - 1.5) * 0.4)
                gpu_cores.add(core)

        # Tạo khối VRAM (bên phải)
        vram_box = RoundedRectangle(width=2.8, height=2.2, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        vram_box.move_to(RIGHT * 4.0 + DOWN * 0.5)
        vram_lbl = create_text("BỘ NHỚ VRAM\n(Model weights & KV Cache)", font_size=11, color=BLUE_A).next_to(vram_box, UP, buff=0.15)

        # Vẽ lưới lưu trữ trong VRAM
        vram_grids = VGroup()
        for r in range(4):
            for c in range(3):
                grid = Rectangle(width=0.6, height=0.35, color=BLUE, fill_color=BLUE_E, fill_opacity=0.15, stroke_width=1)
                grid.move_to(vram_box.get_center() + RIGHT * (c - 1.0) * 0.75 + UP * (r - 1.5) * 0.42)
                vram_grids.add(grid)

        # Cây cầu hẹp nối hai khối (Băng thông bộ nhớ)
        bridge_upper = Line(start=gpu_box.get_right() + UP * 0.3, end=vram_box.get_left() + UP * 0.3, color=GRAY, stroke_width=2.5)
        bridge_lower = Line(start=gpu_box.get_right() + DOWN * 0.3, end=vram_box.get_left() + DOWN * 0.3, color=GRAY, stroke_width=2.5)
        bridge_lbl = create_markup_text(
            "Băng thông bộ nhớ\n"
            "<span foreground=\"#888888\"><b>Memory Bandwidth (GB/s)</b></span>",
            font_size=9, color=WHITE, line_spacing=1.1
        ).move_to(DOWN * 0.5)

        self.play(
            FadeIn(gpu_box), FadeIn(gpu_lbl), FadeIn(gpu_cores),
            FadeIn(vram_box), FadeIn(vram_lbl), FadeIn(vram_grids),
            Create(bridge_upper), Create(bridge_lower), Write(bridge_lbl),
            run_time=2.0
        )
        self.wait(8.0)

        # Minh họa luồng dữ liệu (Model weights) truyền qua cầu
        packets = VGroup()
        for i in range(5):
            packet = RoundedRectangle(width=0.4, height=0.3, color=BLUE_A, fill_color=BLUE, fill_opacity=0.8, corner_radius=0.03)
            packet.move_to(vram_box.get_center())
            packets.add(packet)

        # Hiệu ứng chuyển động qua cầu từ VRAM sang GPU
        self.play(
            LaggedStart(
                *[p.animate(run_time=1.5, rate_func=linear).move_to(gpu_box.get_center()) for p in packets],
                lag_ratio=0.3
            )
        )
        # Các lõi GPU phát sáng nhẹ khi nhận dữ liệu
        self.play(
            *[c.animate(run_time=0.4).set_fill(ORANGE, opacity=0.8) for c in gpu_cores]
        )
        self.play(
            *[c.animate(run_time=0.4).set_fill(ORANGE, opacity=0.2) for c in gpu_cores],
            FadeOut(packets)
        )
        self.wait(5.0)

        # =====================================================================
        # BƯỚC 3: CÔNG THỨC CƯỜNG ĐỘ SỐ HỌC (ARITHMETIC INTENSITY)
        # =====================================================================
        self.play(FadeOut(intro_text), run_time=0.8)

        formula_title = create_text("Cường độ Số học (Arithmetic Intensity)", font_size=13, color=GOLD_B).move_to(UP * 2.3)
        formula_box = RoundedRectangle(width=8.2, height=0.55, color=GOLD_A, fill_color="#1a1814", fill_opacity=0.9, corner_radius=0.06)
        formula_box.move_to(UP * 1.4)
        
        formula_txt = create_markup_text(
            "Cường độ số học = <span foreground=\"#00FF7F\">Số lượng phép tính (FLOPs)</span> / <span foreground=\"#33AAFF\">Dung lượng nạp bộ nhớ (Bytes)</span>",
            font_size=9.5, color=WHITE
        ).move_to(formula_box.get_center())

        self.play(
            Write(formula_title),
            FadeIn(formula_box),
            Write(formula_txt),
            run_time=1.5
        )
        self.wait(8.0)

        # =====================================================================
        # BƯỚC 3.2: CÔNG THỨC THỜI GIAN TÍNH TOÁN CỦA PHÉP TOÁN
        # =====================================================================
        self.play(
            FadeOut(formula_title),
            FadeOut(formula_box),
            FadeOut(formula_txt),
            run_time=0.8
        )

        time_title = create_text("Thời gian thực thi của một phép toán", font_size=13, color=GOLD_B).move_to(UP * 2.3)
        time_box = RoundedRectangle(width=8.6, height=0.6, color=GOLD_A, fill_color="#1a1814", fill_opacity=0.9, corner_radius=0.06)
        time_box.move_to(UP * 1.4)

        time_txt = create_markup_text(
            "Time = max ( <span foreground=\"#00FF7F\">GEMM/GEMV FLOPs</span> / <span foreground=\"#00FF7F\">GPU FLOP/s</span> , <span foreground=\"#33AAFF\">Nạp Weights (GB)</span> / <span foreground=\"#33AAFF\">Băng thông VRAM (GB/s)</span> )",
            font_size=8.5, color=WHITE
        ).move_to(time_box.get_center())

        self.play(
            Write(time_title),
            FadeIn(time_box),
            Write(time_txt),
            run_time=1.5
        )
        self.wait(10.0)

        self.play(
            FadeOut(time_title),
            FadeOut(time_box),
            FadeOut(time_txt),
            run_time=0.8
        )

        # =====================================================================
        # BƯỚC 4: GIAI ĐOẠN PREFILL (COMPUTE-BOUND)
        # =====================================================================
        prefill_title = create_text(
            "Giai đoạn Prefill (Xử lý Prompt) - Compute-bound",
            font_size=13, color="#00FFFF", weight=BOLD
        ).move_to(UP * 2.2)

        prefill_math = create_markup_text(
            "- Phép toán: Nhân ma trận - ma trận (GEMM) : Q × K<sup>T</sup>\n"
            "- Chiều dài prompt T lớn ⇒ Số phép tính O(T · d<sup>2</sup>) rất lớn so với weights O(d<sup>2</sup>)\n"
            "- <b>Cường độ số học cực cao</b> ⇒ Giới hạn bởi tốc độ tính toán của nhân GPU.",
            font_size=10, color=WHITE, line_spacing=1.3
        ).move_to(UP * 1.3)

        self.play(
            Write(prefill_title),
            Write(prefill_math),
            run_time=1.5
        )
        self.wait(8.0)

        # Mô phỏng Prefill (Luồng dữ liệu dồi dào, GPU Core hoạt động hết công suất)
        prefill_packets = VGroup()
        for i in range(12):
            p = RoundedRectangle(width=0.35, height=0.25, color=BLUE_A, fill_color=BLUE_B, fill_opacity=0.9, corner_radius=0.03)
            p.move_to(vram_box.get_center() + np.array([random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), 0]))
            prefill_packets.add(p)

        prefill_anims = []
        for idx, p in enumerate(prefill_packets):
            dest_pos = gpu_box.get_center() + np.array([random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), 0])
            prefill_anims.append(p.animate(run_time=random.uniform(1.0, 1.6), rate_func=linear).move_to(dest_pos))

        gpu_status_lbl = create_text("Hiệu suất GPU: 100%\n(Nghẽn Tính Toán - Compute-bound)", font_size=10, color=GREEN).next_to(gpu_box, DOWN, buff=0.2)

        self.play(
            FadeIn(prefill_packets),
            run_time=0.5
        )
        self.play(
            *[c.animate(run_time=0.3).set_fill(ORANGE, opacity=0.9) for c in gpu_cores]
        )
        
        self.play(
            *prefill_anims,
            FadeIn(gpu_status_lbl),
            run_time=1.8
        )
        self.play(
            FadeOut(prefill_packets),
            run_time=0.5
        )
        self.wait(10.0)

        # Dọn dẹp giai đoạn Prefill
        self.play(
            FadeOut(prefill_title),
            FadeOut(prefill_math),
            FadeOut(gpu_status_lbl),
            *[c.animate(run_time=0.4).set_fill(ORANGE, opacity=0.2) for c in gpu_cores],
            run_time=0.8
        )
        self.wait(1.0)

        # =====================================================================
        # BƯỚC 5: GIAI ĐOẠN DECODE (MEMORY-BOUND)
        # =====================================================================
        decode_title = create_text(
            "Giai đoạn Decode (Sinh token tuần tự) - Memory-bound",
            font_size=13, color="#FF3333", weight=BOLD
        ).move_to(UP * 2.2)

        decode_math = create_markup_text(
            "- Phép toán: Nhân ma trận - vector (GEMV) : W × x\n"
            "- Sinh từng token (T = 1) ⇒ Phép tính O(d<sup>2</sup>), nạp bộ nhớ O(d<sup>2</sup>)\n"
            "- <b>Cường độ số học cực thấp (~1 FLOP/Byte)</b> ⇒ GPU rảnh rỗi chờ weights nạp từ VRAM.",
            font_size=10, color=WHITE, line_spacing=1.3
        ).move_to(UP * 1.3)

        self.play(
            Write(decode_title),
            Write(decode_math),
            run_time=1.5
        )
        self.wait(8.0)

        # Minh họa Decode: Nạp khối Model Weights khổng lồ từ VRAM sang GPU cực chậm
        large_weight_box = RoundedRectangle(width=1.6, height=1.3, color=BLUE_D, fill_color=BLUE_E, fill_opacity=0.9, corner_radius=0.05)
        large_weight_box.move_to(vram_box.get_center())
        large_weight_lbl = create_text("Model Weights\n(Hàng chục GB)", font_size=8, color=WHITE).move_to(large_weight_box.get_center())
        large_weight = VGroup(large_weight_box, large_weight_lbl)

        token_dot = Dot(color=YELLOW, radius=0.08).move_to(gpu_box.get_center())
        token_lbl = create_text("1 Token mới", font_size=8, color=YELLOW).next_to(token_dot, UP, buff=0.1)

        gpu_idle_lbl = create_markup_text(
            "<span foreground=\"#FF5555\"><b>GPU Nhàn Rỗi (95% Idle)</b></span>\n"
            "Đang chờ Weights từ VRAM...",
            font_size=9, color=WHITE, line_spacing=1.1
        ).next_to(gpu_box, DOWN, buff=0.2)

        self.play(
            FadeIn(large_weight),
            FadeIn(token_dot), FadeIn(token_lbl),
            run_time=1.0
        )
        self.wait(3.0)

        self.play(
            FadeOut(token_dot),
            FadeOut(token_lbl),
            run_time=0.6
        )
        self.wait(0.5)

        self.play(
            large_weight.animate(run_time=4.0, rate_func=linear).move_to(gpu_box.get_center()),
            FadeIn(gpu_idle_lbl),
            *[c.animate(run_time=0.8).set_fill(ORANGE, opacity=0.35) for c in gpu_cores],
        )
        self.play(
            *[c.animate(run_time=0.4).set_fill(ORANGE, opacity=0.2) for c in gpu_cores]
        )
        self.wait(8.0)

        # Dọn dẹp sơ đồ phần cứng để chuẩn bị sang phần Batching
        self.play(
            FadeOut(large_weight),
            FadeOut(gpu_idle_lbl),
            FadeOut(decode_title),
            FadeOut(decode_math),
            FadeOut(gpu_box), FadeOut(gpu_lbl), FadeOut(gpu_cores),
            FadeOut(vram_box), FadeOut(vram_lbl), FadeOut(vram_grids),
            FadeOut(bridge_upper), FadeOut(bridge_lower), FadeOut(bridge_lbl),
            run_time=1.0
        )
        self.wait(1.0)

        # =====================================================================
        # BƯỚC 5.2: CƠ CHẾ GHÉP LÔ (BATCHING)
        # =====================================================================
        batch_title = create_text("Cơ chế Ghép lô (Batching) trong giải mã", font_size=13, color=YELLOW).move_to(UP * 2.5)
        batch_intro = create_markup_text(
            "Ghép $B$ inputs song song cho phép <b>nạp Model Weights 1 lần duy nhất</b>,\n"
            "chia sẻ chi phí nạp weights từ VRAM để tận dụng tài nguyên GPU.",
            font_size=10, color=WHITE, line_spacing=1.2
        ).move_to(UP * 1.9)

        self.play(
            Write(batch_title),
            Write(batch_intro),
            run_time=1.5
        )
        self.wait(3.0)

        # Trực quan hóa Batching (4 inputs đi song song) - Đẩy lệch xuống dưới tránh chạm đè intro
        batch_rects = VGroup()
        batch_lbls = VGroup()
        for idx in range(4):
            rect = RoundedRectangle(width=1.8, height=0.5, color=GREEN, fill_color="#122418", fill_opacity=0.9, corner_radius=0.04)
            rect.move_to(LEFT * 3.3 + DOWN * (0.8 * (1.5 - idx) + 0.4))
            lbl = create_text(f"Request {idx+1}", font_size=8, color=WHITE).move_to(rect.get_center())
            batch_rects.add(rect)
            batch_lbls.add(lbl)

        shared_weight = RoundedRectangle(width=2.5, height=1.6, color=BLUE_B, fill_color="#121824", fill_opacity=0.9, corner_radius=0.06)
        shared_weight.move_to(RIGHT * 3.0 + DOWN * 0.4)
        shared_lbl = create_text("Model Weights\n(Nạp 1 lần)", font_size=8, color=BLUE_A).move_to(shared_weight.get_center())

        arrow_group = VGroup()
        for idx in range(4):
            arr = Arrow(start=shared_weight.get_left(), end=batch_rects[idx].get_right(), color=GOLD, stroke_width=1.5)
            arrow_group.add(arr)

        self.play(
            FadeIn(batch_rects), Write(batch_lbls),
            FadeIn(shared_weight), Write(shared_lbl),
            run_time=1.5
        )
        self.play(Create(arrow_group), run_time=1.0)
        self.wait(10.0)

        self.play(
            FadeOut(batch_title), FadeOut(batch_intro),
            FadeOut(batch_rects), FadeOut(batch_lbls),
            FadeOut(shared_weight), FadeOut(shared_lbl),
            FadeOut(arrow_group),
            run_time=1.0
        )
        self.wait(1.0)

        # =====================================================================
        # BƯỚC 6: CƠ CHẾ BẢN CHẤT CỦA KV CACHE
        # =====================================================================
        kv_title = create_text("Cơ chế hoạt động của Bộ nhớ đệm Key-Value (KV Cache)", font_size=13, color=GOLD_B)
        kv_title.move_to(UP * 2.2)
        self.play(Write(kv_title), run_time=0.8)
        self.wait(3.0)

        # --- TRƯỜNG HỢP 1: KHÔNG DÙNG KV CACHE ---
        no_kv_lbl = create_markup_text(
            "<span foreground=\"#FF5555\"><b>Trường hợp 1: Không sử dụng KV Cache</b></span>\n"
            "Mô hình bắt buộc phải tính lại khóa (Key) và giá trị (Value)\n"
            "của tất cả các token trước đó ở mỗi bước giải mã mới.",
            font_size=10, color=WHITE, line_spacing=1.2
        ).move_to(UP * 1.2)
        self.play(Write(no_kv_lbl), run_time=1.2)
        self.wait(8.0)

        tok1 = RoundedRectangle(width=0.9, height=0.5, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.04)
        tok1.move_to(LEFT * 2.2 + DOWN * 0.2)
        tok1_lbl = create_text("Token 1", font_size=8, color=WHITE).move_to(tok1.get_center())

        tok2 = RoundedRectangle(width=0.9, height=0.5, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.04)
        tok2.move_to(LEFT * 1.1 + DOWN * 0.2)
        tok2_lbl = create_text("Token 2", font_size=8, color=WHITE).move_to(tok2.get_center())

        tok3 = RoundedRectangle(width=0.9, height=0.5, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.95, corner_radius=0.04)
        tok3.move_to(RIGHT * 0.0 + DOWN * 0.2)
        tok3_lbl = create_text("Token 3", font_size=8, color=WHITE).move_to(tok3.get_center())

        old_tokens = VGroup(tok1, tok1_lbl, tok2, tok2_lbl, tok3, tok3_lbl)
        self.play(FadeIn(old_tokens), run_time=1.0)
        self.wait(8.0)

        tok4 = RoundedRectangle(width=0.9, height=0.5, color=YELLOW, fill_color="#2b2614", fill_opacity=0.95, corner_radius=0.04)
        tok4.move_to(RIGHT * 1.1 + DOWN * 0.2)
        tok4_lbl = create_text("Token 4", font_size=8, color=YELLOW).move_to(tok4.get_center())

        recompute_arrows = VGroup(
            Arrow(start=tok1.get_top() + UP * 0.1, end=tok4.get_top() + UP * 0.1, color=RED, stroke_width=1.5, path_arc=-0.35),
            Arrow(start=tok2.get_top() + UP * 0.1, end=tok4.get_top() + UP * 0.1, color=RED, stroke_width=1.5, path_arc=-0.25),
            Arrow(start=tok3.get_top() + UP * 0.1, end=tok4.get_top() + UP * 0.1, color=RED, stroke_width=1.5, path_arc=-0.15)
        )
        recompute_lbl = create_text("Tính toán lại Key-Value lặp lại từ đầu!", font_size=8, color=RED).next_to(recompute_arrows[1], UP, buff=0.1)

        self.play(
            FadeIn(tok4), Write(tok4_lbl),
            Create(recompute_arrows), Write(recompute_lbl),
            run_time=1.5
        )
        self.wait(8.0)

        # Dọn dẹp trường hợp 1
        self.play(
            FadeOut(no_kv_lbl),
            FadeOut(old_tokens),
            FadeOut(tok4), FadeOut(tok4_lbl),
            FadeOut(recompute_arrows), FadeOut(recompute_lbl),
            run_time=1.0
        )
        self.wait(2.0)

        # --- TRƯỜNG HỢP 2: CÓ DÙNG KV CACHE ---
        with_kv_lbl = create_markup_text(
            "<span foreground=\"#00FF7F\"><b>Trường hợp 2: Có sử dụng KV Cache (Tối ưu)</b></span>\n"
            "Các vector Key và Value của token cũ được lưu trữ lại trong VRAM.\n"
            "Khi có token mới, ta chỉ tính toán và thêm (append) nó vào bộ nhớ đệm.",
            font_size=10, color=WHITE, line_spacing=1.2
        ).move_to(UP * 1.3)

        gpu_box = RoundedRectangle(width=2.8, height=2.2, color=ORANGE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        gpu_box.move_to(LEFT * 4.0 + DOWN * 0.5)
        gpu_lbl = create_text("LÕI TÍNH TOÁN GPU\n(GPU Core)", font_size=11, color=ORANGE).next_to(gpu_box, UP, buff=0.15)

        gpu_cores = VGroup()
        for r in range(4):
            for c in range(4):
                core = Square(side_length=0.25, color=ORANGE, fill_color=ORANGE, fill_opacity=0.2, stroke_width=1)
                core.move_to(gpu_box.get_center() + RIGHT * (c - 1.5) * 0.45 + UP * (r - 1.5) * 0.4)
                gpu_cores.add(core)

        vram_box = RoundedRectangle(width=2.8, height=2.2, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        vram_box.move_to(RIGHT * 4.0 + DOWN * 0.5)
        vram_lbl = create_text("BỘ NHỚ VRAM\n(Model weights & KV Cache)", font_size=11, color=BLUE_A).next_to(vram_box, UP, buff=0.15)

        bridge_upper = Line(start=gpu_box.get_right() + UP * 0.3, end=vram_box.get_left() + UP * 0.3, color=GRAY, stroke_width=2.5)
        bridge_lower = Line(start=gpu_box.get_right() + DOWN * 0.3, end=vram_box.get_left() + DOWN * 0.3, color=GRAY, stroke_width=2.5)
        bridge_lbl = create_markup_text(
            "Băng thông bộ nhớ\n"
            "<span foreground=\"#888888\"><b>Memory Bandwidth (GB/s)</b></span>",
            font_size=9, color=WHITE, line_spacing=1.1
        ).move_to(DOWN * 0.5)

        self.play(
            Write(with_kv_lbl),
            FadeIn(gpu_box), FadeIn(gpu_lbl), FadeIn(gpu_cores),
            FadeIn(vram_box), FadeIn(vram_lbl),
            Create(bridge_upper), Create(bridge_lower), FadeIn(bridge_lbl),
            run_time=1.5
        )
        self.wait(6.0)

        # Vẽ hộp KV Cache phụ nằm bên trong VRAM
        kv_cache_subbox = RoundedRectangle(width=2.5, height=1.4, color=GREEN_C, fill_color="#142b1a", fill_opacity=0.4, corner_radius=0.05)
        kv_cache_subbox.move_to(RIGHT * 4.0 + DOWN * 0.72)
        cache_lbl = create_text("KV Cache (VRAM)", font_size=9, color=GREEN, weight=BOLD).next_to(kv_cache_subbox, UP, buff=0.1)

        cache_rows = VGroup()
        for idx in range(3):
            row_rect = Rectangle(width=2.2, height=0.22, color=GREEN_E, fill_color=GREEN_E, fill_opacity=0.2, stroke_width=1)
            row_rect.move_to(RIGHT * 4.0 + DOWN * (0.3 + idx * 0.28))
            row_lbl = create_text(f"Key-Value Token {idx+1}", font_size=7, color=WHITE).move_to(row_rect.get_center())
            cache_rows.add(VGroup(row_rect, row_lbl))

        self.play(
            FadeIn(kv_cache_subbox), Write(cache_lbl),
            FadeIn(cache_rows),
            run_time=1.5
        )
        self.wait(8.0)

        # Sinh token 4 mới ở phía bên LÕI TÍNH TOÁN GPU
        tok4_new = RoundedRectangle(width=1.0, height=0.5, color=YELLOW, fill_color="#2b2614", fill_opacity=0.95, corner_radius=0.04)
        tok4_new.move_to(LEFT * 4.0 + UP * 0.2)
        tok4_new_lbl = create_text("Token 4", font_size=8, color=YELLOW).move_to(tok4_new.get_center())

        self.play(
            FadeIn(tok4_new), Write(tok4_new_lbl),
            *[c.animate(run_time=0.5).set_fill(ORANGE, opacity=0.9) for c in gpu_cores],
            run_time=1.0
        )
        self.play(
            *[c.animate(run_time=0.5).set_fill(ORANGE, opacity=0.2) for c in gpu_cores]
        )
        self.wait(3.0)

        # Trích xuất KV vector từ token 4 và trượt vào KV Cache ở VRAM
        new_kv_rect = Rectangle(width=2.2, height=0.22, color=YELLOW, fill_color=YELLOW, fill_opacity=0.4, stroke_width=1.5)
        new_kv_rect.move_to(LEFT * 4.0 + DOWN * 0.3)
        new_kv_lbl = create_text("Key-Value Token 4", font_size=7, color=YELLOW).move_to(new_kv_rect.get_center())
        new_kv_group = VGroup(new_kv_rect, new_kv_lbl)

        success_lbl = create_text("Lưu trực tiếp vào Cache Grid! Không cần tính lại token cũ.", font_size=8, color=GREEN_B).move_to(DOWN * 1.7)

        self.play(
            FadeIn(new_kv_group),
            run_time=0.8
        )
        self.wait(2.0)
        
        self.play(
            new_kv_group.animate(run_time=1.8).move_to(RIGHT * 4.0 + DOWN * 1.14).set_color(GREEN_C),
            FadeIn(success_lbl),
        )
        self.wait(8.0)

        # Dọn dẹp sơ đồ phần cứng
        self.play(
            FadeOut(kv_title),
            FadeOut(with_kv_lbl),
            FadeOut(kv_cache_subbox), FadeOut(cache_lbl),
            FadeOut(cache_rows),
            FadeOut(tok4_new), FadeOut(tok4_new_lbl),
            FadeOut(new_kv_group), FadeOut(success_lbl),
            FadeOut(gpu_box), FadeOut(gpu_lbl), FadeOut(gpu_cores),
            FadeOut(vram_box), FadeOut(vram_lbl),
            FadeOut(bridge_upper), FadeOut(bridge_lower), FadeOut(bridge_lbl),
            run_time=1.2
        )
        self.wait(2.0)

        # =====================================================================
        # BƯỚC 6.2: CÔNG THỨC KÍCH THƯỚC KV CACHE (SLIDE 107)
        # =====================================================================
        size_title = create_text("Kích thước bộ nhớ đệm KV Cache", font_size=13, color=YELLOW).move_to(UP * 2.2)
        size_box = RoundedRectangle(width=8.6, height=0.6, color=GOLD_A, fill_color="#1a1814", fill_opacity=0.9, corner_radius=0.06)
        size_box.move_to(UP * 1.4)

        size_txt = create_markup_text(
            "Size = ( <span foreground=\"#FFC66D\">batch</span> · <span foreground=\"#FFC66D\">n<sub>ctx</sub></span> ) · ( 2 · <span foreground=\"#FF5555\">n<sub>layer</sub></span> · <span foreground=\"#FF5555\">n<sub>heads</sub></span> · <span foreground=\"#FF5555\">head_dim</span> ) · <span foreground=\"#33AAFF\">n<sub>bytes</sub></span>",
            font_size=8.5, color=WHITE
        ).move_to(size_box.get_center())

        size_desc = create_markup_text(
            "• <span foreground=\"#FFC66D\">batch · n<sub>ctx</sub></span> : Tăng tuyến tính theo lô và chiều dài ngữ cảnh.\n"
            "• Hệ số còn lại là cố định theo cấu trúc của từng mô hình.\n"
            "⇒ Ngữ cảnh càng dài, KV Cache càng khổng lồ, là điểm nghẽn VRAM chính.",
            font_size=9.5, color=WHITE, line_spacing=1.3
        ).move_to(DOWN * 0.4)

        self.play(
            Write(size_title),
            FadeIn(size_box),
            Write(size_txt),
            Write(size_desc),
            run_time=1.5
        )
        self.wait(10.0)

        self.play(
            FadeOut(size_title),
            FadeOut(size_box),
            FadeOut(size_txt),
            FadeOut(size_desc),
            run_time=1.0
        )
        self.wait(1.0)

        # =====================================================================
        # BƯỚC 6.3: CÁC KỸ THUẬT TỐI ƯU HÓA SUY LUẬN (SLIDE 108)
        # =====================================================================
        opt_title = create_text("Tối ưu hóa giải mã đơn token (Single-token optimization)", font_size=13, color=YELLOW).move_to(UP * 2.2)

        # Card 1: Memory Bandwidth ↓
        card_mem = RoundedRectangle(width=3.8, height=2.2, color=BLUE_B, fill_color="#121824", fill_opacity=0.9, corner_radius=0.06)
        card_mem.move_to(LEFT * 4.2 + DOWN * 0.2)
        lbl_mem = create_markup_text(
            "<b>Memory Bandwidth ↓</b>\n"
            "<span foreground=\"#888888\">(Giảm lượng dữ liệu nạp)</span>\n\n"
            "• Quantization (Lượng tử hóa)\n"
            "• Model Compression (Nén)",
            font_size=8, color=WHITE, line_spacing=1.3
        ).move_to(card_mem.get_center())

        # Card 2: FLOP/s ↑
        card_flop_rate = RoundedRectangle(width=3.8, height=2.2, color=ORANGE, fill_color="#241a12", fill_opacity=0.9, corner_radius=0.06)
        card_flop_rate.move_to(LEFT * 0.0 + DOWN * 0.2)
        lbl_flop_rate = create_markup_text(
            "<b>FLOP/s ↑</b>\n"
            "<span foreground=\"#888888\">(Tăng hiệu suất tính toán)</span>\n\n"
            "• FlashAttention\n"
            "• Tối ưu phần cứng &amp; I/O",
            font_size=8, color=WHITE, line_spacing=1.3
        ).move_to(card_flop_rate.get_center())

        # Card 3: FLOP ↓
        card_flop_total = RoundedRectangle(width=3.8, height=2.2, color=GREEN_B, fill_color="#122418", fill_opacity=0.9, corner_radius=0.06)
        card_flop_total.move_to(RIGHT * 4.2 + DOWN * 0.2)
        lbl_flop_total = create_markup_text(
            "<b>FLOP ↓</b>\n"
            "<span foreground=\"#888888\">(Giảm số phép tính)</span>\n\n"
            "• Mixture of Experts (MoE)\n"
            "• Giảm tham số kích hoạt",
            font_size=8, color=WHITE, line_spacing=1.3
        ).move_to(card_flop_total.get_center())

        self.play(
            FadeIn(opt_title),
            FadeIn(card_mem), Write(lbl_mem),
            FadeIn(card_flop_rate), Write(lbl_flop_rate),
            FadeIn(card_flop_total), Write(lbl_flop_total),
            run_time=1.8
        )
        self.wait(12.0)

        self.play(
            FadeOut(opt_title),
            FadeOut(card_mem), FadeOut(lbl_mem),
            FadeOut(card_flop_rate), FadeOut(lbl_flop_rate),
            FadeOut(card_flop_total), FadeOut(lbl_flop_total),
            run_time=1.0
        )
        self.wait(1.0)

        # =====================================================================
        # BƯỚC 7: TỔNG KẾT & SO SÁNH
        # =====================================================================
        recap_title = create_text("Tổng kết: So sánh Giai đoạn Prefill và Decode", font_size=13, color=YELLOW)
        recap_title.to_edge(UP, buff=0.4)
        self.play(
            FadeOut(sub_title),
            FadeIn(recap_title),
            run_time=1.0
        )
        self.wait(3.0)

        # Tạo bảng so sánh
        comparison_table = VGroup()
        headers = ["Giai đoạn", "Loại phép toán", "Cường độ số học", "Loại nghẽn"]
        header_colors = [BLUE_A, WHITE, WHITE, RED]
        
        # Dòng tiêu đề
        header_group = VGroup()
        for idx, h_text in enumerate(headers):
            cell = RoundedRectangle(width=2.5, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            cell.move_to(LEFT * (2.7 * (1.5 - idx)) + UP * 1.0)
            lbl = create_text(h_text, font_size=10, color=header_colors[idx]).move_to(cell.get_center())
            header_group.add(VGroup(cell, lbl))
        comparison_table.add(header_group)

        # 2 dòng dữ liệu
        table_rows = [
            ("Prefill Stage", "Nhân Ma trận - Ma trận\n(GEMM)", "Rất cao (tỷ lệ thuận T)", "Compute-bound\n(Nghẽn tính toán)"),
            ("Decode Stage", "Nhân Ma trận - Vector\n(GEMV)", "Cực kỳ thấp (~1 FLOP/B)", "Memory-bound\n(Nghẽn bộ nhớ)")
        ]

        row_y_coords = [0.1, -0.9]
        row_colors = [GREEN_B, RED_B]
        for r_idx, row_data in enumerate(table_rows):
            row_group = VGroup()
            for c_idx, cell_text in enumerate(row_data):
                cell = RoundedRectangle(width=2.5, height=0.8, color=GRAY_E, fill_color="#121315", fill_opacity=0.8, corner_radius=0.04)
                cell.move_to(LEFT * (2.7 * (1.5 - c_idx)) + UP * row_y_coords[r_idx])
                
                t_color = row_colors[r_idx] if c_idx == 3 else (BLUE_A if c_idx == 0 else WHITE)
                lbl = create_text(cell_text, font_size=9, color=t_color).move_to(cell.get_center())
                
                row_group.add(VGroup(cell, lbl))
            comparison_table.add(row_group)

        solution_note = create_markup_text(
            "<b>Ghi chú:</b> Sử dụng <span foreground=\"#00FF7F\"><b>KV Cache</b></span> giúp tránh tính toán lại các token cũ,\n"
            "chuyển đổi tính toán thành dạng gia tăng và tăng tốc độ xử lý lên nhiều lần.",
            font_size=10, color=WHITE, line_spacing=1.2
        ).move_to(DOWN * 2.1)

        self.play(
            FadeIn(comparison_table),
            Write(solution_note),
            run_time=1.8
        )
        self.wait(15.0)

        # Dọn dẹp kết thúc phân cảnh 4.1
        self.play(
            FadeOut(comparison_table),
            FadeOut(solution_note),
            FadeOut(recap_title),
            run_time=1.2
        )
        self.wait(2.0)
