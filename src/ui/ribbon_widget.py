from PyQt6.QtWidgets import QWidget, QTabWidget, QToolBar, QToolButton, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class RibbonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                padding: 8px;
                background: #f0f0f0;
                border: 1px solid #ccc;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: #fff;
            }
        """)
        layout.addWidget(self.tab_widget)

    def add_tab(self, title):
        """Add a new tab to the ribbon"""
        tab = QWidget()
        self.tab_widget.addTab(tab, title)
        return tab

    def add_group(self, tab, title):
        """Add a group to a tab"""
        group = QToolBar(title)
        group.setOrientation(Qt.Orientation.Horizontal)
        group.setMovable(False)
        group.setFloatable(False)
        group.setStyleSheet("QToolBar { border: none; }")
        
        # Add group to tab layout
        if not tab.layout():
            tab_layout = QVBoxLayout()
            tab_layout.setContentsMargins(5, 5, 5, 5)
            tab.setLayout(tab_layout)
        tab.layout().addWidget(group)
        
        return group

    def add_action(self, group, icon, text, callback, shortcut=None):
        """Add an action to a group"""
        button = QToolButton()
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        button.setIcon(QIcon(icon))
        button.setText(text)
        if shortcut:
            button.setShortcut(shortcut)
        button.clicked.connect(callback)
        group.addWidget(button)
        return button
