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
    QFileDialog,
    QWidget
)

from datetime import datetime

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

        # Text controls container
        self.text_widget = QWidget()
        self.text_group = QVBoxLayout(self.text_widget)
        self.text_edit = QLineEdit()
        self.text_group.addWidget(QLabel("水印文字:"))

        # Get the current date and time
        current_datetime = datetime.now()
        # Format the date and time as a string
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Set the formatted date and time as the default text of the QTextEdit
        self.text_edit.setText(formatted_datetime)

        self.text_group.addWidget(self.text_edit)
        layout.addWidget(self.text_widget)

        # Image controls container
        self.image_widget = QWidget()
        self.image_group = QVBoxLayout(self.image_widget)
        self.image_path = QLineEdit()
        self.image_path.setReadOnly(True)
        self.image_browse = QPushButton("浏览")
        self.image_browse.clicked.connect(self._browse_image)
        self.image_group.addWidget(QLabel("水印图片:"))
        self.image_group.addWidget(self.image_path)
        self.image_group.addWidget(self.image_browse)
        layout.addWidget(self.image_widget)        
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
            self.text_widget.setHidden(not show_text)
            self.image_widget.setHidden(show_text)
        
        self.text_radio.toggled.connect(_update_groups)
        self.image_radio.toggled.connect(_update_groups)
        
        # Initialize with text mode visible
        _update_groups()

    def _browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片文件", "", "图片文件 (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path.setText(file_path)

    def get_settings(self):
        settings = {
            "text": self.text_edit.text() if self.text_radio.isChecked() else None,
            "image": self.image_path.text() if self.image_radio.isChecked() else None
        }
        return settings