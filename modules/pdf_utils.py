'''import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    return text'''

import pymupdf
from modules.multi_column import column_boxes
import re

def extract_text_from_pdf(file_path):
    text = ' '
    doc = pymupdf.open(file_path)
    for page in doc:
        bboxes = column_boxes(page, footer_margin=50, no_image_text=True)
        for rect in bboxes:
            text += page.get_text(clip=rect, sort=True) + " "
    
    # Replace '|' with a space
    text = re.sub(r'\|', ' ', text)
    
    # Modified regex to allow '@', single hyphen '-', en dash '–', and plus sign '+'
    text = re.sub(r'[^a-zA-Z0-9/.,()@: \n\-–+]', '', text)  # Allows single hyphen, en dash, and plus sign
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces

    return text

