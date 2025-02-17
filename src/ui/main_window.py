from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout,
    QListWidget, QCheckBox
)
from PyQt6.QtCore import Qt

from src.ui.dialogs.extract_dialog import ExtractDialog
from src.ui.dialogs.rotate_dialog import RotateDialog
from src.ui.dialogs.split_dialog import SplitDialog
from src.ui.dialogs.watermark_dialog import WatermarkDialog
from .menu_bar import MenuBarSetup

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFMaster - PDF 文档处理工具")
        self.resize(1200, 800)
        # self.setWindowIcon(QIcon(":/icons/app_icon.png"))

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

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
