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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.file_handler = FileHandler(self, self.file_list)
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


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    import sys
    main()