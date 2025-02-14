# PDFMaster - PDF 文档处理工具

一款功能强大的 PDF 文档处理工具，支持 PDF 文件的合并、拆分、页面提取，以及添加水印。

## 功能特点

- **PDF 合并**: 将多个 PDF 文件合并成一个 PDF 文件
- **PDF 拆分**: 按页码范围或逐页拆分 PDF 文件
- **页面提取**: 提取指定页码范围的 PDF 页面
- **书签保留**: 在合并 PDF 文件时可选择保留书签
- **添加水印**: 添加文字或图片水印到 PDF 文件的每一页

## 使用说明

1. 添加 PDF 文件：
   - 将文件拖拽到应用窗口内。
   - 或通过文件菜单选择“添加文件”进行添加。

2. 使用“PDF 处理”菜单进行操作：
   - **合并 PDF**: 将选中的文件合并为一个 PDF 文件。
   - **拆分 PDF**: 拆分选中的 PDF 文件，可选择逐页拆分或按范围拆分。
   - **提取页面**: 提取选中的 PDF 文件中的指定页码范围。
   - **添加水印**: 配置水印设置，选择水印类型、内容、位置、旋转角度和透明度。

3. 在弹出的配置对话框中完成相应设置后，点击“确定”开始处理。

4. 处理完成后的 PDF 文件将保存到指定的输出目录中。

## 安装指南

1. 克隆仓库：
   ```bash
   git clone https://github.com/username/PDFMaster.git
   ```

2. 安装依赖包：
   ```bash
   pip install pyqt6 pymupdf
   ```

3. 构建应用（可选）：
   ```bash
   python scripts/package.py
   ```

4. 运行应用：
   ```bash
   python src/main.py
   ```

## 项目依赖

- **Python 3.8+**
- **PyQt6** (版本 2.3.0 及以上)
- **PyMuPDF (fitz)** (版本 1.20.0 及以上)

## 项目许可

本项目采用 MIT 许可证，详细内容请查看 [LICENSE](LICENSE) 文件。

## 联系我们

如遇任何问题或有建议，请通过以下方式联系我们：
- 邮箱: support@pdfmaster.com
- GitHub Issues: [GitHub Issues](https://github.com/username/PDFMaster/issues)

## 致谢

由 ❤️ 使用 **PyQt6** 和 **PyMuPDF** 开发。
