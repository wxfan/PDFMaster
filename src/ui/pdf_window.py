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
from .menu_bar import create_menu_bar  # 导入新的菜单栏模块
from src.ui.handlers.preview_handler import PreviewHandler  # 导入新的预览处理模块
from src.ui.handlers.pdffile_handler import PDFFileHandler  # 导入新的文件处理模块

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

        # 添加翻页按钮
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一页")
        self.next_button = QPushButton("下一页")
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        preview_layout.addLayout(button_layout)

        main_layout.addWidget(preview_widget, stretch=3)  # 右侧占3份

        # 实例化 PreviewHandler 和 PDFFileHandler
        self.preview_handler = PreviewHandler(self.preview_scene, self.preview_view)
        self.file_handler = PDFFileHandler(self.file_list)

        # 创建菜单栏
        self.create_menu_bar()

        # 连接信号
        self.file_list.currentItemChanged.connect(self.update_preview)
        self.prev_button.clicked.connect(self.preview_handler.previous_page)
        self.next_button.clicked.connect(self.preview_handler.next_page)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFWindow()
    window.show()
    sys.exit(app.exec())