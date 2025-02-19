import fitz  # type:ignore
from pathlib import Path

def rotate_pdfs(input_path, output_path, degrees):
    """
    旋转 PDF 文件中的所有页面。

    :param input_path: 输入 PDF 文件路径
    :param output_path: 输出 PDF 文件路径
    :param degrees: 旋转角度（90, 180, 270）
    """
    # 打开 PDF 文件
    doc = fitz.open(input_path)
    
    # 验证旋转角度
    if degrees not in (90, 180, 270):
        raise ValueError("旋转角度必须是 90, 180 或 270 度")
    
    # 旋转每一页
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page.set_rotation(degrees)  # 使用 set_rotation 方法
    
    # 保存旋转后的 PDF
    doc.save(output_path)
    doc.close()