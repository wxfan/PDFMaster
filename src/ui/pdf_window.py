import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QListWidget,
    QGraphicsScene,
    QGraphicsView,
    QPushButton,
    QVBoxLayout,
    QSizePolicy
)
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt  # 导入 Qt 模块
from .menu_bar import create_menu_bar  # 导入新的菜单栏模块
from src.ui.handlers.preview_handler import PreviewHandler  # 导入新的预览处理模块
from src.ui.handlers.addfile_handler import AddFileHandler  # 导入新的文件处理模块

class PDFWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF 管理器")
        self.resize(1200, 800)

        # 设置窗口最大尺寸为屏幕尺寸，防止超出全屏
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setMaximumSize(screen_geometry.width(), screen_geometry.height())

        # 创建主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 左侧文件列表区
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.file_list.setFixedWidth(200)  # 设置固定宽度
        main_layout.addWidget(self.file_list)

        # 右侧预览区
        preview_widget = QWidget()
        preview_layout = QHBoxLayout(preview_widget)

        self.preview_scene = QGraphicsScene()
        self.preview_view = QGraphicsView(self.preview_scene)
        self.preview_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.preview_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        preview_layout.addWidget(self.preview_view, stretch=3)  # 右侧占3份

        # Enable scrolling for the QGraphicsView
        self.preview_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.preview_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        main_layout.addWidget(preview_widget, stretch=3)  # 右侧占3份

        # 实例化 PreviewHandler 和 PDFFileHandler
        self.preview_handler = PreviewHandler(self.preview_scene, self.preview_view)
        self.file_handler = AddFileHandler(self.file_list)

        # 创建菜单栏
        self.create_menu_bar()

        # 连接信号
        self.file_list.currentItemChanged.connect(self.update_preview)

    def update_menu_bar(self, current_page, total_pages):
        """更新菜单栏中的当前页面信息"""
        window_title = f"PDF 管理器 - 当前页面: {current_page}/{total_pages}"
        self.setWindowTitle(window_title)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        create_menu_bar(menu_bar, self)  # 使用新的菜单栏模块

    def add_files(self):
        """添加文件到文件列表"""
        self.file_handler.add_files()

    def remove_files(self):
        """从文件列表中删除选中的文件"""
        self.file_handler.remove_files()

    def clear_list(self):
        """清空文件列表"""
        self.file_handler.clear_list()

    def update_preview(self, current_item):
        """更新预览区域"""
        if current_item:
            file_path = current_item.text()
            self.preview_handler.update_preview(file_path, page_number=0)  # 初始显示第一页
            # Update menu bar with current page information
            total_pages = self.preview_handler.pdf_document.page_count if self.preview_handler.pdf_document else 0
            if total_pages > 0:
                self.update_menu_bar(1, total_pages)  # Page count starts at 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFWindow()
    window.show()
    sys.exit(app.exec())
