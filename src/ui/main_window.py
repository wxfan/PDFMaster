<<<<<<< HEAD
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout, QListWidget, QApplication
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

from src.ui.dialogs.extract_dialog import ExtractDialog
from src.ui.dialogs.rotate_dialog import RotateDialog
from src.ui.dialogs.split_dialog import SplitDialog
from src.ui.dialogs.watermark_dialog import WatermarkDialog
from src.ui.handlers.encryption_handler import EncryptionHandler
from src.ui.handlers.file_handler import FileHandler
from src.ui.handlers.pdf_processing_handler import PDFProcessingHandler
from src.ui.handlers.preview_handler import PreviewHandler
from .menu_bar import MenuBarSetup

=======
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
from src.core import *
from src.ui.menu_bar import MenuBar  # Import the update_preview function
from src.ui.handlers.encrypt_handler import encrypt_handler
from src.ui.handlers.decrypt_handler import decrypt_handler
from src.ui.handlers.extract_handler import extract_handler
from src.ui.handlers.split_handler import split_handler
from src.ui.handlers.watermark_handler import watermark_handler
from src.ui.handlers.merge_handler import merge_handler
from src.ui.handlers.rotate_handler import rotate_handler
>>>>>>> refactercode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
<<<<<<< HEAD
        self.setWindowTitle("PDFMaster - PDF 文档处理工具")
        self.resize(1200, 800)
                
        # Initialize UI components
        self._setup_ui()
        
        # Initialize handlers after UI setup
        self._init_handlers()
        
        # Initialize dialogs
        self.init_dialogs()
        
        # Setup menu bar
        self.menu_bar_setup = MenuBarSetup(self)
        self.menu_bar_setup.setup_menu()

    def _setup_ui(self):
        """Setup UI components and layout"""
        main_layout = QVBoxLayout()
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        # Preview area setup
        self.scroll_area = QScrollArea()
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.preview_layout.setSpacing(10)
        self.preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.preview_container)
        self.scroll_area.setWidgetResizable(True)
        
        # File list setup

        # 左侧文件列表区
        self.file_list_model = QStandardItemModel()
        self.file_list = QListWidget()
        self.file_list.setModel(self.file_list_model)
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        main_layout.addWidget(self.file_list, 1)  # 弹性布局        
        
        # Add components to layout
        main_layout.addWidget(self.scroll_area, stretch=4)
        
        # Set central widget
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # 连接信号
        self.file_list.currentItemChanged.connect(self.update_preview)

    def _init_handlers(self):
        """Initialize all event handling handlers"""
        self.file_handler = FileHandler(self, self.file_list_model)
        self.file_handler.fileAdded.connect(self._on_file_added)
        self.pdf_processing_handler = PDFProcessingHandler(self)
        self.encryption_handler = EncryptionHandler(self)
        self.preview_handler = PreviewHandler(self)

    def init_dialogs(self):
        """初始化对话框"""
        self.rotate_dialog = RotateDialog(self)
        self.split_dialog = SplitDialog(self)
        self.extract_dialog = ExtractDialog(self)
        self.watermark_dialog = WatermarkDialog(self)

    # 事件处理方法
    def add_files(self):
        self.file_handler._add_files()

    def remove_files(self):
        self.file_handler._remove_files()

    def merge_files(self):
        self.pdf_processing_handler._merge_files()

    def split_files(self):
        self.pdf_processing_handler._split_files()

    def extract_pages(self):
        self.pdf_processing_handler._extract_pages()

    def encrypt_current_file(self):
        self.encryption_handler._encrypt_current_file()

    def remove_password(self):
        self.encryption_handler._remove_password()

    def add_watermark(self):
        self.pdf_processing_handler._add_watermark()

    def rotate_pdf(self):
        self.pdf_processing_handler._rotate_pdf()

    def update_preview(self, file_path=None):
        """更新预览区域"""
        if file_path:
            self.preview_handler.update_preview(file_path)
        else:
            self.preview_handler.show_empty_preview()

    def _on_file_added(self):
        if self.file_list_model.rowCount() > 0:
            self.file_list.setCurrentRow(0)
            self.update_preview()


def main():
=======
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

if __name__ == "__main__":
    import sys

>>>>>>> refactercode
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
<<<<<<< HEAD
    sys.exit(app.exec())


if __name__ == "__main__":
    import sys
    main()
=======
    sys.exit(app.exec())
>>>>>>> refactercode
