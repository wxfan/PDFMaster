import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QListWidget,
    QFileDialog,
    QMessageBox,
    QGraphicsScene,
    QGraphicsView
)
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap,QAction,QImage
import fitz  # type: ignore

class PDFWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF 管理器")
        self.setGeometry(100, 100, 1200, 800)

        # 创建主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 左侧文件列表区
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        main_layout.addWidget(self.file_list, 1)  # 左侧占布局比例

        # 右侧预览区
        self.preview_scene = QGraphicsScene()
        self.preview_view = QGraphicsView(self.preview_scene)
        main_layout.addWidget(self.preview_view, 2)  # 右侧占布局比例
        # 创建菜单栏
        self.create_menu_bar()

        # 连接信号
        self.file_list.currentItemChanged.connect(self.update_preview)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        self._add_menu_action(file_menu, "添加文件", self.add_files)
        self._add_menu_action(file_menu, "移除选中", self.remove_files)
        self._add_menu_action(file_menu, "清空列表", self.clear_list)
        self._add_menu_action(file_menu, "退出", self.close)

        # 编辑菜单（占位）
        edit_menu = menu_bar.addMenu("编辑")
        self._add_menu_action(edit_menu, "合并 PDF", lambda: QMessageBox.information(self, "功能待实现", "合并 PDF 功能尚未实现。"))
        self._add_menu_action(edit_menu, "拆分 PDF", lambda: QMessageBox.information(self, "功能待实现", "拆分 PDF 功能尚未实现。"))
        self._add_menu_action(edit_menu, "提取页面", lambda: QMessageBox.information(self, "功能待实现", "提取页面功能尚未实现。"))
        self._add_menu_action(edit_menu, "旋转页面", lambda: QMessageBox.information(self, "功能待实现", "旋转页面功能尚未实现。"))

        # 安全菜单（占位）
        security_menu = menu_bar.addMenu("安全")
        self._add_menu_action(security_menu, "加密文件", lambda: QMessageBox.information(self, "功能待实现", "加密文件功能尚未实现。"))
        self._add_menu_action(security_menu, "移除密码", lambda: QMessageBox.information(self, "功能待实现", "移除密码功能尚未实现。"))
        self._add_menu_action(security_menu, "添加水印", lambda: QMessageBox.information(self, "功能待实现", "添加水印功能尚未实现。"))

    def _add_menu_action(self, menu, text, triggered_function, shortcut=None):
        action = QAction(text, self)
        if shortcut:
            action.setShortcut(shortcut)
        action.triggered.connect(triggered_function)
        menu.addAction(action)

    def add_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("PDF 文件 (*.pdf)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            for file_path in selected_files:
                if file_path not in self.file_list.findItems(file_path, Qt.MatchFlag.MatchExactly):
                    self.file_list.addItem(file_path)

    def remove_files(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择一个或多个文件进行删除。")
            return
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除选中的文件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for item in selected_items:
                self.file_list.takeItem(self.file_list.row(item))

    def clear_list(self):
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有文件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.file_list.clear()
            self.preview_widget.set_pixmap(None)

    def update_preview(self, current_item, previous_item):
        if current_item:
            file_path = current_item.text()
            try:
                pdf_document = fitz.open(file_path)
                # 获取第一页
                page = pdf_document.load_page(0)
                # 设置缩放比例
                zoom = 2.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                # 转换为 QPixmap
                qimage = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qimage)
                self.preview_widget.set_pixmap(pixmap)
            except Exception as e:
                QMessageBox.critical(self, "预览错误", f"无法预览 PDF 文件: {str(e)}")
                self.preview_scene.clear()
            else:
                self.preview_scene.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFWindow()
    window.show()
    sys.exit(app.exec())
