import os
import sys

pdf_path = r"d:\ML\Lab1\slide\neurips2024metageneration-tutorial-all.pdf"
txt_out_path = r"d:\ML\Lab1\slide\pdf_text.txt"

def try_extract():
    # Try pypdf
    try:
        import pypdf
        print("Using pypdf...")
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"--- PAGE {i+1} ---\n"
            text += page.extract_text() or ""
            text += "\n"
        with open(txt_out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted {len(text)} chars to {txt_out_path}")
        return True
    except ImportError:
        pass

    # Try pdfplumber
    try:
        import pdfplumber
        print("Using pdfplumber...")
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text += f"--- PAGE {i+1} ---\n"
                text += page.extract_text() or ""
                text += "\n"
        with open(txt_out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted {len(text)} chars to {txt_out_path}")
        return True
    except ImportError:
        pass

    # Try fitz (PyMuPDF)
    try:
        import fitz
        print("Using PyMuPDF (fitz)...")
        doc = fitz.open(pdf_path)
        text = ""
        for i, page in enumerate(doc):
            text += f"--- PAGE {i+1} ---\n"
            text += page.get_text()
            text += "\n"
        with open(txt_out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted {len(text)} chars to {txt_out_path}")
        return True
    except ImportError:
        pass

    # Fallback to pdfminer if installed
    try:
        from pdfminer.high_level import extract_text
        print("Using pdfminer...")
        text = extract_text(pdf_path)
        with open(txt_out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted {len(text)} chars to {txt_out_path}")
        return True
    except ImportError:
        pass

    print("No PDF libraries found. Let's try installing pypdf...")
    return False

if __name__ == "__main__":
    if os.path.exists(pdf_path):
        success = try_extract()
        if not success:
            # We will attempt to run pip install pypdf in terminal if needed
            print("Failed to find any PDF library.")
    else:
        print("PDF path does not exist.")
