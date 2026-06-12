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

SCENE_2_4_DURATIONS = {
    "sc24_001.mp3": 2.182676,
    "sc24_002.mp3": 9.427302,
    "sc24_003.mp3": 4.226032,
    "sc24_004.mp3": 10.959819,
    "sc24_005.mp3": 3.111474,
    "sc24_006.mp3": 3.761633,
    "sc24_007.mp3": 6.315828,
    "sc24_008.mp3": 6.965986,
    "sc24_009.mp3": 1.718277,
    "sc24_010.mp3": 5.572789,
    "sc24_011.mp3": 6.548027,
    "sc24_012.mp3": 5.201270,
    "sc24_013.mp3": 2.925714,
    "sc24_014.mp3": 21.548118,
    "sc24_015.mp3": 7.569705,
    "sc24_016.mp3": 3.575873,
    "sc24_017.mp3": 6.919546,
    "sc24_018.mp3": 5.665669,
    "sc24_019.mp3": 2.925714,
    "sc24_020.mp3": 2.182676,
    "sc24_021.mp3": 9.148662,
}
SCENE_2_4_VOICEOVERS = tuple(SCENE_2_4_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc24_*.mp3"))
    expected = sorted(SCENE_2_4_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 2.4 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_2_4_DURATIONS:
        raise KeyError(f"Unexpected Scene 2.4 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 2.4 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_2_4_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_2_4_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 2.4 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


def create_text(text, font_size=24, font="Noto Sans", color=WHITE, **kwargs):
    if font_size < 20:
        item = Text(text, font_size=36, font=font, color=color, **kwargs)
        item.scale(font_size / 36)
        return item
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)


def pill(text, width, color=BLUE_B, fill="#111a25", font_size=20):
    box = RoundedRectangle(
        width=width,
        height=0.62,
        corner_radius=0.08,
        color=color,
        fill_color=fill,
        fill_opacity=0.9,
        stroke_width=1.7,
    )
    label = create_text(text, font_size=font_size)
    label.move_to(box)
    return VGroup(box, label)


def token(text, color=BLUE_B, fill="#111a25", width=None):
    width = width or max(0.9, 0.22 * len(text) + 0.5)
    box = RoundedRectangle(
        width=width,
        height=0.48,
        corner_radius=0.06,
        color=color,
        fill_color=fill,
        fill_opacity=0.95,
        stroke_width=1.4,
    )
    label = create_text(text, font_size=18)
    label.move_to(box)
    return VGroup(box, label)


class CustomBarChart(VGroup):
    def __init__(self, probs, labels, colors=None, width=7, height=3, y_max=1.0, **kwargs):
        super().__init__(**kwargs)
        self.probs = probs
        self.labels = labels
        self.y_max = y_max
        self.chart_width = width
        self.chart_height = height
        
        self.baseline = Line(
            LEFT * (width / 2),
            RIGHT * (width / 2),
            color=GRAY_D,
            stroke_width=1.5
        )
        self.add(self.baseline)
        
        self.num_bars = len(probs)
        self.bar_width = (width / self.num_bars) * 0.7
        self.gap = (width / self.num_bars) * 0.3
        
        self.bars = VGroup()
        self.label_mobjects = VGroup()
        
        for i, p in enumerate(probs):
            bar_height = (p / y_max) * height
            bar_height = max(bar_height, 0.02)
            
            if colors is None:
                color = BLUE_B
            elif isinstance(colors, list):
                color = colors[i]
            else:
                color = colors
                
            bar = Rectangle(
                width=self.bar_width,
                height=bar_height,
                color=color,
                fill_color=color,
                fill_opacity=0.85,
                stroke_width=1.0
            )
            x_pos = -width / 2 + i * (self.bar_width + self.gap) + self.bar_width / 2 + self.gap / 2
            bar.move_to([self.baseline.get_x() + x_pos, 0, 0])
            bar.align_to(self.baseline, DOWN)
            self.bars.add(bar)
            
            if i < len(labels):
                lbl = create_text(labels[i], font_size=15, color=GRAY_A)
                lbl.next_to(bar, DOWN, buff=0.15)
                self.label_mobjects.add(lbl)
                
        self.add(self.bars, self.label_mobjects)
        
    def update_chart(self, new_probs, new_labels, colors=None):
        target_bars = VGroup()
        target_labels = VGroup()
        
        for i, p in enumerate(new_probs):
            bar_height = (p / self.y_max) * self.chart_height
            bar_height = max(bar_height, 0.02)
            
            if colors is None:
                color = self.bars[i].get_color()
            elif isinstance(colors, list):
                color = colors[i]
            else:
                color = colors
                
            new_bar = Rectangle(
                width=self.bar_width,
                height=bar_height,
                color=color,
                fill_color=color,
                fill_opacity=0.85,
                stroke_width=1.0
            )
            x_pos = self.bars[i].get_x()
            new_bar.move_to([x_pos, 0, 0])
            new_bar.align_to(self.baseline, DOWN)
            target_bars.add(new_bar)
            
            if i < len(new_labels):
                lbl = create_text(new_labels[i], font_size=15, color=GRAY_A)
                lbl.next_to(new_bar, DOWN, buff=0.15)
                target_labels.add(lbl)
                
        self.probs = new_probs
        self.labels = new_labels
        
        return [Transform(self.bars, target_bars), Transform(self.label_mobjects, target_labels)]


class Scene2_4(MovingCameraScene):

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
        for idx, (filename, duration) in enumerate(SCENE_2_4_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        title = create_text("Sampling & Truncation", font_size=32, color=YELLOW)
        subtitle = create_text("Temperature changes sharpness; truncation changes support", font_size=17, color=GRAY_A)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.18)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.8)

        content = None

        # --- Cue 1: Intro ---
        self.wait_until(cue_start[1] + 0.25)
        objective = VGroup(
            pill("Objective", 2.2, YELLOW, "#211e11"),
            Arrow(LEFT, RIGHT, color=YELLOW),
            pill("Sampling", 2.2, GREEN_B, "#102418")
        ).arrange(RIGHT, buff=0.35).move_to(ORIGIN)
        content = self.replace_content(content, objective)

        # --- Cue 2: Ancestral Sampling Intro with Custom BarChart ---
        self.wait_until(cue_start[2] + 0.25)
        vocab = ["the", "cat", "sat", "on", "mat", "banana", "galaxy", "elephant"]
        probs = [0.35, 0.25, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01]
        colors = [BLUE_B] * 5 + [BLUE_E] * 3
        
        chart = CustomBarChart(probs, vocab, colors=colors, width=8, height=3)
        chart.move_to(DOWN * 0.5)
        
        # Selector arrow pointing down
        selector = Arrow(UP, DOWN, color=YELLOW, stroke_width=4).scale(0.35)
        selector.next_to(chart.bars[0], UP, buff=0.2)
        
        chart_group = VGroup(chart, selector)
        content = self.replace_content(content, chart_group)
        
        # Scan selector over bars and land on "cat" (index 1)
        self.play(selector.animate.next_to(chart.bars[0], UP, buff=0.2), run_time=0.2)
        self.play(selector.animate.next_to(chart.bars[1], UP, buff=0.2), run_time=0.2)
        self.play(selector.animate.next_to(chart.bars[2], UP, buff=0.2), run_time=0.2)
        self.play(selector.animate.next_to(chart.bars[1], UP, buff=0.2), run_time=0.2)
        
        self.play(chart.bars[1].animate.set_color(YELLOW), run_time=0.3)

        # --- Cue 3: Sequence Sampling Loop ---
        self.wait_until(cue_start[3] + 0.2)
        seq_text = VGroup(
            create_text("Sequence:", font_size=20, color=GRAY_A),
            token("cat", color=YELLOW)
        ).arrange(RIGHT, buff=0.2).move_to(UP * 1.5)
        
        self.play(
            FadeIn(seq_text),
            chart.bars[1].animate.set_color(BLUE_B),
            run_time=0.4
        )
        
        # Next token: "sat"
        probs_2 = [0.40, 0.20, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01]
        vocab_2 = ["sat", "on", "is", "and", "mat", "banana", "galaxy", "elephant"]
        
        self.play(*chart.update_chart(probs_2, vocab_2, colors=[BLUE_B]*5 + [BLUE_E]*3), run_time=0.5)
        self.play(selector.animate.next_to(chart.bars[0], UP, buff=0.2), run_time=0.3)
        self.play(chart.bars[0].animate.set_color(YELLOW), run_time=0.2)
        
        sat_token = token("sat", color=YELLOW)
        sat_token.next_to(seq_text[-1], RIGHT, buff=0.2)
        seq_text.add(sat_token)
        self.play(FadeIn(sat_token), run_time=0.3)
        
        # Next token: "on"
        probs_3 = [0.30, 0.25, 0.20, 0.12, 0.07, 0.03, 0.02, 0.01]
        vocab_3 = ["on", "mat", "in", "and", "banana", "galaxy", "the", "elephant"]
        
        self.play(
            *chart.update_chart(probs_3, vocab_3, colors=[BLUE_B]*5 + [BLUE_E]*3),
            chart.bars[0].animate.set_color(BLUE_B),
            run_time=0.5
        )
        self.play(selector.animate.next_to(chart.bars[0], UP, buff=0.2), run_time=0.3)
        self.play(chart.bars[0].animate.set_color(YELLOW), run_time=0.2)
        
        on_token = token("on", color=YELLOW)
        on_token.next_to(seq_text[-1], RIGHT, buff=0.2)
        seq_text.add(on_token)
        self.play(FadeIn(on_token), run_time=0.3)

        # --- Cue 4: Greedy vs Ancestral Incoherence ---
        self.wait_until(cue_start[4] + 0.25)
        self.play(
            FadeOut(chart_group),
            FadeOut(seq_text),
            run_time=0.5
        )
        
        # Left Panel: Greedy Repetition Trap
        greedy_title = create_text("Greedy Decoding", font_size=20, color=RED_B)
        greedy_seq = VGroup(
            token("cat", RED_B), Arrow(LEFT, RIGHT, color=RED_B, stroke_width=2).scale(0.35),
            token("sat", RED_B), Arrow(LEFT, RIGHT, color=RED_B, stroke_width=2).scale(0.35),
            token("cat", RED_B), Arrow(LEFT, RIGHT, color=RED_B, stroke_width=2).scale(0.35),
            create_text("...", font_size=20, color=RED_B)
        ).arrange(RIGHT, buff=0.1)
        greedy_label = create_text("Repetition Trap!", font_size=16, color=RED_A)
        greedy_panel = VGroup(greedy_title, greedy_seq, greedy_label).arrange(DOWN, buff=0.3)
        greedy_panel.shift(LEFT * 3.4 + DOWN * 0.6)
        
        # Right Panel: Ancestral Incoherence (Heavy Tail)
        ancestral_title = create_text("Ancestral Sampling", font_size=20, color=ORANGE)
        
        mini_chart = CustomBarChart(
            probs=[0.35, 0.25, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01],
            labels=["the", "cat", "sat", "", "", "", "galaxy", ""],
            colors=[BLUE_B]*5 + [RED_B]*3,
            width=4.5,
            height=1.8
        )
        
        ancestral_seq = VGroup(
            token("cat", BLUE_B), Arrow(LEFT, RIGHT, color=BLUE_A, stroke_width=2).scale(0.35),
            token("sat", BLUE_B), Arrow(LEFT, RIGHT, color=BLUE_A, stroke_width=2).scale(0.35),
            token("galaxy", RED_B)
        ).arrange(RIGHT, buff=0.1)
        
        ancestral_label = create_text("Incoherent! (Landed on tail)", font_size=16, color=RED_A)
        ancestral_panel = VGroup(ancestral_title, ancestral_seq, mini_chart, ancestral_label).arrange(DOWN, buff=0.35)
        ancestral_panel.shift(RIGHT * 3.4 + DOWN * 0.6)
        
        self.play(
            FadeIn(greedy_panel, shift=UP * 0.15),
            FadeIn(ancestral_panel, shift=UP * 0.15),
            run_time=0.8
        )
        
        # Land on tail token
        mini_selector = Arrow(UP, DOWN, color=YELLOW, stroke_width=3).scale(0.25)
        mini_selector.next_to(mini_chart.bars[0], UP, buff=0.15)
        self.play(FadeIn(mini_selector), run_time=0.2)
        self.play(mini_selector.animate.next_to(mini_chart.bars[6], UP, buff=0.15), run_time=0.4)
        
        self.play(
            mini_chart.bars[6].animate.set_color(YELLOW),
            ancestral_seq[-1].animate.set_color(YELLOW),
            run_time=0.3
        )

        # --- Cue 5-6: Chop off the tail (Truncation) ---
        self.wait_until(cue_start[5] + 0.15)
        self.play(
            FadeOut(greedy_panel),
            FadeOut(ancestral_panel),
            FadeOut(mini_selector),
            run_time=0.5
        )
        
        # Redraw main chart
        chart = CustomBarChart(probs, vocab, colors=[BLUE_B]*8, width=8, height=3)
        chart.move_to(DOWN * 0.5)
        self.play(FadeIn(chart), run_time=0.5)
        
        # Truncation wall
        self.wait_until(cue_start[6] + 0.2)
        wall_x = chart.bars[4].get_right()[0] + 0.12
        wall = Line(
            [wall_x, chart.baseline.get_y() - 0.4, 0],
            [wall_x, chart.baseline.get_y() + 3.0, 0],
            color=RED,
            stroke_width=3
        )
        wall_label = create_text("Cutoff Gate", font_size=14, color=RED).next_to(wall, UP, buff=0.1)
        
        self.play(
            Create(wall),
            FadeIn(wall_label),
            run_time=0.6
        )
        
        # Apply truncation (fade tail to grey and renormalize)
        renormalized_probs = [0.38, 0.27, 0.16, 0.11, 0.08, 0.0, 0.0, 0.0]
        renorm_colors = [BLUE_B]*5 + [GRAY_E]*3
        
        self.play(
            *chart.update_chart(renormalized_probs, vocab, colors=renorm_colors),
            run_time=0.8
        )

        # --- Cue 7: Truncation Variants ---
        self.wait_until(cue_start[7] + 0.2)
        self.play(
            FadeOut(chart),
            FadeOut(wall),
            FadeOut(wall_label),
            run_time=0.5
        )
        
        variants = VGroup(
            pill("Top-k", 1.6, BLUE_B, "#111a25"),
            pill("Top-p", 1.6, BLUE_B, "#111a25"),
            pill("Epsilon", 1.9, BLUE_B, "#111a25"),
            pill("Eta", 1.3, BLUE_B, "#111a25"),
            pill("Min-p", 1.6, BLUE_B, "#111a25"),
        ).arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        
        self.play(FadeIn(variants), run_time=0.6)
        
        self.play(
            variants[0][0].animate.set_color(YELLOW),
            variants[1][0].animate.set_color(GREEN_B),
            run_time=0.5
        )

        # --- Cue 8: Top-k vs Top-p detailed comparison ---
        self.wait_until(cue_start[8] + 0.25)
        self.play(FadeOut(variants), run_time=0.5)
        
        topk_title = create_text("Top-k (k=4)", font_size=20, color=YELLOW)
        topk_title.move_to(LEFT * 3.5 + UP * 1.6)
        
        topp_title = create_text("Top-p (p=0.90)", font_size=20, color=GREEN_B)
        topp_title.move_to(RIGHT * 3.5 + UP * 1.6)
        
        # Peaked Shape
        vocab_peaked = ["A", "B", "C", "D", "E", "F", "G", "H"]
        probs_peaked = [0.85, 0.08, 0.04, 0.02, 0.01, 0.0, 0.0, 0.0]
        
        chart_k = CustomBarChart(probs_peaked, vocab_peaked, colors=[BLUE_B]*8, width=5, height=2.2)
        chart_k.move_to(LEFT * 3.5 + DOWN * 0.5)
        
        chart_p = CustomBarChart(probs_peaked, vocab_peaked, colors=[BLUE_B]*8, width=5, height=2.2)
        chart_p.move_to(RIGHT * 3.5 + DOWN * 0.5)
        
        self.play(
            FadeIn(topk_title),
            FadeIn(topp_title),
            FadeIn(chart_k),
            FadeIn(chart_p),
            run_time=0.6
        )
        
        # Top-k Wall (k=4)
        wall_k_x = chart_k.bars[3].get_right()[0] + 0.08
        wall_k = Line([wall_k_x, chart_k.baseline.get_y() - 0.2, 0], [wall_k_x, chart_k.baseline.get_y() + 2.2, 0], color=YELLOW, stroke_width=2.5)
        wall_k_lbl = create_text("k=4", font_size=12, color=YELLOW).next_to(wall_k, UP, buff=0.08)
        
        # Top-p Wall (A=0.85 + B=0.08 = 0.93 >= 0.90) => cut at 2nd token
        wall_p_x = chart_p.bars[1].get_right()[0] + 0.08
        wall_p = Line([wall_p_x, chart_p.baseline.get_y() - 0.2, 0], [wall_p_x, chart_p.baseline.get_y() + 2.2, 0], color=GREEN_B, stroke_width=2.5)
        wall_p_lbl = create_text("p=0.90", font_size=12, color=GREEN_B).next_to(wall_p, UP, buff=0.08)
        
        self.play(
            Create(wall_k), FadeIn(wall_k_lbl),
            Create(wall_p), FadeIn(wall_p_lbl),
            run_time=0.6
        )
        
        probs_k_cut = [0.85/0.99, 0.08/0.99, 0.04/0.99, 0.02/0.99, 0, 0, 0, 0]
        probs_p_cut = [0.85/0.93, 0.08/0.93, 0, 0, 0, 0, 0, 0]
        
        self.play(
            *chart_k.update_chart(probs_k_cut, vocab_peaked, colors=[BLUE_B]*4 + [GRAY_E]*4),
            *chart_p.update_chart(probs_p_cut, vocab_peaked, colors=[BLUE_B]*2 + [GRAY_E]*6),
            run_time=0.8
        )
        
        self.wait(1.0)
        
        # Morph both to Flat Distribution
        probs_flat = [0.20, 0.18, 0.15, 0.14, 0.12, 0.10, 0.07, 0.04]
        
        self.play(
            FadeOut(wall_k), FadeOut(wall_k_lbl),
            FadeOut(wall_p), FadeOut(wall_p_lbl),
            run_time=0.3
        )
        
        self.play(
            *chart_k.update_chart(probs_flat, vocab_peaked, colors=[BLUE_B]*8),
            *chart_p.update_chart(probs_flat, vocab_peaked, colors=[BLUE_B]*8),
            run_time=0.8
        )
        
        # Top-k Wall is still k=4.
        wall_k_x = chart_k.bars[3].get_right()[0] + 0.08
        wall_k = Line([wall_k_x, chart_k.baseline.get_y() - 0.2, 0], [wall_k_x, chart_k.baseline.get_y() + 2.2, 0], color=YELLOW, stroke_width=2.5)
        wall_k_lbl = create_text("k=4", font_size=12, color=YELLOW).next_to(wall_k, UP, buff=0.08)
        
        # Top-p Wall is now at index 7 (sum of first 7 = 0.96 >= 0.90)
        wall_p_x = chart_p.bars[6].get_right()[0] + 0.08
        wall_p = Line([wall_p_x, chart_p.baseline.get_y() - 0.2, 0], [wall_p_x, chart_p.baseline.get_y() + 2.2, 0], color=GREEN_B, stroke_width=2.5)
        wall_p_lbl = create_text("p=0.90", font_size=12, color=GREEN_B).next_to(wall_p, UP, buff=0.08)
        
        self.play(
            Create(wall_k), FadeIn(wall_k_lbl),
            Create(wall_p), FadeIn(wall_p_lbl),
            run_time=0.6
        )
        
        probs_k_cut_flat = [0.20/0.67, 0.18/0.67, 0.15/0.67, 0.14/0.67, 0, 0, 0, 0]
        probs_p_cut_flat = [0.20/0.96, 0.18/0.96, 0.15/0.96, 0.14/0.96, 0.12/0.96, 0.10/0.96, 0.07/0.96, 0]
        
        self.play(
            *chart_k.update_chart(probs_k_cut_flat, vocab_peaked, colors=[BLUE_B]*4 + [GRAY_E]*4),
            *chart_p.update_chart(probs_p_cut_flat, vocab_peaked, colors=[BLUE_B]*7 + [GRAY_E]*1),
            run_time=0.8
        )

        # --- Cue 9: Temperature Introduction ---
        self.wait_until(cue_start[9] + 0.25)
        self.play(
            FadeOut(topk_title), FadeOut(topp_title),
            FadeOut(chart_k), FadeOut(chart_p),
            FadeOut(wall_k), FadeOut(wall_k_lbl),
            FadeOut(wall_p), FadeOut(wall_p_lbl),
            run_time=0.5
        )
        
        temp_title = pill("Temperature Scaling", 3.2, YELLOW, "#211e11", font_size=22)
        temp_title.move_to(UP * 1.6)
        
        vocab = ["A", "B", "C", "D", "E", "F", "G", "H"]
        probs_norm = [0.35, 0.25, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01]
        chart = CustomBarChart(probs_norm, vocab, colors=[BLUE_B]*8, width=7, height=2.5)
        chart.move_to(DOWN * 0.5)
        
        # Interactive temperature slider
        slider_line = Line(LEFT * 2, RIGHT * 2, color=GRAY_C, stroke_width=2.5)
        slider_line.next_to(chart, DOWN, buff=0.4)
        slider_label = create_text("Temperature (tau)", font_size=14, color=GRAY_A).next_to(slider_line, LEFT, buff=0.2)
        slider_knob = Dot(color=YELLOW).move_to(slider_line.get_center())
        slider_val = create_text("1.0", font_size=14, color=YELLOW).next_to(slider_line, RIGHT, buff=0.2)
        slider = VGroup(slider_line, slider_label, slider_knob, slider_val)
        
        self.play(
            FadeIn(temp_title),
            FadeIn(chart),
            FadeIn(slider),
            run_time=0.6
        )

        # --- Cue 10-12: High vs Low Temperature ---
        self.wait_until(cue_start[10] + 0.2)
        
        # Slide knob left (tau = 0.5)
        low_knob_pos = slider_line.get_left() + RIGHT * 0.8
        low_val_text = create_text("0.5", font_size=14, color=YELLOW).move_to(slider_val)
        probs_low = [0.54, 0.28, 0.10, 0.04, 0.03, 0.01, 0.00, 0.00]
        
        self.play(
            slider_knob.animate.move_to(low_knob_pos),
            Transform(slider_val, low_val_text),
            *chart.update_chart(probs_low, vocab, colors=[BLUE_B]*8),
            run_time=1.0
        )
        
        low_lbl = create_text("Sharp / Peaked (Coherent but repetitive)", font_size=16, color=BLUE_A)
        low_lbl.next_to(temp_title, DOWN, buff=0.15)
        self.play(FadeIn(low_lbl), run_time=0.4)
        
        self.wait_until(cue_start[11] + 0.2)
        self.play(FadeOut(low_lbl), run_time=0.2)
        
        # Slide knob right (tau = 1.5)
        high_knob_pos = slider_line.get_right() - LEFT * 0.8
        high_val_text = create_text("1.5", font_size=14, color=YELLOW).move_to(slider_val)
        probs_high = [0.23, 0.20, 0.15, 0.13, 0.11, 0.08, 0.06, 0.04]
        
        self.play(
            slider_knob.animate.move_to(high_knob_pos),
            Transform(slider_val, high_val_text),
            *chart.update_chart(probs_high, vocab, colors=[BLUE_B]*8),
            run_time=1.0
        )
        
        high_lbl = create_text("Flat / Uniform (Diverse but incoherent)", font_size=16, color=YELLOW)
        high_lbl.next_to(temp_title, DOWN, buff=0.15)
        self.play(FadeIn(high_lbl), run_time=0.4)
        
        self.wait_until(cue_start[12] + 0.2)
        self.play(FadeOut(high_lbl), run_time=0.2)
        
        # Reset to tau = 1.0
        norm_val_text = create_text("1.0", font_size=14, color=YELLOW).move_to(slider_val)
        self.play(
            slider_knob.animate.move_to(slider_line.get_center()),
            Transform(slider_val, norm_val_text),
            *chart.update_chart(probs_norm, vocab, colors=[BLUE_B]*8),
            run_time=0.8
        )

        # --- Cue 13: Pipeline Map ---
        self.wait_until(cue_start[13] + 0.2)
        self.play(
            FadeOut(temp_title),
            FadeOut(chart),
            FadeOut(slider),
            run_time=0.5
        )
        
        pipe_title = create_text("Generation Pipeline", font_size=22, color=YELLOW).move_to(UP * 1.6)
        
        p1 = token("Logits", color=GRAY_B)
        p2 = token("Temperature", color=YELLOW)
        p3 = token("Truncation", color=RED_B)
        p4 = token("Softmax / Sample", color=GREEN_B)
        p5 = token("Next Token", color=GREEN)
        
        pipeline = VGroup(
            p1, Arrow(LEFT, RIGHT, color=GRAY_C, stroke_width=2).scale(0.5),
            p2, Arrow(LEFT, RIGHT, color=GRAY_C, stroke_width=2).scale(0.5),
            p3, Arrow(LEFT, RIGHT, color=GRAY_C, stroke_width=2).scale(0.5),
            p4, Arrow(LEFT, RIGHT, color=GRAY_C, stroke_width=2).scale(0.5),
            p5
        ).arrange(RIGHT, buff=0.15).move_to(ORIGIN)
        
        self.play(
            FadeIn(pipe_title),
            FadeIn(pipeline),
            run_time=0.8
        )

        # --- Cue 14: Grid of 6 mini-charts (replacing slide code) ---
        self.wait_until(cue_start[14] + 0.25)
        self.play(
            FadeOut(pipe_title),
            FadeOut(pipeline),
            run_time=0.5
        )
        
        grid = VGroup()
        base_probs = [0.45, 0.25, 0.15, 0.10, 0.05]
        labels = ["A", "B", "C", "D", "E"]
        
        # 1. Greedy
        g_chart = CustomBarChart(base_probs, labels, colors=[YELLOW] + [BLUE_E]*4, width=3.2, height=1.1)
        g_lbl = create_text("Greedy", font_size=13, color=YELLOW).next_to(g_chart, UP, buff=0.1)
        g_box = VGroup(g_chart, g_lbl)
        
        # 2. Ancestral
        a_chart = CustomBarChart(base_probs, labels, colors=[BLUE_B]*5, width=3.2, height=1.1)
        a_lbl = create_text("Ancestral", font_size=13, color=BLUE_B).next_to(a_chart, UP, buff=0.1)
        a_box = VGroup(a_chart, a_lbl)
        
        # 3. Top-k
        tk_chart = CustomBarChart([0.45/0.85, 0.25/0.85, 0.15/0.85, 0, 0], labels, colors=[BLUE_B]*3 + [GRAY_E]*2, width=3.2, height=1.1)
        tk_wall = Line(tk_chart.bars[2].get_right() + RIGHT*0.04 + DOWN*0.1, tk_chart.bars[2].get_right() + RIGHT*0.04 + UP*1.0, color=RED, stroke_width=1.5)
        tk_lbl = create_text("Top-k (k=3)", font_size=13, color=BLUE_B).next_to(tk_chart, UP, buff=0.1)
        tk_box = VGroup(tk_chart, tk_lbl, tk_wall)
        
        # 4. Top-p
        tp_chart = CustomBarChart([0.45/0.70, 0.25/0.70, 0, 0, 0], labels, colors=[BLUE_B]*2 + [GRAY_E]*3, width=3.2, height=1.1)
        tp_wall = Line(tp_chart.bars[1].get_right() + RIGHT*0.04 + DOWN*0.1, tp_chart.bars[1].get_right() + RIGHT*0.04 + UP*1.0, color=RED, stroke_width=1.5)
        tp_lbl = create_text("Top-p (p=0.70)", font_size=13, color=BLUE_B).next_to(tp_chart, UP, buff=0.1)
        tp_box = VGroup(tp_chart, tp_lbl, tp_wall)
        
        # 5. Epsilon
        eps_chart = CustomBarChart([0.45, 0.25, 0.15, 0, 0], labels, colors=[BLUE_B]*3 + [GRAY_E]*2, width=3.2, height=1.1)
        eps_line = Line(eps_chart.baseline.get_left() + UP*0.35, eps_chart.baseline.get_right() + UP*0.35, color=RED, stroke_width=1.5)
        eps_lbl = create_text("Epsilon (prob >= 0.12)", font_size=13, color=BLUE_B).next_to(eps_chart, UP, buff=0.1)
        eps_box = VGroup(eps_chart, eps_lbl, eps_line)
        
        # 6. Temperature
        t_probs = [0.65, 0.22, 0.09, 0.03, 0.01]
        t_chart = CustomBarChart(t_probs, labels, colors=[BLUE_B]*5, width=3.2, height=1.1)
        t_lbl = create_text("Temperature", font_size=13, color=BLUE_B).next_to(t_chart, UP, buff=0.1)
        t_box = VGroup(t_chart, t_lbl)
        
        grid.add(g_box, a_box, tk_box, tp_box, eps_box, t_box)
        grid.arrange_in_grid(rows=2, cols=3, buff_x=0.7, buff_y=0.5)
        grid.move_to(DOWN * 0.2)
        
        self.play(FadeIn(grid), run_time=0.9)

        # --- Cue 15: Heavy Tail Causes ---
        self.wait_until(cue_start[15] + 0.2)
        self.play(FadeOut(grid), run_time=0.5)
        
        causes_title = create_text("Why does the model have a heavy tail?", font_size=24, color=YELLOW)
        causes_title.move_to(UP * 1.8)
        
        cause1 = VGroup(
            pill("Under-training", 2.5, RED_B, "#261116"),
            create_text("Model has not learned to exclude nonsense words.", font_size=16, color=GRAY_A)
        ).arrange(RIGHT, buff=0.4)
        
        cause2 = VGroup(
            pill("Cross-Entropy Loss", 2.8, RED_B, "#261116"),
            create_text("Encourages broad coverage, preventing zero probabilities.", font_size=16, color=GRAY_A)
        ).arrange(RIGHT, buff=0.4)
        
        cause3 = VGroup(
            pill("Low-rank constraints", 2.8, RED_B, "#261116"),
            create_text("Logits layer cannot represent complex tail shapes perfectly.", font_size=16, color=GRAY_A)
        ).arrange(RIGHT, buff=0.4)
        
        causes = VGroup(cause1, cause2, cause3).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        causes.move_to(DOWN * 0.3)
        
        self.play(
            FadeIn(causes_title),
            FadeIn(causes, shift=UP * 0.15),
            run_time=0.8
        )

        # --- Cue 16-18: Gate Metaphor for Top-k vs Top-p ---
        self.wait_until(cue_start[16] + 0.2)
        self.play(
            FadeOut(causes_title),
            FadeOut(causes),
            run_time=0.5
        )
        
        gate_title = create_text("Comparing Threshold Mechanisms", font_size=22, color=YELLOW).move_to(UP * 1.6)
        
        # Top-k (Fixed Gate)
        tk_gate_title = create_text("Top-k (Fixed Gate)", font_size=18, color=YELLOW).move_to(LEFT * 3.5 + UP * 0.8)
        tk_gate_left = Line(LEFT * 4.5 + DOWN * 0.5, LEFT * 4.5 + UP * 0.5, color=GRAY_C, stroke_width=4)
        tk_gate_right = Line(LEFT * 2.5 + DOWN * 0.5, LEFT * 2.5 + UP * 0.5, color=GRAY_C, stroke_width=4)
        tk_gate_label = create_text("Fixed k Width", font_size=14, color=GRAY_A).next_to(tk_gate_left, DOWN, buff=0.25).shift(RIGHT * 1.0)
        tk_gate = VGroup(tk_gate_left, tk_gate_right, tk_gate_label)
        
        # Top-p (Adaptive Gate)
        tp_gate_title = create_text("Top-p (Adaptive Gate)", font_size=18, color=GREEN_B).move_to(RIGHT * 3.5 + UP * 0.8)
        tp_gate_left = Line(RIGHT * 2.5 + DOWN * 0.5, RIGHT * 2.5 + UP * 0.5, color=GRAY_C, stroke_width=4)
        tp_gate_right = Line(RIGHT * 4.5 + DOWN * 0.5, RIGHT * 4.5 + UP * 0.5, color=GRAY_C, stroke_width=4)
        tp_gate_label = create_text("Flexible Width", font_size=14, color=GRAY_A).next_to(tp_gate_left, DOWN, buff=0.25).shift(RIGHT * 1.0)
        tp_gate = VGroup(tp_gate_left, tp_gate_right, tp_gate_label)
        
        self.play(
            FadeIn(gate_title),
            FadeIn(tk_gate_title),
            FadeIn(tk_gate),
            FadeIn(tp_gate_title),
            FadeIn(tp_gate),
            run_time=0.7
        )
        
        self.wait_until(cue_start[17] + 0.2)
        
        # Top-p shrinks (narrow) when confident
        self.wait_until(cue_start[18] + 0.2)
        self.play(
            tp_gate_right.animate.shift(LEFT * 1.2),
            tp_gate_label.animate.set_color(GREEN_A),
            run_time=0.6
        )
        # Top-p expands (wide) when uncertain
        self.play(
            tp_gate_right.animate.shift(RIGHT * 1.8),
            run_time=0.8
        )

        # --- Cue 19-21: Final Summary ---
        self.wait_until(cue_start[19] + 0.2)
        self.play(
            FadeOut(gate_title),
            FadeOut(tk_gate_title),
            FadeOut(tk_gate),
            FadeOut(tp_gate_title),
            FadeOut(tp_gate),
            run_time=0.5
        )
        
        summary_title = create_text("Summary: Rescaling vs Truncating", font_size=24, color=YELLOW).move_to(UP * 1.8)
        
        # Left side: Temperature (Rescaling)
        temp_sum_title = create_text("Temperature", font_size=18, color=YELLOW).move_to(LEFT * 3.5 + UP * 1.0)
        temp_sum_chart = CustomBarChart(probs_norm, vocab, colors=[BLUE_B]*8, width=5, height=2.0)
        temp_sum_chart.move_to(LEFT * 3.5 + DOWN * 0.8)
        temp_sum_lbl = create_text("Rescales heights (All tokens kept)", font_size=14, color=GRAY_A).next_to(temp_sum_chart, DOWN, buff=0.2)
        temp_sum_group = VGroup(temp_sum_title, temp_sum_chart, temp_sum_lbl)
        
        # Right side: Truncation (Filtering)
        trunc_sum_title = create_text("Truncation", font_size=18, color=RED_B).move_to(RIGHT * 3.5 + UP * 1.0)
        trunc_sum_chart = CustomBarChart(probs_norm, vocab, colors=[BLUE_B]*8, width=5, height=2.0)
        trunc_sum_chart.move_to(RIGHT * 3.5 + DOWN * 0.8)
        trunc_sum_lbl = create_text("Cuts off tail (Removes tokens)", font_size=14, color=GRAY_A).next_to(trunc_sum_chart, DOWN, buff=0.2)
        trunc_sum_group = VGroup(trunc_sum_title, trunc_sum_chart, trunc_sum_lbl)
        
        self.play(
            FadeIn(summary_title),
            FadeIn(temp_sum_group),
            FadeIn(trunc_sum_group),
            run_time=0.7
        )
        
        self.wait_until(cue_start[20] + 0.2)
        # Flatten distribution (diversity high temp)
        self.play(
            *temp_sum_chart.update_chart(probs_high, vocab, colors=[BLUE_B]*8),
            run_time=0.8
        )
        
        self.wait_until(cue_start[21] + 0.25)
        # Drop truncation wall and filter tail
        wall_sum_x = trunc_sum_chart.bars[4].get_right()[0] + 0.08
        wall_sum = Line([wall_sum_x, trunc_sum_chart.baseline.get_y() - 0.2, 0], [wall_sum_x, trunc_sum_chart.baseline.get_y() + 2.0, 0], color=RED, stroke_width=2.5)
        
        self.play(
            Create(wall_sum),
            *trunc_sum_chart.update_chart(renormalized_probs, vocab, colors=renorm_colors),
            run_time=0.8
        )
        
        self.wait_until(voiceover_end + 0.35)
        self.play(
            FadeOut(summary_title),
            FadeOut(temp_sum_group),
            FadeOut(trunc_sum_group),
            FadeOut(wall_sum),
            FadeOut(header),
            run_time=0.8
        )
        assert_all_scene_voiceovers_played(self)
