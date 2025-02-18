# src/ui/handlers/pdffile_handler.py
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QListWidget
from PyQt6.QtCore import Qt

class PDFFileHandler:
    def __init__(self, file_list):
        self.file_list = file_list

    def add_files(self):
        """添加文件到文件列表"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("PDF 文件 (*.pdf)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            for file_path in selected_files:
                if file_path not in self.file_list.findItems(file_path, Qt.MatchFlag.MatchExactly):
                    self.file_list.addItem(file_path)

    def remove_files(self):
        """从文件列表中删除选中的文件"""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "警告", "请先选择一个或多个文件进行删除。")
            return
        reply = QMessageBox.question(
            None,
            "确认删除",
            "确定要删除选中的文件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for item in selected_items:
                self.file_list.takeItem(self.file_list.row(item))

    def clear_list(self):
        """清空文件列表"""
        reply = QMessageBox.question(
            None,
            "确认清空",
            "确定要清空所有文件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.file_list.clear()