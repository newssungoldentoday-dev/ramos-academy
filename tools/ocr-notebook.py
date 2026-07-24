#!/usr/bin/env python3
"""
Extracts raw text from a photo of a notebook page, as a rough first draft.
You still need to clean it up and feed it into notebook-to-lesson.py by hand.

Setup (once):
    pkg install tesseract
    pip install pytesseract pillow --break-system-packages

Run:
    python3 tools/ocr-notebook.py /path/to/photo.jpg
"""

import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/ocr-notebook.py /path/to/photo.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        sys.exit(1)

    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        print("Missing dependencies. Run:")
        print("  pkg install tesseract")
        print("  pip install pytesseract pillow --break-system-packages")
        sys.exit(1)

    print(f"Reading text from {image_path}...\n")
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    print("=== Extracted text (raw, needs cleanup) ===\n")
    print(text)

    outfile = image_path.rsplit(".", 1)[0] + "-ocr.txt"
    with open(outfile, "w") as f:
        f.write(text)
    print(f"\nSaved to {outfile}. Clean this up, then feed it into notebook-to-lesson.py.")

if __name__ == "__main__":
    main()
