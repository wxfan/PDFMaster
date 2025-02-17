import sys
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QMenuBar,
    QToolBar, QListView, QGraphicsView, QPushButton,
    QLabel, QSpinBox, QScrollArea, QGraphicsScene, 
    QHBoxLayout
)
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QTransform

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Master")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Create left layout for file list
        left_layout = QVBoxLayout()
        self.file_list = QListView()
        self.file_list.setFixedSize(300, 400)
        left_layout.addWidget(self.file_list)
        
        # Add file management buttons
        self.add_file_btn = QPushButton(parent=self, text="添加文件")
        self.remove_file_btn = QPushButton(parent=self, text="移除文件")
        left_layout.addWidget(self.add_file_btn)
        left_layout.addWidget(self.remove_file_btn)
        
        # File status
        self.file_status = QLabel("未选择文件")
        left_layout.addWidget(self.file_status)
        
        # Create right layout for preview
        self.preview_area = QGraphicsView()
        self.preview_area.setFixedSize(700, 600)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.preview_area)
        
        # Add zoom controls
        self.zoom_level = QSpinBox()
        self.zoom_level.setRange(1, 400)
        self.zoom_level.setSingleStep(10)
        self.zoom_level.setValue(100)
        right_layout.addWidget(QLabel("缩放比例:"))
        right_layout.addWidget(self.zoom_level)
        
        # Menu bar
        menu_bar = QMenuBar()
        main_layout.addWidget(menu_bar)
        
        # Create splitter to hold left and right layouts
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)  # Right side takes more space
        
        # Left side: file management
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # File list
        self.file_list = QListView()
        self.file_list.setFixedSize(280, 400)
        left_layout.addWidget(QLabel("文件列表"))
        left_layout.addWidget(self.file_list)
        
        # Add/remove buttons
        button_layout = QHBoxLayout()
        self.add_file_btn = QPushButton("添加文件")
        self.remove_file_btn = QPushButton("移除文件")
        button_layout.addWidget(self.add_file_btn)
        button_layout.addWidget(self.remove_file_btn)
        left_layout.addLayout(button_layout)
        
        # File status
        self.file_status = QLabel("未选择文件")
        left_layout.addWidget(self.file_status)
        
        # Add spacer
        left_layout.addStretch()
        
        # Right side: preview area
        self.preview_area = QGraphicsView()
        self.preview_area.setScene(QGraphicsScene())
        self.preview_area.setRenderHint(QPainter.Antialiasing)
        
        # Add zoom controls
        zoom_layout = QHBoxLayout()
        self.zoom_level = QSpinBox()
        self.zoom_level.setRange(1, 400)
        self.zoom_level.setSingleStep(10)
        self.zoom_level.setValue(100)
        zoom_layout.addWidget(QLabel("缩放比例:"))
        zoom_layout.addWidget(self.zoom_level)
        zoom_layout.addStretch()
        
        # Add to splitter
        splitter.addWidget(left_container)
        splitter.addWidget(self.preview_area)
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set main widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
```

这个布局包括：
1. 顶部菜单栏
2. 左侧文件列表区域，包含文件管理按钮和状态显示
3. 右侧预览区域，可以显示PDF内容，并有缩放控制
4. 使用Splitter来分隔左右区域，便于用户调整大小

让我们继续完善布局的代码：

src\ui\main_window.py
```python
<<<<<<< SEARCH
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QMenuBar, 
    QToolBar, QListView, QGraphicsView
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Master")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main layout
        main_layout = QHBoxLayout()
