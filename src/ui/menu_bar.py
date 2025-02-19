<<<<<<< HEAD
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction

class MenuBarSetup:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_bar = main_window.menuBar()

    def setup_menu(self):
        # 文件菜单
        file_menu = self.menu_bar.addMenu("文件")
        self._add_menu_action(file_menu, "添加文件", self.main_window.event_handlers._add_files)
        self._add_menu_action(file_menu, "移除选中", self.main_window.event_handlers._remove_files)
        self._add_menu_action(file_menu, "清空列表", lambda: self.main_window.file_list.clear())
        self._add_menu_action(file_menu, "退出", self.main_window.close)

        # 编辑菜单
        edit_menu = self.menu_bar.addMenu("编辑")
        self._add_menu_action(edit_menu, "合并 PDF", self.main_window.event_handlers._merge_files)
        self._add_menu_action(edit_menu, "拆分 PDF", self.main_window.event_handlers._split_files)
        self._add_menu_action(edit_menu, "提取页面", self.main_window.event_handlers._extract_pages)
        self._add_menu_action(edit_menu, "旋转页面", self.main_window.event_handlers._rotate_pdf)

        # Security menu
        security_menu = self.menu_bar.addMenu("安全")
        self._add_menu_action(security_menu, "加密文件", self.main_window.event_handlers._encrypt_current_file)
        self._add_menu_action(security_menu, "移除密码", self.main_window.event_handlers._remove_password)
        self._add_menu_action(security_menu, "添加水印", self.main_window.event_handlers._add_watermark)

    def _add_menu_action(self, menu, text, callback):
        action = QAction(text, self.main_window)
        action.triggered.connect(callback)
        menu.addAction(action)
=======
# menu_bar.py

class MenuBar:
    def __init__(self, main_window):
        self.main_window = main_window
        self.create_menus()

    def create_menus(self):
        menubar = self.main_window.menuBar()

        # File menu
        file_menu = menubar.addMenu("文件")
        file_menu.addAction("添加文件", self.main_window._add_files)
        file_menu.addAction("移除选中", self.main_window._remove_files)
        file_menu.addAction("清空列表", lambda: self.main_window.file_list.clear())
        file_menu.addAction("退出", self.main_window.close)

        # Edit menu
        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction("合并", self.main_window._merge_files)
        edit_menu.addAction("拆分", self.main_window._split_files)
        edit_menu.addAction("提取页面", self.main_window._extract_pages)
        edit_menu.addAction("旋转页面", self.main_window._rotate_files)       

        # Security menu
        security_menu = menubar.addMenu("安全")
        security_menu.addAction("加密", self.main_window._encrypt_current_file)
        security_menu.addAction("解密", self.main_window._decrypt_current_file)
        security_menu.addAction("添加水印", self.main_window._add_watermark)

>>>>>>> refactercode
