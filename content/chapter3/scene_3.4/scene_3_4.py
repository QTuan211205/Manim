import os
import tempfile
from pathlib import Path

from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_3_4_DURATIONS = {
    "sc34_001.mp3": 3.622313,
    "sc34_002.mp3": 3.065034,
    "sc34_003.mp3": 3.854512,
    "sc34_004.mp3": 5.990748,
    "sc34_005.mp3": 5.712109,
    "sc34_006.mp3": 7.291066,
    "sc34_007.mp3": 3.900952,
    "sc34_008.mp3": 4.597551,
    "sc34_009.mp3": 10.681179,
    "sc34_010.mp3": 4.643991,
    "sc34_011.mp3": 4.736871,
    "sc34_012.mp3": 10.681179,
    "sc34_013.mp3": 6.269388,
    "sc34_014.mp3": 14.442812,
    "sc34_015.mp3": 3.157914,
    "sc34_016.mp3": 7.616145,
    "sc34_017.mp3": 7.894785,
    "sc34_018.mp3": 12.027937,
    "sc34_019.mp3": 9.938141,
}
SCENE_3_4_VOICEOVERS = tuple(SCENE_3_4_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc34_*.mp3"))
    expected = sorted(SCENE_3_4_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 3.4 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_3_4_DURATIONS:
        raise KeyError(f"Unexpected Scene 3.4 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 3.4 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_3_4_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_3_4_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 3.4 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
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


def labeled_box(
    title,
    body=None,
    width=2.4,
    height=1.0,
    color=BLUE_B,
    fill="#15181d",
    title_size=11,
    body_size=8,
):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.07,
        color=color,
        fill_color=fill,
        fill_opacity=0.92,
        stroke_width=1.5,
    )
    title_obj = create_text(title, font_size=title_size, color=color)
    if body:
        body_obj = create_text(body, font_size=body_size, color=GRAY_A, line_spacing=1.05)
        group = VGroup(box, title_obj, body_obj)
        title_obj.move_to(box.get_center() + UP * height * 0.18)
        body_obj.move_to(box.get_center() + DOWN * height * 0.18)
    else:
        group = VGroup(box, title_obj)
        title_obj.move_to(box.get_center())
    return group


def feedback_loop(color=GREEN):
    draft = labeled_box("Draft", width=1.6, height=0.72, color=BLUE_A)
    feedback = labeled_box("Feedback", width=1.8, height=0.72, color=YELLOW)
    improved = labeled_box("Improved", width=1.8, height=0.72, color=GREEN)
    VGroup(draft, feedback, improved).arrange(RIGHT, buff=0.85).move_to(DOWN * 0.15)
    arrows = VGroup(
        Arrow(draft.get_right(), feedback.get_left(), color=color, stroke_width=1.5, buff=0.08),
        Arrow(feedback.get_right(), improved.get_left(), color=color, stroke_width=1.5, buff=0.08),
        CurvedArrow(improved.get_bottom(), draft.get_bottom(), angle=-TAU / 4, color=GRAY_C, stroke_width=1.2),
    )
    return VGroup(draft, feedback, improved, arrows)


def method_card(title, status, color, width=3.35):
    card = RoundedRectangle(
        width=width,
        height=1.15,
        corner_radius=0.08,
        color=color,
        fill_color="#14171b",
        fill_opacity=0.94,
        stroke_width=1.5,
    )
    title_obj = create_text(title, font_size=10, color=color).move_to(card.get_center() + UP * 0.22)
    status_obj = create_text(status, font_size=7.6, color=GRAY_A, line_spacing=1.05).move_to(
        card.get_center() + DOWN * 0.22
    )
    return VGroup(card, title_obj, status_obj)


def create_packet(label, color=GREEN):
    packet = RoundedRectangle(
        width=0.72,
        height=0.32,
        corner_radius=0.05,
        color=color,
        fill_color="#111a14",
        fill_opacity=0.95,
        stroke_width=1.2,
    )
    text = create_text(label, font_size=7, color=color).move_to(packet.get_center())
    return VGroup(packet, text)


def create_letter_row(chars, target=None):
    row = VGroup()
    for idx, char in enumerate(chars):
        color = RED_B if target and char != target[idx] else BLUE_B
        box = RoundedRectangle(
            width=0.58,
            height=0.62,
            corner_radius=0.05,
            color=color,
            fill_color="#15181d",
            fill_opacity=0.95,
            stroke_width=1.5,
        )
        label = create_text(char, font_size=13, color=WHITE).move_to(box.get_center())
        row.add(VGroup(box, label))
    row.arrange(RIGHT, buff=0.08)
    return row


def create_signal_meter(label, value, color):
    base = Line(LEFT * 1.3, RIGHT * 1.3, color=GRAY_D, stroke_width=7)
    fill = Line(LEFT * 1.3, LEFT * 1.3 + RIGHT * 2.6 * value, color=color, stroke_width=7)
    dot = Dot(fill.get_end(), radius=0.075, color=color)
    text = create_text(label, font_size=8, color=color).next_to(base, UP, buff=0.12)
    return VGroup(base, fill, dot, text)


def create_probability_bars(items):
    bars = VGroup()
    for label, prob, color in items:
        bar = Rectangle(width=0.34, height=1.6 * prob, color=color, fill_color=color, fill_opacity=0.82, stroke_width=1)
        base = Line(LEFT * 0.2, RIGHT * 0.2, color=GRAY_D, stroke_width=1)
        label_obj = create_text(label, font_size=9, color=WHITE).next_to(base, DOWN, buff=0.08)
        pct = create_text(f"{int(prob * 100)}", font_size=7, color=color).next_to(bar, UP, buff=0.08)
        group = VGroup(bar, base, label_obj, pct)
        bar.next_to(base, UP, buff=0)
        bars.add(group)
    bars.arrange(RIGHT, buff=0.25)
    return bars


def create_correction_graph():
    axes = Axes(
        x_range=[0, 6, 1],
        y_range=[0, 1, 0.25],
        x_length=5.1,
        y_length=2.15,
        tips=False,
        axis_config={"color": GRAY_C, "stroke_width": 1.4},
    )
    red_points = [axes.c2p(0, 0.35), axes.c2p(1.2, 0.52), axes.c2p(2.4, 0.35), axes.c2p(4.0, 0.12), axes.c2p(6, 0.06)]
    green_points = [axes.c2p(0, 0.35), axes.c2p(1.2, 0.47), axes.c2p(2.4, 0.58), axes.c2p(4.0, 0.68), axes.c2p(6, 0.75)]
    collapse_curve = VMobject(color=RED_B, stroke_width=3).set_points_smoothly(red_points)
    score_curve = VMobject(color=GREEN, stroke_width=3).set_points_smoothly(green_points)
    y_label = create_text("Correction quality", font_size=8, color=GRAY_A).next_to(axes.y_axis, LEFT, buff=0.12)
    x_label = create_text("Training loop", font_size=8, color=GRAY_A).next_to(axes.x_axis, DOWN, buff=0.12)
    red_label = create_text("Collapse", font_size=8, color=RED_B).move_to(axes.c2p(4.8, 0.18))
    green_label = create_text("SCoRe", font_size=8, color=GREEN).move_to(axes.c2p(4.8, 0.85))
    return VGroup(axes, collapse_curve, score_curve, y_label, x_label, red_label, green_label)


class Scene3_4(Scene):
    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def construct(self):
        self.camera.background_color = "#111111"
        voiceover_end = schedule_scene_voiceovers(self)

        cue_start = {}
        current = 0.0
        for idx, (_, duration) in enumerate(SCENE_3_4_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        chapter_title = create_text("Chapter 3: High-Level Orchestrators", font_size=24, color=YELLOW)
        chapter_sub = create_text("Part 3.4: Refinement & Self-Correction", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub).move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.0)
        self.wait_until(cue_start[2])

        sub_title = create_text("Refinement & Self-Correction", font_size=15, color=YELLOW)
        sub_title.to_edge(UP, buff=0.4)
        self.play(ReplacementTransform(chapter_header, sub_title), run_time=0.8)

        quality_bar = Line(LEFT * 2.4, RIGHT * 2.4, color=GRAY_D, stroke_width=6).move_to(UP * 1.15)
        quality_fill = Line(LEFT * 2.4, LEFT * 0.45, color=RED_B, stroke_width=6).move_to(UP * 1.15)
        quality_dot = Dot(LEFT * 0.45 + UP * 1.15, radius=0.09, color=RED_B)
        quality_label = create_text("Quality depends on feedback", font_size=10, color=GRAY_A).next_to(
            quality_bar, UP, buff=0.2
        )
        source_label = create_text("Source", font_size=9, color=YELLOW).move_to(LEFT * 1.65 + UP * 0.45)
        quality_word = create_text("Quality", font_size=9, color=YELLOW).move_to(RIGHT * 1.65 + UP * 0.45)
        overview_loop = feedback_loop()
        self.play(FadeIn(overview_loop), FadeIn(quality_label), Create(quality_bar), Create(quality_fill), FadeIn(quality_dot), run_time=1.0)
        self.wait_until(cue_start[3])
        self.play(FadeIn(source_label), FadeIn(quality_word), run_time=0.5)

        extrinsic_card = method_card("Extrinsic", "outside information\nat inference time", GREEN)
        intrinsic_card = method_card("Intrinsic", "feedback from\nthe model itself", RED_B)
        VGroup(extrinsic_card, intrinsic_card).arrange(RIGHT, buff=0.6).move_to(DOWN * 1.55)
        self.play(FadeIn(extrinsic_card, shift=UP * 0.15), FadeIn(intrinsic_card, shift=UP * 0.15), run_time=0.8)

        self.wait_until(cue_start[4])
        self.play(
            FadeOut(overview_loop),
            FadeOut(quality_label),
            FadeOut(quality_bar),
            FadeOut(quality_fill),
            FadeOut(quality_dot),
            FadeOut(source_label),
            FadeOut(quality_word),
            FadeOut(extrinsic_card),
            FadeOut(intrinsic_card),
            run_time=0.6,
        )

        ext_title = create_text("1. Extrinsic Feedback", font_size=13, color=GREEN)
        ext_title.next_to(sub_title, DOWN, buff=0.3)
        draft_chars = create_letter_row(list("TAYLORSWIPT"), list("TAYLORSWIFT")).move_to(LEFT * 2.65 + UP * 0.35)
        draft_label = create_text("Draft output", font_size=9, color=BLUE_A).next_to(draft_chars, UP, buff=0.2)
        verifier = labeled_box("External\nverifier", "program / tool\nruns outside model", width=2.35, height=1.2, color=GREEN)
        verifier.move_to(RIGHT * 2.2 + UP * 0.32)
        draft_to_verifier = Arrow(draft_chars.get_right(), verifier.get_left(), color=GRAY_B, stroke_width=1.5, buff=0.12)
        outside_badge = create_text("Outside information", font_size=10, color=GREEN).move_to(UP * 1.7)
        self.play(
            FadeIn(ext_title),
            FadeIn(draft_label),
            FadeIn(draft_chars, lag_ratio=0.04),
            FadeIn(verifier),
            Create(draft_to_verifier),
            FadeIn(outside_badge),
            run_time=1.0,
        )

        self.wait_until(cue_start[5])
        tool_packets = VGroup(
            create_packet("verify", GREEN),
            create_packet("run", BLUE_A),
            create_packet("retrieve", YELLOW),
            create_packet("tool", PURPLE_A),
        ).arrange(RIGHT, buff=0.18).move_to(DOWN * 1.7)
        packet_sources = VGroup(
            create_text("[Aggarwal]", font_size=7, color=GREEN),
            create_text("[Chen]", font_size=7, color=BLUE_A),
            create_text("[Asai]", font_size=7, color=YELLOW),
            create_text("Agent env", font_size=7, color=PURPLE_A),
        ).arrange(RIGHT, buff=0.42).next_to(tool_packets, DOWN, buff=0.12)
        packet_copies = tool_packets.copy()
        self.play(FadeIn(tool_packets, lag_ratio=0.1), FadeIn(packet_sources, lag_ratio=0.1), run_time=0.7)
        self.add(packet_copies)
        self.play(
            *[
                packet.animate.move_to(verifier.get_bottom() + DOWN * 0.25 + RIGHT * (idx - 1.5) * 0.22).scale(0.72)
                for idx, packet in enumerate(packet_copies)
            ],
            run_time=0.9,
        )

        self.wait_until(cue_start[6])
        locator = SurroundingRectangle(draft_chars[9], color=RED_B, buff=0.04, stroke_width=3)
        locator_text = create_text("Error localized", font_size=9, color=RED_B).next_to(locator, UP, buff=0.18)
        signal_arrow = Arrow(verifier.get_left() + DOWN * 0.18, locator.get_right() + DOWN * 0.12, color=RED_B, stroke_width=1.6, buff=0.12)
        fixed_chars = create_letter_row(list("TAYLORSWIFT")).move_to(LEFT * 2.65 + DOWN * 0.85)
        fixed_label = create_text("Corrected output", font_size=9, color=GREEN).next_to(fixed_chars, UP, buff=0.2)
        fix_arrow = Arrow(locator.get_bottom(), fixed_chars[9].get_top(), color=GREEN, stroke_width=1.6, buff=0.08)
        self.play(Create(signal_arrow), Create(locator), FadeIn(locator_text), verifier[0].animate.set_stroke(width=3), run_time=0.7)
        self.play(Create(fix_arrow), FadeIn(fixed_label), FadeIn(fixed_chars, lag_ratio=0.04), run_time=0.8)
        ext_scene = VGroup(
            ext_title,
            draft_chars,
            draft_label,
            verifier,
            draft_to_verifier,
            outside_badge,
            tool_packets,
            packet_sources,
            packet_copies,
            signal_arrow,
            locator,
            locator_text,
            fixed_chars,
            fixed_label,
            fix_arrow,
        )

        self.wait_until(cue_start[7])
        self.play(
            FadeOut(ext_scene),
            run_time=0.6,
        )

        intr_title = create_text("2. Prompted Intrinsic Feedback", font_size=13, color=RED_B)
        intr_title.next_to(sub_title, DOWN, buff=0.3)
        same_model = labeled_box("Same LLM", "generator", width=1.85, height=0.9, color=RED_B)
        same_model.move_to(LEFT * 2.75 + DOWN * 0.15)
        judge_model = labeled_box("Same LLM", "judge", width=1.85, height=0.9, color=RED_B)
        judge_model.move_to(RIGHT * 2.75 + DOWN * 0.15)
        self_loop = CurvedArrow(
            judge_model.get_bottom(),
            same_model.get_bottom(),
            angle=-TAU / 5,
            color=RED_B,
            stroke_width=2,
        )
        internal_arrow = Arrow(same_model.get_right(), judge_model.get_left(), color=RED_B, stroke_width=1.5, buff=0.1)
        sealed_box = DashedVMobject(
            RoundedRectangle(width=6.4, height=2.4, corner_radius=0.12, color=RED_B),
            num_dashes=32,
        ).move_to(DOWN * 0.2)
        no_external = create_text("Closed loop: no outside signal enters", font_size=10, color=GRAY_A).move_to(UP * 1.5)
        self.play(
            FadeIn(intr_title),
            Create(sealed_box),
            FadeIn(same_model),
            FadeIn(judge_model),
            Create(internal_arrow),
            Create(self_loop),
            FadeIn(no_external),
            run_time=1.0,
        )

        self.wait_until(cue_start[8])
        reprompt = labeled_box("Self-Refine", "re-prompt\n[Madaan et al., 2023]", width=2.25, height=0.9, color=BLUE_A)
        reprompt.move_to(DOWN * 1.6)
        prompt_arrow = Arrow(judge_model.get_bottom(), reprompt.get_top(), color=BLUE_A, stroke_width=1.5, buff=0.08)
        critique_packet = create_packet("critique", BLUE_A).move_to(judge_model.get_center())
        self.play(FadeIn(critique_packet), run_time=0.25)
        self.play(critique_packet.animate.move_to(reprompt.get_top() + UP * 0.18), Create(prompt_arrow), FadeIn(reprompt), run_time=0.75)

        self.wait_until(cue_start[9])
        self.play(FadeOut(reprompt), FadeOut(prompt_arrow), FadeOut(critique_packet), run_time=0.3)
        easy_meter = create_signal_meter("easy tasks", 0.78, GREEN)
        missing_meter = create_signal_meter("missing info", 0.55, YELLOW)
        math_meter = create_signal_meter("math reasoning", 0.18, RED_B)
        meters = VGroup(easy_meter, missing_meter, math_meter).arrange(RIGHT, buff=0.45).move_to(DOWN * 2.15)
        meter_caption = create_text("Usable feedback signal", font_size=9, color=GRAY_A).next_to(meters, UP, buff=0.25)
        self.play(FadeIn(meter_caption), FadeIn(meters, lag_ratio=0.12), run_time=1.0)

        self.wait_until(cue_start[10])
        noisy_panel = RoundedRectangle(width=6.9, height=1.05, corner_radius=0.08, color=RED, fill_color="#241014", fill_opacity=0.95)
        noisy_panel.move_to(UP * 1.45)
        noisy_text = create_markup_text(
            "Large Language Models Cannot Self-Correct Reasoning Yet\n"
            "<span foreground='#FF7777'>Takeaway: feedback is too noisy</span>",
            font_size=12,
            color=WHITE,
            line_spacing=1.15,
        ).move_to(noisy_panel.get_center())
        noise_dots = VGroup()
        for idx in range(30):
            x = -2.9 + (idx % 10) * 0.64
            y = -0.75 + (idx // 10) * 0.22
            color = RED_B if idx % 3 else YELLOW
            noise_dots.add(Dot([x, y, 0], radius=0.035, color=color))
        noise_label = create_text("Noisy self-feedback", font_size=9, color=RED_B).next_to(noise_dots, UP, buff=0.18)
        self.play(FadeIn(noisy_panel), FadeIn(noisy_text), FadeIn(noise_dots, lag_ratio=0.03), FadeIn(noise_label), run_time=0.8)

        self.wait_until(cue_start[11])
        self.play(
            FadeOut(intr_title),
            FadeOut(sealed_box),
            FadeOut(same_model),
            FadeOut(judge_model),
            FadeOut(self_loop),
            FadeOut(internal_arrow),
            FadeOut(no_external),
            FadeOut(meter_caption),
            FadeOut(meters),
            FadeOut(noisy_panel),
            FadeOut(noisy_text),
            FadeOut(noise_dots),
            FadeOut(noise_label),
            run_time=0.7,
        )

        train_title = create_text("3. Intrinsic Trained Corrector", font_size=13, color=BLUE_A)
        train_title.next_to(sub_title, DOWN, buff=0.3)
        corrector = labeled_box("Corrector", "learn to fix", width=2.2, height=1.0, color=BLUE_A)
        corrector.move_to(ORIGIN)
        welleck = create_text("[Welleck et al., 2023]", font_size=9, color=GRAY_A).next_to(corrector, DOWN, buff=0.25)
        self.play(FadeIn(train_title), FadeIn(corrector), FadeIn(welleck), run_time=0.9)

        self.wait_until(cue_start[12])
        bad = labeled_box("Bad", "generated sample", width=1.6, height=0.8, color=RED_B)
        reward = labeled_box("Reward", "evaluate", width=1.7, height=0.8, color=YELLOW)
        better = labeled_box("Better", "improved sample", width=1.8, height=0.8, color=GREEN)
        update = labeled_box("Update", "pθ(better | bad)", width=2.1, height=0.8, color=BLUE_A)
        train_flow = VGroup(bad, reward, better, update).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.55)
        train_arrows = VGroup(
            Arrow(bad.get_right(), reward.get_left(), color=GRAY_B, stroke_width=1.3, buff=0.08),
            Arrow(reward.get_right(), better.get_left(), color=GRAY_B, stroke_width=1.3, buff=0.08),
            Arrow(better.get_right(), update.get_left(), color=GRAY_B, stroke_width=1.3, buff=0.08),
        )
        repeat_arrow = CurvedArrow(update.get_bottom(), bad.get_bottom(), angle=-TAU / 4, color=GRAY_C, stroke_width=1.2)
        formula = create_markup_text(
            "<span foreground='#87CEFA'>pθ(better | bad)</span>",
            font_size=20,
            color=WHITE,
        ).move_to(UP * 1.45)
        self.play(FadeOut(corrector), FadeOut(welleck), FadeIn(formula), FadeIn(train_flow), Create(train_arrows), run_time=1.2)
        self.play(Create(repeat_arrow), run_time=0.4)
        pair_tokens = VGroup()
        for idx in range(4):
            pair = VGroup(create_packet("bad", RED_B), create_packet("better", GREEN)).arrange(RIGHT, buff=0.05)
            pair.scale(0.82).move_to(LEFT * 3.8 + DOWN * (1.1 + idx * 0.24))
            pair_tokens.add(pair)
        self.play(FadeIn(pair_tokens, lag_ratio=0.08), run_time=0.45)
        self.play(
            pair_tokens.animate.arrange(DOWN, buff=0.05).next_to(update, DOWN, buff=0.25).scale(0.82),
            run_time=0.8,
        )

        self.wait_until(cue_start[13])
        graph = create_correction_graph().move_to(DOWN * 1.15)
        graph_title = create_text("Training stability", font_size=10, color=GRAY_A).next_to(graph, UP, buff=0.15)
        collapse_note = labeled_box("Behavior\ncollapse", "same flawed output", width=2.0, height=0.9, color=RED)
        score_note = labeled_box("SCoRe", "regularization + RL", width=2.0, height=0.9, color=GREEN)
        VGroup(collapse_note, score_note).arrange(RIGHT, buff=3.1).move_to(UP * 0.75)
        self.play(
            FadeOut(pair_tokens),
            FadeOut(train_flow),
            FadeOut(train_arrows),
            FadeOut(repeat_arrow),
            FadeIn(graph_title),
            Create(graph[0]),
            FadeIn(graph[3]),
            FadeIn(graph[4]),
            run_time=0.7,
        )
        self.play(Create(graph[1]), FadeIn(graph[5]), FadeIn(collapse_note), run_time=0.7)
        self.play(Create(graph[2]), FadeIn(graph[6]), FadeIn(score_note), run_time=0.7)

        self.wait_until(cue_start[14])
        self.play(
            FadeOut(train_title),
            FadeOut(formula),
            FadeOut(graph),
            FadeOut(graph_title),
            FadeOut(collapse_note),
            FadeOut(score_note),
            run_time=0.7,
        )

        summary_title = create_text("Refinement Summary", font_size=13, color=YELLOW).next_to(sub_title, DOWN, buff=0.3)
        summary_cards = VGroup(
            method_card("Extrinsic", "works when environment\nlocalizes errors", GREEN),
            method_card("Prompted intrinsic", "mixed results;\nfeedback can be noisy", RED_B),
            method_card("Trained intrinsic", "promising, but needs\nspecific training strategy", BLUE_A),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.1)
        self.play(FadeIn(summary_title), FadeIn(summary_cards, lag_ratio=0.1), run_time=1.0)

        self.wait_until(cue_start[15])
        self.play(FadeOut(summary_title), FadeOut(summary_cards), run_time=0.5)

        feedback_title = create_text("What does feedback add?", font_size=13, color=YELLOW).next_to(sub_title, DOWN, buff=0.3)
        gauge_base = Line(LEFT * 3.2, RIGHT * 3.2, color=GRAY_D, stroke_width=8).move_to(DOWN * 0.15)
        gauge_left = create_text("Internal guess", font_size=9, color=RED_B).next_to(gauge_base, LEFT, buff=0.2)
        gauge_right = create_text("New signal", font_size=9, color=GREEN).next_to(gauge_base, RIGHT, buff=0.2)
        gauge_dot = Dot(gauge_base.get_start(), radius=0.09, color=RED_B)
        self.play(FadeIn(feedback_title), Create(gauge_base), FadeIn(gauge_left), FadeIn(gauge_right), FadeIn(gauge_dot), run_time=0.9)

        self.wait_until(cue_start[16])
        verifier_signal = labeled_box("Verifier", "detects an error", width=2.0, height=0.85, color=GREEN)
        interpreter_signal = labeled_box("Code interpreter", "runs the output", width=2.2, height=0.85, color=GREEN)
        VGroup(verifier_signal, interpreter_signal).arrange(RIGHT, buff=0.4).move_to(UP * 1.25)
        self.play(FadeIn(verifier_signal), FadeIn(interpreter_signal), gauge_dot.animate.move_to(gauge_base.get_end()), run_time=1.0)

        self.wait_until(cue_start[17])
        self_judge = labeled_box("Same model", "creates and judges", width=2.0, height=0.85, color=RED_B)
        self_judge.move_to(DOWN * 1.45)
        risk = create_text("Risk: fails to judge its own error", font_size=10, color=RED_B).next_to(self_judge, RIGHT, buff=0.3)
        self.play(FadeIn(self_judge), FadeIn(risk), gauge_dot.animate.move_to(gauge_base.get_start() + RIGHT * 1.0), run_time=1.0)

        self.wait_until(cue_start[18])
        self.play(
            FadeOut(feedback_title),
            FadeOut(gauge_base),
            FadeOut(gauge_left),
            FadeOut(gauge_right),
            FadeOut(gauge_dot),
            FadeOut(verifier_signal),
            FadeOut(interpreter_signal),
            FadeOut(self_judge),
            FadeOut(risk),
            run_time=0.6,
        )

        toy_title = create_text('Toy Example: Generate "TAYLORSWIFT"', font_size=13, color=YELLOW).next_to(
            sub_title, DOWN, buff=0.3
        )
        target = list("TAYLORSWIFT")
        draft = list("TAYLORSWIPT")
        boxes = VGroup()
        for idx, char in enumerate(draft):
            color = RED_B if char != target[idx] else BLUE_B
            box = RoundedRectangle(width=0.58, height=0.62, corner_radius=0.05, color=color, fill_color="#15181d", fill_opacity=0.95)
            label = create_text(char, font_size=13, color=WHITE).move_to(box.get_center())
            boxes.add(VGroup(box, label))
        boxes.arrange(RIGHT, buff=0.08).move_to(UP * 0.65)
        generator_label = create_text("Generator: p(character)", font_size=10, color=BLUE_A).next_to(boxes, UP, buff=0.35)
        prob_bars = create_probability_bars(
            [("I", 0.40, BLUE_A), ("P", 0.36, RED_B), ("F", 0.18, GREEN), ("T", 0.06, GRAY_B)]
        ).scale(0.82)
        prob_bars.next_to(boxes[9], DOWN, buff=0.45)
        prob_label = create_text("Position 10 distribution", font_size=8, color=GRAY_A).next_to(prob_bars, DOWN, buff=0.12)
        feedback_box = labeled_box("Feedback", "character 10 is incorrect", width=2.6, height=0.9, color=RED_B)
        feedback_box.move_to(LEFT * 2.0 + DOWN * 1.75)
        corrector_box = labeled_box("Corrector", "regenerate wrong part", width=2.6, height=0.9, color=GREEN)
        corrector_box.next_to(feedback_box, RIGHT, buff=0.65)
        target_arrow = Arrow(feedback_box.get_top(), boxes[9].get_bottom(), color=RED_B, stroke_width=1.8, buff=0.08)
        fix_arrow = Arrow(feedback_box.get_right(), corrector_box.get_left(), color=GREEN, stroke_width=1.8, buff=0.08)
        self.play(FadeIn(toy_title), FadeIn(generator_label), FadeIn(boxes, lag_ratio=0.04), FadeIn(prob_bars, lag_ratio=0.08), FadeIn(prob_label), run_time=1.2)
        self.play(FadeIn(feedback_box), Create(target_arrow), FadeIn(corrector_box), Create(fix_arrow), run_time=0.9)

        self.wait_until(cue_start[19])
        fixed_label = create_text("F", font_size=13, color=WHITE).move_to(boxes[9][1].get_center())
        final = create_markup_text("Final: <b>TAYLORSWIFT</b>", font_size=13, color=GREEN).move_to(DOWN * 2.55)
        localization = create_text("Localized error -> easier correction", font_size=10, color=YELLOW).move_to(DOWN * 2.95)
        corrected_bars = create_probability_bars(
            [("I", 0.08, BLUE_A), ("P", 0.04, RED_B), ("F", 0.82, GREEN), ("T", 0.06, GRAY_B)]
        ).scale(0.82)
        corrected_bars.move_to(prob_bars.get_center())
        self.play(
            boxes[9][0].animate.set_color(GREEN).set_fill("#143c14", opacity=0.95),
            FadeOut(boxes[9][1]),
            FadeIn(fixed_label),
            FadeOut(target_arrow),
            ReplacementTransform(prob_bars, corrected_bars),
            run_time=0.8,
        )
        boxes[9].remove(boxes[9][1])
        boxes[9].add(fixed_label)
        self.play(FadeIn(localization), FadeIn(final), run_time=0.7)

        self.wait_until(voiceover_end + 0.2)
        self.play(
            FadeOut(toy_title),
            FadeOut(generator_label),
            FadeOut(boxes),
            FadeOut(corrected_bars),
            FadeOut(prob_label),
            FadeOut(feedback_box),
            FadeOut(corrector_box),
            FadeOut(fix_arrow),
            FadeOut(localization),
            FadeOut(final),
            FadeOut(sub_title),
            run_time=0.8,
        )

        assert_all_scene_voiceovers_played(self)
