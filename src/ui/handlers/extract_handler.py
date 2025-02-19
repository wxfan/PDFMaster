# src/ui/extract_pages.py
from PyQt6.QtWidgets import QMessageBox, QFileDialog,QDialog
from src.ui.dialogs import ExtractDialog
from src.core import extract_pages

def extract_handler(main_window):
    if main_window.file_list.count() == 0:
        QMessageBox.warning(main_window, "警告", "请先添加文件")
        return

    # Show extract dialog
    dialog = ExtractDialog(main_window)
    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    settings = dialog.get_settings()
    page_range = settings["page_range"]

    input_path = main_window.file_list.item(0).text()
    output_path, _ = QFileDialog.getSaveFileName(
        main_window, "保存提取的 PDF 文件", "extracted.pdf", "PDF 文件 (*.pdf)"
    )
    if not output_path:
        return

    try:
        extract_pages(input_path, output_path, page_range)
        QMessageBox.information(main_window, "成功", "页面提取完成！")
    except Exception as e:
        QMessageBox.critical(main_window, "错误", f"提取失败: {str(e)}")