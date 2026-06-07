import os
import docx

def read_docx(file_path):
    doc = docx.Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return paragraphs

docx_path = r"d:\ML\Lab1\subtitle\Subtitle-lab1-ml.docx"
print("Reading DOCX...")
if os.path.exists(docx_path):
    paragraphs = read_docx(docx_path)
    print(f"Total non-empty paragraphs: {len(paragraphs)}")
    print("First 10 paragraphs:")
    for i, p in enumerate(paragraphs[:10]):
        print(f"{i+1}: {p[:150]}...")
else:
    print("DOCX file not found!")
