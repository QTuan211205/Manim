import os
import tempfile
from pathlib import Path
from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000

VOICEOVER_DIR = Path(__file__).resolve().parents[3] / "voiceover" / "generated_sentence_level"

SCENE_2_5_DURATIONS = {
    "sc25_001.mp3": 6.130068,
    "sc25_002.mp3": 16.904127,
    "sc25_003.mp3": 7.058866,
    "sc25_004.mp3": 12.399456,
    "sc25_005.mp3": 8.591383,
    "sc25_006.mp3": 5.387029,
    "sc25_007.mp3": 4.272472,
    "sc25_008.mp3": 6.501587,
    "sc25_009.mp3": 5.665669,
    "sc25_010.mp3": 11.935057,
    "sc25_011.mp3": 6.083628,
    "sc25_012.mp3": 3.250794,
    "sc25_013.mp3": 15.278730,
    "sc25_014.mp3": 3.297234,
    "sc25_015.mp3": 2.832834,
    "sc25_016.mp3": 4.179592,
    "sc25_017.mp3": 9.752381,
    "sc25_018.mp3": 6.315828,
    "sc25_019.mp3": 6.130068,
    "sc25_020.mp3": 5.851429,
}
SCENE_2_5_VOICEOVERS = tuple(SCENE_2_5_DURATIONS)


def validate_scene_voiceover_files():
    available = sorted(path.name for path in VOICEOVER_DIR.glob("sc25_*.mp3"))
    expected = sorted(SCENE_2_5_VOICEOVERS)
    if available != expected:
        missing = sorted(set(expected) - set(available))
        extra = sorted(set(available) - set(expected))
        raise FileNotFoundError(
            f"Scene 2.5 voiceover mismatch. Missing: {missing or 'none'}; extra: {extra or 'none'}"
        )


def add_voiceover(scene, filename, time_offset=0.0, duration=0.0):
    if filename not in SCENE_2_5_DURATIONS:
        raise KeyError(f"Unexpected Scene 2.5 voiceover: {filename}")
    if not (VOICEOVER_DIR / filename).exists():
        raise FileNotFoundError(f"Missing Scene 2.5 voiceover file: {filename}")
    scene.add_sound(str(VOICEOVER_DIR / filename), time_offset=time_offset)
    scene.played_voiceovers.append(filename)
    return time_offset + duration


def schedule_scene_voiceovers(scene):
    validate_scene_voiceover_files()
    scene.played_voiceovers = []
    voiceover_end = 0.0
    for filename, duration in SCENE_2_5_DURATIONS.items():
        voiceover_end = add_voiceover(scene, filename, voiceover_end, duration)
    return voiceover_end


def assert_all_scene_voiceovers_played(scene):
    played = tuple(scene.played_voiceovers)
    expected = tuple(SCENE_2_5_VOICEOVERS)
    if played != expected:
        missing = [filename for filename in expected if filename not in played]
        raise RuntimeError(
            f"Scene 2.5 did not schedule every voiceover. Played: {played}; missing: {missing or 'none'}"
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


class Scene2_5(Scene):

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
        for idx, (filename, duration) in enumerate(SCENE_2_5_DURATIONS.items(), start=1):
            cue_start[idx] = current
            current += duration

        title = create_text("Sampling Adapters & Constrained Decoding", font_size=30, color=YELLOW)
        subtitle = create_text("Modifying and structuring model outputs", font_size=16, color=GRAY_A)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.18)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.8)

        content = None

        # --- Cue 1: Intro to Sampling Adapters ---
        self.wait_until(cue_start[1] + 0.25)
        intro_pill = pill("Sampling Adapter: Adjusts next-token probabilities", 6.8, BLUE_B, "#111a25", font_size=20)
        content = self.replace_content(content, intro_pill)

        # --- Cue 2: Sampling Adapters Table ---
        self.wait_until(cue_start[2] + 0.25)
        table_box = RoundedRectangle(
            width=11.6, height=3.8, color=BLUE_B, fill_color="#101720", fill_opacity=0.95, corner_radius=0.08
        ).move_to(DOWN * 0.1)
        table_title = create_text("Sampling Adapters Classification", font_size=14, color=BLUE_A, weight=BOLD).next_to(table_box.get_top(), DOWN, buff=0.15)
        
        headers = VGroup(
            create_markup_text("<b>Method</b>", font_size=10, color=YELLOW),
            create_markup_text("<b>Formula / Purpose</b>", font_size=10, color=YELLOW),
            create_markup_text("<b>Adapter Type</b>", font_size=10, color=YELLOW)
        )
        headers[0].move_to(LEFT * 4.6 + UP * 1.0, aligned_edge=LEFT)
        headers[1].move_to(LEFT * 1.4 + UP * 1.0, aligned_edge=LEFT)
        headers[2].move_to(RIGHT * 2.3 + UP * 1.0, aligned_edge=LEFT)
        
        rows = VGroup()
        row_y_starts = 0.6
        row_spacing = 0.36
        
        table_data = [
            ("Typical sampling", "y ~ q(p_theta)", "Truncation (entropy)"),
            ("Mirostat decoding", "Target perplexity", "Truncation (adaptive top-k)"),
            ("Basis-aware sampling", "y ~ q(p_theta)", "Truncation (linear program)"),
            ("Contrastive decoding", "log p_expert - log p_antiexpert", "Contrastive & truncation"),
            ("DExperts", "p_theta * (p_expert+ / p_expert-)^alpha", "Logits adjustment"),
            ("Inference-time adapters", "p_theta * reward_model^alpha", "Logits adjustment"),
            ("Proxy tuning", "p_theta * (p_tuned / p_untuned)", "Logits adjustment")
        ]
        
        for idx, (m, f, a) in enumerate(table_data):
            y_pos = row_y_starts - idx * row_spacing
            col1 = create_text(m, font_size=9, color=WHITE)
            col1.move_to(LEFT * 4.6 + UP * y_pos, aligned_edge=LEFT)
            
            col2 = create_text(f, font_size=9, color=BLUE_A)
            col2.move_to(LEFT * 1.4 + UP * y_pos, aligned_edge=LEFT)
            
            col3 = create_text(a, font_size=9, color=GRAY_A)
            col3.move_to(RIGHT * 2.3 + UP * y_pos, aligned_edge=LEFT)
            
            rows.add(VGroup(col1, col2, col3))
            
        table_group = VGroup(table_box, table_title, headers, rows)
        content = self.replace_content(content, table_group)

        # --- Cue 3: Constrained Decoding Intro ---
        self.wait_until(cue_start[3] + 0.2)
        cd_title = create_text("Constrained Decoding", font_size=22, color=GREEN).move_to(UP * 1.6)
        
        schema_box = RoundedRectangle(
            width=3.6, height=3.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08
        )
        schema_box.move_to(LEFT * 4.2 + DOWN * 0.4)
        
        schema_title = create_markup_text("<b>JSON Schema</b>", font_size=13, color=YELLOW)
        schema_title.next_to(schema_box.get_top(), DOWN, buff=0.18)
        
        schema_code = create_text(
            "{\n"
            '  "name": "string",\n'
            '  "birth year": "int"\n'
            "}",
            font_size=13, color=LIGHT_GREY, line_spacing=1.3
        )
        schema_code.next_to(schema_title, DOWN, buff=0.2)
        schema_group = VGroup(schema_box, schema_title, schema_code)
        
        cd_intro_text = create_text(
            "Forces the LLM to output structured data\nthat conforms exactly to a schema.",
            font_size=16, color=WHITE
        ).move_to(RIGHT * 2.2 + DOWN * 0.4)
        
        cd_group = VGroup(cd_title, schema_group, cd_intro_text)
        content = self.replace_content(content, cd_group)

        # --- Cue 4: Free-form Output Issue ---
        self.wait_until(cue_start[4] + 0.25)
        invalid_output_title = create_text("Free-form LLM Output:", font_size=14, color=RED_B)
        invalid_output_title.move_to(RIGHT * 2.2 + UP * 0.4)
        
        invalid_output_val = create_text(
            '"Taylor Swift was born in 1989."',
            font_size=16, color=RED_A
        ).next_to(invalid_output_title, DOWN, buff=0.2)
        
        invalid_label = create_text("Error: Output is not valid JSON!", font_size=13, color=RED)
        invalid_label.next_to(invalid_output_val, DOWN, buff=0.25)
        
        invalid_group = VGroup(invalid_output_title, invalid_output_val, invalid_label)
        
        self.play(
            FadeOut(cd_intro_text),
            FadeIn(invalid_group, shift=UP * 0.1),
            run_time=0.6
        )

        # --- Cue 5: State Machine & Vocabulary Filtering ---
        self.wait_until(cue_start[5] + 0.25)
        self.play(
            FadeOut(invalid_group),
            FadeOut(cd_title),
            run_time=0.5
        )
        
        # Reposition Schema box slightly to make room
        self.play(schema_group.animate.move_to(LEFT * 4.8 + UP * 0.8), run_time=0.6)
        
        # State machine nodes
        s0_pos = LEFT * 2.2 + UP * 1.8
        s1_pos = LEFT * 0.6 + UP * 1.8
        s2_pos = RIGHT * 1.0 + UP * 1.8
        s6_pos = RIGHT * 2.6 + UP * 1.8
        s4_pos = LEFT * 0.6 + UP * 0.0
        s7_pos = RIGHT * 1.0 + UP * 0.0
        s8_pos = RIGHT * 2.6 + UP * 0.0
        
        def make_node(label_text, pos, is_double=False):
            circle = Circle(radius=0.26, color=WHITE, stroke_width=2)
            circle.move_to(pos)
            lbl = create_text(label_text, font_size=9, color=WHITE)
            lbl.move_to(pos)
            if is_double:
                circle_in = Circle(radius=0.20, color=WHITE, stroke_width=1.5)
                circle_in.move_to(pos)
                return VGroup(circle, circle_in, lbl)
            return VGroup(circle, lbl)
            
        node0 = make_node("S0", s0_pos)
        node1 = make_node("S1", s1_pos)
        node2 = make_node("S2", s2_pos)
        node6 = make_node("S6", s6_pos)
        node4 = make_node("S4", s4_pos)
        node7 = make_node("S7", s7_pos)
        node8 = make_node("S8", s8_pos, is_double=True)
        nodes = VGroup(node0, node1, node2, node6, node4, node7, node8)
        
        def make_arrow(start_pos, end_pos, label_text, edge_buff=0.27, label_side=UP, label_buff=0.12):
            arrow = Arrow(start=start_pos, end=end_pos, color=GRAY_A, stroke_width=1.5, buff=edge_buff, max_tip_length_to_length_ratio=0.15)
            lbl = create_text(label_text, font_size=10, color=GRAY_B)
            lbl.next_to(arrow, label_side, buff=label_buff)
            return VGroup(arrow, lbl)
            
        arr0_1 = make_arrow(s0_pos, s1_pos, "'{'", label_side=UP)
        arr1_2 = make_arrow(s1_pos, s2_pos, '"name": "', label_side=UP)
        arr2_6 = make_arrow(s2_pos, s6_pos, "[A-Za-z]", label_side=UP)
        
        loop6 = Arc(radius=0.15, start_angle=-30*DEGREES, angle=240*DEGREES, color=GRAY_A, stroke_width=1.5)
        loop6.next_to(node6, UP, buff=0.01).shift(RIGHT * 0.1)
        loop6_tip = ArrowTriangleFilledTip(color=GRAY_A).scale(0.12)
        loop6_tip.move_to(loop6.get_start()).rotate(-70*DEGREES)
        loop6_lbl = create_text("[A-Za-z]", font_size=10, color=GRAY_B).next_to(loop6, UP, buff=0.05)
        loop6_group = VGroup(loop6, loop6_tip, loop6_lbl)
        
        arr6_4 = make_arrow(s6_pos, s4_pos, '", "birth year": ', label_side=LEFT, label_buff=0.02)
        arr4_7 = make_arrow(s4_pos, s7_pos, "\\d", label_side=DOWN)
        
        loop7 = Arc(radius=0.15, start_angle=-30*DEGREES, angle=240*DEGREES, color=GRAY_A, stroke_width=1.5)
        loop7.next_to(node7, UP, buff=0.01).shift(RIGHT * 0.1)
        loop7_tip = ArrowTriangleFilledTip(color=GRAY_A).scale(0.12)
        loop7_tip.move_to(loop7.get_start()).rotate(-70*DEGREES)
        loop7.rotate(180 * DEGREES, about_point=s7_pos)
        loop7_tip.rotate(180 * DEGREES, about_point=s7_pos)
        loop7_lbl = create_text("\\d", font_size=10, color=GRAY_B).next_to(loop7, DOWN, buff=0.05)
        loop7_group = VGroup(loop7, loop7_tip, loop7_lbl)
        
        arr7_8 = make_arrow(s7_pos, s8_pos, "'}'", label_side=DOWN)
        arrows = VGroup(arr0_1, arr1_2, arr2_6, loop6_group, arr6_4, arr4_7, loop7_group, arr7_8)
        
        # Vocabulary Box on the right
        vocab_box = RoundedRectangle(
            width=3.6, height=4.2, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08
        ).move_to(RIGHT * 5.0 + UP * 0.2)
        vocab_title = create_text("Vocabulary & Probabilities", font_size=11, color=YELLOW)
        vocab_title.next_to(vocab_box.get_top(), DOWN, buff=0.15)
        vocab_group = VGroup(vocab_box, vocab_title)
        
        # Result Box at the bottom
        result_box = RoundedRectangle(
            width=12.5, height=1.0, color=GRAY_E, fill_color="#141517", fill_opacity=0.9, corner_radius=0.08
        ).move_to(DOWN * 2.8)
        result_label = create_text("Generated JSON:", font_size=11, color=GRAY_B)
        result_label.move_to(result_box.get_left() + RIGHT * 1.2)
        result_group = VGroup(result_box, result_label)
        
        self.play(
            FadeIn(nodes), FadeIn(arrows),
            FadeIn(vocab_group), FadeIn(result_group),
            run_time=1.0
        )
        
        current_node_highlight = Circle(radius=0.28, color=GREEN, stroke_width=3).move_to(s0_pos)
        self.play(Create(current_node_highlight), run_time=0.4)

        # --- Cue 6: Step 1: Open brace '{' ---
        self.wait_until(cue_start[6] + 0.2)
        
        def show_vocab_list(items, chosen_idx):
            list_group = VGroup()
            for i, (tok, pr, lg, valid) in enumerate(items):
                tok_color = GREEN if valid else RED
                if '"' in tok:
                    tok_lbl = create_text(f"'{tok}'", font_size=10, color=tok_color)
                else:
                    tok_lbl = create_text(f'"{tok}"', font_size=10, color=tok_color)
                
                if i == chosen_idx:
                    tok_lbl.set_color(YELLOW)
                    bg_highlight = BackgroundRectangle(tok_lbl, color=YELLOW, fill_opacity=0.15, buff=0.05)
                    item_v = VGroup(bg_highlight, tok_lbl)
                else:
                    item_v = VGroup(tok_lbl)
                    
                pr_lbl = create_text(f"P: {pr}", font_size=9, color=WHITE if valid else RED)
                lg_lbl = create_text(f"Logit: {lg}", font_size=9, color=WHITE if valid else RED)
                
                item_row = VGroup(item_v, pr_lbl, lg_lbl).arrange(RIGHT, buff=0.3)
                item_row.move_to(RIGHT * 5.0 + UP * (1.2 - i * 0.75))
                
                if not valid:
                    strike_line = Line(
                        item_row.get_left() - LEFT*0.1, item_row.get_right() + LEFT*0.1,
                        color=RED_E, stroke_width=1.5
                    )
                    item_row.add(strike_line)
                    
                list_group.add(item_row)
            return list_group

        vocab_items_1 = [
            ("\\n", "0.36", "1.20", False),
            ('"', "0.16", "0.80", False),
            ("{", "0.026", "0.10", True),
            ("https", "0.025", "0.08", False)
        ]
        
        vocab_list_1 = show_vocab_list(vocab_items_1, chosen_idx=2)
        self.play(FadeIn(vocab_list_1), run_time=0.8)
        
        self.wait(1.5)
        current_json_text = "{"
        json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        json_display.next_to(result_label, RIGHT, buff=0.3)
        
        self.play(
            FadeIn(json_display),
            current_node_highlight.animate.move_to(s1_pos),
            arr0_1[0].animate.set_color(GREEN),
            run_time=0.8
        )
        self.play(FadeOut(vocab_list_1), run_time=0.4)

        # --- Cue 7: Step 2: Key "name" ---
        self.wait_until(cue_start[7] + 0.2)
        vocab_items_2 = [
            ("name\": \"", "0.31", "1.10", True),
            ("date\": \"", "0.069", "0.20", False),
            ("\"", "0.039", "0.12", False),
            ("id\": \"", "0.033", "0.10", False)
        ]
        
        vocab_list_2 = show_vocab_list(vocab_items_2, chosen_idx=0)
        self.play(FadeIn(vocab_list_2), run_time=0.8)
        
        self.wait(1.0)
        current_json_text += ' "name": "'
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)
        
        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s2_pos),
            arr1_2[0].animate.set_color(GREEN),
            run_time=0.8
        )
        json_display = new_json_display
        self.play(FadeOut(vocab_list_2), run_time=0.4)

        # --- Cue 8: Step 3-8: Fast-forward JSON assembly ---
        self.wait_until(cue_start[8] + 0.25)
        
        # A. Land on "Taylor Swift" (S2 -> S6)
        current_json_text += "Taylor Swift"
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)
        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s6_pos),
            arr2_6[0].animate.set_color(GREEN),
            run_time=0.6
        )
        json_display = new_json_display
        self.wait(0.3)
        
        # B. Land on '", "birth year": ' (S6 -> S4)
        current_json_text += '", "birth year": '
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)
        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s4_pos),
            arr6_4[0].animate.set_color(GREEN),
            run_time=0.6
        )
        json_display = new_json_display
        self.wait(0.3)
        
        # C. Land on '1989' (S4 -> S7)
        current_json_text += '1989'
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)
        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s7_pos),
            arr4_7[0].animate.set_color(GREEN),
            run_time=0.6
        )
        json_display = new_json_display
        self.wait(0.3)
        
        # D. Land on '}' (S7 -> S8)
        current_json_text += '}'
        new_json_display = create_text(current_json_text, font_size=13, color=GREEN, font="Courier New")
        new_json_display.next_to(result_label, RIGHT, buff=0.3)
        self.play(
            ReplacementTransform(json_display, new_json_display),
            current_node_highlight.animate.move_to(s8_pos),
            arr7_8[0].animate.set_color(GREEN),
            run_time=0.6
        )
        json_display = new_json_display
        
        success_flash = Circle(radius=0.36, color=GREEN, stroke_width=4).move_to(s8_pos)
        self.play(Create(success_flash), run_time=0.4)
        self.play(FadeOut(success_flash), run_time=0.4)

        # --- Cue 9: Side Effects of Constrained Decoding ---
        self.wait_until(cue_start[9] + 0.25)
        self.play(
            FadeOut(schema_group),
            FadeOut(nodes), FadeOut(arrows),
            FadeOut(vocab_group),
            FadeOut(result_group), FadeOut(json_display), FadeOut(current_node_highlight),
            run_time=0.5
        )
        
        side_effects_title = create_text("Side Effects of Constrained Decoding", font_size=22, color=BLUE_A).move_to(UP * 1.6)
        
        slide_box = RoundedRectangle(
            width=8.0, height=3.5, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.1
        ).move_to(DOWN * 0.2)
        
        bullet_speedup = create_markup_text(
            "• <span color='#55ff55'>Generation Speedup</span>: Speeds up generation\n"
            "  by automatically filling paths with only one valid token.",
            font_size=11, color=WHITE
        )
        bullet_performance = create_markup_text(
            "• <span color='#ffaa55'>Reduced Performance / Bias</span>: Restricts sampling paths,\n"
            "  which can force unnatural sentence structures.",
            font_size=11, color=WHITE
        )
        bullets = VGroup(bullet_speedup, bullet_performance).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        bullets.move_to(slide_box.get_center())
        
        self.play(
            FadeIn(side_effects_title),
            FadeIn(slide_box),
            FadeIn(bullets, shift=UP * 0.15),
            run_time=0.8
        )

        # --- Cue 10: Token Boundary Shift & Token Healing ---
        self.wait_until(cue_start[10] + 0.2)
        self.play(
            FadeOut(side_effects_title),
            FadeOut(slide_box),
            FadeOut(bullets),
            run_time=0.5
        )
        
        th_title = create_text("Token Boundary Shift & Token Healing", font_size=22, color=ORANGE).move_to(UP * 1.6)
        
        prompt_label = create_text("Prompt ends with forced prefix:", font_size=12, color=GRAY_A).move_to(UP * 0.8)
        prompt_val = create_text('"The URL is http:"', font_size=18, color=YELLOW).next_to(prompt_label, DOWN, buff=0.15)
        prompt_group = VGroup(prompt_label, prompt_val)
        
        segment_label = create_text("Standard Tokenization (Boundary shifted):", font_size=12, color=GRAY_B)
        segment_label.move_to(LEFT * 3.9 + DOWN * 0.4, aligned_edge=LEFT)
        
        def make_block(text, width, pos, color=BLUE_D):
            rect = RoundedRectangle(
                width=width, height=0.6, corner_radius=0.08,
                color=color, fill_color=color, fill_opacity=0.8
            )
            rect.move_to(pos)
            lbl = create_text(text, font_size=10, color=WHITE)
            lbl.move_to(pos)
            return VGroup(rect, lbl)
            
        b1 = make_block("The", 0.8, LEFT * 3.5 + DOWN * 1.2)
        b2 = make_block(" URL", 0.9, LEFT * 2.6 + DOWN * 1.2)
        b3 = make_block(" is", 0.7, LEFT * 1.75 + DOWN * 1.2)
        b4 = make_block(" http", 1.0, LEFT * 0.85 + DOWN * 1.2)
        b5 = make_block(":", 0.45, RIGHT * 0.0 + DOWN * 1.2, color=RED)
        blocks_group_1 = VGroup(b1, b2, b3, b4, b5)
        
        b_next_wrong = make_block("//", 0.7, RIGHT * 0.9 + DOWN * 1.2, color=RED_E)
        
        warning_icon = create_markup_text(
            "<b>[!] Segmentation error</b>\nToken sequence <i>[http] + [:] + [//]</i>\nnever appeared during pretraining!",
            font_size=10, color=RED
        ).next_to(b_next_wrong, RIGHT, buff=0.75).shift(UP * 0.15)
        
        warn_border = RoundedRectangle(width=1.7, height=0.9, color=RED, stroke_width=2.5).move_to(RIGHT * 0.51 + DOWN * 1.2)
        
        self.play(
            FadeIn(th_title),
            FadeIn(prompt_group),
            FadeIn(segment_label),
            LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in blocks_group_1], lag_ratio=0.15),
            run_time=1.0
        )
        
        self.wait(1.5)
        self.play(
            FadeIn(b_next_wrong, shift=LEFT * 0.15),
            Create(warn_border),
            FadeIn(warning_icon),
            run_time=0.8
        )

        # --- Cue 11: Token Healing Solution ---
        self.wait_until(cue_start[11] + 0.2)
        self.play(
            FadeOut(b_next_wrong),
            FadeOut(warn_border),
            FadeOut(warning_icon),
            run_time=0.5
        )
        
        healing_label = create_text("Token Healing Solution (Boundary healed):", font_size=12, color=GREEN)
        healing_label.move_to(LEFT * 3.9 + DOWN * 0.4, aligned_edge=LEFT)
        
        self.play(
            ReplacementTransform(segment_label, healing_label),
            b5[0].animate.set_color(WHITE).set_opacity(0.3),
            run_time=0.8
        )
        self.wait(1.0)
        self.play(FadeOut(b5), run_time=0.4)
        
        prompt_val_healed = create_text('"The URL is http"', font_size=18, color=GREEN).move_to(prompt_val.get_center())
        
        candidates_box = RoundedRectangle(
            width=5.0, height=2.0, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08
        ).move_to(RIGHT * 3.5 + DOWN * 1.2)
        cand_title = create_text("Vocabulary Candidates", font_size=10, color=YELLOW).next_to(candidates_box.get_top(), DOWN, buff=0.15)
        cand_1 = create_markup_text("s:// <span color='#ffaa55'>(Filtered: does not match ':')</span>", font_size=9, color=WHITE).next_to(cand_title, DOWN, buff=0.25).align_to(cand_title, LEFT).shift(LEFT * 0.5)
        cand_2 = create_markup_text("<b>://</b> <span color='#55ff55'>(Matches prefix constraint)</span>", font_size=9, color=WHITE).next_to(cand_1, DOWN, buff=0.2).align_to(cand_1, LEFT)
        candidates_group = VGroup(candidates_box, cand_title, cand_1, cand_2)
        
        self.play(
            ReplacementTransform(prompt_val, prompt_val_healed),
            FadeIn(candidates_group),
            run_time=0.8
        )
        
        self.wait(1.5)
        strike_cand1 = Line(cand_1.get_left(), cand_1.get_right(), color=RED, stroke_width=1.5)
        b_next_healed = make_block("://", 0.7, RIGHT * 0.12 + DOWN * 1.2, color=GREEN)
        
        self.play(
            Create(strike_cand1),
            cand_1.animate.set_opacity(0.4),
            cand_2.animate.set_color(YELLOW),
            FadeIn(b_next_healed, shift=LEFT * 0.1),
            run_time=0.8
        )

        # --- Cue 12: Tokenizer Regularization ---
        self.wait_until(cue_start[12] + 0.2)
        self.play(
            FadeOut(candidates_group),
            FadeOut(strike_cand1),
            run_time=0.5
        )
        
        regularization_note = create_markup_text(
            "<span color='#88bbff'>Alternative Solution:</span> Tokenizer Regularization (BPE-Dropout) during training [Kudo, 2018]",
            font_size=11, color=LIGHT_GREY
        ).move_to(DOWN * 2.2)
        
        self.play(Write(regularization_note), run_time=0.8)

        # --- Cue 13: Summary: Primitive Generators ---
        self.wait_until(cue_start[13] + 0.25)
        self.play(
            FadeOut(th_title),
            FadeOut(prompt_group),
            FadeOut(prompt_val_healed),
            FadeOut(healing_label),
            FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b4), FadeOut(b_next_healed),
            FadeOut(regularization_note),
            run_time=0.5
        )
        
        sum_title = create_text("Summary: Primitive Generators", font_size=24, color=YELLOW).move_to(UP * 1.8)
        
        sum_bullet_1 = create_markup_text(
            "1. <span color='#55ff55'>Decoding Views</span>: Optimization (Greedy, Beam Search) vs.\n"
            "   Sampling (Ancestral, Truncation).",
            font_size=13, color=WHITE
        )
        sum_bullet_2 = create_markup_text(
            "2. <span color='#ffaa55'>Diversity-Coherence Trade-off</span>: Controlled by Temperature\n"
            "   and Truncation to manage tail probabilities.",
            font_size=13, color=WHITE
        )
        sum_bullet_3 = create_markup_text(
            "3. <span color='#88bbff'>Constrained Decoding</span>: Enforces structure on output tokens\n"
            "   using schemas compiled to state machines.",
            font_size=13, color=WHITE
        )
        sum_bullets = VGroup(sum_bullet_1, sum_bullet_2, sum_bullet_3).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        sum_bullets.move_to(DOWN * 0.2)
        
        self.play(
            FadeIn(sum_title),
            FadeIn(sum_bullets, shift=UP * 0.15),
            run_time=0.8
        )

        # --- Cue 14: Building Blocks ---
        self.wait_until(cue_start[14] + 0.2)
        building_blocks_lbl = create_text("Building blocks of modern LLM generation methods.", font_size=14, color=GRAY_A)
        building_blocks_lbl.next_to(sum_bullets, DOWN, buff=0.35)
        self.play(FadeIn(building_blocks_lbl), run_time=0.6)

        # --- Cue 15: Sampling Adapters as Transformation Layers ---
        self.wait_until(cue_start[15] + 0.2)
        self.play(
            FadeOut(sum_title),
            FadeOut(sum_bullets),
            FadeOut(building_blocks_lbl),
            run_time=0.5
        )
        
        layer_title = create_text("Sampling Adapters: Transformation Layers", font_size=22, color=YELLOW).move_to(UP * 1.8)
        
        # Draw transformation flowchart
        flow_logits = token("LLM Logits", color=GRAY_B)
        flow_softmax = token("Softmax", color=GRAY_C)
        flow_adapter = token("Adapter", color=YELLOW)
        flow_sample = token("Sample", color=GREEN_B)
        flow_token = token("Next Token", color=GREEN)
        
        flowchart = VGroup(
            flow_logits, Arrow(LEFT, RIGHT, color=GRAY_C, stroke_width=2).scale(0.5),
            flow_softmax, Arrow(LEFT, RIGHT, color=GRAY_C, stroke_width=2).scale(0.5),
            flow_adapter, Arrow(LEFT, RIGHT, color=GRAY_C, stroke_width=2).scale(0.5),
            flow_sample, Arrow(LEFT, RIGHT, color=GRAY_C, stroke_width=2).scale(0.5),
            flow_token
        ).arrange(RIGHT, buff=0.15).move_to(UP * 0.2)
        
        adapter_label = create_text(
            "Transforms the raw output distribution (p_theta) without replacing the model itself.\n"
            "Examples: Temperature, Truncation, Contrastive Decoding, DExperts.",
            font_size=13, color=GRAY_A
        ).next_to(flowchart, DOWN, buff=0.5)
        
        self.play(
            FadeIn(layer_title),
            FadeIn(flowchart),
            FadeIn(adapter_label),
            run_time=0.8
        )

        # --- Cue 16: Readjust probabilities ---
        self.wait_until(cue_start[16] + 0.2)
        self.play(
            flow_adapter.animate.set_color(GREEN_B),
            run_time=0.5
        )

        # --- Cue 17: transformation layers ---
        self.wait_until(cue_start[17] + 0.2)
        self.play(
            flow_adapter.animate.set_color(YELLOW),
            run_time=0.5
        )

        # --- Cue 18: Constrained Decoding State Machine Concept ---
        self.wait_until(cue_start[18] + 0.2)
        self.play(
            FadeOut(layer_title),
            FadeOut(flowchart),
            FadeOut(adapter_label),
            run_time=0.5
        )
        
        cd_sum_title = create_text("Summary: Constrained Decoding", font_size=22, color=GREEN).move_to(UP * 1.8)
        
        # Split screen
        # Left side: Schema -> State Machine
        left_box = RoundedRectangle(width=5.5, height=3.2, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        left_box.move_to(LEFT * 3.2 + DOWN * 0.2)
        left_lbl = create_markup_text(
            "<b>Schema Compiler</b>\n\nJSON Schema\n  ↓\nState Machine\n  ↓\nAllowed Token Mask",
            font_size=12, color=WHITE
        ).move_to(left_box.get_center())
        left_group = VGroup(left_box, left_lbl)
        
        # Right side: Gate mechanism
        right_box = RoundedRectangle(width=5.5, height=3.2, color=GRAY_E, fill_color="#181a1e", fill_opacity=0.9, corner_radius=0.08)
        right_box.move_to(RIGHT * 3.2 + DOWN * 0.2)
        right_lbl = create_markup_text(
            "<b>Token Filtering</b>\n\nModel Distribution\n  ↓\nState Machine Filter (Gate)\n  ↓\nRenormalized Output",
            font_size=12, color=WHITE
        ).move_to(right_box.get_center())
        right_group = VGroup(right_box, right_lbl)
        
        self.play(
            FadeIn(cd_sum_title),
            FadeIn(left_group),
            FadeIn(right_group),
            run_time=0.8
        )

        # --- Cue 19: Filter out invalid tokens ---
        self.wait_until(cue_start[19] + 0.2)
        self.play(
            right_box.animate.set_color(GREEN),
            run_time=0.5
        )

        # --- Cue 20: Structured output JSON communication ---
        self.wait_until(cue_start[20] + 0.2)
        self.play(
            left_box.animate.set_color(GREEN),
            run_time=0.5
        )

        # --- End of Scene ---
        self.wait_until(voiceover_end + 0.35)
        self.play(
            FadeOut(cd_sum_title),
            FadeOut(left_group),
            FadeOut(right_group),
            FadeOut(header),
            run_time=0.8
        )
        assert_all_scene_voiceovers_played(self)
