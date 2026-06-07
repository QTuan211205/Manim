from manim import *

draft_bar_rect = Rectangle(width=1.0, height=2.4, color=ORANGE, fill_color=ORANGE, fill_opacity=0.7)
ground_line = Line(start=RIGHT * 0.1 + DOWN * 2.6, end=RIGHT * 4.3 + DOWN * 2.6, color=GRAY, stroke_width=2)

print("With buff=0:")
draft_bar_rect.next_to(ground_line, UP, buff=0)
print("  bottom:", draft_bar_rect.get_bottom()[1])

print("With buff=0.15:")
draft_bar_rect.next_to(ground_line, UP, buff=0.15)
print("  bottom:", draft_bar_rect.get_bottom()[1])
