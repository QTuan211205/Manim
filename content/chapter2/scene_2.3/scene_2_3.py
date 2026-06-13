import os
import tempfile
from pathlib import Path

from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"
ASSET_DIR = Path(__file__).resolve().parent / "assets"
SOURCE_URL = "https://neurips.cc/virtual/2024/tutorial/99522"

VOICEOVERS = [
    ("sc23_001.mp3", 4.736871),
    ("sc23_002.mp3", 4.133152),
    ("sc23_003.mp3", 10.959819),
    ("sc23_004.mp3", 3.808073),
    ("sc23_005.mp3", 3.111474),
    ("sc23_006.mp3", 7.012426),
    ("sc23_007.mp3", 12.724535),
    ("sc23_008.mp3", 2.089796),
    ("sc23_009.mp3", 12.492336),
    ("sc23_010.mp3", 4.504671),
    ("sc23_011.mp3", 6.640907),
    ("sc23_012.mp3", 5.201270),
    ("sc23_013.mp3", 7.430385),
    ("sc23_014.mp3", 8.637823),
    ("sc23_015.mp3", 3.482993),
]


def create_text(text, font_size=24, font="Noto Sans", color=WHITE, **kwargs):
    if font_size < 20:
        item = Text(text, font_size=36, font=font, color=color, **kwargs)
        item.scale(font_size / 36)
        return item
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)


def create_markup_text(text, font_size=24, font="Noto Sans", **kwargs):
    if font_size < 20:
        item = MarkupText(text, font_size=36, font=font, **kwargs)
        item.scale(font_size / 36)
        return item
    return MarkupText(text, font_size=font_size, font=font, **kwargs)


def short_label(text, font_size=20, color=WHITE):
    return create_text(text, font_size=font_size, color=color)


def pill(text, width, color=BLUE_B, fill="#181a1e", font_size=20):
    box = RoundedRectangle(
        width=width,
        height=0.62,
        corner_radius=0.08,
        color=color,
        fill_color=fill,
        fill_opacity=0.9,
        stroke_width=1.8,
    )
    label = create_text(text, font_size=font_size, color=WHITE)
    label.move_to(box.get_center())
    return VGroup(box, label)


def token(text, color=BLUE_B, fill="#111a25", width=None):
    width = width or max(0.8, 0.22 * len(text) + 0.55)
    box = RoundedRectangle(
        width=width,
        height=0.48,
        corner_radius=0.06,
        color=color,
        fill_color=fill,
        fill_opacity=0.95,
        stroke_width=1.5,
    )
    label = create_text(text, font_size=18, color=WHITE)
    label.move_to(box)
    return VGroup(box, label)


def slide_visual(filename, width=8.0):
    image = ImageMobject(str(ASSET_DIR / filename))
    image.scale_to_fit_width(width)
    source = create_text(SOURCE_URL, font_size=14, color=GRAY_A)
    source.next_to(image, DOWN, buff=0.14)
    return Group(image, source).move_to(ORIGIN).shift(DOWN * 0.1)


def score_bar(label, value, color, width=3.8):
    label_mob = create_text(label, font_size=18, color=WHITE)
    track = RoundedRectangle(
        width=width,
        height=0.22,
        corner_radius=0.06,
        color=GRAY_D,
        fill_color="#1a1a1a",
        fill_opacity=1,
        stroke_width=1,
    )
    fill = RoundedRectangle(
        width=width * value,
        height=0.22,
        corner_radius=0.06,
        color=color,
        fill_color=color,
        fill_opacity=0.85,
        stroke_width=0,
    )
    fill.align_to(track, LEFT)
    group = VGroup(label_mob, VGroup(track, fill)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    return group


class Scene2_3(MovingCameraScene):
    def schedule_voiceovers(self):
        starts = {}
        current = 0.0
        missing = []

        for index, (filename, duration) in enumerate(VOICEOVERS, start=1):
            audio_path = VOICEOVER_DIR / filename
            if not audio_path.exists():
                missing.append(str(audio_path))
            starts[index] = current
            self.add_sound(str(audio_path), time_offset=current)
            current += duration

        if missing:
            raise FileNotFoundError("Missing scene 2.3 voiceover files:\n" + "\n".join(missing))

        return starts, current

    def wait_until(self, target_time):
        current_time = getattr(self.renderer, "time", 0.0)
        if target_time > current_time:
            self.wait(target_time - current_time)

    def replace_content(self, old_group, new_group, run_time=0.6):
        if old_group is None:
            self.play(FadeIn(new_group, shift=UP * 0.12), run_time=run_time)
        else:
            self.play(FadeOut(old_group, shift=DOWN * 0.08), FadeIn(new_group, shift=UP * 0.08), run_time=run_time)
        return new_group

    def construct(self):
        self.camera.background_color = "#111111"
        cue_start, voiceover_end = self.schedule_voiceovers()

        title = create_text("MAP Pitfalls", font_size=32, color=RED_A)
        subtitle = create_text("Most likely is not always best", font_size=18, color=GRAY_A)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.18)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.8)

        content = None

        self.wait_until(cue_start[1] + 0.35)
        closed = VGroup(
            pill("Translation", 2.4, BLUE_B, "#111a25"),
            pill("QA", 1.3, BLUE_B, "#111a25"),
        ).arrange(RIGHT, buff=0.45)
        constrained = SurroundingRectangle(closed, color=BLUE_C, buff=0.25, corner_radius=0.08)
        map_badge = pill("MAP", 1.4, BLUE_A, "#102033", font_size=21)
        arrow = Arrow(map_badge.get_right(), constrained.get_left(), color=BLUE_A, buff=0.2)
        next_content = VGroup(map_badge, arrow, constrained, closed).move_to(ORIGIN)
        content = self.replace_content(content, next_content, run_time=0.8)

        self.wait_until(cue_start[2] + 0.25)
        traps = VGroup(
            pill("Loop", 1.5, RED_B, "#261116"),
            pill("EOS", 1.4, RED_B, "#261116"),
            pill("Atypical", 2.2, RED_B, "#261116"),
        ).arrange(RIGHT, buff=0.55)
        warning = create_text("MAP failure modes", font_size=26, color=RED_A)
        next_content = VGroup(warning, traps).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[3] + 0.25)
        repetition_crop = slide_visual("slide_26_repetition_crop.png", width=8.6)
        loop_ring = Ellipse(width=3.1, height=0.95, color=RED_A, stroke_width=4)
        loop_ring.move_to(UP * 0.05 + LEFT * 0.6)
        loop_arrow = CurvedArrow(LEFT * 2.15 + DOWN * 1.4, RIGHT * 2.15 + DOWN * 1.4, angle=-TAU / 3, color=RED_A)
        loop_label = create_text("Loop", font_size=22, color=RED_A).next_to(loop_arrow, UP, buff=0.05)
        next_content = Group(repetition_crop, loop_ring, loop_arrow, loop_label)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[4] + 0.2)
        remedies = VGroup(
            pill("Penalty", 2.0, YELLOW, "#211e11"),
            pill("Unlikelihood", 2.9, YELLOW, "#211e11"),
        ).arrange(RIGHT, buff=0.45)
        loop_small = pill("Loop", 1.5, RED_B, "#261116")
        breaker = Line(LEFT * 0.65, RIGHT * 0.65, color=YELLOW, stroke_width=5).rotate(PI / 4)
        breaker.move_to(loop_small)
        next_content = VGroup(loop_small, breaker, remedies).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[5] + 0.2)
        eos = token("<eos>", RED_B, "#261116", width=1.4)
        prompt = token("Taylor Swift is", GRAY_B, "#181a1e", width=2.6)
        early_path = VGroup(prompt.copy(), Arrow(LEFT, RIGHT, color=RED_A), eos).arrange(RIGHT, buff=0.25)
        stop_label = create_text("Early stop", font_size=24, color=RED_A)
        next_content = VGroup(stop_label, early_path).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[6] + 0.25)
        short_path = VGroup(
            token("Taylor Swift is", GRAY_B, "#181a1e", width=2.5),
            token("<eos>", RED_B, "#261116", width=1.2),
        ).arrange(RIGHT, buff=0.25)
        long_path = VGroup(
            token("Taylor Swift is", GRAY_B, "#181a1e", width=2.5),
            token("an", GREEN_B, "#102418", width=0.8),
            token("American", GREEN_B, "#102418", width=1.55),
            token("singer", GREEN_B, "#102418", width=1.2),
        ).arrange(RIGHT, buff=0.18)
        bars = VGroup(
            score_bar("raw score: early EOS", 0.86, RED_A, width=3.4),
            score_bar("raw score: longer answer", 0.46, GREEN_A, width=3.4),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        paths = VGroup(short_path, long_path).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        next_content = VGroup(paths, bars).arrange(RIGHT, buff=0.75).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[7] + 0.25)
        norm = pill("Length normalization", 4.3, YELLOW, "#211e11")
        before = score_bar("raw", 0.86, RED_A, width=3.0)
        after = score_bar("normalized", 0.64, GREEN_A, width=3.0)
        arrow_norm = Arrow(before.get_right(), after.get_left(), color=YELLOW, buff=0.25)
        next_content = VGroup(norm, VGroup(before, arrow_norm, after).arrange(RIGHT, buff=0.35)).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[8] + 0.2)
        atypical = pill("Atypical", 2.3, RED_B, "#261116")
        likely = pill("Most likely", 2.7, YELLOW, "#211e11")
        not_natural = Cross(atypical, stroke_color=RED_A, stroke_width=5)
        next_content = VGroup(likely, Arrow(LEFT, RIGHT, color=GRAY_A), atypical, not_natural).arrange(RIGHT, buff=0.4).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[9] + 0.25)
        coin_crop = slide_visual("slide_26_coin_atypicality_crop.png", width=8.9)
        stamp = create_text("Atypical", font_size=30, color=RED_A).rotate(-0.12)
        stamp_box = SurroundingRectangle(stamp, color=RED_A, buff=0.16, corner_radius=0.04)
        stamp_group = VGroup(stamp_box, stamp).move_to(UP * 1.15 + RIGHT * 2.65)
        content = self.replace_content(content, Group(coin_crop, stamp_group))

        self.wait_until(cue_start[10] + 0.25)
        model = pill("Language model", 3.4, BLUE_B, "#111a25")
        output = pill("Unnatural output", 3.5, RED_B, "#261116")
        next_content = VGroup(model, Arrow(LEFT, RIGHT, color=RED_A), output).arrange(RIGHT, buff=0.45).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[11] + 0.25)
        exact = pill("Exact MAP", 2.5, RED_B, "#261116")
        narrow = pill("Narrow beam", 2.8, BLUE_B, "#111a25")
        better = create_text("Works better", font_size=22, color=GREEN_A)
        next_content = VGroup(exact, Arrow(LEFT, RIGHT, color=BLUE_A), VGroup(narrow, better).arrange(DOWN, buff=0.18)).arrange(RIGHT, buff=0.55).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[12] + 0.25)
        likely_best = VGroup(
            pill("most likely", 2.7, YELLOW, "#211e11"),
            create_text("≠", font_size=34, color=GRAY_A),
            pill("best", 1.5, GREEN_B, "#102418"),
        ).arrange(RIGHT, buff=0.45).move_to(ORIGIN)
        content = self.replace_content(content, likely_best)

        self.wait_until(cue_start[13] + 0.25)
        box = RoundedRectangle(width=4.8, height=1.7, corner_radius=0.08, color=BLUE_C, fill_color="#101722", fill_opacity=0.85)
        constrained = VGroup(
            token("A", BLUE_B, "#111a25", width=0.8),
            token("B", BLUE_B, "#111a25", width=0.8),
            token("C", BLUE_B, "#111a25", width=0.8),
        ).arrange(RIGHT, buff=0.3)
        label = create_text("Closed-ended", font_size=22, color=BLUE_A).next_to(box, UP, buff=0.18)
        constrained.move_to(box)
        content = self.replace_content(content, VGroup(box, constrained, label))

        self.wait_until(cue_start[14] + 0.25)
        open_tokens = VGroup(
            token("loop", RED_B, "#261116", width=1.2),
            token("<eos>", RED_B, "#261116", width=1.2),
            token("atypical", RED_B, "#261116", width=1.7),
        ).arrange(RIGHT, buff=0.35)
        funnel = Polygon(LEFT * 2.6 + UP * 1.0, RIGHT * 2.6 + UP * 1.0, RIGHT * 0.9 + DOWN * 0.6, LEFT * 0.9 + DOWN * 0.6, color=RED_A)
        funnel.set_fill("#261116", opacity=0.35)
        open_label = create_text("Open-ended", font_size=23, color=RED_A).next_to(funnel, UP, buff=0.2)
        open_tokens.move_to(funnel.get_center() + DOWN * 0.05)
        content = self.replace_content(content, VGroup(funnel, open_tokens, open_label))

        self.wait_until(cue_start[15] + 0.2)
        sampling = pill("Sampling", 2.4, GREEN_B, "#102418", font_size=23)
        particles = VGroup(*[Dot(radius=0.045, color=GREEN_A).shift(RIGHT * (i * 0.28 - 0.7) + UP * ((i % 3) * 0.18 - 0.18)) for i in range(6)])
        particles.next_to(sampling, RIGHT, buff=0.35)
        next_content = VGroup(sampling, particles).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(voiceover_end + 0.35)
        self.play(FadeOut(content), FadeOut(header), run_time=0.8)
