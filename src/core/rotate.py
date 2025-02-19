from pathlib import Path
import fitz  # type: ignore

def rotate_pdfs(input_path: str, output_path: str, rotate_by: int = 90) -> bool:
    """
    旋转 PDF 文件
    支持旋转角度：90, 180, 270, 0 (不旋转)
    
    :param input_path: 输入 PDF 文件路径
    :param output_path: 输出 PDF 文件路径
    :param rotate_by: 旋转角度，默认为 90 度
    :return: 旋转是否成功
    """
    try:
        # Open the PDF file
        doc = fitz.open(input_path)
        
        # 遍历所有页面进行旋转
        for page in doc:
            page.rotate(rotate_by)

        # 处理 90 和 270 度旋转时的页面尺寸调整
        if rotate_by in [90, 270]:
            # 获取第一页面的尺寸进行调整
            first_page = doc[0]
            rect = first_page.rect
            if rotate_by == 90:
                new_rect = fitz.Rect(0, 0, rect.height, rect.width)
            else:  # 270
                new_rect = fitz.Rect(0, 0, rect.width, rect.height)
            
            # 遍历所有页面进行尺寸调整
            for page in doc:
                page.set_rect(new_rect)

        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return True
        
    except Exception as e:
        raise RuntimeError(f"PDF旋转失败: {str(e)}")
