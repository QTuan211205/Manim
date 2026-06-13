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


def create_state_node(label, position, color=BLUE_B, radius=0.32, fill="#181a1e"):
    circle = Circle(radius=radius, color=color, fill_color=fill, fill_opacity=0.9, stroke_width=2)
    circle.move_to(position)
    text = create_text(label, font_size=11, color=WHITE).move_to(position)
    return VGroup(circle, text)


def create_score_badge(text, color=GREEN, width=0.82):
    box = RoundedRectangle(width=width, height=0.28, corner_radius=0.05, color=color, fill_color="#151819", fill_opacity=0.95, stroke_width=1.2)
    label = create_text(text, font_size=7.5, color=color).move_to(box.get_center())
    return VGroup(box, label)


def create_step_card(label, score=None, color=BLUE_B, width=1.35):
    card = RoundedRectangle(width=width, height=0.48, corner_radius=0.06, color=color, fill_color="#17191d", fill_opacity=0.95, stroke_width=1.4)
    text = create_text(label, font_size=9, color=WHITE).move_to(card.get_center())
    group = VGroup(card, text)
    if score is not None:
        badge = create_score_badge(score, color=GREEN if float(score) >= 0.7 else RED)
        badge.next_to(card, DOWN, buff=0.1)
        group.add(badge)
    return group


def create_compute_tokens(count, color=GREEN):
    tokens = VGroup()
    for _ in range(count):
        tokens.add(Circle(radius=0.055, color=color, fill_color=color, fill_opacity=0.9, stroke_width=0.8))
    tokens.arrange(RIGHT, buff=0.055)
    return tokens


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
        
        root = create_state_node("s0", UP * 1.1, color=YELLOW)
        s1 = create_state_node("s1", LEFT * 2.6 + DOWN * 0.25, color=BLUE_B)
        s2 = create_state_node("s2", RIGHT * 2.6 + DOWN * 0.25, color=BLUE_B)
        s3 = create_state_node("s3", LEFT * 3.6 + DOWN * 1.7, color=GRAY_C)
        s4 = create_state_node("s4", LEFT * 1.6 + DOWN * 1.7, color=GRAY_C)
        s5 = create_state_node("s5", RIGHT * 2.6 + DOWN * 1.7, color=GRAY_C)
        edges = VGroup(
            Arrow(root.get_bottom(), s1.get_top(), color=GRAY_C, stroke_width=1.5, buff=0.08),
            Arrow(root.get_bottom(), s2.get_top(), color=GRAY_C, stroke_width=1.5, buff=0.08),
            Arrow(s1.get_bottom(), s3.get_top(), color=GRAY_D, stroke_width=1.2, buff=0.08),
            Arrow(s1.get_bottom(), s4.get_top(), color=GRAY_D, stroke_width=1.2, buff=0.08),
            Arrow(s2.get_bottom(), s5.get_top(), color=GRAY_D, stroke_width=1.2, buff=0.08),
        )
        prefix_label = create_text("State = reasoning prefix", font_size=9, color=YELLOW).next_to(root, UP, buff=0.2)
        transition_label = create_text("Transition = next step", font_size=8, color=GRAY_A).move_to(LEFT * 0.05 + DOWN * 0.1)
        score_s1 = create_score_badge("v=0.82", GREEN).next_to(s1, LEFT, buff=0.12)
        score_s2 = create_score_badge("v=0.24", RED).next_to(s2, RIGHT, buff=0.12)
        score_label = create_text("Score ranks partial paths", font_size=9, color=GREEN).move_to(RIGHT * 3.0 + UP * 1.05)
        traversal = Dot(root.get_center(), radius=0.08, color=YELLOW)
        traversal_path = VMobject(color=YELLOW, stroke_width=3)
        traversal_path.set_points_smoothly([root.get_center(), s1.get_center(), s4.get_center()])
        strategy_label = create_text("Strategy chooses visit order", font_size=9, color=BLUE_A).move_to(LEFT * 3.0 + UP * 1.05)
        
        part1_group = VGroup(
            part1_title, root, s1, s2, s3, s4, s5, edges, prefix_label, transition_label,
            score_s1, score_s2, score_label, traversal, traversal_path, strategy_label
        )
        self.play(FadeIn(part1_title), FadeIn(edges), FadeIn(root), FadeIn(prefix_label), run_time=1.0)
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(transition_label), run_time=0.8)
        self.play(FadeIn(score_s1), FadeIn(score_s2), FadeIn(score_label), run_time=0.8)
        self.play(FadeIn(s3), FadeIn(s4), FadeIn(s5), run_time=0.7)
        self.play(MoveAlongPath(traversal, traversal_path), FadeIn(strategy_label), run_time=2.3)
            
        content = part1_group

        # --- Cue 3: Process-based Reward Model ---
        self.wait_until(cue_start[3] + 0.25)
        self.play(FadeOut(content), run_time=0.4)
        
        part2_title = create_text("2. Process-based Reward Model (PRM)", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)
        
        orm_label = create_text("ORM", font_size=12, color=BLUE_A).move_to(LEFT * 4.4 + UP * 1.55)
        prm_label = create_text("PRM", font_size=12, color=GOLD_A).move_to(LEFT * 4.4 + DOWN * 0.75)
        orm_steps = VGroup(
            create_step_card("s1"),
            create_step_card("s2"),
            create_step_card("s3"),
            create_step_card("answer", color=GREEN_B),
        ).arrange(RIGHT, buff=0.18).move_to(UP * 1.05 + RIGHT * 0.25)
        prm_steps = VGroup(
            create_step_card("s1", "0.79", color=GOLD_B),
            create_step_card("s2", "0.18", color=GOLD_B),
            create_step_card("s3", "0.86", color=GOLD_B),
            create_step_card("answer", "0.90", color=GREEN_B),
        ).arrange(RIGHT, buff=0.18).move_to(DOWN * 1.25 + RIGHT * 0.25)
        orm_arrows = VGroup(*[
            Arrow(orm_steps[i].get_right(), orm_steps[i + 1].get_left(), color=GRAY_C, stroke_width=1.3, buff=0.05)
            for i in range(3)
        ])
        prm_arrows = VGroup(*[
            Arrow(prm_steps[i].get_right(), prm_steps[i + 1].get_left(), color=GRAY_C, stroke_width=1.3, buff=0.05)
            for i in range(3)
        ])
        final_meter = create_score_badge("final score", GREEN, width=1.25).next_to(orm_steps[-1], RIGHT, buff=0.35)
        final_arrow = Arrow(orm_steps[-1].get_right(), final_meter.get_left(), color=GREEN, stroke_width=1.6, buff=0.08)
        prm_probe = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=0.9).scale(0.16).rotate(PI)
        prm_probe.next_to(prm_steps[0], UP, buff=0.22)
        prm_formula = create_markup_text(
            "<span color='#FFD700'><i>v</i>(<i>x</i>, <i>s</i><sub>1:t</sub>) → [0, 1]</span>",
            font_size=12
        ).move_to(DOWN * 2.5)
        
        orm_full = VGroup(orm_label, orm_steps, orm_arrows, final_meter, final_arrow)
        prm_full = VGroup(prm_label, prm_steps, prm_arrows, prm_probe, prm_formula)
        self.play(FadeIn(part2_title), FadeIn(orm_label), FadeIn(orm_steps), FadeIn(orm_arrows), run_time=1.0)
        self.play(FadeIn(final_meter), Create(final_arrow), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(prm_label), FadeIn(prm_steps), FadeIn(prm_arrows), FadeIn(prm_formula), run_time=1.0)
        for target in prm_steps[1:]:
            self.play(prm_probe.animate.next_to(target, UP, buff=0.22), run_time=0.55)
        
        content = VGroup(part2_title, orm_full, prm_full)

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
        
        budget_pool = create_compute_tokens(10, color=BLUE_A).move_to(DOWN * 0.35)
        budget_label = create_text("Budget", font_size=9, color=BLUE_A).next_to(budget_pool, UP, buff=0.18)
        branch_a = create_state_node("sA", LEFT * 3.25 + DOWN * 1.35, color=GREEN, radius=0.28)
        branch_b = create_state_node("sB", RIGHT * 3.25 + DOWN * 1.35, color=RED, radius=0.28)
        score_a_bar = Rectangle(width=1.55, height=0.14, color=GREEN, fill_color=GREEN, fill_opacity=0.85).next_to(branch_a, RIGHT, buff=0.2)
        score_b_bar = Rectangle(width=0.52, height=0.14, color=RED, fill_color=RED, fill_opacity=0.85).next_to(branch_b, LEFT, buff=0.2)
        score_a = create_text("PRM 0.90", font_size=8, color=GREEN).next_to(score_a_bar, UP, buff=0.08)
        score_b = create_text("PRM 0.30", font_size=8, color=RED).next_to(score_b_bar, UP, buff=0.08)
        temp_slider = Line(LEFT * 0.9, RIGHT * 0.9, color=ORANGE, stroke_width=2)
        temp_dot = Dot(RIGHT * 0.45, radius=0.07, color=ORANGE)
        temp_label = create_text("tau controls focus", font_size=8, color=ORANGE).next_to(temp_slider, DOWN, buff=0.12)
        temp_knob = VGroup(temp_slider, temp_dot, temp_label).move_to(DOWN * 2.1)
        visual_terms = VGroup(
            budget_pool, budget_label, branch_a, branch_b, score_a_bar, score_b_bar,
            score_a, score_b, temp_knob
        )
        
        self.play(FadeIn(visual_terms, shift=UP * 0.15), run_time=1.0)
        rebase_full_group = VGroup(content, visual_terms)

        # --- Cue 6: Rebase Node Allocation Example ---
        self.wait_until(cue_start[6] + 0.2)
        self.play(FadeOut(visual_terms), run_time=0.4)
        
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
        
        tokens_a = create_compute_tokens(9, color=GREEN).next_to(node_a, DOWN, buff=0.28)
        tokens_b = create_compute_tokens(1, color=RED).next_to(node_b, DOWN, buff=0.28)
        alloc_a = create_text("9 Streams", font_size=9, color=GREEN).next_to(tokens_a, DOWN, buff=0.1)
        alloc_b = create_text("1 Stream", font_size=9, color=RED).next_to(tokens_b, DOWN, buff=0.1)
        
        self.play(FadeIn(tokens_a, shift=UP * 0.1), FadeIn(tokens_b, shift=UP * 0.1), FadeIn(alloc_a), FadeIn(alloc_b), run_time=0.8)

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
        rebase_example_group = VGroup(sim_title, node_a_group, node_b_group, tokens_a, tokens_b, alloc_a, alloc_b, arrows_a, arrows_b)
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
        
        parallel_label = create_text("Parallel", font_size=11, color=BLUE_A).move_to(LEFT * 4.65 + UP * 0.95)
        tree_label = create_text("Tree search", font_size=11, color=GREEN_A).move_to(LEFT * 4.65 + DOWN * 1.05)
        parallel_cards = VGroup(
            create_step_card("y1", color=BLUE_B, width=0.95),
            create_step_card("y2", color=BLUE_B, width=0.95),
            create_step_card("y3", color=BLUE_B, width=0.95),
        ).arrange(RIGHT, buff=0.45).move_to(LEFT * 0.6 + UP * 0.95)
        verifier = RoundedRectangle(width=1.55, height=0.55, corner_radius=0.07, color=YELLOW, fill_color="#1c1a11", fill_opacity=0.95)
        verifier.next_to(parallel_cards, RIGHT, buff=0.55)
        verifier_text = create_text("Verify\nat end", font_size=8, color=YELLOW).move_to(verifier.get_center())
        parallel_arrows = VGroup(*[
            Arrow(card.get_right(), verifier.get_left(), color=YELLOW, stroke_width=1.1, buff=0.05)
            for card in parallel_cards
        ])
        tree_root = create_state_node("s0", LEFT * 2.2 + DOWN * 0.8, color=YELLOW, radius=0.25)
        tree_good = create_state_node("s1", LEFT * 0.65 + DOWN * 0.55, color=GREEN, radius=0.25)
        tree_bad = create_state_node("s2", LEFT * 0.65 + DOWN * 1.55, color=RED, radius=0.25)
        tree_next = create_state_node("s3", RIGHT * 1.0 + DOWN * 0.55, color=GREEN, radius=0.25)
        tree_answer = create_step_card("answer", "0.91", color=GREEN_B, width=1.05).move_to(RIGHT * 2.85 + DOWN * 0.55)
        tree_edges = VGroup(
            Arrow(tree_root.get_right(), tree_good.get_left(), color=GREEN, stroke_width=1.4, buff=0.05),
            Arrow(tree_root.get_right(), tree_bad.get_left(), color=RED, stroke_width=1.4, buff=0.05),
            Arrow(tree_good.get_right(), tree_next.get_left(), color=GREEN, stroke_width=1.4, buff=0.05),
            Arrow(tree_next.get_right(), tree_answer.get_left(), color=GREEN, stroke_width=1.4, buff=0.05),
        )
        checkpoint_1 = create_score_badge("0.84", GREEN).next_to(tree_good, UP, buff=0.08)
        checkpoint_2 = create_score_badge("0.12", RED).next_to(tree_bad, DOWN, buff=0.08)
        prune_cross = get_crossmark(color=RED, stroke_width=3).move_to(tree_bad.get_center() + RIGHT * 0.5)
        backtrack_arrow = CurvedArrow(tree_bad.get_top(), tree_root.get_bottom(), angle=TAU / 4, color=RED, stroke_width=2)
        compute_shift = create_compute_tokens(6, color=GREEN).next_to(tree_next, UP, buff=0.25)
        compute_label = create_text("Reallocate compute", font_size=8, color=GREEN).next_to(compute_shift, UP, buff=0.08)
        comp_group = VGroup(
            comp_title, parallel_label, tree_label, parallel_cards, verifier, verifier_text,
            parallel_arrows, tree_root, tree_good, tree_bad, tree_next, tree_answer, tree_edges,
            checkpoint_1, checkpoint_2, prune_cross, backtrack_arrow, compute_shift, compute_label
        )
        
        self.play(FadeIn(comp_title), FadeIn(parallel_label), FadeIn(parallel_cards), run_time=0.8)
        
        self.wait_until(cue_start[11] + 0.15)
        self.play(FadeIn(verifier), FadeIn(verifier_text), Create(parallel_arrows), run_time=0.7)
        
        self.wait_until(cue_start[12] + 0.15)
        self.play(
            FadeIn(tree_label), FadeIn(tree_root), FadeIn(tree_good), FadeIn(tree_bad),
            Create(tree_edges[:2]), FadeIn(checkpoint_1), FadeIn(checkpoint_2), run_time=0.8
        )
        
        self.wait_until(cue_start[13] + 0.15)
        self.play(Create(prune_cross), Create(backtrack_arrow), run_time=0.55)
        self.play(FadeIn(tree_next), FadeIn(tree_answer), Create(tree_edges[2:]), FadeIn(compute_shift), FadeIn(compute_label), run_time=0.8)
        
        content = comp_group

        # --- Cue 14-15: Limitations of Tree Search & Expert Panel Quote ---
        self.wait_until(cue_start[14] + 0.2)
        self.play(FadeOut(content), run_time=0.4)
        
        limit_title = create_text("Limitations of Tree Search & Expert Panel", font_size=13, color=YELLOW)
        limit_title.next_to(sub_title, DOWN, buff=0.3)
        
        card_specs = [
            ("no states", "cannot split\ninto steps", RED),
            ("no feedback", "nothing to score\nmid-solution", ORANGE),
            ("noisy PRM", "wrong branches\nlook promising", RED_B),
        ]
        limit_cards = VGroup()
        for heading, body, color in card_specs:
            box = RoundedRectangle(width=2.55, height=1.35, color=color, fill_color="#211719", fill_opacity=0.92, corner_radius=0.08)
            icon = Triangle(color=color, fill_color=color, fill_opacity=0.85).scale(0.16).rotate(PI)
            icon.move_to(box.get_center() + UP * 0.42)
            head = create_text(heading, font_size=10, color=color).move_to(box.get_center() + UP * 0.08)
            desc = create_text(body, font_size=7.5, color=GRAY_A, line_spacing=1.05).move_to(box.get_center() + DOWN * 0.37)
            limit_cards.add(VGroup(box, icon, head, desc))
        limit_cards.arrange(RIGHT, buff=0.35).move_to(UP * 0.35)
        
        panel_box = RoundedRectangle(width=8.6, height=1.25, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.08)
        panel_box.move_to(DOWN * 1.75)
        panel_title = create_text("Takeaway from the NeurIPS 2024 expert panel:", font_size=10, color=GOLD_B)
        panel_title.move_to(panel_box.get_center() + UP * 0.4)
        panel_desc = create_markup_text(
            "<i>\"Inference Compute is an infinite frontier. For humanity's most important problems,\n"
            "people are willing to pay thousands of dollars for an accurate answer through Tree Search.\"</i>  -- Noam Brown",
            font_size=9, color=WHITE, line_spacing=1.3
        ).move_to(panel_box.get_center() + DOWN * 0.25)
        
        limit_panel_group = VGroup(limit_title, limit_cards, panel_box, panel_title, panel_desc)
        self.play(FadeIn(limit_title), FadeIn(limit_cards, shift=UP * 0.12), run_time=0.9)
        self.play(FadeIn(panel_box), FadeIn(panel_title), FadeIn(panel_desc), run_time=0.8)
        
        # End about two seconds after the final voiceover.
        self.wait_until(voiceover_end + 1.2)
        
        self.play(
            FadeOut(limit_panel_group),
            FadeOut(sub_title),
            run_time=0.8
        )
        
        assert_all_scene_voiceovers_played(self)
