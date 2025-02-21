import threading
from PyQt6.QtWidgets import (QProgressDialog, QMessageBox, QFileDialog, 
                            QDialog, QDialogButtonBox, QWidget)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from src.core.summary import summary_text
from src.ui.dialogs.summary_dialog import SummaryDialog

class SummaryGenerator(QObject):
    update = pyqtSignal(str)
    complete = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, selected_files, llm_settings):
        super().__init__()
        self.selected_files = selected_files
        self.llm_settings = llm_settings

    def run(self):
        try:
            generator = summary_text(
                self.selected_files,
                self.llm_settings["api_key"],
                self.llm_settings["base_url"],
                self.llm_settings["model"],
                self.llm_settings.get("temperature", 0.7),
                stream=True
            )
            
            complete_summary = ""
            for chunk in generator:
                print(f"Received chunk: {chunk[:200]}")  # Debugging line
                complete_summary += chunk
                self.update.emit(chunk)
            
            self.complete.emit(complete_summary)
            print("Summary generation complete.")  # Debugging line
            
        except Exception as e:
            self.error.emit(f"Summary generation error: {str(e)}")

def summary_handler(main_window):
    if not main_window.file_list.selectedItems():
        QMessageBox.warning(main_window, "警告", "请先选择要处理的 PDF 文件")
        return
    
    selected_files = [
        main_window.file_list.item(i).text() 
        for i in range(main_window.file_list.count())
        if main_window.file_list.item(i).isSelected()
    ]

    llm_settings = main_window.gettings_llm()
    
    if not llm_settings.get("api_key"):
        QMessageBox.warning(main_window, "警告", "请先配置LLM API密钥")
        return

    progress_dialog = QProgressDialog("生成摘要中...", "取消", 0, 0, main_window)
    progress_dialog.setCancelButton(None)
    progress_dialog.show()

    try:
        summary_generator = SummaryGenerator(selected_files, llm_settings)
        summary_dialog = SummaryDialog(main_window)

        summary_generator.update.connect(summary_dialog.append_to_summary)
        summary_generator.complete.connect(
            lambda s: (summary_dialog.set_summary(s), progress_dialog.close())
        )
        summary_generator.error.connect(
            lambda e: (progress_dialog.close(),
                       QMessageBox.critical(main_window, "错误", f"生成摘要失败: {e}"))
        )

        thread = threading.Thread(target=summary_generator.run)
        thread.start()
        
    except Exception as e:
        progress_dialog.close()
        QMessageBox.critical(main_window, "错误", f"生成摘要失败: {str(e)}")