from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QMessageBox
import fitz  # type: ignore


class PreviewHandler:
    def __init__(self, preview_scene, preview_view):
        self.preview_scene = preview_scene
        self.preview_view = preview_view
        self.pdf_document = None
        self.current_page = 0

    def update_preview(self, file_path, page_number=0):
        """更新预览区域"""
        if file_path:
            try:
                self.pdf_document = fitz.open(file_path)
                self.current_page = page_number
                page = self.pdf_document.load_page(self.current_page)
                # 设置缩放比例
                zoom = 1.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                # Convert the pixmap to QImage using correct format
                qimage = QImage(
                    pix.samples,
                    pix.width,
                    pix.height,
                    pix.stride,
                    QImage.Format.Format_RGB888  # 使用正确的格式
                ).rgbSwapped()  # 转换为 RGB 格式
                pixmap = QPixmap.fromImage(qimage)
                # 清除之前的预览并添加新的图像
                self.preview_scene.clear()
                self.preview_scene.addPixmap(pixmap)
                # 设置视图大小适应图像
                view_rect = QRectF(pixmap.rect())
                self.preview_view.setSceneRect(view_rect)
                # 不设置固定大小，以允许场景矩形调整
            except Exception as e:
                QMessageBox.critical(None, "预览错误", f"无法预览 PDF 文件: {str(e)}")
                self.preview_scene.clear()
                self.pdf_document = None

    def next_page(self):
        """翻到下一页"""
        if self.pdf_document is not None:
            if self.current_page < len(self.pdf_document) - 1:
                self.current_page += 1
                self.update_preview(None, self.current_page)

    def previous_page(self):
        """翻到上一页"""
        if self.pdf_document is not None:
            if self.current_page > 0:
                self.current_page -= 1
                self.update_preview(None, self.current_page)