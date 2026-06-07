import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("d:/ML/Lab1/chapter2/scene_2.1/scene_2_1.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "1048" in line or "lor" in line:
        print(f"Line {idx+1}: {line.strip()}")
