from pathlib import Path
import fitz  # type: ignore

def rotate_pdfs(input_path: str, output_path: str, rotate_by: int = 90):
    """
    旋转 PDF 文件
    支持旋转角度：90, 180, 270, 0 (不旋转)
    
    :param input_path: 输入 PDF 文件路径
    :param output_path: 输出 PDF 文件路径
    :param rotate_by: 旋转角度，默认为 90 度
    """
    try:
        # Open the PDF file
        doc = fitz.open(input_path)
        
        # Iterate through all pages and rotate them
        for page in doc:
            rect = page.rect
            if rotate_by == 90:
                page.setRotation(90)  # 顺时针旋转90度
                new_rect = fitz.Rect(0, 0, rect.height, rect.width)
            elif rotate_by == 180:
                page.setRotation(180)
                new_rect = rect
            elif rotate_by == 270:
                page.setRotation(270)
                new_rect = fitz.Rect(0, 0, rect.height, rect.width)
            elif rotate_by == 0:
                # No rotation
                new_rect = rect
            else:
                raise ValueError("Invalid rotation angle. Use 90, 180, 270, or 0.")
            
            # Set the new page rectangle
            page.setRect(new_rect)
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
    except Exception as e:
        raise RuntimeError(f"PDF旋转失败: {str(e)}")
