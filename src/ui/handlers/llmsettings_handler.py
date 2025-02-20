# src/ui/llmsettings_handler.py
from PyQt6.QtWidgets import QMessageBox, QDialog
from src.ui.dialogs.llmsettings_dialog import LLMSettingsDialog
from PyQt6.QtCore import Qt
import fitz # type: ignore


def llmsettings_handler(main_window):
    print("LLM Settings Handler called")
    
    # Create and show the dialog
    dialog = LLMSettingsDialog(main_window)
    result = dialog.exec()
    
    if result == QDialog.DialogCode.Accepted:
        settings = dialog.get_settings()
        print(f"LLM Settings saved: {settings}")
        # Here, you can add code to save the settings to a file or database
        QMessageBox.information(main_window, "提示", "LLM 设置已保存")

