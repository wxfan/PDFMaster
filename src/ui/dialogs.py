from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QSpinBox,
    QDialogButtonBox,
    QLineEdit,
    QPushButton,
    QDoubleSpinBox,
    QFileDialog
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

class WatermarkDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加水印")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Watermark type
        self.text_radio = QRadioButton("文字水印")
        self.image_radio = QRadioButton("图片水印")
        self.text_radio.setChecked(True)
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.text_radio)
        mode_layout.addWidget(self.image_radio)
        layout.addLayout(mode_layout)

        # Text controls
        self.text_edit = QLineEdit()
        text_group = QVBoxLayout()
        text_group.addWidget(QLabel("水印文字:"))
        text_group.addWidget(self.text_edit)
        layout.addLayout(text_group)

        # Image controls
        self.image_path = QLineEdit()
        self.image_browse = QPushButton("选择图片")
        self.image_browse.clicked.connect(self._browse_image)
        image_group = QVBoxLayout()
        image_group.addWidget(QLabel("水印图片:"))
        image_group.addWidget(self.image_path)
        image_group.addWidget(self.image_browse)
        layout.addLayout(image_group)

        # Position controls
        self.x_pos = QSpinBox()
        self.y_pos = QSpinBox()
        pos_group = QVBoxLayout()
        pos_group.addWidget(QLabel("位置 (x, y):"))
        pos_group.addWidget(QHBoxLayout([self.x_pos, self.y_pos]))
        layout.addLayout(pos_group)

        # Opacity and rotation controls
        self.opacity = QDoubleSpinBox()
        self.rotation = QSpinBox()
        self.opacity.setRange(0.0, 1.0)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(1.0)
        self.rotation.setRange(0, 360)
        self.rotation.setValue(0)
        other_group = QVBoxLayout()
        other_group.addWidget(QLabel("透明度:"))
        other_group.addWidget(self.opacity)
        other_group.addWidget(QLabel("旋转角度 (度):"))
        other_group.addWidget(self.rotation)
        layout.addLayout(other_group)

        # Buttons
        button_box = QDialogButtonBox()
        button_box.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Enable/disable controls based on mode
        self.text_radio.toggled.connect(lambda: text_group.setEnabled(self.text_radio.isChecked()))
        self.image_radio.toggled.connect(lambda: image_group.setEnabled(self.image_radio.isChecked()))

    def _browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片文件", "", "图片文件 (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.image_path.setText(file_path)

    def get_settings(self):
        settings = {
            "text": self.text_edit.text() if self.text_radio.isChecked() else None,
            "image": self.image_path.text() if self.image_radio.isChecked() else None,
            "opacity": self.opacity.value(),
            "rotation": self.rotation.value(),
            "position": (self.x_pos.value(), self.y_pos.value())
        }
        return settings
