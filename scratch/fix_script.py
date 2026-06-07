path = r"d:\ML\Lab1\full_video_script.md"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix form feed from \frac
text = text.replace("\x0crac", "\\frac")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed additional LaTeX escape characters in full_video_script.md")
