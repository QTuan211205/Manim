import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VOICEOVER_DIR = PROJECT_ROOT / "voiceover" / "generated_sentence_level"

SCENE_1_4_DURATIONS = {
    "sc14_001.mp3": 6.316,
    "sc14_002.mp3": 3.994,
    "sc14_003.mp3": 9.381,
    "sc14_004.mp3": 11.517,
    "sc14_005.mp3": 11.610,
    "sc14_006.mp3": 3.529,
    "sc14_007.mp3": 6.130,
    "sc14_008.mp3": 5.341,
}
SCENE_1_4_VOICEOVERS = tuple(SCENE_1_4_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc14_*.mp3"))
    expected = sorted(SCENE_1_4_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 1.4 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_1_4_DURATIONS:
        raise KeyError(f"Unexpected Scene 1.4 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 1.4 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    
    offsets = {
        "sc14_001.mp3": 0.0,
        "sc14_002.mp3": 6.316,
        "sc14_003.mp3": 12.7,
        "sc14_004.mp3": 24.0,
        "sc14_005.mp3": 38.0,
        "sc14_006.mp3": 51.8,
        "sc14_007.mp3": 55.329,
        "sc14_008.mp3": 61.459,
    }
    
    voiceover_end = 0.0
    for filename, duration in SCENE_1_4_DURATIONS.items():
        offset = offsets[filename]
        add_voiceover(scene, filename, offset, duration)
        voiceover_end = max(voiceover_end, offset + duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    if played != SCENE_1_4_VOICEOVERS:
        missing = [filename for filename in SCENE_1_4_VOICEOVERS if filename not in played]
        raise RuntimeError(
            f"Scene 1.4 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


def finish_voiceovers(scene, voiceover_end, padding=0.25):
    current_time = getattr(scene.renderer, "time", 0.0)
    remaining = voiceover_end + padding - current_time
    if remaining > 0:
        scene.wait(remaining)


# Note: visual/narration alignment comment translated from Vietnamese.
def create_text(text, font_size=24, font="Arial", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)

# Note: visual/narration alignment comment translated from Vietnamese.
def create_markup_text(text, font_size=24, font="Arial", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)


class Scene1_4(Scene):
    def construct(self):
        # =========================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =========================================================================

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.camera.background_color = "#111111"

        # Voiceover audio is scheduled from sentence-level MP3 durations.
        voiceover_end = schedule_scene_voiceovers(self)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        main_title = create_text("Conceptual Framework: Generator & Meta-Generator", font_size=20, color=BLUE_A)
        main_title.to_edge(UP, buff=0.4)
        self.play(Write(main_title))
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        diag_center = DOWN * 0.4

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        gen_box = RoundedRectangle(width=2.8, height=1.1, color=BLUE_C, fill_color="#0e1b29", fill_opacity=0.9, corner_radius=0.08)
        gen_box.move_to(diag_center + UP * 0.9)
        gen_title = create_text("Generator", font_size=10, color=WHITE)
        gen_sub = create_text("Generator (g)", font_size=8.5, color=BLUE_A)
        gen_sub.next_to(gen_title, DOWN, buff=0.06)
        gen_text = VGroup(gen_title, gen_sub)
        gen_text.move_to(gen_box.get_center())
        gen_group = VGroup(gen_box, gen_text)

        # Note: visual/narration alignment comment translated from Vietnamese.
        in_box = RoundedRectangle(width=1.5, height=0.7, color=GRAY_A, fill_color="#1e1e1e", fill_opacity=0.9, corner_radius=0.06)
        in_box.move_to(diag_center + LEFT * 2.6 + UP * 0.9)
        in_text = create_text("Input (x)", font_size=10, color=WHITE)
        in_text.move_to(in_box.get_center())
        in_group = VGroup(in_box, in_text)

        # Note: visual/narration alignment comment translated from Vietnamese.
        out_temp_box = RoundedRectangle(width=1.5, height=0.7, color=GRAY_A, fill_color="#1e1e1e", fill_opacity=0.9, corner_radius=0.06)
        out_temp_box.move_to(diag_center + RIGHT * 2.6 + UP * 0.9)
        out_temp_text = create_text("Output (y)", font_size=10, color=WHITE)
        out_temp_text.move_to(out_temp_box.get_center())
        out_temp_group = VGroup(out_temp_box, out_temp_text)

        # Note: visual/narration alignment comment translated from Vietnamese.
        arrow_in = Line(
            in_box.get_right(), gen_box.get_left(), 
            color=GRAY_A, stroke_width=1.8, buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)

        # Note: visual/narration alignment comment translated from Vietnamese.
        arrow_out_temp = Line(
            gen_box.get_right(), out_temp_box.get_left(),
            color=GRAY_A, stroke_width=1.8, buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeIn(in_group, shift=RIGHT * 0.2),
            FadeIn(gen_group, shift=RIGHT * 0.2),
            Create(arrow_in),
            run_time=1.0
        )
        self.play(
            Create(arrow_out_temp),
            FadeIn(out_temp_group, shift=RIGHT * 0.2),
            run_time=1.0
        )
        self.wait(19.0)


        # Keep the centered generator diagram until the meta-generator beat.


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        eval_box = RoundedRectangle(width=2.8, height=1.1, color=GREEN_C, fill_color="#0d2417", fill_opacity=0.9, corner_radius=0.08)
        eval_box.move_to(diag_center + DOWN * 1.3)
        eval_title = create_text("Evaluator", font_size=10, color=WHITE)
        eval_sub = create_text("Evaluator (v)", font_size=8.5, color=GREEN_A)
        eval_sub.next_to(eval_title, DOWN, buff=0.06)
        eval_text = VGroup(eval_title, eval_sub)
        eval_text.move_to(eval_box.get_center())
        eval_group = VGroup(eval_box, eval_text)

        # Note: visual/narration alignment comment translated from Vietnamese.
        out_box = RoundedRectangle(width=1.5, height=0.7, color=GRAY_A, fill_color="#1e1e1e", fill_opacity=0.9, corner_radius=0.06)
        out_box.move_to(diag_center + LEFT * 2.6 + DOWN * 1.3)
        out_text = create_text("Output (y)", font_size=10, color=WHITE)
        out_text.move_to(out_box.get_center())
        out_group = VGroup(out_box, out_text)

        # Note: visual/narration alignment comment translated from Vietnamese.
        arrow_down = Line(
            gen_box.get_bottom(), eval_box.get_top(), 
            color=GRAY_A, stroke_width=1.8, buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)
        arrow_down_label = create_text("Generated sample (y)", font_size=8, color=GRAY_A)
        arrow_down_label.next_to(arrow_down, RIGHT, buff=0.1)

        # Note: visual/narration alignment comment translated from Vietnamese.
        arrow_loop = CurvedArrow(
            eval_box.get_right() + RIGHT * 0.1, gen_box.get_right() + RIGHT * 0.1, 
            angle=PI/2.5, color=YELLOW_B, stroke_width=1.8
        )
        loop_line1 = create_text("Feedback /", font_size=8, color=YELLOW_B)
        loop_line2 = create_text("Retry", font_size=8, color=YELLOW_B)
        loop_label = VGroup(loop_line1, loop_line2).arrange(DOWN, buff=0.05)
        # Note: visual/narration alignment comment translated from Vietnamese.
        loop_label.next_to(arrow_loop, RIGHT, buff=0.15)

        # Note: visual/narration alignment comment translated from Vietnamese.
        arrow_out_new = Line(
            eval_box.get_left(), out_box.get_right(),
            color=GRAY_A, stroke_width=1.8, buff=0.1
        ).add_tip(tip_length=0.12, tip_width=0.12)

        # Note: visual/narration alignment comment translated from Vietnamese.
        meta_box = RoundedRectangle(width=7.4, height=4.2, color=YELLOW_C, fill_color="#1c1b0c", fill_opacity=0.4, corner_radius=0.12)
        meta_box.move_to(DOWN * 0.6)
        meta_box_title = create_text("Orchestrator (Meta-Generator) G", font_size=11, color=YELLOW_B)
        meta_box_title.next_to(meta_box.get_top(), DOWN, buff=0.15)
        meta_group = VGroup(meta_box, meta_box_title)

        # Note: visual/narration alignment comment translated from Vietnamese.
        eq_box_G = RoundedRectangle(width=5.2, height=2.0, color=YELLOW_E, fill_color="#1c1b0c", fill_opacity=0.6, corner_radius=0.08)
        eq_box_G.move_to(UP * 1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(arrow_out_temp),
            FadeOut(out_temp_group, shift=LEFT * 0.2),
            run_time=0.6
        )
        self.play(
            FadeIn(eval_group, shift=UP * 0.2),
            Create(arrow_down),
            Write(arrow_down_label),
            run_time=0.8
        )
        self.play(
            Create(arrow_loop),
            Write(loop_label),
            run_time=0.6
        )
        self.play(
            Create(meta_box),
            Write(meta_box_title),
            run_time=0.8
        )
        self.play(
            Create(arrow_out_new),
            FadeIn(out_group, shift=LEFT * 0.2),
            run_time=0.6
        )
        self.wait(0.9)

        diagram_scene = VGroup(
            in_group, gen_group, eval_group, out_group, meta_group,
            arrow_in, arrow_down, arrow_down_label, arrow_loop, loop_label, arrow_out_new,
        )
        self.play(FadeOut(diagram_scene, shift=LEFT * 0.2), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        meta_eq_title = create_text("Mathematical Definition", font_size=12, color=GRAY_A)
        meta_eq_title.move_to(UP * 1.85)

        y_part_G = create_markup_text("<span color='#ffff00'><i>y</i></span>", font_size=18)
        sim_part_G = create_text(" ~ ", font_size=18, color=GRAY_A)
        G_part_G = create_markup_text("<span color='#ebcb8b'><i>G</i></span>", font_size=18)
        lparen_part_G = create_text("(", font_size=18, color=WHITE)
        y2_part_G = create_markup_text("<span color='#ffff00'><i>y</i></span>", font_size=18)
        pipe_part_G = create_text(" | ", font_size=18, color=WHITE)
        x_part_G = create_markup_text("<span color='#ffffff'><i>x</i></span>", font_size=18)
        semi_part_G = create_text("; ", font_size=18, color=WHITE)
        g_list_part = create_markup_text("<span color='#88c0d0'><i>g</i><sub>1</sub>, <i>g</i><sub>2</sub>, ..., <i>g</i><sub><i>G</i></sub></span>", font_size=18)
        comma_part_G = create_text(", ", font_size=18, color=WHITE)
        phi_part_G = create_markup_text("<span color='#d08770'><i>φ</i></span>", font_size=18)
        rparen_part_G = create_text(")", font_size=18, color=WHITE)

        meta_eq = VGroup(
            y_part_G, sim_part_G, G_part_G, lparen_part_G, y2_part_G, pipe_part_G, x_part_G, semi_part_G, g_list_part, comma_part_G, phi_part_G, rparen_part_G
        )
        meta_eq.arrange(RIGHT, buff=0.04)
        meta_eq.move_to(UP * 1.1)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeIn(eq_box_G),
            Write(meta_eq_title),
            Write(meta_eq),
            run_time=1.0
        )
        self.wait(1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        brace_G_lbl = Brace(G_part_G, direction=DOWN, color=YELLOW_A, buff=0.1)
        lbl_G_desc = create_text("High-level orchestration strategy\n(Chain, Parallel, Tree...)", font_size=8, color=YELLOW_A)
        lbl_G_desc.next_to(brace_G_lbl, DOWN, buff=0.05)

        self.play(Create(brace_G_lbl), Write(lbl_G_desc), run_time=0.6)
        self.wait(0.9)

        # Note: visual/narration alignment comment translated from Vietnamese.
        brace_gi = Brace(g_list_part, direction=DOWN, color=BLUE_A, buff=0.1)
        lbl_gi_desc = create_text("Primitive generators\n(treated as black boxes)", font_size=8, color=BLUE_A)
        lbl_gi_desc.next_to(brace_gi, DOWN, buff=0.05)

        self.play(
            FadeOut(brace_G_lbl), FadeOut(lbl_G_desc),
            Create(brace_gi), Write(lbl_gi_desc),
            run_time=0.6
        )
        self.wait(0.9)

        # Note: visual/narration alignment comment translated from Vietnamese.
        brace_phi_G = Brace(phi_part_G, direction=DOWN, color=ORANGE, buff=0.1)
        lbl_phi_G_desc = create_text("Evaluator (reward model),\nexternal tools, sample count...", font_size=8, color=ORANGE)
        lbl_phi_G_desc.next_to(brace_phi_G, DOWN, buff=0.05)

        self.play(
            FadeOut(brace_gi), FadeOut(lbl_gi_desc),
            Create(brace_phi_G), Write(lbl_phi_G_desc),
            run_time=0.6
        )
        self.wait(0.9)
        self.play(FadeOut(brace_phi_G), FadeOut(lbl_phi_G_desc), run_time=0.4)

        # Note: visual/narration alignment comment translated from Vietnamese.
        eg_bg_G = RoundedRectangle(width=5.2, height=2.0, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.8, corner_radius=0.08)
        eg_bg_G.move_to(DOWN * 1.45)

        eg_title_G = create_text("Meta-Generator G strategies:", font_size=9, color=YELLOW_A)
        eg_item1_G = create_text("• Reasoning chains (Chaining - CoT, Self-Ask)", font_size=8, color=WHITE)
        eg_item2_G = create_text("• Parallel sampling & filtering (Best-of-N, Voting)", font_size=8, color=WHITE)
        eg_item3_G = create_text("• Tree traversal & backtracking (ToT, MCTS)", font_size=8, color=WHITE)
        eg_item4_G = create_text("• Refinement & self-correction (Self-Correction)", font_size=8, color=WHITE)

        eg_items_group_G = VGroup(eg_title_G, eg_item1_G, eg_item2_G, eg_item3_G, eg_item4_G).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        eg_items_group_G.move_to(eg_bg_G.get_center() + LEFT * 0.2)
        eg_group_G = VGroup(eg_bg_G, eg_items_group_G)

        self.play(
            FadeIn(eg_group_G, shift=UP * 0.15),
            run_time=1.0
        )
        self.wait(1.2)

        # Note: visual/narration alignment comment translated from Vietnamese.
        all_stage1_2 = VGroup(
            meta_eq_title, meta_eq, eg_group_G, eq_box_G
        )
        self.play(FadeOut(all_stage1_2, shift=DOWN * 0.2), run_time=0.8) # Ends at 42.0s
        self.wait(0.5) # Starts sc14_005 at 42.5s


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        outline_title = create_markup_text("DETAILED COURSE OUTLINE", font_size=20, color=BLUE_A)
        outline_title.move_to(UP * 2.5)
        
        outline_underline = Line(
            outline_title.get_left() + DOWN * 0.15,
            outline_title.get_right() + DOWN * 0.15,
            color=BLUE_C, stroke_width=1.8
        )

        self.play(
            Write(outline_title),
            Create(outline_underline),
            run_time=1.0
        ) # Ends at 44.0s
        self.wait(0.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        outline_y_positions = [1.2, 0.3, -0.6, -1.5, -2.4]
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        items_data = [
            {
                "part": "Chapter I",
                "title": "The Era of Inference-Time Compute Scaling (Inference Scaling Laws)",
                "speaker": "Overview & Role of Test-Time Compute | Speaker: Sean Welleck (CMU)",
                "color": BLUE_B
            },
            {
                "part": "Chapter II",
                "title": "Token-Level Primitive Generators",
                "speaker": "Greedy, Beam Search, Temperature, Truncation & Constraints | Speaker: Matthew Finlayson (USC)",
                "color": GREEN_A
            },
            {
                "part": "Chapter III",
                "title": "Sequence-Level High-Level Orchestrators (Meta-Generators)",
                "speaker": "Chaining, Parallel (Voting, MBR), Tree Search & Self-Correction | Speaker: Sean Welleck (CMU)",
                "color": YELLOW_A
            },
            {
                "part": "Chapter IV",
                "title": "Hardware Systems Efficiency",
                "speaker": "Memory-bound vs Compute-bound, KV Cache & Speculative Decoding | Speaker: Hailey Schoelkopf",
                "color": ORANGE
            },
            {
                "part": "Panel",
                "title": "Panel discussion with leading experts",
                "speaker": "Future directions for test-time compute | Moderator: Ilia Kulikov (Meta AI)",
                "color": RED_A
            }
        ]

        outline_group = VGroup()
        chapter_mobjects = []

        for idx, data in enumerate(items_data):
            y_pos = outline_y_positions[idx]
            
            # Note: visual/narration alignment comment translated from Vietnamese.
            item_header = create_markup_text(
                f"<b>{data['part']}:</b> {data['title']}", 
                font_size=9.5, 
                color=data['color']
            )
            item_header.move_to(LEFT * 5.0 + UP * y_pos, aligned_edge=LEFT)
            
            # Note: visual/narration alignment comment translated from Vietnamese.
            item_speaker = create_text(
                data['speaker'], 
                font_size=8.0, 
                color=GRAY_A
            )
            item_speaker.next_to(item_header, DOWN, buff=0.06, aligned_edge=LEFT)
            
            item_group = VGroup(item_header, item_speaker)
            chapter_mobjects.append(item_group)
            outline_group.add(item_group)

            self.play(FadeIn(item_group, shift=LEFT * 0.2), run_time=0.5)
            if idx < 4:
                self.wait(1.3)
            else:
                self.wait(2.41) # Total outline loop takes exactly 10.11s, ending at 54.11s (end of sc14_005)

        self.wait(0.49) # Scene time: 54.6s (starts sc14_006)

        # Highlight Chapter II to discuss "Primitive Generators" during sc14_006 - sc14_008
        self.play(
            chapter_mobjects[0].animate.set_opacity(0.35),
            chapter_mobjects[2].animate.set_opacity(0.35),
            chapter_mobjects[3].animate.set_opacity(0.35),
            chapter_mobjects[4].animate.set_opacity(0.35),
            run_time=0.8
        )
        self.wait(13.7) # Keep the final outline beat close to the last voiceover.

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            *[item.animate.set_opacity(1.0) for item in chapter_mobjects],
            run_time=1.0
        )
        self.wait(0.2)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(outline_title),
            FadeOut(outline_underline),
            FadeOut(outline_group, shift=UP * 0.2),
            run_time=1.2
        )
        self.wait(0.05)
        finish_voiceovers(self, voiceover_end)
        assert_all_scene_voiceovers_played(self)
