from pathlib import Path
import fitz  # type:ignore

from io import BytesIO
from PIL import Image, ImageEnhance
import os

def summary_text():
    # Define the path to the PDF file
    pdf_path = Path("example.pdf")
    
