import sys
sys.stdout.reconfigure(encoding='utf-8')

sub_path = "d:/ML/Lab1/subtitle/Subtitle-lab1-ml-clean.txt"
with open(sub_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

found = []
for idx, line in enumerate(lines):
    if "pagedattention" in line.lower() or "radix" in line.lower() or "hydragen" in line.lower() or "prefix" in line.lower():
        found.append((idx, line.strip()))

print(f"Found {len(found)} matches in subtitles:")
# Group matches that are close together and print them
printed_indices = set()
for idx, line in found:
    if idx in printed_indices:
        continue
    print(f"\n--- SUBTITLE SEGMENT (around line {idx}) ---")
    start = max(0, idx - 5)
    end = min(len(lines), idx + 15)
    for j in range(start, end):
        print(f"{j}: {lines[j].strip()}")
        printed_indices.add(j)
