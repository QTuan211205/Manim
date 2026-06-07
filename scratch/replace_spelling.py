import sys
sys.stdout.reconfigure(encoding='utf-8')

script_path = "d:/ML/Lab1/full_video_script.md"
with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# Count occurrences of Hydrogen (case insensitive)
import re
matches = re.findall(r'Hydrogen', content, re.IGNORECASE)
print(f"Found {len(matches)} occurrences of Hydrogen/hydrogen")

new_content = re.sub(r'Hydrogen', 'Hydragen', content)
new_content = re.sub(r'hydrogen', 'hydragen', new_content)

with open(script_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Replacement complete!")
