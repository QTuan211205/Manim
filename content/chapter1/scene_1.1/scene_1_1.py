import os
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
FONTCONFIG_CACHE_DIR = PROJECT_ROOT / ".cache" / "fontconfig"
FONTCONFIG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
FONTCONFIG_FILE = Path(tempfile.gettempdir()) / "manim_fontconfig_fonts.conf"
FONTCONFIG_FILE.write_text(
    f"""<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <dir>{PROJECT_ROOT / ".local" / "share" / "fonts"}</dir>
  <cachedir>{FONTCONFIG_CACHE_DIR}</cachedir>
</fontconfig>
""",
    encoding="utf-8",
)
os.environ.setdefault("FONTCONFIG_FILE", str(FONTCONFIG_FILE))
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_ROOT / ".cache"))

from manim import *
import manimpango

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = PROJECT_ROOT / "voiceover" / "generated_sentence_level"
DEFAULT_FONT = "Segoe UI" if "Segoe UI" in manimpango.list_fonts() else "Selawik"

SCENE_1_1_DURATIONS = {
    "sc11_001.mp3": 10.495,
    "sc11_002.mp3": 10.217,
    "sc11_003.mp3": 9.149,
    "sc11_004.mp3": 10.495,
    "sc11_005.mp3": 6.687,
    "sc11_006.mp3": 4.087,
    "sc11_007.mp3": 12.399,
}
SCENE_1_1_VOICEOVERS = tuple(SCENE_1_1_DURATIONS)

FIRST_VOICEOVER_START = 3.0


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc11_*.mp3"))
    expected = sorted(SCENE_1_1_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 1.1 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def wait_for_voiceover(scene, voiceover_start, duration, padding=0.5):
    current_time = getattr(scene.renderer, "time", 0.0)
    remaining = voiceover_start + duration + padding - current_time
    if remaining > 0:
        scene.wait(remaining)


def wait_until(scene, target_time):
    current_time = getattr(scene.renderer, "time", 0.0)
    remaining = target_time - current_time
    if remaining > 0:
        scene.wait(remaining)


def play_voiceover(scene, filename):
    if filename not in SCENE_1_1_DURATIONS:
        raise KeyError(f"Unexpected Scene 1.1 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 1.1 voiceover file: {filename}")
    voiceover_start = scene.renderer.time
    scene.add_sound(str(VOICEOVER_DIR / filename))
    scene.played_voiceovers.append(filename)
    return voiceover_start, SCENE_1_1_DURATIONS[filename]


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    if played != SCENE_1_1_VOICEOVERS:
        missing = [filename for filename in SCENE_1_1_VOICEOVERS if filename not in played]
        raise RuntimeError(
            f"Scene 1.1 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


# Note: visual/narration alignment comment translated from Vietnamese.
def create_text(text, font_size=24, font=DEFAULT_FONT, color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)

# Note: visual/narration alignment comment translated from Vietnamese.
def create_markup_text(text, font_size=24, font=DEFAULT_FONT, **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)

def source_arrow(left, right, color=BLUE_B, stroke_width=3, buff=0.04, tip_ratio=0.25):
    return Arrow(
        left.get_right(),
        right.get_left(),
        buff=buff,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=tip_ratio,
        color=color,
    )


class Scene1_1(Scene):
    def construct(self):
        validate_scene_voiceover_files()
        self.played_voiceovers = []

        # =========================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
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
        # Note: visual/narration alignment comment translated from Vietnamese.
        # 
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =========================================================================

        self.camera.background_color = "#111111"

        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4.5, 4.5, 1],
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 0.6,
                "stroke_opacity": 0.12,
            },
            axis_config={"stroke_opacity": 0},
        )
        self.add(grid)

        # =========================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =========================================================================
        # Slide 1: title.
        title = create_text("Beyond Decoding", font_size=38, color=BLUE_B, weight=BOLD)
        subtitle = create_text(
            "Meta-Generation Algorithms\nfor Large Language Models",
            font_size=24,
            color=WHITE,
            line_spacing=0.85,
        ).next_to(title, DOWN, buff=0.35)
        title_group = VGroup(title, subtitle).move_to(ORIGIN)
        underline = Line(title.get_left(), title.get_right(), color=BLUE_E, stroke_width=2)
        underline.next_to(title, DOWN, buff=0.08)

        self.play(Write(title), Create(underline), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)
        self.wait(0.5)

        wait_until(self, FIRST_VOICEOVER_START)
        voiceover_start, voiceover_duration = play_voiceover(self, "sc11_001.mp3")
        self.play(
            title_group.animate.scale(0.58).to_edge(UP, buff=0.32),
            FadeOut(underline),
            run_time=1.0,
        )

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Slides 2-3: today's talk and why test-time compute matters.
        talk_box = RoundedRectangle(
            width=6.2,
            height=1.45,
            corner_radius=0.08,
            color=BLUE_D,
            fill_color="#0e1726",
            fill_opacity=0.9,
        ).shift(UP * 1.05)
        talk_title = create_text("Today's talk", font_size=18, color=BLUE_A, weight=BOLD)
        talk_line = create_text(
            "Algorithms for generating outputs\nwith a language model",
            font_size=20,
            color=WHITE,
            line_spacing=0.8,
        )
        talk_content = VGroup(talk_title, talk_line).arrange(DOWN, buff=0.18).move_to(talk_box)

        lm_box = RoundedRectangle(
            width=2.1,
            height=0.85,
            corner_radius=0.08,
            color=BLUE_C,
            fill_color="#101f35",
            fill_opacity=0.95,
        ).shift(LEFT * 2.65 + DOWN * 1.2)
        lm_text = create_text("Language\nmodel", font_size=15, color=BLUE_A, line_spacing=0.8).move_to(lm_box)

        alg_box = RoundedRectangle(
            width=2.4,
            height=0.85,
            corner_radius=0.08,
            color=YELLOW_D,
            fill_color="#2a240d",
            fill_opacity=0.95,
        ).shift(DOWN * 1.2)
        alg_text = create_text("Generation\nalgorithm", font_size=15, color=YELLOW, line_spacing=0.8).move_to(alg_box)

        out_box = RoundedRectangle(
            width=2.1,
            height=0.85,
            corner_radius=0.08,
            color=GREEN_D,
            fill_color="#0e2418",
            fill_opacity=0.95,
        ).shift(RIGHT * 2.65 + DOWN * 1.2)
        out_text = create_text("Output\nsequence", font_size=15, color=GREEN_A, line_spacing=0.8).move_to(out_box)

        arrows = VGroup(source_arrow(lm_box, alg_box), source_arrow(alg_box, out_box))
        pipe = VGroup(lm_box, lm_text, alg_box, alg_text, out_box, out_text, arrows)

        token_stream = VGroup()
        for tok in ["Taylor", "Swift", "is", "..."]:
            cell = RoundedRectangle(
                width=0.78,
                height=0.32,
                corner_radius=0.05,
                color=GREEN_C,
                fill_color="#12281a",
                fill_opacity=0.95,
                stroke_width=1.2,
            )
            label = create_text(tok, font_size=10, color=GREEN_A).move_to(cell)
            token_stream.add(VGroup(cell, label))
        token_stream.arrange(RIGHT, buff=0.08).next_to(out_box, DOWN, buff=0.25)

        self.play(FadeIn(talk_box), Write(talk_content), run_time=1.3)
        wait_for_voiceover(self, voiceover_start, voiceover_duration, padding=0.35)

        voiceover_start, voiceover_duration = play_voiceover(self, "sc11_002.mp3")
        self.play(FadeIn(lm_box), Write(lm_text), run_time=0.6)
        self.play(FadeIn(alg_box), Write(alg_text), GrowArrow(arrows[0]), run_time=0.8)
        self.play(FadeIn(out_box), Write(out_text), GrowArrow(arrows[1]), run_time=0.8)
        for token in token_stream:
            self.play(FadeIn(token, shift=RIGHT * 0.12), run_time=0.25)
        self.wait(1.2)

        # Note: visual/narration alignment comment translated from Vietnamese.
        why_title = create_text("Why?", font_size=19, color=YELLOW, weight=BOLD)
        why_text = create_text(
            "Use test-time compute\nto improve performance",
            font_size=22,
            color=WHITE,
            line_spacing=0.82,
        )
        why_group = VGroup(why_title, why_text).arrange(DOWN, buff=0.18)
        why_group.next_to(talk_box, DOWN, buff=0.42).shift(LEFT * 3.9)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 3, 1],
            x_length=3.7,
            y_length=2.0,
            axis_config={"color": GRAY_B, "stroke_width": 1.6, "include_ticks": False},
        ).shift(RIGHT * 2.35 + DOWN * 1.15)
        x_label = create_text("Test-time compute", font_size=10, color=GRAY_A).next_to(
            axes.x_axis, DOWN, buff=0.12
        )
        y_label = create_text("Performance", font_size=10, color=GRAY_A).next_to(
            axes.y_axis, LEFT, buff=0.1
        ).rotate(PI / 2)
        curve = axes.plot(lambda x: 0.42 + 2.1 * (1 - np.exp(-0.58 * x)), x_range=[0, 3.75], color=BLUE_B)

        self.play(FadeOut(token_stream), FadeOut(pipe), run_time=0.8)
        self.play(Write(why_title), FadeIn(why_text, shift=UP * 0.15), run_time=0.9)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.9)
        self.play(Create(curve), run_time=0.8)
        wait_for_voiceover(self, voiceover_start, voiceover_duration, padding=0.55)

        # =========================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =========================================================================
        # Slide 4: language-model tasks are sequence-generation tasks.
        self.play(
            FadeOut(title_group),
            FadeOut(talk_box),
            FadeOut(talk_content),
            FadeOut(why_group),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(curve),
            run_time=0.8,
        )

        section_title = create_text("Language models", font_size=28, color=BLUE_A, weight=BOLD)
        section_title.to_edge(UP, buff=1.05)
        sequence_caption = create_text(
            "Tasks framed as generating sequences",
            font_size=18,
            color=GRAY_A,
        ).next_to(section_title, DOWN, buff=0.18)

        math_card = self.make_task_card(
            "Solving olympiad problems",
            ["Problem", "Reasoning", "Answer"],
            PURPLE_B,
        ).shift(LEFT * 2.95 + DOWN * 0.35)
        code_card = self.make_task_card(
            "Writing code",
            ["Spec", "Function", "Program"],
            GREEN_B,
        ).shift(RIGHT * 2.95 + DOWN * 0.35)

        voiceover_start, voiceover_duration = play_voiceover(self, "sc11_003.mp3")
        self.play(Write(section_title), FadeIn(sequence_caption, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(math_card, shift=UP * 0.2), FadeIn(code_card, shift=UP * 0.2), run_time=1.1)

        math_tokens = self.make_token_chain(["x<sub>1</sub>", "x<sub>2</sub>", "x<sub>3</sub>", "..."], PURPLE_A)
        math_tokens.next_to(math_card, DOWN, buff=0.28)
        code_tokens = self.make_token_chain(["def", "solve", "(", "..."], GREEN_A)
        code_tokens.next_to(code_card, DOWN, buff=0.28)

        for chain in [math_tokens, code_tokens]:
            for token in chain:
                self.play(FadeIn(token, shift=RIGHT * 0.1), run_time=0.18)
        wait_for_voiceover(self, voiceover_start, voiceover_duration, padding=0.45)

        voiceover_start, voiceover_duration = play_voiceover(self, "sc11_004.mp3")
        focus_question = create_text(
            "How should we call, control,\nand combine the model?",
            font_size=21,
            color=YELLOW,
            line_spacing=0.82,
        ).move_to(DOWN * 2.15)
        result_tag = create_text("Goal: best result", font_size=16, color=GREEN_A)
        result_tag.next_to(focus_question, DOWN, buff=0.22)
        self.play(
            FadeOut(math_tokens),
            FadeOut(code_tokens),
            math_card.animate.shift(LEFT * 0.45).scale(0.86),
            code_card.animate.shift(RIGHT * 0.45).scale(0.86),
            run_time=0.9,
        )
        self.play(FadeIn(focus_question, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(result_tag, shift=UP * 0.1), run_time=0.5)
        wait_for_voiceover(self, voiceover_start, voiceover_duration, padding=0.65)

        # =========================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =========================================================================
        voiceover_start, voiceover_duration = play_voiceover(self, "sc11_005.mp3")

        self.play(
            FadeOut(math_card),
            FadeOut(code_card),
            FadeOut(focus_question),
            FadeOut(result_tag),
            run_time=0.8,
        )

        context_title = create_text("Inference algorithms + LLM OS", font_size=26, color=BLUE_A, weight=BOLD)
        context_title.to_edge(UP, buff=1.05)
        model_node = self.make_system_node("Language\nmodel", BLUE_B).shift(LEFT * 3.4 + DOWN * 0.16)
        algorithm_node = self.make_system_node("Inference\nalgorithm", YELLOW_D).shift(LEFT * 1.1 + DOWN * 0.16)
        os_node = self.make_system_node("LLM OS", PURPLE_B).shift(RIGHT * 1.1 + DOWN * 0.16)
        output_node = self.make_system_node("Output", GREEN_B).shift(RIGHT * 3.4 + DOWN * 0.16)
        system_arrows = VGroup(
            source_arrow(model_node, algorithm_node, color=BLUE_B),
            source_arrow(algorithm_node, os_node, color=YELLOW_D),
            source_arrow(os_node, output_node, color=GREEN_B),
        )
        self.play(
            ReplacementTransform(section_title, context_title),
            FadeOut(sequence_caption),
            run_time=0.8,
        )
        system_group = VGroup(model_node, algorithm_node, os_node, output_node, system_arrows)
        self.play(
            FadeIn(model_node, shift=UP * 0.15),
            FadeIn(algorithm_node, shift=UP * 0.15),
            FadeIn(os_node, shift=UP * 0.15),
            FadeIn(output_node, shift=UP * 0.15),
            run_time=1.0,
        )
        self.play(*[GrowArrow(arrow) for arrow in system_arrows], run_time=0.9)
        wait_for_voiceover(self, voiceover_start, voiceover_duration, padding=0.45)

        voiceover_start, voiceover_duration = play_voiceover(self, "sc11_006.mp3")
        self.play(system_group.animate.shift(UP * 0.35), run_time=0.6)
        system_highlight = SurroundingRectangle(
            system_group,
            buff=0.28,
            corner_radius=0.12,
            color=BLUE_E,
            stroke_width=1.8,
        )
        system_highlight.set_stroke(opacity=0.55)
        self.play(
            FadeIn(system_highlight),
            run_time=0.45,
        )
        self.play(Indicate(algorithm_node, color=YELLOW, scale_factor=1.04), run_time=0.6)
        wait_for_voiceover(self, voiceover_start, voiceover_duration, padding=0.45)

        voiceover_start, voiceover_duration = play_voiceover(self, "sc11_007.mp3")
        component_labels = VGroup(
            self.make_small_chip("many model calls", BLUE_A),
            self.make_small_chip("tools", GREEN_A),
            self.make_small_chip("evaluators", YELLOW),
            self.make_small_chip("compute budget", PURPLE_A),
        ).arrange(RIGHT, buff=0.24)
        component_labels.to_edge(DOWN, buff=1.0)
        complete_system = create_text("A complete generation system", font_size=22, color=WHITE, weight=BOLD)
        complete_system.next_to(component_labels, UP, buff=0.34)
        self.play(FadeIn(complete_system, shift=UP * 0.1), run_time=0.55)
        for chip in component_labels:
            self.play(FadeIn(chip, shift=UP * 0.08), run_time=0.22)

        closing = create_text(
            "One viewpoint: generating an output sequence with a language model.",
            font_size=17,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(closing, shift=UP * 0.15), run_time=0.8)
        wait_for_voiceover(self, voiceover_start, voiceover_duration, padding=0.75)

        self.play(
            FadeOut(context_title),
            FadeOut(model_node),
            FadeOut(algorithm_node),
            FadeOut(os_node),
            FadeOut(output_node),
            FadeOut(system_arrows),
            FadeOut(system_highlight),
            FadeOut(complete_system),
            FadeOut(component_labels),
            FadeOut(closing),
            run_time=1.0,
        )
        assert_all_scene_voiceovers_played(self)

    def make_task_card(self, title, steps, color):
        card = RoundedRectangle(
            width=4.4,
            height=2.2,
            corner_radius=0.1,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
            stroke_width=2,
        )
        title_text = create_text(title, font_size=15, color=color, weight=BOLD).next_to(
            card.get_top(), DOWN, buff=0.22
        )
        step_groups = VGroup()
        for step in steps:
            box = RoundedRectangle(
                width=1.15,
                height=0.44,
                corner_radius=0.06,
                color=color,
                fill_color="#202020",
                fill_opacity=0.95,
                stroke_width=1.2,
            )
            txt = create_text(step, font_size=10, color=WHITE).move_to(box)
            step_groups.add(VGroup(box, txt))
        step_groups.arrange(RIGHT, buff=0.22).move_to(card.get_center() + DOWN * 0.22)
        arrows = VGroup()
        for left, right in zip(step_groups[:-1], step_groups[1:]):
            arrows.add(source_arrow(left, right, color=color, stroke_width=2, buff=0.03, tip_ratio=0.22))
        return VGroup(card, title_text, step_groups, arrows)

    def make_token_chain(self, tokens, color):
        chain = VGroup()
        for token in tokens:
            box = RoundedRectangle(
                width=0.72,
                height=0.34,
                corner_radius=0.05,
                color=color,
                fill_color="#191919",
                fill_opacity=0.95,
                stroke_width=1.1,
            )
            txt = create_markup_text(token, font_size=10, color=color).move_to(box)
            chain.add(VGroup(box, txt))
        chain.arrange(RIGHT, buff=0.08)
        return chain

    def make_system_node(self, label, color):
        box = RoundedRectangle(
            width=1.65,
            height=0.82,
            corner_radius=0.08,
            color=color,
            fill_color="#181818",
            fill_opacity=0.95,
            stroke_width=1.5,
        )
        text = create_text(label, font_size=13, color=color, line_spacing=0.8).move_to(box)
        return VGroup(box, text)

    def make_small_chip(self, label, color):
        chip = RoundedRectangle(
            width=1.72,
            height=0.42,
            corner_radius=0.08,
            color=color,
            fill_color="#181818",
            fill_opacity=0.95,
            stroke_width=1.2,
        )
        text = create_text(label, font_size=10, color=color).move_to(chip)
        return VGroup(chip, text)
