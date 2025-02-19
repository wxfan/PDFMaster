# src/ui/encrypt_current_file.py
from PyQt6.QtWidgets import QMessageBox, QLineEdit,QInputDialog
import os
from src.core import encrypt_pdf

def encrypt_handler(main_window):
    if main_window.file_list.count() == 0:
        QMessageBox.warning(main_window, "警告", "请先添加文件")
        return

    selected_item = main_window.file_list.currentItem().text()
    password = _show_password_dialog(main_window)

    if password is None:
        return

    output_path = os.path.splitext(selected_item)[0] + "_encrypted.pdf"
    try:
        encrypt_pdf(selected_item, output_path, password)
        QMessageBox.information(main_window, '成功', f'文件已加密保存为：{output_path}')
    except Exception as e:
        QMessageBox.critical(main_window, '错误', f'加密失败: {str(e)}')

def _show_password_dialog(self):
        """
        显示密码输入对话框
        :return: str 或 None 密码或取消
        """
        dialog = QInputDialog(self)
        dialog.setWindowTitle('输入密码')
        dialog.setLabelText('请输入加密密码：')
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        dialog.resize(300, 150)  # 设置窗口大小

        ok = dialog.exec()
        if ok:
            password = dialog.textValue()
            return password
        return None