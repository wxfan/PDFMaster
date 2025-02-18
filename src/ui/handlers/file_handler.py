from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog, QLineEdit,QDialog
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QStandardItem
import fitz  # type: ignore
from src.core import PDFSecurity

class FileHandler(QObject):
    fileAdded = pyqtSignal()  # 定义一个信号，文件添加完成后发出

    def __init__(self, main_window, file_list_model):
        super().__init__()
        if not main_window:
            raise ValueError("MainWindow instance required")
        if not file_list_model:
            raise ValueError("QStandardItemModel instance required")

        self.main_window = main_window
        self.file_list_model = file_list_model
        self.preview_manager = self.main_window.preview_container
  # 确保传入的是视图组件

        # 连接信号到槽
        self.fileAdded.connect(self.on_file_added)

    def _add_files(self):
        """添加文件到文件列表模型。"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.main_window,
            "选择 PDF 文件",
            "",
            "PDF 文件 (*.pdf)"
        )

        if not file_paths:
            return

        for file_path in file_paths:
            # 尝试打开文件以检测是否已加密
            password = None
            try:
                with fitz.open(file_path) as doc:
                    pass  # 文件未加密，直接添加
            except fitz.PasswordError:
                # 文件加密，需要用户输入密码
                password = self._show_password_dialog()
                if not password:
                    continue  # 用户取消操作
                if not PDFSecurity.verify_password(file_path, password):
                    QMessageBox.critical(self.main_window, '错误', '密码错误，请重试！')
                    continue
            except Exception as e:
                # 处理其他可能的错误，如文件损坏
                QMessageBox.critical(self.main_window, '错误', f'无法打开文件：{str(e)}')
                continue

            # 创建 QStandardItem 并添加到模型中
            item = QStandardItem(file_path)
            self.file_list_model.appendRow(item)

        if self.file_list_model.rowCount() > 0:
            self.fileAdded.emit()  # 发出信号

    def on_file_added(self):
        """槽函数，设置当前选中行并更新预览。"""
        if self.main_window and self.main_window.file_list_widget:
            self.main_window.file_list_widget.setCurrentRow(0)
            self.preview_manager.update_preview()

    def _remove_files(self):
        """从列表中移除选中的文件。"""
        if not self.main_window or not self.main_window.file_list_model:
            return

        selected_indexes = self.main_window.file_list_model.selectedIndexes()
        if not selected_indexes:
            return

        # 按行删除，避免索引偏移问题
        rows_to_remove = sorted([index.row() for index in selected_indexes], reverse=True)
        for row in rows_to_remove:
            self.main_window.file_list_model.removeRow(row)

        if self.main_window.file_list_model.rowCount() > 0:
            self.main_window.file_list_widget.setCurrentRow(0)
            self.preview_manager.update_preview()

    def _show_password_dialog(self):
        """显示密码输入对话框并返回密码。"""
        dialog = QInputDialog(self.main_window)
        dialog.setWindowTitle('输入密码')
        dialog.setLabelText('请输入加密密码：')
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        dialog.resize(300, 150)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.textValue()
        return None