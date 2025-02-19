from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QSpinBox,
    QDialogButtonBox
)

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