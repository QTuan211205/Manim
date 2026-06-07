from manim import *
import os
import tempfile

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")

class TestFormulas2(Scene):
    def construct(self):
        t1 = Text("y ∈ C (Arial)", font="Arial", font_size=36, color=YELLOW).move_to(UP * 1)
        t2 = Text("y ∈ C (Consolas)", font="Consolas", font_size=36, color=YELLOW).move_to(DOWN * 1)
        self.add(t1, t2)
        self.wait(1)
