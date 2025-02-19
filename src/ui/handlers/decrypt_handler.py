# src/ui/encrypt_current_file.py
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QInputDialog
import os
from src.core import decrypt_pdf

def decrypt_handler(main_window):
    if main_window.file_list.count() == 0:
        QMessageBox.warning(main_window, "警告", "请先添加文件")
        return

    selected_item = main_window.file_list.currentItem().text()
    user_password, owner_password = _show_password_dialog(main_window)

    if user_password is None:
        return

    output_path = os.path.splitext(selected_item)[0] + "_decrypted.pdf"
    try:
        decrypt_pdf(selected_item, output_path, user_password, owner_password=owner_password)
        QMessageBox.information(main_window, '成功', f'文件已解密保存为：{output_path}')
    except Exception as e:
        QMessageBox.critical(main_window, '错误', f'解密失败: {str(e)}')

def _show_password_dialog(main_window):
    """
    显示密码输入对话框
    :param main_window: 主窗口对象
    :return: tuple 用户密码或所有者密码，或取消时为 (None, None)
    """
    user_dialog = QInputDialog(main_window)
    user_dialog.setWindowTitle('输入用户密码')
    user_dialog.setLabelText('请输入用户密码：')
    user_dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
    user_dialog.resize(300, 150)  # 设置窗口大小

    ok = user_dialog.exec()
    if not ok:
        return None, None

    user_password = user_dialog.textValue()

    owner_dialog = QInputDialog(main_window)
    owner_dialog.setWindowTitle('输入所有者密码')
    owner_dialog.setLabelText('请输入所有者密码（可选）：')
    owner_dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
    owner_dialog.resize(300, 150)  # 设置窗口大小

    owner_ok = owner_dialog.exec()
    owner_password = owner_dialog.textValue() if owner_ok else None

    return user_password, owner_password








