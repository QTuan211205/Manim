import docx
import os

docx_path = r"d:\ML\Lab1\subtitle\Subtitle-lab1-ml.docx"
output_path = r"d:\ML\Lab1\scratch\intro_subtitle.txt"

if os.path.exists(docx_path):
    doc = docx.Document(docx_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== EXTRACTED SUBTITLE FOR INTRO ===\n\n")
        # Let's extract first 300 paragraphs to find where Part I starts
        for i in range(min(300, len(paragraphs))):
            f.write(f"{paragraphs[i]}\n")
    print(f"Intro subtitles saved to {output_path}")
else:
    print("DOCX not found!")
