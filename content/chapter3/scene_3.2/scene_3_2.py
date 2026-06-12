import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"
ASSET_DIR = Path(__file__).resolve().parent / "assets"

SCENE_3_2_DURATIONS = {
    "sc32_001.mp3": 9.287982,
    "sc32_002.mp3": 7.476825,
    "sc32_003.mp3": 3.297234,
    "sc32_004.mp3": 7.012426,
    "sc32_005.mp3": 10.727619,
    "sc32_006.mp3": 6.315828,
    "sc32_007.mp3": 4.318912,
    "sc32_008.mp3": 7.383946,
    "sc32_009.mp3": 5.665669,
    "sc32_010.mp3": 2.972154,
    "sc32_011.mp3": 4.040272,
    "sc32_012.mp3": 8.730703,
    "sc32_013.mp3": 5.201270,
    "sc32_014.mp3": 4.411791,
    "sc32_015.mp3": 5.201270,
    "sc32_016.mp3": 5.154830,
    "sc32_017.mp3": 4.226032,
    "sc32_018.mp3": 3.715193,
    "sc32_019.mp3": 4.504671,
    "sc32_020.mp3": 5.944308,
    "sc32_021.mp3": 10.263220,
    "sc32_022.mp3": 10.681179,
    "sc32_023.mp3": 4.040272,
    "sc32_024.mp3": 5.712109,
}
SCENE_3_2_VOICEOVERS = tuple(SCENE_3_2_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc32_*.mp3"))
    expected = sorted(SCENE_3_2_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 3.2 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_3_2_DURATIONS:
        raise KeyError(f"Unexpected Scene 3.2 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 3.2 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_3_2_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_3_2_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 3.2 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
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


def get_voter_icon(color=BLUE_A):
    voter = VGroup()
    body = RoundedRectangle(width=0.24, height=0.2, corner_radius=0.03, color=color, fill_color=color, fill_opacity=0.3, stroke_width=1.2)
    head = Circle(radius=0.08, color=color, fill_color=color, fill_opacity=0.5, stroke_width=1.2)
    head.next_to(body, UP, buff=0.04)
    eye_l = Circle(radius=0.015, color=WHITE, fill_color=WHITE, fill_opacity=1.0).move_to(head.get_center() + LEFT * 0.03 + UP * 0.015)
    eye_r = Circle(radius=0.015, color=WHITE, fill_color=WHITE, fill_opacity=1.0).move_to(head.get_center() + RIGHT * 0.03 + UP * 0.015)
    antenna = Line(start=head.get_top(), end=head.get_top() + UP * 0.05, color=color, stroke_width=1.2)
    antenna_dot = Circle(radius=0.012, color=color, fill_color=color, fill_opacity=1.0).move_to(antenna.get_end())
    voter.add(body, head, eye_l, eye_r, antenna, antenna_dot)
    return voter


def create_slide_crop(filename, max_width=7.8, max_height=3.0):
    image = ImageMobject(str(ASSET_DIR / filename))
    if image.width > max_width:
        image.scale_to_fit_width(max_width)
    if image.height > max_height:
        image.scale_to_fit_height(max_height)
    return image


def create_source_label(width=7.8):
    source = create_text(
        "Source: https://neurips.cc/virtual/2024/tutorial/99522",
        font_size=4.5,
        color=GRAY_B,
    )
    source.scale_to_fit_width(min(width, 3.8))
    return source


def create_asset_panel(filename, title, max_width=7.8, max_height=2.8):
    image = create_slide_crop(filename, max_width=max_width, max_height=max_height)
    title_label = create_text(title, font_size=11, color=BLUE_A)
    title_label.next_to(image, UP, buff=0.18)
    source = create_source_label(max_width)
    source.next_to(image, DOWN, buff=0.12)
    return Group(title_label, image, source)


class Speedometer(VGroup):
    def __init__(self, radius=0.6, title="Reward Model", **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.current_score = 0.0
        
        self.arc = Arc(
            start_angle=PI, 
            angle=-PI, 
            radius=radius, 
            stroke_width=4, 
            color=GRAY_D
        )
        self.red_zone = Arc(start_angle=PI, angle=-PI/3, radius=radius, stroke_width=4, color=RED)
        self.yellow_zone = Arc(start_angle=2*PI/3, angle=-PI/3, radius=radius, stroke_width=4, color=YELLOW)
        self.green_zone = Arc(start_angle=PI/3, angle=-PI/3, radius=radius, stroke_width=4, color=GREEN)
        
        self.ticks = VGroup()
        for val in [0.0, 0.25, 0.5, 0.75, 1.0]:
            angle = PI - val * PI
            tick = Line(
                start=ORIGIN,
                end=UP * 0.08,
                color=GRAY_A,
                stroke_width=1.2
            )
            tick.shift(UP * (radius - 0.08))
            tick.rotate(angle - PI/2, about_point=ORIGIN)
            self.ticks.add(tick)

        self.center_dot = Dot(point=ORIGIN, radius=0.05, color=WHITE)
        
        self.needle = Line(
            start=ORIGIN, 
            end=LEFT * (radius - 0.08), 
            color=WHITE, 
            stroke_width=2.2
        )
        
        self.title_lbl = create_text(title, font_size=8, color=BLUE_B)
        self.title_lbl.next_to(self.center_dot, DOWN, buff=0.1)
        
        self.add(self.arc, self.red_zone, self.yellow_zone, self.green_zone, self.ticks, self.center_dot, self.needle, self.title_lbl)


class Scene3_2(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def replace_content(self, old_group, new_group, run_time=0.55):
        if old_group is None:
            self.play(FadeIn(new_group, shift=UP * 0.12), run_time=run_time)
        else:
            self.play(FadeOut(old_group, shift=DOWN * 0.08), FadeIn(new_group, shift=UP * 0.08), run_time=run_time)
            self.remove(*old_group.get_family())
        return new_group

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (filename, duration) in enumerate(SCENE_3_2_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        # --- Chapter Title (Cue 1) ---
        chapter_title = create_text("Chapter 3: High-Level Orchestrators", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 3.2: Parallel Generation Algorithms\n(Best-of-N, Voting, Weighted Voting)", font_size=16, color=GRAY_A, line_spacing=1.3)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub).move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)
        self.wait(3.0)

        sub_title = create_text("Parallel generation algorithms (Best-of-N, Voting, MBR)", font_size=16, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=1.0)
        
        content = None

        # --- Cue 2: Best-of-N Intro ---
        self.wait_until(cue_start[2] + 0.25)
        part1_title = create_text("1. Best-of-N: generate, score, select", font_size=13, color=BLUE_A)
        part1_title.next_to(sub_title, DOWN, buff=0.3)

        bon_panel = create_asset_panel(
            "parallel_best_of_n_diagram.png",
            "Parallel candidates flow through a reward model",
            max_width=8.4,
            max_height=2.2,
        ).move_to(UP * 0.12)

        candidate_cards = VGroup()
        card_specs = [
            ("y1", "0.1", RED),
            ("y2", "1.0", GREEN),
            ("y3", "0.7", YELLOW),
        ]
        for idx, (name, score, color) in enumerate(card_specs):
            card = RoundedRectangle(
                width=1.05,
                height=0.54,
                color=color,
                fill_color="#151719",
                fill_opacity=0.92,
                corner_radius=0.06,
            )
            card.move_to(LEFT * 2.3 + RIGHT * idx * 1.2 + DOWN * 2.25)
            name_lbl = create_text(name, font_size=8, color=WHITE).move_to(card.get_center() + UP * 0.10)
            score_lbl = create_text(score, font_size=8, color=color).move_to(card.get_center() + DOWN * 0.12)
            candidate_cards.add(VGroup(card, name_lbl, score_lbl))
        winner_ring = SurroundingRectangle(candidate_cards[1], color=GREEN, stroke_width=2.5, buff=0.06)
        winner_lbl = create_text("select max v(y)", font_size=9, color=GREEN).next_to(winner_ring, DOWN, buff=0.10)

        part1_group = VGroup(part1_title)
        content = self.replace_content(content, Group(bon_panel, candidate_cards))
        self.play(Create(winner_ring), FadeIn(winner_lbl), run_time=0.55)

        # --- Cue 3: Best-of-N Formula ---
        self.wait_until(cue_start[3] + 0.2)
        bon_formula = create_markup_text(
            "Best-of-N = argmax<sub>y in candidates</sub> v(y)",
            font_size=12,
            color=YELLOW,
        )
        bon_formula.next_to(bon_panel, DOWN, buff=0.48)
        quality_axis = NumberLine(
            x_range=[0, 1, 0.25],
            length=5.2,
            color=GRAY_B,
            include_numbers=False,
        ).move_to(DOWN * 1.35)
        low_lbl = create_text("low score", font_size=7, color=GRAY_B).next_to(quality_axis, LEFT, buff=0.12)
        high_lbl = create_text("high score", font_size=7, color=GREEN).next_to(quality_axis, RIGHT, buff=0.12)
        score_dots = VGroup(
            Dot(quality_axis.n2p(0.1), radius=0.05, color=RED),
            Dot(quality_axis.n2p(0.7), radius=0.05, color=YELLOW),
            Dot(quality_axis.n2p(1.0), radius=0.06, color=GREEN),
        )
        score_runner = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=0.9).scale(0.09)
        score_runner.next_to(quality_axis.n2p(0.1), UP, buff=0.08)
        formula_group = VGroup(bon_formula, quality_axis, low_lbl, high_lbl, score_dots, score_runner)
        self.play(
            FadeOut(candidate_cards),
            FadeOut(winner_ring),
            FadeOut(winner_lbl),
            FadeIn(formula_group),
            run_time=0.6,
        )
        self.play(score_runner.animate.next_to(quality_axis.n2p(1.0), UP, buff=0.08), run_time=0.8)
        content = Group(bon_panel, formula_group)

        # --- Cue 4: RM Training Data ---
        self.wait_until(cue_start[4] + 0.2)
        binary_panel = create_asset_panel(
            "reward_model_binary_examples.png",
            "Correct / incorrect examples teach a score",
            max_width=4.4,
            max_height=1.55,
        )
        preference_panel = create_asset_panel(
            "reward_model_preference_examples.png",
            "Preference pairs teach a ranking",
            max_width=4.4,
            max_height=1.55,
        )
        training_panels = Group(binary_panel, preference_panel).arrange(RIGHT, buff=0.45).move_to(UP * 0.2)
        rm_core = RoundedRectangle(width=2.0, height=0.7, color=BLUE_A, fill_color="#141c2b", fill_opacity=0.95, corner_radius=0.08)
        rm_core.move_to(DOWN * 1.65)
        rm_lbl = create_text("Reward model v(y)", font_size=11, color=BLUE_A).move_to(rm_core.get_center())
        train_arrows = VGroup(
            Arrow(binary_panel.get_bottom(), rm_core.get_top() + LEFT * 0.45, color=BLUE_A, stroke_width=1.5, buff=0.08),
            Arrow(preference_panel.get_bottom(), rm_core.get_top() + RIGHT * 0.45, color=BLUE_A, stroke_width=1.5, buff=0.08),
        )
        rm_train_group = Group(training_panels, rm_core, rm_lbl, train_arrows)
        content = self.replace_content(content, rm_train_group)

        # --- Cue 5: Best-of-N Limit/Over-opt Intro ---
        self.wait_until(cue_start[5] + 0.2)
        overopt_panel = create_asset_panel(
            "overoptimization_graph.png",
            "More search can overfit an imperfect reward model",
            max_width=4.2,
            max_height=2.55,
        )
        overopt_panel.move_to(RIGHT * 2.65 + DOWN * 0.15)
        trap_box = RoundedRectangle(width=4.0, height=2.55, color=RED, fill_color="#261313", fill_opacity=0.78, corner_radius=0.08)
        trap_box.move_to(LEFT * 2.7 + DOWN * 0.1)
        trap_title = create_text("Best-looking to v(y)", font_size=11, color=RED).move_to(trap_box.get_top() + DOWN * 0.35)
        true_quality = create_text("true quality", font_size=9, color=GREEN).move_to(trap_box.get_center() + LEFT * 0.95 + UP * 0.25)
        rm_score = create_text("reward score", font_size=9, color=BLUE_A).move_to(trap_box.get_center() + RIGHT * 0.95 + UP * 0.25)
        mismatch_arrow = Arrow(true_quality.get_right(), rm_score.get_left(), color=RED, stroke_width=2.0, buff=0.12)
        blind_spot = create_text("blind spot", font_size=10, color=RED).move_to(trap_box.get_center() + DOWN * 0.65)
        overopt_group = Group(overopt_panel, trap_box, trap_title, true_quality, rm_score, mismatch_arrow, blind_spot)
        content = self.replace_content(content, overopt_group)
        self.play(Indicate(blind_spot, color=RED), run_time=0.8)

        # --- Cue 6: Voting Intro ---
        self.wait_until(cue_start[6] + 0.2)
        self.play(FadeOut(part1_group), run_time=0.25)

        part2_title = create_text("2. Voting: aggregate answers, not only scores", font_size=13, color=BLUE_A)
        part2_title.next_to(sub_title, DOWN, buff=0.3)
        part2_group = VGroup(part2_title)

        voting_panel = create_asset_panel(
            "voting_self_consistency_diagram.png",
            "Many reasoning paths collapse into answer groups",
            max_width=8.4,
            max_height=2.15,
        ).move_to(UP * 0.22)
        vote_bins = VGroup()
        for label, color, x_pos in [("Answer 2", GREEN, -1.4), ("Answer 4", RED, 1.4)]:
            box = RoundedRectangle(width=1.9, height=0.72, color=color, fill_color="#151719", fill_opacity=0.95, corner_radius=0.06)
            box.move_to(RIGHT * x_pos + DOWN * 1.7)
            lbl = create_text(label, font_size=9, color=color).move_to(box.get_center())
            vote_bins.add(VGroup(box, lbl))
        vote_tokens = VGroup(*[
            Dot(LEFT * 3.5 + RIGHT * idx * 0.35 + DOWN * 1.7, radius=0.06, color=GREEN if idx < 3 else RED)
            for idx in range(4)
        ])
        voting_group = Group(part2_group, voting_panel, vote_bins, vote_tokens)
        content = self.replace_content(content, voting_group)
        self.play(
            vote_tokens[0].animate.move_to(vote_bins[0].get_center() + LEFT * 0.35),
            vote_tokens[1].animate.move_to(vote_bins[0].get_center()),
            vote_tokens[2].animate.move_to(vote_bins[0].get_center() + RIGHT * 0.35),
            vote_tokens[3].animate.move_to(vote_bins[1].get_center()),
            run_time=0.9,
        )

        # --- Cue 7: Weighted Voting highlight ---
        self.wait_until(cue_start[7] + 0.15)
        weighted_panel = create_asset_panel(
            "weighted_voting_diagram.png",
            "Weighted voting lets verifier scores change the vote mass",
            max_width=8.4,
            max_height=2.2,
        ).move_to(UP * 0.2)
        weight_bars = VGroup()
        weights = [(0.8, GREEN), (0.1, RED), (0.2, RED), (0.9, GREEN)]
        for idx, (weight, color) in enumerate(weights):
            bg = RoundedRectangle(width=1.15, height=0.14, color=GRAY_D, fill_color=GRAY_E, fill_opacity=0.7, corner_radius=0.03)
            bg.move_to(LEFT * 2.0 + RIGHT * idx * 1.35 + DOWN * 1.72)
            fg = RoundedRectangle(width=1.15 * weight, height=0.14, color=color, fill_color=color, fill_opacity=0.95, corner_radius=0.03)
            fg.align_to(bg, LEFT).move_to(bg.get_center() + LEFT * (1.15 * (1 - weight) / 2))
            lbl = create_text(f"{weight:.1f}", font_size=7, color=color).next_to(bg, UP, buff=0.06)
            weight_bars.add(VGroup(bg, fg, lbl))
        weighted_group = Group(part2_group, weighted_panel, weight_bars)
        content = self.replace_content(content, weighted_group)
        self.play(LaggedStart(*[GrowFromEdge(bar[1], LEFT) for bar in weight_bars], lag_ratio=0.12), run_time=0.8)

        # --- Cue 8: Easy-to-Hard Generalization ---
        self.wait_until(cue_start[8] + 0.25)
        easy_graph = create_asset_panel(
            "voting_vs_weighted_graph.png",
            "Voting and weighted voting can beat Best-of-N",
            max_width=5.0,
            max_height=2.85,
        )
        easy_graph.move_to(RIGHT * 2.55 + DOWN * 0.02)
        easy_ladder = VGroup()
        ladder_labels = [("easy", GREEN), ("medium", YELLOW), ("hard", RED)]
        for idx, (label, color) in enumerate(ladder_labels):
            step = RoundedRectangle(width=1.45, height=0.46, color=color, fill_color="#151719", fill_opacity=0.95, corner_radius=0.05)
            step.move_to(LEFT * 3.75 + RIGHT * idx * 0.82 + DOWN * (1.25 - idx * 0.55))
            txt = create_text(label, font_size=8, color=color).move_to(step.get_center())
            easy_ladder.add(VGroup(step, txt))
        ladder_arrow = Arrow(easy_ladder[0].get_right(), easy_ladder[-1].get_left(), color=ORANGE, stroke_width=2, buff=0.06)
        verifier_badge = RoundedRectangle(width=2.2, height=0.62, color=ORANGE, fill_color="#2b1a14", fill_opacity=0.9, corner_radius=0.06)
        verifier_badge.move_to(LEFT * 3.15 + UP * 1.0)
        verifier_lbl = create_text("trained verifier transfers", font_size=8, color=ORANGE).move_to(verifier_badge.get_center())
        easy_hard_group = Group(easy_graph, easy_ladder, ladder_arrow, verifier_badge, verifier_lbl)
        content = self.replace_content(content, easy_hard_group)
        self.play(LaggedStart(*[FadeIn(step, shift=UP * 0.12) for step in easy_ladder], lag_ratio=0.15), Create(ladder_arrow), run_time=0.9)

        # --- Cue 9: Convergence Theorem ---
        self.wait_until(cue_start[9] + 0.2)
        conv_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.05, 0.25],
            x_length=6.1,
            y_length=2.6,
            axis_config={"color": GRAY_B, "stroke_width": 1.4},
        ).move_to(LEFT * 1.2)
        conv_curve = conv_axes.plot(lambda x: 0.84 * (1 - np.exp(-0.48 * x)), x_range=[0, 9.5], color=GREEN, stroke_width=3)
        ceiling = DashedLine(conv_axes.c2p(0, 0.84), conv_axes.c2p(9.5, 0.84), color=YELLOW, stroke_width=1.5)
        ceiling_lbl = create_text("limit as N grows", font_size=8, color=YELLOW).move_to(conv_axes.c2p(7.0, 0.93))
        samples_lbl = create_text("number of candidates N", font_size=8, color=GRAY_A).next_to(conv_axes.x_axis, DOWN, buff=0.18)
        acc_lbl = create_text("voting accuracy", font_size=8, color=GRAY_A).next_to(conv_axes.y_axis, LEFT, buff=0.15).rotate(90 * DEGREES)
        marginalize_card = RoundedRectangle(width=3.15, height=1.2, color=BLUE_A, fill_color="#141c2b", fill_opacity=0.92, corner_radius=0.08)
        marginalize_card.move_to(RIGHT * 3.35 + UP * 0.25)
        marginalize_txt = create_markup_text(
            "sum over paths z\n"
            "<span foreground='#8fd3ff'>g(z,a|x)</span> × <span foreground='#89ff89'>v(x,z,a)</span>",
            font_size=9,
            color=WHITE,
            line_spacing=1.25,
        ).move_to(marginalize_card.get_center())
        convergence_group = VGroup(conv_axes, conv_curve, ceiling, ceiling_lbl, samples_lbl, acc_lbl, marginalize_card, marginalize_txt)
        content = self.replace_content(content, convergence_group)
        self.play(Create(conv_curve), Create(ceiling), run_time=1.0)

        # --- Cue 10: Convergence takeaways intro ---
        self.wait_until(cue_start[10] + 0.15)
        self.play(Indicate(ceiling_lbl, color=YELLOW), run_time=0.55)

        # --- Cue 11: Takeaway 1 ---
        self.wait_until(cue_start[11] + 0.15)
        takeaway1 = create_text("More samples help, then plateau.", font_size=10, color=WHITE)
        takeaway1.next_to(samples_lbl, DOWN, buff=0.16)
        self.play(FadeIn(takeaway1, shift=UP * 0.1), run_time=0.4)

        # --- Cue 12: Takeaway 2 ---
        self.wait_until(cue_start[12] + 0.15)
        weighted_mass = RoundedRectangle(width=2.8, height=0.42, color=GREEN, fill_color=GREEN_E, fill_opacity=0.22, corner_radius=0.06)
        weighted_mass.next_to(marginalize_card, DOWN, buff=0.24)
        weighted_mass_lbl = create_text("correct answers get more v · g mass", font_size=7.5, color=GREEN).move_to(weighted_mass.get_center())
        self.play(FadeIn(weighted_mass), Write(weighted_mass_lbl), run_time=0.45)

        # --- Cue 13: Takeaway 3 ---
        self.wait_until(cue_start[13] + 0.15)
        improve_v = create_text("improve v", font_size=8, color=BLUE_A).move_to(RIGHT * 2.75 + DOWN * 1.45)
        improve_g = create_text("improve g", font_size=8, color=GREEN).move_to(RIGHT * 3.95 + DOWN * 1.45)
        improve_arrows = VGroup(
            Arrow(improve_v.get_top(), marginalize_card.get_bottom() + LEFT * 0.35, color=BLUE_A, stroke_width=1.6, buff=0.05),
            Arrow(improve_g.get_top(), marginalize_card.get_bottom() + RIGHT * 0.35, color=GREEN, stroke_width=1.6, buff=0.05),
        )
        self.play(FadeIn(improve_v), FadeIn(improve_g), Create(improve_arrows), run_time=0.55)
        content = Group(convergence_group, takeaway1, weighted_mass, weighted_mass_lbl, improve_v, improve_g, improve_arrows)

        # --- Cue 14-17: Limitations of Parallel Meta-Generation ---
        self.wait_until(cue_start[14] + 0.25)
        self.play(FadeOut(part2_group), run_time=0.4)
        
        lim_title = create_text("Limitations of Parallel Meta-Generation (Slide 124-125)", font_size=13, color=YELLOW)
        lim_title.next_to(sub_title, DOWN, buff=0.3)
        
        lim_box = RoundedRectangle(width=9.2, height=2.6, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1)
        lim_box.move_to(DOWN * 0.4)
        
        lim_line1 = create_markup_text("• Parallel generators explore output space by generating <b>full sequences</b>.", font_size=10.5, color=GRAY_A)
        lim_line2 = create_markup_text("• Brings large performance gains in practice, but is <b>bounded by evaluator/generator quality</b>.", font_size=10.5, color=GRAY_A)
        lim_line3 = create_markup_text("• Crucial insight: The verifier/reward model is used <b>only at the end</b> on completed sequences.", font_size=10.5, color=GRAY_A)
        lim_line4 = create_markup_text("• Next step: Can we use <b>intermediate evaluations step-by-step</b> more effectively?", font_size=10.5, color=GRAY_A)
        
        lim_list = VGroup(lim_line1, lim_line2, lim_line3, lim_line4).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(lim_box.get_center())
        lim_group = VGroup(lim_title, lim_box, lim_list)
        
        content = self.replace_content(content, lim_group)
        
        self.play(lim_line1.animate.set_color(WHITE), run_time=0.4)
        
        self.wait_until(cue_start[15] + 0.15)
        self.play(lim_line2.animate.set_color(WHITE), run_time=0.4)
        
        self.wait_until(cue_start[16] + 0.15)
        self.play(lim_line3.animate.set_color(WHITE), run_time=0.4)
        
        self.wait_until(cue_start[17] + 0.15)
        self.play(lim_line4.animate.set_color(WHITE), run_time=0.4)

        # --- Cue 18: Deep Dive Title ---
        self.wait_until(cue_start[18] + 0.2)
        
        dive_title = create_text("Reward Model & Over-Optimization Deep Dive", font_size=13, color=YELLOW)
        dive_title.next_to(sub_title, DOWN, buff=0.3)
        
        dive_intro = create_markup_text(
            "<b>Reward Model:</b> The bridge between probability and acceptability.\n"
            "Maps sequence candidate <i>y</i> to score <i>v(y) ∈ [0, 1]</i>.",
            font_size=12, color=WHITE, line_spacing=1.3
        ).move_to(DOWN * 0.4)
        
        dive_group = VGroup(dive_title, dive_intro)
        content = self.replace_content(content, dive_group)

        # --- Cue 19: Candidate Generation ---
        self.wait_until(cue_start[19] + 0.2)
        
        prompt_box = RoundedRectangle(width=2.2, height=1.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        prompt_box.move_to(LEFT * 5.0 + DOWN * 0.4)
        prompt_lbl = create_text("Prompt x", font_size=12, color=GREEN).move_to(prompt_box.get_center())
        prompt_group = VGroup(prompt_box, prompt_lbl)
        
        y_y_coords = [1.3, 0.5, -0.3, -1.1, -1.9]
        y_boxes = VGroup()
        y_texts = VGroup()
        y_arrows = VGroup()
        y_texts_str = [
            'y(1): "The result is 42"',
            'y(2): "17 + 25 = 42"',
            'y(3): "John has 42 items"',
            'y(4): "17 + 25 = 32"',
            'y(5): "Answer y(5)"'
        ]
        
        for idx, y_val in enumerate(y_y_coords):
            box = RoundedRectangle(width=2.8, height=0.6, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.06)
            box.move_to(LEFT * 1.0 + UP * y_val)
            lbl = create_text(y_texts_str[idx], font_size=9, color=WHITE).move_to(box.get_center())
            arrow = Arrow(start=prompt_box.get_right(), end=box.get_left(), color=GRAY_D, stroke_width=1.5, buff=0.08)
            
            y_boxes.add(box)
            y_texts.add(lbl)
            y_arrows.add(arrow)
            
        candidates_group = VGroup(prompt_group, y_boxes, y_texts, y_arrows)
        content = self.replace_content(content, candidates_group)

        # --- Cue 20: Speedometer Scoring ---
        self.wait_until(cue_start[20] + 0.2)
        
        rm_box = RoundedRectangle(width=2.4, height=2.2, color=BLUE_A, fill_color="#141c2b", fill_opacity=0.9, corner_radius=0.08)
        rm_box.move_to(RIGHT * 4.6 + DOWN * 0.4)
        
        speedometer = Speedometer(radius=0.7, title="Reward Model (Scoring)")
        speedometer.move_to(rm_box.get_center() + UP * 0.25)
        
        digital_score_lbl = create_text("Score: 0.00", font_size=10, color=GRAY_A)
        digital_score_lbl.next_to(speedometer.center_dot, DOWN, buff=0.45)
        
        rm_display_group = VGroup(rm_box, speedometer, digital_score_lbl)
        self.play(FadeIn(rm_display_group), run_time=0.8)
        
        score_colors = [RED, GREEN, YELLOW, GREEN_B, GREEN]
        score_values = [0.15, 0.88, 0.45, 0.62, 0.99]
        score_labels = VGroup()
        rm_flow_arrows = VGroup()

        for idx, y_val in enumerate(y_y_coords):
            flow_arrow = Line(start=y_boxes[idx].get_right(), end=rm_box.get_left() + UP * y_val * 0.25, color=BLUE_A, stroke_width=1.2)
            rm_flow_arrows.add(flow_arrow)

            lbl = create_text(f"Score: {score_values[idx]:.2f}", font_size=10, color=score_colors[idx])
            lbl.next_to(y_boxes[idx], RIGHT, buff=0.15)
            
            mask = SurroundingRectangle(lbl, color="#111111", fill_color="#111111", fill_opacity=1.0, stroke_width=0, buff=0.04)
            label_group = VGroup(mask, lbl)
            score_labels.add(label_group)
            
        for idx in range(5):
            target_score = score_values[idx]
            delta_angle = - (target_score - speedometer.current_score) * PI
            speedometer.current_score = target_score
            
            new_digital_lbl = create_text(f"Score: {target_score:.2f}", font_size=10, color=score_colors[idx])
            new_digital_lbl.next_to(speedometer.center_dot, DOWN, buff=0.45)

            self.play(
                Create(rm_flow_arrows[idx]),
                Rotate(speedometer.needle, angle=delta_angle, about_point=speedometer.center_dot.get_center()),
                Transform(digital_score_lbl, new_digital_lbl),
                FadeIn(score_labels[idx]),
                run_time=0.45
            )
            self.wait(0.2)
            
        selection_box = RoundedRectangle(width=2.9, height=0.7, color=GREEN, stroke_width=2.5, fill_opacity=0.0, corner_radius=0.08).move_to(y_boxes[1].get_center())
        self.play(Create(selection_box), run_time=0.5)
        self.wait(1.5)

        # --- Cue 21: Reward Hacking & Over-Optimization ---
        self.wait_until(cue_start[21] + 0.2)
        
        y5_hacking_text = create_text('"...the the the the the..."', font_size=8, color=RED)
        y5_hacking_text.move_to(y_boxes[4].get_center())
        
        hacking_warn_box = RoundedRectangle(width=3.2, height=0.8, color=RED, fill_color=RED_E, fill_opacity=0.3, corner_radius=0.08)
        hacking_warn_box.next_to(y_boxes[4], DOWN, buff=0.4)
        hacking_warn_lbl = create_text("Reward Hacking\n(Reward-model exploit)", font_size=10, color=RED).move_to(hacking_warn_box.get_center())
        arrow_to_hacking = Arrow(start=hacking_warn_box.get_top(), end=y_boxes[4].get_bottom(), color=RED, stroke_width=1.5, buff=0.05)

        warning_icon = VGroup()
        triangle = Polygon(UP * 0.15, DOWN * 0.1 + LEFT * 0.15, DOWN * 0.1 + RIGHT * 0.15, color=RED, fill_color=RED, fill_opacity=0.9, stroke_width=1)
        excl = create_text("!", font_size=8, color=WHITE).move_to(triangle.get_center() + DOWN * 0.01)
        warning_icon.add(triangle, excl)
        warning_icon.next_to(digital_score_lbl, RIGHT, buff=0.1)
        
        self.play(
            ReplacementTransform(y_texts[4], y5_hacking_text),
            y_boxes[4].animate.set_stroke(color=RED).set_fill(color="#551a1a", opacity=0.9),
            Rotate(speedometer.needle, angle=- (0.99 - speedometer.current_score) * PI, about_point=speedometer.center_dot.get_center()),
            Transform(digital_score_lbl, create_text("Score: 0.99 !!!", font_size=10, color=RED).next_to(speedometer.center_dot, DOWN, buff=0.45)),
            FadeIn(warning_icon),
            FadeIn(hacking_warn_box),
            Write(hacking_warn_lbl),
            Create(arrow_to_hacking),
            run_time=1.0
        )
        self.wait(2.5)
        
        overopt_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.2, 0.2],
            x_length=6.0,
            y_length=3.0,
            axis_config={"color": GRAY, "stroke_width": 1.5}
        ).move_to(DOWN * 0.5)
        
        overopt_x_label = create_text("Inference Compute N", font_size=8, color=GRAY_A).next_to(overopt_axes.x_axis, DOWN, buff=0.25, aligned_edge=RIGHT)
        overopt_y_label = create_text("Score / Acceptability", font_size=8, color=GRAY_A).next_to(overopt_axes.y_axis, LEFT, buff=0.2).rotate(90 * DEGREES)
        
        rm_curve = overopt_axes.plot(lambda x: 1.0 - np.exp(-0.4 * x), x_range=[0.1, 9.5], color=BLUE, stroke_width=2.5)
        rm_lbl = create_text("Reward Model Score", font_size=8, color=BLUE).next_to(rm_curve.get_end(), UR, buff=0.1)
        
        acc_curve = overopt_axes.plot(lambda x: 1.25 * x * np.exp(-0.35 * x), x_range=[0.1, 9.5], color=GREEN, stroke_width=2.5)
        acc_lbl = create_text("True Acceptability", font_size=8, color=GREEN).next_to(overopt_axes.c2p(2.8, 1.25*2.8*np.exp(-0.35*2.8)), UP, buff=0.1)
        
        overopt_region = DashedLine(overopt_axes.c2p(3.0, 0), overopt_axes.c2p(3.0, 1.0), color=RED, stroke_width=1.5)
        overopt_region_lbl = create_markup_text(
            "<span color='#FF5555'>Over-optimization\n(Reward Hacking)</span>", 
            font_size=7, color=RED
        ).next_to(overopt_region, RIGHT, buff=0.15).shift(UP * 0.5)
        
        overopt_group = VGroup(overopt_axes, overopt_x_label, overopt_y_label, rm_curve, rm_lbl, acc_curve, acc_lbl, overopt_region, overopt_region_lbl)
        
        self.play(
            FadeOut(candidates_group), FadeOut(selection_box),
            FadeOut(rm_display_group), FadeOut(rm_flow_arrows), FadeOut(score_labels),
            FadeOut(y5_hacking_text), FadeOut(hacking_warn_box), FadeOut(hacking_warn_lbl), FadeOut(arrow_to_hacking), FadeOut(warning_icon),
            FadeIn(overopt_group),
            run_time=1.0
        )
        self.wait(3.5)

        # --- Cue 22: Voting Deep Dive & Math Question ---
        self.wait_until(cue_start[22] + 0.2)
        
        self.play(FadeOut(overopt_group), run_time=0.4)
        
        dive_title_2 = create_text("Voting & Self-Consistency Deep Dive", font_size=13, color=YELLOW)
        dive_title_2.next_to(sub_title, DOWN, buff=0.3)
        self.play(Transform(dive_title, dive_title_2), run_time=0.5)
        
        math_question_box = RoundedRectangle(width=9.0, height=0.6, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.05)
        math_question_box.move_to(UP * 0.9)
        math_question_lbl = create_markup_text("<b>Math question:</b> <i>\"John has 17 apples. John buys 25 more apples. How many apples does John have?\"</i>", font_size=11, color=YELLOW)
        math_question_lbl.move_to(math_question_box.get_center())
        
        math_q_group = VGroup(math_question_box, math_question_lbl)
        self.play(FadeIn(math_q_group), run_time=0.8)
        self.wait(3.0)

        # --- Cue 23: Intermediate Reasoning Paths ---
        self.wait_until(cue_start[23] + 0.25)
        
        cot_y_coords = [0.1, -0.6, -1.3, -2.0]
        cot_boxes = VGroup()
        cot_texts = VGroup()
        cot_data = [
            ("Reasoning z1: 17 + 20 = 37, 37 + 5 = 42", "y = 42", "#87FF87"),
            ("Reasoning z2: 17 + 5 = 22, 22 + 20 = 42", "y = 42", "#87FF87"),
            ("Reasoning z3: 10 + 20 = 30, 7 + 5 = 12 -> 42", "y = 42", "#87FF87"),
            ("Reasoning z4: 17 + 25 = 17 + 20 + 5 = 32", "y = 32 (Wrong)", "#FF8787")
        ]

        voters = VGroup()
        for idx in range(4):
            v = get_voter_icon(color=[BLUE_B, BLUE_C, BLUE_D, RED_C][idx])
            v.move_to(LEFT * 4.1 + UP * cot_y_coords[idx])
            voters.add(v)

        for idx, (z_str, y_str, col_str) in enumerate(cot_data):
            box = RoundedRectangle(width=7.4, height=0.5, color=GRAY_D, fill_color="#141517", fill_opacity=0.9, corner_radius=0.05)
            box.move_to(RIGHT * 0.2 + UP * cot_y_coords[idx])
            
            text_str = f"{z_str}  →  <span foreground='{col_str}'><b>{y_str}</b></span>"
            lbl = create_markup_text(text_str, font_size=10, color=WHITE).move_to(box.get_center())
            
            cot_boxes.add(box)
            cot_texts.add(lbl)
            
        cot_group = VGroup(voters, cot_boxes, cot_texts)
        self.play(FadeIn(cot_group), run_time=1.0)
        self.wait(1.5)

        # --- Cue 24: Vote Aggregation & Self-Consistency ---
        self.wait_until(cue_start[24] + 0.2)
        
        voter_dest_coords = [LEFT * 3.0, LEFT * 1.0, RIGHT * 1.0, RIGHT * 3.0]
        voter_ans_lbls = VGroup()
        voter_sub_boxes = VGroup()
        for idx in range(4):
            ans_text = "y = 42" if idx < 3 else "y = 32"
            ans_color = GREEN if idx < 3 else RED
            lbl = create_text(ans_text, font_size=10, color=ans_color)
            lbl.move_to(voter_dest_coords[idx] + UP * 0.20)
            voter_ans_lbls.add(lbl)
            
            box = RoundedRectangle(width=1.6, height=1.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.8, corner_radius=0.06)
            box.move_to(voter_dest_coords[idx] + UP * 0.45)
            voter_sub_boxes.add(box)
            
        self.play(
            FadeOut(math_q_group),
            FadeOut(cot_boxes), FadeOut(cot_texts),
            voters[0].animate.move_to(voter_dest_coords[0] + UP * 0.65),
            voters[1].animate.move_to(voter_dest_coords[1] + UP * 0.65),
            voters[2].animate.move_to(voter_dest_coords[2] + UP * 0.65),
            voters[3].animate.move_to(voter_dest_coords[3] + UP * 0.65),
            FadeIn(voter_sub_boxes),
            FadeIn(voter_ans_lbls),
            run_time=1.0
        )
        
        bin_42 = RoundedRectangle(width=3.6, height=1.6, color=GREEN, fill_color=GREEN_E, fill_opacity=0.1, corner_radius=0.08)
        bin_42.move_to(LEFT * 2.0 + DOWN * 1.4)
        bin_42_lbl = create_text("Group y = 42", font_size=11, color=GREEN).next_to(bin_42.get_top(), DOWN, buff=0.15)
        
        bin_32 = RoundedRectangle(width=3.6, height=1.6, color=RED, fill_color=RED_E, fill_opacity=0.1, corner_radius=0.08)
        bin_32.move_to(RIGHT * 2.0 + DOWN * 1.4)
        bin_32_lbl = create_text("Group y = 32", font_size=11, color=RED).next_to(bin_32.get_top(), DOWN, buff=0.15)

        self.play(
            FadeIn(bin_42), Write(bin_42_lbl),
            FadeIn(bin_32), Write(bin_32_lbl),
            run_time=0.8
        )
        
        ballots = VGroup()
        ballot_targets = [
            bin_42.get_center() + DOWN * 0.3 + LEFT * 0.8,
            bin_42.get_center() + DOWN * 0.3 + ORIGIN,
            bin_42.get_center() + DOWN * 0.3 + RIGHT * 0.8,
            bin_32.get_center() + DOWN * 0.3
        ]
        for idx in range(4):
            color = GREEN if idx < 3 else RED
            card = RoundedRectangle(width=0.5, height=0.4, color=color, fill_color=color, fill_opacity=0.8, corner_radius=0.04)
            card.move_to(voters[idx].get_center())
            card_lbl = create_text("+1", font_size=8, color=WHITE).move_to(card.get_center())
            ballots.add(VGroup(card, card_lbl))

        count_42_lbl = create_text("0 votes", font_size=12, color=GREEN).next_to(bin_42, DOWN, buff=0.2)
        count_32_lbl = create_text("0 votes", font_size=12, color=RED).next_to(bin_32, DOWN, buff=0.2)
        self.play(FadeIn(count_42_lbl), FadeIn(count_32_lbl), run_time=0.5)

        for idx in range(4):
            target_pos = ballot_targets[idx]
            self.play(
                ballots[idx].animate.move_to(target_pos),
                run_time=0.4
            )
            if idx < 3:
                new_cnt_lbl = create_text(f"{idx+1} votes", font_size=12, color=GREEN).next_to(bin_42, DOWN, buff=0.2)
                self.play(Transform(count_42_lbl, new_cnt_lbl), run_time=0.15)
            else:
                new_cnt_lbl = create_text("1 votes", font_size=12, color=RED).next_to(bin_32, DOWN, buff=0.2)
                self.play(Transform(count_32_lbl, new_cnt_lbl), run_time=0.15)
            self.wait(0.1)

        winner_highlight = RoundedRectangle(width=3.9, height=2.8, color=GREEN, stroke_width=3.5, fill_opacity=0, corner_radius=0.1).move_to(
            LEFT * 2.0 + DOWN * 1.85
        )
        winner_tag = create_text("HIGH CONSENSUS - SELECT Y = 42", font_size=10, color=GREEN).next_to(count_42_lbl, DOWN, buff=0.2)
        self.play(Create(winner_highlight), Write(winner_tag), run_time=0.6)
        self.wait(1.5)

        # --- End of Scene Recap: Comparison Table ---
        self.wait_until(voiceover_end + 0.1)
        
        self.play(
            FadeOut(voters), FadeOut(voter_sub_boxes), FadeOut(voter_ans_lbls),
            FadeOut(bin_42), FadeOut(bin_42_lbl),
            FadeOut(bin_32), FadeOut(bin_32_lbl),
            FadeOut(ballots), FadeOut(count_42_lbl), FadeOut(count_32_lbl),
            FadeOut(winner_highlight), FadeOut(winner_tag),
            FadeOut(dive_title),
            run_time=0.8
        )
        
        recap_title = create_text("Summary: Pros and cons of parallel generation techniques", font_size=13, color=YELLOW)
        recap_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(recap_title), run_time=0.8)
        
        comparison_table = VGroup()
        headers = ["Technique", "Core principle", "Traps / limits"]
        header_colors = [BLUE_A, WHITE, RED]
        
        header_group = VGroup()
        for idx, h_text in enumerate(headers):
            cell = RoundedRectangle(width=3.2, height=0.6, color=GRAY_D, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            cell.move_to(LEFT * (3.4 * (1 - idx)) + UP * 1.0)
            lbl = create_text(h_text, font_size=11, color=header_colors[idx]).move_to(cell.get_center())
            header_group.add(VGroup(cell, lbl))
        comparison_table.add(header_group)

        table_rows = [
            ("1. Best-of-N", "Choose the highest-RM-scored answer", "Reward Hacking"),
            ("2. Majority Voting", "Majority vote over CoT chains", "Not applicable to free-form text"),
            ("3. MBR (Bayes)", "Pairwise cross-similarity comparison", "High N^2 compute cost")
        ]

        row_y_coords = [0.2, -0.6, -1.4]
        for r_idx, row_data in enumerate(table_rows):
            row_group = VGroup()
            for c_idx, cell_text in enumerate(row_data):
                cell = RoundedRectangle(width=3.2, height=0.6, color=GRAY_E, fill_color="#121315", fill_opacity=0.8, corner_radius=0.04)
                cell.move_to(LEFT * (3.4 * (1 - c_idx)) + UP * row_y_coords[r_idx])
                
                t_color = RED if c_idx == 2 else (GREEN if c_idx == 1 else WHITE)
                lbl = create_text(cell_text, font_size=9, color=t_color).move_to(cell.get_center())
                
                row_group.add(VGroup(cell, lbl))
            comparison_table.add(row_group)

        self.play(FadeIn(comparison_table), run_time=1.0)
        
        self.wait(15.0)
        
        self.play(
            FadeOut(comparison_table),
            FadeOut(recap_title),
            FadeOut(sub_title),
            run_time=0.8
        )
        self.wait(1.5)
        
        assert_all_scene_voiceovers_played(self)
