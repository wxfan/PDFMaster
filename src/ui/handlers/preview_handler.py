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