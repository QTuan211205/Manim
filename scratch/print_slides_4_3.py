import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("d:/ML/Lab1/slide/pdf_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find PAGE 186 to PAGE 195
pages = {}
current_page = None
page_lines = []
for line in lines:
    if "--- PAGE" in line:
        if current_page:
            pages[current_page] = page_lines
        current_page = line.strip()
        page_lines = []
    elif current_page:
        page_lines.append(line)
if current_page:
    pages[current_page] = page_lines

for p in range(185, 196):
    pkey = f"--- PAGE {p} ---"
    if pkey in pages:
        print(pkey)
        for line in pages[pkey]:
            print("  " + line, end="")
