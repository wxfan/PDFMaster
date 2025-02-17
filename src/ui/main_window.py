from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout,
    QListWidget, QCheckBox
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

        # Initialize UI components
        self.merge_bookmarks = QCheckBox("保留书签", self)

        # Left panel - File list
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)  # Changed to single selection for clarity
        
        # Create main vertical layout
        main_layout = QVBoxLayout()

        # Create content layout for file list and preview
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.addWidget(self.file_list, stretch=2)  # Adjusted stretch for better layout

        # Right panel - Preview area
        self.scroll_area = QScrollArea()
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.preview_layout.setSpacing(10)
        self.preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area.setWidget(self.preview_container)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area, stretch=4)  # Adjusted stretch for better layout

        # Initialize other components        
        self.menu_bar_setup = MenuBarSetup(self)
        self._init_handlers()

        # Initialize dialog references
        self.file_rotate_dialog = RotateDialog(self)
        self.file_split_dialog = SplitDialog(self)
        self.file_extract_dialog = ExtractDialog(self)
        self.file_watermark_dialog = WatermarkDialog(self)
        self.file_preview_handler = WatermarkDialog(self)

        # Setup menu
        self.menu_bar_setup.setup_menu()
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _init_handlers(self):
        """Initialize all event handling handlers"""
        self.file_handler = FileHandler(self)
        self.pdf_processing_handler = PDFProcessingHandler(self)
        self.encryption_handler = EncryptionHandler(self)
        self.preview_handler = PreviewHandler(self)

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
