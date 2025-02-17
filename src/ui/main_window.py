from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout, QListWidget,
    QCheckBox
)
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
        
        self.file_list = None  # Explicit initialization
        
        # Setup UI components first
        self._setup_ui()
        
        # Initialize handlers
        self._init_handlers()
        
        # Initialize dialogs
        self._init_dialogs()
        
        # Setup menu bar
        self.menu_bar_setup = MenuBarSetup(self)
        self.menu_bar_setup.setup_menu()

    def _init_handlers(self):
        """Initialize all event handling handlers"""
        self.file_handler = FileHandler(self)
        self.file_handler.file_list = self.file_list  # Ensure handler has valid reference
        self.pdf_processing_handler = PDFProcessingHandler(self)
        self.encryption_handler = EncryptionHandler(self)
        self.preview_handler = PreviewHandler(self)

    def _setup_ui(self):
        """Setup UI components and layout"""
        # Left panel - File list
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        
        # Main layout setup
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
        
        # Add components to layout
        content_layout.addWidget(self.file_list, stretch=2)
        main_layout.addWidget(self.scroll_area, stretch=4)
        
        # Set central widget
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _init_dialogs(self):
        """Initialize dialogs"""
        self.file_rotate_dialog = RotateDialog(self)
        self.file_split_dialog = SplitDialog(self)
        self.file_extract_dialog = ExtractDialog(self)
        self.file_watermark_dialog = WatermarkDialog(self)

    # Event handler methods
    def _add_files(self):
        self.file_handler._add_files()

    def _remove_files(self):
        self.file_handler._remove_files()

    def _merge_files(self):
        self.pdf_processing_handler._merge_files()

    def _split_files(self):
        self.pdf_processing_handler._split_files()

    def _extract_pages(self):
        self.pdf_processing_handler._extract_pages()

    def _encrypt_current_file(self):
        self.encryption_handler._encrypt_current_file()

    def _remove_password(self):
        self.encryption_handler._remove_password()

    def _add_watermark(self):
        self.pdf_processing_handler._add_watermark()

    def _rotate_pdf(self):
        self.pdf_processing_handler._rotate_pdf()

    def update_preview(self):
        self.preview_handler.update_preview()

    def show_empty_preview(self):
        self.preview_handler._show_empty_preview()

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
