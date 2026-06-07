import sys
import os

print("Python version:", sys.version)

try:
    import docx
    print("docx (python-docx) is available")
except ImportError:
    print("docx (python-docx) is NOT available")

try:
    import docx2txt
    print("docx2txt is available")
except ImportError:
    print("docx2txt is NOT available")

try:
    import pypdf
    print("pypdf is available")
except ImportError:
    print("pypdf is NOT available")

try:
    import PyPDF2
    print("PyPDF2 is available")
except ImportError:
    print("PyPDF2 is NOT available")

try:
    import pdfplumber
    print("pdfplumber is available")
except ImportError:
    print("pdfplumber is NOT available")
