import os
import tempfile
from pathlib import Path
import random
from manim import *

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[2] / "voiceover" / "generated_unsorted"


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    return time_offset + duration


def finish_voiceovers(scene, voiceover_end, padding=0.25):
    current_time = getattr(scene.renderer, "time", 0.0)
    remaining = voiceover_end + padding - current_time
    if remaining > 0:
        scene.wait(remaining)


# Note: visual/narration alignment comment translated from Vietnamese.
def create_text(text, font_size=24, font="Segoe UI", color=WHITE, **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    t = Text(text, font_size=base_size, font=font, color=color, **kwargs)
    t.scale(scale_factor)
    return t

# Note: visual/narration alignment comment translated from Vietnamese.
def create_markup_text(text, font_size=24, font="Segoe UI", **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    t = MarkupText(text, font_size=base_size, font=font, **kwargs)
    t.scale(scale_factor)
    return t

# Note: visual/narration alignment comment translated from Vietnamese.
def get_checkmark(color=GREEN, stroke_width=2.5):
    checkmark = VMobject(color=color, stroke_width=stroke_width)
    checkmark.set_points_as_corners([
        LEFT * 0.12 + DOWN * 0.05,
        ORIGIN + DOWN * 0.15,
        RIGHT * 0.2 + UP * 0.15
    ])
    return checkmark

# Note: visual/narration alignment comment translated from Vietnamese.
def get_crossmark(color=RED, stroke_width=2.5):
    cross = VGroup()
    line1 = Line(LEFT * 0.12 + UP * 0.12, RIGHT * 0.12 + DOWN * 0.12, color=color, stroke_width=stroke_width)
    line2 = Line(LEFT * 0.12 + DOWN * 0.12, RIGHT * 0.12 + UP * 0.12, color=color, stroke_width=stroke_width)
    cross.add(line1, line2)
    return cross


class Scene4_1(Scene):
    def construct(self):
        # Note: visual/narration alignment comment translated from Vietnamese.

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.camera.background_color = "#111111"

        # Voiceover audio is scheduled from actual MP3 durations.
        voiceover_end = 0.0
        voiceover_end = add_voiceover(self, "sc41_1.mp3", voiceover_end, 10.960)
        voiceover_end = add_voiceover(self, "sc41_2.mp3", voiceover_end, 17.508)
        voiceover_end = add_voiceover(self, "sc41_3.mp3", voiceover_end, 21.409)
        voiceover_end = add_voiceover(self, "sc41_4.mp3", voiceover_end, 30.975)
        voiceover_end = add_voiceover(self, "sc41_5.mp3", voiceover_end, 20.387)
        voiceover_end = add_voiceover(self, "sc41_6.mp3", voiceover_end, 17.879)
        voiceover_end = add_voiceover(self, "sc41_7.mp3", voiceover_end, 15.557)
        voiceover_end = add_voiceover(self, "sc41_8.mp3", voiceover_end, 24.520)


        # =====================================================================
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        chapter_title = create_text("Chapter 4: Systems Efficiency", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 4.1: Hardware Bottlenecks & The Nature of KV Cache", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(5.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        sub_title = create_text("Hardware Bottlenecks & Nature of KV Cache", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(3.0)

        # =====================================================================
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        perf_title = create_markup_text("<b>Latency (Latency) vs. Throughput (Throughput)</b>", font_size=14, color=YELLOW).move_to(UP * 2.0)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        card_latency = RoundedRectangle(width=4.5, height=2.4, color=BLUE_B, fill_color="#121824", fill_opacity=0.9, corner_radius=0.06)
        card_latency.move_to(LEFT * 2.8 + DOWN * 0.2)
        lbl_latency = create_markup_text(
            "<b>Latency (Latency)</b>\n\n"
            "• Response time for one request\n"
            "• Unit: milliseconds (ms)\n"
            "• Best for: single-user experience",
            font_size=8.5, color=WHITE, line_spacing=1.3
        ).move_to(card_latency.get_center())

        # Note: visual/narration alignment comment translated from Vietnamese.
        card_throughput = RoundedRectangle(width=4.5, height=2.4, color=GREEN_B, fill_color="#122418", fill_opacity=0.9, corner_radius=0.06)
        card_throughput.move_to(RIGHT * 2.8 + DOWN * 0.2)
        lbl_throughput = create_markup_text(
            "<b>Throughput (Throughput)</b>\n\n"
            "• Completed requests per second\n"
            "• Unit: requests/second (RPS)\n"
            "• Best for: serving many users at scale",
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
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        intro_text = create_markup_text(
            "<b>Hardware block diagram &amp; memory bandwidth</b>",
            font_size=14, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(intro_text), run_time=1.5)
        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        gpu_box = RoundedRectangle(width=2.8, height=2.2, color=ORANGE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        gpu_box.move_to(LEFT * 4.0 + DOWN * 0.5)
        gpu_lbl = create_text("GPU COMPUTE CORE\n(GPU Core)", font_size=11, color=ORANGE).next_to(gpu_box, UP, buff=0.15)
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        gpu_cores = VGroup()
        for r in range(4):
            for c in range(4):
                core = Square(side_length=0.25, color=ORANGE, fill_color=ORANGE, fill_opacity=0.2, stroke_width=1)
                core.move_to(gpu_box.get_center() + RIGHT * (c - 1.5) * 0.45 + UP * (r - 1.5) * 0.4)
                gpu_cores.add(core)

        # Note: visual/narration alignment comment translated from Vietnamese.
        vram_box = RoundedRectangle(width=2.8, height=2.2, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        vram_box.move_to(RIGHT * 4.0 + DOWN * 0.5)
        vram_lbl = create_text("VRAM MEMORY\n(Model weights & KV Cache)", font_size=11, color=BLUE_A).next_to(vram_box, UP, buff=0.15)

        # Note: visual/narration alignment comment translated from Vietnamese.
        vram_grids = VGroup()
        for r in range(4):
            for c in range(3):
                grid = Rectangle(width=0.6, height=0.35, color=BLUE, fill_color=BLUE_E, fill_opacity=0.15, stroke_width=1)
                grid.move_to(vram_box.get_center() + RIGHT * (c - 1.0) * 0.75 + UP * (r - 1.5) * 0.42)
                vram_grids.add(grid)

        # Note: visual/narration alignment comment translated from Vietnamese.
        bridge_upper = Line(start=gpu_box.get_right() + UP * 0.3, end=vram_box.get_left() + UP * 0.3, color=GRAY, stroke_width=2.5)
        bridge_lower = Line(start=gpu_box.get_right() + DOWN * 0.3, end=vram_box.get_left() + DOWN * 0.3, color=GRAY, stroke_width=2.5)
        bridge_lbl = create_markup_text(
            "Memory bandwidth\n"
            "<span foreground=\"#888888\"><b>Memory Bandwidth (GB/s)</b></span>",
            font_size=9, color=WHITE, line_spacing=1.1
        ).move_to(DOWN * 0.5)

        self.play(
            FadeIn(gpu_box), FadeIn(gpu_lbl), FadeIn(gpu_cores),
            FadeIn(vram_box), FadeIn(vram_lbl), FadeIn(vram_grids),
            Create(bridge_upper), Create(bridge_lower), Write(bridge_lbl),
            run_time=2.0
        )
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        specs_box = RoundedRectangle(width=8.0, height=1.6, color=GOLD_A, fill_color="#181812", fill_opacity=0.95, corner_radius=0.08)
        specs_box.move_to(DOWN * 2.7)
        specs_title = create_text("NVIDIA H100 SXM GPU specs", font_size=10, color=GOLD_B).next_to(specs_box.get_top(), DOWN, buff=0.12)
        
        specs_text = create_markup_text(
            "• BF16 dense tensor core max FLOP/s:  <b>≈ 1 × 10<sup>15</sup> FLOP/s</b> (1 PFLOPS)\n"
            "• Memory bandwidth (Memory Bandwidth):  <b>≈ 3.35 × 10<sup>12</sup> bytes/s</b> (3.35 TB/s)\n"
            "• Ratio >> 100 FLOP/byte -> compute is almost \"free\" compared with memory loading!",
            font_size=7.5, line_spacing=1.2
        ).next_to(specs_title, DOWN, buff=0.1)
        specs_group = VGroup(specs_box, specs_title, specs_text)

        self.play(FadeIn(specs_group, shift=UP * 0.15), run_time=1.0)
        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        packets = VGroup()
        for i in range(5):
            packet = RoundedRectangle(width=0.4, height=0.3, color=BLUE_A, fill_color=BLUE, fill_opacity=0.8, corner_radius=0.03)
            packet.move_to(vram_box.get_center())
            packets.add(packet)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            LaggedStart(
                *[p.animate(run_time=1.5, rate_func=linear).move_to(gpu_box.get_center()) for p in packets],
                lag_ratio=0.3
            )
        )
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            *[c.animate(run_time=0.4).set_fill(ORANGE, opacity=0.8) for c in gpu_cores]
        )
        self.play(
            *[c.animate(run_time=0.4).set_fill(ORANGE, opacity=0.2) for c in gpu_cores],
            FadeOut(packets)
        )
        self.wait(5.0)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        self.play(FadeOut(intro_text), FadeOut(specs_group), run_time=0.8)

        formula_title = create_text("Arithmetic Intensity (Arithmetic Intensity)", font_size=13, color=GOLD_B).move_to(UP * 2.3)
        formula_box = RoundedRectangle(width=8.2, height=0.55, color=GOLD_A, fill_color="#1a1814", fill_opacity=0.9, corner_radius=0.06)
        formula_box.move_to(UP * 1.4)
        
        formula_txt = create_markup_text(
            "Arithmetic intensity = <span foreground=\"#00FF7F\">Number of operations (FLOPs)</span> / <span foreground=\"#33AAFF\">Loaded memory volume (Bytes)</span>",
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
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        #
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        self.play(
            FadeOut(formula_title),
            FadeOut(formula_box),
            FadeOut(formula_txt),
            run_time=0.8
        )

        time_title = create_text("Execution time of one operation", font_size=13, color=GOLD_B).move_to(UP * 2.3)
        time_box = RoundedRectangle(width=8.6, height=0.6, color=GOLD_A, fill_color="#1a1814", fill_opacity=0.9, corner_radius=0.06)
        time_box.move_to(UP * 1.4)

        time_txt = create_markup_text(
            "Time = max ( <span foreground=\"#00FF7F\">GEMM/GEMV FLOPs</span> / <span foreground=\"#00FF7F\">GPU FLOP/s</span> , <span foreground=\"#33AAFF\">Load weights (GB)</span> / <span foreground=\"#33AAFF\">VRAM bandwidth (GB/s)</span> )",
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
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        prefill_title = create_text(
            "Prefill phase (Prompt processing) - Compute-bound",
            font_size=13, color="#00FFFF", weight=BOLD
        ).move_to(UP * 2.2)

        prefill_math = create_markup_text(
            "- Operation: matrix-matrix multiplication (GEMM) : Q × K<sup>T</sup>\n"
            "- Large prompt length T ⇒ Number of operations O(T · d<sup>2</sup>) much larger than weights O(d<sup>2</sup>)\n"
            "- <b>extremely high arithmetic intensity</b> ⇒ Limited by GPU compute speed.",
            font_size=10, color=WHITE, line_spacing=1.3
        ).move_to(UP * 1.3)

        self.play(
            Write(prefill_title),
            Write(prefill_math),
            run_time=1.5
        )
        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        prefill_packets = VGroup()
        for i in range(12):
            p = RoundedRectangle(width=0.35, height=0.25, color=BLUE_A, fill_color=BLUE_B, fill_opacity=0.9, corner_radius=0.03)
            p.move_to(vram_box.get_center() + np.array([random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), 0]))
            prefill_packets.add(p)

        prefill_anims = []
        for idx, p in enumerate(prefill_packets):
            dest_pos = gpu_box.get_center() + np.array([random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), 0])
            prefill_anims.append(p.animate(run_time=random.uniform(1.0, 1.6), rate_func=linear).move_to(dest_pos))

        gpu_status_lbl = create_text("GPU utilization: 100%\n(Compute bottleneck - Compute-bound)", font_size=10, color=GREEN).next_to(gpu_box, DOWN, buff=0.2)

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

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(prefill_title),
            FadeOut(prefill_math),
            FadeOut(gpu_status_lbl),
            *[c.animate(run_time=0.4).set_fill(ORANGE, opacity=0.2) for c in gpu_cores],
            run_time=0.8
        )
        self.wait(1.0)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        decode_title = create_text(
            "Decode phase (Sequential token generation) - Memory-bound",
            font_size=13, color="#FF3333", weight=BOLD
        ).move_to(UP * 2.2)

        decode_math = create_markup_text(
            "- Operation: matrix-vector multiplication (GEMV) : W × x\n"
            "- Generate one token at a time (T = 1) ⇒ Compute O(d<sup>2</sup>), memory loading O(d<sup>2</sup>)\n"
            "- <b>extremely low arithmetic intensity (~1 FLOP/Byte)</b> ⇒ GPU idles while waiting for weights from VRAM.",
            font_size=10, color=WHITE, line_spacing=1.3
        ).move_to(UP * 1.3)

        self.play(
            Write(decode_title),
            Write(decode_math),
            run_time=1.5
        )
        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        large_weight_box = RoundedRectangle(width=1.6, height=1.3, color=BLUE_D, fill_color=BLUE_E, fill_opacity=0.9, corner_radius=0.05)
        large_weight_box.move_to(vram_box.get_center())
        large_weight_lbl = create_text("Model Weights\n(Tens of GB)", font_size=8, color=WHITE).move_to(large_weight_box.get_center())
        large_weight = VGroup(large_weight_box, large_weight_lbl)

        token_dot = Dot(color=YELLOW, radius=0.08).move_to(gpu_box.get_center())
        token_lbl = create_text("1 new token", font_size=8, color=YELLOW).next_to(token_dot, UP, buff=0.1)

        gpu_idle_lbl = create_markup_text(
            "<span foreground=\"#FF5555\"><b>GPU Idle (95% Idle)</b></span>\n"
            "Waiting for weights from VRAM...",
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

        # Note: visual/narration alignment comment translated from Vietnamese.
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
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        batch_title = create_text("Batching mechanism (Batching) in decoding", font_size=13, color=YELLOW).move_to(UP * 2.5)
        batch_intro = create_markup_text(
            "Batching $B$ inputs in parallel allows <b>loading model weights only once</b>,\n"
            "sharing VRAM weight-loading cost to utilize GPU resources.",
            font_size=10, color=WHITE, line_spacing=1.2
        ).move_to(UP * 1.9)

        self.play(
            Write(batch_title),
            Write(batch_intro),
            run_time=1.5
        )
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
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
        shared_lbl = create_text("Model Weights\n(Load once)", font_size=8, color=BLUE_A).move_to(shared_weight.get_center())

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
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        kv_title = create_text("How the Key-Value Cache Works (KV Cache)", font_size=13, color=GOLD_B)
        kv_title.move_to(UP * 2.2)
        self.play(Write(kv_title), run_time=0.8)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        no_kv_lbl = create_markup_text(
            "<span foreground=\"#FF5555\"><b>Case 1: Without KV Cache</b></span>\n"
            "The model must recompute the Key and Value\n"
            "for all previous tokens at every new decoding step.",
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
        recompute_lbl = create_text("Repeatedly recompute Key-Value from scratch!", font_size=8, color=RED).next_to(recompute_arrows[1], UP, buff=0.1)

        self.play(
            FadeIn(tok4), Write(tok4_lbl),
            Create(recompute_arrows), Write(recompute_lbl),
            run_time=1.5
        )
        self.wait(8.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(no_kv_lbl),
            FadeOut(old_tokens),
            FadeOut(tok4), FadeOut(tok4_lbl),
            FadeOut(recompute_arrows), FadeOut(recompute_lbl),
            run_time=1.0
        )
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        with_kv_lbl = create_markup_text(
            "<span foreground=\"#00FF7F\"><b>Case 2: With KV Cache (optimized)</b></span>\n"
            "Key and Value vectors for old tokens are stored in VRAM.\n"
            "When a new token arrives, only compute it and append it to the cache.",
            font_size=10, color=WHITE, line_spacing=1.2
        ).move_to(UP * 1.3)

        gpu_box = RoundedRectangle(width=2.8, height=2.2, color=ORANGE, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        gpu_box.move_to(LEFT * 4.0 + DOWN * 0.5)
        gpu_lbl = create_text("GPU COMPUTE CORE\n(GPU Core)", font_size=11, color=ORANGE).next_to(gpu_box, UP, buff=0.15)

        gpu_cores = VGroup()
        for r in range(4):
            for c in range(4):
                core = Square(side_length=0.25, color=ORANGE, fill_color=ORANGE, fill_opacity=0.2, stroke_width=1)
                core.move_to(gpu_box.get_center() + RIGHT * (c - 1.5) * 0.45 + UP * (r - 1.5) * 0.4)
                gpu_cores.add(core)

        vram_box = RoundedRectangle(width=2.8, height=2.2, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        vram_box.move_to(RIGHT * 4.0 + DOWN * 0.5)
        vram_lbl = create_text("VRAM MEMORY\n(Model weights & KV Cache)", font_size=11, color=BLUE_A).next_to(vram_box, UP, buff=0.15)

        bridge_upper = Line(start=gpu_box.get_right() + UP * 0.3, end=vram_box.get_left() + UP * 0.3, color=GRAY, stroke_width=2.5)
        bridge_lower = Line(start=gpu_box.get_right() + DOWN * 0.3, end=vram_box.get_left() + DOWN * 0.3, color=GRAY, stroke_width=2.5)
        bridge_lbl = create_markup_text(
            "Memory bandwidth\n"
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

        # Note: visual/narration alignment comment translated from Vietnamese.
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

        # Note: visual/narration alignment comment translated from Vietnamese.
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

        # Note: visual/narration alignment comment translated from Vietnamese.
        new_kv_rect = Rectangle(width=2.2, height=0.22, color=YELLOW, fill_color=YELLOW, fill_opacity=0.4, stroke_width=1.5)
        new_kv_rect.move_to(LEFT * 4.0 + DOWN * 0.3)
        new_kv_lbl = create_text("Key-Value Token 4", font_size=7, color=YELLOW).move_to(new_kv_rect.get_center())
        new_kv_group = VGroup(new_kv_rect, new_kv_lbl)

        success_lbl = create_text("Store directly in the cache grid. No need to recompute old tokens.", font_size=8, color=GREEN_B).move_to(DOWN * 1.7)

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

        # Note: visual/narration alignment comment translated from Vietnamese.
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
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        size_title = create_text("KV Cache memory size", font_size=13, color=YELLOW).move_to(UP * 2.2)
        size_box = RoundedRectangle(width=8.6, height=0.6, color=GOLD_A, fill_color="#1a1814", fill_opacity=0.9, corner_radius=0.06)
        size_box.move_to(UP * 1.4)

        size_txt = create_markup_text(
            "Size = ( <span foreground=\"#FFC66D\">batch</span> · <span foreground=\"#FFC66D\">n<sub>ctx</sub></span> ) · ( 2 · <span foreground=\"#FF5555\">n<sub>layer</sub></span> · <span foreground=\"#FF5555\">n<sub>heads</sub></span> · <span foreground=\"#FF5555\">head<sub>dim</sub></span> ) · <span foreground=\"#33AAFF\">n<sub>bytes</sub></span>",
            font_size=8.5, color=WHITE
        ).move_to(size_box.get_center())

        size_desc = create_markup_text(
            "• <span foreground=\"#FFC66D\">batch · n<sub>ctx</sub></span> : Scales linearly with batch and context length.\n"
            "• The remaining factors are fixed by each model architecture.\n"
            "⇒ The longer the context, the larger the KV Cache, making it the main VRAM bottleneck.",
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
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        opt_title = create_text("Single-token decoding optimization (Single-token optimization)", font_size=13, color=YELLOW).move_to(UP * 2.2)

        # Card 1: Memory Bandwidth ↓
        card_mem = RoundedRectangle(width=3.8, height=2.2, color=BLUE_B, fill_color="#121824", fill_opacity=0.9, corner_radius=0.06)
        card_mem.move_to(LEFT * 4.2 + DOWN * 0.2)
        lbl_mem = create_markup_text(
            "<b>Memory Bandwidth ↓</b>\n"
            "<span foreground=\"#888888\">(Reduce loaded data)</span>\n\n"
            "• Quantization (Quantization)\n"
            "• Model Compression (Compression)",
            font_size=8, color=WHITE, line_spacing=1.3
        ).move_to(card_mem.get_center())

        # Card 2: FLOP/s ↑
        card_flop_rate = RoundedRectangle(width=3.8, height=2.2, color=ORANGE, fill_color="#241a12", fill_opacity=0.9, corner_radius=0.06)
        card_flop_rate.move_to(LEFT * 0.0 + DOWN * 0.2)
        lbl_flop_rate = create_markup_text(
            "<b>FLOP/s ↑</b>\n"
            "<span foreground=\"#888888\">(Increase compute efficiency)</span>\n\n"
            "• FlashAttention\n"
            "• Hardware &amp; I/O optimization",
            font_size=8, color=WHITE, line_spacing=1.3
        ).move_to(card_flop_rate.get_center())

        # Card 3: FLOP ↓
        card_flop_total = RoundedRectangle(width=3.8, height=2.2, color=GREEN_B, fill_color="#122418", fill_opacity=0.9, corner_radius=0.06)
        card_flop_total.move_to(RIGHT * 4.2 + DOWN * 0.2)
        lbl_flop_total = create_markup_text(
            "<b>FLOP ↓</b>\n"
            "<span foreground=\"#888888\">(Reduce FLOPs)</span>\n\n"
            "• Mixture of Experts (MoE)\n"
            "• Reduce active parameters",
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
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        recap_title = create_text("Summary: Comparing Prefill and Decode Phases", font_size=13, color=YELLOW)
        recap_title.to_edge(UP, buff=0.4)
        self.play(
            FadeOut(sub_title),
            FadeIn(recap_title),
            run_time=1.0
        )
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        comparison_table = VGroup()
        headers = ["Phase", "Operation type", "Arithmetic intensity", "Bottleneck type"]
        header_colors = [BLUE_A, WHITE, WHITE, RED]
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        header_group = VGroup()
        for idx, h_text in enumerate(headers):
            cell = RoundedRectangle(width=2.5, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            cell.move_to(LEFT * (2.7 * (1.5 - idx)) + UP * 1.0)
            lbl = create_text(h_text, font_size=10, color=header_colors[idx]).move_to(cell.get_center())
            header_group.add(VGroup(cell, lbl))
        comparison_table.add(header_group)

        # Note: visual/narration alignment comment translated from Vietnamese.
        table_rows = [
            ("Prefill Stage", "Matrix-Matrix multiply\n(GEMM)", "very high (proportional to T)", "Compute-bound\n(compute bottleneck)"),
            ("Decode Stage", "Matrix-Vector multiply\n(GEMV)", "Extremely low (~1 FLOP/B)", "Memory-bound\n(memory bottleneck)")
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
            "<b>Note:</b> Using <span foreground=\"#00FF7F\"><b>KV Cache</b></span> avoids recomputing old tokens,\n"
            "turns computation into incremental work, and speeds up processing many times.",
            font_size=10, color=WHITE, line_spacing=1.2
        ).move_to(DOWN * 2.1)

        self.play(
            FadeIn(comparison_table),
            Write(solution_note),
            run_time=1.8
        )
        self.wait(15.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(comparison_table),
            FadeOut(solution_note),
            FadeOut(recap_title),
            run_time=1.2
        )
        self.wait(2.0)
        finish_voiceovers(self, voiceover_end)
