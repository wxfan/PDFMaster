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
        
        # Get all pages at once
        pages = doc.pages()
        
        # Handle special cases for rectangle calculations
        if rotate_by in [90, 270]:
            # For 90/270 degrees, width and height are swapped
            page = next(pages)  # Get first page to calculate sizes
            if rotate_by == 90:
                new_width = page.rect.height
                new_height = page.rect.width
            else:  # 270
                new_width = page.rect.width
                new_height = page.rect.height
            del page  # Cleanup
            
            # Update all pages
            for page in doc:
                page.setRect(fitz.Rect(0, 0, new_width, new_height))
        
        # Rotate all pages at once
        try:
            doc.rotateAllPages(rotate_by)
        except Exception as e:
            raise RuntimeError(f"旋转失败: {str(e)}")
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        
        return True  # Success
        
    except Exception as e:
        raise RuntimeError(f"PDF旋转失败: {str(e)}")
