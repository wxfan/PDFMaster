# src/ui/llmsettings_handler.py
from PyQt6.QtWidgets import QMessageBox, QDialog
from src.ui.dialogs.llmsettings_dialog import LLMSettingsDialog
from src.core.llmsetting import get_llm_settings, save_llm_settings
from PyQt6.QtCore import Qt
import fitz # type: ignore


import json

def llmsettings_handler(main_window):
    print("LLM Settings Handler called")
    
    # Create and show the dialog
    dialog = LLMSettingsDialog(main_window)
    result = dialog.exec()
    
    if result == QDialog.DialogCode.Accepted:
        settings = dialog.get_settings()
        print(f"LLM Settings saved: {settings}")
        # Save settings to a JSON file or another persistent storage
        save_llm_settings(settings)
        QMessageBox.information(main_window, "提示", "LLM 设置已保存")
    return get_llm_settings()  # Return the current settings

