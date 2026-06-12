import os
import tempfile
from pathlib import Path

from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"
ASSET_DIR = Path(__file__).resolve().parent / "assets"

VOICEOVERS = [
    ("sc22_001.mp3", 3.900952),
    ("sc22_002.mp3", 4.551111),
    ("sc22_003.mp3", 3.900952),
    ("sc22_004.mp3", 5.154830),
    ("sc22_005.mp3", 5.665669),
    ("sc22_006.mp3", 7.894785),
    ("sc22_007.mp3", 8.962902),
    ("sc22_008.mp3", 3.250794),
    ("sc22_009.mp3", 5.758549),
    ("sc22_010.mp3", 8.080544),
    ("sc22_011.mp3", 14.535692),
    ("sc22_012.mp3", 7.476825),
    ("sc22_013.mp3", 5.572789),
    ("sc22_014.mp3", 5.433469),
    ("sc22_015.mp3", 9.891701),
    ("sc22_016.mp3", 4.133152),
    ("sc22_017.mp3", 8.730703),
    ("sc22_018.mp3", 6.780227),
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


def labeled_box(text, width, height=0.5, color=BLUE_B, fill="#181a1e", font_size=18):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.06,
        color=color,
        fill_color=fill,
        fill_opacity=0.9,
        stroke_width=1.6,
    )
    label = create_text(text, font_size=font_size, color=WHITE)
    label.move_to(box.get_center())
    return VGroup(box, label)


def slide_visual(filename, width=7.3):
    image = ImageMobject(str(ASSET_DIR / filename))
    image.scale_to_fit_width(width)
    source = create_text("https://neurips.cc/virtual/2024/tutorial/99522", font_size=14, color=GRAY_A)
    source.next_to(image, DOWN, buff=0.12)
    return Group(image, source).move_to(ORIGIN).shift(DOWN * 0.15)


class Scene2_2(MovingCameraScene):
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
            raise FileNotFoundError("Missing scene 2.2 voiceover files:\n" + "\n".join(missing))

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

        title = create_text("Optimization in Decoding", font_size=30, color=BLUE_A)
        subtitle = create_text("MAP, Greedy Decoding, and Beam Search", font_size=18, color=GRAY_A)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.18)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.8)

        content = None

        # 001-003: MAP objective and the two optimization algorithms.
        self.wait_until(cue_start[1] + 0.5)
        map_formula = create_markup_text(
            "<span color='#ebcb8b'>argmax<sub><i>x</i></sub></span> "
            "<span color='#8fbcbb'><i>p</i><sub><i>θ</i></sub>(<i>x</i>)</span>",
            font_size=34,
        )
        map_caption = create_text("MAP decoding searches for the highest-probability sequence", font_size=22, color=WHITE)
        content = VGroup(map_formula, map_caption).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(content, shift=UP * 0.15), run_time=0.8)

        self.wait_until(cue_start[2] + 0.35)
        chooses_text = create_text("Choose the sequence the model assigns the largest probability to", font_size=22, color=BLUE_A)
        chooses_text.next_to(map_formula, DOWN, buff=0.5)
        self.play(ReplacementTransform(map_caption, chooses_text), run_time=0.55)
        content = VGroup(map_formula, chooses_text)

        self.wait_until(cue_start[3] + 0.25)
        greedy_card = labeled_box("Greedy decoding", 3.0, color=BLUE_B, fill="#111a25", font_size=20)
        beam_card = labeled_box("Beam search", 2.6, color=YELLOW, fill="#211e11", font_size=20)
        algorithm_cards = VGroup(greedy_card, beam_card).arrange(RIGHT, buff=0.8)
        algorithm_label = create_text("Two common optimization algorithms", font_size=22, color=GRAY_A)
        next_content = VGroup(algorithm_label, algorithm_cards).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        # 004-007: Greedy makes local choices and can miss MAP.
        self.wait_until(cue_start[4] + 0.2)
        greedy_formula = create_markup_text(
            "<i>x</i><sub><i>t</i></sub> = "
            "<span color='#ebcb8b'>argmax<sub><i>w</i></sub></span> "
            "<i>p</i><sub><i>θ</i></sub>(<i>w</i> | <i>x</i><sub>&lt;<i>t</i></sub>)",
            font_size=30,
        )
        greedy_note = create_text("Highest-probability token at each step", font_size=22, color=BLUE_A)
        next_content = VGroup(greedy_formula, greedy_note).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[5] + 0.25)
        next_content = slide_visual("slide_23_greedy_table_crop.png", width=10.0)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[6] + 0.25)
        prompt = labeled_box("Taylor Swift is", 2.6, color=GRAY_B, font_size=18)
        an = labeled_box('"an"', 1.0, color=RED_B, fill="#281719", font_size=18)
        american = labeled_box('"American"', 1.7, color=RED_B, fill="#281719", font_size=16)
        an_score = create_text("0.80 -> 0.016 cumulative", font_size=18, color=RED_A)
        greedy_path = VGroup(an, american).arrange(DOWN, buff=0.45)
        greedy_path.next_to(prompt, DOWN, buff=0.55)
        an_score.next_to(greedy_path, RIGHT, buff=0.55)
        local_label = create_text("Greedy starts with the locally best token", font_size=22, color=RED_A)
        tree_1 = VGroup(prompt, greedy_path, an_score, local_label)
        local_label.next_to(tree_1, DOWN, buff=0.45)
        tree_1.move_to(ORIGIN)
        content = self.replace_content(content, tree_1)

        self.wait_until(cue_start[7] + 0.25)
        a = labeled_box('"a"', 1.0, color=GREEN_B, fill="#102418", font_size=18)
        singer = labeled_box('"singer"', 1.5, color=GREEN_B, fill="#102418", font_size=16)
        songwriter = labeled_box('"songwriter"', 2.0, color=GREEN_B, fill="#102418", font_size=15)
        non_greedy_path = VGroup(a, singer, songwriter).arrange(DOWN, buff=0.35)
        non_greedy_score = create_text("0.13 -> 0.117 / 0.104 cumulative", font_size=18, color=GREEN_A)
        non_greedy_label = create_text("A lower first token can lead to a better sequence", font_size=22, color=GREEN_A)
        comparison = VGroup(
            VGroup(greedy_path.copy(), an_score.copy()).arrange(RIGHT, buff=0.4),
            VGroup(non_greedy_path, non_greedy_score).arrange(RIGHT, buff=0.45),
            non_greedy_label,
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        content = self.replace_content(content, comparison)

        # 008-013: Beam search keeps a finite beam and prunes by cumulative score.
        self.wait_until(cue_start[8] + 0.2)
        next_content = slide_visual("slide_24_beam_graph_crop.png", width=6.9)
        content = self.replace_content(content, next_content)

        self.wait_until(cue_start[9] + 0.25)
        keep = labeled_box("Keep top K branches", 3.3, color=YELLOW, fill="#211e11", font_size=18)
        expand = labeled_box("Expand them", 2.4, color=BLUE_B, fill="#111a25", font_size=18)
        arrow = Arrow(keep.get_right(), expand.get_left(), buff=0.25, color=GRAY_A)
        beam_loop = VGroup(keep, arrow, expand).arrange(RIGHT, buff=0.55).move_to(ORIGIN)
        beam_loop_label = create_text("Beam size K controls the number of active branches", font_size=21, color=GRAY_A)
        beam_loop_label.next_to(beam_loop, DOWN, buff=0.45)
        content = self.replace_content(content, VGroup(beam_loop, beam_loop_label))

        self.wait_until(cue_start[10] + 0.25)
        step1_rows = VGroup(
            create_text('Step 1, K = 2', font_size=24, color=YELLOW),
            create_text('"an"   0.80   keep', font_size=21, color=YELLOW),
            create_text('"a"    0.13   keep', font_size=21, color=YELLOW),
            create_text('"the"  0.06   prune', font_size=21, color=GRAY_B),
            create_text('"to"   0.0004 prune', font_size=21, color=GRAY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(ORIGIN)
        content = self.replace_content(content, step1_rows)

        self.wait_until(cue_start[11] + 0.25)
        step2_rows = VGroup(
            create_text("Step 2 cumulative scores", font_size=24, color=YELLOW),
            create_text('"a singer"       0.117', font_size=21, color=GREEN_A),
            create_text('"a songwriter"   0.104', font_size=21, color=GREEN_A),
            create_text('"an American"    0.016', font_size=21, color=RED_A),
            create_text('"an artist"      0.008', font_size=21, color=RED_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(ORIGIN)
        content = self.replace_content(content, step2_rows)

        self.wait_until(cue_start[12] + 0.25)
        keep_rows = VGroup(
            create_text('Keep: "a singer" and "a songwriter"', font_size=24, color=GREEN_A),
            create_text('Prune: "an American"', font_size=24, color=RED_A),
            create_text("The branch that started with the greedy token is removed", font_size=21, color=GRAY_A),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        content = self.replace_content(content, keep_rows)

        self.wait_until(cue_start[13] + 0.25)
        k1_note = VGroup(
            create_text("When K = 1", font_size=30, color=YELLOW),
            create_text("Beam search is exactly greedy decoding", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        content = self.replace_content(content, k1_note)

        # 014-018: Closing comparison.
        self.wait_until(cue_start[14] + 0.2)
        greedy_summary = VGroup(
            create_text("Greedy decoding", font_size=28, color=BLUE_A),
            create_text("Local choice: best token right now", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        content = self.replace_content(content, greedy_summary)

        self.wait_until(cue_start[15] + 0.25)
        greedy_tradeoff = VGroup(
            create_text("Simple and cheap", font_size=26, color=BLUE_A),
            create_text("But not guaranteed globally optimal", font_size=24, color=RED_A),
            create_text("A better sequence may begin with a weaker first token", font_size=21, color=GRAY_A),
        ).arrange(DOWN, buff=0.32).move_to(ORIGIN)
        content = self.replace_content(content, greedy_tradeoff)

        self.wait_until(cue_start[16] + 0.2)
        search_scale = VGroup(
            labeled_box("Greedy", 1.9, color=BLUE_B, fill="#111a25", font_size=18),
            labeled_box("Beam search", 2.6, color=YELLOW, fill="#211e11", font_size=18),
            labeled_box("Exhaustive", 2.3, color=RED_B, fill="#281719", font_size=18),
        ).arrange(RIGHT, buff=0.45).move_to(ORIGIN)
        search_label = create_text("Beam search sits between greedy and exhaustive search", font_size=22, color=GRAY_A)
        search_label.next_to(search_scale, DOWN, buff=0.45)
        content = self.replace_content(content, VGroup(search_scale, search_label))

        self.wait_until(cue_start[17] + 0.25)
        exhaustive_note = VGroup(
            create_text("Exhaustive search expands too many possibilities", font_size=25, color=RED_A),
            create_text("Language-model vocabularies can have tens or hundreds of thousands of tokens", font_size=20, color=GRAY_A),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        content = self.replace_content(content, exhaustive_note)

        self.wait_until(cue_start[18] + 0.25)
        final_note = VGroup(
            create_text("Beam search keeps a finite beam", font_size=28, color=YELLOW),
            create_text("More branches than greedy, with cost controlled by K", font_size=23, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        content = self.replace_content(content, final_note)

        self.wait_until(voiceover_end + 0.35)
        self.play(FadeOut(content), FadeOut(header), run_time=0.8)
