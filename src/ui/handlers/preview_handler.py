<<<<<<< HEAD
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtWidgets import QGraphicsTextItem, QMessageBox,QTextFormat
import fitz  # type: ignore


class PreviewHandler:
    def __init__(self, preview_scene, preview_view):
        self.preview_scene = preview_scene
        self.preview_view = preview_view
        self.pdf_document = None
        self.current_page = 0
        self.text_item = None  # For displaying page number
        if self.text_item is None:
            self.text_item = QGraphicsTextItem()
            self.text_item.setPlainText("当前页数")
            self.text_item.setPos(10, 10)
            self.text_item.setZValue(10)
            self.preview_scene.addItem(self.text_item)
            
            # Set text styling using painter
            self.set_text_style()
            
    def set_text_style(self):
        """Set the text styling properties"""
        font = self.text_item.font()
        font.setPointSize(12)
        self.text_item.setFont(font)
        
    def draw_page_number(self, pixmap, page_number):
        """Draw page number on the pixmap"""
        painter = QPainter(pixmap)
        painter.setPen(Qt.GlobalColor.white)
        painter.setBrush(Qt.GlobalColor.black)
        painter.setFont(self.text_item.font())
        
        # Calculate text position
        text = f"第 {page_number + 1} 页"
        bounding_rect = painter.drawText(10, 10, text)
        
        painter.end()
        return pixmap

    def update_preview(self, file_path, page_number=0):
        """更新预览区域"""
        if file_path:
            try:
                self.pdf_document = fitz.open(file_path)
                # Clear previous preview
                self.preview_scene.clear()
            
                # If multiple pages, add scrollable view
                if len(self.pdf_document) > 1:
                    # Calculate combined size for all pages (stacked vertically)
                    max_page_width = 0
                    total_page_height = 0
                
                    # First pass: calculate cumulative dimensions
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
                    
                        # Update max width and total height
                        max_page_width = max(max_page_width, pixmap.width())
                        total_page_height += pixmap.height()
                
                    # Set scene size to accommodate all pages
                    self.preview_scene.setSceneRect(
                        0, 0, 
                        max_page_width, 
                        total_page_height
                    )
                
                    # Second pass: add pages to the scene
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
                        # Draw page number on image
                        self.draw_page_number(pixmap, page_num)
                        # Add each page to the scene with vertical offset
                        pixmap_item = self.preview_scene.addPixmap(pixmap)
                        pixmap_item.setPos(0, y_pos)
                        y_pos += pixmap.height()

                    # Connect scroll to update page text
                    self.preview_view.verticalScrollBar().valueChanged.connect(lambda: self._update_page_text(y_pos, len(self.pdf_document)))
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
                    # Draw page number on image
                    self.draw_page_number(pixmap, 0)
                    self.preview_scene.addPixmap(pixmap)
                    self.preview_view.setSceneRect(QRectF(pixmap.rect()))
            
                # Update initial page text
                if len(self.pdf_document) > 0:
                    self._update_page_text(0, len(self.pdf_document))
                    self.draw_page_number(self.preview_scene.items()[-1].pixmap(), 0)
                
                # Reset current page counter
                self.current_page = 0
            except Exception as e:
                QMessageBox.critical(None, "预览错误", f"无法预览 PDF 文件: {str(e)}")
                self.preview_scene.clear()
                self.pdf_document = None

    def _update_page_text(self, total_height, total_pages):
        """更新页面信息文本"""
        # Get current position
        current_pos = self.preview_view.verticalScrollBar().value()
        
        # Calculate approx current page
        # This assumes all pages have approximately the same height
        page_height = total_height / total_pages if total_pages > 0 else 1
        current_page = current_pos // page_height
        
        # Set text
        if self.text_item:
            self.text_item.setPlainText(f"Page {current_page + 1}/{total_pages}")

    # Remove the next_page and previous_page methods
=======
# preview_handler.py

from PyQt6.QtWidgets import  QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
import fitz  # type:ignore
import os

def update_preview(file_list, preview_layout):
    """更新 PDF 预览"""
    # 获取当前选中的文件
    selected_items = file_list.selectedItems()
    if selected_items:
        file_path = selected_items[0].text()
        try:
            # 清除之前的预览
            while preview_layout.count():
                item = preview_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # 打开 PDF 文件
            with fitz.open(file_path) as doc:
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap(dpi=96)

                    # 创建图片标签
                    image_label = QLabel()
                    image = QImage(
                        pix.samples,
                        pix.width,
                        pix.height,
                        QImage.Format.Format_RGB888
                    )
                    pixmap = QPixmap.fromImage(image)

                    # 添加页码
                    page_label = QLabel(f"第 {page_num + 1} 页")
                    page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    page_label.setStyleSheet("font-size: 14px; font-weight: bold;")

                    # 添加到布局
                    image_label.setPixmap(pixmap.scaled(
                        500, 700,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    ))
                    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    preview_layout.addWidget(image_label)
                    preview_layout.addWidget(page_label)

        except Exception as e:
            error_label = QLabel("无法预览文件")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            preview_layout.addWidget(error_label)
            print(f"预览 PDF 出错: {str(e)}")
    else:
        empty_label = QLabel("请选择 PDF 文件进行预览")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(empty_label)
>>>>>>> refactercode
