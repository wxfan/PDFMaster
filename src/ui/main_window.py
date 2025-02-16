from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout,
    QListWidget, QLabel, QCheckBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
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
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)

        # Create main vertical layout
        main_layout = QVBoxLayout()

        # Create content layout for file list and preview
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.addWidget(self.file_list, stretch=1)

        # Right panel - Preview area
        self.scroll_area = QScrollArea()
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.preview_layout.setSpacing(10)
        self.preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area.setWidget(self.preview_container)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area, stretch=3)

        # Initialize other components
        self.preview_manager = PreviewManager(self.file_list, self.scroll_area, self.preview_layout)
        self.menu_bar_setup = MenuBarSetup(self)
        self.event_handlers = EventHandlers(self)

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
