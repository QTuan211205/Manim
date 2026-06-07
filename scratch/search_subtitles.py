import os

sub_path = "d:/ML/Lab1/subtitle/Subtitle-lab1-ml-clean.txt"
with open(sub_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("File has", len(lines), "lines.")
# Let's search for "Taylor" or "Primitive Generators"
found = []
for idx, line in enumerate(lines):
    if "Taylor" in line or "Primitive" in line or "autoregressive" in line or "tự hồi quy" in line:
        found.append((idx, line.strip()))

print(f"Found {len(found)} occurrences:")
for idx, line in found[:20]:
    print(f"Line {idx}: {line}")
