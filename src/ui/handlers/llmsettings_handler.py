# src/ui/llmsettings_handler.py
from PyQt6.QtWidgets import QMessageBox, QDialog
from src.ui.dialogs.llmsettings_dialog import LLMSettingsDialog
from PyQt6.QtCore import Qt
import fitz # type: ignore


import json

def save_llm_settings(settings):
    with open('llm_settings.json', 'w') as f:
        json.dump(settings, f)

def get_llm_settings():
    try:
        with open('llm_settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "api_key": "",
            "base_url": "",
            "model": "",
            "temperature": 0.7
        }

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

