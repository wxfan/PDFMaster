from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLabel, QFileDialog, QMessageBox, QProgressBar, QTabWidget, QSpinBox,
    QLineEdit, QCheckBox, QGroupBox, QFormLayout, QSplitter, QProgressDialog,
    QScrollArea
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
import fitz # type: ignore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from src.core.pdf_processor import PDFProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFMaster - PDF 文档处理工具")
        self.resize(1000, 700)

        # 设置窗口图标
        self.setWindowIcon(QIcon(":/icons/app_icon.png"))

        # 初始化 UI
        self._setup_ui()

    def _setup_ui(self):
        """初始化主界面布局"""
        # 主布局
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # 左侧文件操作面板
        left_panel = QTabWidget()
        
        # 文件操作面板 - 文件管理
        file_operation_tab = QWidget()
        file_operation_layout = QVBoxLayout()
        
        # 文件列表容器
        file_list_panel = self._create_file_list_panel()
        file_operation_layout.addWidget(file_list_panel)
        
        # 文件操作按钮
        file_operation_buttons = QGroupBox("文件操作")
        file_op_buttons_layout = QVBoxLayout()
        
        btn_add_files = QPushButton("添加文件")
        btn_add_files.clicked.connect(self._add_files)
        
        btn_remove_files = QPushButton("移除选中")
        btn_remove_files.clicked.connect(self._remove_files)
        
        btn_clear_files = QPushButton("清空列表")
        btn_clear_files.clicked.connect(self.file_list.clear)
        
        file_op_buttons_layout.addWidget(btn_add_files)
        file_op_buttons_layout.addWidget(btn_remove_files)
        file_op_buttons_layout.addWidget(btn_clear_files)
        file_operation_buttons.setLayout(file_op_buttons_layout)
        
        file_operation_layout.addWidget(file_operation_buttons)
        file_operation_tab.setLayout(file_operation_layout)
        
        # 文件操作面板 - PDF处理
        pdf_operations_tab = QWidget()
        pdf_operations_layout = QVBoxLayout()
        
        # PDF 处理按钮容器
        pdf_processing_buttons = QGroupBox("PDF 处理")
        pdf_processing_layout = QVBoxLayout()
        
        # 合并 PDF 按钮
        btn_merge = QPushButton("合并 PDF")
        btn_merge.clicked.connect(self._merge_files)
        
        # 拆分 PDF 按钮
        btn_split = QPushButton("拆分 PDF")
        btn_split.clicked.connect(self._split_files)
        
        # 提取页面按钮
        btn_extract = QPushButton("提取页面")
        btn_extract.clicked.connect(self._extract_pages)
        
        pdf_processing_layout.addWidget(btn_merge)
        pdf_processing_layout.addWidget(btn_split)
        pdf_processing_layout.addWidget(btn_extract)
        pdf_processing_buttons.setLayout(pdf_processing_layout)
        
        pdf_operations_layout.addWidget(pdf_processing_buttons)
        pdf_operations_tab.setLayout(pdf_operations_layout)
        
        left_panel.addTab(file_operation_tab, "文件管理")
        left_panel.addTab(pdf_operations_tab, "PDF处理")
        
        main_layout.addWidget(left_panel, stretch=1)

        # 预览区域 (右侧面板)
        right_panel = QGroupBox("预览与处理结果")
        right_layout = QVBoxLayout()
        
        # 文件预览区域
        self.preview_widget = QLabel("请选择 PDF 文件进行预览")
        self.preview_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_widget.setMinimumSize(200, 300)
        
        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.preview_widget)
        scroll_area.setWidgetResizable(True)
        right_layout.addWidget(scroll_area)
        
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, stretch=3)

        self.setCentralWidget(main_widget)

    def _create_file_list_panel(self):
        """创建文件列表面板"""
        panel = QGroupBox("文件列表")
        layout = QVBoxLayout()

        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list.itemSelectionChanged.connect(self._update_preview)
        layout.addWidget(self.file_list)

        panel.setLayout(layout)
        return panel


    def _create_merge_tab(self):
        """创建合并功能页"""
        tab = QWidget()
        layout = QVBoxLayout()

        # 输出文件名
        output_layout = QFormLayout()
        self.merge_output_name = QLineEdit("merged.pdf")
        output_layout.addRow("输出文件名:", self.merge_output_name)
        layout.addLayout(output_layout)

        # 合并选项
        options_group = QGroupBox("合并选项")
        options_layout = QVBoxLayout()
        self.merge_bookmarks = QCheckBox("保留书签")
        self.merge_bookmarks.setChecked(True)
        options_layout.addWidget(self.merge_bookmarks)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # 合并按钮
        btn_merge = QPushButton("开始合并")
        btn_merge.clicked.connect(self._merge_files)
        layout.addWidget(btn_merge)

        tab.setLayout(layout)
        return tab

    def _create_split_tab(self):
        """创建拆分功能页"""
        tab = QWidget()
        layout = QVBoxLayout()

        # 拆分模式选择
        mode_group = QGroupBox("拆分模式")
        mode_layout = QVBoxLayout()
        self.split_mode_single = QCheckBox("每页拆分为单独文件")
        self.split_mode_range = QCheckBox("按页码范围拆分")
        mode_layout.addWidget(self.split_mode_single)
        mode_layout.addWidget(self.split_mode_range)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # 页码范围输入
        range_layout = QFormLayout()
        self.split_range_start = QSpinBox()
        self.split_range_start.setMinimum(1)
        self.split_range_end = QSpinBox()
        self.split_range_end.setMinimum(1)
        range_layout.addRow("起始页:", self.split_range_start)
        range_layout.addRow("结束页:", self.split_range_end)
        layout.addLayout(range_layout)

        # 拆分按钮
        btn_split = QPushButton("开始拆分")
        btn_split.clicked.connect(self._split_files)
        layout.addWidget(btn_split)

        tab.setLayout(layout)
        return tab

    def _create_extract_tab(self):
        """创建提取功能页"""
        tab = QWidget()
        layout = QVBoxLayout()

        # 提取选项
        options_group = QGroupBox("提取选项")
        options_layout = QFormLayout()
        self.extract_pages = QLineEdit("1,3-5,7")
        options_layout.addRow("页码范围:", self.extract_pages)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # 提取按钮
        btn_extract = QPushButton("开始提取")
        btn_extract.clicked.connect(self._extract_pages)
        layout.addWidget(btn_extract)

        tab.setLayout(layout)
        return tab

    def _update_preview(self):
        """更新 PDF 预览"""
        # 获取当前选中的文件
        selected_items = self.file_list.selectedItems()
        if selected_items:
            file_path = selected_items[0].text()
            try:
                # 打开 PDF 文件
                with fitz.open(file_path) as doc:
                    # 获取第一页
                    page = doc.load_page(0)
                    pix = page.get_pixmap(dpi=96)  # 调整 DPI 根据需要

                    # 转换为 QImage 然后转为 QPixmap
                    image = QImage(
                        pix.samples,
                        pix.width,
                        pix.height,
                        QImage.Format.Format_RGB888
                    )
                    pixmap = QPixmap.fromImage(image)

                    # 缩放并保持宽高比
                    scaled_pixmap = pixmap.scaled(
                        self.preview_widget.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )

                    # 显示预览
                    self.preview_widget.setPixmap(scaled_pixmap)
            except Exception as e:
                self.preview_widget.setText("无法预览文件")
                print(f"预览 PDF 出错: {str(e)}")
        else:
            self.preview_widget.setText("请选择 PDF 文件进行预览")

    def _add_files(self):
        """添加文件到列表"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择 PDF 文件", "", "PDF 文件 (*.pdf)"
        )
        if files:
            self.file_list.addItems(files)
            self.file_list.setCurrentRow(0)  # 自动选择第一个文件
            self._update_preview()  # 更新预览

    def _remove_files(self):
        """移除选中的文件"""
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def _merge_files(self):
        """合并文件逻辑"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        # 获取文件列表
        file_list = [self.file_list.item(i).text() for i in range(self.file_list.count())]

        # 获取输出路径
        output_path, _ = QFileDialog.getSaveFileName(
            self, "保存合并文件", "merged.pdf", "PDF 文件 (*.pdf)"
        )
        if not output_path:
            return

        # 执行合并
        try:
            PDFProcessor.merge_pdfs(file_list, output_path, self.merge_bookmarks.isChecked())
            QMessageBox.information(self, "成功", "文件合并完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"合并失败: {str(e)}")

    def _split_files(self):
        """拆分文件逻辑"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        # 获取输入文件
        input_path = self.file_list.item(0).text()

        # 获取输出目录
        output_dir = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if not output_dir:
            return

        # 创建进度对话框
        progress_dialog = QProgressDialog("正在拆分文件...", "取消", 0, 100, self)
        progress_dialog.setWindowTitle("处理进度")
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setAutoClose(True)

        def update_progress(value):
            progress_dialog.setValue(int(value * 100))
            if progress_dialog.wasCanceled():
                raise Exception("用户取消操作")

        # 执行拆分
        try:
            if self.split_mode_single.isChecked():
                PDFProcessor.split_pdf(input_path, output_dir, mode="single", progress_callback=update_progress)
                with fitz.open(input_path) as doc:
                    total_pages = len(doc)
                QMessageBox.information(self, "成功", f"文件拆分完成！共输出了 {total_pages} 个文件。")
            elif self.split_mode_range.isChecked():
                start = self.split_range_start.value()
                end = self.split_range_end.value()
                PDFProcessor.split_pdf(input_path, output_dir, mode="range", page_range=(start, end))
                QMessageBox.information(self, "成功", f"文件拆分完成！输出了 {end - start + 1} 个页面。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"拆分失败: {str(e)}")

    def _extract_pages(self):
        """提取页面逻辑"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return

        # 获取输入文件
        input_path = self.file_list.item(0).text()

        # 获取输出路径
        output_path, _ = QFileDialog.getSaveFileName(
            self, "保存提取文件", "extracted.pdf", "PDF 文件 (*.pdf)"
        )
        if not output_path:
            return

        # 执行提取
        try:
            page_range = self.extract_pages.text()
            PDFProcessor.extract_pages(input_path, output_path, page_range)
            QMessageBox.information(self, "成功", "页面提取完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"提取失败: {str(e)}")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 设置跨平台样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
