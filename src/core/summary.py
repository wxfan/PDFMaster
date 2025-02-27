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
                "content": f"请使用中文总结如下的PDF内容:\n\n{pdf_text[:8000]}"  # limit to ~8KB
            }
        ],
        "temperature": temperature,
        "stream": True  # Enable streaming
    }

    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            json=data,
            headers=headers,
            stream=True  # Enable streaming
        )
        response.raise_for_status()

        # Process the streamed response
        summary = ""
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                # Decode the chunk and append to the summary
                summary += chunk.decode('utf-8')

        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"