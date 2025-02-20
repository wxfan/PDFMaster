from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QComboBox,
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
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("输入您的 API 密钥")
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_edit)
        layout.addWidget(api_key_section)
        
        # Temperature Control
        temperature_section = QWidget()
        temp_layout = QHBoxLayout()
        temperature_section.setLayout(temp_layout)
        temp_label = QLabel("温度:")
        self.temp_spin = QSpinBox()
        self.temp_spin.setMinimum(0)
        self.temp_spin.setMaximum(2)
        self.temp_spin.setSingleStep(0.1)
        self.temp_spin.setValue(0.7)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.temp_spin)
        layout.addWidget(temperature_section)
        
        # Max Tokens
        tokens_section = QWidget()
        tokens_layout = QHBoxLayout()
        tokens_section.setLayout(tokens_layout)
        tokens_label = QLabel("最大 Tokens:")
        self.tokens_spin = QSpinBox()
        self.tokens_spin.setMinimum(100)
        self.tokens_spin.setMaximum(4096)
        self.tokens_spin.setValue(1024)
        tokens_layout.addWidget(tokens_label)
        tokens_layout.addWidget(self.tokens_spin)
        layout.addWidget(tokens_section)
        
        # Model Selection
        model_section = QWidget()
        model_layout = QHBoxLayout()
        model_section.setLayout(model_layout)
        model_label = QLabel("模型:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4", "gpt-4-32k"])
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        layout.addWidget(model_section)
        
        # Provider Selection
        provider_section = QWidget()
        provider_layout = QHBoxLayout()
        provider_section.setLayout(provider_layout)
        provider_label = QLabel("Provider:")
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI", "Hugging Face", "Anthropic"])
        provider_layout.addWidget(provider_label)
        provider_layout.addWidget(self.provider_combo)
        layout.addWidget(provider_section)
        
        # Add Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def get_settings(self):
        return {
            "api_key": self.api_key_edit.text(),
            "temperature": self.temp_spin.value(),
            "max_tokens": self.tokens_spin.value(),
            "model": self.model_combo.currentText(),
            "provider": self.provider_combo.currentText()
        }
from PyQt6.QtCore import Qt
