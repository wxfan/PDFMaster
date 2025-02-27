from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton


class SummaryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF 摘要")
        self.setModal(True)
        self.resize(600, 400)

        # Layout
        layout = QVBoxLayout()

        # Text area to display summary
        self.summary_text_edit = QTextEdit(self)
        self.summary_text_edit.setReadOnly(True)
        layout.addWidget(self.summary_text_edit)

        # Close button
        self.close_button = QPushButton("关闭", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def append_summary(self, text):
        """Append new text to the summary display without adding a newline."""
        cursor = self.summary_text_edit.textCursor()  # Get the current cursor
        # cursor.movePosition(cursor.End)  # Move the cursor to the end of the text
        cursor.insertText(text)  # Insert the new text without a newline
        self.summary_text_edit.setTextCursor(cursor)  # Update the cursor position
        self.summary_text_edit.ensureCursorVisible()  # Scroll to the bottom

    def closeEvent(self, event):
        """Ensure the streaming thread is properly cleaned up when the dialog is closed."""
        if hasattr(self, 'streaming_thread') and self.streaming_thread.isRunning():
            self.streaming_thread.quit()  # Stop the thread
            self.streaming_thread.wait()  # Wait for the thread to finish
        event.accept()