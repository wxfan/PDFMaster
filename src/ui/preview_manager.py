from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
import fitz # type: ignore

class PreviewManager:
    def __init__(self, file_list, scroll_area, preview_layout):
        self.file_list = file_list
        self.scroll_area = scroll_area
        self.preview_layout = preview_layout

    def update_preview(self):
        file_list = self._get_file_list()
        if not file_list:
            return

        selected_items = file_list.selectedItems()
        if selected_items:
            self._show_pdf_preview(selected_items[0].text())
        else:
            self._show_empty_preview()

    def _clear_preview(self):
        while self.preview_layout.count():
            item = self.preview_layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()

    def _show_pdf_preview(self, file_path):
        try:
            self._clear_preview()
            with fitz.open(file_path) as doc:
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap(dpi=96)

                    image_label = QLabel()
                    image = QImage(
                        pix.samples,
                        pix.width,
                        pix.height,
                        QImage.Format.Format_RGB888
                    )
                    pixmap = QPixmap.fromImage(image)

                    page_label = QLabel(f"第 {page_num + 1} 页")
                    page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    page_label.setStyleSheet("font-size: 14px; font-weight: bold;")

                    image_label.setPixmap(pixmap)
                    image_label.setFixedSize(500, 700)
                    image_label.setScaledContents(True)
                    self.preview_layout.addWidget(image_label)
                    self.preview_layout.addWidget(page_label)

        except Exception as e:
            error_label = QLabel("无法预览文件")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.preview_layout.addWidget(error_label)
            print(f"预览 PDF 出错: {str(e)}")

    def _show_empty_preview(self):
        empty_label = QLabel("请选择 PDF 文件进行预览")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_layout.addWidget(empty_label)
