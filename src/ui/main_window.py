# main_window.py
from PyQt6.QtWidgets import (QMainWindow, QListWidget, QVBoxLayout, QWidget,  QHBoxLayout, 
                             QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog
import fitz  # type:ignore
import os
from src.ui.handlers.preview_handler import update_preview
from src.core import *
from src.ui.menu_bar import MenuBar  # Import the update_preview function
from src.core.summary import summary_text
from src.ui.handlers.encrypt_handler import encrypt_handler
from src.ui.handlers.decrypt_handler import decrypt_handler
from src.ui.handlers.extract_handler import extract_handler
from src.ui.handlers.split_handler import split_handler
from src.ui.handlers.watermark_handler import watermark_handler
from src.ui.handlers.merge_handler import merge_handler
from src.ui.handlers.rotate_handler import rotate_handler
from src.ui.handlers.summary_handler import summary_handler
from src.ui.handlers.extract_handler import extract_handler
from src.ui.handlers.llmsettings_handler import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 处理工具")
        self.setGeometry(100, 100, 1000, 800)

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
                    if not verify_password(file_path, password):
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
        merge_handler(self)  # Call the new merge_files function


    # Updated to call the new function in split_files module
    def _split_files(self):
        split_handler(self)

    # Updated to call the new function in extract_pages module
    def _extract_pages(self):
        extract_handler(self)
    
    # rorate_files method remains unchanged
    def _rotate_files(self):
        rotate_handler(self)

    # Updated to call the new function in encrypt_current_file module
    def _encrypt_current_file(self):
        encrypt_handler(self)

    def _decrypt_current_file(self):
        decrypt_handler(self)


    # Updated to call the new function in add_watermark module
    def _add_watermark(self):
        watermark_handler(self)
    
    def settings_llm(self):   
        llmsettings_handler(self)     
        settings = get_llm_settings()
        return settings
    
    def gettings_llm(self):      
        settings = get_llm_settings()
        return settings

    def _summary_text(self):
        summary_handler(self)
    
    def _extract_text(self):
        extract_handler(self)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
