# merge_handler.py
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from src.core import merge_pdfs

def merge_handler(main_window):
    """合并文件逻辑"""
    if main_window.file_list.count() == 0:
        QMessageBox.warning(main_window, "警告", "请先添加文件")
        return

    # 获取文件列表
    file_list = [main_window.file_list.item(i).text() for i in range(main_window.file_list.count())]

    # 获取输出路径
    output_path, _ = QFileDialog.getSaveFileName(
        main_window, "保存合并文件", "merged.pdf", "PDF 文件 (*.pdf)"
    )
    if not output_path:
        return

    # 执行合并
    try:
        merge_pdfs(file_list, output_path)

        QMessageBox.information(main_window, "成功", "文件合并完成！")
    except Exception as e:
        QMessageBox.critical(main_window, "错误", f"合并失败: {str(e)}")