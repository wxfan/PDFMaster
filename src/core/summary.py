from pathlib import Path
import fitz  # type:ignore

from io import BytesIO
from PIL import Image, ImageEnhance
import os

import requests

def summary_text(pdf_paths, api_key, base_url, model, temperature=0.7):
    # Extract text from PDF files
    pdf_text = ""
    for pdf_path in pdf_paths:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                pdf_text += page.get_text() + "\n"
                
    if not pdf_text.strip():
        return "PDF文件内容为空，无法生成摘要。"
    
    # Prepare API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    messages = [
        {
            "role": "user",
            "content": f"请总结以下PDF内容:\n\n{pdf_text[:8000]}"  # 限制到约8KB
        }
    ]
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature
            },
            headers=headers
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"API请求失败: {str(e)}"
    except KeyError as e:
        return f"API响应格式不正确: {str(e)}"
    except Exception as e:
        return f"生成摘要时发生错误: {str(e)}"
