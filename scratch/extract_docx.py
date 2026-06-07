import zipfile
import xml.etree.ElementTree as ET
import os

docx_path = r"d:\ML\Lab1\subtitle\Subtitle-lab1-ml.docx"
txt_path = r"d:\ML\Lab1\subtitle\Subtitle-lab1-ml.txt"

def docx_to_text(path):
    try:
        # Standard docx is a zip file, text is in word/document.xml
        with zipfile.ZipFile(path) as z:
            xml_content = z.read('word/document.xml')
            
        root = ET.fromstring(xml_content)
        
        # Namespace for wordprocessingML
        namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        paragraphs = []
        for p in root.findall('.//w:p', namespaces):
            texts = [t.text for t in p.findall('.//w:t', namespaces) if t.text]
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if os.path.exists(docx_path):
        text = docx_to_text(docx_path)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Successfully extracted text to {txt_path}. Total length: {len(text)} characters.")
    else:
        print(f"Error: {docx_path} does not exist.")
