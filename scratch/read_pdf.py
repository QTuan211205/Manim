import pypdf
import os

pdf_path = r"d:\ML\Lab1\slide\neurips2024metageneration-tutorial-all.pdf"
print("Reading PDF...")

if os.path.exists(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")
    
    # Let's inspect text from a few slides
    for i in range(min(15, len(reader.pages))):
        page = reader.pages[i]
        text = page.extract_text()
        first_line = text.split("\n")[0] if text else "(No text)"
        print(f"Slide {i+1} title/first line: {repr(first_line)}")
else:
    print("PDF file not found!")
