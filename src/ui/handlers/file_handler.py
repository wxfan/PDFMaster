from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog, QLineEdit
from PyQt6.QtCore import QObject
import fitz # type: ignore
from src.core import PDFSecurity

class FileHandler(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        if not main_window:
            raise ValueError("MainWindow instance required")

        # Initialize file_list safely
        self.file_list = None
        if hasattr(main_window, 'file_list'):
            self.file_list = main_window.file_list

    def _add_files(self):
        """Add files to the file list."""
        main_window = self.main_window
        if not main_window:
            QMessageBox.critical(None, "错误", "主窗口不存在")
            return
        
        if not hasattr(main_window, 'file_list'):
            QMessageBox.critical(None, "错误", "文件列表不存在")
            return
            
        if not main_window.file_list:
            QMessageBox.critical(None, "错误", "文件列表未初始化")
            return

        file_paths, _ = QFileDialog.getOpenFileNames(
            self.main_window, "选择 PDF 文件", "", "PDF 文件 (*.pdf)"
        )

        if file_paths:
            for file_path in file_paths:
                # 尝试打开文件以检测是否已加密
                password = None
                try:
                    with fitz.open(file_path) as doc:
                        pass  # 文件未加密，直接添加
                except fitz.PasswordError:
                    # 文件加密，需要用户输入密码
                    password = self._show_password_dialog()
                    if password is None:
                        continue  # 用户取消操作
                    if not PDFSecurity.verify_password(file_path, password):
                        QMessageBox.critical(self, '错误', '密码错误，请重试！')
                        continue
                except Exception as e:
                    # 处理其他可能的错误，如文件损坏
                    QMessageBox.critical(self, '错误', f'无法打开文件：{str(e)}')
                    continue

                # 如果文件未加密或密码验证成功，添加到列表
                self.file_list.addItems([file_path])

            if self.file_list.count() > 0:
                self.file_list.setCurrentRow(0)
                self.preview_manager.update_preview()

    def _remove_files(self):
        """Remove selected files from the list"""
        main_window = self.main_window
        file_list = main_window.file_list
        if not main_window or not file_list:
            return

        for item in file_list.selectedItems():
            file_list.takeItem(file_list.row(item))
        self.preview_manager.update_preview()

    def _show_password_dialog(self):
        main_window = self.main_window
        dialog = QInputDialog(main_window)
        dialog.setWindowTitle('输入密码')
        dialog.setLabelText('请输入加密密码：')
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        dialog.resize(300, 150)

        ok = dialog.exec()
        if ok:
            return dialog.textValue()
        return None
