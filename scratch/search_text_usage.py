import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = glob.glob("d:/ML/Lab1/chapter2/**/*.py", recursive=True)
for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    if "Text(" in content or "create_text" in content:
        print("File:", f)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            if "Text(" in line or "create_text" in line or "font=" in line:
                print(f"  Line {idx+1}: {line.strip()}")
