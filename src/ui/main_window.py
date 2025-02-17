from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLabel, QFileDialog, QMessageBox, QProgressBar, QTabWidget, QSpinBox,
    QLineEdit, QCheckBox, QGroupBox, QFormLayout, QSplitter, QMenuBar
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from src.core import PDFExtractor, PDFMerger, PDFSplitter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_bar = None
        self.setWindowTitle("PDFMaster - PDF 文档处理工具")
        self.resize(1000, 700)

        # 设置窗口图标
        self.setWindowIcon(QIcon(":/icons/app_icon.png"))

        # 初始化菜单栏
        self._create_menu_bar()
        
        # 初始化 UI
        self._setup_ui()

    def _setup_ui(self):
        """初始化主界面布局"""
        # 创建主菜单栏
        self._create_menu_bar()

        # 主布局
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # 左侧文件列表区域
        left_panel = self._create_file_list_panel()
        main_layout.addWidget(left_panel, stretch=1)

        # 右侧功能区域
        right_panel = self._create_function_panel()
        main_layout.addWidget(right_panel, stretch=3)

        # 设置中心部件
        self.setCentralWidget(main_widget)

    def _create_file_list_panel(self):
        """创建文件列表面板"""
        panel = QGroupBox("文件列表")
        layout = QVBoxLayout()

        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        layout.addWidget(self.file_list)

        # 操作按钮
        btn_add = QPushButton("添加文件")
        btn_add.clicked.connect(self._add_files)
        btn_remove = QPushButton("移除选中")
        btn_remove.clicked.connect(self._remove_files)
        btn_clear = QPushButton("清空列表")
        btn_clear.clicked.connect(self.file_list.clear)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_remove)
        btn_layout.addWidget(btn_clear)
        layout.addLayout(btn_layout)

        panel.setLayout(layout)
        return panel

    def _create_function_panel(self):
        """创建功能面板"""
        panel = QTabWidget()

        # 合并功能页
        merge_tab = self._create_merge_tab()
        panel.addTab(merge_tab, "合并 PDF")

        # 拆分功能页
        split_tab = self._create_split_tab()
        panel.addTab(split_tab, "拆分 PDF")

        # 提取功能页
        extract_tab = self._create_extract_tab()
        panel.addTab(extract_tab, "提取页面")

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

        tab.setLayout(layout)
        return tab

    def _add_files(self):
        """添加文件到列表"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择 PDF 文件", "", "PDF 文件 (*.pdf)"
        )
        if files:
            self.file_list.addItems(files)

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
            PDFMerger.merge_pdfs(file_list, output_path, self.merge_bookmarks.isChecked())
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

        # 执行拆分
        try:
            if self.split_mode_single.isChecked():
                PDFSplitter.split_pdf(input_path, output_dir, mode="single")
            elif self.split_mode_range.isChecked():
                start = self.split_range_start.value()
                end = self.split_range_end.value()
                PDFSplitter.split_pdf(input_path, output_dir, mode="range", page_range=(start, end))
            QMessageBox.information(self, "成功", "文件拆分完成！")
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
            PDFExtractor.extract_pages(input_path, output_path, page_range)
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
