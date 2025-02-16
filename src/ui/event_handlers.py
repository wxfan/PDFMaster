import os
from src.ui.preview_manager import PreviewManager
from PyQt6.QtWidgets import (
    QFileDialog, QMessageBox, QProgressDialog,
    QDialog, QInputDialog, QLineEdit,QListWidget 
)
from PyQt6.QtCore import Qt, QObject
import fitz  # type: ignore
from src.core import (
    PDFExtractor, PDFMerger, PDFRotator, PDFSecurity, PDFWatermarker, PDFSplitter
)
from src.ui.dialogs import RotateDialog, SplitDialog, ExtractDialog, WatermarkDialog

class EventHandlers(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.file_list = main_window.file_list
        self.preview_manager = main_window.preview_manager

        # Initialize dialog references
        self.file_rotate_dialog = None
        self.file_split_dialog = None
        self.file_extract_dialog = None
        self.file_watermark_dialog = None

    def closeEvent(self, event):
        if hasattr(self, 'event_handlers'):
            self.event_handlers.main_window = None
            self.event_handlers.file_list = None
        event.accept()

    def _get_main_window(self):
        main_window = self.main_window_ref()
        if main_window is None:
            return None
        return main_window
    
    def _get_file_list(self):
        file_list = self.file_list_ref()
        if file_list is None:
            return None
        return file_list

    def _show_password_dialog(self):
        main_window = self._get_main_window()
        if not main_window:
            return None

        dialog = QInputDialog(main_window)
        dialog.setWindowTitle('输入密码')
        dialog.setLabelText('请输入加密密码：')
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        dialog.resize(300, 150)

        ok = dialog.exec()
        if ok:
            return dialog.textValue()
        return None

    def _add_files(self):
        """Add files to the file list."""
        print(self.file_list)
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.main_window, "选择 PDF 文件", "", "PDF 文件 (*.pdf)"
        )
        if file_paths:
            for file_path in file_paths:
                print(file_path)
                self.main_window.file_list.addItem(file_path)  # Access file_list through main_window
        

    def _remove_files(self):
        """Remove selected files from the list"""
        if not self._is_valid():
            return
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))
        self.preview_manager.update_preview()

    def _merge_files(self):
        """合并文件逻辑"""
        main_window = self._get_main_window()
        file_list = self._get_file_list()
        if not main_window or not file_list or file_list.count() == 0:
            QMessageBox.warning(main_window, "警告", "请先添加文件")
            return
        if not self._validate_file_list():
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
            PDFMerger.merge_pdfs(file_list, output_path, self.merge_bookmarks.isChecked())
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
            PDFSplitter.split_pdf(input_path, output_dir, mode, page_range, update_progress)
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
            PDFExtractor.extract_pages(input_path, output_path, page_range)
            QMessageBox.information(self, "成功", "页面提取完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"提取失败: {str(e)}")

    def _encrypt_current_file(self):
        main_window = self._get_main_window()
        file_list = self._get_file_list()
        if not main_window or not file_list or file_list.count() == 0:
            QMessageBox.warning(main_window, "警告", "请先选择文件")
            return

        selected_item = file_list.currentItem()
        if not selected_item:
            QMessageBox.warning(main_window, "警告", "请先选择一个文件")
            return

        password = self._show_password_dialog()
        if password is None:
            return

        output_path = os.path.splitext(selected_item.text())[0] + "_encrypted.pdf"
        try:
            PDFSecurity.encrypt_pdf(selected_item.text(), output_path, password)
            QMessageBox.information(main_window, '成功', f'文件已加密保存为：{output_path}')
        except Exception as e:
            QMessageBox.critical(main_window, '错误', f'加密失败: {str(e)}')

    def _remove_password(self):
        """Remove password from the currently selected PDF file."""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        selected_item = self.file_list.currentItem().text()
        password = self._show_password_dialog()
        
        if password is None:
            return

        # 显示新密码输入对话框（留空以移除密码）
        new_password_dialog = QInputDialog(self)
        new_password_dialog.setWindowTitle('输入新密码')
        new_password_dialog.setLabelText('请输入新密码（留空以移除密码）：')
        new_password_dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        new_password_dialog.resize(300, 150)

        ok = new_password_dialog.exec()
        if ok:
            new_password = new_password_dialog.textValue()
        else:
            return

        output_path = os.path.splitext(selected_item)[0] + "_unlocked.pdf"
        
        try:
            # 仅在提供密码时打开文档            
            doc = fitz.open(selected_item)
            if doc.needs_pass:
                doc.authenticate(password)
            # 设置保存时的加密参数
            encryption_params = {}
            if new_password:
                encryption_params['user_pw'] = new_password
                encryption_params['encryption'] = fitz.PDF_ENCRYPT_V2  # 或其他适当的加密级别
            else:
                # 移除密码保护
                encryption_params['encryption'] = fitz.PDF_ENCRYPT_NONE
            
            doc.save(output_path, **encryption_params)
            doc.close()  # 确保文档被关闭

            if new_password:
                QMessageBox.information(self, '成功', f'文件已重新加密并保存为：{output_path}')
            else:
                QMessageBox.information(self, '成功', '文件密码已成功移除！')
                    
        except fitz.fitz.FileDataError as e:
            QMessageBox.critical(self, '错误', f'无法打开文件或文件已损坏: {str(e)}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'移除密码失败: {str(e)}')

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
        
        # Open PDF with context manager to ensure proper cleanup
        with fitz.open(input_path) as doc:
            if doc.page_count == 0:  # 👈 新增有效性检查
                raise ValueError("PDF文件为空或损坏，无法处理")
        try:
            PDFWatermarker.add_watermark(
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

    def _rotate_pdf(self):
        """Rotate selected PDF pages"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        # Show rotate dialog
        dialog = RotateDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        settings = dialog.get_settings()

        input_path = self.file_list.item(0).text()
        output_dir = QFileDialog.getExistingDirectory(self, "选择输出目录")

        if not output_dir:
            return

        try:
            PDFRotator.rotate_pdfs(input_path, output_dir, settings["angle"], settings["page_range"])
            QMessageBox.information(self, "成功", "PDF旋转完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"旋转失败: {str(e)}")
