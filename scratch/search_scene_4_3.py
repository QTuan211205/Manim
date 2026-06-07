import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("d:/ML/Lab1/full_video_script.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

found = False
start_idx = 0
for idx, line in enumerate(lines):
    if "Phân cảnh 4.3" in line or "Scene 4.3" in line or "4.3:" in line:
        print(f"Found match at line {idx+1}: {line.strip()}")
        start_idx = idx
        found = True

if found:
    # Print the next 150 lines from start_idx
    print("\n--- SCRIPT DETAIL ---")
    for i in range(start_idx, min(start_idx + 150, len(lines))):
        print(f"{i+1}: {lines[i]}", end="")
