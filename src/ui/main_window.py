from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QMenuBar, QScrollArea, QVBoxLayout,
    QListWidget, QLabel, QFileDialog, QMessageBox, QProgressDialog,
    QCheckBox, QDialog, QInputDialog
)
import os
from PyQt6.QtCore import Qt
from src.ui.dialogs import SplitDialog, ExtractDialog, WatermarkDialog

import fitz  # type: ignore
from PyQt6.QtGui import QIcon, QImage, QPixmap
from src.core.pdf_processor import PDFProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFMaster - PDF 文档处理工具")
        self.resize(1200, 800)
        self.setWindowIcon(QIcon(":/icons/app_icon.png"))

        # Create main layout
        main_layout = QHBoxLayout()

        # Initialize UI components
        self.merge_bookmarks = QCheckBox("保留书签", self)

        # Left panel - File list
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list.itemSelectionChanged.connect(self._update_preview)
        
        # Create menu bar
        self._create_menus()

        # Add widgets to layout
        main_layout.addWidget(self.file_list, stretch=1)

        # Right panel - Preview area
        self.scroll_area = QScrollArea()
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.preview_layout.setSpacing(10)
        self.preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scroll_area.setWidget(self.preview_container)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area, stretch=3)

        # Set layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _create_menus(self):
        """Create the menu bar and its actions"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("文件")
        file_menu.addAction("添加文件", self._add_files)
        file_menu.addAction("移除选中", self._remove_files)
        file_menu.addAction("清空列表", lambda: self.file_list.clear())
        file_menu.addAction("退出", self.close)
        file_menu.addAction("加密当前文件", self._encrypt_current_file)  # 新增

        # Edit menu
        edit_menu = menubar.addMenu("编辑")
        process_menu = edit_menu.addMenu("PDF 处理")

        # PDF Processing Menu Items
        process_menu.addAction("合并 PDF", self._merge_files)
        process_menu.addAction("拆分 PDF", self._split_files)
        process_menu.addAction("提取页面", self._extract_pages)
        process_menu.addAction("添加水印", self._add_watermark)


    def _update_preview(self):
        """更新 PDF 预览"""
        # 获取当前选中的文件
        selected_items = self.file_list.selectedItems()
        if selected_items:
            file_path = selected_items[0].text()
            try:
                # 清除之前的预览
                while self.preview_layout.count():
                    item = self.preview_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

                # 打开 PDF 文件
                with fitz.open(file_path) as doc:
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        pix = page.get_pixmap(dpi=96)

                        # 创建图片标签
                        image_label = QLabel()
                        image = QImage(
                            pix.samples,
                            pix.width,
                            pix.height,
                            QImage.Format.Format_RGB888
                        )
                        pixmap = QPixmap.fromImage(image)
                        
                        # 添加页码
                        page_label = QLabel(f"第 {page_num + 1} 页")
                        page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        page_label.setStyleSheet("font-size: 14px; font-weight: bold;")

                        # 添加到布局
                        image_label.setPixmap(pixmap)
                        image_label.setFixedSize(500, 700)  # 固定大小以便更好缩放
                        image_label.setScaledContents(True)
                        self.preview_layout.addWidget(image_label)
                        self.preview_layout.addWidget(page_label)

            except Exception as e:
                error_label = QLabel("无法预览文件")
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.preview_layout.addWidget(error_label)
                print(f"预览 PDF 出错: {str(e)}")
        else:
            empty_label = QLabel("请选择 PDF 文件进行预览")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.preview_layout.addWidget(empty_label)

    def _show_password_dialog(self):
        """
        显示密码输入对话框
        :return: str 或 None 密码或取消
        """
        dialog = QInputDialog(self)
        dialog.setWindowTitle('输入密码')
        dialog.setLabelText('请输入加密密码：')
        dialog.setInputMode(QInputDialog.InputMode.PasswordInput)
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

        input_path = self.file_list.item(0).text()
        output_dir = QFileDialog.getExistingDirectory(self, "选择输出目录")

        if not output_dir:
            return

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
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
