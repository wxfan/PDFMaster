from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QWidget,
    QSpinBox
)
from src.core.llmsetting  import get_llm_settings, save_llm_settings


class LLMSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置 LLM")
        
        # Get saved settings
        settings = get_llm_settings()
        
        # Initialize UI components and set values from settings
        layout = QVBoxLayout()
        self.setLayout(layout)

        # API Key Section
        api_key_section = QWidget()
        api_key_layout = QHBoxLayout()
        api_key_section.setLayout(api_key_layout)
        api_key_label = QLabel("API 密钥:")
        self.api_key_edit = QLineEdit(settings.get("api_key", "sk-XXXXX"))
        self.api_key_edit.setFixedWidth(300)
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_edit)
        layout.addWidget(api_key_section)

        # Base URL Section
        base_url_section = QWidget()
        base_url_layout = QHBoxLayout()
        base_url_section.setLayout(base_url_layout)
        base_url_label = QLabel("基础 URL:")
        self.base_url_edit = QLineEdit(settings.get("base_url", "https://api.siliconflow.cn/v1"))
        self.base_url_edit.setFixedWidth(300)
        base_url_layout.addWidget(base_url_label)
        base_url_layout.addWidget(self.base_url_edit)
        layout.addWidget(base_url_section)

        # Model Section
        model_section = QWidget()
        model_layout = QHBoxLayout()
        model_section.setLayout(model_layout)
        model_label = QLabel("文本模型:")
        self.model_edit = QLineEdit(settings.get("model", "Qwen/Qwen2.5-7B-Instruct"))
        self.model_edit.setFixedWidth(300)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_edit)
        layout.addWidget(model_section)

        # add vision model
        vision_model_section = QWidget()
        vision_model_layout = QHBoxLayout()
        vision_model_section.setLayout(vision_model_layout)
        vision_model_label = QLabel("视觉模型:")
        self.vision_model_edit = QLineEdit(settings.get("visionmode", "qwen-vl-ocr"))
        self.vision_model_edit.setFixedWidth(300)
        vision_model_layout.addWidget(vision_model_label)
        vision_model_layout.addWidget(self.vision_model_edit)
        layout.addWidget(vision_model_section)
        # add vision model end

        # Temperature control
        temp_section = QWidget()
        temp_layout = QHBoxLayout()
        temp_section.setLayout(temp_layout)
        
        temp_label = QLabel("温度 (控制创造力):")
        self.temperature_slider = QSpinBox()
        self.temperature_slider.setRange(0, 100)
        self.temperature_slider.setSingleStep(10)
        self.temperature_slider.setSuffix(" %")
        # Convert float temperature to percentage
        initial_temp = int(settings.get("temperature", 0.7) * 100)
        self.temperature_slider.setValue(initial_temp)
        
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.temperature_slider)
        
        layout.insertWidget(4, temp_section)

        # Add Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_settings(self):
        settings = {}
        settings["api_key"] = self.api_key_edit.text()
        settings["base_url"] = self.base_url_edit.text()
        settings["model"] = self.model_edit.text()
        settings["visionmode"]= self.vision_model_edit.text()
        settings["temperature"] = self.temperature_slider.value() / 100.0
        return settings

