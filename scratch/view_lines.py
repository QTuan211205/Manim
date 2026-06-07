sub_path = "d:/ML/Lab1/subtitle/Subtitle-lab1-ml-clean.txt"
with open(sub_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(100, 250):
    if idx < len(lines):
        print(f"Line {idx}: {lines[idx].strip()}")
