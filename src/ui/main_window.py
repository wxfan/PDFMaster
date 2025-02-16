from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout,
    QListWidget, QLabel, QCheckBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from src.ui.dialogs.extract_dialog import ExtractDialog
from src.ui.dialogs.rotate_dialog import RotateDialog
from src.ui.dialogs.split_dialog import SplitDialog
from src.ui.dialogs.watermark_dialog import WatermarkDialog
from .menu_bar import MenuBarSetup
from .preview_manager import PreviewManager
from .event_handlers import EventHandlers
from .preview_manager import PreviewManager
from .event_handlers import EventHandlers

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFMaster - PDF 文档处理工具")
        self.resize(1200, 800)
        self.setWindowIcon(QIcon(":/icons/app_icon.png"))

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
        self.preview_manager = PreviewManager(self.file_list, self.scroll_area, self.preview_layout)
        self.menu_bar_setup = MenuBarSetup(self)
        self.event_handlers = EventHandlers(self)  # Initialize EventHandlers once

        # Initialize dialog references
        self.event_handlers.file_rotate_dialog = RotateDialog(self)
        self.event_handlers.file_split_dialog = SplitDialog(self)
        self.event_handlers.file_extract_dialog = ExtractDialog(self)
        self.event_handlers.file_watermark_dialog = WatermarkDialog(self)

        # Connect file list selection change to preview update
        self.file_list.itemSelectionChanged.connect(self.preview_manager.update_preview)

        # Setup menu
        self.menu_bar_setup.setup_menu()
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def update_preview(self):
        """Update the preview based on the selected file(s)."""
        selected_items = self.file_list.selectedItems()
        if selected_items:
            # Assuming you want to preview the first selected file
            file_path = selected_items[0].text()  # Adjust this based on how file paths are stored in the list
            self.preview_manager.load_preview(file_path)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
