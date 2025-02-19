# src/ui/add_watermark.py
from PyQt6.QtWidgets import QMessageBox, QFileDialog,QDialog
from src.ui.dialogs import WatermarkDialog
import fitz #type:ignore
from src.core import add_watermark

def watermark_handler(main_window):
    if main_window.file_list.count() == 0:
        QMessageBox.warning(main_window, "警告", "请先添加文件")
        return

    # Show watermark configuration dialog
    dialog = WatermarkDialog(main_window)
    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    settings = dialog.get_settings()
    if not settings.get("text") and not settings.get("image"):
        QMessageBox.warning(main_window, "警告", "请配置水印内容")
        return

    input_path = main_window.file_list.item(0).text()
    output_dir = QFileDialog.getExistingDirectory(main_window, "选择输出目录")

    if not output_dir:
        return

    doc = fitz.open(input_path)
    if doc.page_count == 0:  # 👈 新增有效性检查
        raise ValueError("PDF文件为空或损坏，无法处理")
    print(settings)
    try:
        add_watermark(
            input_path=input_path,
            output_dir=output_dir,
            watermark_text=settings.get("text"),
            watermark_image_path=settings.get("image")
        )
        QMessageBox.information(main_window, "成功", "水印添加完成！")
    except Exception as e:
        q_err = f"添加水印失败: {str(e)}"
        if "page 0 is not in document" in str(e):
            q_err = "无法添加水印，PDF 文件为空或已损坏。请检查文件并重试。"
        QMessageBox.critical(main_window, "错误", q_err)