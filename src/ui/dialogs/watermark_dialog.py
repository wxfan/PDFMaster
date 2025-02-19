from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QDialogButtonBox,
    QFileDialog
)

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
        self.text_group = QVBoxLayout()
        self.text_group.addWidget(QLabel("水印文字:"))
        self.text_group.addWidget(self.text_edit)
        layout.addLayout(self.text_group)

        # Image controls
        self.image_path = QLineEdit()
        self.image_browse = QPushButton("选择图片")
        self.image_browse.clicked.connect(self._browse_image)
        self.image_group = QVBoxLayout()
        self.image_group.addWidget(QLabel("水印图片:"))
        self.image_group.addWidget(self.image_path)
        self.image_group.addWidget(self.image_browse)
        layout.addLayout(self.image_group)

        # Position controls
        self.x_pos = QSpinBox()
        self.y_pos = QSpinBox()
        pos_group = QVBoxLayout()
        pos_group.addWidget(QLabel("位置 (x, y):"))
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.x_pos)
        hbox_layout.addWidget(self.y_pos)
        pos_group.addLayout(hbox_layout)
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
        def _update_groups():
            show_text = self.text_radio.isChecked()
            self.text_group.setHidden(not show_text)
            self.image_group.setHidden(show_text)
        
        self.text_radio.toggled.connect(_update_groups)
        self.image_radio.toggled.connect(_update_groups)
        
        # Initialize with text mode visible
        _update_groups()

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
