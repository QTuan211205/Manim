import os
import tempfile
from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")

class TestRender3(Scene):
    def construct(self):
        self.camera.background_color = "#111111"
        draft_bar_rect = Rectangle(width=1.0, height=2.4, color=ORANGE, fill_color=ORANGE, fill_opacity=0.7)
        ground_line = Line(start=RIGHT * 0.1 + DOWN * 2.6, end=RIGHT * 4.3 + DOWN * 2.6, color=GRAY, stroke_width=2)
        self.add(ground_line)
        draft_bar_rect.next_to(ground_line, UP, buff=0.08)
        draft_bar_rect.set_x(0.8)
        self.add(draft_bar_rect)

class TestRender4(Scene):
    def construct(self):
        self.camera.background_color = "#111111"
        draft_bar_rect = Rectangle(width=1.0, height=2.4, color=ORANGE, fill_color=ORANGE, fill_opacity=0.7)
        ground_line = Line(start=RIGHT * 0.1 + DOWN * 2.6, end=RIGHT * 4.3 + DOWN * 2.6, color=GRAY, stroke_width=2)
        self.add(ground_line)
        draft_bar_rect.next_to(ground_line, UP, buff=0.12)
        draft_bar_rect.set_x(0.8)
        self.add(draft_bar_rect)

config.pixel_width = 854
config.pixel_height = 480
config.frame_rate = 15

scene3 = TestRender3()
scene3.render()

scene4 = TestRender4()
scene4.render()
