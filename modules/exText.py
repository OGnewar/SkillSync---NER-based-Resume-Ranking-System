import pymupdf
import re
import os
import docx

from modules.multi_column import column_boxes  # Existing function

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF using PyMuPDF."""
    text = ''
    doc = pymupdf.open(file_path)
    for page in doc:
        bboxes = column_boxes(page, footer_margin=50, no_image_text=True)
        for rect in bboxes:
            text += page.get_text(clip=rect, sort=True) + " "

    # Replace '|' with space
    text = re.sub(r'\|', ' ', text)

    # Allow '@', single hyphen '-', en dash '–', and plus sign '+'
    text = re.sub(r'[^a-zA-Z0-9/.,()@: \n\-–+]', '', text)  # Clean unwanted characters
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces

    return text.strip()

def extract_text_from_docx(file_path):
    """Extracts text from a DOCX file using python-docx."""
    doc = docx.Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text.strip()

def extract_text_from_txt(file_path):
    """Extracts text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text.strip()

def extract_text(file_path):
    """Extracts text based on file type."""
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        return extract_text_from_docx(file_path)
    elif file_extension == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF, DOCX, or TXT file.")
