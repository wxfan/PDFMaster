from pathlib import Path
import fitz  # type:ignore

from io import BytesIO
from PIL import Image, ImageEnhance
import os

def add_watermark(
    input_path,
    output_dir,
    watermark_text=None,
    watermark_image_path=None,
    rotation=0,  
    opacity=0.3,
    text_fontsize=48,
    image_width=200,
    image_height=None,
):
    """
    Add watermark to PDF file
    """
    if not watermark_text and not watermark_image_path:
        raise ValueError("Please provide either text or image for the watermark")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        doc = fitz.open(input_path)

        if doc.page_count == 0:
            raise ValueError("PDF 文件为空或已损坏，请检查文件并重试")

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            rect = page.rect

            overlay = fitz.open()
            overlay_page = overlay.new_page(width=rect.width, height=rect.height)

            if watermark_text:
                # 计算文本中心位置
                text_width = fitz.get_text_length(watermark_text, fontsize=text_fontsize, fontname="helv")
                text_height = text_fontsize
                center_x = (rect.width - text_width) / 2
                center_y = (rect.height - text_height) / 2

                # 插入文本并旋转
                overlay_page.insert_text(
                    (center_x, center_y),
                    watermark_text,
                    fontname="helv",
                    fontsize=text_fontsize,
                    rotate=rotation,  # 旋转文本
                    color = (0.0/255, 0.0/255, 0.0/255,opacity)
                )

            if watermark_image_path:
                try:
                    img = Image.open(watermark_image_path).convert("RGBA")
                    img = ImageEnhance.Brightness(img).enhance(opacity)
                    img = img.rotate(rotation, expand=True)

                    img_bytes = BytesIO()
                    img.save(img_bytes, format='PNG')
                    
                    if img_bytes.tell() == 0:
                        raise ValueError("生成的图片字节流为空")

                    img_pixmap = fitz.Pixmap(img_bytes.getvalue())

                    img_rect = fitz.Rect(
                        (rect.width - img.width) / 2,
                        (rect.height - img.height) / 2,
                        (rect.width + img.width) / 2,
                        (rect.height + img.height) / 2
                    )
                    overlay_page.insert_image(img_rect, pixmap=img_pixmap)
                except Exception as img_err:
                    print(f"处理图片水印时出错: {str(img_err)}")
                    continue  # 跳过当前页面，继续处理下一个页面

            page.show_pdf_page(rect, overlay, 0)

        output_path = os.path.join(output_dir, "watermarked.pdf")
        doc.save(output_path)
        doc.close()
        print(f"水印已成功添加并保存到 {output_path}")

    except ValueError as ve:
        print(f"无效操作: {str(ve)}")
        raise
    except Exception as e:
        print(f"添加水印失败: {str(e)}")
        raise