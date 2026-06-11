import os
import tempfile
from pathlib import Path
from manim import *
import numpy as np

# Note: visual/narration alignment comment translated from Vietnamese.
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VOICEOVER_DIR = PROJECT_ROOT / "voiceover" / "generated_sentence_level"

SCENE_2_1_DURATIONS = {
    "sc21_001.mp3": 3.483,
    "sc21_002.mp3": 7.802,
    "sc21_003.mp3": 5.944,
    "sc21_004.mp3": 4.226,
    "sc21_005.mp3": 4.087,
    "sc21_006.mp3": 1.161,
    "sc21_007.mp3": 1.300,
    "sc21_008.mp3": 2.508,
    "sc21_009.mp3": 9.288,
    "sc21_010.mp3": 6.548,
    "sc21_011.mp3": 9.660,
    "sc21_012.mp3": 5.480,
    "sc21_013.mp3": 4.272,
    "sc21_014.mp3": 6.641,
    "sc21_015.mp3": 6.827,
}
SCENE_2_1_VOICEOVERS = tuple(SCENE_2_1_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc21_*.mp3"))
    expected = sorted(SCENE_2_1_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 2.1 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_2_1_DURATIONS:
        raise KeyError(f"Unexpected Scene 2.1 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 2.1 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_2_1_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    if played != SCENE_2_1_VOICEOVERS:
        missing = [filename for filename in SCENE_2_1_VOICEOVERS if filename not in played]
        raise RuntimeError(
            f"Scene 2.1 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
        )


def finish_voiceovers(scene, voiceover_end, padding=0.25):
    current_time = getattr(scene.renderer, "time", 0.0)
    remaining = voiceover_end + padding - current_time
    if remaining > 0:
        scene.wait(remaining)


# Note: visual/narration alignment comment translated from Vietnamese.
def create_text(text, font_size=24, font="Arial", color=WHITE, **kwargs):
    if font_size < 20:
        t = Text(text, font_size=36, font=font, color=color, **kwargs)
        t.scale(font_size / 36)
        return t
    return Text(text, font_size=font_size, font=font, color=color, **kwargs)

# Note: visual/narration alignment comment translated from Vietnamese.
def create_markup_text(text, font_size=24, font="Arial", **kwargs):
    if font_size < 20:
        t = MarkupText(text, font_size=36, font=font, **kwargs)
        t.scale(font_size / 36)
        return t
    return MarkupText(text, font_size=font_size, font=font, **kwargs)


# Note: visual/narration alignment comment translated from Vietnamese.
def get_checkmark(color=GREEN_A, stroke_width=2.0):
    checkmark = VMobject(color=color, stroke_width=stroke_width)
    checkmark.set_points_as_corners([
        LEFT * 0.12 + DOWN * 0.04,
        ORIGIN + DOWN * 0.12,
        RIGHT * 0.16 + UP * 0.12
    ])
    return checkmark

# Note: visual/narration alignment comment translated from Vietnamese.
def get_infinity(color=WHITE, stroke_width=2.0):
    left_circle = Circle(radius=0.07, color=color, stroke_width=stroke_width)
    right_circle = Circle(radius=0.07, color=color, stroke_width=stroke_width)
    left_circle.move_to(LEFT * 0.06)
    right_circle.move_to(RIGHT * 0.06)
    return VGroup(left_circle, right_circle)

# Note: visual/narration alignment comment translated from Vietnamese.
def get_minus_infinity(color=RED_A, stroke_width=1.8):
    minus = Line(LEFT * 0.06, RIGHT * 0.06, color=color, stroke_width=stroke_width)
    inf = get_infinity(color=color, stroke_width=stroke_width)
    inf.scale(0.8)
    minus.next_to(inf, LEFT, buff=0.03)
    return VGroup(minus, inf)

# Note: visual/narration alignment comment translated from Vietnamese.
def get_theta(color=WHITE, stroke_width=2.0):
    ellipse = Ellipse(width=0.15, height=0.22, color=color, stroke_width=stroke_width)
    line = Line(LEFT * 0.06, RIGHT * 0.06, color=color, stroke_width=stroke_width)
    line.move_to(ellipse.get_center())
    return VGroup(ellipse, line)

# Note: visual/narration alignment comment translated from Vietnamese.
def get_sigma(color=WHITE, stroke_width=2.0):
    sigma = VMobject(color=color, stroke_width=stroke_width)
    sigma.set_points_as_corners([
        RIGHT * 0.12 + UP * 0.14,
        LEFT * 0.12 + UP * 0.14,
        RIGHT * 0.04 + ORIGIN,
        LEFT * 0.12 + DOWN * 0.14,
        RIGHT * 0.12 + DOWN * 0.14
    ])
    return sigma


class Scene2_1(MovingCameraScene):
    def construct(self):
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.camera.background_color = "#111111"

        # Voiceover audio is scheduled from actual MP3 durations.
        voiceover_end = schedule_scene_voiceovers(self)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        chapter_title = create_text("CHAPTER II: PRIMITIVE GENERATORS", font_size=24, color=GREEN_A)
        chapter_sub = create_text("(Primitive Generators)", font_size=18, color=GRAY_A)
        chapter_sub.next_to(chapter_title, DOWN, buff=0.15)
        chapter_header = VGroup(chapter_title, chapter_sub)
        chapter_header.move_to(ORIGIN)

        self.play(FadeIn(chapter_header, shift=UP * 0.3), run_time=1.2)
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        sub_title = create_text("Primitive Generators - Autoregressive Token Generation", font_size=16, color=GREEN_B)
        sub_title.to_edge(UP, buff=0.4)
        
        self.play(
            ReplacementTransform(chapter_header, sub_title),
            run_time=1.2
        )
        self.wait(1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        grid_group = VGroup()
        rows, cols = 10, 10
        cell_size = 0.3
        spacing = 0.05

        grid_width = cols * cell_size + (cols - 1) * spacing
        grid_height = rows * cell_size + (rows - 1) * spacing
        start_x = -grid_width / 2 + cell_size / 2
        start_y = -0.8 + grid_height / 2 - cell_size / 2

        squares = []
        for r in range(rows):
            for c in range(cols):
                sq = Square(
                    side_length=cell_size, 
                    stroke_width=1.0, 
                    stroke_color=GRAY_E, 
                    fill_opacity=0.0
                )
                sq.move_to(np.array([start_x + c * (cell_size + spacing), start_y - r * (cell_size + spacing), 0]))
                squares.append(sq)
                grid_group.add(sq)

        grid_title = create_text("Huge vocabulary space (Vocabulary V ≈ 50,000)", font_size=12, color=GRAY_A)
        grid_title.next_to(grid_group, UP, buff=0.25)
        
        self.play(
            Write(grid_title),
            LaggedStart(*[Create(sq) for sq in squares], lag_ratio=0.01),
            run_time=1.5
        )
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        idx_tay = 24
        idx_lor = 56
        idx_is = 83

        sq_tay = squares[idx_tay]
        sq_lor = squares[idx_lor]
        sq_is = squares[idx_is]

        self.camera.frame.save_state()
        
        self.play(
            sq_tay.animate.set_fill(BLUE_C, opacity=0.8).set_color(BLUE_C),
            sq_lor.animate.set_fill(GREEN_C, opacity=0.8).set_color(GREEN_C),
            sq_is.animate.set_fill(ORANGE, opacity=0.8).set_color(ORANGE),
            run_time=0.8
        )
        
        self.play(
            self.camera.frame.animate.set(width=3.0).move_to(sq_tay.get_center() + RIGHT * 0.4),
            run_time=1.5
        )
        
        lbl_tay = create_text('ID 23910: "Tay"', font_size=5.76, font="Consolas", color=BLUE_A)
        lbl_tay.next_to(sq_tay, RIGHT, buff=0.1)
        self.play(FadeIn(lbl_tay, shift=RIGHT * 0.1), run_time=0.6)
        self.wait(2.0)

        self.play(
            self.camera.frame.animate.move_to(sq_lor.get_center() + RIGHT * 0.4),
            run_time=1.2
        )
        lbl_lor = create_text('ID 1048: "lor"', font_size=5.76, font="Consolas", color=GREEN_A)
        lbl_lor.next_to(sq_lor, RIGHT, buff=0.1)
        self.play(FadeIn(lbl_lor, shift=RIGHT * 0.1), run_time=0.6)
        self.wait(2.0)

        self.play(
            Restore(self.camera.frame),
            FadeOut(lbl_tay),
            FadeOut(lbl_lor),
            run_time=1.5
        )
        self.wait(1.5)

        self.play(
            FadeOut(grid_group),
            FadeOut(grid_title),
            run_time=1.0
        )
        self.wait(0.5)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step1b_title = create_text("Comparison of 3 tokenizer segmentation levels", font_size=13, color=BLUE_A)
        step1b_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step1b_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        orig_text_box = RoundedRectangle(width=4.0, height=0.6, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
        orig_text_box.move_to(UP * 1.8)
        orig_text = create_text("Original text: \"Taylor Swift is\"", font_size=11, color=WHITE)
        orig_text.move_to(orig_text_box.get_center())
        orig_group = VGroup(orig_text_box, orig_text)
        self.play(FadeIn(orig_group, shift=DOWN * 0.15), run_time=0.8)
        self.wait(2.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        lbl_word = create_text("Word level (Word)", font_size=9, color=BLUE_A)
        lbl_word.move_to(LEFT * 4.8 + UP * 0.8, aligned_edge=LEFT)
        words_tok = ["Taylor", "Swift", "is"]
        words_boxes = []
        for idx, w in enumerate(words_tok):
            box = RoundedRectangle(width=1.3, height=0.45, color=BLUE_C, fill_color="#0e1b29", fill_opacity=0.8, corner_radius=0.04)
            box.move_to(LEFT * 2.2 + idx * 1.5 * RIGHT + UP * 0.8)
            t = create_text(f'"{w}"', font_size=9, color=WHITE)
            t.move_to(box.get_center())
            words_boxes.append(VGroup(box, t))
        words_group = VGroup(lbl_word, *words_boxes)

        self.play(
            Write(lbl_word),
            LaggedStart(*[FadeIn(wb, shift=RIGHT * 0.1) for wb in words_boxes], lag_ratio=0.15),
            run_time=1.2
        )
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        lbl_char = create_text("Character level (Char)", font_size=9, color=GRAY_A)
        lbl_char.move_to(LEFT * 4.8 + DOWN * 0.1, aligned_edge=LEFT)
        chars_tok = ["T", "a", "y", "l", "o", "r", " ", "S", "w", "i", "f", "t", " ", "i", "s"]
        chars_boxes = []
        for idx, c in enumerate(chars_tok):
            box = RoundedRectangle(width=0.35, height=0.45, color=GRAY_B, fill_color="#1e1e1e", fill_opacity=0.8, corner_radius=0.03)
            box.move_to(LEFT * 2.65 + idx * 0.42 * RIGHT + DOWN * 0.1)
            t = create_text(c if c != " " else " ", font_size=8, color=GRAY_A)
            t.move_to(box.get_center())
            chars_boxes.append(VGroup(box, t))
        chars_group = VGroup(lbl_char, *chars_boxes)

        self.play(
            Write(lbl_char),
            LaggedStart(*[FadeIn(cb, shift=DOWN * 0.05) for cb in chars_boxes], lag_ratio=0.05),
            run_time=1.2
        )
        self.wait(4.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        lbl_bpe = create_text("BPE level (Subword)", font_size=9, color=GREEN_A)
        lbl_bpe.move_to(LEFT * 4.8 + DOWN * 1.0, aligned_edge=LEFT)
        bpe_tok = ["Taylor", " Swift", " is"]
        bpe_boxes = []
        for idx, b in enumerate(bpe_tok):
            box = RoundedRectangle(width=1.5, height=0.45, color=GREEN_C, fill_color="#0d2417", fill_opacity=0.8, corner_radius=0.04)
            box.move_to(LEFT * 2.1 + idx * 1.7 * RIGHT + DOWN * 1.0)
            t = create_text(f'"{b}"', font_size=9, color=WHITE)
            t.move_to(box.get_center())
            bpe_boxes.append(VGroup(box, t))
        bpe_group = VGroup(lbl_bpe, *bpe_boxes)

        self.play(
            Write(lbl_bpe),
            LaggedStart(*[FadeIn(bb, shift=UP * 0.1) for bb in bpe_boxes], lag_ratio=0.15),
            run_time=1.2
        )
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            *[bb[0].animate.set_color(YELLOW).set_stroke(width=2.0) for bb in bpe_boxes],
            run_time=0.6
        )
        self.play(
            *[bb[0].animate.set_color(GREEN_C).set_stroke(width=1.0) for bb in bpe_boxes],
            run_time=0.6
        )
        self.wait(5.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        all_step1b = VGroup(orig_group, step1b_title, words_group, chars_group, bpe_group)
        self.play(FadeOut(all_step1b, shift=LEFT * 0.3), run_time=1.2)
        self.wait(0.5)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step2_title = create_text("Self-attention collects past context", font_size=13, color=BLUE_A)
        step2_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step2_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        words = ["Taylor", " Swift", " is"]
        colors = [BLUE_D, BLUE_D, GREEN_D]
        boxes = []
        labels = []
        box_width = 1.6

        for idx, word in enumerate(words):
            box = RoundedRectangle(width=box_width, height=0.6, color=colors[idx], fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.06)
            box.move_to(LEFT * 2.0 + idx * 2.0 * RIGHT + DOWN * 1.5)
            lbl = create_text(f'"{word}"', font_size=11, color=WHITE)
            lbl.move_to(box.get_center())
            boxes.append(box)
            labels.append(lbl)

        box_group = VGroup(*boxes, *labels)
        self.play(FadeIn(box_group, shift=UP * 0.2), run_time=1.0)
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        curves = []
        for i in range(2):
            start = boxes[i].get_top()
            end = boxes[2].get_top()
            angle = - (2 - i) * 0.2 * PI
            curve = ArcBetweenPoints(start, end, angle=angle, color=YELLOW_E, stroke_width=1.5)
            curve.add_tip(tip_length=0.12, tip_width=0.12)
            curves.append(curve)

        self.play(*[Create(c) for c in curves], run_time=1.0)
        self.wait(1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        dots = []
        moves = []
        for i in range(2):
            dot = Dot(radius=0.06, color=YELLOW)
            dot.move_to(boxes[i].get_top())
            dots.append(dot)
            moves.append(MoveAlongPath(dot, curves[i], run_time=1.8, rate_func=linear))

        self.play(*moves)
        self.remove(*dots)
        self.play(boxes[2].animate.set_color(YELLOW).set_fill("#2e2202", opacity=0.9), run_time=0.4)
        self.wait(0.5)
        self.play(boxes[2].animate.set_color(GREEN_D).set_fill("#181a1e", opacity=0.9), run_time=0.4)

        # Note: visual/narration alignment comment translated from Vietnamese.
        formula_box = RoundedRectangle(width=6.8, height=1.5, color=BLUE_E, fill_color="#0e1726", fill_opacity=0.6, corner_radius=0.08)
        formula_box.move_to(UP * 1.0)
        
        # Build formula p_theta(x_t | x_{<t}) manually with custom drawn theta on a straight baseline
        p_text = create_text("p", font_size=28, color="#8fbcbb")
        
        open_paren = create_text("(", font_size=28, color=WHITE)
        open_paren.next_to(p_text, RIGHT, buff=0.25)
        
        xt_part = create_text("x", font_size=28, color=YELLOW)
        xt_part.next_to(open_paren, RIGHT, buff=0.05)
        
        pipe_part = create_text(" | ", font_size=28, color=WHITE)
        pipe_part.next_to(xt_part, RIGHT, buff=0.20)
        
        x_lt_part = create_text("x", font_size=28, color="#88c0d0")
        x_lt_part.next_to(pipe_part, RIGHT, buff=0.05)
        
        close_paren = create_text(")", font_size=28, color=WHITE)
        close_paren.next_to(x_lt_part, RIGHT, buff=0.30)
        
        theta_sub = get_theta(color="#8fbcbb", stroke_width=1.5).scale(0.5)
        theta_sub.next_to(p_text.get_corner(DOWN + RIGHT), RIGHT, buff=0.01).shift(DOWN * 0.05)
        
        t_sub = create_text("t", font_size=18, color=YELLOW)
        t_sub.next_to(xt_part.get_corner(DOWN + RIGHT), RIGHT, buff=0.01).shift(DOWN * 0.04)
        
        lt_sub = create_text("<t", font_size=18, color="#88c0d0")
        lt_sub.next_to(x_lt_part.get_corner(DOWN + RIGHT), RIGHT, buff=0.01).shift(DOWN * 0.04)
        
        formula = VGroup(p_text, theta_sub, open_paren, xt_part, t_sub, pipe_part, x_lt_part, lt_sub, close_paren)
        formula.move_to(formula_box.get_center())

        self.play(
            FadeIn(formula_box),
            Write(formula),
            run_time=1.0
        )
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        dots_2 = []
        moves_2 = []
        for i in range(2):
            dot = Dot(radius=0.06, color=YELLOW)
            dot.move_to(boxes[i].get_top())
            dots_2.append(dot)
            moves_2.append(MoveAlongPath(dot, curves[i], run_time=1.8, rate_func=linear))

        self.play(
            *moves_2,
            x_lt_part.animate.set_color(BLUE_A),
            lt_sub.animate.set_color(BLUE_A),
            run_time=1.8
        )
        self.remove(*dots_2)
        
        self.play(
            xt_part.animate.set_color(YELLOW),
            t_sub.animate.set_color(YELLOW),
            boxes[2].animate.set_color(YELLOW).set_fill("#2e2202", opacity=0.9),
            run_time=0.8
        )
        self.wait(3.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(step2_title),
            FadeOut(box_group),
            FadeOut(formula_box),
            FadeOut(formula),
            *[FadeOut(c) for c in curves],
            run_time=1.2
        )
        self.wait(0.5)

        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step2a_title = create_text("Causal mask prevents looking into the future", font_size=13, color=BLUE_A)
        step2a_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step2a_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        matrix_cells = VGroup()
        cell_size = 0.7
        spacing = 0.08
        matrix_start_x = -1.2
        matrix_start_y = 0.8
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        matrix_labels = ["Taylor", "Swift", "is", "an"]
        col_labels_mobs = VGroup()
        row_labels_mobs = VGroup()
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        for col in range(4):
            x_val = matrix_start_x + col * (cell_size + spacing)
            lbl = create_text(matrix_labels[col], font_size=9, color=BLUE_A)
            lbl.move_to(np.array([x_val, matrix_start_y + cell_size/2.0 + 0.3, 0]))
            col_labels_mobs.add(lbl)
            
        # Note: visual/narration alignment comment translated from Vietnamese.
        for row in range(4):
            y_val = matrix_start_y - row * (cell_size + spacing)
            lbl = create_text(matrix_labels[row], font_size=9, color=GREEN_A)
            lbl.move_to(np.array([matrix_start_x - cell_size/2.0 - 0.5, y_val, 0]))
            row_labels_mobs.add(lbl)

        self.play(
            FadeIn(col_labels_mobs),
            FadeIn(row_labels_mobs),
            run_time=0.8
        )
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        squares_grid = []
        for r in range(4):
            row_squares = []
            for c in range(4):
                x_val = matrix_start_x + c * (cell_size + spacing)
                y_val = matrix_start_y - r * (cell_size + spacing)
                sq = Square(side_length=cell_size, stroke_width=1.5, stroke_color=GRAY_D, fill_opacity=0.0)
                sq.move_to(np.array([x_val, y_val, 0]))
                row_squares.append(sq)
                matrix_cells.add(sq)
            squares_grid.append(row_squares)

        self.play(
            LaggedStart(*[Create(s) for s in matrix_cells], lag_ratio=0.03),
            run_time=1.0
        )
        self.wait(2.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        green_fill = "#153a1e"
        red_fill = "#3a1515"
        
        checks_and_masks = VGroup()
        
        for r in range(4):
            play_list = []
            for c in range(4):
                sq = squares_grid[r][c]
                x_val = sq.get_center()[0]
                y_val = sq.get_center()[1]
                
                if c <= r:
                    # Note: visual/narration alignment comment translated from Vietnamese.
                    sq_anim = sq.animate.set_fill(green_fill, opacity=0.85).set_color(GREEN_B)
                    symbol = get_checkmark(color=GREEN_A, stroke_width=1.8)
                    symbol.move_to(sq.get_center())
                    play_list.append(sq_anim)
                    play_list.append(FadeIn(symbol))
                    checks_and_masks.add(symbol)
                else:
                    # Note: visual/narration alignment comment translated from Vietnamese.
                    sq_anim = sq.animate.set_fill(red_fill, opacity=0.85).set_color(RED_B)
                    symbol = get_minus_infinity(color=RED_A, stroke_width=1.5)
                    symbol.move_to(sq.get_center())
                    play_list.append(sq_anim)
                    play_list.append(FadeIn(symbol))
                    checks_and_masks.add(symbol)
            
            # Note: visual/narration alignment comment translated from Vietnamese.
            self.play(*play_list, run_time=1.0)
            self.wait(2.0)

        self.wait(6.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(step2a_title),
            FadeOut(matrix_cells),
            FadeOut(col_labels_mobs),
            FadeOut(row_labels_mobs),
            FadeOut(checks_and_masks),
            run_time=1.2
        )
        self.wait(0.5)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step2b_title = create_text("Softmax transform: from raw logits to probabilities", font_size=13, color=BLUE_A)
        step2b_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step2b_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        softmax_box = RoundedRectangle(width=5.5, height=1.3, color=GREEN_E, fill_color="#0d2417", fill_opacity=0.4, corner_radius=0.08)
        softmax_box.move_to(UP * 1.5)
        # Build Softmax formula manually to avoid Sigma rendering issue and format as fraction
        left_part = create_text("Softmax(z", font_size=20, color="#8fbcbb")
        right_paren_left = create_text(") = ", font_size=20, color=WHITE)
        right_paren_left.next_to(left_part, RIGHT, buff=0.18)
        
        i_sub_left = create_text("i", font_size=14, color="#8fbcbb")
        i_sub_left.next_to(left_part.get_corner(DOWN + RIGHT), RIGHT, buff=0.01).shift(DOWN * 0.03)
        
        # Numerator
        num_e = create_text("e", font_size=20, color=YELLOW)
        num_zi = create_text("z", font_size=14, color=YELLOW)
        num_zi.next_to(num_e.get_corner(UP + RIGHT), RIGHT, buff=0.01).shift(UP * 0.03)
        num_i = create_text("i", font_size=10, color=YELLOW)
        num_i.next_to(num_zi.get_corner(DOWN + RIGHT), RIGHT, buff=0.01).shift(DOWN * 0.02)
        numerator = VGroup(num_e, num_zi, num_i)
        
        # Denominator (uses custom drawn Sigma)
        sigma = get_sigma(color="#88c0d0", stroke_width=1.5).scale(0.65)
        j_sub_sigma = create_text("j", font_size=12, color="#88c0d0")
        j_sub_sigma.next_to(sigma, DOWN, buff=0.04)
        
        den_e = create_text("e", font_size=20, color="#88c0d0")
        den_zj = create_text("z", font_size=14, color="#88c0d0")
        den_zj.next_to(den_e.get_corner(UP + RIGHT), RIGHT, buff=0.01).shift(UP * 0.03)
        den_j = create_text("j", font_size=10, color="#88c0d0")
        den_j.next_to(den_zj.get_corner(DOWN + RIGHT), RIGHT, buff=0.01).shift(DOWN * 0.02)
        
        den_term = VGroup(den_e, den_zj, den_j)
        den_term.next_to(sigma, RIGHT, buff=0.1)
        
        denominator = VGroup(sigma, j_sub_sigma, den_term)
        
        # Align fraction
        fraction_line = Line(LEFT * 0.6, RIGHT * 0.6, color=WHITE, stroke_width=1.5)
        
        # Arrange numerator, line, denominator vertically
        numerator.move_to(UP * 0.35)
        fraction_line.move_to(ORIGIN)
        denominator.move_to(DOWN * 0.35)
        
        fraction = VGroup(numerator, fraction_line, denominator)
        fraction.next_to(right_paren_left, RIGHT, buff=0.15)
        
        softmax_formula = VGroup(left_part, i_sub_left, right_paren_left, fraction)
        softmax_formula.move_to(softmax_box.get_center())
        
        self.play(
            FadeIn(softmax_box),
            Write(softmax_formula),
            run_time=1.0
        )
        self.wait(3.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Logits: "an" (2.5), "a" (0.5), "the" (1.6), "best" (-0.8)
        chart_base_y = -2.2
        chart_center_x = 0.0
        labels_words = ["\"an\"", "\"a\"", "\"the\"", "\"best\""]
        logits_vals = [2.5, 0.5, 1.6, -0.8]
        colors_chart = [BLUE_D, GRAY_C, GRAY_C, RED_D]

        # Note: visual/narration alignment comment translated from Vietnamese.
        axis_line = Line(LEFT * 4.5 + UP * chart_base_y, RIGHT * 4.5 + UP * chart_base_y, color=WHITE, stroke_width=2.0)
        chart_title = create_text("Raw logits from the model (z)", font_size=10, color=GRAY_A)
        chart_title.move_to(UP * (chart_base_y - 0.7) + LEFT * 3.0, aligned_edge=LEFT)

        self.play(Create(axis_line), Write(chart_title), run_time=0.8)

        bars = []
        labels_mobs = []
        val_labels = []

        for i in range(4):
            x_pos = -3.0 + i * 2.0
            
            # Note: visual/narration alignment comment translated from Vietnamese.
            lbl = create_text(labels_words[i], font_size=10, color=WHITE)
            lbl.move_to(np.array([x_pos, chart_base_y - 0.35, 0]))
            labels_mobs.append(lbl)

            # Note: visual/narration alignment comment translated from Vietnamese.
            height = logits_vals[i] * 0.4
            # Note: visual/narration alignment comment translated from Vietnamese.
            bar = Rectangle(
                width=0.8, 
                height=abs(height), 
                color=colors_chart[i], 
                fill_color=colors_chart[i], 
                fill_opacity=0.9
            )
            # Note: visual/narration alignment comment translated from Vietnamese.
            if height >= 0:
                bar.move_to(np.array([x_pos, chart_base_y + abs(height)/2.0, 0]))
            else:
                bar.move_to(np.array([x_pos, chart_base_y - abs(height)/2.0, 0]))
            bars.append(bar)

            # Note: visual/narration alignment comment translated from Vietnamese.
            y_val_pos = chart_base_y + height + (0.2 if height >= 0 else -0.2)
            v_lbl = create_text(f"{logits_vals[i]:+.1f}", font_size=9, color=colors_chart[i])
            v_lbl.move_to(np.array([x_pos, y_val_pos, 0]))
            val_labels.append(v_lbl)

        bar_group = VGroup(*bars)
        label_group = VGroup(*labels_mobs)
        val_group = VGroup(*val_labels)

        self.play(
            FadeIn(bar_group, shift=UP * 0.2),
            FadeIn(label_group),
            Write(val_group),
            run_time=1.2
        )
        self.wait(5.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        chart_title_ez = create_markup_text("Natural exponential e<sup>z</sup> (Always positive)", font_size=10, color=YELLOW)
        chart_title_ez.move_to(chart_title.get_center(), aligned_edge=LEFT)

        # Note: visual/narration alignment comment translated from Vietnamese.
        ez_vals = [np.exp(v) for v in logits_vals]
        # Note: visual/narration alignment comment translated from Vietnamese.
        scale_ez = 2.0 / max(ez_vals)

        new_bars_ez = []
        new_val_labels_ez = []

        for i in range(4):
            x_pos = -3.0 + i * 2.0
            height_ez = ez_vals[i] * scale_ez
            bar_ez = Rectangle(
                width=0.8, 
                height=height_ez, 
                color=colors_chart[i], 
                fill_color=colors_chart[i], 
                fill_opacity=0.9
            )
            bar_ez.move_to(np.array([x_pos, chart_base_y + height_ez/2.0, 0]))
            new_bars_ez = VGroup(*new_bars_ez, bar_ez)

            v_lbl_ez = create_text(f"{ez_vals[i]:.2f}", font_size=9, color=YELLOW)
            v_lbl_ez.move_to(np.array([x_pos, chart_base_y + height_ez + 0.2, 0]))
            new_val_labels_ez = VGroup(*new_val_labels_ez, v_lbl_ez)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            ReplacementTransform(chart_title, chart_title_ez),
            ReplacementTransform(bar_group, new_bars_ez),
            ReplacementTransform(val_group, new_val_labels_ez),
            numerator.animate.set_color(YELLOW), # Note: visual/narration alignment comment translated from Vietnamese.
            run_time=1.5
        )
        self.wait(5.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        chart_title_prob = create_text("Probability distribution (Total = 100%)", font_size=10, color=GREEN_A)
        chart_title_prob.move_to(chart_title.get_center(), aligned_edge=LEFT)

        # Note: visual/narration alignment comment translated from Vietnamese.
        prob_vals = [0.63, 0.09, 0.26, 0.02]
        scale_prob = 2.4 # Note: visual/narration alignment comment translated from Vietnamese.

        new_bars_prob = []
        new_val_labels_prob = []

        for i in range(4):
            x_pos = -3.0 + i * 2.0
            height_prob = prob_vals[i] * scale_prob
            bar_prob = Rectangle(
                width=0.8, 
                height=max(height_prob, 0.05), # Note: visual/narration alignment comment translated from Vietnamese.
                color=GREEN_C if i==0 else GRAY_C, 
                fill_color=GREEN_C if i==0 else GRAY_C, 
                fill_opacity=0.9
            )
            bar_prob.move_to(np.array([x_pos, chart_base_y + height_prob/2.0, 0]))
            new_bars_prob = VGroup(*new_bars_prob, bar_prob)

            v_lbl_prob = create_text(f"{prob_vals[i]*100:.0f}%", font_size=9, color=GREEN_A)
            v_lbl_prob.move_to(np.array([x_pos, chart_base_y + height_prob + 0.2, 0]))
            new_val_labels_prob = VGroup(*new_val_labels_prob, v_lbl_prob)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            ReplacementTransform(chart_title_ez, chart_title_prob),
            ReplacementTransform(new_bars_ez, new_bars_prob),
            ReplacementTransform(new_val_labels_ez, new_val_labels_prob),
            denominator.animate.set_color(BLUE_A), # Note: visual/narration alignment comment translated from Vietnamese.
            run_time=1.5
        )
        self.wait(6.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(step2b_title),
            FadeOut(softmax_box),
            FadeOut(softmax_formula),
            FadeOut(axis_line),
            FadeOut(chart_title_prob),
            FadeOut(new_bars_prob),
            FadeOut(label_group),
            FadeOut(new_val_labels_prob),
            run_time=1.2
        )
        self.wait(0.5)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # decoding."
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step3_title = create_text("Autoregressive decoding loop across 4 generation steps", font_size=13, color=BLUE_A)
        step3_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step3_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        prefix_container = RoundedRectangle(width=5.8, height=4.2, color=BLUE_E, fill_color="#0e1726", fill_opacity=0.3, corner_radius=0.08)
        prefix_container.move_to(LEFT * 3.3 + DOWN * 0.6)
        prefix_title = create_text("Prefix sequence (Context window)", font_size=10, color=BLUE_C)
        prefix_title.next_to(prefix_container.get_top(), DOWN, buff=0.15)
        prefix_group = VGroup(prefix_container, prefix_title)

        vocab_container = RoundedRectangle(width=6.0, height=4.2, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.7, corner_radius=0.08)
        vocab_container.move_to(RIGHT * 3.2 + DOWN * 0.6)
        vocab_title = create_markup_text("Vocabulary probability distribution p(x<sub>t</sub> | x<sub>&lt;t</sub>)", font_size=10, color=GRAY_A)
        vocab_title.next_to(vocab_container.get_top(), DOWN, buff=0.15)
        vocab_group = VGroup(vocab_container, vocab_title)

        self.play(
            FadeIn(prefix_group, shift=RIGHT * 0.15),
            FadeIn(vocab_group, shift=LEFT * 0.15),
            run_time=1.0
        )
        self.wait(1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        prefix_lines = [
            create_text("Taylor Alison Swift", font_size=12, color=WHITE),
            create_text("(born December 13, 1989) is", font_size=12, color=WHITE)
        ]
        prefix_text_group = VGroup(*prefix_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        prefix_text_group.move_to(prefix_container.get_center())

        self.play(FadeIn(prefix_text_group), run_time=0.8)
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        candidates_1 = [
            {"word": "an", "prob": 0.13, "color": BLUE_C},
            {"word": "a", "prob": 0.03, "color": GRAY_C},
            {"word": "the", "prob": 0.06, "color": GRAY_C},
            {"word": "best", "prob": 0.02, "color": GRAY_C}
        ]
        chart_1 = build_bar_chart(candidates_1, 0.4)
        self.play(FadeIn(chart_1, shift=UP * 0.15), run_time=0.8)
        self.wait(2.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        selected_text_1 = create_text("an", font_size=12, color=YELLOW)
        selected_text_1.move_to(chart_1[0][0].get_center())
        
        prefix_line2_new = create_text("(born December 13, 1989) is an", font_size=12, color=WHITE)
        prefix_line2_new.move_to(prefix_lines[1].get_left(), aligned_edge=LEFT)
        word_an_highlight = create_text("an", font_size=12, color=YELLOW)
        word_an_highlight.next_to(prefix_lines[1], RIGHT, buff=0.1)

        self.play(
            chart_1[0][1].animate.set_color(YELLOW),
            ReplacementTransform(selected_text_1, word_an_highlight),
            run_time=1.0
        )
        self.remove(prefix_lines[1], word_an_highlight)
        self.add(prefix_line2_new)
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(FadeOut(chart_1), run_time=0.4)
        candidates_2 = [
            {"word": "American", "prob": 0.82, "color": BLUE_C},
            {"word": "actress", "prob": 0.05, "color": GRAY_C},
            {"word": "English", "prob": 0.02, "color": GRAY_C},
            {"word": "award", "prob": 0.01, "color": GRAY_C}
        ]
        chart_2 = build_bar_chart(candidates_2, 0.4)
        self.play(FadeIn(chart_2, shift=UP * 0.15), run_time=0.8)
        self.wait(2.5)

        selected_text_2 = create_text("American", font_size=12, color=YELLOW)
        selected_text_2.move_to(chart_2[0][0].get_center())

        prefix_line3 = create_text("American", font_size=12, color=WHITE)
        prefix_line3.next_to(prefix_line2_new, DOWN, buff=0.15, aligned_edge=LEFT)
        prefix_line3_highlight = create_text("American", font_size=12, color=YELLOW)
        prefix_line3_highlight.move_to(prefix_line3.get_left(), aligned_edge=LEFT)

        self.play(
            chart_2[0][1].animate.set_color(YELLOW),
            ReplacementTransform(selected_text_2, prefix_line3_highlight),
            run_time=1.0
        )
        self.add(prefix_line3)
        self.remove(prefix_line3_highlight)
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(FadeOut(chart_2), run_time=0.4)
        candidates_3 = [
            {"word": "singer", "prob": 0.65, "color": BLUE_C},
            {"word": "actress", "prob": 0.15, "color": GRAY_C},
            {"word": "songwriter", "prob": 0.08, "color": GRAY_C},
            {"word": "writer", "prob": 0.04, "color": GRAY_C}
        ]
        chart_3 = build_bar_chart(candidates_3, 0.4)
        self.play(FadeIn(chart_3, shift=UP * 0.15), run_time=0.8)
        self.wait(2.5)

        selected_text_3 = create_text("singer", font_size=12, color=YELLOW)
        selected_text_3.move_to(chart_3[0][0].get_center())

        prefix_line3_new = create_text("American singer", font_size=12, color=WHITE)
        prefix_line3_new.move_to(prefix_line3.get_left(), aligned_edge=LEFT)
        word_singer_highlight = create_text("singer", font_size=12, color=YELLOW)
        word_singer_highlight.next_to(prefix_line3, RIGHT, buff=0.1)

        self.play(
            chart_3[0][1].animate.set_color(YELLOW),
            ReplacementTransform(selected_text_3, word_singer_highlight),
            run_time=1.0
        )
        self.remove(prefix_line3, word_singer_highlight)
        self.add(prefix_line3_new)
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(FadeOut(chart_3), run_time=0.4)
        candidates_4 = [
            {"word": ",", "prob": 0.75, "color": BLUE_C},
            {"word": "and", "prob": 0.12, "color": GRAY_C},
            {"word": "who", "prob": 0.05, "color": GRAY_C},
            {"word": ".", "prob": 0.03, "color": GRAY_C}
        ]
        chart_4 = build_bar_chart(candidates_4, 0.4)
        self.play(FadeIn(chart_4, shift=UP * 0.15), run_time=0.8)
        self.wait(2.5)

        selected_text_4 = create_text(",", font_size=12, color=YELLOW)
        selected_text_4.move_to(chart_4[0][0].get_center())

        prefix_line3_new2 = create_text("American singer ,", font_size=12, color=WHITE)
        prefix_line3_new2.move_to(prefix_line3_new.get_left(), aligned_edge=LEFT)
        word_comma_highlight = create_text(",", font_size=12, color=YELLOW)
        word_comma_highlight.next_to(prefix_line3_new, RIGHT, buff=0.06)

        self.play(
            chart_4[0][1].animate.set_color(YELLOW),
            ReplacementTransform(selected_text_4, word_comma_highlight),
            run_time=1.0
        )
        self.remove(prefix_line3_new, word_comma_highlight)
        self.add(prefix_line3_new2)
        self.wait(3.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        all_step2 = VGroup(
            step3_title, prefix_group, vocab_group, prefix_lines[0], prefix_line2_new, prefix_line3_new2, chart_4
        )
        self.play(FadeOut(all_step2, shift=DOWN * 0.2), run_time=1.2)
        self.wait(0.5)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step3_title_new = create_text("Exponential combinatorial explosion of the decision tree", font_size=13, color=BLUE_A)
        step3_title_new.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step3_title_new), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        root_node = RoundedRectangle(width=2.2, height=0.5, color=BLUE_D, fill_color="#0e1726", fill_opacity=0.9, corner_radius=0.04)
        root_node.move_to(UP * 2.2)
        root_text = create_text('"Taylor Swift is"', font_size=9, color=WHITE)
        root_text.move_to(root_node.get_center())
        root_group = VGroup(root_node, root_text)

        self.play(FadeIn(root_group), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        child_words = ["a", "the", "singer", "writer"]
        child_coords = [LEFT * 4.5, LEFT * 1.5, RIGHT * 1.5, RIGHT * 4.5]
        child_groups = []
        arrows_1 = []

        for idx, word in enumerate(child_words):
            coord = child_coords[idx] + UP * 0.8
            node = RoundedRectangle(width=1.2, height=0.4, color=GRAY_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.04)
            node.move_to(coord)
            txt = create_text(f'"{word}"', font_size=8, color=WHITE)
            txt.move_to(node.get_center())
            ng = VGroup(node, txt)
            child_groups.append(ng)
            
            arr = Line(root_node.get_bottom(), node.get_top(), color=GRAY_B, stroke_width=1.5).add_tip(tip_length=0.07, tip_width=0.07)
            arrows_1.append(arr)

        self.play(
            *[Create(arr) for arr in arrows_1],
            *[FadeIn(c, shift=DOWN * 0.15) for c in child_groups],
            run_time=1.0
        )
        self.wait(1.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        grandchild_groups = []
        arrows_2 = []
        for i in range(4):
            for j in range(3):
                offset_x = -0.8 + j * 0.8
                coord = child_coords[i] + RIGHT * offset_x + DOWN * 0.5
                node = RoundedRectangle(width=0.7, height=0.3, color=GRAY_B, fill_color="#20232a", fill_opacity=0.9, corner_radius=0.03)
                node.move_to(coord)
                txt = create_text("...", font_size=7, color=GRAY_A)
                txt.move_to(node.get_center())
                ng = VGroup(node, txt)
                grandchild_groups.append(ng)

                arr = Line(child_groups[i].get_bottom(), node.get_top(), color=GRAY_C, stroke_width=1.0).add_tip(tip_length=0.05, tip_width=0.05)
                arrows_2.append(arr)

        self.play(
            *[Create(arr) for arr in arrows_2],
            *[FadeIn(gc) for gc in grandchild_groups],
            run_time=1.2
        )
        self.wait(1.5)

        self.camera.frame.save_state()

        # Note: visual/narration alignment comment translated from Vietnamese.
        fractal_lines = VGroup()
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        def generate_fractal_tree(start_pt, depth, angle_offset, scale_factor, max_d=4):
            if depth > max_d:
                return
            branching = 3
            spread = 0.5 / depth
            for k in range(branching):
                angle = angle_offset + (k - 1) * spread - PI/2
                length = 2.0 / (depth ** 0.85)
                end_pt = start_pt + np.array([length * np.cos(angle), length * np.sin(angle), 0])
                
                line = Line(start_pt, end_pt, color=GRAY_D, stroke_width=1.5/depth)
                fractal_lines.add(line)
                
                generate_fractal_tree(end_pt, depth + 1, angle + PI/2, scale_factor, max_d)

        # Note: visual/narration alignment comment translated from Vietnamese.
        for i in range(4):
            start = child_groups[i].get_bottom()
            generate_fractal_tree(start, 2, (i - 1.5) * 0.1, 0.7, max_d=4)

        # Camera zoom out
        self.play(
            self.camera.frame.animate.scale(2.5).move_to(DOWN * 2.0),
            FadeIn(fractal_lines, run_time=2.0),
            run_time=2.5
        )
        self.wait(1.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        search_box = RoundedRectangle(width=8.5, height=2.2, color=GOLD_A, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        search_box.scale(2.5)
        search_box.move_to(self.camera.frame.get_center() + DOWN * 4.2)
        
        search_title = create_text("Search Space (Search Space) - Slide 30-31", font_size=9, color=GOLD_B)
        search_title.scale(2.5)
        search_title.next_to(search_box.get_top(), DOWN, buff=0.4)
        
        search_desc = create_markup_text(
            "• <b>Primitive Generators:</b> Generate autoregressively one token at a time.\n"
            "• <b>Search Space:</b> Space expands exponentially <i>V<sup>t</sup></i>.\n"
            "• <b>Search for what? Objective?</b> What objective are we searching for?",
            font_size=7, line_spacing=1.3
        )
        search_desc.scale(2.5)
        search_desc.next_to(search_title, DOWN, buff=0.4).align_to(search_box, LEFT).shift(RIGHT * 0.8)
        search_info_group = VGroup(search_box, search_title, search_desc)

        self.play(
            FadeIn(search_info_group, shift=UP * 0.3),
            run_time=1.5
        )
        self.wait(5.0)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            Restore(self.camera.frame),
            FadeOut(search_info_group),
            FadeOut(fractal_lines),
            FadeOut(root_group),
            *[FadeOut(c) for c in child_groups],
            *[FadeOut(a) for a in arrows_1],
            *[FadeOut(gc) for gc in grandchild_groups],
            *[FadeOut(a) for a in arrows_2],
            FadeOut(step3_title_new),
            run_time=1.8
        )
        self.wait(0.5)


        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        # Note: visual/narration alignment comment translated from Vietnamese.
        # =====================================================================
        step4_title = create_text("Three main objective groups in decoding algorithms", font_size=13, color=BLUE_A)
        step4_title.next_to(sub_title, DOWN, buff=0.3)
        self.play(Write(step4_title), run_time=0.8)

        # Note: visual/narration alignment comment translated from Vietnamese.
        box_width, box_height = 3.8, 2.2
        
        # Note: visual/narration alignment comment translated from Vietnamese.
        box_opt = RoundedRectangle(width=box_width, height=box_height, color=BLUE_C, fill_color="#0e1b29", fill_opacity=0.8, corner_radius=0.08)
        box_opt.move_to(LEFT * 4.2 + DOWN * 0.5)
        opt_title = create_text("1. OPTIMIZATION (Optimization)", font_size=10, color=BLUE_A)
        opt_desc1 = create_text("Find the highest-probability sequence:", font_size=8, color=WHITE)
        
        # Build argmax_x p_theta(x) manually to avoid Sigma/Theta rendering issue
        opt_argmax = create_text("argmax", font_size=10, color=YELLOW)
        opt_p = create_text("p", font_size=10, color=YELLOW)
        opt_p.next_to(opt_argmax, RIGHT, buff=0.10)
        
        opt_x_sub = create_text("x", font_size=7, color=YELLOW)
        opt_x_sub.next_to(opt_argmax, DOWN, buff=0.01).align_to(opt_argmax, RIGHT).shift(RIGHT * 0.01)
        
        opt_x_paren = create_text("(x)", font_size=10, color=YELLOW)
        opt_x_paren.next_to(opt_p, RIGHT, buff=0.07)
        
        opt_theta = get_theta(color=YELLOW, stroke_width=0.8).scale(0.3)
        opt_theta.next_to(opt_p.get_corner(DOWN + RIGHT), RIGHT, buff=0.005).shift(DOWN * 0.02)
        
        opt_formula = VGroup(opt_argmax, opt_p, opt_x_sub, opt_x_paren, opt_theta)
        
        opt_desc2 = create_text("Example: Greedy, Beam Search", font_size=8, color=GRAY_A)
        opt_content = VGroup(opt_title, opt_desc1, opt_formula, opt_desc2).arrange(DOWN, buff=0.12)
        opt_content.move_to(box_opt.get_center())
        opt_group = VGroup(box_opt, opt_content)

        # Note: visual/narration alignment comment translated from Vietnamese.
        box_sam = RoundedRectangle(width=box_width, height=box_height, color=GREEN_C, fill_color="#0d2417", fill_opacity=0.8, corner_radius=0.08)
        box_sam.move_to(DOWN * 0.5)
        sam_title = create_text("2. SAMPLING (Sampling)", font_size=10, color=GREEN_A)
        sam_desc1 = create_text("Sample randomly from the distribution:", font_size=8, color=WHITE)
        
        # Build y ~ q(p_theta) manually to avoid Theta rendering issue on straight baseline
        sam_prefix = create_text("y ~ q(", font_size=10, color=YELLOW)
        sam_p = create_text("p", font_size=10, color=YELLOW)
        sam_p.next_to(sam_prefix, RIGHT, buff=0.02)
        
        sam_paren = create_text(")", font_size=10, color=YELLOW)
        sam_paren.next_to(sam_p, RIGHT, buff=0.07)
        
        sam_theta = get_theta(color=YELLOW, stroke_width=0.8).scale(0.3)
        sam_theta.next_to(sam_p.get_corner(DOWN + RIGHT), RIGHT, buff=0.005).shift(DOWN * 0.02)
        
        sam_formula = VGroup(sam_prefix, sam_p, sam_paren, sam_theta)
        
        sam_desc2 = create_text("Example: Temperature, Top-p, Top-k", font_size=8, color=GRAY_A)
        sam_content = VGroup(sam_title, sam_desc1, sam_formula, sam_desc2).arrange(DOWN, buff=0.12)
        sam_content.move_to(box_sam.get_center())
        sam_group = VGroup(box_sam, sam_content)

        # Note: visual/narration alignment comment translated from Vietnamese.
        box_con = RoundedRectangle(width=box_width, height=box_height, color=ORANGE, fill_color="#1c130c", fill_opacity=0.8, corner_radius=0.08)
        box_con.move_to(RIGHT * 4.2 + DOWN * 0.5)
        con_title = create_text("3. CONSTRAINTS (Constraints)", font_size=10, color=ORANGE)
        con_desc1 = create_text("Constrain the output space:", font_size=8, color=WHITE)
        con_formula = create_markup_text("<i>y</i> belongs to <i>C</i> (for example: JSON Schema)", font_size=9, color=YELLOW)
        con_desc2 = create_text("Example: DFA / FSM parsing", font_size=8, color=GRAY_A)
        con_content = VGroup(con_title, con_desc1, con_formula, con_desc2).arrange(DOWN, buff=0.12)
        con_content.move_to(box_con.get_center())
        con_group = VGroup(box_con, con_content)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(FadeIn(opt_group, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(sam_group, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(con_group, shift=UP * 0.2), run_time=1.0)
        self.wait(3.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            box_sam.animate.set_opacity(0.25),
            sam_content.animate.set_opacity(0.25),
            box_con.animate.set_opacity(0.25),
            con_content.animate.set_opacity(0.25),
            box_opt.animate.scale(1.05).set_color(YELLOW),
            run_time=1.2
        )
        self.wait(3.5)

        # Note: visual/narration alignment comment translated from Vietnamese.
        self.play(
            FadeOut(opt_group),
            FadeOut(sam_group),
            FadeOut(con_group),
            FadeOut(step4_title),
            FadeOut(sub_title),
            run_time=1.2
        )
        self.wait(1.5)
        finish_voiceovers(self, voiceover_end)
        assert_all_scene_voiceovers_played(self)


# Note: visual/narration alignment comment translated from Vietnamese.
def build_bar_chart(candidates, base_y):
    group = VGroup()
    for idx, item in enumerate(candidates):
        y_pos = base_y - idx * 0.7
        
        lbl = create_text(item["word"], font_size=10, color=WHITE)
        lbl.move_to(RIGHT * 1.5 + UP * y_pos, aligned_edge=LEFT)
        
        bar_len = item["prob"] * 3.0 + 0.05
        bar = RoundedRectangle(width=bar_len, height=0.22, color=item["color"], fill_color=item["color"], fill_opacity=0.9, corner_radius=0.02)
        bar.next_to(lbl, RIGHT, buff=0.2)
        
        val = create_text(f'{item["prob"]:.2f}', font_size=9.5, color=item["color"])
        val.next_to(bar, RIGHT, buff=0.15)
        
        row = VGroup(lbl, bar, val)
        group.add(row)
    return group
