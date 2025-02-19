from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from src.core.rotate import rotate_pdfs
from pathlib import Path

def rotate_handler(main_window):
    """旋转当前选中的文件"""
    if main_window.file_list.count() == 0:
        QMessageBox.warning(main_window, "警告", "请先添加文件")
        return

    # 获取当前选中的文件
    current_file = main_window.file_list.currentItem()
    if not current_file:
        QMessageBox.warning(main_window, "警告", "请选择一个文件进行旋转")
        return
    current_file = current_file.text()

    # 设置默认输出路径
    output_path = str(Path(current_file).with_name(f"{Path(current_file).stem}_rotated.pdf"))
    
    # 询问用户旋转角度
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
        return  # 旋转失败后不再继续执行

    # 将旋转后的文件添加到列表并选中
    main_window.file_list.addItem(output_path)
    main_window.file_list.setCurrentRow(main_window.file_list.count() - 1)

    # 正确访问状态栏并显示消息
    main_window.statusBar().showMessage(f"文件已旋转 {degrees} 度: {output_path}")