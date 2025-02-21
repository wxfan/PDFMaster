from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QWidget
)

class LLMSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置 LLM")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # API Key Section
        api_key_section = QWidget()
        api_key_layout = QHBoxLayout()
        api_key_section.setLayout(api_key_layout)
        api_key_label = QLabel("API 密钥:")
        self.api_key_edit = QLineEdit("sk_XXXXX")
        self.api_key_edit.setFixedWidth(300)
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_edit)
        layout.addWidget(api_key_section)

        # Base URL Section
        base_url_section = QWidget()
        base_url_layout = QHBoxLayout()
        base_url_section.setLayout(base_url_layout)
        base_url_label = QLabel("基础 URL:")
        self.base_url_edit = QLineEdit("https://api.siliconflow.cn/v1")
        self.base_url_edit.setFixedWidth(300)
        base_url_layout.addWidget(base_url_label)
        base_url_layout.addWidget(self.base_url_edit)
        layout.addWidget(base_url_section)

        # Model Section
        model_section = QWidget()
        model_layout = QHBoxLayout()
        model_section.setLayout(model_layout)
        model_label = QLabel("模型:")
        self.model_edit = QLineEdit("Qwen/Qwen2.5-7B-Instruct")
        self.model_edit.setFixedWidth(300)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_edit)
        layout.addWidget(model_section)

        # Add Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_settings(self):
        settings = super().get_settings()
        settings["temperature"] = self.temperature_slider.value() / 100.0
        return settings
