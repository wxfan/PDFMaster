# main_window.py
from PyQt6.QtWidgets import (QMainWindow, QListWidget, QVBoxLayout, QWidget, 
                             QLabel, QLineEdit, QInputDialog, QHBoxLayout, 
                             QScrollArea, QDialog,QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog, QProgressDialog
import fitz  # type:ignore
import os
from src.ui.handlers.preview_handler import update_preview
from src.core.pdf_processor import PDFProcessor
from src.ui.dialogs import ExtractDialog, SplitDialog, WatermarkDialog
from src.ui.menu_bar import MenuBar  # Import the update_preview function

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize file list
        self.file_list = QListWidget()
        self.file_list.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.file_list.setFixedWidth(200)  # 设置固定宽

        # Initialize preview area
        self.preview_layout = QVBoxLayout()
        self.preview_widget = QWidget()
        self.preview_widget.setLayout(self.preview_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.preview_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.file_list)
        main_layout.addWidget(scroll_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Create menus using MenuBar class
        self.menu_bar = MenuBar(self)

        # Connect signals and slots
        self.file_list.itemSelectionChanged.connect(self._update_preview)

    def _update_preview(self):
        """更新 PDF 预览"""
        update_preview(self.file_list, self.preview_layout)

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

    def _add_files(self):
        """Add files to the file list"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择 PDF 文件", "", "PDF 文件 (*.pdf)"
        )
        if files:
            for file_path in files:
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
                    if not PDFProcessor.verify_password(file_path, password):
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
                self._update_preview()

    def _remove_files(self):
        """Remove selected files from the list"""
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def _merge_files(self):
        """合并文件逻辑"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        # 获取文件列表
        file_list = [self.file_list.item(i).text() for i in range(self.file_list.count())]

        # 获取输出路径
        output_path, _ = QFileDialog.getSaveFileName(
            self, "保存合并文件", "merged.pdf", "PDF 文件 (*.pdf)"
        )
        if not output_path:
            return

        # 执行合并
        try:
            PDFProcessor.merge_pdfs(file_list, output_path, self.merge_bookmarks.isChecked())
            QMessageBox.information(self, "成功", "文件合并完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"合并失败: {str(e)}")

    def _split_files(self):
        """拆分文件逻辑"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        # Show split dialog
        dialog = SplitDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        settings = dialog.get_settings()
        mode = settings["mode"]
        page_range = (settings.get("start"), settings.get("end")) if mode == "range" else None

        input_path = self.file_list.item(0).text()
        output_dir = QFileDialog.getExistingDirectory(self, "选择输出目录")

        if not output_dir:
            return

        # Set up progress dialog
        progress_dialog = QProgressDialog("正在处理...", "取消", 0, 100, self)
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setAutoClose(True)

        def update_progress(value):
            progress_dialog.setValue(int(value * 100))
            return not progress_dialog.wasCanceled()

        try:
            PDFProcessor.split_pdf(input_path, output_dir, mode, page_range, update_progress)
            QMessageBox.information(self, "成功", "文件拆分完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"拆分失败: {str(e)}")

    def _extract_pages(self):
        """提取页面逻辑"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        # Show extract dialog
        dialog = ExtractDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        settings = dialog.get_settings()
        page_range = settings["page_range"]

        input_path = self.file_list.item(0).text()
        output_path, _ = QFileDialog.getSaveFileName(
            self, "保存提取的 PDF 文件", "extracted.pdf", "PDF 文件 (*.pdf)"
        )
        if not output_path:
            return

        try:
            PDFProcessor.extract_pages(input_path, output_path, page_range)
            QMessageBox.information(self, "成功", "页面提取完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"提取失败: {str(e)}")

    def _encrypt_current_file(self):
        """Encrypt the currently selected PDF file."""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        selected_item = self.file_list.currentItem().text()
        password = self._show_password_dialog()

        if password is None:
            return

        output_path = os.path.splitext(selected_item)[0] + "_encrypted.pdf"
        try:
            PDFProcessor.encrypt_pdf(selected_item, output_path, password)
            QMessageBox.information(self, '成功', f'文件已加密保存为：{output_path}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加密失败: {str(e)}')

    def _add_watermark(self):
        """Add a watermark to the selected PDF file."""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        # Show watermark configuration dialog
        dialog = WatermarkDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        settings = dialog.get_settings()
        if not settings.get("text") and not settings.get("image"):
            QMessageBox.warning(self, "警告", "请配置水印内容")
            return

        input_path = self.file_list.item(0).text()
        output_dir = QFileDialog.getExistingDirectory(self, "选择输出目录")

        if not output_dir:
            return

        doc = fitz.open(input_path)
        if doc.page_count == 0:  # 👈 新增有效性检查
            raise ValueError("PDF文件为空或损坏，无法处理")
        print(settings)
        try:
            PDFProcessor.add_watermark(
                input_path=input_path,
                output_dir=output_dir,
                watermark_text=settings.get("text"),
                watermark_image_path=settings.get("image"),
                rotation=settings.get("rotation"),
                opacity=settings.get("opacity"),
                position=settings.get("position"),
            )
            QMessageBox.information(self, "成功", "水印添加完成！")
        except Exception as e:
            q_err = f"添加水印失败: {str(e)}"
            if "page 0 is not in document" in str(e):
                q_err = "无法添加水印，PDF 文件为空或已损坏。请检查文件并重试。"
            QMessageBox.critical(self, "错误", q_err)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec())