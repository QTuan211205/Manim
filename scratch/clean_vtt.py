import re

vtt_path = r"d:\ML\Lab1\subtitle\Subtitle-lab1-ml.txt"
clean_txt_path = r"d:\ML\Lab1\subtitle\Subtitle-lab1-ml-clean.txt"

def clean_vtt(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove WEBVTT header
    content = re.sub(r'^WEBVTT\s*', '', content)
    
    # Remove timestamps line (e.g. 00:00:14.119 --> 00:00:14.760) and potential line numbers or index numbers
    lines = content.split('\n')
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        # Skip timestamp lines
        if '-->' in line:
            continue
        # Skip lines that are just numbers (sometimes indices are written above timestamps in SRT, though VTT doesn't always have them)
        if line.isdigit():
            continue
        clean_lines.append(line)
        
    # Group lines to form continuous text, joining lines unless they end with sentence termination
    full_text = []
    current_sentence = []
    
    for line in clean_lines:
        current_sentence.append(line)
        if line.endswith(('.', '?', '!')):
            full_text.append(' '.join(current_sentence))
            current_sentence = []
            
    if current_sentence:
        full_text.append(' '.join(current_sentence))
        
    return '\n\n'.join(full_text)

if __name__ == "__main__":
    import os
    if os.path.exists(vtt_path):
        clean_text = clean_vtt(vtt_path)
        with open(clean_txt_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        print(f"Successfully cleaned VTT into plain text at {clean_txt_path}. Size: {len(clean_text)} characters.")
    else:
        print(f"Error: {vtt_path} does not exist.")
