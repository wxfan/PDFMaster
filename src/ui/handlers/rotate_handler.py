from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from src.core.rotate import rotate_pdfs
from pathlib import Path

def rotate_handler(main_window):
    """旋转当前选中的文件"""
    if main_window.file_list.count() == 0:
        QMessageBox.warning(main_window, "警告", "请先添加文件")
        return

    # Get the current selected file
    current_file = main_window.file_list.currentItem().text()
    if not current_file:
        QMessageBox.warning(main_window, "警告", "请选择一个文件进行旋转")
        return

    # Set default output path
    output_path = str(Path(current_file).with_name(f"{Path(current_file).stem}_rotated.pdf"))
    
    # Ask user for rotation angle
    degrees, ok = QInputDialog.getInt(
        main_window, "选择旋转角度", 
        "请输入旋转角度(度)：", 
        90, 0, 270, 90
    )
    if not ok:
        return

    try:
        rotate_pdfs(current_file, output_path, degrees)
        QMessageBox.information(main_window, "成功", "文件旋转完成！")
    except Exception as e:
        QMessageBox.critical(main_window, "错误", f"旋转失败: {str(e)}")
