import os
import re
import json
import base64
from PyQt6.QtWidgets import QProgressDialog, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import fitz  # type: ignore
from src.core.summary import summary_text
from src.ui.dialogs.ocr_dialog import OcrDialog
from openai import OpenAI

def ocr_handler(main_window):
    # Check if any files are selected
    if not main_window.file_list.selectedItems():
        QMessageBox.warning(main_window, "警告", "请先选择要处理的 PDF 文件")
        return

    # Get selected PDF files
    selected_files = [
        main_window.file_list.item(i).text()
        for i in range(main_window.file_list.count())
        if main_window.file_list.item(i).isSelected()
    ]

    print(f"Selected files: {selected_files}")  # Debugging line to print selected files

    # Get LLM settings from main window
    llm_settings = main_window.gettings_llm()

    # Add validation for required settings
    if not llm_settings.get("api_key"):
        QMessageBox.warning(main_window, "警告", "请先配置LLM API密钥")
        return

    print(f"LLM Settings: {llm_settings}")  # Debugging line to print LLM settings

    # Show the ocr dialog immediately
    ocr_dialog = OcrDialog(main_window)
    ocr_dialog.show()  # Show the dialog before starting the streaming process

    # Create and start the streaming thread
    streaming_thread = StreamingThread(
        selected_files,
        llm_settings["api_key"],
        llm_settings["base_url"],
        llm_settings["visionmode"],
        llm_settings.get("temperature", 0.7)
    )
    streaming_thread.update_signal.connect(ocr_dialog.append_summary)  # Connect signal to dialog

    # Store the thread as an attribute of the dialog to prevent premature destruction
    ocr_dialog.streaming_thread = streaming_thread

    streaming_thread.start()  # Start the thread


class StreamingThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, files, api_key, base_url, model, temperature):
        super().__init__()
        self.files = files
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def run(self):
        for file in self.files:
            doc = fitz.open(file)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                img_path = f"temp_page_{page_num + 1}.png"
                pix.save(img_path)
                print(f"Saved image to {img_path}")  # Debugging line to print image path

                # Encode the image to BASE64
                base64_image = self.encode_image(img_path)

                try:
                    completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                                        "min_pixels": 28 * 28 * 4,
                                        "max_pixels": 1280 * 784
                                    },
                                    {"type": "text", "text": "Read all the text in the image."}
                                ]
                            }
                        ],
                        temperature=self.temperature
                    )
                    self.update_signal.emit(completion.choices[0].message.content + "\n")
                except Exception as e:
                    self.update_signal.emit(f"Error processing file {file}, page {page_num + 1}: {str(e)}\n")
                finally:
                    os.remove(img_path)