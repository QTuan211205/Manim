import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("d:/ML/Lab1/full_video_script.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "CHƯƠNG 4" in line or "Chương IV" in line or "4." in line:
        print(f"Line {idx+1}: {line.strip()}")
