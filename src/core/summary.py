from pathlib import Path
import fitz  # type:ignore

from io import BytesIO
from PIL import Image, ImageEnhance
import os

import requests

 # updates to src/core/summary.py
def summary_text(pdf_paths, api_key, base_url, model, temperature=0.7):

     # Extract text from PDF files
     pdf_text = ""
     for pdf_path in pdf_paths:
         with fitz.open(pdf_path) as doc:
             for page in doc:
                 pdf_text += page.get_text() + "\n"

     print(f"Extracted text from PDFs: {pdf_text[:500]}")  # Print first 500 characters for debugging

     # Prepare API request
     headers = {
         "Content-Type": "application/json",
         "Authorization": f"Bearer {api_key}"
     }

     data = {
         "model": model,
         "messages": [
             {
                 "role": "user",
                 "content": f"Please summarize the following PDF content:\n\n{pdf_text[:8000]}"  # limit to ~8KB
             }
         ],
         "temperature": temperature
     }

     try:
         response = requests.post(
             f"{base_url}/chat/completions",
             json=data,
             headers=headers
         )
         response.raise_for_status()
         return response.json()["choices"][0]["message"]["content"]
     except Exception as e:
         return f"Error generating summary: {str(e)}"
