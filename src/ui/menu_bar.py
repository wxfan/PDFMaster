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

        # AI menu
        ai_menu = self.main_window.menuBar().addMenu("AI工具")
        ai_menu.addAction("生成摘要", self.main_window._summary_text)
        ai_menu.addAction("提取文本",self.main_window._ocr_text)
        ai_menu.addAction("配置LLM", self.main_window.settings_llm)  # Added LLM settings action






