# src/ui/split_files.py
from PyQt6.QtWidgets import QProgressDialog, QMessageBox, QFileDialog,QDialog
from PyQt6.QtCore import Qt
from src.ui.dialogs import SplitDialog
import fitz # type: ignore

from src.core import split_pdf

def split_handler(main_window):
    if main_window.file_list.count() == 0:
        QMessageBox.warning(main_window, "警告", "请先添加文件")
        return

    # Show split dialog
    dialog = SplitDialog(main_window)
    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    settings = dialog.get_settings()
    mode = settings["mode"]
    page_range = (settings.get("start"), settings.get("end")) if mode == "range" else None

    input_path = main_window.file_list.item(0).text()
    output_dir = QFileDialog.getExistingDirectory(main_window, "选择输出目录")

    if not output_dir:
        return

    # Set up progress dialog
    progress_dialog = QProgressDialog("正在处理...", "取消", 0, 100, main_window)
    progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    progress_dialog.setAutoClose(True)

    def update_progress(value):
        progress_dialog.setValue(int(value * 100))
        return not progress_dialog.wasCanceled()

    try:
        split_pdf(input_path, output_dir, mode, page_range, update_progress)
        QMessageBox.information(main_window, "成功", "文件拆分完成！")
    except Exception as e:
        QMessageBox.critical(main_window, "错误", f"拆分失败: {str(e)}")