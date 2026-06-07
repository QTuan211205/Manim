import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("d:/ML/Lab1/full_video_script.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(332, min(384, len(lines))):
    print(f"{i+1}: {lines[i]}", end="")
