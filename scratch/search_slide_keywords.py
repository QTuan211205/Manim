import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("d:/ML/Lab1/slide/pdf_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

found = []
keywords = ["PagedAttention", "RadixAttention", "Hydrogen", "prefix", "prefix tree", "shared prefix"]
for idx, line in enumerate(lines):
    for kw in keywords:
        if kw.lower() in line.lower():
            found.append((idx, kw, line.strip()))
            break

print(f"Found {len(found)} matches:")
# Print around matches to see slide numbers (e.g. --- PAGE X ---)
for idx, kw, line in found:
    # scan backwards to find PAGE number
    page = "Unknown"
    for j in range(idx, -1, -1):
        if "--- PAGE" in lines[j]:
            page = lines[j].strip()
            break
    print(f"  Line {idx+1} ({page}): [{kw}] {line}")
