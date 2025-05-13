import sys
import os
from pdfminer.high_level import extract_text as pdf_extract

def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        # Extract text from PDF
        return pdf_extract(path)
    else:
        # Fallback: read as plain text
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py path/to/file.(txt|pdf)")
        sys.exit(1)
    content = extract_text_from_file(sys.argv[1])
    print("Extracted Text:\n", content)

