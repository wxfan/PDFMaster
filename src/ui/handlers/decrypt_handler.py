# src/ui/encrypt_current_file.py
from PyQt6.QtWidgets import QMessageBox, QLineEdit,QInputDialog
import os
from src.core import decrypt

def decrypt_handler(main_window):
    file_path = main_window.current_file_path
    if not file_path:
        QMessageBox.warning(main_window, "No File Selected", "Please select a file first.")
        return
    password, ok = QInputDialog.getText(main_window, "Enter Password", "Enter the password to decrypt the file:")
    if ok and password:
        try:
            output_path = os.path.splitext(file_path)[0] + "_decrypted.pdf"
            decrypt(file_path, output_path, password)
            QMessageBox.information(main_window, "Success", f"File decrypted successfully and saved as {output_path}")
        except Exception as e:
            QMessageBox.critical(main_window, "Error", f"Failed to decrypt file: {str(e)}")
    else:
        QMessageBox.warning(main_window, "No Password Entered", "Please enter a password to decrypt the file.")








