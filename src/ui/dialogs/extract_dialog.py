from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox
)

class ExtractDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF提取设置")
        
        layout = QVBoxLayout()
        
        # Page range input
        self.range_edit = QLineEdit()
        self.range_edit.setPlaceholderText("输入页码范围, 例如: 1-3,5,7")
        layout.addWidget(QLabel("页码范围:"))
        layout.addWidget(self.range_edit)
        
        # Button box
        buttons = QDialogButtonBox()
        buttons.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)

    def get_settings(self):
        return {"page_range": self.range_edit.text()}