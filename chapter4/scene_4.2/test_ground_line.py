import os
import tempfile
import numpy as np
from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")

class TestGroundLine(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Tạo 3 cột giống scene chính
        draft_bar_rect = Rectangle(width=1.0, height=2.4, color=ORANGE, fill_color=ORANGE, fill_opacity=0.7)
        target_bar_rect = Rectangle(width=1.0, height=0.6, color=BLUE, fill_color=BLUE, fill_opacity=0.7)
        target_alt_rect = Rectangle(width=1.0, height=2.1, color=GREEN_C, fill_color=GREEN_C, fill_opacity=0.7)

        baseline_y = -2.6
        draft_bar_rect.move_to(np.array([0.8, baseline_y + 2.4 / 2, 0]))
        target_bar_rect.move_to(np.array([2.2, baseline_y + 0.6 / 2, 0]))
        target_alt_rect.move_to(np.array([3.6, baseline_y + 2.1 / 2, 0]))

        # Vẽ đường kẻ ngang ở dưới cùng các cột
        ground_line = Line(
            start=np.array([0.1, 0, 0]),
            end=np.array([4.3, 0, 0]),
            color=GRAY, stroke_width=2
        )
        ground_line.next_to(draft_bar_rect, DOWN, buff=0)
        ground_y = ground_line.get_center()[1]
        ground_line.put_start_and_end_on(
            np.array([0.1, ground_y, 0]),
            np.array([4.3, ground_y, 0])
        )

        self.add(draft_bar_rect, target_bar_rect, target_alt_rect, ground_line)

        # Debug: print positions
        print(f"draft_bar bottom: {draft_bar_rect.get_bottom()}")
        print(f"target_bar bottom: {target_bar_rect.get_bottom()}")
        print(f"target_alt bottom: {target_alt_rect.get_bottom()}")
        print(f"ground_line center Y: {ground_line.get_center()[1]}")
        print(f"ground_line top: {ground_line.get_top()}")
        print(f"ground_line bottom: {ground_line.get_bottom()}")
