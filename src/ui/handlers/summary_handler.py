import re
import json
from PyQt6.QtWidgets import QProgressDialog, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import fitz  # type: ignore
from src.core.summary import summary_text
from src.ui.dialogs.summary_dialog import SummaryDialog


class StreamingThread(QThread):
    """A QThread to handle streaming updates."""
    update_signal = pyqtSignal(str)  # Signal to emit new content

    def __init__(self, selected_files, api_key, base_url, model, temperature):
        super().__init__()
        self.selected_files = selected_files
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.temperature = temperature

    def run(self):
        """Run the streaming process."""
        try:
            # Generate summary (streaming)
            summary_result = summary_text(
                self.selected_files,
                self.api_key,
                self.base_url,
                self.model,
                self.temperature
            )

            # Process the streaming response
            buffer = ""  # Buffer to accumulate incomplete JSON data
            for line in summary_result.splitlines():
                if line.startswith("data:"):
                    try:
                        # Remove "data: " prefix and strip whitespace
                        json_str = line[5:].strip()

                        # Skip empty lines
                        if not json_str:
                            continue

                        # Add the line to the buffer
                        buffer += json_str

                        # Attempt to parse the JSON
                        try:
                            json_data = json.loads(buffer)
                            if "choices" in json_data and len(json_data["choices"]) > 0:
                                content = json_data["choices"][0]["delta"].get("content", "")
                                if content:
                                    # Emit the new content
                                    self.update_signal.emit(content)
                            buffer = ""  # Clear the buffer after successful parsing
                        except json.JSONDecodeError:
                            # JSON is incomplete; wait for more data
                            continue
                    except Exception as e:
                        print(f"Error processing line: {e}")
                        buffer = ""  # Clear the buffer on error

        except Exception as e:
            self.update_signal.emit(f"Error: {str(e)}")

def summary_handler(main_window):
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

    # Show the summary dialog immediately
    summary_dialog = SummaryDialog(main_window)
    summary_dialog.show()  # Show the dialog before starting the streaming process

    # Create and start the streaming thread
    streaming_thread = StreamingThread(
        selected_files,
        llm_settings["api_key"],
        llm_settings["base_url"],
        llm_settings["model"],
        llm_settings.get("temperature", 0.7)
    )
    streaming_thread.update_signal.connect(summary_dialog.append_summary)  # Connect signal to dialog

    # Store the thread as an attribute of the dialog to prevent premature destruction
    summary_dialog.streaming_thread = streaming_thread

    streaming_thread.start()  # Start the thread