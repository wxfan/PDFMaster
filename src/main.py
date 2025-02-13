# src/main.py
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from PyQt6.QtCore import Qt

def main():
    # 高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 跨平台统一风格
    
    # 初始化主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()