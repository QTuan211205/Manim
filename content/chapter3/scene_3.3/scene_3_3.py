import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_3_3_DURATIONS = {
    "sc33_001.mp3": 5.572789,
    "sc33_002.mp3": 11.238458,
    "sc33_003.mp3": 12.027937,
    "sc33_004.mp3": 5.665669,
    "sc33_005.mp3": 4.318912,
    "sc33_006.mp3": 5.944308,
    "sc33_007.mp3": 4.133152,
    "sc33_008.mp3": 6.269388,
    "sc33_009.mp3": 7.337506,
    "sc33_010.mp3": 4.922630,
    "sc33_011.mp3": 5.758549,
    "sc33_012.mp3": 2.647075,
    "sc33_013.mp3": 6.269388,
    "sc33_014.mp3": 2.043356,
    "sc33_015.mp3": 11.424218,
}
SCENE_3_3_VOICEOVERS = tuple(SCENE_3_3_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc33_*.mp3"))
    expected = sorted(SCENE_3_3_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 3.3 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_3_3_DURATIONS:
        raise KeyError(f"Unexpected Scene 3.3 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 3.3 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_3_3_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_3_3_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 3.3 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
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


def get_checkmark(color=GREEN, stroke_width=2.5):
    checkmark = VMobject(color=color, stroke_width=stroke_width)
    checkmark.set_points_as_corners([
        LEFT * 0.12 + DOWN * 0.05,
        ORIGIN + DOWN * 0.15,
        RIGHT * 0.2 + UP * 0.15
    ])
    return checkmark


def get_crossmark(color=RED, stroke_width=2.5):
    cross = VGroup()
    line1 = Line(LEFT * 0.12 + UP * 0.12, RIGHT * 0.12 + DOWN * 0.12, color=color, stroke_width=stroke_width)
    line2 = Line(LEFT * 0.12 + DOWN * 0.12, RIGHT * 0.12 + UP * 0.12, color=color, stroke_width=stroke_width)
    cross.add(line1, line2)
    return cross


class Scene3_3(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def replace_content(self, old_group, new_group, run_time=0.55):
        if old_group is None:
            self.play(FadeIn(new_group, shift=UP * 0.12), run_time=run_time)
        else:
            self.play(FadeOut(old_group, shift=DOWN * 0.08), FadeIn(new_group, shift=UP * 0.08), run_time=run_time)
        return new_group

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (filename, duration) in enumerate(SCENE_3_3_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        # --- Chapter Title (Cue 1) ---
        chapter_title = create_text("Chapter 3: High-Level Orchestrators", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 3.3: Tree Search & Backtracking Mechanisms", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub).move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)
        self.wait(2.5)

        sub_title = create_text("Tree search & Backtracking", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=1.0)
        
        content = None

        # --- Cue 2: Basic Tree Search elements ---
        self.wait_until(cue_start[2] + 0.25)
        part1_title = create_text("1. Waste in Parallel Decoding & the Tree Search Mechanism", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)
        
        design_title = create_text("4 basic Tree Search design elements:", font_size=14, color=YELLOW).move_to(UP * 1.5)
        design_items = VGroup(
            create_markup_text("• <b>States <i>s</i>:</b> Generated reasoning prefix.", font_size=12),
            create_markup_text("• <b>Transitions <i>s -> s'</i>:</b> Explore the next step.", font_size=12),
            create_markup_text("• <b>Scores <i>v(s)</i>:</b> Estimate the potential of the current step.", font_size=12),
            create_markup_text("• <b>Traversal strategy:</b> Depth-first search (DFS), breadth-first search (BFS), ...", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.4)
        
        part1_group = VGroup(part1_title, design_title, design_items)
        self.play(FadeIn(part1_title), Write(design_title), run_time=1.0)
        for item in design_items:
            self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=0.6)
            self.wait(1.4)
            
        content = part1_group

        # --- Cue 3: Process-based Reward Model ---
        self.wait_until(cue_start[3] + 0.25)
        self.play(FadeOut(content), run_time=0.4)
        
        part2_title = create_text("2. Process-based Reward Model (PRM)", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)
        
        box_width, box_height = 3.6, 2.0
        
        orm_box = RoundedRectangle(width=box_width, height=box_height, color=BLUE_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        orm_box.move_to(LEFT * 3.6 + DOWN * 0.6)
        orm_lbl = create_text("Outcome-based RM\n(ORM)", font_size=13, color=BLUE_A).move_to(orm_box.get_center() + UP * 0.5)
        orm_desc = create_text("Score the complete answer y\nv(y) belongs to [0, 1] at the end", font_size=10, color=GRAY_B).move_to(orm_box.get_center() + DOWN * 0.4)
        orm_group = VGroup(orm_box, orm_lbl, orm_desc)

        orm_input = create_text("Chained y", font_size=11, color=WHITE).next_to(orm_box, LEFT, buff=0.6)
        orm_in_arrow = Arrow(start=orm_input.get_right(), end=orm_box.get_left(), color=BLUE_B, stroke_width=1.5, buff=0.08)
        orm_output = create_text("Score: 0.88", font_size=11, color=GREEN).next_to(orm_box, RIGHT, buff=0.6)
        orm_out_arrow = Arrow(start=orm_box.get_right(), end=orm_output.get_left(), color=GREEN, stroke_width=1.5, buff=0.08)
        orm_full = VGroup(orm_group, orm_input, orm_in_arrow, orm_output, orm_out_arrow)

        prm_box = RoundedRectangle(width=box_width, height=box_height, color=GOLD_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        prm_box.move_to(RIGHT * 3.6 + DOWN * 0.6)
        prm_lbl = create_text("Process-based RM\n(PRM)", font_size=13, color=GOLD_A).move_to(prm_box.get_center() + UP * 0.5)
        prm_desc = create_text("Score each reasoning step s(t)\nv(x, s1, ..., st) belongs to [0, 1]", font_size=10, color=GRAY_B).move_to(prm_box.get_center() + DOWN * 0.4)
        prm_group = VGroup(prm_box, prm_lbl, prm_desc)

        prm_input = create_text("Step s(t)", font_size=11, color=WHITE).next_to(prm_box, LEFT, buff=0.6)
        prm_in_arrow = Arrow(start=prm_input.get_right(), end=prm_box.get_left(), color=GOLD_B, stroke_width=1.5, buff=0.08)
        prm_output = create_text("Score: 0.95", font_size=11, color=GREEN).next_to(prm_box, RIGHT, buff=0.6)
        prm_out_arrow = Arrow(start=prm_box.get_right(), end=prm_output.get_left(), color=GREEN, stroke_width=1.5, buff=0.08)
        prm_full = VGroup(prm_group, prm_input, prm_in_arrow, prm_output, prm_out_arrow)

        prm_formula_box = RoundedRectangle(width=5.8, height=0.8, color=GOLD, fill_color="#16171a", fill_opacity=0.9, corner_radius=0.08)
        prm_formula_box.move_to(UP * 1.8)
        prm_formula_txt = create_markup_text(
            "Formula PRM:  <span color='#FFD700'><i>v</i>(<i>x</i>, <i>s</i><sub>1</sub>, <i>s</i><sub>2</sub>, ..., <i>s</i><sub><i>t</i></sub>) → [0, 1]</span>",
            font_size=13
        ).move_to(prm_formula_box.get_center())
        prm_formula_group = VGroup(prm_formula_box, prm_formula_txt)

        self.play(FadeIn(part2_title), FadeIn(orm_full), run_time=1.0)
        self.wait(2.5)
        self.play(FadeIn(prm_full), FadeIn(prm_formula_group), run_time=1.2)
        
        content = VGroup(part2_title, orm_full, prm_full, prm_formula_group)

        # --- Cue 4: Rebase Algorithm ---
        self.wait_until(cue_start[4] + 0.25)
        self.play(FadeOut(content), run_time=0.4)
        
        part3_title = create_text("3. Rebase Algorithm (Reward Balanced Search)", font_size=13, color=BLUE_A)
        part3_title.next_to(sub_title, DOWN, buff=0.3)
        
        rebase_formula_box = RoundedRectangle(width=8.0, height=1.1, color=BLUE_B, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        rebase_formula_box.move_to(UP * 1.3)
        rebase_txt = create_markup_text(
            "Formula Rebase:  <span color='#87CEFA'>explore<sub><i>i</i></sub> = Round( Budget × </span>"
            "<span color='#00FF7F'>e<sup><i>v</i>(<i>s</i><sub><i>i</i></sub>)/τ</sup></span> / "
            "<span color='#FFD700'>∑<sub><i>j</i></sub> e<sup><i>v</i>(<i>s</i><sub><i>j</i></sub>)/τ</sup></span><span color='#87CEFA'> )</span>",
            font_size=13
        ).move_to(rebase_formula_box.get_center())
        rebase_formula_group = VGroup(rebase_formula_box, rebase_txt)
        
        self.play(FadeIn(part3_title), FadeIn(rebase_formula_group), run_time=1.0)
        content = VGroup(part3_title, rebase_formula_group)

        # --- Cue 5: Rebase annotations ---
        self.wait_until(cue_start[5] + 0.25)
        
        annotations = VGroup(
            create_markup_text("<span color='#87CEFA'>• <b>explore<sub><i>i</i></sub>:</b></span> Number of compute streams allocated to branch <i>s<sub>i</sub></i>.", font_size=11),
            create_markup_text("<span color='#FFFFFF'>• <b>Budget:</b></span> Total compute-stream budget at inference time.", font_size=11),
            create_markup_text("<span color='#00FF7F'>• <b><i>v</i>(<i>s</i><sub><i>i</i></sub>):</b></span> PRM score reflecting how promising state <i>s<sub>i</sub></i>.", font_size=11),
            create_markup_text("<span color='#FFA500'>• <b>τ (Temperature):</b></span> Control parameter: small τ -> focused; large τ -> diverse.", font_size=11)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 0.8)
        
        self.play(FadeIn(annotations, shift=UP * 0.15), run_time=1.0)
        rebase_full_group = VGroup(content, annotations)

        # --- Cue 6: Rebase Node Allocation Example ---
        self.wait_until(cue_start[6] + 0.2)
        self.play(FadeOut(annotations), run_time=0.4)
        
        sim_title = create_text("Example: Budget = 10 streams | Temperature τ = 0.3", font_size=12, color=YELLOW).move_to(UP * 0.2)
        
        node_a = RoundedRectangle(width=2.5, height=0.7, color=GREEN, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        node_a.move_to(LEFT * 3.8 + DOWN * 0.8)
        lbl_a = create_text("Branch sA (PRM: 0.90)", font_size=10, color=GREEN).move_to(node_a.get_center())
        node_a_group = VGroup(node_a, lbl_a)

        node_b = RoundedRectangle(width=2.5, height=0.7, color=RED, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        node_b.move_to(RIGHT * 3.8 + DOWN * 0.8)
        lbl_b = create_text("Branch sB (PRM: 0.30)", font_size=10, color=RED).move_to(node_b.get_center())
        node_b_group = VGroup(node_b, lbl_b)

        self.play(Write(sim_title), FadeIn(node_a_group), FadeIn(node_b_group), run_time=1.0)
        
        alloc_a = create_markup_text("Allocation: <span color='#00FF00'><b>9 streams</b></span> (90% compute)", font_size=11)
        alloc_a.next_to(node_a, DOWN, buff=0.25)

        alloc_b = create_markup_text("Allocation: <span color='#FF0000'><b>1 stream</b></span> (10% compute)", font_size=11)
        alloc_b.next_to(node_b, DOWN, buff=0.25)
        
        self.play(FadeIn(alloc_a, shift=UP * 0.1), FadeIn(alloc_b, shift=UP * 0.1), run_time=0.8)

        arrows_a = VGroup()
        arrows_b = VGroup()
        for idx in range(9):
            angle = (-30 + idx * 7.5) * DEGREES
            arr = Arrow(
                start=node_a.get_right(),
                end=node_a.get_right() + RIGHT * 1.5 + UP * np.sin(angle) * 0.8,
                color=GREEN, stroke_width=1.0, buff=0.05
            )
            arrows_a.add(arr)

        arr_b = Arrow(
            start=node_b.get_right(),
            end=node_b.get_right() + RIGHT * 1.5,
            color=RED, stroke_width=1.0, buff=0.05
        )
        arrows_b.add(arr_b)
        
        self.play(Create(arrows_a), Create(arrows_b), run_time=1.2)
        
        # Keep group
        rebase_example_group = VGroup(sim_title, node_a_group, node_b_group, alloc_a, alloc_b, arrows_a, arrows_b)
        content = VGroup(rebase_full_group, rebase_example_group)

        # --- Cue 7: Traversal & Applications ---
        self.wait_until(cue_start[7] + 0.25)
        self.play(FadeOut(content), run_time=0.4)
        
        part4_title = create_text("4. Tree Traversal Algorithms & Real Applications", font_size=13, color=BLUE_A)
        part4_title.next_to(sub_title, DOWN, buff=0.3)
        
        center_box = RoundedRectangle(width=3.2, height=0.8, color=YELLOW, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        center_box.move_to(ORIGIN)
        center_lbl = create_text("Tree Search", font_size=13, color=YELLOW).move_to(center_box.get_center())
        center_group = VGroup(center_box, center_lbl)

        left_box = RoundedRectangle(width=3.4, height=1.6, color=BLUE_B, fill_color="#141517", fill_opacity=0.8, corner_radius=0.06)
        left_box.move_to(LEFT * 3.8)
        left_lbl = create_text("Common algorithms", font_size=11, color=BLUE_A).move_to(left_box.get_center() + UP * 0.5)
        left_desc = create_markup_text(
            "• DFS (Depth-first)\n• BFS (Breadth-first)\n• Tree of Thoughts (ToT)\n• Monte Carlo Tree Search (MCTS)",
            font_size=9, line_spacing=1.2
        ).move_to(left_box.get_center() + DOWN * 0.25)
        arrow_left = Arrow(start=center_box.get_left(), end=left_box.get_right(), color=BLUE_B, stroke_width=1.5, buff=0.05)
        left_group = VGroup(left_box, left_lbl, left_desc, arrow_left)

        right_box = RoundedRectangle(width=3.4, height=1.6, color=GREEN_B, fill_color="#141517", fill_opacity=0.8, corner_radius=0.06)
        right_box.move_to(RIGHT * 3.8)
        right_lbl = create_text("Application domains", font_size=11, color=GREEN_A).move_to(right_box.get_center() + UP * 0.5)
        right_desc = create_markup_text(
            "• Go playing (AlphaGo)\n• Math proving (AlphaProof)\n• Programming code generation\n• AI Agents (Web / Tool)",
            font_size=9, line_spacing=1.2
        ).move_to(right_box.get_center() + DOWN * 0.25)
        arrow_right = Arrow(start=center_box.get_right(), end=right_box.get_left(), color=GREEN_B, stroke_width=1.5, buff=0.05)
        right_group = VGroup(right_box, right_lbl, right_desc, arrow_right)
        
        app_group = VGroup(part4_title, center_group, left_group, right_group)
        self.play(FadeIn(part4_title), FadeIn(center_group), run_time=0.8)
        self.play(FadeIn(left_group), FadeIn(right_group), run_time=1.0)
        content = app_group

        # --- Cue 8 & 9: Search & Backtracking Tree Animation ---
        self.wait_until(cue_start[8] + 0.25)
        self.play(FadeOut(content), run_time=0.4)
        
        part5_title = create_text("5. Search & Backtracking Animation", font_size=13, color=BLUE_A)
        part5_title.next_to(sub_title, DOWN, buff=0.3)
        
        tree_intro = create_markup_text(
            "PRM scores each reasoning step: low-scoring steps are removed,\n"
            "and the algorithm performs <b>Backtracking</b> to follow a better branch.",
            font_size=13, color=WHITE, line_spacing=1.3
        ).move_to(UP * 1.8)
        
        self.play(FadeIn(part5_title), Write(tree_intro), run_time=1.0)

        root_pos = UP * 0.4 + ORIGIN
        s1_pos = LEFT * 2.5 + DOWN * 0.6
        s2_pos = RIGHT * 2.5 + DOWN * 0.6
        s3_pos = LEFT * 2.5 + DOWN * 2.0
        s4_pos = RIGHT * 2.5 + DOWN * 2.0

        node_radius = 0.45
        root_circle = Circle(radius=node_radius, color=GRAY_C, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        root_circle.move_to(root_pos)
        root_lbl = create_text("x", font_size=14, color=YELLOW).move_to(root_pos)
        root_group = VGroup(root_circle, root_lbl)

        s1_circle = Circle(radius=node_radius, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        s1_circle.move_to(s1_pos)
        s1_lbl = create_text("s1", font_size=13, color=WHITE).move_to(s1_pos)
        s1_group = VGroup(s1_circle, s1_lbl)

        s2_circle = Circle(radius=node_radius, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        s2_circle.move_to(s2_pos)
        s2_lbl = create_text("s2", font_size=13, color=WHITE).move_to(s2_pos)
        s2_group = VGroup(s2_circle, s2_lbl)

        s3_circle = Circle(radius=node_radius, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        s3_circle.move_to(s3_pos)
        s3_lbl = create_text("s3", font_size=13, color=WHITE).move_to(s3_pos)
        s3_group = VGroup(s3_circle, s3_lbl)

        s4_circle = Circle(radius=node_radius, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, stroke_width=2)
        s4_circle.move_to(s4_pos)
        s4_lbl = create_text("s4", font_size=13, color=WHITE).move_to(s4_pos)
        s4_group = VGroup(s4_circle, s4_lbl)

        line_root_s1 = Line(start=root_pos + DOWN * node_radius, end=s1_pos + UP * node_radius, color=GRAY_E, stroke_width=2)
        line_root_s2 = Line(start=root_pos + DOWN * node_radius, end=s2_pos + UP * node_radius, color=GRAY_E, stroke_width=2)
        line_s1_s3 = Line(start=s1_pos + DOWN * node_radius, end=s3_pos + UP * node_radius, color=GRAY_E, stroke_width=1.5)
        line_s2_s4 = Line(start=s2_pos + DOWN * node_radius, end=s4_pos + UP * node_radius, color=GRAY_E, stroke_width=1.5)
        
        static_tree = VGroup(line_root_s1, line_root_s2, line_s1_s3, line_s2_s4, root_group, s1_group, s2_group, s3_group, s4_group)
        self.play(FadeIn(static_tree), run_time=1.0)

        # Animate exploration of s2 branch
        self.wait_until(cue_start[8] + 2.2)
        path_root_s2 = Line(start=root_pos + DOWN * node_radius, end=s2_pos + UP * node_radius, color=YELLOW, stroke_width=4.0)
        self.play(Create(path_root_s2), s2_circle.animate.set_color(YELLOW), run_time=0.8)

        # Fail s2
        self.wait_until(cue_start[8] + 4.2)
        s2_score = create_text("PRM: 0.20", font_size=11, color=RED).next_to(s2_circle, RIGHT, buff=0.15)
        s2_cross = get_crossmark().next_to(s2_score, RIGHT, buff=0.1)
        self.play(FadeIn(s2_score), Create(s2_cross), s2_circle.animate.set_color(RED), run_time=0.8)

        # Backtrack to root (Cue 9)
        self.wait_until(cue_start[9] + 0.2)
        backtrack_path = Line(start=s2_pos + UP * node_radius, end=root_pos + DOWN * node_radius, color=RED, stroke_width=4.0)
        self.play(ReplacementTransform(path_root_s2, backtrack_path), run_time=0.5)
        self.play(FadeOut(backtrack_path), s2_circle.animate.set_color(GRAY_D), run_time=0.5)

        # Explore s1 branch
        self.wait_until(cue_start[9] + 2.0)
        path_root_s1 = Line(start=root_pos + DOWN * node_radius, end=s1_pos + UP * node_radius, color=GREEN, stroke_width=4.0)
        self.play(Create(path_root_s1), s1_circle.animate.set_color(GREEN), run_time=0.8)

        # Pass s1
        self.wait_until(cue_start[9] + 3.2)
        s1_score = create_text("PRM: 0.95", font_size=11, color=GREEN).next_to(s1_circle, LEFT, buff=0.15)
        s1_check = get_checkmark().next_to(s1_score, LEFT, buff=0.1)
        self.play(FadeIn(s1_score), Create(s1_check), s1_circle.animate.set_color(GREEN), run_time=0.6)

        # Explore s3 branch
        self.wait_until(cue_start[9] + 4.5)
        path_s1_s3 = Line(start=s1_pos + DOWN * node_radius, end=s3_pos + UP * node_radius, color=GREEN, stroke_width=4.0)
        self.play(Create(path_s1_s3), s3_circle.animate.set_color(GREEN), run_time=0.8)

        # Pass s3
        self.wait_until(cue_start[9] + 5.7)
        s3_score = create_text("PRM: 0.85", font_size=11, color=GREEN).next_to(s3_circle, LEFT, buff=0.15)
        s3_check = get_checkmark().next_to(s3_score, LEFT, buff=0.1)
        self.play(FadeIn(s3_score), Create(s3_check), s3_circle.animate.set_color(GREEN), run_time=0.6)

        # Output final answer
        self.wait_until(cue_start[9] + 6.8)
        y_box = RoundedRectangle(width=2.4, height=0.6, color=GREEN, fill_color="#143c14", fill_opacity=0.9, corner_radius=0.06)
        y_box.move_to(LEFT * 2.5 + DOWN * 2.8)
        y_lbl = create_text("y_correct (Answer)", font_size=11, color=WHITE).move_to(y_box.get_center())
        arrow_to_y = Arrow(start=s3_circle.get_bottom(), end=y_box.get_top(), color=GREEN, stroke_width=1.5, buff=0.05)
        y_group = VGroup(y_box, y_lbl, arrow_to_y)
        self.play(FadeIn(y_group), run_time=0.8)
        
        dynamic_tree_group = VGroup(
            tree_intro, static_tree, s2_score, s2_cross, s1_score, s1_check, 
            path_root_s1, path_s1_s3, s3_score, s3_check, y_group
        )
        content = VGroup(part5_title, dynamic_tree_group)

        # --- Cue 10-13: Parallel vs Tree Search Evaluation timing ---
        self.wait_until(cue_start[10] + 0.25)
        self.play(FadeOut(content), run_time=0.4)
        
        comp_title = create_text("Comparison: Evaluation Timing", font_size=13, color=YELLOW)
        comp_title.next_to(sub_title, DOWN, buff=0.3)
        
        comp_box = RoundedRectangle(width=9.2, height=2.6, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        comp_box.move_to(DOWN * 0.4)
        
        comp_line1 = create_markup_text("• Parallel generation usually waits until a <b>full sequence</b> is complete.", font_size=10.5, color=GRAY_A)
        comp_line2 = create_markup_text("• Tree search uses scores on <b>intermediate states</b> step-by-step.", font_size=10.5, color=GRAY_A)
        comp_line3 = create_markup_text("• Allows stopping bad branches early, backtracking, and dynamic budget allocation.", font_size=10.5, color=GRAY_A)
        
        comp_list = VGroup(comp_line1, comp_line2, comp_line3).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(comp_box.get_center())
        comp_group = VGroup(comp_title, comp_box, comp_list)
        
        self.play(FadeIn(comp_title), FadeIn(comp_box), FadeIn(comp_line1), run_time=0.8)
        
        self.wait_until(cue_start[11] + 0.15)
        self.play(comp_line1.animate.set_color(WHITE), run_time=0.4)
        
        self.wait_until(cue_start[12] + 0.15)
        self.play(FadeIn(comp_line2), comp_line2.animate.set_color(WHITE), run_time=0.4)
        
        self.wait_until(cue_start[13] + 0.15)
        self.play(FadeIn(comp_line3), comp_line3.animate.set_color(WHITE), run_time=0.4)
        
        content = comp_group

        # --- Cue 14-15: Limitations of Tree Search & Expert Panel Quote ---
        self.wait_until(cue_start[14] + 0.2)
        self.play(FadeOut(content), run_time=0.4)
        
        limit_title = create_text("Limitations of Tree Search & Expert Panel", font_size=13, color=YELLOW)
        limit_title.next_to(sub_title, DOWN, buff=0.3)
        
        limit_box = RoundedRectangle(width=9.2, height=1.6, color=RED, fill_color="#2b1414", fill_opacity=0.8, corner_radius=0.08)
        limit_box.move_to(UP * 0.4)
        
        limit_desc = create_markup_text(
            "Tree search fails or provides no benefit if:\n"
            "  • Task is <b>non-decomposable</b> into sequential states\n"
            "  • Environment does <b>not provide intermediate feedback</b>\n"
            "  • Process Reward Model (PRM) signal is <b>weak or noisy</b>",
            font_size=10.5, color=WHITE, line_spacing=1.3
        ).move_to(limit_box.get_center())
        
        panel_box = RoundedRectangle(width=9.5, height=1.3, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.08)
        panel_box.move_to(DOWN * 1.8)
        panel_title = create_text("Takeaway from the NeurIPS 2024 expert panel:", font_size=10, color=GOLD_B)
        panel_title.move_to(panel_box.get_center() + UP * 0.4)
        panel_desc = create_markup_text(
            "<i>\"Inference Compute is an infinite frontier. For humanity's most important problems,\n"
            "people are willing to pay thousands of dollars for an accurate answer through Tree Search.\"</i>  -- Noam Brown",
            font_size=9, color=WHITE, line_spacing=1.3
        ).move_to(panel_box.get_center() + DOWN * 0.25)
        
        limit_panel_group = VGroup(limit_title, limit_box, limit_desc, panel_box, panel_title, panel_desc)
        self.play(FadeIn(limit_panel_group), run_time=1.2)
        
        # Hold at the end to allow reading
        self.wait_until(voiceover_end + 0.2)
        self.wait(15.0)
        
        self.play(
            FadeOut(limit_panel_group),
            FadeOut(sub_title),
            run_time=0.8
        )
        self.wait(1.5)
        
        assert_all_scene_voiceovers_played(self)
