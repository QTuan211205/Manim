import os

sub_path = "d:/ML/Lab1/subtitle/Subtitle-lab1-ml.txt"
with open(sub_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("File has", len(lines), "lines.")
found = []
for idx, line in enumerate(lines):
    if "Taylor" in line or "tự hồi quy" in line or "Chương II" in line or "cơ bản" in line or "Primitive" in line:
        found.append((idx, line.strip()))

print(f"Found {len(found)} occurrences in Subtitle-lab1-ml.txt:")
for idx, line in found[:30]:
    print(f"Line {idx}: {line}")
