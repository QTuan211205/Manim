import sys
# Make sure we don't try to open a window
from manim import *

# Initialize a dummy scene or just construct the mobject
start = RIGHT * 4.6 + UP * 0.55
end = RIGHT * 2.8 + UP * 0.55

# Test with negative angle
arrow_neg = CurvedArrow(start, end, angle=-TAU/3.2)
points_neg = arrow_neg.points
max_y_neg = max(p[1] for p in points_neg)
min_y_neg = min(p[1] for p in points_neg)

# Test with positive angle
arrow_pos = CurvedArrow(start, end, angle=TAU/3.2)
points_pos = arrow_pos.points
max_y_pos = max(p[1] for p in points_pos)
min_y_pos = min(p[1] for p in points_pos)

print(f"Start/End Y: {start[1]}")
print(f"Negative angle Y range: {min_y_neg} to {max_y_neg}")
print(f"Positive angle Y range: {min_y_pos} to {max_y_pos}")
