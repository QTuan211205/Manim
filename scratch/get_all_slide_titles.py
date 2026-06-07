import pypdf
import os

pdf_path = r"d:\ML\Lab1\slide\neurips2024metageneration-tutorial-all.pdf"
output_path = r"d:\ML\Lab1\scratch\slide_titles.txt"

if os.path.exists(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Total Slides: {len(reader.pages)}\n\n")
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                lines = [line.strip() for line in text.split("\n") if line.strip()]
                # Write slide index and first few non-empty lines
                f.write(f"--- Slide {i+1} ---\n")
                for j, line in enumerate(lines[:4]):
                    f.write(f"Line {j+1}: {line}\n")
                f.write("\n")
            else:
                f.write(f"--- Slide {i+1} ---\n(Empty or Image only)\n\n")
    print(f"Slide titles and headers saved to {output_path}")
else:
    print("PDF not found!")
