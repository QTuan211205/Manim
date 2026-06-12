import os
import tempfile
from pathlib import Path
import numpy as np
from manim import *

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_4_3_DURATIONS = {
    "sc43_001.mp3": 10.124,
    "sc43_002.mp3": 5.387,
    "sc43_003.mp3": 6.687,
    "sc43_004.mp3": 3.715,
    "sc43_005.mp3": 6.734,
    "sc43_006.mp3": 7.663,
    "sc43_007.mp3": 4.598,
    "sc43_008.mp3": 7.663,
    "sc43_009.mp3": 4.923,
    "sc43_010.mp3": 8.777,
    "sc43_011.mp3": 7.198,
    "sc43_012.mp3": 3.762,
    "sc43_013.mp3": 3.065,
    "sc43_014.mp3": 11.006,
    "sc43_015.mp3": 5.248,
    "sc43_016.mp3": 3.390,
    "sc43_017.mp3": 5.201,
    "sc43_018.mp3": 4.923,
    "sc43_019.mp3": 8.173,
    "sc43_020.mp3": 4.458,
    "sc43_021.mp3": 10.635,
    "sc43_022.mp3": 4.133,
    "sc43_023.mp3": 15.836,
    "sc43_024.mp3": 6.873,
    "sc43_025.mp3": 4.783,
    "sc43_026.mp3": 4.412,
    "sc43_027.mp3": 7.941,
    "sc43_028.mp3": 14.907,
    "sc43_029.mp3": 10.031,
    "sc43_030.mp3": 4.969,
    "sc43_031.mp3": 10.124,
    "sc43_032.mp3": 6.827,
}
SCENE_4_3_VOICEOVERS = tuple(SCENE_4_3_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc43_*.mp3"))
    expected = sorted(SCENE_4_3_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 4.3 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_4_3_DURATIONS:
        raise KeyError(f"Unexpected Scene 4.3 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 4.3 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_4_3_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_4_3_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 4.3 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


def create_text(text, font_size=24, font="Segoe UI", color=WHITE, **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    t = Text(text, font_size=base_size, font=font, color=color, **kwargs)
    t.scale(scale_factor)
    return t


def create_markup_text(text, font_size=24, font="Segoe UI", **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    t = MarkupText(text, font_size=base_size, font=font, **kwargs)
    t.scale(scale_factor)
    return t


class Scene4_3(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (filename, duration) in enumerate(SCENE_4_3_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        # =====================================================================
        # CHAPTER TITLE & HEADER
        # =====================================================================
        chapter_title = create_text("Chapter 4: Systems Efficiency", font_size=22, color=YELLOW)
        chapter_sub = create_text("Part 4.3: Shared Prefix Optimizations", font_size=16, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        sub_title = create_text("Shared prefix optimization (Shared Prefix)", font_size=13, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)

        # Cue 1 (sc43_001): How to speed up meta-generation title
        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait_until(cue_start[2])

        # Cue 2 (sc43_002): shared prefix redundant prompts
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )

        step1_title = create_markup_text(
            "<b>1. Redundant KV Cache problem (Redundant KV Cache)</b>",
            font_size=12, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(step1_title), run_time=1.2)

        prompt_boxes = VGroup()
        for idx in range(3):
            box = RoundedRectangle(width=3.2, height=0.8, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            box.move_to(LEFT * (3.5 * (1 - idx)) + UP * 0.8)
            
            sys_part = RoundedRectangle(width=1.8, height=0.6, color=GRAY_B, fill_color=GRAY_E, fill_opacity=0.7, corner_radius=0.03)
            sys_part.move_to(box.get_center() + LEFT * 0.55)
            sys_lbl = create_text("System Prompt (1000t)", font_size=6, color=WHITE).move_to(sys_part.get_center())
            sys_grp = VGroup(sys_part, sys_lbl)
            
            query_part = RoundedRectangle(width=0.9, height=0.6, color=YELLOW_D, fill_color=YELLOW_E, fill_opacity=0.7, corner_radius=0.03)
            query_part.move_to(box.get_center() + RIGHT * 0.95)
            query_lbl = create_text(f"Query {idx+1}", font_size=6, color=WHITE).move_to(query_part.get_center())
            query_grp = VGroup(query_part, query_lbl)
            
            prompt_boxes.add(VGroup(box, sys_grp, query_grp))

        self.play(FadeIn(prompt_boxes, shift=DOWN * 0.2), run_time=1.2)
        self.wait_until(cue_start[3])

        # =====================================================================
        # Cue 3 (sc43_003): PagedAttention block mapping
        # =====================================================================
        self.play(
            FadeOut(step1_title),
            FadeOut(prompt_boxes),
            run_time=0.8
        )

        step2_title = create_markup_text(
            "<b>2. PagedAttention solution (vLLM) — Share physical blocks</b>",
            font_size=12, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(step2_title), run_time=1.0)

        logical_blocks = VGroup()
        for idx in range(3):
            lbl_box = RoundedRectangle(width=2.5, height=0.5, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.03)
            lbl_box.move_to(LEFT * 3.5 + UP * (0.6 - 0.7 * idx))
            lbl_txt = create_text(f"Block Logic {idx+1}", font_size=8, color=WHITE).move_to(lbl_box.get_center())
            logical_blocks.add(VGroup(lbl_box, lbl_txt))
            
        physical_block = RoundedRectangle(width=3.2, height=1.0, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.04)
        physical_block.move_to(RIGHT * 2.5 + UP * 0.0)
        physical_lbl = create_markup_text(
            "<b>Physical Block (Physical Block)</b>\n<span foreground=\"#33FF55\">Stores the only KV Cache copy\nof the system prompt in VRAM</span>",
            font_size=6.5, color=WHITE, line_spacing=1.2
        ).move_to(physical_block.get_center())
        physical_grp = VGroup(physical_block, physical_lbl)

        mapping_arrows = VGroup()
        for idx in range(3):
            arrow = Arrow(start=logical_blocks[idx].get_right(), end=physical_block.get_left(), color=GREEN, stroke_width=2)
            mapping_arrows.add(arrow)

        paged_note = create_markup_text(
            "PagedAttention works like <b>Virtual Memory (Virtual Memory)</b>:\n"
            "Map many logical request streams to the same shared physical memory block.\n"
            "<span foreground=\"#33FF55\">=> Saves substantial memory, enabling larger batch sizes.</span>",
            font_size=8, color=WHITE, line_spacing=1.3
        ).move_to(DOWN * 1.8)

        self.play(
            FadeIn(logical_blocks, shift=RIGHT * 0.2),
            FadeIn(physical_grp, shift=LEFT * 0.2),
            run_time=1.2
        )
        self.play(
            LaggedStart(*[Create(a) for a in mapping_arrows], lag_ratio=0.2),
            run_time=1.0
        )
        self.play(Write(paged_note), run_time=1.2)
        self.wait_until(cue_start[4])

        # =====================================================================
        # Cue 4-5 (sc43_004, sc43_005): Multi-level prefix sharing, few-shot prompt + Best-of-N tree
        # =====================================================================
        self.play(
            FadeOut(step2_title),
            FadeOut(logical_blocks),
            FadeOut(physical_grp),
            FadeOut(mapping_arrows),
            FadeOut(paged_note),
            run_time=0.8
        )

        step3_title = create_markup_text(
            "<b>3. RadixAttention (SGLang) — multi-level prefix tree &amp; LRU Eviction</b>",
            font_size=12, color=YELLOW
        ).move_to(UP * 2.0)
        self.play(Write(step3_title), run_time=1.0)

        root_rect = RoundedRectangle(width=3.6, height=0.55, color=BLUE, fill_color="#14202b", fill_opacity=0.9, corner_radius=0.04)
        root_rect.move_to(UP * 1.0)
        root_lbl = create_text("Root: System Prompt (1000t)", font_size=8, color=BLUE_A).move_to(root_rect.get_center())
        root_node = VGroup(root_rect, root_lbl)

        fewshot_rect = RoundedRectangle(width=3.2, height=0.5, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.04)
        fewshot_rect.move_to(UP * 0.0)
        fewshot_lbl = create_text("Few-shot Examples (500t)", font_size=8, color=GREEN_A).move_to(fewshot_rect.get_center())
        fewshot_node = VGroup(fewshot_rect, fewshot_lbl)

        qa_rect = RoundedRectangle(width=2.0, height=0.45, color=YELLOW, fill_color="#2b2b14", fill_opacity=0.9, corner_radius=0.03)
        qa_rect.move_to(LEFT * 2.4 + DOWN * 0.9)
        qa_lbl = create_text("Question A (100t)", font_size=7, color=YELLOW_A).move_to(qa_rect.get_center())
        qa_node = VGroup(qa_rect, qa_lbl)

        qb_rect = RoundedRectangle(width=2.0, height=0.45, color=YELLOW, fill_color="#2b2b14", fill_opacity=0.9, corner_radius=0.03)
        qb_rect.move_to(RIGHT * 2.4 + DOWN * 0.9)
        qb_lbl = create_text("Question B (100t)", font_size=7, color=YELLOW_A).move_to(qb_rect.get_center())
        qb_node = VGroup(qb_rect, qb_lbl)

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

        line_root_few = Line(root_rect.get_bottom(), fewshot_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_few_qa = Line(fewshot_rect.get_bottom(), qa_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_few_qb = Line(fewshot_rect.get_bottom(), qb_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_qa_ansa1 = Line(qa_rect.get_bottom(), ansa1_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_qa_ansa2 = Line(qa_rect.get_bottom(), ansa2_rect.get_top(), color=GRAY_C, stroke_width=1.5)
        line_qb_ansb1 = Line(qb_rect.get_bottom(), ansb1_rect.get_top(), color=GRAY_C, stroke_width=1.5)

        tree_lines = VGroup(line_root_few, line_few_qa, line_few_qb, line_qa_ansa1, line_qa_ansa2, line_qb_ansb1)
        tree_nodes = VGroup(root_node, fewshot_node, qa_node, qb_node, ansa1_node, ansa2_node, ansb1_node)

        self.play(
            LaggedStart(
                *[Create(l) for l in tree_lines],
                *[FadeIn(n) for n in tree_nodes],
                lag_ratio=0.1
            ),
            run_time=1.5
        )
        
        self.wait_until(cue_start[5])
        search_dot = Dot(color=YELLOW, radius=0.08)
        search_dot.move_to(root_rect.get_center())
        
        self.play(FadeIn(search_dot), run_time=0.3)
        self.play(search_dot.animate.move_to(fewshot_rect.get_center()), run_time=0.6)
        self.play(search_dot.animate.move_to(qa_rect.get_center()), run_time=0.6)
        self.play(search_dot.animate.move_to(ansa1_rect.get_center()), run_time=0.6)
        self.play(FadeOut(search_dot), run_time=0.3)
        self.wait_until(cue_start[6])

        # =====================================================================
        # Cue 6 (sc43_006): RadixAttention radix tree LRU Eviction
        # =====================================================================
        evict_lbl = create_markup_text(
            "<b>LRU eviction mechanism:</b> When memory is full, the least recently used leaf nodes\n"
            "are evicted first (for example <b>Answer B1</b>) to make room for new requests.",
            font_size=8, color=RED, line_spacing=1.25
        ).move_to(DOWN * 2.5)
        
        self.play(Write(evict_lbl), run_time=1.0)
        self.play(
            ansb1_rect.animate.set_color(RED).set_fill(RED, opacity=0.3),
            ansb1_lbl.animate.set_color(RED),
            run_time=0.6
        )
        self.play(Flash(ansb1_rect, color=RED, num_lines=8, flash_radius=0.4), run_time=0.6)
        
        self.play(
            FadeOut(ansb1_node),
            FadeOut(line_qb_ansb1),
            run_time=0.8
        )
        self.wait_until(cue_start[7])

        # =====================================================================
        # Cue 7 (sc43_007): Hydragen Tensor Cores attention speedup
        # =====================================================================
        self.play(
            FadeOut(step3_title),
            FadeOut(tree_nodes),
            FadeOut(tree_lines),
            FadeOut(evict_lbl),
            run_time=0.8
        )

        step4_title = create_text("4. Using Tensor Cores: How Hydragen Works", font_size=13, color=YELLOW)
        step4_title.to_edge(UP, buff=0.4)
        self.play(ReplacementTransform(sub_title, step4_title), run_time=1.0)

        trad_title = create_text("1. Traditional method (vLLM / SGLang):", font_size=9, color=RED).move_to(LEFT * 3.5 + UP * 1.3, aligned_edge=LEFT)
        trad_formula = create_markup_text(
            "<span foreground=\"#FF3333\">q<sub>i</sub> * K<sup>T</sup></span>  (for each stream <i>i</i>)",
            font_size=9.5, font="Consolas"
        ).next_to(trad_title, DOWN, buff=0.15, aligned_edge=LEFT)
        
        trad_desc = create_markup_text(
            "• Multiplication <b>Matrix-Vector</b> independently.\n"
            "• The prefix KV Cache must be loaded from VRAM into\n"
            "  the processor multiple times (limited by <i>Memory-bound</i>).",
            font_size=7, color=GRAY_A, line_spacing=1.2
        ).next_to(trad_formula, DOWN, buff=0.15, aligned_edge=LEFT)
        trad_grp = VGroup(trad_title, trad_formula, trad_desc)

        hydra_title = create_text("2. Hydragen solution:", font_size=9, color=GREEN).move_to(LEFT * 3.5 + DOWN * 0.5, aligned_edge=LEFT)
        hydra_formula = create_markup_text(
            "<span foreground=\"#33FF55\">Q<sub>batch</sub> * K<sup>T</sup></span>  (Matrix-Matrix)",
            font_size=9.5, font="Consolas"
        ).next_to(hydra_title, DOWN, buff=0.15, aligned_edge=LEFT)
        
        hydra_desc = create_markup_text(
            "• Merge stream queries into matrix <b>Q</b>.\n"
            "• Load the prefix KV Cache into registers exactly once.\n"
            "• Multiplication <b>Matrix-Matrix</b> very fast thanks to\n"
            "  using cores <b>Tensor Cores</b> (<i>Compute-bound</i>).",
            font_size=7, color=GRAY_A, line_spacing=1.2
        ).next_to(hydra_formula, DOWN, buff=0.15, aligned_edge=LEFT)
        hydra_grp = VGroup(hydra_title, hydra_formula, hydra_desc)

        axes = Axes(
            x_range=[0, 8, 2],
            y_range=[0, 8, 2],
            x_length=4.5,
            y_length=3.0,
            axis_config={"color": GRAY_C, "stroke_width": 2},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        ).move_to(RIGHT * 3.2 + DOWN * 0.4)

        graph_title = create_text("Throughput vs. Batch Size", font_size=8.5, color=YELLOW).next_to(axes, UP, buff=0.2)
        x_lbl = create_text("Batch Size", font_size=7, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.15)
        y_lbl = create_text("Throughput", font_size=7, color=GRAY_A).next_to(axes.y_axis, LEFT, buff=0.15).rotate(90 * DEGREES)

        vllm_curve = axes.plot(lambda x: 0.5 + 0.9 * (x**0.55), x_range=[0, 8], color=RED, stroke_width=3)
        hydragen_curve = axes.plot(lambda x: 0.5 + 1.8 * (x**0.65), x_range=[0, 8], color=GREEN, stroke_width=4)
        upper_bound = DashedLine(
            start=axes.c2p(0, 7.2), end=axes.c2p(8, 7.2),
            color=BLUE, stroke_width=2
        )
        upper_lbl = create_text("Theoretical limit (Attention-free)", font_size=6, color=BLUE).next_to(upper_bound, UP, buff=0.05).shift(LEFT * 0.4)

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
            run_time=1.0
        )
        self.play(
            FadeIn(hydra_grp, shift=RIGHT * 0.25),
            run_time=1.0
        )
        self.play(
            Create(axes), Write(graph_title), Write(x_lbl), Write(y_lbl),
            run_time=1.0
        )
        self.play(
            Create(vllm_curve), Create(hydragen_curve),
            Create(upper_bound), FadeIn(upper_lbl),
            FadeIn(legend),
            run_time=1.2
        )
        self.wait_until(cue_start[8])

        # =====================================================================
        # Cue 8 (sc43_008): Token Dropping (KV cache size formula bottleneck)
        # =====================================================================
        self.play(
            FadeOut(trad_grp), FadeOut(hydra_grp),
            FadeOut(axes), FadeOut(graph_title), FadeOut(x_lbl), FadeOut(y_lbl),
            FadeOut(vllm_curve), FadeOut(hydragen_curve),
            FadeOut(upper_bound), FadeOut(upper_lbl),
            FadeOut(legend),
            FadeOut(step4_title),
            run_time=0.8
        )

        step5_title = create_text("5. Token Dropping (Token Dropping)", font_size=13, color=YELLOW)
        step5_title.to_edge(UP, buff=0.4)
        self.play(Write(step5_title), run_time=1.0)

        formula_bg = RoundedRectangle(width=8.5, height=0.6, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04).move_to(UP * 1.0)
        formula_lbl = create_markup_text(
            'Size = (batch * <span foreground="#FF3333">n<sub>ctx</sub></span>) * (2 * n<sub>layer</sub> * n<sub>heads</sub> * head<sub>dim</sub>) * n<sub>bytes</sub>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeIn(formula_bg, shift=DOWN * 0.2), FadeIn(formula_lbl, shift=DOWN * 0.2), run_time=1.0)

        tokens = VGroup()
        for i in range(8):
            tok = RoundedRectangle(width=0.8, height=0.65, color=GRAY_D, fill_color="#1e2025", fill_opacity=0.9, corner_radius=0.04)
            tok.move_to(LEFT * (3.5 - 1.0 * i) + DOWN * 0.2)
            lbl = create_text(f"T{i+1}", font_size=8, color=WHITE).move_to(tok.get_center())
            tokens.add(VGroup(tok, lbl))
        self.play(FadeIn(tokens, shift=UP * 0.1), run_time=1.0)

        scores = [0.05, 0.42, 0.08, 0.35, 0.03, 0.51, 0.07, 0.48]
        score_labels = VGroup()
        for i, s in enumerate(scores):
            col = RED if s < 0.1 else GREEN
            score_lbl = create_text(f"{s:.2f}", font_size=7, color=col).next_to(tokens[i], DOWN, buff=0.1)
            score_labels.add(score_lbl)
        self.play(FadeIn(score_labels, shift=UP * 0.15), run_time=1.0)

        drop_indices = [0, 2, 4, 6]
        self.play(
            *[tokens[idx][0].animate.set_color(RED).set_fill(RED, opacity=0.3) for idx in drop_indices],
            run_time=0.6
        )
        self.play(
            *[FadeOut(tokens[idx]) for idx in drop_indices],
            *[FadeOut(score_labels[idx]) for idx in drop_indices],
            run_time=0.6
        )

        keep_indices = [1, 3, 5, 7]
        self.play(
            *[tokens[idx].animate.move_to(LEFT * (1.5 - 1.0 * i) + DOWN * 0.2) for i, idx in enumerate(keep_indices)],
            *[score_labels[idx].animate.move_to(LEFT * (1.5 - 1.0 * i) + DOWN * 0.7) for i, idx in enumerate(keep_indices)],
            run_time=0.8
        )

        formula_lbl_new = create_markup_text(
            'Size = (batch * <span foreground="#FF3333">n<sub>ctx</sub> (reduced 50%)</span>) * (2 * n<sub>layer</sub> * n<sub>heads</sub> * head<sub>dim</sub>) * n<sub>bytes</sub>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeOut(formula_lbl), FadeIn(formula_lbl_new), run_time=0.6)
        formula_lbl = formula_lbl_new

        warning_box = RoundedRectangle(width=9.5, height=0.75, color=ORANGE, fill_color="#2b1b14", fill_opacity=0.9, corner_radius=0.04).move_to(DOWN * 1.9)
        warning_lbl = create_markup_text(
            '<b>Limitation:</b> The model can easily lose context (brittle) if an important token is dropped by mistake\n'
            'or when the discussion content changes abruptly (because the corresponding KV Cache vector was deleted).',
            font_size=7, color=WHITE, line_spacing=1.2
        ).move_to(warning_box.get_center())
        warning_grp = VGroup(warning_box, warning_lbl)
        self.play(FadeIn(warning_grp, shift=UP * 0.2), run_time=1.0)
        self.wait_until(cue_start[9])

        # =====================================================================
        # Cue 9 (sc43_009): KV Cache Quantization
        # =====================================================================
        self.play(
            FadeOut(step5_title), FadeOut(formula_bg), FadeOut(formula_lbl),
            *[FadeOut(tokens[idx]) for idx in keep_indices],
            *[FadeOut(score_labels[idx]) for idx in keep_indices],
            FadeOut(warning_grp),
            run_time=0.8
        )

        step6_title = create_text("6. KV Cache Quantization (KV Cache Quantization)", font_size=13, color=YELLOW)
        step6_title.to_edge(UP, buff=0.4)
        self.play(Write(step6_title), run_time=1.0)

        formula_bg = RoundedRectangle(width=8.5, height=0.6, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04).move_to(UP * 1.0)
        formula_lbl = create_markup_text(
            'Size = (batch * n<sub>ctx</sub>) * (2 * n<sub>layer</sub> * n<sub>heads</sub> * head<sub>dim</sub>) * <span foreground="#33FF55">n<sub>bytes</sub></span>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeIn(formula_bg, shift=DOWN * 0.2), FadeIn(formula_lbl, shift=DOWN * 0.2), run_time=1.0)

        fp16_box = RoundedRectangle(width=3.6, height=0.8, color=BLUE, fill_color="#14202b", fill_opacity=0.9, corner_radius=0.04).move_to(LEFT * 2.2 + DOWN * 0.3)
        fp16_lbl = create_markup_text("<b>FP16 (2 Bytes)</b>\nInitially high precision", font_size=7.5, color=WHITE).move_to(fp16_box.get_center())
        fp16_grp = VGroup(fp16_box, fp16_lbl)
        self.play(FadeIn(fp16_grp, shift=RIGHT * 0.25), run_time=1.0)

        arrow = Arrow(start=fp16_box.get_right(), end=RIGHT * 0.2 + DOWN * 0.3, color=GREEN, stroke_width=2.5)
        int8_box = RoundedRectangle(width=1.8, height=0.8, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.04).move_to(RIGHT * 1.3 + DOWN * 0.3)
        int8_lbl = create_markup_text("<b>INT8 (1B)</b>\n2x compression", font_size=7, color=WHITE).move_to(int8_box.get_center())
        int8_grp = VGroup(int8_box, int8_lbl)

        int4_box = RoundedRectangle(width=0.9, height=0.8, color=YELLOW, fill_color="#2b2b14", fill_opacity=0.9, corner_radius=0.04).move_to(RIGHT * 3.1 + DOWN * 0.3)
        int4_lbl = create_markup_text("<b>INT4</b>\n4x compression", font_size=6, color=WHITE).move_to(int4_box.get_center())
        int4_grp = VGroup(int4_box, int4_lbl)

        self.play(Create(arrow), FadeIn(int8_grp, shift=RIGHT * 0.2), run_time=1.0)
        self.play(FadeIn(int4_grp, shift=RIGHT * 0.2), run_time=0.8)

        formula_lbl_new = create_markup_text(
            'Size = (batch * n<sub>ctx</sub>) * (2 * n<sub>layer</sub> * n<sub>heads</sub> * head<sub>dim</sub>) * <span foreground="#33FF55">n<sub>bytes</sub> (reduced 2x - 4x)</span>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeOut(formula_lbl), FadeIn(formula_lbl_new), run_time=0.6)
        formula_lbl = formula_lbl_new

        benefit_box = RoundedRectangle(width=9.5, height=0.75, color=GREEN, fill_color="#142b18", fill_opacity=0.9, corner_radius=0.04).move_to(DOWN * 1.9)
        benefit_lbl = create_markup_text(
            '<b>Benefit:</b> Allows storing more KV Cache vectors on the same GPU.\n'
            '<span foreground="#33FF55">=> Run larger batch sizes and maximize throughput.</span>',
            font_size=7, color=WHITE, line_spacing=1.2
        ).move_to(benefit_box.get_center())
        benefit_grp = VGroup(benefit_box, benefit_lbl)
        self.play(FadeIn(benefit_grp, shift=UP * 0.2), run_time=1.0)
        self.wait_until(cue_start[10])

        # =====================================================================
        # Cue 10 (sc43_010): Multi-Query / Grouped-Query Attention
        # =====================================================================
        self.play(
            FadeOut(step6_title), FadeOut(formula_bg), FadeOut(formula_lbl),
            FadeOut(fp16_grp), FadeOut(arrow), FadeOut(int8_grp), FadeOut(int4_grp),
            FadeOut(benefit_grp),
            run_time=0.8
        )

        step7_title = create_text("7. Structural optimization: Multi-Query & Grouped-Query Attention", font_size=13, color=YELLOW)
        step7_title.to_edge(UP, buff=0.4)
        self.play(Write(step7_title), run_time=1.0)

        formula_bg = RoundedRectangle(width=8.5, height=0.6, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04).move_to(UP * 1.1)
        formula_lbl = create_markup_text(
            'Size = (batch * n<sub>ctx</sub>) * (2 * n<sub>layer</sub> * <span foreground="#33CCFF">n<sub>heads</sub></span> * head<sub>dim</sub>) * n<sub>bytes</sub>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeIn(formula_bg, shift=DOWN * 0.2), FadeIn(formula_lbl, shift=DOWN * 0.2), run_time=1.0)

        mha_lbl = create_text("MHA (Traditional)", font_size=7, color=WHITE).move_to(LEFT * 4.0 + UP * 0.25)
        mha_q_heads = VGroup(*[Circle(radius=0.08, color=ORANGE, fill_color=ORANGE, fill_opacity=0.8).move_to(LEFT * 4.4 + UP * (0.0 - 0.25 * j)) for j in range(4)])
        mha_kv_heads = VGroup(*[Circle(radius=0.08, color=GREEN, fill_color=GREEN, fill_opacity=0.8).move_to(LEFT * 3.6 + UP * (0.0 - 0.25 * j)) for j in range(4)])
        mha_lines = VGroup(*[Line(mha_q_heads[j].get_right(), mha_kv_heads[j].get_left(), color=GRAY_B, stroke_width=1.2) for j in range(4)])
        mha_grp = VGroup(mha_lbl, mha_q_heads, mha_kv_heads, mha_lines)

        mqa_lbl = create_text("MQA (Multi-Query)", font_size=7, color=WHITE).move_to(UP * 0.25)
        mqa_q_heads = VGroup(*[Circle(radius=0.08, color=ORANGE, fill_color=ORANGE, fill_opacity=0.8).move_to(LEFT * 0.4 + UP * (0.0 - 0.25 * j)) for j in range(4)])
        mqa_kv_heads = VGroup(Circle(radius=0.08, color=GREEN, fill_color=GREEN, fill_opacity=0.8).move_to(RIGHT * 0.4 - UP * 0.38))
        mqa_lines = VGroup(*[Line(mqa_q_heads[j].get_right(), mqa_kv_heads[0].get_left(), color=GRAY_B, stroke_width=1.2) for j in range(4)])
        mqa_grp = VGroup(mqa_lbl, mqa_q_heads, mqa_kv_heads, mqa_lines)

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

        self.play(FadeIn(mha_grp, shift=UP*0.1), run_time=1.0)
        self.play(FadeIn(mqa_grp, shift=UP*0.1), run_time=1.0)
        self.play(FadeIn(gqa_grp, shift=UP*0.1), run_time=1.0)

        formula_lbl_new = create_markup_text(
            'Size = (batch * n<sub>ctx</sub>) * (2 * n<sub>layer</sub> * <span foreground="#33CCFF">n<sub>heads</sub> (reduced 4x - 8x)</span> * head<sub>dim</sub>) * n<sub>bytes</sub>',
            font_size=9.5
        ).move_to(formula_bg.get_center())
        self.play(FadeOut(formula_lbl), FadeIn(formula_lbl_new), run_time=0.6)
        formula_lbl = formula_lbl_new

        arch_note = create_markup_text(
            'MQA and GQA share <b>Key and Value</b> across many different query heads.\n'
            '<span foreground="#33CCFF">=> Greatly reduces the KV Cache produced for each long-context sequence.</span>',
            font_size=7.5, color=WHITE, line_spacing=1.25
        ).move_to(DOWN * 1.9)
        self.play(Write(arch_note), run_time=1.0)
        self.wait_until(cue_start[11])

        # =====================================================================
        # Cue 11-12 (sc43_011, sc43_012): Efficiency criteria & summary table
        # =====================================================================
        self.play(
            FadeOut(step7_title), FadeOut(formula_bg), FadeOut(formula_lbl),
            FadeOut(mha_grp), FadeOut(mqa_grp), FadeOut(gqa_grp), FadeOut(arch_note),
            run_time=0.8
        )

        step8_title = create_text("8. Summary: Meta-generator performance evaluation", font_size=13, color=YELLOW)
        step8_title.to_edge(UP, buff=0.4)
        self.play(Write(step8_title), run_time=1.0)

        header_box = RoundedRectangle(width=10.0, height=0.55, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.03).move_to(UP * 1.0)
        header_txt = create_markup_text("<b>Algorithm</b>  |  <b>Parallelizable (Parallelizable)</b>  |  <b>Prefix-shareable (Prefix-shareable)</b>", font_size=7.5, color=WHITE).move_to(header_box.get_center())
        header_grp = VGroup(header_box, header_txt)

        row1_box = RoundedRectangle(width=10.0, height=0.5, color=GRAY_E, fill_color="#111215", fill_opacity=0.8, corner_radius=0.02).move_to(UP * 0.45)
        row1_txt = create_markup_text("Chained (Chained)  |  ❌ No (Sequential)  |  ❌ No", font_size=7, color=WHITE).move_to(row1_box.get_center())

        row2_box = RoundedRectangle(width=10.0, height=0.5, color=GRAY_E, fill_color="#111215", fill_opacity=0.8, corner_radius=0.02).move_to(DOWN * 0.1)
        row2_txt = create_markup_text("Parallel (Song song)  |   Yes (maximum)  |   Yes (good)", font_size=7, color=WHITE).move_to(row2_box.get_center())

        row3_box = RoundedRectangle(width=10.0, height=0.5, color=GRAY_E, fill_color="#111215", fill_opacity=0.8, corner_radius=0.02).move_to(DOWN * 0.65)
        row3_txt = create_markup_text("Tree Search  |  ⚠️ semi-parallel  |   Yes (very high)", font_size=7, color=WHITE).move_to(row3_box.get_center())

        row4_box = RoundedRectangle(width=10.0, height=0.5, color=GRAY_E, fill_color="#111215", fill_opacity=0.8, corner_radius=0.02).move_to(DOWN * 1.2)
        row4_txt = create_markup_text("Refinement (Refinement)  |  ❌ No (Sequential)  |  ❌ No", font_size=7, color=WHITE).move_to(row4_box.get_center())

        table = VGroup(header_grp, row1_box, row1_txt, row2_box, row2_txt, row3_box, row3_txt, row4_box, row4_txt)
        self.play(FadeIn(table, shift=UP*0.1), run_time=1.2)

        quote_box = RoundedRectangle(width=10.0, height=0.65, color=YELLOW_D, fill_color="#201c14", fill_opacity=0.9, corner_radius=0.04).move_to(DOWN * 2.05)
        quote_lbl = create_markup_text(
            '<b>Message:</b> Token budget is only a simplification. Prompt structure\n'
            'and system optimization mechanisms determine most real inference performance.',
            font_size=7.5, color=YELLOW_A, line_spacing=1.2
        ).move_to(quote_box.get_center())
        quote_grp = VGroup(quote_box, quote_lbl)

        self.wait_until(cue_start[12])
        self.play(FadeIn(quote_grp, shift=UP * 0.15), run_time=1.0)
        self.wait_until(cue_start[13])

        # =====================================================================
        # Cue 13-14 (sc43_013, sc43_014): Prefix sharing naturally occurring examples
        # =====================================================================
        self.play(FadeOut(step8_title), FadeOut(table), FadeOut(quote_grp), run_time=0.8)

        self.play(Write(step1_title), run_time=1.0)
        self.play(FadeIn(prompt_boxes, shift=DOWN * 0.2), run_time=1.2)
        self.wait_until(cue_start[15])

        # =====================================================================
        # Cue 15 (sc43_015): Redundant VRAM storage waste
        # =====================================================================
        vram_bg = RoundedRectangle(width=11.2, height=1.6, color=GRAY_C, fill_color="#0e0f11", fill_opacity=0.95, corner_radius=0.06)
        vram_bg.move_to(DOWN * 1.5)
        vram_title = create_text("GPU VRAM memory", font_size=8, color=GRAY_B).next_to(vram_bg, UP, buff=0.05, aligned_edge=LEFT).shift(RIGHT * 0.2)
        
        vram_caches = VGroup()
        arrows = VGroup()
        for idx in range(3):
            cache_box = RoundedRectangle(width=3.0, height=0.8, color=RED, fill_color="#2b1414", fill_opacity=0.9, corner_radius=0.04)
            cache_box.move_to(LEFT * (3.5 * (1 - idx)) + DOWN * 1.5)
            
            cache_lbl = create_markup_text(
                f"<b>KV Cache Stream {idx+1}</b>\n<span foreground=\"#FF3333\">Contains a 1000-token system prompt</span>",
                font_size=6, color=WHITE, line_spacing=1.1
            ).move_to(cache_box.get_center())
            vram_caches.add(VGroup(cache_box, cache_lbl))
            
            arrow = Arrow(start=prompt_boxes[idx].get_bottom(), end=cache_box.get_top(), color=RED, stroke_width=2)
            arrows.add(arrow)

        wasted_label = create_markup_text(
            "<b>WARNING: Wasted VRAM! (Wasted Memory)</b>\n"
            "The system prompt is duplicated into 3 identical copies in cache.",
            font_size=8, color=RED, line_spacing=1.2
        ).move_to(DOWN * 2.6)

        self.play(
            FadeIn(vram_bg), FadeIn(vram_title),
            run_time=1.0
        )
        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2),
            LaggedStart(*[FadeIn(c, shift=DOWN*0.1) for c in vram_caches], lag_ratio=0.2),
            run_time=1.2
        )
        self.play(Write(wasted_label), run_time=1.0)
        self.wait_until(cue_start[16])

        # =====================================================================
        # Cue 16-18 (sc43_016, sc43_017, sc43_018): PagedAttention vs RadixAttention vs Hydragen recap
        # =====================================================================
        self.play(
            FadeOut(step1_title),
            FadeOut(prompt_boxes),
            FadeOut(vram_caches),
            FadeOut(arrows),
            FadeOut(wasted_label),
            FadeOut(vram_bg), FadeOut(vram_title),
            run_time=0.8
        )

        recap_title = create_text("Shared Prefix Optimizations Recap", font_size=14, color=YELLOW).move_to(UP * 2.0)
        recap_paged = create_markup_text("• <b>PagedAttention:</b> Page-level sharing (vLLM)", font_size=10, color=WHITE)
        recap_radix = create_markup_text("• <b>RadixAttention:</b> Multi-level prefix tree (SGLang)", font_size=10, color=WHITE)
        recap_hydra = create_markup_text("• <b>Hydragen:</b> Tensor Cores speedup (Matrix-Matrix)", font_size=10, color=WHITE)
        recap_list = VGroup(recap_paged, recap_radix, recap_hydra).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.2)

        self.play(FadeIn(recap_title), FadeIn(recap_paged, shift=RIGHT*0.2), run_time=1.0)
        self.wait_until(cue_start[17])
        self.play(FadeIn(recap_radix, shift=RIGHT*0.2), run_time=1.0)
        self.wait_until(cue_start[18])
        self.play(FadeIn(recap_hydra, shift=RIGHT*0.2), run_time=1.0)
        self.wait_until(cue_start[19])

        # =====================================================================
        # Cue 19 (sc43_019): Message: prompt structure determines optimization
        # =====================================================================
        recap_msg = create_markup_text(
            "<b>Message:</b> Prompt and meta-generator structure create system optimization opportunities.",
            font_size=9, color=YELLOW_A
        ).move_to(DOWN * 1.8)
        self.play(FadeIn(recap_msg, shift=UP*0.2), run_time=1.2)
        self.wait_until(cue_start[20])

        # =====================================================================
        # Cue 20-22 (sc43_020, sc43_021, sc43_022): KV cache compression formula connections
        # =====================================================================
        self.play(
            FadeOut(recap_title),
            FadeOut(recap_list),
            FadeOut(recap_msg),
            run_time=0.8
        )

        formula_recap_title = create_text("KV Cache Compression Bottleneck", font_size=14, color=YELLOW).move_to(UP * 2.0)
        formula_bg_recap = RoundedRectangle(width=9.5, height=1.5, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04).move_to(ORIGIN)
        formula_lbl_recap = create_markup_text(
            'Size = (batch * <span foreground="#FF3333">n<sub>ctx</sub></span>) * (2 * n<sub>layer</sub> * <span foreground="#33CCFF">n<sub>heads</sub></span> * head<sub>dim</sub>) * <span foreground="#33FF55">n<sub>bytes</sub></span>',
            font_size=10
        ).move_to(formula_bg_recap.get_center())
        
        desc_recap = VGroup(
            create_markup_text("• <span color='#FF3333'>n<sub>ctx</sub></span>: Reduced by <b>Token Dropping</b>", font_size=9.5),
            create_markup_text("• <span color='#33FF55'>n<sub>bytes</sub></span>: Reduced by <b>Quantization</b> (FP16 -> INT8/INT4)", font_size=9.5),
            create_markup_text("• <span color='#33CCFF'>n<sub>heads</sub></span>: Reduced by <b>Architectural Modification</b> (MQA/GQA)", font_size=9.5)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 2.0)

        self.play(
            FadeIn(formula_recap_title),
            FadeIn(formula_bg_recap),
            FadeIn(formula_lbl_recap),
            run_time=1.2
        )
        self.wait_until(cue_start[21])
        self.play(
            LaggedStart(*[FadeIn(d, shift=RIGHT*0.2) for d in desc_recap], lag_ratio=0.4),
            run_time=1.8
        )
        self.wait_until(cue_start[23])

        # =====================================================================
        # Cue 23 (sc43_023): Tutorial parts recap
        # =====================================================================
        self.play(
            FadeOut(formula_recap_title),
            FadeOut(formula_bg_recap),
            FadeOut(formula_lbl_recap),
            FadeOut(desc_recap),
            run_time=0.8
        )

        summary_title = create_text("Tutorial Overview Summary", font_size=14, color=YELLOW).move_to(UP * 2.0)
        part1 = create_markup_text("1. <b>Primitive Generators:</b> One token at a time (e.g. Greedy, Nucleus)", font_size=9.5)
        part2 = create_markup_text("2. <b>Meta-Generators:</b> Calling generators (e.g. Chaining, Tree Search)", font_size=9.5)
        part3 = create_markup_text("3. <b>System Efficiency:</b> Optimizing hardware system (e.g. KV Cache optimizations)", font_size=9.5)
        parts_grp = VGroup(part1, part2, part3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)

        self.play(FadeIn(summary_title), run_time=1.0)
        self.play(
            LaggedStart(
                FadeIn(part1, shift=RIGHT*0.25),
                FadeIn(part2, shift=RIGHT*0.25),
                FadeIn(part3, shift=RIGHT*0.25),
                lag_ratio=0.4
            ),
            run_time=2.2
        )
        self.wait_until(cue_start[24])

        # =====================================================================
        # Cue 24-27 (sc43_024 to sc43_027): Strategies recap table
        # =====================================================================
        self.play(
            FadeOut(summary_title),
            FadeOut(parts_grp),
            run_time=0.8
        )

        self.play(Write(step8_title), run_time=1.0)
        self.play(FadeIn(table, shift=UP*0.1), run_time=1.2)

        self.wait_until(cue_start[27])
        self.play(FadeIn(quote_grp, shift=UP * 0.15), run_time=1.2)
        self.wait_until(cue_start[28])

        # =====================================================================
        # Cue 28 (sc43_028): Looking Ahead future directions list
        # =====================================================================
        self.play(
            FadeOut(step8_title),
            FadeOut(table),
            FadeOut(quote_grp),
            run_time=0.8
        )

        step9_title = create_text("9. Future directions (Looking Ahead)", font_size=13, color=YELLOW)
        step9_title.to_edge(UP, buff=0.4)
        self.play(Write(step9_title), run_time=1.0)

        bullets = VGroup(
            create_markup_text("• <b>Hybrid Systems (Hybrid Systems):</b> Combine parallelism and sequential refinement (for example: AlphaVerus).", font_size=7.5),
            create_markup_text("• <b>Learning to search (Learning to search):</b> LLMs explore, backtrack, and self-correct.", font_size=7.5),
            create_markup_text("• <b>Agent optimization:</b> Interact dynamically with external environments and receive multi-dimensional feedback.", font_size=7.5),
            create_markup_text("• <b>Compute allocation:</b> Adapt compute spending flexibly for hard/easy questions.", font_size=7.5)
        )
        bullets.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(UP * 0.1 + LEFT * 0.2)

        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT*0.2) for b in bullets], lag_ratio=0.4),
            run_time=2.0
        )
        self.wait_until(cue_start[29])

        # =====================================================================
        # Cue 29-32 (sc43_029 to sc43_032): Warning on generalization & survey links
        # =====================================================================
        science_warning_box = RoundedRectangle(width=9.5, height=0.75, color=RED, fill_color="#2b1414", fill_opacity=0.9, corner_radius=0.04).move_to(DOWN * 1.85)
        science_warning_lbl = create_markup_text(
            '<b>Science warning:</b> Many conclusions are based on a few tasks.\n'
            '<span color="#ff8888">Generalization depends on tasks, evaluator, generator, and budget.</span>',
            font_size=7.5, color=WHITE, line_spacing=1.2
        ).move_to(science_warning_box.get_center())
        science_warning_grp = VGroup(science_warning_box, science_warning_lbl)

        paper_box = RoundedRectangle(width=9.5, height=0.65, color=BLUE, fill_color="#14202b", fill_opacity=0.95, corner_radius=0.04).move_to(DOWN * 1.85)
        paper_lbl = create_markup_text(
            '<b>Research material:</b> Survey Paper (TMLR 2024) &amp; Code/Slides at the website:\n'
            '<span foreground="#33CCFF"><b>cmu-l3.github.io/neurips2024-inference-tutorial</b></span>',
            font_size=7.5, color=WHITE, line_spacing=1.2
        ).move_to(paper_box.get_center())
        paper_grp = VGroup(paper_box, paper_lbl)

        self.play(FadeIn(science_warning_grp, shift=UP*0.2), run_time=1.2)
        self.wait_until(cue_start[31])

        self.play(ReplacementTransform(science_warning_grp, paper_grp), run_time=1.2)
        self.wait_until(cue_start[32])

        thank_you = create_text("Thank you!", font_size=18, color=YELLOW).move_to(DOWN * 2.7)
        self.play(FadeIn(thank_you, shift=UP*0.1), run_time=1.0)
        self.wait_until(cue_start[32] + SCENE_4_3_DURATIONS["sc43_032.mp3"])

        self.play(
            FadeOut(step9_title),
            FadeOut(bullets),
            FadeOut(paper_grp),
            FadeOut(thank_you),
            run_time=1.0
        )
        self.wait(0.2)

        assert_all_scene_voiceovers_played(self)
