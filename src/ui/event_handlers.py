from PyQt6.QtCore import QObject
from src.ui.handlers.file_handler import FileHandler
from src.ui.handlers.pdf_processing_handler import PDFProcessingHandler
from src.ui.handlers.encryption_handler import EncryptionHandler
from src.ui.handlers.preview_handler import PreviewHandler

class EventHandlers(QObject):
    def _init_handlers(self):
        """Initialize all event handling handlers"""
        self.file_handler = FileHandler(self)
        self.pdf_processing_handler = PDFProcessingHandler(self)
        self.encryption_handler = EncryptionHandler(self)
        self.preview_handler = PreviewHandler(self)

    def _add_files(self):
        self.file_handler._add_files()

    def _remove_files(self):
        self.file_handler._remove_files()

    def _merge_files(self):
        self.pdf_processing_handler._merge_files()

    def _split_files(self):
        self.pdf_processing_handler._split_files()

    def _extract_pages(self):
        self.pdf_processing_handler._extract_pages()

    def _encrypt_current_file(self):
        self.encryption_handler._encrypt_current_file()

    def _remove_password(self):
        self.encryption_handler._remove_password()

    def _add_watermark(self):
        self.pdf_processing_handler._add_watermark()

    def _rotate_pdf(self):
        self.pdf_processing_handler._rotate_pdf()

    def update_preview(self):
        self.preview_handler.update_preview()

    def show_empty_preview(self):
        self.preview_handler._show_empty_preview()
