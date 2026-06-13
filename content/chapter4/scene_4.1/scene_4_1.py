import os
import tempfile
from pathlib import Path

from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_4_1_DURATIONS = {
    "sc41_001.mp3": 3.157914,
    "sc41_002.mp3": 8.173424,
    "sc41_003.mp3": 3.065034,
    "sc41_004.mp3": 6.362268,
    "sc41_005.mp3": 6.176508,
    "sc41_006.mp3": 12.027937,
    "sc41_007.mp3": 7.105306,
    "sc41_008.mp3": 5.944308,
    "sc41_009.mp3": 13.746213,
    "sc41_010.mp3": 9.195102,
    "sc41_011.mp3": 20.758639,
    "sc41_012.mp3": 5.015510,
    "sc41_013.mp3": 5.944308,
    "sc41_014.mp3": 4.458231,
    "sc41_015.mp3": 4.318912,
    "sc41_016.mp3": 5.061950,
    "sc41_017.mp3": 4.365351,
    "sc41_018.mp3": 8.266304,
    "sc41_019.mp3": 5.294150,
    "sc41_020.mp3": 9.427302,
}
SCENE_4_1_VOICEOVERS = tuple(SCENE_4_1_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc41_*.mp3"))
    expected = sorted(SCENE_4_1_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 4.1 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_4_1_DURATIONS:
        raise KeyError(f"Unexpected Scene 4.1 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 4.1 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_4_1_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_4_1_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 4.1 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


def create_text(text, font_size=24, font="Noto Sans", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)


def create_markup_text(text, font_size=24, font="Noto Sans", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)


def labeled_box(title, body="", width=2.2, height=0.9, color=BLUE_A, fill="#15181d"):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.07,
        color=color,
        fill_color=fill,
        fill_opacity=0.94,
        stroke_width=1.5,
    )
    title_obj = create_text(title, font_size=9.5, color=color)
    title_obj.move_to(box.get_center() + UP * height * (0.17 if body else 0.0))
    group = VGroup(box, title_obj)
    if body:
        body_obj = create_text(body, font_size=7.4, color=GRAY_A, line_spacing=1.0)
        body_obj.move_to(box.get_center() + DOWN * height * 0.2)
        group.add(body_obj)
    return group


def token_box(text, color=GRAY_C, width=0.72, height=0.42):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.04,
        color=color,
        fill_color="#17191d",
        fill_opacity=0.96,
        stroke_width=1.2,
    )
    lbl = create_text(text, font_size=7.5, color=color if color != GRAY_C else WHITE).move_to(box.get_center())
    return VGroup(box, lbl)


def progress_bar(label, value, color, width=2.8):
    track = RoundedRectangle(width=width, height=0.24, color=GRAY_D, fill_color="#202124", fill_opacity=1, corner_radius=0.04)
    fill = Rectangle(width=width * value, height=0.19, color=color, fill_color=color, fill_opacity=0.9, stroke_width=0)
    fill.move_to(track.get_left() + RIGHT * width * value / 2)
    text = create_text(label, font_size=8, color=color).next_to(track, UP, buff=0.1)
    return VGroup(track, fill, text)


def lane(label, color, width=3.0):
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=GRAY_D, stroke_width=4)
    dot = Dot(line.get_left(), radius=0.075, color=color)
    text = create_text(label, font_size=8.5, color=color).next_to(line, UP, buff=0.14)
    return VGroup(line, dot, text)


def gpu_vram_pipeline():
    vram = labeled_box("VRAM", "weights\nactivations\nKV cache", width=2.25, height=1.65, color=BLUE_A, fill="#101826")
    gpu = labeled_box("Processor", "FLOP/s", width=2.2, height=1.4, color=ORANGE, fill="#21170f")
    vram.move_to(LEFT * 3.35 + DOWN * 0.05)
    gpu.move_to(RIGHT * 2.95 + DOWN * 0.05)
    wire = Arrow(vram.get_right(), gpu.get_left(), color=BLUE_A, stroke_width=2.2, buff=0.16)
    wire_label = create_text("Memory bandwidth", font_size=9, color=BLUE_A).next_to(wire, UP, buff=0.15)
    cores = VGroup()
    for row in range(3):
        for col in range(4):
            sq = Square(side_length=0.18, color=ORANGE, fill_color=ORANGE, fill_opacity=0.25, stroke_width=0.8)
            sq.move_to(gpu[0].get_center() + RIGHT * (col - 1.5) * 0.32 + UP * (row - 1) * 0.24 + DOWN * 0.08)
            cores.add(sq)
    packets = VGroup()
    for idx in range(5):
        p = Square(side_length=0.17, color=BLUE_A, fill_color=BLUE_A, fill_opacity=0.9, stroke_width=0.6)
        p.move_to(vram[0].get_right() + LEFT * 0.25 + UP * (idx - 2) * 0.16)
        packets.add(p)
    return VGroup(vram, gpu, wire, wire_label, cores, packets)


def kv_rows(n, color=GREEN):
    rows = VGroup()
    for _ in range(n):
        rows.add(Rectangle(width=1.85, height=0.2, color=color, fill_color=color, fill_opacity=0.34, stroke_width=0.8))
    rows.arrange(DOWN, buff=0.08)
    return rows


class Scene4_1(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (_, duration) in enumerate(SCENE_4_1_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        chapter_title = create_text("Chapter 4: Systems Efficiency", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 4.1: Efficient Generation Basics", font_size=17, color=GRAY_A)
        chapter_header = VGroup(chapter_title, chapter_sub.next_to(chapter_title, DOWN, buff=0.15)).move_to(ORIGIN)
        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)
        self.wait_until(cue_start[2])

        sub_title = create_text("Efficient generation: from algorithm to hardware", font_size=15, color=YELLOW).to_edge(UP, buff=0.4)
        scope = VGroup(
            labeled_box("Basics", "what limits one decode", width=2.2, color=BLUE_A),
            labeled_box("Faster", "reuse + parallelize", width=2.2, color=GREEN),
            labeled_box("Compare", "efficient meta-generators", width=2.35, color=PURPLE_A),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.15)
        scope_path = VGroup(
            Arrow(scope[0].get_right(), scope[1].get_left(), color=GRAY_B, stroke_width=1.4, buff=0.06),
            Arrow(scope[1].get_right(), scope[2].get_left(), color=GRAY_B, stroke_width=1.4, buff=0.06),
        )
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=0.8)
        self.play(FadeIn(scope, lag_ratio=0.1), Create(scope_path), run_time=1.0)

        self.wait_until(cue_start[3])
        self.play(FadeOut(VGroup(scope, scope_path)), run_time=0.45)

        latency_title = create_text("Latency: one request's waiting time", font_size=11, color=RED_B)
        latency_title.move_to(LEFT * 3.1 + UP * 1.7)
        latency_track = Line(LEFT * 4.6, LEFT * 1.4, color=GRAY_D, stroke_width=5).shift(DOWN * 0.05)
        request = token_box("req", color=RED_B, width=0.62).move_to(latency_track.get_left())
        response = token_box("done", color=GREEN, width=0.78).move_to(latency_track.get_right())
        clock = Circle(radius=0.42, color=RED_B).next_to(latency_track, DOWN, buff=0.45)
        hand = Line(clock.get_center(), clock.get_center() + UP * 0.34, color=RED_B, stroke_width=2.2)
        latency_group = VGroup(latency_title, latency_track, request, response, clock, hand)

        throughput_title = create_text("Throughput: completed requests per second", font_size=11, color=GREEN)
        throughput_title.move_to(RIGHT * 3.0 + UP * 1.7)
        lanes = VGroup()
        done_marks = VGroup()
        for idx in range(4):
            line = Line(LEFT * 0.95, RIGHT * 0.95, color=GRAY_D, stroke_width=3)
            line.move_to(RIGHT * 3.0 + UP * (0.65 - idx * 0.45))
            dot = Dot(line.get_left(), color=GREEN, radius=0.055)
            mark = token_box("ok", color=GREEN, width=0.48, height=0.32).move_to(line.get_right() + RIGHT * 0.45)
            lanes.add(VGroup(line, dot))
            done_marks.add(mark)
        throughput_group = VGroup(throughput_title, lanes, done_marks)
        self.play(FadeIn(latency_group), FadeIn(throughput_group), run_time=0.9)

        self.wait_until(cue_start[4])
        self.play(
            request.animate.move_to(latency_track.get_right()),
            Rotate(hand, angle=-TAU * 0.8, about_point=clock.get_center()),
            *[lane_group[1].animate.move_to(lane_group[0].get_right()) for lane_group in lanes],
            run_time=1.3,
        )
        self.play(FadeIn(done_marks, lag_ratio=0.08), response[0].animate.set_fill("#12331c", opacity=1), run_time=0.7)

        self.wait_until(cue_start[5])
        triangle = Polygon(UP * 1.2, LEFT * 1.55 + DOWN * 1.05, RIGHT * 1.55 + DOWN * 1.05, color=YELLOW, fill_opacity=0.04)
        tri_labels = VGroup(
            create_text("Quality", font_size=10, color=YELLOW).next_to(triangle.get_top(), UP, buff=0.1),
            create_text("Latency", font_size=10, color=RED_B).next_to(triangle.get_left(), LEFT, buff=0.12),
            create_text("Throughput", font_size=10, color=GREEN).next_to(triangle.get_right(), RIGHT, buff=0.12),
        )
        budget_dot = Dot(triangle.get_center(), color=YELLOW, radius=0.085)
        trade = VGroup(triangle, tri_labels, budget_dot).move_to(ORIGIN)
        self.play(FadeOut(VGroup(latency_group, throughput_group)), FadeIn(trade), run_time=0.75)
        self.play(budget_dot.animate.move_to(triangle.get_left() + RIGHT * 0.35 + UP * 0.25), run_time=0.55)
        self.play(budget_dot.animate.move_to(triangle.get_right() + LEFT * 0.45 + UP * 0.2), run_time=0.55)

        self.wait_until(cue_start[6])
        self.play(FadeOut(trade), run_time=0.45)

        hardware_title = create_text("Generation speed is a hardware pipeline", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        pipeline = gpu_vram_pipeline()
        factor_labels = VGroup(
            labeled_box("Capacity", "how much fits in VRAM", width=2.05, height=0.78, color=BLUE_A),
            labeled_box("Compute", "FLOP/s", width=1.65, height=0.78, color=ORANGE),
            labeled_box("Transfer", "GB/s", width=1.65, height=0.78, color=GREEN),
        ).arrange(RIGHT, buff=0.35).move_to(DOWN * 2.2)
        self.play(FadeIn(hardware_title), FadeIn(pipeline[:-1]), FadeIn(factor_labels, lag_ratio=0.1), run_time=1.0)
        self.play(FadeIn(pipeline[-1], lag_ratio=0.05), run_time=0.4)
        self.play(
            *[packet.animate.move_to(pipeline[1][0].get_left() + RIGHT * 0.28 + UP * (idx - 2) * 0.12) for idx, packet in enumerate(pipeline[-1])],
            pipeline[4].animate.set_fill(ORANGE, opacity=0.85),
            run_time=1.25,
        )

        self.wait_until(cue_start[7])
        bottlenecks = VGroup(
            labeled_box("Activations", "load input", width=1.55, height=0.75, color=BLUE_A),
            labeled_box("Weights", "load model", width=1.55, height=0.75, color=BLUE_A),
            labeled_box("Compute", "matmul", width=1.55, height=0.75, color=ORANGE),
            labeled_box("Devices", "communicate", width=1.7, height=0.75, color=PURPLE_A),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 2.2)
        bottleneck_arrow = Arrow(bottlenecks[1].get_top(), pipeline[2].get_center(), color=RED_B, stroke_width=1.6, buff=0.08)
        slow_label = create_text("Slowest stage limits the whole pipeline", font_size=9.5, color=RED_B).next_to(bottlenecks, DOWN, buff=0.2)
        self.play(ReplacementTransform(factor_labels, bottlenecks), FadeIn(slow_label), Create(bottleneck_arrow), run_time=0.9)

        self.wait_until(cue_start[8])
        self.play(FadeOut(VGroup(hardware_title, pipeline, bottlenecks, slow_label, bottleneck_arrow)), run_time=0.55)
        time_title = create_text("Operation time is a race between two limits", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        compute_lane = lane("compute time = operation FLOP / FLOP/s", ORANGE, width=4.0).move_to(UP * 0.55)
        memory_lane = lane("memory time = transferred bytes / bandwidth", BLUE_A, width=4.0).move_to(DOWN * 0.55)
        finish_line = DashedLine(UP * 1.1, DOWN * 1.1, color=GRAY_B).move_to(RIGHT * 2.0)
        max_formula = create_text("Time = max(compute, memory)", font_size=11, color=YELLOW).move_to(
            RIGHT * 2.7 + DOWN * 2.15
        )
        self.play(FadeIn(time_title), FadeIn(compute_lane), FadeIn(memory_lane), Create(finish_line), FadeIn(max_formula), run_time=0.9)
        self.play(compute_lane[1].animate.move_to(compute_lane[0].point_from_proportion(0.48)), run_time=0.65)
        self.play(memory_lane[1].animate.move_to(memory_lane[0].point_from_proportion(0.88)), run_time=1.1)
        memory_wins = SurroundingRectangle(memory_lane, color=RED_B, buff=0.14, stroke_width=2.2)
        self.play(Create(memory_wins), run_time=0.45)

        self.wait_until(cue_start[9])
        h100 = labeled_box(
            "NVIDIA H100 SXM",
            "compute: ~1e15 FLOP/s\nbandwidth: ~3.35e12 B/s",
            width=3.65,
            height=1.08,
            color=YELLOW,
        ).move_to(UP * 1.75)
        byte_bucket = labeled_box("1 Byte", "loaded once", width=1.25, height=0.75, color=BLUE_A).move_to(
            LEFT * 4.05 + DOWN * 1.55
        )
        flop_stack = VGroup(*[Dot(radius=0.028, color=ORANGE) for _ in range(48)]).arrange_in_grid(6, 8, buff=0.05)
        flop_stack.next_to(byte_bucket, RIGHT, buff=0.45)
        self.play(FadeIn(h100), FadeIn(byte_bucket), FadeIn(flop_stack, lag_ratio=0.01), run_time=0.9)

        self.wait_until(cue_start[10])
        threshold = create_text(">100 FLOP/byte: compute is almost free vs transfer", font_size=9, color=GREEN)
        threshold.next_to(VGroup(byte_bucket, flop_stack), DOWN, buff=0.25)
        green_ring = SurroundingRectangle(VGroup(byte_bucket, flop_stack), color=GREEN, buff=0.16, stroke_width=2.0)
        self.play(FadeIn(threshold), Create(green_ring), run_time=0.75)

        self.wait_until(cue_start[11])
        self.play(FadeOut(VGroup(time_title, compute_lane, memory_lane, finish_line, max_formula, memory_wins, h100, byte_bucket, flop_stack, threshold, green_ring)), run_time=0.55)

        opt_title = create_text("Single decoding step: reduce the slow work", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        bytes_before = progress_bar("loaded bytes", 0.9, BLUE_A, width=2.1)
        bytes_after = progress_bar("after quantization/distillation", 0.38, GREEN, width=2.1)
        bandwidth_demo = VGroup(labeled_box("Bandwidth", "move fewer bytes", width=2.15, color=BLUE_A), bytes_before, bytes_after)
        bandwidth_demo.arrange(DOWN, buff=0.22).move_to(LEFT * 3.8 + DOWN * 0.25)

        util_grid = VGroup(*[Square(side_length=0.2, color=ORANGE, fill_color=ORANGE, fill_opacity=0.18) for _ in range(16)])
        util_grid.arrange_in_grid(4, 4, buff=0.06)
        flash_demo = VGroup(
            labeled_box("FLOP/s", "FlashAttention\n[Dao et al., 2022]", width=2.15, color=ORANGE),
            util_grid,
            create_text("Same ops, higher utilization", font_size=7.7, color=ORANGE),
        ).arrange(DOWN, buff=0.16).move_to(DOWN * 0.25)

        experts = VGroup(*[Circle(radius=0.16, color=GRAY_C, fill_color="#191b1e", fill_opacity=0.95) for _ in range(6)])
        experts.arrange(RIGHT, buff=0.1)
        route = Arrow(LEFT * 0.55, RIGHT * 0.55, color=GREEN, stroke_width=1.3)
        moe_demo = VGroup(
            labeled_box("FLOP", "Mixture-of-Experts\n[Fedus et al., 2022]", width=2.35, color=GREEN),
            VGroup(route, experts),
            create_text("Activate only selected experts", font_size=7.7, color=GREEN),
        ).arrange(DOWN, buff=0.16).move_to(RIGHT * 3.8 + DOWN * 0.25)

        self.play(FadeIn(opt_title), FadeIn(bandwidth_demo), run_time=0.8)
        self.play(Transform(bytes_before[1], bytes_after[1].copy()), FadeIn(bytes_after[2]), run_time=0.75)
        self.play(FadeIn(flash_demo), util_grid.animate.set_fill(ORANGE, opacity=0.8), run_time=0.85)
        self.play(FadeIn(moe_demo), experts[1].animate.set_color(GREEN), experts[4].animate.set_color(GREEN), run_time=0.85)

        self.wait_until(cue_start[12])
        self.play(FadeOut(VGroup(opt_title, bandwidth_demo, flash_demo, moe_demo)), run_time=0.5)

        bound_title = create_text("Compute-bound vs memory-bound", font_size=12, color=YELLOW).next_to(sub_title, DOWN, buff=0.35)
        compute_bound = VGroup(
            labeled_box("Compute-bound", "many FLOPs", width=2.25, color=ORANGE),
            progress_bar("compute branch", 0.86, ORANGE, width=2.45),
            progress_bar("memory branch", 0.34, BLUE_A, width=2.45),
        ).arrange(DOWN, buff=0.2).move_to(LEFT * 3.0 + DOWN * 0.3)
        compute_ring = SurroundingRectangle(compute_bound[1], color=ORANGE, buff=0.12, stroke_width=2.0)
        self.play(FadeIn(bound_title), FadeIn(compute_bound), Create(compute_ring), run_time=0.9)

        self.wait_until(cue_start[13])
        memory_bound = VGroup(
            labeled_box("Memory-bound", "processor waits", width=2.25, color=BLUE_A),
            progress_bar("compute branch", 0.32, ORANGE, width=2.45),
            progress_bar("memory branch", 0.9, BLUE_A, width=2.45),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.0 + DOWN * 0.3)
        idle = create_text("Wait", font_size=10, color=RED_B).next_to(memory_bound[0], LEFT, buff=0.22)
        memory_ring = SurroundingRectangle(memory_bound[2], color=RED_B, buff=0.12, stroke_width=2.0)
        self.play(FadeIn(memory_bound), FadeIn(idle), Create(memory_ring), run_time=0.9)

        self.wait_until(cue_start[14])
        rule = create_text("The longer branch controls the operation", font_size=10, color=YELLOW).move_to(DOWN * 2.35)
        self.play(FadeIn(rule), run_time=0.7)

        self.wait_until(cue_start[15])
        self.play(FadeOut(VGroup(bound_title, compute_bound, compute_ring, memory_bound, memory_ring, idle, rule)), run_time=0.5)

        batch_title = create_text("Batching amortizes weight loading", font_size=12, color=YELLOW).next_to(sub_title, DOWN, buff=0.35)
        no_batch_title = create_text("Without batching", font_size=9.5, color=RED_B).move_to(LEFT * 3.1 + UP * 1.15)
        with_batch_title = create_text("With batching", font_size=9.5, color=GREEN).move_to(RIGHT * 3.1 + UP * 1.15)
        repeated_loads = VGroup(*[labeled_box("Weights", "", width=1.25, height=0.45, color=BLUE_A) for _ in range(4)]).arrange(DOWN, buff=0.16)
        repeated_reqs = VGroup(*[token_box(f"r{i+1}", color=RED_B, width=0.55, height=0.36) for i in range(4)]).arrange(DOWN, buff=0.25)
        left_batch = VGroup(repeated_loads, repeated_reqs.arrange(DOWN, buff=0.25).next_to(repeated_loads, RIGHT, buff=0.35)).move_to(LEFT * 3.1 + DOWN * 0.35)
        shared_load = labeled_box("Weights", "load once", width=1.45, height=0.75, color=BLUE_A).move_to(RIGHT * 2.0 + DOWN * 0.35)
        batch_reqs = VGroup(*[token_box(f"r{i+1}", color=GREEN, width=0.55, height=0.36) for i in range(4)]).arrange(DOWN, buff=0.16)
        batch_reqs.next_to(shared_load, RIGHT, buff=0.65)
        fanout = VGroup(*[Arrow(shared_load.get_right(), row.get_left(), color=GREEN, stroke_width=1.2, buff=0.06) for row in batch_reqs])
        self.play(FadeIn(batch_title), FadeIn(no_batch_title), FadeIn(left_batch, lag_ratio=0.08), run_time=0.9)

        self.wait_until(cue_start[16])
        self.play(FadeIn(with_batch_title), FadeIn(shared_load), FadeIn(batch_reqs, lag_ratio=0.08), Create(fanout), run_time=0.9)
        saved = create_text("Same weight load feeds many inputs", font_size=9.5, color=GREEN).move_to(DOWN * 2.1)
        self.play(FadeIn(saved), run_time=0.5)

        self.wait_until(cue_start[17])
        x_marks = VGroup()
        for idx in [1, 2, 3]:
            x_marks.add(Cross(repeated_loads[idx], stroke_color=RED_B, stroke_width=3))
        free_note = create_text("Extra memory-transfer cost stays small", font_size=9.5, color=GREEN).move_to(DOWN * 2.45)
        self.play(Create(x_marks), Transform(saved, free_note), run_time=0.8)

        self.wait_until(cue_start[18])
        self.play(FadeOut(VGroup(batch_title, no_batch_title, left_batch, with_batch_title, shared_load, batch_reqs, fanout, x_marks, saved)), run_time=0.5)

        kv_title = create_text("KV cache removes repeated prefix work", font_size=12, color=YELLOW).next_to(sub_title, DOWN, buff=0.35)
        prefix = VGroup(*[token_box(f"t{i+1}", color=GRAY_C) for i in range(4)]).arrange(RIGHT, buff=0.12)
        prefix.move_to(LEFT * 2.8 + DOWN * 0.35)
        no_cache = labeled_box("Without cache", "recompute K,V\nfor old prefix", width=2.25, height=1.0, color=RED_B)
        no_cache.next_to(prefix, UP, buff=0.4)
        recompute = VGroup(*[Arrow(tok.get_top(), no_cache.get_bottom(), color=RED_B, stroke_width=1.2, buff=0.07) for tok in prefix])
        cache_label = labeled_box("KV cache", "store old K,V", width=2.1, height=0.8, color=GREEN).move_to(RIGHT * 3.0 + UP * 0.7)
        cache = kv_rows(4, GREEN).next_to(cache_label, DOWN, buff=0.25)
        self.play(FadeIn(kv_title), FadeIn(prefix), FadeIn(no_cache), Create(recompute), run_time=0.9)
        self.play(FadeIn(cache_label), FadeIn(cache, lag_ratio=0.08), run_time=0.75)

        self.wait_until(cue_start[19])
        prefill = labeled_box("Prefill", "prompt -> cache", width=1.8, height=0.78, color=BLUE_A).move_to(LEFT * 3.7 + DOWN * 2.0)
        decode = labeled_box("Decode", "append only new K,V", width=2.25, height=0.78, color=YELLOW).move_to(LEFT * 0.5 + DOWN * 2.0)
        new_row = Rectangle(width=1.85, height=0.2, color=YELLOW, fill_color=YELLOW, fill_opacity=0.38, stroke_width=1.1)
        new_row.move_to(decode.get_right() + RIGHT * 0.7)
        append = Arrow(new_row.get_right(), cache.get_bottom() + DOWN * 0.28, color=YELLOW, stroke_width=1.4, buff=0.06)
        old_fade = VGroup(no_cache, recompute)
        self.play(FadeOut(old_fade), FadeIn(prefill), FadeIn(decode), FadeIn(new_row), run_time=0.8)
        self.play(Create(append), new_row.animate.move_to(cache.get_bottom() + DOWN * 0.28), run_time=1.0)

        self.wait_until(cue_start[20])
        self.play(FadeOut(VGroup(kv_title, prefix, cache_label, cache, prefill, decode, new_row, append)), run_time=0.45)
        size_title = create_text("KV cache helps speed, but consumes VRAM", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        formula = create_text("Size = (batch x n_ctx) x model factors x bytes", font_size=11, color=YELLOW).move_to(UP * 1.35)
        tank = RoundedRectangle(width=5.9, height=1.0, color=BLUE_A, fill_color="#101826", fill_opacity=0.85, corner_radius=0.07)
        tank.move_to(DOWN * 0.1)
        chunks = VGroup()
        for idx, color in enumerate([GREEN, GREEN, YELLOW, RED_B]):
            chunk = Rectangle(width=1.18, height=0.78, color=color, fill_color=color, fill_opacity=0.55, stroke_width=0.8)
            chunk.move_to(tank.get_left() + RIGHT * (0.72 + idx * 1.32))
            chunks.add(chunk)
        batch_slider = progress_bar("batch", 0.62, YELLOW, width=2.1).move_to(LEFT * 1.45 + DOWN * 1.55)
        ctx_slider = progress_bar("context length", 0.82, YELLOW, width=2.1).move_to(RIGHT * 1.45 + DOWN * 1.55)
        bottleneck = create_text("Larger batch/context -> cache fills VRAM", font_size=10, color=RED_B).move_to(DOWN * 2.35)
        self.play(FadeIn(size_title), FadeIn(formula), FadeIn(tank), run_time=0.75)
        self.play(FadeIn(chunks, lag_ratio=0.1), FadeIn(batch_slider), FadeIn(ctx_slider), FadeIn(bottleneck), run_time=1.0)
        self.play(chunks[-1].animate.set_fill(RED_B, opacity=0.85), tank.animate.set_color(RED_B), run_time=0.65)

        self.wait_until(voiceover_end + 0.2)
        self.play(FadeOut(VGroup(size_title, formula, tank, chunks, batch_slider, ctx_slider, bottleneck, sub_title)), run_time=0.8)

        assert_all_scene_voiceovers_played(self)
