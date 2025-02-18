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
                # Clear previous preview
                self.preview_scene.clear()
            
                # If multiple pages, add scrollable view
                if len(self.pdf_document) > 1:
                    # Calculate combined size for all pages
                    x_pos = 0
                    y_pos = 0
                
                    for page_num in range(len(self.pdf_document)):
                        page = self.pdf_document.load_page(page_num)
                        zoom = 1.0
                        mat = fitz.Matrix(zoom, zoom)
                        pix = page.get_pixmap(matrix=mat)
                    
                        qimage = QImage(
                            pix.samples,
                            pix.width,
                            pix.height,
                            pix.stride,
                            QImage.Format.Format_RGB888
                        ).rgbSwapped()
                        pixmap = QPixmap.fromImage(qimage)
                    
                        # Add each page to the scene with vertical offset
                        self.preview_scene.addPixmap(pixmap)
                        x_pos += pixmap.width()
                        y_pos += pixmap.height()
                
                    # Set scene size to accommodate all pages
                    self.preview_scene.setSceneRect(
                        0, 0, 
                        x_pos, 
                        y_pos
                    )
                else:
                    # Single page display
                    page = self.pdf_document.load_page(0)
                    zoom = 1.0
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=mat)
                    qimage = QImage(
                        pix.samples,
                        pix.width,
                        pix.height,
                        pix.stride,
                        QImage.Format.Format_RGB888
                    ).rgbSwapped()
                    pixmap = QPixmap.fromImage(qimage)
                    self.preview_scene.addPixmap(pixmap)
                    self.preview_view.setSceneRect(QRectF(pixmap.rect()))
            
                # Reset current page counter
                self.current_page = 0
            except Exception as e:
                QMessageBox.critical(None, "预览错误", f"无法预览 PDF 文件: {str(e)}")
                self.preview_scene.clear()
                self.pdf_document = None

    # Remove the next_page and previous_page methods
