from pathlib import Path
import fitz  # type:ignore
import requests
from typing import Generator

def summary_text(pdf_paths, api_key, base_url, model, temperature=0.7, stream=False):
    pdf_text = ""
    for pdf_path in pdf_paths:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                pdf_text += page.get_text() + "\n"
    
    print(f"Extracted text from PDFs: {pdf_text[:500]}")  # Debugging line

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"请使用中文总结如下的PDF内容:\n\n{pdf_text[:8000]}"
            }
        ],
        "temperature": temperature,
        "stream": stream  # Enable streaming
    }

    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            json=data,
            headers=headers,
            stream=stream  # Stream the response
        )
        response.raise_for_status()

        if stream:
            for chunk in response.iter_lines(chunk_size=8192):
                if chunk:
                    try:
                        chunk_text = chunk.decode('utf-8').replace('data: ', '')
                        print(f"Handling chunk: {chunk_text[:200]}")  # Debugging line
                        if chunk_text.strip() == '[DONE]':
                            break
                        yield chunk_text
                    except Exception as e:
                        print(f"Error processing chunk: {e}")  # Debugging line
                        continue
        else:
            return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error generating summary: {str(e)}"