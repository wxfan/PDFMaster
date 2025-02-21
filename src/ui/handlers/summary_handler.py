from PyQt6.QtWidgets import QProgressDialog, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt
import fitz  # type: ignore
from src.core.summary import summary_text


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
    
    # Get LLM settings from main window
    llm_settings = main_window.get_llm_settings()
    
    try:
        # Generate summary
        summary_result = summary_text(selected_files, 
                                    llm_settings["api_key"], 
                                    llm_settings["base_url"], 
                                    llm_settings["model"], 
                                    llm_settings.get("temperature", 0.7))
        
        # Show summary dialog
        summary_dialog = SummaryDialog(main_window)
        summary_dialog.set_summary(summary_result)
        summary_dialog.exec()
        
    except Exception as e:
        QMessageBox.critical(main_window, "错误", f"生成摘要失败: {str(e)}")

