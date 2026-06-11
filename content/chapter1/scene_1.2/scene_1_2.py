import os
import tempfile
from pathlib import Path
from manim import *

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VOICEOVER_DIR = PROJECT_ROOT / "voiceover" / "generated_sentence_level"
PRETRAINING_CHART_PATH = Path(__file__).resolve().parent / "assets" / "pretraining_scaling_laws_chart.png"
POSTTRAINING_CHART_PATH = Path(__file__).resolve().parent / "assets" / "posttraining_instruction_finetuning_chart.png"
SLIDE_PAGE6_EXTRA_TOKENS_PATH = Path(__file__).resolve().parent / "assets" / "slide_page6_generate_extra_tokens.png"
SLIDE_PAGE8_MATH_CHART_PATH = Path(__file__).resolve().parent / "assets" / "slide_page8_math_chart.png"
SLIDE_PAGE9_TOOLS_DIAGRAM_PATH = Path(__file__).resolve().parent / "assets" / "slide_page9_tools_diagram.png"

SCENE_1_2_DURATIONS = {
    "sc12_001.mp3": 4.505,
    "sc12_002.mp3": 8.313,
    "sc12_003.mp3": 10.031,
    "sc12_004.mp3": 2.183,
    "sc12_005.mp3": 6.687,
    "sc12_006.mp3": 7.663,
    "sc12_007.mp3": 3.437,
    "sc12_008.mp3": 7.291,
    "sc12_009.mp3": 26.517,
}
SCENE_1_2_VOICEOVERS = (
    "sc12_001.mp3",
    "sc12_002.mp3",
    "sc12_003.mp3",
    "sc12_004.mp3",
    "sc12_005.mp3",
    "sc12_009.mp3",
    "sc12_006.mp3",
    "sc12_007.mp3",
    "sc12_008.mp3",
)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc12_*.mp3"))
    expected = sorted(SCENE_1_2_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 1.2 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_1_2_DURATIONS:
        raise KeyError(f"Unexpected Scene 1.2 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 1.2 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene, start_offset=0.0):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = start_offset
    for filename, duration in SCENE_1_2_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    if played != SCENE_1_2_VOICEOVERS:
        missing = [filename for filename in SCENE_1_2_VOICEOVERS if filename not in played]
        raise RuntimeError(
            f"Scene 1.2 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


def finish_voiceovers(scene, voiceover_end, padding=0.25):
    current_time = getattr(scene.renderer, "time", 0.0)
    remaining = voiceover_end + padding - current_time
    if remaining > 0:
        scene.wait(remaining)


# Note: visual/narration alignment comment translated from Vietnamese.
def create_text(text, font_size=24, font="Noto Sans", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)

# Note: visual/narration alignment comment translated from Vietnamese.
def create_markup_text(text, font_size=24, font="Noto Sans", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)

# Note: visual/narration alignment comment translated from Vietnamese.
def get_text_part(mobject, substring):
    raw_text = getattr(mobject, "text", "")
    if not raw_text:
        for sub in mobject.submobjects:
            if hasattr(sub, "text"):
                raw_text = sub.text
                mobject = sub
                break

    # Note: visual/narration alignment comment translated from Vietnamese.
    clean_chars = []
    in_tag = False
    for char in raw_text:
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        elif not in_tag:
            clean_chars.append(char)
    clean_text = "".join(clean_chars)

    # Note: visual/narration alignment comment translated from Vietnamese.
    clean_text_no_spaces = clean_text.replace(" ", "")
    sub_no_spaces = substring.replace(" ", "")
    start_idx_no_spaces = clean_text_no_spaces.find(sub_no_spaces)
    if start_idx_no_spaces == -1:
        raise ValueError(f"Substring not found '{substring}' trong '{clean_text}' (raw: '{raw_text}')")

    # Note: visual/narration alignment comment translated from Vietnamese.
    mapping = []
    for idx, char in enumerate(clean_text):
        if char != ' ':
            mapping.append(idx)
            
    start_idx = mapping[start_idx_no_spaces]
    end_idx = mapping[start_idx_no_spaces + len(sub_no_spaces) - 1] + 1
    return mobject[start_idx:end_idx]



class Scene1_2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Voiceover audio is scheduled at each visual beat, not all at scene start.
        validate_scene_voiceover_files()
        self.played_voiceovers = []

        def make_center_card(title, body, accent_color, fill_color, title_size=48, body_size=25):
            box = RoundedRectangle(
                width=11.6,
                height=4.9,
                corner_radius=0.18,
                color=accent_color,
                stroke_width=3,
                fill_color=fill_color,
                fill_opacity=0.92,
            )
            title_text = create_text(title, font_size=title_size, color=accent_color, weight=BOLD)
            body_text = create_markup_text(body, font_size=body_size, line_spacing=1.0, color=WHITE)
            content = VGroup(title_text, body_text).arrange(DOWN, buff=0.35)
            content.move_to(box.get_center())
            return VGroup(box, content)

        def add_voiceovers_now(filenames):
            offset = 0.0
            for filename in filenames:
                duration = SCENE_1_2_DURATIONS[filename]
                add_voiceover(self, filename, time_offset=offset, duration=duration)
                offset += duration
            return offset

        def show_card(card, duration=None, voiceovers=(), fade_in_time=0.25, fade_out_time=0.25):
            voiceover_duration = add_voiceovers_now(voiceovers)
            hold_duration = duration if duration is not None else voiceover_duration
            self.play(FadeIn(card), run_time=fade_in_time)
            self.wait(max(hold_duration - fade_in_time, 0))
            self.play(FadeOut(card), run_time=fade_out_time)

        def make_title_card(title, accent_color, fill_color):
            box = RoundedRectangle(
                width=11.6,
                height=3.1,
                corner_radius=0.18,
                color=accent_color,
                stroke_width=3,
                fill_color=fill_color,
                fill_opacity=0.92,
            )
            title_text = create_text(title, font_size=58, color=accent_color, weight=BOLD)
            if title_text.width > box.width - 0.8:
                title_text.scale_to_fit_width(box.width - 0.8)
            title_text.move_to(box.get_center())
            return VGroup(box, title_text)

        def make_side_visual(chart_path, body, accent_color, fill_color, source_text):
            chart = ImageMobject(str(chart_path))
            chart.set(width=5.25)
            chart.move_to(LEFT * 3.25)

            box = RoundedRectangle(
                width=6.2,
                height=4.25,
                corner_radius=0.18,
                color=accent_color,
                stroke_width=3,
                fill_color=fill_color,
                fill_opacity=0.92,
            )
            box.move_to(RIGHT * 3.25 + UP * 0.18)

            body_text = create_markup_text(
                body,
                font_size=22,
                line_spacing=1.0,
                color=WHITE,
            )
            max_text_width = box.width - 0.65
            if body_text.width > max_text_width:
                body_text.scale_to_fit_width(max_text_width)
            body_text.move_to(box.get_center())

            source = create_markup_text(
                source_text,
                font_size=13,
                color=GRAY_A,
            )
            if source.width > chart.width:
                source.scale_to_fit_width(chart.width)
            source.next_to(chart, DOWN, buff=0.18)

            return Group(chart, box, body_text, source)

        def make_method_panel(number, title, image_path, source_text, pos):
            accent_color = BLUE_A
            panel = RoundedRectangle(
                width=11.3,
                height=1.75,
                corner_radius=0.16,
                color=accent_color,
                stroke_width=2.2,
                fill_color="#12161c",
                fill_opacity=0.95,
            ).move_to(pos)

            badge = Circle(
                radius=0.24,
                color=accent_color,
                fill_color=accent_color,
                fill_opacity=0.25,
                stroke_width=2,
            )
            badge.move_to(panel.get_left() + RIGHT * 0.62 + UP * 0.28)
            badge_text = create_text(str(number), font_size=18, color=accent_color, weight=BOLD)
            badge_text.move_to(badge)

            title_text = create_text(title, font_size=13, color=WHITE, weight=BOLD, line_spacing=0.85)
            if title_text.width > 2.4:
                title_text.scale_to_fit_width(2.4)
            title_text.next_to(badge, RIGHT, buff=0.18)
            title_text.align_to(badge, UP).shift(DOWN * 0.02)

            slide_image = ImageMobject(str(image_path))
            slide_image.set(width=5.8)
            max_image_height = 1.42 if number == 2 else 1.12
            if slide_image.height > max_image_height:
                slide_image.set(height=max_image_height)
            slide_image.move_to(panel.get_center() + RIGHT * 1.75 + UP * 0.12)

            source = create_text(source_text, font_size=9.5, color=GRAY_A)
            if source.width > 5.8:
                source.scale_to_fit_width(5.8)
            source.next_to(slide_image, DOWN, buff=0.08)

            return Group(panel, badge, badge_text, title_text, slide_image, source)

        def make_test_time_methods_scene():
            panels = Group(
                make_method_panel(
                    1,
                    "Generate extra tokens",
                    SLIDE_PAGE6_EXTRA_TOKENS_PATH,
                    "[Wei et al., 2022]",
                    UP * 2.05,
                ),
                make_method_panel(
                    2,
                    "Call generator\nmultiple times",
                    SLIDE_PAGE8_MATH_CHART_PATH,
                    "Math [Brown et al., 2024]",
                    ORIGIN,
                ),
                make_method_panel(
                    3,
                    "Incorporate\nmodels/tools",
                    SLIDE_PAGE9_TOOLS_DIAGRAM_PATH,
                    "[Zaharia et al., 2024]",
                    DOWN * 2.05,
                ),
            )
            return panels

        wave_1_title = make_title_card(
            "1. Scale Pre-training Compute",
            BLUE_A,
            "#12161c",
        )
        wave_1 = make_side_visual(
            PRETRAINING_CHART_PATH,
            "- Increase compute power\n"
            "- Larger dataset\n"
            "- More parameters\n"
            "Goal: Enhance generalization capabilities, reduce errors.",
            BLUE_A,
            "#12161c",
            "Source: Scaling Laws for Neural Language Models [Kaplan et al., 2020]",
        )
        wave_2_title = make_title_card(
            "2. Scale Post-training Compute",
            BLUE_A,
            "#12161c",
        )
        wave_2 = make_side_visual(
            POSTTRAINING_CHART_PATH,
            "- Instruction finetuning\n"
            "- Reinforcement Learning from human feedback\n"
            "- Chain-Of-Thought finetuning\n"
            "Goal: Generalization to unseen tasks",
            BLUE_A,
            "#12161c",
            "Source: Scaling Instruction-Finetuned Language Models [Chung et al., 2022]",
        )
        wave_3 = make_title_card(
            "3. Test-time compute wave",
            BLUE_A,
            "#12161c",
        )
        closing = make_center_card(
            "Another Compute Dimension",
            "• Test-time scaling does not replace pretraining\n"
            "  or post-training\n"
            "• It is used after the model already exists\n"
            "• It is applied when the system generates an answer",
            BLUE_A,
            "#12161c",
            title_size=44,
            body_size=23,
        )

        self.wait(1.0)
        add_voiceovers_now(("sc12_001.mp3",))
        self.wait(SCENE_1_2_DURATIONS["sc12_001.mp3"])
        show_card(wave_1_title, duration=3.0, voiceovers=("sc12_002.mp3",))
        show_card(
            wave_1,
            duration=SCENE_1_2_DURATIONS["sc12_002.mp3"] - 3.0,
        )
        show_card(wave_2_title, 1.0)
        show_card(wave_2, voiceovers=("sc12_003.mp3",))
        show_card(
            wave_3,
            voiceovers=("sc12_004.mp3", "sc12_005.mp3"),
        )
        methods_scene = make_test_time_methods_scene()
        show_card(methods_scene, voiceovers=("sc12_009.mp3",), fade_in_time=0.35, fade_out_time=0.35)
        show_card(
            closing,
            voiceovers=("sc12_006.mp3", "sc12_007.mp3", "sc12_008.mp3"),
        )

        assert_all_scene_voiceovers_played(self)
