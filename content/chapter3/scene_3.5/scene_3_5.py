import os
import tempfile
from pathlib import Path

from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_3_5_DURATIONS = {
    "sc35_001.mp3": 5.897868,
    "sc35_002.mp3": 3.436553,
    "sc35_003.mp3": 3.622313,
    "sc35_004.mp3": 11.517098,
    "sc35_005.mp3": 10.30966,
    "sc35_006.mp3": 6.919546,
    "sc35_007.mp3": 2.739955,
    "sc35_008.mp3": 3.808073,
    "sc35_009.mp3": 3.482993,
    "sc35_010.mp3": 7.523265,
    "sc35_011.mp3": 5.572789,
    "sc35_012.mp3": 4.179592,
    "sc35_013.mp3": 7.755465,
    "sc35_014.mp3": 8.777143,
    "sc35_015.mp3": 8.823583,
    "sc35_016.mp3": 2.647075,
    "sc35_017.mp3": 9.148662,
    "sc35_018.mp3": 6.780227,
}
SCENE_3_5_VOICEOVERS = tuple(SCENE_3_5_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc35_*.mp3"))
    expected = sorted(SCENE_3_5_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 3.5 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_3_5_DURATIONS:
        raise KeyError(f"Unexpected Scene 3.5 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 3.5 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_3_5_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_3_5_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 3.5 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
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


def labeled_box(title, body="", width=2.1, height=0.9, color=BLUE_A, fill="#15181d"):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.07,
        color=color,
        fill_color=fill,
        fill_opacity=0.94,
        stroke_width=1.5,
    )
    title_obj = create_text(title, font_size=10, color=color).move_to(box.get_center() + UP * height * 0.18)
    if body:
        body_obj = create_text(body, font_size=7.5, color=GRAY_A, line_spacing=1.05).move_to(
            box.get_center() + DOWN * height * 0.18
        )
        return VGroup(box, title_obj, body_obj)
    title_obj.move_to(box.get_center())
    return VGroup(box, title_obj)


def compute_tokens(count, color=BLUE_A):
    tokens = VGroup()
    for _ in range(count):
        tokens.add(Circle(radius=0.07, color=color, fill_color=color, fill_opacity=0.95, stroke_width=0.7))
    tokens.arrange(RIGHT, buff=0.055)
    return tokens


def make_knob(label, value, color, width=2.8):
    base = Line(LEFT * width / 2, RIGHT * width / 2, color=GRAY_D, stroke_width=5)
    dot = Dot(base.get_left() + RIGHT * width * value, radius=0.09, color=color)
    lbl = create_text(label, font_size=9, color=color).next_to(base, UP, buff=0.15)
    return VGroup(base, dot, lbl)


def frontier_axes():
    axes = Axes(
        x_range=[0, 10, 2],
        y_range=[0, 1.0, 0.2],
        x_length=5.8,
        y_length=3.25,
        axis_config={"color": GRAY_C, "stroke_width": 1.5},
        tips=False,
    )
    x_lbl = create_text("Compute cost", font_size=8, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.12)
    y_lbl = create_text("Lower error", font_size=8, color=GRAY_A).next_to(axes.y_axis, LEFT, buff=0.15).rotate(PI / 2)
    curve = axes.plot(lambda x: 0.78 / (x + 1) + 0.08, x_range=[0.2, 10], color=GREEN, stroke_width=3.5)
    label = create_text("Compute-optimal frontier", font_size=8, color=GREEN).move_to(axes.c2p(7.0, 0.34))
    return VGroup(axes, x_lbl, y_lbl, curve, label)


class Scene3_5(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (_, duration) in enumerate(SCENE_3_5_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        chapter_title = create_text("Chapter 3: High-Level Orchestrators", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 3.5: Scaling Meta-Generators & Compute Allocation", font_size=17, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub).move_to(ORIGIN)
        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)
        self.wait_until(cue_start[2])

        sub_title = create_text("Scaling Meta-Generators & Compute Allocation", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=0.8)

        budget = labeled_box("Compute budget C", "test-time compute", width=2.4, height=0.9, color=YELLOW).move_to(UP * 1.2)
        tokens = compute_tokens(14, YELLOW).next_to(budget, DOWN, buff=0.25)
        performance = labeled_box("Task performance", "what improves?", width=2.35, height=0.9, color=GREEN).move_to(LEFT * 3.1 + DOWN * 0.9)
        cost = labeled_box("Compute cost", "what we pay", width=2.25, height=0.9, color=RED_B).move_to(RIGHT * 3.1 + DOWN * 0.9)
        arrows_intro = VGroup(
            Arrow(tokens.get_left(), performance.get_top(), color=GREEN, stroke_width=1.4, buff=0.08),
            Arrow(tokens.get_right(), cost.get_top(), color=RED_B, stroke_width=1.4, buff=0.08),
        )
        self.play(FadeIn(budget), FadeIn(tokens, lag_ratio=0.04), run_time=0.8)
        self.wait_until(cue_start[3])
        self.play(FadeIn(performance), FadeIn(cost), Create(arrows_intro), run_time=0.8)

        self.wait_until(cue_start[4])
        self.play(FadeOut(VGroup(budget, tokens, performance, cost, arrows_intro)), run_time=0.5)

        opt_title = create_text("Choose N, T, S under the same budget", font_size=12, color=BLUE_A).next_to(
            sub_title, DOWN, buff=0.35
        )
        formula = create_markup_text(
            "minimize error(N, T, S)    subject to    cost(N, T, S) = C",
            font_size=13,
            color=YELLOW,
        ).move_to(UP * 1.6)
        n_knob = make_knob("N: model size", 0.35, BLUE_A).move_to(LEFT * 3.0 + DOWN * 0.3)
        t_knob = make_knob("T: generated tokens", 0.65, GREEN).move_to(RIGHT * 3.0 + DOWN * 0.3)
        s_knob = make_knob("S: strategy", 0.82, PURPLE_A).move_to(DOWN * 1.75)
        knob_group = VGroup(n_knob, t_knob, s_knob)
        self.play(FadeIn(opt_title), FadeIn(formula), FadeIn(knob_group, lag_ratio=0.12), run_time=1.1)

        self.wait_until(cue_start[5])
        flops_meter = VGroup(
            create_text("FLOP meter", font_size=9, color=GRAY_A),
            Line(LEFT * 2.2, RIGHT * 2.2, color=GRAY_D, stroke_width=7),
        ).arrange(DOWN, buff=0.12).move_to(DOWN * 2.75)
        flops_fill = Line(flops_meter[1].get_left(), flops_meter[1].get_left() + RIGHT * 3.0, color=YELLOW, stroke_width=7)
        self.play(FadeIn(flops_meter), Create(flops_fill), run_time=0.8)

        self.wait_until(cue_start[6])
        self.play(FadeOut(VGroup(opt_title, formula, knob_group, flops_meter, flops_fill)), run_time=0.5)

        trade_title = create_text("Small model + more generations vs large model + fewer generations", font_size=11, color=YELLOW)
        trade_title.next_to(sub_title, DOWN, buff=0.35)
        small_model = Circle(radius=0.48, color=BLUE_A, fill_color="#102033", fill_opacity=0.95).move_to(LEFT * 3.1 + UP * 0.55)
        small_lbl = create_text("Small N", font_size=9, color=BLUE_A).move_to(small_model.get_center())
        many_samples = VGroup(*[compute_tokens(4, GREEN).scale(0.85) for _ in range(3)]).arrange(DOWN, buff=0.16).next_to(
            small_model, DOWN, buff=0.35
        )
        large_model = Circle(radius=0.78, color=RED_B, fill_color="#2b1414", fill_opacity=0.95).move_to(RIGHT * 3.1 + UP * 0.55)
        large_lbl = create_text("Large N", font_size=9, color=RED_B).move_to(large_model.get_center())
        few_samples = compute_tokens(5, GREEN).next_to(large_model, DOWN, buff=0.45)
        budget_brace = BraceBetweenPoints(LEFT * 4.4 + DOWN * 2.0, RIGHT * 4.4 + DOWN * 2.0, color=YELLOW)
        equal_cost = VGroup(
            budget_brace,
            create_text("Same compute budget C", font_size=9, color=YELLOW).next_to(budget_brace, DOWN, buff=0.3),
        )
        self.play(
            FadeIn(trade_title),
            FadeIn(VGroup(small_model, small_lbl, many_samples)),
            FadeIn(VGroup(large_model, large_lbl, few_samples)),
            FadeIn(equal_cost),
            run_time=1.0,
        )

        self.wait_until(cue_start[7])
        win_ring = SurroundingRectangle(VGroup(small_model, small_lbl, many_samples), color=GREEN, buff=0.18, stroke_width=3)
        win_note = create_text("Sometimes compute-optimal", font_size=10, color=GREEN).next_to(win_ring, UP, buff=0.18)
        self.play(Create(win_ring), FadeIn(win_note), run_time=0.75)

        self.wait_until(cue_start[8])
        self.play(FadeOut(VGroup(trade_title, small_model, small_lbl, many_samples, large_model, large_lbl, few_samples, equal_cost, win_ring, win_note)), run_time=0.5)

        strategy_title = create_text("Which strategy is compute-optimal?", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        frontier = frontier_axes().move_to(LEFT * 2.7 + DOWN * 0.35)
        greedy_pt = Dot(frontier[0].c2p(3.0, 0.36), radius=0.09, color=GRAY_B)
        bestofn_pt = Dot(frontier[0].c2p(5.5, 0.23), radius=0.09, color=BLUE_A)
        rebase_pt = Dot(frontier[0].c2p(4.4, 0.20), radius=0.11, color=YELLOW)
        rebase_lbl = create_text("Rebase / tree search", font_size=9, color=YELLOW).move_to(frontier[0].c2p(5.0, 0.38))
        tree = VGroup()
        root = Dot(ORIGIN, radius=0.07, color=YELLOW)
        nodes = VGroup(Dot(LEFT * 0.7 + DOWN * 0.55, radius=0.055, color=GREEN), Dot(RIGHT * 0.7 + DOWN * 0.55, radius=0.055, color=RED_B))
        leaves = VGroup(Dot(LEFT * 1.05 + DOWN * 1.1, radius=0.045, color=GREEN), Dot(LEFT * 0.35 + DOWN * 1.1, radius=0.045, color=GREEN))
        edges = VGroup(
            Line(root.get_center(), nodes[0].get_center(), color=GRAY_B),
            Line(root.get_center(), nodes[1].get_center(), color=GRAY_B),
            Line(nodes[0].get_center(), leaves[0].get_center(), color=GREEN),
            Line(nodes[0].get_center(), leaves[1].get_center(), color=GREEN),
        )
        tree.add(edges, root, nodes, leaves).scale(1.35).move_to(RIGHT * 3.15 + DOWN * 0.4)
        tree_label = create_text("Reallocate search budget", font_size=9, color=GREEN).next_to(tree, DOWN, buff=0.25)
        self.play(FadeIn(strategy_title), FadeIn(frontier), FadeIn(VGroup(greedy_pt, bestofn_pt)), FadeIn(tree), run_time=1.0)

        self.wait_until(cue_start[9])
        self.play(Create(rebase_pt), FadeIn(rebase_lbl), FadeIn(tree_label), root.animate.set_color(YELLOW), run_time=0.9)

        self.wait_until(cue_start[10])
        self.play(FadeOut(VGroup(strategy_title, frontier, greedy_pt, bestofn_pt, rebase_pt, rebase_lbl, tree, tree_label)), run_time=0.5)

        recap_title = create_text("Scaling recap: more compute helps, but optimum moves", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        axes = frontier_axes().move_to(LEFT * 3.0 + DOWN * 0.45)
        axes[4].move_to(axes[0].c2p(5.1, 0.5))
        low_budget = DashedLine(axes[0].c2p(2.2, 0), axes[0].c2p(2.2, 1), color=RED_B)
        high_budget = DashedLine(axes[0].c2p(7.6, 0), axes[0].c2p(7.6, 1), color=GREEN)
        opt_low = Dot(axes[0].c2p(2.2, 0.32), color=YELLOW, radius=0.1)
        opt_high = Dot(axes[0].c2p(7.6, 0.17), color=YELLOW, radius=0.1)
        moving_optimum = VGroup(low_budget, high_budget, opt_low, opt_high)
        budget_map = VGroup(
            labeled_box("Tight C", "small model\ncheap strategy", width=1.8, height=1.0, color=RED_B),
            labeled_box("Larger C", "different N\n+ strategy", width=1.8, height=1.0, color=GREEN),
        ).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.25 + DOWN * 0.1)
        self.play(FadeIn(recap_title), FadeIn(axes), FadeIn(moving_optimum), FadeIn(budget_map), run_time=1.0)

        self.wait_until(cue_start[11])
        opt_arrow = Arrow(opt_low.get_center(), opt_high.get_center(), color=YELLOW, stroke_width=2, buff=0.12)
        self.play(Create(opt_arrow), budget_map[0].animate.set_opacity(0.35), run_time=0.8)

        self.wait_until(cue_start[12])
        universal = labeled_box("Long-term goal", "universally optimal\nstrategies", width=2.6, height=1.1, color=PURPLE_A)
        universal.move_to(RIGHT * 3.25 + DOWN * 1.75)
        self.play(FadeIn(universal), run_time=0.8)

        self.wait_until(cue_start[13])
        self.play(FadeOut(VGroup(recap_title, axes, moving_optimum, budget_map, opt_arrow, universal)), run_time=0.5)

        bridge_title = create_text("Why systems efficiency comes next", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        many_tokens = VGroup(*[compute_tokens(6, BLUE_A).scale(0.8) for _ in range(4)]).arrange(DOWN, buff=0.18).move_to(LEFT * 2.8)
        tree_paths = VGroup()
        root2 = Dot(ORIGIN, color=YELLOW)
        for angle, color in [(-35, GREEN), (-10, BLUE_A), (15, GREEN), (40, RED_B)]:
            end = RIGHT * 1.5 + UP * (angle / 40)
            tree_paths.add(Arrow(root2.get_center(), end, color=color, stroke_width=1.4, buff=0.05))
        diverse = VGroup(root2, tree_paths).scale(1.4).move_to(RIGHT * 2.8)
        question = create_text("How do we generate quickly?", font_size=12, color=YELLOW).move_to(DOWN * 2.25)
        self.play(FadeIn(bridge_title), FadeIn(many_tokens, lag_ratio=0.06), FadeIn(diverse), FadeIn(question), run_time=1.0)

        self.wait_until(cue_start[14])
        self.play(FadeOut(VGroup(bridge_title, many_tokens, diverse, question)), run_time=0.5)

        dom_title = create_text("Compute-optimal frontier: not dominated", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        dom_axes = frontier_axes().move_to(LEFT * 2.8 + DOWN * 0.45)
        dominated = Dot(dom_axes[0].c2p(5.0, 0.42), radius=0.1, color=RED_B)
        better_error = Dot(dom_axes[0].c2p(5.0, 0.21), radius=0.1, color=GREEN)
        lower_cost = Dot(dom_axes[0].c2p(2.0, 0.42), radius=0.1, color=GREEN)
        arrow_down = Arrow(dominated.get_center(), better_error.get_center(), color=GREEN, stroke_width=2, buff=0.1)
        arrow_left = Arrow(dominated.get_center(), lower_cost.get_center(), color=GREEN, stroke_width=2, buff=0.1)
        dominance_note = VGroup(
            create_text("Same cost -> lower error", font_size=9, color=GREEN),
            create_text("Same error -> lower cost", font_size=9, color=GREEN),
            create_text("Red point is dominated", font_size=9, color=RED_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.2 + DOWN * 0.1)
        self.play(FadeIn(dom_title), FadeIn(dom_axes), FadeIn(dominated), FadeIn(dominance_note[2]), run_time=0.8)
        self.play(FadeIn(better_error), Create(arrow_down), FadeIn(dominance_note[0]), run_time=0.65)
        self.play(FadeIn(lower_cost), Create(arrow_left), FadeIn(dominance_note[1]), run_time=0.65)

        self.wait_until(cue_start[15])
        largest_model = Circle(radius=0.85, color=RED_B, fill_color="#2b1414", fill_opacity=0.9).move_to(RIGHT * 3.2 + UP * 1.35)
        largest_lbl = create_text("Largest model", font_size=9, color=RED_B).move_to(largest_model.get_center())
        not_equal = Cross(VGroup(largest_model, largest_lbl), stroke_color=YELLOW, stroke_width=5)
        choose = create_text("Choose N + T + S for the budget", font_size=10, color=YELLOW).next_to(largest_model, DOWN, buff=0.35)
        self.play(FadeIn(largest_model), FadeIn(largest_lbl), Create(not_equal), FadeIn(choose), run_time=0.8)

        self.wait_until(cue_start[16])
        self.play(FadeOut(VGroup(dom_title, dom_axes, dominated, better_error, lower_cost, arrow_down, arrow_left, dominance_note, largest_model, largest_lbl, not_equal, choose)), run_time=0.5)

        systems_title = create_text("Same token budget, different real latency", font_size=12, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.35
        )
        algo_a = labeled_box("Method A", "sequential\nno prefix sharing", width=2.4, height=1.2, color=RED_B).move_to(LEFT * 3.15 + UP * 0.7)
        algo_b = labeled_box("Method B", "parallelizable\nprefix-shareable", width=2.4, height=1.2, color=GREEN).move_to(RIGHT * 3.15 + UP * 0.7)
        seq_steps = VGroup(*[labeled_box(f"t{i+1}", "", width=0.55, height=0.45, color=RED_B) for i in range(4)]).arrange(RIGHT, buff=0.18).next_to(algo_a, DOWN, buff=0.35)
        seq_arrows = VGroup(*[Arrow(seq_steps[i].get_right(), seq_steps[i + 1].get_left(), color=RED_B, stroke_width=1.2, buff=0.03) for i in range(3)])
        shared_prefix = labeled_box("Shared prefix", "", width=1.4, height=0.45, color=GREEN).next_to(algo_b, DOWN, buff=0.35)
        branches = VGroup(*[labeled_box(f"b{i+1}", "", width=0.55, height=0.38, color=GREEN) for i in range(3)]).arrange(DOWN, buff=0.12).next_to(shared_prefix, RIGHT, buff=0.55)
        branch_arrows = VGroup(*[Arrow(shared_prefix.get_right(), branches[i].get_left(), color=GREEN, stroke_width=1.2, buff=0.04) for i in range(3)])
        latency_a = create_text("High latency", font_size=9, color=RED_B).next_to(seq_steps, DOWN, buff=0.25)
        latency_b = create_text("Lower real cost / latency", font_size=9, color=GREEN).next_to(branches, DOWN, buff=0.2)
        self.play(FadeIn(systems_title), FadeIn(algo_a), FadeIn(algo_b), run_time=0.7)

        self.wait_until(cue_start[17])
        self.play(FadeIn(seq_steps), Create(seq_arrows), FadeIn(latency_a), FadeIn(shared_prefix), FadeIn(branches), Create(branch_arrows), FadeIn(latency_b), run_time=1.0)

        self.wait_until(cue_start[18])
        conclusion = create_text("Cost-performance tradeoff = algorithm + system execution", font_size=12, color=YELLOW).move_to(DOWN * 2.5)
        self.play(FadeIn(conclusion), run_time=0.7)

        self.wait_until(voiceover_end + 0.2)
        self.play(
            FadeOut(VGroup(systems_title, algo_a, algo_b, seq_steps, seq_arrows, latency_a, shared_prefix, branches, branch_arrows, latency_b, conclusion, sub_title)),
            run_time=0.8,
        )

        assert_all_scene_voiceovers_played(self)
