from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QSpinBox,
    QDialogButtonBox,
    QScrollArea,
    QTextEdit,
    QWidget
)

class SummaryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI 生成的摘要")
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Scrollable text display
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        scroll.setWidget(content)
        
        content_layout = QVBoxLayout()
        content.setLayout(content_layout)
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMinimumSize(600, 400)
        content_layout.addWidget(self.summary_text)
        
        layout.addWidget(scroll)
        
        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
    def set_summary(self, summary_text):
        self.summary_text.setPlainText(summary_text)

    def append_to_summary(self, chunk_text):
        self.summary_text.append(chunk_text)
