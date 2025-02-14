from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QSpinBox,
    QDialogButtonBox,
    QLineEdit
)
from PyQt6.QtCore import Qt

class SplitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF拆分设置")
        
        layout = QVBoxLayout()
        
        # Single page mode
        self.single_radio = QRadioButton("逐页拆分")
        self.single_radio.setChecked(True)
        layout.addWidget(self.single_radio)
        
        # Range mode
        self.range_radio = QRadioButton("按范围拆分")
        layout.addWidget(self.range_radio)
        
        # Range controls
        range_row = QHBoxLayout()
        self.start_spin = QSpinBox()
        self.start_spin.setRange(1, 10000)
        self.start_spin.setValue(1)
        self.end_spin = QSpinBox()
        self.end_spin.setRange(1, 10000)
        self.end_spin.setValue(1)
        
        range_row.addWidget(QLabel("开始页:"))
        range_row.addWidget(self.start_spin)
        range_row.addWidget(QLabel("结束页:"))
        range_row.addWidget(self.end_spin)
        layout.addLayout(range_row)
        
        # Button box
        buttons = QDialogButtonBox()
        buttons.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        self.range_radio.toggled.connect(lambda: self.start_spin.setEnabled(self.range_radio.isChecked()))
        self.range_radio.toggled.connect(lambda: self.end_spin.setEnabled(self.range_radio.isChecked()))

    def get_settings(self):
        if self.single_radio.isChecked():
            return {"mode": "single"}
        else:
            return {"mode": "range", "start": self.start_spin.value(), "end": self.end_spin.value()}

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
